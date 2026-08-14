"""
THROW -- automatic tempo-synced delay throw on the last word of a line.

The move: everything stays dry except the final word of a phrase, which gets
thrown into a 100%-wet, tempo-synced, filtered feedback delay. It is the most
repeated manual gesture in this owner's recipe book (`upfront-rap-vocal.md`
step 6, and again in the JID DiCaprio 2 and Never Story recipes), and today
it is drawn by hand as an automation spike on the send, once per line. The
standard instruction for doing it manually ends with "you may have to redo
this until the timing sounds right" -- that redo loop is what this removes.

Prior art check (2026-08-14): phrase detection ships in products -- Magic.RIDE
detects musical phrases rather than signal peaks -- but drives a fader, not an
FX send. Nothing found that auto-triggers a throw.

STRUCTURE, per the contract in vox/core.py: the offline analysis
(`find_phrase_ends`) produces parameters; the per-block `ThrowDelay` Module
does the audio and is real-time-legal.

REAL-TIME HONESTY: `find_phrase_ends` is offline and cannot be otherwise --
a phrase end is only *known* to be a phrase end once the silence after it has
been observed, so a live version needs `min_gap_s` of lookahead (default
250 ms). The delay itself adds no latency. Do not present the detection half
as real-time-capable without that lookahead in the budget.
"""
from __future__ import annotations

import numpy as np

from ..core import Module, ParamSpec, one_pole_coeff, lin2db
from .modules import Band, Compressor

# Note divisions as a fraction of a whole note. Dotted 8th and 1/4 are the two
# the recipes actually call for; the rest are here because they cost nothing.
NOTE_DIVISIONS = {
    "1/4": 1 / 4,
    "1/4T": 1 / 6,
    "1/8D": 3 / 16,
    "1/8": 1 / 8,
    "1/8T": 1 / 12,
    "1/16": 1 / 16,
}


def note_delay_seconds(bpm: float, division: str = "1/8D") -> float:
    """Seconds per `division` at `bpm`. A whole note is 4 beats."""
    if division not in NOTE_DIVISIONS:
        raise ValueError(f"unknown division {division!r}; have {sorted(NOTE_DIVISIONS)}")
    if bpm <= 0:
        raise ValueError("bpm must be > 0")
    return (240.0 / bpm) * NOTE_DIVISIONS[division]


