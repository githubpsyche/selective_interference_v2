# Quarto review with CriticMarkup and a fixed reference

> Implemented design record, with revised migration scope agreed afterward. The working system uses the untouched Henson/Holmes pool plus the three title-review steps. The earlier instruction below to reconcile the cloud Word draft before migration was superseded by that choice. Use the [project README](../../README.md) for current files, scope, and commands.

Updated 27 September 2026. Design agreed in chat; the initial implementation and verification are complete in the separate repository at `/Users/jordangunn/workspace/quarto-review`. This plan records the agreed workflow; the compatibility report lists the supported cases and remaining limits.

The initial implementation now includes source review commands, frozen QMD/YAML and executed references, Quarto rendering and live preview, native Word export, and reconciliation against retained exports. The full local suite passes 114 tests, including the private fixture, the existing APA format, live review updates, and independent reviewers returning the same export. A complete native review cycle passed in Word for Mac 16.113.2: add a reply, resolve a thread, accept/reject edits, save, import, render, reopen, and save again. Repeated and unchanged return imports introduced no extra changes; the frozen reference was preserved. Current evidence and explicit limits are recorded in [the compatibility report](/Users/jordangunn/workspace/quarto-review/docs/status.md); everyday commands are in [the repository README](/Users/jordangunn/workspace/quarto-review/README.md). The current manuscript has not been migrated.

## Working files and reference

For a manuscript with one source file, maintain this structure:

```text
index.qmd                    Current manuscript, suggestions, and initial comments
review.yml                   Authors, dates, replies, states, and stable identifiers
review/reference/
    index.qmd                Frozen manuscript at the start of this review round
    review.yml               Frozen review metadata from the same point
```

The QMD is authoritative for prose, explicit suggested wording, initial comment text, and comment anchors. YAML is authoritative for attribution, timestamps, reply bodies and relationships, resolution states, suggestion decisions, and Word provenance. Do not duplicate initial comment text in the working YAML.

In everyday use, we edit `index.qmd` and `review.yml`. The corresponding files under `review/reference/` are a frozen pair maintained by the tools. Original Word files and exchange records are also kept automatically; they preserve information needed to return active threads to Word and reconcile collaborators' replies.

Use CriticMarkup for both suggestions and comments. For example:

```markdown
The effect was {~~large~>modest~~}{#s12}.

This is {==the passage being discussed==}{>>Clarify this claim.<<}{#c17}
```

The compact identifiers are an extension to standard CriticMarkup. They connect source annotations to their metadata. Replies remain in YAML so long discussions do not obscure the manuscript. Each reply retains its own author, date, identifier, and parent relationship.

The reference freezes both the QMD and YAML. For a project with multiple manuscript sources, freeze all relevant QMD files. Preserve the corresponding configuration, bibliography, and required assets or cached rendered dependencies so the reference is reproducible. Keep received and sent Word files with small exchange records identifying their reference and exported source version. The tools maintain these snapshots and archives.

Rendering never advances the reference. Starting a new round explicitly creates a new reference and archives the previous one, including its review state.

## Everyday workflow

1. Establish a reference from an existing Quarto project or a reconciled Word import. Archive the original Word file and extract its review information directly.
2. Edit the manuscript normally. Rendering automatically identifies net prose changes against the fixed reference. Explicit CriticMarkup controls grouping where desired, such as showing one sentence replacement instead of many small changes. Do not count explicit and automatically detected changes twice.
3. Read feedback in the source, chat, or rendered HTML. Tools expose the anchored passage and the complete thread assembled from QMD and YAML. Discuss edits, replies, resolution/reopening, and suggestion acceptance/rejection here.
4. Use ordinary `quarto preview` and `quarto render` to build outputs. HTML provides original, proposed, and redline views, anchored threads, navigation, and author/status filters. Word contains native revisions and active comment threads. PDF defaults to the proposed clean text.
5. Import collaborators' returned Word files against the exact export they received. Preserve identities, avoid duplicate imports, and report conflicting changes. Start another round only when explicitly requested.

