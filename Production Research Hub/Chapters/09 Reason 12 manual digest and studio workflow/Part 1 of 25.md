# Chapter 09: Reason 12 manual digest and studio workflow
## Part 1 of 25

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- README.md — Reason 12.7 manual digests: index
- arranging.md — Arranging: clip handling, repeat tricks, bounce, insert/remove bars
- blocks.md — Blocks: build sections once, reuse them (digest of Reason 12.7 manual, ch. 10)
- combinator.md — Combinator — what the existing guide does NOT cover
- drum-devices.md — Drum devices — Kong, Redrum, Dr. Octo Rex (how to build and control drums)

(Next: Part 2 of 25)


=====================================================
SOURCE FILE: README.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/README.md
=====================================================

# Reason 12.7 manual digests: index

Plain-language, organized digests of manual chapters your notes did not cover. Built 2026-09-30 from
`~/.reason_voice/reason12_manual/full_chapters/`. Every fact is tagged **Manual** (read in the manual). Nothing was tried in Reason or heard.
Use with the `reason-reference` skill (search rules) and `docs/reason/remote-vocab.json` (parameter spellings, not the manual).

## What is here

| File | Manual chapter | Use it when | Skill status |
|---|---|---|---|
| [players.md](players.md) | 12 Working with Players | chords/arps from single notes, Note Echo, Direct Record | idea only |
| [blocks.md](blocks.md) | 10 Blocks | build and reuse song sections, intros by muting lanes | idea only |
| [audio-editing.md](audio-editing.md) | 8 Audio Editing | fix audio timing, tune vocals, comp takes, drums to MIDI, audio to REX | idea only |
| [sampling.md](sampling.md) | 21 Sampling | resample a device, Edit Sample window, Song Samples | idea only |
| [delay-compensation.md](delay-compensation.md) | 18 Delay Compensation | phasey parallel chains; when to switch it off to record | idea only |
| [key-commands.md](key-commands.md) | 70 Key Commands | any shortcut (Mac left of the slash, Windows right) | reference |
| [routing-and-main-mixer.md](routing-and-main-mixer.md) | 16 Routing, 17 Main Mixer | cables, auto-routing, channel strip, sends, buses, sidechain, de-ess, recipes A-J | idea only (`reason-mixer-chains`) |
| [rack.md](rack.md) | 11 Working with the Rack | creating/moving/duplicating devices, Device Groups, naming, Shift tricks | reference |
| [combinator.md](combinator.md) | 63 Combinator (extras only; basics in `device_refs/combinator.md`) | split/layer zones, macro knobs, CV, panel design | idea only |
| [recording.md](recording.md) | 6 Recording | vocal levels, monitoring, takes, resampling, automation recording | idea only |
| [note-and-automation-editing.md](note-and-automation-editing.md) | 9 Note and Automation Editing | quantize, velocity, Explode, Alter Notes, curves, cleanup | idea only |
| [remote-control.md](remote-control.md) | 23 Remote | map hardware knobs, lock surfaces, Remote Override, keyboard control | reference |
| [sequencer-functions.md](sequencer-functions.md) | 5 Sequencer Functions | track types, lanes, toolbar, snap, locators, loop, tempo | reference |
| [arranging.md](arranging.md) | 7 Arranging | copy a section across tracks, Razor in Ruler, Bounce in Place, insert/remove bars | reference |
| [export-and-performance.md](export-and-performance.md) | 19 Song files, 20 Import/Export, 25 Performance | export a mix, stems, dither, crackle fix order, cheap-CPU habits | reference |
| [patches-and-browser.md](patches-and-browser.md) | 13 Rack Extensions, 14 VST, 15 Patches and Browser | find/load/save patches, Insert FX patches, ReFills, RE and VST handling | reference |
| [drum-devices.md](drum-devices.md) | 27 Kong, 28 Redrum, 29 Dr. Octo Rex (technique only; knobs in `device_refs/`) | Kong output/FX flow, choke and layer groups, Redrum pattern tricks, REX to MIDI | idea only |
| [synth-sound-design.md](synth-sound-design.md) | 30 Europa, 32 Mimic, 33 Thor, 34 Subtractor, 36 Monotone, 43 NN-XT | build bass/pad/pluck/lead, mod routing, slicing | idea only |
| ReGroove | 22 ReGroove Mixer | swing, slide, groove patches | **draft skill**: `.claude/skills/reason-regroove/SKILL.md` |
Earlier summaries: [../manual-bigger-wins-2026-09-30.md](../manual-bigger-wins-2026-09-30.md), [../guide-new-ideas-2026-09-30.md](../guide-new-ideas-2026-09-30.md).

