"""Draw Figure 7 from preserved recognition evidence, without running simulations."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/selective-interference-mpl")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "recognition_evidence.csv"
PROVENANCE = HERE / "provenance.json"
WIDTH, HEIGHT = 1680, 780
INK = "#111111"
SLATE = "#3D4B5C"
BLUE = "#1764D8"
ORANGE = "#D96B2B"
GREEN = "#178A4C"
RED = "#A83232"
CONTEXT = "#EEF3F8"
FILM = "#EAF2FF"
TASK = "#FFF0E6"


def main(layout="input-top-muted"):
    provenance = json.loads(PROVENANCE.read_text())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == provenance["data_sha256"]
    with DATA.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    keys = [(reminder, task) for reminder in ("No reminder", "With reminder")
            for task in ("Weak task encoding", "Strong task encoding")]
    assert [(r["reminder_condition"], r["task_condition"]) for r in rows] == keys
    assert all(r["metric"] == "mfc_current_context_evidence_separation" for r in rows)
    values = [float(r["value"]) for r in rows]
    assert all(0 <= value <= 0.8 for value in values)
    for row in rows:
        assert float(row["recognition_cue_reinstatement"]) == 0.9
        assert float(row["recognition_temporal_weight"]) == 1
        assert float(row["recognition_source_weight"]) == 1
        assert int(row["n_foils"]) == 16

    plt.rcParams.update({"font.family": "Arial", "font.size": 20,
                         "svg.fonttype": "none", "pdf.fonttype": 42,
                         "svg.hashsalt": "recognition-compact-figure"})
    fig = plt.figure(figsize=(14, HEIGHT / 120), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, WIDTH), ylim=(HEIGHT, 0))
    ax.set_axis_off()
    node_labels = []

    def text(x, y, value, size=20, weight="normal", color=INK, ha="center"):
        return ax.text(x, y, value, fontsize=size, fontweight=weight, color=color,
                       ha=ha, va="center", linespacing=1.12)

    def box(x, y, w, h, label, fill=CONTEXT, edge=SLATE, size=20):
        patch = FancyBboxPatch((x, y), w, h,
                     boxstyle="round,pad=0,rounding_size=13", linewidth=1.8,
                     edgecolor=edge, facecolor=fill, zorder=2)
        ax.add_patch(patch)
        label_artist = text(x + w / 2, y + h / 2, label, size=size, weight="bold")
        node_labels.append((patch, label_artist))

    def arrow(start, end, color=SLATE, connection="arc3,rad=0"):
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>",
                     mutation_scale=16, linewidth=1.9, color=color,
                     connectionstyle=connection, shrinkA=2, shrinkB=3, zorder=3))

    def node(x, y, label, fill, edge, active=False, radius=34, muted=False):
        if muted:
            fill = tuple(0.5 + 0.5 * c for c in matplotlib.colors.to_rgb(fill))
            edge = tuple(0.6 + 0.4 * c for c in matplotlib.colors.to_rgb(edge))
        patch = Circle((x, y), radius, facecolor=fill, edgecolor=edge,
                       linewidth=1.2 if muted else (2.6 if active else 1.6), zorder=4)
        ax.add_patch(patch)
        label_artist = text(x, y, label, size=15,
                            weight="normal" if muted else "bold",
                            color="#858C94" if muted else INK)
        label_artist.set_zorder(5)
        node_labels.append((patch, label_artist))

    def node_arrow(start, end, color):
        dx, dy = end[0] - start[0], end[1] - start[1]
        distance = math.hypot(dx, dy)
        arrow((start[0] + 34 * dx / distance, start[1] + 34 * dy / distance),
              (end[0] - 34 * dx / distance, end[1] - 34 * dy / distance), color)

    def network(context_y, item_y, recognition=False):
        xs = (290, 460, 630, 800)
        for i, x in enumerate(xs):
            node(x, context_y, f"C{i+1}", CONTEXT, SLATE,
                 active=not recognition and i == 2)
            node(x, item_y, "Task" if i == 3 else "Film",
                 TASK if i == 3 else FILM, ORANGE if i == 3 else BLUE,
                 active=recognition and i == 1)
            if recognition:
                node_arrow((xs[1], item_y), (x, context_y), GREEN)
            else:
                node_arrow((xs[2], context_y), (x, item_y), RED)

    def frame(y, height, color):
        ax.add_patch(FancyBboxPatch((45, y), 840, height,
                     boxstyle="round,pad=0,rounding_size=16",
                     edgecolor=color, facecolor="none", linewidth=1.5))

    text(34, 42, "A", size=26, weight="bold", ha="left")
    text(445, 42, "Recall and recognition", size=22, weight="bold")
    text(990, 42, "B", size=26, weight="bold", ha="left")
    text(1335, 42, "Recognition evidence", size=22, weight="bold")

    if layout in ("input-top", "input-top-muted"):
        # Both operations begin with their retrieval input on the upper row.
        for offset, recognition, color, heading in [
            (0, False, RED, "Recall: context-to-item retrieval"),
            (320, True, GREEN, "Recognition: item-to-context retrieval"),
        ]:
            text(45, 100 + offset, heading, size=19, weight="bold", color=color, ha="left")
            frame(125 + offset, 270, color)
            text(63, 197 + offset,
                 "Presented\nprobe" if recognition else "Film-associated\ncontext",
                 size=15, ha="left")
            text(63, 322 + offset,
                 "Retrieved\ncontext" if recognition else "Competing\ncandidates",
                 size=15, ha="left")
            if recognition:
                probe_x = 460 if layout == "input-top-muted" else 545
                if layout == "input-top":
                    node(probe_x, 197 + offset, "Film", FILM, BLUE, active=True)
                for i, x in enumerate((290, 460, 630, 800)):
                    if layout == "input-top-muted":
                        node(x, 197 + offset, "Task" if i == 3 else "Film",
                             TASK if i == 3 else FILM, ORANGE if i == 3 else BLUE,
                             active=i == 1, muted=i != 1)
                    node(x, 322 + offset, f"C{i+1}", CONTEXT, SLATE)
                    node_arrow((probe_x, 197 + offset), (x, 322 + offset), GREEN)
            else:
                network(197 + offset, 322 + offset)
    elif layout == "nodes":
        # Keep the same nodes in place so the reversed retrieval direction is visible.
        for offset, recognition, color, heading, cue in [
            (0, False, RED, "Recall: context-to-item retrieval", "Cue: current context"),
            (320, True, GREEN, "Recognition: item-to-context retrieval", "Cue: presented probe"),
        ]:
            text(45, 100 + offset, heading, size=19, weight="bold", color=color, ha="left")
            frame(125 + offset, 270, color)
            text(63, 190 + offset,
                 "Retrieved\ncontext" if recognition else "Film-associated\ncontext",
                 size=15, ha="left")
            text(63, 300 + offset, "Items" if recognition else "Competing\ncandidates",
                 size=15, ha="left")
            network(190 + offset, 300 + offset, recognition=recognition)
            text(545, 363 + offset, cue, size=15, weight="bold", color=color)
    else:
        # Recall: current context supports competing item candidates.
        text(45, 110, "Recall", size=21, weight="bold", ha="left")
        box(45, 177, 270, 104, "Film-associated\ncontext", size=19)
        box(400, 140, 230, 82, "Film\ncandidates", fill=FILM, edge=BLUE, size=19)
        box(400, 252, 230, 82, "Task\ncandidates", fill=TASK, edge=ORANGE, size=19)
        arrow((315, 229), (400, 181), RED)
        arrow((315, 229), (400, 293), RED)
        text(344, 125, "Cues", size=17, color=RED)
        ax.plot([656, 680, 680, 656], [155, 155, 319, 319], color=SLATE, lw=1.5)
        text(772, 237, "Compete\nfor recall", size=19, weight="bold")
        ax.plot([45, 866], [369, 369], color="#DCE3EA", lw=0.9)

        # Recognition: a supplied probe retrieves context for an evidence comparison.
        text(45, 415, "Recognition", size=21, weight="bold", ha="left")
        box(45, 474, 210, 108, "Presented\nprobe", fill=FILM, edge=BLUE)
        box(348, 474, 230, 108, "Associated\ncontext")
        box(348, 639, 230, 102, "Ongoing test\ncontext")
        box(665, 553, 225, 110, "Recognition\nevidence", fill="#F2F4F6", size=19)
        arrow((255, 528), (348, 528), GREEN)
        text(301, 451, "Retrieves", size=16, color=GREEN)
        arrow((578, 528), (665, 585))
        arrow((578, 690), (665, 631))
        text(778, 513, "Context match", size=18, weight="bold")

    # Same four saved evidence values and the same 0–0.8 scale as the old plot.
    plot = fig.add_axes([1060 / WIDTH, 130 / HEIGHT, 575 / WIDTH, 555 / HEIGHT])
    plot.set_ylim(0, 0.8)
    plot.set_xlim(-0.6, 1.6)
    plot.set_yticks([0, .2, .4, .6, .8])
    plot.set_yticklabels(["0.0", "0.2", "0.4", "0.6", "0.8"])
    plot.set_xticks([0, 1])
    plot.set_xticklabels(["Without pre-task\nfilm reminder", "With pre-task\nfilm reminder"],
                        fontsize=18, fontweight="bold")
    plot.set_ylabel("Old-film minus foil\nrecognition evidence", fontsize=19,
                    fontweight="bold", labelpad=17)
    plot.tick_params(axis="both", length=0, labelsize=18, pad=9)
    plot.spines[["top", "right"]].set_visible(False)
    for side in ("left", "bottom"):
        plot.spines[side].set_color(SLATE)
        plot.spines[side].set_linewidth(1.8)
    plot.grid(axis="y", color="#DCE3EA", linewidth=0.9)
    plot.set_axisbelow(True)
    bars = []
    for i, value in enumerate(values):
        group, strong = divmod(i, 2)
        bar = plot.bar(group + (-.16 if strong == 0 else .16), value, width=.25,
                       color="#F2F4F6" if strong == 0 else TASK,
                       edgecolor=SLATE if strong == 0 else ORANGE, linewidth=2)
        bars.append(bar[0])
    assert [b.get_height() for b in bars] == values
    legend = plot.legend(
        handles=[Rectangle((0, 0), 1, 1, facecolor=fill, edgecolor=edge,
                           linewidth=1.8, label=label)
                 for label, fill, edge in [
                     ("Weaker task associations", "#F2F4F6", SLATE),
                     ("Stronger task associations", TASK, ORANGE),
                 ]],
        loc="upper center", bbox_to_anchor=(0.5, 0.995), frameon=False,
        fontsize=18, handlelength=1.1, handletextpad=0.5,
        labelspacing=0.3, borderpad=0.25, borderaxespad=0.25,
    )

    # Ensure all labels fit their figure/axes bounds before exporting.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    legend_bounds = legend.get_window_extent(renderer)
    plot_bounds = plot.get_window_extent(renderer)
    assert abs((legend_bounds.x0 + legend_bounds.x1) / 2 -
               (plot_bounds.x0 + plot_bounds.x1) / 2) < 1
    assert plot_bounds.contains(legend_bounds.x0, legend_bounds.y0)
    assert plot_bounds.contains(legend_bounds.x1, legend_bounds.y1)
    assert legend_bounds.y0 > max(bar.get_window_extent(renderer).y1 for bar in bars)
    for patch, label in node_labels:
        outer = patch.get_window_extent(renderer)
        inner = label.get_window_extent(renderer)
        assert inner.x0 >= outer.x0+4 and inner.x1 <= outer.x1-4, label.get_text()
        assert inner.y0 >= outer.y0+4 and inner.y1 <= outer.y1-4, label.get_text()
    for artist in fig.findobj(matplotlib.text.Text):
        if not artist.get_text() or not artist.get_visible():
            continue
        b = artist.get_window_extent(renderer)
        assert b.x0 >= bounds.x0-1 and b.x1 <= bounds.x1+1, artist.get_text()
        assert b.y0 >= bounds.y0-1 and b.y1 <= bounds.y1+1, artist.get_text()

    stem = {"flow": "figure7_recognition", "nodes": "figure7_recognition_nodes",
            "input-top": "figure7_recognition_input_top",
            "input-top-muted": "figure7_recognition_input_top_muted"}[layout]
    for suffix in ("svg", "pdf", "png"):
        fig.savefig(HERE / f"{stem}.{suffix}", dpi=240, facecolor="white",
                    metadata={"Creator": "recognition_compact_figure/render_figure.py"}
                    if suffix == "pdf" else None)
    plt.close(fig)
    print("Exported SVG, PDF and PNG; all four bar values and label bounds verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", choices=("flow", "nodes", "input-top", "input-top-muted"),
                        default="input-top-muted")
    main(parser.parse_args().layout)
