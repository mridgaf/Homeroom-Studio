"""Read a reference track's tempo and key.

Section 5 of the beat-generator v-next plan. He drops a song on the page;
this reads it and hands back numbers he can correct before making beats.
Nothing from the track is sampled or kept — only the two numbers.

numpy + scipy only, deliberately: librosa is not installed here, and the
v-next plan says take the approach, not the package.

Both answers are wrong in predictable ways, which is exactly why the page
shows alternates: a tempo comes back half or double, and a key comes back
as its relative major/minor. The correction buttons are the feature, not
a fallback.
"""
from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from scipy.signal import stft

SR = 22050
N_FFT = 1024
HOP = 128
FPS = SR / HOP
TEMPO_LO, TEMPO_HI = 60, 200          # the window /make already enforces
MAX_SECS = 60.0                       # a minute out of the middle is plenty

# WHAT THIS NUMBER WAS MEASURED ON, before anyone re-tunes it: 25 of his
# own rendered beats in Favorites, whose true tempo is in the filename and
# whose true key is in the recipe. Swept 0.0/0.3/0.5/0.7/1.0 -> exact
# tempo 11/13/14/14/13. Those beats are a HARSHER set than a real song
# (drum-led, chords one lane in ten), so treat these as a floor.
HALF_W = 0.5                          # weight of the half-beat term

# The engine's spelling. beat_machine.ROOT_HZ and key_context.SUB_ROOTS
# both write the black note between A and B as "Bb", never "A#", so this
# module hands back names those tables can look up directly.
ROOTS = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B")

# Krumhansl-Schmuckler key profiles: how much each scale degree is worth
# in a major and a minor key. Rotating these twelve ways and correlating
# against the track's chroma is the whole key detector.
_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                   2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                   2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


# ------------------------------------------------------------------ audio

def _read_audio(path):
    """(mono float64 at SR, the whole file's length in seconds)."""
    import soundfile as sf
    try:
        x, native = sf.read(str(path), dtype="float64", always_2d=True)
    except Exception:
        # m4a/aac and anything else libsndfile won't open. afconvert ships
        # with macOS, so the fallback costs no dependency.
        with tempfile.TemporaryDirectory() as d:
            wav = Path(d) / "ref.wav"
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16",
                            str(path), str(wav)],
                           check=True, capture_output=True)
            x, native = sf.read(str(wav), dtype="float64", always_2d=True)
    mono = x.mean(axis=1)
    secs = len(mono) / float(native)
    want = int(MAX_SECS * native)
    if len(mono) > want:        # the middle — intros and fade-outs mislead
        start = (len(mono) - want) // 2
        mono = mono[start:start + want]
    if native != SR:
        import soxr
        mono = soxr.resample(mono, native, SR)
    return np.asarray(mono, dtype=np.float64), secs


def _onset_env(x):
    """Where the hits are: half-wave-rectified spectral flux, one value
    per HOP samples."""
    _f, _t, Z = stft(x, fs=SR, nperseg=N_FFT, noverlap=N_FFT - HOP,
                     window="hann", boundary=None, padded=False)
    # log magnitude, so a hit in a quiet passage counts like a loud one
    mag = np.log1p(1000.0 * np.abs(Z))
    env = np.maximum(np.diff(mag, axis=1), 0.0).sum(axis=0)
    if not env.size:
        return env
    # subtract a slow moving average, so a build-up doesn't swamp the pulse
    k = max(1, int(round(FPS * 0.4)))
    pad = np.pad(env, (k, k), mode="edge")
    base = np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
    return np.maximum(env - base, 0.0)


# ------------------------------------------------------------------ tempo

def _acf(env):
    """Autocorrelation of the onset envelope, via FFT."""
    n = int(2 ** math.ceil(math.log2(max(len(env), 2) * 2)))
    E = np.fft.rfft(env - env.mean(), n=n)
    return np.fft.irfft(E * np.conj(E), n=n)[:len(env)]


def detect_tempo(env):
    """(bpm, [the half and double readings that are still in range])."""
    ac = _acf(env)
    grid = np.arange(TEMPO_LO, TEMPO_HI + 0.5, 0.5)
    lags = 60.0 * FPS / grid
    keep = lags < len(ac) - 1
    grid, lags = grid[keep], lags[keep]
    if not grid.size:
        return 0, []
    # A tempo is only a tempo if the level below it is periodic too: at
    # 150 BPM the 8ths land every half-beat, at 100 they would have to
    # land in triplets. The half-lag term is what separates the two
    # readings of a dead-even pulse — without it an even 8th-note click
    # at 150 reads as 100, because the prior likes 100 better.
    idx = np.arange(len(ac))
    score = (np.interp(lags, idx, ac)
             + HALF_W * np.interp(lags / 2.0, idx, ac))
    # the usual prior: this music lives near 100, so a 190 reading of a
    # 95 BPM track loses to the 95 one
    weight = np.exp(-0.5 * (np.log2(grid / 100.0) / 0.65) ** 2)
    bpm = float(grid[int(np.argmax(score * weight))])
    alts = [int(round(b)) for b in (bpm / 2.0, bpm * 2.0)
            if TEMPO_LO <= b <= TEMPO_HI]
    return int(round(bpm)), alts


