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
OUTPUT_PREFIX = "simulation1_unguided_cued_context_overlap"
FIT_PATH = ROOT / "results/fits/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json"

N_FILM = 16
N_BREAK = 16
N_INTERFERENCE = 16
N_FILLER = 16
EXPERIMENT_COUNT = 5000
MAX_RECALL = 48

FILM_EMOTIONAL = True
INTERFERENCE_EMOTIONAL = False

BASE_FIXED_SCALES = {
    "break_drift_scale": 1.0,
    "break_mcf_scale": 1.0,
    "filler_drift_scale": 1.0,
    "filler_mcf_scale": 1.0,
    "source_learning_baseline": 0.05,
    "primacy_scale": 0.1,
    "primacy_decay": 1.5,
}

REMINDER_CONDITIONS = {
    "Without pre-task reminder": {
        "reminder_start_drift_scale": 0.0,
        "reminder_drift_scale": 0.0,
    },
    "With pre-task film reminder": {
        "reminder_start_drift_scale": 1.0,
        "reminder_drift_scale": 1.0,
    },
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


def make_paradigm() -> Paradigm:
    return Paradigm(
        n_film=N_FILM,
        n_break=N_BREAK,
        n_interference=N_INTERFERENCE,
        n_filler=N_FILLER,
        experiment_count=EXPERIMENT_COUNT,
        max_recall=MAX_RECALL,
    )


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


def trace_contexts(reminder_scales: dict[str, float]) -> tuple[np.ndarray, np.ndarray]:
    paradigm = make_paradigm()
    fixed_scales = {**BASE_FIXED_SCALES, **reminder_scales}
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
    _, task_context = encode_items(
        model,
        paradigm.interference_items,
        "experience_interference",
        collect_context=True,
    )
    return film_context, task_context


def context_overlap(film_context: np.ndarray, task_context: np.ndarray) -> np.ndarray:
    return normalize_rows(film_context) @ normalize_rows(task_context).T


def build_rows(matrices: dict[str, np.ndarray]) -> list[dict]:
    rows = []
    for reminder_condition, matrix in matrices.items():
        for film_position in range(matrix.shape[0]):
            for task_position in range(matrix.shape[1]):
                rows.append(
                    {
                        "reminder_condition": reminder_condition,
                        "film_position": film_position + 1,
                        "task_position": task_position + 1,
                        "context_overlap": float(matrix[film_position, task_position]),
                    }
                )
    return rows


def build_summary_rows(matrices: dict[str, np.ndarray]) -> list[dict]:
    rows = []
    for reminder_condition, matrix in matrices.items():
        mean_overlap = matrix.mean(axis=1)
        max_overlap = matrix.max(axis=1)
        for film_position, (mean_value, max_value) in enumerate(
            zip(mean_overlap, max_overlap),
            start=1,
        ):
            rows.append(
                {
                    "reminder_condition": reminder_condition,
                    "film_position": film_position,
                    "mean_task_context_overlap": float(mean_value),
                    "max_task_context_overlap": float(max_value),
                }
            )
    return rows


def plot_candidate(paradigm: Paradigm, matrices: dict[str, np.ndarray]) -> None:
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
            "Mean task-context overlap by film position",
        ),
        (
            title_axis_b,
            "B",
            "Film-task context overlap by position",
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
    axis.plot(
        positions,
        matrices["Without pre-task reminder"].mean(axis=1),
        color="#7C8794",
        linestyle=(0, (3, 2)),
        linewidth=2.0,
        label="Without pre-task reminder",
    )
    axis.plot(
        positions,
        matrices["With pre-task film reminder"].mean(axis=1),
        color=PHASE_COLORS["film"],
        linewidth=2.0,
        label="With pre-task film reminder",
    )
    axis.set_xlabel("Encoded film position", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_ylabel("Mean task-context overlap", fontsize=STRUCTURAL_FONTSIZE)
    axis.set_xlim(1, paradigm.n_film)
    axis.set_xticks([1, 4, 8, 12, 16])
    max_mean = max(float(np.max(matrix.mean(axis=1))) for matrix in matrices.values())
    axis.set_ylim(0, max_mean * 1.15)
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
            "Without pre-task reminder",
            matrices["Without pre-task reminder"],
        ),
        (
            fig.add_subplot(heatmap_grid[0, 1]),
            "With pre-task film reminder",
            matrices["With pre-task film reminder"],
        ),
    ]
    colorbar_axis = fig.add_subplot(heatmap_grid[0, 2])
    overlap_max = max(float(np.max(value)) for value in matrices.values())
    heatmap_image = None
    for heatmap_axis, title, matrix in heatmap_axes:
        heatmap_image = heatmap_axis.imshow(
            matrix.T,
            origin="lower",
            aspect="auto",
            interpolation="nearest",
            cmap="viridis",
            vmin=0.0,
            vmax=overlap_max,
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
        colorbar.ax.set_title("Context\noverlap", fontsize=STRUCTURAL_FONTSIZE, pad=7)
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
    paradigm = make_paradigm()
    matrices = {}
    for reminder_condition, reminder_scales in REMINDER_CONDITIONS.items():
        film_context, task_context = trace_contexts(reminder_scales)
        matrices[reminder_condition] = context_overlap(film_context, task_context)
    write_rows(
        FIGURE_DIR / f"{OUTPUT_PREFIX}.csv",
        [
            "reminder_condition",
            "film_position",
            "task_position",
            "context_overlap",
        ],
        build_rows(matrices),
    )
    write_rows(
        FIGURE_DIR / f"{OUTPUT_PREFIX}_summary.csv",
        [
            "reminder_condition",
            "film_position",
            "mean_task_context_overlap",
            "max_task_context_overlap",
        ],
        build_summary_rows(matrices),
    )
    plot_candidate(paradigm, matrices)


if __name__ == "__main__":
    main()
