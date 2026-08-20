"""
Verifies the hand-rolled single-channel de-reverb against the synthetic
testbench's KNOWN rt60 and KNOWN dry reference (see testsignal.py). This
replaces nara_wpe, which measured as ineffective on mono input (see
docs/03_engineer.md addendum): -77.5 -> -77.8 dB tail RMS, i.e. no real
suppression. This module must beat that.
"""
import numpy as np
import pytest

from vox.testsignal import make_testbench
from vox.dsp import dereverb

FS = 48000


def _tail_rms_db(x, fs, tail_s=0.15):
    seg = x[-int(tail_s * fs):]
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12)


def _snr_proxy(ref, test):
    n = min(len(ref), len(test))
    a = ref[:n] / (np.sqrt(np.mean(ref[:n] ** 2)) + 1e-12)
    b = test[:n] / (np.sqrt(np.mean(test[:n] ** 2)) + 1e-12)
    err = a - b
    return 20 * np.log10((np.sqrt(np.mean(a ** 2)) + 1e-12) / (np.sqrt(np.mean(err ** 2)) + 1e-12))


def test_rt60_blind_estimate_midband_accurate():
    """1-2 kHz band has the most vocal energy in our testbench, so the blind
    Schroeder-slope RT60 estimate should land within 0.15 s of ground truth
    there, even though extremes (low bass / high air band) are noisier with
    only ~3s of signal -- documented, not hidden."""
    dirty, truth = make_testbench(fs=FS, seed=1, rt60=0.6, noise_db=-90, hum_db=-90)
    est = dereverb.estimate_rt60_bands(dirty, FS)
    freqs = np.fft.rfftfreq(1024, 1 / FS)
    i = np.argmin(np.abs(freqs - 1000))
    assert abs(est[i] - truth["rt60"]) < 0.15, est[i]


def test_late_reverb_suppression_reduces_tail_energy():
    dirty, truth = make_testbench(fs=FS, seed=1, rt60=0.6, noise_db=-90, hum_db=-90)
    y, info = dereverb.suppress_late_reverb(dirty, FS, strength=1.0, floor_db=-18)
    before, after = _tail_rms_db(dirty, FS), _tail_rms_db(y, FS)
    assert after < before - 10.0, (before, after)  # must beat the WPE mono result decisively


def test_late_reverb_suppression_improves_snr_proxy():
    dirty, truth = make_testbench(fs=FS, seed=1, rt60=0.6, noise_db=-90, hum_db=-90)
    y, info = dereverb.suppress_late_reverb(dirty, FS, strength=1.0, floor_db=-18)
    clean = truth["clean_dry"]
    assert _snr_proxy(clean, y) > _snr_proxy(clean, dirty[: len(y)]) + 1.0


def test_latency_is_bounded_and_reported():
    """Architecture requirement: no algorithm may claim real-time viability
    without a stated, fixed latency. This estimator is causal with D frames
    of look-ahead-free delay -- confirm it stays small and is reported."""
    dirty, _ = make_testbench(fs=FS, seed=1, rt60=0.6)
    _, info = dereverb.suppress_late_reverb(dirty, FS, direct_frames=2)
    assert info["latency_ms"] < 30.0
    assert info["latency_frames"] == 2


def test_strength_zero_is_near_transparent():
    """strength=0 must not meaningfully alter the signal (sanity/regression
    guard against the gain floor accidentally engaging at rest)."""
    dirty, _ = make_testbench(fs=FS, seed=1, rt60=0.6, noise_db=-90, hum_db=-90)
    y, _ = dereverb.suppress_late_reverb(dirty, FS, strength=0.0, floor_db=-60)
    n = min(len(y), len(dirty))
    # STFT/ISTFT round trip alone introduces some error; bound it generously.
    err = 20 * np.log10(np.max(np.abs(y[:n] - dirty[:n])) + 1e-12)
    assert err < -20.0


def test_dry_sustained_tone_is_not_treated_as_reverb():
    """A pure sustained tone with ZERO reverb, run through the estimator's
    OWN blind RT60 estimate (the real-world default -- no oracle RT60), must
    come out close to untouched.

    THE project's worst bug (2026-08-13, real vocal, "muffled"): measured
    ~20 dB of suppression on this exact signal. Was xfail; fixed 2026-08-14
    by the decay gate in suppress_late_reverb -- now 0.0 dB. Do NOT loosen
    this threshold; if it regresses, the gate broke."""
    fs = FS
    t = np.arange(int(3 * fs)) / fs
    tone = 0.3 * np.sin(2 * np.pi * 220 * t)
    y, _info = dereverb.suppress_late_reverb(tone, fs)
    before = 20 * np.log10(np.sqrt(np.mean(tone[fs:] ** 2)) + 1e-12)
    after = 20 * np.log10(np.sqrt(np.mean(y[fs:] ** 2)) + 1e-12)
    assert before - after < 3.0, f"suppressed a dry tone by {before - after:.1f} dB"


