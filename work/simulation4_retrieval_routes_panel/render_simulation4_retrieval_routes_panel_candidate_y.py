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


def defs() -> str:
    return (
        "<defs>"
        '<marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{c.FILM_EDGE}"/>'
        "</marker>"
        '<marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{c.RED}"/>'
        "</marker>"
        "</defs>"
    )


def item_circle(
    x: float,
    y: float,
    label: str,
    fill: str,
    stroke: str,
    *,
    stroke_width: float = 3,
    text_fill: str | None = None,
) -> list[str]:
    return [
        c.circle(x, y, 48, fill, stroke, stroke_width),
        c.text(x, y + 9, label, 24, fill=text_fill or c.TEXT),
    ]


def context_circle(
    x: float,
    y: float,
    label: str,
    *,
    stroke: str = "",
    stroke_width: float = 3,
) -> list[str]:
    return [
        c.circle(x, y, 48, c.CONTEXT_FILL, stroke or c.AXIS, stroke_width),
        c.text(x, y + 9, label, 24),
    ]


def active_halo(x: float, y: float, color: str) -> str:
    return (
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="54" fill="none" '
        f'stroke="{color}" stroke-width="5" opacity="0.28"/>'
    )


def panel_a() -> list[str]:
    parts = [
        c.text(16, 52, "A", 44, anchor="start"),
        c.text(330, 57, "Item-to-context retrieval", 28, fill=c.FILM_EDGE),
    ]
    for x, label in [(90, "C1"), (250, "C2"), (410, "C3"), (570, "C4")]:
        parts.extend(context_circle(x, 145, label))
    parts.extend(item_circle(90, 310, "Film", c.FILM_FILL, c.FILM_EDGE))
    parts.append(active_halo(250, 310, c.FILM_EDGE))
    parts.extend(item_circle(250, 310, "Film", c.FILM_FILL, c.FILM_EDGE, stroke_width=5))
    parts.extend(item_circle(410, 310, "Film", c.FILM_FILL, c.FILM_EDGE))
    parts.extend(item_circle(570, 310, "Task", c.TASK_FILL, c.TASK_EDGE))
    parts.extend(
        [
            c.line(217, 276, 123, 180, c.FILM_EDGE, 4, marker="arrow-blue"),
            c.line(250, 262, 250, 200, c.FILM_EDGE, 4, marker="arrow-blue"),
            c.line(283, 276, 377, 180, c.FILM_EDGE, 4, marker="arrow-blue"),
            c.line(293, 288, 527, 167, c.FILM_EDGE, 4, marker="arrow-blue"),
            c.multiline(
                642,
                232,
                ["Presented film item", "reinstates context"],
                21,
                fill=c.FILM_EDGE,
                anchor="start",
                line_height=24,
            ),
            c.text(330, 396, "Context-to-item retrieval", 28, fill=c.RED),
        ]
    )
    for x, label in [(90, "C1"), (250, "C2"), (570, "C4")]:
        parts.extend(context_circle(x, 485, label))
    parts.append(active_halo(410, 485, c.RED))
    parts.extend(context_circle(410, 485, "C3", stroke=c.RED, stroke_width=5))
    for x, label, fill, edge in [
        (90, "Film", c.FILM_FILL, c.FILM_EDGE),
        (250, "Film", c.FILM_FILL, c.FILM_EDGE),
        (410, "Film", c.FILM_FILL, c.FILM_EDGE),
        (570, "Task", c.TASK_FILL, c.TASK_EDGE),
    ]:
        parts.extend(item_circle(x, 650, label, fill, edge))
    parts.extend(
        [
            c.line(367, 507, 133, 628, c.RED, 4, marker="arrow-red"),
            c.line(377, 520, 283, 616, c.RED, 4, marker="arrow-red"),
            c.line(410, 533, 410, 595, c.RED, 4, marker="arrow-red"),
            c.line(443, 520, 537, 616, c.RED, 4, marker="arrow-red"),
            c.multiline(
                642,
                586,
                ["Film context cues", "film and task items"],
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
            defs(),
            f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
            *panel_a(),
            "</svg>",
        ]
    )


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_y.svg"
    png_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_y.png"
    pdf_path = FIGURE_DIR / "simulation4_retrieval_routes_panel_candidate_y.pdf"
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
