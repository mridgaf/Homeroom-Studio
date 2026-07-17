#!/bin/bash
# Reason Voice installer (macOS)
set -e
cd "$(dirname "$0")"

echo "== Reason Voice install =="

# 1. Python environment
if ! command -v python3 >/dev/null; then
  echo "python3 not found. Install Xcode Command Line Tools or Homebrew python first."
  exit 1
fi
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip -q
./.venv/bin/pip install -r requirements.txt -q
echo "[ok] Python environment ready (.venv)"

# 2. Remote codec + map
REMOTE_BASE="$HOME/Library/Application Support/Propellerhead Software/Remote"
mkdir -p "$REMOTE_BASE/Codecs/Lua Codecs/ReasonVoice"
mkdir -p "$REMOTE_BASE/Maps/ReasonVoice"
cp remote/ReasonVoice.luacodec "$REMOTE_BASE/Codecs/Lua Codecs/ReasonVoice/"
cp remote/ReasonVoice.remotemap "$REMOTE_BASE/Maps/ReasonVoice/"
echo "[ok] Remote codec + map installed"

cat <<'EOF'

== Manual steps (one time) ==
1. IAC virtual MIDI bus:
   Open "Audio MIDI Setup" > Window > Show MIDI Studio > double-click
   "IAC Driver" > check "Device is online". Ensure "Bus 1" exists.

2. Register the control surface in Reason:
   Reason > Settings/Preferences > Control Surfaces > Add manually >
   Manufacturer "ReasonVoice", Model "ReasonVoice",
   MIDI input: "IAC Driver Bus 1". (Restart Reason if it's not listed.)

3. macOS permissions (System Settings > Privacy & Security):
   - Microphone: allow for Terminal (or whatever runs the app)

== Run it ==
   Double-click ReasonVoice.command — it opens in your web browser.

First run downloads the whisper model (~500 MB for small.en).
EOF
