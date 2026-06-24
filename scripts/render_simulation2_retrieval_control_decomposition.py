from __future__ import annotations

import csv
import math
import os
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures" / "manuscript" / "simulation2"
DATA_PREFIX = os.environ.get(
    "SIM2_RETRIEVAL_CONTROL_DECOMP_DATA_PREFIX",
    "simulation2_retrieval_control_decomposition",
)
OUTPUT_PREFIX = os.environ.get(
    "SIM2_RETRIEVAL_CONTROL_DECOMP_OUTPUT_PREFIX",
    "simulation2_retrieval_control_decomposition",
)
PHASE_TOTALS_PATH = FIGURE_DIR / f"{DATA_PREFIX}_phase_totals.csv"
SUMMARY_PATH = FIGURE_DIR / f"{OUTPUT_PREFIX}_summary.csv"
OUTPUT_SVG = FIGURE_DIR / f"{OUTPUT_PREFIX}.svg"
OUTPUT_PNG = FIGURE_DIR / f"{OUTPUT_PREFIX}.png"
OUTPUT_PDF = FIGURE_DIR / f"{OUTPUT_PREFIX}.pdf"
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")

WIDTH = 1700
HEIGHT = 760
FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"
TEXT_COLOR = "#111111"
AXIS_COLOR = "#2F3A46"
GRID_MINOR_COLOR = "#EEF3F7"
GRID_MAJOR_COLOR = "#DCE3EA"
LOW_FILL = "#F2F4F6"
LOW_EDGE = "#3D4B5C"
HIGH_FILL = "#FFF0E6"
HIGH_EDGE = "#D96B2B"

PANEL_LETTER_SIZE = 34
TITLE_SIZE = 36
STRUCTURAL_SIZE = 22
AXIS_LABEL_SIZE = 24
TICK_SIZE = 22
LEGEND_SIZE = 24
GROUP_SIZE = 24
PACKAGE_SIZE = 23

AXIS_STROKE = 4.0
GRID_MINOR_STROKE = 1.2
GRID_MAJOR_STROKE = 2.0
BAR_STROKE = 4.0

PLOT_X = 250
PLOT_W = 1330
PLOT_A_Y = 165
PLOT_A_H = 310
Y_MAX_A = 8.0

STEP = 145
GROUP_GAP = 115
FIRST_CENTER = PLOT_X + 75
PAIR_BAR_W = 46

ENDPOINTS = [
    ("No reminder + weak task encoding", "Low endpoint", LOW_FILL, LOW_EDGE),
    ("Film reminder + strong task encoding", "High endpoint", HIGH_FILL, HIGH_EDGE),
]

DISPLAY_LABELS = {
    1: "No deliberate\ncontrol",
    2: "Retrieval\nmonitoring",
    3: "Start-of-\nfilm\nreinstatement",
    4: "Reinstatement\n+\nmonitoring",
    5: "Film-\nretrieval\ngoal",
    6: "Goal\n+\nmonitoring",
    7: "Goal\n+\nreinstatement",
    8: "Full\ncontrol",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def coerce_bool(value: str) -> bool:
    return str(value).strip().lower() == "true"


def coerce_row(row: dict[str, str]) -> dict:
    row = dict(row)
    for key in [
        "package_index",
        "start_drift_scale",
        "film_item_support_boost",
        "rejected_recall_drift_scale",
        "task_mcf_scale",
        "film_source_start_drift_rate",
        "film_cue_reinstatement",
        "experiment_count",
        "recall_probability_mass",
    ]:
        row[key] = float(row[key])
    for key in [
        "film_goal_included",
        "start_reinstatement_included",
        "target_monitoring_included",
    ]:
        row[key] = coerce_bool(row[key])
    return row


def display_label(row: dict) -> str:
    package_index = int(row["package_index"])
    try:
        return DISPLAY_LABELS[package_index]
    except KeyError as error:
        raise ValueError(f"Missing display label for package {package_index}.") from error


def write_summary(rows: list[dict]) -> None:
    fieldnames = [
        "package_index",
        "retrieval_control_package",
        "goal_group",
        "within_group_label",
        "display_label",
        "film_goal_included",
        "start_reinstatement_included",
        "target_monitoring_included",
        "start_drift_scale",
        "film_item_support_boost",
        "rejected_recall_drift_scale",
        "low_endpoint_film_recall",
        "high_endpoint_film_recall",
        "film_items_reduced",
    ]
    with SUMMARY_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def svg_text(
    x: float,
    y: float,
    content: str,
    size: int,
    weight: str = "normal",
    anchor: str = "middle",
    fill: str = TEXT_COLOR,
    extra: str = "",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>'
        f"{escape(str(content))}</text>"
    )


def svg_multiline(
    x: float,
    y: float,
    content: str,
    size: int,
    weight: str = "normal",
    anchor: str = "middle",
    line_height: int = 24,
) -> str:
    lines = str(content).split("\n")
    first_y = y - line_height * (len(lines) - 1) / 2
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{escape(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{first_y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" dominant-baseline="middle" fill="{TEXT_COLOR}">'
        f"{''.join(tspans)}</text>"
    )


def svg_line(x1: float, y1: float, x2: float, y2: float, color: str, width: float) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}"/>'
    )


def svg_rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    stroke: str,
    stroke_width: float,
) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def centers() -> list[float]:
    first_group = [FIRST_CENTER + index * STEP for index in range(4)]
    second_start = FIRST_CENTER + 4 * STEP + GROUP_GAP
    second_group = [second_start + index * STEP for index in range(4)]
    return first_group + second_group


