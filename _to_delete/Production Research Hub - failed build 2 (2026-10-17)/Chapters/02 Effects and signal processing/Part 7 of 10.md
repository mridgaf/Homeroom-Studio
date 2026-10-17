# Chapter 02: Effects and signal processing
## Part 7 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- 2026-08-08-sound-engine-mixer.md (piece 5 of 8) — Sound Engine Multi-Stem Mixer Implementation Plan

(Next: Part 8 of 10)


=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer.md (piece 5 of 8)
ORIGINAL LOCATION: HS:docs/superpowers/plans/2026-08-08-sound-engine-mixer.md
=====================================================

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


=== END OF PART ===
