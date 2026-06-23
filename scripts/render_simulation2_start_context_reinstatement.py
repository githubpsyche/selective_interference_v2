from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from selective_interference_v2 import PHASE_COLORS, add_phase_bands


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
FIGURE_STR = "simulation2_start_context_reinstatement"

SUPPORT_PATH = FIGURE_DIR / f"{FIGURE_STR}_support.csv"
PFR_PATH = FIGURE_DIR / f"{FIGURE_STR}_pfr.csv"
SPC_PATH = FIGURE_DIR / f"{FIGURE_STR}_spc.csv"

PANEL_LETTER_FONTSIZE = 16
PANEL_TITLE_FONTSIZE = 13
STRUCTURAL_FONTSIZE = 11
SUPPORT_FONTSIZE = 10

plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

UNGUIDED_LABEL = "Unguided recall"
REINSTATEMENT_LABEL = "Start-of-film context reinstatement"
SETTING_STYLES = {
    UNGUIDED_LABEL: {
        "color": "#7C8794",
        "linestyle": (0, (3, 2)),
        "linewidth": 1.7,
    },
    REINSTATEMENT_LABEL: {
        "color": "#111111",
        "linestyle": "-",
        "linewidth": 1.7,
    },
}
GRID_COLOR = "#E7EBF0"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def coerce_position_rows(rows: list[dict[str, str]], value_key: str) -> list[dict]:
    out = []
    for row in rows:
        out.append(
            {
                **row,
                "position": int(row["position"]),
                value_key: float(row[value_key]),
            }
        )
    return out


def position_phase(rows: list[dict]) -> list[str]:
    first_setting = rows[0]["retrieval_setting"]
    ordered = sorted(
        [row for row in rows if row["retrieval_setting"] == first_setting],
        key=lambda row: row["position"],
    )
    return [row["phase"] for row in ordered]


def curve_by_setting(rows: list[dict], value_key: str) -> dict[str, np.ndarray]:
    curves = {}
    for setting in [UNGUIDED_LABEL, REINSTATEMENT_LABEL]:
        setting_rows = sorted(
            [row for row in rows if row["retrieval_setting"] == setting],
            key=lambda row: row["position"],
        )
        if not setting_rows:
            raise ValueError(f"Missing rows for {setting}")
        curves[setting] = np.asarray([row[value_key] for row in setting_rows], dtype=float)
    return curves


def add_panel_heading(axis, label: str, title: str, x: float = -0.12, y: float = 0.86) -> None:
    axis.axis("off")
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
    axis.text(
        0.5,
        y,
        title,
        transform=axis.transAxes,
        fontsize=PANEL_TITLE_FONTSIZE,
        fontweight="bold",
        va="top",
        ha="center",
    )


def add_phase_boundaries(axis, phases: list[str]) -> None:
    current = phases[0]
    for index, phase in enumerate(phases[1:], start=2):
        if phase != current:
            axis.axvline(index - 0.5, color="#7C8794", linewidth=0.7, alpha=0.45, zorder=1)
            current = phase


def add_reminder_marker(axis) -> None:
    reminder_x = 32.5
    axis.axvline(reminder_x, color=PHASE_COLORS["reminder"], linewidth=1.6, alpha=0.85, zorder=2)
    axis.text(
        reminder_x - 1.05,
        0.62,
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
        zorder=3,
    )


def style_axis(axis) -> None:
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.set_axisbelow(True)
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.45, alpha=0.45, zorder=0)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def padded_ylim(curves: dict[str, np.ndarray], minimum_upper: float, lower: float = 0.0) -> tuple[float, float]:
    max_value = max(float(np.nanmax(curve)) for curve in curves.values())
    return lower, max(minimum_upper, max_value * 1.16)


def plot_position_curves(
    axis,
    phases: list[str],
    curves: dict[str, np.ndarray],
    ylabel: str,
    ylim: tuple[float, float],
) -> None:
    positions = np.arange(1, len(phases) + 1)
    add_phase_bands(axis, phases, fontsize=SUPPORT_FONTSIZE)
    add_phase_boundaries(axis, phases)
    add_reminder_marker(axis)
    for setting, curve in curves.items():
        style = SETTING_STYLES[setting]
        axis.plot(
            positions,
            curve,
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            label=setting,
            zorder=3,
        )
    axis.set_xlabel("Encoded position", fontsize=STRUCTURAL_FONTSIZE, labelpad=7)
    axis.set_ylabel(ylabel, fontsize=STRUCTURAL_FONTSIZE)
    axis.set_xlim(1, len(phases))
    axis.set_ylim(*ylim)
    style_axis(axis)


def main() -> None:
    support_rows = coerce_position_rows(read_rows(SUPPORT_PATH), "raw_support")
    pfr_rows = coerce_position_rows(read_rows(PFR_PATH), "first_recall_probability")
    spc_rows = coerce_position_rows(read_rows(SPC_PATH), "recall_probability")
    phases = position_phase(spc_rows)

    support_curves = curve_by_setting(support_rows, "raw_support")
    pfr_curves = curve_by_setting(pfr_rows, "first_recall_probability")
    spc_curves = curve_by_setting(spc_rows, "recall_probability")

    fig = plt.figure(figsize=(8.2, 7.8))
    outer = fig.add_gridspec(
        5,
        4,
        height_ratios=[0.16, 1.0, 0.32, 0.16, 1.0],
        hspace=0.08,
        wspace=0.68,
        left=0.105,
        right=0.955,
        top=0.940,
        bottom=0.150,
    )

    heading_a = fig.add_subplot(outer[0, 0:2])
    heading_b = fig.add_subplot(outer[0, 2:4])
    heading_c = fig.add_subplot(outer[3, 1:3])
    add_panel_heading(heading_a, "A", "Item accessibility before first recall")
    add_panel_heading(heading_b, "B", "First recall probability distribution")
    add_panel_heading(heading_c, "C", "Full recall probability distribution")

    axis_a = fig.add_subplot(outer[1, 0:2])
    axis_b = fig.add_subplot(outer[1, 2:4])
    axis_c = fig.add_subplot(outer[4, 1:3])

    plot_position_curves(
        axis_a,
        phases,
        support_curves,
        "Retrieval support",
        padded_ylim(support_curves, minimum_upper=0.2),
    )
    plot_position_curves(
        axis_b,
        phases,
        pfr_curves,
        "Probability of first recall",
        padded_ylim(pfr_curves, minimum_upper=0.05, lower=-0.005),
    )
    plot_position_curves(
        axis_c,
        phases,
        spc_curves,
        "Recall probability",
        padded_ylim(spc_curves, minimum_upper=0.2, lower=-0.02),
    )

    handles, labels = axis_c.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        frameon=False,
        fontsize=SUPPORT_FONTSIZE,
        loc="lower center",
        bbox_to_anchor=(0.535, 0.030),
        ncol=2,
        handlelength=2.0,
        columnspacing=1.9,
    )

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    base = FIGURE_DIR / FIGURE_STR
    for suffix in ["png", "svg"]:
        fig.savefig(f"{base}.{suffix}", bbox_inches="tight", dpi=600)
    plt.close(fig)


if __name__ == "__main__":
    main()
