from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

from selective_interference_v2 import PHASE_COLORS


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(__file__).resolve().parent
FIGURE_STR = "simulation1_unguided_cued"
OUTPUT_PREFIX = f"{FIGURE_STR}_sequence_summary"
SEQUENCE_ROWS_PATH = DATA_DIR / f"{FIGURE_STR}_sequence_rows.csv"
PHASE_TOTALS_PATH = DATA_DIR / f"{FIGURE_STR}_phase_totals_sequence_summary.csv"

PANEL_LETTER_FONTSIZE = 16
PANEL_TITLE_FONTSIZE = 13
STRUCTURAL_FONTSIZE = 11
SUPPORT_FONTSIZE = 10

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

REMINDER_CONDITIONS = ["No reminder", "With reminder"]
REMINDER_LABELS = {
    "No reminder": "Without pre-task reminder",
    "With reminder": "With pre-task film reminder",
}
TASK_LABELS_BY_SCALE = {
    1.0: "Weaker task associations",
    2.0: "Stronger task associations",
}
TASK_BAR_STYLES = {
    1.0: {"facecolor": "#F2F4F6", "edgecolor": "#3D4B5C"},
    2.0: {"facecolor": "#FFF0E6", "edgecolor": "#D96B2B"},
}
RASTER_PHASE_COLORS = {
    "none": "#F7FAFF",
    "film": PHASE_COLORS["film"],
    "task": PHASE_COLORS["task"],
    "delay_filler": "#9CA3AF",
}
RASTER_PHASE_LABELS = {
    "film": "Film",
    "task": "Task",
    "delay_filler": "Delay/filler",
    "none": "No output",
}
GRID_COLOR = "#E7EBF0"
BRACKET_COLOR = "#3D4B5C"
BRACKET_LINEWIDTH = 1.2
BRACKET_PAD = 0.06
BRACKET_BAR_GAP_FRACTION = 0.05
BRACKET_CAP_FRACTION = 0.035
BRACKET_LABEL_GAP_FRACTION = 0.025


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def coerce_sequence_row(row: dict[str, str]) -> dict:
    out = dict(row)
    out["task_mcf_scale"] = float(out["task_mcf_scale"])
    out["display_trial"] = int(out["display_trial"])
    out["output_position"] = int(out["output_position"])
    out["phase_code"] = int(out["phase_code"])
    return out


def coerce_total_row(row: dict[str, str]) -> dict:
    out = dict(row)
    out["task_mcf_scale"] = float(out["task_mcf_scale"])
    out["recall_probability_mass"] = float(out["recall_probability_mass"])
    return out


def build_sequence_samples(rows: list[dict]) -> tuple[dict[tuple[str, float], np.ndarray], list[float], int]:
    task_scales = sorted({row["task_mcf_scale"] for row in rows})
    raster_max_outputs = max(row["output_position"] for row in rows)
    samples: dict[tuple[str, float], np.ndarray] = {}
    for reminder_condition in REMINDER_CONDITIONS:
        for task_scale in task_scales:
            condition_rows = [
                row
                for row in rows
                if row["reminder_condition"] == reminder_condition
                and np.isclose(row["task_mcf_scale"], task_scale)
            ]
            display_trials = sorted({row["display_trial"] for row in condition_rows})
            trial_lookup = {display_trial: index for index, display_trial in enumerate(display_trials)}
            codes = np.zeros((len(display_trials), raster_max_outputs), dtype=int)
            for row in condition_rows:
                output_index = row["output_position"] - 1
                codes[trial_lookup[row["display_trial"]], output_index] = row["phase_code"]
            samples[(reminder_condition, task_scale)] = codes
    return samples, task_scales, raster_max_outputs


def phase_total(rows: list[dict], reminder_condition: str, task_scale: float, phase: str) -> float:
    for row in rows:
        if (
            row["reminder_condition"] == reminder_condition
            and np.isclose(row["task_mcf_scale"], task_scale)
            and row["phase"] == phase
        ):
            return row["recall_probability_mass"]
    return float("nan")


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


