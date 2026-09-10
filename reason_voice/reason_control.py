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
}


class ReasonControl:
    def __init__(self, midi_port_substring: str = "IAC", app_name: str = "Reason",
                 speak_feedback: bool = True):
        self.app_name = app_name
        self.speak_feedback = speak_feedback
        self.port = None
        names = mido.get_output_names()
        for name in names:
            if midi_port_substring.lower() in name.lower():
                self.port = mido.open_output(name)
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
        """Move a knob. `knob` is "knob_1".."knob_8", value 0-127."""
        if self.port is None or knob not in CC:
            return False
        self.port.send(mido.Message("control_change", control=CC[knob],
                                    value=max(0, min(127, int(value)))))
        return True

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
