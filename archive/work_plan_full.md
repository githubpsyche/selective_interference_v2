# PB&R-first paper contract, updated v2

This is the contract for the **first complete manuscript draft**. It is designed to keep the paper ambitious enough to matter, but compact enough to finish.

The operating target is:

> **A focused theoretical/modeling article for *Psychonomic Bulletin & Review* that develops a retrieved-context account of selective interference in intrusive memory, supported by simulations that test the core mechanism, boundary conditions, and test-format implications.**

Not a Psychological Review expansion. Not a full clinical theory. Not a maximal model of every trauma-film result.

---

# 1. Target journals

## Primary target: *Psychonomic Bulletin & Review*

The v1 manuscript should be written for **PB&R Theoretical/Review**. PB&R’s author guidance says theoretical articles should propose a new theoretical treatment or modify an existing one, and that theoretical/review articles may include model simulations; papers relying on newly collected empirical data are not appropriate for that article format. This makes PB&R the best operational fit for a no-new-data theory paper with formal simulations. ([Springer][1])

**Implications for the paper**

The manuscript should be:

* theory-led, not methods-led;
* readable by cognitive psychologists who are not CMR specialists;
* centered on a clear cognitive-memory problem;
* supported by simulations, but not buried under implementation detail;
* explicit about boundary conditions and design implications.

The paper should not read like a technical note saying “CMR can simulate Tetris.” It should read like a theoretical article saying:

> The selective-interference dissociation can arise from competitive retrieval dynamics in a shared episodic system.

## Secondary target: *Journal of Memory and Language*

JML is the secondary target if the paper becomes more strongly centered on memory architecture and less on the intrusive-memory intervention literature. JML says it generally favors papers with multiple experiments, but also allows significant theoretical or computational papers without new experimental findings. ([ScienceDirect][2])

**Implications for the paper**

Even though PB&R is the primary target, the draft should satisfy the JML-compatible basics:

* simulations should be reproducible;
* code/model availability should be planned from the beginning;
* the memory-theory contribution should be clear without relying only on clinical importance;
* claims should be grounded in established empirical regularities rather than speculative clinical extrapolation.

## Not a v1 target: *Psychological Review*

Psychological Review remains an aspirational expansion target only after the PB&R draft exists and the simulations prove robust. Psychological Review publishes papers making important theoretical contributions across scientific psychology, but writing toward that bar from the start risks turning this into a much broader theory of intrusive memory, reconsolidation, PTSD, and voluntary/involuntary remembering. ([American Psychological Association][3])

Do not write the v1 draft for Psychological Review.

---

# 2. One-sentence paper contract

> The paper develops a retrieved-context account of selective interference, arguing that reduced intrusion-like retrieval with relatively preserved voluntary memory can arise when reminders reinstate trauma-film context, interference tasks encode competitors into overlapping temporal/source context, and later tests differ in retrieval cue precision.

This sentence is the spine. If a section, simulation, paragraph, or model component does not serve this sentence, it should be cut, moved to supplement, or deferred.

---

# 3. Core claim hierarchy

Use this hierarchy to calibrate how strongly to write.

## Level 1: Inference claim

Selective interference does **not by itself** require separate intrusive and voluntary memory traces.

## Level 2: Positive theoretical claim

A single retrieved-context system can produce selective interference when post-reminder interference changes the competitive structure of trauma-associated context.

## Level 3: Mechanistic claim

The effect depends on three quantities:

1. **Competitor strength**
   How strongly interference-task items are encoded and later compete for retrieval.

2. **Target–competitor overlap**
   How much interference items share temporal and source context with trauma-film items.

3. **Retrieval cue precision**
   How strongly the test constrains retrieval toward the film episode rather than relying on broad context-to-item sampling.

## Level 4: Design payoff

Some variation across experiments may reflect differences in test format. Diary intrusions, vigilance-intrusion tasks, free recall, cued recall, recognition, and associative/source tests differ in cue precision and therefore in vulnerability to contextual competitors.

---

# 4. Scope boundaries

## In scope

The v1 paper is about:

* trauma-film and selective-interference paradigms;
* reminder-driven context reinstatement;
* competitor encoding after reminder;
* temporal context and source context;
* intrusion-like retrieval as uncontrolled trauma-item sampling;
* voluntary memory as a family of test formats with different cue precision;
* boundary conditions for when selective interference should appear, weaken, or disappear;
* experiment-design implications.

## Out of scope

The v1 paper is **not** about:

