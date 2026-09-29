"""Render the Figure 10 candidate from a preserved subset of saved results.

Run from any directory with the manuscript project's Python environment.
This does not run simulations or change manuscript files.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
import numpy as np


PACKAGE = Path(__file__).resolve().parent
BASELINE = "No deliberate control"
PANELS = [
    ("A", "Start-of-film reinstatement", "start-of-film reinstatement"),
    ("B", "Maintained film-category cue", "maintained film-category cue"),
    ("C", "Retrieval monitoring", "retrieval monitoring"),
]
PHASES = [
    ("Film", 1, 16, "#1760BD", "#EEF4FC"),
    ("Break", 17, 32, "#586575", "#F5F6F8"),
    ("Task", 33, 48, "#C65F1C", "#FFF3E9"),
    ("Filler", 49, 64, "#586575", "#F5F6F8"),
]
CONDITIONS = {
    "reminder_condition": "With reminder",
    "task_condition": "Strong task encoding",
    "task_mcf_scale": "2.0",
    "film_cue_reinstatement": "0.9",
    "cue_interval": "4",
    "first_cue_after": "0",
    "experiment_count": "5000",
}
# start reinstatement scale, sustained film support, non-film context updating
CONTROL_VALUES = {
    BASELINE: (0.0, 0.0, 1.0),
    "start-of-film reinstatement": (1.0, 0.0, 1.0),
    "maintained film-category cue": (0.0, 1.0, 1.0),
    "retrieval monitoring": (0.0, 0.0, 0.0),
}


def load_curves() -> dict[str, np.ndarray]:
    data = PACKAGE / "data" / "position_curves.csv"
    provenance = json.loads((PACKAGE / "provenance.json").read_text())
    digest = hashlib.sha256(data.read_bytes()).hexdigest()
    if digest != provenance["selected_data_sha256"]:
        raise ValueError("The preserved plotting data have changed; review provenance before rendering.")
    with data.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 256
    assert {r["retrieval_control_package"] for r in rows} == set(CONTROL_VALUES)
    curves = {}
    expected_phases = [phase.lower() for phase, lo, hi, _, _ in PHASES for _ in range(lo, hi + 1)]
    for name, parameters in CONTROL_VALUES.items():
        selected = sorted(
            (r for r in rows if r["retrieval_control_package"] == name),
            key=lambda r: int(r["position"]),
        )
        assert [int(r["position"]) for r in selected] == list(range(1, 65)), name
        assert [r["phase"] for r in selected] == expected_phases, name
        for row in selected:
            assert all(row[k] == v for k, v in CONDITIONS.items()), (name, row)
            assert tuple(float(row[k]) for k in (
                "start_drift_scale", "film_item_support_boost", "rejected_recall_drift_scale"
            )) == parameters, name
        values = np.array([float(r["recall_probability"]) for r in selected])
        assert np.isfinite(values).all() and ((values >= 0) & (values <= 1)).all()
        curves[name] = values
    return curves


def write_summary(curves: dict[str, np.ndarray]) -> None:
    fields = ["control", "phase", "mean_recall_probability", "expected_items_recalled",
              "difference_in_expected_items_from_baseline"]
    with (PACKAGE / "phase_summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for name, values in curves.items():
            for phase, lo, hi, _, _ in PHASES:
                selected = values[lo - 1:hi]
                baseline = curves[BASELINE][lo - 1:hi]
                writer.writerow({
                    "control": name,
                    "phase": phase.lower(),
                    "mean_recall_probability": f"{selected.mean():.9f}",
                    "expected_items_recalled": f"{selected.sum():.9f}",
                    "difference_in_expected_items_from_baseline": f"{(selected - baseline).sum():.9f}",
                })


def main() -> None:
    curves = load_curves()
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 10,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "axes.linewidth": 0.8,
        "savefig.facecolor": "white",
    })
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 7.4), sharex=True, sharey=True)
    # A single scale for every panel, determined from all four saved curves.
    ceiling = float(np.ceil(max(v.max() for v in curves.values()) * 1.06 / 0.1) * 0.1)
    positions = np.arange(1, 65)
    for ax, (letter, title, name) in zip(axes, PANELS, strict=True):
        for phase, lo, hi, ink, tint in PHASES:
            ax.axvspan(lo - 0.5, hi + 0.5, facecolor=tint, edgecolor="none", zorder=0)
            ax.text((lo + hi) / 2, 0.94, phase, color=ink, fontsize=9.5,
                    fontweight="bold", ha="center", va="top", transform=ax.get_xaxis_transform())
        for edge in (16.5, 32.5, 48.5):
            ax.axvline(edge, color="#B8C1CA", lw=0.6, zorder=1)
        ax.plot(positions, curves[BASELINE], color="#7C8794", ls=(0, (4, 2.8)), lw=1.7, zorder=3)
        ax.plot(positions, curves[name], color="#161A1F", lw=1.8, zorder=4)
        ax.set_xlim(0.5, 64.5)
        ax.set_ylim(0, ceiling)
        ax.set_xticks([1, 16, 32, 48, 64])
        ax.yaxis.set_major_locator(MultipleLocator(0.2))
        ax.grid(axis="y", color="#DDE3EA", lw=0.55, zorder=1)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color("#65717D")
        ax.tick_params(axis="both", labelsize=9, length=3, color="#65717D")
        ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        ax.text(-0.085, 1.08, letter, transform=ax.transAxes, fontsize=15,
                fontweight="bold", va="bottom", ha="left")
    axes[-1].set_xlabel("Encoded position", fontsize=11, labelpad=7)
    fig.supylabel("Recall probability", x=0.025, fontsize=11)
    fig.legend(handles=[
        Line2D([], [], color="#7C8794", ls=(0, (4, 2.8)), lw=1.7, label="No control operations"),
        Line2D([], [], color="#161A1F", lw=1.8, label="One control operation"),
    ], loc="lower center", bbox_to_anchor=(0.54, 0.015), ncol=2,
       fontsize=9.5, frameon=False, handlelength=3, columnspacing=2)
    fig.subplots_adjust(left=0.115, right=0.985, bottom=0.115, top=0.94, hspace=0.47)
    for suffix in ("png", "svg", "pdf"):
        fig.savefig(PACKAGE / f"figure10_candidate.{suffix}", dpi=300)
    plt.close(fig)
    write_summary(curves)
    print("Verified 4 conditions × 64 positions; saved PNG, SVG, PDF and phase summary.")


if __name__ == "__main__":
    main()
