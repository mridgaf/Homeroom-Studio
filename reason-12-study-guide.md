# Reason 12 Study Guide
*Compiled from existing project knowledge (2026-10-09)*

---

## What Reason 12 Is

Reason 12 is a **rack-based DAW** (Digital Audio Workstation) by Propellerhead. Think of it as a virtual version of a physical signal chain: you build a "rack" of audio devices, patch cables between them, and send MIDI to control those devices.

**Core workflow:**
1. Load a song project (`.pres`)
2. Build a rack: insert devices (instruments, effects, mixers)
3. Patch cables: route audio/CV between device jacks
4. Load patches: each device type has factory patches (compressor settings, synth tones, drum kits)
5. Control via MIDI: control surfaces map physical knobs to specific device parameters

---

## The Three Ways Into Reason

*From `references/lessons/01-what-reason-allows-from-outside.md`*

1. **Remote** (official): MIDI CCs to control remotable parameters. Limited to what factory control surfaces mapped.
2. **Combinator** (advanced): `.cmb` files that save entire rigs — devices, settings, AND cable routing.
3. **Manual**: drag-and-drop, no automation.

---

## Device Types & Their Roles

### Instruments
Generate audio from MIDI or samples:
- **Redrum/Dr. Octo Rex**: drum machines (grid-based sequencing)
- **NN-XT/NN19**: samplers (NN-XT = multi-sampling, NN19 = one-shot)
- **Subtractor/Thor/Malstrom**: synthesizers (analog-style, subtractive)
- **Mimic**: acoustic guitar
- **Kong**: supersampler (many samples per key)
- **Combinator**: container device holding a mini-rack

### Effects
Process audio:
- **Scream 4**: distortion/overdrive
- **RV7000 MKII**: reverb (convolution)
- **MClass Compressor**: dynamics (Softube modeled)
- **Channel EQ/Channel Dynamics**: parametric EQ, dynamics per band
- **EQ3/Pulsar**: multi-band EQ
- **DDL1**: saturation
- **Echo Delays**: delay/echo
- **Neptune**: pitch-shifted delay

### Mixers
- **Mixer 14-2**: 14-channel mixer with FX sends
- **Master Bus Compressor**: final limiting
- **Samson Servo 300**: power amp simulation

---

## The Remote Protocol

*From `reason_control.py` and `reason-reference` skill*

Remote is Reason's MIDI control protocol. Each **device TYPE** (not instance) exposes a fixed list of "remotable" parameters.

**How it works:**
1. App sends MIDI CC on IAC Bus 1
2. Custom codec (Lua) converts CC to named surface item
3. `.remotemap` binds item to specific device parameter
4. Reason applies change to **locked device** (Ctrl/right-click → "Lock to Surface")

**48 Knobs:** CCs 30-77 map to knob_1 through knob_48
**Feedback:** CCs 77+ report knob positions as SysEx

**Critical rule:** Parameter names must come from `remote-vocab.json` — off-by-one errors fail silently.

---

## Patch Loading

*From `reason_control.py`*

Reason has **no API** to build device chains or route cables. The only programmatic entry:

```bash
open -a Reason <patchfile>
```

This creates a device with that patch loaded in the rack of the open song. Patches are saved settings snapshots — they **do not** carry cable/routing info (except Combinator `.cmb` files).

---

## Recipe System (The Project's Knowledge Base)

*From `recipes.py`*

The project maintains a recipe library in `recipes/**/*.md`:

**Frontmatter (YAML):**
```yaml
name: "G-Funk Lead"
book: "hip-hop"
accuracy: "C"  # A-D honesty rating
status: "tested"  # tested | theoretical
technique: "portamento saw lead"
sounds_like: "Quik/E-Soul"
```

**Body Sections:**
- `## The Chain`: device chain description
- `## Steps`: numbered walkthrough
- `## Why this works`: technique explanation
- `## Order of operations`: setup sequence
- `## Reason-specific trick`: DAW tip
- `## RE upgrade path`: future-proofing
- `## Technique you just learned`: transferable skill
- `## Reference`: device/technique source

---

## 12 Legends (Producer Identities)

*From `HARMONY-IDENTITY-PROPOSAL.md`*

Each legend has a harmonic fingerprint: tempo range, mode, progressions, chord_source lean.

| Legend | Tempo | Mode | Chord Source |
|--------|-------|------|--------------|
| J Dillo (Dilla) | 70-95 | minor+major | loop (Rhodes/soul) |
| DJ Premium (Premier) | 82-96 | minor/dorian | loop (dark stab) + scratch |
| Doc Day (Dre) | 85-100 | minor | strings + synth |
| Timberline (Timbaland) | 90-100/135-145 | phrygian | drone |
| Memphis (Three 6) | 140 | minor/phrygian | synth/horror-organ |
| G-Funk | 85-105 | dorian | synth-lead + loop |
| Miami Bass | 118-140 | minor pentatonic | 808 riff |
| Reggaeton Alt | 85-100 | minor/phrygian | synth stab |
| Farrow (Pharrell) | 95-115 | near-atonal → major | synth |
| Kane East (Kanye) | 83-97/85-145 | major/minor | loop/strings |
| Razor (RZA) | 80-96 | minor | loop (90%+ reused) |
| No I.D. | 85-96 | major/minor | loop |

**Plus 3 more:** Swish Beatz (synth stab), Just Flame (horn/brass), Hitt Kid (club/trap era pivot).

---

## Device Reference Files

*From `device_refs/` directory*

