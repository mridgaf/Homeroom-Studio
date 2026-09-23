"""The 70/30 freedom pass (owner 2026-09-14).

"all djs have all instruments, chords and keys available to them. keep djs
70% true to character weights, 70% of the time. the rest is free for all" —
drum kit sounds, patterns and backbeats included, drum parts borrowed "each
from a different DJ". And the hard rule that came with it: "don't pile lows
on lows" — the kick plus ONE low sound per beat.
"""
import random
import re
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


def test_the_kick_is_short_whenever_a_bass_plays():
    """Kick and bass as one unit (owner 2026-09-23): a long 808 kick can no
    longer be the beat's low sound. On an 808 beat the kick leaves the 808
    pool for the DJ's own non-808 flavor; either way it is capped short."""
    p = {"kit": {"kick": ("bass", "808", ["deep"], (0.9, 2.0))},
         "kick_flavors": [[0.2, "808", ["deep"], [0.9, 2.0]],
                          [0.8, None, ["punch"], [0.25, 0.6]]]}
    beat_machine._pair_kick(p, plays_808=True, has_bass=True)
    assert p["kit"]["kick"] == ("kick", None, ["punch"], (0.25, 0.5))
    q = {"kit": {"kick": ("bass", "808", [], (0.9, 2.0))}, "kick_flavors": []}
    beat_machine._pair_kick(q, plays_808=False, has_bass=True)
    assert q["kit"]["kick"][3] == (0.5, 0.5)
    r = {"kit": {"kick": ("bass", "808", [], (0.9, 2.0))}, "kick_flavors": []}
    beat_machine._pair_kick(r, plays_808=False, has_bass=False)
    assert r["kit"]["kick"][3] == (0.9, 2.0)        # no bass: left alone


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


def test_the_strings_basses_never_play(low_env, monkeypatch):
    """Since 2026-09-23 the 808 or the bass line is ALWAYS the bass, so the
    strings' own double basses never get the low end."""
    root, shots = low_env
    seen = []
    real = beat_machine._build_chords

    def spy(*a, **kw):
        seen.append(kw.get("allow_basses"))
        return real(*a, **kw)
    monkeypatch.setattr(beat_machine, "_build_chords", spy)
    for name in ("Otto Grit", "Night Metro"):
        random.seed(4)
        beat_machine.generate([name], root=root, shots=shots)
    assert seen == [False, False], seen


def test_no_beat_ever_has_two_basses(low_env, monkeypatch):
    """The invariant, end to end: one bass per beat -- an 808 OR the bass
    line, never both, never two low lanes. Premise check: the run must
    include both kinds of beat, or it proves nothing."""
    root, shots = low_env
    monkeypatch.setattr(beat_machine, "_808_notes",
                        lambda: {e["path"]: "C" for e in shots["bass"]})
    kinds = set()
    for seed in range(12):
        name = ("Otto Grit", "Night Metro", "Mustang", "Sunday Chop")[seed % 4]
        random.seed(seed)
        path, report = beat_machine.generate([name], root=root, shots=shots)
        rec = beat_recipes.load_recipe(root, int(path.name.split()[0]))
        lanes = rec["preset"]["lanes"]
        lows = [ln for ln in lanes if ln in crew._LOW_END]
        line = [ln for ln in lanes if re.fullmatch(r"bass\d+", ln)]
        voiced_808 = bool((rec.get("harmony") or {}).get("bass808"))
        assert len(lows) <= 1 and not (lows and line), (lows, line, report)
        kinds.add("808" if (voiced_808 or lows) else
                  "line" if line else "none")
    assert {"808", "line"} <= kinds, kinds
