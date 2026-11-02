// Physics layout (owner-approved handoff, 2026-11-01). Pure layout, like
// science.js: every sound change still goes through app.js / effects.js /
// science.js (openCard, showPage, toggleMute, setBusLevel, the fine-tune
// sliders), so live audio, server sync and Export stay on the tested path.
const FX_LIST = [["eq", "EQ"], ["comp", "Compressor"], ["sat", "Saturation"], ["crunch", "Crunch"],
  ["punch", "Punch"], ["reverb", "Reverb"], ["delay", "Delay"], ["stutter", "Stutter"],
  ["space", "Space"], ["width", "Width"], ["chorus", "Chorus"], ["phaser", "Phaser"]];
const chanlistEl = document.getElementById("chanlist");
const wholeCard = document.getElementById("wholeCard");
const eqSvg = document.getElementById("eqcurve");
eqSvg.removeAttribute("preserveAspectRatio");
let fxOpen = "eq";
let wholeMode = false;

// is this effect doing anything on that channel? (same tests as effectsOn)
function fxActive(ch, k) {
  if (!ch) return false;
  try {
    switch (k) {
      case "eq": return !!(ch.lowShelf.gain.value || ch.midPeak.gain.value || ch.highShelf.gain.value);
      case "comp": return ch.compressor.ratio.value > 1;
      case "sat": return ch.satWet.gain.value > 0;
      case "crunch": return ch.crunch.mix > 0;
      case "punch": return ch.punch.mix > 0;
      case "reverb": return ch.revWet.gain.value > 0;
      case "delay": return ch.dly.mix > 0;
      case "stutter": return ch.br.mix > 0;
      case "space": return ch.convWet.gain.value > 0;
      case "width": return Math.abs(ch.sideWidth.gain.value - 1) > 1e-3;
      case "chorus": return ch.choWet.gain.value > 0;
      case "phaser": return ch.phsWet.gain.value > 0;
    }
  } catch (e) {}
  return false;
}
const POWER = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v8"/><path d="M6.3 6.6a8 8 0 1 0 11.4 0"/></svg>';

// --- 1. the stem list ----------------------------------------------------------
function paintList() {
  const rows = [`<button type="button" class="crow whole${wholeMode ? " sel" : ""}" data-l="">` +
    `<span class="code">All</span><span class="nm">Whole beat</span><span class="chev">&rsaquo;</span></button>`];
  channelOrder.forEach((l, i) => {
    const ch = channels[l];
    const sel = !wholeMode && openPage === "stems" && openStem === l;
    rows.push(`<button type="button" class="crow c${i % 4}${sel ? " sel" : ""}${ch.muted ? " muted" : ""}" data-l="${esc(l)}" title="${esc(ch.label)}">` +
      `<span class="code"><small>${i + 1}</small>${esc(symbolFor(ch.label))}</span>` +
      `<span class="nm">${esc(ch.label.split(" - ")[0])}</span>` +
      `<span class="tags">${ch.muted ? "<i>M</i>" : ""}${ch.solo ? "<i>S</i>" : ""}${ch.bus ? `<i class="b${ch.bus}">${ch.bus}</i>` : ""}</span>` +
      `<span class="chev">&rsaquo;</span></button>`);
  });
  chanlistEl.innerHTML = rows.join("");
  chanlistEl.querySelectorAll(".crow").forEach(b => b.addEventListener("click", () => {
    if (b.dataset.l) { wholeMode = false; showPage("stems"); openCard(b.dataset.l); }
    else showWhole();
  }));
}

function showWhole() {
  wholeMode = true;
  showPage("stems");
  if (openStem) closeCard();
  targetEl.value = "";
  targetEl.dispatchEvent(new Event("change"));
  document.getElementById("wholeSlot").appendChild(knobGrid);
  notebookEl.classList.remove("busA", "busB");
  wholeCard.hidden = false;
  paintAll();
}

