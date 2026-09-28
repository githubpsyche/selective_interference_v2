from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "work/simulation2_start_context_reinstatement"
REVIEW_DIR = SOURCE_DIR / "review_start_strength"
NOTEBOOK = SOURCE_DIR / "simulation2_start_context_reinstatement.ipynb"

COMPARISON_PREFIX = "recomputed_beta_comparison"

ONGOING_KEY = "Ongoing context"
MAXIMAL_KEY = "Maximal reinstatement"
MATCHED_KEY = "Matched reinstatement"
STYLES = {
    ONGOING_KEY: {
        "color": "#7C8794",
        "linestyle": (0, (3, 2)),
        "linewidth": 2.0,
    },
    "reinstatement": {
        "color": "#111111",
        "linestyle": "-",
        "linewidth": 2.0,
    },
}

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]


def cell_source(cell: dict) -> str:
    source = cell["source"]
    return "".join(source) if isinstance(source, list) else source


def generate_matched_data() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    namespace: dict[str, object] = {"__name__": "review_notebook"}
    previous_cwd = Path.cwd()
    os.chdir(ROOT)
    try:
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] != "code":
                continue
            exec(compile(cell_source(cell), f"{NOTEBOOK.name}:cell-{index}", "exec"), namespace)
            if index == 3:
                namespace["PROJECT_ROOT"] = str(ROOT)
                namespace["FIGURE_DIR"] = str(REVIEW_DIR.relative_to(ROOT))
                namespace["DATA_DIR"] = str(REVIEW_DIR.relative_to(ROOT))
                namespace["FIGURE_STR"] = COMPARISON_PREFIX
                namespace["RETRIEVAL_SETTINGS"] = [
                    {
                        "label": ONGOING_KEY,
                        "figure_label": ONGOING_KEY,
                        "start_drift_scale": 0.0,
                    },
                    {
                        "label": MAXIMAL_KEY,
                        "figure_label": MAXIMAL_KEY,
                        "start_drift_scale": 1.5,
                    },
                    {
                        "label": MATCHED_KEY,
                        "figure_label": MATCHED_KEY,
                        "start_drift_scale": 1.0,
                    },
                ]
    finally:
        os.chdir(previous_cwd)


def read_curves(
    path: Path,
    value_key: str,
    settings: list[str],
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    curves: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for setting in settings:
        selected = sorted(
            [
                row
                for row in rows
                if row["retrieval_setting"] == setting and row["phase"] == "film"
            ],
            key=lambda row: int(row["position"]),
        )
        encoded_positions = np.asarray([int(row["position"]) for row in selected])
        film_positions = encoded_positions - encoded_positions.min() + 1
        values = np.asarray([float(row[value_key]) for row in selected])
        curves[setting] = (film_positions, values)
    return curves


def plot_curves(
    axis: plt.Axes,
    curves: dict[str, tuple[np.ndarray, np.ndarray]],
    reinstatement_key: str,
) -> None:
    display_labels = {
        ONGOING_KEY: "Ongoing context",
        reinstatement_key: "Reinstated start-of-film context",
    }
    for setting in [ONGOING_KEY, reinstatement_key]:
        positions, values = curves[setting]
        style = STYLES[ONGOING_KEY] if setting == ONGOING_KEY else STYLES["reinstatement"]
        axis.plot(
            positions,
            values,
            label=display_labels[setting],
            **style,
        )
    axis.set_xlim(1, 16)
    axis.set_xticks([1, 4, 8, 12, 16])
    axis.grid(axis="y", color="#E7EBF0", linewidth=0.6)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def render_comparison() -> None:
    datasets = [
        (
            "Current parameter choice, recomputed: maximal reinstatement (effective beta = 1.0)",
            MAXIMAL_KEY,
        ),
        (
            "Matched diagnostic: main-analysis reinstatement (effective beta = .766)",
            MATCHED_KEY,
        ),
    ]

    loaded = []
    for label, reinstatement_key in datasets:
        loaded.append(
            (
                label,
                reinstatement_key,
                read_curves(
                    REVIEW_DIR / f"{COMPARISON_PREFIX}_pfr.csv",
                    "first_recall_probability",
                    [ONGOING_KEY, reinstatement_key],
                ),
                read_curves(
                    REVIEW_DIR / f"{COMPARISON_PREFIX}_spc.csv",
                    "recall_probability",
                    [ONGOING_KEY, reinstatement_key],
                ),
            )
        )

    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.0), sharex="col", sharey="col")
    column_titles = ["First recall", "Recall across search"]
    ylabels = ["Probability of first recall", "Recall probability"]

    for row, (row_label, reinstatement_key, pfr_curves, spc_curves) in enumerate(loaded):
        for column, curves in enumerate([pfr_curves, spc_curves]):
            axis = axes[row, column]
            plot_curves(axis, curves, reinstatement_key)
            axis.set_xlabel("Encoded film position")
            axis.set_ylabel(ylabels[column])
            if row == 0:
                axis.set_title(column_titles[column], fontsize=13, fontweight="bold")
        axes[row, 0].text(
            -0.03,
            1.09,
            row_label,
            transform=axes[row, 0].transAxes,
            fontsize=11,
            fontweight="bold",
            ha="left",
            va="bottom",
        )

    for column in range(2):
        maximum = max(
            max(float(values.max()) for _, values in loaded[row][column + 2].values())
            for row in range(2)
        )
        for row in range(2):
            axes[row, column].set_ylim(0, maximum * 1.12)

    handles, labels = axes[0, 1].get_legend_handles_labels()
    figure.legend(
        handles,
        labels,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.005),
        ncol=2,
        handlelength=3.0,
        columnspacing=2.2,
    )
    figure.subplots_adjust(
        left=0.10,
        right=0.98,
        top=0.91,
        bottom=0.12,
        hspace=0.42,
        wspace=0.28,
    )

    output = REVIEW_DIR / "start_reinstatement_strength_comparison"
    figure.savefig(f"{output}.png", dpi=300, bbox_inches="tight")
    figure.savefig(f"{output}.svg", bbox_inches="tight")
    plt.close(figure)


def summarize_difference() -> None:
    pfr_curves = read_curves(
        REVIEW_DIR / f"{COMPARISON_PREFIX}_pfr.csv",
        "first_recall_probability",
        [MAXIMAL_KEY, MATCHED_KEY],
    )
    spc_curves = read_curves(
        REVIEW_DIR / f"{COMPARISON_PREFIX}_spc.csv",
        "recall_probability",
        [MAXIMAL_KEY, MATCHED_KEY],
    )
    current_pfr = pfr_curves[MAXIMAL_KEY][1]
    matched_pfr = pfr_curves[MATCHED_KEY][1]
    current_spc = spc_curves[MAXIMAL_KEY][1]
    matched_spc = spc_curves[MATCHED_KEY][1]

    rows = [
        {
            "measure": "first_recall_positions_1_to_5",
            "current_beta_1p0": float(current_pfr[:5].sum()),
            "matched_beta_0p766": float(matched_pfr[:5].sum()),
        },
        {
            "measure": "recall_positions_1_to_5_mean",
            "current_beta_1p0": float(current_spc[:5].mean()),
            "matched_beta_0p766": float(matched_spc[:5].mean()),
        },
        {
            "measure": "film_items_recalled_sum",
            "current_beta_1p0": float(current_spc.sum()),
            "matched_beta_0p766": float(matched_spc.sum()),
        },
    ]
    with (REVIEW_DIR / "comparison_summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    generate_matched_data()
    render_comparison()
    summarize_difference()


if __name__ == "__main__":
    main()
