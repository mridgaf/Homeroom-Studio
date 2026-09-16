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
from groove import OWNER_TASTE
from make_drum_loops import SR, read_wav24, sub808, wav24_bytes, write_wav24
from make_drum_beats import ban_sound, build_shots, name_twins
from make_hiphop_tracks import load_audio
from crew import (BARS, CREW, GENRE_NAMES, LEGEND_NAMES, bars_of,
                  boom_bap_variant,
                  build_kit, is_dj, lock_stamps, normalize_preset,
                  render_crew_beat, sub_sidechain,
                  _LOW_END, _load_choked, _pick_path, _resolve_secs)
from beat_recipes import (history_avoid, lane_label, load_recipe,
                          record_history, save_recipe, write_midi,
                          write_stems)
from pattern_gen import (LIB_DIR, break_list, compose, free_beat,
                         load_library, _lib_lane)

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
    HOLE_P = 1 / 6.0
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
    elif rng.random() < HOLE_P:
        t = rng.choice(["thinbar", "frisson", "breath"])
    else:
        t = "bshift"
    if t == "thinbar":                       # a bar rests, canon breathes
        b = rng.choice(late)
        for ln in mutable:
            bars = barlist(ln)
            if ln in canon:
                bars[b] = bars[b].replace("X", "x")
            else:
                bars[b] = "-" * len(bars[b])
            rewrite(ln, bars)
        notes.append(f"bar {b + 1} drops out")
    elif t == "frisson" and nbars >= 2:      # build: thins, then slams
        for ln in mutable:
            bars = barlist(ln)
            if ln not in canon:
                bars[last - 1] = "-" * len(bars[last - 1])
            bars[last] = bars[last].replace("x", "X")
            rewrite(ln, bars)
        notes.append(f"build: bar {last} thins out, bar {last + 1} slams")
    elif t == "bshift" and nbars >= 2:       # a lane sits out a half
        cands = [ln for ln in mutable if ln not in canon and
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
        notes.append(f"lanes sit out the back half of bar {b + 1}")

    # 4c. OWNER RULE 2026-08-01: bar 1 always has a kick. Separate from the
    # gap rule and not covered by it — measured under 07-29, 1 beat in 20
    # started with no kick at all and 1 in 50 with no drums at all, because
    # the treatments above and the density pass could both empty bar 1. A
    # loop that starts on nothing is not usable as a loop. Restores only the
    # downbeat, and only when the whole bar came out empty, so a deliberately
    # syncopated opening bar is left alone.
    if "kick" in lanes:
        kbars = barlist("kick")
        if kbars and not _hits(kbars[0]):
            kbars[0] = "X" + kbars[0][1:]
            rewrite("kick", kbars)
            notes.append("kick restored on the downbeat")

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
    djs = sorted(n for n in CREW if is_dj(n) and n != name)
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
    if not bb and is_dj(name) and free_beat(variant):
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
        # 70/30 like a solo beat (owner 2026-09-14): the lane's parent's
        # taste in character, the whole library on a free beat
        path, x = _pick_path(shots, role, wants, secs, seed,
                             must=must, avoid=avoid,
                             open_bank=free_beat(variant))
        if path:
            avoid.add(path)
        kit[lane] = x
        sources[lane] = path
        spec_used[lane] = (role, must, wants, secs)
    kit["stamp"] = stamps[host][1]
    sources["stamp"] = f"{Path(stamps[host][0]).stem}  [{host}'s stamp]"
    for i, g in enumerate(names[1:]):
        kit[f"stamp{i + 2}"] = stamps[g][1]
        sources[f"stamp{i + 2}"] = f"{Path(stamps[g][0]).stem}  [{g}'s stamp]"
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
    ("kick", ("kick drums", "kick drum", "kicks", "kick")),
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
    ("bass", ("bass drums", "bass drum", "bass 808", "808 bass", "808s",
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


# "add the root" (owner rule 2026-07-18): ON. Retired 2026-07-23 as
# collateral of that morning's engine-wide 808 ban ("ignore previous push
# for 808"), then restored the same day once the ban itself was reversed
# ("allow DJs to stay true to style, with the kick") and the owner asked
# for the sub back explicitly. Round trip left no scar: the mechanism was
# flag-gated rather than deleted. Unreachable again 2026-07-25 to
# 2026-09-01 — not by this flag but by a "not chords" condition at the
# call site, once every identity gained chords_default. Fixed 2026-09-01:
# the sub now rides WITH the chords, tuned to the beat's own key.
ADD_THE_ROOT_808 = True

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
    """This beat's ONE low sound: "sub", "808", "bass", "brass", "kit" (the
    kit already carries it — a long 808 kick) or None.

    OWNER HARD RULE 2026-09-14, "don't pile lows on lows": the kick plus
    only ONE of sub / 808 / bass sample / low brass / the strings' basses.
    This is the single place it is decided, before anything that could add
    one: the strings read the answer (allow_basses) and the lanes add
    exactly what it says. generate() then refuses a second low lane outright.

    How OFTEN a beat has one is unchanged. In character this is the old
    rule verbatim: the tuned sub for SUB_DJS on a traditional beat without
    chords at 3 in 4, else the sampled 808 at SAMPLED_BASS_P. On a free beat
    (pattern_gen.free_beat) any DJ gets any low sound his library can play,
    at that same rate — "interchangeable with every DJ"."""
    if "kick" not in preset["lanes"]:
        return None
    if _holds_low_end(preset):
        return "kit"
    muted = "bass" in dirs.get("mute", set())
    sub_ok = ADD_THE_ROOT_808 and (ROOT_808_WITH_CHORDS or not dirs["chords"])
    if (sub_ok and traditional and dj in SUB_DJS
            and random.Random(variant * 577 + 13).random() < 0.75):
        voice = "sub"
    elif (shots.get("bass") and not muted
          and random.Random(variant * 907 + 31).random() < SAMPLED_BASS_P):
        voice = "808"
    else:
        return None
    if not (free_beat(variant) and is_dj(dj)):
        return voice
    options = [v for v, ok in (("sub", sub_ok),
                               ("808", bool(shots.get("bass")) and not muted),
                               ("bass", not muted and bool(_low_pool("bass"))),
                               ("brass", not muted and bool(_low_pool("brass"))))
               if ok]
    return random.Random(variant * 383 + 19).choice(options)


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
    preserved -- pedalboard's PitchShift, not a resample: a tape-speed
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
        semis = (pitch_class(key_root) - pitch_class(have)) % 12
    except (ValueError, AttributeError):
        return None, 0
    if semis > 6:
        semis -= 12
    if semis == 0:
        return audio, 0
    try:
        from pedalboard import PitchShift
        x = np.asarray(audio, dtype=np.float32)
        y = PitchShift(semitones=float(semis))(x.reshape(1, -1), SR)[0]
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
    # root into sample_808_index.json, so on a keyed beat the sample is
    # SHIFTED into the beat's key instead of being skipped (owner
    # 2026-09-07, asked and answered: "pitch-shift to the key").
    #
    # An 808 whose note could not be read (1 of 411) is still barred from a
    # keyed beat -- shifting by an unknown interval is worse than no 808.
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
        path, audio = _pick_path(shots, "bass", [], secs, variant * 71 + 5)
        if audio is not None and np.any(audio) and key_root:
            audio, semis = _808_to_key(path, audio, key_root)
            if audio is None:
                path = None                      # note unknown: no 808 here
            elif semis:
                vnotes.append("808 shifted %+d semitones to %s"
                              % (semis, key_root))
    if low in ("808", "bass", "brass"):
        if path is not None and audio is not None and np.any(audio):
            _pan, _g, (_o, _j, ksw, ks), kbars = preset["lanes"]["kick"]
            preset["lanes"]["bass"] = (0.0, 0.6, (0, 0, ksw, ks + 9),
                                       [b for b in kbars])
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


def _source_order(pref, rng, free=False):
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
    handles the case where they all do."""
    if free:
        import instrument_sampler
        every = sorted(set(instrument_sampler.VOICES) - {"chip"}
                       | {"strings", "loop", "midi"})
        primary = rng.choice(every)
        names = [s[0] for s in pref] if pref else ["loop", "synth"]
    elif not pref:
        return ("loop", "synth")
    else:
        names = [s[0] for s in pref]
        primary = _wpick(pref, rng)
    order = [primary] + [n for n in names if n != primary]
    if "synth" not in order:
        order.append("synth")
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
    order = _source_order(pref, random.Random(variant * 461),
                          free=free_beat(variant) and not preset.get("genre"))
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


def _roll_key(sig, variant, dirs, open_roll, srng):
    """(key root, mode, progression name or None) for one beat — the three
    harmonic dice _build_chords rolls, in the same order on the same `srng`.
    A reference track's key wins hard; a free beat rolls the whole pool
    (every progression, all twelve roots — owner 2026-09-14, "all keys
    available" — and every mode); otherwise the identity's own signature."""
    import harmony
    from key_context import MODES, SUB_ROOTS
    sig_key = sig.get("key") or {}
    forced = dirs.get("force_key")
    if forced:
        key_root, mode = forced
        prog = dirs["chord_feel"] or (
            _wpick(sig.get("progressions"), random.Random(variant * 419 + 5))
            or srng.choice(harmony.names()))
    elif open_roll:
        # SUB_ROOTS is only seven and stays that way for the in-character pick
        key_root = srng.choice(sorted(ROOT_HZ))
        mode = srng.choice(sorted(MODES))
        prog = dirs["chord_feel"] or srng.choice(harmony.names())
    else:
        key_root = _wpick(sig_key.get("roots"), srng) or srng.choice(SUB_ROOTS)
        mode = sig_key.get("mode", "minor")
        if isinstance(mode, list):                  # weighted mode list
            mode = _wpick(mode, srng)
        prog = dirs["chord_feel"] or _wpick(sig.get("progressions"),
                                            random.Random(variant * 419 + 5))
    return key_root, mode, prog


def _build_chords(preset, kit, sources, variant, dirs, vnotes, voice=None,
                  allow_basses=None):
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
    disclosed here rather than silently risked."""
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
    key_root, mode, prog = _roll_key(sig, variant, dirs, open_roll, srng)
    key = KeyContext(key_root, mode)
    prog_name, chords = harmony.compose(
        key, prog, rng=random.Random(variant * 419 + 5))
    num, den = preset.get("tsig", (4, 4))
    bar_s = num * (4.0 / den) * 60.0 / preset["bpm"]
    nb = bars_of(preset)
    # A progression longer than the loop has bars would silently lose its
    # tail below (`if start_bar >= nb: break`). Nothing in the pool is long
    # enough to hit that today — the longest is 4 chords and the shortest
    # loop is 4 bars — and tests/test_harmony.py pins it so a future 6-chord
    # progression fails loudly instead of arriving half-played.
    per_chord = max(1, nb // len(chords))
    pref = sig.get("chord_source")
    # "arp" = broken-chord riff, "sustain" = held block. A weighted list
    # rolls per beat (Dre's keepers were a mix of both — owner 2026-07-22).
    rhythm_spec = sig.get("chord_rhythm", "sustain")
    # underscored: _render_one below shadows this with its own `rhythm`
    # local (rhythm_override or _rhythm), so every voice can be overridden
    # independently — see _render_one's docstring.
    _rhythm = (_wpick(rhythm_spec, random.Random(variant * 733 + 11))
              if isinstance(rhythm_spec, list) else rhythm_spec)
    # ---- the chord PERFORMANCE grammar (owner build 2026-09-05) ----
    # Every DJ since 2026-09-14, arps half as often (chord_rhythm.spec_for);
    # genre presets still opt in with a top-level `chord_grammar` key. See
    # tools/chord_rhythm.py for why the figure is baked into the slot
    # buffer instead of written into the lane's bar string.
    _grammar = chord_rhythm.spec_for(
        preset, free=free_beat(variant) and not preset.get("genre"))
    # what the drums are already playing, so the "comp" figure can answer
    # them instead of doubling them. Read BEFORE any chord lane is added.
    _busy = {k: v[3] for k, v in preset["lanes"].items()
             if not k.startswith(("chord", "bass")) and len(v) > 3}
    # only pay for the melodic-loop library scan if a loop voice is on
    # the table (the default, a signature that lists "loop", or the owner
    # asking for it outright from the rack)
    # a free beat's lead voice can be ANY instrument (_source_order), so
    # both libraries have to be on the table for it
    free = open_roll and not preset.get("genre")
    want_loop = (not pref or any(s[0] == "loop" for s in pref)
                 or voice == "loop" or free)
    pool = chord_synth.sample_pool(key, preset["bpm"]) if want_loop else []
    # same "only scan if it's actually on the table" guard as want_loop
    # above, for the owner's MIDI chord packs (tools/midi_packs.py) —
    # one candidate file per beat, not per chord slot, same reasoning as
    # loop_voice's own pool[:3] top-candidates convention.
    want_midi = (pref and any(s[0] == "midi" for s in pref)) or voice == "midi" or free
    midi_prog, midi_pick_name = None, None
    if want_midi:
        m_pool = chord_synth.midi_pool(key)
        if m_pool:
            m_pick = random.Random(variant * 967).choice(m_pool[:3])
            midi_prog = chord_synth.midi_progression(m_pick, key)
            midi_pick_name = m_pick["name"]
    strings_idx = None
    if voice == "strings" or free or (
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
        # one low sound per beat: the basses only play when nothing else
        # holds the low end. generate() decides that before the chords and
        # passes it in; a rebuild reads it off the saved lanes.
        if allow_basses is None:
            allow_basses = not _holds_low_end(preset)
        strings_idx = string_sampler.beat_pool(s_all, s_style, s_mic,
                                               basses=allow_basses)
    # every non-strings, non-loop voice is now a SAMPLED instrument out of
    # his own banks (owner 2026-07-23) — "synth" included, so this index is
    # needed for essentially every signature, not just the horn one.
    import instrument_sampler
    inst_idx = instrument_sampler.scan()
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
        _all_notes = sorted({n for c in chords for n in c["notes"]})
        if voice == "strings" and strings_idx:
            forced_idx = _best_folder(
                strings_idx, {e.get("group") for e in strings_idx},
                _all_notes)
            if forced_idx:
                strings_idx = forced_idx
        elif voice in instrument_sampler.VOICES:
            forced_idx = _best_folder(       # [:1] — the named group only
                inst_idx, instrument_sampler.VOICES[voice][:1], _all_notes)
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
    for i, chord in enumerate(chords):
        start_bar = i * per_chord
        if start_bar >= nb:
            break
        end_bar = nb if i == len(chords) - 1 else \
            min(start_bar + per_chord, nb)
        slots.append((i, chord, start_bar, (end_bar - start_bar) * bar_s))

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
        notes = notes if notes is not None else chord["notes"]
        # "midi" swaps in a real chord someone else already wrote in
        # place of harmony.compose()'s notes, cycling through the
        # picked file's own progression by slot — the same way a
        # normal progression's 2-4 chords already cycle across a beat
        # (see per_chord below). No audio here: a MIDI file is silent
        # by itself, so it still needs a sampled voice to sound —
        # forced to "synth" (owner 2026-07-23: no synthesized chord
        # voice, everything sampled from his own banks).
        midi_groups = None
        if src == "midi":
            if not midi_prog:
                return None, None
            _, _, notes = midi_prog[slot % len(midi_prog)]
            midi_groups = instrument_sampler.VOICES["synth"]
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
            figure, bars, shape = chord_rhythm.gen_figure(
                _grammar, rng, nbars, busy=_busy)
            a = chord_rhythm.render_figure(
                bars, dur, preset["bpm"], notes, render_note, render_chord,
                figure=figure, shape=shape, spec=_grammar,
                seed=variant * 101 + slot)
            # Silence means his library couldn't voice a single step of
            # the figure. Hand back None so the OLD arp/sustain path gets
            # its own try, rather than failing the whole plan — the
            # grammar is a way of playing these notes, not a gate on them.
            if a is None or not np.max(np.abs(a)) > 0:
                return None
            return a, figure
        if src == "strings" and strings_idx:
            cache = {}                           # one load per note, not step
            got = _fig(
                lambda nt, sd: string_sampler.note_slice(
                    strings_idx, nt, sd, cache=cache, used=used, pin=pin),
                lambda ns, sd: string_sampler.play_chord(
                    strings_idx, ns, sd, used=used, pin=pin))
            if got:
                return got[0], "strings %s" % got[1]
            if rhythm == "arp":
                a = chord_synth.arp_riff(
                    notes, dur, preset["bpm"],
                    lambda nt, sd: string_sampler.note_slice(
                        strings_idx, nt, sd, cache=cache, used=used,
                        pin=pin))
                return a, "strings arp"
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
            # header. Always arpeggio-fused: the NES had two pulse voices,
            # so a held triad was IMPOSSIBLE and chords were always faked
            # by flicking between the notes. Honouring rhythm="sustain"
            # here would be less authentic, not more.
            import chip_synth
            # Two optional identity knobs, both New Math's (2026-07-24):
            # chip_tuning "atari" -> the TIA's integer-divider grid, out
            # of tune on purpose; chip_count -> notes per beat.
            tuning = sig.get("chip_tuning", "equal")
            per_beat = sig.get("chip_count")
            rate = (chip_synth.count_rate(preset["bpm"], per_beat)
                    if per_beat else chip_synth.NTSC_FRAME_HZ / 3.0)
            a = chip_synth.chip_chord(notes, dur,
                                      tuning=tuning, rate_hz=rate)
            return a, ("chiptune arp%s"
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
            if rhythm == "arp":
                a = chord_synth.arp_riff(
                    notes, dur, preset["bpm"],
                    lambda nt, sd: instrument_sampler.note_slice(
                        idx, nt, sd, cache=cache, groups=groups,
                        used=used, pin=pin))
                return a, "%s stabs" % gname
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
    order = _source_order(pref, random.Random(variant * 461),
                          free=free_beat(variant) and not preset.get("genre"))
    plan_rng = random.Random(variant * 883 + 7)
    own = [s[0] for s in pref] if pref else []
    plans = [(s,) for s in order]
    # then every OTHER instrument group he owns. "chip" is excluded on
    # purpose: it is the one generated voice, so it may only play for an
    # identity whose own chord_source asks for it (New Math, Chiptune,
    # Farrow's 1-in-6) — never as a substitute for his instruments.
    # Without this it became a universal fallback that always succeeds,
    # which is the opposite of the owner's hard rule (2026-07-25).
    extra = [g for g in instrument_sampler.VOICES
             if g not in order and g != "chip"]
    plan_rng.shuffle(extra)
    plans += [(g,) for g in extra]
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
    # HARD RULE (owner 2026-07-29, overrides the 2026-07-25 rule below):
    # exactly one melodic voice, always — no stacking whatsoever, not even
    # the chip voice, no rare "extra" third part. The weighted 1/2/3-part
    # roll that used to live here is gone; part_count stays 1, which makes
    # the multi-part render path below (part_count >= 2) unreachable. Kept
    # rather than torn out in case this ever comes back — see
    # theory/arrangement.md and the now-dormant OWNER_TASTE weights.
    part_count = 1

    if part_count >= 2:
        role_srcs = _role_sources(primary, order, own, part_count)
        role_beds, role_ok = [], True
        for i, chord, start_bar, dur in slots:
            support_n, lead_n, passing_n = _split_chord_roles(chord["notes"])
            if not lead_n:               # nothing left to split (e.g. a
                role_ok = False          # bare power chord) — not a
                break                    # multi-part beat after all
            layers = []
            used_s = []
            a_s, nm_s = _render_one(role_srcs[0], chord, dur, used=used_s,
                                    notes=support_n, slot=i,
                                    rhythm_override="sustain")
            if a_s is None or not np.max(np.abs(a_s)) > 0:
                role_ok = False
                break
            layers.append((a_s, "%s (support)" % nm_s, used_s))
            used_l = []
            a_l, nm_l = _render_one(role_srcs[1], chord, dur, used=used_l,
                                    notes=lead_n, slot=i)
            if a_l is None or not np.max(np.abs(a_l)) > 0:
                role_ok = False
                break
            layers.append((a_l, "%s (lead)" % nm_l, used_l))
            # passing is never fatal — a plain triad has no note to spare
            # for it, and even when a chord has one, it only plays SOME
            # of the time (owner: "the sparsest, easiest to cut"). Rolled
            # per slot so it can appear on one chord and rest on the next.
            if (part_count >= 3 and passing_n and random.Random(
                    variant * 991 + 43 + i).random()
                    < OWNER_TASTE["passing_note_p"]):
                used_p = []
                a_p, nm_p = _render_one(role_srcs[2], chord, dur,
                                        used=used_p, notes=passing_n,
                                        slot=i, rhythm_override="sustain")
                if a_p is not None and np.max(np.abs(a_p)) > 0:
                    layers.append((a_p, "%s (passing)" % nm_p, used_p))
            g = _balance_layers([a for a, _, _ in layers],
                                chord_synth.PEAK_CEILING)
            n = min(len(a) for a, _, _ in layers)
            role_beds.append([(a[:n] * g if g != 1.0 else a[:n], nm, fl)
                              for a, nm, fl in layers])
        if role_ok:
            committed, beds = tuple(role_srcs), role_beds

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
            if ok and beds:
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
    bass_idx = instrument_sampler.scan_bass()
    bass_beds, bass_files, bcache = {}, {}, {}
    if bass_idx:
        for i, chord, start_bar, dur in slots:
            bused = []
            a = instrument_sampler.voice_note(
                bass_idx, chord["notes"][0] - 12, dur, cache=bcache,
                used=bused)
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
        preset["lanes"][f"bass{i}"] = (0.0,
                                       old_b[1] if old_b
                                       else _BASS_GAIN * accent,
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
                # SAME feel seed for every voice of a slot, so two
                # layers of one chord land together. The lane feel tuple
                # stays (0, 0, 50): a chord lane's single X triggers the
                # WHOLE slot buffer, so lane-level offset/jitter/swing
                # would shift the entire block, not its hits. Since
                # 2026-09-05 the performance — hits, swing, jitter,
                # written dynamics — is baked INSIDE that buffer by
                # chord_rhythm for identities that opted in; see its
                # header for why it can't live out here.
                preset["lanes"][lane] = (_chord_pan,
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
        midi_chords.append({"start_sec": start_bar * bar_s,
                            "dur_sec": dur,
                            "notes": chord["notes"] + [bass_note]})
        chord_rows.append({"bar": start_bar + 1,      # 1-based, as counted
                           "roman": chord["roman"],
                           "chord": chord["chord"],
                           "notes": list(chord["notes"]),
                           "bass": bass_note,
                           "voice": voice_desc})
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
    harmony_info = {"key": str(key), "root": key_root, "mode": mode,
                    "progression": prog_name, "rhythm": _rhythm,
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
                    "voice_names": dict(voice_names)}
    return midi_chords, harmony_info


def _pick_loop_bed(dj_name, preset, dirs, key, shots, variant):
    """Whole-beat-from-loops (owner 2026-09-16 correction: "I want the
    loops. Option to make whole beats. using only loops."). Picks ONE
    drum loop and ONE melodic loop for this DJ, on the same weighted
    taste-roll every DJ already uses (loop_mode.pick_loop), pitch-fits
    the melodic pick into the beat's key, and repeats whichever is
    shorter until both match (loop_mode.match_lengths) rather than
    stretching or cropping either one.

    Returns (sources, loop_bufs, nbars): `sources` names the two loop
    files (for the recipe/README/stems, same as a one-shot's source
    path); `loop_bufs` is {"kick": mono, "chord0": mono} ready for
    render_crew_beat's loop_bufs override — those two lane names are
    reused on purpose (not new lane names) so the existing mix bus
    (kick_dist, reverb space, mix EQ, glue, master) treats them exactly
    like it would a normal beat's kick and chord lanes. No sidechain
    duck for these lanes (owner 2026-09-16: skip it, revisit if it
    sounds muddy) — that falls out for free, since duck() only fires at
    onsets["kick"] positions and a loop lane's onsets list is left
    empty rather than faked."""
    import loop_mode
    import melodic_loops
    import sample_library
    from key_context import KeyContext

    sig = preset.get("signature") or {}
    srng = random.Random(f"{dj_name}|loopbed|{variant}")
    want_key = clean_key(key)
    key_root, mode, _prog = _roll_key(
        sig, variant,
        {"force_key": want_key or dirs.get("force_key"), "chord_feel": None},
        open_roll=False, srng=srng)
    kctx = KeyContext(key_root, mode)

    drum_pool = sample_library.loops_scored(
        shots, tags=[t for t, _w in (preset.get("library") or {}).get("tags", [])],
        bpm=preset.get("bpm"))
    drum_entry, drum_taste = loop_mode.pick_loop(sig, drum_pool, srng)
    if drum_entry is None:
        raise FileNotFoundError(
            "No drum loops found for a loops-only beat — check the loop "
            "pool is mounted (drive unplugged?).")
    mel_pool = melodic_loops.in_key_scored(melodic_loops.scan(), kctx,
                                           bpm=preset.get("bpm"))
    mel_entry, mel_taste = loop_mode.pick_loop(sig, mel_pool, srng)
    if mel_entry is None:
        raise FileNotFoundError(
            "No melodic loops found for a loops-only beat — check the "
            "loop pool is mounted (drive unplugged?).")

    drum_x = load_audio(drum_entry["path"])
    mel_x = load_audio(mel_entry["path"])
    if drum_x is None or not len(drum_x):
        raise FileNotFoundError(f"Couldn't read {drum_entry['path']}")
    if mel_x is None or not len(mel_x):
        raise FileNotFoundError(f"Couldn't read {mel_entry['path']}")
    drum_mono = drum_x.mean(axis=1)
    mL, mR = mel_x[:, 0].copy(), mel_x[:, 1].copy()
    if mel_entry.get("key"):
        src_key = KeyContext(mel_entry["key"], mel_entry.get("mode") or "major")
        secs = len(mL) / SR
        mL = melodic_loops.fit_loop(mL, SR, secs, src_key, kctx)
        mR = melodic_loops.fit_loop(mR, SR, secs, src_key, kctx)
    mel_mono = (mL + mR) / 2

    loop_bufs, nbars = loop_mode.match_lengths(
        {"kick": drum_mono, "chord0": mel_mono}, SR, preset["bpm"],
        tuple(preset.get("tsig", (4, 4))))
    sources = {"kick": drum_entry["path"], "chord0": mel_entry["path"]}
    note = (f"loops only, {nbars} bars in {kctx}: drum loop "
           f"'{Path(drum_entry['path']).stem}' ({'on-taste' if drum_taste else 'free pick'})"
           f" + melodic loop '{Path(mel_entry['path']).stem}' "
           f"({'on-taste' if mel_taste else 'free pick'})")
    return sources, loop_bufs, nbars, note


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
    _pick_loop_bed. One DJ at a time for now; a collab raises, since
    whose loop taste should win hasn't been asked yet."""
    seen = set()                                  # dedupe, KEEP caller order
    names = [n for n in names
             if n in CREW and not (n in seen or seen.add(n))]
    if not names:
        raise ValueError("Check at least one DJ first.")
    if loops_only and len(names) != 1:
        raise ValueError("Loops-only beats are one DJ at a time for now.")
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
    rng = random.Random(variant)
    title = fresh_title(names, rng, root)

    loop_bufs, loop_nbars = None, None
    if loops_only:
        status(f"Picking loops for {names[0]}…")
        sources, loop_bufs, loop_nbars, loop_note = _pick_loop_bed(
            names[0], preset, dirs, key, shots, variant)
        kit, spec_used, lane_parent = {}, {}, {}
        preset = dict(preset)                # don't mutate CREW's shared dict
        preset["lanes"] = {
            "kick": (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),)),
            "chord0": (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),)),
        }
        # the one-shot vnotes above (groove seed, kick/snare flavor...)
        # describe a composition that's about to be thrown away — none
        # of it plays. Report what actually sounds instead.
        vnotes = [loop_note]
    elif len(names) == 1:
        status(f"Building the kit for {' x '.join(names)}…")
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
        space = random.Random(variant * 941 + 7).choices(
            ["gated", "dry", "room", "plate"], [0.35, 0.35, 0.2, 0.1])[0]

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
        low = _low_voice(preset, variant, dirs, traditional, names[0], shots)
        midi_chords, harmony_info = _build_chords(preset, kit, sources, variant,
                                                  dirs, vnotes,
                                                  allow_basses=low is None)

        # ...and NOW the tuned root 808, moved below _build_chords so that on a
        # chords beat it can be tuned to THAT BEAT'S KEY rather than skipped.
        # Which of those two happens is ROOT_808_WITH_CHORDS, and with the flag
        # off this is byte-identical to the old position: _build_chords returns
        # immediately when there are no chords, and the sub's dice are their own
        # seeded generators, so nothing upstream shifts by moving the call.
        if low == "sub":
            root_note = _add_root_sub(
                preset, kit, sources, variant, vnotes,
                harmony_info=harmony_info if ROOT_808_WITH_CHORDS else None,
                traditional=traditional, dj=names[0], decided=True)

        # phase 2 (owner 2026-07-23): sampled bass/808 and vocals get their lanes
        # here, after the chord lanes so bass can defer to the harmony bass on a
        # 'chords' beat.
        _add_sample_lanes(preset, kit, sources, shots, variant, dirs, vnotes,
                          key_root=(harmony_info or {}).get("root"), low=low)
        _refuse_second_low(preset, kit, sources, vnotes)

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
    write_stems(folder / f"{no} {' x '.join(names)} {title} Stems",
                parts["stems"], sources=sources)

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
        "kit_paths": (dict(sources) if loops_only
                     else {ln: sources[ln] for ln in spec_used}),
        "loops_only": loops_only,
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
    write_stems(folder / f"{no} {title} Stems", parts["stems"],
               sources=sources)
    spec_used = {ln: (r, m, w, _resolve_secs(s, preset["num"], idx))
                for ln, (r, m, w, s) in preset["kit"].items()}
    save_recipe(root, no, {
        "file": fname, "folder": "Fixed Bank", "names": ["Fixed Bank"],
        "title": title, "variant": idx, "bpm": preset["bpm"],
        "space": "dry", "preset": _shareable_preset(preset),
        "kit_spec": spec_used,
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
    write_stems(folder / f"{no} {title} Stems", parts["stems"],
               sources=sources)
    spec_used = {ln: (r, m, w, _resolve_secs(s, preset["num"], variant))
                for ln, (r, m, w, s) in preset["kit"].items()}
    save_recipe(root, no, {
        "file": fname, "folder": label, "names": [label],
        "title": title, "variant": variant, "bpm": preset["bpm"],
        "space": "dry", "preset": _shareable_preset(preset),
        "kit_spec": spec_used,
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


def _change_words(lanes, trims, drops, chord_voice=None):
    """How a staged set of rack changes reads: `what` is the short title
    that becomes part of a filename, `changed` is the sentence for the
    log. Split out of swap_many so the chunk folder names its files with
    the same words the rebuild uses — one place to change the wording.

    A family removal is 4 lanes but ONE musical change — say "Chords",
    not "Chord0 & Chord1 & Chord2 & Chord3"."""
    said = [ln for ln in drops if not _chord_family(ln)]
    if any(_CHORD_LANE.match(ln) for ln in drops):
        said.append("chords")
    if any(_CHORD_BASS_LANE.match(ln) for ln in drops):
        said.append("chord bass")
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
        return "New Mix", _trim_words(trims)
    if len(lanes) == 1:
        return f"New {lanes[0].capitalize()}", lanes[0]
    if len(lanes) == 2:
        return (f"New {lanes[0].capitalize()} & {lanes[1].capitalize()}",
                " and ".join(lanes))
    return "Rebuilt", ", ".join(lanes)


def swap_many(number, picks, root=ROOT, shots=None, status=lambda msg: None,
              trims=None, drops=None, render_only=False):
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
    what Rebuild will print, not an approximation of it."""
    number = int(number)
    rec = load_recipe(root, number)
    picks = {str(ln).strip().lower(): v for ln, v in (picks or {}).items()}
    drops = sorted({str(ln).strip().lower() for ln in (drops or [])})
    # "chords"/"bass" are FAMILY names from the rack: one row standing for
    # chord0..chordN. Expand them to the real lanes so a removal takes the
    # whole instrument out at once (owner 2026-07-25) — a per-bar removal
    # would make it drop out mid-beat.
    all_lanes = list(normalize_preset(rec["preset"]).get("lanes", {}))
    fam_drops = []
    for fam in (CHORD_FAM, CHORD_BASS_FAM):
        if fam in drops:
            drops.remove(fam)
            fam_drops += _family_members(fam, all_lanes)
    # A pick on a harmony row names an INSTRUMENT, not a file (owner
    # 2026-08-04). It leaves `picks` here — there is no kit_paths entry
    # to swap — and is handed to _build_chords below as the voice to try
    # first. Only the chord family takes one: the bass line is his to
    # play (2026-07-29), so its lanes are never rendered.
    chord_voice = None
    for fam in [f for f in list(picks) if _family_members(f, all_lanes)]:
        want = picks.pop(fam)
        if want and want not in {c["path"] for c in _chord_voices()}:
            raise ValueError(f"'{want}' isn't an instrument in your library.")
        chord_voice = want or chord_voice
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
    for lane in drops:                        # a drop wins over the rest
        picks.pop(lane, None)
        trims.pop(lane, None)
    if set(rec["kit_spec"]) <= set(drops):
        raise ValueError("That would remove every drum — keep at least "
                         "one.")
    if not picks and not trims and not drops and not chord_voice:
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
    chord_sources = {}          # lane -> what to CALL it in the stems folder
    # the tuned root sub is synthesized, not a sample — rebuild it from
    # the recipe's root note so the swapped beat keeps its low end
    if rec.get("root_note") and "sub" in preset.get("lanes", {}):
        kit["sub"] = sub808(ROOT_HZ.get(rec["root_note"], 43.65), 0.6)
        # ...and it must still SAY what it is. generate() names this stem
        # "bass drum - synth 808 sub, root F" (see the sources line in
        # generate); without this a swap printed a bare "bass drum.wav".
        chord_sources["sub"] = "synth 808 sub, root %s" % rec["root_note"]
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
        _dirs = {"chords": True, "chord_feel": None}
        if REBUILD_LOCKS_KEY:
            _h = rec.get("harmony") or {}
            _dirs["chord_feel"] = _h.get("progression")
            if _h.get("root") and _h.get("mode"):
                _dirs["force_key"] = (_h["root"], _h["mode"])
        _build_chords(preset, kit, chord_sources, rec["variant"],
                      _dirs, [], voice=chord_voice)
        # ...but a chord/bass lane the owner just REMOVED must not come
        # back: _build_chords rebuilds the whole family from the recipe's
        # variant, which would silently undo the removal.
        for lane in drops:
            preset["lanes"].pop(lane, None)
            kit.pop(lane, None)

    lanes = sorted(picks)
    what, changed = _change_words(lanes, trims, drops, chord_voice)
    status(f"Re-rendering beat {number} with the new {changed}…")
    L, R, lufs, parts = render_crew_beat(names[0], kit, space=rec["space"],
                                         preset=preset, want_parts=True)
    if rec.get("dj_cut_bar") is not None:
        L, R = dj_cut(L, R, parts, rec["dj_cut_bar"])

    if render_only:            # live preview — nothing is printed or filed
        return L, R

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
                sources={**chord_sources, **kit_paths, **rec["stamp_paths"]})

    rec2 = dict(rec, file=fname, kit_paths=kit_paths, parent=number,
                folder=rec["folder"], date=str(date.today()))
    if drops:                    # the lane is gone from the child recipe
        rec2["kit_spec"] = {ln: s for ln, s in rec["kit_spec"].items()
                            if ln not in drops}
    if trims or drops:           # the new gains/lanes ARE this beat
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
        f.write(f"  LUFS {lufs:.1f}\n")
    bits = [f"{ln} → {Path(kit_paths[ln]).name}" for ln in lanes]
    if trims:
        bits.append(_trim_words(trims))
    report = (f"{fname}\n-> {rec['folder']} folder | same beat as "
              f"{number} | {' | '.join(bits)} | LUFS {lufs:.1f}")
    return path, report



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


def chunk_dir(no, root=None):
    """Where beat `no` keeps its arrangement chunks. Sits next to the
    beat's own wav and its Stems folder (owner 2026-09-01), so nothing
    new appears in the library root and the numbering is untouched."""
    w = beat_wav(no, root)
    if w is None:
        raise ValueError(f"No beat {no} to chunk.")
    return w.parent / f"{w.stem} Chunks"


def save_chunk(number, picks=None, root=ROOT, shots=None,
               status=lambda msg: None, trims=None, drops=None):
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
                     status=status, trims=trims, drops=drops,
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
    chords = h.get("chords") or []
    return {"key": h.get("key"),
            "progression": prog.get("label") or h.get("progression"),
            "roman": " – ".join(c["roman"] for c in chords),
            "chords": " ".join(c["chord"] for c in chords),
            "voices": ", ".join(h.get("chord_source") or []),
            "why": prog.get("why")}


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
    if len(rel.parts) != 1 or " Drums " not in wav.stem:
        return None
    return f"{rel.parts[0]}/{wav.stem.split(' Drums ')[0]}"


def _batch_beats(root=None):
    """The last batch's tracks with their current location, for the
    player. Missing files (moved by hand) are skipped."""
    root = Path(root or ROOT)
    beats = []
    for no in _load_state().get("last_batch", []):
        w = beat_wav(no, root)
        if w:
            beats.append({"no": int(no), "label": w.stem,
                          "loc": beat_location(no, root),
                          "se_id": _sound_engine_id(w, root),
                          "theory": _beat_theory(no, root)})
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
    return None


def _family_members(fam, lanes):
    """Every real lane a family row stands for, in bar order."""
    return sorted((ln for ln in lanes if _chord_family(ln) == fam),
                  key=lambda ln: int((_CHORD_LANE.match(ln)
                                      or _CHORD_BASS_LANE.match(ln)).group(1)))


def _fam_sort(fam):
    """Instrument rows in playing order: the chord instruments (chords,
    chords2, …) and then the bass line."""
    return (fam == CHORD_BASS_FAM, len(fam), fam)


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
    names = [lane_label(lane), lane]
    for f in sorted(folder.glob("*.wav")):
        if any(f.stem == n or f.stem.startswith(n + " - ") for n in names):
            return f
    return None


def _beat_stems(no, root=None):
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
    folder = _stems_dir(no, root)     # walk the library once, not per lane
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
            "label": lane_label(lane),
            "role": spec[0] if spec else lane,
            "sample": Path(path).stem if path else "built from scratch",
            "pack": _pack_of(path),
            # a lane with no file behind it stays locked (the tuned 808
            # "sub" is the case) — only the chord/bass families below are
            # deliberately unlocked for removal
            "locked": locked or not path,
            "can_swap": bool(path) and not locked,
            "why": ("the DJ's producer tag — same in every beat they make"
                    if locked else
                    "synthesised, not a sample" if not path else ""),
            "stem": bool(_stem_wav(no, lane, root, folder=folder)),
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
            label = "bass"
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
            "can_swap": True,
            "voices": True,          # the dropdown lists instruments
            "why": why,
            "members": sorted(members, key=_lane_sort),
            "stem": bool(_stem_wav(no, members[0], root, folder=folder)),
        })
    return out


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
    gone = [b.strip().lower()
            for b in str(q.get("drop", [""])[0] or "").split(",") if b.strip()]
    L, R = swap_many(no, clean, root=Path(root or ROOT), shots=shots,
                     trims=trims, drops=gone, render_only=True)
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


def _chord_voices(rec=None):
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
        idx = instrument_sampler.scan()
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
        sidx = string_sampler.scan()
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


def _lane_candidates(no, lane, shots=None, root=None):
    """Every sample in the library that could fill this lane, grouped by
    pack for the dropdown. Also the allow-list the rebuild validates
    against: a path the client sends back is only ever accepted if it
    came from here, so no client string reaches disk unchecked."""
    root = Path(root or ROOT)
    rec = load_recipe(root, int(no))
    lane = str(lane).strip().lower()
    # a harmony row ("chords", "chords2", "chordbass") is an INSTRUMENT
    # row, not a file row — it offers voices instead of samples
    if _family_members(lane, rec["preset"].get("lanes", {})):
        return _chord_voices(rec)
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
    Homeroom Studio — reskinned 2026-08-06 to mockup D ("Show Flyer"):
    paper + halftone, blue ink, yellow highlight, poster-condensed type.
    Owner picked D after reviewing A-G, then asked for it live on both
    rooms (Beat Machine + Reason Voice). Same palette shape as before —
    the mark's yellow scrawl and blue square carry every accent — just
    flipped from dark xerox paper to light flyer stock.
    ---------------------------------------------------------------- */
 :root {
   --paper:   #f4ecc4;
   --card:    #fffef4;
   --card2:   #ffffff;
   --line:    #1020a826;
   --line2:   #1020a845;
   --text:    #12157f;
   --dim:     #12157f99;
   --dimmer:  #12157f66;
   /* straight off the Back of the Class mark: the yellow scrawl and the
      blue square it sits on — verbatim, "keep the blue and yellow no
      matter what" (owner, 2026-08-06). --co/--ch used to be lifted
      tints for a dark background; on paper the ink blue reads fine on
      its own, so both now just alias --blue.                         */
   --hi:      #e8d810;   /* band yellow — actions, keeps, selection    */
   --hi-ink:  #16150a;
   --blue:    #1020a8;   /* band blue — masthead, fills, blocks, ink   */
   --co:      #1020a8;
   --no:      #ff4d4d;   /* trash + real errors only                   */
   --ch:      #1020a8;
   --display: "Anton", Impact, "Haettenschweiler", sans-serif;
   --mono:    "Space Mono", ui-monospace, "SF Mono", Menlo, monospace;
 }
 * { box-sizing: border-box; }
 html { -webkit-text-size-adjust: 100%; }
 @import url('https://fonts.googleapis.com/css2?family=Anton&family=Space+Mono:wght@400;700&display=swap');
 body {
   font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif;
   margin: 0; padding: 0 24px 90px;
   background: radial-gradient(circle, #1020a814 1px, transparent 1.4px) 0 0/16px 16px,
               var(--paper);
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
 /* MAKE / STUDIO — one app, two rooms (packaging step 5). Plain links on
    purpose; no iframes until the simple version has been lived with. */
 .apptabs { position: absolute; top: 0; right: 0; z-index: 2; display: flex; }
 .apptabs a, .apptabs .here {
   font-family: var(--display); font-weight: 700; font-size: 13.5px;
   letter-spacing: .13em; text-transform: uppercase;
   padding: 10px 20px 12px; text-decoration: none; }
 .apptabs .here { background: var(--hi); color: var(--hi-ink);
                  border-radius: 0 0 0 14px; }
 .apptabs a { color: #ffffffb8; background: #00000026;
              border-radius: 0 18px 0 0; }
 .apptabs a:hover { color: #fff; background: #00000042; }
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
 .dj.legend:has(input:checked) { border-color: var(--co); background: #1020a814; }
 .dj.legend:has(input:checked) .dot { background: var(--co); border-color: var(--co); }
 .dj.legend:has(input:checked) .ord { background: var(--co); color: #fff; }
 /* the third box gets CHALK rather than a fourth hue — the mark only
    owns yellow and blue, and chalk on a board is the one other colour
    this band already has (crew = yellow scrawl, legends = blue, styles
    = chalk). */
 .dj.genre:has(input:checked) { border-color: var(--ch); border-style: dashed; background: #1020a80c; }
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
                background: var(--card2); color: var(--text); font-family: inherit; }
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

 /* ------------------------------------------- reference track (sec. 5) */
 #refdrop { border: 1.5px dashed var(--line2); border-radius: 10px;
            padding: 11px 12px; text-align: center; font-size: 12.5px;
            color: var(--dim); cursor: default;
            transition: background .12s, border-color .12s, color .12s; }
 #refdrop.over, #refdrop.busy { border-color: var(--co); color: var(--co);
                                background: #7d8cff14; }
 /* the row is its own grid: the two key dropdowns need more than the
    132px column the tempo box sits in, and the drop target needs the
    rest of the width or its one sentence wraps into three lines. */
 .refrow { grid-template-columns: 264px 1fr; }
 #refline { min-height: 15px; }
 #refline b { color: var(--ink); }
 #refline button { font-size: 11px; padding: 1px 7px; margin-left: 5px;
                   vertical-align: baseline; }

 #empty { padding: 34px 0 10px; text-align: center; position: relative; }
 #empty .ghost { width: 132px; margin: 0 auto 4px; opacity: .13;
                 transform: rotate(-3deg); }
 #empty .ghost img { width: 100%; display: block; }
 #empty .scribble { font-family: var(--display); font-weight: 700;
                    font-size: 38px; letter-spacing: .04em; color: #1020a812;
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
       border: 1px solid var(--line2); background: #1020a80a;
       color: var(--text); cursor: pointer; font-size: 11px;
       display: grid; place-items: center; transition: all .12s; }
 .pp:hover { background: #1020a81c; }
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
       background: #1020a808; color: var(--text); transition: all .12s; }
 .acts button:hover { background: #1020a817; }
 .acts button.on-fav   { border-color: var(--hi); color: var(--hi); }
 .acts button.on-trash { border-color: var(--no); color: var(--no); }
 .stembtn { font-family: var(--display); font-weight: 600; font-size: 12.5px;
            letter-spacing: .09em; text-transform: uppercase; padding: 8px 12px;
            white-space: nowrap; }
 .stembtn.open { background: var(--hi); color: var(--hi-ink); border-color: var(--hi); }

 /* ------------------------------------- why this beat works (step 3) */
 .theory { display: none; border-top: 1px solid var(--line);
           padding: 9px 14px 11px; background: #1020a805; }
 .tline { font-family: var(--mono); font-size: 11.5px; color: var(--dimmer);
          display: flex; flex-wrap: wrap; gap: 7px; align-items: baseline; }
 .tline b { color: var(--hi); font-weight: 700; }
 .tline i { color: var(--line); font-style: normal; }
 .tline .rom { color: var(--dim); }
 .twhy { margin-top: 6px; font-size: 12.5px; line-height: 1.5;
         color: var(--dim); max-width: 66ch; }

 /* -------------------------------------------------- the stem rack */
 .rack { display: none; border-top: 1px solid var(--line);
         background: #1020a80d; padding: 4px 14px 14px; }
 .rack.open { display: block; }
 .lane { display: grid; grid-template-columns: 74px 1fr auto auto;
         gap: 12px; align-items: center; padding: 10px 0;
         border-bottom: 1px solid #1020a80c; }
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
       background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='7'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%231020a8' stroke-width='1.6' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
       background-repeat: no-repeat; background-position: right 9px center; }
 .lane select:focus { outline: none; border-color: var(--hi); }
 .lane.changed select { border-color: var(--hi); }
 .lane .mini { font-size: 13px; line-height: 1; padding: 7px 8px;
       border: 1px solid var(--line); border-radius: 8px; cursor: pointer;
       background: #1020a808; color: var(--text); }
 .lane .mini:hover { background: #1020a817; }
 .lane .mini.playing { border-color: var(--co); color: var(--co); }
 .lane .lock { font-size: 11.5px; color: var(--dimmer); font-style: italic; }

 /* the stem faders — one per lane, so the rack reads down like a mixer */
 /* volume: 1 dB arrows, not a slider (owner 2026-07-25 — the slider
    jumped and left gaps). The dB readout doubles as the reset button. */
 .lane .vol { display: flex; align-items: center; gap: 2px; flex: none; }
 .lane .vol .step { width: 26px; height: 26px; padding: 0; line-height: 1;
       font-size: 15px; font-weight: 700; border-radius: 7px;
       border: 1px solid var(--line2); background: var(--card2);
       color: var(--text); cursor: pointer; }
 .lane .vol .step:hover { border-color: var(--hi); color: var(--hi); }
 .lane .vol .step:active { transform: translateY(1px); }
 .lane .vol .db { font-family: var(--mono); font-size: 12px;
       color: var(--dimmer); width: 40px; text-align: center;
       cursor: pointer; user-select: none; }
 .lane.trimmed .vol .db { color: var(--hi); }
 .lane.trimmed .swatch { background: var(--hi); }
 /* a stem staged for removal reads as struck-through and faded */
 /* the ban prompt: three real buttons, because a ban cannot be
    undone from this page and confirm() has no safe third answer */
 .banask { grid-column: 1 / -1; display: flex; flex-wrap: wrap;
   align-items: center; gap: 7px; margin-top: 6px; padding: 7px 9px;
   border-radius: 7px; background: #3a2020; color: #f4e6e6;
   font-size: 13px; }
 .banask span { flex: 1 1 220px; }
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
 .chunk { font-family: var(--display); font-weight: 700; font-size: 13px;
   background: none; border: 1px solid var(--dim); border-radius: 6px;
   color: var(--ink); padding: 5px 10px; cursor: pointer; }
 .chunk:disabled { color: var(--dimmer); border-color: var(--dimmer);
   cursor: default; }
 .rebuild:disabled { background: #1020a810; color: var(--dimmer); cursor: default; }
 .undo { background: none; border: 0; color: var(--dim); font-size: 12.5px;
         cursor: pointer; text-decoration: underline; padding: 6px; }
 /* secondary to Rebuild: rolling stages changes, it doesn't print a beat */
 .rollall { font-family: var(--display); font-weight: 700; font-size: 12.5px;
       letter-spacing: .06em; text-transform: uppercase; padding: 9px 15px;
       border: 1px solid #1020a826; border-radius: 9px; background: none;
       color: var(--text); cursor: pointer; white-space: nowrap; }
 .rollall:hover { border-color: var(--hi); color: var(--hi); }
 .rackmsg { font-size: 12.5px; color: var(--no); padding: 4px 0 0;
            white-space: pre-wrap; }

 /* -------------------------------------------------------- pull-up */
 .pullup { display: flex; align-items: flex-end; gap: 12px; flex-wrap: wrap; }
 .pullup .field { width: 130px; }
 .pullup button { font-family: var(--display); font-weight: 600; font-size: 14px;
       letter-spacing: .08em; text-transform: uppercase; padding: 11px 20px;
       border: 1px solid var(--co); border-radius: 9px; background: #1020a81a;
       color: var(--co); cursor: pointer; }
 .pullup .note { flex: 1; min-width: 200px; font-size: 12.5px;
                 color: var(--dimmer); }
 #pullmsg { font-size: 13px; color: var(--no); margin-top: 9px; }

 @media (max-width: 720px) {
   .fields { grid-template-columns: 1fr 1fr; }
   .refrow { grid-template-columns: 1fr; }
   .fields .field:last-child { grid-column: 1 / -1; }
   .thead audio { width: 100%; order: 9; }
   .thead { flex-wrap: wrap; }
   .lane { grid-template-columns: 1fr; gap: 7px; }
   .zones { grid-template-columns: 1fr; }
 }
</style></head><body>
<div class="wrap">

<div class="board">
<nav class="apptabs">
  <span class="here" title="You're here — making beats">Make</span>
  <a href="http://localhost:8765"
     title="The studio half — recipes, patches, Reason. Same launcher starts it.">Studio</a>
</nav>
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

<h2 class="box">The Crew <small>__CREWCOUNT__ personalities</small></h2>
<div class="djs">__CREW__</div>
<h2 class="box">The Legends <small>signature styles</small></h2>
<div class="djs">__LEGENDS__</div>
<h2 class="box">The Styles <small>seventeen subgenres, played by the rules</small></h2>
<div class="djs">__GENRES__</div>

<h2 class="box">Rhythm test bank <small>five real, well-known hip-hop beats — the rhythm never changes, only the sounds</small></h2>
<div class="fixedbank" id="fixedbank">__FIXEDBANK__</div>

<h2 class="box">Pattern library <small>every transcribed groove, by genre — drums only, no chords or bass</small></h2>
<div class="pullup">
  <div class="field" style="width:170px"><label>Genre</label>
    <select id="libgenre">__LIBGENRES__</select></div>
  <div class="field" style="width:300px"><label>Pattern</label>
    <select id="libpattern"></select></div>
  <button id="libgo">Play it</button>
  <div class="note">renders standalone, drops into the player below — roll again for a new kit on the same rhythm</div>
</div>

<h2 class="box">Breaks <small>famous figures + funk breaks — kept separate, played verbatim</small></h2>
<div class="pullup">
  <div class="field" style="width:340px"><label>Break</label>
    <select id="libbreak">__LIBBREAKS__</select></div>
  <button id="libbreakgo">Play it</button>
  <div class="note">saved to its own Breaks folder, never mixed into a genre</div>
</div>

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
    <div class="field"><label>&nbsp;</label>
      <label><input type="checkbox" id="loopsonly"> Loops only</label>
      <div class="hint">whole beat built from loop material instead of one-shots</div></div>
  </div>
  <div class="fields refrow">
    <div class="field"><label>Key</label>
      <span style="display:flex; gap:6px">
        <select id="keyroot"><option value="">&mdash; any &mdash;</option>__KEYROOTS__</select>
        <select id="keymode">__KEYMODES__</select>
      </span>
      <div class="hint">set a key and the beat gets chords in it</div></div>
    <div class="field"><label>Reference track</label>
      <div id="refdrop">Drag a song here to match its tempo and key</div>
      <div class="hint" id="refline">nothing dropped yet</div></div>
  </div>
  <div class="field quick"><label>Quick directions</label>
    <select id="quick">
      <option value="">&mdash; pick one &mdash;</option>
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
    </select>
    <div class="hint">fills the Directions box above &mdash; edit it after if you like</div></div>
  <div class="field quick"><label>Famous beats</label>
    <select id="famous">
      <option value="">&mdash; none, make it up &mdash;</option>
      <option value="break">surprise me &mdash; any of them</option>
__BREAKS__
    </select>
    <div class="hint">the drum part is played exactly as it was drummed, on
      your own samples &mdash; no audio from any record</div></div>
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

 // Famous beats: same trick — it types the words into Directions, so there
 // is ONE code path (parse_directions) whether he picks it or types it, and
 // the README trail says what he asked for either way.
 const BREAK_WORDS = __BREAKWORDS__;
 document.getElementById('famous').addEventListener('change', e => {
   const n = document.getElementById('notes');
   const kept = n.value.split(',').map(s => s.trim())
                 .filter(s => s && !BREAK_WORDS.includes(s.toLowerCase()));
   if (e.target.value) kept.unshift(e.target.value);
   n.value = kept.join(', ');
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
       // `loop`: a beat repeats until you press stop (owner 2026-08-31).
       // The attribute lives on the ELEMENT, so it survives cue()'s
       // src+load() and the /mix preview loops too. Renders are already
       // loop-safe (no edge fades, tails wrap), so the seam is clean.
       '<audio loop preload="none" src="/audio?no=' + b.no + '"></audio>' +
       '<span class="acts">' +
         '<button class="stembtn" data-role="stems">Stems</button>' +
         (b.se_id ? '<button class="stembtn" data-role="engine" ' +
           'title="Open in the Sound Engine with this DJ&apos;s effects ' +
           'already dialled in (start it from Sound Engine.command first)">' +
           'FX</button>' : '') +
         '<button title="Keep it" data-dest="favorites">&starf;</button>' +
         '<button title="DJ folder" data-dest="dj">&#9635;</button>' +
         '<button title="Trash it" data-dest="trash">&#9587;</button>' +
       '</span>' +
     '</div>' +
     '<div class="theory"></div>' +
     '<div class="rack"></div>';
   el.querySelector('.tname').textContent = t.rest;
   el.querySelector('.tsub').innerHTML =
     (t.bpm ? t.bpm + ' BPM' : '') + ' <span class="tloc"></span>';
   // why this beat works — only for beats that recorded their harmony;
   // anything older just doesn't get the block (see _beat_theory)
   const th = b.theory;
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
   el.addEventListener('dragstart', e => {
     e.dataTransfer.setData('text/plain', b.no); el.classList.add('dragging'); });
   el.addEventListener('dragend', () => el.classList.remove('dragging'));
   el.querySelectorAll('.acts button[data-dest]').forEach(btn =>
     btn.onclick = () => triage(b.no, btn.dataset.dest, el));
   el.querySelector('[data-role=stems]').onclick = ev => toggleRack(el, b.no, ev.target);
   // Open this beat in the Sound Engine with the DJ's effects already set
   // (sound_engine/fx_presets.py). It is a separate app on its own port, so
   // this is a plain link out — nothing is printed here and this beat's
   // files are not touched. If the Sound Engine isn't running the new tab
   // just fails to connect, which is why the button says to start it.
   const eng = el.querySelector('[data-role=engine]');
   if (eng) eng.onclick = () => window.open(
     'http://localhost:8767/?beat=' + encodeURIComponent(b.se_id), '_blank');
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
     pp.innerHTML = '&#10073;&#10073;'; });
   const stop = () => { pp.classList.remove('on'); pp.innerHTML = '&#9654;'; };
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

 // Where to play a beat FROM. Untouched, that's the rendered file (which
 // seeks, since /audio serves byte ranges). Touched at all — a new sound,
 // a volume, a removal — it's /mix, which renders the beat as the rack is
 // set (owner 2026-08-03: picking a new hi hat changed nothing when he
 // played the beat back). One URL shape for all three kinds of change, so
 // the preview can never disagree with itself.
 function mixUrl(no) {
   const t = trims[no] || {}, d = drops[no] || {}, p = staged[no] || {};
   const tk = Object.keys(t), dk = Object.keys(d).filter(k => d[k]);
   const pk = Object.keys(p).filter(k => p[k]);
   if (!tk.length && !dk.length && !pk.length) return '/audio?no=' + no;
   let u = '/mix?no=' + no
     + '&trims=' + encodeURIComponent(tk.map(k => k + ':' + t[k]).join(','))
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
   if (au.dataset.src === url && au.readyState) return false;
   au.dataset.src = url; au.src = url; au.load();
   return true;
 }

 // A beat that's already playing re-cues with the new levels. A paused one
 // is left alone on purpose: every arrow click would otherwise make the
 // server mix the beat again and throw the last one away, and the URL is
 // worked out at play time anyway.
 function refreshMix(el, no) {
   const au = el.querySelector('audio');
   if (!au || au.paused) return;
   const want = mixUrl(no);
   if (au.dataset.src === want) return;
   const at = au.currentTime;
   cue(au, want);
   au.addEventListener('loadedmetadata', function once() {
     au.removeEventListener('loadedmetadata', once);
     if (at < au.duration) au.currentTime = at;
     au.play().catch(() => {});
   });
 }

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
   foot.querySelector('.chunk').disabled = !(n + v + r);
   foot.querySelector('.undo').style.display = (n + v + r) ? '' : 'none';
   refreshMix(el, no);      // every volume/remove change lands here first
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
     '<span class="vol">' +
       '<button class="step dn" title="1 dB quieter">&minus;</button>' +
       '<span class="db" title="Click to reset to 0">0</span>' +
       '<button class="step up" title="1 dB louder">+</button>' +
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
   const STEP = 1, LIMIT = 24;
   let v = 0;
   const showDb = () => {
     db.textContent = v ? (v > 0 ? '+' : '') + v.toFixed(0) : '0';
     row.classList.toggle('trimmed', !!v);
     trims[no] = trims[no] || {};
     if (v) trims[no][s.lane] = v; else delete trims[no][s.lane];
     if (!Object.keys(trims[no]).length) delete trims[no];
     paintFoot(row.closest('.track'), no);
   };
   const nudge = (d) => {
     v = Math.max(-LIMIT, Math.min(LIMIT, v + d));
     showDb();
   };
   row.querySelector('.step.up').onclick = () => nudge(STEP);
   row.querySelector('.step.dn').onclick = () => nudge(-STEP);
   db.onclick = () => { v = 0; showDb(); };

   const picks = row.querySelector('.picks');

   if (s.stem) {
     const b = document.createElement('button');
     b.className = 'mini';
     b.title = 'Hear this on its own, at its level in the track';
     b.innerHTML = '&#9654;';
     // the staged dB rides along, so a stem previews at the level the
     // arrows are set to — same as it will sound in the beat
     b.onclick = () => play('/stem?no=' + no + '&lane=' +
                            encodeURIComponent(s.lane) +
                            '&db=' + (v || 0), b);
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
       const opts = [...sel.options].filter(o => o.value && o.value !== sel.value);
       if (!opts.length) return;         // list still loading, or nothing else
       sel.value = opts[Math.floor(Math.random() * opts.length)].value;
       sel.onchange();                   // stages it, plays it, repaints
     };
     picks.appendChild(dice);
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
       // by rendering the BEAT with that instrument in it, which is the
       // only honest way to hear the choice (owner 2026-08-04).
       if (s.voices) play(mixUrl(no));
       else play('/sample?no=' + no + '&lane=' + encodeURIComponent(s.lane) +
                 '&path=' + encodeURIComponent(sel.value));
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
   else {
     const opt = row.querySelector('select').selectedOptions[0];
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
   specs.forEach(s => rack.appendChild(laneRow(no, s)));
   const foot = document.createElement('div');
   foot.className = 'rackfoot';
   foot.innerHTML = '<span class="staged"></span>' +
     '<button class="rollall" title="New sound for every row at once">' +
       '🎲 Roll everything</button>' +
     '<button class="undo">clear changes</button>' +
     '<button class="chunk" title="Save this version into the Chunks ' +
       'folder and keep going">+ Add chunk</button>' +
     '<button class="rebuild">Rebuild beat</button>' +
     '<div class="rackmsg" style="flex-basis:100%"></div>';
   rack.appendChild(foot);
   // One click, a whole new kit (owner 2026-08-04). Rolls every row that
   // CAN be rolled — the locked producer tag and the synthesised sub are
   // skipped, and so is anything already removed, since rolling a sound
   // he just took out would be nonsense. Nothing plays per row: with a
   // dozen rows that would be a dozen overlapping one-shots, so it
   // auditions once, as the beat, which is the point of rolling them all.
   foot.querySelector('.rollall').onclick = () => {
     let n = 0;
     rack.querySelectorAll('.lane').forEach(r => {
       const sel = r.querySelector('select');
       if (!sel || sel.disabled) return;
       if (drops[no] && drops[no][r.dataset.lane]) return;
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
     delete staged[no]; delete trims[no]; delete drops[no];
     rack.querySelectorAll('.lane').forEach(r => {
       const sel = r.querySelector('select'); if (sel) sel.value = '';
       const d = r.querySelector('.db');
       if (d) d.click();                       // arrows: click resets to 0
       r.classList.remove('trimmed');
       r.classList.remove('dropped');
       const s = specs.find(x => x.lane === r.dataset.lane);
       if (s) paintLane(r, no, s);
     });
     paintFoot(el, no);
   };
   foot.querySelector('.rebuild').onclick = () => rebuild(el, no, foot);
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
                              drops: Object.keys(drops[no] || {}) }) });
     const d = await r.json();
     msg.textContent = d.ok
       ? 'chunk ' + d.count + ' saved — ' + d.file
       : d.error;
   } catch (e) { msg.textContent = String(e); }
   btn.textContent = was; btn.disabled = false;
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

 // --------------------------------------------- reference track (sec. 5)
 // Drop a song; read its tempo and key; SHOW both so he can correct them.
 // The detector is wrong in two predictable ways — half or double the
 // tempo, and the relative major/minor — so the correction buttons are
 // the feature, not a fallback.
 const refdrop = document.getElementById('refdrop'),
       refline = document.getElementById('refline'),
       keyroot = document.getElementById('keyroot'),
       keymode = document.getElementById('keymode'),
       tempoBox = document.getElementById('tempo');
 let refName = '', refAlt = null;
 const TLO = __TEMPOLO__, THI = __TEMPOHI__;   // the window /make enforces

 function refSay() {
   if (!refName) { refline.textContent = 'nothing dropped yet'; return; }
   const bpm = parseFloat(tempoBox.value);
   refline.innerHTML = '<b>' + esc(refName) + '</b> &mdash; ' +
     (tempoBox.value || '?') + ' BPM, ' + (keyroot.value || 'any') + ' ' +
     keymode.value +
     // only offer an octave the tempo box would actually accept
     (bpm / 2 >= TLO ? '<button data-ref="half">&divide;2</button>' : '') +
     (bpm * 2 <= THI ? '<button data-ref="double">&times;2</button>' : '') +
     (refAlt ? '<button data-ref="rel">' + esc(refAlt.root + ' ' +
               refAlt.mode) + '?</button>' : '') +
     '<button data-ref="clear">clear</button>';
 }

 refline.onclick = e => {
   const what = e.target.dataset && e.target.dataset.ref;
   if (!what) return;
   const bpm = parseFloat(tempoBox.value);
   if (what === 'half' && bpm / 2 >= TLO) tempoBox.value = Math.round(bpm / 2);
   if (what === 'double' && bpm * 2 <= THI) tempoBox.value = Math.round(bpm * 2);
   if (what === 'rel' && refAlt) {          // swaps, so it flips back
     const was = { root: keyroot.value, mode: keymode.value };
     keyroot.value = refAlt.root; keymode.value = refAlt.mode;
     refAlt = was;
   }
   if (what === 'clear') {
     refName = ''; refAlt = null; tempoBox.value = ''; keyroot.value = '';
   }
   refSay();
 };

 ['dragover', 'dragenter'].forEach(ev =>
   refdrop.addEventListener(ev, e => {
     e.preventDefault(); refdrop.classList.add('over'); }));
 refdrop.addEventListener('dragleave', () => refdrop.classList.remove('over'));
 refdrop.addEventListener('drop', async e => {
   e.preventDefault(); refdrop.classList.remove('over');
   const f = e.dataTransfer.files && e.dataTransfer.files[0];
   if (!f) return;
   const was = refdrop.textContent;
   refdrop.classList.add('busy');
   refdrop.textContent = 'Listening to ' + f.name + '\u2026';
   try {
     const dot = f.name.lastIndexOf('.');
     const ext = (dot > 0 ? f.name.slice(dot) : '.wav')
                   .replace(/[^A-Za-z0-9.]/g, '');
     const r = await fetch('/reference', { method: 'POST',
       headers: { 'X-Ext': ext || '.wav' }, body: await f.arrayBuffer() });
     const d = await r.json();
     if (d.ok) {
       refName = f.name;
       tempoBox.value = d.bpm;
       keyroot.value = d.root;
       keymode.value = d.mode;
       refAlt = { root: d.alt_root, mode: d.alt_mode };
       refSay();
     } else { refline.textContent = d.error; }
   } catch (err) { refline.textContent = String(err); }
   refdrop.classList.remove('busy');
   refdrop.textContent = was;
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
         tempo: tempoBox.value.trim(),
         key: keyroot.value ? keyroot.value + ' ' + keymode.value : '',
         count, notes: document.getElementById('notes').value,
         loops_only: document.getElementById('loopsonly').checked }) });
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
    words = json.dumps([w for w, _ in BREAK_WORDS] + ["break"])
    # straight off ROOT_HZ and MODES, so the dropdowns can never offer a
    # key the engine would then refuse
    from key_context import MODES
    keyroots = "".join(f"<option>{r}</option>" for r in ROOT_HZ)
    keymodes = "".join(
        '<option value="%s"%s>%s</option>'
        % (m, " selected" if m == "minor" else "", m.replace("_", " "))
        for m in sorted(MODES))
    return (_PAGE.replace("__CREW__", crew).replace("__LEGENDS__", legends)
            .replace("__GENRES__", styles)
            .replace("__FIXEDBANK__", fixedbank)
            .replace("__BREAKS__", _break_options())
            .replace("__BREAKWORDS__", words)
            .replace("__LIBGENRES__", _library_genre_options())
            .replace("__LIBBREAKS__", _library_break_options())
            .replace("__LIBRARYJSON__", json.dumps({
                key: [p["name"] for p in patterns]
                for key, (label, patterns) in library_genres().items()}))
            .replace("__CREWCOUNT__", _count_word(len(CREW_ORDER)))
            .replace("__TEMPOLO__", str(TEMPO_LO))
            .replace("__TEMPOHI__", str(TEMPO_HI))
            .replace("__KEYROOTS__", keyroots)
            .replace("__KEYMODES__", keymodes)
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
                                 "/reference"):
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
                except Exception as e:
                    self._json({"ok": False, "error": str(e)})
                return
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
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
                                                 drops=data.get("drops"))
                        print(" ", report.replace("\n", " "))
                    self._json({"ok": True,
                                "no": int(path.name.split(" ", 1)[0])})
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
                                         drops=data.get("drops"))
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