* full PTSD or clinical treatment efficacy;
* distress, vividness, appraisals, avoidance, or symptom trajectories;
* all reconsolidation findings;
* all dual-representation theory;
* whether Tetris is clinically effective;
* individual differences in trauma vulnerability;
* a full computational model of the vigilance-intrusion task;
* a complete taxonomy of intrusive-memory phenomenology.

Clinical studies can motivate the importance of the problem, but the simulations target the controlled logic of selective-interference paradigms.

---

# 5. Non-negotiable writing constraints

## Constraint 1: The paper is about an inference problem

The target is not:

> Dual-representation theory is false.

The target is:

> The selective-interference dissociation is not uniquely diagnostic of separate intrusive and voluntary traces.

Critique the inference, not a caricature of the theory.

## Constraint 2: Separate empirical regularities from theoretical glosses

Keep this distinction visible:

* **Empirical regularity:** post-reminder interference can reduce later intrusions while voluntary memory is relatively preserved.
* **Theoretical gloss:** this happens because a sensory/intrusive trace is selectively disrupted.

The model challenges the gloss, not the existence of the empirical pattern.

## Constraint 3: Intrusions are modeled at the sampling level

Use language like:

> We model intrusion occurrence as the probability that trauma-film items are sampled during uncontrolled context-to-item retrieval.

Do not imply that the model explains distress, vividness, flashback phenomenology, appraisals, or clinical symptoms.

## Constraint 4: Source context is the main construct

Use **source context** as the umbrella term for non-temporal context dimensions, including arousal, visuospatial processing, imagery-like processing, task state, and film-source features.

Do not make “emotional context” the headline unless the simulations specifically require an emotional/arousal dimension. The cleaner claim is:

> Source context allows film-wide and task-specific competition that temporal context alone may not provide.

## Constraint 5: Do not make Tetris primitive

Avoid:

> Tetris works because it is Tetris.

Use:

> Tetris-like tasks are expected to be effective when they create strong competitors that overlap with trauma-film memories in relevant temporal/source dimensions.

## Constraint 6: Do not claim recognition immunity

Replace “recognition immunity” with **cue precision** or **probe specificity**.

The claim is conditional:

> Recognition-like tests are less vulnerable when item-specific probes bypass broad context-to-item competition, but associative/source recognition may be more vulnerable.

## Constraint 7: Every model component must serve one of three roles

A component stays in the main text only if it affects:

1. competitor strength;
2. target–competitor overlap;
3. retrieval cue precision.

Otherwise, move it to supplement or defer it.

## Constraint 8: Every simulation must answer a boundary-condition question

Do not simulate a parameter because it exists.

Each simulation should answer:

> Under what conditions should selective interference appear, weaken, disappear, or look different across test formats?

## Constraint 9: Results determine rhetorical strength

If the simulations are robust, write:

> The selective-interference pattern follows naturally from retrieved-context competition under these conditions.

If the simulations are constrained, write:

> A retrieved-context account is viable, but only under identifiable constraints.

If the simulations are brittle, write:

> The simulations identify constraints on any single-system retrieved-context explanation.

Do not promise more than the results support.

## Constraint 10: Keep the main paper compact

The main text should have approximately:

* 4 main simulation figures plus one optional compact robustness figure;
* 1 mechanism schematic;
* 1–2 conceptual tables;
* a supplement for technical details, large parameter tables, additional sweeps, and full ablations.

---

# 6. Working title

Use this as the default PB&R title:

> **A Retrieved-Context Account of Selective Interference in Intrusive Memory**

This is safer than “Selective Interference Without Separate Traces.” The stronger title can return only if the simulations are robust and the rhetoric warrants it.

Alternative subtitle if needed:

> **Contextual Competition, Cue Precision, and the Intrusion/Voluntary-Memory Dissociation**

---

# 7. Abstract skeleton

The abstract should have five moves.

## Move 1: Phenomenon

Post-encoding or post-reminder interference tasks can reduce later intrusive memories while leaving voluntary memory relatively preserved.

## Move 2: Inference problem

This selective-interference pattern has often been interpreted as evidence for separate intrusive and voluntary traces, or for selective disruption of a reactivated sensory trace.

## Move 3: Model proposal

The retrieved-context account says reminders reinstate trauma-film context, and interference tasks encode competitors into overlapping temporal/source context.

## Move 4: Simulation evidence

Simulations test whether this mechanism can produce stronger impairment of intrusion-like sampling than of target-cued voluntary retrieval, whether reminder/overlap/competitor strength determine the effect, and whether cue precision explains variation across test formats.

