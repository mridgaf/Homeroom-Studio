// Effects Controller face (owner-approved mockup 11, 2026-10-03).
// Ten big knobs, each one of the Sound Engine's existing effects. A knob
// never touches an AudioNode itself: it moves the fine-tune sliders and
// fires their own events (app.js fireControl), so live sound, the server
// sync and Export all stay on the one tested path.

// [slider id, value at 0%, extra at 100%] — knob % maps linearly onto each
const EFFECTS = [
  { name: "EQ",       tip: "Bass + air lift",           ctl: [["lowDb", 0, 9], ["highDb", 0, 6]] },
  { name: "Compress", tip: "Squash + punch",            ctl: [["compRatio", 1, 7], ["compMakeup", 0, 4]] },
  { name: "Drive",    tip: "Saturation / warmth",       ctl: [["satMix", 0, 100]] },
  { name: "Width",    tip: "Wider stereo",              ctl: [["widthKnob", 1, 1]] },
  { name: "Chorus",   tip: "Thicken",                   ctl: [["choMix", 0, 100]] },
  { name: "Phaser",   tip: "Sweeping whoosh",           ctl: [["phsMix", 0, 100]] },
  { name: "Echo",     tip: "Repeats in time",           ctl: [["dlyMix", 0, 100]] },
  { name: "Stutter",  tip: "Beat repeat",               ctl: [["brMix", 0, 100]] },
  { name: "Reverb",   tip: "Room / space",              ctl: [["revWet", 0, 100]] },
  { name: "Convolve", tip: "Drop a sound in Fine tune", ctl: [["convMix", 0, 100]], needsIr: true },
];
for (const fx of EFFECTS) { fx.pct = 0; fx.on = false; }

const knobsEl = document.getElementById("knobs");
const targetEl = document.getElementById("knobTarget");
const holdBtn = document.getElementById("holdBtn");
const dryWetEl = document.getElementById("dryWet");
let held = false;

// --- apply a knob to the beat ------------------------------------------
function targetLanes() {
  return targetEl.value ? [targetEl.value] : channelOrder.slice();
}

function pushEffect(fx) {
  const p = fx.on ? fx.pct / 100 : 0;
  const keep = selectedLane;
  for (const lane of targetLanes()) {
    const ch = channels[lane];
    // an empty convolver outputs silence — raising its mix would MUTE the stem
    if (!ch || (fx.needsIr && !ch.irName)) continue;
    selectedLane = lane;  // the slider handlers all act on the selected stem
    for (const [id, base, span] of fx.ctl) fireControl(id, base + p * span);
  }
  selectedLane = keep;
  if (keep && channels[keep]) loadRackFromChannel(channels[keep]);
}

// ponytail: one pending push per knob per frame, so a fast drag over a
// 10-stem beat doesn't fire 10 x 60 slider events a second
const pending = new Set();
function schedulePush(fx) {
  if (!pending.size) requestAnimationFrame(() => {
    for (const f of pending) pushEffect(f);
    pending.clear();
  });
  pending.add(fx);
}

// --- knob drawing --------------------------------------------------------
const SWEEP = 270, START = 135;  // degrees, clockwise from 3 o'clock
function arc(r, a0, a1) {
  const pt = a => [60 + r * Math.cos(a * Math.PI / 180), 60 + r * Math.sin(a * Math.PI / 180)];
  const [x0, y0] = pt(a0), [x1, y1] = pt(a1);
  return `M${x0.toFixed(2)} ${y0.toFixed(2)}A${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1.toFixed(2)} ${y1.toFixed(2)}`;
}

function drawKnob(fx) {
  const shown = fx.pct;
  const end = START + SWEEP * shown / 100;
  fx.el.querySelector(".lit").setAttribute("d", shown > 0 ? arc(48, START, end) : "");
  fx.el.querySelector(".ptr").setAttribute("transform", `rotate(${end} 60 60)`);
  fx.el.querySelector(".pct").textContent = Math.round(shown) + "%";
  fx.el.classList.toggle("on", fx.on);
  const sw = fx.el.querySelector(".sw");
  sw.setAttribute("aria-pressed", fx.on);
  sw.querySelector("b").textContent = fx.on ? "ON" : "OFF";
  fx.el.querySelector(".dial").setAttribute("aria-valuenow", Math.round(shown));
}

