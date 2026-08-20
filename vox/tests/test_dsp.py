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
    """At mix=0 the output must be the input -- delayed by the module's
    reported latency, NOT bit-aligned to it.

    The dry path is delayed to match the wet path (see
    test_saturation_partial_mix_does_not_comb). That delay deliberately stays
    constant at every mix value: a module whose latency changes when you move
    a mix knob breaks the host's delay compensation and jumps the signal
    mid-automation. Constant latency is the correct behaviour, so this test
    nulls against the delayed input.
    """
    m = dsp.Saturation(FS, mix=0.0)
    lat = m.latency_samples()
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = m.process(x[:, None])[:, 0]
    assert meter.null_test_db(x[:-lat], y[lat:]) < -300


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
    to within 0.05 dB -- this is the check that caught the
    rectify-before-interpolate bug.

    NOTE what this does and does not prove. meter.true_peak_db is NOT an
    independent implementation: both it and the detector are
    firwin(48*OS+1, 1/OS, kaiser) zero-stuffed interpolation, same window,
    same tap count. This test can only catch one drifting from the other, not
    an error they share. test_true_peak_matches_an_independent_resampler is
    the one that grades the method itself.
    """
    lim = dsp.Limiter(FS, ceiling_dbtp=-1.0)
    x = 1.3 * sine(12000, dur=0.5, phase=0.7)
    env = lim._true_peak_envelope(x[:, None])
    got = 20 * np.log10(env.max())
    want = meter.true_peak_db(x, FS)
    assert abs(got - want) < 0.05, (got, want)


def _faded(f, phase, amp=0.7, dur=1.0):
    """A sine with faded ends.

    The fade is load-bearing. Both true-peak methods interpolate, and both ring
    at a signal boundary -- so a raw slice out of the middle of a tone (or the
    edge of a resampled buffer) reads several TENTHS of a dB above the real
    peak. An adversarial review of this project reported a 0.40 dB limiter
    overshoot that was entirely this artifact, and the same mistake was
    reproduced and caught while verifying the claim. Fade, do not slice.
    """
    x = sine(f, dur=dur, phase=phase) * amp
    return x * sg.windows.tukey(len(x), 0.1)


def _independent_true_peak_db(x, os=64):
    """True peak via polyphase resampling -- a genuinely different algorithm
    from the project's zero-stuff + firwin path."""
    return 20 * np.log10(np.max(np.abs(sg.resample_poly(x, os, 1))) + 1e-30)


@pytest.mark.parametrize("f", [997, 4000, 8000, 9600, 12000, 16000, 19200, 20500])
def test_true_peak_matches_an_independent_resampler(f):
    """Grade meter.true_peak_db against a different algorithm, across the band.

    This is the test that actually validates the method.
    test_limiter_detector_matches_reference_meter cannot: it compares two
    instances of the SAME algorithm.

    The frequency list is chosen adversarially -- 9600, 12000, 16000 and 19200
    are fs/5, fs/4, fs/3 and fs/2.5. At exact submultiples the interpolation
    grid lands on the same phases every cycle, so it can straddle the true peak
    indefinitely rather than converging. Worst error over 32 phases at the
    4x the spec permits is -0.464 dB; the 16x default gets it to -0.059.
    """
    err = [meter.true_peak_db(_faded(f, ph), FS) - _independent_true_peak_db(_faded(f, ph))
           for ph in np.linspace(0, 2 * np.pi, 16, endpoint=False)]
    worst = max(err, key=abs)
    assert abs(worst) < 0.1, f"{f} Hz: worst {worst:+.3f} dB (bar is +/-0.1 dBTP)"


