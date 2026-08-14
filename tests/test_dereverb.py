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


@pytest.mark.xfail(
    reason="KNOWN BUG, see docs/06_REAL_STEM_FINDINGS.md: the frame-persistence "
           "model can't tell a held/sustained dry tone from a decaying reverb "
           "tail -- both look like 'energy that outlasts direct_frames' to it. "
           "Confirmed on real vocal material (muffled complaint, 2026-08-13). "
           "This is why dereverb defaults to OFF in chain_demo.py. If this test "
           "starts passing, the algorithm was actually fixed -- remove the "
           "xfail, don't just re-enable the default blindly; re-verify on a "
           "real stem too, the synthetic bench alone missed this bug originally.",
    strict=True,
)
def test_dry_sustained_tone_is_not_treated_as_reverb():
    """A pure sustained tone with ZERO reverb, run through the estimator's
    OWN blind RT60 estimate (the real-world default -- no oracle RT60), must
    come out close to untouched. It does not: measured ~20 dB of suppression
    on this exact signal during real-stem testing."""
    fs = FS
    t = np.arange(int(3 * fs)) / fs
    tone = 0.3 * np.sin(2 * np.pi * 220 * t)
    y, _info = dereverb.suppress_late_reverb(tone, fs)
    before = 20 * np.log10(np.sqrt(np.mean(tone[fs:] ** 2)) + 1e-12)
    after = 20 * np.log10(np.sqrt(np.mean(y[fs:] ** 2)) + 1e-12)
    assert before - after < 3.0, f"suppressed a dry tone by {before - after:.1f} dB"
