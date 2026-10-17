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
    "kick": ("dip", "stutter", "tape_stop"),
    "bass": ("lp_open", "sweep_up", "tape_stop", "dip"),
    "snare": ("echo", "bloom", "stutter", "crush", "dip", "reverse"),
    "hat": ("drift", "phase", "widen", "stutter", "crush", "echo", "sweep_up"),
    "chords": tuple(m for m in MOVES if m not in ("none", "breath")),
    "texture": ("drift", "phase", "widen", "lp_open", "bloom", "reverse", "echo",
                "pump", "crush", "sweep_up"),
}
WHOLE_MOVES = ("lp_open", "widen", "phase", "pump", "drift")
# Each type is a list of rows: scene, moves that colour the whole section (one
# at most), moves that carry it into the next section. 7 x 8 bars is about
# 150 s at 90 BPM; the other types differ in length, rhythm of scenes and which
# moves they lean on.
TEMPLATES = {
    "song_150": [
        ("intro", ["lp_open"], ["bloom", "reverse", "echo"]),
        ("pocket", ["pump", "drift"], ["sweep_up", "stutter", "dip"]),
        ("full", ["widen", "phase", "pump"], ["echo", "tape_stop", "bloom"]),
        ("break", ["phase", "drift", "widen"], ["reverse", "sweep_up", "crush"]),
        ("full", ["pump", "widen", "phase"], ["echo", "stutter", "dip"]),
        ("pocket", ["drift", "widen"], ["bloom", "tape_stop", "echo"]),
        ("outro", ["phase", "drift"], []),
    ],
    "slow_burn": [
        ("intro", ["lp_open"], ["bloom", "reverse"]),
        ("pocket", ["drift", "pump"], ["bloom", "echo"]),
        ("pocket", ["widen", "phase"], ["sweep_up", "reverse"]),
        ("full", ["widen", "pump"], ["echo", "bloom"]),
        ("full", ["phase", "drift"], ["tape_stop", "bloom"]),
        ("outro", ["drift", "phase"], []),
    ],
    "hard_hits": [
        ("full", ["pump"], ["stutter", "dip"]),
        ("drums", ["pump", "phase"], ["sweep_up", "crush"]),
        ("break", ["drift", "widen"], ["reverse", "dip"]),
        ("full", ["pump", "widen"], ["stutter", "tape_stop"]),
        ("pocket", ["pump"], ["crush", "dip"]),
        ("drums", ["phase", "pump"], ["sweep_up", "stutter"]),
        ("full", ["pump", "widen"], ["tape_stop", "crush"]),
        ("outro", ["phase"], []),
    ],
    "dub_wash": [
        ("pocket", ["phase", "drift"], ["echo", "bloom"]),
        ("drums", ["phase", "widen"], ["echo", "reverse"]),
        ("break", ["drift", "phase", "widen"], ["bloom", "echo", "reverse"]),
        ("full", ["phase", "drift"], ["echo", "tape_stop"]),
        ("outro", ["phase", "drift"], []),
    ],
    "fever_dream": [
        ("intro", ["lp_open"], ["reverse", "crush"]),
        ("full", ["pump", "widen"], ["stutter", "dip"]),
        ("break", ["phase", "drift"], ["bloom", "reverse"]),
        ("drums", ["pump", "phase"], ["sweep_up", "crush"]),
        ("pocket", ["widen", "drift"], ["tape_stop", "echo"]),
        ("full", ["phase", "pump"], ["stutter", "tape_stop"]),
        ("break", ["drift", "widen"], ["reverse", "bloom"]),
        ("pocket", ["pump", "phase"], ["crush", "sweep_up"]),
        ("full", ["widen", "drift"], ["dip", "stutter"]),
        ("drums", ["phase", "pump"], ["echo", "crush"]),
        ("pocket", ["drift", "widen"], ["bloom", "tape_stop"]),
        ("outro", ["phase", "drift"], []),
    ],
}
TEMPLATE = TEMPLATES["song_150"]


def auto_plan(seed, key="song_150"):
    """Producer-style placement: at most one colour move per section, one
    carrying move per change, and neither repeats back to back. Same seed,
    same plan."""
    rng = random.Random(seed)
    prev_whole = prev_end = None
    plan = []
    for scene, whole, end in TEMPLATES[key]:
        moves = []
        pool = [m for m in whole if m != prev_whole]
        if pool and rng.random() < 0.75:
            prev_whole = rng.choice(pool)
            moves.append(prev_whole)
        else:
            prev_whole = None
        pool = [m for m in end if m != prev_end]
        if pool:
            prev_end = rng.choice(pool)
            moves.append(prev_end)
        plan.append({"scene": scene, "moves": moves})
    return plan


def auto_plans(count=12, key="song_150"):
    return [auto_plan(s, key) for s in range(count)]
