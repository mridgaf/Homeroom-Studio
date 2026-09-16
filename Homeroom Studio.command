#!/bin/bash
# Double-click me to open Homeroom Studio — the whole thing.
#
# One door (packaging step 4, 2026-07-25): this starts all three pieces —
#   the Beat Machine   (makes beats)         http://localhost:8770
#   Reason Voice       (the studio helper)   http://localhost:8765
#   Sound Engine       (the FX button)       http://localhost:8767
# waits until they answer, and opens ONE page. Leave this window open
# while you work; closing it (or Ctrl+C here) stops all three.
#
# Want only the studio half? ReasonVoice.command still works on its own.
#
# Lives in the PROJECT folder (internal drive), not in the beats folder —
# the beats library moves between drives, and a launcher that lived
# inside it died with the move (2026-07-18). beat_machine.py finds the
# library itself via beats_root.json. Paths are relative to this file
# (2026-07-19), so moving the project folder doesn't break it.

cd "$(dirname "$0")" || exit 1

if [ ! -x ./.venv/bin/python ]; then
  echo
  echo "Can't find the app's Python (.venv is missing from this folder)."
  echo "Nothing was started."
  echo
  read -p "Press Return to close."
  exit 1
fi

BEAT_URL="http://localhost:8770"
VOICE_URL="http://localhost:8765"
SE_URL="http://localhost:8767"

up () { curl -s -o /dev/null --max-time 2 "$1"; }

# Each piece skips opening its own browser page (REASON_VOICE_NO_BROWSER /
# SOUND_ENGINE_NO_BROWSER) so this window opens exactly ONE page at the
# end. If a piece is already running from an earlier window, it's left
# alone and reused.
PIDS=""
if up "$VOICE_URL"; then
  echo "Reason Voice is already running — using it."
else
  REASON_VOICE_NO_BROWSER=1 ./.venv/bin/python -m reason_voice.server &
  PIDS="$PIDS $!"
fi
if up "$BEAT_URL"; then
  echo "The Beat Machine is already running — using it."
else
  REASON_VOICE_NO_BROWSER=1 ./.venv/bin/python tools/beat_machine.py &
  PIDS="$PIDS $!"
fi
if up "$SE_URL"; then
  echo "The Sound Engine is already running — using it."
else
  SOUND_ENGINE_NO_BROWSER=1 ./.venv/bin/python -m sound_engine.server &
  PIDS="$PIDS $!"
fi

# closing this window (or Ctrl+C) stops whatever this window started.
# INT/TERM/HUP are listed too: bash skips the EXIT trap when it's killed
# by an untrapped signal, and closing a Terminal window is a HUP.
trap 'kill $PIDS 2>/dev/null' EXIT INT TERM HUP

# Wait for both to answer. Reason Voice loads the speech model, so it can
# take a little while on a cold start.
echo "Starting up…"
BEAT_OK=""; VOICE_OK=""; SE_OK=""
for i in $(seq 1 40); do
  [ -z "$BEAT_OK" ]  && up "$BEAT_URL"  && BEAT_OK=yes  && echo "  beat machine: ready"
  [ -z "$VOICE_OK" ] && up "$VOICE_URL" && VOICE_OK=yes && echo "  reason voice: ready"
  [ -z "$SE_OK" ]     && up "$SE_URL"    && SE_OK=yes    && echo "  sound engine: ready"
  [ -n "$BEAT_OK" ] && [ -n "$VOICE_OK" ] && [ -n "$SE_OK" ] && break
  sleep 1
done

if [ -z "$BEAT_OK" ]; then
  echo
  echo "The Beat Machine didn't start. Scroll up — the reason is printed"
  echo "above this line. Nothing was opened."
  echo
  read -p "Press Return to close."
  exit 1
fi
if [ -z "$VOICE_OK" ]; then
  echo
  echo "Heads up: Reason Voice didn't come up, but the Beat Machine is"
  echo "fine — opening that. The voice half's error is printed above."
fi
if [ -z "$SE_OK" ]; then
  echo
  echo "Heads up: the Sound Engine (FX button) didn't come up, but the"
  echo "Beat Machine is fine — opening that. Its error is printed above."
fi

echo
echo "Homeroom Studio is open. Leave this window open while you work;"
echo "close it (or press Ctrl+C) to stop everything."
open "$BEAT_URL"

wait
