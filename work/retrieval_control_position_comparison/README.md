# Retrieval-control position comparison

Status: Figures 10–11 selected in the manuscript as pending tracked replacements, 28 September 2026.
The live captions and Results wording are maintained only in `index.qmd`.
No manuscript output was refreshed during the initial integration.
Regular HTML and APA Word were subsequently refreshed on 29 September 2026.

Open [Figure 10](figure10_candidate.png), or use its [vector PDF](figure10_candidate.pdf) / [editable SVG](figure10_candidate.svg).
[Figure 11](figure11_monitoring_return.png) retains the return-to-film diagnostic as a single panel.
The [integration audit](../../notes/2026-09-28/rik-positional-figures-integration.md) records the feedback, interpretation and tracking decisions.

## What the figure compares

Three panels show recall probability across the full encoded sequence: film, break, task and filler, with 16 positions per phase.
Each panel adds one operation to the same no-control baseline: start-of-film reinstatement, maintained film-category cue, or retrieval monitoring.
The baseline curve is identical in all panels and both axes use the same scale throughout.
No fitted curve, smoothing, normalization or interpolation is applied to the 64 saved probabilities.

Every curve comes from the film-reminder plus stronger-task-association condition of the saved retrieval-control decomposition analysis.
Each setting has 5,000 simulated trials, with a weak film cue before the first recall and at four-attempt intervals thereafter.
The three deliberate-control operations are absent in the baseline; the weak film cues remain present in every condition.
These are aggregate saved probabilities; uncertainty intervals cannot be recovered from this file alone.

| Panel | Start reinstatement scale | Maintained film support | Non-film context updating scale |
|---|---:|---:|---:|
| Baseline | 0 | 0 | 1 |
| A: reinstatement alone | 1 | 0 | 1 |
| B: maintained cue alone | 0 | 1 | 1 |
| C: monitoring alone | 0 | 0 | 0 |

Reinstatement scale 1 uses the unscaled fitted retrieval-start rate; it is not a claim of complete reinstatement.
Monitoring uses the full suppression setting in the decomposition data: non-film samples do not update context.
This differs from the moderate monitoring setting described in the former Figure 11B caption, which also includes reinstatement.
We deliberately use the isolated conditions from one decomposition dataset rather than combine those two diagnostics.

## Feedback addressed

Rik's c355 asks to show positional effects of maintained cueing alongside reinstatement, instead of using both main panels for first versus any recall.
His c366 asks for plots over all positions for each mechanism.
This candidate follows that request literally, retaining task and filler positions rather than restricting the display to film positions.
It uses recall across the entire search as the common outcome.
The earlier first-recall diagnostic remains available in its original package; no existing figure has been deleted.

The comparison makes the early-position advantage of reinstatement visible and lets the maintained-cue and monitoring patterns be assessed alongside it.
Neither the maintained-cue nor the monitoring curve should be described as flat.
The output-order diagnostic remains relevant because input-position patterns alone need not uniquely distinguish the mechanisms.
This figure holds reminder and task conditions fixed, so it does not by itself establish protection from interference or the reminder-specific interaction.
Those claims depend on the preceding aggregate and sensitivity analyses.

The approved integration retains these decomposition strengths and removes the overlapping positional panel from the old Figure 11.
Figure 11 retains its output-order comparison, where reinstatement is present and monitoring strength varies.
No new simulation or parameter selection was performed to make the curves more distinctive.
Rik’s c355 and c366 are resolved in the manuscript; the wording and figure replacements remain pending for collaborator review.
c357 is also resolved.
The manuscript specifies the item identities, input positions and retrieval order needed for future tests; we decided not to add analyses of the collaborators’ existing experiments.

## Verification

All four conditions contain exactly 64 positions with matching reminder, task and weak-cue settings.
Only the selected control parameters vary, and the same baseline array is plotted in every panel.
All 16 derived phase totals agree with the independently saved phase-total table to within 0.0000001 items.
The PNG was checked for legibility, clipping, alignment and consistent axes.
The manuscript, frozen reference, rendered manuscript outputs and original simulation data were unchanged when the candidate was prepared.

## Files and reproduction

- `data/position_curves.csv`: preserved 256-row subset, with the original condition and parameter columns.
- `provenance.json`: source paths, source/subset checksums, selection rule and recorded versions.
- `render_candidate.py`: validates the subset, draws the three aligned panels, and exports PNG, SVG and PDF.
- `phase_summary.csv`: derived mean probabilities and expected item counts by phase, including differences from baseline.
- `caption.md`: historical caption proposal from the evaluation stage; the active caption is in `index.qmd`.
- `data/monitoring_return.csv`: five preserved transition-probability rows used for Figure 11.
- `monitoring_return_provenance.json`: the source path, selection and checksums for those rows.
- `render_monitoring_return.py`: verifies the conditional probabilities against counts and exports Figure 11 as PNG, SVG and PDF.

From the repository root:

```sh
MPLCONFIGDIR=/tmp/selective-interference-mpl .venv/bin/python -B work/retrieval_control_position_comparison/render_candidate.py
MPLCONFIGDIR=/tmp/selective-interference-mpl .venv/bin/python -B work/retrieval_control_position_comparison/render_monitoring_return.py
```

Rendering reads the preserved subset, not the live source CSV, so subsequent analysis work cannot silently change this candidate.
To use updated results, deliberately re-extract the four conditions and update their provenance before rendering.
The source CSV is `work/simulation2_retrieval_control_decomposition/simulation2_retrieval_control_decomposition_spc.csv`.
The recorded generator and fit-file checksums identify their state when the package was prepared; they do not independently prove the historical execution environment that produced the saved CSV.
