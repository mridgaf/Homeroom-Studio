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
