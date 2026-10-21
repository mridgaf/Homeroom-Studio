"""Song Sketch: deterministic, stem-aware arrangements at the source tempo.

Original DSP, inspired by Sonic Reference Engine's input-gated delay/reverb
recipes. No REAPER dependency, pitch shifting, source writes or random effects.
The transition return is a separate stem, so exported stems sum to the mix.
"""
from __future__ import annotations

import math
import random
import re

import numpy as np
from scipy.signal import butter, sosfilt

ROLES = ("drums", "bass", "music", "texture")
SCENES = {
    "intro": {"name": "Open the door", "levels": [0.0, 0.0, 0.78, 0.55],
              "description": "Melody and atmosphere. Leave room for the entrance."},
    "pocket": {"name": "Find the pocket", "levels": [0.86, 0.9, 0.66, 0.3],
               "description": "Drums and bass lead. The melody steps back."},
    "full": {"name": "All in", "levels": [1.0, 1.0, 1.0, 0.7],
             "description": "The whole band, with space around the details."},
    "break": {"name": "Empty the room", "levels": [0.0, 0.0, 0.65, 0.8],
              "description": "Pull the rhythm out. Let the music hang in the air."},
    "drums": {"name": "Just the rhythm", "levels": [1.0, 0.8, 0.0, 0.25],
              "description": "A drum-and-bass spotlight, ready for a vocal."},
    "outro": {"name": "Lights out", "levels": [0.45, 0.5, 0.65, 0.4],
              "description": "Ease the band away with a gradual fade."},
}
MOVES = {
    "none": "Clean change",
    "echo": "Echo exit",
    "bloom": "Space bloom",
    "breath": "Drum breath",
    # Added 2026-10-17 for the 2:30 song. All process his own stems only.
    "sweep_up": "Filter rise",
    "lp_open": "Filter open",
    "tape_stop": "Tape stop",
    "crush": "Crush then clean",
    "stutter": "Stutter",
    "dip": "Pre-drop dip",
    "reverse": "Reverse swell",
    "widen": "Wide chorus",
    "phase": "Phaser wash",
    "pump": "Pump",
    "drift": "Pan drift",
}
# Which roles each move touches. Anything not listed here is handled inline.
MOVE_ROLES = {
    "sweep_up": ROLES, "tape_stop": ROLES, "dip": ROLES,
    "lp_open": ("music", "texture"), "widen": ("music",),
    "phase": ("music", "texture"), "pump": ("music", "texture"),
    "drift": ("music", "texture"), "crush": ("drums", "music", "texture"),
    "stutter": ("drums", "music", "texture"), "reverse": ("music", "texture"),
    "echo": ("music", "texture"), "bloom": ("music", "texture"),
    "breath": ("drums", "bass"),
}
# Per-lane habits (2026-10-17): what each KIND of lane may be given when moves
# are auto-placed. Kick and bass stay centred and unchorused; hats pan; chords
# and texture take everything. Hand edits in the grid are never refused.
KINDS = ("kick", "bass", "snare", "hat", "chords", "texture")
HABITS = {
    "kick": ("dip", "stutter", "tape_stop", "breath"),
    "bass": ("lp_open", "sweep_up", "tape_stop", "dip", "breath"),
    "snare": ("echo", "bloom", "stutter", "crush", "dip", "reverse", "breath"),
    "hat": ("drift", "phase", "widen", "stutter", "crush", "echo", "sweep_up", "breath"),
    "chords": tuple(m for m in MOVES if m not in ("none", "breath")),
    "texture": ("drift", "phase", "widen", "lp_open", "bloom", "reverse", "echo",
                "pump", "crush", "sweep_up"),
}
WHOLE_MOVES = ("lp_open", "widen", "phase", "pump", "drift")
# ---- effect styles (2026-10-17; the Random button) ---------------------------------
# Each style is one producer habit from the Production Research Hub (chapters
# 01, 02, 03, 05), turned into placement rules. Random picks a style and a
# seed; every cell stays editable. colour = moves that tint a whole section,
# keyed by scene ("*" = any); hook = moves on the change INTO a hook; other =
# moves on every other change; combo = chance of a second carrying move;
# spread = how many fitting lanes get each move (one / few / many).
STYLES = {
    "bare_bones": {"name": "Bare bones", "odd": False,
        "note": "Almost nothing: a filtered intro, the beat drops out before a hook, one echo now and then. Hip-hop mistakes are nearly always too much, not too little.",
        "intro": ["lp_open"], "colour": {}, "p_colour": 0,
        "hook": ["breath", "echo"], "p_hook": 0.6, "other": ["echo"], "p_other": 0.15,
        "combo": 0, "spread": "one"},
    "throws": {"name": "Echo throws", "odd": False,
        "note": "The classic delay throw: an echo on the last beat of a phrase, one part at a time. Everything else stays dry.",
        "intro": [], "colour": {}, "p_colour": 0,
        "hook": ["echo"], "p_hook": 0.85, "other": ["echo", "bloom"], "p_other": 0.5,
        "combo": 0, "spread": "one"},
    "curtain": {"name": "Curtain lift", "odd": False,
        "note": "The filter opens into each hook and the hook opens up wide, so the chorus feels bigger without getting louder.",
        "intro": ["lp_open"], "colour": {"full": ["widen"]}, "p_colour": 0.7,
        "hook": ["sweep_up"], "p_hook": 0.9, "other": ["bloom"], "p_other": 0.3,
        "combo": 0, "spread": "few"},
    "hole": {"name": "Hole before the hook", "odd": False,
        "note": "Cut almost everything for the last beat before a hook. A moment of near-nothing makes the return hit harder than any riser.",
        "intro": [], "colour": {"full": ["widen"]}, "p_colour": 0.3,
        "hook": ["dip", "breath"], "p_hook": 1.0, "other": ["breath"], "p_other": 0.2,
        "combo": 0.5, "spread": "many"},
    "build_drop": {"name": "Build and drop", "odd": False,
        "note": "2010s build-ups: a rising filter or reverse swell into every hook, a pumping hook, a phaser on the break.",
        "intro": ["lp_open"], "colour": {"full": ["pump", "widen"], "break": ["phase"]}, "p_colour": 0.6,
        "hook": ["sweep_up", "reverse", "dip"], "p_hook": 1.0, "other": ["echo"], "p_other": 0.3,
        "combo": 0.6, "spread": "few"},
    "dub": {"name": "Dub throws", "odd": False,
        "note": "Dub habits: echo and reverb thrown on single parts, phaser and slow panning on the music, the rhythm left alone.",
        "intro": ["phase"], "colour": {"*": ["phase", "drift"]}, "p_colour": 0.5,
        "hook": ["echo", "bloom"], "p_hook": 0.8, "other": ["echo", "bloom", "reverse"], "p_other": 0.6,
        "combo": 0.3, "spread": "few", "outro": ["phase", "drift"]},
    "tape_dust": {"name": "Tape and dust", "odd": False,
        "note": "SP-303 / lo-fi habits: a light wobble on one part, a tape stop or crush into a hook. Keep it subtle: if you can point to it, it's too much.",
        "intro": ["lp_open"], "colour": {"*": ["widen", "drift"]}, "p_colour": 0.35,
        "hook": ["tape_stop", "crush"], "p_hook": 0.7, "other": ["crush", "breath"], "p_other": 0.3,
        "combo": 0, "spread": "one"},
    "gasps": {"name": "Nervous gasps", "odd": False,
        "note": "The anxiety trick (Doechii): drums vanish for a split second at the end of sections and everything but the loop drops before each hook.",
        "intro": [], "colour": {}, "p_colour": 0,
        "hook": ["dip", "breath"], "p_hook": 1.0, "other": ["breath", "stutter"], "p_other": 0.9,
        "combo": 0.5, "spread": "many"},
    "stutter": {"name": "Stutter punctuation", "odd": False,
        "note": "Trap punctuation: a one-beat stutter or tape stop right before the hook, a pumping hook, short drops in the verses.",
        "intro": [], "colour": {"full": ["pump"]}, "p_colour": 0.7,
        "hook": ["stutter", "tape_stop"], "p_hook": 0.9, "other": ["stutter", "dip"], "p_other": 0.5,
        "combo": 0, "spread": "few"},
    "slow_bloom": {"name": "Slow bloom", "odd": False,
        "note": "Dreamy: chorus and phaser washes, reverb that blooms at the ends, reverse swells felt more than heard.",
        "intro": ["lp_open"], "colour": {"*": ["widen", "phase"]}, "p_colour": 0.5,
        "hook": ["reverse", "bloom"], "p_hook": 0.8, "other": ["bloom", "echo"], "p_other": 0.5,
        "combo": 0, "spread": "few", "outro": ["phase", "drift"]},
    "seasick": {"name": "Seasick (odd)", "odd": True,
        "note": "Unusual on purpose: phaser, chorus and panning on lots of parts at once, crushes in odd spots. A wall that never sits still.",
        "intro": ["phase"], "colour": {"*": ["phase", "widen", "drift"]}, "p_colour": 0.9,
        "hook": ["crush", "reverse"], "p_hook": 0.7, "other": ["crush", "tape_stop", "reverse"], "p_other": 0.6,
        "combo": 0.4, "spread": "many", "outro": ["drift"]},
    "wrong_turns": {"name": "Wrong turns (odd)", "odd": True,
        "note": "Unusual on purpose: moves where nobody expects them, like a tape stop into a verse, a crush into the hook, a stutter in the intro.",
        "intro": ["pump"], "colour": {"*": ["pump", "drift", "phase"]}, "p_colour": 0.5,
        "hook": ["crush", "tape_stop", "stutter"], "p_hook": 0.8,
        "other": ["tape_stop", "stutter", "reverse", "crush"], "p_other": 0.8,
        "combo": 0.5, "spread": "few"},
}
# ---- genre buttons (2026-10-21) ---------------------------------------------
# Same shape as STYLES: which moves colour a section, which carry the change
# into a hook / any other change. Sources: Production Research Hub ch 02 + 05
# (boom bap dry room + SP grit, trap kick/808 duck, lo-fi tape + filter, dub
# delays). Drill and G-funk are thin in the Hub: general knowledge, unsourced.
GENRES = {
    "boom_bap": {"name": "Boom bap", "odd": False,
        "note": "Dry and dusty: a filtered intro, the beat drops out a beat before the hook, an echo on the snare now and then, a little SP grit.",
        "intro": ["lp_open"], "colour": {"pocket": ["crush"]}, "p_colour": 0.3,
        "hook": ["breath", "echo"], "p_hook": 0.9, "other": ["echo", "breath"], "p_other": 0.4,
        "combo": 0.2, "spread": "one"},
    "trap": {"name": "Trap", "odd": False,
        "note": "Pumping hooks, stutters and tape stops right before the hook, the 808 dropping out for a beat, reverse swells.",
        "intro": ["lp_open"], "colour": {"full": ["pump"]}, "p_colour": 0.8,
        "hook": ["stutter", "dip", "tape_stop", "reverse"], "p_hook": 1.0, "other": ["stutter", "dip"], "p_other": 0.6,
        "combo": 0.4, "spread": "few"},
    "lofi": {"name": "Lo-fi", "odd": False,
        "note": "Like an old tape: filtered and wobbly, crushed a little, reverb blooming at the ends, the odd tape stop.",
        "intro": ["lp_open"], "colour": {"*": ["widen", "drift", "crush"]}, "p_colour": 0.6,
        "hook": ["tape_stop", "bloom"], "p_hook": 0.7, "other": ["bloom", "crush"], "p_other": 0.4,
        "combo": 0, "spread": "few", "outro": ["lp_open", "drift"]},
    "drill": {"name": "Drill", "odd": False,
        "note": "Sliding, nervous energy: stutters and quick drop-outs, reverse swells into the hook, drums that switch up a lot. (Not from the research notes.)",
        "intro": ["sweep_up"], "colour": {"full": ["pump"]}, "p_colour": 0.4,
        "hook": ["reverse", "dip", "stutter"], "p_hook": 1.0, "other": ["stutter", "breath", "dip"], "p_other": 0.8,
        "combo": 0.5, "spread": "few"},
    "gfunk": {"name": "G-funk", "odd": False,
        "note": "Smooth and wide: phaser and chorus on the music, filters opening into the hook, few hard stops. (Not from the research notes.)",
        "intro": ["lp_open"], "colour": {"*": ["phase", "widen"]}, "p_colour": 0.7,
        "hook": ["sweep_up", "echo"], "p_hook": 0.8, "other": ["echo", "bloom"], "p_other": 0.4,
        "combo": 0, "spread": "few", "outro": ["phase"]},
    "dub": {"name": "Dub / Reggae", "odd": False,
        "note": "Echo and reverb thrown on single parts, phaser and slow panning, the rhythm dropping in and out.",
        "intro": ["phase"], "colour": {"*": ["phase", "drift"]}, "p_colour": 0.6,
        "hook": ["echo", "bloom", "dip"], "p_hook": 0.9, "other": ["echo", "bloom", "breath"], "p_other": 0.7,
        "combo": 0.4, "spread": "few", "outro": ["phase", "drift"]},
}

