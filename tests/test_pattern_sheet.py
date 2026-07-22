"""The pattern sheet (owner request 2026-07-22): a readable picture of
every lane against the backbeat, saved beside each beat."""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import crew                                                      # noqa: E402
import pattern_gen                                               # noqa: E402
from crew import CREW                                            # noqa: E402
from pattern_sheet import sheet, write_sheet                     # noqa: E402


def _beat(name="Otto Grit", variant=7):
    p = copy.deepcopy(CREW[name])
    notes = pattern_gen.compose(p, name, variant)
    return p, notes


def test_sheet_shows_every_lane_and_bar():
    p, _ = _beat()
    text = sheet(p, "test beat")
    n = crew.bars_of(p)
    for b in range(n):
        assert "bar %d" % (b + 1) in text
    assert "bar %d" % (n + 1) not in text        # no bars that don't exist
    for lane in p["lanes"]:
        assert lane in text, lane


def test_sheet_calls_out_the_backbeat():
    """The whole point: he must be able to SEE which row is the frame."""
    p, _ = _beat()
    text = sheet(p)
    assert "<- backbeat" in text
    for line in text.splitlines():
        if "<- backbeat" in line:
            assert line.split()[0].rstrip("0123456789") in ("snare", "clap")


def test_sheet_header_reports_the_setup():
    p, _ = _beat()
    p["sidechain"] = 0.2
    text = sheet(p)
    head = text.splitlines()[0]
    assert "BPM" in head and "bars" in head
    assert "swing" in head and "duck" in head


def test_sheet_marks_a_fully_quantized_beat():
    p, _ = _beat()
    for k, (pan, gain, (o, j, sw, seed), bars) in list(p["lanes"].items()):
        p["lanes"][k] = (pan, gain, (0.0, 0.0, 50, seed), bars)
    assert "fully quantized" in sheet(p)


def test_mixed_resolution_lanes_line_up():
    """A 16th-grid kick under a 32nd-grid hat roll must print on ONE
    shared grid — otherwise the columns disagree and the picture lies
    about where hits land relative to each other."""
    p, _ = _beat()
    lanes = p["lanes"]
    k = list(lanes)[0]
    pan, gain, feel, bars = lanes[k]
    lanes[k] = (pan, gain, feel, ["X" + "-" * 31] * len(bars))   # 32-step
    text = sheet(p)
    rows = [ln for ln in text.splitlines()
            if ln.startswith("  ") and "<-" not in ln and "|" in ln]
    widths = {len(ln.split()[1]) for ln in rows if len(ln.split()) > 1}
    assert len(widths) == 1, widths


def test_quantized_label_requires_no_swing_too():
    """'Fully quantized' while swing is 52 is a contradiction."""
    p, _ = _beat()
    for k, (pan, gain, (o, j, sw, seed), bars) in list(p["lanes"].items()):
        p["lanes"][k] = (pan, gain, (0.0, 0.0, 52, seed), bars)
    assert "fully quantized" not in sheet(p)


def test_write_sheet_never_raises_on_a_broken_preset():
    """A picture failing to draw must never cost a render."""
    assert write_sheet("/nowhere/at/all/x.txt", {"lanes": {}}) is None
    assert write_sheet("/nowhere/at/all/x.txt", None) is None


def test_sheet_round_trips_to_disk(tmp_path):
    p, notes = _beat()
    out = tmp_path / "beat.txt"
    assert write_sheet(out, p, title="beat", extra=notes) is not None
    assert out.read_text() == sheet(p, "beat", notes)
