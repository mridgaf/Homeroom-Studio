import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import beat_machine as b


def test_collab_keeps_instruments_if_either_dj_has_them():
    with_chords = [n for n in b.CREW
                   if (b.CREW[n].get("signature") or {}).get("chords_default")]
    for v in range(6):
        p, notes = b.collab_preset(with_chords[:2], v, None)
        assert (p.get("signature") or {}).get("chords_default")
        assert any(n.startswith("harmony: ") for n in notes)
