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
NEUTRAL_FILL = "#F2F4F6"
CONTEXT_FILL = "#EEF3F8"
FILM_FILL = "#EAF2FF"
FILM_EDGE = "#1764D8"
TASK_FILL = "#FFF0E6"
TASK_EDGE = "#D96B2B"
GREEN = "#178A4C"
RED = "#A83232"
WHITE = "#FFFFFF"


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
    line_height: int = 23,
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
    dash: str = "",
) -> str:
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round"'
        f'{dash_attr}{marker_attr}/>'
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
        '<marker id="arrow-red" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
        f'<path d="M0,0 L10,4 L0,8 Z" fill="{RED}"/>'
        "</marker>"
        "</defs>"
    )


def item_circle(x: float, y: float, label: str, fill: str, edge: str, *, dashed: bool = False) -> list[str]:
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return [
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="25" fill="{fill}" stroke="{edge}" stroke-width="4"{dash}/>',
        text(x, y + 8, label, 23, fill=edge),
    ]


def render_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="{FONT}">',
        defs(),
        f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
        text(370, 54, "Retrieval routes at test", 27),
        rect(24, 82, 692, 172, WHITE, AXIS, 3, rx=22),
        text(370, 116, "Presented item reinstates context", 21, fill=GREEN),
        text(112, 151, "Presented item", 18, fill=AXIS),
        circle(112, 190, 29, WHITE, FILM_EDGE, 4),
        text(112, 198, "F", 25, fill=FILM_EDGE),
        line(144, 190, 202, 190, AXIS, 3),
        rect(222, 153, 168, 74, WHITE, AXIS, 3, rx=16),
        multiline(306, 177, ["Feature-to-", "context memory", "(MFC)"], 21, line_height=20),
        line(390, 190, 444, 190, GREEN, 3.5, marker="arrow-green"),
        text(545, 151, "Reinstated contexts", 18, fill=AXIS),
        circle(476, 190, 27, CONTEXT_FILL, AXIS, 3),
        text(476, 198, "C1", 20),
        circle(544, 190, 27, CONTEXT_FILL, AXIS, 3),
        text(544, 198, "C2", 20),
        circle(612, 190, 27, CONTEXT_FILL, AXIS, 3),
        text(612, 198, "C3", 20),
        rect(24, 286, 692, 172, WHITE, AXIS, 3, rx=22),
        text(370, 320, "Current context cues competitors", 21, fill=RED),
        text(112, 355, "Current context", 18, fill=AXIS),
        circle(112, 394, 29, CONTEXT_FILL, AXIS, 3),
        text(112, 402, "C", 25),
        line(144, 394, 202, 394, AXIS, 3),
        rect(222, 357, 168, 74, WHITE, AXIS, 3, rx=16),
        multiline(306, 381, ["Context-to-", "feature memory", "(MCF)"], 21, line_height=20),
        line(390, 394, 444, 394, RED, 3.5, marker="arrow-red"),
        text(545, 355, "Candidate items", 18, fill=AXIS),
        *item_circle(476, 394, "F", FILM_FILL, FILM_EDGE),
        *item_circle(544, 394, "F", FILM_FILL, FILM_EDGE),
        *item_circle(612, 394, "T", TASK_FILL, TASK_EDGE, dashed=True),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_t.svg"
    png_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_t.png"
    pdf_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_t.pdf"
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
