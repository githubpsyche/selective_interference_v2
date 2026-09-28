# Manuscript root consolidation — 27 September 2026

The active review manuscript was moved from `manuscript-review/` to the project
root. The manuscript and review metadata, frozen reference, staged checkpoints,
exchange archives, and imported images were preserved byte for byte.

`previous-root/` preserves the earlier root manuscript, its Quarto settings,
bibliography, ignore rules, and generated `docs/`. `index.staged.qmd` additionally
preserves the version that was in Git's index. The Git index was not changed.
The snapshot retains its original relative paths; its research assets remain
in the project root. Restore the source there to reproduce that earlier draft.

`previous-review-build/` and `previous-root-cache/` were removed during the
verified 27 September cleanup. They contained superseded generated files and
caches; their Word output has an exact retained copy in the review exchange
archive. Details are in `../2026-09-27-cleanup/manifest.json`. The existing root APAQuarto extension was identical to the
review project's copy and was reused.

`relocation.json` records checksums before the move. The active project now uses
root `index.qmd`, `review.yml`, `_quarto.yml`, and the existing `references.bib`.
Generated HTML and APA Word documents are written to root `docs/`.
