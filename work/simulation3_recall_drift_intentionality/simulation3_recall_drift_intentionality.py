"""Generate a Simulation 3 recall-drift intentionality figure.

This figure compares unguided retrieval with deliberate recall while sweeping
target-item post-recall context drift. It uses the same post-reminder task-encoding regime
as the film-cue figure, but without intermittent supplied film cues.
"""

from __future__ import annotations

import csv
import os
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from jax import random
from jaxcmr.analyses.spc import fixed_pres_spc
from jaxcmr.helpers import find_project_root

SCRIPT_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(SCRIPT_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_PROJECT_ROOT))

from selective_interference_v2 import (
    PHASE_COLORS,
    Paradigm,
    add_phase_bands,
    batch_trial,
    configure_rates,
    light_to_dark_colors,
    load_fit_params,
    make_factory,
    make_is_emotional,
    make_is_target,
    prepare_sweep,
    run_sweep,
    simulate_periodic_cued_free_recall,
    save_figure,
    split_scales_for_cache,
    standard_remap,
    sweep_rngs,
)

warnings.filterwarnings("ignore")


# --- configuration ---------------------------------------------------------
PROJECT_ROOT = os.environ.get("PROJECT_ROOT", "")
FIT_PATH = os.environ.get(
    "FIT_PATH",
    "work/fitting/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json",
)
FIGURE_DIR = os.environ.get("FIGURE_DIR", "work/simulation3_recall_drift_intentionality")
DATA_DIR = os.environ.get("FIGURE_DATA_DIR", "work/simulation3_recall_drift_intentionality")
FIGURE_STR = os.environ.get(
    "FIGURE_STR",
    "simulation3_recall_drift_intentionality",
)
RNG_SEED = int(os.environ.get("RNG_SEED", "0"))

SWEEP_VALUES = np.asarray([0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.0])
SWEEP_PARAM = os.environ.get("SWEEP_PARAM", "target_recall_drift_scale")
if SWEEP_PARAM not in {
    "target_recall_drift_scale",
    "rejected_recall_drift_scale",
    "target_offtarget_recall_drift_gap",
}:
    raise ValueError(
        "SWEEP_PARAM must be 'target_recall_drift_scale' "
        "'rejected_recall_drift_scale', or "
        "'target_offtarget_recall_drift_gap'"
    )
SWEEP_COLUMN = (
    "target_offtarget_recall_drift_gap"
    if SWEEP_PARAM == "target_offtarget_recall_drift_gap"
    else
    "off_target_recall_drift_scale"
    if SWEEP_PARAM == "rejected_recall_drift_scale"
    else "target_recall_drift_scale"
)
SWEEP_XLABEL = (
    "Film minus off-target\nrecall drift gap"
    if SWEEP_PARAM == "target_offtarget_recall_drift_gap"
    else
    "Off-target recall\ndrift scale"
    if SWEEP_PARAM == "rejected_recall_drift_scale"
    else "Film recall\ndrift scale"
)
SUMMARY_XLABEL = SWEEP_XLABEL.replace("\n", " ")
SWEEP_LABEL_FMT = "{:.2f}"

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
EXPERIMENT_COUNT = int(os.environ.get("EXPERIMENT_COUNT", "5000"))
MAX_RECALL = 48
OFF_TARGET_RECALL_DRIFT_SCALE = float(
    os.environ.get("OFF_TARGET_RECALL_DRIFT_SCALE", "0.25")
)
TARGET_RECALL_DRIFT_SCALE = float(os.environ.get("TARGET_RECALL_DRIFT_SCALE", "1.0"))
USE_PERIODIC_CUES = os.environ.get("USE_PERIODIC_CUES", "0") == "1"
FILM_CUE_REINSTATEMENT = float(os.environ.get("FILM_CUE_REINSTATEMENT", "0.675"))
CUE_INTERVAL = int(os.environ.get("CUE_INTERVAL", "4"))
FIRST_CUE_AFTER = int(os.environ.get("FIRST_CUE_AFTER", "4"))

TASK_MCF_SCALE = 2.0
FILM_EMOTIONAL = True
INTERFERENCE_EMOTIONAL = False
CACHE_AFTER = "filler"

