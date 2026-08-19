"""
THROW: automatic tempo-synced delay throw on the last word of a line.

Graded the same way as everything else here: exact arithmetic where arithmetic
is claimed (delay time), a bypass null, block-size invariance as core.Module
requires, and detection tested against a signal whose phrase structure is
known by construction rather than eyeballed.
"""
import numpy as np
import pytest

from vox.core import Chain
from vox.dsp import throw as T

FS = 48000


def _phrases(fs, layout, f0=180.0, amp=0.3, seed=0):
    """Build a signal from (duration_s, is_voiced) pairs. Voiced segments get a
    windowed tone so the envelope has real attacks and releases; gaps are
    near-silent. The phrase structure is therefore known exactly, which is what
    lets the detection tests assert counts instead of ranges."""
    rng = np.random.default_rng(seed)
    out = []
    for dur, voiced in layout:
        n = int(dur * fs)
        if voiced:
            t = np.arange(n) / fs
            w = np.hanning(n) if n > 1 else np.ones(n)
            out.append(amp * np.sin(2 * np.pi * f0 * t) * w)
        else:
            out.append(rng.normal(0, 1e-5, n))
    return np.concatenate(out)


# ---------------------------------------------------------------- delay time

def test_note_delay_seconds_is_exact():
    """A quarter note at 120 bpm is 0.5 s. This is arithmetic, not a feel
    parameter -- if it drifts, every throw lands off the grid."""
    assert T.note_delay_seconds(120, "1/4") == pytest.approx(0.5)
    assert T.note_delay_seconds(120, "1/8") == pytest.approx(0.25)
    assert T.note_delay_seconds(120, "1/8D") == pytest.approx(0.375)
    assert T.note_delay_seconds(90, "1/4") == pytest.approx(60.0 / 90.0)
    # the recipes' actual call: dotted 8th at 90 bpm
    assert T.note_delay_seconds(90, "1/8D") == pytest.approx(0.5)


def test_unknown_division_and_bad_bpm_raise():
    with pytest.raises(ValueError):
        T.note_delay_seconds(120, "1/5")
    with pytest.raises(ValueError):
        T.note_delay_seconds(0, "1/4")


def test_delay_places_repeats_on_the_grid():
    """An impulse must come back out at exactly D, 2D, 3D samples -- measured
    on the output, not inferred from the parameter."""
    delay_s = 0.05
    d = T.ThrowDelay(FS, delay_s=delay_s, feedback=0.7, hp_hz=20.0, lp_hz=20000.0)
    x = np.zeros(int(0.5 * FS))
    x[0] = 1.0
    y = d.process(x)
    D = int(round(delay_s * FS))
    peaks = np.flatnonzero(np.abs(y) > 0.05 * np.max(np.abs(y)))
    # group peaks into echoes and take the first sample of each
    firsts = [peaks[0]] + [b for a, b in zip(peaks, peaks[1:]) if b - a > 10]
    for i, p in enumerate(firsts[:3]):
        assert abs(p - (i + 1) * D) <= 2, (i, p, (i + 1) * D)


def test_feedback_decays_and_is_bounded():
    d = T.ThrowDelay(FS, delay_s=0.05, feedback=0.5, hp_hz=20.0, lp_hz=20000.0)
    x = np.zeros(int(1.0 * FS))
    x[0] = 1.0
    y = d.process(x)
    D = int(round(0.05 * FS))
    e1 = np.max(np.abs(y[D - 5:D + 200]))
    e2 = np.max(np.abs(y[2 * D - 5:2 * D + 200]))
    assert e2 < e1, (e1, e2)
    assert np.all(np.isfinite(y))
    assert np.max(np.abs(y)) < 10.0     # cannot run away


def test_feedback_cannot_be_driven_unstable():
    """feedback is clamped at 0.95 internally; asking for 5.0 must not explode.
    An unbounded feedback delay is how you destroy a monitor chain."""
    d = T.ThrowDelay(FS, delay_s=0.01, feedback=5.0, hp_hz=20.0, lp_hz=20000.0)
    x = np.zeros(int(2.0 * FS))
    x[0] = 1.0
    y = d.process(x)
    assert np.all(np.isfinite(y))
    assert np.max(np.abs(y)) < 50.0


