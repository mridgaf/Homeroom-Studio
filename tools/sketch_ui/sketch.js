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

  window.openSketch = async function (no, src) {
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
    try { d = await (await fetch('/sketch-info?no=' + encodeURIComponent(no) +
      (src ? '&src=' + encodeURIComponent(src) : ''))).json(); }
    catch (e) { d = { ok: false, error: String(e) }; }
    if (!d.ok) {
      box.innerHTML = '<div class="skhead"><h2>Song Sketch</h2>' +
        '<button class="skbtn" id="skback">← Back to beats</button></div>' +
        '<p class="skstatus bad">' + esc(d.error || 'Could not open this beat.') + '</p>';
      box.querySelector('#skback').onclick = close;
      return;
    }
    S = { d, no, src: src || '', type: Object.keys(d.types)[0], fx: 'built_in', roll: 0, amt: null,
          result: null, which: 'sketch' };
    draw();
  };

  function close() {
    closePop();
    if (au) au.pause();
    board.classList.remove('sketching');
    if (box) box.hidden = true;
  }

  // 2026-10-21: six arrangement types x effects (built in / six genres /
  // Random = the 12 producer styles). Every plan is a whole song, 2:30-4:00.
  const plans = () => S.d.plans[S.type + '|' + S.fx];
  const shortName = (d, ms) => ms.length ? ms.map(k => d.moves[k]).join(', ') : '·';
  const HALF = { '': 'whole loop', front: 'front 4 bars', back: 'back 4 bars' };

  // Lanes down the side, sections across. A cell is one lane in one section:
  // its moves, or "sits out" (a drum variation).
  function gridHtml(d, plan) {
    const n = plan.length;
    return '<div class="lgridwrap"><div class="lgrid" id="sksecs" style="grid-template-columns:150px repeat(' + n + ',minmax(120px,1fr))">' +
      '<div class="gh"></div>' + plan.map((s, i) => '<div class="gh"><b>' + (i + 1) + '. ' + esc(s.part) + '</b>' +
        '<select class="sc" data-i="' + i + '">' + opt(d.scenes, s.scene) + '</select>' +
        '<select class="bars" data-i="' + i + '">' + [4, 8].map(b => '<option' + (b === s.bars ? ' selected' : '') +
          '>' + b + '</option>').join('') + '</select> bars ' +
        '<select class="half" data-i="' + i + '">' + opt(HALF, s.half || '') + '</select><p></p></div>').join('') +
      d.stems.map(st => '<div class="gl" title="' + esc(st.label) + '">' + esc(st.label) + '</div>' +
        plan.map((s, i) => {
          const ms = (s.lanes || {})[st.lane] || [], out = s.mute.includes(st.lane);
          return '<div class="gc' + (out ? ' muted' : '') + '" data-l="' + esc(st.lane) + '" data-i="' + i +
            '" data-m="' + ms.join(',') + '" data-out="' + (out ? 1 : '') + '"><span>' +
            esc(out ? 'sits out' : shortName(d, ms)) + '</span></div>';
        }).join('')).join('') +
      '</div></div><p class="sknote">Click a cell to change that part’s effects in that section, ' +
      'or make it sit out (drum variations). “Front/back 4 bars” plays only that half of an 8-bar loop. ' +
      'Dim cells are silent in that scene.</p>';
  }

  function songLength() {
    const bars = [...box.querySelectorAll('.bars')].reduce((a, s) => a + +s.value, 0);
    return bars * 240 / (S.d.bpm || 90);
  }

  let pop = null;
  function openPop(cell) {
    closePop();
    const d = S.d, have = cell.dataset.m ? cell.dataset.m.split(',') : [];
    pop = document.createElement('div'); pop.className = 'gpop';
    pop.innerHTML = '<label><input type="checkbox" class="out"' + (cell.dataset.out ? ' checked' : '') +
      '> <b>Sits out this section</b></label>' +
      Object.keys(d.moves).filter(k => k !== 'none').map(k =>
      '<label><input type="checkbox" value="' + k + '"' + (have.includes(k) ? ' checked' : '') + '> ' + esc(d.moves[k]) + '</label>').join('');
    pop.onchange = () => {
      const out = pop.querySelector('.out').checked;
      const ms = [...pop.querySelectorAll('input:not(.out):checked')].map(c => c.value);
      cell.dataset.m = ms.join(','); cell.dataset.out = out ? 1 : '';
      cell.classList.toggle('muted', out);
      cell.firstChild.textContent = out ? 'sits out' : shortName(d, ms);
    };
    cell.appendChild(pop);
  }
  function closePop() { if (pop) { pop.remove(); pop = null; } }

  function fxNote(d) {
    if (S.fx === 'built_in') return 'The arrangement’s own effects.';
    if (S.fx === 'random') { const st = d.styles[S.roll]; return '<b>' + esc(st.name) + ':</b> ' + esc(st.note); }
    return '<b>' + esc(d.genres[S.fx].name) + ':</b> ' + esc(d.genres[S.fx].note);
  }

  function draw() {
    const d = S.d, plan = plans()[S.roll];
    const fxBtn = (k, name) => '<button class="skbtn' + (k === S.fx ? ' on' : '') + '" data-fx="' + k + '">' + name + '</button>';
    box.innerHTML =
      '<div class="skhead"><h2>Song Sketch<small>Beat ' + esc(S.no) + (S.src ? ' (as set on the Effects page)' : '') +
        ' · ' + esc(d.bpm || '?') + ' BPM · ' + d.stems.length + ' stems</small></h2>' +
        '<button class="skbtn" id="skback">← Back to beats</button></div><hr>' +
      '<h3>1. Pick an arrangement</h3><div class="row" id="sktypes">' +
        Object.keys(d.types).map(k => '<button class="skbtn' + (k === S.type ? ' on' : '') +
          '" data-t="' + k + '">' + esc(d.types[k].name) + '</button>').join('') + '</div>' +
      '<p class="sknote">' + esc(d.types[S.type].note) + '</p>' +
      '<h3>2. Effects</h3><div class="row" id="skfx">' + fxBtn('built_in', 'Built in') +
        Object.keys(d.genres).map(k => fxBtn(k, esc(d.genres[k].name))).join('') +
        fxBtn('random', '🎲 Random') + ' <button class="skbtn" id="skroll">Re-roll</button></div>' +
      '<p class="sknote">' + fxNote(d) + '</p>' +
      '<h3>3. ' + plan.length + ' sections · <span id="sklen"></span></h3>' + gridHtml(d, plan) +
      '<div class="row"><div class="amt">Echo / reverb <input type="range" id="skamt" min="0" max="1" step="0.05" value="' +
        (S.amt != null ? S.amt : 0.6) + '"></div></div>' +
      '<h3>4. Who is who</h3><div class="lanes">' +
        d.stems.map(s => '<div class="ln"><span title="' + esc(s.label) + '">' + esc(s.label) +
          '</span><select class="rl" data-l="' + esc(s.lane) + '">' + opt(
            Object.fromEntries(d.roles.map(r => [r, r])), s.role) + '</select></div>').join('') + '</div>' +
      '<p class="sknote">The DJ’s producer tag is left out so it isn’t repeated every section.</p>' +
      '<div class="row" style="margin-top:14px"><button class="skbtn sun" id="skgo">Make the sketch</button></div>' +
      '<div class="skstatus" id="skstatus" role="status"></div><div id="skresult"></div>';
    const redraw = change => { S.amt = +box.querySelector('#skamt').value; change(); draw(); };
    box.querySelector('#skback').onclick = close;
    box.querySelectorAll('#sktypes button').forEach(b => b.onclick = () => redraw(() => { S.type = b.dataset.t; S.roll = 0; }));
    box.querySelectorAll('#skfx button[data-fx]').forEach(b => b.onclick = () => redraw(() => {
      S.fx = b.dataset.fx;
      S.roll = S.fx === 'random' ? Math.floor(Math.random() * plans().length) : 0;
    }));
    box.querySelector('#skroll').onclick = () => redraw(() => { S.roll = (S.roll + 1) % plans().length; });
    box.querySelectorAll('.gc').forEach(c => c.onclick = e => {
      if (e.target.closest('.gpop')) return;
      pop && pop.parentNode === c ? closePop() : openPop(c);
    });
    const dim = () => box.querySelectorAll('.gc').forEach(c => {
      const sc = box.querySelector('.sc[data-i="' + c.dataset.i + '"]').value;
      const role = [...box.querySelectorAll('.rl')].find(r => r.dataset.l === c.dataset.l);
      c.classList.toggle('off', !!role && d.scenes[sc].levels[d.roles.indexOf(role.value)] === 0);
    });
    const note = () => box.querySelectorAll('.gh').forEach(el => {
      if (el.querySelector('.sc')) el.querySelector('p').textContent = d.scenes[el.querySelector('.sc').value].description;
    });
    const len = () => {
      const s = songLength(), ok = s >= 150 && s <= 240;
      const el = box.querySelector('#sklen');
      el.textContent = clock(s) + (ok ? '' : ' (must be 2:30 to 4:00)');
      el.className = ok ? '' : 'bad';
      box.querySelector('#skgo').disabled = !ok;
    };
    box.querySelectorAll('.rl, .sc').forEach(el => el.addEventListener('change', dim));
    box.querySelectorAll('.sc').forEach(s => s.addEventListener('change', note));
    box.querySelectorAll('.bars').forEach(s => s.addEventListener('change', len));
    dim(); note(); len();
    box.querySelector('#skgo').onclick = go;
    if (S.result) showResult();
  }

  async function go() {
    const btn = box.querySelector('#skgo'), st = box.querySelector('#skstatus');
    const roles = {};
    box.querySelectorAll('.rl').forEach(s => roles[s.dataset.l] = s.value);
    const recipe = {
      amount: +box.querySelector('#skamt').value, roles,
      sections: [...box.querySelectorAll('.sc')].map((el, i) => {
        const lanes = {}, mute = [];
        box.querySelectorAll('.gc[data-i="' + i + '"]').forEach(c => {
          if (c.dataset.out) mute.push(c.dataset.l);
          else if (c.dataset.m) lanes[c.dataset.l] = c.dataset.m.split(',');
        });
        const half = box.querySelector('.half[data-i="' + i + '"]').value || null;
        return { scene: el.value, bars: +box.querySelector('.bars[data-i="' + i + '"]').value,
                 half, mute, lanes };
      }) };
    btn.disabled = true; st.className = 'skstatus';
    st.textContent = 'Arranging the stems and printing the transitions…';
    if (au) au.pause();
    try {
      const r = await fetch('/sketch', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ no: S.no, src: S.src, lanes: S.d.stems.map(s => s.lane), recipe }) });
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
