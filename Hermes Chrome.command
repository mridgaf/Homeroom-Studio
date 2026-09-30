#!/bin/bash
# Opens a separate Chrome just for Hermes. Log into Looperman + Freesound here once,
# then leave this window open. Hermes uses it for the daily loop grab.
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.hermes/hermes-chrome" \
  --no-first-run "https://www.looperman.com/" "https://freesound.org/" >/dev/null 2>&1 &
echo "Hermes Chrome is open. Log into Looperman and Freesound there, then leave it open."
sleep 3
