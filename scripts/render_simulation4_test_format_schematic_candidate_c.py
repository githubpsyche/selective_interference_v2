from __future__ import annotations

import os
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures" / "exploratory"
INKSCAPE = Path("/Applications/Inkscape.app/Contents/MacOS/inkscape")
INKSCAPE_GDK_BACKEND = os.environ.get("INKSCAPE_GDK_BACKEND", "x11")

WIDTH = 1500
HEIGHT = 900
FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"

TEXT = "#111111"
AXIS = "#2F3A46"
GRID = "#DCE3EA"
CONTEXT_FILL = "#EAF2F8"
NEUTRAL_FILL = "#F2F4F6"
FILM_FILL = "#EAF2FF"
FILM_EDGE = "#1764D8"
FOIL_FILL = "#F3F4F6"
FOIL_EDGE = "#596575"
TASK_FILL = "#FFF0E6"
TASK_EDGE = "#D96B2B"
GREEN = "#168A4A"

STROKE = 3.2
THIN = 2.0
PANEL_SIZE = 36
TITLE_SIZE = 31
LABEL_SIZE = 21
SMALL_SIZE = 18


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
    line_height: float = 24,
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


def circle(cx: float, cy: float, r: float, fill: str, edge: str) -> str:
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
        f'fill="{fill}" stroke="{edge}" stroke-width="{STROKE:.1f}"/>'
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
        "</defs>"
    )


def item(cx: float, cy: float, label: str, fill: str, edge: str) -> list[str]:
    return [
        circle(cx, cy, 48, fill, edge),
        multiline(cx, cy + 7, label, LABEL_SIZE, weight="bold", line_height=22),
    ]


def context_pair(x: float, y: float, top_label: str) -> list[str]:
    return [
        rect(x, y, 250, 82, CONTEXT_FILL, AXIS, STROKE, rx=14),
        multiline(x + 125, y + 47, top_label, SMALL_SIZE, weight="bold", line_height=20),
        rect(x, y + 104, 250, 82, NEUTRAL_FILL, AXIS, STROKE, rx=14),
        multiline(x + 125, y + 151, "Current\ntest context", SMALL_SIZE, weight="bold", line_height=20),
        line(x + 262, y + 41, x + 342, y + 88, AXIS),
        line(x + 262, y + 145, x + 342, y + 104, AXIS),
    ]


def decision_box(x: float, y: float, label: str, edge: str = AXIS) -> list[str]:
    return [
        rect(x, y, 210, 106, NEUTRAL_FILL, edge, STROKE, rx=12),
        multiline(x + 105, y + 58, label, LABEL_SIZE, weight="bold", line_height=23),
    ]


def row(
    y: float,
    row_label: str,
    probe_label: str,
    probe_fill: str,
    probe_edge: str,
    trace_text: str,
    evidence_label: str,
    evidence_edge: str,
) -> list[str]:
    parts = []
    parts.append(text(85, y - 112, row_label, TITLE_SIZE - 4, weight="bold", anchor="start"))
    parts.extend(item(205, y, probe_label, probe_fill, probe_edge))
    parts.append(multiline(205, y + 95, trace_text, SMALL_SIZE, line_height=21))
    parts.append(line(270, y, 405, y, GREEN, marker="green-arrow"))
    parts.append(text(340, y - 24, "item->context", SMALL_SIZE, weight="bold", fill=GREEN))
    parts.append(rect(405, y - 55, 230, 110, CONTEXT_FILL, AXIS, STROKE, rx=14))
    parts.append(multiline(520, y + 7, "Probe-\nreinstated context", LABEL_SIZE, weight="bold", line_height=23))
    parts.append(line(645, y, 720, y, AXIS))
    parts.extend(context_pair(720, y - 92, "Probe context"))
    parts.append(text(935, y - 114, "compare", SMALL_SIZE, weight="bold"))
    parts.extend(decision_box(1128, y - 53, evidence_label, evidence_edge))
    parts.append(line(1072, y, 1120, y, AXIS))
    return parts


def render_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        defs(),
        '<rect width="100%" height="100%" fill="white"/>',
        text(50, 65, "A", PANEL_SIZE, weight="bold", anchor="start"),
        text(112, 68, "Supplied-probe recognition decision", TITLE_SIZE, weight="bold", anchor="start"),
        text(765, 122, "The item is given; old/new evidence comes from how its reinstated context matches test context", LABEL_SIZE, weight="bold"),
    ]
    parts.extend(
        row(
            300,
            "Old film probe",
            "Film\nitem",
            FILM_FILL,
            FILM_EDGE,
            "Studied temporal trace\n+ film source",
            "High old\nevidence",
            FILM_EDGE,
        )
    )
    parts.extend(
        row(
            625,
            "Film-like foil",
            "Film-like\nfoil",
            FOIL_FILL,
            FOIL_EDGE,
            "Film source only\nno studied temporal trace",
            "Lower old\nevidence",
            FOIL_EDGE,
        )
    )
    parts.append(multiline(1258, 775, "Task items can be\nsearch competitors\nwithout being probes", SMALL_SIZE, line_height=22, fill=TASK_EDGE))
    parts.extend(item(1282, 302, "Task", TASK_FILL, TASK_EDGE))
    parts.extend(item(1370, 375, "Task", TASK_FILL, TASK_EDGE))
    parts.append(line(1272, 435, 1100, 585, TASK_EDGE, THIN, marker="", extra='stroke-dasharray="7 8"'))
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_c.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_c.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_c.pdf"
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
