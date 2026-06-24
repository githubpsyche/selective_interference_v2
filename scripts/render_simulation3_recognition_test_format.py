from __future__ import annotations

import csv
import math
import os
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures" / "exploratory"
DATA_DIR = ROOT / "figure_data" / "exploratory"
DATA_PREFIX = os.environ.get(
    "SIM3_RECOGNITION_TEST_FORMAT_DATA_PREFIX",
    "simulation3_recognition_test_format",
)
OUTPUT_PREFIX = os.environ.get(
    "SIM3_RECOGNITION_TEST_FORMAT_OUTPUT_PREFIX",
    DATA_PREFIX,
)
SUMMARY_PATH = DATA_DIR / f"{DATA_PREFIX}_recognition_summary.csv"
DIAGNOSTIC_SUMMARY_PATH = DATA_DIR / f"{DATA_PREFIX}_recognition_diagnostic_summary.csv"
OUTPUT_SVG = FIGURE_DIR / f"{OUTPUT_PREFIX}.svg"
OUTPUT_PNG = FIGURE_DIR / f"{OUTPUT_PREFIX}.png"
OUTPUT_PDF = FIGURE_DIR / f"{OUTPUT_PREFIX}.pdf"
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")
INKSCAPE_GDK_BACKEND = os.environ.get("INKSCAPE_GDK_BACKEND", "x11")

WIDTH = 1680
HEIGHT = 1320
FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"
TEXT_COLOR = "#111111"
AXIS_COLOR = "#2F3A46"
GRID_MAJOR_COLOR = "#DCE3EA"
GRID_MINOR_COLOR = "#EEF3F7"
WEAK_FILL = "#F2F4F6"
WEAK_EDGE = "#3D4B5C"
STRONG_FILL = "#FFF0E6"
STRONG_EDGE = "#D96B2B"
FILM_FILL = "#EAF2FF"
FILM_EDGE = "#1764D8"
FOIL_FILL = "#F3F4F6"
FOIL_EDGE = "#596575"
COST_FILL = "#F7F8FA"
COST_EDGE = AXIS_COLOR

PANEL_SIZE = 34
TITLE_SIZE = 34
COLUMN_SIZE = 27
AXIS_LABEL_SIZE = 23
TICK_SIZE = 21
LEGEND_SIZE = 23

AXIS_STROKE = 4.0
GRID_MAJOR_STROKE = 2.0
GRID_MINOR_STROKE = 1.2
BAR_STROKE = 4.0
HIST_STROKE = 2.0

REMINDER_ORDER = [
    ("No reminder", "Without pre-task reminder"),
    ("With reminder", "With pre-task film reminder"),
]
TASK_ORDER = [
    (1.0, "Weak task encoding", WEAK_FILL, WEAK_EDGE),
    (2.0, "Strong task encoding", STRONG_FILL, STRONG_EDGE),
]
PROBE_ORDER = [
    ("hit_probability", "Old film probes", FILM_FILL, FILM_EDGE),
    ("false_alarm_probability", "Film-like foils", FOIL_FILL, FOIL_EDGE),
]
CORRECTED_METRIC = "corrected_recognition"
HIT_METRIC = "hit_probability"
FALSE_ALARM_METRIC = "false_alarm_probability"
AUC_METRIC = "old_foil_auc"
FILM_SUPPORT_METRIC = "film_context_to_item_mass"
TASK_SUPPORT_METRIC = "task_context_to_item_mass"

PANEL_A_X = 275
PANEL_A_Y = 185
PANEL_A_W = 900
PANEL_A_H = 310
PANEL_B_X = 140
PANEL_B_Y = 760
PANEL_B_W = 650
PANEL_B_H = 330
PANEL_C_X = 1005
PANEL_C_Y = 760
PANEL_C_W = 540
PANEL_C_H = 330


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def f(value: str) -> float:
    return float(value)


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
    line_height: int = 31,
    fill: str = TEXT_COLOR,
) -> str:
    lines = str(content).split("\n")
    first_y = y - line_height * (len(lines) - 1) / 2
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{escape(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{first_y:.1f}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
        f'dominant-baseline="middle" fill="{fill}">{"".join(tspans)}</text>'
    )


def svg_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str,
    width: float,
    extra: str = "",
) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" {extra}/>'
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


