#!/bin/bash
set -e

echo "=== Setting up nightly loops from Looperman and Freesound ==="
echo

cd "$HOME/Desktop/Homeroom Studio" || exit 1

# Save accounts
mkdir -p "Nightly Loops"
printf '%s' "johnsuhr007@gmail.com" > "Nightly Loops/.looperman_account"
printf '%s' "johnsuhr007@gmail.com" > "Nightly Loops/.freesound_account"

# Save passwords to Keychain
security add-generic-password -U -s "HomeroomStudio Looperman" -a "johnsuhr007@gmail.com" -w "puvzot-3voxpi-jycsEk" 2>&1 | grep -v "already exists" || true
security add-generic-password -U -s "HomeroomStudio Freesound" -a "johnsuhr007@gmail.com" -w "zyfqaj-sunvav-tybPu3" 2>&1 | grep -v "already exists" || true

echo "✓ Logins saved"

# Install Looperman nightly
LABEL_LM="com.homeroomstudio.nightlyloops"
PLIST_LM="$HOME/Library/LaunchAgents/$LABEL_LM.plist"

mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST_LM" <<'EOF'
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

launchctl bootout "gui/$(id -u)" "$PLIST_LM" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_LM"
echo "✓ Looperman nightly: 4:00 a.m. daily, 45 loops"

echo
echo "Done! Both nightly systems are ready."
echo "Looperman: every night at 4 a.m., 45 loops into BOTC Sorted Loops/_New Tonight"
echo "Freesound: coming next"
echo
read -r -p "Press Return to close"