## Manual chapters NOT digested yet
24 Sync and Advanced MIDI, 69 Menu and Dialog Reference (only a few lines read), 1-4 intro/basics, and the device chapters not listed above (35 Malstrom, 37 ID8, 38 Rytmik, 39 Radical Piano, 40 Klang, 41 Pangea, 42 Humana, 44 NN-19, 45-51 and 56-62 effects, 55 Softube Amps, 64-68 utilities). The effects and instruments in that list already have short guides in `device_refs/`; 52 BV512 and 54 Neptune were read for `../techniques/vocals.md`.
Suggested next, by likely value: 24 Sync (if he syncs hardware), 55 Softube Amps, 61 MClass effects, 49 Pulveriser.

## Chain techniques (manual + web) live next door
[../techniques/README.md](../techniques/README.md): vocals, drums, bass/808, instruments and movement, buses/sends/master.

## Known limits
- Key Commands was converted by script and spot-checked; join-wrapped rows should be checked against the manual before relying on them.
- Skill ideas are not yet tested with the skill-creator benchmark loop (your standing rule for new skills).

=====================================================
SOURCE FILE: arranging.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/arranging.md
=====================================================

# Arranging: clip handling, repeat tricks, bounce, insert/remove bars
Source: Reason 12.7 Operation Manual, ch. 7 (whole chapter read, ends p. 202). Tag: **Manual**.
Tracks, lanes, tools, Snap and locators are in `sequencer-functions.md`. Sections you reuse (Blocks) are in `blocks.md`. Comping and audio clip internals are in `audio-editing.md`.
(KC) = from the Key Commands chapter, `key-commands.md`.

## 1. The 10 moves that build a song fast
| Job | Do this |
|---|---|
| Make an empty clip | Double-click a lane with the arrow (length = Snap value, e.g. 1 bar). Double-click and drag right for longer. Or draw with the Pencil (**W**) |
| **Repeat a whole section** | Stop. Snap on, Snap = Bar (or section length). Select the clips (can be on many tracks). **Cmd+C**. Playhead jumps to the end of the selection. **Cmd+V**, then V again and again. Each paste lands right after the last |
| Quick copies in a row | **Cmd+D** on selected clips. Copies line up after each other, spaced by Snap |
| Drag a copy | **Option+drag** (cursor shows +). Copies on the same lane or another |
| Split anywhere | Razor (**R**) click. Notes that cross the cut stay whole |
| Split EVERY track at one spot | Razor click in the **Ruler**. Includes lanes scrolled out of view |
| Cut a hole out of the whole song | Razor click-drag in the Ruler. Releases = clips split at both ends |
| Silence a part without deleting | Mute tool (**T**) or select + **M** (M again to unmute) |
| Make the end of a part longer | Select clips, drag any resize handle. All selected grow the same amount |
| Change many clip lengths/positions at once | Inspector Position/Length boxes, or Match Values (sec. 7) |

## 2. Selecting
- Click a clip. Click empty space to deselect.
- Several: **Shift+click** on Mac [Ctrl+click on Windows]. Or drag a box with the arrow (anything touched is picked). Shift while boxing adds to what is already picked. **Cmd+A** = all.
- Arrow keys: Left/Right = previous/next clip on the lane. Up/Down = closest clip on the lane above/below. Shift+Left/Right = extend on the same lane.
- Selected note clips: open several together for Multi Lanes editing (`note-and-automation-editing.md`).

