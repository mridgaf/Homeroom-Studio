"""MIDI push-to-talk: hold a pedal/pad/button on any controller to talk.

Works while Reason has focus and needs no macOS permissions — the exact
gap the in-page spacebar can't cover. Listens on every MIDI input EXCEPT
the IAC bus (we transmit commands there; listening would hear our own CCs).

Default control: CC 64 (sustain pedal), hold = record. Change midi_ptt_cc
in config.yaml if you use the pedal for actual sustain while talking.
"""
import mido


class MidiPTT:
    def __init__(self, on_press, on_release, cc=64, note=None,
                 exclude_substring="IAC"):
        self.on_press = on_press
        self.on_release = on_release
        self.cc = cc
        self.note = note
        self.ports = []
        self.port_names = []
        for name in mido.get_input_names():
            if exclude_substring.lower() in name.lower():
                continue
            try:
                self.ports.append(mido.open_input(name, callback=self._cb))
                self.port_names.append(name)
            except (IOError, OSError):
                pass

    def _cb(self, msg):
        try:
            if msg.type == "control_change" and msg.control == self.cc:
                (self.on_press if msg.value >= 64 else self.on_release)()
            elif self.note is not None and getattr(msg, "note", None) == self.note:
                if msg.type == "note_on" and msg.velocity > 0:
                    self.on_press()
                elif msg.type in ("note_off", "note_on"):
                    self.on_release()
        except Exception:
            pass   # a broken callback must never kill the MIDI thread

    def close(self):
        for p in self.ports:
            try:
                p.close()
            except (IOError, OSError):
                pass
