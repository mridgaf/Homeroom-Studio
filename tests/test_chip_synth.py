"""chip_synth: does it actually model the hardware, or just make bleeps?

Each test pins a real property of the chip rather than a waveform
snapshot — duty cycle, the triangle's 4-bit stepping, the LFSR, and the
Atari's out-of-tune divider. If one of these breaks the sound stops
being period-correct, which is the whole point of the module.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "tools"))

import numpy as np                                          # noqa: E402
import pytest                                               # noqa: E402

import chip_synth                                           # noqa: E402
from chip_synth import (DUTIES, atari_detune_cents,  # noqa: E402
                        chip_chord, chip_hat, chip_kick, chip_note,
                        chip_snare, midi_to_hz, noise, pulse, sweep,
                        triangle)
from chord_synth import PEAK_CEILING                        # noqa: E402
from make_drum_loops import SR                              # noqa: E402


@pytest.mark.parametrize("duty", DUTIES)
def test_pulse_duty_cycle_is_what_was_asked_for(duty):
    # duty IS the NES timbre control, so it has to be accurate
    x = pulse(440.0, 0.5, duty=duty)
    high = float(np.mean(x > 0))
    assert abs(high - duty) < 0.02, "duty %.3f came out %.3f" % (duty, high)


def test_pulse_is_only_two_values():
    x = pulse(440.0, 0.2, 0.5)
    assert set(np.unique(np.round(x, 6))) == {-1.0, 1.0}


def test_pulse_frequency_is_right():
    # count rising edges over a known duration
    hz, dur = 200.0, 1.0
    x = pulse(hz, dur, 0.5)
    rises = int(np.sum((x[1:] > 0) & (x[:-1] <= 0)))
    assert abs(rises - hz * dur) <= 2


def test_triangle_is_quantized_to_16_steps():
    # the NES triangle's audible stepping — smooth would be wrong
    x = triangle(220.0, 0.3, steps=16)
    levels = len(np.unique(np.round(x, 6)))
    assert levels <= 17, "got %d levels, hardware had ~16" % levels
    assert levels > 4, "over-quantized to %d levels" % levels


def test_noise_is_lfsr_not_white_noise():
    a = noise(0.2, period=32)
    b = noise(0.2, period=32)
    assert np.array_equal(a, b), "LFSR must be deterministic"
    assert set(np.unique(a)) <= {-1.0, 1.0}
    assert len(np.unique(a)) == 2, "noise should be a 1-bit register"


def test_noise_short_mode_is_more_periodic_than_long():
    # short mode is the metallic, almost-pitched rattle
    long_n = noise(0.3, period=8, short=False)
    short_n = noise(0.3, period=8, short=True)
    def rep(x, lag=600):
        x = x - x.mean()
        return abs(float(np.dot(x[:-lag], x[lag:]) / max(np.dot(x, x), 1e-9)))
    assert rep(short_n) > rep(long_n)


def test_noise_period_controls_brightness():
    fast, slow = noise(0.2, period=4), noise(0.2, period=64)
    flips = lambda x: int(np.sum(np.diff(x) != 0))
    assert flips(fast) > flips(slow) * 4


def test_sweep_changes_pitch_in_the_right_direction():
    down = sweep(800, 100, 0.4)
    half = len(down) // 2
    edges = lambda x: int(np.sum((x[1:] > 0) & (x[:-1] <= 0)))
    assert edges(down[:half]) > edges(down[half:]), "downward sweep"
    up = sweep(100, 800, 0.4)
    assert edges(up[:half]) < edges(up[half:]), "upward sweep"


def test_atari_is_out_of_tune_the_way_the_hardware_was():
    # C4 lands nearly perfect, but its neighbours do not — that uneven
    # error across one octave IS the Atari sound.
    errs = {n: atari_detune_cents(n) for n in range(60, 72)}
    assert abs(errs[60]) < 5, "C4 should land close: %.1f" % errs[60]
    worst = max(abs(c) for c in errs.values())
    assert worst > 25, "not sour enough (worst %.1f cents)" % worst
    assert worst < 100, "worse than a semitone means a modelling bug"
    # and it must be deterministic, not random detuning
    assert atari_detune_cents(67) == atari_detune_cents(67)


def test_atari_note_renders_and_is_bounded():
    x = chip_synth.atari_note(64, 0.3)
    assert len(x) == int(0.3 * SR)
    assert np.max(np.abs(x)) <= 1.0


def test_chip_note_voices_and_bounds():
    for voice in ("pulse", "triangle"):
        x = chip_note(60, 0.25, voice=voice)
        assert len(x) == int(0.25 * SR)
        assert 0.05 < np.max(np.abs(x)) <= 1.0
        assert abs(x[0]) < 1e-9 and abs(x[-1]) < 1e-9


def test_chip_chord_respects_the_house_peak_ceiling():
    x = chip_chord([48, 52, 55, 59], 1.2)
    assert np.max(np.abs(x)) <= PEAK_CEILING + 1e-9


def test_drum_voices_are_audible_and_bounded():
    for name, fn in (("kick", chip_kick), ("snare", chip_snare),
                     ("hat", chip_hat)):
        x = fn()
        assert len(x) > 100, name
        assert 0.01 < np.max(np.abs(x)) <= 1.0, name
        assert not np.isnan(x).any(), name
        assert abs(x[-1]) < 1e-6, "%s must not step into silence" % name


def test_kick_sweeps_downward():
    x = chip_kick(0.2)
    half = len(x) // 2
    edges = lambda s: int(np.sum((s[1:] > 0) & (s[:-1] <= 0)))
    assert edges(x[:half]) > edges(x[half:])


def test_atari_tuning_option_actually_detunes_the_chord():
    # New Math's character trait: chords snap to the TIA divider grid, so
    # they come out genuinely sour. If this silently reverted to equal
    # temperament the identity would quietly vanish, so it's pinned.
    notes = [60, 64, 67]
    equal = chip_chord(notes, 0.6, tuning="equal")
    atari = chip_chord(notes, 0.6, tuning="atari")
    assert not np.allclose(equal, atari), "atari tuning changed nothing"
    # G (MIDI 67) is the sour one in this triad — well over a comma out
    assert abs(atari_detune_cents(67)) > 25


def test_chip_chord_is_held_not_arpeggiated():
    # owner 2026-11-01: no arpeggios. Every note sounds the whole time,
    # so the chord's first and last tenth carry the same pitches.
    x = chip_chord([60, 64, 67], 1.0)
    n = len(x) // 10
    spec = lambda s: np.abs(np.fft.rfft(s))
    a, b = spec(x[n:2 * n]), spec(x[-3 * n:-2 * n])
    assert np.corrcoef(a, b)[0, 1] > 0.9
    assert np.max(np.abs(chip_chord([], 0.5))) == 0.0


def test_chip_chord_passes_tuning_through():
    a = chip_chord([60, 64, 67], 0.5, tuning="atari")
    b = chip_chord([60, 64, 67], 0.5, tuning="equal")
    assert not np.allclose(a, b)
    for x in (a, b):
        assert np.max(np.abs(x)) <= PEAK_CEILING + 1e-9
        assert abs(x[0]) < 1e-9 and abs(x[-1]) < 1e-9


def test_midi_to_hz_matches_concert_pitch():
    assert abs(midi_to_hz(69) - 440.0) < 1e-9
