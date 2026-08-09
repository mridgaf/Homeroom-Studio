// Real-time preview runs entirely in the browser's own audio engine
// (Web Audio API native nodes) — instant, sample-accurate, no Python
// garbage-collector risk. Export bounces through the tested Python
// pedalboard engine (tools/audio_engine.py) for the final file, so the
// heavy DSP is the same code the beat generator uses. Chain order (both
// live and export) is: EQ -> Compressor -> Saturation -> Width -> Reverb.
// A project can hold multiple channels (one per beat stem, or a single
// "upload" channel for a dropped-in file) — every channel gets its own
// full copy of this chain, summed into one masterGain.
let projectId = null;
let audioCtx = null;
let masterGain = null;
let channels = {};       // lane_id -> channel object, see buildChannelGraph()
let channelOrder = [];   // lane_ids, display order
let selectedLane = null;
let isPlaying = false;
let projectLoadSeq = 0;  // guards against two concurrent openProject() calls
                          // (e.g. double-click a beat, or upload while a beat
                          // is still loading) interleaving their per-channel
                          // fetch loops and corrupting the shared channels{}

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

const RAMP_SECONDS = 0.02;  // setTargetAtTime time-constant — smooth knob
                             // moves, no zipper-noise clicks (same reason
                             // pedalboard smooths param changes internally,
                             // verified separately in the Python engine)

["dragenter", "dragover"].forEach(ev =>
  dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.add("drag"); }));
["dragleave", "drop"].forEach(ev =>
  dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.remove("drag"); }));
dropzone.addEventListener("drop", e => {
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
  // A second openProject() can start (double-click a beat, or drop a file
  // while a beat is still loading) before this one's per-channel fetch loop
  // below finishes. Build everything into locals keyed to this call's own
  // token and only commit to the shared globals if no newer load has started
  // in the meantime — same "parse into locals, commit atomically" shape as
  // the partial-commit bug fixed server-side in channel_process() (see
  // DECISIONS.md 2026-08-09). Committing incrementally into the shared
  // `channels`/`channelOrder` here would let two projects' stems interleave
  // in the same mixer.
  const myLoad = ++projectLoadSeq;
  const newProjectId = data.project_id;

  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const myMasterGain = audioCtx.createGain();
  myMasterGain.connect(audioCtx.destination);

  const newChannels = {};
  const newChannelOrder = [];
  for (const ch of data.channels) {
    const arrayBuf = await (await fetch(
      `/api/project/${newProjectId}/channel/${ch.lane_id}/dry?t=${Date.now()}`)).arrayBuffer();
    let audioBuffer = await audioCtx.decodeAudioData(arrayBuf);
    // defensive: dsp.py upmixes mono to dual-mono server-side today, so this
    // never actually fires via the normal load path — but the M/S width
    // graph below assumes 2 channels (ChannelSplitterNode silences a missing
    // channel rather than duplicating it), so don't trust an unrelated file
    // never to change.
    if (audioBuffer.numberOfChannels === 1) {
      const stereo = audioCtx.createBuffer(2, audioBuffer.length, audioBuffer.sampleRate);
      stereo.copyToChannel(audioBuffer.getChannelData(0), 0);
      stereo.copyToChannel(audioBuffer.getChannelData(0), 1);
      audioBuffer = stereo;
    }
    newChannels[ch.lane_id] = buildChannelGraph(ch.lane_id, ch.label, audioBuffer, myMasterGain);
    newChannelOrder.push(ch.lane_id);
  }

  if (myLoad !== projectLoadSeq) {
    // a newer load won the race while this one was still fetching — abandon
    // it and disconnect its half-built graph rather than touch shared state
    myMasterGain.disconnect();
    return;
  }

  // tear down the previous project's whole graph before switching to the new
  // one — Web Audio only processes nodes reachable from destination, so
  // disconnecting the old masterGain (the single exit point every channel's
  // fader feeds into) is enough to orphan the entire old chain instead of
  // leaking it into destination for the rest of the tab session (same class
  // of node leak fixed for the single-channel version — see DECISIONS.md
  // 2026-08-08).
  if (masterGain) masterGain.disconnect();
  projectId = newProjectId;
  masterGain = myMasterGain;
  channels = newChannels;
  channelOrder = newChannelOrder;
  fileName.textContent = data.name;
  fileMeta.textContent = `${data.channels.length} channel(s)`;
  exportStatus.textContent = "";
  renderChannelList();
  selectChannel(channelOrder[0]);
  dropzone.classList.add("hidden");
  workspace.classList.remove("hidden");
}

function makeSaturationCurve(driveDb) {
  const k = Math.max(Math.pow(10, driveDb / 20), 1e-3);
  const n = 2048;
  const curve = new Float32Array(n);
  const norm = Math.tanh(k) || 1;
  for (let i = 0; i < n; i++) {
    const x = (i / (n - 1)) * 2 - 1;
    curve[i] = Math.tanh(k * x) / norm;
  }
  return curve;
}

function makeReverbIR(ctx, seconds) {
  const rate = ctx.sampleRate;
  const length = Math.max(1, Math.floor(rate * seconds));
  const impulse = ctx.createBuffer(2, length, rate);
  for (let ch = 0; ch < 2; ch++) {
    const data = impulse.getChannelData(ch);
    for (let i = 0; i < length; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2);
    }
  }
  return impulse;
}

