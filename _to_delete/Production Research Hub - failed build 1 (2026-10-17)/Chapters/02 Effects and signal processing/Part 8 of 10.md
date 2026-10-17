# Chapter 02: Effects and signal processing
## Part 8 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- 2026-08-08-sound-engine-mixer.md (piece 6 of 8) — Sound Engine Multi-Stem Mixer Implementation Plan

(Next: Part 9 of 10)


=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer.md (piece 6 of 8)
ORIGINAL LOCATION: HS:docs/superpowers/plans/2026-08-08-sound-engine-mixer.md
=====================================================

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


=== END OF PART ===
