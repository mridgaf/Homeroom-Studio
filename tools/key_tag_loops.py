"""One-off: tag currently-unkeyed loops in given BOTC Sorted Loops folders
with a detected key, using the same method already used for the synth
batch (tools/reference_track.py's Krumhansl-Schmuckler detect_key()).

Usage (run from the project root, with its venv):
    ./.venv/bin/python tools/key_tag_loops.py \
        "/Volumes/TBOTC 3/Sample Packs/BOTC Sorted Loops/Melody" \
        "/Volumes/TBOTC 3/Sample Packs/BOTC Sorted Loops/Melody Loops"

For each audio file in the given folder(s) that has NO key token anywhere
in its name (same rule melodic_loops.py itself uses), this:
  1. Reads the audio and runs detect_key() + its own correlation score.
  2. Renames the file in place to append "_<Key>" (e.g. "_Gm", "_CMaj").
  3. Writes a confidence log next to the folder, same shape as
     synth_key_confidence_2026-09-18.txt, so low-confidence reads can be
     spot-checked by ear before being trusted in a beat.

Does NOT touch files that already have a key -- safe to re-run.
Does NOT guess tempo -- that's duration math or detect_tempo, a separate
pass; this is key only.
"""
from __future__ import annotations

import math
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np                                            # noqa: E402
from reference_track import _read_audio, chroma_of, _MAJOR, _MINOR, ROOTS  # noqa: E402

AUDIO_EXTS = {".wav", ".aif", ".aiff", ".mp3", ".flac", ".ogg"}
_KEY_TOKEN = re.compile(r"^([A-G])(#|b)?(major|maj|minor|min|m)?$", re.I)
_SPLIT = re.compile(r"[\s_\-(),]+")


def tokens_of(stem):
    return [t for t in _SPLIT.split(stem) if t]


def has_key(stem):
    for tok in tokens_of(stem):
        m = _KEY_TOKEN.match(tok)
        if m and m.group(1).upper() in "ABCDEFG":
            return True
    return False


def detect_key_scored(x):
    """(root, mode, score) -- same math as reference_track.detect_key,
    but also returns the winning correlation score (0-1ish) so low
    confidence reads can be flagged, matching the synth batch's log."""
    chroma = chroma_of(x)
    if chroma.sum() <= 0:
        return "C", "minor", 0.0
    c = chroma - chroma.mean()
    best = None
    for mode, profile in (("major", _MAJOR), ("minor", _MINOR)):
        p = profile - profile.mean()
        pn = math.sqrt(float((p ** 2).sum()))
        for r in range(12):
            v = np.roll(c, -r)
            vn = math.sqrt(float((v ** 2).sum()))
            score = float((v * p).sum()) / (vn * pn) if vn and pn else 0.0
            if best is None or score > best[0]:
                best = (score, r, mode)
    score, root, mode = best
    return ROOTS[root], mode, score


def mode_suffix(mode):
    return "Maj" if mode == "major" else "m"


def main(folders):
    for folder in folders:
        root = Path(folder)
        if not root.exists():
            print(f"SKIP (not found): {folder}")
            continue
        files = sorted(p for p in root.iterdir()
                        if p.is_file() and p.suffix.lower() in AUDIO_EXTS)
        results = []
        tagged = 0
        for path in files:
            if has_key(path.stem):
                continue
            try:
                x, _secs = _read_audio(path)
            except Exception as e:
                print(f"  COULD NOT READ: {path.name} ({e})")
                continue
            key_root, mode, score = detect_key_scored(x)
            new_stem = f"{path.stem}_{key_root}{mode_suffix(mode)}"
            new_path = path.with_name(new_stem + path.suffix)
            if new_path.exists():
                print(f"  COLLISION, skipping: {new_path.name}")
                continue
            path.rename(new_path)
            results.append((score, new_path.name))
            tagged += 1
        print(f"{root.name}: tagged {tagged} of {len(files)} files")
        if results:
            results.sort()
            log_path = root.parent / f"key_tag_confidence_{root.name.replace(' ', '_')}_{date.today()}.txt"
            with open(log_path, "w") as f:
                f.write(f"{root.name} -- key-tagging confidence, lowest first\n")
                f.write("=" * 60 + "\n")
                f.write("Method: tools/key_tag_loops.py -> reference_track.py's\n")
                f.write("chroma/Krumhansl-Schmuckler detect_key(). Always answers;\n")
                f.write("anything under ~0.5 is a coin-flip-level read -- worth a\n")
                f.write("quick listen before trusting it in a beat.\n\n")
                for score, name in results:
                    flag = "  <-- LOW CONFIDENCE, check by ear" if score < 0.5 else ""
                    f.write(f"{score:.3f}  {name:45s}{flag}\n")
            print(f"  confidence log: {log_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1:])
