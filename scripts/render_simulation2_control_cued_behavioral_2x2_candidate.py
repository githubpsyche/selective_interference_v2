from pathlib import Path
import csv
import subprocess
from xml.sax.saxutils import escape

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"
FIGURE_STR = "simulation2_control_cued"

PHASE_TOTALS_PATH = FIGURE_DIR / f"{FIGURE_STR}_phase_totals.csv"
COST_PATH = FIGURE_DIR / f"{FIGURE_STR}_maximal_interference_cost.csv"
SUMMARY_PATH = FIGURE_DIR / f"{FIGURE_STR}_behavioral_2x2_candidate_summary.csv"
OUTPUT_SVG = FIGURE_DIR / f"{FIGURE_STR}_behavioral_2x2_candidate.svg"
OUTPUT_PNG = FIGURE_DIR / f"{FIGURE_STR}_behavioral_2x2_candidate.png"
OUTPUT_PDF = FIGURE_DIR / f"{FIGURE_STR}_behavioral_2x2_candidate.pdf"
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")

WIDTH = 1504
HEIGHT = 980
Y_MAX = 8.0

FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"
TEXT_COLOR = "#111111"
AXIS_COLOR = "#2F3A46"
GRID_COLOR = "#DCE3EA"
WEAK_FILL = "#F2F4F6"
WEAK_EDGE = "#3D4B5C"
STRONG_FILL = "#FFF0E6"
STRONG_EDGE = "#D96B2B"

TITLE_SIZE = 36
COLUMN_SIZE = 30
ROW_SIZE = 27
AXIS_LABEL_SIZE = 23
TICK_SIZE = 22
LEGEND_SIZE = 24

AXIS_STROKE = 4.0
GRID_STROKE = 2.0
BAR_STROKE = 4.0

GRID_LEFT = 420
GRID_RIGHT_X = 930
AXIS_WIDTH = 390
AXIS_HEIGHT = 260
TOP_Y = 220
BOTTOM_Y = 580
BAR_WIDTH = 140
PAIR_WIDTH = BAR_WIDTH * 2

REMINDER_ORDER = [
    ("No reminder", "No reminder"),
    ("With reminder", "Film reminder"),
]
TASK_ORDER = [
    (1.0, "Weak task encoding", WEAK_FILL, WEAK_EDGE),
    (2.0, "Strong task encoding", STRONG_FILL, STRONG_EDGE),
]
RETRIEVAL_REGIMES = [
    ("Unguided recall", "Unguided\nrecall"),
    ("Deliberate recall: start context + monitoring", "Deliberate\nrecall"),
]


def read_rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def coerce_phase_row(row):
    row = dict(row)
    row["start_drift_scale"] = float(row["start_drift_scale"])
    row["rejected_recall_drift_scale"] = float(row["rejected_recall_drift_scale"])
    row["task_mcf_scale"] = float(row["task_mcf_scale"])
    row["recall_probability_mass"] = float(row["recall_probability_mass"])
    return row


def coerce_cost_row(row):
    row = dict(row)
    row["start_drift_scale"] = float(row["start_drift_scale"])
    row["rejected_recall_drift_scale"] = float(row["rejected_recall_drift_scale"])
    return row


def lookup_phase_total(rows, start_drift_scale, kappa, reminder_condition, task_scale):
    matches = [
        row["recall_probability_mass"]
        for row in rows
        if np.isclose(row["start_drift_scale"], start_drift_scale)
        and np.isclose(row["rejected_recall_drift_scale"], kappa)
        and row["reminder_condition"] == reminder_condition
        and np.isclose(row["task_mcf_scale"], task_scale)
        and row["phase"] == "film"
    ]
    if len(matches) != 1:
        raise ValueError(
            "Expected one film total for "
            f"start={start_drift_scale}, kappa={kappa}, reminder={reminder_condition}, task={task_scale}; "
            f"found {len(matches)}."
        )
    return matches[0]


