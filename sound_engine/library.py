"""Finds beats in the owner's beat library that have a stems folder to
load into the mixer. Beat-generator output is untouched by this file —
every beat already writes a "... Stems" folder (tools/beat_recipes.py's
write_stems()); this module only reads what's already there.

resolve_beats_root() is a deliberate copy of tools/beat_machine.py's
_resolve_beats_root(), not an import of it — that module pulls in the
whole beat-generation stack (crew, pattern_gen, groove) with real work
at import time, which this lightweight server process has no reason to
pay for. Keep this copy's lookup order in sync with beat_machine.py's if
that one ever changes."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

_BPM_RE = re.compile(r"(\d+(?:\.\d+)?)bpm")


def resolve_beats_root() -> Path:
    env = os.environ.get("REASON_VOICE_BEATS_ROOT")
    if env:
        return Path(env).expanduser()
    cfg = Path(__file__).resolve().parent.parent / "beats_root.json"
    if cfg.exists():
        try:
            p = Path(json.loads(cfg.read_text())["root"]).expanduser()
            if p.exists():
                return p
            print(f"WARNING: beats_root.json points at {p}, which isn't "
                  "there — looking for the library elsewhere.")
        except (json.JSONDecodeError, KeyError, TypeError):
            print("WARNING: beats_root.json is broken — ignoring it.")
    home = Path.home()
    name = "Claude Drum Beats"
    cands = [home / "Documents/Samples" / name,
              home / "Library/Mobile Documents/com~apple~CloudDocs"
              / "Documents/Samples" / name]
    vols = Path("/Volumes")
    if vols.exists():
        for v in sorted(vols.iterdir()):
            cands += [v / name, v / "Samples" / name]
    empty = None
    for p in cands:
        try:
            if not p.is_dir():
                continue
            if next(p.rglob("*.wav"), None) is not None:
                return p
            empty = empty or p
        except OSError:
            continue
    return empty or cands[0]


def list_beats(root: Path) -> list[dict]:
    """Every beat under `root` that has a matching Stems folder, newest
    dj-folder-then-filename order (good enough for a picker; no claim of
    chronological accuracy)."""
    root = Path(root)
    if not root.is_dir():
        return []
    out = []
    for dj_dir in sorted(p for p in root.iterdir()
                          if p.is_dir() and not p.name.startswith(".")):
        for wav in sorted(dj_dir.glob("* Drums *.wav")):
            m = _BPM_RE.search(wav.name)
            if not m or " Drums " not in wav.name:
                continue
            prefix = wav.name.split(" Drums ")[0]
            stems_dir = dj_dir / f"{prefix} Stems"
            if not stems_dir.is_dir():
                continue
            stem_files = [f for f in stems_dir.iterdir()
                          if f.is_file() and f.suffix.lower() == ".wav"]
            if not stem_files:
                continue
            out.append({
                "beat_id": f"{dj_dir.name}/{prefix}",
                "dj": dj_dir.name,
                "display_name": prefix,
                "bpm": float(m.group(1)),
                "stem_count": len(stem_files),
                "stems_dir": stems_dir,
            })
    return out


def find_beat(root: Path, beat_id: str) -> dict | None:
    if "/" not in beat_id:
        return None
    dj, prefix = beat_id.split("/", 1)
    dj_dir = Path(root) / dj
    stems_dir = dj_dir / f"{prefix} Stems"
    if not stems_dir.is_dir():
        return None
    stem_files = [f for f in stems_dir.iterdir()
                  if f.is_file() and f.suffix.lower() == ".wav"]
    if not stem_files:
        return None
    # Find the corresponding Drums WAV to extract BPM
    drums_wav = dj_dir / f"{prefix} Drums *.wav"
    drums_files = sorted(dj_dir.glob(f"{prefix} Drums *.wav"))
    bpm = None
    for wav in drums_files:
        m = _BPM_RE.search(wav.name)
        if m:
            bpm = float(m.group(1))
            break
    return {"beat_id": beat_id, "dj": dj, "display_name": prefix,
            "bpm": bpm, "stem_count": len(stem_files), "stems_dir": stems_dir}
