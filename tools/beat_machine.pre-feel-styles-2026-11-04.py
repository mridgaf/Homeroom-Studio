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
import subprocess
import sys
import wave
import zlib
from datetime import date
from pathlib import Path
from urllib.parse import quote

import numpy as np

sys.path.append(str(Path(__file__).parent))
from groove import OWNER_TASTE
from make_drum_loops import SR, read_wav24, sub808, wav24_bytes, write_wav24
from make_drum_beats import ban_sound, build_shots, name_twins
from make_hiphop_tracks import load_audio
from crew import (BARS, CREW, GENRE_NAMES, LEGEND_NAMES, bars_of,
                  boom_bap_variant,
                  build_kit, is_dj, lock_stamps, normalize_preset,
                  render_crew_beat, ring_secs, sub_sidechain,
                  LONG_KICK_SECS, _LOW_END, _load_choked, _pick_path, _resolve_secs)
from beat_recipes import (OLD_LANE_LABELS, history_avoid, lane_label,
                          load_recipe, record_history, save_recipe,
                          write_midi, write_stems)
from pattern_gen import (LIB_DIR, break_list, compose, flavor_role,
                         free_beat, load_library, _lib_lane, SOUND_OPEN_P)

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
    project root: {"root": "/Volumes/TBOTC 3/Homeroom Rhythms"}
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
    name = "Homeroom Rhythms"
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
# All twelve, so a key detected by tools/reference_track.py ("F#") can be
# looked up. Widened 2026-09-02; NOT a wider pool. The random fallback
# picker below draws from key_context.SUB_ROOTS (the original seven, in the
# original order) — picking from this dict instead would re-tune the sub
# under every traditional beat already on disk.
ROOT_HZ = {"C": 32.70, "C#": 34.65, "D": 36.71, "D#": 38.89, "E": 41.20,
           "F": 43.65, "F#": 46.25, "G": 49.00, "G#": 51.91, "A": 55.00,
           "Bb": 58.27, "B": 61.74}

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
    "Half Light": (["Dim", "Late", "Behind", "Hollow", "Dusk", "Faded",
                    "Slack", "Amber"],
                   ["Room", "Hour", "Curtain", "Echo", "Fade", "Glow",
                    "Drift", "Hall"]),
    "Fast Water": (["Rapid", "Undertow", "Spillway", "Shallow", "Cold",
                    "Steel", "Loose", "Running"],
                   ["Current", "Chop", "Channel", "Rush", "Ladder",
                    "Bank", "Break", "Weir"]),
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


def _vary_pat(pat, rng, p_drop, adds):
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


def _vary_kick(bars, rng):
    """The kick grammar itself wanders between beats (owner 2026-07-16:
    half the crew wrote their kicks entirely in capital anchors, so the
    small-hit mutation never touched them and every beat shared one kick
    line). Bar 1 states the character's grammar untouched; in later bars
    up to two anchors may drop or slide a 16th, and a soft extra kick can
    land in a gap. The downbeat is fair game too now (owner 2026-07-29,
    overrides the old "downbeat never moves" rule) — any variation,
    whatever fits the style or personality."""
    out = [bars[0]]
    for pat in bars[1:]:
        s = list(pat)
        n = len(s)
        xs = [i for i, c in enumerate(s) if c == "X"]
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
# The lanes a famous figure is transcribed into — the ones compose() seeds
# verbatim from patterns_breaks.json, and therefore the ones nothing
# downstream may rewrite. See the break gate in vary_preset.
BREAK_LANES = {"kick", "snare", "hat"}


def vary_preset(preset, variant, num, tempo_locked, density=None):
    """Apply the per-beat variety plan to a (deep-copied) preset in place.
    Returns a list of plain-words notes describing what this beat does.
    (The 2026-07-17 "kick and snare play through every bar" rule and the
    bar-1 kick restore were removed by the owner 2026-10-30.) density (from the
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

    # kick_min_hits (Baltimore Club, 2026-09-24): compose() already holds
    # the floor; this pass's anchor wander and bar treatments could still
    # thin a bar under it, so the composed bar comes back at the end.
    floor = preset.get("kick_min_hits")
    kick_in = list(lanes["kick"][3]) if floor and "kick" in lanes else None

    def barlist(ln):
        """This lane's bars, padded to the beat's length so a treatment
        can index any bar without an IndexError on a short pattern."""
        bars = list(lanes[ln][3])
        while len(bars) < nbars:
            bars.append(bars[len(bars) % len(bars)] if bars else "-" * 16)
        return bars

    mutable = [ln for ln in lanes if not ln.startswith("stamp")]
    # OWNER RULE 2026-08-04: "whatever rules are keeping the break beats from
    # being what they should be, exclude the break beats from those rules."
    # compose() already spares a verbatim break its thinning and bank-vary,
    # but THIS pass runs on every beat afterwards and undid the work: the
    # density roll added and dropped hits, and thinbar/frisson/breath/bshift
    # blanked whole bars or rewrote X into x. A transcription that survives
    # compose() and then gets a bar emptied is not a transcription. The
    # figure's own lanes are untouchable here; guests still get everything,
    # so a break beat still has an arrangement.
    if preset.get("break_beat"):
        mutable = [ln for ln in mutable if ln not in BREAK_LANES]
        notes.append("break: figure left exactly as transcribed")
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
            rewrite(ln, _vary_kick(list(bars), rng))
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
        rewrite(ln, [_vary_pat(b, rng, p_drop, adds) for b in bars])
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
              if ln not in {"kick", "snare", "clap"} | TIMEKEEPERS | canon
              and ln not in preset.get("_guests", ())]
    if colors and rng.random() < 0.3:
        ln = rng.choice(colors)
        rewrite(ln, ["-" * len(b) for b in lanes[ln][3]])
        notes.append(f"no {ln} this time")

    # 3b. OWNER RULE 2026-08-01: the clap should appear "in fewer beats".
    # It was in 44% of beats and, where a snare was also present, landed on
    # the snare's exact steps 89% of the time — a doubled backbeat, with the
    # clap measuring LOUDER than the snare. Lowering the backbeat weight
    # (done in the configs) moves it off 2&4; this drops it entirely on a
    # third of the beats that have one.
    # Two hard conditions, both about not removing the backbone: there must
    # be a snare still playing, and a canon clap (Baltimore Club's 8-count)
    # is never touched. The six snare+clap STACK identities are exempt —
    # owner: "the claps should stay as intended for signature DJs" — and
    # they are recognisable by their clap copying the snare outright.
    # The stack is declared in the grammar, and it runs BOTH ways: six
    # identities have clap={"copy": "snare"} and six more have the reverse,
    # snare={"copy": "clap"} — "a BIG clap with the snare tucked underneath"
    # (Kane East, Sunday Chop), "a harsh clap-snare stack" (Swish Beatz).
    # Both are that identity's documented sound, so both are exempt. Missing
    # the reverse direction on the first pass left 6 identities still
    # doubling at 100%; caught by measuring per-identity, not in aggregate.
    _g = preset.get("grammar") or {}
    stacked = any(isinstance(_g.get(ln), dict) and "copy" in _g[ln]
                  for ln in ("clap", "snare"))
    snare_live = "snare" in lanes and any(_hits(b) for b in lanes["snare"][3])
    if ("clap" in lanes and "clap" not in canon and not stacked
            and snare_live and rng.random() < 0.33):
        rewrite("clap", ["-" * len(b) for b in lanes["clap"][3]])
        notes.append("no clap this time")

    # 4. one structural treatment. Was: owner rule 2026-07-17, no silence
    # gaps ever, kick/snare/clap always play through. Overridden 2026-07-29
    # — kick, snare and clap can go fully silent for a whole bar now too,
    # same as any other lane, whatever fits the style or personality. The
    # CANON lane (the figure that DEFINES the style, owner rule 2026-07-19)
    # is a separate, still-live rule — it softens here, never vanishes,
    # same as it always has, so a reggaeton doesn't stop being a reggaeton.
    # OWNER RULE 2026-08-01, replacing the 2026-07-29 free-for-all: "the gaps
    # I want to be rare. One in six." Measured under 07-29: 47% of beats had a
    # completely silent bar and 90% had a hole of some kind (full bar or back
    # half). In the finished mix the chords covered it — a 5-8 dB dip — but in
    # the DRUM STEMS ALONE, which is how he actually works in Reason, 8 of 12
    # beats dropped 17-61 dB. That is what he was hearing.
    #
    # So the treatments are split: the two that punch a hole in every lane are
    # now rolled at 1-in-6, and the rest of the time a beat gets an
    # arrangement move that costs nothing structurally (one lane sits out a
    # half, or a velocity dip). The "breath" — every lane resting the back
    # half of a bar — was unconditional on two of the four branches; it is a
    # hole too, so it joins the rare group instead of riding along free.
    # OWNER RULE 2026-08-03: velocity dips are GONE. "quietbar" pulled a
    # whole bar's accents down to normal hits (-2.9 dB) and could stack with
    # the contrast pass in generate(), which pulled those down again to
    # ghosts (-8.8 dB more) — 11.7 dB off a bar before the per-hit wobble
    # added its own. That is the "drum parts get way too quiet". With
    # everything level, a dip is the one thing that contradicts the rule, so
    # the only non-hole treatment left is the arrangement move.
    # OWNER RULE 2026-09-28: "too often" and "doesn't sound intentional".
    # 1 in 6 -> 1 in 20, and every stop now slams back in: the bar after
    # the hole plays its accents hard (frisson already did). Length and
    # placement unchanged -- he didn't flag them.
    HOLE_P = 1 / 20.0
    def _slam(b):
        """Bar b comes back hard after a stop: its hits play as accents."""
        if b >= nbars:
            return
        for ln in mutable:
            bars = barlist(ln)
            bars[b] = bars[b].replace("x", "X")
            rewrite(ln, bars)

    if preset.get("break_beat"):
        # REAL REGRESSION, 2026-08-04, caught by
        # test_real_beats_are_not_mono_or_silent on his beat 1803 and traced
        # back here. Taking kick/snare/hat out of `mutable` above (so a
        # transcription stays a transcription) left the GUESTS as the only
        # thing a treatment could pick. So every break beat now aimed its
        # structural move at a guest lane — and the guests are the only
        # off-centre content a break beat has, since kick and snare sit dead
        # centre and the hat is pinned near it by house rule. 1803's shaker
        # was sent "only in the A section" and half the beat had nothing in
        # the sides at all: -28 dB side-to-mid, i.e. mono.
        #
        # The right answer is not a cleverer treatment. It is that "for
        # break beats, stay verbatim" means the arrangement stops moving
        # too — the figure IS the arrangement.
        t = ""
    else:
        # owner 2026-10-30: "I don't want any halfway switch", then "all
        # four" -- the default "bshift" (one lane only in the A or B half,
        # 19 in 20 beats) and the rare holes (thinbar / frisson / breath,
        # 1 in 20) are all off. The branches below stay for the A/B benches.
        t = ""
    if t == "thinbar":                       # a bar rests, canon breathes
        b = rng.choice(late)
        for ln in mutable:
            bars = barlist(ln)
            if ln in canon:
                bars[b] = bars[b].replace("X", "x")
            else:
                bars[b] = "-" * len(bars[b])
            rewrite(ln, bars)
        _slam(b + 1)
        notes.append(f"bar {b + 1} drops out, bar {b + 2} slams back")
    elif t == "frisson" and nbars >= 2:      # build: thins, then slams
        for ln in mutable:
            bars = barlist(ln)
            if ln not in canon:
                bars[last - 1] = "-" * len(bars[last - 1])
            bars[last] = bars[last].replace("x", "X")
            rewrite(ln, bars)
        notes.append(f"build: bar {last} thins out, bar {last + 1} slams")
    # (the "quietbar" velocity dip that used to live here is gone —
    #  owner 2026-08-03, see the treatment roll above)

    # 4b. the breath: every lane rests for the back half of one bar. Owner
    # 2026-08-01 — this used to fire on the two most common branches, i.e.
    # roughly half of ALL beats, on top of whatever step 4 had already done.
    # It is a hole, so it is now one of the three rare treatments above and
    # only ever runs on its own.
    if t == "breath":
        b = rng.choice(late)
        for ln in mutable:
            if ln in canon:
                continue
            bars = barlist(ln)
            n = len(bars[b])
            bars[b] = bars[b][:n // 2] + "-" * (n - n // 2)
            rewrite(ln, bars)
        _slam(b + 1)
        notes.append(f"lanes sit out the back half of bar {b + 1}, "
                     f"bar {b + 2} slams back")

    # 4c. (bar 1 always has a kick -- REMOVED, owner 2026-10-30: "Remove
    #  it" when asked about the kick/snare-every-bar rule.)

    # 5. tempo lean (only when he didn't set a tempo himself). A
    # subgenre's tempo is part of its identity (owner rule 2026-07-19):
    # Baltimore club is 130 and leaning it to 124 makes it not-quite-
    # club, a screw beat is 66, reggaeton sits in a narrow band. So the
    # styles lean HALF as far, and only ever by a hair.
    if not tempo_locked:
        orig_bpm = preset["bpm"]
        # a signature's tempo range is the identity's pocket — keep the lean
        # inside it (owner ear 2026-07-22: Dre's keepers all sat 90-93, the
        # 98bpm renders missed). Same protection genres get, earned by data.
        sig_tempo = (preset.get("signature") or {}).get("tempo")
        if sig_tempo and isinstance(sig_tempo[0], (list, tuple)):
            # multiple disconnected pockets (owner call 2026-07-23,
            # Timberline: normal 90-100 AND double-time 135-145) — pick a
            # pocket, then a tempo inside it. The %-lean below can't reach
            # a second pocket from the base bpm, so it doesn't apply here.
            lo, hi = rng.choice(sig_tempo)
            preset["bpm"] = rng.randint(lo, hi)
        else:
            lean = rng.choice((-0.02, 0.0, 0.0, 0.02)) \
                if preset.get("genre") \
                else rng.choice((-0.05, -0.03, 0.0, 0.03, 0.05))
            if lean:
                preset["bpm"] = max(TEMPO_LO,
                                    min(TEMPO_HI,
                                        int(round(preset["bpm"] * (1 + lean)))))
            if sig_tempo:
                preset["bpm"] = max(sig_tempo[0],
                                    min(sig_tempo[1], preset["bpm"]))
        if preset["bpm"] != orig_bpm:
            notes.append(f"tempo leans to {preset['bpm']}")
    if kick_in:
        rewrite("kick", [b if _hits(b) >= floor else kick_in[i % len(kick_in)]
                         for i, b in enumerate(lanes["kick"][3])])
    return notes


# Owner call 2026-07-22: "have the kick gate the bass and other
# instruments, 90 percent of the creations regardless of DJ." This
# outranks each DJ's own sidechain number — the old rule was the
# reverse (a DJ's 0.0 meant never duck, and Crate Prophet never did),
# which is exactly the kind of built-in rule the dialog box and the
# house settings are now allowed to overrule.
DUCK_P = 0.9
DUCK_DEFAULT = 0.2               # depth for a DJ who carries none

# The LOW END gets its own, much deeper duck (owner 2026-09-01: "I want
# sidechain compression on the sub — I haven't heard it working at all").
# It was working; it was inaudible. The mix-wide 0.2 is a 1.9 dB dip, which
# is the right size for hats and chords getting out of the kick's way and
# far too small to read as pumping on a sub sitting in the same octave as
# the kick.
#
# 5 dB is the owner's own call, by ear, off an A/B render at 7 dB
# (2026-09-01): 7 was audible and too much, 5 is the setting he kept. The
# constant is written as the depth that MEASURES 5 dB, not as a round
# number that happens to be near it: 1 - 10**(-5/20).
#
# The 1-in-10 skip still skips it: off means off, and that no-duck beat is
# the owner's own texture call from 2026-07-22. A deep sub duck on 9 beats
# in 10 is not a thing he can miss.
SUB_DUCK_DEFAULT = 0.4377        # 5.0 dB dip on sub / 808 / bass


def apply_duck(preset, rng):
    """Decide this beat's sidechain. Returns the depth applied."""
    if rng.random() < DUCK_P:
        preset["sidechain"] = preset.get("sidechain") or DUCK_DEFAULT
    else:
        preset["sidechain"] = 0.0
    preset["sub_sidechain"] = SUB_DUCK_DEFAULT
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
    # reggaeton that wanders to 62% stops being one. Pinned outright, no
    # outliers. (This comment used to say "Baltimore club is straight or
    # it isn't club" - an illustration, never his words; 2026-09-24 his
    # research-build answer gave Baltimore Club a light swing, 54.)
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


# Owner rule 2026-08-01: "All sounds are open to all DJs, but they try to
# maintain seventy five percent of their personality within." Raised to 30%
# and widened to everything on 2026-09-14 — OPEN_P and free_beat() now live
# in pattern_gen (see there). Used here to give the four clap-only DJs a
# snare sometimes; _build_chords, build_kit and the low end use the same roll.


def _maybe_seat_snare(preset, variant):
    """Four identities (Chrome Dial, Night Metro, Mustang, Timberline) have a
    clap and NO snare, so the clap IS their backbeat and can never rest —
    which is exactly why their clap sat on 2 and 4 in every beat. Owner
    2026-08-01: "the four DJs can have a snare at times." On OPEN_P of beats
    they get one, built from the clap's own row so it inherits the identity's
    pan/feel, with its own seed so it composes a DIFFERENT figure. Once a
    snare is carrying the backbeat, the clap becomes free to move or rest."""
    kit, lanes = preset.get("kit", {}), preset.get("lanes", {})
    if "snare" in kit or "clap" not in kit or "clap" not in lanes:
        return False
    if not free_beat(variant):
        return False
    pan, gain, (off, jit, swing, seed), bars = lanes["clap"]
    kit["snare"] = ("snare", None, ["snare"], 1.0)
    lanes["snare"] = (0.0, round(gain * 0.85, 3),
                      (off, jit, swing, seed + 7717), list(bars))
    grammar = preset.setdefault("grammar", {})
    if "clap" in grammar and isinstance(grammar["clap"], dict):
        grammar["snare"] = copy.deepcopy(grammar["clap"])
    return True


def _borrow_drum_parts(p, name, variant):
    """A free beat's drums (owner 2026-09-14): "make sure all patterns and
    back beats are given the same freedom for djs as the instruments", and
    asked how, "each part from a different DJ". So each drum part's grammar
    — the kick (with its kick flavors), every backbeat and timekeeper lane,
    and the guest-percussion palette — comes from its own randomly rolled
    DJ. compose() then writes a fresh pattern from that borrowed grammar
    exactly as it would from the DJ's own.

    Left alone on purpose: a lane that only COPIES another lane (it follows
    whatever that lane borrowed, and two borrowed copies could point at
    each other), and Doc Day's snare_locked_24 (a hard lock he set). The
    traditional backbone still applies afterwards inside compose(), and a
    typed backbeat in the notes box still wins after this. Returns notes."""
    rng = random.Random(variant * 709 + 23)
    djs = sorted(n for n in CREW if n != name)     # genres lend too
    grammar = p.get("grammar") or {}
    notes = []

    def real(spec):
        return isinstance(spec, dict) and "copy" not in spec

    for lane in sorted(grammar):
        if not real(grammar[lane]):
            continue
        if lane == "snare" and p.get("snare_locked_24"):
            continue
        donors = [n for n in djs
                  if real((CREW[n].get("grammar") or {}).get(lane))]
        if not donors:
            continue
        d = rng.choice(donors)
        grammar[lane] = copy.deepcopy(CREW[d]["grammar"][lane])
        if lane == "kick" and CREW[d].get("kick_flavors"):
            p["kick_flavors"] = copy.deepcopy(CREW[d]["kick_flavors"])
        notes.append("%s from %s" % (lane, d))
    donors = [n for n in djs if CREW[n].get("extras")]
    if p.get("extras") and donors:
        d = rng.choice(donors)
        p["extras"] = copy.deepcopy(CREW[d]["extras"])
        notes.append("percussion from %s" % d)
    return notes


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
    # must be set BEFORE compose() — apply_directions runs after it, too
    # late for the composer to choose a break transcription.
    p["break_beat"] = bool(dirs and dirs.get("break_beat"))
    p["break_name"] = (dirs or {}).get("break_name")
    _maybe_seat_snare(p, variant)
    _pin_bars_for_loop_voice(p, variant, dirs)
    borrowed = []
    # owner 2026-10-29: every DJ/Legend/genre borrows on half its beats
    if not bb and name in CREW and free_beat(variant, SOUND_OPEN_P):
        borrowed = _borrow_drum_parts(p, name, variant)
    if dirs and dirs.get("force_mode"):
        for ln in ("snare", "clap"):
            spec = p.get("grammar", {}).get(ln)
            if isinstance(spec, dict) and "modes" in spec:
                spec["modes"] = [[dirs["force_mode"], 1.0]]
    notes = compose(p, name, variant, boom_bap=bb, tsig=tsig, trick=trick,
                    traditional=traditional)
    if borrowed:
        notes.insert(0, "free beat, drums: " + ", ".join(borrowed))
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
        # same as solo_preset: the composer needs this before it runs
        q["break_beat"] = bool(dirs and dirs.get("break_beat"))
        q["break_name"] = (dirs or {}).get("break_name")
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

    # harmony (owner 2026-11-02): instruments on if EITHER parent plays
    # them; the voice is dealt to one of the parents that does
    harm = [n for n in names
            if (CREW[n].get("signature") or {}).get("chords_default")]
    hp = rng.choice(harm) if harm else host
    for k in ("signature", "chord_flow", "chord_gen", "one_chord",
              "two_chord", "harmony_diet", "chord_lift", "melody_flow"):
        if k in CREW[hp]:
            p[k] = copy.deepcopy(CREW[hp][k])
    if harm:
        notes.append(f"harmony: {hp}")

    p["vel_seed"] = variant
    if tsig:
        p["tsig"] = list(tsig)
    # Razor, DJ Light Green and Well Damn have no stamp lane — a collab
    # with them crashed on a KeyError. Stamps are stripped from every new
    # beat anyway (_drop_stamp), so whoever lacks one is just skipped.
    no_stamp = (0.0, 0.0, None, None)
    pan = CREW[host]["lanes"].get("stamp", no_stamp)[0]
    if "stamp" in CREW[host]["lanes"]:
        p["lanes"]["stamp"] = copy.deepcopy(CREW[host]["lanes"]["stamp"])
    for i, g in enumerate(names[1:]):
        if "stamp" not in CREW[g]["lanes"]:
            continue
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
        # The lane's parent's taste in character, the whole library on a
        # free beat. Half of beats from the whole bank (owner 2026-10-28, as build_kit)
        path, x = _pick_path(shots, role, wants, secs, seed,
                             must=must, avoid=avoid,
                             open_bank=(False if preset.get("_asked_kick_snare")
                                        else free_beat(variant, SOUND_OPEN_P)))
        if path:
            avoid.add(path)
        kit[lane] = x
        sources[lane] = path
        spec_used[lane] = (role, must, wants, secs)
    # Legends have no locked stamp (None) and three identities have no
    # stamp lane at all; generate() drops stamp lanes from new beats
    # anyway, so only a real locked stamp is carried here.
    for lane, who in [("stamp", host)] + [(f"stamp{i + 2}", g)
                                         for i, g in enumerate(names[1:])]:
        if lane in preset["lanes"] and stamps.get(who, (None,))[0]:
            kit[lane] = stamps[who][1]
            sources[lane] = f"{Path(stamps[who][0]).stem}  [{who}'s stamp]"
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
    # KICK DRUM, BASS DRUM and BASS are three different sounds and three
    # different words (owner 2026-07-25). "bass drum" used to be a synonym
    # for the kick here, so typing it changed the wrong sound; and "bass"
    # muted the 808 boom rather than the melodic line. Both fixed below —
    # longest phrase wins, see parse_directions.
    # 2026-09-23: "bass drum" means the KICK again -- the standard word;
    # the long boom is "808" (owner: use the terms the way producers do).
    ("kick", ("kick drums", "kick drum", "bass drums", "bass drum",
              "kicks", "kick")),
    ("snap", ("snaps", "snap", "finger snaps")),
    ("perc", ("percussion", "percs", "perc")),
    ("bongo", ("bongos", "bongo", "congas", "conga")),
    ("stamp", ("stamps", "stamp")),
    # phase 2 lanes (owner 2026-07-23): let the notes box switch them off.
    # No "loop" entry — there is no loop lane (see _add_sample_lanes).
    ("vox", ("vocals", "vocal", "vox", "voices", "voice", "adlibs",
             "adlib", "chants", "chant")),
    # the BASS DRUM — the long low boom under the kick, whether it's a
    # sampled 808 (lane "bass") or the tuned synth root (lane "sub")
    ("bass", ("bass 808", "808 bass", "808s",
              "808", "sub bass", "subs", "sub")),
    # the BASS — the melodic low line following the chords (bass0..N).
    # Matches the chordbass family in _chord_family, which is what
    # apply_directions deletes.
    ("chordbass", ("basslines", "bassline", "bass line", "bass")),
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


# Typed words -> which famous figure. The right-hand side must appear in
# that pattern's "name" in pattern_library/patterns_breaks.json; the picker
# on the page sends the full name and matches the same way, so there is one
# lookup, not two. "think" is deliberately NOT a trigger on its own — "I
# think this should be dark" is a sentence, not a request for Lyn Collins.
BREAK_WORDS = (
    ("amen", "Amen"), ("funky drummer", "Funky Drummer"),
    ("impeach", "Impeach"), ("apache", "Apache"),
    ("assembly line", "Assembly Line"),
    ("synthetic substitution", "Synthetic Substitution"),
    ("cold sweat", "Cold Sweat"), ("roachclip", "Roachclip"),
    ("nautilus", "Nautilus"), ("get out my life", "Get Out My Life"),
    ("think break", "Think"), ("think about it", "Think"),
    ("lyn collins", "Think"),
    ("levee", "Levee"), ("when the levee breaks", "Levee"),
    ("big beat", "Big Beat"), ("billy squier", "Big Beat"),
    # off his own step chart, 2026-08-04
    ("billie jean", "Billie Jean"),
    ("walk this way", "Walk This Way"),
    ("new day", "New Day"), ("skull snaps", "New Day"),
    ("papa was too", "Papa Was Too"),
    ("mardi gras", "Mardi Gras"))


def clean_key(key):
    """The Key control's value -> (root, mode), or None for "no key set".

    Accepts ("F", "minor"), "F minor", or "F". A bad note or a mode this
    engine doesn't know is an error he can read, not a silent fallback to
    something else's key."""
    if not key:
        return None
    from key_context import MODES
    if isinstance(key, str):
        bits = key.replace("-", " ").split()
        root = bits[0] if bits else ""
        mode = " ".join(bits[1:]).lower().replace(" ", "_") or "minor"
    else:
        root, mode = (list(key) + ["minor"])[:2]
        mode = str(mode).lower().replace(" ", "_")
    root = str(root).strip()
    root = root[:1].upper() + root[1:].replace("B", "b")
    # ROOT_HZ spells one note per pitch class ("Bb", never "A#"); accept
    # whichever spelling he typed or a pack labelled a file with.
    root = {"A#": "Bb", "Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#",
            "Cb": "B", "Fb": "E", "E#": "F", "B#": "C"}.get(root, root)
    if root not in ROOT_HZ:
        raise ValueError("Key %r isn't a note this engine plays (%s)."
                         % (root, ", ".join(ROOT_HZ)))
    if mode not in MODES:
        raise ValueError("Mode %r isn't one this engine knows (%s)."
                         % (mode, ", ".join(sorted(MODES))))
    return root, mode


def parse_directions(notes):
    """Read this click's directions out of the notes text. v6 adds
    space (gated/dry/room/washed), swing (more/straight), time
    signature (3/4, waltz, 6/8), and halftime words."""
    t = " " + (notes or "").lower() + " "
    t = t.replace(" 3/4", " 3-4 ").replace(" 6/8", " 6-8 ")
    # Everything that isn't a letter, digit or the 3-4/6-8 hyphen becomes a
    # space. Was: only "," and "." were stripped, so "funky drummer!" and
    # "no 808s?" simply didn't match (found 2026-08-04).
    t = re.sub(r"[^a-z0-9\- ]+", " ", t)
    t = " ".join(t.split())
    t = f" {t} "
    out = {"mute": set(), "tags": [], "kick": None, "density": None,
           "space": None, "swing": None, "tsig": None, "force_mode": None,
           "chords": False, "chord_feel": None, "break_beat": False}
    # OWNER 2026-08-01: the classic sampled-break grooves. Typing any of
    # these puts the beat on a real transcription played straight through
    # (pattern_gen: verbatim), instead of the library's usual role as a
    # thinned, varied influence. The PATTERN is transcribed; no audio from
    # any recording is used — the figure plays on his own drum samples,
    # which is how every drum machine ships a break.
    # The typed word must SELECT the figure, not just switch the feature on.
    # It used to set break_beat and then get thrown away, so all ten names
    # picked at random out of ten (found 2026-08-04). The value here is a
    # fragment of the pattern's name in patterns_breaks.json — see
    # pattern_gen._pick_break. None = "surprise me".
    out["break_name"] = next(
        (name for word, name in BREAK_WORDS if f" {word} " in t), None)
    if out["break_name"] or any(x in t for x in (
            " break ", " breaks ", " breakbeat ", " break beat ")):
        out["break_beat"] = True
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
    # Longest phrase wins, and a matched phrase is struck out of the text
    # so it can't be counted twice (owner 2026-07-25): "no bass drum" is
    # ONE instruction about the bass drum, but plain substring matching
    # also saw "no bass" inside it and silently killed the bass line too.
    scan = t
    for lane, words in LANE_WORDS:
        for w in sorted(words, key=len, reverse=True):
            for neg in NEGATIONS:
                if neg + w in scan:
                    out["mute"].add(lane)
                    scan = scan.replace(neg + w, " ")
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
    # "no chords" / "drums only" turns the chord+bass lanes OFF and beats
    # chords_default. Checked before the plain chord words, because "no
    # chords" CONTAINS "chords" — without this, asking for less turned the
    # lane on (real bug, found 2026-07-25 when chords_default went
    # roster-wide and the off-switch suddenly mattered).
    out["no_chords"] = (
        any(f" {neg.strip()} {w} " in t for w in CHORD_WORDS
            for neg in NEGATIONS)
        or any(f" {x} " in t for x in ("drums only", "just drums",
                                       "only drums", "drum only")))
    out["chords"] = not out["no_chords"] and (
        bool(out["chord_feel"])
        or any(f" {w} " in t for w in CHORD_WORDS))
    return out


def apply_directions(preset, dirs):
    """Mutate this beat's preset per the parsed directions. Returns
    plain-words notes; the caller must run this BEFORE the kit is picked
    so muted lanes never grab a sample."""
    notes = []
    guests = set(preset.get("_guests", ()))
    for lane in list(preset["lanes"]):
        # digit-suffixed lanes belong to a family, and the family is what
        # he names: bass0..N are the BASS (the line), chord0..N the chords.
        # Stripping digits instead would fold bass0 into "bass" — the 808
        # BASS DRUM lane — so "no bass drum" would take the line out too.
        fam = _chord_family(lane)
        base = fam or lane.rstrip("0123456789")
        if base in dirs["mute"] or (lane in guests
                                    and "_guests" in dirs["mute"]):
            del preset["lanes"][lane]
            preset["kit"].pop(lane, None)
            msg = ("no %s (as asked)"
                   % ("bass" if fam == CHORD_BASS_FAM else
                      MELODY_FAM if fam == MELODY_FAM else
                      "chords" if fam else lane_label(lane)))
            if msg not in notes:          # one note per family, not per bar
                notes.append(msg)
    if "kick" not in preset["lanes"]:
        preset["sidechain"] = 0.0            # nothing left to duck around
        preset["sub_sidechain"] = 0.0
    space, on = preset["space"]
    preset["space"] = (space, [ln for ln in on if ln in preset["lanes"]])

    if dirs["kick"] and "kick" in preset["kit"]:
        flavors = [f for f in preset.get("kick_flavors", [])
                   if (f[1] == "808") == (dirs["kick"] == "808")]
        if flavors:
            _, must, wants, secs = flavors[0]
            role = flavor_role(must, preset["kit"]["kick"][0])
            preset["kit"]["kick"] = (role, must, list(wants), tuple(secs))
            notes.append(f"kick: {dirs['kick']} (as asked)")
            preset["_asked_kick_snare"] = True   # keep his words

    if dirs["tags"]:
        for lane, (role, must, wants, secs) in list(preset["kit"].items()):
            merged = dirs["tags"] + [w for w in wants
                                     if w not in dirs["tags"]]
            preset["kit"][lane] = (role, must, merged, secs)
        notes.append("prefer " + "/".join(dirs["tags"]) + " (as asked)")
        preset["_asked_kick_snare"] = True
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


# "add the root" (owner rule 2026-07-18): ON. Retired 2026-07-23 as
# collateral of that morning's engine-wide 808 ban ("ignore previous push
# for 808"), then restored the same day once the ban itself was reversed
# ("allow DJs to stay true to style, with the kick") and the owner asked
# for the sub back explicitly. Round trip left no scar: the mechanism was
# flag-gated rather than deleted. Unreachable again 2026-07-25 to
# 2026-09-01 — not by this flag but by a "not chords" condition at the
# call site, once every identity gained chords_default. Fixed 2026-09-01:
# the sub now rides WITH the chords, tuned to the beat's own key.
# OFF since 2026-09-23 -- owner hard rule, "I don't want any tones created
# by machine", and the tuned sub is a synthesized sine. Its DJs play the
# bass line instead (BASS_808_DJS below). Kept only for the A/B bench.
ADD_THE_ROOT_808 = False

# Does the root 808 also ride on a CHORDS beat, tuned to that beat's key?
#
# It does not today, and the cost is measured: across his library, 150
# traditional beats carry chords and NOT ONE of them got a sub. The gate
# was `not dirs["chords"]`, written when a chords beat had harmony's own
# moving bass under it — but that bass was retired 2026-07-29
# (_build_chords: bass_idx is permanently None) and every identity has
# since gained chords_default, so the gate quietly took the 2026-07-18
# "add the root" rule off the table unless he types "no chords".
#
# HE HEARD IT AND SAID NO — 2026-09-04, on the Desktop batch, his words:
# "leave the eight zero eight tuning off, I don't like it in the mix."
# That is a verdict, not a pending question: do not re-propose it, do not
# quietly flip it as part of some other change. The measurement that made
# the case for it (150 chords beats, not one sub) still stands and is still
# wrong-by-the-numbers — his ear outranks it. What he is hearing is most
# likely the cost the batch READ ME named: the drums step back 2.5-5.2 dB
# to make room for the sub, so the trade is drum level for weight.
# The flag stays so the bench (tools/make_root_808_ab.py) can still render
# it if he ever asks again; False is the shipped sound.
ROOT_808_WITH_CHORDS = False

# Does a REBUILD (swap a hat, trim a level) hand the beat back its own key
# and progression, or re-roll them?
#
# Re-rolling is deterministic from the saved variant + the saved signature,
# so on an ordinary beat it lands on the same answer and there is nothing
# to hear — measured: 0 of the 118 September beats on his drive come back
# different. It goes wrong in exactly two places, and both are ones he
# creates on purpose: a REFERENCE TRACK that set the key (6 of 6 beats came
# back in a different key), and a typed mood word, which is never persisted
# past the click it was typed for (6 of 6 came back on a different
# progression). The recipe knows all three, so it can hand all three back.
#
# ON — he heard folder 2 of the 2026-09-04 batch and kept it: "I will keep
# the locks." So a rebuild now hands the beat back its own key, mode and
# progression instead of re-rolling them. On an ordinary beat this changes
# nothing audible (0 of 118 September beats drift); it is there for the two
# cases he creates on purpose, the reference track and the typed mood word.
REBUILD_LOCKS_KEY = True

# FOUR EFFECTS THAT USED TO GO UNUSED (owner 2026-09-28, "small share,
# everyone"): each rolls per beat, on this share of beats, for every DJ,
# Legend and genre. Hall is a reverb SPACE, so a genre (which keeps the
# space it declares, owner rule 2026-07-19) never rolls it. First guesses,
# not heard: one number each.
EXTRA_FX_P = {"hall": 0.10, "haas": 0.20, "ratchet": 0.15,
              "kick_layer": 0.15}
HAAS_LANES = ("hat", "perc", "shaker", "snap", "bongo", "conga", "rim")
# A kick that rings past crew.LONG_KICK_SECS gets a short kick's snap on
# top and ducks under it (crew.punch_long_kick) on this share of beats --
# owner 2026-09-28, "7 of 10". The other 3 keep the raw long kick.
LONG_KICK_PUNCH_P = 0.7


def _roll_extra_fx(preset, kit, sources, spec_used, lane_parent, shots,
                   variant, owner):
    """Haas, ratchet and kick layer for one new beat. Everything lands in
    the preset/kit/recipe, so a rebuild plays the same thing back."""
    rng = random.Random(variant * 977 + 31)
    lanes = preset["lanes"] = dict(preset["lanes"])
    if rng.random() < EXTRA_FX_P["haas"]:
        preset["haas_lanes"] = [ln for ln in lanes
                                if ln.startswith(HAAS_LANES)]
    if rng.random() < EXTRA_FX_P["ratchet"]:
        for ln, (pan, gain, feel, bars) in list(lanes.items()):
            if not ln.startswith("hat"):
                continue
            new = []
            for b in bars:
                hits = [i for i, c in enumerate(b) if c == "x"]
                if len(b) == 16 and hits and rng.random() < 0.5:
                    b = list(b)
                    b[rng.choice(hits[len(hits) // 2:])] = "r"   # late in the bar
                    b = "".join(b)
                new.append(b)
            lanes[ln] = (pan, gain, feel, new)
    if ("kick" in kit and "kick" in spec_used
            and rng.random() < EXTRA_FX_P["kick_layer"]):
        role, must, wants, secs = spec_used["kick"]
        if "808" not in str(must or ""):     # an 808 kick carries its own low end
            path, x = _pick_path(shots, role, wants, secs,
                                 rng.randrange(1, 1 << 30), must=must,
                                 avoid=set(p for p in sources.values() if p))
            if path and x is not None:
                kit["kicklayer"] = x
                sources["kicklayer"] = path
                spec_used["kicklayer"] = spec_used["kick"]
                lane_parent["kicklayer"] = owner
    krng = random.Random(variant * 1013 + 7)
    if ("kick" in kit and ring_secs(kit["kick"]) > LONG_KICK_SECS
            and krng.random() < LONG_KICK_PUNCH_P):
        avoid = set(p for p in sources.values() if p)
        for _ in range(5):               # the snap is a kick, never an 808
            path, x = _pick_path(shots, "kick", [], KICK_WITH_BASS_SECS,
                                 krng.randrange(1, 1 << 30), avoid=avoid)
            if path and x is not None and "808" not in Path(path).name:
                kit["kickpunch"] = x
                sources["kickpunch"] = path
                spec_used["kickpunch"] = ("kick", None, [],
                                          KICK_WITH_BASS_SECS)
                lane_parent["kickpunch"] = owner
                break
            avoid.add(path)



# WHO GETS THE TUNED SUB (owner 2026-09-07: "tuned sub should only be used
# when specific DJs require it"). It is a synthesized SINE on the beat's
# root -- a different instrument from the sampled 808, and the wrong sound
# under a dusty SP-1200 kit. Before this it ran on 75% of every DJ's
# traditional beats, which is how it came to hold the low end everywhere
# and lock the 411-file 808 pool out (the two share one slot).
#
# The list is his, approved 2026-09-07 off their own descriptions:
#   Doc Day    "an occasional deep sub" -- says it outright
#   Wonky      "a sub-heavy kick"
#   Trip Hop   "patient half-time weight" -- his call, not written as sub
#   Half Light slowest on the roster, everything drags -- his call
# Everyone naming an 808 (Night Metro, Rage Engine, Mustang, Hitt Kid,
# Memphis, Crunk, Houston Screw, Emo Hip Hop, Miami Bass) gets the SAMPLE
# instead; the boom-bap and live-band names get neither.
SUB_DJS = ("Doc Day", "Wonky", "Trip Hop", "Half Light")

# WHO PLAYS THE BASS ON AN 808 (owner 2026-09-23, list approved as shown).
# Standard practice is ONE bass per beat, and which one is a style call:
# in trap / Southern / Memphis / bounce the bass is the 808 -- ONE 808
# recorded in the beat's key, hitting with the kick, ducked under it, never
# pitched and never following the chords (owner 2026-09-23, second pass); in
# boom bap, soul, funk and live-band styles a bass instrument plays the
# line (his bass one-shots, _build_chords) under a short punchy kick and
# there is no long 808. Everyone not named here is the second kind --
# including the four old SUB_DJS, whose tuned sub was a machine tone.
# A free beat (pattern_gen.free_beat) may land on either, as before.
BASS_808_DJS = ("Night Metro", "Rage Engine", "Mustang", "Hitt Kid",
                "DJ Light Green", "Memphis", "Crunk", "Houston Screw",
                "Emo Hip Hop", "Miami Bass", "Plug", "Reggaeton Alt",
                "New Math", "New Orleans Bounce")
# The kick's longest ring whenever a bass plays: the kick is the punch,
# the bass carries the long low tail (kick + 808 built as one unit).
KICK_WITH_BASS_SECS = 0.5


def _plays_808(variant, dirs, dj, shots):
    """True when this beat's bass is the 808, False when it is the bass
    line. Deterministic from the variant, so the kick pairing (before the
    kit) and _low_voice (after it) always agree."""
    if "bass" in dirs.get("mute", set()) or not shots.get("bass"):
        return False
    if dirs.get("kick") == "808":       # he typed "long 808": he gets one
        return True
    if free_beat(variant) and is_dj(dj):
        return random.Random(variant * 383 + 19).random() < 0.5
    return dj in BASS_808_DJS


def _pair_kick(preset, plays_808, has_bass):
    """Kick and bass as one unit (owner 2026-09-23, standard practice).
    Whenever a bass plays, the kick is the short punchy hit -- capped at
    KICK_WITH_BASS_SECS -- and the bass carries the long tail. On an 808
    beat the kick also never comes from the 808 pool: two 808 samples
    stacked is exactly the "kick drum AND bass drum" he heard 2026-09-20.
    Runs before the kit is picked, so the kick sample is chosen short."""
    spec = preset.get("kit", {}).get("kick")
    if not spec or not has_bass:
        return
    role, must, wants, secs = spec
    if plays_808 and must == "808":
        flav = next((f for f in preset.get("kick_flavors", [])
                     if f[1] != "808"), None)
        role, must = "kick", None
        wants, secs = (list(flav[2]), flav[3]) if flav else ([], secs)
    lo, hi = secs if isinstance(secs, (tuple, list)) else (secs, secs)
    cap = KICK_WITH_BASS_SECS
    preset["kit"]["kick"] = (role, must, list(wants),
                             (min(lo, cap), min(hi, cap)))


def _add_root_sub(preset, kit, sources, variant, vnotes,
                  harmony_info=None, traditional=False, dj=None,
                  decided=False):
    """The tuned 808 sub under the kick — owner rule 2026-07-18, "add the
    root". Returns the note name it used, or None if this beat gets no sub.

    Extracted out of generate() 2026-09-03 so the audition bench renders
    THIS code rather than a copy of it: a bench that reimplements the thing
    it is testing can pass while the real path is broken.

    `harmony_info` is the beat's chords, when it has any. Given one, the
    sub takes the beat's own key instead of rolling its own note — a static
    sub on the wrong root under a progression is worse than no sub at all.
    An identity's `signature.key.roots` may ask for a note ROOT_HZ does not
    spell (Half Light asks for B on 7.4% of its beats); that beat gets no
    sub rather than a random one.

    `decided=True` is generate(): _low_voice already made this beat's one
    low-sound call (owner 2026-09-14), so only the kick check is left
    here. Without it — the root-808 bench — the old gates run as they
    always did."""
    if "kick" not in preset["lanes"]:
        return None
    if not decided:
        if not (ADD_THE_ROOT_808 and traditional):
            return None
        if dj not in SUB_DJS:                   # see SUB_DJS above
            return None
        # a LONG 808 kick is carrying the sub itself; two would just fight
        if _holds_low_end(preset):
            return None
        if random.Random(variant * 577 + 13).random() >= 0.75:
            return None
    key_root = (harmony_info or {}).get("root")
    if key_root:
        if key_root not in ROOT_HZ:
            return None
        root_note, sub_audio = key_root, sub808(ROOT_HZ[key_root], 0.6)
    else:
        root_note, sub_audio = _root_sub(variant)
    kpan, kgain, (ko, kj, ksw, ks), kbars = preset["lanes"]["kick"]
    preset["lanes"]["sub"] = (0.0, 0.7, (0, 0, ksw, ks + 7),
                              [b for b in kbars])
    kit["sub"] = sub_audio
    sources["sub"] = "synth 808 sub, root %s" % root_note
    vnotes.append("root: %s (tuned 808 sub under the kick)" % root_note)
    return root_note


CHORD_LIFT_FLOOR = 60   # C4: chords sit an octave+ above the bass line
LOW_TOP = 47      # top of MIDI octave 2, the register an 808/bass root sits in


def _low_pool(kind):
    """His samples that can play a LOW root: "bass" = the Bass folder's
    synth-bass and bass one-shots, "brass" = brass recorded within
    MAX_SHIFT of octave 2. His lowest brass today is F3 (MIDI 53), so the
    brass pool stays empty until tuba/trombone samples land in the Brass
    folder (owner 2026-09-14) — reported, never faked with a big stretch."""
    import instrument_sampler as ins
    idx = ins.scan_bass() if kind == "bass" else ins.scan()
    return [e for e in idx if e["group"] == kind
            and e["note"] <= LOW_TOP + ins.MAX_SHIFT]


def _low_sample(kind, key_root, variant, secs):
    """(path, audio) of a bass-sample or low-brass hit on the beat's ROOT —
    one note, never a line (the 2026-07-29 no-melodic-bassline rule) — or
    (None, None) when nothing reaches it."""
    import instrument_sampler as ins
    got = _low_pool(kind)
    if not got:
        return None, None
    if key_root:
        from key_context import pitch_class
        note = 36 + pitch_class(key_root)
        if not ins.covers(got, [note], (kind,)):
            return None, None
    else:                                    # no key: play it where it sits
        note = random.Random(variant * 71 + 5).choice(got)["note"]
    used = []
    audio = ins.voice_note(got, note, secs, groups=(kind,), used=used)
    return (used[0] if used else None), audio


def _low_voice(preset, variant, dirs, traditional, dj, shots):
    """This beat's ONE low sound under the kick: "808" or None (None means
    the bass LINE is the bass -- see _plays_808 / BASS_808_DJS).

    OWNER HARD RULE 2026-09-14, "don't pile lows on lows", made standard
    practice 2026-09-23: one bass per beat, chosen by the DJ's style. This
    is the single place it is decided, before anything that could add one;
    generate() then refuses a second low lane outright."""
    if "kick" not in preset["lanes"]:
        return None
    # 2026-09-23 (owner, standard practice): the one low sound is the 808
    # for BASS_808_DJS and nothing here for everyone else -- their bass is
    # the bass LINE, which _build_chords plays. No sub (a machine tone), no
    # single held bass/brass root under the kick (that plus the line was
    # two basses). A long 808 kick can no longer happen: _pair_kick caps
    # every kick short before the kit is picked.
    return "808" if _plays_808(variant, dirs, dj, shots) else None


def add_bass_and_chords(preset, kit, sources, shots, variant, dirs, vnotes,
                        traditional, dj):
    """The melodic half of a from-scratch beat, in its one right order:
    decide the ONE bass, build the chords (and the bass line), add the 808
    lane if it isn't already the line, refuse any second low sound.
    generate() and the legend audition bench both call THIS, so an
    audition can never drift from what generate() ships.
    Returns (midi_chords, harmony_info)."""
    low = _low_voice(preset, variant, dirs, traditional, dj, shots)
    # CHORD FLOW (owner 2026-09-26, "not very much variety"): smooth
    # voicings, varied chord lengths, turnarounds, fewer 1-2 chord loops.
    # Stamped on NEW beats only, and saved in the recipe, so a rebuild of a
    # beat made before today gives back exactly the sound it had.
    import harmony
    preset.setdefault("chord_flow", harmony.FLOW_VERSION)
    # CHORD PATTERNS v2 (2026-10-19): the 100 added rhythms; older beats keep 63
    # v3 (2026-10-24): 150 more; beats stamped 2 keep the 163 they were made with
    preset.setdefault("chord_lib", 3)
    # BASS GROOVE (2026-10-19): same deal -- new beats play a bass figure
    # (tools/bass_rhythm.py), a rebuild of an older beat keeps its held root.
    import bass_rhythm
    preset.setdefault("bass_flow", bass_rhythm.FLOW_VERSION)
    # ALTERNATE BASS SOUNDS (2026-10-19, tools/bass_voices.py): new beats may
    # play orchestral bass / cello / piano / guitar / organ / synth as the bass
    preset.setdefault("bass_voice_flow", 1)
    # ANSWER MELODY (2026-10-19): same deal (tools/melody_rhythm.py)
    import melody_rhythm
    preset.setdefault("melody_flow", melody_rhythm.FLOW_VERSION)
    # LEAD (2026-10-19): same deal -- fewer leads, and the lead keeps the
    # 7th (see _build_chords)
    preset.setdefault("lead_flow", 1)
    # ARP FLOW (2026-10-19): arps rarer and varied (chord_rhythm.ARP_MAX)
    preset.setdefault("arp_flow", 1)
    # PERC FLOW (2026-10-19): percussion capped by loudness (crew.PERC_ROLES)
    preset.setdefault("perc_flow", 1)
    # COMP FLOW (2026-10-19): stab/comp rhythm across the loop, phrase
    # shape, comp's own words (chord_rhythm.COMP_CELLS)
    preset.setdefault("comp_flow", 1)
    # HAT FLOW (2026-10-19): hats capped by loudness (crew.HAT_UNDER_DB)
    preset.setdefault("hat_flow", 1)
    # MIX TRIM (2026-10-31): hats -3.5 dB, bass +4 dB (crew.HAT_TRIM_DB)
    preset.setdefault("mix_trim", 1)
    # TASTE FLOW (2026-10-31, Plan C): this beat's kit leaned toward his
    # Favorites' sample folders (generate -> taste.weights). Record only.
    preset.setdefault("taste_flow", 1)
    # REAL FEEL (2026-10-31, Plan A): a real drummer's timing + gentle
    # accents, picked from the listen line (tools/real_groove.py). Stored as
    # the template key so a rebuild plays the same drummer. New beats only.
    if "real_feel" not in preset:
        import real_groove
        preset["real_feel"] = real_groove.pick(
            preset.get("listen") or (CREW.get(dj) or {}).get("listen", ""),
            random, dj)
    # ARRANGEMENT FLOW (2026-10-20): one optional structural move inside
    # the loop plus an optional fill into bar 1. New beats only.
    import arrangement
    preset.setdefault("arrange_flow", arrangement.FLOW_VERSION)
    # GROOVE FLOW (2026-10-20, tools/groove_lock.py): bass and chords read
    # how busy each bar's kick is -- simpler on a busy kick, moving or
    # held where the drums leave space, the kick kept clear. New beats only.
    preset.setdefault("groove_flow", 1)
    # BAND FLOW (2026-10-21, owner from the Reason demo songs): a chord part
    # doubled on a second instrument (sometimes a L/R pair), and a bass that
    # can play the chords' own rhythm. New beats only.
    preset.setdefault("band_flow", 1)
    # MIDI VOICE FLOW (2026-10-24, owner): MIDI notes play on the identity's
    # own researched instruments, never bell/pluck, London strings for the
    # gaps (see _build_chords). New beats only.
    preset.setdefault("midi_voice_flow", 1)
    # CHORD LIFT (2026-10-24, owner: chords sat almost as low as the bass):
    # every chord is voiced from C4 up (see CHORD_LIFT_FLOOR). The bass
    # still reads the unlifted roots. New beats only.
    preset.setdefault("chord_lift", 1)
    # CHORD GEN (owner 2026-10-29: "a whole new selection of chord
    # progressions"): chords come from tools/chord_gen.py (genre tables
    # built from 666k real songs) instead of progressions_config.json; the
    # loop it made is saved here so a rebuild plays the same chords. The
    # bass line writes its own genre pattern (tools/bass_gen.py), and
    # chords + bass play written loud/soft (tools/dynamics.py). New beats
    # only.
    import chord_gen
    import dynamics
    preset.setdefault("chord_gen", {"v": chord_gen.VERSION, "who": dj})
    # TEXTURE (owner 2026-10-29): full chords rare; most beats carry the
    # music with two notes, a riff or a sampled loop (tools/riff_gen.py).
    # New beats only.
    import riff_gen
    preset.setdefault("texture_flow", riff_gen.VERSION)
    # NO MIDI (owner 2026-10-29: "It just doesn't sound right"): no chords
    # from his MIDI packs, no riffs from MIDI (packs or Lakh). Riff beats
    # become two-note or loop beats. New beats only.
    preset.setdefault("no_midi", 1)
    # NO LOOPS on the Original side (owner 2026-10-30: "This side, I don't
    # want to use loops. Unless absolutely necessary."). A loop is only the
    # last resort after every instrument fails; loop/riff textures become
    # two-note beats. Loops-only beats are a separate path. New beats only.
    preset.setdefault("no_loop", 1)
    # NO EQ (owner 2026-10-29): see crew.render_crew_beat. Soft chord/bass
    # hits only get quieter, not darker. New beats only.
    preset.setdefault("no_eq", 1)
    preset.setdefault("dyn_flow", dynamics.VERSION)
    # LENGTH FLOW (owner 2026-10-30): chord hits mix short, half and held
    # lengths, and two-note beats may hold a chord (chord_rhythm.LEN_W).
    # New beats only.
    preset.setdefault("len_flow", 1)
    # NO HALFWAY (owner 2026-10-30: "I don't want any halfway switch"):
    # 2-chord loops never split exactly in half, and comp/arp chords drop
    # the every-2nd-bar back-half rest and every-4th-bar push. New beats only.
    preset.setdefault("no_halfway", 1)
    # DJ FLOW (owner 2026-10-31): comp/arp/pad rhythms follow the DJ's
    # pattern_tags, and bends move hits off the 8th grid. New beats only.
    preset.setdefault("dj_flow", 1)
    # ONE CHORD (owner 2026-10-31): one chord per loop, every note in the
    # key (harmony.home_chord / safe_scale). New beats only.
    preset.setdefault("one_chord", 1)
    # HARMONY DIET (owner 2026-11-03): rap-shaped scale odds (free rolls and
    # in-character alike), flat chord names, and a 2-chord shuttle (i-iv
    # first) on the soul / melodic identities; dark ones stay on one chord.
    # New beats only.
    preset.setdefault("two_chord", 1)
    preset.setdefault("harmony_diet", 1)
    # An 808 beat plays NO bass line: the 808 bangs with the kick on its
    # own lane (_add_sample_lanes), one note, never following the chords
    # (owner 2026-09-23, reversing that morning's 808-plays-the-roots).
    # The strings' own basses never play -- the 808 or the line is THE bass.
    midi_chords, harmony_info = _build_chords(preset, kit, sources, variant,
                                              dirs, vnotes,
                                              allow_basses=False,
                                              bass_line=(low != "808"))
    # (the tuned root sub used to be added here -- gone 2026-09-23, owner:
    # no machine-made tones. _add_root_sub survives for the A/B bench.)
    # phase 2 (owner 2026-07-23): the sampled 808 lane -- only on a beat
    # where it did NOT become the bass line (no chords) -- and vocals.
    _add_sample_lanes(preset, kit, sources, shots, variant, dirs, vnotes,
                      key_root=(harmony_info or {}).get("root"), low=low)
    _refuse_second_low(preset, kit, sources, vnotes)
    if preset.get("arrange_flow") and tuple(preset.get("tsig", (4, 4))) == (4, 4):
        arrangement_plan = arrangement.plan(variant, bars_of(preset))
        preset["arrangement"] = arrangement_plan
        arrangement.apply_patterns(preset, arrangement_plan)
        if harmony_info is not None:
            harmony_info["arrangement"] = arrangement_plan
    return midi_chords, harmony_info


def pair_kick_for(preset, variant, dirs, dj, shots):
    """generate()'s kick pairing, for any caller about to pick a kit."""
    _808 = _plays_808(variant, dirs, dj, shots)
    _pair_kick(preset, _808, has_bass=_808 or bool(dirs["chords"]))


def _refuse_second_low(preset, kit, sources, vnotes):
    """The refusal half of the one-low-sound rule (owner 2026-09-14). Every
    path is meant to go through _low_voice, but if anything ever leaves a
    beat with two low lanes, the first one stays and the rest are dropped
    and named in the beat's notes — never mixed together."""
    lows = [ln for ln in preset["lanes"] if ln in _LOW_END]
    for ln in lows[1:]:
        for d in (preset["lanes"], kit, sources, preset["kit"]):
            d.pop(ln, None)
        vnotes.append("%s dropped: one low sound per beat" % ln)


def _holds_low_end(preset):
    """True when this beat already has its ONE low sound (owner hard rule
    2026-09-14: "don't pile lows on lows"): a low-end lane (crew._LOW_END)
    or a long 808 kick, which carries the sub by itself — the reason
    _add_root_sub always refused to put a sub under one."""
    if any(ln in preset.get("lanes", {}) for ln in _LOW_END):
        return True
    kick = preset.get("kit", {}).get("kick")
    if not kick or kick[1] != "808":
        return False
    secs = kick[3]
    return (max(secs) if isinstance(secs, (tuple, list)) else secs) > 0.6


def _root_sub(variant, secs=0.6):
    """Owner rule 2026-07-18 ("add the root"), retired 2026-07-23 — see
    ADD_THE_ROOT_808 above. Kept for recipe-rebuild fidelity: an
    already-rendered beat's saved root_note still needs this to
    reproduce its sub on a re-render. A tuned 808 sub for the
    traditional beats — a real synthesized sub on a chosen musical root,
    so the kick has a low note under it. Deterministic per beat; returns
    (note name, mono audio)."""
    from key_context import SUB_ROOTS
    note = random.Random(variant * 13 + 7).choice(list(SUB_ROOTS))
    return note, sub808(ROOT_HZ[note], secs)


# Phase 2 (owner 2026-07-23): the newly-unlocked bass/808 and vocal samples
# get real lanes. Optional and seeded per beat, so a batch varies and any beat
# re-renders identically. Rates are below 1 so neither is "in every beat".
#
# NO DRUM-LOOP LANE. It was built (owner asked for "Full loop") and then
# removed the same day: "The drum loops cause problems. Exclude drum loops —
# there are enough drum sounds." A loop laid over an already-programmed kit
# fought it. Loops are still TAGGED into the scanner's "_loops" bucket, which
# is what keeps them OUT of the one-shot drum roles (a loop must never be
# choked into a drum hit); nothing plays them. Melodic/in-key loops are
# unaffected — those reach a beat through the chords feature's own scanner.
SAMPLED_BASS_P = 0.4        # sampled 808 under the kick (non-chord beats)
# Owner 2026-09-28, overruling part of 2026-09-23 ("bang along with the
# kick"): 808 on the kick's hits made every 808 beat's low end identical
# (44 of 44 measured). About 1 in 3 now plays its OWN rhythm: it still lands
# with the bar's first kick, then answers in the kick's gaps. Still one note,
# never pitched. 0 = always on the kick.
OWN_808_RHYTHM_P = 1 / 3


def _own_808_bars(kbars, rng):
    """The 808's own rhythm off the kick's bars: struck with the first kick
    of each bar, then 1-2 hits on even steps where the kick is silent. A bar
    the kick rests in, the 808 rests in too."""
    out = []
    for bar in kbars:
        hits = [i for i, c in enumerate(bar) if c != "-"]
        if not hits:
            out.append(bar)
            continue
        cells = ["-"] * len(bar)
        cells[hits[0]] = "X"
        gaps = [i for i in range(hits[0] + 3, len(bar), 2) if bar[i] == "-"]
        for i in rng.sample(gaps, min(len(gaps), rng.choice((1, 2)))):
            cells[i] = "x"
        out.append("".join(cells))
    return out
# Owner rule 2026-08-01: "Kill the vocal hits completely." Was 0.3 — a vocal
# one-shot on 30% of beats, measured at up to +7.9 dB ABOVE the kick, i.e. the
# loudest thing in the beat. 0.0 switches the lane off without deleting the
# code path, so his 145 existing beats still rebuild from their recipes.
# The OTHER vocal source was the stamp lane (17 of 18 genres carried "vocal"
# in its tags) — killed separately by STAMP_LANE below.
VOX_LANE_P = 0.0           # a sparse vocal one-shot — OFF (owner 2026-08-01)

# Owner rule 2026-08-01: "Remove the stamp lane. The DJs don't have to have a
# signature sound for every track if that's what that is." That is exactly
# what it was — crew.lock_stamps pins ONE sample per personality and puts it
# in every beat they make. Measured cost: the stamp was on 100% of beats and
# drew from 32 unique files across 509 picks, half of them from 6 files;
# "Sub Riser.wav" alone landed on 17% of the whole library. Chiptune's stamp
# tags could only ever match 5 files in his library, Glass Cat's and Farrow's
# 6. It was the single biggest cause of "the same sounds over and over".
#
# NOT torn out — switched off at the one choke point where a new beat's lanes
# are settled. The 57 code sites that read `stamp_paths`/`stamp_secs` stay, so
# all 506 existing beats still rebuild and swap exactly as before.
STAMP_LANE = False


def _drop_stamp(preset):
    """Remove the stamp lane (and collab stamp2/stamp3) from a fresh preset.
    Called once in generate() so compose(), vary_preset() and the kit builder
    never see it. Returns the preset for chaining."""
    if STAMP_LANE:
        return preset
    for k in [k for k in preset.get("kit", {}) if k.startswith("stamp")]:
        preset["kit"].pop(k, None)
    for k in [k for k in preset.get("lanes", {}) if k.startswith("stamp")]:
        preset["lanes"].pop(k, None)
    return preset


_808_INDEX_FILE = Path(__file__).resolve().parent.parent / \
    "sample_808_index.json"
_808_INDEX = None


def _808_notes():
    """{path: note} for the sorted 808s, from sample_808_index.json.
    Empty when the file or the drive is missing -- the caller then simply
    leaves the 808 off a keyed beat, which is the old behaviour."""
    global _808_INDEX
    if _808_INDEX is None:
        try:
            got = json.loads(_808_INDEX_FILE.read_text())["files"]
            _808_INDEX = {k: v.get("note") for k, v in got.items()}
        except (OSError, ValueError, KeyError, TypeError):
            _808_INDEX = {}
    return _808_INDEX


def _808_to_key(path, audio, key_root):
    """(audio shifted onto `key_root`, semitones moved), or (None, 0).

    Shortest way round the circle, so the move is never more than 6
    semitones and the 808 keeps the register it was sampled in. Length is
    preserved -- Rubber Band, not a resample: a tape-speed
    shift would make the long 808s shorter as they go up, and the length
    of an 808's tail is the whole feel of it.
    """
    have = _808_notes().get(str(path))
    if not have:
        return None, 0
    from key_context import pitch_class
    try:
        # pitch_class, not an index into a sharps-only list: "Bb".upper()
        # is "BB", which was not in it, so every Bb beat silently lost its
        # 808 (12% of chord beats, found 2026-09-14)
        # a note name (the beat's key) or a pitch class 0-11 (a chord's
        # root, when the 808 plays the bass line -- owner 2026-09-23)
        target = (key_root % 12 if isinstance(key_root, int)
                  else pitch_class(key_root))
        semis = (target - pitch_class(have)) % 12
    except (ValueError, AttributeError):
        return None, 0
    if semis > 6:
        semis -= 12
    if semis == 0:
        return audio, 0
    try:
        # Rubber Band (pedalboard.time_stretch at 1.0), not PitchShift.
        # Measured 2026-09-23 on 8 of his C 808s x 6 targets: PitchShift
        # landed 22 cents off on average and up to 277 cents (nearly three
        # semitones) -- its window is too short for a 30-60 Hz fundamental;
        # Rubber Band 10 cents mean, 67 worst, and exact on a test sine.
        # Formants follow the pitch: an 808 is a tone, not a voice.
        from pedalboard import time_stretch
        x = np.asarray(audio, dtype=np.float32)
        y = time_stretch(x.reshape(1, -1), SR, stretch_factor=1.0,
                         pitch_shift_in_semitones=float(semis),
                         preserve_formants=False)[0]
        return y.astype(np.float64)[:len(x)], semis
    except Exception:
        return audio, 0                   # shift unavailable: play it as-is


def _add_sample_lanes(preset, kit, sources, shots, variant, dirs, vnotes,
                      key_root=None, low="auto"):
    """Put bass/808 and vocal samples into real lanes (owner phase 2,
    2026-07-23). Both optional and seeded, and each stays out of a 'chords'
    beat's low end / key where it would clash. Reuses the same
    preload-audio-into-a-lane trick the sub and chord lanes use; the render
    ducks every non-kick lane, so both breathe under the kick automatically."""
    rng = random.Random(variant * 907 + 31)
    nbars = bars_of(preset)
    muted = dirs.get("mute", set())

    # BASS 808 sample under the kick. Fires whenever the synth root-sub did
    # not already claim the low end -- the two are one slot, not two.
    #
    # It used to be barred from 'chords' beats outright ("no key there, so
    # an untuned 808 can't clash"). That was true only because nothing knew
    # what note an 808 was, and it cost him the whole 411-file 808 pool on
    # every beat with chords. tools/sort_808s.py now measures each file's
    # root into sample_808_index.json. 2026-09-07 to 09-23 a keyed beat
    # SHIFTED the sample into its key; since 2026-09-23 (owner: "shouldn't
    # need to be pitched or stretched") it picks one RECORDED in the key.
    # Do not bring the shift back without asking him.
    #
    # An 808 whose note could not be read (1 of 411) is barred from a
    # keyed beat -- it can't be shown to be in key.
    #
    # `low` is generate()'s one low-sound call (_low_voice, owner 2026-09-14):
    # this adds exactly that and nothing else. "auto" is a caller that never
    # decided (the benches) and gets the old roll.
    if low == "auto":
        low = ("808" if (shots.get("bass") and "bass" not in muted
                         and "sub" not in preset["lanes"]
                         and "kick" in preset["lanes"]
                         and rng.random() < SAMPLED_BASS_P) else None)
    secs, path, audio, label = 0.8, None, None, "808"
    if low in ("bass", "brass"):
        path, audio = _low_sample(low, key_root, variant, secs)
        label = "synth bass sample" if low == "bass" else "low brass"
        if audio is None and shots.get("bass"):
            low = "808"                      # nothing reached the root
    if low == "808" and audio is None:
        label = "808"
        # NEVER PITCHED OR STRETCHED (owner 2026-09-23): on a keyed beat
        # only an 808 RECORDED in the key's root can play -- it goes in as
        # recorded. (Replaces the 2026-09-07 shift-to-key.) No key: any 808.
        pool = shots
        if key_root:
            from key_context import pitch_class
            notes = _808_notes()

            def _in_key(e):
                try:
                    return (pitch_class(notes.get(e["path"]) or "")
                            == pitch_class(key_root))
                except ValueError:
                    return False
            pool = dict(shots, bass=[e for e in shots.get("bass", [])
                                     if _in_key(e)])
        if pool.get("bass"):
            path, audio = _pick_path(pool, "bass", [], secs,
                                     variant * 71 + 5)
        else:
            vnotes.append("no 808: none recorded in %s" % key_root)
    if low in ("808", "bass", "brass"):
        if path is not None and audio is not None and np.any(audio):
            _pan, _g, (_o, _j, ksw, ks), kbars = preset["lanes"]["kick"]
            brng = random.Random(variant * 631 + 17)
            bbars = (_own_808_bars(kbars, brng)
                     if label == "808" and brng.random() < OWN_808_RHYTHM_P
                     else [b for b in kbars])
            preset["lanes"]["bass"] = (0.0, 0.6, (0, 0, ksw, ks + 9), bbars)
            kit["bass"] = audio
            # sources[lane] must be the RAW path, matching every other
            # lane (build_kit: `sources[lane] = path`) — write_stems reads
            # it with Path(src).stem to name the stem file, kit_paths
            # copies it verbatim for rebuild/swap/anti-repeat history to
            # reload from. A earlier version put a decorated display
            # string here instead ("808 sample: <name>"), which produced
            # a mangled stem filename and, worse, meant a later rebuild
            # tried to re-load that string AS a file path and failed
            # ("...has moved or vanished") — found while checking today's
            # kit_spec fix actually round-trips through a rebuild.
            sources["bass"] = path
            # a real sample pick, same as any drum lane — must register in
            # preset["kit"] or it's invisible to the recipe (kit_spec), and
            # with it the app's stems/swap list and anti-repeat history.
            preset["kit"]["bass"] = ("bass", None, [], secs)
            vnotes.append(("bass %s: %s" if label == "808" else
                           "bass (%s): %s") % (label, Path(path).stem))

    # VOX one-shot — a sparse chant/adlib on a phrase accent (untuned).
    if (shots.get("vox") and "vox" not in muted
            and rng.random() < VOX_LANE_P):
        secs = 0.9
        path, audio = _pick_path(shots, "vox", [], secs, variant * 53 + 9)
        if audio is not None and np.any(audio):
            bars = ["-" * 16 for _ in range(nbars)]
            bars[0] = "X" + "-" * 15                    # downbeat of bar 1
            if nbars > 1:
                bars[-1] = "-" * 14 + "X-"              # '&' of the last bar
            side = round(rng.choice((-1, 1)) * rng.uniform(0.1, 0.25), 2)
            preset["lanes"]["vox"] = (side, 0.5, (0, 0, 50, variant * 17 + 2),
                                      bars)
            kit["vox"] = audio
            sources["vox"] = path                  # raw path — see bass note above
            preset["kit"]["vox"] = ("vox", None, [], secs)
            vnotes.append("vox: %s" % Path(path).stem)


def _wpick(spec, rng):
    """Pick one item from a flat list (['F','G','C']) or a weighted one
    ([['gfunk_minor_i_iv_v', 3], ['vamp_i_iv7', 2]]). None for an empty or
    missing spec, so callers can fall back to their own default."""
    if not spec:
        return None
    if isinstance(spec[0], (list, tuple)):
        items, weights = zip(*spec)
        return rng.choices(list(items), list(weights))[0]
    return rng.choice(spec)


def _source_order(pref, rng, free=False, no_midi=False, no_loop=False):
    """The order to try chord voices for one chord. No signature -> the
    historical default (a sampled loop, else the sampled-instrument
    voice). With a signature `chord_source` (weighted, e.g.
    [['strings',2],['synth',1]]) roll a primary from the weights, then
    fall through the rest of that identity's own sources.

    `free` (pattern_gen.free_beat, owner 2026-09-14: "all djs have all
    instruments"): the primary is rolled from EVERY voice instead — his
    sampled groups, the London strings and the loops — and the identity's
    own sources follow it as the fallback. "chip" stays out: it is the one
    generated voice, and his 2026-07-25 rule keeps it to the identities
    that ask for it.

    "synth" is appended as the last resort, but note what it MEANS now
    (owner 2026-07-23): sampled synth/pluck/pad material out of his own
    banks, via instrument_sampler.VOICES — not an oscillator. The
    synthesized pad that used to be the never-fails floor is deleted, so
    unlike before, every source in this order can fail; _build_chords
    handles the case where they all do.

    `no_midi` (owner 2026-10-29): "midi" is never on the table.
    `no_loop` (owner 2026-10-30): "loop" only as the very last resort."""
    if no_midi and pref:
        pref = [s for s in pref if s[0] != "midi"] or None
    if no_loop and pref:
        pref = [s for s in pref if s[0] != "loop"] or None
    if free:
        import instrument_sampler
        every = sorted(set(instrument_sampler.VOICES) - {"chip"}
                       | {"strings", "loop", "midi"})
        if no_midi:
            every.remove("midi")
        if no_loop:
            every.remove("loop")
        primary = rng.choice(every)
        names = [s[0] for s in pref] if pref else ["loop", "synth"]
    elif not pref:
        return ["synth", "loop"] if no_loop else ("loop", "synth")
    else:
        names = [s[0] for s in pref]
        primary = _wpick(pref, rng)
    order = [primary] + [n for n in names if n != primary]
    if no_loop:
        order = [n for n in order if n != "loop"]
    if "synth" not in order:
        order.append("synth")
    if no_loop:
        order.append("loop")      # only when every instrument failed
    return order


def _split_chord_roles(notes):
    """One chord's notes, split into up to three PARTS instead of one
    stack (owner 2026-07-25, see theory/arrangement.md): support gets the
    root and the 5th at the chord's own register, lead gets whatever
    color tone is left (the 3rd, the note that actually decides
    happy/sad) moved UP an octave, and passing — if the chord has one to
    spare — gets the richest extension (a 7th or a 9th) up another octave
    on top of that, for the rare 3rd part.

    The octave moves are rule 1 from arrangement.md ("different
    heights") made literal: without them, lead's note sits INSIDE
    support's span rather than above it (e.g. support C3+G3 straddles
    lead's plain Eb3) — same notes, same register, not actually
    separated, just relabeled. instrument_sampler.nearest() never fails
    on an out-of-range request (it falls back to the least-bad sample
    instead of None — see its docstring), so moving a note up an octave
    only ever costs a slightly larger pitch-shift, never a silent lane.

    No note is ever handed to two roles: that's the whole fix. A plain
    triad has nothing left over for passing, which is correct, not a
    shortfall — passing is meant to be rare. A bare power chord (root+5th
    only, quality "5") leaves lead empty; the caller reads that as "this
    chord can't be split" and falls back to one part for the whole beat."""
    if len(notes) <= 2:
        return list(notes), [], []
    fifth_i = min(2, len(notes) - 1)
    support = [notes[0], notes[fifth_i]]
    rest = [n for j, n in enumerate(notes) if j not in (0, fifth_i)]
    if len(rest) <= 1:
        return support, [n + 12 for n in rest], []
    return support, [n + 12 for n in rest[:-1]], [n + 24 for n in rest[-1:]]


def _keep_guide_tones(splits, want):
    """Guide tones: the 3rd AND the 7th carry a seventh chord, and the 7th
    must not be dropped (Open Music Theory + Berklee, Hub ch.13 part 2
    rules 8 + 11). On a plain 7th chord _split_chord_roles gives the 7th to
    passing, so on every chord passing doesn't play (`want[k]` False), the
    lead takes it, just above the lead's 3rd. lead_flow beats only."""
    return [(s, l + [l[0] + (p - l[0]) % 12 for p in pa], [])
            if len(l) == 1 and pa and not want[k] else (s, l, pa)
            for k, (s, l, pa) in enumerate(splits)]


def _role_sources(primary, order, own, count):
    """`count` instruments for a multi-part chord — primary first, then
    the identity's OTHER own sources in fallback order. "loop", "midi",
    and "chip" never fill a role (a loop or a MIDI pick is a finished
    part on its own, chip is
    already a fused imitation of a whole chord) — see _build_chords.

    Repeats `primary` when the identity doesn't own `count` distinct
    voices. That's not a shortfall either: one instrument voicing two
    registers of the same chord (a pianist's left hand and right hand)
    is a real, ordinary arrangement, not a fallback."""
    pool = [s for s in order if s in own and s not in ("loop", "chip", "midi")]
    if primary in pool:
        pool.remove(primary)
    srcs = [primary]
    for s in pool:
        if len(srcs) >= count:
            break
        if s not in srcs:
            srcs.append(s)
    while len(srcs) < count:
        srcs.append(primary)
    return srcs[:count]


def _balance_layers(layers, peak_ceiling):
    """Sum a chord slot's layers to check the balance, then hand back the
    ONE shared gain that keeps them at that balance — applied per-layer so
    each stays its own stem (owner 2026-07-25: never re-merge them),
    while the sum still lands at the same loudness a single merged bed
    would have. A single layer needs no correction. `peak_ceiling` is
    chord_synth.PEAK_CEILING, passed in rather than imported here since
    chord_synth is only ever imported locally, inside _build_chords."""
    if len(layers) <= 1:
        return 1.0
    n = min(len(a) for a in layers)
    mix = sum(a[:n] for a in layers)
    g = 10 ** (-18.0 / 20) / (float(np.sqrt((mix ** 2).mean())) + 1e-12)
    peak = float(np.max(np.abs(mix))) * g
    if peak > peak_ceiling:
        g *= peak_ceiling / peak
    return g


def _shareable_preset(preset):
    """The preset as it goes into .recipes/NN.json, with every real-producer
    reference stripped.

    The recipe is a sidecar file that travels next to a beat, so it is the
    one place the internal-only attribution must never reach (owner decision
    2026-07-22, legends_config.json's _readme). Two things carried it and
    both leaked until 2026-07-25:

      `built`      — "J Dilla", "Metro Boomin". Nothing reads it back out of
                     a recipe: the batch-player card reads it live from CREW,
                     and the collab line in the render report is written
                     before this point.
      `_*` keys    — house convention across the configs is that an
                     underscore-prefixed key is documentation, not settings
                     (`_readme`, `_note`, `_horns_status`). The research
                     notes inside `signature._note` name producers in prose,
                     which a `built`-only strip walked straight past.

    Dropped recursively, so a doc key added later is covered without anyone
    remembering this function exists. No code branches on a `_` key — every
    setting _build_chords reads is a plain name.

    Old recipes on disk, written before this, may still contain both.
    """
    def clean(v):
        if isinstance(v, dict):
            return {k: clean(x) for k, x in v.items()
                    if not (isinstance(k, str) and k.startswith("_"))}
        if isinstance(v, list):
            return [clean(x) for x in v]
        return v
    out = clean(preset)
    out.pop("built", None)
    return out


def _pin_bars_for_loop_voice(preset, variant, dirs):
    """OWNER RULE 2026-08-03: "Four bar beats if a loop is being used. The
    loops always seem to be too short for anything else."

    A sampled loop is a fixed length of recorded music. Stretched over an
    8-bar beat it has to repeat itself, which is what makes it sound short.
    So when the chord voice for this beat is going to be a LOOP, the beat is
    pinned to 4 bars. Beats voiced by an instrument keep the normal 4/8 roll.

    Has to run before compose(), which is where the length is rolled — and
    it can, because _source_order is deterministic from `variant` and the
    identity's own chord_source, so the primary voice is knowable up front
    without rendering anything.

    NOTE this reads the same `chords_default` upgrade generate() applies
    later; if that moves, this has to move with it."""
    sig = preset.get("signature") or {}
    dirs = dirs or {}
    if dirs.get("no_chords"):
        return False
    if not (dirs.get("chords") or sig.get("chords_default")):
        return False
    pref = sig.get("chord_source")
    # every DJ/Legend/genre: any instrument or loop on half its beats
    # (owner 2026-10-28, overrides the 30% roll and the genre exemption)
    order = _source_order(pref, random.Random(variant * 461),
                          free=free_beat(variant, SOUND_OPEN_P), no_midi=True,
                          no_loop=True)
    if not order or order[0] != "loop":
        return False
    preset["bar_lengths"] = [4]
    return True


def _one_instrument(used):
    """True when every file in `used` is the SAME instrument.

    OWNER HARD RULE 2026-08-03: "No matter what the situation, one
    instrument per stem." He named the failure exactly — "it's being done
    with piano and strings. It's just creating a noise mess."

    One instrument is NOT the same as one file, and I built it as one file
    first, which was wrong: a real sampled piano is one instrument spread
    over many files (one recording every few notes), so a file count
    rejects a perfectly good piano and forces the engine to fall back to
    some other instrument entirely. Measured: it dropped 1 chord lane in 24
    beats and, worse, silently swapped Timberline's chosen piano for a bell
    because the bell happened to fit in one file.

    Owner's call between the options was (b): same FOLDER and same
    INSTRUMENT TYPE. The folder alone would let a pack that dumps unrelated
    one-shots into one shared bin slip a piano and a bell into the same
    stem; the group check catches that. The group alone is too loose the
    other way — "synth" spans many vendor packs, which is the 2026-07-29
    bug where four packs' sounds landed under one "synth stabs" label.
    """
    paths = [p for p in (used or []) if p]
    if len(paths) < 2:
        return True
    import instrument_sampler
    ident = set()
    for p in paths:
        pp = Path(p)
        # group_of reads the FILE NAME, so a folder of mixed one-shots
        # still resolves per file — which is the point of pairing it with
        # the folder rather than trusting either on its own.
        ident.add((str(pp.parent), instrument_sampler.group_of(pp.stem)))
    return len(ident) == 1


# Owner 2026-08-03: how much of its slot a chord may HOLD before it starts
# decaying. Rolled per slot, so lengths vary inside one beat. The tail then
# runs to silence by the end of the slot, which is what puts a gap between
# one chord and the next instead of a seamless pad.
CHORD_HOLD = (0.40, 0.80)
# REVERSED 2026-08-03, same day it was added. He asked for level variation
# between chords, heard it on beat 1761, and said: "I don't like how the
# samples get louder and quieter like this one. Let's keep those at a steady
# volume." Measured on 1761: its three chord slots peaked at -13.4, -16.4 and
# -9.7 dB — a 6.7 dB spread on ONE sample, which is this 2.5 plus the 1.7 dB
# chord_accents cycle.
#
# 0.0 keeps the machinery in place but flat. The DECAYS stay (he confirmed
# option (a): "every chord starts at the same level; each still holds and
# fades"), so a chord still gets quieter across its own length — what is gone
# is one chord being louder than the next.
CHORD_LEVEL_VAR_DB = 0.0


def _decay_chord_slots(beds, slots, variant):
    """Give every chord slot a hold-then-decay shape and its own level, in
    place.

    `beds` is one list per slot of (audio, name, files); `slots` carries that
    slot's length in seconds. Deterministic from `variant` so a rebuild
    reproduces the same lengths and levels.

    The per-slot gain here is RELATIVE — the chord-bus governor in
    render_crew_beat still sets where the whole bed sits against the kick, so
    varying slots against each other does not fight it."""
    rng = random.Random(variant * 7717 + 23)
    for slot_no, layers in enumerate(beds):
        if slot_no >= len(slots) or not layers:
            continue
        dur = slots[slot_no][3]
        hold = rng.uniform(*CHORD_HOLD)
        lvl = 10 ** (rng.uniform(-CHORD_LEVEL_VAR_DB,
                                 CHORD_LEVEL_VAR_DB) / 20.0)
        for j, (a, nm, fl) in enumerate(layers):
            n = len(a)
            if n < 8:
                continue
            h = max(1, min(n - 2, int(n * hold)))
            env = np.zeros(n)
            env[:h] = 1.0
            # The decay has to FINISH EARLY, not merely reach zero at the
            # slot boundary — a tail that is still audible when the next
            # chord lands is the seamless pad again, just quieter. It runs
            # over 70% of what is left and the rest of the slot is true
            # silence, which is the gap he asked for.
            tail = int((n - h) * 0.7)
            if tail > 1:
                env[h:h + tail] = np.exp(-np.arange(tail) * (9.2 / tail))
            layers[j] = (a * env * lvl, nm, fl)
    return beds


# HARMONY DIET (owner 2026-11-03). Rap lives in minor/dorian/phrygian (Hub
# ch.4); a free roll used to pick all 8 scales at equal odds, so 31% of
# beats came out phrygian/harmonic/dominant/lydian. Lydian and phrygian
# dominant leave the free roll; in character they are cut unless the
# identity lists them in signature.key.keep_modes.
OPEN_MODES = [["minor", 55], ["dorian", 20], ["phrygian", 10],
              ["harmonic_minor", 5], ["major", 5], ["mixolydian", 5]]
OPEN_ROOTS = [["C", 12], ["D", 12], ["F", 12], ["G", 12], ["A", 10],
              ["Bb", 10], ["E", 8], ["Eb", 6], ["Ab", 6], ["F#", 3],
              ["C#", 3], ["B", 3]]
MODE_DIET = {"lydian": 0.4, "phrygian_dominant": 0.4,
             "harmonic_minor": 0.6, "major": 0.8}


def _roll_key(sig, variant, dirs, open_roll, srng, flow=False, diet=False):
    """(key root, mode, progression name or None) for one beat — the three
    harmonic dice _build_chords rolls, in the same order on the same `srng`.
    A reference track's key wins hard; a free beat rolls the whole pool
    (every progression, all twelve roots — owner 2026-09-14, "all keys
    available" — and every mode); otherwise the identity's own signature."""
    import harmony
    from key_context import MODES, SUB_ROOTS
    sig_key = sig.get("key") or {}
    # chord flow: 1-2 chord loops picked half as often (harmony.pick_weights)
    progs = (harmony.pick_weights(sig.get("progressions")) if flow
             else sig.get("progressions"))

    def _any(rng):
        if not flow:
            return rng.choice(harmony.names())
        # jazz-out 2026-10-23: new free beats skip the extension-heavy deep_* loops
        return _wpick(harmony.pick_weights(
            [n for n in harmony.names() if not n.startswith("deep_")]), rng)
    forced = dirs.get("force_key")
    if forced:
        key_root, mode = forced
        prog = dirs["chord_feel"] or (
            _wpick(progs, random.Random(variant * 419 + 5))
            or _any(srng))
    elif open_roll:
        # SUB_ROOTS is only seven and stays that way for the in-character pick
        if diet:
            key_root = _wpick(OPEN_ROOTS, srng)
            mode = _wpick(OPEN_MODES, srng)
        else:
            key_root = srng.choice(sorted(ROOT_HZ))
            mode = srng.choice(sorted(MODES))
        prog = dirs["chord_feel"] or _any(srng)
    else:
        key_root = _wpick(sig_key.get("roots"), srng) or srng.choice(SUB_ROOTS)
        mode = sig_key.get("mode", "minor")
        if isinstance(mode, list):                  # weighted mode list
            if diet:
                keep = set(sig_key.get("keep_modes") or ())
                mode = [[m, w * (1 if m in keep else MODE_DIET.get(m, 1))]
                        for m, w in mode]
            mode = _wpick(mode, srng)
        prog = dirs["chord_feel"] or _wpick(progs,
                                            random.Random(variant * 419 + 5))
    if diet and not forced:
        from key_context import FLATS, pitch_class, uses_flats
        _pc = pitch_class(key_root)
        if uses_flats(_pc, mode):               # F minor is Bb/Eb/Ab, not A#
            key_root = FLATS[_pc]
    return key_root, mode, prog


def _limit_loop_pool(pool, sig, key, variant):
    """signature["loop_pool_only"] (2026-10-11, Tenth Wonder / DJ Hint): this
    DJ's loop voice may ONLY use loops whose path contains the phrase. The
    library-wide pool ranks by key then tempo, and files with no tempo token
    (the Library of Congress excerpts) would never reach the top three
    (loop_voice picks from pool[:3]). Within the allowed files, exact-key
    matches go first and each group is shuffled by `variant`, so the same
    three files do not voice every beat. The result can be EMPTY on purpose:
    loop_voice then returns None and the caller falls through to an
    instrument voice, instead of quietly playing a loop from the wrong
    library. No setting -> the pool comes back untouched."""
    only = (sig.get("loop_pool_only") or "").lower()
    if not only or not pool:
        return pool
    pool = [e for e in pool if only in e["path"].lower()]
    rg = random.Random(variant * 977)
    hit = [e for e in pool if e.get("key") == key.root]
    rest = [e for e in pool if e.get("key") != key.root]
    rg.shuffle(hit)
    rg.shuffle(rest)
    return hit + rest


def _build_chords(preset, kit, sources, variant, dirs, vnotes, voice=None,
                  allow_basses=None, bass808=None, bass_line=True,
                  bass_pick=None, exact=None):
    """Every chord lane's audio: key, progression, and voice (strings vs
    sampled loop vs synth pad), per the DJ's `signature` (or the old
    identity-blind default without one).

    Returns `(midi_chords, harmony)` — or `(None, None)` if this beat has
    no chords. `harmony` (added 2026-07-25, packaging step 1) is the plain
    record of what was decided: key, mode, progression name, and one row
    per chord with its bar, roman numeral, spelling, MIDI notes and the
    voice that actually sounded it. It goes straight into the beat's
    .recipes/NN.json so a beat on disk knows its own harmony instead of
    forgetting it the moment it's written. Read-only bookkeeping — nothing
    here feeds back into the audio.

    Fully deterministic from `variant` — same trick _root_sub already uses
    for the tuned 808 sub — which is what makes it safe to call a SECOND
    time, at rebuild, to regenerate this beat's chord audio (extracted out
    of generate() 2026-07-23 for exactly that: owner asked to "control the
    volume for all sounds", and a chords beat's kit had nothing to reload
    on rebuild since this audio was never a sample file to begin with).
    Reusing the rendered STEM instead was considered and rejected: a stem
    is already panned and sidechain-ducked, so reusing it as a kit source
    would double both.

    If a lane row already exists in `preset["lanes"]` (the rebuild case,
    where a prior trim may already be baked into its gain), that gain is
    PRESERVED — only the pattern (pan/feel/bars) and the audio are
    refreshed, both of which are deterministic reproductions anyway.

    Two honest, narrow limits on an exact rebuild match: (1) a typed
    notes-box mood word ("dreamy") is never persisted past the click it
    was typed for (house rule), so a rebuild without that word can pick a
    different — still valid, still in-signature — progression than the
    one actually audible in the original file. (2) a "loop"/"strings"
    voice draws from a fresh library scan, so if packs changed since the
    original render, the exact sample picked could differ. Both are
    disclosed here rather than silently risked.

    `bass_pick` (a bass file's path, owner 2026-09-26: the bass row's
    dropdown) is the ONE file the bass line plays instead of the seeded
    roll. It touches only the bass block below -- the chord voice, key and
    progression never see it. A path that is no longer in the bass pool
    (moved, or an 808 on a non-808 beat) is ignored and the seeded roll
    stands, so an old pick can't break a rebuild.

    `exact` (owner 2026-09-28, the chord row's second dropdown): the ONE
    instrument inside `voice` to play -- see _exact_voices for the forms.
    Like bass_pick, one that no longer exists is ignored and `voice`
    alone stands."""
    if not dirs["chords"]:
        return None, None
    import chord_rhythm
    import chord_synth
    import harmony
    from key_context import KeyContext
    sig = preset.get("signature") or {}
    srng = random.Random(variant * 353 + 17)
    # OWNER RULE 2026-08-01: "All sounds are open to all DJs, but they try to
    # maintain seventy five percent of their personality within." Measured
    # cause of "I just keep getting the same sounds over and over": each
    # identity could only ever reach its own 2-5 progressions x 3-5 roots x
    # 1-2 modes. Farrow had SIX distinct harmonic outcomes in total; half the
    # roster had 12 or fewer, so ten beats exhausted them.
    #
    # OPEN_P of beats (30% since 2026-09-14, pattern_gen.free_beat) ignore
    # the signature entirely and roll the whole pool — every progression,
    # all twelve roots and every mode. The other 70% stay in character,
    # which is what keeps Otto Grit from sounding like Rage Engine. A typed
    # mood word still beats both.
    open_roll = free_beat(variant)
    # A key taken off a reference track BEATS BOTH (owner 2026-09-01,
    # asked directly: "reference wins, hard"). The progression still
    # rolls in character — only the root and the mode are pinned, so a
    # batch in F minor still sounds like the DJ who made it.
    flow = bool(preset.get("chord_flow"))
    key_root, mode, prog = _roll_key(sig, variant, dirs, open_roll, srng,
                                     flow=flow,
                                     diet=bool(preset.get("harmony_diet")))
    key = KeyContext(key_root, mode)
    gen = preset.get("chord_gen")
    # a rebuild hands back "gen:<style>" as the progression: that means
    # "play the saved generated loop", not a named one
    if gen and str(dirs.get("chord_feel") or "").startswith("gen:"):
        dirs = dict(dirs, chord_feel=None)
    if gen and not dirs.get("chord_feel") and "chords" not in gen:
        # a typed mood word still picks a named loop; otherwise new beats
        # play a generated one. Owner 2026-10-29: every DJ/Legend/genre
        # rolls any of the styles on half its beats (SOUND_OPEN_P, like the
        # sounds); the bass line follows the style the chords picked.
        import chord_gen
        got = chord_gen.generate(
            chord_gen.styles_for(gen.get("who"), sig,
                                 free=free_beat(variant, SOUND_OPEN_P)),
            mode, random.Random(variant * 1201 + 7))
        if got:
            gen.update(got)
    if gen and gen.get("chords") and not dirs.get("chord_feel"):
        prog_name = "gen:%s" % gen["style"]
        chords = harmony.compose_chords(key, gen["chords"])
    else:
        prog_name, chords = harmony.compose(
            key, prog, rng=random.Random(variant * 419 + 5))
    _one = bool(preset.get("one_chord"))
    _pair = False
    if _one:
        _loop = chords
        chords = [harmony.home_chord(key, chords)]
        if preset.get("two_chord") and harmony.wants_two(
                sig, random.Random(variant * 863 + 29)):
            _second = harmony.second_chord(
                key, _loop, chords[0], random.Random(variant * 863 + 31))
            if _second:
                chords = [chords[0], _second]
                _pair = True
    num, den = preset.get("tsig", (4, 4))
    bar_s = num * (4.0 / den) * 60.0 / preset["bpm"]
    nb = bars_of(preset)
    # A progression longer than the loop has bars would silently lose its
    # tail below (`if start_bar >= nb: break`). Nothing in the pool is long
    # enough to hit that today — the longest is 4 chords and the shortest
    # loop is 4 bars — and tests/test_harmony.py pins it so a future 6-chord
    # progression fails loudly instead of arriving half-played.
    per_chord = max(1, nb // len(chords))
    voicing = None
    if flow:
        # chord flow: lay the chords over the loop (uneven lengths, repeats,
        # a turnaround) and voice each one close to the chord before it.
        # Own seed, so none of the older rolls above move.
        # chord colour (2026-10-19): richer chords on the same roots, per
        # the identity's chord_color card. Own seed -> no other roll moves.
        harmony.colorize(key, chords, sig.get("chord_color"),
                         random.Random(variant * 733 + 11), in_key=_one)
        _frng = random.Random(variant * 541 + 23)
        chords = harmony.arrange(key, chords, nb, _frng,
                                 no_half=bool(preset.get("no_halfway")),
                                 turn_ok=not _one)
        voicing = harmony.voice_lead(chords, _frng)
    # the scale the riff / bass / melody pick passing notes from
    _nscale = (harmony.safe_scale_pair(key, chords) if _pair
               else harmony.safe_scale(key, chords[0]["notes"]) if _one
               else key.scale())
    pref = sig.get("chord_source")
    # "arp" = broken-chord riff, "sustain" = held block. A weighted list
    # rolls per beat (Dre's keepers were a mix of both — owner 2026-07-22).
    rhythm_spec = sig.get("chord_rhythm", "sustain")
    # underscored: _render_one below shadows this with its own `rhythm`
    # local (rhythm_override or _rhythm), so every voice can be overridden
    # independently — see _render_one's docstring.
    _rhythm = (_wpick(rhythm_spec, random.Random(variant * 733 + 11))
              if isinstance(rhythm_spec, list) else rhythm_spec)
    # NO ARPS (owner 2026-11-01): "we're no longer using that, in any way,
    # for any DJ or genre". Any old "arp" setting plays held.
    if _rhythm == "arp":
        _rhythm = "sustain"
    # ---- the chord PERFORMANCE grammar (owner build 2026-09-05) ----
    # Every DJ since 2026-09-14, arps half as often (chord_rhythm.spec_for);
    # genre presets still opt in with a top-level `chord_grammar` key. See
    # tools/chord_rhythm.py for why the figure is baked into the slot
    # buffer instead of written into the lane's bar string.
    _grammar = chord_rhythm.spec_for(
        preset, free=free_beat(variant) and not preset.get("genre"))
    # DYN FLOW (2026-10-29): written loud/soft by the style's accent shape
    # (tools/dynamics.py), and the hits logged for the MIDI file
    _dyn = None
    if preset.get("dyn_flow"):
        import dynamics
        _dyn = dynamics.shape_for((preset.get("chord_gen") or {}).get("style"))
    if _grammar and _dyn:
        _grammar = dict(_grammar, dyn=_dyn,
                        plain_soft=bool(preset.get("no_eq")))
    _chord_hits = {}          # slot -> [(t_sec, dur_sec, notes, level)]
    # what the drums are already playing, so the "comp" figure can answer
    # them instead of doubling them. Read BEFORE any chord lane is added.
    # A rebuild hands back the lanes the beat was MADE with (dirs
    # "busy_lanes"), so removing a drum doesn't re-roll the chords'
    # rhythm too (owner 2026-09-27: "remove a sound and all the other
    # sounds change").
    # The drums get a fill and extra lanes AFTER this (add_bass_and_chords),
    # so the finished recipe's lanes aren't what the chords answered: the
    # answer is saved as preset["chord_busy"] and a rebuild replays it
    # (2026-10-30, the drift test caught it on 4 of 30 beats). Beats made
    # before that fall back to the recipe's lanes.
    _busy = dirs.get("busy") or {
        k: list(v[3]) for k, v in
        (dirs.get("busy_lanes") or preset["lanes"]).items()
        if not k.startswith(("chord", "bass", "melody")) and len(v) > 3}
    preset["chord_busy"] = _busy
    # slot -> the chord figure's written bars, so the answer melody can
    # lean away from the cells the chords hit (melody_rhythm)
    _chord_cells = {}
    # only pay for the melodic-loop library scan if a loop voice is on
    # the table (the default, a signature that lists "loop", or the owner
    # asking for it outright from the rack)
    # a free beat's lead voice can be ANY instrument (_source_order), so
    # both libraries have to be on the table for it
    free = open_roll and not preset.get("genre")
    # TEXTURE (riff_gen.py): one per beat, own seed
    _tex, _riff = "full", None
    if preset.get("texture_flow"):
        import riff_gen
        _tex = riff_gen.roll(variant, riff_gen.full_chance(
            sig.get("texture_full"), preset["texture_flow"]))
        if preset.get("no_loop") and _tex != "full":  # no riffs, no loops
            _tex = "two"
        if _tex == "riff" and preset.get("no_midi"):   # riffs are MIDI
            _tex = riff_gen.no_riff(variant)
        if _tex == "riff":
            _riff = riff_gen.pick(
                variant, (preset.get("chord_gen") or {}).get("style"))
    want_loop = (not pref or any(s[0] == "loop" for s in pref)
                 or voice == "loop" or free or _tex == "loop"
                 or preset.get("no_loop"))      # its last resort
    pool = chord_synth.sample_pool(key, preset["bpm"]) if want_loop else []
    if exact and exact.startswith("loop:"):      # his exact loop, alone
        pool = [e for e in pool if e["path"] == exact[5:]] or pool
    # signature["loop_pool_only"] (2026-10-11): see _limit_loop_pool.
    if not (exact and exact.startswith("loop:")):
        pool = _limit_loop_pool(pool, sig, key, variant)
    if (_tex == "loop" and not pool) or (_tex == "riff" and not _riff):
        _tex = "two"                 # nothing to carry it: two notes
    if _tex in ("two", "riff"):
        _grammar = dict(_grammar or chord_rhythm.DEFAULT)
        if _dyn:
            _grammar["dyn"] = _dyn
            _grammar["plain_soft"] = bool(preset.get("no_eq"))
        if preset.get("len_flow"):
            _grammar["len_flow"] = True
        if _tex == "two":            # sparse stabs, never arped
            # len_flow (owner 2026-10-30): some chords held, too
            _grammar["figures"] = [["stab", 3], ["comp", 2]] + (
                [["pad", 1]] if preset.get("len_flow") else [])
    _tonic = 60 + key.pc             # where a riff's 0 sits (C4-B4)
    # same "only scan if it's actually on the table" guard as want_loop
    # above, for the owner's MIDI chord packs (tools/midi_packs.py) —
    # one candidate file per beat, not per chord slot, same reasoning as
    # loop_voice's own pool[:3] top-candidates convention.
    want_midi = not preset.get("no_midi") and (
        (pref and any(s[0] == "midi" for s in pref)) or voice == "midi"
        or free)
    midi_prog, midi_pick_name = None, None
    if want_midi:
        m_pool = chord_synth.midi_pool(key)
        if m_pool:
            m_pick = random.Random(variant * 967).choice(
                m_pool[:chord_synth.MIDI_PICK_TOP])
            # new beats (midi_voice_flow): the MIDI chords stay above the
            # bass line's register (owner 2026-10-24)
            midi_prog = chord_synth.midi_progression(
                m_pick, key, floor=(
                    CHORD_LIFT_FLOOR if preset.get("chord_lift")
                    else chord_synth.MIDI_CHORD_FLOOR
                    if preset.get("midi_voice_flow") else None))
            midi_pick_name = m_pick["name"]
    # every non-strings, non-loop voice is now a SAMPLED instrument out of
    # his own banks (owner 2026-07-23) — "synth" included, so this index is
    # needed for essentially every signature, not just the horn one.
    import instrument_sampler
    import multisample
    # one note-by-note instrument, articulation and layer per group for
    # this whole beat (owner 2026-09-24; see multisample.one_per_beat)
    inst_idx = multisample.one_per_beat(instrument_sampler.scan(),
                                        random.Random(variant * 983 + 41))
    # ONE instrument for the whole MIDI phrase (owner 2026-09-19): piano,
    # organ, guitar, bell or the synth family, chosen once per beat from
    # whichever can cover the phrase's notes.
    midi_group_order = None
    midi_gap = False
    if midi_prog and inst_idx:
        _mnotes = sorted({n for _, _, ns in midi_prog for n in ns})
        _mrng = random.Random(variant * 971 + 13)
        if preset.get("midi_voice_flow"):
            # MIDI VOICE FLOW (owner 2026-10-24): the identity's own
            # researched instruments, never bell or pluck; a free beat
            # keeps every MIDI voice but those two. Nothing of his that
            # reaches the notes -> the London strings play them.
            if free or not pref:
                _allow = [((g,), 1) for g in instrument_sampler.MIDI_VOICES]
            else:
                _allow = [(instrument_sampler.VOICES[s[0]], s[1])
                          for s in pref if s[0] in instrument_sampler.VOICES
                          and s[0] != "chip"]
            midi_group_order = instrument_sampler.midi_groups_for(
                inst_idx, _mnotes, _mrng, _allow)
            if not midi_group_order:
                midi_gap = True
                midi_group_order = tuple(dict.fromkeys(
                    g for gs, w in _allow if w > 0 for g in gs
                    if g not in instrument_sampler.MIDI_NEVER)) or ("synth", "pad")
        else:
            midi_group_order = instrument_sampler.midi_groups(
                inst_idx, _mnotes, _mrng)
    strings_idx = None
    if voice == "strings" or free or midi_gap or (
            pref and any(s[0] == "strings" for s in pref)):
        import string_sampler
        s_all = string_sampler.scan()
        # One style and one mic for the whole beat (owner 2026-09-14). In
        # character: the identity's own articulation on the dry close mic.
        # Free beat: any of his four styles from any of the four mics.
        if free and s_all:
            s_rng = random.Random(variant * 587 + 29)
            s_style = s_rng.choice(sorted({e["style"] for e in s_all}))
            s_mic = s_rng.choice(sorted({e["mic"] for e in s_all}))
        else:
            s_style, s_mic = sig.get("articulation"), string_sampler.CLOSE
        if exact and exact.startswith("style:"):  # the style he picked
            s_style = exact[6:]
        # one low sound per beat: the basses only play when nothing else
        # holds the low end. generate() decides that before the chords and
        # passes it in; a rebuild reads it off the saved lanes.
        if allow_basses is None:
            allow_basses = not _holds_low_end(preset)
        strings_idx = string_sampler.beat_pool(s_all, s_style, s_mic,
                                               basses=allow_basses)
    # A MIDI phrase may instead be voiced on the London strings — exact note,
    # no pitch shift (owner rule) — rather than the sampled instrument family.
    # One choice for the WHOLE phrase (one instrument per lane, same as
    # midi_group_order). Offered to a free beat ("all DJs have all instruments")
    # and to any identity whose chord_source already asks for strings; never
    # forced on an identity that doesn't. Owner 2026-09-20.
    midi_on_strings = bool(
        midi_prog and strings_idx and (midi_gap or ((
            free or (pref and any(s[0] == "strings" for s in pref)))
            and random.Random(variant * 733 + 51).random() < 0.5)))
    # ---- the owner's own pick, made to actually land (2026-08-04) ----
    # Picking "guitar" on the rack used to change nothing: nearest() shops
    # per NOTE across the whole group, so a 3-note chord pulled its notes
    # from two different folders and the one-instrument-per-stem rule
    # (2026-08-03) threw the plan out — every instrument fell through to
    # the DJ's own choice, measured on beat 1776. Pinning his pick to the
    # single folder that can reach every note satisfies both rules at
    # once: it is his instrument, and it is one instrument.
    #
    # ONLY when he picked. A beat the machine makes for itself still
    # ranges over the whole group exactly as before, so this cannot move
    # the sound of anything he didn't ask to change.
    forced_idx = None
    if voice:
        _all_notes = sorted({n for c in chords
                             for n in c.get("voiced", c["notes"])})
        if voice == "strings" and strings_idx:
            forced_idx = _best_folder(
                strings_idx, {e.get("group") for e in strings_idx},
                _all_notes)
            if forced_idx:
                strings_idx = forced_idx
        elif voice in instrument_sampler.VOICES:
            forced_idx = _best_folder(       # [:1] — the named group only
                inst_idx, instrument_sampler.VOICES[voice][:1], _all_notes)
            # the exact instrument he picked (2026-09-28): a note-by-note
            # instrument keeps one recording per note (one_per_beat on just
            # that instrument), his own sound is that one file
            _grp = instrument_sampler.VOICES[voice][0]
            if exact and exact.startswith("multi:"):
                _m, _, _a = exact[6:].rpartition("|")
                forced_idx = multisample.one_per_beat(
                    [e for e in instrument_sampler.scan()
                     if e.get("multi") == _m and e.get("art", "-") == _a
                     and e.get("group") == _grp],
                    random.Random(variant * 983 + 41)) or forced_idx
            elif exact and exact.startswith("file:"):
                forced_idx = [e for e in instrument_sampler.scan()
                              if e["path"] == exact[5:] and not e.get("multi")
                              and e.get("group") == _grp] or forced_idx
    # ---- geometry first, voice second (owner 2026-07-25) ----
    # The voice is committed ONCE for the whole beat, before any audio is
    # kept: the owner heard beat 1174 go strings, strings, choir — the old
    # per-chord fallback swapping instruments mid-beat — and a chord slot
    # going silent when nothing could voice it. Both are gone: a plan
    # either voices EVERY chord in the beat or the next plan takes the
    # WHOLE beat. How many separate melodic PARTS the beat gets (1-3, not
    # a stack) is decided below, once, the same way — see
    # theory/arrangement.md and OWNER_TASTE["melody_part_weights"].
    slots = []
    if flow:
        _at = 0
        for i, chord in enumerate(chords):
            if _at >= nb:
                break
            _b = min(chord["bars"], nb - _at)
            slots.append((i, chord, _at, _b * bar_s))
            _at += _b
    for i, chord in (() if flow else enumerate(chords)):
        start_bar = i * per_chord
        if start_bar >= nb:
            break
        end_bar = nb if i == len(chords) - 1 else \
            min(start_bar + per_chord, nb)
        slots.append((i, chord, start_bar, (end_bar - start_bar) * bar_s))

    _bar0 = {i: sb for i, _c, sb, _d in slots}   # chord slot -> loop bar

    def _lift(ns, ref):
        """`ns` up whole octaves until the CHORD `ref`'s lowest note is at
        C4+ -- the shift comes from the whole chord, so a role's slice
        keeps its place against the other roles."""
        ns = list(ns)
        if preset.get("chord_lift") and ref:
            up = 0
            while min(ref) + up < CHORD_LIFT_FLOOR:
                up += 12
            ns = [n + up for n in ns]
        return ns

    def _render_one(src, chord, dur, used=None, notes=None,
                    rhythm_override=None, pin=None, slot=0):
        """One source, one chord slot -> (audio, voice name). `used` (a
        list) collects the actual FILES the audio came from, so the beat
        can name its own instruments instead of the rack claiming "built
        from scratch" over his own library. The per-source recipes are the
        old per-chord loop's, unchanged — only where they are called from
        moved.

        `notes` overrides which MIDI notes actually sound — the whole
        chord by default, or just one role's slice of it (root+5th for
        the support part, the color tone(s) for lead, see
        _split_chord_roles) when a multi-part beat calls this per role.
        `rhythm_override` likewise overrides the beat's rolled arp/sustain
        choice — the support and passing roles are always held, never
        arpeggiated, regardless of what the lead is doing (owner
        2026-07-25: two parts trading is the point; a "hold" part that
        also arpeggiates isn't holding anything).

        `pin` (owner 2026-07-29): a list, shared across every chord slot
        this beat's caller renders, so every note of the WHOLE beat
        prefers one real source file over hunting a fresh nearest-pitch
        match per note. See instrument_sampler.nearest()'s docstring for
        why — a thin group like "synth" is scattered one-shots from many
        different vendor packs, so per-note picking made one chord sound
        like several different instruments stacked."""
        notes = notes if notes is not None else chord.get("voiced",
                                                          chord["notes"])
        notes = _lift(notes, chord["notes"])
        # "midi" swaps in a real chord someone else already wrote in
        # place of harmony.compose()'s notes, cycling through the
        # picked file's own progression by slot — the same way a
        # normal progression's 2-4 chords already cycle across a beat
        # (see per_chord below). No audio here: a MIDI file is silent
        # by itself, so it still needs a sampled voice to sound —
        # played by his own sampled instruments (owner 2026-07-23: no
        # synthesized chord voice; 2026-09-19: piano/organ/guitar/bell
        # too, one per beat -- see instrument_sampler.midi_groups).
        rhythm = rhythm_override or _rhythm

        def _fig(render_note, render_chord):
            """The grammar's take on this slot as (audio, figure), or None
            when the identity hasn't opted in — then the caller's old
            arp/sustain runs untouched. One roll per slot, seeded off the
            beat so a rebuild matches."""
            if not _grammar or rhythm_override:
                return None                  # support/passing roles hold
            rng = random.Random(variant * 733 + 97 + slot)
            nbars = max(int(round(dur / bar_s)), 1)
            _base = sorted(notes) if src == "midi" else chord["notes"]
            if _tex == "riff":
                import riff_gen
                bars, pitch, length = riff_gen.riff_bars(
                    _riff["notes"], nbars, _bar0.get(slot, 0),
                    {n % 12 for n in _base}, set(_nscale), _tonic)
                _chord_cells[slot] = bars
                _log = [] if slot not in _chord_hits else None
                a = chord_rhythm.render_figure(
                    bars, dur, preset["bpm"], notes, render_note,
                    render_chord, figure="riff", spec=_grammar,
                    seed=variant * 101 + slot, log=_log,
                    riff=(pitch, length))
                if _log and _dyn:
                    _chord_hits[slot] = _log
                if a is not None and _riff["bed"]:
                    bed = render_chord(_lift(riff_gen.two_notes(_base),
                                             _base), dur)
                    if bed is not None:
                        m = min(len(a), len(bed))
                        a = a.copy()
                        a[:m] += bed[:m] * riff_gen.BED_LEVEL
                if a is None or not np.max(np.abs(a)) > 0:
                    return None
                return a, "riff" + (" + bed" if _riff["bed"] else "")
            two = None
            if _tex == "two":
                import riff_gen
                two = _lift((riff_gen.three_notes
                             if preset["texture_flow"] >= 3
                             else riff_gen.two_notes)(_base), _base)
            # Skip the library patterns the last 3 beats of this DJ just
            # played: replay THEIR seeds, so the result depends only on
            # this beat's number and a rebuild still matches.
            _recent = []
            if _grammar.get("library"):
                for _pv in (variant - 1, variant - 2, variant - 3):
                    if _pv >= 0:
                        chord_rhythm.gen_figure(
                            _grammar, random.Random(_pv * 733 + 97 + slot),
                            nbars, busy=_busy, trace=_recent,
                            bar0=_bar0.get(slot, 0))
            figure, bars, shape = chord_rhythm.gen_figure(
                _grammar, rng, nbars, busy=_busy, avoid=tuple(_recent),
                bar0=_bar0.get(slot, 0))
            _long = None
            if _grammar.get("groove_flow") and figure in ("stab", "comp"):
                import groove_lock
                bars, _long = groove_lock.lock_chords(
                    bars, _bar0.get(slot, 0), _busy.get("kick"),
                    random.Random(variant * 1013 + 29 + slot))
            _chord_cells[slot] = bars
            _log = [] if slot not in _chord_hits else None
            a = chord_rhythm.render_figure(
                bars, dur, preset["bpm"], two or notes, render_note,
                render_chord, figure=figure, shape=shape, spec=_grammar,
                seed=variant * 101 + slot, long=_long, log=_log)
            if _log and _dyn:
                _chord_hits[slot] = _log
            # Silence means his library couldn't voice a single step of
            # the figure. Hand back None so the OLD arp/sustain path gets
            # its own try, rather than failing the whole plan — the
            # grammar is a way of playing these notes, not a gate on them.
            if a is None or not np.max(np.abs(a)) > 0:
                return None
            return a, figure
        midi_groups = None
        if src == "midi":
            if not midi_prog:
                return None, None
            _, _, notes = midi_prog[slot % len(midi_prog)]
            notes = _lift(notes, notes)
            if midi_on_strings and strings_idx:
                # the MIDI phrase's notes, voiced on the London strings via the
                # exact-note engine (owner 2026-09-20). Mirrors the src=="strings"
                # branch below; one instrument (strings) for the whole lane.
                cache = {}
                lbl = "midi: %s, strings" % midi_pick_name
                got = _fig(
                    lambda nt, sd: string_sampler.note_slice(
                        strings_idx, nt, sd, cache=cache, used=used, pin=pin),
                    lambda ns, sd: string_sampler.play_chord(
                        strings_idx, ns, sd, used=used, pin=pin))
                if got:
                    return got[0], "%s %s" % (lbl, got[1])
                return (string_sampler.play_chord(
                    strings_idx, notes, dur, used=used, pin=pin), lbl)
            midi_groups = (midi_group_order
                           or instrument_sampler.VOICES["synth"])
        if src == "strings" and strings_idx:
            cache = {}                           # one load per note, not step
            got = _fig(
                lambda nt, sd: string_sampler.note_slice(
                    strings_idx, nt, sd, cache=cache, used=used, pin=pin),
                lambda ns, sd: string_sampler.play_chord(
                    strings_idx, ns, sd, used=used, pin=pin))
            if got:
                return got[0], "strings %s" % got[1]
            return (string_sampler.play_chord(strings_idx, notes, dur,
                                              used=used, pin=pin),
                   "strings")
        if src == "loop":
            # CONSTANT seed — no `+ i`: the same library pick voices every
            # chord slot, so the loop bed can't change sample mid-beat
            a, nm = chord_synth.loop_voice(
                pool, dur, key, rng=random.Random(variant * 461), used=used)
            if a is None:
                return None, None
            # A loop is already a finished melody, so the grammar can't
            # "play" it — it CHOPS it (owner call 2026-09-05, asked in
            # plain language). chop_onsets is the same slicer loop_voice
            # already uses to make a rhythmic file usable as a one-shot;
            # here its pieces get retriggered on the figure's own cells,
            # which is the actual Premier move. No grammar -> the whole
            # loop plays exactly as it always has.
            if _grammar and not rhythm_override:
                import melodic_loops
                clips = melodic_loops.chop_onsets(a, chord_synth.SR)
                if clips:
                    def _clip(_i, sd, _c=clips):
                        c = _c[abs(int(_i)) % len(_c)]
                        return c[:max(int(sd * chord_synth.SR), 1)]
                    got = _fig(_clip, lambda ns, sd: _clip(ns[0], sd))
                    if got:
                        return got[0], ("sample: %s (chopped %s)"
                                        % (nm, got[1]))
            return a, "sample: %s" % nm
        if src == "chip":
            # HIS OWN 8-bit/video-game samples first (owner rule
            # 2026-07-25: "if there are eight bit or sixteen bit or video
            # game sounds in my real library, use those. If there are no
            # sounds that exist fitting that stick with what you have").
            # covers() is an explicit all-notes-in-range test, not
            # nearest()'s least-bad pick, so a group that would only
            # answer by stretching a sample across an octave counts as
            # "doesn't exist" rather than being used badly. Measured
            # today: he owns 2 pitched chip samples, at notes 38 and 70,
            # so this is False for real progressions and the synthesized
            # voice below plays — but the moment he adds a chiptune pack
            # that covers a beat, his own files take over with no code
            # change. That is the rule, implemented rather than decided.
            if inst_idx and instrument_sampler.covers(
                    inst_idx, notes, ("chip",)):
                a = instrument_sampler.play_chord(
                    inst_idx, notes, dur, groups=("chip",),
                    used=used)
                if a is not None and np.max(np.abs(a)) > 0:
                    return a, "8-bit sample stack"
            # ...otherwise the synthesized chip voice: the one synthesized
            # chord voice left in the engine, and a deliberate exception
            # the owner re-confirmed 2026-07-25 — see tools/chip_synth.py's
            # header. Held, never arpeggiated (owner 2026-11-01).
            import chip_synth
            # chip_tuning "atari" -> the TIA's integer-divider grid, out
            # of tune on purpose (New Math).
            tuning = sig.get("chip_tuning", "equal")
            a = chip_synth.chip_chord(notes, dur, tuning=tuning)
            return a, ("chiptune%s"
                       % (" (atari-tuned)" if tuning == "atari" else ""))
        if (src in instrument_sampler.VOICES or midi_groups) and inst_idx:
            # EVERY named instrument voice — "horns", "synth", "piano",
            # "guitar", ... — is sampled from his own banks and
            # pitch-mapped (owner 2026-07-23). "synth" means sampled
            # synth/pluck/pad material, NOT an oscillator. "midi" isn't
            # a real VOICES group — it's forced to the "synth" group
            # above, since a MIDI pick supplies the NOTES but still
            # needs one of his own samples to make a sound.
            groups = midi_groups or instrument_sampler.VOICES[src]
            # An explicit pick means the thing he named, not its backups:
            # "pluck" lists ("pluck", "synth"), so without this, choosing
            # Pluck could hand back a synth and label it Pluck. The backup
            # groups stay in play for beats the machine voices itself.
            if voice and src == voice and not midi_groups:
                groups = groups[:1]
            # Name the group the audio ACTUALLY came from: a thin group
            # hands off to the next one (instrument_sampler.nearest), and
            # a stem shouldn't claim "choir" when the note came from a pad.
            # Reads the pin first if one's already set, so the label
            # matches the source every note actually prefers.
            # his pick plays out of its one pinned folder; everything else
            # ranges over the group as it always has
            idx = forced_idx if (forced_idx and src == voice) else inst_idx
            got = instrument_sampler.nearest(
                idx, notes[0], groups, prefer=pin[0] if pin else None)
            gname = got["group"] if got else src
            if midi_groups:
                gname = "midi: %s, %s" % (midi_pick_name, gname)
            cache = {}                       # one load per file, not step
            got = _fig(
                lambda nt, sd: instrument_sampler.note_slice(
                    idx, nt, sd, cache=cache, groups=groups, used=used,
                    pin=pin),
                lambda ns, sd: instrument_sampler.play_chord(
                    idx, ns, sd, groups=groups, used=used, pin=pin))
            if got:
                return got[0], "%s %s" % (gname, got[1])
            return (instrument_sampler.play_chord(
                idx, notes, dur, groups=groups, used=used, pin=pin),
                "%s stack" % gname)
        return None, None

    # Candidate plans, in the order they get the chance to take the beat:
    # each of the identity's sounds solo (rolled primary first), then —
    # only if none of HIS assigned sounds can cover the whole beat — every
    # other instrument group he owns, shuffled per beat. One plan = one
    # sound for the entire beat. Multi-PART beats (below) are tried first
    # and separately — this list is the single-part fallback.
    # every DJ/Legend/genre: any instrument or loop on half its beats
    # (owner 2026-10-28, overrides the 30% roll and the genre exemption)
    order = _source_order(pref, random.Random(variant * 461),
                          free=free_beat(variant, SOUND_OPEN_P),
                          no_midi=bool(preset.get("no_midi")),
                          no_loop=bool(preset.get("no_loop")))
    if _tex == "loop" and not voice:
        order = ["loop"] + [s for s in order if s != "loop"]
    elif _tex in ("two", "riff") and not voice and order[0] == "loop":
        order = order[1:] + ["loop"]      # a loop would play over it
    plan_rng = random.Random(variant * 883 + 7)
    own = [s[0] for s in pref] if pref else []
    plans = [(s,) for s in order]
    # then every OTHER instrument group he owns. "chip" is excluded on
    # purpose: it is the one generated voice, so it may only play for an
    # identity whose own chord_source asks for it (New Math, Chiptune,
    # Farrow's 1-in-6) — never as a substitute for his instruments.
    # Without this it became a universal fallback that always succeeds,
    # which is the opposite of the owner's hard rule (2026-07-25).
    #
    # signature `chord_fallback` (owner 2026-09-24, Chiptune: "borrow
    # bells/plucks only") narrows that list for one identity, so a beat its
    # own sounds can't cover borrows a sound that still fits it instead of
    # piano or brass. Absent -> every group, exactly as before.
    extra = [g for g in (sig.get("chord_fallback")
                         or instrument_sampler.VOICES)
             if g not in order and g != "chip"]
    plan_rng.shuffle(extra)
    plans += [(g,) for g in extra]
    if preset.get("no_loop"):        # a loop only after every instrument
        plans = [p for p in plans if p != ("loop",)] + [("loop",)]
    # The owner picking an instrument on the rack (2026-08-04) puts it at
    # the FRONT of the queue rather than replacing the queue: the plans
    # below are tried in turn and the first that can voice every chord
    # wins, so his choice plays whenever it can, and a voice his library
    # can't actually cover falls through to the DJ's own order instead of
    # printing a beat with a silent instrument. "chip" is allowed here
    # even though it is excluded from `extra` — the exclusion stops it
    # being a universal fallback, not an explicit request.
    if voice:
        plans = [(voice,)] + [p for p in plans if p != (voice,)]

    committed, beds = None, None

    # ---- how many separate melodic PARTS, not one stack (owner
    # 2026-07-25: "individual instruments... not everything stacked on
    # top of each other, playing the same thing. one or two samples at a
    # time... up to three"). See theory/arrangement.md for the actual
    # arranging rules this follows. A loop is already a finished melody
    # and the chip voice is already a fused chord — neither ever combines
    # with another part, so they always stay at one.
    primary = order[0]
    # How many separate melodic PARTS (owner 2026-07-25): "individual
    # instruments... not everything stacked... one or two... up to three".
    # Each part is its OWN lane with its OWN single instrument — _one_instrument
    # guards against combining two instruments WITHIN a lane, while different
    # lanes are free to use different instruments. That is the "one instrument
    # per LANE" rule.
    #
    # This restores the weighted 1/2/3-part roll. It OVERRULES the 2026-07-29
    # whole-beat clamp (`part_count = 1`): owner 2026-09-20 clarified that rule
    # was only ever meant to be per-lane, not one instrument for the entire
    # beat. The "noise mess" it was patching came from combining instruments
    # inside one lane, which _one_instrument still prevents.
    #
    # A loop is a finished melody, and chip/midi are already self-voiced picks
    # (a fused chord / a written phrase), so a beat led by one of those stays a
    # single part — they never split into roles.
    # An explicit instrument pick (voice) means "play the chords on THIS
    # instrument" — one instrument, his choice, never auto-layered over. Loops
    # and chip/midi are self-voiced picks, so they stay single too. Everything
    # else the machine voices itself may layer.
    if voice or primary in ("loop", "chip", "midi") or _tex in ("two",
                                                                 "riff"):
        part_count = 1
    else:
        part_count = random.Random(variant * 617 + 5).choices(
            (1, 2, 3), weights=OWNER_TASTE[
                "lead_part_weights" if preset.get("lead_flow")
                else "melody_part_weights"])[0]

    # Melody beats (2026-10-19): the lead keeps the chord rhythm and the
    # melody answers in its gaps, an octave-plus ABOVE it (Hub ch.04 §11 +
    # 2026 producer guides: separate by height first, then by time).
    import melody_rhythm
    _mel_on = bool(preset.get("melody_flow") and (num, den) == (4, 4)
                   and primary not in ("loop", "chip", "midi")
                   and _tex != "riff"             # the riff IS the line
                   and melody_rhythm.plays(variant))
    _lead_top = {}
    # which layer a double copies (band_flow): the lead on a multi-part
    # beat -- it carries the chord rhythm -- else the one whole-chord layer
    _dbl_v, _dbl_notes = 0, (lambda k: None)
    if part_count >= 2:
        role_srcs = _role_sources(primary, order, own, part_count)
        splits = [_split_chord_roles(chord["notes"])
                  for _, chord, _, _ in slots]
        if voicing in ("smooth", "open"):
            # chord flow: each part glides to its nearest octave instead of
            # every part jumping with the root (same split, same notes)
            splits = harmony.lead_parts(splits)
        # which chords the rare passing part plays (rolled per slot)
        want = [part_count >= 3 and bool(splits[k][2]) and random.Random(
                    variant * 991 + 43 + i).random()
                < OWNER_TASTE["passing_note_p"]
                for k, (i, _, _, _) in enumerate(slots)]
        if preset.get("lead_flow"):
            splits = _keep_guide_tones(splits, want)
        # a bare power chord has no lead note to split off -> single part
        role_ok = all(lead_n for _, lead_n, _ in splits)

        def _whole_role(src, role, pick):
            """One ROLE across EVERY chord slot on ONE instrument -> list of
            per-slot (audio, name, files) or None. `pick(k)` says whether
            slot k plays this role at all (passing is optional).

            OWNER 2026-09-25 (beat 2876): "I don't want instruments reaching
            for other instruments in the same lane." Before this the roles
            were rendered chord by chord with no pin and no one-instrument
            check, so the lead could be a trombone on chord 1 and a muted-horn
            loop on chord 2 (beats 2827, 2832, 2866). His pick was "lock +
            pick another": the caller tries the next family if this fails."""
            pin, out, every = [], [], []
            for k, (i, chord, _, dur) in enumerate(slots):
                if not pick(k):
                    out.append(None)
                    continue
                used = []
                a, nm = _render_one(
                    src, chord, dur, used=used, notes=splits[k][role],
                    slot=i, pin=pin,
                    rhythm_override=None if role == 1 else "sustain")
                if a is None or not np.max(np.abs(a)) > 0:
                    return None
                every += used
                out.append((a, "%s (%s)" % (nm, ("support", "lead",
                                                 "passing")[role]), used))
            # the WHOLE beat, not one chord: one instrument for the lane
            return out if _one_instrument(every) else None

        def _lock_role(role, pick):
            cands = [role_srcs[role]] + [
                s for s in order if s in own and s != role_srcs[role]
                and s not in ("loop", "chip", "midi")]
            for src in cands:
                got = _whole_role(src, role, pick)
                if got is not None:
                    role_srcs[role] = src
                    return got
            return None

        per_role = []
        if role_ok:
            for role in (0, 1):
                got = _lock_role(role, lambda k: True)
                if got is None:
                    role_ok = False
                    break
                per_role.append(got)
        if role_ok and part_count >= 3:
            # passing is never fatal and only plays SOME chords (owner:
            # "the sparsest, easiest to cut") — rolled per slot above
            if any(want):
                got = _lock_role(2, lambda k: want[k])
                if got is not None:
                    per_role.append(got)
        if role_ok:
            role_beds = []
            for k in range(len(slots)):
                layers = [r[k] for r in per_role if r[k] is not None]
                g = _balance_layers([a for a, _, _ in layers],
                                    chord_synth.PEAK_CEILING)
                n = min(len(a) for a, _, _ in layers)
                role_beds.append([(a[:n] * g if g != 1.0 else a[:n], nm, fl)
                                  for a, nm, fl in layers])
            committed, beds = tuple(role_srcs[:len(per_role)]), role_beds
            _dbl_v, _dbl_notes = 1, (lambda k: splits[k][1])
            _lead_top = {i: max(splits[k][1])
                         for k, (i, _, _, _) in enumerate(slots)}

    if committed is None:
        for plan in plans:
            beds, ok = [], True
            # one preferred source per src in this plan, shared across
            # EVERY chord slot below — owner 2026-07-29, see _render_one's
            # `pin` doc. Fresh per plan attempt: a failed plan's picks
            # must not leak into the next candidate's.
            pins = {}
            for i, chord, start_bar, dur in slots:
                layers = []
                for src in plan:
                    used = []
                    a, nm = _render_one(src, chord, dur, used=used,
                                        slot=i,
                                        pin=pins.setdefault(src, []))
                    # arp_riff hands back SILENCE (not None) when every
                    # step was unvoiceable — an all-zero buffer is a
                    # failure too
                    if a is None or not np.max(np.abs(a)) > 0:
                        ok = False
                        break
                    # OWNER HARD RULE 2026-08-03: "No matter what the
                    # situation, one instrument per stem." Before this, a
                    # chord's notes were picked one at a time by nearest
                    # pitch, so a thin group could answer each note from a
                    # different vendor pack and print four instruments under
                    # one "synth stabs" label. 2026-07-29 softened that to a
                    # PREFERENCE (reuse one sample within 12 semitones) with
                    # the ceiling written into the comment — and a preference
                    # with a documented escape hatch is what kept leaking.
                    # This is the invariant instead: more than one source
                    # file fails the plan outright, and if no plan can voice
                    # the chord from a single instrument the chord lane is
                    # dropped from the beat (his call, option c).
                    if not _one_instrument(used):
                        ok = False
                        break
                    layers.append((a, nm, used))
                if not ok:
                    break
                g = _balance_layers([a for a, _, _ in layers],
                                    chord_synth.PEAK_CEILING)
                n = min(len(a) for a, _, _ in layers)
                beds.append([(a[:n] * g if g != 1.0 else a[:n], nm, fl)
                            for a, nm, fl in layers])
            # per-slot check above isn't enough: the pin is only a
            # preference, so chord 2 could still land on another pack. One
            # instrument per source across the WHOLE beat (owner 2026-09-25).
            if ok and beds and all(
                    _one_instrument([f for bed in beds for f in bed[v][2]])
                    for v in range(len(plan))):
                committed = plan
                break

    # OWNER RULE 2026-08-03: "when they are on the track, I don't want them
    # being played nonstop. Decays and variation in length should be
    # present." Measured before this: the chord bus was sounding 95% of the
    # loop against the kick's 34% — each chord filled its whole slot and the
    # next one started the instant it ended, so there was a continuous pad
    # under everything with no gaps anywhere.
    #
    # Every slot now HOLDS for part of its length and then DECAYS to silence
    # before the next chord lands. The hold fraction is rolled per slot, so
    # the chords are different lengths within one beat as well as between
    # beats. One place, after both plan paths above have settled `beds`, so
    # it covers all four voice sources (strings / instrument / loop / chip).
    # DOUBLE (band_flow, owner 2026-10-21; Reason demo Power plays one chord
    # on 4 instruments): a second instrument plays the SAME notes and hits
    # as the main part, on its own lane (the last layer of every slot).
    # Same seeds, so the hits land together. Overrules 2026-07-25 "never
    # the same thing twice". An explicit instrument pick or a loop/chip/MIDI
    # lead stays single. `_dbl` = (pair?, side) for the pan below.
    _dbl = None
    if (beds and committed and preset.get("band_flow") and not voice
            and not set(committed) & {"loop", "chip", "midi"}):
        _dr = random.Random(variant * 1523 + 61)
        if _dr.random() < OWNER_TASTE["double_p"]:
            _pair = _dr.random() < OWNER_TASTE["double_pair_p"]
            _side = _dr.choice((-1.0, 1.0))
            for src in dict.fromkeys(order + extra):
                if src in committed or src in ("loop", "chip", "midi"):
                    continue
                pin, got, every = [], [], []
                for k, (i, chord, _sb, dur) in enumerate(slots):
                    used = []
                    a, nm = _render_one(src, chord, dur, used=used,
                                        notes=_dbl_notes(k), slot=i, pin=pin)
                    if a is None or not np.max(np.abs(a)) > 0:
                        got = None
                        break
                    every += used
                    got.append((a, nm, used))
                if not got or not _one_instrument(every):
                    continue
                # one gain for the whole lane: the double peaks where the
                # part it copies peaks, then each slot is re-balanced
                ref = max(float(np.max(np.abs(bed[_dbl_v][0])))
                          for bed in beds)
                pk = max(float(np.max(np.abs(a))) for a, _, _ in got)
                for k, (a, nm, fl) in enumerate(got):
                    layers = beds[k] + [(a * (ref / pk), "%s (double)" % nm,
                                         fl)]
                    g = _balance_layers([x for x, _, _ in layers],
                                        chord_synth.PEAK_CEILING)
                    n = min(len(x) for x, _, _ in layers)
                    beds[k] = [(x[:n] * g, m, f) for x, m, f in layers]
                _dbl = (_pair, _side)
                vnotes.append("double: %s also on %s%s" % (
                    ("lead" if _dbl_v else "chords"), got[0][1],
                    ", left/right pair" if _pair else ""))
                break
    if beds:
        _decay_chord_slots(beds, slots, variant)

    # Owner's hard rule has a consequence he chose explicitly (option c):
    # when no single instrument in his library can voice this chord, the
    # beat ships with NO chord lane rather than with two instruments glued
    # into one stem. Say so on the beat card — a chords beat that arrives
    # without chords should be explained, not silently drummed.
    if committed is None:
        vnotes.append("no chords: no single instrument could voice this "
                      "progression on its own")
        return None, None

    # ---- the bass line: back on (owner 2026-09-16 reversed the
    # 2026-07-29 hard rule) ----
    # The melodic bassline (chordbass family, bass0..N) had been off
    # entirely since 2026-07-29 because he wanted to play it himself in
    # Reason. Owner 2026-09-16: "allow them" -- the block traces back to
    # that rule, not a classifier gap, and he wants it back. Restored to
    # its pre-2026-07-29 behavior: his own bass one-shots (role "bass"
    # in the melodic index, instrument_sampler.scan_bass()) voice the
    # bassline one root at a time; per owner rule 2026-07-25, a bass
    # sample voiced as a full CHORD is still mud, so scan() (used for
    # the chord lanes above) keeps excluding role=="bass" -- only this
    # dedicated bass lane uses them. No notes-box opt-out exists yet
    # (removed along with the rest of the old mechanism in 2026-07-29);
    # add one if he wants a per-beat "no bass" escape hatch back.
    bass_beds, bass_files, bcache = {}, {}, {}
    if bass808:
        # REBUILD ONLY since 2026-09-23 (second pass): new beats never pass
        # bass808 -- their 808 hits with the kick on the "bass" lane. This
        # keeps beats made earlier that day rebuilding the way they were made.
        # THE 808 IS THE BASS LINE (owner 2026-09-23, BASS_808_DJS): his
        # one picked 808 -- (path, audio) -- re-pitched onto each chord's
        # root the shortest way round ("fine, it's my sample"). An 808
        # whose note was never measured can't be tuned: no line at all.
        p808, a808 = bass808
        for i, chord, start_bar, dur in slots:
            a, _semis = _808_to_key(p808, a808, chord["notes"][0])
            if a is None:
                bass_beds, bass_files = {}, {}
                break
            bass_beds[i] = a
            bass_files[i] = p808
    # ONE BASS SOUND PER BEAT (owner hard rule 2026-09-23, beat 2807: the
    # line went guitar bass / 808 / unison bass / guitar bass because every
    # chord picked its own nearest file). The line's single file is chosen
    # ONCE, near the middle of its roots, and every root is voiced from an
    # index holding only that file -- nothing else is reachable. And no 808
    # files: an 808 DJ's line is the bass808 branch above; everyone else
    # plays a real bass line (owner 2026-09-23).
    bass_idx = None if (bass808 or not bass_line) else [
        e for e in instrument_sampler.scan_bass()
        if "808" not in Path(e["path"]).name]
    bass_oct = 0
    bass_plan, bass_notes = None, None
    if bass_idx:
        roots = [chord["notes"][0] - 12 for _i, chord, _s, _d in slots]
        mid = (min(roots) + max(roots)) / 2.0

        def _oct(e):
            # whole octaves that bring the line's middle to this file
            return int(round((e["note"] - mid) / 12.0))

        def _gap(e):
            return abs(e["note"] - (mid + 12 * _oct(e)))
        # EVERY bass file is a candidate (owner 2026-09-25: "the same
        # instrument almost every time"). Was: only files within 4 notes
        # of the line's pitch -- his bass files sit at notes 24-31 and the
        # line near 36-45, so 1-2 files ever qualified. Now the LINE moves
        # by whole octaves to meet the file (same notes, other octave).
        near = [e for e in bass_idx
                if _gap(e) <= instrument_sampler.MAX_SHIFT] or bass_idx
        pick = next((e for e in bass_idx if bass_pick
                     and str(e["path"]) == str(bass_pick)), None)
        _explicit = pick is not None     # a Bass-folder file he picked
        if pick is None:
            pick = random.Random(variant * 29 + 3).choice(near)
        bass_idx, bass_oct = [pick], 12 * _oct(pick)
        _fnote = pick.get("pitch", pick["note"])
        # ALTERNATE BASS SOUNDS (2026-10-19, tools/bass_voices.py): on new
        # beats the ONE bass sound may be an orchestral bass, cello, piano,
        # guitar, organ or synth that really has the notes; None keeps the
        # Bass-folder file picked above. A rebuild rolls the same sound
        # (seeded from the variant).
        _alt = None
        if preset.get("bass_voice_flow") and not _explicit:
            import bass_voices
            import string_sampler
            _alt = bass_voices.choose(
                variant, roots, preset, strings=string_sampler.scan,
                instruments=instrument_sampler.scan, cache=bcache)
            if _alt:
                bass_oct = _alt["oct"]
        _fits = (_alt["fits"] if _alt else (
            lambda n: abs(n - _fnote) <= instrument_sampler.PREFER_MAX_SHIFT))

        def _bass_voice(used):
            if _alt:
                return _alt["make_render"](bcache, used, bar_s / num)
            return lambda n, secs: instrument_sampler.voice_note(
                bass_idx, n, secs, cache=bcache, used=used,
                snap_sec=bar_s / num)
        # BASS GROOVE (2026-10-19, tools/bass_rhythm.py): new beats play a
        # real bass figure -- kick-locked, walking, pushed, funk... -- with
        # the kick's swing, instead of one held root per chord. The whole
        # line is ONE loop-length buffer, cut at the slot starts so the
        # bass{i} lanes stay as they were. Old beats (no stamp) and odd
        # meters keep the held root below.
        if preset.get("bass_flow") and (num, den) == (4, 4):
            import bass_rhythm
            _fnote = pick.get("pitch", pick["note"])
            _bslots = [{"root": c["notes"][0] - 12 + bass_oct,
                        "chord_root": c["notes"][0],
                        "tones": list(c["notes"]),
                        "bars": max(1, int(round(d / bar_s))),
                        "start_bar": sb} for _i, c, sb, d in slots]
            _kick = preset["lanes"].get("kick")
            bass_plan = bass_rhythm.plan_line(
                _bslots, _kick[3] if _kick else None,
                bass_rhythm.spec_for(preset), variant,
                _fits, _nscale, in_key=_one)
            _ccells = [_chord_cells.get(_i) for _i, _c, _sb, _d in slots]
            if (preset.get("band_flow") and any(_ccells)
                    and random.Random(variant * 1531 + 67).random()
                    < OWNER_TASTE["bass_chord_lock_p"]):
                # bass on the chords' rhythm (the kick-clear lock is the
                # other style, below)
                import groove_lock
                groove_lock.bass_from_chords(bass_plan, _bslots, _ccells)
                vnotes.append("bass: plays the chord rhythm")
            elif preset.get("groove_flow"):
                import groove_lock
                groove_lock.lock_bass(bass_plan, _bslots,
                                      _kick[3] if _kick else None,
                                      variant, _fits)
            _end = int(round(nb * bar_s * instrument_sampler.SR))
            bused = []
            line, bass_notes = bass_rhythm.render_line(
                bass_plan, _bslots, bar_s, preset["bpm"], _end,
                _bass_voice(bused),
                bass_rhythm.kick_feel(preset["lanes"], variant * 887 + 7),
                dyn=_dyn, plain_soft=bool(preset.get("no_eq")))
            if line is None:
                bass_plan = None         # keep today's held root
            else:
                # the render's own trigger sample for each slot; each
                # piece stops ONE sample short of the next trigger so the
                # low-end choke sees a note that ended, not one it must
                # cut -- the line is already one note at a time
                _pos = [int(sb * bar_s * instrument_sampler.SR)
                        for _i, _c, sb, _d in slots] + [_end]
                for k, (i, _c, _sb, _d) in enumerate(slots):
                    bass_beds[i] = line[_pos[k]:max(_pos[k + 1] - 1,
                                                    _pos[k] + 1)]
                    bass_files[i] = bused[0] if bused else None
        for i, chord, start_bar, dur in (() if bass_plan else slots):
            bused = []
            a = _bass_voice(bused)(chord["notes"][0] - 12 + bass_oct, dur)
            if a is None:
                bass_beds, bass_files = {}, {}
                break
            bass_beds[i] = a
            bass_files[i] = bused[0] if bused else None

    # Pan was hardcoded 0.0 on every chord lane. It is a real lane field
    # that the render loop already honours (constant-power, same as the
    # drums) — it just had no config path. Opted-in identities can now
    # place their chords; everyone else still gets dead centre.
    _chord_pan = float(_grammar.get("pan", 0.0)) if _grammar else 0.0
    midi_chords = []
    chord_rows = []
    voice_desc = None
    voice_files = {}          # lane -> the library files it actually used
    voice_names = {}          # lane -> which INSTRUMENT it is ("horns stack")
    for slot_no, (i, chord, start_bar, dur) in enumerate(slots):
        bass_note = chord["notes"][0] - 12
        bars_list = ["-" * 16 for _ in range(nb)]
        bars_list[start_bar] = "X" + "-" * 15
        # traditional dynamics: the downbeat leans, the repeats ease off,
        # instead of every bar landing at an identical level (owner
        # 2026-07-25). Deterministic from the slot, so a rebuild matches.
        accent = _ACCENTS[slot_no % len(_ACCENTS)]
        old_b = preset["lanes"].get(f"bass{i}")
        if bass808 and "kick" in preset["lanes"]:
            # the 808 plays on the KICK's hits inside this chord's bars,
            # with the kick's swing -- kick and 808 built as one unit, the
            # way the old single 808 lane copied the kick. The render cuts
            # each note at the next one (crew: one bass note at a time).
            _kp, _kg, (_ko, _kj, ksw, ks), kbars = preset["lanes"]["kick"]
            _end_bar = start_bar + max(1, int(round(dur / bar_s)))
            b808 = [kbars[b % len(kbars)] if start_bar <= b < _end_bar
                    else "-" * len(kbars[b % len(kbars)]) for b in range(nb)]
            # ...and every chord change re-strikes it on its downbeat, kick
            # or no kick. Without this a chord whose bars the kick skips
            # kept the LAST chord's 808 ringing under it, a wrong note.
            if b808[start_bar][:1] == "-":
                b808[start_bar] = "X" + b808[start_bar][1:]
            preset["lanes"][f"bass{i}"] = (
                0.0, old_b[1] if old_b else 0.78, (0, 0, ksw, ks + 9), b808)  # 2026-10-20 owner: 808 baseline +30% (0.6 x 1.3)
        else:
            # a grooved line is one performance cut into slots: one gain
            # for every slot, so a note tied across a chord change doesn't
            # jump in level -- its accents are written into the figure
            preset["lanes"][f"bass{i}"] = (0.0,
                                           old_b[1] if old_b
                                           else _BASS_GAIN * (
                                               1.0 if bass_plan else accent),
                                           (0, 0, 50, variant + i),
                                           [b for b in bars_list])
        if committed:
            voice_desc = " + ".join(nm for _, nm, _ in beds[slot_no])
            # ONE LANE PER INSTRUMENT. Voice 0 keeps the plain chord{i}
            # key so every beat made before today still loads; a second
            # layered instrument gets chord{i}v1, and the rack shows it
            # as its own row with its own stem, volume and remove button.
            for v, (audio, nm, files) in enumerate(beds[slot_no]):
                lane = f"chord{i}" if v == 0 else f"chord{i}v{v}"
                old_c = preset["lanes"].get(lane)   # preserve a baked trim
                _pan = _chord_pan
                if _dbl and _dbl[0] and v in (_dbl_v, len(beds[slot_no]) - 1):
                    # L/R pair: the copied part one side, its double the
                    # other (Power's Piano L / Piano R)
                    _pan = _dbl[1] * OWNER_TASTE["double_pair_pan"] * (
                        1.0 if v == len(beds[slot_no]) - 1 else -1.0)
                # SAME feel seed for every voice of a slot, so two
                # layers of one chord land together. The lane feel tuple
                # stays (0, 0, 50): a chord lane's single X triggers the
                # WHOLE slot buffer, so lane-level offset/jitter/swing
                # would shift the entire block, not its hits. Since
                # 2026-09-05 the performance — hits, swing, jitter,
                # written dynamics — is baked INSIDE that buffer by
                # chord_rhythm for identities that opted in; see its
                # header for why it can't live out here.
                preset["lanes"][lane] = (_pan,
                                         old_c[1] if old_c
                                         else _CHORD_GAIN * accent,
                                         (0, 0, 50, variant + i),
                                         [b for b in bars_list])
                kit[lane] = audio
                sources[lane] = "%s, %s (%s)" % (nm, chord["chord"],
                                                 chord["roman"])
                voice_names[lane] = nm
                # the real files behind this lane, so the rack can name them
                for f in files:
                    voice_files.setdefault(lane, []).append(f)
        if bass_beds:
            kit[f"bass{i}"] = bass_beds[i]
            src_name = Path(bass_files[i]).stem if bass_files.get(i) else None
            sources[f"bass{i}"] = "%s, %s root" % (
                src_name or "sampled bass", chord["chord"])
            if bass_files.get(i):
                voice_files.setdefault(f"bass{i}", []).append(bass_files[i])
        else:
            # No synthesized substitute (owner 2026-07-25, hard rule: "the
            # only thing I want rendered from you is the chip tune pack,
            # all other instruments mine every time"). If his own bass
            # samples can't voice every root, the beat gets no bass lane
            # rather than a generated one — the kick and its tuned root
            # still carry the low end.
            preset["lanes"].pop(f"bass{i}", None)
        _mc = {"start_sec": start_bar * bar_s, "dur_sec": dur,
               "notes": chord.get("voiced", chord["notes"]) + [bass_note]}
        if _chord_hits.get(i):
            # dyn flow: the chords track plays the figure's real hits at
            # their written loud/soft, not one held block at velocity 90
            _mc["hits"] = [(t, d, list(ns), int(min(127, max(1, round(127 * v)))))
                           for t, d, ns, v in _chord_hits[i]]
        if bass_plan and bass_beds:
            # the real line goes to its own MIDI track (write_midi), not a
            # held root inside the chords
            _mc["notes"] = list(chord.get("voiced", chord["notes"]))
            _mc["bass_line"] = [(t, min(d, nb * bar_s - t), n,
                                 int(min(127, max(1, round(127 * v)))))
                                for t, d, n, v in bass_notes[slot_no]]
        midi_chords.append(_mc)
        chord_rows.append({"bar": start_bar + 1,      # 1-based, as counted
                           "roman": chord["roman"],
                           "chord": chord["chord"],
                           "notes": list(chord.get("voiced", chord["notes"])),
                           "bass": bass_note,
                           "voice": voice_desc})
    # ANSWER MELODY (2026-10-19, tools/melody_rhythm.py; owner pick: its
    # own part, about half of beats). A short tune in the chords' gaps on
    # ONE of his instruments, not the chords' own family. One loop-length
    # buffer on lane melody0, triggered once on bar 1. New beats only
    # (melody_flow stamp); a loop/chip/MIDI-led beat already has its one
    # melodic part (theory/arrangement.md), so it gets none.
    melody_info = None
    # rebuilt fresh every time (a rebuild keeps the trimmed level/pan)
    old_m = preset["lanes"].pop("melody0", None)
    kit.pop("melody0", None)
    if _mel_on and committed:
        _mslots = [{"tones": list(c.get("voiced", c["notes"])),
                    "top": max(list(c.get("voiced", c["notes"]))
                               + [_lead_top.get(_i, 0)]),
                    "start_bar": sb, "bars": max(1, int(round(d / bar_s)))}
                   for _i, c, sb, d in slots]
        _mcells = {}
        for _i, _c, sb, _d in slots:
            for b, bar in enumerate(_chord_cells.get(_i) or ("X",)):
                _mcells.setdefault(sb + b, set()).update(
                    k for k, ch in enumerate(bar) if ch != "-")
        _diet = bool(preset.get("harmony_diet"))
        _mscale = (melody_rhythm.melody_scale(
            _nscale, key.pc, key.mode,
            (sig.get("key") or {}).get("keep_modes") or ()) if _diet
            else _nscale)
        _mhits = melody_rhythm.plan_phrase(
            _mslots, _mscale, melody_rhythm.spec_for(preset), variant,
            nb, _mcells, flow=int(preset.get("melody_flow") or 1))
        _by_path = {e["path"]: e for e in inst_idx}
        _avoid = {(_by_path.get(f) or {}).get("group")
                  for ln, fs in voice_files.items() if _CHORD_LANE.match(ln)
                  for f in fs}
        _ments, _mshift = melody_rhythm.pick_instrument(
            inst_idx, [n for _b, _s, _c, n in _mhits], _avoid, variant,
            floor=max(s["top"] for s in _mslots), diet=_diet,
            allow_bell=any(r[0] == "bell" and r[1] for r in
                           (sig.get("chord_source") or [])
                           if isinstance(r, (list, tuple))))
        if _ments and _mhits:
            _mhits = [(b, st, ch, n + _mshift) for b, st, ch, n in _mhits]
            _end = int(round(nb * bar_s * instrument_sampler.SR))
            mused, mcache = [], {}
            mline, mnotes = melody_rhythm.render_line(
                _mhits, bar_s, preset["bpm"], _end,
                lambda n, secs: instrument_sampler.voice_note(
                    _ments, n, secs, cache=mcache, used=mused),
                melody_rhythm.feel_for(preset["lanes"], variant * 1301 + 3),
                seed=variant * 1301 + 5)
            if mline is not None and np.max(np.abs(mline)) > 0 \
                    and _one_instrument(mused):
                # his files vary ~30 dB in level (a wine glass peaked at
                # -40 dB): seat the tune 2 dB under the chords' loudest
                # peak, then the lane gain matches the chords'. ponytail:
                # peak match, not loudness; -2 dB is a guess, tune by ear
                _cpk = max((float(np.max(np.abs(kit[ln]))) for ln in kit
                            if _CHORD_LANE.match(ln)), default=0.0)
                if _cpk > 0:
                    mline = mline * (MELODY_UNDER_CHORDS * _cpk
                                     / float(np.max(np.abs(mline))))
                _mbars = ["-" * 16 for _ in range(nb)]
                _mbars[0] = "X" + "-" * 15
                preset["lanes"]["melody0"] = (
                    old_m[0] if old_m else _chord_pan,
                    old_m[1] if old_m else _CHORD_GAIN,
                    (0, 0, 50, variant), _mbars)
                kit["melody0"] = mline
                _mname = (_ments[0].get("multi")
                          or Path(_ments[0]["path"]).stem)
                sources["melody0"] = "%s, answer melody" % _mname
                voice_names["melody0"] = "melody (%s)" % _mname
                voice_files["melody0"] = list(dict.fromkeys(mused))
                if midi_chords:
                    midi_chords[0]["melody_line"] = [
                        (t, min(d, nb * bar_s - t), n,
                         int(min(127, max(1, round(127 * v)))))
                        for t, d, n, v in mnotes]
                melody_info = {"instrument": _mname,
                               "group": _ments[0]["group"],
                               "notes": [list(h) for h in _mhits]}
                vnotes.append("melody: %d notes on %s"
                              % (len(_mhits), _mname))
    # BACKING VOCALS (2026-10-23, tools/backing_vox.py; owner: G-Funk-only
    # layer from the vocal loops already in the bank). Opt-in through
    # signature["backing_vox"], so only G-Funk has it. One loop-length
    # buffer on melody1 (rack row: melody), triggered once on bar 1, seated
    # under the chords. Rebuilt fresh every time, like melody0.
    old_v = preset["lanes"].pop("melody1", None)
    kit.pop("melody1", None)
    _bv = sig.get("backing_vox")
    if (_bv and committed and (num, den) == (4, 4)
            and random.Random(variant * 1747 + 31).random()
            < float(_bv.get("p", 0))):
        import backing_vox
        _ve = backing_vox.pick(backing_vox.scan(), key, preset["bpm"],
                               variant)
        _vbuf = (backing_vox.render(_ve, key, preset["bpm"], nb * bar_s,
                                    chord_synth.SR) if _ve else None)
        if _vbuf is not None:
            _cpk = max((float(np.max(np.abs(kit[ln]))) for ln in kit
                        if _CHORD_LANE.match(ln)), default=0.0)
            if _cpk > 0:
                # ponytail: peak match, under_db is a guess, tune by ear
                _vbuf = _vbuf * (10 ** (float(_bv.get("under_db", -6)) / 20)
                                 * _cpk / float(np.max(np.abs(_vbuf))))
                _vbars = ["-" * 16 for _ in range(nb)]
                _vbars[0] = "X" + "-" * 15
                preset["lanes"]["melody1"] = (
                    old_v[0] if old_v else -_chord_pan or 0.0,
                    old_v[1] if old_v else _CHORD_GAIN,
                    (0, 0, 50, variant), _vbars)
                kit["melody1"] = _vbuf
                sources["melody1"] = "%s, backing vocals" % _ve["name"]
                voice_names["melody1"] = "backing vocals (%s)" % _ve["name"]
                voice_files["melody1"] = [_ve["path"]]
                vnotes.append("backing vocals: %s" % _ve["name"])
    if committed:
        vnotes.append("chords: %s in %s (%s) on %s" % (
            prog_name, key, ", ".join(c["chord"] for c in chords),
            voice_desc))
    else:
        # Nothing in his banks could voice the whole progression (in
        # practice: the sample drive is unplugged, in which case the drum
        # lanes have already failed too). No synthesized floor, by
        # instruction — the beat ships without a chord lane at all rather
        # than with a tone he didn't ask for or a voice that cuts in and
        # out. Bass and MIDI still ride.
        vnotes.append("chords: %s in %s — no instrument could voice it, "
                      "chord lane left out" % (prog_name, key))
    if _tex != "full":
        vnotes.append("texture: %s" % (
            "riff from %s%s" % (_riff["src"], " over a soft 2-note bed"
                                if _riff["bed"] else "")
            if _tex == "riff" else "%s notes of each chord" % (
                "three" if preset.get("texture_flow", 0) >= 3 else "two")
            if _tex == "two" else "a sampled loop carries it"))
    harmony_info = {"key": str(key), "root": key_root, "mode": mode,
                    "progression": prog_name, "rhythm": _rhythm,
                    "texture": ({"kind": _tex, "riff": _riff and _riff["src"],
                                 "bed": bool(_riff and _riff["bed"])}
                                if preset.get("texture_flow") else None),
                    # chord flow (2026-09-26): how the chords were stacked
                    # and how many bars each got; None on older beats
                    "flow": ({"voicing": voicing,
                              "bars": [c["bars"] for c in chords],
                              "turnaround": next((c["chord"] for c in chords
                                                  if c.get("turnaround")),
                                                 None)}
                             if flow else None),
                    "chords": chord_rows,
                    # what actually sounded, not what the identity asked for
                    "chord_source": sorted({r["voice"] for r in chord_rows
                                            if r["voice"]}),
                    # every library file this beat's chord/bass lanes used,
                    # deduped per lane and order-preserved
                    "voice_files": {ln: list(dict.fromkeys(fs))
                                    for ln, fs in voice_files.items()},
                    # which INSTRUMENT each chord lane is, so the rack can
                    # say "HORNS" instead of "CHORDS" (owner 2026-07-25)
                    "voice_names": dict(voice_names),
                    # the 808 that played the bass line, so a rebuild can
                    # voice it again (None: the bass line was his bass
                    # one-shots, or there was no line)
                    "bass808": (str(bass808[0]) if bass808 and bass_beds
                                else None),
                    # the ONE file the bass line played (None: an 808 line
                    # or no line), so the rack can mark it and a rebuild
                    # keeps a pick he made
                    # the bass figure each chord slot played (bass groove,
                    # 2026-10-19); None on older beats / held-root lines
                    "bass_figures": ([p["figure"] + ("+tied" if p["tied"]
                                                     else "")
                                      for p in bass_plan]
                                     if bass_plan and bass_beds else None),
                    # the answer melody (2026-10-19); None = no melody
                    "melody": melody_info,
                    "bass_file": (str(next(iter(bass_files.values()), None))
                                  if bass_beds and not bass808 and any(
                                      bass_files.values()) else None)}
    if bass808 and bass_beds:
        vnotes.append("bass: 808 %s on the chord roots"
                      % Path(bass808[0]).stem)
    return midi_chords, harmony_info


def _pick_loop_bed(dj_name, preset, variant, state=None, guests=()):
    """Loops-only beat, FIVE LANES (owner spec 2026-09-16 — see
    tools/loop_lanes.py and the DECISIONS.md entry). `state` is a saved
    recipe's loop_state (a rebuild); None picks a fresh one leaning on
    this DJ's taste. Returns (state, loop_bufs, nbars, note).
    `guests` are the genres in a loops collab: their library tags join
    the host's, so the loops lean on both."""
    import loop_lanes
    import loop_vocab
    if state is None:
        # a collab preset carries no library/signature — fall back to the host's
        tags = [t for t, _w in (preset.get("library")
                                or CREW[dj_name].get("library") or {}).get("tags", [])]
        for g in guests:
            tags += [t for t, _w in (CREW[g].get("library") or {}).get("tags", [])
                     if t not in tags]
        # owner 2026-10-24: listen line + library tags steer, through the
        # loops vocabulary (loops_config.json), host and guests alike
        words = loop_vocab.identity_words(dj_name, preset)
        for g in guests:
            words += loop_vocab.identity_words(g)
        state = loop_lanes.pick_state(preset.get("signature")
                                      or CREW[dj_name].get("signature") or {}, tags,
                                      preset.get("bpm") or 90,
                                      random.Random(f"{dj_name}|loops|{variant}"),
                                      groups=loop_vocab.groups_of(words))
        # CRATE DIGGER (owner 2026-10-31): new beats may chop the lead loop
        # in the host's style; saved in the state, so a rebuild plays it the
        # same and older beats (no "chop") stay whole. Own rng: picks above
        # are unchanged.
        lead = next((e for e in loop_lanes.scan_all()["lead"]
                     if e["path"] == state["lanes"].get("leadloop")), None)
        spec = loop_lanes.chop_roll(loop_vocab.chop_style(dj_name),
                                    random.Random(f"{dj_name}|chop|{variant}"),
                                    lead)
        if spec:
            state["chop"] = spec
    bufs = loop_lanes.render_bufs(state, SR)
    note = "loops only, %d bars at %d BPM (drum loop's tempo), %s: %s" % (
        loop_lanes.NBARS, state["bpm"],
        "same key %s" % " ".join(k for k in state["key"] if k) if state["key"]
        else "keys ignored",
        "; ".join("%s '%s'" % (loop_lanes.LABELS[ln], Path(p).stem)
                  for ln, p in state["lanes"].items()))
    if state.get("chop"):
        note += "; lead chopped (%s%s)" % (
            state["chop"]["style"],
            ", chopped twice" if state["chop"].get("resample") else "")
    return state, bufs, loop_lanes.NBARS, note


def generate(names, tempo=None, notes="", root=ROOT, shots=None,
             traditional=False, status=lambda msg: None, key=None,
             loops_only=False):
    """Render one random beat (solo or collab) into names[0]'s folder.
    Returns (path, report_line). Raises on an empty selection.
    traditional=True (a quarter of every 4+ batch, owner rule
    2026-07-21, was half):
    a common, popular hip-hop beat — conventional kick+snare backbone,
    no exotic meter, and a tuned root 808 sub when the 808 flavor rolls
    (so the sub is present on some but not every traditional beat).

    loops_only=True (owner 2026-09-16): the drums and melodic content
    both come from a picked loop instead of one-shots/synth — see
    _pick_loop_bed. Owner 2026-10-03: in loops mode a DJ collabs with
    GENRES only, never another DJ (crew or Legend) — so at most one
    non-genre name; the host's folder, tempo and taste lead."""
    seen = set()                                  # dedupe, KEEP caller order
    names = [n for n in names
             if n in CREW and not (n in seen or seen.add(n))]
    if not names:
        raise ValueError("Check at least one DJ first.")
    if loops_only and sum(n not in GENRE_NAMES for n in names) > 1:
        raise ValueError("Loops only: a DJ can team up with styles, "
                         "not with another DJ. Untick all but one DJ.")
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
    # A key off a reference track turns chords ON, because that is the
    # only way the key is audible (owner 2026-09-01: "turn chords on
    # too"). Typing "no chords" still wins — he typed that on purpose.
    want_key = clean_key(key)
    if want_key and not dirs.get("no_chords"):
        dirs["chords"] = True
        dirs["force_key"] = want_key

    # one compose + vary per beat — the reroll-until-different kick
    # guard is gone (owner call 2026-07-21: variety comes from the
    # composition itself, not from rejection loops)
    status(f"Composing for {' x '.join(names)}…")
    # LOOK-ALIKES (owner 2026-10-31, Plan C): re-compose a beat whose
    # drums sit too close to one of this DJ's recent beats (variety.py)
    import variety
    _recent = [] if loops_only else variety.recent_drums(root, names[0])
    for _try in range(1 + (variety.LOOKALIKE_REROLLS if _recent else 0)):
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
        # OWNER RULE 2026-08-01: "We're not using odd signatures." The 3/4
        # and 6/8 roll is gone — measured at 25 of 506 library beats, and it
        # was the source of the genuinely strange lengths (a 3-bar 3/4 loop
        # runs 7.91s). Everything is 4/4 now unless the notes box asks.
        # The EXOTIC GRIDS stay: triplets, quintuplets and 32nd walls are
        # note values inside 4/4, not time signatures, and they are what
        # gives trap rolls and the swung genres their feel. Their share
        # absorbs the 20% the odd meters used to take.
        if tsig is None and not traditional and not pure_legend \
                and not pure_genre:
            if troll.random() < 0.40:
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
        # owner 2026-08-01: no producer-tag stamp on new beats. compose() has
        # already run inside the two branches above, but it skips stamp lanes
        # anyway ("stamps ride their own grids"), so removing them here is
        # enough — and it lands before apply_directions and vary_preset.
        _drop_stamp(preset)
        # An identity whose signature says `chords_default` turns the chord
        # lane ON without the notes box asking. This exists because of a
        # real bug the owner hit (2026-07-24): "I no longer hear the
        # chiptune ... even when I choose the genre or new math". Chords
        # only ever render when parse_directions sees a chord word, so
        # picking Chiptune and pressing go produced NO chord lane and
        # therefore no chip sound at all. For identities whose chord voice
        # IS the identity that is plainly wrong. Deliberately opt-in per
        # identity rather than global: switching chords on for all 39
        # identities would change every beat he has already approved.
        # A typed "no chords" still wins, since dirs is only forced on.
        if not dirs["chords"] and not dirs.get("no_chords") \
                and (preset.get("signature") or {}).get("chords_default"):
            dirs = dict(dirs, chords=True)
        dnotes = apply_directions(preset, dirs)
        vnotes = evo_notes + style_notes + dnotes + vary_preset(
            preset, variant, CREW[names[0]]["num"],
            tempo_locked=bool(bpm), density=dirs["density"])
        if not variety.looks_alike(preset.get("lanes") or {}, _recent):
            break
        if _try < variety.LOOKALIKE_REROLLS:
            status("Too close to a recent beat, composing again…")
    rng = random.Random(variant)
    title = fresh_title(names, rng, root)

    if not loops_only:
        # kick + bass built as one unit (owner 2026-09-23): the kick is
        # chosen SHORT before the kit is picked, on the same deterministic
        # call _low_voice makes after it. Chords on = a bass line plays.
        pair_kick_for(preset, variant, dirs, names[0], shots)

    loop_bufs, loop_nbars, loop_state = None, None, None
    if loops_only:
        status(f"Picking loops for {' x '.join(names)}…")
        loop_state, loop_bufs, loop_nbars, loop_note = _pick_loop_bed(
            names[0], preset, variant, guests=names[1:])
        preset = dict(preset)                # don't mutate CREW's shared dict
        preset["bpm"] = loop_state["bpm"]    # the drum loop sets the tempo
        sources = dict(loop_state["lanes"])
        kit, lane_parent = {}, {ln: names[0] for ln in sources}
        spec_used = {ln: (ln, None, [], 0) for ln in sources}
        preset["lanes"] = {ln: (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),))
                           for ln in sources}
        # the one-shot vnotes above describe a composition that's about
        # to be thrown away — report what actually sounds instead
        vnotes = [loop_note]
    elif len(names) == 1:
        status(f"Building the kit for {' x '.join(names)}…")
        # YOUR EAR (owner 2026-10-31, Plan C): lean toward the sample
        # folders his Favorites keep and away from his Trash (taste.py)
        import taste
        kit, sources = build_kit(shots, names[0], stamps[names[0]][1],
                                 variant=variant, avoid=avoid,
                                 preset=preset, taste=taste.weights(root))
        sources["stamp"] = stamps[names[0]][0]
        # same resolution build_kit just did, kept for the beat's recipe
        spec_used = {ln: (r, m, w, _resolve_secs(s, preset["num"], variant))
                     for ln, (r, m, w, s) in preset["kit"].items()
                     if ln != "stamp"}
        lane_parent = {ln: names[0] for ln in spec_used}
    else:
        status(f"Building the kit for {' x '.join(names)}…")
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
        # hall takes its EXTRA_FX_P share off the top; the old four keep
        # their proportions in the rest
        _h = EXTRA_FX_P["hall"]
        space = random.Random(variant * 941 + 7).choices(
            ["gated", "dry", "room", "plate", "hall"],
            [0.35 * (1 - _h), 0.35 * (1 - _h), 0.2 * (1 - _h),
             0.1 * (1 - _h), _h])[0]

    # "add the root" (owner rule 2026-07-18): traditional beats get a
    # tuned 808 sub on a musical root under the kick — 3 in 4 of them,
    # and traditional is a quarter of a batch, so it lands on roughly one
    # beat in five overall: a regular feature, still "not in everything"
    # the way the rule asks. (The comment here used to say 3 in 5; the
    # roll has been 0.75 since the feature landed.) It's
    # skipped when the kick already rolled a LONG 808 (that sample is
    # carrying the sub itself; two would just fight). The sub mirrors the
    # final kick line, plays straight, and rides the un-ducked bass path.
    root_note = None

    # "chords" / a mood word in the notes box (punch list steps 2+7,
    # 2026-07-22): a real in-key progression, synthesized as a pad + bass
    # and dropped in as extra lanes. Extracted into _build_chords (below)
    # 2026-07-23 so a REBUILD can regenerate this beat's chord audio too
    # (owner: "control the volume for all sounds") — see that function's
    # docstring for why regenerating, not reusing the rendered stem.
    # the beat's ONE low sound, decided before the chords so the strings
    # know whether their basses may play (owner hard rule 2026-09-14)
    if loops_only:
        # a loop IS the melodic/rhythmic content — no synthesized chord
        # lane, no sampled bass/vocal lanes, no root 808 (there's no
        # "kick" one-shot for it to mirror). sources/spec_used/lane_parent
        # were already set to the two loop files above.
        low, midi_chords, harmony_info = None, None, None
    else:
        midi_chords, harmony_info = add_bass_and_chords(
            preset, kit, sources, shots, variant, dirs, vnotes,
            traditional, names[0])

        # bug found 2026-07-23 (owner: "a vocal sound... doesn't show up in the
        # stems but is present in the song"): spec_used/lane_parent were snapshot
        # right after build_kit, BEFORE the root sub, chords, and this phase-2
        # code ever run — so a real sample lane added after that point (bass,
        # vox) played correctly in the render but was invisible to the recipe
        # (kit_spec), and everything downstream that reads it: the app's
        # stems/swap list (_beat_stems), kit_paths, and the anti-repeat history.
        # The audio was real; the bookkeeping just never caught up. Refresh both
        # here, now that every lane that will ever touch preset["kit"] has run.
        spec_used.update({ln: (r, m, w, _resolve_secs(s, preset["num"], variant))
                          for ln, (r, m, w, s) in preset["kit"].items()
                          if ln not in spec_used and ln != "stamp"})
        lane_parent.update({ln: names[0] for ln in spec_used
                            if ln not in lane_parent})

    if not loops_only:
        _roll_extra_fx(preset, kit, sources, spec_used, lane_parent, shots,
                       variant, names[0])

    status(f"Rendering beat {no} at {preset['bpm']} BPM…")
    nbars = loop_nbars if loops_only else bars_of(preset)
    L, R, lufs, parts = render_crew_beat(
        names[0], kit, space=space, preset=preset, want_parts=True,
        loop_bufs=loop_bufs, nbars_override=(loop_nbars if loops_only else None))

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
    # THE CONTRAST-DEEPENING PASS IS GONE (owner 2026-08-03).
    #
    # It measured the finished audio and, if the loop was flatter than
    # 2.5 dB bar to bar, went back and pulled one bar down on every lane,
    # then re-rendered. Two owner rules killed it on the same day:
    #   - 08-01 "gaps rare": as a BLANKING pass it was a second, hidden
    #     hole source that put holes back in 40% of beats after
    #     vary_preset had been dialled to 1-in-6. Rewritten as a dip.
    #   - 08-03 "let's just have everything level": as a DIP it stacked
    #     with quietbar (-2.9 dB) for -11.7 dB off a whole bar before the
    #     per-hit wobble, which is the "drum parts get way too quiet and
    #     don't come back" he reported.
    # There is no version of it left that does not contradict a live rule,
    # so it is removed rather than tuned a third time. `bar_swing` stays —
    # it is still measured and printed on the beat card.

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
    sync_reason_copy(path)
    write_stems(folder / f"{no} {' x '.join(names)} {title} Stems",
                parts["stems"], sources=sources, loops=loops_only)

    # the pattern sheet (owner request 2026-07-22): a readable picture of
    # every lane against the backbeat, so a beat he doesn't like can be
    # diagnosed by eye instead of by ear alone
    from pattern_sheet import write_sheet
    write_sheet(path.with_suffix(".txt"), preset,
                title=path.stem, extra=vnotes)

    # and the recipe, so "same beat, different snare" can rebuild it
    # owner 2026-08-01: no stamp on new beats, so the recipe records none.
    # Writing one anyway would make the app's stem/swap list offer a lane the
    # beat does not actually have (it reads stamp_paths at swap time).
    if STAMP_LANE:
        stamp_paths = {"stamp": stamps[names[0]][0]}
        stamp_secs = {"stamp": CREW[names[0]]["kit"]["stamp"][3]}
        for i, g in enumerate(names[1:]):
            stamp_paths[f"stamp{i + 2}"] = stamps[g][0]
            stamp_secs[f"stamp{i + 2}"] = CREW[g]["kit"]["stamp"][3]
    else:
        stamp_paths, stamp_secs = {}, {}
    save_recipe(root, no, {
        "file": fname, "folder": names[0], "names": names, "title": title,
        "variant": variant, "bpm": preset["bpm"], "space": space,
        "preset": _shareable_preset(preset), "kit_spec": spec_used,
        "lock": parts["lock"],
        "kit_paths": (dict(sources) if loops_only
                     else {ln: sources[ln] for ln in spec_used}),
        "loops_only": loops_only,
        "loop_state": loop_state,
        "stamp_paths": stamp_paths, "stamp_secs": stamp_secs,
        "root_note": root_note, "traditional": traditional,
        "dj_cut_bar": cut_bar, "parent": None, "date": str(date.today()),
        # --- packaging step 1 (2026-07-25): the beat's own harmony, so it
        # stops forgetting itself the moment it lands on disk ---
        "harmony": harmony_info,
        "lanes": sorted(preset["lanes"]),
        "legend": names[0] if names[0] in LEGEND_NAMES else None})

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
    want = nbars * tn * (4.0 / td) * 60.0 / preset["bpm"]
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
    def _db(depth):              # how far the duck pulls a lane down
        return -20 * np.log10(max(1 - depth, 1e-6))
    _sc = ("off" if preset["sidechain"] <= 0 else
           f"-{_db(preset['sidechain']):.1f} dB, "
           f"sub -{_db(sub_sidechain(preset)):.1f} dB")
    lines.append(f"  snare space: {space} | sidechain: {_sc}"
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
    sync_reason_copy(path)
    write_stems(folder / f"{no} {title} Stems", parts["stems"],
               sources=sources)
    spec_used = {ln: (r, m, w, _resolve_secs(s, preset["num"], idx))
                for ln, (r, m, w, s) in preset["kit"].items()}
    save_recipe(root, no, {
        "file": fname, "folder": "Fixed Bank", "names": ["Fixed Bank"],
        "title": title, "variant": idx, "bpm": preset["bpm"],
        "space": "dry", "preset": _shareable_preset(preset),
        "kit_spec": spec_used, "lock": parts["lock"],
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


# --------------------------------------------------- pattern library browser
# Owner request 2026-08-06: a genre dropdown over the whole pattern_library,
# not just the five FIXED_PATTERNS. Same drums-only rendering as the Fixed
# Bank above (no chords, no bass, no DJ stamp), but every lane a pattern
# actually has (toms, open hat, etc.), not just kick/snare/hat, and the two
# breaks files (famous figures + funk breaks) are kept in their own separate
# "Breaks" bucket instead of being mixed into a genre.

LIBRARY_GENRES = {
    "hiphop": ("Hip-Hop", "patterns_hiphop.json"),
    "electronic": ("Electronic", "patterns_electronic.json"),
    "rock": ("Rock", "patterns_rock.json"),
    "funk": ("Funk", "patterns_funk.json"),
}
LIBRARY_BREAKS_FILES = ("patterns_breaks.json", "patterns_funk_breaks.json")

# lane name -> (sample role, want-tags, pan, gain), covering every track
# name seen anywhere in pattern_library/*.json. Role/tag vocabulary is
# sample_library.py's DIR_ROLES — no new sample-scanning code needed.
LANE_SPEC = {
    "kick":       ("kick", ["punch", "knock"], 0.0, 1.0),
    "snare":      ("snare", ["crack", "tight"], 0.0, 0.85),
    "closed_hat": ("hat", ["closed"], -0.12, 0.35),
    "open_hat":   ("hat", ["open"], -0.12, 0.4),
    "hat":        ("hat", ["closed"], -0.12, 0.35),
    "ride":       ("hat", ["ride"], 0.2, 0.4),
    "crash":      ("crash", ["crash"], -0.2, 0.5),
    "tom_hi":     ("perc", ["tom", "hi"], 0.35, 0.6),
    "tom_mid":    ("perc", ["tom", "mid"], 0.0, 0.6),
    "tom_low":    ("perc", ["tom", "low"], -0.35, 0.6),
    "cowbell":    ("perc", ["cowbell"], 0.25, 0.45),
    "shaker":     ("perc", ["shaker"], -0.25, 0.3),
    "clap":       ("clap", ["clap"], 0.0, 0.6),
    "rim":        ("rim", ["rim"], 0.15, 0.5),
}


def _library_json(fname):
    try:
        return json.loads((LIB_DIR / fname).read_text())
    except (OSError, json.JSONDecodeError):
        return []


def library_genres():
    """{genre_key: (label, [pattern dicts])} for the four genre dropdowns —
    raw pattern dicts (full multi-lane tracks), not load_library()'s
    reduced kick/snare/hat engine form, so toms and open hats survive."""
    return {key: (label, _library_json(fname))
           for key, (label, fname) in LIBRARY_GENRES.items()}


def library_breaks():
    """The separate Breaks bucket: famous figures + funk breaks, combined."""
    out = []
    for fname in LIBRARY_BREAKS_FILES:
        out += _library_json(fname)
    return out


def _library_pattern_lanes(pat):
    """Every lane this pattern actually hits, converted to engine bar
    strings with _lib_lane — the same written-dynamics reading the breaks
    pack uses, just applied per-lane instead of only kick/snare/hat."""
    lanes = {}
    for lane, vels in pat.get("tracks", {}).items():
        if lane not in LANE_SPEC or not any(vels):
            continue
        flat = {"kick": "positional", "snare": "X"}.get(lane, "x")
        s = _lib_lane(vels, flat)
        if s.count("-") < len(s):
            lanes[lane] = s
    return lanes


def _library_preset(pat, variant=0):
    lane_strs = _library_pattern_lanes(pat)
    seed_num = zlib.crc32(pat["name"].encode()) % 90000 + 10000
    lanes, kit = {}, {}
    for i, (lane, bar) in enumerate(lane_strs.items()):
        role, wants, pan, gain = LANE_SPEC[lane]
        lanes[lane] = (pan, gain, (0, 0, 50, seed_num * 10 + i),
                       [bar] * BARS)
        kit[lane] = (role, None, wants, (0.2, 0.5) if lane == "kick" else 1.0)
    return dict(num=seed_num, bpm=pat.get("bpm", 96), lanes=lanes, kit=kit,
               kick_dist=0.0, dust=0.0, vinyl=0, wow=0.0, mix_sat=0.0,
               drive=1.0, sidechain=0.0, space=("dry", []), alt=None,
               title=pat["name"], variant=variant)


def generate_library(genre_key, name, root=ROOT, shots=None,
                     status=lambda msg: None):
    """Render one pattern_library pattern standalone: drums only (whatever
    lanes it actually has), no chords/bass/DJ stamp. genre_key is one of
    LIBRARY_GENRES or "breaks"."""
    if genre_key == "breaks":
        label, pool = "Breaks", library_breaks()
    else:
        if genre_key not in LIBRARY_GENRES:
            raise RuntimeError(f"unknown library genre {genre_key!r}")
        label, pool = library_genres()[genre_key]
    pat = next((p for p in pool if p["name"] == name), None)
    if pat is None:
        raise RuntimeError(f"{name!r} not found in the {label} library")
    variant = zlib.crc32(pat["name"].encode()) % 1000
    preset = _library_preset(pat, variant=variant)
    if shots is None:
        status("Scanning your sample library…")
        shots = build_shots()
    kit, sources = build_kit(shots, label, None, variant=variant,
                             avoid=history_avoid([label]), preset=preset)
    del kit["stamp"]
    L, R, lufs, parts = render_crew_beat(label, kit, preset=preset,
                                         want_parts=True)
    no = next_number(root)
    folder = root / label
    folder.mkdir(parents=True, exist_ok=True)
    title = preset["title"]
    fname = f"{no} {title} Drums {preset['bpm']}bpm.wav"
    path = folder / fname
    if path.exists():
        raise RuntimeError(f"{fname} already exists — not overwriting.")
    write_wav24(path, L, R)
    write_midi(path.with_suffix(".mid"), parts["events"], preset["bpm"])
    sync_reason_copy(path)
    write_stems(folder / f"{no} {title} Stems", parts["stems"],
               sources=sources)
    spec_used = {ln: (r, m, w, _resolve_secs(s, preset["num"], variant))
                for ln, (r, m, w, s) in preset["kit"].items()}
    save_recipe(root, no, {
        "file": fname, "folder": label, "names": [label],
        "title": title, "variant": variant, "bpm": preset["bpm"],
        "space": "dry", "preset": _shareable_preset(preset),
        "kit_spec": spec_used, "lock": parts["lock"],
        "kit_paths": {ln: sources[ln] for ln in spec_used},
        "stamp_paths": {}, "stamp_secs": {}, "root_note": None,
        "traditional": False, "dj_cut_bar": None, "parent": None,
        "date": str(date.today())})
    record_history({ln: label for ln in spec_used}, sources)
    report = (f"{fname}\n-> {label} folder (+ MIDI and "
             f"{len(parts['stems'])} stems) | LUFS {lufs:.1f}"
             f"\n   pattern library: {title} — roll again for a new kit")
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
                or (p.is_dir() and (p.name.endswith("Stems")
                                    or p.name.endswith("Chunks")))):
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


_ORIGINS = ".triage_origins.json"       # beside the beats: where each beat came from


def _origins(root):
    try:
        return json.loads((Path(root) / _ORIGINS).read_text())
    except (OSError, ValueError):
        return {}


def _save_origins(root, data):
    f = Path(root) / _ORIGINS
    tmp = f.with_name(f.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=1))
    tmp.replace(f)


def triage(no, dest, root=None):
    """Move beat `no` to Favorites / Trash / back to where it came from.
    MOVE, never delete. Returns the new location string. Idempotent.

    The folder a beat sits in before it first goes to Favorites or Trash is
    remembered (.triage_origins.json), so "back to its DJ folder" returns
    it to EXACTLY that folder, even for a beat with no saved recipe, and a
    failed beat can always be recovered (design handoff 2026-10-04)."""
    root = Path(root or ROOT)
    no = int(no)
    items = beat_items(no, root)
    if not items:
        raise FileNotFoundError(f"No beat {no} to move.")
    kept = _origins(root)
    mine = kept.get(str(no), {})
    if dest in ("fav", "favorite", "favorites"):
        target, loc = Path(root) / FAV_DIR, "favorites"
    elif dest in ("trash", "bin", "reject"):
        target, loc = Path(root) / TRASH_DIR, "trash"
    else:                                     # 'dj' - back where it came from
        target, loc = None, "dj"
    # remember each item's home before it first leaves it
    if target is not None:
        for p in items:
            if p.relative_to(root).parts[0] not in (FAV_DIR, TRASH_DIR):
                mine[p.name] = str(p.parent.relative_to(root))
        if mine:
            kept[str(no)] = mine
            _save_origins(root, kept)
    dj = None
    for p in items:
        if target is not None:
            to = target
        else:
            home = mine.get(p.name)
            if home:
                to = Path(root) / home
            else:
                dj = dj or beat_dj(no, root)
                if not dj:
                    raise ValueError(
                        f"Don't know which DJ beat {no} belongs to.")
                to = Path(root) / dj
        to.mkdir(parents=True, exist_ok=True)
        d = to / p.name
        if p.resolve() == d.resolve() or d.exists():
            continue                          # already there / never clobber
        shutil.move(str(p), str(d))
    if target is None and mine:               # home again: forget the old address
        kept.pop(str(no), None)
        _save_origins(root, kept)
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


def ban_lane(number, lane, choice=None, root=ROOT, shots=None):
    """Ban the sound sitting on one lane of one beat (owner 2026-08-31:
    "When I ban a sound, it is banned everywhere. forever.").

    The lane is named, never the file: the client sends a beat number and a
    lane, and the path is looked up in the saved recipe here. Same rule the
    swap dropdown follows — no client string reaches disk unchecked.

    Two-step by his choice ("ask me each time"). Called with no `choice`
    it REPORTS: how many samples in his library share this file name. One
    means there is nothing to ask about and it bans outright. More than one
    means a name-ban would take innocent samples, so it returns and waits.
    Measured on his library, that is 17.5% of samples.

    Existing beats are left alone — a ban stops the sound being picked
    again, and nothing else (his call)."""
    number = int(number)
    lane = str(lane).strip().lower()
    rec = load_recipe(Path(root), number)
    path = (rec.get("kit_paths") or {}).get(lane)
    if not path:
        raise ValueError(
            f"The {lane_label(lane)} on beat {number} isn't a sample — "
            "there's no file to ban.")
    twins = name_twins(path, shots)
    name = Path(path).stem
    # Ask unless we can PROVE this name is unique. `shots` is the already
    # filtered pool, so a path missing from it (or a missing pool) means
    # the count is an undercount, not a one — and banning silently on an
    # undercount is the thing he asked to be protected from. Only a count
    # that actually found this file, and found it alone, skips the prompt.
    sure = len(twins) == 1 and str(path) in twins
    if choice is None and not sure:
        return {"asked": True, "name": name, "twins": len(twins),
                "sure": bool(twins),
                "others": [Path(p).stem for p in twins[:8]]}
    res = ban_sound(path, whole_name=(choice == "name"), shots=shots)
    # the cached pool is already filtered, so it would keep serving the
    # banned sound until the next restart. The rendered previews are keyed
    # by query string and would keep playing the banned sound back at him
    # after he banned it, so they go too.
    _CACHE.pop("shots", None)
    _PREVIEW_CACHE.clear()
    res["asked"] = False
    res["twins"] = len(twins)
    return res


def swap(number, lane, root=ROOT, shots=None, status=lambda msg: None,
         pick=None):
    """One drum swapped — the single-lane door into `swap_many`, kept for
    the CLI (`--swap N --lane snare`) and the tests."""
    return swap_many(number, {lane: pick}, root=root, shots=shots,
                     status=status)


def _change_words(lanes, trims, drops, chord_voice=None, fx=False):
    """How a staged set of rack changes reads: `what` is the short title
    that becomes part of a filename, `changed` is the sentence for the
    log. Split out of swap_many so the chunk folder names its files with
    the same words the rebuild uses — one place to change the wording.

    A family removal is 4 lanes but ONE musical change — say "Chords",
    not "Chord0 & Chord1 & Chord2 & Chord3"."""
    if fx:                            # the FX on button, alone or on top
        if not (lanes or trims or drops or chord_voice):
            return "FX On", "effects on"
        what, changed = _change_words(lanes, trims, drops, chord_voice)
        return what + " FX", changed + ", effects on"
    said = [ln for ln in drops if not _chord_family(ln)]
    if any(_CHORD_LANE.match(ln) for ln in drops):
        said.append("chords")
    if any(_CHORD_BASS_LANE.match(ln) for ln in drops):
        said.append("chord bass")
    if any(_MELODY_LANE.match(ln) for ln in drops):
        said.append("melody")
    if drops and not lanes and not trims:      # removal is the headline
        return ("No " + " & ".join(d.title() for d in said),
                "removed " + " and ".join(said))
    if drops:
        return ("Rebuilt",
                "removed " + " and ".join(said)
                + (", new " + ", ".join(lanes) if lanes else ""))
    if chord_voice and not lanes:     # the instrument IS the change
        nice = CHORD_VOICE_NAMES.get(chord_voice, chord_voice).split(" (")[0]
        return (f"{nice} Chords",
                f"chords on {nice.lower()}"
                + (", " + _trim_words(trims) if trims else ""))
    if not lanes:                     # volumes only — same drums, new mix
        return "New Mix", _trim_words(trims) if trims else "mix"
    if len(lanes) == 1:
        return f"New {lanes[0].capitalize()}", lanes[0]
    if len(lanes) == 2:
        return (f"New {lanes[0].capitalize()} & {lanes[1].capitalize()}",
                " and ".join(lanes))
    return "Rebuilt", ", ".join(lanes)


def swap_many(number, picks, root=ROOT, shots=None, status=lambda msg: None,
              trims=None, drops=None, render_only=False, fx=False,
              _learn=False, pans=None, stage=False, solo=None):
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
    swap or trim staged on the same lane.

    `render_only=True` stops after the render and returns (L, R) instead
    of printing anything: the live preview behind /mix (owner
    2026-08-03, "it does not change the sound in the beat when I go back
    and preview it — before committing to the rerender"). A swap can't
    be previewed by summing stems the way a level move can, so the
    preview IS this render — which also means what he hears is exactly
    what Rebuild will print, not an approximation of it.

    `fx=True` (owner 2026-09-24, the "FX on" button): the same beat with
    its style's own effects baked in -- dust, vinyl, wow, saturation, 808
    drive, hot master -- which the clean-render rule keeps off by default.
    The stems carry them too (his call). Lands as a new number like any
    rebuild; the clean original stays.

    The beat's VOLUME SETTING is locked (owner 2026-09-27, "lock it per
    beat"): the rebuild replays rec["lock"] instead of re-levelling the
    whole mix, so only the sound he touched changes. A beat made before
    the lock existed learns it on its first edit ("learn it on first
    edit"): one unchanged re-render (`_learn=True`, returns the lock and
    stops), saved into its recipe so it only ever happens once."""
    number = int(number)
    rec = load_recipe(root, number)
    if rec.get("engine_fx"):     # effects from the Effects page live in its stems
        return _engine_swap(number, rec, picks, trims, pans, drops,
                            render_only, fx, Path(root), stage=stage)
    lock = rec.get("lock")
    if (lock is None or "lane_gains" not in lock) and not _learn:
        status(f"First edit of beat {number} — learning its volume…")
        if shots is None and not rec.get("loops_only"):
            status("Scanning your sample library…")
            shots = build_shots()
        lock = swap_many(number, {}, root=root, shots=shots, _learn=True)
        rec["lock"] = lock
        save_recipe(root, number, dict(load_recipe(root, number), lock=lock))
    picks = {str(ln).strip().lower(): v for ln, v in (picks or {}).items()}
    drops = sorted({str(ln).strip().lower() for ln in (drops or [])})
    # "chords"/"bass" are FAMILY names from the rack: one row standing for
    # chord0..chordN. Expand them to the real lanes so a removal takes the
    # whole instrument out at once (owner 2026-07-25) — a per-bar removal
    # would make it drop out mid-beat.
    all_lanes = list(normalize_preset(rec["preset"]).get("lanes", {}))
    # Each chord instrument is its own rack row (chords, chords2, chords3, …)
    # since 2026-09-20 — a beat can layer more than one. Any family handle in
    # `drops` that resolves to real lanes is expanded to them, so removing any
    # instrument row takes that whole instrument out. Non-family names (a drum
    # lane, a single chord lane) resolve to no members and stay as literals.
    fam_drops = []
    for fam in [f for f in list(drops) if _family_members(f, all_lanes)]:
        drops.remove(fam)
        fam_drops += _family_members(fam, all_lanes)
    # A pick on a harmony row names an INSTRUMENT, not a file (owner
    # 2026-08-04). It leaves `picks` here — there is no kit_paths entry
    # to swap — and is handed to _build_chords below as the voice to try
    # first. Only the chord family takes one: the bass line is his to
    # play (2026-07-29), so its lanes are never rendered.
    chord_voice = chord_exact = None
    bass_pick = None
    for fam in [f for f in list(picks) if _family_members(f, all_lanes)]:
        want = picks.pop(fam)
        if fam == MELODY_FAM:
            raise ValueError("The melody's instrument can't be swapped yet "
                             "— turn it down or remove it.")
        if fam == CHORD_BASS_FAM:
            # the bass row lists his real bass FILES (owner 2026-09-26),
            # and the pick is one of them -- never a chord voice
            if want and want not in {c["path"] for c in
                                     _lane_candidates(number, fam, root=root)}:
                raise ValueError(f"'{want}' isn't a bass in your library.")
            if want and want != (rec.get("harmony") or {}).get("bass_file"):
                bass_pick = want
            continue
        # "voice" = a type, the machine picks inside it; "voice::exact" =
        # the one instrument he picked in the second dropdown (2026-09-28)
        voice, _, exact = (want or "").partition("::")
        if voice and voice not in {c["path"] for c in _chord_voices()}:
            raise ValueError(f"'{want}' isn't an instrument in your library.")
        if exact and want not in {c["path"] for c in _chord_choices(rec)}:
            raise ValueError(f"'{exact}' can't play this beat's chords.")
        if voice:
            chord_voice, chord_exact = voice, exact or None
    # a pick made on an earlier rebuild keeps playing (2026-09-28): before
    # this, the child's next rebuild quietly went back to the old voice
    _vp = (rec.get("harmony") or {}).get("voice_pick") or {}
    play_voice = chord_voice or _vp.get("voice")
    play_exact = chord_exact if chord_voice else _vp.get("exact")
    for lane in list(picks) + drops:
        if lane not in rec["kit_spec"]:
            raise ValueError(f"Beat {number} has no '{lane}' to change — "
                             f"it has: {', '.join(sorted(rec['kit_spec']))}.")
    drops = sorted(set(drops) | set(fam_drops))
    # picking the sample that's already in the lane isn't a swap
    picks = {ln: v for ln, v in picks.items()
             if not (v and v == rec["kit_paths"].get(ln))}
    preset = normalize_preset(rec["preset"])
    trims = _clean_trims(trims, preset, number)
    pans = _clean_pans(pans, preset, number)
    for lane in drops:                        # a drop wins over the rest
        picks.pop(lane, None)
        trims.pop(lane, None)
        pans.pop(lane, None)
    if set(rec["kit_spec"]) <= set(drops):
        raise ValueError("That would remove every drum — keep at least "
                         "one.")
    if fx:
        if rec.get("loops_only"):           # owner 2026-10-24
            raise ValueError("Loop beats stay clean — no effects to turn on.")
        if preset.get("allow_dirt") is True:
            raise ValueError("This beat already has its effects on.")
        if not (any(preset.get(k, 0) > 0
                    for k in ("dust", "wow", "mix_sat", "kick_dist"))
                or preset.get("vinyl") or preset.get("drive", 0) > 0.7):
            raise ValueError("This beat's style has no effects to turn on.")
        preset["allow_dirt"] = True    # crew.render_crew_beat's own switch
        preset["fx_stems"] = True      # ...and onto every stem, not just the mix
    if (not picks and not trims and not pans and not drops
            and not chord_voice and not bass_pick and not fx and not _learn):
        raise ValueError("Nothing to change — pick a different sound, "
                         "move a volume slider, or remove a stem first.")
    for lane in drops:
        preset["lanes"].pop(lane, None)
    # a changed sound gets levelled fresh by the rules; every other sound
    # keeps the level it was made with (owner 2026-09-28)
    if lock and not _learn:
        _changed = set(picks)
        lock = dict(lock, lane_gains={
            ln: g for ln, g in (lock.get("lane_gains") or {}).items()
            if ln not in _changed
            and not (chord_voice and ln.startswith("chord"))
            and not (bass_pick and _CHORD_BASS_LANE.match(ln))})
    if fx:                   # the effects button re-voices everything:
        lock = None          # it gets levelled fresh, then locked anew
    # bake the trims into this beat's own gains. The child recipe stores
    # the RESULT, so its sliders start at 0 again ("nudge from how it
    # sounds now") and re-rendering it without trims reproduces it.
    for lane, db in trims.items():
        pan, gain, feel, bars = preset["lanes"][lane]
        preset["lanes"][lane] = (pan, gain * 10 ** (db / 20.0), feel, bars)
    # pan knobs (owner 2026-10-15): an absolute position, -1 left .. +1
    # right, replacing the lane's own pan. His hand overrides the hat rule.
    for lane, pos in pans.items():
        _, gain, feel, bars = preset["lanes"][lane]
        preset["lanes"][lane] = (pos, gain, feel, bars)
    names = rec["names"]
    if rec.get("loops_only"):
        # five-lane loops beat (owner 2026-09-16): swap = a different loop
        # file on that lane; a new drum loop brings its own tempo
        import loop_lanes
        state = copy.deepcopy(rec["loop_state"])
        olds = {ln: rec["kit_paths"].get(ln) for ln in picks}
        for lane, chosen in picks.items():
            if not chosen:
                raise ValueError("Pick a loop from the list first.")
            state["lanes"][lane] = chosen
        for lane in drops:
            state["lanes"].pop(lane, None)
        if "kick" in picks and "kick" in state["lanes"]:
            state["bpm"] = loop_lanes.drum_bpm(state["lanes"]["kick"],
                                               CREW[names[0]]["bpm"])
        preset["bpm"] = state["bpm"]
        kit_paths, chord_sources, kit = dict(state["lanes"]), {}, {}
        lanes = sorted(picks)
        what, changed = _change_words(lanes, trims, drops, chord_voice, fx)
        status(f"Re-rendering beat {number} with the new {changed}…")
        _, loop_bufs, nb, _note = _pick_loop_bed(names[0], preset,
                                                 rec["variant"], state=state)
        L, R, lufs, parts = render_crew_beat(
            names[0], kit, space=rec["space"], preset=preset,
            want_parts=True, loop_bufs=loop_bufs, nbars_override=nb,
            lock=lock)
    else:
        if shots is None:
            status("Scanning your sample library…")
            shots = build_shots()

        avoid = set(p for p in rec["kit_paths"].values() if p)
        avoid |= set(rec["stamp_paths"].values())
        avoid |= history_avoid(names)

        bass_rebuilt = None
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
        chord_sources = {}          # lane -> what to CALL it in the stems folder
        # the tuned root sub was synthesized, not a sample. Since 2026-09-23
        # (owner: "I don't want any tones created by machine") a rebuild
        # leaves it OUT rather than resynthesizing it.
        if "sub" in preset.get("lanes", {}) and "sub" not in kit_paths:
            preset["lanes"].pop("sub", None)
        # chord/chord-bass lanes are ALSO synthesized (owner 2026-07-23,
        # "control the volume for all sounds" — the ask that surfaced this gap:
        # those lanes now show a volume slider, so a rebuild has to actually be
        # able to regenerate their audio). Detected by lane name since a chords
        # beat's kit_spec never lists them (see _build_chords' docstring for why
        # this regenerates rather than reuses the rendered stem, and the two
        # narrow, disclosed limits on an exact match).
        # EITHER family is enough to need the regen: removing just the chords
        # leaves the bass roots behind, and they still need their audio built
        # (they are synthesized-at-render like the chords, not kit_paths files)
        if any(_chord_family(ln) for ln in preset.get("lanes", {})):
            # chord/bass lanes are never in kit_paths (nothing to swap them
            # for), so none of this is persisted into the recipe — but it IS
            # what names their stem files. Passing a throwaway {} here printed
            # every rebuilt chord stem as a bare "chord0.wav", losing the
            # instrument and the chord it plays (owner rule 2026-07-18: a stem
            # says WHICH sound it is). Measured 2026-09-01: swap one hat and
            # "chord0 - sample_ Cymatics ... , Dm7 (ii7)" came back as
            # "chord0". Keep the dict; write_stems reads it below.
            #
            # Hand back the KEY and the PROGRESSION this beat was actually
            # printed in (2026-09-01). The rebuild used to re-roll both from
            # the variant + the DJ's signature and land on the same answer by
            # luck — a luck that ran out the moment a REFERENCE TRACK could
            # override the signature. Pinning only the key was worse than
            # pinning neither: it sent the rebuild down the forced branch,
            # which re-picks the progression from the signature, so an
            # open-roll beat came back with different chords under the same
            # instrument (measured: F7#9 out, Gm7 back). The recipe knows
            # all three, so hand back all three.
            # Whether that hand-back actually happens is REBUILD_LOCKS_KEY.
            _dirs = {"chords": True, "chord_feel": None,
                     "busy_lanes": normalize_preset(rec["preset"])["lanes"],
                     "busy": rec["preset"].get("chord_busy")}
            if REBUILD_LOCKS_KEY:
                _h = rec.get("harmony") or {}
                _dirs["chord_feel"] = _h.get("progression")
                if _h.get("root") and _h.get("mode"):
                    _dirs["force_key"] = (_h["root"], _h["mode"])
            # an 808 that played the bass line plays it again (2026-09-23)
            _b808 = (rec.get("harmony") or {}).get("bass808")
            _b808_audio = _load_choked(_b808, 0.8) if _b808 else None
            if _b808 and _b808_audio is None:
                raise RuntimeError(f"{Path(_b808).name} (the beat's 808) has "
                                   "moved or vanished — can't rebuild.")
            # a bass he picked, else the one this beat was last built on
            _hb = rec.get("harmony") or {}
            _bp = bass_pick or _hb.get("bass_file")
            _, bass_rebuilt = _build_chords(
                          preset, kit, chord_sources, rec["variant"],
                          _dirs, [], voice=play_voice, bass_pick=_bp,
                          exact=play_exact,
                          # beats made since 2026-09-23 (the key exists
                          # even when None) never let the strings' basses
                          # play; older beats rebuild the way they were made
                          allow_basses=(False if "bass808" in
                                        (rec.get("harmony") or {}) else None),
                          bass808=((_b808, _b808_audio) if _b808 else None))
            # ...but a chord/bass lane the owner just REMOVED must not come
            # back: _build_chords rebuilds the whole family from the recipe's
            # variant, which would silently undo the removal.
            for lane in drops:
                preset["lanes"].pop(lane, None)
                kit.pop(lane, None)

        lanes = sorted(picks)
        what, changed = _change_words(
            lanes + (["bass"] if bass_pick else []), trims, drops,
            chord_voice, fx)
        status(f"Re-rendering beat {number} with the new {changed}…")
        L, R, lufs, parts = render_crew_beat(names[0], kit, space=rec["space"],
                                             preset=preset, want_parts=True,
                                             lock=lock)
        if rec.get("dj_cut_bar") is not None:
            L, R = dj_cut(L, R, parts, rec["dj_cut_bar"])

    if _learn:                 # the unchanged beat's volume setting
        return parts["lock"]
    if render_only and solo:   # one row's new sound on its own (audition)
        got = [parts["stems"][ln] for ln in
               (_family_members(solo, list(parts["stems"])) or [solo])
               if ln in parts["stems"]]
        if not got:
            raise ValueError(f"Beat {number} has no '{solo}' to play.")
        L = sum(g[0] for g in got)
        R = sum(g[1] for g in got)
        # at full level like a drum audition: in the track a chord sits
        # ~16 dB under the drums, too quiet to judge on its own
        pk = float(max(np.abs(L).max(), np.abs(R).max()))
        if pk > 0:
            L, R = L * (0.9 / pk), R * (0.9 / pk)
        return L, R
    if render_only:            # live preview — nothing is printed or filed
        return L, R
    if stage:                  # the Effects button: no new number
        def put(sdir):
            write_stems(sdir, parts["stems"],
                        sources={**chord_sources, **kit_paths, **rec["stamp_paths"]},
                        loops=bool(rec.get("loops_only")))
        return _write_stage(number, root, (L, R), put, preset["bpm"])

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
    sync_reason_copy(path)
    write_stems(folder / f"{no} {stem_of} Stems", parts["stems"],
                sources={**chord_sources, **kit_paths, **rec["stamp_paths"]},
                loops=bool(rec.get("loops_only")))

    if rec.get("loops_only"):
        rec = dict(rec, loop_state=state, bpm=state["bpm"])
    rec2 = dict(rec, file=fname, kit_paths=kit_paths, parent=number,
                folder=rec["folder"], date=str(date.today()),
                lock=parts["lock"])
    if drops:                    # the lane is gone from the child recipe
        rec2["kit_spec"] = {ln: s for ln, s in rec["kit_spec"].items()
                            if ln not in drops}
    if bass_pick and bass_rebuilt:   # the child beat remembers its bass
        _h = dict(rec.get("harmony") or {})
        _h["bass_file"] = bass_rebuilt.get("bass_file")
        _h["voice_files"] = {
            **(_h.get("voice_files") or {}),
            **{ln: fs for ln, fs in bass_rebuilt["voice_files"].items()
               if _CHORD_BASS_LANE.match(ln)}}
        rec2["harmony"] = _h
    if chord_voice and bass_rebuilt:   # ...and its chord instrument
        _h = dict(rec2.get("harmony") or {})
        _h["voice_pick"] = {"voice": chord_voice, "exact": chord_exact}
        for k in ("chords", "chord_source"):
            if k in bass_rebuilt:
                _h[k] = bass_rebuilt[k]
        for k in ("voice_files", "voice_names"):   # chord rows: new names
            _h[k] = {**{ln: v for ln, v in (_h.get(k) or {}).items()
                        if not _CHORD_LANE.match(ln)},
                     **{ln: v for ln, v in (bass_rebuilt.get(k) or {}).items()
                        if _CHORD_LANE.match(ln)}}
        rec2["harmony"] = _h
    if trims or pans or drops or fx:     # new gains/pans/lanes/effects ARE this beat
        rec2["preset"] = preset
    # a swap inherits its parent's recipe, so an OLD parent written before
    # 2026-07-25 would carry `built` forward into the new file
    rec2["preset"] = _shareable_preset(rec2.get("preset") or {})
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
        if pans:
            f.write(f"  pans: {_pan_words(pans)}\n")
        f.write(f"  LUFS {lufs:.1f}\n")
    bits = [f"{ln} → {Path(kit_paths[ln]).name}" for ln in lanes]
    if trims:
        bits.append(_trim_words(trims))
    if pans:
        bits.append(_pan_words(pans))
    report = (f"{fname}\n-> {rec['folder']} folder | same beat as "
              f"{number} | {' | '.join(bits)} | LUFS {lufs:.1f}")
    return path, report



# ------------------------------------------- effected beats (owner 2026-10-15)
# A beat sent back from the Effects page has its effects baked into its
# stems, which its recipe can't reproduce. So it is never re-rendered: a
# chunk, preview or rebuild of it is a mix of those stems with the rack's
# volume, pan and removals. Sound swaps are off on it (owner's choice).

def _engine_mix(number, rec, trims, pans, drops, root):
    """(L, R, stems, trims, pans, drops) — the effected stems mixed as the
    rack is set. `stems` maps stem filename -> (L, R) after the moves."""
    import math
    preset = rec["preset"]
    lanes = preset.get("lanes", {})
    trims = _clean_trims(trims, preset, number)
    pans = _clean_pans(pans, preset, number)
    gone = set()
    for d in drops or []:
        d = str(d).strip().lower()
        gone |= set(_family_members(d, lanes) or [d])
    folder = _stems_dir(number, root)
    if not folder:
        raise ValueError(f"Beat {number} has no Stems folder to mix.")
    lane_of = {}
    for ln in set(lanes) | set(rec.get("kit_spec", {})) | set(rec.get("stamp_paths", {})):
        f = _stem_wav(number, ln, root, folder=folder)
        if f:
            lane_of[f] = ln
    stems = {}
    for f in sorted(folder.glob("*.wav")):
        ln = lane_of.get(f)
        if ln in gone:
            continue
        L, R = read_wav24(f)
        g = 10 ** (trims.get(ln, 0.0) / 20.0)
        gl = gr = g
        if ln in pans:
            # ponytail: relative balance on an already-panned stereo stem
            d = max(-1.0, min(1.0, pans[ln] - float(lanes[ln][0])))
            th = (d + 1) * math.pi / 4
            gl, gr = g * math.cos(th) * math.sqrt(2), g * math.sin(th) * math.sqrt(2)
        stems[f.name] = (L * gl, R * gr)
    if not stems:
        raise ValueError("That would remove every stem — keep at least one.")
    n = max(len(L) for L, _ in stems.values())
    L, R = np.zeros(n), np.zeros(n)
    for sL, sR in stems.values():
        L[:len(sL)] += sL
        R[:len(sR)] += sR
    peak = float(max(np.abs(L).max(), np.abs(R).max()))
    if peak > 0.966:             # -0.3 dB: turn the whole mix down, never clip
        L, R = L * (0.966 / peak), R * (0.966 / peak)
    return L, R, stems, trims, pans, gone


def _engine_swap(number, rec, picks, trims, pans, drops, render_only, fx, root,
                 stage=False):
    if any(v for v in (picks or {}).values()):
        raise ValueError("Sound swaps are off on an effected beat — its "
                         "effects are baked into its stems.")
    if fx:
        raise ValueError("This beat already has its effects on.")
    L, R, stems, trims, pans, gone = _engine_mix(number, rec, trims, pans,
                                                 drops, root)
    if render_only:
        return L, R
    if stage:
        def put(sdir):
            sdir.mkdir(parents=True)
            for name, (sL, sR) in stems.items():
                write_wav24(sdir / name, sL, sR)
            (sdir / ".base_clean").write_text("1")
        return _write_stage(number, root, (L, R), put,
                            rec["preset"].get("bpm") or rec.get("bpm"))
    if not (trims or pans or gone):
        raise ValueError("Nothing to change — move a volume or pan, or "
                         "remove a stem first.")
    what, _ = _change_words([], trims, sorted(gone))
    preset = copy.deepcopy(rec["preset"])
    for ln in gone:
        preset["lanes"].pop(ln, None)
    for ln, pos in pans.items():   # the knob starts where it was left
        t = list(preset["lanes"][ln]); t[0] = pos; preset["lanes"][ln] = t
    rec = dict(rec, preset=preset,
               kit_spec={k: v for k, v in rec["kit_spec"].items()
                         if k not in gone})
    return _file_engine_beat(number, stems, (L, R), what, root, rec=rec)


STAGE_DIR = ".effects-stage"


def stage_name(number):
    """The staged copy's name. Never starts with a digit, so next_number and
    every by-number lookup skip it; the Sound Engine's send-back reads the
    number back out of it."""
    return f"Beat {int(number)} (your mix)"


def sketch_stage_dir(number, root=None):
    """Where the Effects page's Sketch button leaves the beat as heard there
    (effects, levels, mutes), for Song Sketch to arrange. No new number."""
    root = Path(root or ROOT)
    w = beat_wav(number, root)
    if w is None:
        raise ValueError(f"Beat {number} isn't in the library.")
    return (root / w.relative_to(root).parts[0] / STAGE_DIR
            / f"Beat {int(number)} (sketch mix) Stems")


def _beat_rms(no):
    """The finished beat's average level, for Song Sketch to match."""
    import soundfile as sf
    w = beat_wav(no)
    if w is None:
        return None
    x, _ = sf.read(str(w), dtype="float32", always_2d=True)
    return float(np.sqrt(np.mean(x ** 2))) or None


def _sketch_folder(no, src):
    """The stems Song Sketch reads: the beat's own, or (src="effects") the
    copy the Effects page just left."""
    if src != "effects":
        return None
    f = sketch_stage_dir(no)
    if not f.is_dir():
        raise ValueError("Open this beat on the Effects page and press "
                         "Sketch there first.")
    return f


def _write_stage(number, root, mix, put_stems, bpm):
    """The rack as it is set (swaps, volumes, pans, removals) for the
    Effects page, WITHOUT a new number (owner 2026-10-21). Lands in
    <DJ folder>/.effects-stage/, which the Sound Engine opens as
    "<dj>/.effects-stage/Beat N (your mix)" and its picker never lists.
    Replaced on every click: it is a working copy the machine made, not
    one of his beats. Returns the Sound Engine id."""
    root = Path(root)
    w = beat_wav(number, root)
    if w is None:
        raise ValueError(f"Beat {number} isn't in the library.")
    dj = w.relative_to(root).parts[0]
    stage = root / dj / STAGE_DIR
    name = stage_name(number)
    sdir = stage / f"{name} Stems"
    if sdir.exists():
        assert sdir.parent.name == STAGE_DIR       # never anything else
        shutil.rmtree(sdir)
    for old in stage.glob(f"{name} Drums *.wav"):
        old.unlink()
    stage.mkdir(parents=True, exist_ok=True)
    put_stems(sdir)
    write_wav24(stage / f"{name} Drums {bpm}bpm.wav", *mix)
    return f"{dj}/{STAGE_DIR}/{name}"


def _file_engine_beat(parent, stems, mix, what, root, rec=None):
    """File effected stems + mix as the next numbered beat, next to its
    parent like any rebuild. Returns (path, report)."""
    root = Path(root)
    rec = rec or load_recipe(root, parent)
    no = next_number(root)
    folder, anc = _family_dir_for(parent, root)
    folder.mkdir(parents=True, exist_ok=True)
    if beat_location(anc, root) == "dj":
        for p in beat_items(anc, root):
            dst = folder / p.name
            if p.parent.resolve() != folder.resolve() and not dst.exists():
                shutil.move(str(p), str(dst))
    bpm = rec["preset"].get("bpm") or rec.get("bpm")
    stem_of = f"{' x '.join(rec['names'])} {rec['title']} {what}"
    fname = f"{no} {stem_of} Drums {bpm}bpm.wav"
    path = folder / fname
    if path.exists():                             # never overwrite
        raise RuntimeError(f"{fname} already exists — not overwriting.")
    write_wav24(path, *mix)
    sdir = folder / f"{no} {stem_of} Stems"
    sdir.mkdir()
    for name, (sL, sR) in stems.items():
        write_wav24(sdir / name, sL, sR)
    (sdir / ".base_clean").write_text("1")     # see tools/base_clean.py
    mid = beat_wav(parent, root)
    if mid is not None and mid.with_suffix(".mid").exists():   # same notes
        shutil.copy2(str(mid.with_suffix(".mid")), str(path.with_suffix(".mid")))
    sync_reason_copy(path)
    save_recipe(root, no, dict(rec, file=fname, parent=int(parent),
                               date=str(date.today()), engine_fx=True))
    append_last_batch(no, root)
    with open(root / "README.txt", "a") as f:
        f.write(f"\nBEAT MACHINE — {date.today()}\n{fname}  ->  "
                f"{rec['folder']}/  (+ Stems)\n  effected copy of beat "
                f"{parent} ({what})\n")
    return path, f"{fname}\n-> effected copy of {parent}"


def import_engine_send(parent, folder, root=ROOT):
    """The Effects page's Send back: a folder it wrote under its exports
    (one wav per lane + mix.wav) becomes a new numbered beat."""
    exports = Path("~/Desktop/Homeroom Sound Engine Exports").expanduser().resolve()
    folder = Path(folder).resolve()
    if exports not in folder.parents or not (folder / "mix.wav").exists():
        raise ValueError("That isn't an Effects page send-back folder.")
    stems = {f.name: read_wav24(f) for f in sorted(folder.glob("*.wav"))
             if f.name != "mix.wav"}
    return _file_engine_beat(int(parent), stems, read_wav24(folder / "mix.wav"),
                             "FX", Path(root))


def _clean_picks(no, picks, shots):
    """The allow-list every rebuild path enforces: a sample only reaches
    the renderer if it came out of that lane's own candidate list. An
    empty value means "surprise me"."""
    out = {}
    for lane, want in (picks or {}).items():
        if not want:
            out[lane] = None
            continue
        if not any(c["path"] == want
                   for c in _lane_candidates(no, lane, shots=shots)):
            raise ValueError(f"That {lane} isn't in your library.")
        out[lane] = want
    return out


CHUNKS_ROOT = Path.home() / "Desktop" / "Homeroom Chunks"


def chunk_dir(no, root=None):
    """Where beat `no` keeps its arrangement chunks: one folder per DJ on
    the Desktop, just chunks for songs (owner 2026-10-17; was beside the
    beat's wav on the drive). The DJ comes from the recipe, so a beat in
    Favorites or Trash still files under its own DJ."""
    w = beat_wav(no, root)
    if w is None:
        raise ValueError(f"No beat {no} to chunk.")
    return CHUNKS_ROOT / (beat_dj(no, root) or "Unsorted") / f"{w.stem} Chunks"


REASON_ROOT = Path.home() / "Desktop" / "Homeroom Loops for Reason"


def sync_reason_copy(wav, dj=None, chunks_dir=None):
    """Copy a loop and its chunks into one easy folder for Reason (owner
    2026-10-25): REASON_ROOT/<DJ>/<NN Title NNNbpm>/. Copies only, so the
    drive library and Reason Voice never notice. The tempo is in the folder
    name, the loop name (already) and every chunk name. Safe to call any
    number of times; it only adds or refreshes files."""
    wav = Path(wav)
    if not wav.exists():
        raise FileNotFoundError(f"Can't copy to the Reason folder, missing: {wav}")
    dj = dj or wav.parent.name
    base = wav.stem.replace(" Drums ", " ", 1)        # "NN Title 134bpm"
    out = REASON_ROOT / dj / base
    out.mkdir(parents=True, exist_ok=True)
    pairs = [(f, out / f.name) for f in (wav, wav.with_suffix(".mid"))
             if f.exists()]
    cd = Path(chunks_dir) if chunks_dir else CHUNKS_ROOT / dj / f"{wav.stem} Chunks"
    if cd.is_dir():
        pairs += [(c, out / f"{base} - {c.name}") for c in sorted(cd.glob("*.wav"))]
    for src, dst in pairs:
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(str(src), str(dst))
    return out


def save_chunk(number, picks=None, root=ROOT, shots=None,
               status=lambda msg: None, trims=None, drops=None, pans=None):
    """Section 4 of the v-next plan — songify. Renders the beat as the
    stem rack is currently set and files it as one more chunk in the
    beat's own Chunks folder, INSTEAD of printing a new numbered beat.

    Owner 2026-09-01: no speculative variants. The chunks are the
    original plus whatever versions he builds by hand in the rack, one
    click each ("Add chunk"), so a song is a folder he drags into Reason
    and arranges.

    Loop-safety comes for free: this is the same render path every beat
    takes, and that path already wraps tails instead of fading edges.
    """
    number = int(number)
    folder = chunk_dir(number, root)
    folder.mkdir(parents=True, exist_ok=True)
    # the untouched beat is chunk 01, pulled in the first time — a song
    # needs the full loop as much as it needs the pieces
    full = folder / "01 Full.wav"
    if not full.exists():
        shutil.copy2(str(beat_wav(number, root)), str(full))
    L, R = swap_many(number, picks or {}, root=Path(root), shots=shots,
                     status=status, trims=trims, drops=drops, pans=pans,
                     render_only=True)
    # a slider left at 0 is not a change, so it doesn't get named
    named = {ln: db for ln, db in (trims or {}).items() if db}
    what, changed = _change_words(sorted(picks or {}), named,
                                  sorted({str(ln).strip().lower()
                                          for ln in (drops or [])}))
    # number from the HIGHEST prefix already in the folder, not the file
    # count: he renames chunks ("Verse.wav") and deletes ones he doesn't
    # want, and counting files made the next chunk reuse a number that was
    # already taken — two different "04"s in the same folder, out of order
    # in Reason's browser.
    used = [int(m.group(1)) for m in
            (re.match(r"(\d+) ", f.name) for f in folder.glob("*.wav")) if m]
    n = max(used or [0]) + 1
    path = folder / f"{n:02d} {what}.wav"
    while path.exists():                          # never overwrite
        n += 1
        path = folder / f"{n:02d} {what}.wav"
    write_wav24(path, L, R)
    sync_reason_copy(beat_wav(number, root), dj=beat_dj(number, root),
                     chunks_dir=folder)
    return {"folder": str(folder), "file": path.name, "count": n,
            "changed": changed}


# ------------------------------------------------ web helpers (player etc.)


def _beat_theory(no, root):
    """What this beat's harmony is, in a shape the card can print — or None.

    Packaging step 3 (2026-07-25), the teaching feature: pure read-and-
    display of what step 1 started writing into the recipe. `why` is the
    owner's own plain-English line for that progression, transcribed from
    theory/progressions.md into progressions_config.json, so an edit there
    changes the card with no code change.

    Returns None rather than raising for every beat that can't answer:
    made before step 1, recipe cleared, drums-only, or a progression that
    has since been renamed. The player must render an old beat exactly as
    it always did.
    """
    try:
        h = load_recipe(root, int(no)).get("harmony")
    except Exception:
        return None
    if not h:
        return None
    import harmony
    prog = harmony.PROGRESSIONS.get(h.get("progression"), {})
    if str(h.get("progression", "")).startswith("gen:"):
        # chord_gen.py (2026-10-29): no hand-written card, say where from
        prog = {"label": "%s loop, generated" %
                h["progression"][4:].replace("_", " "),
                "why": "Made by the chord generator from how real songs in "
                       "this style move between chords."}
    chords = h.get("chords") or []
    return {"key": h.get("key"),
            "progression": prog.get("label") or h.get("progression"),
            "roman": " – ".join(c["roman"] for c in chords),
            "chords": " ".join(c["chord"] for c in chords),
            "voices": ", ".join(h.get("chord_source") or []),
            "why": prog.get("why")}


def ensure_sound_engine(wait=15.0):
    """Start the Sound Engine (port 8767) if nothing is listening there,
    so Rebuild can hand the new beat straight to the Effects page (owner
    2026-10-15). Never a second copy: they share a scratch folder."""
    import socket
    import time

    def up():
        with socket.socket() as sk:
            sk.settimeout(0.3)
            return sk.connect_ex(("127.0.0.1", 8767)) == 0
    if up():
        return True
    here = Path(__file__).resolve().parents[1]
    subprocess.Popen([sys.executable, "-m", "sound_engine.server"], cwd=str(here),
                     env=dict(os.environ, SOUND_ENGINE_NO_BROWSER="1"),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    end = time.time() + wait
    while time.time() < end:
        if up():
            return True
        time.sleep(0.3)
    return False


def _sound_engine_id(wav, root):
    """How the Sound Engine names this beat, or None if it can't take it.

    Its picker is one folder deep (sound_engine/library.py's find_beat
    splits the id on a single "/"), so a beat sitting in a nested folder
    has no id it could be asked for — better to drop the button than to
    hand over a link that 404s.
    """
    try:
        rel = wav.parent.relative_to(Path(root))
    except ValueError:
        return None
    # sound_engine.library.find_beat splits once, so "DJ/Sub/prefix"
    # still resolves: rebuilt beats sit in a Variations subfolder and must
    # open too (owner 2026-10-15: Rebuild goes straight to Effects)
    if not rel.parts or " Drums " not in wav.stem:
        return None
    return "/".join(rel.parts) + "/" + wav.stem.split(" Drums ")[0]


def _batch_beats(root=None):
    """The last batch's tracks with their current location, for the
    player. Missing files (moved by hand) are skipped."""
    root = Path(root or ROOT)
    beats = []
    for no in _load_state().get("last_batch", []):
        w = beat_wav(no, root)
        if w:
            _WAV_AT[int(no)] = w
            beats.append({"no": int(no), "label": w.stem,
                          "loc": beat_location(no, root),
                          "se_id": _sound_engine_id(w, root),
                          "theory": _beat_theory(no, root)})
    return beats


# ---- the batch tabs + waveforms (owner 2026-10-03, notebook/chalkboard
# redesign). Both are READ-ONLY: nothing here moves, writes or deletes.

_BEAT_WAV = re.compile(r"^(\d+) .+ Drums [\d.]+bpm$", re.I)


def _folder_beats(loc, root=None, limit=50):
    """Beats sitting in Favorites ('favorites'), Trash ('trash') or in the
    current batch's host DJ folder ('dj'), newest first, same shape as
    _batch_beats. Trash is listed so a failed beat can be found and moved
    back (design handoff 2026-10-04: fail is recoverable, never a delete).
    Walks only that one folder (never the whole library) and skips the
    Stems/Chunks folders that live beside each beat."""
    root = Path(root or ROOT)
    if loc == "favorites":
        top = FAV_DIR
    elif loc == "trash":
        top = TRASH_DIR
    elif loc == "dj":
        batch = _load_state().get("last_batch", []) if root == ROOT else []
        top = beat_dj(batch[0], root) if batch else None
        if not top:
            return []
    else:
        raise ValueError(f"No such folder: {loc}")
    folder = root / top
    if not folder.is_dir():
        return []
    hits = {}
    for w in folder.rglob("*.wav"):
        if any(p.endswith(("Stems", "Chunks")) for p in w.relative_to(folder).parts[:-1]):
            continue
        m = _BEAT_WAV.match(w.stem)
        if m:
            hits.setdefault(int(m.group(1)), w)
    out = []
    for no in sorted(hits, reverse=True)[:limit]:
        w = hits[no]
        if root == ROOT:
            _WAV_AT[no] = w
        out.append({"no": no, "label": w.stem,
                    "loc": {FAV_DIR: "favorites",
                            TRASH_DIR: "trash"}.get(top, "dj"),
                    "se_id": _sound_engine_id(w, root),
                    "theory": _beat_theory(no, root)})
    return out


_PEAKS = {}                                   # (path, mtime, n) -> peaks
# beat no -> wav path, filled by the listings above so a card's waveform
# doesn't search the whole drive again. Only trusted while the file is
# still there; a moved beat falls back to the full search.
_WAV_AT = {}


def _known_wav(no):
    w = _WAV_AT.get(int(no))
    if not (w and w.exists()):
        w = beat_wav(int(no))
        if w:
            _WAV_AT[int(no)] = w
    return w


def _peaks(wav, n=160):
    """n bars, 0..1, the loudness (RMS) of each slice of the beat — what
    the card draws as its waveform. RMS, not the loudest sample: a
    mastered beat peaks near full scale in every slice, so peaks drew a
    flat block (measured 0.88-1.0 on beat 3187). Cached by file + time."""
    wav = Path(wav)
    key = (str(wav), wav.stat().st_mtime, n)
    if key not in _PEAKS:
        left, right = read_wav24(wav)
        mono = (left + right) / 2
        if not len(mono):
            return [0.0] * n
        edges = np.linspace(0, len(mono), n + 1).astype(int)
        bars = np.array([np.sqrt(np.mean(mono[a:max(b, a + 1)] ** 2))
                         for a, b in zip(edges, edges[1:])])
        top = bars.max() or 1.0
        _PEAKS[key] = [round(float(v), 3) for v in bars / top]
    return _PEAKS[key]


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


# ONE ROW PER INSTRUMENT (owner 2026-07-25: "no longer group instruments
# under one stem — always individual, so I know exactly what's going on").
# A chord lane is chord{slot}[v{voice}]: the SLOT is which chord of the
# progression it plays, the VOICE is which instrument is playing it. One
# instrument playing four chords is still one instrument, so the slots
# collapse into a single row — but two layered instruments are two rows,
# two stems, two volumes, two remove buttons. bass0..N (the melodic bass
# LINE) collapse the same way.
#
# Matching is digit-suffixed on purpose — "bass" with no digit is the 808
# BASS DRUM lane, a different sound entirely, and swallowing it into the
# family would take the wrong thing out.
CHORD_FAM, CHORD_BASS_FAM = "chords", "chordbass"
# opening levels + per-bar accents for the harmony, from the house mix
# numbers in groove.OWNER_TASTE — see the comment there for why
_CHORD_GAIN = OWNER_TASTE["chord_gain"]
_BASS_GAIN = OWNER_TASTE["chord_bass_gain"]
_ACCENTS = OWNER_TASTE["chord_accents"]
_CHORD_LANE = re.compile(r"^chord(\d+)(?:v(\d+))?$")
_CHORD_BASS_LANE = re.compile(r"^bass(\d+)$")
# the answer melody's lane (2026-10-19): its own rack row, "melody"
MELODY_FAM = "melody"
MELODY_UNDER_CHORDS = 10 ** (-2.0 / 20)   # melody peak vs the chords' peak
_MELODY_LANE = re.compile(r"^melody(\d+)$")


def _chord_voice(lane):
    """(slot, voice) for a chord lane — 'chord3' -> (3, 0), 'chord3v1' ->
    (3, 1). None for anything that isn't one."""
    m = _CHORD_LANE.match(lane)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else None


def _chord_family(lane):
    """Which rack row a lane belongs to: 'chord3' -> 'chords', 'chord3v1'
    -> 'chords2' (the second instrument), 'bass3' -> 'chordbass'."""
    sv = _chord_voice(lane)
    if sv:
        return CHORD_FAM if sv[1] == 0 else "%s%d" % (CHORD_FAM, sv[1] + 1)
    if _CHORD_BASS_LANE.match(lane):
        return CHORD_BASS_FAM
    if _MELODY_LANE.match(lane):
        return MELODY_FAM
    return None


def _family_members(fam, lanes):
    """Every real lane a family row stands for, in bar order."""
    return sorted((ln for ln in lanes if _chord_family(ln) == fam),
                  key=lambda ln: int((_CHORD_LANE.match(ln)
                                      or _CHORD_BASS_LANE.match(ln)
                                      or _MELODY_LANE.match(ln)).group(1)))


def _fam_sort(fam):
    """Instrument rows in playing order: the chord instruments (chords,
    chords2, …) and then the bass line."""
    return (fam == CHORD_BASS_FAM, fam == MELODY_FAM, len(fam), fam)


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
        # a family name ("chords", "chords2", "chordbass") is the rack's
        # one-row-per-instrument handle: levelling it moves every chord
        # that instrument plays together, the same way removing it takes
        # all of that instrument out (owner 2026-07-25)
        members = _family_members(lane, preset.get("lanes", {}))
        if not members and lane not in preset.get("lanes", {}):
            raise ValueError(f"Beat {number} has no '{lane}' to turn up "
                             "or down.")
        db = round(max(-TRIM_DB, min(TRIM_DB, db)), 2)
        if db:
            for ln in (members or [lane]):
                out[ln] = db
    return out


def _clean_pans(pans, preset, number):
    """The pan knobs, checked: lane -> -100 (left) .. +100 (right),
    stored as -1..+1. Absolute, so an untouched knob is simply not sent.
    Families move together, same as volume."""
    out = {}
    for lane, v in (pans or {}).items():
        lane = str(lane).strip().lower()
        try:
            v = float(v)
        except (TypeError, ValueError):
            raise ValueError(f"'{v}' isn't a pan for the {lane}.")
        if v != v or v in (float("inf"), float("-inf")):
            raise ValueError(f"'{v}' isn't a pan for the {lane}.")
        members = _family_members(lane, preset.get("lanes", {}))
        if not members and lane not in preset.get("lanes", {}):
            raise ValueError(f"Beat {number} has no '{lane}' to pan.")
        for ln in (members or [lane]):
            out[ln] = round(max(-100.0, min(100.0, v)) / 100.0, 2)
    return out


def _pan_words(pans):
    """'hat L40, snare C' — how a pan reads in the log."""
    seen = {}
    for ln, p in pans.items():
        fam = _chord_family(ln)
        seen.setdefault("bass" if fam == CHORD_BASS_FAM
                        else fam if fam else lane_label(ln), (p, ln))
    def side(p):
        return "C" if not p else ("L%d" % round(-p * 100) if p < 0
                                  else "R%d" % round(p * 100))
    return ", ".join("%s pan %s" % (n, side(p)) for n, (p, ln) in sorted(
        seen.items(), key=lambda kv: _lane_sort(kv[1][1])))


def _trim_words(trims):
    """'kick drum +2 dB, bass -3.5 dB' — how a trim reads in the log.

    Named the way he names them, and one entry per INSTRUMENT: an
    instrument playing four chords moved as one move, so writing it as
    "chord0 -3, chord1 -3, chord2 -3, chord3 -3" described four decisions
    he never made (owner 2026-07-25)."""
    seen = {}
    for ln, db in trims.items():
        fam = _chord_family(ln)
        name = ("bass" if fam == CHORD_BASS_FAM
                else fam if fam else lane_label(ln))
        seen.setdefault(name, (db, ln))
    return ", ".join("%s %+g dB" % (name, db)
                     for name, (db, ln) in sorted(
                         seen.items(), key=lambda kv: _lane_sort(kv[1][1])))


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
    """The isolated wav for one lane — 'kick drum - Real Name.wav' on
    beats made since the rename, plain 'kick.wav' on the older ones. Both
    the owner-facing label and the raw lane key are tried so beats made
    before 2026-07-25 still find their stems. Pass `folder` to skip the
    library walk when the caller already found it."""
    folder = folder if folder is not None else _stems_dir(no, root)
    if not folder:
        return None
    names = [n for n in (lane_label(lane), OLD_LANE_LABELS.get(lane), lane)
             if n]
    for f in sorted(folder.glob("*.wav")):
        if any(f.stem == n or f.stem.startswith(n + " - ") for n in names):
            return f
    return None


def _loop_label(lane):
    import loop_lanes
    return loop_lanes.LABELS.get(lane, lane)


def _beat_stems(no, root=None, folder=None):
    """Every drum in a beat: the real sample behind it, whether it can be
    swapped, and whether there's a solo stem to play. Stamps are the DJ's
    producer tag — shown, but locked (crew rule).

    Owner 2026-07-23 ("control the volume for all sounds"): synthesized
    lanes (the tuned 808 sub, chord/bass pads) have no sample to swap, so
    they never joined kit_spec — but that also meant they never appeared
    here, so the web page had nothing to attach a volume slider to, even
    though the trim mechanism (_clean_trims, swap_many) already works on
    any lane in preset["lanes"] and the JS already renders a slider for a
    locked row. Listing every real lane here is the actual fix; nothing
    downstream needed to change."""
    root = Path(root or ROOT)
    no = int(no)
    rec = load_recipe(root, no)
    out = []
    # stamps live outside kit_spec but are still part of the beat — he
    # should SEE his producer tag even though he can't swap it. Same for
    # any other lane that's rendered but has no kit_spec entry (sub,
    # chordN, bassN) — it gets a volume control, just no swap dropdown.
    named = set(rec["kit_spec"]) | set(rec.get("stamp_paths", {}))
    lanes = (list(rec["kit_spec"])
             + [ln for ln in rec.get("stamp_paths", {})
                if ln not in rec["kit_spec"]]
             + [ln for ln in rec["preset"].get("lanes", {})
                if ln not in named])
    if folder is None:                # walk the library once, not per lane
        folder = _stems_dir(no, root)
    # chord/bass lanes are voiced live from his library rather than from a
    # single kit_paths entry, so their real files live here (owner
    # 2026-07-25: the rack said "built from scratch" over audio that was
    # 100% his own brass and strings, which is why he believed the
    # his-instruments rule was being ignored — the label was the bug).
    voiced = (rec.get("harmony") or {}).get("voice_files") or {}
    # which INSTRUMENT each chord lane is ("horns stack"), so a row can be
    # named for the thing playing it instead of the generic word "chords"
    vnames = (rec.get("harmony") or {}).get("voice_names") or {}
    # One row per instrument. The chord SLOTS of a single instrument
    # collapse (one instrument playing four chords is one instrument, and
    # removing a single bar's worth would make it vanish mid-beat, which
    # he ruled out) — but a second layered instrument is its own row, its
    # own stem, its own volume. Owner 2026-07-25.
    fams = {}
    for lane in list(lanes):
        fam = _chord_family(lane)
        if fam:
            fams.setdefault(fam, []).append(lane)
            lanes.remove(lane)
    for lane in sorted(lanes, key=_lane_sort):
        locked = lane == "stamp" or lane.startswith("stamp")
        path = (rec["stamp_paths"] if locked else rec["kit_paths"]).get(lane)
        spec = rec["kit_spec"].get(lane)
        out.append({
            "lane": lane,
            "label": (_loop_label(lane) if rec.get("loops_only")
                      else lane_label(lane)),
            "loop": bool(rec.get("loops_only")),
            "role": spec[0] if spec else lane,
            "sample": Path(path).stem if path else "built from scratch",
            "pack": _pack_of(path),
            # a lane with no file behind it stays locked (the tuned 808
            # "sub" is the case) — only the chord/bass families below are
            # deliberately unlocked for removal
            "locked": locked or not path,
            "can_swap": bool(path) and not locked and not rec.get("engine_fx"),
            "why": ("the DJ's producer tag — same in every beat they make"
                    if locked else
                    "synthesised, not a sample" if not path else ""),
            "stem": bool(_stem_wav(no, lane, root, folder=folder)),
            "pan": _lane_pan(rec, lane),
        })
    for fam in sorted(fams, key=_fam_sort):
        members = fams.get(fam)
        if not members:
            continue
        files, seen = [], set()
        for ln in sorted(members, key=_lane_sort):
            for f in voiced.get(ln) or []:
                if f not in seen:
                    seen.add(f)
                    files.append(f)
        names = [Path(f).stem for f in files]
        if names:
            sample = names[0] if len(names) == 1 else \
                "%s + %d more" % (names[0], len(names) - 1)
            why = "played from your library" + (
                "" if len(names) == 1 else " (%s)" % ", ".join(names[1:5]))
        else:                        # a beat made before provenance landed
            sample, why = "from your library", "played from your library"
        # name the row for the INSTRUMENT, not the word "chords" — the
        # several files under it are one instrument's multisamples (a horn
        # patch has a different sample per note), which is why they are one
        # row and not several. The bass LINE is just "bass".
        if fam == CHORD_BASS_FAM:
            # an 808 playing the chords is still called the 808 (2026-09-23)
            label = ("808" if (rec.get("harmony") or {}).get("bass808")
                     else "bass")
        else:
            # beats made before voice_names existed still recorded what
            # sounded, in chord_source — use it rather than showing them
            # the generic word
            was = (rec.get("harmony") or {}).get("chord_source") or []
            label = next((vnames[ln] for ln in sorted(members, key=_lane_sort)
                          if vnames.get(ln)),
                         (was[0] if len(was) == 1 else fam))
        out.append({
            "lane": fam,
            "label": label,
            "role": fam,
            "sample": sample,
            "pack": _pack_of(files[0]) if files else "",
            "locked": False,
            # Swappable since 2026-08-04 (owner: "chords and bass can now
            # have drop downs and dice"). What it offers is an INSTRUMENT,
            # not a file — the DJ's identity still picks the default, this
            # just lets him overrule it for one beat. Before this the row
            # could only be levelled and removed.
            "can_swap": not (fam == CHORD_BASS_FAM
                             and (rec.get("harmony") or {}).get("bass808"))
                        and fam != MELODY_FAM
                        and not rec.get("engine_fx"),
            "voices": fam != MELODY_FAM,          # the dropdown lists instruments
            "why": why,
            "members": sorted(members, key=_lane_sort),
            "stem": bool(_stem_wav(no, members[0], root, folder=folder)),
            "pan": _lane_pan(rec, sorted(members, key=_lane_sort)[0]),
        })
    return out


def _lane_pan(rec, lane):
    """Where a lane sits now, -100 (left) .. +100 (right); 0 if unknown."""
    t = (rec["preset"].get("lanes") or {}).get(lane)
    try:
        return int(round(float(t[0]) * 100))
    except (TypeError, ValueError, IndexError):
        return 0


def _qs_db(raw):
    """A dB value off the query string, clamped — never trusted."""
    try:
        db = float(raw)
    except (TypeError, ValueError):
        return 0.0
    if db != db or db in (float("inf"), float("-inf")):
        return 0.0
    return max(-TRIM_DB, min(TRIM_DB, db))


_TRACK_GAIN = {}          # beat no -> stems-to-track gain, computed once


def _rms(L, R):
    """How loud a stereo buffer actually is, which is what an ear hears —
    unlike the peak, which one transient can set."""
    return float(np.sqrt((np.asarray(L) ** 2).mean()
                         + (np.asarray(R) ** 2).mean()) / np.sqrt(2))


def _track_gain(no, root=None, folder=None):
    """How much louder a lane is IN THE TRACK than in its stem file.

    The stems are printed with one shared gain that puts the loudest of
    them at -6 dBFS (crew.render_crew_beat: it protects headroom when the
    set lands in Reason, and being SHARED it keeps the balance between
    stems exact). The side effect was that soloing a stem played it well
    below its level in the beat, which is what he heard as "the stems are
    a different volume than the track". One shared gain in means one
    shared gain out: the sum of the stems is the whole mix scaled by that
    same factor, so comparing that sum against the finished beat recovers
    it.

    Matched on RMS, not peak. The finished beat has been through the
    master chain (LUFS normalisation and a limiter), which flattens peaks
    without changing how loud the thing sounds — peak-matching a limited
    mix against an unlimited sum lands roughly 5 dB out. RMS is what
    "the same volume" means to an ear.
    """
    no = int(no)
    if no in _TRACK_GAIN:
        return _TRACK_GAIN[no]
    g = 1.0
    try:
        w = beat_wav(no, root)
        folder = folder if folder is not None else _stems_dir(no, root)
        if w and folder:
            L = R = None
            for f in sorted(folder.glob("*.wav")):
                sL, sR = read_wav24(f)
                if L is None:
                    L, R = sL, sR
                else:
                    n = min(len(L), len(sL))
                    L, R = L[:n] + sL[:n], R[:n] + sR[:n]
            tL, tR = read_wav24(w)
            srms = _rms(L, R)
            trms = _rms(tL, tR)
            if srms > 1e-9 and trms > 1e-9:
                g = trms / srms
    except Exception:
        g = 1.0               # never let a preview fail over a level
    _TRACK_GAIN[no] = g
    return g


def _solo_audio(no, lane, root=None, folder=None):
    """(L, R) for ONE rack row, played on its own.

    A row is an instrument, not always a single lane: the harmony rows
    stand for every chord that instrument plays (chord0, chord1, …), so
    soloing one has to sum its lanes — otherwise the button reaches for a
    file called "chords", nothing has that name, and the row silently
    refuses to play. That was the "some of the stems do not let me click
    and preview them" the owner reported on 2026-07-25."""
    folder = folder if folder is not None else _stems_dir(no, root)
    if not folder:
        return None
    try:
        rec = load_recipe(Path(root or ROOT), int(no))
        lanes = list(rec["preset"].get("lanes", {})) or list(rec["kit_spec"])
    except Exception:
        lanes = []
    L = R = None
    for ln in (_family_members(lane, lanes) or [lane]):
        w = _stem_wav(no, ln, root, folder=folder)
        if not w:
            continue
        sL, sR = read_wav24(w)
        if L is None:
            L, R = sL, sR
        else:
            n = min(len(L), len(sL))
            L, R = L[:n] + sL[:n], R[:n] + sR[:n]
    return None if L is None else (L, R)


_PREVIEW_CACHE = {}          # query string -> rendered bytes, last 3 only


def _preview_render(query, q, shots=None, root=None):
    """The beat as the rack is currently SET — swaps, volumes and
    removals all in — for /mix. Runs the real render path with
    render_only=True and prints nothing, so what he hears is
    byte-for-byte what Rebuild will produce.

    ONE path for every kind of change (2026-08-04). Volumes and removals
    used to take a shortcut that summed the printed stems instead of
    re-rendering: faster (0.13s vs 0.40s warm), but the stem sum is the
    beat BEFORE the master bus, so it played **8 dB under** what Rebuild
    actually prints — measured on beat 1774 at kick -3. Every level move
    he judged was judged against the wrong mix. _preview_mix's own
    docstring called this ("if the two ever drift enough to mislead him,
    the upgrade is to run the master chain over this sum"); the cheapest
    way to run the master chain is to run the master, so the shortcut is
    deleted rather than patched. 0.27s is a fair price for the preview
    telling the truth, and it leaves one preview path instead of two that
    can disagree.

    A render is a fraction of a second, and a browser asks for the same
    URL more than once (it re-requests with a Range header before it will
    seek), so the last few results are kept.
    """
    hit = _PREVIEW_CACHE.get(query)
    if hit is not None:
        return hit
    no = int(q.get("no", [""])[0])
    picks = json.loads(q.get("picks", ["{}"])[0] or "{}")
    if not isinstance(picks, dict):
        raise ValueError("bad picks")
    shots = shots if shots is not None else build_shots()
    # same allow-list the rebuild enforces: a path only reaches disk if
    # it came out of this lane's own candidate list
    clean = {}
    for lane, want in picks.items():
        lane = str(lane).strip().lower()
        if not want:
            continue
        if not any(c["path"] == want
                   for c in _lane_candidates(no, lane, shots=shots)):
            raise ValueError(f"That {lane} isn't in your library.")
        clean[lane] = want
    trims = {}
    for bit in str(q.get("trims", [""])[0] or "").split(","):
        name, _, val = bit.partition(":")
        if name.strip():
            trims[name.strip().lower()] = _qs_db(val)
    pans = {}
    for bit in str(q.get("pans", [""])[0] or "").split(","):
        name, _, val = bit.partition(":")
        if name.strip():
            pans[name.strip().lower()] = val
    gone = [b.strip().lower()
            for b in str(q.get("drop", [""])[0] or "").split(",") if b.strip()]
    L, R = swap_many(no, clean, root=Path(root or ROOT), shots=shots,
                     trims=trims, drops=gone, pans=pans, render_only=True,
                     solo=(q.get("solo", [""])[0].strip().lower() or None))
    data = wav24_bytes(L, R)
    _PREVIEW_CACHE[query] = data
    for old in list(_PREVIEW_CACHE)[:-3]:
        del _PREVIEW_CACHE[old]
    return data


# The instruments a harmony row can be handed to, in plain English. Keys
# are the voice names _build_chords already understands (instrument_
# sampler.VOICES, plus the two that live in their own modules) — so the
# dropdown value IS the thing the renderer takes, with nothing to
# translate in between.
CHORD_VOICE_NAMES = {
    "piano": "Piano",
    "guitar": "Guitar",
    "horns": "Horns (brass)",
    "strings": "Strings",
    "bell": "Bells",
    "organ": "Organ",
    "wood": "Woodwind",
    "choir": "Choir",
    "pad": "Pad",
    "pluck": "Pluck",
    "synth": "Synth",
    "orchestral": "Orchestral (strings + brass)",
    "chip": "8-bit / chiptune",
    "loop": "Melodic loop (a finished riff)",
}


def _best_folder(idx, groups, notes):
    """The entries of ONE folder inside `groups` that can reach every one
    of `notes` within MAX_SHIFT — or None if no single folder can.

    The folder is the unit because _one_instrument's unit is the folder
    (same directory + same instrument type), not the file — a real
    sampled piano is one instrument spread over a recording every few
    notes. Per file would reject that piano; per group would pass
    instruments that then fail the render.

    Both jobs this does are the same question. The rack asks it to decide
    what to OFFER (_chord_voices), and _build_chords asks it to decide
    what to PLAY when the owner has picked — handing the renderer this
    one folder is what makes his pick actually land, because nearest()
    otherwise shops per note across the whole group and pulls a second
    folder in, which the one-instrument rule then rejects."""
    import instrument_sampler
    want = set(instrument_sampler._as_groups(groups))
    shift = instrument_sampler.MAX_SHIFT
    folders = {}
    for e in idx:
        if e.get("group") in want:
            folders.setdefault(str(Path(e["path"]).parent), []).append(e)
    fits = [got for got in folders.values()
            if all(min(abs(e["note"] - n) for e in got) <= shift
                   for n in notes)]
    # widest wins: most notes reachable without stretching, so the arp
    # and the stack both stay on it
    return max(fits, key=len) if fits else None


def _voice_covers(idx, groups, notes):
    return _best_folder(idx, groups, notes) is not None


def _chord_voices(rec=None, idx=None, sidx=None):
    """Which instruments can play THIS beat's harmony, for the rack's
    chord/bass dropdown (owner 2026-08-04: "chords and bass can now have
    drop downs and dice"). Unlike a drum, the value is an instrument
    FAMILY, not one file: a chord voice is a whole multisample (a horn
    patch has a different sample per note), so there is nothing single
    to pick.

    Filtered against the beat's own notes, not just "does the library
    own a piano". Measured on beat 1776 while building this: EVERY
    instrument fell through to the DJ's own choice, because a 3-note
    chord kept drawing its notes from two different folders and the
    2026-08-03 one-instrument-per-stem rule rejected the lot. Offering
    all fourteen anyway would have recreated the exact bug this session
    started with — pick a sound, hear no change. So the menu only lists
    what will actually play, and a beat whose notes nothing can cover
    gets an honest empty list instead of fourteen dead options.

    Without a recipe (no notes to check) every stocked voice is listed —
    that path is only the allow-list check, where breadth is safe."""
    notes = sorted({n for ch in ((rec or {}).get("harmony") or {}).get(
        "chords") or [] for n in (ch.get("notes") or [])})
    out = []
    try:
        import instrument_sampler
        idx = idx if idx is not None else instrument_sampler.scan()
        for g, groups in instrument_sampler.VOICES.items():
            # [:1] — offer a voice only when the group it is NAMED for can
            # play the beat. "pluck" falling back to its synth group would
            # put Pluck in the menu and then hand back a synth.
            if not instrument_sampler.pool(idx, groups[:1]):
                continue
            if not notes or _voice_covers(idx, groups[:1], notes):
                out.append(g)
    except Exception:
        pass
    try:
        import string_sampler
        sidx = sidx if sidx is not None else string_sampler.scan()
        if sidx and (not notes or _voice_covers(sidx, ("string",), notes)
                     or _voice_covers(sidx, {e.get("group") for e in sidx},
                                      notes)):
            out.append("strings")
    except Exception:
        pass
    # a melodic loop is a finished riff in ONE file, so it never has a
    # second instrument to fail on and never needs per-note coverage
    out.append("loop")
    return [{"path": g, "name": CHORD_VOICE_NAMES.get(g, g.title()),
             "pack": "your instruments", "current": False}
            for g in sorted(set(out), key=lambda g: CHORD_VOICE_NAMES
                            .get(g, g).lower())]


# instrument group -> the word the dropdowns show for it
TYPE_NAMES = {"piano": "Piano", "guitar": "Guitar", "bell": "Bells",
              "organ": "Organ", "brass": "Brass", "wood": "Woodwind",
              "string": "Strings", "choir": "Choir", "pluck": "Pluck",
              "pad": "Pad", "synth": "Synth", "chip": "8-bit"}


def _exact_voices(g, notes, rec, idx, s_all):
    """The exact instruments inside chord voice `g` that can play every one
    of `notes` (owner 2026-09-28: pick Trumpet vs Tuba vs his own horn
    stab, not just "brass"). Values: "multi:<instrument>|<articulation>"
    (a note-by-note library), "file:<path>" (one of his own sounds, which
    the engine already stretches up to an octave once chosen --
    PREFER_MAX_SHIFT), "style:<style>" (London strings), "loop:<path>" (an
    in-key melodic loop). Listed only if it will actually play, same
    promise as _chord_voices."""
    import instrument_sampler
    out = []

    def add(ref, name, pack):
        out.append({"path": ref, "name": name, "pack": pack,
                    "current": False})
    if g == "strings":
        import string_sampler
        for style in sorted({e["style"] for e in s_all}):
            pool = string_sampler.beat_pool(s_all, style)
            if pool and (not notes or _voice_covers(
                    pool, {e.get("group") for e in pool}, notes)):
                add("style:" + style, "London Strings — " + style,
                    "London Strings")
        return out
    if g == "loop":
        h = rec.get("harmony") or {}
        if h.get("root") and h.get("mode"):
            import chord_synth
            from key_context import KeyContext
            for e in chord_synth.sample_pool(KeyContext(h["root"], h["mode"]),
                                             rec["preset"].get("bpm")):
                add("loop:" + e["path"], e["name"], Path(e["path"]).parent.name)
        return out
    groups = instrument_sampler.VOICES.get(g)
    if not groups or g == "chip":
        return out
    combos = {}
    for e in idx:
        if e.get("group") != groups[0]:
            continue
        if e.get("multi"):
            combos.setdefault((e["multi"], e.get("art", "-")), []).append(e)
        elif all(abs(e["note"] - n) <= instrument_sampler.PREFER_MAX_SHIFT
                 for n in notes):
            add("file:" + e["path"], e["name"],
                _pack_of(e["path"]) or Path(e["path"]).parent.name)
    for (multi, art), es in sorted(combos.items()):
        if all(min(abs(e["note"] - n) for e in es)
               <= instrument_sampler.MAX_SHIFT for n in notes):
            inst = multi.split("/")[-1]
            add("multi:%s|%s" % (multi, art),
                inst if art in ("-", "") else "%s — %s" % (inst, art),
                multi.split("/")[0])
    return out


def _chord_choices(rec):
    """A chord row's two dropdowns (owner 2026-09-28). Step 1 = the
    instrument TYPE (the old one-step list, _chord_voices): its value is
    the voice, and the machine picks inside it as before. Step 2 = the
    exact instruments of that type, grouped by the words in their names;
    value "voice::exact". Also the allow-list every rebuild path checks."""
    import sound_words
    notes = sorted({n for ch in ((rec or {}).get("harmony") or {}).get(
        "chords") or [] for n in (ch.get("notes") or [])})
    import instrument_sampler
    import string_sampler
    idx = instrument_sampler.scan()    # read once, not once per type
    try:
        s_all = string_sampler.scan()
    except Exception:
        s_all = []
    out = []
    for v in _chord_voices(rec, idx=idx, sidx=s_all):
        g, tname = v["path"], v["name"].split(" (")[0]
        out.append(dict(v, type=tname, any=True, words=[]))
        out += [dict(e, path="%s::%s" % (g, e["path"]), type=tname)
                for e in sound_words.tag(_exact_voices(g, notes, rec, idx, s_all))]
    return out


def _loop_type(e):
    """A loop's instrument for the Loops page's first dropdown: from its
    name, else its folder names, else "Unlabeled" (owner 2026-09-28)."""
    import instrument_sampler
    g = (instrument_sampler.group_of(e["name"])
         or instrument_sampler.group_of(e["folder"].replace("/", " ")))
    return TYPE_NAMES.get(g, "Unlabeled")


def _bass_files(rec):
    """The bass row's dropdown: his real bass one-shots (scan_bass), grouped
    by pack like a drum row. No 808s -- the bass LINE never plays one
    outside the legacy 808 beats, whose row is locked and lists nothing.
    Same pool _build_chords draws from, so every entry here will play."""
    h = rec.get("harmony") or {}
    if h.get("bass808"):
        return []
    import instrument_sampler
    current, seen, out = h.get("bass_file"), set(), []
    if not current:            # made before bass_file: the row's own file
        current = next(iter((h.get("voice_files") or {}).get("bass0") or []),
                       None)
    for e in instrument_sampler.scan_bass():
        p = str(e["path"])
        if p in seen or "808" in Path(p).name:
            continue
        seen.add(p)
        out.append({"path": p, "name": Path(p).stem, "pack": _pack_of(p),
                    "current": p == current})
    out.sort(key=lambda d: (d["pack"].lower(), d["name"].lower()))
    return out


def _lane_candidates(no, lane, shots=None, root=None):
    """Every sample in the library that could fill this lane, grouped by
    pack for the dropdown. Also the allow-list the rebuild validates
    against: a path the client sends back is only ever accepted if it
    came from here, so no client string reaches disk unchecked."""
    import sound_words
    root = Path(root or ROOT)
    rec = load_recipe(root, int(no))
    lane = str(lane).strip().lower()
    # a harmony row ("chords", "chords2", "chordbass") is an INSTRUMENT
    # row, not a file row — it offers voices instead of samples
    if rec.get("loops_only"):
        # five-lane loops beat: that lane's own category. Owner 2026-09-28:
        # instrument type first (lead/chords lanes), then tempo, then the
        # sounds grouped by the words in their names.
        import loop_lanes
        if lane not in rec["kit_paths"]:
            raise ValueError(f"Beat {no} has no '{lane}'.")
        current = rec["kit_paths"].get(lane)
        typed = loop_lanes.lane_category(lane) in ("lead", "chords")
        # owner 2026-10-07: swapped loops that need a big time-stretch
        # smear, so the list only offers tempos near the beat's own
        pool = loop_lanes.near_tempo(loop_lanes.candidates(lane), lane,
                                     rec["loop_state"]["bpm"], current)
        return sound_words.tag(
            [{"path": e["path"], "name": e["name"], "pack": e["folder"],
              "current": e["path"] == current, "bpm": e.get("bpm"),
              "type": _loop_type(e) if typed else None}
             for e in pool], by="type")
    if _family_members(lane, rec["preset"].get("lanes", {})):
        if lane == CHORD_BASS_FAM:
            return sound_words.tag(_bass_files(rec))
        return _chord_choices(rec)
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
    return sound_words.tag(out)       # grouped by name words (2026-09-28)


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
<title>Homeroom Studios</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Inter:wght@400;500;600;700&display=swap">
<style>
 /* ---------------------------------------------------------------
    Homeroom Studios -- "Chemistry" look (owner-approved handoff,
    2026-11-01, UI Handoff/Claude Final Package). Matte black panels,
    ivory serif wordmark, four accents. Loops only swaps the accent
    ROLES (green leads instead of orange); the palette never changes.
    --------------------------------------------------------------- */
 :root {
   --orange: #FF5A12; --green: #7CFF32; --violet: #A66CFF; --blue: #4E8DFF;
   --bg: #08090b; --panel: #111215; --panel2: #16171b; --well: #0c0d10;
   --line: #24262c; --line2: #33363e;
   --text: #ece6d6; --dim: #a7a7ad; --dimmer: #74767e; --bad: #ff7b6b;
   /* roles: Beat mode */
   --lead: var(--orange); --wave: var(--green);
   --u1: var(--violet); --u2: var(--blue);
   --c0: var(--orange); --c1: var(--violet); --c2: var(--blue); --c3: var(--green);
   --ink-on-lead: #0b0b0b;
   --serif: "Cinzel", "Trajan Pro", Georgia, serif;
   --sans: "Inter", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
   --mono: ui-monospace, "SF Mono", Menlo, monospace;
   --r: 10px;
   --grain: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .05 0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E");
 }
 /* Loops only: same four colours, different jobs */
 body.loops {
   --lead: var(--green); --wave: var(--orange);
   --u1: var(--blue); --u2: var(--violet);
   --c0: var(--green); --c1: var(--blue); --c2: var(--violet); --c3: var(--orange);
 }
 * { box-sizing: border-box; }
 [hidden] { display: none !important; }
 html, body { margin: 0; }
 body { background: var(--bg) var(--grain); color: var(--text); font: 14px/1.4 var(--sans);
        min-height: 100vh; display: grid; grid-template-columns: 96px minmax(0, 1fr);
        padding-bottom: 84px; }
 button, select, input { font: inherit; color: inherit; }
 button { cursor: pointer; }
 :focus-visible { outline: 2px solid var(--lead); outline-offset: 2px; }
 svg.ic { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 1.8;
          stroke-linecap: round; stroke-linejoin: round; flex: none; }

 /* ------------------------------------------------ sidebar */
 .side { position: sticky; top: 0; height: 100vh; background: #0a0b0d;
         border-right: 1px solid var(--line); display: flex; flex-direction: column;
         align-items: stretch; gap: 4px; padding: 14px 0; }
 .side .logo { display: grid; place-items: center; padding: 4px 0 18px; color: var(--text); }
 .side .logo svg { width: 46px; height: 54px; }
 .side a:not(.logo), .side button { display: flex; flex-direction: column; align-items: center; gap: 6px;
         padding: 14px 4px; color: var(--dim); text-decoration: none; background: none; border: 0;
         border-left: 3px solid transparent; font-size: 12.5px; text-align: center; }
 .side a:not(.logo):hover, .side button:hover { color: var(--text); background: #ffffff08; }
 .side .here { color: var(--lead) !important; border-left-color: var(--lead) !important;
               background: color-mix(in srgb, var(--lead) 12%, transparent) !important; }
 .side svg.ic { width: 28px; height: 28px; stroke-width: 1.6; }

 /* ------------------------------------------------ masthead */
 .main { min-width: 0; padding: 0 22px 18px; }
 .mast { display: flex; align-items: center; padding: 16px 0 12px; }
 .word { display: inline-flex; flex-direction: column; align-items: center; color: var(--text); }
 .word .hr { font: 600 38px/1 var(--serif); letter-spacing: .16em; display: flex; align-items: center; gap: 20px; }
 .word .hr::before, .word .hr::after { content: ""; width: 62px; height: 1.5px; background: currentColor; opacity: .8; }
 .word .st { font: 500 11px/1 var(--serif); letter-spacing: .62em; margin-top: 8px; display: flex;
             align-items: center; gap: 12px; padding-left: .62em; }
 .word .st::before, .word .st::after { content: ""; width: 60px; height: 1px; background: currentColor; opacity: .6; }

 /* ------------------------------------------------ panels */
 .board { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.55fr); gap: 14px; }
 .panel { background: var(--panel) var(--grain); border: 1px solid var(--line); border-radius: 12px;
          padding: 16px 18px; min-width: 0; }
 .board > .cls, .board > .params { border-top: 2px solid var(--lead); }
 .panel h2 { margin: 0 0 12px; display: flex; align-items: center; gap: 14px;
             font: 500 20px var(--sans); color: var(--text); }
 .num { width: 40px; height: 40px; border-radius: 50%; border: 2px solid var(--lead);
        display: grid; place-items: center; font: 500 21px var(--sans); color: var(--text); flex: none; }
 label, .lbl { color: var(--text); font-size: 14px; }
 select, input[type=text], input[type=number] {
   background: var(--well); border: 1px solid var(--line2); border-radius: 6px; padding: 8px 10px;
   color: var(--text); min-width: 0; }
 select { appearance: none; -webkit-appearance: none; padding-right: 30px;
   background-image: linear-gradient(45deg, transparent 50%, var(--dim) 50%), linear-gradient(135deg, var(--dim) 50%, transparent 50%);
   background-position: calc(100% - 15px) 52%, calc(100% - 10px) 52%; background-size: 5px 5px; background-repeat: no-repeat; }
 select:focus, input:focus { border-color: var(--lead); outline: none; }
 .hint { color: var(--dimmer); font-size: 12.5px; margin: 6px 0 0; }
 .hint.bad, .bad { color: var(--bad); }

 /* step 1: class tabs + portraits */
 .tabs { display: grid; grid-template-columns: 1fr 1fr; background: var(--well); border: 1px solid var(--line);
         border-radius: 6px; padding: 3px; margin-bottom: 12px; }
 .tabs button { background: none; border: 0; padding: 8px 6px; color: var(--dim); border-radius: 4px;
                border-bottom: 3px solid transparent; }
 .tabs button[aria-selected=true] { color: var(--text); background: var(--panel2); border-bottom-color: var(--lead); }
 .roster .djs { display: flex; gap: 12px; overflow-x: auto; padding: 4px 2px 8px; scroll-snap-type: x proximity; }
 .roster .dj { flex: none; width: 92px; display: flex; flex-direction: column; align-items: center; gap: 6px;
               cursor: pointer; position: relative; scroll-snap-align: start; text-align: center; }
 .roster .dj input { position: absolute; opacity: 0; pointer-events: none; }
 .roster .dj .dot { width: 82px; height: 82px; border-radius: 50%; border: 2px solid var(--line2);
   background: #1a1b20 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 80 80'%3E%3Ccircle cx='40' cy='31' r='14' fill='%233a3c44'/%3E%3Cpath d='M14 76c3-17 13-25 26-25s23 8 26 25z' fill='%233a3c44'/%3E%3C/svg%3E") center/100% no-repeat;
   transition: border-color .15s, box-shadow .15s; }
 .roster .dj:hover .dot { border-color: var(--dim); }
 .roster .dj input:checked ~ .dot { border: 3px solid var(--lead); box-shadow: 0 0 0 3px color-mix(in srgb, var(--lead) 25%, transparent); }
 .roster .dj input:focus-visible ~ .dot { outline: 2px solid var(--lead); outline-offset: 3px; }
 .roster .dj .who { display: flex; flex-direction: column; font-size: 12px; line-height: 1.2; }
 .roster .dj .name { color: var(--text); }
 .roster .dj .built { color: var(--dimmer); font-size: 11px; }
 .roster .dj .bpm { display: none; }
 .roster .dj .ord { position: absolute; top: 0; right: 4px; min-width: 22px; height: 22px; border-radius: 11px;
   background: var(--lead); color: var(--ink-on-lead); font: 700 12px/22px var(--sans); text-align: center; }
 .roster .dj .ord:empty { display: none; }
 .popnote { color: var(--dimmer); font-size: 12px; margin: 4px 0 0; }
 #hosthint { display: block; color: var(--lead); font-size: 12.5px; min-height: 18px; margin-top: 4px; }

 /* step 2: parameters */
 .params { display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 8px 20px; align-items: start; }
 .params h2 { grid-column: 1 / -1; }
 .pgrid { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); gap: 10px 16px; }
 .fld { display: flex; flex-direction: column; gap: 5px; min-width: 0; }
 .fld.wide { grid-column: 1 / -1; }
 .fld.cnt { grid-row: span 2; }
 .fld small { color: var(--dimmer); font-size: 12px; }
 .spin { display: flex; align-items: center; gap: 8px; }
 .spin input[type=number] { width: 76px; text-align: center; font: 600 22px var(--sans); padding: 6px; -moz-appearance: textfield; }
 .spin input::-webkit-inner-spin-button, .spin input::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
 .arrows { display: flex; flex-direction: column; gap: 4px; }
 .arrows button { width: 32px; height: 22px; border: 1px solid var(--line2); background: var(--well);
                  border-radius: 5px; font-size: 10px; color: var(--text); }
 .arrows button:hover, .pm button:hover { border-color: var(--lead); }
 /* the style picker: a multi-pick dropdown of the genre cards */
 .pick { position: relative; }
 .picker { display: flex; align-items: center; gap: 6px; min-height: 38px; background: var(--well);
           border: 1px solid var(--line2); border-radius: 6px; padding: 4px 30px 4px 8px; cursor: pointer; position: relative; }
 .pick.open .picker { border-color: var(--lead); }
 .chev { position: absolute; right: 12px; top: 50%; width: 7px; height: 7px; border: solid var(--dim);
         border-width: 0 1.5px 1.5px 0; transform: translateY(-70%) rotate(45deg); }
 .chips { display: flex; flex-wrap: wrap; gap: 4px; min-width: 0; }
 .chips .ph { color: var(--dimmer); }
 .chip { display: inline-flex; align-items: center; gap: 5px; background: var(--panel2); border: 1px solid var(--line2);
         border-radius: 4px; padding: 1px 4px 1px 6px; font-size: 12.5px; }
 .chip b { color: var(--lead); }
 .chip .x { color: var(--dim); padding: 0 3px; cursor: pointer; }
 .pop { display: none; position: absolute; z-index: 40; top: calc(100% + 4px); left: 0; width: min(420px, 90vw);
        max-height: 360px; overflow: auto; background: var(--panel2); border: 1px solid var(--line2);
        border-radius: 8px; padding: 8px; box-shadow: 0 14px 40px #000a; }
 .pick.open .pop { display: block; }
 .pop .dj { display: grid; grid-template-columns: 18px 1fr auto 20px; align-items: center; gap: 8px;
            padding: 7px 8px; border-radius: 6px; cursor: pointer; }
 .pop .dj:hover { background: #ffffff0a; }
 .pop .dj input { accent-color: var(--lead); margin: 0; }
 .pop .dj .dot { display: none; }
 .pop .dj .who { display: flex; flex-direction: column; min-width: 0; }
 .pop .dj .built { color: var(--dimmer); font-size: 12px; }
 .pop .dj .bpm { color: var(--dim); font: 12px var(--mono); }
 .pop .dj .bpm::after { content: " bpm"; }
 .pop .dj .ord { color: var(--lead); font-weight: 700; text-align: right; }
 /* tempo flask */
 .tempo { display: flex; align-items: center; gap: 12px; padding-left: 18px; border-left: 1px solid var(--line); }
 .flask { width: 124px; height: 166px; flex: none; }
 .flask .glass { fill: #ffffff07; stroke: var(--text); stroke-width: 2.5; stroke-linejoin: round; }
 .flask .liq { fill: var(--lead); transition: y .35s ease, height .35s ease; }
 .flask .shine { fill: #ffffff22; }
 .flask .tk line { stroke: #0b0b0bcc; stroke-width: 1.4; }
 .flask .tk text { fill: #0b0b0b; font: 600 9.5px var(--sans); }
 .flask .tk.dry line { stroke: var(--dim); }
 .flask .tk.dry text { fill: var(--dim); }
 .flask.auto .liq { opacity: .25; }
 .bpmbox { display: flex; flex-direction: column; align-items: center; gap: 10px; }
 .tspin { flex-direction: column; gap: 4px; }
 #tempo { width: 92px; text-align: center; font: 600 32px/1 var(--sans); background: none; border: 1px solid transparent; padding: 2px; }
 #tempo:hover { border-color: var(--line2); }
 #tempo::placeholder { color: var(--dim); font-size: 24px; }
 .tspin .unit { font-size: 14px; color: var(--text); margin-top: -2px; }
 .pm { display: flex; gap: 12px; margin-top: 4px; }
 .pm button { width: 38px; height: 38px; border-radius: 50%; border: 1.5px solid var(--dim); background: none;
              font-size: 20px; line-height: 1; color: var(--text); }
 .toggle { display: flex; align-items: center; gap: 10px; cursor: pointer; }
 .toggle input { position: absolute; opacity: 0; pointer-events: none; }
 .toggle .sw { width: 40px; height: 22px; border-radius: 11px; background: var(--line2); position: relative; flex: none; transition: background .15s; }
 .toggle .sw::after { content: ""; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; border-radius: 50%; background: var(--text); transition: left .15s; }
 .toggle input:checked + .sw { background: var(--lead); }
 .toggle input:checked + .sw::after { left: 21px; background: #0b0b0b; }
 .toggle input:focus-visible + .sw { outline: 2px solid var(--lead); outline-offset: 2px; }
 .toggle b { display: block; font-weight: 500; }
 .toggle small { color: var(--dim); font-size: 13px; }
 #go { align-self: center; min-width: 170px; min-height: 96px; border: 0; border-radius: 8px; background: var(--lead);
       color: var(--ink-on-lead); font: 700 19px var(--sans); display: flex; flex-direction: column; align-items: center;
       justify-content: center; gap: 8px; padding: 12px 18px; box-shadow: 0 6px 26px color-mix(in srgb, var(--lead) 30%, transparent); }
 #go svg.ic { width: 34px; height: 34px; }
 #go:hover:not(:disabled) { filter: brightness(1.08); }
 #go:disabled { opacity: .55; cursor: progress; }

 /* toolbar: library, breaks, saved, famous, reference */
 .tools { grid-column: 1 / -1; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr));
          background: var(--panel) var(--grain); border: 1px solid var(--line); border-radius: 10px; }
 .tool { position: relative; min-width: 0; }
 .tool + .tool { border-left: 1px solid var(--line); }
 .tool > summary { list-style: none; display: flex; align-items: center; justify-content: center; gap: 12px;
                   padding: 13px 10px; cursor: pointer; font-size: 15px; color: var(--text); border-radius: 10px; }
 .tool > summary::-webkit-details-marker { display: none; }
 .tool > summary:hover { background: #ffffff07; }
 .tool > summary svg.ic { width: 26px; height: 26px; color: var(--u2); }
 .tool:nth-child(2n) > summary svg.ic { color: var(--u1); }
 .tool[open] > summary { background: #ffffff0a; }
 .tool.set > summary::after { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--lead); }
 .tpop { position: absolute; z-index: 30; top: calc(100% + 6px); left: 0; width: max(100%, 340px); background: var(--panel2);
         border: 1px solid var(--line2); border-radius: 10px; padding: 14px; box-shadow: 0 18px 44px #000b;
         display: flex; flex-direction: column; gap: 10px; }
 .tool:nth-last-child(-n+2) .tpop { left: auto; right: 0; }
 .tpop .note { color: var(--dimmer); font-size: 12px; }
 .tpop .row { display: flex; gap: 8px; align-items: end; flex-wrap: wrap; }
 .tpop .row .fld { flex: 1 1 140px; }
 .btn { background: var(--panel2); border: 1px solid var(--line2); border-radius: 7px; padding: 8px 14px;
        display: inline-flex; align-items: center; gap: 8px; color: var(--text); }
 .btn:hover:not(:disabled) { border-color: var(--dim); }
 .btn.lead { background: var(--lead); color: var(--ink-on-lead); border-color: var(--lead); font-weight: 600; }
 .btn:disabled { opacity: .45; cursor: default; }
 #refdrop { border: 1.5px dashed var(--line2); border-radius: 8px; padding: 12px; display: flex; gap: 12px;
            align-items: center; cursor: pointer; color: var(--text); }
 #refdrop.over, #refdrop:hover { border-color: var(--lead); }
 #refdrop.busy { cursor: progress; color: var(--dim); }
 #refdrop small { display: block; color: var(--dimmer); font-size: 12px; }
 #refline button { margin-left: 6px; background: var(--well); border: 1px solid var(--line2); border-radius: 5px; padding: 1px 7px; color: var(--text); }
 #pullmsg { color: var(--bad); font-size: 12.5px; }

 /* busy banner */
 #work { grid-column: 1 / -1; display: none; background: var(--panel); border: 1px solid var(--line);
         border-left: 3px solid var(--lead); border-radius: 8px; padding: 10px 14px; }
 #work.on { display: block; }
 #work.bad { border-left-color: var(--bad); }
 #work.bad #worktext { color: var(--bad); }
 #workbar { height: 3px; background: var(--line); border-radius: 2px; overflow: hidden; margin-bottom: 8px; }
 #workbar i { display: block; height: 100%; width: 35%; background: var(--lead); animation: slide 1.4s ease-in-out infinite; }
 #work.bad #workbar { display: none; }
 @keyframes slide { from { transform: translateX(-100%); } to { transform: translateX(300%); } }

 /* ------------------------------------------------ beat list */
 .lower { grid-column: 1 / -1; display: grid; grid-template-columns: minmax(0, 1.95fr) minmax(280px, 1fr); gap: 14px; align-items: start; }
 #tracklist { display: flex; flex-direction: column; gap: 10px; }
 #tracklist.loading::before { content: "Cooking\2026"; display: block; padding: 22px; border: 1px dashed var(--line2);
   border-radius: var(--r); color: var(--dim); animation: pulse 1.4s ease-in-out infinite; }
 @keyframes pulse { 50% { opacity: .45; } }
 .track { background: var(--panel) var(--grain); border: 1px solid var(--line); border-radius: var(--r); padding: 12px 14px;
          cursor: default; transition: border-color .15s; }
 .track:hover { border-color: var(--line2); }
 .track.sel { border: 2px solid var(--lead); padding: 11px 13px; box-shadow: 0 0 0 4px color-mix(in srgb, var(--lead) 10%, transparent); }
 .track.loc-trash { opacity: .62; }
 .thead { display: grid; grid-template-columns: 76px minmax(0, 1fr); gap: 14px; align-items: center; }
 .art { width: 76px; height: 76px; border-radius: 6px; display: grid; place-items: center; position: relative; overflow: hidden;
        background: radial-gradient(circle at 30% 30%, var(--ac) 0 18%, transparent 19%),
                    radial-gradient(circle at 70% 64%, color-mix(in srgb, var(--ac) 70%, #000) 0 24%, transparent 25%),
                    radial-gradient(circle at 62% 26%, #ece6d633 0 10%, transparent 11%), #15161a;
        border: 1px solid var(--line2); }
 .art b { font: 600 18px var(--serif); color: var(--text); text-shadow: 0 1px 6px #000; }
 .c0 { --ac: var(--c0); } .c1 { --ac: var(--c1); } .c2 { --ac: var(--c2); } .c3 { --ac: var(--c3); }
 .tmain { min-width: 0; display: flex; flex-direction: column; gap: 3px; }
 .trow1 { display: flex; align-items: flex-start; gap: 10px; }
 .tmeta { flex: 1; min-width: 0; }
 .tname { display: block; font-size: 19px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 .tsub { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 2px; }
 .tag { font-size: 11.5px; letter-spacing: .04em; text-transform: uppercase; padding: 1px 8px; border-radius: 4px;
        background: color-mix(in srgb, var(--u2) 18%, transparent); color: color-mix(in srgb, var(--u2) 55%, #fff); }
 .tag:empty { display: none; }
 .tag.tloc { background: color-mix(in srgb, var(--u1) 20%, transparent); color: color-mix(in srgb, var(--u1) 55%, #fff); }
 .tmetaline { color: var(--dim); font-size: 13.5px; }
 .acts { display: flex; align-items: center; gap: 4px; flex: none; }
 .acts > button { display: inline-flex; align-items: center; gap: 7px; background: none; border: 1px solid transparent;
                  border-radius: 7px; padding: 4px 8px; color: var(--text); }
 .acts > button:hover { border-color: var(--line2); }
 .acts svg.ic { width: 26px; height: 26px; stroke-width: 1.5; }
 .acts .pass.on-fav { color: var(--green); border-color: color-mix(in srgb, var(--green) 50%, transparent); }
 .acts .fail.on-trash { color: var(--bad); border-color: color-mix(in srgb, var(--bad) 50%, transparent); }
 .more { position: relative; }
 .morebtn { background: none; border: 0; font-size: 20px; letter-spacing: 1px; padding: 2px 8px; color: var(--text); }
 .menu { display: none; position: absolute; right: 0; top: 100%; z-index: 20; background: var(--panel2);
         border: 1px solid var(--line2); border-radius: 8px; padding: 6px; min-width: 220px; box-shadow: 0 10px 30px #000a; }
 .more.open .menu { display: block; }
 .menu button { display: block; width: 100%; text-align: left; background: none; border: 0; padding: 8px 10px; border-radius: 5px; color: var(--text); }
 .menu button:hover { background: #ffffff0d; }
 .player .bar { display: block; position: relative; height: 34px; cursor: pointer; }
 .player .bar canvas { width: 100%; height: 100%; display: block; }
 .player .bar i { position: absolute; left: 0; bottom: 0; height: 2px; background: var(--wave); width: 0; }
 .player .bar.has-wave i { display: none; }
 .trow3 { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-top: 2px; }
 .pp { width: 40px; height: 40px; border-radius: 50%; border: 2px solid var(--text); background: none; flex: none;
       display: grid; place-items: center; font-size: 13px; color: var(--text); }
 .pp.on { border-color: var(--lead); color: var(--lead); }
 .stembtn { display: inline-flex; align-items: center; gap: 9px; background: var(--panel2); border: 1px solid var(--line2);
            border-radius: 7px; padding: 7px 18px; color: var(--text); font-size: 13.5px; }
 .stembtn:hover:not(:disabled) { border-color: var(--dim); }
 .stembtn.open { border-color: var(--lead); color: var(--lead); }
 .stembtn:disabled { opacity: .4; cursor: default; }
 .time { margin-left: auto; color: var(--dim); font: 13px var(--mono); }
 .theory { display: none !important; }

 /* the stem rack, inside a beat card */
 .rack { display: none; border-top: 1px solid var(--line); margin-top: 12px; padding-top: 6px; }
 .rack.open { display: block; }
 .lane { display: grid; grid-template-columns: 110px minmax(0, 1fr) auto auto auto; gap: 12px; align-items: center;
         padding: 8px 4px; border-bottom: 1px solid var(--line); border-radius: 6px; }
 .lane.flash { background: color-mix(in srgb, var(--lead) 14%, transparent); }
 .lane .who2 { display: flex; align-items: center; gap: 8px; }
 .lane .swatch { width: 3px; height: 18px; border-radius: 2px; background: var(--line2); }
 .lane.changed .swatch, .lane.trimmed .swatch { background: var(--lead); }
 .lane.locked .swatch { background: var(--dimmer); }
 .lane .lname { font-weight: 600; font-size: 12.5px; letter-spacing: .05em; }
 .lane .what { min-width: 0; }
 .lane .sample { display: block; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 .lane .pack { display: block; font-size: 11.5px; color: var(--dimmer); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 .lane.changed .sample { color: var(--lead); }
 .lane .picks { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; justify-content: flex-end; }
 .lane select { padding: 5px 26px 5px 8px; font-size: 12.5px; max-width: 220px; }
 .lane select:not(.snd) { max-width: 140px; }
 .lane.changed select { border-color: var(--lead); }
 .lane .mini { font-size: 13px; line-height: 1; padding: 7px 8px; background: var(--well); border: 1px solid var(--line2);
               border-radius: 6px; color: var(--text); }
 .lane .mini:hover { border-color: var(--dim); }
 .lane .mini.playing { border-color: var(--lead); color: var(--lead); }
 .lane .lock { font-size: 11.5px; color: var(--dimmer); font-style: italic; }
 .lane .vol { display: flex; align-items: center; gap: 3px; }
 .lane .vol .knob { width: 38px; height: 38px; cursor: ns-resize; touch-action: none; border-radius: 50%; }
 .lane .vol .knob svg { width: 100%; height: 100%; display: block; }
 .lane .vol .ktrack { fill: none; stroke: var(--line2); stroke-width: 9; stroke-linecap: round; }
 .lane .vol .klit { fill: none; stroke: var(--lead); stroke-width: 10; stroke-linecap: round; }
 .lane .vol.pan .klit { stroke: var(--u2); }
 .lane .vol .kcap { fill: var(--panel2); stroke: var(--line2); stroke-width: 3; }
 .lane .vol .kptr rect { fill: var(--text); }
 .lane .vol .knob:hover .kcap { stroke: var(--dim); }
 .lane .vol .db { font: 12px var(--mono); min-width: 34px; text-align: left; color: var(--dim); cursor: pointer; }
 .lane.trimmed .vol .db { color: var(--lead); }
 /* stem rack: each lane wears its Elements tile colour (same order) */
 .lane.c0 { --ac: var(--orange); } .lane.c1 { --ac: var(--green); } .lane.c2 { --ac: var(--violet); } .lane.c3 { --ac: var(--blue); }
 .lane .swatch { background: var(--ac); width: 4px; height: 26px; }
 .lane .lname { color: var(--ac); }
 .lane .vol:not(.pan) .klit { stroke: var(--ac); }
 .lane { border-left: 2px solid color-mix(in srgb, var(--ac) 35%, transparent); padding-left: 10px; }
 .lane:hover { background: color-mix(in srgb, var(--ac) 6%, transparent); }
 .lane.changed .sample, .lane.trimmed .vol .db { color: var(--ac); }
 .lane.changed select { border-color: var(--ac); }
 .lane.locked .swatch { background: var(--dimmer); }
 .lane.dropped .who2, .lane.dropped .what, .lane.dropped .vol { opacity: .3; text-decoration: line-through; }
 .banask { grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; font-size: 12.5px; color: var(--dim); }
 .banask span { flex: 1 1 220px; }
 .rackfoot { display: flex; align-items: center; gap: 10px; padding: 12px 0 2px; flex-wrap: wrap; }
 .rackfoot .staged { font-size: 12.5px; color: var(--dim); flex: 1 1 260px; }
 .rackfoot .staged b { color: var(--lead); font-weight: 600; }
 .rackfoot button { background: var(--panel2); border: 1px solid var(--line2); border-radius: 7px; padding: 7px 12px; color: var(--text); }
 .rackfoot button:hover:not(:disabled) { border-color: var(--dim); }
 .rackfoot button:disabled { opacity: .4; cursor: default; }
 .rackfoot .rebuild:not(.toeffects) { background: var(--lead); border-color: var(--lead); color: var(--ink-on-lead); font-weight: 600; }
 .rackmsg { font-size: 12.5px; color: var(--dim); }

 /* empty state */
 #empty { display: none; text-align: center; padding: 40px 20px; border: 1px dashed var(--line2); border-radius: var(--r); color: var(--dim); }
 #empty.err { border-color: var(--bad); color: var(--bad); }
 #empty .ghost img { width: 90px; opacity: .25; filter: grayscale(1); }
 #empty .scribble { display: block; font: 500 20px var(--serif); letter-spacing: .08em; color: var(--text); margin: 8px 0 4px; }

 /* ------------------------------------------------ elements table */
 .elements { position: sticky; top: 12px; max-height: calc(100vh - 110px); display: flex; flex-direction: column; padding: 14px; }
 .elements h2 { margin: 0 0 4px; font-size: 19px; }
 .elements h2 #elcount { color: var(--dim); font-weight: 400; }
 #elmeta { font-size: 12.5px; color: var(--dim); margin-bottom: 10px; }
 #elmeta .eltitle { color: var(--text); font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 #elmeta .tline { margin-top: 4px; color: var(--text); }
 #elmeta .tline i { color: var(--dimmer); font-style: normal; margin: 0 6px; }
 #elmeta .rom { font-family: var(--mono); font-size: 12px; }
 #elmeta .twhy { margin-top: 3px; color: var(--dimmer); }
 .tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr)); gap: 8px; overflow-y: auto;
          padding-right: 4px; min-height: 0; }
 .tile { aspect-ratio: 1 / 1.08; display: flex; flex-direction: column; align-items: center; justify-content: center;
         gap: 1px; padding: 6px 4px; position: relative; background: color-mix(in srgb, var(--ac) 7%, var(--well));
         border: 1.5px solid var(--ac); border-radius: 6px; color: var(--text); min-width: 0; }
 .tile:hover { background: color-mix(in srgb, var(--ac) 16%, var(--well)); }
 .tile.locked { border-style: dashed; }
 .tile .tn { position: absolute; top: 4px; left: 7px; font: 600 11.5px var(--sans); color: var(--ac); }
 .tile .tc { font: 700 30px/1 var(--sans); color: var(--ac); letter-spacing: -.01em; }
 .tile .tl { font-size: 12.5px; max-width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 .tile .ts { font-size: 10.5px; color: var(--dimmer); max-width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

 /* ------------------------------------------------ now playing */
 .nowbar { position: fixed; left: 0; right: 0; bottom: 0; height: 76px; z-index: 50; background: #0a0b0d;
           border-top: 1px solid var(--line); display: grid; grid-template-columns: minmax(180px, 260px) minmax(0, 1fr) auto auto;
           align-items: center; gap: 22px; padding: 0 18px; }
 .nowbar .nhead { display: flex; align-items: center; gap: 12px; min-width: 0; }
 .nowbar .art { width: 54px; height: 54px; }
 .nowbar .art b { font-size: 13px; }
 .nowbar .ntitle { min-width: 0; }
 .nowbar .ntitle b { display: block; font-weight: 500; font-size: 15px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
 .nowbar .ntitle small { color: var(--dim); font-size: 12.5px; }
 .nprog { display: flex; align-items: center; gap: 12px; min-width: 0; }
 .ntrack { flex: 1; height: 6px; background: var(--line2); border-radius: 3px; overflow: hidden; }
 .ntrack i { display: block; height: 100%; width: 0; background: var(--lead); border-radius: 3px; }
 #ntime { font: 12.5px var(--mono); color: var(--dim); white-space: nowrap; }
 .nctl { display: flex; align-items: center; gap: 14px; }
 .nctl button { background: none; border: 0; color: var(--text); padding: 4px; display: grid; place-items: center; }
 .nctl svg.ic { width: 24px; height: 24px; }
 .nctl #npp { width: 54px; height: 54px; border-radius: 50%; border: 2px solid var(--text); font-size: 16px; }
 .nctl #npp.on { border-color: var(--lead); color: var(--lead); }
 .nqueue { display: flex; gap: 8px; max-width: 30vw; overflow-x: auto; }
 .nqueue button { padding: 0; border: 2px solid transparent; border-radius: 7px; background: none; }
 .nqueue button.now { border-color: var(--lead); }
 .nqueue .art { width: 42px; height: 42px; }
 .nqueue .art b { font-size: 11px; }

 #toast { position: fixed; left: 50%; bottom: 92px; transform: translateX(-50%); z-index: 60; background: var(--panel2);
          border: 1px solid var(--line2); border-radius: 8px; padding: 10px 14px; display: flex; gap: 14px; align-items: center;
          box-shadow: 0 10px 30px #000a; }
 #toast button { background: var(--lead); color: var(--ink-on-lead); border: 0; border-radius: 6px; padding: 5px 12px; font-weight: 600; }

 /* ------------------------------------------------ narrower windows */
 @media (max-width: 1240px) {
   .board { grid-template-columns: 1fr; }
   .params { grid-template-columns: minmax(0, 1fr) auto; }
   #go { grid-column: 1 / -1; min-height: 60px; flex-direction: row; }
 }
 @media (max-width: 900px) {
   body { grid-template-columns: 1fr; }
   .side { position: static; height: auto; flex-direction: row; justify-content: center; padding: 6px; }
   .side .logo { padding: 0 10px; }
   .lower { grid-template-columns: 1fr; }
   .elements { position: static; max-height: none; }
   .tools { grid-template-columns: repeat(2, minmax(0, 1fr)); }
   .tool + .tool { border-left: 0; }
   .params { grid-template-columns: 1fr; }
   .tempo { border-left: 0; padding-left: 0; }
   .lane { grid-template-columns: 1fr; }
   .nowbar { grid-template-columns: minmax(0, 1fr) auto; }
   .nprog, .nqueue { display: none; }
   .word .hr { font-size: 28px; }
 }
</style></head><body>
<nav class="side" aria-label="Main">
  <a class="logo" href="/" aria-label="Homeroom Studios">
    <svg viewBox="0 0 46 54" aria-hidden="true"><path d="M23 2 L43 8 V28 C43 40 34 48 23 52 C12 48 3 40 3 28 V8 Z" fill="none" stroke="currentColor" stroke-width="2"/>
      <text x="23" y="24" text-anchor="middle" font-family="Cinzel, Georgia, serif" font-size="13" fill="currentColor">H</text>
      <line x1="13" y1="28.5" x2="33" y2="28.5" stroke="currentColor" stroke-width="1"/>
      <text x="23" y="42" text-anchor="middle" font-family="Cinzel, Georgia, serif" font-size="13" fill="currentColor">S</text></svg></a>
  <a class="here" href="/" aria-current="page">
    <svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7 15h10"/></svg>Beat Making</a>
  <button type="button" id="side-saved">
    <svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5A1.5 1.5 0 0 1 4.5 5H9l2 2.5h8.5A1.5 1.5 0 0 1 21 9v9.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"/></svg>My Beats</button>
  <a href="http://localhost:8765" title="The studio half: recipes, patches, Reason. Same launcher starts it.">
    <svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5.5C5.5 4 9 4 12 6c3-2 6.5-2 9-.5V19c-2.5-1.5-6-1.5-9 .5-3-2-6.5-2-9-.5z"/><path d="M12 6v13.5"/></svg>Get Schooled</a>
</nav>

<div class="main">
<header class="mast"><div class="word" aria-label="Homeroom Studios"><span class="hr">HOMEROOM</span><span class="st">STUDIOS</span></div></header>

<div class="board">
  <section class="panel cls" aria-labelledby="h-class">
    <h2 id="h-class"><span class="num">1</span>Choose your class</h2>
    <div class="tabs" role="tablist">
      <button type="button" role="tab" id="tab-crew" data-tab="crew" aria-selected="true">The Back of the Class</button>
      <button type="button" role="tab" id="tab-legends" data-tab="legends" aria-selected="false">The Legends</button>
    </div>
    <div class="roster" data-kind="crew" role="tabpanel" aria-labelledby="tab-crew"><div class="djs">__CREW__</div></div>
    <div class="roster" data-kind="legends" role="tabpanel" aria-labelledby="tab-legends" hidden><div class="djs">__LEGENDS__</div></div>
    <p class="popnote">Pick one for a solo beat. Pick more for a collab &mdash; it lands in the folder of whoever you pick
      <b>first</b>. Ask for four or more and a quarter come back as straight, traditional hip hop.</p>
    <span id="hosthint" role="status"></span>
  </section>

  <section class="panel params" aria-labelledby="h-params">
    <h2 id="h-params"><span class="num">2</span>Set your parameters</h2>
    <div class="pgrid">
      <div class="fld"><label for="key">Key</label>
        <select id="key"><option value="">any key</option>__KEYOPTS__</select></div>
      <div class="fld cnt"><label for="count">Number of beats</label>
        <div class="spin"><input type="number" id="count" value="1" min="1" max="10" title="1 to 10">
          <span class="arrows"><button type="button" data-for="count" data-d="1" aria-label="One more beat">&#9650;</button><button type="button" data-for="count" data-d="-1" aria-label="One fewer beat">&#9660;</button></span></div>
        <small>1&ndash;10 beats</small></div>
      <div class="fld pick" data-kind="styles">
        <span class="lbl" id="lbl-styles">Style</span>
        <div class="picker" role="button" tabindex="0" aria-haspopup="true" aria-expanded="false" aria-labelledby="lbl-styles">
          <span class="chips"><span class="ph">Any &mdash; pick subgenres, played by the rules</span></span>
          <span class="chev" aria-hidden="true"></span></div>
        <div class="pop"><div class="djs">__GENRES__</div></div>
      </div>
      <!-- Directions + Famous beats feed the SAME hidden notes text the old
           Directions box held (syncNotes), so parsing is unchanged. -->
      <input type="hidden" id="notes" value="">
      <div class="fld wide"><label for="quick">Directions</label>
        <select id="quick">
          <option value="">e.g. dark, melodic, aggressive&hellip;</option>
          <option value="no chords">no chords &mdash; drums only, old style</option>
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
        </select></div>
    </div>

    <div class="tempo">
      <svg class="flask auto" viewBox="0 0 120 160" aria-hidden="true">
        <defs><clipPath id="flaskclip"><path d="M47 10H73V54L107 136Q112 152 98 152H22Q8 152 13 136L47 54Z"/></clipPath></defs>
        <g clip-path="url(#flaskclip)"><rect class="liq" x="0" y="152" width="120" height="0"/>
          <rect class="shine" x="22" y="0" width="6" height="160"/></g>
        <g id="fticks"></g>
        <path class="glass" d="M47 10H73V54L107 136Q112 152 98 152H22Q8 152 13 136L47 54Z"/>
        <path class="glass" d="M42 10H78"/>
      </svg>
      <div class="bpmbox">
        <div class="spin tspin">
          <input type="text" id="tempo" inputmode="numeric" placeholder="auto" aria-label="Tempo in BPM"
                 title="Leave blank to use the DJ's home tempo">
          <span class="unit">BPM</span>
          <span class="pm"><button type="button" data-for="tempo" data-d="-1" aria-label="Tempo down">&minus;</button><button type="button" data-for="tempo" data-d="1" aria-label="Tempo up">+</button></span>
        </div>
        <label class="toggle" title="Build the whole beat from loop material instead of one-shots">
          <input type="checkbox" id="loopsonly"><span class="sw"></span>
          <span><b>Loops only</b><small id="modeword">Beat mode</small></span></label>
      </div>
    </div>

    <button type="button" id="go" aria-label="Generate beats">
      <svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M12 13v5M9.5 15.5h5"/></svg>
      <span id="goword">Generate Beats</span></button>
  </section>

  <nav class="tools" aria-label="Library, saved beats and reference">
    <details class="tool">
      <summary><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/></svg>Pattern Library</summary>
      <div class="tpop"><p class="note">Every transcribed groove, by genre &mdash; drums only, no chords or bass.</p>
        <div class="row">
          <div class="fld"><label for="libgenre">Genre</label><select id="libgenre">__LIBGENRES__</select></div>
          <div class="fld"><label for="libpattern">Pattern</label><select id="libpattern"></select></div>
          <button type="button" class="btn lead" id="libgo">Play it</button></div>
        <p class="note">Renders on its own and lands in the beat list &mdash; play it again for a new kit on the same rhythm.</p></div>
    </details>
    <details class="tool">
      <summary><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12h4l2.5-6 4 13 3-9 1.5 2H22"/></svg>Breaks</summary>
      <div class="tpop"><p class="note">Famous figures and funk breaks &mdash; kept separate, played verbatim.</p>
        <div class="row">
          <div class="fld"><label for="libbreak">Break</label><select id="libbreak">__LIBBREAKS__</select></div>
          <button type="button" class="btn lead" id="libbreakgo">Play it</button></div>
        <p class="note">Saved to its own Breaks folder, never mixed into a genre.</p></div>
    </details>
    <details class="tool" id="savedtool">
      <summary><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6.5A1.5 1.5 0 0 1 4.5 5H9l2 2.5h8.5A1.5 1.5 0 0 1 21 9v9.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"/></svg>Saved Beats</summary>
      <div class="tpop">
        <div class="fld"><label for="viewsrc">Show in the list</label>
          <select id="viewsrc">
            <option value="batch">This batch</option>
            <option value="favorites">Passed (Favorites)</option>
            <option value="dj">DJ folder</option>
            <option value="trash">Failed (Trash &mdash; get one back)</option>
          </select></div>
        <div class="row">
          <div class="fld"><label for="pullno">Beat number</label><input type="number" id="pullno" min="1" placeholder="316"></div>
          <button type="button" class="btn lead" id="pullgo">Open it</button></div>
        <p class="note">Puts an older beat in the list so you can play it, open its stems and swap sounds. (Beats made from July&nbsp;16 on.)</p>
        <div id="pullmsg" role="status"></div></div>
    </details>
    <details class="tool" id="famoustool">
      <summary><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4-4.7-4.4 6.4-.8z"/></svg>Famous Beats</summary>
      <div class="tpop">
        <div class="fld"><label for="famous">Build on a famous drum break</label>
          <select id="famous">
            <option value="">none</option>
            <option value="break">surprise me &mdash; any of them</option>
__BREAKS__
          </select></div>
        <p class="note">Goes in with your next Generate. A dot on this button means one is picked.</p></div>
    </details>
    <details class="tool">
      <summary><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 11.5l-8.2 8.2a5 5 0 0 1-7.1-7.1l8.6-8.6a3.4 3.4 0 0 1 4.8 4.8l-8.4 8.4a1.7 1.7 0 0 1-2.4-2.4l7.7-7.7"/></svg>Reference</summary>
      <div class="tpop">
        <span class="lbl" id="lbl-ref">Match a song&rsquo;s tempo and key</span>
        <div id="refdrop" role="button" tabindex="0" aria-labelledby="lbl-ref refdrop-hint">
          <svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V4M7.5 8.5L12 4l4.5 4.5M5 14v5h14v-5"/></svg>
          <span>Drop a track here or click to upload
            <small id="refdrop-hint">MP3, WAV, M4A, AIFF, FLAC (max 300 MB)</small></span></div>
        <input type="file" id="reffile" accept=".mp3,.wav,.m4a,.aif,.aiff,.flac,audio/*" hidden>
        <div class="hint" id="refline" role="status">nothing dropped yet</div></div>
    </details>
  </nav>

  <div id="work" role="status"><div id="workbar"><i></i></div><div id="worktext"></div></div>

  <div class="lower">
    <section aria-label="Beats">
      <div id="tracklist"></div>
      <div id="empty"><div class="ghost"><img src="/brand?name=logo-chalk.png" alt=""
           onerror="this.style.display='none'"></div><span class="scribble">Nothing cooking yet</span>
        <p id="emptytext">Make a beat and it lands here &mdash; with every drum in it.</p></div>
    </section>
    <aside class="panel elements" aria-labelledby="h-el">
      <h2 id="h-el">Elements <span id="elcount"></span></h2>
      <div id="elmeta"><span class="hint">Pick a beat to see what&rsquo;s in it.</span></div>
      <div class="tiles" id="eltiles"></div>
    </aside>
  </div>
</div>
</div>

<footer class="nowbar" aria-label="Now playing">
  <span class="nhead"><span class="art c0" id="nart" aria-hidden="true"><b></b></span>
    <span class="ntitle"><b id="ntitle">Nothing playing</b><small id="nsub"></small></span></span>
  <span class="nprog"><span class="ntrack"><i id="nfill"></i></span><span id="ntime">0:00 / 0:00</span></span>
  <span class="nctl">
    <button type="button" id="nprev" aria-label="Previous beat"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5v14M19 5l-10 7 10 7z"/></svg></button>
    <button type="button" id="npp" aria-label="Play">&#9654;</button>
    <button type="button" id="nnext" aria-label="Next beat"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M18 5v14M5 5l10 7-10 7z"/></svg></button>
  </span>
  <span class="nqueue" id="nqueue" aria-label="Beats in the list"></span>
</footer>
<div id="toast" role="status" aria-live="polite" hidden></div>
<script>
 // The Directions typing box is gone. Quick directions and Famous beats
 // still make the SAME notes text (a hidden field), so parse_directions and
 // the README trail are unchanged whether he picks or, in future, types.
 const notesBox = document.getElementById('notes');
 function syncNotes() {
   notesBox.value = [document.getElementById('famous').value,
                     document.getElementById('quick').value].filter(Boolean).join(', ');
   document.getElementById('famoustool').classList.toggle('set',
     !!document.getElementById('famous').value);
 }
 ['quick', 'famous'].forEach(id =>
   document.getElementById(id).addEventListener('change', syncNotes));

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
   // each dropdown shows its own picks as chips, numbered in pick order
   document.querySelectorAll('.pick').forEach(pk => {
     const mine = [...pk.querySelectorAll('.dj input')].map(cb => cb.value);
     const picked = order.filter(n => mine.includes(n));
     pk.querySelector('.chips').innerHTML = picked.length
       ? picked.map(n => '<span class="chip"><b>' + (order.indexOf(n) + 1) +
           '</b>' + esc(n) + '<span class="x" role="button" tabindex="0" ' +
           'aria-label="Remove ' + esc(n) + '" data-name="' + esc(n) +
           '">&times;</span></span>').join('')
       : '<span class="ph">' + pk.dataset.ph + '</span>';
   });
 }
 // the dropdowns: open one at a time; the tick boxes inside are the same
 // .dj cards as before, so picking, pick order and the folder rule are
 // untouched (owner 2026-10-03: dropdowns, but keep picking several)
 function closePicks() {
   document.querySelectorAll('.pick.open').forEach(o => {
     o.classList.remove('open');
     o.querySelector('.picker').setAttribute('aria-expanded', 'false');
   });
 }
 document.querySelectorAll('.pick').forEach(pk => {
   pk.dataset.ph = pk.querySelector('.ph').innerHTML;
   const btn = pk.querySelector('.picker');
   const toggle = () => {
     const open = !pk.classList.contains('open');
     closePicks();
     pk.classList.toggle('open', open);
     btn.setAttribute('aria-expanded', open);
   };
   btn.addEventListener('click', e => {
     const x = e.target.closest('.x');
     if (x) {                                  // a chip's ×: untick it
       const cb = [...pk.querySelectorAll('.dj input')]
                    .find(c => c.value === x.dataset.name);
       if (cb) { cb.checked = false; cb.dispatchEvent(new Event('change')); }
       return;
     }
     toggle();
   });
   btn.addEventListener('keydown', e => {
     if (e.key !== 'Enter' && e.key !== ' ') return;
     e.preventDefault();
     const x = e.target.closest('.x');
     if (x) x.click(); else toggle();
   });
 });
 document.addEventListener('click', e => {
   if (!e.target.closest('.pick')) closePicks();
   if (!e.target.closest('details.tool'))
     document.querySelectorAll('details.tool[open]').forEach(d => d.open = false);
   if (!e.target.closest('.more'))
     document.querySelectorAll('.more.open').forEach(m => m.classList.remove('open'));
 });
 document.addEventListener('keydown', e => {
   if (e.key !== 'Escape') return;
   closePicks();
   document.querySelectorAll('details.tool[open]').forEach(d => d.open = false);
   document.querySelectorAll('.more.open').forEach(m => m.classList.remove('open'));
 });
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

 // A beat repeats until you press stop (owner 2026-08-31), and with NO
 // gap at the seam (owner 2026-10-03). <audio loop> hiccups every time it
 // wraps; the Sound Engine page loops a decoded buffer in Web Audio and
 // is seamless, so the beat cards do the same. Same surface as <audio>
 // (src/load/play/pause/currentTime/duration + events) so the transport
 // code around it didn't change.
 const actx = new (window.AudioContext || window.webkitAudioContext)();
 class LoopAudio extends EventTarget {
   constructor(src) {
     super(); this.src = src; this.dataset = {}; this.buf = null;
     this.node = null; this.paused = true; this.readyState = 0;
     this._off = 0; this._t0 = 0; this._gen = 0; this._loading = false;
     this._tick = null; LoopAudio.all.push(this);
   }
   get duration() { return this.buf ? this.buf.duration : NaN; }
   get currentTime() {
     if (!this.buf) return 0;
     if (this.paused) return this._off;
     return (actx.currentTime - this._t0) % this.buf.duration;
   }
   set currentTime(t) {
     this._off = t;
     if (!this.paused) { this._kill(); this._start(); }
   }
   _fire(n) { this.dispatchEvent(new Event(n)); }
   load() {
     const gen = ++this._gen;
     this._kill(); clearInterval(this._tick); this.paused = true; this.buf = null;
     this.readyState = 0; this._off = 0; this._loading = true;
     const get = u => fetch(u)
       .then(r => { if (!r.ok) throw new Error(r.status); return r.arrayBuffer(); })
       .then(b => actx.decodeAudioData(b));
     const lanes = this.src.startsWith('stems:') ? (stemLanes[this.no] || []) : null;
     this.layers = null;
     (lanes ? Promise.all(lanes.map(s => get('/stem?no=' + this.no + '&lane=' +
                encodeURIComponent(s.lane) + '&db=0')
                .then(buf => [s.lane, { buf, pan0: s.pan || 0 }])))
              .then(list => {
                this.layers = Object.fromEntries(list);
                return list.reduce((a, [, L]) => !a || L.buf.duration > a.duration ? L.buf : a, null);
              })
            : get(this.src))
       .then(buf => {
         if (gen !== this._gen) return;          // a newer load won
         this.buf = buf; this.readyState = 4; this._loading = false;
         this._fire('loadedmetadata'); this._fire('canplay');
       })
       .catch(() => {
         if (gen !== this._gen) return;
         this._loading = false; this._fire('error');
       });
   }
   async play() {
     this._want = true;
     await actx.resume();
     if (!this.buf) {
       if (!this._loading) this.load();
       await new Promise((ok, no) => {
         this.addEventListener('canplay', ok, { once: true });
         this.addEventListener('error', no, { once: true });
       });
     }
     if (!this.paused || !this._want) return;   // paused while it loaded
     this.paused = false; this._start(); this._fire('play');
     this._tick = setInterval(() => this._fire('timeupdate'), 200);
   }
   pause() {
     this._want = false;
     if (this.paused) return;
     this._off = this.currentTime; this._kill(); clearInterval(this._tick);
     this.paused = true; this._fire('pause');
   }
   _start() {
     if (this.layers) return this._startLayers();
     const n = actx.createBufferSource();
     n.buffer = this.buf; n.loop = true;
     // a gain stage so a stem's knob moves the sound while it plays
     // (owner 2026-10-10); at 0 dB it is a straight wire
     const g = actx.createGain(); this.gainNode = g;
     const pn = actx.createStereoPanner(); this.panNode = pn;
     n.connect(g); g.connect(pn); pn.connect(actx.destination);
     this.setGain(this.db || 0); this.setPan(this.panv || 0);
     const off = (this._off || 0) % this.buf.duration;
     n.start(0, off); this._t0 = actx.currentTime - off; this.node = n;
   }
   // Stem mode (owner 2026-10-15): every lane plays as its own looping
   // source with its own gain + pan, so the rack knobs are heard live
   // while Play runs. Close to the printed beat, not exact: no master
   // chain or kick ducking. Rebuild / Add chunk print the exact one.
   // ponytail: relative pan on a stereo stem, not a true re-pan.
   _startLayers() {
     const g = actx.createGain(); this.gainNode = g; g.connect(actx.destination);
     const off = (this._off || 0) % this.buf.duration;
     const t = actx.currentTime + 0.05;
     this.nodes = [];
     for (const [lane, L] of Object.entries(this.layers)) {
       if (!L.buf) continue;
       const n = actx.createBufferSource(); n.buffer = L.buf; n.loop = true;
       L.g = actx.createGain(); L.p = actx.createStereoPanner();
       n.connect(L.g); L.g.connect(L.p); L.p.connect(g);
       n.start(t, off % L.buf.duration); this.nodes.push(n);
     }
     this._t0 = t - off; this.node = this.nodes[0] || null;
     this.setLayers();
   }
   // push every lane's current knob values into the live nodes
   setLayers() {
     if (!this.layers) return;
     for (const [lane, L] of Object.entries(this.layers)) {
       if (!L.g) continue;
       const db = (trims[this.no] || {})[lane] || 0;
       const off = !!(drops[this.no] || {})[lane];
       L.g.gain.setTargetAtTime(off ? 0 : Math.pow(10, db / 20), actx.currentTime, 0.01);
       const want = ((pans[this.no] || {})[lane] ?? L.pan0) / 100;
       L.p.pan.setTargetAtTime(Math.max(-1, Math.min(1, want - L.pan0 / 100)),
                               actx.currentTime, 0.01);
     }
   }
   // -100..100 on the solo player (relative to where the stem sits)
   setPan(p) {
     this.panv = p;
     if (this.panNode) this.panNode.pan.setTargetAtTime(
       Math.max(-1, Math.min(1, p / 100)), actx.currentTime, 0.01);
   }
   _kill() {
     if (this.panNode) { this.panNode.disconnect(); this.panNode = null; }
     (this.nodes || []).forEach(n => { try { n.stop(); } catch (e) {} n.disconnect(); });
     if (this.nodes) { this.nodes = null; this.node = null; }
     if (this.node) { try { this.node.stop(); } catch (e) {} this.node.disconnect(); this.node = null; }
     if (this.gainNode) { this.gainNode.disconnect(); this.gainNode = null; }
   }
   // dB -> live gain. Never lets the boost clip: same 0.94 ceiling the
   // server's _solo applies when it renders a stem at a given dB.
   setGain(db) {
     this.db = db;
     if (!this.gainNode) return;
     if (this.peak == null && this.buf) {
       let p = 0;
       for (let c = 0; c < this.buf.numberOfChannels; c++) {
         const d = this.buf.getChannelData(c);
         for (let i = 0; i < d.length; i++) { const a = Math.abs(d[i]); if (a > p) p = a; }
       }
       this.peak = p;
     }
     let g = Math.pow(10, db / 20);
     if (this.peak && this.peak * g > 0.94) g = 0.94 / this.peak;
     this.gainNode.gain.setTargetAtTime(g, actx.currentTime, 0.01);
   }
 }
 LoopAudio.all = [];
 let auditionBtn = null;
 function play(url, btn) {
   if (auditionBtn) auditionBtn.classList.remove('playing');
   if (auditionBtn === btn && !audition.paused) {
     audition.pause(); auditionBtn = null; return;
   }
   LoopAudio.all.forEach(a => a.pause());
   audition.src = url; audition.play().catch(() => {});
   auditionBtn = btn || null;
   if (auditionBtn) auditionBtn.classList.add('playing');
 }
 audition.addEventListener('ended', () => {
   if (auditionBtn) auditionBtn.classList.remove('playing');
   auditionBtn = null;
 });

 // ------------------------------------------------------------ the batch
 const LOC = { favorites: 'Passed', trash: 'Failed \u00b7 in Trash', dj: '' };
 const staged = {};                    // beat no -> { lane: path | null }
 const trims = {};                     // beat no -> { lane: dB }
 const SOUND_ENGINE = 'http://localhost:8767';
 // &back= tells the Effects page where its "Send back" goes
 const engineLink = id => SOUND_ENGINE + '/?beat=' + encodeURIComponent(id) +
   '&back=' + encodeURIComponent(location.origin);
 const pans = {};                      // beat no -> { lane: -100..100 }
 const stemLanes = {};                 // beat no -> rack rows that have a stem
 // knob settings are kept per beat across visits (owner 2026-10-15)
 try {
   const m = JSON.parse(localStorage.getItem('bm-mix') || '{}');
   Object.assign(trims, m.trims || {}); Object.assign(pans, m.pans || {});
 } catch (e) {}
 function saveMix() {
   try { localStorage.setItem('bm-mix', JSON.stringify({ trims, pans })); } catch (e) {}
 }
 const drops = {};                     // beat no -> { lane: true }

 function setLoc(el, loc) {
   el.className = 'track loc-' + loc + (el === selEl ? ' sel' : '');
   el.dataset.loc = loc;
   el.querySelector('.tloc').innerHTML = LOC[loc] || '';
   el.querySelectorAll('.acts button[data-dest]').forEach(b => {
     const on = (loc === 'favorites' && b.dataset.dest === 'favorites') ||
                (loc === 'trash' && b.dataset.dest === 'trash');
     b.classList.toggle('on-fav', on && b.dataset.dest === 'favorites');
     b.classList.toggle('on-trash', on && b.dataset.dest === 'trash');
     if (b.classList.contains('star') || b.classList.contains('eraser'))
       b.setAttribute('aria-pressed', on);
   });
 }
 // Pass (star) and Fail (eraser) only ever MOVE the beat's files between
 // folders on the server - nothing is deleted - so a fail can be undone.
 let toastTimer;
 function toast(msg, undo) {
   const t = document.getElementById('toast');
   clearTimeout(toastTimer);
   t.textContent = '';
   const s = document.createElement('span'); s.textContent = msg; t.appendChild(s);
   if (undo) {
     const b = document.createElement('button');
     b.type = 'button'; b.textContent = 'Undo';
     b.onclick = () => { t.hidden = true; undo(); };
     t.appendChild(b);
   }
   t.hidden = false;
   toastTimer = setTimeout(() => { t.hidden = true; }, 9000);
 }
 async function triage(no, dest, el, was) {
   try {
     const r = await fetch('/triage', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ number: no, dest }) });
     const d = await r.json();
     if (!d.ok) throw new Error(d.error || 'the move failed');
     if (el) setLoc(el, d.loc);
     if (d.loc === 'trash')
       toast('Beat ' + no + ' moved to Trash (nothing is deleted).',
             () => triage(no, was && was !== 'trash' ? was : 'dj', el));
   } catch (e) {
     failed('Could not move beat ' + no + ': ' + (e.message || e));
   }
 }

 function prettyTitle(label) {          // "316 Doc Day Boulevard Protocol Drums 93bpm"
   const m = label.match(/^(\d+)\s+(.*?)\s+Drums\s+([\d.]+)bpm$/i);
   return m ? { no: m[1], rest: m[2], bpm: m[3] } : { no: '', rest: label, bpm: '' };
 }

 function makeTrack(b) {
   const t = prettyTitle(b.label);
   const el = document.createElement('div');
   el.className = 'track loc-' + b.loc;
   el.dataset.no = b.no; el.dataset.seId = b.se_id || '';
   el.au = new LoopAudio('/audio?no=' + b.no);
   const ICON = d => '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>';
   el.innerHTML =
     '<div class="thead">' +
       '<span class="art c' + (b.no % 4) + '" aria-hidden="true"><b>' + b.no + '</b></span>' +
       '<span class="tmain">' +
         '<span class="trow1"><span class="tmeta"><span class="tname"></span>' +
           '<span class="tsub"></span></span>' +
           // Pass = keep (Favorites), Fail = Trash (a move, never a delete);
           // a second click sends it back to its DJ folder. Same data-dest
           // buttons as before; "..." holds the rest.
           '<span class="acts">' +
             '<button class="star pass" title="Pass \u2014 save to Favorites" aria-label="Pass / Save to Favorites" aria-pressed="false" data-dest="favorites">' +
               ICON('<circle cx="12" cy="12" r="9.5"/><path d="M7.5 12.3l3 3 6-6.3"/>') + 'Pass</button>' +
             '<button class="eraser fail" title="Fail \u2014 move to Trash (you can get it back)" aria-label="Fail / Move to Trash" aria-pressed="false" data-dest="trash">' +
               ICON('<circle cx="12" cy="12" r="9.5"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7"/>') + 'Fail</button>' +
             '<span class="more"><button class="morebtn" title="More" aria-label="More" aria-haspopup="true">&middot;&middot;&middot;</button>' +
               '<span class="menu">' +
                 '<button title="Move it back to its DJ folder (also gets a beat out of Trash or Favorites)" data-dest="dj">Back to its DJ folder</button>' +
               '</span></span>' +
           '</span></span>' +
         '<span class="tmetaline"></span>' +
         '<span class="player"><span class="bar"><canvas></canvas><i></i></span></span>' +
         '<span class="trow3"><button class="pp" aria-label="Play">&#9654;</button>' +
           '<button class="stembtn" data-role="sketch" title="Make a whole song (2:30 to 4:00) from this beat">' +
             ICON('<path d="M6 3h8l4 4v14H6z"/><path d="M9 11h6M9 15h6"/>') + 'Sketch</button>' +
           '<button class="stembtn" data-role="stems">' +
             ICON('<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 12.5l9 5 9-5"/><path d="M3 16.5l9 5 9-5"/>') + 'Stems</button>' +
           '<button class="stembtn" data-role="engine"' + (b.se_id
             ? ' title="Open this beat on the Physics (Effects) page, in this tab">'
             : ' disabled title="This beat has no Effects copy. Open Stems, change something, then use Effects there.">') +
             ICON('<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>') + 'Open Physics</button>' +
           '<span class="time">0:00</span></span>' +
       '</span>' +
     '</div>' +
     '<div class="theory"></div>' +
     '<div class="rack"></div>';
   const th = b.theory;
   el.querySelector('.tname').textContent = t.rest || ('Beat ' + b.no);
   el.querySelector('.tsub').innerHTML =
     '<span class="tag">Beat ' + esc(String(b.no)) + '</span><span class="tag tloc"></span>';
   el.querySelector('.tmetaline').innerHTML =
     [th && th.key ? esc(th.key) : '', t.bpm ? t.bpm + ' BPM' : '', '<span class="dur"></span>']
       .filter(Boolean).join(' &nbsp;|&nbsp; ');
   // why this beat works — only for beats that recorded their harmony;
   // anything older just doesn't get the block (see _beat_theory)
   if (th && th.key) {
     const box = el.querySelector('.theory');
     const bits = ['<b>' + esc(th.key) + '</b>'];
     if (th.progression) bits.push(esc(th.progression));
     if (th.roman) bits.push('<span class="rom">' + esc(th.roman) + '</span>');
     if (th.chords) bits.push('<span class="rom">' + esc(th.chords) + '</span>');
     if (th.voices) bits.push(esc(th.voices));
     box.innerHTML = '<div class="tline">' + bits.join('<i>·</i>') + '</div>' +
       (th.why ? '<div class="twhy">' + esc(th.why) + '</div>' : '');
     box.style.display = 'block';
   }
   setLoc(el, b.loc);
   el.querySelectorAll('.acts button[data-dest]').forEach(btn =>
     btn.onclick = () => {
       const was = el.dataset.loc;
       let dest = btn.dataset.dest;
       // pressing a lit star / eraser again takes it back to the DJ folder
       if (dest === was && dest !== 'dj') dest = 'dj';
       triage(b.no, dest, el, was);
       el.querySelector('.more').classList.remove('open');
     });
   el.querySelector('.morebtn').onclick = () => {
     const m = el.querySelector('.more'), open = !m.classList.contains('open');
     document.querySelectorAll('.more.open').forEach(x => x.classList.remove('open'));
     m.classList.toggle('open', open);
   };
   // currentTarget, not target: the button holds an icon now, and a click
   // on the icon would otherwise get the "open" class instead of the button
   el.querySelector('[data-role=stems]').onclick = ev => toggleRack(el, b.no, ev.currentTarget);
   el.querySelector('[data-role=sketch]').onclick = () => window.openSketch && openSketch(b.no);
   // Open this beat in the Sound Engine with the DJ's effects already set
   // (sound_engine/fx_presets.py). It is a separate app on its own port, so
   // this is a plain link out — nothing is printed here and this beat's
   // files are not touched. If the Sound Engine isn't running the page
   // just fails to connect, which is why the button says to start it.
   const eng = el.querySelector('[data-role=engine]');
   if (eng && b.se_id) eng.onclick = () => openEffects(b.no, b.se_id);
   // clicking anywhere on a card (not inside its open rack) selects it, and
   // the Elements table beside the list follows the selection
   el.addEventListener('click', e => { if (!e.target.closest('.rack')) selectBeat(el); });
   wireTransport(el);
   return el;
 }

 function clock(s) {
   if (!isFinite(s)) return '0:00';
   const m = Math.floor(s / 60), r = Math.floor(s % 60);
   return m + ':' + String(r).padStart(2, '0');
 }

 function wireTransport(el) {
   const au = el.au, pp = el.querySelector('.pp'),
         bar = el.querySelector('.bar'), fill = bar.querySelector('i'),
         time = el.querySelector('.time');
   pp.onclick = () => {
     if (!au.paused) { au.pause(); return; }
     audition.pause();                     // never two things at once
     LoopAudio.all.forEach(a => { if (a !== au) a.pause(); });
     // Play what the rack is currently SET to, not the file on disk: with
     // volumes nudged or stems removed, hitting play has to reflect that
     // so a mix decision can be heard before rendering (owner 2026-07-25).
     // The beat number comes off the element — wireTransport only gets
     // `el`, and reaching for makeTrack's `b` here threw on every click.
     if (cue(au, mixUrl(el.dataset.no))) {
       // a staged sample swap makes the machine render the beat again,
       // which is a couple of seconds — say so, or it reads as broken
       pp.innerHTML = '&hellip;';
       au.addEventListener('canplay', function once() {
         au.removeEventListener('canplay', once);
         au.play().catch(() => {});
       });
     } else {
       au.play().catch(() => {});
     }
   };
   au.addEventListener('play', () => { pp.classList.add('on');
     pp.innerHTML = '&#10073;&#10073;'; setNow(el, true); });
   const stop = () => { pp.classList.remove('on'); pp.innerHTML = '&#9654;';
                        if (nowEl === el) setNow(el, false); };
   // A preview that couldn't be built has to SAY so. It used to serve the
   // untouched beat instead, so a failed swap sounded exactly like a swap
   // that did nothing (owner 2026-08-04).
   au.addEventListener('error', () => {
     stop();
     if (au.dataset.src && au.dataset.src.indexOf('/mix') === 0)
       failed('Could not build that preview — the beat you are hearing is '
              + 'unchanged. Check the drive is connected.');
   });
   au.addEventListener('pause', stop);
   const told = () => time.textContent = clock(au.currentTime) + ' / ' + clock(au.duration);
   au.addEventListener('ended', () => { stop(); fill.style.width = '0';
     paintWave(bar, 0); told(); });
   au.addEventListener('timeupdate', () => {
     if (au.duration) {
       fill.style.width = (au.currentTime / au.duration * 100) + '%';
       paintWave(bar, au.currentTime / au.duration);
     }
     told();
     if (nowEl === el) nowTime(au);
   });
   au.addEventListener('loadedmetadata', told);
   bar.onclick = e => {
     if (!au.duration) return;
     const r = bar.getBoundingClientRect();
     au.currentTime = ((e.clientX - r.left) / r.width) * au.duration;
   };
 }

 // ------------------------------------------------------------ waveforms
 // Bars come from the server (/peaks, read-only), drawn on a canvas; the
 // part already played is full colour. If they can't be read the card
 // keeps the old thin progress bar, so playback never depends on it.
 async function drawWave(el, idx) {
   const bar = el.querySelector('.bar');
   try {
     const d = await (await fetch('/peaks?no=' + el.dataset.no + '&n=150')).json();
     if (!d.ok || !d.peaks.length) throw new Error(d.error || 'no peaks');
     bar.peaks = d.peaks;
     // the length is known before the audio loads, so the card can say
     // "0:00 / 0:12" like the mockup without fetching the whole beat
     const au = el.au, time = el.querySelector('.time');
     if (d.seconds && !au.duration) time.textContent = '0:00 / ' + clock(d.seconds);
     if (d.seconds) el.querySelector('.dur').textContent = clock(d.seconds);
     bar.classList.add('has-wave');
     paintWave(bar, bar.frac || 0);
   } catch (e) { bar.classList.remove('has-wave'); }
 }
 function paintWave(bar, frac) {
   bar.frac = frac;
   const p = bar.peaks, cv = bar.querySelector('canvas');
   if (!p || !cv) return;
   const w = cv.clientWidth, h = cv.clientHeight, dpr = window.devicePixelRatio || 1;
   if (!w || !h) return;
   if (cv.width !== Math.round(w * dpr)) {
     cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
   }
   const g = cv.getContext('2d');
   g.setTransform(dpr, 0, 0, dpr, 0, 0);
   g.clearRect(0, 0, w, h);
   const step = w / p.length, bw = Math.max(1, step * 0.55), mid = h / 2;
   const css = getComputedStyle(document.body);
   const lit = css.getPropertyValue('--wave').trim() || '#7CFF32',
         grey = css.getPropertyValue('--dim').trim() || '#a7a7ad';
   p.forEach((v, i) => {
     const x = i * step;
     g.fillStyle = (frac > 0 && x / w <= frac) ? lit : grey;
     g.globalAlpha = (frac > 0 && x / w <= frac) ? 1 : .7;
     const bh = Math.max(2, v * (h - 4));
     g.fillRect(x, mid - bh / 2, bw, bh);
   });
   g.globalAlpha = 1;
 }
 window.addEventListener('resize', () =>
   document.querySelectorAll('.bar.has-wave').forEach(b => paintWave(b, b.frac || 0)));

 // ----------------------------------------- tabs: batch / favorites / dj
 // This batch = what you just made (/batch). Favorites and DJ folder are
 // read-only listings (/folder) — nothing is moved by switching tabs.
 const EMPTY_SAY = {
   batch: 'Make a beat and it lands here &mdash; with every drum in it.',
   favorites: 'No favorites yet &mdash; pass a beat with its star to keep it.',
   trash: 'Trash is empty. A beat you fail lands here &mdash; nothing is deleted, and you can move it back.',
   dj: 'Nothing here yet. This tab shows the folder of the DJ your last batch went to.'
 };
 let SRC = 'batch';
 const viewsrc = document.getElementById('viewsrc');
 viewsrc.onchange = () => loadBatch(null, viewsrc.value);

 async function loadBatch(focus, src) {
   SRC = src || 'batch';
   viewsrc.value = SRC;
   const list = document.getElementById('tracklist'),
         empty = document.getElementById('empty'),
         say = document.getElementById('emptytext');
   let d;
   try {
     d = await (await fetch(SRC === 'batch' ? '/batch' : '/folder?loc=' + SRC)).json();
     if (d.ok === false) throw new Error(d.error);
   } catch (e) {
     list.innerHTML = ''; clearElements(); paintQueue();
     empty.classList.add('err'); empty.style.display = 'block';
     say.textContent = "Couldn't read your beats (" + (e.message || e) +
       '). Is the beats drive plugged in?';
     return;
   }
   empty.classList.remove('err');
   say.innerHTML = EMPTY_SAY[SRC];
   const open = [...list.querySelectorAll('.rack.open')]
                  .map(r => r.closest('.track').dataset.no);
   list.innerHTML = '';
   empty.style.display = (d.beats && d.beats.length) ? 'none' : 'block';
   (d.beats || []).forEach((b, i) => {
     const el = makeTrack(b);
     list.appendChild(el);
     drawWave(el, i);
     if (open.includes(String(b.no)))
       toggleRack(el, b.no, el.querySelector('[data-role=stems]'));
   });
   const keep = selEl && selEl.dataset.no;
   selEl = null;
   const want = list.querySelector('.track[data-no="' + (focus || keep) + '"]') ||
                list.querySelector('.track');
   if (want) selectBeat(want); else clearElements();
   paintQueue();
   if (focus) {
     const el = list.querySelector('.track[data-no="' + focus + '"]');
     if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
   }
 }

 // ---------------------------------------------------------- the stem rack
 function stagedCount(no) { return Object.keys(staged[no] || {}).length; }
 function trimCount(no) { return Object.keys(trims[no] || {}).length; }
 function dropCount(no) { return Object.keys(drops[no] || {}).length; }

 // Where to play a beat FROM. Untouched, that's the rendered file (which
 // seeks, since /audio serves byte ranges). Touched at all — a new sound,
 // a volume, a removal — it's /mix, which renders the beat as the rack is
 // set (owner 2026-08-03: picking a new hi hat changed nothing when he
 // played the beat back). One URL shape for all three kinds of change, so
 // the preview can never disagree with itself.
 function mixUrl(no) {
   const t = trims[no] || {}, d = drops[no] || {}, p = staged[no] || {};
   const pa = pans[no] || {}, ak = Object.keys(pa);
   const tk = Object.keys(t), dk = Object.keys(d).filter(k => d[k]);
   const pk = Object.keys(p).filter(k => p[k]);
   if (!tk.length && !dk.length && !pk.length && !ak.length) return '/audio?no=' + no;
   // only knobs/removals moved and the rack knows the stems: play the
   // lanes live so every knob turn is heard at once
   if (!pk.length && (stemLanes[no] || []).length) return 'stems:' + no;
   let u = '/mix?no=' + no
     + '&trims=' + encodeURIComponent(tk.map(k => k + ':' + t[k]).join(','))
     + '&pans=' + encodeURIComponent(ak.map(k => k + ':' + pa[k]).join(','))
     + '&drop=' + encodeURIComponent(dk.join(','));
   if (pk.length) {
     const picks = {};
     pk.forEach(k => picks[k] = p[k]);
     u += '&picks=' + encodeURIComponent(JSON.stringify(picks));
   }
   return u;
 }

 // Point a player at a URL. load() is not optional: these elements are
 // preload="none", and assigning .src alone leaves them sitting there —
 // that is what made the tracks go silent while the stems still played.
 function cue(au, url) {
   if (au.dataset.src === url && au.readyState) {
     if (au.setLayers) au.setLayers();         // live knobs: no reload
     return false;
   }
   if (url.startsWith('stems:')) au.no = url.slice(6);
   au.dataset.src = url; au.src = url; au.load();
   return true;
 }

 // A beat that's already playing re-cues with the new levels. A paused one
 // is left alone on purpose: every arrow click would otherwise make the
 // server mix the beat again and throw the last one away, and the URL is
 // worked out at play time anyway.
 function refreshMix(el, no) {
   const au = el.au;
   if (!au || au.paused) return;
   const want = mixUrl(no);
   if (au.dataset.src === want) { if (au.setLayers) au.setLayers(); return; }
   const at = au.currentTime;
   cue(au, want);
   au.addEventListener('loadedmetadata', function once() {
     au.removeEventListener('loadedmetadata', once);
     if (at < au.duration) au.currentTime = at;
     au.play().catch(() => {});
   });
 }

 function paintFoot(el, no) {
   saveMix();
   const n = stagedCount(no), v = trimCount(no) + Object.keys(pans[no] || {}).length,
         r = dropCount(no);
   const foot = el.querySelector('.rackfoot');
   if (!foot) return;
   const bits = [];
   if (n) bits.push('<b>' + n + ' ' + (n === 1 ? 'sound' : 'sounds') + ' staged</b>');
   if (v) bits.push('<b>' + v + ' ' + (v === 1 ? 'level' : 'levels') + ' changed</b>');
   if (r) bits.push('<b>' + r + ' ' + (r === 1 ? 'stem' : 'stems') + ' removed</b>');
   foot.querySelector('.staged').innerHTML = bits.length
     ? bits.join(' + ') + ' — Add chunk saves a chunk, Rebuild makes one new beat'
     : 'Pick a different sound, roll the dice, slide a volume, or remove a stem.';
   foot.querySelector('.chunk').disabled = !(n + v + r);
   foot.querySelector('.rebuild').disabled = !(n + v + r);
   foot.querySelector('.undo').style.display = (n + v + r) ? '' : 'none';
   refreshMix(el, no);      // every volume/remove change lands here first
 }

 function laneRow(no, s, i) {
   const row = document.createElement('div');
   row.className = 'lane c' + ((i || 0) % 4) + (s.locked ? ' locked' : '');
   row.dataset.lane = s.lane;
   row.innerHTML =
     '<span class="who2"><span class="swatch"></span>' +
       '<span class="lname"></span></span>' +
     '<span class="what"><span class="sample"></span>' +
       '<span class="pack"></span></span>' +
     '<span class="vol">' +
       '<span class="knob" role="slider" tabindex="0" aria-label="Stem volume" ' +
         'aria-valuemin="-24" aria-valuemax="24" aria-valuenow="0" ' +
         'title="Drag up/down, scroll, or arrow keys. Double-click resets to 0.">' +
         '<svg viewBox="0 0 120 120" aria-hidden="true">' +
           '<path class="ktrack"/><path class="klit"/>' +
           '<circle class="kcap" cx="60" cy="60" r="38"/>' +
           '<g class="kptr"><rect x="88" y="56.5" width="16" height="7" rx="2"/></g>' +
         '</svg></span>' +
       '<span class="db" title="Click to reset to 0">0</span>' +
     '</span>' +
     '<span class="vol pan">' +
       '<span class="knob" role="slider" tabindex="0" aria-label="Stem pan" ' +
         'aria-valuemin="-100" aria-valuemax="100" aria-valuenow="0" ' +
         'title="Pan: drag up/down, scroll, or arrow keys. Double-click centers.">' +
         '<svg viewBox="0 0 120 120" aria-hidden="true">' +
           '<path class="ktrack"/><path class="klit"/>' +
           '<circle class="kcap" cx="60" cy="60" r="38"/>' +
           '<g class="kptr"><rect x="88" y="56.5" width="16" height="7" rx="2"/></g>' +
         '</svg></span>' +
       '<span class="db" title="Click to center">C</span>' +
     '</span>' +
     '<span class="picks"></span>';
   // the row says what the sound IS — "kick drum", "bass drum", "bass",
   // "horns stack" — never a lane key (owner 2026-07-25)
   row.querySelector('.lname').textContent = (s.label || s.lane).toUpperCase();
   row.querySelector('.sample').textContent = s.sample;
   row.querySelector('.pack').textContent = s.pack || '';

   // Volume rides on every lane, locked ones included: a stamp's SAMPLE is
   // the DJ's identity, its level is just mix. Arrows rather than a slider
   // (owner 2026-07-25): a slider jumped and left gaps, this steps exactly
   // 1 dB a click — the standard fine-adjust on a real desk — and the
   // number always shows where you are.
   const db = row.querySelector('.db');
   // Owner 2026-10-10: a KNOB, heard live. Dragging while a stem plays
   // moves its Web Audio gain, so the change is audible as you turn.
   // Same drawing as the Sound Engine's knobs (effects.js), 0.5 dB steps.
   const STEP = 0.5, LIMIT = 24, SWEEP = 270, START = 135;
   const knob = row.querySelector('.knob');
   const kpt = (r, a) => [60 + r * Math.cos(a * Math.PI / 180),
                          60 + r * Math.sin(a * Math.PI / 180)];
   const karc = (a0, a1) => {
     const [x0, y0] = kpt(48, a0), [x1, y1] = kpt(48, a1);
     return 'M' + x0.toFixed(2) + ' ' + y0.toFixed(2) + 'A48 48 0 ' +
            (a1 - a0 > 180 ? 1 : 0) + ' 1 ' + x1.toFixed(2) + ' ' + y1.toFixed(2);
   };
   knob.querySelector('.ktrack').setAttribute('d', karc(START, START + SWEEP));
   let v = (trims[no] || {})[s.lane] || 0, player = null;
   const showDb = () => {
     db.textContent = v ? (v > 0 ? '+' : '') + v.toFixed(1).replace(/\.0$/, '') : '0';
     row.classList.toggle('trimmed', !!v);
     const end = START + SWEEP * (v + LIMIT) / (2 * LIMIT);
     const mid = START + SWEEP / 2;           // 12 o'clock = 0 dB
     knob.querySelector('.klit').setAttribute('d', v ? karc(Math.min(mid, end), Math.max(mid, end)) : '');
     knob.querySelector('.kptr').setAttribute('transform', 'rotate(' + end + ' 60 60)');
     knob.setAttribute('aria-valuenow', v);
     if (player) player.setGain(v);           // heard immediately
     trims[no] = trims[no] || {};
     if (v) trims[no][s.lane] = v; else delete trims[no][s.lane];
     if (!Object.keys(trims[no]).length) delete trims[no];
     paintFoot(row.closest('.track'), no);
   };
   const setV = (x) => {
     v = Math.max(-LIMIT, Math.min(LIMIT, Math.round(x / STEP) * STEP));
     showDb();
   };
   knob.addEventListener('pointerdown', (e) => {
     knob.setPointerCapture(e.pointerId);
     const y0 = e.clientY, v0 = v;
     // owner 2026-10-31: a knob moves ONLY while the button is held. No
     // wheel turning (scrolling past a knob turned it), and any lost
     // release ends the drag so a knob never follows the cursor.
     const move = (ev) => ev.buttons & 1 ? setV(v0 + (y0 - ev.clientY) * 0.25) : up();  // 192 px = full sweep
     const up = () => { knob.removeEventListener('pointermove', move);
                        knob.removeEventListener('pointerup', up);
                        knob.removeEventListener('lostpointercapture', up); };
     knob.addEventListener('pointermove', move);
     knob.addEventListener('pointerup', up);
     knob.addEventListener('lostpointercapture', up);
   });
   knob.addEventListener('keydown', (e) => {
     const d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }[e.key];
     if (d) { e.preventDefault(); setV(v + d * STEP * 2); }
   });
   knob.addEventListener('dblclick', () => setV(0));
   db.onclick = () => setV(0);
   knob.querySelector('.kptr').setAttribute('transform', 'rotate(' + (START + SWEEP / 2) + ' 60 60)');
   if (v) showDb();                          // a saved setting from last time

   // Pan knob (owner 2026-10-15): L100..R100, starts where the lane sits
   // now; double-click or the readout centers it. Only a position that
   // differs from the beat's own is staged.
   const pk = row.querySelector('.pan .knob'), pdb = row.querySelector('.pan .db');
   const pan0 = s.pan || 0;
   let pv = (pans[no] || {})[s.lane] ?? pan0;
   pk.querySelector('.ktrack').setAttribute('d', karc(START, START + SWEEP));
   const showPan = () => {
     pdb.textContent = !pv ? 'C' : (pv < 0 ? 'L' : 'R') + Math.abs(pv);
     const end = START + SWEEP * (pv + 100) / 200, mid = START + SWEEP / 2;
     pk.querySelector('.klit').setAttribute('d', pv ? karc(Math.min(mid, end), Math.max(mid, end)) : '');
     pk.querySelector('.kptr').setAttribute('transform', 'rotate(' + end + ' 60 60)');
     pk.setAttribute('aria-valuenow', pv);
     pans[no] = pans[no] || {};
     if (pv !== pan0) pans[no][s.lane] = pv; else delete pans[no][s.lane];
     if (!Object.keys(pans[no]).length) delete pans[no];
     if (player && player.setPan) player.setPan(pv - pan0);
     paintFoot(row.closest('.track'), no);
   };
   const setP = (x) => { pv = Math.max(-100, Math.min(100, Math.round(x / 5) * 5)); showPan(); };
   pk.addEventListener('pointerdown', (e) => {
     pk.setPointerCapture(e.pointerId);
     const y0 = e.clientY, p0 = pv;
     const move = (ev) => ev.buttons & 1 ? setP(p0 + (y0 - ev.clientY)) : up();   // 200 px = full sweep
     const up = () => { pk.removeEventListener('pointermove', move);
                        pk.removeEventListener('pointerup', up);
                        pk.removeEventListener('lostpointercapture', up); };
     pk.addEventListener('pointermove', move);
     pk.addEventListener('pointerup', up);
     pk.addEventListener('lostpointercapture', up);
   });
   pk.addEventListener('keydown', (e) => {
     const d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }[e.key];
     if (d) { e.preventDefault(); setP(pv + d * 5); }
   });
   pk.addEventListener('dblclick', () => setP(0));
   pdb.onclick = () => setP(0);
   pdb.textContent = !pv ? 'C' : (pv < 0 ? 'L' : 'R') + Math.abs(pv);
   { const end = START + SWEEP * (pv + 100) / 200, mid = START + SWEEP / 2;
     pk.querySelector('.klit').setAttribute('d', pv ? karc(Math.min(mid, end), Math.max(mid, end)) : '');
     pk.querySelector('.kptr').setAttribute('transform', 'rotate(' + end + ' 60 60)'); }

   const picks = row.querySelector('.picks');

   if (s.stem) {
     const b = document.createElement('button');
     b.className = 'mini';
     b.title = 'Hear this on its own, at its level in the track';
     b.innerHTML = '&#9654;';
     // the staged dB rides along, so a stem previews at the level the
     // arrows are set to — same as it will sound in the beat
     // loaded once at 0 dB and looped; the knob moves its gain live
     b.onclick = () => {
       if (player && !player.paused) { player.pause(); b.classList.remove('playing'); return; }
       audition.pause();
       if (auditionBtn) auditionBtn.classList.remove('playing');
       auditionBtn = null;
       LoopAudio.all.forEach(a => a.pause());
       document.querySelectorAll('.lane .mini.playing').forEach(x => x.classList.remove('playing'));
       if (!player) {
         player = new LoopAudio('/stem?no=' + no + '&lane=' +
                                encodeURIComponent(s.lane) + '&db=0');
         player.db = v; player.panv = pv - pan0;
       }
       player.play().catch(() => {});
       b.classList.add('playing');
     };
     picks.appendChild(b);
   }
   if (s.locked) {
     const t = document.createElement('span');
     t.className = 'lock'; t.textContent = s.why || 'locked';
     picks.appendChild(t);
     return row;
   }

   // Drum rows list SAMPLES; a chord/bass row lists INSTRUMENTS (s.voices)
   // — a chord voice is a whole multisample, so there is no one file to
   // pick. Same dropdown, same dice, different contents and a different
   // way of auditioning: see sel.onchange below.
   let sel = null;
   if (s.can_swap) {
     sel = document.createElement('select');
     sel.className = 'snd';            // the sound list; type/tempo sit before it
     sel.innerHTML = '<option value="">reading your library&hellip;</option>';
     sel.disabled = true;
     picks.appendChild(sel);

     const dice = document.createElement('button');
     dice.className = 'mini';
     dice.title = 'Roll a random one — you hear it straight away';
     dice.textContent = '🎲';
     // The dice picks a REAL sample out of the same list the dropdown
     // shows, then plays it (owner 2026-08-03: "I would like the dice
     // roll option to allow me to hear what the sound would be"). It
     // used to stage a "surprise me" the machine only resolved during
     // the rebuild, so there was nothing to play and nothing to name.
     // Roll again for a different one.
     dice.onclick = () => {
       if (row.pickType) row.pickType();   // no type chosen yet: roll one
       const opts = [...sel.options].filter(o => o.value && o.value !== sel.value);
       if (!opts.length) return;         // list still loading, or nothing else
       sel.value = opts[Math.floor(Math.random() * opts.length)].value;
       sel.onchange();                   // stages it, plays it, repaints
     };
     // loops beats: dropdown only, no dice (owner 2026-09-16)
     if (!s.loop) picks.appendChild(dice);
   } else {
     const t = document.createElement('span');
     t.className = 'lock'; t.textContent = s.why || '';
     picks.appendChild(t);
   }

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

   // Ban this sound for good (owner 2026-08-31: "When I ban a sound, it is
   // banned everywhere. forever."). Only offered on rows that ARE a sample
   // — there is nothing to ban on a synthesised lane. Existing beats are
   // never touched; this only stops it being picked again.
   if (s.can_swap) {
     const ban = document.createElement('button');
     ban.className = 'mini';
     ban.title = 'Never use this sound again';
     ban.textContent = '🚫';
     ban.onclick = () => {
       if (ban.disabled) return;              // no double-fire
       const done = d => {
         ban.textContent = '✓';
         ban.disabled = true;
         ban.title = (d.banned === 'name'
           ? 'Every sound called "' + d.name + '" is banned'
           : '"' + d.name + '" is banned — it will not come back');
       };
       const send = choice => {
         ban.disabled = true;
         return fetch('/ban', {
           method: 'POST',
           headers: {'Content-Type': 'application/json'},
           body: JSON.stringify({number: no, lane: s.lane, choice: choice})
         }).then(r => r.json()).then(d => {
           if (!d.ok) { ban.disabled = false; alert(d.error); return; }
           if (d.asked) { ask(d); return; }
           done(d);
         }).catch(() => { ban.disabled = false;
                          alert('could not reach the beat machine'); });
       };
       // A ban cannot be undone from this page, so the choice is three
       // real buttons and NOT confirm(). confirm() has only two answers,
       // which forced Cancel — and Escape, and clicking away — to mean
       // "ban every sound with this name". The dangerous option was on
       // the key people press to get out of a dialog.
       const ask = d => {
         ban.disabled = false;
         const box = document.createElement('div');
         box.className = 'banask';
         const n = d.twins;
         box.innerHTML = '<span>' + (d.sure
           ? n + ' sounds in your library are called "' + esc(d.name) + '".'
           : 'Other sounds may be called "' + esc(d.name) + '" too.')
           + '</span>';
         const pick = (label, choice, title) => {
           const b = document.createElement('button');
           b.className = 'mini'; b.textContent = label; b.title = title;
           b.onclick = () => { box.remove(); if (choice) send(choice); };
           box.appendChild(b);
         };
         pick('just this one', 'sound', 'Ban only the exact sound in this beat');
         if (d.sure) pick('all ' + n, 'name',
                          'Ban every sound with this file name');
         pick('cancel', null, 'Change nothing');
         row.appendChild(box);
       };
       send(null);
     };
     picks.appendChild(ban);
   }

   if (!sel) return row;          // locked row: level + remove only

   sel.onchange = () => {
     staged[no] = staged[no] || {};
     if (!sel.value) delete staged[no][s.lane];
     else {
       staged[no][s.lane] = sel.value;
       // A drum has one file, so play that file. An instrument doesn't —
       // "piano" is a whole multisample, and a single note out of it says
       // nothing about how the chords will sit. So a harmony row auditions
       // by rendering the beat's chords with that instrument (owner
       // 2026-08-04), played on their own (2026-11-01, below).
       // Owner 2026-11-01: the whole beat buried the new instrument (a
       // chord sits ~16 dB under the drums) so it sounded unchanged. Now
       // it is the new instrument ALONE; Play hears it in the beat.
       if (s.voices) play(mixUrl(no) + '&solo=' + encodeURIComponent(s.lane));
       else play('/sample?no=' + no + '&lane=' + encodeURIComponent(s.lane) +
                 '&path=' + encodeURIComponent(sel.value));
       // play() stopped the beat; its next Play starts from the top
       const au = row.closest('.track').au;
       if (au) au.currentTime = 0;
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
       // Owner 2026-09-28: instrument TYPE first (brass, strings,
       // woodwind...), then TEMPO on the Loops page, then the sounds
       // grouped by the words in their names (his synonyms as one group,
       // plain names by pack). A row with one type skips that step.
       const cands = d.candidates;
       const types = [...new Set(cands.map(c => c.type).filter(Boolean))]
         .sort((a, b) => (a === 'Unlabeled') - (b === 'Unlabeled') ||
                         a.localeCompare(b));
       const timed = cands.some(c => 'bpm' in c);
       const bin = c => c.bpm ? String(Math.floor(c.bpm / 10) * 10) : 'none';
       const mine = d.bpm ? String(Math.floor(d.bpm / 10) * 10) : '';
       const mk = title => {
         const x = document.createElement('select');
         x.title = title; picks.insertBefore(x, sel); return x;
       };
       const typeSel = types.length > 1 ? mk('Instrument type') : null;
       const tempoSel = timed ? mk('Tempo') : null;
       if (typeSel) typeSel.innerHTML =
         '<option value="">every type' +
         '</option>' + types.map(t => '<option>' + esc(t) + '</option>').join('');
       const ofType = () => cands.filter(c =>
         !typeSel || !typeSel.value || c.type === typeSel.value);
       const fillTempo = () => {
         if (!tempoSel) return;
         const bins = [...new Set(ofType().map(bin))].sort((a, b) =>
           a === 'none' ? 1 : b === 'none' ? -1 : a - b);
         tempoSel.innerHTML = '<option value="">every tempo</option>' +
           bins.map(b => '<option value="' + b + '">' +
             (b === 'none' ? 'no tempo in name' : b + '–' + (+b + 9) + ' bpm') +
             (b === mine ? ' (this beat)' : '') + '</option>').join('');
         if (bins.includes(mine)) tempoSel.value = mine;
       };
       const fillSounds = () => {
         let html = '<option value="">keep this one</option>';
         const list = ofType().filter(c =>
           !tempoSel || !tempoSel.value || bin(c) === tempoSel.value);
         list.filter(c => c.any).forEach(c => {
           html += '<option value="' + esc(c.path) + '">any ' +
                   esc(c.type.toLowerCase()) + ' &mdash; the machine picks</option>';
         });
         const groups = new Map();
         list.filter(c => !c.any).forEach(c =>
           (c.words && c.words.length ? c.words : [c.pack || 'other']).forEach(w => {
             if (!groups.has(w)) groups.set(w, []);
             groups.get(w).push(c);
           }));
         const plain = w => w.startsWith('Plain names');
         [...groups.keys()].sort((a, b) => (plain(a) - plain(b)) ||
                                          a.localeCompare(b)).forEach(w => {
           html += '<optgroup label="' + esc(w) + '">';
           groups.get(w).forEach(c => {
             html += '<option value="' + esc(c.path) + '">' + esc(c.name) +
                     (c.bpm ? ' · ' + c.bpm + ' bpm' : '') +
                     (c.current ? ' (in this beat now)' : '') + '</option>';
           });
           html += '</optgroup>';
         });
         sel.innerHTML = html;
         const st = (staged[no] || {})[s.lane];
         if (st && list.some(c => c.path === st)) sel.value = st;
       };
       row.refill = () => { fillTempo(); fillSounds(); };
       row.pickType = () => {
         if (!typeSel || typeSel.value) return;
         typeSel.value = types[Math.floor(Math.random() * types.length)];
         row.refill();
       };
       if (typeSel) typeSel.onchange = () => {
         row.refill();
         // one click on a chord type still does what it always did: that
         // instrument, the machine picking inside it
         if (s.voices) {
           const any = cands.find(c => c.any && c.type === typeSel.value);
           sel.value = any ? any.path : '';
           sel.onchange();
         }
       };
       if (tempoSel) tempoSel.onchange = fillSounds;
       const st = cands.find(c => c.path === (staged[no] || {})[s.lane]);
       if (st && typeSel) typeSel.value = st.type;
       fillTempo();
       if (st && tempoSel) tempoSel.value = bin(st);
       fillSounds();
       sel.disabled = false;
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
   else {
     const opt = row.querySelector('select.snd').selectedOptions[0];
     name.textContent = opt ? opt.textContent.replace(' (in this beat now)', '') : 'chosen';
     // an instrument row says what INSTRUMENT it was ("was strings arp"),
     // not which files it drew on — the file names mean nothing here
     row.querySelector('.pack').textContent =
       'was ' + (s.voices ? (s.label || s.sample) : s.sample);
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
   stemLanes[no] = specs.filter(s => s.stem)
     .map(s => ({ lane: s.lane, pan: s.pan || 0 }));
   specs.forEach((s, i) => rack.appendChild(laneRow(no, s, i)));
   const foot = document.createElement('div');
   foot.className = 'rackfoot';
   foot.innerHTML = '<span class="staged"></span>' +
     '<button class="rollall" title="New sound for every row at once">' +
       '🎲 Roll everything</button>' +
     '<button class="undo">clear changes</button>' +
     '<button class="chunk" title="Save this version into the Chunks ' +
       'folder and keep going">+ Add chunk</button>' +
     '<button class="chunk fxon" title="Save a copy of this beat with ' +
       'its style\'s effects (dust, vinyl, saturation) baked in, stems ' +
       'too. The clean one stays.">Effects on</button>' +
     '<button class="rebuild">Rebuild beat</button>' +
     '<button class="rebuild toeffects" title="Open this beat on the Effects ' +
       'page exactly as set here: volumes, pans, removed and swapped sounds. ' +
       'No new beat number.">Effects &rarr;</button>' +
     '<div class="rackmsg" style="flex-basis:100%"></div>';
   rack.appendChild(foot);
   if (specs.some(x => x.loop)) foot.querySelector('.rollall').style.display = 'none';
   // One click, a whole new kit (owner 2026-08-04). Rolls every row that
   // CAN be rolled — the locked producer tag and the synthesised sub are
   // skipped, and so is anything already removed, since rolling a sound
   // he just took out would be nonsense. Nothing plays per row: with a
   // dozen rows that would be a dozen overlapping one-shots, so it
   // auditions once, as the beat, which is the point of rolling them all.
   foot.querySelector('.rollall').onclick = () => {
     let n = 0;
     rack.querySelectorAll('.lane').forEach(r => {
       const sel = r.querySelector('select.snd');
       if (!sel || sel.disabled) return;
       if (drops[no] && drops[no][r.dataset.lane]) return;
       if (r.pickType) r.pickType();
       const opts = [...sel.options].filter(o => o.value && o.value !== sel.value);
       if (!opts.length) return;
       sel.value = opts[Math.floor(Math.random() * opts.length)].value;
       staged[no] = staged[no] || {};
       staged[no][r.dataset.lane] = sel.value;
       const s = specs.find(x => x.lane === r.dataset.lane);
       if (s) paintLane(r, no, s);
       n++;
     });
     if (n) play(mixUrl(no));
   };
   foot.querySelector('.undo').onclick = () => {
     delete staged[no]; delete trims[no]; delete drops[no]; delete pans[no];
     rack.querySelectorAll('.lane').forEach(r => {
       r.querySelectorAll('select').forEach(x => { x.value = ''; });
       if (r.refill) r.refill();
       r.querySelectorAll('.db').forEach(d => d.click());  // volume + pan reset
       r.classList.remove('trimmed');
       r.classList.remove('dropped');
       const s = specs.find(x => x.lane === r.dataset.lane);
       if (s) paintLane(r, no, s);
     });
     paintFoot(el, no);
   };
   foot.querySelector('.rebuild').onclick = () => rebuild(el, no, foot);
   foot.querySelector('.fxon').onclick = () => rebuild(el, no, foot, true);
   foot.querySelector('.toeffects').onclick = () =>
     openEffects(no, el.dataset.seId, foot.querySelector('.rackmsg'));
   foot.querySelector('.chunk').onclick = () => addChunk(no, foot);
   rack.dataset.loaded = '1';
   paintFoot(el, no);
 }

 // Songify: file the rack as it stands into the beat's Chunks folder,
 // then LEAVE the rack staged — the next chunk is usually one more mute
 // on top of this one, not a fresh start.
 async function addChunk(no, foot) {
   const btn = foot.querySelector('.chunk'), msg = foot.querySelector('.rackmsg');
   const was = btn.textContent;
   btn.disabled = true; btn.textContent = 'Saving…'; msg.textContent = '';
   try {
     const r = await fetch('/chunk', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ number: no, picks: staged[no] || {},
                              trims: trims[no] || {},
                              pans: pans[no] || {},
                              drops: Object.keys(drops[no] || {}) }) });
     const d = await r.json();
     msg.textContent = d.ok
       ? 'chunk ' + d.count + ' saved — ' + d.file
       : d.error;
   } catch (e) { msg.textContent = String(e); }
   btn.textContent = was; btn.disabled = false;
 }

 // Effects (owner 2026-10-21): the beat AS THE RACK IS SET goes to the
 // Effects page -- volumes, pans, removals and sound swaps -- with no new
 // number. Nothing changed = the beat itself.
 async function openEffects(no, seId, msg) {
   // One tab only (owner 2026-10-31): Effects loads in THIS tab, and its
   // Send back / Sketch buttons load the Beat Machine back into it.
   const picks = staged[no] || {}, vols = trims[no] || {}, pn = pans[no] || {};
   const gone = Object.keys(drops[no] || {});
   const changed = Object.keys(picks).length || Object.keys(vols).length ||
                   Object.keys(pn).length || gone.length;
   try {
     let id = seId;
     if (changed) {
       if (msg) msg.textContent = 'Getting your mix ready for Effects…';
       const r = await fetch('/effects-stage', { method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ number: no, picks, trims: vols, pans: pn,
                                drops: gone }) });
       const d = await r.json();
       if (!d.ok) throw new Error(d.error);
       id = d.se_id;
     } else {
       await fetch('/engine-up', { method: 'POST', body: '{}' });
     }
     if (!id) throw new Error('This beat can\'t open in Effects.');
     if (msg) msg.textContent = '';
     location.href = engineLink(id);
   } catch (e) {
     if (msg) msg.textContent = String(e.message || e); else alert(e.message || e);
   }
 }

 async function rebuild(el, no, foot, fx) {
   const picks = staged[no] || {}, vols = trims[no] || {};
   const gone = Object.keys(drops[no] || {});
   if (!fx && !Object.keys(picks).length && !Object.keys(vols).length
       && !Object.keys(pans[no] || {}).length && !gone.length) return;
   const btn = foot.querySelector(fx ? '.fxon' : '.rebuild'),
         msg = foot.querySelector('.rackmsg');
   btn.disabled = true; msg.textContent = '';
   const was = btn.textContent;
   btn.textContent = 'Rebuilding…';
   // Rebuild goes straight on to the Effects page (owner 2026-10-15),
   // in this same tab (owner 2026-10-31: one tab only).
   try {
     const r = await fetch('/rebuild', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ number: no, picks, trims: vols,
                              pans: pans[no] || {}, drops: gone, fx: !!fx }) });
     const d = await r.json();
     if (d.ok) { delete staged[no]; delete trims[no]; delete drops[no];
                 delete pans[no]; saveMix();
                 if (!fx && d.se_id) {
                   await fetch('/engine-up', { method: 'POST', body: '{}' });
                   location.href = engineLink(d.se_id); return;
                 }
                 btn.textContent = was; await loadBatch(d.no); }
     else { msg.textContent = d.error; btn.textContent = was; btn.disabled = false; }
   } catch (e) {
     msg.textContent = String(e); btn.textContent = was; btn.disabled = false;
   }
 }

 // --------------------------------------------- reference track (sec. 5)
 // Drop a song; read its tempo and key; SHOW both so he can correct them.
 // The detector is wrong in two predictable ways — half or double the
 // tempo, and the relative major/minor — so the correction buttons are
 // the feature, not a fallback.
 const refdrop = document.getElementById('refdrop'),
       refline = document.getElementById('refline'),
       keysel = document.getElementById('key'),
       tempoBox = document.getElementById('tempo');
 let refName = '', refAlt = null;
 const TLO = __TEMPOLO__, THI = __TEMPOHI__;   // the window /make enforces

 function refSay() {
   refline.classList.remove('bad');
   flask();
   if (!refName) { refline.textContent = 'nothing dropped yet'; return; }
   const bpm = parseFloat(tempoBox.value);
   refline.innerHTML = '<b>' + esc(refName) + '</b> &mdash; ' +
     (tempoBox.value || '?') + ' BPM, ' +
     (keysel.value ? keysel.value.replace('_', ' ') : 'any key') +
     // only offer an octave the tempo box would actually accept
     (bpm / 2 >= TLO ? '<button data-ref="half">&divide;2</button>' : '') +
     (bpm * 2 <= THI ? '<button data-ref="double">&times;2</button>' : '') +
     (refAlt ? '<button data-ref="rel">' + esc(refAlt.replace('_', ' ')) +
               '?</button>' : '') +
     '<button data-ref="clear">clear</button>';
 }

 refline.onclick = e => {
   const what = e.target.dataset && e.target.dataset.ref;
   if (!what) return;
   const bpm = parseFloat(tempoBox.value);
   if (what === 'half' && bpm / 2 >= TLO) tempoBox.value = Math.round(bpm / 2);
   if (what === 'double' && bpm * 2 <= THI) tempoBox.value = Math.round(bpm * 2);
   if (what === 'rel' && refAlt) {          // swaps, so it flips back
     const was = keysel.value;
     keysel.value = refAlt;
     refAlt = was || null;
   }
   if (what === 'clear') {
     refName = ''; refAlt = null; tempoBox.value = ''; keysel.value = '';
   }
   refSay();
 };

 ['dragover', 'dragenter'].forEach(ev =>
   refdrop.addEventListener(ev, e => {
     e.preventDefault(); refdrop.classList.add('over'); }));
 refdrop.addEventListener('dragleave', () => refdrop.classList.remove('over'));
 refdrop.addEventListener('drop', e => {
   e.preventDefault(); refdrop.classList.remove('over');
   readRef(e.dataTransfer.files && e.dataTransfer.files[0]);
 });
 // click (or Enter) to pick a file instead of dragging one \u2014 same reader
 const reffile = document.getElementById('reffile');
 refdrop.addEventListener('click', () => { if (!refdrop.classList.contains('busy')) reffile.click(); });
 refdrop.addEventListener('keydown', e => {
   if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); refdrop.click(); } });
 reffile.addEventListener('change', () => { readRef(reffile.files[0]); reffile.value = ''; });
 // what the server's reader can open (reference_track.py: libsndfile, then
 // macOS afconvert for m4a/mp3) and the size it will take (/reference)
 const REF_EXT = ['.mp3', '.wav', '.m4a', '.aif', '.aiff', '.flac'];
 const REF_MAX = 300 * 1024 * 1024;
 function refBad(msg) { refline.textContent = msg; refline.classList.add('bad'); }
 async function readRef(f) {
   if (!f) return;
   const dot = f.name.lastIndexOf('.');
   const ext = (dot > 0 ? f.name.slice(dot) : '.wav')
                 .replace(/[^A-Za-z0-9.]/g, '');
   if (!REF_EXT.includes(ext.toLowerCase())) {
     refBad("Can't read " + (ext || 'that') + ' files. Use MP3, WAV, M4A, AIFF or FLAC.');
     return; }
   if (f.size > REF_MAX) {
     refBad('That file is ' + Math.round(f.size / 1048576) + ' MB. The limit is 300 MB.');
     return; }
   const was = refdrop.innerHTML;
   refdrop.classList.add('busy');
   refdrop.textContent = 'Listening to ' + f.name + '\u2026';
   try {
     const r = await fetch('/reference', { method: 'POST',
       headers: { 'X-Ext': ext || '.wav' }, body: await f.arrayBuffer() });
     const d = await r.json();
     if (d.ok) {
       refName = f.name;
       tempoBox.value = d.bpm;
       keysel.value = d.root + ' ' + d.mode;
       refAlt = d.alt_root ? d.alt_root + ' ' + d.alt_mode : null;
       refSay();
     } else { refBad(d.error); }
   } catch (err) { refBad(String(err)); }
   refdrop.classList.remove('busy');
   refdrop.innerHTML = was;
 }

 // ------------------------------------------------- tempo / count arrows
 // Tempo blank still means "home tempo"; the first arrow click starts from
 // the first-picked DJ's home tempo (or 95) so it never jumps somewhere odd.
 document.querySelectorAll('.spin [data-for]').forEach(b => b.onclick = () => {
   const box = document.getElementById(b.dataset.for);
   const isTempo = box.id === 'tempo';
   const lo = isTempo ? TLO : 1, hi = isTempo ? THI : 10;
   let v = parseFloat(box.value);
   if (!isFinite(v)) {
     const card = order.length && [...document.querySelectorAll('.dj input')]
                    .find(c => c.value === order[0]);
     v = isTempo ? parseFloat(card ? card.closest('.dj').querySelector('.bpm').textContent : 95) || 95
                 : 1;
     if (isTempo) { box.value = Math.min(hi, Math.max(lo, Math.round(v))); return; }
   }
   box.value = Math.min(hi, Math.max(lo, Math.round(v + Number(b.dataset.d))));
   flask();
 });
 // a clicked arrow that sets the starting tempo returns early: catch it too
 document.querySelectorAll('.spin [data-for=tempo]').forEach(b =>
   b.addEventListener('click', flask));

 // ------------------------------------------------------------- make them
 const go = document.getElementById('go'),
       work = document.getElementById('work'),
       worktext = document.getElementById('worktext'),
       tracklist = document.getElementById('tracklist');
 // while anything renders, the board shows a pulsing placeholder card
 function working(msg) { work.className = 'on'; worktext.textContent = msg;
                         if (SRC === 'batch') tracklist.classList.add('loading'); }
 function failed(msg) { work.className = 'on bad'; worktext.textContent = msg;
                        tracklist.classList.remove('loading'); }
 function done() { work.className = ''; tracklist.classList.remove('loading'); }

 go.onclick = async () => {
   if (!order.length) { failed('Check at least one DJ first.'); return; }
   // loops mode: a DJ teams up with styles only, never another DJ
   if (document.getElementById('loopsonly').checked &&
       order.filter(n => !document.querySelector(
         '.dj.genre input[value="' + CSS.escape(n) + '"]')).length > 1) {
     failed('Loops only: a DJ can team up with styles, not with another DJ. ' +
            'Untick all but one DJ.'); return; }
   const count = document.getElementById('count').value;
   go.disabled = true; go.setAttribute('aria-busy', 'true');
   working(count > 1
     ? 'Making ' + count + ' beats… the first one scans your sample library.'
     : 'Making it… the first beat scans your sample library (about 30 seconds).');
   try {
     const r = await fetch('/make', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ names: order,
         tempo: tempoBox.value.trim(),
         key: keysel.value,
         count, notes: notesBox.value,
         loops_only: document.getElementById('loopsonly').checked }) });
     const d = await r.json();
     if (d.ok) { done(); await loadBatch(); }
     else failed(d.error);
   } catch (e) { failed(String(e)); }
   go.disabled = false; go.removeAttribute('aria-busy');
 };

 // -------------------------------------------------------- pattern library
 const LIBRARY_PATTERNS = __LIBRARYJSON__;
 function fillLibPatterns() {
   const names = LIBRARY_PATTERNS[document.getElementById('libgenre').value] || [];
   document.getElementById('libpattern').innerHTML =
     names.map(n => `<option value="${n}">${n}</option>`).join('');
 }
 document.getElementById('libgenre').onchange = fillLibPatterns;
 fillLibPatterns();

 async function playLibrary(genre, name, btn) {
   btn.disabled = true;
   working('Rendering ' + name + '…');
   try {
     const r = await fetch('/library', { method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ genre, name }) });
     const d = await r.json();
     if (d.ok) { done(); await loadBatch(d.no); }
     else failed(d.error);
   } catch (e) { failed(String(e)); }
   btn.disabled = false;
 }
 document.getElementById('libgo').onclick = () => {
   const btn = document.getElementById('libgo');
   playLibrary(document.getElementById('libgenre').value,
              document.getElementById('libpattern').value, btn);
 };
 document.getElementById('libbreakgo').onclick = () => {
   const btn = document.getElementById('libbreakgo');
   playLibrary('breaks', document.getElementById('libbreak').value, btn);
 };

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


 // ------------------------------------------- class tabs + toolbar pop-ups
 document.querySelectorAll('.tabs [data-tab]').forEach(t => t.onclick = () => {
   document.querySelectorAll('.tabs [data-tab]').forEach(x =>
     x.setAttribute('aria-selected', String(x === t)));
   document.querySelectorAll('.roster').forEach(r => r.hidden = r.dataset.kind !== t.dataset.tab);
 });
 document.querySelectorAll('details.tool').forEach(d => d.addEventListener('toggle', () => {
   if (d.open) document.querySelectorAll('details.tool[open]').forEach(o => { if (o !== d) o.open = false; });
 }));
 document.getElementById('side-saved').onclick = e => {
   e.stopPropagation();
   const t = document.getElementById('savedtool');
   t.open = true; t.scrollIntoView({ behavior: 'smooth', block: 'center' });
 };

 // ------------------------------------------------------------ tempo flask
 // The liquid and the scale come from the SAME numbers (TLO..THI), so the
 // flask can never disagree with the BPM box. Blank = the DJ's home tempo.
 const FL_TOP = 22, FL_BOT = 146;
 const flY = v => FL_BOT - (v - TLO) / (THI - TLO) * (FL_BOT - FL_TOP);
 (function ticks() {
   const g = document.getElementById('fticks');
   for (let i = 0; i <= 4; i++) {
     const v = Math.round(TLO + (THI - TLO) * i / 4), y = flY(v);
     g.insertAdjacentHTML('beforeend', '<g class="tk" data-v="' + v + '"><line x1="44" x2="51" y1="' + y +
       '" y2="' + y + '"/><text x="55" y="' + (y + 3.4) + '">' + v + '</text></g>');
   }
 })();
 function flask() {
   const v = parseFloat(tempoBox.value), ok = isFinite(v);
   const y = ok ? flY(Math.max(TLO, Math.min(THI, v))) : FL_BOT - 12;
   const f = document.querySelector('.flask'), liq = f.querySelector('.liq');
   liq.setAttribute('y', y); liq.setAttribute('height', 160 - y);
   f.classList.toggle('auto', !ok);
   // a tick above the liquid sits on glass, not liquid: draw it light
   f.querySelectorAll('.tk').forEach(t => t.classList.toggle('dry', flY(+t.dataset.v) < y - 1));
 }
 tempoBox.addEventListener('input', flask);
 flask();

 // ------------------------------------------------------- Loops only mode
 // Same palette, swapped roles (body.loops in the CSS), plus words, so the
 // colour is never the only sign of which mode is on.
 const loopsBox = document.getElementById('loopsonly');
 function paintMode() {
   const on = loopsBox.checked;
   document.body.classList.toggle('loops', on);
   document.getElementById('goword').textContent = on ? 'Generate Loops' : 'Generate Beats';
   document.getElementById('modeword').textContent = on ? 'Loop mode' : 'Beat mode';
   go.setAttribute('aria-label', on ? 'Generate loops' : 'Generate beats');
   document.querySelectorAll('.bar.has-wave').forEach(b => paintWave(b, b.frac || 0));
 }
 loopsBox.addEventListener('change', paintMode);
 paintMode();

 // ------------------------------------------- selected beat: Elements table
 // Tiles come from /stems (the same read-only call the rack makes): the
 // real role and sample for every sound, however many there are.
 let selEl = null, nowEl = null;
 const CODES = [['open hat', 'Oh'], ['hat', 'Hh'], ['kick', 'Kk'], ['bass drum', 'Kk'],
   ['snare', 'Sn'], ['clap', 'Cp'], ['rim', 'Rm'], ['808', 'Bm'], ['boom', 'Bm'],
   ['sub', 'Sb'], ['bass', 'Bs'], ['chord', 'Ch'], ['pad', 'Pd'], ['lead', 'Ld'],
   ['melod', 'Ml'], ['piano', 'Pn'], ['key', 'Ky'], ['string', 'St'], ['horn', 'Hn'],
   ['brass', 'Br'], ['vocal', 'Vx'], ['vox', 'Vx'], ['sample', 'Sm'], ['loop', 'Lp'],
   ['perc', 'Pc'], ['shaker', 'Sh'], ['tom', 'Tm'], ['ride', 'Rd'], ['crash', 'Cr'],
   ['cymbal', 'Cy'], ['bell', 'Bl'], ['guitar', 'Gt'], ['organ', 'Or'], ['tag', 'Tg'],
   ['fx', 'Fx'], ['texture', 'Fx'], ['riser', 'Fx']];
 function code(label) {
   const l = label.toLowerCase(), hit = CODES.find(([w]) => l.includes(w));
   if (hit) return hit[1];
   const w = label.replace(/[^A-Za-z]/g, '');
   return (w[0] || '?').toUpperCase() + (w[1] || '').toLowerCase();
 }
 const elTiles = document.getElementById('eltiles'),
       elMeta = document.getElementById('elmeta'),
       elCount = document.getElementById('elcount');
 function clearElements() {
   elCount.textContent = ''; elTiles.innerHTML = '';
   elMeta.innerHTML = '<span class="hint">Pick a beat to see what&rsquo;s in it.</span>';
 }
 async function selectBeat(el) {
   if (!el || el === selEl) return;
   if (selEl) selEl.classList.remove('sel');
   selEl = el; el.classList.add('sel');
   const no = el.dataset.no, th = el.querySelector('.theory').innerHTML;
   elMeta.innerHTML = '<div class="eltitle">' + esc(el.querySelector('.tname').textContent) +
     '</div><div>' + el.querySelector('.tmetaline').innerHTML + '</div>' + th;
   elCount.textContent = ''; elTiles.innerHTML = '<p class="hint">reading the sounds&hellip;</p>';
   let d;
   try { d = await (await fetch('/stems?no=' + no)).json(); }
   catch (e) { d = { ok: false, error: 'Could not read that beat.' }; }
   if (selEl !== el) return;                  // picked another meanwhile
   if (!d.ok) { elTiles.innerHTML = '<p class="hint bad">' + esc(d.error || 'Could not read that beat.') + '</p>'; return; }
   elCount.textContent = '· ' + d.stems.length + (d.stems.length === 1 ? ' sound' : ' sounds');
   elTiles.innerHTML = d.stems.map((s, i) => {
     const name = s.label || s.lane;
     return '<button type="button" class="tile c' + (i % 4) + (s.locked ? ' locked' : '') +
       '" data-lane="' + esc(s.lane) + '" title="' + esc(name + ' — ' + (s.sample || '') +
       (s.pack ? ' (' + s.pack + ')' : '') + '. Click to open it in Stems.') + '">' +
       '<span class="tn">' + String(i + 1).padStart(2, '0') + '</span>' +
       '<span class="tc">' + esc(code(name)) + '</span>' +
       '<span class="tl">' + esc(name) + '</span>' +
       '<span class="ts">' + esc(s.sample || '') + '</span></button>';
   }).join('');
   elTiles.querySelectorAll('.tile').forEach(t => t.onclick = async () => {
     const rack = el.querySelector('.rack');
     if (!rack.classList.contains('open'))
       await toggleRack(el, no, el.querySelector('[data-role=stems]'));
     const row = rack.querySelector('.lane[data-lane="' + CSS.escape(t.dataset.lane) + '"]');
     if (row) {
       row.scrollIntoView({ behavior: 'smooth', block: 'center' });
       row.classList.add('flash'); setTimeout(() => row.classList.remove('flash'), 1400);
     }
   });
 }

 // ------------------------------------------------------ now-playing bar
 // Mirrors whichever card is playing; its buttons press that card's own
 // play button, so there is still only one player per beat.
 const npp = document.getElementById('npp');
 function artOf(el) {
   const a = el.querySelector('.art');
   return { cls: a.className, no: el.dataset.no };
 }
 function setNow(el, playing) {
   nowEl = el;
   const a = artOf(el), art = document.getElementById('nart');
   art.className = a.cls; art.querySelector('b').textContent = a.no;
   document.getElementById('ntitle').textContent = el.querySelector('.tname').textContent;
   document.getElementById('nsub').innerHTML = el.querySelector('.tmetaline').innerHTML;
   npp.classList.toggle('on', playing);
   npp.innerHTML = playing ? '&#10073;&#10073;' : '&#9654;';
   npp.setAttribute('aria-label', playing ? 'Pause' : 'Play');
   document.querySelectorAll('#nqueue button').forEach(b =>
     b.classList.toggle('now', b.dataset.no === el.dataset.no));
 }
 function nowTime(au) {
   document.getElementById('nfill').style.width = (au.duration ? au.currentTime / au.duration * 100 : 0) + '%';
   document.getElementById('ntime').textContent = clock(au.currentTime) + ' / ' + clock(au.duration);
 }
 npp.onclick = () => {
   const el = nowEl || selEl || document.querySelector('.track');
   if (el) el.querySelector('.pp').click();
 };
 function step(d) {
   const all = [...document.querySelectorAll('#tracklist .track')];
   if (!all.length) return;
   const cur = all.indexOf(nowEl || selEl);
   const el = all[(cur + d + all.length) % all.length];
   selectBeat(el);
   el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
   el.querySelector('.pp').click();
 }
 document.getElementById('nprev').onclick = () => step(-1);
 document.getElementById('nnext').onclick = () => step(1);
 function paintQueue() {
   const q = document.getElementById('nqueue');
   q.innerHTML = [...document.querySelectorAll('#tracklist .track')].map(el => {
     const a = artOf(el);
     return '<button type="button" data-no="' + a.no + '" title="' + esc(el.querySelector('.tname').textContent) +
       '"' + (nowEl && nowEl.dataset.no === a.no ? ' class="now"' : '') +
       '><span class="' + a.cls + '"><b>' + a.no + '</b></span></button>';
   }).join('');
   q.querySelectorAll('button').forEach(b => b.onclick = () => {
     const el = document.querySelector('#tracklist .track[data-no="' + b.dataset.no + '"]');
     if (el) { selectBeat(el); el.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
   });
 }

 loadBatch(+new URLSearchParams(location.search).get('beat') || undefined);
 // the Effects page's Sketch button lands here with &sketch=effects
 if (new URLSearchParams(location.search).get('sketch') === 'effects')
   window.addEventListener('load', () => window.openSketch &&
     openSketch(+new URLSearchParams(location.search).get('beat'), 'effects'));
</script>
<link rel="stylesheet" href="/sketch.css">
<script src="/sketch.js"></script>
</body></html>"""


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


def _break_word(name):
    """The words the picker should type for this figure — the SAME trigger
    the notes box matches, so picking and typing take one code path."""
    return next((w for w, frag in BREAK_WORDS if frag in name), None)


def _break_options():
    """The Famous beats menu, built from the pattern pack itself so adding a
    figure to the JSON is the only step needed to make it pickable."""
    out = []
    for p in break_list():
        word = _break_word(p["name"])
        if not word:                # in the pack but nothing selects it
            continue
        label = p["name"].replace(" Figure", "")
        src = p.get("source", "")
        out.append('      <option value="%s">%s%s</option>'
                   % (word, label,
                      " &mdash; " + src.replace("&", "&amp;") if src else ""))
    return "\n".join(out)


def _library_genre_options():
    return "\n".join(f'      <option value="{key}">{label}</option>'
                     for key, (label, _fname) in LIBRARY_GENRES.items())


def _library_break_options():
    """Combined famous-figures + funk-breaks menu — its own dropdown, its
    own render target, never merged into a genre."""
    out = []
    for p in library_breaks():
        name = p["name"]
        src = p.get("source", "").replace("&", "&amp;")
        label = name + (" &mdash; " + src if src else "")
        out.append(f'      <option value="{name}">{label}</option>')
    return "\n".join(out)


def _page():
    crew = "".join(_dj_card(n) for n in CREW_ORDER)
    legends = "".join(_dj_card(n) for n in LEGEND_ORDER)
    styles = "".join(_dj_card(n) for n in GENRE_ORDER)
    logo = _brand_logo("blue")
    if logo:
        src = f"/brand?name={quote(logo.name)}"
        mark = f'<img src="{src}" alt="The Back of the Class">'
        ghost = f'<div class="ghost"><img src="{src}" alt=""></div>'
    else:                       # no artwork dropped in yet — type mark
        mark, ghost = "<span>BOTC</span>", ""
    # straight off ROOT_HZ and MODES, so the dropdowns can never offer a
    # key the engine would then refuse
    from key_context import MODES
    # ONE dropdown ("A minor"): minor keys, major keys, then the other modes
    order = [m for m in ("minor", "major") if m in MODES] + sorted(
        m for m in MODES if m not in ("minor", "major"))
    keyopts = "".join(
        '<optgroup label="%s keys">%s</optgroup>' % (
            m.replace("_", " ").capitalize(),
            "".join('<option value="%s %s">%s %s</option>'
                    % (r, m, r, m.replace("_", " ")) for r in ROOT_HZ))
        for m in order)
    return (_PAGE.replace("__CREW__", crew).replace("__LEGENDS__", legends)
            .replace("__GENRES__", styles)
            .replace("__BREAKS__", _break_options())
            .replace("__LIBGENRES__", _library_genre_options())
            .replace("__LIBBREAKS__", _library_break_options())
            .replace("__LIBRARYJSON__", json.dumps({
                key: [p["name"] for p in patterns]
                for key, (label, patterns) in library_genres().items()}))
            .replace("__CREWCOUNT__", _count_word(len(CREW_ORDER)))
            .replace("__TEMPOLO__", str(TEMPO_LO))
            .replace("__TEMPOHI__", str(TEMPO_HI))
            .replace("__KEYOPTS__", keyopts)
            .replace("__MARK__", mark).replace("__GHOST__", ghost))


def _count_word(n):
    """Spell the crew count on the page. It was hard-coded "nine" and went
    stale the moment a tenth DJ arrived (2026-09-03), so it is derived from
    CREW_ORDER now and cannot lie again."""
    return {9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
            13: "thirteen", 14: "fourteen"}.get(n, str(n))


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

    class Server(ThreadingHTTPServer):
        def handle_error(self, request, client_address):
            # The <audio> player cancels in-flight requests whenever he
            # scrubs or switches tracks — the client just hung up mid-
            # response. That's normal, not a bug, so don't dump a
            # traceback for it (same "never a stack trace" rule as the
            # port-in-use case below). Anything else still prints.
            if isinstance(sys.exc_info()[1],
                         (BrokenPipeError, ConnectionResetError)):
                return
            super().handle_error(request, client_address)

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
            elif u.path == "/weights":
                self._send(200, "text/html; charset=utf-8",
                           (Path(__file__).parent / "weights_page.html")
                           .read_bytes())
            elif u.path == "/weights-data":
                import weights_editor
                self._json(weights_editor.collect())
            elif u.path == "/batch":
                self._json({"beats": _batch_beats()})
            elif u.path == "/folder":
                loc = parse_qs(u.query).get("loc", [""])[0]
                try:
                    self._json({"ok": True, "beats": _folder_beats(loc)})
                except Exception as e:
                    self._json({"ok": False, "error": str(e), "beats": []})
            elif u.path == "/peaks":
                q = parse_qs(u.query)
                no = q.get("no", [""])[0]
                n = q.get("n", ["160"])[0]
                w = _known_wav(no) if no.isdigit() else None
                try:
                    if not w:
                        raise FileNotFoundError(f"No beat {no} in your library.")
                    with wave.open(str(w), "rb") as f:   # length, header only
                        secs = f.getnframes() / float(f.getframerate())
                    self._json({"ok": True, "seconds": round(secs, 2),
                                "peaks": _peaks(w, max(16, min(
                                    int(n) if n.isdigit() else 160, 600)))})
                except Exception as e:
                    self._json({"ok": False, "error": str(e), "peaks": []})
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
                        bpm = load_recipe(ROOT, int(q.get("no", [""])[0])
                                          )["preset"].get("bpm")
                    self._json({"ok": True, "candidates": cands, "bpm": bpm})
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
                if not str(no).isdigit():
                    self._send(404, "text/plain", b"not found")
                    return
                self._solo(int(no), lane.strip().lower(),
                           _qs_db(q.get("db", ["0"])[0]))
            elif u.path == "/mix":
                # the whole beat as the rack is SET — new sounds, volumes
                # and removals — rendered but not printed (owner
                # 2026-07-25: "I adjust a stem's volume, hit play, and the
                # track reflects it — so I can hear what's going on before
                # I render")
                q = parse_qs(u.query)
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        got = _preview_render(u.query, q,
                                              shots=_CACHE["shots"])
                    self._media(got)
                except Exception as e:
                    # NEVER fall back to the printed file (owner
                    # 2026-08-04). It used to serve the untouched beat
                    # here, which is the worst possible answer: the change
                    # is staged, the page says so, and playback quietly
                    # sounds like the old one — the exact confusion the
                    # swap-preview fix was for, wearing a disguise. Say
                    # what went wrong instead, and let the page show it.
                    self._send(500, "text/plain",
                               str(e).encode("utf-8") or b"preview failed")
            elif u.path == "/sketch-info":
                # Song Sketch: what the sketch board needs for beat `no`
                no = parse_qs(u.query).get("no", [""])[0]
                src = parse_qs(u.query).get("src", [""])[0]
                try:
                    import song_sketch
                    rows = song_sketch.rows_for(
                        _beat_stems(no, folder=_sketch_folder(int(no), src)))
                    if not rows:
                        raise ValueError("This beat has no stem files to "
                                         "arrange.")
                    bpm = load_recipe(ROOT, int(no))["preset"].get("bpm")
                    self._json({"ok": True, "no": int(no), "bpm": bpm,
                                "stems": rows, **song_sketch.options(rows, bpm)})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
            elif u.path == "/sketch-file":
                q = parse_qs(u.query)
                import song_sketch
                p = song_sketch.file_path(q.get("id", [""])[0],
                                          q.get("name", [""])[0])
                if not p:
                    self._send(404, "text/plain", b"not found")
                elif p.suffix == ".wav":
                    self._media(p.read_bytes())
                else:
                    self._send(200, song_sketch.FILES[p.name], p.read_bytes())
            elif u.path in ("/sketch.js", "/sketch.css"):
                f = Path(__file__).parent / "sketch_ui" / u.path[1:]
                self._send(200, "text/javascript; charset=utf-8"
                           if f.suffix == ".js" else "text/css; charset=utf-8",
                           f.read_bytes())
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
            """A one-shot from the library, decoded and re-wrapped as the
            same 24-bit WAV every other endpoint serves. No level is
            applied — it is not part of any mix.

            Decoded, NOT handed through raw (owner 2026-08-03: "sometimes
            when I click on the new sample it doesn't make a sound"):
            about a quarter of his library is .aif, and the raw bytes went
            out labelled audio/wav, which the browser silently refused to
            play. Same for any WAV whose bit depth the browser won't take.
            load_audio already reads every format the engine accepts, so
            routing through it makes the audition match the render."""
            if not path or not Path(path).exists():
                self._send(404, "text/plain", b"not found")
                return
            x = load_audio(path)
            if x is None or not len(x):
                self._send(404, "text/plain", b"not found")
                return
            self._media(wav24_bytes(x[:, 0], x[:, 1]))

        def _solo(self, no, lane, db=0.0):
            # One row on its own, at its level IN THE TRACK plus whatever
            # the volume arrows are set to — so previewing tells him what
            # he will actually hear (owner 2026-07-25). Before this,
            # stems played at their printed level and the arrows did
            # nothing until a rebuild, so a mix move couldn't be heard.
            try:
                got = _solo_audio(no, lane)
            except Exception:
                got = None
            if got is None:
                self._send(404, "text/plain", b"not found")
                return
            L, R = got
            g = (10 ** (float(db) / 20.0)) * _track_gain(no)
            peak = float(max(np.abs(L).max(), np.abs(R).max())) * g
            if peak > 0.94:               # a big boost can't be allowed
                g *= 0.94 / peak          # to clip the preview
            self._media(wav24_bytes(L * g, R * g))

        def _media(self, data):
            """Audio for an <audio> element. Range-aware: the player asks
            for "bytes=0-" before it will commit to a file, and the scrub
            bar needs real ranges to seek. Serving a plain 200 here is
            what left the live /mix silent — the element reported itself
            as playing while duration stayed null (owner 2026-07-25)."""
            rng = self.headers.get("Range")
            if rng and rng.startswith("bytes="):
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

        def _audio(self, no):
            # only ever a beat NUMBER from the client, resolved to a file
            # under the beats root here — no client path ever touches disk
            w = beat_wav(int(no)) if str(no).isdigit() else None
            if not w or not w.exists():
                self._send(404, "text/plain", b"not found")
                return
            self._media(w.read_bytes())

        def do_POST(self):
            if self.path not in ("/make", "/swap", "/triage", "/rebuild",
                                 "/fixed", "/library", "/ban", "/chunk",
                                 "/reference", "/engine-up", "/engine-import", "/effects-stage",
                                 "/sketch", "/weights-save"):
                self._send(404, "text/plain", b"not found")
                return
            if self.path == "/reference":
                # He dragged a song onto the page. The body is the raw
                # file, not JSON, so this branch sits above the parse.
                # The audio is read, measured and thrown away — nothing
                # from his reference track is kept or sampled.
                size = int(self.headers.get("Content-Length", 0))
                if size > 300 * 1024 * 1024:
                    self._json({"ok": False,
                                "error": "That file is too big to read."})
                    return
                try:
                    raw = self.rfile.read(size)
                    ext = self.headers.get("X-Ext", ".wav")
                    import reference_track
                    res = reference_track.analyze_bytes(raw, "ref" + ext)
                    print("  reference: %s BPM, %s %s"
                          % (res["bpm"], res["root"], res["mode"]))
                    self._json({"ok": True, **res})
                except subprocess.CalledProcessError:
                    # afconvert (the m4a/mp3 reader) refused it
                    self._json({"ok": False, "error":
                                "Couldn't read that file as audio. Try an "
                                "MP3, WAV, M4A, AIFF or FLAC."})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/weights-save":
                try:
                    import weights_editor
                    with lock:
                        weights_editor.save(data["label"], data["name"],
                                            data["path"], data["items"])
                    self._json({"ok": True})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/library":
                # the pattern-library browser: any groove from the four
                # genre files, or the separate Breaks bucket
                try:
                    genre = str(data.get("genre", ""))
                    name = str(data.get("name", ""))
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        path, report = generate_library(genre, name,
                                                        shots=_CACHE["shots"])
                        no = int(path.name.split(" ", 1)[0])
                        append_last_batch(no)
                        print(" ", report.replace("\n", " "))
                    self._json({"ok": True, "no": no})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
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
            if self.path == "/engine-import":
                try:
                    with lock:
                        path, report = import_engine_send(data.get("parent"),
                                                          data.get("folder"))
                        print(" ", report.replace("\n", " "))
                    self._json({"ok": True,
                                "no": int(path.name.split(" ", 1)[0])})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/effects-stage":
                # the Effects button: the rack as set, no new number
                no = data.get("number")
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        picks = _clean_picks(no, data.get("picks"),
                                             _CACHE["shots"])
                        se_id = swap_many(no, picks, shots=_CACHE["shots"],
                                          trims=data.get("trims"),
                                          drops=data.get("drops"),
                                          pans=data.get("pans"), stage=True)
                    self._json({"ok": True, "se_id": se_id,
                                "engine": ensure_sound_engine()})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/engine-up":
                self._json({"ok": ensure_sound_engine()})
                return
            if self.path == "/rebuild":
                # the stem rack: several drums staged, one new beat out
                no = data.get("number")
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        picks = _clean_picks(no, data.get("picks"),
                                             _CACHE["shots"])
                        path, report = swap_many(no, picks,
                                                 shots=_CACHE["shots"],
                                                 trims=data.get("trims"),
                                                 drops=data.get("drops"),
                                                 pans=data.get("pans"),
                                                 fx=bool(data.get("fx")))
                        print(" ", report.replace("\n", " "))
                    self._json({"ok": True,
                                "no": int(path.name.split(" ", 1)[0]),
                                "se_id": _sound_engine_id(path, ROOT)})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/chunk":
                # songify: same staged rack as /rebuild, but the render
                # lands in the beat's Chunks folder and the rack stays
                # set so he can keep adding versions
                no = data.get("number")
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        picks = _clean_picks(no, data.get("picks"),
                                             _CACHE["shots"])
                        res = save_chunk(no, picks, shots=_CACHE["shots"],
                                         trims=data.get("trims"),
                                         drops=data.get("drops"),
                                         pans=data.get("pans"))
                        print(f"  chunk {res['count']}: {res['file']}")
                    self._json({"ok": True, **res})
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
            if self.path == "/ban":
                try:
                    with lock:
                        if "shots" not in _CACHE:
                            _CACHE["shots"] = build_shots()
                        res = ban_lane(data.get("number"),
                                       data.get("lane", ""),
                                       choice=data.get("choice"),
                                       shots=_CACHE["shots"])
                    if not res.get("asked"):
                        how = ("every file with that name"
                               if res["banned"] == "name" else "this sound")
                        print(f"  banned {res['name']} ({how})")
                    self._json({"ok": True, **res})
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            if self.path == "/sketch":
                # Song Sketch render. Takes the same lock as every other
                # render, so it never overlaps one (drive-starvation rule).
                try:
                    import song_sketch
                    no = int(data.get("no"))
                    sf = _sketch_folder(no, data.get("src"))
                    rows = song_sketch.rows_for(_beat_stems(no, folder=sf))
                    keep = set(data.get("lanes") or [r["lane"] for r in rows])
                    rows = [r for r in rows if r["lane"] in keep]
                    bpm = load_recipe(ROOT, no)["preset"].get("bpm")
                    with lock:
                        got = song_sketch.build(
                            no, bpm, rows,
                            lambda ln: _solo_audio(no, ln, folder=sf),
                            data.get("recipe") or {},
                            ref_rms=_beat_rms(no))
                    self._json({"ok": True, **got})
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
            key = data.get("key") or None
            notes = data.get("notes", "")
            loops_only = bool(data.get("loops_only"))
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
                                                shots=_CACHE["shots"],
                                                key=key,
                                                loops_only=loops_only)
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
            httpd = Server(("127.0.0.1", p), Handler)
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
