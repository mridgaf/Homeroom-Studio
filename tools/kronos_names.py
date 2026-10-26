"""Read program names straight from the Kronos (SysEx Object Dump Request, obj 0x13, read-only).

    python tools/kronos_names.py             # all INT + USER banks -> tools/kronos_unit_programs.json
    python tools/kronos_names.py 4a 80       # one name: bank byte (hex), index
Bank bytes (Korg SysEx doc): INT-A..F = 00-05, USER-A..G = 40-46, USER-AA..GG = 47-4D.
"""
import json
import os
import sys
import time

import mido

HERE = os.path.dirname(os.path.abspath(__file__))
USER = ["USER-" + x for x in ["A", "B", "C", "D", "E", "F", "G", "AA", "BB", "CC", "DD", "EE", "FF", "GG"]]


def unpack(b):
    """Korg 7-bit sysex bytes -> 8-bit bytes (every 8th byte holds the top bits of the next 7)."""
    out = []
    for i in range(0, len(b), 8):
        grp = b[i:i + 8]
        for j, v in enumerate(grp[1:]):
            out.append(v | (((grp[0] >> j) & 1) << 7))
    return bytes(out)


def read_name(out, inp, bank, idx, wait=0.4):
    while inp.poll():
        pass
    out.send(mido.Message("sysex", data=[0x42, 0x30, 0x68, 0x72, 0x13, bank, idx >> 7, idx & 0x7F]))
    t = time.time()
    while time.time() - t < wait:
        for m in inp.iter_pending():
            d = list(m.data) if m.type == "sysex" else []
            if d[:5] == [0x42, 0x30, 0x68, 0x73, 0x13] and d[5] == bank and (d[6] << 7 | d[7]) == idx:
                raw = unpack(d[9:])  # d[8] = object version
                return raw[:24].decode("latin-1").rstrip("\x00 ")
        time.sleep(0.005)
    return None


if __name__ == "__main__":
    out, inp = mido.open_output("KRONOS SOUND"), mido.open_input("KRONOS KEYBOARD")
    if len(sys.argv) == 3:
        print(repr(read_name(out, inp, int(sys.argv[1], 16), int(sys.argv[2]))))
        sys.exit()
    res = []
    # (bank name, SysEx bank byte, Bank Select LSB)
    banks = [("INT-" + c, i, i) for i, c in enumerate("ABCDEF")]
    banks += [(USER[n], 0x40 + n, 8 + n) for n in range(14)]
    for bank, sysex_bank, lsb in banks:
        for i in range(128):
            res.append({"bank": bank, "lsb": lsb, "pc": i, "text": read_name(out, inp, sysex_bank, i)})
        print(bank, "done", flush=True)
    json.dump(res, open(os.path.join(HERE, "kronos_unit_programs.json"), "w"), ensure_ascii=False, indent=0)
