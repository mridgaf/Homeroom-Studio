#!/bin/bash
cd "$HOME/Desktop/Homeroom Studio" || exit 1
mkdir -p "Nightly Loops"
security add-generic-password -U -s "HomeroomStudio Freesound" -a "johnsuhr007@gmail.com" -w "zyfqaj-sunvav-tybPu3" 2>&1 | grep -v "already exists" || true
LABEL="com.homeroomstudio.nightlyfreesound"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
cat > "$PLIST" <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.homeroomstudio.nightlyfreesound</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$HOME/Desktop/Homeroom Studio/tools/freesound_nightly.py</string>
  </array>
  <key>WorkingDirectory</key><string>$HOME/Desktop/Homeroom Studio</string>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>4</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$HOME/Desktop/Homeroom Studio/Nightly Loops/freesound.log</string>
  <key>StandardErrorPath</key><string>$HOME/Desktop/Homeroom Studio/Nightly Loops/freesound.log</string>
</dict>
</plist>
EOF
launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "✓ Freesound nightly: 4:00 a.m."
read -r -p "Press Return to close"
