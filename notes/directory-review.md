# Directory organization and deprecation review

Reviewed 27 September 2026, after the review manuscript was promoted to the
project root. The organizational cleanup below was subsequently authorized and
implemented the same day. The original findings are retained as an audit record.

## Implementation status

- Historical status notes now point to the active project; the earlier broad
  manuscript comparisons point to its preserved archive.
- Recoverable Git checkpoints preserve the source and review history while the
  active branch and staged research contents remain unchanged.
- All six active presentation helpers are in `presentation/`, with updated
  Quarto paths and verified renders.
- Earlier Word workflows, the July drafts, prose fragments, the Word-phase
  working files, and the stale figure bundle are catalogued under `archive/`.
- Retained literature is in `notes/literature/`; reading figures are identified
  separately as `figure-extracts/`.
- Notes, archives, review checkpoints, and research packages have navigation
  indexes. `work/figure-map.yml` verifies all 12 images against the original Word
  media and distinguishes related code from proven reproduction.
- The exact duplicate web-trial file, superseded build/cache directories,
  disposable Python/Finder caches, and three confirmed stale Word owner files
  were removed. The retained Word copy and original trial provenance are linked.
- Existing review/reference/exchange records, manuscript and review YAML,
  bibliography, figures, model/test sources, and all 464 scientific-work files
  were verified unchanged. APA Word and both HTML styles were re-rendered.

The full action manifest, preservation checks, and recovery instructions are in
[the cleanup record](../archive/2026-09-27-cleanup/README.md).

Potential future engineering work—automatically deriving APA display metadata
and defining an exchange-retention policy—is separate from this directory cleanup.
Citation conversion and scientific package renaming also remain deliberate
manuscript/research tasks, rather than cleanup side effects.

## Current responsibilities

The active manuscript is root `index.qmd`, accompanied by `review.yml` and
`_quarto.yml`. `references.bib` remains the project bibliography. The imported
manuscript currently contains literal citations and reference entries; it does
not yet consume that bibliography. Current outputs belong in `docs/`.

The sibling `../quarto-review/` repository owns the reusable review software.
This repository owns its manuscript, project-specific presentation adaptations,
research code, analyses, and feedback history.

`review/reference/`, `review/rounds/`, `review/stages/`, and
`review/exchanges/` are preserved review records with distinct responsibilities.
Their repeated QMD/YAML files and Word documents are intentional snapshots.
The original collaborator files and meeting notes remain evidence for future
manuscript decisions.

## Findings, in priority order

### 1. Historical documents still describe themselves as current

- `notes/decision_ledger.md`, especially lines 16–20, labels its decisions
  “Locked Or Current” and specifies a different title while advising against
  “single system” in the headline. That title guidance predates the currently
  approved title.
- `notes/26_09_2026/minimal_feedback_review.md`, lines 3–13, still presents the
  earlier Word/cloud workflow and author-page changes as the current working
  state. Its line-31 “Current manuscript” link now points to the newly promoted
  pooled review draft, although the accompanying description concerns the
  broader-edited manuscript that was moved into the root-consolidation archive.
- `notes/26_09_2026/document_workflow_options.md` and `quarto_review_plan.md`
  preserve workflow research and implementation planning that precede the
  working local review system.

Recommended action: date and label superseded status/decision sections, retain
useful feedback and proposed passages, and make the root README the entry point
for current implementation status. Retarget historical links describing the
former root draft to
`archive/2026-09-27-before-root-consolidation/previous-root/index.qmd`.
Historical decisions remain valuable; they should not silently become current
instructions. The new abstract and other proposals must not be marked implemented
as part of an organizational cleanup.

### 2. Version-control coverage favors outputs over the new source history

`index.qmd`, `_quarto.yml`, and `references.bib` are tracked. At audit time,
`review.yml`, the new README, `migration.json`, and
`review/reference/manifest.json` are untracked. Git already tracks 47 files
under `docs/`, including outputs of the earlier manuscript.

