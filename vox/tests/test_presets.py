"""Preset sanity checks: does it run, does it null-safe, does the compressor
land in the documented gain-reduction range. Not a sound-quality judgment --
that's the owner's ear, per the "lighter touch" bar (DECISIONS.md 2026-08-18)."""
import numpy as np

from vox import presets, meter

FS = 48000


def _loud_phrase(dbfs=-6.0, dur=1.0, fs=FS):
    """Program-like level (not a pure tone) so the 7:1 comp actually engages."""
    rng = np.random.RandomState(0)
    t = np.arange(int(dur * fs)) / fs
    tone = np.sin(2 * np.pi * 220 * t) + 0.5 * np.sin(2 * np.pi
        * 440 * t)
    x = tone * (10 ** (dbfs / 20)) + rng.randn(len(t)) * 1e-4
    return x[:, None]


def test_eminem_chain_runs_and_stays_finite():
    x = _loud_phrase()
    y = presets.build_eminem_chain(FS).process(x)
    assert y.shape == x.shape
    assert np.all(np.isfinite(y))


def test_eminem_chain_true_peak_under_ceiling():
    x = _loud_phrase(dbfs=-1.0)
    y = presets.build_eminem_chain(FS).process(x)[:, 0]
    assert meter.true_peak_db(y, FS) <= -1.0 + 0.15  # limiter ceiling + tolerance


def _peak_gain_reduction_db(chain, x, fs=FS):
    """GR the chain's compressor actually applies at program level. Measured
    off the compressor's own detector + static curve, so it isolates the comp
    from the limiter and makeup gain sitting around it."""
    from vox import dsp
    comp = next(m for m in chain.modules if m.name == "compressor")
    mono = x.mean(axis=1) if x.ndim > 1 else x
    det = dsp.Detector(fs, mode="rms", rms_window_s=0.006,
                       attack_s=comp.get("attack_s"), release_s=comp.get("release_s"))
    env = det.process(mono)
    return -min(comp._gain_curve_db(v) for v in env)


def test_eminem_compressor_hits_documented_gain_reduction():
    """Research doc: 7:1, catching 3-7 dB on the loudest peaks.

    REGRESSION: the first version of this preset copied the HARDWARE threshold
    ("~0 dB") straight into a digital 0 dBFS threshold. Measured on the real
    reference acapella that engaged on 0.0% of the file -- the chain's defining
    stage did nothing. The bound here must be tight enough to fail that."""
    x = _loud_phrase()
    prog = presets.program_level_db(x, FS)
    gr = _peak_gain_reduction_db(presets.build_eminem_chain(FS, program_db=prog), x)
    assert 3.0 <= gr <= 7.0, f"GR {gr:.2f} dB outside documented 3-7 dB"


def test_jayz_compressor_is_lighter_than_eminem():
    """'Anti-compression' philosophy -- must be measurably gentler than the
    7:1 leveling chain on identical material, not just nominally different."""
    x = _loud_phrase()
    prog = presets.program_level_db(x, FS)
    gr_jayz = _peak_gain_reduction_db(presets.build_jayz_chain(FS, program_db=prog), x)
    gr_eminem = _peak_gain_reduction_db(presets.build_eminem_chain(FS, program_db=prog), x)
    assert 0.5 <= gr_jayz <= 3.5, f"GR {gr_jayz:.2f} dB not a light-touch comp"
    assert gr_jayz < gr_eminem - 1.5


def test_threshold_derivation_produces_target_gain_reduction():
    """The math behind both presets: _threshold_for must invert the
    compressor's own static curve, or every preset threshold is a guess."""
    from vox import dsp
    for ratio, target in [(7.0, 5.0), (2.5, 2.0), (4.0, 3.0)]:
        prog = -14.0
        thr = presets._threshold_for(prog, ratio, target)
        comp = dsp.Compressor(FS, threshold_db=thr, ratio=ratio, knee_db=0.0,
                              makeup_db=0.0, mix=1.0)
        assert abs(-comp._gain_curve_db(prog) - target) < 0.01


def test_jayz_chain_runs_and_stays_finite():
    x = _loud_phrase()
    y = presets.build_jayz_chain(FS).process(x)
    assert y.shape == x.shape
    assert np.all(np.isfinite(y))


