"""Note-by-note instruments (tools/multisample.py), owner 2026-09-24.

Pins his wiring answers (families, harmonicas out, strings as backup),
the octave trap (names read an octave low on most of VCSL/VSCO — measured),
and the "each note gets its own recording" rule. No drive needed: the
tree is built in tmp_path and the pitch reader is faked with the offsets
actually measured on the real files."""
from __future__ import annotations

import random
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import instrument_sampler as IS                             # noqa: E402
import multisample as MS                                    # noqa: E402


def _touch(root, rel):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(p), "wb") as w:        # a real (tiny) wav header
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(b"\0\0" * 10)
    return p


# measured 2026-09-24 (detect_pitch and pyin agree): true pitch minus name
MEASURED = {"Grand Piano, Steinway B": 0, "Oboe": 12, "Concert Harp": 0,
            "Cello Section": 12, "Clavisynth": 12, "Harpsichord, French": 12,
            "Kalimba, Kenya": 12, "Harmonica-Hohner-Super64": 12}


def _fake_measure(path):
    for inst, off in MEASURED.items():
        if "/%s/" % inst in path:
            return MS.named_note(Path(path).stem) + off
    if "/Bell Tree/" in path:                 # unpitched: never agrees
        return MS.named_note(Path(path).stem) + 4.3
    return None


def _tree(tmp_path):
    r = tmp_path / "BOTC Multisampled Instruments"
    for n in ("C4", "D4", "E4", "F4", "G4", "A4"):
        _touch(r, "VCSL/Chordophones/Zithers/Grand Piano, Steinway B/"
                  "Sustains/Steinway_sus_%s_v2_rr1.wav" % n)
        _touch(r, "VCSL/Chordophones/Zithers/Grand Piano, Steinway B/"
                  "Releases/Steinway_rel_%s_v2_rr1.wav" % n)
        _touch(r, "VSCO-2-CE/Woodwinds/Oboe/Vib/Oboe_Vib_%s_v3_Main.wav" % n)
        _touch(r, "VCSL/Chordophones/Composite Chordophones/Concert Harp/"
                  "Harp_%s_mf.wav" % n)
        _touch(r, "VSCO-2-CE/Strings/Cello Section/sus/sus_%s_v1_RR1.wav" % n)
        _touch(r, "VCSL/Electrophones/TX81Z/Clavisynth/Clav_%s.wav" % n)
        _touch(r, "VCSL/Chordophones/Zithers/Harpsichord, French/Sustains/"
                  "Harpsi_Sus_%s_rr1.wav" % n)
        _touch(r, "VCSL/Idiophones/Plucked Idiophones/Kalimba, Kenya/"
                  "Kal_%s_vl1.wav" % n)
        _touch(r, "VCSL/Aerophones/Free Aerophones/Harmonica-Hohner-Super64/"
                  "Harm_%s.wav" % n)
        _touch(r, "VCSL/Idiophones/Struck Idiophones/Bell Tree/BT_%s.wav" % n)
    _touch(r, "VSCO-2-CE/Keys/Upright Piano/Player_dyn1_rr1_034.wav")
    return r


def test_named_note_reads_one_note_or_none():
    assert MS.named_note("Oboe_Vib_F5_v3_Main") == 77
    assert MS.named_note("GPiano_sus_A#-1_v3_rr1_Player") == 10
    assert MS.named_note("Kal_Db4_vl1") == 61
    assert MS.named_note("KSHarp_A2_f1") == 45               # f1 = forte
    assert MS.named_note("Player_dyn1_rr1_034") is None       # numbered
    assert MS.named_note("leg_C4_D4") is None                 # a slide


def test_octave_vote_needs_agreement():
    assert MS.octave_vote([12.0, 11.9, -12.1]) == 12
    assert MS.octave_vote([0.1, -0.2]) == 0
    assert MS.octave_vote([60.3, 60.3]) == 60           # Tubular Glockenspiel
    assert MS.octave_vote([11.25, 11.65]) == 12         # glock, read flat
    assert MS.octave_vote([1.8, 7.7]) is None           # Bell Tree
    assert MS.octave_vote([23.8, 12.0]) is None         # split: ask the
    assert MS.octave_vote([None, None]) is None         # instrument instead


