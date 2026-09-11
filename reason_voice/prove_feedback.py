"""Prove Reason talks BACK: knob position + the value Reason displays.

    ./.venv/bin/python reason_voice/prove_feedback.py

Needs, in order:
  1. remote/ files installed and Reason FULLY quit (Cmd+Q) and reopened.
  2. Reason > Preferences > Control Surfaces > ReasonVoice:
     MIDI Output set to "IAC Driver Bus 1"  <- NEW, this is the return path.
  3. The MClass Compressor Ctrl-clicked -> "Lock to ReasonVoice".

Why this matters: "turn the threshold down 5 percent" needs to know where the
knob is now, and "set attack to 30 ms" needs to know how a 0-127 dial position
maps to milliseconds. Reason's own displayed value answers both, so neither has
to be modelled or guessed.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reason_voice.reason_control import ReasonControl

r = ReasonControl(speak_feedback=False)
if r.port is None:
    sys.exit("No IAC MIDI output. Audio MIDI Setup > IAC Driver > Device is online.")
if r.inport is None:
    sys.exit("No IAC MIDI input, so nothing can come back. Same IAC bus, input side.")

r.poll()  # drop anything already queued
print("Setting Knob 5 (Attack) to three positions and reading Reason back.\n")

seen_any = False
for target in (10, 64, 120):
    r.set_value("knob_5", target)
    time.sleep(0.4)
    r.poll()
    got = r.current("knob_5")
    if got is None:
        print("  sent %3d -> nothing came back" % target)
        continue
    seen_any = True
    pos, name, shown = got
    print("  sent %3d -> Reason says %s = %-12s (position %d)"
          % (target, name or "?", shown or "?", pos))

print()
if not seen_any:
    print("NOTHING CAME BACK. In order of likelihood:")
    print("  1. The surface's MIDI OUTPUT is unassigned in Reason's")
    print("     Preferences > Control Surfaces. Set it to IAC Driver Bus 1.")
    print("  2. Reason wasn't fully quit (Cmd+Q) after the codec changed.")
    print("  3. The compressor isn't locked to ReasonVoice.")
    sys.exit(1)

print("Return path works. Now turn the Attack knob with your MOUSE in Reason.")
print("Watching for 10 seconds -- this is the part that proves it notices you,")
print("not just itself.\n")
before = r.current("knob_5")
deadline = time.time() + 10
while time.time() < deadline:
    r.poll()
    now = r.current("knob_5")
    if now and before and now[0] != before[0]:
        print("  saw you move it: %s = %s (position %d)" % (now[1], now[2], now[0]))
        before = now
    time.sleep(0.1)
print("\nDone.")
