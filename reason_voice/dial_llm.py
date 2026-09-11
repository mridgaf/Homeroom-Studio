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
VALUE_NAMES = PROJECT_ROOT / "docs" / "reason" / "value_names.json"

# device name in the .remotemap  ->  device_refs file
DEVICE_REF_FILES = {"MClass Compressor": "mclass-compressor.md",
                    "Scream 4 Distortion": "scream-4.md",
                    "RV7000 Advanced Reverb": "rv7000-mkii.md",
                    "Kong Drum Designer": "kong.md",
                    "Redrum Drum Computer": "redrum.md",
                    "Dr.REX Loop Player": "dr-octo-rex.md"}

# The remotemap spells a control the way REASON does; a device guide spells it
# the way a person does. One entry so far: the RV7000's algorithm picker is
# "Soft Knob 1" to Reason and "Algorithm" to everyone else, and without the
# bridge the model is handed a name that means nothing.
NOTE_ALIASES = {"RV7000 Advanced Reverb": {"Soft Knob 1": "Algorithm",
                                           "EQ On/Off": "EQ button",
                                           "Gate On/Off": "GATE button"}}


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


def devices(remotemap=REMOTEMAP):
    """Every device with knob mappings, in remotemap order.

    Parsed, not listed -- adding a Scope block is all it takes to teach the
    app a new device.
    """
    out, current = [], None
    for line in remotemap.read_text().splitlines():
        if line.startswith("Scope"):
            parts = [p for p in line.split("\t") if p.strip()]
            current = parts[-1].strip() if parts else None
        elif current and line.startswith("Map"):
            parts = [p for p in line.split("\t") if p.strip()]
            if len(parts) >= 3 and parts[1].strip().startswith("Knob "):
                if current not in out:
                    out.append(current)
    return out


def device_for_param(param, remotemap=REMOTEMAP):
    """Which mapped device owns this parameter name? None if it is not unique.

    Reason names the parameter with every change it reports ("Damage Control"),
    so this is how the app knows what got locked without being told. A name
    that two devices share ("Enabled") returns None -- it never guesses.
    """
    if not param:
        return None
    hits = [d for d in devices(remotemap)
            if param in set(knob_map(d, remotemap).values())]
    return hits[0] if len(hits) == 1 else None


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
            # "**Attack**: ..." and "**Algorithm** (in the programmer): ..."
            m = re.match(r"\s*-\s*\*\*(.+?)\*\*[^:]*:\s*(.+)", line)
            if m:
                for key in m.group(1).split("/"):
                    notes[key.strip()] = m.group(2).strip()
    return notes


def note_for(notes, param, alias=None):
    """The guide's line for this parameter, allowing for how Reason spells it.

    Reason names a Kong knob "Drum 1 FX1 P1"; the guide has one bullet for
    "FX1". So: drop the pad prefix, then try shorter and shorter names until
    one matches. An alias (see NOTE_ALIASES) is tried first.
    """
    if alias and notes.get(alias):
        return notes[alias]
    tries = [param, re.sub(r"^Drum \d+ ", "", param)]
    words = tries[-1].split()
    while len(words) > 1:
        words = words[:-1]
        tries.append(" ".join(words))
    for name in tries:
        if notes.get(name):
            return notes[name]
        if notes.get(name.replace(" ", "-")):   # "Soft-knee"
            return notes[name.replace(" ", "-")]
    return ""


def named_choices(entry, limit=12):
    """["Tube", "Tape", "Fuzz", ...] for a picker, or None for a real knob.

    Damage Type and Body Type display words and letters, not numbers, so the
    model has to be TOLD what the settings are called or it cannot ask for one.
    Measured off Reason like everything else -- never a hardcoded list.
    """
    seen = []
    for _pos, shown in (entry or {}).get("table") or []:
        shown = (shown or "").strip()
        if shown and shown not in seen:
            seen.append(shown)
        if len(seen) > limit:
            return None
    if not seen or all(_num_unit(s)[0] is not None for s in seen):
        return None  # numeric: the unit lookup already handles it
    return seen


