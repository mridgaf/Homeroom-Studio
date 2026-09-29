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
