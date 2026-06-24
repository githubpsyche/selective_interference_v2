from __future__ import annotations

import os
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")
INKSCAPE_GDK_BACKEND = os.environ.get("INKSCAPE_GDK_BACKEND", "x11")

WIDTH = 1500
HEIGHT = 820
FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"

TEXT = "#111111"
AXIS = "#2F3A46"
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
GRID = "#DCE3EA"

STROKE = 3.0
THIN = 2.0
PANEL_SIZE = 36
TITLE_SIZE = 30
LABEL_SIZE = 21
SMALL_SIZE = 17
TINY_SIZE = 15


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


def box(x: float, y: float, w: float, h: float, label: str, fill: str = NEUTRAL_FILL, edge: str = AXIS) -> list[str]:
    return [
        rect(x, y, w, h, fill, edge, STROKE, rx=13),
        multiline(x + w / 2, y + h / 2 + 7, label, LABEL_SIZE, weight="bold", line_height=23),
    ]


def panel_title(x: float, y: float, label: str, title: str) -> list[str]:
    return [
        text(x, y, label, PANEL_SIZE, weight="bold", anchor="start"),
        text(x + 62, y + 2, title, TITLE_SIZE, weight="bold", anchor="start"),
    ]


def draw_route_panel() -> list[str]:
    parts: list[str] = []
    parts.extend(panel_title(36, 62, "A", "Two directions through the same associations"))
    parts.append(text(360, 104, "A supplied item can reinstate context; context can also cue candidate items", SMALL_SIZE))

    top_contexts = [(105, 185, "C1"), (245, 185, "C2"), (385, 185, "C3"), (525, 185, "C4")]
    top_items = [(105, 325, "Film", FILM_FILL, FILM_EDGE), (245, 325, "Film", FILM_FILL, FILM_EDGE), (385, 325, "Film", FILM_FILL, FILM_EDGE), (525, 325, "Task", TASK_FILL, TASK_EDGE)]
    bottom_contexts = [(105, 540, "C1"), (245, 540, "C2"), (385, 540, "C3"), (525, 540, "C4")]
    bottom_items = [(105, 680, "Film", FILM_FILL, FILM_EDGE), (245, 680, "Film", FILM_FILL, FILM_EDGE), (385, 680, "Film", FILM_FILL, FILM_EDGE), (525, 680, "Task", TASK_FILL, TASK_EDGE)]

    parts.append(text(360, 140, "Item-to-context route", LABEL_SIZE, weight="bold", fill=GREEN))
    for x, y, label in top_contexts:
        parts.extend(context(x, y, label))
    for x, y, label, fill, edge in top_items:
        radius = 43 if x == 245 else 39
        parts.extend(item(x, y, label, fill, edge, r=radius))
    parts.append(path("M 218 292 L 128 214", GREEN, marker="green-arrow"))
    parts.append(path("M 245 280 L 245 224", GREEN, marker="green-arrow"))
    parts.append(path("M 272 292 L 360 214", GREEN, marker="green-arrow"))
    parts.append(path("M 284 306 L 493 211", GREEN, marker="green-arrow"))
    parts.append(multiline(604, 250, "Presented item\nreinstates context", SMALL_SIZE, weight="bold", anchor="start", line_height=21, fill=GREEN))

    parts.append(line(70, 420, 650, 420, GRID, THIN, marker=""))

    parts.append(text(360, 495, "Context-to-item route", LABEL_SIZE, weight="bold", fill=RED))
    for x, y, label in bottom_contexts:
        radius = 43 if x == 385 else 38
        parts.extend(context(x, y, label, r=radius, edge=RED if x == 385 else AXIS))
    for x, y, label, fill, edge in bottom_items:
        parts.extend(item(x, y, label, fill, edge))
    parts.append(path("M 358 570 L 128 653", RED, marker="red-arrow"))
    parts.append(path("M 368 576 L 267 648", RED, marker="red-arrow"))
    parts.append(path("M 385 584 L 385 637", RED, marker="red-arrow"))
    parts.append(path("M 412 570 L 502 650", RED, marker="red-arrow"))
    parts.append(multiline(604, 608, "Current context\ncues competitors", SMALL_SIZE, weight="bold", anchor="start", line_height=21, fill=RED))
    return parts


def draw_recognition_panel() -> list[str]:
    parts: list[str] = []
    parts.extend(panel_title(745, 62, "B", "Supplied-probe recognition decision"))
    parts.append(text(1110, 104, "Recognition uses the item-to-context route, then compares contexts", SMALL_SIZE))

    parts.extend(item(845, 270, "Presented\nprobe", NEUTRAL_FILL, AXIS, r=48))
    parts.append(text(845, 180, "Old film item or film-like foil", SMALL_SIZE, weight="bold"))
    parts.append(line(910, 270, 1025, 270, GREEN, marker="green-arrow"))
    parts.append(text(970, 245, "item->context", SMALL_SIZE, weight="bold", fill=GREEN))
    parts.extend(box(1025, 215, 210, 110, "Probe-\nreinstated context", CONTEXT_FILL, AXIS))

    parts.extend(box(1025, 425, 210, 100, "Current\ntest context", CONTEXT_FILL, AXIS))
    parts.append(line(1248, 270, 1330, 338, AXIS))
    parts.append(line(1248, 475, 1330, 368, AXIS))
    parts.extend(box(1330, 312, 135, 82, "Compare", NEUTRAL_FILL, AXIS))
    parts.append(line(1465, 353, 1490, 353, AXIS))
    parts.extend(box(1228, 610, 215, 100, "Old/new\nevidence", NEUTRAL_FILL, AXIS))
    parts.append(path("M 1398 397 C 1400 470 1368 540 1344 602", AXIS))

    parts.append(rect(770, 570, 360, 165, "#FFFFFF", GRID, THIN, rx=14))
    parts.append(text(950, 604, "Probe consequence", SMALL_SIZE, weight="bold"))
    parts.append(circle(820, 642, 14, FILM_FILL, FILM_EDGE, THIN))
    parts.append(multiline(855, 649, "Old film probe: stronger\nstudied-context match", SMALL_SIZE, anchor="start", line_height=20))
    parts.append(circle(820, 700, 14, FOIL_FILL, FOIL_EDGE, THIN))
    parts.append(multiline(855, 706, "Film-like foil: weaker match\nwithout studied temporal trace", SMALL_SIZE, anchor="start", line_height=20))

    parts.append(multiline(1326, 515, "The response is old/new,\nnot a selected task item", SMALL_SIZE, weight="bold", line_height=21, fill=TASK_EDGE))
    parts.extend(item(1420, 470, "Task", TASK_FILL, TASK_EDGE, r=34))
    return parts


def render_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        defs(),
        '<rect width="100%" height="100%" fill="white"/>',
        *draw_route_panel(),
        line(720, 95, 720, 760, GRID, THIN, marker=""),
        *draw_recognition_panel(),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_e.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_e.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_e.pdf"
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