function setPct(fx, pct) {
  if (held) return;
  fx.pct = Math.min(100, Math.max(0, pct));
  fx.on = fx.pct > 0;  // turning a knob up switches it on
  drawKnob(fx);
  schedulePush(fx);
}

function buildKnobs() {
  knobsEl.innerHTML = "";
  for (const fx of EFFECTS) {
    const card = document.createElement("div");
    card.className = "fx";
    card.innerHTML = `
      <div class="fxname">${esc(fx.name)}</div>
      <div class="dial" role="slider" tabindex="0" aria-label="${esc(fx.name)} amount"
           aria-valuemin="0" aria-valuemax="100" title="${esc(fx.tip)} — drag up/down, or scroll">
        <svg viewBox="0 0 120 120" aria-hidden="true">
          <path class="track" d="${arc(48, START, START + SWEEP)}"/>
          <path class="lit" d=""/>
          <circle class="cap" cx="60" cy="60" r="38"/>
          <g class="ptr"><rect x="88" y="56.5" width="16" height="7" rx="2"/></g>
        </svg>
        <span class="pct">0%</span>
      </div>
      <button class="sw" aria-pressed="false" aria-label="${esc(fx.name)} on/off"><b>OFF</b><i></i></button>
      <div class="fxtip">${esc(fx.tip)}</div>`;
    fx.el = card;
    const dial = card.querySelector(".dial");
    // vertical drag, like a hardware knob: 200 px = full sweep
    dial.addEventListener("pointerdown", e => {
      if (held) return;
      dial.setPointerCapture(e.pointerId);
      const y0 = e.clientY, p0 = fx.pct;
      const move = ev => setPct(fx, p0 + (y0 - ev.clientY) / 2);
      const up = () => { dial.removeEventListener("pointermove", move); dial.removeEventListener("pointerup", up); };
      dial.addEventListener("pointermove", move);
      dial.addEventListener("pointerup", up);
    });
    dial.addEventListener("wheel", e => { e.preventDefault(); setPct(fx, fx.pct - Math.sign(e.deltaY) * 2); }, { passive: false });
    dial.addEventListener("keydown", e => {
      const d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1, PageUp: 10, PageDown: -10 }[e.key];
      if (d) { e.preventDefault(); setPct(fx, fx.pct + d); }
    });
    card.querySelector(".sw").addEventListener("click", () => {
      if (held) return;
      fx.on = !fx.on;
      if (fx.on && fx.pct === 0) fx.pct = 25;  // ON with nothing dialled in would do nothing
      drawKnob(fx);
      schedulePush(fx);
    });
    knobsEl.appendChild(card);
    drawKnob(fx);
  }
}
buildKnobs();

// read the knobs back off the sliders (a DJ's preset, or a stem switch)
function knobsFromSliders() {
  for (const fx of EFFECTS) {
    const [id, base, span] = fx.ctl[0];
    const v = parseFloat(document.getElementById(id).value);
    fx.pct = Math.round(Math.min(1, Math.max(0, (v - base) / span)) * 100);
    fx.on = fx.pct > 0;
    drawKnob(fx);
  }
  refreshConvolve();
}

function refreshConvolve() {
  const fx = EFFECTS.find(f => f.needsIr);
  const any = targetLanes().some(l => channels[l] && channels[l].irName);
  fx.el.classList.toggle("noir", !any);
  fx.el.querySelector(".fxtip").textContent = any ? "Through your sound" : fx.tip;
}
document.getElementById("convDrop").addEventListener("drop", () => setTimeout(refreshConvolve, 1500));
document.getElementById("convClear").addEventListener("click", () => setTimeout(refreshConvolve, 50));
targetEl.addEventListener("change", () => {
  if (targetEl.value) selectChannel(targetEl.value);
  knobsFromSliders();
});

// --- Hold, Dry/Wet, Return to Clean ---------------------------------------
holdBtn.addEventListener("click", () => {
  held = !held;
  holdBtn.setAttribute("aria-pressed", held);
  holdBtn.textContent = held ? "HELD" : "HOLD";
  document.getElementById("workspace").classList.toggle("held", held);
  dryWetEl.disabled = held;
  document.getElementById("cleanBtn").disabled = held;
});

