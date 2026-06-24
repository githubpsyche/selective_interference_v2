from __future__ import annotations

import os
import subprocess

from render_simulation4_recognition_decision_panel_candidate_r import (
    FIGURE_DIR,
    INKSCAPE,
    INKSCAPE_GDK_BACKEND,
    render_svg,
)


def render_variant_svg() -> str:
    svg = render_svg()
    svg = svg.replace(
        '<text x="454" y="331" font-size="21" font-weight="700" fill="#111111" text-anchor="middle">Comparison</text>',
        '<text x="452" y="296" font-size="21" font-weight="700" fill="#111111" text-anchor="middle">Comparison</text>',
    )
    svg = svg.replace(
        '<path d="M 335 318 C 406 318 430 340 494 350" fill="none" stroke="#3D4B5C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"/>',
        '<path d="M 335 318 C 398 318 440 326 494 350" fill="none" stroke="#3D4B5C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"/>',
    )
    svg = svg.replace(
        '<path d="M 335 426 C 406 426 430 404 494 394" fill="none" stroke="#3D4B5C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"/>',
        '<path d="M 335 426 C 398 426 440 406 494 394" fill="none" stroke="#3D4B5C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"/>',
    )
    return svg


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_s.svg"
    png_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_s.png"
    pdf_path = FIGURE_DIR / "simulation4_recognition_decision_panel_candidate_s.pdf"
    for path_ in [svg_path, png_path, pdf_path]:
        if path_.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path_}")
    svg_path.write_text(render_variant_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", INKSCAPE_GDK_BACKEND)
    subprocess.run([str(INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
