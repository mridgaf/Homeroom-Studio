"""Send one parameter-change and print every SysEx reply (to learn why an edit is ignored). Edit buffer only."""
import sys, time, mido
sys.path.insert(0, "tools")
import kronos
out, inp = mido.open_output("KRONOS SOUND"), mido.open_input("KRONOS KEYBOARD")
HDR = [0x42, 0x30, 0x68]
def show(label, data, wait=2.5):
    while inp.poll(): pass
    out.send(mido.Message("sysex", data=HDR + data)); t = time.time(); got = []
    while time.time() - t < wait:
        for m in inp.iter_pending():
            if m.type == "sysex": got.append(bytes(m.data).hex())
        time.sleep(0.02)
    print(label, "->", got or "no reply")
for kind, kw in (("control_change", {"control": 0, "value": 0}), ("control_change", {"control": 32, "value": 14}), ("program_change", {"program": 0})):
    out.send(mido.Message(kind, channel=0, **kw))
time.sleep(3)
show("MS number 136 (TYP9 SOC12 PID2)", [0x43, 9, 12, 0, 2, 0] + kronos._val(136))
show("IFX1 Send2 100 (TYP7 SOC0 PID8)", [0x43, 7, 0, 0, 8, 0] + kronos._val(100))
show("IFX2 effect type 37 (TYP7 SOC1 PID0)", [0x43, 7, 1, 0, 0, 0] + kronos._val(37))
show("OSC mode query? Mode Request", [0x12])

import os
sys.stdout.flush()
os._exit(0)  # MIDI/audio threads otherwise keep the finished script alive
