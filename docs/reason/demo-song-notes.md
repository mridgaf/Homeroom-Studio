# What the Street Phone demo song teaches

**Song:** Gabriel Gassi, "Street Phone" (`~/Music/Reason 12/Demo Songs/Gabriel Gassi - Street Phone.rsndemo`).
A Reason 10 demo track. Opens **Read-only**. 100 BPM. About 69 bars.
**Explored:** 2026-09-29, step 00b of OPEN-ISSUES. Claude can't hear, so everything here comes from
the screen, the meters and the Reason 12.7 manual, not from listening.
**Lists that go with this:** [phrase ideas](demo-song-phrase-ideas.md) ·
[skill ideas](demo-song-skill-ideas.md)

**How to read the tags**
- **Seen** = on screen in this song.
- **Manual** = the Reason 12.7 Operation Manual says so (`~/.reason_voice/reason12_manual/`, chapter in brackets).
- **Guess** = my reading, not confirmed.

**Does Reason itself say anything about this song?** No. Searched: the Reason 12 app, Reason Companion,
the manual text, the Showcase favorites file, Spotlight. The only place the name appears is the song file.
The file is a compressed Reason archive, so its insides can't be read outside Reason. The song's own
info card has only the artist's web page and e-mail, no notes.

---

## 1. How the rack is laid out (front view)

**Seen + Manual [11]:** the rack is grouped by mixer channel ("Auto-group Devices and Tracks"). Each
coloured strip is a track (mute, solo, level, pan, SEQ, MIX). The instrument and the effects for that
track sit right under it, top to bottom in signal order.

**Output and master (top of the rack)**

| # | Device | What it is |
|---|---|---|
| 1 | Hardware Interface | Where sound leaves the computer (here "MacBook Pro Speakers") |
| 2 | Master Section | The main mixer's master strip, with its insert-FX switch |
| 3 | Combinator "MASTER SECT..." (patch "Init Patch") | Master-bus processing in one box: MClass EQ, Stereo Imager, Compressor, Maximizer. Four big knobs: Loudness Curve, EQ Boost Freq, Compression, Master Gain. Four buttons: Stereo Imager On, EQ Boost On, Compressor On (lit), Punch |
| 4 | MClass Equalizer "MASTER EQ" | One more EQ after it |
| 5 | Combinator "DEFAULT MAS..." (patch "Default Mastering Suite") | A ready-made mastering chain |
| 6-9 | RV7000 "PLATE" (patch "ALL 1st Plate"), RV7000 "ROOM" (patch "AMB Oak Room"), The Echo "ECHO" (patch "Warm Echo"), DDL-1 "DELAY 3/16" | The four shared effects (send effects). See section 3 for how tracks feed them |

**Tracks, in mixer order**

| Track | Type | What is under it |
|---|---|---|
| Main Vox | audio track | Combinator "Vocal Khabang 2", MClass EQ "M VOX EQ", **ECF-42 filter "M VOX FILTER"**, EQ "FILTER EQ", Compressor "M VOX COMP" |
| Middle 8 Vox | audio track | Combinator "Toxic Vocal", **Neptune "M8 VOX NEPT..."** (pitch adjuster / voice synth), **ECF-42 "M8 VOX FILTER"**, Compressor, EQ "M8 FILTER EQ" |
| Chorus Vox | audio track | nothing in the rack |
| Kick | instrument | Kong drum kit "Deep House", Compressor "KICK COMP", Combinator "KICK SQUASH" (patch "Dance") |
| Clap | instrument | Kong "Deep House", Compressor "CLAP COMP", Combinator "CLAP SQUASH" (patch "Dance") |
| LambaBeat | instrument | Dr. OctoRex loop player (loop "Crb22_LambaBeat_130_TSB"), Combinator "BEAT PROCESS" (patch "Synth Processor") |
| Timbales | audio track | Combinator "TIMB PROCESS..." (patch "Synth Processor"), **ECF-42 "TIMB FILTER"** |
| Bass Tonewheel | instrument | Combinator (patch "Tonewheels - Jazz Perc"), Compressor "TW COMP", EQ "TW EQ" |
| Organ 1 | instrument | Combinator "ORGAN 1" (patch "Organ & Choir"), Combinator "ORG 1 SQUASH" (patch "Dance"), **ECF-42 "ORGAN 1 FILT..."** |
| Organ 2 | instrument | same as Organ 1 ("ORG 2 SQUASH", "ORGAN 2 FILT...") |
| WarmPad | instrument | SubTractor (patch "WarmPad"), Compressor "PAD COMP", EQ "PAD EQ", Combinator "PAD PROCESSOR" (patch "Synth Processor") |
| Guitar question | instrument | Combinator (patch "Guitar question"), EQ "GUIT EQ", Combinator "DELUXE VOCA..." (patch "Deluxe Vocal FX Chain", Multi-FX) |
| Pictures of Moments | instrument | Combinator (patch "Pictures of Moments"), Combinator "SYNTH PROCE..." (patch "Synth Processor"), EQ "PICTURES EQ" |
| Booomzzz | audio track | nothing in the rack |

