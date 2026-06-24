from __future__ import annotations

import csv
from pathlib import Path

from jax import tree_util, vmap
import jax.numpy as jnp
import matplotlib.pyplot as plt
import numpy as np
from jaxcmr.helpers import find_project_root

from selective_interference_v2 import (
    PHASE_COLORS,
    Paradigm,
    configure_rates,
    load_fit_params,
    make_factory,
    make_is_emotional,
    make_is_target,
)


ROOT = Path(find_project_root())
FIGURE_DIR = ROOT / "figures"
OUTPUT_PREFIX = "simulation2_film_retrieval_goal_context_overlap"
FIT_PATH = ROOT / "results/fits/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
EXPERIMENT_COUNT = 5000
MAX_RECALL = 48

FILM_EMOTIONAL = True
INTERFERENCE_EMOTIONAL = False
FILM_RETRIEVAL_GOAL_WEIGHT = 1.0
TASK_MCF_SCALE = 2.0
REMINDER_CONDITION = "With reminder"
TASK_CONDITION = "Strong task encoding"

BASE_FIXED_SCALES = {
    "break_drift_scale": 1.0,
    "break_mcf_scale": 1.0,
    "filler_drift_scale": 1.0,
    "filler_mcf_scale": 1.0,
    "source_learning_baseline": 0.05,
    "primacy_scale": 0.1,
    "primacy_decay": 1.5,
}
REMINDER_SCALES = {
    "reminder_start_drift_scale": 1.0,
    "reminder_drift_scale": 1.0,
}

PANEL_LETTER_FONTSIZE = 16
PANEL_TITLE_FONTSIZE = 13
STRUCTURAL_FONTSIZE = 11
SUPPORT_FONTSIZE = 10

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def encode_items(model, items, method, collect_context=False):
    states = []
    for item in np.asarray(items, dtype=int):
        model = getattr(model, method)(jnp.asarray(int(item)))
        if collect_context:
            states.append(np.asarray(model.context.state))
    if collect_context:
        return model, np.asarray(states)
    return model


