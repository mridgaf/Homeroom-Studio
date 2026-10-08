"""Loops-only beats, FIVE LANES (owner spec 2026-09-16, DECISIONS.md
"Loops-only beats: FIVE LANES" — every rule below is his answer, not a
guess; read that entry before changing any number here).

  kick       the full drum loop (lane name kept as "kick": the mix bus
             anchors every level to a lane called kick)
  leadloop   guitar / synth / orchestral / melodies / keys
  bassloop   bass lines, subs
  fxloop     FX, sparse (1-2 hits per 8 bars)
  lane 5     chordloop | percloop | vocalloop | fxloop2, 25% each

Tempo = the drum loop's BPM; everything else is time-stretched to it,
pitch never moves. Always 8 bars. Half of beats match key LABELS on
lead/bass/chords (unlabeled still allowed), half ignore key.
"""
from __future__ import annotations

import json
import os
import random
import re
from functools import lru_cache
from pathlib import Path

import numpy as np

import loop_mode
import melodic_loops as ml
from key_context import mode_family
from sample_library import AUDIO_EXTS, _wav_secs, load_loop_roots, loops_scored

NBARS = 8
RISER_ODDS = 0.08                 # owner: risers "less than 10% of the time"
SAME_KEY_ODDS = 0.5
LANE5 = {"chordloop": "chords", "percloop": "perc",
         "vocalloop": "vocals", "fxloop2": "fx"}
LABELS = {"kick": "drum loop", "leadloop": "lead", "bassloop": "bass",
          "fxloop": "fx", "chordloop": "chords", "percloop": "percussion",
          "vocalloop": "vocals", "fxloop2": "fx 2"}
KEYED = ("lead", "bass", "chords")
CACHE = ml.CACHE.with_name("loop_lanes.json")

# whole words (matched on word tokens); keys words sit in lead AND chords
_KEYS = {"PIANO", "PIANOS", "ORGAN", "ORGANS", "PAD", "PADS", "KEYS", "RHODES",
         "EP", "WURLI"}
WORDS = {
    "lead": {"LEAD", "LEADS", "MELODY", "MELODIES", "MELODIC", "ARP", "ARPS",
             "TOPLINE", "PLUCK", "PLUCKS", "GUITAR", "GUITARS", "SAX", "SYNTH",
             "SYNTHS", "FLUTE", "FLUTES", "STRINGS", "STRING", "ORCHESTRAL",
             "ORCHESTRA", "HORN", "HORNS", "BRASS", "VIOLIN", "CELLO", "BELL",
             "BELLS", "INSTRUMENT", "MUSIC"} | _KEYS,
    "chords": {"CHORD", "CHORDS", "HARMONY"} | _KEYS,
    "bass": {"BASS", "BASSLINE", "808", "808S", "SUB", "SUBS"},
    "perc": {"PERC", "PERCS", "PERCUSSION", "CONGA", "CONGAS", "BONGO",
             "BONGOS", "SHAKER", "SHAKERS", "TAMBOURINE", "TAMB"},
    "vocals": {"VOCAL", "VOCALS", "VOX", "ACAPELLA", "CHANT", "CHANTS"},
    "fx": {"FX", "SFX", "RISER", "RISERS", "SWEEP", "SWEEPS", "IMPACT",
           "IMPACTS", "UPLIFTER", "DOWNLIFTER", "NOISE", "TRANSITION",
           "WHOOSH", "REVERSE"},
}
RISER = {"RISER", "RISERS", "UPLIFTER", "SWEEP", "SWEEPS"}
DRUMISH = {"DRUM", "DRUMS", "KICK", "SNARE", "HAT", "HATS", "HIHAT", "CLAP",
           "BREAK", "BREAKS", "TOP", "TOPS"}


def _words(s):                          # digits kept, so "808" is a word
    return {w for w in re.split(r"[^A-Za-z0-9]+", s.upper()) if w}


def _toks(rel):
    return set().union(*(_words(r) for r in rel))


def categories(rel):
    """Which lane pools a file (path parts under its root) belongs to."""
    w = _toks(rel)
    own = _words(rel[-1])                   # the file's own name wins
    cats = ([c for c, words in WORDS.items() if own & words]
            or [c for c, words in WORDS.items() if w & words])
    if w & DRUMISH:                                # a drum loop is not a lead
        cats = [c for c in cats if c in ("perc", "fx")]
    if "fx" in cats:                               # "Sub Riser" is FX only
        cats = ["fx"]
    if "bass" in cats and "lead" in cats:          # "Bass Synth" is bass
        cats.remove("lead")
    return cats