**Patterns worth noticing**
- **Every device has a name label** on it (KICK COMP, TW EQ, PAD PROCESSOR). That is why the song is readable. Seen.
- **Combinators are used as effect boxes, not only as instruments.** Manual [17]: an "Effect Combi"
  patch can sit in a channel's insert-FX slot, and several can be chained in a row. The "Dance"
  (x4: Kick, Clap, Organ 1, Organ 2) and "Synth Processor" (x4: LambaBeat, Timbales, WarmPad, Pictures
  of Moments) boxes look like exactly that. Seen (faces) + Manual. Which slot they sit in: not checked.
- **The four "SQUASH"/"PROCESSOR" faces (opened two):**
  - KICK SQUASH: four knobs Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input; buttons Run and Bypass FX. Seen.
  - PAD PROCESSOR: four knobs Filter Freq, Filter Rez, Reverb, Dly; four buttons Chorus (on), Dly FX, Unison, Wide (on). Seen.
    Inside it (Devices button), top to bottom: a Combinator mixer, an MClass Compressor "COMPRESSOR",
    an MClass Stereo Imager "IMAGER", a 14-channel Mixer whose four returns are named MAIN VERB, DLY VERB,
    CHORUS, UNISON, then the devices those returns feed: RV7000 "MAIN VERB" (patch "Synth Verb"),
    DDL-1 "DELAY L" and DDL-1 "DELAY R", MClass EQ "BP FILTER", RV7000 "DLY VERB" (patch "Default
    Verb"), CF-101 Chorus/Flanger "CHORUS", UN-16 Unison "UNISON", and an ECF-42 "FILTER". Seen. Guess: the
    face's Filter Freq and Filter Rez drive that inner ECF-42; not confirmed (Modulation Routing not opened).
    So one small face hides a whole send-effects rig, built from stock devices.
  - The knob names on the face are the song author's own labels (Manual [63]: double-click a label to
    rename it). Hovering a knob shows its name and value, e.g. "Filter Freq: 123". Seen.
- **ECF-42 filters sit on 5 tracks** (Main Vox, Middle 8 Vox, Timbales, Organ 1, Organ 2). Section 3 shows what moves them.

## 2. How devices are connected (back view)

**How to look:** Options > Toggle Rack Front/Rear (or press Tab). Manual [16].

**Cable colours, from the manual [16]:** green = effect devices · red = instrument to mixer ·
yellow = CV · blue = Combinator connections. Seen: the ECF-42's audio cables are green.

**What I saw**
- **The Organ 1 ECF-42 back panel:** only the four audio jacks are cabled (In L/R, Out L/R). Freq CV,
  Decay CV, Res CV and Env. Gate are all empty. Seen. So no cable is moving that filter. The only thing
  I saw moving it is its automated Frequency lane. Not checked: its Env Amount, or notes on its own
  sequencer track (`device_refs/ecf-42.md` says notes there can fire its envelope).
- **The back of the whole rack is a thick tangle**, mostly green cables running up and down the
  length of the rack, plus teal cables running the full height. I did not follow the teal ones.
  Guess: the green bundle is the per-track insert chains. Manual [17]: signals go from the channel
  device's "To Devices" jacks, through the effects, and back to its "From Devices" jacks.
  Whether the teal cables are the Combinator (blue) connections: **not confirmed**.
- **Channel to master has no cable at all.** Manual [16]: this internal route ("P-LAN") is only shown as an
  "Audio Output" readout on the channel's device.
- **Shared effects:** manual [17]: send effects plug into the Master Section's 8 FX Send / 8 FX Return
  jacks, up to 8 at once. Seen (mixer view, "FX RETURN" column): 1 = Plate, 2 = Room, 3 = Echo,
  4 = Delay 3/16, 5-8 empty. Every channel has 8 send slots: a number button (on/off, blue when on),
  a LEVEL knob and a PRE switch. Manual [17] agrees.

**How to trace a cable without the tangle (Manual [16], not tried):** hover a jack for a tooltip with the device it goes to ·
click-and-hold a jack > "Scroll to Connected Device" · Options > Reduce Cable Clutter (key K); with the
"Show for selected devices only" setting it fades every cable except the selected device's.

## 3. Sweeps (automation)

**In this song a "sweep" is automation: a knob move stored in the song as a clip on a lane.** That is
what I found on every lane I opened. I only checked one filter's back panel (Organ 1's, section 2), so I
can't say nothing else in the song is driven by an LFO or an envelope.

**Where they live (Seen):** in the sequencer, each automated knob has its own lane, under its track. Devices
that aren't instrument or audio tracks get their own "device track" (Delay 3/16, M Vox Filter, M8 Vox
Filter, Timb Processor, Organ 1 Filter, Organ Echo, Organ 2 Filter, a second "WarmPad", Pad Processor).
A green border on a knob or fader means it is automated (Manual [6]).

| Track | Lanes I opened or saw | Clips at |
|---|---|---|
| Main Vox | FX1 Send On/Off, FX1 Send Level, FX2 Send On/Off, FX4 Send On/Off, FX4 Send Level, Level, Pan | bars 24-29 and again 49-61 |
| Middle 8 Vox | FX1 Send Level, FX4 Send On/Off | short clips near its phrases |
| Chorus Vox | FX2 Send On/Off | not measured |
| M Vox Filter (ECF-42) | Enabled, Frequency, Resonance, Mode | bars 24-29 and 48-63 (Resonance has a small dip near bar 57) |
| Organ 1 Filter (ECF-42) | Frequency | bars 9-21 and 33-45, three 4-bar clips each |
| Pad Processor (Combinator) | Reverb | bars 45-65, four clips |

