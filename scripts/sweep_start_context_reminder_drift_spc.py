from __future__ import annotations

import csv
import os
from pathlib import Path

from jax import random
from jaxcmr.analyses.spc import fixed_pres_spc
from jaxcmr.helpers import find_project_root
import matplotlib.pyplot as plt
import numpy as np

from selective_interference_v2 import (
    PHASE_COLORS,
    Paradigm,
    add_phase_bands,
    apply_supplied_item_context_cue,
    batch_trial,
    configure_rates,
    load_fit_params,
    make_factory,
    make_is_emotional,
    make_is_target,
    prepare_sweep,
    simulate_periodic_cued_free_recall,
    split_scales_for_cache,
    standard_remap,
    sweep_rngs,
)


PROJECT_ROOT = ""
FIT_PATH = "results/fits/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"
FIGURE_DIR = "figures"
OUTPUT_PREFIX = "simulation2_start_context_reminder_drift_sweep_spc"
RNG_SEED = 0

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
EXPERIMENT_COUNT = int(os.environ.get("REMINDER_DRIFT_SWEEP_EXPERIMENT_COUNT", "5000"))
MAX_RECALL = 48

TASK_MCF_SCALE = 2.0
REMINDER_START_DRIFT_SCALE = 1.0
REMINDER_DRIFT_SCALES = [
    float(value)
    for value in os.environ.get(
        "REMINDER_DRIFT_SWEEP_VALUES",
        "0,0.25,0.5,0.75,1.0,1.5,2.0",
    ).split(",")
    if value.strip()
]

START_DRIFT_SCALE = 1.5
REJECTED_RECALL_DRIFT_SCALE = 1.0
PRIMARY_SOURCE_ORIENTATION = 0.0
FILM_CUE_REINSTATEMENT = 0.90
CUE_INTERVAL = 4
FIRST_CUE_AFTER = 0

FILM_EMOTIONAL = True
INTERFERENCE_EMOTIONAL = False
CACHE_AFTER = "filler"

EXTRA_FIXED_SCALES = {
    "source_learning_baseline": 0.05,
    "primacy_scale": 0.1,
    "primacy_decay": 1.5,
}

BASE_FIXED_SCALES = {
    "break_drift_scale": 1.0,
    "break_mcf_scale": 1.0,
    "filler_drift_scale": 1.0,
    "filler_mcf_scale": 1.0,
}

RETRIEVAL_FIXED_SCALES = {
    "tau_scale": 1.0,
    "target_recall_drift_scale": 1.0,
    "recall_drift_scale": 1.0,
    "rejected_recall_drift_scale": REJECTED_RECALL_DRIFT_SCALE,
}


def project_root() -> Path:
    return Path(PROJECT_ROOT).expanduser() if PROJECT_ROOT else Path(find_project_root())


