# Chapter 02: Effects and signal processing
## Part 3 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- 2026-08-08-sound-engine-mixer.md (piece 1 of 8) — Sound Engine Multi-Stem Mixer Implementation Plan

(Next: Part 4 of 10)


=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer.md (piece 1 of 8)
ORIGINAL LOCATION: HS:docs/superpowers/plans/2026-08-08-sound-engine-mixer.md
=====================================================

# Sound Engine Multi-Stem Mixer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the Sound Engine app from a single-file effects preview into a real multi-channel mixer that loads a beat's already-rendered stems (one channel per drum), plus expose real parameter depth (not just one knob) on the EQ, Compressor, and Reverb panels.

**Architecture:** Unify "one file" and "one beat's worth of stems" into a single `project` concept with 1+ `channels`, both server-side (`sound_engine/server.py`) and client-side (`sound_engine/static/app.js`). Each channel gets its own copy of today's effect chain (now deeper). A new `sound_engine/library.py` scans the existing beat library (which already writes a `... Stems` folder per beat, no beat-generator changes needed) for beats that have stems to load.

**Tech Stack:** FastAPI + pedalboard (server, unchanged), Web Audio API (client, unchanged) — no new dependencies.

## Global Constraints

- Every new effect parameter must work live while audio plays (Web Audio side) — this is the app's whole reason for existing, per the owner. No parameter may be export-only.
- No VST/plugin hosting, no new effect types (Gate, Limiter, Multiband, Chorus, Phaser, Delay) — explicitly deferred, do not add them in this plan.
- Every new server-side parameter must map to a parameter that already exists in `tools/audio_engine.py`'s function signatures — confirmed exact signatures below. No new DSP functions.
- Exports always go to a NEW file in `~/Desktop/Homeroom Sound Engine Exports/` — never overwrite, matches existing behavior.
- Tests must never depend on the real beat library / `/Volumes/TBOTC 3` being mounted — use fixture folders under `tmp_path`.
- Follow this project's existing code style: terse comments only where the *why* isn't obvious from the code, dark-theme CSS variables already defined in `sound_engine/static/style.css`, reuse `.panel`/`.knob`/`.btn` classes rather than inventing new ones.
- Run `.venv/bin/python -m pytest tests/test_sound_engine.py tests/test_sound_engine_library.py -v` after every server-side task; full suite (`.venv/bin/python -m pytest tests/`) before considering the plan done.

## Confirmed existing signatures (do not re-verify, do not change)

```python
# tools/audio_engine.py
def eq3(L, R, low_db=0.0, low_hz=120.0, mid_db=0.0, mid_hz=800.0, mid_q=0.9,
        high_db=0.0, high_hz=8000.0, sr=None): ...

def glue_compressor(L, R, threshold_db=-14.0, ratio=2.5, attack_ms=12.0,
                     release_ms=180.0, makeup_db=2.0, sr=None): ...

def saturate(L, R, drive_db=6.0, mix=0.35, sr=None): ...

def stereo_width(L, R, width=1.0): ...

def loop_algo_reverb(L, R, room_size=0.5, damping=0.5, wet=0.25, dry=1.0,
                       width=1.0, sr=None): ...
# NOTE: loop_algo_reverb does not take `freeze` — algo_reverb does. Add
# freeze support to loop_algo_reverb in Task 12 (it's a 1-line pass-through,
# see that task).

def brickwall_limit(L, R, ceiling_db=-0.3, release_ms=100.0): ...

# sound_engine/dsp.py
def load_audio(path) -> tuple[np.ndarray, np.ndarray, int]: ...  # (L, R, sr)
def save_wav(path, L, R, sr) -> None: ...

# tools/beat_recipes.py
def lane_label(lane: str) -> str: ...  # "kick" -> "kick drum", etc.
```

Stem file layout on disk (confirmed by reading `tools/beat_machine.py` and
`tools/beat_recipes.py::write_stems`):
```
{beats_root}/{DJ Name}/{NO} {Names} {Title} Drums {BPM}bpm{meter}.wav   # main render
{beats_root}/{DJ Name}/{NO} {Names} {Title} Stems/                      # sibling folder
    {lane label}.wav                        # e.g. "hat.wav"
    {lane label} - {real sample name}.wav   # e.g. "kick drum - Cymatics Kong Kick 9.wav"
```

---

## Phase 1 — Server-side project/channel model + library browsing

### Task 1: `sound_engine/library.py` — find beats that have stems

**Files:**
- Create: `sound_engine/library.py`
- Test: `tests/test_sound_engine_library.py`

**Interfaces:**
- Produces: `resolve_beats_root() -> Path`, `list_beats(root: Path) -> list[dict]`,
  `find_beat(root: Path, beat_id: str) -> dict | None`. Each beat dict:
  `{"beat_id": str, "dj": str, "display_name": str, "bpm": float, "stem_count": int, "stems_dir": Path}`.

