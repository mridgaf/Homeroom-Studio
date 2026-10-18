// Song Sketch board. A "Sketch" button on a beat calls openSketch(no); this
// swaps the chalkboard to the sketch setup. "Back to beats" puts it back.
(function () {
  const board = document.querySelector('.board');
  let box = null, au = null, S = null;       // S = state for the open beat

  const esc = s => String(s).replace(/[&<>"]/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const clock = s => !isFinite(s) ? '0:00' :
    Math.floor(s / 60) + ':' + String(Math.floor(s % 60)).padStart(2, '0');
  const opt = (obj, sel) => Object.keys(obj).map(k =>
    '<option value="' + k + '"' + (k === sel ? ' selected' : '') + '>' +
    esc(typeof obj[k] === 'string' ? obj[k] : obj[k].name) + '</option>').join('');

  function stopOthers() {                    // never two things at once
    try { audition.pause(); } catch (e) {}
    try { LoopAudio.all.forEach(a => a.pause()); } catch (e) {}
  }

  window.openSketch = async function (no) {
    stopOthers();
    if (!box) {
      box = document.createElement('div');
      box.id = 'sketchboard';
      const tray = board.querySelector('.tray');
      board.insertBefore(box, tray);
    }
    board.classList.add('sketching');
    box.hidden = false;
    box.innerHTML = '<p class="sknote">chalking up the sketch board…</p>';
    let d;
    try { d = await (await fetch('/sketch-info?no=' + encodeURIComponent(no))).json(); }
    catch (e) { d = { ok: false, error: String(e) }; }
    if (!d.ok) {
      box.innerHTML = '<div class="skhead"><h2>Song Sketch</h2>' +
        '<button class="skbtn" id="skback">← Back to beats</button></div>' +
        '<p class="skstatus bad">' + esc(d.error || 'Could not open this beat.') + '</p>';
      box.querySelector('#skback').onclick = close;
      return;
    }
    S = { d, no, preset: 'slow_reveal', roll: 0, style: '', result: null, which: 'sketch' };
    draw();
  };

  function close() {
    closePop();
    if (au) au.pause();
    board.classList.remove('sketching');
    if (box) box.hidden = true;
  }

  // An auto preset (the 2:30 song) shows the rolled plan; the others use their own lists.
  const planMoves = (P, i) => P.auto ? S.d.plans[S.preset][S.roll][i].moves : [].concat(P.moves[i]);

  const shortName = (d, ms) => ms.length ? ms.map(k => d.moves[k]).join(', ') : '·';

  // Older presets: one set of moves per section, applied to every fitting lane.
  function chipsHtml(d, P) {
    return '<div class="secs" id="sksecs">' + P.scenes.map((sc, i) => '<div class="sec"><b>Section ' + (i + 1) + '</b>' +
      '<p></p><label class="lbl">What plays</label><select class="sc" data-i="' + i + '">' +
      opt(d.scenes, sc) + '</select>' +
      '<label class="lbl">Effect moves</label><div class="mvs" data-i="' + i + '">' +
      Object.keys(d.moves).filter(k => k !== 'none').map(k => '<label><input type="checkbox" value="' + k + '"' +
        (planMoves(P, i).includes(k) ? ' checked' : '') + '> ' + esc(d.moves[k]) + '</label>').join('') +
      '</div></div>').join('') + '</div>';
  }

  // Auto types: lanes down the side, sections across. A cell is one lane's moves in one section.
  function gridHtml(d, P) {
    const plan = d.plans[S.preset][S.roll], n = P.scenes.length;
    return '<div class="lgridwrap"><div class="lgrid" id="sksecs" style="grid-template-columns:150px repeat(' + n + ',minmax(120px,1fr))">' +
      '<div class="gh"></div>' + P.scenes.map((sc, i) => '<div class="gh"><b>Section ' + (i + 1) + '</b>' +
        '<select class="sc" data-i="' + i + '">' + opt(d.scenes, sc) + '</select><p></p></div>').join('') +
      d.stems.map(st => '<div class="gl" title="' + esc(st.label) + '">' + esc(st.label) + '</div>' +
        P.scenes.map((sc, i) => {
          const ms = (plan[i].lanes || {})[st.lane] || [];
          return '<div class="gc" data-l="' + esc(st.lane) + '" data-i="' + i + '" data-m="' + ms.join(',') +
            '" title="' + esc(shortName(d, ms)) + '"><span>' + esc(shortName(d, ms)) + '</span></div>';
        }).join('')).join('') +
      '</div></div><p class="sknote">Click a cell to change that lane’s moves in that section. ' +
      'Dim cells are silent in that scene. ' + (P.styles ? 'Random' : 'Re-roll') +
      ' puts a fresh spotlight on different lanes.</p>';
  }

  // 3:00 song: Random picks a producer style + placement; the picker narrows it to one style.
  const styleOf = () => S.d.plan_styles[S.preset][S.roll];
  function stylesHtml(d) {
    const st = d.styles[styleOf()];
    return '<div class="row"><button class="skbtn on" id="skrandom">🎲 Random effects</button>' +
      '<select id="skstyle" style="width:auto"><option value="">Any style</option>' +
      Object.keys(d.styles).map(k => '<option value="' + k + '"' + (k === S.style ? ' selected' : '') + '>' +
        esc(d.styles[k].name) + '</option>').join('') + '</select></div>' +
      '<p class="sknote"><b>' + esc(st.name) + ':</b> ' + esc(st.note) + '</p>';
  }
  function randomPlan() {
    const all = S.d.plan_styles[S.preset].map((k, i) => [k, i]).filter(([k, i]) => (!S.style || k === S.style));
    const pick = all.filter(([, i]) => i !== S.roll);
    const pool = pick.length ? pick : all;
    S.roll = pool[Math.floor(Math.random() * pool.length)][1];
  }

  let pop = null;
  function openPop(cell) {
    closePop();
    const d = S.d, have = cell.dataset.m ? cell.dataset.m.split(',') : [];
    pop = document.createElement('div'); pop.className = 'gpop';
    pop.innerHTML = Object.keys(d.moves).filter(k => k !== 'none').map(k =>
      '<label><input type="checkbox" value="' + k + '"' + (have.includes(k) ? ' checked' : '') + '> ' + esc(d.moves[k]) + '</label>').join('');
    pop.onchange = () => {
      const ms = [...pop.querySelectorAll('input:checked')].map(c => c.value);
      cell.dataset.m = ms.join(','); cell.title = cell.firstChild.textContent = shortName(d, ms);
    };
    cell.appendChild(pop);
  }
  function closePop() { if (pop) { pop.remove(); pop = null; } }

  function draw() {
    const d = S.d, P = Object.assign({}, d.presets[S.preset]);
    if (P.auto) P.scenes = d.plans[S.preset][S.roll].map(s => s.scene);
    box.innerHTML =
      '<div class="skhead"><h2>Song Sketch<small>Beat ' + esc(S.no) + ' · ' +
        esc(d.bpm || '?') + ' BPM · ' + d.stems.length + ' stems</small></h2>' +
        '<button class="skbtn" id="skback">← Back to beats</button></div><hr>' +
      '<h3>1. Pick a shape</h3><div class="row" id="skpresets">' +
        Object.keys(d.presets).map(k => '<button class="skbtn' + (k === S.preset ? ' on' : '') +
          '" data-p="' + k + '">' + esc(d.presets[k].name) + '</button>').join('') + '</div>' +
      '<p class="sknote" id="skpnote">' + esc(P.note) + '</p>' +
      '<h3>2. ' + P.scenes.length + ' sections' + (P.styles ? '' : P.auto ? ' <button class="skbtn" id="skroll">Re-roll moves</button>' : '') +
        '</h3>' + (P.styles ? stylesHtml(d) : '') + (P.auto ? gridHtml(d, P) : chipsHtml(d, P)) +
      '<h3>3. Length and space</h3><div class="row"><div class="amt">Bars per section ' +
        '<select id="skbars" style="width:auto"><option>2</option><option selected>4</option><option>8</option></select></div>' +
        '<div class="amt">Echo / reverb <input type="range" id="skamt" min="0" max="1" step="0.05" value="0.6"></div></div>' +
      '<h3>4. Who is who</h3><div class="lanes">' +
        d.stems.map(s => '<div class="ln"><span title="' + esc(s.label) + '">' + esc(s.label) +
          '</span><select class="rl" data-l="' + esc(s.lane) + '">' + opt(
            Object.fromEntries(d.roles.map(r => [r, r])), s.role) + '</select></div>').join('') + '</div>' +
      '<p class="sknote">The DJ’s producer tag is left out so it isn’t repeated every section. ' +
        'Echo and reverb only catch the music and texture parts.</p>' +
      '<div class="row" style="margin-top:14px"><button class="skbtn sun" id="skgo">Make the sketch</button></div>' +
      '<div class="skstatus" id="skstatus" role="status"></div><div id="skresult"></div>';
    box.querySelector('#skback').onclick = close;
    box.querySelectorAll('#skpresets button').forEach(b => b.onclick = () => {
      const keep = { bars: box.querySelector('#skbars').value, amt: box.querySelector('#skamt').value };
      S.preset = b.dataset.p; S.roll = 0; draw();
      box.querySelector('#skbars').value = d.presets[S.preset].bars || keep.bars;
      box.querySelector('#skamt').value = keep.amt;
    });
    const redraw = change => {               // keep length + space settings across a redraw
      const keep = { bars: box.querySelector('#skbars').value, amt: box.querySelector('#skamt').value };
      change(); draw();
      box.querySelector('#skbars').value = keep.bars; box.querySelector('#skamt').value = keep.amt;
    };
    const roll = box.querySelector('#skroll');
    if (roll) roll.onclick = () => redraw(() => { S.roll = (S.roll + 1) % d.plans[S.preset].length; });
    const rnd = box.querySelector('#skrandom');
    if (rnd) rnd.onclick = () => redraw(randomPlan);
    const sty = box.querySelector('#skstyle');
    if (sty) sty.onchange = () => redraw(() => { S.style = sty.value; randomPlan(); });
    box.querySelectorAll('.gc').forEach(c => c.onclick = e => {
      if (e.target.closest('.gpop')) return;
      pop && pop.parentNode === c ? closePop() : openPop(c);
    });
    const dim = () => box.querySelectorAll('.gc').forEach(c => {
      const sc = box.querySelector('.sc[data-i="' + c.dataset.i + '"]').value;
      const role = [...box.querySelectorAll('.rl')].find(r => r.dataset.l === c.dataset.l);
      c.classList.toggle('off', !!role && d.scenes[sc].levels[d.roles.indexOf(role.value)] === 0);
    });
    box.querySelectorAll('.rl, .sc').forEach(el => el.addEventListener('change', dim));
    dim();
    const note = () => box.querySelectorAll('.sec, .gh').forEach((el, i) => {
      if (!el.querySelector('.sc')) return;
      el.querySelector('p').textContent = d.scenes[el.querySelector('.sc').value].description;
    });
    box.querySelectorAll('.sc').forEach(s => s.onchange = note);
    note();
    box.querySelector('#skgo').onclick = go;
    if (S.result) showResult();
  }

  async function go() {
    const btn = box.querySelector('#skgo'), st = box.querySelector('#skstatus');
    const roles = {};
    box.querySelectorAll('.rl').forEach(s => roles[s.dataset.l] = s.value);
    const recipe = {
      section_bars: +box.querySelector('#skbars').value,
      amount: +box.querySelector('#skamt').value, roles,
      sections: [...box.querySelectorAll('.sc')].map((el, i) => {
        const cells = [...box.querySelectorAll('.gc[data-i="' + i + '"]')];
        if (cells.length) {                    // grid: per-lane moves
          const lanes = {};
          cells.forEach(c => { if (c.dataset.m) lanes[c.dataset.l] = c.dataset.m.split(','); });
          return { scene: el.value, lanes };
        }
        return { scene: el.value,
          moves: [...box.querySelectorAll('.mvs[data-i="' + i + '"] input:checked')].map(c => c.value) };
      }) };
    btn.disabled = true; st.className = 'skstatus';
    st.textContent = 'Arranging the stems and printing the transitions…';
    if (au) au.pause();
    try {
      const r = await fetch('/sketch', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ no: S.no, lanes: S.d.stems.map(s => s.lane), recipe }) });
      const d = await r.json();
      if (!d.ok) throw new Error(d.error || 'The sketch failed.');
      S.result = d; S.which = 'sketch'; st.textContent = '';
      showResult();
    } catch (e) {
      st.className = 'skstatus bad'; st.textContent = String(e.message || e);
    }
    btn.disabled = false;
  }

  function url(name) {
    return '/sketch-file?id=' + encodeURIComponent(S.result.id) + '&name=' + encodeURIComponent(name);
  }

  function showResult() {
    const m = S.result.meta, host = box.querySelector('#skresult');
    host.innerHTML = '<h3>5. Listen</h3><div class="skplay">' +
      '<div class="row"><button class="skbtn sun" id="skpp">▶ Play</button>' +
        '<button class="skbtn" id="skab"></button>' +
        '<span id="sktime" style="margin-left:auto">0:00</span></div>' +
      '<div class="skbar" id="skbar"></div>' +
      '<input type="range" class="skseek" id="skseek" min="0" max="1000" value="0" aria-label="Position">' +
      '</div>' +
      '<p class="sknote">A/B keeps your place and plays at the same level. ' +
        m.gain_db + ' dB overall to stay under clipping.</p>' +
      (m.warnings.length ? '<p class="skwarn">' + m.warnings.map(esc).join('<br>') + '</p>' : '') +
      '<div class="row" style="margin-top:8px"><a class="skbtn" style="text-decoration:none" href="' +
        url('stems-and-mix.zip') + '" download>Download stems + mix (ZIP)</a></div>' +
      '<p class="sknote">Saved in Homeroom Auditions › Song Sketches › ' + esc(S.result.id) + '</p>';
    au = new Audio(); au.preload = 'auto'; au.src = url('sketch.wav');
    const pp = host.querySelector('#skpp'), ab = host.querySelector('#skab'),
          seek = host.querySelector('#skseek'), time = host.querySelector('#sktime'),
          bar = host.querySelector('#skbar');
    const names = S.d.scenes;
    bar.innerHTML = m.sections.map((s, i) => '<button data-t="' + s.start_s + '" style="flex:' +
      (s.end_s - s.start_s) + '">' + (i + 1) + '. ' + esc(names[s.scene].name) + '</button>').join('');
    bar.querySelectorAll('button').forEach(b => b.onclick = () => { au.currentTime = +b.dataset.t; });
    const label = () => ab.textContent = S.which === 'sketch' ? 'Hearing: the sketch' : 'Hearing: the plain loop';
    label();
    pp.onclick = () => { if (au.paused) { stopOthers(); au.play().catch(() => {}); } else au.pause(); };
    ab.onclick = () => {
      const t = au.currentTime, was = !au.paused;
      S.which = S.which === 'sketch' ? 'original' : 'sketch';
      au.src = url(S.which === 'sketch' ? 'sketch.wav' : 'original.wav');
      au.addEventListener('loadedmetadata', function f() {
        au.removeEventListener('loadedmetadata', f);
        au.currentTime = Math.min(t, au.duration || t);
        if (was) au.play().catch(() => {});
      });
      label();
    };
    au.onplay = () => pp.textContent = '❚❚ Pause';
    au.onpause = () => pp.textContent = '▶ Play';
    au.onended = () => { pp.textContent = '▶ Play'; };
    au.ontimeupdate = () => {
      const d = au.duration || m.duration_s;
      seek.value = d ? au.currentTime / d * 1000 : 0;
      time.textContent = clock(au.currentTime) + ' / ' + clock(d);
      bar.querySelectorAll('button').forEach((b, i) => b.classList.toggle('now',
        au.currentTime >= m.sections[i].start_s && au.currentTime < m.sections[i].end_s));
    };
    seek.oninput = () => { au.currentTime = seek.value / 1000 * (au.duration || m.duration_s); };
  }
})();
