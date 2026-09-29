# Holistic manuscript and feedback audit

Status: assessment and proposed finishing work, completed 29 September 2026.
This audits the manuscript state reached on 28 September; the audit crossed midnight.
This audit does not implement manuscript changes or accept pending suggestions.
The current `index.qmd`, including its decisions and proposed wording, is authoritative.
Earlier drafts and planning notes are evidence of previous choices, not instructions to restore those drafts wholesale.

## Overall assessment

The revision substantially addresses the Henson/Holmes feedback and most of Deborah's substantive concerns.
The principal additions have identifiable purposes in the feedback or meeting discussion.
It is a substantial revision, however, and should not be described to collaborators as involving only small wording changes.
The strongest case for its scope is that the changes answer specific concerns while retaining the paper's central argument and analyses.

The most important unfinished work is concentrated in Model Specification and the parameter tables.
Some accuracy corrections present in the later QMD draft were not carried into the pooled-review draft.
A remaining categorical sentence also needs to catch up with the sensitivity results.
These require local corrections to the manuscript's description, not changes to the model or new simulations.

All 47 active threads are marked resolved: 36 from Rik, 10 from Emily, and the meeting-analysis thread c385 from Jordan.
Every original Rik and Emily suggestion has an accept/reject decision.
There are 367 pending Jordan records, of which 164 have original Word provenance and 203 are later local records.
That count includes granular changes and native revision records; it is not a count of 367 newly rewritten passages.
Resolution records Jordan's response, not the collaborator's subsequent agreement, and does not accept the proposed wording.

## Basis and limits

Read the current proposed manuscript from title through Discussion and Supplementary Material, the 47 complete discussion threads and replies, and the 54 Deborah comment wordings in the [feedback register](../26_09_2026/minimal_feedback_review.md:1169).
The register contains 49 comments from the later July review and five additional wordings from the 14 July review.
Checked the original later-July Word comment anchors for the remaining structural and terminology concerns.
Also consulted [Deborah's additional feedback and Jordan's reflections](../advisor_feedback_notes.md), the [July meeting record](../meeting_notes_2026-07-03.md), and the [meeting notes stored as August](../meeting_notes_august.md).
The latter filename does not establish when the meeting occurred.

Applied the [recovered writing standards](../../../eventcmr/notes/22_09_2026/theoretical_implications/writing_standards.md): reason at passage level, make the smallest effective edit, explain mechanisms concretely, preserve empirical breadth, and distinguish findings from proposed processes and future tests.
The standards document separates Jordan's quotations from assistant synthesis.
Old feedback plans were used as finding aids rather than evidence that a repair is already present.

Checked the reported sensitivity and repetition conclusions against their saved results, and the newly identified specification issues against the implementation and fit file.
This was not an independent rerun of the simulations, an exhaustive verification of every cited paper, or a visual audit of the figures or rendered documents.
Tommy's separate annotated draft was not treated as an additional accepted revision agenda in this pass; the pooled review and the explicitly incorporated Deborah/meeting feedback define the present scope.

## Finishing work, in priority order

### 1. Restore the missing model-description corrections

The current specification defines recall context as including temporal and source components, then writes Equations 12 and 13 using one retrieval drift rate.
The implementation updates those components separately: temporal retrieval drift is approximately .678, whereas source-context retrieval drift is fixed at 1.
The latter rate is also absent from the current parameter table.
Monitoring scales both updates, rather than making the two underlying rates equal.

