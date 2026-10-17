# Chapter 03: Mixing, routing and buses
## Part 1 of 4

_How to wire effects, buses and sends in Reason, plus the Reason 12 template and technique library (by genre and by type)._

**In this part:**
- SKILL.md — Reason 12.7 drum routing and drum bus
- SKILL.md — Reason 12.7 mixer chains: how to build and control them
- SKILL.md — Reason 12.7 vocal chain

(Next: Part 2 of 4)


=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:docs/reason/skill-benchmarks-2026-10-01/skills/reason-drum-bus/SKILL.md
=====================================================

---
name: reason-drum-bus
description: How to route, glue and add punch to drums in Reason 12.7. Getting each drum from Kong, Redrum or Dr. Octo Rex onto its own mixer channel, building a drum bus with glue compression, parallel compression (Mix knob, Parallel Channel, Spider split), saturation and grit, one shared room, kick-and-808 relationship, kick ducking the bass, plus trap and industrial pattern recipes. Use whenever the owner says his drums sound thin, flat, separate, weak, "not glued", asks how to route a kit, make a drum bus, parallel-compress drums, make hats roll, build a trap or boom-bap or industrial beat chain, or get the kick and 808 to stop fighting in Reason. Reason 12.7 only; nothing has been heard.
---

# Reason 12.7 drum routing and drum bus

Sources: Reason 12.7 Operation Manual (ch. 17 mixer, 27 Kong, 28 Redrum, 29 Dr. Octo Rex, 59 compressors), Reason Studios
articles (a trap drums piece, a 2025 industrial house piece), r/reasoners threads. Nothing here has been heard on this
machine. Tell him once, briefly, that settings are starting points.

## How to answer
- Plain words, short numbered steps, exact button and knob names. Name the cheapest fix first (usually a Mix knob), then the
  heavier one.
- Fit the length to the question: about 300 words or fewer unless he asks for the full setup. Offer the next piece in one line.
- Reason 12.7 only. NOT in 12.7: Sidechain Tool, Gain Tool, Stereo Tool, Ripley, RV-9. Use the cable method below.
- Knob names: never from memory. `device_refs/kong.md`, `redrum.md`, `master-bus-compressor.md`, `scream-4.md`, or
  `docs/reason/remote-vocab.json` (`tools/reason_vocab.py` does the same but only runs on the Mac with Reason installed).
- Separate what the manual says from web opinion and from your own idea. One short flag each, no more.
- Don't split everything by default. Split a drum onto its own channel only when it needs its own treatment (EQ, compressor,
  bus, sidechain). Level and pan can be done inside the drum device.

## 1. Get each drum onto its own channel
| Device | How |
|---|---|
| **Redrum** | Every drum has its own output jack on the back. Cable one out and that drum is **removed from Redrum's main stereo out**, so it is not heard twice. Mono sound: use the Left (Mono) jack. Ctrl-click the jack and pick "new Mix Channel". Per-drum **Send 1 / Send 2** feed Send Out 1 and 2 for per-drum effects |
| **Kong** | Pick the pad's destination with the **Drum Output** selector (bottom of the Drum and FX section). Master FX = normal, with Bus FX acting as a send. Outputs 3-4 up to 15-16 go to their own jack pairs. These are NEVER auto-routed. Cable them to a Mix Channel yourself |
| **Dr. Octo Rex** | Slices can go to their own jacks with the slice **Output** setting (1 to 8) |
| A MIDI drum clip already recorded | **Explode** (Tool Window, F8) makes one clip per drum pitch. Give each lane its own ReGroove channel, or bounce each to audio |