## 3. Resize = mask, nothing is deleted
- Shrinking a clip HIDES what falls outside. Notes, audio and automation are still inside and come back when you drag the edge out again. Masked events travel with the clip when moved, cut or copied.
- Note/automation clips show **white corners** where masked events sit. Audio clips show no sign.
- Masked notes turn blue in the open clip. A note that STARTS inside the clip still plays in full.
- Edge case: a masked controller/automation point just outside the clip still bends the curve toward it inside. Black-and-white points = still active.
- **Edit > Crop Events to Clips** permanently deletes everything outside the edges. Use only when you want it gone.
- Audio fades follow the clip edges when you resize.

## 4. Moving
| Do | How |
|---|---|
| Move on the lane | Drag (obeys Snap) |
| Move to another lane or track | Drag. **Shift** while dragging = straight up/down only (on Windows press Shift AFTER the mouse button) |
| Nudge by Snap value | **Cmd+Left/Right** (works with Snap off) |
| Nudge by a beat | **Cmd+Shift+Left/Right** |
| Nudge by a tick (240 per 16th) | **Cmd+Option+Left/Right**. Watch the Inspector, you will not see it |
| Cut then paste at playhead | Cut, move playhead, Paste. Lands on its ORIGINAL lane |
- Wrong lane type = **alien clip** (red stripes, plays nothing). Hover for the reason. A note clip on an automation lane is alien. An automation clip on a lane with a different range (e.g. -64..63 vs 0..127) is alien. Fix the range case with **Edit > Adjust Alien Clips to Lane**.
- Moving a note clip to another instrument: Pitch Bend, Mod Wheel, Sustain translate fine. Not every device answers Aftertouch/Expression/Breath (Malström does not). Odd recorded knob moves with no match are ignored.
- Paste into ANOTHER song: select a track there, set the playhead, paste. Missing tracks come in on empty Combinators. Pick a patch in that Combinator.

## 5. Overlap rules
- A lane plays ONE clip at a time. To hear two at once, use separate note lanes or separate tracks.
- The clip that STARTS LATER wins where they overlap. A short clip dropped inside a long one plays: long part, short clip, rest of long.
- Same start and same length: the one moved last sounds, the other is silent.
- **Crossfade audio**: overlap two audio clips, select the later one, press **X** (or right-click > Crossfade). X again removes it. Drag the zone edges to resize (this resizes the clips). Drag the curve sideways for symmetry.

## 6. Join, merge, bounce
| Function | What it does |
|---|---|
| **Join Clips** (Cmd+J) | Same-lane clips become one. Gaps stay empty. DANGER: masked events between or under the joined clips are permanently deleted. The top clip wins in overlaps |
| Join OVERLAPPING audio | Nothing lost. Clips go on separate Comp Rows and are auto-comped. Fades in overlaps are removed. Clip Level resets to 0 dB, the old levels move to Comp Row levels |
| Join CROSSFADED audio | The crossfade zone is bounced to a new Comp Row. Result becomes stereo (two identical channels) even if the clips were mono |
| Muted clips | Cannot be joined |
| **Merge Note Lanes on Tracks** (Cmd+R, KC) | All lanes on the track collapse onto the TOP lane. Muted lanes/clips are left out. Works on several tracks at once |
| **Bounce in Place** (Edit or right-click; audio clips: Bounce > Bounce in Place) | Renders a clip to audio on a NEW audio track, with insert FX and channel strip, WITHOUT sends or the Master Section. Same position and length. Source clip is muted automatically. New track copies mixer settings and Output Bus routing |
- Bounce in Place jobs the manual lists: make audio from notes to chop or reverse (reverb tail played backwards), print effects, make samples for a sampler or a REX loop (Bounce > Bounce Clip(s) to New Sample(s) / to REX Loop in `audio-editing.md`).
- Bounce details: tail limit = 5 seconds after the last note-off or clip end. The tail may be hidden: drag the new clip's edge out to show it. Long notes that run past the clip edge are rendered fully (also hidden). Fully masked notes are not rendered. Source parameter automation IS included. Mono audio comes out stereo (post-pan).
- Several clips: same source track = same new track; different tracks = separate new tracks. Instrument split across several Mix Channels = one audio track per Mix Channel.
- Bounce in Place is DISABLED when the device does not have its own Mix Channel (e.g. it goes through a shared Mixer 14:2). Whole tracks: use Bounce Mixer Channels instead (`audio-editing.md`, `recording.md`).

