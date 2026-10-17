# Chapter 02: Effects and signal processing
## Part 6 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- 2026-08-08-sound-engine-mixer.md (piece 4 of 8) — Sound Engine Multi-Stem Mixer Implementation Plan

(Next: Part 7 of 10)


=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer.md (piece 4 of 8)
ORIGINAL LOCATION: HS:docs/superpowers/plans/2026-08-08-sound-engine-mixer.md
=====================================================

### Task 4: `index.html` + `style.css` — channel list, beat picker, detail-rack shell

**Files:**
- Modify: `sound_engine/static/index.html`
- Modify: `sound_engine/static/style.css`

**Interfaces:**
- Produces: DOM elements Task 5's `app.js` binds to —
  `#browseBeatsBtn`, `#beatPickerModal` (with `#beatPickerList`,
  `#beatPickerClose`), `#channelList` (empty `<div>`, populated by JS),
  `#channelRackTitle`, `#channelRack` (holds the same EQ/Comp/Sat/Width/
  Reverb `.panel` markup as today, once, reused for whichever channel is
  selected — NOT duplicated per channel).

- [ ] **Step 1: Add the beat picker + channel list markup**

In `index.html`, replace the single `<section id="dropzone">` /
`<section id="workspace">` pair with:

```html
    <section id="dropzone" class="dropzone">
      <p>Drop an audio file here, or</p>
      <label class="btn">
        Choose a file
        <input type="file" id="fileInput" accept="audio/*" hidden>
      </label>
      <button id="browseBeatsBtn" class="btn">Browse your beats</button>
      <p class="hint">WAV, MP3, M4A, AIFF, FLAC — most audio formats work.</p>
    </section>

    <div id="beatPickerModal" class="modal hidden">
      <div class="modal-card">
        <div class="modal-header">
          <h2>Pick a beat</h2>
          <button id="beatPickerClose" class="btn">Close</button>
        </div>
        <p id="beatPickerWarning" class="meta hidden"></p>
        <div id="beatPickerList" class="beatList"></div>
      </div>
    </div>

    <section id="workspace" class="workspace hidden">
      <div class="filebar">
        <span id="fileName">—</span>
        <span id="fileMeta" class="meta"></span>
      </div>

      <div class="transport">
        <button id="playBtn" class="btn primary">▶ Play</button>
        <button id="stopBtn" class="btn">■ Stop</button>
        <label class="loopToggle">
          <input type="checkbox" id="loopToggle"> Loop
        </label>
        <label class="loopToggle">
          <input type="checkbox" id="bypassToggle"> Bypass (A/B)
        </label>
        <span id="playStatus" class="meta"></span>
      </div>

      <div class="mixer">
        <div id="channelList" class="channelList"></div>

        <div class="channelRack">
          <h2 id="channelRackTitle">—</h2>

          <div class="panel">
            <h2>EQ — live, moves while it plays</h2>
            <div class="knobs">
              <div class="knob">
                <label for="lowDb">Low <span id="lowDbVal">0.0</span> dB</label>
                <input type="range" id="lowDb" min="-18" max="18" step="0.5" value="0">
                <span class="freq">@ 120 Hz shelf</span>
              </div>
              <div class="knob">
                <label for="midDb">Mid <span id="midDbVal">0.0</span> dB</label>
                <input type="range" id="midDb" min="-18" max="18" step="0.5" value="0">
                <span class="freq">@ 800 Hz bell</span>
              </div>
              <div class="knob">
                <label for="highDb">High <span id="highDbVal">0.0</span> dB</label>
                <input type="range" id="highDb" min="-18" max="18" step="0.5" value="0">
                <span class="freq">@ 8 kHz shelf</span>
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Compressor</h2>
            <div class="knobs">
              <div class="knob">
                <label for="compThreshold">Threshold <span id="compThresholdVal">-24</span> dB</label>
                <input type="range" id="compThreshold" min="-60" max="0" step="1" value="-24">
              </div>
              <div class="knob">
                <label for="compRatio">Ratio <span id="compRatioVal">1.0</span>:1</label>
                <input type="range" id="compRatio" min="1" max="20" step="0.5" value="1">
                <span class="freq">1 = off</span>
              </div>
              <div class="knob">
                <label for="compAttack">Attack <span id="compAttackVal">12</span> ms</label>
                <input type="range" id="compAttack" min="1" max="200" step="1" value="12">
              </div>
              <div class="knob">
                <label for="compRelease">Release <span id="compReleaseVal">180</span> ms</label>
                <input type="range" id="compRelease" min="20" max="1000" step="10" value="180">
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Saturation</h2>
            <div class="knobs">
              <div class="knob">
                <label for="satDrive">Drive <span id="satDriveVal">6</span> dB</label>
                <input type="range" id="satDrive" min="0" max="24" step="0.5" value="6">
              </div>
              <div class="knob">
                <label for="satMix">Mix <span id="satMixVal">0</span>%</label>
                <input type="range" id="satMix" min="0" max="100" step="1" value="0">
                <span class="freq">0 = off</span>
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Reverb</h2>
            <div class="knobs">
              <div class="knob">
                <label for="revSize">Size <span id="revSizeVal">2.0</span> s</label>
                <input type="range" id="revSize" min="0.2" max="6" step="0.1" value="2.0">
              </div>
              <div class="knob">
                <label for="revMix">Mix <span id="revMixVal">0</span>%</label>
                <input type="range" id="revMix" min="0" max="100" step="1" value="0">
                <span class="freq">0 = off</span>
              </div>
            </div>
          </div>

          <div class="panel">
            <h2>Stereo Width</h2>
            <div class="knobs">
              <div class="knob">
                <label for="widthKnob">Width <span id="widthKnobVal">1.0</span>x</label>
                <input type="range" id="widthKnob" min="0" max="2" step="0.05" value="1.0">
                <span class="freq">0 = mono, 1 = unchanged, 2 = wide</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="exportbar">
        <button id="exportBtn" class="btn primary">Export mix as new file</button>
        <span id="exportStatus" class="meta"></span>
      </div>
    </section>
```

