# Chapter 02: Effects and signal processing
## Part 9 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- 2026-08-08-sound-engine-mixer.md (piece 7 of 8) — Sound Engine Multi-Stem Mixer Implementation Plan

(Next: Part 10 of 10)


=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer.md (piece 7 of 8)
ORIGINAL LOCATION: HS:docs/superpowers/plans/2026-08-08-sound-engine-mixer.md
=====================================================

### Task 8: Deepen Compressor — real makeup gain

**Files:**
- Modify: `sound_engine/static/index.html`
- Modify: `sound_engine/static/app.js`
- Modify: `sound_engine/server.py`
- Modify: `tests/test_sound_engine.py`

**Interfaces:**
- Consumes: `glue_compressor(..., makeup_db=...)` (already exists).

- [ ] **Step 1: Write the failing test**

```python
def test_compressor_makeup_gain_reaches_export():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"comp_ratio": 4.0, "comp_makeup_db": 0.0})
    quiet = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"comp_ratio": 4.0, "comp_makeup_db": 12.0})
    loud = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert np.abs(loud[0]).max() > np.abs(quiet[0]).max()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_compressor_makeup_gain_reaches_export -v`
Expected: FAIL

- [ ] **Step 3: Wire `comp_makeup_db` through `_apply_channel_chain` in `server.py`**

```python
    comp_makeup_db = float(p.get("comp_makeup_db", 0.0))
    ...
    if comp_ratio > 1.0:
        L, R = ae.glue_compressor(L, R, sr=sr, threshold_db=comp_threshold_db,
                                    ratio=comp_ratio, attack_ms=comp_attack_ms,
                                    release_ms=comp_release_ms, makeup_db=comp_makeup_db)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_compressor_makeup_gain_reaches_export -v`
Expected: PASS

- [ ] **Step 5: Add a Makeup Gain slider to the Compressor panel in `index.html`**

Add inside the Compressor `.knobs` div (Task 4):

```html
              <div class="knob">
                <label for="compMakeup">Makeup <span id="compMakeupVal">0</span> dB</label>
                <input type="range" id="compMakeup" min="0" max="24" step="0.5" value="0">
              </div>
```

- [ ] **Step 6: Wire it live in `app.js`**

Live side needs a real gain stage — the Web Audio `DynamicsCompressorNode`
has no makeup-gain concept, matching why `server.py`'s export needed a
separate `pb.Gain` stage too (see `glue_compressor`'s pedalboard chain).
Add a `makeupGain` node per channel in `buildChannelGraph()` (Task 5,
Step 2): insert `const makeupGain = audioCtx.createGain(); makeupGain.gain.value = 1;`
next to the `compressor` node, splice it into the chain
(`compressor.connect(makeupGain)` then change `compressor.connect(satDry)`
/ `compressor.connect(satWet)` to `makeupGain.connect(satDry)` /
`makeupGain.connect(satWet)`), and add `makeupGain` to the returned
channel object.

```javascript
bindRamped("compMakeup", ch => ch.makeupGain, "gain", db => 10 ** (db / 20));
```

Add to `loadRackFromChannel()`:
```javascript
  const makeupDb = 20 * Math.log10(ch.makeupGain.gain.value);
  document.getElementById("compMakeup").value = makeupDb;
  document.getElementById("compMakeupVal").textContent = makeupDb.toFixed(1);
```

Add to `syncChannelToServer()`'s `params`:
```javascript
    comp_makeup_db: 20 * Math.log10(ch.makeupGain.gain.value),
```

- [ ] **Step 7: Run tests, then manually re-verify in browser**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py tests/test_sound_engine_library.py -v`
Expected: all pass. In the browser, confirm turning Makeup up while
audio plays audibly raises the level.

- [ ] **Step 8: Commit**

```bash
git add sound_engine/static/index.html sound_engine/static/app.js sound_engine/server.py tests/test_sound_engine.py
git commit -m "Deepen Compressor panel: add real makeup gain"
```

---

### Task 9: Deepen Reverb — independent wet/dry, damping, width, freeze

**Files:**
- Modify: `sound_engine/static/index.html`
- Modify: `sound_engine/static/app.js`
- Modify: `sound_engine/server.py`
- Modify: `tools/audio_engine.py` (one-line addition — `loop_algo_reverb` needs a `freeze` passthrough, it currently doesn't accept one; `algo_reverb` already does)
- Modify: `tests/test_sound_engine.py`
- Modify: `tests/test_audio_engine.py` (regression test for the new `freeze` passthrough)

**Interfaces:**
- Consumes: `algo_reverb(..., width, freeze, ...)` (exists),
  `loop_algo_reverb` (exists, gains a new `freeze` kwarg this task).

This is the biggest depth win — Reverb goes from 2 knobs to 6. Do it in
two passes: wet/dry decoupling first (smallest, proves the pattern),
then damping/width/freeze together (all three touch the same live-side
reverb send path).

- [ ] **Step 1: Write the failing test for independent wet/dry**

```python
def test_reverb_wet_and_dry_are_independent():
    project_id = _upload().json()["project_id"]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.4, "reverb_dry": 1.0})
    both = [a.copy() for a in server.PROJECTS[project_id]["channels"]["upload"]["wet"]]
    client.post(f"/api/project/{project_id}/channel/upload/process",
                json={"reverb_mix": 0.4, "reverb_dry": 0.0})
    wet_only = server.PROJECTS[project_id]["channels"]["upload"]["wet"]
    assert not np.array_equal(both[0], wet_only[0])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py::test_reverb_wet_and_dry_are_independent -v`
Expected: FAIL (today `dry` is always computed as `1 - reverb_mix`, never read from the body)

- [ ] **Step 3: Decouple wet/dry in `_apply_channel_chain`**

```python
    reverb_size_s = float(p.get("reverb_size_s", 2.0))
    reverb_mix = float(p.get("reverb_mix", 0.0))
    reverb_dry = float(p.get("reverb_dry", 1.0 - reverb_mix))
    reverb_damping = float(p.get("reverb_damping", 0.5))
    reverb_width = float(p.get("reverb_width", 1.0))
    reverb_freeze = bool(p.get("reverb_freeze", False))
    ...
    if reverb_mix > 0.0 or reverb_freeze:
        room_size = min(1.0, reverb_size_s / 6.0)
        L, R = ae.loop_algo_reverb(L, R, sr=sr, room_size=room_size,
                                     damping=reverb_damping, wet=reverb_mix,
                                     dry=reverb_dry, width=reverb_width,
                                     freeze=reverb_freeze)