// --- 2. the selected stem: level + pan knobs, M / S ----------------------------
const KSWEEP = 270, KSTART = 135;
function karc(a0, a1) {
  const pt = a => [60 + 46 * Math.cos(a * Math.PI / 180), 60 + 46 * Math.sin(a * Math.PI / 180)];
  const [x0, y0] = pt(a0), [x1, y1] = pt(a1);
  return `M${x0.toFixed(2)} ${y0.toFixed(2)}A46 46 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1.toFixed(2)} ${y1.toFixed(2)}`;
}
// a drag-up/down knob over a value; o = {label, min, max, step, zero, get, set, fmt, cls}
function knob(o) {
  const wrap = document.createElement("div");
  wrap.className = "pk " + (o.cls || "");
  wrap.innerHTML = `<span class="pkl">${o.label}</span>` +
    `<span class="pkd" role="slider" tabindex="0" aria-label="${o.label}" aria-valuemin="${o.min}" aria-valuemax="${o.max}"` +
    ` title="Drag up or down, or use the arrow keys. Double-click resets.">` +
    `<svg viewBox="0 0 120 120" aria-hidden="true"><path class="kt" d="${karc(KSTART, KSTART + KSWEEP)}"/><path class="kl"/>` +
    `<circle class="kc" cx="60" cy="60" r="34"/><g class="kp"><rect x="86" y="57" width="16" height="6" rx="2"/></g></svg></span>` +
    `<output class="pkv"></output>`;
  const dial = wrap.querySelector(".pkd");
  const frac = v => (v - o.min) / (o.max - o.min);
  const show = () => {
    const v = o.get(), end = KSTART + KSWEEP * frac(v), z = KSTART + KSWEEP * frac(o.zero);
    wrap.querySelector(".kl").setAttribute("d", Math.abs(end - z) > .5 ? karc(Math.min(z, end), Math.max(z, end)) : "");
    wrap.querySelector(".kp").setAttribute("transform", `rotate(${end} 60 60)`);
    wrap.querySelector(".pkv").textContent = o.fmt(v);
    dial.setAttribute("aria-valuenow", v);
    dial.setAttribute("aria-valuetext", o.fmt(v));
  };
  const put = v => {
    v = Math.max(o.min, Math.min(o.max, Math.round(v / o.step) * o.step));
    o.set(+v.toFixed(3)); show();
  };
  // moves only while the button is held (owner rule from the Beat Machine knobs)
  dial.addEventListener("pointerdown", e => {
    dial.setPointerCapture(e.pointerId);
    const y0 = e.clientY, v0 = o.get(), span = o.max - o.min;
    const move = ev => (ev.buttons & 1) ? put(v0 + (y0 - ev.clientY) / 200 * span) : up();
    const up = () => { dial.removeEventListener("pointermove", move); dial.removeEventListener("pointerup", up);
                       dial.removeEventListener("lostpointercapture", up); };
    dial.addEventListener("pointermove", move);
    dial.addEventListener("pointerup", up);
    dial.addEventListener("lostpointercapture", up);
  });
  dial.addEventListener("keydown", e => {
    const d = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }[e.key];
    if (d) { e.preventDefault(); put(o.get() + d * o.step); }
  });
  dial.addEventListener("dblclick", () => put(o.zero));
  show();
  return wrap;
}

