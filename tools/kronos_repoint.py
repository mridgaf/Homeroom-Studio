"""Save program USER-G 000 pointing at its own kit (USER-G kit 00 = kit 136). Test first in scratch slot USER-G 127."""
import sys, time
import mido, numpy as np, sounddevice as sd
sys.path.insert(0, "tools")
import kronos
from kronos_bank import pack
from kronos_names import read_name, unpack

HDR = [0x42, 0x30, 0x68]
out, inp = mido.open_output("KRONOS SOUND"), mido.open_input("KRONOS KEYBOARD")
send = lambda d: out.send(mido.Message("sysex", data=HDR + d))  # noqa: E731
KIT_BYTE = 2776


def stored_prog(bank, idx):
    while inp.poll(): pass
    send([0x72, 0x00, bank, idx >> 7, idx & 0x7F]); t = time.time()
    while time.time() - t < 30:
        for m in inp.iter_pending():
            d = list(m.data) if m.type == "sysex" else []
            if d[:5] == HDR + [0x73, 0x00]:
                return bytearray(unpack(d[9:]))
        time.sleep(0.02)


def write_prog(slot, raw, name):
    raw = bytearray(raw); raw[0:24] = name.encode().ljust(24, b"\x00")
    send([0x73, 0x00, 0x46, 0, slot, 4] + pack(bytes(raw))); time.sleep(2)
    send([0x76, 0x00, 0x46]); time.sleep(4)


def select(pc):
    for kind, kw in (("control_change", {"control": 0, "value": 0}), ("control_change", {"control": 32, "value": 14}), ("program_change", {"program": pc})):
        out.send(mido.Message(kind, channel=0, **kw))
    time.sleep(3)


def hit(note=24):
    rec = sd.rec(int(1.6 * 48000), samplerate=48000, channels=2, device="KRONOS _ USB _ L&R", dtype="float32"); time.sleep(0.3)
    out.send(mido.Message("note_on", channel=0, note=note, velocity=110)); time.sleep(0.15)
    out.send(mido.Message("note_off", channel=0, note=note)); sd.wait()
    return round(float(np.abs(rec).max()), 3)


src = stored_prog(0x46, 0)
print("USER-G 000 name:", bytes(src[:24]).decode().rstrip("\x00 "), "| kit bytes now:", src[KIT_BYTE], src[KIT_BYTE + 1])
assert src[KIT_BYTE] == 4 and src[KIT_BYTE + 1] == 0, "kit byte is not the expected 4: stopping"
new = bytearray(src); new[KIT_BYTE] = 136
write_prog(127, new, "Claude Scratch 1")
print("scratch slot:", read_name(out, inp, 0x46, 127))
select(127)
print("scratch peak (kick, kit 136 untouched):", hit())
send([0x71, 0x00, 1, 8]); time.sleep(0.5)
for z in range(3): send([0x53, z, 24, 9] + kronos._val(-99)); time.sleep(0.1)
time.sleep(0.5)
muted = hit(); print("scratch peak with kit 136 kick muted:", muted)
levels = [15, 22, -25]   # stored levels of kit 136 key 24 (read earlier)
for z in range(3): send([0x53, z, 24, 9] + kronos._val(levels[z])); time.sleep(0.1)
if muted < 0.01:
    write_prog(0, new, "Claude Hip Hop Kit")
    print("USER-G 000 saved pointing at kit 136:", read_name(out, inp, 0x46, 0))
else:
    print("scratch did not follow kit 136: NOT touching USER-G 000")

import os
sys.stdout.flush()
os._exit(0)  # MIDI/audio threads otherwise keep the finished script alive
