"""Find where a drum program stores its kit number, by comparing stored programs that use different kits (read-only)."""
import sys, time
import mido
sys.path.insert(0, "tools")
from kronos_names import unpack
HDR = [0x42, 0x30, 0x68]
out, inp = mido.open_output("KRONOS SOUND"), mido.open_input("KRONOS KEYBOARD")
def prog(bank, idx):
    while inp.poll(): pass
    out.send(mido.Message("sysex", data=HDR + [0x72, 0x00, bank, idx >> 7, idx & 0x7F]))
    t = time.time()
    while time.time() - t < 25:
        for m in inp.iter_pending():
            d = list(m.data) if m.type == "sysex" else []
            if d[:5] == HDR + [0x73, 0x00] and d[5] == bank and (d[6] << 7 | d[7]) == idx:
                return bytes(unpack(d[9:]))
        time.sleep(0.02)
names = {}
progs = {}
for label, bank, idx in (("F078 Studio Standard", 5, 78), ("F079 Funk", 5, 79), ("F080 Jazz/Brush", 5, 80), ("F081 Acoustic Pop", 5, 81), ("F095 Hip Hop (kit 4)", 5, 95), ("F096 Velo-Pitch HH", 5, 96)):
    progs[label] = prog(bank, idx)
    print(label, "->", None if progs[label] is None else len(progs[label]), flush=True)
base = progs["F095 Hip Hop (kit 4)"]
print("bytes 2480-2620 of F095:", list(base[2480:2620]))
labels = [k for k in progs if progs[k]]
cands = []
for o in range(2300, 2800):
    vals = [progs[k][o] for k in labels]
    if len(set(vals)) > 1 and all(v < 64 for v in vals):
        cands.append((o, vals))
print("offsets 2300-2800 where these programs differ and all values < 64:", cands[:40])

import os
sys.stdout.flush()
os._exit(0)  # MIDI/audio threads otherwise keep the finished script alive