function paintStrip() {
  if (!openStem || !channels[openStem]) return;
  const l = openStem, ch = channels[l];
  document.getElementById("scname").textContent = ch.label.split(" - ")[0];
  const lp = document.getElementById("lpknobs");
  lp.innerHTML = "";
  lp.appendChild(knob({ label: "Level", min: -24, max: 12, step: 0.5, zero: 0, cls: "lvlk",
    get: () => ch.faderDb,
    set: v => { ch.faderDb = v; recomputeAudibility(); syncChannelToServer(l); },
    fmt: v => (v > 0 ? "+" : "") + v.toFixed(1) + " dB" }));
  lp.appendChild(knob({ label: "Pan", min: -1, max: 1, step: 0.05, zero: 0, cls: "pank",
    get: () => ch.pan,
    set: v => { ch.pan = v; if (ch.panner) ch.panner.pan.setTargetAtTime(v, audioCtx.currentTime, RAMP_SECONDS);
                syncChannelToServer(l); },
    fmt: v => Math.abs(v) < 0.01 ? "C" : (v < 0 ? "L" : "R") + Math.round(Math.abs(v) * 100) }));
  const ms = document.getElementById("msrow");
  ms.innerHTML = `<button type="button" class="m${ch.muted ? " active" : ""}" aria-pressed="${ch.muted}" title="Mute">M</button>` +
                 `<button type="button" class="s${ch.solo ? " active" : ""}" aria-pressed="${ch.solo}" title="Solo">S</button>`;
  ms.querySelector(".m").addEventListener("click", () => toggleMute(l));
  ms.querySelector(".s").addEventListener("click", () => toggleSolo(l));
}

// --- 3 + 4. one effect's settings, and the list of effects ----------------------
function paintFx() {
  const ch = channels[selectedLane];
  document.querySelectorAll(".channelRack .panel").forEach(p => p.hidden = p.dataset.fx !== fxOpen);
  document.getElementById("fxtitle").textContent = FX_LIST.find(f => f[0] === fxOpen)[1];
  document.getElementById("fxpow").className = "pw" + (fxActive(ch, fxOpen) ? " on" : "");
  document.getElementById("fxpow").innerHTML = POWER;
  eqSvg.style.display = fxOpen === "eq" ? "" : "none";
  const list = document.getElementById("fxlist");
  list.innerHTML = FX_LIST.map(([k, name], i) =>
    `<button type="button" class="frow a${i % 4}${k === fxOpen ? " sel" : ""}${fxActive(ch, k) ? " on" : ""}" data-k="${k}">` +
    `<span class="pw" title="${fxActive(ch, k) ? "Doing something on this stem" : "Off on this stem"}">${POWER}</span>` +
    `<span class="nm">${name}</span><span class="chev">&rsaquo;</span></button>`).join("");
  list.querySelectorAll(".frow").forEach(b => b.addEventListener("click", () => { fxOpen = b.dataset.k; paintFx(); }));
  drawEq();
}

// the EQ curve is the stem's REAL filters (getFrequencyResponse), not a drawing
function drawEq() {
  const ch = channels[selectedLane];
  if (fxOpen !== "eq" || !ch || !ch.lowShelf) { eqSvg.innerHTML = ""; return; }
  const W = 640, H = 220, N = 240, PADL = 34, PADB = 22, top = 8;
  const f = new Float32Array(N), mag = new Float32Array(N), ph = new Float32Array(N), tot = new Float32Array(N);
  for (let i = 0; i < N; i++) f[i] = 20 * Math.pow(1000, i / (N - 1));
  for (const node of [ch.lowShelf, ch.midPeak, ch.highShelf]) {
    node.getFrequencyResponse(f, mag, ph);
    for (let i = 0; i < N; i++) tot[i] += 20 * Math.log10(Math.max(mag[i], 1e-6));
  }
  const x = hz => PADL + Math.log10(hz / 20) / 3 * (W - PADL - 6);
  const y = db => top + (18 - Math.max(-18, Math.min(18, db))) / 36 * (H - top - PADB);
  let g = "";
  for (const db of [18, 12, 6, 0, -6, -12, -18]) g += `<line class="gl${db ? "" : " z"}" x1="${PADL}" x2="${W - 6}" y1="${y(db)}" y2="${y(db)}"/><text class="gt" x="${PADL - 6}" y="${y(db) + 4}" text-anchor="end">${db > 0 ? "+" : ""}${db}</text>`;
  for (const hz of [50, 100, 200, 500, 1000, 2000, 5000, 10000]) g += `<line class="gl" x1="${x(hz)}" x2="${x(hz)}" y1="${top}" y2="${H - PADB}"/><text class="gt" x="${x(hz)}" y="${H - 6}" text-anchor="middle">${hz >= 1000 ? hz / 1000 + "k" : hz}</text>`;
  const pts = Array.from(f, (hz, i) => `${x(hz).toFixed(1)},${y(tot[i]).toFixed(1)}`);
  const at = hz => { let i = 0; while (i < N - 1 && f[i] < hz) i++; return tot[i]; };
  const dots = [[ch.lowShelf.frequency.value, "lo"], [ch.midPeak.frequency.value, "mi"], [ch.highShelf.frequency.value, "hi"]]
    .map(([hz, c]) => `<circle class="dot ${c}" cx="${x(hz)}" cy="${y(at(hz))}" r="6"><title>${Math.round(hz)} Hz</title></circle>`).join("");
  eqSvg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  eqSvg.innerHTML = g + `<path class="area" d="M${x(20)},${y(0)}L${pts.join("L")}L${x(20000)},${y(0)}Z"/>` +
    `<polyline class="curve" points="${pts.join(" ")}"/>` + dots;
}

