"""Homeroom Studio — the crew's jukebox (owner request 2026-07-15;
named by the owner 2026-07-18, was "Beat Machine").

A little window with a checkbox per DJ, a tempo box, and a notes box.
Check ONE DJ -> one brand-new random beat from them. Check TWO OR MORE
-> one collab beat (first-checked DJ hosts: their groove and snare,
the second DJ's kick tone, everyone's stamp) filed in the FIRST-checked
DJ's folder. Tempo blank = the DJ's home tempo.

Beats land in ~/Documents/Samples/Claude Drum Beats/<DJ name>/ with the
next file number, and every render is logged in the root README.txt
(sources, variant, tempo, and whatever was typed in the notes box).
Numbering continues across all folders; nothing is ever overwritten.

Double-click "Homeroom Studio.command" in the project folder: it
opens Homeroom Studio as a local web page in your browser (macOS Tk is
too broken to draw a native window, so this is a tiny stdlib http.server
instead — no installs). Leave the Terminal window open; close it to quit.
Or run:  ./.venv/bin/python tools/beat_machine.py
CLI (for testing):  ... beat_machine.py --render "Otto Grit,Cutz"
                    [--tempo 95] [--count N] [--notes "..."] [--out DIR]
"""
import argparse
import copy
import json
import os
import random
import re
import shutil
import sys
import zlib
from datetime import date
from pathlib import Path
from urllib.parse import quote

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, sub808, write_wav24
from make_drum_beats import build_shots
from crew import (BARS, CREW, GENRE_NAMES, LEGEND_NAMES, bars_of,
                  boom_bap_variant,
                  build_kit, lock_stamps, normalize_preset,
                  render_crew_beat,
                  _load_choked, _pick_path, _resolve_secs)
from beat_recipes import (history_avoid, load_recipe, record_history,
                          save_recipe, write_midi, write_stems)
from pattern_gen import compose, load_library

def _resolve_beats_root():
    """Where the beat library ACTUALLY lives (owner note 2026-07-18: he
    moves these folders between the internal drive, the iCloud container,
    and external volumes). A hardcoded path is dangerous here — when it
    goes missing the machine would quietly start a brand-new empty
    library and restart numbering ON TOP of existing beats. So: an
    explicit setting wins, otherwise take the candidate that actually
    holds beats, and only fall back to the classic path when nothing
    does.

    Override with REASON_VOICE_BEATS_ROOT, or beats_root.json at the
    project root: {"root": "/Volumes/TBOTC 3/Claude Drum Beats"}
    """
    env = os.environ.get("REASON_VOICE_BEATS_ROOT")
    if env:
        return Path(env).expanduser()
    cfg = Path(__file__).resolve().parent.parent / "beats_root.json"
    if cfg.exists():
        try:
            p = Path(json.loads(cfg.read_text())["root"]).expanduser()
            if p.exists():
                return p
            print(f"WARNING: beats_root.json points at {p}, which isn't "
                  "there — looking for the library elsewhere.")
        except (json.JSONDecodeError, KeyError, TypeError):
            print("WARNING: beats_root.json is broken — ignoring it.")
    home = Path.home()
    name = "Claude Drum Beats"
    cands = [home / "Documents/Samples" / name,
             home / "Library/Mobile Documents/com~apple~CloudDocs"
             / "Documents/Samples" / name]
    vols = Path("/Volumes")
    if vols.exists():
        for v in sorted(vols.iterdir()):
            cands += [v / name, v / "Samples" / name]
    empty = None
    for p in cands:
        try:
            if not p.is_dir():
                continue
            if next(p.rglob("*.wav"), None) is not None:
                return p                      # the one with the beats in it
            empty = empty or p
        except OSError:                       # unreadable/ejected volume
            continue
    return empty or cands[0]


ROOT = _resolve_beats_root()
# the nine loose crew and the twelve Legends get their own boxes on the
# page; both render through the same engine (CREW holds them all)
CREW_ORDER = sorted((n for n in CREW
                     if n not in LEGEND_NAMES and n not in GENRE_NAMES),
                    key=lambda n: CREW[n]["num"])
LEGEND_ORDER = sorted(LEGEND_NAMES, key=lambda n: CREW[n]["num"])
GENRE_ORDER = sorted(GENRE_NAMES, key=lambda n: CREW[n]["num"])
ORDER = CREW_ORDER + LEGEND_ORDER + GENRE_ORDER

# where triaged beats go — moved, never deleted (owner request
# 2026-07-18). Everything else stays in its DJ folder.
FAV_DIR = "Favorites"
TRASH_DIR = "Trash"
# the batch player remembers the last batch across app restarts
STATE = Path(os.path.expanduser("~/.reason_voice/beat_machine_state.json"))

# roots the tuned 808 sub reaches for on traditional beats — low, in the
# octave a hip-hop sub lives (Hz), a handful of common, musical keys
ROOT_HZ = {"C": 32.70, "D": 36.71, "E": 41.20, "F": 43.65, "G": 49.00,
           "A": 55.00, "Bb": 58.27}

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

# the Legends and the Styles bring their own two-word title banks
try:
    from legends import LEGEND_TITLES
    TITLES.update(LEGEND_TITLES)
except Exception:
    pass
try:
    from genres import GENRE_TITLES
    TITLES.update(GENRE_TITLES)
