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
# this task (mechanical, not shown line-by-line here).

def test_upload_creates_single_channel_project():
    r = _upload()
    assert r.status_code == 200
    data = r.json()
    assert "project_id" in data
    assert len(data["channels"]) == 1
    assert data["channels"][0]["lane_id"] == "upload"


def test_from_beat_creates_multi_channel_project(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    dj = tmp_path / "Test DJ"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(dj / "1 Test DJ Beat Drums 90bpm.wav", sig, sig)
    stems = dj / "1 Test DJ Beat Stems"
    stems.mkdir()
    write_wav24(stems / "kick.wav", sig, sig)
    write_wav24(stems / "snare.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)

    r = client.post("/api/project/from-beat", json={"beat_id": "Test DJ/1 Test DJ Beat"})
    assert r.status_code == 200
    data = r.json()
    assert len(data["channels"]) == 2
    lane_ids = {c["lane_id"] for c in data["channels"]}
    assert lane_ids == {"kick", "snare"}


def test_from_beat_unknown_id_returns_404(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)
    r = client.post("/api/project/from-beat", json={"beat_id": "nope/nope"})
    assert r.status_code == 404


def test_library_beats_endpoint_lists_fixture_beat(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    dj = tmp_path / "Test DJ"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(dj / "1 Test DJ Beat Drums 90bpm.wav", sig, sig)
    stems = dj / "1 Test DJ Beat Stems"
    stems.mkdir()
    write_wav24(stems / "kick.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)

    r = client.get("/api/library/beats")
    assert r.status_code == 200
    beats = r.json()["beats"]
    assert len(beats) == 1
    assert beats[0]["dj"] == "Test DJ"


def test_project_count_is_capped():
    for _ in range(server.MAX_PROJECTS + 2):
        _upload()
    assert len(server.PROJECTS) <= server.MAX_PROJECTS
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py -v`
Expected: FAIL — `AttributeError: module 'sound_engine.server' has no attribute 'BEATS_ROOT'` (and others, since the endpoints don't exist yet)

- [ ] **Step 3: Rewrite the session/project section of `server.py`**

Replace the `SESSIONS`/`MAX_SESSIONS`/`_evict_old_sessions`/`/api/upload`
block (current lines ~63-111) with:

```python
from . import library

BEATS_ROOT = library.resolve_beats_root()

# project state: project_id -> {name, channels: {lane_id -> {...}},
# src_paths}. In-memory, single local user, gone on restart. Capped at
# MAX_PROJECTS — a multi-channel project holds 10+ stereo float64 arrays
# instead of one file's 2, so the per-entry memory cost is proportionally
# higher than the old single-file SESSIONS; cap lower to compensate.
PROJECTS: dict[str, dict] = {}
MAX_PROJECTS = 3


def _evict_old_projects():
    while len(PROJECTS) > MAX_PROJECTS:
        old_id, old = next(iter(PROJECTS.items()))
        del PROJECTS[old_id]
        for p in old.get("src_paths", []):
            Path(p).unlink(missing_ok=True)
        for lane_id in old.get("channels", {}):
            for variant in ("dry", "wet"):
                (RENDERS / f"{old_id}_{lane_id}_{variant}.wav").unlink(missing_ok=True)


def _new_channel(label, L, R, sr):
    return {"label": label, "sr": sr, "dry": (L, R), "wet": (L, R),
            "gain_db": 0.0, "pan": 0.0, "muted": False, "solo": False}


def _project_response(project_id, project):
    return {
        "project_id": project_id,
        "name": project["name"],
        "channels": [
            {"lane_id": lane_id, "label": ch["label"],
             "sample_rate": ch["sr"],
             "duration_s": round(len(ch["dry"][0]) / ch["sr"], 2)}
            for lane_id, ch in project["channels"].items()
        ],
    }


@app.get("/api/library/beats")
async def library_beats():
    if not BEATS_ROOT.is_dir():
        return JSONResponse({"beats": [],
                              "warning": f"Beat library not found at {BEATS_ROOT} "
                                         "— is the drive plugged in?"})
    beats = library.list_beats(BEATS_ROOT)
    return JSONResponse({
        "beats": [{"beat_id": b["beat_id"], "dj": b["dj"],
                    "display_name": b["display_name"], "bpm": b["bpm"],
                    "stem_count": b["stem_count"]} for b in beats],
        "warning": None,
    })


@app.post("/api/project/from-beat")
async def project_from_beat(body: dict):
    beat_id = body.get("beat_id", "")
    beat = library.find_beat(BEATS_ROOT, beat_id)
    if beat is None:
        return JSONResponse({"error": "unknown or stem-less beat_id"}, status_code=404)
    project_id = uuid.uuid4().hex[:12]
    channels = {}
    for wav in sorted(beat["stems_dir"].glob("*.wav")):
        lane_id = wav.stem
        try:
            L, R, sr = dsp.load_audio(wav)
        except Exception:
            continue  # one bad stem shouldn't sink the whole load
        channels[lane_id] = _new_channel(lane_id, L, R, sr)
    if not channels:
        return JSONResponse({"error": "no readable stems in that beat"}, status_code=400)
    PROJECTS[project_id] = {"name": beat["display_name"], "channels": channels,
                              "src_paths": []}
    _evict_old_projects()
    return JSONResponse(_project_response(project_id, PROJECTS[project_id]))


@app.post("/api/project/from-upload")
async def project_from_upload(file: UploadFile = File(...)):
    safe_name = Path(file.filename or "upload").name
    project_id = uuid.uuid4().hex[:12]
    src = UPLOADS / f"{project_id}_{safe_name}"
    with open(src, "wb") as f:
        f.write(await file.read())
    try:
        L, R, sr = dsp.load_audio(src)
    except Exception as e:
        src.unlink(missing_ok=True)
        return JSONResponse({"error": f"couldn't read that as audio ({e})"},
                             status_code=400)
    PROJECTS[project_id] = {
        "name": safe_name,
        "channels": {"upload": _new_channel(safe_name, L, R, sr)},
        "src_paths": [src],
    }
    _evict_old_projects()
    return JSONResponse(_project_response(project_id, PROJECTS[project_id]))
```

Also update the module docstring's mention of "Drag in any audio file...
export the result as a new file" to note beats can be loaded from the
library too — one sentence, not a rewrite.

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py -v`
Expected: the tests from Step 1 pass. Tests referencing the now-removed
`/api/process/{file_id}` / `/api/export/{file_id}` / `/api/audio/{file_id}/...`
still fail — that's Task 3, not this task. Confirm the failures are ONLY
in those (unmigrated) tests, nothing else.

- [ ] **Step 5: Commit**

```bash
git add sound_engine/server.py tests/test_sound_engine.py
git commit -m "Replace Sound Engine's single-file sessions with multi-channel projects"
```

---

### Task 3: `server.py` — per-channel process / audio / export endpoints

**Files:**
- Modify: `sound_engine/server.py`
- Modify: `tests/test_sound_engine.py`

**Interfaces:**
- Consumes: `PROJECTS` (Task 2), `tools/audio_engine.py`'s functions (signatures above).
- Produces: `POST /api/project/{project_id}/channel/{lane_id}/process`,
  `GET /api/project/{project_id}/channel/{lane_id}/{dry|wet}`,
  `POST /api/project/{project_id}/export`.

This task intentionally does NOT add the new deepened parameters
(`low_hz`, `comp_makeup_db`, `reverb_damping`, etc.) — those come in
Phase 3 (Tasks 10-12) once the mixer itself is proven working end-to-end
with today's existing parameter set. Keep this task's `process()` body
parameters identical in spirit to today's, just scoped per-channel plus
the 3 new channel-strip fields (`gain_db`, `pan`, `muted`).

- [ ] **Step 1: Write the failing tests**

```python
def test_channel_process_export_round_trip():
    project_id = _upload().json()["project_id"]
    r2 = client.post(f"/api/project/{project_id}/channel/upload/process",
                      json={"low_db": 3.0, "high_db": -2.0})
    assert r2.status_code == 200
    r3 = client.post(f"/api/project/{project_id}/export")
    assert r3.status_code == 200
    out_path = Path(r3.json()["path"])
    assert out_path.exists()
    out_path.unlink()


def test_channel_process_unknown_channel_returns_404():
    project_id = _upload().json()["project_id"]
    r = client.post(f"/api/project/{project_id}/channel/doesnotexist/process", json={})
    assert r.status_code == 404


def test_export_sums_multiple_channels_louder_than_one_muted(tmp_path, monkeypatch):
    from tools.make_drum_loops import write_wav24
    dj = tmp_path / "Test DJ"
    dj.mkdir()
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(dj / "1 Test DJ Beat Drums 90bpm.wav", sig, sig)
    stems = dj / "1 Test DJ Beat Stems"
    stems.mkdir()
    write_wav24(stems / "kick.wav", sig, sig)
    write_wav24(stems / "snare.wav", sig, sig)
    monkeypatch.setattr(server, "BEATS_ROOT", tmp_path)
    project_id = client.post("/api/project/from-beat",
                              json={"beat_id": "Test DJ/1 Test DJ Beat"}).json()["project_id"]

    client.post(f"/api/project/{project_id}/channel/kick/process", json={})
    client.post(f"/api/project/{project_id}/channel/snare/process", json={})
    both = client.post(f"/api/project/{project_id}/export")
    both_peak = _wav_peak(Path(both.json()["path"]))

    client.post(f"/api/project/{project_id}/channel/snare/process", json={"muted": True})
    one = client.post(f"/api/project/{project_id}/export")
    one_peak = _wav_peak(Path(one.json()["path"]))

    assert both_peak > one_peak
    Path(both.json()["path"]).unlink()
    Path(one.json()["path"]).unlink()


def _wav_peak(path):
    with wave.open(str(path)) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
    return float(np.abs(data).max())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py -v`
Expected: FAIL — endpoints don't exist yet (404 on paths that aren't
registered, or `NameError`/route-not-found style failures).

- [ ] **Step 3: Add the endpoints to `server.py`**

Replace the old `/api/process/{file_id}`, `/api/audio/{file_id}/{variant}`,
`/api/export/{file_id}` block with:

```python
def _apply_channel_chain(L, R, sr, p):
    ae = dsp.audio_engine
    low_db = float(p.get("low_db", 0.0))
    mid_db = float(p.get("mid_db", 0.0))
    high_db = float(p.get("high_db", 0.0))
    comp_threshold_db = float(p.get("comp_threshold_db", -24.0))
    comp_ratio = float(p.get("comp_ratio", 1.0))
    comp_attack_ms = float(p.get("comp_attack_ms", 12.0))
    comp_release_ms = float(p.get("comp_release_ms", 180.0))
    sat_drive_db = float(p.get("sat_drive_db", 6.0))
    sat_mix = float(p.get("sat_mix", 0.0))
    width = float(p.get("width", 1.0))
    reverb_size_s = float(p.get("reverb_size_s", 2.0))
    reverb_mix = float(p.get("reverb_mix", 0.0))

    L, R = ae.eq3(L, R, sr=sr, low_db=low_db, mid_db=mid_db, high_db=high_db)
    if comp_ratio > 1.0:
        L, R = ae.glue_compressor(L, R, sr=sr, threshold_db=comp_threshold_db,
                                    ratio=comp_ratio, attack_ms=comp_attack_ms,
                                    release_ms=comp_release_ms, makeup_db=0.0)
    if sat_mix > 0.0:
        L, R = ae.saturate(L, R, sr=sr, drive_db=sat_drive_db, mix=sat_mix)
    if width != 1.0:
        L, R = ae.stereo_width(L, R, width=width)
    if reverb_mix > 0.0:
        room_size = min(1.0, reverb_size_s / 6.0)
        L, R = ae.loop_algo_reverb(L, R, sr=sr, room_size=room_size,
                                     wet=reverb_mix, dry=1 - reverb_mix)
    return L, R


def _get_channel(project_id, lane_id):
    project = PROJECTS.get(project_id)
    if project is None:
        return None, None
    channel = project["channels"].get(lane_id)
    return project, channel


@app.post("/api/project/{project_id}/channel/{lane_id}/process")
async def channel_process(project_id: str, lane_id: str, params: dict):
    project, channel = _get_channel(project_id, lane_id)
    if channel is None:
        return JSONResponse({"error": "unknown project_id or lane_id"}, status_code=404)
    try:
        L, R = channel["dry"]
        L, R = _apply_channel_chain(L.copy(), R.copy(), channel["sr"], params)
        channel["gain_db"] = float(params.get("gain_db", channel["gain_db"]))
        channel["pan"] = float(params.get("pan", channel["pan"]))
        channel["muted"] = bool(params.get("muted", channel["muted"]))
        channel["solo"] = bool(params.get("solo", channel["solo"]))
    except (TypeError, ValueError):
        return JSONResponse({"error": "invalid parameter values"}, status_code=400)
    channel["wet"] = (L, R)
    return JSONResponse({"ok": True})


@app.get("/api/project/{project_id}/channel/{lane_id}/{variant}")
async def channel_audio(project_id: str, lane_id: str, variant: str):
    project, channel = _get_channel(project_id, lane_id)
    if channel is None or variant not in ("dry", "wet"):
        return JSONResponse({"error": "not found"}, status_code=404)
    L, R = channel[variant]
    out = RENDERS / f"{project_id}_{lane_id}_{variant}.wav"
    dsp.save_wav(out, L, R, channel["sr"])
    return FileResponse(out, media_type="audio/wav",
                         headers={"Cache-Control": "no-store"})


def _pan_gains(pan):
    # equal-power pan law, -1..1 -> (left_gain, right_gain)
    theta = (pan + 1) * (np.pi / 4)
    return np.cos(theta), np.sin(theta)


@app.post("/api/project/{project_id}/export")
async def project_export(project_id: str):
    project = PROJECTS.get(project_id)
    if project is None:
        return JSONResponse({"error": "unknown project_id"}, status_code=404)
    channels = project["channels"]
    any_solo = any(c["solo"] for c in channels.values())
    audible = [c for c in channels.values()
               if (c["solo"] if any_solo else not c["muted"])]
    if not audible:
        return JSONResponse({"error": "nothing to export — every channel is muted"},
                             status_code=400)
    sr = next(iter(channels.values()))["sr"]
    n = max(len(c["wet"][0]) for c in audible)
    mixL = np.zeros(n)
    mixR = np.zeros(n)
    for c in audible:
        L, R = c["wet"]
        g = 10 ** (c["gain_db"] / 20.0)
        panL, panR = _pan_gains(c["pan"])
        mixL[:len(L)] += L * g * panL
        mixR[:len(R)] += R * g * panR
    ae = dsp.audio_engine
    mixL, mixR = ae.brickwall_limit(mixL, mixR, ceiling_db=-0.3)
    stem = re.sub(r'[\\/:*?"<>|]', "_", project["name"]).strip() or "mix"
    stamp = datetime.now().strftime("%Y-%m-%d %H%M%S.%f")
    out = EXPORT_DIR / f"{stem} (engine) {stamp}.wav"
    dsp.save_wav(out, mixL, mixR, sr)
    return JSONResponse({"path": str(out)})
```

Add `import re` and `import numpy as np` to `server.py`'s imports if not
already present (check the top of the file before adding — `re` and
`numpy` are not currently imported there since the old code never needed
them; `dsp.py` already imports `numpy as np` but `server.py` needs its
own import for `_pan_gains`/the mix-summing code above).

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py -v`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add sound_engine/server.py tests/test_sound_engine.py
git commit -m "Add per-channel process/export endpoints with gain/pan/mute/solo mixing"
```

---

## Phase 2 — Client-side multi-channel mixer

### Task 4: `index.html` + `style.css` — channel list, beat picker, detail-rack shell

**Files:**
- Modify: `sound_engine/static/index.html`
- Modify: `sound_engine/static/style.css`

**Interfaces:**
- Produces: DOM elements Task 5's `app.js` binds to —
  `#browseBeatsBtn`, `#beatPickerModal` (with `#beatPickerList`,
  `#beatPickerClose`), `#channelList` (empty `<div>`, populated by JS),
  `#channelRackTitle`, `#channelRack` (holds the same EQ/Comp/Sat/Width/
  Reverb `.panel` markup as today, once, reused for whichever channel is
  selected — NOT duplicated per channel).

- [ ] **Step 1: Add the beat picker + channel list markup**

In `index.html`, replace the single `<section id="dropzone">` /
`<section id="workspace">` pair with:

```html
    <section id="dropzone" class="dropzone">
      <p>Drop an audio file here, or</p>
      <label class="btn">
        Choose a file
        <input type="file" id="fileInput" accept="audio/*" hidden>
      </label>
      <button id="browseBeatsBtn" class="btn">Browse your beats</button>
      <p class="hint">WAV, MP3, M4A, AIFF, FLAC — most audio formats work.</p>
    </section>

    <div id="beatPickerModal" class="modal hidden">
      <div class="modal-card">
        <div class="modal-header">
          <h2>Pick a beat</h2>
          <button id="beatPickerClose" class="btn">Close</button>
        </div>
        <p id="beatPickerWarning" class="meta hidden"></p>
        <div id="beatPickerList" class="beatList"></div>
      </div>
    </div>

    <section id="workspace" class="workspace hidden">
      <div class="filebar">
        <span id="fileName">—</span>
        <span id="fileMeta" class="meta"></span>
      </div>

      <div class="transport">
        <button id="playBtn" class="btn primary">▶ Play</button>
        <button id="stopBtn" class="btn">■ Stop</button>
        <label class="loopToggle">
          <input type="checkbox" id="loopToggle"> Loop
        </label>
        <label class="loopToggle">
          <input type="checkbox" id="bypassToggle"> Bypass (A/B)
        </label>
        <span id="playStatus" class="meta"></span>
      </div>

      <div class="mixer">
        <div id="channelList" class="channelList"></div>

        <div class="channelRack">
          <h2 id="channelRackTitle">—</h2>

          <div class="panel">
            <h2>EQ — live, moves while it plays</h2>
            <div class="knobs">
              <div class="knob">
                <label for="lowDb">Low <span id="lowDbVal">0.0</span> dB</label>
                <input type="range" id="lowDb" min="-18" max="18" step="0.5" value="0">
                <span class="freq">@ 120 Hz shelf</span>
              </div>
              <div class="knob">
                <label for="midDb">Mid <span id="midDbVal">0.0</span> dB</label>
                <input type="range" id="midDb" min="-18" max="18" step="0.5" value="0">
                <span class="freq">@ 800 Hz bell</span>
              </div>
              <div class="knob">
                <label for="highDb">High <span id="highDbVal">0.0</span> dB</label>
                <input type="range" id="highDb" min="-18" max="18" step="0.5" value="0">
                <span class="freq">@ 8 kHz shelf</span>
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Compressor</h2>
            <div class="knobs">
              <div class="knob">
                <label for="compThreshold">Threshold <span id="compThresholdVal">-24</span> dB</label>
                <input type="range" id="compThreshold" min="-60" max="0" step="1" value="-24">
              </div>
              <div class="knob">
                <label for="compRatio">Ratio <span id="compRatioVal">1.0</span>:1</label>
                <input type="range" id="compRatio" min="1" max="20" step="0.5" value="1">
                <span class="freq">1 = off</span>
              </div>
              <div class="knob">
                <label for="compAttack">Attack <span id="compAttackVal">12</span> ms</label>
                <input type="range" id="compAttack" min="1" max="200" step="1" value="12">
              </div>
              <div class="knob">
                <label for="compRelease">Release <span id="compReleaseVal">180</span> ms</label>
                <input type="range" id="compRelease" min="20" max="1000" step="10" value="180">
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Saturation</h2>
            <div class="knobs">
              <div class="knob">
                <label for="satDrive">Drive <span id="satDriveVal">6</span> dB</label>
                <input type="range" id="satDrive" min="0" max="24" step="0.5" value="6">
              </div>
              <div class="knob">
                <label for="satMix">Mix <span id="satMixVal">0</span>%</label>
                <input type="range" id="satMix" min="0" max="100" step="1" value="0">
                <span class="freq">0 = off</span>
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Reverb</h2>
            <div class="knobs">
              <div class="knob">
                <label for="revSize">Size <span id="revSizeVal">2.0</span> s</label>
                <input type="range" id="revSize" min="0.2" max="6" step="0.1" value="2.0">
              </div>
              <div class="knob">
                <label for="revMix">Mix <span id="revMixVal">0</span>%</label>
                <input type="range" id="revMix" min="0" max="100" step="1" value="0">
                <span class="freq">0 = off</span>
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Stereo Width</h2>
            <div class="knobs">
              <div class="knob">
                <label for="widthKnob">Width <span id="widthKnobVal">1.0</span>x</label>
                <input type="range" id="widthKnob" min="0" max="2" step="0.05" value="1.0">
                <span class="freq">0 = mono, 1 = unchanged, 2 = wide</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="exportbar">
        <button id="exportBtn" class="btn primary">Export mix as new file</button>
        <span id="exportStatus" class="meta"></span>
      </div>
    </section>
```

(This step keeps today's EQ/Comp/Sat/Width/Reverb panel markup verbatim
except renaming the Reverb `<h2>` context and export button label —
Phase 3, Tasks 10-12, add the new sliders into these same panels. Don't
add them here; this task is purely the mixer shell.)

- [ ] **Step 2: Add channel-list, modal, and mixer-layout CSS**

Append to `style.css`:

```css
main { max-width: 900px; }

.modal {
  position: fixed; inset: 0;
  background: rgba(10, 12, 16, 0.7);
  display: flex; align-items: center; justify-content: center;
  z-index: 10;
}
.modal-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  width: min(520px, 90vw);
  max-height: 80vh;
  overflow-y: auto;
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px;
}
.beatList { display: flex; flex-direction: column; gap: 6px; }
.beatItem {
  display: flex; justify-content: space-between; align-items: baseline;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
}
.beatItem:hover { border-color: var(--accent); }
.beatItem .meta { font-size: 12px; }

.mixer { display: flex; gap: 20px; align-items: flex-start; }
.channelList {
  flex: 0 0 220px;
  display: flex; flex-direction: column; gap: 6px;
}
.channelStrip {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
}
.channelStrip.selected { border-color: var(--accent); }
.channelStrip .label {
  font-size: 13px; font-weight: 600;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  margin-bottom: 6px;
}
.channelStrip .row { display: flex; align-items: center; gap: 8px; }
.channelStrip input[type=range] { flex: 1; accent-color: var(--accent); }
.channelStrip .mutesolo { display: flex; gap: 4px; margin-top: 6px; }
.channelStrip .mutesolo button {
  flex: 1; font-size: 11px; padding: 4px;
  background: var(--bg); border: 1px solid var(--border); color: var(--muted);
  border-radius: 6px; cursor: pointer;
}
.channelStrip .mutesolo button.active.mute { background: #a33; color: #fff; border-color: #a33; }
.channelStrip .mutesolo button.active.solo { background: var(--accent); color: #0a0e14; border-color: var(--accent); }

.channelRack { flex: 1; min-width: 0; }
.channelRack > h2 { margin: 0 0 12px; font-size: 18px; }
```

- [ ] **Step 3: Commit**

```bash
git add sound_engine/static/index.html sound_engine/static/style.css
git commit -m "Add mixer shell markup: beat picker modal, channel list, shared effects rack"
```

(No automated test for this step — it's static markup with no behavior
yet. Task 5 wires it up and gets browser-verified.)

---

### Task 5: `app.js` — multi-channel rewrite

**Files:**
- Modify: `sound_engine/static/app.js` (full rewrite of the module-level
  singleton section; the pure-function helpers `makeSaturationCurve` /
  `makeReverbIR` stay as-is)

**Interfaces:**
- Consumes: `/api/library/beats`, `/api/project/from-beat`,
  `/api/project/from-upload`, `/api/project/{id}/channel/{lane}/process`,
  `/api/project/{id}/channel/{lane}/{dry|wet}`, `/api/project/{id}/export`
  (Tasks 2-3). DOM elements from Task 4.
- Produces: nothing consumed by later Phase-2 tasks (this is the last
  Phase-2 code task); Phase 3 (Tasks 10-12) edits this file's per-channel
  `buildChannelGraph()` and the slider-binding section.

This is the biggest single task in the plan. Structure it as: a
`channels` object keyed by `lane_id`, each holding the exact node set
`buildGraph()` builds today (renamed `buildChannelGraph`), plus a
per-channel fader/pan/mute node, all summing into one `masterGain`.

- [ ] **Step 1: Replace the module-level state and add project/channel loading**

```javascript
// sound_engine/static/app.js — top of file, replaces today's singleton
// `let lowShelf, midPeak, ...` block. Every channel gets its OWN full
// copy of the effect chain (previously the only chain); they all sum
// into masterGain -> destination.
let projectId = null;
let audioCtx = null;
let masterGain = null;
let channels = {};       // lane_id -> channel object, see buildChannelGraph()
let channelOrder = [];   // lane_ids, display order
let selectedLane = null;
let isPlaying = false;

const dropzone = document.getElementById("dropzone");
const workspace = document.getElementById("workspace");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const fileMeta = document.getElementById("fileMeta");
const playBtn = document.getElementById("playBtn");
const stopBtn = document.getElementById("stopBtn");
const loopToggle = document.getElementById("loopToggle");
const bypassToggle = document.getElementById("bypassToggle");
const playStatus = document.getElementById("playStatus");
const exportBtn = document.getElementById("exportBtn");
const exportStatus = document.getElementById("exportStatus");
const channelListEl = document.getElementById("channelList");
const channelRackTitle = document.getElementById("channelRackTitle");
const browseBeatsBtn = document.getElementById("browseBeatsBtn");
const beatPickerModal = document.getElementById("beatPickerModal");
const beatPickerList = document.getElementById("beatPickerList");
const beatPickerWarning = document.getElementById("beatPickerWarning");
const beatPickerClose = document.getElementById("beatPickerClose");

const RAMP_SECONDS = 0.02;

dropzone.addEventListener("dragover", e => e.preventDefault());
dropzone.addEventListener("drop", e => {
  e.preventDefault();
  const f = e.dataTransfer.files[0];
  if (f) loadUpload(f);
});
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) loadUpload(fileInput.files[0]);
});

browseBeatsBtn.addEventListener("click", openBeatPicker);
beatPickerClose.addEventListener("click", () => beatPickerModal.classList.add("hidden"));

async function openBeatPicker() {
  beatPickerModal.classList.remove("hidden");
  beatPickerList.innerHTML = "<p class=\"meta\">Loading…</p>";
  const res = await fetch("/api/library/beats");
  const data = await res.json();
  if (data.warning) {
    beatPickerWarning.textContent = data.warning;
    beatPickerWarning.classList.remove("hidden");
  } else {
    beatPickerWarning.classList.add("hidden");
  }
  beatPickerList.innerHTML = "";
  if (data.beats.length === 0) {
    beatPickerList.innerHTML = "<p class=\"meta\">No beats with stems found.</p>";
    return;
  }
  for (const b of data.beats) {
    const item = document.createElement("div");
    item.className = "beatItem";
    item.innerHTML = `<span>${b.dj} — ${b.display_name}</span>` +
      `<span class="meta">${b.bpm} bpm · ${b.stem_count} stems</span>`;
    item.addEventListener("click", () => loadBeat(b.beat_id));
    beatPickerList.appendChild(item);
  }
}

async function loadBeat(beatId) {
  beatPickerModal.classList.add("hidden");
  const res = await fetch("/api/project/from-beat", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ beat_id: beatId }),
  });
  const data = await res.json();
  if (!res.ok) { alert("Couldn't load that beat: " + (data.error || res.statusText)); return; }
  await openProject(data);
}

async function loadUpload(file) {
  const form = new FormData();
  form.append("file", file);
  let res, data;
  try {
    res = await fetch("/api/project/from-upload", { method: "POST", body: form });
    data = await res.json();
  } catch (e) {
    alert("Couldn't reach the Sound Engine server: " + e);
    return;
  }
  if (!res.ok || data.error) {
    alert("Couldn't load that file: " + (data.error || res.statusText));
    return;
  }
  await openProject(data);
}

async function openProject(data) {
  stopPlayback();
  projectId = data.project_id;
  fileName.textContent = data.name;
  fileMeta.textContent = `${data.channels.length} channel(s)`;
  exportStatus.textContent = "";
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  masterGain = audioCtx.createGain();
  masterGain.connect(audioCtx.destination);

  channels = {};
  channelOrder = [];
  for (const ch of data.channels) {
    const arrayBuf = await (await fetch(
      `/api/project/${projectId}/channel/${ch.lane_id}/dry?t=${Date.now()}`)).arrayBuffer();
    let audioBuffer = await audioCtx.decodeAudioData(arrayBuf);
    if (audioBuffer.numberOfChannels === 1) {
      const stereo = audioCtx.createBuffer(2, audioBuffer.length, audioBuffer.sampleRate);
      stereo.copyToChannel(audioBuffer.getChannelData(0), 0);
      stereo.copyToChannel(audioBuffer.getChannelData(0), 1);
      audioBuffer = stereo;
    }
    channels[ch.lane_id] = buildChannelGraph(ch.lane_id, ch.label, audioBuffer);
    channelOrder.push(ch.lane_id);
  }
  renderChannelList();
  selectChannel(channelOrder[0]);
  dropzone.classList.add("hidden");
  workspace.classList.remove("hidden");
}
```

- [ ] **Step 2: Add `buildChannelGraph` (today's `buildGraph`, per-channel)**

```javascript
function makeSaturationCurve(driveDb) { /* unchanged from today — keep as-is */ }
function makeReverbIR(ctx, seconds) { /* unchanged from today — keep as-is */ }

function buildChannelGraph(laneId, label, audioBuffer) {
  const lowShelf = audioCtx.createBiquadFilter();
  lowShelf.type = "lowshelf"; lowShelf.frequency.value = 120; lowShelf.gain.value = 0;

  const midPeak = audioCtx.createBiquadFilter();
  midPeak.type = "peaking"; midPeak.frequency.value = 800; midPeak.Q.value = 0.9; midPeak.gain.value = 0;

  const highShelf = audioCtx.createBiquadFilter();
  highShelf.type = "highshelf"; highShelf.frequency.value = 8000; highShelf.gain.value = 0;

  const compressor = audioCtx.createDynamicsCompressor();
  compressor.threshold.value = -24; compressor.ratio.value = 1;
  compressor.attack.value = 0.012; compressor.release.value = 0.18; compressor.knee.value = 0;

  const satDry = audioCtx.createGain(); satDry.gain.value = 1;
  const satWet = audioCtx.createGain(); satWet.gain.value = 0;
  const waveshaper = audioCtx.createWaveShaper();
  waveshaper.curve = makeSaturationCurve(6); waveshaper.oversample = "4x";
  const satOut = audioCtx.createGain(); satOut.gain.value = 1;

  const splitter = audioCtx.createChannelSplitter(2);
  const merger = audioCtx.createChannelMerger(2);
  const midGainL = audioCtx.createGain(); midGainL.gain.value = 0.5;
  const midGainR = audioCtx.createGain(); midGainR.gain.value = 0.5;
  const midBus = audioCtx.createGain(); midBus.gain.value = 1;
  const sideGainL = audioCtx.createGain(); sideGainL.gain.value = 0.5;
  const sideGainR = audioCtx.createGain(); sideGainR.gain.value = -0.5;
  const sideBus = audioCtx.createGain(); sideBus.gain.value = 1;
  const sideWidth = audioCtx.createGain(); sideWidth.gain.value = 1;
  const sideNeg = audioCtx.createGain(); sideNeg.gain.value = -1;
  splitter.connect(midGainL, 0); midGainL.connect(midBus);
  splitter.connect(midGainR, 1); midGainR.connect(midBus);
  splitter.connect(sideGainL, 0); sideGainL.connect(sideBus);
  splitter.connect(sideGainR, 1); sideGainR.connect(sideBus);
  sideBus.connect(sideWidth);
  midBus.connect(merger, 0, 0);
  sideWidth.connect(merger, 0, 0);
  midBus.connect(merger, 0, 1);
  sideWidth.connect(sideNeg);
  sideNeg.connect(merger, 0, 1);

  const revDry = audioCtx.createGain(); revDry.gain.value = 1;
  const revWet = audioCtx.createGain(); revWet.gain.value = 0;
  const convolver = audioCtx.createConvolver();
  convolver.normalize = true;
  convolver.buffer = makeReverbIR(audioCtx, 2.0);
  const revOut = audioCtx.createGain(); revOut.gain.value = 1;

  const wetGain = audioCtx.createGain();
  const bypassGain = audioCtx.createGain();

  lowShelf.connect(midPeak).connect(highShelf).connect(compressor);
  compressor.connect(satDry).connect(satOut);
  compressor.connect(satWet).connect(waveshaper).connect(satOut);
  satOut.connect(splitter);
  merger.connect(revDry).connect(revOut);
  merger.connect(revWet).connect(convolver).connect(revOut);
  revOut.connect(wetGain);
  wetGain.gain.value = 1; bypassGain.gain.value = 0;

  const fader = audioCtx.createGain(); fader.gain.value = 1;
  const panner = audioCtx.createStereoPanner ? audioCtx.createStereoPanner() : null;
  wetGain.connect(panner || fader);
  if (panner) panner.connect(fader);
  bypassGain.connect(panner || fader);
  fader.connect(masterGain);

  return {
    laneId, label, audioBuffer, sourceNode: null,
    lowShelf, midPeak, highShelf, compressor,
    satDry, satWet, waveshaper, satOut,
    splitter, merger, sideWidth,
    revDry, revWet, convolver, revOut,
    wetGain, bypassGain, fader, panner,
    muted: false, solo: false, lastSatDriveTick: 0, lastSatDriveApplied: null,
    lastRevSizeTick: 0, lastRevSizeApplied: null,
  };
}
```

(Note: this factors today's `setBypass()`-driven crossfade into per-
channel `wetGain`/`bypassGain` as before; Step 4 wires the play/bypass
logic per channel.)

- [ ] **Step 3: Channel list rendering, selection, mute/solo/fader/pan**

```javascript
function renderChannelList() {
  channelListEl.innerHTML = "";
  for (const laneId of channelOrder) {
    const ch = channels[laneId];
    const strip = document.createElement("div");
    strip.className = "channelStrip" + (laneId === selectedLane ? " selected" : "");
    strip.innerHTML = `
      <div class="label">${ch.label}</div>
      <div class="row"><input type="range" class="faderInput" min="-24" max="12" step="0.5" value="0"></div>
      <div class="row"><input type="range" class="panInput" min="-1" max="1" step="0.05" value="0"></div>
      <div class="mutesolo">
        <button class="mute">M</button>
        <button class="solo">S</button>
      </div>`;
    strip.addEventListener("click", e => {
      if (e.target.tagName !== "INPUT" && e.target.tagName !== "BUTTON") selectChannel(laneId);
    });
    strip.querySelector(".faderInput").addEventListener("input", e => {
      ch.fader.gain.setTargetAtTime(10 ** (parseFloat(e.target.value) / 20),
                                     audioCtx.currentTime, RAMP_SECONDS);
    });
    strip.querySelector(".panInput").addEventListener("input", e => {
      if (ch.panner) ch.panner.pan.setTargetAtTime(parseFloat(e.target.value),
                                                     audioCtx.currentTime, RAMP_SECONDS);
    });
    strip.querySelector(".mute").addEventListener("click", () => toggleMute(laneId));
    strip.querySelector(".solo").addEventListener("click", () => toggleSolo(laneId));
    channelListEl.appendChild(strip);
    applyMuteSoloUI(laneId, strip);
  }
}

function applyMuteSoloUI(laneId, strip) {
  const ch = channels[laneId];
  strip.querySelector(".mute").classList.toggle("active", ch.muted);
  strip.querySelector(".solo").classList.toggle("active", ch.solo);
}

function recomputeAudibility() {
  const anySolo = Object.values(channels).some(c => c.solo);
  for (const laneId of channelOrder) {
    const ch = channels[laneId];
    const audible = anySolo ? ch.solo : !ch.muted;
    const t = audioCtx.currentTime;
    ch.fader.gain.cancelScheduledValues(t);
    // audibility is a hard mute, independent of the fader's own dB value —
    // reflect the current fader slider rather than always forcing unity
    const strip = channelListEl.children[channelOrder.indexOf(laneId)];
    const faderDb = strip ? parseFloat(strip.querySelector(".faderInput").value) : 0;
    ch.fader.gain.setTargetAtTime(audible ? 10 ** (faderDb / 20) : 0, t, RAMP_SECONDS);
  }
}

function toggleMute(laneId) {
  channels[laneId].muted = !channels[laneId].muted;
  renderChannelList();
  recomputeAudibility();
  syncChannelToServer(laneId);
}

function toggleSolo(laneId) {
  channels[laneId].solo = !channels[laneId].solo;
  renderChannelList();
  recomputeAudibility();
  syncChannelToServer(laneId);
}

function selectChannel(laneId) {
  selectedLane = laneId;
  channelRackTitle.textContent = channels[laneId].label;
  loadRackFromChannel(channels[laneId]);
  renderChannelList();
}
```

- [ ] **Step 4: Rack binding (today's `bindRamped` section, now channel-aware)**

```javascript
function loadRackFromChannel(ch) {
  document.getElementById("lowDb").value = ch.lowShelf.gain.value;
  document.getElementById("lowDbVal").textContent = ch.lowShelf.gain.value.toFixed(1);
  document.getElementById("midDb").value = ch.midPeak.gain.value;
  document.getElementById("midDbVal").textContent = ch.midPeak.gain.value.toFixed(1);
  document.getElementById("highDb").value = ch.highShelf.gain.value;
  document.getElementById("highDbVal").textContent = ch.highShelf.gain.value.toFixed(1);
  document.getElementById("compThreshold").value = ch.compressor.threshold.value;
  document.getElementById("compThresholdVal").textContent = ch.compressor.threshold.value.toFixed(0);
  document.getElementById("compRatio").value = ch.compressor.ratio.value;
  document.getElementById("compRatioVal").textContent = ch.compressor.ratio.value.toFixed(1);
  document.getElementById("compAttack").value = (ch.compressor.attack.value * 1000).toFixed(0);
  document.getElementById("compAttackVal").textContent = (ch.compressor.attack.value * 1000).toFixed(0);
  document.getElementById("compRelease").value = (ch.compressor.release.value * 1000).toFixed(0);
  document.getElementById("compReleaseVal").textContent = (ch.compressor.release.value * 1000).toFixed(0);
  document.getElementById("satMix").value = ch.satWet.gain.value * 100;
  document.getElementById("satMixVal").textContent = Math.round(ch.satWet.gain.value * 100);
  document.getElementById("revMix").value = ch.revWet.gain.value * 100;
  document.getElementById("revMixVal").textContent = Math.round(ch.revWet.gain.value * 100);
  document.getElementById("widthKnob").value = ch.sideWidth.gain.value;
  document.getElementById("widthKnobVal").textContent = ch.sideWidth.gain.value.toFixed(2);
}

function currentChannel() { return channels[selectedLane]; }

function bindRamped(id, getNode, param, transform) {
  const el = document.getElementById(id);
  const out = document.getElementById(id + "Val");
  el.addEventListener("input", () => {
    const raw = parseFloat(el.value);
    out.textContent = raw.toFixed(raw >= 10 || raw <= -10 ? 0 : 1);
    const ch = currentChannel();
    const n = ch && getNode(ch);
    if (!n || !audioCtx) return;
    const v = transform ? transform(raw) : raw;
    n[param].setTargetAtTime(v, audioCtx.currentTime, RAMP_SECONDS);
    syncChannelToServer(selectedLane);
  });
}
bindRamped("lowDb", ch => ch.lowShelf, "gain");
bindRamped("midDb", ch => ch.midPeak, "gain");
bindRamped("highDb", ch => ch.highShelf, "gain");
bindRamped("compThreshold", ch => ch.compressor, "threshold");
bindRamped("compRatio", ch => ch.compressor, "ratio");
bindRamped("compAttack", ch => ch.compressor, "attack", ms => ms / 1000);
bindRamped("compRelease", ch => ch.compressor, "release", ms => ms / 1000);
bindRamped("satMix", ch => ch.satWet, "gain", pct => pct / 100);
bindRamped("widthKnob", ch => ch.sideWidth, "gain");
bindRamped("revMix", ch => ch.revWet, "gain", pct => pct / 100);

document.getElementById("satMix").addEventListener("input", e => {
  const ch = currentChannel();
  if (!ch || !audioCtx) return;
  ch.satDry.gain.setTargetAtTime(1 - parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
});
document.getElementById("revMix").addEventListener("input", e => {
  const ch = currentChannel();
  if (!ch || !audioCtx) return;
  ch.revDry.gain.setTargetAtTime(1 - parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
});

document.getElementById("satDrive").addEventListener("input", e => {
  document.getElementById("satDriveVal").textContent = parseFloat(e.target.value).toFixed(1);
  const ch = currentChannel(); if (!ch) return;
  const now = performance.now();
  if (now - ch.lastSatDriveTick < 50) return;
  ch.lastSatDriveTick = now;
  const val = parseFloat(e.target.value);
  if (val === ch.lastSatDriveApplied) return;
  ch.lastSatDriveApplied = val;
  ch.waveshaper.curve = makeSaturationCurve(val);
});
document.getElementById("satDrive").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  const val = parseFloat(e.target.value);
  if (val === ch.lastSatDriveApplied) return;
  ch.lastSatDriveApplied = val;
  ch.waveshaper.curve = makeSaturationCurve(val);
});
document.getElementById("revSize").addEventListener("input", e => {
  document.getElementById("revSizeVal").textContent = parseFloat(e.target.value).toFixed(1);
  const ch = currentChannel(); if (!ch) return;
  const now = performance.now();
  if (now - ch.lastRevSizeTick < 50) return;
  ch.lastRevSizeTick = now;
  const val = parseFloat(e.target.value);
  if (val === ch.lastRevSizeApplied) return;
  ch.lastRevSizeApplied = val;
  ch.convolver.buffer = makeReverbIR(audioCtx, val);
});
document.getElementById("revSize").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  const val = parseFloat(e.target.value);
  if (val === ch.lastRevSizeApplied) return;
  ch.lastRevSizeApplied = val;
  ch.convolver.buffer = makeReverbIR(audioCtx, val);
});

function syncChannelToServer(laneId) {
  // fire-and-forget — keeps the server's copy of this channel's settings
  // current for export; live audio never waits on this
  if (!projectId) return;
  const ch = channels[laneId];
  const params = selectedLane === laneId ? {
    low_db: ch.lowShelf.gain.value, mid_db: ch.midPeak.gain.value, high_db: ch.highShelf.gain.value,
    comp_threshold_db: ch.compressor.threshold.value, comp_ratio: ch.compressor.ratio.value,
    comp_attack_ms: ch.compressor.attack.value * 1000, comp_release_ms: ch.compressor.release.value * 1000,
    sat_mix: ch.satWet.gain.value, width: ch.sideWidth.gain.value, reverb_mix: ch.revWet.gain.value,
    gain_db: 0, pan: 0, muted: ch.muted, solo: ch.solo,
  } : { muted: ch.muted, solo: ch.solo };
  fetch(`/api/project/${projectId}/channel/${laneId}/process`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
}
```

- [ ] **Step 5: Playback (all channels in sync), bypass, safety net, export**

```javascript
function play() {
  const bufferLen = channelOrder.length ? channels[channelOrder[0]].audioBuffer.length : 0;
  if (!bufferLen) return;
  stopPlayback();
  const startAt = audioCtx.currentTime + 0.05;  // small common offset, same clock for every source
  for (const laneId of channelOrder) {
    const ch = channels[laneId];
    const src = audioCtx.createBufferSource();
    src.buffer = ch.audioBuffer;
    src.loop = loopToggle.checked;
    src.connect(ch.lowShelf);
    src.connect(ch.bypassGain);
    src.start(startAt);
    ch.sourceNode = src;
  }
  setBypass(bypassToggle.checked);
  recomputeAudibility();
  isPlaying = true;
  playStatus.textContent = "Playing…";
  channels[channelOrder[0]].sourceNode.onended = () => {
    if (isPlaying) { isPlaying = false; playStatus.textContent = ""; }
  };
}

function setBypass(on) {
  const t = audioCtx.currentTime;
  for (const laneId of channelOrder) {
    const ch = channels[laneId];
    ch.wetGain.gain.setTargetAtTime(on ? 0 : 1, t, RAMP_SECONDS);
    ch.bypassGain.gain.setTargetAtTime(on ? 1 : 0, t, RAMP_SECONDS);
  }
}
bypassToggle.addEventListener("change", () => { if (audioCtx) setBypass(bypassToggle.checked); });

function stopPlayback() {
  for (const laneId of channelOrder) {
    const ch = channels[laneId];
    if (ch.sourceNode) {
      try { ch.sourceNode.onended = null; ch.sourceNode.stop(); } catch (e) {}
      ch.sourceNode.disconnect();
      ch.sourceNode = null;
    }
  }
  isPlaying = false;
  playStatus.textContent = "";
}

playBtn.addEventListener("click", () => { audioCtx.resume(); play(); });
stopBtn.addEventListener("click", stopPlayback);

document.addEventListener("visibilitychange", () => {
  if (document.hidden && isPlaying && channelOrder.length &&
      channels[channelOrder[0]].sourceNode && channels[channelOrder[0]].sourceNode.loop) {
    stopPlayback();
  }
});
window.addEventListener("pagehide", stopPlayback);

exportBtn.addEventListener("click", async () => {
  if (!projectId || exportBtn.disabled) return;
  exportBtn.disabled = true;
  exportStatus.textContent = "Rendering final mix…";
  try {
    for (const laneId of channelOrder) syncChannelToServer(laneId);
    await new Promise(r => setTimeout(r, 150));  // let the syncs land server-side
    const res = await fetch(`/api/project/${projectId}/export`, { method: "POST" });
    const data = await res.json();
    exportStatus.textContent = data.path ? `Saved: ${data.path}` : `Export failed: ${data.error || ""}`;
  } finally {
    exportBtn.disabled = false;
  }
});
```

- [ ] **Step 6: Delete the now-dead single-chain code**

Remove the old module-level `let lowShelf, audioCtx, ...` block, the old
`upload()`, `buildGraph()`, and the old single-set `bindRamped(...)` calls
— all superseded by Steps 1-5 above. Confirm nothing in the file still
references a bare (non-channel-scoped) `lowShelf`/`compressor`/etc.

Run: `grep -n "^let lowShelf\|function upload(\|function buildGraph(" sound_engine/static/app.js`
Expected: no matches (all removed/renamed).

- [ ] **Step 7: Commit**

```bash
git add sound_engine/static/app.js
git commit -m "Rewrite Sound Engine's live-preview engine for multi-channel mixing"
```

---

### Task 6: Manual browser verification of the mixer (no automated test — client-only)

**Files:** none (verification only)

This mirrors how this project already verifies Web-Audio-only behavior
(see the earlier bug-fix session's pattern in `DECISIONS.md`) — pytest
cannot exercise a live audio graph, so this is a scripted manual pass via
the Browser MCP tools.

- [ ] **Step 1: Start the server and open it**

```bash
lsof -ti:8767 | xargs -r kill 2>/dev/null; sleep 0.3
SOUND_ENGINE_NO_BROWSER=1 ./.venv/bin/python -m sound_engine.server > /tmp/se_verify.log 2>&1 &
sleep 1.5 && curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8767/
```
Expected: `200`

- [ ] **Step 2: Verify "Browse your beats" against a real (or fixture) library**

Open the app in the Browser pane, click "Browse your beats." If the real
library is mounted, confirm real beats list with correct DJ/bpm/stem
count. If not mounted, confirm the warning text renders (not a silent
empty list) — matches the spec's error-handling requirement.

- [ ] **Step 3: Load a beat, confirm N channels, confirm sync playback**

Pick a beat with several stems. Confirm the channel list shows one strip
per stem. Click Play — confirm (via `javascript_tool`, checking each
channel's `sourceNode.buffer` start time / `isPlaying`) that every
channel's source started, and listen for all stems audible together, not
just the first.

- [ ] **Step 4: Confirm per-channel knobs are independent**

Select channel A, move its EQ; select channel B, confirm its EQ is
unaffected (still transparent); switch back to A, confirm its EQ value
persisted (re-opening a channel's rack must show that channel's actual
current values, not reset to default — verify `loadRackFromChannel`
reads live node values correctly).

- [ ] **Step 5: Confirm mute/solo affects audible output**

Mute one channel, confirm its fader ramps toward 0 (`ch.fader.gain.value`
approaches 0 shortly after). Solo a different channel, confirm every
other channel's fader ramps toward 0 regardless of its own mute state.

- [ ] **Step 6: Confirm export produces a real multi-channel mix**

Export, confirm the file exists and is longer/louder-summed than any
single channel alone (reuse the same peak-comparison technique as
`test_export_sums_multiple_channels_louder_than_one_muted`, but on the
real exported file via `javascript_tool` + `fetch`, or via a quick Bash
`python -c` peak check on the resulting WAV).

- [ ] **Step 7: Clean up**

```bash
lsof -ti:8767 | xargs -r kill 2>/dev/null
rm -f ~/.homeroom_engine/uploads/* ~/.homeroom_engine/renders/* 2>/dev/null
```
Delete any test export left in `~/Desktop/Homeroom Sound Engine Exports/`.

No commit for this task (verification only, no file changes) — if any
step fails, that's a bug to fix as its own small commit before continuing
to Phase 3.

---

## Phase 3 — Deepen EQ, Compressor, Reverb

### Task 7: Deepen EQ — expose frequency + mid Q

**Files:**
- Modify: `sound_engine/static/index.html`
- Modify: `sound_engine/static/app.js`
- Modify: `sound_engine/server.py`
- Modify: `tests/test_sound_engine.py`

**Interfaces:**
- Consumes: `eq3(..., low_hz, mid_hz, mid_q, high_hz, ...)` (already exists,
  confirmed signature above — no Python changes needed beyond wiring the
  request body through).

- [ ] **Step 1: Write the failing test**

```python
def test_eq_frequency_params_reach_export():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"low_db": 6.0, "low_hz": 60.0})
    wet_low_hz_60 = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"low_db": 6.0, "low_hz": 300.0})
    wet_low_hz_300 = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert not np.array_equal(wet_low_hz_60[0], wet_low_hz_300[0])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_eq_frequency_params_reach_export -v`
Expected: FAIL (both currently produce the same output — `low_hz` isn't
read from the request body yet)

- [ ] **Step 3: Wire the new params through `_apply_channel_chain` in `server.py`**

```python
    low_hz = float(p.get("low_hz", 120.0))
    mid_hz = float(p.get("mid_hz", 800.0))
    mid_q = float(p.get("mid_q", 0.9))
    high_hz = float(p.get("high_hz", 8000.0))
    ...
    L, R = ae.eq3(L, R, sr=sr, low_db=low_db, low_hz=low_hz,
                   mid_db=mid_db, mid_hz=mid_hz, mid_q=mid_q,
                   high_db=high_db, high_hz=high_hz)
```

(Replace the existing `low_db = ...` block and the `ae.eq3(...)` call
inside `_apply_channel_chain` from Task 3 — insert the four new `float(p.get(...))`
lines alongside the existing ones, and pass the four new kwargs.)

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_eq_frequency_params_reach_export -v`
Expected: PASS

- [ ] **Step 5: Add frequency/Q sliders to the EQ panel in `index.html`**

Replace the EQ `.panel` block from Task 4 with:

```html
          <div class="panel">
            <h2>EQ — live, moves while it plays</h2>
            <div class="knobs">
              <div class="knob">
                <label for="lowDb">Low <span id="lowDbVal">0.0</span> dB</label>
                <input type="range" id="lowDb" min="-18" max="18" step="0.5" value="0">
                <label for="lowHz" class="freq">@ <span id="lowHzVal">120</span> Hz shelf</label>
                <input type="range" id="lowHz" min="40" max="400" step="5" value="120">
              </div>
              <div class="knob">
                <label for="midDb">Mid <span id="midDbVal">0.0</span> dB</label>
                <input type="range" id="midDb" min="-18" max="18" step="0.5" value="0">
                <label for="midHz" class="freq">@ <span id="midHzVal">800</span> Hz bell</label>
                <input type="range" id="midHz" min="200" max="4000" step="20" value="800">
                <label for="midQ" class="freq">Q <span id="midQVal">0.9</span></label>
                <input type="range" id="midQ" min="0.2" max="4" step="0.1" value="0.9">
              </div>
              <div class="knob">
                <label for="highDb">High <span id="highDbVal">0.0</span> dB</label>
                <input type="range" id="highDb" min="-18" max="18" step="0.5" value="0">
                <label for="highHz" class="freq">@ <span id="highHzVal">8000</span> Hz shelf</label>
                <input type="range" id="highHz" min="2000" max="16000" step="100" value="8000">
              </div>
            </div>
          </div>
```

- [ ] **Step 6: Wire the new sliders live in `app.js`**

Add to the `bindRamped(...)` calls block (Task 5, Step 4):

```javascript
bindRamped("lowHz", ch => ch.lowShelf, "frequency");
bindRamped("midHz", ch => ch.midPeak, "frequency");
bindRamped("midQ", ch => ch.midPeak, "Q");
bindRamped("highHz", ch => ch.highShelf, "frequency");
```

Add the four new fields to `loadRackFromChannel()`:

```javascript
  document.getElementById("lowHz").value = ch.lowShelf.frequency.value;
  document.getElementById("lowHzVal").textContent = ch.lowShelf.frequency.value.toFixed(0);
  document.getElementById("midHz").value = ch.midPeak.frequency.value;
  document.getElementById("midHzVal").textContent = ch.midPeak.frequency.value.toFixed(0);
  document.getElementById("midQ").value = ch.midPeak.Q.value;
  document.getElementById("midQVal").textContent = ch.midPeak.Q.value.toFixed(1);
  document.getElementById("highHz").value = ch.highShelf.frequency.value;
  document.getElementById("highHzVal").textContent = ch.highShelf.frequency.value.toFixed(0);
```

And to `syncChannelToServer()`'s `params` object:

```javascript
    low_hz: ch.lowShelf.frequency.value, mid_hz: ch.midPeak.frequency.value,
    mid_q: ch.midPeak.Q.value, high_hz: ch.highShelf.frequency.value,
```

- [ ] **Step 7: Run full sound_engine test suite, then manually re-verify frequency sliders move live in the browser (repeat Task 6's Step 1 setup)**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py tests/test_sound_engine_library.py -v`
Expected: all pass.

- [ ] **Step 8: Commit**

```bash
git add sound_engine/static/index.html sound_engine/static/app.js sound_engine/server.py tests/test_sound_engine.py
git commit -m "Deepen EQ panel: expose frequency and mid-band Q, not just gain"
```

---

### Task 8: Deepen Compressor — real makeup gain

**Files:**
- Modify: `sound_engine/static/index.html`
- Modify: `sound_engine/static/app.js`
- Modify: `sound_engine/server.py`
- Modify: `tests/test_sound_engine.py`

**Interfaces:**
- Consumes: `glue_compressor(..., makeup_db=...)` (already exists).

- [ ] **Step 1: Write the failing test**

```python
def test_compressor_makeup_gain_reaches_export():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"comp_ratio": 4.0, "comp_makeup_db": 0.0})
    quiet = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"comp_ratio": 4.0, "comp_makeup_db": 12.0})
    loud = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert np.abs(loud[0]).max() > np.abs(quiet[0]).max()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_compressor_makeup_gain_reaches_export -v`
Expected: FAIL

- [ ] **Step 3: Wire `comp_makeup_db` through `_apply_channel_chain` in `server.py`**

```python
    comp_makeup_db = float(p.get("comp_makeup_db", 0.0))
    ...
    if comp_ratio > 1.0:
        L, R = ae.glue_compressor(L, R, sr=sr, threshold_db=comp_threshold_db,
                                    ratio=comp_ratio, attack_ms=comp_attack_ms,
                                    release_ms=comp_release_ms, makeup_db=comp_makeup_db)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_compressor_makeup_gain_reaches_export -v`
Expected: PASS

- [ ] **Step 5: Add a Makeup Gain slider to the Compressor panel in `index.html`**

Add inside the Compressor `.knobs` div (Task 4):

```html
              <div class="knob">
                <label for="compMakeup">Makeup <span id="compMakeupVal">0</span> dB</label>
                <input type="range" id="compMakeup" min="0" max="24" step="0.5" value="0">
              </div>
```

- [ ] **Step 6: Wire it live in `app.js`**

Live side needs a real gain stage — the Web Audio `DynamicsCompressorNode`
has no makeup-gain concept, matching why `server.py`'s export needed a
separate `pb.Gain` stage too (see `glue_compressor`'s pedalboard chain).
Add a `makeupGain` node per channel in `buildChannelGraph()` (Task 5,
Step 2): insert `const makeupGain = audioCtx.createGain(); makeupGain.gain.value = 1;`
next to the `compressor` node, splice it into the chain
(`compressor.connect(makeupGain)` then change `compressor.connect(satDry)`
/ `compressor.connect(satWet)` to `makeupGain.connect(satDry)` /
`makeupGain.connect(satWet)`), and add `makeupGain` to the returned
channel object.

```javascript
bindRamped("compMakeup", ch => ch.makeupGain, "gain", db => 10 ** (db / 20));
```

Add to `loadRackFromChannel()`:
```javascript
  const makeupDb = 20 * Math.log10(ch.makeupGain.gain.value);
  document.getElementById("compMakeup").value = makeupDb;
  document.getElementById("compMakeupVal").textContent = makeupDb.toFixed(1);
```

Add to `syncChannelToServer()`'s `params`:
```javascript
    comp_makeup_db: 20 * Math.log10(ch.makeupGain.gain.value),
```

- [ ] **Step 7: Run tests, then manually re-verify in browser**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py tests/test_sound_engine_library.py -v`
Expected: all pass. In the browser, confirm turning Makeup up while
audio plays audibly raises the level.

- [ ] **Step 8: Commit**

```bash
git add sound_engine/static/index.html sound_engine/static/app.js sound_engine/server.py tests/test_sound_engine.py
git commit -m "Deepen Compressor panel: add real makeup gain"
```

---

### Task 9: Deepen Reverb — independent wet/dry, damping, width, freeze

**Files:**
- Modify: `sound_engine/static/index.html`
- Modify: `sound_engine/static/app.js`
- Modify: `sound_engine/server.py`
- Modify: `tools/audio_engine.py` (one-line addition — `loop_algo_reverb` needs a `freeze` passthrough, it currently doesn't accept one; `algo_reverb` already does)
- Modify: `tests/test_sound_engine.py`
- Modify: `tests/test_audio_engine.py` (regression test for the new `freeze` passthrough)

**Interfaces:**
- Consumes: `algo_reverb(..., width, freeze, ...)` (exists),
  `loop_algo_reverb` (exists, gains a new `freeze` kwarg this task).

This is the biggest depth win — Reverb goes from 2 knobs to 6. Do it in
two passes: wet/dry decoupling first (smallest, proves the pattern),
then damping/width/freeze together (all three touch the same live-side
reverb send path).

- [ ] **Step 1: Write the failing test for independent wet/dry**

```python
def test_reverb_wet_and_dry_are_independent():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.4, "reverb_dry": 1.0})
    both = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.4, "reverb_dry": 0.0})
    wet_only = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert not np.array_equal(both[0], wet_only[0])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_reverb_wet_and_dry_are_independent -v`
Expected: FAIL (today `dry` is always computed as `1 - reverb_mix`, never read from the body)

- [ ] **Step 3: Decouple wet/dry in `_apply_channel_chain`**

```python
    reverb_size_s = float(p.get("reverb_size_s", 2.0))
    reverb_mix = float(p.get("reverb_mix", 0.0))
    reverb_dry = float(p.get("reverb_dry", 1.0 - reverb_mix))
    reverb_damping = float(p.get("reverb_damping", 0.5))
    reverb_width = float(p.get("reverb_width", 1.0))
    reverb_freeze = bool(p.get("reverb_freeze", False))
    ...
    if reverb_mix > 0.0 or reverb_freeze:
        room_size = min(1.0, reverb_size_s / 6.0)
        L, R = ae.loop_algo_reverb(L, R, sr=sr, room_size=room_size,
                                     damping=reverb_damping, wet=reverb_mix,
                                     dry=reverb_dry, width=reverb_width,
                                     freeze=reverb_freeze)
```

- [ ] **Step 4: Add `freeze` passthrough to `loop_algo_reverb` in `tools/audio_engine.py`**

```python
def loop_algo_reverb(L, R, room_size=0.5, damping=0.5, wet=0.25, dry=1.0,
                       width=1.0, freeze=False, sr=None):
    """Loop-safe algorithmic reverb. ...(existing docstring unchanged)..."""
    n = len(L)
    dblL, dblR = algo_reverb(np.concatenate([L, L]), np.concatenate([R, R]),
                               room_size=room_size, damping=damping, wet=wet,
                               dry=dry, width=width, freeze=freeze, sr=sr)
    return dblL[n:], dblR[n:]
```

(Only the signature and the one new `freeze=freeze` kwarg passed through
to `algo_reverb` change — everything else in this function is unchanged.)

- [ ] **Step 5: Add the regression test to `tests/test_audio_engine.py`**

```python
def test_loop_algo_reverb_freeze_passthrough_sustains_longer():
    sr = 44100
    n = sr  # 1s
    L = np.zeros(n); L[0] = 1.0
    R = L.copy()
    normal_L, _ = loop_algo_reverb(L, R, room_size=0.5, wet=1.0, dry=0.0, sr=sr)
    frozen_L, _ = loop_algo_reverb(L, R, room_size=0.5, wet=1.0, dry=0.0,
                                     freeze=True, sr=sr)
    # freeze mode should not decay to silence by the end of the buffer
    # the way a normal room_size=0.5 tail does
    assert np.abs(frozen_L[-100:]).mean() > np.abs(normal_L[-100:]).mean()
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_audio_engine.py tests/test_sound_engine.py -v`
Expected: all pass.

- [ ] **Step 7: Add damping/width/freeze to the Reverb panel in `index.html`**

Replace the Reverb `.panel` block (Task 4) with:

```html
          <div class="panel">
            <h2>Reverb</h2>
            <div class="knobs">
              <div class="knob">
                <label for="revSize">Size <span id="revSizeVal">2.0</span> s</label>
                <input type="range" id="revSize" min="0.2" max="6" step="0.1" value="2.0">
              </div>
              <div class="knob">
                <label for="revDamping">Damping <span id="revDampingVal">0.5</span></label>
                <input type="range" id="revDamping" min="0" max="1" step="0.05" value="0.5">
                <span class="freq">0 = dark, 1 = bright</span>
              </div>
              <div class="knob">
                <label for="revWidth">Width <span id="revWidthVal">1.0</span>x</label>
                <input type="range" id="revWidth" min="0" max="2" step="0.05" value="1.0">
              </div>
              <div class="knob">
                <label for="revWet">Wet <span id="revWetVal">0</span>%</label>
                <input type="range" id="revWet" min="0" max="100" step="1" value="0">
              </div>
              <div class="knob">
                <label for="revDry">Dry <span id="revDryVal">100</span>%</label>
                <input type="range" id="revDry" min="0" max="100" step="1" value="100">
              </div>
              <div class="knob">
                <label class="loopToggle"><input type="checkbox" id="revFreeze"> Freeze (infinite sustain)</label>
              </div>
            </div>
          </div>
```

(This removes the old single `revMix` slider entirely, replaced by
separate `revWet`/`revDry` — update every reference to `revMix` across
`app.js` accordingly in the next step, including the `bindRamped("revMix", ...)`
call and the `document.getElementById("revMix")` dry-coupling listener
added in Task 5, both now dead code to remove.)

- [ ] **Step 8: Wire damping/width/freeze/wet/dry live in `app.js`**

Live-side approximations (documented in the design spec): damping = a
lowpass filter on the wet path only; width = the same M/S gain-scaling
pattern already used for the channel's own Stereo Width effect, applied
to the reverb wet signal; freeze = swap in a non-decaying impulse
response instead of the normal exponentially-decaying one.

In `buildChannelGraph()` (Task 5, Step 2), replace the reverb section:

```javascript
  const revDry = audioCtx.createGain(); revDry.gain.value = 1;
  const revWet = audioCtx.createGain(); revWet.gain.value = 0;
  const revDamp = audioCtx.createBiquadFilter();
  revDamp.type = "lowpass"; revDamp.frequency.value = 18000;
  const revSplitter = audioCtx.createChannelSplitter(2);
  const revMerger = audioCtx.createChannelMerger(2);
  const revMidBus = audioCtx.createGain(); revMidBus.gain.value = 1;
  const revSideBus = audioCtx.createGain(); revSideBus.gain.value = 1;
  const revSideWidth = audioCtx.createGain(); revSideWidth.gain.value = 1;
  const revSideNeg = audioCtx.createGain(); revSideNeg.gain.value = -1;
  const revMidL = audioCtx.createGain(); revMidL.gain.value = 0.5;
  const revMidR = audioCtx.createGain(); revMidR.gain.value = 0.5;
  const revSideL = audioCtx.createGain(); revSideL.gain.value = 0.5;
  const revSideR = audioCtx.createGain(); revSideR.gain.value = -0.5;
  const convolver = audioCtx.createConvolver();
  convolver.normalize = true;
  convolver.buffer = makeReverbIR(audioCtx, 2.0, false);
  const revOut = audioCtx.createGain(); revOut.gain.value = 1;

  revSplitter.connect(revMidL, 0); revMidL.connect(revMidBus);
  revSplitter.connect(revMidR, 1); revMidR.connect(revMidBus);
  revSplitter.connect(revSideL, 0); revSideL.connect(revSideBus);
  revSplitter.connect(revSideR, 1); revSideR.connect(revSideBus);
  revSideBus.connect(revSideWidth);
  revMidBus.connect(revMerger, 0, 0);
  revSideWidth.connect(revMerger, 0, 0);
  revMidBus.connect(revMerger, 0, 1);
  revSideWidth.connect(revSideNeg);
  revSideNeg.connect(revMerger, 0, 1);

  // merger (M/S width control, unchanged from before) feeds dry AND the
  // damping+width-processed wet path
  merger.connect(revDry).connect(revOut);
  merger.connect(revWet).connect(convolver).connect(revDamp)
        .connect(revSplitter);
  revMerger.connect(revOut);
```

(This replaces the simpler `merger.connect(revWet).connect(convolver).connect(revOut)`
line from Task 5's `buildChannelGraph` with the damping filter + a SECOND
M/S width stage scoped to the reverb tail only — distinct from the
channel's own `splitter`/`sideWidth`, which controls the whole channel's
width, not just the reverb send.)

Update `makeReverbIR` to support freeze:

```javascript
function makeReverbIR(ctx, seconds, freeze) {
  const rate = ctx.sampleRate;
  const length = Math.max(1, Math.floor(rate * seconds));
  const impulse = ctx.createBuffer(2, length, rate);
  for (let ch = 0; ch < 2; ch++) {
    const data = impulse.getChannelData(ch);
    for (let i = 0; i < length; i++) {
      const envelope = freeze ? 1.0 : Math.pow(1 - i / length, 2);
      data[i] = (Math.random() * 2 - 1) * envelope;
    }
  }
  return impulse;
}
```

Add the new channel-object fields (`revDamp`, `revSideWidth`, `freeze`
state) to `buildChannelGraph()`'s return object, then bind:

```javascript
bindRamped("revDamping", ch => ch.revDamp, "frequency", d => 200 + d * 17800);
bindRamped("revWidth", ch => ch.revSideWidth, "gain");
document.getElementById("revWet").addEventListener("input", e => {
  document.getElementById("revWetVal").textContent = e.target.value;
  const ch = currentChannel(); if (!ch) return;
  ch.revWet.gain.setTargetAtTime(parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
});
document.getElementById("revDry").addEventListener("input", e => {
  document.getElementById("revDryVal").textContent = e.target.value;
  const ch = currentChannel(); if (!ch) return;
  ch.revDry.gain.setTargetAtTime(parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
});
document.getElementById("revFreeze").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  ch.freeze = e.target.checked;
  ch.convolver.buffer = makeReverbIR(audioCtx, parseFloat(document.getElementById("revSize").value), ch.freeze);
});
```

Update the existing `revSize` `input`/`change` listeners (Task 5, Step 4)
to pass `ch.freeze` as the new third argument to `makeReverbIR(...)`.

Update `loadRackFromChannel()` — replace the old `revMix` lines with:
```javascript
  document.getElementById("revDamping").value = (ch.revDamp.frequency.value - 200) / 17800;
  document.getElementById("revDampingVal").textContent = ((ch.revDamp.frequency.value - 200) / 17800).toFixed(2);
  document.getElementById("revWidth").value = ch.revSideWidth.gain.value;
  document.getElementById("revWidthVal").textContent = ch.revSideWidth.gain.value.toFixed(2);
  document.getElementById("revWet").value = Math.round(ch.revWet.gain.value * 100);
  document.getElementById("revWetVal").textContent = Math.round(ch.revWet.gain.value * 100);
  document.getElementById("revDry").value = Math.round(ch.revDry.gain.value * 100);
  document.getElementById("revDryVal").textContent = Math.round(ch.revDry.gain.value * 100);
  document.getElementById("revFreeze").checked = !!ch.freeze;
```

Update `syncChannelToServer()`'s `params` — replace `reverb_mix:
ch.revWet.gain.value` with:
```javascript
    reverb_mix: ch.revWet.gain.value, reverb_dry: ch.revDry.gain.value,
    reverb_damping: (ch.revDamp.frequency.value - 200) / 17800,
    reverb_width: ch.revSideWidth.gain.value, reverb_freeze: !!ch.freeze,
```

- [ ] **Step 9: Run tests, then manually re-verify all 6 reverb knobs live in the browser**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py tests/test_sound_engine_library.py tests/test_audio_engine.py -v`
Expected: all pass. In the browser: confirm Wet and Dry move independently;
confirm Damping audibly darkens/brightens the tail while playing; confirm
Freeze sustains indefinitely instead of decaying; confirm turning Freeze
off restores normal decay at the current Size.

- [ ] **Step 10: Commit**

```bash
git add sound_engine/static/index.html sound_engine/static/app.js sound_engine/server.py tools/audio_engine.py tests/test_sound_engine.py tests/test_audio_engine.py
git commit -m "Deepen Reverb panel: independent wet/dry, damping, width, freeze"
```

---

## Final verification (whole plan)

- [ ] Run `.venv/bin/python -m pytest tests/ -q` — full suite green (or only the
      pre-existing, unrelated `test_real_beats_are_not_mono_or_silent`
      failure already flagged as a separate task on 2026-08-08 — no new
      failures).
- [ ] Full manual browser pass: load a real multi-stem beat, verify all
      three deepened panels (EQ, Compressor, Reverb) live, mute/solo,
      export, confirm the exported file plays and matches what was heard.
- [ ] Append a `DECISIONS.md` entry summarizing what shipped, what was
      verified, and status — this project's standing convention.
- [ ] Update `sound_engine/server.py`'s module docstring if it still
      describes the old single-file-only behavior anywhere.

## Self-review notes (from writing this plan)

- **Spec coverage:** every numbered item in the design spec's "What ships
  this round" section has a task — beat browsing (Task 1-2), multi-channel
  loading/mixing (Task 2-6), EQ/Compressor/Reverb depth (Task 7-9). The
  spec's explicit deferral (new effect types, VSTs) has no task, correctly.
- **Type consistency check performed:** `lane_id` is used consistently as
  the channel dict key across `library.py`, `server.py`'s `PROJECTS`
  structure, and every `app.js` reference (`channels[laneId]`) — verified
  no task introduces a second name for the same concept (e.g. no
  `channel_id` vs `lane_id` drift).
- **One known gap, deliberately deferred, not silently dropped:** Task 3's
  `_apply_channel_chain` and Task 9's reverb rework both read `sr` from
  `channel["sr"]` (the original file's own rate) — if a project mixes
  stems at different sample rates (shouldn't happen for stems from one
  beat render, per `write_stems` using the project's fixed `SR`, but could
  happen for a future edge case) the export mix-summing step in Task 3
  assumes a single shared `sr` for the whole project (`sr = next(iter(...))`).
  Not fixed in this plan — flag to the owner if a mixed-rate project ever
  actually surfaces; not worth solving speculatively now (YAGNI).
