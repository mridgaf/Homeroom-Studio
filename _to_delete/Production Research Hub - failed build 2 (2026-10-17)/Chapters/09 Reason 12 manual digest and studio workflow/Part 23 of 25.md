# Chapter 09: Reason 12 manual digest and studio workflow
## Part 23 of 25

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- demo-song-notes.md (piece 2 of 2) — What the Street Phone demo song teaches
- demo-song-phrase-ideas.md — Phrase ideas from the demo songs (Street Phone A-E, Airplane F, Power G)
- demo-song-skill-ideas.md — Skill ideas from the demo songs (Street Phone, Airplane, Power, Qua z mo)
- demo-song-template-and-automation-ideas.md — Template and automation ideas from the demo songs

(Next: Part 24 of 25)


=====================================================
SOURCE FILE: demo-song-notes.md (piece 2 of 2)
ORIGINAL LOCATION: HS:docs/reason/demo-song-notes.md
=====================================================

### 8i. Correction to 8c (2026-09-30, Seen in real Reason)
8c said it was not checked whether Combinator front controls are remotable. They are: Reason's Remote exposes exactly **Rotary 1-4 and Button 1-4** per Combinator (Rotary 5-16 never answered), under those generic names, never the panel labels (Lo Drive, Reverb, Perc...). The voice app can now move them by number ("rotary 2 up 30 percent", "switch button 1 off", tried on a factory reverb Combinator). Phrases by label ("more reverb on the bass tonewheel") are not built; see DECISIONS 2026-09-30 item 30. Not tried on this song's Combinators (demo songs are read-only and I did not lock anything here).

### 8j. ORGAN 1 (Organ 1 insert, patch name "Organ & Choir"; Seen)
- Front: an "ID8 COMBINATOR" panel. Knobs Organ Level, Vox Level, Color, Reverb; buttons Organ Spring, Spring Length, Vox Flange, Vox Reverb (all lit). Programmer and Device buttons lit while I looked. **It is an ID8 Combinator**: the same patch name on Organ 2 was not opened (that one I only saw on the rack front, so the two are not confirmed identical).
- Inside (Devices): Combinator Mixer, a micromix "MIXER COPY 3" (channel 1 "ORGAN", channel 2 "CHOIR", channels 3-6 blank), RV7000 MkII "RV7000 COPY 2" (patch "ALL DarkStrsHall"), an ID8 "ORGAN" (Organ page, variation B "Perc"), MClass Stereo Imager "ORGAN IMAGE...", MClass Equalizer "ORGAN EQ CO...", MClass Compressor "ORGAN", an ID8 "CHOIR" (Strings page, variation D "Choir"), then a Choir Imager, Choir EQ, and two CF-101 choruses "CHOIR CRS L/R". Every name ends "copy 2" or "copy 3", so this was copied from another Combinator (**Guess**: the Organ 2 one).
- Key ranges (Editor list): both ID8s play the full keyboard C-2 to G8; **the Choir is transposed +12** (an octave up), the organ 0.
- Routing read, every row clicked:
  | Device | Source -> Target (min-max) |
  |---|---|
  | Mixer copy 3 | Organ Level -> Channel 1 Level (0-100); Vox Level -> Channel 2 Level (0-100); Reverb -> Aux Return Level (0-104); Vox Reverb (button) -> Channel 2 Aux Send (0-62) |
  | Organ EQ (M EQ) | Color -> Parametric 2 Frequency (0-1,000) |
  | Choir ID8 | Mod Wheel -> Volume (100-60, reversed) |
  | Choir EQ (M EQ) | Color -> Parametric 1 Frequency (1,000-615) |
  | Choir Crs L and Crs R | Vox Flange (button) -> Enabled (2 to 1, as shown) |
  | RV7000, Organ ID8, both Imagers, Organ Comp | none |
- Two buttons on the front (Organ Spring, Spring Length) have **no mapping in Organ 1's Editor rows** (Seen). Corrected by 8k: they drive an "Organ Echo" RV7000 that Organ 1 does not have, so on Organ 1 those two buttons do nothing I could find (**Guess**: Organ 1 was copied from Organ 2 and lost the device).
- Voice-app link (updates 8c, see 8i): its four knobs are the Combinator's Rotary 1-4 and its four buttons Button 1-4 to Remote, so "rotary 3" here would move "Color" (an EQ frequency in both EQs, in opposite directions: Organ 0 up to 1,000, Choir 1,000 down to 615).