# -------------------------------------------------------------------- key

def chroma_of(x):
    """How much energy sits on each of the twelve notes, octaves folded."""
    n = 8192                             # 2.7 Hz bins: a semitone at the
    f, _t, Z = stft(x, fs=SR, nperseg=n, noverlap=n - n // 4,
                    window="hann", boundary=None, padded=False)
    # bottom of this band is ~4 Hz, so notes down there land in the right
    # bin. Both bounds were swept against his own library: dropping the
    # ceiling to 2 kHz costs 3 of 21, and a bass-only window (his "the 808
    # note IS the key" rule) collapses to 3 of 21 because the kick drowns
    # the note.
    band = (f >= 65.0) & (f <= 5000.0)
    freqs, mag = f[band], np.abs(Z)[band]
    if not freqs.size or not mag.size:
        return np.zeros(12)
    pcs = np.rint(69 + 12 * np.log2(freqs / 440.0)).astype(int) % 12
    energy = mag.sum(axis=1)
    return np.array([energy[pcs == pc].sum() for pc in range(12)])


def detect_key(x):
    """(root, mode, alt_root, alt_mode). The alternate is the relative
    major/minor — the mistake this method actually makes."""
    chroma = chroma_of(x)
    if chroma.sum() <= 0:
        return "C", "minor", "D#", "major"
    c = chroma - chroma.mean()
    best = None
    for mode, profile in (("major", _MAJOR), ("minor", _MINOR)):
        p = profile - profile.mean()
        pn = math.sqrt(float((p ** 2).sum()))
        for r in range(12):
            v = np.roll(c, -r)
            vn = math.sqrt(float((v ** 2).sum()))
            score = float((v * p).sum()) / (vn * pn) if vn and pn else 0.0
            if best is None or score > best[0]:
                best = (score, r, mode)
    _score, root, mode = best
    alt = (root + 3) % 12 if mode == "minor" else (root + 9) % 12
    return ROOTS[root], mode, ROOTS[alt], ("major" if mode == "minor"
                                           else "minor")


# ------------------------------------------------------------------- both

def analyze(path):
    """Everything the page needs from one reference track."""
    x, secs = _read_audio(path)
    bpm, alts = detect_tempo(_onset_env(x))
    root, mode, alt_root, alt_mode = detect_key(x)
    return {"bpm": bpm, "bpm_alts": alts,
            "root": root, "mode": mode,
            "alt_root": alt_root, "alt_mode": alt_mode,
            "seconds": round(secs, 1)}


def analyze_bytes(data, name="reference.wav"):
    """The server's entry point: raw upload bytes in, numbers out. The
    file is written to a temp dir and thrown away — nothing from his
    reference track is ever kept."""
    suffix = Path(str(name)).suffix or ".wav"
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / ("ref" + suffix)
        p.write_bytes(data)
        return analyze(p)


# ---------------------------------------------------------- the self-check

def _click(bpm, secs=20.0, accent=True):
    """A drum-machine-plain pulse: loud on the beat, quiet on the 8th."""
    n = int(SR * secs)
    x = np.zeros(n)
    step = SR * 30.0 / bpm                      # an 8th note
    rng = np.random.RandomState(7)
    for i in range(int(n / step)):
        at = int(i * step)
        hit = rng.randn(600) * np.exp(-np.arange(600) / 90.0)
        loud = 1.0 if (i % 2 == 0 or not accent) else 0.35
        x[at:at + 600] += hit[:max(0, min(600, n - at))] * loud
    return x


def _drone(root_pc, minor=True, secs=20.0):
    third = 3 if minor else 4
    t = np.arange(int(SR * secs)) / SR
    x = np.zeros_like(t)
    for semi in (0, third, 7, 12, 12 + third, 19):
        f = 440.0 * 2 ** ((root_pc - 9 + semi + 12 - 12) / 12.0)
        x += np.sin(2 * np.pi * f * t) / (1 + semi / 6.0)
    return x * 0.2


def demo():
    got, _ = detect_tempo(_onset_env(_click(96)))
    assert abs(got - 96) <= 2, "96 BPM click read as %s" % got
    # A dead-even pulse has no accent to say which hit is the downbeat,
    # so 75 is as true as 150 and the reading is allowed to be either —
    # but the right answer has to be one click away on the page.
    got, alts = detect_tempo(_onset_env(_click(150, accent=False)))
    assert 150 in [got] + alts, "150 BPM pulse: %s, alts %s" % (got, alts)
    root, mode, alt, alt_mode = detect_key(_drone(0, minor=True))
    assert (root, mode) == ("C", "minor"), "C minor drone read as %s %s" % (
        root, mode)
    assert (alt, alt_mode) == ("D#", "major"), "relative of Cm: %s %s" % (
        alt, alt_mode)
    print("reference_track: tempo and key self-check passed")


if __name__ == "__main__":
    demo()