function buildChannelGraph(laneId, label, audioBuffer, targetMasterGain) {
  const lowShelf = audioCtx.createBiquadFilter();
  lowShelf.type = "lowshelf"; lowShelf.frequency.value = 120; lowShelf.gain.value = 0;

  const midPeak = audioCtx.createBiquadFilter();
  midPeak.type = "peaking"; midPeak.frequency.value = 800; midPeak.Q.value = 0.9; midPeak.gain.value = 0;

  const highShelf = audioCtx.createBiquadFilter();
  highShelf.type = "highshelf"; highShelf.frequency.value = 8000; highShelf.gain.value = 0;

  // pedalboard.Compressor (export path) has no knee parameter at all — 0
  // (hard knee) is the closest live/export reconciliation available.
  const compressor = audioCtx.createDynamicsCompressor();
  compressor.threshold.value = -24; compressor.ratio.value = 1;
  compressor.attack.value = 0.012; compressor.release.value = 0.18; compressor.knee.value = 0;

  // --- saturation: parallel dry/wet through a WaveShaper, mix sums at
  // satOut (Web Audio auto-sums multiple connections into one input)
  const satDry = audioCtx.createGain(); satDry.gain.value = 1;
  const satWet = audioCtx.createGain(); satWet.gain.value = 0;
  const waveshaper = audioCtx.createWaveShaper();
  waveshaper.curve = makeSaturationCurve(6); waveshaper.oversample = "4x";
  const satOut = audioCtx.createGain(); satOut.gain.value = 1;

  // --- stereo width: M/S via splitter/merger + gain math, matches
  // tools/audio_engine.py's stereo_width() exactly (mid untouched, only
  // the side signal is scaled — loudness-neutral on the mono sum)
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

  // --- reverb: parallel dry/wet through a Convolver fed a generated
  // impulse response (no sample IR files needed for a real, usable tail)
  const revDry = audioCtx.createGain(); revDry.gain.value = 1;
  const revWet = audioCtx.createGain(); revWet.gain.value = 0;
  const convolver = audioCtx.createConvolver();
  convolver.normalize = true;
  convolver.buffer = makeReverbIR(audioCtx, 2.0);
  const revOut = audioCtx.createGain(); revOut.gain.value = 1;

  // bypass A/B: wetGain/bypassGain crossfade between processed and dry
  // paths so "Bypass" is instant and glitch-free, not a graph rewire
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
  fader.connect(targetMasterGain);

  return {
    laneId, label, audioBuffer, sourceNode: null,
    lowShelf, midPeak, highShelf, compressor,
    satDry, satWet, waveshaper, satOut,
    splitter, merger, sideWidth,
    revDry, revWet, convolver, revOut,
    wetGain, bypassGain, fader, panner,
    muted: false, solo: false, faderDb: 0, pan: 0,
    lastSatDriveTick: 0, lastSatDriveApplied: null,
    lastRevSizeTick: 0, lastRevSizeApplied: null,
  };
}

