"""The ladder's whole value is that stage N differs from stage N-1.

If a bypass is wired wrong the tool happily writes eight identical files, the
owner hears one sound eight times, and concludes the chain does nothing. That
failure is silent -- no exception, no NaN, correct file sizes -- so it needs
its own test.
"""
import sys
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import render_ladder  # noqa: E402

FS = 48000


def _phrase(dbfs=-6.0, dur=1.5, fs=FS):
    """Sibilant, loud, and gappy, so every stage in the chain has something to
    act on: gate needs the gap, de-esser needs the HF, comp needs the level."""
    rng = np.random.RandomState(0)
    t = np.arange(int(dur * fs)) / fs
    voiced = np.sin(2 * np.pi * 180 * t) + 0.5 * np.sin(2 * np.pi * 900 * t)
    ess = rng.randn(len(t)) * 0.3
    env = ((t % 0.5) < 0.35).astype(float)          # phrases with gaps
    x = (voiced + ess * ((t % 0.5) > 0.25)) * env * (10 ** (dbfs / 20))
    return x[:, None] + rng.randn(len(t), 1) * 1e-5


def test_every_ladder_stage_changes_the_sound():
    stages = list(render_ladder.ladder(_phrase(), FS))
    assert len(stages) >= 7, "chain lost modules"
    for (_, prev_name, prev), (_, name, cur) in zip(stages, stages[1:]):
        d = 20 * np.log10(np.sqrt(np.mean((cur - prev) ** 2)) + 1e-20)
        assert d > -80, f"stage '{name}' is identical to '{prev_name}' ({d:.1f} dB)"


def test_ladder_is_cumulative_not_solo():
    """The last stage must equal the full chain. If `bypassed` were inverted
    each file would be one module in isolation, which sounds plausible and is
    completely wrong."""
    from vox import presets
    x = _phrase()
    a = presets.analyse(x, FS)
    full = presets.build_eminem_chain(FS, **a).process(x)
    last = list(render_ladder.ladder(x, FS))[-1][2]
    assert np.allclose(last, full, atol=1e-9)


def test_check_rejects_broken_renders():
    ok = _phrase() * 0.3
    render_ladder.check(ok, "ok")
    for bad, why in ((np.zeros_like(ok), "silence"),
                     (ok * 100, "clipping"),
                     (ok * np.nan, "NaN")):
        with pytest.raises(AssertionError):
            render_ladder.check(bad, why)


def test_written_files_all_carry_the_same_monitoring_trim(tmp_path, monkeypatch):
    """The trim must be ONE number on every file. Per-file normalising would
    still produce eight playable renders, still pass every other test here, and
    still destroy the only thing the ladder is for -- hearing what each stage
    does to the LEVEL. It also has to match the Clear renders, or the owner
    A/Bs a 4.5 dB level difference and picks the louder one every time.
    """
    src = tmp_path / "src.wav"
    sf.write(src, _phrase()[:, [0, 0]], FS, subtype="PCM_24")
    monkeypatch.setattr(render_ladder, "OUT_DIR", tmp_path / "out")
    render_ladder.main([str(src)])

    x, fs = sf.read(src, always_2d=True)
    stages = list(render_ladder.ladder(x, fs))
    g = 10.0 ** (render_ladder.MONITOR_TRIM_DB / 20.0)
    for i, name, y in stages:
        written, _ = sf.read(tmp_path / "out" / f"{i:02d} {name}.wav", always_2d=True)
        assert np.allclose(written, y * g, atol=1e-6), f"'{name}' not at the shared trim"


def test_clear_renders_use_the_same_trim_as_the_ladder():
    """Same constant, one definition. Two independent copies is how the ladder
    and the Clear set drifted 4.5 dB apart the first time."""
    import render_clear
    assert render_clear.MONITOR_TRIM_DB is render_ladder.MONITOR_TRIM_DB
