# Prompt: Integrate Selective Interference Introduction

I am drafting the Introduction for a theoretical/computational paper for *Psychonomic Bulletin & Review* on selective interference in intrusive memory.
Your task is to produce a revised `# Introduction` only.
Do not write the abstract, model section, results, or discussion.
Use one sentence per line.

The target manuscript file is `selective_interference_v2/index.qmd`.
The current `# Introduction` is empty except for headings that follow it.
The introduction should end before the next heading, `# Empirical and Theoretical Target`.

## Current Abstract

Visuospatial tasks performed after trauma-film encoding, or after a later reminder of the film, can reduce intrusive memories while leaving voluntary memory relatively intact.
This selective-interference pattern is often treated as evidence that intrusive and voluntary remembering depend on differently vulnerable memory representations.
Here we implement an alternative retrieved-context account in an emotional Context Maintenance and Retrieval model (eCMR), where the dissociation can arise from context reinstatement and retrieval competition rather than from separately vulnerable representations.
In the model, film context remains active after encoding and can later be reinstated by reminders, so interference performed in either state binds task items to overlapping context.
When later contexts cue both film items and task competitors, uncontrolled context-to-item sampling is less likely to select trauma-film items as intrusions, even though film-item strength is not reduced.
Deliberate recall is less vulnerable when task goals and control processes reinstate film context and favor film items over competitors; item-specific probes can provide a further route to protected voluntary access.
Simulations show that this modeled sequence can selectively impair intrusion-like retrieval, and that the pattern depends on contextual overlap between film and task items and on reminder-driven reinstatement before competitor encoding.
Selective interference is therefore compatible with a single retrieved-context system and is not by itself diagnostic of separate representational systems or selective trace weakening.

## Manuscript Heading Context

The revised Introduction should precede these sections:

```markdown
# Empirical and Theoretical Target

# A Retrieved-Context Account of Selective Interference

# Model and Paradigm

# Simulation Overview

# Results

## Simulation 1: Selective Interference Across Retrieval Configurations

## Simulation 2: Competitor Encoding in Reinstated Context

## Simulation 3: Contextual Overlap Versus Generic Task Load

## Simulation 4: Test-Format Heterogeneity

## Robustness and Diagnostic Checks
```

Because the next section is `# Empirical and Theoretical Target`, the Introduction should not exhaustively review the empirical literature.
Because the section after that is `# A Retrieved-Context Account of Selective Interference`, the Introduction should not fully specify the model.
The Introduction should orient the reader, state the problem, and motivate why a formal retrieved-context account is worth developing.

## Source Hierarchy

Use the old introduction as the primary prose source.
It has the best paragraph architecture and style.

Use the browser-draft material as a secondary source.
It adds useful newer framing about diagnosticity, heterogeneity, retrieval/test configurations, and generalization-oriented modeling.

Use the current abstract as binding.
Do not reintroduce claims that the abstract has moved away from.

Use `workspace/downloads/references.bib` as the citation-key source.
Do not invent citation keys unless clearly marked as placeholders.

## Scope Constraints

Keep the Introduction narrow.
Include only enough literature to motivate:

1. the trauma-film / selective-interference phenomenon;
2. the common inference from selective interference to differently vulnerable intrusive and voluntary memory representations;
3. the need for a formal alternative account;
4. the retrieved-context proposal at a high level.

Do not write:

- a broad PTSD review;
- a clinical treatment review;
- a reconsolidation review;
- a full trauma-film literature review;
- a complete theory of voluntary versus involuntary remembering;
- a taxonomy of intrusive-memory phenomenology;
- a detailed model specification.

Clinical and real-world intervention studies may be mentioned only to motivate why the phenomenon matters.
The simulations target the controlled logic of selective-interference paradigms, not clinical efficacy.

Avoid these framings:

- claiming dual-representation or reconsolidation accounts are false;
- making "Tetris works because it is Tetris" the mechanism;
- claiming the model weakens, erases, or damages film items;
- making recognition immunity the headline;
- treating all voluntary-memory measures as one computational category;
- making emotional/source context the whole paper unless needed.

## Desired Introduction Shape

Aim for roughly 4-6 compact paragraphs.
Preserve the old introduction's useful arc, but update it to match the current abstract:

