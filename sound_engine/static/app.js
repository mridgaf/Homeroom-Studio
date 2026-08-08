// Real-time preview runs entirely in the browser's own audio engine
// (Web Audio API native nodes) — instant, sample-accurate, no Python
// garbage-collector risk. Export bounces through the tested Python
// pedalboard engine (tools/audio_engine.py) for the final file, so the
// heavy DSP is the same code the beat generator uses. Chain order (both
// live and export) is: EQ -> Compressor -> Saturation -> Width -> Reverb.
let fileId = null;
let audioCtx = null;
let audioBuffer = null;   // decoded original, decoded once per upload
let sourceNode = null;    // recreated each Play (can't restart a source)
let lowShelf, midPeak, highShelf, bypassGain, wetGain;
let compressor;
let satDry, satWet, waveshaper, satOut;
let splitter, merger, midBus, sideBus, sideWidth;
let revDry, revWet, convolver, revOut;
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

const RAMP_SECONDS = 0.02;  // setTargetAtTime time-constant — smooth knob
                             // moves, no zipper-noise clicks (same reason
                             // pedalboard smooths param changes internally,
                             // verified separately in the Python engine)

function bindRamped(id, getNode, param, transform) {
  const el = document.getElementById(id);
  const out = document.getElementById(id + "Val");
  el.addEventListener("input", () => {
    const raw = parseFloat(el.value);
    out.textContent = raw.toFixed(raw >= 10 || raw <= -10 ? 0 : 1);
    const n = getNode();
    if (!n || !audioCtx) return;
    const v = transform ? transform(raw) : raw;
    n[param].setTargetAtTime(v, audioCtx.currentTime, RAMP_SECONDS);
  });
}

bindRamped("lowDb", () => lowShelf, "gain");
bindRamped("midDb", () => midPeak, "gain");
bindRamped("highDb", () => highShelf, "gain");
bindRamped("compThreshold", () => compressor, "threshold");
bindRamped("compRatio", () => compressor, "ratio");
bindRamped("compAttack", () => compressor, "attack", ms => ms / 1000);
bindRamped("compRelease", () => compressor, "release", ms => ms / 1000);
bindRamped("satMix", () => satWet, "gain", pct => pct / 100);
bindRamped("widthKnob", () => sideWidth, "gain");
bindRamped("revMix", () => revWet, "gain", pct => pct / 100);

// dry-side gains that mirror a mix slider (1 - mix) need a second binding
document.getElementById("satMix").addEventListener("input", e => {
  if (!satDry || !audioCtx) return;
  satDry.gain.setTargetAtTime(1 - parseFloat(e.target.value) / 100,
                               audioCtx.currentTime, RAMP_SECONDS);
});
document.getElementById("revMix").addEventListener("input", e => {
  if (!revDry || !audioCtx) return;
  revDry.gain.setTargetAtTime(1 - parseFloat(e.target.value) / 100,
                               audioCtx.currentTime, RAMP_SECONDS);
});

// drive and reverb size aren't smoothly rampable params — they rebuild a
// curve / impulse response. Reassigning that buffer on every "input" tick
// mid-drag risks an audible click each step (found in review), so throttle
// the actual rebuild to ~20Hz; the value label still updates every tick for
// live feel, and a trailing "change" listener guarantees the final dragged-
// to value always lands even if its last tick got throttled out. Both
// listeners also skip the rebuild if the value hasn't actually changed
// since the last one applied — makeReverbIR() is randomized (fresh noise
// each call), so without this dedupe, a throttled "input" tick and the
// immediately-following "change" for the SAME final value would swap in
// two different random buffers back to back, clicking at the exact moment
// this fix was meant to make click-free (found in re-review).
let lastSatDriveTick = 0, lastSatDriveApplied = null;
document.getElementById("satDrive").addEventListener("input", e => {
  document.getElementById("satDriveVal").textContent = parseFloat(e.target.value).toFixed(1);
  const now = performance.now();
  if (now - lastSatDriveTick < 50) return;
  lastSatDriveTick = now;
  const val = parseFloat(e.target.value);
  if (val === lastSatDriveApplied) return;
  lastSatDriveApplied = val;
  if (waveshaper) waveshaper.curve = makeSaturationCurve(val);
});
document.getElementById("satDrive").addEventListener("change", e => {
  const val = parseFloat(e.target.value);
  if (val === lastSatDriveApplied) return;
  lastSatDriveApplied = val;
  if (waveshaper) waveshaper.curve = makeSaturationCurve(val);
});

