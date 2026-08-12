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

  // DynamicsCompressorNode has no makeup-gain concept — a real gain stage
  // matches glue_compressor()'s pedalboard chain, which has one
  const makeupGain = audioCtx.createGain(); makeupGain.gain.value = 1;

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
  // impulse response (no sample IR files needed for a real, usable tail).
  // Damping = a lowpass on the wet-only path; Width = a second M/S
  // gain-scaling stage scoped just to the reverb send (distinct from the
  // channel's own splitter/sideWidth, which controls the whole channel).
  const revDry = audioCtx.createGain(); revDry.gain.value = 1;
  const revWet = audioCtx.createGain(); revWet.gain.value = 0;
  const revDamp = audioCtx.createBiquadFilter();
  // 9100 Hz = damping 0.5 under the d => 200 + d*17800 mapping used by
  // bindRamped/syncChannelToServer below — must match reverb_damping's
  // server-side default (0.5) and the revDamping slider's HTML default,
  // or a fresh channel reports/exports a different damping than its own
  // slider shows until the user touches it.
  revDamp.type = "lowpass"; revDamp.frequency.value = 9100;
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

  // --- convolve: same shape as the reverb send, but the impulse response
  // is whatever sound the owner drops in. ConvolverNode with no buffer
  // outputs silence, so convMix stays disabled in the UI until a file is
  // loaded — otherwise the live channel would go quiet while the server
  // (which no-ops without an IR) still returned the dry signal.
  const convDry = audioCtx.createGain(); convDry.gain.value = 1;
  const convWet = audioCtx.createGain(); convWet.gain.value = 0;
  const convNode = audioCtx.createConvolver();
  // normalize OFF: the browser's own loudness normalize landed ~11 dB above
  // the server's peak-match, so live and export disagreed. convScale carries
  // a factor measured by the same RULE the server uses (see peakMatchScale).
  convNode.normalize = false;
  const convScale = audioCtx.createGain(); convScale.gain.value = 1;
  const convOut = audioCtx.createGain(); convOut.gain.value = 1;

  // bypass A/B: wetGain/bypassGain crossfade between processed and dry
  // paths so "Bypass" is instant and glitch-free, not a graph rewire
  const wetGain = audioCtx.createGain();
  const bypassGain = audioCtx.createGain();

  lowShelf.connect(midPeak).connect(highShelf).connect(compressor);
  compressor.connect(makeupGain);
  makeupGain.connect(satDry).connect(satOut);
  makeupGain.connect(satWet).connect(waveshaper).connect(satOut);
  satOut.connect(splitter);
  merger.connect(convDry).connect(convOut);
  merger.connect(convWet).connect(convNode).connect(convScale).connect(convOut);
  convOut.connect(revDry).connect(revOut);
  convOut.connect(revWet).connect(convolver).connect(revDamp)
        .connect(revSplitter);
  revMerger.connect(revOut);
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
    lowShelf, midPeak, highShelf, compressor, makeupGain,
    satDry, satWet, waveshaper, satOut,
    splitter, merger, sideWidth,
    convDry, convWet, convNode, convScale, convOut, irName: null,
    revDry, revWet, revDamp, revSideWidth, convolver, revOut,
    wetGain, bypassGain, fader, panner,
    muted: false, solo: false, faderDb: 0, pan: 0, freeze: false,
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
  document.getElementById("lowHz").value = ch.lowShelf.frequency.value;
  document.getElementById("lowHzVal").textContent = ch.lowShelf.frequency.value.toFixed(0);
  document.getElementById("midDb").value = ch.midPeak.gain.value;
  document.getElementById("midDbVal").textContent = ch.midPeak.gain.value.toFixed(1);
  document.getElementById("midHz").value = ch.midPeak.frequency.value;
  document.getElementById("midHzVal").textContent = ch.midPeak.frequency.value.toFixed(0);
  document.getElementById("midQ").value = ch.midPeak.Q.value;
  document.getElementById("midQVal").textContent = ch.midPeak.Q.value.toFixed(1);
  document.getElementById("highDb").value = ch.highShelf.gain.value;
  document.getElementById("highDbVal").textContent = ch.highShelf.gain.value.toFixed(1);
  document.getElementById("highHz").value = ch.highShelf.frequency.value;
  document.getElementById("highHzVal").textContent = ch.highShelf.frequency.value.toFixed(0);
  document.getElementById("compThreshold").value = ch.compressor.threshold.value;
  document.getElementById("compThresholdVal").textContent = ch.compressor.threshold.value.toFixed(0);
  document.getElementById("compRatio").value = ch.compressor.ratio.value;
  document.getElementById("compRatioVal").textContent = ch.compressor.ratio.value.toFixed(1);
  document.getElementById("compAttack").value = (ch.compressor.attack.value * 1000).toFixed(0);
  document.getElementById("compAttackVal").textContent = (ch.compressor.attack.value * 1000).toFixed(0);
  document.getElementById("compRelease").value = (ch.compressor.release.value * 1000).toFixed(0);
  document.getElementById("compReleaseVal").textContent = (ch.compressor.release.value * 1000).toFixed(0);
  const makeupDb = 20 * Math.log10(ch.makeupGain.gain.value);
  document.getElementById("compMakeup").value = makeupDb;
  document.getElementById("compMakeupVal").textContent = makeupDb.toFixed(1);
  document.getElementById("satDrive").value = ch.lastSatDriveApplied ?? 6;
  document.getElementById("satDriveVal").textContent = (ch.lastSatDriveApplied ?? 6).toFixed(1);
  document.getElementById("satMix").value = ch.satWet.gain.value * 100;
  document.getElementById("satMixVal").textContent = Math.round(ch.satWet.gain.value * 100);
  document.getElementById("revSize").value = ch.lastRevSizeApplied ?? 2.0;
  document.getElementById("revSizeVal").textContent = (ch.lastRevSizeApplied ?? 2.0).toFixed(1);
  document.getElementById("revDamping").value = (ch.revDamp.frequency.value - 200) / 17800;
  document.getElementById("revDampingVal").textContent = ((ch.revDamp.frequency.value - 200) / 17800).toFixed(2);
  document.getElementById("revWidth").value = ch.revSideWidth.gain.value;
  document.getElementById("revWidthVal").textContent = ch.revSideWidth.gain.value.toFixed(2);
  document.getElementById("revWet").value = Math.round(ch.revWet.gain.value * 100);
  document.getElementById("revWetVal").textContent = Math.round(ch.revWet.gain.value * 100);
  document.getElementById("revDry").value = Math.round(ch.revDry.gain.value * 100);
  document.getElementById("revDryVal").textContent = Math.round(ch.revDry.gain.value * 100);
  document.getElementById("revFreeze").checked = !!ch.freeze;
  document.getElementById("widthKnob").value = ch.sideWidth.gain.value;
  document.getElementById("widthKnobVal").textContent = ch.sideWidth.gain.value.toFixed(2);
  document.getElementById("convMix").value = Math.round(ch.convWet.gain.value * 100);
  document.getElementById("convMixVal").textContent = Math.round(ch.convWet.gain.value * 100);
  updateConvPanel(ch);
}