def test_limiter_holds_its_ceiling_against_an_independent_resampler():
    """End-to-end: the limiter's OUTPUT, graded by an algorithm that shares
    nothing with its detector.

    Test material is deliberately bandlimited-ish (summed harmonics, plus
    noise through a lowpass). Hard-clipped noise is NOT a fair test signal
    here: it has discontinuities, so it is not bandlimited, "true peak" is
    ill-defined for it, and different reconstruction filters legitimately
    disagree by ~0.4 dB. Measured on the real reference acapellas driven 12 dB
    into the limiter, worst overshoot is +0.043 dB.
    """
    rng = np.random.default_rng(0)
    t = np.arange(FS) / FS
    dense = sum(np.sin(2 * np.pi * f * t + p) for f, p in
                zip([220, 440, 661, 883, 1103, 2207, 4409, 8819], rng.random(8) * 6.28))
    noise = sg.lfilter(*sg.butter(4, 16000 / (FS / 2)), rng.standard_normal(FS))
    for name, x in [("harmonics", dense / np.max(np.abs(dense)) * 0.95),
                    ("lp noise", noise / np.max(np.abs(noise)) * 0.95)]:
        lim = dsp.Limiter(FS)
        lim.set("ceiling_dbtp", -1.0)
        y = lim.process(x[:, None])[:, 0]
        got = _independent_true_peak_db(y)
        assert got < -1.0 + 0.1, f"{name}: {got:+.3f} dBTP over a -1.0 ceiling"


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


# --------------------------------------------- partial-mix / latency alignment
def _response_ripple_db(mod, fs=FS, lo=100.0, hi=15000.0):
    """Magnitude response of `mod` on white noise, in dB, over [lo, hi).

    Welch on a long noise burst: at low drive tanh is essentially linear, so
    any ripple here is a filtering artifact, not distortion.
    """
    x = np.random.RandomState(0).randn(8 * fs) * 0.02
    y = mod.process(x[:, None])[:, 0]
    f, pxx = sg.welch(x, fs, nperseg=8192)
    _, pyy = sg.welch(y, fs, nperseg=8192)
    band = (f >= lo) & (f < hi)
    h = 10 * np.log10(pyy[band] / pxx[band])
    return h.min(), h.max()


@pytest.mark.parametrize("mix", [0.1, 0.15, 0.2, 0.5, 0.75])
def test_saturation_partial_mix_does_not_comb(mix):
    """REGRESSION: the wet path is delayed by latency_samples() (32 samples of
    oversampling FIR), so mixing it against an UNDELAYED dry signal is a comb
    filter, not a blend.

    Measured before the fix at the settings the presets actually ship
    (Eminem mix=0.10, Tupac mix=0.20, chain_demo mix=0.15): -3.81/+0.86 dB of
    ripple across 100 Hz-15 kHz, with notches every ~1.5 kHz. The "light Neve
    warmth" stage was a comb filter sitting on the vocal.

    Every other saturation test uses mix=0 (nulls) or mix=1 (no dry path at
    all), so none of them can see this. Partial mix is the only place it lives,
    and partial mix is all the product uses.
    """
    lo, hi = _response_ripple_db(
        dsp.Saturation(FS, drive_db=0.0, mix=mix, oversample=8, mode="tanh"))
    assert lo > -0.5 and hi < 0.5, f"comb ripple at mix={mix}: {lo:+.2f}/{hi:+.2f} dB"


def test_saturation_reports_its_true_latency():
    """latency_samples() must match the measured impulse delay -- a host that
    trusts it for PDC misaligns every parallel path if it lies."""
    m = dsp.Saturation(FS, drive_db=0.0, mix=1.0, oversample=8, mode="tanh")
    imp = np.zeros(4096)
    imp[100] = 0.5
    y = m.process(imp[:, None])[:, 0]
    assert abs(int(np.argmax(np.abs(y))) - 100 - m.latency_samples()) <= 1