### 8k. ORGAN 2 (Organ 2 insert, patch name "Organ & Choir"; Seen)
- Same ID8 COMBINATOR front as Organ 1 (Organ Level, Vox Level, Color, Reverb; Organ Spring, Spring Length, Vox Flange, Vox Reverb), mixer labelled "MIXER COPY 2", channels ORGAN and CHOIR. **Its device list is one longer**: an extra RV7000 MkII "ORGAN ECHO" (patch "Init Patch") sits between the Organ Imager and the Organ EQ. Names end "copy" or "copy 2" (Organ 1's end "copy 2" or "copy 3"), so Organ 2 is the older one (**Guess**).
- Key ranges same as Organ 1: both ID8s C-2 to G8, Choir +12.
- Routing read, every row clicked except the Choir Crs R (shown the same as Crs L by its panel; not opened):
  | Device | Source -> Target (min-max) |
  |---|---|
  | Mixer copy 2 | Organ Level -> Channel 1 Level (0-100); Vox Level -> Channel 2 Level (0-100); Reverb -> Aux Return Level (0-104); Vox Reverb -> Channel 2 Aux Send (0-62) |
  | **Organ Echo (RV7000)** | **Organ Spring (button) -> Dry/Wet (0-54); Spring Length (button) -> Spring Length (48-127)** |
  | Organ EQ (M EQ) | Color -> Parametric 2 Frequency (0-1,000) |
  | Choir ID8 | Mod Wheel -> Volume (100-60, reversed) |
  | Choir EQ (M EQ) | Color -> Parametric 1 Frequency (1,000-615) |
  | Choir Crs L | Vox Flange -> Enabled (2 to 1, as shown) |
  | RV7000 copy, Organ ID8, both Imagers, Organ Comp | none |
- So the four knob mappings match Organ 1; the two spring buttons only work here, because only this one has the Echo reverb to drive. Both use the Combinator's front controls, which the voice app reaches as Rotary 1-4 and Button 1-4 (see 8i).

### 8l. ORG 2 SQUASH (Organ 2 insert, patch name "Dance"; Seen)
- Front: the same four labels (Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input). Editor list names end "copy 2" (M Comp copy 2, M EQ copy 2, Stereo Imager copy 2, Maximizer copy 2).
- Routing read, all four rows: Comp Input -> Input Gain (0-127); EQ Bass Freq -> Parametric 1 Frequency (30-200); EQ Treble Amount -> Hi Shelf Gain (0-30); Stereo Imager none; Maximizer Input -> Input Gain (0-127). **Identical to Clap Squash (8g) and Org 1 Squash (8e).** So the "Dance" squash macro is one patch used three times (Clap, Organ 1, Organ 2; Kick Squash not opened yet).

### 8m. PAD PROCESSOR (WarmPad insert, patch name "Synth Processor"; Seen)
- Front: same as Beat Process (8a): knobs Filter Freq, Filter Rez, Reverb (green frame = automated), Dly; buttons Chorus (lit), Dly FX (off), Unison (off), Wide (lit).
- Editor list (11 devices, same order as Timb Process 8d): Compressor (M Comp), Imager (M Stereo), Mixer, Main Verb (RV7000), Delay L, Delay R, BP Filter (M EQ), Dly Verb (RV7000), Chorus, Unison, Filter.
- Routing read, all 11 rows clicked: Imager: Wide -> Enabled (2 to 1). Mixer: Reverb -> Channel 1 Aux 1 Send (0-127); Dly -> Channel 1 Aux 2 Send (0-127); Chorus (button) -> Channel 13 Mute (1 to 0, reversed); Dly FX (button) -> Channel 12 Aux 3 Send (0-64); Unison (button) -> Channel 1 Aux 4 Send (0-83). BP Filter (M EQ): Dly FX -> Enabled (2 to 1). Dly Verb (RV7000): Dly FX -> Enabled (2 to 1). Filter: Filter Freq -> Frequency (0-127); Filter Rez -> Resonance (0-127). Compressor, Main Verb, Delay L, Delay R, Chorus, Unison: none.
- **Identical to Timb Process.** Beat Process (8a) had a different list (a 14-channel mixer, different devices) but the same knob and button names. So far "Synth Processor" is one front used over two different insides: Beat Process, and Timb Process / Pad Processor as a matching pair.

### 8n. GUITAR QUESTION (Guitar question insert, patch name "Guitar question"; Seen)
- Front: knobs Delay Time, Gtr Decay and two unlabelled knobs; button Loudness (lit), three more unlabelled buttons. Only two knobs and one button carry labels here.
- Editor list (7 devices): Scream 1 (Scream), Line Mixer 1, Guitar1 (NN-XT), Guitar 7th (NN-XT), Guitar 12 (NN-XT), Delay 7, Delay 12. The three NN-XTs play the full keyboard C-2 to G8, no transpose (their names say what they are: a plain guitar, a 7th, and a 12-string, **Guess**).
- Routing read, all 7 rows clicked:
  | Device | Source -> Target (min-max) |
  |---|---|
  | Scream 1 | Loudness (button) -> Enabled (2 to 1, as shown) |
  | Guitar1, Guitar 7th, Guitar 12 (NN-XT) | Gtr Decay -> Amp Env Decay (-17 to 5), the same range on all three |
  | Delay 7 | Delay Time -> DelayTime (steps) (1-4) |
  | Delay 12 | Delay Time -> DelayTime (steps) (2-8) |
  | Line Mixer 1 | none |
- Reading: Delay Time sets two delays in step units over different ranges (1-4 and 2-8, so Delay 12 runs at twice Delay 7's steps; **Guess**), and Gtr Decay shortens or lengthens all three guitars together. The Scream turns on with the Loudness button.
- Voice link: this Combinator's two labelled knobs are Rotary 1 and Rotary 2 to Remote, Loudness is Button 1 (8i). (Correction, mine: I first wrote here that the NN-XT is not in the voice map. It is: `remote/ReasonVoice.remotemap` has an "NN-XT Advanced Sampler" scope with 17 controls, checked 2026-09-30. The old line in the bridge skill that says NN-XT has no bridge knobs is out of date. Amp Env Decay is its knob 2, so a locked NN-XT can be told "longer decay" directly; the NN-XT scope has not been measured or phrase-tested here.)

### 8o. DELUXE VOCAL FX CHAIN (insert under the Guitar question channel, patch name "Deluxe Vocal FX Chain"; Seen)
- Front: a factory "MULTI FX combinator" panel. Knobs Decay, Early Rvb Vol, Tail Volume, Delay Vol (**all four have green frames = automated**); buttons Long Dly Tail, Hi Damp (off), Hi EQ Boost (lit), Delay Color (lit). Programmer and Device buttons shown.
- Editor list (8 devices): Effect Mixer (Line Mixer), Short Hall RV 7000, Long Verb RV 7000, Delay L DDL-1, Delay R DDL-1, Delay M EQ, Chorus CF-101, Distributor (Spider Audio).
- Routing read, all 8 rows clicked (min-max as shown):
  | Device | Source -> Target |
  |---|---|
  | Effect Mixer | Early Rvb Vol -> Channel 1 Level (0-127); Tail Volume -> Channel 2 Level (0-127); Delay Vol -> Channel 3 Level (0-127) |
  | Short Hall (RV7000) | Decay -> Decay (0-74); Hi Damp (button) -> HF Damp (40-115); Hi EQ Boost (button) -> Hi EQ (-20 to 60) |
  | Long Verb (RV7000) | Decay -> Decay (85-125); Hi Damp -> HF Damp (45-120); Hi EQ Boost -> Hi EQ (-20 to 60) |
  | Delay L (DDL-1) | Long Dly Tail (button) -> DelayTime (steps) (2-3) |
  | Delay R (DDL-1) | Long Dly Tail -> DelayTime (steps) (3-4) |
  | Delay M EQ (M EQ) | Delay Color (button) -> Low Shelf Enable, Parametric 2 Enable, Hi Shelf Enable (each 0-1) |
  | Chorus, Distributor | none |
- Reading: one Decay knob sweeps two reverbs over **non-overlapping ranges** (Short Hall 0-74, Long Verb 85-125), so the same knob position gives a short hall in the lower half and a long verb in the upper half (**Guess** that this is a crossfade by range); the Effect Mixer levels are the three blends (early reverb, tail, delay). The four automated knobs mean the song moves this effect by automation lanes.
- Voice link: these four knobs are Rotary 1-4 and the four buttons Button 1-4 to Remote (8i). A phrase like "more delay" has no route to "Delay Vol" until labels exist (DECISIONS 2026-09-30 item 30).

### 8p. PICTURES OF MOMENTS (Pictures of Moments insert, patch name "Pictures of Moments"; Seen)
- Front: knobs Squash, Tremolo, Dirt, Unison Detune; buttons Long Release, Tremolo Spread (lit), No Pulveriser, Unison (all others unlit).
- Editor list (6 devices): Pulveriser, Unison, Mixer (Line Mixer), Hall Reverb (RV7000), Sine (Malström), Triangle (Malström). Both Malströms play the full keyboard C-2 to G8, no transpose.
- Routing read, all 6 rows clicked. Values here show **percent and on/off words** rather than raw numbers: 
  | Device | Source -> Target (min-max) |
  |---|---|
  | Pulveriser | Squash -> Squash (0%-100%); Tremolo -> Tremor to Volume (0%-100%); Dirt -> Dirt (0%-100%); Long Release (button) -> Release (15%-55%); Tremolo Spread (button) -> Tremor Spread (Off-On); No Pulveriser (button) -> Blend (100% to 0%, reversed) |
  | Unison | Unison Detune -> Detune (0-127); Unison (button) -> Enabled (2 to 1, as shown) |
  | Mixer, Hall Reverb, Sine, Triangle | none |
- Reading: a synth pad made of a sine and a triangle Malström through a Pulveriser (squash / tremolo / dirt). "No Pulveriser" is a bypass made by turning the Pulveriser's Blend to 0%.
- This Combinator's Editor shows the percentage scale, not 0-127, for the Pulveriser targets; Remote still reports its own controls as Rotary 1-4 and Button 1-4 (8i).

### 8q. SYNTH PROCESSOR (Pictures of Moments insert, rack label "SYNTH PROCE..."; Seen)
- Same "Synth Processor" front as 8a/8b/8m (Filter Freq, Filter Rez, Reverb, Dly; Chorus lit, Dly FX off, Unison off, Wide lit). Here the Reverb knob has **no** green frame (Pad Processor and Timb Process do), so this one is not automated.
- Editor list, same 11 devices in the same order as Timb Process and Pad Processor. Rows clicked: Imager, Mixer, BP Filter, Dly Verb, Filter (the others carry no mapping in the two earlier copies; Compressor, Main Verb, Delay L/R, Chorus, Unison not clicked here).
- Mappings match Pad Processor exactly: Imager: Wide -> Enabled (2 to 1); Mixer: Reverb -> Channel 1 Aux 1 Send (0-127), Dly -> Channel 1 Aux 2 Send (0-127), Chorus -> Channel 13 Mute (1 to 0), Dly FX -> Channel 12 Aux 3 Send (0-64), Unison -> Channel 1 Aux 4 Send (0-83); BP Filter: Dly FX -> Enabled (2 to 1); Dly Verb: Dly FX -> Enabled (2 to 1); Filter: Filter Freq -> Frequency (0-127), Filter Rez -> Resonance (0-127).
- **The "Synth Processor" is used at least three times with one inside (Timb, Pad, this), plus Beat Process with a different inside.**

### 8r. Where item 39 stands after the sixth pass (2026-09-30)
- Read so far in Street Phone: Beat Process, Timb Process, Org 1 Squash (earlier passes); Clap Squash, Bass Tonewheel, Organ 1, Organ 2, Org 2 Squash, Pad Processor, Guitar question, Deluxe Vocal FX Chain, Pictures of Moments, Synth Processor (today).
- Not read: Kick Squash (same "Dance" patch name as the other squash ones, probably identical, not confirmed), the vocal channels' Combinators higher up the rack (Main Vox, Middle 8 Vox, Chorus Vox inserts), Toxic Vocal, Vocal Khaba, and the master-section Combinators (Master Section FX, Default Mastering Suite). Right-hand jacks and Neptune settings on Middle 8 Vox also still open.

### 8s. MASTER SECTION COMBINATOR (rack label "MASTER SECT...", patch name "Init Patch"; Seen)
- Front: knobs Loudness Curve, EQ Boost Freq, Compression, Master Gain; buttons Stereo Imager On, EQ Boost On, Compressor On (lit), Punch. Inside: Combinator Mixer, then MClass Equalizer, Stereo Imager, Compressor, Maximizer (the mastering chain I saw in the master section before, notes section 6).
- Editor list (4 devices): M EQ, Stereo Imager, M Comp, Maximizer. Routing read, all rows clicked (min-max as shown):
  | Device | Source -> Target |
  |---|---|
  | M EQ | Loudness Curve -> Low Shelf Gain (-8 to 23) and Parametric 2 Gain (-8 to 23); EQ Boost Freq -> Parametric 1 Frequency (315-1,000); EQ Boost On (button) -> Parametric 1 Enabled (0-1) |
  | Stereo Imager | Stereo Imager On (button) -> Enabled (2 to 1, as shown) |
  | M Comp | Compression -> Threshold (127 to 0, reversed) and Ratio (25-50); Master Gain -> Output Gain (51-88); Compressor On (button) -> Enabled (2 to 1) |
  | Maximizer | Master Gain -> Input Gain (48-127); Punch (button) -> Look Ahead Enable (1 to 0, reversed), Soft Clip Enable (0-1), Attack Speed (0-2) |
- Reading: one **Compression** knob lowers the threshold and raises the ratio together (more squash), and one **Master Gain** knob raises the compressor's output and the maximizer's input together. "Punch" switches the maximizer to soft clip, fast attack and no look-ahead. (**Guess** on how each sounds; nothing heard.)
- The patch name "Init Patch" says nothing about what is inside; here the front labels were the only hint.

### 8t. Seventh pass (2026-09-30, owner away; Street Phone opened read-only, closed with no save prompt, Seen)
- **KICK SQUASH** (Kick insert, patch name "Dance"): same four front labels as the other squash Combinators (Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input). Editor list: "M Comp copy 5", "M EQ copy 5", "Stereo Imager copy 5", "Maximizer copy 5". All four rows clicked: Comp Input -> Input Gain 0-127; EQ Bass Freq -> Parametric 1 Frequency 30-200; EQ Treble Amount -> Hi Shelf Gain 0-30; Stereo Imager none; Maximizer Input -> Input Gain 0-127. **Identical mappings to Clap Squash / Org 1 Squash (8g, 8e), so the "Dance" patch is one design used four times** (Kick, Clap, Organ 1, Organ 2). Only the device names differ ("copy 5").
- **TOXIC VOCAL** (Middle 8 Vox insert): four front knobs and four buttons with NO labels. Editor list: "M EQ 2", "M Comp 2", "M Comp 1"; all three rows clicked: **no routing at all** (Source list empty). So none of its knobs do anything; nothing in it can be reached by a label. Inside: M EQ 2 (low end tilted down, gentle lift above about 1 kHz), M Comp 2 (soft knee on, adapt release on), M Comp 1 (soft knee off, adapt release off). Cabling between them not read.
- **VOCAL KHABANG 2** (Main Vox insert, rack label "VOCAL KHABA..."): **same three devices with the same names and what look like the same compressor settings as Toxic Vocal, no routing either**; only the EQ curve differs (nearly flat, with a lift at the very top). (**Guess**: one was copied from the other and the EQ edited.) Compressor knob positions compared by eye, not numerically.
- **NEPTUNE "MB VOX NEPT..."** (Middle 8 Vox, pitch adjuster): Root and Scale fields show "--" (no scale chosen); scale memory slot 1; Catch Zone Size marker between 100 and 200 cents (about 130, by eye); MIDI "To Pitch Adjust" is lit (so it follows MIDI notes), To Voice Synth and MIDI Input off; Transpose Semi 0, Cent 0; the Input buttons (Low Freq, Wide Vibrato, Live Mode) look off; Correction Speed knob about straight up, Preserve Expression about 4 o'clock. The note-key lights on the little keyboard: most lit; I could not tell from the picture which white keys are on, so I do not claim which notes are allowed.
- Closed with the red button: no save dialog. SHA-1 after `e377af376e09a211ad065069149e71b515906652` (same), 46,923,828 bytes, Demo Songs folder still two files dated 2023-09-04. The scratch song "untitled 2" stayed open.
- **Still not read:** the four Main Vox inserts' right-hand jacks, Master Section FX, and the automation lanes. Everything else on the to-do line is now read.

### 8u. Eighth pass (2026-09-30, owner asked "Do 39"; Street Phone opened read-only again, Seen)
- **DEFAULT MASTERING SUITE** (rack label "DEFAULT MAS...", right under the Master EQ, above the two RV7000s): same front labels as the "Init Patch" master Combinator of 8s (Loudness Curve, EQ Boost Freq, Compression, Master Gain; Stereo Imager On, EQ Boost On, Compressor On, Punch) and **the same routing in all four rows** (M EQ, Stereo Imager, M Comp, Maximizer: every Source, Target and min-max matches the 8s table). So the song carries the same mastering Combinator twice under different patch names; I did not find out which one is actually in the signal path.
- **Automation lanes, vocal area** (opened the lane groups; shapes read by eye from the clips):
  - Main Vox: FX1 Send On/Off, FX1 Send Level, FX2 Send On/Off, FX4 Send On/Off, FX4 Send Level, Level, Pan. Clips only around bars 24-29 (and again later); Level has a small step. FX1/FX4 Send Level and Pan show no clip in the bars I looked at.
  - M Vox Filter (the ECF-42 track): lanes Enabled, Frequency, Resonance, Mode. Bars ~24-28 and ~47-61, mostly FLAT lines (held values); Resonance steps up, dips, steps up near bars 57-59; Mode only in the second block (~53-61). So its filter is switched on and held, not swept.
  - Middle 8 Vox: FX1 Send Level, FX4 Send On/Off (clips around bars 5-7, 17-31, 27-31). M8 Vox Filter: Frequency and Mode clips at bars ~41-44, Resonance none; flat lines.
  - Chorus Vox: FX2 Send On/Off (clips near bars 17-29 and from 40).
- **Reading (Guess):** the vocal sends and filters are switched on and held for sections, not swept. That fits the earlier note that the demo's only real stepped move is the organ filter (8r / whole-song shape).
- Not read: **right-hand jacks** (rear view, hover). Not done on purpose: mostly outputs that mirror the left side already read, and the tooltip method is slow. Item 39 is otherwise done.
- Closed with the red button: this time Reason DID ask to save; answered **Don't Save**. (I had only clicked Editor rows, unfolded Combinators and opened lane groups, so the earlier guess that "unfolding causes the prompt" is still unproven.) SHA-1 after `e377af376e09a211ad065069149e71b515906652`, same; Demo Songs folder unchanged (two files, 2023-09-04). "untitled 2" still open, unsaved.


=====================================================
SOURCE FILE: demo-song-phrase-ideas.md
ORIGINAL LOCATION: HS:docs/reason/demo-song-phrase-ideas.md
=====================================================

# Phrase ideas from the demo songs (Street Phone A-E, Airplane F, Power G)

Running list (started 2026-09-29, step 00b). Spoken phrases the voice app may need for controls and
techniques seen in the demo song. Your call which to add; nothing here has been built.
Song details are in [demo-song-notes.md](demo-song-notes.md).

**Can the app do it today?**
- `yes`: works now, file named.
- `phrase only`: the machinery exists; only the phrase or a name is missing.
- `needs new code`: the app can't reach it yet.

Evidence used below:
- Voice grammar: `reason_voice/intents.py` (transport: play, stop, record, loop on/off, undo, lines 55-59).
- Knobs the app can turn: the scopes in `remote/ReasonVoice.remotemap`, measured in `docs/reason/calibration.json`.
- Names Reason accepts: `docs/reason/remote-vocab.json`.
- One device answers at a time: the one locked to ReasonVoice (`.claude/skills/reason-remote-bridge/SKILL.md`, "The device must be LOCKED").

## A. Filters and effects (devices the app already knows)

**About the "yes" answers below:** they mean the code and maps are there (remotemap:641; calibration.json
"ECF-42"; the phrase rules from DECISIONS "Item 28"). Item 28 says those fixes were tested offline and
"not yet re-tried live in Reason". So "yes" = built and offline-tested, not proven live.

| Phrase | What it should do | Device / control | Can the app do it today? | Seen in the song |
|---|---|---|---|---|
| "open the filter" / "close the filter a bit" | Raise or lower the filter cutoff by one nudge (10%) | ECF-42 Frequency | **yes** (see above), on whichever ECF-42 is locked | Organ 1/2, Main Vox, Middle 8, Timbales filters |
| "make it more resonant" | Nudge Resonance up | ECF-42 Resonance | **yes** (see above), same lock condition | M Vox Filter has a Resonance lane |
| "switch to band pass" | Set the filter mode | ECF-42 Mode | **yes** (see above): value names Low Pass 24 dB / Low Pass 12 dB / Band Pass 12 dB (DECISIONS "Item 28", `value_names.json`) | M Vox Filter has a Mode lane |
| "turn the filter on" / "off" | Enabled switch | ECF-42 Enabled | **yes** (see above), same lock condition | M Vox Filter has an Enabled lane |
| "the organ filter" (pick a filter by name) | Choose which of five ECF-42s to control | which device is locked | **needs new code**: only the locked device answers; there are five ECF-42s in this song | Main Vox, Middle 8, Timbales, Organ 1, Organ 2 |
| "more delay" / "less echo" | Nudge a shared effect's wet level | DDL-1, The Echo | **yes** if that device is locked (both are in calibration.json) | Delay 3/16, Echo returns |

## B. Mixer channels (the app can't reach these yet)

**Found while checking:** Reason's own "Reason Master Section" map (`remote-vocab.json`) names, for
every channel by number, Mute, Solo, Level, Pan and FX1-FX8 Send Level, plus "All Mutes Off",
"All Solo Off", FX1-FX8 Return Level and Master Level. My reading (**not tried**): locking the Master
Section, one device, might reach the whole mixer. There is also a per-channel "Reason Main Mixer Channel"
map (Level, Mute, Pan, Solo, FX1-FX8 Send Level and Send On). The catch is turning "the kick" into
"Channel N", which needs the song's channel order. Neither map is in `remote/ReasonVoice.remotemap`
(`grep Mixer` finds nothing), and `intents.py` has no mute or solo.

| Phrase | What it should do | Device / control | Can the app do it today? | Seen in the song |
|---|---|---|---|---|
| "mute the kick" / "unmute the kick" | Channel Mute on/off | Master Section "Channel N Mute" | **needs new code** (see the note above) | Kick channel mute worked by hand |
| "solo the bass" | Channel Solo | same | **needs new code**, same reason | Bass Tonewheel |
| "turn the pad down" / "pad up a bit" | Channel Level nudge | Main Mixer channel Level | **needs new code** | WarmPad fader (it is automated) |
| "pan the organ left" | Channel Pan | Main Mixer channel Pan | **needs new code** | Main Vox has a Pan lane |
| "send the vocal to the delay" / "more plate on the vocal" | Turn a channel's FX send on and raise its level | Main Mixer channel "FX4 Send On" / "FX4 Send Level" (names exist in remote-vocab.json) | **needs new code**. Also needs a name-to-number step: send 1 = Plate, 2 = Room, 3 = Echo, 4 = Delay 3/16 in THIS song (FX RETURN column); other songs differ | Main Vox FX1/FX2/FX4 lanes; Middle 8 Vox FX1/FX4; Chorus Vox FX2 |
| "everything on" / "solo off" | Clear every mute / every solo | Master Section "All Mutes Off" / "All Solo Off" | **needs new code**; the names exist in the Master Section map | The Mute All Off / Solo All Off buttons at the bottom right of the mixer |

## C. Combinator macro knobs (labels are the song author's)

| Phrase | What it should do | Device / control | Can the app do it today? | Seen in the song |
|---|---|---|---|---|
| "more reverb on the pad" | Raise the pad box's Reverb knob | PAD PROCESSOR Combinator, Rotary 3 | **needs new code**: Combinator scope has only Patch Next/Prev (remotemap:17-19), though Reason has Rotary 1-16 and Button 1-4 (remote-vocab.json). **And** the word "Reverb" lives in the song's label, not in Reason's map. Needs a per-song label list | Pad Processor: Filter Freq, Filter Rez, Reverb, Dly |
| "turn on the wide button" / "chorus on" | Flip a Combinator button | PAD PROCESSOR Buttons: Chorus, Dly FX, Unison, Wide | **needs new code**, same reason | Chorus and Wide lit |
| "squash the kick" / "less squash" | Kick box's Comp Input knob | KICK SQUASH Rotary 1 (my reading of the face) | **needs new code**, same reason | Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input |
| "punch" / "compressor on" / "EQ boost on" | Master box buttons | MASTER SECT Combinator buttons | **needs new code**, same reason | Master box: Stereo Imager On, EQ Boost On, Compressor On, Punch |

## D. Techniques and time (automation)

| Phrase | What it should do | Device / control | Can the app do it today? | Seen in the song |
|---|---|---|---|---|
| "sweep the filter up over four bars" | Write a filter move that lasts N bars, as an automation clip | any locked device with its own sequencer track | **needs new code**. The path is proven by hand on Scream 4 (`experiments/automation-test-2026-09-25/RESULTS.md`): device needs its own track, and Reason must be recording. Nothing in `reason_voice/` writes a move over time | Organ 1 filter Frequency lane: three one-point clips over bars 9-21 (guess: a stepped build-up) |
| "fade the reverb in" | Same, on a level or send | same | **needs new code** | Pad Processor Reverb lane: four clips over bars 45-65 (which way it moves: not checked) |
| "throw the last word to the delay" | Switch a send on for a short stretch, then off | Main Mixer channel FX send On + timing | **needs new code**, and needs the bar position of "the last word" | Main Vox FX4 Send On/Off clips (24-29, 49-61) |
| "record a sweep" / "record automation" | Arm and start recording so the next knob move is captured | Reason Record | **phrase only, partly**: "record" already presses Record (intents.py:57). Making the track and arming it are still by hand | (technique from the manual, not tried on this song) |
| "hold that" / "freeze the filter" | Stop a lane playing, keeping its current value | the lane's M button | **needs new code**; UI only, no remote name found | Lane M buttons in the sequencer |
| "give control back" / "let the automation take over" | Click Automation Override to hand a hand-moved knob back to its lane | transport Automation Override light | **needs new code**; not checked whether the remote map has an item for it | Worked by hand on the WarmPad fader |
| "go to bar 9" / "back to the start" | Move the playhead | transport position | **needs new code**: transport words are only play, stop, record, loop, undo | Needed for every check I did |

## E. Naming and asking

| Phrase | What it should do | Can the app do it today? |
|---|---|---|
| "what's on the kick?" / "what's the pad's reverb set to" | Read a value back | **partly**: the app shows the DISPLAYED value of a moved knob (`reason_control.py:79`, `displays`) but "volunteers nothing on lock" (SKILL.md line 337), so it only knows knobs that moved |
| "list the filters" | Say which ECF-42s exist | **needs new code**: the app can't read the rack, only the locked device |

## F. Added from the Airplane demo song (step 00c, 2026-09-29)

Song details are in [demo-song-notes-airplane.md](demo-song-notes-airplane.md). Same rule as above: "yes" means the
code or map is there, not proven live, and only the ONE locked device answers. This song has 4 Europas
(Nightclub Saw, Fifth Dimension, Punch Drunk Saw, Unisaw) and 4 Grains (Mothership Landing, Boomer Bass, Mushi,
Please Release Me), so "which one?" is the same open problem as the five ECF-42s in Street Phone.

| Phrase | What it should do | Device / control | Can the app do it today? | Seen in the song |
|---|---|---|---|---|
| "more filter mod" / "open the filter" on a Europa | Nudge Filter Mod or Filter Freq | Europa scope (`remote/ReasonVoice.remotemap` ~line 1260 has Filter Freq, Filter Reso, Filter Mod) | **yes**, if that Europa is locked | Nightclub Saw "Filter Mod" lane (bars 1-5, 19-20, 61-65) |
| "more distortion" / "filter up" on a Grain | Nudge Dist Amount or Filter Freq | Grain scope (remotemap ~line 1159 has Filter Freq, Dist Amount, Motion) | **yes**, if that Grain is locked | Mushi "Filter Freq" and "Dist Amount" lanes (bars 43-45) |
| "freeze it" | Set Grain's motion to Freeze | Grain "Motion" | **unknown**: Motion is mapped; I did not check whether "Freeze" is one of its value names (`value_names.json`) | Mothership Landing shows motion "Freeze" |
| "next drum pattern" / "pattern B" | Change the Redrum pattern | Redrum "Pattern Select" | **needs new code**: the Redrum scope has no item with "pattern" in its name | Kick and Clap "Pattern Select" lanes, blocks "A1" |
| "pump the pads" / "less pump" | Change how strongly the Synchronous curve moves the level | Synchronous modulation-amount dial over "Level" | **needs new code**: the Synchronous scope has Level, Master Level, Filter, Dist, Delay, Reverb knobs but no modulation-amount dials | Sidechain Bus Combinator holds Synchronous "Long Sidechain" |
| "put the leads on the bus" / "take the crash off the sidechain bus" | Change a channel's Output destination | mixer Output selector | **needs new code**; whether Reason's remote vocab names an output-routing item: not checked | 7 of 18 channels output to "Sidechain Bus" |
| "filter the kick" / "low pass on the kick" | Turn a channel's LPF or HPF on, or move its frequency | Reason's names "Channel N LPF On", "Channel N HPF On", "Channel N LPF Frequency", "Channel N HPF Frequency" (`remote-vocab.json`) | **needs new code**, same reason as OPEN-ISSUES 29 (no mixer scope) | Kick thin row: "LPF On/Off", "HPF On/Off" lanes (bars 1-13, 61-65) |
| "send the kick to the plate" | Turn Send 1 on for a channel | "Channel N FX1 Send On" (name exists in the vocab file, my reading) | **needs new code**, same reason. Also needs the name-to-number step: here FX1 = Plate, FX2 = Room, FX3 = Echo | Kick "FX1 Send On/Off" lane (about bars 21-22) |
| "more shift" / "hammer on" | Turn a Combinator macro knob or button by its author's label | Combinator Rotary and Button | **needs new code**, OPEN-ISSUES 30. The labels (Shift, Dirt, Width, Reverb Level; Hammer On, Compress, AM, Delay) come from the patch and are the same words as the lane names | Norwegian Boy -LNB Combinator; its automation lane is named "Shift" |
| "arp on" / "hold" | Control the Dual Arpeggio player | Dual Arpeggio | **needs new code**: the remotemap has no Dual Arpeggio scope (the vocab file mentions "Arpeggio" on 6 lines; not read in detail) | Norwegian Boy -LNB is played through Dual Arpeggio |
| "what goes to the sidechain bus?" | Read back which channels feed a bus | mixer Output labels | **needs new code**: the app can't read the rack or mixer, only the locked device | The pink Sidechain Bus channel and the pink Output labels |


## G. Added from the BLKMGK "Power" demo song (step 00d, 2026-09-29)

Song details are in [demo-song-notes-power.md](demo-song-notes-power.md). Same rule: "yes" means the code or map is there, not
proven live, and only the ONE locked device answers. None of these was heard.

| Phrase | What it should do | Device / control | Can the app do it today? | Seen in the song |
|---|---|---|---|---|
| "turn on the unison send for the piano" / "no echo two on the bass" | Switch a channel's FX send on or off by the effect's name | "Channel N FX Send On" (name in `remote-vocab.json`) plus the send names Plate, Room, Echo, Echo 2, Unison | **needs new code**, OPEN-ISSUES 29 (no mixer scope). Needs the name-to-number step (Plate=1 ... Unison=5) | Mixer send names 1-5; send 5 on for every channel, send 4 on for none |
| "bypass the audiomatic on the drums" / "audiomatic off" | Turn one Audiomatic insert off | Audiomatic scope `se.propellerheads.Audiomatic` (remotemap line 769: Enabled, Dry Wet, Transform, Input Gain, Volume, Preset) | **yes**, if that Audiomatic is locked. This song has 6 of them (Kong half, Kong double, Kong FX, Drum loop, Bass, Wub M), the same "which one?" problem as OPEN-ISSUES 34 | Kong, Drum loop, Bass and Wub M insert chains |
| "more transform" | Turn the Audiomatic "Transform" knob | same scope, Transform | **yes**, if locked | Audiomatic front and back (CV jacks Transform and Dry-Wet, no cables) |
| "more squash on the kick" / "more dirt on the drums" | Move a Pulveriser knob | Pulveriser is in the remotemap (scope exists, listed in the Street Phone section A) | **yes**, if that Pulveriser is locked (there are 3 in this song: Kong half, Kong double, Kong FX) | Kong "pulveriser" inserts |
| "more scream on the piano" | Move Scream 4 "Damage Control" or "Master Level" | Scream 4 scope (remotemap line 533: Damage Control, Damage Type, Master Level, Enabled ...) | **yes**, if locked (4 Scream 4s here: Piano L, Piano R, Mal L, Mal R) | Scream 4 inserts on the Piano and Mal chains |
| "arp on the bass" / "hold the arp" | Turn the RPG-8 on, or set its mode | RPG-8 (Bass arp): no scope in the remotemap that I checked | **needs new code**, same open issue as the Dual Arpeggio row in section F | Bass arp is an RPG-8 cabled to the Bass Malstrom by CV and gate; its clips are at bars 11-19 and 29-40 |
| "duck the bass under the kick" | Change how hard the Bass compressor is keyed | Bass channel compressor, KEY, threshold | **needs new code** (no mixer scope) | Bass channel KEY is lit and a Redrum feeds its Side Chain Input |
| "high pass the drums up for four bars" | Write a short filter-lift clip on the drum channel | Channel HPF Frequency automation lane | **needs new code**, OPEN-ISSUES 31 (no code writes automation) | Drum loop "HPF Frequency" lane clip at about bars 25-29 |
| "throw the echo on the last word" / "more echo" | Move an Echo's Dry/Wet Balance, or write a short clip on that lane | The Echo scope (remotemap line 491 has "Dry/Wet Balance", Feedback, Delay Time, Ducking ...) | **knob: yes**, if locked (there are 2 Echoes). **Writing the lane: needs new code**, OPEN-ISSUES 31 | "Jayy echo" lane "Dry/Wet Balance", bars ~40-42 |
| "show me the back of the piano" | Flip to the rack back and scroll to a device | Reason UI only (Tab, RACK button); no bridge path | **needs new code and is out of the bridge's reach**: today only the mouse or keyboard can do it | Tab key and PageUp/PageDown worked while the mouse was blocked |
| "more unison" / "less chorus" | Move UN-16 Unison Dry/Wet or Detune | UN-16 Unison scope (remotemap line 676: Detune, Dry/Wet, Voice Count, Enabled) | **yes**, if locked | Unison is send 5, on for all 13 channels |

=====================================================
SOURCE FILE: demo-song-skill-ideas.md
ORIGINAL LOCATION: HS:docs/reason/demo-song-skill-ideas.md
=====================================================

# Skill ideas from the demo songs (Street Phone, Airplane, Power, Qua z mo)

Running list (started 2026-09-29, step 00b). Skills worth having, found while exploring the demo.
Song details are in [demo-song-notes.md](demo-song-notes.md).

**Your rule for this session:** list first, build only the clear wins (small, reusable, already done by
hand in the demo).
**Why nothing is built yet:** your standing rule (memory `skill-benchmark-loop`) says a new skill goes
through skill-creator's benchmark loop (test prompts, with/without runs, review viewer, then your
feedback). That is a separate piece of work, not something to slip in at the end of an exploring
session. The two clear wins are marked below and are ready to start on your say-so.

Status: `idea` | `clear win, ready to build` | `built`

| Skill | One-line job | What triggers it | Status | Came from |
|---|---|---|---|---|
| **explore-reason-song** | Safely tour an open Reason song by screen: switch Mixer / Rack / Sequencer, unfold devices, expand automation lanes, read the transport, then close with Don't Save | "look at this song", "what's in this song", "learn from this demo" | **clear win, ready to build** | Everything I did by hand this session. Traps from this session, with how sure I am: Magnify tool zooms on double-click (seen, use the arrow); a second double-click on an automation clip may have changed its point (manual says it inserts one; I couldn't tell what happened), so open a clip once and click a point once; my playhead clicks landed on wrong bars because I mis-scaled coordinates (my error, so read the transport readout); a batch that stops mid-way leaves playback running (seen); never press a lane's X (manual); File > Close and Edit > Undo were greyed out while Reason wasn't the active app (seen), so close with the window's red button and read which document the dialog names first. **From Airplane (00c):** Window > View Main Mixer / View Racks / View Sequencer switches the view (Seen); Options > Toggle Rack Front/Rear flips to the back (Seen; a Tab keypress via the tool got "no verdict" twice, the menu worked); the mixer scrolls sideways by dragging its bottom scrollbar and the rack by dragging the blue box in its top-right map (Seen); the sequencer's ZOOM button fits the whole song and the two magnifiers at bottom left change track height, not the timeline (Seen); the small triangle at a device's top left folds it (Seen, needs a precise click); hover tooltips and the Ctrl-click jack menu need screen control (approved on a second visit): Ctrl-click via the display tools, Escape closes only sub-menus, a click on the window title bar closes the whole menu, and the list scrolls while the pointer rests on its bottom arrow (Seen). Closing a song with no changes gives no save dialog (Seen) |
| **reason-automation-lanes** | Read, open and explain automation: one lane per knob, clips with a cut corner, one-point clips holding a value, the Static Value, green borders, Automation Override, what M and X do | "how is this sweep made", "what is automated", "add a sweep" | **clear win (read side), ready to build**. The create side is from the manual only, not tried | Organ 1 filter clip opened by hand; override tested on the WarmPad fader; manual ch. 6 and 9 |
| reason-signal-flow | Read the back of the rack: cable colours (green effects, red instrument-to-mixer, yellow CV, blue Combinator), insert chains, shared effects on the Master Section's 8 sends, P-LAN having no cables, hover and "Scroll to Connected Device". **Also covers (merged from two earlier rows):** keyboard-only reading (Tab flips front/back, PageUp/PageDown scroll, arrow keys move between rack columns, hover a jack 2-3 s for "Connected to <device>: <jack>"; works while mouse clicks are blocked), and the layout convention (a channel strip sits directly above its instrument, inserts below it carry the channel's name, last insert goes up to the strip; Seen in Power and Street Phone, **Guess** that Reason always lays it out this way), plus the unfold trap (one unfold click per screenshot; batching misfires because Reason auto-scrolls) | "how is this connected", "where does this go", "map the rack" | **clear win (read side), ready to build**. Hover and Ctrl-click jack menu Seen (Airplane); whole rack read by keyboard and hover (Power, Qua z mo master and Pad FX, Street Phone channels). Needs screen control approved each session | Airplane, Power, Qua z mo, Street Phone back views; Manual [16] lines 11430-11500 and 11646-11660 |
| reason-combinator-macros | Read a Combinator's face (Rotary 1-4, Button 1-4, author labels), open its Devices and Editor, explain Modulation Routing (source to target, min/max, reversed, source range) | "what does this knob do", "what's inside this box" | idea. Modulation Routing itself not opened | KICK SQUASH and PAD PROCESSOR faces; manual ch. 63 |
| reason-mixer-by-master-section | Control any mixer channel by number through the Master Section map (Mute, Solo, Level, Pan, FX sends, All Mutes Off), and the channel-name-to-number step | "mute the kick", "more delay on the vocal" | idea (needs the app work in OPEN-ISSUES item 29 first) | Found in `remote-vocab.json` while checking the phrase list |
| song-to-phrase-gaps | Take the devices and lanes of an open song, look each up in the remotemap and calibration, and print what the voice app can and can't do | "what can the voice app do with this song" | idea. A small script plus a skill | The phrase list (A-E) was made by hand this way |
| reason-reference (update, not new) | Add a chapter-and-page pointer table to the existing skill: automation (ch. 6, 9), routing (16), main mixer and sends (17), Combinator (63), rack groups (11) | "look up how Reason does X" | idea. Small edit to an existing skill | The manual answered almost every "why" question I had |
| **reason-ducking-methods** | Explain the three ways a Reason song can "duck" or pump, and how to tell which one a song uses: (a) a compressor keyed by a cable in its Sidechain Input (Manual [17], lines ~12958-12991), (b) an Output Bus with a sidechain source (same place), (c) a Synchronous curve on Level, no cable (Airplane), (d) a Redrum used as a silent kick trigger cabled into a channel's Side Chain Input with KEY lit (Power Bass; check that the Redrum runs: RUN, pattern, no track; Seen wiring, not heard; OPEN-ISSUES 41) | "how is this sidechained", "why does it pump" | idea. Method (c) is Guess: the curve is Seen, the sound is not heard | Airplane: the channel and bus are both named "Sidechain Bus", but the Sidechain Input jacks are empty and the pumping device is a Synchronous "Long Sidechain" |
| **reason-output-bus-routing** | Read which channels feed which Output Bus: pink Output labels in the mixer, "Audio Output" on each rack device, red fader knob and "INPUT DISABLED, CHANNEL IS USED AS OUTPUT BUS" on the bus device's back | "what goes to this bus", "why is this pink" | idea. Small; done by hand in Airplane. Manual [17] "Output Busses" lines 12600-12660 | Airplane mixer and rack back |

