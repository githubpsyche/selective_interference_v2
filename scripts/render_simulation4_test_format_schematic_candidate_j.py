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
    parts.append(c.text(1300, 104, "A supplied probe reinstates context; evidence reflects the match to current test context", c.SMALL_SIZE))

    parts.append(c.text(975, 215, "Presented probe", c.SMALL_SIZE, weight="bold"))
    parts.extend(c.item(975, 300, "Probe", c.NEUTRAL_FILL, c.AXIS, r=46))
    parts.append(c.line(1038, 300, 1155, 300, c.GREEN, marker="green-arrow"))
    parts.append(c.text(1100, 274, "item->context", c.SMALL_SIZE, weight="bold", fill=c.GREEN))

    parts.extend(c.box(1155, 242, 250, 116, "Probe-\nreinstated context", c.CONTEXT_FILL, c.AXIS))
    parts.extend(c.box(1155, 500, 250, 106, "Current\ntest context", c.CONTEXT_FILL, c.AXIS))

    parts.append(c.text(1500, 345, "context match", c.SMALL_SIZE, weight="bold"))
    parts.append(c.line(1422, 300, 1572, 378, c.AXIS))
    parts.append(c.line(1422, 553, 1572, 408, c.AXIS))
    parts.extend(c.box(1572, 350, 180, 100, "Old/new\nevidence", c.NEUTRAL_FILL, c.AXIS))
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
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_j.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_j.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_j.pdf"
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
