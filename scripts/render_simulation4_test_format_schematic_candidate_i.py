from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures" / "exploratory"
SOURCE = Path(__file__).with_name("render_simulation4_test_format_schematic_candidate_h.py")

spec = importlib.util.spec_from_file_location("candidate_h", SOURCE)
candidate_h = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_h)


def draw_recognition_panel() -> list[str]:
    c = candidate_h
    parts: list[str] = []
    parts.extend(c.panel_title(850, 62, "B", "Supplied-probe recognition decision"))
    parts.append(c.text(1300, 104, "The probe reinstates context; old/new evidence depends on the context match", c.SMALL_SIZE))

    parts.extend(c.item(975, 292, "Presented\nprobe", c.NEUTRAL_FILL, c.AXIS, r=48))
    parts.append(c.text(975, 198, "Old film item or film-like foil", c.SMALL_SIZE, weight="bold"))
    parts.append(c.line(1040, 292, 1155, 292, c.GREEN, marker="green-arrow"))
    parts.append(c.text(1100, 267, "item->context", c.SMALL_SIZE, weight="bold", fill=c.GREEN))

    parts.extend(c.box(1155, 235, 245, 114, "Probe-\nreinstated context", c.CONTEXT_FILL, c.AXIS))
    parts.extend(c.box(1155, 488, 245, 104, "Current\ntest context", c.CONTEXT_FILL, c.AXIS))

    parts.append(c.text(1495, 285, "context match", c.SMALL_SIZE, weight="bold"))
    parts.append(c.line(1416, 292, 1570, 365, c.AXIS))
    parts.append(c.line(1416, 540, 1570, 392, c.AXIS))
    parts.extend(c.box(1570, 330, 180, 100, "Old/new\nevidence", c.NEUTRAL_FILL, c.AXIS))

    parts.append(c.rect(880, 645, 560, 125, "#FFFFFF", c.GRID, c.THIN, rx=14))
    parts.append(c.text(1160, 676, "Probe consequence", c.SMALL_SIZE, weight="bold"))
    parts.append(c.circle(925, 710, 14, c.FILM_FILL, c.FILM_EDGE, c.THIN))
    parts.append(c.text(960, 716, "Old film probe: stronger studied-context match", c.SMALL_SIZE, anchor="start"))
    parts.append(c.circle(925, 748, 14, c.FOIL_FILL, c.FOIL_EDGE, c.THIN))
    parts.append(c.text(960, 754, "Film-like foil: weaker match without studied temporal trace", c.SMALL_SIZE, anchor="start"))

    parts.append(
        c.multiline(
            1635,
            610,
            "Task items can be search competitors,\nbut they are not the supplied probe",
            c.SMALL_SIZE,
            weight="bold",
            line_height=21,
            fill=c.TASK_EDGE,
        )
    )
    parts.extend(c.item(1635, 515, "Task", c.TASK_FILL, c.TASK_EDGE, r=34))
    return parts


def render_svg() -> str:
    c = candidate_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{c.WIDTH}" height="{c.HEIGHT}" viewBox="0 0 {c.WIDTH} {c.HEIGHT}">',
        c.defs(),
        '<rect width="100%" height="100%" fill="white"/>',
        *c.draw_route_panel(),
        c.line(810, 95, 810, 780, c.GRID, c.THIN, marker=""),
        *draw_recognition_panel(),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_i.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_i.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_i.pdf"
    for path_ in [svg_path, png_path, pdf_path]:
        if path_.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path_}")
    svg_path.write_text(render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", candidate_h.INKSCAPE_GDK_BACKEND)
    subprocess.run([str(candidate_h.INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(candidate_h.INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
