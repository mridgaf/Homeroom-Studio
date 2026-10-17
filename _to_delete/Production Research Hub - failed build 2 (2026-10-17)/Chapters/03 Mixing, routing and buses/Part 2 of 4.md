# Chapter 03: Mixing, routing and buses
## Part 2 of 4

_How to wire effects, buses and sends in Reason, plus the Reason 12 template and technique library (by genre and by type)._

**In this part:**
- routing-and-main-mixer.md — Routing and the Main Mixer: how to build and control chains (digest of manual ch. 16 and 17)
- delay-compensation.md — Delay Compensation (digest of Reason 12.7 manual, ch. 18)
- recording.md — Recording — audio (vocals), notes, automation
- audio-editing.md — Audio Editing in the Sequencer (digest of Reason 12.7 manual, ch. 8)

(Next: Part 3 of 4)


=====================================================
SOURCE FILE: routing-and-main-mixer.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/routing-and-main-mixer.md
=====================================================

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

=====================================================
SOURCE FILE: delay-compensation.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/delay-compensation.md
=====================================================

# Delay Compensation (digest of Reason 12.7 manual, ch. 18)

Source: `~/.reason_voice/reason12_manual/full_chapters/18-delay-compensation.txt` (manual pp. 501-516). Digested 2026-09-30.
Tag: all **Manual**. Nothing here was tried or heard. Index: [README](README.md)

## In one line
Some effects delay the sound a little. Delay Compensation delays every OTHER channel by the same amount so everything arrives together.
Without it, a channel and its parallel copy that runs through an effect sound phasey or smeared.

## Where the switch is
Three places, same setting: the **Delay Comp button** in the Master Section of the Main Mixer, on the **Transport panel**, and the **Options menu**.
The total delay shows as a number of samples next to it. Hover over the number to see milliseconds.
(The Quazmo demo song had it off: `demo-song-notes-quazmo.md`.)

## How it works (the 12-sample example)
Reason adds up the reported delay of every effect in each channel's chain. The channel with the biggest total gets nothing.
Every other channel gets extra silent delay to match. Four channels at 12, 12, 10 and 3 samples: the 10 gets +2, the 3 gets +9, the 12s get 0.
It recalculates by itself when you add or remove effects.

## What is compensated (standard setups only)
- Effects in series between an instrument and its Mix Channel.
- Insert FX inside a channel (between the To/From Insert FX jacks), including an Effect Combinator in there.
- Effects in series from a channel's **Parallel Out** to another channel.
- Any mix of those three (the delays are added up).
- Signals going from channels to the 8 Send FX buses are kept in step.
- The Metronome click, and bounces (to disk, to new tracks, Bounce in Place).

## What is NOT compensated
| Thing | What happens |
|---|---|
| Rack mixer (Mixer 14:2) channels | No compensation. Only the Main Mixer is covered |
| Channels using **Direct Outs** | Skipped. The channel's delay display shows " - " |
| The Send FX devices themselves | Their own delay is ignored (reverbs and delays hardly matter here) |
| Return channels fed from Send FX | Not compensated |
| **Master Insert FX** (maximizer, mastering EQ) | Not compensated, on purpose: everything passes through together. The Master Section has no Channel Delay display |
| Effects inside an **Instrument** Combinator | Not compensated (Effect Combinators are) |
| CV, MIDI, automation, MIDI Clock, Ableton Link | Not compensated. MIDI Clock Sync Offset can be set by hand |

## Odd routings: the red LED
Splits, feedback loops, cross-routing and effects wired outside the Insert FX section confuse it. Reason uses only the SHORTEST path
and ignores feedback loops and send effects inside the chain. A **red LED** in the Delay Compensation section on the back of the Mix Channel
or Audio Track lights up and a tooltip names the problem. "Could not calculate latency. The default value of 0 samples was used" means a cable is not fully connected.

## Setting it by hand
On the back of the Audio Track / Mix Channel, the unfolded Insert FX section has two displays: the effects' reported delay, and your manual adjustment.
You can only add to the reported figure, never go below it. Works only if the effects are in the Insert FX chain. Use it when a plugin reports its delay wrongly.

## Rules of thumb from the manual (for playing and recording)
1. **Playing an instrument live, or monitoring through Reason: switch Delay Comp OFF**, record, then switch it back on. Otherwise even a clean
   channel is delayed to match the slowest one.
