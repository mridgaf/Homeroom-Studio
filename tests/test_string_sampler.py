"""Strings sampler (harmonizer step 2) — the pure token-parsing and
chord-stacking math, no drive needed. `scan()` walks the library root
and isn't covered here (same reason test_melodic_loops.py skips it).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import string_sampler                                          # noqa: E402
from make_drum_loops import SR                                # noqa: E402
from string_sampler import nearest, note_from_tokens, play_chord  # noqa: E402


def test_note_from_tokens_reads_the_single_note():
    assert note_from_tokens(["pizz", "55", "ff", "RR1", "c"]) == 55


def test_note_from_tokens_drops_legato_transition_two_notes():
    # susbowleg_55_56_17_17: two plausible-note tokens (the bow moving
    # 55->56) -> not one playable pitch, so it's excluded.
    assert note_from_tokens(["susbowleg", "55", "56", "17", "17"]) is None


def test_note_from_tokens_ignores_out_of_range_numbers():
    # "17" is below the piano floor, so a name whose only note-ish token
    # is 17 has no playable note.
    assert note_from_tokens(["down", "17", "c"]) is None


def test_note_from_tokens_none_when_no_number():
    assert note_from_tokens(["down", "c"]) is None


def _entry(note, instrument="violin", style="sustain", mic="c"):
    return {"path": "/n%d" % note, "note": note, "instrument": instrument,
            "style": style, "mic": mic}


def test_nearest_picks_closest_pitch():
    idx = [_entry(50), _entry(60), _entry(72)]
    assert nearest(idx, 64)["note"] == 60      # 64 is closer to 60 than 72


def test_nearest_filters_by_instrument():
    idx = [_entry(60, instrument="violin"), _entry(60, instrument="basses")]
    assert nearest(idx, 60, instrument="basses")["instrument"] == "basses"


def test_nearest_empty_pool_is_none():
    assert nearest([], 60) is None


def test_play_chord_length_and_no_clipping(monkeypatch):
    idx = [_entry(60), _entry(64), _entry(67)]
    monkeypatch.setattr(string_sampler, "load_audio",
                        lambda path: np.ones(SR // 2))   # 0.5s mono per note
    chord = play_chord(idx, [60, 64, 67], dur=1.0)
    assert chord.shape == (SR,)                          # tiled to a full sec
    assert np.max(np.abs(chord)) < 1.0


def test_play_chord_none_when_nothing_voiced():
    assert play_chord([], [60, 64, 67], dur=1.0) is None


def test_play_chord_peak_guard_prevents_clipping(monkeypatch):
    # a hot transient (crest well above the RMS target) must be pulled
    # back under 1.0, not handed back clipping.
    idx = [_entry(60), _entry(64), _entry(67)]
    spike = np.zeros(SR // 2)
    spike[0] = 8.0                                       # huge crest, tiny RMS
    monkeypatch.setattr(string_sampler, "load_audio", lambda path: spike)
    chord = play_chord(idx, [60, 64, 67], dur=1.0)
    assert np.max(np.abs(chord)) <= 0.99


# ---- 2026-09-14: chords play their own notes, in tune ------------------

def _sine_for(idx):
    """load_audio stand-in: each path plays a 1s sine at its entry's note."""
    notes = {e["path"]: e["note"] for e in idx}

    def load(path):
        f = 440.0 * 2 ** ((notes[path] - 69) / 12.0)
        return np.sin(2 * np.pi * f * np.arange(SR) / SR)
    return load


def _peak_hz(x):
    mag = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    return np.argmax(mag) * SR / len(x)


def test_pinned_chord_plays_its_own_notes_not_the_pinned_file():
    # the 07-29 pin handed back the pinned FILE for every note, and with no
    # pitch shift a C-E-G chord came out C-C-C
    idx = [_entry(n, "viola", "sustain") for n in (48, 49, 51, 53, 55)]
    pin = idx[0]
    assert nearest(idx, 52, prefer=pin)["note"] in (51, 53)
    assert nearest(idx, 55, prefer=pin)["note"] == 55


def test_pin_keeps_style_and_mic_and_leaves_a_section_it_cannot_reach():
    idx = [_entry(55, "violin", "sustain"), _entry(41, "cello", "sustain"),
           _entry(41, "cello", "pizz"), _entry(41, "cello", "sustain", "r")]
    got = nearest(idx, 40, prefer=idx[0])     # violins stop at 55
    assert (got["instrument"], got["style"], got["mic"]) == \
        ("cello", "sustain", "c")


def test_play_chord_shifts_each_note_onto_its_exact_pitch(monkeypatch):
    # recorded every other note: asking for C4 (60) gets the 59 file,
    # which must come out at C4, not B3
    idx = [_entry(59, "violin", "sustain"), _entry(61, "violin", "sustain")]
    monkeypatch.setattr(string_sampler, "load_audio", _sine_for(idx))
    chord = play_chord(idx, [60], dur=1.0)
    assert abs(_peak_hz(chord) - 261.63) < 3.0


def test_plucked_style_rings_once_instead_of_repicking(monkeypatch):
    idx = [_entry(60, "violin", "pizz")]
    monkeypatch.setattr(string_sampler, "load_audio",
                        lambda path: np.ones(SR // 10))   # 0.1s pluck
    chord = play_chord(idx, [60], dur=1.0)
    assert np.max(np.abs(chord[SR // 2:])) == 0.0         # no re-pluck


def test_style_comes_from_the_vendor_folder_not_the_file_name(tmp_path):
    root = tmp_path
    lie = root / "LSS Violin I" / "samples" / "Glissando Samples"
    real = root / "LSS Violin I" / "samples" / "Sustain Samples"
    pizz = root / "LSS Cellos" / "samples" / "pizz" / "f" / "close"
    assert string_sampler._style(lie / "sustain_60_c.wav", root) is None
    assert string_sampler._style(real / "sustainff_60_c.wav", root) == "sustain"
    assert string_sampler._style(pizz / "pizz_36_f_RR1_c.wav", root) == "pizz"


def test_scan_keeps_picks_and_all_mics_drops_slides_and_sfx(tmp_path,
                                                            monkeypatch):
    files = [
        "LSS Cellos/samples/sus/f/close/sus_49_f_c.wav",
        "LSS Cellos/samples/sus/f/main/sus_49_f_m.wav",
        "LSS Cellos/samples/sus/l/close/sus_c_49_51_17_17.wav",   # a slide
        "LSS Violin I/samples/SFX Samples/100_c.wav",               # a noise
        "LSS Basses/samples/pizz/f/close/pizz_33_f_RR1_c.wav",      # not picked
    ]
    for f in files:
        (tmp_path / f).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / f).write_bytes(b"")
    monkeypatch.setattr(string_sampler, "CACHE", tmp_path / "cache.json")
    monkeypatch.setattr(string_sampler, "load_picks",
                        lambda: ({"cello", "violin"}, {"sustain"}))
    got = string_sampler.scan(root=str(tmp_path))
    assert sorted((e["note"], e["mic"]) for e in got) == [(49, "c"), (49, "m")]


def test_beat_pool_drops_basses_even_if_that_empties_it():
    idx = [_entry(40, "basses", "sustain")]
    assert string_sampler.beat_pool(idx, "sustain", basses=False) == []
    assert string_sampler.beat_pool(idx, "sustain") == idx