## Move 5: Conclusion

Selective interference is treated as a boundary condition on competitive retrieval from a shared episodic memory system, not as direct evidence for separate memory traces.

## Draft abstract placeholder

> Post-encoding and post-reminder interference tasks can reduce later intrusive memories while leaving voluntary memory relatively preserved. This selective-interference pattern has often been interpreted as evidence for separate intrusive and voluntary memory traces, or for selective disruption of a reactivated sensory trace. We develop a retrieved-context account in which reminders reinstate trauma-film context and subsequent interference encodes competitor episodes into overlapping temporal/source context. Later uncontrolled retrieval from nearby context is then less likely to sample trauma-film items, whereas voluntary retrieval is less vulnerable when tests provide target-specific cues or item-specific probes. Simulations examine the core dissociation, the joint effects of reminder reinstatement, source overlap, and competitor strength, and the way test-phase cue precision can sharpen or blur the intrusion/voluntary-memory dissociation. The account treats selective interference as a boundary condition on competitive retrieval from a shared episodic memory system rather than as direct evidence for separate memory traces.

Keep this provisional. After simulations, replace “Simulations examine” with the strongest defensible verb.

---

# 8. Manuscript outline

## Section 1. Introduction: The inference problem

### Job

Make the reader understand why the selective-interference effect matters theoretically.

### Skeleton

**Paragraph 1: Empirical phenomenon**
Introduce the selective-interference pattern: interference after film or reminder can reduce later intrusions while voluntary memory is often relatively preserved.

**Paragraph 2: Why this is theoretically interesting**
The same event appears less likely to intrude while remaining deliberately accessible.

**Paragraph 3: Standard interpretation**
Explain, fairly and briefly, the separate-trace / sensory-trace / reconsolidation interpretation.

**Paragraph 4: Underdetermination**
A dissociation between retrieval outcomes does not by itself reveal the architecture of storage. A shared store can produce different retrieval outcomes under different cue states and retrieval policies.

**Paragraph 5: Retrieved-context alternative**
Introduce reminder reinstatement, competitor encoding, temporal/source overlap, and retrieval cue precision.

**Paragraph 6: Present contribution**
State that the paper formalizes this account and tests its qualitative boundary conditions.

### Required thesis paragraph

Use a version of this:

> The present paper develops a retrieved-context account of selective interference. The account makes three commitments. First, reminders matter because they reinstate the context in which trauma-related material was encoded. Second, interference matters because it encodes competitor episodes into overlapping temporal/source context. Third, voluntary memory is relatively spared when retrieval is guided by target-specific cues or probe-specific access, whereas uncontrolled retrieval is vulnerable to competition from items bound into the same contextual neighborhood. These commitments allow a single memory system to produce the intrusion/voluntary-memory dissociation without positing separate intrusive and voluntary traces.

### Do not include

* a full history of trauma-film studies;
* broad clinical treatment claims;
* extended PTSD theory;
* a long reconsolidation review.

---

## Section 2. The empirical and theoretical target

### Job

Define what the model is trying to explain and what it is not trying to explain.

### Recommended structure

Use a compact table.

| Empirical pattern                     | Model target                                                           |
| ------------------------------------- | ---------------------------------------------------------------------- |
| Intrusions reduced after interference | Lower probability of trauma-film items winning uncontrolled retrieval  |
| Reminder matters                      | Reinstatement increases target–competitor context overlap              |
| Task type matters                     | Effectiveness depends on source overlap and competitor strength        |
| Voluntary memory often spared         | Target-cued/probe-specific tests are less exposed to broad competition |
| Results vary across tests             | Test cues change retrieval cue precision                               |

### Required scope statement

> We model intrusion occurrence at the level of trauma-item sampling. We do not model distress, vividness, appraisal, avoidance, or clinical symptom change.

### Do not include

Do not make every empirical result in the selective-interference literature a benchmark. The benchmark is the qualitative pattern and its boundary conditions.

---

## Section 3. A contextual-competition account of selective interference

### Job

Explain the theory in prose before equations.

### Subsections

**3.1 Film encoding**
Film items are encoded into temporal context and source context.

**3.2 Reminder reinstatement**
A reminder pulls current context back toward the film-associated region.

**3.3 Interference as competitor encoding**
Interference items are encoded into the reinstated region and become competitors.

