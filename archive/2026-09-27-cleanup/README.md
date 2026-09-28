# Organization cleanup — 27 September 2026

The user authorized the directory audit's cleanup recommendations. The active
manuscript remains root `index.qmd`, `review.yml`, `_quarto.yml`, and
`references.bib`. The [project README](../../README.md) is the current entry point.

## Recovery checkpoints

Local Git recovery refs retain complete working-source/history snapshots:

- Before cleanup: `refs/checkpoints/organization-2026-09-27-before`
  (`4b53f78eec649e537c177d69796ccc36a21b1c11`).
- After cleanup: `refs/checkpoints/organization-2026-09-27-after`.

They preserve untracked manuscript/review materials as well as working research
files. The before checkpoint also includes the retained literature that was
previously ignored under `tmp/pdfs/`. The active branch and the contents of the
normal Git staging area remain unchanged. These local recovery refs are not a
remote backup or publication commit.

For example, inspect the prior configuration without modifying the working tree:

```sh
git show refs/checkpoints/organization-2026-09-27-before:_quarto.yml
```

Restore selected files deliberately from the appropriate checkpoint; do not
reset the whole working tree over unrelated research edits. The checkpoint commit
message also records the original staged tree.

## Actions and preservation

`manifest.json` records each move, original checksums, each removal and reason,
canonical copies retained for duplicate files, and verification results.
It also preserves the pre-cleanup hashes of the manuscript, review history,
figures, model code, and tests.

- 23 relocation operations grouped presentation helpers, archived older drafts
  and document workflows, archived the stale figure bundle, and preserved the
  literature in a permanent location.
- One byte-identical web-trial Word duplicate was removed. Its original
  `baseline.json` is retained and a README points to the canonical historical
  draft with the same checksum.
- Superseded render/cache directories, disposable caches, empty directories,
  and three stale Word owner files were removed. Word's open-document list and
  filesystem handles were checked before deleting owner files.
- Original moved artifacts retain their bytes. Newly added READMEs explain
  historical paths and how to restore older scripts before running them.
- The root-consolidation archive's actual former manuscript, bibliography,
  configuration, and older publication outputs remain preserved.
- Existing frozen references, round snapshots, named review checkpoints, and
  exact Word exchange archives retain their files and paths.

The model/test sources and all 464 scientific-work files were verified unchanged.
The active QMD, review metadata, bibliography, and imported figures are unchanged.
No author-page, abstract, citation, or scientific-result revision was introduced.

## Render verification

Both HTML styles and APA Word were regenerated from the root configuration.
Each HTML output retains 517 boundary elements, including the expected TOC copies,
and loads the relocated stylesheet. The APA Word document retains 52 comment
records and 285 native revision fragments. Every document/review/formatting part
matches the approved third title checkpoint; only packaging timestamps and the
associated export identity differ.

Both live HTML previews, their stylesheets, and the APA Word download were
checked successfully. The downloaded Word file also passes the review-package
validator and matches the approved third title checkpoint. Results are recorded
in `manifest.json`.

The original audit and implemented/deferred distinctions are preserved in
[notes/directory-review.md](../../notes/directory-review.md).
