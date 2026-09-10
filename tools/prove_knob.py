"""Sweep one Reason knob so you can watch it move. Proof, not a feature.

    ./.venv/bin/python tools/prove_knob.py            # Knob 5 = Attack
    ./.venv/bin/python tools/prove_knob.py knob_1     # = Threshold

Select an MClass Compressor in Reason first -- knobs act on the selected device.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reason_voice.reason_control import ReasonControl

knob = sys.argv[1] if len(sys.argv) > 1 else "knob_5"
r = ReasonControl(speak_feedback=False)
if r.port is None:
    sys.exit("No IAC MIDI port. Audio MIDI Setup > IAC Driver > Device is online.")

print(f"Sweeping {knob} 0 -> 127 -> 64. Watch the compressor.")
for v in list(range(0, 128, 4)) + list(range(127, 63, -4)):
    r.set_value(knob, v)
    time.sleep(0.02)
print("Done. If nothing moved, Reason wasn't restarted (Cmd+Q, not just close song).")