def y_pos(plot_y: float, plot_h: float, y_max: float, value: float) -> float:
    return plot_y + plot_h - (float(value) / y_max) * plot_h


def y_pos_range(
    plot_y: float,
    plot_h: float,
    y_min: float,
    y_max: float,
    value: float,
) -> float:
    return plot_y + plot_h - ((float(value) - y_min) / (y_max - y_min)) * plot_h


def nice_upper(value: float, minimum: float) -> float:
    if value <= minimum:
        return minimum
    magnitude = 10 ** math.floor(math.log10(value))
    for step in [1.0, 2.0, 4.0, 5.0, 8.0, 10.0]:
        candidate = step * magnitude
        if candidate >= value:
            return candidate
    return 10.0 * magnitude


def tick_values(y_max: float, step: float) -> list[float]:
    values = []
    tick = 0.0
    while tick <= y_max + 1e-9:
        values.append(tick)
        tick += step
    return values


def format_tick(value: float) -> str:
    value = float(value)
    if abs(value) >= 10.0:
        return f"{value:.0f}"
    if abs(value) >= 1.0:
        return f"{value:.1f}".rstrip("0").rstrip(".")
    return f"{value:.2f}".rstrip("0").rstrip(".")


def draw_axes(
    x: float,
    y: float,
    w: float,
    h: float,
    y_max: float,
    ticks: list[float],
    *,
    label_every: int = 1,
) -> list[str]:
    parts = []
    for index, tick in enumerate(ticks):
        ty = y_pos(y, h, y_max, tick)
        label_tick = index % label_every == 0
        grid_color = GRID_MAJOR_COLOR if label_tick else GRID_MINOR_COLOR
        grid_stroke = GRID_MAJOR_STROKE if label_tick else GRID_MINOR_STROKE
        parts.append(svg_line(x, ty, x + w, ty, grid_color, grid_stroke))
        if label_tick:
            parts.append(svg_text(x - 18, ty + 8, format_tick(tick), TICK_SIZE, anchor="end"))
    parts.append(svg_line(x, y, x, y + h, AXIS_COLOR, AXIS_STROKE))
    parts.append(svg_line(x, y + h, x + w, y + h, AXIS_COLOR, AXIS_STROKE))
    return parts


def draw_axes_range(
    x: float,
    y: float,
    w: float,
    h: float,
    y_min: float,
    y_max: float,
    ticks: list[float],
) -> list[str]:
    parts = []
    for tick in ticks:
        ty = y_pos_range(y, h, y_min, y_max, tick)
        parts.append(svg_line(x, ty, x + w, ty, GRID_MAJOR_COLOR, GRID_MAJOR_STROKE))
        parts.append(svg_text(x - 18, ty + 8, format_tick(tick), TICK_SIZE, anchor="end"))
    parts.append(svg_line(x, y, x, y + h, AXIS_COLOR, AXIS_STROKE))
    parts.append(svg_line(x, y + h, x + w, y + h, AXIS_COLOR, AXIS_STROKE))
    return parts


def draw_ylabel(x: float, y: float, h: float, label: str) -> str:
    return svg_text(
        0,
        0,
        label,
        AXIS_LABEL_SIZE,
        extra=f'transform="translate({x - 82:.1f} {y + h / 2:.1f}) rotate(-90)"',
    )


def draw_xlabel(x: float, y: float, w: float, h: float, label: str) -> str:
    return svg_text(x + w / 2, y + h + 78, label, AXIS_LABEL_SIZE)


