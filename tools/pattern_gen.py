"""Pattern grammar: each DJ composes a FRESH pattern every generation
(owner verdict 2026-07-17: beats were coming out with the same rhythm
every time — the old engine only mutated one hardcoded skeleton per DJ).

A grammar is style rules, not a pattern: where this DJ's kicks like to
land (a weight per 16th step), how many, whether they double up; what
they do with the backbeat (2&4 / halftime on 3 / displaced / ghosts);
what their hats do (8ths, 16ths, sparse, gallop, 32nd roll walls, New
Math's quintuplets). Every beat rolls fresh choices inside those rules,
so the style survives but the rhythm never repeats.

Also per the same verdict:
- kick FLAVORS: not solely 808s — each DJ rolls a kick type per beat
  (clean/punchy/acoustic vs 808, era-weighted), with era choke ranges;
- GUEST LANES: beats may add 1-2 extra colors (shaker, rims, toms,
  congas, blocks, fx one-shots) from that DJ's palette;
- PATTERN HISTORY: ~/.reason_voice/pattern_history.json remembers each
  DJ's recent rolls — since 2026-07-21 it only feeds the kick-flavor
  streak-breaker (the too-similar-regenerate guard is gone: variety
  comes from the composition, not from rejection).

v6 (owner directive 2026-07-18): MINIMAL constraints — variety beats
style fidelity. Identity = stamp + mix flavor + tempo zone. Density is
fully free, every mode is on every DJ's menu (home-leaned), kick banks
cross-pollinate, swing rolls per beat around the home feel (in
beat_machine), and beats are 4/4 80% / real 3-4 or 6-8 10% / exotic
grids in 4/4 10%.
"""
import json
import os
import random
from pathlib import Path

PAT_HIST = Path(os.path.expanduser("~/.reason_voice/pattern_history.json"))
PAT_KEEP = 24
BEATS = (0, 4, 8, 12)
STYLE_VERSION = 7      # bump when DEFAULT_STYLE changes (config auto-syncs)

# ------------------------------------------------- the groove library
# Owner drop 2026-07-17 (second library expansion): 131 genre-tagged
# reference grooves with per-lane velocity grids, built in a separate
# session and imported to <project>/pattern_library/. compose() may
# reach for one as this beat's seed — kick and hat lines, and on a crew
# (non-legend, non-traditional) beat sometimes the snare line too
# (owner call 2026-07-21; legends keep their own backbeat). Every
# seeded line still passes _bank_vary, the sparse-bed thinning, and
# both repeat guards, so a groove seed reads as an influence, never a
# copy. Per-DJ taste (which genres, how often) lives in the "library"
# style key in crew_config.json — tune it there.

LIB_DIR = Path(__file__).resolve().parent.parent / "pattern_library"
_LIB_CACHE = None


