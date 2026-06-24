from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve().parent.parent / "simulation4_test_format_schematic" / "render_simulation4_test_format_schematic_candidate_l.py"

spec = importlib.util.spec_from_file_location("candidate_l", SOURCE)
candidate_l = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_l)

c = candidate_l

WIDTH = 880
HEIGHT = 700


def muted_task_circle(x: float, y: float) -> list[str]:
    return [
        (
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="48" fill="{c.WHITE}" '
            f'stroke="{c.TASK_EDGE}" stroke-width="3" stroke-dasharray="7 6" opacity="0.70"/>'
        ),
        c.text(x, y + 9, "Task", 24, fill=c.TASK_EDGE, weight=700),
    ]


def panel_a() -> list[str]:
    parts = [
        c.text(16, 52, "A", 44, anchor="start"),
        c.text(330, 57, "Item-to-context retrieval", 28, fill=c.GREEN),
    ]
    for x, label in [(90, "C1"), (250, "C2"), (410, "C3"), (570, "C4")]:
        parts.append(c.circle(x, 145, 48, c.CONTEXT_FILL, c.AXIS))
        parts.append(c.text(x, 154, label, 24))
    for x, label, fill, edge in [
        (90, "Film", c.FILM_FILL, c.FILM_EDGE),
        (250, "Film", c.FILM_FILL, c.FILM_EDGE),
        (410, "Film", c.FILM_FILL, c.FILM_EDGE),
    ]:
        parts.append(c.circle(x, 310, 48, fill, edge))
        parts.append(c.text(x, 319, label, 24))
    parts.extend(muted_task_circle(570, 310))
    parts.extend(
        [
            c.line(217, 276, 123, 180, c.GREEN, marker="green-arrow"),
            c.line(250, 262, 250, 200, c.GREEN, marker="green-arrow"),
            c.line(283, 276, 377, 180, c.GREEN, marker="green-arrow"),
            c.line(293, 288, 527, 167, c.GREEN, marker="green-arrow"),
            c.multiline(
                642,
                232,
                ["Presented film item", "reinstates context"],
                21,
                fill=c.GREEN,
                anchor="start",
                line_height=24,
            ),
            c.text(330, 396, "Context-to-item retrieval", 28, fill=c.RED),
        ]
    )
    for x, label in [(90, "C1"), (250, "C2"), (410, "C3"), (570, "C4")]:
        parts.append(c.circle(x, 485, 48, c.CONTEXT_FILL, c.AXIS))
        parts.append(c.text(x, 494, label, 24))
    for x, label, fill, edge in [
        (90, "Film", c.FILM_FILL, c.FILM_EDGE),
        (250, "Film", c.FILM_FILL, c.FILM_EDGE),
        (410, "Film", c.FILM_FILL, c.FILM_EDGE),
        (570, "Task", c.TASK_FILL, c.TASK_EDGE),
    ]:
        parts.append(c.circle(x, 650, 48, fill, edge))
        parts.append(c.text(x, 659, label, 24))
    parts.extend(
        [
            c.line(367, 507, 133, 628, c.RED, marker="red-arrow"),
            c.line(377, 520, 283, 616, c.RED, marker="red-arrow"),
            c.line(410, 533, 410, 595, c.RED, marker="red-arrow"),
            c.line(443, 520, 537, 616, c.RED, marker="red-arrow"),
            c.multiline(
                642,
                586,
                ["Film-like context cues", "film and task items"],
                21,
                fill=c.RED,
                anchor="start",
                line_height=24,
            ),
        ]
    )
    return parts


def render_svg() -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="{c.FONT}">',
            c.defs(),
            f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
            *panel_a(),
            "</svg>",
        ]
    )


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_w.svg"
    png_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_w.png"
    pdf_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_w.pdf"
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
