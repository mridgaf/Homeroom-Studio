#!/bin/bash
# Turns on the nightly loop download: wakes the Mac at 3:58 a.m., runs at 4:00 a.m.
# Run "Save Looperman Login.command" first and test 5 loops before using this.
cd "$(dirname "$0")" || exit 1
HERE="$(pwd)"
PY="$HERE/.venv/bin/python"; [ -x "$PY" ] || PY=/usr/bin/python3
LABEL="com.homeroomstudio.nightlyloops"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

echo "=== Turn on nightly loops ==="
echo "Every night: Mac wakes 3:58 a.m., loops download from 4:00 a.m."
echo

if ! /usr/bin/security find-generic-password -s "HomeroomStudio Looperman" >/dev/null 2>&1; then
  echo "No saved Looperman login found. Run 'Save Looperman Login.command' first."
  read -r -p "Press Return to close."; exit 1
fi

mkdir -p "$HOME/Library/LaunchAgents" "$HERE/Nightly Loops"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PY</string>
    <string>$HERE/tools/nightly_loops.py</string>
    <string>--respect-window</string>
  </array>
  <key>WorkingDirectory</key><string>$HERE</string>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>4</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$HERE/Nightly Loops/launchd.log</string>
  <key>StandardErrorPath</key><string>$HERE/Nightly Loops/launchd.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null
if launchctl bootstrap "gui/$(id -u)" "$PLIST"; then
  echo "4:00 a.m. schedule: ON"
else
  echo "Could not turn on the schedule."; read -r -p "Press Return to close."; exit 1
fi

echo
echo "--- Wake-up ---"
echo "Current wake/power schedule on this Mac:"
pmset -g sched
if pmset -g sched | grep -q "Repeating power events"; then
  echo
  echo "This Mac ALREADY has a repeating wake/power schedule (shown above)."
  echo "Turning on nightly loops would replace it."
  read -r -p "Type yes to replace it, or anything else to skip the wake-up: " OK
  [ "$OK" = "yes" ] || { echo "Wake-up skipped. The 4 a.m. job only runs if the Mac is awake."; read -r -p "Press Return to close."; exit 0; }
fi
echo
echo "The Mac will now ask for your Mac login password (once)."
if sudo pmset repeat wakeorpoweron MTWRFSU 03:58:00; then
  echo "Wake at 3:58 a.m.: ON"
else
  echo "Wake-up was NOT set. The 4 a.m. job only runs if the Mac is awake."
fi
echo
echo "Done. Each morning, read: Nightly Loops/LATEST.txt"
echo "To turn it off: double-click 'Uninstall Nightly Loops.command'."
read -r -p "Press Return to close."