Relevant locations: [current recall update](../../index.qmd:466), [monitoring description](../../index.qmd:492), [implementation](../../selective_interference_v2/cmr.py:398), and the [fit's fixed values](../../work/fitting/Dupertuys2026_eCMR_source_only_phi_no_shared_support_best_of_1.json:2).
The [later draft](../../archive/2026-09-27-before-root-consolidation/previous-root/index.qmd:471) already distinguished the two updates explicitly.

The current Equations 6 and 8 also introduce an additional context-to-feature learning scale, lambda, without specifying its value.
There is no separate corresponding free scale in this implementation: temporal learning uses the primacy rate and the applicable task multiplier.
The [later draft](../../archive/2026-09-27-before-root-consolidation/previous-root/index.qmd:383) removed lambda and explicitly defined the primacy function.
That is a focused accuracy correction worth recovering, subject to checking the exact proposed wording and native equation tracking.
It does not justify importing the rest of the later Model Specification over the current manuscript.

Do not change fitted values, simulation settings, or results to resolve these description problems.
The fit distinguishes the source retrieval rate fixed at 1 from estimated source encoding drift of approximately .696.
The current simulation overrides for primacy (.100 and 1.500) and baseline source learning (.050) are already recorded in the analysis settings.
State those choices clearly without reinstating the rejected per-parameter provenance column or inventing an empirical justification for them.

### 2. Complete Deborah's parameter-table response

Deborah's DT-482 says: “I think it’s best not to list them twice, so suggest uniting with table 1”.
The current draft still has a notation/role/use table and a value/role table with overlapping parameter definitions: [Table 1](../../index.qmd:328) and [Table 2](../../index.qmd:567).
This request is not implemented simply because the historical review plan says table duplication was removed.
The later archived QMD also contains both tables, so the old completion label should not be relied on.

A single parameter table can give the relevant definitions and numerical values, while the surrounding prose already defines the vectors and matrices.
The merged table should include the separate source retrieval rate and a concise note distinguishing fitted, fixed and overridden settings.
This is a direct response to feedback, not a reason for a broader Methods rewrite.

### 3. Align the remaining control claim with the sensitivity analysis

The specification still says:

> Therefore, unlike start-of-film reinstatement and retrieval monitoring, a maintained film-category cue can reduce the effect of those task competitors on film recall.

See [the current sentence](../../index.qmd:516).
The unqualified “unlike” implies that reinstatement and monitoring cannot reduce interference at all.
The current Results and c349 reply correctly acknowledge limited protection on simpler comparisons while distinguishing the full reminder-dependent selective-protection contrast.
The saved [sensitivity results](../../work/simulation2_control_parameter_sensitivity/results/RESULTS.md) support that distinction.
The sentence predates the new analysis; the problem is incomplete follow-through rather than an error in the new sensitivity paragraph.

Revise this local contrast so it describes the cue's selective support without categorically denying the smaller effects of the other operations.
The abstract, Results and conclusion already bound the requirement claim to reproducing the pattern across reminder and task conditions in the simulations.
They need not be reopened merely to weaken that finding.

There is also a smaller ordering inconsistency: the theory, figures and summaries use start reinstatement → maintained cue → monitoring, whereas the formal specification presents start reinstatement → monitoring → maintained cue.
Deborah's DT-379 concerned inconsistent ordering.
The original theory-level mismatch is repaired; harmonizing the formal presentation would be a reasonable finishing edit, but is less urgent than correcting the equations and overstatement.
Any accepted relocation should retain the pending wording changes within it, following the agreed treatment of earlier moves.

### 4. Repair citation destinations without rebuilding the bibliography

The correct references are present, but five imported anchors sit on the wrong reference entries:

| Citation target | Entry currently carrying the anchor | Source |
| --- | --- | --- |
| Bird et al. (2012) | Berntsen (2021) | [Reference entry](../../index.qmd:963) |
| Deeprose et al. (2012) | Cortis Mack et al. (2017) | [Reference entry](../../index.qmd:983) |
| Dupertuys et al. (2026) | Diamond and Levine (2020) | [Reference entry](../../index.qmd:987) |
| Healey and Kahana (2016) | Healey (2018) | [Reference entry](../../index.qmd:997) |
| Norman et al. (2017) | Mundorf et al. (2021) | [Reference entry](../../index.qmd:1087) |

Two Kessler (2020) citations still target the Kessler (2018) entry, in the [Simulations opening](../../index.qmd:538) and [Discussion](../../index.qmd:869).
The corresponding introduction citation has already been corrected.
These wrong destinations are also present in the comparison reference, so they are inherited problems rather than evidence that the recent scientific revisions broke the citations.
Repairing them does not require converting the manuscript's literal citations into a new bibliography system.

### 5. Finish small, traceable feedback and copy corrections

- **DT-454 / DT-252:** Deborah explicitly asked to eliminate “reminder-linked”.
  It reappears in the new diagnostic lead-in at [index.qmd:777](../../index.qmd:777).
  Replace that one occurrence with ordinary wording about interference following a reminder.
- **DT-484:** the Visser et al. (2018) paper Deborah supplied is present in References but is not cited in the proposed body.
  The broader-memory motivation requested in DT-483 is present.
  A local citation in the existing [reconsolidation/post-reactivation sentence](../../index.qmd:85), if retained as the intended use of this paper, would finish the more specific reference request.
- **Figure 6 caption:** the local terminology revision now gives “stronger task associations reduce recall from film positions and increases recall from task positions”.
  Change “increases” to “increase” at [index.qmd:648](../../index.qmd:648).
  This is a small new agreement error, not a reason to rewrite the caption.

### 6. Presentation and status records to check at the next appropriate step

The dual-list paragraph is still a source heading, and the HTML outline adapter recognizes its old wording, “would isolate these predictions”.
Pending s494 changes that wording to “would isolate the roles of competitor learning and cue discriminability”.
See [source paragraph](../../index.qmd:915) and [outline adapter](../../presentation/manuscript-outline.lua:17).
The old phrase remains inside the pending deletion, so this audit does not establish that the current redline HTML is broken.
The correction is nevertheless dependent on revision text and may fail for a proposed-only or accepted version.
Treat this as a source/presentation check when that output is next requested; do not describe it as a visually observed rendering failure.

The [root README](../../README.md:1) still describes the body as at the pooled baseline, the abstract comments as active, and Word as the title-stage export.
Those status statements are obsolete.
The [positional-figure README](../../work/retrieval_control_position_comparison/README.md) and [notes index](../README.md:9) also retain language about an outstanding experimental-data question despite the recorded decision not to add those analyses.
These records should be updated as status documentation rather than converted into new manuscript obligations.
The live replies on c357, c355, c366 and c368 describe completed work and the current decisions correctly.

## What the larger changes accomplish, and why I would retain them

| Change | Feedback or decision | Assessment of scope |
| --- | --- | --- |
| Revised abstract | c21, c22, c24, c32; Jordan expressly chose a good coherent abstract over preserving nearly all original wording | More than a minimal line edit, but explicitly authorized and consistent with the paper's results. Recognition remains omitted. |
| Goal → construction/maintenance of a cue → selective support | Abstract decisions, c70/c92, control discussion | Necessary positive explanation. The absence of simulated step-by-step cue construction does not make the account inherently circular. |
| Recognition before control, shorter prose and two-panel figure | c92, c102, c110–c112, c129, c368, c374; meeting discussion | A reasoned response to requests to move or remove recognition. Retaining it is a documented disagreement with deletion, not overlooked feedback. |
| 121-setting sensitivity analysis | c349 | Directly tests whether the conclusion depends on default reinstatement/monitoring values. No further parameter search is required by this audit. |
| Matched positional diagnostics and retained output-order diagnostic | c354, c355, c357, c366, c383 | Directly requested. Figure 10 isolates each operation; Figure 11's caption discloses that reinstatement is present. |
| Repeated versus unique scoring | Meeting question; c385 records the reason for the addition | A compact robustness analysis. The manuscript correctly limits it to one retrieval sequence, not diary recurrence across days. |
| Concrete film/task/delay examples and hotspot references | c119, c162, meeting notes | Necessary explanatory detail. Hotspots are a subset of film moments, and the model's representational limits remain explicit. |
| Shared imagery format hypothesis and Tetris-imagery evidence | c381, Emily's supplied references, meeting discussion | Answers the missing task-content explanation without claiming that visual overlap was implemented or that competition was empirically established. |
| Neutral-material prediction | c117/c368, meeting suggestion | Clearly untested. The decision not to add an emotional-versus-neutral simulation is preserved. |
| Balanced clinical/laboratory appraisal | c377–c379 | Restores positive aggregate and clinical findings while separating intrusion reduction, selective interference and evidence for the proposed mechanism. |
| General-memory experiment | Existing Discussion passage, c357/c383 and prior broader-memory decisions | The substantial dual-list proposal predates this latest round. Preserve its role; it is not a new third simulation or a commitment to collect data now. |

Saved repetition results give selective protection of .7866 with repeats prohibited, .7798 with repeats allowed but unique items scored, and 1.0612 with all events scored.
That supports the manuscript's qualitative description: protection survives unique scoring and repetitions amplify the total-event contrast.
The sensitivity record reports no positive full reminder-specific protection among the 121 no-cue combinations, while some simpler contrasts show modest protection.
Neither result warrants reopening the already agreed central conclusion.

As a rough scope indicator, normalized source-word counts from Abstract through Discussion rose from about 11,416 to 12,325, approximately 8%.
The Discussion rose from about 1,847 to 2,319, approximately 26%.
These counts include captions, tables, citations and mathematical tokens, exclude reference entries and review discussions, and compare against the current reference with accepted structural moves.
They are not journal word counts and do not measure gross wording turnover.
They indicate that the revision is substantial and the Discussion deserves restraint, not that any particular addition should be removed.

The main remaining scope risk is starting another general polishing or restructuring round.
The present introduction/theory/specification overlap is not wholly eliminated, but each has an identifiable job.
A new decision to interleave all theory and Results, give goal cueing a separate simulation, or build a third analysis from neutral material would exceed the finishing work identified here.

## Henson/Holmes and meeting-thread coverage

“Addressed” means that the implemented response is identifiable and proportionate; it does not certify reviewer agreement.
All listed threads are resolved in the source.

| Threads | Current response | Audit outcome |
| --- | --- | --- |
| c1 | Title identifies trauma-film selective interference and the shared-system account | Addressed; keep the approved title. |
| c21, c22, c24 | Task memories, intrusions, context and involuntary retrieval explained in the abstract | Addressed. |
| c32 | Recognition omitted from the abstract and retained in the main text | Addressed. |
| c37, c41 | McConnell methods citation and Lau-Zhu citations added | Addressed. |
| c70 | Contribution framed around susceptibility to interference, not simply raising recall | Addressed. Preserve the causal cue account. |
| c86 | Context can remain active after the film or become active again following a reminder | Addressed. |
| c92 | Recognition explained before deliberate recall and its control requirements | Addressed. |
| c94 | Emotional variant's source-context adaptation explained | Addressed; no claim that emotion's contribution was independently tested. |
| c102, c110, c111, c112, c374 | Recognition moved before control; supporting role retained; introduction ends on recall | Documented retain-and-shorten decision rather than literal acceptance of removal. |
| c104 | “Task phase”/“task condition” replace the queried label | Addressed. |
| c115 | Redundant recognition roadmap removed | Addressed. |
| c117 | Neutral-material generalization stated as untested | Addressed within agreed scope. |
| c119, c162 | Concrete task/delay examples; film hotspots distinguished and Singh cited | Addressed; examples do not claim to solve general falsifiability concerns. |
| c120, c128, c133 | Conceptual figures use descriptive pathway labels; formal notation retained in specification | Figure choices and captions support the replies. No new visual inspection in this audit. |
| c123, c124 | “Instead” removed; opening states the goal/control comparison; “target episode” used | Addressed. |
| c126 | Instruction-context associations explain recovery; implementation represents the resulting shift | Addressed without demanding new instruction-encoding simulations. |
| c129, c368 | Brief recognition explanation and simplified Figure 7 retained; neutral prediction added | Documented response, including reason for declining removal and further simulation. |
| c318 | Evidence-level recognition scope and need for an additional decision rule stated | Addressed without inventing accuracy predictions. |
| c344 | Figures 5, 7, 8 and 9 follow their explanatory passages; 10–11 have lead-ins | Addressed in source order; accepted moves preserve readable wording changes. |
| c345 | Current prose/captions use involuntary/deliberate distinctions; revised graphics selected | Addressed at source/provenance level; historical IDs and filenames appropriately remain unchanged. |
| c346 | Redundant numerical recall/evidence totals removed; methods retain settings | Addressed. |
| c349 | Finite-grid robustness analysis and distinction between contrasts reported | Main response addressed; specification sentence still needs alignment, as above. |
| c354, c355, c366 | Diagnostic rationale and matched three-mechanism positional figure | Addressed. |
| c357 | Diagnostic purpose and item/position/order recording explained; no existing-data analysis promised | Addressed; obsolete package notes do not reopen the decision. |
| c371 | Discussion begins with the empirical problem, dual-representation interpretation and alternative | Addressed. |
| c375 | Proposed VIT cue-maintenance reconciliation made explicit and identified as unestablished | Addressed; diary-null qualification retained. |
| c377, c378, c379 | Balanced clinical evidence and distinct claims about reduction, selectivity and mechanism | Addressed in the latest passage. |
| c381 | Task imagery, format versus content/source, existing Tetris-imagery evidence and a discriminating test | Addressed as a bounded theoretical proposal, not a validated account of task superiority. |
| c383, c384 | Ending identifies the key result and separable, potentially co-occurring control operations | Addressed. |
| c385 | Meeting-derived repetition analysis and its limits documented | Addressed. |

## Deborah coverage

The IDs below refer to the [historical source-comment register](../26_09_2026/minimal_feedback_review.md:1169), not active thread IDs in `index.qmd`.

| Source comments | Current assessment |
| --- | --- |
| DT-2, DT14-1 | Title has been replaced with the approved, more direct formulation. |
| DT-9 | Abstract rewritten for accessibility; Jordan explicitly approved that broader revision. |
| DT-27, DT-32, DT-33, DT-76, DT-79 | ICTI is defined more broadly than Tetris without assuming a working-memory account. Empirical breadth is retained. This does not certify that every potentially relevant citation is included. |
| DT-82, DT-84, DT-147, DT-148 | General-memory contribution is clearer. Unsupported universal “first account” language has not been restored. The current paragraph sequence reflects later explicit choices. |
| DT-144, DT-252, DT-253, DT-254, DT-454, DT14-124 | Immediate activation and later reinstatement are distinguished. One newly reintroduced “reminder-linked” remains to repair. |
| DT-176 | Citation additions are implemented; surrounding empirical examples are retained rather than narrowed. |
| DT-184, DT-220, DT-223, DT-271, DT-310, DT-311, DT-318, DT-323, DT-324, DT14-66, DT14-102 | Definitions, transitions and separate explanatory jobs are substantially improved. Some cross-section repetition remains, but does not justify an unrequested wholesale rewrite. |
| DT-225 | Laboratory origins, incidental encoding and nonlaboratory temporal-contiguity evidence are explained. |
| DT-248, DT-249, DT-435 | Film/task/delay events are concretely introduced; imagery is distinguished from implemented content representation. |
| DT-328, DT-346, DT-479 | The broader deliberate-retrieval question is explicit. Interleaving the whole paper was an alternative, subsequently declined in favor of the accepted simulation order. Do not silently revive it. |
| DT-337, DT-347, DT-348 | Control processes are introduced and developed as stages of retrieval, with the retrieval-goal problem made explicit. |
| DT-379 | Theory-level order is consistent; formal specification still reverses cueing and monitoring. Local harmonization remains possible. |
| DT-405, DT-407 | The old results-like theory paragraph is gone. The surviving specification contrast still needs the bounded correction identified above. |
| DT-432, DT-434, DT-456, DT-462, DT-472, DT14-101 | Shared sampling, simulation roles and externalized recall/monitoring are explained. Separately, recover the identified mathematical accuracy corrections. |
| DT-476 | Recognition's evidence-only scope is stated before the formal measure. |
| DT-482 | Still incomplete: tables remain duplicated. |
| DT-483 | Everyday reminders, autobiographical/museum/smartphone findings and Berntsen are present. Do not add recurrence literature merely to satisfy an unbounded reference wish list. |
| DT-484 | Supplied Visser paper is in References but lacks the intended body citation. |
| DT-489 | Context-overlap figure is supplementary, with a main-text pointer. |

The additional advisor notes' concerns about opening accessibility, general framing, hippocampal/sensory accounts, clinical balance and abstract emphasis are substantially reflected in the current version.
Their suggested recognition material in the abstract is superseded by the later explicit decision to omit it.
Their broad instruction to state that a reminder is essential should not be converted into a universal empirical claim; the manuscript appropriately distinguishes immediate and delayed procedures and describes the modeled reminder contrast.

## Verification and recommended stopping point

The review source parses successfully, all 47 active comment anchors contain text in the proposed projection, source decisions validate, and comparison with `reference.qmd` completes.
The earlier review-boundary failure reported by a side chat is not present in this check.
The manuscript, reference, bibliography and project configuration hashes were unchanged during the audit.
No HTML was inspected or rendered, no Word file was generated, and no pending suggestion was decided.

Finish the model-description/table unit, the one overbroad control contrast, and the small citation/wording repairs.
Review exact passage-level edits and tracking treatment before implementation.
Then reassess only the affected passages and reply consistency.
This audit supplies no reason to add another simulation, collect new data, rebuild the bibliography workflow, or restart the paper's structure.