## Notes
- The first two are the ones I'd build first. `explore-reason-song` would have saved most of the wrong
  turns in this session.
- `reason-remote-bridge` already covers locking a device and the bridge's file formats. None of the
  ideas above overlap it.
- Only `reason-ducking-methods` needs a listening check (method (c) is a guess until someone hears the Airplane bus).

## Build-by-hand skills (2026-09-29, practice songs untitled 2 and 3)
Owner: many small skills in sets, not one big one, for Hermes to do these jobs in Reason. All Seen by doing, none heard by me, none built.

| Set | Skill | Job and trap |
|---|---|---|
| 1 Safe handling | open-close-demo-safely | hash before/after, red-button close, read dialog, never save |
| 1 | fresh-blank-song | Cmd-N, Select All, Delete Tracks and Devices, answer "Delete All in Group" |
| 1 | reason-control-methods | app_menu picks menu items by name (best); coordinate menu clicks flaky; right-click and real drags need the full-screen tools |
| 2 Reading | read-rack-by-hover | hover 3 s for "Connected to..." |
| 2 | read-insert-chains | strip above its inserts, named for the channel |
| 2 | read-combinator-routing | Editor, click each device row: Source, Target, Min/Max |
| 2 | unfold-one-at-a-time | one unfold per screenshot |
| 3 Building | create-devices-by-menu | Create > Instruments/Effects/Utilities; effects made with an instrument selected chain in |
| 3 | matrix-on-instrument | right-click instrument > Utilities > Matrix (auto-cabled), draw 16 notes, Run |
| 3 | redrum-pattern | click steps; needs a Pattern Select lane clip or it does not play |
| 4 Automation | make-automation-lane | right-click knob > Edit Automation |
| 4 | draw-lane-clip | pencil: press, move, release (plain drag does nothing; first stroke after a tool switch is swallowed) |
| 4 | shape-lane-curve | Edit Inline (sometimes needs a second click), pencil a curve |
| 4 | matrix-pattern-lane | Matrix "Pattern Enable" lane needs a clip |
| 4 | loop-to-lanes | drag right loop marker to end of lanes, Loop on; else lanes end and effects stop |
| 5 Traps | hands-off-when-owner-moves | owner rule: cursor moves, stop and watch |
| 5 | dictation-blocks-clicks | turn Dictation off first |
| 5 | classifier-no-verdict | retry once, then stop and report |