def test_slowly_fading_dry_note_is_not_treated_as_reverb():
    """The harder half of the same bug, and the one the original test did not
    cover: a DRY note that fades naturally (6 dB/s) is decaying, so a naive
    decay detector would call it a reverb tail. It must not -- real reverb at
    the RT60s we care about decays 50-200 dB/s, two orders of magnitude
    faster. This is what stops the fix from being 'never suppress anything
    that changes level'."""
    fs = FS
    t = np.arange(int(3 * fs)) / fs
    note = 0.3 * np.sin(2 * np.pi * 220 * t) * 10 ** (-6.0 * t / 20.0)
    y, _info = dereverb.suppress_late_reverb(note, fs)
    before = 20 * np.log10(np.sqrt(np.mean(note[fs:] ** 2)) + 1e-12)
    after = 20 * np.log10(np.sqrt(np.mean(y[fs:] ** 2)) + 1e-12)
    assert before - after < 3.0, f"suppressed a fading dry note by {before - after:.1f} dB"


def test_decay_gate_separates_sustained_from_reverberant():
    """Directly assert the mechanism, not just its effect: the reported mean
    decay weight must be near zero on dry sustained content and clearly
    engaged on genuinely reverberant content. Guards against a future 'fix'
    that passes the two tests above by simply never subtracting anything."""
    t = np.arange(int(3 * FS)) / FS
    tone = 0.3 * np.sin(2 * np.pi * 220 * t)
    _, dry_info = dereverb.suppress_late_reverb(tone, FS)
    dirty, _ = make_testbench(fs=FS, seed=1, rt60=0.6, noise_db=-90, hum_db=-90)
    _, wet_info = dereverb.suppress_late_reverb(dirty, FS)
    assert dry_info["mean_decay_weight"] < 0.15, dry_info["mean_decay_weight"]
    assert wet_info["mean_decay_weight"] > dry_info["mean_decay_weight"] * 2


@pytest.mark.xfail(
    reason="KNOWN, MEASURED 2026-08-19: this module's central mechanism is "
           "inert. It implements the Lebart/Habets statistical model, whose "
           "key parameter is the per-band RT60 -- but (a) the blind estimator "
           "returns 3.0 s in EVERY band on the synthetic bench, pegged at its "
           "own clamp ceiling, against a ground truth of 0.45 s, and (b) "
           "forcing RT60 across a 16x range (x0.25 to x4.0) moves tail energy "
           "by 1.05 dB total. Whatever suppression this module achieves comes "
           "from the decay gate added 2026-08-14, not from the statistical "
           "model it is built around. "
           "ROOT CAUSE: Schroeder backward integration is defined on an "
           "impulse-response DECAY. Applied to a whole vocal take, the EDC of "
           "roughly stationary material is a linear energy ramp, so the "
           "-5..-25 dB fit measures clip duration, not room decay. "
           "Not fixable by tuning: needs onset-gated estimation (fit only on "
           "decaying regions after note offsets) or an externally supplied "
           "RT60. Do NOT loosen this test to make it pass.",
    strict=True,
)
def test_rt60_is_load_bearing():
    """The RT60 estimate must actually drive the suppression.

    A module whose defining parameter can be wrong by 16x without changing the
    result is not doing what its docstring says. This test is the spec for a
    replacement: make the estimate matter, or drop the statistical model and
    keep only the decay gate that is demonstrably doing the work.
    """
    from vox.dsp import estimate_rt60_bands, suppress_late_reverb
    from vox.testsignal import make_testbench

    dirty, _truth = make_testbench(fs=FS, seed=0, voice="male")
    est = estimate_rt60_bands(dirty, FS)

    def scaled(k):
        return {b: float(v) * k for b, v in est.items()} if hasattr(est, "items") \
            else np.asarray(est) * k

    def tail_db(y):
        seg = y[int(3.0 * FS):int(3.3 * FS)]
        return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-30)

    short, _ = suppress_late_reverb(dirty, FS, rt60_bands=scaled(0.25))
    long_, _ = suppress_late_reverb(dirty, FS, rt60_bands=scaled(4.0))
    spread = abs(tail_db(short) - tail_db(long_))
    assert spread > 3.0, (
        f"RT60 changed 16x, tail energy moved {spread:.2f} dB -- the parameter is inert")