def test_repeats_get_darker_not_just_quieter():
    """The filter is inside the feedback loop, so repeat 2 must be darker than
    repeat 1. A filter outside the loop would colour every repeat the same --
    the wrong sound, and the bug this asserts against."""
    d = T.ThrowDelay(FS, delay_s=0.1, feedback=0.8, hp_hz=20.0, lp_hz=2000.0)
    x = np.zeros(int(1.0 * FS))
    x[:64] = np.random.default_rng(0).normal(0, 0.3, 64)   # broadband burst
    y = d.process(x)
    D = int(0.1 * FS)

    def centroid(seg):
        S = np.abs(np.fft.rfft(seg)) ** 2
        f = np.fft.rfftfreq(len(seg), 1 / FS)
        return float((S * f).sum() / (S.sum() + 1e-20))

    c1 = centroid(y[D:D + 2048])
    c2 = centroid(y[3 * D:3 * D + 2048])
    assert c2 < c1, (c1, c2)


# ------------------------------------------------------------ Module contract

def test_block_size_invariance():
    """core.Module: 'correct at block size 1 and at block size 8192 alike'.
    A chunked feedback delay is exactly where this breaks, so assert it."""
    x = np.random.default_rng(1).normal(0, 0.1, 5000)
    ref = T.ThrowDelay(FS, delay_s=0.013, feedback=0.6).process(x)
    for bs in (1, 7, 64, 1024, 8192):
        d = T.ThrowDelay(FS, delay_s=0.013, feedback=0.6)
        out = np.concatenate([d.process(x[i:i + bs]) for i in range(0, len(x), bs)])
        assert np.allclose(out, ref, atol=1e-12), f"block size {bs} diverged"


def test_silent_send_produces_silence():
    """Bypass null: the send is what gates this effect, so a zero send must
    produce digital silence, not a floor."""
    d = T.ThrowDelay(FS, delay_s=0.2, feedback=0.5)
    y = d.process(np.zeros(FS))
    assert np.max(np.abs(y)) == 0.0


def test_reset_clears_the_tail():
    d = T.ThrowDelay(FS, delay_s=0.05, feedback=0.8)
    x = np.zeros(1000)
    x[0] = 1.0
    d.process(x)
    d.reset()
    y = d.process(np.zeros(FS))
    assert np.max(np.abs(y)) == 0.0


def test_reports_zero_latency():
    assert T.ThrowDelay(FS, delay_s=0.3).latency_samples() == 0


def test_works_inside_a_chain_and_keeps_shape():
    x = np.random.default_rng(2).normal(0, 0.1, (2000, 1))
    y = Chain(FS, [T.ThrowDelay(FS, delay_s=0.01)]).process(x)
    assert y.shape == x.shape


# ----------------------------------------------------------------- detection

def test_finds_line_endings_with_gaps():
    """Three lines separated by long gaps -> three throwable endings."""
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.5, False),
                      (0.8, True), (0.5, False), (0.8, True), (0.5, False)])
    got = T.find_phrase_ends(x, FS)
    assert len(got) == 3, [(t["phrase_start"], t["phrase_end"]) for t in got]


def test_does_not_throw_when_the_next_line_comes_straight_back():
    """The musical rule, and the whole reason this beats a hand-drawn spike:
    a throw needs empty space after it or the repeats smear into the next
    line. Two phrases 60 ms apart -> only the LAST one is throwable."""
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.06, False),
                      (0.8, True), (0.8, False)])
    got = T.find_phrase_ends(x, FS)
    assert len(got) == 1, len(got)
    assert got[0]["phrase_end"] > int(1.5 * FS)


def test_ignores_clicks_and_breaths_too_short_to_be_a_line():
    x = _phrases(FS, [(0.1, False), (0.05, True), (0.5, False),
                      (0.8, True), (0.5, False)])
    got = T.find_phrase_ends(x, FS)
    assert len(got) == 1


def test_threshold_is_relative_to_the_takes_own_level():
    """A stem printed 20 dB quieter must yield the same phrase structure --
    the detector adapts to the take instead of assuming an operating level."""
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.5, False), (0.8, True), (0.5, False)])
    loud = T.find_phrase_ends(x, FS)
    quiet = T.find_phrase_ends(x * 10 ** (-20 / 20.0), FS)
    assert len(loud) == len(quiet) == 2
    assert loud[0]["phrase_end"] == quiet[0]["phrase_end"]