1. Open with the memory problem: durable encoding versus selective access.
2. Introduce the trauma-film paradigm and the intrusion/voluntary-memory dissociation.
3. Introduce selective interference after film encoding or later reminder.
4. Explain the common architecture-level interpretation without over-reviewing dual-representation or reconsolidation accounts.
5. Introduce the alternative retrieved-context account and why formal simulation is useful.
6. Preview the simulation package at a high level: reminder-driven context reinstatement, competitor encoding in overlapping context, selective intrusion-like impairment, deliberate-recall protection, and test-format/design implications.

The introduction should make diagnosticity visible, but the positive formal account should be primary.
Do not make "we ask whether that inference is required" the central research question.
Use "alternative account" or similar wording instead.

## Style Constraints

Use one sentence per line.
Keep the style compact, theoretical, and concrete.
Avoid excessive signposting.
Avoid making the prose sound like a planning document.
Do not add subheadings inside the Introduction.
Prefer citation keys already listed below.
Use straight quotes and ASCII punctuation.
Avoid em dashes.

## Primary Prose Source: Old Introduction

```markdown
# Introduction

Traumatic experience foregrounds a trade-off between durability and selectivity in episodic remembering.
Memory should retain highly consequential episodes so critical details stay accessible long into the future.
At the same time, adaptive retrieval is selective: what comes to mind should normally depend on current cues, goals, and safety.
Intrusive memories after trauma suggest that durable encoding can outpace regulatory control.
The event returns repeatedly and indiscriminately, despite the demands of the present [@ehlers2000cognitive; @brewin2010intrusive; @krans2009intrusive; @iyadurai2019intrusive].

The present work examines this trade-off in the trauma-film paradigm [@james2016trauma; @holmes2008inducing].
Participants watch a distressing film depicting scenes of injury or threat [@holmes2008inducing; @james2016trauma].
Intrusive memories commonly emerge over the following days in diary measures [@holmes2004trauma; @holmes2008inducing; @james2016trauma].
When asked to recall or recognize the same material deliberately, voluntary memory can be relatively preserved, and its relationship to intrusion frequency can be weak, such that the two measures dissociate [@holmes2004trauma; @james2016trauma].
The same encoded episode can therefore support both uncontrolled and controlled access, and these modes can come apart empirically [@holmes2004trauma; @iyadurai2019intrusive].

A sharper dissociation emerges when a brief visuospatial task follows the film or a later film reminder [@holmes2009can; @james2015computer; @kessler2020visuospatial].
Across studies, participants who play Tetris or perform a similarly visually-engaging task report fewer intrusive memories over the following days [@holmes2009can; @holmes2010key; @deeprose2012imagery].
Voluntary memory for the same material generally shows little measurable impact even when retrieval conditions are matched [@lau2019intrusive; @asselbergs2023systematic].
Such interventions are effective even after prompting reinstatement of real-life traumatic memories, reducing intrusions while preserving deliberate recall for life experiences such as motor vehicle accidents, traumatic childbirth following emergency caesarean section, and war-related trauma in refugees [@iyadurai2018preventing; @horsch2017reducing; @kanstrup2021single].
A post-encoding or post-reminder manipulation appears to alter one mode of retrieval more than the other, even when both draw on the same recent experience.

A prominent interpretation attributes this selectivity to separable memory representations [@brewin1996dual; @brewin2014episodic].
Under the dual-representation account, traumatic experience produces distinct sensory and contextual memory traces -- the first supporting involuntary re-experiencing, the second supporting deliberate recall [@brewin2010intrusive; @brewin2014episodic].
A visuospatial interference task competes for the perceptual processing resources needed to consolidate the sensory trace, reducing later intrusions while leaving the contextual trace and the voluntary memory it supports relatively intact [@holmes2009can; @james2015computer].
When the intervention follows a reminder at longer delays, the account invokes reconsolidation: the reminder reactivates the sensory trace, and the interfering task disrupts its restabilization during a time-limited window [@kindt2009beyond; @james2015computer].
The account thus ties selective interference to separate memory representations, modality-specific disruption of one trace, and a discrete reconsolidation window.

Here we develop, to our knowledge, the first formalized computational account of selective interference within a retrieved-context framework.
In this account, the original event, any reminder, and subsequent interference are each encoded by binding item representations to a continuously evolving context representation [@yonelinas2019contextual; @howard2002distributed; @polyn2009context].
Later retrieval is driven by the current context state as a cue, so competition depends on how strongly different episodes are associated with overlapping regions of context.
Deliberate recall is more resistant because it combines a more target-oriented initial cue with a sharper decision rule, both of which favor film items over competitors.
The dissociation between involuntary and voluntary recall is thus attributed to differences in retrieval state applied to the same stored episodes.
The simulations first test the central behavioral consequence of that account: under the same interference manipulation, unguided retrieval should be more impaired than deliberate recall.
They then examine delayed reminder effects and design features that alter the observed pattern across trauma-film studies.
On this view, post-reminder interference works by encoding strong competitors in reinstated trauma context, and shared arousal between trauma and interference items can further amplify that competition.
The result is a mechanistic alternative to the dual-representation account and a set of specific hypotheses about when selective interference should appear and how it should vary across paradigms.
```