def metric_lookup(rows: list[dict[str, str]], metric: str) -> dict[tuple[str, float], float]:
    values = {}
    for row in rows:
        if row["metric"] == metric:
            values[(row["reminder_condition"], f(row["task_mcf_scale"]))] = f(row["value"])
    return values


def metric_ci_lookup(
    rows: list[dict[str, str]],
    metric: str,
) -> dict[tuple[str, float], tuple[float, float, float]]:
    values = {}
    for row in rows:
        if row["metric"] == metric:
            values[(row["reminder_condition"], f(row["task_mcf_scale"]))] = (
                f(row["value"]),
                f(row["ci_lower"]),
                f(row["ci_upper"]),
            )
    return values


def diagnostic_metric_lookup(
    rows: list[dict[str, str]],
    metric: str,
    *,
    diagnostic_setting: str = "sequential_update",
    probe_window: str = "all",
    probe_type: str = "all",
) -> dict[tuple[str, float], float]:
    values = {}
    for row in rows:
        if (
            row["metric"] == metric
            and row["diagnostic_setting"] == diagnostic_setting
            and row["probe_window"] == probe_window
            and row["probe_type"] == probe_type
        ):
            values[(row["reminder_condition"], f(row["task_mcf_scale"]))] = f(row["value"])
    return values


def task_support_share_lookup(
    rows: list[dict[str, str]],
) -> dict[tuple[str, float], tuple[float, float, float]]:
    film = diagnostic_metric_lookup(rows, FILM_SUPPORT_METRIC)
    task = diagnostic_metric_lookup(rows, TASK_SUPPORT_METRIC)
    values = {}
    for key, task_value in task.items():
        total = film[key] + task_value
        share = task_value / total if total > 0 else 0.0
        values[key] = (share, share, share)
    return values


def draw_panel_heading(x: float, y: float, w: float, label: str, title: str) -> list[str]:
    return [
        svg_text(x - 75, y - 68, label, PANEL_SIZE, weight="bold", anchor="start"),
        svg_text(x + w / 2, y - 68, title, TITLE_SIZE, weight="bold"),
    ]


def draw_task_legend(x: float, y: float) -> list[str]:
    patch = 28
    gap = 58
    parts = []
    start = x
    for _, label, fill, edge in TASK_ORDER:
        parts.append(svg_rect(start, y - patch + 5, patch, patch, fill, edge, BAR_STROKE))
        parts.append(svg_text(start + patch + 16, y, label, LEGEND_SIZE, anchor="start"))
        start += patch + 16 + (255 if "Weak" in label else 295) + gap
    return parts


def draw_probe_legend(x: float, y: float) -> list[str]:
    patch = 26
    gap = 48
    parts = []
    start = x
    for _, label, fill, edge in PROBE_ORDER:
        parts.append(svg_rect(start, y - patch + 5, patch, patch, fill, edge, 3.0))
        parts.append(svg_text(start + patch + 14, y, label, LEGEND_SIZE, anchor="start"))
        start += patch + 14 + (215 if label.startswith("Old") else 270) + gap
    return parts


def draw_error_bar(
    x: float,
    y: float,
    h: float,
    y_max: float,
    ci_lower: float,
    ci_upper: float,
) -> list[str]:
    low_y = y_pos(y, h, y_max, ci_lower)
    high_y = y_pos(y, h, y_max, ci_upper)
    return [
        svg_line(x, high_y, x, low_y, AXIS_COLOR, 2.2),
        svg_line(x - 9, high_y, x + 9, high_y, AXIS_COLOR, 2.2),
        svg_line(x - 9, low_y, x + 9, low_y, AXIS_COLOR, 2.2),
    ]