## 7. Clean-up tools
| Tool | What it does |
|---|---|
| **Match Values** (button beside Position / Length / Fade / Level / Transpose in the Inspector) | Copies the TOP (or leftmost) selected clip's value to all selected. Position match stacks clips on the same start, so same-lane clips will overlap |
| Clip Fade handles / Level handle | Selected audio clip: drag top corners for fades, drag the middle handle up/down for level. Non-destructive. Obeys Snap |
| Add Labels to Clips | Names a clip. Double-click the label to rename. Remove Labels from Clips clears them |
| Clip Color | Default is Track Color. Override per clip. Colour-code Verse/Hook visually |
| Scale tempo by dragging | Arrow tool, hold **Option** over a clip resize handle, drag. Contents stretch with the clip (notes, automation, audio). Pattern clips only resize; the device pattern speed does NOT change. Numeric version = Scale Tempo in the Tool Window |
| Reverse clips | Edit > Reverse (note/automation: see `note-and-automation-editing.md`; audio: `audio-editing.md`) |

## 8. Insert or remove whole bars (song-level edits)
1. Set the Left and Right Locators round the gap (loop locators do this job here).
2. **Edit > Insert Bars Between Locators**: clips crossing the left locator are split. The part after the left locator is moved to start at the Right Locator. Result: empty bars between them for a new bridge or longer intro.
3. **Edit > Remove Bars Between Locators**: that range is cut out and the rest slides left. Notes and automation inside it are DELETED. Audio inside is NOT deleted: it is masked and moved forward on a Comp Row, still reachable in the Comp Editor.
- Affects ALL tracks and lanes at once. **[Guess]** do a Save As first when removing many bars. Undo is there too.

## 9. Ideas for us (**Guess**, not tried)
- Build a 64-bar skeleton: Razor in the Ruler at section boundaries, then colour clips per section.
- Make a drop: copy a verse, Insert Bars before the hook, paste.
- Print a finished synth part with Bounce in Place (source clip is muted for you). **[Guess]** this is the closest thing to "freezing"; the manual does not use that word and does not say it saves CPU.

=====================================================
SOURCE FILE: blocks.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/blocks.md
=====================================================

# Blocks: build sections once, reuse them (digest of Reason 12.7 manual, ch. 10)

Source: `~/.reason_voice/reason12_manual/full_chapters/10-working-with-blocks-in-the-sequencer.txt` (manual pp. 311-326). Digested 2026-09-30.
Tag: all **Manual**. Nothing tried or heard. Overlap check: 0 files in your notes mention Blocks. Index: [README](README.md)

## In one line
A **Block** is a short multi-track section (a verse, a chorus, usually 4-8 bars) you record once and place anywhere in the song. Same idea as a
drum machine "pattern", but for whole tracks. 32 Blocks per song.

## Set up
1. **Options > Enable Blocks** (new songs and template songs already have it on; a song saved without it needs this).
2. A **Blocks Track** appears above the Transport Track with a **Block button** and a **Song button**. Shortcut to toggle the view: **B**.
3. Block View and Song View share the same Track List, but the CLIPS are separate. You can put Song clips on top of Block clips.

## Make a Block
1. Click the **Block** button (Block View). Pick Block 1 to 32 from the drop-down in the Track List.
2. Rename: double-click the Block name on the Blocks Track.
3. **Length** = drag the **End Marker** in the ruler. Length always counts from the start of the ruler. Loop locators don't change it. It loops at the End Marker while you work.
4. Record and edit clips on tracks exactly like normal. Anything to the right of the End Marker is ignored when the Block plays in the song.
5. Color: Block Color palette (Blocks Track right-click menu or Edit menu). Track and clip colors stay as they were.

