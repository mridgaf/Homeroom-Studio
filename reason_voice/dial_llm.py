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
        "Pick the ONE knob that best serves what they asked for, and a MIDI "
        "value 0-127 for it (0 = fully left/minimum, 127 = fully right/maximum). "
        "Answer with JSON only, no explanation: "
        '{"knob": "knob_N", "value": N, "why": "six words max"}'
    ) % (device, "\n".join(lines), phrase)


def _extract(text, valid_knobs):
    """Pull the first valid {knob, value} object out of a model reply."""
    for blob in re.findall(r"\{[^{}]*\}", text):
        try:
            d = json.loads(blob)
        except ValueError:
            continue
        knob = d.get("knob")
        if knob not in valid_knobs:
            continue
        try:
            value = int(d.get("value"))
        except (TypeError, ValueError):
            continue
        if not 0 <= value <= 127:
            continue
        return knob, value, str(d.get("why", ""))[:60]
    return None


def choose(phrase, device="MClass Compressor", timeout=20):
    """(knob, value, why) or None if the model gave nothing usable."""
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
    import time

    # -- deterministic parts: these must hold with or without the server --
    km = knob_map()
    assert km["knob_5"] == "Attack", km
    assert km["knob_1"] == "Threshold", km
    assert len(km) == 8, km
    notes = control_notes()
    assert "Attack" in notes and "punch" in notes["Attack"].lower(), notes
    assert "Attack" in build_prompt("more punch")
    assert _extract('{"knob":"knob_5","value":96}', km) == ("knob_5", 96, "")
    assert _extract('{"knob":"knob_99","value":5}', km) is None      # bad knob
    assert _extract('{"knob":"knob_5","value":900}', km) is None     # out of range
    assert _extract("sorry, I can't help with that", km) is None     # no JSON
    print("parsing + validation: OK (8 knobs, %d control notes)" % len(notes))
    try:
        urllib.request.urlopen("http://127.0.0.1:8080/v1/models", timeout=5)
        print("local model server: reachable\n")
    except (urllib.error.URLError, OSError):
        print("local model server: NOT REACHABLE -- the four answers below "
              "will all be blank\n")

    # -- the judgment call: printed, for your ear/eye, not asserted --
    for phrase in ["give it more punch",
                   "turn down the threshold",
                   "squash it harder",
                   "back off the compression"]:
        t = time.time()
        got = choose(phrase)
        if got is None:
            print('  "%s" -> no usable answer' % phrase)
            continue
        knob, value, why = got
        print('  "%s"\n      -> %s = %s at %d/127%s   [%.1fs]'
              % (phrase, knob, km[knob], value,
                 ("  (%s)" % why) if why else "", time.time() - t))
