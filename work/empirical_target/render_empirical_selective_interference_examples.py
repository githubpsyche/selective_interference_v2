from __future__ import annotations

import csv
import subprocess
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = Path(__file__).resolve().parent
OUT_DIR = WORK_DIR
DATA_DIR = WORK_DIR
CAPTION_EXPORT_DIR = ROOT / "work" / "captioned_exports"
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")

OUTPUT_BASE = OUT_DIR / "empirical_selective_interference_examples"
OUTPUT_DATA_BASE = DATA_DIR / "empirical_selective_interference_examples"
OUTPUT_SVG = OUTPUT_BASE.with_suffix(".svg")
OUTPUT_PNG = OUTPUT_BASE.with_suffix(".png")
OUTPUT_PDF = OUTPUT_BASE.with_suffix(".pdf")
OUTPUT_CSV = OUTPUT_DATA_BASE.with_suffix(".csv")
OUTPUT_CAPTION_BASE = CAPTION_EXPORT_DIR / "empirical_selective_interference_examples_with_caption"

WIDTH = 1504
HEIGHT = 1220

FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"
TEXT = "#111111"
AXIS = "#3D4B5C"
GRID = "#D8DEE6"
CONTROL_FILL = "#F2F4F6"
CONTROL_EDGE = "#3D4B5C"
TETRIS_FILL = "#FFF0E6"
TETRIS_EDGE = "#D96B2B"

TITLE_SIZE = 34
COLUMN_SIZE = 27
STUDY_SIZE = 23
STUDY_DETAIL_SIZE = 18
PANEL_TITLE_SIZE = 20
AXIS_LABEL_SIZE = 18
TICK_SIZE = 17
SUBLABEL_SIZE = 17
LEGEND_SIZE = 21

AXIS_STROKE = 3.2
GRID_STROKE = 1.8
BAR_STROKE = 3.2


ROWS = [
    {
        "study": "James et al. 2015, Exp. 2",
        "study_label": "James et al. 2015\nExp. 2",
        "detail": "24-hr reminder x Tetris; diary + verbal recognition",
        "left": {
            "title": "Diary intrusions",
            "ylabel": "Film intrusions",
            "ymax": 6,
            "ticks": [0, 3, 6],
            "groups": [
                ("No pre-task\nreminder", 5.11, 3.89),
                ("After pre-task\nfilm reminder", 4.83, 1.89),
            ],
        },
        "right": {
            "title": "Verbal recognition",
            "ylabel": "Film recognition hits",
            "ymax": 32,
            "ticks": [0, 16, 32],
            "groups": [
                ("No pre-task\nreminder", 19.78, 18.83),
                ("After pre-task\nfilm reminder", 18.89, 18.33),
            ],
            "ns": True,
        },
    },
    {
        "study": "Lau-Zhu et al. 2019, Exp. 1",
        "study_label": "Lau-Zhu et al. 2019\nExp. 1",
        "detail": "30-min reminder; diary + voluntary free recall",
        "left": {
            "title": "Diary intrusions",
            "ylabel": "Film intrusions",
            "ymax": 6,
            "ticks": [0, 3, 6],
            "groups": [("After pre-task\nfilm reminder", 5.61, 2.70)],
        },
        "right": {
            "title": "Voluntary free recall",
            "ylabel": "Film details recalled",
            "ymax": 80,
            "ticks": [0, 40, 80],
            "groups": [("After pre-task\nfilm reminder", 59.35, 65.82)],
            "ns": True,
        },
    },
    {
        "study": "Lau-Zhu et al. 2021",
        "study_label": "Lau-Zhu et al. 2021",
        "detail": "30-min reminder; trauma-film-cued VIT + recognition",
        "left": {
            "title": "VIT intrusions",
            "ylabel": "Film-cued intrusions",
            "ymax": 20,
            "ticks": [0, 10, 20],
            "groups": [("After pre-task\nfilm reminder", 17.94, 7.56)],
        },
        "right": {
            "title": "Cued recognition",
            "ylabel": "Film-cued recognition accuracy",
            "ymax": 1.0,
            "ticks": [0, 0.5, 1.0],
            "groups": [("After pre-task\nfilm reminder", 0.51, 0.41)],
            "ns": True,
        },
    },
]


def text(
    x: float,
    y: float,
    content: str,
    size: int,
    weight: str = "normal",
    anchor: str = "middle",
    fill: str = TEXT,
    extra: str = "",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>'
        f"{escape(content)}</text>"
    )


