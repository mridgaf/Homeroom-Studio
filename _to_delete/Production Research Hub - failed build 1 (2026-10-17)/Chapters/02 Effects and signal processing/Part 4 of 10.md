# Chapter 02: Effects and signal processing
## Part 4 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- 2026-08-08-sound-engine-mixer.md (piece 2 of 8) — Sound Engine Multi-Stem Mixer Implementation Plan

(Next: Part 5 of 10)


=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer.md (piece 2 of 8)
ORIGINAL LOCATION: HS:docs/superpowers/plans/2026-08-08-sound-engine-mixer.md
=====================================================

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


=== END OF PART ===
