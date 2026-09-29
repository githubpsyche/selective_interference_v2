"""Export the retained output-order diagnostic as a single-panel Figure 11.

Uses preserved aggregate results; does not rerun simulations or touch the manuscript.
"""

from pathlib import Path
import csv
import hashlib
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


PACKAGE = Path(__file__).resolve().parent


def main() -> None:
    path = PACKAGE / "data" / "monitoring_return.csv"
    provenance = json.loads((PACKAGE / "monitoring_return_provenance.json").read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == provenance["selected_data_sha256"]
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda r: 1 - float(r["rejected_recall_drift_scale"]))
    strength = np.array([1 - float(r["rejected_recall_drift_scale"]) for r in rows])
    probability = np.array([float(r["film_return_probability"]) for r in rows])
    assert np.array_equal(strength, [0, .25, .5, .75, 1])
    for row in rows:
        assert float(row["start_drift_scale"]) == 1
        assert row["reminder_condition"] == "With reminder"
        assert float(row["task_mcf_scale"]) == 2
        assert float(row["film_cue_reinstatement"]) == .9
        assert int(row["first_cue_after"]) == 0
        assert abs(int(row["film_return_count"]) / int(row["transition_count"])
                   - float(row["film_return_probability"])) < 1e-12
    assert ((probability >= 0) & (probability <= 1)).all()
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 10,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "savefig.facecolor": "white",
    })
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(strength, probability, color="#161A1F", marker="o", lw=1.8, ms=4.8)
    ax.set(xlim=(-.025, 1.025), ylim=(0, .65))
    ax.set_xticks(strength, ["0", "0.25", "0.5", "0.75", "1"])
    ax.set_yticks([0, .2, .4, .6])
    ax.set_xlabel("Retrieval monitoring strength", fontsize=11, labelpad=8)
    ax.set_ylabel("Probability next output is film", fontsize=11, labelpad=8)
    ax.set_title("Return to film after a non-film sample", fontsize=11,
                 fontweight="bold", pad=13)
    ax.grid(axis="y", color="#DDE3EA", lw=.55)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#65717D")
    ax.tick_params(labelsize=9.5, color="#65717D")
    fig.subplots_adjust(left=.11, right=.98, top=.86, bottom=.19)
    for suffix in ("png", "svg", "pdf"):
        fig.savefig(PACKAGE / f"figure11_monitoring_return.{suffix}", dpi=300)
    plt.close(fig)
    print("Five saved transition probabilities verified against their counts; exported Figure 11.")


if __name__ == "__main__":
    main()
