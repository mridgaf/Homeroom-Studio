"""Automation-recording test (2026-09-25).

Starts Reason recording through the ReasonVoice bridge, sweeps Knob 1 on the
locked device (Scream 4 -> Damage Control) up and back down over ~4 bars at
90 BPM, then stops. Afterwards, look for a new automation lane in Reason.
Knob 1's starting position is captured if Reason reports it, and restored.
"""
import os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from reason_voice.reason_control import ReasonControl

r = ReasonControl(speak_feedback=False)
if r.port is None:
    sys.exit("No IAC MIDI port found.")
print("Starting in 3 seconds...")
time.sleep(3)
if not os.environ.get("NO_TRANSPORT"): r.tap("record")
time.sleep(0.5)
up = list(range(0, 128, 2)); down = list(range(127, -1, -2))
steps = up + down
dur = 10.0
for v in steps:
    r.set_value("knob_1", v)
    r.poll()
    time.sleep(dur / len(steps))
time.sleep(0.5)
if not os.environ.get("NO_TRANSPORT"): r.tap("stop")
r.poll()
print("Done. Reason reported:", getattr(r, "displays", None) or "(nothing)")
