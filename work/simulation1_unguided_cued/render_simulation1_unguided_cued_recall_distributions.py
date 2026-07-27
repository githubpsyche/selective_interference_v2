from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

from selective_interference_v2 import PHASE_COLORS, add_phase_bands


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(__file__).resolve().parent
OUTPUT_PREFIX = "simulation1_unguided_cued_recall_distributions"
SOURCE_CSV = DATA_DIR / f"{OUTPUT_PREFIX}.csv"

PANEL_LETTER_FONTSIZE = 16
PANEL_TITLE_FONTSIZE = 13
STRUCTURAL_FONTSIZE = 11
SUPPORT_FONTSIZE = 10
ANNOTATION_FONTSIZE = 10

N_FILM = 16
N_BREAK = 16
N_TASK = 16
N_FILLER = 16

REMINDER_LABELS = {
    "No reminder": "Without pre-task reminder",
    "With reminder": "With pre-task film reminder",
}
TASK_LABELS = {
    "Weak task encoding": "Weaker task associations",
    "Strong task encoding": "Stronger task associations",
}
TASK_ORDER = list(TASK_LABELS)
TASK_COLORS = {
    "Weak task encoding": "#9CA3AF",
    "Strong task encoding": PHASE_COLORS["task"],
}
GRID_COLOR = "#E7EBF0"
ANNOTATION_COLOR = "#1F2933"
BRACKET_X1 = 2.25
BRACKET_X2 = 14.75
BRACKET_CURVE_GAP = 0.015
BRACKET_CAP = 0.018
BRACKET_LABEL_GAP = 0.012
BRACKET_LINEWIDTH = 1.0

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]


def phase_labels() -> list[str]:
    return (
        ["film"] * N_FILM
        + ["break"] * N_BREAK
        + ["task"] * N_TASK
        + ["filler"] * N_FILLER
    )


def add_panel_heading(axis, label: str, title: str, y: float = 0.86) -> None:
    axis.axis("off")
    axis.text(
        -0.055,
        y,
        label,
        transform=axis.transAxes,
        fontsize=PANEL_LETTER_FONTSIZE,
        fontweight="bold",
        ha="left",
        va="top",
    )
    axis.text(
        0.5,
        y,
        title,
        transform=axis.transAxes,
        fontsize=PANEL_TITLE_FONTSIZE,
        fontweight="bold",
        ha="center",
        va="top",
    )


def add_phase_boundaries(axis) -> None:
    for boundary in [N_FILM + 0.5, N_FILM + N_BREAK + 0.5, N_FILM + N_BREAK + N_TASK + 0.5]:
        axis.axvline(boundary, color="#7C8794", linewidth=0.75, alpha=0.42, zorder=1)


def add_reminder_marker(axis) -> None:
    reminder_x = N_FILM + N_BREAK + 0.5
    axis.axvline(
        reminder_x,
        color=PHASE_COLORS["reminder"],
        linewidth=1.8,
        alpha=0.85,
        zorder=2,
    )
    axis.text(
        reminder_x - 1.05,
        0.58,
        "Film reminder",
        ha="center",
        va="center",
        fontsize=SUPPORT_FONTSIZE,
        fontstyle="italic",
        color=PHASE_COLORS["reminder"],
        rotation=90,
        rotation_mode="anchor",
        transform=axis.get_xaxis_transform(),
        clip_on=False,
        zorder=5,
    )


def add_reduction_bracket(axis, subset: pd.DataFrame, label: str) -> None:
    film_rows = subset[subset["position"].between(1, N_FILM)]
    high_y = float(film_rows["recall_probability"].max())
    cap_bottom_y = high_y + BRACKET_CURVE_GAP
    bracket_y = cap_bottom_y + BRACKET_CAP
    axis.plot(
        [BRACKET_X1, BRACKET_X1, BRACKET_X2, BRACKET_X2],
        [cap_bottom_y, bracket_y, bracket_y, cap_bottom_y],
        color=ANNOTATION_COLOR,
        linewidth=BRACKET_LINEWIDTH,
        solid_capstyle="butt",
        clip_on=False,
        zorder=5,
    )
    axis.text(
        (BRACKET_X1 + BRACKET_X2) / 2,
        bracket_y + BRACKET_LABEL_GAP,
        label,
        color=ANNOTATION_COLOR,
        fontsize=ANNOTATION_FONTSIZE,
        fontweight="bold",
        ha="center",
        va="bottom",
        clip_on=False,
        zorder=5,
    )


