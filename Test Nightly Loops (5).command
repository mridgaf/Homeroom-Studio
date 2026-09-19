#!/bin/bash
# Test run: downloads 5 loops into the review folder (_New Tonight). Nothing goes
# into your main library. Run "Save Looperman Login.command" first.
cd "$(dirname "$0")" || exit 1
PY="$(pwd)/.venv/bin/python"; [ -x "$PY" ] || PY=/usr/bin/python3

echo "=== Test: download 5 loops ==="
echo "The loop drive (TBOTC 3) must be plugged in."
echo
"$PY" tools/nightly_loops.py --count 5
echo
echo "Files are in:  TBOTC 3 > Sample Packs > BOTC Sorted Loops > _New Tonight"
echo "The same summary is saved in:  Nightly Loops/LATEST.txt"
echo
read -r -p "Press Return to close."
