# Manuscript presentation

These files adapt the pooled Word import to the three formats selected in the
root `_quarto.yml`. They change presentation during rendering and preserve the
annotated QMD and frozen review reference.

| File | Responsibility |
| --- | --- |
| `manuscript-frontmatter.lua` | Moves the annotated Word title and author information into Quarto's regular-HTML title block while retaining `# Abstract` in the body. |
| `title-block.html` | Adds the annotated author line beside Quarto's native author metadata in regular HTML. |
| `manuscript-outline.lua` | Keeps imported front-matter headings out of the HTML table of contents. Body heading levels are authoritative in the QMD. |
| `manuscript-import.css` | Regular-HTML reading-view presentation. |
| `apa-import.lua` | Retains the literal imported References heading. |
| `apa-import.css` | APA HTML alignment and image sizing. |
| `apa-import-docx.lua` | Imported front matter and references use APAQuarto's Word styles and page breaks. |
| `finish-docx.py` | Applies Word-only table widths, note styling and figure pagination after native review export, preserving text and review records. |

Reusable review behavior belongs in the sibling `quarto-review` repository.
The installed integration remains under root `_extensions/quarto-review`.
Changing these adaptations requires checking review boundaries in both HTML
formats and native Word comment/revision preservation. Do not rewrite the
annotated source merely to change its presentation.

The source distinguishes a table's short caption from its explanatory `.table-note` block.
The source supplies the conventional “Note.” label in every format.
The Word adapter styles that note and all entries in the References section, independently of citation anchors.
Table cells, table notes and figure captions use single spacing at the existing type size; manuscript body spacing is unchanged.
The Word finishing hook runs after the review hook and updates the finished-output hash so repeated finishing remains safe.
It changes only layout properties, leaving pending wording and image revisions intact.
Before/after images occupy separate lines with widow/orphan control disabled, so a caption can stay with the first image while the second continues on the next page.
Large before/after images can still span multiple pages.

The project enables subsequent Word editing with `quarto-review.word.track-changes: true` in `_quarto.yml`.
The installed `finish.py` and `word_options.py` implement this reusable setting with the existing pinned runtime; `_environment.local` is unchanged.
The regular-HTML front matter regression check is `tests/test_review_frontmatter.py`.
The original `abstract-section` extension from the local homophily project is
installed at `_extensions/pandoc-ext/abstract-section` for APA PDF only.
As in homophily, regular HTML renders the body `# Abstract` section directly.
