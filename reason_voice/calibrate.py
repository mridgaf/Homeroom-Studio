"""Measure what every knob position MEANS, by asking Reason.

    ./.venv/bin/python reason_voice/calibrate.py                     # all 8 knobs
    ./.venv/bin/python reason_voice/calibrate.py knob_5              # just one
    ./.venv/bin/python reason_voice/calibrate.py --device "MClass Compressor"

Sweeps each knob 0..127 and records the value Reason DISPLAYS at each position,
then writes docs/reason/calibration.json. That file is what lets "set attack to
30 ms" and "threshold to -20 dB" be exact instead of estimated.

Nothing here models a curve. Attack happens to be linear (measured), but Ratio
and Release are not assumed to be -- every position is read back from Reason.

Setup, same as reason_voice/prove_feedback.py:
  - surface MIDI input AND output both on IAC Driver Bus 1
  - the device Ctrl-clicked -> "Lock to ReasonVoice"

Your knobs are put back where they started when it finishes.
"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reason_voice.reason_control import ReasonControl

OUT = Path(__file__).resolve().parent.parent / "docs" / "reason" / "calibration.json"
SETTLE = 0.06  # seconds between setting a position and reading it back


def parse(shown):
    """'91 ms' -> (91.0, 'ms').  '-20.0 dB' -> (-20.0, 'dB').  'On' -> (None, '')."""
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*(.*)$", shown or "")
    if not m:
        return None, ""
    return float(m.group(1)), m.group(2).strip()


def sweep(r, knob):
    """[[position, 'displayed text'], ...] for 0..127, or (None, None) if silent.

    Reason only reports a parameter when it CHANGES. Two consequences, both of
    which bit the first version of this function:

    * Writing the value a control already holds produces no report. Soft Knee is
      a BUTTON that sits off, so writing position 0 first was silent and the
      whole knob was skipped as dead. Hence the seed below: drive it to the far
      end first, so the first real write is guaranteed to be a change.
    * Mid-sweep silence means "unchanged", not "no answer" -- a 2-state button
      reports twice across 128 positions and says nothing in between. So carry
      the last reading forward instead of bailing.
    """
    # seed: force at least one report regardless of where the control started
    r.set_value(knob, 127)
    time.sleep(SETTLE)
    r.poll()

    table, name, last = [], None, None
    for pos in range(128):
        r.set_value(knob, pos)
        time.sleep(SETTLE)
        r.poll()
        got = r.current(knob)
        if got is not None:
            _, name, last = got
        table.append([pos, last])
        if pos % 32 == 0:
            print("      %3d/127 %s = %s" % (pos, name or "?", last or "?"))
    if all(v is None for _, v in table):
        return None, None
    return name, table


def main():
    args = [a for a in sys.argv[1:]]
    device = "MClass Compressor"
    if "--device" in args:
        i = args.index("--device")
        device = args[i + 1]
        del args[i:i + 2]
    knobs = args or ["knob_%d" % k for k in range(1, 9)]

    r = ReasonControl(speak_feedback=False)
    if r.port is None or r.inport is None:
        sys.exit("Need IAC Driver Bus 1 on BOTH the input and output side.")
    r.poll()

    # remember where things were, so a calibration run doesn't rearrange his patch
    start = {}
    for knob in knobs:
        got = r.current(knob)
        if got:
            start[knob] = got[0]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(OUT.read_text()) if OUT.exists() else {}
    data.setdefault(device, {})

    for knob in knobs:
        print("   %s ..." % knob)
        name, table = sweep(r, knob)
        if table is None:
            print("      nothing came back -- skipped (is the device locked?)")
            continue
        lo, lo_unit = parse(table[0][1])
        hi, hi_unit = parse(table[-1][1])
        data[device][name or knob] = {
            "knob": knob,
            "unit": hi_unit or lo_unit,
            "min_display": table[0][1],
            "max_display": table[-1][1],
            "table": table,
        }
        span = ("%s .. %s" % (table[0][1], table[-1][1])) if lo is not None else "not numeric"
        print("      %s: %s" % (name or knob, span))

    for knob, pos in start.items():
        r.set_value(knob, pos)

    OUT.write_text(json.dumps(data, indent=1))
    print("\nWrote %s" % OUT)
    print("Knobs put back where they started.")


if __name__ == "__main__":
    main()
