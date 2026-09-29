# Retrieval terminology audit

Implementation update: the source changes and remaining Figure 10 replacement are now implemented.
See the [figure integration audit](rik-positional-figures-integration.md) for the completed work and current review state.
The checklist below records the original audit.

Status: audit and proposed implementation, not manuscript changes.
Prepared 28 September 2026 against the current proposed reading of `index.qmd`, accounting for suggestion decisions rather than treating deleted text as live prose.
No manuscript, comment state, figure, comparison baseline, runtime or output was changed for this audit.

## Outcome

The terminology decisions remain useful, but the current pooled-review draft has not inherited all the changes made in the later Word/QMD drafts.
There are **32 remaining occurrences of “unguided” in live prose and captions**, plus **one duplicate in Figure 5’s image description**.
Six attached graphics contain the old label: **Figures 1, 2, 4, 8, 9 and 10**.
These contain seven “Unguided” labels, because Figure 1 uses it in both panels.

The right repair is contextual, not a global replacement of “retrieval” with “recall”.
Preserve the approved abstract’s **involuntary retrieval**.
Use **involuntary recall / deliberate recall** for parallel recall conditions, preserve **deliberate recognition**, and distinguish empirical measures from simulated outputs.
For comparisons between control operations, name the operation or starting state instead of treating every condition as an intentionality category.

## Decisions recovered from the earlier drafting process

The primary evidence is the [August editing conversation](/Users/jordangunn/.codex/sessions/2026/08/23/rollout-2026-08-23T18-25-02-01a02fa7-847b-7580-9cab-30b56dda18f2.jsonl), supplemented by the current manuscript’s review records and this chat.
Line numbers below identify messages in that local transcript, not manuscript lines.

| Decision | Evidence and implication |
|---|---|
| Retire “unguided” as the manuscript’s retrieval-condition label. | At line 3400, Jordan said “we will definitely not keep ‘unguided recall’ or the like”; at 9350, he requested a contextual audit rather than a blanket substitution. |
| Use parallel recall labels in Figure 1. | At 10665, Jordan challenged “Involuntary retrieval” beside “Deliberate film recall”; at 10807 he proposed “involuntary recall”, “deliberate recall” and “deliberate recognition”, then authorized implementation at 10819. |
| Use empirical umbrella terms in Figure 2. | At 10989, Jordan explicitly approved **Intrusive memory / Voluntary memory**, retained the study-specific measure names, and declined reminder-label cleanup without supporting feedback. |
| Keep Figure 4’s recall labels parallel. | The proposal at 11265 used **Involuntary recall / Deliberate recall** and removed MCF/MFC shorthand from the graphic and caption; Jordan approved at 11271. |
| Preserve literal output labels. | The Figure 5 discussion at 11683–11705 retained “Film recall across all trials” and “Mean film items recalled”, with **involuntary-recall condition** in the caption. |
| Describe manipulated associations precisely. | The Figure 6 proposal at 11890 distinguished stronger task associations from the timing of task encoding; Jordan approved at 11896. |
| Do not reopen all earlier figure proposals. | At 12250, Jordan said the other figure issues were matters he had actively decided to leave as they were. Earlier assistant suggestions are therefore not automatically outstanding obligations. |
| Preserve the newer abstract decision. | Current resolved c22 and c24 explicitly distinguish empirical “intrusions” from **involuntary retrieval** in the simulations. The corresponding wording suggestions remain pending; resolution did not accept them. |

The [August meeting notes](/Users/jordangunn/workspace/selective_interference_v2/notes/meeting_notes_august.md) support the involuntary/deliberate distinction and identify ambiguity in “guided”.
The older [structural decisions file](/Users/jordangunn/workspace/selective_interference_v2/notes/22_08_2026/structural_decisions.md) records an earlier preference for “involuntary retrieval” in graph labels.
That was subsequently refined by the explicit figure discussions above; it is not a universal rule to reinstate.

## Working terminology

| What the passage describes | Use | Keep the distinction clear |
|---|---|---|
| Retrieval as a general process, including the approved abstract | Involuntary retrieval | No need to replace every natural use of “retrieval”. |
| Parallel recall conditions | Involuntary recall / deliberate recall | Include “film” in both labels when helpful; Figure 1’s shorter labels were explicitly chosen. |
| A supplied-item test | Deliberate recognition | Recognition is not a recall condition. |
| Figure 2’s heterogeneous empirical outcomes | Intrusive memory / voluntary memory | Retain diary intrusions, recognition, free recall and laboratory report labels within the columns. |
| Literal model outputs and axes | Film items recalled, recall probability, output position | Do not relabel these as measured intrusion counts. |
| A comparison of retrieval starting states | Ongoing context / start-of-film context reinstatement | This identifies the manipulated mechanism rather than suggesting a complete contrast between involuntary and deliberate remembering. |
| A comparison of combinations of three control operations | No control operations; the names of the included operations | The caption must identify the three operations; weak film cues can still be present. |
| The model’s sampling mechanism | Context-guided search/recall | “Guided” here identifies what directs sampling, not the deprecated condition name. |

