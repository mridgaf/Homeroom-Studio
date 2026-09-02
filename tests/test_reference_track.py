"""Section 5: reading a reference track's tempo and key.

Both readings are allowed to be wrong in one specific way each — a tempo
half or double, a key swapped for its relative major/minor — because the
page shows the alternate and he corrects it in one click. What is NOT
allowed is a reading that is wrong in some third way, with no button
that reaches the truth.
"""
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import reference_track as rt

LIBRARY = Path("/Volumes/TBOTC 3/Claude Drum Beats/Favorites")


def test_the_modules_own_self_check_passes():
    rt.demo()


def test_an_accented_pulse_reads_its_real_tempo():
    bpm, _ = rt.detect_tempo(rt._onset_env(rt._click(96)))
    assert abs(bpm - 96) <= 2, bpm


def test_a_dead_even_pulse_is_at_worst_one_click_away():
    """Nothing in an unaccented stream of 8ths says which hit is the
    downbeat, so 75 is as true as 150. The truth still has to be on the
    page — that is what the x2 button is for."""
    bpm, alts = rt.detect_tempo(rt._onset_env(rt._click(150, accent=False)))
    assert 150 in [bpm] + alts, (bpm, alts)


def test_the_alternates_are_the_half_and_the_double():
    bpm, alts = rt.detect_tempo(rt._onset_env(rt._click(96)))
    want = [int(round(b)) for b in (bpm / 2.0, bpm * 2.0)
            if rt.TEMPO_LO <= b <= rt.TEMPO_HI]
    assert alts == want, (bpm, alts)
    assert alts, "there is always at least one octave to offer"
    for a in alts:
        assert rt.TEMPO_LO <= a <= rt.TEMPO_HI


def test_a_minor_drone_reads_as_that_minor_key():
    root, mode, alt, alt_mode = rt.detect_key(rt._drone(0, minor=True))
    assert (root, mode) == ("C", "minor")
    # the mistake this method actually makes, offered as the alternate
    assert (alt, alt_mode) == ("D#", "major")


def test_a_major_drone_reads_as_that_major_key():
    root, mode, alt, alt_mode = rt.detect_key(rt._drone(7, minor=False))
    assert (root, mode) == ("G", "major")
    assert (alt, alt_mode) == ("E", "minor")


def test_the_roots_are_spelled_the_way_the_engine_spells_them():
    """beat_machine.ROOT_HZ writes the note between A and B as "Bb". A
    detector that answered "A#" would hand back a key the engine then
    refuses."""
    import beat_machine
    assert len(rt.ROOTS) == 12
    assert set(rt.ROOTS) == set(beat_machine.ROOT_HZ)


def test_analyze_reads_a_file_off_disk(tmp_path):
    """The server's path: bytes in, numbers out, nothing kept."""
    f = tmp_path / "ref.wav"
    x = (rt._click(96, secs=12.0) / 8.0 * 32000).astype("<i2")
    with wave.open(str(f), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rt.SR)
        w.writeframes(x.tobytes())
    got = rt.analyze_bytes(f.read_bytes(), "ref.wav")
    assert abs(got["bpm"] - 96) <= 2, got
    assert got["root"] in rt.ROOTS and got["mode"] in ("major", "minor")
    assert 11.0 <= got["seconds"] <= 13.0
    assert got["alt_root"] in rt.ROOTS


def test_a_stereo_44k_file_is_read_too(tmp_path):
    """His reference tracks are stereo at 44.1 kHz, not mono at 22050."""
    f = tmp_path / "ref.wav"
    mono = rt._click(96, secs=12.0) / 8.0
    import soxr
    up = soxr.resample(mono, rt.SR, 44100)
    st = np.repeat(up[:, None], 2, axis=1)
    with wave.open(str(f), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes((st * 32000).astype("<i2").tobytes())
    got = rt.analyze(f)
    assert abs(got["bpm"] - 96) <= 2, got


@pytest.mark.skipif(not LIBRARY.exists(),
                    reason="needs the TBOTC 3 drive mounted")
def test_scored_against_his_own_beats():
    """The honest accuracy number, on real material with known answers:
    his rendered beats carry the tempo in the filename and the key in the
    recipe. This is a HARSH set — drum-led beats where the chords are one
    lane among ten — so the floors here are deliberately below what a
    full song should give. They exist to catch a regression, not to
    advertise the detector.

    Measured 2026-09-01: 17/25 tempo exact, 19/25 within one click,
    11/21 key root exact.
    """
    import json
    import re
    recipes = LIBRARY.parent / ".recipes"
    wavs = sorted(p for p in LIBRARY.iterdir() if p.suffix == ".wav")[:12]
    assert wavs, "no beats in Favorites to score against"
    exact = close = tempos = keys = roots = 0
    for w in wavs:
        got = rt.analyze(w)
        m = re.search(r" (\d+)bpm", w.name)
        if m:
            tempos += 1
            exact += got["bpm"] == int(m.group(1))
            if int(m.group(1)) in [got["bpm"]] + got["bpm_alts"]:
                close += 1
        rj = recipes / (w.name.split(" ", 1)[0] + ".json")
        if rj.exists():
            want = (json.loads(rj.read_text()).get("harmony") or {}).get("root")
            if want:
                keys += 1
                roots += got["root"] == want
    assert tempos and keys, (tempos, keys)
    assert close / tempos >= 0.6, f"tempo within one click: {close}/{tempos}"
    # exactness is what the 128-sample hop buys: at 256 the envelope is
    # too coarse and a 93 BPM beat reads 92
    assert exact / tempos >= 0.55, f"tempo exact: {exact}/{tempos}"
    assert roots / keys >= 0.3, f"key root exact: {roots}/{keys}"
