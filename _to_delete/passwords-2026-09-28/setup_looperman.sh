#!/bin/bash
cd "$HOME/Desktop/Homeroom Studio" || exit 1

mkdir -p "Nightly Loops"
printf '%s' "johnsuhr007@gmail.com" > "Nightly Loops/.looperman_account"

security add-generic-password -U -s "HomeroomStudio Looperman" -a "johnsuhr007@gmail.com" -w "puvzot-3voxpi-jycsEk" 2>&1

PY="$(pwd)/.venv/bin/python"
[ -x "$PY" ] || PY=/usr/bin/python3

mkdir -p "$HOME/Library/LaunchAgents"
LABEL="com.homeroomstudio.nightlyloops"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

cat > "$PLIST" <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.homeroomstudio.nightlyloops</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$HOME/Desktop/Homeroom Studio/tools/nightly_loops.py</string>
    <string>--respect-window</string>
  </array>
  <key>WorkingDirectory</key><string>$HOME/Desktop/Homeroom Studio</string>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>4</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$HOME/Desktop/Homeroom Studio/Nightly Loops/launchd.log</string>
  <key>StandardErrorPath</key><string>$HOME/Desktop/Homeroom Studio/Nightly Loops/launchd.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "✓ Looperman nightly installed"
