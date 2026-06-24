from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
SOURCE = Path(__file__).with_name("render_simulation4_retrieval_routes_panel_candidate_aa.py")

spec = importlib.util.spec_from_file_location("candidate_aa", SOURCE)
candidate_aa = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_aa)


def render_svg() -> str:
    svg = candidate_aa.render_svg()
    svg = svg.replace(
        '<tspan x="642" dy="0">Film items</tspan><tspan x="642" dy="23">reinstate context</tspan>',
        '<tspan x="642" dy="0">Film items reinstate</tspan><tspan x="642" dy="23">context without</tspan><tspan x="642" dy="23">task-item competition</tspan>',
    )
    return svg


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_ab.svg"
    png_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_ab.png"
    pdf_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_ab.pdf"
    for path in [svg_path, png_path, pdf_path]:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    svg_path.write_text(render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", candidate_aa.c.INKSCAPE_GDK_BACKEND)
    subprocess.run([str(candidate_aa.c.INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(candidate_aa.c.INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
