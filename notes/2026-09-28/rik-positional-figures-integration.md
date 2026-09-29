# Rik's positional-figure comments: audit and integration

Status: implemented in the manuscript source, 28 September 2026; manuscript outputs not refreshed.
Scope: c355 and c366, the affected Figures 10–11, their Results text and captions, and replies whose wording became stale.
The current `index.qmd` remains authoritative; earlier drafts supply decisions and useful wording, not a manuscript to restore wholesale.

## Feedback and earlier decisions

Rik's c355 questions the value of allocating two panels to first versus any recall while the text contrasts reinstatement with a maintained cue that is not shown.
His c366 requests comparable plots across all encoded positions for the three mechanisms.
The original review's Figures 9 and 10B are the current Figures 10 and 11B.
The existing replies already proposed three isolated operations against a common baseline but incorrectly narrowed c366 to film positions.

The [later draft](/Users/jordangunn/workspace/selective_interference_v2/archive/2026-09-27-before-root-consolidation/previous-root/index.qmd:790) had already made the reinstatement strength explicit and treated the predicted early-position benefit as a conditional consequence of reinstating an episode's initial context.
It still retained the two positional diagnostics; their existence does not override the present decision to address Rik's comparison directly.
The [earlier feedback synthesis](/Users/jordangunn/workspace/selective_interference_v2/notes/26_09_2026/minimal_feedback_review.md:663) recommended matched isolated controls and warned against relabeling the existing monitoring-plus-reinstatement curve as monitoring alone.
That is assistant synthesis consistent with the actual comments, not a separate instruction from Jordan.

The [August conversation](/Users/jordangunn/.codex/sessions/2026/08/23/rollout-2026-08-23T18-25-02-01a02fa7-847b-7580-9cab-30b56dda18f2.jsonl) records Jordan asking to see before/after plots before agreeing to matched reinstatement strength (line 18114), questioning whether parameter detail belonged in a caption (18430), rejecting an overloaded sentence (19097), and rejecting a monitoring caption without a coherent line of presentation (20125).
It also records his objection to unnecessary qualifications that make sentences complex by defending against unlikely misreadings (19955).
Accordingly, the revision shows the actual matched curves, keeps detailed parameter provenance in the figure package, and gives each caption a clear sequence: what is compared, which conditions are shared, and what the axes/panels mean.

The [recovered writing standards](/Users/jordangunn/workspace/eventcmr/notes/22_09_2026/introduction/writing_standards.md) support paragraph-level reasoning with local tracked edits, ordinary reader-facing language, and distinctions between simulated findings and proposed human mechanisms.
The present abstract and sensitivity-analysis decisions additionally require preserving the difference between increasing recall and protecting recall from the full reminder-specific interference pattern.

## Changes required

| Location | Decision and purpose |
|---|---|
| Figure 10 graphic | Adopt the three-panel candidate from the preserved control-decomposition results: reinstatement alone, maintained cue alone and monitoring alone, each against the same baseline, across all 64 positions with identical axes. |
| Figure 10 caption | Replace the first/any-recall panel descriptions with the three operations; identify the shared reminder/task condition, baseline, phase regions, outcome and fixed strengths. Preserve the distinction between absent deliberate controls and the weak film cues present in every setting. |
| Diagnostic lead-in, s333 | Refine Jordan's pending wording to promise encoded-position and post-non-film diagnostics. Remove the figure-specific promise to show where recall begins. |
| Paragraph after Figure 10 | Report the early-film and early-task increases under reinstatement, the film/task shift under the maintained cue, and the monitoring pattern. Remove the first-recall finding attributed to the replaced plot. Preserve the conditional early-position prediction, describing a recall benefit rather than claiming selective protection. |
| Monitoring transition | Keep Rik's contribution about retrieval order. Accept Rik’s linking insertion s272 and repair the missing noun in “maintained film-category” with a local tracked insertion under Jordan’s name, retaining Rik’s original wording and attribution. |
| Figure 11 graphic | Retain the return-to-film diagnostic as a single panel, exported from the saved transition probabilities. Remove the overlapping positional panel without calling it identical to Figure 10C: its control settings differ. |
| Figure 11 caption | Remove A/B labels and the obsolete positional/phase-band description. Identify the conditional probability, fixed reinstatement, absent maintained cue, and the monitoring-strength scale. |
| Review state | Resolve c355 and c366 after the matched comparison and companion update are in source. Resolve c345 because the last obsolete graphical label is removed. Keep the new manuscript suggestions pending; only Rik’s linking insertion s272 is accepted for the local noun correction. |
| Replies | Edit the existing replies under Jordan's name, retaining their identities and authorship. Update c354's description of the lead-in and c357's distinction between completed figure work and the still-open experimental-data question. |
| Other manuscript material | Preserve abstract, sensitivity results, section order, stable figure IDs, bibliography and all unrelated suggestions/comments. Conceptual claims that reinstatement changes retrieval initiation remain valid; only claims that the new Figure 10 displays first recall are removed. |

