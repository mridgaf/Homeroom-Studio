// The Sound of Science (owner-approved mockup 14, 2026-10-16).
// Pure layout: every sound change goes through app.js / effects.js —
// setLaneBus, setBusLevel, toggleMute/Solo, the knob target select — so
// live audio, server sync and export stay on the one tested path.
const notebookEl = document.getElementById("notebook");
const knobGrid = document.getElementById("knobs");
const stableEl = document.getElementById("stable");
const scardEl = document.getElementById("scard");
const lanesEl = document.getElementById("lanes");
let openStem = null;     // lane whose own card is open, or null = the table
let openPage = "stems";  // "stems" | "A" | "B"

const DRUM_WORDS = /kick|snare|hat|perc|clap|rim|tom|shak|crash|ride|cymb|tamb|conga|bongo|drum|break|snap/i;
const LOW_WORDS = /bass|sub|808|boom/i;

// stems are named "lane - sample name"; the lane part is the instrument
const shortName = label => label.split(" - ")[0].replace(/\d+$/, "").trim() || label;

function family(label) {
  const s = shortName(label);
  if (LOW_WORDS.test(s)) return "low";            // "bass drum" is the 808, not a drum hit
  if (DRUM_WORDS.test(s)) return "drums";
  return DRUM_WORDS.test(label) ? "drums" : "mel";  // "woods - MZ Rim" is a drum
}

// "kick drum" -> Kd, "snare" -> Sn, "chords" -> Cd: a chemical-symbol look
function symbolFor(label) {
  const words = shortName(label).replace(/\(.*?\)|\d+/g, " ").trim().split(/\s+/).filter(Boolean);
  if (!words.length) return "?";
  const first = words[0][0].toUpperCase();
  if (words.length > 1) return first + words[1][0].toLowerCase();
  const next = words[0].slice(1).match(/[^aeiou\W]/i);
  return first + (next ? next[0].toLowerCase() : "");
}

// how many of the ten effects are doing anything on this channel
function effectsOn(ch) {
  return [ch.lowShelf.gain.value || ch.highShelf.gain.value || ch.midPeak.gain.value,
          ch.compressor.ratio.value > 1, ch.satWet.gain.value > 0,
          Math.abs(ch.sideWidth.gain.value - 1) > 1e-3, ch.choWet.gain.value > 0,
          ch.phsWet.gain.value > 0, ch.dly.mix > 0, ch.br.mix > 0,
          ch.revWet.gain.value > 0, ch.convWet.gain.value > 0].filter(Boolean).length;
}

function tileHtml(laneId, i, cls) {
  const ch = channels[laneId];
  return `<span class="no">${i + 1}</span><b class="sym">${esc(symbolFor(ch.label))}</b>` +
         `<span class="nm" title="${esc(ch.label)}">${esc(ch.label.split(" - ")[0])}</span>${cls || ""}`;
}

// --- point the ten knobs at a stem or a flask ------------------------------
function aimKnobs(target, slot) {
  if (!channels[target]) return;
  targetEl.value = target;
  targetEl.dispatchEvent(new Event("change"));   // selectChannel + knobsFromSliders
  document.getElementById(slot).appendChild(knobGrid);
  notebookEl.classList.toggle("busA", target === "bus:A");
  notebookEl.classList.toggle("busB", target === "bus:B");
}

// --- notebook pages ----------------------------------------------------------
function showPage(p) {
  openPage = p;
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("on", t.dataset.p === p));
  document.getElementById("p-stems").classList.toggle("on", p === "stems");
  document.getElementById("p-flask").classList.toggle("on", p !== "stems");
  if (p === "stems") { if (openStem) openCard(openStem); return; }
  document.getElementById("flaskTitle").textContent = "Flask " + p;
  const bus = channels["bus:" + p];
  const lvl = document.getElementById("flaskLevel");
  lvl.value = bus ? bus.faderDb : 0;
  document.getElementById("flaskLevelVal").textContent = `${lvl.value} dB`;
  drawFlaskWho();
  aimKnobs("bus:" + p, "flaskSlot");
}
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
  if (t.dataset.p === "stems" && openPage === "stems") closeCard();
  showPage(t.dataset.p);
}));

function drawFlaskWho() {
  if (openPage === "stems") return;
  const who = channelOrder.filter(l => channels[l].bus === openPage).map(l => channels[l].label);
  document.getElementById("flaskWho").textContent = who.length
    ? "Holding: " + who.join(", ")
    : "Empty. Put stems in here with the A / B buttons.";
}

document.getElementById("flaskLevel").addEventListener("input", e => {
  if (!projectId) return;
  setBusLevel("bus:" + openPage, parseFloat(e.target.value));
  document.getElementById("flaskLevelVal").textContent = `${e.target.value} dB`;
});

function openCard(laneId) {
  openStem = laneId;
  const ch = channels[laneId];
  const i = channelOrder.indexOf(laneId);
  document.getElementById("tableView").hidden = true;
  scardEl.hidden = false;
  const big = document.getElementById("bigTile");
  big.className = "big " + family(ch.label);
  big.innerHTML = tileHtml(laneId, i);
  drawConn();
  aimKnobs(laneId, "stemSlot");
}