```

- [ ] **Step 4: Add `freeze` passthrough to `loop_algo_reverb` in `tools/audio_engine.py`**

```python
def loop_algo_reverb(L, R, room_size=0.5, damping=0.5, wet=0.25, dry=1.0,
                       width=1.0, freeze=False, sr=None):
    """Loop-safe algorithmic reverb. ...(existing docstring unchanged)..."""
    n = len(L)
    dblL, dblR = algo_reverb(np.concatenate([L, L]), np.concatenate([R, R]),
                               room_size=room_size, damping=damping, wet=wet,
                               dry=dry, width=width, freeze=freeze, sr=sr)
    return dblL[n:], dblR[n:]
```

(Only the signature and the one new `freeze=freeze` kwarg passed through
to `algo_reverb` change — everything else in this function is unchanged.)

- [ ] **Step 5: Add the regression test to `tests/test_audio_engine.py`**

```python
def test_loop_algo_reverb_freeze_passthrough_sustains_longer():
    sr = 44100
    n = sr  # 1s
    L = np.zeros(n); L[0] = 1.0
    R = L.copy()
    normal_L, _ = loop_algo_reverb(L, R, room_size=0.5, wet=1.0, dry=0.0, sr=sr)
    frozen_L, _ = loop_algo_reverb(L, R, room_size=0.5, wet=1.0, dry=0.0,
                                     freeze=True, sr=sr)
    # freeze mode should not decay to silence by the end of the buffer
    # the way a normal room_size=0.5 tail does
    assert np.abs(frozen_L[-100:]).mean() > np.abs(normal_L[-100:]).mean()
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `.venv/bin/python -m pytest tests/test_audio_engine.py tests/test_sound_engine.py -v`
Expected: all pass.

- [ ] **Step 7: Add damping/width/freeze to the Reverb panel in `index.html`**

Replace the Reverb `.panel` block (Task 4) with:

```html
          <div class="panel">
            <h2>Reverb</h2>
            <div class="knobs">
              <div class="knob">
                <label for="revSize">Size <span id="revSizeVal">2.0</span> s</label>
                <input type="range" id="revSize" min="0.2" max="6" step="0.1" value="2.0">
              </div>
              <div class="knob">
                <label for="revDamping">Damping <span id="revDampingVal">0.5</span></label>
                <input type="range" id="revDamping" min="0" max="1" step="0.05" value="0.5">
                <span class="freq">0 = dark, 1 = bright</span>
              </div>
              <div class="knob">
                <label for="revWidth">Width <span id="revWidthVal">1.0</span>x</label>
                <input type="range" id="revWidth" min="0" max="2" step="0.05" value="1.0">
              </div>
              <div class="knob">
                <label for="revWet">Wet <span id="revWetVal">0</span>%</label>
                <input type="range" id="revWet" min="0" max="100" step="1" value="0">
              </div>
              <div class="knob">
                <label for="revDry">Dry <span id="revDryVal">100</span>%</label>
                <input type="range" id="revDry" min="0" max="100" step="1" value="100">
              </div>
              <div class="knob">
                <label class="loopToggle"><input type="checkbox" id="revFreeze"> Freeze (infinite sustain)</label>
              </div>
            </div>
          </div>
```

(This removes the old single `revMix` slider entirely, replaced by
separate `revWet`/`revDry` — update every reference to `revMix` across
`app.js` accordingly in the next step, including the `bindRamped("revMix", ...)`
call and the `document.getElementById("revMix")` dry-coupling listener
added in Task 5, both now dead code to remove.)

