#!/bin/bash
# Double-click me for a clean-slate reset of the Legends and the 9 DJs.
# Moves every beat out of the 12 Legend folders and 9 DJ folders into a
# dated "Cleared YYYY-MM-DD" holding folder — Favorites and Fixed Bank
# are left alone. It will ask you to type "yes" before moving anything.
#
# It then also PERMANENTLY empties the Trash folder (files already
# rejected there) — that step asks you to type DELETE, and cannot be
# undone.
cd "$(dirname "$0")"
exec ./.venv/bin/python tools/clear_legends_djs.py
