#!/bin/bash
# Chord flow (2026-09-26). Engine code changed again, so the FULL suite runs
# first (~16 min), then (only if it passes) 5 old-vs-new beat pairs render
# into Desktop > Homeroom Auditions. Tests finish before rendering starts.
cd "$(dirname "$0")" || exit 1
LOG="$(pwd)/Chord Flow Test Log.txt"
echo "=== Step 1 of 2: full test suite (about 16 min) ===" | tee "$LOG"
./.venv/bin/python -m pytest tests/ -q \
  2>&1 | tee -a "$LOG"
if [ "${PIPESTATUS[0]}" -ne 0 ]; then
  echo "TESTS FAILED - no beats rendered. Claude will read this log." | tee -a "$LOG"
  read -r -p "Press Return to close."; exit 1
fi
echo "=== Step 2 of 2: rendering 5 old-vs-new pairs ===" | tee -a "$LOG"
./.venv/bin/python tools/make_chord_flow_ab.py 2>&1 | tee -a "$LOG"
echo "Done. Listen in: Desktop > Homeroom Auditions > Homeroom CHORD FLOW ... v3" | tee -a "$LOG"
read -r -p "Press Return to close."