Build first: make-automation-lane, draw-lane-clip, loop-to-lanes, matrix-on-instrument, create-devices-by-menu. Not solid: live knob recording wrote no lanes; Redrum and Europa sounding not confirmed.

=====================================================
SOURCE FILE: demo-song-template-and-automation-ideas.md
ORIGINAL LOCATION: HS:docs/reason/demo-song-template-and-automation-ideas.md
=====================================================

# Template and automation ideas from the demo songs

Running list (started 2026-09-29, after step 00c). Requested by the owner mid-session: "Look for template ideas.
Automation ideas and skill ideas. Along with phrases." Skills and phrases live in their own lists:
[skill ideas](demo-song-skill-ideas.md) · [phrase ideas](demo-song-phrase-ideas.md). Nothing here is built.

**ASSUMING (correct me any time):** "template" = a reusable starting setup (a song, rack or mixer layout) that
could be saved as a Reason template or written up as a recipe card in `recipes/`.

Tags as in the song notes: **Seen** = on screen · **Manual** = manual place named · **Guess** = not confirmed.
Songs: [Street Phone](demo-song-notes.md) · [Airplane](demo-song-notes-airplane.md) · [Power](demo-song-notes-power.md). Nothing here was heard.

## A. Template ideas (setups worth reusing)

