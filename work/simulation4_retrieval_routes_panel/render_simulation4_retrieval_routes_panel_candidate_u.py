from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve().parent.parent / "simulation4_test_format_schematic" / "render_simulation4_test_format_schematic_candidate_p.py"

spec = importlib.util.spec_from_file_location("candidate_p", SOURCE)
candidate_p = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_p)

c = candidate_p.candidate_l

WIDTH = 820
HEIGHT = 700


def render_svg() -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="{c.FONT}">',
            c.defs(),
            f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
            *candidate_p.panel_a(),
            "</svg>",
        ]
    )


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_u.svg"
    png_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_u.png"
    pdf_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_u.pdf"
    for path in [svg_path, png_path, pdf_path]:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    svg_path.write_text(render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", c.INKSCAPE_GDK_BACKEND)
    subprocess.run([str(c.INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(c.INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