**What a clip is (Manual [9]):** a block with a cut-off top-right corner. Inside are points joined by
straight lines (can be bent into curves later). Outside the clips the knob sits at its **Static Value**.

**Opened one to check (Seen):** Organ 1 Filter, Frequency lane, first clip (bars 9-13).
- Static Value box at the left of the open clip: **127** (the top of the 0-127 range).
- The clip holds **one point**, in the middle of the clip (bar 11).
- The next two clips (bars 13-21) show their line **higher up the lane** than the first clip's. Which
  means clip 1 is a lower value than clips 2 and 3. **The actual numbers I don't know.** My first read
  off the picture was "near 51" and "near 78" (a rough guess from where the line sat in the lane).
  Later, after a second double-click I shouldn't have made (section 4), the toolbar showed **Value 24**
  for the point, and I can't tell whether that was its original value or something my click changed.
  So I'm not stating a number for any clip. What I'm sure of from the first look is the order (clip 1
  lower than clips 2 and 3) and the Static Value of 127.
- Manual [9]: a one-point clip holds its value across the whole clip, and you stretch the clip to change how long.
- **Guess** from those clips: the organ filter is held below its static value at bar 9, a step higher at
  bar 13, and back at the static 127 from bar 21, then the same shape again at bars 33-45. That would
  be a **staircase build-up**, not a smooth ramp. I did not hear it.

**The vocal "throws":** Seen (mixer view) FX1 = Plate, FX2 = Room, FX3 = Echo, FX4 = Delay 3/16. Seen:
Main Vox has clips on its FX1, FX2 and FX4 send lanes at bars 24-29 and 49-61, and its vocal audio
starts around bar 25. **Guess:** those on/off clips switch the sends on for those stretches so the
voice throws into the reverbs and delay, and the sends are off the rest of the time. I did not check
whether each clip holds "on" or "off".

**Whole-song shape (Seen, zoomed out):** the organ-filter clips cover bars 9-21 and 33-45, the vocal
filter clips 24-29 and 48-63, the pad reverb 45-65. Guess: those are the song's sections, with the
automation starting at the section starts. I didn't listen, so I can't say what each section is.

**How to make one (Manual [6, 9]), none of it tried by me:**
- Record: arm the track, press Record, turn the knob. The track must exist (right-click the knob > Edit
  Automation, or Create Track for it). Set the Static Value first.
- Add a lane by hand: Option-click the knob, or the "Track Parameter Automation" drop-down.
- Draw: Pencil in an open clip. Option-click with Pencil draws a held value over a span.
- Open a clip: double-click it (Selection tool). Esc closes it. The lane's Static Value box is at its left.
- Lane buttons: **M** freezes the lane, **X deletes it and its clips. Don't press X.**
- Alt/Option-click a lane's triangle to fold or unfold every lane.

**Bridge side (already proven, `experiments/automation-test-2026-09-25/RESULTS.md`):** the voice bridge can
write automation on a locked device, if that device has its own sequencer track and Reason is recording.
Night 2 of that file says the Record and Play buttons over the bridge were fixed.

## 4. What happened when I changed things

Nothing was saved. The demo was closed with Don't Save, so every change below was thrown away with it.

