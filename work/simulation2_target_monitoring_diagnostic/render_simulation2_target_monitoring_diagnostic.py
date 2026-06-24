from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np

from selective_interference_v2 import PHASE_COLORS, add_phase_bands


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(__file__).resolve().parent
FIGURE_STR = "simulation2_target_monitoring_diagnostic"

SPC_PATH = DATA_DIR / "simulation2_control_cued_spc.csv"
RECOVERY_PATH = DATA_DIR / "simulation2_control_cued_offtarget_recovery.csv"

START_DRIFT_SCALE = 1.0
REMINDER_CONDITION = "With reminder"
TASK_MCF_SCALE = 2.0
NO_MONITORING_KAPPA = 1.0
MODERATE_MONITORING_KAPPA = 0.5

PANEL_LETTER_FONTSIZE = 16
PANEL_TITLE_FONTSIZE = 13
STRUCTURAL_FONTSIZE = 11
SUPPORT_FONTSIZE = 10
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

FILM_COLOR = PHASE_COLORS["film"]
NO_MONITORING_COLOR = "#7C8794"
MODERATE_MONITORING_COLOR = "#111111"
GRID_COLOR = "#E7EBF0"


def read_rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def coerce_spc_row(row):
    row = dict(row)
    row["start_drift_scale"] = float(row["start_drift_scale"])
    row["rejected_recall_drift_scale"] = float(row["rejected_recall_drift_scale"])
    row["task_mcf_scale"] = float(row["task_mcf_scale"])
    row["position"] = int(row["position"])
    row["recall_probability"] = float(row["recall_probability"])
    return row


def coerce_recovery_row(row):
    row = dict(row)
    row["start_drift_scale"] = float(row["start_drift_scale"])
    row["rejected_recall_drift_scale"] = float(row["rejected_recall_drift_scale"])
    row["task_mcf_scale"] = float(row["task_mcf_scale"])
    row["film_return_probability"] = float(row["film_return_probability"])
    row["transition_count"] = int(row["transition_count"])
    return row


def is_focus_row(row):
    return (
        np.isclose(row["start_drift_scale"], START_DRIFT_SCALE)
        and row["reminder_condition"] == REMINDER_CONDITION
        and np.isclose(row["task_mcf_scale"], TASK_MCF_SCALE)
    )


def target_monitoring_strength(kappa):
    return 1.0 - float(kappa)


def add_panel_heading(axis, label, title, y=0.86):
    axis.axis("off")
    axis.text(
        -0.055,
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


def style_axis(axis):
    axis.tick_params(labelsize=SUPPORT_FONTSIZE)
    axis.set_axisbelow(True)
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.45, alpha=0.45, zorder=0)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def add_phase_boundaries(axis, position_phase):
    boundaries = []
    current = position_phase[0]
    for index, phase in enumerate(position_phase[1:], start=2):
        if phase != current:
            boundaries.append(index - 0.5)
            current = phase
    for boundary in boundaries:
        axis.axvline(boundary, color="#7C8794", linewidth=0.7, alpha=0.45, zorder=1)


def add_reminder_marker(axis):
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


spc_rows = [coerce_spc_row(row) for row in read_rows(SPC_PATH)]
recovery_rows = [coerce_recovery_row(row) for row in read_rows(RECOVERY_PATH)]

focus_spc_rows = [row for row in spc_rows if is_focus_row(row)]
focus_recovery_rows = [row for row in recovery_rows if is_focus_row(row)]

if not focus_spc_rows or not focus_recovery_rows:
    raise ValueError("Missing current-regime target-monitoring rows.")

kappa_values = sorted(
    {row["rejected_recall_drift_scale"] for row in focus_recovery_rows},
    reverse=True,
)
monitoring_strengths = np.asarray([target_monitoring_strength(kappa) for kappa in kappa_values], dtype=float)

recovery_values = []
for kappa in kappa_values:
    matches = [
        row["film_return_probability"]
        for row in focus_recovery_rows
        if np.isclose(row["rejected_recall_drift_scale"], kappa)
    ]
    if not matches:
        raise ValueError(f"Missing off-target recovery row for kappa={kappa}")
    recovery_values.append(matches[0])
