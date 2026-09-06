"""The chord performance grammar (build 2026-09-05).

The layer this covers had NO test at all before today — `arp_riff`, its
only rhythm generator, was untested, and the nine legends with no
`chord_rhythm` key were invisible to the suite.
"""
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import chord_rhythm                                          # noqa: E402
from chord_rhythm import DEFAULT, FIGURES, gen_figure, spec_for  # noqa: E402


# ---------------------------------------------------------------- opt-in

def test_absent_key_means_no_grammar():
    """The whole point of the opt-in: twenty-two identities must be able
    to see this module and get nothing from it."""
    assert spec_for({}) is None
    assert spec_for({"chord_grammar": False}) is None


def test_true_means_the_house_default():
    assert spec_for({"chord_grammar": True}) == DEFAULT


def test_a_dict_overrides_only_what_it_names():
    spec = spec_for({"chord_grammar": {"hits": [1, 1]}})
    assert spec["hits"] == [1, 1]
    assert spec["w"] == DEFAULT["w"]          # untouched keys still there


# ---------------------------------------------------------------- figures

@pytest.mark.parametrize("figure", FIGURES)
def test_every_figure_writes_legal_bars(figure):
    spec = dict(DEFAULT, figures=[[figure, 1]])
    fig, bars, shape = gen_figure(spec, random.Random(7), 4)
    assert fig == figure
    assert len(bars) == 4
    for bar in bars:
        assert len(bar) == 16
        assert set(bar) <= set("Xxo.-")
    assert any(ch != "-" for bar in bars for ch in bar)
    assert (shape in chord_rhythm.SHAPES) == (figure == "arp")


def test_stab_respects_its_hit_count():
    spec = dict(DEFAULT, figures=[["stab", 1]], hits=[2, 3], ghost_p=0.0)
    for seed in range(25):
        _, bars, _ = gen_figure(spec, random.Random(seed), 1)
        assert 2 <= sum(ch != "-" for ch in bars[0]) <= 3


def test_stab_never_writes_two_adjacent_hits():
    """Two hits a 16th apart read as a flam, not as two stabs — the same
    rejection gen_kick makes on the drum side."""
    spec = dict(DEFAULT, figures=[["stab", 1]])
    for seed in range(40):
        _, bars, _ = gen_figure(spec, random.Random(seed), 1)
        cells = [i for i, ch in enumerate(bars[0]) if ch != "-"]
        assert all(b - a > 1 for a, b in zip(cells, cells[1:]))


def test_comp_stays_out_of_the_drums_way():
    """`comp` is chords ANSWERING the kit. Given drums that fill every
    beat, it should land off them far more often than on."""
    busy = {"kick": ["X---X---X---X---"], "snare": ["----X-------X---"]}
    spec = dict(DEFAULT, figures=[["comp", 1]])
    on = off = 0
    for seed in range(60):
        _, bars, _ = gen_figure(spec, random.Random(seed), 1, busy=busy)
        for i, ch in enumerate(bars[0]):
            if ch == "-":
                continue
            on += i in (0, 4, 8, 12)
            off += i not in (0, 4, 8, 12)
    assert off > on


def test_pad_still_lands_the_chord_then_breathes():
    """The nine held-pad legends' figure: bar 1 still starts the block
    (so a pad is never late), and the re-attacks are the new part."""
    spec = dict(DEFAULT, figures=[["pad", 1]], swells=[2, 2])
    _, bars, _ = gen_figure(spec, random.Random(3), 4)
    assert bars[0][0] == "X"
    assert sum(ch == "o" for bar in bars for ch in bar) >= 4


def test_arp_has_rests_which_the_old_fixed_figure_never_did():
    spec = dict(DEFAULT, figures=[["arp", 1]], rest_p=0.5)
    _, bars, _ = gen_figure(spec, random.Random(1), 4)
    assert any(ch == "-" for bar in bars for ch in bar)


