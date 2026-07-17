#!/usr/bin/env python3
"""Build a MIDI + JSON drum-pattern library from step-grid pattern specs.

Reads patterns_*.json (each an array of pattern dicts), renders one General MIDI
drum .mid file per pattern (channel 10), and writes a master catalog.json.
No third-party dependencies.
"""
import json, os, struct, glob, re

TPQN = 480            # ticks per quarter note
NUM_BARS = 2          # render each pattern as a 2-bar loop
NOTE_LEN = 40         # gate length in ticks for each hit

# track name -> General MIDI drum note number (channel 10)
GM = {
    "kick": 36, "snare": 38, "rim": 37, "clap": 39,
    "closed_hat": 42, "open_hat": 46,
    "tom_low": 41, "tom_mid": 45, "tom_hi": 50,
    "crash": 49, "ride": 51, "shaker": 82, "cowbell": 56,
}

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def vlq(n):
    """MIDI variable-length quantity."""
    buf = n & 0x7F
    n >>= 7
    out = bytearray()
    while n:
        buf <<= 8
        buf |= (n & 0x7F) | 0x80
        n >>= 7
    while True:
        out.append(buf & 0xFF)
        if buf & 0x80:
            buf >>= 8
        else:
            break
    return bytes(out)

def bar_ticks(time_sig):
    num, den = (int(x) for x in time_sig.split("/"))
    return int(num * (TPQN * 4 / den))

def build_track(pattern):
    steps = pattern["steps"]
    bt = bar_ticks(pattern["time_signature"])
    step_ticks = bt / steps
    # collect absolute-time events: (time, is_note_off, note, vel)
    events = []
    for tname, arr in pattern["tracks"].items():
        note = GM.get(tname)
        if note is None:
            continue
        for bar in range(NUM_BARS):
            for i, vel in enumerate(arr[:steps]):
                if vel and vel > 0:
                    t = int(round(bar * bt + i * step_ticks))
                    events.append((t, 0, note, min(int(vel), 127)))          # note on
                    events.append((t + NOTE_LEN, 1, note, 0))                # note off
    # sort: by time, note-offs before note-ons at same tick
    events.sort(key=lambda e: (e[0], -e[1]))

    body = bytearray()
    # tempo meta
    tempo = int(round(60_000_000 / pattern["bpm"]))
    body += vlq(0) + b"\xFF\x51\x03" + struct.pack(">I", tempo)[1:]
    # time signature meta
    num, den = (int(x) for x in pattern["time_signature"].split("/"))
    dd = {1:0,2:1,4:2,8:3,16:4}.get(den, 2)
    body += vlq(0) + b"\xFF\x58\x04" + bytes([num, dd, 24, 8])
    # program: keep default drum kit on ch10 (no program change needed)
    prev = 0
    for t, off, note, vel in events:
        delta = t - prev
        prev = t
        if off:
            body += vlq(delta) + bytes([0x89, note, 64])   # note off ch10
        else:
            body += vlq(delta) + bytes([0x99, note, vel])  # note on ch10
    body += vlq(0) + b"\xFF\x2F\x00"                        # end of track

    header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPQN)
    track = b"MTrk" + struct.pack(">I", len(body)) + bytes(body)
    return header + track

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out_root = os.path.join(base, "drum_library")
    genre_files = {
        "hip-hop": "patterns_hiphop.json",
        "electronic": "patterns_electronic.json",
        "rock": "patterns_rock.json",
    }
    catalog = []
    count = 0
    for genre, fname in genre_files.items():
        path = os.path.join(base, fname)
        with open(path) as f:
            patterns = json.load(f)
        gdir = os.path.join(out_root, "MIDI", genre)
        os.makedirs(gdir, exist_ok=True)
        used = {}
        for p in patterns:
            slug = slugify(p["name"])
            used[slug] = used.get(slug, 0) + 1
            if used[slug] > 1:
                slug = f"{slug}-{used[slug]}"
            fn = f"{slug}.mid"
            with open(os.path.join(gdir, fn), "wb") as mf:
                mf.write(build_track(p))
            catalog.append({
                "name": p["name"],
                "genre": genre,
                "subgenre": p.get("subgenre"),
                "bpm": p["bpm"],
                "time_signature": p["time_signature"],
                "steps": p["steps"],
                "feel": p.get("feel"),
                "bars": NUM_BARS,
                "instruments": list(p["tracks"].keys()),
                "midi_file": f"MIDI/{genre}/{fn}",
            })
            count += 1

    os.makedirs(out_root, exist_ok=True)
    with open(os.path.join(out_root, "catalog.json"), "w") as f:
        json.dump({
            "library": "Beat Generator Drum Pattern Library",
            "total_patterns": count,
            "gm_drum_map": GM,
            "ticks_per_quarter": TPQN,
            "bars_per_file": NUM_BARS,
            "patterns": catalog,
        }, f, indent=2)
    print(f"Wrote {count} MIDI files to {out_root}")
    # quick genre/subgenre tally
    from collections import Counter
    print("By genre:", dict(Counter(c["genre"] for c in catalog)))

if __name__ == "__main__":
    main()