def position_phase_labels(paradigm: Paradigm) -> list[str]:
    return (
        ["film"] * paradigm.n_film
        + ["break"] * paradigm.n_break
        + ["task"] * paradigm.n_interference
        + ["filler"] * paradigm.n_filler
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cued_recall_trial(
    model,
    rng,
    film_items,
    cue_scale,
    max_recall,
    cue_interval,
    first_cue_after,
):
    recall_rng, initial_cue_rng = random.split(rng)
    model = model.start_retrieving()
    if first_cue_after == 0:
        cue_item = random.choice(initial_cue_rng, film_items)
        model = apply_supplied_item_context_cue(model, cue_item, cue_scale)
        scheduled_first_cue_after = cue_interval
    else:
        scheduled_first_cue_after = first_cue_after
    _, recalls, cue_attempts, cue_items = simulate_periodic_cued_free_recall(
        model,
        max_recall,
        recall_rng,
        film_items,
        cue_scale,
        cue_interval=cue_interval,
        first_cue_after=scheduled_first_cue_after,
    )
    return recalls, cue_attempts, cue_items


batched_cued_recall = batch_trial(cued_recall_trial, n_args=7, n_static=3)


def phase_totals(spc: np.ndarray, position_phase: list[str]) -> dict[str, float]:
    totals = {}
    for phase in sorted(set(position_phase)):
        positions = [idx for idx, value in enumerate(position_phase) if value == phase]
        totals[phase] = float(np.sum(spc[positions]))
    return totals


def run_sweep():
    root = project_root()
    figure_dir = root / FIGURE_DIR
    fit_path = root / FIT_PATH

    params, _ = load_fit_params(fit_path)
    paradigm = Paradigm(
        n_film=N_FILM,
        n_break=N_BREAK,
        n_interference=N_INTERFERENCE,
        n_filler=N_FILLER,
        experiment_count=EXPERIMENT_COUNT,
        max_recall=MAX_RECALL,
    )
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=FILM_EMOTIONAL,
            interference_emotional=INTERFERENCE_EMOTIONAL,
        ),
        is_target=make_is_target(paradigm),
    )
    position_phase = position_phase_labels(paradigm)
    n_presented = len(position_phase)
    base_fixed_scales = {**BASE_FIXED_SCALES, **EXTRA_FIXED_SCALES}

    fit_encoding_drift = float(np.asarray(params["encoding_drift_rate"])[0])
    fit_start_drift = float(np.asarray(params["start_drift_rate"])[0])

    spc_curves = {}
    spc_rows = []
    phase_rows = []
    rng = random.PRNGKey(RNG_SEED + 9500)

    for reminder_drift_scale in REMINDER_DRIFT_SCALES:
        print(f"Running reminder_drift_scale={reminder_drift_scale:g}")
        fixed_scales = {
            **base_fixed_scales,
            "reminder_start_drift_scale": REMINDER_START_DRIFT_SCALE,
            "reminder_drift_scale": reminder_drift_scale,
            "interference_mcf_scale": TASK_MCF_SCALE,
        }
        pre_cache_scales, post_cache_scales = split_scales_for_cache(
            fixed_scales,
            CACHE_AFTER,
        )
        prepared = prepare_sweep(
            params,
            paradigm,
            factory,
            cache_after=CACHE_AFTER,
            **pre_cache_scales,
        )
        ready_models = configure_rates(
            prepared.models,
            **post_cache_scales,
            **RETRIEVAL_FIXED_SCALES,
            start_drift_scale=START_DRIFT_SCALE,
            film_source_start_drift_rate=PRIMARY_SOURCE_ORIENTATION,
        )
        rngs, rng = sweep_rngs(
            rng,
            prepared.n_subjects,
            prepared.experiment_count,
        )
        recalls, _, _ = batched_cued_recall(
            ready_models,
            rngs,
            paradigm.film_items,
            FILM_CUE_REINSTATEMENT,
            paradigm.max_recall,
            CUE_INTERVAL,
            FIRST_CUE_AFTER,
        )
        raw_recalls = np.asarray(recalls).reshape(-1, recalls.shape[-1])
        remapped_recalls = np.asarray(
            standard_remap(
                raw_recalls,
                paradigm,
                show_break=True,
            )
        )
        spc = np.asarray(fixed_pres_spc(remapped_recalls, n_presented), dtype=float)
        spc_curves[reminder_drift_scale] = spc
        metadata = {
            "reminder_start_drift_scale": REMINDER_START_DRIFT_SCALE,
            "reminder_start_drift_rate": REMINDER_START_DRIFT_SCALE * fit_start_drift,
            "reminder_drift_scale": reminder_drift_scale,
            "reminder_drift_rate": min(1.0, reminder_drift_scale * fit_encoding_drift),
            "task_mcf_scale": TASK_MCF_SCALE,
            "start_drift_scale": START_DRIFT_SCALE,
            "rejected_recall_drift_scale": REJECTED_RECALL_DRIFT_SCALE,
            "film_source_start_drift_rate": PRIMARY_SOURCE_ORIENTATION,
            "film_cue_reinstatement": FILM_CUE_REINSTATEMENT,
            "cue_interval": CUE_INTERVAL,
            "first_cue_after": FIRST_CUE_AFTER,
            "experiment_count": EXPERIMENT_COUNT,
        }
        for position, phase in enumerate(position_phase, start=1):
            spc_rows.append(
                {
                    **metadata,
                    "position": position,
                    "phase": phase,
                    "recall_probability": float(spc[position - 1]),
                }
            )
        for phase, total in phase_totals(spc, position_phase).items():
            phase_rows.append({**metadata, "phase": phase, "recall_probability_mass": total})

    output_base = figure_dir / OUTPUT_PREFIX
    write_rows(
        output_base.with_suffix(".csv"),
        [
            "reminder_start_drift_scale",
            "reminder_start_drift_rate",
            "reminder_drift_scale",
            "reminder_drift_rate",
            "task_mcf_scale",
            "start_drift_scale",
            "rejected_recall_drift_scale",
            "film_source_start_drift_rate",
            "film_cue_reinstatement",
            "cue_interval",
            "first_cue_after",
            "experiment_count",
            "position",
            "phase",
            "recall_probability",
        ],
        spc_rows,
    )
    write_rows(
        output_base.with_name(f"{OUTPUT_PREFIX}_phase_totals.csv"),
        [
            "reminder_start_drift_scale",
            "reminder_start_drift_rate",
            "reminder_drift_scale",
            "reminder_drift_rate",
            "task_mcf_scale",
            "start_drift_scale",
            "rejected_recall_drift_scale",
            "film_source_start_drift_rate",
            "film_cue_reinstatement",
            "cue_interval",
            "first_cue_after",
            "experiment_count",
            "phase",
            "recall_probability_mass",
        ],
        phase_rows,
    )
    return output_base, paradigm, position_phase, spc_curves, phase_rows


