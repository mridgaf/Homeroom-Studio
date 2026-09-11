/* Reason Voice v2 front-end. Plain JS, no build step.
   All state lives on the server; this file renders snapshots and sends
   user actions over one WebSocket. */
"use strict";

const $ = (id) => document.getElementById(id);
let ws = null;
let lastState = null;
let openRecipePath = null;

/* ---------- websocket ---------- */

function connect() {
  ws = new WebSocket(`ws://${location.host}/ws`);
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.type === "state") render(msg);
    else if (msg.type === "doc") showDoc(msg);
    else if (msg.type === "help") showHelp(msg.items);
    else if (msg.type === "bins") renderBins(msg.bins);
    else if (msg.type === "dial") renderDial(msg.dial);
  };
  ws.onclose = () => {
    $("status").textContent = "DISCONNECTED";
    $("status").className = "pill loading";
    $("feedback").textContent =
      "Lost connection — is the ReasonVoice window in Terminal still open?";
    setTimeout(connect, 1500);
  };
}

function send(obj) {
  if (ws && ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(obj));
}

/* ---------- tiny markdown renderer (escape first, then format) ---------- */

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function inline(s) {
  return esc(s)
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

function mdlite(text) {
  const out = [];
  let list = null;
  for (const raw of text.split("\n")) {
    const line = raw.trim();
    const li = line.match(/^[-*]\s+(.*)$/) || line.match(/^\d+[.)]\s+(.*)$/);
    if (li) {
      if (!list) { list = []; }
      list.push(`<li>${inline(li[1])}</li>`);
      continue;
    }
    if (list) { out.push(`<ul>${list.join("")}</ul>`); list = null; }
    if (line) out.push(`<p>${inline(line)}</p>`);
  }
  if (list) out.push(`<ul>${list.join("")}</ul>`);
  return out.join("");
}

/* ---------- rendering ---------- */

const STATUS_LABEL = {
  idle: "READY", recording: "RECORDING…", thinking: "THINKING…",
};

function render(st) {
  lastState = st;

  // status pill
  const pill = $("status");
  if (!st.model_ready && st.status === "idle") {
    pill.textContent = "LOADING MODEL"; pill.className = "pill loading";
  } else {
    pill.textContent = STATUS_LABEL[st.status] || st.status.toUpperCase();
    pill.className = "pill " + st.status;
  }
  $("midi").classList.toggle("ok", st.midi_connected);
  $("midi").title = st.midi_connected
    ? "MIDI bridge connected"
    : "MIDI bridge NOT connected — enable the IAC Driver, restart Reason";
  $("ptt").classList.toggle("recording", st.status === "recording");
  $("pttLabel").textContent =
    st.status === "recording" ? "Listening… release when done"
      : st.model_ready ? "Hold to talk" : "Model loading…";

  // transcript + feedback
  $("heard").hidden = !st.transcript;
  $("transcript").textContent = st.transcript;
  $("feedback").textContent = st.feedback;

  renderDial(st.dial);
  renderResults(st);
  renderRecipe(st);
  renderTemplates(st.templates || []);
  renderCrates(st.crates || []);

  // settings + info
  $("setSpeak").checked = !!st.settings.speak_feedback;
  $("setModel").value = st.settings.whisper_model;
  $("setPer").value = String(st.settings.results_per_search);
  const info = st.info || {};
  $("infoLan").textContent = info.lan_url || "off";
  $("infoMidi").textContent = (info.midi_ptt_ports || []).length
    ? `CC ${info.midi_ptt_cc} on ${info.midi_ptt_ports.join(", ")}`
    : "no controller found";
}