function renderChannelList() {
  channelListEl.innerHTML = "";
  for (const laneId of channelOrder) {
    const ch = channels[laneId];
    const strip = document.createElement("div");
    strip.className = "channelStrip" + (laneId === selectedLane ? " selected" : "");
    strip.innerHTML = `
      <div class="label">${ch.label}</div>
      <div class="row"><input type="range" class="faderInput" min="-24" max="12" step="0.5" value="${ch.faderDb}"></div>
      <div class="row"><input type="range" class="panInput" min="-1" max="1" step="0.05" value="${ch.pan}"></div>
      <div class="mutesolo">
        <button class="mute">M</button>
        <button class="solo">S</button>
      </div>`;
    strip.addEventListener("click", e => {
      if (e.target.tagName !== "INPUT" && e.target.tagName !== "BUTTON") selectChannel(laneId);
    });
    strip.querySelector(".faderInput").addEventListener("input", e => {
      ch.faderDb = parseFloat(e.target.value);
      recomputeAudibility();
      syncChannelToServer(laneId);
    });
    strip.querySelector(".panInput").addEventListener("input", e => {
      ch.pan = parseFloat(e.target.value);
      if (ch.panner) ch.panner.pan.setTargetAtTime(ch.pan, audioCtx.currentTime, RAMP_SECONDS);
      syncChannelToServer(laneId);
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
    // reflect ch.faderDb (channel state, survives renderChannelList()
    // rebuilding the DOM) rather than a DOM value that no longer exists by
    // the time a later mute/solo toggle calls this again
    ch.fader.gain.setTargetAtTime(audible ? 10 ** (ch.faderDb / 20) : 0, t, RAMP_SECONDS);
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
  document.getElementById("satDrive").value = ch.lastSatDriveApplied ?? 6;
  document.getElementById("satDriveVal").textContent = (ch.lastSatDriveApplied ?? 6).toFixed(1);
  document.getElementById("satMix").value = ch.satWet.gain.value * 100;
  document.getElementById("satMixVal").textContent = Math.round(ch.satWet.gain.value * 100);
  document.getElementById("revSize").value = ch.lastRevSizeApplied ?? 2.0;
  document.getElementById("revSizeVal").textContent = (ch.lastRevSizeApplied ?? 2.0).toFixed(1);
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

// dry-side gains that mirror a mix slider (1 - mix) need a second binding
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

// drive and reverb size aren't smoothly rampable params — they rebuild a
// curve / impulse response. Reassigning that buffer on every "input" tick
// mid-drag risks an audible click each step, so throttle the actual rebuild
// to ~20Hz; the value label still updates every tick for live feel, and a
// trailing "change" listener guarantees the final dragged-to value always
// lands even if its last tick got throttled out. Both listeners also skip
// the rebuild if the value hasn't actually changed since the last one
// applied — makeReverbIR() is randomized (fresh noise each call), so
// without this dedupe, a throttled "input" tick and the immediately-
// following "change" for the SAME final value would swap in two different
// random buffers back to back, clicking at the exact moment this fix was
// meant to make click-free. Per-channel state (lastSatDriveTick etc.) lives
// on the channel object so dragging one channel's knob never throttles or
// dedupes against a different channel's last-applied value.
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
  syncChannelToServer(selectedLane);
});
document.getElementById("satDrive").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  const val = parseFloat(e.target.value);
  if (val === ch.lastSatDriveApplied) return;
  ch.lastSatDriveApplied = val;
  ch.waveshaper.curve = makeSaturationCurve(val);
  syncChannelToServer(selectedLane);
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
  syncChannelToServer(selectedLane);
});
document.getElementById("revSize").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  const val = parseFloat(e.target.value);
  if (val === ch.lastRevSizeApplied) return;
  ch.lastRevSizeApplied = val;
  ch.convolver.buffer = makeReverbIR(audioCtx, val);
  syncChannelToServer(selectedLane);
});

function syncChannelToServer(laneId) {
  // fire-and-forget — keeps the server's copy of this channel's settings
  // current for export; live audio never waits on this
  if (!projectId) return;
  const ch = channels[laneId];
  // Every field the server's _apply_channel_chain() reads is sent every
  // time, for every channel — not just the one currently selected in the
  // rack. The server has no memory of a channel's prior processing: it
  // recomputes the whole chain from the dry buffer on each call and
  // defaults any missing field to a bypass value (0 dB EQ, ratio 1, etc).
  // Sending only {gain_db, pan, muted, solo} for a non-selected channel
  // (e.g. a mute/solo/fader touch from the sidebar strip) would silently
  // reset that channel's EQ/comp/sat/reverb back to defaults server-side
  // even though the live Web Audio preview still shows it processed — each
  // channel's own AudioNodes hold accurate values regardless of selection,
  // so there's no reason to omit them.
  const params = {
    low_db: ch.lowShelf.gain.value, mid_db: ch.midPeak.gain.value, high_db: ch.highShelf.gain.value,
    comp_threshold_db: ch.compressor.threshold.value, comp_ratio: ch.compressor.ratio.value,
    comp_attack_ms: ch.compressor.attack.value * 1000, comp_release_ms: ch.compressor.release.value * 1000,
    sat_drive_db: ch.lastSatDriveApplied ?? 6, sat_mix: ch.satWet.gain.value,
    width: ch.sideWidth.gain.value,
    reverb_size_s: ch.lastRevSizeApplied ?? 2.0, reverb_mix: ch.revWet.gain.value,
    gain_db: ch.faderDb, pan: ch.pan, muted: ch.muted, solo: ch.solo,
  };
  fetch(`/api/project/${projectId}/channel/${laneId}/process`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
}

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

// Safety net (added after a looping preview was accidentally left running
// in a backgrounded tab and kept playing indefinitely — closing the tab
// stops it, but nothing should be relying on remembering that). A LOOPING
// playback that gets backgrounded stops automatically; a one-shot
// (non-loop) play is left alone since it'll end on its own shortly.
document.addEventListener("visibilitychange", () => {
  if (document.hidden && isPlaying && channelOrder.length &&
      channels[channelOrder[0]].sourceNode && channels[channelOrder[0]].sourceNode.loop) {
    stopPlayback();
  }
});
window.addEventListener("pagehide", stopPlayback);

exportBtn.addEventListener("click", async () => {
  // disabled for the whole round trip — a double-click used to fire two
  // overlapping export calls racing on the same server-side session, and
  // could export the wrong values or (with same-second timestamps) silently
  // overwrite the first export.
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