LOW_RETRIEVAL_LABEL = os.environ.get("LOW_RETRIEVAL_LABEL", "Unguided retrieval")
HIGH_RETRIEVAL_LABEL = os.environ.get("HIGH_RETRIEVAL_LABEL", "Deliberate recall")
LOW_START_DRIFT_SCALE = float(os.environ.get("LOW_START_DRIFT_SCALE", "0.0"))
HIGH_START_DRIFT_SCALE = float(os.environ.get("HIGH_START_DRIFT_SCALE", "1.0"))
RETRIEVAL_CONDITIONS = {
    LOW_RETRIEVAL_LABEL: LOW_START_DRIFT_SCALE,
    HIGH_RETRIEVAL_LABEL: HIGH_START_DRIFT_SCALE,
}

FIXED_SCALES = {
    "break_drift_scale": 1.0,
    "break_mcf_scale": 1.0,
    "reminder_start_drift_scale": 1.0,
    "reminder_drift_scale": 1.0,
    "interference_mcf_scale": TASK_MCF_SCALE,
    "filler_drift_scale": 1.0,
    "filler_mcf_scale": 1.0,
    "source_learning_baseline": 0.05,
    "film_source_start_drift_rate": 0.5,
    "primacy_scale": 0.1,
    "primacy_decay": 1.5,
}

CONDITION_COLORS = {
    LOW_RETRIEVAL_LABEL: "#4A5563",
    HIGH_RETRIEVAL_LABEL: PHASE_COLORS["film"],
}


def position_phase_labels(paradigm: Paradigm) -> list[str]:
    return (
        ["film"] * paradigm.n_film
        + ["break"] * paradigm.n_break
        + ["task"] * paradigm.n_interference
        + ["filler"] * paradigm.n_filler
    )


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def phase_recall_totals(
    spc: np.ndarray,
    position_phase: list[str],
) -> dict[str, float]:
    totals = {}
    for phase in sorted(set(position_phase)):
        positions = [idx for idx, value in enumerate(position_phase) if value == phase]
        totals[phase] = float(np.sum(spc[positions]))
    return totals


def add_panel_label(axis, label: str, x: float = -0.12, y: float = 1.14) -> None:
    axis.text(
        x,
        y,
        label,
        transform=axis.transAxes,
        fontsize=18,
        fontweight="bold",
        va="top",
        ha="left",
    )


def add_phase_boundaries(axis, paradigm: Paradigm) -> None:
    boundaries = np.cumsum([
        paradigm.n_film,
        paradigm.n_break,
        paradigm.n_interference,
    ]) + 0.5
    for boundary in boundaries:
        axis.axvline(boundary, color="#7C8794", linewidth=0.7, alpha=0.45, zorder=1)


def add_reminder_marker(axis, paradigm: Paradigm, show_label: bool = True) -> None:
    reminder_x = paradigm.n_film + paradigm.n_break + 0.5
    axis.axvline(
        reminder_x,
        color=PHASE_COLORS["reminder"],
        linewidth=1.8,
        alpha=0.85,
        zorder=2,
    )
    if show_label:
        axis.text(
            reminder_x - 1.05,
            0.61,
            "Film reminder",
            ha="center",
            va="center",
            fontsize=12,
            fontstyle="italic",
            color=PHASE_COLORS["reminder"],
            rotation=90,
            rotation_mode="anchor",
            transform=axis.get_xaxis_transform(),
            clip_on=False,
            zorder=3,
        )


def style_spc_axis(
    axis,
    paradigm: Paradigm,
    position_phase: list[str],
    title: str,
    ylabel: str | None = None,
) -> None:
    add_phase_bands(axis, position_phase, fontsize=12)
    add_phase_boundaries(axis, paradigm)
    add_reminder_marker(axis, paradigm)
    axis.set_title(title, fontsize=14, pad=36)
    axis.set_xlabel("Encoded position", fontsize=12)
    if ylabel is not None:
        axis.set_ylabel(ylabel, fontsize=12)
    axis.set_xlim(1, len(position_phase))
    axis.set_ylim(-0.025, 0.75)
    axis.tick_params(labelsize=10)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def plot_spc_sweep(
    axis,
    curves: list[np.ndarray],
    paradigm: Paradigm,
    position_phase: list[str],
    title: str,
    ylabel: str | None = None,
) -> None:
    style_spc_axis(axis, paradigm, position_phase, title, ylabel=ylabel)
    colors = light_to_dark_colors(len(SWEEP_VALUES))
    positions = np.arange(1, len(position_phase) + 1)
    for color, value, curve in zip(colors, SWEEP_VALUES, curves):
        axis.plot(
            positions,
            curve,
            color=color,
            linewidth=1.4,
            label=SWEEP_LABEL_FMT.format(value),
        )