def write_summary(rows):
    fieldnames = [
        "retrieval_mode",
        "start_drift_scale",
        "rejected_recall_drift_scale",
        "reminder_condition",
        "task_encoding_strength",
        "task_mcf_scale",
        "mean_film_items_recalled",
    ]
    with SUMMARY_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def svg_text(
    x,
    y,
    content,
    size,
    weight="normal",
    anchor="middle",
    fill=TEXT_COLOR,
    extra="",
):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>'
        f"{escape(str(content))}</text>"
    )


def svg_multiline(x, y, content, size, weight="normal", anchor="middle", line_height=32):
    lines = str(content).split("\n")
    first_y = y - line_height * (len(lines) - 1) / 2
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(
            f'<tspan x="{x:.1f}" dy="{dy:.1f}">{escape(line)}</tspan>'
        )
    return (
        f'<text x="{x:.1f}" y="{first_y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" dominant-baseline="middle" fill="{TEXT_COLOR}">'
        f"{''.join(tspans)}</text>"
    )


def svg_line(x1, y1, x2, y2, color, width, extra=""):
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" {extra}/>'
    )


def svg_rect(x, y, width, height, fill, stroke, stroke_width, extra=""):
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" {extra}/>'
    )


def value_to_y(axis_y, value):
    return axis_y + AXIS_HEIGHT - (float(value) / Y_MAX) * AXIS_HEIGHT


def draw_axis(axis_x, axis_y, values, show_ylabel=False):
    parts = []
    for tick in [0, 2, 4, 6, 8]:
        y = value_to_y(axis_y, tick)
        parts.append(svg_line(axis_x, y, axis_x + AXIS_WIDTH, y, GRID_COLOR, GRID_STROKE))
        parts.append(
            svg_text(
                axis_x - 18,
                y + 8,
                str(tick),
                TICK_SIZE,
                anchor="end",
                fill=TEXT_COLOR,
            )
        )
    parts.append(svg_line(axis_x, axis_y, axis_x, axis_y + AXIS_HEIGHT, AXIS_COLOR, AXIS_STROKE))
    parts.append(svg_line(axis_x, axis_y + AXIS_HEIGHT, axis_x + AXIS_WIDTH, axis_y + AXIS_HEIGHT, AXIS_COLOR, AXIS_STROKE))

    bar_start = axis_x + (AXIS_WIDTH - PAIR_WIDTH) / 2
    for index, (_, task_label, fill, edge) in enumerate(TASK_ORDER):
        value = values[task_label]
        bar_height = axis_y + AXIS_HEIGHT - value_to_y(axis_y, value)
        parts.append(
            svg_rect(
                bar_start + index * BAR_WIDTH,
                value_to_y(axis_y, value),
                BAR_WIDTH,
                bar_height,
                fill,
                edge,
                BAR_STROKE,
            )
        )
    if show_ylabel:
        label_x = axis_x - 72
        label_y = axis_y + AXIS_HEIGHT / 2
        parts.append(
            svg_text(
                0,
                0,
                "Mean film items recalled",
                AXIS_LABEL_SIZE,
                anchor="middle",
                extra=f'transform="translate({label_x:.1f} {label_y:.1f}) rotate(-90)"',
            )
        )
    return parts


def draw_legend(grid_center):
    legend_y = 920
    patch_size = 28
    gap = 58
    first_label_width = 275
    second_label_width = 300
    total_width = patch_size + 14 + first_label_width + gap + patch_size + 14 + second_label_width
    start_x = grid_center - total_width / 2

    parts = []
    x = start_x
    for _, label, fill, edge in TASK_ORDER:
        parts.append(svg_rect(x, legend_y - patch_size + 5, patch_size, patch_size, fill, edge, BAR_STROKE))
        parts.append(svg_text(x + patch_size + 16, legend_y, label, LEGEND_SIZE, anchor="start", fill=TEXT_COLOR))
        x += patch_size + 14 + (first_label_width if "Weak" in label else second_label_width) + gap
    return parts