| Template | What it is | Came from | How sure |
|---|---|---|---|
| **Pump bus** | An Output Bus channel that several channels route to, with an insert Combinator holding a Synchronous "Long Sidechain" curve on Level. One place sets the pumping for the whole group | Airplane: 7 of 18 channels go to "Sidechain Bus"; Sidechain Bus FX Combinator holds the Synchronous | Seen. That it pumps: Guess, not heard |
| **Send-effects trio** | Master Section sends 1-3 feeding RV7000 "Plate", RV7000 "Room" and The Echo, each named for what it is; Street Phone adds a DDL-1 "Delay 3/16" on send 4 | Both songs | Seen |
| **Macro-knob instrument or effect box** | A Combinator whose four knobs and four buttons carry author labels: Airplane "Shift / Dirt / Width / Reverb Level" and "Hammer On / Compress / AM / Delay"; Street Phone PAD PROCESSOR "Filter Freq / Filter Rez / Reverb / Dly". The labels become automation lane names | Both songs | Seen |
| **Effect Combinator as channel insert** | A Combinator used as the insert FX of a mixer channel | Street Phone pad processor; Airplane Sidechain Bus FX | Seen |
| **Kick squash chain** | Kick drum, then a squash stage before the mixer: Redrum then Pulveriser 1 "SQUASH" (Airplane); Kong then Compressor then Combinator "KICK SQUASH" (Street Phone) | Both songs | Seen |
| **Name-everything rule** | Every device carries a label (KICK COMP, PAD PROCESSOR); the mixer channel, the rack label and the patch share a name, so a spoken "the pad" can be matched. Airplane mostly does this but drifts a little (mixer "Please Release" vs rack "Please Release Me") | Both songs | Seen |
| **Riser and crash track pair** | Two Thor "Stereo Noise Sweep [Run]" tracks with short clips about every 8 bars, plus a Crash audio track with hits at section starts | Airplane | Seen the clips. Risers and section changes: Guess |
| **Filtered intro and outro on the kick channel** | The Kick's own channel-strip low-pass and high-pass switched on by clips over the first 12 and last 4 bars | Airplane Kick lanes "LPF On/Off", "HPF On/Off" at about bars 1-13 and 61-65 | Seen lanes. What it sounds like: Guess |
| **64-bar song map** | Entries at about bars 1, 13, 21, 29, 45 and 61 with an outro at 61-65 | Airplane | Guess (sections read from where tracks enter) |
| **Master chain** | A master-bus Combinator plus a separate mastering EQ | Street Phone "MASTER SECT" Combinator, MClass EQ, "Default Mastering Suite"; Airplane "Master Section FX" Combinator | Seen (Airplane one only by name) |
| **Arp into macro instrument** | A Dual Arpeggio player in front of a Combinator patch, so one macro knob (Shift) can move the whole part | Airplane Norwegian Boy -LNB | Seen |
| **Pulsar as an oscillator** | A Combinator with no synth: Pulsar LFO 1 Audio Out feeds an ECF-42 filter, a second Pulsar's CV Out wobbles LFO 1's Rate, then mixer, Scream 4, RV7000; an RPG-8 arpeggiator on top | Airplane "Pulse Scream -LC" (wiring file, D3) | Seen the cables. How it sounds: not heard |
| **Double Malstrom "Kalimba" voice** | Two Malstrom synths (L and R) into a Line Mixer 6:2, then Pulveriser, The Echo, Compressor, all inside one Combinator with four macro knobs (Shift, Dirt, Width, Reverb Level) | Airplane "Norwegian Boy -LNB" (wiring file, D and D2) | Seen. What the knobs drive: Modulation Routing not opened |
| **Same master Combinator in both songs** | "Master Section FX": M EQ, Stereo Imager, M Comp, Maximizer inside a Combinator, knobs Loudness Curve, Compression, EQ Boost Freq, Master Gain | Airplane and Street Phone | Seen (left jacks read) |
| **Silent kick trigger for the bass duck** | A Redrum (pattern A1, steps 1-5-9-13, one kick sample) cabled from its channel 1 outputs into the Bass mixer channel's Side Chain Input, with the channel compressor's KEY lit. Nothing else in the mix plays it | Power "BASS SIDECHA..." Redrum | Seen wiring and KEY. That it pumps: not heard, and whether the Redrum runs is unknown (OPEN-ISSUES 41) |
| **Per-channel insert chain "Comp, EQ, Scream 4, EQ"** | Four inserts under the instrument, each labelled with the channel name (PIANO L COMP, PIANO L EQ, ...) and a Scream 4 in the middle | Power Piano L/R and Mal L/R | Seen. Order taken from the rack order; middle links not hovered |
| **Drum-machine character chain "Audiomatic, Pulveriser, EQ"** | Each Kong runs through an Audiomatic (Retro Transformer) then a Pulveriser, and Kong FX adds an EQ | Power Kong half / double / FX | Seen (Kong half fully hovered) |
| **RPG-8 into a synth by CV and gate** | An RPG-8 arpeggiator cabled to the Malstrom's Gate, CV, Mod Wheel and Pitch Wheel inputs, so an arp part plays the same bass patch | Power Bass arp to Bass | Seen by hover |
| **Send 5 on for every channel** | One shared Unison effect on send 5, on for all 13 channels, while send 4 (a second Echo) is on for none | Power mixer | Seen (levels not read) |
| **Own track for the vocal, own strip** | An Audio Track "Jayy vox comp" whose channel has sends 3 and 4 off | Power | Seen |
| **42-bar hook song at 84 BPM** | Intro 1-3, verse 3-11, hook 11-19, break 19-25, verse 25-29, final hook 29-40, echo tail 40-42 | Power | Guess (read from clip positions) |

