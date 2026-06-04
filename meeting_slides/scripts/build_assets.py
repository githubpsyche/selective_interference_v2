"""Build figure walkthrough assets for the meeting slide deck.

The whole-figure slides reuse the manuscript composites. Panel-focus slides are
exported from the same panel sources and composite-style layout decisions:
existing standalone Figure 1 panel files, Matplotlib composite figures rebuilt
from simulation sidecars for Figures 2-5, and the whole Figure 6 composite.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.transforms import Bbox

SLIDE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SLIDE_ROOT.parent
ASSET_DIR = SLIDE_ROOT / "assets"

sys.path.insert(0, str(PROJECT_ROOT))
from selective_interference_v2.plotting import (  # noqa: E402
    PHASE_COLORS,
    add_phase_bands,
    light_to_dark_colors,
)

PANEL_LETTER_FONTSIZE = 18
PANEL_TITLE_FONTSIZE = 14
STRUCTURAL_FONTSIZE = 12
SUPPORT_FONTSIZE = 10

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
N_PRESENTED = N_FILM + N_BREAK + N_INTERFERENCE + N_FILLER
POSITION_PHASE = (
    ["film"] * N_FILM
    + ["break"] * N_BREAK
    + ["task"] * N_INTERFERENCE
    + ["filler"] * N_FILLER
)


def reset_assets() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for path in ASSET_DIR.glob("figure*"):
        path.unlink()


def copy_asset(src: Path, dest_name: str) -> None:
    shutil.copyfile(src, ASSET_DIR / dest_name)


def save_panel_region(
    fig: plt.Figure,
    name: str,
    axes: list[plt.Axes],
    *,
    extra_artists: list[plt.Artist] | None = None,
    hide_artists: list[plt.Artist] | None = None,
    pad: float = 0.08,
) -> None:
    """Save a panel region from an already laid-out composite-style figure."""
    hidden: list[tuple[plt.Artist, bool]] = []
    for artist in hide_artists or []:
        hidden.append((artist, artist.get_visible()))
        artist.set_visible(False)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bboxes = [axis.get_tightbbox(renderer) for axis in axes]
    bboxes.extend(artist.get_tightbbox(renderer) for artist in extra_artists or [])
    display_bbox = Bbox.union(bboxes)
    inches_bbox = display_bbox.transformed(fig.dpi_scale_trans.inverted())
    inches_bbox = Bbox.from_extents(
        inches_bbox.x0 - pad,
        inches_bbox.y0 - pad,
        inches_bbox.x1 + pad,
        inches_bbox.y1 + pad,
    )

    base = ASSET_DIR / name
    fig.savefig(f"{base}.png", bbox_inches=inches_bbox, dpi=300)
    fig.savefig(f"{base}.svg", bbox_inches=inches_bbox)

    for artist, visible in hidden:
        artist.set_visible(visible)


def add_panel_label(axis: plt.Axes, label: str, x: float = -0.14, y: float = 1.14) -> None:
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


def add_phase_boundaries(axis: plt.Axes) -> None:
    for boundary in np.cumsum([N_FILM, N_BREAK, N_INTERFERENCE]) + 0.5:
        axis.axvline(boundary, color="#7C8794", linewidth=0.7, alpha=0.45, zorder=1)


def add_reminder_marker(axis: plt.Axes, show_label: bool = True) -> None:
    reminder_x = N_FILM + N_BREAK + 0.5
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


def style_position_axis(
    axis: plt.Axes,
    ylabel: str,
    title: str,
    *,
    ylim: tuple[float, float],
    show_reminder: bool = True,
) -> None:
    add_phase_bands(axis, POSITION_PHASE, fontsize=STRUCTURAL_FONTSIZE)
    add_phase_boundaries(axis)
    if show_reminder:
        add_reminder_marker(axis)
    axis.set_title(title, fontsize=PANEL_TITLE_FONTSIZE, pad=32)
    axis.set_xlabel("Encoded position", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_ylabel(ylabel, fontsize=STRUCTURAL_FONTSIZE)
    axis.set_xlim(1, N_PRESENTED)
    axis.set_ylim(*ylim)
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def plot_spc_lines(
    axis: plt.Axes,
    data: pd.DataFrame,
    value_col: str,
    value_label_fmt: str,
    *,
    ylabel: str = "Recall probability",
    title: str,
    ylim: tuple[float, float],
    show_reminder: bool = True,
    show_legend: bool = False,
    legend_title: str | None = None,
) -> None:
    values = sorted(data[value_col].unique())
    colors = light_to_dark_colors(len(values))
    style_position_axis(axis, ylabel, title, ylim=ylim, show_reminder=show_reminder)
    for color, value in zip(colors, values):
        curve = data[data[value_col] == value].sort_values("position")
        axis.plot(
            curve["position"],
            curve["recall_probability"],
            color=color,
            linewidth=1.4,
            label=value_label_fmt.format(value),
        )
    if show_legend:
        legend = axis.legend(
            title=legend_title,
            loc="upper left",
            bbox_to_anchor=(1.02, 1.0),
            fontsize=SUPPORT_FONTSIZE,
            title_fontsize=SUPPORT_FONTSIZE,
        )
        if legend.get_title():
            legend.get_title().set_multialignment("center")
            legend.get_title().set_ha("center")


def finish_composite_layout(fig: plt.Figure) -> None:
    """Match the manuscript notebooks' final layout pass before panel export."""
    fig.tight_layout()
    fig.canvas.draw()