The qualification at manuscript line 533 already explains that the involuntary condition models film material coming to mind without deliberate intent and does not reproduce diary or laboratory intrusion procedures.
Keep that qualification, changing its condition name as specified below.
Do not add “analogue” to every label or describe involuntary retrieval as necessarily uncued.
The simulations explicitly include weak film cues.

## Exact proposed source changes

These are local differences against the **current proposed reading**: ~~deletions~~ and **additions**.
The links identify source lines at the time of this audit; locate the wording again before implementation if the manuscript changes.
For rows that only replace one word, the surrounding sentence stays intact.

### Introduction and theoretical account

| ID | Location | Proposed local difference |
|---|---|---|
| T01 | [128, Figure 1A caption](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:128) | “a later test of ~~unguided or deliberate film recall~~ **involuntary recall, deliberate recall, or deliberate recognition**.” This also describes the recognition branch already drawn in Panel A. |
| T02 | [130, Figure 1B caption](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:130) | “rows distinguish ~~unguided film recall from deliberate film recall~~ **involuntary recall from deliberate recall**” to match the approved graphic labels. |
| T03 | [131, Figure 1B caption](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:131) | “reduces ~~unguided film recall more than deliberate film recall~~ **involuntary recall more than deliberate recall**.” The surrounding caption already identifies film recall as the quantity. |
| T04 | [164, intentionality/test-format conclusion](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:164) | “~~unguided~~ **involuntary** versus deliberate recall”. Preserve the recognition clause and c111. |
| T05 | [171, theory roadmap](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:171) | “deliberate and ~~unguided~~ **involuntary** recall”. |
| T06 | [234, comparison with previous modeling](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:234) | “across ~~unguided~~ **involuntary** and deliberate recall”. |
| T07 | [271, Figure 4A caption](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:271) | “~~Unguided~~ **Involuntary** and deliberate recall”. |
| T08 | [272, Figure 4A caption](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:272) | “~~Unguided~~ **Involuntary** recall begins from ongoing context”. |

### Model specification and simulation overview

| ID | Location | Proposed local difference |
|---|---|---|
| T09 | [439, sampling](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:439) | “~~Unguided~~ **Involuntary** and deliberate recall”. |
| T10 | [474, control settings](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:474) | “the same sampling rule as ~~unguided~~ **involuntary** recall”. |
| T11 | [500, maintained cue](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:500) | “absent during ~~unguided~~ **involuntary** recall”. This names the modeled condition, not a claim that involuntary remembering has no cues. |
| T12 | [532, simulation target](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:532) | “reduces ~~unguided~~ **involuntary** film recall more than deliberate film recall”. |
| T13 | [533, model qualification](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:533) | “~~Unguided recall~~ **The involuntary-recall condition** provides a simplified model of film material coming to mind without deliberate intent to retrieve it; it does not reproduce diary or laboratory intrusion procedures.” |

### Simulation 1

| ID | Location | Proposed local difference |
|---|---|---|
| T14 | [607, opening](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:607) | “competitors for ~~unguided~~ **involuntary** film recall”. |
| T15 | [620, Figure 5 title](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:620) | “Simulation 1: ~~unguided~~ **involuntary** film recall by reminder condition and task association strength.” |
| T16 | [620, Figure 5 design sentence](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:620) | “while ~~retrieval mode was held unguided~~ **all trials used the involuntary-recall condition**; weak film cues were supplied periodically during recall in every condition.” |
| T17 | [624, Figure 5 conclusion](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:624) | “isolating the ~~unguided-retrieval component~~ **involuntary-recall component** of the selective interference effect.” |
| T18 | [639, Figure 6 design sentence](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:639) | “while ~~retrieval was held unguided~~ **all trials used the involuntary-recall condition**; weak film cues were supplied periodically during recall in all conditions.” |
| T19 | [647, conclusion](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:647) | “competitors for ~~unguided~~ **involuntary** film recall”. |

**A01 — image description:** make the same T15 word replacement in Figure 5’s `alt` text at [line 618](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:618).
This is a second source occurrence of the title, not an additional visible caption or a reason to regenerate Figure 5’s graphic.