dryWetEl.addEventListener("input", () => {
  dryWet = parseFloat(dryWetEl.value) / 100;
  document.getElementById("dryWetVal").textContent = dryWetEl.value + "%";
  dryWetEl.style.setProperty("--fill", dryWetEl.value + "%");
  applyDryWet();
});

document.getElementById("cleanBtn").addEventListener("click", () => {
  if (held) return;
  // switches everything OFF but keeps each knob's amount, so ON brings it back
  for (const fx of EFFECTS) { fx.on = false; drawKnob(fx); schedulePush(fx); }
});

// --- strip: name, BPM, waveform, play state ---------------------------------
const wave = document.getElementById("wave");
let peaks = [];

function computePeaks() {
  const n = 220;
  const bufs = channelOrder.map(l => channels[l].audioBuffer);
  const len = Math.max(...bufs.map(b => b.length));
  peaks = new Array(n).fill(0);
  for (const b of bufs) {
    const d = b.getChannelData(0), step = Math.max(1, Math.floor(len / n / 64));
    for (let i = 0; i < b.length; i += step) {
      const k = Math.floor(i / len * n);
      peaks[k] = Math.max(peaks[k], Math.abs(d[i]));
    }
  }
  const top = Math.max(...peaks, 1e-6);
  peaks = peaks.map(p => p / top);
}

function drawWave() {
  const dpr = window.devicePixelRatio || 1;
  const w = wave.clientWidth, h = wave.clientHeight;
  if (wave.width !== w * dpr) { wave.width = w * dpr; wave.height = h * dpr; }
  const g = wave.getContext("2d");
  g.setTransform(dpr, 0, 0, dpr, 0, 0);
  g.clearRect(0, 0, w, h);
  if (!peaks.length || !channelOrder.length) return;
  const dur = channels[channelOrder[0]].audioBuffer.duration;
  const at = audioCtx ? playheadSeconds() / dur : 0;
  const bw = w / peaks.length;
  peaks.forEach((p, i) => {
    g.fillStyle = i / peaks.length <= at ? "#9be22d" : "#bdbdbd";
    const bh = Math.max(2, p * (h - 6));
    g.fillRect(i * bw, (h - bh) / 2, Math.max(1, bw - 1.2), bh);
  });
  g.fillStyle = "#fff";
  g.fillRect(at * w - 1, 0, 2, h);
}

wave.addEventListener("click", e => {
  if (!channelOrder.length || !audioCtx) return;
  const dur = channels[channelOrder[0]].audioBuffer.duration;
  const t = (e.offsetX / wave.clientWidth) * dur;
  if (isPlaying) { stopPlayback(); play(t); } else { pausedAt = t; }
});

function tick() {
  const playing = typeof isPlaying !== "undefined" && isPlaying;
  document.getElementById("playBtn").classList.toggle("playing", playing);
  document.getElementById("playBtn").setAttribute("aria-label", playing ? "Pause" : "Play");
  document.getElementById("playDot").classList.toggle("live", playing);
  document.getElementById("playWord").textContent = playing ? "Playing" : (pausedAt > 0 ? "Paused" : "Stopped");
  drawWave();
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

// called by app.js openProject() once a beat or file is loaded
function effectsProjectOpened(data) {
  document.getElementById("strip").hidden = false;
  document.getElementById("bpmLine").textContent = data.bpm ? `${Math.round(data.bpm)} BPM` : "";
  targetEl.innerHTML = '<option value="">Whole beat</option>' +
    channelOrder.map(l => `<option value="${esc(l)}">${esc(channels[l].label)} only</option>`).join("");
  computePeaks();
  knobsFromSliders();  // a DJ's preset shows up on the knobs
}

// Space = play/pause, like every music app
document.addEventListener("keydown", e => {
  if (e.code !== "Space" || /INPUT|SELECT|TEXTAREA|BUTTON/.test(e.target.tagName) || e.target.closest(".dial")) return;
  e.preventDefault();
  document.getElementById("playBtn").click();
});