def build_values():
    phase_rows = [coerce_phase_row(row) for row in read_rows(PHASE_TOTALS_PATH)]
    cost_rows = [coerce_cost_row(row) for row in read_rows(COST_PATH)]
    cost_by_regime = {row["retrieval_regime"]: row for row in cost_rows}

    missing = [regime for regime, _ in RETRIEVAL_REGIMES if regime not in cost_by_regime]
    if missing:
        raise ValueError(f"Missing retrieval regimes in {COST_PATH}: {missing}")

    summary_rows = []
    values = {}
    for regime_name, row_label in RETRIEVAL_REGIMES:
        regime = cost_by_regime[regime_name]
        start_drift = regime["start_drift_scale"]
        kappa = regime["rejected_recall_drift_scale"]
        for reminder_key, reminder_label in REMINDER_ORDER:
            for task_scale, task_label, _, _ in TASK_ORDER:
                value = lookup_phase_total(phase_rows, start_drift, kappa, reminder_key, task_scale)
                values[(row_label, reminder_label, task_label)] = value
                summary_rows.append(
                    {
                        "retrieval_mode": row_label.replace("\n", " "),
                        "start_drift_scale": start_drift,
                        "rejected_recall_drift_scale": kappa,
                        "reminder_condition": reminder_label,
                        "task_encoding_strength": task_label,
                        "task_mcf_scale": task_scale,
                        "mean_film_items_recalled": value,
                    }
                )
    write_summary(summary_rows)
    return values


def render_svg(values):
    axes = {
        ("Unguided\nrecall", "No reminder"): (GRID_LEFT, TOP_Y),
        ("Unguided\nrecall", "Film reminder"): (GRID_RIGHT_X, TOP_Y),
        ("Deliberate\nrecall", "No reminder"): (GRID_LEFT, BOTTOM_Y),
        ("Deliberate\nrecall", "Film reminder"): (GRID_RIGHT_X, BOTTOM_Y),
    }
    grid_center = (GRID_LEFT + GRID_RIGHT_X + AXIS_WIDTH) / 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="white"/>',
        svg_text(grid_center, 72, "Simulated selective interference effect", TITLE_SIZE, weight="bold"),
        svg_text(GRID_LEFT + AXIS_WIDTH / 2, 164, "No reminder", COLUMN_SIZE, weight="bold"),
        svg_text(GRID_RIGHT_X + AXIS_WIDTH / 2, 164, "Film reminder", COLUMN_SIZE, weight="bold"),
        svg_multiline(180, TOP_Y + AXIS_HEIGHT / 2, "Unguided\nrecall", ROW_SIZE, weight="bold", line_height=34),
        svg_multiline(180, BOTTOM_Y + AXIS_HEIGHT / 2, "Deliberate\nrecall", ROW_SIZE, weight="bold", line_height=34),
    ]

    for (row_label, reminder_label), (axis_x, axis_y) in axes.items():
        cell_values = {
            task_label: values[(row_label, reminder_label, task_label)]
            for _, task_label, _, _ in TASK_ORDER
        }
        parts.extend(draw_axis(axis_x, axis_y, cell_values, show_ylabel=axis_x == GRID_LEFT))

    parts.extend(draw_legend(grid_center))
    parts.append("</svg>")
    OUTPUT_SVG.write_text("\n".join(parts))


def export_outputs():
    if not INKSCAPE.exists():
        raise FileNotFoundError(f"Inkscape not found at {INKSCAPE}")
    subprocess.run([str(INKSCAPE), str(OUTPUT_SVG), f"--export-filename={OUTPUT_PNG}"], check=True)
    subprocess.run([str(INKSCAPE), str(OUTPUT_SVG), f"--export-filename={OUTPUT_PDF}"], check=True)


def main():
    values = build_values()
    render_svg(values)
    export_outputs()
    print(OUTPUT_SVG)
    print(OUTPUT_PNG)
    print(OUTPUT_PDF)
    print(SUMMARY_PATH)


if __name__ == "__main__":
    main()