def draw_cost_panel(
    label: str,
    title: str,
    x: float,
    y: float,
    w: float,
    h: float,
    values: dict[tuple[str, float], tuple[float, float, float]],
    y_label: str,
    y_abs_max: float,
) -> list[str]:
    parts = draw_panel_heading(x, y, w, label, title)
    y_min = -y_abs_max
    y_max = y_abs_max
    ticks = [-y_abs_max, -y_abs_max / 2, 0.0, y_abs_max / 2, y_abs_max]
    parts.extend(draw_axes_range(x, y, w, h, y_min, y_max, ticks))
    zero_y = y_pos_range(y, h, y_min, y_max, 0.0)
    parts.append(svg_line(x, zero_y, x + w, zero_y, AXIS_COLOR, 2.4))
    parts.append(draw_ylabel(x, y, h, y_label))
    group_centers = [
        x + w * 0.28,
        x + w * 0.72,
    ]
    bar_w = 138
    compact_labels = w < 620
    for (reminder_key, reminder_label), group_center in zip(
        REMINDER_ORDER,
        group_centers,
        strict=True,
    ):
        weak, _, _ = values[(reminder_key, 1.0)]
        strong, _, _ = values[(reminder_key, 2.0)]
        value = weak - strong
        bar_x = group_center - bar_w / 2
        value_y = y_pos_range(y, h, y_min, y_max, value)
        bar_y = min(value_y, zero_y)
        parts.append(
            svg_rect(
                bar_x,
                bar_y,
                bar_w,
                abs(zero_y - value_y),
                COST_FILL,
                COST_EDGE,
                BAR_STROKE,
            )
        )
        display_label = reminder_label
        if compact_labels:
            display_label = display_label.replace(" pre-task ", " pre-task\n")
            display_label = display_label.replace(" film reminder", " film\nreminder")
        parts.append(
            svg_multiline(
                group_center,
                y + h + (58 if compact_labels else 55),
                display_label,
                19 if compact_labels else 22,
                weight="bold",
                line_height=23 if compact_labels else 25,
            )
        )
    return parts


def draw_condition_bar_panel(
    label: str,
    title: str,
    x: float,
    y: float,
    w: float,
    h: float,
    values: dict[tuple[str, float], tuple[float, float, float]],
    y_label: str,
    y_max: float,
    ticks: list[float],
    *,
    show_error_bars: bool = True,
) -> list[str]:
    parts = draw_panel_heading(x, y, w, label, title)
    parts.extend(draw_axes(x, y, w, h, y_max, ticks))
    parts.append(draw_ylabel(x, y, h, y_label))
    group_centers = [
        x + w * 0.28,
        x + w * 0.72,
    ]
    bar_w = 108 if w < 700 else 126
    gap = 28 if w < 700 else 34
    compact_labels = w < 700
    for (reminder_key, reminder_label), group_center in zip(
        REMINDER_ORDER,
        group_centers,
        strict=True,
    ):
        group_width = 2 * bar_w + gap
        start_x = group_center - group_width / 2
        for index, (task_scale, _, fill, edge) in enumerate(TASK_ORDER):
            value, ci_lower, ci_upper = values[(reminder_key, task_scale)]
            bar_x = start_x + index * (bar_w + gap)
            bar_y = y_pos(y, h, y_max, value)
            parts.append(
                svg_rect(
                    bar_x,
                    bar_y,
                    bar_w,
                    y + h - bar_y,
                    fill,
                    edge,
                    BAR_STROKE,
                )
            )
            if show_error_bars:
                parts.extend(
                    draw_error_bar(
                        bar_x + bar_w / 2,
                        y,
                        h,
                        y_max,
                        ci_lower,
                        ci_upper,
                    )
                )
        display_label = reminder_label
        if compact_labels:
            display_label = display_label.replace(" pre-task ", " pre-task\n")
            display_label = display_label.replace(" film reminder", " film\nreminder")
        parts.append(
            svg_multiline(
                group_center,
                y + h + (58 if compact_labels else 55),
                display_label,
                19 if compact_labels else 22,
                weight="bold",
                line_height=23 if compact_labels else 25,
            )
        )
    return parts