def plot_panel(axis, df: pd.DataFrame, reminder_condition: str) -> None:
    add_phase_bands(axis, phase_labels(), fontsize=SUPPORT_FONTSIZE, label_y=1.035)
    add_phase_boundaries(axis)
    if reminder_condition == "With reminder":
        add_reminder_marker(axis)

    subset = df[df["reminder_condition"].eq(reminder_condition)]
    for task_condition in TASK_ORDER:
        curve = subset[subset["task_condition"].eq(task_condition)].sort_values("position")
        axis.plot(
            curve["position"],
            curve["recall_probability"],
            color=TASK_COLORS[task_condition],
            linewidth=1.9,
            label=TASK_LABELS[task_condition],
            zorder=4,
        )

    bracket_label = "smaller reduction" if reminder_condition == "No reminder" else "larger reduction"
    add_reduction_bracket(axis, subset, bracket_label)

    axis.set_ylabel("Recall probability", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_xlabel("Encoded position", fontsize=STRUCTURAL_FONTSIZE, labelpad=7)
    axis.set_xlim(1, N_FILM + N_BREAK + N_TASK + N_FILLER)
    axis.set_ylim(-0.025, 0.85)
    axis.set_xticks([1, 16, 32, 48, 64])
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.set_axisbelow(True)
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.45, alpha=0.45, zorder=0)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SOURCE_CSV)
    required_columns = {
        "reminder_condition",
        "reminder_label",
        "task_condition",
        "task_mcf_scale",
        "film_cue_reinstatement",
        "first_cue_after",
        "position",
        "phase",
        "recall_probability",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"{SOURCE_CSV} is missing required column(s): {missing}")
    df = df[df["reminder_condition"].isin(["No reminder", "With reminder"])]
    df = df[df["task_condition"].isin(TASK_ORDER)]
    df = df.sort_values(["reminder_condition", "task_mcf_scale", "position"])

    fig = plt.figure(figsize=(8.2, 7.8))
    outer = fig.add_gridspec(
        5,
        1,
        height_ratios=[0.22, 1.0, 0.28, 0.22, 1.0],
        hspace=0.10,
        left=0.115,
        right=0.955,
        top=0.940,
        bottom=0.165,
    )

    heading_a = fig.add_subplot(outer[0, 0])
    spacer = fig.add_subplot(outer[2, 0])
    heading_b = fig.add_subplot(outer[3, 0])
    spacer.axis("off")
    add_panel_heading(heading_a, "A", REMINDER_LABELS["No reminder"], y=0.88)
    add_panel_heading(heading_b, "B", REMINDER_LABELS["With reminder"], y=0.88)

    axis_a = fig.add_subplot(outer[1, 0])
    axis_b = fig.add_subplot(outer[4, 0], sharex=axis_a, sharey=axis_a)
    plot_panel(axis_a, df, "No reminder")
    plot_panel(axis_b, df, "With reminder")
    axis_a.tick_params(labelbottom=True)

    legend_handles = [
        Line2D([0], [0], color=TASK_COLORS[task_condition], linewidth=1.9, label=TASK_LABELS[task_condition])
        for task_condition in TASK_ORDER
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.535, 0.035),
        ncol=2,
        frameon=False,
        fontsize=SUPPORT_FONTSIZE,
        columnspacing=1.8,
        handlelength=2.5,
    )

    for extension, kwargs in {
        "png": {"dpi": 600},
        "svg": {},
        "pdf": {},
    }.items():
        fig.savefig(
            FIGURE_DIR / f"{OUTPUT_PREFIX}.{extension}",
            bbox_inches="tight",
            **kwargs,
        )
    plt.close(fig)


if __name__ == "__main__":
    main()