| I did | What happened |
|---|---|
| Muted the **Kick** channel while the song played | MUTE lit red; the Kick channel's meter dropped to almost nothing; the Bass Tonewheel meter was still lighting up. Unmuted after |
| Dragged the **WarmPad fader** by hand (song stopped) | Fader moved; its green border disappeared; the **Automation Override** light in the transport bar lit green |
| Clicked the **Automation Override** light | Light went off; fader went back to its automated position; green border came back. Same as Manual [6] "Live mode" |
| Double-clicked the first Organ 1 Filter clip (arrow tool) | It opened, showing its one point and the Static Value 127. Esc closed it. (With the Magnify tool selected, double-click only zooms. Use the arrow tool) |
| **Double-clicked the same clip a second time** (a slip on my part) | **What happened is unclear.** The toolbar then read Position 11.1.1.0, Value 24. Either (a) the second double-click put a point down or overwrote the clip's point (the manual says a double-click inside an open clip inserts a point), or (b) it only selected the existing point and 24 was already its value. My click was on the clip's middle, exactly where the existing point sits, so I can't tell which. Edit > Undo was greyed out and Cmd-Z showed no change. **Treated as a possible edit and discarded by closing the song with Don't Save.** Nothing reached the song file |
| Turned the Pad Processor **Wide** button off, then on | It went dark, then lit again. It is the fourth button on the Combinator's face |
| Dragged the Pad Processor **Filter Freq** knob | No visible change; I didn't chase it |
| Unfolded the Organ 1 ECF-42, the KICK SQUASH and PAD PROCESSOR panels, opened the Pad Processor's Devices view, changed sequencer zoom, switched Mixer / Rack / Sequencer views | Views only |
| Closed the demo (the window's red button), answered **Don't Save** | Demo file unchanged: same size (46,923,828 bytes) and date (2023-09-04). Your scratch song was not touched |

**My knob-watching was not reliable.** I moved the playhead to a few bars, played about a second, and
read the ECF-42 Frequency knob from a screenshot. The first run looked like steps up at bars 10 and 14.
A later run showed no change, and one click landed on the wrong bar. The two runs disagree. **Trust the
open clip (Static Value 127, one point per clip, clip 1 lower than clips 2-3), not the knob readings.**
Watching a knob by screenshot is too slow to be useful. A better way is to open the clip (and to
read the exact value by clicking its point once, not double-clicking).

**Not done:** re-patching a cable (the back of the rack is too tangled to grab one jack reliably by
screenshot), soloing a channel, deliberately drawing or editing a sweep (the one edit I made was an
accident), turning the Combinator macro knobs beyond the Wide button, hearing any of it (no ears).
Nothing needed a listening check, so no question went to you.

## 5. Anything else useful

- **Opening a second song with `open -a "Reason 12" <file>`** opened it in its own window and left the
  scratch song alone. No save prompt came up for the scratch song. (I did not try File > Open.)
- **The mixer view hides the send rows** until you press FX in the Show/Hide column on the right.
- **Claude's menu-control tool sometimes fails its safety check** and works on a retry. The
  Window menu (View Main Mixer / View Racks / View Sequencer) and Options > Toggle Rack Front/Rear are
  the reliable way to change views.
- **A slip of mine, not a Reason quirk:** several of my playhead clicks landed on the wrong bar because I
  mis-scaled the screenshot coordinates. Lesson for next time: read the transport's bar readout in the
  same screenshot before trusting a result.
- **What this song shows about the voice app** (details in OPEN-ISSUES items 29-33):
  - Voice already handles: ECF-42 knobs (calibrated; Frequency, Resonance, Mode, Enabled in
    `remote/ReasonVoice.remotemap:641`), MClass EQ/Compressor/Stereo Imager/Maximizer, RV7000, The Echo,
    DDL-1, Kong, SubTractor, Neptune (all in `docs/reason/calibration.json`). Transport words: play,
    stop, record, loop, undo (`intents.py:55-59`). Only one device answers at a time (the locked one),
    so with five ECF-42s in this song, "the organ filter" can't be picked by name today.
  - Voice can't do yet: mixer channels (level, pan, mute, solo, FX sends: Reason's "Master Section" map in
    `docs/reason/remote-vocab.json` has all of them by channel number, plus "All Mutes Off" and
    "All Solo Off", but no mixer scope is in the remotemap), Combinator knobs (the
    Combinator scope has only Patch Next/Prev, `remotemap:17-19`), moving the playhead, automation by phrase.
  - **Combinator knob labels are the song author's own** ("Reverb", "Filter Freq"). Reason's map only
    says "Rotary 3". So a phrase like "more reverb on the pad" needs a per-song label list.
- **Manual chapters worth knowing:** 9 Note and Automation Editing (p. 255) · 6 Recording (p. 135) ·
  16 Routing Audio and CV (p. 429) · 17 The Main Mixer (p. 441) · 63 The Combinator (p. 1305).

## Not looked at (open questions the demo left)
- The real numbers of the Organ 1 filter clips (I only know their order: low, higher, higher).
- What the Pad Processor's Reverb knob actually drives inside (Editor > Modulation Routing).
- The Delay 3/16 device track's lanes, the Timb Processor, Organ Echo and Organ 2 Filter tracks, and the second "WarmPad" track.
- What the teal cables in the back view are.
- How the "Dance" boxes on Kick, Clap and the organs differ from each other.

## 6. Wiring read by hover tooltip (added later the same day, after the owner approved screen control)
Owner's tip: hovering a jack shows what it is wired to. **Seen: it works on jacks** ("Connected to ..." tooltip).
Hovering the cable bodies in the folded rack view showed nothing (two tries; not proven that cable bodies never
show one). Street Phone's devices are folded to strips in the rear view, so only the jacks of unfolded devices
could be read. **Sample only, not a full map.**

| From (jack) | Connected to |
|---|---|
| Master Section FX Send 1 Left / 2 Left / 3 Left / 4 Left | Plate: Left Input / Room: Left Input / Echo: Left Input / Delay 3/16: Left |
| FX Return 1 (Left) | Plate: Left Output (read from the send side: same wire) |
| FX Return 4 (Left) | Delay 3/16: Left (Guess for the direction: the tooltip reads the same as Send 4) |
| Master Section Insert FX "To Device" L | Master Section FX (Combinator): Combi Input Left |
| Master Section Insert FX "From Device" L | Master Section FX (Combinator): Combi Output (tooltip cut off at the edge) |
| Master Out Left | Default Mastering Suite (Combinator): Combi Input Left |
| Master Section FX Combinator, "To Devices Output L" | MClass "M EQ" input L |
| M EQ output | Stereo Imager: Left |
| Stereo Imager input L | M EQ: Left |
| Maximizer input L | M Comp (Compressor): Left |
| Maximizer output R | Master Section FX: Mixer Input Right (tooltip text cut off) |

