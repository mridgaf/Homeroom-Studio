"""Read the Kronos Global settings (SysEx obj 0x03) and print the MIDI / memory-protect bits. Read-only."""
import os
import sys
import time

import mido

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kronos_names import unpack  # noqa: E402


def read_global(wait=40):
    out, inp = mido.open_output("KRONOS SOUND"), mido.open_input("KRONOS KEYBOARD")
    while inp.poll():
        pass
    out.send(mido.Message("sysex", data=[0x42, 0x30, 0x68, 0x72, 0x03, 0x00, 0x00, 0x00]))
    t = time.time()
    while time.time() - t < wait:
        for m in inp.iter_pending():
            d = list(m.data) if m.type == "sysex" else []
            if d[:5] == [0x42, 0x30, 0x68, 0x73, 0x03]:
                return d[8], unpack(d[9:])
        time.sleep(0.02)
    raise SystemExit("no Global dump")


if __name__ == "__main__":
    ver, g = read_global()
    print("Global object version", ver, "bytes", len(g))
    b = lambda off, bit: (g[off] >> bit) & 1  # noqa: E731
    print("global MIDI channel (1-16):", g[24576] + 1)
    print("Local On", b(24577, 0), "| Bank Map (0=KORG,1=GM2)", b(24577, 4))
    print("Program Change Enable", b(24578, 0), "| Bank Change Enable", b(24578, 1), "| Control Change Enable", b(24578, 4),
          "| SysEx (Exclusive) Enable", b(24578, 5))
    print("Protect: Program", b(24580, 0), "Combi", b(24580, 1), "Song", b(24580, 2), "DrumKit", b(24580, 3), "WaveSeq", b(24580, 4))
