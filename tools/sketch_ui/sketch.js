// Song Sketch workspace. A "Sketch" button on a beat calls openSketch(no);
// this swaps the generator for the sketch setup. "Back to beats" puts it back.
// 2026-11-01: laid out like the approved handoff mockup (instruments down the
// side, sections across, a cell editor on the right). Same data, same /sketch
// recipe, same controls: one Echo/reverb amount, move checkboxes per cell.
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
  const code = s => (window.code ? window.code(s) : s.slice(0, 2));

  function stopOthers() {                    // never two things at once
    try { audition.pause(); } catch (e) {}
    try { LoopAudio.all.forEach(a => a.pause()); } catch (e) {}
  }

  window.openSketch = async function (no, src) {
    stopOthers();
    if (!box) {
      box = document.createElement('div');
      box.id = 'sketchboard';
      board.appendChild(box);
    }
    board.classList.add('sketching');
    document.body.classList.add('sketching');
    box.hidden = false;
    window.scrollTo(0, 0);
    box.innerHTML = '<p class="sknote">Setting up the sketch&hellip;</p>';
    let d;
    try { d = await (await fetch('/sketch-info?no=' + encodeURIComponent(no) +
      (src ? '&src=' + encodeURIComponent(src) : ''))).json(); }
    catch (e) { d = { ok: false, error: String(e) }; }
    if (!d.ok) {
      box.innerHTML = '<div class="skhead"><div class="sktitle">Song Sketch</div>' +
        '<button class="btn" id="skback">&larr; Back to beats</button></div>' +
        '<p class="skstatus bad">' + esc(d.error || 'Could not open this beat.') + '</p>';
      box.querySelector('#skback').onclick = close;
      return;
    }
    S = { d, no, src: src || '', type: Object.keys(d.types)[0], fx: 'built_in', roll: 0, amt: null,
          result: null, which: 'sketch', cell: null };
    draw();
  };

  function close() {
    if (au) au.pause();
    board.classList.remove('sketching');
    document.body.classList.remove('sketching');
    if (box) box.hidden = true;
  }

  // Six arrangement types x effects (built in / six genres / Random = the
  // 12 producer styles). Every plan is a whole song, 2:30-4:00.
  const plans = () => S.d.plans[S.type + '|' + S.fx];
  const shortName = (d, ms) => ms.length ? ms.map(k => d.moves[k]).join(', ') : 'Plays';
  const HALF = { '': 'Whole loop', front: 'Front 4 bars', back: 'Back 4 bars' };

  // Lanes down the side, sections across. A cell is one lane in one section:
  // its moves, or "sits out" (a drum variation). Each lane keeps one colour
  // pair (background / marks) in every section.
  function gridHtml(d, plan) {
    const n = plan.length;
    return '<div class="lgrid" id="sksecs" style="--n:' + n + ';grid-template-columns:230px repeat(' + n + ',minmax(118px,1fr))">' +
      '<div class="gh gcorner"><b>Instruments</b><span>Who is who</span></div>' +
      plan.map((s, i) => '<div class="gh s' + (i % 4) + '"><div class="ghtop"><b>' + esc(s.part) + '</b>' +
        '<select class="bars" data-i="' + i + '" aria-label="' + esc(s.part) + ' length">' + [4, 8].map(b => '<option value="' + b + '"' +
          (b === s.bars ? ' selected' : '') + '>' + b + ' bars</option>').join('') + '</select></div>' +
        '<select class="half" data-i="' + i + '" aria-label="' + esc(s.part) + ' loop part">' + opt(HALF, s.half || '') + '</select>' +
        '<select class="sc" data-i="' + i + '" aria-label="' + esc(s.part) + ' scene">' + opt(d.scenes, s.scene) + '</select>' +
        '<p></p></div>').join('') +
      d.stems.map((st, li) => '<div class="gl"><span class="code l' + (li % 4) + '">' + esc(code(st.label)) + '</span>' +
          '<span class="glname" title="' + esc(st.label) + '">' + esc(st.label) + '</span>' +
          '<select class="rl" data-l="' + esc(st.lane) + '" aria-label="' + esc(st.label) + ' role">' +
            opt(Object.fromEntries(d.roles.map(r => [r, r])), st.role) + '</select></div>' +
        plan.map((s, i) => {
          const ms = (s.lanes || {})[st.lane] || [], out = s.mute.includes(st.lane);
          return '<button type="button" class="gc l' + (li % 4) + (out ? ' muted' : '') + '" data-l="' + esc(st.lane) +
            '" data-i="' + i + '" data-m="' + ms.join(',') + '" data-out="' + (out ? 1 : '') + '"><span>' +
            esc(out ? 'Out' : shortName(d, ms)) + '</span></button>';
        }).join('')).join('') +
      '</div>';
  }

  function songLength() {
    const bars = [...box.querySelectorAll('.bars')].reduce((a, s) => a + +s.value, 0);
    return bars * 240 / (S.d.bpm || 90);
  }

  // The cell editor (right-hand panel): sits out + the effect moves.
  function sideHtml() {
    const c = S.cell && box.querySelector('.gc[data-l="' + CSS.escape(S.cell.l) + '"][data-i="' + S.cell.i + '"]');
    if (!c) return '<p class="sknote">Click a cell to edit that instrument in that section: ' +
      'make it sit out (a drum variation) or pick its effect moves.</p>' +
      '<p class="sknote">&ldquo;Front/back 4 bars&rdquo; plays only that half of an 8-bar loop. ' +
      'Dim cells are silent in that scene.</p>';
    const d = S.d, st = d.stems.find(x => x.lane === c.dataset.l), li = d.stems.indexOf(st);
    const part = plans()[S.roll][+c.dataset.i].part, have = c.dataset.m ? c.dataset.m.split(',') : [];
    return '<div class="sidehead"><span class="code l' + (li % 4) + '">' + esc(code(st.label)) + '</span>' +
        '<b>' + esc(st.label) + ' &middot; ' + esc(part) + '</b>' +
        '<button type="button" class="x" id="skcellx" aria-label="Close">&times;</button></div>' +
      '<label class="chk big"><input type="checkbox" class="out"' + (c.dataset.out ? ' checked' : '') +
        '> <span><b>Sits out this section</b><small>This instrument is muted in the ' + esc(part) + '.</small></span></label>' +
      '<h4>Effect moves</h4><div class="moves">' +
      Object.keys(d.moves).filter(k => k !== 'none').map(k =>
        '<label class="chk"><input type="checkbox" value="' + k + '"' + (have.includes(k) ? ' checked' : '') +
        (c.dataset.out ? ' disabled' : '') + '> ' + esc(d.moves[k]) + '</label>').join('') + '</div>';
  }
  function paintSide() {
    const side = box.querySelector('#skside');
    side.innerHTML = sideHtml();
    box.querySelectorAll('.gc').forEach(g => g.classList.toggle('picked',
      !!S.cell && g.dataset.l === S.cell.l && g.dataset.i === S.cell.i));
    const x = side.querySelector('#skcellx');
    if (x) x.onclick = () => { S.cell = null; paintSide(); };
    side.onchange = () => {
      const c = box.querySelector('.gc.picked');
      if (!c) return;
      const out = side.querySelector('.out').checked;
      const ms = [...side.querySelectorAll('.moves input:checked')].map(i => i.value);
      c.dataset.m = ms.join(','); c.dataset.out = out ? 1 : '';
      c.classList.toggle('muted', out);
      c.firstChild.textContent = out ? 'Out' : shortName(S.d, ms);
      side.querySelectorAll('.moves input').forEach(i => i.disabled = out);
    };
  }

  function fxNote(d) {
    if (S.fx === 'built_in') return 'The arrangement&rsquo;s own effects.';
    if (S.fx === 'random') { const st = d.styles[S.roll]; return '<b>' + esc(st.name) + ':</b> ' + esc(st.note); }
    return '<b>' + esc(d.genres[S.fx].name) + ':</b> ' + esc(d.genres[S.fx].note);
  }

  function draw() {
    const d = S.d, plan = plans()[S.roll];
    const genre = d.genres[S.fx] ? S.fx : '';
    box.innerHTML =
      '<div class="skhead"><div class="sktitle">Beat ' + esc(S.no) + (S.src ? ' (as set on the Effects page)' : '') +
        ' &middot; ' + esc(d.bpm || '?') + ' BPM &middot; ' + d.stems.length + ' stems</div>' +
        '<button class="btn" id="skback">&larr; Back to beats</button></div>' +
      '<div class="sktop">' +
        '<section class="panel"><h2><span class="num">1</span>Arrangement</h2><div class="skrow">' +
          '<label class="lbl" for="sktype">Preset</label><select id="sktype">' + opt(d.types, S.type) + '</select>' +
          '<p class="sknote">' + esc(d.types[S.type].note) + '</p></div></section>' +
        '<section class="panel"><h2><span class="num">2</span>Section effects</h2><div class="skrow" id="skfx">' +
          '<button class="btn' + (S.fx === 'built_in' ? ' on' : '') + '" data-fx="built_in">Built in</button>' +
          '<label class="lbl" for="skgenre">Genre</label><select id="skgenre"><option value="">&mdash;</option>' +
            opt(d.genres, genre) + '</select>' +
          '<button class="btn' + (S.fx === 'random' ? ' on' : '') + '" data-fx="random">&#9861; Random</button>' +
          '<button class="btn" id="skroll">&#8635; Re-roll</button></div>' +
          '<p class="sknote">' + fxNote(d) + '</p></section>' +
      '</div>' +
      '<div class="skmid">' +
        '<section class="panel lgridwrap" aria-label="Arrangement grid"><div class="skgridhead"><b>' + plan.length +
          ' sections</b> &middot; <span id="sklen"></span></div>' + gridHtml(d, plan) +
          '<p class="sknote">The DJ&rsquo;s producer tag is left out so it isn&rsquo;t repeated every section.</p></section>' +
        '<aside class="panel skside" id="skside"></aside>' +
      '</div>' +
      '<div class="panel skfoot">' +
        '<span class="sknote">Click a cell to edit this section.</span>' +
        '<label class="amt" for="skamt">Echo / reverb amount <input type="range" id="skamt" min="0" max="1" step="0.05" value="' +
          (S.amt != null ? S.amt : 0.6) + '"> <output id="skamtv"></output></label>' +
        '<span class="skstatus" id="skstatus" role="status"></span>' +
        '<button class="btn lead big" id="skgo">Make the sketch</button></div>' +
      '<div id="skresult"></div>';
    const redraw = change => { S.amt = +box.querySelector('#skamt').value; change(); S.cell = null; draw(); };
    box.querySelector('#skback').onclick = close;
    box.querySelector('#sktype').onchange = e => redraw(() => { S.type = e.target.value; S.roll = 0; });
    box.querySelectorAll('#skfx button[data-fx]').forEach(b => b.onclick = () => redraw(() => {
      S.fx = b.dataset.fx;
      S.roll = S.fx === 'random' ? Math.floor(Math.random() * plans().length) : 0;
    }));
    box.querySelector('#skgenre').onchange = e => redraw(() => { S.fx = e.target.value || 'built_in'; S.roll = 0; });
    box.querySelector('#skroll').onclick = () => redraw(() => { S.roll = (S.roll + 1) % plans().length; });
    box.querySelectorAll('.gc').forEach(c => c.onclick = () => {
      S.cell = { l: c.dataset.l, i: c.dataset.i }; paintSide();
    });
    const amt = box.querySelector('#skamt'), amtv = box.querySelector('#skamtv');
    const showAmt = () => amtv.textContent = Math.round(amt.value * 100) + '%';
    amt.oninput = showAmt; showAmt();
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
      box.querySelector('#skstatus').innerHTML = ok ? '<i class="okdot"></i>Ready to build' : '';
    };
    box.querySelectorAll('.rl, .sc').forEach(el => el.addEventListener('change', dim));
    box.querySelectorAll('.sc').forEach(s => s.addEventListener('change', note));
    box.querySelectorAll('.bars').forEach(s => s.addEventListener('change', len));
    dim(); note(); len(); paintSide();
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
      S.result = d; S.which = 'sketch'; st.textContent = 'Built.';
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
    const art = document.querySelector('.track[data-no="' + S.no + '"] .art');
    host.innerHTML = '<div class="panel sklisten">' +
      '<span class="' + (art ? art.className : 'art c0') + '" aria-hidden="true"><b>' + esc(S.no) + '</b></span>' +
      '<span class="skwho"><b>Listen</b><small>Beat ' + esc(S.no) + '</small><small id="sktime">0:00</small></span>' +
      '<button class="skpp" id="skpp" aria-label="Play">&#9654;</button>' +
      '<span class="seg" role="group" aria-label="Which version">' +
        '<button type="button" data-w="sketch">Sketch</button><button type="button" data-w="original">Plain loop</button></span>' +
      '<span class="skbarwrap"><span class="skbar" id="skbar"></span>' +
        '<input type="range" class="skseek" id="skseek" min="0" max="1000" value="0" aria-label="Position"></span>' +
      '<a class="btn" href="' + url('stems-and-mix.zip') + '" download>&#8615; Download stems + mix</a>' +
      '</div>' +
      '<p class="sknote">A/B keeps your place and plays at the same level. ' + esc(m.gain_db) +
        ' dB overall to stay under clipping. Saved in Homeroom Auditions &rsaquo; Song Sketches &rsaquo; ' + esc(S.result.id) + '</p>' +
      (m.warnings.length ? '<p class="skwarn">' + m.warnings.map(esc).join('<br>') + '</p>' : '');
    au = new Audio(); au.preload = 'auto'; au.src = url(S.which === 'sketch' ? 'sketch.wav' : 'original.wav');
    const pp = host.querySelector('#skpp'), seek = host.querySelector('#skseek'),
          time = host.querySelector('#sktime'), bar = host.querySelector('#skbar');
    const names = S.d.scenes;
    bar.innerHTML = m.sections.map((s, i) => '<button type="button" class="s' + (i % 4) + '" data-t="' + s.start_s + '" style="flex:' +
      (s.end_s - s.start_s) + '" title="' + esc(names[s.scene].name) + ' at ' + clock(s.start_s) + '"><b></b>' +
      (i + 1) + '. ' + esc(names[s.scene].name) + '</button>').join('');
    bar.querySelectorAll('button').forEach(b => b.onclick = () => { au.currentTime = +b.dataset.t; });
    const seg = host.querySelectorAll('.seg button');
    const label = () => seg.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.w === S.which)));
    label();
    pp.onclick = () => { if (au.paused) { stopOthers(); au.play().catch(() => {}); } else au.pause(); };
    seg.forEach(b => b.onclick = () => {
      if (b.dataset.w === S.which) return;
      const t = au.currentTime, was = !au.paused;
      S.which = b.dataset.w;
      au.src = url(S.which === 'sketch' ? 'sketch.wav' : 'original.wav');
      au.addEventListener('loadedmetadata', function f() {
        au.removeEventListener('loadedmetadata', f);
        au.currentTime = Math.min(t, au.duration || t);
        if (was) au.play().catch(() => {});
      });
      label();
    });
    au.onplay = () => { pp.innerHTML = '&#10073;&#10073;'; pp.setAttribute('aria-label', 'Pause'); pp.classList.add('on'); };
    au.onpause = au.onended = () => { pp.innerHTML = '&#9654;'; pp.setAttribute('aria-label', 'Play'); pp.classList.remove('on'); };
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
