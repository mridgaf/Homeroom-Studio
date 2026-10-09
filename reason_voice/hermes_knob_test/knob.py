"""Hermes's only tool for Scream 4 knobs: find -> read -> set.

    ./.venv/bin/python reason_voice/hermes_knob_test/knob.py find "high cut"
    ./.venv/bin/python reason_voice/hermes_knob_test/knob.py read knob_7
    ./.venv/bin/python reason_voice/hermes_knob_test/knob.py set knob_7 25%
    ./.venv/bin/python reason_voice/hermes_knob_test/knob.py set "high cut" 25%
    (set also takes: on, off. read/set take knob_N or a control name.)

find searches the Panel Map (device_refs/_panel_map/scream-4.json).
read/set use the value Reason reports back. Percent = percent of a full turn
(0% = 0, 100% = 127). Only ONE set is allowed per case (run_typed.py clears it).
"""
import asyncio
import json
import re
import sys
from pathlib import Path

import judge

HERE = Path(__file__).resolve().parent
MAP = json.loads((HERE.parent.parent / "device_refs/_panel_map/scream-4.json").read_text())
SET_LOCK = HERE / ".set_done"
# Words people say -> words on the panel. ponytail: hand list, grow it from failures.
ALIAS = {"high": "hi", "low": "lo", "middle": "mid", "volume": "level",
         "output": "master", "size": "scale", "resonance": "reso",
         "distortion": "damage", "drive": "damage", "bypass": "enabled"}
STOP = {"the", "a", "an", "knob", "control", "slider", "button", "switch", "of"}


def words(text):
    out = set()
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if w not in STOP:
            out.add(ALIAS.get(w, w))
    return out


def find_hits(query):
    q = words(query)
    hits = []
    for c in MAP["controls"]:
        hay = words(" ".join(str(c.get(k) or "") for k in ("panel_label", "reason_name", "what")))
        if q and q <= hay:
            hits.append(c)
    hits.sort(key=lambda c: (not c.get("knob_slot"), words(c.get("reason_name") or "") != q))
    return hits


def find(query):
    hits = find_hits(query)
    if not hits:
        return ["NO SUCH CONTROL: nothing on Scream 4 matches '%s'" % query]
    lines = []
    for c in hits:
        if c.get("knob_slot"):
            lines.append("%s  %s  knob_%d  (%s)" % (c["code"], c["reason_name"], c["knob_slot"], c["what"]))
        else:
            lines.append("%s  %s  NOT MOVABLE by knob (%s)" % (c["code"], c.get("reason_name") or c["panel_label"], c["what"]))
    return lines


def name_of(knob):
    n = int(knob[5:])
    for c in MAP["controls"]:
        if c.get("knob_slot") == n:
            return c["reason_name"]
    return knob


def pct(v):
    return "%d%%" % round(v * 100 / 127)


def parse_value(s):
    s = s.strip().lower()
    if s == "on":
        return 127
    if s == "off":
        return 0
    m = re.fullmatch(r"(\d+(?:\.\d+)?)%", s)
    if not m or not 0 <= float(m.group(1)) <= 100:
        sys.exit("value must be 0%..100%, on, or off")
    return round(float(m.group(1)) * 127 / 100)


def resolve(arg, value=""):
    """knob_N or a control name -> knob_N. Refuses instead of guessing."""
    if re.fullmatch(r"knob_\d+", arg):
        if not 1 <= int(arg[5:]) <= 16:
            sys.exit("knob must be knob_1 to knob_16")
        return arg
    hits = find_hits(arg)
    if not hits:
        sys.exit("NO SUCH CONTROL: nothing on Scream 4 matches '%s'" % arg)
    best = hits[0]
    if not best.get("knob_slot"):
        sys.exit("NOT MOVABLE by knob: %s (%s)" % (best.get("reason_name") or best["panel_label"], best["what"]))
    movable = [c for c in hits if c.get("knob_slot")]
    q = words(arg)
    exact = [c for c in movable if words(c["reason_name"]) == q]
    switches = [c for c in movable if c["reason_name"].endswith("On/Off")]
    if value.strip().lower() in ("on", "off") and len(switches) == 1:
        best = switches[0]  # "body" + on/off can only mean the switch
    elif len(exact) == 1:
        best = exact[0]
    elif len(movable) > 1:
        sys.exit("AMBIGUOUS '%s', say which: " % arg + "; ".join(
            "%s (knob_%d)" % (c["reason_name"], c["knob_slot"]) for c in movable))
    return "knob_%d" % best["knob_slot"]


async def read(knob):
    v = (await judge.read_panel())[knob]
    print("%s %s = %s" % (knob, name_of(knob), pct(v)))


async def set_(knob, raw):
    if SET_LOCK.exists():
        sys.exit("REFUSED: one move per case, already sent: " + SET_LOCK.read_text())
    target = parse_value(raw)
    before = (await judge.read_panel())[knob]
    await judge.set_knob(knob, target)
    await asyncio.sleep(judge.SETTLE)
    after = (await judge.read_panel())[knob]
    SET_LOCK.write_text("%s %s" % (knob, raw))
    ok = abs(after - target) <= judge.SLOP
    print("%s (%s): %s -> %s (checked: %s)%s" % (name_of(knob), knob, pct(before), pct(target), pct(after),
                                            "" if ok else "  DID NOT LAND"))


def main():
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "find":
        print("\n".join(find(a[1])))
    elif len(a) == 2 and a[0] == "read":
        asyncio.run(read(resolve(a[1])))
    elif len(a) == 3 and a[0] == "set":
        parse_value(a[2])  # bad value exits before anything is sent
        asyncio.run(set_(resolve(a[1], a[2]), a[2]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