PRESETS = {
    "slow_reveal": {"name": "Slow reveal", "note": "Let the hook introduce itself. Earn the drums.",
                    "scenes": ["intro", "pocket", "break", "full"],
                    "moves": ["bloom", "echo", "breath", "echo"]},
    "hard_entrance": {"name": "Hard entrance", "note": "Start with the band. Strip it back, then hit again.",
                      "scenes": ["full", "drums", "break", "full"],
                      "moves": ["echo", "none", "bloom", "echo"]},
    "smoke_break": {"name": "Smoke break", "note": "A low-key pocket with a little space to disappear into.",
                    "scenes": ["pocket", "break", "pocket", "outro"],
                    "moves": ["echo", "bloom", "breath", "bloom"]},
    "song_150": {"name": "2:30 song", "bars": 8, "auto": True,
             "note": "Seven sections, about two and a half minutes. Effects are placed like a producer would; re-roll for a new arrangement, then edit any section.",
             "scenes": [s["scene"] for s in auto_plan(0, "song_150")],
             "moves": [s["moves"] for s in auto_plan(0, "song_150")]},
    "slow_burn": {"name": "Slow burn", "bars": 8, "auto": True,
             "note": "Six long sections that build one step at a time. Lots of space, no sudden hits.",
             "scenes": [s["scene"] for s in auto_plan(0, "slow_burn")],
             "moves": [s["moves"] for s in auto_plan(0, "slow_burn")]},
    "hard_hits": {"name": "Hard hits", "bars": 4, "auto": True,
             "note": "Eight short sections that keep changing. Drum spotlights, stutters, drops and tape stops.",
             "scenes": [s["scene"] for s in auto_plan(0, "hard_hits")],
             "moves": [s["moves"] for s in auto_plan(0, "hard_hits")]},
    "dub_wash": {"name": "Dub wash", "bars": 8, "auto": True,
             "note": "Five sections drenched in echo, reverb and phaser. The rhythm drops in and out.",
             "scenes": [s["scene"] for s in auto_plan(0, "dub_wash")],
             "moves": [s["moves"] for s in auto_plan(0, "dub_wash")]},
    "fever_dream": {"name": "Fever dream", "bars": 4, "auto": True,
             "note": "Twelve short sections that never sit still. Reverse swells, crushes and constant changes.",
             "scenes": [s["scene"] for s in auto_plan(0, "fever_dream")],
             "moves": [s["moves"] for s in auto_plan(0, "fever_dream")]},
}


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


def auto_lane_plan(seed, key, stems):
    """Spotlight placement per LANE. stems = [{lane, role, kind}]. The section
    pattern is auto_plan's; each move then goes to only the few lanes that are
    audible in that scene, whose kind allows it, and who have had the fewest
    turns so far. Same seed, same stems, same plan."""
    rng = random.Random(seed * 7919 + 1)
    base = auto_plan(seed, key)
    used = {s["lane"]: 0 for s in stems}
    n_pick = max(1, math.ceil(len(stems) / 4))
    plan = []
    for sec in base:
        levels = SCENES[sec["scene"]]["levels"]
        live = [s for s in stems if levels[ROLES.index(s["role"])] > 0]
        lanes = {}
        for m in sec["moves"]:
            ok = [s for s in live if m in HABITS.get(s["kind"], ())]
            count = n_pick if m in WHOLE_MOVES else (2 if len(ok) > 1 and rng.random() < 0.4 else 1)
            ok.sort(key=lambda s: (used[s["lane"]], rng.random()))
            for s in ok[:count]:
                lanes.setdefault(s["lane"], []).append(m)
                used[s["lane"]] += 1
        union = [m for m in sec["moves"] if any(m in v for v in lanes.values())]
        plan.append({"scene": sec["scene"], "moves": union, "lanes": lanes})
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
    if not isinstance(sections, list) or not 1 <= len(sections) <= 12:
        raise ValueError("Choose between one and twelve sections")
    clean = []
    for s in sections:
        if not isinstance(s, dict) or not isinstance(s.get("scene"), str) or s["scene"] not in SCENES:
            raise ValueError("Unknown section or transition")
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
                          "move": union[0] if union else "none", "lanes": lanes_c})
            continue
        # "moves" is the list; a lone "move" string still works (old recipes).
        moves = s.get("moves", [s.get("move", "none")])
        if (not isinstance(moves, list) or len(moves) > 4
                or any(not isinstance(m, str) or m not in MOVES for m in moves)):
            raise ValueError("Unknown section or transition")
        moves = [m for i, m in enumerate(moves) if m != "none" and m not in moves[:i]]
        clean.append({"scene": s["scene"], "moves": moves,
                      "move": moves[0] if moves else "none"})
    roles = body.get("roles", {})
    if not isinstance(roles, dict) or any(k not in lane_ids or not isinstance(v, str) or v not in ROLES for k, v in roles.items()):
        raise ValueError("Unknown stem or role")
    roles = {k: roles.get(k, guess_role(k)) for k in lane_ids}
    amount = _number(body.get("amount", 0.6), 0, 1, "Transition amount")
    if len(clean) * bars * 240 / bpm > 180:
        raise ValueError("Sketch is too long; use fewer bars or a faster tempo (maximum 3 minutes)")
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
    section_seconds = recipe["section_bars"] * 4 * beat
    # Round absolute boundaries, not a repeatedly rounded bar: no tempo drift.
    secs = recipe["sections"]
    bounds = [round(i * section_seconds * sr) for i in range(len(secs) + 1)]
    tail_seconds = 4.0 if recipe["amount"] and any(
        m in ("echo", "bloom") for s in secs for m in s["moves"]) else 0.0
    n = bounds[-1] + round(tail_seconds * sr)
    if n * 2 * 4 * (len(channels) + 9) > 2_500_000_000:
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