def phase_total(
    phase_rows: list[dict],
    retrieval_condition: str,
    sweep_value: float,
    phase: str,
) -> float:
    matches = [
        row for row in phase_rows
        if row["retrieval_condition"] == retrieval_condition
        and np.isclose(
            row[SWEEP_COLUMN],
            sweep_value,
        )
        and row["phase"] == phase
    ]
    if not matches:
        return np.nan
    return float(matches[0]["recall_probability_mass"])


def plot_film_mass_panel(axis_recall, axis_gap, phase_rows: list[dict]) -> None:
    film_by_condition = {}
    for retrieval_condition in RETRIEVAL_CONDITIONS:
        values = np.asarray([
            phase_total(
                phase_rows,
                retrieval_condition,
                sweep_value,
                "film",
            )
            for sweep_value in SWEEP_VALUES
        ])
        film_by_condition[retrieval_condition] = values
        axis_recall.plot(
            SWEEP_VALUES,
            values,
            marker="o",
            linewidth=1.9,
            markersize=4.8,
            color=CONDITION_COLORS[retrieval_condition],
            label=retrieval_condition,
        )

    gap = film_by_condition[HIGH_RETRIEVAL_LABEL] - film_by_condition[LOW_RETRIEVAL_LABEL]
    axis_gap.plot(
        SWEEP_VALUES,
        gap,
        marker="o",
        linewidth=1.8,
        markersize=4.8,
        color="#2F3B4A",
    )

    axis_recall.set_title("Film recall", fontsize=10, pad=6)
    axis_recall.set_xlabel(SUMMARY_XLABEL, fontsize=10)
    axis_recall.set_ylabel("Film recall mass", fontsize=10)
    axis_recall.set_xlim(float(np.min(SWEEP_VALUES)), float(np.max(SWEEP_VALUES)))
    axis_recall.set_ylim(
        0,
        max(3.25, float(np.nanmax([*film_by_condition.values()])) + 0.35),
    )
    x_ticks = np.linspace(float(np.min(SWEEP_VALUES)), float(np.max(SWEEP_VALUES)), 4)
    axis_recall.set_xticks(x_ticks)
    axis_recall.set_xticklabels([f"{value:.2f}" for value in x_ticks])
    axis_recall.tick_params(labelsize=8.5)
    axis_recall.grid(axis="y", color="#D6DBE1", linewidth=0.7, alpha=0.7)
    axis_recall.spines["top"].set_visible(False)
    axis_recall.spines["right"].set_visible(False)
    axis_recall.legend(
        frameon=False,
        fontsize=8.5,
        loc="upper left",
        bbox_to_anchor=(0.00, 0.98),
        handlelength=1.1,
        borderpad=0.1,
        labelspacing=0.25,
    )

    axis_gap.set_title("Intentionality gap", fontsize=10, pad=6)
    axis_gap.set_xlabel(SUMMARY_XLABEL, fontsize=10)
    axis_gap.set_ylabel("Deliberate - unguided", fontsize=8.5)
    axis_gap.set_xlim(float(np.min(SWEEP_VALUES)), float(np.max(SWEEP_VALUES)))
    axis_gap.set_ylim(0, max(2.6, float(np.nanmax(gap)) + 0.25))
    axis_gap.set_xticks(x_ticks)
    axis_gap.set_xticklabels([f"{value:.2f}" for value in x_ticks])
    axis_gap.tick_params(labelsize=8.5)
    axis_gap.grid(axis="y", color="#D6DBE1", linewidth=0.7, alpha=0.7)
    axis_gap.spines["top"].set_visible(False)
    axis_gap.spines["right"].set_visible(False)


