"""Chord/bass audio synthesis (punch list step 7) — shape and level
sanity, not exact waveform matching. These get mixed straight into a
beat's stereo bus, so the two things that would quietly break a render
are: wrong length (throws off the lane's timing) and clipping/silence
(a chord that swamps or vanishes in the mix).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from chord_synth import bass_voice, midi_to_hz, pad_voice          # noqa: E402
from make_drum_loops import SR                                    # noqa: E402


def test_midi_to_hz_matches_concert_pitch():
    assert midi_to_hz(69) == 440.0


def test_pad_voice_length_matches_duration():
    audio = pad_voice([60, 64, 67], dur=1.5)
    assert audio.shape == (int(1.5 * SR),)


def test_pad_voice_stays_under_clipping():
    audio = pad_voice([48, 52, 55, 60], dur=1.0)
    assert np.max(np.abs(audio)) < 1.0


def test_pad_voice_empty_notes_is_silence():
    audio = pad_voice([], dur=0.5)
    assert np.all(audio == 0.0)


def test_pad_voice_fades_in_and_out():
    audio = pad_voice([60, 64, 67], dur=1.0)
    assert abs(audio[0]) < abs(audio[SR // 2])
    assert abs(audio[-1]) < 0.05


def test_bass_voice_length_matches_duration():
    audio = bass_voice(48, dur=2.0)
    assert audio.shape == (int(2.0 * SR),)


def test_bass_voice_short_duration_is_exactly_that_long():
    # dur shorter than sub808's own natural length shouldn't wrap,
    # repeat, or get silently padded past what was asked for.
    short = bass_voice(48, dur=0.3)
    assert short.shape == (int(0.3 * SR),)
    assert np.max(np.abs(short)) < 1.0