**3.4 Intrusion-like retrieval**
Uncontrolled retrieval samples from context-to-item competition. Competitors reduce the chance that film items win.

**3.5 Voluntary retrieval and cue precision**
Voluntary tests differ in how much they constrain retrieval toward the target episode.

**3.6 Boundary conditions**
The model predicts effects of reminder strength, source overlap, competitor strength, and cue precision.

### Figure 1: Mechanism schematic

Panel A: film items encoded in temporal/source context.
Panel B: reminder reinstates film context.
Panel C: interference encodes competitors into overlapping context.
Panel D: uncontrolled retrieval is captured by competitors; target-cued retrieval is more protected.

### Do not include

Do not lead with formal CMR equations. This section should stand on its own.

---

## Section 4. Formal model

### Job

Specify the model compactly enough to support the simulations.

### Main subsections

**4.1 Representations**
Items, temporal context, source context.

**4.2 Encoding**
Items update context and bind to temporal/source states.

**4.3 Reminder operation**
Reminder reinstates film-associated context. If reminder learning is included, treat it as an implementation choice or sensitivity analysis.

**4.4 Interference manipulation**
Interference varies by competitor strength and temporal/source overlap.

**4.5 Retrieval modes**
Define a cue-precision continuum: unguided sampling, directed recall-like retrieval, and probe-specific retrieval.

**4.6 Parameters and calibration**
Use externally estimated CMR-family parameters where possible. Treat trauma-film-specific quantities as paradigm-level variables rather than fitted parameters.

### Required model-component table

| Component              | Theoretical role                                |
| ---------------------- | ----------------------------------------------- |
| Temporal context       | Sequential proximity and reminder reinstatement |
| Source context         | Film-wide/task-overlap competition              |
| Competitor strength    | Strength of interference-task competitors       |
| Reminder reinstatement | Places interference encoding near film context  |
| Cue precision          | Determines test-format vulnerability            |

### Move to supplement

* full matrix definitions;
* indexing details;
* long parameter tables;
* normalization derivations;
* implementation pseudocode;
* extensive sensitivity plots.

---

## Section 5. Simulation overview

### Job

State simulation logic and success criteria before showing results.

### Main text

The simulations evaluate three core questions:

1. Can a single temporal/source retrieved-context system produce the selective-interference dissociation?
2. Does interference depend on reminder reinstatement, source overlap, and competitor strength?
3. Can cue precision explain why some test formats reveal a sharper dissociation than others?

### Predefined qualitative success criteria

The account is supported if:

* interference reduces intrusion-like film sampling;
* impairment is stronger for unguided retrieval than for target-cued/probe-specific retrieval;
* high-overlap competitors interfere more than low-overlap competitors;
* reminder-plus-interference is stronger than interference without reminder;
* effects are not limited to a single hand-tuned parameter setting.

### Do not include

Do not describe every internal diagnostic here. Keep the reader focused on the main evidential package.

---

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

# 12. Discussion skeleton

## 7.1 Summary of results

Restate the three model ingredients:

* reminder reinstatement;
* competitor encoding in overlapping temporal/source context;
* cue precision at retrieval.

## 7.2 What the account changes

The selective-interference dissociation is not direct evidence for separate intrusive and voluntary memory traces.

## 7.3 Relation to separate-trace and reconsolidation accounts

Be fair:

* the model does not disprove separate traces;
* the model does not disprove reconsolidation;
* the model shows that the core dissociation can be produced by competitive retrieval in a shared episodic system.

## 7.4 Source context and task specificity

Explain why source context matters:

* prevents the account from being purely recency-based;
* provides a principled way to model why task type matters;
* treats “visuospatial” as one possible source-overlap dimension rather than a primitive category.

## 7.5 Test format and experiment design

Explain the design payoff:

* item recognition may be protected because of probe specificity;
* free recall may be more vulnerable;
* source/associative tests may reveal effects hidden by item recognition;
* intrusion tasks with strong cues may narrow differences across conditions.

## 7.6 Predictions

Use three levels.

**Framework-level predictions**

* interference scales with temporal/source overlap;
* reminder effects scale with reinstatement;
* voluntary sparing depends on cue precision;
* task category matters through overlap and competitor strength.

**Variant-specific predictions**

* temporal-only variants predict stronger local/late-item effects;
* source-context variants predict broader interference;
* arousal-source and visuospatial-source variants predict different task rankings.

**Implementation-specific predictions**

* exact serial-position curves;
* exact threshold values;
* exact effects of choice sensitivity.