def normalize_rows(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    return x / np.maximum(norms, 1e-12)


def make_scalar_model(scales: dict[str, float]):
    params, _ = load_fit_params(FIT_PATH)
    one_subject_params = {key: value[:1] for key, value in params.items()}
    paradigm = make_paradigm()
    factory = make_factory(
        is_emotional=make_is_emotional(
            paradigm,
            film_emotional=FILM_EMOTIONAL,
            interference_emotional=INTERFERENCE_EMOTIONAL,
        ),
        is_target=make_is_target(paradigm),
    )
    models = vmap(
        lambda p: factory(paradigm.list_length, p, None),
    )(one_subject_params)
    models = models.replace(n_film=jnp.asarray([paradigm.n_film]))
    configured = configure_rates(models, **scales)
    return tree_util.tree_map(
        lambda x: x[0]
        if hasattr(x, "shape") and len(x.shape) > 0 and x.shape[0] == 1
        else x,
        configured,
    )


def make_paradigm() -> Paradigm:
    return Paradigm(
        n_film=N_FILM,
        n_break=N_BREAK,
        n_interference=N_INTERFERENCE,
        n_filler=N_FILLER,
        experiment_count=EXPERIMENT_COUNT,
        max_recall=MAX_RECALL,
    )


def trace_high_interference_contexts() -> tuple[Paradigm, np.ndarray, np.ndarray]:
    paradigm = make_paradigm()
    fixed_scales = {
        **BASE_FIXED_SCALES,
        **REMINDER_SCALES,
        "interference_mcf_scale": TASK_MCF_SCALE,
    }
    model = make_scalar_model(fixed_scales)
    model, film_context = encode_items(
        model,
        paradigm.film_items,
        "experience_film",
        collect_context=True,
    )
    model = encode_items(model, paradigm.break_items, "experience_break")
    model = model.start_reminders()
    model = encode_items(model, paradigm.film_items, "remind")
    model, task_context = encode_items(
        model,
        paradigm.interference_items,
        "experience_interference",
        collect_context=True,
    )
    return paradigm, film_context, task_context


def context_similarity(film_context: np.ndarray, task_context: np.ndarray) -> np.ndarray:
    return normalize_rows(film_context) @ normalize_rows(task_context).T


def goal_augmented_similarity(
    film_context: np.ndarray,
    task_context: np.ndarray,
    goal_weight: float,
) -> np.ndarray:
    film_goal = np.full((film_context.shape[0], 1), goal_weight, dtype=float)
    task_goal = np.zeros((task_context.shape[0], 1), dtype=float)
    film_augmented = np.concatenate([film_context, film_goal], axis=1)
    task_augmented = np.concatenate([task_context, task_goal], axis=1)
    return context_similarity(film_augmented, task_augmented)


def build_rows(matrices: dict[str, np.ndarray]) -> list[dict]:
    rows = []
    for panel, matrix in matrices.items():
        for film_position in range(matrix.shape[0]):
            for task_position in range(matrix.shape[1]):
                rows.append(
                    {
                        "panel": panel,
                        "reminder_condition": REMINDER_CONDITION,
                        "task_condition": TASK_CONDITION,
                        "task_mcf_scale": TASK_MCF_SCALE,
                        "film_retrieval_goal_weight": FILM_RETRIEVAL_GOAL_WEIGHT,
                        "film_position": film_position + 1,
                        "task_position": task_position + 1,
                        "context_similarity": float(matrix[film_position, task_position]),
                    }
                )
    return rows


def build_summary_rows(matrices: dict[str, np.ndarray]) -> list[dict]:
    rows = []
    for panel, matrix in matrices.items():
        mean_similarity = matrix.mean(axis=1)
        max_similarity = matrix.max(axis=1)
        for film_position, (mean_value, max_value) in enumerate(
            zip(mean_similarity, max_similarity),
            start=1,
        ):
            rows.append(
                {
                    "panel": panel,
                    "reminder_condition": REMINDER_CONDITION,
                    "task_condition": TASK_CONDITION,
                    "task_mcf_scale": TASK_MCF_SCALE,
                    "film_retrieval_goal_weight": FILM_RETRIEVAL_GOAL_WEIGHT,
                    "film_position": film_position,
                    "mean_similarity_to_task_contexts": float(mean_value),
                    "max_similarity_to_task_context": float(max_value),
                }
            )
    return rows


def plot_summary(paradigm: Paradigm, matrices: dict[str, np.ndarray]) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(8.2, 7.8))
    outer = fig.add_gridspec(
        5,
        1,
        height_ratios=[0.16, 0.78, 0.18, 0.24, 1.12],
        hspace=0.08,
        left=0.105,
        right=0.955,
        top=0.940,
        bottom=0.095,
    )
    title_axis_a = fig.add_subplot(outer[0, 0])
    title_axis_b = fig.add_subplot(outer[3, 0])
    for title_axis, letter, title in [
        (
            title_axis_a,
            "A",
            "Mean task overlap with film-context retrieval cues",
        ),
        (
            title_axis_b,
            "B",
            "Task overlap with film-context retrieval cues",
        ),
    ]:
        title_axis.axis("off")
        title_y = 0.86 if letter == "A" else 0.70
        title_axis.text(
            -0.055,
            title_y,
            letter,
            ha="left",
            va="top",
            fontsize=PANEL_LETTER_FONTSIZE,
            fontweight="bold",
            transform=title_axis.transAxes,
        )
        title_axis.text(
            0.5,
            title_y,
            title,
            ha="center",
            va="top",
            fontsize=PANEL_TITLE_FONTSIZE,
            fontweight="bold",
            transform=title_axis.transAxes,
        )

    line_grid = outer[1, 0].subgridspec(
        1,
        3,
        width_ratios=[0.22, 1.0, 0.22],
        wspace=0.0,
    )
    axis = fig.add_subplot(line_grid[0, 1])
    positions = np.arange(1, paradigm.n_film + 1)
    mean_temporal = matrices["Without film-retrieval goal"].mean(axis=1)
    mean_goal = matrices["With film-retrieval goal"].mean(axis=1)
    axis.plot(
        positions,
        mean_temporal,
        color="#7C8794",
        linestyle=(0, (3, 2)),
        linewidth=2.0,
        label="Without film-retrieval goal",
    )
    axis.plot(
        positions,
        mean_goal,
        color=PHASE_COLORS["film"],
        linewidth=2.0,
        label="With film-retrieval goal",
    )
    axis.set_xlabel("Encoded film position", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_ylabel("Mean task-context overlap", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_xlim(1, paradigm.n_film)
    axis.set_xticks([1, 4, 8, 12, 16])
    axis.set_ylim(0, max(float(np.max(mean_temporal)), float(np.max(mean_goal))) * 1.15)
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.grid(axis="y", color="#E7EBF0", linewidth=0.45, alpha=0.45, zorder=0)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.legend(
        frameon=False,
        fontsize=SUPPORT_FONTSIZE,
        loc="upper left",
        handlelength=2.4,
    )
    heatmap_grid = outer[4, 0].subgridspec(
        1,
        3,
        width_ratios=[1.0, 1.0, 0.055],
        wspace=0.20,
    )
    heatmap_axes = [
        (
            fig.add_subplot(heatmap_grid[0, 0]),
            "Without film-retrieval goal",
            matrices["Without film-retrieval goal"],
        ),
        (
            fig.add_subplot(heatmap_grid[0, 1]),
            "With film-retrieval goal",
            matrices["With film-retrieval goal"],
        ),
    ]
    colorbar_axis = fig.add_subplot(heatmap_grid[0, 2])
    similarity_max = max(float(np.max(value)) for value in matrices.values())
    heatmap_image = None
    for heatmap_axis, title, matrix in heatmap_axes:
        heatmap_image = heatmap_axis.imshow(
            matrix.T,
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            cmap="viridis",
            vmin=0.0,
            vmax=similarity_max,
        )
        heatmap_axis.set_title(
            title,
            fontsize=STRUCTURAL_FONTSIZE,
            pad=7,
        )
        heatmap_axis.set_xlabel(
            "Encoded film position",
            fontsize=STRUCTURAL_FONTSIZE,
        )
        heatmap_axis.set_xticks([0, 7, 15], ["1", "8", "16"])
        heatmap_axis.set_yticks([0, 7, 15], ["1", "8", "16"])
        heatmap_axis.tick_params(labelsize=SUPPORT_FONTSIZE, length=3)
        for spine in heatmap_axis.spines.values():
            spine.set_color("#2F3A45")
            spine.set_linewidth(0.9)
    heatmap_axes[0][0].set_ylabel(
        "Encoded task position",
        fontsize=STRUCTURAL_FONTSIZE,
    )
    heatmap_axes[1][0].tick_params(labelleft=False)
    if heatmap_image is not None:
        colorbar = fig.colorbar(heatmap_image, cax=colorbar_axis)
        colorbar.ax.set_title("Overlap", fontsize=STRUCTURAL_FONTSIZE, pad=7)
        colorbar.ax.tick_params(labelsize=SUPPORT_FONTSIZE)
    base = FIGURE_DIR / OUTPUT_PREFIX
    fig.savefig(f"{base}.png", dpi=600)
    fig.savefig(f"{base}.svg")
    fig.savefig(f"{base}.pdf")
    plt.close(fig)
    print(f"{base}.png")
    print(f"{base}.svg")
    print(f"{base}.pdf")


def main() -> None:
    paradigm, film_context, task_context = trace_high_interference_contexts()
    matrices = {
        "Without film-retrieval goal": context_similarity(film_context, task_context),
        "With film-retrieval goal": goal_augmented_similarity(
            film_context,
            task_context,
            FILM_RETRIEVAL_GOAL_WEIGHT,
        ),
    }
    write_rows(
        FIGURE_DIR / f"{OUTPUT_PREFIX}.csv",
        [
            "panel",
            "reminder_condition",
            "task_condition",
            "task_mcf_scale",
            "film_retrieval_goal_weight",
            "film_position",
            "task_position",
            "context_similarity",
        ],
        build_rows(matrices),
    )
    write_rows(
        FIGURE_DIR / f"{OUTPUT_PREFIX}_summary.csv",
        [
            "panel",
            "reminder_condition",
            "task_condition",
            "task_mcf_scale",
            "film_retrieval_goal_weight",
            "film_position",
            "mean_similarity_to_task_contexts",
            "max_similarity_to_task_context",
        ],
        build_summary_rows(matrices),
    )
    plot_summary(paradigm, matrices)


if __name__ == "__main__":
    main()
