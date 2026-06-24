from __future__ import annotations

import os
import subprocess

import render_simulation4_retrieval_routes_panel_candidate_u as candidate_u


def main() -> None:
    candidate_u.WIDTH = 860
    svg_path = candidate_u.FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_v.svg"
    png_path = candidate_u.FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_v.png"
    pdf_path = candidate_u.FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_v.pdf"
    for path in [svg_path, png_path, pdf_path]:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    svg_path.write_text(candidate_u.render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", candidate_u.c.INKSCAPE_GDK_BACKEND)
    subprocess.run([str(candidate_u.c.INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(candidate_u.c.INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