def add_centered_legend_title(legend: plt.Legend) -> None:
    legend.get_title().set_multialignment("center")
    legend.get_title().set_ha("center")


def copy_whole_figures() -> None:
    whole_figures = {
        "figure1_whole.png": PROJECT_ROOT
        / "retrieved_context_account_figure"
        / "retrieved_context_account_composite.png",
        "figure2_whole.png": PROJECT_ROOT / "figures" / "simulation1_context_binding.png",
        "figure3_whole.png": PROJECT_ROOT / "figures" / "simulation2_start_context_reinstatement.png",
        "figure4_whole.png": PROJECT_ROOT / "figures" / "simulation2_retrieval_selectivity.png",
        "figure5_whole.png": PROJECT_ROOT / "figures" / "simulation3_film_cue_inclusion.png",
        "figure6_whole.png": PROJECT_ROOT / "figures" / "simulation4_test_format_schematic.png",
    }
    for dest, src in whole_figures.items():
        copy_asset(src, dest)


def copy_figure1_panels() -> None:
    panel_sources = {
        "figure1_a": "panel_a_phase_sequence",
        "figure1_b": "panel_b_contextual_associations",
        "figure1_c": "panel_c_retrieved_context_cycle",
        "figure1_d": "panel_d_retrieval_control",
    }
    source_dir = PROJECT_ROOT / "retrieved_context_account_figure"
    for dest, stem in panel_sources.items():
        copy_asset(source_dir / f"{stem}.png", f"{dest}.png")
        copy_asset(source_dir / f"{stem}.svg", f"{dest}.svg")