function updateConvPanel(ch) {
  const has = !!ch.irName;
  document.getElementById("convMix").disabled = !has;
  document.getElementById("convClear").disabled = !has;
  document.getElementById("convName").textContent =
    has ? `through: ${ch.irName}` : "nothing loaded — this channel is untouched";
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
bindRamped("lowHz", ch => ch.lowShelf, "frequency");
bindRamped("midDb", ch => ch.midPeak, "gain");
bindRamped("midHz", ch => ch.midPeak, "frequency");
bindRamped("midQ", ch => ch.midPeak, "Q");
bindRamped("highDb", ch => ch.highShelf, "gain");
bindRamped("highHz", ch => ch.highShelf, "frequency");
bindRamped("compThreshold", ch => ch.compressor, "threshold");
bindRamped("compRatio", ch => ch.compressor, "ratio");
bindRamped("compAttack", ch => ch.compressor, "attack", ms => ms / 1000);
bindRamped("compRelease", ch => ch.compressor, "release", ms => ms / 1000);
bindRamped("compMakeup", ch => ch.makeupGain, "gain", db => 10 ** (db / 20));
bindRamped("satMix", ch => ch.satWet, "gain", pct => pct / 100);
bindRamped("widthKnob", ch => ch.sideWidth, "gain");
bindRamped("revDamping", ch => ch.revDamp, "frequency", d => 200 + d * 17800);
bindRamped("revWidth", ch => ch.revSideWidth, "gain");

// dry-side gains that mirror a mix slider (1 - mix) need a second binding
document.getElementById("satMix").addEventListener("input", e => {
  const ch = currentChannel();
  if (!ch || !audioCtx) return;
  ch.satDry.gain.setTargetAtTime(1 - parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
});
document.getElementById("revWet").addEventListener("input", e => {
  document.getElementById("revWetVal").textContent = e.target.value;
  const ch = currentChannel(); if (!ch || !audioCtx) return;
  ch.revWet.gain.setTargetAtTime(parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
  syncChannelToServer(selectedLane);
});
document.getElementById("revDry").addEventListener("input", e => {
  document.getElementById("revDryVal").textContent = e.target.value;
  const ch = currentChannel(); if (!ch || !audioCtx) return;
  ch.revDry.gain.setTargetAtTime(parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
  syncChannelToServer(selectedLane);
});
document.getElementById("convMix").addEventListener("input", e => {
  document.getElementById("convMixVal").textContent = e.target.value;
  const ch = currentChannel(); if (!ch || !audioCtx) return;
  const mix = parseFloat(e.target.value) / 100;
  ch.convWet.gain.setTargetAtTime(mix, audioCtx.currentTime, RAMP_SECONDS);
  ch.convDry.gain.setTargetAtTime(1 - mix, audioCtx.currentTime, RAMP_SECONDS);
  syncChannelToServer(selectedLane);
});

// Drop a sound on the panel: decode it locally for the live ConvolverNode
// AND post the same file to the server, so the export is convolved with
// the same sound the owner just heard.
const convDropEl = document.getElementById("convDrop");
convDropEl.addEventListener("dragover", e => { e.preventDefault(); convDropEl.classList.add("drag"); });
convDropEl.addEventListener("dragleave", () => convDropEl.classList.remove("drag"));
convDropEl.addEventListener("drop", e => {
  e.preventDefault();
  convDropEl.classList.remove("drag");
  const file = e.dataTransfer.files[0];
  if (file) loadConvolveFile(file);
});
convDropEl.addEventListener("click", () => {
  const picker = document.createElement("input");
  picker.type = "file"; picker.accept = "audio/*";
  picker.addEventListener("change", () => { if (picker.files[0]) loadConvolveFile(picker.files[0]); });
  picker.click();
});

// Level rule, shared with the server: the 100%-wet signal peaks where the
// dry peaked. Raw convolution levels differ by ~800x between Chrome and
// numpy, so the two sides can't share a scale FACTOR — they apply the same
// RULE, each measured in its own engine, both against the RAW (pre-effects)
// buffer. One offline render per loaded IR.
async function peakMatchScale(dryBuffer, irBuffer) {
  // Render the dry buffer TWICE and measure only the second half: the
  // server's loop_convolve is circular, so its tail wraps onto the start
  // and can raise the peak. A single linear pass undershoots that, which
  // would leave the live preview louder than the exported file. Same
  // double-buffer trick audio_engine.loop_algo_reverb uses.
  const n = dryBuffer.length;
  const rate = dryBuffer.sampleRate;
  const off = new OfflineAudioContext(2, n * 2, rate);
  const twice = off.createBuffer(2, n * 2, rate);
  for (let c = 0; c < 2; c++) {
    const src = dryBuffer.getChannelData(Math.min(c, dryBuffer.numberOfChannels - 1));
    twice.copyToChannel(src, c, 0);
    twice.copyToChannel(src, c, n);
  }
  const node = off.createBufferSource(); node.buffer = twice;
  const conv = off.createConvolver(); conv.normalize = false; conv.buffer = irBuffer;
  node.connect(conv).connect(off.destination);
  node.start();
  const rendered = await off.startRendering();
  let wetPeak = 0;
  for (let c = 0; c < rendered.numberOfChannels; c++) {
    const d = rendered.getChannelData(c);
    for (let i = n; i < d.length; i++) { const v = Math.abs(d[i]); if (v > wetPeak) wetPeak = v; }
  }
  let dryPeak = 0;
  for (let c = 0; c < dryBuffer.numberOfChannels; c++) {
    const d = dryBuffer.getChannelData(c);
    for (let i = 0; i < d.length; i++) { const v = Math.abs(d[i]); if (v > dryPeak) dryPeak = v; }
  }
  return (wetPeak > 0 && dryPeak > 0) ? dryPeak / wetPeak : 1;
}

// The server trims every IR to the stem's length (loop_convolve requires
// it). Chrome would use the whole thing, so a 4s IR on a 2s stem would
// sound different live than exported — trim here too.
function trimIRToStem(ctx, irBuffer, stemLength) {
  if (irBuffer.length <= stemLength) return irBuffer;
  const out = ctx.createBuffer(irBuffer.numberOfChannels, stemLength, irBuffer.sampleRate);
  for (let c = 0; c < irBuffer.numberOfChannels; c++) {
    out.copyToChannel(irBuffer.getChannelData(c).subarray(0, stemLength), c);
  }
  return out;
}

let convLoadSeq = 0;  // last drop wins — two IRs dropped in a row could
                      // otherwise land out of order, leaving the server on
                      // one IR and the live graph on the other

async function loadConvolveFile(file) {
  if (!currentChannel() || !projectId) return;
  // capture BOTH — the owner can switch channels, or open a whole different
  // project, while this decodes; the IR belongs where it was dropped
  const laneId = selectedLane;
  const myProjectId = projectId;
  const mySeq = ++convLoadSeq;
  const stale = () => myProjectId !== projectId || mySeq !== convLoadSeq
                       || !channels[laneId];
  const say = msg => {
    if (!stale() && selectedLane === laneId)
      document.getElementById("convName").textContent = msg;
  };

  say(`loading ${file.name}...`);
  const bytes = await file.arrayBuffer();
  let buffer;
  try {
    buffer = await audioCtx.decodeAudioData(bytes.slice(0));
  } catch (err) {
    say("couldn't read that as audio");
    return;
  }
  if (stale()) return;
  const form = new FormData();
  form.append("file", file);
  let r;
  try {
    r = await fetch(`/api/project/${myProjectId}/channel/${encodeURIComponent(laneId)}/ir`,
                    { method: "POST", body: form });
  } catch (e) {
    // without this the panel sat on "loading …" forever with no way back
    say("couldn't reach the Sound Engine server — is it still running?");
    return;
  }
  if (!r.ok) {
    const err = await r.json().catch(() => ({}));
    say(err.error || "the server couldn't read that file");
    return;
  }
  if (stale()) return;
  const target = channels[laneId];
  const ir = trimIRToStem(audioCtx, buffer, target.audioBuffer.length);
  const scale = await peakMatchScale(target.audioBuffer, ir);
  if (stale()) return;
  target.convNode.buffer = ir;
  // ramp, don't step: swapping an IR mid-playback with the Mix up stepped
  // the wet gain in one sample and clicked (found in re-review)
  target.convScale.gain.setTargetAtTime(scale, audioCtx.currentTime, RAMP_SECONDS);
  target.irName = file.name;
  if (selectedLane === laneId) updateConvPanel(target);
}

document.getElementById("convClear").addEventListener("click", async () => {
  const ch = currentChannel(); if (!ch || !projectId) return;
  const laneId = selectedLane;
  convLoadSeq++;  // cancel any drop still in flight for this panel
  await fetch(`/api/project/${projectId}/channel/${encodeURIComponent(laneId)}/ir`,
              { method: "DELETE" });
  ch.irName = null;
  ch.convNode.buffer = null;
  ch.convWet.gain.setTargetAtTime(0, audioCtx.currentTime, RAMP_SECONDS);
  ch.convDry.gain.setTargetAtTime(1, audioCtx.currentTime, RAMP_SECONDS);
  document.getElementById("convMix").value = 0;
  document.getElementById("convMixVal").textContent = "0";
  updateConvPanel(ch);
  syncChannelToServer(laneId);
});

document.getElementById("revFreeze").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  ch.freeze = e.target.checked;
  ch.convolver.buffer = makeReverbIR(audioCtx, parseFloat(document.getElementById("revSize").value), ch.freeze);
  syncChannelToServer(selectedLane);
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
  ch.convolver.buffer = makeReverbIR(audioCtx, val, ch.freeze);
  syncChannelToServer(selectedLane);
});
document.getElementById("revSize").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  const val = parseFloat(e.target.value);
  if (val === ch.lastRevSizeApplied) return;
  ch.lastRevSizeApplied = val;
  ch.convolver.buffer = makeReverbIR(audioCtx, val, ch.freeze);
  syncChannelToServer(selectedLane);
});

