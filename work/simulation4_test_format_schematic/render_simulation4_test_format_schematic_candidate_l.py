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
HEIGHT = 700
FONT = "Arial, Helvetica, sans-serif"

TEXT = "#111111"
AXIS = "#3D4B5C"
CONTEXT_FILL = "#EEF3F8"
FILM_FILL = "#EAF2FF"
FILM_EDGE = "#1764D8"
TASK_FILL = "#FFF0E6"
TASK_EDGE = "#D96B2B"
GREEN = "#178A4C"
RED = "#A83232"
WHITE = "#FFFFFF"
NEUTRAL_FILL = "#F2F4F6"


def text(
    x: float,
    y: float,
    value: str,
    size: int,
    *,
    weight: int = 700,
    fill: str = TEXT,
    anchor: str = "middle",
) -> str:
    return (
        f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
        f"{escape(value)}</text>"
    )


def multiline(
    x: float,
    y: float,
    lines: list[str],
    size: int,
    *,
    weight: int = 700,
    fill: str = TEXT,
    anchor: str = "middle",
    line_height: int = 28,
) -> str:
    spans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else line_height
        spans.append(f'<tspan x="{x:.0f}" dy="{dy}">{escape(line)}</tspan>')
    return (
        f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
        f"{''.join(spans)}</text>"
    )


def circle(cx: float, cy: float, r: float, fill: str, stroke: str, stroke_width: float = 3) -> str:
    return (
        f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def rect(
    x: float,
    y: float,
    width: float,
    height: float,
    fill: str,
    stroke: str,
    stroke_width: float = 3,
    rx: float = 18,
) -> str:
    return (
        f'<rect x="{x:.0f}" y="{y:.0f}" width="{width:.0f}" height="{height:.0f}" '
        f'rx="{rx:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
    )


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str,
    stroke_width: float = 3,
    *,
    marker: str = "arrow",
) -> str:
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round"{marker_attr}/>'
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


def panel_a() -> list[str]:
    parts = [
        text(16, 52, "A", 44, anchor="start"),
        text(330, 57, "Item-to-context retrieval", 28, fill=GREEN),
    ]
    for x, label in [(90, "C1"), (250, "C2"), (410, "C3"), (570, "C4")]:
        parts.append(circle(x, 145, 48, CONTEXT_FILL, AXIS))
        parts.append(text(x, 154, label, 24))
    for x, label, fill, edge in [
        (90, "Film", FILM_FILL, FILM_EDGE),
        (250, "Film", FILM_FILL, FILM_EDGE),
        (410, "Film", FILM_FILL, FILM_EDGE),
        (570, "Task", TASK_FILL, TASK_EDGE),
    ]:
        parts.append(circle(x, 310, 48, fill, edge))
        parts.append(text(x, 319, label, 24))
    parts.extend(
        [
            line(217, 276, 123, 180, GREEN, marker="green-arrow"),
            line(250, 262, 250, 200, GREEN, marker="green-arrow"),
            line(283, 276, 377, 180, GREEN, marker="green-arrow"),
            line(293, 288, 527, 167, GREEN, marker="green-arrow"),
            text(330, 396, "Context-to-item retrieval", 28, fill=RED),
        ]
    )
    for x, label in [(90, "C1"), (250, "C2"), (410, "C3"), (570, "C4")]:
        parts.append(circle(x, 485, 48, CONTEXT_FILL, AXIS))
        parts.append(text(x, 494, label, 24))
    for x, label, fill, edge in [
        (90, "Film", FILM_FILL, FILM_EDGE),
        (250, "Film", FILM_FILL, FILM_EDGE),
        (410, "Film", FILM_FILL, FILM_EDGE),
        (570, "Task", TASK_FILL, TASK_EDGE),
    ]:
        parts.append(circle(x, 650, 48, fill, edge))
        parts.append(text(x, 659, label, 24))
    parts.extend(
        [
            line(367, 507, 133, 628, RED, marker="red-arrow"),
            line(377, 520, 283, 616, RED, marker="red-arrow"),
            line(410, 533, 410, 595, RED, marker="red-arrow"),
            line(443, 520, 537, 616, RED, marker="red-arrow"),
        ]
    )
    return parts


def panel_b() -> list[str]:
    parts = [
        text(756, 52, "B", 44, anchor="start"),
        text(1120, 57, "Recognition decision", 28),
        circle(850, 280, 48, WHITE, AXIS),
        text(850, 289, "Probe", 24),
        line(910, 280, 1005, 280, GREEN, 4, marker="green-arrow"),
        text(958, 250, "item-to-context", 21, fill=GREEN),
        rect(1005, 220, 230, 120, CONTEXT_FILL, AXIS, 3, rx=18),
        multiline(1120, 270, ["Probe-reinstated", "context"], 24),
        rect(1005, 430, 230, 105, CONTEXT_FILL, AXIS, 3, rx=18),
        multiline(1120, 474, ["Current", "test context"], 24),
        text(1325, 308, "Comparison", 21),
        line(1245, 280, 1318, 350, AXIS, 4),
        line(1245, 483, 1318, 350, AXIS, 4),
        circle(1325, 350, 7, AXIS, AXIS, 0),
        line(1334, 350, 1388, 350, AXIS, 4),
        rect(1388, 300, 98, 100, NEUTRAL_FILL, AXIS, 3, rx=14),
        multiline(1437, 340, ["Old/new", "evidence"], 24),
    ]
    return parts


def render_svg() -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="{FONT}">',
            defs(),
            f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
            *panel_a(),
            *panel_b(),
            "</svg>",
        ]
    )


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_l.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_l.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_l.pdf"
    for path in [svg_path, png_path, pdf_path]:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path}")
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