def draw_high_interference_probe_panel(
    rows: list[dict[str, str]],
    x: float,
    y: float,
    w: float,
    h: float,
) -> list[str]:
    hit_values = metric_ci_lookup(rows, HIT_METRIC)
    false_alarm_values = metric_ci_lookup(rows, FALSE_ALARM_METRIC)
    parts = draw_panel_heading(x, y, w, "C", "High-interference recognition")
    parts.extend(draw_axes(x, y, w, h, 1.0, [0.0, 0.25, 0.5, 0.75, 1.0]))
    parts.append(draw_ylabel(x, y, h, "Old response probability"))
    reminder_key = "With reminder"
    task_scale = 2.0
    bar_w = 122
    gap = 70
    start_x = x + w / 2 - bar_w - gap / 2
    for index, (metric, label_text, fill, edge) in enumerate(PROBE_ORDER):
        values = hit_values if metric == HIT_METRIC else false_alarm_values
        value, ci_lower, ci_upper = values[(reminder_key, task_scale)]
        bar_x = start_x + index * (bar_w + gap)
        bar_y = y_pos(y, h, 1.0, value)
        parts.append(
            svg_rect(
                bar_x,
                bar_y,
                bar_w,
                y + h - bar_y,
                fill,
                edge,
                BAR_STROKE,
            )
        )
        parts.extend(
            draw_error_bar(
                bar_x + bar_w / 2,
                y,
                h,
                1.0,
                ci_lower,
                ci_upper,
            )
        )
        display_label = label_text
        if label_text == "Old film probes":
            display_label = "Old film\nprobes"
        elif label_text == "Film-like foils":
            display_label = "Film-like\nfoils"
        parts.append(
            svg_multiline(
                bar_x + bar_w / 2,
                y + h + 57,
                display_label,
                21,
                weight="bold",
                line_height=24,
            )
        )
    parts.append(svg_text(x + w / 2, y + h + 128, "With reminder + strong task encoding", 23, weight="bold"))
    return parts


def render_svg() -> None:
    summary_rows = read_rows(SUMMARY_PATH)
    diagnostic_rows = read_rows(DIAGNOSTIC_SUMMARY_PATH)
    task_support_share = task_support_share_lookup(diagnostic_rows)
    corrected = metric_ci_lookup(summary_rows, CORRECTED_METRIC)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    parts.extend(
        draw_condition_bar_panel(
            "A",
            "Task competitors cued by context",
            PANEL_A_X,
            PANEL_A_Y,
            PANEL_A_W,
            PANEL_A_H,
            task_support_share,
            "Task share of candidate support",
            0.55,
            [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            show_error_bars=False,
        )
    )
    parts.extend(
        draw_condition_bar_panel(
            "B",
            "Corrected recognition",
            PANEL_B_X,
            PANEL_B_Y,
            PANEL_B_W,
            PANEL_B_H,
            corrected,
            "Hits minus false alarms",
            0.5,
            [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
        )
    )
    parts.extend(
        draw_high_interference_probe_panel(
            summary_rows,
            PANEL_C_X,
            PANEL_C_Y,
            PANEL_C_W,
            PANEL_C_H,
        )
    )
    parts.extend(draw_task_legend(520, 1265))
    parts.append("</svg>")
    OUTPUT_SVG.write_text("\n".join(parts))


def export_outputs() -> None:
    if not INKSCAPE.exists():
        raise FileNotFoundError(f"Inkscape not found at {INKSCAPE}")
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", INKSCAPE_GDK_BACKEND)
    subprocess.run(
        [str(INKSCAPE), str(OUTPUT_SVG), f"--export-filename={OUTPUT_PNG}"],
        check=True,
        env=env,
    )
    subprocess.run(
        [str(INKSCAPE), str(OUTPUT_SVG), f"--export-filename={OUTPUT_PDF}"],
        check=True,
        env=env,
    )


def main() -> None:
    render_svg()
    export_outputs()
    print(OUTPUT_SVG)
    print(OUTPUT_PNG)
    print(OUTPUT_PDF)


if __name__ == "__main__":
    main()
