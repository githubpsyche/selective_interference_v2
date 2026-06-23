from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
OUTPUT_PREFIX = "simulation2_context_overlap_goal_combined_candidate"
DATA_PATH = FIGURE_DIR / f"{OUTPUT_PREFIX}_data.npz"

NO_REMINDER_LABEL = "No pre-task reminder"
REMINDER_LABEL = "Pre-task film reminder"
GOAL_LABEL = "Pre-task film reminder + film-retrieval goal"

PANEL_LETTER_FONTSIZE = 16
PANEL_TITLE_FONTSIZE = 13
STRUCTURAL_FONTSIZE = 11
SUPPORT_FONTSIZE = 9

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]


@dataclass(frozen=True)
class PlotParadigm:
    n_film: int


def simulation1_matrices():
    import render_simulation1_context_overlap_candidate_one_row as sim1_overlap

    paradigm = sim1_overlap.make_paradigm()
    matrices = {}
    for reminder_condition, reminder_scales in sim1_overlap.REMINDER_CONDITIONS.items():
        film_context, task_context = sim1_overlap.trace_contexts(reminder_scales)
        matrices[reminder_condition] = sim1_overlap.context_overlap(
            film_context,
            task_context,
        )
    return paradigm, matrices


def goal_matrices():
    import render_simulation2_maintained_film_goal_context_similarity_candidate as goal_overlap

    paradigm, film_context, task_context = goal_overlap.trace_high_interference_contexts()
    matrices = {
        "Temporal context only": goal_overlap.context_similarity(
            film_context,
            task_context,
        ),
        "Temporal context + film-retrieval goal": goal_overlap.goal_augmented_similarity(
            film_context,
            task_context,
            goal_overlap.FILM_RETRIEVAL_GOAL_WEIGHT,
        ),
    }
    return paradigm, matrices


def build_overlap_data() -> tuple[PlotParadigm, dict[str, np.ndarray]]:
    sim1_paradigm, sim1_mats = simulation1_matrices()
    _, goal_mats = goal_matrices()
    return PlotParadigm(n_film=sim1_paradigm.n_film), {
        NO_REMINDER_LABEL: sim1_mats[NO_REMINDER_LABEL],
        REMINDER_LABEL: sim1_mats[REMINDER_LABEL],
        GOAL_LABEL: goal_mats["Temporal context + film-retrieval goal"],
    }


def save_overlap_data(
    path: Path,
    paradigm: PlotParadigm,
    matrices: dict[str, np.ndarray],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        n_film=np.asarray(paradigm.n_film, dtype=int),
        no_reminder=matrices[NO_REMINDER_LABEL],
        reminder=matrices[REMINDER_LABEL],
        goal=matrices[GOAL_LABEL],
    )


def load_overlap_data(path: Path) -> tuple[PlotParadigm, dict[str, np.ndarray]]:
    data = np.load(path)
    paradigm = PlotParadigm(n_film=int(data["n_film"]))
    return paradigm, {
        NO_REMINDER_LABEL: np.asarray(data["no_reminder"], dtype=float),
        REMINDER_LABEL: np.asarray(data["reminder"], dtype=float),
        GOAL_LABEL: np.asarray(data["goal"], dtype=float),
    }


def get_overlap_data(refresh_data: bool) -> tuple[PlotParadigm, dict[str, np.ndarray]]:
    if refresh_data or not DATA_PATH.exists():
        paradigm, matrices = build_overlap_data()
        save_overlap_data(DATA_PATH, paradigm, matrices)
        print(f"Wrote {DATA_PATH}")
        return paradigm, matrices
    print(f"Reading {DATA_PATH}")
    return load_overlap_data(DATA_PATH)


def add_panel_title(axis, letter: str, title: str) -> None:
    axis.axis("off")
    axis.text(
        -0.045,
        0.88,
        letter,
        ha="left",
        va="top",
        fontsize=PANEL_LETTER_FONTSIZE,
        fontweight="bold",
        transform=axis.transAxes,
    )
    axis.text(
        0.5,
        0.88,
        title,
        ha="center",
        va="top",
        fontsize=PANEL_TITLE_FONTSIZE,
        fontweight="bold",
        transform=axis.transAxes,
    )


