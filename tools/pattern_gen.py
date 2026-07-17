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
  DJ's recent rhythms; a too-similar roll regenerates (up to 12 tries).

Timing DNA (LaneFeel offsets, swing) and the locked stamps are never
touched — the character survives; the rhythm doesn't repeat.
"""
import json
import os
import random
from pathlib import Path

PAT_HIST = Path(os.path.expanduser("~/.reason_voice/pattern_history.json"))
PAT_KEEP = 24
BEATS = (0, 4, 8, 12)
STYLE_VERSION = 5      # bump when DEFAULT_STYLE changes (config auto-syncs)

# ------------------------------------------------- the groove library
# Owner drop 2026-07-17 (second library expansion): 131 genre-tagged
# reference grooves with per-lane velocity grids, built in a separate
# session and imported to <project>/pattern_library/. compose() may
# reach for one as this beat's seed — the kick and hat lines only; the
# backbeat stays with the DJ's own grammar (identity rule). Every
# seeded line still passes _bank_vary, the sparse-bed thinning, and
# both repeat guards, so a groove seed reads as an influence, never a
# copy. Per-DJ taste (which genres, how often) lives in the "library"
# style key in crew_config.json — tune it there.

LIB_DIR = Path(__file__).resolve().parent.parent / "pattern_library"
_LIB_CACHE = None


def _lib_kick(vels):
    n = len(vels)
    caps = set(range(0, n, n // 4))
    return "".join(("X" if i in caps else "x") if v else "-"
                   for i, v in enumerate(vels))


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
            hat = _lib_hat(tr, n)
            if hat and hat.count("-") < n:
                entry["hat"] = hat
            if "kick" in entry or "hat" in entry:
                pats.append(entry)
    _LIB_CACHE = pats
    return pats


def _pick_library(spec, rng):
    """One groove, weighted by this DJ's genre taste. Tags match the
    subgenre at full weight, the whole genre file at half."""
    pats = load_library()
    tags = {t: w for t, w in spec.get("tags", [])}
    weights = [tags.get(p["subgenre"], 0) + 0.5 * tags.get(p["genre"], 0)
               for p in pats]
    if not any(weights):
        return None
    return rng.choices(pats, weights=weights)[0]


def _thin_kick(bar, rng):
    """The sparse-bed rule (2026-07-17): he plays over the top, so the
    kick stays ~2-5 hits per 16 steps. Library grooves that run hotter
    (d-beat, four-on-floor plus doubles) shed lowercase hits first."""
    cap = max(2, round(5 * len(bar) / 16))
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

DEFAULT_STYLE = {
    "Otto Grit": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 1, 2, 1, 1, 3, 6, 3, 1, 5, 2, 1, 3, 5, 2],
                      hits=[2, 4], double_p=0.3),
            snare=dict(modes=[["backbeat", 0.7], ["displaced", 0.15],
                              ["sparse", 0.15]],
                       ghosts=[0, 3], gcells=[3, 7, 11, 14, 15]),
            hat=dict(modes=[["eighths", 0.3], ["sixteenths", 0.1],
                            ["sparse", 0.35], ["broken", 0.25]],
                     open_p=0.08),
        ),
        kick_flavors=[[0.4, "808", ["dust", "boom", "dirty"], [0.35, 0.9]],
                      [0.6, None, ["boom", "punch", "acoustic", "break",
                                   "knock"], [0.18, 0.5]]],
        library=dict(p=0.35, tags=[["lofi", 3], ["boom-bap", 2],
                                   ["neo-soul", 2]]),
        extras=dict(p=0.55, nmax=1, pool=[
            ["perc", ["tamb", "shaker"], "shaker"],
            ["rim", ["rim", "stick"], "rims"],
            ["perc", ["tom"], "toms"],
            ["fx", ["vinyl", "reverse", "foley"], "foundfx"]]),
    ),
    "Cutz": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 0, 5, 1, 0, 2, 1, 1, 0, 5, 1, 0, 5, 1, 1],
                      hits=[2, 4], double_p=0.15),
            snare=dict(modes=[["backbeat", 0.9], ["displaced", 0.1]],
                       ghosts=[0, 2], gcells=[6, 7, 15]),
            hat=dict(modes=[["eighths", 0.4], ["offbeats", 0.35],
                            ["broken", 0.25]], open_p=0.04),
        ),
        kick_flavors=[[0.3, "808", ["punch", "hard"], [0.3, 0.7]],
                      [0.7, None, ["punch", "knock", "hard", "acoustic"],
                       [0.15, 0.45]]],
        library=dict(p=0.3, tags=[["boom-bap", 4], ["funk", 1]]),
        extras=dict(p=0.45, nmax=1, pool=[
            ["fx", ["scratch"], "cutfx"],
            ["rim", ["rim", "stick"], "rims"],
            ["perc", ["shaker", "tamb"], "shaker"]]),
    ),
    "Crate Prophet": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 2, 1, 0, 1, 4, 4, 1, 1, 4, 1, 3, 1, 4, 1],
                      hits=[2, 4], double_p=0.2),
            snare=dict(modes=[["backbeat", 0.85], ["displaced", 0.15]],
                       ghosts=[1, 3], gcells=[2, 3, 7, 10, 15]),
            hat=dict(modes=[["eighths", 0.4], ["sparse", 0.35],
                            ["broken", 0.25]], open_p=0.2),
            bongo=dict(euclid=[3, 5]),
        ),
        kick_flavors=[[0.35, "808", ["warm", "deep"], [0.4, 0.9]],
                      [0.65, None, ["boom", "warm", "break", "acoustic"],
                       [0.2, 0.5]]],
        library=dict(p=0.35, tags=[["boom-bap", 3], ["soul", 2],
                                   ["lofi", 1], ["funk", 1]]),
        extras=dict(p=0.6, nmax=1, pool=[
            ["perc", ["conga", "bongo"], "congas2"],
            ["perc", ["shaker", "tamb"], "shaker"],
            ["fx", ["vinyl", "reverse", "foley"], "foundfx"]]),
    ),
    "Chrome Dial": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 0, 6, 0, 0, 4, 0, 3, 0, 2, 4, 0, 2, 3, 1],
                      hits=[3, 5], double_p=0.45),
            clap=dict(modes=[["backbeat", 0.7], ["displaced", 0.3]],
                      ghosts=[0, 0], gcells=[]),
            snap=dict(modes=[["answer", 0.6], ["offbeats", 0.4]]),
            perc=dict(euclid=[5, 7]),
        ),
        kick_flavors=[[0.2, "808", ["clean", "tight"], [0.3, 0.6]],
                      [0.8, None, ["clean", "punch", "tight", "pop"],
                       [0.12, 0.4]]],
        library=dict(p=0.35, tags=[["rnb", 3], ["garage", 2],
                                   ["funk", 1], ["electro", 1]]),
        extras=dict(p=0.6, nmax=1, pool=[
            ["perc", ["tabla", "block", "cowbell"], "exotic2"],
            ["fx", ["zap", "laser", "glitch"], "blips"],
            ["rim", ["rim", "click"], "clicks"]]),
    ),
    "Glass Cat": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 0, 2, 0, 0, 1, 0, 6, 0, 4, 0, 0, 1, 1, 1],
                      hits=[2, 3], double_p=0.05),
            snare=dict(modes=[["backbeat", 0.7], ["displaced", 0.1],
                              ["sparse", 0.2]],
                       ghosts=[0, 0], gcells=[]),
            clap=dict(copy="snare"),          # the documented late flam
            snap=dict(modes=[["eighths", 0.3], ["sparse", 0.4],
                             ["gallop", 0.3]]),
        ),
        kick_flavors=[[0.15, "808", ["clean"], [0.25, 0.5]],
                      [0.85, None, ["clean", "tight", "pop", "punch"],
                       [0.1, 0.35]]],
        library=dict(p=0.3, tags=[["rnb", 2], ["minimal", 2],
                                  ["funk", 2], ["cloud-rap", 1]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["fx", ["glitch", "zap", "laser"], "blips"],
            ["perc", ["block", "clave"], "woods"]]),
    ),
    "Sunday Chop": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 0, 1, 4, 0, 1, 4, 8, 0, 1, 1, 4, 0, 2, 3],
                      hits=[3, 5], double_p=0.25),
            clap=dict(modes=[["backbeat", 0.9], ["displaced", 0.1]],
                      ghosts=[0, 0], gcells=[]),
            snare=dict(copy="clap"),          # tucked under the big clap
            hat=dict(modes=[["eighths", 0.45], ["sixteenths", 0.3],
                            ["broken", 0.25]], open_p=0.06),
            perc=dict(modes=[["offbeats", 1.0]]),
        ),
        kick_flavors=[[0.3, "808", ["punch", "knock"], [0.3, 0.7]],
                      [0.7, None, ["punch", "knock", "clean"],
                       [0.15, 0.45]]],
        library=dict(p=0.35, tags=[["soul", 3], ["motown", 2],
                                   ["boom-bap", 2]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["perc", ["tamb", "shaker"], "shaker"],
            ["crash", ["crash"], "crash2"],
            ["fx", ["reverse", "impact"], "swellfx"]]),
    ),
    "Night Metro": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 0, 3, 0, 0, 5, 0, 1, 0, 4, 1, 3, 0, 1, 1],
                      hits=[2, 3], double_p=0.15),
            clap=dict(modes=[["halftime", 1.0]],
                      ghosts=[0, 0], gcells=[]),
            hat=dict(modes=[["rolls32", 0.5], ["sixteenths", 0.5]],
                     roll_n=[1, 2]),
        ),
        kick_flavors=[[0.2, "808", ["deep", "sub", "long"], [0.9, 2.0]],
                      [0.25, "808", ["deep", "sub"], [0.4, 0.8]],
                      [0.55, None, ["punch", "deep", "knock"],
                       [0.25, 0.6]]],
        library=dict(p=0.35, tags=[["trap", 4], ["cloud-rap", 2],
                                   ["drill", 1]]),
        extras=dict(p=0.45, nmax=1, pool=[
            ["fx", ["riser", "reverse", "sweep"], "risers"],
            ["perc", ["cowbell", "block"], "bells"]]),
    ),
    "Rage Engine": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 0, 2, 0, 0, 6, 0, 1, 0, 1, 1, 6, 0, 1, 2],
                      hits=[2, 4], double_p=0.35),
            snare=dict(modes=[["halftime", 1.0]],
                       ghosts=[0, 0], gcells=[], burst_p=0.5),
            clap=dict(copy="snare"),
            hat=dict(modes=[["rolls32", 0.55], ["sixteenths", 0.45]],
                     roll_n=[1, 2]),
        ),
        kick_flavors=[[0.2, "808", ["hard", "distort"], [0.8, 1.8]],
                      [0.25, "808", ["hard", "punch"], [0.35, 0.7]],
                      [0.55, None, ["hard", "punch", "knock"],
                       [0.2, 0.5]]],
        library=dict(p=0.35, tags=[["trap", 4], ["drill", 2]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["crash", ["crash", "impact"], "impacts"],
            ["fx", ["riser", "sweep"], "sirens"]]),
    ),
    "New Math": dict(
        grammar=dict(
            kick=dict(w=[10, 0, 0, 7, 0, 0, 6, 0, 6, 0, 5, 0, 2, 0, 2, 1],
                      hits=[3, 5], double_p=0.3),
            snare=dict(modes=[["backbeat", 0.5], ["displaced", 0.5]],
                       ghosts=[0, 1], gcells=[10, 15]),
            snap=dict(modes=[["offbeats", 0.6], ["answer", 0.4]]),
            hat=dict(modes=[["quint20", 0.4], ["sixteenths", 0.2],
                            ["gallop", 0.4]]),
            perc=dict(euclid=[5, 7]),
        ),
        kick_flavors=[[0.3, "808", ["punch", "club"], [0.4, 1.0]],
                      [0.7, None, ["punch", "knock", "club", "tight"],
                       [0.15, 0.45]]],
        library=dict(p=0.4, tags=[["garage", 3], ["breakbeat", 2],
                                  ["jungle", 1], ["dnb", 1],
                                  ["electro", 1], ["drill", 1]]),
        extras=dict(p=0.65, nmax=1, pool=[
            ["fx", ["glitch", "laser", "zap", "reverse"], "glitches"],
            ["perc", ["block", "clave", "tabla"], "mathperc"],
            ["rim", ["rim", "click"], "clicks"]]),
    ),
}

# New Math's boom-bap mode reaches for dusty, short drums instead
BOOM_BAP_FLAVORS = [[0.5, "808", ["boom", "dust", "dirty"], [0.35, 0.8]],
                    [0.5, None, ["boom", "punch", "knock", "acoustic"],
                     [0.18, 0.5]]]

# ------------------------------------------------------- the kick banks
# Owner request 2026-07-17: a LARGER library of patterns. Each DJ carries
# ~10 curated kick skeletons in their vocabulary — real moves from their
# style lane, not one generator's habits. The composer usually starts
# from one of these (then varies it inside the grammar); sometimes it
# still freestyles from the weight map. History keeps repeats away.

KICK_BANK = {
    "Otto Grit": [                            # drunk, off-the-grid leans
        "X------x--X-----", "X--x------X--x--", "X------xX---x---",
        "X-----x---X----x", "X--x---x--X-x---", "X---x-----Xx----",
        "X------x-X---x--", "X-x-----x-X-----", "Xx-----x--X--x--",
        "X-----xx--X----x"],
    "Cutz": [                                 # surgical, sparse punches
        "X--x------X-----", "X---------X--x--", "X--x--x---X-----",
        "X-x-------X---x-", "X--x------Xx----", "X---x-----X--x--",
        "X--------xX-----", "X--x---x--X--x--", "X---------X-x---",
        "X-xx------X-----"],
    "Crate Prophet": [                        # warm golden-era rollers
        "X-----x---X--x--", "X--x--x---X-----", "X-----x-x-X-----",
        "X---x-----X-x---", "X-----xx--X--x--", "X-x---x---X-----",
        "X-----x---X-xx--", "X--x------X---x-", "X-----x--xX-----",
        "X---xx----X--x--"],
    "Chrome Dial": [                          # stutters and syncopation
        "X--X--X---------", "X--X--X---X-----", "X-----X--X--X---",
        "X--X----X-X-----", "X---XX----X-----", "X--X--X--X--X---",
        "X-----X---XX----", "X--X---X--X---X-", "XX----X---X-----",
        "X---X--X----X---"],
    "Glass Cat": [                            # minimal, negative space
        "X-------X-X-----", "X---------X---X-", "X-------X-------",
        "X--X----X-------", "X-------XX------", "X---X---X-X-----",
        "X-------X---X---", "X-X-----X-------"],
    "Sunday Chop": [                          # gospel drive, pushed 8ths
        "X---x---X---x---", "X---x--xX---x---", "X--xX---X---x---",
        "X---x---X--xx---", "X---X---X---X---", "X---x-x-X---x---",
        "X---x---X-x-x---", "Xx--x---X---x---"],
    "Night Metro": [                          # halftime dark sparse
        "X-----X---X-----", "X---------X-----", "X-----X-------X-",
        "X------X--X-----", "X-----X---X---X-", "X---------X--X--",
        "X-----X-----X---", "X--------X-X----"],
    "Rage Engine": [                          # relentless triplet-feel
        "X-----X-----X---", "X-----X-----X--X", "X--X--X-----X---",
        "X-----X---X-X---", "X-----XX----X---", "X--X--X--X--X---",
        "XX----X-----X---", "X-----X-----XX--"],
    "New Math": [                             # Jersey claves + necklaces
        "X--X--X-X-X-----", "X--X--X-X-------", "X--X---X--X-X---",
        "X-X--X--X-X-----", "X--X-X--X--X----", "X--X--X-X-X-X---",
        "X---X-X--X--X---", "X--XX--X--X-----"],
}

BOOM_BAP_KICKS = [                            # New Math's odd-variant lane
    "X------x--X-----", "X--x------X--x--", "X-----x---X--x--",
    "X------xX---x---", "X--x--x---X-----", "X-----x-x-X-----"]


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
    """One bar of snare/clap: the DJ's mode plus ghost notes."""
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