def plot_paradigm_extension(axis) -> None:
    axis.axis("off")
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.set_title("Intermittent test-phase film cues", fontsize=14, pad=12)

    x0 = 0.221
    step = 0.062
    y = 0.60
    cue_after = {FIRST_CUE_AFTER, FIRST_CUE_AFTER + CUE_INTERVAL}
    for attempt in range(1, 11):
        x = x0 + (attempt - 1) * step
        axis.add_patch(
            plt.Rectangle(
                (x - 0.020, y - 0.034),
                0.040,
                0.068,
                facecolor="white",
                edgecolor="#3D4B5C",
                linewidth=1.0,
            )
        )
        axis.text(
            x,
            y,
            str(attempt),
            ha="center",
            va="center",
            fontsize=10,
            color="#3D4B5C",
        )
        if attempt < 10:
            axis.plot(
                [x + 0.022, x + step - 0.022],
                [y, y],
                color="#9AA4B2",
                linewidth=0.8,
            )
        if attempt in cue_after:
            pulse_x = x + step / 2
            axis.plot(
                [pulse_x, pulse_x],
                [y - 0.13, y + 0.14],
                color=PHASE_COLORS["film"],
                linewidth=2.0,
            )
            axis.scatter(
                [pulse_x],
                [y + 0.14],
                marker="v",
                s=34,
                color=PHASE_COLORS["film"],
                zorder=3,
            )
            axis.text(
                pulse_x,
                y + 0.22,
                "film-item\ncue",
                ha="center",
                va="bottom",
                fontsize=10,
                color=PHASE_COLORS["film"],
                fontweight="bold",
            )

    axis.text(
        0.50,
        0.35,
        f"Cue after attempts {FIRST_CUE_AFTER}, {FIRST_CUE_AFTER + CUE_INTERVAL}, ...",
        ha="center",
        va="center",
        fontsize=10,
        color=PHASE_COLORS["film"],
    )

    schematic_y = 0.18
    box_h = 0.075
    box_specs = [
        (0.10, 0.22, "supplied cue", PHASE_COLORS["film"], "#EAF2FF"),
        (0.39, 0.22, "film context", PHASE_COLORS["reminder"], "#ECFDF3"),
        (0.68, 0.22, "next search", "#3D4B5C", "#F7F9FB"),
    ]
    for x, width, label, color, fill in box_specs:
        axis.add_patch(
            plt.Rectangle(
                (x, schematic_y),
                width,
                box_h,
                facecolor=fill,
                edgecolor=color,
                linewidth=1.1,
            )
        )
        axis.text(
            x + width / 2,
            schematic_y + box_h / 2,
            label,
            ha="center",
            va="center",
            fontsize=8.3,
            color=color,
            fontweight="bold" if color != "#3D4B5C" else "normal",
        )
    axis.annotate(
        "",
        xy=(0.39, schematic_y + box_h / 2),
        xytext=(0.32, schematic_y + box_h / 2),
        arrowprops={"arrowstyle": "->", "linewidth": 1.1, "color": "#3D4B5C"},
    )
    axis.annotate(
        "",
        xy=(0.68, schematic_y + box_h / 2),
        xytext=(0.61, schematic_y + box_h / 2),
        arrowprops={"arrowstyle": "->", "linewidth": 1.1, "color": "#3D4B5C"},
    )

    axis.text(
        0.50,
        0.075,
        "Cue is not a response slot and adds no new learning",
        ha="center",
        va="center",
        fontsize=8.5,
        color="#6B7280",
    )


def cued_recall_trial(
    model,
    rng,
    film_items,
    cue_scale,
    max_recall,
    cue_interval,
    first_cue_after,
):
    model = model.start_retrieving()
    _, recalls, _, _ = simulate_periodic_cued_free_recall(
        model,
        max_recall,
        rng,
        film_items,
        cue_scale,
        cue_interval=cue_interval,
        first_cue_after=first_cue_after,
    )
    return recalls


batched_cued_recall = batch_trial(cued_recall_trial, n_args=7, n_static=3)