def multiline(
    x: float,
    y: float,
    content: str,
    size: int,
    weight: str = "normal",
    anchor: str = "middle",
    line_height: float = 24,
    fill: str = TEXT,
) -> str:
    lines = content.split("\n")
    start_y = y - (len(lines) - 1) * line_height / 2
    spans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        spans.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{escape(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{start_y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">'
        f"{''.join(spans)}</text>"
    )


def line(x1: float, y1: float, x2: float, y2: float, stroke: str, width: float, extra: str = "") -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{width}" {extra}/>'
    )


def rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    stroke: str,
    stroke_width: float,
    rx: float = 0,
) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def y_pos(axis_y: float, axis_h: float, value: float, ymax: float) -> float:
    return axis_y + axis_h - (value / ymax) * axis_h


def tick_label(value: float) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"{value:.1f}"
    return str(int(value))


def draw_axis(
    x: float,
    y: float,
    w: float,
    h: float,
    spec: dict,
    show_ylabel: bool,
) -> list[str]:
    parts: list[str] = []
    groups = spec["groups"]
    ymax = spec["ymax"]
    ticks = spec["ticks"]

    parts.append(text(x + w / 2, y - 30, spec["title"], PANEL_TITLE_SIZE, weight="bold"))

    for tick in ticks:
        ty = y_pos(y, h, tick, ymax)
        parts.append(line(x, ty, x + w, ty, GRID, GRID_STROKE))
        parts.append(text(x - 12, ty + 6, tick_label(tick), TICK_SIZE, anchor="end"))
    parts.append(line(x, y, x, y + h, AXIS, AXIS_STROKE))
    parts.append(line(x, y + h, x + w, y + h, AXIS, AXIS_STROKE))

    group_count = len(groups)
    group_gap = 34 if group_count > 1 else 0
    total_bar_area = w - group_gap * (group_count - 1)
    group_w = total_bar_area / group_count
    bar_w = min(58, group_w / 2)
    group_inner = bar_w * 2

    for index, (group_label, control_value, tetris_value) in enumerate(groups):
        gx = x + index * (group_w + group_gap) + (group_w - group_inner) / 2
        for bar_index, (value, fill, edge) in enumerate(
            [
                (control_value, CONTROL_FILL, CONTROL_EDGE),
                (tetris_value, TETRIS_FILL, TETRIS_EDGE),
            ]
        ):
            by = y_pos(y, h, value, ymax)
            parts.append(rect(gx + bar_index * bar_w, by, bar_w, y + h - by, fill, edge, BAR_STROKE, rx=1.5))

        parts.append(multiline(gx + group_inner / 2, y + h + 41, group_label, SUBLABEL_SIZE, fill=AXIS, line_height=20))

    if spec.get("ns"):
        parts.append(text(x + w / 2, y + 20, "n.s.", SUBLABEL_SIZE, weight="bold", fill=AXIS))

    if show_ylabel:
        label_x = x - 50
        label_y = y + h / 2
        parts.append(
            text(
                0,
                0,
                spec["ylabel"],
                AXIS_LABEL_SIZE,
                anchor="middle",
                extra=f'transform="translate({label_x:.1f} {label_y:.1f}) rotate(-90)"',
            )
        )

    return parts


