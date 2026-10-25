"""One-time fill of ~/Desktop/Homeroom Loops for Reason from beats that
already have chunks (new beats and chunks sync themselves). Copies only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import beat_machine as bm  # noqa: E402

n = 0
for cd in sorted(bm.CHUNKS_ROOT.glob("*/* Chunks")):
    no = cd.name.split(" ", 1)[0]
    if not no.isdigit():
        continue                                  # e.g. Experiments
    wav = bm.beat_wav(int(no))
    if wav is None:
        print(f"skip (beat not on the drive): {cd.name}")
        continue
    out = bm.sync_reason_copy(wav, dj=cd.parent.name, chunks_dir=cd)
    n += 1
    print(f"{out.relative_to(bm.REASON_ROOT)}  ({len(list(out.iterdir()))} files)")
print(f"{n} beats copied into {bm.REASON_ROOT}")
