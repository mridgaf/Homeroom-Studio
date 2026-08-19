"""DSP module verification: bypass nulls, aliasing bar, and the limiter's
true-peak accuracy (this file exists because that measurement caught two real
bugs during development -- see dsp/modules.py Limiter docstring)."""
import numpy as np
import pytest
from scipy import signal as sg

from vox import dsp, meter

FS = 48000


def sine(f, dbfs=0.0, dur=0.5, fs=FS, phase=0.0):
    t = np.arange(int(dur * fs)) / fs
    return (10 ** (dbfs / 20)) * np.sin(2 * np.pi * f * t + phase)


# ---------------------------------------------------------------- bypass nulls
def test_compressor_unity_ratio_nulls():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.Compressor(FS, threshold_db=0.0, ratio=1.0, makeup_db=0.0, mix=1.0).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_eq_zero_gain_nulls():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.ParametricEQ(FS, bands=[dict(kind="bell", freq=1000, gain_db=0.0, q=1.0)]).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_saturation_zero_mix_nulls():
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.Saturation(FS, mix=0.0).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_gate_settles_open_and_transparent():
    """After the cold-start attack ramp, an always-above-threshold signal
    must pass through unchanged."""
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.Gate(FS, open_db=-90, close_db=-95).process(x[:, None])[:, 0]
    assert meter.null_test_db(x[2400:], y[2400:]) < -300


# ---------------------------------------------------------------- aliasing bar
def test_saturation_8x_tanh_meets_bar():
    s = dsp.Saturation(FS, drive_db=12.0, mix=1.0, mode="tanh", oversample=8)
    r = meter.aliasing_floor_db(lambda x: s.process(x[:, None])[:, 0], FS)
    assert r["alias_db"] < -90, r


def test_saturation_4x_tanh_fails_bar():
    """Documents WHY the default is 8x: 4x measurably fails our own bar."""
    s = dsp.Saturation(FS, drive_db=12.0, mix=1.0, mode="tanh", oversample=4)
    r = meter.aliasing_floor_db(lambda x: s.process(x[:, None])[:, 0], FS)
    assert r["alias_db"] > -90


def test_saturation_adaa_hardclip_meets_bar():
    s = dsp.Saturation(FS, drive_db=12.0, mix=1.0, mode="adaa_hardclip", oversample=8)
    r = meter.aliasing_floor_db(lambda x: s.process(x[:, None])[:, 0], FS)
    assert r["alias_db"] < -90, r


def test_saturation_channels_are_independent():
    """Regression: the oversampling filters kept ONE shared zi across all
    channels, so channel N started from channel N-1's filter tail. On real
    true-stereo material that put a 0.76-amplitude error (larger than the
    signal) in the first 64 samples of the right channel -- an audible pop at
    every block boundary. Right channel must process identically whether it's
    alone or alongside a different left channel."""
    rng = np.random.RandomState(0)
    n = 4000
    left, right = rng.randn(n) * 0.2, rng.randn(n) * 0.2  # deliberately different

    def sat():
        return dsp.Saturation(FS, drive_db=6.0, mix=1.0, mode="tanh", oversample=8)

    in_pair = sat().process(np.stack([left, right], axis=1))[:, 1]
    alone = sat().process(right[:, None])[:, 0]
    assert np.max(np.abs(in_pair - alone)) < 1e-12


# ---------------------------------------------------------------- limiter
@pytest.mark.parametrize("f0,phase", [
    (997, 0.0), (12000, 0.7), (12000, 0.3), (19000, 0.0), (20500, 0.3), (8000, 1.1),
])
def test_limiter_never_exceeds_true_peak_ceiling(f0, phase):
    lim = dsp.Limiter(FS, ceiling_dbtp=-1.0, lookahead_ms=5.0)
    x = 1.3 * sine(f0, dur=0.5, phase=phase)
    y = lim.process(x[:, None])[:, 0]
    tp = meter.true_peak_db(y, FS)
    assert tp <= -1.0 + 0.15, f"overshoot at {f0}Hz phase {phase}: {tp} dBTP"


