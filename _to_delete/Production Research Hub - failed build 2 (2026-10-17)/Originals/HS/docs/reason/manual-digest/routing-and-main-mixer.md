# Routing and the Main Mixer: how to build and control chains (digest of manual ch. 16 and 17)

Sources: `16-routing-audio-and-cv.txt` (manual pp. 429-440), `17-the-main-mixer.txt` (pp. 441-500) in `~/.reason_voice/reason12_manual/full_chapters/`.
Digested 2026-09-30. Tag: all **Manual** unless marked. Nothing here was tried or heard. Index: [README](README.md)
Overlap check: your notes cover the demo songs' wiring and a few mixer facts, but not the channel-strip numbers, the auto-routing rules, buses or parallel channels as how-tos.

## Part 1: how cables work (ch. 16)

| Signal | Jack | Notes |
|---|---|---|
| **Audio** | Big quarter-inch jacks | Cable colors: instrument to mixer = red, effects = green, CV = yellow, Combinator = blue |
| **CV / Gate** | Small mini jacks | CV modulates a value. Gate is on/off plus a value (like velocity). Only output-to-input |
| **P-LAN** | No cable. Shown as the **Audio Output** label on Mix Channel and Audio Track | Carries channel to Master Section or to an Output Bus. **Using the Direct Out jacks breaks it** (shown as red dashes) |
| **MIDI** | No cable | Comes from the device's sequencer track. Other ways: Remote, MIDI Out device |
Cable tricks: **Tab** flips the rack. **K** (or Options > Reduce Cable Clutter) shows fewer cables. Hover a jack to see what it connects to. Click-hold or Ctrl-click a jack >
**Scroll to Connected Device**. Ctrl-click a jack > pop-up menu connects to any device (the first item on an audio output is "new Mix Channel", good for sending Kong or Redrum
outs to separate channels; * = already used). Drag a cable end off a jack to disconnect. **Disconnect Device** clears all of a device's cables.

### Auto-routing: what happens depends on what is SELECTED when you create a device
| You create... | With this selected | Result |
|---|---|---|
| Instrument | nothing (or a used Mix Channel) | New Mix Channel, connected. If created right under an empty Mix Channel, uses that one |
| Instrument | Mixer 14:2 or Line Mixer | First free mixer inputs |
| Effect | An **instrument** | Insert between the instrument and its Mix Channel (distortion, compression, modulation) |
| Effect | A **Mix Channel / Audio Track** | Insert FX inside that channel |
| Effect | The **Master Section** | Send effect on the first free Send FX (use the Insert FX container for a master insert) |
| Effect | A Mixer 14:2 / Line Mixer | Send effect on the first free Aux Send/Return |
| Matrix | An instrument | Note + Gate CV go to its Sequencer Control inputs automatically |
| RPG-8 | An instrument | Note, Gate, Mod Wheel and Pitch Bend CV auto-connect |
- **Hold Shift while creating** = no auto-routing.
- **Auto-route Device** / **Disconnect Device** (Edit menu) redo a device's routing. **Shift-drag** a device to a new rack position = re-routes it (this changes effect ORDER in a chain).
- Deleting a device in the middle of a chain keeps the two neighbours connected. Moving a device keeps its cables. Copy/paste or drag-duplicate does NOT auto-route unless Shift is held.
- Old (Reason 5 or earlier) song: delete Mixer 14:2, Select All, **Auto-route Device** = one Mix Channel per instrument.
- **Sequencer Control** inputs (Subtractor, Thor, Malstrom, NN-19, NN-XT) are mono and meant for Matrix/RPG-8 notes. For modulating many voices, use other CV inputs.
- Every CV input has a **Trim knob**: clockwise = more modulation (full = 100% of the range). Counter-clockwise all the way = none.
- CV into a Combinator's rotaries lets CV drive almost any parameter inside it.

## Part 2: the channel strip (ch. 17). Same on Mix Channel and Audio Track

Default order of processing: **Dynamics > EQ > Insert FX**. Signal Path buttons change it: **Insert Pre** (inserts first), **Dyn Post EQ** (EQ first), both = Insert, EQ, Dynamics.

