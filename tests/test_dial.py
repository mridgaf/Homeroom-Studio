"""The dial: knob panel state, slider moves, one-step undo.

No MIDI, no Reason, no local model — a fake control surface stands in for all
three. What is NOT covered here, because nothing outside Reason can cover it:
whether Reason actually reports its knobs on lock. That check lives in the
manual steps at the bottom of DECISIONS.md.
"""
import asyncio
import json

import pytest

from reason_voice.intents import parse
from reason_voice.server import DEFAULT_SETTINGS, Session, WebApp
from reason_voice import dial_llm

COMPRESSOR = "MClass Compressor"
SCREAM = "Scream 4 Distortion"
RV7000 = "RV7000 Advanced Reverb"

ALGOS = ["Small Space", "Room", "Hall", "Arena", "Plate",
         "Spring", "Echo", "Multi Tap", "Reverse", "Convolution"]
MODES = ["Reverb", "EQ", "Gate"]


def algo_cal():
    """The RV7000 as the sweep leaves it: an algorithm dial that only means the
    algorithm while Edit Mode reads Reverb, plus the mode control itself."""
    return {RV7000: {
        "Soft Knob 1": {"knob": "knob_9", "unit": "", "volatile": "Edit Mode",
                        "requires": {"Edit Mode": "Reverb"},
                        "table": [[p, ALGOS[min(9, p * 10 // 128)]]
                                  for p in range(128)]},
        "Edit Mode": {"knob": "knob_5", "unit": "",
                      "table": [[p, MODES[min(2, p * 3 // 128)]]
                                for p in range(128)]},
        "Decay": {"knob": "knob_1", "unit": "s",
                  "table": [[p, "%.1f s" % (p / 10.0)] for p in range(128)]}}}


class FakeControl:
    """Stands in for ReasonControl. Records what was sent; replays what
    'Reason' has reported, in the same shape the real class exposes."""

    def __init__(self, connected=True):
        self.connected = connected
        self.positions = {}
        self.displays = {}
        self.sent = []
        self.device = ""      # Reason's own Device Name, "" until it says

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
        # mirrors the real class: re-insert so `displays` stays in report
        # order, oldest first
        self.displays.pop(knob, None)
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
    a.dial_device = None      # worked out from what Reason reports
    a.dial_knobs = {}
    a.dial_cal = dial_llm.load_calibration()
    a.dial_undo = None

    async def _push(extra=None):
        pass

    a.push = _push
    return a


def locked(connected=True, device=COMPRESSOR):
    """An app whose surface is locked to `device`, because Reason named one of
    that device's parameters — exactly how the real thing finds out."""
    a = app(connected)
    first = {COMPRESSOR: ("knob_5", 38, "Attack", "30 ms"),
             SCREAM: ("knob_1", 60, "Damage Control", "47"),
             RV7000: ("knob_1", 40, "Decay", "4.0 s")}[device]
    a.control.report(*first)
    return a


def run(a, command, **args):
    from reason_voice.intents import Intent
    asyncio.run(a.execute(Intent(command, args)))
    return a.feedback


# -- panel state -------------------------------------------------------------

def test_knob_names_come_from_the_remotemap():
    a = locked()
    st = a.dial_state()
    assert st["device"] == COMPRESSOR
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
    actually holding the parameter. (The device is still identified, from the
    OTHER knob whose name the map does recognise.)"""
    a = app()
    a.control.report("knob_1", 64, "Threshold", "-18.0 dB")
    a.control.report("knob_5", 38, "Attack Time", "30 ms")
    row = {k["knob"]: k for k in a.dial_state()["knobs"]}["knob_5"]
    assert row["param"] == "Attack Time"
    assert row["shown"] == "30 ms"
    assert row["pos"] == 38


def test_slider_ends_are_the_measured_values():
    a = locked()
    row = {k["knob"]: k for k in a.dial_state()["knobs"]}["knob_5"]
    assert row["lo"] == "1 ms" and row["hi"] == "100 ms"


# -- moving knobs ------------------------------------------------------------

def test_slider_move_sends_the_position():
    a = locked()
    run(a, "dial_set", knob="knob_5", value=96)
    assert a.control.sent == [("knob_5", 96)]


def test_undo_puts_it_back():
    a = locked()
    run(a, "dial_set", knob="knob_5", value=96)
    assert a.dial_undo["pos"] == 38
    run(a, "dial_undo")
    assert a.control.sent[-1] == ("knob_5", 38)
    assert a.dial_undo is None          # one slot, spent
    assert "Nothing to put back" in run(a, "dial_undo")


def test_nothing_moves_without_the_midi_bridge():
    a = locked(connected=False)
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
    table = dict(a.dial_cal[COMPRESSOR]["Attack"]["table"])
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
    a = locked()
    said = run(a, "dial", phrase="make it sound like tuesday")
    assert a.control.sent == []
    assert "more punch" in said          # tells him what phrasing does work


def test_the_grammar_actually_routes_here():
    """The wiring that makes all of the above reachable: intents.py's final
    fallback. If this flips back to `find`, the dial is unreachable by voice."""
    intent = parse("give it more punch")
    assert intent.command == "dial"
    assert intent.args["phrase"] == "give it more punch"


# -- two devices: which one is locked (added 2026-09-10) ---------------------

def test_the_device_is_worked_out_from_what_reason_reports():
    """A Scream 4 and a compressor share knob NUMBERS, not parameters. Getting
    this wrong reads a value out of the wrong calibration table."""
    a = locked(device=SCREAM)
    st = a.dial_state()
    assert st["device"] == SCREAM
    assert len(st["knobs"]) == 16
    by_knob = {k["knob"]: k for k in st["knobs"]}
    assert by_knob["knob_1"]["param"] == "Damage Control"
    assert by_knob["knob_10"]["param"] == "Body Type"


def test_an_unknown_device_moves_nothing(monkeypatch):
    """Reason has spoken, but only with a name we cannot place. Refuse."""
    called = []
    monkeypatch.setattr(dial_llm, "choose", lambda *a, **k: called.append(a))
    a = app()
    a.control.report("knob_1", 64, "Womble Depth", "3")
    assert a.dial_state()["locked"] is False
    assert "Lock to ReasonVoice" in run(a, "dial", phrase="make it dirtier")
    assert a.control.sent == [] and called == []
    assert "locked" in run(a, "dial_set", knob="knob_1", value=99).lower()
    assert a.control.sent == []


def test_a_shared_parameter_name_never_picks_a_device():
    """"Enabled" is on both devices. Guessing from it would be a coin flip."""
    a = app()
    a.control.report("knob_8", 127, "Enabled", "2")
    assert a.dial_state()["device"] in ("", None)
    assert a.dial_state()["knobs"] == []


def test_reason_s_device_name_is_a_cold_start_hint_only():
    """Before any knob moves, an un-renamed device still identifies itself."""
    a = app()
    a.control.device = SCREAM
    assert a.dial_device is None
    st = a.dial_state()
    assert st["device"] == SCREAM and len(st["knobs"]) == 16
    # ...but a parameter name always wins, because he can rename the rack device
    a.control.device = "My Crunch Box"
    a.control.report("knob_5", 38, "Attack", "30 ms")
    assert a.dial_state()["device"] == COMPRESSOR


def test_the_high_knob_slots_reach_reason():
    """Slots past the first eight are useless if the CC map stops short.

    Knob 48 is the last one Kong's 16-pad block uses, so this is the end of
    the range in practice as well as on paper.
    """
    a = locked(device=SCREAM)
    a.control.report("knob_48", 10, "Enabled", "1")
    run(a, "dial_set", knob="knob_48", value=127)
    assert a.control.sent[-1] == ("knob_48", 127)
    from reason_voice.reason_control import CC, FEEDBACK_CC, NUM_KNOBS
    assert NUM_KNOBS == 48
    assert CC["knob_16"] == 45, "knobs 1-16 kept their original outgoing CCs"
    assert CC["knob_48"] == 77 and 125 in FEEDBACK_CC


def test_a_named_setting_lands_in_the_middle_of_its_run(monkeypatch):
    """"body type C" — a picker shows letters, so the number path can't help."""
    table = [[p, "ABCDE"[min(4, p * 5 // 128)]] for p in range(128)]
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_10", "target": "C",
                                         "delta": None, "why": ""})
    cal = {SCREAM: {"Body Type": {"knob": "knob_10", "unit": "",
                                  "table": table}}}
    # the handler re-reads the calibration file on every phrase, so patching
    # a.dial_cal alone would be overwritten and the test would pass on nothing
    monkeypatch.setattr(dial_llm, "load_calibration", lambda *a, **k: cal)
    a = locked(device=SCREAM)
    run(a, "dial", phrase="body type C")
    knob, pos = a.control.sent[-1]
    assert knob == "knob_10" and table[pos][1] == "C"
    # ...and in the MIDDLE of C's run (52-76), not on an edge one rounding
    # step away from B. Landing anywhere inside C would pass the line above.
    assert pos == 64, pos


def test_a_volatile_knob_refuses_a_real_unit(monkeypatch):
    """Scream's P1 means something else under every Damage Type, so its
    measured table is not a lookup anyone may trust."""
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_3", "target": "30 ms",
                                         "delta": None, "why": ""})
    cal = {SCREAM: {"Parameter 1": {
        "knob": "knob_3", "unit": "ms", "volatile": "Damage Type",
        "table": [[p, "%d ms" % p] for p in range(128)]}}}
    monkeypatch.setattr(dial_llm, "load_calibration", lambda *a, **k: cal)
    a = locked(device=SCREAM)
    said = run(a, "dial", phrase="p1 to 30 milliseconds")
    assert a.control.sent == []
    assert "can’t place" in said

    # ...and the SAME table without the volatile flag does resolve, so the
    # assertion above is about the flag and not about a missing entry.
    del cal[SCREAM]["Parameter 1"]["volatile"]
    a2 = locked(device=SCREAM)
    run(a2, "dial", phrase="p1 to 30 milliseconds")
    assert a2.control.sent[-1] == ("knob_3", 30)


# -- Scream 4 reports numbers, not labels (added 2026-09-11) ----------------

def test_bare_numbers_become_the_panel_labels():
    """Measured 2026-09-11: Scream 4's Remote layer returns "4" where its panel
    reads "Tape". The compressor returns "30 ms". Only the LABEL is filled in;
    every position stays exactly as it was measured off Reason."""
    cal = {SCREAM: {"Damage Type": {
        "knob": "knob_2", "unit": "",
        "table": [[p, str(min(9, p * 10 // 128))] for p in range(128)]}}}
    before = [row[0] for row in cal[SCREAM]["Damage Type"]["table"]]
    named = dial_llm.apply_value_names(cal)["Scream 4 Distortion"]["Damage Type"]
    assert [row[0] for row in named["table"]] == before   # positions untouched
    assert named["min_display"] == "Overdrive"
    assert named["max_display"] == "Scream"
    assert dial_llm.named_choices(named)[4] == "Tape"
    pos, _ = dial_llm.resolve({"knob": "knob_2", "target": "Tape"},
                              SCREAM, calibration=cal)
    assert named["table"][pos][1] == "Tape"


def test_naming_is_never_applied_twice():
    """Second pass must be a no-op -- "Tape" is not a number to re-index."""
    cal = {SCREAM: {"Body Type": {
        "knob": "knob_10", "unit": "",
        "table": [[p, str(min(4, p * 5 // 128))] for p in range(128)]}}}
    once = dial_llm.apply_value_names(cal)
    twice = dial_llm.apply_value_names(once)
    assert (twice[SCREAM]["Body Type"]["table"]
            == once[SCREAM]["Body Type"]["table"])


def test_a_device_with_real_units_is_left_alone():
    """The compressor already speaks dB and ms -- naming must not touch it."""
    cal = {COMPRESSOR: {"Attack": {"knob": "knob_5", "unit": "ms",
                                   "table": [[0, "1 ms"], [127, "100 ms"]]}}}
    assert (dial_llm.apply_value_names(cal)[COMPRESSOR]["Attack"]["table"]
            == [[0, "1 ms"], [127, "100 ms"]])


def test_the_real_scream_table_names_every_picker():
    """Guards the shipped files together: if calibration.json is re-swept or
    value_names.json is edited, a number left showing here means a mismatch."""
    cal = dial_llm.load_calibration()
    scream = cal.get(SCREAM)
    if not scream:
        pytest.skip("Scream 4 not calibrated on this machine")
    for param in ("Damage Type", "Body Type", "Body On/Off"):
        choices = dial_llm.named_choices(scream[param])
        assert choices, f"{param} still shows bare numbers"
        assert not any(c.strip().lstrip("-").isdigit() for c in choices), choices


# -- RV7000: a knob that only means what it means in one mode (2026-09-11) ---

def test_the_reverb_maps_sixteen_controls():
    a = locked(device=RV7000)
    st = a.dial_state()
    assert st["device"] == RV7000
    assert len(st["knobs"]) == 16
    by_knob = {k["knob"]: k for k in st["knobs"]}
    assert by_knob["knob_9"]["param"] == "Soft Knob 1"   # the algorithm dial
    assert by_knob["knob_5"]["param"] == "Edit Mode"
    assert dial_llm.device_for_param("Decay") == RV7000
    assert dial_llm.device_for_param("Enabled") is None  # on all three devices


def test_naming_an_algorithm_sets_the_mode_first(monkeypatch):
    """"give me a plate": the dial is only the algorithm dial on the Reverb
    page, so the mode is set and CHECKED before anything else moves."""
    cal = algo_cal()
    monkeypatch.setattr(dial_llm, "load_calibration", lambda *a, **k: cal)
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_9", "target": "Plate",
                                         "delta": None, "why": ""})
    a = locked(device=RV7000)
    a.control.report("knob_5", 100, "Edit Mode", "Gate")   # on the wrong page

    # the fake surface answers a write the way Reason would: position moves,
    # and the label follows the measured table
    real_set = a.control.set_value

    def set_value(knob, value):
        ok = real_set(knob, value)
        if ok and knob == "knob_5":
            a.control.report(knob, value, "Edit Mode",
                             cal[RV7000]["Edit Mode"]["table"][value][1])
        return ok

    a.control.set_value = set_value
    run(a, "dial", phrase="give me a plate")

    moved = [k for k, _ in a.control.sent]
    assert moved[0] == "knob_5", a.control.sent     # mode FIRST
    assert moved[-1] == "knob_9", a.control.sent    # then the algorithm
    assert cal[RV7000]["Edit Mode"]["table"][a.control.sent[0][1]][1] == "Reverb"
    assert cal[RV7000]["Soft Knob 1"]["table"][a.control.sent[-1][1]][1] == "Plate"


def test_a_plain_knob_never_touches_the_mode(monkeypatch):
    """Decay means Decay on every page — no mode write, one move."""
    cal = algo_cal()
    monkeypatch.setattr(dial_llm, "load_calibration", lambda *a, **k: cal)
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_1", "target": "4.0 s",
                                         "delta": None, "why": ""})
    a = locked(device=RV7000)
    a.control.report("knob_5", 100, "Edit Mode", "Gate")
    run(a, "dial", phrase="four second tail")
    assert [k for k, _ in a.control.sent] == ["knob_1"], a.control.sent


def test_already_on_reverb_means_one_move_only(monkeypatch):
    cal = algo_cal()
    monkeypatch.setattr(dial_llm, "load_calibration", lambda *a, **k: cal)
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_9", "target": "Hall",
                                         "delta": None, "why": ""})
    a = locked(device=RV7000)
    a.control.report("knob_5", 0, "Edit Mode", "Reverb")
    run(a, "dial", phrase="make it a hall")
    assert [k for k, _ in a.control.sent] == ["knob_9"], a.control.sent


def test_a_mode_that_never_arrives_moves_nothing(monkeypatch):
    """The whole point of the mechanism: if the page can't be reached, turning
    the dial anyway would be a confidently wrong move. It refuses instead."""
    cal = algo_cal()
    monkeypatch.setattr(dial_llm, "load_calibration", lambda *a, **k: cal)
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_9", "target": "Plate",
                                         "delta": None, "why": ""})
    a = locked(device=RV7000)
    a.control.report("knob_5", 100, "Edit Mode", "Gate")   # writes change nothing
    said = run(a, "dial", phrase="give me a plate")
    assert not any(k == "knob_9" for k, _ in a.control.sent), a.control.sent
    assert "Edit Mode" in said and "Reverb" in said
    assert a.dial_undo is None


def test_a_programmer_dial_still_refuses_a_real_unit(monkeypatch):
    """Named settings are allowed on a context-dependent knob; units are not.
    Soft Knob 2 is predelay under one algorithm and something else under the
    next, so its measured milliseconds are true for one algorithm only."""
    cal = algo_cal()
    cal[RV7000]["Soft Knob 2"] = {
        "knob": "knob_10", "unit": "ms",
        "volatile": ["Edit Mode", "Soft Knob 1"],
        "table": [[p, "%d ms" % p] for p in range(128)]}
    monkeypatch.setattr(dial_llm, "load_calibration", lambda *a, **k: cal)
    monkeypatch.setattr(dial_llm, "choose",
                        lambda *a, **k: {"knob": "knob_10", "target": "30 ms",
                                         "delta": None, "why": ""})
    a = locked(device=RV7000)
    a.control.report("knob_5", 0, "Edit Mode", "Reverb")
    said = run(a, "dial", phrase="predelay to 30 milliseconds")
    assert a.control.sent == []
    assert "can’t place" in said

    # ...and the SAME table without the flag resolves, so this is about the
    # flag and not about a table the lookup could never have matched.
    del cal[RV7000]["Soft Knob 2"]["volatile"]
    a2 = locked(device=RV7000)
    run(a2, "dial", phrase="predelay to 30 milliseconds")
    assert a2.control.sent[-1] == ("knob_10", 30)


# -- the sweep itself: don't vandalise a button, don't measure the wrong page --

class FakeKnob:
    """A control surface for calibrate.py. `flip` makes a control behave like a
    button that toggles on EVERY message instead of taking a value."""

    def __init__(self, labels, flip=False):
        self.labels = labels          # position -> what Reason would display
        self.flip = flip
        self.pos = 0
        self.state = 0
        self.sent = []

    def set_value(self, knob, value):
        self.sent.append((knob, int(value)))
        if self.flip:
            self.state = 1 - self.state
            self.pos = 127 if self.state else 0
        else:
            self.pos = int(value)
        return True

    def poll(self):
        return 0

    def current(self, knob):
        return self.pos, "Edit Mode", self.labels[self.pos]


def test_a_toggle_button_is_spotted_before_it_gets_swept():
    """128 writes to a control that flips on every one would leave his patch
    somewhere random. Three writes tell us which kind it is."""
    from reason_voice import calibrate
    straight = FakeKnob(["Off"] * 64 + ["On"] * 64)
    assert calibrate.probe(straight, "knob_6") == "absolute"
    # The count is an implementation detail -- it went 3 -> 5 when probe() was
    # hardened against dropped reports. What must stay true is the reason the
    # assertion exists: a handful of writes, nowhere near a 128-step sweep.
    assert len(straight.sent) <= 10

    toggling = FakeKnob(["Off"] * 64 + ["On"] * 64, flip=True)
    assert calibrate.probe(toggling, "knob_6") == "toggle"


def test_the_sweep_refuses_to_measure_on_the_wrong_page():
    """put() has to CHECK it arrived. A table measured on the EQ page would be
    wrong in a way nothing downstream could detect."""
    from reason_voice import calibrate
    modes = [MODES[min(2, p * 3 // 128)] for p in range(128)]
    data = {RV7000: {"Edit Mode": {
        "knob": "knob_5", "unit": "",
        "table": [[p, modes[p]] for p in range(128)]}}}

    arrives = FakeKnob(modes)
    assert calibrate.put(arrives, data, RV7000, "Edit Mode", "Reverb") is True

    stuck = FakeKnob(["Gate"] * 128)        # writes change nothing
    assert calibrate.put(stuck, data, RV7000, "Edit Mode", "Reverb") is False
    assert calibrate.put(stuck, data, RV7000, "Nonexistent", "Reverb") is False


# -- Kong: a context that can never be reached (2026-09-11) ------------------

KONG = "Kong Drum Designer"


def test_kong_reaches_every_pad_three_deep():
    """All 16 pads x Level/Pitch Offset/Decay Offset, in pad order.

    Knob (pad-1)*3+1..+3 is the contract the phrase->knob step relies on: get
    the stride wrong and "make the snare louder" turns a different drum. The
    DM and FX knobs are deliberately gone -- they were percentage-only under
    every module, so depth was the cheap half of the trade.
    """
    km = dial_llm.knob_map(KONG)
    assert len(km) == 48
    want = {"knob_%d" % ((pad - 1) * 3 + 1 + i): "Drum %d %s" % (pad, param)
            for pad in range(1, 17)
            for i, param in enumerate(("Level", "Pitch Offset", "Decay Offset"))}
    assert km == want, {k: (km.get(k), want[k])
                        for k in want if km.get(k) != want[k]}
    # nothing module-dependent survived the trade
    assert not [v for v in km.values()
                if " DM " in v or "FX" in v or "Aux" in v], km
    assert dial_llm.device_for_param("Drum 16 Pitch Offset") == KONG


def test_an_unreachable_context_refuses_names_too(monkeypatch):
    """Reason never reports which drum module is loaded, so a measured name on
    a Kong knob may be a leftover from a module he has since swapped. Only a
    context the app can SET and READ BACK (`requires`) earns named settings."""
    entry = {"knob": "knob_10", "unit": "",
             "volatile": "the drum module loaded in that pad",
             "table": [[p, "Boom" if p < 64 else "Click"] for p in range(128)]}
    cal = {KONG: {"Drum 1 DM Variable": entry}}
    assert dial_llm.resolve({"knob": "knob_10", "target": "Click"},
                            KONG, calibration=cal) is None
    # percentages still work — they are arithmetic, not a lookup
    pos, _ = dial_llm.resolve({"knob": "knob_10", "target": "50%"},
                              KONG, calibration=cal)
    assert pos == 64

    # ...and the SAME entry WITH a reachable context does accept the name, so
    # this is about `requires` and not about the table.
    entry["requires"] = {"Drum 1 FX1 On": "On"}
    pos, _ = dial_llm.resolve({"knob": "knob_10", "target": "Click"},
                              KONG, calibration=cal)
    assert entry["table"][pos][1] == "Click"


def test_the_guide_reaches_a_parameter_reason_spells_differently():
    """Reason says "Drum 16 Pitch Offset"; the guide has one "Pitch Offset"
    bullet for all sixteen pads. Strip the pad number or every knob past pad 1
    reaches the model with no description at all."""
    notes = dial_llm.control_notes(KONG)
    assert dial_llm.note_for(notes, "Drum 1 Level").startswith("how loud")
    for pad in (1, 9, 16):
        assert dial_llm.note_for(notes, "Drum %d Pitch Offset" % pad), pad
        assert dial_llm.note_for(notes, "Drum %d Decay Offset" % pad), pad
    assert dial_llm.note_for(notes, "Drum 1 FX1 P1"), notes   # guide still has it
    assert dial_llm.note_for(notes, "Drum 1 DM Variable") == ""   # honestly unknown


def test_it_refuses_to_pick_a_pad_he_did_not_name(monkeypatch):
    """Kong's parameters name the pad; Reason never says what is ON a pad.

    So "make the snare louder" has no answer, and the model picks one anyway —
    measured on 2026-09-11, it confidently chose Drum 5. Moving the wrong drum
    is worse than doing nothing, so a numbered parameter needs its number said.
    """
    import contextlib
    import io

    # the model always answers knob_13 = Drum 5 Level; no server, no network
    reply = json.dumps({"choices": [{"message": {
        "content": '{"knob":"knob_13","target":"75%"}'}}]})
    monkeypatch.setattr(dial_llm.urllib.request, "urlopen",
                        lambda *a, **k: contextlib.closing(io.BytesIO(
                            reply.encode())))
    call = lambda phrase: dial_llm.choose(phrase, KONG, calibration={})

    assert call("make the snare louder") is None       # knob_13 is Drum 5 Level
    assert call("turn up pad 5")["knob"] == "knob_13"  # digits
    assert call("turn up pad five")["knob"] == "knob_13"   # or the word
    assert call("turn up pad 15") is None              # 15 is not 5
    # a device whose parameters name no copy is untouched by the rule
    assert dial_llm.numbered_copy("Attack") is None
    assert dial_llm.numbered_copy("Soft Knob 1") is None


def test_one_description_per_control_not_one_per_pad():
    """48 knobs x the same 3 sentences is a wall the model reads past.

    Measured 2026-09-11: with the notes repeated, "make pad 12 ring longer"
    landed on Level. Hoisted into a legend, it lands on Decay Offset.
    """
    p = dial_llm.build_prompt("x", KONG, {})
    assert "What each control does:" in p
    assert p.count("how long the sound rings") == 1, "note repeated per pad"
    for knob, param in dial_llm.knob_map(KONG).items():
        assert "%s = %s\n" % (knob, param) in p + "\n", (knob, param)

    # unrelated knobs that merely share a note have no common name to hoist
    # them under, so the compressor's prompt keeps its notes inline
    mc = dial_llm.build_prompt("more punch")
    assert "What each control does:" not in mc
    assert "knob_4 = Input Gain --" in mc


# -- Redrum: ten channels, four deep (2026-09-11) ----------------------------

REDRUM = "Redrum Drum Computer"


def test_redrum_reaches_every_channel_four_deep():
    """10 channels x Level, Pitch, Length, Pan, in channel order.

    Stride 4, so knob_5 is channel 2's Level. If the block is ever rewritten
    by hand the tabs or the order go quietly wrong, and the app then turns
    channel 2's Pitch believing it is channel 1's Pan.
    """
    got = dial_llm.knob_map(REDRUM)
    want = {}
    k = 0
    for ch in range(1, 11):
        for control in ("Level", "Pitch", "Length", "Pan"):
            k += 1
            want["knob_%d" % k] = "Drum %d %s" % (ch, control)
    assert got == want, sorted(set(got.items()) ^ set(want.items()))
    assert len(got) == 40
    # the controls that are NOT wired stay out of the map
    for skip in (" Tone", " Send 1", " Send 2", " Mute", " Solo",
                 " Vel to ", " Sample", "Decay/Gate"):
        assert not [p for p in got.values() if skip in p], skip


def test_kong_and_redrum_both_say_drum_n_level():
    """The one collision wiring Redrum introduced, stated rather than found.

    Both devices spell loudness "Drum N Level" on channels 1-10, so a Level
    report alone no longer identifies which is locked and the app refuses.
    Everything else still separates them: Kong says Pitch OFFSET, Redrum says
    Pitch; Pan and Length are Redrum's alone; pads 11-16 are Kong's alone.
    """
    assert dial_llm.device_for_param("Drum 1 Level") is None
    assert dial_llm.device_for_param("Drum 10 Level") is None
    assert dial_llm.device_for_param("Drum 11 Level") == KONG
    for param, dev in (("Drum 1 Pitch", REDRUM), ("Drum 1 Pitch Offset", KONG),
                       ("Drum 7 Length", REDRUM), ("Drum 7 Decay Offset", KONG),
                       ("Drum 4 Pan", REDRUM)):
        assert dial_llm.device_for_param(param) == dev, param


def test_redrum_inherits_the_say_the_number_rule(monkeypatch):
    """Redrum numbers its channels the same way Kong numbers its pads, so the
    guard that stopped Kong inventing a pad covers Redrum without new code."""
    import contextlib
    import io

    reply = json.dumps({"choices": [{"message": {
        "content": '{"knob":"knob_9","target":"75%"}'}}]})   # Drum 3 Level
    monkeypatch.setattr(dial_llm.urllib.request, "urlopen",
                        lambda *a, **k: contextlib.closing(io.BytesIO(
                            reply.encode())))
    call = lambda phrase: dial_llm.choose(phrase, REDRUM, calibration={})

    assert call("make the snare louder") is None
    assert call("turn up drum 3")["knob"] == "knob_9"
    assert call("turn up channel three")["knob"] == "knob_9"


def test_the_redrum_guide_describes_every_wired_control():
    """A knob whose name reaches the model with no description gets picked by
    spelling alone. All four of Redrum's need a bullet in the guide."""
    notes = dial_llm.control_notes(REDRUM)
    for ch in (1, 5, 10):
        for control in ("Level", "Pitch", "Length", "Pan"):
            param = "Drum %d %s" % (ch, control)
            assert dial_llm.note_for(notes, param), param
    p = dial_llm.build_prompt("turn up drum 3", REDRUM, {})
    assert "What each control does:" in p
    assert p.count("where it sits left to right") == 1, "note repeated per channel"


def test_the_device_is_read_from_the_newest_report_not_the_oldest():
    """`displays` is never cleared, and the devices are different widths.

    Sweep Kong (48 knobs), then lock Redrum (40): slots 41-48 still hold Kong's
    names, because Redrum never writes them. Scanned oldest-first the app pins
    Kong while Redrum is locked, then moves knob 9 using Kong's calibration
    table into Redrum's Length. Newest-first is the whole fix.
    """
    a = app()
    a.control.report("knob_47", 64, "Drum 16 Pitch Offset", "0")   # stale Kong
    assert a.dial_state()["device"] == KONG
    a.control.report("knob_3", 64, "Drum 1 Length", "64")          # Redrum now
    assert a.dial_state()["device"] == REDRUM
    assert len(a.dial_state()["knobs"]) == 40
    # and back again, without restarting the app
    a.control.report("knob_47", 64, "Drum 16 Pitch Offset", "0")
    assert a.dial_state()["device"] == KONG


REX = "Dr.REX Loop Player"


def test_rex_maps_the_reachable_controls_and_no_slice_ones():
    """Every famous Dr. Octo Rex trick that lives at slice level is
    unreachable: slice pitch, pan, level, decay, reverse, alt group and slice
    output are not remotable parameters at all. Mapping one would mean the app
    promising a move Reason never performs -- the Kong drum-module problem
    again. What IS reachable is the whole global synth, and it is all here.
    """
    got = dial_llm.knob_map(REX)
    assert len(got) == 41
    assert got["knob_1"] == "Select Loop 1"
    assert got["knob_8"] == "Select Loop 8"
    for want in ("Selected Loop Slot", "Enable Loop Playback", "Notes to Slot",
                 "Osc Env Amount", "Amp Env Decay", "Filter Env Amount",
                 "Loop Transpose", "Trigger Next Setting", "LFO1 Dest"):
        assert want in got.values(), want
    for never in ("Slice", "Alt", "Rev", "Output"):
        assert not [p for p in got.values() if never in p], never


def test_rex_does_not_remap_screams_master_level():
    """Master Level is spelled identically on Scream 4. Mapping it on both
    would cost the app the ability to tell them apart for nothing -- Loop
    Level is the per-slot control and is what "louder" should reach anyway.
    """
    rex = dial_llm.knob_map(REX)
    assert "Master Level" not in rex.values()
    assert "Loop Level" in rex.values()
    assert dial_llm.device_for_param("Master Level") == SCREAM
    # and Rex is still identified easily -- these are its alone
    for param in ("Osc Env Amount", "Selected Loop Slot", "Loop Transpose",
                  "Filter Freq", "Select Loop 5"):
        assert dial_llm.device_for_param(param) == REX, param


def test_a_copy_numbered_at_the_end_still_needs_the_number_spoken():
    """Kong and Redrum write "Drum 7 Level"; Rex writes "Select Loop 3". Same
    hazard -- eight interchangeable things, and the model will pick one -- so
    the same refusal, via copy_number() rather than numbered_copy().

    The RV7000's "Soft Knob 1" also ends in a digit and is NOT a copy of
    anything: it is the Algorithm picker. Holding it to this rule would break
    "give me a plate".
    """
    assert dial_llm.copy_number("Select Loop 3", REX) == 3
    assert dial_llm.copy_number("Drum 7 Level", KONG) == 7
    assert dial_llm.copy_number("Soft Knob 1", RV7000) is None
    assert dial_llm.copy_number("Selected Loop Slot", REX) is None
    assert dial_llm.copy_number("LFO1 Rate", REX) is None
    # build_prompt still splits the middle-numbered form; widening
    # numbered_copy() instead of adding copy_number() would have broken it
    assert dial_llm.numbered_copy("Select Loop 3") is None
    assert dial_llm.numbered_copy("Drum 7 Level") == 7


def test_rex_refuses_to_pick_a_loop_slot_he_did_not_name(monkeypatch):
    import contextlib
    import io

    reply = json.dumps({"choices": [{"message": {
        "content": '{"knob":"knob_3","target":"100%"}'}}]})   # Select Loop 3
    monkeypatch.setattr(dial_llm.urllib.request, "urlopen",
                        lambda *a, **k: contextlib.closing(io.BytesIO(
                            reply.encode())))
    call = lambda phrase: dial_llm.choose(phrase, REX, calibration={})

    assert call("change the loop") is None
    assert call("play the drum loop") is None
    assert call("go to loop 3")["knob"] == "knob_3"
    assert call("switch to loop three")["knob"] == "knob_3"


def test_the_rex_guide_describes_every_wired_control():
    notes = dial_llm.control_notes(REX)
    missing = [p for p in dial_llm.knob_map(REX).values()
               if not dial_llm.note_for(notes, p)]
    assert not missing, missing
    assert "vinyl-scratch" in dial_llm.note_for(notes, "Osc Env Amount")


def test_rex_lfo_amount_is_percentage_only_because_dest_changes_its_units():
    """LFO1 Amount is however much of whatever LFO1 Dest points at -- pitch
    wobble and pan wobble are not the same units. Dest is a mapped knob, so
    the context is readable, but there is no single correct setting to drive
    it to the way the RV7000 has "Reverb", so it carries no `requires` and
    stays percentage-only.

    Loop Transpose and Loop Level are deliberately absent: they act on
    whichever slot is selected, but semitones are semitones in every slot.
    The target moves, the meaning does not.
    """
    from reason_voice import calibrate
    vol = calibrate.VOLATILE[REX]
    assert vol == {"LFO1 Amount": "LFO1 Dest"}, vol
    assert REX not in calibrate.REQUIRES


ALLIGATOR = "Alligator"


def test_alligator_reaches_all_three_bands_eight_deep():
    """3 bands x 8 controls, then the gates, envelopes, LFO, pattern, output.

    Stride 8, so knob_9 is the BAND pass's Filter On. Written from a script
    and checked here, because a hand-edited block goes quietly wrong in the
    tabs or the order and the app then drives the high pass believing it is
    the low pass.
    """
    got = dial_llm.knob_map(ALLIGATOR)
    want = {}
    k = 0
    for band in ("Low Pass", "Band Pass", "High Pass"):
        for control in ("Filter On", "Frequency", "Resonance", "Env Amount",
                        "LFO Amount", "Drive Amount", "Pan", "Volume"):
            k += 1
            want["knob_%d" % k] = "%s %s" % (band, control)
    for g in (1, 2, 3):
        for control in ("Open", "Trig"):
            k += 1
            want["knob_%d" % k] = "Gate %d %s" % (g, control)
    for rest in ("Amp Env Attack", "Amp Env Decay", "Amp Env Release",
                 "Filter Env Attack", "Filter Env Decay", "Filter Env Release",
                 "LFO Freq", "LFO Waveform", "LFOSync",
                 "Pattern", "Pattern Enable", "Resolution", "Shift", "Shuffle",
                 "Dry Volume", "Master Volume", "Ducking", "Enabled"):
        k += 1
        want["knob_%d" % k] = rest
    assert got == want, sorted(set(got.items()) ^ set(want.items()))
    assert len(got) == 48, "the surface holds 48 and Alligator now fills it"


def test_alligators_delay_and_phaser_are_the_cut():
    """61 remotable controls do not fit in 48 slots. The 13 dropped are the
    built-in delay and phaser (and Dry Pan) -- his call, 2026-09-11. Stated
    here so a later session re-adding one notices it must drop something else.
    """
    got = set(dial_llm.knob_map(ALLIGATOR).values())
    for cut in ("Low Pass Delay Amount", "Band Pass Delay Amount",
                "High Pass Delay Amount", "Low Pass Phaser Amount",
                "Band Pass Phaser Amount", "High Pass Phaser Amount",
                "Delay Time", "Delay Feedback", "Delay Pan", "DelaySync",
                "Phaser Rate", "Phaser Feedback", "Dry Pan"):
        assert cut not in got, cut


def test_alligator_and_rex_both_say_amp_env_attack():
    """The collision wiring Alligator introduced, stated rather than found.

    Alligator spells its two envelopes exactly as Dr. Octo Rex does, so those
    six names now identify nothing and the app refuses rather than guessing.
    Survivable: every band control is Alligator's alone, and Rex's Osc and
    Loop names are Rex's alone, so one move of any of them pins the device.
    """
    for shared in ("Amp Env Attack", "Amp Env Decay", "Amp Env Release",
                   "Filter Env Attack", "Filter Env Decay",
                   "Filter Env Release"):
        assert dial_llm.device_for_param(shared) is None, shared
    for param, dev in (("Band Pass Drive Amount", ALLIGATOR),
                       ("Ducking", ALLIGATOR),
                       ("High Pass Frequency", ALLIGATOR),
                       ("Osc Env Amount", REX),
                       ("Selected Loop Slot", REX)):
        assert dial_llm.device_for_param(param) == dev, param


def test_alligator_gates_are_numbered_but_its_bands_are_not(monkeypatch):
    """Three gates need the number spoken; three NAMED bands do not.

    "Open the gate" has no answer -- the model picks one of three and opens a
    band he did not mean. "Open up the low pass" is unambiguous, and holding
    it to the same rule would refuse a move that is perfectly clear.
    """
    import contextlib
    import io

    assert dial_llm.copy_number("Gate 2 Trig", ALLIGATOR) == 2
    assert dial_llm.copy_number("Low Pass Frequency", ALLIGATOR) is None
    assert dial_llm.copy_number("Ducking", ALLIGATOR) is None

    def answers(knob):
        reply = json.dumps({"choices": [{"message": {
            "content": '{"knob":"%s","target":"75%%"}' % knob}}]})
        monkeypatch.setattr(dial_llm.urllib.request, "urlopen",
                            lambda *a, **k: contextlib.closing(io.BytesIO(
                                reply.encode())))

    answers("knob_27")                                  # Gate 2 Open
    assert dial_llm.choose("open the gate", ALLIGATOR, calibration={}) is None
    assert dial_llm.choose("open gate 2", ALLIGATOR,
                           calibration={})["knob"] == "knob_27"
    answers("knob_2")                                   # Low Pass Frequency
    assert dial_llm.choose("open up the low pass", ALLIGATOR,
                           calibration={})["knob"] == "knob_2"


def test_the_alligator_guide_describes_every_wired_control():
    """A knob the model is shown with no description gets picked by spelling
    alone -- all 48 need a bullet the guide's lookup actually reaches."""
    notes = dial_llm.control_notes(ALLIGATOR)
    missing = [p for p in dial_llm.knob_map(ALLIGATOR).values()
               if not dial_llm.note_for(notes, p)]
    assert not missing, missing
    assert "squelchy" in dial_llm.note_for(notes, "High Pass Resonance")


def test_nothing_on_alligator_is_volatile():
    """Pattern Enable off makes four knobs do nothing, but it does not change
    what any of them MEAN. A targeting caveat belongs in the guide; only a
    units caveat belongs in VOLATILE. So Alligator carries neither.
    """
    from reason_voice import calibrate
    assert ALLIGATOR not in calibrate.VOLATILE
    assert ALLIGATOR not in calibrate.REQUIRES
    assert "Pattern Enable" in dial_llm.control_notes(ALLIGATOR)


def test_the_named_setting_example_only_appears_where_a_picker_exists():
    """The prompt used to show `target":"Tape"` on every device.

    Measured 2026-09-11 against the live model on Alligator, which has no
    picker at all: shown that example the model copies its SHAPE and invents a
    word -- "shuffle it" came back as target "Shuffle", "open gate 2" as
    "Open", and twice as the literal "Tape" from the example itself. A word
    that is not in the measured table resolves to nothing, so the knob never
    moves and the phrase looks broken to him. Withholding the example moved
    all eleven test phrases to percentages.

    Both directions asserted: a device WITH a picker must keep the example, or
    "give me a plate" stops working.
    """
    plain = dial_llm.build_prompt("shuffle it", ALLIGATOR, calibration={})
    assert '"Tape"' not in plain
    assert "never a word" in plain
    assert "three forms" in plain

    picker = {SCREAM: {"Body Type": {
        "knob": "knob_10", "unit": "",
        "table": [[p, "ABCDE"[min(4, p * 5 // 128)]] for p in range(128)]}}}
    withnames = dial_llm.build_prompt("body type c", SCREAM, calibration=picker)
    assert '"Tape"' in withnames
    assert "spelled exactly as listed" in withnames
    assert "four forms" in withnames


def test_a_knob_that_probed_as_a_toggle_never_crashes_a_lookup():
    """A button has no measured table, and resolve() used to reach into it anyway.

    Found at the machine, not in review: Kong's sweep on 2026-09-11 recorded
    `Drum 2 Level` as `{"knob": "knob_4", "unit": "", "toggle": true}` with no
    `table` key, because probe() saw it flip on every write. Any target with a
    real unit -- or a bare number, which is what a 0..127 Level invites -- then
    died on KeyError: 'table' in the live path.

    A percentage must still work: that is arithmetic on position and never
    touches the table. Everything else refuses, quietly.
    """
    cal = {KONG: {"Drum 2 Level": {"knob": "knob_4", "unit": "", "toggle": True}}}

    assert dial_llm.resolve({"knob": "knob_4", "target": "100"}, KONG,
                            calibration=cal) is None      # bare number
    assert dial_llm.resolve({"knob": "knob_4", "target": "30 ms"}, KONG,
                            calibration=cal) is None      # real unit
    assert dial_llm.resolve({"knob": "knob_4", "target": "On"}, KONG,
                            calibration=cal) is None      # a word

    pos, _ = dial_llm.resolve({"knob": "knob_4", "target": "75%"}, KONG,
                              calibration=cal)
    assert pos == 95
    pos, _ = dial_llm.resolve({"knob": "knob_4", "delta": "-5%"}, KONG,
                              current_pos=100, calibration=cal)
    assert pos == 94


def test_an_unswept_toggle_is_not_described_to_the_model_as_a_broken_range():
    """It printed "range: None .. None" -- teaching the model the knob is dead."""
    cal = {KONG: {"Drum 2 Level": {"knob": "knob_4", "unit": "", "toggle": True},
                  "Drum 1 Level": {"knob": "knob_1", "unit": "",
                                   "min_display": "0", "max_display": "127",
                                   "table": [[p, str(p)] for p in range(128)]}}}
    prompt = dial_llm.build_prompt("turn up pad 2", KONG, calibration=cal)
    assert "range: None" not in prompt
    assert "range: 0 .. 127" in prompt        # the swept one still says its ends


def test_a_sweep_that_lost_reports_says_so_instead_of_lying():
    """A dropped MIDI report becomes a stale value pretending to be measured.

    Reason warned about a MIDI input buffer overflow during Kong's sweep on
    2026-09-11, and it cost real data: positions 21-25 of Drum 2 Level all
    recorded "20" while the knob was moving. sweep() cannot tell that from a
    switch sitting still, so the table looked clean. The same overflow made
    probe() call that knob a toggle.

    The detector must fire on that shape and stay quiet on every control that
    legitimately repeats itself -- or it is noise and gets ignored.
    """
    from reason_voice import calibrate

    # a clean continuous knob: every position its own reading
    assert calibrate.lost_readings([[p, str(p)] for p in range(128)]) == []

    # the real failure: one flat run against a background of ones
    vals = list(range(128))
    for p in range(21, 26):
        vals[p] = 20                       # five reports never arrived
    lost = calibrate.lost_readings([[p, str(v)] for p, v in enumerate(vals)])
    assert len(lost) == 1
    run, at = lost[0]
    assert (at, run) == (20, 6)            # "20" held from position 20 to 25

    # a 2-state switch reports twice in 128 positions and is silent between
    assert calibrate.lost_readings(
        [[p, "Off" if p < 64 else "On"] for p in range(128)]) == []

    # a 3-state picker, and a 10-way one: even runs, nothing anomalous
    assert calibrate.lost_readings(
        [[p, str(min(2, p * 3 // 128))] for p in range(128)]) == []
    algos = ["Small Space", "Room", "Hall", "Arena", "Plate",
             "Spring", "Echo", "Multi Tap", "Reverse", "Convolution"]
    assert calibrate.lost_readings(
        [[p, algos[min(9, p * 10 // 128)]] for p in range(128)]) == []


def test_the_sweep_refuses_to_measure_a_device_that_is_not_the_locked_one():
    """The guard that would have caught the wrong-device sweep on its first knob.

    2026-09-11, at the machine: a Redrum sweep ran with Kong still Locked to
    ReasonVoice. Reason routed all 40 writes to Kong and reported Kong's names
    back, so the run printed clean, plausible numbers -- and filed Kong's
    Pitch Offset and Decay Offset under Redrum, where its map says Pitch,
    Length and Pan. Nothing in the output said anything was wrong.

    Reason names the parameter in every report, so the remotemap already holds
    the answer. Asserted here as data, so the rule survives an edit to main().
    """
    redrum = dial_llm.knob_map(REDRUM)
    kong = dial_llm.knob_map(KONG)

    # The exact readings that came back that day, on Redrum's knob slots.
    reported = {"knob_1": "Drum 1 Level", "knob_2": "Drum 1 Pitch Offset",
                "knob_3": "Drum 1 Decay Offset", "knob_4": "Drum 2 Level"}
    for knob, name in reported.items():
        assert kong[knob] == name, knob          # it was Kong all along

    mismatched = [k for k, name in reported.items() if redrum[k] != name]
    assert mismatched == ["knob_2", "knob_3", "knob_4"]

    # knob_1 is the trap: Kong and Redrum spell it identically, so the FIRST
    # knob alone cannot clear a run. The guard has to keep checking every knob.
    assert redrum["knob_1"] == kong["knob_1"] == "Drum 1 Level"

    src = (dial_llm.PROJECT_ROOT / "reason_voice" / "calibrate.py").read_text()
    assert "WRONG DEVICE" in src
    assert "if name and expected and name != expected:" in src


class _FakeSurface:
    """Just enough of ReasonControl to drive probe(): a control and a flaky bus.

    `kind` is what the control really is. `drop` is the index of the read whose
    report never arrives, so the previous reading is what gets seen -- exactly
    what a MIDI input buffer overflow does.
    """

    def __init__(self, kind, drop=None):
        self.kind = kind
        self.drop = drop
        self.state = 0
        self.reads = 0
        self.sent = []
        self.last = "0"

    def set_value(self, knob, value):
        self.sent.append(value)
        self.state = (1 - self.state) if self.kind == "toggle" else value

    def poll(self):
        pass

    def current(self, knob):
        fresh = str(self.state) if self.kind == "toggle" else str(self.state)
        if self.reads != self.drop:          # a dropped report shows the stale value
            self.last = fresh
        self.reads += 1
        return (0, "Whatever", self.last)


def test_probe_survives_the_dropped_report_that_fooled_it_twice():
    """Both real misfires from 2026-09-11, in both directions.

    Kong's Drum 2 Level (a normal 0-127 knob) was called a toggle, and
    Alligator's Gate 1 Open (a real button) was called absolute and then swept
    128 times -- flipping it 128 times -- while Gate 2 and Gate 3 Open, the same
    control, were correctly spared. One comparison of one pair of readings
    decided both, and one lost report was enough to invert it.
    """
    from reason_voice import calibrate

    calibrate.SETTLE = 0                       # no need to wait on a fake bus

    assert calibrate.probe(_FakeSurface("absolute"), "knob_4") == "absolute"
    assert calibrate.probe(_FakeSurface("toggle"), "knob_25") == "toggle"

    # a report lost anywhere in the run must not change either verdict
    for at in range(4):
        assert calibrate.probe(_FakeSurface("absolute", drop=at), "knob_4") \
            == "absolute", at
        assert calibrate.probe(_FakeSurface("toggle", drop=at), "knob_25") \
            == "toggle", at


def test_probe_breaks_a_tie_toward_the_safer_answer():
    """The two mistakes are not equal, so an undecidable control is a toggle.

    Wrongly calling a knob a toggle costs it its table and falls back to
    percentages, which still work. Wrongly calling a toggle a knob hammers it
    128 times -- damaging his patch AND recording noise as measurement.
    """
    from reason_voice import calibrate
    calibrate.SETTLE = 0

    class _AlwaysOneChange(_FakeSurface):
        """Exactly one change per round, however many samples are taken."""

        def set_value(self, knob, value):
            if value == 0:
                self.reads = 0          # the seed write starts a new round

        def current(self, knob):
            self.reads += 1
            return (0, "Whatever", "1" if self.reads == 1 else "0")

    assert calibrate.probe(_AlwaysOneChange("absolute"), "knob_1") == "toggle"


def test_an_obvious_toggle_is_decided_without_a_second_round_of_writes():
    """Why probe() keeps a "2 or more changes = toggle" branch at all.

    Drop it and the tie-break still reaches the right answer, so no verdict
    changes -- which is exactly why this needs its own test. What it costs is
    MIDI: every button takes two rounds instead of one, and there are 22 of
    them across Dr. Octo Rex and Alligator. Reason was already overflowing its
    input buffer on this bus on 2026-09-11; doubling the traffic to reach an
    answer we already have is how that gets worse.
    """
    from reason_voice import calibrate
    calibrate.SETTLE = 0

    clear = _FakeSurface("toggle")
    assert calibrate.probe(clear, "knob_25") == "toggle"
    assert len(clear.sent) == 5          # one seed + four samples, one round
