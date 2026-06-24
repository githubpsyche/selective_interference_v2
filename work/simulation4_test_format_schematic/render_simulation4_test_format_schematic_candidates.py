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
HEIGHT = 900
FONT = "Arial, Helvetica, DejaVu Sans, sans-serif"

TEXT = "#111111"
AXIS = "#2F3A46"
NEUTRAL_FILL = "#F2F4F6"
NEUTRAL_EDGE = "#3D4B5C"
CONTEXT_FILL = "#EAF2F8"
CONTEXT_EDGE = "#3D4B5C"
FILM_FILL = "#EAF2FF"
FILM_EDGE = "#1764D8"
TASK_FILL = "#FFF0E6"
TASK_EDGE = "#D96B2B"
FOIL_FILL = "#F3F4F6"
FOIL_EDGE = "#596575"
GREEN = "#168A4A"
RED = "#B13A3A"
GRID = "#DCE3EA"

PANEL_SIZE = 36
TITLE_SIZE = 31
LABEL_SIZE = 21
SMALL_SIZE = 18
TINY_SIZE = 15
STROKE = 3.2
THIN = 2.2


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


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str,
    width: float = STROKE,
    marker: bool = True,
    extra: str = "",
) -> str:
    marker_attr = 'marker-end="url(#arrow)"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width:.1f}" stroke-linecap="round" '
        f'{marker_attr} {extra}/>'
    )


def path(d: str, color: str, width: float = STROKE, marker: bool = True, extra: str = "") -> str:
    marker_attr = 'marker-end="url(#arrow)"' if marker else ""
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width:.1f}" '
        f'stroke-linecap="round" stroke-linejoin="round" {marker_attr} {extra}/>'
    )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    edge: str,
    stroke: float = STROKE,
    rx: float = 10,
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


def defs() -> str:
    return (
        "<defs>"
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{AXIS}"/>'
        "</marker>"
        '<marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{RED}"/>'
        "</marker>"
        '<marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{GREEN}"/>'
        "</marker>"
        "</defs>"
    )


def item(x: float, y: float, label: str, fill: str, edge: str, r: float = 43) -> list[str]:
    return [
        circle(x, y, r, fill, edge),
        multiline(x, y + 7, label, LABEL_SIZE, weight="bold", line_height=21),
    ]


def context_box(x: float, y: float, w: float, h: float, label: str) -> list[str]:
    return [
        rect(x, y, w, h, CONTEXT_FILL, CONTEXT_EDGE, STROKE, rx=16),
        multiline(x + w / 2, y + h / 2 + 7, label, LABEL_SIZE, weight="bold", line_height=23),
    ]


def decision_box(x: float, y: float, w: float, h: float, label: str) -> list[str]:
    return [
        rect(x, y, w, h, NEUTRAL_FILL, NEUTRAL_EDGE, STROKE, rx=12),
        multiline(x + w / 2, y + h / 2 + 7, label, LABEL_SIZE, weight="bold", line_height=23),
    ]


def panel_heading(x: float, y: float, label: str, title: str) -> list[str]:
    return [
        text(x, y, label, PANEL_SIZE, weight="bold", anchor="start"),
        text(x + 62, y + 3, title, TITLE_SIZE, weight="bold", anchor="start"),
    ]


def candidate_a() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        defs(),
        '<rect width="100%" height="100%" fill="white"/>',
    ]

    parts.extend(panel_heading(50, 65, "A", "Context-guided recall"))
    parts.extend(context_box(90, 165, 190, 105, "Current\ntest context"))
    parts.append(line(295, 218, 420, 218, RED))
    parts.append(text(357, 196, "C->item", SMALL_SIZE, weight="bold", fill=RED))
    parts.append(rect(420, 125, 370, 185, "#FFFFFF", GRID, THIN, rx=14))
    parts.append(text(605, 158, "Candidate items", LABEL_SIZE, weight="bold"))
    for x, y, label, fill, edge in [
        (505, 225, "Film", FILM_FILL, FILM_EDGE),
        (605, 225, "Film", FILM_FILL, FILM_EDGE),
        (705, 225, "Task", TASK_FILL, TASK_EDGE),
    ]:
        parts.extend(item(x, y, label, fill, edge, r=39))
    parts.append(path("M 790 218 C 875 218 895 218 970 218", AXIS))
    parts.extend(decision_box(970, 168, 190, 100, "Recalled\nitem"))
    parts.append(text(605, 336, "Film and task candidates compete before a response is selected", SMALL_SIZE))

    parts.extend(panel_heading(50, 465, "B", "Supplied-probe recognition"))
    parts.extend(item(155, 610, "Old\nfilm", FILM_FILL, FILM_EDGE, r=42))
    parts.extend(item(155, 715, "Film-like\nfoil", FOIL_FILL, FOIL_EDGE, r=42))
    parts.append(text(155, 525, "Presented probe", LABEL_SIZE, weight="bold"))
    parts.append(path("M 205 610 C 285 600 315 574 385 574", GREEN, marker=False))
    parts.append(path("M 205 715 C 285 705 315 646 385 646", GREEN, marker=False))
    parts.append(
        '<path d="M 205 610 C 285 600 315 574 385 574" fill="none" '
        f'stroke="{GREEN}" stroke-width="{STROKE}" stroke-linecap="round" '
        'marker-end="url(#arrow-green)"/>'
    )
    parts.append(
        '<path d="M 205 715 C 285 705 315 646 385 646" fill="none" '
        f'stroke="{GREEN}" stroke-width="{STROKE}" stroke-linecap="round" '
        'marker-end="url(#arrow-green)"/>'
    )
    parts.append(text(290, 579, "item->C", SMALL_SIZE, weight="bold", fill=GREEN))
    parts.extend(context_box(385, 560, 205, 105, "Probe-\nreinstated context"))
    parts.extend(context_box(385, 700, 205, 105, "Current\ntest context"))
    parts.append(line(600, 613, 730, 673, AXIS))
    parts.append(line(600, 752, 730, 692, AXIS))
    parts.extend(decision_box(730, 622, 205, 118, "Compare\ncontexts"))
    parts.append(line(945, 681, 1075, 681, AXIS))
    parts.extend(decision_box(1075, 630, 190, 102, "Old/new\nresponse"))
    parts.append(text(830, 775, "No item search is required for the response", SMALL_SIZE))
    parts.append(line(1065, 330, 1065, 502, GRID, THIN, marker=False, extra='stroke-dasharray="8 8"'))
    parts.append(multiline(1215, 413, "Task competitors can be\npresent in context without\nbecoming response options", SMALL_SIZE, line_height=22, fill=TASK_EDGE))
    parts.extend(item(1322, 610, "Task", TASK_FILL, TASK_EDGE, r=38))
    parts.extend(item(1402, 670, "Task", TASK_FILL, TASK_EDGE, r=34))
    parts.append("</svg>")
    return "\n".join(parts)


