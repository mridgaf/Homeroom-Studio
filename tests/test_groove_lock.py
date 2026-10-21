"""groove_lock: drums, bass and chords as one groove (2026-10-20). Pure
checks -- no library, no drive."""
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import bass_rhythm as br  # noqa: E402
import chord_rhythm as cr  # noqa: E402
import groove  # noqa: E402
import groove_lock as gl  # noqa: E402

BUSY = "X-x-X-x-X-x-X-x-"      # 8 hits
SPACE = "X-------x-------"     # 2 hits
KICK = [BUSY, "X---x-x---X---x-", SPACE, SPACE]
SCALE = (9, 11, 0, 2, 4, 5, 7)


def fits(n):
    return abs(n - 33) <= 12


def _slots():
    out, at = [], 0
    for r, b in zip((33, 29, 36), (2, 1, 1)):
        out.append({"root": r, "chord_root": r + 24,
                    "tones": [r + 24, r + 27, r + 31], "bars": b,
                    "start_bar": at})
        at += b
    return out


def _plan(v, fam="bright_funk"):
    spec = br.spec_for({"signature": {"chord_family": fam}})
    slots = _slots()
    plan = br.plan_line(slots, KICK, spec, v, fits, SCALE)
    return slots, gl.lock_bass(plan, slots, KICK, v, fits)


def test_loads():
    assert gl.load(BUSY) == "busy"
    assert gl.load(SPACE) == "space"
    assert gl.load("X---x-x---X---x-") == "mid"


def test_busy_kick_bar_keeps_bass_simple_and_on_the_kick():
    for v in range(60):
        for fam in ("bright_funk", "grit", "soul_jazz"):
            slots, plan = _plan(v, fam)
            hits = [h for h in plan[0]["hits"] if h[0] == 0]   # loop bar 0
            assert len(hits) <= gl.BASS_CAP
            assert all(h[1] == 0 or BUSY[h[1]] != "-" for h in hits)


def test_no_bass_note_a_16th_off_the_kick():
    for v in range(60):
        slots, plan = _plan(v, "bright_funk")
        for s, p in zip(slots, plan):
            for b, st, _ch, _n in p["hits"]:
                kb = KICK[(s["start_bar"] + b) % 4]
                pushed = b == s["bars"] - 1 and st >= 13
                if st and not pushed and kb[st] == "-":
                    assert not ({st - 1, st + 1}
                                & {i for i, c in enumerate(kb) if c != "-"})


def test_space_bars_sometimes_hold_sometimes_move():
    held = moved = 0
    for v in range(80):
        _slots_, plan = _plan(v, "soul_jazz")
        bar3 = [h for h in plan[2]["hits"] if h[0] == 0]     # loop bar 3
        held += len(bar3) <= 1
        moved += any(h[1] == 14 and h[2] == "o" for h in bar3)
    assert held and moved


def test_same_seed_same_lock():
    assert _plan(9) == _plan(9)


def test_short_note_leaves_a_rest():
    slots = [{"root": 33, "chord_root": 57, "tones": [57, 60, 64],
              "bars": 1, "start_bar": 0}]
    plan = [{"figure": "hold", "tied": False,
             "hits": [(0, 0, "X", 33), (0, 8, "x", 33)]}]
    feel = groove.LaneFeel(0, 0, 50, seed=1)
    sr, bar_s = 1000, 2.0
    def note(n, secs):
        return np.ones(int(secs * sr))
    out, notes = br.render_line(plan, slots, bar_s, 120, int(bar_s * sr),
                                note, feel, sr=sr)
    assert abs(notes[0][1][1] - 1.0) < 0.01          # rings to the loop end
    plan[0]["short"] = {(0, 8): 2}
    out, notes = br.render_line(plan, slots, bar_s, 120, int(bar_s * sr),
                                note, feel, sr=sr)
    assert abs(notes[0][1][1] - 0.25) < 0.01         # 2 16ths, then rest
    assert out[int(1.5 * sr)] == 0


def test_chords_stay_off_a_busy_kick_and_never_go_empty():
    bars = ["X-x-X-x-X-x-X-x-", "-x-x-x-x-x-x-x-x"]
    for v in range(40):
        got, _long = gl.lock_chords(bars, 0, [BUSY, BUSY],
                                    random.Random(v))
        first = [k for k, c in enumerate(got[0]) if c != "-"]
        assert 0 in first                       # the chord change stays
        for g in got:
            hits = [k for k, c in enumerate(g) if c != "-"]
            assert hits and len(hits) <= gl.CHORD_CAP
        assert all(BUSY[k] == "-" for k, c in enumerate(got[1]) if c != "-")


def test_chords_may_sustain_in_space():
    longs = 0
    for v in range(40):
        got, long = gl.lock_chords(["X-------x-------"], 0, [SPACE],
                                   random.Random(v))
        assert got == ["X-------x-------"]
        longs += bool(long)
    assert 0 < longs < 40


def test_invert_keeps_the_chord():
    assert gl.invert([57, 60, 64]) == [60, 64, 69]
    assert {n % 12 for n in gl.invert([57, 60, 64, 67])} == {9, 0, 4, 7}


def test_second_bar_plays_the_new_voicing():
    seen = []

    def chord(notes, secs):
        seen.append(tuple(notes))
        return np.ones(10)
    cr.render_figure(["X-------", "X-------"], 4.0, 120, [57, 60, 64],
                     lambda n, s: None, chord, figure="stab",
                     spec=dict(cr.DEFAULT, groove_flow=True))
    assert seen == [(57, 60, 64), (60, 64, 69)]
    seen.clear()
    cr.render_figure(["X-------", "X-------"], 4.0, 120, [57, 60, 64],
                     lambda n, s: None, chord, figure="stab",
                     spec=dict(cr.DEFAULT))
    assert seen == [(57, 60, 64), (57, 60, 64)]       # old beats unchanged