## Place Blocks in the song
1. Click the **Song** button. Pick the **Pencil**. A **Block selector** appears in the Inspector: choose the Block.
2. Draw a **Block Automation Clip** on the Blocks Track (or double-click with the Arrow tool for one snap-length clip, then drag to lengthen).
3. The Block's content shows ghosted on the tracks.
- Longer than the Block: the Block repeats (thin lines mark the repeats). 8-bar Block in a 20-bar clip = repeats at bars 9 and 17, the last 4 bars cut off.
- Shorter than a full multiple: the rest is masked (muted).
- **Block Offset**: dragging the clip's LEFT edge makes it start partway into the Block. Pattern tracks (Redrum) stay in step.
- **Swap the Block** in an existing clip: little triangle on the clip > pick another Block.

## Build an intro from ONE Block (the manual's example)
Copy the Block Automation Clip twice, resize the last one longer, then use the **Mute tool** on lanes inside each clip.
Clip 1 (8 bars): Piano + Bass. Clip 2 (8 bars): + Drums. Clip 3 (16 bars): all but Piano. One 8-bar Block gives a 32-bar build.
Mutes last exactly as long as that clip, so each different mute pattern needs its own clip.

## Turn Blocks into normal clips
- One clip: select the Block Automation Clip > Edit menu or its right-click > **Convert Block Automation to Song Clips**. Only unmuted clips are converted; the Block stays.
- All at once: Track List right-click > **Convert Block Automation to Song Clips**. The Blocks Track is then muted automatically (click **M** to bring it back).
- Copy and paste clips between Block View and Song View also works.

## Add variations on top
**Song clips beat Block data.** A normal clip on the same lane silences the Block underneath it. Manual's tip: arrange Blocks first, then record short
Song clips (a fill, a pickup, a one-bar change) over the top.

## Ideas for us (not built)
- Skill idea **reason-blocks**. Fits "64-bar song map" in `../demo-song-template-and-automation-ideas.md` (Intro / verse / hook as Blocks).
- Voice phrases to consider: "switch to block view", "make block 2 eight bars". Not checked whether the remote map can reach any of this.

=====================================================
SOURCE FILE: combinator.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/combinator.md
=====================================================

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

=====================================================
SOURCE FILE: drum-devices.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/drum-devices.md
=====================================================

# Drum devices — Kong, Redrum, Dr. Octo Rex (how to build and control drums)
Source: Reason 12.7 Operation Manual, ch. 27 Kong, ch. 28 Redrum, ch. 29 Dr. Octo Rex (all three read in full). Tag: **Manual**.
Knob lists are NOT repeated: see `device_refs/kong.md`, `redrum.md`, `dr-octo-rex.md`. Anything the manual does not say is marked **[Guess]**.
(The chapter files number Redrum as ch. 28; `device_refs/redrum.md` cites ch. 26.)