## Data and interpretation checks

Figure 10 uses the preserved 256 rows in [the figure package](/Users/jordangunn/workspace/selective_interference_v2/work/retrieval_control_position_comparison/README.md), selected from one saved decomposition run.
Its four conditions each contain 64 positions and match on reminder, task association strength and weak-cue settings.
The mean probabilities sum to the independently saved phase totals.
No simulations are rerun and no parameters are selected to improve the apparent contrast.

The maintained-cue and monitoring curves are not flat.
Reinstatement increases recall of early task items as well as early film items.
Monitoring reduces recall of most task positions while increasing recall at the earliest task positions.
These statements must be checked against the saved values rather than inferred from mechanism names.
The fixed high-interference comparison does not itself establish a selective-protection interaction; the earlier aggregate and sensitivity analyses continue to support that claim.

Figure 11 uses five saved transition probabilities with reinstatement present.
The plotted probabilities are checked against `film_return_count / transition_count`.
It remains a conditional output-order diagnostic, not an isolated monitoring-versus-no-control comparison equivalent to Figure 10C.
The original embedded PNG is retained for rejection/history; the new single-panel plot is redrawn from the saved data rather than described as a pixel-identical crop.

## Tracking and reply boundaries

Each graphic is a pending image replacement under Jordan's name, preserving the old asset.
Caption and prose changes use local pending replacements/insertions/deletions; already-pending Jordan wording is refined in place where appropriate.
Original comment bodies, reply IDs, suggestion identities and stable figure identities are preserved.
Rik’s linking insertion s272 is accepted before adding the missing noun “support” as Jordan’s pending s430.
This preserves Rik’s wording and attribution while allowing the local correction; all other pre-existing suggestion decisions are unchanged.
The comment on the removed Figure 11B caption stays attached to the tracked deletion, so its original context remains available.
No change is made to the frozen comparison reference.

c357 remains open: the current notes discuss a broader search for suitable datasets, but they do not establish whether the collaborators' own experiments retain the item identities and ordered outputs required for this comparison.
Completing the figure does not answer that question.
c349 and c383 require no new resolution or substantive rewrite; their completed sensitivity/contribution work remains intact.

The old terminology audit and its pending tasks are historical proposals.
This document and the current source supersede its outstanding Figure 10 item.
No manuscript HTML or Word output is refreshed as part of this integration.

## Completion and verification

The manuscript contains pending suggestions s417–s435 for the two graphics, captions, positional interpretation and small linking-clause correction.
Jordan’s existing pending s333 and s399 were refined in place to match the selected diagnostic.
The existing replies to c345, c354, c355, c357 and c366 were updated without changing their IDs, authors, original dates or original reviewer text.
c345, c355 and c366 are resolved; c354 remains resolved; c357 remains open for the experimental-data check.

Source parsing and decision validation pass.
Comparison against the frozen reference adds exactly the same one pre-existing ordinary edit as before; the integration introduces no new unmarked wording changes.
All original comment boundaries survive, including c366 on the removed panel description.
The frozen reference, presentation configuration and rendered HTML/Word files are unchanged.
The source and data checks are recorded in `verification.json` in the figure package.
No manuscript HTML or Word rendering, browser inspection, simulation rerun or commit was performed.

## Requested render refresh

After the source integration, Jordan requested regular HTML and APA Word exports.
`docs/index-regular.html` and `docs/index.docx` were rebuilt from the unchanged working manuscript.
The HTML front-matter regression check passed; no browser inspection was performed.
Word checks verified s417–s435, the updated replies, c345/c354/c355/c366 resolved and c357 open.
The updated figure pages were also inspected in the Word layout render.

The Word render exposed a pre-existing APAQuarto caption bug: `apacaption.lua` replaced Quarto’s assigned number with an empty string when APA-specific number attributes were absent.
The project’s vendored filter now retains Quarto’s number in that case and resets its optional override for each float.
A synthetic Word check covered normal numbers, an appendix override and a following normal figure; the rebuilt manuscript has labels Figure 1 through Figure 11.
The source manuscript, frozen reference and project configuration were not changed by this refresh.
