"""Turn an open-ended phrase into one knob move.

"give it more punch" -> ("knob_5", 96)   # Knob 5 = Attack on MClass Compressor

Falls to the local llama.cpp server (already running under launchd, see
DECISIONS 2026-09-10). The fast regex parser in intents.py stays primary --
this is only for phrasing it doesn't recognise.

Self-test:  ./.venv/bin/python reason_voice/dial_llm.py
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

SERVER = "http://127.0.0.1:8080/v1/chat/completions"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REMOTEMAP = PROJECT_ROOT / "remote" / "ReasonVoice.remotemap"
DEVICE_REFS = PROJECT_ROOT / "device_refs"
CALIBRATION = PROJECT_ROOT / "docs" / "reason" / "calibration.json"

# device name in the .remotemap  ->  device_refs file
DEVICE_REF_FILES = {"MClass Compressor": "mclass-compressor.md"}


def knob_map(device="MClass Compressor", remotemap=REMOTEMAP):
    """{"knob_5": "Attack", ...} read from the remotemap Reason itself uses.

    Parsed, not hardcoded -- so the map and this file can never disagree.
    """
    out = {}
    in_scope = False
    for line in remotemap.read_text().splitlines():
        if line.startswith("Scope"):
            in_scope = line.rstrip().endswith(device)
            continue
        if in_scope and line.startswith("Map"):
            parts = [p for p in line.split("\t") if p.strip()]
            if len(parts) >= 3 and parts[1].strip().startswith("Knob "):
                n = parts[1].strip().split()[1]
                out["knob_%s" % n] = parts[2].strip()
    return out


def control_notes(device="MClass Compressor"):
    """{"Attack": "THE character control. Slow lets transients punch..."}

    From the "## Key controls" bullets of the device_refs entry. Without these
    the model only sees knob names and guesses badly -- asked for "more punch"
    with names alone it answered "Threshold down".
    """
    fname = DEVICE_REF_FILES.get(device)
    if not fname:
        return {}
    path = DEVICE_REFS / fname
    if not path.exists():
        return {}
    notes = {}
    in_section = False
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            in_section = line.strip().lower() == "## key controls"
            continue
        if in_section:
            m = re.match(r"\s*-\s*\*\*(.+?)\*\*:\s*(.+)", line)
            if m:
                notes[m.group(1).strip()] = m.group(2).strip()
    return notes


def build_prompt(phrase, device="MClass Compressor"):
    knobs = knob_map(device)
    notes = control_notes(device)
    lines = []
    for knob in sorted(knobs, key=lambda k: int(k.split("_")[1])):
        param = knobs[knob]
        # notes keys don't always match the remotemap spelling ("Soft-knee")
        note = notes.get(param) or notes.get(param.replace(" ", "-")) or ""
        lines.append("%s = %s%s" % (knob, param, (" -- " + note) if note else ""))
    return (
        "You control a %s in the DAW Reason. Available knobs:\n\n%s\n\n"
        "The producer said: \"%s\"\n\n"
        "Pick the ONE knob that best serves what they asked for, then say where "
        "to put it, using EXACTLY ONE of these three forms:\n"
        '  {"knob":"knob_N","target":"30 ms"}    <- they named a real value\n'
        '  {"knob":"knob_N","target":"75%%"}      <- a position, no unit given\n'
        '  {"knob":"knob_N","delta":"-5%%"}       <- a nudge from where it is now\n'
        "Use `delta` whenever they said more/less/up/down/turn it X percent. "
        "Use `target` when they named a destination. "
        'Answer with JSON only, plus "why": six words max.'
    ) % (device, "\n".join(lines), phrase)


def _extract(text, valid_knobs):
    """First usable {knob, target|delta} object in a model reply."""
    for blob in re.findall(r"\{[^{}]*\}", text):
        try:
            d = json.loads(blob)
        except ValueError:
            continue
        if d.get("knob") not in valid_knobs:
            continue
        target, delta = d.get("target"), d.get("delta")
        if not isinstance(target, str) and not isinstance(delta, str):
            continue
        if target and delta:
            continue  # ambiguous: it must pick one
        return {"knob": d["knob"], "target": target, "delta": delta,
                "why": str(d.get("why", ""))[:60]}
    return None


def load_calibration(path=CALIBRATION):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except ValueError:
        return {}


def _num_unit(s):
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*(.*)$", s or "")
    return (float(m.group(1)), m.group(2).strip()) if m else (None, "")


def resolve(answer, device, current_pos=None, calibration=None):
    """Turn {"target": "30 ms"} into a 0-127 position. (position, note) or None.

    Percentages are exact arithmetic. Real units (ms, dB) are looked up in the
    calibration table measured from Reason itself -- never a modelled curve, so
    a knob with an odd taper is as accurate as a linear one.
    """
    knob = answer["knob"]
    cal = calibration if calibration is not None else load_calibration()
    entry = None
    for param, e in (cal.get(device) or {}).items():
        if e.get("knob") == knob:
            entry = e
            break

    if answer.get("delta"):
        amount, unit = _num_unit(answer["delta"])
        if amount is None or unit not in ("%", "percent"):
            return None  # only percentage nudges for now
        if current_pos is None:
            return None
        pos = current_pos + amount * 127.0 / 100.0
        return max(0, min(127, int(round(pos)))), "nudged from %d" % current_pos

    value, unit = _num_unit(answer.get("target"))
    if value is None:
        return None
    if unit in ("%", "percent"):
        return max(0, min(127, int(round(value * 127.0 / 100.0)))), "percent of travel"
    if entry is None:
        return None  # a real unit was asked for and we have not measured this knob
    best, best_gap = None, None
    for pos, shown in entry["table"]:
        got, got_unit = _num_unit(shown)
        if got is None or got_unit.lower() != unit.lower():
            continue
        gap = abs(got - value)
        if best_gap is None or gap < best_gap:
            best, best_gap = (pos, shown), gap
    if best is None:
        return None
    return best[0], "measured: %s" % best[1]


def choose(phrase, device="MClass Compressor", timeout=20):
    """{"knob","target","delta","why"} or None if the model gave nothing usable."""
    knobs = knob_map(device)
    if not knobs:
        return None
    body = json.dumps({
        "model": "local",
        "temperature": 0,
        "max_tokens": 120,
        # Qwen3.5 is a reasoning model: left alone it spends every token in
        # `reasoning_content` and returns an EMPTY `content`. Measured, not
        # guessed -- `reasoning_budget: 0` does NOT work, this does.
        "chat_template_kwargs": {"enable_thinking": False},
        "messages": [{"role": "user", "content": build_prompt(phrase, device)}],
    }).encode()
    req = urllib.request.Request(SERVER, data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            reply = json.load(r)["choices"][0]["message"]["content"]
    except (urllib.error.URLError, OSError, KeyError, IndexError, ValueError):
        return None  # server down or answered nonsense -- caller falls back
    return _extract(reply, knobs)


if __name__ == "__main__":
    import math
    import time

    # ---- deterministic: must hold with or without the model server ----
    km = knob_map()
    assert km["knob_5"] == "Attack" and km["knob_1"] == "Threshold", km
    assert len(km) == 8, km
    notes = control_notes()
    assert "Attack" in notes and "punch" in notes["Attack"].lower(), notes
    assert "Attack" in build_prompt("more punch")

    assert _extract('{"knob":"knob_5","target":"30 ms"}', km)["target"] == "30 ms"
    assert _extract('{"knob":"knob_1","delta":"-5%"}', km)["delta"] == "-5%"
    assert _extract('{"knob":"knob_99","target":"1 ms"}', km) is None   # bad knob
    assert _extract('{"knob":"knob_5","value":96}', km) is None         # old shape
    assert _extract('{"knob":"knob_5","target":"1 ms","delta":"-5%"}', km) is None
    assert _extract("sorry, I can't help", km) is None                  # no JSON

    # Attack, as MEASURED off Reason on 2026-09-10: ms = floor(1 + pos*99/127),
    # exact on all 33 observed points. Used here only to exercise resolve().
    fake = {"MClass Compressor": {"Attack": {
        "knob": "knob_5", "unit": "ms",
        "table": [[p, "%d ms" % math.floor(1 + p * 99 / 127)] for p in range(128)]}}}

    pos, note = resolve({"knob": "knob_5", "target": "30 ms"},
                        "MClass Compressor", calibration=fake)
    assert fake["MClass Compressor"]["Attack"]["table"][pos][1] == "30 ms", (pos, note)
    pos, _ = resolve({"knob": "knob_5", "target": "100 ms"},
                     "MClass Compressor", calibration=fake)
    assert pos == 127, pos
    pos, _ = resolve({"knob": "knob_5", "target": "50%"},
                     "MClass Compressor", calibration=fake)
    assert pos == 64, pos
    pos, _ = resolve({"knob": "knob_5", "delta": "-5%"}, "MClass Compressor",
                     current_pos=100, calibration=fake)
    assert pos == 94, pos                      # 100 - 6.35 -> 94
    assert resolve({"knob": "knob_5", "delta": "-5%"}, "MClass Compressor",
                   calibration=fake) is None   # a nudge with no current position
    assert resolve({"knob": "knob_1", "target": "-20 dB"}, "MClass Compressor",
                   calibration=fake) is None   # Threshold not measured yet
    print("parsing, validation and unit lookup: OK (%d knobs, %d control notes)"
          % (len(km), len(notes)))

    real = load_calibration()
    measured = sorted((real.get("MClass Compressor") or {}))
    print("calibration on disk: %s"
          % (", ".join(measured) if measured else "NONE -- run reason_voice/calibrate.py"))
    try:
        urllib.request.urlopen("http://127.0.0.1:8080/v1/models", timeout=5)
        print("local model server: reachable\n")
    except (urllib.error.URLError, OSError):
        print("local model server: NOT REACHABLE\n")

    # ---- the judgment call: printed for your eye, not asserted ----
    for phrase in ["give it more punch",
                   "set the attack to 30 milliseconds",
                   "turn the threshold down five percent",
                   "squash it harder",
                   "back off the compression"]:
        t = time.time()
        ans = choose(phrase)
        if ans is None:
            print('  "%s" -> no usable answer' % phrase)
            continue
        asked = ans["target"] or ans["delta"]
        got = resolve(ans, "MClass Compressor", current_pos=64)
        where = ("position %d (%s)" % got) if got else "CANNOT RESOLVE (not calibrated)"
        print('  "%s"\n      -> %s = %s  ->  %s   [%.1fs]'
              % (phrase, km[ans["knob"]], asked, where, time.time() - t))