### Simulation 3: deliberate recall control

| ID | Location | Proposed local difference |
|---|---|---|
| T20 | [691, opening comparison](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:691) | “compares ~~unguided~~ **involuntary** and deliberate film recall”. |
| T21 | [700, sensitivity methods; within s331](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:700) | “relative to ~~unguided retrieval~~ **the involuntary-recall condition**.” Amend the wording of Jordan’s pending addition; retain its pending status. |
| T22 | [707, Figure 8 design](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:707) | “between ~~unguided~~ **involuntary** film recall and deliberate film recall”. |
| T23 | [711, Figure 8 interpretation](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:711) | “under ~~unguided~~ **involuntary** film recall”. |
| T24 | [712, Figure 8 result](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:712) | “under ~~unguided~~ **involuntary** film recall than under deliberate film recall”. |
| T25 | [713, Figure 8 conclusion](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:713) | “reduces ~~unguided~~ **involuntary** film recall”. |
| T26 | [718, c345 anchor](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:718) | “In ~~unguided~~ **involuntary** film recall”. Keep Emily’s anchor attached to the terminology change. |
| T27 | [728, Figure 9 caption](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:728) | “~~Unguided film recall~~ **The involuntary-recall condition** includes none of the three deliberate-control operations.” This connects the condition to the proposed graphic label “No control operations”. |
| T28 | [744, sensitivity results; within s332](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:744) | “relative to ~~unguided retrieval~~ **the involuntary-recall condition**.” Preserve the 121-setting result and all qualifications about simpler comparisons. |
| T29 | [758, Figure 10 caption](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:758) | “Curves compare ~~unguided recall with retrieval initialized by~~ **recall initialized from ongoing context with recall initialized by** start-of-film context reinstatement.” This identifies the actual starting-state comparison. |

T29 and the mechanism label proposed for Figure 9 are contextual recommendations from this audit.
They should not be represented as verbatim wording Jordan already approved.
Neither changes the simulated conditions or results.

### Discussion and supplement

| ID | Location | Proposed local difference |
|---|---|---|
| T30 | [834, weak cues versus maintained cue](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:834) | “in the ~~unguided~~ **involuntary-recall** condition.” Preserve the distinction between weak film cues and the maintained discriminating cue. |
| T31 | [847, prediction](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:847) | “impair deliberate as well as ~~unguided~~ **involuntary** recall”. |
| T32 | [1071, Supplementary Figure S1](/Users/jordangunn/workspace/selective_interference_v2/index.qmd:1071) | “Reminder condition was varied before task encoding while ~~retrieval was held unguided~~ **all trials used the involuntary-recall condition**.” This is a terminology repair only; whether this encoding-context caption needs a retrieval clause is a separate editorial question. |

## Artwork audit

This audit inspected the actual attached images, not just captions or filenames.
Figure numbers below use the current accepted recognition-before-control order.
The original asset filenames retain the earlier numbering.

| Current figure | Attached image | Required terminology work |
|---|---|---|
| 1 | [image1.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image1.png) | In both panels: **Unguided film recall → Involuntary recall**, **Deliberate film recall → Deliberate recall**. Keep **Deliberate recognition**. Preserve “Film items recalled” axes and the schematic bars. |
| 2 | [image2.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image2.png) | Column headings: **Unguided film recall → Intrusive memory**, **Deliberate film recall → Voluntary memory**. Preserve every study-specific measure name, its units and the reminder labels. This is the earlier explicit decision. |
| 3 | [image3.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image3.png) | No unguided/recall-condition correction needed. MCF/MFC notation is a separate matter, not grounds for replacing this whole graphic. |
| 4 | [image4.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image4.png) | **Unguided recall → Involuntary recall** beside **Deliberate recall**. Preserve “Film candidates”, “Task competitors”, “Film recall” and the off-target recall labels. See the separately recovered acronym decision below. |
| 5 | [image5.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image5.png) | No graphic change. Keep “Example recall sequences”, “Film recall across all trials”, “Mean film items recalled” and all legend categories. Caption and image-description changes are T15–T17/A01. |
| 6 | [image6.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image6.png) | No graphic change. Keep “Recall probability”, “Encoded position” and weaker/stronger task-association labels. Caption changes are T18 and the separate association-strength recovery below. |
| 7, previously 11 | [image11.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image11.png) | No recall-condition correction. Recognition evidence remains recognition evidence; it must not become “recall” or “intrusions”. |
| 8, previously 7 | [image7.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image7.png) | **Unguided film recall → Involuntary film recall**, paired with the existing **Deliberate film recall**. Both retain “film”; there is no need to shorten these merely because Figure 1 uses shorter labels. |
| 9, previously 8 | [image8.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image8.png) | Recommend **Unguided film recall → No control operations** for the first control setting. The caption connects this to the involuntary-recall condition. Leave the other operation labels and “Mean film items recalled” intact. A global rename to involuntary recall would be acceptable but less explicit about this decomposition. |
| 10, previously 9 | [image9.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image9.png) | Recommend **Unguided recall → Ongoing context** beside **Start-of-film context reinstatement**. Preserve first-recall and recall-probability axes. This names the starting-state manipulation, not a full deliberate-control condition. Coordinate with the separately outstanding positional-figure work. |
| 11, previously 10 | [image10.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image10.png) | No terminology correction needed. “No retrieval monitoring / Retrieval monitoring” already identifies the mechanism, and “Recall probability” is the correct quantity. |
| S1 | [image12.png](/Users/jordangunn/workspace/selective_interference_v2/assets/media/image12.png) | No graphic change. Its context-similarity labels are correct; only the caption contains “unguided”. |