# ---- six arrangement types (2026-10-21) --------------------------------------
# Every song is 2:30-4:00 (owner). A type = head + body (repeated until the
# song is long enough) + tail. Each row: scene, bars (4 or 8), half (an 8-bar
# loop plays only its "front" or "back" 4 bars; None = straight through),
# colour moves, carrying moves, drum mode (see DRUM_MODES).
SONG_MIN, SONG_MAX = 150, 240
PARTS = {"intro": "Intro", "pocket": "Verse", "full": "Hook", "break": "Break",
         "drums": "Drum break", "outro": "Outro"}
DRUM_MODES = {"all": "Every drum", "thin": "One drum part out",
              "core": "Kick + snare only", "kick": "Kick only", "hats": "No kick"}
TYPES = {
    "radio": {"name": "Radio song", "target": 180,
        "note": "Intro, two verse/hook rounds, a break, the last hook, outro. About 3 minutes.",
        "head": [("intro", 4, "front", ["lp_open"], ["sweep_up"], "core")],
        "body": [("pocket", 8, None, [], ["echo"], "thin"),
                 ("pocket", 8, None, [], ["breath", "dip"], "all"),
                 ("full", 8, None, ["widen"], ["echo"], "all"),
                 ("full", 8, "back", ["pump"], ["sweep_up", "dip"], "all")],
        "tail": [("break", 8, None, ["phase"], ["reverse"], "all"),
                 ("full", 8, None, ["widen"], ["tape_stop", "echo"], "all"),
                 ("outro", 4, "front", [], [], "core")]},
    "verse_heavy": {"name": "Long verses", "target": 210,
        "note": "Long verses for rapping, short punchy hooks cut from the loop's front and back halves. About 3:30.",
        "head": [("intro", 8, None, ["lp_open"], ["bloom"], "core")],
        "body": [("pocket", 8, None, [], ["echo"], "all"),
                 ("pocket", 8, "front", [], ["breath"], "thin"),
                 ("pocket", 8, None, [], ["echo"], "thin"),
                 ("full", 4, "front", ["widen"], ["stutter"], "all"),
                 ("full", 4, "back", ["pump"], ["dip"], "all")],
        "tail": [("outro", 8, None, ["drift"], [], "core")]},
    "slow_build": {"name": "Slow build", "target": 180,
        "note": "Starts nearly empty and adds a layer at a time: kick only, then kick and snare, then everything. About 3 minutes.",
        "head": [("break", 8, "front", ["lp_open"], ["bloom"], "all"),
                 ("pocket", 8, "front", [], ["sweep_up"], "kick"),
                 ("pocket", 8, None, [], ["reverse"], "core")],
        "body": [("full", 8, None, ["widen"], ["echo"], "thin"),
                 ("full", 8, None, ["pump"], ["bloom", "sweep_up"], "all")],
        "tail": [("break", 8, None, ["phase"], ["reverse"], "hats"),
                 ("full", 8, None, ["widen"], ["tape_stop"], "all"),
                 ("outro", 8, None, ["drift"], [], "core")]},
    "chop_shop": {"name": "Chop shop", "target": 165,
        "note": "Short 4-bar pieces that flip between the loop's front and back halves, drum spotlights, lots of quick changes. About 2:45.",
        "head": [("drums", 4, "front", [], ["stutter"], "core")],
        "body": [("full", 4, "front", [], ["dip"], "all"),
                 ("pocket", 4, "back", [], ["stutter", "breath"], "thin"),
                 ("drums", 4, "front", [], ["crush"], "hats"),
                 ("full", 4, "back", ["pump"], ["tape_stop", "reverse"], "all")],
        "tail": [("break", 4, "front", ["phase"], ["reverse"], "all"),
                 ("full", 4, "back", [], ["stutter"], "all"),
                 ("outro", 4, "front", [], [], "kick")]},
    "two_drops": {"name": "Break and return", "target": 195,
        "note": "Two big drops: everything stops, the music hangs, then the beat comes back harder. About 3:15.",
        "head": [("intro", 8, None, ["lp_open"], ["sweep_up"], "all"),
                 ("full", 8, None, [], ["echo"], "all")],
        "body": [("pocket", 8, None, [], ["breath"], "thin"),
                 ("break", 4, "back", ["phase"], ["reverse", "dip"], "all"),
                 ("drums", 4, "front", [], ["tape_stop", "sweep_up"], "core"),
                 ("full", 8, None, ["widen"], ["echo"], "all")],
        "tail": [("outro", 8, None, ["drift"], [], "core")]},
    "mixtape": {"name": "Mixtape ride", "target": 150,
        "note": "The beat just rides, like a DJ playing it: drum parts drop in and out every section so it never sits still. About 2:30.",
        "head": [("pocket", 8, None, ["lp_open"], ["echo"], "core")],
        "body": [("full", 8, None, [], ["echo"], "thin"),
                 ("pocket", 8, "front", [], ["breath"], "hats"),
                 ("full", 8, None, [], ["dip"], "all"),
                 ("pocket", 8, "back", [], ["echo"], "thin")],
        "tail": [("outro", 8, None, [], [], "kick")]},
}


