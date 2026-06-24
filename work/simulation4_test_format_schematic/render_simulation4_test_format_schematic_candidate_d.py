from __future__ import annotations

import importlib.util
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
SOURCE = Path(__file__).with_name("render_simulation4_test_format_schematic_candidate_c.py")

spec = importlib.util.spec_from_file_location("candidate_c", SOURCE)
candidate_c = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(candidate_c)


def render_svg() -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{candidate_c.WIDTH}" height="{candidate_c.HEIGHT}" viewBox="0 0 {candidate_c.WIDTH} {candidate_c.HEIGHT}">',
        candidate_c.defs(),
        '<rect width="100%" height="100%" fill="white"/>',
        candidate_c.text(50, 65, "A", candidate_c.PANEL_SIZE, weight="bold", anchor="start"),
        candidate_c.text(
            112,
            68,
            "Supplied-probe recognition decision",
            candidate_c.TITLE_SIZE,
            weight="bold",
            anchor="start",
        ),
        candidate_c.text(
            765,
            122,
            "The item is given; old/new evidence comes from how its reinstated context matches test context",
            candidate_c.LABEL_SIZE,
            weight="bold",
        ),
    ]
    parts.extend(
        candidate_c.row(
            300,
            "Old film probe",
            "Film\nitem",
            candidate_c.FILM_FILL,
            candidate_c.FILM_EDGE,
            "Studied temporal trace\n+ film source",
            "High old\nevidence",
            candidate_c.FILM_EDGE,
        )
    )
    parts.extend(
        candidate_c.row(
            625,
            "Film-like foil",
            "Film-like\nfoil",
            candidate_c.FOIL_FILL,
            candidate_c.FOIL_EDGE,
            "Film source only\nno studied temporal trace",
            "Lower old\nevidence",
            candidate_c.FOIL_EDGE,
        )
    )
    parts.append(
        candidate_c.multiline(
            1295,
            760,
            "Task items can be\nsearch competitors\nwithout being probes",
            candidate_c.SMALL_SIZE,
            line_height=22,
            fill=candidate_c.TASK_EDGE,
        )
    )
    parts.extend(candidate_c.item(1290, 440, "Task", candidate_c.TASK_FILL, candidate_c.TASK_EDGE))
    parts.extend(candidate_c.item(1380, 510, "Task", candidate_c.TASK_FILL, candidate_c.TASK_EDGE))
    parts.append(
        candidate_c.line(
            1250,
            535,
            1090,
            612,
            candidate_c.TASK_EDGE,
            candidate_c.THIN,
            marker="",
            extra='stroke-dasharray="7 8"',
        )
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    svg_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_d.svg"
    png_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_d.png"
    pdf_path = FIGURE_DIR / "simulation4_test_format_schematic_candidate_d.pdf"
    for path_ in [svg_path, png_path, pdf_path]:
        if path_.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {path_}")
    svg_path.write_text(render_svg())
    env = os.environ.copy()
    env.setdefault("GDK_BACKEND", candidate_c.INKSCAPE_GDK_BACKEND)
    subprocess.run(
        [str(candidate_c.INKSCAPE), str(svg_path), f"--export-filename={png_path}"],
        check=True,
        env=env,
    )
    subprocess.run(
        [str(candidate_c.INKSCAPE), str(svg_path), f"--export-filename={pdf_path}"],
        check=True,
        env=env,
    )
    print(svg_path)
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