def assemble(gen_bar, rng):
    """8 bars, A/B form: bars 1-4 state and decorate A, bars 5-8 answer
    with a B built from A's bones, both phrases ending in a fill."""
    A = gen_bar()
    B = _mutate(A, rng, 0.45)
    return [A, _mutate(A, rng, 0.15), A, _fill(A, rng),
            B, _mutate(B, rng, 0.15), B, _fill(B, rng)]


# --------------------------------------------------------- pattern memory


def _load_pat_hist():
    try:
        return json.loads(PAT_HIST.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _too_close(fp, past):
    """A rhythm counts as a repeat when its kick bar sits within 2 moves
    of a recent one (hard floor, no matter what the other lanes do), or
    within 3 while the backbeat+timekeeper modes also match."""
    for old in past:
        if len(old[0]) != len(fp[0]):
            continue
        d = sum(a != b for a, b in zip(old[0], fp[0]))
        if d < 3 or (d < 4 and old[1:] == fp[1:]):
            return True
    return False


def kick_seen(name, bar, thresh=3):
    """Has this DJ recently RENDERED a kick line within thresh moves of
    this one? Checked on the final post-variety pattern (2026-07-17:
    the compose-time guard missed collapses that happened later)."""
    past = _load_pat_hist().get(name + "#final", [])
    return any(len(o[0]) == len(bar)
               and sum(a != b for a, b in zip(o[0], bar)) < thresh
               for o in past)


def remember_kick(name, bar):
    h = _load_pat_hist()
    lst = h.setdefault(name + "#final", [])
    lst.insert(0, [bar])
    del lst[PAT_KEEP:]
    PAT_HIST.parent.mkdir(parents=True, exist_ok=True)
    PAT_HIST.write_text(json.dumps(h))


def remember_pattern(name, fp):
    h = _load_pat_hist()
    lst = h.setdefault(name, [])
    lst.insert(0, list(fp))
    del lst[PAT_KEEP:]
    PAT_HIST.parent.mkdir(parents=True, exist_ok=True)
    PAT_HIST.write_text(json.dumps(h))


# ------------------------------------------------------------ the composer


def compose(preset, name, variant, boom_bap=False):
    """Rewrite the preset's lane patterns fresh from the DJ's grammar,
    roll a kick flavor, and maybe seat 1-2 guest lanes. Deterministic per
    (name, variant, attempt); regenerates if the rhythm is too close to
    one this DJ made recently. Returns plain-words notes for the README.
    Timing DNA (pan, gain, LaneFeel) is carried over untouched."""
    style = {k: preset.get(k) or DEFAULT_STYLE[name].get(k)
             for k in ("grammar", "kick_flavors", "extras", "library")}
    past = [tuple(f) for f in _load_pat_hist().get(name, [])]

    best, best_d = None, -1
    for attempt in range(40):
        rng = random.Random(f"{name}|{variant}|pattern|{attempt}")
        lanes, modes, notes = {}, {}, []

        # groove-library seed (2026-07-17, wired in with the variety
        # engine): sometimes this beat starts from one of the 131
        # reference grooves, weighted by the DJ's genre taste. Kick and
        # hat lines only — the backbeat stays with the DJ's own grammar
        # (identity rule) — and the seed still passes _bank_vary, the
        # sparse thinning, and both repeat guards: an influence, never
        # a copy. Boom-bap mode keeps its own hat law, so no hat seed.
        lib_seed = None
        lib = style.get("library")
        if lib and rng.random() < lib.get("p", 0):
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
                lanes[lane] = assemble(lambda: bar, rng)
                modes[lane] = f"E({k},16)"
                continue
            if lane == "kick":
                # usually start from a curated skeleton in the DJ's bank
                # (owner 2026-07-17: a larger pattern library), sometimes
                # a groove-library seed or a freestyle from the weight
                # map — then vary either way
                bank = BOOM_BAP_KICKS if boom_bap \
                    else KICK_BANK.get(name, [])
                if lib_seed and len(lib_seed.get("kick", "")) == 16:
                    barA = _bank_vary(_thin_kick(lib_seed["kick"], rng),
                                      spec, rng)
                    notes.append("groove seed: %s (%s)"
                                 % (lib_seed["name"], lib_seed["subgenre"]
                                    or lib_seed["genre"]))
                elif bank and rng.random() < 0.75:
                    barA = _bank_vary(rng.choice(bank), spec, rng)
                else:
                    barA = gen_kick(spec, rng)
                lanes[lane] = assemble(lambda: barA, rng)
                continue
            if "modes" in spec and "gcells" in spec:      # backbeat lane
                # the backbeat is identity: its mode holds for the whole
                # beat, B answers with fresh ghosts, motion lives only in
                # the phrase-tail fills — never a stray mid-bar hit
                barA, mode = gen_backbeat(spec, rng)
                barB, _ = gen_backbeat(dict(spec, modes=[[mode, 1]]), rng)
                lanes[lane] = [barA, barA, barA, _fill(barA, rng),
                               barB, barB, barB, _fill(barB, rng)]
                modes[lane] = mode
                continue
            if lane == "hat" and not boom_bap and lib_seed \
                    and lib_seed.get("hat"):
                bar = lib_seed["hat"]
                mode = "seed:" + (lib_seed["subgenre"]
                                  or lib_seed["genre"])
            else:
                bar, mode = gen_timekeeper(spec, rng)
            if mode == "answer":             # call-and-response bar pairs
                lanes[lane] = ["-" * 16, bar] * 4
            else:
                lanes[lane] = [bar] * 7 + [_fill(bar, rng)]
            modes[lane] = mode

        # kick flavor: not solely 808s (owner verdict 2026-07-17). The
        # streak-breaker guarantees it: after the same flavor twice in a
        # row, the dice exclude it — no run of long-sustain 808s can
        # happen no matter the luck (owner report later that day).
        flavors = BOOM_BAP_FLAVORS if boom_bap else style["kick_flavors"]
        weights = [f[0] for f in flavors]
        if len(past) >= 2 and past[0][3] == past[1][3] \
                and len(flavors) > 1 and past[0][3] < len(flavors):
            weights = [0 if i == past[0][3] else w
                       for i, w in enumerate(weights)]
        fi = rng.choices(range(len(flavors)), weights=weights)[0]
        _, must, wants, secs = flavors[fi]

        fp = (lanes["kick"][0], modes.get("snare", modes.get("clap", "")),
              modes.get("hat", modes.get("snap", "")), fi)
        if not _too_close(fp, past):
            break
        # remember the roll that stays farthest from everything recent,
        # in case no attempt clears the guard outright (sparse styles
        # have fewer places to put a kick, so collisions happen)
        d = min((sum(a != b for a, b in zip(old[0], fp[0]))
                 for old in past if len(old[0]) == len(fp[0])),
                default=99)
        if d > best_d:
            best, best_d = (dict(lanes), dict(modes), fp, must, wants,
                            secs), d
    else:
        lanes, modes, fp, must, wants, secs = best

    for lane, bars in lanes.items():
        pan, gain, feel, _ = preset["lanes"][lane]
        preset["lanes"][lane] = (pan, gain, feel, bars)
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
        bar, mode = gen_timekeeper(
            dict(modes=[["offbeats", 2], ["sparse", 2], ["answer", 1]]), rng)
        side = rng.choice((-1, 1)) * rng.uniform(0.15, 0.35)
        preset["lanes"][lname] = (
            round(side, 2), round(rng.uniform(0.22, 0.36), 2),
            (0, rng.uniform(1.5, 4.0), swing if rng.random() < 0.5 else 50,
             rng.randrange(1, 99999)),
            ["-" * 16, bar] * 4 if mode == "answer"
            else [bar] * 7 + [_fill(bar, rng)])
        preset["kit"][lname] = (role, None, list(wants),
                                EXTRA_SECS.get(role, 0.8))
        preset.setdefault("_guests", []).append(lname)
        notes.append(f"guest {lname} ({mode})")

    remember_pattern(name, fp)
    return notes
