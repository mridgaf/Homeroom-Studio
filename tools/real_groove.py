"""Real-drummer feel (Plan A, owner 2026-10-31).

Reads the Groove MIDI Dataset (Google Magenta, CC BY 4.0: ten drummers on
an electronic kit, recorded to a click) and boils every style/drummer down
to a 16-step template per drum: how early/late a real player hits each step
(as a fraction of a 16th, so it holds at any tempo) and how hard.

    .venv/bin/python tools/real_groove.py          # rebuild groove_templates.json

The JSON is small and lives in the project; the dataset stays on the drive.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

GMD = Path("/Volumes/TBOTC 3/Datasets/Groove MIDI/groove")
OUT = Path(__file__).resolve().parents[1] / "groove_templates.json"

# GM drum notes -> the three lanes a template covers (the dataset's own map)
CLASS = {36: "kick", 38: "snare", 40: "snare", 37: "snare",
         42: "hat", 22: "hat", 44: "hat", 46: "hat", 26: "hat"}
MIN_HITS = 8          # fewer hits on a step than this -> no claim for it
MAX16 = 0.25          # never move a hit more than a quarter of a 16th


def _hits(mid_path, bpm):
    """(class, position in 16ths, velocity 0-1) for every drum hit."""
    import mido
    m = mido.MidiFile(str(mid_path))
    sixteenth = 60.0 / bpm / 4
    t, out = 0.0, []
    for msg in m:                       # iterating a MidiFile yields seconds
        t += msg.time
        if msg.type == "note_on" and msg.velocity > 0 and msg.note in CLASS:
            out.append((CLASS[msg.note], t / sixteenth, msg.velocity / 127))
    return out


def build(gmd=GMD):
    rows = list(csv.DictReader(open(gmd / "info.csv")))
    acc = defaultdict(lambda: defaultdict(lambda: ([], [])))
    for r in rows:
        if r["beat_type"] != "beat" or r["time_signature"] != "4-4":
            continue
        key = "%s:%s" % (r["style"].split("/")[0], r["drummer"])
        hits = _hits(gmd / r["midi_filename"], float(r["bpm"]))
        # Zero = this take's own quarter notes. Whole takes sit ~20 ms early
        # (kit/recording latency, or the player's lean); the lean is the
        # DJ's lane offset's job, so only the step-to-step shape is kept.
        q = [p - round(p) for _c, p, _v in hits if round(p) % 4 == 0]
        zero = float(np.median(q)) if q else 0.0
        for cls, pos, vel in hits:
            pos -= zero
            step = int(round(pos))
            devs, vels = acc[key][(cls, step % 16)]
            devs.append(pos - step)
            vels.append(vel)
    out = {}
    for key, cells in acc.items():
        tpl = {}
        for cls in ("kick", "snare", "hat"):
            off, vel = [None] * 16, [None] * 16
            for s in range(16):
                devs, vels = cells.get((cls, s), ([], []))
                if len(devs) >= MIN_HITS:
                    off[s] = round(float(np.clip(np.median(devs),
                                                 -MAX16, MAX16)), 4)
                    vel[s] = float(np.mean(vels))
            top = max([v for v in vel if v] or [0])
            if top <= 0:
                continue
            tpl[cls] = {"offset16": off,
                        "vel": [round(v / top, 3) if v else None
                                for v in vel]}
        if tpl:
            out[key] = tpl
    return out


# Which real drummers fit an identity, read off its listen line. Machine
# words first: a drum-machine style keeps its machine timing.
MACHINE_WORDS = ("trap", "drill", "rage", "32nd", "drum machine",
                 "drum-machine", "electro", "8-bit", "chip", "club",
                 "four-on-the-floor", "industrial", "dembow", "halftime",
                 "half-time", "jungle", "bounce", "miami")
STYLE_WORDS = (("jazz", "jazz"), ("soul", "soul"), ("funk", "funk"),
               ("new orleans", "neworleans"), ("rock", "rock"),
               ("breakbeat", "funk"))
# a style word only picks the drummer when the line says the drums are
# PLAYED; otherwise "jazz"/"soul" describe the samples, not the kit
PLAYED_WORDS = ("by hand", "hand-played", "played", "band", "live")
# machine-timed by their sound, though their lines carry no machine word
MACHINE_NAMES = {"Glass Cat", "Swish Beatz", "Baltimore Club", "Wonky",
                 "New Orleans Bounce", "Houston Screw", "Detroit"}
ACCENT_FLOOR = 10 ** (-4.0 / 20)   # owner pick: softest accent 4 dB down
_TEMPLATES = None


def templates():
    global _TEMPLATES
    if _TEMPLATES is None:
        _TEMPLATES = json.loads(OUT.read_text()) if OUT.exists() else {}
    return _TEMPLATES


OUTSIDE_P = 0.10    # owner 2026-11-04: 1 beat in 10 plays outside its zone


def pick(listen, rng, name="", style=None):
    """The `real_feel` stamp for a new beat: {"key": "hiphop:drummer3",
    "skip": [...]}, or None for a machine-timed identity.  1 beat in 10
    (OUTSIDE_P) swaps to a drummer family outside the identity's own zone:
    any family but its own, and a machine-timed identity gets a real one."""
    low = (listen or "").lower()
    skip = ["hat"] if "hats dead straight" in low else []
    own = None                          # None = machine zone
    if style:                           # crew_config "real_feel_style"
        own = style
    elif not (name in MACHINE_NAMES or any(w in low for w in MACHINE_WORDS)):
        own = "hiphop"
        if any(w in low for w in PLAYED_WORDS):
            own = next((st for w, st in STYLE_WORDS if w in low), "hiphop")
    if rng.random() < OUTSIDE_P:
        fams = sorted({k.split(":")[0] for k in templates()} - {own})
        if fams:
            own = rng.choice(fams)
    if own is None:
        return None
    keys = sorted(k for k in templates() if k.startswith(own + ":"))
    return {"key": rng.choice(keys), "skip": skip} if keys else None


def lane_class(lane):
    if lane.startswith("kick"):
        return "kick"
    if lane.startswith(("snare", "clap")):
        return "snare"
    if lane.startswith("hat"):
        return "hat"
    return None


def accent(tpl, lane_class, step16):
    """Gain for a written normal/accent hit: the drummer's own loud/soft
    shape for this step, never more than 4 dB down (1.0 where silent)."""
    v = ((tpl or {}).get(lane_class) or {}).get("vel")
    if not v or v[step16 % 16] is None:
        return 1.0
    return max(ACCENT_FLOOR, min(1.0, v[step16 % 16]))


def offset_s(tpl, lane_class, step16, bpm):
    """Seconds a real player moves this step (0 when the template is
    silent on it)."""
    d = ((tpl or {}).get(lane_class) or {}).get("offset16")
    if not d or d[step16 % 16] is None:
        return 0.0
    return d[step16 % 16] * 60.0 / bpm / 4


def _demo():
    import random
    assert pick("dark trap, 808s", random.Random(1)) is None
    n = sum(pick("dark trap, 808s", random.Random(i)) is not None
            for i in range(2000))
    assert 130 < n < 270, n            # about 10% play outside the zone
    fam = lambda i: pick("jazz played by hand", random.Random(i))["key"][:4]
    assert sum(fam(i) != "jazz" for i in range(2000)) < 270
    st = pick("New York boom bap, hats dead straight", random.Random(1))
    if st:                                   # needs groove_templates.json
        assert st["key"].startswith("hiphop:") and st["skip"] == ["hat"]
    tpl = {"hat": {"offset16": [0.1] + [None] * 15, "vel": [0.3] + [None] * 15}}
    assert accent(tpl, "hat", 0) == ACCENT_FLOOR and accent(tpl, "hat", 1) == 1.0
    assert abs(offset_s(tpl, "hat", 16, 90) - 0.1 * 60 / 90 / 4) < 1e-9
    assert offset_s(tpl, "kick", 0, 90) == 0.0


if __name__ == "__main__" and sys.argv[1:] == ["--check"]:
    _demo()
    print("ok")
elif __name__ == "__main__":
    if not GMD.exists():
        sys.exit("Groove MIDI Dataset not found at %s (is TBOTC 3 mounted?)"
                 % GMD)
    t = build()
    OUT.write_text(json.dumps(t, indent=1, ensure_ascii=False))
    print("%d templates -> %s" % (len(t), OUT))