@lru_cache(maxsize=1)
def scan_all():
    """{category: [entry]} for every lane. Memory-cached for the server's
    life (ponytail: restart the app to see newly added loops); last good
    scan on disk when the drive is unplugged."""
    out = {c: [] for c in ("drums", *WORDS)}
    seen_any = False
    try:
        durs = json.loads(ml.DUR_CACHE.read_text())
    except (OSError, ValueError):
        durs = {}
    for root in load_loop_roots():
        rootp = Path(os.path.expanduser(root))
        if not rootp.exists():
            continue
        seen_any = True
        for path in sorted(rootp.rglob("*")):
            if path.suffix.lower() not in AUDIO_EXTS or not path.is_file():
                continue
            rel = path.relative_to(rootp).parts
            cats = categories(rel)
            if not cats:
                continue
            tokens = ml._tokens(path, rootp)
            if ml.is_full_mix(tokens):
                continue
            loopish = (rootp.name == "BOTC Sorted Loops"
                       or _toks(rel) & ml.LOOP_SIGN_WORDS
                       or ml.bpm_from_tokens(tokens))
            dkey = "%s|%d" % (path, path.stat().st_size)
            if dkey not in durs:
                durs[dkey] = _wav_secs(path)
            secs = durs[dkey] or 0
            key = ml.key_from_tokens(tokens)
            e = {"name": path.stem, "path": str(path), "secs": secs,
                 "bpm": ml.bpm_from_tokens(tokens),
                 "key": key[0] if key else None,
                 "mode": key[1] if key else None,
                 "riser": bool(_toks(rel) & RISER),
                 "folder": "/".join(rel[:-1]) or rootp.name,
                 "tokens": sorted({t.lower() for t in tokens})}
            for c in cats:
                if c == "fx" and secs >= 0.2:
                    out[c].append(e)
                elif c != "fx" and loopish and secs >= 1.5:
                    out[c].append(e)
    if not seen_any:
        try:
            return json.loads(CACHE.read_text())
        except (OSError, ValueError):
            return out
    secs_of = {k.rsplit("|", 1)[0]: v for k, v in durs.items()}
    for e in ml.scan_drums():
        out["drums"].append(dict(e, secs=secs_of.get(e["path"]) or 0,
                                 folder=str(Path(e["path"]).parent.name)))
    try:
        CACHE.write_text(json.dumps(out))
        ml.DUR_CACHE.write_text(json.dumps(durs))
    except OSError:
        pass
    return out


def lane_category(lane):
    return {"kick": "drums", "leadloop": "lead", "bassloop": "bass",
            "fxloop": "fx"}.get(lane) or LANE5[lane]


def candidates(lane):
    """Dropdown list for one lane: its category only, grouped by folder."""
    pool = scan_all()[lane_category(lane)]
    return sorted(pool, key=lambda e: (e["folder"].lower(), e["name"].lower()))


def source_bpm(secs, named_bpm, near_bpm):
    """A loop's tempo: the BPM in its name, else the whole-bar count whose
    implied tempo sits closest to `near_bpm` (measured from length)."""
    if named_bpm:
        return float(named_bpm)
    bars = min((0.25, 0.5, 1, 2, 4, 8, 16),
               key=lambda b: abs(b * 240.0 / secs - near_bpm))
    return bars * 240.0 / secs


def _load(path):
    from make_hiphop_tracks import load_audio
    x = load_audio(path)
    if x is None or not len(x):
        raise FileNotFoundError(f"Couldn't read {path}")
    return x                                        # (n, 2)


def _stretch(x, sr, ratio):
    if abs(ratio - 1.0) < 0.002:
        return x
    import pedalboard
    y = pedalboard.time_stretch(np.ascontiguousarray(x.T, dtype=np.float32),
                                sr, stretch_factor=float(ratio))
    return y.T.astype(np.float64)