def test_scan_fixes_the_octave_and_follows_his_families(tmp_path, monkeypatch):
    monkeypatch.setattr(MS, "CACHE", tmp_path / "cache.json")
    idx = MS.scan(_tree(tmp_path), measure=_fake_measure)
    by = {}
    for e in idx:
        by.setdefault(e["multi"].split("/")[-1], []).append(e)
    # the octave: name C4 (60) on an oboe really sounds C5 (72); a
    # Steinway named C4 really is C4
    assert min(e["note"] for e in by["Oboe"]) == 72
    assert min(e["note"] for e in by["Grand Piano, Steinway B"]) == 60
    # owner's families
    assert {e["group"] for e in by["Concert Harp"]} == {"guitar"}
    assert {e["group"] for e in by["Clavisynth"]} == {"synth"}
    assert {e["group"] for e in by["Harpsichord, French"]} == {"piano"}
    assert {e["group"] for e in by["Kalimba, Kenya"]} == {"bell"}
    assert {e["group"] for e in by["Oboe"]} == {"wood"}
    # strings are a backup only
    assert all(e["group"] == "string" and e.get("backup")
               for e in by["Cello Section"])
    assert not any(e.get("backup") for e in by["Oboe"])
    # left out: harmonicas (owner), Bell Tree (no pitch), release tails,
    # numbered files
    assert "Harmonica-Hohner-Super64" not in by
    assert "Bell Tree" not in by
    assert not any("Releases" in e["path"] for e in idx)
    assert "Upright Piano" not in by


def test_cached_votes_mean_no_second_read(tmp_path, monkeypatch):
    monkeypatch.setattr(MS, "CACHE", tmp_path / "cache.json")
    root = _tree(tmp_path)
    first = MS.scan(root, measure=_fake_measure)
    calls = []
    again = MS.scan(root, measure=lambda p: calls.append(p))
    assert not calls and len(again) == len(first)


def _row(path, note, group, multi=None, art="-", layer=0.5, backup=False):
    r = {"path": path, "name": Path(path).stem, "note": note,
         "clarity": 1.0 if multi else 0.8, "group": group}
    if multi:
        r.update(multi=multi, art=art, layer=layer)
    if backup:
        r["backup"] = True
    return r


def test_multisample_plays_first_his_samples_are_the_fallback():
    idx = [_row("/his/Pianos/keys_C4.wav", 60, "piano"),
           _row("/ms/Steinway/s_D4.wav", 62, "piano", "Steinway")]
    # his file is the exact note, but the multisample is within reach
    assert IS.nearest(idx, 60, "piano")["path"].startswith("/ms/")
    # out of the multisample's reach (> MAX_SHIFT) -> his sample plays
    far = [_row("/his/Pianos/keys_C4.wav", 60, "piano"),
           _row("/ms/Steinway/s_C6.wav", 84, "piano", "Steinway")]
    assert IS.nearest(far, 60, "piano")["path"].startswith("/his/")


def test_vsco_strings_are_a_backup_behind_his_own():
    idx = [_row("/his/Strings/str_C4.wav", 60, "string"),
           _row("/ms/Cello/c_C4.wav", 60, "string", "Cello", backup=True)]
    assert IS.nearest(idx, 60, "string")["path"].startswith("/his/")
    only = [idx[1]]
    assert IS.nearest(only, 60, "string")["path"].startswith("/ms/")


def test_every_note_gets_its_own_recording():
    idx = [_row("/ms/St/s_%d.wav" % n, n, "piano", "St", "sus")
           for n in (60, 62, 64, 65, 67)]
    idx.append(_row("/ms/Kawai/k_64.wav", 64, "piano", "Kawai", "sus"))
    pin = []
    first = IS.nearest(idx, 60, "piano")
    pin.append(first)
    picks = [IS.nearest(idx, n, "piano", prefer=pin[0]) for n in (60, 64, 67)]
    # one instrument (the pinned one), and each note its own file
    assert {p["multi"] for p in picks} == {first["multi"]}
    assert [p["note"] for p in picks] == [60, 64, 67]


def test_one_per_beat_keeps_one_instrument_articulation_and_layer():
    idx = [_row("/his/Pianos/k.wav", 60, "piano")]
    for inst in ("Steinway", "Kawai"):
        for art in ("sus", "stac"):
            for n in (60, 62, 64):
                for lay in (0.2, 0.5, 0.8):
                    idx.append(_row("/ms/%s/%s/%d_%s.wav" % (inst, art, n, lay),
                                    n, "piano", inst, art, lay))
    for seed in range(20):
        got = MS.one_per_beat(idx, random.Random(seed))
        ms = [e for e in got if e.get("multi")]
        assert len({(e["multi"], e["art"]) for e in ms}) == 1
        assert sorted(e["note"] for e in ms) == [60, 62, 64]    # one per note
        assert {e["layer"] for e in ms} == {0.5}
        assert got[0]["path"] == "/his/Pianos/k.wav"            # his stays
    insts = {[e for e in MS.one_per_beat(idx, random.Random(s))
              if e.get("multi")][0]["multi"] for s in range(40)}
    assert insts == {"Steinway", "Kawai"}                       # variety
