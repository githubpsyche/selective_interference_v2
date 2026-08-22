# Parameter-sensitivity methodology

## Purpose and claim boundary

This analysis tests the narrow robustness claim raised in Rik Henson's comment
316: whether start-of-film reinstatement and retrieval monitoring remain
insufficient when their settings are varied, with the maintained category cue
disabled. It is a global finite-grid sensitivity analysis, not a parameter fit.

The phrase “all parameter settings” is operationalized as a Cartesian grid
covering both mechanisms' complete admissible domains at increments of 0.1,
plus the exact fitted start-drift value used by the manuscript. Conclusions
must therefore be phrased as “across the evaluated grid under the fixed fitted
base regime,” not as a proof over every real-valued point or every possible
CMR parameterization.

## Fixed model and experimental design

The analysis loads the same independent eCMR fit used in the manuscript and
retains its fixed paradigm: 16 film, 16 break, 16 task, and 16 filler items,
followed by at most 48 retrieval attempts. Film items are emotional and task
items are neutral. The encoding design crosses:

- no reminder versus a pre-task film reminder; and
- weak versus strong task-to-context learning.

All four cells are simulated for every retrieval-control configuration. Weak
periodic film cues are held identical across cells and mechanisms. These
external probes are distinct from the maintained film-category cue, which is
disabled throughout the primary grid.

## Mechanism parameterization

Start reinstatement is varied in terms of the **realized** start drift,
`beta_start_effective`, from 0 to 1. The model API accepts a multiplier of the
fitted start drift; the runner converts each desired realized value into that
multiplier and verifies the value present in the configured model. This avoids
mistaking an implementation scale factor for the psychologically interpreted
drift parameter.

Monitoring is varied through `kappa`, the fraction of the ordinary context
update retained after a sampled non-film item. `kappa = 1` means no monitoring;
`kappa = 0` is maximal monitoring. Plots use `1 - kappa` when labeling
monitoring strength.

The primary `no_category_grid` crosses all declared start-drift and kappa
values with category support fixed to zero. Two outcome-space comparators then
vary category support from 0 to 1: category cue alone, and category cue added
to the manuscript's fitted start drift plus maximal monitoring. These curves
are comparators, not fitted alternatives.

## Estimands

Let `Y[c, r, t]` denote mean film items recalled under control configuration
`c`, reminder condition `r`, and task strength `t`. Define the task-encoding
cost under each reminder condition:

`D[c, r] = Y[c, r, weak] - Y[c, r, strong]`.

The sensitivity of retrieval configuration `c` to reminder-linked competitor
encoding is:

`S[c] = D[c, with reminder] - D[c, no reminder]`.

The primary selective-protection estimand is:

`P[c] = S[unguided] - S[c]`.

This is the retrieval-control × reminder × task contrast. Positive values mean
the candidate control reduces the reminder-specific task cost relative to the
no-control retrieval baseline. The package also reports protection within
each reminder condition. Two secondary contrasts preserve direct continuity
with the existing manuscript figures:

- endpoint loss: `L[c] = Y[c, no reminder, weak] - Y[c, with reminder,
  strong]`;
- endpoint protection: `L[unguided] - L[c]`.

Endpoint protection asks whether a mechanism shrinks the low-to-high loss in
the current control-decomposition figure. It does **not** isolate the
reminder-specific interaction: a mechanism can improve this contrast by
altering both reminder conditions or by broadly raising recall. Therefore a
positive endpoint or within-reminder contrast is reported as technical
protection, not as the selective-interference effect, unless the primary
three-way contrast is also positive.

The package also reports two level effects:

- generic gain: `Y[c, no reminder, weak] - Y[unguided, no reminder, weak]`;
- high-interference gain: `Y[c, with reminder, strong] - Y[unguided, with
  reminder, strong]`.

Protection and generic gain remain separate. There is no weighted score,
post-hoc pass threshold, or search for a visually preferred parameter setting.

## Monte Carlo design and uncertainty

Each cell contains 5,000 simulated trials divided into ten independently keyed
batches. The same batch keys are reused in every experimental and parameter
cell (common random numbers), making all contrasts paired and reducing Monte
Carlo noise without changing expected values. Batch-level summaries are
retained. Two-sided 95% Student-t intervals are computed over the ten paired
batch estimands. They quantify simulation error only; they are not confidence
intervals for participant data or fitted parameter uncertainty.

## Mechanism signatures

The package retains full input-position recall curves. Start reinstatement is
additionally summarized over early (film positions 1–5), middle (6–11), and
late (12–16) positions. Monitoring is summarized by the probability that the
next nonzero output is a film item given that the current output is non-film
and retrieval continues. Numerator and denominator counts are retained for
audit.

These diagnostics answer a different question from the global outcome
surface. A mechanism may fail to produce the target three-way contrast while
still produce its predicted sequence signature, and multiple mechanisms may
operate simultaneously.

## Reproducibility records

The run manifest records the fit, specification, runner, and model-source
hashes; Git revision and dirty-state paths; package versions; realized
parameters; command-line overrides; and hashes of every generated result. A
separate verifier recomputes the primary estimands from batch summaries and
checks duplicate comparator anchors against the primary grid.
