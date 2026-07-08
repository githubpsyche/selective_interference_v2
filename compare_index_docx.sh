#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTES_DIR="$ROOT_DIR/notes"
REVISED_DOC="${REVISED_DOC:-$ROOT_DIR/docs/index.docx}"
OUTPUT_DOC="${OUTPUT_DOC:-$ROOT_DIR/notes/compare_index.docx}"
TIMEOUT_SECONDS="${COMPARE_TIMEOUT_SECONDS:-180}"

if [[ ! -d "$NOTES_DIR" ]]; then
  echo "Missing notes directory: $NOTES_DIR" >&2
  exit 1
fi

if [[ ! -f "$REVISED_DOC" ]]; then
  echo "Missing revised document: $REVISED_DOC" >&2
  exit 1
fi

LATEST_ADVISOR="$(
  python3 - "$NOTES_DIR" <<'PY'
import re
import sys
from pathlib import Path

notes_dir = Path(sys.argv[1])
pattern = re.compile(r"^advisor_feedback_(\d{4})[-_](\d{2})[-_](\d{2})\.docx$")
matches = []

for path in notes_dir.glob("advisor_feedback_*.docx"):
    match = pattern.match(path.name)
    if match:
        date_key = tuple(int(part) for part in match.groups())
        matches.append((date_key, path))

if not matches:
    sys.exit("No advisor_feedback_YYYY-MM-DD.docx files found in notes/")

matches.sort()
print(matches[-1][1])
PY
)"

if [[ ! -f "$LATEST_ADVISOR" ]]; then
  echo "Latest advisor document was not found: $LATEST_ADVISOR" >&2
  exit 1
fi

if ! command -v osascript >/dev/null 2>&1; then
  echo "Missing osascript; this script requires Microsoft Word on macOS." >&2
  exit 1
fi

if ! osascript -e 'tell application "Microsoft Word" to get version' >/dev/null 2>&1; then
  echo "Microsoft Word is not available to AppleScript." >&2
  exit 1
fi

# Stage files inside Word's sandbox container to reduce macOS file-access prompts.
WORD_CONTAINER="$HOME/Library/Containers/com.microsoft.Word/Data/tmp/selective_interference_compare"
rm -rf "$WORD_CONTAINER"
mkdir -p "$WORD_CONTAINER"

ORIGINAL_STAGED="$WORD_CONTAINER/original_advisor_feedback.docx"
REVISED_STAGED="$WORD_CONTAINER/revised_index.docx"
OUTPUT_STAGED="$WORD_CONTAINER/compare_index.docx"

cp "$LATEST_ADVISOR" "$ORIGINAL_STAGED"
cp "$REVISED_DOC" "$REVISED_STAGED"
rm -f "$OUTPUT_STAGED" "$OUTPUT_DOC"
mkdir -p "$(dirname "$OUTPUT_DOC")"

echo "Original: $LATEST_ADVISOR"
echo "Revised:  $REVISED_DOC"
echo "Output:   $OUTPUT_DOC"

run_compare() {
  osascript - "$ORIGINAL_STAGED" "$REVISED_STAGED" "$OUTPUT_STAGED" <<'APPLESCRIPT'
on run argv
  set originalPathText to item 1 of argv
  set revisedPathText to item 2 of argv
  set outputPathText to item 3 of argv

  tell application "Microsoft Word"
    set display alerts to alerts none
    open (POSIX file originalPathText)
    set originalDoc to active document
    compare originalDoc path revisedPathText author name "Codex Compare" target compare target new detect format changes true ignore all comparison warnings true add to recent files false
    set comparedDoc to active document
    save as comparedDoc file name outputPathText file format format document default add to recent files false
    try
      close comparedDoc saving no
    end try
    try
      close originalDoc saving no
    end try
  end tell
end run
APPLESCRIPT
}

run_compare &
COMPARE_PID=$!

(
  sleep "$TIMEOUT_SECONDS"
  if kill -0 "$COMPARE_PID" >/dev/null 2>&1; then
    echo "Word compare timed out after ${TIMEOUT_SECONDS}s. A macOS permission prompt or Word dialog may be waiting." >&2
    kill "$COMPARE_PID" >/dev/null 2>&1 || true
  fi
) &
WATCHDOG_PID=$!

set +e
wait "$COMPARE_PID"
COMPARE_STATUS=$?
set -e

kill "$WATCHDOG_PID" >/dev/null 2>&1 || true
wait "$WATCHDOG_PID" >/dev/null 2>&1 || true

if [[ "$COMPARE_STATUS" -ne 0 ]]; then
  echo "Word compare failed." >&2
  exit "$COMPARE_STATUS"
fi

if [[ ! -f "$OUTPUT_STAGED" ]]; then
  echo "Word compare completed but did not create: $OUTPUT_STAGED" >&2
  exit 1
fi

cp "$OUTPUT_STAGED" "$OUTPUT_DOC"
echo "Wrote $OUTPUT_DOC"
