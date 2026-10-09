"""Judge for the Hermes knob test (Scream 4 only).

Hermes picks the knob and the value and sends them. This script does NOT send
Hermes's moves. It only reads what Reason reports back and scores it.

Run from the Homeroom Studio folder, with Reason Voice running and Scream 4
Distortion locked to ReasonVoice in Reason:
    ./.venv/bin/python reason_voice/hermes_knob_test/judge.py start
    ./.venv/bin/python reason_voice/hermes_knob_test/judge.py before C1
    (Hermes runs C1 now)
    ./.venv/bin/python reason_voice/hermes_knob_test/judge.py after C1
    ... same before/after for each case ...
    ./.venv/bin/python reason_voice/hermes_knob_test/judge.py restore
"""
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import websockets

HERE = Path(__file__).resolve().parent
URL = "ws://localhost:8765/ws"
DEVICE = "Scream 4"
KNOBS = ["knob_%d" % n for n in range(1, 17)]
CASES = json.loads((HERE / os.environ.get("CASES_FILE", "cases.json")).read_text())
STATE_FILE = HERE / "state.json"
RESULTS = HERE / "results.md"
# The starting point the test sets, so every case has a known number to aim from.
BASELINE = {"knob_7": 127, "knob_8": 100, "knob_9": 127, "knob_11": 64, "knob_14": 127}
SETTLE = 1.0   # seconds to let Reason answer
SLOP = 2       # readback jitter allowed


async def read_panel(seconds=2.0):
    """Newest dial panel Reason Voice has sent. It ticks about 5 times a second."""
    latest = None
    async with websockets.connect(URL) as ws:
        end = time.time() + seconds
        while time.time() < end:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=0.5)
            except asyncio.TimeoutError:
                continue
            msg = json.loads(raw)
            if "dial" in msg:
                latest = msg["dial"]
    if not latest or not latest.get("locked"):
        sys.exit("Reason is not reporting. Lock Scream 4 to ReasonVoice first.")
    if DEVICE not in latest.get("device", ""):
        sys.exit("Locked device is '%s', not Scream 4. Lock the right one."
                 % latest.get("device"))
    pos = {k["knob"]: k["pos"] for k in latest["knobs"]}
    missing = [k for k in KNOBS if pos.get(k) is None]
    if missing:
        sys.exit("Reason has not reported: " + ", ".join(missing))
    return pos


async def set_knob(knob, value):
    async with websockets.connect(URL) as ws:
        await ws.send(json.dumps({"type": "command", "command": "dial_set",
                                  "args": {"knob": knob, "value": int(value)}}))
    await asyncio.sleep(0.3)


def load_state():
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}


def save_state(s):
    STATE_FILE.write_text(json.dumps(s, indent=2))


def add_result(line):
    if not RESULTS.exists():
        RESULTS.write_text("# Hermes knob test results (Scream 4)\n\n")
    with RESULTS.open("a") as f:
        f.write(line + "\n")


def case_by_id(cid):
    for c in CASES:
        if c["id"] == cid:
            return c
    sys.exit("No case %s. Known: %s" % (cid, ", ".join(c["id"] for c in CASES)))


async def cmd_start():
    pos = await read_panel()
    state = {"user_start": pos, "before": {}}
    save_state(state)
    print("Saved Scream 4's current positions. They go back at the end.")
    for knob, value in BASELINE.items():
        await set_knob(knob, value)
    await asyncio.sleep(SETTLE)
    now = await read_panel()
    bad = [k for k, v in BASELINE.items() if abs(now[k] - v) > SLOP]
    if bad:
        sys.exit("Readback does not match the baseline on " + ", ".join(bad)
                 + ". Stop: Reason is not answering the knob path. Nothing judged.")
    print("Baseline set and read back correctly: "
          + "  ".join("%s=%d" % (k, now[k]) for k in BASELINE))


async def cmd_before(cid):
    case_by_id(cid)
    pos = await read_panel()
    state = load_state()
    state.setdefault("before", {})[cid] = pos
    save_state(state)
    print("%s before: " % cid + "  ".join("%s=%d" % (k, pos[k]) for k in KNOBS))
    print("Now Hermes runs %s: \"%s\"" % (cid, case_by_id(cid)["prompt"]))


async def cmd_after(cid):
    case = case_by_id(cid)
    before = load_state().get("before", {}).get(cid)
    if before is None:
        sys.exit("Run 'before %s' first." % cid)
    now = await read_panel()
    changed = [k for k in KNOBS if abs(now[k] - before[k]) > SLOP]
    problems = []
    if case.get("no_change"):
        if changed:
            problems.append("moved " + ", ".join(changed) + " but nothing should move")
        detail = "no knob should move; moved: " + (", ".join(changed) or "none")
    else:
        if "rel" in case:
            r = case["rel"]
            target = r["knob"]
            want = before[target] + r["delta"]
            if abs(now[target] - want) > r["tol"]:
                problems.append("%s wanted about %d (+/-%d), got %d"
                                % (target, want, r["tol"], now[target]))
            detail = "%s %d -> %d (wanted about %d +/-%d)" % (
                target, before[target], now[target], want, r["tol"])
        else:
            target = case["knob"]
            if not (case["min"] <= now[target] <= case["max"]):
                problems.append("%s wanted %d to %d, got %d"
                                % (target, case["min"], case["max"], now[target]))
            detail = "%s %d -> %d (wanted %d to %d)" % (
                target, before[target], now[target], case["min"], case["max"])
        others = [k for k in changed if k != target]
        if others:
            problems.append("also moved " + ", ".join(others))
    verdict = "PASS" if not problems else "FAIL"
    text = detail + ("; " + "; ".join(problems) if problems else "")
    print("%s %s: %s" % (cid, verdict, text))
    print("By hand, from Hermes's transcript: (1) did it send dial_set itself, "
          "not the 'dial' or 'text' route? (2) for C8/C9, did it say '%s'? "
          "Write both into results.md." % case.get("expect_reply", "-"))
    add_result("- %s  %s  %s  | %s" % (datetime.now().strftime("%Y-%m-%d %H:%M"),
                                       cid, verdict, text))


async def cmd_status():
    pos = await read_panel()
    for k in KNOBS:
        print("%s = %d" % (k, pos[k]))


async def cmd_restore():
    start = load_state().get("user_start")
    if not start:
        sys.exit("No saved starting positions. Run 'start' first.")
    for k in KNOBS:
        await set_knob(k, start[k])
    await asyncio.sleep(SETTLE)
    now = await read_panel()
    off = [k for k in KNOBS if abs(now[k] - start[k]) > SLOP]
    print("Restored. " + ("NOT back on: " + ", ".join(off) if off
                          else "All 16 knobs back where they started."))


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    if cmd == "start":
        asyncio.run(cmd_start())
    elif cmd == "before" and len(args) == 2:
        asyncio.run(cmd_before(args[1]))
    elif cmd == "after" and len(args) == 2:
        asyncio.run(cmd_after(args[1]))
    elif cmd == "status":
        asyncio.run(cmd_status())
    elif cmd == "restore":
        asyncio.run(cmd_restore())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