2. Or bypass the Insert FX on the highest-delay channels, and the Master Insert FX, while recording.
3. Recording audio with External Monitoring: Reason moves the clip earlier by input + output latency, plus the Delay Comp total when it is on.

## Ideas for us (not built)
- A voice command "turn delay comp off for recording" (a Transport-panel button; whether the remote map can reach it is NOT checked).
- A line in any recipe that builds a parallel chain (parallel compression): "keep Delay Comp on, or the parallel copy phases."

=====================================================
SOURCE FILE: recording.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/recording.md
=====================================================

# Recording — audio (vocals), notes, automation
Source: Reason 12.7 Operation Manual, ch. 6 (whole chapter read, pp. ~140–174). Tag: **Manual**.
Mixer-side recording (Rec Source, sub-mix) is also in `routing-and-main-mixer.md` recipe I/J; the steps here are the fuller version.

## 1. Set up before you hit record
| Thing | What the manual says |
|---|---|
| Record Enable (red) | Audio: click it on the track. Any number of audio tracks at once. Instruments: only ONE note lane at a time (unless extra MIDI keyboards are locked to devices via Remote) |
| Record Enable Parameter Automation | Separate red button. Works on any number of tracks at once. Setting Master Keyboard Input to a track turns it on |
| Manual Rec (Track List) | Stops tracks auto-arming when selected. Use it when you move from recording audio to recording automation |
| Click (C) / Pre-count (Cmd+P) | 1–4 bars via Options. Manual tip: 3–4 bars for fast songs, 1–2 for slow. No pre-count with Ableton Link |
| Click Level | The click goes straight to the audio card, NOT through the mixer. A loud click can make the output meter clip |
| Save first | Manual: save the song before long or many audio recordings (shortens later save time) |

## 2. Input level (the vocal rule)
- Choose mono or stereo input + which interface input from the track's Audio Input drop-down.
- Aim for **about −12 dB** on the track Input Meter (first yellow LEDs) on a 24-bit interface. Raise a couple dB for 16-bit.
- Red clip LED stays lit until you click the meter. Never go past 0 dB.
- Set the level at the SOURCE (preamp / interface knob). The mixer channel strip does NOT change what is recorded.
- Recording Meter window (Windows menu › Show/Hide Recording Meter): big meter + tuner you can see from across the room.
- Built-in **Tuner** on the audio track (Enable Tuner button): for guitar, bass etc. The note must sustain a moment to be detected.
- Clip Safe is Balance-interface only (discontinued hardware). Skip.