Recommended action: record the complete new authoring configuration, review
state, required assets/extensions, and preserved history in an intentional
version-control or backup checkpoint. Keep local runtime paths and caches
ignored. Retain or stop tracking generated `docs/` according to the project's
publication policy; the audit did not establish that policy. Existing staged
research changes should be handled separately rather than swept into cleanup.

### 3. Project-specific presentation code is scattered across the root

The six files are `apa-import-docx.lua`, `apa-import.lua`, `apa-import.css`,
`manuscript-frontmatter.lua`, `manuscript-outline.lua`, and
`manuscript-import.css`. They are all in use.

Recommended action: group them under `presentation/` and update their paths in
`_quarto.yml`. Re-render all three formats and check review boundaries and native
Word records afterward. Keep reusable engine code in the sibling repository and
its installed integration under `_extensions/quarto-review/`.

There is also some remaining metadata duplication: APA format settings contain
title/author values also represented in the annotated manuscript. Deriving those
display values from one source would reduce drift. The two annotated title
occurrences themselves preserve separate original Word review locations and
should remain independently identifiable.

### 4. Earlier Word workflows and old drafts look like active project files

The following are suitable archival candidates:

| Current location | Reason | Suggested home |
| --- | --- | --- |
| Root `compare_index_docx.sh` | Earlier Word/AppleScript comparison workflow; current review export handles native changes directly. | `archive/legacy-word-workflow/` |
| Root `extract_composite_feedback_ordered.py` | Earlier standalone feedback extractor, with a June/July composite as its default input. | Same archive, retaining its extraction output and provenance. |
| Root `selective_interference_24_07_2026_jg.docx` and `selective_interference_clean_24_07_2026.docx` | July manuscript versions outside the current output and review archive locations. | `archive/legacy-drafts/` |
| `work/document_workflow_trial_20260927/` | Superseded conversion/redline prototype, about 8.9 MiB, mixed into scientific analyses. Its imported text remains evidence for the earlier draft. | `archive/legacy-word-workflow/` |
| `work/merge_favor_source_true_test.docx` | Earlier merge experiment mixed into scientific analyses. | Same workflow archive. |
| `notes/26_09_2026/word_web_trial/` | Superseded Word-for-web experiment. | Same workflow archive. |
| `notes/compare_index.docx` | Output of the earlier comparison workflow. | Same workflow archive. |
| `notes/slop.qmd` and `notes/slop2.md` | Older full/partial prose drafts with names that do not identify their role. | `archive/legacy-drafts/`, preserving their original names and documenting their contents. |
| `_extensions/pandoc-ext/abstract-section/` | Used by the former root APA PDF configuration; absent from the current active format/filter settings. | Archive with the old rendering setup if that setup is formally retired. |

Archive these as history, preserving their bytes and recording old-to-new paths.
Several historical artifacts contain absolute links, and the comparison script
derives its project root from its own location. Moving them requires either
updating navigation around them or documenting how to restore the old workflow;
it should not imply they can still run unchanged from the archive.

### 5. Useful literature is stored in the temporary directory

`tmp/pdfs/` contains about 24.1 MiB of research papers, extracted text, and figure
inspection images, including McConnell, Polyn, Talmi, Cohen/Kahana, and specialized
recall material. These are not all disposable render caches. No references to
`tmp/pdfs` were found in the searched active project text/code.

Recommended action: move retained papers and useful reading material to a named
literature location, such as `notes/literature/`; classify rendered inspection
images separately before deletion. Remove the empty `tmp/docs/` directory.

### 6. Research packages need a navigation and status map

`work/` contains model notebooks, scripts, result tables, figure exports,
exploratory variants, and workflow experiments. Its simulation numbers reflect
multiple stages of the paper's ordering: recognition appears in names beginning
both `simulation3_` and `simulation4_`, while prior manuscript plans place it
second. A filename's number therefore does not establish its current manuscript
role.

Recommended action: add a `work/README.md` mapping each analysis package to its
scientific question, status, manuscript figure, and authoritative generator.
Prefer stable mechanism names for future packages. Defer bulk renaming until
notebook/script dependencies have been mapped. Treat the sensitivity analysis
package's own README and feedback trace as useful existing examples.

