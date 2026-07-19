#!/bin/bash
# Double-click me to open Homeroom Studio.
# Lives in the PROJECT folder (internal drive), not in the beats folder —
# the beats library moves between drives, and a launcher that lived
# inside it died with the move (2026-07-18). beat_machine.py finds the
# library itself via beats_root.json.
# Paths are relative to this file (2026-07-19), so moving the project folder
# no longer breaks the launcher.
cd "$(dirname "$0")"
exec ./.venv/bin/python tools/beat_machine.py
