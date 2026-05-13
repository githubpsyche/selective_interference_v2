# 9. Main-text simulation package

This is the revised **minimum viable PB&R package**.

## Figure 2 / Simulation 1: Core selective-interference dissociation

### Question

Can the final single-system model produce stronger impairment for intrusion-like retrieval than for target-cued/probe-specific voluntary retrieval?

### Minimal design

Compare:

* no or weak interference;
* strong overlapping interference.

Retrieval modes:

* unguided/contextual sampling;
* directed or probe-specific voluntary retrieval.

### Primary measures

* trauma-film item sampling probability or expected count;
* impairment relative to no-interference baseline;
* optionally, competitor capture.

### Predicted pattern

The same interference manipulation should suppress unguided trauma-item sampling more than target-cued/probe-specific retrieval.

### Interpretation

This is the core sufficiency result.

---

## Figure 3 / Simulation 2: Boundary conditions — reminder, overlap, and competitor strength

### Question

When does interference work?

### Minimal design

Compact factorial manipulation:

* reminder absent vs present;
* low vs high source overlap;
* weak vs strong competitor encoding.

### Primary measures

* intrusion-like film sampling;
* competitor capture;
* impairment relative to baseline.

### Predicted pattern

The strongest effect occurs when strong, high-overlap competitors are encoded after reminder-driven reinstatement.

### Interpretation

This shows that the model is not merely adding generic post-film distraction. Interference depends on reinstatement, overlap, and competitor strength.

---

## Figure 4 / Simulation 3: Cue precision and test-format variation

### Question

When does the intrusion/voluntary-memory dissociation appear sharp, weak, or blurred?

### Minimal design

Use three or four anchor points on a cue-precision continuum.

Recommended anchors:

1. **Unguided sampling**
   Intrusion-like retrieval.

2. **Directed recall-like search**
   Voluntary retrieval with some target orientation but still dependent on context-to-item competition.

3. **Probe-specific retrieval**
   Recognition-like or strongly cued retrieval.

4. **Optional: source/associative test**
   A voluntary test that depends on contextual/source retrieval, included only if it clarifies the recognition issue.

### Primary measures

* interference effect by retrieval mode;
* relative impairment across cue precision.

### Predicted pattern

The dissociation is strongest when intrusion-like retrieval is broad and voluntary retrieval is probe-specific. It narrows when voluntary retrieval depends more heavily on broad contextual/source search or when intrusion-like tasks provide strong cues.

### Interpretation

This is the recognition/test-phase payoff, without over-modeling every experimental task.

---

## Figure 5 or supplement: Compact robustness and ablation evidence

### Question

Is the result hand-tuned?

### Minimum required analyses

At minimum, test:

* source context present vs absent;
* reminder present vs absent;
* overlap × competitor strength sweep;
* cue precision sensitivity;
* temporal drift sensitivity.

### Primary output

A compact robustness map or criterion table:

| Criterion                     | Proportion/region of parameter space satisfying it |
| ----------------------------- | -------------------------------------------------- |
| selective unguided impairment | ...                                                |
| reminder dependence           | ...                                                |
| overlap dependence            | ...                                                |
| cue-precision gradient        | ...                                                |

### Interpretation rules

If broad:

> The qualitative pattern is robust across plausible parameter regions.

If narrow:

> The account is viable under identifiable constraints.

If brittle:

> The model is best treated as a constraint analysis rather than a strong positive account.

---

# 10. Required diagnostics and optional backlog

## Bucket A: Must appear in main text

* mechanism schematic;
* core dissociation simulation;
* reminder/overlap/competitor-strength boundary condition;
* cue-precision gradient;
* concise robustness or ablation statement.

## Bucket B: Must be run, but may be supplementary

* temporal-only baseline;
* source-context ablation;
* reminder ablation;
* temporal drift sensitivity;
* overlap × competitor-strength sweep;
* cue-precision sensitivity.

## Bucket C: Optional backlog

Do not include in v1 unless results force it.

* detailed vigilance-intrusion task implementation;
* separate diary, VIT, free recall, cued recall, item recognition, source recognition models;
* extensive clinical intervention simulations;
* symptom/distress/vividness modeling;
* full emotional-arousal versus visuospatial-source model comparison;
* individual-difference theory;
* detailed serial-position predictions beyond what is needed to diagnose temporal/source context.

---

# 11. Temporal-only baseline policy

The temporal-only baseline is required for model development, but not automatically a main-text simulation.

## Why run it

It answers:

> Does temporal context alone produce the effect, and if so, does it overpredict interference with late film items?

## How to use it

* If temporal-only results are informative but secondary, place them in the supplement.
* If temporal-only results reveal a major limitation that source context solves, mention them briefly in the main text and show a compact inset or supplementary figure.
* If temporal-only results work robustly, source context becomes a task-overlap extension rather than a required fix.

## Do not present the manuscript as

> We tried temporal context, it failed, then we patched the model with source context.

Present source context as theoretically motivated from the start.

---