- [ ] **Step 8: Wire damping/width/freeze/wet/dry live in `app.js`**

Live-side approximations (documented in the design spec): damping = a
lowpass filter on the wet path only; width = the same M/S gain-scaling
pattern already used for the channel's own Stereo Width effect, applied
to the reverb wet signal; freeze = swap in a non-decaying impulse
response instead of the normal exponentially-decaying one.

In `buildChannelGraph()` (Task 5, Step 2), replace the reverb section:

```javascript
  const revDry = audioCtx.createGain(); revDry.gain.value = 1;
  const revWet = audioCtx.createGain(); revWet.gain.value = 0;
  const revDamp = audioCtx.createBiquadFilter();
  revDamp.type = "lowpass"; revDamp.frequency.value = 18000;
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

  // merger (M/S width control, unchanged from before) feeds dry AND the
  // damping+width-processed wet path
  merger.connect(revDry).connect(revOut);
  merger.connect(revWet).connect(convolver).connect(revDamp)
        .connect(revSplitter);
  revMerger.connect(revOut);
```

(This replaces the simpler `merger.connect(revWet).connect(convolver).connect(revOut)`
line from Task 5's `buildChannelGraph` with the damping filter + a SECOND
M/S width stage scoped to the reverb tail only — distinct from the
channel's own `splitter`/`sideWidth`, which controls the whole channel's
width, not just the reverb send.)

Update `makeReverbIR` to support freeze:

```javascript
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
```

Add the new channel-object fields (`revDamp`, `revSideWidth`, `freeze`
state) to `buildChannelGraph()`'s return object, then bind:

```javascript
bindRamped("revDamping", ch => ch.revDamp, "frequency", d => 200 + d * 17800);
bindRamped("revWidth", ch => ch.revSideWidth, "gain");
document.getElementById("revWet").addEventListener("input", e => {
  document.getElementById("revWetVal").textContent = e.target.value;
  const ch = currentChannel(); if (!ch) return;
  ch.revWet.gain.setTargetAtTime(parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
});
document.getElementById("revDry").addEventListener("input", e => {
  document.getElementById("revDryVal").textContent = e.target.value;
  const ch = currentChannel(); if (!ch) return;
  ch.revDry.gain.setTargetAtTime(parseFloat(e.target.value) / 100,
                                  audioCtx.currentTime, RAMP_SECONDS);
});
document.getElementById("revFreeze").addEventListener("change", e => {
  const ch = currentChannel(); if (!ch) return;
  ch.freeze = e.target.checked;
  ch.convolver.buffer = makeReverbIR(audioCtx, parseFloat(document.getElementById("revSize").value), ch.freeze);
});
```

Update the existing `revSize` `input`/`change` listeners (Task 5, Step 4)
to pass `ch.freeze` as the new third argument to `makeReverbIR(...)`.

Update `loadRackFromChannel()` — replace the old `revMix` lines with:
```javascript
  document.getElementById("revDamping").value = (ch.revDamp.frequency.value - 200) / 17800;
  document.getElementById("revDampingVal").textContent = ((ch.revDamp.frequency.value - 200) / 17800).toFixed(2);
  document.getElementById("revWidth").value = ch.revSideWidth.gain.value;
  document.getElementById("revWidthVal").textContent = ch.revSideWidth.gain.value.toFixed(2);
  document.getElementById("revWet").value = Math.round(ch.revWet.gain.value * 100);
  document.getElementById("revWetVal").textContent = Math.round(ch.revWet.gain.value * 100);
  document.getElementById("revDry").value = Math.round(ch.revDry.gain.value * 100);
  document.getElementById("revDryVal").textContent = Math.round(ch.revDry.gain.value * 100);
  document.getElementById("revFreeze").checked = !!ch.freeze;
```

Update `syncChannelToServer()`'s `params` — replace `reverb_mix:
ch.revWet.gain.value` with:
```javascript
    reverb_mix: ch.revWet.gain.value, reverb_dry: ch.revDry.gain.value,
    reverb_damping: (ch.revDamp.frequency.value - 200) / 17800,
    reverb_width: ch.revSideWidth.gain.value, reverb_freeze: !!ch.freeze,
```

- [ ] **Step 9: Run tests, then manually re-verify all 6 reverb knobs live in the browser**

Run: `.venv/bin/python -m pytest tests/test_sound_engine.py tests/test_sound_engine_library.py tests/test_audio_engine.py -v`
Expected: all pass. In the browser: confirm Wet and Dry move independently;
confirm Damping audibly darkens/brightens the tail while playing; confirm
Freeze sustains indefinitely instead of decaying; confirm turning Freeze
off restores normal decay at the current Size.

- [ ] **Step 10: Commit**

```bash
git add sound_engine/static/index.html sound_engine/static/app.js sound_engine/server.py tools/audio_engine.py tests/test_sound_engine.py tests/test_audio_engine.py
git commit -m "Deepen Reverb panel: independent wet/dry, damping, width, freeze"
```

---


=== END OF PART ===
