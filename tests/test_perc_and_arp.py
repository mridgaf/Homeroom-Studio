"""Owner 2026-10-19: "this consistent arpeggio thing in almost every beat",
and percussion "loud and intrusive ... very similar or repetitive".
His picks: arps rarer + varied, perc capped by how loud it SOUNDS, and the
research rebuild for perc + guest patterns. All on new beats only."""
import copy
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import chord_rhythm  # noqa: E402
import crew  # noqa: E402
import pattern_gen  # noqa: E402
from crew import CREW, SR, normalize_preset, render_crew_beat  # noqa: E402


# ------------------------------------------------------------------ arp

def _arp_share(name, flow):
    q = normalize_preset(json.loads(json.dumps(CREW[name])))
    q["chord_flow"] = 1
    if flow:
        q["arp_flow"] = 1
    return chord_rhythm._share(chord_rhythm.spec_for(q)["figures"], "arp")


def test_arp_flow_caps_every_identity_at_15_percent():
    assert _arp_share("Cutz", False) > 0.45          # was 50%
    for name in CREW:
        q = normalize_preset(json.loads(json.dumps(CREW[name])))
        q.update(chord_flow=1, arp_flow=1)
        spec = chord_rhythm.spec_for(q)
        if spec:
            assert chord_rhythm._share(spec["figures"], "arp") <= \
                chord_rhythm.ARP_MAX + 1e-3, name


def test_arp_bars_vary_and_rest_at_the_phrase_tail():
    rng = random.Random(5)
    seen = set()
    for _ in range(40):
        bars = chord_rhythm.arp_bars(rng, 4, 0.18)
        for b, bar in enumerate(bars):
            if b % 2 == 1:
                assert bar[8:] == "-" * 8, bar
        assert bars[0][0] == "X"
        seen.update(bars)
    assert len(seen) > 8                              # not one fixed bar


def test_arp_notes_ring_to_the_next_hit():
    lens = []
    chord_rhythm.render_figure(
        ["X--x--x-x--x--x-"], 2.0, 120, [60, 64, 67],
        lambda n, d: lens.append(d) or np.ones(8), lambda ns, d: None,
        figure="arp", shape="up", spec=dict(chord_rhythm.DEFAULT,
                                            arp_flow=True))
    six = 60.0 / 120 / 4
    assert len(set(round(x / six, 2) for x in lens)) > 1   # varied lengths


# ------------------------------------------------------------ percussion

def test_a_weighting_hears_mids_over_lows():
    t = np.arange(SR) / SR
    def db(f):
        return 20 * np.log10(np.std(crew.a_weighted(np.sin(2 * np.pi * f * t)))
                             / np.std(np.sin(2 * np.pi * f * t)))
    assert abs(db(1000)) < 0.3
    assert -21 < db(100) < -17                        # IEC 61672: -19.1


def _loud(x):
    n = int(crew.LOUD_WINDOW_S * SR)
    c = np.concatenate([[0.0], np.cumsum(np.concatenate([x, x[:n]]) ** 2)])
    return np.sqrt((c[n:] - c[:-n]).max() / n)


def _perc_vs_hat(monkeypatch, flow):
    monkeypatch.setattr(crew, "TRUE_LEVELS", True)
    p = copy.deepcopy(CREW["Cutz"])
    p["space"] = ("dry", [])
    p["sidechain"] = 0.0
    p["kit"]["perc"] = ("perc", None, [], 0.5)
    p["lanes"] = {"kick": (0.0, 1.0, (0, 0, 50, 1), ["X-------X-------"]),
                  "hat": (0.0, 1.0, (0, 0, 50, 2), ["x-x-x-x-x-x-x-x-"]),
                  "perc": (0.0, 1.0, (0, 0, 50, 3), ["--x---x---x---x-"])}
    if flow:
        p["perc_flow"] = 1
    t = np.arange(SR // 10) / SR
    env = np.exp(-t * 40)
    kit = {"kick": np.sin(2 * np.pi * 60 * t) * env,
           "hat": 0.05 * np.sin(2 * np.pi * 3000 * t) * env,
           "perc": 0.6 * np.sin(2 * np.pi * 3000 * t) * env}
    _L, _R, _lufs, parts = render_crew_beat("Cutz", kit, preset=p,
                                            want_parts=True)
    st = {ln: sum(parts["stems"][ln]) / 2 for ln in ("hat", "perc")}
    return 20 * np.log10(_loud(crew.a_weighted(st["perc"]))
                         / _loud(crew.a_weighted(st["hat"])))


def test_perc_sounds_quieter_than_the_hat(monkeypatch):
    assert _perc_vs_hat(monkeypatch, False) > 3       # loud before
    assert _perc_vs_hat(monkeypatch, True) <= crew.EXTRA_CUT_DB + 0.2


def test_perc_bars_answer_the_kit_and_leave_the_phrase_tail():
    busy = {0, 4, 8, 12}
    rng = random.Random(11)
    for _ in range(50):
        bars = pattern_gen.perc_bars(rng, 8, busy)
        for i, bar in enumerate(bars):
            assert len(bar) == 16
            if i % 4 == 3:                            # hole or late answer
                assert all(c in "-o" for c in bar[8:12]) and \
                    bar[8:12] == "----" and bar[12:].count("o") <= 2
        a = bars[0]
        assert a.count("x") == 1                      # one hit leads
        assert not ({i for i, c in enumerate(a) if c != "-"} & {0})
        assert len(set(bars)) > 1                     # not one bar x8


def test_guest_perc_lanes_use_the_new_writer(monkeypatch, tmp_path):
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "h.json")
    got = 0
    for v in range(30):
        q = normalize_preset(json.loads(json.dumps(CREW["Otto Grit"])))
        notes = pattern_gen.compose(q, "Otto Grit", 7000 + v)
        got += sum("(perc)" in n for n in notes)
    assert got > 0