def y_pos(plot_y: float, plot_h: float, y_max: float, value: float) -> float:
    return plot_y + plot_h - (float(value) / y_max) * plot_h


def draw_grid(plot_y: float, plot_h: float, y_max: float, label_every: int = 2) -> list[str]:
    parts = []
    for tick in range(0, int(y_max) + 1):
        y = y_pos(plot_y, plot_h, y_max, tick)
        is_major = tick % label_every == 0
        parts.append(
            svg_line(
                PLOT_X,
                y,
                PLOT_X + PLOT_W,
                y,
                GRID_MAJOR_COLOR if is_major else GRID_MINOR_COLOR,
                GRID_MAJOR_STROKE if is_major else GRID_MINOR_STROKE,
            )
        )
        if is_major:
            parts.append(svg_text(PLOT_X - 18, y + 7, str(tick), TICK_SIZE, anchor="end"))
    parts.append(svg_line(PLOT_X, plot_y, PLOT_X, plot_y + plot_h, AXIS_COLOR, AXIS_STROKE))
    parts.append(
        svg_line(
            PLOT_X,
            plot_y + plot_h,
            PLOT_X + PLOT_W,
            plot_y + plot_h,
            AXIS_COLOR,
            AXIS_STROKE,
        )
    )
    return parts


def draw_ylabel(plot_y: float, plot_h: float, label: str) -> str:
    return svg_text(
        0,
        0,
        label,
        AXIS_LABEL_SIZE,
        extra=f'transform="translate({PLOT_X - 78:.1f} {plot_y + plot_h / 2:.1f}) rotate(-90)"',
    )


def group_bounds(center_values: list[float]) -> list[tuple[float, float, float]]:
    first = center_values[:4]
    second = center_values[4:]
    pad = STEP * 0.45
    return [
        (first[0] - pad, first[-1] + pad, (first[0] + first[-1]) / 2),
        (second[0] - pad, second[-1] + pad, (second[0] + second[-1]) / 2),
    ]


def build_summary() -> list[dict]:
    rows = [coerce_row(row) for row in read_rows(PHASE_TOTALS_PATH)]
    film_rows = [row for row in rows if row["phase"] == "film"]
    summary = []
    package_indices = sorted({int(row["package_index"]) for row in film_rows})
    for package_index in package_indices:
        package_rows = [row for row in film_rows if int(row["package_index"]) == package_index]
        low_rows = [
            row
            for row in package_rows
            if row["endpoint"] == "No reminder + weak task encoding"
        ]
        high_rows = [
            row
            for row in package_rows
            if row["endpoint"] == "Film reminder + strong task encoding"
        ]
        if len(low_rows) != 1 or len(high_rows) != 1:
            raise ValueError(f"Expected one low and one high endpoint for package {package_index}.")
        low = low_rows[0]
        high = high_rows[0]
        summary.append(
            {
                "package_index": package_index,
                "retrieval_control_package": low["retrieval_control_package"],
                "goal_group": low["goal_group"],
                "within_group_label": low["within_group_label"],
                "display_label": display_label(low),
                "film_goal_included": low["film_goal_included"],
                "start_reinstatement_included": low["start_reinstatement_included"],
                "target_monitoring_included": low["target_monitoring_included"],
                "start_drift_scale": low["start_drift_scale"],
                "film_item_support_boost": low["film_item_support_boost"],
                "rejected_recall_drift_scale": low["rejected_recall_drift_scale"],
                "low_endpoint_film_recall": low["recall_probability_mass"],
                "high_endpoint_film_recall": high["recall_probability_mass"],
                "film_items_reduced": low["recall_probability_mass"] - high["recall_probability_mass"],
            }
        )
    write_summary(summary)
    return summary