def type_form(key, bpm):
    """The type's sections for this tempo, always 2:30-4:00 (cap 40 sections).
    Body rows are added one at a time until the song reaches the type's
    target; at very slow tempos 8-bar rows are halved until it fits."""
    t, bar = TYPES[key], 240 / (bpm or 90)
    rows = lambda body: [list(r) for r in t["head"] + body + t["tail"]]
    secs = lambda f: sum(r[1] for r in f) * bar
    body, i = [], 0
    while (secs(rows(body)) < t["target"] or secs(rows(body)) < SONG_MIN) \
            and len(rows(body)) < 40:
        nxt = body + [t["body"][i % len(t["body"])]]
        if secs(rows(nxt)) > SONG_MAX:
            break
        body, i = nxt, i + 1
    form = rows(body)
    for r in reversed(form):                 # very slow beats: shorten
        if secs(form) <= SONG_MAX:
            break
        if r[1] == 8:
            r[1] = 4
    return [{"scene": sc, "part": PARTS[sc], "bars": b, "half": h,
             "colour": c, "carry": e, "drums": dm}
            for sc, b, h, c, e, dm in form]


def _pick_moves(form, rng, st=None):
    """Moves per section: the type's own pools, or a genre/style's pools
    laid over the type's scenes. One colour move at most, carrying moves
    never repeat back to back, the last section carries nothing."""
    prev_c = prev_e = None
    out = []
    for i, sec in enumerate(form):
        sc, last = sec["scene"], i + 1 == len(form)
        if st is None:
            cpool, cp = sec["colour"], 0.75
        elif i == 0:
            cpool, cp = st["intro"], 0.8
        elif sc == "outro":
            cpool, cp = st.get("outro", []), 0.6
        else:
            cpool, cp = st["colour"].get(sc, st["colour"].get("*", [])), st["p_colour"]
        cpool = [m for m in cpool if m != prev_c]
        prev_c = rng.choice(cpool) if cpool and rng.random() < cp else None
        moves = [prev_c] if prev_c else []
        if not last:
            if st is None:
                epool, ep, combo = sec["carry"], 0.85, 0.2
            else:
                hook = form[i + 1]["scene"] == "full"
                epool = st["hook" if hook else "other"]
                ep, combo = st["p_hook" if hook else "p_other"], st["combo"]
            epool = [m for m in epool if m != prev_e]
            if epool and rng.random() < ep:
                prev_e = rng.choice(epool)
                moves.append(prev_e)
                rest = [m for m in epool if m != prev_e]
                if rest and rng.random() < combo:
                    moves.append(rng.choice(rest))
            else:
                prev_e = None
        out.append(moves)
    return out


