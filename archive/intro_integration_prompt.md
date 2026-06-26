# Prompt: Integrate Selective Interference Introduction

I am drafting the Introduction for a theoretical/computational paper for *Psychonomic Bulletin & Review* on selective interference in intrusive memory.
Your task is to produce a revised `# Introduction` only.
Do not write the abstract, model section, results, or discussion.
Use one sentence per line.
This prompt is intended for a web LLM with no access to my local workspace.
All context available for the task is included below.

In the manuscript, the current `# Introduction` is empty except for headings that follow it.
The introduction must stop before the next manuscript section, which will handle the empirical and theoretical target in more detail.

## Current Abstract

Visuospatial tasks performed after trauma-film encoding, or after a later reminder of the film, can reduce intrusive memories while leaving voluntary memory relatively intact.
This selective interference effect is often treated as evidence that intrusive and voluntary remembering depend on differently vulnerable memory representations.
Here we simulate an alternative retrieved-context account using an emotional Context Maintenance and Retrieval (eCMR) model, asking whether context reinstatement, competitor learning, and retrieval control can generate the selective-interference pattern without separately vulnerable representations.
In the model, film context remains active after encoding and can later be reinstated by reminders, so an interfering task performed in either state binds task representations to overlapping context.
When later retrieval contexts cue both film representations and task competitors, uncontrolled retrieval from context cues is less likely to sample trauma-film items in intrusion-like retrieval, even though film-item strength is not reduced.
Deliberate recall is less vulnerable when task goals and control processes reinstate film context and prioritize film items over competitors for retrieval; film-specific cues can also steer retrieval toward film context across test formats.
Together, the simulations reproduce selective impairment of intrusion-like retrieval and specify when the intrusion-voluntary-memory dissociation should be more or less pronounced, helping to interpret heterogeneity across empirical paradigms.
Selective interference is therefore compatible with a single retrieved-context system and is not by itself diagnostic of separate representational systems or selective trace weakening.

## Manuscript Placement

Write only the prose that belongs under the manuscript heading `# Introduction`.
Do not include any later manuscript headings in your response.
The planned downstream manuscript structure is:

- `# Empirical and Theoretical Target`
- `# A Retrieved-Context Account of Selective Interference`
- `# Model and Paradigm`
- `# Simulation Overview`
- `# Results`
- `## Simulation 1: Selective Interference Across Retrieval Configurations`
- `## Simulation 2: Competitor Encoding in Reinstated Context`
- `## Simulation 3: Contextual Overlap Versus Generic Task Load`
- `## Simulation 4: Test-Format Heterogeneity`
- `## Robustness and Diagnostic Checks`
- `# General Discussion`

Use this section map only as structural context for deciding what the Introduction needs to orient, what it can signpost, and what it should leave for later sections.
Do not reproduce these headings or write those later sections.
Do not exhaustively review the empirical literature or fully specify the model.

## Context and Binding Constraints

The current abstract is binding for the manuscript's current claims, terms, and emphasis.
The prior introduction drafts and browser-thread notes below are included as context, not as templates or a language bank.
You may write the Introduction from scratch.
You are not limited to reusing, combining, or revising the existing prose.
You may use, ignore, or depart from the prior drafts.
Do not preserve text solely because it appears in a prior draft.
Where the contextual materials conflict with the current abstract, follow the current abstract.
Do not introduce claims that conflict with the current abstract or the hard constraints below.

Use only the citation keys and reference metadata embedded below.
Do not invent citation keys unless clearly marked as placeholders.

## Hard Style Constraints

Use one sentence per line.
Write manuscript prose, not planning prose.
Do not add subheadings inside the Introduction.
Use citation keys from the embedded list when citing.
Use straight quotes and ASCII punctuation.
Avoid em dashes.

## Context Excerpt A: Older Local Introduction Draft

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

## Context Excerpt B: Browser-Draft Introduction

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

## Citation Reference Notes

These are the available citation keys and reference metadata.
Use only keys relevant to the Introduction.
Do not assume access to an external `.bib` file.

Core selective-interference / trauma-film keys:

- `holmes2004trauma`: Holmes, Brewin, & Hennessy (2004), "Trauma films, information processing, and intrusive memory development," *Journal of Experimental Psychology: General*.
- `holmes2008inducing`: Holmes & Bourne (2008), "Inducing and modulating intrusive emotional memories: A review of the trauma film paradigm," *Acta Psychologica*.
- `holmes2009can`: Holmes, James, Coode-Bate, & Deeprose (2009), "Can playing the computer game 'Tetris' reduce the build-up of flashbacks for trauma? A proposal from cognitive science," *PLoS ONE*.
- `holmes2010key`: Holmes, James, Kilford, & Deeprose (2010), "Key steps in developing a cognitive vaccine against traumatic flashbacks: Visuospatial Tetris versus verbal Pub Quiz," *PLoS ONE*.
- `deeprose2012imagery`: Deeprose, Zhang, DeJong, Dalgleish, & Holmes (2012), "Imagery in the aftermath of viewing a traumatic film: Using cognitive tasks to modulate the development of involuntary memory," *Journal of Behavior Therapy and Experimental Psychiatry*.
- `james2015computer`: James et al. (2015), "Computer game play reduces intrusive memories of experimental trauma via reconsolidation-update mechanisms," *Psychological Science*.
- `james2016trauma`: James et al. (2016), "The trauma film paradigm as an experimental psychopathology model of psychological trauma: Intrusive memories and beyond," *Clinical Psychology Review*.
- `kessler2020visuospatial`: Kessler et al. (2020), "Visuospatial computer game play after memory reminder delivered three days after a traumatic film reduces the number of intrusive memories of the experimental trauma," *Journal of Behavior Therapy and Experimental Psychiatry*.
- `lau2019intrusive`: Lau-Zhu, Henson, & Holmes (2019), "Intrusive memories and voluntary memory of a trauma film: Differential effects of a cognitive interference task after encoding," *Journal of Experimental Psychology: General*.
- `lau2021selectively`: Lau-Zhu, Henson, & Holmes (2021), "Selectively interfering with intrusive but not voluntary memories of a trauma film: Accounting for the role of associative memory," *Clinical Psychological Science*.
- `asselbergs2023systematic`: Asselbergs et al. (2023), "A systematic review and meta-analysis of the effect of cognitive interventions to prevent intrusive memories using the trauma film paradigm," *Journal of Psychiatric Research*.
- `varma2024experimental`: Varma et al. (2024), "A systematic review and meta-analysis of experimental methods for modulating intrusive memories following lab-analogue trauma exposure in non-clinical populations," *Nature Human Behaviour*.
- `wessel2025evidence`: Wessel et al. (2025), "Evidence that Tetris reduces immediate but not subsequent daily intrusions of a trauma film: A multilab replication study," *Collabra: Psychology*.
- `hagenaars2017tetris`: Hagenaars, Holmes, Klaassen, & Elzinga (2017), "Tetris and word games lead to fewer intrusive memories when applied several days after analogue trauma," *European Journal of Psychotraumatology*.

Clinical/context keys:

- `iyadurai2018preventing`: Iyadurai et al. (2018), "Preventing intrusive memories after trauma via a brief intervention involving Tetris computer game play in the emergency department," *Molecular Psychiatry*.
- `horsch2017reducing`: Horsch et al. (2017), "Reducing intrusive traumatic memories after emergency caesarean section," *Behaviour Research and Therapy*.
- `kanstrup2021single`: Kanstrup et al. (2021), "A single case series using visuospatial task interference to reduce the number of visual intrusive memories of trauma with refugees," *Clinical Psychology & Psychotherapy*.
- `iyadurai2019intrusive`: Iyadurai et al. (2019), "Intrusive memories of trauma: A target for research bridging cognitive science and its clinical application," *Clinical Psychology Review*.
- `ehlers2000cognitive`: Ehlers & Clark (2000), "A cognitive model of posttraumatic stress disorder," *Behaviour Research and Therapy*.
- `krans2009intrusive`: Krans, Naring, Becker, & Holmes (2009), "Intrusive trauma memories: A review and functional analysis," *Applied Cognitive Psychology*.

