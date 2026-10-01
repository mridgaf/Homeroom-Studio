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
