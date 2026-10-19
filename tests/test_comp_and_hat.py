"""Owner 2026-10-19: hats "stand out more than I would like", and the stab /
chord / comp rhythms are "the same old ones". New beats only (stamps
`comp_flow`, `hat_flow`)."""
import copy
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import chord_rhythm  # noqa: E402
import crew  # noqa: E402
from crew import CREW, SR, normalize_preset, render_crew_beat  # noqa: E402

KICK_SNARE = {"kick": ["X-------X-------"], "snare": ["----X-------X---"],
              "hat": ["x-x-x-x-x-x-x-x-"]}


def _spec(flow):
    q = normalize_preset(json.loads(json.dumps(CREW["Otto Grit"])))
    q["chord_flow"] = 1
    if flow:
        q["comp_flow"] = 1
    return chord_rhythm.spec_for(q)


def _loop(spec, seed, nslots=4):
    """Four 1-bar chord slots, the case where the old code always played
    bar 1 of its pattern."""
    out = []
    for slot in range(nslots):
        rng = random.Random(seed * 733 + 97 + slot)
        out += chord_rhythm.gen_figure(spec, rng, 1, busy=KICK_SNARE,
                                       bar0=slot)[1]
    return out


def test_comp_flow_needs_its_stamp():
    assert "comp_flow" not in _spec(False)
    assert _spec(True)["comp_flow"]


def test_comp_has_its_own_words_and_dodges_the_snare():
    spec = dict(_spec(True), figures=[["comp", 1]])
    bars = [b for s in range(200) for b in _loop(spec, s)]
    assert len(set(bars)) >= 12
    on_snare = sum(b[4] != "-" or b[12] != "-" for b in bars) / len(bars)
    assert on_snare < 0.35


def test_phrase_shape_tail_rest_and_push():
    spec = dict(_spec(True), figures=[["stab", 1]])
    loops = [_loop(spec, s) for s in range(300)]
    push = sum(l[3][chord_rhythm.PUSH] != "-" for l in loops) / len(loops)
    assert push > 0.5                                  # bar 4 pushes
    tail = sum(all(c == "-" for c in l[1][8:]) for l in loops) / len(loops)
    assert tail > 0.3                                  # bar 2 rests late


def test_loop_varies_more_than_before():
    def distinct(flow):
        spec = dict(_spec(flow), figures=[["stab", 1]])
        return np.mean([len(set(_loop(spec, s))) for s in range(300)])
    assert distinct(True) > distinct(False)


def test_old_beats_unchanged_without_stamp():
    spec = _spec(False)
    a = chord_rhythm.gen_figure(spec, random.Random(5), 2, busy=KICK_SNARE)
    b = chord_rhythm.gen_figure(spec, random.Random(5), 2, busy=KICK_SNARE,
                                bar0=3)
    assert a == b


def test_comp_hits_ring_to_the_next_hit():
    lens = []
    chord_rhythm.render_figure(
        ["X-----x-------x-"], 2.0, 120, [60, 64, 67], lambda n, d: None,
        lambda ns, d: lens.append(d) or np.ones(8), figure="comp",
        shape="hold:3", spec=dict(chord_rhythm.DEFAULT, comp_flow=True))
    six = 60.0 / 120 / 4
    assert sorted(round(x / six / 0.9) for x in lens) == [2, 3, 3]


# ------------------------------------------------------------------ hats

def _loud(x):
    n = int(crew.LOUD_WINDOW_S * SR)
    c = np.concatenate([[0.0], np.cumsum(np.concatenate([x, x[:n]]) ** 2)])
    return np.sqrt((c[n:] - c[:-n]).max() / n)


def _hat_vs_snare(monkeypatch, flow):
    monkeypatch.setattr(crew, "TRUE_LEVELS", True)
    p = copy.deepcopy(CREW["Cutz"])
    p["space"] = ("dry", [])
    p["sidechain"] = 0.0
    p["lanes"] = {"kick": (0.0, 1.0, (0, 0, 50, 1), ["X-------X-------"]),
                  "snare": (0.0, 1.0, (0, 0, 50, 2), ["----X-------X---"]),
                  "hat": (0.0, 1.0, (0, 0, 50, 3), ["x-x-x-x-x-x-x-x-"])}
    if flow:
        p["hat_flow"] = 1
    t = np.arange(SR // 10) / SR
    env = np.exp(-t * 40)
    kit = {"kick": np.sin(2 * np.pi * 60 * t) * env,
           "snare": 0.3 * np.sin(2 * np.pi * 1500 * t) * env,
           "hat": 0.6 * np.sin(2 * np.pi * 3000 * t) * env}
    _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                            want_parts=True)
    st = {ln: sum(parts["stems"][ln]) / 2 for ln in ("hat", "snare")}
    return 20 * np.log10(_loud(crew.a_weighted(st["hat"]))
                         / _loud(crew.a_weighted(st["snare"])))


def test_hats_sound_quieter_than_the_snare(monkeypatch):
    assert _hat_vs_snare(monkeypatch, False) > 0       # loud before
    assert _hat_vs_snare(monkeypatch, True) <= crew.HAT_UNDER_DB + 0.3
