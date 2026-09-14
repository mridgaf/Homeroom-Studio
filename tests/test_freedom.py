"""The 70/30 freedom pass (owner 2026-09-14).

"all djs have all instruments, chords and keys available to them. keep djs
70% true to character weights, 70% of the time. the rest is free for all" —
drum kit sounds, patterns and backbeats included, drum parts borrowed "each
from a different DJ". And the hard rule that came with it: "don't pile lows
on lows" — the kick plus ONE low sound per beat.
"""
import random
import sys
import wave
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import beat_machine                                           # noqa: E402
import beat_recipes                                           # noqa: E402
import crew                                                   # noqa: E402
import pattern_gen                                            # noqa: E402
from crew import CREW                                         # noqa: E402
from make_drum_loops import SR                                # noqa: E402

from test_beat_machine import _wav_pool                       # noqa: E402


def _free_and_not(n=2):
    free = [v for v in range(2, 400) if pattern_gen.free_beat(v)][:n]
    kept = [v for v in range(2, 400) if not pattern_gen.free_beat(v)][:n]
    return free, kept


# ------------------------------------------------------------- the roll

def test_thirty_percent_of_beats_are_free():
    got = sum(pattern_gen.free_beat(v) for v in range(2, 10002)) / 10000.0
    assert 0.28 < got < 0.32, got


# ----------------------------------------------------------- instruments

def test_a_free_beat_can_lead_with_any_instrument():
    pref = [["strings", 3], ["piano", 1]]
    leads = {beat_machine._source_order(pref, random.Random(s), free=True)[0]
             for s in range(300)}
    assert {"horns", "guitar", "loop", "strings"} <= leads
    assert "chip" not in leads                  # his 2026-07-25 rule stands
    order = beat_machine._source_order(pref, random.Random(1), free=True)
    assert "strings" in order and "piano" in order and order[-1] == "synth"


def test_in_character_order_is_unchanged():
    pref = [["strings", 3], ["piano", 1]]
    for s in range(50):
        order = beat_machine._source_order(pref, random.Random(s))
        assert order[0] in ("strings", "piano")


# ----------------------------------------------------------- drum sounds

