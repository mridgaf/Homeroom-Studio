"""Original side = MIDI chords played on his sound packs (owner 2026-10-24).

Every identity whose Original settings are built carries chord odds of
midi 75 / loop 10 / sound packs 15. MIDI notes play on the identity's own
researched instruments, never bell or pluck; when none of those reach the
notes, the London strings play them (beat_machine._build_chords,
midi_voice_flow 1, new beats only)."""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import instrument_sampler as ins  # noqa: E402

# add a name here when its Original settings are built (TRACKER.md)
ORIGINAL_BUILT = {
    "legends_config.json": ["Doc Day", "DJ Hint"],
    "genres_config.json": ["G-Funk", "Acid Rap Bright", "Horror Rap",
                           "Crunk", "Chiptune", "Baltimore Club",
                           "Acid Rap Detroit"],
    "crew_config.json": ["Cutz", "Chrome Dial", "Crate Prophet"],
}


def test_original_builds_are_mostly_midi():
    for f, names in ORIGINAL_BUILT.items():
        d = json.load(open(str(ROOT / f)))
        for n in names:
            cs = dict(d[n]["signature"]["chord_source"])
            tot = sum(cs.values())
            assert abs(cs["midi"] / tot - 0.75) < 0.005, n
            assert abs(cs.get("loop", 0) / tot - 0.10) < 0.005, n


def _idx(groups, notes=range(36, 90, 2)):
    return [{"group": g, "note": n} for g in groups for n in notes]


def test_midi_never_plays_bell_or_pluck():
    idx = _idx(["bell", "pluck", "piano"])
    allow = [(("bell",), 5), (("pluck", "synth"), 5), (("piano",), 1)]
    for seed in range(50):
        got = ins.midi_groups_for(idx, [48, 52, 55], random.Random(seed), allow)
        assert got and got[0] == "piano"
        assert not set(got) & {"bell", "pluck"}


def test_midi_plays_only_the_researched_instruments():
    idx = _idx(["piano", "guitar", "organ", "synth"])
    allow = [(("piano",), 3), (("guitar",), 1)]
    firsts = {ins.midi_groups_for(idx, [48, 52, 55], random.Random(s), allow)[0]
              for s in range(80)}
    assert firsts == {"piano", "guitar"}


def test_nothing_reaches_the_notes_means_strings():
    idx = _idx(["piano"], notes=[40])          # one far-away piano sample
    assert ins.midi_groups_for(idx, [70, 74], random.Random(1),
                               [(("piano",), 1)]) == ()


def test_zero_weight_instrument_never_plays_midi():
    idx = _idx(["piano", "guitar"])
    allow = [(("piano",), 0), (("guitar",), 1)]
    for s in range(30):
        got = ins.midi_groups_for(idx, [48], random.Random(s), allow)
        assert got == ("guitar",)


def test_new_beats_are_stamped_old_beats_are_not():
    src = (ROOT / "tools" / "beat_machine.py").read_text()
    assert 'preset.setdefault("midi_voice_flow", 1)' in src
    assert 'if preset.get("midi_voice_flow"):' in src


def test_daily_drift_never_moves_midi_loop_or_a_zeroed_sound():
    import copy
    import evolution
    d = json.load(open(str(ROOT / "crew_config.json")))
    p = copy.deepcopy(d["Cutz"])
    p["signature"]["chord_source"].append(["chip", 0])
    for seed in range(200):
        q = copy.deepcopy(p)
        got = evolution._op_chord_voice(q, "Cutz", random.Random(seed))
        cs = dict(q["signature"]["chord_source"])
        assert cs["midi"] == 75 and cs["loop"] == 10 and cs["chip"] == 0
        assert got is not None
