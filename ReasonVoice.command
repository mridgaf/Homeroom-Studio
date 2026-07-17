#!/bin/bash
# Double-click me to start Reason Voice. It opens in your web browser.
cd "$(dirname "$0")"
exec ./.venv/bin/python -m reason_voice.server