def energy_envelope(x: np.ndarray, fs: float, attack_s: float = 0.005,
                    release_s: float = 0.020) -> np.ndarray:
    """Rectified, asymmetrically smoothed level envelope (fast up, slow down),
    which is what tracks syllables without chattering on every glottal pulse."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    a_up = one_pole_coeff(attack_s, fs)
    a_dn = one_pole_coeff(release_s, fs)
    env = np.empty(len(x))
    e = 0.0
    for n in range(len(x)):
        v = abs(x[n])
        e += (a_up if v > e else a_dn) * (v - e)
        env[n] = e
    return env


def find_phrase_ends(x, fs, min_gap_s=0.25, min_phrase_s=0.20,
                     threshold_db=-38.0, word_s=0.30, syllable_gap_s=0.15):
    """
    Find throwable line endings.

    A phrase is a run of above-threshold audio. Its end is *throwable* only if
    at least `min_gap_s` of silence follows -- that is the musical rule, not a
    detail: the whole point of throwing the last word is that the repeats have
    an empty bar to be heard in. A word followed immediately by the next line
    would smear the two together, which is the mistake the manual method makes
    when you put the automation spike one word too early.

    threshold_db is RELATIVE to the take's own loud level (95th percentile of
    the envelope), so it adapts to how hot the stem was printed instead of
    assuming a fixed operating level.

    Runs closer together than `syllable_gap_s` are MERGED before anything is
    measured. Without that merge you have to choose between a slow envelope
    release (which inflates a 50 ms mouth click into a 240 ms "line" and
    throws it -- measured, this is why the constant is not 50 ms) and a fast
    one (which shatters a single line at every stop consonant). Merging lets
    the release stay fast and still keeps a line whole.

    Returns a list of dicts: start/end sample of the phrase, and start/end of
    the throw word (the last `word_s` of it, or the whole phrase if shorter).
    """
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    n = len(x)
    if n == 0:
        return []

    env = energy_envelope(x, fs)
    loud = np.percentile(env, 95)
    if loud <= 0:
        return []
    thresh = loud * 10 ** (threshold_db / 20.0)

    voiced = env > thresh
    # contiguous voiced runs
    edges = np.diff(voiced.astype(np.int8))
    starts = list(np.flatnonzero(edges == 1) + 1)
    ends = list(np.flatnonzero(edges == -1) + 1)
    if voiced[0]:
        starts.insert(0, 0)
    if voiced[-1]:
        ends.append(n)

    # merge runs separated by less than a syllable gap -- see docstring
    syl = int(syllable_gap_s * fs)
    merged_s, merged_e = [], []
    for s, e in zip(starts, ends):
        if merged_e and s - merged_e[-1] < syl:
            merged_e[-1] = e
        else:
            merged_s.append(s)
            merged_e.append(e)
    starts, ends = merged_s, merged_e

    min_gap = int(min_gap_s * fs)
    min_phrase = int(min_phrase_s * fs)
    word = max(int(word_s * fs), 1)

    out = []
    for i, (s, e) in enumerate(zip(starts, ends)):
        if e - s < min_phrase:
            continue                      # a click or a breath, not a line
        nxt = starts[i + 1] if i + 1 < len(starts) else n
        if nxt - e < min_gap:
            continue                      # next line comes in too fast to throw
        out.append({
            "phrase_start": int(s),
            "phrase_end": int(e),
            "word_start": int(max(s, e - word)),
            "word_end": int(e),
            "gap_s": float((nxt - e) / fs),
        })
    return out


def find_bar_ends(x, fs, bpm, bars=4, beats_per_bar=4, downbeat_s=0.0,
                  threshold_db=-38.0, word_s=0.30, search_s=0.60):
    """
    Find the last word before every `bars`-th bar line. THE RAP MODE.

    `find_phrase_ends` waits for a silence, which is a sung-vocal assumption.
    This mode instead walks the tempo grid and, at each target bar line, takes
    the last voiced audio within `search_s` before it.

    WHY, and what is actually established (2026-08-14):
    - SUPPORTED by the owner's own recipe corpus, which places this gesture
      musically, not on silence: "end every 4th bar", "double only the last
      word of every 4th bar" (recipes/hiphop/*).
    - NOT YET VERIFIED on a rap take. An earlier version of this docstring
      cited a 20 s measurement (longest inter-word gap 0.26 s, median 0.033 s)
      as evidence that "a rapper does not stop". That measurement was taken on
      `delo mirror`, which the owner has confirmed is NOT a rap vocal, so it
      says nothing about rap and has been removed. The claim it supported may
      still be true; it is currently unevidenced.

    Re-run the gap-vs-grid comparison on an actual rap stem before treating
    grid mode's superiority for hip-hop as measured rather than assumed.

    Needs `bpm` and `downbeat_s` (where beat 1 of bar 1 sits). Both are facts
    about the song, not guesses -- pass them in. A wrong downbeat puts every
    throw on the wrong syllable, and that is audible immediately.
    """
    x = np.asarray(x, dtype=np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    n = len(x)
    if n == 0 or bpm <= 0:
        return []

    env = energy_envelope(x, fs)
    loud = np.percentile(env, 95)
    if loud <= 0:
        return []
    voiced = env > loud * 10 ** (threshold_db / 20.0)

    bar_s = (60.0 / bpm) * beats_per_bar
    step = bar_s * max(int(bars), 1)
    word = max(int(word_s * fs), 1)
    search = int(search_s * fs)

    out = []
    k = 1
    while True:
        line = downbeat_s + k * step
        pos = int(round(line * fs))
        k += 1
        if pos > n:
            break
        lo = max(0, pos - search)
        seg = voiced[lo:min(pos, n)]
        if not seg.any():
            continue                       # nothing sung into this bar line
        end = lo + int(np.flatnonzero(seg)[-1]) + 1
        out.append({
            "phrase_start": lo,
            "phrase_end": end,
            "word_start": int(max(lo, end - word)),
            "word_end": int(end),
            "bar_line_s": float(line),
            "gap_s": float((pos - end) / fs),
        })
    return out


def throw_envelope(n_samples, fs, throws, ramp_s=0.020, hold_s=0.0):
    """
    Build the send-gain automation the engineer would otherwise draw by hand:
    0 everywhere, ramped to 1 across each throw word, back to 0 after.

    The ramps matter -- a rectangular send gate clicks, and clicking is the
    tell that a throw was automated rather than ridden. `hold_s` keeps the
    send open past the word if you want the tail fed a little longer.
    """
    g = np.zeros(int(n_samples))
    ramp = max(int(ramp_s * fs), 1)
    hold = int(hold_s * fs)
    for t in throws:
        s, e = t["word_start"], min(int(n_samples), t["word_end"] + hold)
        if e <= s:
            continue
        seg = e - s
        up = min(ramp, seg)
        g[s:s + up] = np.maximum(g[s:s + up], np.linspace(0.0, 1.0, up))
        if e > s + up:
            g[s + up:e] = 1.0
        dn_end = min(int(n_samples), e + ramp)
        if dn_end > e:
            g[e:dn_end] = np.maximum(g[e:dn_end],
                                     np.linspace(1.0, 0.0, dn_end - e))
    return g


class ThrowDelay(Module):
    """
    Tempo-synced feedback delay with filtered repeats. 100% wet -- this is a
    SEND, so the caller mixes it against the untouched dry signal. That is
    deliberate: pedalboard.Reverb's internal dry path was measured at -6.6 dB
    against silence (docs/06_REAL_STEM_FINDINGS.md), so this project's rule is
    that an effect never gets to touch the dry path.

    Repeats are filtered INSIDE the feedback loop, so each successive repeat
    is darker than the last -- the recipes call for HP 500 / LP 3k (phone
    band) or LP 2k (dark ping-pong). A filter outside the loop would colour
    every repeat identically, which is the wrong sound.
    """

    name = "throw_delay"
    params = (
        ParamSpec("delay_s", "float", 0.25, 0.001, 4.0, "s", curve="log"),
        ParamSpec("feedback", "float", 0.35, 0.0, 0.95, ""),
        ParamSpec("hp_hz", "float", 300.0, 20.0, 4000.0, "Hz", curve="log"),
        ParamSpec("lp_hz", "float", 3000.0, 500.0, 20000.0, "Hz", curve="log"),
    )

    def prepare(self, fs: float):
        self.fs = float(fs)
        self._alloc()

    def _alloc(self):
        # +2 so a delay of exactly buffer length can't alias onto itself
        self._n = max(int(round(self.get("delay_s") * self.fs)), 1)
        self._buf = np.zeros(self._n + 2)
        self._w = 0
        self._hp = Band(self.fs, "highpass", self.get("hp_hz"), q=0.707)
        self._lp = Band(self.fs, "lowpass", self.get("lp_hz"), q=0.707)

    def on_param_changed(self, name, value):
        if name == "delay_s":
            self._alloc()          # resizing the line is not click-free; see reset()
        elif name == "hp_hz":
            self._hp.set(freq=value)
        elif name == "lp_hz":
            self._lp.set(freq=value)

    def reset(self):
        self._buf[:] = 0.0
        self._w = 0
        self._hp.reset()
        self._lp.reset()

    def latency_samples(self) -> int:
        return 0                   # a send delay adds no latency to the dry path

    def process(self, x: np.ndarray) -> np.ndarray:
        mono_in = x.ndim == 1
        xs = x[:, None] if mono_in else x
        n_total, n_ch = xs.shape
        src = xs.mean(axis=1)
        out = np.empty(n_total)

        fb = float(np.clip(self.get("feedback"), 0.0, 0.95))
        D, buf = self._n, self._buf
        pos = 0
        # Chunk by the delay length: nothing written this chunk can be read
        # back within it, so the recursion stays exact while still vectorising.
        # Correct at block size 1 and at 8192 alike, as core.Module requires.
        while pos < n_total:
            k = min(D, n_total - pos)
            r = (self._w - D) % len(buf)
            idx = (r + np.arange(k)) % len(buf)
            delayed = buf[idx]
            delayed = self._lp.process(self._hp.process(delayed))
            out[pos:pos + k] = delayed
            widx = (self._w + np.arange(k)) % len(buf)
            buf[widx] = src[pos:pos + k] + fb * delayed
            self._w = (self._w + k) % len(buf)
            pos += k

        return out[:, None] * np.ones((1, n_ch)) if not mono_in else out


def duck_against(wet, key, fs, duck_db=6.0, attack_s=0.005, release_s=0.180):
    """
    Duck `wet` (the delay return) while `key` (the dry vocal) is present --
    the standard modern rap treatment for delay throws.

    Why this matters more than it sounds: an undicked throw competes with the
    next line, which is why the manual method needs the throw placed in a gap.
    Ducked, the repeats are pushed down under the voice and swell back into
    whatever space exists, so a throw that overlaps the next line degrades
    gracefully instead of turning to mush. It is what makes the effect usable
    on dense rap at all.

    Published practice: compressor on the delay return, keyed off the dry
    vocal, 4-8 dB of duck, fast attack, 100-250 ms release.

    Threshold is derived from the key's OWN loud level rather than assumed, so
    this works on a stem printed at any level. Returns (ducked, measured_db)
    -- the measured depth is reported because "I asked for 6 dB" and "it did
    6 dB" are different claims, and this project only accepts the second.
    """
    wet = np.asarray(wet, dtype=np.float64)
    key = np.asarray(key, dtype=np.float64)
    kmono = key.mean(axis=1) if key.ndim > 1 else key

    loud = np.percentile(np.abs(kmono), 95)
    if loud <= 0 or duck_db <= 0:
        return wet, 0.0

    # Solve the threshold so duck_db is DELIVERED, not approached. For a hard
    # knee, gr = (x - thr) * (1/ratio - 1), so hitting -duck_db at the key's
    # own working level x needs (x - thr) = duck_db / (1 - 1/ratio).
    # The first version of this set thr = loud - 6 with a soft knee and a
    # ratio picked by feel; asking for 6 dB delivered 2.9. A control that
    # silently means something else is worse than no control.
    active = np.abs(kmono) > loud * 0.5
    x_db = float(lin2db(np.sqrt(np.mean(kmono[active] ** 2)))) if active.any() \
        else float(lin2db(loud))
    ratio = 8.0
    thr_db = x_db - duck_db / (1.0 - 1.0 / ratio)

    def _run(thr):
        c = Compressor(fs, threshold_db=thr, ratio=ratio, knee_db=0.0,
                       attack_s=attack_s, release_s=release_s,
                       makeup_db=0.0, mix=1.0)
        out = c.process(wet, key=key)
        if not active.any():
            return out, 0.0
        rms = lambda s: np.sqrt(np.mean(
            (s[active] if s.ndim == 1 else s[active].mean(axis=1)) ** 2))
        return out, float(20 * np.log10((rms(wet) + 1e-20) / (rms(out) + 1e-20)))

    # CALIBRATE. The open-loop threshold consistently under-delivers on real
    # material -- measured 4.3 dB for a requested 6 on an actual rap take --
    # because the key's level moves and gain reduction is non-linear, so the
    # reduction at the average level is not the average reduction. Rather than
    # ship a control whose number is decorative, measure and correct. Offline,
    # so two extra passes cost nothing.
    ducked, measured = _run(thr_db)
    for _ in range(3):
        err = duck_db - measured
        if abs(err) < 0.3:
            break
        thr_db -= err / (1.0 - 1.0 / ratio)
        ducked, measured = _run(thr_db)
    return ducked, measured


def apply_throws(x, fs, bpm, division="1/8D", feedback=0.35, send_db=-3.0,
                 hp_hz=300.0, lp_hz=3000.0, throws=None, mode="grid",
                 bars=4, downbeat_s=0.0, duck_db=6.0, duck_attack_s=0.005,
                 duck_release_s=0.180, **detect_kw):
    """
    Offline convenience: detect the line endings, build the send automation,
    run the delay, return dry + wet.

    mode="grid" (default, RAP): throw the last word before every `bars`-th
        bar line. Needs an accurate bpm and downbeat_s.
    mode="gap" (SUNG): throw the last word of a phrase followed by real
        silence. Measured useless on dense rap -- see find_bar_ends.

    Returns (y, info). info carries the throws found and the delay time, so the
    "why did it do that" transparency requirement is satisfiable -- you can see
    exactly which words it chose before you trust it.
    """
    x = np.asarray(x, dtype=np.float64)
    mono = x.ndim == 1
    xs = x[:, None] if mono else x
    if throws is None:
        if mode == "grid":
            throws = find_bar_ends(xs, fs, bpm, bars=bars,
                                   downbeat_s=downbeat_s, **detect_kw)
        elif mode == "gap":
            throws = find_phrase_ends(xs, fs, **detect_kw)
        else:
            raise ValueError(f"mode must be 'grid' or 'gap', got {mode!r}")

    delay_s = note_delay_seconds(bpm, division)
    g = throw_envelope(len(xs), fs, throws)
    send = xs * g[:, None]

    d = ThrowDelay(fs, delay_s=delay_s, feedback=feedback,
                   hp_hz=hp_hz, lp_hz=lp_hz)
    wet = d.process(send)
    if wet.ndim == 1:
        wet = wet[:, None]

    duck_measured = 0.0
    if duck_db > 0:
        wet, duck_measured = duck_against(wet, xs, fs, duck_db=duck_db,
                                          attack_s=duck_attack_s,
                                          release_s=duck_release_s)

    y = xs + wet * (10.0 ** (send_db / 20.0))

    info = {
        "throws": throws,
        "n_throws": len(throws),
        "delay_s": delay_s,
        "division": division,
        "bpm": bpm,
        "mode": mode,
        "duck_db_requested": duck_db,
        "duck_db_measured": duck_measured,
    }
    return (y[:, 0] if mono else y), info
