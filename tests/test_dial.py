"""The dial: knob panel state, slider moves, one-step undo.

No MIDI, no Reason, no local model — a fake control surface stands in for all
three. What is NOT covered here, because nothing outside Reason can cover it:
whether Reason actually reports its knobs on lock. That check lives in the
manual steps at the bottom of DECISIONS.md.
"""
import asyncio

import pytest

from reason_voice.intents import parse
from reason_voice.server import DIAL_DEVICE, DEFAULT_SETTINGS, Session, WebApp
from reason_voice import dial_llm


class FakeControl:
    """Stands in for ReasonControl. Records what was sent; replays what
    'Reason' has reported, in the same shape the real class exposes."""

    def __init__(self, connected=True):
        self.connected = connected
        self.positions = {}
        self.displays = {}
        self.sent = []

    def poll(self):
        return 0

    def set_value(self, knob, value):
        if not self.connected:
            return False
        self.sent.append((knob, int(value)))
        return True

    def current(self, knob):
        if knob not in self.positions:
            return None
        name, shown = self.displays.get(knob, ("", ""))
        return self.positions[knob], name, shown

    # Reason told us about a knob
    def report(self, knob, pos, name, shown):
        self.positions[knob] = pos
        self.displays[knob] = (name, shown)


def app(connected=True):
    """A WebApp with only the dial's dependencies wired. Bypasses __init__ on
    purpose — the real one scans a 68k-file drive and opens MIDI ports."""
    a = object.__new__(WebApp)
    a.s = Session()
    a.settings = dict(DEFAULT_SETTINGS)
    a.status = "idle"
    a.feedback = ""
    a.clients = set()
    a.control = FakeControl(connected)
    a.dial_knobs = dial_llm.knob_map(DIAL_DEVICE)
    a.dial_cal = dial_llm.load_calibration()
    a.dial_undo = None

    async def _push(extra=None):
        pass

    a.push = _push
    return a


def run(a, command, **args):
    from reason_voice.intents import Intent
    asyncio.run(a.execute(Intent(command, args)))
    return a.feedback


# -- panel state -------------------------------------------------------------

def test_knob_names_come_from_the_remotemap():
    a = app()
    st = a.dial_state()
    assert st["device"] == DIAL_DEVICE
    assert len(st["knobs"]) == 8
    by_knob = {k["knob"]: k for k in st["knobs"]}
    assert by_knob["knob_5"]["param"] == "Attack"
    assert by_knob["knob_1"]["param"] == "Threshold"


def test_locked_is_false_until_reason_speaks():
    a = app()
    assert a.dial_state()["locked"] is False
    a.control.report("knob_5", 38, "Attack", "30 ms")
    assert a.dial_state()["locked"] is True


def test_reasons_own_name_wins_over_the_remotemap():
    """If Reason ever disagrees with the map, believe Reason — it is the one
    actually holding the parameter."""
    a = app()
    a.control.report("knob_5", 38, "Attack Time", "30 ms")
    row = {k["knob"]: k for k in a.dial_state()["knobs"]}["knob_5"]
    assert row["param"] == "Attack Time"
    assert row["shown"] == "30 ms"
    assert row["pos"] == 38


def test_slider_ends_are_the_measured_values():
    a = app()
    row = {k["knob"]: k for k in a.dial_state()["knobs"]}["knob_5"]
    assert row["lo"] == "1 ms" and row["hi"] == "100 ms"


# -- moving knobs ------------------------------------------------------------

def test_slider_move_sends_the_position():
    a = app()
    a.control.report("knob_5", 38, "Attack", "30 ms")
    run(a, "dial_set", knob="knob_5", value=96)
    assert a.control.sent == [("knob_5", 96)]


def test_undo_puts_it_back():
    a = app()
    a.control.report("knob_5", 38, "Attack", "30 ms")
    run(a, "dial_set", knob="knob_5", value=96)
    assert a.dial_undo["pos"] == 38
    run(a, "dial_undo")
    assert a.control.sent[-1] == ("knob_5", 38)
    assert a.dial_undo is None          # one slot, spent
    assert "Nothing to put back" in run(a, "dial_undo")


def test_nothing_moves_without_the_midi_bridge():
    a = app(connected=False)
    a.control.report("knob_5", 38, "Attack", "30 ms")
    assert "MIDI bridge not connected" in run(a, "dial_set", knob="knob_5",
                                              value=96)
    assert a.control.sent == []
    assert a.dial_undo is None          # nothing to undo if nothing moved


# -- the open-ended phrase ---------------------------------------------------

def test_unlocked_says_so_and_moves_nothing(monkeypatch):
    """Owner decision: no silent patch search, and no guessing at a knob when
    we cannot see where any of them sit."""
    called = []
    monkeypatch.setattr(dial_llm, "choose", lambda *a, **k: called.append(a))
    a = app()
    said = run(a, "dial", phrase="give it more punch")
    assert "Lock to ReasonVoice" in said
    assert a.control.sent == []
    assert called == []                 # the model is never even asked


def test_phrase_moves_the_knob_the_model_picked(monkeypatch):
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_5", "target": "30 ms",
                                         "delta": None, "why": "slower attack"})
    a = app()
    a.control.report("knob_5", 120, "Attack", "94 ms")
    said = run(a, "dial", phrase="give it more punch")
    knob, pos = a.control.sent[-1]
    assert knob == "knob_5"
    # the position must be the MEASURED one, not a modelled curve
    table = dict(a.dial_cal[DIAL_DEVICE]["Attack"]["table"])
    assert table[pos] == "30 ms"
    assert "Attack" in said and "30 ms" in said
    assert a.dial_undo["pos"] == 120    # undo remembers where it was


def test_relative_move_counts_from_where_reason_says_it_is(monkeypatch):
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_1", "target": None,
                                         "delta": "-5%", "why": ""})
    a = app()
    a.control.report("knob_1", 100, "Threshold", "-7.7 dB")
    run(a, "dial", phrase="turn the threshold down five percent")
    assert a.control.sent[-1] == ("knob_1", 94)   # 100 - 6.35


def test_unusable_model_answer_moves_nothing(monkeypatch):
    monkeypatch.setattr(dial_llm, "choose", lambda *a, **k: None)
    a = app()
    a.control.report("knob_5", 38, "Attack", "30 ms")
    said = run(a, "dial", phrase="make it sound like tuesday")
    assert a.control.sent == []
    assert "more punch" in said          # tells him what phrasing does work


def test_the_grammar_actually_routes_here():
    """The wiring that makes all of the above reachable: intents.py's final
    fallback. If this flips back to `find`, the dial is unreachable by voice."""
    intent = parse("give it more punch")
    assert intent.command == "dial"
    assert intent.args["phrase"] == "give it more punch"