def add_three_line_panel(
    axis,
    paradigm,
    line_specs: tuple[tuple[str, np.ndarray, str, str | tuple[int, tuple[int, int]], float], ...],
) -> None:
    positions = np.arange(1, paradigm.n_film + 1)
    max_mean = 0.0
    for label, matrix, color, linestyle, linewidth in line_specs:
        mean_values = matrix.mean(axis=1)
        max_mean = max(max_mean, float(np.max(mean_values)))
        axis.plot(
            positions,
            mean_values,
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            label=label,
        )
        axis.text(
            1.015,
            mean_values[-1],
            label,
            color=color,
            fontsize=SUPPORT_FONTSIZE,
            ha="left",
            va="center",
            transform=axis.get_yaxis_transform(),
            clip_on=False,
        )
    axis.set_xlabel("Encoded film position", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_ylabel("Mean overlap with task contexts", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_xlim(1, paradigm.n_film)
    axis.set_xticks([1, 4, 8, 12, 16])
    axis.set_ylim(0, max_mean * 1.15)
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.grid(axis="y", color="#D6DBE1", linewidth=0.7, alpha=0.7, zorder=0)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def add_three_heatmap_panel(
    slot,
    heatmap_specs: tuple[tuple[str, np.ndarray], ...],
    colorbar_label: str,
) -> None:
    grid = slot.subgridspec(
        1,
        4,
        width_ratios=[1.0, 1.0, 1.0, 0.050],
        wspace=0.17,
    )
    axes = [
        (plt.gcf().add_subplot(grid[0, i]), title, matrix)
        for i, (title, matrix) in enumerate(heatmap_specs)
    ]
    colorbar_axis = plt.gcf().add_subplot(grid[0, 3])
    vmax = max(float(np.max(matrix)) for _, matrix in heatmap_specs)
    image = None
    for heatmap_axis, title, matrix in axes:
        image = heatmap_axis.imshow(
            matrix.T,
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            cmap="viridis",
            vmin=0.0,
            vmax=vmax,
        )
        heatmap_axis.set_title(title, fontsize=STRUCTURAL_FONTSIZE, pad=7)
        heatmap_axis.set_xlabel("Encoded film position", fontsize=STRUCTURAL_FONTSIZE)
        heatmap_axis.set_xticks([0, 7, 15], ["1", "8", "16"])
        heatmap_axis.set_yticks([0, 7, 15], ["1", "8", "16"])
        heatmap_axis.tick_params(labelsize=SUPPORT_FONTSIZE, length=3)
        for spine in heatmap_axis.spines.values():
            spine.set_color("#2F3A45")
            spine.set_linewidth(0.9)
    axes[0][0].set_ylabel("Encoded task position", fontsize=STRUCTURAL_FONTSIZE)
    for heatmap_axis, _, _ in axes[1:]:
        heatmap_axis.tick_params(labelleft=False)
    if image is not None:
        colorbar = plt.gcf().colorbar(image, cax=colorbar_axis)
        colorbar.ax.set_title(colorbar_label, fontsize=STRUCTURAL_FONTSIZE, pad=7)
        colorbar.ax.tick_params(labelsize=SUPPORT_FONTSIZE)


def plot_combined(refresh_data: bool = False, data_only: bool = False) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    paradigm, matrices = get_overlap_data(refresh_data)

    if data_only:
        return

    sim1_no = matrices[NO_REMINDER_LABEL]
    sim1_reminder = matrices[REMINDER_LABEL]
    goal_with = matrices[GOAL_LABEL]

    fig = plt.figure(figsize=(10.2, 7.05))
    outer = fig.add_gridspec(
        5,
        1,
        height_ratios=[0.14, 0.98, 0.32, 0.36, 1.0],
        hspace=0.06,
        left=0.095,
        right=0.965,
        top=0.945,
        bottom=0.100,
    )

    add_panel_title(
        fig.add_subplot(outer[0, 0]),
        "A",
        "Mean task overlap by film position",
    )
    line_grid = outer[1, 0].subgridspec(
        1,
        3,
        width_ratios=[0.72, 1.56, 0.72],
        wspace=0.0,
    )
    add_three_line_panel(
        fig.add_subplot(line_grid[0, 1]),
        paradigm,
        (
            (
                "No pre-task reminder",
                sim1_no,
                "#A0A8B2",
                (0, (4, 2)),
                2.0,
            ),
            (
                "Pre-task reminder",
                sim1_reminder,
                "#2F3A45",
                "-",
                2.2,
            ),
            (
                "+ film-retrieval goal",
                goal_with,
                "#2F3A45",
                (0, (1.2, 1.4)),
                2.6,
            ),
        ),
    )
    add_panel_title(
        fig.add_subplot(outer[3, 0]),
        "B",
        "Task overlap across film and task positions",
    )
    add_three_heatmap_panel(
        outer[4, 0],
        (
            ("No pre-task reminder", sim1_no),
            ("Pre-task film reminder", sim1_reminder),
            ("+ film-retrieval goal", goal_with),
        ),
        "Overlap",
    )

    base = FIGURE_DIR / OUTPUT_PREFIX
    fig.savefig(f"{base}.png", dpi=600)
    fig.savefig(f"{base}.svg")
    fig.savefig(f"{base}.pdf")
    plt.close(fig)
    print(f"{base}.png")
    print(f"{base}.svg")
    print(f"{base}.pdf")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Render the context-overlap/film-retrieval-goal candidate figure. "
            "By default, layout edits read cached overlap matrices."
        )
    )
    parser.add_argument(
        "--refresh-data",
        action="store_true",
        help="Regenerate overlap matrices before rendering.",
    )
    parser.add_argument(
        "--data-only",
        action="store_true",
        help="Regenerate/read overlap matrices without rendering the figure.",
    )
    args = parser.parse_args()
    plot_combined(refresh_data=args.refresh_data, data_only=args.data_only)