Compare manuscript prose separately from review records: parse initial comments from QMD and combine them with YAML before comparing threads with the reference. Editing or replying to a comment must not appear as a prose revision. Apply explicit accept/reject decisions to an in-memory view of the reference review state before calculating new edits, so rejecting a collaborator's suggestion is not attributed to Jordan as a new deletion. Leave the saved reference unchanged.

## Implementation and interfaces

- Use a project-local Pandoc launcher, Lua filters, and Quarto project render hooks, composed with existing formats including this project's `apaquarto-docx`. The launcher prepares review syntax before Quarto's initial Markdown parse; a filter alone proved too slow on the large test fixture. The setup command maintains its local settings without modifying Quarto itself. Parse CriticMarkup into structured elements while retaining citations, equations, links, formatting, and block structure. Markup inside code examples remains literal.
- Align document blocks, then compare words within matched prose. Handle citations, equations, and other structured content as units. Preserve explicit change boundaries and stable annotation identities as text moves.
- Use Python and namespace-aware XML processing to import Word review records and finish generated DOCX files. Preserve original comment text, attribution, reply relationships, resolution states, and pending revisions. Retain the export mappings needed to reconcile returned files.
- Support comments across edited passages and overlapping ranges through the internal anchor model. Locate and report ambiguous anchors, conflicting suggestions, and unsupported constructs; never silently discard or move feedback.
- Provide a small command-line interface for setup, reference capture, Word import, feedback listing, replies, resolve/reopen, accept/reject, change grouping, and validation. Return structured results for use by an LLM. Source operations update QMD or YAML according to the ownership rules above.
- Keep rendering local and deterministic. Cache reference parsing and mappings and process affected inputs only. Render hooks may update generated files and caches, but must not rewrite authoring sources or references. No model calls, screenshots, or browser automation belong in the rendering path.

## Validation and delivery

Build the native Word preservation proof first, followed by Quarto integration and the HTML review presentation. Package the result with installation instructions, synthetic examples, regression fixtures, and a compatibility report.

- Round-trip the existing private local fixture and verify all 52 comment records and five reply relationships, including content, authors, anchors, and states. Verify revision text and attribution independently of XML run counts.
- Confirm initial comments survive QMD → Word → QMD with their metadata and replies correctly linked, without duplicated comment bodies. Test edits to comment text separately from prose edits.
- Confirm accepting exported changes yields the proposed text and rejecting them restores the appropriate reference text. Test both explicit CriticMarkup and ordinary edits detected against the reference.
- Cover replies, resolve/reopen, multiple reviewers, repeated imports, conflicting returns, paragraph replacements, whitespace, Unicode, overlapping ranges, deleted anchors, tables, captions, footnotes, citations, equations, and cross-references.
- Confirm repeated renders preserve source and reference files and do not duplicate review items. Check integration with the existing APA format and clean PDF output.
- Validate DOCX structure independently and perform a small manual Word compatibility check before declaring native review support complete.
- Benchmark cold and cached processing. Target no more than two seconds of added review processing for a 50,000-word, 500-comment fixture on this Mac, excluding ordinary Quarto rendering and analytical computation. Publish actual benchmark results.

## Defaults and migration

- New revisions use `Gunn, Jordan`; imported reviewers retain their identities.
- Quarto controls layout. The comparison reference is distinct from Word's formatting-template setting.
- HTML supports reading and navigation; decisions happen through chat or source. Cloud synchronization and a separate writing application are outside this project.
- Private manuscripts stay outside the reusable repository. Preserve original inputs and previous round snapshots.
- The saved local Word file is a technical fixture, not a confirmed current draft. Before migrating this manuscript, reconcile the latest Word content and existing Quarto source, including the already approved abstract, then establish the reference. Do not treat the root `index.qmd` or stale local DOCX as the current draft without that reconciliation.

Design references: [CriticMarkup notation](https://github.com/CriticMarkup/CriticMarkup-toolkit), [existing Quarto CriticMarkup extension](https://github.com/mloubout/critic-markup), [Quarto filters](https://quarto.org/docs/extensions/filters.html), and [Quarto project scripts](https://quarto.org/docs/projects/scripts.html#pre-and-post-render). The existing CriticMarkup extension's Word output uses formatting; native revisions and threaded comments are additional work in this plan.
