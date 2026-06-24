from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
SOURCE_F = Path(__file__).with_name("render_simulation4_test_format_schematic_candidate_f.py")
SOURCE_E = Path(__file__).with_name("render_simulation4_test_format_schematic_candidate_e.py")

spec_f = importlib.util.spec_from_file_location("candidate_f", SOURCE_F)
candidate_f = importlib.util.module_from_spec(spec_f)
assert spec_f.loader is not None
spec_f.loader.exec_module(candidate_f)

spec_e = importlib.util.spec_from_file_location("candidate_e", SOURCE_E)
candidate_e = importlib.util.module_from_spec(spec_e)
assert spec_e.loader is not None
spec_e.loader.exec_module(candidate_e)

WIDTH = 1800
HEIGHT = 840


def draw_recognition_panel() -> list[str]:
    c = candidate_e
    parts: list[str] = []
    parts.extend(c.panel_title(850, 62, "B", "Supplied-probe recognition decision"))
    parts.append(c.text(1300, 104, "The probe reinstates context; the decision compares contexts", c.SMALL_SIZE))

    parts.extend(c.item(980, 285, "Presented\nprobe", c.NEUTRAL_FILL, c.AXIS, r=48))
    parts.append(c.text(980, 195, "Old film item or film-like foil", c.SMALL_SIZE, weight="bold"))
    parts.append(c.line(1045, 285, 1160, 285, c.GREEN, marker="green-arrow"))
    parts.append(c.text(1104, 260, "item->context", c.SMALL_SIZE, weight="bold", fill=c.GREEN))
    parts.extend(c.box(1160, 230, 230, 110, "Probe-\nreinstated context", c.CONTEXT_FILL, c.AXIS))

    parts.extend(c.box(1160, 430, 230, 100, "Current\ntest context", c.CONTEXT_FILL, c.AXIS))
    parts.append(c.line(1405, 285, 1480, 348, c.AXIS))
    parts.append(c.line(1405, 480, 1480, 372, c.AXIS))
    parts.extend(c.box(1480, 328, 140, 80, "Compare", c.NEUTRAL_FILL, c.AXIS))
    parts.append(c.line(1620, 368, 1655, 368, c.AXIS))
    parts.extend(c.box(1655, 315, 125, 106, "Old/new\nevidence", c.NEUTRAL_FILL, c.AXIS))

    parts.append(c.rect(880, 595, 540, 150, "#FFFFFF", c.GRID, c.THIN, rx=14))
    parts.append(c.text(1150, 628, "Probe consequence", c.SMALL_SIZE, weight="bold"))
    parts.append(c.circle(925, 666, 14, c.FILM_FILL, c.FILM_EDGE, c.THIN))
    parts.append(c.multiline(960, 672, "Old film probe: stronger studied-context match", c.SMALL_SIZE, anchor="start", line_height=20))
    parts.append(c.circle(925, 714, 14, c.FOIL_FILL, c.FOIL_EDGE, c.THIN))
    parts.append(c.multiline(960, 720, "Film-like foil: weaker match without studied temporal trace", c.SMALL_SIZE, anchor="start", line_height=20))

    parts.append(c.multiline(1565, 612, "Task items can be search competitors,\nbut they are not the supplied probe", c.SMALL_SIZE, weight="bold", line_height=21, fill=c.TASK_EDGE))
    parts.extend(c.item(1565, 510, "Task", c.TASK_FILL, c.TASK_EDGE, r=34))
    return parts


def render_svg() -> str:
    c = candidate_e
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        c.defs(),
        '<rect width="100%" height="100%" fill="white"/>',
        *candidate_f.draw_route_panel(),
        c.line(810, 95, 810, 760, c.GRID, c.THIN, marker=""),
        *draw_recognition_panel(),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_g.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_g.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_g.pdf"
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
