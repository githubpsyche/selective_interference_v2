# Review history

The current manuscript and review state are in [index.qmd](../index.qmd).
The frozen comparison is [reference.qmd](../reference.qmd).
The latest generated Word file is [docs/index.docx](../docs/index.docx).

## Approved title checkpoints — APA Word

1. [Emily's suggestion rejected](stages/2026-09-27-title/apaquarto/01-emily-title-rejected.docx).
2. [Our title suggested](stages/2026-09-27-title/apaquarto/02-our-title-suggested.docx).
3. [Reply added and comment resolved](stages/2026-09-27-title/apaquarto/03-title-comment-replied-resolved.docx).

Each has its source snapshot and verification manifest. Earlier generic Word
files in the parent stage directory are retained superseded exports.

## Directory responsibilities

- `reference/`: the legacy frozen comparison archive; the active comparison is root `reference.qmd`.
- `rounds/`: earlier preserved baseline snapshots.
- `stages/`: named checkpoints retained for discussion and verification.
- `exchanges/`: original Word input and exact content-addressed exports with the
  source state and identities needed to reconcile a collaborator's return.

Preserve established files and manifests at their current paths. Similar Word
files can carry distinct export identities; they are not disposable render
caches. Future retention changes belong in the review engine and must preserve
identities of documents that may have been shared.

Routine export directories are retained locally and ignored by Git.
Complete records for the named title checkpoints and the retained current Word output are explicitly tracked.
Before sharing a new export, use `git add -f review/exchanges/exports/<export-id>/` from the project root to track its document, source snapshot and identity map together.
No export records were deleted during the Git cleanup.
