# Document workflows without Computer Use

> Superseded workflow research, retained 27 September 2026. The active workflow is the local Quarto review system described in the [project README](../../README.md). Recommendations below to start from an earlier Word copy or avoid root index.qmd describe the pre-migration situation. Historical Word drafts are catalogued in [the archive](../../archive/README.md).

Research checked 27 September 2026. This is a recommendation record, not an approved migration plan. No new connector was installed or manuscript changed during this research.

## Recommendation for the current revision pass

Use a fresh Markdown or Quarto draft alongside an explicitly linked review register. Conduct the passage-by-passage discussion in the existing Codex chat and edit these files directly. Produce Word checkpoints when a batch of edits has been agreed, rather than after every sentence.

Start the text draft from `selective_interference_minimal_revision_working.docx` in this folder, including the title-page work already done. Do not start from the root `index.qmd`: that manuscript contains later changes whose inclusion in this minimal revision pass has not been agreed.

The existing `minimal_feedback_review.md` is a source map and proposal record. It covers 100 reviewer-comment records across the specified Rik, Emily, and Deborah sources and links the relevant meeting notes. It is not itself a complete, synchronized representation of the working Word document and all its review metadata.

For a migration, preserve the source DOCX files and extract the review information explicitly: source file, original comment ID, author, date, exact text, anchored passage, parent/reply relationships, and resolution state. Existing tracked changes need a separate record of their original and proposed text, author, and disposition; a readable text extraction must not silently count as accepting them. Link each proposed minimal edit and response to its source feedback. Record agreed wording and decisions without overwriting the reviewers' original words.

This permits reading, discussing, replying to, and recording resolution of feedback in the intermediate workspace. Those decisions would only appear in Word once applied back to a Word checkpoint. Native Word thread synchronization is a separate requirement, not something ordinary Markdown provides.

## Markdown and Quarto