## B. Automation ideas (patterns for moves over time)

| Idea | What it does | Came from | How sure |
|---|---|---|---|
| **Hold a value with a one-point clip** | A clip with one point holds that value for its length; outside clips the parameter sits at its static value | Street Phone Organ 1 filter clips; Manual [6] lines 4380-4389 | Seen and Manual |
| **End-of-section filter lift** | A short clip near a section end that rises from the resting value: Mushi "Filter Freq" 2 bars at bars 43-45 (three points, rising), with a "Dist Amount" clip about a bar later | Airplane | Seen the shape. That it lifts the filter: Guess |
| **Switch lanes as long clips** | On/Off lanes ("LPF On/Off", "HPF On/Off", "FX1 Send On/Off") where a clip is the "on" stretch. "FX1 Send On/Off" has a short clip at about bars 21-22: a one-bar throw to the Plate | Airplane Kick | Seen lanes. The one-bar-throw reading: Guess |
| **Pattern automation** | Redrum "Pattern Select" clips ("A1" blocks) switch patterns on the bar. Manual [6] line 4512: pattern lanes have no static value, and where there is no clip the device stops | Airplane Kick and Clap | Seen and Manual |
| **One lane per macro knob** | A Combinator knob lane ("Shift", bars 29-45) moves everything wired to that knob at once, one curve instead of many | Airplane Norwegian Boy | Seen |
| **Mod Wheel lanes** | "(Mod Wheel)" lanes on the three Europas (about bars 9-13, 13-20, 45-61). What they drive inside Europa: not looked at | Airplane | Seen lanes only |
| **Level lane on a channel** | A "Level" lane on a mixer-style row: Kick bars 29-45 | Airplane | Seen |
| **Automate the modulation, not the sound** | Synchronous already loops a curve on the beat, so the song only needs to change its settings (Level, filter) instead of drawing many volume dips | Airplane Synchronous | Seen the device. How the composer used it: Guess |
| **Lane name equals parameter name** | The lane is named by the parameter ("Filter Mod", "Filter Freq", "Dist Amount", "Pattern Select"); the voice app's Europa and Grain scopes already have "Filter Mod", "Filter Freq", "Dist Amount" | Airplane and `remote/ReasonVoice.remotemap` | Seen |
| **Voice-written sweep** | "Sweep the filter up over four bars" would write a clip like the Mushi one. Proven by hand for a device with its own track while recording (`experiments/automation-test-2026-09-25/RESULTS.md`); nothing in `reason_voice/` writes it. OPEN-ISSUES 31 | Both songs | Seen (bridge test) and file facts |
| **Channel-strip HPF lift** | A short clip on a mixer channel's "HPF Frequency" lane (Drum loop, about bars 25-29), the channel's high-pass knob getting a green frame | Power | Seen the lane and the green frame. Direction: not read |
| **Echo throw at the end** | A short "Dry/Wet Balance" clip on an echo device over the last two bars (about 40-42) | Power "Jayy echo" | Seen the lane. What it sounds like: not heard |

## B2. Things this exploring taught about method (worth reusing)

| Idea | Detail | How sure |
|---|---|---|
| **Read wiring by hover** | Hover a jack, wait 2 seconds: tooltip "Connected to <device>: <jack>". Works on jacks, not on cable bodies (two tries) | Seen |
| **Read wiring by menu** | Ctrl-click a jack: full device list, check on the connected device, asterisk on occupied jacks in each sub-menu | Seen |
| **Jump the rack with RACK** | The RACK button under a mixer channel scrolls the rack to that device | Seen |
| **Find every keyed sidechain in one pass** | Open one jack menu and hover each channel: an asterisk beside "Side Chain Input L/R" means a real cable. Airplane has none | Seen |

## C. What each template or automation idea would need
- **Recipe cards:** a card needs `recipes/**/*.md` frontmatter and the section list from CLAUDE.md. Good first cards: "Pump without a
  sidechain cable (Synchronous)", "Filter riser (Grain filter and distortion)", "Kick squash", "Sub-mix bus".
- **Reason templates:** a Reason song saved as a template would hold the rack; that is for the owner to do in Reason.
- **Checking:** each "Guess" above needs ears, or a look at the parameter values in the clip.

=== END OF PART ===
