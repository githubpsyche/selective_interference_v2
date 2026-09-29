# Compact recognition figure

Status: selected as a pending Figure 7 replacement, 28 September 2026.
The active caption and review decisions are maintained in the root `index.qmd`.

Open [the figure](figure7_recognition_input_top_muted.png), [vector PDF](figure7_recognition_input_top_muted.pdf) or [editable SVG](figure7_recognition_input_top_muted.svg).
The figure responds to the agreed reduction of recognition's visual emphasis following c368.
Panel A compares context-to-item retrieval in recall with item-to-context retrieval in recognition, with the retrieval input on the top row in both diagrams.
The supplied recognition probe is emphasized while the other stored items remain visible but muted.
Panel B retains the original four recognition-evidence conditions and the 0–0.8 axis range.
Its two-row legend is centered inside the upper plotting area, above the bars.
The repeated architecture panel, separate context-match flowchart and categorical “no reduction” bracket are omitted.
The caption retains the explanation of how recognition evidence is calculated.
No simulation, parameter setting or numerical result was changed.

## Selected version with other item representations retained

[Preview](figure7_recognition_input_top_muted.png), [vector PDF](figure7_recognition_input_top_muted.pdf) and [editable SVG](figure7_recognition_input_top_muted.svg).
This version preserves the input-on-top layout and restores the other film and task representations in recognition.
Only the supplied film probe has full-strength styling and outgoing arrows; other items retain readable muted labels, pale fills and thin coloured outlines.
The context components below remain fully visible, and Panel B is unchanged.
The manuscript selects this version within pending suggestion s448.
Its caption explains the context components, heavier outlines and faded items in a separate pending insertion.
Render with `.venv/bin/python -B work/recognition_compact_figure/render_figure.py --layout input-top-muted`.

## Earlier candidate with retrieval input on top

[Preview](figure7_recognition_input_top.png), [vector PDF](figure7_recognition_input_top.pdf) and [editable SVG](figure7_recognition_input_top.svg).
This earlier candidate is retained for comparison and is not selected in the manuscript.
Both diagrams place the retrieval input on the upper row and the activated candidates or context below.
Recognition shows one supplied film item, labelled by the row heading “Presented probe.”
Frame dimensions, node spacing and heading typography match across the diagrams, with no extra cue labels or context-match flowchart.
Panel B preserves the previous evidence plot and centered legend.
Render with `.venv/bin/python -B work/recognition_compact_figure/render_figure.py --layout input-top`.

## Earlier node-based candidate

[Preview](figure7_recognition_nodes.png), [vector PDF](figure7_recognition_nodes.pdf) and [editable SVG](figure7_recognition_nodes.svg).
This earlier alternative is retained for comparison and is not selected in the manuscript.
Panel A keeps context and item nodes in the same positions across recall and recognition, with explicit context-to-item and item-to-context retrieval labels.
It identifies the presented film probe and retains the task node in both diagrams.
The context-match flowchart has been removed to give the two retrieval diagrams more vertical space.
The diagrams use equal frame heights, identical node spacing, matching cue labels and a uniform heading style.
Panel B is unchanged from the previous candidate, including its centered legend.
Render this alternative with `.venv/bin/python -B work/recognition_compact_figure/render_figure.py --layout nodes`.

The first [flowchart candidate](figure7_recognition.png) is also retained for comparison and can be reproduced with `--layout flow`.

## Data and checks

`data/recognition_evidence.csv` preserves the four evidence-separation rows from `work/simulation3_recognition_test_format/simulation3_recognition_test_format_recognition_summary.csv`.
The metric is mean old-film evidence minus mean evidence for film-source-matched foils, not recognition accuracy.
The extraction checks each difference against its old-item and foil means and verifies that these values reproduce the earlier composite SVG's bar heights within its 0.1-pixel rounding.
`provenance.json` records source and subset hashes, the original manuscript image, the earlier SVG and the selection rule.
The original Word-imported image is retained for rejection and review history; the new figure is a redraw, not an exact reproduction of that PNG.

The renderer validates the frozen subset and plots its values without rounding, scaling, smoothing or normalization.
It also checks that text fits its boxes and the overall figure bounds.
The exported PNG was inspected for legibility, arrow direction, clipping and overlaps before selection.
Existing schematic colours, typography and bar styles are retained.

## Reproduce

From the repository root:

```sh
MPLCONFIGDIR=/tmp/selective-interference-mpl .venv/bin/python -B work/recognition_compact_figure/render_figure.py
```

This writes PNG, SVG and PDF figure exports only.
It neither runs simulations nor renders the manuscript.
To adopt different simulation results, deliberately replace the preserved subset and update its provenance first.
