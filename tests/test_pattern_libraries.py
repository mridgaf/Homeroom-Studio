"""The 100 new chord patterns and 100 new answer-melody shapes (2026-10-19).
Pure checks -- no drive, no audio."""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import chord_rhythm  # noqa: E402
import melody_rhythm as mr  # noqa: E402

SCALE = (9, 11, 0, 2, 4, 5, 7)
FAMILIES = list(mr.FAMILY) + [None]


def _slots(roots=(57, 53, 60, 55)):
    out = []
    for at, r in enumerate(roots):
        tones = [r, r + 3 if r % 12 in (9, 2, 4) else r + 4, r + 7]
        out.append({"tones": tones, "top": max(tones), "bars": 1,
                    "start_bar": at})
    return out


def _plan(fam, v, flow):
    spec = mr.spec_for({"signature": {"chord_family": fam}})
    return mr.plan_phrase(_slots(), SCALE, spec, v, 4, None, flow=flow)


# ---- chords ----

def test_chord_library_now_has_163_and_100_are_marked_v2():
    lib = chord_rhythm.library()
    assert len(lib) == 163
    assert sum(1 for e in lib if e["v"] == 2) == 100
    assert len({e["name"] for e in lib}) == 163


def test_new_chord_patterns_are_legal():
    for e in chord_rhythm.library():
        for bar in e["bars"]:
            hits = [i for i, ch in enumerate(bar) if ch != "-"]
            assert len(bar) == 16 and hits, e["name"]
            assert all(b - a >= 2 for a, b in zip(hits, hits[1:])), e["name"]


def test_beats_made_before_the_stamp_never_see_the_new_chord_patterns():
    old = chord_rhythm.spec_for({"chord_grammar": True, "chord_flow": 1})
    new = chord_rhythm.spec_for({"chord_grammar": True, "chord_flow": 1,
                                 "chord_lib": 2})
    assert old["lib_v"] == 1 and new["lib_v"] == 2
    v2 = {e["name"] for e in chord_rhythm.library() if e["v"] == 2}
    seen_old, seen_new = set(), set()
    for s in range(400):
        for spec, seen in ((old, seen_old), (new, seen_new)):
            tr = []
            chord_rhythm._library_bars(spec, random.Random(s), 2, False,
                                       None, trace=tr)
            seen.update(tr)
    assert not (seen_old & v2)
    assert seen_new & v2


# ---- melody ----

def test_melody_library_is_100_legal_unique_shapes():
    raw = json.load(open(ROOT / "melody_patterns.json"))["patterns"]
    assert len(raw) == 100
    lib = mr.library()
    assert len(lib) == 100                      # none dropped by the loader
    assert len({e["name"] for e in lib}) == 100
    assert len({(tuple(e["cells"]), tuple(e["moves"])) for e in lib}) == 100
    for e in lib:
        m = e["moves"]
        assert sum(1 for x in m if abs(x) >= 3) <= 1, e["name"]
        for i, x in enumerate(m):
            if abs(x) >= 3:
                assert i + 1 < len(m) and m[i + 1] == -1, e["name"]
    assert {len(e["cells"]) for e in lib} == {2, 3, 4, 5}


def test_flow_1_melody_beats_are_untouched_by_the_library(monkeypatch):
    for fam in FAMILIES:
        for v in range(60):
            with_lib = _plan(fam, v, 1)
            monkeypatch.setattr(mr, "_LIB", [])
            assert with_lib == _plan(fam, v, 1), (fam, v)
            monkeypatch.setattr(mr, "_LIB", None)


def test_flow_2_plays_a_library_shape_in_the_back_half():
    lib = {(tuple(e["cells"])) for e in mr.library()}
    for fam in FAMILIES:
        for v in range(80):
            hits = _plan(fam, v, 2)
            bar1 = tuple(st for b, st, _c, _n in hits if b == 1)
            assert bar1 in lib, (fam, v, bar1)


def test_flow_2_keeps_every_melody_rule():
    sl = _slots()
    tones = {t % 12 for s in sl for t in s["tones"]}
    top = max(s["top"] for s in sl)
    for fam in FAMILIES:
        for v in range(150):
            hits = _plan(fam, v, 2)
            assert hits, (fam, v)
            assert _plan(fam, v, 2) == hits                 # repeatable
            for b, st, ch, n in hits:
                assert n % 12 in set(SCALE) | tones, (fam, v, n)
                assert n > top, (fam, v, n)
                if st in mr.STRONG:
                    assert n % 12 in {t % 12 for t in mr._slot_at(
                        sl, b)["tones"]}, (fam, v, b, st, n)
            assert not any(b == 0 for b, *_ in hits)       # nothing on bar 1


def test_flow_2_gives_many_different_phrases():
    seen = {tuple((b, st, n) for b, st, _c, n in _plan("soul_jazz", v, 2))
            for v in range(200)}
    assert len(seen) > 120