## 2. The drum bus
1. Drums on their own Mix Channels.
2. Select them, **Cmd+G** (Route to New Output Bus). Rename it "Drums".
3. If you layer, sub-bus similar sounds first (two snares to a "Snares" bus, then to Drums).
4. Per channel: only the compression or saturation that drum needs. On the bus: glue and/or saturation. Reverb on a send.
5. Glue: select the Drums bus channel and create a **Master Bus Compressor** (SSL-style); it lands in that channel's Insert FX.
   **Ratio 2:1**, **Mix 100%**, aim for **1 to 3 dB** of reduction, **Attack 10 to 30 ms** so the hits still punch through. Or
   **MClass Compressor** with a slowish attack (30 ms or more). Watch the reduction meter. This is the glue compressor, so
   leave Mix at 100%.
6. Kong shortcut: put a Compressor in Kong's **Master FX** for glue across the whole kit without any routing.
7. Redrum with no bus yet: select the Redrum and create the compressor; it is inserted between Redrum and its Mix Channel. The
   catch: a drum you cabled out of its own jack is no longer in Redrum's main stereo out, so a compressor on Redrum does not touch
   it. Build the bus once you split drums out.
Cable steps for buses, sends and parallel: `reason-mixer-chains` recipes 2, 3, 4.

## 3. Punch AND weight: parallel compression (cheapest first)
1. **Mix knob**: a SECOND compressor on the drum bus (a glue compressor at Mix 100% and a parallel one need two devices).
   Channel Dynamics or Master Bus Compressor, **Mix** about 30 to 50%, Ratio high, compress hard. No cables.
