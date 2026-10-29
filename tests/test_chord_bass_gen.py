"""The genre chord + bass generators and written loud/soft (2026-10-29)."""
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import bass_gen                                    # noqa: E402
import bass_rhythm                                 # noqa: E402
import chord_gen                                   # noqa: E402
import chord_rhythm                                # noqa: E402
import dynamics                                    # noqa: E402
import harmony                                     # noqa: E402
from key_context import CHORDS, KeyContext         # noqa: E402


def test_every_identity_has_styles_in_the_table():
    assert chord_gen.tables(), "chord_tables.json missing"
    for who in chord_gen.STYLE_FOR:
        assert chord_gen.styles_for(who), who


def test_generated_loops_are_playable_varied_and_seeded():
    key = KeyContext("F", "minor")
    seen = set()
    for i in range(200):
        g = chord_gen.generate(chord_gen.styles_for("Cutz"), "minor",
                               random.Random(i))
        assert 2 <= len(g["chords"]) <= 4
        assert all(q in CHORDS for _o, q in g["chords"])
        roots = [o for o, _q in g["chords"]]
        assert len(set(roots)) == len(roots)
        assert harmony.compose_chords(key, g["chords"])
        seen.add(str(g["chords"]))
    assert len(seen) >= 100          # the old lists gave an identity ~6
    a = chord_gen.generate({"trap": 1}, "minor", random.Random(5))
    assert a == chord_gen.generate({"trap": 1}, "minor", random.Random(5))


def test_bass_gen_entries_play_through_the_pattern_path():
    slot = {"root": 41, "chord_root": 53, "tones": [53, 56, 60],
            "bars": 2, "start_bar": 0}
    for style in bass_gen.STYLES:
        e = bass_gen.make(style, random.Random(1), ["X-----x---X-----"])
        hits = bass_rhythm._pattern_hits(e, slot, 2, -2, [3, 7],
                                         lambda n: True)
        assert hits and hits[0][:3] == (0, 0, "X")


def test_old_bass_flow_never_rolls_gen():
    spec = bass_rhythm.spec_for({"bass_flow": 2})
    assert all(f != "gen" for f, _w in spec["figures"])
    spec = bass_rhythm.spec_for({"bass_flow": 3,
                                 "chord_gen": {"style": "funk"}})
    assert any(f == "gen" for f, _w in spec["figures"])
    assert spec["style"] == "funk"


def test_levels_have_a_floor_and_a_shape():
    for shape in dynamics.SHAPES:
        lv = [dynamics.level(c, s, shape) for c in "Xxo." for s in range(16)]
        assert min(lv) >= dynamics.FLOOR - 1e-9
        assert max(lv) <= 1.0
        assert len(set(round(v, 3) for v in lv)) >= 4    # real loud/soft
    assert dynamics.level("X", 0, "boom_bap") > dynamics.level("x", 3, "boom_bap")
    assert dynamics.level("x", 2, "club") > dynamics.level("x", 4, "club")


def test_chord_figure_logs_hits_at_written_levels():
    notes = [60, 63, 67]
    tone = lambda n, d: np.ones(max(1, int(d * 44100)))        # noqa: E731
    log = []
    out = chord_rhythm.render_figure(
        ["X-x-x--.X---x-o-"], 2.0, 120, notes, tone,
        lambda ns, d: tone(ns[0], d), figure="stab",
        spec=dict(chord_rhythm.DEFAULT, dyn="boom_bap"), log=log)
    assert out is not None and len(log) == 7
    lv = [v for _t, _d, _n, v in log]
    assert max(lv) == 1.0 and min(lv) >= dynamics.FLOOR
    assert len(set(lv)) >= 3
