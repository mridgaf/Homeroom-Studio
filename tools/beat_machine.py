"""Beat Machine — the crew's jukebox (owner request 2026-07-15).

A little window with a checkbox per DJ, a tempo box, and a notes box.
Check ONE DJ -> one brand-new random beat from them. Check TWO OR MORE
-> one collab beat (first-checked DJ hosts: their groove and snare,
the second DJ's kick tone, everyone's stamp) filed in the FIRST-checked
DJ's folder. Tempo blank = the DJ's home tempo.

Beats land in ~/Documents/Samples/Claude Drum Beats/<DJ name>/ with the
next file number, and every render is logged in the root README.txt
(sources, variant, tempo, and whatever was typed in the notes box).
Numbering continues across all folders; nothing is ever overwritten.

Double-click "Beat Machine.command" in the Claude Drum Beats folder: it
opens the Beat Machine as a local web page in your browser (macOS Tk is
too broken to draw a native window, so this is a tiny stdlib http.server
instead — no installs). Leave the Terminal window open; close it to quit.
Or run:  ./.venv/bin/python tools/beat_machine.py
CLI (for testing):  ... beat_machine.py --render "Otto Grit,Cutz"
                    [--tempo 95] [--count N] [--notes "..."] [--out DIR]
"""
import argparse
import copy
import random
import re
import sys
import zlib
from datetime import date
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, write_wav24
from make_drum_beats import build_shots
from crew import (BARS, CREW, boom_bap_variant, build_kit, lock_stamps,
                  normalize_preset, render_crew_beat, _load_choked,
                  _pick_path, _resolve_secs)
from beat_recipes import (history_avoid, load_recipe, record_history,
                          save_recipe, write_midi, write_stems)
from pattern_gen import compose, kick_seen, remember_kick

ROOT = Path("~/Documents/Samples/Claude Drum Beats").expanduser()
ORDER = sorted(CREW, key=lambda n: CREW[n]["num"])

# Random beat titles, two words, in each character's voice. The picker
# retries until the title isn't already on a file anywhere in the folder.
TITLES = {
    "Otto Grit": (["Couch", "Pocket", "Porch", "Wobbly", "Corner", "Sleepy",
                   "Crooked", "Basement"],
                  ["Spring", "Change", "Nap", "Stairs", "Button", "Shuffle",
                   "Lean", "Drawer"]),
    "Cutz": (["Razor", "Fader", "Needle", "Scalpel", "Blade", "Crossfade",
              "Precision", "Surgical"],
             ["Talk", "Discipline", "Etiquette", "Practice", "Lesson",
              "Motion", "Routine", "Work"]),
    "Crate Prophet": (["Attic", "Incense", "Reel", "Warm", "Dusty", "Vinyl",
                       "Basement", "Sunday"],
                      ["Sermon", "Smoke", "Ritual", "Prayer", "Garden",
                       "Letters", "Wisdom", "Groove"]),
    "Chrome Dial": (["Beeper", "Satellite", "Dial", "Signal", "Neon",
                     "Static", "Velvet", "Mirror"],
                    ["Bounce", "Answer", "Language", "Games", "Logic",
                     "Season", "Traffic", "Code"]),
    "Glass Cat": (["Empty", "Clean", "White", "Quiet", "Bare", "Cold",
                   "Simple", "Still"],
                  ["Hallway", "Corners", "Marble", "Mirror", "Windows",
                   "Porcelain", "Geometry", "Space"]),
    "Sunday Chop": (["Choir", "Gospel", "Pulpit", "Steeple", "Revival",
                     "Deacon", "Sanctuary", "Amen"],
                    ["Hands", "Stomp", "Morning", "Shout", "Doors", "March",
                     "Echo", "Corner"]),
    "Night Metro": (["Midnight", "Tunnel", "Last", "Empty", "Shadow",
                     "Platform", "Concrete", "Downtown"],
                    ["Line", "Lights", "Transfer", "Window", "District",
                     "Signal", "Rain", "Route"]),
    "Rage Engine": (["Piston", "Redline", "Throttle", "Furnace", "Nitro",
                     "Turbine", "Gravel", "Voltage"],
                    ["Storm", "Fever", "Sprint", "Riot", "Charge", "Alarm",
                     "Stampede", "Surge"]),
    "New Math": (["Fifth", "Prime", "Vector", "Axiom", "Modular", "Curved",
                  "Golden", "Infinite"],
                 ["Postulate", "Remainder", "Function", "Sequence",
                  "Fraction", "Lemma", "Ratio", "Angle"]),
}
COLLAB_TITLES = (["Split", "Shared", "Double", "Joint", "Twin", "Crossed",
                  "Common", "Meeting"],
                 ["Custody", "Language", "Booth", "Statement", "Shift",
                  "Wires", "Ground", "Point"])

TEMPO_LO, TEMPO_HI = 60, 200


def next_number(root=ROOT):
    """Next file number, scanning every folder so numbering stays global."""
    top = max((int(m.group(1)) for f in root.rglob("*.wav")
               if (m := re.match(r"(\d+) ", f.name))), default=0)
    return max(top, 85) + 1


def fresh_title(names, rng, root=ROOT):
    first, second = TITLES[names[0]] if len(names) == 1 else COLLAB_TITLES
    taken = " | ".join(f.name for f in root.rglob("*.wav")).lower()
    for _ in range(200):
        t = f"{rng.choice(first)} {rng.choice(second)}"
        if f" {t.lower()} drums" not in taken:
            return t
    return f"Take {rng.randrange(100, 999)}"          # bank exhausted


# ---------------------------------------------------------- variety engine
# Owner verdict 2026-07-16: sample-swapping alone reads as "the same beat
# slightly changed" — he wants every beat significantly different. So each
# beat now ALSO mutates patterns and arrangement (seeded by variant, so any
# beat re-renders identically): small-hit mutation, a density profile, hat
# density, one structural treatment from the school notes (drop-out /
# frisson build / phrase-tail hole / B-section lane change / quiet bar),
# an occasional color-lane omit, and a tempo lean. Timing DNA (LaneFeel
# offsets, swing) and the locked stamp are never touched — the character
# survives; the beat doesn't repeat.

