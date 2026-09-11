"""Sweep one Reason knob so you can watch it move. Proof, not a feature.

    ./.venv/bin/python reason_voice/prove_knob.py            # Knob 5 = Attack
    ./.venv/bin/python reason_voice/prove_knob.py knob_1     # = Threshold

FIRST, in Reason: Ctrl-click (right-click) the MClass Compressor's front panel
and choose "Lock to ReasonVoice".

Selecting/clicking the device is NOT enough. Reason 12 Operation Manual, ch.23 (pp.587-606):
control surfaces follow the sequencer's Master Keyboard Input, not the rack
selection -- and an MClass Compressor is an effect, so it never has a
sequencer track and can never hold Master Keyboard Input. Locking the surface
to the device is the only route to it. The lock saves with the song.
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
print("Done.\n"
      "Nothing moved? Two causes, in order of likelihood:\n"
      "  1. The compressor is not locked to ReasonVoice "
      "(Ctrl-click its panel -> 'Lock to ReasonVoice').\n"
      "  2. Reason was not fully quit after the files changed "
      "(Cmd+Q, not just closing the song).")
