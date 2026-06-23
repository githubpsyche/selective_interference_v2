from __future__ import annotations

import csv
import os
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from jax import random
from jaxcmr.analyses.pnr import fixed_pres_pnr
from jaxcmr.analyses.spc import fixed_pres_spc
from jaxcmr.helpers import find_project_root

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
    save_figure,
    simulate_periodic_cued_free_recall,
    split_scales_for_cache,
    standard_remap,
    sweep_rngs,
)

warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

PROJECT_ROOT = Path(find_project_root())
FIT_PATH = PROJECT_ROOT / "results/fits/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"
FIGURE_DIR = PROJECT_ROOT / "figures"
RNG_SEED = 0

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
N_PRESENTED = N_FILM + N_BREAK + N_INTERFERENCE + N_FILLER
EXPERIMENT_COUNT = 5000
MAX_RECALL = 48

FILM_CUE_REINSTATEMENT = 0.90
CUE_INTERVAL = 4
FIRST_CUE_AFTER = 0
PRIMARY_SOURCE_ORIENTATION = 0.0
SELECTED_START_DRIFT = 1.5
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
    "rejected_recall_drift_scale": 1.0,
}

RETRIEVAL_SETTINGS = [
    {
        "label": "Unguided recall",
        "figure_label": "Unguided recall",
        "start_drift_scale": 0.0,
    },
    {
        "label": "Start-of-film context reinstatement",
        "figure_label": "Start-of-film context reinstatement",
        "start_drift_scale": SELECTED_START_DRIFT,
    },
]

CONDITIONS = [
    {
        "figure_str": "simulation2_start_context_reinstatement_just_reminder_candidate",
        "reminder_condition": "With reminder",
        "task_condition": "Weak task encoding",
        "task_mcf_scale": 1.0,
        "reminder_scales": {
            "reminder_start_drift_scale": 1.0,
            "reminder_drift_scale": 1.0,
        },
        "show_reminder_marker": True,
    },
    {
        "figure_str": "simulation2_start_context_reinstatement_just_strong_task_candidate",
        "reminder_condition": "No reminder",
        "task_condition": "Strong task encoding",
        "task_mcf_scale": 2.0,
        "reminder_scales": {
            "reminder_start_drift_scale": 0.0,
            "reminder_drift_scale": 0.0,
        },
        "show_reminder_marker": False,
    },
]


def position_phase_labels(paradigm):
    return (
        ["film"] * paradigm.n_film
        + ["break"] * paradigm.n_break
        + ["task"] * paradigm.n_interference
        + ["filler"] * paradigm.n_filler
    )


