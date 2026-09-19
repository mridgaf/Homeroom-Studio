#!/bin/bash
# Turns OFF the nightly loop download and the 3:58 a.m. wake-up.
# Nothing is deleted: the schedule file is moved into "Nightly Loops".
cd "$(dirname "$0")" || exit 1
LABEL="com.homeroomstudio.nightlyloops"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

echo "=== Turn off nightly loops ==="
launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null
if [ -f "$PLIST" ]; then
  mkdir -p "Nightly Loops"
  mv -n "$PLIST" "Nightly Loops/$LABEL.plist.removed-$(date +%Y-%m-%d)"
fi
echo "4:00 a.m. schedule: OFF"
echo
echo "The Mac will ask for your Mac login password to cancel the wake-up."
if sudo pmset repeat cancel; then echo "Wake at 3:58 a.m.: OFF"; else echo "Wake-up NOT cancelled."; fi
echo
read -r -p "Press Return to close."