def test_throw_word_is_the_end_of_the_phrase_not_the_whole_phrase():
    x = _phrases(FS, [(0.1, False), (1.2, True), (0.6, False)])
    t = T.find_phrase_ends(x, FS, word_s=0.30)[0]
    assert t["word_end"] == t["phrase_end"]
    assert t["word_start"] == pytest.approx(t["phrase_end"] - 0.30 * FS, abs=2)
    assert t["word_start"] > t["phrase_start"]


def test_empty_and_silent_input_are_handled():
    assert T.find_phrase_ends(np.zeros(0), FS) == []
    assert T.find_phrase_ends(np.zeros(FS), FS) == []


# ------------------------------------------------------- grid mode (rap)

def test_grid_mode_finds_a_throw_per_bar_group_with_no_silence_at_all():
    """Grid mode must find throws on continuous audio with NO usable silence
    anywhere, which is the case gap mode cannot serve at all.

    NOTE ON PROVENANCE: this test is built on a SYNTHETIC continuous signal.
    It asserts the mechanism, not that real rap looks like this -- no rap take
    has been measured yet (see find_bar_ends). Do not cite this test as
    evidence about how rap vocals are actually phrased."""
    bpm, bars = 90, 4
    bar_s = (60.0 / bpm) * 4
    dur = bar_s * bars * 3            # three 4-bar groups
    n = int(dur * FS)
    t = np.arange(n) / FS
    # continuous, never stops -- amplitude modulated like syllables but the
    # envelope never drops to silence
    x = 0.3 * np.sin(2 * np.pi * 180 * t) * (0.7 + 0.3 * np.sin(2 * np.pi * 6 * t))

    assert len(T.find_phrase_ends(x, FS)) == 0        # gap mode: helpless
    got = T.find_bar_ends(x, FS, bpm=bpm, bars=bars)
    assert len(got) >= 2, len(got)
    for g in got:
        assert g["word_end"] <= int(g["bar_line_s"] * FS) + 1


def test_grid_throws_land_just_before_the_bar_line():
    bpm, bars = 120, 2
    bar_s = (60.0 / bpm) * 4          # 2.0 s
    n = int(bar_s * bars * 3 * FS)
    t = np.arange(n) / FS
    x = 0.3 * np.sin(2 * np.pi * 200 * t)
    got = T.find_bar_ends(x, FS, bpm=bpm, bars=bars)
    for g in got:
        expected = g["bar_line_s"] * FS
        assert 0 <= expected - g["word_end"] < 0.05 * FS, g


def test_downbeat_offset_shifts_every_throw():
    """A wrong downbeat puts every throw on the wrong syllable, so it must
    actually be honoured rather than silently ignored."""
    n = int(20 * FS)
    t = np.arange(n) / FS
    x = 0.3 * np.sin(2 * np.pi * 200 * t)
    a = T.find_bar_ends(x, FS, bpm=90, bars=4, downbeat_s=0.0)
    b = T.find_bar_ends(x, FS, bpm=90, bars=4, downbeat_s=0.5)
    assert a and b
    assert b[0]["bar_line_s"] - a[0]["bar_line_s"] == pytest.approx(0.5)


def test_grid_mode_skips_bar_lines_with_nothing_sung_into_them():
    """An instrumental bar must not get a throw of silence."""
    bpm = 120
    bar_s = (60.0 / bpm) * 4
    voiced = _phrases(FS, [(bar_s, True)])
    silence = np.zeros(int(bar_s * 3 * FS))
    x = np.concatenate([voiced, silence])
    got = T.find_bar_ends(x, FS, bpm=bpm, bars=1)
    assert all(g["word_end"] <= len(voiced) + 1 for g in got), got


def test_bad_mode_raises():
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.6, False)])
    with pytest.raises(ValueError):
        T.apply_throws(x, FS, bpm=90, mode="whatever")


def test_grid_is_the_default_mode():
    """Hip-hop is the stated use case, so the rap-correct rule is the default
    and the sung rule is opt-in -- not the other way round."""
    n = int(12 * FS)
    t = np.arange(n) / FS
    x = 0.3 * np.sin(2 * np.pi * 180 * t)     # no silence anywhere
    y, info = T.apply_throws(x, FS, bpm=90)
    assert info["mode"] == "grid"
    assert info["n_throws"] >= 1