def build_prompt(phrase, device="MClass Compressor", calibration=None):
    knobs = knob_map(device)
    notes = control_notes(device)
    cal = (calibration if calibration is not None else load_calibration())
    by_knob = {e.get("knob"): e for e in (cal.get(device) or {}).values()}
    lines = []
    for knob in sorted(knobs, key=lambda k: int(k.split("_")[1])):
        param = knobs[knob]
        note = note_for(notes, param, NOTE_ALIASES.get(device, {}).get(param))
        cal_entry = by_knob.get(knob)
        choices = named_choices(cal_entry)
        if choices:
            # A volatile knob CAN still be named -- the RV7000's algorithm
            # picker is only the algorithm picker while Edit Mode says Reverb,
            # and the app puts it there before moving anything. What a volatile
            # knob still refuses is a real unit; see resolve().
            note = ((note + " " if note else "")
                    + "settings: " + ", ".join(choices))
        elif cal_entry is not None and cal_entry.get("volatile"):
            note = ((note + " " if note else "")
                    + "meaning depends on %s -- ask for a percentage"
                    % _depends_text(cal_entry["volatile"]))
        elif cal_entry:
            # The measured ends, so the model can't invent a unit. Without
            # this it answered "cut the lows" with "30 ms" on an EQ band.
            note = ((note + " " if note else "") + "range: %s .. %s"
                    % (cal_entry.get("min_display"),
                       cal_entry.get("max_display")))
        lines.append([knob, param, note])

    # Kong repeats three identical descriptions 16 times over, and a wall of
    # near-identical bullets is what made it answer "ring longer" with Level.
    # Say each description ONCE, then list the knobs bare.
    legend = []
    seen = {}
    for _, param, note in lines:
        if note:
            seen.setdefault(note, []).append(param)
    shared = {}
    for note, params in seen.items():
        # Only for numbered copies: "Drum 1 Level", "Drum 2 Level", ... all
        # strip to one label. Two UNRELATED knobs that happen to share a note
        # (the compressor's Input and Output Gain share a range line) have no
        # common name to hoist them under, so they stay inline.
        tails = {p.split(" ", 2)[2] for p in params if numbered_copy(p)}
        if len(params) > 1 and len(tails) == 1 and len(tails) == len(set(
                numbered_copy(p) is not None for p in params)):
            shared[note] = params
            legend.append("  %s -- %s" % (tails.pop(), note))
    body = "\n".join(
        "%s = %s%s" % (knob, param,
                       (" -- " + note) if note and note not in shared else "")
        for knob, param, note in lines)
    if legend:
        body = "What each control does:\n%s\n\n%s" % (
            "\n".join(sorted(set(legend))), body)
    lines = body
    return (
        "You control a %s in the DAW Reason. Available knobs:\n\n%s\n\n"
        "The producer said: \"%s\"\n\n"
        "Pick the ONE knob that best serves what they asked for, then say where "
        "to put it, using EXACTLY ONE of these four forms:\n"
        '  {"knob":"knob_N","target":"30 ms"}    <- they named a real value\n'
        '  {"knob":"knob_N","target":"Tape"}     <- one of that knob\'s settings\n'
        '  {"knob":"knob_N","target":"75%%"}      <- a position, no unit given\n'
        '  {"knob":"knob_N","delta":"-5%%"}       <- a nudge from where it is now\n'
        "Use `delta` whenever they said more/less/up/down/turn it X percent. "
        "Use `target` when they named a destination. "
        "For a knob that lists settings, `target` must be one of them, spelled "
        "exactly as listed. "
        'Answer with JSON only, plus "why": six words max.'
    ) % (device, lines, phrase)


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


def apply_value_names(cal, names_path=VALUE_NAMES):
    """Rewrite bare numbers in a measured table into what the panel says.

    Reason's Remote layer is not consistent about `text_value`. The MClass
    Compressor hands back "30 ms" and "-20.0 dB"; Scream 4 hands back "4"
    where its panel reads "Tape", and "2" where it reads "C". So for those
    devices the measured POSITIONS stay exactly as measured and only the label
    is filled in, from the Operation Manual -- see docs/reason/value_names.json.

    Nothing here invents a position. A parameter with no entry is untouched.
    """
    try:
        names = json.loads(names_path.read_text())["devices"]
    except (OSError, ValueError, KeyError):
        return cal
    for device, params in names.items():
        for param, labels in (params or {}).items():
            entry = (cal.get(device) or {}).get(param)
            if not entry or entry.get("named"):
                continue
            table = []
            for pos, shown in entry.get("table") or []:
                value, unit = _num_unit(shown)
                if value is not None and not unit and 0 <= int(value) < len(labels):
                    shown = labels[int(value)]
                table.append([pos, shown])
            entry["table"] = table
            entry["named"] = True
            entry["min_display"] = table[0][1] if table else ""
            entry["max_display"] = table[-1][1] if table else ""
    return cal