def draw_panel_a(summary: list[dict], center_values: list[float]) -> list[str]:
    parts = [
        svg_text(42, 78, "A", PANEL_LETTER_SIZE, weight="bold", anchor="start"),
        svg_text(PLOT_X + PLOT_W / 2, 78, "Endpoint film recall by control setting", TITLE_SIZE, weight="bold"),
    ]
    legend_y = 126
    legend_center = PLOT_X + PLOT_W / 2
    patch = 26
    entry_xs = [legend_center - 475, legend_center + 135]
    for (endpoint, _, fill, edge), x in zip(ENDPOINTS, entry_xs, strict=True):
        parts.append(svg_rect(x, legend_y - patch + 6, patch, patch, fill, edge, BAR_STROKE))
        parts.append(svg_text(x + patch + 14, legend_y, endpoint, LEGEND_SIZE, anchor="start"))
    parts.extend(draw_grid(PLOT_A_Y, PLOT_A_H, Y_MAX_A))
    parts.append(draw_ylabel(PLOT_A_Y, PLOT_A_H, "Mean film items recalled"))
    for row, center_x in zip(summary, center_values, strict=True):
        values = [
            (row["low_endpoint_film_recall"], LOW_FILL, LOW_EDGE),
            (row["high_endpoint_film_recall"], HIGH_FILL, HIGH_EDGE),
        ]
        start_x = center_x - PAIR_BAR_W
        for index, (value, fill, edge) in enumerate(values):
            bar_y = y_pos(PLOT_A_Y, PLOT_A_H, Y_MAX_A, value)
            parts.append(
                svg_rect(
                    start_x + index * PAIR_BAR_W,
                    bar_y,
                    PAIR_BAR_W,
                    PLOT_A_Y + PLOT_A_H - bar_y,
                    fill,
                    edge,
                    BAR_STROKE,
                )
            )
    label_y = PLOT_A_Y + PLOT_A_H + 55
    for row, center_x in zip(summary, center_values, strict=True):
        parts.append(
            svg_multiline(
                center_x,
                label_y,
                row.get("display_label", row["within_group_label"]),
                PACKAGE_SIZE,
                line_height=22,
            )
        )
    bounds = group_bounds(center_values)
    group_y = PLOT_A_Y + PLOT_A_H + 150
    for (left, right, center), label in zip(
        bounds,
        ["Film-retrieval goal absent", "Film-retrieval goal present"],
        strict=True,
    ):
        parts.append(svg_line(left, group_y - 20, right, group_y - 20, AXIS_COLOR, 2.2))
        parts.append(svg_text(center, group_y + 6, label, GROUP_SIZE, weight="bold"))
    return parts


def render_svg() -> None:
    summary = build_summary()
    center_values = centers()
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    parts.extend(draw_panel_a(summary, center_values))
    parts.append("</svg>")
    OUTPUT_SVG.write_text("\n".join(parts))


def export_outputs() -> None:
    if not INKSCAPE.exists():
        raise FileNotFoundError(f"Inkscape not found at {INKSCAPE}")
    subprocess.run(
        [str(INKSCAPE), str(OUTPUT_SVG), f"--export-filename={OUTPUT_PNG}"],
        check=True,
    )
    subprocess.run(
        [str(INKSCAPE), str(OUTPUT_SVG), f"--export-filename={OUTPUT_PDF}"],
        check=True,
    )


def main() -> None:
    render_svg()
    export_outputs()
    print(OUTPUT_SVG)
    print(OUTPUT_PNG)
    print(OUTPUT_PDF)
    print(SUMMARY_PATH)


if __name__ == "__main__":
    main()