def candidate_b() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        defs(),
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    parts.extend(panel_heading(50, 65, "A", "Recognition decision with film-like foils"))
    parts.append(text(765, 118, "Presented item reinstates context; old/new evidence comes from the context match", LABEL_SIZE, weight="bold"))

    row_y = [275, 570]
    row_labels = ["Old film probe", "Film-like foil"]
    probe_specs = [
        ("Film\nitem", FILM_FILL, FILM_EDGE, "Studied temporal trace\n+ film source"),
        ("Film-like\nfoil", FOIL_FILL, FOIL_EDGE, "Film source only\nno studied temporal trace"),
    ]
    for y, row_label, spec in zip(row_y, row_labels, probe_specs, strict=True):
        label, fill, edge, note = spec
        parts.append(text(105, y - 118, row_label, TITLE_SIZE - 4, weight="bold", anchor="start"))
        parts.extend(item(210, y, label, fill, edge, r=48))
        parts.append(multiline(210, y + 92, note, SMALL_SIZE, line_height=21))
        parts.append(
            '<path d="M 270 %.1f C 350 %.1f 390 %.1f 465 %.1f" fill="none" '
            'stroke="%s" stroke-width="%.1f" stroke-linecap="round" marker-end="url(#arrow-green)"/>'
            % (y, y, y, y, GREEN, STROKE)
        )
        parts.append(text(365, y - 22, "item->context", SMALL_SIZE, weight="bold", fill=GREEN))
        parts.extend(context_box(465, y - 55, 220, 110, "Probe\ncontext"))
        parts.extend(context_box(805, y - 55, 220, 110, "Current\ntest context"))
        parts.append(line(694, y, 796, y, AXIS))
        parts.append(text(745, y - 26, "match", SMALL_SIZE, weight="bold"))
        decision = "High old\nevidence" if y == row_y[0] else "Lower old\nevidence"
        parts.append(line(1036, y, 1160, y, AXIS))
        parts.extend(decision_box(1160, y - 55, 220, 110, decision))

    parts.append(rect(742, 155, 350, 660, "#FFFFFF", GRID, THIN, rx=18))
    parts.append(text(917, 845, "The comparison is to context, not to a generated item", SMALL_SIZE, weight="bold"))
    parts.append(multiline(1275, 800, "Task items may be strong\nsearch competitors, but they\nare not supplied probes", SMALL_SIZE, line_height=22, fill=TASK_EDGE))
    parts.extend(item(1285, 255, "Task", TASK_FILL, TASK_EDGE, r=36))
    parts.extend(item(1370, 315, "Task", TASK_FILL, TASK_EDGE, r=34))
    parts.append(line(1265, 350, 1075, 482, TASK_EDGE, THIN, marker=False, extra='stroke-dasharray="7 8"'))
    parts.append("</svg>")
    return "\n".join(parts)


def write_candidate(name: str, svg: str) -> tuple[Path, Path, Path]:
    svg_path = FIGURE_DIR / f"{name}.svg"
    png_path = FIGURE_DIR / f"{name}.png"
    pdf_path = FIGURE_DIR / f"{name}.pdf"
    for path_ in [svg_path, png_path, pdf_path]:
        if path_.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path_}")
    svg_path.write_text(svg)
    return svg_path, png_path, pdf_path


def export(svg_path: Path, png_path: Path, pdf_path: Path) -> None:
    if not INKSCAPE.exists():
        raise FileNotFoundError(f"Inkscape not found at {INKSCAPE}")
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", INKSCAPE_GDK_BACKEND)
    subprocess.run(
        [str(INKSCAPE), str(svg_path), f"--export-filename={png_path}"],
        check=True,
        env=env,
    )
    subprocess.run(
        [str(INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"],
        check=True,
        env=env,
    )


def main() -> None:
    outputs = [
        write_candidate(
            "simulation4_test_format_schematic_candidate_a",
            candidate_a(),
        ),
        write_candidate(
            "simulation4_test_format_schematic_candidate_b",
            candidate_b(),
        ),
    ]
    for svg_path, png_path, pdf_path in outputs:
        export(svg_path, png_path, pdf_path)
        print(svg_path)
        print(png_path)
        print(pdf_path)


if __name__ == "__main__":
    main()