- **Seen, so the chain inside the master Combinator is:** Master Section insert, then M EQ, Stereo Imager, M Comp, Maximizer,
  back to the Combinator's mixer. (Compressor input not read; inferred from the neighbours.)
- **Correction to my earlier reading (section 1):** I listed the master chain as "Combinator MASTER SECT, then MClass EQ
  MASTER EQ, then Combinator DEFAULT MAS...". The tooltips say Master Out goes straight into the "Default Mastering
  Suite" Combinator, so that one is the last stage before the speakers. Where it leads next: not read.
- **Seen:** on the back, this song's master effects (Plate, Room, Echo, Delay 3/16) are wired to Master Section sends 1 to 4 and
  returns 1 to 4, matching the FX RETURN names in section 3.
- **Not done:** every channel's instrument-to-mixer cable, the insert chains, and the Combinator inner cabling of
  the other Combinators, because the devices are folded to strips.
- **File check:** SHA-1 of the demo before this visit and after closing: `e377af376e09a211ad065069149e71b515906652`
  both times. Closing gave no save dialog.

## 7. Channel wiring, started (second pass, 2026-09-29; in progress)
Read by hover after unfolding devices one at a time. Unfolding several devices in one batch of clicks does not work: Reason scrolls
the rack when an unfolded device ends below the window, so later click positions are wrong (my error while trying it; only some devices
unfolded). One click, one screenshot, is reliable. Option-click "unfold the whole column" (Manual [11] line 9103) could not be tried:
display-scope mouse clicks stayed blocked by the Dictation overlay and my request for access to it was declined.
- **Kick channel (Seen, all four jacks by tooltip):** Kong "KICK" Main Audio Out L / R -> **Kick Comp** (MClass Compressor) Left / Right;
  Kick Comp output -> **Kick Squash** (Combinator) Input L / R (the tooltips on the Combinator inputs read "Kick Comp: Left / Right");
  Kick Squash Output L / R -> **Kick** channel strip Input L / R. So: Kong, Compressor, Squash Combinator, channel. Kong Aux Send Out jacks and
  the Combinator's Gate/CV inputs show no cable. The Combinator's four Control CV labels: Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input.
- Not yet read: every other channel (Clap, LambaBeat, Timbales, Bass Tonewheel, Organ 1, Organ 2, WarmPad, Guitar question, Pictures of Moments,
  Main Vox, Middle 8 Vox, Chorus Vox, Booomzzz) and the insides of the Combinators. Several devices are now unfolded in the open (unsaved) copy only.
- **Clap channel (Seen, all read by tooltip):** exactly the Kick pattern: Kong "CLAP" Main Audio Out L / R -> **Clap Comp** (Compressor) Audio Input L / R; Clap Comp
  Audio Output L / R -> **Clap Squash** (Combinator) Combi Input Left / Right; Clap Squash Output L / R -> **Clap** channel strip Input L / R.
  Same four Control CV labels as Kick Squash (Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input). Kong Aux Send Out jacks: no cable.
- **LambaBeat channel (Seen, by tooltip):** Dr. OctoRex "LAMBABEAT" Left / Right -> **Beat Process** (Combinator) Combi Input L / R (tooltips "LambaBeat: Left / Right", read from the
  Combinator side); Beat Process Output L / R -> **LambaBeat** channel strip Input L / R. The Dr. OctoRex's own jacks were not hovered (folded). Control CV labels of Beat Process:
  Filter Freq, Reverb, Filter Rez, Dly (same four as PAD PROCESSOR, so the "Synth Processor" patch).
- **Timbales channel (Seen, ECF side and strip side):** Timbales is an Audio Track (no instrument). Its Insert FX jacks go out to **Timb Process** (Combinator); **Timb Process Combi Output Left / Right ->
  ECF-42 "TIMB FILTER" In L / R** (tooltips on the ECF inputs); **ECF-42 Out L / R -> Timbales strip "From Insert FX" L / R**. So the audio clip runs Insert FX send, Timb Process,
  the ECF-42 filter, and back into the strip. The ECF-42's Freq CV, Decay CV, Res CV and Env. Gate jacks show no cable. Not read: what feeds Timb Process (its input side).
  The strip's Audio Output reads "Master Section" (front label).

### 7b. Channel wiring, continued (third pass, all read by hover, Seen; left jacks only)
Method: hover a jack for 3 s, tooltip "Connected to <device>: <jack>". The tooltip did not show when I moved the mouse 1 pixel from a jack I had just hovered; moving away first and back fixed it (my method note). Rack window had moved down on screen between passes, so I re-took a screenshot before using coordinates.

