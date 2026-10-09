"""Typed Hermes knob test: no talking, no pasting.
Runs judge before -> hermes (fresh session, rules prepended) -> judge after, per case.
    ./.venv/bin/python reason_voice/hermes_knob_test/run_typed.py [C1 C2 ...]   (default: all)
Run `judge.py start` first and `judge.py restore` after.
"""
import json
import os
import subprocess
import time
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = str(HERE.parent.parent / ".venv/bin/python")
JUDGE = str(HERE / "judge.py")
RULES = HERE.joinpath("HERMES-PROMPT.md").read_text().split("\n---\n")[1].strip()
CASES = json.loads((HERE / os.environ.get("CASES_FILE", "cases.json")).read_text())


def judge(*a):
    r = subprocess.run([PY, JUDGE, *a], capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


want = sys.argv[1:] or [c["id"] for c in CASES]
for c in CASES:
    if c["id"] not in want:
        continue
    (HERE / ".set_done").unlink(missing_ok=True)
    if "start" in c:  # switch cases: put it in the opposite state first, so the move is real
        subprocess.run([PY, str(HERE / "send_move.py"), c["knob"], str(c["start"])], capture_output=True)
        time.sleep(1)
    print(judge("before", c["id"]).splitlines()[0][:60])
    reply = subprocess.run(
        ["hermes", "-p", "homeroom-studio", "-t", "terminal,file", "-z", RULES + "\n\nCase: " + c["prompt"]],
        capture_output=True, text=True, timeout=600).stdout.strip()
    print("  Hermes:", reply.replace("\n", " | ")[:200])
    if c.get("expect_reply") and not reply.lstrip("* ").startswith(("NOT POSSIBLE", "NO SUCH CONTROL", "NOT MOVABLE")):  # any plain refusal; exact word is not enforced (owner 2026-10-08)
        print("  WORDING FAIL: no plain refusal (command printed or no answer)")
        with open(HERE / "results.md", "a") as f:
            f.write("- %s WORDING FAIL: wanted %s\n" % (c["id"], c["expect_reply"]))
    print(" ", judge("after", c["id"]).splitlines()[0])
    with open(HERE / "results.md", "a") as f:
        f.write("- typed %s Hermes said: %s\n" % (c["id"], reply.replace("\n", " | ")[:200]))