## 1. Kong — signal flow (the one picture to keep)
Drum Module -> FX1 -> FX2 -> (Tone, Pan applied; Aux 1/2 Send tapped here) -> Bus FX -> Master FX -> Main Out L/R.
| Slot | Per pad or shared | Notes |
|---|---|---|
| Drum Module | Per pad (16) | 9 types, see section 2 |
| FX1, FX2 | Per pad | Any FX module OR a Noise / Tone generator |
| Bus FX | Shared by all pads | Works as a send. No Noise/Tone generators here |
| Master FX | Shared | Last stop before Main Out. Same choices as Bus FX |
- Each slot has an On button. Only 4 params per drum module and 2 per FX module can be automated.
- **Pitch Offset** moves pitch in drum modules only (never FX). **Decay Offset** moves decay in drum modules AND in FX that have a decay (Room Reverb's decay time too).

### Where a pad goes (Drum Output selector, bottom of Drum and FX section)
| Setting | What happens | Use it for |
|---|---|---|
| Master FX | Bus FX is a send, level = **Bus FX Send** | Normal kit, one shared reverb/delay |
| Bus FX | Bus FX is insert AND send at once | Whole pad through one effect. Set **Bus FX Send** to zero or it doubles |
| 3-4 ... 15-16 | Taken after FX2 to its own jack pair. Bus FX part still reaches Main Out | One pad on its own mixer channel |
- Separate outs are NEVER auto-routed. Cable them to a Mix Channel yourself (rename the strip, see `rack.md`).

| To get | Do |
|---|---|
| One room for the whole kit | Drum Room Reverb in Bus FX, raise **Bus FX Send** on the pads that need it |
| Glue on the whole kit | Compressor in Master FX |
| Sweep the whole kit | Filter or Ring Modulator in Bus/Master FX, set MIDI Trig EG Amount, play MIDI note E2 (Bus FX) or F2 (Master FX). Pads end at D#2, so E2/F2 are free |
| Kick on its own channel for EQ/comp | Drum Output 3-4, cable Audio Out 3-4 to a Mix Channel |
| An RV7000 between Bus and Master FX | External Effect jacks. With Output on Master FX or Separate, **Bus FX Send** also sets the level into it |

## 2. Kong — the drum modules (what each is FOR)
| Module | Good for | Controls that shape it (manual names) |
|---|---|---|
| Physical Bass Drum | Acoustic kick | Pitch (= drum size), Tune 1/2, Bend Amount, Damp, Shell Level, Density (beater hardness), Beater Level |
| Synth Bass Drum | Electronic kick | Click Frequency/Resonance/Level, Bend Amount/Time, Attack, Tone |
| Physical Snare | Acoustic snare | Tune, Snare Tension, Bottom Pitch, Bottom Mix, Edge Tune (only for Hit Type 4, Edge Hit) |
| Synth Snare | Electronic snare | Harmonic Balance/Frequency/Decay, Noise Tone/Decay/Mix |
| Physical Tom | Acoustic toms | Tune 1/2, Shell Size, Shell Level, Stick Level |
| Synth Tom | Electronic toms (modelled on an 80s hexagonal-pad kit) | Bend Amount/Time, Click Level, Noise Tone/Decay/Mix |
| Synth Hi-hat | Early drum-machine hats | Click, Tone, Ring (higher = more metallic), Decay. Hit Types: Closed, Semi-Closed, Semi-Open, Open |
| NN-Nano Sampler | Any one-shot sample (also REX slices, SoundFonts) | 4 Hits, layers, per-sample Velocity range/Level/Pitch/Alt |
| Nurse Rex | A REX loop spread over pads | Hit Types Loop/Chunk/Slice Trig and Stop (section 4) |
- No clap, cymbal or percussion module. **[Guess]** use NN-Nano with samples for those.
- Support generators (FX1/FX2 only, beside any module or alone): **Noise** (Pitch, Attack, Decay, Reso, Sweep, Click, Level) and **Tone** (Pitch, Attack, Decay, Bend, Bend Decay, Shape, Level). Their Hit Type buttons pick which hits they sound on.

| To get | Do |
|---|---|
| Bigger, boomier acoustic kick | Lower Pitch (it is the drum's total size), raise Decay; Shell Level adds body |
| More punch on any drum | Transient Shaper: Attack positive + Amount high. Negative Attack softens |
| Snare buzz on a kick or hat | Rattler. Odd rule: HIGHER Snare Tension = LESS rattle |
| Shorter room on a snare | Reverb in FX2, lower **Decay Offset** (it shortens the reverb too) |
| Metal hi-hat | Synth Hi-hat, raise Ring |
| Sub under a sampled kick | **[Guess]** NN-Nano in the Drum slot, Tone generator in FX1 (Bend for the drop) |

## 3. Kong — layers, Hit Types, groups, choke
| Tool | What it does | Recipe |
|---|---|---|
| Drum Assignment | Many pads can play ONE drum (default pad N = drum N) | Same drum on 4 pads, a different Hit Type on each (Closed to Open) = a "live" hat |
| Mute Group (3) | Pads in one group cut each other off | Closed hat + open hat pads in one Mute Group = hat choke |
| Link Group (3) | Hit one pad, all pads in the group play | Layer two different drums (each with own FX) from one pad |
| Alt Group (3) | Any pad in the group fires a RANDOM pad of the group | Round-robin snares/hats so no two hits match |
| Pad Mute / Solo | Red = muted, green = solo. Also blocks MIDI to that drum | CLR clears all |
- A pad can sit in several of the 9 groups. Every "Quick Edit" button shows all pads at once; Esc exits.
- NN-Nano layering: load several samples at once = several Layers in a Hit. Each has Velocity Lo/Hi (velocity layers), Level, Pitch, Alt (tick on several = they alternate).
- NN-Nano **Polyphony**: Full / Exclusive Hits (one Hit mutes the others = choke inside one drum) / Monophonic. Its Velocity section can steer Pitch, Decay, Level, Bend, Sample Start.
- Pitch/Decay Quick Edit: drag a crosshair on each pad (X = Decay Offset, Y = Pitch Offset).
- Clicking low on a pad = soft, high = hard. MIDI: C1 to D#2 = one key per pad; C3 to B6 = 3 keys per pad (fast rolls).
- Build a kit: click a pad, load a `.drum` patch / sample / REX (Factory Sound Bank > Kong Drum Patches), repeat, save the Kit Patch. Cmd+C/V copies a drum to another pad. **Sample** button records into an NN-Nano. **Reset Device** = empty kit.

## 4. Kong — Nurse Rex (a loop across pads)
| Hit Type | Pad does |
|---|---|
| Loop Trig | Plays the whole loop once per hit (set Start/End slice) |
| Chunk Trig | Each pad plays an equal chunk. 4 pads = 4 chunks; drag tab edges to resize |
| Slice Trig | One slice, or several alternating (Cmd-click slices to add; default slice 1) |
| Stop | Cuts a playing loop/chunk. Only useful with Loop or Chunk Trig |
- Manual's example: 8 pads on one Nurse Rex = pad 1 Loop Trig, 2-6 Chunk Trig, 7 Slice Trig (4 slices), 8 Stop.
- WARNING: drop a REX file ON a pad or the Drum Control Panel. Dropped anywhere else it replaces all of Kong with a Dr. Octo Rex.

## 5. Redrum — building patterns
Tutorial in short: load a patch > Clear Pattern > Enable Pattern Section and Pattern on > **Run** > click **Select** under a channel > click Step buttons (click a lit one to remove, drag to paint) > pick the next channel. Steps can be edited with Run off.
| Want | Do |
|---|---|
| Pattern length | **Steps** spin, 1 to 64. Shortening only hides steps; raise it and they return |
| See steps past 16 | **Edit Steps** switch (17-32, 33-48...). They play even when hidden |
| Speed | **Resolution** changes each step's length. The chapter lists no values, so **[Guess]** use it for double-time hats |
| Accents | **Dynamic** switch Soft / Medium / Hard (yellow, orange, red) before clicking. At Medium: Shift-click = Hard, Option-click = Soft |
| Accents you can hear | Set that channel's Vel knob off zero. At zero every step plays the same |
| Flam / roll | Click Flam, then add a step (red LED). Click the LED to add/remove later. Flam on steps in a row = roll. **Flam** knob can give 1/32 on a 1/16 grid |
| Swing | **Shuffle** button per pattern (delays the 16ths between 8ths). Amount = Global Shuffle in the ReGroove Mixer |
| New idea | Edit menu: Randomize Pattern/Drum, Alter Pattern/Drum (reshuffles existing hits, tamer), Shift Pattern/Drum left/right |
- 32 patterns: Banks A-D x buttons 1-8. Bank click does nothing until you click a Pattern button. Changes land on the next downbeat.
- Patterns are NOT in the patch; they live in the song. To keep them with a kit, put Redrum in a Combinator and save the Combi.
- Cut / Copy / Paste Pattern moves patterns (even between songs). **Pattern** button OFF mutes it from the next downbeat.
- **Chaining:** record or insert pattern changes in the main sequencer ("Recording pattern automation" is in another chapter, not read here). Main-sequencer or MIDI notes can add fills over the pattern (C1 = channel 1).
- Hits as editable notes: set locators (a multiple of the pattern length), **Copy Pattern to Track**. Velocities: Soft 30 / Medium 80 / Hard 127. Turn OFF Enable Pattern Section or hits double. **Convert Pattern Automation to Notes** does a whole chain.

## 6. Redrum — channel and send tricks
| Trick | How |
|---|---|
| Hat choke | **Channel 8 & 9 Exclusive** on: either channel cuts the other |
| Kick/tom pitch drop | **Bend** (+ Rate, Vel): channels 6 and 7 ONLY. **[Guess]** kick/tom use |
| Tone filter | Channels 1, 2, 10 only |
| Hits that react to velocity | Sample **Start** (channels 3-5, 8, 9 only): raise it a little, Start Vel negative = the attack only appears on hard hits |
| Gated sounds | Decay/Gate to Gate: stops at Length or when the note ends. Warning: a looped sample with Length at max never stops |
| Effects on single drums | **Send 1 / Send 2 Amount**. Sends auto-go to the Mixer's first two Chaining Aux inputs; needs send effects there; muted if Redrum is soloed in the Mixer |
| Own mixer channel per drum | Each channel has its own output (mono: Left (Mono)). Using it removes that drum from the stereo mix |
| Mute a drum live | MIDI keys C2 to E3 (white) mute channels 1-10 while held; C4 to E5 solo. Recordable |
| Slice from a loop | Browser: unfold a REX file, load one slice into a channel |
| Trigger other gear | Gate Out fires on every hit; Gate In / Pitch CV In play a channel from outside |

## 7. Dr. Octo Rex — loops, slices, MIDI
A REX file is a loop pre-cut at every hit, so tempo changes keep pitch and punch.
| To get | Do |
|---|---|
| 8 loop variations | Folder button, multi-select (Cmd/Shift), Load: first goes in the selected slot, rest in the next slots (replaces what is there) |
| Switch loops in time | Click a Loop Slot while it runs. **Trigger Next Setting** (Trig Next Loop) Bar / Beat / 1/16 sets when it lands. Pattern Automation in the main sequencer switches instantly instead |
| Play slots from keys | E0 to B0 = slot 1-8 start, D#0 = stop, D0 = play the Note-To-Slot loop once (cannot be stopped) |
| Duplicate and tweak a loop | Copy Loop, Paste Loop into another slot (right-click the panel background, not a knob), edit the copy's slices |
| Play slices like a sampler | Slices sit on C1, C#1... one per slice. **Notes to Slot** picks the slot. Turn **Enable Loop Playback** off or it also loops |

### Slice-to-MIDI: "Copy Loop to Track"
1. Select the Dr. Octo Rex's sequencer track. 2. Set locators over the span to fill. 3. Select the slot. 4. Click **Copy Loop To Track**. 5. Turn **Enable Loop Playback** OFF or every note doubles.
- One clip, one note per slice from C1 up, timed as in the loop. **Notes to Slot** is written in as a controller so it plays the right slot.
- Locators longer than the loop = clip repeats. It makes whole clips, so the last may poke past the right locator (drag its edge to mask it).
- Every velocity is 64. Edit the Velocity Lane or the velocity amounts (F. Env, F. Decay, Amp) do little.
- Then: quantize, move notes, transpose notes to reorder slices, Alter Notes to scramble while keeping timing, User Groove to copy the loop's feel onto other tracks. A REX edit lane shows slice numbers.
- Automate **Notes to Slot** to take each slice from a different slot (the manual's "beat mangling").

### Per-slice shaping (waveform display, or **Slice Edit Mode** to draw one parameter across all slices)
| Slice parameter | Use |
|---|---|
| Pitch (semitones) / Pan / Level (default 100) | Tune a kick slice, widen hats, balance hits |
| Decay | Shorten single slices (tighten a ringing snare) |
| Rev / F.Freq | Backwards slice / per-slice filter offset on top of the panel Freq |
| Alt (1-4) | Slices in one Alt group are picked at random each pass. Snares in Alt 1, hats in Alt 2 = loop differs every cycle |
| Output (1-8) | Slice to its own jack, e.g. snare slices to their own mixer channel with reverb |
- Ctrl/Cmd-click resets a slice in Slice Edit Mode. All slice settings are LOST if you load a new REX into that slot.
- Polyphony of 3-4 voices is enough for loops. Amp and Filter envelopes re-fire on every slice.
- Gate Output sends a gate per slice. **[Guess]** it can fire a Kong pad.

## 8. For the project (**Guess**)
- Hit Types, Mute/Link/Alt groups and slice settings are mouse work, so recipes should name the button.
- Redrum Gate Out into a Kong pad's Gate In would let Redrum's steps play Kong drums. Two manual facts joined, not a manual tutorial.

=== END OF PART ===
