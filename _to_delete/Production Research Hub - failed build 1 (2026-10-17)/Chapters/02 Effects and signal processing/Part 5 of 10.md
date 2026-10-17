# Chapter 02: Effects and signal processing
## Part 5 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- 2026-08-08-sound-engine-mixer.md (piece 3 of 8) — Sound Engine Multi-Stem Mixer Implementation Plan

(Next: Part 6 of 10)


=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer.md (piece 3 of 8)
ORIGINAL LOCATION: HS:docs/superpowers/plans/2026-08-08-sound-engine-mixer.md
=====================================================

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


=== END OF PART ===