2. **Parallel Channel**: select the Drums bus, Create Parallel Channel, turn on its compressor with a high Ratio, blend its
   fader under the dry bus. (The manual's own example.)
3. **Spider split**: bus out into a Spider Audio splitter, one clean path plus effect-only paths (a reverb, a Scream 4), each
   on its own mixer channel. The clean beat stays as the backbone.
It is common to parallel-compress only the kick or snare, not the whole kit.

## 4. Grit and glue
- Saturation per drum, and on the bus. When the kick pushes the bus into the saturation, hats and shakers get squashed and
  gritty with it. That is the "edge of breakup" feel.
- Tools in 12.7: **Scream 4** (Tape or Tube = warm, Overdrive = harder) and **MClass Maximizer**. A hard clipper is not in
  the box. In parallel, pull Scream 4's **Cut Lo** down so the low end stays clean. Keep Damage Control in the 20 to 60 range.
- ONE subtle room send shared by the whole kit makes it sound played in one space. Don't wash it. Gated 80s snare: RV7000's
  Gate section. How to wire it: put a send reverb on the Master Section (Create Send FX, `reason-mixer-chains` recipe 2) and
  turn the Drums bus's send up a little. Redrum's own per-drum **Send 1 / Send 2 Amount** go to the Mixer's first two Chaining
  Aux inputs and only work if send effects exist there. For a drum bus, the bus send is the simpler route.

## 5. Kick, 808 and the bass
- Two sounds cannot own the same low notes. Separate them by **pitch** or by **time**.
- Treat the kick as the **attack** and the 808 as the **sustain**. Keep the kick's low end short; give the 808 a long decay or
  delay it 10 to 50 ms (back off if you hear two hits). Add light saturation to the 808 so it shows on small speakers.
- Kick ducks the bass: see `reason-mixer-chains` recipe 5 (kick channel's Parallel Out to the bass compressor's Sidechain
  input, KEY lights). A drum machine's kick must be on its own channel first (table above).
- Details, EQ separation, building an 808 from a synth: `docs/reason/techniques/bass-and-low-end.md`.

## 6. Pattern recipes
**Trap** (web: Reason Studios, 2018): 60 to 90 BPM, clap or snare on 2 and 4. Hats: write straight 16ths, then vary with
triplets, 32nds and bursts of 64ths at phrase ends; Quantize changes the rhythm feel. 808 kick on beat 1, space on 3, a few
on the "and" around 3. A second long-sustain 808, pitch changed per note, becomes the bassline.

**Redrum rolls and accents**: Flam button then add a step; flams on steps in a row make a roll; the Flam knob can give 1/32
on a 1/16 grid. Set a channel's **Vel** knob off zero or accents are inaudible. Redrum hat choke: **Channel 8 & 9 Exclusive** on.

**Kong hat choke and variation** (manual ch. 27, "Working with Pad Groups"): Kong has 9 pad groups: 3 Mute, 3 Link, 3 Alt.
Click **Quick Edit** in the Pad Group section; every pad then shows its group letters. Click the SAME Mute Group letter on the
closed-hat pad and the open-hat pad (the manual's example uses letter B for a Mute Group and G for an Alt Group; so A to C are
probably the Mute letters, D to F Link, G to I Alt. That split is my inference from the example, so read the letters on screen).
Click Quick Edit again or press Esc to leave. An **Alt Group** makes the pads in it fire in random order, so no two hits match.
Fast rolls: each pad answers three MIDI keys in the C3 to B6 range, so you can play or draw quick repeats.

**Industrial deep house** (web: Reason Studios, 2025): low kick with a long "subby" tail, four on the floor, short metallic
hats, shakers for movement, a clap with a long tail. Send a half-speed noise clap through a delay (high feedback) and raise
the delay's dry/wet over the loop for a build. Parallel: an RV7000 for space and a Scream 4 for scuzz via a Spider split.

## 7. Idea for later (not tested)
One Combinator holding Redrum, per-drum Mix Channels, an Output Bus, Master Bus Compressor (Mix) and Scream 4 (parallel), with
macro knobs Glue (Comp Threshold), Parallel (Mix), Grit (Scream Damage Control), Space (reverb send). Cables to anything
outside a Combinator are not saved, so keep all of it inside.

## Go deeper (files in the Homeroom Studio project folder; skip if they are not there)
`docs/reason/techniques/drums.md` (same material with source URLs), `docs/reason/manual-digest/drum-devices.md` (Kong, Redrum
and Dr. Octo Rex in detail), `docs/reason/techniques/bass-and-low-end.md`, `docs/reason/manual-digest/routing-and-main-mixer.md`.

=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:docs/reason/skill-benchmarks-2026-10-01/skills/reason-mixer-chains/SKILL.md
=====================================================

---
name: reason-mixer-chains
description: Exact click-by-click routing for Reason 12.7's main mixer. Insert chains, send effects (shared reverb or delay), Output Buses (drum or vocal sub-mixes), Parallel Channels, kick-ducking sidechain, de-essing, gating a pad from a drum loop, recording THROUGH effects (Rec Source), stems, and master-section order. Use whenever the owner asks how to connect, route, bus, group, duck, sidechain, parallel-compress, send to a reverb, "build a chain", record with effects baked in, or why a cable or effect isn't doing anything in Reason, even if he never says "mixer". Reason 12.7 only; nothing in it has been heard.
---

# Reason 12.7 mixer chains: how to build and control them

Source: Reason 12.7 Operation Manual ch. 16 (routing) and ch. 17 (main mixer), plus web notes. Nothing here has been heard
in Reason, so every setting is a starting point. Say that once, briefly, in the answer.

## How to answer
- Plain words, short numbered steps, one action per step, exact button and menu names. He wants "what do I click", not theory.
- Fit the length to the question: one narrow question gets about 250 words or fewer. Give the steps for what he asked, then stop.
  Offer the next recipe in one line instead of writing it out.
- Say the cheapest working method first. If two methods exist, name both in one line and say which to try first.
- Mark what you are sure of: steps from the manual are fine to state; anything from the web or your own idea gets one short
  "not tested" flag. Do not dress a guess up as a fact.
- Reason **12.7 only**. The web is full of Reason 13 and 14 tutorials. These are NOT in 12.7: Sidechain Tool, Gain Tool,
  Stereo Tool, Ripley, RV-9, Track Panel, Rack per Track. Do not tell him to use them. Use the 12.7 way below, and if the
  only good answer needs one, say "that needs Reason 13/14" instead of inventing a substitute.
- Parameter names: never type one from memory. A name that is slightly wrong does nothing and gives no error. Copy from
  `device_refs/<device>.md`, or look in `docs/reason/remote-vocab.json` (`tools/reason_vocab.py --device "<name>"` does the
  same but only runs on the Mac with Reason installed).
- Two spellings exist for some controls. When telling him what to CLICK, use the panel label from the manual ("Filters To Dyn S/C").
  When writing a remote map or automation, use the Remote name from `remote-vocab.json` ("Filters Dyn S/C").

## The one rule that explains most routing surprises
**What is selected when you create a device decides where it connects.** Select first, then create.

| You create | While this is selected | What you get |
|---|---|---|
| Instrument | nothing | A new Mix Channel, already connected |
| Effect | An instrument | Inserted between that instrument and its Mix Channel |
| Effect | A Mix Channel or Audio Track | Goes into that channel's Insert FX |
| Effect | The Master Section | A **send** effect on the first free Send FX slot |
| Effect | Mixer 14:2 or Line Mixer | A send on its first free Aux Send/Return |
| Matrix or RPG-8 | An instrument | Note and Gate CV connect by themselves |

- Hold **Shift** while creating = no auto-routing at all.
- Wrong spot? Edit menu: **Auto-route Device** or **Disconnect Device**. **Shift-drag** a device to a new rack position to
  re-route it (this is how you change the ORDER of effects in a chain).
- Copy-paste and drag-duplicate do not auto-route unless Shift is held.
- **Made an effect with the wrong thing selected?** Deleting a device in the middle of a chain keeps its two neighbours
  connected, so delete it, select what it SHOULD hang from (the Master Section for a shared reverb or delay, then
  **Create Send FX**), and create it again. If cables look wrong afterwards, select the device and use **Auto-route Device**.
  A quicker patch is the effect's own **Dry/Wet** knob, but that only softens it.
- To see the cables: press **Tab** to flip the rack. Press **K** to hide clutter. Ctrl-click a jack for a menu that connects
  to any device ("new Mix Channel" is the first choice on an audio output).

## Recipes (all from the manual; steps in order)

### 1. Insert chain on one sound
1. Select the instrument (or the Mix Channel).
2. Create the effects one at a time, in the order the sound should pass through them.
3. To reorder, Shift-drag a device up or down the rack.
4. On a Mix Channel, **Show Insert FX** lets you drag devices in and out. **Clear Insert FX** removes all and leaves a straight
   connection.
5. Keep a chain you like: save it as an **Insert FX Patch** (a .cmb file) from the File menu's Export.

The channel strip already has its own gain (±18 dB), gate, compressor, EQ, high-pass and low-pass. Use those first and add
devices only for what the strip cannot do. Default order is dynamics, then EQ, then inserts. Buttons **Insert Pre** and
**Dyn Post EQ** change it.

### 2. Send effect (one reverb or delay shared by many)
1. Select the Master Section (or any channel), right-click, **Create Send FX...**, pick the device. Eight sends max.
   For vocals a good first pick is the **RV7000 MkII** on a plate setting (the device guide calls plate the vocal workhorse).
2. On each channel turn the matching **Send Level** knob up. That sets how much goes in.
3. Leave the Master Section **Return** knob near 0 dB. Change the effect amount with the channel send knobs.
4. **PRE** on a send means the channel fader no longer changes the send amount.
5. Reverb wants the effect at 100% wet. The dry sound is the channel itself.

### 3. Output Bus (one fader for a group, e.g. all drums)
1. Select the channels (Shift-click).
2. **Cmd+G** (Route to New Output Bus). A "Bus 1" channel appears.
3. Rename it, drag it next to the group. Put shared EQ, compression and sends on the bus channel.
4. Muting the bus mutes the sends of everything feeding it. Delete the bus and the channels return to the Master Section.

### 4. Parallel Channel (keep the dry sound, blend in a processed copy)
1. Select the channel or bus. Choose **Create Parallel Channel** from the Edit menu or the right-click menu. A "P1: name"
   channel appears, fed from the source's **Parallel Out** jacks.
2. Put the heavy effect in the P1 channel (for drums: turn its compressor on and raise the Ratio).
3. Blend with the P1 fader under the dry one.
4. Need a second one? Make it from the last parallel channel (each source has one Parallel Out pair).

Easier first try: Channel Dynamics or Master Bus Compressor has a **Mix** knob. Below 100% is parallel compression with no cables.

### 5. Kick ducks the bass (sidechain)
1. Put the kick on its own channel first. A drum machine's kick shares a channel with the other drums until you split it.
   Kong: click the kick pad, set its **Drum Output** to 3-4 (bottom of the Drum and FX section), press Tab to flip the rack,
   Ctrl-click Kong's Audio Out 3-4 and pick "new Mix Channel". Kong's separate outs are never auto-routed. Redrum: Ctrl-click
   that drum's own output jack and pick "new Mix Channel" (that drum then leaves Redrum's main out, which is what you want here).
   More in `reason-drum-bus`.
