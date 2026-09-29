# What the Airplane demo song teaches

**Song:** Carlström, "Airplane" (`~/Music/Reason 12/Demo Songs/Carlstrom - Airplane.rsndemo`).
**Explored:** 2026-09-29, step 00c of OPEN-ISSUES (paused once by the owner's limits, then resumed).
Claude can't hear, so this comes from the screen, the meters, the Reason 12.7 manual and the project files.
**Lists that go with this:** [phrase ideas](demo-song-phrase-ideas.md) (section F) · [skill ideas](demo-song-skill-ideas.md) (rows marked Airplane)
Same tags as the Street Phone notes ([demo-song-notes.md](demo-song-notes.md)):
**Seen** = on screen · **Manual** = Reason 12.7 manual, place named · **Guess** = not confirmed.
Manual places are line numbers in `~/.reason_voice/reason12_manual/Reason_12.7_Operation_Manual_Full_Text.md`.

## Where it ended
- **Closed 2026-09-29 with Don't Save.** The dialog named "Carlstrom - Airplane.rsndemo" before I answered.
- **Demo file unchanged:** SHA-1 before opening and after closing are both
  `91a2df7aedba4313b274f45511b2046c72575649` (5,242,932 bytes, dated Sep 4 2023). The `ls` line now shows an
  "@" flag on the file. `xattr -l` shows it is only macOS's "last used date" tag (`com.apple.lastuseddate#PS`),
  which the Street Phone file has too. The contents are identical.
- **Second visit, same day, after the owner approved screen control:** Airplane was reopened only to look at the
  jack pop-up menus and tooltips (section 5). Closing it this time showed **no save dialog** (nothing had been
  changed), and the window simply closed. SHA-1 checked again afterwards: identical.
- The scratch song "Step 8 test copy 09 29 26" is still open and unsaved, as before.
- Not done from the brief: re-patching a cable, soloing, a deliberate sweep edit, Combinator Modulation Routing,
  and every "needs ears" check (section 8).

## 1. The song itself
- **Seen:** title bar "Carlstrom - Airplane.rsndemo [Reason 10 Demo Song] [Read-only]". 125.000 BPM, 4/4.
- **Seen:** the info card says Carlström is Ludvig Carlson and Mattias Häggström Gerdt, who "make demo
  songs" when not changing the world of music making. Web page www.propellerheads.se. E-mail: n/a.
  No notes about how the song is built.
- **Does Reason itself say anything about this song?** Only partly checked. The manual text has no hit for
  "Carlstrom" or "Airplane"; Spotlight finds only the song file (and OPEN-ISSUES.md, which I wrote).
  Not repeated for this song: the Reason app folder, Reason Companion, the Showcase file.

## 2. Mixer (Seen)
18 channels, left to right. "Output" is the grey label under each channel.

| # | Channel | Output goes to |
|---|---|---|
| 1 | Nightclub Saw | blank label (Master Section) |
| 2 | Punch Drunk Saw | blank label (Master Section) |
| 3 | Fifth Dimension | **Sidechain Bus** |
| 4 | Unisaw | **Sidechain Bus** |
| 5 | Kick | blank label (Master Section) |
| 6 | Hi-hat | blank label (Master Section) |
| 7 | Clap and Hats | blank label (Master Section) |
| 8 | Ending Top | blank label (Master Section) |
| 9 | Mushi | blank label (Master Section) |
| 10 | Norwegian Boy -LNB | **Sidechain Bus** |
| 11 | Mothership Landing | blank label (Master Section) |
| 12 | Boomer Bass | **Sidechain Bus** |
| 13 | Please Release | blank label (Master Section) |
| 14 | Pulse Scream | blank label (Master Section) |
| 15 | Crash | **Sidechain Bus** |
| 16 | Stereo Noise | **Sidechain Bus** |
| 17 | Stereo Noise | **Sidechain Bus** |
| 18 | Sidechain Bus (pink, red fader knob) | "Master Section" (read on its rack device, section 4) |

- **Seen:** channels 1-17 have a blank grey Output label, or a pink one naming "Sidechain Bus". **Manual [17] (line
  ~12257):** the default destination is the Master Section, so a blank label means Master Section. I read
  "Master Section" directly on the device only for the bus channel (section 4).
- **Seen:** FX return list on the Master Section: 1 = Plate, 2 = Room, 3 = Echo; 4 to 8 empty. Several
  channels have the send number buttons for 1, 2 or 3 lit blue.
- **Not known:** what a lit blue send button means on the Main Mixer. The manual line I found (~36318) is about
  the old Mixer 14:2 device (a "P" pre-fader button on Aux 4 only), so I am not applying it here.
- **Seen:** mixer channel names differ slightly from the rack device names: mixer "Please Release" is
  "Please Release Me" in the rack; "Pulse Scream" is "Pulse Scream -LC"; "Stereo Noise" is "Stereo Noise Sw...".
  Why is not known.

## 3. Rack, front view (Seen)
- **Seen:** the rack is drawn as two columns side by side that scroll together. A small map at the top right
  shows both. Wide left column first, narrow right column second (its right edge is cut off unless you drag the
  blue box in the map).
- **Top of the left column:** Hardware Interface ("MacBook Pro Speakers"), Master Section, RV7000 Mk II "PLATE"
  (patch "ALL 1st Plate"), RV7000 Mk II "ROOM" (patch "AMB Oak Room"), The Echo (patch "Warm Echo"). These match FX
  return 1, 2, 3.
- **Then, in the left column, top to bottom:**

| Track | What is in the rack under its Mix header |
|---|---|
| Nightclub Saw | Europa synth (patch "Nightclub Saw"), then a **Synchronous** effect (patch "Long Sidechain") |
| Fifth Dimension | Europa (patch "Fifth Dimension") |
| Punch Drunk Saw | Europa (patch "Punch Drunk Saw") |
| Norwegian Boy -LNB | **Dual Arpeggio** player, then a Combinator (patch "Norwegian Boy -LNB", "Plucks & Mallets" printed on it). Its face: Pitch and Wheel, four knobs Shift / Dirt / Width / Reverb Level, four buttons Hammer On (lit) / Compress / AM / Delay |
| Mothership Landing | Grain sample manipulator (patch "Mothership Landing", sample "wavecrash sweep 048.wav", motion "Freeze") |
| Boomer Bass | Grain (patch "Boomer Bass", sample "Bass Drum 608a - stretch", motion "End Freeze") |

  After Boomer Bass the left column ends in empty rack (an "Add device" area).
- **Right column, seen but order not confirmed:** Kick (Redrum, then Pulveriser 1 with a SQUASH knob),
  Hi-hat (Dr. Octorex), Clap and Hats (Redrum), two "Stereo Noise Sweep [Run]" channels (Thor synthesizers), Mushi (Grain, sample "Bird3.aif"), Unisaw (Europa), Ending Top (Dr. Octorex),
  Pulse Scream -LC (a Combinator; its inner devices are listed in the jack pop-up, see below), Please Release Me (Grain, sample "HRP_GL_Dwn(E3).aif"),
  Crash (an Audio Track device), Sidechain Bus (Mix Channel device).
- **Seen:** the Kick track uses the Redrum drum machine here (Street Phone used Kong).
- **Seen, full device list from the jack pop-up menu (section 5), in rack order:** Hardware Interface II, Master
  Section, Master Section FX (Combinator), Plate (RV7000), Room (RV7000), Echo (The Echo); then per channel:
  Nightclub Saw (Mix Channel, Europa), Long Sidechain (Synchronous), Fifth Dimension (Mix Channel, Europa),
  Punch Drunk Saw (Mix Channel, Europa), Norwegian Boy -LNB (Mix Channel, Default Arp = Dual Arpeggio,
  Combinator), Mothership Landing (Mix Channel, Grain), Boomer Bass (Mix Channel, Grain), Kick (Mix Channel,
  Redrum, Pulveriser 1), Hi-hat (Mix Channel, Dr. Octo Rex), Clap and Hats (Mix Channel, Redrum "Clap"),
  Stereo Noise Sweep [Run] (Mix Channel, Thor) twice, Mushi (Mix Channel, Grain), Crash (Audio Track),
  Sidechain Bus (Mix Channel), Sidechain Bus FX (Combinator), Unisaw (Mix Channel, Europa), Ending Top (Mix
  Channel, "ny_drm124_ruff_top" Dr. Octo Rex), Pulse Scream -LC (Mix Channel, Combinator), Please Release Me
  (Mix Channel, Grain). Devices inside a Combinator are not in the main list; they show under the Combinator's
  sub-menu. New from this: **there is a "Master Section FX" Combinator** which I had not
  spotted on the front view (Guess: it is the master insert; blue cables enter the Master Section's Insert FX slot on the back view).
- **Seen (Pulse Scream -LC sub-menu, first rows only, list not scrolled to the end):** Spider Audio 1, EasyFuzz
  (Scream 4), First Mix (Line Mixer 6:2), AMB Blue Room (RV7000), Pulse Osc (Pulsar), Filter__ (ECF-42 Filter),
  Vibrato (Pulsar).

## 4. The Sidechain Bus, in detail (Seen unless marked)
This is the main thing this song shows that Street Phone did not.
- **The bus is a Mix Channel device** in the rack. On its back panel the Input section says "INPUT DISABLED,
  CHANNEL IS USED AS OUTPUT BUS" with a red light lit. Its Audio Output reads "Master Section".
- **Manual [17], "Output Busses" (lines 12600-12660):** an Output Bus is a sub-mixer. You route channels to it with
  the Output selector on the channel strip (or Cmd-G on selected channels, or on the device's Audio Output
  dropdown). The bus channel gets a coloured fader background and a red fader knob. The device's Audio
  Output then shows the bus name instead of "Master Section". All of that matches what is on screen: the
  Boomer Bass Mix Channel device reads "Audio Output: Sidechain Bus", and so does the Crash Audio Track device.
- **Seen (jack pop-up menu, section 5): none of the 18 channel devices has a cable in its Side Chain Input.** In
  each one's sub-menu "Side Chain Input L" and "R" have no asterisk (an asterisk means already cabled). The only
  device with "From Insert FX L/R" marked occupied is the Sidechain Bus. So there is no keyed sidechain anywhere
  in this song (the Master Section's own sidechain jacks looked empty on the back view; not checked in a menu).
- **Seen:** on the bus Mix Channel and on Crash, the "Sidechain Input" jacks (the Dynamics section, with a KEY
  button) have **no cables**, and the KEY button does not look lit. So nothing is keyed through those jacks.
  My first guess (the Kick feeds the bus's sidechain input) was **wrong** for these jacks.
- **Seen:** the bus channel's Insert FX slot is filled. "To device" and "From device" jacks have blue cables
  going to a **Combinator** (name label "SIDECHAIN BU...", patch "Init Patch"). The Combinator's four
  Control knobs and four Switches have no labels (Control 1-4, Switch 1-4).
- **Seen:** under a strip labelled "COMBINATOR / MIXER" (Guess: the Combinator's built-in mixer), inside the
  Combinator's frame, sits a **Synchronous** "Timed Effect Modulator" (patch "Long Sidechain"), with green audio cables from its Audio In and Audio Out jacks up to the
  Combinator's Input and Output. Its CV In and CV Out jacks have no cables.
- **Seen (front of Synchronous):** rate buttons with 1/4 selected, speed x1, three curve lanes (yellow 1,
  pink 2, blue 3), FRZ and KILL buttons per lane. Lane 2 (pink) shows a curve that starts near the top on the
  left, falls to the bottom by about its third column and stays at the bottom to the end of its four columns; a
  loop marker at the top spans those four columns. Lanes 1 and 3 show no curve. A row of ten small modulation dials sits
  above the ten effect knobs. Only the one over the last knob, **Level**, has coloured rings; the other nine
  look plain.
- **Manual [60], "Synchronous Timed Effect Modulator" (lines ~33125-33692):** you draw up to three modulation
  curves, and a row of "modulation control" dials sets how much each curve affects each effect knob. Its Level
  section says (about line 33590): if the Level is modulated by a curve, the volume rises above the Level
  knob's setting by the modulation amount.
- **Seen:** the Level modulation dial looks turned toward "+" (the pointer sits near the + mark; not measured).
- **Guess (not tested, not heard):** the curve is a repeating volume shape, a pumping effect without any
  sidechain cable. Whether it dips the sound on the beat or swells it (the manual says modulation raises the
  volume above the Level setting, and I don't know this patch's Level setting) I can't tell from the screen.
  To check: hear it, or compare the bus meter at fixed points. Not done.
- **Seen:** the "non-standard routing" warning is printed on the bus device, but its small light looks dark (a tiny dot; not certain).
  **Manual [18] (line ~13346):** that light comes on when Reason detects non-standard routing; hovering over it
  shows why. If it is dark, Reason is reporting no problem; I did not hover.
- **Seen:** Nightclub Saw has its own Synchronous "Long Sidechain" in the rack too. Hovering Nightclub Saw's
  Europa "Audio Left" jack shows the tooltip "Connected to Long Sidechain: Left Input", so that Europa plays
  through its own Synchronous. That Synchronous is folded to a strip in this song. Where its output goes:
  not checked (Guess: to the Nightclub Saw Mix Channel input, which the menu shows as occupied).
  Why only that track has one: not known (Guess: it is not routed to the bus, so it gets its own pumping).
- **Seen (pop-up sub-menu of "Sidechain Bus FX (Combinator)"):** "Combi Input Left/Right" and "Mixer Input
  Left 1 / Right 1" are marked occupied, Mixer Inputs 2 to 8 are free, and "Long Sidechain (Synchronous)" is
  listed inside it. That confirms the Synchronous sits inside that Combinator.

## 5. Cables (back view)
**The full wiring map is in [demo-song-wiring-airplane.md](demo-song-wiring-airplane.md)** (fourth visit, 2026-09-29). It
supersedes the sample below where they differ. Three things it added or corrected: the Pulse Scream -LC Combinator has no
synthesizer (a Pulsar LFO is used as the audio oscillator, with CV cables between Pulsars); the Norwegian Boy -LNB Combinator
holds two Malstrom synths ("Kalimba L / R") with a mixer, Pulveriser, Echo and compressor; and the Redrum send outputs are
unconnected (my earlier "has a cable" was a misreading). The "no CV cable anywhere" idea was wrong, see section F there.
- **Manual [16], "About cables" (lines 11430-11500):** the colours are green for effect devices, red for
  instrument to mixer, yellow for CV, blue for Combinator. [K] or Options > Reduce Cable Clutter toggles a
  view that shows fewer cables. Hover over a jack for a tooltip naming the device and jack at the other end.
  Click-and-hold (or Ctrl-click) on a jack gives a menu with "Scroll to Connected Device".
- **Seen and matching that:** Grain and Europa to their Mix channel are red or orange cables; the Norwegian Boy
  Combinator's Output goes up as a pair of blue cables toward its Mix channel (not confirmed by tooltip); the two
  Synchronous audio pairs are green.
- **Seen:** Grain back panel (Mothership Landing): Sequencer Control (Gate, CV, Pitch Bend, Mod Wheel) and
  CV Modulation In/Out 1-4 all empty. Only audio is cabled.
- **Seen:** the Norwegian Boy Combinator back panel: Gate In, CV In, four "Control CV In" jacks with dropdowns
  reading Shift, Dirt, Width, Reverb Level (the same four labels as the front knobs). Their jacks look empty.
- **Owner's tip, 2026-09-29: "The back has drop downs to see all cables."** Tried after the owner approved
  screen control. **Seen:** Ctrl-click on a jack opens a menu. Top of the menu: "Scroll to Connected Device",
  "Route to New Mix Channel", "Disconnect". Below that, a list of EVERY device in the rack. A **check mark** sits
  on the device this jack is cabled to (here "Plate (RV7000)" for FX Send 1 Left), devices with no suitable
  jack are greyed, and hovering a device opens a sub-menu of its jacks: a check mark on the one this cable
  uses ("Left Input") and an **asterisk** on jacks that already have a cable ("Right Input *"). That matches
  Manual [16] (lines 11646-11660), and it is very likely what the owner meant, though he did not say so.
- **Seen, hover:** resting the pointer on a jack shows a tooltip such as "Connected to Long Sidechain: Left Input"
  (Nightclub Saw's Europa) and "...d to Plate: Left Input" (FX Send 1 Left; the first word is hidden by a second
  small label reading "Reason Sounds"). Matches Manual [16] line ~11470.
- **How the menu behaved (Seen):** Escape closes only sub-menus, not the main list. The list scrolls while the
  pointer rests on the arrow at its bottom edge. Clicking the window's title bar closed it. I picked no item;
  the cables looked the same afterwards on screenshots (not diffed). Picking a device would replace the cable.
- **Seen (Master Section back):** FX Send 1, 2, 3 and FX Return 1, 2, 3 have cables and 4 to 8 have none, to
  (the Send 1 tooltip names Plate; I did not read tooltips for Sends 2 and 3, whose Return names are Room and Echo).
- **Wiring read by hover tooltip (Seen, third visit, "Connected to ..." text quoted):**

| From (jack) | Connected to |
|---|---|
| Master Section FX Send 1 Left / 2 Left / 3 Left | Plate: Left Input / Room: Left Input / Echo: Left Input |
| Plate / Room / Echo outputs | Master Section FX Return 1 / 2 / 3 (Plate and Room read from the return side as "Plate: Left Output" and "Room: Left Output"; Echo as "Echo: Left Output") |
| Master Out Left | Hardware Interface II: Output 1 |
| Nightclub Saw Europa, Audio Left | Long Sidechain (Synchronous): Left Input |
| Nightclub Saw Mix Channel, Input L | Long Sidechain: Left Output |
| Fifth Dimension Mix Channel, Input L | Fifth Dimension (Europa): Left Output. Mix Channel Audio Output reads "Sidechain Bus" |
| Punch Drunk Saw Europa Audio Left | Punch Drunk Saw (Mix Channel): Input L |
| Mothership Landing Mix Channel, Input L | Mothership Landing (Grain): Left Output. Audio Output reads "Master Section" |
| Norwegian Boy Combinator, Output | Norwegian Boy -LNB (Mix Channel): Input R |
| Sidechain Bus Mix Channel insert: To Insert FX L / R | the Sidechain Bus FX Combinator (Combi Input) |
| Sidechain Bus Mix Channel insert: From Insert FX L / R | the Sidechain Bus FX Combinator (Combi Output) |

  Not read by tooltip (so **only cabled, source not read**): the input jacks of the other twelve channels' Mix
  Channels. Their pop-up menus showed "Input L *" and "Input R *" as occupied, so a cable is there.
  The Norwegian Boy Combinator's Input jack: hovering gave only its name, "Combi Input Left" (no "Connected to"),
  which may mean nothing is cabled to it (Guess); the Dual Arpeggio player is a Player, not an audio device, and
  reaches the Combinator without an audio cable (Guess, not traced).
- **Seen:** the RACK button under a mixer channel strip scrolls the rack to that channel's device. That was the easy way
  to reach the Sidechain Bus, which sits in the second rack column. (Mixer view: press RACK; then look at the rack.)
- **Seen, unexplained:** while reading tooltips in the Norwegian Boy area the rack scrolled by itself and the
  Mothership Landing back panel appeared unfolded, though I had not clicked it. I do not know why; it is a view
  change only and nothing was edited.
- **Folding:** the small triangle at the top left of a device folds it to a one-unit strip (Seen). I folded the
  Synchronous back panel that way. My first two attempts to unfold it missed the triangle (my aim, not a
  Reason quirk); the third worked and a screenshot shows it open again. View change only.

## 6. Sequencer and sweeps
**Song length. Seen:** the ruler with "zoom to fit" runs from a left marker at bar 1 to a right marker at about
bar 65, so about 64 bars. **My arithmetic, not played:** 64 bars at 125 BPM is about 2 minutes 3 seconds. The
transport read 0:01:25:440 at 45.3.1.0, which matches that pace.

**Track list, top to bottom (Seen).** Bar numbers are read off the ruler at 4-bar marks, so they can be off by
about one bar.

| Track (what it is) | Automation lanes | Where the clips are |
|---|---|---|
| Transport | none opened | none seen |
| Nightclub Saw (Europa) | "(Mod Wheel)", "Filter Mod" | notes 1-20 and 45-64. Mod Wheel: bar 9, 13-20, 45-61. Filter Mod: 1-5, 19-20, 61-65 |
| Punch Drunk Saw (Europa) | "(Mod Wheel)" | notes 9-20 and 45-61. Mod Wheel 9-13 |
| Fifth Dimension (Europa), plus a thin row of the same name | "(Mod Wheel)", "Eng3 Level" | notes 13-20 and 45-61. Mod Wheel 45-61. Eng3 Level 17-21 |
| Unisaw (Europa) | none | notes 45-61 |
| Mushi (Grain), plus a thin row of the same name | "Filter Freq", "Dist Amount" | main clip 21-45. Filter Freq clip 43-45 (toolbar: Position 43.1.1.0, Length 2.0.0.0). Dist Amount clip near 44. Thin row line 29-45 |
| Norwegian Boy -LNB (Combinator) | **"Shift"** | notes 29-45. Shift 29-45 |
| Mothership Landing (Grain) | "(Pitch Bend)" | 21-29. Pitch Bend 25-29 |
| Boomer Bass (Grain), thin row too | none opened | 21-46; thin row has small marks near 37 and 43-46 |
| Please Release Me (Grain) | none opened | about 25-30 |
| Pulse Scream -LC, thin row too | none opened | 33-46; thin row 37-45 |
| Kick, **thin row with a device icon** | **"LPF On/Off", "HPF On/Off", "FX1 Send On/Off", "Level"** | LPF and HPF: 1-13 and 61-65. HPF also near 20 and 44. FX1 Send: about 21-22. Level: 29-45 |
| Kick (Redrum) | "Pattern Select" | pattern "A1" blocks across 1-13, 13-21, 29-61 |
| Hi-hat (Dr. Octorex), thin row too | none opened | 13-21, 22-45, 45-61 |
| Clap (Redrum), two note lanes; thin "Clap and Hats" row | "Pattern Select" | 13-21 and 29-61 |
| ny_drm124_ruff_top (the "Ending Top" channel) | none | 45-61 |
| Crash (audio track) | none | short audio clips near 13, 20-21, 29, 37, 45, 53 |
| Stereo Noise Sweep [Run] (Thor), two tracks | none | short clips about every 8 bars (pink near 21, 25, 29, 37, 45, 53, 61; magenta near 10, 20, 30, 40, 49, 58) |

- **Seen:** the "Stereo Noise Sweep [Run]" tracks are a **Thor** synthesizer whose patch name is
  "Stereo Noise Sweep [Run]" (patch display in the rack). So the bracket is part of the patch name, not a
  control. My first guess (a Combinator "Run" button) was wrong.
- **Seen:** track names follow the device or patch name, or the loop file ("ny_drm124_ruff_top" is the name shown
  for the Dr. Octorex track, whose channel is "Ending Top").
- **Guess (not heard):** the clips every 8 bars in the Stereo Noise Sweep tracks and the Crash hits are risers
  and cymbal hits at section changes. Where tracks enter suggests sections near bars 1-13, 13-21, 21-29, 29-45,
  45-61, 61-65.

**How the lane names work (Seen, matched to the manual or files where marked)**
- The lane name is the parameter's name. Europa lanes read "(Mod Wheel)", "Filter Mod", "Eng3 Level"; Grain lanes
  read "Filter Freq", "Dist Amount", "(Pitch Bend)"; Redrum lanes read "Pattern Select".
- **Seen:** the Norwegian Boy Combinator's lane reads "Shift", the same word as the label on its front knob
  (section 3). So a Combinator lane takes the label the patch author gave the knob.
- **Seen + Manual [17] (lines 12112-12122):** the Kick thin row's lane names "LPF On/Off", "HPF On/Off",
  "FX1 Send On/Off" and "Level" are mixer-channel control names (the manual lists LPF ON and HPF ON buttons on
  the channel strip). **Guess:** that thin row is the Kick channel's own automation track; I did not open its
  header to confirm.
- **Seen (file):** `docs/reason/remote-vocab.json` has Reason's names "Channel N LPF On", "Channel N HPF On",
  "Channel N LPF Frequency" and "Channel N HPF Frequency" for every channel. Not tried.
- **Not known:** what the brackets in "(Mod Wheel)" and "(Pitch Bend)" mean. The manual text search found
  nothing on it.

**One clip opened (Seen).** Double-click on the Mushi "Filter Freq" clip opened it inline in the lane
(toolbar switched to EDIT INLINE / EDIT MODE). It shows three points joined by lines, rising from about
mid-height to the top over its 2 bars, with a horizontal line across the lane at mid-height and a value
readout "485.4 Hz" in the lane header. **Guess:** the horizontal line and the 485.4 Hz are the lane's Static
Value (Manual [6], lines 4380-4389: a parameter has a "static value" whenever it is not automated, and you can change it by opening the clip in Edit Mode); I did not confirm it. Direction
of the sound (filter opening) not heard. I clicked the EDIT INLINE button once afterwards; the lane shrank back
and the clip stayed selected. No point was dragged or typed.

## 7. What I did to the song (for honesty)
- Looked only. View switches (mixer, rack, sequencer), rack front/rear toggle, folding one device and unfolding
  it, unfolding automation lists, zoom to fit, moving the playhead to 45.3.1.0, playing for a few seconds while I
  watched the Synchronous display, stopping, opening one automation clip inline and pressing EDIT INLINE once.
- **Seen while playing:** a small pink marker moved along the top of the Synchronous curve grid across the first
  four columns, while the curve itself stayed the same. That fits a repeating dip, but it does not show the level
  going down, and I could not hear it.
- No knob was turned, no mute or solo pressed, no cable touched, nothing saved. The demo is read-only and
  was closed with Don't Save (see "Where it ended").
- **Second visit (screen control):** Ctrl-clicked the FX Send 1 Left jack twice to open its menu, hovered items
  and read sub-menus for all 18 channels, hovered two jacks for tooltips, scrolled the rack, dismissed each menu
  with a click on the title bar, then closed the window with the red button (no dialog, nothing changed).
- **Slips of mine, not Reason facts:** I clicked a fold triangle hoping it was the owner's cable drop-down and it folded the Synchronous back panel; two of my unfold clicks then missed before the third worked; two "app_key" and
  two "app_menu" calls returned "no verdict" from the safety check (transient; retried or worked around); the
  zoom-out buttons at the bottom left changed track height, not the timeline (my wrong guess about them).

## 8. Not looked at
- Combinator "Modulation Routing" for the Norwegian Boy Combinator (Manual [63]) and what its Control CV jacks do.
- Whether the pink Synchronous curve dips or swells the level (needs ears).
- Nightclub Saw's own Synchronous "Long Sidechain": its settings, and what feeds it.
- "Scroll to Connected Device" (not pressed) and most jack tooltips; only two were read.
- What a lit blue send button means on the Main Mixer, and each channel's send levels.
- The unnamed devices (Pulse Scream -LC, Stereo Noise Sw...) beyond their headers, and the Transport track.
- Everything that needs a listening check.

## 9. What this song adds to the running lists
- Phrase list: new section F in [demo-song-phrase-ideas.md](demo-song-phrase-ideas.md).
- Skill list: new rows in [demo-song-skill-ideas.md](demo-song-skill-ideas.md).
- Voice-app facts found while checking (files named, not tried live): the remotemap already has scopes for Europa,
  Grain, Redrum, Thor, Pulveriser, Synchronous and Combinator (Combinator = patch next/previous only). Europa's scope has
  "Filter Mod" and Grain's has "Filter Freq" and "Dist Amount", the same names as lanes this song automates. The
  Synchronous scope has Level, Filter, Dist, Delay and Reverb knobs but not the modulation-amount dials. Redrum's scope
  has nothing for pattern. Dr. Octorex has no scope (no "Octo" in the remotemap, calibration or vocab).