Do NOT import `tools/beat_machine.py` for its `_resolve_beats_root()` — that
module transitively imports `crew`, `pattern_gen`, `groove` and does real
sample-library work at import time (confirmed by reading its top-of-file
imports). Pulling that into the lightweight Sound Engine server on every
startup is wasteful and risks slow/flaky imports in a process that has
nothing to do with beat generation. Copy the small, fully self-contained
lookup logic instead (it only touches `os`/`json`/`pathlib`, zero
project-specific dependencies) — same behavior, same warnings, no heavy
import.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_sound_engine_library.py
"""Tests for sound_engine/library.py's beat-listing. Uses a fixture
folder under tmp_path — NEVER the real beats_root.json / TBOTC 3 path,
which isn't always mounted and must never be a test dependency."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
pytest.importorskip("pedalboard")

from sound_engine import library  # noqa: E402
from tools.make_drum_loops import write_wav24  # noqa: E402


def _make_fixture_beat(root: Path, dj="Test DJ", no="1", title="Sample Beat",
                        bpm="90", with_stems=True, n_stems=3):
    folder = root / dj
    folder.mkdir(parents=True, exist_ok=True)
    prefix = f"{no} {dj} {title}"
    main = folder / f"{prefix} Drums {bpm}bpm.wav"
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(main, sig, sig)
    if with_stems:
        stems_dir = folder / f"{prefix} Stems"
        stems_dir.mkdir()
        for i in range(n_stems):
            write_wav24(stems_dir / f"lane{i}.wav", sig, sig)
    return folder


def test_list_beats_finds_a_beat_with_stems(tmp_path):
    _make_fixture_beat(tmp_path)
    beats = library.list_beats(tmp_path)
    assert len(beats) == 1
    b = beats[0]
    assert b["dj"] == "Test DJ"
    assert b["bpm"] == 90.0
    assert b["stem_count"] == 3
    assert b["stems_dir"].is_dir()


def test_list_beats_skips_a_beat_with_no_stems_folder(tmp_path):
    _make_fixture_beat(tmp_path, with_stems=False)
    beats = library.list_beats(tmp_path)
    assert beats == []


def test_list_beats_skips_dotdirs(tmp_path):
    (tmp_path / ".recipes").mkdir()
    (tmp_path / ".recipes" / "1.json").write_text("{}")
    _make_fixture_beat(tmp_path)
    beats = library.list_beats(tmp_path)
    assert len(beats) == 1


def test_find_beat_round_trips_from_list_beats(tmp_path):
    _make_fixture_beat(tmp_path)
    beat_id = library.list_beats(tmp_path)[0]["beat_id"]
    found = library.find_beat(tmp_path, beat_id)
    assert found is not None
    assert found["stems_dir"].is_dir()


def test_find_beat_returns_none_for_unknown_id(tmp_path):
    assert library.find_beat(tmp_path, "nope/nope") is None


def test_resolve_beats_root_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("REASON_VOICE_BEATS_ROOT", str(tmp_path))
    assert library.resolve_beats_root() == tmp_path
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_sound_engine_library.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'sound_engine.library'`

- [ ] **Step 3: Write `sound_engine/library.py`**

```python
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
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
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
    stems_dir = Path(root) / dj / f"{prefix} Stems"
    if not stems_dir.is_dir():
        return None
    stem_files = [f for f in stems_dir.iterdir()
                  if f.is_file() and f.suffix.lower() == ".wav"]
    if not stem_files:
        return None
    return {"beat_id": beat_id, "dj": dj, "display_name": prefix,
            "stem_count": len(stem_files), "stems_dir": stems_dir}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_sound_engine_library.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add sound_engine/library.py tests/test_sound_engine_library.py
git commit -m "Add Sound Engine beat-library scanner (finds beats with stems)"
```

---

### Task 2: `server.py` — replace SESSIONS with PROJECTS, add `from-beat` / `from-upload`

**Files:**
- Modify: `sound_engine/server.py`
- Modify: `tests/test_sound_engine.py` (existing single-file tests move to the new API shape)

**Interfaces:**
- Consumes: `library.resolve_beats_root()`, `library.list_beats()`, `library.find_beat()` (Task 1); `dsp.load_audio()`, `dsp.save_wav()` (existing).
- Produces: `PROJECTS: dict[str, dict]`, `MAX_PROJECTS = 3`,
  `_evict_old_projects()`, `GET /api/library/beats`,
  `POST /api/project/from-beat`, `POST /api/project/from-upload`.
  Project shape (later tasks depend on these exact keys):
  ```python
  {
      "name": str,
      "channels": {
          lane_id: {
              "label": str, "sr": int,
              "dry": (np.ndarray, np.ndarray), "wet": (np.ndarray, np.ndarray),
              "gain_db": float, "pan": float, "muted": bool, "solo": bool,
          }
      },
      "src_paths": list[Path],
  }
  ```

This task removes the old `/api/upload` endpoint and `SESSIONS` dict
entirely — replaced, not kept alongside (no other consumer of the old API
exists besides `app.js`, which Task 8 rewrites; no back-compat shim per
this project's own conventions).

- [ ] **Step 1: Write the failing tests**

Replace the top of `tests/test_sound_engine.py` (imports and fixtures stay,
`_upload` helper changes shape) and add these new tests. This step rewrites
existing tests that assumed `/api/upload`/`file_id`, since that endpoint no
longer exists after this task:

```python
# tests/test_sound_engine.py — replace _upload() and add these tests.
# _upload() becomes:
def _upload(name="t.wav", data=None):
    return client.post("/api/project/from-upload",
                        files={"file": (name, data or _wav_bytes(), "audio/wav")})

# All existing tests that did `r.json()["file_id"]` now do
# `r.json()["project_id"]`, and all existing tests that did
# `client.post(f"/api/process/{file_id}", ...)` now do
# `client.post(f"/api/project/{project_id}/channel/upload/process", ...)`
# (lane_id is always "upload" for a from-upload project — see Step 3).
# Apply that rename across every existing test in this file as part of

=== END OF PART ===
