"""Typed Hermes knob test: no talking, no pasting.
Runs judge before -> hermes (fresh session, rules prepended) -> judge after, per case.
    ./.venv/bin/python reason_voice/hermes_knob_test/run_typed.py [C1 C2 ...]   (default: all)
Run `judge.py start` first and `judge.py restore` after.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = str(HERE.parent.parent / ".venv/bin/python")
JUDGE = str(HERE / "judge.py")
RULES = HERE.joinpath("HERMES-PROMPT.md").read_text().split("\n---\n")[1].strip()
CASES = json.loads((HERE / "cases.json").read_text())


def judge(*a):
    r = subprocess.run([PY, JUDGE, *a], capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


want = sys.argv[1:] or [c["id"] for c in CASES]
for c in CASES:
    if c["id"] not in want:
        continue
    print(judge("before", c["id"]).splitlines()[0][:60])
    reply = subprocess.run(
        ["hermes", "-p", "homeroom-studio", "-t", "terminal,file", "-z", RULES + "\n\nCase: " + c["prompt"]],
        capture_output=True, text=True, timeout=600).stdout.strip()
    print("  Hermes:", reply.replace("\n", " | ")[:200])
    print(" ", judge("after", c["id"]).splitlines()[0])
    with open(HERE / "results.md", "a") as f:
        f.write("- typed %s Hermes said: %s\n" % (c["id"], reply.replace("\n", " | ")[:200]))