def retrieval_scales_for_value(start_drift_scale: float, value: float) -> dict[str, float]:
    scales = {
        "start_drift_scale": start_drift_scale,
        "rejected_recall_drift_scale": OFF_TARGET_RECALL_DRIFT_SCALE,
        "target_recall_drift_scale": TARGET_RECALL_DRIFT_SCALE,
    }
    if SWEEP_PARAM == "target_offtarget_recall_drift_gap":
        scales["target_recall_drift_scale"] = TARGET_RECALL_DRIFT_SCALE
        scales["rejected_recall_drift_scale"] = max(
            0.0,
            TARGET_RECALL_DRIFT_SCALE * (1.0 - float(value)),
        )
    else:
        scales[SWEEP_PARAM] = float(value)
    return scales


def run_recall_drift_sweep(
    prepared,
    rng,
    paradigm: Paradigm,
    post_cache_scales: dict,
    start_drift_scale: float,
):
    if not USE_PERIODIC_CUES and SWEEP_PARAM != "target_offtarget_recall_drift_gap":
        fixed_retrieval_scales = retrieval_scales_for_value(start_drift_scale, 0.0)
        fixed_retrieval_scales.pop(SWEEP_PARAM)
        return run_sweep(
            prepared,
            rng,
            **post_cache_scales,
            **fixed_retrieval_scales,
            **{SWEEP_PARAM: SWEEP_VALUES},
        )

    results = []
    for value in SWEEP_VALUES:
        ready = configure_rates(
            prepared.models,
            **post_cache_scales,
            **retrieval_scales_for_value(start_drift_scale, float(value)),
        )
        rngs, rng = sweep_rngs(
            rng,
            prepared.n_subjects,
            prepared.experiment_count,
        )
        if USE_PERIODIC_CUES:
            recalls = batched_cued_recall(
                ready,
                rngs,
                paradigm.film_items,
                FILM_CUE_REINSTATEMENT,
                paradigm.max_recall,
                CUE_INTERVAL,
                FIRST_CUE_AFTER,
            )
        else:
            recalls = prepared.batched(ready, rngs, *prepared.item_args)
        results.append(recalls)
    return np.asarray(results), rng