TIMEKEEPERS = {"hat", "snap"}


def _hits(pat):
    return sum(c != "-" for c in pat)


def _mutate_pat(pat, rng, p_drop, adds):
    """Drop/shift the small hits (x o .), sprinkle a few new soft ones.
    Capital-X anchors (the character's core grammar) and deliberate
    all-rest bars (blackouts) are left alone."""
    if _hits(pat) == 0:
        return pat
    s = list(pat)
    n = len(s)
    for i in range(n):
        if s[i] in "xo." and rng.random() < p_drop:
            s[i] = "-"
        elif s[i] in "xo." and rng.random() < 0.25:
            j = i + rng.choice((-1, 1))
            if 0 <= j < n and s[j] == "-":
                s[j], s[i] = s[i], "-"
    empties = [i for i, c in enumerate(s) if c == "-"]
    rng.shuffle(empties)
    for i in empties[:adds]:
        s[i] = "x"
    return "".join(s)


def _mutate_kick(bars, rng):
    """The kick grammar itself wanders between beats (owner 2026-07-16:
    half the crew wrote their kicks entirely in capital anchors, so the
    small-hit mutation never touched them and every beat shared one kick
    line). Bar 1 states the character's grammar untouched; in later bars
    up to two anchors may drop or slide a 16th, and a soft extra kick can
    land in a gap. The downbeat never moves."""
    out = [bars[0]]
    for pat in bars[1:]:
        s = list(pat)
        n = len(s)
        xs = [i for i, c in enumerate(s) if c == "X" and i != 0]
        rng.shuffle(xs)
        for i in xs[:2]:
            r = rng.random()
            if r < 0.18:
                s[i] = "-"
            elif r < 0.36:
                j = i + rng.choice((-1, 1))
                if 0 <= j < n and s[j] == "-":
                    s[j], s[i] = "X", "-"
        if rng.random() < 0.25:
            gaps = [i for i, c in enumerate(s) if c == "-" and i % 2 == 0]
            if gaps:
                s[rng.choice(gaps)] = "x"
        out.append("".join(s))
    return out


def _hat_density(bars, mode):
    """thin = timekeeper drops to the strong steps; dense = fills gaps
    between existing hits. Straightness/swing are untouched (feel DNA)."""
    out = []
    for pat in bars:
        if _hits(pat) == 0:
            out.append(pat)
            continue
        s = list(pat)
        n = len(s)
        if mode == "thin":
            for i in range(n):
                if s[i] in "xo." and i % 2 == 1:
                    s[i] = "-"
        elif mode == "dense":
            for i in range(1, n - 1):
                if s[i] == "-" and s[i - 1] != "-" and i % 2 == 1:
                    s[i] = "x"
        out.append("".join(s))
    return out


BACKBONE = {"kick", "snare", "clap"}     # owner rule 2026-07-17: never stops