2. On the bass channel turn its compressor **On**.
3. Cable the **kick channel's Parallel Out** to the **bass channel's Sidechain input** (back of the rack, flip with Tab).
4. The **KEY** light comes on by itself. The bass compressor now reacts to the kick. Lower Threshold and raise Ratio until the
   bass dips on each kick. If the ducking weakens when you pull the kick fader down, the Parallel Out may follow the fader.
   The manual does not say either way, so check it by ear (an open question, not a fact).
5. A rack compressor (Channel Dynamics with **Sidechain** on, Master Bus Compressor, MClass Compressor) works the same way
   through its own sidechain input.
6. Several targets: split with a **Spider Audio Merger & Splitter**, or put the targets on one Output Bus and key the bus.
If you plug a drum's own output jack straight into a sidechain, that drum leaves the main mix. Split it first.

### 6. De-ess a vocal (no extra device)
1. Vocal channel: turn its compressor on.
2. Turn on **Filters To Dyn S/C**. Now the HPF and LPF filter only what triggers the compressor.
3. Set the HPF high so only the "s" sounds trigger it, then raise Ratio. Set the numbers by ear.

### 7. Gate a pad with a drum loop
Cable the drum loop's output into the pad channel's **Sidechain input**, turn its gate on (KEY lights). The pad opens on each hit.

