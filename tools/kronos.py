"""Talk to the Korg KRONOS 61 over USB-MIDI: find a sound by description, play it, nudge it.

    python tools/kronos.py find creepy piano      # shortlist from the 2,176 program names
    python tools/kronos.py play INT-B 36          # pick a program (bank + number as on the screen)
    python tools/kronos.py chord [C|Am|...]       # play a test chord
    python tools/kronos.py cc cutoff 40           # move a knob-type control (0-127)
    python tools/kronos.py check                  # offline self-check, no Kronos needed

Facts come from Korg's KRONOS MIDI Implementation (2024-08-08); sound names are read from the unit itself:
Bank Select MSB 0 + LSB per bank, then Program Change. Assumes the Kronos Global
MIDI channel is 1 and "Enable Program and Bank Change" is ticked (Global > MIDI);
both are factory defaults but NOT verified on this unit.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PORT_OUT = "KRONOS SOUND"  # the port that feeds the Kronos sound engines
CHANNEL = 0                # MIDI channel 1

# name -> CC number, from the Kronos MIDI chart (sound controllers / effect sends)
CC = {"mod": 1, "volume": 7, "pan": 10, "expression": 11, "fx1": 12, "fx2": 13,
      "sustain": 64, "resonance": 71, "release": 72, "attack": 73,
      "cutoff": 74, "decay": 75, "lfo_speed": 76, "lfo_depth": 77}

# plain word -> words that show up in Korg's program names / categories
STYLES = {
    "creepy": ["dark", "ghost", "whisper", "reverse", "cave", "cold", "music box", "eerie",
               "haunt", "drone", "spooky", "nightmare", "abyss", "shadow", "ice"],
    "dark": ["dark", "night", "shadow", "deep", "cave", "abyss"],
    "warm": ["warm", "soft", "mellow", "velvet", "analog"],
    "dirty": ["dirty", "grit", "fuzz", "drive", "distort", "crunch", "overdrive", "screamer"],
    "bright": ["bright", "shine", "glass", "sparkle"],
    "dreamy": ["dream", "float", "ambient", "atmos", "cloud", "wash"],
}

CHORDS = {"C": [60, 64, 67], "Am": [57, 60, 64], "Cm": [60, 63, 67], "Dm": [62, 65, 69],
          "Fm": [53, 56, 60], "Gm": [55, 58, 62]}


def catalog():
    """Sounds read from THIS Kronos (tools/kronos_names.py); empty 'Init' slots left out.
    Korg's published Voice Name List does not match this unit's firmware, so it is not used."""
    path = os.path.join(HERE, "kronos_unit_programs.json")
    return [p for p in json.load(open(path)) if p["text"] and not p["text"].startswith("Init")]


def find(words, limit=12):
    """Programs whose name/category contain the words; style words expand via STYLES."""
    terms = []
    for w in words:
        terms += STYLES.get(w.lower(), [w.lower()])
    wanted = [w.lower() for w in words if w.lower() not in STYLES]  # literal words must match
    scored = []
    for p in catalog():
        t = p["text"].lower()
        if any(w not in t for w in wanted):
            continue
        s = sum(1 for x in terms if x in t)
        if s:
            scored.append((s, p))
    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored[:limit]]


def label(p):
    return "%s %03d  %s" % (p["bank"], p["pc"], p["text"])


def lookup(bank, pc):
    for p in catalog():
        if p["bank"] == bank.upper() and p["pc"] == int(pc):
            return p
    raise SystemExit("no such program: %s %s" % (bank, pc))


def messages_for(p):
    """The three MIDI messages that select a program (bank MSB 0, bank LSB, program change)."""
    return [("control_change", {"control": 0, "value": 0}),
            ("control_change", {"control": 32, "value": p["lsb"]}),
            ("program_change", {"program": p["pc"]})]


def _port():
    import mido
    if PORT_OUT not in mido.get_output_names():
        raise SystemExit("Kronos MIDI port not found. Is it on and plugged in? Ports: %s"
                         % mido.get_output_names())
    return mido.open_output(PORT_OUT)


def play(bank, pc):
    import mido
    p = lookup(bank, pc)
    out = _port()
    for kind, kw in messages_for(p):
        out.send(mido.Message(kind, channel=CHANNEL, **kw))
    print("Kronos ->", label(p))


def chord(name="C", seconds=2.0):
    import mido
    out = _port()
    notes = CHORDS[name]
    for n in notes:
        out.send(mido.Message("note_on", channel=CHANNEL, note=n, velocity=80))
    time.sleep(seconds)
    for n in notes:
        out.send(mido.Message("note_off", channel=CHANNEL, note=n))


# General MIDI drum map; GM2 drum bank g(d) = Bank Select MSB 120 / LSB 0, program 16 = Power Kit
GM_KIT = {"kick": 36, "kick2": 35, "snare": 38, "clap": 39, "hat": 42, "open": 46}


def play_gm_drums(program=16):
    import mido
    out = _port()
    for kind, kw in (("control_change", {"control": 0, "value": 120}),
                     ("control_change", {"control": 32, "value": 0}),
                     ("program_change", {"program": program})):
        out.send(mido.Message(kind, channel=CHANNEL, **kw))


def beat(bpm=90, bars=8, swing=0.12, kit=None, lanes=None, lead=0.3):
    """8-bar boom-bap loop on a drum kit key map (GM_KIT or HH_KIT), sent live to the Kronos. Last bar adds a fill."""
    import random
    import mido
    kit = kit or GM_KIT
    out = _port()
    step = 60.0 / bpm / 4  # one 16th
    ev = []  # (16th index, key, velocity)
    for b in range(bars):
        o = b * 16
        ev += [(o, "kick", 112), (o + 10, "kick", 98), (o + 4, "snare", 112), (o + 12, "snare", 116)]
        if b % 2:
            ev += [(o + 7, "kick2", 90)]
        if b % 4 == 3:
            ev += [(o + 14, "snare", 80), (o + 15, "snare", 96), (o + 13, "clap", 90)]
        for i in range(0, 16, 2):
            ev += [(o + i, "open" if i == 14 and b % 2 else "hat", 70 + (14 if i % 4 == 0 else 0))]
    random.seed(7)
    t0 = time.time() + lead
    for n, key, vel in sorted(ev):
        if lanes and key not in lanes:
            continue
        when = t0 + (n + (swing if n % 2 else 0)) * step
        time.sleep(max(0, when - time.time()))
        note = kit[key]
        out.send(mido.Message("note_on", channel=CHANNEL, note=note, velocity=min(127, vel + random.randint(-6, 6))))
        out.send(mido.Message("note_off", channel=CHANNEL, note=note))
    time.sleep(1.5)


def set_cc(name, value):
    import mido
    _port().send(mido.Message("control_change", channel=CHANNEL, control=CC[name], value=int(value)))


def check():
    cat = catalog()
    assert len(cat) == 1536 and len({(p["bank"], p["pc"]) for p in cat}) == 1536
    assert messages_for(lookup("INT-B", 36))[1][1]["value"] == 1       # INT-B = LSB 1
    assert messages_for(lookup("USER-F", 0))[1][1]["value"] == 13      # USER-F = LSB 0x0D
    assert lookup("INT-B", 36)["text"] == '"...lead to Rome" E.P.'     # read from the unit 2026-10-25
    assert find(["creepy", "piano"]) and all("piano" in p["text"].lower() for p in find(["creepy", "piano"]))
    print("ok")


if __name__ == "__main__":
    a = sys.argv[1:] or ["check"]
    if a[0] == "find":
        for p in find(a[1:]):
            print(label(p))
    elif a[0] == "play":
        play(a[1], a[2])
    elif a[0] == "chord":
        chord(*(a[1:2] or ["C"]))
    elif a[0] == "cc":
        set_cc(a[1], a[2])
    else:
        check()


# ---- edits made INSIDE the Kronos (its own Drive and effect sends) ----
# "Hip Hop Kit" = program INT-F 095 = drum kit 4 (read from the unit). Keys per Korg's INT04 kit list, C4=60 so C1=24.
HH_KIT = {"kick": 24, "kick2": 26, "snare": 29, "clap": 35, "hat": 17, "open": 18}


def _val(v):
    """21-bit two's-complement value as the three 7-bit SysEx bytes (H, M, L)."""
    v &= 0x1FFFFF
    return [(v >> 14) & 0x7F, (v >> 7) & 0x7F, v & 0x7F]


def _sysex(data):
    import mido
    _port().send(mido.Message("sysex", data=[0x42, 0x30, 0x68] + data))


def kit_drive(note, drive, zones=3, kit=136):
    """Kit sample Drive (-99..+99) for a key, all velocity zones. Edit buffer only, not stored.
    Default kit 136 = USER-G kit 00 (Claude's copy). Never point this at a factory kit. Drive alone is not audible (it offsets the Program driver)."""
    _sysex([0x71, 0x00, kit >> 7, kit & 0x7F])  # Set Current Object: drum kit
    for z in range(zones):
        _sysex([0x53, z, note, 16] + _val(drive))  # PID 16 = Drive


def ifx_send(ifx, send, level):
    """Insert-effect send level (0-127) to Master FX 1/2. Edit buffer only, not stored."""
    _sysex([0x43, 7, ifx - 1, 0, 7 + send - 1, 0] + _val(level))  # TYP7 SOC=ifx SUB0 PID7/8 IDX0