66 device guides covering:
- ReFills devices (MClass, Kong, Redrum, NN-XT, NN19)
- Combinator setups
- Stock devices (Subtractor, Thor, EQ, dynamics)
- Third-party (Softube, Yamaha, Samson)

Each file: plain-language device guide with parameter descriptions.

---

## Signal Flow & Routing

*From `references/study-notes/16-routing-audio-and-cv.md`*

**Cables:** drag between jacks OR pop-up menu. Colors indicate signal type (audio, CV, MIDI).

**Auto-routing:** Reason can auto-connect MIDI to devices that need it.

**CV Trim:** adjusts voltage scaling for CV signals.

**P-LAN / Direct Out:** alternative routing paths.

**Flipping rack:** mirror view horizontally.

---

## Automation & Recording

*From `references/lessons/04-recording-and-sweeps.md`*

**Create Track:** add audio lanes
**Arming a lane:** prepare for recording
**Sweeps:** Fill-In (short), Throw (long), Snap-Back (instant return)
**Tempo:** global BPM control
**Microphone:** for recording into lanes

---

## Known Limitations

1. **No cable routing API** — only Combinator `.cmb` files save routing
2. **No device creation API** — must use `open -a Reason`
3. **48-knob limit** per device (hardware constraint)
3. **Remote Override** — one surface controls one device at a time
4. **Rex/Kong limits** — specific patch constraints
5. **Sampled patches** — can't browse ReFills archive (sealed)

---

## Voice Commands (Current Grammar)

*From `intents.py`*

**Patch browsing:**
- "next patch" / "patch next" → CC 20
- "previous patch" / "back" → CC 21

**Transport:**
- "play" / "start" → CC 22
- "stop" → CC 23
- "record" → CC 24
- "loop on/off" → CC 25

**Track navigation:**
- "next track" → CC 27
- "previous track" → CC 26

**Undo/redo:**
- "undo" → CC 28
- "redo" → CC 29

**Recipe system:**
- "walk me through" → start walkthrough
- "next step" / "repeat" → navigation
- "done" → end walkthrough

**Find/search:**
- "find [sound]" → recipe search
- "walk me through [sound]" → find + walkthrough
- "how do i make [sound]" → walkthrough (if open)

**Device lookup:**
- "what is [device]" → device reference

**Crates (favorites):**
- "favorites" / "my crate" → open favorites
- "star #1" / "add #2 to my crate" → add to favorites
- "unstar #3" → remove from favorites

---

## Key Files & Their Roles

| File | Purpose |
|------|---------|
| `reason_voice/intents.py` | Regex grammar for voice commands |
| `reason_voice/reason_control.py` | MIDI bridge to Reason |
| `reason_voice/recipes.py` | Recipe parsing/search |
| `reason_voice/search.py` | Recipe search expansion |
| `reason_voice/server.py` | API server + UI |
| `remote/ReasonVoice.luacodec` | MIDI CC → surface item codec |
| `remote/ReasonVoice.remotemap` | Surface item → parameter binding |
| `docs/reason/remote-vocab.json` | Official parameter name source |

---

## Learning Path Recommendations

### Week 1: Foundations
1. **Understand the rack** — how devices sit in rows, columns
2. **Learn patch loading** — factory patches vs. user patches
3. **Master cable routing** — audio vs. CV, jack types
4. **Explore one device deep** — Redrum drum sequencing

### Week 2: Control & Automation
1. **Remote protocol** — which parameters are remotable
2. **Locking devices** — why a knob won't move
3. **Automation lanes** — drawing parameter changes over time
4. **Record sweeps** — Fill-In, Throw, Snap-Back

### Week 3: Production Techniques
1. **Chaining effects** — signal path order matters
2. **Parallel processing** — stereo bus sends
3. **CV routing** — modulation between devices
4. **Combinator** — building reusable rigs

### Week 4: Advanced Topics
1. **Sidechain** — ducking with MIDI
2. **Multi-sampling** — NN-XT velocity layers
3. **Supersampling** — Kong sample organization
4. **Bounce tracks** — freezing devices

---

## Common Mistakes to Avoid

1. **Assuming all parameters are remotable** — check `remote-vocab.json`
2. **Forgetting to lock a device** — CCs go to the locked surface
3. **Wrong CC ranges** — knobs 0-127, not percent
4. **Sampled patches** — can't search sealed ReFills archives
5. **Overlooking CV Trim** — modulation may be too weak/strong

---

## Resources

**Manual chapters:**
- Rack basics: Chapter 11
- Routing: Chapter 16
- Automation: Chapter 20+

**Project docs:**
- `references/devices-core.md` — per-device cheat sheets
- `references/study-notes/*.md` — detailed guides
- `device_refs/*.md` — 66 device guides
- `recipes/**/*.md` — 1000+ sound recipes

**Skills (Hermes):**
- `reason-reference` — device params & Remote mapping
- `reason-remote-bridge` — IAC Bus + codec details

---

## Next Study Topics

Based on gaps identified in existing materials:

1. **Modulation routing** — CV paths between devices
2. **MIDI routing** — note-on/off, program change
3. **Return tracks** — FX send routing
4. **Group routing** — device groups, bus assignment
5. **Scene control** — clip-based device switching
6. **FX chains** — device-specific FX (not rack-wide)
7. **Instrument layering** — stacking multiple instruments
8. **Sample replacement** — NN-XT velocity zones
9. **Synth architecture** — Subtractor/Thor signal paths
10. **Mixing** — panning, EQ, dynamics per channel

---

*End of guide*
