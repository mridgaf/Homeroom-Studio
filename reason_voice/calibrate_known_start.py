"""Run calibrate.main() without waiting for Reason's lock announcement.

Only for a scratch device whose start position does not matter: every knob is
restored to START (default 0) afterwards. Usage:
  calibrate_known_start.py START --device "<scope>" knob_N ...
"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from reason_voice import calibrate

start_pos = int(sys.argv[1])
sys.argv = [sys.argv[0]] + sys.argv[2:]
calibrate.await_lock = lambda r, knobs, seconds=30, out=print: {k: start_pos for k in knobs}
code = 0
try:
    calibrate.main()
except SystemExit as e:
    if e.code not in (None, 0):
        print(e.code, file=sys.stderr)
        code = 1
sys.stdout.flush()
os._exit(code)
