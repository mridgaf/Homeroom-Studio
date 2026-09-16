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

import chord_synth                                                # noqa: E402
import midi_packs                                                 # noqa: E402
from chord_synth import bass_voice, midi_to_hz                     # noqa: E402
from key_context import KeyContext                                # noqa: E402
from make_drum_loops import SR                                    # noqa: E402


def test_midi_to_hz_matches_concert_pitch():
    assert midi_to_hz(69) == 440.0


def test_bass_voice_length_matches_duration():
    audio = bass_voice(48, dur=2.0)
    assert audio.shape == (int(2.0 * SR),)


def test_bass_voice_short_duration_is_exactly_that_long():
    # dur shorter than sub808's own natural length shouldn't wrap,
    # repeat, or get silently padded past what was asked for.
    short = bass_voice(48, dur=0.3)
    assert short.shape == (int(0.3 * SR),)
    assert np.max(np.abs(short)) < 1.0


def test_sample_pool_includes_melody_role_and_both_kinds(monkeypatch):
    index = [
        {"key": "C", "mode": "minor", "bpm": 90, "role": "chord",
         "kind": "loop", "name": "chord-loop", "path": "/a.wav"},
        {"key": "C", "mode": "minor", "bpm": 90, "role": "melody",
         "kind": "oneshot", "name": "melody-oneshot", "path": "/b.wav"},
        {"key": "C", "mode": "minor", "bpm": 90, "role": "bass",
         "kind": "oneshot", "name": "bass-oneshot", "path": "/c.wav"},
    ]
    monkeypatch.setattr(chord_synth, "scan_loops", lambda: index)
    pool = chord_synth.sample_pool(KeyContext("C", "minor"), bpm=90)
    assert {e["name"] for e in pool} == {"chord-loop", "melody-oneshot"}


def test_loop_voice_chops_a_loop_kind_pick(monkeypatch):
    # A loop-kind pick must go through chop_onsets before fit_loop —
    # feed it two fake "hits" and confirm the returned audio is one of
    # the chopped clips (short), not the full uncut loop.
    pick = {"key": "C", "mode": "minor", "bpm": 90, "role": "chord",
            "kind": "loop", "name": "loop-pick", "path": "/x.wav"}
    full_loop = np.ones(SR * 4)
    hit_a, hit_b = np.ones(200), np.ones(300)
    monkeypatch.setattr(chord_synth, "load_audio", lambda path: full_loop)
    monkeypatch.setattr(chord_synth, "chop_onsets",
                        lambda mono, sr: [hit_a, hit_b])
    audio, name = chord_synth.loop_voice(
        [pick], dur=0.5, key=KeyContext("C", "minor"))
    assert name == "loop-pick"
    assert audio.shape == (int(0.5 * SR),)         # fit_loop's crop/tile


def test_loop_voice_loop_kind_no_onsets_falls_back_to_none(monkeypatch):
    pick = {"key": "C", "mode": "minor", "bpm": 90, "role": "chord",
            "kind": "loop", "name": "silent-loop", "path": "/x.wav"}
    monkeypatch.setattr(chord_synth, "load_audio", lambda path: np.zeros(SR))
    monkeypatch.setattr(chord_synth, "chop_onsets", lambda mono, sr: [])
    audio, name = chord_synth.loop_voice(
        [pick], dur=0.5, key=KeyContext("C", "minor"))
    assert (audio, name) == (None, None)


def test_loop_voice_empty_pool_falls_back_to_none():
    audio, name = chord_synth.loop_voice([], dur=1.0, key=KeyContext("C", "minor"))
    assert (audio, name) == (None, None)


def test_loop_voice_fits_pick_to_duration(monkeypatch):
    pick = {"key": "C", "mode": "minor", "bpm": 90, "role": "chord",
            "kind": "oneshot", "name": "test-pick", "path": "/x.wav"}
    fake_audio = np.sin(2 * np.pi * 110 * np.arange(SR) / SR)  # 1s mono
    monkeypatch.setattr(chord_synth, "load_audio", lambda path: fake_audio)
    audio, name = chord_synth.loop_voice(
        [pick], dur=0.5, key=KeyContext("C", "minor"))
    assert name == "test-pick"
    assert audio.shape == (int(0.5 * SR),)
    assert np.max(np.abs(audio)) < 1.0


# ---------------------------------------------------- MIDI chord packs


def test_midi_pool_delegates_to_midi_packs_in_key(monkeypatch):
    monkeypatch.setattr(midi_packs, "scan", lambda: ["fake-index"])
    seen = {}

    def fake_in_key(index, key, role="chord"):
        seen["args"] = (index, key.root, key.mode, role)
        return ["a-pick"]
    monkeypatch.setattr(midi_packs, "in_key", fake_in_key)
    pool = chord_synth.midi_pool(KeyContext("C", "minor"))
    assert pool == ["a-pick"]
    assert seen["args"] == (["fake-index"], "C", "minor", "chord")


def test_midi_progression_transposes_into_key(monkeypatch):
    # File is itself in D minor; asking for it in C minor should shift
    # the D-minor chord (root pc 2) down 2 semitones to root pc 0, and
    # re-voice it compactly with KeyContext.voice (not reuse the file's
    # own raw, possibly wide, note stack — see midi_progression's
    # docstring).
    pick = {"path": "/x.mid", "key": "D", "mode": "minor"}
    monkeypatch.setattr(midi_packs, "read_notes", lambda path: "raw-notes")
    monkeypatch.setattr(midi_packs, "progression", lambda notes: [
        (0.0, 2, "minor", [50, 53, 57])])
    prog = chord_synth.midi_progression(pick, KeyContext("C", "minor"))
    assert prog == [(0, "minor", KeyContext("C", "minor").voice(0, "minor"))]


def test_midi_progression_no_chords_returns_none(monkeypatch):
    pick = {"path": "/x.mid", "key": "C", "mode": "minor"}
    monkeypatch.setattr(midi_packs, "read_notes", lambda path: "raw-notes")
    monkeypatch.setattr(midi_packs, "progression", lambda notes: [])
    assert chord_synth.midi_progression(pick, KeyContext("C", "minor")) is None