def drum_mutes(form, stems):
    """Drum variations: which drum lanes sit out each section. Kick and snare
    lanes are the core; every other drum lane is an extra. "thin" drops one
    extra, a different one each time, so repeated verses differ."""
    drums = [s for s in stems if s["role"] == "drums"]
    kick = [s["lane"] for s in drums if s["kind"] == "kick"]
    snare = [s["lane"] for s in drums if s["kind"] == "snare"]
    extra = [s["lane"] for s in drums if s["lane"] not in kick + snare]
    turn = 0
    out = []
    for sec in form:
        mode = sec["drums"]
        if mode == "thin" and extra:
            mute = [extra[turn % len(extra)]]
            turn += 1
        elif mode == "core":
            mute = extra
        elif mode == "kick" and kick:
            mute = snare + extra
        elif mode == "hats" and extra:
            mute = kick
        else:
            mute = []
        out.append(list(mute))
    return out


def type_plan(seed, key, bpm, stems, fx=None):
    """One full plan: the type's sections, their moves (built in, or from a
    GENRES / STYLES key), spread over the beat's lanes, plus drum mutes.
    Same inputs, same plan."""
    form = type_form(key, bpm)
    st = GENRES.get(fx) or STYLES.get(fx)
    rng = random.Random(f"{key}:{fx}:{seed}")
    base = [dict(s, moves=m, mute=mu) for s, m, mu in
            zip(form, _pick_moves(form, rng, st), drum_mutes(form, stems))]
    plan = assign_lanes(base, stems, rng, st["spread"] if st else "few")
    keep = ("scene", "part", "bars", "half", "drums", "moves", "lanes", "mute")
    return [{k: s[k] for k in keep} for s in plan]


