#!/bin/bash
cd "$HOME/Desktop/Homeroom Studio" || exit 1

mkdir -p "Nightly Loops"
printf '%s' "johnsuhr007@gmail.com" > "Nightly Loops/.freesound_account"

# Save Freesound password to Keychain
security add-generic-password -U -s "HomeroomStudio Freesound" -a "johnsuhr007@gmail.com" -w "zyfqaj-sunvav-tybPu3" 2>&1 | grep -v "already exists" || true

echo "✓ Freesound login saved"

# Install Freesound nightly at 5:00 a.m. (after Looperman at 4:00)
LABEL_FS="com.homeroomstudio.nightlyfreesound"
PLIST_FS="$HOME/Library/LaunchAgents/$LABEL_FS.plist"

cat > "$PLIST_FS" <<'EOF'
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
  <dict><key>Hour</key><integer>5</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>$HOME/Desktop/Homeroom Studio/Nightly Loops/freesound.log</string>
  <key>StandardErrorPath</key><string>$HOME/Desktop/Homeroom Studio/Nightly Loops/freesound.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$PLIST_FS" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_FS"

echo "✓ Freesound nightly: 5:00 a.m. daily, 60 loops"
echo
echo "Both systems are now running:"
echo "  • Looperman: 4:00 a.m., 45 loops"
echo "  • Freesound: 5:00 a.m., 60 loops"
echo
read -r -p "Press Return to close"
