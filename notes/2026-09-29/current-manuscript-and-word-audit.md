# Current manuscript and Word review audit

Status: assessment after the requested regular HTML and APA Word renders on 29 September 2026.
This is a review of the current proposed reading and exported review records, not an instruction to accept pending suggestions.
No manuscript wording, review decisions, comparison reference, runtime or presentation settings were changed for this audit.
The source was stable throughout rendering and checking.

## Assessment

The scientific revision is substantially complete as a response to the agreed feedback.
The recent side-thread work resolves the main substantive defects identified in the [previous holistic audit](holistic-feedback-audit.md).
The remaining work is a bounded source/presentation and review-export pass, rather than another round of general rewriting or new simulations.
I would not yet describe the generated Word document as a finished collaborator-facing review copy.
Its prose and review records are preserved, but there is avoidable tracking noise and several visible layout problems.

“Resolved” records Jordan's response to a comment; it does not mean the collaborator has approved the response or that Jordan's wording suggestions have been accepted.
That distinction is maintained in the current export.

## What the side-thread work has fixed

| Previous finding | Current outcome |
| --- | --- |
| Retrieval equations omitted separate temporal and source updating | Equations 12–13 and adjacent prose now distinguish the two components and explain that monitoring scales both rates. Source retrieval drift is identified as fixed at 1. This agrees with `cmr.py` and the saved fitting configuration. |
| Context-to-feature equations introduced an unspecified λ | Equations 6 and 8 no longer contain λ; the prose specifies the primacy increment and decay. This corrects the description without changing the simulations. |
| Duplicate parameter tables | There is now one numerical/role table in Methodology. The table note distinguishes fitted, fixed and simulation-specific values. c386 records the accepted consolidation; additions remain pending. |
| Unqualified contrast implying reinstatement and monitoring cannot reduce interference | The two relevant specification sentences have been narrowed, and c349's reply records the alignment. The full reminder-specific sensitivity result remains intact. |
| Five citation anchors attached to the wrong reference entries, plus two Kessler destinations | Corrected in the latest source. This does not require rebuilding the bibliography system. |
| Figure 6 agreement error | “Reduce … and increase” now agrees. |
| Instruction/context wording could imply that instruction encoding was simulated | s474 now says that the simulations represent the instruction's effect by shifting context. The positive instruction-association account and c126's reply are preserved. |
| Abstract had redundant account framing | The latest version removes the duplicate contribution sentence and retains the shared-system contribution at the end. This does not remove the goal → cue → selective support explanation. |

The table and specification additions have their own resolved explanatory comments, c386 and c387.
They explain why the corrections were made and that the implementation and results have not changed.
This is an appropriate way to document accuracy corrections that do not correspond one-to-one to a Rik/Emily comment.

## Feedback coverage and scope

