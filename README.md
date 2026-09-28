# Working manuscript review

This project starts from the untouched Henson/Holmes pooled Word document:
`notes/22_08_2026/selective_interference_rik_emily_combined_review.docx`.
Talmi's separate feedback and later manuscript edits have not been added.

The project root is the single active manuscript project. The review draft was
moved here from `manuscript-review/`; that parallel project has been removed.
The earlier root draft, settings, bibliography snapshot, and generated files are
preserved in `archive/2026-09-27-before-root-consolidation/previous-root/`.
Research code and analysis results retain their existing locations. Earlier Word
workflows and draft fragments are catalogued in `archive/README.md`.

The imported draft retains 47 comment threads and 4 replies (51 comment records),
and 285 existing tracked-change records. They include comments and changes already
attributed to Jordan in the source. Their identities and individual decisions are retained.
There were no new prose edits in the migration baseline. The working draft now
includes the three cumulative title-review steps requested on 27 September:
Emily's five title insertions rejected, our agreed title suggested at both title
occurrences, and a reply added to Emily's title comment with the thread resolved.
The new title replacements remain pending and are attributed to `Gunn, Jordan`.
The five agreed authors and four affiliations are present as pending additions.
The draft-only author note is a pending deletion, and the short title is updated in the render settings.
The approved abstract is proposed through local, attributed changes against the pooled-review wording.
The original abstract comments remain active; the redundant “involuntary” and “(intrusions)” insertions are rejected.
The body remains at the pooled-review baseline.

The three corrected APAQuarto Word checkpoints and their source states are preserved in
`review/stages/2026-09-27-title/apaquarto/`. Its `manifest.json` records hashes, export
identities, and preservation checks. The existing `docs/index.docx` matches the
third title checkpoint and predates the later author-page changes.
Word export is deferred while we work in QMD and HTML.
The HTML navigation hides its Word link during this round.
The earlier generic Word exports remain in the parent folder as superseded archives.
`migration.json` remains the record of the original unedited migration.

## Files we work in

- `index.qmd`: manuscript, suggestions, anchored discussions, replies, attribution, decisions and Word provenance in the single-source review format.
- `reference.qmd`: the converted frozen source for the current round; leave it unchanged while editing.
- `references.bib`: the existing project bibliography. The imported draft still
  contains literal citations and reference entries; moving it does not convert
  or rewrite them. Bibliography conversion is a separate manuscript change.
- `assets/media/`: original embedded figures.
- `_quarto.yml`: rendering settings.
- `presentation/`: the project-specific Lua/CSS adaptations referenced by those settings.
- `work/README.md` and `work/figure-map.yml`: analysis navigation and figure provenance.
- `notes/README.md`: feedback, meeting records, proposals, and retained literature.
- `archive/README.md`: historical drafts, retired workflows, and recovery records.
- `review/reference/`: retained legacy reference archive; the active comparison source is now root `reference.qmd`.
- `review/exchanges/`: exact archived original Word document.
- `review/rounds/`: earlier import snapshots, retained while finalizing the migration.
- `review/stages/`: named cumulative exports and source checkpoints for review.
- `migration.json`: source checksum and verification results.
- `docs/`: generated HTML and Word files; edit the source files above instead.

The reusable review software is in `../quarto-review/`. This repository contains
the manuscript and its research materials. The review engine is maintained in
the separate sibling repository.

## Reading and editing

The HTML offers **Redline**, **Proposed**, and **Original** views. These change
what is displayed without accepting or rejecting suggestions. The author and
status filters narrow the comments shown. Threads and replies appear automatically
in the free margin beside the passage on screen. Hover over a marked passage
to bring its particular comment into view without moving the manuscript. On
narrow screens, comments appear immediately after their passage. The full review
index is also available at the end, but is not needed for ordinary reading. Replies and decisions are stored in index.qmd, not by editing the rendered HTML.

The review toolbar stays at the top as you scroll. **Hide controls** removes the
toolbar; **Hide comments** removes comment cards, links, and underlines. You can
hide them independently. **Reading view** hides both and shows clean proposed
text with no change markings or filter dimming. The small **Show review** button
restores the previous view and filters. These are display controls only: they do
not change the source, accept suggestions, or resolve comments.

We can discuss and make edits here in chat. Ordinary wording edits are compared
against the frozen reference and exported as tracked changes; explicit suggested
wording uses CriticMarkup. Do not recapture the reference during routine editing.

In manuscript prose, keep one sentence per source line so revisions are easy to review.
Use ordinary soft line breaks, with no trailing spaces that would force line breaks in rendered HTML or Word.
Keep review markup, equations, tables, citations, and bibliography entries intact when reflowing text.

The working `_quarto.yml` uses `project.type: manuscript`, matching the original
project and the other manuscript projects in the workspace. It offers both
`apaquarto-html`, using this project's copy of APAQuarto, and regular manuscript
`html`, using the original project's Darkly theme and Quarto's native manuscript
title block, author/affiliation layout, abstract, and navigation.
APA HTML remains the default. Change either format or theme there to change its presentation;
the review controls and comments adapt to it. Quarto's usual document and
directory metadata overrides still apply. HTML, Word, and PDF formats are chosen
separately.