def build_lane(lane, path, bpm, sr, fx_bars=None):
    """(L, R) for one lane, exactly NBARS bars at `bpm`."""
    bar = int(round(240.0 / bpm * sr))
    total = NBARS * bar
    x = _load(path)
    secs = len(x) / sr
    named = ml.bpm_from_tokens(ml._tokens(Path(path), Path(path).parent))
    if lane_category(lane) == "fx":
        # sparse hits: FX only stretched when its name states a tempo;
        # tails wrap round the loop point (loop-safe renders)
        if named:
            x = _stretch(x, sr, bpm / named)
        # owner 2026-09-16: FX once or twice, never throughout — a long FX
        # file cut to one bar, faded so the cut doesn't click
        x = x[:bar].copy()
        fade = min(len(x), int(0.05 * sr))
        x[-fade:] *= np.linspace(1.0, 0.0, fade)[:, None]
        out = np.zeros((total, 2))
        for b in fx_bars or [NBARS - 1]:
            idx = (b * bar + np.arange(len(x))) % total
            np.add.at(out, idx, x)
        return out[:, 0], out[:, 1]
    src = source_bpm(secs, named, bpm)
    x = _stretch(x, sr, bpm / src)
    nb = max(1, round(len(x) / bar))
    x = loop_mode.tile_to(x, nb * bar) if len(x) < nb * bar else x[:nb * bar]
    L = loop_mode.tile_to(x[:, 0], total)
    R = loop_mode.tile_to(x[:, 1], total)
    return L, R


def _key_ok(e, anchor):
    if anchor is None or e.get("key") is None:
        return True
    return (e["key"] == anchor[0]
            and mode_family(e.get("mode") or "major")
            == mode_family(anchor[1] or "major"))


def pick_state(dj_sig, tags, home_bpm, rng):
    """Initial fill: {lanes: {lane: path}, bpm, same_key, key, fx_bars}.
    Random, leaning on DJ taste (loop_mode.pick_loop)."""
    pools = scan_all()
    lane5 = rng.choice(sorted(LANE5))
    order = ["kick", "leadloop", "bassloop", lane5, "fxloop"]
    same_key = rng.random() < SAME_KEY_ODDS
    anchor, picks, fx_bars = None, {}, {}
    bpm = None
    for lane in order:
        cat = lane_category(lane)
        pool = pools[cat]
        if cat == "fx":
            risers = [e for e in pool if e["riser"]]
            rest = [e for e in pool if not e["riser"]]
            pool = risers if (risers and (rng.random() < RISER_ODDS
                                          or not rest)) else rest
        if same_key and cat in KEYED:
            pool = [e for e in pool if _key_ok(e, anchor)]
        scored = loops_scored({"_loops": pool}, tags=tags, bpm=bpm or home_bpm)
        e, _taste = loop_mode.pick_loop(dj_sig, scored, rng)
        if e is None:
            if lane == "kick":
                raise FileNotFoundError(
                    "No drum loops found — is the sample drive plugged in?")
            continue
        picks[lane] = e["path"]
        if lane == "kick":
            bpm = int(round(source_bpm(e["secs"] or 1, e.get("bpm"), home_bpm)))
        if same_key and cat in KEYED and anchor is None and e.get("key"):
            anchor = (e["key"], e.get("mode"))
        if cat == "fx":
            fx_bars[lane] = fx_spots(rng)
    return {"lanes": picks, "bpm": bpm, "same_key": same_key,
            "key": list(anchor) if anchor else None, "fx_bars": fx_bars}


def fx_spots(rng):
    """1 or 2 random bars, never side by side."""
    first = rng.randrange(NBARS)
    if rng.random() < 0.5:
        return [first]
    return sorted([first, rng.choice([b for b in range(NBARS)
                                      if abs(b - first) % NBARS not in (0, 1, NBARS - 1)])])


def drum_bpm(path, home_bpm):
    e = next((d for d in scan_all()["drums"] if d["path"] == path), None)
    secs = (e or {}).get("secs") or _wav_secs(Path(path)) or 1
    named = (e or {}).get("bpm") or ml.bpm_from_tokens(
        ml._tokens(Path(path), Path(path).parent))
    return int(round(source_bpm(secs, named, home_bpm)))


def render_bufs(state, sr):
    """{lane: (L, R)} for every lane in the state."""
    return {ln: build_lane(ln, p, state["bpm"], sr,
                           fx_bars=state["fx_bars"].get(ln))
            for ln, p in state["lanes"].items()}


if __name__ == "__main__":
    assert categories(("Synths - Loops", "Sub Riser.wav")) == ["fx"]
    assert set(categories(("Keys", "Piano Loop 90bpm Cm.wav"))) == {"lead", "chords"}
    assert categories(("Drums", "Kick Loop 90.wav")) == []
    assert abs(source_bpm(4.0, None, 95) - 120.0) < 1e-6    # 2 bars of 120
    assert abs(source_bpm(8.0, None, 95) - 120.0) < 1e-6    # 4 bars of 120
    assert source_bpm(3.0, 87, 120) == 87.0                   # name wins
    print("self-check ok")
