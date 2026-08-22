# Simulation 2 control-parameter sensitivity

This is the reviewable analysis package for Rik Henson's parameter-robustness
query. It does not edit or regenerate the manuscript. Exact feedback and its
mapping to outputs are in `FEEDBACK_TRACE.md`; the frozen design and estimands
are in `analysis_spec.json` and `METHODS.md`.

## Run

From the repository root:

```bash
MPLCONFIGDIR=/tmp/selective-interference-mpl \
  .venv/bin/python \
  work/simulation2_control_parameter_sensitivity/run_parameter_sensitivity.py
```

The declared full run uses 5,000 trials in ten paired Monte Carlo batches for
every cell. Results are written to `results/`. The runner refuses to overwrite
an existing completed run unless `--overwrite` is supplied.

For a fast implementation check that does not touch the package outputs:

```bash
MPLCONFIGDIR=/tmp/selective-interference-mpl \
  .venv/bin/python \
  work/simulation2_control_parameter_sensitivity/run_parameter_sensitivity.py \
  --output-dir /tmp/sim2-control-sensitivity-smoke \
  --experiment-count 40 \
  --batch-count 2 \
  --beta-values 0,fitted,1 \
  --kappa-values 0,1 \
  --cue-boost-values 0,1
```

Verify an existing full run independently:

```bash
.venv/bin/python \
  work/simulation2_control_parameter_sensitivity/verify_results.py \
  work/simulation2_control_parameter_sensitivity/results
```

## Outputs

- `run_manifest.json`: source/data hashes, software versions, Git state, RNG
  design, command, and hashes of generated artifacts.
- `cell_manifest.csv`: every simulated model × experimental cell and its
  requested and realized parameters.
- `batch_summaries.csv`: the retained Monte Carlo-batch phase totals,
  positional summaries, and output-transition counts.
- `spc.csv`: full cell-level serial-position curves.
- `estimand_batches.csv`: primary and secondary contrasts recomputed within
  each paired batch.
- `estimand_summary.csv`: means and Monte Carlo intervals across batches.
- `representative_diagnostics.csv`: declared mechanism settings used for
  the diagnostic panels.
- `parameter_sensitivity.{png,svg,pdf}`: global surface, outcome-space tradeoff,
  input-position signature, and output-transition signature.
- `contrast_sensitivity.{png,svg,pdf}`: matched surfaces for the primary
  three-way contrast, protection within the reminder condition, and the
  low-to-high endpoint contrast used in the current decomposition figure.
- `robustness_summary.json` and `RESULTS.md`: machine-readable and concise
  prose summaries of the complete surface—never a tuned winner.
- `verification.json`: dimensional, identity, range, duplicate-anchor, and
  hash checks performed by the runner.

## Relation to prior work

The existing decomposition sweep evaluates a small set of on/off packages:
`work/simulation2_retrieval_control_decomposition/`. The earlier exploration
in `work/simulation2_control_cued_parameter_exploration/` samples a narrower
set of start/monitoring values and ranks candidates with a post-hoc weighted
score. Those files remain useful development provenance, but neither is the
evidential analysis for comment 316. This package replaces candidate ranking
with a frozen full-factorial surface and declared contrasts.