function renderResults(st) {
  const panel = $("resultsPanel");
  if (!st.results_kind || !st.results_total) { panel.hidden = true; return; }
  panel.hidden = false;
  const first = st.results_offset + 1;
  const last = st.results_offset + st.results.length;
  const noun = st.results_kind === "recipe" ? "Recipes"
    : st.results.every((r) => r.kind === "folder") ? "Folders"
    : st.results.every((r) => r.kind === "sample") ? "Samples"
    : st.results.every((r) => r.kind === "patch") ? "Patches" : "Results";
  $("resultsTitle").textContent = `${noun} ${first}–${last} of ${st.results_total}`;
  const ol = $("results");
  ol.innerHTML = "";
  let anySample = false;
  st.results.forEach((r, i) => {
    const li = document.createElement("li");
    const sub = st.results_kind === "recipe"
      ? [r.book, r.sounds_like && `sounds like ${r.sounds_like}`].filter(Boolean).join(" · ")
      : [r.folder, r.device].filter(Boolean).join(" · ");
    if (r.path) li.title = r.path;
    li.innerHTML =
      `<span class="n">${i + 1}</span>
       <span class="info"><span class="name"></span><span class="sub"></span></span>
       <span class="row-btns"></span>`;
    li.querySelector(".name").textContent = r.name;
    li.querySelector(".sub").textContent = sub || "";
    const btns = li.querySelector(".row-btns");
    const addBtn = (label, title, command) => {
      const b = document.createElement("button");
      b.className = "small";
      b.textContent = label;
      b.title = title;
      b.onclick = () =>
        send({ type: "command", command, args: { which: i + 1 } });
      btns.appendChild(b);
    };
    if (r.kind === "sample") {
      anySample = true;
      addBtn("▶", "Preview here", "preview_result");
      addBtn("■", "Stop", "preview_stop");
      addBtn("☆", "Star into favorites (or say: add two to my drums crate)", "crate_add");
      addBtn("Load", "Send to Reason", "load_result");
      addBtn("📂", "Reveal in Finder (drag it into Reason)", "reveal_result");
    } else if (r.kind === "folder") {
      addBtn("Open", "See what's inside", "load_result");
    } else {
      addBtn(st.results_kind === "recipe" ? "Open" : "Load",
             "", "load_result");
      if (r.kind === "patch") addBtn("☆", "Star into favorites", "crate_add");
    }
    li.classList.toggle("auditioning",
      st.audition >= 0 && st.results_offset + i === st.audition);
    ol.appendChild(li);
  });
  $("stopPreview").hidden = !anySample && st.audition < 0;
  $("auditionBtn").hidden = !anySample;
  $("moreBtn").hidden = last >= st.results_total;
}

function renderRecipe(st) {
  const card = $("card");
  const r = st.recipe;
  $("walkbar").hidden = !r;
  $("empty").hidden = !!r;
  markOpenRecipe(r ? r.path : null);
  if (!r) { card.hidden = true; return; }
  card.hidden = false;

  $("rName").textContent = r.name;
  $("rBook").textContent = r.book || "recipe";
  $("rAcc").textContent = "accuracy " + r.accuracy;
  $("rAcc").className = "chip acc-" + r.accuracy.toLowerCase();
  $("rStatus").textContent = r.status;
  $("rStatus").className = "chip " + (r.status === "tested" ? "tested" : "");
  $("testedBtn").hidden = r.status !== "theoretical";
  $("rLike").textContent = r.sounds_like ? "Sounds like: " + r.sounds_like : "";
  $("rLike").hidden = !r.sounds_like;

  const box = $("rSections");
  box.innerHTML = "";
  for (const [title, content] of r.sections) {
    const sec = document.createElement("div");
    sec.className = "section";
    const h = document.createElement("h4");
    h.textContent = title;
    sec.appendChild(h);
    if (title.toLowerCase() === "steps") {
      const ol = document.createElement("ol");
      ol.className = "steps";
      r.steps.forEach((s, i) => {
        const li = document.createElement("li");
        li.appendChild(document.createTextNode(s));
        if (st.step >= 0) {
          if (i === st.step) li.className = "active";
          else if (i < st.step) li.className = "done";
        }
        ol.appendChild(li);
      });
      sec.appendChild(ol);
    } else {
      const div = document.createElement("div");
      div.className = "prose";
      div.innerHTML = mdlite(content);
      sec.appendChild(div);
    }
    box.appendChild(sec);
  }
  const active = box.querySelector("li.active");
  if (active) active.scrollIntoView({ block: "nearest", behavior: "smooth" });

  // walkthrough button states
  const started = st.step >= 0;
  document.querySelector('[data-cmd="walkthrough"]').hidden = started;
  ["step_prev", "step_repeat", "step_next"].forEach((c) => {
    document.querySelector(`#walkbar [data-cmd="${c}"]`).hidden = !started;
  });

  // template button: start a session if one matches this recipe, else explain
  const tplBtn = $("tplBtn");
  if (st.recipe_template) {
    tplBtn.textContent = "🎛 New session from template";
    tplBtn.onclick = () => send({ type: "command", command: "template_start",
                                  args: { query: st.recipe_template } });
  } else {
    tplBtn.textContent = "Save as template…";
    tplBtn.onclick = () => send({ type: "command", command: "template_howto",
                                  args: {} });
  }
}

/* ---------- the dial: the knobs on whichever device is locked ---------- */
/* Rows are built once and then updated in place, so a push arriving from
   Reason never yanks a slider out from under the finger dragging it. */

let dialRows = null;
let dialDeviceShown = null;

