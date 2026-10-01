# Combinator — what the existing guide does NOT cover
Source: Reason 12.7 Operation Manual, ch. 63 (pp. 1305–1332). Tag: **Manual** unless marked.
Basics (Rotary 1–16, Bypass All FX, External Routing rule, Combine/Uncombine) are already in
`device_refs/combinator.md`. This file holds only the extra detail, so nothing is stored twice.

## 1. Split and layer (key + velocity zones)
- Each instrument inside has a **Key** checkbox and a **Key Range** bar. Default = whole keyboard.
- Same key range = layered (plays together). Different ranges = split.
- Ranges may overlap: the overlap zone is layered.
- **Transpose** (far right of the Combi panel): ±36 semitones (±3 octaves). Moves the pitch only, NOT the key mapping.
- **Velocity ranges** (1–127) work on top of key ranges: soft = device A, hard = device B.
- Overlap trick: Dev 1 = 1–45, Dev 2 = 33–88, Dev 3 = 76–127. Velocities 33–45 trigger BOTH 1 and 2 — a crossfade between layers.
- Uses: pad underneath a piano only on hard hits; bass below a split point, lead above it; soft = mellow, hard = bright sample.

## 2. Note on/off per device (a switch for layers)
- In Modulation Routing the **Target** list ends with an option to receive note data or not.
- Map a Combi **Button** to it and one click mutes/unmutes a layer's notes. Gives a "layer 2 on/off" button without touching the sequencer.

## 3. Modulation Routing — the four columns
Source | Target | Min | Max. Source can be a Rotary, Button, a **CV input**, or a **performance controller** (mod wheel, pitch bend, etc.).
- Pick a device on the left of the Editor; Target list = that device's parameters.
- **Min > Max** (drag handles past each other) = reversed: knob up, target down.
- **Source Range** (e.g. 50–100 %): the knob only acts in that part of its travel. Below it, the target stays put.
- Worked example from the manual (one FILTER knob on a Europa):
  - Filter Freq: normal range, rises as the knob goes up.
  - Filter Reso: range reduced AND reversed, Source Range 0–50 %. Resonance falls during the first half of the knob, then stays.
  - Result: one knob opens the filter and calms the resonance. A "macro".
- One knob → many targets, on one device or across devices (e.g. one "master cutoff" for two Subtractors and a Malström).
- One target ← many knobs: pick the same Target from different Sources.
- **Clear Mappings** (the X button) wipes all mappings for a clean start.

## 4. Panel design (look only — does not change sound)
- Size 1U–6U. Background colour or backdrop image.
- Backdrop image width for full hi-res = **3770 px**. Heights: 345 / 690 / 1035 / 1380 / 1725 / 2070 px for 1U–6U.
- Up to 32 knobs/faders + 32 buttons + the 2 wheels + Run + Bypass FX.
- Factory Sound Bank › Combinator Patches › **Combi Layout Templates**: ready-made panel layouts to start from.

## 5. Rear-panel CV
CV connections **inside** the Combi and from inside to the Combi's own CV jacks ARE saved with the patch (unlike cables to outside devices).
| Jack | Does |
|---|---|
| Sequencer Control CV + Gate | Play the whole Combi from a Matrix or RPG-8. CV = pitch, Gate = note on/off + velocity |
| Control CV In (4) | Each can drive any chosen front-panel control; attenuator knob each |
| Wheel CV In | Pitch bend / mod wheel by CV |
| Source CV In (8) | Extra Sources for Modulation Routing. Click **Editor** to see them |
- Each Source CV In has a **sensitivity** knob (turn it down) and a **polarity** switch.
  - **Unipolar** for envelopes. **Bipolar** for LFOs. Wrong setting = modulation sits off-centre.

## 6. Ideas for the project (**Guess**, not tested)
- Recipe chains that are "device + effects + one macro knob" are good Combi candidates. The voice bridge can't see Combi knobs yet (only patch next/prev), but Rotary moves record as automation.
- A "Layer on/off" Button (section 2) is a cheap way to build live-performance patches.
