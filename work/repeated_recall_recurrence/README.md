# Repeated-recall recurrence pilot

This isolated work package asks whether the modeled selective-interference
effect changes when film retrieval is scored as:

- total film retrieval events;
- unique film items retrieved at least once; or
- repeated film retrieval events (`total - unique`).

The project model already supports this pilot. When
`allow_repeated_recalls=True`, a retrieved item remains available for later
sampling in the same retrieval sequence. No shared model or analysis code is
changed here.

## Scope

This is a **within-retrieval-sequence** recurrence model. It can reveal whether
the existing dynamics produce recurrence, concentration on a few film items,
or immediate self-repetition. It is not yet a model of diary intrusions across
hours or days, because it does not introduce separate retrieval episodes,
changing external triggers, or a refractory period between episodes.

The package computes recurrence metrics directly from raw recall sequences.
Auditing or adapting the repository's conventional SPC/CRP analysis functions
for repeated outputs is deliberately deferred as a separate work step.

## Design

The runner crosses:

- repeated recalls disabled versus enabled;
- unguided versus full deliberate retrieval control;
- no reminder versus film reminder; and
- weak versus strong task encoding.

All other settings match the current Simulation 2 behavioral anchor. Common
random-number streams are reused across cells. The primary descriptive
quantity is the reminder-specific task cost for each scoring metric:

`(reminder weak - reminder strong) - (no-reminder weak - no-reminder strong)`

The package also reports the difference in that quantity between unguided and
deliberate retrieval.

## Run

From the repository root:

```bash
MPLCONFIGDIR=/tmp/selective-interference-mpl \
  .venv/bin/python \
  work/repeated_recall_recurrence/run_repeated_recall_recurrence.py
```

Fast smoke run without touching the package results:

```bash
MPLCONFIGDIR=/tmp/selective-interference-mpl \
  .venv/bin/python \
  work/repeated_recall_recurrence/run_repeated_recall_recurrence.py \
  --output-dir /tmp/repeated-recall-recurrence-smoke \
  --experiment-count 40 \
  --batch-count 2 \
  --overwrite
```

## Outputs

- `batch_metrics.csv`: recurrence summaries for every model cell and Monte
  Carlo batch.
- `cell_summary.csv`: cell means and Monte Carlo intervals.
- `contrast_batches.csv` and `contrast_summary.csv`: total-versus-unique
  selective-interference contrasts.
- `example_sequences.csv`: a small audit sample of raw output sequences.
- `recurrence_summary.{png,svg}`: recurrence composition and metric-dependent
  task effects.
- `run_manifest.json`: settings and invariant checks.
- `RESULTS.md`: concise machine-generated interpretation of the run.