def plot_sequence_raster(axis, sample: np.ndarray, raster_max_outputs: int, show_xticks: bool) -> None:
    cmap = ListedColormap(
        [
            RASTER_PHASE_COLORS["none"],
            RASTER_PHASE_COLORS["film"],
            RASTER_PHASE_COLORS["task"],
            RASTER_PHASE_COLORS["delay_filler"],
        ]
    )
    norm = BoundaryNorm(np.arange(-0.5, 4.5, 1.0), cmap.N)
    axis.imshow(sample, cmap=cmap, norm=norm, aspect="auto", interpolation="none")
    axis.set_xlim(-0.5, raster_max_outputs - 0.5)
    axis.set_ylim(sample.shape[0] - 0.5, -0.5)
    if show_xticks:
        tick_positions = [0, min(7, raster_max_outputs - 1), raster_max_outputs - 1]
        axis.set_xticks(tick_positions)
        axis.set_xticklabels([str(position + 1) for position in tick_positions])
        axis.tick_params(axis="x", labelsize=SUPPORT_FONTSIZE, length=2.5, pad=2)
        axis.set_xlabel("output position", fontsize=STRUCTURAL_FONTSIZE, labelpad=5)
    else:
        axis.set_xticks([])
    axis.set_yticks([])
    axis.set_xticks(np.arange(-0.5, raster_max_outputs, 1), minor=True)
    axis.set_yticks(np.arange(-0.5, sample.shape[0], 1), minor=True)
    axis.grid(which="minor", color="white", linewidth=0.5)
    axis.tick_params(which="minor", bottom=False, left=False)
    axis.set_facecolor("#FAFBFC")
    for spine in axis.spines.values():
        spine.set_visible(True)
        spine.set_color("#3D4B5C")
        spine.set_linewidth(1.2)


