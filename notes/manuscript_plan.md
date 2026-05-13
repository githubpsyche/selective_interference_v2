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

