from __future__ import annotations

import os
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")
INKSCAPE_GDK_BACKEND = os.environ.get("INKSCAPE_GDK_BACKEND", "x11")

WIDTH = 1800
HEIGHT = 840
FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"

TEXT = "#111111"
AXIS = "#2F3A46"
GRID = "#DCE3EA"
CONTEXT_FILL = "#EEF3F8"
NEUTRAL_FILL = "#F2F4F6"
FILM_FILL = "#EAF2FF"
FILM_EDGE = "#1764D8"
FOIL_FILL = "#F3F4F6"
FOIL_EDGE = "#596575"
TASK_FILL = "#FFF0E6"
TASK_EDGE = "#D96B2B"
GREEN = "#168A4A"
RED = "#B13A3A"

STROKE = 3.0
THIN = 2.0
PANEL_SIZE = 36
TITLE_SIZE = 30
LABEL_SIZE = 21
SMALL_SIZE = 17


def text(
    x: float,
    y: float,
    value: str,
    size: int,
    weight: str = "normal",
    anchor: str = "middle",
    fill: str = TEXT,
    extra: str = "",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>'
        f"{escape(value)}</text>"
    )


def multiline(
    x: float,
    y: float,
    value: str,
    size: int,
    weight: str = "normal",
    anchor: str = "middle",
    line_height: float = 23,
    fill: str = TEXT,
) -> str:
    lines = value.split("\n")
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


def defs() -> str:
    return (
        "<defs>"
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{AXIS}"/>'
        "</marker>"
        '<marker id="green-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{GREEN}"/>'
        "</marker>"
        '<marker id="red-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{RED}"/>'
        "</marker>"
        "</defs>"
    )


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str,
    width: float = STROKE,
    marker: str = "arrow",
    extra: str = "",
) -> str:
    marker_attr = f'marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width:.1f}" stroke-linecap="round" '
        f'{marker_attr} {extra}/>'
    )


def path(d: str, color: str, width: float = STROKE, marker: str = "arrow") -> str:
    marker_attr = f'marker-end="url(#{marker})"' if marker else ""
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width:.1f}" '
        f'stroke-linecap="round" stroke-linejoin="round" {marker_attr}/>'
    )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    edge: str,
    stroke: float = STROKE,
    rx: float = 12,
) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" '
        f'fill="{fill}" stroke="{edge}" stroke-width="{stroke:.1f}"/>'
    )


def circle(cx: float, cy: float, r: float, fill: str, edge: str, stroke: float = STROKE) -> str:
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
        f'fill="{fill}" stroke="{edge}" stroke-width="{stroke:.1f}"/>'
    )


def panel_title(x: float, y: float, label: str, title: str) -> list[str]:
    return [
        text(x, y, label, PANEL_SIZE, weight="bold", anchor="start"),
        text(x + 62, y + 2, title, TITLE_SIZE, weight="bold", anchor="start"),
    ]


def item(cx: float, cy: float, label: str, fill: str, edge: str, r: float = 39) -> list[str]:
    return [
        circle(cx, cy, r, fill, edge),
        multiline(cx, cy + 7, label, LABEL_SIZE, weight="bold", line_height=21),
    ]


def context(cx: float, cy: float, label: str, r: float = 38, edge: str = AXIS) -> list[str]:
    return [
        circle(cx, cy, r, CONTEXT_FILL, edge),
        text(cx, cy + 8, label, LABEL_SIZE, weight="bold"),
    ]


def box(
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    fill: str = NEUTRAL_FILL,
    edge: str = AXIS,
) -> list[str]:
    return [
        rect(x, y, w, h, fill, edge, STROKE, rx=13),
        multiline(x + w / 2, y + h / 2 + 7, label, LABEL_SIZE, weight="bold", line_height=23),
    ]