Keep simulation sources, results, and variants until their scientific status is
established. The current draft cites imported Word images in `assets/media/`;
only one of the 12 imported images exactly matches a PNG under scientific
`work/` by hash. This does not prove the others depict different results, but it
does rule out assuming all imported images are interchangeable with current
exports. Add a figure-to-generator provenance map before replacing them.

### 7. The figure bundle is a separate, stale export path

`figure_package/selected_figures.docx` was last modified in July, while its QMD
was modified in August. Its QMD explicitly requests generic `docx`; the active
root review project registers only `index.qmd` as a manuscript source.

Recommended action: label the Word file as a historical export. Decide whether
the figure bundle remains a maintained deliverable. If it does, give it an
explicit build configuration and source/figure mapping; otherwise archive the
bundle together. The audit did not attempt to rebuild it.

### 8. Naming and historical checkpoint presentation are inconsistent

Date conventions include `22_08_2026`, `26_09_2026`, `2026-09-27-title`, and the
mixed `advisor_feedback_2026_07-03.docx`. Notes also mix source documents,
decision records, proposals, and full draft fragments in one listing.

Recommended action: use ISO dates for new dated records and add a short notes
index distinguishing source feedback, meeting records, current proposals, and
superseded decisions. Preserve received filenames and existing immutable review
records; avoid a broad rename solely for cosmetic consistency.

The title-stage directory exposes generic Word files above the corrected
`apaquarto/` subfolder. Its README already marks those generic files superseded.
Make the three correct APA checkpoints prominent in the archive catalog; any
physical reorganization must preserve manifests and their path relationships.

## Removal candidates and retention limits

- **Exact duplicate confirmed:**
  `notes/26_09_2026/word_web_trial/selective_interference_word_web_trial.docx`
  and `notes/26_09_2026/selective_interference_minimal_revision_working.docx`
  are byte-identical, SHA-256
  `c7577b101d8c1213aac88dd68fbca1725cc321e07f7e7f37252a2bc72545b83c`.
  Keep one canonical historical copy and a clear trial provenance record before
  removing the duplicate.
- **Superseded generated directories:**
  `archive/2026-09-27-before-root-consolidation/previous-root-cache/` and
  `previous-review-build/` total about 14.2 MiB. The latter contains generated
  outputs, intermediate files, and redundant installed presentation assets.
  Its `_output/index.docx` has an exact retained counterpart at
  `review/exchanges/exports/1449c4f3584e6dc7fa1fe5feff24db27851fe2cbf8dd1d51823bd6f92fb205fd/document.docx`.
  These directories can be removed after the already-recorded root relocation
  checks; retain `previous-root/`, its old manuscript/output history, and
  `relocation.json`.
- **Disposable caches:** Python `__pycache__/`, `.pytest_cache/`, and `.DS_Store`
  can be regenerated. Removing them saves little and does not fix the main
  organizational problems.
- **Word owner files:** three `~$...docx` files exist at the root and under notes.
  Their open-file status was not checked. Remove only confirmed stale owner
  files after the corresponding Word documents are closed.
- **Active render support:** retain `.quarto/`, `site_libs/`, `index.html.md`,
  `index.docx.md`, and current output assets while using the preview. The project
  deliberately retains intermediates for its multiple HTML formats.
- **Review history:** do not prune hashed exchange directories or frozen
  references based on names or age. Repeated exports can differ only in core
  metadata/export identity, but those identities can be needed to recognize a
  returned Word document. Growth here needs an explicit retention policy in the
  reusable review software.

## Suggested implementation order

1. Record a complete source/history checkpoint and clarify which status notes are
   historical. Correct historical links affected by the root move.
2. Archive obsolete Word workflows and old draft fragments; add an archive index.
3. Group presentation helpers, relocate literature out of `tmp`, and create the
   research/figure navigation map.
4. Remove verified duplicate files, superseded caches, and confirmed stale owner
   files. Leave scientific results and preserved review exchanges intact.
5. Re-render both HTML formats and APA Word, check review identities and frozen
   reference hashes, and verify the live download after any path changes.
