from __future__ import annotations

import os
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")
INKSCAPE_GDK_BACKEND = os.environ.get("INKSCAPE_GDK_BACKEND", "x11")

WIDTH = 740
HEIGHT = 500
FONT = "Arial, Helvetica, sans-serif"

TEXT = "#111111"
AXIS = "#3D4B5C"
GRID = "#DCE3EA"
CONTEXT_FILL = "#EEF3F8"
NEUTRAL_FILL = "#F2F4F6"
GREEN = "#178A4C"


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
    line_height: int = 24,
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


def circle(cx: float, cy: float, r: float, fill: str, stroke: str, stroke_width: float = 3) -> str:
    return (
        f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
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


def path(d: str, stroke: str, stroke_width: float = 3, *, marker: str = "") -> str:
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round"{marker_attr}/>'
    )


def defs() -> str:
    return (
        "<defs>"
        '<marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
        f'<path d="M0,0 L10,4 L0,8 Z" fill="{AXIS}"/>'
        "</marker>"
        '<marker id="arrow-green" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
        f'<path d="M0,0 L10,4 L0,8 Z" fill="{GREEN}"/>'
        "</marker>"
        "</defs>"
    )


def render_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="{FONT}">',
        defs(),
        f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
        text(370, 62, "Recognition decision", 27),
        circle(120, 158, 34, "white", AXIS, 3),
        text(120, 167, "Probe", 21),
        line(158, 158, 250, 158, AXIS, 3),
        rect(270, 116, 190, 84, "white", AXIS, 3, rx=16),
        multiline(365, 142, ["Feature-to-", "context memory", "(MFC)"], 21, line_height=21),
        line(460, 158, 554, 158, GREEN, 3.5, marker="arrow-green"),
        text(508, 133, "reinstates", 20, fill=GREEN),
        rect(574, 116, 142, 84, CONTEXT_FILL, GREEN, 3, rx=18),
        multiline(645, 148, ["Probe", "context"], 21, fill=AXIS, line_height=23),
        rect(574, 268, 142, 84, NEUTRAL_FILL, AXIS, 3, rx=18),
        multiline(645, 300, ["Current", "test context"], 21, fill=AXIS, line_height=23),
        path("M 645 206 L 645 248", AXIS, 3),
        path("M 610 248 C 610 235 622 226 645 226 C 668 226 680 235 680 248", AXIS, 2.5),
        path("M 610 248 C 610 261 622 270 645 270 C 668 270 680 261 680 248", AXIS, 2.5),
        text(520, 255, "Comparison", 21, anchor="end"),
        line(645, 354, 645, 394, AXIS, 3),
        rect(554, 394, 182, 76, NEUTRAL_FILL, AXIS, 3, rx=16),
        multiline(645, 421, ["Old/new", "evidence"], 21, line_height=23),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_q.svg"
    png_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_q.png"
    pdf_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_q.pdf"
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
