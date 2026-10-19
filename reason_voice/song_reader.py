#!/usr/bin/env python3
"""Read the rack out of a saved Reason song: devices and cables.

READ-ONLY. Opens the file 'rb', never writes. Run it on a COPY if in doubt.

Usage:
    python3 reason_voice/song_reader.py "song.reason"          # table
    python3 reason_voice/song_reader.py "song.reason" --json   # machine form

What is decoded (checked on 'teste claude.reason', 13 devices / 42 records):
  * DEVIDESC record: id (u32 at payload byte 6), parent byte (5; 0xff = none),
    name (u32 length at 10, then text), device type (1 length byte, then text).
  * CNCT record (26-byte payload): five big-endian u32 at byte 6:
        (device_a, jack_a, device_b, jack_b, flag)
    Every cable is stored TWICE, once from each end, so records are folded into
    one undirected cable.
What is NOT decoded (do not claim it):
  * Which end is the output (direction).
  * Jack NAMES. Only jack numbers; L/R pairs are jack n and n+1.
  * 'flag' meaning.
  * Only the first FORM X15S block is read (re-saves leave stale older copies).
  * Songs with no DEVIDESC text (packed/compressed; demo songs) -> reported as
    unreadable, never guessed.
"""
import json
import mmap
import re
import struct
import sys


def read_song(path):
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            # Reason leaves old copies of the song in unused pages after a re-save.
            # Only the FIRST 'FORM <len> X15S' block is live; read inside it only.
            lo, hi = 0, len(mm)
            i = mm.find(b"FORM")
            while i != -1:
                if mm[i + 8:i + 12] == b"X15S":
                    lo = i
                    hi = min(len(mm), i + 8 + struct.unpack(">I", mm[i + 4:i + 8])[0])
                    break
                i = mm.find(b"FORM", i + 4)
            devices = {}
            order = []
            for m in re.compile(b"DEVIDESC").finditer(mm, lo, hi):
                s = m.start()
                ln = struct.unpack(">I", mm[s + 8:s + 12])[0]
                p = mm[s + 12:s + 12 + ln]
                if len(p) < 20:
                    continue
                dev_id = struct.unpack(">I", p[6:10])[0]
                nlen = struct.unpack(">I", p[10:14])[0]
                name = p[14:14 + nlen].decode("latin-1")
                rest = p[14 + nlen:].lstrip(b"\x00")
                tlen = rest[0] if rest else 0
                dtype = rest[1:1 + tlen].decode("latin-1").strip()
                devices[dev_id] = {"id": dev_id, "name": name, "type": dtype,
                                   "parent_byte": p[5]}
                order.append(dev_id)
            seen = set()
            cables = []
            for m in re.compile(b"CNCT\x00\x00\x00\x1a").finditer(mm, lo, hi):
                s = m.start() + 8
                p = mm[s:s + 26]
                if len(p) < 26:
                    continue
                a, ja, b, jb, flag = struct.unpack(">5I", p[6:26])
                key = frozenset(((a, ja), (b, jb)))
                if key in seen:
                    continue
                seen.add(key)
                cables.append({"a": a, "jack_a": ja, "b": b, "jack_b": jb})
            return {"path": path, "readable": bool(devices),
                    "devices": [devices[i] for i in order],
                    "cables": cables}
        finally:
            mm.close()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    song = read_song(sys.argv[1])
    if "--json" in sys.argv:
        print(json.dumps(song, indent=1))
        return 0
    if not song["readable"]:
        print("UNREADABLE: no device records in plain text (packed or compressed song).")
        return 2
    devs = {d["id"]: d for d in song["devices"]}
    for d in devs.values():
        if not d["name"].strip():
            d["name"] = f"(unnamed {d['type'] or 'device'} #{d['id']})"
    print(f"{len(devs)} devices, {len(song['cables'])} cables (each stored twice in the file)")
    print("\nDEVICES")
    for d in song["devices"]:
        print(f"  id {d['id']:>5}  {d['name']}  [{d['type']}]")
    print("\nCABLES (undirected; jack numbers, names not decoded)")
    for c in sorted(song["cables"], key=lambda c: (c["a"], c["jack_a"], c["b"], c["jack_b"])):
        print(f"  {devs.get(c['a'],{}).get('name','?')}:{c['jack_a']}  <->  "
              f"{devs.get(c['b'],{}).get('name','?')}:{c['jack_b']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