def write_rows(path, fieldnames, rows):
    os.makedirs(path.parent, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def phase_recall_totals(spc, position_phase):
    totals = {}
    for phase in sorted(set(position_phase)):
        positions = [idx for idx, value in enumerate(position_phase) if value == phase]
        totals[phase] = float(np.sum(spc[positions]))
    return totals


def retrieval_start_support_trial(model, rng, film_items, cue_scale):
    _, cue_rng = random.split(rng)
    model = model.start_retrieving()
    cue_item = random.choice(cue_rng, film_items)
    model = apply_supplied_item_context_cue(model, cue_item, cue_scale)
    support = model.mcf.probe(model.context.state)[: N_PRESENTED]
    return support


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


PANEL_LETTER_FONTSIZE = 16
PANEL_TITLE_FONTSIZE = 13
STRUCTURAL_FONTSIZE = 11
SUPPORT_FONTSIZE = 10

SETTING_STYLES = {
    "Unguided recall": {
        "color": "#7C8794",
        "linestyle": "--",
        "linewidth": 1.7,
    },
    "Start-of-film context reinstatement": {
        "color": "#222222",
        "linestyle": "-",
        "linewidth": 1.9,
    },
}


def add_panel_label(axis, label, x=-0.14, y=1.12):
    axis.text(
        x,
        y,
        label,
        transform=axis.transAxes,
        fontsize=PANEL_LETTER_FONTSIZE,
        fontweight="bold",
        va="top",
        ha="left",
    )


def add_phase_boundaries(axis, paradigm):
    boundaries = np.cumsum([
        paradigm.n_film,
        paradigm.n_break,
        paradigm.n_interference,
    ]) + 0.5
    for boundary in boundaries:
        axis.axvline(boundary, color="#7C8794", linewidth=0.7, alpha=0.45, zorder=1)


def add_reminder_marker(axis, paradigm):
    reminder_x = paradigm.n_film + paradigm.n_break + 0.5
    axis.axvline(
        reminder_x,
        color=PHASE_COLORS["reminder"],
        linewidth=1.6,
        alpha=0.85,
        zorder=2,
    )
    axis.text(
        reminder_x - 1.05,
        0.62,
        "Film reminder",
        ha="center",
        va="center",
        fontsize=STRUCTURAL_FONTSIZE,
        fontstyle="italic",
        color=PHASE_COLORS["reminder"],
        rotation=90,
        rotation_mode="anchor",
        transform=axis.get_xaxis_transform(),
        clip_on=False,
        zorder=3,
    )


def style_position_axis(axis, paradigm, position_phase, ylabel, title, show_reminder_marker, ylim=None):
    add_phase_bands(axis, position_phase, fontsize=SUPPORT_FONTSIZE)
    add_phase_boundaries(axis, paradigm)
    if show_reminder_marker:
        add_reminder_marker(axis, paradigm)
    axis.set_title(title, fontsize=PANEL_TITLE_FONTSIZE, pad=30)
    axis.set_xlabel("Encoded position", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_ylabel(ylabel, fontsize=STRUCTURAL_FONTSIZE)
    axis.set_xlim(1, len(position_phase))
    if ylim is not None:
        axis.set_ylim(*ylim)
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.set_axisbelow(True)
    axis.grid(axis="y", color="#E7EBF0", linewidth=0.45, alpha=0.45, zorder=0)


def plot_curves(axis, paradigm, position_phase, retrieval_settings, curves, ylabel, title, show_reminder_marker, ylim=None):
    style_position_axis(
        axis,
        paradigm,
        position_phase,
        ylabel,
        title,
        show_reminder_marker,
        ylim=ylim,
    )
    positions = np.arange(1, len(position_phase) + 1)
    for setting in retrieval_settings:
        label = setting["label"]
        style = SETTING_STYLES[label]
        axis.plot(
            positions,
            curves[label],
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            label=setting["figure_label"],
            zorder=3,
        )


def padded_ylim(curves, minimum_upper=0.05, lower=0.0):
    max_value = max(float(np.nanmax(curve)) for curve in curves.values())
    upper = max(minimum_upper, max_value * 1.16)
    return (lower, upper)


def render_condition(condition, params, factory, paradigm):
    position_phase = position_phase_labels(paradigm)
    n_presented = len(position_phase)
    batched_start_support = batch_trial(retrieval_start_support_trial, n_args=4)
    batched_cued_recall = batch_trial(cued_recall_trial, n_args=7, n_static=3)

    fixed_scales = {
        **BASE_FIXED_SCALES,
        **EXTRA_FIXED_SCALES,
        **condition["reminder_scales"],
        "interference_mcf_scale": float(condition["task_mcf_scale"]),
    }
    pre_cache_scales, post_cache_scales = split_scales_for_cache(fixed_scales, CACHE_AFTER)
    prepared = prepare_sweep(
        params,
        paradigm,
        factory,
        cache_after=CACHE_AFTER,
        **pre_cache_scales,
    )

    support_rows = []
    pfr_rows = []
    spc_rows = []
    phase_rows = []
    support_curves = {}
    pfr_curves = {}
    spc_curves = {}
    run_rng = random.PRNGKey(RNG_SEED + 20)

    common_metadata = {
        "reminder_condition": condition["reminder_condition"],
        "task_condition": condition["task_condition"],
        "task_mcf_scale": float(condition["task_mcf_scale"]),
        "film_cue_reinstatement": float(FILM_CUE_REINSTATEMENT),
        "first_cue_after": int(FIRST_CUE_AFTER),
        "cue_interval": int(CUE_INTERVAL),
        "film_source_start_drift_rate": float(PRIMARY_SOURCE_ORIENTATION),
        "rejected_recall_drift_scale": float(RETRIEVAL_FIXED_SCALES["rejected_recall_drift_scale"]),
    }

    for setting in RETRIEVAL_SETTINGS:
        start_drift_scale = float(setting["start_drift_scale"])
        ready_models = configure_rates(
            prepared.models,
            **post_cache_scales,
            **RETRIEVAL_FIXED_SCALES,
            start_drift_scale=start_drift_scale,
            film_source_start_drift_rate=float(PRIMARY_SOURCE_ORIENTATION),
        )
        rngs, run_rng = sweep_rngs(
            run_rng,
            prepared.n_subjects,
            prepared.experiment_count,
        )
        support = batched_start_support(
            ready_models,
            rngs,
            paradigm.film_items,
            FILM_CUE_REINSTATEMENT,
        )
        recalls, cue_attempts, cue_items = batched_cued_recall(
            ready_models,
            rngs,
            paradigm.film_items,
            FILM_CUE_REINSTATEMENT,
            paradigm.max_recall,
            CUE_INTERVAL,
            FIRST_CUE_AFTER,
        )

        support_matrix = np.asarray(support).reshape(-1, n_presented)
        support_curve = np.mean(support_matrix, axis=0)
        support_denom = float(np.sum(support_curve))
        support_share = (
            support_curve / support_denom
            if support_denom > 0
            else np.full_like(support_curve, np.nan)
        )

        raw_recalls = np.asarray(recalls).reshape(-1, recalls.shape[-1])
        remapped_recalls = np.asarray(
            standard_remap(
                raw_recalls,
                paradigm,
                show_break=True,
            )
        )
        pfr = np.asarray(
            fixed_pres_pnr(
                remapped_recalls,
                n_presented,
                query_recall_position=0,
            ),
            dtype=float,
        )
        spc = np.asarray(fixed_pres_spc(remapped_recalls, n_presented), dtype=float)
        totals = phase_recall_totals(spc, position_phase)

        key = setting["label"]
        support_curves[key] = support_curve
        pfr_curves[key] = pfr
        spc_curves[key] = spc

        for phase, total in totals.items():
            phase_rows.append({
                **common_metadata,
                "retrieval_setting": key,
                "start_drift_scale": start_drift_scale,
                "phase": phase,
                "recall_probability_mass": total,
            })

        for position, phase in enumerate(position_phase, start=1):
            support_rows.append({
                **common_metadata,
                "retrieval_setting": key,
                "start_drift_scale": start_drift_scale,
                "position": position,
                "phase": phase,
                "raw_support": float(support_curve[position - 1]),
                "support_share": float(support_share[position - 1]),
            })
            pfr_rows.append({
                **common_metadata,
                "retrieval_setting": key,
                "start_drift_scale": start_drift_scale,
                "position": position,
                "phase": phase,
                "first_recall_probability": float(pfr[position - 1]),
            })
            spc_rows.append({
                **common_metadata,
                "retrieval_setting": key,
                "start_drift_scale": start_drift_scale,
                "position": position,
                "phase": phase,
                "recall_probability": float(spc[position - 1]),
            })

    prefix = condition["figure_str"]
    write_rows(
        FIGURE_DIR / f"{prefix}_support.csv",
        [
            *common_metadata.keys(),
            "retrieval_setting",
            "start_drift_scale",
            "position",
            "phase",
            "raw_support",
            "support_share",
        ],
        support_rows,
    )
    write_rows(
        FIGURE_DIR / f"{prefix}_pfr.csv",
        [
            *common_metadata.keys(),
            "retrieval_setting",
            "start_drift_scale",
            "position",
            "phase",
            "first_recall_probability",
        ],
        pfr_rows,
    )
    write_rows(
        FIGURE_DIR / f"{prefix}_spc.csv",
        [
            *common_metadata.keys(),
            "retrieval_setting",
            "start_drift_scale",
            "position",
            "phase",
            "recall_probability",
        ],
        spc_rows,
    )
    write_rows(
        FIGURE_DIR / f"{prefix}_phase_totals.csv",
        [
            *common_metadata.keys(),
            "retrieval_setting",
            "start_drift_scale",
            "phase",
            "recall_probability_mass",
        ],
        phase_rows,
    )

    fig = plt.figure(figsize=(11.2, 7.15))
    gs = fig.add_gridspec(
        2,
        4,
        height_ratios=[1.0, 1.0],
        hspace=0.62,
        wspace=0.58,
        left=0.095,
        right=0.945,
        top=0.900,
        bottom=0.105,
    )
    axis_a = fig.add_subplot(gs[0, 0:2])
    axis_b = fig.add_subplot(gs[0, 2:4])
    axis_c = fig.add_subplot(gs[1, 1:3])

    show_marker = bool(condition["show_reminder_marker"])
    plot_curves(
        axis_a,
        paradigm,
        position_phase,
        RETRIEVAL_SETTINGS,
        support_curves,
        "Retrieval support",
        "Item accessibility before first recall",
        show_marker,
        ylim=padded_ylim(support_curves, minimum_upper=0.2),
    )
    add_panel_label(axis_a, "A")

    plot_curves(
        axis_b,
        paradigm,
        position_phase,
        RETRIEVAL_SETTINGS,
        pfr_curves,
        "Probability of first recall",
        "First recall probability distribution",
        show_marker,
        ylim=padded_ylim(pfr_curves, minimum_upper=0.05, lower=-0.005),
    )
    add_panel_label(axis_b, "B")

    plot_curves(
        axis_c,
        paradigm,
        position_phase,
        RETRIEVAL_SETTINGS,
        spc_curves,
        "Recall probability",
        "Overall recall probability distribution",
        show_marker,
        ylim=padded_ylim(spc_curves, minimum_upper=0.2, lower=-0.02),
    )
    add_panel_label(axis_c, "C")

    axis_c.legend(
        frameon=False,
        fontsize=SUPPORT_FONTSIZE,
        loc="center left",
        bbox_to_anchor=(1.035, 0.52),
        ncol=1,
        handlelength=2.0,
        borderaxespad=0.0,
    )

    save_figure(str(FIGURE_DIR), prefix)


def main():
    params, n_subjects = load_fit_params(FIT_PATH)
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
            film_emotional=True,
            interference_emotional=False,
        ),
        is_target=make_is_target(paradigm),
    )
    print(f"Loaded {n_subjects} fit parameter set(s).")
    for condition in CONDITIONS:
        print(f"Rendering {condition['figure_str']}")
        render_condition(condition, params, factory, paradigm)


if __name__ == "__main__":
    main()
