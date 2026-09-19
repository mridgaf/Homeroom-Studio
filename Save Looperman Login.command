#!/bin/bash
# Saves your Looperman login on this Mac (the password goes in the Keychain,
# never in a file), then tests the login. Downloads nothing.
cd "$(dirname "$0")" || exit 1
PY="$(pwd)/.venv/bin/python"; [ -x "$PY" ] || PY=/usr/bin/python3

echo "=== Save your Looperman login ==="
echo
read -r -p "Your Looperman email: " EMAIL
if [ -z "$EMAIL" ]; then echo "No email typed. Nothing saved."; read -r -p "Press Return to close."; exit 1; fi

mkdir -p "Nightly Loops"
printf '%s' "$EMAIL" > "Nightly Loops/.looperman_account"

echo
echo "Now type your Looperman password. Nothing shows as you type."
echo "Press Return, then type it once more to confirm."
security add-generic-password -U -s "HomeroomStudio Looperman" -a "$EMAIL" -w
if [ $? -ne 0 ]; then
  echo "The password was NOT saved."; read -r -p "Press Return to close."; exit 1
fi

echo
echo "Saved. Testing the login now (this downloads nothing)..."
echo
"$PY" tools/nightly_loops.py --check-login
echo
read -r -p "Press Return to close."