def plot_film_totals(axis, total_rows: list[dict], task_scales: list[float]) -> None:
    x = np.arange(len(REMINDER_CONDITIONS))
    width = 0.34
    all_values = []
    offsets = np.linspace(-width / 2, width / 2, len(task_scales))
    for offset, task_scale in zip(offsets, task_scales):
        values = [phase_total(total_rows, reminder_condition, task_scale, "film") for reminder_condition in REMINDER_CONDITIONS]
        all_values.extend(values)
        style = TASK_BAR_STYLES.get(task_scale, TASK_BAR_STYLES[1.0])
        axis.bar(
            x + offset,
            values,
            width=width,
            color=style["facecolor"],
            edgecolor=style["edgecolor"],
            linewidth=1.5,
            label=TASK_LABELS_BY_SCALE.get(task_scale, f"{task_scale:g}"),
            zorder=2,
        )
    axis.set_title("Film recall across all trials", fontsize=PANEL_TITLE_FONTSIZE, fontweight="bold", pad=8)
    axis.set_xticks(x)
    axis.set_xticklabels([REMINDER_LABELS[condition] for condition in REMINDER_CONDITIONS])
    axis.set_ylabel("Mean film items recalled", fontsize=STRUCTURAL_FONTSIZE)
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.set_axisbelow(True)
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.45, alpha=0.45, zorder=0)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    upper = max(1.0, np.ceil(max(all_values) * 1.14 * 4) / 4)
    axis.set_ylim(0, upper)

    reminder_index = REMINDER_CONDITIONS.index("With reminder")
    reminder_values = [
        phase_total(total_rows, "With reminder", task_scale, "film")
        for task_scale in task_scales
    ]
    bracket_y = max(reminder_values) + upper * BRACKET_BAR_GAP_FRACTION
    bracket_cap = upper * BRACKET_CAP_FRACTION
    bracket_left = reminder_index + offsets[0] - width / 2 - BRACKET_PAD
    bracket_right = reminder_index + offsets[-1] + width / 2 + BRACKET_PAD
    axis.plot(
        [bracket_left, bracket_left, bracket_right, bracket_right],
        [bracket_y - bracket_cap, bracket_y, bracket_y, bracket_y - bracket_cap],
        color=BRACKET_COLOR,
        linewidth=BRACKET_LINEWIDTH,
        zorder=4,
    )
    axis.text(
        (bracket_left + bracket_right) / 2,
        bracket_y + upper * BRACKET_LABEL_GAP_FRACTION,
        "larger reduction",
        color=BRACKET_COLOR,
        fontsize=SUPPORT_FONTSIZE,
        fontweight="bold",
        ha="center",
        va="bottom",
        zorder=4,
    )

    axis.legend(
        handles=[
            Patch(
                facecolor=TASK_BAR_STYLES[1.0]["facecolor"],
                edgecolor=TASK_BAR_STYLES[1.0]["edgecolor"],
                linewidth=1.5,
                label=TASK_LABELS_BY_SCALE[1.0],
            ),
            Patch(
                facecolor=TASK_BAR_STYLES[2.0]["facecolor"],
                edgecolor=TASK_BAR_STYLES[2.0]["edgecolor"],
                linewidth=1.5,
                label=TASK_LABELS_BY_SCALE[2.0],
            ),
        ],
        frameon=False,
        fontsize=SUPPORT_FONTSIZE,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.28),
        borderaxespad=0.0,
        ncol=2,
        columnspacing=1.5,
        handlelength=1.4,
    )


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    sequence_rows = [coerce_sequence_row(row) for row in read_rows(SEQUENCE_ROWS_PATH)]
    total_rows = [coerce_total_row(row) for row in read_rows(PHASE_TOTALS_PATH)]
    samples, task_scales, raster_max_outputs = build_sequence_samples(sequence_rows)

    fig = plt.figure(figsize=(8.2, 7.8))
    outer = fig.add_gridspec(
        5,
        1,
        height_ratios=[0.64, 2.55, 0.34, 0.22, 1.18],
        hspace=0.11,
        left=0.125,
        right=0.905,
        top=0.940,
        bottom=0.105,
    )

    heading_a = fig.add_subplot(outer[0, 0])
    add_panel_heading(heading_a, "A", "Example recall sequences", y=0.96)
    legend_handles = [
        Patch(facecolor=RASTER_PHASE_COLORS["film"], edgecolor="none", label=RASTER_PHASE_LABELS["film"]),
        Patch(facecolor=RASTER_PHASE_COLORS["task"], edgecolor="none", label=RASTER_PHASE_LABELS["task"]),
        Patch(facecolor=RASTER_PHASE_COLORS["delay_filler"], edgecolor="none", label=RASTER_PHASE_LABELS["delay_filler"]),
        Patch(facecolor=RASTER_PHASE_COLORS["none"], edgecolor="#C7D0DA", label=RASTER_PHASE_LABELS["none"]),
    ]
    heading_a.legend(
        handles=legend_handles,
        frameon=False,
        fontsize=SUPPORT_FONTSIZE,
        loc="center",
        bbox_to_anchor=(0.5, 0.40),
        ncol=4,
        columnspacing=1.0,
        handlelength=1.2,
    )
    raster_grid = outer[1, 0].subgridspec(2, 2, hspace=0.28, wspace=0.12)
    raster_axes = {}
    for row_index, task_scale in enumerate(task_scales):
        for col_index, reminder_condition in enumerate(REMINDER_CONDITIONS):
            axis = fig.add_subplot(raster_grid[row_index, col_index])
            sample = samples[(reminder_condition, task_scale)]
            show_xticks = row_index == len(task_scales) - 1
            plot_sequence_raster(axis, sample, raster_max_outputs, show_xticks=show_xticks)
            if row_index == 0:
                axis.set_title(
                    REMINDER_LABELS[reminder_condition],
                    fontsize=STRUCTURAL_FONTSIZE,
                    fontweight="bold",
                    pad=8,
                )
            if col_index == 0:
                axis.set_ylabel(
                    TASK_LABELS_BY_SCALE.get(task_scale, f"{task_scale:g}"),
                    fontsize=STRUCTURAL_FONTSIZE,
                    labelpad=16,
                    rotation=0,
                    ha="right",
                    va="center",
                )
            raster_axes[(reminder_condition, task_scale)] = axis

    spacer = fig.add_subplot(outer[2, 0])
    spacer.axis("off")
    heading_b = fig.add_subplot(outer[3, 0])
    add_panel_heading(heading_b, "B", "", y=0.88)

    bar_grid = outer[4, 0].subgridspec(1, 3, width_ratios=[0.24, 1.0, 0.24], wspace=0.0)
    axis_b = fig.add_subplot(bar_grid[0, 1])
    plot_film_totals(axis_b, total_rows, task_scales)

    for extension, kwargs in {
        "png": {"dpi": 600},
        "svg": {},
        "pdf": {},
    }.items():
        fig.savefig(FIGURE_DIR / f"{OUTPUT_PREFIX}.{extension}", bbox_inches="tight", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