The imported title page stays in the QMD source body so its original review
anchors remain active. For regular HTML, `presentation/manuscript-frontmatter.lua` moves
the annotated title, author line, and affiliations into the title block while
leaving `# Abstract` as the first article section, following the homophily manuscript.
The clean Reading view uses Quarto's five structured author records from YAML;
review views show the annotated Word author line without forcing it into Quarto's
two-column author grid. Annotated keywords use the
native keyword presentation beside the abstract. An unannotated repeated Word
title is omitted; when it has a tracked edit, it remains available in review mode
and is hidden in Reading view by `presentation/manuscript-import.css`.
The former author note appears as a deletion in Redline and Original views and is hidden in Proposed and Reading views.
This bridge is specific to the imported title-page structure; update it if that structure changes.
After rendering regular HTML, run `python3 -m unittest discover -s tests -p test_review_frontmatter.py`
to check that review deletion markers do not span native author metadata or the abstract
and that the abstract appears below the title block. The `abstract-section`
extension from the local homophily project is enabled only for APA PDF, where it
converts the body section to metadata for that format.
The reusable review interface supports title blocks outside the article body and ignores the copies of review markers in Quarto's contents list.

APAQuarto requires title and author metadata as well, so its HTML format repeats
the original source values in YAML and suppresses its generated title page.
Its `title-block-style: default` preserves APAQuarto's own presentation within
the manuscript project. None of these settings changes the source author list.
`presentation/apa-import.css`, loaded only for this APA HTML format, applies the APA author,
abstract, and reference alignment to the imported body structure and lets figures
shrink on narrow screens. `presentation/apa-import.lua` retains the imported References heading,
which APAQuarto would otherwise remove because these references are plain text
rather than generated bibliography entries. The HTML-only `presentation/manuscript-outline.lua` keeps title-page headings out of the TOC
and corrects the source Word heading-style mix-up in the testing-proposals section.
Its existing bold label becomes the heading; the following paragraph becomes body
text. These display corrections preserve the pooled source and all review anchors.
Word export uses `apaquarto-docx` and the installed APAQuarto reference document.
`presentation/apa-import-docx.lua` maps the imported author, affiliation, optional author note, abstract,
and references to that template's own styles. It places the abstract on a new
page, its keywords after the abstract, and the second annotated title before the
introduction on the next page. Both title occurrences retain their independent
review anchors. The short title now reflects the agreed title, ready for the next deliberate Word export.
The frozen reference keeps the original migration settings, allowing presentation changes to be distinguished from prose.

To reopen the live preview from this folder:

```sh
quarto preview --to apaquarto-html --no-clean --no-browser --host 127.0.0.1 --port 4317
```

Then open `http://127.0.0.1:4317/index.html` for APA HTML or
`http://127.0.0.1:4317/index-regular.html` for regular HTML.

During this review round, render HTML without cleaning away the other view:

```sh
quarto render --to apaquarto-html --no-clean
quarto render --to html --no-clean
```

They write `docs/index.html` and `docs/index-regular.html`, respectively.
Both include the review interface and the configured presentation filters.
The preview displays these generated files; no browser-only styling changes are needed to reproduce them.
Use `--no-clean` to retain the other HTML view and the older Word export.
Render APA Word deliberately when that review stage resumes.

`execute.keep-md: true` retains generated intermediates used by the two HTML
formats. The retained `index_files/` and `*.html.md` files are ignored by Git and
are not authoring files. Manuscript projects place shared HTML assets in
`docs/site_libs/`.

## Migration checks

The original Word file is archived byte for byte. Comment text, authors, dates,
thread relationships, identifiers, and anchors are checked against the Word
round-trip export, along with every tracked-change record's content and identity.
Word may split one revision into multiple XML elements during export.

Three existing equation bookmarks were restored during conversion. No equation
or prose was rewritten. One internal link was already broken in the original
Word file (`X510f1211e07a3ef8f4aa5eaadde4214adc1a9dc`) and remains unresolved.
Quarto uses nonbreaking spaces after `e.g.` and `i.e.` in two tracked passages;
their source wording is unchanged.

This is a review-preserving migration, not a reproduction of Word's page layout.
Bibliography entries remain the text imported from Word, rather than being
silently replaced by citations from the newer manuscript.

## Preservation and generated outputs

Current source and review history are covered by local Git recovery checkpoints
recorded in `archive/2026-09-27-cleanup/README.md`. The active branch and staged
research contents were preserved. These local recovery refs are not a remote
backup or a normal publication commit.

The existing Git policy for `docs/` is retained: it contains generated publication
and preview snapshots. Authoring takes place in QMD/YAML and the source assets.
Local runtime configuration, caches, owner files, and intermediate files are
ignored. Do not manually edit a generated output as the source of a revision.

Commit generated publication snapshots deliberately, separately from manuscript and research changes.
Ordinary rendering can change these tracked outputs; browser diagnostics and TeX intermediates are ignored.
Automatically retained Word exports in `review/exchanges/exports/` stay local by default.
The complete export records for the named title checkpoints and retained current Word file are tracked explicitly.
Before sharing a new Word export, add its complete export directory with `git add -f review/exchanges/exports/<export-id>/` so a returned document can be reconciled from another checkout.
Ignoring routine exports does not delete their local files.

Use ISO dates for new dated records. Original collaborator filenames, immutable
review snapshots, and established scientific package paths remain stable.

## Review format 0.2 migration

The active review uses single-source schema 2 and a fixed, non-editable version 0.2.0 runtime.
Current review state is in index.qmd; reference.qmd preserves the prior frozen comparison rather than starting a new round.
The temporary pre-upgrade backup, including the old root review.yml, has been removed.
The current source and review format are recorded in Git.
The legacy review/reference directory remains a historical archive.

To run commands with the project's pinned runtime from this directory:

~~~sh
source _environment.local
"$QUARTO_REVIEW_COMMAND" feedback
~~~

The development checkout is separate from this runtime; future extension edits do not change the manuscript installation.