## 3. Monitoring — the key vocal-chain fact
- The mixer channel (EQ, dynamics, insert FX, sends) is applied to what you HEAR, not to what is RECORDED to disk.
- So: you can monitor with compression and reverb on and still record the dry voice. Effects stay changeable later.
- Preferences › Audio › Monitoring: **Automatic** (armed = monitored, playback = not), **Manual** (you click Monitor), **External** (Reason never monitors; use the interface's direct monitor if latency is a problem).
- Latency too long? Monitor on the interface and set Reason to Manual/External.

## 4. Takes and comping
- **Loop-record**: set locators round the section, Loop on (L), go to left locator (the L button), Record. Each pass is stored as a **Comp Row** (Take). Earlier takes are silent but kept.
  - Last pass full length = Single Take clip (opens in Slice Edit; click Comp Edit). Stopped mid-clip = Comp Clip (opens in the Comp Editor).
  - Then pick best parts from each take. (Comp Editor steps are in `audio-editing.md`.)
- **Punch over an existing clip**: recording over it incorporates the old audio. Old = Take 1, new = Take 2 on Comp Rows, new part plays. Nothing erased. Fix a single line of a vocal this way.
- **Dub** (Transport button): new audio track copying the current track's settings INCLUDING channel strip and insert FX. Record stacked backing vocals/doubles, all play together.
- **New Alt**: same as Dub but MUTES the original. For alternative takes of the same part. Both work on the fly while recording.
- Lower the tempo to record a hard part. Audio stretches back to full tempo afterwards, pitch unchanged.

## 5. Record from inside Reason (resampling)
Steps in the manual for recording an instrument to audio:
1. Make the instrument track (so the keyboard plays it).
2. Make an audio track.
3. Press **Rec Source** on the instrument's Mix Channel in the rack.
4. On the audio track pick Stereo + that channel in the Select Audio Input list.
5. Select the INSTRUMENT track (Master Keyboard Input) and switch its Record Enable OFF.
6. Arm the AUDIO track only. Do NOT give it Master Keyboard Input.
7. Set level with the Mix Channel fader. Manual: instrument volume 0 dB + fader 0 dB is often best. Watch the audio track's Input Meter.
8. Record. Works for previously recorded note clips too.
- Same trick on an **Audio Track** device's Rec Source = re-record an audio track with its effects.
- **Output Bus** Rec Source = record a drum sub-mix.
- **Master Section** Rec Source + Solo the tracks you want + Stereo input = record a **stem** (e.g. 4 backing vocals panned and mixed to one track). Then un-solo and mute the originals so you don't hear them twice. You can ride faders live while recording.
- If you don't need live moves: **Bounce Mixer Channels** (see `audio-editing.md`/Song menu).

## 6. Notes
- Instrument track: arms itself and takes Master Keyboard Input. Clip edges snap to the nearest bar.
- Loop-record notes = each pass ADDS notes (layering a drum pattern).
- Delete/Backspace while recording a note clip = deletes it and starts a fresh one at the current position, still recording.
- Recording over a note clip adds notes. Starting before the clip and running into it makes a new clip that swallows the old one. Masked events inside the swallowed part are permanently deleted.
- Cleaner way to overdub: **Dub** (extra note lane, all play) or **New Alt** (extra lane, previous muted). With Loop on, Alt splits and mutes only the clip between locators.
- **Q Record** button quantizes as you play.
- Players can generate notes while you record (see `players.md`).

## 7. Automation recording
Two kinds:
| Kind | Where it lives | Use for |
|---|---|---|
| Performance controllers (pitch bend, mod wheel, sustain, aftertouch, breath, expression) | Inside the note clip, moves with it | Part of the performance |
| Track parameter automation | Own lane per parameter, own clips | Mixing and sound design (filter sweep, fade) |
- Optional middle path: Options › **Record Automation into Note Clip** records ANY instrument knob into the note clip (self-contained clip, less overview). Track automation wins if both exist for the same knob.
- Topmost note lane wins when two overlapping lanes automate the same controller.
- **Set the static value first** (the value the knob should have everywhere it isn't automated), then record the move. Clip ends → knob returns to the static value.
- Procedure: make sure the device has a track (Ctrl-click a knob › **Edit Parameter Automation** makes one for mix channels/effects) → arm Automation → Record → move knobs. One lane per knob appears. Master Keyboard Input is not needed.
- Click Stop again or the **Automation Override** light to show the green borders.
- Punch in: record again, and as soon as you move the knob the Override light comes on and new values replace old. Click Override to hand control back to the lane.
- Grab an automated knob during playback = Live mode override. Override light resets it.
- Mute one lane with its On button to hear the static value.
- Loop recording automation: each pass replaces the previous values.
- Spectrum EQ window moves can be recorded too.
- **Pattern automation** (Redrum, Matrix, Dr. Octo Rex): arm automation, pattern "Enable" on, set start pattern, record, change Bank/Pattern buttons slightly BEFORE the bar line (change lands on the next downbeat). No static value: where no pattern clip exists, the device is silent. Afterwards "Convert Pattern Track to Notes" or Copy Pattern to Track for editable notes.
- **Tempo automation**: Option-click the Tempo display (selects Transport track + creates lane), record while changing tempo. Audio clips stretch to follow unless Stretch is disabled for the clip.

## 8. Recipe: record a vocal (all from Manual rules)
1. Interface input → Audio Track, mono. Level at the preamp to about −12 dB peaks.
2. Monitoring Automatic (or interface direct if latency).
3. Put compressor/reverb on the channel strip for the singer's headphones. They are not recorded.
4. Click + 2-bar pre-count. Loop the chorus, sing 4–5 passes.
5. Comp the best lines. Fix single words by punching over that spot.
6. Backing vocals: **Dub** per layer, then a Master-Section stem if you need to free tracks.

=====================================================
SOURCE FILE: audio-editing.md
ORIGINAL LOCATION: HS:docs/reason/manual-digest/audio-editing.md
=====================================================

# Audio Editing in the Sequencer (digest of Reason 12.7 manual, ch. 8)

Source: `~/.reason_voice/reason12_manual/full_chapters/08-audio-editing-in-the-sequencer.txt` (manual pp. 203-254). Digested 2026-09-30.
Tag: all **Manual**. Nothing here was tried or heard. Index: [README](README.md)
Overlap check: your notes mention Slice Edit only for Dr. Octo Rex slices (`device_refs/dr-octo-rex.md`) and Pitch Edit in one line
(`device_refs/neptune.md`). The audio-clip tools below are not written up anywhere else.

## The 3 ways to edit an audio clip (double-click the clip, or select it and press Return)
| Mode | For | Opens by default when the clip is |
|---|---|---|
| **Slice Edit** | Fix timing: move/stretch the detected hits (slices). Quantize audio. Turn it into a REX loop | Single Take with **Allround** or **Melody** stretch type |
| **Pitch Edit** | Fix or change the pitch of single-voice audio (vocals) | Single Take with **Vocal** stretch type |
| **Comp Edit** | Pick the best parts of several takes and join them | A **Comp** clip (made from several takes) |
Buttons for all three are in the Toolbar. Close an open clip with **Esc**. Cmd+E opens it in its default mode.
**Order of work:** comp first, then slice or pitch edit. Doing slices first and comping after wastes the slice work.

## First, set the Stretch and Transpose Type (Edit menu or the clip's right-click menu)
| Type | Use for | Formants |
|---|---|---|
| **Allround** | Full mixes, chords, anything with several notes at once | Move with the pitch |
| **Melody** | One note at a time (bass, lead) | Move with the pitch |
| **Vocal** | Voice | Kept, so the voice keeps its character |
Wrong type = bad-sounding stretch. **Enable Stretch** must be ticked on the clip (right-click menu) or stretch and quantize do nothing.
Reason also stretches twice: a quick version you hear at once, then a high-quality version in the background (the **Calc** meter on the Transport shows progress).

## Slice Edit: fix the timing of a recording
- Reason finds the hits and draws white **Slice Markers**. Drag a marker to move that hit; the audio each side stretches. Pitch does not change.
- **Speaker tool** (or hold Cmd with the Arrow tool): click a slice to hear it alone. It bypasses the mixer.
- Several markers at once: select them, drag the **Slice Group Handle**. A selected range stretches "accordion style" if you drag a marker inside it.
- Nudge with Cmd+Left/Right (snap step), +Shift (beat), +Option (tick). Turn Snap off (**S**) for fine moves. You can't drag a marker past its neighbour.
- **Quantize audio**: select markers, set Value (Amount, Random) in the Tool Window or Transport, Apply. Choosing **Shuffle** uses the ReGroove Global Shuffle value.
  Only the markers nearest the grid move; two markers never land on the same spot. Audio can be quantized only after recording, not while recording.
- **Split at Slices**: cuts the clip into separate clips at the chosen markers (to reverse one hit, or bounce each to a sample).
- **Revert All Slices**: puts every marker back.
- **Bounce Clip to REX Loop**: set markers where you want slices, trim the clip to a whole beat, then Edit > Bounce > Bounce Clip to REX Loop.
  The REX file lands in Song Samples > All Self-contained Samples. Double-click it to open it in a new Dr. Octo Rex. It exports as `.rx2`.
  To use it in another sampler, un-self-contain the song first.

## Pitch Edit: vocal tuning (opens a clip as "Vocal" type automatically)
| Move | How |
|---|---|
| Snap every note to the nearest exact pitch | Select notes (or none = all), click **Pitch Correct**, or Shift+Cmd+C. **Reset** undoes it |
| Change a note's pitch | Drag it up or down. Transpose switch: **Snap** (absolute semitones), **Jump** (default, keeps your fine tuning), **Fine** (cents). Shift+Cmd while dragging = fine |
| Hear the note while dragging | **Monitor** button (a steady reference tone) |
| Straighten wobble or vibrato | Lower the note's **Drift** handle (100% = untouched, 0% = no drift). **Preserve Expression** keeps small natural movements |
| Smooth the jump between two notes | **Transition** handle. Only matters after you've changed pitches. Max 200 ms, or half the note if it is under 400 ms |
| Change tone without changing pitch | **Formant** in the Inspector: -1 to +1 octave in 0.01 semitone steps. Down = deeper, up = brighter |
| Per-note level | Note Level handle, or Inspector: -inf to +18 dB |
| Move a note's timing | Drag its handle in the Clip Overview (neighbours stretch). Option-drag a note line to move the start WITHOUT moving the audio |
| Split / join notes | **Razor** splits, **Eraser** joins (the notes are re-analyzed) |
| Everything numeric | Inspector: Position, Note, Fine-tune (1 cent steps), Drift, Preserve, Transition, Formant, Level. **Match Value (=)** copies one note's setting to the others |
| Undo everything | **Revert All Notes** re-analyzes the clip from scratch |
Quantize in Pitch Edit moves note STARTS, not drum-style hits. Related device: Neptune (`device_refs/neptune.md`).

## Comp Edit: make one perfect take from many
- Every take recorded in Loop Mode (or recorded over an existing clip) is a **Comp Row**: newest on top. Only one plays at a time unless you comp.
- If a **Single Take Mode** button is down, click it to deselect before adding cuts.
- **Razor tool**: click a Comp Row = cut there and use that row from that point on; click the **Silence Row** = silence from that point (cut breaths and noise);
  click the **Cut Row** = cut without changing the take. **Swipe** the Razor along a row to assign a whole segment. Hold Option while clicking to first duplicate the row.
- Change which take plays in a segment: double-click that row between the cut lines. Or Cmd+Up/Down; Cmd+Option+Shift+Left/Right moves segment focus.
- **Crossfades** at cuts: select the cut and drag its Crossfade Handle right (all the way left removes it). Match Value copies one crossfade to every cut.
- **Move a cut**: drag its handle (the recording stays put, only the mask moves). Two cuts can't share a spot.
- **Fix a take's timing**: select the row, drag it, or type the **Recording Offset** (240 ticks per 16th, 16 subticks per tick). Nudge with Cmd+arrows.
- **Row Level** fader per take; **Transpose** per row in the Inspector.
- **Bounce** button: joins the comp into one new recording (marked "(bounced)"), and the clip becomes Single Take. Needed before Slice Edit or stretch.
- **Delete Unused Recordings** shrinks the file, but it is permanent. Then File > **Save and Optimize** to actually shrink the song file.

## Functions that work on any audio clip
| Function | What it does |
|---|---|
| **Normalize Clips** | Makes a new top row "(normalized)" with the peak at 0 dB. Originals kept. Boosts noise too |
| **Reverse** | New top row "(reversed)". Originals kept |
| **Transpose clip** | Up or down 12 semitones in 1-cent steps, non-destructive, Inspector. Works on chords too |
| **Scale Tempo** | Option-drag a clip's resize handle: the audio stretches to fit the new length. Slices follow |
| **Bounce > Bounce Clip(s) to New Sample(s)** | Makes Song Samples you can open in the Edit Sample window and load into a sampler (see [sampling](sampling.md)) |
| **Bounce > Bounce Clip to Disk** | Exports one clip as WAV/AIFF for outside editing |
| **Bounce > Bounce Audio Clips To MIDI** | Single Take audio becomes a note clip on a new Subtractor track. **Vocal** type gives real pitches. **Allround/Melody** gives all notes on C3 = a rhythm. Handy for **drums to MIDI** (then move the notes onto the right pads) |
| Drag a Single Take clip onto an Instrument track | Same MIDI conversion in one move (one instrument track per audio track, right below it) |

## Match an imported loop to the song tempo
- Files exported or bounced from Reason carry their tempo, so they stretch to fit by themselves.
- A loop with a steady but unknown tempo: (1) **Disable Stretch** on the clip, (2) change the song tempo until it matches the loop (use the click), (3) set the clip length to the loop,
  (4) **Bounce Clip to New Recording** (stores that tempo), (5) **Enable Stretch**, (6) set the song tempo back. Or just use Scale Tempo.

## Ideas for us (not built)
- Skill idea **reason-audio-editing** (or three small ones: slice, pitch, comp). Highest value for you: **drums to MIDI**, **audio to REX**, **vocal pitch edit**, **comping takes**.
- Pairs with [sampling](sampling.md) and `device_refs/dr-octo-rex.md`.
- Not checked: the Key Commands for Comp/Slice modes in [key-commands](key-commands.md) (covered there).

=== END OF PART ===
