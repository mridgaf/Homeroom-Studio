#!/bin/bash
# Runs ONE test that errored, saves the full error + disk space to a file for Claude. Takes seconds.
cd "$(dirname "$0")" || exit 1
OUT="$(pwd)/Test Error Detail.txt"
{
  echo "=== disk ==="; df -h / "$(pwd)" /private/var/folders 2>&1
  echo "=== tmp dir ==="; python3 -c "import tempfile;print(tempfile.gettempdir())"
  echo "=== one test ==="
  ./.venv/bin/python -m pytest "tests/test_variety.py::test_backbeat_modes_actually_spread" -x --tb=long -q 2>&1 | tail -60
} > "$OUT" 2>&1
echo "Saved. You can close this window. Tell Claude: done"
read -r -p "Press Return to close."
