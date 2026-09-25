"""Bridge Record + sweep several knobs in turn, then Stop (2026-09-25 night 2).
Usage: multi_knob_test.py 3 5 12   (knob numbers on the locked device)"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from reason_voice.reason_control import ReasonControl

r = ReasonControl(speak_feedback=False)
if r.port is None:
    sys.exit("No IAC MIDI port found.")
knobs = [int(k) for k in sys.argv[1:]] or [3]
r.tap("record"); time.sleep(1.0)
for k in knobs:
    for v in list(range(0, 128, 4)) + list(range(127, -1, -4)):
        r.set_value(f"knob_{k}", v); r.poll(); time.sleep(0.06)
    time.sleep(0.5)
r.tap("stop"); time.sleep(0.5); r.poll()
for k, (name, shown) in sorted(r.displays.items()):
    print(k, name, shown)