def guess_role(label):
    """Only a starting suggestion; the page exposes every assignment."""
    words = re.split(r"[^a-z0-9]+", label.lower())
    if any(re.match(r"^(bass|sub|808)", w) for w in words):
        return "bass"
    if any(re.match(r"^(kick|snare|snap|clap|hat|hihat|drum|perc|shaker|rim|tom|cymbal|mathperc)", w)
           for w in words):
        return "drums"
    if any(re.match(r"^(fx|air|noise|riser|texture|atmo|woods|clicks)", w) for w in words):
        return "texture"
    return "music"


def guess_kind(label):
    """Finer than role: which habits a lane gets. Only a starting guess."""
    words = re.split(r"[^a-z0-9]+", label.lower())
    has = lambda pat: any(re.match(pat, w) for w in words)
    if has(r"^(bass|sub|808|boom)"):
        return "bass"
    if has(r"^(kick|bd)"):
        return "kick"
    if has(r"^(snare|snap|clap|rim)"):
        return "snare"
    if has(r"^(hat|hihat|shaker|cymbal|perc|tom|drum|mathperc)"):
        return "hat"
    if has(r"^(fx|air|noise|riser|texture|atmo|woods|clicks|vinyl|dust)"):
        return "texture"
    return "chords"


def assign_lanes(base, stems, rng, spread="few"):
    """Give each section move to the lanes that are audible in that scene,
    whose kind allows it, and who have had the fewest turns so far. spread:
    one lane, a few (about a quarter for colour moves), or many (half)."""
    used = {s["lane"]: 0 for s in stems}
    n_pick = max(1, math.ceil(len(stems) / 4))
    plan = []
    for sec in base:
        levels = SCENES[sec["scene"]]["levels"]
        live = [s for s in stems if levels[ROLES.index(s["role"])] > 0
                and s["lane"] not in sec.get("mute", ())]
        lanes = {}
        for m in sec["moves"]:
            ok = [s for s in live if m in HABITS.get(s["kind"], ())]
            if spread == "one":
                count = 1
            elif spread == "many":
                count = max(1, math.ceil(len(ok) / 2))
            else:
                count = n_pick if m in WHOLE_MOVES else (2 if len(ok) > 1 and rng.random() < 0.4 else 1)
            ok.sort(key=lambda s: (used[s["lane"]], rng.random()))
            for s in ok[:count]:
                lanes.setdefault(s["lane"], []).append(m)
                used[s["lane"]] += 1
        union = [m for m in sec["moves"] if any(m in v for v in lanes.values())]
        plan.append(dict(sec, moves=union, lanes=lanes))
    return plan


def _number(value, low, high, label):
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a number")
    try:
        n = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a number") from None
    if not math.isfinite(n) or not low <= n <= high:
        raise ValueError(f"{label} must be between {low} and {high}")
    return n


