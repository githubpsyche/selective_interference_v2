# Title review checkpoints

**Format correction:** use the [APAQuarto checkpoints](apaquarto/README.md).
The three Word files in this folder were rendered with generic `docx` by mistake.
They remain unchanged as superseded archives. The corrected files use the actual
`apaquarto-docx` format and preserve these same cumulative review states.

These are three cumulative Word exports from the live Quarto review project,
created on 27 September 2026. The fixed migration reference has not been recaptured.

| Stage | Word file | State |
| --- | --- | --- |
| 1 | [Emily's title suggestion rejected](01-emily-title-rejected.docx) | Rejects the five native insertion records `s1`–`s5`. The original title remains. Emily's comment is still open, with no new reply. |
| 2 | [Our title suggested](02-our-title-suggested.docx) | Adds pending tracked replacements `s286` and `s287`, one for each title occurrence, attributed to `Gunn, Jordan`. The comment remains open. |
| 3 | [Reply added and title comment resolved](03-title-comment-replied-resolved.docx) | Adds reply `r1` to Emily's original title thread `c1` and resolves the thread. The title replacements remain pending. |

The proposed title is:

> Intrusive and voluntary memory from a single system: A retrieved-context account of selective interference in the trauma-film paradigm

This was recovered from the earlier web-draft title recorded in
`notes/26_09_2026/minimal_feedback_review.md`, unit 01, and the retained Word draft.

The reply, attributed to `Gunn, Jordan`, is:

> Agreed. I’ve made the trauma-film setting explicit in the title and brought intrusive and voluntary memory into the opening phrase.

The matching folders preserve each stage's QMD, review YAML, and presentation
settings. `baseline/` preserves the pre-change working files and Word export.
`manifest.json` records file hashes, exact export identities, and verification.
The content-addressed exports also remain in `review/exchanges/exports/`.

Checks passed for all three exports: original comment identities, authors, dates,
thread relationships and anchors; unchanged unrelated revisions and their
attribution; both title projections; and the unchanged manuscript body and fixed
reference. Stages 1 and 2 retain all 51 original comment records. Stage 3 retains
those records and adds the requested reply, for 52 records. The only resolution
change is Emily's title thread and its new reply.

The final render's regular and APA HTML views contain all 514 review boundaries
exactly once across their title block and article, including both new title
replacements. Both views link to the final Word export. The preview's Word download
was fetched and checked against stage 3: the manuscript body and every comment,
reply, decision, revision, and other document part match. Quarto preview refreshed
the file's creation/modification timestamps and associated export ID; those are
the only package differences. The downloaded export is also retained in the
content-addressed archive. Later edits may update the live download; the three
named checkpoints here are retained unchanged.