Existing later assets can reduce implementation work:

- [Figure 1 candidate](/Users/jordangunn/workspace/selective_interference_v2/work/empirical_target/empirical_target_composite_recognition_candidate.png) has the approved short recall/recognition labels.
- [Figure 2 source graphic](/Users/jordangunn/workspace/selective_interference_v2/work/empirical_target/empirical_selective_interference_examples.png) has **Intrusive memory / Voluntary memory**.
- [Figure 4 source graphic](/Users/jordangunn/workspace/selective_interference_v2/work/retrieved_context_account/retrieved_context_retrieval_operations_composite.png) has **Involuntary recall / Deliberate recall** and expanded pathway names.
- [Figure 8 source graphic](/Users/jordangunn/workspace/selective_interference_v2/work/simulation2_control_cued_behavioral/simulation2_control_cued_behavioral.png) has a generator using **Involuntary film recall / Deliberate film recall** for display while retaining the old internal data key.
- [Figure 9 source graphic](/Users/jordangunn/workspace/selective_interference_v2/work/simulation2_retrieval_control_decomposition/simulation2_retrieval_control_decomposition.png) has an SVG using **No control operations**, but also changes “Full deliberate control” to “All three controls”. Do not silently import that additional change.
- [Figure 10 candidate](/Users/jordangunn/workspace/selective_interference_v2/work/simulation2_start_context_reinstatement/simulation2_start_context_reinstatement_film_positions_candidate.png) has a generator mapping the old data key to **Ongoing context**. Its plotted scope must be checked against the agreed positional-figure work before reuse.

These are reuse candidates, not certification that every pixel or plotted value matches the current attached figure.
Check the source/data and nonlabel differences before adopting one.
Do not import a broader redesign or new analysis under a terminology-only change.

## Related earlier decisions worth recovering separately

These are adjacent repairs, not additional “unguided” occurrences.
Keep them separately identifiable in the tracked changes.

**R01 — Figure 1’s task terminology and recognition branch.**
At line 128, change “an intervening task” to “a task phase”, retaining c104 on the edited phrase.
At line 129, change “intervening task” to “task condition”.
Keep “intervening delay”: it accurately describes the interval.
T01 above adds the recognition branch already present in Panel A.
Preserve Rik’s pending caption edits s79–s81 and do not resolve c111/c112 merely because the terminology is repaired.

**R02 — Figure 4’s unexplained pathway abbreviations.**
The earlier approved change removes “(MCF)” and “(MFC)” from this conceptual graphic, retaining the full pathway names.
In its caption at line 278, replace “MCF or MFC pathways” with “context-to-feature or feature-to-context pathways”.
This is relevant to c128 and readability, but it does not establish a policy of deleting matrix notation from the formal specification or every other figure.

**R03 — Figure 6’s association-strength wording.**
Recover the earlier local distinctions in the caption:

- “**Strong task encoding** after a film reminder shifts recall from film to task items” → “**Strengthening task associations** after a film reminder shifts recall from film to task items”.
- “when **task encoding is strengthened**” → “when **task associations are strengthened**”.
- “**strong task encoding reduces**” → “**stronger task associations reduce**”.
- “Curves compare **weak and strong task encoding**” → “Curves compare **weaker and stronger task associations**”.

Update the duplicate title in Figure 6’s image description if this title change is adopted.
Keep “when task encoding follows a film reminder”, which describes temporal order rather than association strength.
The graphic already uses the appropriate association-strength labels.