def validate_recipe(body, lane_ids, default_bpm=None):
    if not isinstance(body, dict):
        raise ValueError("recipe must be an object")
    bpm = _number(body.get("bpm", default_bpm), 40, 240, "Tempo")
    bars = _number(body.get("section_bars", 4), 1, 8, "Bars per section")
    if int(bars) != bars:
        raise ValueError("Bars per section must be a whole number")
    sections = body.get("sections")
    if not isinstance(sections, list) or not 1 <= len(sections) <= 40:
        raise ValueError("Choose between one and forty sections")
    clean = []
    for s in sections:
        if not isinstance(s, dict) or not isinstance(s.get("scene"), str) or s["scene"] not in SCENES:
            raise ValueError("Unknown section or transition")
        # 2026-10-21: each section may set its own length, play only the
        # front or back half of an 8-bar loop, and sit some lanes out
        sb = _number(s.get("bars", bars), 1, 8, "Bars per section")
        half = s.get("half")
        mute = s.get("mute", [])
        if (int(sb) != sb or half not in (None, "front", "back")
                or not isinstance(mute, list) or any(m not in lane_ids for m in mute)):
            raise ValueError("Unknown section length, half or muted stem")
        shape = {"bars": int(sb), "half": half, "mute": sorted(set(mute))}
        lanes_in = s.get("lanes")
        if lanes_in is not None:             # per-lane moves (the grid)
            if (not isinstance(lanes_in, dict)
                    or any(k not in lane_ids or not isinstance(v, list) or len(v) > 4
                           or any(not isinstance(m, str) or m not in MOVES for m in v)
                           for k, v in lanes_in.items())):
                raise ValueError("Unknown stem or move")
            lanes_c = {}
            for k, v in lanes_in.items():
                v = [m for i, m in enumerate(v) if m != "none" and m not in v[:i]]
                if v:
                    lanes_c[k] = v
            union = [m for m in MOVES if any(m in v for v in lanes_c.values())]
            clean.append({"scene": s["scene"], "moves": union,
                          "move": union[0] if union else "none", "lanes": lanes_c, **shape})
            continue
        # "moves" is the list; a lone "move" string still works (old recipes).
        moves = s.get("moves", [s.get("move", "none")])
        if (not isinstance(moves, list) or len(moves) > 4
                or any(not isinstance(m, str) or m not in MOVES for m in moves)):
            raise ValueError("Unknown section or transition")
        moves = [m for i, m in enumerate(moves) if m != "none" and m not in moves[:i]]
        clean.append({"scene": s["scene"], "moves": moves,
                      "move": moves[0] if moves else "none", **shape})
    roles = body.get("roles", {})
    if not isinstance(roles, dict) or any(k not in lane_ids or not isinstance(v, str) or v not in ROLES for k, v in roles.items()):
        raise ValueError("Unknown stem or role")
    roles = {k: roles.get(k, guess_role(k)) for k in lane_ids}
    amount = _number(body.get("amount", 0.6), 0, 1, "Transition amount")
    if sum(c["bars"] for c in clean) * 240 / bpm > SONG_MAX:
        raise ValueError("Sketch is too long; use fewer bars or a faster tempo (maximum 4:00)")
    return {"version": 1, "bpm": bpm, "section_bars": int(bars),
            "sections": clean, "roles": roles, "amount": amount}


