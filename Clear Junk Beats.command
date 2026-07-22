#!/bin/bash
# Double-click me to clear out every beat made so far.
# Moves all wav/mid/stems (and matching recipe files) into a dated
# "Cleared YYYY-MM-DD" folder inside the beats library — nothing is
# deleted, it's all just moved into one place you can inspect or trash
# later. It will ask you to type "yes" before moving anything.
cd "$(dirname "$0")"
exec ./.venv/bin/python tools/clear_junk_beats.py
