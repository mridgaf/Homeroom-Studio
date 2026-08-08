// Real-time preview runs entirely in the browser's own audio engine
// (Web Audio API native nodes) — instant, sample-accurate, no Python
// garbage-collector risk. Export bounces through the tested Python
// pedalboard engine (tools/audio_engine.py) for the final file, so the
// heavy DSP is the same code the beat generator uses.
let fileId = null;
let audioCtx = null;
let audioBuffer = null;   // decoded original, decoded once per upload
let sourceNode = null;    // recreated each Play (can't restart a source)
let lowShelf, midPeak, highShelf, bypassGain, wetGain;
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

const sliders = {
  lowDb: { node: () => lowShelf, param: "gain" },
  midDb: { node: () => midPeak, param: "gain" },
  highDb: { node: () => highShelf, param: "gain" },
};
for (const id of Object.keys(sliders)) {
  const el = document.getElementById(id);
  const out = document.getElementById(id + "Val");
  el.addEventListener("input", () => {
    out.textContent = parseFloat(el.value).toFixed(1);
    const { node, param } = sliders[id];
    const n = node();
    if (n) n[param].setTargetAtTime(parseFloat(el.value), audioCtx.currentTime, RAMP_SECONDS);
  });
}

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
  buildGraph();
  dropzone.classList.add("hidden");
  workspace.classList.remove("hidden");
}

function buildGraph() {
  // persistent effect chain — knobs mutate these nodes live; only the
  // source node gets recreated per Play (Web Audio sources are one-shot)
  lowShelf = audioCtx.createBiquadFilter();
  lowShelf.type = "lowshelf";
  lowShelf.frequency.value = 120;
  lowShelf.gain.value = parseFloat(document.getElementById("lowDb").value);

  midPeak = audioCtx.createBiquadFilter();
  midPeak.type = "peaking";
  midPeak.frequency.value = 800;
  midPeak.Q.value = 0.9;
  midPeak.gain.value = parseFloat(document.getElementById("midDb").value);

  highShelf = audioCtx.createBiquadFilter();
  highShelf.type = "highshelf";
  highShelf.frequency.value = 8000;
  highShelf.gain.value = parseFloat(document.getElementById("highDb").value);

  // bypass A/B: wetGain/bypassGain crossfade between processed and dry
  // paths so "Bypass" is instant and glitch-free, not a graph rewire
  wetGain = audioCtx.createGain();
  bypassGain = audioCtx.createGain();
  setBypass(bypassToggle.checked);

  lowShelf.connect(midPeak).connect(highShelf).connect(wetGain).connect(audioCtx.destination);
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
  // and could export the wrong EQ values or (with same-second timestamps)
  // silently overwrite the first export (found in review)
  if (!fileId || exportBtn.disabled) return;
  exportBtn.disabled = true;
  exportStatus.textContent = "Rendering final file…";
  const eq = {
    low_db: parseFloat(document.getElementById("lowDb").value),
    mid_db: parseFloat(document.getElementById("midDb").value),
    high_db: parseFloat(document.getElementById("highDb").value),
  };
  try {
    await fetch(`/api/process/${fileId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(eq),
    });
    const res = await fetch(`/api/export/${fileId}`, { method: "POST" });
    const data = await res.json();
    exportStatus.textContent = data.path ? `Saved: ${data.path}` : "Export failed";
  } finally {
    exportBtn.disabled = false;
  }
});