**R04 — optional consistency in the new simulation overview.**
At line 536, Jordan’s pending s370 already replaces the old wording with “the involuntary-retrieval condition”.
That is not an unresolved “unguided” occurrence.
For the direct contrast with deliberate recall, “the involuntary-recall condition” would follow the figure-level convention more closely.
Treat this as a small proposed refinement of the existing pending addition, not a reason to reopen the abstract or claim the previous approved wording was wrong.

## What stays unchanged

- The approved abstract, including s324/s325 and the c22/c24 replies and resolved states.
- The contribution paragraph’s general comparison of involuntary retrieval with deliberate recall and recognition.
- The roadmap’s already-pending “involuntary” replacement s363.
- “Context-guided search”, “context-guided recall”, “item-guided access”, the audio-guided museum-tour description, and the published article title containing “guided”. These do not name the obsolete condition.
- Literal model-output labels and the empirical study-specific measures in Figure 2.
- Old text on the deletion sides of s339/s341, s363, s370 and s267. Those are preserved review history, not live wording to repair again.
- Historical comment bodies and replies, including Emily’s request mentioning “guided”, and older discussion of unguided retrieval.
- The frozen source, comparison baseline, archived drafts, figure IDs, cross-reference targets, filenames and internal data keys such as `Unguided recall`. Stable identifiers are not reader-facing terminology.
- The goal → construction and maintenance of a discriminating retrieval cue → selective support explanation, and the sensitivity analysis’s distinction between simpler protection comparisons and the full reminder-specific interaction.

The old caption-composite export utility also contains legacy wording.
It is not the source of the current native QMD captions.
Do not revive it as a second editable caption source or update every historical export to make a repository-wide text search empty.
If an active figure generator is used, ensure its display labels produce the intended new wording while its data-selection keys retain their meaning.

## Tracking and comment handling when implemented

1. Add local pending suggestions under Jordan’s name for unchanged base prose; do not replace complete paragraphs to rename one condition.
2. For T21 and T28, amend the wording within Jordan’s pending s331/s332 additions, retaining their identities, attribution and pending status.
   Do the same for R04 if adopted; avoid nesting a second change inside Jordan’s own still-pending wording merely to record this refinement.
3. Preserve all other authors’ suggestions and comment anchors, especially c104 and c345.
   A terminology pass is not authorization to accept unrelated prose or reviewer deletions.
4. Track each changed graphic as one image replacement, with its original image recoverable when rejected.
   Keep caption changes local and separate so they remain readable.
   Do not overwrite the old image bytes at the existing path and thereby make the graphic change invisible to review.
5. Keep `reference.qmd` unchanged for these wording and graphic proposals.
   Acceptance of the earlier section reorder and figure grouping does not mean acceptance of these new semantic changes.
6. After checking the proposed reading and actual revised graphics, reply to and resolve the relevant comments while leaving wording/graphic suggestions pending.
   No comment is resolved by this audit.

Proposed c345 reply, once the terminology work is complete:

> I’ve replaced “unguided” in the manuscript and figure labels.
> Recall comparisons now use “involuntary recall” and “deliberate recall”; the empirical figure uses “intrusive memory” and “voluntary memory” to cover its different measures.
> Labels for model outputs and specific control operations retain those distinctions.

Proposed c104 reply, if R01 is implemented:

> I’ve changed this to “task phase” in the procedure and “task condition” in the comparison, so the terminology does not assume that every task condition causes interference.

Proposed c128 reply, if R02 is implemented:

> I’ve replaced the abbreviations in this figure and its caption with the full context-to-feature and feature-to-context pathway names.

Leave the recognition-removal comments c111/c112 and the separate positional-figure/data follow-ups open unless their substantive questions are addressed.
Do not regenerate Word for this terminology work unless requested.

## Audit provenance

Sources checked: current QMD and review decisions, all twelve attached PNGs, relevant later figure sources/candidates, the August decision conversation, meeting notes and the later abstract decisions.
No HTML inspection or manuscript rendering was performed.
The proposed-reading count excludes review-thread quotations, deletion sides, technical identifiers and image-description duplicates.

Audited `index.qmd` SHA-256: `022eadc7450daa18e2cdbbe994bbd337829a23b855123d1b5c6842c4d9919ef0`.
Audited `reference.qmd` SHA-256: `0bebf9e5ae8efd06a93407bfdb7862044dc2982f052c370e254ce75e4f7a9645`.
These identify the audited state; the live files remain authoritative if another chat subsequently changes them.