def write_data_csv() -> None:
    rows = []
    for row in ROWS:
        for side_key, outcome_family in [("left", "intrusion_like"), ("right", "deliberate_memory")]:
            spec = row[side_key]
            for group_label, control_value, tetris_value in spec["groups"]:
                rows.append(
                    {
                        "study": row["study"],
                        "outcome_family": outcome_family,
                        "outcome": spec["title"],
                        "group": group_label,
                        "condition": "Comparison/rest",
                        "mean": control_value,
                    }
                )
                rows.append(
                    {
                        "study": row["study"],
                        "outcome_family": outcome_family,
                        "outcome": spec["title"],
                        "group": group_label,
                        "condition": "Tetris interference",
                        "mean": tetris_value,
                    }
                )
    with OUTPUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def build_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">',
        f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
        text(WIDTH / 2, 56, "Empirical examples of selective interference", TITLE_SIZE, weight="bold"),
        text(542, 126, "Intrusion-like access", COLUMN_SIZE, weight="bold"),
        text(1058, 126, "Deliberate memory", COLUMN_SIZE, weight="bold"),
        line(292, 150, 292, 1012, GRID, 2.4),
        line(800, 150, 800, 1012, GRID, 2.4),
        line(1316, 150, 1316, 1012, GRID, 2.4),
    ]

    row_tops = [205, 515, 825]
    axis_h = 170
    axis_w = 374
    left_x = 372
    right_x = 888
    for index, (row, top) in enumerate(zip(ROWS, row_tops)):
        if index:
            parts.append(line(58, top - 70, 1448, top - 70, GRID, 2.0))
        study_text = row.get("study_label", row["study"])
        detail_text = row["detail"]
        parts.append(multiline(164, top + 60, study_text, STUDY_SIZE, weight="bold", line_height=27))
        parts.append(multiline(164, top + 112, textwrap.fill(detail_text, width=26), STUDY_DETAIL_SIZE, fill=AXIS, line_height=23))

        parts.extend(draw_axis(left_x, top, axis_w, axis_h, row["left"], show_ylabel=True))
        parts.extend(draw_axis(right_x, top, axis_w, axis_h, row["right"], show_ylabel=True))

    legend_y = 1122
    legend_center = WIDTH / 2
    patch = 30
    first_x = legend_center - 294
    parts.append(rect(first_x, legend_y - 24, patch, patch, CONTROL_FILL, CONTROL_EDGE, BAR_STROKE, rx=2))
    parts.append(text(first_x + 44, legend_y, "Comparison / rest", LEGEND_SIZE, weight="bold", anchor="start", fill=AXIS))
    second_x = legend_center + 40
    parts.append(rect(second_x, legend_y - 24, patch, patch, TETRIS_FILL, TETRIS_EDGE, BAR_STROKE, rx=2))
    parts.append(text(second_x + 44, legend_y, "Tetris interference", LEGEND_SIZE, weight="bold", anchor="start", fill=AXIS))
    parts.append(
        text(
            WIDTH / 2,
            1172,
            "Bars plot published condition means in native units; y-axis scales differ across outcomes.",
            SUBLABEL_SIZE,
            fill=AXIS,
        )
    )
    parts.append("</svg>")
    return "\n".join(parts)


def export_svg() -> None:
    OUTPUT_SVG.write_text(build_svg())
    if not INKSCAPE.exists():
        raise FileNotFoundError(f"Inkscape not found at {INKSCAPE}")
    subprocess.run(
        [str(INKSCAPE), str(OUTPUT_SVG), "--export-type=png", f"--export-filename={OUTPUT_PNG}", "--export-dpi=300"],
        check=True,
    )
    subprocess.run(
        [str(INKSCAPE), str(OUTPUT_SVG), "--export-type=pdf", f"--export-filename={OUTPUT_PDF}"],
        check=True,
    )


def save_caption_composite() -> None:
    image = plt.imread(str(OUTPUT_PNG))
    fig_width = 10.8
    image_aspect = image.shape[0] / image.shape[1]
    image_height = fig_width * image_aspect
    title = "Empirical examples of selective interference."
    body = (
        "Rows show exemplar trauma-film studies selected to span core methodological variants in the review table: "
        "a delayed reminder-by-Tetris design, a voluntary free-recall test, and a laboratory vigilance-intrusion task with "
        "trauma-film cues. "
            "Gray bars show comparison or rest conditions, and orange bars show Tetris interference. "
        "Bars reproduce published condition means in native study units, not model output; y-axis scales differ across outcomes."
    )
    body_lines = textwrap.wrap(body, width=142)
    caption_height = 0.55 + 0.22 * max(1, len(body_lines))
    fig = plt.figure(figsize=(fig_width, image_height + caption_height))
    image_bottom = caption_height / (image_height + caption_height)
    axis = fig.add_axes([0, image_bottom, 1, 1 - image_bottom])
    axis.imshow(image)
    axis.axis("off")
    y = image_bottom - 0.08
    fig.text(0.02, y, title, fontsize=13, fontweight="bold", ha="left", va="top")
    y -= 0.045
    for line_text in body_lines:
        fig.text(0.02, y, line_text, fontsize=10.5, ha="left", va="top")
        y -= 0.030
    fig.savefig(f"{OUTPUT_CAPTION_BASE}.png", bbox_inches="tight", dpi=600)
    fig.savefig(f"{OUTPUT_CAPTION_BASE}.svg", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CAPTION_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    write_data_csv()
    export_svg()
    save_caption_composite()
    print(OUTPUT_SVG)
    print(OUTPUT_PNG)
    print(OUTPUT_PDF)
    print(OUTPUT_CSV)
    print(f"{OUTPUT_CAPTION_BASE}.png")


if __name__ == "__main__":
    main()
