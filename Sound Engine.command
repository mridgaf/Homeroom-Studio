#!/bin/bash
# Double-click me to start the Sound Engine. It opens in your web browser.
cd "$(dirname "$0")"
exec ./.venv/bin/python -m sound_engine.server