recovery_values = np.asarray(recovery_values, dtype=float)

spc_curves = {}
position_phase = []
for kappa in [NO_MONITORING_KAPPA, MODERATE_MONITORING_KAPPA]:
    curve_rows = [
        row
        for row in focus_spc_rows
        if np.isclose(row["rejected_recall_drift_scale"], kappa)
    ]
    curve_rows = sorted(curve_rows, key=lambda row: row["position"])
    if not curve_rows:
        raise ValueError(f"Missing SPC rows for kappa={kappa}")
    spc_curves[kappa] = np.asarray([row["recall_probability"] for row in curve_rows], dtype=float)
    if not position_phase:
        position_phase = [row["phase"] for row in curve_rows]

n_presented = len(position_phase)
positions = np.arange(1, n_presented + 1)

fig = plt.figure(figsize=(8.2, 7.8))
outer = fig.add_gridspec(
    4,
    1,
    height_ratios=[0.16, 0.78, 0.44, 1.12],
    hspace=0.08,
    left=0.115,
    right=0.955,
    top=0.940,
    bottom=0.165,
)

heading_a = fig.add_subplot(outer[0, 0])
heading_b = fig.add_subplot(outer[2, 0])
add_panel_heading(heading_a, "A", "Return to film after non-film sample", y=0.86)
add_panel_heading(heading_b, "B", "Recall probability by encoded position", y=0.52)

axis_a = fig.add_subplot(outer[1, 0])
axis_b = fig.add_subplot(outer[3, 0])

axis_a.plot(
    monitoring_strengths,
    recovery_values,
    color=MODERATE_MONITORING_COLOR,
    marker="o",
    linewidth=1.8,
    markersize=4.8,
)
axis_a.set_xlabel("Retrieval monitoring strength", fontsize=STRUCTURAL_FONTSIZE)
axis_a.set_ylabel("Probability next output is film", fontsize=STRUCTURAL_FONTSIZE)
axis_a.set_xlim(-0.04, 1.04)
axis_a.set_ylim(0, max(recovery_values) * 1.18)
axis_a.set_xticks(monitoring_strengths)
axis_a.set_xticklabels([f"{value:.2f}" for value in monitoring_strengths])
style_axis(axis_a)

add_phase_bands(axis_b, position_phase, fontsize=SUPPORT_FONTSIZE)
add_phase_boundaries(axis_b, position_phase)
add_reminder_marker(axis_b)
axis_b.plot(
    positions,
    spc_curves[NO_MONITORING_KAPPA],
    color=NO_MONITORING_COLOR,
    linestyle=(0, (3, 2)),
    linewidth=1.7,
    label="No retrieval monitoring",
    zorder=3,
)
axis_b.plot(
    positions,
    spc_curves[MODERATE_MONITORING_KAPPA],
    color=MODERATE_MONITORING_COLOR,
    linewidth=1.7,
    label="Retrieval monitoring",
    zorder=3,
)
axis_b.set_xlabel("Encoded position", fontsize=STRUCTURAL_FONTSIZE, labelpad=7)
axis_b.set_ylabel("Recall probability", fontsize=STRUCTURAL_FONTSIZE)
axis_b.set_xlim(1, n_presented)
axis_b.set_ylim(
    -0.025,
    max(float(np.max(curve)) for curve in spc_curves.values()) * 1.15,
)
style_axis(axis_b)
handles, labels = axis_b.get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    frameon=False,
    fontsize=SUPPORT_FONTSIZE,
    loc="lower center",
    bbox_to_anchor=(0.535, 0.035),
    ncol=2,
    handlelength=2.0,
    columnspacing=1.9,
)

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
base = FIGURE_DIR / FIGURE_STR
fig.savefig(f"{base}.png", bbox_inches="tight", dpi=600)
fig.savefig(f"{base}.svg", bbox_inches="tight")
plt.close(fig)

print(f"Saved {base}.png")
print(f"Saved {base}.svg")
