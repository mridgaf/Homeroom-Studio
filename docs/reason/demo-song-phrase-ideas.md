# Phrase ideas from the demo songs (Street Phone A-E, Airplane F)

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

