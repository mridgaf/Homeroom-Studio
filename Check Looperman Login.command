#!/bin/bash
# Tries the saved Looperman login again. Downloads nothing.
# Saves what the site answered in "Nightly Loops/login-debug.txt" (no password in it).
cd "$(dirname "$0")" || exit 1
PY="$(pwd)/.venv/bin/python"; [ -x "$PY" ] || PY=/usr/bin/python3
echo "=== Checking your Looperman login (downloads nothing) ==="
echo
"$PY" tools/nightly_loops.py --check-login
echo
read -r -p "Press Return to close."
