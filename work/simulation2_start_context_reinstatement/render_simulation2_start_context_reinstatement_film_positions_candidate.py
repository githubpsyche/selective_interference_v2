from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


FIGURE_DIR = Path(__file__).resolve().parent
SOURCE_PREFIX = "simulation2_start_context_reinstatement"
OUTPUT_PREFIX = f"{SOURCE_PREFIX}_film_positions_candidate"

PFR_PATH = FIGURE_DIR / f"{SOURCE_PREFIX}_pfr.csv"
SPC_PATH = FIGURE_DIR / f"{SOURCE_PREFIX}_spc.csv"

UNGUIDED_LABEL = "Unguided recall"
REINSTATEMENT_LABEL = "Start-of-film context reinstatement"
SETTINGS = [UNGUIDED_LABEL, REINSTATEMENT_LABEL]
STYLES = {
    UNGUIDED_LABEL: {
        "color": "#7C8794",
        "linestyle": (0, (3, 2)),
        "linewidth": 2.0,
    },
    REINSTATEMENT_LABEL: {
        "color": "#111111",
        "linestyle": "-",
        "linewidth": 2.0,
    },
}

PANEL_LETTER_SIZE = 15
PANEL_TITLE_SIZE = 12
AXIS_LABEL_SIZE = 11
TICK_SIZE = 9.5
LEGEND_SIZE = 9.5
GRID_COLOR = "#E7EBF0"

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]


def read_film_curves(path: Path, value_key: str) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    curves: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for setting in SETTINGS:
        film_rows = sorted(
            [
                row
                for row in rows
                if row["retrieval_setting"] == setting and row["phase"] == "film"
            ],
            key=lambda row: int(row["position"]),
        )
        if not film_rows:
            raise ValueError(f"No film rows found for {setting} in {path}")

        encoded_positions = np.asarray(
            [int(row["position"]) for row in film_rows],
            dtype=int,
        )
        film_positions = encoded_positions - encoded_positions.min() + 1
        values = np.asarray([float(row[value_key]) for row in film_rows], dtype=float)
        curves[setting] = (film_positions, values)

    return curves


def style_axis(
    axis: plt.Axes,
    panel: str,
    title: str,
    ylabel: str,
    curves: dict[str, tuple[np.ndarray, np.ndarray]],
) -> None:
    for setting in SETTINGS:
        positions, values = curves[setting]
        axis.plot(positions, values, label=setting, **STYLES[setting])

    film_positions = curves[SETTINGS[0]][0]
    axis.set_xlim(float(film_positions.min()), float(film_positions.max()))
    axis.set_xticks([1, 4, 8, 12, 16])
    axis.set_xlabel("Encoded film position", fontsize=AXIS_LABEL_SIZE, labelpad=6)
    axis.set_ylabel(ylabel, fontsize=AXIS_LABEL_SIZE, labelpad=6)

    maximum = max(float(values.max()) for _, values in curves.values())
    axis.set_ylim(0, maximum * 1.13)

    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.6)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.tick_params(labelsize=TICK_SIZE)

    axis.text(
        -0.12,
        1.08,
        panel,
        transform=axis.transAxes,
        fontsize=PANEL_LETTER_SIZE,
        fontweight="bold",
        ha="left",
        va="top",
    )
    axis.set_title(title, fontsize=PANEL_TITLE_SIZE, fontweight="bold", pad=13)


def main() -> None:
    first_recall_curves = read_film_curves(PFR_PATH, "first_recall_probability")
    full_recall_curves = read_film_curves(SPC_PATH, "recall_probability")

    figure, axes = plt.subplots(1, 2, figsize=(7.4, 3.35))
    style_axis(
        axes[0],
        "A",
        "First recall",
        "Probability of first recall",
        first_recall_curves,
    )
    style_axis(
        axes[1],
        "B",
        "Recall across search",
        "Recall probability",
        full_recall_curves,
    )

    handles, labels = axes[1].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        frameon=False,
        fontsize=LEGEND_SIZE,
        loc="lower center",
        bbox_to_anchor=(0.52, 0.005),
        ncol=2,
        handlelength=2.8,
        columnspacing=2.2,
    )
    figure.subplots_adjust(
        left=0.105,
        right=0.975,
        top=0.84,
        bottom=0.25,
        wspace=0.36,
    )

    output_base = FIGURE_DIR / OUTPUT_PREFIX
    for suffix in ["png", "svg"]:
        figure.savefig(
            f"{output_base}.{suffix}",
            bbox_inches="tight",
            dpi=600,
        )
    plt.close(figure)


if __name__ == "__main__":
    main()