### 8. Record THROUGH effects (guitar through an amp, vocal through a chain)
Audio records DRY unless you do this, and the effects only apply on playback.
1. Make an Audio Track and a separate Mix Channel.
2. Put the effects (for example Scream 4 then RV7000) in the Mix Channel's Insert FX. For "compressor baked in", put a
   compressor DEVICE there (Channel Dynamics or MClass Compressor). The manual only promises that the Insert FX are
   recorded; it does not say whether that channel's own strip compressor and EQ are, so don't count on them.
3. Cable a Hardware Interface **Audio In** to the Mix Channel's **Input L** (back of the rack).
4. Press **Rec Source** on the Mix Channel.
5. Set the Audio Track's input to that Mix Channel and arm only the Audio Track.
6. You will hear the processed input live. If you don't want that, mute the Mix Channel in the Main Mixer. (The manual's own
   advice for its guitar example.)

### 9. Record a sub-mix or stem
Mix the parts on an Output Bus (or use the Master Section), press **Rec Source** on it, and make that the Audio Track's input.

### 10. Own send levels per Redrum drum
Make two extra Mix Channels named "FX 1 Chaining" and "FX 2 Chaining". Turn on one Send FX bus on each with PRE on, pull their
faders to zero, and cable Redrum's Send Out 1 and 2 into them.

