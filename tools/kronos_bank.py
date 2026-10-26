"""Claude's own working bank on the Kronos: USER-G (SysEx bank byte 0x46, Bank Select LSB 14).

Slots 0-63 = drum programs, 64-127 = keys, all copies of factory sounds so factory sounds are
never edited. Edit THESE (live via kronos.py, or by changing the copied object before writing).
    python tools/kronos_bank.py init      # copy a drum and a piano program in and store the bank
"""
import sys
import time

import mido

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import kronos  # noqa: E402
from kronos_names import read_name, unpack  # noqa: E402

CLAUDE_BANK = 0x46  # USER-G


def pack(raw):
    """8-bit bytes -> Korg 7-bit sysex bytes (inverse of kronos_names.unpack)."""
    out = []
    for i in range(0, len(raw), 7):
        grp = raw[i:i + 7]
        out.append(sum(((b >> 7) & 1) << j for j, b in enumerate(grp)))
        out += [b & 0x7F for b in grp]
    return out


def dump_program(out, inp, bank, idx, wait=25):
    while inp.poll():
        pass
    out.send(mido.Message("sysex", data=[0x42, 0x30, 0x68, 0x72, 0x00, bank, idx >> 7, idx & 0x7F]))
    t = time.time()
    while time.time() - t < wait:
        for m in inp.iter_pending():
            d = list(m.data) if m.type == "sysex" else []
            if d[:5] == [0x42, 0x30, 0x68, 0x73, 0x00] and d[5] == bank and (d[6] << 7 | d[7]) == idx:
                return d[8], bytearray(unpack(d[9:]))  # (object version, bytes)
        time.sleep(0.01)
    raise SystemExit("no dump from Kronos for bank %02x slot %d" % (bank, idx))


def copy_program(out, inp, src_bank, src_idx, dst_idx, new_name):
    ver, raw = dump_program(out, inp, src_bank, src_idx)
    raw[0:24] = new_name.encode("latin-1")[:24].ljust(24, b"\x00")
    out.send(mido.Message("sysex", data=[0x42, 0x30, 0x68, 0x73, 0x00, CLAUDE_BANK, dst_idx >> 7,
                                         dst_idx & 0x7F, ver] + pack(bytes(raw))))
    time.sleep(0.5)


def store(out):
    out.send(mido.Message("sysex", data=[0x42, 0x30, 0x68, 0x76, 0x00, CLAUDE_BANK]))
    time.sleep(2)


if __name__ == "__main__":
    out, inp = mido.open_output("KRONOS SOUND"), mido.open_input("KRONOS KEYBOARD")
    # only fill slots that are empty or already ours, so a rerun never clobbers anything else
    for slot, src, name in ((0, (5, 95), "Claude Hip Hop Kit"), (64, (1, 33), "Claude Piano")):
        have = read_name(out, inp, CLAUDE_BANK, slot)
        assert have.startswith("Init") or have == name, "USER-G %d holds %r, stopping" % (slot, have)
        if have != name:
            copy_program(out, inp, src[0], src[1], slot, name)
    store(out)
    for i in (0, 64):
        print("USER-G %03d ->" % i, read_name(out, inp, CLAUDE_BANK, i))