The [previous audit's Henson/Holmes and Deborah coverage tables](holistic-feedback-audit.md) remain the detailed passage map, subject to the updates above and the qualification about DT-484 below.
I rechecked the current replies against the proposed reading, including the newer c386/c387 records.
There are now 49 root discussion threads: 36 attributed to Rik, 10 to Emily and 3 to Jordan.
All 49 are resolved.
There are 48 replies, including preserved historical replies as well as the newer responses.

The main larger revisions still have identifiable reasons:

| Revision | Feedback or explicit decision supporting its scope |
| --- | --- |
| Revised abstract and goal-to-cue account | c21/c22/c24/c32, c70/c92, and Jordan's explicit decision to prioritize a coherent abstract over cosmetic minimality. |
| Brief recognition simulation before recall control, with the two-panel figure | c92/c102/c110–c112/c129/c368/c374 and the subsequent retain-and-shorten decision. This is a reasoned response to the removal suggestion, rather than a claim that Rik asked for exactly this implementation. |
| Sensitivity analysis and matched control diagnostics | c349/c354/c355/c357/c366/c383. The scope stays with the full reminder-specific contrast and identifiable consequences of the control mechanisms. |
| Repeated versus unique scoring | The meeting question, explicitly documented in c385. The text limits the analysis to repeats within a retrieval sequence rather than diary recurrence across episodes. |
| Task imagery, hotspot evidence and the format/content distinction | c119/c162/c381 and Emily's supplied references. The proposed psychological explanation remains distinct from the model's implemented representations. |
| Neutral-material prediction | c117/c368 and meeting discussion. It remains a prediction, not a newly claimed simulation result. |
| Balanced laboratory and clinical interpretation | c375/c377–c379. The text distinguishes intrusion reduction, selective interference and identification of a mechanism. |
| Consolidated parameter table and corrected equations | Deborah's DT-482 plus checking whether the specification faithfully describes the reported simulations; c386/c387 document this. |

There is no reason from this audit to add a new simulation section, undertake an emotional-versus-neutral analysis, analyse existing experimental data, or reopen the accepted section order.
The theoretical instruction-to-context explanation is not a stub needing expansion merely because its paragraphs are short.
Likewise, the absence of step-by-step cue construction in the simulation does not make the psychological account circular.

A rough count from Abstract through Discussion, including captions, table content, equation notation and source labels but excluding the reference list, is about 9% larger than the current comparison reference.
The Discussion is about 27% larger.
These are scope indicators, not journal word counts or measures of gross wording turnover.
They support describing this as a substantial feedback-led revision, not a light copyedit.
They do not identify an unsupported addition that should now be removed.
The next pass should remain limited to the concrete issues below.

## Remaining manuscript-level points

1. **One explicit terminology request remains:** “reminder-linked interference” is still in s333's new diagnostic lead-in at [index.qmd](../../index.qmd:765).
   Deborah asked to eliminate that expression (DT-252/DT-454).
   A local replacement describing interference after a film reminder would finish this point; it does not require changing the analysis or paragraph argument.
2. **The formal control presentation still puts monitoring before maintained cueing**, while the theoretical account and summary use the sequence in which the operations act.
   This is a small ordering inconsistency relevant to DT-379, not an unresolved mechanistic claim.
   If harmonized, use the accepted-move convention and preserve pending wording inside the moved material.
3. **Correcting the earlier audit's interpretation of DT-484:** Deborah wrote, “I recommend adding citations from here to make this paper less inward looking,” followed by the Visser et al. review DOI.
   That requests using the review as a source of broader literature; it does not explicitly require citing the review itself.
   Its absence from the body should therefore not be counted as a definite unfinished citation obligation.
   The current manuscript already includes the broader-memory material discussed under DT-483.
4. **Status documentation remains stale:** the root README still says the body is at the pooled baseline, the author note is a pending deletion and Word export is deferred.
   The positional-figure README and notes index still imply an outstanding experimental-data task, despite the recorded decision not to add those analyses.
   These records should be brought up to date without treating them as new scientific obligations.

The old c71 reply still uses future tense, but it is preserved history followed by a later completed response.
I would not erase original discussion history merely to remove that wording.
The latest substantive replies describe the decisions that are actually implemented.

## Word review fidelity: what passed

The generated file is [docs/index.docx](../../docs/index.docx), produced with the project's `apaquarto-docx` format and pinned review exporter.
The regular HTML output is [docs/index-regular.html](../../docs/index-regular.html).
APA HTML was not refreshed in this turn.

- All **49 threads and 48 replies** are present in native Word comment parts.
- All 49 root threads and all 48 replies carry resolved state.
- Comment/reply text, authors, dates, parent relationships and preserved original identities match the prepared source records.
- Original comment identities remain available; the deleted c17 thread has not reappeared.
- All **641 native revision elements** are attributed to **Gunn, Jordan**.
- They map to **387 pending suggestions**: 385 explicit source records plus two automatic whitespace comparisons.
- No accepted or rejected suggestion is exported as a pending revision.
  In particular, none of Rik's or Emily's decided edits is resurrected as a pending change.
- The native package has no missing relationships, duplicate revision identities, unclosed comment ranges or leftover conversion markers.
- An independent Pandoc read of Word's proposed text was compared with the source projection.
  The differences were front-matter/caption placement, generated figure labels and equivalent equation serialization, rather than missing or changed manuscript prose.
- Native equations survive as Word math objects.
- The accepted section and figure relocations are not exported as wholesale moved-section deletions and insertions.
  The largest individual text insertion is 702 characters, the sensitivity-results addition; the largest text deletion is 474 characters.
  This is consistent with the intended local wording review rather than a manuscript-length redline.

The absence of duplicate IDs or missing anchors is not the same as every comment retaining a highlighted phrase.
c24 has a zero-length range because its original “intrusions” insertion was rejected.
Eight root comments (c1, c24, c32, c70, c86, c115, c123 and c366) have no surviving highlighted text in the proposed view; their ranges are points or refer to pending deletions.
The records and their positions are retained, so this is not comment loss.
For easier review, c24 could be attached to the surviving definition, while comments deliberately answering a deletion can remain attached to the deleted wording.
This should be a targeted anchor decision, not wholesale reassignment of historical comments.

## Word review readability: what still needs work

### Unnecessary image replacements

**Figures 5 and 6 are each tracked as a deleted picture followed by an inserted copy of the identical picture.**
The before/after image bytes are identical.
The source suggestions s415/s416 change only the `alt` wording, while the exported drawing description fields are empty.
Thus the collaborator sees a large graphical replacement without an actual visual change.
This is visible for Figure 5 in the markup rendering around pages 45–47.
Accepting just these image-description updates, or teaching the exporter to separate descriptive metadata from image replacement, would remove the false visual comparison while preserving the pending caption wording.
No such decisions were made during this audit.

The other nine main-figure replacements do change image content and should not be automatically accepted as though they were the same problem.
They are legitimately large review objects.

### Empty and inherited revision records

There are **176 revision elements with no non-whitespace text**.
Of these, 147 are inside native mathematical control properties, 24 are paragraph-mark revisions, and five are other empty/whitespace records.
That total must not be described as 176 meaningless changes: paragraph marks can represent real paragraph edits, and math objects require inspecting the object as well as its text.
Nevertheless, the 147 older math-control insertions, the empty imported conflict s13, and the two automatic whitespace suggestions are candidates for a narrowly scoped tracking cleanup.
The corresponding identities remain in the frozen original, and any decisions should preserve actual equation changes, especially the newly corrected Equations 6, 8, 12 and 13.
Do not bulk-accept all of Jordan's changes.

### Heading and bibliography styles

The entire dual-list experimental-design paragraph is exported as **Heading 2** at [index.qmd](../../index.qmd:903).
Its actual section label, “Testing Competitor Learning and Retrieval Selectivity,” is exported as ordinary body text with bold formatting.
This produces a full bold paragraph in Word (markup page 76), and gives the wrong document outline.
The existing HTML-only adapter does not repair Word, and its recognition of the paragraph depends on the older wording.
Repair the semantic source heading/body distinction or apply a robust format-wide adapter, preserving the paragraph's pending wording change.
No new prose is needed.

Of 91 reference-entry paragraphs, 72 receive Word's Bibliography style and 19 receive BodyText.
The current Word adapter assigns bibliography styling only to paragraphs containing an explicit reference anchor.
Unanchored entries consequently retain different indentation and spacing.
This also means moving a reference anchor to its correct destination can inadvertently change which entry receives the bibliography style.
Apply reference styling by membership in the References section, not by whether an entry happens to carry a hyperlink target.
This is a presentation correction, not a bibliography rewrite.

### Table and figure layout

The consolidated parameter table has an oversized symbol column and a cramped description column.
Its title and full explanatory note are treated as one italic caption before the table.
The table occupies multiple pages; the proposed-only diagnostic places the final control row on a third table page.
The reference to Table 1 and its label also separate from the main table caption in the current pagination.
Column widths, title/note treatment and grouping deserve a focused APA Word layout fix.

Large figure captions and images frequently fall on separate pages.
Some of this follows from actual image size and the additional deleted/inserted pictures in a redline, but it is not solved merely by having the caption in a proper source figure block.
The Word render needs its own layout treatment.
Do not address it by cutting justified scientific explanation or shrinking the whole document's font.

### Tracking future collaborator edits

The Word file contains native revisions but does **not** contain `w:trackRevisions` in its settings.
The export therefore does not itself request that subsequent edits be tracked automatically.
An individual Word session may have its own setting, so this is not a claim about what a particular user's Word window currently shows.
For a review file intended to circulate, enabling tracking in the export would make the intended workflow explicit.
This is separate from preserving the already-exported revisions, which passed the checks above.

## Render evidence and limits

Both requested Quarto renders completed without reported warnings or errors.
The bundled LibreOffice renderer produced all 94 pages of the tracked Word document as PDF/PNGs.
A temporary diagnostic copy with pending changes accepted in memory produced 79 pages, isolating final-layout problems from redline expansion.
That temporary copy was not installed in the manuscript project or offered as a second editable manuscript.
The delivered DOCX still contains every intended pending revision.

Review-record and proposed-text checks cover the whole document.
Visual inspection focused on the title, abstract, revised equations, table, selected changed figures, and the malformed Discussion heading.
This establishes the specific problems above; it is not a full visual sign-off of all 94 pages, and it does not verify the appearance of Word's own comment-pane interface.
The HTML browser view was not inspected.

Audit source hashes:

- `index.qmd`: `929bc435fe01234fb972129c3fa34a983968c863caf5674140e9b5031e99487f`
- `reference.qmd`: `b32251add11b6f192862befe6253ace1a6ab25862f6032620edc4f8aac5d483f`
- `references.bib`: `f7e74fde0bbf286feecf563b40d9bbfc548cbd766a6fe8c1966c9962fe1322bd`
- `_quarto.yml`: `103a61fced4215d2067fd962b7a0212e424742c8ef054cd3782d6351f898e496`

## Recommended next pass

1. Finish the one outstanding “reminder-linked” wording correction and decide whether to harmonize the formal control order.
2. Correct the heading, reference styles, table/caption layout and future-tracking setting through the source/presentation/export system.
3. Remove the two identical-image replacements and review the inherited empty math/conflict records without accepting substantive wording changes.
4. Re-render and check the resulting collaborator-facing Word copy, including its proposed reading and retained comments.

This work finishes the response and its presentation.
It does not justify another broad scientific rewrite.

## Implementation update — 29 September 2026

The terminology, formal-description order and status-documentation points above have now been implemented.
The “reminder-linked interference” wording in s333 is now “interference after a film reminder”; s333 remains pending, and the existing reply to resolved c354 records Deborah’s terminology request.
Resolved c388 records the accepted order of start-of-film reinstatement, maintained cueing and monitoring, with cueing numbered Equation 13 and monitoring Equation 14.
Only that relocation and numbering are mirrored in `reference.qmd`; pending wording and mathematical corrections, including s529, retain their identities and decisions.

The native equation objects o60/o61 use a small, immutable [two-equation archive](../../review/exchanges/1474edfe1908bf5592f90f1ec512b1c5bbb7cdb9841a7e0cede90cb55956f8f4.docx) so future Word exports use the accepted numbers as well.
It contains the original native equations and review records with only the two number labels swapped.
Empty paragraph placeholders preserve the original XPath addresses; all revision identities, authors, timestamps, provenance and decisions are unchanged.
The original pooled Word archive is unchanged.
This is supporting data for native equation preservation, not a second editable manuscript or a regenerated manuscript Word output.

The root README, positional-figure README and notes index now reflect the current manuscript and the decision not to add existing-experiment analyses.
No manuscript citation was added for DT-484: the corrected interpretation above stands.
The Word-fidelity and layout findings in this audit describe the earlier export and have not been silently treated as fixed by these source edits.

Verification confirmed that the original and proposed text projections differ only by the accepted relocation and numbering, plus the intended s333 wording refinement in the proposed reading.
All existing suggestion metadata and decisions were preserved, and comparison against the reference still produces only the same two automatic whitespace suggestions.
The native Word object exporter produces the new equation numbers while retaining the 18 pending native revisions across these two equations.
Regular HTML was refreshed and the front-matter regression check passed.
The existing manuscript Word output was not regenerated; its checksum is unchanged.