def build_figure2_panels() -> None:
    fig_dir = PROJECT_ROOT / "figures"
    spc = pd.read_csv(fig_dir / "simulation1_context_binding_spc.csv")
    overlap = pd.read_csv(fig_dir / "simulation1_context_binding_context_overlap.csv")
    support = pd.read_csv(fig_dir / "simulation1_context_binding_support_share.csv")

    labels = {"No reminder": "No film reminder", "With reminder": "With film reminder"}
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(
        2,
        4,
        height_ratios=[1.05, 1.0],
        hspace=0.55,
        wspace=0.80,
    )

    axis_a = fig.add_subplot(gs[0, 0:2])
    axis_b = fig.add_subplot(gs[0, 2:4], sharey=axis_a)
    plot_spc_lines(
        axis_a,
        spc[spc["condition"] == "No reminder"],
        "task_mcf_scale",
        "{:.2f}",
        title=labels["No reminder"],
        ylim=(-0.025, 0.75),
        show_reminder=False,
    )
    plot_spc_lines(
        axis_b,
        spc[spc["condition"] == "With reminder"],
        "task_mcf_scale",
        "{:.2f}",
        title=labels["With reminder"],
        ylim=(-0.025, 0.75),
        show_reminder=True,
    )
    axis_a.set_ylabel("Recall probability", fontsize=STRUCTURAL_FONTSIZE)
    axis_b.set_ylabel("Recall probability", fontsize=STRUCTURAL_FONTSIZE)
    axis_b.tick_params(labelleft=True)
    add_panel_label(axis_a, "A")
    add_panel_label(axis_b, "B")
    axis_b_legend = axis_b.legend(
        title="Task learning factor",
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        fontsize=SUPPORT_FONTSIZE,
        title_fontsize=SUPPORT_FONTSIZE,
    )

    no = overlap[overlap["condition"] == "No reminder"].pivot(
        index="film_position", columns="task_position", values="similarity"
    )
    yes = overlap[overlap["condition"] == "With reminder"].pivot(
        index="film_position", columns="task_position", values="similarity"
    )
    vmin = min(0.0, no.to_numpy().min(), yes.to_numpy().min())
    vmax = max(no.to_numpy().max(), yes.to_numpy().max())
    c_gs = gs[1, 0:2].subgridspec(1, 3, width_ratios=[1, 1, 0.06], wspace=0.18)
    axis_c1 = fig.add_subplot(c_gs[0, 0])
    axis_c2 = fig.add_subplot(c_gs[0, 1], sharex=axis_c1, sharey=axis_c1)
    axis_cbar = fig.add_subplot(c_gs[0, 2])
    image = None
    for ax, data, title in [
        (axis_c1, no, "No film reminder"),
        (axis_c2, yes, "With film reminder"),
    ]:
        image = ax.imshow(
            data.to_numpy(),
            origin="lower",
            aspect="auto",
            cmap="viridis",
            vmin=vmin,
            vmax=vmax,
        )
        ax.set_title(title, fontsize=PANEL_TITLE_FONTSIZE)
        ax.set_xlabel("Task position", fontsize=STRUCTURAL_FONTSIZE)
        ax.set_xticks([0, N_INTERFERENCE - 1])
        ax.set_xticklabels([1, N_INTERFERENCE])
        ax.set_yticks([0, N_FILM - 1])
        ax.set_yticklabels([1, N_FILM])
        ax.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis_c1.set_ylabel("Film position", labelpad=0, fontsize=STRUCTURAL_FONTSIZE)
    axis_c2.tick_params(labelleft=False)
    cbar = fig.colorbar(image, cax=axis_cbar)
    cbar.set_label("Context similarity", fontsize=STRUCTURAL_FONTSIZE)
    cbar.ax.tick_params(labelsize=SUPPORT_FONTSIZE)
    add_panel_label(axis_c1, "C", x=-0.36)

    support_pivot = support.pivot(
        index="task_mcf_scale", columns="condition", values="task_support_share"
    ).reset_index()
    axis_d = fig.add_subplot(gs[1, 2:4])
    axis_d.plot(
        support_pivot["task_mcf_scale"],
        support_pivot["No reminder"],
        marker="o",
        color="#3D4B5C",
        label="No film reminder",
        linewidth=1.8,
    )
    axis_d.plot(
        support_pivot["task_mcf_scale"],
        support_pivot["With reminder"],
        marker="o",
        color=PHASE_COLORS["reminder"],
        label="With film reminder",
        linewidth=1.8,
    )
    axis_d.set_xlabel("Task learning factor", fontsize=STRUCTURAL_FONTSIZE)
    axis_d.set_ylabel("Task competition from film context", fontsize=STRUCTURAL_FONTSIZE)
    axis_d.set_ylim(0, 0.65)
    axis_d.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis_d.spines["top"].set_visible(False)
    axis_d.spines["right"].set_visible(False)
    axis_d.legend(loc="upper left", fontsize=SUPPORT_FONTSIZE)
    add_panel_label(axis_d, "D")

    finish_composite_layout(fig)
    save_panel_region(fig, "figure2_ab", [axis_a, axis_b], extra_artists=[axis_b_legend])
    save_panel_region(fig, "figure2_c", [axis_c1, axis_c2, axis_cbar])
    save_panel_region(fig, "figure2_d", [axis_d])
    plt.close(fig)


