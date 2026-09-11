"""Bridge to Reason 12.

Two channels:
1. MIDI CC over the IAC virtual bus -> custom Remote codec -> Reason remote
   items (patch next/prev, transport, target track). Reliable, official path.
2. `open -a Reason <patchfile>` to load a search result. Reason creates the
   matching device with that patch in the rack of the open song.
"""
import subprocess

import mido

# Must match remote/ReasonVoice.luacodec
CC = {
    "patch_next": 20,
    "patch_prev": 21,
    "play": 22,
    "stop": 23,
    "record": 24,
    "loop": 25,
    "track_prev": 26,
    "track_next": 27,
    "undo": 28,
    "redo": 29,
    # Knobs -- continuous values, not taps. Which parameter each one moves
    # depends on the selected device; see the Scope blocks in the .remotemap.
    "knob_1": 30,
    "knob_2": 31,
    "knob_3": 32,
    "knob_4": 33,
    "knob_5": 34,
    "knob_6": 35,
    "knob_7": 36,
    "knob_8": 37,
    "knob_9": 38,
    "knob_10": 39,
    "knob_11": 40,
    "knob_12": 41,
    "knob_13": 42,
    "knob_14": 43,
    "knob_15": 44,
    "knob_16": 45,
    "knob_17": 46,
    "knob_18": 47,
    "knob_19": 48,
    "knob_20": 49,
    "knob_21": 50,
    "knob_22": 51,
    "knob_23": 52,
    "knob_24": 53,
    "knob_25": 54,
    "knob_26": 55,
    "knob_27": 56,
    "knob_28": 57,
    "knob_29": 58,
    "knob_30": 59,
    "knob_31": 60,
    "knob_32": 61,
    "knob_33": 62,
    "knob_34": 63,
    "knob_35": 64,
    "knob_36": 65,
    "knob_37": 66,
    "knob_38": 67,
    "knob_39": 68,
    "knob_40": 69,
    "knob_41": 70,
    "knob_42": 71,
    "knob_43": 72,
    "knob_44": 73,
    "knob_45": 74,
    "knob_46": 75,
    "knob_47": 76,
    "knob_48": 77,
}


# Reason -> us. Must match remote_deliver_midi() in remote/ReasonVoice.lua.
# Knob k reports its position on CC 77+k and its DISPLAYED value as SysEx.
# 77, not 59: knobs go OUT on 30-77, and the two directions share one IAC
# bus, so the return range has to start above them or the app reads its own
# echo as Reason's answer.
# SysEx slot 0 is not a knob -- it is the name of the device the surface is
# locked to, so the app can tell a Scream 4 from a compressor.
NUM_KNOBS = 48
FEEDBACK_CC = {77 + k: "knob_%d" % k for k in range(1, NUM_KNOBS + 1)}
SYSEX_ID = 0x7d  # MIDI non-commercial manufacturer ID
SYSEX_DEVICE_SLOT = 0


class ReasonControl:
    def __init__(self, midi_port_substring: str = "IAC", app_name: str = "Reason",
                 speak_feedback: bool = True):
        self.app_name = app_name
        self.speak_feedback = speak_feedback
        self.port = None
        self.inport = None
        # knob -> last position Reason reported (0-127)
        self.positions = {}
        # knob -> ("Attack", "30 ms") as Reason displays it
        self.displays = {}
        # Reason's own name for the locked device, e.g. "Scream 4 Distortion".
        #  until Reason says so -- never guessed.
        self.device = ""
        names = mido.get_output_names()
        for name in names:
            if midi_port_substring.lower() in name.lower():
                self.port = mido.open_output(name)
                break
        for name in mido.get_input_names():
            if midi_port_substring.lower() in name.lower():
                self.inport = mido.open_input(name)
                break
        if self.port is None:
            print(f"[warn] No MIDI port matching '{midi_port_substring}'. "
                  f"Available: {names or 'none'}. "
                  f"Enable the IAC Driver in Audio MIDI Setup. "
                  f"Patch next/prev and transport are disabled until then.")

    def tap(self, command: str) -> bool:
        """Send a momentary CC press for a Remote-mapped command."""
        if self.port is None or command not in CC:
            return False
        cc = CC[command]
        self.port.send(mido.Message("control_change", control=cc, value=127))
        self.port.send(mido.Message("control_change", control=cc, value=0))
        return True

    def set_value(self, knob: str, value: int) -> bool:
        """Move a knob. `knob` is "knob_1".."knob_16", value 0-127."""
        if self.port is None or knob not in CC:
            return False
        self.port.send(mido.Message("control_change", control=CC[knob],
                                    value=max(0, min(127, int(value)))))
        return True

    def poll(self) -> int:
        """Drain whatever Reason has sent back. Returns messages consumed.

        Call this before reading `positions`/`displays`. Nothing runs in a
        thread -- messages sit in the port buffer until collected, so a poll
        immediately before use is enough and there is no lock to get wrong.
        """
        if self.inport is None:
            return 0
        n = 0
        for msg in self.inport.iter_pending():
            n += 1
            if msg.type == "control_change" and msg.control in FEEDBACK_CC:
                self.positions[FEEDBACK_CC[msg.control]] = msg.value
            elif msg.type == "sysex" and len(msg.data) > 2 and msg.data[0] == SYSEX_ID:
                text = "".join(chr(b) for b in msg.data[2:])
                name, _, shown = text.partition("=")
                if msg.data[1] == SYSEX_DEVICE_SLOT:
                    self.device = shown
                else:
                    # Re-insert so the dict stays in REPORT order, oldest
                    # first. Whatever moved last is the best evidence of what
                    # is locked now: knob 9 says "Drum 3 Decay Offset" (Kong)
                    # until Redrum is locked and it says "Drum 3 Length", and
                    # knobs 41-48 keep Kong's names forever because Redrum
                    # never writes them. Scanning oldest-first would pin the
                    # device he unlocked an hour ago.
                    key = "knob_%d" % msg.data[1]
                    self.displays.pop(key, None)
                    self.displays[key] = (name, shown)
            # Anything else is our own CC 30-45 echoing back off the IAC bus.
        return n

    def current(self, knob: str):
        """(position 0-127, "Attack", "30 ms") or None if Reason hasn't said."""
        self.poll()
        if knob not in self.positions:
            return None
        name, shown = self.displays.get(knob, ("", ""))
        return self.positions[knob], name, shown

    def load_patch(self, path: str) -> bool:
        """Open a patch file in Reason (creates the device in the rack)."""
        result = subprocess.run(
            ["open", "-a", self.app_name, path],
            capture_output=True, text=True,
        )
        return result.returncode == 0

    def say(self, text: str):
        """Spoken feedback via macOS `say`, non-blocking."""
        print(f">> {text}")
        if self.speak_feedback:
            subprocess.Popen(["say", "-r", "220", text])
