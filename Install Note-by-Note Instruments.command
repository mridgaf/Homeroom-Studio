#!/bin/bash
# Adds the note-by-note instruments (VCSL + VSCO) to the Beat Machine.
# Double-click. Safe: it stops before changing anything if the patch doesn't fit.
cd "$HOME/Desktop/Homeroom Studio" || { echo "Homeroom Studio folder not found"; read -n1; exit 1; }
PATCH="$(dirname "$0")/note-by-note-instruments.patch"
[ -f "$PATCH" ] || PATCH="./note-by-note-instruments.patch"
if [ ! -d "/Volumes/TBOTC 3/Sample Packs/BOTC Multisampled Instruments" ]; then
  echo "TBOTC 3 drive not plugged in. Plug it in and double-click again."; read -n1; exit 1
fi
if [ -f tools/multisample.py ]; then
  echo "Already installed - skipping the patch."
else
  git apply --3way "$PATCH" || { echo; echo "Patch didn't fit. Nothing changed. Tell Claude."; read -n1; exit 1; }
fi
echo; echo "== New tests =="
./.venv/bin/python -m pytest tests/test_multisample.py -q || { echo "New tests FAILED. Tell Claude."; read -n1; exit 1; }
echo; echo "== Reading the instruments (first time takes a few minutes) =="
./.venv/bin/python tools/multisample.py | tee "Note-by-Note Report.txt"
echo; echo "== Full test suite (~8 min). Don't render beats until this finishes. =="
./.venv/bin/python -m pytest tests/ -q 2>&1 | tail -15 | tee -a "Note-by-Note Report.txt"
echo; echo "Done. Results saved in Note-by-Note Report.txt. Press any key."; read -n1
