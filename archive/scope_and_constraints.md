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