def _fade_edges(x, sr, seconds=0.005):
    n = min(round(sr * seconds), len(x) // 2)
    if n:
        ramp = np.linspace(0, 1, n, dtype=np.float32)
        x[:n] *= ramp[:, None]
        x[-n:] *= ramp[::-1, None]
    return x


def _tone(x, sr):
    # Tone shaping lives inside the repeat path: every repeat gets darker.
    sos = butter(2, [min(180, sr * 0.02), min(4800, sr * 0.42)],
                 btype="bandpass", fs=sr, output="sos")
    return sosfilt(sos, x, axis=0).astype(np.float32)


def echo_return(feed, sr, bpm, amount):
    """Wet only, causal dotted-eighth repeats; zero input gives zero output.

    Gate the feed, never the return. Delays spill into the next section,
    and alternate L/R. No circular wrap from the end into the intro.
    """
    out = np.zeros_like(feed)
    repeat = feed
    step = max(1, round(sr * 60 / bpm * 0.75))
    for i in range(1, 9):
        shift = step * i
        if shift >= len(feed):
            break
        repeat = _tone(repeat, sr)[:, ::-1]
        out[shift:] += repeat[:-shift] * (amount * 0.65 * 0.48 ** (i - 1))
    return out


def bloom_return(feed, sr, amount):
    """Wet-only forward reverb; the caller supplies the growing input feed."""
    if not np.any(feed) or amount == 0:
        return np.zeros_like(feed)
    import pedalboard as pb
    toned = _tone(feed, sr)
    wet = pb.Reverb(room_size=0.72, damping=0.65, wet_level=1.0,
                    dry_level=0.0, width=0.9)(toned.T.copy(), sr).T
    return wet.astype(np.float32) * (amount * 0.6)


def _sweep(x, sr, lo, hi, kind):
    """Cutoff glides lo -> hi Hz (exponential) over x; filter state carried
    across ~12 ms steps so there are no clicks."""
    out = np.empty_like(x)
    n, step = len(x), max(1, round(sr * 0.012))
    zi = None
    for s in range(0, n, step):
        e = min(n, s + step)
        f = min(lo * (hi / lo) ** (((s + e) / 2) / n), sr * 0.45)
        sos = butter(2, f, btype=kind, fs=sr, output="sos")
        if zi is None:
            zi = np.zeros((sos.shape[0], 2, x.shape[1]))
        out[s:e], zi = sosfilt(sos, x[s:e], axis=0, zi=zi)
    return out


def _whole_fx(block, moves, sr, beat, start, amount, salt=0):
    """Moves that colour the whole section, for ONE lane. salt (the lane's
    number) gives each lane its own rate, phase and direction."""
    ok = list(moves)
    if "lp_open" in ok:
        w = min(len(block), round(8 * beat * sr))
        block[:w] = _sweep(block[:w], sr, 500, 16000, "lowpass")
    if "widen" in ok or "phase" in ok:
        import pedalboard as pb
        fx = []
        if "widen" in ok:
            fx.append(pb.Chorus(rate_hz=0.5 * (1 + 0.17 * (salt % 5)), depth=0.4, centre_delay_ms=8.0,
                                feedback=0.0, mix=0.25 + 0.3 * amount))
        if "phase" in ok:
            fx.append(pb.Phaser(rate_hz=0.25 * (1 + 0.13 * (salt % 5)), depth=0.7, centre_frequency_hz=900.0,
                                feedback=0.3, mix=0.3 + 0.2 * amount))
        block[:] = pb.Pedalboard(fx)(block.T.copy(), sr).T
    t = (np.arange(len(block)) + start)
    if "pump" in ok:    # gain dips on every beat and swells back
        phase = (t / (beat * sr)) % 1.0
        block *= (1 - (0.3 + 0.3 * amount) * (1 - phase) ** 3).astype(np.float32)[:, None]
    if "drift" in ok:   # slow pan, 16 beats per lap
        lap = (16 + 4 * (salt % 4)) * beat * sr
        p = 0.7 * (-1 if salt % 2 else 1) * np.sin(2 * np.pi * t / lap + 0.9 * salt)
        th = (p + 1) * np.pi / 4
        block *= (np.sqrt(2) * np.column_stack((np.cos(th), np.sin(th)))).astype(np.float32)
    return block


def _end_fx(block, moves, sr, beat, amount):
    """Moves that carry the section into the next one, for ONE lane."""
    ok = list(moves)
    bs = round(beat * sr)
    if "sweep_up" in ok:
        w = min(len(block), 8 * bs)
        block[-w:] = _sweep(block[-w:], sr, 40, 2500, "highpass")
    if "crush" in ok:
        w = min(len(block), 4 * bs)
        seg = block[-w:]
        hard = np.repeat(np.round(seg[::6] * 32) / 32, 6, axis=0)[:w]
        wet = np.linspace(0, 1, w, dtype=np.float32)[:, None]
        block[-w:] = seg * (1 - wet) + hard * wet
    if "stutter" in ok:
        w = min(len(block), bs)
        cell = max(1, w // 8)
        piece = block[-w:][:cell].copy()
        _fade_edges(piece, sr)
        block[-w:] = np.tile(piece, (math.ceil(w / cell), 1))[:w]
    if "dip" in ok:
        w = min(len(block), bs)
        block[-w:] *= 0.3
        _fade_edges(block[-w:], sr)
    if "tape_stop" in ok:
        w = min(len(block), bs)
        seg = block[-w:].copy()
        pos = np.minimum(np.cumsum(np.linspace(1.0, 0.04, w)), w - 1)
        idx = np.arange(w)
        slowed = np.column_stack([np.interp(pos, idx, seg[:, c]) for c in range(seg.shape[1])])
        block[-w:] = slowed.astype(np.float32) * np.linspace(1, 0, w, dtype=np.float32)[:, None] ** 0.7
    if "breath" in moves:
        rest = min(len(block), round(beat * 0.5 * sr))
        fade = min(round(0.005 * sr), len(block) - rest)
        if fade:
            block[-rest-fade:-rest] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]
        block[-rest:] = 0
    return block


def reverse_swell(piece, sr, amount):
    """Wet-only reversed reverb of the next section's first hit; its loudest
    point lands on the downbeat. Returns audio that ENDS at the boundary."""
    import pedalboard as pb
    padded = np.vstack((piece, np.zeros((round(2.0 * sr), 2), dtype=np.float32)))
    wet = pb.Reverb(room_size=0.8, damping=0.5, wet_level=1.0, dry_level=0.0,
                    width=1.0)(padded.T.copy(), sr).T
    rev = np.ascontiguousarray(wet[::-1]).astype(np.float32) * (amount * 0.7)
    return _fade_edges(rev, sr)


def render(channels, recipe):
    """Return (stems, mix, repeated_original, metadata), all float32 stereo.

    Inputs are original dry channel arrays. Source loops keep their native
    period, pitch and rate. Different sample rates are resampled, not stretched.
    Section boundaries follow the requested BPM; UI flags non-bar-length loops.
    """
    if not channels or len(channels) > 24:
        raise ValueError("Use between 1 and 24 stems")
    sr = int(next(iter(channels.values()))["sr"])
    if not 8000 <= sr <= 96000:
        raise ValueError("Use audio between 8 and 96 kHz")
    recipe = validate_recipe(recipe, channels, recipe.get("bpm"))
    bpm = recipe["bpm"]
    beat = 60 / bpm
    # Round absolute boundaries, not a repeatedly rounded bar: no tempo drift.
    secs = recipe["sections"]
    at = np.cumsum([0] + [s["bars"] for s in secs])
    bounds = [round(b * 4 * beat * sr) for b in at]
    tail_seconds = 4.0 if recipe["amount"] and any(
        m in ("echo", "bloom") for s in secs for m in s["moves"]) else 0.0
    n = bounds[-1] + round(tail_seconds * sr)
    if n * 2 * 4 * (len(channels) + 9) > 3_200_000_000:   # 4:00 x ~24 stems
        raise ValueError("This sketch is too large; use fewer bars or fewer stems")
    stems = {}
    original = np.zeros((n, 2), dtype=np.float32)
    echo_feed = np.zeros_like(original)
    bloom_feed = np.zeros_like(original)
    reverse_ret = np.zeros_like(original)
    warnings = []
    source_info = []
    for li, (lane, ch) in enumerate(channels.items()):
        L, R = ch["dry"]
        if len(L) != len(R) or not len(L) or not np.isfinite(L).all() or not np.isfinite(R).all():
            raise ValueError(f"{lane}: source is empty or contains invalid audio")
        src = np.column_stack((L, R)).astype(np.float32)
        if not np.isfinite(src).all():
            raise ValueError(f"{lane}: source exceeds the supported audio range")
        source_rate = ch["sr"]
        if source_rate != sr:
            import soxr
            src = soxr.resample(src, source_rate, sr).astype(np.float32)
        source_bars = len(src) / sr / (4 * beat)
        source_info.append({"lane": lane, "role": recipe["roles"][lane],
                            "samples": len(L), "sample_rate": source_rate,
                            "bars_at_tempo": round(source_bars, 4)})
        if abs(source_bars - round(source_bars)) > 0.03:
            warnings.append(f"{lane}: length is {source_bars:.2f} bars at {bpm:g} BPM; native loop timing retained.")
        # Smooth only the existing loop seam (5 ms); never change its period.
        _fade_edges(src, sr)
        repeated = np.tile(src, (math.ceil(bounds[-1] / len(src)), 1))[:bounds[-1]]
        original[:bounds[-1]] += repeated
        out = np.zeros_like(original)
        role = recipe["roles"][lane]
        for i, section in enumerate(secs):
            start, end = bounds[i:i + 2]
            if "lanes" in section:      # per-lane grid: only the named lanes move
                moves = section["lanes"].get(lane, [])
            else:                       # section-level moves: every lane of a fitting role
                moves = [m for m in section["moves"] if role in MOVE_ROLES.get(m, ROLES)]
            gain = SCENES[section["scene"]]["levels"][ROLES.index(role)]
            if lane in section["mute"]:
                gain = 0.0
            if section["half"] and source_bars >= 7.97:
                # front/back 4 of an 8-bar loop, looped from the section start
                h = len(src) // 2
                piece = (src[:h] if section["half"] == "front" else src[h:]).copy()
                _fade_edges(piece, sr)       # the cut point gets the same 5 ms seam
                block = np.tile(piece, (math.ceil((end - start) / h), 1))[:end - start] * gain
            else:
                block = repeated[start:end].copy() * gain
            _fade_edges(block, sr)
            if section["scene"] == "outro":
                block *= np.linspace(1, 0, len(block), dtype=np.float32)[:, None]
            block = _whole_fx(block, moves, sr, beat, start, recipe["amount"], li)
            # Select just the phrase END before the wet effect. Bass never feeds it.
            if moves:
                if "echo" in moves:
                    width = min(len(block), round(beat * sr))
                    feed = block[-width:].copy()
                    _fade_edges(feed, sr)
                    echo_feed[end-width:end] += feed
                if "bloom" in moves:
                    width = min(len(block), round(4 * beat * sr))
                    feed = block[-width:].copy()
                    feed *= np.linspace(0, 1, width, dtype=np.float32)[:, None] ** 2
                    _fade_edges(feed, sr)
                    bloom_feed[end-width:end] += feed
                if "reverse" in moves and i + 1 < len(secs):
                    w = min(round(2 * beat * sr), bounds[-1] - end)
                    nxt = repeated[end:end + w] * SCENES[secs[i + 1]["scene"]]["levels"][ROLES.index(role)]
                    if lane in secs[i + 1]["mute"]:
                        nxt = nxt * 0
                    if w and np.any(nxt) and recipe["amount"]:
                        rev = reverse_swell(nxt, sr, recipe["amount"])
                        s0 = max(0, end - len(rev))
                        reverse_ret[s0:end] += rev[len(rev) - (end - s0):]
            block = _end_fx(block, moves, sr, beat, recipe["amount"])
            _fade_edges(block, sr)
            out[start:end] = block
        stems[lane] = out
    transitions = echo_return(echo_feed, sr, bpm, recipe["amount"])
    transitions += bloom_return(bloom_feed, sr, recipe["amount"])
    transitions += reverse_ret
    # Explicit finite ending: preserve decay, then fade the last 80 ms.
    ending = min(len(transitions), round(0.08 * sr))
    transitions[-ending:] *= np.linspace(1, 0, ending, dtype=np.float32)[:, None]
    transition_key = "Sketch transitions"
    while transition_key in stems:
        transition_key += "_"
    stems[transition_key] = transitions
    mix = np.sum(list(stems.values()), axis=0, dtype=np.float32)
    if not np.isfinite(mix).all() or not np.isfinite(original).all():
        raise ValueError("Source levels exceed the supported audio range")
    # One fixed attenuation across BOTH previews and ALL stems. No loudness
    # boost, hidden master compression, or per-stem normalizing that breaks sums.
    peak = max(float(np.max(np.abs(mix))), float(np.max(np.abs(original))), 1e-12)
    gain = min(1.0, 10 ** (-1 / 20) / peak)
    for x in stems.values():
        x *= gain
    mix *= gain
    original *= gain
    metadata = {"sample_rate": sr, "frames": n, "duration_s": n / sr,
                "music_duration_s": bounds[-1] / sr, "tail_s": tail_seconds,
                "gain_db": round(20 * math.log10(gain), 3),
                "peak_dbfs": round(20 * math.log10(max(float(np.max(np.abs(mix))), 1e-12)), 3),
                "sections": [{"start_s": bounds[i] / sr, "end_s": bounds[i+1] / sr,
                              **s} for i, s in enumerate(secs)],
                "sources": source_info, "warnings": warnings,
                "basis": "Original stems; Science rack settings are not used.",
                "level_rule": "Both previews and every stem share one peak-safe attenuation; not loudness normalized."}
    return stems, mix, original, metadata