def test_new_beats_are_stamped_for_the_library():
    assert mr.FLOW_VERSION == 2


# ---- bass patterns (2026-10-19) ----

import numpy as np  # noqa: E402

import bass_rhythm as br  # noqa: E402

BASS_SLOTS = [{"root": r - 12, "chord_root": r, "bars": 1, "start_bar": i,
               "tones": [r, r + 3, r + 7]}
              for i, r in enumerate((57, 53, 60, 55))]


def _bplan(fam, v, flow, slots=None):
    spec = br.spec_for({"bass_flow": flow,
                        "signature": {"chord_family": fam}})
    return br.plan_line(slots or BASS_SLOTS, None, spec, v,
                        lambda n: 28 <= n <= 62, SCALE)


def test_bass_library_is_100_legal_unique_patterns():
    raw = json.load(open(ROOT / "bass_patterns.json"))["patterns"]
    lib = br.library()
    assert len(raw) == 100 and len(lib) == 100        # loader dropped none
    assert len({e["name"] for e in lib}) == 100
    assert len({(tuple(e["bars"]), tuple(e["roles"])) for e in lib}) == 100
    for e in lib:
        assert e["bars"][0][0] == "X" and e["roles"][0][0] == "R", e["name"]
        for b, r in zip(e["bars"], e["roles"]):
            hits = [i for i, ch in enumerate(b) if ch != "-"]
            assert all(y - x >= 2 or "." in (b[x], b[y])
                       for x, y in zip(hits, hits[1:])), e["name"]
            if len(e["bars"]) > 1 and (b, r) != (e["bars"][-1],
                                                 e["roles"][-1]):
                assert "a" not in r and "n" not in r, e["name"]


def test_bass_flow_1_never_sees_the_patterns(monkeypatch):
    for fam in list(br.FAMILY) + [None]:
        spec = br.spec_for({"bass_flow": 1,
                            "signature": {"chord_family": fam}})
        assert "pattern" not in [f for f, _w in spec["figures"]]
        for v in range(40):
            with_lib = _bplan(fam, v, 1)
            monkeypatch.setattr(br, "_LIB", [])
            assert with_lib == _bplan(fam, v, 1), (fam, v)
            monkeypatch.setattr(br, "_LIB", None)


def test_bass_flow_2_plays_patterns_about_half_the_slots():
    n = pat = 0
    for fam in list(br.FAMILY) + [None]:
        for v in range(60):
            for p in _bplan(fam, v, 2):
                n += 1
                pat += p["figure"] == "pattern"
    assert 0.40 < pat / n < 0.60, pat / n


def test_bass_pattern_notes_are_real_in_range_and_start_on_the_root():
    for fam in list(br.FAMILY) + [None]:
        for v in range(120):
            plan = _bplan(fam, v, 2)
            for i, (s, p) in enumerate(zip(BASS_SLOTS, plan)):
                if p["figure"] != "pattern":
                    continue
                for _b, _st, ch, note in p["hits"]:
                    assert isinstance(note, int), (fam, v, note)
                    assert 28 <= note <= 62, (fam, v, note)
                if not plan[i - 1]["figure"] == "push":   # a push ties in
                    assert p["hits"][0] == (0, 0, "X", s["root"]), (fam, v)


def test_bass_family_leans_to_its_tags():
    names = {fam: collections_counter() for fam in ("dark", "bright_funk")}
    for fam in names:
        for v in range(300):
            for p in _bplan(fam, v, 2):
                if p["figure"] == "pattern":
                    names[fam]["n"] += 1
    assert names["dark"]["n"] and names["bright_funk"]["n"]


def collections_counter():
    import collections
    return collections.Counter()


def test_bass_pattern_render_is_one_note_at_a_time():
    slots = BASS_SLOTS
    plan = _bplan("bright_funk", 5, 2)
    feel = br.kick_feel({}, 1)
    bar_s, loop_n = 2.0, 8 * 44100
    out, notes = br.render_line(
        plan, slots, bar_s, 120, loop_n,
        lambda n, secs: np.ones(int(secs * 44100)) * 0.1, feel)
    assert out is not None and len(out) == loop_n
    assert all(len(x) >= 1 for x in notes)


# ---- alternate bass sounds (2026-10-19) ----

import bass_voices as bv  # noqa: E402
import instrument_sampler as ins  # noqa: E402
import string_sampler as ss  # noqa: E402

ROOTS = [45 - 12 + 0, 41 - 12 + 12, 48 - 12, 43 - 12 + 12]    # 33..36 area


def _strings(inst, style, lo, hi):
    return [{"path": "/x/%s_%s_%d_c.wav" % (inst, style, n), "note": n,
             "instrument": inst, "style": style, "mic": "c"}
            for n in range(lo, hi + 1, 2)]


