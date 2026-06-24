from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures" / "exploratory"
SOURCE = Path(__file__).with_name("render_simulation4_test_format_schematic_candidate_e.py")

spec = importlib.util.spec_from_file_location("candidate_e", SOURCE)
candidate_e = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_e)

WIDTH = 1700
HEIGHT = 840


def draw_route_panel() -> list[str]:
    c = candidate_e
    parts: list[str] = []
    parts.extend(c.panel_title(36, 62, "A", "Item-context retrieval directions"))
    parts.append(c.text(385, 104, "The same learned associations can be read in either direction", c.SMALL_SIZE))

    top_contexts = [(110, 185, "C1"), (260, 185, "C2"), (410, 185, "C3"), (560, 185, "C4")]
    top_items = [(110, 325, "Film", c.FILM_FILL, c.FILM_EDGE), (260, 325, "Film", c.FILM_FILL, c.FILM_EDGE), (410, 325, "Film", c.FILM_FILL, c.FILM_EDGE), (560, 325, "Task", c.TASK_FILL, c.TASK_EDGE)]
    bottom_contexts = [(110, 540, "C1"), (260, 540, "C2"), (410, 540, "C3"), (560, 540, "C4")]
    bottom_items = [(110, 680, "Film", c.FILM_FILL, c.FILM_EDGE), (260, 680, "Film", c.FILM_FILL, c.FILM_EDGE), (410, 680, "Film", c.FILM_FILL, c.FILM_EDGE), (560, 680, "Task", c.TASK_FILL, c.TASK_EDGE)]

    parts.append(c.text(400, 140, "Item-to-context route", c.LABEL_SIZE, weight="bold", fill=c.GREEN))
    for x, y, label in top_contexts:
        parts.extend(c.context(x, y, label))
    for x, y, label, fill, edge in top_items:
        parts.extend(c.item(x, y, label, fill, edge, r=43 if x == 260 else 39))
    parts.append(c.path("M 233 292 L 132 214", c.GREEN, marker="green-arrow"))
    parts.append(c.path("M 260 280 L 260 224", c.GREEN, marker="green-arrow"))
    parts.append(c.path("M 287 292 L 385 214", c.GREEN, marker="green-arrow"))
    parts.append(c.path("M 299 306 L 528 211", c.GREEN, marker="green-arrow"))
    parts.append(c.multiline(645, 252, "Presented item\nreinstates context", c.SMALL_SIZE, weight="bold", anchor="start", line_height=21, fill=c.GREEN))

    parts.append(c.line(70, 420, 730, 420, c.GRID, c.THIN, marker=""))

    parts.append(c.text(400, 495, "Context-to-item route", c.LABEL_SIZE, weight="bold", fill=c.RED))
    for x, y, label in bottom_contexts:
        parts.extend(c.context(x, y, label, r=43 if x == 410 else 38, edge=c.RED if x == 410 else c.AXIS))
    for x, y, label, fill, edge in bottom_items:
        parts.extend(c.item(x, y, label, fill, edge))
    parts.append(c.path("M 383 570 L 132 653", c.RED, marker="red-arrow"))
    parts.append(c.path("M 394 576 L 282 648", c.RED, marker="red-arrow"))
    parts.append(c.path("M 410 584 L 410 637", c.RED, marker="red-arrow"))
    parts.append(c.path("M 437 570 L 538 650", c.RED, marker="red-arrow"))
    parts.append(c.multiline(645, 608, "Current context\ncues competitors", c.SMALL_SIZE, weight="bold", anchor="start", line_height=21, fill=c.RED))
    return parts


def draw_recognition_panel() -> list[str]:
    c = candidate_e
    parts: list[str] = []
    parts.extend(c.panel_title(850, 62, "B", "Supplied-probe recognition decision"))
    parts.append(c.text(1260, 104, "The probe reinstates context; the decision compares contexts", c.SMALL_SIZE))

    parts.extend(c.item(970, 285, "Presented\nprobe", c.NEUTRAL_FILL, c.AXIS, r=48))
    parts.append(c.text(970, 195, "Old film item or film-like foil", c.SMALL_SIZE, weight="bold"))
    parts.append(c.line(1035, 285, 1150, 285, c.GREEN, marker="green-arrow"))
    parts.append(c.text(1094, 260, "item->context", c.SMALL_SIZE, weight="bold", fill=c.GREEN))
    parts.extend(c.box(1150, 230, 220, 110, "Probe-\nreinstated context", c.CONTEXT_FILL, c.AXIS))

    parts.extend(c.box(1150, 430, 220, 100, "Current\ntest context", c.CONTEXT_FILL, c.AXIS))
    parts.append(c.line(1385, 285, 1460, 348, c.AXIS))
    parts.append(c.line(1385, 480, 1460, 372, c.AXIS))
    parts.extend(c.box(1460, 328, 130, 80, "Compare", c.NEUTRAL_FILL, c.AXIS))
    parts.append(c.line(1590, 368, 1624, 368, c.AXIS))
    parts.extend(c.box(1624, 315, 68, 106, "Old/new\nevidence", c.NEUTRAL_FILL, c.AXIS))

    parts.append(c.rect(880, 595, 495, 150, "#FFFFFF", c.GRID, c.THIN, rx=14))
    parts.append(c.text(1127, 628, "Probe consequence", c.SMALL_SIZE, weight="bold"))
    parts.append(c.circle(925, 666, 14, c.FILM_FILL, c.FILM_EDGE, c.THIN))
    parts.append(c.multiline(960, 672, "Old film probe: stronger studied-context match", c.SMALL_SIZE, anchor="start", line_height=20))
    parts.append(c.circle(925, 714, 14, c.FOIL_FILL, c.FOIL_EDGE, c.THIN))
    parts.append(c.multiline(960, 720, "Film-like foil: weaker match without studied temporal trace", c.SMALL_SIZE, anchor="start", line_height=20))

    parts.append(c.multiline(1515, 610, "Task items can be search competitors,\nbut they are not the supplied probe", c.SMALL_SIZE, weight="bold", line_height=21, fill=c.TASK_EDGE))
    parts.extend(c.item(1515, 510, "Task", c.TASK_FILL, c.TASK_EDGE, r=34))
    return parts


def render_svg() -> str:
    c = candidate_e
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        c.defs(),
        '<rect width="100%" height="100%" fill="white"/>',
        *draw_route_panel(),
        c.line(810, 95, 810, 760, c.GRID, c.THIN, marker=""),
        *draw_recognition_panel(),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_f.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_f.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_f.pdf"
    for path_ in [svg_path, png_path, pdf_path]:
        if path_.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path_}")
    svg_path.write_text(render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", candidate_e.INKSCAPE_GDK_BACKEND)
    subprocess.run([str(candidate_e.INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(candidate_e.INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