def test_limiter_transparent_below_ceiling():
    """A signal already well under the ceiling must pass through essentially
    unchanged (aside from the reported lookahead delay)."""
    x = np.random.RandomState(1).randn(FS) * 0.05
    lim = dsp.Limiter(FS, ceiling_dbtp=-1.0)
    y = lim.process(x[:, None])[:, 0]
    la = lim.la_n
    assert meter.null_test_db(x[:-la], y[la:]) < -60


def test_limiter_detector_matches_reference_meter():
    """The detector's own true-peak estimate must agree with meter.true_peak_db
    (independently implemented) to within 0.05 dB -- this is the check that
    caught the rectify-before-interpolate bug."""
    lim = dsp.Limiter(FS, ceiling_dbtp=-1.0)
    x = 1.3 * sine(12000, dur=0.5, phase=0.7)
    env = lim._true_peak_envelope(x[:, None])
    got = 20 * np.log10(env.max())
    want = meter.true_peak_db(x, FS)
    assert abs(got - want) < 0.05, (got, want)


# -- Stack (harmonizer doubler) ------------------------------------------
def test_stack_nulls_at_zero_mix():
    from vox.dsp import Stack
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = Stack(FS, mix=0.0).process(x[:, None])[:, 0]
    assert np.max(np.abs(x - y)) == 0.0


def test_stack_is_block_size_invariant():
    """core.Module's contract: identical at block size 1 and 8192. The first
    version failed this at large blocks -- a long block overwrote delay-line
    history the taps were still reading."""
    from vox.dsp import Stack
    t = np.arange(FS) / FS
    x = (np.sin(2 * np.pi * 440 * t) * 0.3)[:, None] * np.ones((1, 2))

    def run(bs):
        s = Stack(FS, mix=1.0)
        return np.concatenate([s.process(x[i:i + bs]) for i in range(0, len(x), bs)])

    assert np.max(np.abs(run(1) - run(8192))) < 1e-9


def test_stack_voices_are_pitch_shifted_the_documented_amount():
    """+12 cents left, -12 cents right (TUPAC-VOCAL-STACKING-TECHNIQUE.md).
    Measured off the wet-only difference against the dry input."""
    from vox.dsp import Stack
    t = np.arange(3 * FS) / FS
    x = (np.sin(2 * np.pi * 440 * t) * 0.3)[:, None] * np.ones((1, 2))
    wet = Stack(FS, mix=1.0).process(x) - x

    def f0(seg):
        w = seg * np.hanning(len(seg))
        sp = np.abs(np.fft.rfft(w))
        i = int(np.argmax(sp))
        a, b, c = np.log(sp[i - 1:i + 2] + 1e-30)
        return (i + 0.5 * (a - c) / (a - 2 * b + c)) * FS / len(seg)

    up, down = f0(wet[FS:2 * FS, 0]), f0(wet[FS:2 * FS, 1])
    assert abs(up - 440 * 2 ** (12 / 1200)) < 2.0
    assert abs(down - 440 * 2 ** (-12 / 1200)) < 2.0


# -- DeEsser --------------------------------------------------------------
def test_deesser_cuts_sibilance_without_eating_the_body():
    """REGRESSION: the sidechain and the subtracted band were both a bell at
    0 dB gain, which is an identity filter -- so this module was a broadband
    ducker that pulled 4.8 dB out of the body to get 2.2 dB of sibilance
    (measured against T-De-Esser, tools/ab_reference.py). Body must survive."""
    fs = FS
    t = np.arange(2 * fs) / fs
    body = 0.3 * np.sin(2 * np.pi * 300 * t)
    ess = 0.3 * np.sin(2 * np.pi * 8000 * t)
    x = body + ess

    y = dsp.DeEsser(fs, freq_hz=7000.0, threshold_db=-30.0, ratio=4.0,
                    range_db=12.0, mix=1.0).process(x[:, None])[:, 0]

    def level(sig_, f0):
        w = np.hanning(len(sig_))
        sp = np.abs(np.fft.rfft(sig_ * w))
        i = int(round(f0 * len(sig_) / fs))
        return 20 * np.log10(np.max(sp[i - 8:i + 9]) + 1e-30)

    assert level(y, 8000) - level(x, 8000) < -4.0   # sibilance genuinely cut
    assert abs(level(y, 300) - level(x, 300)) < 0.5  # body essentially untouched