def _lib_kick(vels):
    """Kick lane string from a library velocity grid.

    Historically this ignored velocity entirely and marked an accent by
    POSITION (every beat-start), which is fine for the style grammars that
    were written flat. It is wrong for a real break: the ghost kicks between
    the accents are a lot of what makes the Funky Drummer sound like the
    Funky Drummer, and they were arriving as full-strength hits.

    So: honour velocity when the pattern actually has any (ghosts below 90
    become "."), and fall back to the old positional accents when every hit
    is the same weight, which keeps all 180 existing patterns unchanged."""
    n = len(vels)
    hits = [v for v in vels if v]
    if hits and min(hits) < 90 <= max(hits):
        return "".join(("X" if v >= 90 else ".") if v else "-" for v in vels)
    caps = set(range(0, n, max(1, n // 4)))
    return "".join(("X" if i in caps else "x") if v else "-"
                   for i, v in enumerate(vels))


def _lib_snare(vels):
    """Backbeat lane string from a library velocity grid: accents land
    as X, soft hits as ghosts."""
    return "".join(("X" if v >= 90 else ".") if v else "-" for v in vels)


def _lib_hat(tracks, steps):
    base = next((tracks[t] for t in ("closed_hat", "ride", "shaker")
                 if t in tracks), None)
    opens = tracks.get("open_hat")
    if base is None and opens is None:
        return None
    s = ["x" if base and base[i] else "-" for i in range(steps)]
    for i in range(steps):
        if opens and opens[i]:
            s[i] = "o"
    return "".join(s)


def load_library():
    """Parse pattern_library/patterns_*.json into engine bar strings.
    Only 4/4 grooves on 16 or 32 steps qualify as seeds (the 12-step
    shuffle/waltz patterns stay in the folder for his own Reason use)."""
    global _LIB_CACHE
    if _LIB_CACHE is not None:
        return _LIB_CACHE
    pats = []
    for f in sorted(LIB_DIR.glob("patterns_*.json")):
        try:
            data = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        genre = f.stem.split("_", 1)[1]
        for p in data:
            n = p.get("steps", 16)
            if p.get("time_signature") != "4/4" or n not in (16, 32):
                continue
            tr = p.get("tracks", {})
            entry = dict(name=p["name"], genre=genre,
                         subgenre=p.get("subgenre", ""), steps=n)
            if tr.get("kick"):
                entry["kick"] = _lib_kick(tr["kick"])
            if tr.get("snare"):
                entry["snare"] = _lib_snare(tr["snare"])
            hat = _lib_hat(tr, n)
            if hat and hat.count("-") < n:
                entry["hat"] = hat
            if "kick" in entry or "hat" in entry:
                pats.append(entry)
    _LIB_CACHE = pats
    return pats


def _pick_break(rng):
    """One of the classic break figures (pattern_library/patterns_breaks.json,
    subgenre "breaks"). Falls back to any two-bar groove if that file is
    missing, so a break request degrades to something break-shaped rather
    than to silence."""
    pats = load_library()
    breaks = [p for p in pats if p.get("subgenre") == "breaks"]
    if not breaks:
        breaks = [p for p in pats if p["steps"] == 32]
    return rng.choice(breaks) if breaks else None


def _pick_library(spec, rng):
    """One groove, weighted by this DJ's genre taste. Tags match the
    subgenre at full weight, the whole genre file at half. A "genres"
    key restricts the pool to those library files (traditional beats
    seed from the hiphop file only)."""
    pats = load_library()
    only = spec.get("genres")
    if only:
        pats = [p for p in pats if p["genre"] in only]
    tags = {t: w for t, w in spec.get("tags", [])}
    weights = [tags.get(p["subgenre"], 0) + 0.5 * tags.get(p["genre"], 0)
               for p in pats]
    if not any(weights):
        return None
    return rng.choices(pats, weights=weights)[0]


def _thin_kick(bar, rng):
    """Density cap for library seeds. v6 (2026-07-18): density is FREE —
    the cap only sheds the truly wall-to-wall grooves (d-beat with
    doubles everywhere), not the busy ones."""
    cap = max(2, round(8 * len(bar) / 16))
    s = list(bar)
    small = [i for i, c in enumerate(s) if c == "x"]
    rng.shuffle(small)
    while sum(c != "-" for c in s) > cap and small:
        s[small.pop()] = "-"
    return "".join(s)

# --------------------------------------------------------- the grammars
# kick: w = a weight per 16th step (step 0 is always anchored), hits =
#   how many per bar, double_p = chance of a stutter pair.
# backbeat lanes: modes weighted per DJ; ghosts land in gcells.
# hat/snap: timekeeper modes weighted per DJ.
# copy: this lane mirrors another's anchors (Neptunes flam, clap stacks).
# extras: (role, want-tags, lane name) palette + how often guests appear.

# Every backbeat mode a crew DJ can reach. The genre roster's canon
# figures (dembow, club, bounce, stomp) are deliberately NOT here —
# those are placed verbatim as that style's identity, not rolled.
BACKBEAT_MODES = ("backbeat", "halftime", "displaced", "sparse",
                  "four", "push", "tresillo", "offbeat", "drag", "pickup")

# How hard a DJ leans on their home mode. Was effectively 0.45 with only
# four modes on the board, which put a bare 2&4 under most of the
# library (see the 2026-07-22 audit). At 0.24 across ten modes the home
# feel is still the single most likely roll — it just stops being the
# default the other 76% of the time.
HOME_LEAN = 0.24


def _bb(home, lean=HOME_LEAN):
    """A backbeat menu leaned toward this DJ's home mode. Keeps the v6
    rule that every mode is on every board; only the lean says who this
    DJ is.

    Shares are rounded to 4 places so the numbers stay hand-editable in
    crew_config.json, and the rounding remainder goes back to the home
    mode so the menu still sums to exactly 1.0."""
    others = [m for m in BACKBEAT_MODES if m != home]
    share = round((1.0 - lean) / len(others), 4)
    return ([[home, round(1.0 - share * len(others), 4)]]
            + [[m, share] for m in others])


DEFAULT_STYLE = {
    # v6 (owner directive 2026-07-18): MINIMAL constraints, variety over
    # style fidelity. Every DJ can reach every backbeat and timekeeper
    # mode — the weights only LEAN toward their home feel. Identity now
    # lives in the stamp, the mix flavor, and the tempo zone; patterns,
    # density, swing, and kits roam free.
    "Otto Grit": dict(
        grammar=dict(
            kick=dict(w=[10, 2, 2, 3, 2, 2, 4, 6, 3, 2, 5, 3, 2, 3, 5, 3],
                      hits=[2, 7], double_p=0.35),
            snare=dict(modes=_bb('backbeat'),
                       ghosts=[0, 3],
                       gcells=[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]),
            hat=dict(modes=[['eighths', 0.1], ['sixteenths', 0.1], ['sparse', 0.3], ['broken', 0.1], ['offbeats', 0.1], ['gallop', 0.1], ['answer', 0.1], ['rolls32', 0.1]], open_p=0.1),
        ),
        kick_flavors=[[0.4, "808", ["dust", "boom", "dirty"], [0.35, 0.9]],
                      [0.6, None, ["boom", "punch", "acoustic", "break",
                                   "knock"], [0.18, 0.5]]],
        library=dict(p=0.5, tags=[["lofi", 3], ["boom-bap", 2],
                                   ["neo-soul", 2], ["soul", 1]]),
        extras=dict(p=0.7, nmax=2, pool=[
            ["perc", ["tamb", "shaker"], "shaker"],
            ["rim", ["rim", "stick"], "rims"],
            ["perc", ["tom"], "toms"],
            ["fx", ["vinyl", "reverse", "foley"], "foundfx"]]),
    ),
    "Cutz": dict(
        grammar=dict(
            kick=dict(w=[10, 1, 1, 5, 2, 1, 3, 2, 2, 1, 5, 2, 1, 5, 2, 2],
                      hits=[2, 6], double_p=0.25),
            snare=dict(modes=_bb('backbeat'),
                       ghosts=[0, 3],
                       gcells=[2, 3, 5, 6, 7, 9, 10, 13, 14, 15]),
            hat=dict(modes=[['eighths', 0.3], ['sixteenths', 0.1], ['sparse', 0.1], ['broken', 0.1], ['offbeats', 0.1], ['gallop', 0.1], ['answer', 0.1], ['rolls32', 0.1]], open_p=0.06),
        ),
        kick_flavors=[[0.3, "808", ["punch", "hard"], [0.3, 0.7]],
                      [0.7, None, ["punch", "knock", "hard", "acoustic"],
                       [0.15, 0.45]]],
        library=dict(p=0.45, tags=[["boom-bap", 4], ["funk", 2],
                                  ["breakbeat", 1]]),
        extras=dict(p=0.6, nmax=2, pool=[
            ["fx", ["scratch"], "cutfx"],
            ["rim", ["rim", "stick"], "rims"],
            ["perc", ["shaker", "tamb"], "shaker"]]),
    ),
    "Crate Prophet": dict(
        grammar=dict(
            kick=dict(w=[10, 2, 3, 2, 1, 2, 4, 4, 2, 2, 4, 2, 3, 2, 4, 2],
                      hits=[2, 6], double_p=0.3),
            snare=dict(modes=_bb('backbeat'),
                       ghosts=[0, 3],
                       gcells=[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]),
            hat=dict(modes=[['eighths', 0.1], ['sixteenths', 0.1], ['sparse', 0.3], ['broken', 0.1], ['offbeats', 0.1], ['gallop', 0.1], ['answer', 0.1], ['rolls32', 0.1]], open_p=0.2),
            bongo=dict(euclid=[3, 5, 7]),
        ),
        kick_flavors=[[0.35, "808", ["warm", "deep"], [0.4, 0.9]],
                      [0.65, None, ["boom", "warm", "break", "acoustic"],
                       [0.2, 0.5]]],
        library=dict(p=0.5, tags=[["boom-bap", 3], ["soul", 3],
                                   ["lofi", 1], ["funk", 2],
                                   ["motown", 1]]),
        extras=dict(p=0.7, nmax=2, pool=[
            ["perc", ["conga", "bongo"], "congas2"],
            ["perc", ["shaker", "tamb"], "shaker"],
            ["fx", ["vinyl", "reverse", "foley"], "foundfx"]]),
    ),
    "Chrome Dial": dict(
        grammar=dict(
            kick=dict(w=[10, 1, 1, 6, 1, 1, 4, 2, 3, 1, 3, 4, 1, 3, 3, 2],
                      hits=[2, 7], double_p=0.5),
            clap=dict(modes=_bb('backbeat'), ghosts=[0, 2],
                      gcells=[2, 3, 6, 7, 10, 11, 14, 15]),
            snap=dict(modes=[['eighths', 0.1], ['sixteenths', 0.1], ['sparse', 0.1], ['broken', 0.1], ['offbeats', 0.1], ['gallop', 0.1], ['answer', 0.3], ['rolls32', 0.1]]),
            perc=dict(euclid=[3, 5, 7]),
        ),
        kick_flavors=[[0.2, "808", ["clean", "tight"], [0.3, 0.6]],
                      [0.8, None, ["clean", "punch", "tight", "pop"],
                       [0.12, 0.4]]],
        library=dict(p=0.5, tags=[["rnb", 3], ["garage", 2],
                                   ["funk", 1], ["electro", 2]]),
        extras=dict(p=0.7, nmax=2, pool=[
            ["perc", ["tabla", "block", "cowbell"], "exotic2"],
            ["fx", ["zap", "laser", "glitch"], "blips"],
            ["rim", ["rim", "click"], "clicks"]]),
    ),
    "Glass Cat": dict(
        grammar=dict(
            kick=dict(w=[10, 1, 1, 2, 1, 1, 2, 1, 6, 1, 4, 1, 1, 2, 2, 2],
                      hits=[2, 5], double_p=0.15),
            snare=dict(modes=_bb('backbeat'),
                       ghosts=[0, 2], gcells=[3, 7, 11, 15]),
            clap=dict(copy="snare"),          # the documented late flam
            snap=dict(modes=[['eighths', 0.1], ['sixteenths', 0.1], ['sparse', 0.3], ['broken', 0.1], ['offbeats', 0.1], ['gallop', 0.1], ['answer', 0.1], ['rolls32', 0.1]]),
        ),
        kick_flavors=[[0.15, "808", ["clean"], [0.25, 0.5]],
                      [0.85, None, ["clean", "tight", "pop", "punch"],
                       [0.1, 0.35]]],
        library=dict(p=0.45, tags=[["rnb", 2], ["minimal", 3],
                                  ["funk", 2], ["cloud-rap", 1]]),
        extras=dict(p=0.6, nmax=2, pool=[
            ["fx", ["glitch", "zap", "laser"], "blips"],
            ["perc", ["block", "clave"], "woods"]]),
    ),
    "Sunday Chop": dict(
        grammar=dict(
            kick=dict(w=[10, 1, 1, 2, 4, 1, 2, 4, 8, 1, 2, 2, 4, 1, 3, 3],
                      hits=[3, 7], double_p=0.35),
            clap=dict(modes=_bb('backbeat'), ghosts=[0, 2],
                      gcells=[2, 3, 6, 7, 10, 11, 14, 15]),
            snare=dict(copy="clap"),          # tucked under the big clap
            hat=dict(modes=[['eighths', 0.3], ['sixteenths', 0.1], ['sparse', 0.1], ['broken', 0.1], ['offbeats', 0.1], ['gallop', 0.1], ['answer', 0.1], ['rolls32', 0.1]], open_p=0.08),
            perc=dict(modes=[['eighths', 0.1], ['sixteenths', 0.1], ['sparse', 0.1], ['broken', 0.1], ['offbeats', 0.3], ['gallop', 0.1], ['answer', 0.1], ['rolls32', 0.1]]),
        ),
        kick_flavors=[[0.3, "808", ["punch", "knock"], [0.3, 0.7]],
                      [0.7, None, ["punch", "knock", "clean"],
                       [0.15, 0.45]]],
        library=dict(p=0.5, tags=[["soul", 3], ["motown", 3],
                                   ["boom-bap", 2], ["funk", 1]]),
        extras=dict(p=0.65, nmax=2, pool=[
            ["perc", ["tamb", "shaker"], "shaker"],
            ["crash", ["crash"], "crash2"],
            ["fx", ["reverse", "impact"], "swellfx"]]),
    ),
    "Night Metro": dict(
        grammar=dict(
            kick=dict(w=[10, 1, 1, 3, 1, 1, 5, 1, 2, 1, 4, 2, 3, 1, 2, 2],
                      hits=[2, 6], double_p=0.25),
            clap=dict(modes=_bb('halftime'), ghosts=[0, 1],
                      gcells=[6, 7, 14, 15]),
            hat=dict(modes=[['eighths', 0.093], ['sixteenths', 0.093], ['sparse', 0.093], ['broken', 0.093], ['offbeats', 0.093], ['gallop', 0.093], ['answer', 0.093], ['rolls32', 0.35]], roll_n=[1, 3]),
        ),
        kick_flavors=[[0.2, "808", ["deep", "sub", "long"], [0.9, 2.0]],
                      [0.25, "808", ["deep", "sub"], [0.4, 0.8]],
                      [0.55, None, ["punch", "deep", "knock"],
                       [0.25, 0.6]]],
        library=dict(p=0.65, tags=[["trap", 4], ["cloud-rap", 2],
                                  ["drill", 2], ["garage", 1],
                                  ["breakbeat", 1]]),
        extras=dict(p=0.6, nmax=2, pool=[
            ["fx", ["riser", "reverse", "sweep"], "risers"],
            ["perc", ["cowbell", "block"], "bells"]]),
    ),
    "Rage Engine": dict(
        grammar=dict(
            kick=dict(w=[10, 1, 1, 3, 1, 1, 6, 1, 2, 1, 2, 2, 6, 1, 2, 3],
                      hits=[2, 7], double_p=0.4),
            snare=dict(modes=_bb('halftime'),
                       ghosts=[0, 1], gcells=[6, 7, 14, 15], burst_p=0.5),
            clap=dict(copy="snare"),
            hat=dict(modes=[['eighths', 0.093], ['sixteenths', 0.093], ['sparse', 0.093], ['broken', 0.093], ['offbeats', 0.093], ['gallop', 0.093], ['answer', 0.093], ['rolls32', 0.35]], roll_n=[1, 3]),
        ),
        kick_flavors=[[0.2, "808", ["hard", "distort"], [0.8, 1.8]],
                      [0.25, "808", ["hard", "punch"], [0.35, 0.7]],
                      [0.55, None, ["hard", "punch", "knock"],
                       [0.2, 0.5]]],
        library=dict(p=0.65, tags=[["trap", 4], ["drill", 2],
                                  ["techno", 1], ["electro", 1]]),
        extras=dict(p=0.65, nmax=2, pool=[
            ["crash", ["crash", "impact"], "impacts"],
            ["fx", ["riser", "sweep"], "sirens"]]),
    ),
    "New Math": dict(
        grammar=dict(
            kick=dict(w=[10, 1, 1, 7, 1, 1, 6, 1, 6, 1, 5, 1, 2, 1, 3, 2],
                      hits=[3, 7], double_p=0.35),
            snare=dict(modes=_bb('displaced'),
                       ghosts=[0, 2], gcells=[2, 5, 7, 10, 13, 15]),
            snap=dict(modes=[['eighths', 0.1], ['sixteenths', 0.1], ['sparse', 0.1], ['broken', 0.1], ['offbeats', 0.3], ['gallop', 0.1], ['answer', 0.1], ['rolls32', 0.1]]),
            hat=dict(modes=[['eighths', 0.087], ['sixteenths', 0.087], ['sparse', 0.087], ['broken', 0.087], ['offbeats', 0.087], ['gallop', 0.087], ['answer', 0.087], ['rolls32', 0.087], ['quint20', 0.3]]),
            perc=dict(euclid=[3, 5, 7]),
        ),
        kick_flavors=[[0.3, "808", ["punch", "club"], [0.4, 1.0]],
                      [0.7, None, ["punch", "knock", "club", "tight"],
                       [0.15, 0.45]]],
        library=dict(p=0.65, tags=[["garage", 3], ["breakbeat", 2],
                                   ["jungle", 2], ["dnb", 2],
                                   ["electro", 1], ["drill", 1],
                                   ["house", 1]]),
        extras=dict(p=0.75, nmax=2, pool=[
            ["fx", ["glitch", "laser", "zap", "reverse"], "glitches"],
            ["perc", ["block", "clave", "tabla"], "mathperc"],
            ["rim", ["rim", "click"], "clicks"]]),
    ),
}

# New Math's boom-bap mode reaches for dusty, short drums instead
BOOM_BAP_FLAVORS = [[0.5, "808", ["boom", "dust", "dirty"], [0.35, 0.8]],
                    [0.5, None, ["boom", "punch", "knock", "acoustic"],
                     [0.18, 0.5]]]

# Kick flavor is the entry's OWN business again (owner rule 2026-07-23,
# second call: "allow DJs to stay true to style, with the kick"). The
# engine-wide clean/punch filter added earlier the same day is gone: it
# dropped every 808 flavor at the one spot all kick rolls route through,
# which also removed the 808 from identities that ARE the 808 — Mustang's
# own one-line description is "a sparse 808 kick," and no entry on the
# roster carries a second non-808 flavor, so the filter left each of them
# exactly one kick sound for every beat. Each entry's declared
# `kick_flavors` weights are the style statement; a DJ who should stay
# clean says so there (Doc Day: 808 at 0.1 vs punch at 0.75) instead of
# every DJ being forced clean from here.

# ------------------------------------------------------- the kick banks
# Owner request 2026-07-17: a LARGER library of patterns. Each DJ carries
# ~10 curated kick skeletons in their vocabulary — real moves from their
# style lane, not one generator's habits. The composer usually starts
# from one of these (then varies it inside the grammar); sometimes it
# still freestyles from the weight map. History keeps repeats away.

KICK_BANK = {
    "Otto Grit": [                 # drunk, off-the-grid leans
        "X------x--X-----", "X--x------X--x--", "X------xX---x---",
        "X-----x---X----x", "X--x---x--X-x---", "X---x-----Xx----",
        "X------x-X---x--", "X-x-----x-X-----", "Xx-----x--X--x--",
        "X-----xx--X----x", "X-----xxX-------", "Xx-x----X-X-----",
        "X----x--XxXX--x-", "X-----xx--XX--xx", "X--x--x---XX--x-",
        "X----xxxX------x", "Xx------X-X--x-x", "Xxx------xXX---x"],
    "Cutz": [                      # surgical, sparse punches
        "X--x------X-----", "X---------X--x--", "X--x--x---X-----",
        "X-x-------X---x-", "X--x------Xx----", "X---x-----X--x--",
        "X--------xX-----", "X--x---x--X--x--", "X---------X-x---",
        "X-xx------X-----", "X--------XXX---x", "X--x-----XX--x--",
        "X--------XXX-x--", "X---------XX-x-x", "X-----x---XX-xx-",
        "X----xx--X-X--x-", "X--x-----XXX----", "X------x-XXX----"],
    "Crate Prophet": [             # warm golden-era rollers
        "X-----x---X--x--", "X--x--x---X-----", "X-----x-x-X-----",
        "X---x-----X-x---", "X-----xx--X--x--", "X-x---x---X-----",
        "X-----x---X-xx--", "X--x------X---x-", "X-----x--xX-----",
        "X---xx----X--x--", "X--------xX-x-x-", "X-xx------X-----",
        "Xxxx--x---X-----", "X-x--x---xX-----", "X-x-------X--xx-",
        "Xxxx------X----x", "Xx----xx-xX-----", "X--------xX----x"],
    "Chrome Dial": [               # stutters and syncopation
        "X--X--X---------", "X--X--X---X-----", "X-----X--X--X---",
        "X--X----X-X-----", "X---XX----X-----", "X--X--X--X--X---",
        "X-----X---XX----", "X--X---X--X---X-", "XX----X---X-----",
        "X---X--X----X---", "X----------X----", "X-------------X-",
        "X--XX---X-------", "X---X-----------", "X---------X-X-X-",
        "X---X-X----X----", "X-------X---X-X-", "X-----X---X---X-"],
    "Glass Cat": [                 # minimal, negative space
        "X-------X-X-----", "X---------X---X-", "X-------X-------",
        "X--X----X-------", "X-------XX------", "X---X---X-X-----",
        "X-------X---X---", "X-X-----X-------", "X---X-X---X-----",
        "X----------X----", "X-----------X-X-", "X------------X--",
        "X-----X-----X--X", "X-----X-------X-", "X----X-X-----X--",
        "X----X----------"],
    "Sunday Chop": [               # gospel drive, pushed 8ths
        "X---x---X---x---", "X---x--xX---x---", "X--xX---X---x---",
        "X---x---X--xx---", "X---X---X---X---", "X---x-x-X---x---",
        "X---x---X-x-x---", "Xx--x---X---x---", "X--x----X------x",
        "X------xX--x----", "X--x---xX--xx---", "X---x--xX--x---x",
        "X------xX--xx--x", "X--xx--xX--x----", "X--x----X--x----",
        "X--x---xX---x--x"],
    "Night Metro": [               # halftime dark sparse
        "X-----X---X-----", "X---------X-----", "X-----X-------X-",
        "X------X--X-----", "X-----X---X---X-", "X---------X--X--",
        "X-----X-----X---", "X--------X-X----", "X--X-----x--X--x",
        "X--x-X-X-----x--", "X--x-----XX----x", "X--x-X---X---X--",
        "X-----------X--x", "X--X-XX------x--", "X--X------X----x",
        "X--X------------"],
    "Rage Engine": [               # relentless triplet-feel
        "X-----X-----X---", "X-----X-----X--X", "X--X--X-----X---",
        "X-----X---X-X---", "X-----XX----X---", "X--X--X--X--X---",
        "XX----X-----X---", "X-----X-----XX--", "X------X---XX--x",
        "X--x-XX------X-x", "X--x-X----------", "X----XX----X----",
        "X--x-XX----X---x", "X--x--X------X--", "X----X-X-------x",
        "X------------X-x"],
    "New Math": [                  # Jersey claves + necklaces
        "X--X--X-X-X-----", "X--X--X-X-------", "X--X---X--X-X---",
        "X-X--X--X-X-----", "X--X-X--X--X----", "X--X--X-X-X-X---",
        "X---X-X--X--X---", "X--XX--X--X-----", "X-----------X---",
        "X-----X-X---X---", "X--X------X-----", "X-------X----X--",
        "X--X----X---X---", "X-----X---X-X---", "X-----X---------",
        "X---------X-XX--"],
}

BOOM_BAP_KICKS = [                            # New Math's odd-variant lane
    "X------x--X-----", "X--x------X--x--", "X-----x---X--x--",
    "X------xX---x---", "X--x--x---X-----", "X-----x-x-X-----",
    "X-xx------X-----", "X----x----X--x-x", "X-----xx--X---x-",
    "X-x-------X--x--"
]


def _bank_vary(bar, spec, rng):
    """A bank skeleton gets this beat's own accent: shift one small hit,
    maybe drop one, maybe sprinkle one from the DJ's weight map, maybe a
    stutter double. The opening X stays planted."""
    s = list(bar)
    idx = [i for i, c in enumerate(s) if c == "x"]
    rng.shuffle(idx)
    if idx and rng.random() < 0.6:
        i = idx[0]
        j = i + rng.choice((-1, 1))
        if 0 <= j < 16 and s[j] == "-":
            s[j], s[i] = s[i], "-"
    if len(idx) > 1 and rng.random() < 0.3:
        s[idx[1]] = "-"
    if rng.random() < 0.4:
        w = [wt if s[i] == "-" else 0 for i, wt in enumerate(spec["w"])]
        if sum(w):
            s[rng.choices(range(16), weights=w)[0]] = "x"
    if rng.random() < spec.get("double_p", 0.2):
        hits = [i for i, c in enumerate(s) if c != "-"]
        i = rng.choice(hits)
        if i + 1 < 16 and s[i + 1] == "-":
            s[i + 1] = "x"
    return "".join(s)

EXTRA_SECS = {"crash": 2.2, "fx": 1.4}       # choke default, else 0.8

# Guest lanes that are PUNCTUATION, not timekeeping (owner 2026-08-01: "clap
# and crash are being overused"). Measured before the fix: every guest lane
# got gen_timekeeper's offbeats/sparse/answer grammar, so a crash cymbal was
# programmed like a shaker — 3.5 hits per BAR (median), 51 in one loop, each
# ringing 2.2s. Same for risers (3.8/bar), impacts (4.0), sirens (3.6),
# swells (3.5). Matched on the lane NAME because the pools reuse roles: a
# "rim" role carries both rims (timekeeping) and claves (timekeeping), while
# an "fx" role carries both scratches (timekeeping) and risers (punctuation).
# Matched by PREFIX, not equality: the crash guest lane is named "crash2"
# (the pools reserve "crash" for a kit lane), so an exact-match tuple silently
# missed the one lane he actually complained about. Caught by measuring after
# the change, not by reading it.
PUNCTUATION_LANES = ("crash", "impact", "swellfx", "riser", "siren",
                     "reversefx", "gamefx")


def is_punctuation(lname):
    return lname.startswith(PUNCTUATION_LANES)


def punctuation_bars(nbars, rng):
    """1-2 hits across the WHOLE loop, on a downbeat — what a crash, a riser
    or an impact actually does. Bar 1 always, and a second landing on the
    half-way bar often enough to matter but not every time."""
    bars = ["-" * 16 for _ in range(nbars)]
    bars[0] = "X" + "-" * 15
    mid = nbars // 2
    if nbars >= 4 and rng.random() < 0.55:
        bars[mid] = "X" + "-" * 15
    return bars

# ------------------------------------------------------- bar generators


def euclid(k, n, rot=0):
    """Evenly spread k hits over n steps (world-rhythm necklaces)."""
    return "".join("x" if ((i - rot) * k) % n < k else "-"
                   for i in range(n))


def _weighted(rng, modes):
    names = [m[0] for m in modes]
    weights = [m[1] for m in modes]
    return rng.choices(names, weights=weights)[0]


def gen_kick(spec, rng):
    """One bar of kick from the DJ's step-weight map. Step 0 always
    anchors; beat-start hits get capital X, syncopations lowercase."""
    w = list(spec["w"])
    hits = {0}
    target = rng.randint(*spec["hits"])
    for _ in range(60):
        if len(hits) >= target:
            break
        s = rng.choices(range(16), weights=w)[0]
        if s in hits or (s - 1 in hits and s + 1 in hits):
            continue
        hits.add(s)
    if rng.random() < spec.get("double_p", 0.2):
        s = rng.choice(sorted(hits))
        if s + 1 < 16 and s + 1 not in hits:
            hits.add(s + 1)
    return "".join(("X" if i in BEATS else "x") if i in hits else "-"
                   for i in range(16))


def gen_backbeat(spec, rng):
    """One bar of snare/clap: the DJ's mode plus ghost notes.

    The last four modes are the GENRE roster's defining figures (owner
    request 2026-07-19). They are not free-form moods like the first
    four — each one is the rhythm that makes its style that style, so
    they place exact steps and the genre presets carry them as canon
    (see compose(): a canon lane is never bank-varied or eroded)."""
    mode = _weighted(rng, spec["modes"])
    s = ["-"] * 16
    if mode == "backbeat":
        s[4] = s[12] = "X"
    elif mode == "halftime":
        s[8] = "X"
    elif mode == "displaced":
        s[4] = "X"
        s[12 + rng.choice((-1, 1))] = "X"
    elif mode == "sparse":
        s[rng.choice((4, 12))] = "X"
    # --- the frame-fix vocabulary (owner call 2026-07-22) -------------
    # The audit of 702 rendered beats found the backbeat welded to steps
    # 4 and 12: 41% of the whole library shared ONE snare line, because
    # three of the four modes above (backbeat, displaced, sparse) all
    # anchor there and only halftime ever left. These six move the frame
    # itself, which is what the ear reads as "a different beat".
    elif mode == "four":
        s[12] = "X"                  # the 4 alone — heavy, spacious
    elif mode == "push":
        s[3] = s[11] = "X"           # backbeat anticipated a 16th
    elif mode == "tresillo":
        for c in (3, 6, 11, 14):     # the 3-3-2 cell (dembow's snare
            s[c] = "X"               # half, off the genre-only list)
    elif mode == "offbeat":
        s[6] = s[14] = "X"           # the "and" of 2 and the "and" of 4
    elif mode == "drag":
        s[4] = s[12] = "X"           # boom-bap grace note into the 4
        s[11] = "x"
    elif mode == "pickup":
        s[4] = s[12] = "X"           # backbeat that pulls into the next bar
        s[15] = "x"
    elif mode == "dembow":
        # reggaeton. The snare/rim half of the dembow: two mirrored
        # tresillo cells (kick 0 +3 +6, kick 8 +3 +6) — "boom-ch-ch,
        # boom-ch-ch". Move any of these and it stops being reggaeton.
        for c in (3, 6, 11, 14):
            s[c] = "X"
    elif mode == "club":
        # Baltimore club. Backbeat on 2 and 4 with the two pushes at the
        # "a" of 2 and the "&" of 3 that give the style its forward lean.
        for c in (4, 7, 10, 12):
            s[c] = "X"
    elif mode == "bounce":
        # New Orleans bounce (Triggerman lineage): backbeat plus the
        # signature stuttered answer at the top of 4.
        for c in (4, 7, 12):
            s[c] = "X"
        s[14] = s[15] = "x"
    elif mode == "stomp":
        # crunk: 2 and 4 hit hard and land twice as often as they should
        s[4] = s[12] = "X"
        if rng.random() < 0.5:
            s[rng.choice((13, 14))] = "x"
    lo, hi = spec.get("ghosts", (0, 0)) or (0, 0)
    cells = [c for c in spec.get("gcells", []) if s[c] == "-"]
    rng.shuffle(cells)
    for c in cells[:rng.randint(lo, hi) if hi else 0]:
        s[c] = "."
    if rng.random() < spec.get("burst_p", 0.0):     # Rage's fill bursts
        at = rng.choice((13, 14))
        s[at] = s[at + 1] = "x"
    return "".join(s), mode


def gen_timekeeper(spec, rng):
    """One bar of hats/snaps in the rolled mode."""
    mode = _weighted(rng, spec["modes"])
    if mode == "eighths":
        s = list("x-" * 8)
        if rng.random() < spec.get("open_p", 0.0) * 4:
            s[rng.choice((2, 6, 10, 14))] = "o"
        return "".join(s), mode
    if mode == "sixteenths":
        return "x" * 16, mode
    if mode == "broken":                     # 16ths with holes punched
        s = ["x"] + ["x" if rng.random() > 0.4 else "-"
                     for _ in range(15)]
        return "".join(s), mode
    if mode == "sparse":
        s = ["-"] * 16
        for c in BEATS:
            s[c] = "x"
        s[rng.choice((2, 6, 10, 14))] = "x"
        return "".join(s), mode
    if mode == "offbeats":
        return "--x-" * 4, mode
    if mode == "gallop":
        return "x--xx--xx--xx--x", mode
    if mode == "answer":                     # silence, then a late reply
        s = ["-"] * 16
        for c in rng.sample((12, 13, 14, 15), rng.randint(1, 2)):
            s[c] = "x"
        return "".join(s), mode
    if mode == "quint20":                    # five against four
        s = list("x-x-" * 5)
        for g in rng.sample(range(5), rng.randint(1, 2)):
            s[g * 4 + 1] = "x"
        return "".join(s), mode
    if mode == "rolls32":                    # trap ramps into the snare
        s = list("x-" * 16)
        for _ in range(rng.randint(*spec.get("roll_n", (1, 2)))):
            endbeat = rng.choice((16, 32))   # land on beat 3 or the bar
            length = rng.choice((4, 6, 8))
            for i in range(endbeat - length, endbeat):
                s[i] = "x"
        return "".join(s), mode
    # ---- genre roster timekeepers (2026-07-19). These return a 24-step
    # bar: six per beat, so triplet 8ths land every 2 steps and triplet
    # 16ths every 1. res comes from len(bar), so the renderer places them
    # correctly with no other change (crew.grid_accent handles res 24).
    if mode == "triplets":                   # Memphis / trap triplet feel
        s = list("x-" * 12)                  # triplet 8ths
        if rng.random() < 0.35:              # sometimes double up
            s = list("x" * 24)
        if rng.random() < spec.get("open_p", 0.0) * 4:
            s[rng.choice((3, 9, 15, 21))] = "o"
        return "".join(s), mode
    if mode == "trip_rolls":                 # triplet base + roll bursts
        s = list("x-" * 12)
        for _ in range(rng.randint(*spec.get("roll_n", (1, 2)))):
            end = rng.choice((12, 24))       # into beat 3 or the bar line
            for i in range(max(0, end - rng.choice((3, 6))), end):
                s[i] = "x"
        return "".join(s), mode
    if mode == "shuffle":                    # swung 16ths: hit 1 and 3 of
        return "x-x" * 8, mode               # each triplet (bounce, club)
    if mode == "drive16":                    # electro/Miami: 16ths, opens
        s = list("x" * 16)                   # riding the offbeats
        for c in (2, 6, 10, 14):
            if rng.random() < 0.4:
                s[c] = "o"
        return "".join(s), mode
    return "x-" * 8, mode


def _mutate(pat, rng, amount):
    """Resample a fraction of the non-anchor hits: move, drop, or add —
    how a bar becomes its A' / B relatives without losing the plot."""
    s = list(pat)
    n = len(s)
    idx = [i for i, c in enumerate(s) if c in "xo." and i != 0]
    rng.shuffle(idx)
    for i in idx[:max(1, int(len(idx) * amount))]:
        r = rng.random()
        if r < 0.4:
            j = i + rng.choice((-1, 1))
            if 0 <= j < n and s[j] == "-":
                s[j], s[i] = s[i], "-"
        elif r < 0.65:
            s[i] = "-"
    if rng.random() < amount:
        gaps = [i for i, c in enumerate(s) if c == "-"]
        if gaps:
            s[rng.choice(gaps)] = "x"
    return "".join(s)


def _fill(pat, rng):
    """Phrase-tail motion for bars 4 and 8."""
    s = list(pat)
    n = len(s)
    for c in rng.sample(range(int(n * 0.75), n), max(1, n // 16)):
        if s[c] == "-":
            s[c] = "x"
    return "".join(s)


def assemble(gen_bar, rng, form=8, nbars=None):
    """The rendered bars of one lane, in one of two musical forms (owner
    call 2026-07-21): form=8 is the A/B answer — the front half states
    and decorates A, the back half answers with a B built from A's
    bones; form=4 is the loop heard straight through.

    nbars (2026-07-22) is how long THIS beat is: 4 is the new normal,
    2 is a tight MPC-style loop, 8 the old length. A short loop has no
    room for an answer, so it just states and closes with a fill."""
    nbars = int(nbars or form or 8)
    A = gen_bar()
    if nbars <= 1:
        return [A]
    if nbars == 2:
        return [A, _fill(A, rng)]
    half = [A, _mutate(A, rng, 0.15), A, _fill(A, rng)][:nbars]
    if nbars <= 4:
        return half
    if form == 4:                    # the same loop again
        return (half * (nbars // len(half) + 1))[:nbars]
    B = _mutate(A, rng, 0.45)
    if B == A:                       # the answer must actually answer
        gaps = [i for i, c in enumerate(B) if c == "-"]
        if gaps:
            s = list(B)
            s[rng.choice(gaps)] = "x"
            B = "".join(s)
    tail = [B, _mutate(B, rng, 0.15), B, _fill(B, rng)]
    return (half + tail + (tail * nbars))[:nbars]


def seed_bars(s):
    """A library seed string as a list of 16-step BARS.

    REAL BUG, found 2026-08-01 while looking for the classic breaks:
    load_library() accepts 16- and 32-step patterns (its docstring says so),
    but compose() gated every seed on `len(...) == 16`, so all 14 two-bar
    patterns — including the only Amen Break in the project — were picked,
    then silently thrown away for kick and snare. Worse, the hat path had NO
    length gate, so a 32-char string went straight through to the renderer,
    which reads `res = len(pat)` and plays 32 characters as 32 steps inside
    ONE bar: double speed, and swing skipped (`if res == 16`). Measured 48
    real cases of that on the breakbeat-tagged identities.

    A break is a TWO-BAR figure — bar 2 answering bar 1 is most of what
    makes it sound like a break rather than a loop — so the fix is to keep
    both bars, not to truncate to the first."""
    if not s:
        return []
    return [s[i:i + 16] for i in range(0, len(s), 16) if len(s[i:i + 16]) == 16]


def _seed_phrase(bars, nbars, rng, fills=True):
    """Lay a 1- or 2-bar seed figure across the beat, keeping its internal
    call-and-response, and let the closing bar of each 4-bar group breathe."""
    if not bars:
        return []
    out = []
    for b in range(nbars):
        base = bars[b % len(bars)]
        closing = fills and nbars > 1 and ((b % 4 == 3) or (b == nbars - 1))
        out.append(_fill(base, rng) if closing else base)
    return out


def _phrase(A, B, nbars, rng):
    """nbars of a NON-composed lane (the backbeat, a canon figure, a
    seeded groove): A states, B answers across the back half when the
    loop is long enough to have one, and the closing bar of each 4-bar
    group takes a fill so the phrase still breathes at any length."""
    out = []
    for b in range(nbars):
        base = B if (B and nbars >= 8 and b >= nbars // 2) else A
        closing = (b % 4 == 3) or (b == nbars - 1)
        out.append(_fill(base, rng) if closing and nbars > 1 else base)
    return out


# --------------------------------------------------------- pattern memory


def _load_pat_hist():
    try:
        return json.loads(PAT_HIST.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def remember_pattern(name, fp):
    h = _load_pat_hist()
    lst = h.setdefault(name, [])
    lst.insert(0, list(fp))
    del lst[PAT_KEEP:]
    PAT_HIST.parent.mkdir(parents=True, exist_ok=True)
    PAT_HIST.write_text(json.dumps(h))


# ------------------------------------------------------------ the composer


ODD_TSIGS = ((3, 4), (6, 8))


def _compose_odd(preset, style, name, variant, tsig):
    """Real 3/4 or 6/8 (owner ruling 2026-07-18: ~10% of beats). Both
    run 12-step bars over three quarter-note beats; 3/4 is a 16th grid
    with beats at 0/4/8, 6/8 is the compound feel with poles at 0/6.
    The loop is 3/4 the length of a 4/4 bar — the filename says so."""
    rng = random.Random("%s|%s|odd|%s" % (name, variant, tsig[0]))
    compound = tsig == (6, 8)
    poles = (0, 6) if compound else (0, 4, 8)
    notes = ["in %d/%d" % tsig]
    preset["tsig"] = list(tsig)

    def kick_bar():
        cells = {0}
        for _ in range(rng.randint(1, 4)):
            c = rng.randrange(12)
            if c - 1 not in cells and c + 1 not in cells:
                cells.add(c)
        return "".join(("X" if i in poles else "x") if i in cells else "-"
                       for i in range(12))

    def backbeat_bar():
        s = ["-"] * 12
        if compound:
            s[6] = "X"
            if rng.random() < 0.3:
                s[rng.choice((3, 9))] = "."
        else:
            for c in rng.sample((4, 8), rng.randint(1, 2)):
                s[c] = "X"
            if rng.random() < 0.3:
                s[rng.choice((2, 6, 10, 11))] = "."
        return "".join(s)

    def keeper_bar():
        pick = rng.choice(("eighths", "twelfths", "offbeats", "lilt"))
        if pick == "eighths":
            return "x-" * 6
        if pick == "twelfths":
            return "x" * 12
        if pick == "offbeats":
            return ("--x---" * 2 if compound else "--x-" * 3)
        return "x--x-x" * 2 if compound else "x-xx-x" * 2

    # odd meters take the same variable loop length as everything else
    # (2026-07-22); a 3/4 or 6/8 bar is already shorter, so the tight
    # 2-bar loop is left off this path — it would fly past.
    nbars = rng.choices((4, 8), weights=(0.65, 0.35))[0]
    preset["bars"] = nbars

    for lane in list(preset["lanes"]):
        if lane.startswith("stamp"):
            continue                     # stamps ride their own grids
        pan, gain, feel, _ = preset["lanes"][lane]
        if lane == "kick":
            bars = assemble(lambda: kick_bar(), rng, nbars=nbars)
        elif lane in ("snare", "clap"):
            bars = _phrase(backbeat_bar(), None, nbars, rng)
        else:
            bars = _phrase(keeper_bar(), None, nbars, rng)
        preset["lanes"][lane] = (pan, gain, feel, bars)

    flavors = style["kick_flavors"]            # the style's own, unfiltered
    fi = rng.choices(range(len(flavors)),
                     weights=[f[0] for f in flavors])[0]
    _, must, wants, secs = flavors[fi]
    role, _, _, _ = preset["kit"]["kick"]
    preset["kit"]["kick"] = (role, must, list(wants), tuple(secs))
    notes.append("kick: " + ("808 " if must else "clean/short ")
                 + "+".join(wants[:2]))
    remember_pattern(name, (preset["lanes"]["kick"][3][0], "odd", "", fi))
    return notes


def compose(preset, name, variant, boom_bap=False, tsig=None, trick=False,
            traditional=False):
    """Rewrite the preset's lane patterns fresh from the DJ's grammar,
    roll a form (4-bar loop or 8-bar A/B) and a kick flavor, and maybe
    seat guest lanes. Deterministic per (name, variant).
    Returns plain-words notes for the README.
    Timing DNA (pan, gain, LaneFeel) is carried over untouched.
    tsig=(3,4)/(6,8) takes the real odd-meter path; trick=True boosts
    the exotic grids (quintuplets, 32nd walls, gallops) inside 4/4.

    traditional=True (owner rule 2026-07-18: half of every 4+ batch is a
    common, popular hip-hop beat): the kick comes straight from the DJ's
    curated bank and the snare/clap lock to a plain 2&4 backbeat — the
    backbone stays conventional. Everything else (hats, perc, guests, fx)
    still rolls free, so the beat is familiar without being generic.
    legend presets follow their producer faithfully: no bank cross-
    pollination borrows another book INTO them.

    genre presets (the subgenre roster, 2026-07-19) go further: the
    lanes named in preset["canon"] carry the figure that DEFINES the
    style — the dembow, the Baltimore 8-count, the Triggerman answer —
    and are placed verbatim from that genre's authentic variants rather
    than composed or bank-varied. Everything not in canon (hats, perc,
    guests, fills, flavors, samples) still rolls free, so the beats
    differ from each other without the style eroding. compose() records
    the canon lanes on the preset so vary_preset leaves them alone."""
    legend = preset.get("legend")
    genre = preset.get("genre")
    canon = preset.get("canon") or {}
    style = {k: preset.get(k) or DEFAULT_STYLE.get(name, {}).get(k)
             for k in ("grammar", "kick_flavors", "extras", "library")}
    if tsig and tuple(tsig) in ODD_TSIGS:
        return _compose_odd(preset, style, name, variant, tuple(tsig))
    if traditional:
        # keep the backbone common. Library seeds stay in play at half
        # strength but only from the hiphop file (owner call 2026-07-21:
        # switching the library fully off here meant half of every batch
        # never saw it, and 2&4-plus-house-grammar took over the whole
        # library's sound).
        #
        # 2026-07-22: this used to pin modes=[["backbeat", 1.0]], and
        # since traditional is ~a quarter of every batch that alone
        # welded a bare 2&4 under a third of the library. "Traditional"
        # should mean FAMILIAR, not identical. Every mode below is an
        # unimpeachably common hip-hop backbone — the boom-bap grace
        # note, the pickup into the next bar, one of the two backbeats
        # alone, the halftime 3 — so these beats still read as the
        # plain popular thing without being literally the same line
        # every time. The exotic cells (tresillo, offbeat, push) stay
        # out of the traditional path on purpose.
        g = {}
        for lane, spec in style["grammar"].items():
            if isinstance(spec, dict) and "modes" in spec \
                    and "gcells" in spec:
                g[lane] = dict(spec, modes=[["backbeat", 0.45],
                                            ["drag", 0.20],
                                            ["pickup", 0.15],
                                            ["sparse", 0.10],
                                            ["halftime", 0.10]])
            else:
                g[lane] = spec
        lib = dict(style.get("library") or {})
        lib["p"] = lib.get("p", 0) * 0.5
        lib["genres"] = ["hiphop"]
        style = dict(style, grammar=g, library=lib)
    if trick:
        # exotic-grid beat: the timekeeper reaches for the odd stuff
        g = {}
        for lane, spec in style["grammar"].items():
            if isinstance(spec, dict) and "modes" in spec \
                    and "gcells" not in spec:
                exotic = [[m, 3.0 if m in ("quint20", "rolls32", "gallop",
                                           "answer") else w]
                          for m, w in spec["modes"]]
                if not any(m == "quint20" for m, _ in exotic):
                    exotic.append(["quint20", 2.0])
                g[lane] = dict(spec, modes=exotic)
            else:
                g[lane] = spec
        style = dict(style, grammar=g)
    past = [tuple(f) for f in _load_pat_hist().get(name, [])]

    # the ≥3-moves repeat guard and its 40-attempt regenerate loop are
    # gone (owner call 2026-07-21: variety comes from the composition
    # itself, not from rejection; the guard bogged batches down and
    # pushed rolls toward weird corners of the space). One rule stays,
    # the weakest possible: never LITERALLY repeat a recent kick bar —
    # an exact match re-rolls, anything else ships.
    for attempt in range(6):
        rng = random.Random(f"{name}|{variant}|pattern|{attempt}")
        lanes, modes, notes = {}, {}, []
        # LOOP LENGTH — OWNER RULE 2026-08-01: "For all other beats
        # regardless of DJ, four to eight bars." Supersedes both the
        # 2026-07-22 call ("make the loops half as long", which is what put
        # 2-bar loops on the table at 15%) and the 2026-07-23 J Dillo pin
        # ("no long beats", bar_lengths [2, 4]) — "regardless of DJ" is
        # explicit, so a preset's own bar_lengths is now filtered to the
        # allowed set rather than obeyed outright. A genre still leans long:
        # the subgenre roster's figures need room to state themselves.
        ALLOWED_BARS = (4, 8)
        pinned = [n for n in (preset.get("bar_lengths") or ())
                  if n in ALLOWED_BARS]
        nbars = (rng.choice(pinned) if pinned else
                 8 if genre else rng.choices(ALLOWED_BARS,
                                             weights=(0.60, 0.40))[0])
        preset["bars"] = nbars
        # form roll (owner call 2026-07-21): half the beats are the loop
        # heard straight through, half the A/B answer form. Only an
        # 8-bar loop is long enough to hold an answer.
        form = 4 if (nbars < 8 or rng.random() < 0.5) else 8
        notes.append("%d-bar %s" % (nbars, "loop" if form == 4 else "A/B"))

        # groove-library seed (2026-07-17, wired in with the variety
        # engine): sometimes this beat starts from one of the 131
        # reference grooves, weighted by the DJ's genre taste. Kick and
        # hat lines, plus sometimes the snare on a crew beat (owner
        # call 2026-07-21) — and the seed still passes _bank_vary, the
        # sparse thinning, and both repeat guards: an influence, never
        # a copy. Boom-bap mode keeps its own hat law, so no hat seed.
        lib_seed = None
        lib = style.get("library")
        # OWNER 2026-08-01, on how faithful a classic break should be:
        # "for break beats, stay verbatim". `break_beat` is set by the notes
        # box ("break", "amen", "funky drummer", ...) — see
        # beat_machine.parse_directions. On those beats the seed pool is
        # restricted to the real transcriptions and the figure is played as
        # written; every other beat keeps treating the library as an
        # influence that gets thinned and varied, which is the 2026-07-17
        # behaviour and is unchanged.
        verbatim = bool(preset.get("break_beat"))
        if verbatim:
            lib_seed = _pick_break(rng)
        elif lib and rng.random() < lib.get("p", 0):
            lib_seed = _pick_library(lib, rng)

        # core lanes, in grammar order so copies can follow their source
        for lane, spec in style["grammar"].items():
            if lane not in preset["lanes"]:
                continue
            if boom_bap and lane == "hat":   # bb hats stay hats, swung
                spec = dict(spec, modes=[["eighths", 0.5],
                                         ["sixteenths", 0.5]])
            if "copy" in spec:
                src = spec["copy"]
                if src in lanes:
                    lanes[lane] = [b.replace(".", "-") for b in lanes[src]]
                continue
            if "euclid" in spec:
                k = rng.choice(spec["euclid"])
                bar = euclid(k, 16, rot=rng.randrange(16))
                lanes[lane] = assemble(lambda: bar, rng, form, nbars)
                modes[lane] = f"E({k},16)"
                continue
            if lane in canon:
                # the genre's defining figure: placed exactly as the
                # style plays it, one of that genre's authentic variants.
                # On a traditional beat it's variant 0 — for a genre,
                # "traditional" means the textbook version of THAT style
                # (owner rule 2026-07-19), not a generic 2&4 backbone,
                # which would simply stop being reggaeton or club.
                bar = canon[lane][0] if traditional else rng.choice(canon[lane])
                if lane == "kick":
                    lanes[lane] = assemble(lambda: bar, rng, form, nbars)
                else:
                    lanes[lane] = _phrase(bar, None, nbars, rng)
                    modes[lane] = "canon"
                continue
            if lane == "kick":
                # usually start from a curated skeleton in the DJ's bank
                # (owner 2026-07-17: a larger pattern library), sometimes
                # a groove-library seed or a freestyle from the weight
                # map — then vary either way
                bank = BOOM_BAP_KICKS if boom_bap \
                    else KICK_BANK.get(name, [])
                # v6: banks cross-pollinate — 15% of bank picks borrow
                # another DJ's vocabulary (variety over style fidelity).
                # NEVER into a legend (likeness), a genre (the figure IS
                # the style) or a traditional beat (the borrowed line
                # could be exotic); legends only borrow from other
                # legends' books, never the loose nine.
                if not boom_bap and not legend and not genre \
                        and not traditional and rng.random() < 0.15:
                    donor = rng.choice([d for d in KICK_BANK if d != name])
                    bank = KICK_BANK[donor]
                    notes.append("kick borrowed from %s's book" % donor)
                kick_seed = seed_bars(lib_seed.get("kick", "")) \
                    if lib_seed else []
                if len(kick_seed) > 1 and verbatim:
                    # a two-bar break played as written (owner 2026-08-01:
                    # break beats stay verbatim). No thinning, no bank-vary —
                    # those are what turn a break back into generic
                    # syncopation, which is exactly why the library never
                    # sounded like the records it was modelled on.
                    lanes[lane] = _seed_phrase(kick_seed, nbars, rng,
                                               fills=False)
                    notes.append("BREAK, played straight: %s"
                                 % lib_seed["name"])
                    continue
                if kick_seed:
                    barA = _bank_vary(_thin_kick(kick_seed[0], rng),
                                      spec, rng)
                    notes.append("groove seed: %s (%s)"
                                 % (lib_seed["name"], lib_seed["subgenre"]
                                    or lib_seed["genre"]))
                elif bank and (traditional or rng.random() < 0.75):
                    barA = _bank_vary(rng.choice(bank), spec, rng)
                else:
                    barA = gen_kick(spec, rng)
                lanes[lane] = assemble(lambda: barA, rng, form, nbars)
                continue
            if "modes" in spec and "gcells" in spec:      # backbeat lane
                # the backbeat may follow the groove seed on a crew beat
                # (owner call 2026-07-21: 75% of the library sat on a
                # bare 2&4 — the loudest lane never moved). Legends keep
                # their own book (likeness) and traditional beats stay
                # locked to 2&4 by definition.
                # ...but a seed whose snare is the bare 2&4 teaches the
                # engine nothing it isn't already over-supplied with
                # (2026-07-22 audit: seeded lanes were landing on the
                # plain line ~28% of the time, reinforcing the very
                # thing the seed was meant to break). Those fall through
                # to the DJ's own roll; every other seed still lands.
                sn_seed = seed_bars(lib_seed.get("snare", "")) \
                    if lib_seed else []
                # OWNER 2026-08-01: legends may now take a groove seed's
                # backbeat. Measured on 720 legend beats under the old rule,
                # a legend received one 0.0% of the time — and the legends
                # are precisely the producers whose whole style was built on
                # sampled breaks, so the one identity group that most needed
                # the Funky Drummer could never have it. `traditional` still
                # locks to 2&4 by definition, and a bare 2&4 seed still
                # teaches nothing so it still falls through.
                if sn_seed and sn_seed[0] != "----X-------X---" \
                        and not traditional \
                        and (verbatim or rng.random() < 0.5):
                    if verbatim and len(sn_seed) > 1:
                        lanes[lane] = _seed_phrase(sn_seed, nbars, rng,
                                                   fills=False)
                    else:
                        lanes[lane] = _phrase(sn_seed[0], None, nbars, rng)
                    modes[lane] = "seed:" + (lib_seed["subgenre"]
                                             or lib_seed["genre"])
                    continue
                # otherwise the backbeat is identity: its mode holds for
                # the whole beat, B answers with fresh ghosts, motion
                # lives only in the phrase-tail fills
                barA, mode = gen_backbeat(spec, rng)
                barB = None if form == 4 else \
                    gen_backbeat(dict(spec, modes=[[mode, 1]]), rng)[0]
                lanes[lane] = _phrase(barA, barB, nbars, rng)
                modes[lane] = mode
                continue
            hat_seed = seed_bars(lib_seed.get("hat", "")) if lib_seed else []
            if lane == "hat" and not boom_bap and hat_seed:
                # was: `bar = lib_seed["hat"]` with no length check, so a
                # two-bar seed handed the renderer a 32-char bar and played
                # at double speed with swing off. seed_bars splits it.
                mode = "seed:" + (lib_seed["subgenre"] or lib_seed["genre"])
                lanes[lane] = _seed_phrase(hat_seed, nbars, rng,
                                           fills=not verbatim)
                modes[lane] = mode
                continue
            bar, mode = gen_timekeeper(spec, rng)
            if mode == "answer":             # call-and-response bar pairs
                lanes[lane] = (["-" * len(bar), bar] * nbars)[:nbars]
            else:
                lanes[lane] = _phrase(bar, None, nbars, rng)
            modes[lane] = mode

        # kick flavor: the style's declared weights, 808 included (owner
        # rule 2026-07-23, second call — see the note above the kick
        # banks). The streak-breaker below still stops any flavor running
        # three beats in a row.
        flavors = BOOM_BAP_FLAVORS if boom_bap else style["kick_flavors"]
        weights = [f[0] for f in flavors]
        # The streak-breaker keeps a crew DJ off a run of long 808s. A
        # subgenre is exempt (owner rule 2026-07-19): the long decaying
        # 808 IS Miami bass and IS a screw beat, so forcing variety here
        # dragged an 80/20 lean down to 57/43 and took the style with
        # it. Their declared weights are the point — let them hold.
        if not genre and len(past) >= 2 and past[0][3] == past[1][3] \
                and len(flavors) > 1 and past[0][3] < len(flavors):
            weights = [0 if i == past[0][3] else w
                       for i, w in enumerate(weights)]
        fi = rng.choices(range(len(flavors)), weights=weights)[0]
        _, must, wants, secs = flavors[fi]

        fp = (lanes["kick"][0], modes.get("snare", modes.get("clap", "")),
              modes.get("hat", modes.get("snap", "")), fi)
        # genres repeat their canon figure by design; everyone else only
        # re-rolls on an exact kick-bar repeat of a recent roll
        if genre or fp[0] not in {old[0] for old in past}:
            break

    for lane, bars in lanes.items():
        pan, gain, feel, _ = preset["lanes"][lane]
        preset["lanes"][lane] = (pan, gain, feel, bars)
    if canon:
        # tell the variety pass which lanes carry the style (beat_machine
        # .vary_preset gives these the gentle anchor wander it already
        # gives the kick, instead of the drop/add mutation that would
        # quietly turn a dembow into generic syncopation)
        preset["_canon"] = sorted(canon)
    role, _, _, _ = preset["kit"]["kick"]
    preset["kit"]["kick"] = (role, must, list(wants), tuple(secs))
    notes.append("kick: " + ("808 " if must else "clean/short ")
                 + "+".join(wants[:2]))
    for lane in ("snare", "clap", "hat", "snap", "perc", "bongo"):
        if lane in modes:
            notes.append(f"{lane}: {modes[lane]}")

    # guest lanes: the rest of the library gets a seat (owner verdict)
    ex = style["extras"]
    n_extra = 0
    if rng.random() < ex["p"]:
        n_extra = rng.randint(1, ex["nmax"])
    pool = [tuple(e) for e in ex["pool"]]
    rng.shuffle(pool)
    swing = max(ln[2][2] for ln in preset["lanes"].values())
    for role, wants, lname in pool[:n_extra]:
        if lname in preset["lanes"]:
            continue
        punct = is_punctuation(lname)
        if punct:
            mode = "punctuation"
            bar = None
        else:
            bar, mode = gen_timekeeper(
                dict(modes=[["offbeats", 2], ["sparse", 2], ["answer", 1]]),
                rng)
        side = rng.choice((-1, 1)) * rng.uniform(0.15, 0.35)
        # a guest normally coin-flips between the beat's swing and
        # straight 50 — that deliberate clash is a v6 crew trick. A
        # subgenre can't afford it (2026-07-19): one straight lane in a
        # 62%-swung Wonky beat, or in a reggaeton, reads as a mistake,
        # so genre guests ride the style's own feel.
        gswing = swing if (genre or rng.random() < 0.5) else 50
        preset["lanes"][lname] = (
            round(side, 2), round(rng.uniform(0.22, 0.36), 2),
            (0, rng.uniform(1.5, 4.0), gswing,
             rng.randrange(1, 99999)),
            punctuation_bars(nbars, rng) if punct
            else (["-" * len(bar), bar] * nbars)[:nbars] if mode == "answer"
            else _phrase(bar, None, nbars, rng))
        preset["kit"][lname] = (role, None, list(wants),
                                EXTRA_SECS.get(role, 0.8))
        preset.setdefault("_guests", []).append(lname)
        notes.append(f"guest {lname} ({mode})")

    remember_pattern(name, fp)
    return notes
