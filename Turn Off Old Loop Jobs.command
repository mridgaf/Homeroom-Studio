#!/bin/bash
# Turns off the old nightly loop jobs (Looperman 4 a.m. + the broken Freesound/Zapsplat/Splice ones).
# The new daily grab runs as a Claude scheduled task instead. Nothing is deleted:
# the job files are moved to Homeroom Studio/_to_delete/old-loop-jobs.
cd "$(dirname "$0")" || exit 1
DEST="$(pwd)/_to_delete/old-loop-jobs"; mkdir -p "$DEST"
for L in nightlyloops nightlyfreesound nightlyzapsplat nightlysplice; do
  P="$HOME/Library/LaunchAgents/com.homeroomstudio.$L.plist"
  if [ -f "$P" ]; then
    launchctl bootout "gui/$(id -u)" "$P" 2>/dev/null
    mv -n "$P" "$DEST/" && echo "Turned off: $L"
  fi
done
echo; echo "Still scheduled (should be none of the above):"
launchctl list | grep homeroomstudio || echo "  none"
echo; echo "Done. You can close this window."
