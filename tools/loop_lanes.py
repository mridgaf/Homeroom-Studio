"""Loops-only beats, FIVE LANES (owner spec 2026-09-16, DECISIONS.md
"Loops-only beats: FIVE LANES" — every rule below is his answer, not a
guess; read that entry before changing any number here).

  kick       the full drum loop (lane name kept as "kick": the mix bus
             anchors every level to a lane called kick)
  leadloop   guitar / synth / orchestral / melodies / keys
  bassloop   bass lines, subs
  fxloop     FX, sparse (1-2 hits per 8 bars)
  lane 5     chordloop | percloop | vocalloop, a third each (one FX lane only)

Tempo = the drum loop's BPM; everything else is time-stretched to it,
pitch never moves. Always 8 bars. Half of beats match key LABELS on
lead/bass/chords (unlabeled still allowed), half ignore key.
"""
from __future__ import annotations

import json
import math
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
         "vocalloop": "vocals"}
OLD_LANE5 = {"fxloop2": "fx"}   # beats already made keep their second FX lane
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
            "fxloop": "fx"}.get(lane) or {**LANE5, **OLD_LANE5}[lane]


def candidates(lane):
    """Dropdown list for one lane: its category only, grouped by folder."""
    pool = scan_all()[lane_category(lane)]
    return sorted(pool, key=lambda e: (e["folder"].lower(), e["name"].lower()))


def source_bpm(secs, named_bpm, near_bpm):
    """A loop's tempo: the BPM in its name, else the whole-bar count whose
    implied tempo sits closest to `near_bpm` (measured from length)."""
    if named_bpm:
        # fold to half/double time when that is the nearer fit, so a 70 BPM
        # loop in a 140 beat plays as-is instead of being stretched 2x
        return float(min((named_bpm / 2.0, float(named_bpm), named_bpm * 2.0),
                         key=lambda b: abs(math.log(near_bpm / b))))
    bars = min((0.25, 0.5, 1, 2, 4, 8, 16),
               key=lambda b: abs(b * 240.0 / secs - near_bpm))
    return bars * 240.0 / secs


NEAR = 0.20                      # swap list: stretch of at most +-20%


def near_tempo(entries, lane, bpm, current=None):
    """Swap-list entries that need little stretch to sit at `bpm`. FX lanes
    are not stretched, so they pass untouched. If fewer than 8 qualify, the
    8 closest are kept so the list is never empty."""
    if lane_category(lane) == "fx":
        return entries
    def off(e):
        return abs(bpm / source_bpm(e.get("secs") or 1, e.get("bpm"), bpm) - 1)
    ok = [e for e in entries if off(e) <= NEAR or e["path"] == current]
    return ok if len(ok) >= 8 else sorted(entries, key=off)[:8]


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


# CRATE DIGGER (owner 2026-10-31, PLAN-B-CRATE-DIGGER.md): on new beats
# the lead loop may be cut at its hits and re-played in a new 2-bar order.
# Saved in the beat's loop_state as "chop"; beats without it play whole.
CHOP_ODDS = 0.5                  # owner: half of new loops beats chop
RESAMPLE_ODDS = 0.25             # owner: 1 in 4 chopped beats chops the chop
SAME_CHORD = 0.95                # Claude's pick, unheard: a bar this close to
                                 # the first bar = same chord (measured: chord changes 0.55-0.92, repeats 0.94-0.99)
PHRASE_BARS = 2
# lens/grid in 16ths; nudge_ms = how far a hit may slide off the grid.
# Claude's numbers from the plan's style table, not sourced, not heard.
CHOP_STYLES = {
    "stabs": {"lens": (1, 2), "grid": 2, "hits": (6, 10), "nudge_ms": 0},
    "loose": {"lens": (2, 3, 4), "grid": 2, "hits": (5, 8), "nudge_ms": 30},
    "held":  {"lens": None, "grid": 4, "hits": (2, 4), "nudge_ms": 0},
}
# ponytail: the one batch whose key the detector guessed (2026-09-18 synth
# loops, ~46% right); owner: chop only pack-labelled keys. List any new
# guessed batch here.
GUESSED_KEY = re.compile(r"^synth\d+_", re.I)


def chop_ok(e):
    """A lead loop may be chopped: its key came from the pack's own label."""
    return bool(e and e.get("key")) and not GUESSED_KEY.match(Path(e["path"]).name)


def chop_roll(style, rng, lead):
    """The "chop" block for a new beat's loop_state, or None (whole loop)."""
    if style not in CHOP_STYLES or not chop_ok(lead) or rng.random() >= CHOP_ODDS:
        return None
    return {"style": style, "seed": rng.randrange(1 << 30),
            "resample": rng.random() < RESAMPLE_ODDS}


def _notes(seg, sr):
    """Unit 12-note profile of a stretch of audio (octaves folded)."""
    m = seg.mean(axis=1)
    mag = np.abs(np.fft.rfft(m * np.hanning(len(m))))
    f = np.fft.rfftfreq(len(m), 1.0 / sr)
    band = (f >= 65.0) & (f <= 5000.0)
    pcs = np.rint(69 + 12 * np.log2(f[band] / 440.0)).astype(int) % 12
    v = np.bincount(pcs, weights=mag[band], minlength=12)
    return v / (np.linalg.norm(v) or 1.0)


