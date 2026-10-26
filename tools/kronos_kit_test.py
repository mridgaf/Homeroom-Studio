"""Which kit does program USER-G 000 play? Mute the kick in kit 136 (USER-G kit 00, edit buffer only), record a kick hit,
then restore. Also prints levels so the result is numeric. Edit buffer only, nothing stored."""
import sys, time
import mido, numpy as np, sounddevice as sd
sys.path.insert(0, "tools")
import kronos
from kronos_names import unpack

HDR = [0x42, 0x30, 0x68]
out, inp = mido.open_output("KRONOS SOUND"), mido.open_input("KRONOS KEYBOARD")
send = lambda d: out.send(mido.Message("sysex", data=HDR + d))  # noqa: E731


def hit(note=24, secs=1.6):
    rec = sd.rec(int(secs * 48000), samplerate=48000, channels=2, device="KRONOS _ USB _ L&R", dtype="float32")
    time.sleep(0.3)
    out.send(mido.Message("note_on", channel=0, note=note, velocity=110)); time.sleep(0.15)
    out.send(mido.Message("note_off", channel=0, note=note)); sd.wait()
    return round(float(np.abs(rec).max()), 3)


def select(bank_lsb, pc):
    for kind, kw in (("control_change", {"control": 0, "value": 0}), ("control_change", {"control": 32, "value": bank_lsb}),
                     ("program_change", {"program": pc})):
        out.send(mido.Message(kind, channel=0, **kw))
    time.sleep(3)


# stored levels of kick key 24 in kit 136 (copy of kit 4): Level offsets 4156, 4174, 4192 (Drive offsets minus 11)
while inp.poll(): pass
send([0x72, 0x04, 0x46, 0, 0])
t = time.time(); stored = None
while time.time() - t < 40 and stored is None:
    for m in inp.iter_pending():
        d = list(m.data) if m.type == "sysex" else []
        if d[:5] == HDR + [0x73, 0x04][:2] + [] or d[:5] == [0x42, 0x30, 0x68, 0x73, 0x04]:
            stored = bytearray(unpack(d[9:]))
    time.sleep(0.02)
lv = [stored[o] - 256 if stored[o] > 127 else stored[o] for o in (4156, 4174, 4192)]
print("kit 136 kick levels (stored):", lv)

select(14, 0)                                # USER-G 000
print("peak, USER-G 000 as saved:", hit())
send([0x43, 9, 12, 0, 2, 0] + kronos._val(136)); time.sleep(1)       # try to point at kit 136
send([0x71, 0x00, 0x00, 136 - 128])           # Set Current Object: drum kit 136 -> idH=1, idL=8
send([0x71, 0x00, 1, 8]); time.sleep(0.5)
for z in range(3):
    send([0x53, z, 24, 9] + kronos._val(-99)); time.sleep(0.1)
time.sleep(0.5)
print("peak with kit 136 kick muted:", hit())
for z in range(3):
    send([0x53, z, 24, 9] + kronos._val(lv[z])); time.sleep(0.1)
time.sleep(0.5)
print("peak after restore:", hit())