def build_figure3_panels() -> None:
    fig_dir = PROJECT_ROOT / "figures"
    support = pd.read_csv(fig_dir / "simulation2_start_context_reinstatement_support.csv")
    pfr = pd.read_csv(fig_dir / "simulation2_start_context_reinstatement_pfr.csv")
    spc = pd.read_csv(fig_dir / "simulation2_start_context_reinstatement_spc.csv")

    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(
        2,
        4,
        height_ratios=[1.05, 1.0],
        hspace=0.55,
        wspace=0.80,
    )
    axis_a = fig.add_subplot(gs[0, 0:2])
    axis_b = fig.add_subplot(gs[0, 2:4], sharex=axis_a)
    axis_c = fig.add_subplot(gs[1, 1:3], sharex=axis_a)
    legend_axis = fig.add_subplot(gs[1, 3])
    legend_axis.axis("off")

    plot_spc_lines(
        axis_a,
        support.rename(columns={"raw_support": "recall_probability"}),
        "start_context_scale",
        "{:.2f}",
        ylabel="Pre-recall item support",
        title="Pre-recall support",
        ylim=(-0.02, 1.45),
        show_reminder=True,
    )
    plot_spc_lines(
        axis_b,
        pfr.rename(columns={"first_recall_probability": "recall_probability"}),
        "start_context_scale",
        "{:.2f}",
        ylabel="Probability of first recall",
        title="Recall initiation",
        ylim=(-0.01, 0.55),
        show_reminder=True,
    )
    plot_spc_lines(
        axis_c,
        spc,
        "start_context_scale",
        "{:.2f}",
        ylabel="Recall probability",
        title="Overall recall",
        ylim=(-0.025, 0.75),
        show_reminder=True,
    )
    add_panel_label(axis_a, "A")
    add_panel_label(axis_b, "B")
    add_panel_label(axis_c, "C")

    handles, legend_labels = axis_a.get_legend_handles_labels()
    legend = legend_axis.legend(
        handles,
        legend_labels,
        title="Start-of-list context\nreinstatement",
        loc="upper left",
        fontsize=SUPPORT_FONTSIZE,
        title_fontsize=SUPPORT_FONTSIZE,
    )
    add_centered_legend_title(legend)

    finish_composite_layout(fig)
    save_panel_region(fig, "figure3_a", [axis_a])
    save_panel_region(fig, "figure3_b", [axis_b])
    save_panel_region(fig, "figure3_c", [axis_c])
    plt.close(fig)