def vary_preset(preset, variant, num, tempo_locked, density=None):
    """Apply the per-beat variety plan to a (deep-copied) preset in place.
    Returns a list of plain-words notes describing what this beat does.
    Owner rule 2026-07-17: room for his top line means SPARSENESS, never
    silence — kick and snare play through every bar; quiet moments are
    hats/colors resting and velocities softening. density (from the
    notes-box directions) overrides the rolled profile for this beat."""
    rng = random.Random(num * 100003 + variant * 977)
    lanes = preset["lanes"]
    notes = []

    def rewrite(ln, new_bars):
        pan, gain, feel, _ = lanes[ln]
        lanes[ln] = (pan, gain, feel, new_bars)

    mutable = [ln for ln in lanes if not ln.startswith("stamp")]

    # 1. density profile + small-hit mutation on every non-stamp lane
    # (leans sparse since 2026-07-17 — these are beds to play over)
    profile = density or rng.choices(["sparse", "home", "busy"],
                                     [5, 4, 1])[0]
    p_drop = {"sparse": 0.5, "home": 0.3, "busy": 0.18}[profile]
    for ln in mutable:
        bars = lanes[ln][3]
        if ln == "kick":
            # the composed kick IS the beat's identity — the density
            # pass must not erode it into a bare skeleton (2026-07-17:
            # two beats collapsed to the same line that way). Only the
            # gentle anchor wander applies.
            rewrite(ln, _mutate_kick(list(bars), rng))
            continue
        busy_ok = sum(map(_hits, bars)) / len(bars) >= 4
        adds = ({"sparse": 0, "home": 1, "busy": 1}[profile]
                if busy_ok else 0)
        rewrite(ln, [_mutate_pat(b, rng, p_drop, adds) for b in bars])
    notes.append(f"{profile} density")

    # 2. timekeeper density (hat/snap): thin / home / dense
    for ln in TIMEKEEPERS & set(mutable):
        mode = rng.choice(["thin", "home", "home", "dense"])
        if mode != "home":
            rewrite(ln, _hat_density(lanes[ln][3], mode))
            notes.append(f"{ln}s {mode}")

    # 3. occasionally rest a color lane for the whole beat (guests are
    # exempt — the composer just seated them for a reason)
    colors = [ln for ln in mutable
              if ln not in {"kick", "snare", "clap"} | TIMEKEEPERS
              and ln not in preset.get("_guests", ())]
    if colors and rng.random() < 0.3:
        ln = rng.choice(colors)
        rewrite(ln, ["-" * len(b) for b in lanes[ln][3]])
        notes.append(f"no {ln} this time")

    # 4. one structural treatment — owner rule 2026-07-17: NO silence
    # gaps, ever. Quiet moments THIN the beat: hats and colors rest,
    # velocities soften, and the kick+snare backbone plays through.
    t = rng.choice(["thinbar", "frisson", "bshift", "quietbar"])
    if t == "thinbar":                       # hats+colors rest a bar
        b = rng.choice((4, 5, 6))
        for ln in mutable:
            bars = list(lanes[ln][3])
            if ln in BACKBONE:
                bars[b] = bars[b].replace("X", "x")   # backbone breathes
            else:
                bars[b] = "-" * len(bars[b])
            rewrite(ln, bars)
        notes.append(f"bar {b + 1} thins to kick and snare")
    elif t == "frisson":                     # build: bar 7 thins, 8 slams
        for ln in mutable:
            bars = list(lanes[ln][3])
            if ln not in BACKBONE:
                bars[6] = "-" * len(bars[6])
            bars[7] = bars[7].replace("x", "X")
            rewrite(ln, bars)
        notes.append("build: bar 7 thins out, bar 8 slams")
    elif t == "bshift":                      # a color lane sits out a half
        cands = [ln for ln in mutable if ln not in BACKBONE and
                 sum(map(_hits, lanes[ln][3]))]
        if cands:
            ln = rng.choice(cands)
            half = rng.choice(("A", "B"))
            bars = list(lanes[ln][3])
            for b in (range(4) if half == "B" else range(4, 8)):
                bars[b] = "-" * len(bars[b])
            rewrite(ln, bars)
            notes.append(f"{ln} only in the {half} section")
    else:                                    # quiet bar: velocity dip
        b = rng.choice((1, 2, 5))
        for ln in mutable:
            bars = list(lanes[ln][3])
            bars[b] = bars[b].replace("X", "x")
            rewrite(ln, bars)
        notes.append(f"bar {b + 1} pulls back (velocity dip)")

    # 4b. every beat gets a breath: hats and colors rest for the back
    # half of one bar while the backbone carries it (sparser, not silent)
    if t in ("bshift", "quietbar"):
        b = rng.choice((5, 6))
        for ln in mutable:
            if ln in BACKBONE:
                continue
            bars = list(lanes[ln][3])
            n = len(bars[b])
            bars[b] = bars[b][:n // 2] + "-" * (n - n // 2)
            rewrite(ln, bars)
        notes.append(f"hats sit out the back half of bar {b + 1}")

    # 5. tempo lean (only when he didn't set a tempo himself)
    if not tempo_locked:
        lean = rng.choice((-0.05, -0.03, 0.0, 0.03, 0.05))
        if lean:
            preset["bpm"] = max(TEMPO_LO,
                                min(TEMPO_HI,
                                    int(round(preset["bpm"] * (1 + lean)))))
            notes.append(f"tempo leans to {preset['bpm']}")
    return notes


def solo_preset(name, variant, bpm):
    """One DJ's preset for this beat: a FRESH pattern composed from their
    grammar (owner verdict 2026-07-17 — no more one-skeleton mutations),
    tempo override, and the standing rules (New Math goes boom bap on odd
    variants; ~1 beat in 10 skips the sidechain — Crate Prophet already
    never ducks). Returns (preset, style notes)."""
    bb = name == "New Math" and variant % 2 == 1
    if bb:
        p = boom_bap_variant(bpm or 94)
    else:
        p = copy.deepcopy(CREW[name])
        if bpm:
            p["bpm"] = bpm
    p["vel_seed"] = variant
    notes = compose(p, name, variant, boom_bap=bb)
    roll = random.Random(CREW[name]["num"] * 31 + variant)
    if p["sidechain"] > 0 and roll.random() < 0.1:
        p["sidechain"] = 0.0
    return p, notes


# which job each lane does in a beat — the unit a collab deals out
LANE_JOB = {"kick": "kick", "snare": "backbeat", "clap": "backbeat",
            "hat": "timekeeper", "snap": "timekeeper"}
JOBS = ("kick", "backbeat", "timekeeper", "color")


def collab_preset(names, variant, bpm):
    """A collab is an even 50/50 blend (owner decision 2026-07-16 —
    supersedes both the old host-carries-it recipe and the spec doc's
    80/20). Each parent first COMPOSES fresh from their own grammar
    (2026-07-17 — collabs get new rhythms too), then the beat's four
    jobs — kick, backbeat, timekeepers, color — are dealt out evenly
    (seeded by variant), each lane keeping its parent's pattern, groove
    numbers, AND drum taste, so both fingerprints are audibly in the
    beat. Mix flavor is averaged, the kick's distortion follows whoever
    brought the kick, and every parent's stamp gets a lane. First-checked
    still names the folder. Returns (preset, style notes)."""
    host = names[0]
    rng = random.Random(CREW[host]["num"] * 6673 + variant)
    order = list(names)
    rng.shuffle(order)
    assign = {job: order[i % len(order)] for i, job in enumerate(JOBS)}

    fresh, notes = {}, []
    for n in names:
        q = copy.deepcopy(CREW[n])
        qnotes = compose(q, n, variant)
        fresh[n] = q
        notes.append(f"{n}: " + "; ".join(qnotes))

    p = {"num": CREW[host]["num"], "era": "collab",
         "built": " x ".join(f"{n} ({', '.join(j for j in JOBS if assign[j] == n)})"
                             for n in names),
         "bpm": bpm or round(sum(CREW[n]["bpm"] for n in names) / len(names)),
         "lanes": {}, "kit": {}, "lane_parent": {}, "alt": None,
         "kick_dist": CREW[assign["kick"]]["kick_dist"]}
    for k in ("dust", "sidechain", "mix_sat", "drive", "wow"):
        p[k] = sum(CREW[n][k] for n in names) / len(names)
    beds = [CREW[n]["vinyl"] for n in names if CREW[n]["vinyl"]]
    p["vinyl"] = min(beds) - 2 if beds else 0     # quieter bed when shared

    for job in JOBS:
        parent = assign[job]
        q = fresh[parent]
        for lane, spec in q["lanes"].items():
            if lane == "stamp" or LANE_JOB.get(lane, "color") != job:
                continue
            p["lanes"][lane] = copy.deepcopy(spec)
            p["kit"][lane] = copy.deepcopy(q["kit"][lane])
            p["lane_parent"][lane] = parent
    # the space treatment follows the backbeat it's treating
    p["kick_flavors"] = copy.deepcopy(
        CREW[assign["kick"]].get("kick_flavors", []))
    bb = CREW[assign["backbeat"]]["space"]
    p["space"] = (bb[0], [ln for ln in bb[1] if ln in p["lanes"]])

    p["vel_seed"] = variant
    pan = CREW[host]["lanes"]["stamp"][0]
    p["lanes"]["stamp"] = copy.deepcopy(CREW[host]["lanes"]["stamp"])
    for i, g in enumerate(names[1:]):
        gpan, ggain, gfeel, gbars = CREW[g]["lanes"]["stamp"]
        side = -pan if abs(pan) > 0.05 else 0.3 * (1 if i % 2 == 0 else -1)
        p["lanes"][f"stamp{i + 2}"] = (side, ggain, gfeel, gbars)
    return p, notes


def collab_kit(shots, names, preset, stamps, variant, avoid):
    """Each lane's drum is picked with that lane's parent's taste (the
    50/50 deal struck in collab_preset) — plus everyone's locked stamp.
    Also returns the resolved spec per lane so the recipe can re-pick a
    single drum later (the swap flow)."""
    host = names[0]
    kit, sources, spec_used = {}, {}, {}
    for lane, (role, must, wants, secs) in preset["kit"].items():
        parent = preset["lane_parent"][lane]
        secs = _resolve_secs(secs, CREW[parent]["num"], variant)
        seed = (CREW[host]["num"] * 1000 + variant * 7919
                + zlib.crc32(lane.encode()) % 997)
        path, x = _pick_path(shots, role, wants, secs, seed,
                             must=must, avoid=avoid)
        if path:
            avoid.add(path)
        kit[lane] = x
        sources[lane] = path
        spec_used[lane] = (role, must, wants, secs)
    kit["stamp"] = stamps[host][1]
    sources["stamp"] = f"{Path(stamps[host][0]).name}  [{host}'s stamp]"
    for i, g in enumerate(names[1:]):
        kit[f"stamp{i + 2}"] = stamps[g][1]
        sources[f"stamp{i + 2}"] = f"{Path(stamps[g][0]).name}  [{g}'s stamp]"
    return kit, sources, spec_used


# --------------------------------------------------- notes-box directions
# Owner rule 2026-07-17: whatever he types in the notes box steers THE
# BEATS OF THAT CLICK ONLY — nothing persists to the config, the crew, or
# later generations. Understood directions are applied and echoed in the
# README; the rest is just a note, like before.

DIRECTION_TAGS = {          # words in the box -> sample want-tags
    "acoustic": "acoustic", "clean": "clean", "dirty": "dirty",
    "dusty": "dust", "lofi": "lofi", "lo-fi": "lofi",
    "vintage": "vintage", "warm": "warm", "hard": "hard", "soft": "soft",
    "punchy": "punch", "deep": "deep", "crisp": "crisp", "tight": "tight",
    "boomy": "boom", "distorted": "distort", "vinyl": "vinyl"}

LANE_WORDS = [              # most specific first; spellings are generous
    ("hat", ("hi hats", "hi-hats", "hihats", "hi hat", "hihat", "hi-hat",
             "high hats", "high hat", "high-hats", "high-hat", "highhats",
             "highhat", "cymbals", "cymbal", "hats", "hat")),
    ("snare", ("snares", "snare")),
    ("clap", ("claps", "clap")),
    ("kick", ("kick drums", "kick drum", "kicks", "kick", "bass drum",
              "bass drums")),
    ("snap", ("snaps", "snap", "finger snaps")),
    ("perc", ("percussion", "percs", "perc")),
    ("bongo", ("bongos", "bongo", "congas", "conga")),
    ("stamp", ("stamps", "stamp")),
    ("_guests", ("guests", "guest", "extras"))]

NEGATIONS = ("no ", "without ", "skip ", "skip the ", "drop the ",
             "drop ", "remove the ", "remove ", "take out the ",
             "take out ", "leave out the ", "leave out ", "minus ",
             "none of the ", "no more ", "hold the ")


def parse_directions(notes):
    """Read this click's directions out of the notes text."""
    t = " " + (notes or "").lower().replace(",", " ").replace(".", " ") + " "
    t = " ".join(t.split())
    t = f" {t} "
    out = {"mute": set(), "tags": [], "kick": None, "density": None}
    for lane, words in LANE_WORDS:
        if any(neg + w in t for w in words for neg in NEGATIONS):
            out["mute"].add(lane)
    if any(x in t for x in ("no 808s", "no 808", "no sub", "clean kick",
                            "acoustic kick", "short kick")):
        out["kick"] = "clean"
    elif any(x in t for x in ("long 808", "sustained", "808 only",
                              "all 808")):
        out["kick"] = "808"
    out["tags"] = [tag for word, tag in DIRECTION_TAGS.items()
                   if word in t]
    if any(x in t for x in ("sparse", "minimal", "less drums",
                            "more space", "empty")):
        out["density"] = "sparse"
    elif any(x in t for x in ("busier", "busy", "more drums")):
        out["density"] = "busy"
    return out


def apply_directions(preset, dirs):
    """Mutate this beat's preset per the parsed directions. Returns
    plain-words notes; the caller must run this BEFORE the kit is picked
    so muted lanes never grab a sample."""
    notes = []
    guests = set(preset.get("_guests", ()))
    for lane in list(preset["lanes"]):
        base = lane.rstrip("0123456789")
        if base in dirs["mute"] or (lane in guests
                                    and "_guests" in dirs["mute"]):
            del preset["lanes"][lane]
            preset["kit"].pop(lane, None)
            notes.append(f"no {lane} (as asked)")
    if "kick" not in preset["lanes"]:
        preset["sidechain"] = 0.0            # nothing left to duck around
    space, on = preset["space"]
    preset["space"] = (space, [ln for ln in on if ln in preset["lanes"]])

    if dirs["kick"] and "kick" in preset["kit"]:
        flavors = [f for f in preset.get("kick_flavors", [])
                   if (f[1] == "808") == (dirs["kick"] == "808")]
        if flavors:
            _, must, wants, secs = flavors[0]
            role = preset["kit"]["kick"][0]
            preset["kit"]["kick"] = (role, must, list(wants), tuple(secs))
            notes.append(f"kick: {dirs['kick']} (as asked)")

    if dirs["tags"]:
        for lane, (role, must, wants, secs) in list(preset["kit"].items()):
            merged = dirs["tags"] + [w for w in wants
                                     if w not in dirs["tags"]]
            preset["kit"][lane] = (role, must, merged, secs)
        notes.append("prefer " + "/".join(dirs["tags"]) + " (as asked)")
    return notes


def dj_cut(L, R, parts, bar):
    """Hard-mute one bar in the finished audio (20 ms fades) — the
    last-resort deepening. Applied to the stems too so the Reason 12
    handoff matches what the WAV plays."""
    barlen = len(L) // BARS
    a, b = bar * barlen, (bar + 1) * barlen
    f = min(int(0.02 * SR), barlen // 4)
    env = np.ones(len(L))
    env[a:b] = 0.0
    env[a - f:a] = np.linspace(1, 0, f)
    env[b:b + f] = np.linspace(0, 1, f)
    parts["stems"] = {ln: (sL * env, sR * env)
                      for ln, (sL, sR) in parts["stems"].items()}
    return L * env, R * env


def generate(names, tempo=None, notes="", root=ROOT, shots=None,
             status=lambda msg: None):
    """Render one random beat (solo or collab) into names[0]'s folder.
    Returns (path, report_line). Raises on an empty selection."""
    seen = set()                                  # dedupe, KEEP caller order
    names = [n for n in names
             if n in CREW and not (n in seen or seen.add(n))]
    if not names:
        raise ValueError("Check at least one DJ first.")
    bpm = None
    if tempo:
        bpm = int(round(float(tempo)))
        if not TEMPO_LO <= bpm <= TEMPO_HI:
            raise ValueError(f"Tempo must be {TEMPO_LO}-{TEMPO_HI} BPM.")

    # engine-driven evolution (owner decision 2026-07-17): first time a
    # DJ is featured today they change ONE deliberate thing, journaled
    # with rollback. Only for the real library — test/--out renders
    # must never move a career.
    evo_notes = []
    if root == ROOT:
        import evolution
        evo_notes = evolution.maybe_evolve(names, status=status)

    if shots is None:
        status("Scanning your sample library…")
        shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    # anti-repetition hard rule (spec 2026-07-16): whatever these DJs
    # used recently is off the table, across sessions
    avoid |= history_avoid(names)

    no = next_number(root)
    # this click's directions from the notes box ("no hi hats",
    # "acoustic", ...) — applied to these beats only, never persisted
    dirs = parse_directions(notes)

    # compose + vary until the FINAL kick line (the one that renders) is
    # genuinely new for this DJ — the compose-time guard alone missed
    # patterns that collapsed into each other during the variety pass
    # (owner report 2026-07-17: "still very similar")
    status(f"Composing for {' x '.join(names)}…")
    for _try in range(8):
        variant = random.randrange(2, 10000)
        if len(names) == 1:
            preset, style_notes = solo_preset(names[0], variant, bpm)
        else:
            preset, style_notes = collab_preset(names, variant, bpm)
        dnotes = apply_directions(preset, dirs)
        vnotes = evo_notes + style_notes + dnotes + vary_preset(
            preset, variant, CREW[names[0]]["num"],
            tempo_locked=bool(bpm), density=dirs["density"])
        final_kick = (preset["lanes"]["kick"][3][0]
                      if "kick" in preset["lanes"] else None)
        if final_kick is None or not kick_seen(names[0], final_kick):
            break
    if final_kick:
        remember_kick(names[0], final_kick)
    rng = random.Random(variant)
    title = fresh_title(names, rng, root)

    status(f"Building the kit for {' x '.join(names)}…")
    if len(names) == 1:
        kit, sources = build_kit(shots, names[0], stamps[names[0]][1],
                                 variant=variant, avoid=avoid,
                                 preset=preset)
        sources["stamp"] = stamps[names[0]][0]
        # same resolution build_kit just did, kept for the beat's recipe
        spec_used = {ln: (r, m, w, _resolve_secs(s, preset["num"], variant))
                     for ln, (r, m, w, s) in preset["kit"].items()
                     if ln != "stamp"}
        lane_parent = {ln: names[0] for ln in spec_used}
    else:
        kit, sources, spec_used = collab_kit(shots, names, preset, stamps,
                                             variant, avoid)
        lane_parent = dict(preset["lane_parent"])

    # standing rule: snare space alternates — odd file numbers gated,
    # even ones dry
    space = "gated" if no % 2 else "dry"
    status(f"Rendering beat {no} at {preset['bpm']} BPM…")
    L, R, lufs, parts = render_crew_beat(names[0], kit, space=space,
                                         preset=preset, want_parts=True)

    def bar_swing(L, R):
        # floor at -30 dB: below that is silence to the ear, and counting
        # digital zero as "dynamics" would inflate the number meaninglessly
        mono = 0.5 * (L + R)
        barlen = len(mono) // BARS
        prof = [max(-30.0, 20 * np.log10(np.sqrt(
            (mono[i * barlen:(i + 1) * barlen] ** 2).mean()) + 1e-12))
            for i in range(BARS)]
        return max(prof) - min(prof)

    swing = bar_swing(L, R)
    cut_bar = None
    if swing < 2.5:
        # the loop needs SOME rise and fall — but owner rule 2026-07-17:
        # never silence. Thin one bar instead: hats and colors rest, the
        # backbone softens and plays through. One re-render, no DJ-cut.
        deep_bar = random.Random(variant * 31
                                 + CREW[names[0]]["num"]).choice((4, 5, 6))
        for ln, (pan, gain, feel, bars) in list(preset["lanes"].items()):
            if ln.startswith("stamp"):
                continue
            bars = list(bars)
            if ln in BACKBONE:
                bars[deep_bar] = bars[deep_bar].replace("X", "x")
            else:
                bars[deep_bar] = "-" * len(bars[deep_bar])
            preset["lanes"][ln] = (pan, gain, feel, bars)
        status(f"Adding contrast to beat {no} "
               f"(bar swing was {swing:.1f} dB)…")
        L, R, lufs, parts = render_crew_beat(names[0], kit, space=space,
                                             preset=preset, want_parts=True)
        swing = bar_swing(L, R)
        vnotes.append(f"bar {deep_bar + 1} thins for contrast")

    folder = root / names[0]
    folder.mkdir(parents=True, exist_ok=True)
    fname = f"{no} {' x '.join(names)} {title} Drums {preset['bpm']}bpm.wav"
    path = folder / fname
    if path.exists():                             # never overwrite
        raise RuntimeError(f"{fname} already exists — not overwriting.")
    write_wav24(path, L, R)

    # the Reason 12 handoff (spec 2026-07-16): MIDI + stems with every WAV
    write_midi(path.with_suffix(".mid"), parts["events"], preset["bpm"])
    write_stems(folder / f"{no} {' x '.join(names)} {title} Stems",
                parts["stems"])

    # and the recipe, so "same beat, different snare" can rebuild it
    stamp_paths = {"stamp": stamps[names[0]][0]}
    stamp_secs = {"stamp": CREW[names[0]]["kit"]["stamp"][3]}
    for i, g in enumerate(names[1:]):
        stamp_paths[f"stamp{i + 2}"] = stamps[g][0]
        stamp_secs[f"stamp{i + 2}"] = CREW[g]["kit"]["stamp"][3]
    save_recipe(root, no, {
        "file": fname, "folder": names[0], "names": names, "title": title,
        "variant": variant, "bpm": preset["bpm"], "space": space,
        "preset": preset, "kit_spec": spec_used,
        "kit_paths": {ln: sources[ln] for ln in spec_used},
        "stamp_paths": stamp_paths, "stamp_secs": stamp_secs,
        "dj_cut_bar": cut_bar, "parent": None, "date": str(date.today())})

    # remember the picks so these DJs don't repeat themselves (hard rule)
    record_history(lane_parent, sources)

    # post-render variety check (2026-07-17): one cheap look at this DJ's
    # recent window; a warning lands in the README + report, never a block
    import variety
    warn = variety.quick_check(root, names[0])
    if warn:
        vnotes.append(warn)

    dur, want = len(L) / SR, BARS * 240.0 / preset["bpm"]
    rms = 20 * np.log10(np.sqrt(0.5 * (L ** 2 + R ** 2).mean()) + 1e-12)
    vnotes.append(f"bar swing {swing:.1f} dB")
    good = abs(dur - want) < 0.02 and -14 < rms < -5 and -10 < lufs < -6.5

    lines = ["", f"BEAT MACHINE — {date.today()}",
             f"{fname}  ->  {names[0]}/  (+ .mid and a Stems folder)"]
    kind = ("solo" if len(names) == 1
            else f"50/50 collab: {preset['built']}")
    home = (f", home tempo is {CREW[names[0]]['bpm']}"
            if bpm and len(names) == 1 else "")
    lines.append(f"  {kind}, {preset['bpm']} BPM"
                 f"{' (requested)' if bpm else ''}{home}, variant {variant}")
    lines.append(f"  snare space: {space} | sidechain: "
                 f"{'on' if preset['sidechain'] > 0 else 'off'}"
                 f" | LUFS {lufs:.1f} | {'ok' if good else 'CHECK'}")
    if len(names) == 1 and names[0] == "New Math":
        lines.append(f"  mode: {'boom bap' if variant % 2 else 'front edge'}")
    lines.append(f"  this beat: {'; '.join(vnotes)}")
    if notes.strip():
        lines.append(f"  notes: {notes.strip()}")
    for lane, p in sources.items():
        lines.append(f"  {lane}: {Path(p).name if p else '(none)'}"
                     if not (p and '[' in str(p))
                     else f"  {lane}: {p}")
    with open(root / "README.txt", "a") as f:
        f.write("\n".join(lines) + "\n")

    report = (f"{fname}\n-> {names[0]} folder (+ MIDI and "
              f"{len(parts['stems'])} stems) | LUFS {lufs:.1f} | "
              f"{'checks passed' if good else 'CHECK THIS ONE'}"
              f"\n   this one: {'; '.join(vnotes)}")
    return path, report


# ------------------------------------------------------------- swap flow


def swap(number, lane, root=ROOT, shots=None, status=lambda msg: None):
    """Owner spec 2026-07-16, revision flow: same beat, one drum swapped.
    Pattern, groove, tempo, treatment, and every other sound come straight
    from the saved recipe; only `lane` gets a fresh sample — its old pick,
    the rest of the kit, and the DJ's recent history are all avoided. The
    re-render lands as a NEW numbered file; nothing is overwritten."""
    number = int(number)
    rec = load_recipe(root, number)
    lane = lane.strip().lower()
    if lane not in rec["kit_spec"]:
        raise ValueError(f"Beat {number} has no '{lane}' to swap — "
                         f"it has: {', '.join(sorted(rec['kit_spec']))}.")
    preset = normalize_preset(rec["preset"])
    names = rec["names"]
    if shots is None:
        status("Scanning your sample library…")
        shots = build_shots()

    role, must, wants, secs = rec["kit_spec"][lane]
    old = rec["kit_paths"].get(lane)
    avoid = set(p for p in rec["kit_paths"].values() if p)
    avoid |= set(rec["stamp_paths"].values())
    avoid |= history_avoid(names)
    status(f"Picking a different {lane}…")
    new_path, x = _pick_path(shots, role, wants, secs,
                             random.randrange(1, 1 << 30),
                             must=must, avoid=avoid)
    if not new_path or new_path == old:
        raise RuntimeError(f"The library has no other {lane} to reach for.")

    kit, kit_paths = {}, dict(rec["kit_paths"])
    kit_paths[lane] = new_path
    for ln, pth in kit_paths.items():
        snd = x if ln == lane else _load_choked(pth, rec["kit_spec"][ln][3])
        if snd is None:
            raise RuntimeError(f"{Path(pth).name} (the beat's {ln}) has "
                               "moved or vanished — can't rebuild.")
        kit[ln] = snd
    for ln, pth in rec["stamp_paths"].items():
        snd = _load_choked(pth, rec["stamp_secs"][ln])
        if snd is None:
            raise RuntimeError(f"{Path(pth).name} (a locked stamp) has "
                               "moved or vanished — can't rebuild.")
        kit[ln] = snd

    status(f"Re-rendering beat {number} with the new {lane}…")
    L, R, lufs, parts = render_crew_beat(names[0], kit, space=rec["space"],
                                         preset=preset, want_parts=True)
    if rec.get("dj_cut_bar") is not None:
        L, R = dj_cut(L, R, parts, rec["dj_cut_bar"])

    no = next_number(root)
    folder = root / rec["folder"]
    folder.mkdir(parents=True, exist_ok=True)
    stem_of = f"{' x '.join(names)} {rec['title']} New {lane.capitalize()}"
    fname = f"{no} {stem_of} Drums {preset['bpm']}bpm.wav"
    path = folder / fname
    if path.exists():                             # never overwrite
        raise RuntimeError(f"{fname} already exists — not overwriting.")
    write_wav24(path, L, R)
    write_midi(path.with_suffix(".mid"), parts["events"], preset["bpm"])
    write_stems(folder / f"{no} {stem_of} Stems", parts["stems"])

    rec2 = dict(rec, file=fname, kit_paths=kit_paths, parent=number,
                date=str(date.today()))
    save_recipe(root, no, rec2)
    parent_dj = preset.get("lane_parent", {}).get(lane, names[0])
    record_history({lane: parent_dj}, {lane: new_path})

    with open(root / "README.txt", "a") as f:
        f.write(f"\nBEAT MACHINE — {date.today()}\n"
                f"{fname}  ->  {rec['folder']}/  (+ .mid and a Stems "
                f"folder)\n"
                f"  swap of beat {number} ({rec['file']}): same beat, "
                f"different {lane}\n"
                f"  {lane} was: {Path(old).name if old else '(none)'}\n"
                f"  {lane} now: {Path(new_path).name} | LUFS {lufs:.1f}\n")
    report = (f"{fname}\n-> {rec['folder']} folder | same beat as "
              f"{number}, {lane} swapped to {Path(new_path).name} | "
              f"LUFS {lufs:.1f}")
    return path, report


# --------------------------------------------------------------- web GUI
# macOS ships Apple's deprecated, half-broken Tk 8.5.9 — plain labels and
# text fields never paint, and the themed ttk widgets don't paint at all
# on this machine. So the Beat Machine is a tiny LOCAL web page instead
# (stdlib http.server, no installs): the browser renders it perfectly,
# and it matches the Reason Voice localhost-UI workflow he already uses.

_CACHE = {}

_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Beat Machine</title>
<style>
 :root { color-scheme: light dark; }
 body { font-family: -apple-system, Helvetica, Arial, sans-serif;
        margin: 0; padding: 28px; background: Canvas; color: CanvasText; }
 h1 { margin: 0 0 4px; font-size: 30px; }
 p.sub { margin: 0 0 20px; opacity: .7; line-height: 1.45; }
 .djs { display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 10px 18px; margin-bottom: 22px; }
 .dj { display: flex; align-items: center; gap: 9px; padding: 10px 12px;
       border: 1px solid color-mix(in srgb, CanvasText 18%, transparent);
       border-radius: 10px; cursor: pointer; user-select: none; }
 .dj:has(input:checked) { border-color: #2f7;
       background: color-mix(in srgb, #2f7 12%, transparent); }
 .dj input { width: 18px; height: 18px; }
 .dj .name { font-weight: 600; } .dj .bpm { opacity: .55; font-size: 13px; }
 .dj .ord { margin-left: auto; font-size: 12px; font-weight: 700;
            color: #2a9; min-width: 1.2em; text-align: right; }
 .row { display: flex; align-items: center; gap: 12px; margin: 12px 0; }
 .row label { min-width: 210px; }
 input[type=text], input[type=number] { font-size: 15px; padding: 7px 9px;
       border-radius: 8px; border: 1px solid color-mix(in srgb, CanvasText 25%, transparent);
       background: Field; color: FieldText; }
 #notes { flex: 1; }
 #go { margin-top: 18px; font-size: 17px; font-weight: 600; padding: 12px 22px;
       border: 0; border-radius: 10px; background: #2a7; color: #fff;
       cursor: pointer; } #go:disabled { opacity: .5; cursor: default; }
 #status { margin-top: 18px; white-space: pre-wrap; line-height: 1.5;
           min-height: 1.5em; }
 .hosthint { opacity: .7; font-size: 13px; margin: 2px 0 0; min-height: 1.2em; }
</style></head><body>
<h1>Beat Machine</h1>
<p class="sub">Check one DJ for a random beat from them. Check two or more for
a collab &mdash; it lands in the folder of whichever DJ you check <b>first</b>,
and the number shows your pick order.</p>
<div class="djs">__DJS__</div>
<p class="hosthint" id="hosthint"></p>
<div class="row"><label>Tempo (BPM), blank = DJ&rsquo;s home tempo:</label>
  <input type="text" id="tempo" size="6" placeholder="e.g. 95"></div>
<div class="row"><label>How many beats:</label>
  <input type="number" id="count" value="1" min="1" max="10" style="width:70px"></div>
<div class="row"><label>Directions for THIS click (&amp; saved in the
  README) &mdash; e.g. &ldquo;no hi hats&rdquo;, &ldquo;acoustic&rdquo;,
  &ldquo;dusty&rdquo;, &ldquo;sparse&rdquo;, &ldquo;no 808&rdquo;:</label>
  <input type="text" id="notes"></div>
<button id="go">Make my beats</button>
<div id="status"></div>
<hr style="margin:26px 0; opacity:.25">
<h2 style="font-size:20px; margin:0 0 4px">Same beat, different drum</h2>
<p class="sub">Give a beat's file number and pick the drum to replace &mdash;
the pattern, groove, and every other sound stay locked. Renders as a new
numbered file. (Works for beats made from July 16 on.)</p>
<div class="row"><label>Beat number:</label>
  <input type="number" id="swapno" min="1" style="width:90px">
  <label style="min-width:0">swap the</label>
  <select id="swaplane" style="font-size:15px; padding:6px">
    <option>snare</option><option>kick</option><option>clap</option>
    <option>hat</option><option>snap</option><option>perc</option>
    <option>bongo</option></select>
  <button id="swapgo" style="font-size:15px; font-weight:600; padding:8px 16px;
    border:0; border-radius:8px; background:#27b; color:#fff; cursor:pointer">
    Swap it</button></div>
<div id="swapstatus" style="white-space:pre-wrap; line-height:1.5"></div>
<script>
 const order = [];
 function refresh() {
   document.querySelectorAll('.dj').forEach(d => {
     const cb = d.querySelector('input');
     const pos = order.indexOf(cb.value);
     d.querySelector('.ord').textContent = pos >= 0 ? (pos + 1) : '';
   });
   const hint = document.getElementById('hosthint');
   if (order.length === 0) hint.textContent = '';
   else if (order.length === 1) hint.textContent = 'Solo beat from ' + order[0] + '.';
   else hint.textContent = 'Collab → lands in ' + order[0] + "'s folder (checked first).";
 }
 document.querySelectorAll('.dj input').forEach(cb => {
   cb.addEventListener('change', () => {
     if (cb.checked) { if (!order.includes(cb.value)) order.push(cb.value); }
     else { const i = order.indexOf(cb.value); if (i >= 0) order.splice(i, 1); }
     refresh();
   });
 });
 const go = document.getElementById('go'), st = document.getElementById('status');
 go.onclick = async () => {
   if (order.length === 0) { st.style.color = '#c33';
     st.textContent = 'Check at least one DJ first.'; return; }
   const tempo = document.getElementById('tempo').value.trim();
   const count = document.getElementById('count').value;
   const notes = document.getElementById('notes').value;
   go.disabled = true; st.style.color = '';
   st.textContent = 'Working… the first beat scans your sample library (~30s), then it’s quick.';
   try {
     const r = await fetch('/make', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ names: order, tempo, count, notes }) });
     const d = await r.json();
     if (d.ok) { st.style.color = '#2a8';
       st.textContent = 'Done!\\n' + d.results.join('\\n'); }
     else { st.style.color = '#c33'; st.textContent = d.error; }
   } catch (e) { st.style.color = '#c33'; st.textContent = String(e); }
   go.disabled = false;
 };
 const sgo = document.getElementById('swapgo'),
       sst = document.getElementById('swapstatus');
 sgo.onclick = async () => {
   const no = document.getElementById('swapno').value.trim();
   const lane = document.getElementById('swaplane').value;
   if (!no) { sst.style.color = '#c33';
     sst.textContent = 'Which beat number?'; return; }
   sgo.disabled = true; sst.style.color = '';
   sst.textContent = 'Rebuilding beat ' + no + ' with a different ' + lane + '…';
   try {
     const r = await fetch('/swap', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ number: no, lane }) });
     const d = await r.json();
     if (d.ok) { sst.style.color = '#2a8'; sst.textContent = 'Done!\\n' + d.result; }
     else { sst.style.color = '#c33'; sst.textContent = d.error; }
   } catch (e) { sst.style.color = '#c33'; sst.textContent = String(e); }
   sgo.disabled = false;
 };