The project already uses Quarto in `index.qmd` and has an APA-related extension. Quarto supports Word output, including use of a reference document for styling. It is therefore an established route for producing a clean manuscript, although reproducing the exact appearance of the reviewed DOCX requires checking the output. [Quarto Word documentation](https://quarto.org/docs/output-formats/ms-word.html)

Pandoc's DOCX reader can retain insertions, deletions, comments, authors, and dates with `--track-changes=all`. Its default instead incorporates changes and ignores comments. This is useful for extraction, but the documented general conversion limitations mean it should not be treated as a guarantee of lossless Word review history. Reply relationships and resolution states must be checked against the original DOCX metadata. [Pandoc manual](https://pandoc.org/MANUAL.html#option--track-changes)

For a clean final manuscript, use the Quarto export route. If collaborators need the original threads and native tracked revisions, test applying the agreed edits and reply/status updates to a copy of the original DOCX. That is a distinct export task; it should be validated before committing a whole revision pass to the new workflow.

## Optional interface: Roughdraft

[Roughdraft](https://github.com/Lex-Inc/roughdraft) presents local Markdown in an editing and review interface. Its documented format supports comments, anchored highlights, insertions, deletions, substitutions, author/date metadata, and replies. Its experimental MCP tools can read pending feedback, append replies, and mark items resolved. The Markdown file remains the durable record, so an agent can interact without screen control.

It is a promising interface for this workflow, not a verified Word importer/exporter. Its documentation does not establish preservation of our existing DOCX threads or support for every Quarto feature. Before adopting it, test a short passage containing a real reviewer thread and a suggestion, plus representative equations, citations, figures, and tables. No installation or manuscript test has been performed.

Plain Markdown plus the existing review register remains usable without installing an editor or connector.

## Staying in Word and this Codex chat

### Word for the web: try before migrating formats

Jordan suggested Word for the web after the initial comparison. This is a sensible next trial because it keeps the manuscript in Word while potentially allowing browser automation through text, accessible controls, and keyboard commands, without screenshots. Microsoft documents web support for comment threads, replies, resolving/reopening, and tracked changes with acceptance/rejection subject to editing permissions. [Web comment accessibility](https://support.microsoft.com/en-us/accessibility/word/use-a-screen-reader-to-add-read-and-delete-comments-in-word), [Word for the web service description](https://learn.microsoft.com/en-us/office365/servicedescriptions/office-online-service-description/word-online)

These documents establish product features, not that the available browser tools can reliably expose every anchored passage or revision. No live Word web session was inspected in this research. Test a duplicate through a signed-in document link: read one complete thread and its anchor, perform one tracked edit with the correct author, and exercise a reply and resolution/reopening. Keep the trial entirely text-based. Its outcome should determine whether to continue in Word or adopt the intermediate Markdown workflow. This is browser interface automation, rather than a direct document API.

### Direct document API through an add-in

Microsoft's Office.js APIs support comment anchors, replies, and resolution state, plus individual tracked-change acceptance/rejection. The installed Word for Mac version was read as 16.113.2; the relevant API sets are supported by earlier Mac versions. Runtime feature checks would still be needed. [Comment API](https://learn.microsoft.com/en-us/javascript/api/word/word.comment?view=word-js-preview), [tracked-change API](https://learn.microsoft.com/en-us/javascript/api/word/word.trackedchange?view=word-js-preview), [supported versions](https://learn.microsoft.com/en-us/javascript/api/requirement-sets/word/word-api-requirement-sets?view=word-js-preview)

Codex supports MCP connections, allowing an add-in to expose structured Word operations to the existing chat. [OpenAI MCP documentation](https://developers.openai.com/codex/mcp)

The [Mindstone Office connector](https://github.com/mindstone/mcp-servers/blob/main/connectors/office/README.md) uses an Office.js add-in and local helper. Its Word source implements native comment replies, resolution, and revision acceptance/rejection. However, inspection of `getComments` found that it returns root-comment fields without loading replies or the anchored text, despite the README's broader claim. It also does not expose reopening comments or explicitly managing the tracking mode in the inspected Word command file. Those gaps make it a starting point requiring changes and testing. Its license is FSL-1.1-MIT, not simply MIT. [Inspected command implementation](https://github.com/mindstone/mcp-servers/blob/main/connectors/office/src/addin/commands/wordCommands.ts)

The [word-mcp-live connector](https://github.com/ykarapazar/word-mcp-live) explicitly lists threaded comment replies and resolving/unresolving as unavailable on macOS. It therefore does not meet the full review requirement here.

## Ready-made alternative assistant

[Claude for Word](https://claude.com/docs/office-agents/word) is a native Word add-in. Its current documentation lists Mac support, reading existing revisions, producing native tracked edits, and working through anchored comment threads with replies. It is available on Pro, Max, Team, and Enterprise plans. This is the strongest ready-made candidate found for staying in Word, but would move the editorial conversation to Claude; our project decisions and writing standards would need transferring. Automatic resolve/reopen and the desired revision-author attribution were not established by the documentation checked. No hands-on test was performed.

## Direct DOCX editing without a live Word connection

It is also possible to edit the saved DOCX structure directly. The previous delays largely concerned managing Word's live interface around file edits. A workflow that reads a saved source and writes a separate output copy can avoid that interface entirely, at the cost of manual handoff between copies.

[docx-comments-mcp](https://github.com/kosh-jelly/docx-comments-mcp) advertises saved-file reading and writing of comments, replies, resolution, and tracked changes, including accepting/rejecting changes. It is an untested candidate; its default author is `Claude`, so every write would need an explicit author override. Generic `python-docx` alone is insufficient for the complete review workflow because its documented comment support excludes replies and resolved state. [python-docx comment documentation](https://python-docx.readthedocs.io/en/latest/user/comments.html)

For all future review operations on this manuscript, use Jordan's requested Word author label, **Gunn, Jordan**, and verify the actual saved attribution. Preserve the original reviewers' attribution.

## Smallest useful trial

Use a copy of one passage and its real comment thread. Verify that the intermediate representation retains the anchor, author, existing replies, status, and any tracked revision. Make one agreed edit and a reply, then create a Word checkpoint and check those same properties through document data. This tests the essential return path before a full migration. The manuscript's final visual layout can be reviewed separately by Jordan in Word.