def draw_route_panel() -> list[str]:
    parts: list[str] = []
    parts.extend(panel_title(36, 62, "A", "Item-context retrieval routes"))
    parts.append(text(385, 104, "The same learned associations can be read in either direction", SMALL_SIZE))

    top_contexts = [(110, 185, "C1"), (260, 185, "C2"), (410, 185, "C3"), (560, 185, "C4")]
    top_items = [
        (110, 325, "Film", FILM_FILL, FILM_EDGE),
        (260, 325, "Film", FILM_FILL, FILM_EDGE),
        (410, 325, "Film", FILM_FILL, FILM_EDGE),
        (560, 325, "Task", TASK_FILL, TASK_EDGE),
    ]
    bottom_contexts = [(110, 540, "C1"), (260, 540, "C2"), (410, 540, "C3"), (560, 540, "C4")]
    bottom_items = [
        (110, 680, "Film", FILM_FILL, FILM_EDGE),
        (260, 680, "Film", FILM_FILL, FILM_EDGE),
        (410, 680, "Film", FILM_FILL, FILM_EDGE),
        (560, 680, "Task", TASK_FILL, TASK_EDGE),
    ]

    parts.append(text(400, 140, "Item-to-context route", LABEL_SIZE, weight="bold", fill=GREEN))
    for x, y, label in top_contexts:
        parts.extend(context(x, y, label))
    for x, y, label, fill, edge in top_items:
        parts.extend(item(x, y, label, fill, edge, r=43 if x == 260 else 39))
    parts.append(path("M 233 292 L 132 214", GREEN, marker="green-arrow"))
    parts.append(path("M 260 280 L 260 224", GREEN, marker="green-arrow"))
    parts.append(path("M 287 292 L 385 214", GREEN, marker="green-arrow"))
    parts.append(path("M 299 306 L 528 211", GREEN, marker="green-arrow"))
    parts.append(
        multiline(
            645,
            252,
            "Presented item\nreinstates context",
            SMALL_SIZE,
            weight="bold",
            anchor="start",
            line_height=21,
            fill=GREEN,
        )
    )

    parts.append(line(70, 420, 730, 420, GRID, THIN, marker=""))

    parts.append(text(400, 495, "Context-to-item route", LABEL_SIZE, weight="bold", fill=RED))
    for x, y, label in bottom_contexts:
        parts.extend(context(x, y, label, r=43 if x == 410 else 38, edge=RED if x == 410 else AXIS))
    for x, y, label, fill, edge in bottom_items:
        parts.extend(item(x, y, label, fill, edge))
    parts.append(path("M 383 570 L 132 653", RED, marker="red-arrow"))
    parts.append(path("M 394 576 L 282 648", RED, marker="red-arrow"))
    parts.append(path("M 410 584 L 410 637", RED, marker="red-arrow"))
    parts.append(path("M 437 570 L 538 650", RED, marker="red-arrow"))
    parts.append(
        multiline(
            645,
            608,
            "Current context\ncues competitors",
            SMALL_SIZE,
            weight="bold",
            anchor="start",
            line_height=21,
            fill=RED,
        )
    )
    return parts


def draw_recognition_panel() -> list[str]:
    parts: list[str] = []
    parts.extend(panel_title(850, 62, "B", "Supplied-probe recognition decision"))
    parts.append(text(1300, 104, "The probe reinstates context; old/new evidence depends on the context match", SMALL_SIZE))

    parts.extend(item(975, 292, "Presented\nprobe", NEUTRAL_FILL, AXIS, r=48))
    parts.append(text(975, 198, "Old film item or film-like foil", SMALL_SIZE, weight="bold"))
    parts.append(line(1040, 292, 1155, 292, GREEN, marker="green-arrow"))
    parts.append(text(1100, 267, "item->context", SMALL_SIZE, weight="bold", fill=GREEN))

    parts.extend(box(1155, 235, 245, 114, "Probe-\nreinstated context", CONTEXT_FILL, AXIS))
    parts.extend(box(1155, 488, 245, 104, "Current\ntest context", CONTEXT_FILL, AXIS))

    parts.append(line(1416, 292, 1570, 365, AXIS))
    parts.append(line(1416, 540, 1570, 392, AXIS))
    parts.append(text(1512, 333, "context match", SMALL_SIZE, weight="bold"))
    parts.append(text(1512, 445, "context match", SMALL_SIZE, weight="bold"))
    parts.extend(box(1570, 330, 180, 100, "Old/new\nevidence", NEUTRAL_FILL, AXIS))

    parts.append(rect(880, 645, 560, 125, "#FFFFFF", GRID, THIN, rx=14))
    parts.append(text(1160, 676, "Probe consequence", SMALL_SIZE, weight="bold"))
    parts.append(circle(925, 710, 14, FILM_FILL, FILM_EDGE, THIN))
    parts.append(text(960, 716, "Old film probe: stronger studied-context match", SMALL_SIZE, anchor="start"))
    parts.append(circle(925, 748, 14, FOIL_FILL, FOIL_EDGE, THIN))
    parts.append(text(960, 754, "Film-like foil: weaker match without studied temporal trace", SMALL_SIZE, anchor="start"))

    parts.append(
        multiline(
            1635,
            610,
            "Task items can be search competitors,\nbut they are not the supplied probe",
            SMALL_SIZE,
            weight="bold",
            line_height=21,
            fill=TASK_EDGE,
        )
    )
    parts.extend(item(1635, 515, "Task", TASK_FILL, TASK_EDGE, r=34))
    return parts


def render_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        defs(),
        '<rect width="100%" height="100%" fill="white"/>',
        *draw_route_panel(),
        line(810, 95, 810, 780, GRID, THIN, marker=""),
        *draw_recognition_panel(),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_h.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_h.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_h.pdf"
    for path_ in [svg_path, png_path, pdf_path]:
        if path_.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path_}")
    svg_path.write_text(render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", INKSCAPE_GDK_BACKEND)
    subprocess.run([str(INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
