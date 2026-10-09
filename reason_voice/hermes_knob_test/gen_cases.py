"""Build test cases from the Panel Map (part D). Writes cases_map.json.

    ./.venv/bin/python reason_voice/hermes_knob_test/gen_cases.py
Then: CASES_FILE=cases_map.json judge.py start / run_typed.py / judge.py restore

Every knob case has a start state (switches: the opposite; percents: 90%/10%).
Per movable control: one "set to X%" case using the panel label, one using
Reason's name. Switches get on/off. Plus not-movable controls (NOT POSSIBLE)
and made-up names (NO SUCH CONTROL). Same seed = same cases every run.
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAP = json.loads((HERE.parent.parent / "device_refs/_panel_map/scream-4.json").read_text())
FAKE = ["flux capacitor", "tape hiss", "chorus depth", "reverb size", "sidechain amount"]
SKIP = {"Enabled", "Damage Type", "Body Type"}  # 3-way / stepped; ponytail: add once their step values are mapped


def raw(p):
    return round(p * 127 / 100)


def main():
    rnd = random.Random(7)
    cases, n = [], 0

    def add(**c):
        nonlocal n
        n += 1
        cases.append(dict(id="M%02d" % n, **c))

    for c in MAP["controls"]:
        name, slot = c.get("reason_name"), c.get("knob_slot")
        if not slot or name in SKIP:
            continue
        knob = "knob_%d" % slot
        label = c["panel_label"].strip("()").lower()
        if name.endswith("On/Off"):
            base = name[:-7].lower()
            add(prompt="Turn the %s off." % base, knob=knob, min=0, max=31, start=127)
            add(prompt="Turn the %s on." % base, knob=knob, min=96, max=127, start=0)
            continue
        for said in sorted({label, name.lower()}):  # sorted: set order changes every run
            p = rnd.choice([10, 25, 40, 60, 75, 90])  # always steps of 5 (owner)
            add(prompt="Set the %s to %d percent." % (said, p), knob=knob,
                min=max(0, raw(p) - 3), max=min(127, raw(p) + 3),
                start=raw(90 if p < 50 else 10))  # far from the target, so the move is real
    for c in MAP["controls"]:
        if c.get("knob_slot") is None and c["side"] == "back" and "CV Input" in (c.get("reason_name") or ""):
            add(prompt="Turn the %s up to 50 percent." % c["reason_name"].lower(),
                no_change=True, expect_reply="NOT POSSIBLE")
    for f in FAKE:
        add(prompt="Set the %s to 50 percent." % f, no_change=True, expect_reply="NO SUCH CONTROL")
    add(prompt="Make a cable from the damage control CV input to the auto CV output.",
        no_change=True, expect_reply="NOT POSSIBLE")
    (HERE / "cases_map.json").write_text(json.dumps(cases, indent=1))
    print("%d cases -> cases_map.json" % len(cases))


if __name__ == "__main__":
    main()