def load_calibration(path=CALIBRATION):
    if not path.exists():
        return {}
    try:
        return apply_value_names(json.loads(path.read_text()))
    except ValueError:
        return {}


def _depends_text(depends):
    """'Damage Type' or 'Edit Mode and Soft Knob 1' -- one dep or several."""
    if isinstance(depends, str):
        return depends
    depends = list(depends or [])
    if len(depends) < 2:
        return depends[0] if depends else ""
    return ", ".join(depends[:-1]) + " and " + depends[-1]


def _num_unit(s):
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*(.*)$", s or "")
    return (float(m.group(1)), m.group(2).strip()) if m else (None, "")


def resolve(answer, device, current_pos=None, calibration=None):
    """Turn {"target": "30 ms"} into a 0-127 position. (position, note) or None.

    Percentages are exact arithmetic. Real units (ms, dB) and named settings
    ("Tape", "C") are looked up in the calibration table measured from Reason
    itself -- never a modelled curve and never a hardcoded list, so a knob with
    an odd taper is as accurate as a linear one and a picker is as accurate as
    a knob.
    """
    knob = answer["knob"]
    cal = calibration if calibration is not None else load_calibration()
    entry = None
    for param, e in (cal.get(device) or {}).items():
        if e.get("knob") == knob:
            entry = e
            break

    # A knob whose meaning is set by something else (Scream 4's P1/P2 follow
    # Damage Type) has a table that is only true for one setting. Percentages
    # always work -- they are arithmetic on position, not a lookup.
    #
    # A NAMED setting is allowed only when the entry also carries `requires`,
    # i.e. the app can put the device into that context and READ BACK that it
    # got there (the RV7000's algorithm dial under Edit Mode = Reverb). Without
    # that there is nothing to verify: Kong's knobs follow whichever drum module
    # is loaded in the pad, and Reason does not report the module at all, so a
    # measured name there could be a leftover from a module he has since
    # swapped. Percentage only.
    #
    # A real unit is refused on every volatile knob, context or not: "30 ms" on
    # a dial that means something else entirely is a confidently wrong move.
    volatile = bool(entry is not None and entry.get("volatile"))
    unverifiable = bool(volatile and not (entry or {}).get("requires"))

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
        # Not a number: a named setting ("Tape", "C", "Off"). Match it against
        # what Reason actually displayed during the sweep, and land in the
        # MIDDLE of the run of positions holding it -- an edge position is one
        # rounding step away from the neighbouring setting.
        wanted = (answer.get("target") or "").strip().lower()
        if not wanted or entry is None or unverifiable:
            return None
        for match in (lambda s: s == wanted, lambda s: wanted in s):
            hits = [pos for pos, shown in entry["table"]
                    if match((shown or "").strip().lower())]
            if hits:
                return hits[len(hits) // 2], "measured: %s" % answer["target"]
        return None
    if unit in ("%", "percent"):
        return max(0, min(127, int(round(value * 127.0 / 100.0)))), "percent of travel"
    if entry is None or volatile:
        return None  # a real unit on an unmeasured -- or context-dependent -- knob
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


# Kong names every pad in the parameter itself -- "Drum 7 Level" -- and Reason
# never reports what is loaded on a pad. So "make the snare louder" has no
# answer: the model picks a pad anyway, confidently, and moves a drum he did
# not mean. Anything numbered like this needs the number said out loud.
_SPELLED = {w: i + 1 for i, w in enumerate(
    "one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen".split())}


def numbered_copy(param):
    """7 for "Drum 7 Level"; None for a parameter that names no copy."""
    m = re.match(r"^[A-Za-z]+ (\d+) ", param or "")
    return int(m.group(1)) if m else None


def copy_number(param, device=None):
    """Which of N interchangeable copies this parameter is, or None.

    Two spellings in the wild: Kong and Redrum put the number in the middle
    ("Drum 7 Level"), Dr. Octo Rex puts it at the end ("Select Loop 3").
    Both mean "one of several identical things" and both need the number
    spoken, or the model picks one.

    A name in NOTE_ALIASES is exempt from the trailing form: the alias exists
    precisely to say Reason's spelling is not the real identity. The RV7000's
    "Soft Knob 1" is the Algorithm picker, not copy 1 of anything, so asking
    for a plate must not be refused for want of saying "one".

    numbered_copy() is deliberately NOT widened to cover this -- build_prompt()
    relies on its prefix shape to split "Drum 7 Level" into copy and tail.
    """
    n = numbered_copy(param)
    if n is not None:
        return n
    if (NOTE_ALIASES.get(device or "", {}) or {}).get(param):
        return None
    m = re.match(r"^[A-Za-z][A-Za-z0-9 ]*? (\d+)$", param or "")
    return int(m.group(1)) if m else None


def said_the_number(phrase, n):
    """Did he actually say which one? Digits or the word, either way."""
    low = (phrase or "").lower()
    if re.search(r"\b%d\b" % n, low):
        return True
    return any(w in _SPELLED and _SPELLED[w] == n
               for w in re.findall(r"[a-z]+", low))


def choose(phrase, device="MClass Compressor", timeout=20, calibration=None):
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
        "messages": [{"role": "user",
                      "content": build_prompt(phrase, device, calibration)}],
    }).encode()
    req = urllib.request.Request(SERVER, data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            reply = json.load(r)["choices"][0]["message"]["content"]
    except (urllib.error.URLError, OSError, KeyError, IndexError, ValueError):
        return None  # server down or answered nonsense -- caller falls back
    move = _extract(reply, knobs)
    if move:
        n = copy_number(knobs.get(move["knob"], ""), device)
        if n is not None and not said_the_number(phrase, n):
            return None   # it guessed which pad -- refuse rather than move one
    return move


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

    # ---- two devices: the app must never guess which one is locked ----
    devs = devices()
    assert devs == ["Kong Drum Designer", "Redrum Drum Computer",
                    "Dr.REX Loop Player", "MClass Compressor",
                    "Scream 4 Distortion", "RV7000 Advanced Reverb"], devs
    kong = knob_map("Kong Drum Designer")
    assert len(kong) == 48 and kong["knob_1"] == "Drum 1 Level", kong
    assert kong["knob_48"] == "Drum 16 Decay Offset", kong
    assert device_for_param("Drum 16 Pitch Offset") == "Kong Drum Designer"
    assert device_for_param("Damage Control") == "Scream 4 Distortion"
    assert device_for_param("Attack") == "MClass Compressor"
    assert device_for_param("Enabled") is None      # on BOTH -- refuse to pick
    assert device_for_param("Nonsense") is None
    assert device_for_param("") is None
    scream = knob_map("Scream 4 Distortion")
    assert len(scream) == 16 and scream["knob_10"] == "Body Type", scream
    verb = knob_map("RV7000 Advanced Reverb")
    assert len(verb) == 16 and verb["knob_9"] == "Soft Knob 1", verb
    assert verb["knob_5"] == "Edit Mode", verb
    assert device_for_param("Decay") == "RV7000 Advanced Reverb"
    assert device_for_param("Enabled") is None      # now on THREE devices

    # ---- Redrum: 10 channels x 4, and the one name it shares with Kong ----
    rd = knob_map("Redrum Drum Computer")
    assert len(rd) == 40 and rd["knob_1"] == "Drum 1 Level", rd
    assert rd["knob_40"] == "Drum 10 Pan", rd
    assert device_for_param("Drum 3 Length") == "Redrum Drum Computer"
    assert device_for_param("Drum 3 Pan") == "Redrum Drum Computer"
    assert device_for_param("Drum 3 Decay Offset") == "Kong Drum Designer"
    # Kong and Redrum BOTH spell loudness "Drum N Level" on channels 1-10, so
    # a Level alone no longer says which is locked. It refuses instead.
    assert device_for_param("Drum 3 Level") is None
    assert device_for_param("Drum 13 Level") == "Kong Drum Designer"

    # ---- Dr. Octo Rex: Reason calls it Dr.REX, and it numbers its copies
    # ---- at the END of the name rather than the middle.
    rex = knob_map("Dr.REX Loop Player")
    assert len(rex) == 41 and rex["knob_1"] == "Select Loop 1", rex
    assert rex["knob_41"] == "LFO Sync Enable", rex
    assert device_for_param("Osc Env Amount") == "Dr.REX Loop Player"
    assert device_for_param("Selected Loop Slot") == "Dr.REX Loop Player"
    # Master Level is on Scream 4 already, so it is NOT mapped here on purpose.
    assert "Master Level" not in rex.values()
    assert device_for_param("Master Level") == "Scream 4 Distortion"
    # Nothing slice-level is remotable, so nothing slice-level is mapped.
    assert not [p for p in rex.values() if "Slice" in p], rex
    # "Select Loop 3" needs the 3 spoken; "Soft Knob 1" is the RV7000's
    # Algorithm picker and must NOT be held to that rule.
    assert copy_number("Select Loop 3", "Dr.REX Loop Player") == 3
    assert copy_number("Soft Knob 1", "RV7000 Advanced Reverb") is None
    assert copy_number("Selected Loop Slot", "Dr.REX Loop Player") is None

    # ---- named settings: a picker shows letters/words, not numbers ----
    # Body Type as a 5-way A-E picker, shaped like a real sweep would read.
    picker = {"Scream 4 Distortion": {"Body Type": {
        "knob": "knob_10", "unit": "",
        "table": [[p, "ABCDE"[min(4, p * 5 // 128)]] for p in range(128)]}}}
    assert named_choices(picker["Scream 4 Distortion"]["Body Type"]) == list("ABCDE")
    assert named_choices(fake["MClass Compressor"]["Attack"]) is None  # numeric
    assert named_choices({"table": []}) is None
    pos, note = resolve({"knob": "knob_10", "target": "C"},
                        "Scream 4 Distortion", calibration=picker)
    assert picker["Scream 4 Distortion"]["Body Type"]["table"][pos][1] == "C", pos
    assert pos == 64, pos                       # middle of C's run, not an edge
    pos, _ = resolve({"knob": "knob_10", "target": "e"},   # case-insensitive
                     "Scream 4 Distortion", calibration=picker)
    assert picker["Scream 4 Distortion"]["Body Type"]["table"][pos][1] == "E", pos
    assert resolve({"knob": "knob_10", "target": "Q"},
                   "Scream 4 Distortion", calibration=picker) is None
    assert "settings: A, B, C, D, E" in build_prompt(
        "body type c", "Scream 4 Distortion", calibration=picker)
    ranged = {"MClass Compressor": {"Attack": dict(
        fake["MClass Compressor"]["Attack"],
        min_display="1 ms", max_display="100 ms")}}
    assert "range: 1 ms .. 100 ms" in build_prompt(
        "more punch", calibration=ranged)

    # ---- a volatile knob is percentage-only, whatever its table says ----
    vol = {"Scream 4 Distortion": {"Parameter 1": {
        "knob": "knob_3", "unit": "ms", "volatile": "Damage Type",
        "table": [[p, "%d ms" % p] for p in range(128)]}}}
    assert resolve({"knob": "knob_3", "target": "30 ms"},
                   "Scream 4 Distortion", calibration=vol) is None
    pos, _ = resolve({"knob": "knob_3", "target": "50%"},
                     "Scream 4 Distortion", calibration=vol)
    assert pos == 64, pos
    assert "depends on Damage Type" in build_prompt(
        "more", "Scream 4 Distortion", calibration=vol)
    assert "depends on Edit Mode and Soft Knob 1" in build_prompt(
        "more", "RV7000 Advanced Reverb", calibration={
            "RV7000 Advanced Reverb": {"Soft Knob 2": dict(
                vol["Scream 4 Distortion"]["Parameter 1"], knob="knob_10",
                volatile=["Edit Mode", "Soft Knob 1"])}})

    # ---- a volatile knob that DISPLAYS NAMES can still be named ----
    # The RV7000's algorithm picker: meaning depends on Edit Mode, so a unit is
    # refused, but "plate" is exactly what the app can put the mode into first.
    algo = {"RV7000 Advanced Reverb": {"Soft Knob 1": {
        "knob": "knob_9", "unit": "", "volatile": "Edit Mode",
        "requires": {"Edit Mode": "Reverb"},
        "table": [[p, ["Small Space", "Room", "Hall", "Arena", "Plate",
                       "Spring", "Echo", "Multi Tap", "Reverse",
                       "Convolution"][min(9, p * 10 // 128)]]
                  for p in range(128)]}}}
    pos, _ = resolve({"knob": "knob_9", "target": "Plate"},
                     "RV7000 Advanced Reverb", calibration=algo)
    assert algo["RV7000 Advanced Reverb"]["Soft Knob 1"]["table"][pos][1] == "Plate"
    assert resolve({"knob": "knob_9", "target": "30 ms"},
                   "RV7000 Advanced Reverb", calibration=algo) is None
    assert "settings: Small Space, Room" in build_prompt(
        "give me a plate", "RV7000 Advanced Reverb", calibration=algo)
    assert "Algorithm" not in knob_map("RV7000 Advanced Reverb").values()
    assert "plate" in build_prompt("x", "RV7000 Advanced Reverb",
                                   calibration=algo).lower()

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
