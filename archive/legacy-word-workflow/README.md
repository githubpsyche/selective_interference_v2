# Retired Word workflow experiments

These preserve the workflows used before the local Quarto review integration:

- `compare_index_docx.sh` and `compare_index.docx`: the earlier Word/AppleScript
  comparison route and a retained comparison output.
- `extract_composite_feedback_ordered.py` and `composite_feedback_ordered.md`:
  the earlier extraction tool and its source-grounded ordered feedback output.
- `merge_favor_source_true_test.docx`: the earlier merge experiment.
- `document_workflow_trial_20260927/`: conversion, redline, and abstract-preview
  experiments; its imported text preserves the earlier draft used for comparison.
- `word_web_trial/`: the original web-trial provenance and a pointer to the
  retained canonical document.
- `abstract-section/`: the filter used by the former APA PDF configuration.

The original files are preserved byte for byte, except that one proven identical
web-trial DOCX was removed in favor of its retained canonical copy. Original
absolute paths and script-relative paths are historical. Restore the old layout
recorded in the cleanup manifest before running a script. For example, the
comparison script originally lived at the project root, and the abstract filter
lived at `_extensions/pandoc-ext/abstract-section`.

The active engine is maintained in the sibling `quarto-review` repository.