function closeCard() {
  openStem = null;
  scardEl.hidden = true;
  document.getElementById("tableView").hidden = false;
  drawTable();
}
document.getElementById("backBtn").addEventListener("click", closeCard);

function drawConn() {
  if (!openStem) return;
  const r = channels[openStem].bus || "";
  const el = document.getElementById("conn");
  el.innerHTML = "Connect to: " + ["", "A", "B"].map(k =>
    `<button data-k="${k}" class="${k} ${r === k ? "on" : ""}">${k ? "Flask " + k : "None"}</button>`).join("");
  el.querySelectorAll("button").forEach(b => b.addEventListener("click", () => route(openStem, b.dataset.k)));
}

function drawTable() {
  const has = channelOrder.length > 0;
  document.getElementById("tableHint").textContent = has
    ? "Click a stem's square to open its own effects and pick its flask."
    : "Pick a beat on the board first.";
  document.getElementById("tableKey").hidden = !has;
  stableEl.innerHTML = "";
  channelOrder.forEach((laneId, i) => {
    const ch = channels[laneId];
    const r = ch.bus || "";
    const n = effectsOn(ch);
    const b = document.createElement("button");
    b.className = `st ${family(ch.label)}${ch.muted ? " muted" : ""}`;
    b.innerHTML = tileHtml(laneId, i,
      `<span class="bus ${r || "none"}">${r || "–"}</span><span class="fxn">${n} effect${n === 1 ? "" : "s"} on</span>`);
    b.addEventListener("click", () => openCard(laneId));
    stableEl.appendChild(b);
  });
}

// --- board: the stems, with level / M / S / flask -----------------------------
function route(laneId, b) {
  setLaneBus(laneId, b);
  drawAll();
}

function drawLanes() {
  lanesEl.innerHTML = "";
  for (const laneId of channelOrder) {
    const ch = channels[laneId];
    const r = ch.bus || "";
    const row = document.createElement("div");
    row.className = "lane";
    row.innerHTML = `<span class="ln" title="${esc(ch.label)} — click to open it in the notebook">${esc(ch.label.split(" - ")[0])}</span>
      <input type="range" min="-24" max="12" step="0.5" value="${ch.faderDb}" aria-label="${esc(ch.label)} level">
      <span class="db">${ch.faderDb > 0 ? "+" : ""}${ch.faderDb} dB</span>
      <div class="ms"><button class="m ${ch.muted ? "active" : ""}" aria-label="Mute">M</button><button class="s ${ch.solo ? "active" : ""}" aria-label="Solo">S</button></div>
      <div class="routes"><button class="route A ${r === "A" ? "on" : ""}" aria-label="Send to Flask A">A</button><button class="route B ${r === "B" ? "on" : ""}" aria-label="Send to Flask B">B</button></div>`;
    row.querySelector(".ln").addEventListener("click", () => { showPage("stems"); openCard(laneId); });
    row.querySelector("input").addEventListener("input", e => {
      ch.faderDb = parseFloat(e.target.value);
      row.querySelector(".db").textContent = `${ch.faderDb > 0 ? "+" : ""}${ch.faderDb} dB`;
      recomputeAudibility();
      syncChannelToServer(laneId);
    });
    row.querySelector(".m").addEventListener("click", () => toggleMute(laneId));
    row.querySelector(".s").addEventListener("click", () => toggleSolo(laneId));
    row.querySelectorAll(".route").forEach(b => b.addEventListener("click", () => {
      const k = b.textContent;
      route(laneId, ch.bus === k ? "" : k);
    }));
    lanesEl.appendChild(row);
  }
}

function drawAll() {
  for (const k of ["A", "B"]) {
    const n = channelOrder.filter(l => channels[l].bus === k).length;
    document.getElementById("c" + k).textContent = `${n} stem${n === 1 ? "" : "s"}`;
  }
  drawLanes();
  if (!openStem) drawTable();
  drawConn();
  drawFlaskWho();
}

// app.js redraws its strip list on every mute/solo/select — redraw ours too
const _renderChannelList = renderChannelList;
renderChannelList = function () { _renderChannelList(); if (typeof lanesEl !== "undefined") drawAll(); };

// a knob move changes a tile's "N effects on" — refresh it once things settle
document.addEventListener("pointerup", () => { if (!openStem && channelOrder.length) setTimeout(drawTable, 50); });

// app.js -> effects.js call this when a beat opens; add the flasks as targets
const _effectsProjectOpened = effectsProjectOpened;
effectsProjectOpened = function (data) {
  _effectsProjectOpened(data);
  targetEl.insertAdjacentHTML("beforeend",
    '<option value="bus:A">Flask A</option><option value="bus:B">Flask B</option>');
  openStem = null;
  scardEl.hidden = true;
  document.getElementById("tableView").hidden = false;
  showPage("stems");
  drawAll();
};

drawTable();
