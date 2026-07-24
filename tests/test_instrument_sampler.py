"""instrument_sampler: the pitch detection and the multi-sample mapping.

The pitch/shift math is tested on SYNTHESIZED tones on purpose — a test
that needed the owner's external drive mounted would be skipped exactly
when it mattered. The library-dependent parts (does the real pool cover
the chord range?) are the report in tools/instrument_sampler.py, not asserts
here.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "tools"))

import numpy as np                                          # noqa: E402
import pytest                                               # noqa: E402

import instrument_sampler                                        # noqa: E402
from instrument_sampler import (_attack, _shift, detect_pitch,    # noqa: E402
                                group_of, nearest, note_slice, play_chord)
from make_drum_loops import SR                              # noqa: E402


def tone(midi, secs=1.0, sr=SR):
    """A harmonically rich tone at `midi` — a saw-ish stack, so
    autocorrelation has a real period to find like it would on brass."""
    hz = 440.0 * 2.0 ** ((midi - 69) / 12.0)
    t = np.arange(int(secs * sr)) / sr
    x = sum(np.sin(2 * np.pi * hz * k * t) / k for k in range(1, 8))
    return x / np.max(np.abs(x))


@pytest.mark.parametrize("midi", [43, 52, 60, 67, 72, 79])
def test_detect_pitch_finds_the_right_note(midi):
    got, clarity = detect_pitch(tone(midi))
    assert got is not None
    assert abs(got - midi) < 0.5, "detected %.2f, wanted %d" % (got, midi)
    assert clarity > 0.6


def test_detect_pitch_rejects_noise():
    rng = np.random.RandomState(0)
    _, clarity = detect_pitch(rng.randn(SR))
    assert clarity < instrument_sampler.MIN_CLARITY


def test_detect_pitch_handles_silence_and_short_input():
    assert detect_pitch(np.zeros(SR))[0] is None
    assert detect_pitch(np.zeros(100))[0] is None


def test_shift_moves_pitch_by_the_right_interval():
    # shift a known tone up 3 semitones, re-detect: it should read 3 higher
    shifted = _shift(tone(60, secs=2.0), 3)
    got, _ = detect_pitch(shifted)
    assert abs(got - 63) < 0.5, "got %.2f" % got


def test_shift_down_and_zero():
    got, _ = detect_pitch(_shift(tone(60, secs=2.0), -5))
    assert abs(got - 55) < 0.5
    same = _shift(tone(60), 0)
    assert np.allclose(same, tone(60))


def test_nearest_picks_the_smallest_shift():
    idx = [{"path": "a", "name": "a", "note": 48, "clarity": 0.9,
            "group": "brass"},
           {"path": "b", "name": "b", "note": 72, "clarity": 0.9,
            "group": "brass"}]
    assert nearest(idx, 50)["note"] == 48
    assert nearest(idx, 70)["note"] == 72
    assert nearest(idx, 60) is not None            # tie -> still voiced


def test_nearest_breaks_ties_toward_the_clearer_sample():
    idx = [{"path": "murky", "name": "m", "note": 60, "clarity": 0.61,
            "group": "brass"},
           {"path": "clear", "name": "c", "note": 60, "clarity": 0.99,
            "group": "brass"}]
    assert nearest(idx, 60)["path"] == "clear"


def test_nearest_respects_group_and_empty_pool():
    idx = [{"path": "s", "name": "s", "note": 62, "clarity": 0.9,
            "group": "wood"}]
    assert nearest(idx, 60, groups="brass") is None
    assert nearest(idx, 60, groups="wood")["path"] == "s"
    assert nearest([], 60) is None


def test_group_matches_whole_tokens_not_substrings():
    # the real trap: "Cymatics - LEAD Hornet" is a synth lead, not a horn.
    # It still classifies (as synth, via "lead") — the point is that the
    # substring "horn" inside "Hornet" must NOT make it brass.
    assert group_of("Cymatics - LEAD Hornet - C") == "synth"
    assert group_of("89 Bpm_Cm_BLEECH_Muted Horns 1") == "brass"
    assert group_of("80_TR07 Low Trumpet Am") == "brass"
    assert group_of("75_TR13 Saxx Delay A") == "wood"
    assert group_of("Bordeaux Piano_Melodic_Piano_16-05_Loop") == "piano"
    assert group_of("Nantes Acoustic_Melodic_Acoustic_16-05") == "guitar"
    assert group_of("Some Untagged Melody 90 Cm") is None


def test_specific_instrument_beats_generic_lead_or_synth():
    # ordered first-match-wins: a flute MELODY loop is wood, not a lead,
    # and a "Pluck Synth" one-shot is a pluck before it's a synth.
    assert group_of("BPM_Loop_Melody_Flute_1_Dm_95") == "wood"
    assert group_of("BPM_Tasty_Poppy_Pluck_Synth_One_Shot_E") == "pluck"
    assert group_of("84 Bpm_Cm_DECEPT_Organ Glide") == "organ"
    assert group_of("82 Bpm_Fm_ROT_Bell Chord 1") == "bell"


def test_thin_group_hands_off_when_it_cannot_cover_the_note():
    # the reason nearest takes max_shift: a group can EXIST but have a
    # hole. A note 9 semitones from the only organ sample should come from
    # the piano listed after it, not be stretched into sounding wrong.
    idx = [{"path": "org", "name": "org", "note": 48, "clarity": 0.9,
            "group": "organ"},
           {"path": "pno", "name": "pno", "note": 60, "clarity": 0.9,
            "group": "piano"}]
    assert nearest(idx, 50, ("organ", "piano"))["path"] == "org"   # covered
    assert nearest(idx, 57, ("organ", "piano"))["path"] == "pno"   # hole
    # no listed group can cover it -> least-bad pick, never None/silence
    assert nearest(idx, 90, ("organ", "piano")) is not None


def test_one_hit_chops_a_long_phrase_but_keeps_a_short_oneshot():
    from instrument_sampler import CHOP_SECS, _one_hit
    short = tone(60, secs=1.0)
    # one-shot: kept whole, bar the few samples _attack trims off the front
    assert len(_one_hit(short)) == pytest.approx(len(short), abs=0.01 * SR)
    # a long phrase: three spaced hits -> only the first survives
    gap = np.zeros(int(0.4 * SR))
    phrase = np.concatenate([tone(60, secs=0.5), gap,
                             tone(64, secs=0.5), gap,
                             tone(67, secs=3.0)])
    assert len(phrase) > CHOP_SECS * SR
    got = _one_hit(phrase)
    assert len(got) < len(phrase)
    assert abs(detect_pitch(got)[0] - 60) < 0.5   # kept the FIRST hit


def test_attack_trims_leading_silence():
    body = tone(60, secs=0.5)
    padded = np.concatenate([np.zeros(int(0.2 * SR)), body])
    trimmed = _attack(padded)
    assert len(trimmed) == pytest.approx(len(body), abs=0.01 * SR)
    assert _attack(np.zeros(1000)).shape == (1000,)      # silence: unchanged


def _fake_index(tmp_path, notes):
    """A real on-disk index of synthesized tones, so the load path
    (load_audio -> trim -> shift -> tile) is exercised end to end."""
    from make_drum_loops import write_wav24
    idx = []
    for n in notes:
        p = tmp_path / ("brass_%d.wav" % n)
        x = tone(n, secs=0.8)
        write_wav24(p, x, x)
        idx.append({"path": str(p), "name": "Brass %d" % n, "note": n,
                    "clarity": 0.95, "group": "brass"})
    return idx


def test_voice_note_is_in_tune_after_shifting(tmp_path):
    idx = _fake_index(tmp_path, [60])
    got, _ = detect_pitch(instrument_sampler.voice_note(idx, 64, dur=1.0))
    assert abs(got - 64) < 0.5, "shifted note landed at %.2f" % got


def test_note_slice_length_and_envelope(tmp_path):
    idx = _fake_index(tmp_path, [60])
    seg = note_slice(idx, 62, dur=0.4)
    assert seg.shape == (int(0.4 * SR),)
    assert abs(seg[0]) < 1e-6 and abs(seg[-1]) < 1e-6   # attack + release
    assert np.max(np.abs(seg)) > 0.01                    # not silent


def test_play_chord_voices_every_note_and_does_not_clip(tmp_path):
    idx = _fake_index(tmp_path, [48, 60, 72])
    out = play_chord(idx, [55, 58, 62], dur=1.5)
    assert out.shape == (int(1.5 * SR),)
    assert np.max(np.abs(out)) <= instrument_sampler.PEAK_CEILING + 1e-9
    assert np.max(np.abs(out)) > 0.01


def _max_step(x):
    return float(np.max(np.abs(np.diff(x)))) if len(x) > 1 else 0.0


def test_repeats_are_crossfaded_not_butt_spliced():
    # THE BUG the owner reported as "clipping at the end of the samples":
    # a source shorter than the chord got np.tile'd, putting a step
    # discontinuity at every seam. Measured on his brass: 0.209 at the
    # seam vs a 0.0001 median step. A crossfade must flatten that.
    from instrument_sampler import _fit_length
    # a ramp makes the seam unmissable and the test deterministic: its own
    # sample-to-sample slope is ~0.8/N, but a butt-splice drops 0.8 -> 0.0
    # in one sample. (A musical tone's own slew would mask that.)
    n_src = int(0.5 * SR)
    src = np.linspace(0.0, 0.8, n_src)
    n = int(1.6 * SR)                      # forces ~3 repeats
    hard = np.tile(src, n // len(src) + 1)[:n]
    soft = _fit_length(src, n)
    assert len(soft) == n
    assert _max_step(hard) > 0.5           # the defect, reproduced
    assert _max_step(soft) < _max_step(hard) / 5
    assert np.max(np.abs(soft)) > 0.4      # still audible, not faded away


def test_fit_length_crops_and_handles_edge_cases():
    from instrument_sampler import _fit_length
    src = tone(60, secs=1.0)
    assert len(_fit_length(src, int(0.4 * SR))) == int(0.4 * SR)
    assert len(_fit_length(np.array([]), 500)) == 500
    tiny = np.ones(3)                       # too short to crossfade
    assert len(_fit_length(tiny, 100)) == 100


def test_every_voiced_note_starts_and_ends_at_silence(tmp_path):
    # the other half of the click: a buffer that begins or ends mid-
    # waveform steps into silence. Both edges must ramp to zero.
    idx = _fake_index(tmp_path, [60])
    for dur in (0.4, 1.0, 2.2):             # 2.2s forces repeats
        seg = instrument_sampler.voice_note(idx, 62, dur=dur)
        assert abs(seg[0]) < 1e-9, "starts at %.5f" % abs(seg[0])
        assert abs(seg[-1]) < 1e-9, "ends at %.5f" % abs(seg[-1])


def test_play_chord_starts_and_ends_at_silence(tmp_path):
    idx = _fake_index(tmp_path, [48, 60, 72])
    out = play_chord(idx, [55, 58, 62], dur=2.2)
    assert abs(out[0]) < 1e-9 and abs(out[-1]) < 1e-9


def test_arp_riff_ends_at_silence():
    # arp_riff wraps its tail to the front for loop-safety, which used to
    # leave the buffer ending mid-note at full amplitude -> a click into
    # the next chord. The wrap stays; the step must not.
    import chord_synth
    out = chord_synth.arp_riff(
        [48, 51, 55], 2.0, 90,
        lambda n, d: np.ones(int(d * SR)) * 0.5)
    assert abs(out[-1]) < 1e-9


def _true_peak(x, os=4):
    """Inter-sample peak via 4x FFT oversampling. A buffer can sit under
    1.0 at every SAMPLE and still exceed 0 dBFS between them, which the
    converter clips on playback — the second half of what the owner heard.
    """
    n = len(x)
    X = np.fft.rfft(x)
    Y = np.zeros(n * os // 2 + 1, dtype=complex)
    Y[:len(X)] = X
    return float(np.max(np.abs(np.fft.irfft(Y, n * os) * os)))


def test_chord_stays_below_zero_dbfs_between_samples_too(tmp_path):
    # regression: at the old 0.99 ceiling the owner's own demos measured
    # +0.49 dBTP ("synth - high") — real clipping on playback that a
    # sample-peak assert called clean. The ceiling must leave headroom.
    idx = _fake_index(tmp_path, [48, 60, 72])
    out = play_chord(idx, [55, 58, 62], dur=1.5)
    assert _true_peak(out) < 1.0, "%.4f (clips between samples)" % _true_peak(out)


def test_play_chord_returns_none_on_empty_pool():
    assert play_chord([], [60, 64], dur=1.0) is None
    assert instrument_sampler.voice_note([], 60, dur=1.0) is None


def test_short_source_is_tiled_to_full_length(tmp_path):
    from make_drum_loops import write_wav24
    p = tmp_path / "short.wav"
    x = tone(60, secs=0.1)
    write_wav24(p, x, x)
    idx = [{"path": str(p), "name": "short", "note": 60, "clarity": 0.9,
            "group": "brass"}]
    out = instrument_sampler.voice_note(idx, 60, dur=1.0)
    assert out.shape == (SR,)
    assert np.max(np.abs(out)) > 0.01          # tiled, not zero-padded