// --- bottom: bus levels -----------------------------------------------------------
document.querySelectorAll(".buscard").forEach(card => {
  const b = card.dataset.bus, r = card.querySelector(".buslvl"), out = card.querySelector("output");
  r.addEventListener("input", () => {
    if (!projectId) return;
    setBusLevel("bus:" + b, parseFloat(r.value));
    out.textContent = r.value + " dB";
    if (openPage === b) {
      document.getElementById("flaskLevel").value = r.value;
      document.getElementById("flaskLevelVal").textContent = r.value + " dB";
    }
  });
  card.querySelector(".busname").addEventListener("click", () => { wholeMode = false; wholeCard.hidden = true; showPage(b); });
});
function paintBuses() {
  document.querySelectorAll(".buscard").forEach(card => {
    const bus = channels["bus:" + card.dataset.bus];
    if (!bus) return;
    card.querySelector(".buslvl").value = bus.faderDb;
    card.querySelector("output").textContent = bus.faderDb + " dB";
    card.classList.toggle("sel", !wholeMode && openPage === card.dataset.bus);
  });
}

function paintAll() { paintList(); paintStrip(); paintFx(); paintBuses(); }

// --- hook into science.js / app.js ---------------------------------------------------
const _openCard = openCard;
openCard = function (laneId) { wholeMode = false; wholeCard.hidden = true; _openCard(laneId); paintAll(); };
const _showPage = showPage;
showPage = function (p) {
  if (p !== "stems") { wholeMode = false; wholeCard.hidden = true; }
  _showPage(p); paintList(); paintFx(); paintBuses();
};
const _closeCard = closeCard;
closeCard = function () { _closeCard(); paintList(); };
const _renderList = renderChannelList;
renderChannelList = function () { _renderList(); if (typeof chanlistEl !== "undefined") { paintList(); paintStrip(); } };
const _opened = effectsProjectOpened;
effectsProjectOpened = function (data) {
  _opened(data);
  wholeMode = false; wholeCard.hidden = true;
  if (channelOrder.length) openCard(channelOrder[0]); else paintAll();
};

// any slider or knob move: refresh the on/off lights, the EQ curve and bus levels
let pend = false;
function soon() {
  if (pend) return;
  pend = true;
  requestAnimationFrame(() => { pend = false; paintFxLights(); drawEq(); paintBuses(); });
  setTimeout(drawEq, 120);              // the filters ramp for ~20 ms
}
function paintFxLights() {
  const ch = channels[selectedLane];
  document.querySelectorAll("#fxlist .frow").forEach(b => b.classList.toggle("on", fxActive(ch, b.dataset.k)));
  document.getElementById("fxpow").className = "pw" + (fxActive(ch, fxOpen) ? " on" : "");
}
document.addEventListener("input", soon);
document.addEventListener("change", soon);
document.addEventListener("pointerup", () => setTimeout(soon, 60));
targetEl.addEventListener("change", () => setTimeout(paintFx, 0));

paintAll();