def _chop_once(x, sr, bpm, style, rng):
    """One 2-bar phrase (n, 2) from loop `x`: slices of ONE chord laid on
    the 16th grid in this style. Tails wrap round the phrase (loop-safe)."""
    st = CHOP_STYLES[style]
    P = PHRASE_BARS * int(round(240.0 / bpm * sr))  # whole bars, as build_lane
    six = P / (PHRASE_BARS * 16.0)                  # one 16th, in samples
    # ONE chord: slices only from bars whose notes match the first bar's.
    # A slice may run on through matching bars (a long held chop) and
    # stops where a different bar starts. ponytail: judged per bar, so a
    # chord change in the middle of a bar slips through; per-beat if heard.
    bar = P // PHRASE_BARS
    nb = max(1, len(x) // bar)
    home = _notes(x[:bar], sr)
    ok = [_notes(x[b * bar:(b + 1) * bar], sr) @ home >= SAME_CHORD
          for b in range(nb)]
    end, run_end = {}, nb * bar
    for b in reversed(range(nb)):
        run_end = run_end if ok[b] else b * bar
        end[b] = run_end
    starts = [s for s in ml.onset_starts(x.mean(axis=1), sr, min_dur=0.08)
              if s < nb * bar and ok[s // bar]
              and end[s // bar] - s > int(0.05 * sr)]
    if not starts:
        return None
    end = {s: end[s // bar] for s in starts}
    slots = list(range(0, PHRASE_BARS * 16, st["grid"]))
    k = min(len(slots), rng.randint(*st["hits"]))
    pos = sorted({0, *rng.sample(slots[1:], k - 1)})
    out = np.zeros((P, 2))
    fi, fo = int(0.002 * sr), int(0.005 * sr)       # de-click each slice
    for i, p in enumerate(pos):
        gap = (pos[i + 1] if i + 1 < len(pos) else PHRASE_BARS * 16) - p
        n16 = gap if st["lens"] is None else min(gap, rng.choice(st["lens"]))
        n = int(round(n16 * six))
        s = rng.choice(starts)
        seg = x[s:min(end[s], s + n)].copy()
        n = len(seg)
        seg[:fi] *= np.linspace(0, 1, fi)[:, None]
        seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
        nudge = rng.uniform(-0.3, 1.0) * st["nudge_ms"] / 1000.0 * sr
        at = int(round(p * six + nudge))
        out[(at + np.arange(n)) % P] += seg
    return out


def chop(x, sr, bpm, spec):
    """The chopped phrase for a saved "chop" block; None = play it whole."""
    rng = random.Random(spec["seed"])
    x = x[:, :2]                       # L/R only, as build_lane plays them
    y = _chop_once(x, sr, bpm, spec["style"], rng)
    if y is not None and spec.get("resample"):      # chop the printed chop
        y2 = _chop_once(y, sr, bpm, spec["style"], rng)
        y = y if y2 is None else y2
    return y


def build_lane(lane, path, bpm, sr, fx_bars=None, chop_spec=None):
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
    if chop_spec:
        y = chop(x, sr, bpm, chop_spec)
        x = x if y is None else y
    L = loop_mode.tile_to(x[:, 0], total)
    R = loop_mode.tile_to(x[:, 1], total)
    return L, R


def _key_ok(e, anchor):
    if anchor is None or e.get("key") is None:
        return True
    return (e["key"] == anchor[0]
            and mode_family(e.get("mode") or "major")
            == mode_family(anchor[1] or "major"))


def pick_state(dj_sig, tags, home_bpm, rng, groups=None):
    """Initial fill: {lanes: {lane: path}, bpm, same_key, key, fx_bars}.
    Random, leaning on DJ taste (loop_mode.pick_loop). `groups`: the
    identity's loop_vocab word groups, joining the exact tags."""
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
        scored = loops_scored({"_loops": pool}, tags=tags, bpm=bpm or home_bpm,
                              groups=groups)
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
    """{lane: (L, R)} for every lane in the state. A saved "chop" block
    chops the lead loop, while that loop's key is pack-labelled (a swap
    to an unlabelled loop plays it whole)."""
    spec = state.get("chop")
    lead = state["lanes"].get("leadloop")
    if spec and not chop_ok(next((e for e in scan_all()["lead"]
                                  if e["path"] == lead), None)):
        spec = None
    return {ln: build_lane(ln, p, state["bpm"], sr,
                           fx_bars=state["fx_bars"].get(ln),
                           chop_spec=spec if ln == "leadloop" else None)
            for ln, p in state["lanes"].items()}


if __name__ == "__main__":
    assert categories(("Synths - Loops", "Sub Riser.wav")) == ["fx"]
    assert set(categories(("Keys", "Piano Loop 90bpm Cm.wav"))) == {"lead", "chords"}
    assert categories(("Drums", "Kick Loop 90.wav")) == []
    assert abs(source_bpm(4.0, None, 95) - 120.0) < 1e-6    # 2 bars of 120
    assert abs(source_bpm(8.0, None, 95) - 120.0) < 1e-6    # 4 bars of 120
    assert source_bpm(3.0, 87, 120) == 87.0                   # name wins
    print("self-check ok")