## Secondary Source: Browser-Draft Introduction

Use this mainly for updated framing, not as the primary prose style.

```markdown
Intrusive memories are involuntary returns of a prior event, often experienced as vivid sensory fragments that enter awareness without deliberate retrieval.
In experimental work, the trauma-film paradigm has provided a controlled analogue for studying such memories: participants view distressing film material and subsequently record involuntary memories of the film over the following days [@holmes2008inducing; @james2016trauma; @krans2009intrusive].
The paradigm is necessarily limited, but it allows researchers to manipulate encoding, reminder, and post-encoding task conditions in ways that would be impossible in real trauma.

A central finding from this literature is the selective interference effect.
In several studies, completing a task such as Tetris after film exposure, or after a later film reminder, reduced subsequent intrusion reports while voluntary memory for the same material was relatively preserved [@holmes2009can; @holmes2010key; @james2015computer; @kessler2020visuospatial; @lau2019intrusive].
The evidence base is heterogeneous, and recent reviews and replications caution against treating the effect as settled or uniform [@asselbergs2023systematic; @varma2024experimental; @wessel2025evidence].
Still, the qualitative pattern remains theoretically important: one manipulation appears to reduce uncontrolled access to an event without comparably disrupting deliberate access to that same event.

That pattern has been used to support representationally selective accounts of intrusive memory.
Dual-representation accounts propose that traumatic events can be represented in partly separable forms, with sensory or situationally accessible representations supporting intrusive re-experiencing and contextual or verbally accessible representations supporting voluntary remembering [@brewin1996dual; @brewin2014episodic].
In the selective-interference literature, visuospatial tasks have often been interpreted as selectively disrupting the sensory/visual representation that supports later intrusions [@holmes2009can; @holmes2010key].
Delayed reminder-plus-interference studies have extended this logic to reconsolidation or updating: a reminder reactivates the memory, and a subsequent visuospatial task disrupts the reactivated visual trace [@james2015computer].

The present paper asks what this dissociation licenses.
A difference between memory outcomes does not by itself establish separate stored traces.
The same stored episode can be differentially accessible under different retrieval conditions, especially when later experience changes the competitive environment around the original memory.
Similar inferential issues arise elsewhere in memory science, where dissociations initially interpreted as evidence for separate processes or stores can sometimes be reproduced by representational or retrieval differences within a single system [@benjamin2010representational; @polyn2025capacity].
The selective-interference pattern therefore motivates a formal test: can a single episodic-memory architecture generate the dissociation without positing separate intrusive and voluntary traces?

Retrieved-context theory provides a natural architecture for this test.
In temporal context and CMR-family models, events are encoded by binding item information to a context state that changes over time, and later recall is driven by context-to-item associations [@howard2002distributed; @polyn2009context].
Retrieved items can reinstate prior context through item-to-context associations, and context can include non-temporal source features such as task, modality, emotional, or source-related information [@polyn2009context; @talmi2019retrieved].
These mechanisms have already been extended to emotional memory and intrusion-relevant phenomena [@cohen2022memory].
What has not been specified is how they might explain selective interference: reduced intrusion-like access with relatively preserved voluntary memory after a post-film or post-reminder task.

We propose that selective interference can arise from contextual competition.
A reminder reinstates temporal/source context associated with the film.
Interference performed in that state encodes new competitor items into overlapping context.
Later retrieval states that overlap this region cue both film items and interference items, so interference items can capture retrieval probability from film items.
The model does not require the interference task to erase or weaken a special intrusive trace.
It requires competitors that are strongly encoded and contextually positioned to compete with film items during later retrieval.

The account also separates retrieval pathways from retrieval/test configurations.
Context-to-item retrieval is not uniquely intrusive; it is also the core operation in recall-like tasks.
Unguided retrieval and directed recall can therefore share a pathway while differing in their retrieval configuration.
Recognition differs because the candidate item is presented and evaluated through the model's recognition operation, potentially involving item-to-context reinstatement.
Cue-presented intrusion tasks differ again: a cue may reinstate context without presenting the remembered event as the candidate response.
These distinctions matter because voluntary memory is not one computational category.
Directed recall and recognition can show different vulnerability to the same interference manipulation.

The simulations follow a generalization-oriented modeling logic rather than fitting the selective-interference literature directly.
Prior CMR work has used externally motivated parameterizations to test whether retrieved-context commitments generalize to new empirical settings [@busemeyer2000model; @lohnas2023event].
We use the same spirit here: the simulations ask whether a retrieved-context account can reproduce the qualitative structure of selective interference and its boundary conditions.
Specifically, we test whether the model produces stronger impairment under unguided retrieval than directed recall, whether contextual overlap distinguishes genuine competition from generic task load, whether recognition-like access differs from recall-like access, and whether delayed reminder effects follow from reinstatement before competitor encoding.
```

