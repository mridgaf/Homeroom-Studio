"""melody_rhythm: the answer melody (2026-10-19). Pure checks -- no
library, no drive: notes are voiced by a fake buffer."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import groove  # noqa: E402
import melody_rhythm as mr  # noqa: E402

SCALE = (9, 11, 0, 2, 4, 5, 7)      # A minor
FAMILIES = list(mr.FAMILY) + [None]


def _slots(roots=(57, 53, 60, 55), bars=(1, 1, 1, 1)):
    out, at = [], 0
    for r, b in zip(roots, bars):
        tones = [r, r + 3 if r % 12 in (9, 2, 4) else r + 4, r + 7]
        out.append({"tones": tones, "top": max(tones), "bars": b,
                    "start_bar": at})
        at += b
    return out


def _plan(fam="soul_jazz", variant=7, slots=None, nbars=4, cells=None):
    spec = mr.spec_for({"signature": {"chord_family": fam}})
    return mr.plan_phrase(slots or _slots(), SCALE, spec, variant, nbars,
                          cells)


def _all(nbars=4):
    for fam in FAMILIES:
        for v in range(150):
            yield fam, v, _plan(fam, v, nbars=nbars)


def test_same_seed_same_plan():
    assert _plan(variant=11) == _plan(variant=11)
    assert _plan(variant=11) != _plan(variant=12)


def test_every_note_in_key_or_a_chord_tone():
    sl = _slots()
    tones = {t % 12 for s in sl for t in s["tones"]}
    for fam, v, hits in _all():
        for b, st, ch, n in hits:
            assert n % 12 in set(SCALE) | tones, (fam, v, n)


def test_strong_beats_take_a_chord_tone():
    sl = _slots()
    for fam, v, hits in _all():
        for b, st, ch, n in hits:
            if st in mr.STRONG:
                assert n % 12 in {t % 12 for t in mr._slot_at(
                    sl, b)["tones"]}, (fam, v, b, st, n)


def test_loop_ends_on_a_chord_tone_of_bar_one():
    sl = _slots()
    first = {t % 12 for t in sl[0]["tones"]}
    for fam, v, hits in _all():
        assert hits[-1][3] % 12 in first or hits[-1][0] % 2 == 0, (fam, v)


@pytest.mark.parametrize("nbars", [2, 4, 8])
def test_at_least_one_silent_bar_per_four(nbars):
    for fam, v, hits in _all(nbars):
        used = {b for b, _, _, _ in hits}
        for g in range(0, nbars, 4):
            grp = set(range(g, min(g + 4, nbars)))
            assert grp - used, (fam, v, nbars, used)


def test_sparse_never_every_sixteenth():
    for fam, v, hits in _all():
        per_bar = {}
        for b, st, _, _ in hits:
            per_bar[b] = per_bar.get(b, 0) + 1
        assert max(per_bar.values()) <= 6
        assert len(hits) <= 14


def test_at_most_one_leap_per_phrase():
    for fam, v, hits in _all():
        by_bar = {}
        for b, st, ch, n in hits:
            by_bar.setdefault(b, []).append(n)
        for b, ns in by_bar.items():
            leaps = sum(abs(x - y) > mr.STEP_MAX for x, y in zip(ns, ns[1:]))
            assert leaps <= 1, (fam, v, b, ns)


def test_melody_always_above_the_chords_and_lead():
    sl = _slots()
    top = max(s["top"] for s in sl)
    for fam, v, hits in _all():
        assert min(n for _, _, _, n in hits) > top, (fam, v)


def test_instrument_shift_stays_above_floor():
    idx = [{"group": "bell", "multi": "Glock", "art": "a", "note": n,
            "path": "g%d" % n} for n in range(40, 110, 3)]
    ents, sh = mr.pick_instrument(idx, [70, 72, 74], (), 1, floor=80)
    assert ents and min(70, 72, 74) + sh > 80
    ents, _ = mr.pick_instrument(idx[:5], [70, 72], (), 1, floor=80)
    assert ents is None                  # nothing recorded that high


def test_never_on_bar_one_downbeat():
    for fam, v, hits in _all():
        assert (0, 0) not in {(b, st) for b, st, _, _ in hits}


def test_dark_is_sparser_than_bright_funk():
    n = {f: sum(len(_plan(f, v)) for v in range(200))
         for f in ("dark", "bright_funk")}
    assert n["dark"] < n["bright_funk"]


def test_motif_answered_with_same_rhythm():
    for v in range(60):
        hits = _plan("dreamy", v)
        call = [st for b, st, _, _ in hits if b == 1]
        resp = [st for b, st, _, _ in hits if b == 3]
        assert call == resp, v


def test_melody_grammar_override():
    spec = mr.spec_for({"signature": {"chord_family": "dark",
                                      "melody_grammar": {"notes": [5, 5]}}})
    assert spec["notes"] == [5, 5]


def test_about_half_of_beats_play():
    n = sum(mr.plays(v) for v in range(2000))
    assert 850 < n < 1150


def _idx():
    return ([{"group": "bell", "multi": "Glock", "art": "a", "note": n,
              "path": "glock%d" % n} for n in range(60, 97, 3)]
            + [{"group": "piano", "multi": "Grand", "art": "p", "note": n,
                "path": "grand%d" % n} for n in range(30, 100, 3)]
            + [{"group": "synth", "note": 40, "path": "lone_synth"}])


def test_instrument_is_one_instrument_and_covers_every_note():
    notes = [n for _, _, _, n in _plan(variant=3)]
    ents, shift = mr.pick_instrument(_idx(), notes, (), 3)
    assert len({(e.get("multi"), e.get("art")) for e in ents}) == 1
    assert all(any(abs(e["note"] - (n + shift)) <= mr.MAX_SHIFT
                   for e in ents) for n in notes)


def test_instrument_avoids_the_chords_family():
    notes = [n for _, _, _, n in _plan(variant=3)]
    for v in range(30):
        ents, _ = mr.pick_instrument(_idx(), notes, ("piano",), v)
        assert ents[0]["group"] != "piano"


def test_no_instrument_means_no_melody():
    ents, _ = mr.pick_instrument(
        [{"group": "synth", "note": 40, "path": "x"}], [100, 102], (), 1)
    assert ents is None


def test_render_levels_only_from_characters_and_monophonic():
    hits = _plan("bright_funk", 5)
    sr, bar_s = 1000, 2.0
    loop_n = int(4 * bar_s * sr)
    got = []

    def note(n, secs):
        got.append(secs)
        return np.ones(max(int(secs * sr), 1))

    out, notes = mr.render_line(hits, bar_s, 120, loop_n, note,
                                groove.LaneFeel(0, 0, 50, seed=1), sr=sr)
    assert len(out) == loop_n
    for (b, st, ch, n), (t, d, nn, lvl) in zip(hits, notes):
        assert lvl == groove.velocity(ch, st, None)
    ts = sorted((t, d) for t, d, _, _ in notes)
    for (t1, d1), (t2, _) in zip(ts, ts[1:]):
        assert t1 + d1 <= t2 + 1e-9


def test_render_unvoiceable_gives_none():
    out, notes = mr.render_line(_plan(), 2.0, 120, 8000,
                                lambda n, s: None,
                                groove.LaneFeel(0, 0, 50, seed=1), sr=1000)
    assert out is None and notes is None


def test_no_kick_or_hat_lane_feel_does_not_crash():
    f = mr.feel_for({}, 3)
    assert f.hit_time(0.0, 4, 90) >= 0


def test_melody_lane_is_its_own_rack_row():
    import beat_machine as bm
    assert bm._chord_family("melody0") == "melody"
    lanes = {"chord0": 1, "chord1": 1, "bass0": 1, "melody0": 1, "kick": 1}
    assert bm._family_members("melody", lanes) == ["melody0"]
    assert sorted({"chords", "melody", "chordbass"}, key=bm._fam_sort) == [
        "chords", "melody", "chordbass"]


def test_midi_gets_a_melody_track_on_channel_3(tmp_path):
    import beat_recipes
    p = tmp_path / "m.mid"
    beat_recipes.write_midi(p, {}, 90, chords=[
        {"start_sec": 0.0, "dur_sec": 2.0, "notes": [60, 64, 67],
         "melody_line": [(0.5, 0.25, 76, 100), (1.0, 0.5, 74, 90)]}])
    b = p.read_bytes()
    assert b"melody" in b and bytes([0x92, 76, 100]) in b
    q = tmp_path / "n.mid"
    beat_recipes.write_midi(q, {}, 90, chords=[
        {"start_sec": 0.0, "dur_sec": 2.0, "notes": [60, 64, 67]}])
    assert b"melody" not in q.read_bytes()


def test_steps_keep_direction_and_leaps_go_up_then_back():
    same = turn = up_back = leaps = 0
    for fam, v, hits in _all():
        by_bar = {}
        for b, st, ch, n in hits:
            by_bar.setdefault(b, []).append(n)
        for ns in by_bar.values():
            iv = [y - x for x, y in zip(ns, ns[1:])]
            for a, b in zip(iv, iv[1:]):
                if abs(a) > mr.STEP_MAX:
                    leaps += 1
                    up_back += a > 0 and b < 0
                elif a and b and abs(b) <= mr.STEP_MAX:
                    same += (a > 0) == (b > 0)
                    turn += (a > 0) != (b > 0)
    assert same > turn                   # inertia
    assert leaps and up_back / leaps > 0.8