const _syncTimers = {};  // laneId -> pending debounce timeout, see syncChannelToServer()

function _sendChannelSync(laneId) {
  const ch = channels[laneId];
  if (!ch) return;
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
    low_db: ch.lowShelf.gain.value, low_hz: ch.lowShelf.frequency.value,
    mid_db: ch.midPeak.gain.value, mid_hz: ch.midPeak.frequency.value, mid_q: ch.midPeak.Q.value,
    high_db: ch.highShelf.gain.value, high_hz: ch.highShelf.frequency.value,
    comp_threshold_db: ch.compressor.threshold.value, comp_ratio: ch.compressor.ratio.value,
    comp_attack_ms: ch.compressor.attack.value * 1000, comp_release_ms: ch.compressor.release.value * 1000,
    comp_makeup_db: 20 * Math.log10(ch.makeupGain.gain.value),
    sat_drive_db: ch.lastSatDriveApplied ?? 6, sat_mix: ch.satWet.gain.value,
    width: ch.sideWidth.gain.value,
    reverb_size_s: ch.lastRevSizeApplied ?? 2.0, reverb_mix: ch.revWet.gain.value,
    reverb_dry: ch.revDry.gain.value,
    reverb_damping: (ch.revDamp.frequency.value - 200) / 17800,
    reverb_width: ch.revSideWidth.gain.value, reverb_freeze: !!ch.freeze,
    conv_mix: ch.convWet.gain.value,
    gain_db: ch.faderDb, pan: ch.pan, muted: ch.muted, solo: ch.solo,
  };
  fetch(`/api/project/${projectId}/channel/${laneId}/process`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
}