# ------------------------------------------------------------- gate hysteresis
def _gate_gain_db(level_db, fs=FS, **kw):
    """Steady-state gain the gate applies to noise at `level_db`."""
    g = dsp.Gate(fs, **kw)
    x = np.random.RandomState(0).randn(fs) * (10 ** (level_db / 20)) * np.sqrt(2)
    y = g.process(x[:, None])[:, 0]
    tail = slice(fs // 2, None)  # past the cold-start ramp
    rms = lambda v: np.sqrt(np.mean(v ** 2)) + 1e-30
    return 20 * np.log10(rms(y[tail]) / rms(x[tail]))


@pytest.mark.parametrize("level_db", [-52, -49, -47, -45, -43])
def test_gate_never_boosts_inside_the_hysteresis_window(level_db):
    """REGRESSION: a gate must attenuate or do nothing. It must never add gain.

    While closed, the expander shortfall was measured as `close_db - lvl`,
    which is NEGATIVE for any level between close_db and open_db -- exactly
    the hysteresis window the gate sits in on real material. That made `gr`
    a positive gain: measured +2.95 dB at -45 dB in, on the settings all
    three presets ship (open_db=-42, close_db=-48, ratio=6). Room tone,
    breaths and bleed got AMPLIFIED up to +3 dB, then snapped back to unity
    the moment the gate opened.

    The pre-existing gate test uses open_db=-90/close_db=-95, which holds the
    gate permanently open -- so the only non-trivial region of a gate's
    design was the one region never exercised.
    """
    g = _gate_gain_db(level_db, open_db=-42, close_db=-48, ratio=6)
    assert g <= 0.05, f"gate ADDED {g:+.2f} dB at {level_db} dB in"


def test_gate_honours_its_own_attack_and_release_params():
    """REGRESSION: prepare() hardcoded attack_s=0.001/release_s=0.15 and never
    read self._p, so constructor kwargs were silently discarded (on_param_changed
    only fires on set()). All three presets ask for release_s=0.12 and got 0.15.
    Compressor.prepare does this correctly -- this was a copy-paste omission."""
    g = dsp.Gate(FS, attack_s=0.05, release_s=1.0)
    assert g.det.attack_s == pytest.approx(0.05)
    assert g.det.release_s == pytest.approx(1.0)


# ----------------------------------------------- live param changes / dry mix
def test_limiter_lookahead_change_does_not_corrupt_the_stream():
    """REGRESSION: on_param_changed updated la_n but left self.buf at its old
    length, so the next block read a truncated lookahead window (a numpy slice
    silently returns short rather than raising) and still applied the OLD
    delay, then jumped to the new one on the block after -- splicing audio out
    of the stream. Measured on a clean 220 Hz sine: a sample-to-sample jump 40x
    larger than the signal's own maximum slew, i.e. an audible click, at
    exactly the block where the knob moved (buf stayed 264 while la_n went
    240 -> 720).

    Note this is NOT caught by comparing the settled tail against a limiter
    that was configured that way from the start -- both settle to the same
    place. The corruption is transient, so the test has to look for the splice
    itself.

    Automating a lookahead knob is ordinary plugin use; nothing in the suite
    called set() mid-stream on any module, so this was invisible.
    """
    fs = FS
    f0, amp, blk = 220.0, 0.2, 480
    x = (amp * np.sin(2 * np.pi * f0 * np.arange(fs) / fs))[:, None]

    lim = dsp.Limiter(fs)
    out = []
    for i in range(0, len(x), blk):
        if i == 10 * blk:
            lim.set("lookahead_ms", 15.0)
        out.append(lim.process(x[i:i + blk]))
    y = np.concatenate(out)[:, 0]

    # This signal is well under the ceiling, so the limiter is inactive and the
    # output should be a clean sine. Its slew is bounded by amp*2*pi*f0/fs.
    #
    # EXACTLY ONE discontinuity is allowed, at the moment of the change: raising
    # lookahead lengthens the delay line, so the signal genuinely shifts in
    # time and the waveform cannot be continuous across it. That one step is
    # physics. What this test guards is everything that ISN'T: before the fix
    # there were TWO steps (the old delay applied, then a jump to the new one)
    # and the larger was 40x the clean slew, because the lookahead window was
    # being read short and padded with silence.
    slew = np.abs(np.diff(y))
    clean = amp * 2 * np.pi * f0 / fs
    steps = np.flatnonzero(slew > 2 * clean)

    # Counting steps does NOT distinguish fixed from broken -- verified by
    # running this against the pre-fix source: it also produces exactly one
    # step, so an `assert len(steps) <= 1` passes on the bug. What actually
    # differs is the step's SIZE and WHERE it lands:
    #
    #            steps   max step / clean slew   at sample
    #   pre-fix    1            40.0x              5279  (a block late)
    #   post-fix   1            11.8x              4799  (= the boundary)
    #
    # The residual step is the delay line genuinely changing length; the bug
    # was reading a short window and padding it with silence.
    assert len(steps) == 1, f"{len(steps)} discontinuities at {steps[:5]}"
    assert steps[0] == 10 * blk - 1, (
        f"step at {steps[0]}, expected the block boundary {10 * blk - 1} -- "
        "a late step means the old delay was still being applied")
    assert slew.max() / clean < 15.0, (
        f"step is {slew.max() / clean:.1f}x the clean slew; pre-fix was 40x")
    assert np.all(np.isfinite(y))
    tail = y[12 * blk:]
    assert np.abs(np.diff(tail)).max() < 2 * clean


@pytest.mark.parametrize("mix", [0.25, 0.5, 0.75])
def test_deesser_partial_mix_does_not_notch(mix):
    """REGRESSION: the wet path is an LR4 lowpass+highpass sum, which is
    magnitude-flat but NOT phase-flat (it is an allpass). Blending that
    against the dry signal therefore combs: measured a -70.1 dB null at
    mix=0.5, freq=5500.

    Latent today because every preset uses mix=1.0, but it is an exposed knob
    that destroys the signal. Fixed by applying mix to the GAIN instead of to
    the signal, so the wet path stays a single allpass sum at every mix value.
    """
    m = dsp.DeEsser(FS, freq_hz=5500.0, threshold_db=0.0, mix=mix)
    lo, hi = _response_ripple_db(m, lo=200.0, hi=15000.0)
    assert lo > -1.0, f"notch at mix={mix}: {lo:+.2f} dB"


def test_gate_has_no_step_discontinuity():
    """REGRESSION: a gate must not click.

    Measuring the expander shortfall against open_db removes the +2.95 dB
    boost bug but makes the gain jump from 0 dB to
    -(open_db-close_db)*(1-1/ratio) the instant the gate closes -- 5.03 dB on
    the preset values, per-sample and unsmoothed, i.e. a click on every breath
    and phrase tail. Trading a boost for a click is not a fix, and no test
    caught it because the boost test only samples steady levels.

    Held unity across the hysteresis window instead, so the curve leaves 0 dB
    continuously at close_db. Max step: 5.03 dB -> 0.05 dB.
    """
    fs = FS
    n = 3 * fs
    ramp_db = np.linspace(-30, -60, n)          # slow fade down through both thresholds
    x = np.random.RandomState(0).randn(n) * db2lin_(ramp_db) * np.sqrt(2)
    g = dsp.Gate(fs, open_db=-42, close_db=-48, ratio=6)
    y = g.process(x[:, None])[:, 0]

    gain_db = 20 * np.log10(np.abs(y) / (np.abs(x) + 1e-12) + 1e-12)
    # smooth to reject per-sample noise-ratio jitter, then look for a jump
    k = 256
    sm = np.convolve(gain_db, np.ones(k) / k, mode="valid")
    assert np.max(np.abs(np.diff(sm))) < 0.5, (
        f"gain steps {np.max(np.abs(np.diff(sm))):.2f} dB -- the gate clicks")


def db2lin_(db):
    return 10.0 ** (np.asarray(db) / 20.0)


def test_deesser_zero_mix_nulls():
    """REGRESSION: mix=0 must be a true bypass.

    The wet path is an LR4 lowpass+highpass sum -- flat in magnitude but
    ALLPASS -- so returning it unmodified at mix=0 leaves the phase rotated.
    Measured null against the input: only -6.6 dB. Magnitude-flat, so it is
    inaudible alone, but every other module in this file nulls at mix=0 and
    any parallel dry path around this one would comb.
    """
    x = np.random.RandomState(0).randn(FS) * 0.1
    y = dsp.DeEsser(FS, freq_hz=5500.0, threshold_db=-30.0, mix=0.0).process(x[:, None])[:, 0]
    assert meter.null_test_db(x, y) < -300


def test_params_are_clamped_to_their_spec():
    """REGRESSION: ParamSpec carried lo/hi that nothing enforced, so an
    out-of-range value propagated into buffer sizing and index arithmetic.
    Limiter was the sharp edge -- lookahead_ms past its 20 ms maximum made an
    internal offset negative and raised "zero-size array to reduction
    operation maximum" from inside process()."""
    lim = dsp.Limiter(FS)
    lim.set("lookahead_ms", 30.0)
    assert lim.get("lookahead_ms") == 20.0
    lim.process(np.zeros((1024, 1)))                      # must not raise
    assert dsp.Limiter(FS, lookahead_ms=25.0).get("lookahead_ms") == 20.0
    assert dsp.Limiter(FS, lookahead_ms=0.1).get("lookahead_ms") == 1.0
