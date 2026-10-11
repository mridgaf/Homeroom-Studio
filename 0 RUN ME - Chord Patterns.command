#!/bin/bash
# Chord pattern library (2026-10-11). Engine code changed, so the FULL suite
# runs first (~17 min, run it ALONE), then 5 old-vs-new beats render into
# Desktop > Homeroom Auditions. Tests finish before rendering starts.
cd "$(dirname "$0")" || exit 1
# The Mac's own disk reports only ~5 GB free (the rest is "purgeable"), and the
# last run hit disk errors partway. Put the tests' scratch files on the TBOTC 3 drive.
TMPBASE="/Volumes/TBOTC 3/pytest-scratch"
if [ ! -d "/Volumes/TBOTC 3" ]; then echo "TBOTC 3 drive not found - plug it in first."; read -r -p "Press Return to close."; exit 1; fi
mkdir -p "$TMPBASE"
export TMPDIR="$TMPBASE/"
LOG="$(pwd)/Chord Patterns Test Log.txt"
echo "=== Step 1 of 2: full test suite (about 17 min) ===" | tee "$LOG"
./.venv/bin/python -m pytest tests/ -q --basetemp="$TMPBASE/run" 2>&1 | tee -a "$LOG"
if [ "${PIPESTATUS[0]}" -ne 0 ]; then
  echo "TESTS FAILED - no beats rendered. Claude will read this log." | tee -a "$LOG"
  read -r -p "Press Return to close."; exit 1
fi
echo "=== Step 2 of 2: rendering 5 old-vs-new beats ===" | tee -a "$LOG"
./.venv/bin/python tools/make_chord_patterns_ab.py 2>&1 | tee -a "$LOG"
echo "Done. Listen in: Desktop > Homeroom Auditions > Homeroom CHORD PATTERNS ..." | tee -a "$LOG"
read -r -p "Press Return to close."
