"""Measure what every knob position MEANS, by asking Reason.

    ./.venv/bin/python reason_voice/calibrate.py                     # every knob
    ./.venv/bin/python reason_voice/calibrate.py knob_5              # just one
    ./.venv/bin/python reason_voice/calibrate.py --device "Scream 4 Distortion"
    ./.venv/bin/python reason_voice/calibrate.py --device "RV7000 Advanced Reverb"

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

from reason_voice import dial_llm
from reason_voice.reason_control import ReasonControl

OUT = Path(__file__).resolve().parent.parent / "docs" / "reason" / "calibration.json"
SETTLE = 0.06  # seconds between setting a position and reading it back

# Knobs whose MEANING is set by another knob, so a measured table is only true
# for whatever that other knob was showing at the time. Scream 4's P1/P2 are
# compression+speed under Tape and something else entirely under Digital.
# These stay percentage-only -- see resolve() in dial_llm.py.
# Contexts Reason does not expose as a parameter at all. Named here so the
# prompt can say WHY a knob is percentage-only instead of just refusing.

VOLATILE = {"Scream 4 Distortion": {"Parameter 1": "Damage Type",
                                    "Parameter 2": "Damage Type"},
            # The RV7000's eight programmer dials are whatever the current edit
            # page says they are; dials 2-8 also change with the algorithm that
            # dial 1 selects. Dial 1 in Reverb mode IS the algorithm picker.
            # Kong has no entry on purpose. Its DM and FX knobs ARE volatile --
            # they scale whatever drum module or effect is in the pad, which
            # Reason never reports -- but the remotemap trades that depth for
            # reach: 16 pads x Level/Pitch/Decay, and those three mean the same
            # thing under every module. Re-add this block if a pad ever goes
            # deep again.
            "RV7000 Advanced Reverb": dict(
                {"Soft Knob 1": "Edit Mode"},
                **{"Soft Knob %d" % n: ["Edit Mode", "Soft Knob 1"]
                   for n in range(2, 9)}),
            # Dr. Octo Rex's LFO Amount is however much of whatever LFO1 Dest
            # is pointed at -- pitch wobble and pan wobble are not the same
            # units. Dest IS a mapped knob, so this is reachable, but there is
            # no one correct setting to drive it to the way the RV7000 has
            # "Reverb" -- so no REQUIRES entry, and it stays percentage-only.
            # Loop Transpose and Loop Level are deliberately NOT here: they
            # act on whichever slot is selected, but semitones are semitones
            # in every slot. The TARGET moves, the MEANING doesn't. That
            # caveat lives in the device guide, not in a refusal.
            "Dr.REX Loop Player": {"LFO1 Amount": "LFO1 Dest"}}

# The context a knob has to be measured in for its table to mean anything, and
# that the app puts the device into before moving it. Without this the sweep
# records whatever page happened to be showing and every later lookup is wrong.
REQUIRES = {"RV7000 Advanced Reverb": {"Soft Knob %d" % n: {"Edit Mode": "Reverb"}
                                       for n in range(1, 9)}}


def parse(shown):
    """'91 ms' -> (91.0, 'ms').  '-20.0 dB' -> (-20.0, 'dB').  'On' -> (None, '')."""
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*(.*)$", shown or "")
    if not m:
        return None, ""
    return float(m.group(1)), m.group(2).strip()


def probe(r, knob, samples=4):
    """"absolute" or "toggle" -- does writing a value SET this control or FLIP it?

    Runs BEFORE the sweep for every knob. A button that flips on every message
    would otherwise be flipped 128 times and "put it back where it started"
    would mean nothing.

    Writes the SAME value repeatedly and counts how often the reading changes.
    An absolute control never changes; a flip-flop alternates every time. The
    first version compared a single pair, and a single dropped report was enough
    to invert the verdict -- which happened twice on 2026-09-11, in both
    directions: Kong's Drum 2 Level, a normal 0-127 knob, was called a toggle,
    and Alligator's Gate 1 Open, a real button, was called absolute and then
    flipped 128 times while its two identical siblings were correctly spared.

    Ties break toward "toggle" on purpose. The two mistakes are not equal: a
    knob wrongly called a toggle loses its table and falls back to percentages,
    which still work. A toggle wrongly called a knob gets hammered 128 times and
    records noise -- it damages his patch AND the calibration.
    """
    seen = []
    r.set_value(knob, 0)          # seed: guarantee the next write is a change
    time.sleep(SETTLE)
    r.poll()
    for _ in range(samples):
        r.set_value(knob, 127)
        time.sleep(SETTLE)
        r.poll()
        got = r.current(knob)
        seen.append(got[2] if got else None)
    changes = sum(1 for a, b in zip(seen, seen[1:]) if a != b)
    if changes == 0:
        return "absolute"
    if changes >= 2:
        return "toggle"
    # Exactly one change across four identical writes is the signature of a
    # dropped report, not of either kind of control. Ask once more.
    return probe(r, knob, samples + 1) if samples == 4 else "toggle"


def put(r, data, device, param, wanted):
    """Move `param` to the setting called `wanted`, and CHECK it got there.

    Returns True only if Reason reports that setting back. Used to reach Reverb
    mode before measuring the programmer dials -- a table measured on the wrong
    page is worse than no table.
    """
    entry = (data.get(device) or {}).get(param)
    if not entry:
        return False
    named = dial_llm.apply_value_names({device: {param: json.loads(json.dumps(entry))}})
    placed = dial_llm.resolve({"knob": entry["knob"], "target": wanted},
                              device, calibration=named)
    if placed is None:
        return False
    r.set_value(entry["knob"], placed[0])
    time.sleep(SETTLE)
    r.poll()
    got = r.current(entry["knob"])
    # Reason's own words win when it gives words; the table's labels came from
    # the manual, so they are the fallback, not the authority.
    shown = ((got[2] if got else "") or "").strip()
    if not shown or shown.lstrip("-").replace(".", "", 1).isdigit():
        table = (named.get(device) or {}).get(param, {}).get("table") or []
        if got and 0 <= got[0] < len(table):
            shown = str(table[got[0]][1])
    return wanted.strip().lower() in shown.strip().lower()


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


def lost_readings(table):
    """Positions where Reason's report went missing, or [] if the sweep was clean.

    sweep() carries the last reading forward when Reason says nothing, because
    mid-sweep silence normally means "unchanged" -- a 2-state button reports
    twice across 128 positions and is silent in between. A report DROPPED by a
    MIDI buffer overflow looks exactly the same from here, and lands in the
    table as a stale value wearing the clothes of a measurement. Measured on
    Kong 2026-09-11: Reason warned about the overflow, and positions 21-25 of
    Drum 2 Level all recorded "20" while the knob was really moving. The same
    overflow made probe() call that knob a toggle.

    Told apart by SHAPE, not by guessing what kind of control it is: a picker's
    runs are all about equal (ten reverb algorithms, ~13 positions each), and a
    switch's are huge but even. A drop is ONE long run against short ones.
    """
    vals = [v for _, v in table]
    runs, start = [], 0
    for i in range(1, len(vals) + 1):
        if i == len(vals) or vals[i] != vals[start]:
            runs.append((i - start, start))
            start = i
    # Upper median on purpose: on an even count it takes the LONGER of the two
    # middle runs, which makes the test harder to trip, not easier. A detector
    # that cries wolf gets ignored, and then it may as well not exist.
    lengths = sorted(n for n, _ in runs)
    median = lengths[len(lengths) // 2]
    return [(n, at) for n, at in runs if n >= 3 and n >= 3 * median]


def main():
    args = [a for a in sys.argv[1:]]
    device = "MClass Compressor"
    if "--device" in args:
        i = args.index("--device")
        device = args[i + 1]
        del args[i:i + 2]
    # Which knobs this device has comes from the remotemap Reason itself
    # reads -- 8 on the compressor, 16 on a Scream 4.
    mapped = dial_llm.knob_map(device)
    if not mapped:
        sys.exit('No Scope block for "%s" in remote/ReasonVoice.remotemap.' % device)
    knobs = args or sorted(mapped, key=lambda k: int(k.split("_")[1]))

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

    skipped_context, lossy = [], []
    for knob in knobs:
        print("   %s ..." % knob)
        param_name = mapped.get(knob, "")
        needs = REQUIRES.get(device, {}).get(param_name) or {}
        ready = True
        for other, wanted in needs.items():
            if not put(r, data, device, other, wanted):
                ready = False
                print("      needs %s = %s and could not get there -- SKIPPED."
                      % (other, wanted))
                skipped_context.append("%s (%s)" % (knob, param_name))
        if not ready:
            continue
        kind = probe(r, knob)
        if kind == "toggle":
            # Every write flips it, so 128 of them would be vandalism and the
            # positions would mean nothing. Record what it is and leave it.
            data[device][param_name or knob] = {"knob": knob, "unit": "",
                                                "toggle": True}
            print("      FLIPS on every write (a toggle) -- not swept. "
                  "Check this control on the panel; it may have moved.")
            continue
        name, table = sweep(r, knob)
        if table is None:
            print("      nothing came back -- skipped (is the device locked?)")
            continue

        # Reason names the parameter in every report, and that name is the only
        # proof that the device we are WRITING to is the device that is LOCKED.
        # Without this check the run looks perfect and measures the wrong rack
        # unit: on 2026-09-11 a Redrum sweep ran with Kong still locked, and all
        # 40 knobs came back as Kong parameters -- correct-looking numbers filed
        # under the wrong device. Caught on the first knob, so one knob is
        # disturbed instead of forty.
        expected = mapped.get(knob, "")
        if name and expected and name != expected:
            for other, pos in start.items():
                r.set_value(other, pos)
            sys.exit(
                '\n   WRONG DEVICE -- nothing was saved.\n'
                '   Sweeping %r, whose map calls %s %r,\n'
                '   but Reason reported %r.\n\n'
                '   Something else is Ctrl-click -> "Lock to ReasonVoice".\n'
                '   Lock the right device and run this again.'
                % (device, knob, expected, name))
        lo, lo_unit = parse(table[0][1])
        hi, hi_unit = parse(table[-1][1])
        entry = {
            "knob": knob,
            "unit": hi_unit or lo_unit,
            "min_display": table[0][1],
            "max_display": table[-1][1],
            "table": table,
        }
        depends = VOLATILE.get(device, {}).get(name or mapped.get(knob, ""))
        if depends:
            entry["volatile"] = depends
        needed = REQUIRES.get(device, {}).get(name or mapped.get(knob, ""))
        if needed:
            # What the app must put the device into before it moves this knob.
            entry["requires"] = needed
        lost = lost_readings(table)
        if lost:
            entry["lossy"] = [[at, n] for n, at in lost]
            lossy.append("%s (%s)" % (knob, name or param_name))
        data[device][name or knob] = entry
        span = ("%s .. %s" % (table[0][1], table[-1][1])) if lo is not None else "not numeric"
        print("      %s: %s" % (name or knob, span))
        for n, at in lost:
            print("      %d READINGS LOST at positions %d-%d -- Reason's reports "
                  "did not keep up." % (n - 1, at + 1, at + n - 1))

    # A volatile knob's table is only true for the setting that was live.
    # Record it, read out of the table we just measured for that other knob.
    for param, entry in data[device].items():
        depends = entry.get("volatile")
        if not depends:
            continue
        entry["measured_with"] = {}
        for dep in ([depends] if isinstance(depends, str) else depends):
            other = data[device].get(dep) or {}
            pos = start.get(other.get("knob"))
            table = other.get("table") or []
            entry["measured_with"][dep] = (
                table[pos][1] if (pos is not None and pos < len(table))
                # a dependency that is not a mapped parameter (Kong's loaded
                # module) can never be read -- say so rather than "unknown"
                else "unknown" if other else "not reported by Reason")
            print("   note: %s was measured with %s = %s"
                  % (param, dep, entry["measured_with"][dep]))

    for knob, pos in start.items():
        r.set_value(knob, pos)

    if lossy:
        print("\n   THIS SWEEP LOST DATA. Re-run just these knobs, one command:")
        print("      ./.venv/bin/python reason_voice/calibrate.py --device %r %s"
              % (device, " ".join(k.split(" ")[0] for k in lossy)))
        print("   Cause is a MIDI buffer overflow -- Reason says so in its own")
        print("   window. Quitting other audio apps helps; re-running a handful")
        print("   of knobs on a quiet bus usually comes back clean.")

    if skipped_context:
        print("\n   Not measured, because the device could not be put in the "
              "right mode first:\n      %s" % ", ".join(skipped_context))
        print("   Look at what Edit Mode reported above. If it came back as "
              "bare numbers,\n   add them to docs/reason/value_names.json and "
              "run this again.")

    OUT.write_text(json.dumps(data, indent=1))
    print("\nWrote %s" % OUT)
    print("Knobs put back where they started.")


if __name__ == "__main__":
    main()
