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
        text(370, 54, "Recognition decision", 27),
        circle(255, 105, 32, "white", AXIS, 3),
        text(255, 114, "Probe", 21),
        line(255, 138, 255, 164, AXIS, 3),
        rect(150, 164, 210, 74, "white", AXIS, 3, rx=16),
        multiline(255, 188, ["Feature-to-", "context memory", "(MFC)"], 21, line_height=20),
        line(255, 238, 255, 280, GREEN, 3.5, marker="arrow-green"),
        text(338, 264, "reinstates", 20, fill=GREEN),
        rect(175, 282, 160, 72, CONTEXT_FILL, GREEN, 3, rx=18),
        multiline(255, 311, ["Probe", "context"], 21, fill=AXIS, line_height=23),
        rect(175, 390, 160, 72, NEUTRAL_FILL, AXIS, 3, rx=18),
        multiline(255, 419, ["Current", "test context"], 21, fill=AXIS, line_height=23),
        text(454, 331, "Comparison", 21),
        path("M 335 318 C 406 318 430 340 494 350", AXIS, 3, marker="arrow"),
        path("M 335 426 C 406 426 430 404 494 394", AXIS, 3, marker="arrow"),
        rect(514, 340, 178, 74, NEUTRAL_FILL, AXIS, 3, rx=16),
        multiline(603, 367, ["Old/new", "evidence"], 21, line_height=23),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_r.svg"
    png_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_r.png"
    pdf_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_r.pdf"
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