# --------------------------------------------------------------- ducking

def _key_and_wet(fs, n_s=4.0):
    """A key that is loud for the first half and silent for the second, and a
    steady 'delay return' underneath it. Lets duck depth be measured directly
    in each half."""
    n = int(n_s * fs)
    t = np.arange(n) / fs
    key = 0.4 * np.sin(2 * np.pi * 200 * t)
    key[n // 2:] = 0.0
    wet = 0.2 * np.sin(2 * np.pi * 900 * t)
    return key, wet


def test_duck_reduces_the_return_while_the_key_is_present():
    key, wet = _key_and_wet(FS)
    ducked, measured = T.duck_against(wet, key, FS, duck_db=6.0)
    n = len(key) // 2
    loud_half = np.sqrt(np.mean(ducked[:n] ** 2))
    quiet_half = np.sqrt(np.mean(ducked[n + FS // 2:] ** 2))
    assert loud_half < quiet_half, (loud_half, quiet_half)


@pytest.mark.parametrize("want", [4.0, 6.0, 8.0])
def test_duck_delivers_the_depth_it_was_asked_for(want):
    """duck_db must MEAN something. The open-loop version delivered 4.3 dB for
    a requested 6 on a real rap take (the reduction at the average level is not
    the average reduction, because the key moves and the curve is non-linear).
    It is now closed-loop; assert the delivered value, not the requested one."""
    key, wet = _key_and_wet(FS)
    _, measured = T.duck_against(wet, key, FS, duck_db=want)
    assert abs(measured - want) < 0.5, (want, measured)


def test_duck_depth_is_monotonic():
    key, wet = _key_and_wet(FS)
    got = [T.duck_against(wet, key, FS, duck_db=d)[1] for d in (3.0, 6.0, 9.0)]
    assert got[0] < got[1] < got[2], got


def test_duck_returns_the_return_untouched_when_disabled():
    key, wet = _key_and_wet(FS)
    out, measured = T.duck_against(wet, key, FS, duck_db=0.0)
    assert measured == 0.0
    assert np.allclose(out, wet)


def test_duck_on_a_silent_key_is_a_no_op():
    _, wet = T.duck_against(np.ones(1000) * 0.2, np.zeros(1000), FS)
    assert _[0] == pytest.approx(0.2 * 1.0, abs=0.2)


def test_compressor_external_sidechain_actually_keys_off_the_other_signal():
    """The Compressor change this rests on: with a key supplied, gain
    reduction must follow the KEY, not the input. Assert it directly rather
    than trusting the plumbing."""
    from vox.dsp import Compressor
    n = FS
    quiet = np.full(n, 0.05)
    loud_key = np.full(n, 0.9)
    c1 = Compressor(FS, threshold_db=-20.0, ratio=8.0, attack_s=0.001, release_s=0.01)
    no_key = c1.process(quiet)
    c2 = Compressor(FS, threshold_db=-20.0, ratio=8.0, attack_s=0.001, release_s=0.01)
    with_key = c2.process(quiet, key=loud_key)
    # keyed by a loud signal, the quiet input gets pushed down hard;
    # unkeyed, a quiet input below threshold is barely touched
    assert np.mean(np.abs(with_key[-1000:])) < np.mean(np.abs(no_key[-1000:])) * 0.5


def test_ducked_throw_is_quieter_over_the_next_line_than_an_undicked_one():
    """The reason ducking matters for rap: when a repeat overlaps the next
    line it must get out of the way instead of fighting it."""
    n = int(12 * FS)
    t = np.arange(n) / FS
    x = 0.3 * np.sin(2 * np.pi * 180 * t)          # continuous, never stops
    plain, _ = T.apply_throws(x, FS, bpm=90, bars=2, duck_db=0.0)
    duckd, info = T.apply_throws(x, FS, bpm=90, bars=2, duck_db=6.0)
    assert info["duck_db_measured"] > 2.0
    # the added (wet) energy over the continuous vocal must be smaller
    assert np.sqrt(np.mean((duckd - x) ** 2)) < np.sqrt(np.mean((plain - x) ** 2))


def test_ducking_is_on_by_default():
    n = int(12 * FS)
    t = np.arange(n) / FS
    x = 0.3 * np.sin(2 * np.pi * 180 * t)
    _, info = T.apply_throws(x, FS, bpm=90)
    assert info["duck_db_requested"] > 0


# ------------------------------------------------------------------ envelope

def test_envelope_is_zero_outside_throws_and_one_inside():
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.6, False)])
    throws = T.find_phrase_ends(x, FS)
    g = T.throw_envelope(len(x), FS, throws)
    assert g.min() == 0.0 and g.max() == pytest.approx(1.0)
    assert g[0] == 0.0                       # dry before the line
    mid = throws[0]["word_start"] + int(0.15 * FS)
    assert g[mid] == pytest.approx(1.0)      # open on the throw word


def test_envelope_has_no_instantaneous_jumps():
    """A rectangular send gate clicks. Bound the per-sample slew."""
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.6, False)])
    g = T.throw_envelope(len(x), FS, T.find_phrase_ends(x, FS), ramp_s=0.02)
    assert np.max(np.abs(np.diff(g))) < 1.0 / (0.02 * FS) * 1.5