| Channel | Chain (instrument, then inserts, then strip) |
|---|---|
| Bass Tonewheel | Tonewheel Combinator (Combi Output Left) -> TW COMP (MClass Compressor) -> TW EQ (MClass Equalizer) -> channel "Bass Tonewheel" Input L |
| Organ 1 | "ORGAN 1" Combinator (Combi Output Left) -> ORG 1 SQUASH Combinator (Input L) -> ECF-42 "ORGAN 1 FILT..." (L In from Org 1 Squash Combi Output Left) -> channel "Organ 1" Input L |
| Organ 2 | "ORGAN 2" Combinator -> ORG 2 SQUASH Combinator -> ECF-42 "ORGAN 2 FILT..." (L In from Org 2 Squash Combi Output Left) -> channel "Organ 2" Input L. The tooltip on Org 2 Squash Input L was cut off after "Connected to Organ 2: Combi Outpu", read as the Organ 2 Combinator's Combi Output Left (**Guess** on the last word) |
| WarmPad | Subtractor "WARMPAD" (Out) -> PAD COMP -> PAD EQ -> PAD PROCESSOR Combinator (Combi Input Left) -> channel "WarmPad" Input L |
| Guitar question | "GUITAR QUEST..." Combinator (Combi Output Left; its own Input jacks have no cable) -> GUIT EQ -> "Deluxe Vocal FX Chain" Combinator (Combi Input Left) -> channel "Guitar question" Input L (from Deluxe Vocal FX Chain Combi Output Left) |
| Pictures of Moments | "PICTURES OF ..." Combinator (control labels Squash, Dirt, Tremolo, Unison Detune) -> SYNTH PROCESSOR Combinator (labels Filter Freq, Filter Rez, Reverb, Dly) -> PICTURES EQ -> channel "Pictures of Moments" Input L |

- Same layout convention as the other songs (strip on top, inserts below it named for the channel). Organ 1 and 2 use the same "squash then ECF-42 filter" pattern as Timbales.
- **Guitar question:** the name is the channel's; its instrument is a Combinator labelled "GUITAR QUEST...", with control labels including Delay Time, Control 3, Gtr Decay. It goes through a vocal FX Combinator named "Deluxe Vocal FX Chain" (name as shown; I did not open it, so I do not know what is inside). Whether the sound is a guitar: **not known**, not heard.
- Channel Audio Output on Guitar question and Pictures of Moments reads "Master Section" (Seen).
- Ctrl-click and clicks were not used. Nothing was played or saved.
- Still unread: Main Vox, Middle 8 Vox, Chorus Vox, Booomzzz, the inside of every Combinator, right-hand jacks.

### 7c. Vocal channels and Booomzzz (fourth pass, Seen by hover; left jacks only)
All vocal channels are Audio Tracks with the Insert FX section (the strip's "To Insert FX" / "From Insert FX" jacks). Output of every one reads "Master Section" on the strip.

| Channel | Insert chain, in signal order |
|---|---|
| Main Vox | strip To Insert FX L -> "VOCAL KHABA..." Combinator (controls unlabelled: Control 1-4) -> M VOX EQ -> M VOX FILTER (ECF-42) -> FILTER EQ -> M VOX COMP -> strip From Insert FX L. Every link read from at least one side; M VOX EQ's own jacks were not hovered (read from its neighbours' tooltips) |
| Middle 8 Vox | strip To Insert FX L -> TOXIC VOCAL Combinator (Control 1-4) -> **Neptune "MB VOX NEPT..."** (pitch adjuster and voice synth, Audio In L from Toxic Vocal, Audio Out L to MB Vox Filter; Note, Gate, Bend, Vibrato, Formant, Pitch and Amplitude jacks have no cable) -> MB VOX FILTER (ECF-42) -> MB VOX COMP -> MB FILTER EQ -> strip From Insert FX L |
| Chorus Vox | Audio Track with **no insert devices** (Insert FX section empty, next rack item is Kick) |
| Booomzzz | Audio Track (red) with **no insert devices**; Direct Out jacks have no cable; output Master Section |

- **Neptune is in this song** (only on Middle 8 Vox). Its settings and what it does to the vocal were not read (Guess: it is used as a pitch effect; not heard).
- The order of EQ and comp differs between the two vocals (Main Vox: EQ, filter, EQ, comp; Middle 8: filter, comp, EQ), so it is not a copied chain.
- Issue on my side: I unfolded devices (Toxic Vocal, Neptune, ECF-42, Comp, Equalizer, Chorus Vox strip; Vocal Khaba, M Vox Comp, Filter EQ, M Vox Filter) in the open copy; view state only, never saved.
- Dictation blocked clicks twice during this pass (the owner turned it off for the second half). Hover and keys worked throughout.

### 7d. Status after this pass
Channel chains read: Kick, Clap, LambaBeat, Timbales, Bass Tonewheel, Organ 1, Organ 2, WarmPad, Guitar question, Pictures of Moments, Main Vox, Middle 8 Vox, Chorus Vox, Booomzzz. Still not read: inside of every Combinator (Modulation Routing, what the macro knobs drive), right-hand jacks, Neptune settings, whether "Guitar question" is a guitar. Nothing was heard.

