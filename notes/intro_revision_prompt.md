# Prompt: Revise Selective Interference Introduction

I am drafting the Introduction for a theoretical/computational paper on selective interference in intrusive memory.

Your task is to revise an existing Introduction, not write from scratch.

The old Introduction below is the primary prose source and already has a good paragraph architecture.
However, it was written for an earlier version of the project and needs to be updated to fit the current paper plan.

Use the browser-draft Introduction as a secondary source: it contains useful newer framing, especially the inference-from-dissociation framing, retrieval/test-configuration distinctions, and generalization-oriented simulation rationale.
Do not treat it as the primary style source.

## Current Paper Claim

The paper develops a retrieved-context account of selective interference.

The core claim is that reduced intrusion-like retrieval with relatively preserved voluntary memory can arise within a single episodic memory system when:

1. reminders reinstate trauma-film context;
2. interference tasks encode competitors into overlapping temporal/source context;
3. later tests differ in retrieval configuration / cue constraint.

The paper is not trying to prove that dual-representation theory is false.
It challenges the inference that the selective-interference dissociation is uniquely diagnostic of separate intrusive and voluntary traces.

## Current Abstract

Selective interference poses a diagnostic problem for theories of memory architecture.
In trauma-film studies, post-encoding or post-reminder visuospatial tasks can reduce later intrusive memories while leaving voluntary memory relatively intact.
This pattern has often been interpreted as evidence for separate intrusive/sensory and voluntary/contextual traces, or for selective disruption of a reactivated sensory trace.
We develop an alternative single-system account within retrieved-context theory.
The account treats interference not as weakening the film representation, but as encoding competitors into a contextual neighborhood later used for retrieval.
Reminders reinstate trauma-film context; interference performed in that state binds new competitors to overlapping temporal/source context.
When later retrieval states return to that neighborhood, they cue both film and interference items, reducing the probability that film items are sampled.
Differences between intrusion and voluntary-memory measures arise because tests differ in retrieval configuration: broad or weakly guided retrieval remains vulnerable to contextual competitors, whereas more constrained, probe-specific access can preserve film-item retrieval.
We implement the account in a CMR-family model of episodic and emotional memory.
Simulations test whether the model reproduces the intrusion/voluntary-memory dissociation, distinguishes contextual overlap from generic task load, explains heterogeneity across test formats, and produces delayed reminder effects through reinstatement before competitor encoding.
Selective interference is therefore treated as a boundary condition on context-guided retrieval, not as uniquely diagnostic evidence for separate memory traces.

## Current Manuscript Heading Order

# Introduction

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

# General Discussion

# References

## Literature Review Scope

This is high priority.

Keep the Introduction narrow.
Include only enough literature to motivate:

1. the trauma-film / selective-interference phenomenon;
2. the standard separate-trace / sensory-trace / reconsolidation interpretation;
3. the inference problem;
4. the retrieved-context alternative.

Do not write a broad PTSD review, clinical treatment review, reconsolidation review, or full trauma-film literature review.

Out of scope:

- full PTSD or clinical treatment efficacy;
- distress, vividness, appraisals, avoidance, or symptom trajectories;
- individual differences;
- whether Tetris is clinically effective;
- a complete theory of voluntary/involuntary remembering;
- a full taxonomy of intrusive-memory phenomenology.

Clinical studies can motivate the importance of the problem, but the simulations target the controlled logic of selective-interference paradigms.

## Source Hierarchy

Use the old Introduction below as the primary source.

Preserve its five-paragraph arc where possible:

1. P1: durability vs selectivity tension in episodic remembering;
2. P2: trauma-film paradigm and involuntary/voluntary dissociation;
3. P3: selective interference phenomenon;
4. P4: dual-representation / reconsolidation interpretation;
5. P5: retrieved-context alternative.

Use the browser draft as a secondary source for three updates:

1. the Introduction should more explicitly frame the paper as asking what the dissociation licenses;
2. the Introduction should distinguish retrieval pathways from retrieval/test configurations;
3. the Introduction should explain that the simulations are generalization-oriented rather than direct fits to the selective-interference literature.

Do not preserve old claims that conflict with the current plan:

- avoid strong clinical translation language;
- avoid “recognition immunity” framing;
- avoid making shared arousal/emotional context central;
- avoid making Tetris/visuospatialness a primitive mechanism;
- avoid claiming the model weakens, erases, or damages film items;
- avoid saying the paper explains full clinical intervention efficacy.

The final paragraph should state the current retrieved-context thesis:

- reminders reinstate trauma-film context;
- interference encodes competitors into overlapping temporal/source context;
- later retrieval from that region cues both film and interference items;
- selective impairment depends on retrieval/test configuration, not separate stored traces;
- simulations test the dissociation, contextual-overlap mechanism, test-format heterogeneity, and delayed reminder effects.

## Style Constraints

Use one sentence per line.
Keep the style close to the old Introduction: compact, theoretical, and concrete.
Avoid excessive signposting.
Avoid making the prose sound like a planning document.
Do not add subheadings inside the Introduction.
Use citation keys already present in the old Introduction when possible.
Do not invent new citation keys unless clearly marked as placeholders.

## Old Introduction To Revise

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
Under the dual-representation account, traumatic experience produces distinct sensory and contextual memory traces — the first supporting involuntary re-experiencing, the second supporting deliberate recall [@brewin2010intrusive; @brewin2014episodic].
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

## Browser-Draft Introduction As Secondary Source

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
Recognition differs because the candidate item is presented and evaluated through the model’s recognition operation, potentially involving item-to-context reinstatement.
Cue-presented intrusion tasks differ again: a cue may reinstate context without presenting the remembered event as the candidate response.
These distinctions matter because voluntary memory is not one computational category.
Directed recall and recognition can show different vulnerability to the same interference manipulation.

The simulations follow a generalization-oriented modeling logic rather than fitting the selective-interference literature directly.
Prior CMR work has used externally motivated parameterizations to test whether retrieved-context commitments generalize to new empirical settings [@busemeyer2000model; @lohnas2023event].
We use the same spirit here: the simulations ask whether a retrieved-context account can reproduce the qualitative structure of selective interference and its boundary conditions.
Specifically, we test whether the model produces stronger impairment under unguided retrieval than directed recall, whether contextual overlap distinguishes genuine competition from generic task load, whether recognition-like access differs from recall-like access, and whether delayed reminder effects follow from reinstatement before competitor encoding.

## Output Requested

Return:

1. A revised Introduction only, using one sentence per line.
2. A short note after the draft listing the major changes you made and why.

Do not rewrite the abstract.
Do not produce a full paper outline.
Do not expand the literature review beyond the scope above.
