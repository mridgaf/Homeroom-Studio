"""bass_rhythm: the bass performance grammar (2026-10-19). Pure checks --
no library, no drive: notes are voiced by a fake sine-free buffer."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import bass_rhythm as br  # noqa: E402
import groove  # noqa: E402

FILE_NOTE = 33          # A1, where his bass files sit
KICK = ["X-----x---X-----", "X-------x-x---x-"]
SCALE = (9, 11, 0, 2, 4, 5, 7)      # A minor


def fits(n):
    return abs(n - FILE_NOTE) <= 12


def _slots(roots=(33, 29, 36, 31), bars=(2, 2, 1, 3)):
    out, at = [], 0
    for r, b in zip(roots, bars):
        out.append({"root": r, "chord_root": r + 24,
                    "tones": [r + 24, r + 27, r + 31], "bars": b,
                    "start_bar": at})
        at += b
    return out


def _plan(fam="soul_jazz", variant=7, kick=KICK, slots=None):
    spec = br.spec_for({"signature": {"chord_family": fam}})
    return br.plan_line(slots or _slots(), kick, spec, variant, fits,
                        SCALE)


def test_same_seed_same_plan():
    assert _plan(variant=11) == _plan(variant=11)


def test_every_slot_starts_on_its_root_unless_tied():
    for fam in br.FAMILY:
        for v in range(60):
            slots = _slots()
            for s, p in zip(slots, _plan(fam, v, slots=slots)):
                if p["tied"]:
                    assert (0, 0) not in [(h[0], h[1]) for h in p["hits"]]
                else:
                    b, st, ch, note = p["hits"][0]
                    assert (b, st, ch, note) == (0, 0, "X", s["root"])


def test_monophonic_one_hit_per_cell_and_in_order():
    for fam in br.FAMILY:
        for v in range(40):
            for p in _plan(fam, v):
                cells = [(h[0], h[1]) for h in p["hits"]]
                assert cells == sorted(set(cells))


def test_every_note_within_an_octave_of_the_file():
    for fam in br.FAMILY:
        for v in range(80):
            for s, p in zip(_slots(), _plan(fam, v)):
                for _b, _st, _ch, note in p["hits"]:
                    assert abs(note - FILE_NOTE) <= 12 or note == s["root"]


def test_walk_approach_is_a_half_step_from_the_next_root_and_wraps():
    seen_wrap = 0
    for v in range(300):
        slots = _slots()
        plan = _plan("soul_jazz", v, slots=slots)
        for i, p in enumerate(plan):
            if p["figure"] != "walk":
                continue
            last = slots[i]["bars"] - 1
            a = [h for h in p["hits"] if (h[0], h[1]) == (last, 12)]
            nxt = slots[(i + 1) % len(slots)]["root"]
            assert len(a) == 1 and abs(a[0][3] - nxt) == 1
            seen_wrap += i == len(slots) - 1
    assert seen_wrap, "no walk ever landed on the last slot"


def test_push_ties_into_the_next_slot_and_wraps():
    seen = 0
    for v in range(300):
        slots = _slots()
        plan = _plan("dreamy", v, slots=slots)
        for i, p in enumerate(plan):
            if p["figure"] != "push":
                continue
            nxt = (i + 1) % len(slots)
            last = slots[i]["bars"] - 1
            b, st, _ch, note = p["hits"][-1]
            assert (b, st >= 14, note) == (last, True, slots[nxt]["root"])
            assert plan[nxt]["tied"]
            seen += nxt == 0
    assert seen


def test_levels_only_come_from_the_written_characters():
    allowed = set("Xxo.")
    for fam in br.FAMILY:
        for v in range(40):
            for p in _plan(fam, v):
                assert {h[2] for h in p["hits"]} <= allowed


@pytest.mark.parametrize("fam", sorted(br.FAMILY))
def test_each_family_plays_at_least_four_figures(fam):
    figs = {p["figure"] for v in range(100) for p in _plan(fam, v)}
    assert len(figs) >= 4, (fam, figs)


def test_missing_kick_lane_does_not_crash():
    spec = {"figures": [["kick", 1]]}
    plan = br.plan_line(_slots(), None, spec, 3, fits, SCALE)
    assert all(p["hits"] for p in plan if not p["tied"])
    feel = br.kick_feel({}, 1)
    assert feel.swing == 50


def test_unknown_family_gets_house_default():
    assert br.spec_for({})["figures"] == br.DEFAULT
    own = {"signature": {"chord_family": "dark",
                         "bass_grammar": {"figures": [["walk", 1]]}}}
    assert br.spec_for(own)["figures"] == [["walk", 1]]


def test_render_is_one_note_at_a_time_and_loop_length():
    slots = _slots()
    plan = _plan("bright_funk", 5, slots=slots)
    bar_s, sr = 2.0, 1000
    loop_n = int(round(sum(s["bars"] for s in slots) * bar_s * sr))
    calls = []

    def note(n, secs):
        calls.append(secs)
        return np.ones(int(secs * sr))

    feel = groove.LaneFeel(0, 0, 50, seed=1)
    out, notes = br.render_line(plan, slots, bar_s, 120, loop_n, note,
                                feel, sr=sr)
    assert len(out) == loop_n
    # every note is cut at the next one: the buffer never stacks above
    # the loudest single level (1.0 for an X)
    assert out.max() <= 1.0 + 1e-9
    starts = sorted(t for ns in notes for t, *_ in ns)
    assert len(starts) == sum(len(p["hits"]) for p in plan)


def test_render_gives_up_when_even_the_root_cannot_be_voiced():
    slots = _slots()
    feel = groove.LaneFeel(0, 0, 50, seed=1)
    out, notes = br.render_line(_plan(slots=slots), slots, 2.0, 120, 8000,
                                lambda n, s: None, feel, sr=1000)
    assert out is None and notes is None
