"""One check for the 808-into-key path: a C 808 shifted to another root
must MEASURE as that root and keep its length. Fails if the index, the
note lookup, or the shift breaks.

  ./.venv/bin/python tools/test_808_key.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np
import soundfile as sf
import beat_machine as bm
from sort_808s import analyse, NAMES

idx = bm._808_notes()
assert idx, "sample_808_index.json missing or empty (drive unplugged?)"

# a long, clean, confidently-C 808 to shift around
rows = json.loads(bm._808_INDEX_FILE.read_text())["files"]
src = next(p for p, a in sorted(rows.items())
           if a["note"] == "C" and a["note_src"] == "measured"
           and a["clarity"] >= 0.95 and a["sustain"] >= 1.5)
x, sr = sf.read(src, always_2d=True)
mono = x.mean(1)

assert bm._808_to_key(src, mono, "C")[1] == 0, "C to C must not shift"

for target, want_semis in (("D", 2), ("G", 7 - 12), ("A#", 10 - 12)):
    out, semis = bm._808_to_key(src, mono, target)
    assert out is not None, target
    assert semis == want_semis, (target, semis, want_semis)
    assert len(out) == len(mono), "shift changed the length"
    sf.write("/tmp/_808_check.wav", out, sr)
    got = analyse("/tmp/_808_check.wav")
    note = NAMES[int(round(got["midi"])) % 12]
    assert note == target, (target, note, got["clarity"])
    print("  C -> %-2s  %+3d semitones  measured %s  clarity %.2f"
          % (target, semis, note, got["clarity"]))

assert bm._808_to_key("/nope/not/a/file.wav", mono, "D") == (None, 0), \
    "an 808 with no known note must be refused, not shifted blind"
print("ok:", Path(src).name)