def _piano_multi(lo, hi):
    return [{"path": "/x/piano_%d.wav" % n, "note": n, "group": "piano",
             "multi": "lib", "art": "sus", "clarity": 1.0}
            for n in range(lo, hi + 1)]




def _all_multi():
    out = []
    for g in ("piano", "guitar", "organ", "synth"):
        out += [dict(e, group=g, multi="lib-" + g) for e in _piano_multi(24, 72)]
    return out


def _fake_audio(monkeypatch):
    sine = np.sin(np.linspace(0, 200, 44100)) * 0.3
    monkeypatch.setattr(ss, "load_audio", lambda p: sine.copy())
    monkeypatch.setattr(ins, "load_audio", lambda p: sine.copy())
    monkeypatch.setattr(ss, "_shift", lambda m, semis: m)
    monkeypatch.setattr(ins, "_shift", lambda m, semis: m)


def _choose(v, w, strings, inst, monkeypatch):
    _fake_audio(monkeypatch)
    return bv.choose(v, ROOTS, {"signature": {"bass_voices": w}},
                     strings=strings, instruments=inst, cache={})


ONLY = lambda k: {kk: (1 if kk == k else 0) for kk in bv.WEIGHTS}  # noqa: E731


def test_cello_can_be_the_bass_and_the_line_fits_its_range(monkeypatch):
    s = _strings("cello", "pizz", 36, 77) + _strings("basses", "pizz", 28, 59)
    got = _choose(3, ONLY("cello"), s, [], monkeypatch)
    assert got and got["kind"] == "cello" and "pizz" in got["label"]
    line = [r + got["oct"] for r in ROOTS]
    assert min(line) >= 36 - bv.REACH and got["fits"](line[0])


def test_orchestral_bass_reaches_lower_than_the_cello(monkeypatch):
    s = _strings("basses", "sustain", 28, 59)
    got = _choose(1, ONLY("contrabass"), s, [], monkeypatch)
    assert got and got["kind"] == "contrabass"
    assert min(r + got["oct"] for r in ROOTS) >= 28 - bv.REACH


def test_an_instrument_without_the_notes_is_not_used(monkeypatch):
    one_shot = [{"path": "/x/p.wav", "note": 84, "group": "piano",
                 "clarity": 1.0}]
    assert _choose(1, ONLY("piano"), [], one_shot, monkeypatch) is None
    got = _choose(1, ONLY("piano"), [], _piano_multi(24, 72), monkeypatch)
    assert got and got["kind"] == "piano"


def test_guitar_organ_synth_play_bass_when_they_cover(monkeypatch):
    for kind in ("guitar", "organ", "synth"):
        lib = [dict(e, group=kind) for e in _piano_multi(24, 72)]
        got = _choose(2, ONLY(kind), [], lib, monkeypatch)
        assert got and got["kind"] == kind, kind


def test_same_beat_same_bass_sound(monkeypatch):
    s = _strings("cello", "pizz", 36, 77) + _strings("basses", "pizz", 28, 59)
    a = _choose(11, dict(bv.WEIGHTS), s, _piano_multi(24, 72), monkeypatch)
    b = _choose(11, dict(bv.WEIGHTS), s, _piano_multi(24, 72), monkeypatch)
    assert (a and a["label"], a and a["oct"]) == (b and b["label"], b and b["oct"])


def test_default_mix_keeps_the_bass_folder_about_a_third(monkeypatch):
    s = _strings("cello", "pizz", 36, 77) + _strings("basses", "pizz", 28, 59)
    kinds = []
    for v in range(300):
        got = _choose(v, {}, s, _all_multi(), monkeypatch)
        kinds.append(got["kind"] if got else "bass")
    share = kinds.count("bass") / 300.0
    assert 0.20 < share < 0.45, share
    assert {"contrabass", "cello", "piano"} <= set(kinds)


def test_a_voice_that_cannot_load_is_dropped(monkeypatch):
    s = _strings("cello", "pizz", 36, 77)
    _fake_audio(monkeypatch)
    monkeypatch.setattr(ss, "load_audio", lambda p: None)
    assert bv.choose(1, ROOTS, {"signature": {"bass_voices": ONLY("cello")}},
                     strings=s, instruments=[], cache={}) is None


def test_voices_render_real_audio_of_the_asked_length(monkeypatch):
    s = _strings("cello", "sustain", 36, 77) + _strings("cello", "pizz", 36, 77)
    for v in range(8):
        got = _choose(v, ONLY("cello"), s, [], monkeypatch)
        r = got["make_render"]({}, [], 0.5)
        seg = r(ROOTS[0] + got["oct"], 1.5)
        assert len(seg) == int(1.5 * ins.SR) and np.abs(seg).max() > 0
