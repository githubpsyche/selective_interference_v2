from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures" / "exploratory"
SOURCE = Path(__file__).with_name("render_simulation4_test_format_schematic_candidate_l.py")

spec = importlib.util.spec_from_file_location("candidate_l", SOURCE)
candidate_l = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_l)


def panel_b() -> list[str]:
    c = candidate_l
    parts = [
        c.text(756, 52, "B", 44, anchor="start"),
        c.text(1120, 57, "Recognition decision", 28),
        c.circle(1120, 138, 43, c.WHITE, c.AXIS),
        c.text(1120, 147, "Probe", 24),
        c.text(1120, 216, "item-to-context", 21, fill=c.GREEN),
        c.line(1120, 186, 1120, 244, c.GREEN, 4, marker="green-arrow"),
        c.rect(1000, 244, 240, 104, c.CONTEXT_FILL, c.AXIS, 3, rx=18),
        c.multiline(1120, 286, ["Probe-reinstated", "context"], 24),
        c.rect(1000, 408, 240, 98, c.CONTEXT_FILL, c.AXIS, 3, rx=18),
        c.multiline(1120, 449, ["Current", "test context"], 24),
        c.text(1330, 370, "Comparison", 21),
        c.line(1255, 296, 1324, 392, c.AXIS, 4),
        c.line(1255, 456, 1324, 392, c.AXIS, 4),
        c.circle(1330, 392, 7, c.AXIS, c.AXIS, 0),
        c.line(1330, 402, 1330, 452, c.AXIS, 4),
        c.rect(1240, 452, 180, 104, c.NEUTRAL_FILL, c.AXIS, 3, rx=14),
        c.multiline(1330, 495, ["Old/new", "evidence"], 24),
    ]
    return parts


def render_svg() -> str:
    c = candidate_l
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {c.WIDTH} {c.HEIGHT}" width="{c.WIDTH}" height="{c.HEIGHT}" font-family="{c.FONT}">',
            c.defs(),
            f'<rect x="0" y="0" width="{c.WIDTH}" height="{c.HEIGHT}" fill="white"/>',
            *c.panel_a(),
            *panel_b(),
            "</svg>",
        ]
    )


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_o.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_o.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_o.pdf"
    for path in [svg_path, png_path, pdf_path]:
        if path.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    svg_path.write_text(render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", candidate_l.INKSCAPE_GDK_BACKEND)
    subprocess.run([str(candidate_l.INKSCAPE), str(svg_path), f"--export-filename={png_path}"], check=True, env=env)
    subprocess.run([str(candidate_l.INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"], check=True, env=env)
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