def main() -> None:
    if PROJECT_ROOT:
        project_root = Path(PROJECT_ROOT)
    else:
        project_root = Path(__file__).resolve().parents[2]

    fit_path = project_root / FIT_PATH
    figure_dir = project_root / FIGURE_DIR if FIGURE_DIR else None
    data_dir = project_root / DATA_DIR if DATA_DIR else None

    params, n_subjects = load_fit_params(fit_path)
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
    rng = random.PRNGKey(RNG_SEED)

    pre_cache_scales, post_cache_scales = split_scales_for_cache(
        FIXED_SCALES,
        CACHE_AFTER,
    )
    prepared = prepare_sweep(
        params,
        paradigm,
        factory,
        cache_after=CACHE_AFTER,
        **pre_cache_scales,
    )

    position_phase = position_phase_labels(paradigm)
    n_presented = len(position_phase)
    spc_rows: list[dict] = []
    phase_rows: list[dict] = []
    gap_rows: list[dict] = []
    spc_curves: dict[str, list[np.ndarray]] = {}

    for retrieval_condition, start_drift_scale in RETRIEVAL_CONDITIONS.items():
        recalls, rng = run_recall_drift_sweep(
            prepared,
            rng,
            paradigm,
            post_cache_scales,
            start_drift_scale,
        )
        recalls = np.asarray(recalls)
        condition_curves = []
        for value_index, sweep_value in enumerate(SWEEP_VALUES):
            raw_recalls = recalls[value_index].reshape(-1, recalls.shape[-1])
            remapped_recalls = np.asarray(
                standard_remap(
                    raw_recalls,
                    paradigm,
                    show_break=True,
                )
            )
            spc = np.asarray(
                fixed_pres_spc(remapped_recalls, n_presented),
                dtype=float,
            )
            condition_curves.append(spc)
            totals = phase_recall_totals(spc, position_phase)

            for position, phase in enumerate(position_phase, start=1):
                spc_rows.append({
                    "retrieval_condition": retrieval_condition,
                    SWEEP_COLUMN: float(sweep_value),
                    "position": position,
                    "phase": phase,
                    "recall_probability": spc[position - 1],
                })
            for phase, total in totals.items():
                phase_rows.append({
                    "retrieval_condition": retrieval_condition,
                    SWEEP_COLUMN: float(sweep_value),
                    "phase": phase,
                    "recall_probability_mass": total,
                })
        spc_curves[retrieval_condition] = condition_curves

    for sweep_value in SWEEP_VALUES:
        low_start = phase_total(
            phase_rows,
            LOW_RETRIEVAL_LABEL,
            sweep_value,
            "film",
        )
        high_start = phase_total(
            phase_rows,
            HIGH_RETRIEVAL_LABEL,
            sweep_value,
            "film",
        )
        gap_rows.append({
            SWEEP_COLUMN: float(sweep_value),
            "low_start_label": LOW_RETRIEVAL_LABEL,
            "high_start_label": HIGH_RETRIEVAL_LABEL,
            "low_start_scale": LOW_START_DRIFT_SCALE,
            "high_start_scale": HIGH_START_DRIFT_SCALE,
            "low_start_film_mass": low_start,
            "high_start_film_mass": high_start,
            "intentionality_gap": high_start - low_start,
        })

    if data_dir is not None and FIGURE_STR:
        write_rows(
            data_dir / f"{FIGURE_STR}_spc.csv",
            [
                "retrieval_condition",
                SWEEP_COLUMN,
                "position",
                "phase",
                "recall_probability",
            ],
            spc_rows,
        )
        write_rows(
            data_dir / f"{FIGURE_STR}_phase_totals.csv",
            [
                "retrieval_condition",
                SWEEP_COLUMN,
                "phase",
                "recall_probability_mass",
            ],
            phase_rows,
        )
        write_rows(
            data_dir / f"{FIGURE_STR}_intentionality_gap.csv",
            [
                SWEEP_COLUMN,
                "low_start_label",
                "high_start_label",
                "low_start_scale",
                "high_start_scale",
                "low_start_film_mass",
                "high_start_film_mass",
                "intentionality_gap",
            ],
            gap_rows,
        )

    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(
        2,
        5,
        width_ratios=[1.0, 1.0, 1.0, 1.0, 0.48],
        height_ratios=[1.10, 0.92],
        hspace=0.55,
        wspace=0.75,
    )
    axis_a = fig.add_subplot(gs[0, 0:2])
    axis_b = fig.add_subplot(gs[0, 2:4], sharex=axis_a, sharey=axis_a)
    gs_c = gs[1, 0:2].subgridspec(1, 2, wspace=0.45)
    axis_c_recall = fig.add_subplot(gs_c[0, 0])
    axis_c_gap = fig.add_subplot(gs_c[0, 1])
    axis_d = fig.add_subplot(gs[1, 2:4])
    legend_axis = fig.add_subplot(gs[:, 4])
    legend_axis.axis("off")

    plot_spc_sweep(
        axis_a,
        spc_curves[LOW_RETRIEVAL_LABEL],
        paradigm,
        position_phase,
        LOW_RETRIEVAL_LABEL,
        ylabel="Recall probability",
    )
    plot_spc_sweep(
        axis_b,
        spc_curves[HIGH_RETRIEVAL_LABEL],
        paradigm,
        position_phase,
        HIGH_RETRIEVAL_LABEL,
    )
    plot_film_mass_panel(axis_c_recall, axis_c_gap, phase_rows)
    plot_paradigm_extension(axis_d)

    add_panel_label(axis_a, "A")
    add_panel_label(axis_b, "B")
    add_panel_label(axis_c_recall, "C", x=-0.18)
    add_panel_label(axis_d, "D")

    handles, labels = axis_a.get_legend_handles_labels()
    legend = legend_axis.legend(
        handles,
        labels,
        title=SWEEP_XLABEL,
        loc="upper left",
        fontsize=10,
        title_fontsize=10,
    )
    legend.get_title().set_multialignment("center")
    legend.get_title().set_ha("center")

    save_figure(str(figure_dir) if figure_dir is not None else "", FIGURE_STR)


if __name__ == "__main__":
    main()