def test_drum_sounds_follow_taste_in_character_and_open_on_free_beats(
        tmp_path):
    tagged = {"name": "hard kick", "path": str(tmp_path / "hard.wav")}
    other = [{"name": "kick %d" % i, "path": str(tmp_path / ("k%d.wav" % i))}
             for i in range(6)]
    for e in [tagged] + other:
        with wave.open(e["path"], "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(np.full(SR // 8, 9000, "<i2").tobytes())
    pool = {"kick": [tagged] + other}
    taste = {crew._pick_path(pool, "kick", ["hard"], 0.1, s,
                             open_bank=False)[0] for s in range(20)}
    assert taste == {tagged["path"]}
    wide = {crew._pick_path(pool, "kick", ["hard"], 0.1, s,
                            open_bank=True)[0] for s in range(40)}
    assert len(wide) > 3


def test_build_kit_hands_the_free_roll_to_every_dj_only(monkeypatch):
    seen = []

    def fake(shots, role, wants, secs, seed, **kw):
        seen.append(kw.get("open_bank"))
        return "/x.wav", np.zeros(64)
    monkeypatch.setattr(crew, "_pick_path", fake)
    free, kept = _free_and_not(1)
    crew.build_kit({}, "Otto Grit", None, variant=free[0])
    assert set(seen) == {True}
    seen.clear()
    crew.build_kit({}, "Doc Day", None, variant=kept[0])
    assert set(seen) == {False}                # a Legend's taste, 70%
    seen.clear()
    genre = next(n for n in CREW if n in crew.GENRE_NAMES)
    crew.build_kit({}, genre, None, variant=free[0])
    assert set(seen) == {None}                 # genre presets unchanged


def test_collab_kits_follow_the_same_roll(monkeypatch):
    seen = []

    def fake(shots, role, wants, secs, seed, **kw):
        seen.append(kw.get("open_bank"))
        return "/x.wav", np.zeros(64)
    monkeypatch.setattr(beat_machine, "_pick_path", fake)
    free, kept = _free_and_not(1)
    names = ["Otto Grit", "Doc Day"]
    for v, want in ((free[0], True), (kept[0], False)):
        preset, _notes = beat_machine.collab_preset(names, v, None)
        stamps = {n: ("/s.wav", np.zeros(8)) for n in names}
        seen.clear()
        beat_machine.collab_kit({}, names, preset, stamps, v, set())
        assert seen and set(seen) == {want}


# ------------------------------------------------------ drum patterns

def test_free_beat_borrows_each_drum_part_from_other_djs():
    import copy
    free, _ = _free_and_not(1)
    p = copy.deepcopy(CREW["Otto Grit"])
    notes = beat_machine._borrow_drum_parts(p, "Otto Grit", free[0])
    lanes = [n.split(" from ")[0] for n in notes]
    assert "kick" in lanes and "hat" in lanes, notes
    donors = {n.split(" from ")[1] for n in notes}
    assert "Otto Grit" not in donors
    for n in donors:
        assert crew.is_dj(n)
    for spec in p["grammar"].values():
        assert not (isinstance(spec, dict) and "copy" in spec
                    and spec["copy"] not in p["grammar"])


def test_doc_days_locked_snare_is_never_borrowed_over():
    import copy
    p = copy.deepcopy(CREW["Doc Day"])
    before = copy.deepcopy(p["grammar"].get("snare"))
    for v in range(2, 60):
        beat_machine._borrow_drum_parts(p, "Doc Day", v)
        assert p["grammar"].get("snare") == before


# ------------------------------------------------------------ the keys

def test_bb_beats_keep_their_808(monkeypatch):
    # "Bb".upper() is "BB"; the old sharps-only lookup dropped every Bb 808
    monkeypatch.setattr(beat_machine, "_808_notes", lambda: {"/x.wav": "C"})
    audio = np.sin(np.arange(SR // 4) / 10.0)
    got, semis = beat_machine._808_to_key("/x.wav", audio, "Bb")
    assert got is not None and semis == -2


# ------------------------------------------------ one low sound per beat

def test_a_second_low_lane_is_refused():
    preset = {"lanes": {"kick": 1, "sub": 2, "bass": 3}, "kit": {"bass": 1}}
    kit, sources, notes = {"sub": 1, "bass": 2}, {"sub": 1, "bass": 2}, []
    beat_machine._refuse_second_low(preset, kit, sources, notes)
    assert [ln for ln in preset["lanes"] if ln in crew._LOW_END] == ["sub"]
    assert "bass" not in kit and "bass" not in sources and notes


def test_a_long_808_kick_is_the_low_sound():
    preset = {"lanes": {"kick": 1}, "kit": {"kick": ("kick", "808", [], 0.9)}}
    assert beat_machine._low_voice(preset, 5, {"chords": True}, False,
                                   "Otto Grit", {"bass": [1]}) == "kit"


@pytest.fixture
def low_env(tmp_path, monkeypatch):
    monkeypatch.setattr(crew, "LOCK", tmp_path / "crew_kits.json")
    monkeypatch.setattr(beat_recipes, "HIST", tmp_path / "hist.json")
    root = tmp_path / "beats"
    root.mkdir()
    shots = _wav_pool(tmp_path)
    shots["bass"] = shots["kick"]                # the "808" pool
    bass = []                                    # his Bass-folder samples
    for i in range(6):
        f = tmp_path / ("basssample_%d.wav" % i)
        with wave.open(str(f), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.sin(2 * np.pi * 65 * np.arange(SR // 2) / SR)
                           * 20000).astype("<i2").tobytes())
        bass.append({"path": str(f), "name": f.stem, "note": 36 + i,
                     "clarity": 0.9, "group": "bass"})
    monkeypatch.setattr(beat_machine, "_low_pool",
                        lambda kind: bass if kind == "bass" else [])
    monkeypatch.setattr(beat_machine, "SAMPLED_BASS_P", 1.0)
    import string_sampler
    monkeypatch.setattr(string_sampler, "scan", lambda *a, **k: [])
    return root, shots


def test_strings_basses_only_play_when_the_beat_has_no_other_low(
        low_env, monkeypatch):
    root, shots = low_env
    seen = []
    real = beat_machine._build_chords

    def spy(*a, **kw):
        seen.append(kw.get("allow_basses"))
        return real(*a, **kw)
    monkeypatch.setattr(beat_machine, "_build_chords", spy)
    for low, allowed in (("808", False), ("kit", False), (None, True)):
        monkeypatch.setattr(beat_machine, "_low_voice",
                            lambda *a, _low=low, **k: _low)
        random.seed(4)
        beat_machine.generate(["Otto Grit"], root=root, shots=shots)
        assert seen and seen[-1] is allowed, (low, seen)


def test_no_beat_ever_has_two_low_sounds(low_env):
    """The invariant, end to end: every beat, free or in character, keeps
    at most one low lane. Premise check: the run must include a free beat
    that reached a low sound other than the 808, or it proves nothing."""
    root, shots = low_env
    other = 0
    for seed in range(18):
        name = ("Otto Grit", "Crate Prophet", "Sunday Chop")[seed % 3]
        random.seed(seed)
        path, report = beat_machine.generate([name], root=root, shots=shots,
                                             notes="no chords",
                                             traditional=True)
        rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
        lows = [ln for ln in rec["preset"]["lanes"] if ln in crew._LOW_END]
        assert len(lows) <= 1, (lows, report)
        bass_file = str((rec.get("kit_paths") or {}).get("bass") or "")
        if "sub" in lows or "basssample" in bass_file:
            other += 1
    assert other, "no free beat reached a non-808 low sound"
