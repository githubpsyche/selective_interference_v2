from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
SOURCE = Path(__file__).with_name("render_simulation4_test_format_schematic_candidate_l.py")

spec = importlib.util.spec_from_file_location("candidate_l", SOURCE)
candidate_l = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_l)


def panel_a() -> list[str]:
    c = candidate_l
    parts = c.panel_a()
    parts.append(
        c.multiline(
            642,
            236,
            ["Presented item", "reinstates context"],
            21,
            fill=c.GREEN,
            anchor="start",
            line_height=24,
        )
    )
    parts.append(
        c.multiline(
            642,
            596,
            ["Current context", "cues competitors"],
            21,
            fill=c.RED,
            anchor="start",
            line_height=24,
        )
    )
    return parts


def panel_b() -> list[str]:
    c = candidate_l
    parts = [
        c.text(820, 52, "B", 44, anchor="start"),
        c.text(1160, 57, "Recognition decision", 28),
        c.circle(1038, 142, 44, c.WHITE, c.AXIS),
        c.text(1038, 151, "Probe", 24),
        c.line(1038, 190, 1038, 236, c.GREEN, 4, marker="green-arrow"),
        c.text(1132, 223, "item-to-context", 21, fill=c.GREEN),
        c.rect(918, 236, 240, 108, c.CONTEXT_FILL, c.AXIS, 3, rx=18),
        c.multiline(1038, 280, ["Probe-reinstated", "context"], 24),
        c.rect(918, 420, 240, 100, c.CONTEXT_FILL, c.AXIS, 3, rx=18),
        c.multiline(1038, 462, ["Current", "test context"], 24),
        c.text(1266, 318, "Comparison", 21),
        c.line(1172, 290, 1260, 370, c.AXIS, 4),
        c.line(1172, 470, 1260, 382, c.AXIS, 4),
        c.circle(1266, 376, 7, c.AXIS, c.AXIS, 0),
        c.line(1275, 376, 1318, 376, c.AXIS, 4),
        c.rect(1318, 326, 158, 100, c.NEUTRAL_FILL, c.AXIS, 3, rx=14),
        c.multiline(1397, 366, ["Old/new", "evidence"], 24),
    ]
    return parts


def render_svg() -> str:
    c = candidate_l
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {c.WIDTH} {c.HEIGHT}" width="{c.WIDTH}" height="{c.HEIGHT}" font-family="{c.FONT}">',
            c.defs(),
            f'<rect x="0" y="0" width="{c.WIDTH}" height="{c.HEIGHT}" fill="white"/>',
            *panel_a(),
            *panel_b(),
            "</svg>",
        ]
    )


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_p.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_p.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_p.pdf"
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