def test_bars_vary_within_one_slot():
    """A four-bar slot used to be the same held block four times over."""
    spec = dict(DEFAULT, figures=[["stab", 1]], rest_p=0.6)
    seen = set()
    for seed in range(20):
        _, bars, _ = gen_figure(spec, random.Random(seed), 4)
        seen.add(len(set(bars)))
    assert max(seen) > 1


# ---------------------------------------------------------------- seeding

def test_same_seed_same_figure():
    a = gen_figure(DEFAULT, random.Random(11), 4)
    b = gen_figure(DEFAULT, random.Random(11), 4)
    assert a == b


def test_different_beats_get_different_figures():
    got = {gen_figure(DEFAULT, random.Random(s), 4)[1][0] for s in range(30)}
    assert len(got) > 5


# ---------------------------------------------------------------- render

def _render(figure, **kw):
    spec = dict(DEFAULT, figures=[[figure, 1]], **kw)
    fig, bars, shape = gen_figure(spec, random.Random(5), 2)
    return chord_rhythm.render_figure(
        bars, 2.0, 90, [60, 64, 67],
        lambda nt, sd: np.ones(int(sd * chord_rhythm.chord_synth.SR)) * 0.1,
        lambda ns, sd: np.ones(int(sd * chord_rhythm.chord_synth.SR)) * 0.1,
        figure=fig, shape=shape, spec=spec)


@pytest.mark.parametrize("figure", FIGURES)
def test_render_is_loop_safe_and_never_clips(figure):
    out = _render(figure)
    assert len(out) == int(2.0 * chord_rhythm.chord_synth.SR)
    assert np.max(np.abs(out)) <= chord_rhythm.chord_synth.PEAK_CEILING
    assert np.isfinite(out).all()
    assert abs(out[0]) < 1e-6 and abs(out[-1]) < 1e-6   # ramped edges


def test_an_unvoiceable_step_is_left_silent_never_synthesized():
    """chord_synth's hard rule (owner 2026-07-23) reaches in here too: a
    note his library can't play is silence, not an oscillator."""
    spec = dict(DEFAULT, figures=[["stab", 1]])
    fig, bars, shape = gen_figure(spec, random.Random(5), 2)
    out = chord_rhythm.render_figure(
        bars, 2.0, 90, [60, 64, 67], lambda nt, sd: None,
        lambda ns, sd: None, figure=fig, shape=shape, spec=spec)
    assert not np.any(out)


def test_levels_come_from_the_written_character_only():
    """OWNER RULE 2026-08-03 — no random level wobble. Two renders of the
    same written bars must be identical in level."""
    assert np.allclose(_render("stab", feel=[0, 0, 50]),
                       _render("stab", feel=[0, 0, 50]))


def test_a_chopped_loop_can_drive_a_figure():
    """Owner call 2026-09-05: a loop is a finished melody, so the grammar
    CHOPS it rather than playing it. beat_machine's loop branch feeds
    chop_onsets' clips in as the render callbacks; this is that shape.
    Swish Beatz, the first identity on the grammar, has no loop in his
    chord_source, so nothing else exercises this path."""
    import melodic_loops
    sr = chord_rhythm.chord_synth.SR
    x = np.zeros(int(2 * sr))
    for k in range(4):                      # four clear attacks
        s0, n = int(k * 0.5 * sr), int(0.2 * sr)
        x[s0:s0 + n] = (np.sin(2 * np.pi * 220 * np.arange(n) / sr)
                        * np.linspace(1, 0, n))
    clips = melodic_loops.chop_onsets(x, sr)
    assert len(clips) > 1

    def clip(i, sd):
        return clips[abs(int(i)) % len(clips)][:max(int(sd * sr), 1)]

    spec = dict(DEFAULT, figures=[["stab", 1]])
    fig, bars, shape = gen_figure(spec, random.Random(2), 4)
    out = chord_rhythm.render_figure(
        bars, 2.0, 95, [60, 63, 67], clip, lambda ns, sd: clip(ns[0], sd),
        figure=fig, shape=shape, spec=spec)
    assert np.any(out)
    assert np.max(np.abs(out)) <= chord_rhythm.chord_synth.PEAK_CEILING