def add_reminder_marker(axis, paradigm: Paradigm) -> None:
    reminder_x = paradigm.n_film + paradigm.n_break + 0.5
    axis.axvline(
        reminder_x,
        color=PHASE_COLORS["reminder"],
        linewidth=1.5,
        alpha=0.85,
        zorder=2,
    )
    axis.text(
        reminder_x - 1.0,
        0.70,
        "Film reminder",
        ha="center",
        va="center",
        fontsize=9,
        fontstyle="italic",
        color=PHASE_COLORS["reminder"],
        rotation=90,
        rotation_mode="anchor",
        transform=axis.get_xaxis_transform(),
        clip_on=False,
        zorder=4,
    )


def plot_sweep(output_base: Path, paradigm: Paradigm, position_phase: list[str], spc_curves) -> None:
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
    fig, axis = plt.subplots(figsize=(9.2, 4.8))
    add_phase_bands(axis, position_phase, fontsize=9)
    boundaries = np.cumsum([paradigm.n_film, paradigm.n_break, paradigm.n_interference]) + 0.5
    for boundary in boundaries:
        axis.axvline(boundary, color="#7C8794", linewidth=0.75, alpha=0.45, zorder=1)
    add_reminder_marker(axis, paradigm)

    positions = np.arange(1, len(position_phase) + 1)
    colors = plt.cm.viridis(np.linspace(0.12, 0.88, len(spc_curves)))
    for color, (scale, curve) in zip(colors, sorted(spc_curves.items())):
        axis.plot(
            positions,
            curve,
            color=color,
            linewidth=1.8,
            label=f"{scale:g}",
            zorder=3,
        )
    axis.set_title(
        "Start-of-film reinstatement: pre-task reminder drift sweep",
        fontsize=13,
        pad=30,
    )
    axis.set_xlabel("Encoded position", fontsize=11)
    axis.set_ylabel("Recall probability", fontsize=11)
    axis.set_xlim(1, len(position_phase))
    upper = max(0.2, max(float(np.max(curve)) for curve in spc_curves.values()) * 1.18)
    axis.set_ylim(-0.01, upper)
    axis.tick_params(labelsize=9)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.grid(axis="y", color="#E7EBF0", linewidth=0.5, alpha=0.6, zorder=0)
    axis.legend(
        title="reminder_drift_scale",
        frameon=False,
        fontsize=9,
        title_fontsize=9,
        loc="center left",
        bbox_to_anchor=(1.01, 0.50),
    )
    fig.subplots_adjust(left=0.085, right=0.825, top=0.83, bottom=0.15)
    for ext in (".png", ".svg", ".pdf"):
        fig.savefig(output_base.with_suffix(ext), dpi=300)
    plt.close(fig)


def main() -> None:
    output_base, paradigm, position_phase, spc_curves, phase_rows = run_sweep()
    plot_sweep(output_base, paradigm, position_phase, spc_curves)
    print(output_base.with_suffix(".png"))
    print(output_base.with_suffix(".svg"))
    print(output_base.with_suffix(".csv"))
    print(output_base.with_name(f"{OUTPUT_PREFIX}_phase_totals.csv"))


if __name__ == "__main__":
    main()
