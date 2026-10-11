#!/bin/bash
# Renders 5 old-vs-new chord beats into Desktop > Homeroom Auditions.
# OLD: only use after a full test run. Engine code changed again on 2026-10-11 (variety pass) - use "0 RUN ME - Chord Patterns.command" instead.
cd "$(dirname "$0")" || exit 1
LOG="$(pwd)/Chord Patterns Render Log.txt"
./.venv/bin/python tools/make_chord_patterns_ab.py 2>&1 | tee "$LOG"
echo "Done. Listen in: Desktop > Homeroom Auditions > Homeroom CHORD PATTERNS ..." | tee -a "$LOG"
read -r -p "Press Return to close."