def test_no_throws_means_a_flat_zero_envelope():
    g = T.throw_envelope(1000, FS, [])
    assert np.all(g == 0.0)


# ------------------------------------------------------------------ end to end

def test_apply_throws_leaves_the_dry_signal_intact_before_the_first_throw():
    """The dry path is never touched -- this is a send. Everything before the
    first throw word must be bit-identical to the input."""
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.6, False), (0.8, True), (0.6, False)])
    y, info = T.apply_throws(x, FS, bpm=90, division="1/8D", mode="gap")
    first = info["throws"][0]["word_start"]
    assert np.allclose(y[:first], x[:first], atol=1e-12)
    assert info["n_throws"] == 2
    assert info["delay_s"] == pytest.approx(0.5)


def test_apply_throws_puts_the_repeat_one_delay_after_the_thrown_word():
    """Energy must appear in the gap at exactly one delay time after the throw
    word -- not merely 'somewhere after the line'. The first version of this
    test measured a 0.167 s window while the repeat was 0.5 s away, and passed
    vacuously against a silent buffer; assert the location, not just presence."""
    x = _phrases(FS, [(0.1, False), (0.8, True), (1.2, False)])
    y, info = T.apply_throws(x, FS, bpm=120, division="1/4", feedback=0.5, mode="gap")
    delay = int(info["delay_s"] * FS)
    word = info["throws"][0]["word_start"]
    echo = word + delay
    win = slice(echo, echo + int(0.2 * FS))
    dry_there = np.sqrt(np.mean(x[win] ** 2))
    wet_there = np.sqrt(np.mean(y[win] ** 2))
    assert wet_there > dry_there * 10, (dry_there, wet_there)
    # and the gap immediately after the line, BEFORE the repeat, stays dry
    quiet = slice(info["throws"][0]["phrase_end"] + 100, echo - int(0.05 * FS))
    assert np.allclose(y[quiet], x[quiet], atol=1e-9)


def test_apply_throws_is_a_no_op_when_nothing_is_throwable():
    """Silence in, silence out -- and specifically NOT a delay tail of noise."""
    x = np.random.default_rng(3).normal(0, 1e-6, FS)
    y, info = T.apply_throws(x, FS, bpm=90, mode="gap")
    assert info["n_throws"] == 0
    assert np.allclose(y, x, atol=1e-12)


def test_stereo_in_stereo_out():
    x = _phrases(FS, [(0.1, False), (0.8, True), (0.6, False)])
    st = np.stack([x, x], axis=1)
    y, _ = T.apply_throws(st, FS, bpm=90, mode="gap")
    assert y.shape == st.shape


def test_caller_can_supply_its_own_throw_points():
    """Detection is a convenience, not a lock-in: the owner must be able to
    override which word gets thrown."""
    x = _phrases(FS, [(0.1, False), (1.0, True), (0.8, False)])
    manual = [{"phrase_start": 0, "phrase_end": int(0.6 * FS),
               "word_start": int(0.4 * FS), "word_end": int(0.6 * FS), "gap_s": 1.0}]
    y, info = T.apply_throws(x, FS, bpm=90, throws=manual)
    assert info["n_throws"] == 1
    assert info["throws"] is manual