(This step keeps today's EQ/Comp/Sat/Width/Reverb panel markup verbatim
except renaming the Reverb `<h2>` context and export button label —
Phase 3, Tasks 10-12, add the new sliders into these same panels. Don't
add them here; this task is purely the mixer shell.)

- [ ] **Step 2: Add channel-list, modal, and mixer-layout CSS**

Append to `style.css`:

```css
main { max-width: 900px; }

.modal {
  position: fixed; inset: 0;
  background: rgba(10, 12, 16, 0.7);
  display: flex; align-items: center; justify-content: center;
  z-index: 10;
}
.modal-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  width: min(520px, 90vw);
  max-height: 80vh;
  overflow-y: auto;
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px;
}
.beatList { display: flex; flex-direction: column; gap: 6px; }
.beatItem {
  display: flex; justify-content: space-between; align-items: baseline;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
}
.beatItem:hover { border-color: var(--accent); }
.beatItem .meta { font-size: 12px; }

.mixer { display: flex; gap: 20px; align-items: flex-start; }
.channelList {
  flex: 0 0 220px;
  display: flex; flex-direction: column; gap: 6px;
}
.channelStrip {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  cursor: pointer;
}
.channelStrip.selected { border-color: var(--accent); }
.channelStrip .label {
  font-size: 13px; font-weight: 600;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  margin-bottom: 6px;
}
.channelStrip .row { display: flex; align-items: center; gap: 8px; }
.channelStrip input[type=range] { flex: 1; accent-color: var(--accent); }
.channelStrip .mutesolo { display: flex; gap: 4px; margin-top: 6px; }
.channelStrip .mutesolo button {
  flex: 1; font-size: 11px; padding: 4px;
  background: var(--bg); border: 1px solid var(--border); color: var(--muted);
  border-radius: 6px; cursor: pointer;
}
.channelStrip .mutesolo button.active.mute { background: #a33; color: #fff; border-color: #a33; }
.channelStrip .mutesolo button.active.solo { background: var(--accent); color: #0a0e14; border-color: var(--accent); }

.channelRack { flex: 1; min-width: 0; }
.channelRack > h2 { margin: 0 0 12px; font-size: 18px; }
```

- [ ] **Step 3: Commit**

```bash
git add sound_engine/static/index.html sound_engine/static/style.css
git commit -m "Add mixer shell markup: beat picker modal, channel list, shared effects rack"
```

(No automated test for this step — it's static markup with no behavior
yet. Task 5 wires it up and gets browser-verified.)

---


=== END OF PART ===
