"""Song Sketch: deterministic, stem-aware arrangements at the source tempo.

Original DSP, inspired by Sonic Reference Engine's input-gated delay/reverb
recipes. No REAPER dependency, pitch shifting, source writes or random effects.
The transition return is a separate stem, so exported stems sum to the mix.
"""
from __future__ import annotations

import math
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
}
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
    if not isinstance(sections, list) or len(sections) != 4:
        raise ValueError("Choose exactly four sections")
    clean = []
    for s in sections:
        if (not isinstance(s, dict) or not isinstance(s.get("scene"), str)
                or not isinstance(s.get("move"), str)
                or s["scene"] not in SCENES or s["move"] not in MOVES):
            raise ValueError("Unknown section or transition")
        clean.append({"scene": s["scene"], "move": s["move"]})
    roles = body.get("roles", {})
    if not isinstance(roles, dict) or any(k not in lane_ids or not isinstance(v, str) or v not in ROLES for k, v in roles.items()):
        raise ValueError("Unknown stem or role")
    roles = {k: roles.get(k, guess_role(k)) for k in lane_ids}
    amount = _number(body.get("amount", 0.6), 0, 1, "Transition amount")
    if 4 * bars * 240 / bpm > 180:
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
    bounds = [round(i * section_seconds * sr) for i in range(5)]
    tail_seconds = 4.0 if recipe["amount"] and any(s["move"] in ("echo", "bloom") for s in recipe["sections"]) else 0.0
    n = bounds[-1] + round(tail_seconds * sr)
    if n * 2 * 4 * (len(channels) + 8) > 600_000_000:
        raise ValueError("This sketch is too large; use fewer bars or fewer stems")
    stems = {}
    original = np.zeros((n, 2), dtype=np.float32)
    echo_feed = np.zeros_like(original)
    bloom_feed = np.zeros_like(original)
    warnings = []
    source_info = []
    for lane, ch in channels.items():
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
        for i, section in enumerate(recipe["sections"]):
            start, end = bounds[i:i + 2]
            gain = SCENES[section["scene"]]["levels"][ROLES.index(role)]
            block = repeated[start:end].copy() * gain
            _fade_edges(block, sr)
            if section["scene"] == "outro":
                block *= np.linspace(1, 0, len(block), dtype=np.float32)[:, None]
            # A half-beat rhythmic rest before the next section, with 5ms edges.
            if section["move"] == "breath" and role in ("drums", "bass"):
                rest = min(len(block), round(beat * 0.5 * sr))
                fade = min(round(0.005 * sr), len(block) - rest)
                if fade:
                    block[-rest-fade:-rest] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]
                block[-rest:] = 0
            out[start:end] = block
            # Select just the phrase END before the wet effect. Bass never feeds it.
            if role in ("music", "texture"):
                if section["move"] == "echo":
                    width = min(len(block), round(beat * sr))
                    feed = block[-width:].copy()
                    _fade_edges(feed, sr)
                    echo_feed[end-width:end] += feed
                elif section["move"] == "bloom":
                    width = min(len(block), round(4 * beat * sr))
                    feed = block[-width:].copy()
                    feed *= np.linspace(0, 1, width, dtype=np.float32)[:, None] ** 2
                    _fade_edges(feed, sr)
                    bloom_feed[end-width:end] += feed
        stems[lane] = out
    transitions = echo_return(echo_feed, sr, bpm, recipe["amount"])
    transitions += bloom_return(bloom_feed, sr, recipe["amount"])
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
                              **s} for i, s in enumerate(recipe["sections"])],
                "sources": source_info, "warnings": warnings,
                "basis": "Original stems; Science rack settings are not used.",
                "level_rule": "Both previews and every stem share one peak-safe attenuation; not loudness normalized."}
    return stems, mix, original, metadata