## Master Section (the end of every chain)
- The Master Compressor sits in the Master Section: Ratio 2:1, 4:1 or 10:1, Attack 0.1 to 30 ms, Release up to 1.2 s or Auto,
  KEY for an outside sidechain. Master Inserts (a maximizer) come after it. Keep a limiter or maximizer last.
- Keep the Master Fader at 0 dB. Set listening volume with the **Control Room Out** knob.
- A sensible order to try (an idea, not tested): MClass Equalizer with Low Cut on, then Master Bus Compressor for 1 to 3 dB,
  then MClass Stereo Imager, then MClass Maximizer.
- Solo and mute follow the routing. Soloing a channel also solos the buses it feeds. Muting a bus lets you hear only the
  parallel path.

## Controlling it
- Automate a mixer knob: right-click it, **Edit Automation**. For an Audio Track, turn off normal record-enable first so you
  do not record audio by accident.
- Remote controls one channel at a time when the surface is locked to it. For many channels, lock the Master Section; the
  surface covers about 8 channels starting at the Remote Base Channel. The Remote bridge skill has the locking steps.
- A channel's **Gain Reduction CV** output (back of the rack) follows how hard its compressor works. It is an envelope
  follower, for example to move a filter. The manual says it exists; wiring it from a kick is an untested idea.

## Go deeper (project files, read only what you need)
- `docs/reason/manual-digest/routing-and-main-mixer.md`: full channel-strip numbers and every recipe above in more detail.
- `docs/reason/techniques/buses-sends-master.md`: insert vs send, depth with reverb, master-section notes with sources.
- `docs/reason/manual-digest/recording.md`: levels, loop recording, resampling.
- Vocal chains: skill `reason-vocal-chain`. Drum routing and drum bus: skill `reason-drum-bus`.

=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:docs/reason/skill-benchmarks-2026-10-01/skills/reason-vocal-chain/SKILL.md
=====================================================

---
name: reason-vocal-chain
description: How to record, process and place a vocal in Reason 12.7 with stock devices. Insert chain order and starting settings (EQ, de-ess, two-stage compression), reverb and delay on sends, doubles and backing-vocal buses, Neptune pitch correction (natural vs robot, octave dub, harmonies) and the BV512 vocoder. Use whenever the owner asks for a vocal chain, "make my vocal sit", rap or singing vocal mixing, de-essing, vocal reverb or slapback, doubling, auto-tune or Neptune, vocoder or robot voice, or asks how to get a vocal "radio ready" in Reason. Reason 12.7 only; nothing has been heard, so settings are starting points.
---

# Reason 12.7 vocal chain

Sources: Reason 12.7 Operation Manual (ch. 6, 17, 52, 54, 57 to 61), a Reason Studios vocal-chain article written for Reason
13, Reason Studios articles on reverb and delay, and r/reasoners threads. Nothing here has been heard on this machine.
Tell him once, briefly, that the numbers are starting points to adjust by ear.

## How to answer
- Plain words, a short numbered chain, exact device and knob names. Say what each step is FOR in half a sentence, so he can
  decide whether to skip it.
- Fit the length to the question: one narrow question (just Neptune, just the vocoder) gets about 250 words or fewer. A full
  chain can be longer. Offer the next section in one line instead of writing it out.
- Reason 12.7 only. The Reason 13 and 14 devices that web tutorials use are NOT in 12.7: Gain Tool, Stereo Tool, Sidechain
  Tool, Ripley, RV-9. Use the 12.7 substitutes in the table. If a tip needs one of them, say "that is a Reason 13/14 device".
- Never type a knob name from memory. Copy from `device_refs/<device>.md` or `docs/reason/remote-vocab.json`
  (`tools/reason_vocab.py` does the same but only runs on the Mac with Reason installed). A near-miss name fails silently.
  Some controls have a panel label in the manual and a different Remote name: use the panel label when telling him what to
  click ("Filters To Dyn S/C", "HF Emph"), and the Remote name when writing automation or a remote map ("Filters Dyn S/C",
  "HF Emphasis").