let lastRevSizeTick = 0, lastRevSizeApplied = null;
document.getElementById("revSize").addEventListener("input", e => {
  document.getElementById("revSizeVal").textContent = parseFloat(e.target.value).toFixed(1);
  const now = performance.now();
  if (now - lastRevSizeTick < 50) return;
  lastRevSizeTick = now;
  const val = parseFloat(e.target.value);
  if (val === lastRevSizeApplied) return;
  lastRevSizeApplied = val;
  if (convolver && audioCtx) convolver.buffer = makeReverbIR(audioCtx, val);
});
document.getElementById("revSize").addEventListener("change", e => {
  const val = parseFloat(e.target.value);
  if (val === lastRevSizeApplied) return;
  lastRevSizeApplied = val;
  if (convolver && audioCtx) convolver.buffer = makeReverbIR(audioCtx, val);
});

["dragenter", "dragover"].forEach(ev =>
  dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.add("drag"); }));
["dragleave", "drop"].forEach(ev =>
  dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.remove("drag"); }));
dropzone.addEventListener("drop", e => {
  const f = e.dataTransfer.files[0];
  if (f) upload(f);
});
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) upload(fileInput.files[0]);
});

async function upload(file) {
  const form = new FormData();
  form.append("file", file);
  let res, data;
  try {
    res = await fetch("/api/upload", { method: "POST", body: form });
    data = await res.json();
  } catch (e) {
    alert("Couldn't reach the Sound Engine server: " + e);
    return;
  }
  if (!res.ok || data.error) {
    alert("Couldn't load that file: " + (data.error || res.statusText));
    return;
  }
  fileId = data.file_id;
  fileName.textContent = data.filename;
  fileMeta.textContent = `${data.duration_s}s · ${data.sample_rate} Hz`;
  exportStatus.textContent = "";

  stopPlayback();
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const arrayBuf = await (await fetch(`/api/audio/${fileId}/dry?t=${Date.now()}`)).arrayBuffer();
  audioBuffer = await audioCtx.decodeAudioData(arrayBuf);
  // defensive: dsp.py upmixes mono to dual-mono server-side today, so this
  // never actually fires via the normal upload path — but the M/S width
  // graph below assumes 2 channels (ChannelSplitterNode silences a missing
  // channel rather than duplicating it), so don't trust an unrelated file
  // never to change (found in review).
  if (audioBuffer.numberOfChannels === 1) {
    const stereo = audioCtx.createBuffer(2, audioBuffer.length, audioBuffer.sampleRate);
    stereo.copyToChannel(audioBuffer.getChannelData(0), 0);
    stereo.copyToChannel(audioBuffer.getChannelData(0), 1);
    audioBuffer = stereo;
  }
  buildGraph();
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

function buildGraph() {
  // persistent effect chain — knobs mutate these nodes live; only the
  // source node gets recreated per Play (Web Audio sources are one-shot)

  // tear down the previous file's chain before building a new one — every
  // upload() run re-enters this function from scratch. Web Audio only
  // processes nodes reachable from destination, so cutting these two exit
  // points is enough to orphan the whole old chain (its internal nodes stay
  // connected to each other but that no longer matters) instead of leaking
  // 12+ nodes into destination for the rest of the tab session (found in
  // review).
  if (wetGain) wetGain.disconnect();
  if (bypassGain) bypassGain.disconnect();

  const v = id => parseFloat(document.getElementById(id).value);

  lowShelf = audioCtx.createBiquadFilter();
  lowShelf.type = "lowshelf"; lowShelf.frequency.value = 120;
  lowShelf.gain.value = v("lowDb");

  midPeak = audioCtx.createBiquadFilter();
  midPeak.type = "peaking"; midPeak.frequency.value = 800; midPeak.Q.value = 0.9;
  midPeak.gain.value = v("midDb");

  highShelf = audioCtx.createBiquadFilter();
  highShelf.type = "highshelf"; highShelf.frequency.value = 8000;
  highShelf.gain.value = v("highDb");

  // --- compressor: threshold/ratio/attack(s)/release(s), Web Audio units
  // (seconds) differ from the export path's ms — converted at the slider
  compressor = audioCtx.createDynamicsCompressor();
  compressor.threshold.value = v("compThreshold");
  compressor.ratio.value = v("compRatio");
  compressor.attack.value = v("compAttack") / 1000;
  compressor.release.value = v("compRelease") / 1000;
  // pedalboard.Compressor (export path) has no knee parameter at all — 0
  // (hard knee) is the closest live/export reconciliation available; a soft
  // knee here is shaping export can never replicate (found in review, was 6).
  compressor.knee.value = 0;

  // --- saturation: parallel dry/wet through a WaveShaper, mix sums at
  // satOut (Web Audio auto-sums multiple connections into one input)
  satDry = audioCtx.createGain(); satDry.gain.value = 1 - v("satMix") / 100;
  satWet = audioCtx.createGain(); satWet.gain.value = v("satMix") / 100;
  waveshaper = audioCtx.createWaveShaper();
  waveshaper.curve = makeSaturationCurve(v("satDrive"));
  waveshaper.oversample = "4x";
  satOut = audioCtx.createGain(); satOut.gain.value = 1;

  // --- stereo width: M/S via splitter/merger + gain math, matches
  // tools/audio_engine.py's stereo_width() exactly (mid untouched, only
  // the side signal is scaled — loudness-neutral on the mono sum)
  splitter = audioCtx.createChannelSplitter(2);
  merger = audioCtx.createChannelMerger(2);
  const midGainL = audioCtx.createGain(); midGainL.gain.value = 0.5;
  const midGainR = audioCtx.createGain(); midGainR.gain.value = 0.5;
  midBus = audioCtx.createGain(); midBus.gain.value = 1;
  const sideGainL = audioCtx.createGain(); sideGainL.gain.value = 0.5;
  const sideGainR = audioCtx.createGain(); sideGainR.gain.value = -0.5;
  sideBus = audioCtx.createGain(); sideBus.gain.value = 1;
  sideWidth = audioCtx.createGain(); sideWidth.gain.value = v("widthKnob");
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
  revDry = audioCtx.createGain(); revDry.gain.value = 1 - v("revMix") / 100;
  revWet = audioCtx.createGain(); revWet.gain.value = v("revMix") / 100;
  convolver = audioCtx.createConvolver();
  convolver.normalize = true;
  convolver.buffer = makeReverbIR(audioCtx, v("revSize"));
  revOut = audioCtx.createGain(); revOut.gain.value = 1;

  // bypass A/B: wetGain/bypassGain crossfade between processed and dry
  // paths so "Bypass" is instant and glitch-free, not a graph rewire
  wetGain = audioCtx.createGain();
  bypassGain = audioCtx.createGain();
  setBypass(bypassToggle.checked);

  lowShelf.connect(midPeak).connect(highShelf).connect(compressor);
  compressor.connect(satDry).connect(satOut);
  compressor.connect(satWet).connect(waveshaper).connect(satOut);
  satOut.connect(splitter);
  merger.connect(revDry).connect(revOut);
  merger.connect(revWet).connect(convolver).connect(revOut);
  revOut.connect(wetGain).connect(audioCtx.destination);
  // bypassGain taps the source directly (wired in when a source exists)
}

function setBypass(on) {
  if (!wetGain || !bypassGain) return;
  const t = audioCtx.currentTime;
  wetGain.gain.setTargetAtTime(on ? 0 : 1, t, RAMP_SECONDS);
  bypassGain.gain.setTargetAtTime(on ? 1 : 0, t, RAMP_SECONDS);
}
bypassToggle.addEventListener("change", () => setBypass(bypassToggle.checked));

function play() {
  if (!audioBuffer) return;
  stopPlayback();
  sourceNode = audioCtx.createBufferSource();
  sourceNode.buffer = audioBuffer;
  sourceNode.loop = loopToggle.checked;
  sourceNode.connect(lowShelf);          // processed path
  sourceNode.connect(bypassGain);        // dry bypass path
  bypassGain.connect(audioCtx.destination);
  sourceNode.start();
  isPlaying = true;
  playStatus.textContent = "Playing…";
  sourceNode.onended = () => {
    if (isPlaying) { isPlaying = false; playStatus.textContent = ""; }
  };
}

function stopPlayback() {
  if (sourceNode) {
    try { sourceNode.onended = null; sourceNode.stop(); } catch (e) {}
    sourceNode.disconnect();
    sourceNode = null;
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
  if (document.hidden && isPlaying && sourceNode && sourceNode.loop) {
    stopPlayback();
  }
});
window.addEventListener("pagehide", stopPlayback);

exportBtn.addEventListener("click", async () => {
  // disabled for the whole round trip — a double-click used to fire two
  // overlapping /api/process calls racing on the same server-side session,
  // and could export the wrong values or (with same-second timestamps)
  // silently overwrite the first export (found in review)
  if (!fileId || exportBtn.disabled) return;
  exportBtn.disabled = true;
  exportStatus.textContent = "Rendering final file…";
  const v = id => parseFloat(document.getElementById(id).value);
  const params = {
    low_db: v("lowDb"), mid_db: v("midDb"), high_db: v("highDb"),
    comp_threshold_db: v("compThreshold"), comp_ratio: v("compRatio"),
    comp_attack_ms: v("compAttack"), comp_release_ms: v("compRelease"),
    sat_drive_db: v("satDrive"), sat_mix: v("satMix") / 100,
    width: v("widthKnob"),
    reverb_size_s: v("revSize"), reverb_mix: v("revMix") / 100,
  };
  try {
    await fetch(`/api/process/${fileId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params),
    });
    const res = await fetch(`/api/export/${fileId}`, { method: "POST" });
    const data = await res.json();
    exportStatus.textContent = data.path ? `Saved: ${data.path}` : "Export failed";
  } finally {
    exportBtn.disabled = false;
  }
});
