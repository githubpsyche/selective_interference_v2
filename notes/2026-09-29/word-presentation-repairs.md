# Word presentation repairs

This side conversation implemented the presentation repairs identified in [the manuscript and Word audit](current-manuscript-and-word-audit.md).
The user approved the repairs, the reusable tracking option in `quarto-review`, and regeneration and layout checks of Word and both HTML outputs.
Concurrent manuscript and review decisions from the main conversation were preserved.

## Scope and files

- `index.qmd` and `reference.qmd`: made “Testing Competitor Learning and Retrieval Selectivity” a real second-level heading, restored the dual-list paragraph to body text, and separated the parameter table's explanation into a `.table-note` block with a conventional “Note.” label.
  The same structural repairs in the comparison reference avoid large structural redlines; existing pending wording remains intact.
- `presentation/manuscript-outline.lua`: removed the obsolete HTML-only repair based on matching the old paragraph wording.
- `presentation/apa-import-docx.lua`: assigns Bibliography style by membership in References, ending before Supplementary Material, and styles the table label and note separately.
- `presentation/finish-docx.py`: adds Word-specific table widths, padding, caption grouping and image pagination after native review export.
  Captions, table cells and the table note use single spacing at the existing type size; body spacing is unchanged.
  Before/after images occupy separate lines with widow/orphan control disabled, allowing the first image to stay with its caption while the replacement continues on the next page.
- `_quarto.yml`: runs that presentation hook after the review hook and enables `quarto-review.word.track-changes: true`.
- `presentation/README.md` and `tests/test_review_word_presentation.py`: document and check these rules and review preservation.

The reusable option was added in `/Users/jordangunn/workspace/quarto-review` in `quarto_review/extension/finish.py`, new `quarto_review/extension/word_options.py`, new `tests/test_word_options.py`, and `README.md`.
The two integration files were copied into the manuscript's `_extensions/quarto-review` directory.
The Python runtime pin and `_environment.local` were not changed.
The option enables tracking of subsequent Word edits; it does not accept suggestions or resolve comments.
No additional scientific wording, review decisions or reviewer comments were introduced by these presentation repairs.

## Verification

Both HTML formats and APA Word were regenerated from the current source.
Use `--no-clean` when rendering a single format to preserve the other generated formats in `docs/`.
HTML was checked structurally, without browser inspection.

Four manuscript presentation checks and six reusable tracking-option tests passed.
All 91 reference entries have Bibliography style, the dual-list paragraph is body text, and the correct section label has Heading 2 style.
The parameter table has a wider description column, repeating headers and a separate note.
The Word settings enable tracking of subsequent edits.

The export retains 50 root comment threads, 48 replies and 235 pending source suggestions, represented by 486 native revision elements.
The native review checks matched comment text, attribution, dates, relationships and resolved states to the current prepared source records.
These counts include concurrent review cleanup from the main conversation; that cleanup was not part of this presentation pass.
The layout hook preserves text, review identities and all package parts other than document/style layout, and applying it twice produces no further changes.
The final export's recorded source and output hashes match the current files.

The bundled Word renderer produced an 82-page document with markup visible.
Targeted visual checks covered the table, revised heading/body distinction, reference formatting and figure-caption pagination.
In that render, Table 1 occupies pages 37–38, Figures 7 and 10 begin with their captions on pages 46 and 53, and the repaired heading/body distinction appears on pages 63–64.
The replacement pictures continue on the following pages when necessary; both versions remain available for review.
The final generated Word package matches the visually checked layout candidate in every part except its creation metadata.
This verifies the targeted repairs, not every page or Microsoft Word's own comment-pane appearance.

Verified source SHA-256: `dbcf83890115c07c06f47a33f782b88bc00ca0a8ba5622462e6a4a629f743c6e`.
Verified Word SHA-256: `a3e06366e29c32cf2d8b8e2dd6ff037f63e03177c1e99f37e7cbac2b861ee377`.

No files were committed or pushed in this side conversation.