function buildDial(d) {
  const box = $("dialKnobs");
  box.innerHTML = "";
  dialRows = {};
  dialDeviceShown = d.device;
  for (const k of d.knobs) {
    const row = document.createElement("div");
    row.className = "dial-row";
    row.innerHTML =
      `<span class="dial-name"></span>
       <span class="dial-val"></span>
       <span class="dial-end lo"></span>
       <input type="range" min="0" max="127" value="0">
       <span class="dial-end hi"></span>`;
    const slider = row.querySelector("input");
    const val = row.querySelector(".dial-val");
    const push = () => send({ type: "command", command: "dial_set",
                              args: { knob: k.knob, value: Number(slider.value) } });
    let last = 0;
    slider.oninput = () => {
      val.textContent = "…";              // Reason's own value replaces this
      const now = Date.now();
      if (now - last < 80) return;        // onchange lands the final value
      last = now;
      push();
    };
    slider.onchange = push;
    box.appendChild(row);
    dialRows[k.knob] = { row, slider, val,
      name: row.querySelector(".dial-name"),
      lo: row.querySelector(".lo"), hi: row.querySelector(".hi") };
  }
}

function renderDial(d) {
  if (!d) return;
  $("dialPanel").hidden = false;
  $("dialDevice").textContent = d.device || "Knobs";
  $("dialLock").textContent = d.locked ? "locked" : "not locked";
  $("dialLock").className = "chip " + (d.locked ? "tested" : "");
  $("dialPanel").classList.toggle("dim", !d.locked);
  $("dialHint").hidden = d.locked;
  $("dialHint").textContent =
    "Ctrl-click the device panel in Reason → “Lock to ReasonVoice”, " +
    "then nudge any knob once so it says hello.";
  $("dialUndo").hidden = !d.undo;
  if (d.undo) {
    $("dialUndo").title =
      `Put ${d.undo.param} back to ${d.undo.shown || "position " + d.undo.pos}`;
  }

  /* Rebuild on a device change too: a different device means different
     parameters behind the same knob numbers. */
  if (!dialRows || dialDeviceShown !== d.device
      || Object.keys(dialRows).length !== d.knobs.length) buildDial(d);
  for (const k of d.knobs) {
    const r = dialRows[k.knob];
    if (!r) continue;
    r.name.textContent = k.param;
    r.val.textContent = k.shown || (k.pos === null ? "—" : String(k.pos));
    r.lo.textContent = k.lo || "0";
    r.hi.textContent = k.hi || "127";
    r.slider.disabled = !d.locked;
    if (document.activeElement !== r.slider && k.pos !== null) {
      r.slider.value = String(k.pos);
    }
  }
}

/* ---------- templates ---------- */

function renderTemplates(items) {
  const box = $("tplList");
  box.innerHTML = "";
  if (!items.length) {
    const p = document.createElement("p");
    p.className = "tpl-empty";
    p.textContent = "None yet — open a recipe and press “Save as template…”, or click ＋ above.";
    box.appendChild(p);
    return;
  }
  for (const t of items) {
    const row = document.createElement("div");
    row.className = "tpl-row";
    const name = document.createElement("span");
    name.className = "tpl-name";
    name.textContent = (t.kind === "song" ? "🎵 " : "🎛 ") + t.name;
    name.title = t.path;
    const b = document.createElement("button");
    b.className = "small";
    b.textContent = t.kind === "song" ? "New session" : "Add to rack";
    b.onclick = () => send({ type: "command", command: "template_start",
                             args: { query: t.name } });
    row.appendChild(name);
    row.appendChild(b);
    box.appendChild(row);
  }
}

/* ---------- sample bins ---------- */

function renderBins(bins) {
  const box = $("binList");
  box.innerHTML = "";
  $("binsSection").hidden = !bins.length;
  for (const bin of bins) {
    const b = document.createElement("button");
    b.title = bin.query;
    b.textContent = bin.label;
    const c = document.createElement("span");
    c.className = "count";
    c.textContent = bin.count;
    b.appendChild(c);
    b.onclick = () => send({ type: "text", text: bin.query });
    box.appendChild(b);
  }
}

async function loadBins() {
  renderBins(await (await fetch("/api/bins")).json());
}

/* ---------- crates ---------- */

function renderCrates(crates) {
  const box = $("crateList");
  box.innerHTML = "";
  $("cratesSection").hidden = !crates.length;
  for (const c of crates) {
    const b = document.createElement("button");
    b.textContent = "★ " + c.name;
    const n = document.createElement("span");
    n.className = "count";
    n.textContent = c.count;
    b.appendChild(n);
    b.onclick = () => send({ type: "command", command: "crate_open",
                             args: { name: c.name } });
    box.appendChild(b);
  }
}

/* ---------- recipe book sidebar ---------- */

const BOOK_LABEL = { rock: "Rock", "hip-hop": "Hip-hop" };

