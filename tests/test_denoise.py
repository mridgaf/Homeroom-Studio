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
    r = denoise(dirty, FS, blend=1.0)
    assert r.audio.shape[0] > 0
    assert r.model_sr == 48000

    tail = dirty[int(3.0 * FS):]
    tail_y = r.audio[int(3.0 * FS): min(len(r.audio), int(3.28 * FS))]
    n = min(len(tail), len(tail_y))
    before = 20 * np.log10(np.sqrt(np.mean(tail[:n] ** 2)) + 1e-12)
    after = 20 * np.log10(np.sqrt(np.mean(tail_y[:n] ** 2)) + 1e-12)
    assert before - after > 15.0, f"only {before - after:.1f} dB reduction"


@pytest.mark.xfail(
    reason="KNOWN LIMITATION, see docs/06_REAL_STEM_FINDINGS.md: DeepFilterNet3 "
           "is trained on speech/VoIP, not singing. A pure sustained tone "
           "(stand-in for a held vowel) is suppressed ~59 dB at full wet -- it "
           "doesn't recognize sustained non-speech-like content as signal. "
           "This is why denoise defaults to blend=0.0 in chain_demo.py. Not "
           "fixable by parameter tuning; needs either a sung-material model, "
           "a VAD-gated blend (only denoise between phrases), or acceptance "
           "as an opt-in aggressive mode the user A/Bs themselves.",
    strict=True,
)
def test_denoise_does_not_destroy_sustained_dry_tone():
    from vox.engines.denoise_dfn import denoise

    t = np.arange(int(3 * FS)) / FS
    tone = 0.3 * np.sin(2 * np.pi * 220 * t)
    r = denoise(tone, FS, blend=1.0)
    n = min(len(tone), len(r.audio))
    before = 20 * np.log10(np.sqrt(np.mean(tone[FS:n] ** 2)) + 1e-12)
    after = 20 * np.log10(np.sqrt(np.mean(r.audio[FS:n] ** 2)) + 1e-12)
    assert before - after < 10.0, f"suppressed a dry tone by {before - after:.1f} dB"
