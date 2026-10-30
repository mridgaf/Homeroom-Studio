"""Loops side settings (owner rulings 2026-10-24, Handoffs/Loops Settings
Build.md): vocabulary steers picks, mood moves EQ/glue only, and loop beats
are fully clean whatever the identity's allow_dirt says."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import loop_vocab
from crew import SR, render_crew_beat
from sample_library import loops_scored


def test_listen_words_steer_toward_matching_loop_titles():
    pool = [{"name": "melody 1", "tokens": ["melody", "1"], "bpm": 90},
            {"name": "jazzy rhodes", "tokens": ["swing", "rhodes"], "bpm": 90}]
    groups = loop_vocab.groups_of(["smooth", "jazz", "piano"])
    best = loops_scored({"_loops": pool}, bpm=90, groups=groups)[0]
    assert best["name"] == "jazzy rhodes"      # jazz group + keys type


def test_boom_in_a_loop_title_is_hip_hop_not_808():
    assert loop_vocab.word_groups()["boom"] == "hip hop"


def test_one_mood_row_wins_and_identity_glue_wins():
    eq, glue = loop_vocab.finish(["dark", "lofi", "creepy"],
                                 {"high_db": 2.0}, {})
    assert eq == {"high_db": 0.0, "low_db": 2.0}   # dark/horror only
    assert glue["ratio"] == 2.2
    assert loop_vocab.finish(["trap"], {}, {"ratio": 4.0})[1]["ratio"] == 4.0


def test_swing_in_a_listen_line_is_groove_not_jazz(monkeypatch):
    import crew
    monkeypatch.setitem(crew.CREW, "Swinger", {"listen": "57% swing, hard"})
    assert "swing" not in loop_vocab.identity_words("Swinger")
    assert loop_vocab.word_groups()["swing"] == "jazz"   # titles still jazz


def _preset(**dirt):
    p = dict(num=1, bpm=120, kick_dist=0.0, dust=0.0, vinyl=0, wow=0.0,
             mix_sat=0.0, drive=1.0, sidechain=0.0, space=("dry", []),
             alt=None, lanes={
                 "kick": (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),)),
                 "chord0": (0.0, 1.0, (0.0, 0.0, 0.0, 0), (("x",),))})
    p.update(dirt)
    return p


def test_loop_beats_ignore_allow_dirt():
    n = int(round(2 * 2.0 * SR))
    sig = np.sin(np.linspace(0, 40 * np.pi, n)) * 0.3
    bufs = {"kick": (sig, sig), "chord0": (sig * 0.5, sig * 0.5)}
    clean = render_crew_beat("Test", kit={}, preset=_preset(),
                             loop_bufs=bufs, nbars_override=2)
    dirty = render_crew_beat(
        "Test", kit={}, loop_bufs=bufs, nbars_override=2,
        preset=_preset(allow_dirt=True, fx_stems=True, vinyl=-30, wow=0.3,
                       dust=0.5, mix_sat=2.0, kick_dist=0.5, drive=1.5))
    assert np.allclose(clean[0], dirty[0]) and np.allclose(clean[1], dirty[1])


def test_doc_day_loop_words_are_only_doc_days():
    """Loops side (2026-10-30): Doc Day's research backs ominous strings
    and a piano hook; no other identity carries these extra words."""
    assert {"dark", "piano", "strings"} <= set(loop_vocab.identity_words("Doc Day"))
    assert "dark" not in loop_vocab.identity_words("Cutz")
    assert loop_vocab._cfg()["Doc Day"]["words"] == ["rap", "dark", "piano", "strings"]


def test_every_identity_has_loop_words_and_none_are_dead():
    """Loops side (2026-10-30): all 45 identities carry a words block, and
    every word reaches a group or lead type, so none are silent."""
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    names = set()

    def walk(o):
        if isinstance(o, dict):
            for n, v in o.items():
                if isinstance(v, dict) and "listen" in v:
                    names.add(n)
                else:
                    walk(v)
    for f in ("crew_config.json", "legends_config.json", "genres_config.json"):
        walk(json.loads((root / f).read_text()))
    cfg = loop_vocab._cfg()
    live = set(loop_vocab.word_groups()) | {
        w for ws in cfg["_lead_types"].values() for w in ws}
    assert len(names) == 45
    for n in names:
        words = cfg[n]["words"]
        assert words and all(w in live for w in words), n