## Additional Browser-Thread Guidance To Consider

The browser thread later became more detailed than an Introduction probably needs.
Use these points as constraints or background, not necessarily as prose to include:

- The manuscript targets a family of selective-interference findings rather than one canonical effect.
- The evidence base is strong enough to motivate modeling but heterogeneous enough that the paper should avoid broad clinical-efficacy claims.
- Contextual overlap and delayed reminder effects are core to the modeling proposal, not optional add-ons.
- A reminder matters because it reinstates film-associated context before interference is encoded.
- Task class should not be reduced to a simple visuospatial-versus-verbal rule.
- Test formats differ: diary intrusions, vigilance-intrusion tasks, free recall, cued recall, recognition, and source/associative tests should not be collapsed into one generic voluntary-memory category.
- The paper abstracts intrusion occurrence to film-item access under retrieval configurations intended to approximate uncontrolled retrieval opportunities.
- The model does not explain distress, vividness, appraisals, avoidance, symptom change, or clinical treatment efficacy.

## Citation-Key Inventory

These keys are available in `workspace/downloads/references.bib`.
Use only keys relevant to the Introduction.

Core selective-interference / trauma-film keys:

- `holmes2004trauma`
- `holmes2008inducing`
- `holmes2009can`
- `holmes2010key`
- `deeprose2012imagery`
- `james2015computer`
- `james2016trauma`
- `kessler2020visuospatial`
- `lau2019intrusive`
- `lau2021selectively`
- `asselbergs2023systematic`
- `varma2024experimental`
- `wessel2025evidence`
- `hagenaars2017tetris`

Clinical/relevance keys to use sparingly:

- `iyadurai2018preventing`
- `horsch2017reducing`
- `kanstrup2021single`
- `iyadurai2019intrusive`
- `ehlers2000cognitive`
- `krans2009intrusive`

Interpretation/theory keys:

- `brewin1996dual`
- `brewin2010intrusive`
- `brewin2014episodic`
- `brewin2014contextualisation`
- `kindt2009beyond`
- `baddeley2000working`
- `bourne2010distraction`

Retrieved-context / modeling keys:

- `howard2002distributed`
- `polyn2009context`
- `polyn2009task`
- `sederberg2008context`
- `kahana1996associative`
- `mensink1989model`
- `yonelinas2019contextual`
- `talmi2019retrieved`
- `cohen2022memory`
- `healey2014memory`
- `lohnas2023event`
- `busemeyer2000model`

General dissociation/modeling analogy keys:

- `benjamin2010representational`
- `polyn2025capacity`

## Output Requested

Return only:

1. A revised `# Introduction` section, with one sentence per line.
2. A short note listing major changes made and why.

Do not rewrite the abstract.
Do not write later manuscript sections.
Do not expand the literature review beyond the constraints above.