### 7e. How it closed (Seen)
Red button: Reason asked "Do you want to save the changes you made in the document 'Gabriel Gassi - Street Phone.rsndemo'?" (Save / Don't Save / Cancel). Answered **Don't Save**. Earlier demos closed with no dialog; this one did because I had unfolded devices (**Guess**: unfolding counts as a change). SHA-1 after: `e377af376e09a211ad065069149e71b515906652`, same as before; the Demo Songs folder still holds the same two files, dated 2023-09-04. The scratch song "Step 8 test copy 09 29 26" is still open and unsaved.

## 8. Inside the Combinators (fifth pass; Street Phone reopened read-only, Seen)
Method: unfold the Combinator (triangle), click **Editor** ("Show Programmer") to see its device list and, for a device clicked in the list, its Modulation Routing (Source, Target, Min, Max). **Devices** shows the inner rack. Clicking a row in the Editor list is view-only. Target names in the list are cut off at about 18 characters ("Channel 1 Aux 1 Sen..."); I read the tail as "Send" (**Guess** on that one word).

### 8a. BEAT PROCESS (LambaBeat insert, patch name "Synth Processor")
- Front: knobs Filter Freq, Filter Rez, Reverb, Dly; buttons Chorus (lit), Dly FX (off), Unison (lit), Wide (lit); RUN and BYPASS FX buttons; Pitch and Mod wheels.
- Inside (Devices): Combinator Mixer (14 channels plus a return strip labelled "CHORUS" and "UNISON"; channel 1 fader labelled "FILTER"), MClass Compressor "COMPRESSOR", Stereo Imager "IMAGER", CF-101 Chorus/Flanger "CHORUS", UN-16 Unison "UNISON", ECF-42 "FILTER".
- Routing read:
  | Device | Source -> Target (min-max) |
  |---|---|
  | Filter (ECF-42) | Filter Freq -> Frequency (0-127); Filter Rez -> Resonance (0-127) |
  | Mixer | Reverb -> Channel 1 Aux 1 Send (0-127); Dly -> Channel 1 Aux 2 Send (0-127); Chorus (button) -> Channel 13 Mute (1 to 0, reversed); Dly FX (button) -> Channel 12 Aux 3 Send (0-64); Unison (button) -> Channel 1 Aux 4 Send (0-83) |
  | Imager | Wide (button) -> Enabled (2 to 1, as shown) |
  | Chorus, Unison, Compressor | no mappings |

### 8b. TIMB PROCESS (Timbales insert, patch name also "Synth Processor")
- Same front labels as Beat Process. The **Reverb knob has a green frame** (automated; Seen). Buttons: Chorus lit, Dly FX off, Unison off, Wide lit.
- **Same patch name, different insides:** the Editor list is Compressor (M Comp), Imager (M Stereo), Mixer, Main Verb (RV7000), Delay L (Delay), Delay R (Delay), BP Filter (M EQ), Dly Verb (RV7000), and possibly more below (the list has a scroll bar; not scrolled). So a patch name does not tell you what is inside (my caution: I first expected them to match).
- Routing read: Mixer has the **same five mappings as Beat Process** (Reverb, Dly, Chorus, Dly FX, Unison to the channel targets above); Imager: Wide -> Enabled (2 to 1); BP Filter (M EQ): Dly FX -> Enabled (2 to 1); Dly Verb (RV7000): Dly FX -> Enabled (2 to 1). Main Verb, Delay L, Delay R: none. Compressor: not clicked.
- Not read: the rest of Timb Process's list, and the other Combinators (Clap/Kick/Org 1/Org 2 Squash "Dance", Organ 1/2 "Organ & Choir", Bass Tonewheel "Tonewheels - Jazz Perc", Pad Processor, Guitar question, Deluxe Vocal FX Chain, Pictures of Moments, Synth Processor, Toxic Vocal, Vocal Khaba, Master Section FX, Default Mastering Suite). Front patch names Seen on the rack front: Clap Squash = "Dance", Org 1 Squash = "Dance", Org 2 Squash = "Dance", Organ 1 = "Organ & Choir", Organ 2 = "Organ & Choir", Bass Tonewheel = "Tonewheels - Jazz Perc"; Organ 1 and Organ 2 also show an "INSTRUMENT" tag.

### 8c. Voice-app relevance (Guess until tested)
- The Combinator macro buttons drive mixer sends and mutes inside the Combinator (Dly FX -> Aux 3 Send, Unison -> Aux 4 Send). A phrase like "turn on the chorus on the beat process" would mean pressing a Combinator button. The remotemap has no Combinator-inner scope for these; whether the Combinator front controls are remotable was not checked.

### 8d. Correction to 8b (mine)
I wrote that Timb Process's device list might have more rows and that its Chorus, Unison and Filter were unread. After scrolling the list: it holds 11 devices in this order: Compressor, Imager, Mixer, Main Verb (RV7000), Delay L, Delay R, BP Filter (M EQ), Dly Verb (RV7000), Chorus, Unison, Filter. Read: **Filter: Filter Freq -> Frequency and Filter Rez -> Resonance (0-127), same as Beat Process; Chorus and Unison: no mappings.** So Timb Process has Beat Process's six devices plus two RV7000s, two Delays and a BP Filter (M EQ). Compressor is the only Timb device not clicked. The scroll I sent to the list also moved the rack behind it a little (view only).

### 8e. ORG 1 SQUASH (Organ 1 insert, patch name "Dance")
- Front labels: Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input (four knobs, buttons unlit, no button labels).
- Inside (Editor list, 4 devices, names as shown): "M Comp copy 3" (M Comp), "M EQ copy 3" (M EQ), "Stereo Imager copy 3" (M Stereo), "Maximizer copy 3" (M Maximizer). The "copy 3" tails suggest the same four devices were copied for other channels (**Guess**; Clap Squash and Org 2 Squash also show patch name "Dance" on the rack front).
- Routing read: M Comp: Comp Input -> Input Gain (0-127). M EQ: EQ Bass Freq -> Parametric 1 Frequency (30-200); EQ Treble Amount -> Hi Shelf Gain (0-30). Stereo Imager: none. Maximizer: Maximizer Input -> Input Gain (0-127).
- So one knob each drives the compressor's input, the bass EQ frequency, the treble shelf and the maximizer's input: a "squash" macro (matches the label, **Guess** on what it sounds like).
- Voice-app link: Combinator front knobs are named by the author; no remotemap scope for these was checked.

### 8f. How the second close went (Seen) and a correction (mine)
Closed with the red button: **no save dialog this time**, even though I unfolded Combinators and opened Editors. So my earlier guess (7e) that unfolding devices makes Reason ask to save is **not supported**: the first visit's dialog appeared after unfolding rack devices and hovering, this one after unfolding Combinators and clicking Editor rows. What triggers the dialog is unknown. Both times the answer was Don't Save (first) or none needed (second). SHA-1 after: `e377af376e09a211ad065069149e71b515906652`, same as before; Demo Songs folder unchanged (two files, 2023-09-04). Scratch song still open, unsaved.
Also my slip at the start of this reopening: I typed a file path into Reason after Cmd-O and Cmd-Shift-G, assuming a Finder-style dialog; Reason's Open Song is an in-app browser panel, so the keys went to the scratch song window. Its title and tempo (90 BPM) looked unchanged afterwards; I did not check further, and it is a scratch song that is never saved.

### 8g. CLAP SQUASH (Clap insert, patch name "Dance"; sixth pass 2026-09-30, Seen)
- Front labels identical to Org 1 Squash: Comp Input, EQ Bass Freq, EQ Treble Amount, Maximizer Input (four knobs, buttons unlit, no button labels).
- Editor list: "M Comp (M Comp)", "M EQ (M EQ)", "Stereo Imager (M Stereo)", "Maximizer (M Maximizer)". No "copy 3" tails, which fits my earlier guess (8e, **Guess**) that Org 1 Squash is a copy of this one.
- Routing read, all four rows clicked: M Comp: Comp Input -> Input Gain (0-127). M EQ: EQ Bass Freq -> Parametric 1 Frequency (30-200); EQ Treble Amount -> Hi Shelf Gain (0-30). Stereo Imager: none. Maximizer: Maximizer Input -> Input Gain (0-127). **Same mappings as Org 1 Squash.**

### 8h. BASS TONEWHEEL (Bass Tonewheel insert, patch name "Tonewheels - Jazz Perc"; Seen)
- Front: knobs Lo Drive, Hi Drive, Balance, Reverb (Reverb has a green frame = automated); buttons Perc (lit), Perc 2nd/3rd (lit), Click (lit), Chorus (unlit, green frame = automated). Pitch and Mod wheels.
- Inside (Devices view), top to bottom: Combinator Mixer, micromix "OUT MIX", RV7000 MkII "RV7000 1" (patch "ALL Cl Sml Hall"), reMIX "DRAWBAR MIX", CF-101 "CHORUS/FLAN...", MClass Stereo Imager "M STEREO 1", Scream 4 "LOW", Spider Audio "LOW" with CF-101 "LOW L" and "LOW R", Scream 4 "HIGH", Spider Audio "HIGH" with CF-101 "HIGH L" and "HIGH R", SubTractor "DRAWBARS 1-2", two Spider CV splitters, SubTractor "DRAWBARS 3-4", SubTractor "PERC", and (Editor list only) a fourth SubTractor "Single Trig". So it is a drawbar organ made from four SubTractors, each on Init Patch (the sound lives in the Combinator, not in a SubTractor patch).
- Routing read (Editor, rows clicked; min-max as shown):
  | Device | Source -> Target |
  |---|---|
  | Out Mix (Line Mixer) | Balance -> Channel 2 Level (118-63, reversed) and Channel 1 Level (118-63, reversed); Balance -> Channel 3 Level (63-127) and Channel 4 Level (63-127); Reverb -> Aux Return Level (0-127) |
  | Drawbar mix (Mixer) | Perc (button) -> Channel 3 Mute (1 to 0, reversed); Chorus (button) -> Aux 1 Return Level (0-127) |
  | Low (Scream) | Lo Drive -> Damage Control (0-60) and Master Level (127-63, reversed) |
  | High (Scream) | Hi Drive -> Damage Control (0-60) and Master Level (127-63, reversed) |
  | Drawbars 1-2 (SubTractor) | Mod Wheel -> LFO1 Rate (28-79) |
  | Drawbars 3-4 (SubTractor) | Click (button) -> Noise On/Off (0-1); Mod Wheel -> LFO1 Rate (28-78) |
  | Perc (SubTractor) | Perc 2nd/3rd (button) -> Osc Mix (0-127) |
  | RV7000 1, Chorus/Flanger 1, M Stereo 1, Single Trig | none |
- Reading: Balance crossfades two pairs of mixer channels (the low and high drawbar banks; **Guess**), and each Drive knob both raises a Scream's Damage and lowers its output to compensate (Master Level runs down as Damage runs up).
- Not clicked: the Spider Audio and Spider CV rows and the four CF-101 rows (splitters and chorus; none expected, **Guess**).

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