def build_figure4_panels() -> None:
    fig_dir = PROJECT_ROOT / "figures"
    crp = pd.read_csv(fig_dir / "simulation2_retrieval_selectivity_crp.csv")
    spc = pd.read_csv(fig_dir / "simulation2_retrieval_selectivity_spc.csv")
    recovery = pd.read_csv(fig_dir / "simulation2_retrieval_selectivity_offtarget_recovery.csv")
    colors = light_to_dark_colors(len(sorted(spc["retrieval_selectivity"].unique())))

    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(
        2,
        5,
        width_ratios=[1, 1, 1, 1, 0.72],
        height_ratios=[1.0, 1.0],
        hspace=0.55,
        wspace=0.85,
    )
    axis_a = fig.add_subplot(gs[0, 0:2])
    axis_d = fig.add_subplot(gs[0, 2:4])
    legend_axis = fig.add_subplot(gs[:, 4])
    axis_b = fig.add_subplot(gs[1, 0:2])
    axis_c = fig.add_subplot(gs[1, 2:4], sharey=axis_b)
    legend_axis.axis("off")

    crp_subset = crp[
        (crp["start_context_condition"] == "With start-of-list reinstatement")
        & (crp["lag"].between(-5, 5))
        & (crp["lag"] != 0)
    ]
    for color, value in zip(colors, sorted(crp_subset["retrieval_selectivity"].unique())):
        curve = crp_subset[crp_subset["retrieval_selectivity"] == value].sort_values("lag")
        axis_a.plot(
            curve["lag"],
            curve["conditional_response_probability"],
            marker="o",
            color=color,
            linewidth=1.5,
            label=f"{value:.2f}",
        )
    axis_a.axvline(0, color="#7C8794", linewidth=0.7, alpha=0.45, zorder=1)
    axis_a.set_title("Full-list lag-CRP", fontsize=PANEL_TITLE_FONTSIZE, pad=16)
    axis_a.set_xlabel("Lag", fontsize=STRUCTURAL_FONTSIZE)
    axis_a.set_ylabel("Conditional response probability", fontsize=STRUCTURAL_FONTSIZE)
    axis_a.set_xlim(-5, 5)
    axis_a.set_ylim(-0.025, 0.42)
    axis_a.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis_a.spines["top"].set_visible(False)
    axis_a.spines["right"].set_visible(False)
    add_panel_label(axis_a, "A")

    for axis, condition, panel in [
        (axis_b, "No start-of-list reinstatement", "B"),
        (axis_c, "With start-of-list reinstatement", "C"),
    ]:
        plot_spc_lines(
            axis,
            spc[spc["start_context_condition"] == condition],
            "retrieval_selectivity",
            "{:.2f}",
            title=condition,
            ylim=(-0.025, 1.02),
            show_reminder=True,
        )
        add_panel_label(axis, panel)
    axis_c.tick_params(labelleft=True)

    styles = {
        "No start-of-list reinstatement": {
            "color": "#7C8794",
            "marker": "o",
            "label": "No start-of-list\nreinstatement",
        },
        "With start-of-list reinstatement": {
            "color": "#222222",
            "marker": "s",
            "label": "With start-of-list\nreinstatement",
        },
    }
    for condition, style in styles.items():
        curve = recovery[recovery["start_context_condition"] == condition].sort_values("kappa")
        axis_d.plot(
            curve["kappa"],
            curve["film_return_probability"],
            color=style["color"],
            marker=style["marker"],
            linewidth=1.7,
            markersize=4.5,
            label=style["label"],
        )
    axis_d.set_title("Return after off-target sample", fontsize=PANEL_TITLE_FONTSIZE, pad=16)
    axis_d.set_xlabel("Off-target update ($\\kappa$)", fontsize=STRUCTURAL_FONTSIZE)
    axis_d.set_ylabel("Probability next sample is film", fontsize=STRUCTURAL_FONTSIZE)
    axis_d.set_xlim(-0.05, 1.05)
    axis_d.set_ylim(-0.02, 0.82)
    axis_d.set_xticks(np.linspace(0.0, 1.0, 5))
    axis_d.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis_d.spines["top"].set_visible(False)
    axis_d.spines["right"].set_visible(False)
    axis_d.legend(loc="upper right", fontsize=SUPPORT_FONTSIZE, frameon=False, handlelength=2.0)
    add_panel_label(axis_d, "D")

    handles, legend_labels = axis_b.get_legend_handles_labels()
    legend = legend_axis.legend(
        handles,
        legend_labels,
        title="Retrieval\nselectivity",
        loc="upper left",
        fontsize=SUPPORT_FONTSIZE,
        title_fontsize=SUPPORT_FONTSIZE,
    )
    add_centered_legend_title(legend)

    finish_composite_layout(fig)
    save_panel_region(fig, "figure4_a", [axis_a])
    save_panel_region(fig, "figure4_bc", [axis_b, axis_c])
    save_panel_region(fig, "figure4_d", [axis_d])
    plt.close(fig)