Interpretation/theory keys:

- `brewin1996dual`: Brewin, Dalgleish, & Joseph (1996), "A dual representation theory of posttraumatic stress disorder," *Psychological Review*.
- `brewin2010intrusive`: Brewin, Gregory, Lipton, & Burgess (2010), "Intrusive images in psychological disorders: Characteristics, neural mechanisms, and treatment implications," *Psychological Review*.
- `brewin2014episodic`: Brewin (2014), "Episodic memory, perceptual memory, and their interaction: Foundations for a theory of posttraumatic stress disorder," *Psychological Bulletin*.
- `brewin2014contextualisation`: Brewin & Burgess (2014), "Contextualisation in the revised dual representation theory of PTSD: A response to Pearson and colleagues," *Journal of Behavior Therapy and Experimental Psychiatry*.
- `kindt2009beyond`: Kindt, Soeter, & Vervliet (2009), "Beyond extinction: Erasing human fear responses and preventing the return of fear," *Nature Neuroscience*.
- `baddeley2000working`: Baddeley & Andrade (2000), "Working memory and the vividness of imagery," *Journal of Experimental Psychology: General*.
- `bourne2010distraction`: Bourne, Frasquilho, Roth, & Holmes (2010), "Is it mere distraction? Peri-traumatic verbal tasks can increase analogue flashbacks but reduce voluntary memory performance," *Journal of Behavior Therapy and Experimental Psychiatry*.

Retrieved-context / modeling keys:

- `howard2002distributed`: Howard & Kahana (2002), "A distributed representation of temporal context," *Journal of Mathematical Psychology*.
- `polyn2009context`: Polyn, Norman, & Kahana (2009), "A context maintenance and retrieval model of organizational processes in free recall," *Psychological Review*.
- `polyn2009task`: Polyn, Norman, & Kahana (2009), "Task context and organization in free recall," *Neuropsychologia*.
- `sederberg2008context`: Sederberg, Howard, & Kahana (2008), "A context-based theory of recency and contiguity in free recall," *Psychological Review*.
- `kahana1996associative`: Kahana (1996), "Associative retrieval processes in free recall," *Memory & Cognition*.
- `mensink1989model`: Mensink & Raaijmakers (1989), "A model for contextual fluctuation," *Journal of Mathematical Psychology*.
- `yonelinas2019contextual`: Yonelinas, Ranganath, Ekstrom, & Wiltgen (2019), "A contextual binding theory of episodic memory: Systems consolidation reconsidered," *Nature Reviews Neuroscience*.
- `talmi2019retrieved`: Talmi, Lohnas, & Daw (2019), "A retrieved context model of the emotional modulation of memory," *Psychological Review*.
- `cohen2022memory`: Cohen & Kahana (2022), "A memory-based theory of emotional disorders," *Psychological Review*.
- `healey2014memory`: Healey & Kahana (2014), "Is memory search governed by universal principles or idiosyncratic strategies?", *Journal of Experimental Psychology: General*.
- `lohnas2023event`: Lohnas, Healey, & Davachi (2023), "Neural temporal context reinstatement of event structure during memory recall," *Journal of Experimental Psychology: General*.
- `busemeyer2000model`: Busemeyer & Wang (2000), "Model comparisons and model selections based on generalization criterion methodology," *Journal of Mathematical Psychology*.

General dissociation/modeling analogy keys:

- `benjamin2010representational`: Benjamin (2010), "Representational explanations of 'process' dissociations in recognition: The DRYAD theory of aging and memory judgments," *Psychological Review*.
- `polyn2025capacity`: Polyn & Woodman (2025), "Capacity not required: A long-term memory model that exhibits key signatures of working memory," *Psychological Review*.

## Output Requested

Return only:

1. A revised `# Introduction` section, with one sentence per line.
2. A short note listing major changes made and why.

Do not rewrite the abstract.
Do not write later manuscript sections.
Do not expand the literature review beyond the constraints above.