| Section | What is in it (numbers) |
|---|---|
| **Input** | Gain +/-18 dB, INV (phase invert; fixes hollow sound when two mics add up) |
| **Compressor/limiter** | Ratio 1:1 to infinity, Threshold -52 to 0 dB (auto make-up gain), Release 100-1000 ms, **PEAK** (instant detection, for drums), **FAST** (attack fixed at 3 ms for 20 dB). Soft-knee |
| **Gate/expander** | Range 0 to -40 dB, **EXP** (expander instead of gate), Threshold, Release 100-1000 ms, **Hold** 0-4000 ms, FAST attack 100 microseconds per 40 dB vs 1.5 ms normal. Close threshold is a bit lower than open threshold |
| **EQ** | HF shelf (1.5-22 kHz), HMF (600 Hz-7 kHz), LMF (200 Hz-2 kHz), LF shelf (40-600 Hz), all +/-20 dB. Q 0.70-2.50 on the two mids. **E button** = constant bandwidth. Bell buttons turn the shelves into peaks. **LPF** 100 Hz-20 kHz (12 dB/oct), **HPF** 20 Hz-4 kHz (18 dB/oct) |
| **Spectrum EQ window** (F2) | Drag the EQ points on a live analyzer. Cmd-click a point = 0 dB. Option-drag = Q. Shift = one direction only. Shows the signal BEFORE the fader |
| **Insert FX** | Bypass button, Edit Inserts |
| **FX Sends 1-8** | On, Level, **PRE** (tap before the fader so the fader doesn't change the send) |
| **Fader** | Pan (-3 dB compensated), **Width** (127 = full stereo, 0 = mono), Mute, Solo, Level, meter, Output Bus selector |
| CV on the back | Level CV and Pan CV (Programmer section), **Gain Reduction CV out** (an envelope follower: use it on a filter for auto-wah), Sidechain inputs |
Mixer Mute/Solo are not the same as sequencer-track mute/solo. Select several channels and moving one fader moves all of them by the same dB.

### Master Section
- **Master Compressor**: Threshold -30 to 0 dB, Ratio 2:1 / 4:1 / 10:1, Attack 0.1/0.3/1/3/10/30 ms, Release 0.1/0.3/0.6/1.2 s or **Auto**, Make-up -5 to +15 dB, KEY for external sidechain.
- **Master Inserts** (maximizer, mastering Combinator) sit AFTER the Master Compressor by default. "Inserts Pre Compressor" flips it. A limiter/maximizer should stay last.
- **FX Send 1-8 / Return 1-8**: leave master levels at 0 dB; change the effect amount with each channel's send knob. Return has Pan and Mute.
- **Master Fader** should stay at 0 dB. Monitor level goes on the **Control Room Out** knob (patch Ctrl Room Out to a spare interface output pair). Control Room can listen to Master, any Send bus or any Return bus.
- **Dim -20 dB** button, **Mute All Off / Solo All Off**, **Delay Comp** button (see [delay-compensation](delay-compensation.md)).

## Part 3: chain recipes built from the manual (each tagged Manual; all untested)

### A. Insert chain on one sound
Select the instrument, create the effects one at a time; they chain instrument > effect 1 > effect 2 > Mix Channel. Or select the Mix Channel and create effects: they go in its **Insert FX** container (click **Show Insert FX** to drag devices in/out). Reorder with Shift-drag in the rack. Effect Combinators can be dropped into the Insert FX container, several in series. **Clear Insert FX** removes the lot and leaves a straight-through connection.
### B. Send effects (reverb/delay shared by all)
Select a channel or the Master Section > right-click **Create Send FX...** > pick a device or Effect Combi (max 8). Use the channel's Send Level knobs. Edit buttons in the Master Section jump to the effect. A bus follows its Output Bus level (sends scale automatically unless PRE is on).
### C. Drum sub-mix (Output Bus)
Select all drum channels > **Cmd+G** (Route to > New Output Bus). A "Bus 1" channel appears (red fader knob). Rename it "Drum Mix" and drag it next to the drums. Muting a bus mutes the sends of what feeds it. Delete the bus and the channels go back to the Master Section. A bus can feed another bus.
### D. Parallel channel (keep the dry sound, add a processed copy)
Select the channel > **Create Parallel Channel** > a new "P1: <name>" Mix Channel is fed from the source's **Parallel Out** jacks. Put effects in the parallel channel's Insert FX, mix with its fader. Make more from the LAST parallel channel (each source has one parallel out pair). 
**Parallel drum compression (manual's example):** drums > Cmd+G for a bus > select the bus > Create Parallel Channel > turn on the P1 channel's compressor, raise the Ratio high > bring up its fader under the dry bus.
### E. Sidechain ducking from a kick
Take the kick channel's **Parallel Out** and cable it to the bass channel's **Sidechain input**. The **KEY** light comes on by itself and the bass compressor now reacts to the kick. For several destinations: tap an Insert FX "To Device" out, use a **Spider Audio Merger & Splitter** to split the signal, or put the targets on one Output Bus and feed the bus's sidechain. (Your own notes found a Redrum silent-kick trigger and an Output-Bus-with-curve method in the demo songs: see `demo-song-template-and-automation-ideas.md`.)
### F. De-essing a vocal (no extra device)
On the vocal channel turn on the compressor, then **Filters To Dyn S/C** (in the Input/EQ section). The HPF/LPF now filter only the signal that triggers the compressor. Set the HPF high so only the "s" sounds trigger it. Caveat from the manual: with Filters To Dyn S/C on, the HPF and LPF buttons are not available in the Spectrum EQ window, and the filters now serve the trigger, not the sound, so cut rumble with an EQ device instead. (Manual describes the method; the numbers are for you to set by ear.)
### G. Rhythmic gate effect on a pad
Cable a drum loop's output into the pad channel's **Sidechain input**; with the gate on (KEY on) the pad opens with the drum hits.
### H. Redrum with its own send levels per drum
Make two extra Mix Channels ("FX 1 Chaining", "FX 2 Chaining"), switch on one Send FX bus each with PRE on, pull the faders to zero, and cable Redrum's Send Out 1 and 2 into them. Then each drum has its own send levels, and the Main Mixer's sends still work for everything else.
### I. Record WITH effects (guitar through an amp, or a vocal through a chain)
Make an Audio Track and a separate **Mix Channel**. Put the effects (for instance Scream 4 then RV7000) in the Mix Channel's Insert FX. Cable a Hardware Interface **Audio In** to the Mix Channel's Input. Press **Rec Source** on the Mix Channel. Set the Audio Track's input to that Mix Channel. Mute the Mix Channel if you don't want to hear it twice. Without this, audio records DRY and effects apply only on playback.
### J. Record a sub-mix onto one track
Mix several inputs on an Output Bus, press **Rec Source** on the bus channel, and choose it as the input of an Audio Track.

## Part 4: Solo, Mute and sends with buses and parallels (logic)
- Soloing a channel auto-solos the buses and parallels it must pass through (dim green) and auto-mutes the rest (dim red).
- Manually muting a bus lets you hear only the parallel path. Soloing a bus solos everything routed to it.
- Muting a bus mutes the Send FX outputs of what feeds it; muting only one parallel does not, unless all paths are muted.

## Part 5: controlling the mixer by Remote
- One channel at a time: lock the surface to that channel's device, or set Master Keyboard Input to its track.
- Many channels: select/lock the **Master Section**. The surface then covers about 8 channels starting at the **Remote Base Channel** (yellow arrow in the channel header). Change it with Edit > **Set Remote Base Channel** or buttons on the surface.
- Automate a mixer knob: right-click it > **Edit Automation** (creates the lane and track). For Audio Track strip parameters, turn off the normal Record Enable so you don't record audio.
- Your `reason-remote-bridge` skill already covers locking a device with the right-click menu (not Options > Surface Locking).

## Ideas for us (not built)
- Skill idea **reason-mixer-chains**: recipes A to J above as step lists for voice walkthrough.
- Recipe additions: "parallel drum compression", "kick ducks bass", "vocal de-ess", "record through effects".