</script></body></html>"""


def _page():
    djs = "".join(
        f'<label class="dj"><input type="checkbox" value="{n}">'
        f'<span class="name">{n}</span>'
        f'<span class="bpm">{CREW[n]["bpm"]} BPM</span>'
        f'<span class="ord"></span></label>'
        for n in ORDER)
    return _PAGE.replace("__DJS__", djs)


def run_web(port=8770):
    """Serve the Beat Machine as a local web page and open the browser."""
    import json
    import threading
    import webbrowser
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, ctype, body):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self._send(200, "text/html; charset=utf-8",
                           _page().encode("utf-8"))
            else:
                self._send(404, "text/plain", b"not found")

        def do_POST(self):
            if self.path not in ("/make", "/swap"):
                self._send(404, "text/plain", b"not found")
                return
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/swap":
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        _, report = swap(data.get("number"),
                                         data.get("lane", "snare"),
                                         shots=_CACHE["shots"])
                        print(" ", report.replace("\n", " "))
                    self._send(200, "application/json",
                               json.dumps({"ok": True,
                                           "result": report}).encode())
                except Exception as e:               # shown in the page
                    self._send(200, "application/json",
                               json.dumps({"ok": False,
                                           "error": str(e)}).encode())
                return
            names = data.get("names", [])
            tempo = data.get("tempo") or None
            notes = data.get("notes", "")
            try:
                how_many = max(1, min(10, int(data.get("count") or 1)))
            except (TypeError, ValueError):
                how_many = 1
            try:
                with lock:
                    if "shots" not in _CACHE:
                        _CACHE["shots"] = build_shots()
                    results = []
                    for _ in range(how_many):
                        _, report = generate(names, tempo, notes,
                                             shots=_CACHE["shots"])
                        results.append(report)
                        print(" ", report.replace("\n", " "))
                self._send(200, "application/json",
                           json.dumps({"ok": True, "results": results}).encode())
            except Exception as e:                   # shown in the page
                self._send(200, "application/json",
                           json.dumps({"ok": False, "error": str(e)}).encode())

        def log_message(self, *a):
            pass                                     # keep the terminal quiet

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"\n  Beat Machine is open in your browser: {url}")
    print("  (leave this window open; close it or press Ctrl+C to quit)\n")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Beat Machine closed.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--render", help='comma-separated DJ names (CLI mode)')
    ap.add_argument("--tempo", default=None)
    ap.add_argument("--notes", default="")
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--out", default=None, help="output root override")
    ap.add_argument("--swap", type=int, default=None,
                    help="beat number to rebuild with one drum swapped")
    ap.add_argument("--lane", default="snare",
                    help="which drum --swap replaces (default snare)")
    a = ap.parse_args()
    if a.swap:
        out = Path(a.out).expanduser() if a.out else ROOT
        path, report = swap(a.swap, a.lane, root=out,
                            status=lambda m: print(" ", m))
        print(report)
    elif a.render:
        names = [n.strip() for n in a.render.split(",")]
        out = Path(a.out).expanduser() if a.out else ROOT
        print("  Scanning your sample library…")
        shots = build_shots()
        for _ in range(max(1, min(10, a.count))):
            path, report = generate(names, a.tempo, a.notes, root=out,
                                    shots=shots,
                                    status=lambda m: print(" ", m))
            print(report)
    else:
        run_web()


if __name__ == "__main__":
    main()