async function loadBook() {
  const recipes = await (await fetch("/api/recipes")).json();
  const groups = {};
  for (const r of recipes) {
    const key = r.book || "other";
    (groups[key] = groups[key] || []).push(r);
  }
  const box = $("recipeList");
  box.innerHTML = "";
  for (const key of Object.keys(groups).sort()) {
    const g = document.createElement("div");
    g.className = "book-group";
    const h = document.createElement("h3");
    h.textContent = BOOK_LABEL[key] || key;
    g.appendChild(h);
    for (const r of groups[key]) {
      const b = document.createElement("button");
      b.className = "recipe-item";
      b.dataset.path = r.path;
      const name = document.createElement("span");
      name.textContent = r.name;
      const sub = document.createElement("span");
      sub.className = "sub";
      sub.textContent = [
        r.sounds_like && `sounds like ${r.sounds_like}`,
        `accuracy ${r.accuracy}`, r.status,
      ].filter(Boolean).join(" · ");
      b.appendChild(name);
      b.appendChild(sub);
      b.onclick = () => send({ type: "open_recipe", path: r.path });
      g.appendChild(b);
    }
    box.appendChild(g);
  }
  markOpenRecipe(openRecipePath);
}

function markOpenRecipe(path) {
  openRecipePath = path;
  document.querySelectorAll(".recipe-item").forEach((b) => {
    b.classList.toggle("open", b.dataset.path === path);
  });
}

/* ---------- doc panel (device references) ---------- */

function showDoc(msg) {
  $("docTitle").textContent = msg.name;
  $("docBody").innerHTML = mdlite(msg.body.replace(/^#.*$/m, ""));
  $("docPanel").hidden = false;
}

/* ---------- help ---------- */

function showHelp(items) {
  const t = $("helpTable");
  t.innerHTML = "";
  for (const [phrase, what] of items) {
    const tr = document.createElement("tr");
    const td1 = document.createElement("td");
    td1.textContent = "“" + phrase + "”";
    const td2 = document.createElement("td");
    td2.textContent = what;
    tr.appendChild(td1);
    tr.appendChild(td2);
    t.appendChild(tr);
  }
  $("helpModal").hidden = false;
}

/* ---------- push-to-talk (button + spacebar) ---------- */

let talking = false;

function pttDown() {
  if (talking) return;
  talking = true;
  send({ type: "ptt_start" });
}

function pttUp() {
  if (!talking) return;
  talking = false;
  send({ type: "ptt_stop" });
}

const ptt = $("ptt");
ptt.addEventListener("pointerdown", (e) => { e.preventDefault(); pttDown(); });
window.addEventListener("pointerup", pttUp);
ptt.addEventListener("pointerleave", () => { if (talking) pttUp(); });

window.addEventListener("keydown", (e) => {
  if (e.code !== "Space" || e.repeat) return;
  const tag = document.activeElement && document.activeElement.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
  e.preventDefault();
  pttDown();
});
window.addEventListener("keyup", (e) => {
  if (e.code === "Space") pttUp();
});
window.addEventListener("blur", pttUp);

/* ---------- wiring ---------- */

document.querySelectorAll("[data-cmd]").forEach((b) => {
  b.addEventListener("click", () =>
    send({ type: "command", command: b.dataset.cmd, args: {} }));
});

$("typeForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const text = $("typebox").value.trim();
  if (text) send({ type: "text", text });
  $("typebox").value = "";
});

$("claudeLoops").onclick = () => send({ type: "command", command: "claude_loops", args: {} });
$("moreBtn").onclick = () => send({ type: "command", command: "more_results", args: {} });
$("stopPreview").onclick = () => send({ type: "command", command: "preview_stop", args: {} });
$("auditionBtn").onclick = () => send({ type: "command", command: "audition", args: {} });
$("testedBtn").onclick = () => send({ type: "command", command: "recipe_tested", args: {} });
$("clearResults").onclick = () => { $("resultsPanel").hidden = true; };
$("docClose").onclick = () => { $("docPanel").hidden = true; };
$("dialUndo").onclick = () => send({ type: "command", command: "dial_undo", args: {} });
$("helpBtn").onclick = () => send({ type: "command", command: "help", args: {} });
$("tplHow").onclick = () => send({ type: "command", command: "template_howto", args: {} });
$("tplFolder").onclick = () => send({ type: "command", command: "templates_folder", args: {} });
$("settingsBtn").onclick = () => { $("settingsModal").hidden = false; };

document.querySelectorAll(".overlay").forEach((ov) => {
  ov.addEventListener("click", (e) => { if (e.target === ov) ov.hidden = true; });
  ov.querySelector(".close").onclick = () => { ov.hidden = true; };
});

$("setSpeak").onchange = (e) =>
  send({ type: "set", key: "speak_feedback", value: e.target.checked });
$("setModel").onchange = (e) =>
  send({ type: "set", key: "whisper_model", value: e.target.value });
$("setPer").onchange = (e) =>
  send({ type: "set", key: "results_per_search", value: Number(e.target.value) });

connect();
loadBook();
loadBins();