def test_jayz_chain_true_peak_under_ceiling():
    x = _loud_phrase(dbfs=-1.0)
    y = presets.build_jayz_chain(FS).process(x)[:, 0]
    assert meter.true_peak_db(y, FS) <= -1.0 + 0.15  # limiter ceiling + tolerance


def test_jayz_eq_bands_are_cuts_not_boosts():
    """Research doc: 'subtractive EQ first', 'does NOT scoop mid-range' --
    mechanically, every non-HPF band should be a cut, never a boost."""
    chain = presets.build_jayz_chain(FS)
    eq = next(m for m in chain.modules if m.name == "eq")
    bell_bands = [b for b in eq.bands if b.kind != "highpass"]
    assert bell_bands, "expected at least one corrective bell band"
    assert all(b.gain_db <= 0.0 for b in bell_bands)


def test_tupac_chain_runs_and_stays_finite():
    x = _loud_phrase()
    y = presets.build_tupac_chain(FS).process(x)
    assert y.shape == x.shape
    assert np.all(np.isfinite(y))


def test_tupac_chain_true_peak_under_ceiling():
    x = _loud_phrase(dbfs=-1.0)
    y = presets.build_tupac_chain(FS).process(x)[:, 0]
    assert meter.true_peak_db(y, FS) <= -1.0 + 0.15


def test_tupac_compressor_is_a_light_console_comp():
    """Doc 07 section 3: least processed of the three -- console comp only.
    Must sit between Jay-Z's anti-compression and Eminem's 7:1 leveling."""
    x = _loud_phrase()
    prog = presets.program_level_db(x, FS)
    gr = _peak_gain_reduction_db(presets.build_tupac_chain(FS, program_db=prog), x)
    gr_eminem = _peak_gain_reduction_db(presets.build_eminem_chain(FS, program_db=prog), x)
    assert 2.0 <= gr <= 4.5, f"GR {gr:.2f} dB not a light console comp"
    assert gr < gr_eminem


def test_tupac_stack_is_on_and_widens_the_image():
    """The doubler is PRINTED on this preset, not a send at mix=0 -- and its
    whole point is stereo width, so L and R must stop being identical."""
    from vox import dsp
    x = np.repeat(_loud_phrase(), 2, axis=1)
    chain = presets.build_tupac_chain(FS)
    stack = next(m for m in chain.modules if m.name == "stack")
    assert stack.get("mix") > 0.0
    y = chain.process(x)
    assert np.max(np.abs(y[:, 0] - y[:, 1])) > 1e-3
    assert isinstance(stack, dsp.Stack)


def test_presets_deess_measurably_on_material_that_has_esses():
    """REGRESSION: every preset carried a flat -22 dB de-esser threshold, which
    measured 0.03 dB of sibilance reduction on the reference acapella -- the
    band never gets that loud. Threshold now comes from the stem's own
    sibilance level, so the stage has to actually do something. Measured on
    the de-esser stage alone; downstream saturation adds its own HF."""
    from vox import dsp
    fs = FS
    t = np.arange(2 * fs) / fs
    body = 0.3 * np.sin(2 * np.pi * 300 * t)
    ess = 0.3 * np.sin(2 * np.pi * 8000 * t) * (t % 0.5 < 0.02)  # 4% duty, like real esses
    x = (body + ess)[:, None]
    sib = presets.sibilance_level_db(x, fs)

    def hf_peak_db(sig_):
        """Loudest HF frames -- a de-esser is supposed to move those and leave
        the average alone, so measuring the mean would hide the whole effect."""
        s = sig_[:, 0]
        for _ in range(2):
            s = dsp.Band(fs, "highpass", 7000.0, q=0.707).process(s)
        n = 512
        f = s[:len(s) // n * n].reshape(-1, n)
        return 20 * np.log10(np.percentile(np.sqrt((f ** 2).mean(1)), 99) + 1e-12)

    for name, build in presets.PRESETS.items():
        chain = build(fs, program_db=presets.program_level_db(x, fs), sibilance_db=sib)
        de = next(m for m in chain.modules if m.name == "deesser")
        drop = hf_peak_db(de.process(x)) - hf_peak_db(x)
        assert drop < -1.5, f"{name} de-esser did nothing (peak HF {drop:+.2f} dB)"