- Mark each setting: manual, web (one person's opinion), or your own idea. Do not present a guess as a rule.

## Order of work (do not start mixing before steps 1 and 2)
1. **Record clean and dry**, peaks around -12 dB. A hot or distorted take can't be fixed later. Audio records DRY in Reason
   anyway; to hear effects while singing, route through effects as in `reason-mixer-chains` recipe 8.
2. **Comp the takes**: pick the best one, punch over single bad words.
3. **Tidy the audio**: even out loud and quiet words clip by clip, remove breaths you do not want, tune with Pitch Edit.
4. **Insert chain** (below).
5. **Sends**: a plate reverb and a delay.
6. **Doubles and backing vocals** on a bus.

## The insert chain (stock 12.7 devices; many small moves beat one big one)
The mixer channel strip already has input gain, gate, compressor, EQ, HPF and LPF, and processes them in the order Dynamics,
then EQ, then Insert FX (the **Insert Pre** and **Dyn Post EQ** buttons change that). The rack devices **Channel Dynamics** and
**Channel EQ** are the same circuits as devices. The order below is the order the sound travels.

| # | What | Starting point | Why |
|---|---|---|---|
| 1 | **Input Gain** (±18 dB, strip) | Level the signal going in. After any big EQ move, level-match again | Fair comparisons: louder always sounds better, so match level before you judge |
| 2 | **De-ess** (mono vocals; strip) | Strip compressor On, then **Filters To Dyn S/C** On, HPF set high so only "s" sounds trigger it, raise Ratio | Before the other compressors, so "s" does not trigger them. The strip's compressor comes first anyway |
| 3 | **Channel EQ device, HPF On** (Insert FX) | About 60 to 100 Hz | Removes rumble and plosive thumps. Use the DEVICE here: with Filters To Dyn S/C on, the strip's own HPF and LPF filter the compressor trigger, not the sound (the manual says those buttons are then unavailable in the Spectrum EQ window) |
| 4 | **MClass Equalizer** (cut mud) | Low shelf cut near 150 Hz, 6 to 8 dB. Boost a narrow band, sweep 300 to 500 Hz, find the ugly spot, turn it into a cut of about 3 dB | Cutting beats boosting |
| 5 | **Channel EQ device** (tone; can be the same device as step 3) | Presence boost 3 to 4 kHz, wide Q. Air: high shelf +3 to 4 dB from about 8 kHz | Clarity |
| 6 | **Channel Dynamics** (comp 1) | Ratio 2:1, about 2 dB of reduction, **Comp Peak On**, shortish Release | Catch peaks gently |
| 7 | **MClass Compressor** (comp 2) | 2:1 again, about 2 dB more | Two gentle stages sound less squashed than one at 6 dB |
| 8 | **Scream 4** (optional, parallel) | Tube or Tape, low **Damage Control**. Pull **Cut Lo** down | Body and warmth without losing the clean take |

- Watch the gain-reduction meter, not the knob positions.
- People disagree on EQ before or after the compressor. Pick one, then flip it and compare.
- Compress with **Mix** under 100% on Channel Dynamics for built-in parallel compression.

## Width and space (the lead stays centered and mono)
- **Reverb on a send, not an insert.** Plate suits vocals. More send plus lower fader = farther away. Less send plus higher fader
  = closer. Cutting the reverb's own lows (RV7000 EQ page) keeps it from muddying the mix. Predelay about 20 to 40 ms keeps
  words clear.
- **Delay with ducking**: **The Echo** on a send at 100% wet, **Ducking** on, so repeats drop while he sings and rise in the gaps.
- **Slapback plus a plate** is a common lead setup.
- **Width** comes from the sends, not from widening the lead. The MClass Stereo Imager can't widen a mono signal. For a stereo
  delay, The Echo's **Right Ch Time Offset** gives a left/right time difference (an idea adapted from a 13/14 tool; not tested).
- **PRE** on a send keeps the effect level steady when you ride the vocal fader.
- Send steps: `reason-mixer-chains` recipe 2.

## Doubles, harmonies, backing vocals
- **Dub** (Transport) copies a track including its insert effects, so every layer gets the same chain.
- Route all doubles to one **Output Bus** (select channels, Cmd+G) and put shared effects on the bus once.
- Use the best take loud, and 2 to 3 other takes very quiet beneath it. If it sounds like several voices, it is too loud.
- Line doubles up with Slice Edit.
- Print a backing-vocal stem: Rec Source on the bus (see `reason-mixer-chains` recipe 9).

## Neptune (pitch, harmony, octave) manual ch. 54
Control names below are the Remote names (`device_refs/neptune.md`): **Pitch Adjust On/Off**, **Correction Speed**,
**Preserve Expression**, **Formant On/Off**, **Formant Shift**, **Transpose On/Off**, **Semitones**, **Cent**.
- **Natural tune**: Neptune as an INSERT. Pitch Adjust On, set the key and **Scale**, **Correction Speed** around the middle
  (the device guide says the middle sounds natural; turning it up gives the stepped robot sound), **Formant On** so notes keep
  their character. **Preserve Expression** keeps the singer's own vibrato during fast correction.
- **Hard robot tune**: Correction Speed to max, **Preserve Expression** to minimum.
- **Fix only the flat bits**: give Neptune a sequencer track and automate its **Pitch Adjust** button On only for bad passages.
- **Change the singer's character**: Pitch Adjust and Formant on, move **Formant Shift** down (deeper) or up.
- **Octave dub**: a SECOND Neptune on a SEND (the insert keeps doing the natural tune), Pitch Adjust OFF, Transpose ON,
  **Semitones** +12, Formant On, balance with the channel's send knob until it is barely there. Idea, not tested: automate that
  send level so the double is only up in the chorus.
- **Harmonies**: Neptune as an insert, send MIDI to the **Voice Synth** (from its track or a keyboard); the Voice Synth jacks
  can feed their own Mix Channel.
- Robotic by accident? Back Correction Speed off from its maximum, check the Scale matches the song, keep the Formant section
  on. (Not a manual step; it follows from the two settings above. Try it by ear.)

## BV512 vocoder (manual ch. 52)
- Needs two signals: a **carrier** (a bright, sustained synth such as a Subtractor sawtooth with the filter fairly open) and a
  **modulator** (his voice). With no notes played on the carrier you hear nothing.
- Setup: create the carrier synth, select it, create a BV512 (it auto-inserts via the Carrier jacks). Patch the audio interface
  input to the **Modulator Input** on the back (Ctrl-click the jack, or flip the rack with Tab). Master Keyboard Input on the
  carrier's track so you can play it. **Dry/Wet fully Wet**. Raise **HF Emph** (Remote name HF Emphasis) if muddy.
- To print the result: Rec Source on the vocoder's Mix Channel, a new Audio Track with that as its input, arm only the Audio
  Track (`reason-mixer-chains` recipe 8 has the same pattern).
- Band count: fewer bands (4, 8, 16) sound more robotic, and one forum user finds they sit better in a mix than 32. Try 16
  first. **FFT** mode is clearest for speech and singing.
- To vocode an existing audio track, patch that track's left **Insert FX To Device** jack into the Modulator Input.
- A vocoder output is already in tune with the keys, so Neptune after it has nothing to fix.

## Go deeper
`docs/reason/techniques/vocals.md` (same material with source URLs and a Combinator-macro idea), `docs/reason/manual-digest/recording.md`
(levels, loop recording, comping), `docs/reason/manual-digest/audio-editing.md` (Slice Edit, Pitch Edit), device guides in
`device_refs/` (channel-dynamics, channel-eq, mclass-equalizer, mclass-compressor, scream-4, rv7000-mkii, the-echo, neptune, bv512).

=== END OF PART ===
