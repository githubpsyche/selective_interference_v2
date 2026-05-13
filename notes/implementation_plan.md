# 13. Ordered work plan

## Phase 1: One-page concept memo

Write one page containing:

* title;
* one-sentence contract;
* three governing quantities;
* in-scope and out-of-scope lists;
* the three main simulations;
* main expected payoff.

Stop after one page.

## Phase 2: Predefine simulation success criteria

Before tuning, define:

* what counts as reduced intrusion-like sampling;
* what counts as voluntary sparing;
* what counts as reminder dependence;
* what counts as overlap dependence;
* what counts as acceptable robustness;
* what counts as unacceptable brittleness.

This is the anti-parameter-chasing safeguard.

## Phase 3: Build unified simulation pipeline

One codebase should run all conditions from a shared parameter file.

Minimum outputs:

* condition-level summary table;
* core dissociation plot;
* boundary-condition plot;
* cue-precision plot;
* robustness/ablation plot;
* seed and parameter log.

Do not tune each simulation independently.

## Phase 4: Run diagnostic temporal-only baseline

Run this first internally.

Decision gate:

* If temporal-only is recency-biased, source context is necessary.
* If temporal-only works broadly, source context is an extension for task specificity.
* If temporal-only is unstable, emphasize constraints.

## Phase 5: Implement final temporal/source model

Implement the model that will appear in the main paper.

Do not finalize prose until this model can produce the core conditions.

## Phase 6: Run main Simulation 1

Core selective-interference dissociation.

Decision gate:

* If it fails, do not proceed to writing.
* If it works only under narrow settings, mark the paper as a constraints paper.
* If it works across plausible settings, proceed.

## Phase 7: Run main Simulation 2

Reminder × overlap × competitor strength.

Decision gate:

* If reminder/overlap do not matter, the theoretical mechanism is not supported.
* If they matter only through arbitrary parameter choices, weaken the claim.
* If they matter robustly, this becomes the main boundary-condition result.

## Phase 8: Run main Simulation 3

Cue precision gradient.

Decision gate:

* If cue precision changes vulnerability, keep recognition/test-format payoff central.
* If not, demote test-format claims and keep only the core dissociation/boundary-condition story.

## Phase 9: Run compact robustness and ablations

At minimum:

* source context ablation;
* reminder ablation;
* overlap × strength sweep;
* cue precision sweep;
* temporal drift sensitivity.

Decision gate:

* robust → positive account;
* constrained → boundary-condition account;
* brittle → constraint analysis.

## Phase 10: Draft results before introduction

Write the simulation sections first using this template:

1. Question.
2. Design.
3. Prediction.
4. Result.
5. Interpretation.
6. Constraint or next step.

This prevents the introduction from promising results the model does not deliver.

## Phase 11: Draft Sections 1–3

Write the Introduction, empirical target, and conceptual account using the actual simulation outcomes.

Keep the introduction short and disciplined.

## Phase 12: Draft Formal Model

Write only what the reader needs for the main simulations.

Move details to supplement if they interrupt the argument.

## Phase 13: Draft Discussion

Use the results-dependent claim strength.

Do not write the discussion as if the strongest possible version succeeded unless it did.

## Phase 14: PB&R pass

Before calling it a complete draft, check:

* Is the paper theory-led?
* Are the simulations serving boundary-condition questions?
* Is the model readable without deep CMR knowledge?
* Are clinical claims limited?
* Is recognition framed as cue precision?
* Is source context motivated rather than patched in?
* Are robustness/ablation results visible?
* Is the code-sharing plan ready?

---