except Exception:
    pass

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
    # 2026-07-22: the loop is no longer always 8 bars, so the structural
    # treatments below can't name bars 4-7 outright — on a 4-bar loop
    # bar 7 doesn't exist, and reaching for it silently did nothing.
    # These pick from the bars this beat actually has.
    nbars = bars_of(preset)
    late = [b for b in (nbars - 4, nbars - 3, nbars - 2) if b >= 1] \
        or [max(nbars - 1, 0)]
    last = max(nbars - 1, 0)

    def rewrite(ln, new_bars):
        pan, gain, feel, _ = lanes[ln]
        lanes[ln] = (pan, gain, feel, new_bars)

    def barlist(ln):
        """This lane's bars, padded to the beat's length so a treatment
        can index any bar without an IndexError on a short pattern."""
        bars = list(lanes[ln][3])
        while len(bars) < nbars:
            bars.append(bars[len(bars) % len(bars)] if bars else "-" * 16)
        return bars

    mutable = [ln for ln in lanes if not ln.startswith("stamp")]
    # the subgenre roster's canon lanes carry the figure that DEFINES the
    # style (owner rule 2026-07-19) — they get the kick's gentle anchor
    # wander, never the drop/add mutation, which would quietly turn a
    # dembow into generic syncopation over a few beats
    canon = set(preset.get("_canon") or ())

    # 1. density profile + small-hit mutation on every non-stamp lane.
    # Owner call 2026-07-22: SPARSE IS ONLY EVER ASKED FOR. The free
    # roll picks home or busy and never sparse — a beat he didn't ask
    # to be thin comes out full. Two things still make it sparse: the
    # dialog box (density, below), and a genre preset that DECLARES it,
    # because trip hop and screw are thin by definition and inside this
    # box fidelity beats the house lean (owner call 2026-07-19).
    profile = density or preset.get("density") \
        or rng.choice(["home", "busy"])
    p_drop = {"sparse": 0.5, "home": 0.3, "busy": 0.1}[profile]
    for ln in mutable:
        bars = lanes[ln][3]
        if ln == "kick" or ln in canon:
            # the composed kick IS the beat's identity — the density
            # pass must not erode it into a bare skeleton (2026-07-17:
            # two beats collapsed to the same line that way). Only the
            # gentle anchor wander applies.
            rewrite(ln, _mutate_kick(list(bars), rng))
            continue
        busy_ok = sum(map(_hits, bars)) / len(bars) >= 4
        adds = ({"sparse": 0, "home": 1, "busy": 2}[profile]
                if busy_ok else {"busy": 1}.get(profile, 0))
        # the backbeat (snare/clap) never gets NEW hits from the density
        # pass, whatever the profile rolls (owner call 2026-07-21: "the
        # backbeat doesn't need to be so busy all the time" — this hit
        # crew and legends alike, since this pass runs on every beat).
        # It can still drop or shift the ghosts compose() gave it, so
        # "sparse" still thins a backbeat out — it just never piles on.
        if ln in BACKBONE:
            adds = 0
        rewrite(ln, [_mutate_pat(b, rng, p_drop, adds) for b in bars])
    notes.append(f"{profile} density")

    # 2. timekeeper density (hat/snap): thin / home / dense
    for ln in TIMEKEEPERS & set(mutable):
        mode = rng.choice(["thin", "home", "home", "dense"])
        if mode != "home":
            rewrite(ln, _hat_density(lanes[ln][3], mode))
            notes.append(f"{ln}s {mode}")

    # everything below treats the canon lanes as backbone too, so a
    # style's defining figure is never the lane chosen to sit out
    backbone = BACKBONE | canon

    # 3. occasionally rest a color lane for the whole beat (guests are
    # exempt — the composer just seated them for a reason)
    colors = [ln for ln in mutable
              if ln not in {"kick", "snare", "clap"} | TIMEKEEPERS | canon
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
        b = rng.choice(late)
        for ln in mutable:
            bars = barlist(ln)
            if ln in backbone:
                bars[b] = bars[b].replace("X", "x")   # backbone breathes
            else:
                bars[b] = "-" * len(bars[b])
            rewrite(ln, bars)
        notes.append(f"bar {b + 1} thins to kick and snare")
    elif t == "frisson" and nbars >= 2:      # build: thins, then slams
        for ln in mutable:
            bars = barlist(ln)
            if ln not in backbone:
                bars[last - 1] = "-" * len(bars[last - 1])
            bars[last] = bars[last].replace("x", "X")
            rewrite(ln, bars)
        notes.append(f"build: bar {last} thins out, bar {last + 1} slams")
    elif t == "bshift" and nbars >= 2:       # a color lane sits out a half
        cands = [ln for ln in mutable if ln not in backbone and
                 sum(map(_hits, lanes[ln][3]))]
        if cands:
            ln = rng.choice(cands)
            half = rng.choice(("A", "B"))
            mid = nbars // 2
            bars = barlist(ln)
            for b in (range(mid) if half == "B" else range(mid, nbars)):
                bars[b] = "-" * len(bars[b])
            rewrite(ln, bars)
            notes.append(f"{ln} only in the {half} section")
    else:                                    # quiet bar: velocity dip
        b = rng.choice([x for x in (1, 2, nbars - 3) if 0 < x < nbars]
                       or [last])
        for ln in mutable:
            bars = barlist(ln)
            bars[b] = bars[b].replace("X", "x")
            rewrite(ln, bars)
        notes.append(f"bar {b + 1} pulls back (velocity dip)")

    # 4b. every beat gets a breath: hats and colors rest for the back
    # half of one bar while the backbone carries it (sparser, not silent)
    if t in ("bshift", "quietbar"):
        b = rng.choice(late)
        for ln in mutable:
            if ln in backbone:
                continue
            bars = barlist(ln)
            n = len(bars[b])
            bars[b] = bars[b][:n // 2] + "-" * (n - n // 2)
            rewrite(ln, bars)
        notes.append(f"hats sit out the back half of bar {b + 1}")

    # 5. tempo lean (only when he didn't set a tempo himself). A
    # subgenre's tempo is part of its identity (owner rule 2026-07-19):
    # Baltimore club is 130 and leaning it to 124 makes it not-quite-
    # club, a screw beat is 66, reggaeton sits in a narrow band. So the
    # styles lean HALF as far, and only ever by a hair.
    if not tempo_locked:
        lean = rng.choice((-0.02, 0.0, 0.0, 0.02)) \
            if preset.get("genre") \
            else rng.choice((-0.05, -0.03, 0.0, 0.03, 0.05))
        if lean:
            preset["bpm"] = max(TEMPO_LO,
                                min(TEMPO_HI,
                                    int(round(preset["bpm"] * (1 + lean)))))
            notes.append(f"tempo leans to {preset['bpm']}")
    return notes


# Owner call 2026-07-22: "have the kick gate the bass and other
# instruments, 90 percent of the creations regardless of DJ." This
# outranks each DJ's own sidechain number — the old rule was the
# reverse (a DJ's 0.0 meant never duck, and Crate Prophet never did),
# which is exactly the kind of built-in rule the dialog box and the
# house settings are now allowed to overrule.
DUCK_P = 0.9
DUCK_DEFAULT = 0.2               # depth for a DJ who carries none


def apply_duck(preset, rng):
    """Decide this beat's sidechain. Returns the depth applied."""
    if rng.random() < DUCK_P:
        preset["sidechain"] = preset.get("sidechain") or DUCK_DEFAULT
    else:
        preset["sidechain"] = 0.0
    return preset["sidechain"]


def roll_swing(preset, variant, force=None, crew_dj=False):
    """v6 (owner ruling 2026-07-18): swing varies per beat around the
    DJ's home feel — a wide window plus the occasional straight or
    triplet outlier. The whole kit shifts together, so deliberate
    straight-vs-swung lane clashes (New Math) keep their relationship.
    Returns the rolled swing for the README, or None when unchanged.

    crew_dj=True applies the owner's 2026-07-22 rule for the loose nine:
    HALF of their beats have no swing at all. Half of those go further
    and are fully quantized — swing 50 AND every per-lane drag/rush and
    hit-to-hit wobble zeroed, so the beat sits dead on the grid. The
    other half keep that human micro-feel; they are simply unswung.
    Legends and the genre roster are untouched: a producer's pocket and
    a subgenre's feel are their identity, not a house setting."""
    rng = random.Random(variant * 733 + 11)
    lanes = preset["lanes"]
    homes = [spec[2][2] for k, spec in lanes.items()
             if not k.startswith("stamp")]
    if not homes:
        return None
    home = max(set(homes), key=homes.count)

    crew_target = None
    if crew_dj and force is None and not preset.get("genre") \
            and not preset.get("legend"):
        roll = random.Random(variant * 6151 + 29).random()
        if roll < 0.5:                       # half of the nine: no swing
            robotic = roll < 0.25            # ...and half of those, dead
            for k, (pan, gain, (o, j, sw, seed), bars) in list(lanes.items()):
                if k.startswith("stamp"):
                    continue
                lanes[k] = (pan, gain,
                            (0.0, 0.0, 50, seed) if robotic
                            else (o, j, 50, seed), bars)
            return "50 (fully quantized)" if robotic else 50
        # The OTHER half has to actually swing. Without this the normal
        # wander below kept landing back on 50 (a -4 from a home of 54),
        # which made "half with no swing" quietly become 87% of them.
        crew_target = max(52, min(66, home + rng.choice((-2, 0, 0, 2, 4))))
    # legends stay in their producer's pocket (owner rule 2026-07-18):
    # a fixed signature swing when set (Premier 53, Dre 50), otherwise a
    # tight +/-2 wander — no straight/triplet outliers pulling them off
    legend = preset.get("legend")
    fixed = preset.get("legend_swing")
    # a subgenre's swing IS the subgenre (owner rule 2026-07-19): a
    # reggaeton that wanders to 62% stops being one, and Baltimore club
    # is straight or it isn't club. Pinned outright, no outliers.
    if preset.get("genre") and preset.get("genre_swing") is not None:
        fixed = preset["genre_swing"]
    if force is not None:
        target = force
    elif crew_target is not None:
        target = crew_target
    elif fixed is not None:
        target = fixed
    elif legend:
        target = home + rng.choice((-2, 0, 0, 2))
    # owner call 2026-07-21: less swing overall — the crew's wander used
    # to lean hard toward swung (75% of rolls moved off home, up to +/-6,
    # plus a 10% swung-outlier roll up to 66%). Halved on both counts:
    # more rolls stay at home, and the ones that move go less far.
    elif rng.random() < 0.04:
        target = rng.choice((50, 54, 58))
    else:
        target = home + rng.choice((-4, -2, 0, 0, 0, 0, 2, 4))
    target = max(50, min(66, target))
    if target == home:
        return None
    delta = target - home
    for k, (pan, gain, (o, j, sw, seed), bars) in list(lanes.items()):
        if k.startswith("stamp"):
            continue
        lanes[k] = (pan, gain,
                    (o, j, max(50, min(66, sw + delta)), seed), bars)
    return target


def solo_preset(name, variant, bpm, tsig=None, trick=False, dirs=None,
                traditional=False):
    """One DJ's preset for this beat: a FRESH pattern composed from their
    grammar (owner verdict 2026-07-17 — no more one-skeleton mutations),
    tempo override, and the standing rules (New Math goes boom bap on odd
    variants; ~1 beat in 10 skips the sidechain, and since 2026-07-22
    the other 9 duck regardless of what the DJ's own preset says). traditional=True keeps the backbone conventional (owner
    rule 2026-07-18). Returns (preset, style notes)."""
    bb = name == "New Math" and variant % 2 == 1 and not tsig
    if bb:
        p = boom_bap_variant(bpm or 94)
    else:
        p = copy.deepcopy(CREW[name])
        if bpm:
            p["bpm"] = bpm
    p["vel_seed"] = variant
    if dirs and dirs.get("force_mode"):
        for ln in ("snare", "clap"):
            spec = p.get("grammar", {}).get(ln)
            if isinstance(spec, dict) and "modes" in spec:
                spec["modes"] = [[dirs["force_mode"], 1.0]]
    notes = compose(p, name, variant, boom_bap=bb, tsig=tsig, trick=trick,
                    traditional=traditional)
    nine = name not in LEGEND_NAMES and name not in GENRE_NAMES
    got = roll_swing(p, variant, force=(dirs or {}).get("swing"),
                     crew_dj=nine)
    if got:
        notes.append("swing %s" % (got if isinstance(got, str)
                                   else "%d%%" % got))
    roll = random.Random(CREW[name]["num"] * 31 + variant)
    apply_duck(p, roll)
    return p, notes


# which job each lane does in a beat — the unit a collab deals out
LANE_JOB = {"kick": "kick", "snare": "backbeat", "clap": "backbeat",
            "hat": "timekeeper", "snap": "timekeeper"}
JOBS = ("kick", "backbeat", "timekeeper", "color")


def collab_preset(names, variant, bpm, tsig=None, trick=False, dirs=None,
                  traditional=False):
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
        qnotes = compose(q, n, variant, tsig=tsig, trick=trick,
                         traditional=traditional)
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
    if tsig:
        p["tsig"] = list(tsig)
    pan = CREW[host]["lanes"]["stamp"][0]
    p["lanes"]["stamp"] = copy.deepcopy(CREW[host]["lanes"]["stamp"])
    for i, g in enumerate(names[1:]):
        gpan, ggain, gfeel, gbars = CREW[g]["lanes"]["stamp"]
        side = -pan if abs(pan) > 0.05 else 0.3 * (1 if i % 2 == 0 else -1)
        p["lanes"][f"stamp{i + 2}"] = (side, ggain, gfeel, gbars)
    apply_duck(p, random.Random(CREW[host]["num"] * 37 + variant))
    nine = all(n not in LEGEND_NAMES and n not in GENRE_NAMES
               for n in names)
    got = roll_swing(p, variant, force=(dirs or {}).get("swing"),
                     crew_dj=nine)
    if got:
        notes.append("swing %s" % (got if isinstance(got, str)
                                   else "%d%%" % got))
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

# words in the box -> harmony.py progression (punch list step 7,
# 2026-07-22). Naming a mood implies "chords" too, so "dreamy" alone is
# enough — no need to also type "chords".
CHORD_WORDS = ("chords", "chord", "harmony", "harmonize", "melody",
               "in key", "with keys", "add keys")
FEEL_WORDS = {
    "dreamy": "dreamy", "sad": "sad_accepting", "sinking": "sad_sinking",
    "uplifting": "uplifting", "happy": "uplifting",
    "nostalgic": "nostalgic_jazz", "jazzy": "nostalgic_jazz",
    "epic": "epic", "dark": "dark_menacing", "menacing": "dark_menacing",
    "vamp": "vamp_i_VI"}


def parse_directions(notes):
    """Read this click's directions out of the notes text. v6 adds
    space (gated/dry/room/washed), swing (more/straight), time
    signature (3/4, waltz, 6/8), and halftime words."""
    t = " " + (notes or "").lower().replace(",", " ") + " "
    t = t.replace(" 3/4", " 3-4 ").replace(" 6/8", " 6-8 ")
    t = t.replace(".", " ")
    t = " ".join(t.split())
    t = f" {t} "
    out = {"mute": set(), "tags": [], "kick": None, "density": None,
           "space": None, "swing": None, "tsig": None, "force_mode": None,
           "chords": False, "chord_feel": None}
    if any(x in t for x in ("no swing", "straight", "unswung")):
        out["swing"] = 50
    elif "triplet swing" in t:
        out["swing"] = 66
    elif any(x in t for x in ("more swing", "swung", "swingy", "swing")):
        out["swing"] = 62
    if any(x in t for x in ("3-4", "waltz", "three four")):
        out["tsig"] = (3, 4)
    elif any(x in t for x in ("6-8", "six eight", "shuffle feel")):
        out["tsig"] = (6, 8)
    if any(x in t for x in ("half time", "halftime", "half-time")):
        out["force_mode"] = "halftime"
    for word, sp in (("gated", "gated"), ("gate", "gated"),
                     ("dry", "dry"), ("room", "room"), ("roomy", "room"),
                     ("washed", "plate"), ("wet", "plate"),
                     ("plate", "plate"), ("reverb", "plate")):
        if f" {word} " in t:
            out["space"] = sp
            break
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
    out["chord_feel"] = next((slug for word, slug in FEEL_WORDS.items()
                              if f" {word} " in t), None)
    out["chords"] = bool(out["chord_feel"]) \
        or any(f" {w} " in t for w in CHORD_WORDS)
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


def dj_cut(L, R, parts, bar, nbars=BARS):
    """Hard-mute one bar in the finished audio (20 ms fades) — the
    last-resort deepening. Applied to the stems too so the Reason 12
    handoff matches what the WAV plays."""
    barlen = len(L) // nbars
    a, b = bar * barlen, (bar + 1) * barlen
    f = min(int(0.02 * SR), barlen // 4)
    env = np.ones(len(L))
    env[a:b] = 0.0
    env[a - f:a] = np.linspace(1, 0, f)
    env[b:b + f] = np.linspace(0, 1, f)
    parts["stems"] = {ln: (sL * env, sR * env)
                      for ln, (sL, sR) in parts["stems"].items()}
    return L * env, R * env


def _root_sub(variant, secs=0.6):
    """Owner rule 2026-07-18 ("add the root"): a tuned 808 sub for the
    traditional beats — a real synthesized sub on a chosen musical root,
    so the kick has a low note under it. Deterministic per beat; returns
    (note name, mono audio)."""
    note = random.Random(variant * 13 + 7).choice(list(ROOT_HZ))
    return note, sub808(ROOT_HZ[note], secs)


def generate(names, tempo=None, notes="", root=ROOT, shots=None,
             traditional=False, status=lambda msg: None):
    """Render one random beat (solo or collab) into names[0]'s folder.
    Returns (path, report_line). Raises on an empty selection.
    traditional=True (a quarter of every 4+ batch, owner rule
    2026-07-21, was half):
    a common, popular hip-hop beat — conventional kick+snare backbone,
    no exotic meter, and a tuned root 808 sub when the 808 flavor rolls
    (so the sub is present on some but not every traditional beat)."""
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
        # Legends never evolve — their careers are already written
        # (owner rule 2026-07-18); only the loose nine do.
        # (owner rule 2026-07-18); nor do the subgenres — a genre is a
        # tradition, not a career (owner rule 2026-07-19). Only the
        # loose nine evolve.
        crew_names = [n for n in names
                      if n not in LEGEND_NAMES and n not in GENRE_NAMES]
        if crew_names:
            evo_notes = evolution.maybe_evolve(crew_names, status=status)

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

    # one compose + vary per beat — the reroll-until-different kick
    # guard is gone (owner call 2026-07-21: variety comes from the
    # composition itself, not from rejection loops)
    status(f"Composing for {' x '.join(names)}…")
    for _try in range(1):
        variant = random.randrange(2, 10000)
        # v6 time-signature roll (owner ruling 2026-07-18): 80% 4/4,
        # 10% real 3/4 or 6/8, 10% exotic grids inside 4/4. The notes
        # box overrides the roll.
        troll = random.Random(variant * 677 + 3)
        tsig, trick = dirs["tsig"], False
        # traditional beats and pure-legend solos stay in 4/4 — no random
        # 3-4 / 6-8 / exotic-grid rolls (the notes box can still ask).
        # A mixed collab is out of character, so it rolls normally.
        # A pure subgenre solo is locked the same way and for a stronger
        # reason: there is no such thing as a 6/8 Baltimore club record.
        pure_legend = all(n in LEGEND_NAMES for n in names)
        pure_genre = all(n in GENRE_NAMES for n in names)
        # Owner call 2026-07-22: "the library doesn't have to be straight
        # sixteenths — measurements can now vary." The audit found 683 of
        # 702 beats in 4/4 and 94% on one straight-16th grid, so the old
        # 10%/10% roll was far too shy. Odd meter doubles to 20% and the
        # exotic grids inside 4/4 (triplets, quintuplets, 32nd walls)
        # double to 20% — a plain straight-16 4/4 is now 60%, still the
        # single most common thing but no longer four beats in five.
        if tsig is None and not traditional and not pure_legend \
                and not pure_genre:
            r = troll.random()
            if r < 0.20:
                tsig = troll.choice(((3, 4), (6, 8)))
            elif r < 0.40:
                trick = True
        if len(names) == 1:
            preset, style_notes = solo_preset(names[0], variant, bpm,
                                              tsig=tsig, trick=trick,
                                              dirs=dirs,
                                              traditional=traditional)
        else:
            preset, style_notes = collab_preset(names, variant, bpm,
                                                tsig=tsig, trick=trick,
                                                dirs=dirs,
                                                traditional=traditional)
        dnotes = apply_directions(preset, dirs)
        vnotes = evo_notes + style_notes + dnotes + vary_preset(
            preset, variant, CREW[names[0]]["num"],
            tempo_locked=bool(bpm), density=dirs["density"])
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

    # v6 (2026-07-18, supersedes the odd/even alternation): the beat
    # rolls its own space — gated / dry / room / washed plate — and the
    # notes box can pick one outright.
    # EXCEPT the subgenre roster (owner rule 2026-07-19: the styles stay
    # true to the genre and don't have to follow the house rules): the
    # treatment IS part of the style — trip hop lives in that plate,
    # Baltimore club is dry, horrorcore is drowned — so a style keeps the
    # space it declares. His typed direction still overrides.
    if dirs["space"]:
        space = dirs["space"]
    elif preset.get("genre"):
        space = preset["space"][0]
    else:
        space = random.Random(variant * 941 + 7).choices(
            ["gated", "dry", "room", "plate"], [0.35, 0.35, 0.2, 0.1])[0]

    # "add the root" (owner rule 2026-07-18): traditional beats get a
    # tuned 808 sub on a musical root under the kick — about 3 in 5, so
    # the root is a regular feature but "808 is not in everything". It's
    # skipped when the kick already rolled a LONG 808 (that sample is
    # carrying the sub itself; two would just fight). The sub mirrors the
    # final kick line, plays straight, and rides the un-ducked bass path.
    root_note = None
    _ksecs = preset["kit"].get("kick", (None, None, None, 0))[3]
    _klen = max(_ksecs) if isinstance(_ksecs, (tuple, list)) else _ksecs
    _long808 = (preset["kit"].get("kick", (None, None))[1] == "808"
                and _klen > 0.6)
    # the harmony bass (below) already gives a moving, in-key root under
    # the kick — the static single-note 808 would just muddy the low
    # end fighting it, so "chords" skips this and takes the bass job.
    if traditional and "kick" in preset["lanes"] and not _long808 \
            and not dirs["chords"] \
            and random.Random(variant * 577 + 13).random() < 0.75:
        root_note, sub_audio = _root_sub(variant)
        kpan, kgain, (ko, kj, ksw, ks), kbars = preset["lanes"]["kick"]
        preset["lanes"]["sub"] = (0.0, 0.7, (0, 0, ksw, ks + 7),
                                  [b for b in kbars])
        kit["sub"] = sub_audio
        sources["sub"] = "synth 808 sub, root %s" % root_note
        vnotes.append("root: %s (tuned 808 sub under the kick)" % root_note)

    # "chords" / a mood word in the notes box (punch list steps 2+7,
    # 2026-07-22): a real in-key progression, synthesized as a pad +
    # bass and dropped in as extra lanes — same trick as the tuned-808
    # sub above, just one long "one-shot" per chord instead of one hit.
    midi_chords = None
    if dirs["chords"]:
        import chord_synth
        import harmony
        from key_context import KeyContext, SUB_ROOTS
        key_root = random.Random(variant * 353 + 17).choice(SUB_ROOTS)
        key = KeyContext(key_root, "minor")
        prog_name, chords = harmony.compose(
            key, dirs["chord_feel"], rng=random.Random(variant * 419 + 5))
        num, den = preset.get("tsig", (4, 4))
        bar_s = num * (4.0 / den) * 60.0 / preset["bpm"]
        nb = bars_of(preset)
        per_chord = max(1, nb // len(chords))
        midi_chords = []
        for i, chord in enumerate(chords):
            start_bar = i * per_chord
            if start_bar >= nb:
                break
            end_bar = nb if i == len(chords) - 1 else \
                min(start_bar + per_chord, nb)
            dur = (end_bar - start_bar) * bar_s
            bass_note = chord["notes"][0] - 12
            bars_list = ["-" * 16 for _ in range(nb)]
            bars_list[start_bar] = "X" + "-" * 15
            preset["lanes"][f"chord{i}"] = (0.0, 0.5, (0, 0, 50, variant + i),
                                            bars_list)
            preset["lanes"][f"bass{i}"] = (0.0, 0.85, (0, 0, 50, variant + i),
                                           [b for b in bars_list])
            kit[f"chord{i}"] = chord_synth.pad_voice(chord["notes"], dur)
            kit[f"bass{i}"] = chord_synth.bass_voice(bass_note, dur)
            sources[f"chord{i}"] = "synth chord pad, %s (%s)" % (
                chord["chord"], chord["roman"])
            sources[f"bass{i}"] = "synth bass, %s root" % chord["chord"]
            midi_chords.append({"start_sec": start_bar * bar_s,
                                "dur_sec": dur,
                                "notes": chord["notes"] + [bass_note]})
        vnotes.append("chords: %s in %s (%s)" % (
            prog_name, key, ", ".join(c["chord"] for c in chords)))

    status(f"Rendering beat {no} at {preset['bpm']} BPM…")
    nbars = bars_of(preset)
    L, R, lufs, parts = render_crew_beat(names[0], kit, space=space,
                                         preset=preset, want_parts=True)

    def bar_swing(L, R):
        # floor at -30 dB: below that is silence to the ear, and counting
        # digital zero as "dynamics" would inflate the number meaninglessly
        mono = 0.5 * (L + R)
        barlen = len(mono) // nbars
        prof = [max(-30.0, 20 * np.log10(np.sqrt(
            (mono[i * barlen:(i + 1) * barlen] ** 2).mean()) + 1e-12))
            for i in range(nbars)]
        return max(prof) - min(prof)

    swing = bar_swing(L, R)
    cut_bar = None
    # the contrast floor is a CREW rule. A subgenre is allowed to be
    # relentless (owner rule 2026-07-19) — Baltimore club, Miami bass
    # and bounce do not rise and fall, that flatness is the style — so
    # the deepening pass never touches them.
    if swing < 2.5 and not preset.get("genre"):
        # the loop needs SOME rise and fall — but owner rule 2026-07-17:
        # never silence. Thin one bar instead: hats and colors rest, the
        # backbone softens and plays through. One re-render, no DJ-cut.
        deep_bar = random.Random(variant * 31 + CREW[names[0]]["num"]).choice(
            [b for b in (nbars - 4, nbars - 3, nbars - 2) if b >= 1]
            or [max(nbars - 1, 0)])
        for ln, (pan, gain, feel, bars) in list(preset["lanes"].items()):
            # stamp + harmony lanes fire once for a whole chord section,
            # not once a bar like a kick — silencing their one trigger
            # bar would drop the entire chord/bass, not just dip it.
            if ln.startswith(("stamp", "chord", "bass")):
                continue
            bars = list(bars)
            if deep_bar >= len(bars):        # short pattern, nothing to thin
                continue
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
    meter = ""
    if preset.get("tsig") and tuple(preset["tsig"]) != (4, 4):
        meter = " in %d-%d" % tuple(preset["tsig"])
    fname = (f"{no} {' x '.join(names)} {title} Drums "
             f"{preset['bpm']}bpm{meter}.wav")
    path = folder / fname
    if path.exists():                             # never overwrite
        raise RuntimeError(f"{fname} already exists — not overwriting.")
    write_wav24(path, L, R)

    # the Reason 12 handoff (spec 2026-07-16): MIDI + stems with every WAV
    write_midi(path.with_suffix(".mid"), parts["events"], preset["bpm"],
               tsig=tuple(preset.get("tsig", (4, 4))), chords=midi_chords)
    write_stems(folder / f"{no} {' x '.join(names)} {title} Stems",
                parts["stems"], sources=sources)

    # the pattern sheet (owner request 2026-07-22): a readable picture of
    # every lane against the backbeat, so a beat he doesn't like can be
    # diagnosed by eye instead of by ear alone
    from pattern_sheet import write_sheet
    write_sheet(path.with_suffix(".txt"), preset,
                title=path.stem, extra=vnotes)

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
        "root_note": root_note, "traditional": traditional,
        "dj_cut_bar": cut_bar, "parent": None, "date": str(date.today())})

    # remember the picks so these DJs don't repeat themselves (hard rule)
    record_history(lane_parent, sources)

    # post-render variety check (2026-07-17): one cheap look at this DJ's
    # recent window; a warning lands in the README + report, never a block
    import variety
    warn = variety.quick_check(root, names[0])
    if warn:
        vnotes.append(warn)

    tn, td = preset.get("tsig", (4, 4))
    dur = len(L) / SR
    want = bars_of(preset) * tn * (4.0 / td) * 60.0 / preset["bpm"]
    rms = 20 * np.log10(np.sqrt(0.5 * (L ** 2 + R ** 2).mean()) + 1e-12)
    vnotes.append(f"bar swing {swing:.1f} dB")
    from groove import OWNER_TASTE
    # The RMS band is a sanity net tuned on mid-density beats at 88-150.
    # A sparse subgenre breaks that premise honestly: a screw beat is 2-4
    # kicks a bar over a 29-second loop at 66 BPM, so its average sits
    # near -19 while LUFS, peak and duration are all exactly right.
    # Loudness is judged by LUFS; the floor just widens for those.
    rms_floor = -21 if (preset.get("genre")
                        and preset.get("density") == "sparse") else -18
    good = abs(dur - want) < 0.02 and rms_floor < rms < -9 \
        and abs(lufs - OWNER_TASTE["master_lufs"]) < 2.0

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


# ------------------------------------------------- fixed-rhythm test bank
# Owner request 2026-07-21: a control group. Five REAL, well-known hip-hop
# grooves pulled straight from the 174-pattern library, UNTOUCHED — no
# compose(), no vary_preset, no per-beat mutation, the same 16-step bar
# played eight times flat. The only thing a re-roll can change is which
# samples fill kick/snare/hat. If the crew and legends still sound like
# one pattern next to each other, this is the fixed point to check them
# against, since these five are guaranteed to never move.
FIXED_PATTERNS = [
    ("Classic Boom Bap", "Classic Boom-Bap Backbeat", 90),
    ("UK Drill", "UK Drill Sliding 808", 142),
    ("90s New Jack Swing", "R&B 90s New Jack Swing", 108),
    ("West Coast G-Funk", "West Coast G-Funk Bounce", 96),
    ("Memphis Trap", "Memphis Lo-Fi Menace", 132),
]


def _fixed_preset(idx):
    """One of the five reference grooves as a preset: the same bar eight
    times, no fills, no swing, no A/B. `idx` picks FIXED_PATTERNS[idx]."""
    title, lib_name, bpm = FIXED_PATTERNS[idx]
    pat = next(p for p in load_library() if p["name"] == lib_name)
    lanes = {
        ln: (pan, gain, (0, 0, 50, 9000 + idx * 10 + i), [pat[ln]] * BARS)
        for i, (ln, pan, gain) in enumerate((
            ("kick", 0.0, 1.0), ("snare", 0.0, 0.85), ("hat", -0.12, 0.35)))
    }
    kit = dict(
        kick=("kick", None, ["punch", "knock"], (0.2, 0.5)),
        snare=("snare", None, ["crack", "tight"], 1.0),
        hat=("hat", None, ["closed"], 0.5))
    return dict(num=900 + idx, bpm=bpm, lanes=lanes, kit=kit,
               kick_dist=0.0, dust=0.0, vinyl=0, wow=0.0, mix_sat=0.0,
               drive=1.0, sidechain=0.0, space=("dry", []), alt=None,
               title=title)


def generate_fixed(idx, root=ROOT, shots=None, status=lambda msg: None):
    """Render one of the five fixed reference beats. Same rhythm every
    single time — only the kit changes. A direct answer to "can this
    thing actually produce different rhythms, or is it just samples?":
    these five never move, so they're the control group."""
    preset = _fixed_preset(idx)
    if shots is None:
        status("Scanning your sample library…")
        shots = build_shots()
    kit, sources = build_kit(shots, "Fixed Bank", None, variant=idx,
                             avoid=history_avoid(["Fixed Bank"]),
                             preset=preset)
    del kit["stamp"]
    L, R, lufs, parts = render_crew_beat("Fixed Bank", kit, preset=preset,
                                         want_parts=True)
    no = next_number(root)
    folder = root / "Fixed Bank"
    folder.mkdir(parents=True, exist_ok=True)
    title = preset["title"]
    fname = f"{no} {title} Drums {preset['bpm']}bpm.wav"
    path = folder / fname
    if path.exists():
        raise RuntimeError(f"{fname} already exists — not overwriting.")
    write_wav24(path, L, R)
    write_midi(path.with_suffix(".mid"), parts["events"], preset["bpm"])
    write_stems(folder / f"{no} {title} Stems", parts["stems"],
               sources=sources)
    spec_used = {ln: (r, m, w, _resolve_secs(s, preset["num"], idx))
                for ln, (r, m, w, s) in preset["kit"].items()}
    save_recipe(root, no, {
        "file": fname, "folder": "Fixed Bank", "names": ["Fixed Bank"],
        "title": title, "variant": idx, "bpm": preset["bpm"],
        "space": "dry", "preset": preset, "kit_spec": spec_used,
        "kit_paths": {ln: sources[ln] for ln in spec_used},
        "stamp_paths": {}, "stamp_secs": {}, "root_note": None,
        "traditional": False, "dj_cut_bar": None, "parent": None,
        "date": str(date.today())})
    record_history({ln: "Fixed Bank" for ln in spec_used}, sources)
    report = (f"{fname}\n-> Fixed Bank folder (+ MIDI and "
             f"{len(parts['stems'])} stems) | LUFS {lufs:.1f}"
             f"\n   this one: fixed rhythm #{idx + 1} ({title}) — "
             "only the sounds changed, roll again for a new kit")
    return path, report


# ------------------------------------- files, batch state, favorites/trash
# Owner request 2026-07-18: the page plays the current batch and lets him
# drag each track to Favorites or Trash (everything else stays in its DJ
# folder). Triaged files are MOVED, never deleted. The last batch and the
# placements survive closing/relaunching the app and asking for a new
# batch — because the placement IS where the file lives, and the batch is
# remembered in a small state file.


def _load_state():
    try:
        return json.loads(STATE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(s):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=1))


def set_last_batch(nos, root=None):
    """Remember the numbers made in the batch just requested (real
    library only — test/--out renders never touch his state)."""
    if (root or ROOT) != ROOT:
        return
    s = _load_state()
    s["last_batch"] = [int(n) for n in nos]
    _save_state(s)


def append_last_batch(no, root=None):
    if (root or ROOT) != ROOT:
        return
    s = _load_state()
    b = [int(x) for x in s.get("last_batch", [])]
    if int(no) not in b:
        b.append(int(no))
    s["last_batch"] = b
    _save_state(s)


def beat_items(no, root=None):
    """Every file/folder belonging to beat `no` (its wav, its .mid, its
    Stems folder), wherever it currently sits under root."""
    root = Path(root or ROOT)
    pre = f"{no} "
    out = []
    if not root.exists():
        return out
    for p in root.rglob("*"):
        if p.name.startswith(pre) and (
                p.suffix in (".wav", ".mid")
                or (p.is_dir() and p.name.endswith("Stems"))):
            out.append(p)
    return out


def beat_wav(no, root=None):
    for p in beat_items(no, root):
        if p.suffix == ".wav":
            return p
    return None


def beat_location(no, root=None):
    """'favorites' / 'trash' / 'dj' by which top-level folder holds it."""
    root = Path(root or ROOT)
    w = beat_wav(no, root)
    if not w:
        return None
    top = w.relative_to(root).parts[0]
    if top == FAV_DIR:
        return "favorites"
    if top == TRASH_DIR:
        return "trash"
    return "dj"


def beat_dj(no, root=None):
    """Which DJ's folder this beat belongs to (from its recipe, or the
    current path when the recipe predates recipes)."""
    root = Path(root or ROOT)
    try:
        dj = load_recipe(root, no).get("folder")
        if dj:
            return dj
    except Exception:
        pass
    w = beat_wav(no, root)
    if w:
        parts = w.relative_to(root).parts
        if parts and parts[0] not in (FAV_DIR, TRASH_DIR):
            return parts[0]
    return None


def triage(no, dest, root=None):
    """Move beat `no` to Favorites / Trash / its DJ folder. MOVE, never
    delete. Returns the new location string. Idempotent."""
    root = Path(root or ROOT)
    no = int(no)
    items = beat_items(no, root)
    if not items:
        raise FileNotFoundError(f"No beat {no} to move.")
    if dest in ("fav", "favorite", "favorites"):
        target, loc = Path(root) / FAV_DIR, "favorites"
    elif dest in ("trash", "bin", "reject"):
        target, loc = Path(root) / TRASH_DIR, "trash"
    else:                                     # 'dj' — back to their folder
        dj = beat_dj(no, root)
        if not dj:
            raise ValueError(f"Don't know which DJ beat {no} belongs to.")
        target, loc = Path(root) / dj, "dj"
    target.mkdir(parents=True, exist_ok=True)
    for p in items:
        d = target / p.name
        if p.resolve() == d.resolve() or d.exists():
            continue                          # already there / never clobber
        shutil.move(str(p), str(d))
    return loc


def _family_dir_for(no, root):
    """The folder a song and its swap variations share, and the original
    ancestor's number + recipe. Follows the parent chain to the root
    beat (owner rule 2026-07-18: a swapped song and its variations live
    together)."""
    anc = int(no)
    rec = load_recipe(root, anc)
    seen = {anc}
    while rec.get("parent") and int(rec["parent"]) not in seen:
        anc = int(rec["parent"])
        seen.add(anc)
        try:
            rec = load_recipe(root, anc)
        except Exception:
            break
    dj = rec.get("folder", "Misc")
    title = rec.get("title", "Song")
    fam = Path(root) / dj / f"{anc} {title} Variations"
    return fam, anc


# ------------------------------------------------------------- swap flow


def swap(number, lane, root=ROOT, shots=None, status=lambda msg: None,
         pick=None):
    """One drum swapped — the single-lane door into `swap_many`, kept for
    the CLI (`--swap N --lane snare`) and the tests."""
    return swap_many(number, {lane: pick}, root=root, shots=shots,
                     status=status)


def swap_many(number, picks, root=ROOT, shots=None, status=lambda msg: None,
              trims=None, drops=None):
    """Owner spec 2026-07-16 (revision flow), widened 2026-07-18 for the
    stem rack: same beat, ONE OR MORE drums swapped in a single rebuild.
    `picks` maps lane -> the sample path he chose in the dropdown, or
    None to let the machine reach for a different one itself. Pattern,
    groove, tempo, treatment, and every drum he didn't touch come
    straight from the saved recipe. The re-render lands as a NEW numbered
    file; nothing is overwritten.

    Staging several swaps into one rebuild is deliberate (owner
    2026-07-18): changing kick + snare + hat used to mean three renders
    and three new beats to sort through, when he only wanted one.

    `trims` maps lane -> dB (owner request 2026-07-19: set each stem's
    volume when re-rendering). It rides the preset's own per-lane gain —
    the same knob evolutions and collabs already turn — so a trim lands
    on the lane's stem AND its share of the mix, which is what "turn the
    snare up" has to mean. Trims alone are a valid rebuild: no drum has
    to change for a remix to be worth printing.

    `drops` is a list of lanes to REMOVE outright (owner request
    2026-07-21: "just remove a stem completely") — the lane leaves the
    mix, the stems folder, and the child recipe. A drop wins over a
    swap or trim staged on the same lane."""
    number = int(number)
    rec = load_recipe(root, number)
    picks = {str(ln).strip().lower(): v for ln, v in (picks or {}).items()}
    drops = sorted({str(ln).strip().lower() for ln in (drops or [])})
    for lane in list(picks) + drops:
        if lane not in rec["kit_spec"]:
            raise ValueError(f"Beat {number} has no '{lane}' to change — "
                             f"it has: {', '.join(sorted(rec['kit_spec']))}.")
    # picking the sample that's already in the lane isn't a swap
    picks = {ln: v for ln, v in picks.items()
             if not (v and v == rec["kit_paths"].get(ln))}
    preset = normalize_preset(rec["preset"])
    trims = _clean_trims(trims, preset, number)
    for lane in drops:                        # a drop wins over the rest
        picks.pop(lane, None)
        trims.pop(lane, None)
    if set(rec["kit_spec"]) <= set(drops):
        raise ValueError("That would remove every drum — keep at least "
                         "one.")
    if not picks and not trims and not drops:
        raise ValueError("Nothing to change — pick a different sound, "
                         "move a volume slider, or remove a stem first.")
    for lane in drops:
        preset["lanes"].pop(lane, None)
    # bake the trims into this beat's own gains. The child recipe stores
    # the RESULT, so its sliders start at 0 again ("nudge from how it
    # sounds now") and re-rendering it without trims reproduces it.
    for lane, db in trims.items():
        pan, gain, feel, bars = preset["lanes"][lane]
        preset["lanes"][lane] = (pan, gain * 10 ** (db / 20.0), feel, bars)
    names = rec["names"]
    if shots is None:
        status("Scanning your sample library…")
        shots = build_shots()

    avoid = set(p for p in rec["kit_paths"].values() if p)
    avoid |= set(rec["stamp_paths"].values())
    avoid |= history_avoid(names)

    kit_paths, fresh, olds = dict(rec["kit_paths"]), {}, {}
    for lane in drops:
        kit_paths.pop(lane, None)
    for lane in sorted(picks):
        role, must, wants, secs = rec["kit_spec"][lane]
        olds[lane] = rec["kit_paths"].get(lane)
        chosen = picks[lane]
        if chosen:                              # he picked this one himself
            x = _load_choked(chosen, secs)
            if x is None:
                raise RuntimeError(f"{Path(chosen).name} wouldn't load — "
                                   "pick another one.")
            new_path = chosen
        else:                                   # surprise me
            status(f"Picking a different {lane}…")
            new_path, x = _pick_path(shots, role, wants, secs,
                                     random.randrange(1, 1 << 30),
                                     must=must, avoid=avoid)
            if not new_path or new_path == olds[lane]:
                raise RuntimeError(f"The library has no other {lane} to "
                                   "reach for.")
        kit_paths[lane] = new_path
        fresh[lane] = x
        avoid.add(new_path)          # two swapped lanes never land together

    kit = {}
    for ln, pth in kit_paths.items():
        snd = (fresh[ln] if ln in fresh
               else _load_choked(pth, rec["kit_spec"][ln][3]))
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
    # the tuned root sub is synthesized, not a sample — rebuild it from
    # the recipe's root note so the swapped beat keeps its low end
    if rec.get("root_note") and "sub" in preset.get("lanes", {}):
        kit["sub"] = sub808(ROOT_HZ.get(rec["root_note"], 43.65), 0.6)

    lanes = sorted(picks)
    if drops and not lanes and not trims:      # removal is the headline
        what = "No " + " & ".join(d.capitalize() for d in drops)
        changed = "removed " + " and ".join(drops)
    elif drops:
        what = "Rebuilt"
        changed = ("removed " + " and ".join(drops)
                   + (", new " + ", ".join(lanes) if lanes else ""))
    elif not lanes:                   # volumes only — same drums, new mix
        what, changed = "New Mix", _trim_words(trims)
    elif len(lanes) == 1:
        what, changed = f"New {lanes[0].capitalize()}", lanes[0]
    elif len(lanes) == 2:
        what = f"New {lanes[0].capitalize()} & {lanes[1].capitalize()}"
        changed = " and ".join(lanes)
    else:
        what, changed = "Rebuilt", ", ".join(lanes)
    status(f"Re-rendering beat {number} with the new {changed}…")
    L, R, lufs, parts = render_crew_beat(names[0], kit, space=rec["space"],
                                         preset=preset, want_parts=True)
    if rec.get("dj_cut_bar") is not None:
        L, R = dj_cut(L, R, parts, rec["dj_cut_bar"])

    no = next_number(root)
    # a swapped song and its variations live together (owner rule
    # 2026-07-18): the whole family gets its own folder under the DJ, and
    # the original is pulled in the first time — unless he's already
    # filed it in Favorites/Trash, which we leave alone.
    folder, anc = _family_dir_for(number, root)
    folder.mkdir(parents=True, exist_ok=True)
    if beat_location(anc, root) == "dj":
        for p in beat_items(anc, root):
            dst = folder / p.name
            if p.parent.resolve() != folder.resolve() and not dst.exists():
                shutil.move(str(p), str(dst))
    stem_of = f"{' x '.join(names)} {rec['title']} {what}"
    fname = f"{no} {stem_of} Drums {preset['bpm']}bpm.wav"
    path = folder / fname
    if path.exists():                             # never overwrite
        raise RuntimeError(f"{fname} already exists — not overwriting.")
    write_wav24(path, L, R)
    write_midi(path.with_suffix(".mid"), parts["events"], preset["bpm"])
    write_stems(folder / f"{no} {stem_of} Stems", parts["stems"],
                sources={**kit_paths, **rec["stamp_paths"]})

    rec2 = dict(rec, file=fname, kit_paths=kit_paths, parent=number,
                folder=rec["folder"], date=str(date.today()))
    if drops:                    # the lane is gone from the child recipe
        rec2["kit_spec"] = {ln: s for ln, s in rec["kit_spec"].items()
                            if ln not in drops}
    if trims or drops:           # the new gains/lanes ARE this beat
        rec2["preset"] = preset
    save_recipe(root, no, rec2)
    append_last_batch(no, root)                   # show up in the player
    lane_parent = preset.get("lane_parent", {})
    record_history({ln: lane_parent.get(ln, names[0]) for ln in lanes},
                   {ln: kit_paths[ln] for ln in lanes})

    with open(root / "README.txt", "a") as f:
        f.write(f"\nBEAT MACHINE — {date.today()}\n"
                f"{fname}  ->  {rec['folder']}/  (+ .mid and a Stems "
                f"folder)\n"
                f"  swap of beat {number} ({rec['file']}): same beat, "
                f"different {changed}\n")
        for ln in lanes:
            f.write(f"  {ln} was: "
                    f"{Path(olds[ln]).name if olds[ln] else '(none)'}\n"
                    f"  {ln} now: {Path(kit_paths[ln]).name}\n")
        if trims:
            f.write(f"  volumes: {_trim_words(trims)}\n")
        f.write(f"  LUFS {lufs:.1f}\n")
    bits = [f"{ln} → {Path(kit_paths[ln]).name}" for ln in lanes]
    if trims:
        bits.append(_trim_words(trims))
    report = (f"{fname}\n-> {rec['folder']} folder | same beat as "
              f"{number} | {' | '.join(bits)} | LUFS {lufs:.1f}")
    return path, report


# ------------------------------------------------ web helpers (player etc.)


def _batch_beats(root=None):
    """The last batch's tracks with their current location, for the
    player. Missing files (moved by hand) are skipped."""
    root = Path(root or ROOT)
    beats = []
    for no in _load_state().get("last_batch", []):
        w = beat_wav(no, root)
        if w:
            beats.append({"no": int(no), "label": w.stem,
                          "loc": beat_location(no, root)})
    return beats


def _swap_lanes(no, root=None):
    """Every drum in this beat that can be swapped — read straight from
    the recipe, so guest colors (congas2, exotic2, blips, fx…) and the
    tuned sub all show up, not a fixed list. Stamps stay locked."""
    rec = load_recipe(Path(root or ROOT), int(no))
    return [ln for ln in sorted(rec["kit_spec"])
            if ln != "stamp" and not ln.startswith("stamp")]


# ---- the stem rack: see every drum in a beat, swap them per sound ----
# Owner request 2026-07-18. The recipe already knows which sample file is
# behind every lane, and write_stems already saved an isolated wav per
# lane with the real sample name — so the rack is mostly wiring, and
# soloing one drum comes free.

LANE_ORDER = ("kick", "sub", "snare", "clap", "snap", "rim", "hat", "ohat",
              "ride", "crash", "perc", "shaker", "tamb", "woods", "conga",
              "congas", "congas2", "exotic", "exotic2", "blips", "fx")


def _lane_sort(lane):
    """Drums in the order a drummer would name them, strays alphabetical."""
    try:
        return (0, LANE_ORDER.index(lane), lane)
    except ValueError:
        return (1, 0, lane)


# How far a stem's volume slider swings either way (owner call
# 2026-07-21: widened from +/-12 — more throw on the fader; at -24 dB a
# stem is all but gone, and the remove button finishes the job).
TRIM_DB = 24.0


def _clean_trims(trims, preset, number):
    """The volume sliders, checked: lane -> dB, clamped to +/-TRIM_DB.
    A slider left in the middle is not a change, so 0 dB drops out and a
    rack full of untouched sliders still counts as 'nothing staged'."""
    out = {}
    for lane, db in (trims or {}).items():
        lane = str(lane).strip().lower()
        try:
            db = float(db)
        except (TypeError, ValueError):
            raise ValueError(f"'{db}' isn't a volume for the {lane}.")
        if db != db or db in (float("inf"), float("-inf")):   # NaN/inf
            raise ValueError(f"'{db}' isn't a volume for the {lane}.")
        if lane not in preset.get("lanes", {}):
            raise ValueError(f"Beat {number} has no '{lane}' to turn up "
                             "or down.")
        db = round(max(-TRIM_DB, min(TRIM_DB, db)), 2)
        if db:
            out[lane] = db
    return out


def _trim_words(trims):
    """'kick +2 dB, snare -3.5 dB' — how a trim reads in the log."""
    return ", ".join(f"{ln} {db:+g} dB"
                     for ln, db in sorted(trims.items(), key=lambda kv:
                                          _lane_sort(kv[0])))


# words that describe a DRUM, not a pack. A folder built only out of
# these ("Snares", "Open Hat", "Drum n Percussion One Shot", "120BPM")
# is a sorting shelf inside a pack, so _pack_of walks straight past it.
_GENERIC_WORDS = {
    "kick", "kicks", "snare", "snares", "clap", "claps", "snap", "snaps",
    "hat", "hats", "hihat", "hihats", "hi", "open", "closed", "perc",
    "percs", "percussion", "808", "808s", "sub", "subs", "fx", "sfx",
    "one", "shot", "shots", "oneshot", "oneshots", "drum", "drums", "kit",
    "kits", "cymbal", "cymbals", "crash", "crashes", "ride", "rides",
    "tom", "toms", "rim", "rims", "shaker", "shakers", "tamb", "tambourine",
    "sample", "samples", "sound", "sounds", "wav", "wavs", "misc", "other",
    "extras", "processed", "dry", "wet", "top", "tops", "loop", "loops",
    "and", "n", "the", "bpm", "vol", "pack",
}


def _is_shelf(name):
    """True when a folder name says only which drum is inside it."""
    toks = [t for t in re.split(r"[^a-z0-9]+", name.lower()) if t]
    return not [t for t in toks
                if t not in _GENERIC_WORDS
                and not re.match(r"^\d+(bpm)?$", t)]


def _pack_of(path):
    """Which sample pack a one-shot came from, so the dropdown can group
    by pack instead of showing one flat list of 400 kicks. Walks up past
    the drum-name folders ("Snares", "808s") to the first folder that
    actually names a pack — a collection folder like "reddit drum kits
    2023" holds dozens of packs, so stopping at the root's first level
    would lump nearly everything together."""
    if not path:
        return ""
    try:
        from sample_library import load_roots
        roots = load_roots()
    except Exception:
        roots = []
    p = Path(path)
    for r in roots:
        try:
            rel = p.relative_to(r)
        except ValueError:
            continue
        dirs = list(rel.parts[:-1])
        while len(dirs) > 1:
            if not _is_shelf(dirs[-1]):
                return dirs[-1]
            dirs.pop()
        return dirs[0] if dirs else Path(r).name
    return p.parent.name


def _stems_dir(no, root=None):
    """Where beat `no` keeps its per-drum wavs, if it has them."""
    for p in beat_items(no, root):
        if p.is_dir() and p.name.endswith("Stems"):
            return p
    return None


def _stem_wav(no, lane, root=None, folder=None):
    """The isolated wav for one lane — 'kick - Real Name.wav' on beats
    made since the rename, plain 'kick.wav' on the older ones. Pass
    `folder` to skip the library walk when the caller already found it."""
    folder = folder if folder is not None else _stems_dir(no, root)
    if not folder:
        return None
    for f in sorted(folder.glob("*.wav")):
        if f.stem == lane or f.stem.startswith(lane + " - "):
            return f
    return None


def _beat_stems(no, root=None):
    """Every drum in a beat: the real sample behind it, whether it can be
    swapped, and whether there's a solo stem to play. Stamps are the DJ's
    producer tag — shown, but locked (crew rule)."""
    root = Path(root or ROOT)
    no = int(no)
    rec = load_recipe(root, no)
    out = []
    # stamps live outside kit_spec but are still part of the beat — he
    # should SEE his producer tag even though he can't swap it
    lanes = list(rec["kit_spec"]) + [ln for ln in rec.get("stamp_paths", {})
                                     if ln not in rec["kit_spec"]]
    folder = _stems_dir(no, root)     # walk the library once, not per lane
    for lane in sorted(lanes, key=_lane_sort):
        locked = lane == "stamp" or lane.startswith("stamp")
        path = (rec["stamp_paths"] if locked else rec["kit_paths"]).get(lane)
        spec = rec["kit_spec"].get(lane)
        out.append({
            "lane": lane,
            "role": spec[0] if spec else lane,
            "sample": Path(path).stem if path else "built from scratch",
            "pack": _pack_of(path),
            "locked": locked or not path,
            "why": ("the DJ's producer tag — same in every beat they make"
                    if locked else
                    "synthesised, not a sample" if not path else ""),
            "stem": bool(_stem_wav(no, lane, root, folder=folder)),
        })
    return out


def _lane_candidates(no, lane, shots=None, root=None):
    """Every sample in the library that could fill this lane, grouped by
    pack for the dropdown. Also the allow-list the rebuild validates
    against: a path the client sends back is only ever accepted if it
    came from here, so no client string reaches disk unchecked."""
    root = Path(root or ROOT)
    rec = load_recipe(root, int(no))
    lane = str(lane).strip().lower()
    if lane not in rec["kit_spec"]:
        raise ValueError(f"Beat {no} has no '{lane}'.")
    if lane == "stamp" or lane.startswith("stamp"):
        raise ValueError("The producer tag stays locked.")
    role = rec["kit_spec"][lane][0]
    shots = shots if shots is not None else build_shots()
    current = rec["kit_paths"].get(lane)
    seen, out = set(), []
    for e in shots.get(role, []):
        p = e.get("path")
        if not p or p in seen:
            continue
        seen.add(p)
        out.append({"path": p, "name": Path(p).stem, "pack": _pack_of(p),
                    "current": p == current})
    out.sort(key=lambda d: (d["pack"].lower(), d["name"].lower()))
    return out


def _traditional_flags(how_many, names=None):
    """A quarter of a 4+ batch is a common, traditional hip-hop beat
    (owner rule 2026-07-21: was half since 2026-07-18, but at half the
    whole library converged on the plain 2&4 backbone), interleaved so
    they're not all up front."""
    if how_many < 4:
        return [False] * how_many
    k = how_many // 4
    flags = [True] * k + [False] * (how_many - k)
    random.shuffle(flags)
    return flags


# --------------------------------------------------------------- web GUI
# macOS ships Apple's deprecated, half-broken Tk 8.5.9 — plain labels and
# text fields never paint, and the themed ttk widgets don't paint at all
# on this machine. So Homeroom Studio is a tiny LOCAL web page instead
# (stdlib http.server, no installs): the browser renders it perfectly,
# and it matches the Reason Voice localhost-UI workflow he already uses.

_CACHE = {}

_PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homeroom Studio</title>
<style>
 /* ---------------------------------------------------------------
    Homeroom Studio — owner brief 2026-07-18: hip hop, a little graffiti,
    nothing goofy. Dark xerox paper, heavy condensed type doing the
    shouting, the band's yellow and blue carrying every accent, and
    the marker/stencil marks kept to four placements so the page reads
    designed instead of stickered.
    ---------------------------------------------------------------- */
 :root {
   --paper:   #0b0b0d;
   --card:    #141417;
   --card2:   #1b1b1f;
   --line:    #ffffff16;
   --line2:   #ffffff28;
   --text:    #f2f0eb;
   --dim:     #f2f0eb99;
   --dimmer:  #f2f0eb5c;
   /* straight off the Back of the Class mark: the yellow scrawl and the
      blue square it sits on. The blue is deep enough to use as a BLOCK
      but too dark to read as text on black, so --co is a lifted tint of
      it for type, borders and small accents.                          */
   --hi:      #e8d810;   /* band yellow — actions, keeps, selection    */
   --hi-ink:  #16150a;
   --blue:    #1020a8;   /* band blue — masthead, fills, blocks        */
   --co:      #7d8cff;   /* the same blue, lifted so it reads on black */
   --no:      #ff4d4d;   /* trash + real errors only                   */
   --ch:      #e9e6dc;   /* chalk — the subgenre box's selection       */
   --display: "Avenir Next Condensed", "HelveticaNeue-CondensedBold",
              Impact, "Haettenschweiler", sans-serif;
   --mono:    ui-monospace, "SF Mono", Menlo, monospace;
 }
 * { box-sizing: border-box; }
 html { -webkit-text-size-adjust: 100%; }
 body {
   font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif;
   margin: 0; padding: 0 24px 90px; background: var(--paper);
   color: var(--text); line-height: 1.5;
   -webkit-font-smoothing: antialiased;
 }
 /* photocopy grain — one inline SVG, no downloads, sits over everything */
 body::before {
   /* no mix-blend-mode: a full-screen blended layer makes the whole page
      recomposite on every scroll, and plain low opacity looks the same */
   content: ""; position: fixed; inset: 0; z-index: 9; pointer-events: none;
   opacity: .035;
   background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E");
 }
 .wrap { max-width: 1120px; margin: 0 auto; position: relative; z-index: 1; }

 /* ------------------------------------------------------- masthead */
 /* the masthead is the band's blue square, blown up: the mark sits on
    the same field it was drawn on, so his logo lands in it seamlessly */
 .board { background: var(--blue); border-radius: 18px; margin: 22px 0 0;
          padding: 26px 30px; position: relative; overflow: hidden; }
 .board::after {                       /* chalk-dust wash, keeps it flat-free */
   /* thrown to the RIGHT on purpose: the logo's own blue is exactly
      --blue, so any highlight behind it turns the artwork into a
      visible square instead of letting it melt into the board */
   content: ""; position: absolute; inset: 0; pointer-events: none;
   background: radial-gradient(110% 90% at 92% 0%, #ffffff1c, transparent 58%); }
 header { display: grid; grid-template-columns: auto minmax(0, 1fr);
          gap: 0 20px; align-items: center; position: relative; z-index: 1; }
 .mark { width: 108px; height: 108px; flex: none; display: grid;
         place-items: center; overflow: hidden; background: var(--blue); }
 .mark img { width: 100%; height: 100%; object-fit: contain; }
 .mark span { font-family: var(--display); font-weight: 700; font-size: 25px;
              letter-spacing: .04em; color: var(--hi); }
 /* no band name in type up here — the mark already says it (owner
    2026-07-18: "I agree about the redundant title, don't use it") */
 h1 { font-family: var(--display); font-weight: 700;
      font-size: clamp(38px, 6vw, 66px); line-height: .86;
      letter-spacing: .012em; margin: 0; text-transform: uppercase;
      color: #fff; }
 .scrawl { display: block; width: min(330px, 80%); height: 13px;
           margin: 8px 0 0; overflow: visible; }
 .scrawl path { fill: none; stroke: var(--hi); stroke-width: 5;
                stroke-linecap: round; }
 .tag { grid-column: 2; margin: 12px 0 0; color: #ffffffc4;
        max-width: 62ch; font-size: 14.5px; }

 /* -------------------------------------------------- section heads */
 h2.box { font-family: var(--display); font-weight: 700; font-size: 20px;
          letter-spacing: .1em; text-transform: uppercase;
          margin: 34px 0 12px; display: flex; align-items: center; gap: 11px; }
 h2.box::before {                       /* stencil bars */
   content: ""; width: 26px; height: 13px; flex: none; border-radius: 2px;
   background: repeating-linear-gradient(90deg, var(--hi) 0 4px,
               transparent 4px 8px);
 }
 h2.box small { font-family: -apple-system, sans-serif; font-weight: 400;
                font-size: 12.5px; letter-spacing: .02em; color: var(--dimmer);
                text-transform: none; }

 /* ------------------------------------------------------ DJ crates */
 .djs { display: grid; grid-template-columns: repeat(auto-fill, minmax(212px, 1fr));
        gap: 9px; }
 .fixedbank { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
              gap: 9px; margin-bottom: 6px; }
 .fixedbtn { padding: 11px 13px; border: 1px solid var(--line); border-radius: 11px;
             background: var(--card); cursor: pointer; text-align: left;
             font-family: var(--display); font-weight: 600; font-size: 15px;
             color: var(--text); transition: border-color .13s, transform .13s; }
 .fixedbtn:hover { border-color: var(--hi); transform: translateY(-1px); }
 .fixedbtn:disabled { opacity: .5; cursor: default; transform: none; }
 .fixedbtn small { display: block; font-weight: 400;
                   font-size: 12px; color: var(--dim); text-transform: none;
                   letter-spacing: 0; margin-top: 3px; }
 .dj { position: relative; display: flex; align-items: center; gap: 10px;
       padding: 11px 13px; border: 1px solid var(--line); border-radius: 11px;
       background: var(--card); cursor: pointer; user-select: none;
       transition: border-color .13s, background .13s, transform .13s; }
 .dj:hover { border-color: var(--line2); transform: translateY(-1px); }
 .dj input { position: absolute; opacity: 0; pointer-events: none; }
 .dj .dot { width: 11px; height: 11px; border-radius: 50%; flex: none;
            border: 2px solid var(--line2); transition: all .13s; }
 .dj .who { flex: 1; min-width: 0; }
 .dj .name { display: block; font-family: var(--display); font-weight: 600;
             font-size: 18.5px; line-height: 1.12; letter-spacing: .028em;
             text-transform: uppercase; white-space: nowrap; overflow: hidden;
             text-overflow: ellipsis; }
 .dj .built { display: block; font-size: 11.5px; color: var(--dimmer);
              white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 .dj .bpm { font-family: var(--mono); font-size: 10.5px; color: var(--dimmer);
            border: 1px solid var(--line); border-radius: 5px;
            padding: 2px 5px; flex: none; }
 .dj .ord { position: absolute; top: -7px; right: -7px; width: 21px;
            height: 21px; border-radius: 50%; display: none;
            place-items: center; font-family: var(--mono); font-size: 11px;
            font-weight: 700; background: var(--hi); color: var(--hi-ink); }
 .dj:has(input:checked) { border-color: var(--hi); background: #e8d81014; }
 .dj:has(input:checked) .dot { background: var(--hi); border-color: var(--hi); }
 .dj:has(input:checked) .ord { display: grid; }
 .dj.legend:has(input:checked) { border-color: var(--co); background: #7d8cff17; }
 .dj.legend:has(input:checked) .dot { background: var(--co); border-color: var(--co); }
 .dj.legend:has(input:checked) .ord { background: var(--co); color: #fff; }
 /* the third box gets CHALK rather than a fourth hue — the mark only
    owns yellow and blue, and chalk on a board is the one other colour
    this band already has (crew = yellow scrawl, legends = blue, styles
    = chalk). */
 .dj.genre:has(input:checked) { border-color: var(--ch); background: #f2f0eb12; }
 .dj.genre:has(input:checked) .dot { background: var(--ch); border-color: var(--ch); }
 .dj.genre:has(input:checked) .ord { background: var(--ch); color: #16150a; }
 .dj.genre .built { font-style: italic; }

 /* ------------------------------------------------------- controls */
 .panel { margin-top: 24px; padding: 20px 22px; border: 1px solid var(--line);
          border-radius: 14px; background: var(--card); }
 .fields { display: grid; grid-template-columns: 132px 132px 1fr; gap: 16px; }
 .field label { display: block; font-family: var(--display); font-weight: 600;
                font-size: 12.5px; letter-spacing: .11em; text-transform: uppercase;
                color: var(--dim); margin-bottom: 6px; }
 .field input, .field select { width: 100%; font-size: 15px; padding: 10px 12px;
                border-radius: 9px; border: 1px solid var(--line2);
                background: #0000004d; color: var(--text); font-family: inherit; }
 .field input:focus, .field select:focus { outline: none; border-color: var(--hi); }
 .field.quick { margin-top: 16px; }
 .field .hint { font-size: 11.5px; color: var(--dimmer); margin-top: 5px; }
 .fire { display: flex; align-items: center; gap: 16px; margin-top: 18px;
         flex-wrap: wrap; }
 #go { position: relative; font-family: var(--display); font-weight: 700;
       font-size: 21px; letter-spacing: .07em; text-transform: uppercase;
       padding: 13px 30px; border: 0; border-radius: 10px;
       background: var(--hi); color: var(--hi-ink); cursor: pointer;
       transition: transform .1s; }
 #go::after {                            /* sticker shadow, marker-ish */
   content: ""; position: absolute; inset: 0; border-radius: 10px;
   border: 2px solid var(--text); opacity: .17;
   transform: translate(4px, 4px) rotate(-.5deg); pointer-events: none; }
 #go:hover:not(:disabled) { transform: translate(-1px, -1px); }
 #go:disabled { opacity: .45; cursor: default; }
 #hosthint { color: var(--dim); font-size: 13.5px; flex: 1; min-width: 180px; }

 /* the working strip — replaces the old green wall of filenames */
 #work { margin-top: 16px; display: none; }
 #work.on { display: block; }
 #workbar { height: 4px; border-radius: 3px; background: var(--line);
            overflow: hidden; }
 #workbar i { display: block; height: 100%; width: 34%; border-radius: 3px;
              background: var(--hi); animation: slide 1.15s ease-in-out infinite; }
 @keyframes slide { 0% { margin-left: -34%; } 100% { margin-left: 100%; } }
 #worktext { margin-top: 9px; font-size: 13.5px; color: var(--dim); }
 #work.bad #workbar { display: none; }
 #work.bad #worktext { color: var(--no); white-space: pre-wrap; }

 /* --------------------------------------------------- batch + bins */
 .zones { display: grid; grid-template-columns: repeat(3, 1fr); gap: 11px;
          margin: 14px 0 16px; }
 .zone { border: 1.5px dashed var(--line2); border-radius: 12px;
         padding: 15px 12px; text-align: center;
         font-family: var(--display); font-weight: 600; font-size: 15.5px;
         letter-spacing: .07em; text-transform: uppercase; color: var(--dim);
         transition: background .12s, border-color .12s, color .12s; }
 .zone small { display: block; font-family: -apple-system, sans-serif;
               font-weight: 400; font-size: 11.5px; letter-spacing: 0;
               text-transform: none; color: var(--dimmer); margin-top: 3px; }
 .zone.fav.over   { border-color: var(--hi); background: #e8d8101f; color: var(--hi); }
 .zone.djz.over   { border-color: var(--co); background: #7d8cff1f; color: var(--co); }
 .zone.trash.over { border-color: var(--no); background: #ff4d4d1f; color: var(--no); }

 #empty { padding: 34px 0 10px; text-align: center; position: relative; }
 #empty .ghost { width: 132px; margin: 0 auto 4px; opacity: .13;
                 transform: rotate(-3deg); }
 #empty .ghost img { width: 100%; display: block; }
 #empty .scribble { font-family: var(--display); font-weight: 700;
                    font-size: 38px; letter-spacing: .04em; color: #ffffff12;
                    text-transform: uppercase; transform: rotate(-2.5deg);
                    display: inline-block; }
 #empty p { color: var(--dimmer); font-size: 13.5px; margin: 6px 0 0; }

 /* ------------------------------------------------------ the track */
 .track { position: relative; border: 1px solid var(--line); border-radius: 13px;
          background: var(--card); margin: 9px 0; overflow: hidden;
          transition: border-color .13s; }
 .track.dragging { opacity: .35; }
 .track.loc-favorites { border-color: #e8d81066; }
 .track.loc-trash { border-color: #ff4d4d55; opacity: .62; }
 .thead { display: flex; align-items: center; gap: 13px; padding: 12px 14px;
          cursor: grab; }
 .thead .no { font-family: var(--display); font-weight: 700; font-size: 27px;
              color: var(--dimmer); flex: none; min-width: 46px; }
 .track.loc-favorites .thead .no { color: var(--hi); }
 .tmeta { flex: 1; min-width: 0; }
 .tname { display: block; font-family: var(--display); font-weight: 600; font-size: 19px;
          letter-spacing: .026em; text-transform: uppercase;
          white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 .tsub { display: block; font-size: 11.5px; color: var(--dimmer); font-family: var(--mono);
         white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 /* the browser's own audio control is a white pill — it wrecked the
    page, and it can't be restyled, so the track gets its own transport */
 .thead audio { display: none; }
 .player { display: flex; align-items: center; gap: 10px; flex: none;
           width: 238px; }
 .pp { width: 33px; height: 33px; flex: none; border-radius: 50%;
       border: 1px solid var(--line2); background: #ffffff0a;
       color: var(--text); cursor: pointer; font-size: 11px;
       display: grid; place-items: center; transition: all .12s; }
 .pp:hover { background: #ffffff1c; }
 .pp.on { background: var(--hi); border-color: var(--hi); color: var(--hi-ink); }
 .bar { flex: 1; height: 5px; border-radius: 3px; background: var(--line2);
        cursor: pointer; position: relative; }
 .bar i { position: absolute; left: 0; top: 0; bottom: 0; width: 0;
          background: var(--hi); border-radius: 3px; }
 .time { font-family: var(--mono); font-size: 10.5px; color: var(--dimmer);
         min-width: 36px; text-align: right; }
 .acts { display: flex; gap: 4px; flex: none; }
 .acts button, .stembtn { font-size: 14px; line-height: 1; padding: 7px 9px;
       border: 1px solid var(--line); border-radius: 8px; cursor: pointer;
       background: #ffffff08; color: var(--text); transition: all .12s; }
 .acts button:hover { background: #ffffff17; }
 .acts button.on-fav   { border-color: var(--hi); color: var(--hi); }
 .acts button.on-trash { border-color: var(--no); color: var(--no); }
 .stembtn { font-family: var(--display); font-weight: 600; font-size: 12.5px;
            letter-spacing: .09em; text-transform: uppercase; padding: 8px 12px;
            white-space: nowrap; }
 .stembtn.open { background: var(--hi); color: var(--hi-ink); border-color: var(--hi); }

 /* -------------------------------------------------- the stem rack */
 .rack { display: none; border-top: 1px solid var(--line);
         background: #00000038; padding: 4px 14px 14px; }
 .rack.open { display: block; }
 .lane { display: grid; grid-template-columns: 74px 1fr auto auto;
         gap: 12px; align-items: center; padding: 10px 0;
         border-bottom: 1px solid #ffffff0c; }
 .lane:last-of-type { border-bottom: 0; }
 .lane .who2 { display: flex; align-items: center; gap: 7px; }
 .lane .swatch { width: 3px; height: 17px; border-radius: 2px;
                 background: var(--co); flex: none; }
 .lane.locked .swatch { background: var(--dimmer); }
 .lane.changed .swatch { background: var(--hi); }
 .lane .lname { font-family: var(--display); font-weight: 600; font-size: 14px;
                letter-spacing: .1em; text-transform: uppercase; }
 .lane .what { min-width: 0; }
 .lane .sample { display: block; font-size: 13px; white-space: nowrap;
                 overflow: hidden; text-overflow: ellipsis; }
 .lane .pack { display: block; font-size: 11px; color: var(--dimmer);
               font-family: var(--mono); white-space: nowrap;
               overflow: hidden; text-overflow: ellipsis; }
 .lane.changed .sample { color: var(--hi); }
 .lane .picks { display: flex; align-items: center; gap: 6px; flex: none; }
 .lane select { appearance: none; -webkit-appearance: none;
       font-family: inherit; font-size: 12.5px; max-width: 250px;
       padding: 7px 26px 7px 10px; border-radius: 8px;
       border: 1px solid var(--line2); background: var(--card2);
       color: var(--text); cursor: pointer;
       background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='7'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%23f2f0eb99' stroke-width='1.6' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
       background-repeat: no-repeat; background-position: right 9px center; }
 .lane select:focus { outline: none; border-color: var(--hi); }
 .lane.changed select { border-color: var(--hi); }
 .lane .mini { font-size: 13px; line-height: 1; padding: 7px 8px;
       border: 1px solid var(--line); border-radius: 8px; cursor: pointer;
       background: #ffffff08; color: var(--text); }
 .lane .mini:hover { background: #ffffff17; }
 .lane .mini.playing { border-color: var(--co); color: var(--co); }
 .lane .lock { font-size: 11.5px; color: var(--dimmer); font-style: italic; }

 /* the stem faders — one per lane, so the rack reads down like a mixer */
 .lane .vol { display: flex; align-items: center; gap: 8px; flex: none; }
 .lane .vol input { -webkit-appearance: none; appearance: none; width: 96px;
       height: 3px; border-radius: 2px; background: var(--line2);
       cursor: pointer; outline: none; }
 .lane .vol input::-webkit-slider-thumb { -webkit-appearance: none;
       appearance: none; width: 13px; height: 13px; border-radius: 50%;
       background: var(--text); cursor: pointer; border: 0; }
 .lane .vol input::-moz-range-thumb { width: 13px; height: 13px;
       border-radius: 50%; background: var(--text); cursor: pointer;
       border: 0; }
 .lane.trimmed .vol input { background: var(--hi); }
 .lane.trimmed .vol input::-webkit-slider-thumb { background: var(--hi); }
 .lane.trimmed .vol input::-moz-range-thumb { background: var(--hi); }
 .lane .vol .db { font-family: var(--mono); font-size: 11.5px;
       color: var(--dimmer); width: 34px; text-align: right; }
 .lane.trimmed .vol .db { color: var(--hi); }
 .lane.trimmed .swatch { background: var(--hi); }
 /* a stem staged for removal reads as struck-through and faded */
 .lane.dropped .who2, .lane.dropped .what, .lane.dropped .vol {
   opacity: .35; text-decoration: line-through; }

 .rackfoot { display: flex; align-items: center; gap: 14px; padding: 13px 0 3px;
             border-top: 1px solid var(--line); margin-top: 4px; flex-wrap: wrap; }
 .rackfoot .staged { font-size: 12.5px; color: var(--dim); flex: 1;
                     min-width: 150px; }
 .rackfoot .staged b { color: var(--hi); }
 .rebuild { font-family: var(--display); font-weight: 700; font-size: 14.5px;
       letter-spacing: .08em; text-transform: uppercase; padding: 10px 20px;
       border: 0; border-radius: 9px; background: var(--hi); color: var(--hi-ink);
       cursor: pointer; }
 .rebuild:disabled { background: #ffffff10; color: var(--dimmer); cursor: default; }
 .undo { background: none; border: 0; color: var(--dim); font-size: 12.5px;
         cursor: pointer; text-decoration: underline; padding: 6px; }
 .rackmsg { font-size: 12.5px; color: var(--no); padding: 4px 0 0;
            white-space: pre-wrap; }

 /* -------------------------------------------------------- pull-up */
 .pullup { display: flex; align-items: flex-end; gap: 12px; flex-wrap: wrap; }
 .pullup .field { width: 130px; }
 .pullup button { font-family: var(--display); font-weight: 600; font-size: 14px;
       letter-spacing: .08em; text-transform: uppercase; padding: 11px 20px;
       border: 1px solid var(--co); border-radius: 9px; background: #7d8cff1a;
       color: var(--co); cursor: pointer; }
 .pullup .note { flex: 1; min-width: 200px; font-size: 12.5px;
                 color: var(--dimmer); }
 #pullmsg { font-size: 13px; color: var(--no); margin-top: 9px; }

 @media (max-width: 720px) {
   .fields { grid-template-columns: 1fr 1fr; }
   .fields .field:last-child { grid-column: 1 / -1; }
   .thead audio { width: 100%; order: 9; }
   .thead { flex-wrap: wrap; }
   .lane { grid-template-columns: 1fr; gap: 7px; }
   .zones { grid-template-columns: 1fr; }
 }
</style></head><body>
<div class="wrap">

<div class="board">
<header>
  <div class="mark" id="mark">__MARK__</div>
  <div class="title">
    <h1>Homeroom Studio</h1>
    <svg class="scrawl" viewBox="0 0 340 13" preserveAspectRatio="none"
         aria-hidden="true"><path d="M3 8.5c46-4.2 92-5.6 138-4.4 41 1 82 3.6 122 1.2
         14-.9 27-2.3 40-4.8"/></svg>
  </div>
  <p class="tag">Check one DJ for a beat of their own. Check more for a collab &mdash;
  it lands in the folder of whoever you check <b>first</b>. Ask for four or more
  and a quarter come back as straight, traditional hip hop.</p>
</header>
</div>

<h2 class="box">The Crew <small>nine personalities</small></h2>
<div class="djs">__CREW__</div>
<h2 class="box">The Legends <small>signature styles</small></h2>
<div class="djs">__LEGENDS__</div>
<h2 class="box">The Styles <small>seventeen subgenres, played by the rules</small></h2>
<div class="djs">__GENRES__</div>

<h2 class="box">Rhythm test bank <small>five real, well-known hip-hop beats — the rhythm never changes, only the sounds</small></h2>
<div class="fixedbank" id="fixedbank">__FIXEDBANK__</div>

<div class="panel">
  <div class="fields">
    <div class="field"><label>Tempo</label>
      <input type="text" id="tempo" placeholder="95">
      <div class="hint">blank = home tempo</div></div>
    <div class="field"><label>How many</label>
      <input type="number" id="count" value="1" min="1" max="10">
      <div class="hint">up to 10</div></div>
    <div class="field"><label>Directions</label>
      <input type="text" id="notes" placeholder="no hi hats, dusty, sparse, no 808&hellip;">
      <div class="hint">used for this click and saved in the README</div></div>
  </div>
  <div class="field quick"><label>Quick directions</label>
    <select id="quick">
      <option value="">&mdash; pick one &mdash;</option>
      <option value="sparse">sparse &mdash; thin everything out</option>
      <option value="sparse, no hi hats">sparse, no hi hats &mdash; thin, and no hats at all</option>
      <option value="sparse, halftime, dark">sparse, halftime, dark &mdash; thin, half-time, dark chords</option>
      <option value="no hi hats, dusty, vinyl">no hi hats, dusty, vinyl &mdash; no hats, dusty vinyl sounds</option>
      <option value="halftime, deep, no claps">halftime, deep, no claps &mdash; half-time, deep kit, claps off</option>
      <option value="waltz, jazzy">waltz, jazzy &mdash; 3/4 time, jazz chords</option>
      <option value="no swing, tight, punchy">no swing, tight, punchy &mdash; dead straight grid</option>
      <option value="washed, dreamy chords">washed, dreamy chords &mdash; big reverb, dreamy chords</option>
      <option value="long 808, boomy, room">long 808, boomy, room &mdash; sustained 808, roomy</option>
      <option value="no 808, acoustic, dry">no 808, acoustic, dry &mdash; short real kick, no reverb</option>
      <option value="no perc">no perc &mdash; percussion off</option>
      <option value="crisp">crisp &mdash; crisp, clear samples</option>
      <option value="dusty">dusty &mdash; dusty, aged samples</option>
    </select>
    <div class="hint">fills the Directions box above &mdash; edit it after if you like</div></div>
  <div class="fire">
    <button id="go">Make my beats</button>
    <span id="hosthint"></span>
  </div>
  <div id="work"><div id="workbar"><i></i></div><div id="worktext"></div></div>
</div>

<h2 class="box">This batch <small>play, open the stems, sort</small></h2>
<div class="zones">
  <div class="zone fav"   data-dest="favorites">&starf; Favorites<small>drag here to keep</small></div>
  <div class="zone djz"   data-dest="dj">&#9635; DJ folder<small>the default home</small></div>
  <div class="zone trash" data-dest="trash">&#9587; Trash<small>moved, never deleted</small></div>
</div>
<div id="tracklist"></div>
<div id="empty">__GHOST__<span class="scribble">nothing cooking yet</span>
  <p>Make a beat and it lands here &mdash; with every drum in it.</p></div>

<h2 class="box">Pull up a beat <small>anything you made before</small></h2>
<div class="pullup">
  <div class="field"><label>Beat number</label>
    <input type="number" id="pullno" min="1" placeholder="316"></div>
  <button id="pullgo">Open it</button>
  <span class="note">Adds an older beat to the list above so you can play it,
  open its stems, and swap sounds. (Beats made from July&nbsp;16 on.)</span>
</div>
<div id="pullmsg"></div>

</div>
<script>
 // the quick list just types into the Directions box for him, so the
 // whole existing parser + README trail works unchanged
 document.getElementById('quick').addEventListener('change', e => {
   if (e.target.value) document.getElementById('notes').value = e.target.value;
 });

 // ---------------------------------------------------------- crew picking
 const order = [];
 function refresh() {
   document.querySelectorAll('.dj').forEach(d => {
     const cb = d.querySelector('input');
     const pos = order.indexOf(cb.value);
     d.querySelector('.ord').textContent = pos >= 0 ? (pos + 1) : '';
   });
   const hint = document.getElementById('hosthint');
   if (!order.length) hint.textContent = '';
   else if (order.length === 1) hint.textContent = 'Solo beat from ' + order[0] + '.';
   else hint.textContent = 'Collab — lands in ' + order[0] + "'s folder.";
 }
 document.querySelectorAll('.dj input').forEach(cb => {
   cb.addEventListener('change', () => {
     if (cb.checked) { if (!order.includes(cb.value)) order.push(cb.value); }
     else { const i = order.indexOf(cb.value); if (i >= 0) order.splice(i, 1); }
     refresh();
   });
 });

 // ------------------------------------------------------------- one voice
 // every preview shares one player, so clicking around never stacks sounds
 const audition = new Audio();
 let auditionBtn = null;
 function play(url, btn) {
   if (auditionBtn) auditionBtn.classList.remove('playing');
   if (auditionBtn === btn && !audition.paused) {
     audition.pause(); auditionBtn = null; return;
   }
   document.querySelectorAll('.track audio').forEach(a => a.pause());
   audition.src = url; audition.play().catch(() => {});
   auditionBtn = btn || null;
   if (auditionBtn) auditionBtn.classList.add('playing');
 }
 audition.addEventListener('ended', () => {
   if (auditionBtn) auditionBtn.classList.remove('playing');
   auditionBtn = null;
 });

 // ------------------------------------------------------------ the batch
 const LOC = { favorites: '&starf; kept', trash: 'trashed', dj: '' };
 const staged = {};                    // beat no -> { lane: path | null }
 const trims = {};                     // beat no -> { lane: dB }
 const drops = {};                     // beat no -> { lane: true }

 function setLoc(el, loc) {
   el.className = 'track loc-' + loc;
   el.querySelector('.tloc').innerHTML = LOC[loc] || '';
   el.querySelectorAll('.acts button').forEach(b => {
     b.classList.toggle('on-fav', loc === 'favorites' && b.dataset.dest === 'favorites');
     b.classList.toggle('on-trash', loc === 'trash' && b.dataset.dest === 'trash');
   });
 }
 async function triage(no, dest, el) {
   try {
     const r = await fetch('/triage', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ number: no, dest }) });
     const d = await r.json();
     if (d.ok && el) setLoc(el, d.loc);
   } catch (e) {}
 }

 function prettyTitle(label) {          // "316 Doc Day Boulevard Protocol Drums 93bpm"
   const m = label.match(/^(\d+)\s+(.*?)\s+Drums\s+([\d.]+)bpm$/i);
   return m ? { no: m[1], rest: m[2], bpm: m[3] } : { no: '', rest: label, bpm: '' };
 }

 function makeTrack(b) {
   const t = prettyTitle(b.label);
   const el = document.createElement('div');
   el.className = 'track loc-' + b.loc;
   el.draggable = true;
   el.dataset.no = b.no;
   el.innerHTML =
     '<div class="thead">' +
       '<span class="no">' + b.no + '</span>' +
       '<span class="tmeta"><span class="tname"></span>' +
         '<span class="tsub"></span></span>' +
       '<span class="player"><button class="pp">&#9654;</button>' +
         '<span class="bar"><i></i></span>' +
         '<span class="time">0:00</span></span>' +
       '<audio preload="none" src="/audio?no=' + b.no + '"></audio>' +
       '<span class="acts">' +
         '<button class="stembtn" data-role="stems">Stems</button>' +
         '<button title="Keep it" data-dest="favorites">&starf;</button>' +
         '<button title="DJ folder" data-dest="dj">&#9635;</button>' +
         '<button title="Trash it" data-dest="trash">&#9587;</button>' +
       '</span>' +
     '</div>' +
     '<div class="rack"></div>';
   el.querySelector('.tname').textContent = t.rest;
   el.querySelector('.tsub').innerHTML =
     (t.bpm ? t.bpm + ' BPM' : '') + ' <span class="tloc"></span>';
   setLoc(el, b.loc);
   el.addEventListener('dragstart', e => {
     e.dataTransfer.setData('text/plain', b.no); el.classList.add('dragging'); });
   el.addEventListener('dragend', () => el.classList.remove('dragging'));
   el.querySelectorAll('.acts button[data-dest]').forEach(btn =>
     btn.onclick = () => triage(b.no, btn.dataset.dest, el));
   el.querySelector('[data-role=stems]').onclick = ev => toggleRack(el, b.no, ev.target);
   wireTransport(el);
   return el;
 }

 function clock(s) {
   if (!isFinite(s)) return '0:00';
   const m = Math.floor(s / 60), r = Math.floor(s % 60);
   return m + ':' + String(r).padStart(2, '0');
 }

 function wireTransport(el) {
   const au = el.querySelector('audio'), pp = el.querySelector('.pp'),
         bar = el.querySelector('.bar'), fill = bar.querySelector('i'),
         time = el.querySelector('.time');
   pp.onclick = () => {
     if (!au.paused) { au.pause(); return; }
     audition.pause();                     // never two things at once
     document.querySelectorAll('.track audio').forEach(a => {
       if (a !== au) a.pause();
     });
     au.play().catch(() => {});
   };
   au.addEventListener('play', () => { pp.classList.add('on');
     pp.innerHTML = '&#10073;&#10073;'; });
   const stop = () => { pp.classList.remove('on'); pp.innerHTML = '&#9654;'; };
   au.addEventListener('pause', stop);
   au.addEventListener('ended', () => { stop(); fill.style.width = '0';
     time.textContent = clock(au.duration); });
   au.addEventListener('timeupdate', () => {
     if (au.duration) fill.style.width =
       (au.currentTime / au.duration * 100) + '%';
     time.textContent = clock(au.duration - au.currentTime);
   });
   au.addEventListener('loadedmetadata', () => {
     time.textContent = clock(au.duration); });
   bar.onclick = e => {
     if (!au.duration) return;
     const r = bar.getBoundingClientRect();
     au.currentTime = ((e.clientX - r.left) / r.width) * au.duration;
   };
 }

 async function loadBatch(focus) {
   let d;
   try { d = await (await fetch('/batch')).json(); } catch (e) { return; }
   const list = document.getElementById('tracklist');
   const open = [...list.querySelectorAll('.rack.open')]
                  .map(r => r.closest('.track').dataset.no);
   list.innerHTML = '';
   document.getElementById('empty').style.display =
     (d.beats && d.beats.length) ? 'none' : 'block';
   (d.beats || []).forEach(b => {
     const el = makeTrack(b);
     list.appendChild(el);
     if (open.includes(String(b.no)))
       toggleRack(el, b.no, el.querySelector('[data-role=stems]'));
   });
   if (focus) {
     const el = list.querySelector('.track[data-no="' + focus + '"]');
     if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
   }
 }

 // ---------------------------------------------------------- the stem rack
 function stagedCount(no) { return Object.keys(staged[no] || {}).length; }
 function trimCount(no) { return Object.keys(trims[no] || {}).length; }
 function dropCount(no) { return Object.keys(drops[no] || {}).length; }

 function paintFoot(el, no) {
   const n = stagedCount(no), v = trimCount(no), r = dropCount(no);
   const foot = el.querySelector('.rackfoot');
   if (!foot) return;
   const bits = [];
   if (n) bits.push('<b>' + n + ' ' + (n === 1 ? 'sound' : 'sounds') + ' staged</b>');
   if (v) bits.push('<b>' + v + ' ' + (v === 1 ? 'volume' : 'volumes') + ' changed</b>');
   if (r) bits.push('<b>' + r + ' ' + (r === 1 ? 'stem' : 'stems') + ' removed</b>');
   foot.querySelector('.staged').innerHTML = bits.length
     ? bits.join(' + ') + ' — rebuild makes one new beat with every change in it'
     : 'Pick a different sound, roll the dice, slide a volume, or remove a stem.';
   foot.querySelector('.rebuild').disabled = !(n + v + r);
   foot.querySelector('.undo').style.display = (n + v + r) ? '' : 'none';
 }

 function laneRow(no, s) {
   const row = document.createElement('div');
   row.className = 'lane' + (s.locked ? ' locked' : '');
   row.dataset.lane = s.lane;
   row.innerHTML =
     '<span class="who2"><span class="swatch"></span>' +
       '<span class="lname"></span></span>' +
     '<span class="what"><span class="sample"></span>' +
       '<span class="pack"></span></span>' +
     '<span class="vol"><input type="range" min="-24" max="24" step="0.5" ' +
       'value="0" title="Volume for this stem — double-click to reset">' +
       '<span class="db">0</span></span>' +
     '<span class="picks"></span>';
   row.querySelector('.lname').textContent = s.lane;
   row.querySelector('.sample').textContent = s.sample;
   row.querySelector('.pack').textContent = s.pack || '';

   // volume rides on every lane, locked ones included: a stamp's SAMPLE is
   // the DJ's identity, its level is just mix
   const vol = row.querySelector('.vol input'), db = row.querySelector('.db');
   const showDb = () => {
     const v = parseFloat(vol.value);
     db.textContent = v ? (v > 0 ? '+' : '') + v : '0';
     row.classList.toggle('trimmed', !!v);
   };
   vol.oninput = () => {
     const v = parseFloat(vol.value);
     trims[no] = trims[no] || {};
     if (v) trims[no][s.lane] = v; else delete trims[no][s.lane];
     if (!Object.keys(trims[no]).length) delete trims[no];
     showDb();
     paintFoot(row.closest('.track'), no);
   };
   vol.ondblclick = () => { vol.value = 0; vol.oninput(); };

   const picks = row.querySelector('.picks');

   if (s.stem) {
     const b = document.createElement('button');
     b.className = 'mini'; b.title = 'Hear this drum on its own';
     b.innerHTML = '&#9654;';
     b.onclick = () => play('/stem?no=' + no + '&lane=' +
                            encodeURIComponent(s.lane), b);
     picks.appendChild(b);
   }
   if (s.locked) {
     const t = document.createElement('span');
     t.className = 'lock'; t.textContent = s.why || 'locked';
     picks.appendChild(t);
     return row;
   }

   const sel = document.createElement('select');
   sel.innerHTML = '<option value="">reading your library&hellip;</option>';
   sel.disabled = true;
   picks.appendChild(sel);

   const dice = document.createElement('button');
   dice.className = 'mini'; dice.title = 'Let the machine pick a different one';
   dice.textContent = '🎲';
   dice.onclick = () => {
     const cur = (staged[no] || {});
     if (s.lane in cur && cur[s.lane] === null) delete staged[no][s.lane];
     else { staged[no] = staged[no] || {}; staged[no][s.lane] = null; sel.value = ''; }
     paintLane(row, no, s);
   };
   picks.appendChild(dice);

   // remove the stem completely (owner request 2026-07-21) — click
   // again to change your mind; the rebuild prints a beat without it
   const rm = document.createElement('button');
   rm.className = 'mini'; rm.title = 'Remove this stem from the beat';
   rm.innerHTML = '&#10005;';
   rm.onclick = () => {
     drops[no] = drops[no] || {};
     if (drops[no][s.lane]) {
       delete drops[no][s.lane];
       if (!Object.keys(drops[no]).length) delete drops[no];
     } else drops[no][s.lane] = true;
     row.classList.toggle('dropped', !!(drops[no] && drops[no][s.lane]));
     paintFoot(row.closest('.track'), no);
   };
   picks.appendChild(rm);

   sel.onchange = () => {
     staged[no] = staged[no] || {};
     if (!sel.value) delete staged[no][s.lane];
     else {
       staged[no][s.lane] = sel.value;
       play('/sample?no=' + no + '&lane=' + encodeURIComponent(s.lane) +
            '&path=' + encodeURIComponent(sel.value));   // hear it right away
     }
     paintLane(row, no, s);
   };

   fetch('/candidates?no=' + no + '&lane=' + encodeURIComponent(s.lane))
     .then(r => r.json()).then(d => {
       if (!d.ok || !d.candidates.length) {
         sel.innerHTML = '<option value="">' +
           (d.error || 'nothing else in the library') + '</option>';
         return;
       }
       const packs = new Map();
       d.candidates.forEach(c => {
         if (!packs.has(c.pack)) packs.set(c.pack, []);
         packs.get(c.pack).push(c);
       });
       let html = '<option value="">keep this one</option>';
       packs.forEach((list, pack) => {
         html += '<optgroup label="' + esc(pack) + '">';
         list.forEach(c => {
           html += '<option value="' + esc(c.path) + '">' + esc(c.name) +
                   (c.current ? ' (in this beat now)' : '') + '</option>';
         });
         html += '</optgroup>';
       });
       sel.innerHTML = html;
       sel.disabled = false;
       const st = (staged[no] || {})[s.lane];
       if (st) sel.value = st;
     })
     .catch(() => { sel.innerHTML = '<option value="">could not read the library</option>'; });
   return row;
 }

 function esc(s) {
   return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
                   .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
 }

 function paintLane(row, no, s) {
   const cur = (staged[no] || {});
   const on = s.lane in cur;
   row.classList.toggle('changed', on);
   const name = row.querySelector('.sample');
   if (!on) { name.textContent = s.sample; row.querySelector('.pack').textContent = s.pack || ''; }
   else if (cur[s.lane] === null) {
     name.textContent = 'the machine picks a new one';
     row.querySelector('.pack').textContent = 'was ' + s.sample;
   } else {
     const opt = row.querySelector('select').selectedOptions[0];
     name.textContent = opt ? opt.textContent.replace(' (in this beat now)', '') : 'chosen';
     row.querySelector('.pack').textContent = 'was ' + s.sample;
   }
   paintFoot(row.closest('.track'), no);
 }

 async function toggleRack(el, no, btn) {
   const rack = el.querySelector('.rack');
   if (rack.classList.contains('open')) {
     rack.classList.remove('open'); btn.classList.remove('open'); return;
   }
   rack.classList.add('open'); btn.classList.add('open');
   if (rack.dataset.loaded) return;
   rack.innerHTML = '<div class="lane"><span class="lname">reading the beat&hellip;</span></div>';
   let d;
   try { d = await (await fetch('/stems?no=' + no)).json(); }
   catch (e) { rack.innerHTML = '<div class="rackmsg">Could not read that beat.</div>'; return; }
   if (!d.ok) { rack.innerHTML = '<div class="rackmsg">' + esc(d.error) + '</div>'; return; }
   rack.innerHTML = '';
   const specs = d.stems;
   specs.forEach(s => rack.appendChild(laneRow(no, s)));
   const foot = document.createElement('div');
   foot.className = 'rackfoot';
   foot.innerHTML = '<span class="staged"></span>' +
     '<button class="undo">clear changes</button>' +
     '<button class="rebuild">Rebuild beat</button>' +
     '<div class="rackmsg" style="flex-basis:100%"></div>';
   rack.appendChild(foot);
   foot.querySelector('.undo').onclick = () => {
     delete staged[no]; delete trims[no]; delete drops[no];
     rack.querySelectorAll('.lane').forEach(r => {
       const sel = r.querySelector('select'); if (sel) sel.value = '';
       const vol = r.querySelector('.vol input');
       if (vol) { vol.value = 0; r.querySelector('.db').textContent = '0'; }
       r.classList.remove('trimmed');
       r.classList.remove('dropped');
       const s = specs.find(x => x.lane === r.dataset.lane);
       if (s) paintLane(r, no, s);
     });
     paintFoot(el, no);
   };
   foot.querySelector('.rebuild').onclick = () => rebuild(el, no, foot);
   rack.dataset.loaded = '1';
   paintFoot(el, no);
 }

 async function rebuild(el, no, foot) {
   const picks = staged[no] || {}, vols = trims[no] || {};
   const gone = Object.keys(drops[no] || {});
   if (!Object.keys(picks).length && !Object.keys(vols).length
       && !gone.length) return;
   const btn = foot.querySelector('.rebuild'), msg = foot.querySelector('.rackmsg');
   btn.disabled = true; msg.textContent = '';
   const was = btn.textContent;
   btn.textContent = 'Rebuilding…';
   try {
     const r = await fetch('/rebuild', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ number: no, picks, trims: vols,
                              drops: gone }) });
     const d = await r.json();
     if (d.ok) { delete staged[no]; delete trims[no]; delete drops[no];
                 btn.textContent = was; await loadBatch(d.no); }
     else { msg.textContent = d.error; btn.textContent = was; btn.disabled = false; }
   } catch (e) {
     msg.textContent = String(e); btn.textContent = was; btn.disabled = false;
   }
 }

 // -------------------------------------------------------------- the bins
 document.querySelectorAll('.zone').forEach(z => {
   z.addEventListener('dragover', e => { e.preventDefault(); z.classList.add('over'); });
   z.addEventListener('dragleave', () => z.classList.remove('over'));
   z.addEventListener('drop', e => {
     e.preventDefault(); z.classList.remove('over');
     const no = e.dataTransfer.getData('text/plain');
     triage(no, z.dataset.dest,
            document.querySelector('.track[data-no="' + no + '"]'));
   });
 });

 // ------------------------------------------------------------- make them
 const go = document.getElementById('go'),
       work = document.getElementById('work'),
       worktext = document.getElementById('worktext');
 function working(msg) { work.className = 'on'; worktext.textContent = msg; }
 function failed(msg) { work.className = 'on bad'; worktext.textContent = msg; }
 function done() { work.className = ''; }

 go.onclick = async () => {
   if (!order.length) { failed('Check at least one DJ first.'); return; }
   const count = document.getElementById('count').value;
   go.disabled = true;
   working(count > 1
     ? 'Making ' + count + ' beats… the first one scans your sample library.'
     : 'Making it… the first beat scans your sample library (about 30 seconds).');
   try {
     const r = await fetch('/make', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ names: order,
         tempo: document.getElementById('tempo').value.trim(),
         count, notes: document.getElementById('notes').value }) });
     const d = await r.json();
     if (d.ok) { done(); await loadBatch(); }
     else failed(d.error);
   } catch (e) { failed(String(e)); }
   go.disabled = false;
 };

 // ------------------------------------------------------- rhythm test bank
 document.querySelectorAll('.fixedbtn').forEach(btn => {
   btn.onclick = async () => {
     document.querySelectorAll('.fixedbtn').forEach(b => b.disabled = true);
     working('Rolling a new kit for ' + btn.dataset.title + '…');
     try {
       const r = await fetch('/fixed', { method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ idx: parseInt(btn.dataset.idx, 10) }) });
       const d = await r.json();
       if (d.ok) { done(); await loadBatch(d.no); }
       else failed(d.error);
     } catch (e) { failed(String(e)); }
     document.querySelectorAll('.fixedbtn').forEach(b => b.disabled = false);
   };
 });

 // --------------------------------------------------------------- pull up
 document.getElementById('pullgo').onclick = async () => {
   const no = document.getElementById('pullno').value.trim();
   const msg = document.getElementById('pullmsg');
   msg.textContent = '';
   if (!no) { msg.textContent = 'Which beat number?'; return; }
   try {
     const d = await (await fetch('/pull?no=' + no)).json();
     if (d.ok) { await loadBatch(d.no); document.getElementById('pullno').value = ''; }
     else msg.textContent = d.error;
   } catch (e) { msg.textContent = String(e); }
 };

 loadBatch();
</script></body></html>"""


def _dj_card(n):
    p = CREW[n]
    cls = "dj legend" if n in LEGEND_NAMES else \
          "dj genre" if n in GENRE_NAMES else "dj"
    if n in LEGEND_NAMES:
        # "like Pharrell" etc — real-producer attribution, INTERNAL ONLY
        # (owner decision 2026-07-22, see legends_config.json's _readme):
        # this local batch-player label is fine, but "built" must never
        # leak into an exported file name, stem, or title — those all
        # read from preset["title"] (the sound-alike codename), never
        # from preset["built"]. Keep it that way if this card ever grows
        # an export/share action.
        built = ('<span class="built">like %s</span>'
                 % p["built"].split("/")[0].strip())
    elif n in GENRE_NAMES:
        # the styles say what they ARE, not who they're like — the first
        # clause of "built" before any dash or bracket reads as a tagline
        built = ('<span class="built">%s</span>'
                 % p["built"].split("—")[0].split("(")[0].strip())
    else:
        built = ""
    return (f'<label class="{cls}"><input type="checkbox" value="{n}">'
            f'<span class="dot"></span>'
            f'<span class="who"><span class="name">{n}</span>{built}</span>'
            f'<span class="bpm">{p["bpm"]}</span>'
            f'<span class="ord"></span></label>')


# ---- band artwork -------------------------------------------------
# Owner 2026-07-18: the page wears the band's own art. Drop image files
# into <project>/brand/ and they're picked up on the next launch — the
# one whose name says logo/mark becomes the masthead. Nothing here is
# required; without a brand folder the page falls back to a type mark.

BRAND = Path(__file__).resolve().parent.parent / "brand"
_ART = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")


def _brand_files():
    if not BRAND.is_dir():
        return []
    return sorted(p for p in BRAND.iterdir()
                  if p.is_file() and p.suffix.lower() in _ART)


def _brand_logo(prefer="blue"):
    """The masthead mark. Prefers the colourway asked for (the blue
    square in the masthead), then any file that calls itself a logo,
    then the smallest image in the folder — a mark, not a photo."""
    files = _brand_files()
    if not files:
        return None
    for want in (prefer, "logo", "mark", "icon"):
        hit = [p for p in files if want in p.stem.lower()]
        if hit:
            return hit[0]
    return min(files, key=lambda p: p.stat().st_size)


def _page():
    crew = "".join(_dj_card(n) for n in CREW_ORDER)
    legends = "".join(_dj_card(n) for n in LEGEND_ORDER)
    styles = "".join(_dj_card(n) for n in GENRE_ORDER)
    fixedbank = "".join(
        f'<button class="fixedbtn" data-idx="{i}" data-title="{title}">'
        f'{title}<small>{lib}</small></button>'
        for i, (title, lib, _bpm) in enumerate(FIXED_PATTERNS))
    logo = _brand_logo("blue")
    if logo:
        src = f"/brand?name={quote(logo.name)}"
        mark = f'<img src="{src}" alt="The Back of the Class">'
        ghost = f'<div class="ghost"><img src="{src}" alt=""></div>'
    else:                       # no artwork dropped in yet — type mark
        mark, ghost = "<span>BOTC</span>", ""
    return (_PAGE.replace("__CREW__", crew).replace("__LEGENDS__", legends)
            .replace("__GENRES__", styles)
            .replace("__FIXEDBANK__", fixedbank)
            .replace("__MARK__", mark).replace("__GHOST__", ghost))


def _is_homeroom(port):
    """Is the thing holding this port our own page, or somebody else's
    server? Decides between 'already open' and 'try the next port'."""
    import urllib.request
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/",
                                    timeout=1.5) as r:
            return b"Homeroom Studio" in r.read(4096)
    except Exception:
        return False


def run_web(port=None):
    """Serve Homeroom Studio as a local web page and open the browser.
    PORT in the environment wins, so a second copy can be run alongside
    the one he already has open."""
    port = int(os.environ.get("PORT") or port or 8770)
    import json
    import threading
    import webbrowser
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from urllib.parse import urlparse, parse_qs

    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, ctype, body):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj, code=200):
            self._send(code, "application/json", json.dumps(obj).encode())

        def do_GET(self):
            u = urlparse(self.path)
            if u.path in ("/", "/index.html"):
                self._send(200, "text/html; charset=utf-8",
                           _page().encode("utf-8"))
            elif u.path == "/batch":
                self._json({"beats": _batch_beats()})
            elif u.path == "/lanes":
                no = parse_qs(u.query).get("no", [""])[0]
                try:
                    self._json({"ok": True, "lanes": _swap_lanes(no)})
                except Exception as e:
                    self._json({"ok": False, "error": str(e), "lanes": []})
            elif u.path == "/stems":
                no = parse_qs(u.query).get("no", [""])[0]
                try:
                    self._json({"ok": True, "no": int(no),
                                "stems": _beat_stems(no)})
                except Exception as e:
                    self._json({"ok": False, "error": str(e), "stems": []})
            elif u.path == "/candidates":
                q = parse_qs(u.query)
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        cands = _lane_candidates(q.get("no", [""])[0],
                                                 q.get("lane", [""])[0],
                                                 shots=_CACHE["shots"])
                    self._json({"ok": True, "candidates": cands})
                except Exception as e:
                    self._json({"ok": False, "error": str(e),
                                "candidates": []})
            elif u.path == "/pull":
                # bring an older beat into the list so it gets a card and
                # a stem rack like anything in the current batch
                no = parse_qs(u.query).get("no", [""])[0]
                try:
                    n = int(no)
                    if not beat_wav(n):
                        raise FileNotFoundError(f"No beat {n} in your library.")
                    load_recipe(ROOT, n)      # no recipe, no stem rack
                    append_last_batch(n)
                    self._json({"ok": True, "no": n})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
            elif u.path == "/brand":
                want = parse_qs(u.query).get("name", [""])[0]
                hit = next((p for p in _brand_files() if p.name == want), None)
                if not hit:
                    self._send(404, "text/plain", b"not found")
                    return
                kind = {".svg": "image/svg+xml", ".jpg": "image/jpeg",
                        ".jpeg": "image/jpeg", ".gif": "image/gif",
                        ".webp": "image/webp"}.get(hit.suffix.lower(),
                                                   "image/png")
                self._send(200, kind, hit.read_bytes())
            elif u.path == "/audio":
                self._audio(parse_qs(u.query).get("no", [""])[0])
            elif u.path == "/stem":
                q = parse_qs(u.query)
                no = q.get("no", [""])[0]
                lane = q.get("lane", [""])[0]
                w = (_stem_wav(int(no), lane.strip().lower())
                     if str(no).isdigit() else None)
                self._wav(w)
            elif u.path == "/sample":
                # a raw one-shot, so he can hear a sample before choosing
                # it. The path is only played if it's in this lane's own
                # candidate list — a made-up path never reaches disk.
                q = parse_qs(u.query)
                want = q.get("path", [""])[0]
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        ok = any(c["path"] == want for c in _lane_candidates(
                            q.get("no", [""])[0], q.get("lane", [""])[0],
                            shots=_CACHE["shots"]))
                except Exception:
                    ok = False
                self._wav(Path(want) if ok else None)
            else:
                self._send(404, "text/plain", b"not found")

        def _wav(self, path):
            if not path or not Path(path).exists():
                self._send(404, "text/plain", b"not found")
                return
            self._send(200, "audio/wav", Path(path).read_bytes())

        def _audio(self, no):
            # only ever a beat NUMBER from the client, resolved to a file
            # under the beats root here — no client path ever touches disk
            w = beat_wav(int(no)) if str(no).isdigit() else None
            if not w or not w.exists():
                self._send(404, "text/plain", b"not found")
                return
            data = w.read_bytes()
            rng = self.headers.get("Range")
            if rng and rng.startswith("bytes="):          # let <audio> seek
                try:
                    s, e = rng[6:].split("-")
                    start = int(s) if s else 0
                    end = min(int(e) if e else len(data) - 1, len(data) - 1)
                    chunk = data[start:end + 1]
                    self.send_response(206)
                    self.send_header("Content-Type", "audio/wav")
                    self.send_header("Accept-Ranges", "bytes")
                    self.send_header("Content-Range",
                                     f"bytes {start}-{end}/{len(data)}")
                    self.send_header("Content-Length", str(len(chunk)))
                    self.end_headers()
                    self.wfile.write(chunk)
                    return
                except Exception:
                    pass
            self.send_response(200)
            self.send_header("Content-Type", "audio/wav")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_POST(self):
            if self.path not in ("/make", "/swap", "/triage", "/rebuild",
                                 "/fixed"):
                self._send(404, "text/plain", b"not found")
                return
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/fixed":
                # the rhythm test bank: same five patterns every time,
                # only the kit rolls
                try:
                    idx = max(0, min(len(FIXED_PATTERNS) - 1,
                                     int(data.get("idx", 0))))
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        path, report = generate_fixed(idx,
                                                      shots=_CACHE["shots"])
                        no = int(path.name.split(" ", 1)[0])
                        append_last_batch(no)
                        print(" ", report.replace("\n", " "))
                    self._json({"ok": True, "no": no})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/rebuild":
                # the stem rack: several drums staged, one new beat out
                no = data.get("number")
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        picks = {}
                        for lane, want in (data.get("picks") or {}).items():
                            if not want:                  # surprise me
                                picks[lane] = None
                                continue
                            if not any(c["path"] == want for c in
                                       _lane_candidates(
                                           no, lane, shots=_CACHE["shots"])):
                                raise ValueError(
                                    f"That {lane} isn't in your library.")
                            picks[lane] = want
                        path, report = swap_many(no, picks,
                                                 shots=_CACHE["shots"],
                                                 trims=data.get("trims"),
                                                 drops=data.get("drops"))
                        print(" ", report.replace("\n", " "))
                    self._json({"ok": True,
                                "no": int(path.name.split(" ", 1)[0])})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/triage":
                try:
                    loc = triage(data.get("number"), data.get("dest", "dj"))
                    self._json({"ok": True, "loc": loc})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/swap":
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        _, report = swap(data.get("number"),
                                         data.get("lane", "snare"),
                                         shots=_CACHE["shots"])
                        print(" ", report.replace("\n", " "))
                    self._json({"ok": True, "result": report})
                except Exception as e:               # shown in the page
                    self._json({"ok": False, "error": str(e)})
                return
            names = data.get("names", [])
            tempo = data.get("tempo") or None
            notes = data.get("notes", "")
            try:
                how_many = max(1, min(10, int(data.get("count") or 1)))
            except (TypeError, ValueError):
                how_many = 1
            try:
                flags = _traditional_flags(how_many, names)
                with lock:
                    if "shots" not in _CACHE:
                        _CACHE["shots"] = build_shots()
                    results, made = [], []
                    for i in range(how_many):
                        path, report = generate(names, tempo, notes,
                                                traditional=flags[i],
                                                shots=_CACHE["shots"])
                        results.append(report)
                        made.append(int(path.name.split(" ", 1)[0]))
                        print(" ", report.replace("\n", " "))
                    set_last_batch(made)              # the player's batch
                self._json({"ok": True, "results": results})
            except Exception as e:                   # shown in the page
                self._json({"ok": False, "error": str(e)})

        def log_message(self, *a):
            pass                                     # keep the terminal quiet

    def open_browser(u):
        if not os.environ.get("REASON_VOICE_NO_BROWSER"):
            webbrowser.open(u)        # same guard the voice server uses

    # Double-clicking the launcher while a copy is already open used to
    # dump a raw "OSError: [Errno 48] Address already in use" traceback
    # into the Terminal window (owner hit this 2026-07-18). He is not a
    # developer and a traceback reads as "it's broken", so: if the port
    # is ours, just bring that window up; if it's something else, step
    # to the next free one. Never a stack trace.
    httpd = None
    for p in range(port, port + 12):
        try:
            httpd = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            port = p
            break
        except OSError:
            if _is_homeroom(p):
                url = f"http://127.0.0.1:{p}/"
                print(f"\n  Homeroom Studio is already open: {url}")
                print("  (bringing that one up — no need to start a "
                      "second copy)\n")
                open_browser(url)
                return
    if httpd is None:
        print(f"\n  Couldn't start: ports {port}-{port + 11} are all busy.")
        print("  Close whatever is using them, or restart the Mac.\n")
        return

    url = f"http://127.0.0.1:{port}/"
    print(f"\n  Homeroom Studio is open in your browser: {url}")
    print("  (leave this window open; close it or press Ctrl+C to quit)\n")
    open_browser(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Homeroom Studio closed.")


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
        how_many = max(1, min(10, a.count))
        flags = _traditional_flags(how_many, names)
        made = []
        for i in range(how_many):
            path, report = generate(names, a.tempo, a.notes, root=out,
                                    traditional=flags[i], shots=shots,
                                    status=lambda m: print(" ", m))
            made.append(int(path.name.split(" ", 1)[0]))
            print(report)
        set_last_batch(made, root=out)
    else:
        run_web()


if __name__ == "__main__":
    main()