function syncChannelToServer(laneId, immediate) {
  // fire-and-forget — keeps the server's copy of this channel's settings
  // current for export; live audio never waits on this. Debounced (trailing,
  // ~120ms) because the server has no per-channel "just update this one
  // field" endpoint — every sync reprocesses that channel's WHOLE effect
  // chain over its full buffer, synchronously, on FastAPI's single event
  // loop (found in harsh-critic re-review). A fader/pan drag or a rack knob
  // fires this on every "input" tick with no throttle of its own, so without
  // debouncing here a single drag gesture could queue dozens of full-chain
  // recomputes back to back and stall every other request against the
  // server for the duration. Only the settled end value matters for export
  // ("live audio never waits on this"), so collapsing a burst to one call
  // loses nothing. `immediate` bypasses the debounce for the export button's
  // own pre-flight sync, which needs the truly-latest value to have already
  // landed server-side before it POSTs /export a moment later.
  if (!projectId) return;
  if (_syncTimers[laneId]) { clearTimeout(_syncTimers[laneId]); delete _syncTimers[laneId]; }
  if (immediate) { _sendChannelSync(laneId); return; }
  _syncTimers[laneId] = setTimeout(() => {
    delete _syncTimers[laneId];
    _sendChannelSync(laneId);
  }, 120);
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
    for (const laneId of channelOrder) syncChannelToServer(laneId, true);
    await new Promise(r => setTimeout(r, 150));  // let the syncs land server-side
    const res = await fetch(`/api/project/${projectId}/export`, { method: "POST" });
    const data = await res.json();
    exportStatus.textContent = data.path ? `Saved: ${data.path}` : `Export failed: ${data.error || ""}`;
  } finally {
    exportBtn.disabled = false;
  }
});