def plot_figure5_schematic(axis: plt.Axes) -> None:
    axis.axis("off")
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.set_title("Intermittent test-phase film cues", fontsize=PANEL_TITLE_FONTSIZE, pad=12)
    x0 = 0.221
    step = 0.062
    y = 0.60
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
        axis.text(x, y, str(attempt), ha="center", va="center", fontsize=SUPPORT_FONTSIZE, color="#3D4B5C")
        if attempt < 10:
            axis.plot([x + 0.022, x + step - 0.022], [y, y], color="#9AA4B2", linewidth=0.8)
        if attempt in {4, 8}:
            pulse_x = x + step / 2
            axis.plot([pulse_x, pulse_x], [y - 0.13, y + 0.14], color=PHASE_COLORS["film"], linewidth=2.0)
            axis.scatter([pulse_x], [y + 0.14], marker="v", s=34, color=PHASE_COLORS["film"], zorder=3)
            axis.text(
                pulse_x,
                y + 0.22,
                "film-item\ncue",
                ha="center",
                va="bottom",
                fontsize=SUPPORT_FONTSIZE,
                color=PHASE_COLORS["film"],
                fontweight="bold",
            )
    axis.text(
        0.50,
        0.35,
        "Cue after attempts 4, 8, ...",
        ha="center",
        va="center",
        fontsize=SUPPORT_FONTSIZE,
        color=PHASE_COLORS["film"],
    )
    schematic_y = 0.18
    box_h = 0.075
    specs = [
        (0.10, 0.22, "supplied cue", PHASE_COLORS["film"], "#EAF2FF"),
        (0.39, 0.22, "film context", PHASE_COLORS["reminder"], "#ECFDF3"),
        (0.68, 0.22, "next search", "#3D4B5C", "#F7F9FB"),
    ]
    for x, width, label, color, fill in specs:
        axis.add_patch(
            plt.Rectangle((x, schematic_y), width, box_h, facecolor=fill, edgecolor=color, linewidth=1.1)
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
    for x0, x1 in [(0.32, 0.39), (0.61, 0.68)]:
        axis.annotate(
            "",
            xy=(x1, schematic_y + box_h / 2),
            xytext=(x0, schematic_y + box_h / 2),
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


def build_figure5_panels() -> None:
    fig_dir = PROJECT_ROOT / "figures"
    spc = pd.read_csv(fig_dir / "simulation3_film_cue_inclusion_spc.csv")
    phase = pd.read_csv(fig_dir / "simulation3_film_cue_inclusion_phase_totals.csv")

    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(
        2,
        5,
        width_ratios=[1, 1, 1, 1, 0.62],
        height_ratios=[0.95, 1.05],
        hspace=0.58,
        wspace=0.88,
    )
    axis_a = fig.add_subplot(gs[0, 0:2])
    gs_b = gs[0, 2:4].subgridspec(1, 2, wspace=0.42)
    axis_b = fig.add_subplot(gs_b[0])
    axis_b_gap = fig.add_subplot(gs_b[1])
    axis_c = fig.add_subplot(gs[1, 0:2])
    axis_d = fig.add_subplot(gs[1, 2:4], sharex=axis_c, sharey=axis_c)
    legend_axis = fig.add_subplot(gs[:, 4])
    legend_axis.axis("off")

    plot_figure5_schematic(axis_a)
    add_panel_label(axis_a, "A", x=-0.08, y=1.12)

    pivot = phase[phase["phase"] == "film"].pivot(
        index="film_cue_reinstatement",
        columns="retrieval_condition",
        values="recall_probability_mass",
    )
    colors = {"Unguided retrieval": "#4A5563", "Deliberate recall": PHASE_COLORS["film"]}
    for condition in ["Unguided retrieval", "Deliberate recall"]:
        axis_b.plot(
            pivot.index,
            pivot[condition],
            marker="o",
            linewidth=1.9,
            markersize=4.8,
            color=colors[condition],
            label=condition,
        )
    gap = pivot["Deliberate recall"] - pivot["Unguided retrieval"]
    axis_b_gap.plot(pivot.index, gap, marker="o", linewidth=1.8, markersize=4.8, color="#2F3B4A")
    axis_b_gap.axhline(gap.iloc[0], color="#9AA4B2", linewidth=0.9, linestyle="--")
    axis_b.set_title("Film recall", fontsize=SUPPORT_FONTSIZE, pad=6)
    axis_b.set_xlabel("Film-cue reinstatement", fontsize=SUPPORT_FONTSIZE)
    axis_b.set_ylabel("Film-item recall mass", fontsize=SUPPORT_FONTSIZE)
    axis_b.set_xlim(float(pivot.index.min()), float(pivot.index.max()))
    axis_b.set_ylim(0, 3.25)
    axis_b.set_xticks([0.0, 0.33, 0.66, 1.0])
    axis_b.set_xticklabels(["0.00", "0.33", "0.66", "1.00"])
    axis_b.legend(
        frameon=False,
        fontsize=8.5,
        loc="upper left",
        bbox_to_anchor=(0.00, 0.98),
        borderaxespad=0.0,
        handlelength=1.6,
    )
    axis_b_gap.set_title("Intentionality gap", fontsize=SUPPORT_FONTSIZE, pad=6)
    axis_b_gap.set_xlabel("Film-cue reinstatement", fontsize=SUPPORT_FONTSIZE)
    axis_b_gap.set_ylabel("Deliberate - unguided", fontsize=8.5)
    axis_b_gap.set_xlim(float(pivot.index.min()), float(pivot.index.max()))
    axis_b_gap.set_ylim(0, 2.6)
    axis_b_gap.set_xticks([0.0, 0.33, 0.66, 1.0])
    axis_b_gap.set_xticklabels(["0.00", "0.33", "0.66", "1.00"])
    for ax in [axis_b, axis_b_gap]:
        ax.tick_params(labelsize=8.5)
        ax.grid(axis="y", color="#D6DBE1", linewidth=0.7, alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    add_panel_label(axis_b, "B", x=-0.22, y=1.22)

    for axis, condition, panel in [
        (axis_c, "Unguided retrieval", "C"),
        (axis_d, "Deliberate recall", "D"),
    ]:
        plot_spc_lines(
            axis,
            spc[spc["retrieval_condition"] == condition],
            "film_cue_reinstatement",
            "{:.2f}",
            title=condition,
            ylim=(-0.025, 0.75),
            show_reminder=True,
        )
        add_panel_label(axis, panel)
    axis_d.set_ylabel("")

    handles, legend_labels = axis_c.get_legend_handles_labels()
    legend = legend_axis.legend(
        handles,
        legend_labels,
        title="Film-cue\nreinstatement",
        loc="center left",
        fontsize=SUPPORT_FONTSIZE,
        title_fontsize=SUPPORT_FONTSIZE,
        frameon=False,
    )
    add_centered_legend_title(legend)

    finish_composite_layout(fig)
    save_panel_region(fig, "figure5_a", [axis_a])
    save_panel_region(fig, "figure5_b", [axis_b, axis_b_gap])
    save_panel_region(fig, "figure5_cd", [axis_c, axis_d])
    plt.close(fig)


def main() -> None:
    reset_assets()
    copy_whole_figures()
    copy_figure1_panels()
    build_figure2_panels()
    build_figure3_panels()
    build_figure4_panels()
    build_figure5_panels()


if __name__ == "__main__":
    main()