Treat implementation-specific predictions cautiously.

## 7.7 Limitations

State explicitly:

* no full phenomenology of intrusions;
* no distress/vividness/appraisal modeling;
* no clinical treatment model;
* simulations target qualitative boundary conditions;
* parameter robustness constrains claim strength.

## 7.8 Conclusion

End with:

> Selective interference can be understood as a boundary condition on competitive retrieval from a shared episodic memory system.

---

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

# 14. Manuscript presentation order

Use this order in the paper unless results suggest otherwise:

1. Introduction.
2. Empirical/theoretical target.
3. Conceptual retrieved-context account.
4. Formal model.
5. Simulation overview.
6. Core dissociation.
7. Boundary conditions.
8. Cue precision/test format.
9. Robustness and ablations.
10. General discussion.

Do not organize the paper around the order in which the model was built. Organize it around the argument.

---

# 15. Main figure plan

## Figure 1: Mechanism schematic

No data. Conceptual.

## Figure 2: Core dissociation

Unguided retrieval more impaired than target-cued/probe-specific retrieval.

## Figure 3: Boundary conditions

Reminder × overlap × competitor strength.

## Figure 4: Cue precision

Three or four retrieval modes ordered by cue precision.

## Figure 5: Robustness/ablation summary

Compact main-text version, with extended sweeps in supplement.

That is enough for PB&R v1.

---

# 16. Main table plan

## Table 1: Empirical targets and model mechanisms

| Empirical target | Model mechanism | Simulation |
| ---------------- | --------------- | ---------- |

## Table 2: Model constructs and theoretical roles

| Construct | Role | Free/fixed/status |
| --------- | ---- | ----------------- |

Do not add more main tables unless absolutely necessary.

---

# 17. Rhetorical strength decision table

Use this after simulations.

| Result pattern                             | Manuscript framing                                                                                        |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| Robust across plausible parameter space    | “Retrieved-context competition provides a compact positive account of selective interference.”            |
| Works under interpretable constraints      | “The model identifies conditions under which a single-system account can explain selective interference.” |
| Works only with fine tuning                | “The model shows formal possibility but mainly clarifies constraints on single-system explanations.”      |
| Fails to show reminder/overlap/cue effects | Reconsider architecture before drafting a paper around this account.                                      |

---

# 18. Minimum viable PB&R manuscript

The real minimum is:

1. inference-problem introduction;
2. contextual-competition account;
3. compact formal model;
4. core dissociation simulation;
5. reminder/overlap/strength boundary-condition simulation;
6. cue-precision simulation;
7. compact robustness/ablation evidence;
8. design implications;
9. limitations.

Not minimum:

* full temporal-only story in the main text;
* full VIT model;
* full recognition taxonomy;
* emotional vs visuospatial source-context comparison;
* clinical intervention simulations;
* exhaustive parameter maps.

---

# 19. Personal work guardrails

Use these to avoid both underperforming and overexpanding.

## When tempted to add a model feature

Ask:

> Does it affect competitor strength, overlap, or cue precision?

If no, defer.

## When tempted to add a simulation

Ask:

> Does it test a boundary condition needed for PB&R v1?

If no, put it in the backlog.

## When tempted to add literature

Ask:

> Does this literature bear directly on selective interference, retrieved context, source context, cue precision, or the inference from dissociation to traces?

If no, cut or save for later.

## When tempted to strengthen claims

Ask:

> Do the robustness results support this wording?

If no, weaken.

## When tempted to make the paper bigger

Ask:

> Would this be required for PB&R v1?

If no, defer.

---

# 20. The final operational summary

Write the v1 paper as:

> A PB&R theoretical/modeling article showing that selective interference can be explained by retrieved-context competition: reminders reinstate trauma-film context, interference encodes competitors into overlapping temporal/source context, and test cue precision determines whether the effect appears selective to intrusion-like retrieval.

The v1 paper should **not** try to be:

> a complete theory of trauma, Tetris, reconsolidation, recognition, emotional memory, and PTSD.

That distinction is the contract.

[1]: https://link.springer.com/journal/13423/submission-guidelines?utm_source=chatgpt.com "Submission guidelines | Psychonomic Bulletin & Review"
[2]: https://www.sciencedirect.com/journal/journal-of-memory-and-language/publish/guide-for-authors?utm_source=chatgpt.com "Guide for authors - Journal of Memory and Language"
[3]: https://www.apa.org/pubs/journals/rev?utm_source=chatgpt.com "Psychological Review"
