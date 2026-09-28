# Manuscript presentation

These files adapt the pooled Word import to the three formats selected in the
root `_quarto.yml`. They change presentation during rendering and preserve the
annotated QMD and frozen review reference.

| File | Responsibility |
| --- | --- |
| `manuscript-frontmatter.lua` | Moves the annotated Word title and author information into Quarto's regular-HTML title block while retaining `# Abstract` in the body. |
| `title-block.html` | Adds the annotated author line beside Quarto's native author metadata in regular HTML. |
| `manuscript-outline.lua` | HTML table-of-contents and imported heading corrections. |
| `manuscript-import.css` | Regular-HTML reading-view presentation. |
| `apa-import.lua` | Retains the literal imported References heading. |
| `apa-import.css` | APA HTML alignment and image sizing. |
| `apa-import-docx.lua` | Imported front matter and references use APAQuarto's Word styles and page breaks. |

Reusable review behavior belongs in the sibling `quarto-review` repository.
The installed integration remains under root `_extensions/quarto-review`.
Changing these adaptations requires checking review boundaries in both HTML
formats and native Word comment/revision preservation. Do not rewrite the
annotated source merely to change its presentation.
The regular-HTML front matter regression check is `tests/test_review_frontmatter.py`.
The original `abstract-section` extension from the local homophily project is
installed at `_extensions/pandoc-ext/abstract-section` for APA PDF only.
As in homophily, regular HTML renders the body `# Abstract` section directly.
