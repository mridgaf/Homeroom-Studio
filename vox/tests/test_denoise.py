"""
Coverage for engines/denoise_dfn.py -- previously untested. Slow (loads a
real pretrained model); keep this file's test count small.
"""
import numpy as np
import pytest

FS = 48000


def test_denoise_runs_and_reduces_noise_floor():
    """Sanity + the one thing this stage is actually good at, per
    docs/05_FINDINGS.md: measured ~25 dB noise-floor reduction in a silent
    region on the synthetic bench. Confirm it still does that."""
    from vox.testsignal import make_testbench
    from vox.engines.denoise_dfn import denoise

    dirty, _truth = make_testbench(fs=FS, seed=0, voice="male")
    # vad_gated=False on purpose: this measures the MODEL's raw noise-floor
    # capability. The shipping path is gated (see the VAD tests below), which
    # deliberately declines to denoise where the mask says a voice is present.
    r = denoise(dirty, FS, blend=1.0, vad_gated=False)
    assert r.audio.shape[0] > 0
    assert r.model_sr == 48000

    tail = dirty[int(3.0 * FS):]
    tail_y = r.audio[int(3.0 * FS): min(len(r.audio), int(3.28 * FS))]
    n = min(len(tail), len(tail_y))
    before = 20 * np.log10(np.sqrt(np.mean(tail[:n] ** 2)) + 1e-12)
    after = 20 * np.log10(np.sqrt(np.mean(tail_y[:n] ** 2)) + 1e-12)
    assert before - after > 15.0, f"only {before - after:.1f} dB reduction"


def test_denoise_does_not_destroy_sustained_dry_tone():
    """WAS xfail(strict) until 2026-08-19. Its own reason listed three possible
    fixes -- a sung-material model, a VAD-gated blend, or acceptance as an
    opt-in aggressive mode -- and the second one is now implemented and on by
    default, so this passes for real rather than by a loosened threshold.

    The underlying limitation is unchanged and still true: DeepFilterNet3 is
    trained on speech/VoIP, not singing, and at full wet it suppresses a
    sustained tone by 18.5-21.5 dB (assert this yourself with vad_gated=False). What
    changed is that the model is no longer allowed to touch the parts of a take
    where that limitation bites. See test_vad_gate_protects_a_sustained_tone.
    """
    from vox.engines.denoise_dfn import denoise

    t = np.arange(int(3 * FS)) / FS
    tone = 0.3 * np.sin(2 * np.pi * 220 * t)
    r = denoise(tone, FS, blend=1.0)
    n = min(len(tone), len(r.audio))
    before = 20 * np.log10(np.sqrt(np.mean(tone[FS:n] ** 2)) + 1e-12)
    after = 20 * np.log10(np.sqrt(np.mean(r.audio[FS:n] ** 2)) + 1e-12)
    assert before - after < 10.0, f"suppressed a dry tone by {before - after:.1f} dB"


# ------------------------------------------------------------------ VAD gate
def test_vad_gate_protects_a_sustained_tone():
    """The whole reason this stage was OFF: DeepFilterNet3 is a speech model
    and flattens sustained non-speech-like content (18.5-21.5 dB at full wet on a
    pure tone, docs/05_FINDINGS.md). Gated, a held note must come back
    untouched, because a take with no silence has no gaps to denoise.

    This is also the regression guard for the first version of the mask, which
    used the classic "noise floor + margin" rule alone. On a signal with no
    silence the 10th percentile IS the content, so the threshold landed above
    the tone, the whole performance read as "silence", and the tone was handed
    to the model anyway -- measured -18.4 dB, i.e. gating had changed nothing.
    """
    from vox.engines.denoise_dfn import denoise
    fs = FS
    tone = 0.3 * np.sin(2 * np.pi * 440 * np.arange(3 * fs) / fs)
    y = denoise(tone, fs, blend=1.0, vad_gated=True).audio[:len(tone)]
    def rms_db(v):
        return 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-30)
    assert abs(rms_db(y) - rms_db(tone)) < 0.5, "gated denoise damaged a sustained tone"


def test_vad_gate_still_removes_the_noise_floor():
    """Protecting content is only worth something if the stage still does its
    job in the gaps.

    Uses a constructed take -- voice, then a long noise-only gap -- rather than
    the test bench, whose gaps are ~0.28 s and dominated by the preceding
    phrase's tail (the mask is still releasing through them, which is correct
    behaviour and makes the bench a bad instrument for this particular
    question).

    On real material (`eminem lose vocal.wav`, 20 s), measured over the frames
    the mask calls silent: noise floor -44.1 -> -48.3 dB, and IDENTICALLY so
    gated or ungated -- which is the actual point. Gating costs nothing where
    the model is useful. What it changes is the voiced region: damage goes
    from -1.30 dB ungated to +0.01 dB gated.

    State the frame selection with any figure like this. An earlier version of
    this docstring claimed "~8 dB", which came from a different choice of
    "quiet region" and did not reproduce; measuring p10 of a 20 ms RMS
    envelope instead gives 22.8 dB. The dB number is an artifact of the
    window, the gated-vs-ungated comparison is not.
    """
    from vox.testsignal import make_testbench
    from vox.engines.denoise_dfn import denoise

    voiced, _truth = make_testbench(fs=FS, seed=0, voice="male")
    voiced = voiced[:int(2.0 * FS)]
    rng = np.random.default_rng(0)
    gap = rng.standard_normal(int(1.5 * FS)) * 10 ** (-45 / 20)
    x = np.concatenate([voiced, gap])

    def rms_db(v):
        return 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-30)

    tail = slice(int(2.5 * FS), len(x))          # well clear of the release
    head = slice(int(0.2 * FS), int(1.8 * FS))
    y = denoise(x, FS, blend=1.0, vad_gated=True).audio[:len(x)]
    ungated = denoise(x, FS, blend=1.0, vad_gated=False).audio[:len(x)]

    assert rms_db(y[tail]) < rms_db(x[tail]) - 6.0, "gated denoise did nothing in the gap"

    # The head bar has to be tight enough that the GATE is what passes it.
    # At 1.0 dB the ungated path also passed (0.54 dB), so the assertion held
    # with the gate disabled and guarded nothing. Gated measures ~0.23 dB.
    damage_gated = abs(rms_db(y[head]) - rms_db(x[head]))
    damage_ungated = abs(rms_db(ungated[head]) - rms_db(x[head]))
    assert damage_gated < 0.25, f"gated denoise damaged the voice by {damage_gated:.2f} dB"
    assert damage_gated < damage_ungated, (
        f"gating changed nothing: {damage_gated:.2f} dB gated vs "
        f"{damage_ungated:.2f} dB ungated")


def test_vad_mask_is_a_mask():
    from vox.engines.denoise_dfn import voice_activity_mask
    from vox.testsignal import make_testbench
    dirty, _ = make_testbench(fs=FS, seed=0, voice="male")
    m = voice_activity_mask(dirty, FS)
    assert m.shape == dirty.shape
    assert m.min() >= 0.0 and m.max() <= 1.0
    assert 0.0 < m.mean() < 1.0, "mask is stuck fully open or fully closed"
