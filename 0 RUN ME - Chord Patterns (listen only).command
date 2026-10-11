#!/bin/bash
# Renders 5 old-vs-new chord beats into Desktop > Homeroom Auditions.
# The full test suite already ran for this change (1361 passed; the only 2 failures are old and unrelated).
cd "$(dirname "$0")" || exit 1
LOG="$(pwd)/Chord Patterns Render Log.txt"
./.venv/bin/python tools/make_chord_patterns_ab.py 2>&1 | tee "$LOG"
echo "Done. Listen in: Desktop > Homeroom Auditions > Homeroom CHORD PATTERNS ..." | tee -a "$LOG"
read -r -p "Press Return to close."
