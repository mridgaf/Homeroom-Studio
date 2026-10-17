# Chapter 09: Reason 12 manual digest and studio workflow
## Part 21 of 25

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- demo-song-notes-power.md — BLKMGK - Power (Reason 12 demo song, step 00d)
- demo-song-notes-quazmo.md — Qua z mo - I Just Wanna Be (Reason demo song, step 00e)

(Next: Part 22 of 25)


=====================================================
SOURCE FILE: demo-song-notes-power.md
ORIGINAL LOCATION: HS:docs/reason/demo-song-notes-power.md
=====================================================

# BLKMGK - Power (Reason 12 demo song, step 00d)

Started 2026-09-29. Owner (2026-09-29): "Can you find the other demo songs for reason, are there any hip hop ones, maybe
online... start with one of those beginning alphabetically hip hop priority", then "begin learning and wiring the first one
alphabetically". Same rules as [Street Phone](demo-song-notes.md) and [Airplane](demo-song-notes-airplane.md): tags **Seen**
(on screen) / **Manual** (Reason 12.7 manual, line numbers in `~/.reason_voice/reason12_manual/Reason_12.7_Operation_Manual_Full_Text.md`)
/ **Guess** (not confirmed). Never saved, closed with Don't Save after reading the dialog. My own slips are labelled as mine.
Nothing here was heard.

## 0. Where the song came from (Seen)
- Not on this Mac before today. Reason Studios' demo-song page (reasonstudios.com/download/reason/demo-songs/) lists 10 demo songs.
  Two are hip hop: **BLKMGK "Power"** (page says "HipHop/RnB track ... cleverly cut up and pitched vocals") and **Qua z mo "I Just Wanna Be"**
  (HipHop, Neptune Pitch Adjuster). Alphabetical first hip hop = BLKMGK. Owner said yes to downloading Power only (clickable answer).
- Downloaded from `https://cdn.reasonstudios.com/demo-songs/BLKMGK-Power.zip` (33,156,523 bytes, same as the server's content-length)
  to `~/Downloads/Reason Demo Songs/`. Unzipped `BLKMGK - Power.rsndemo` (41,680,948 bytes, file date 2015-01-08).
  **SHA-1 before opening: `704ee4ff38319a70d214e907afb9af65375c45f9`.**
- Other songs on this Mac that are not hip hop: Com Truise "Humint Algoritm" (in Downloads, 2022 giveaway folder), plus the template
  songs "Song Starter - Soul Hop" and "Song Starter - Trap" in `~/Music/Reason 12/Template Songs/` (templates, not demos).
- Not downloaded (needs a yes): Qua z mo (63,484,511 bytes) and the other seven demo songs.

## 1. Song info (Seen, Song Information window)
- Title bar: `BLKMGK - Power.rsndemo [Reason Demo Song] [Read-only]`.
- Text: "Reason 8 demo song by BLKMGK from Sweden/USA. Check us out at soundcloud.com/blkmgkofficial. This song requires Audiomatic to
  sound correct. Download it for free from www.propellerhead.se." Web page soundcloud.com/ (link "Browse"), e-mail shown.
- Tempo 84 BPM, 4/4 (transport bar, Seen).
- **Audiomatic:** the info says the song needs the Audiomatic Rack Extension. It is installed here and used (section 4b), and no missing-device message appeared.

## 2. Sequencer tracks (Seen, 18 rows)
Transport, Jayy vox comp (audio track, yellow waveform, from bar 1), Jayy echo (a device with a "Dry/Wet Balance" lane), Kong half, Kong double,
Kong FX (three Kong drum tracks, pattern lane "A1"), Drum loop (a lane "HPF Frequency"), Drum loop (loop player, "A1"), Bass ("A2"), Bass arp,
Piano L, Piano R, Mal L, Mal R (red note tracks, "A2"), Wub M, Rave M, Wub R (light blue note tracks), Resample (audio track, orange).


## 3. Arrangement (Seen; 42 bars at 84 BPM, read from clip positions at "Show All" zoom, so bar numbers are approximate)
| Bars | What plays (Seen) |
|---|---|
| 1-3 | Jayy vox comp (audio, whole song bars 1-40), Piano L; Piano R joins about bar 3 |
| 3-9 | Kong half, Kong FX, Drum loop (loop player), Bass, Piano L/R, Mal L/R |
| 9-11 | Piano L only, then a one-beat blip on Bass, Piano R, Mal L/R at bar 11 |
| 11-19 | Kong half, Kong double, Kong FX, Bass arp, Wub M, Rave M, Wub R |
| 19-25 | thin: short Bass and Kong double bits; Resample audio hit at about bar 24.5 |
| 25-29 | Piano L/R, Mal L/R, Bass, Drum loop, Kong FX, plus the "HPF Frequency" lane clip on the Drum loop channel (about bars 25-29, slightly sloped) |
| 29-40 | Kong half, Kong double, Kong FX, Bass arp, Wub M, Rave M, Wub R, vocal to bar 40 |
| 40-42 | one Bass hit at about 40.5; "Jayy echo" lane clip "Dry/Wet Balance" (bars ~40-42) |
Song end marker at about bar 42. **Guess:** verse (3-11), hook (11-19), break (19-25), verse (25-29), final hook (29-40), echo tail.

## 4. Rack rear, read by hover (Seen; tooltip "Connected to <device>: <jack>")
The rack has TWO columns (Seen in the rack navigator): a long left column and a short right column (Thors, Redrum). Rear view: Tab key
flips it (worked while the mouse tools were blocked); PageUp/PageDown scroll the rack (worked). Mixer channel strips sit directly ABOVE
their instrument; the inserts sit directly BELOW the instrument and carry the channel name, and the last insert feeds the strip above the instrument.
Whether the owner unfolded devices before I looked: some devices were already unfolded when I read them (the owner opened a few to show me).

### 4a. Master Section and effects
| From | To |
|---|---|
| Master Section FX Send 1 L/R | Plate (RV7000) Audio Input L/R |
| Send 2 L | Room (RV7000) Audio Input L |
| Send 3 L/R | The Echo 1, Main Input L/R |
| Send 4 L | The Echo 2, Input L |
| Send 5 L | Unison (UN-16) Left in |
| FX Returns 1-5 | Plate L out, Room L out, The Echo 1 out, The Echo 2 out, Unison out (Echo 1 read on both L and R; Unison out read on L and R as "FX 5 Return L/R") |
| Master Out L/R | Hardware Interface II: Output 1 / Output 2 |
| Control Room Out L, Side Chain Input L | tooltip shows the jack name only: **not connected** |
So five send effects: Plate, Room, two Echoes and a Unison chorus (Seen). Room Audio Input R and the Echo 2 R jacks were not read.

### 4b. Kong half, Kong double, Kong FX (three Kong drum machines, each with its own insert chain)
- Kong half: Main Audio Out L/R -> **Kong audiomatic** L/R input; Audiomatic output L/R -> **Kong pulveriser** L/R input; Pulveriser output L/R -> **Kong half mix channel** Input L/R. Aux send 1 and 2 jacks: not connected. Audiomatic CV inputs (Transform, Dry-Wet): not connected.
- Kong double: Main Audio Out L/R -> Kong audiomatic L/R input (same pattern; Pulveriser and strip not read).
- Kong FX: Main Audio Out L -> Kong Audiomatic Left Input; rack shows Audiomatic, Pulveriser, then **MClass Equalizer "KONG FX EQ"** before its strip. Not every link read.
- The strips' Insert FX jacks read "From Insert FX L" (jack name only) on Drum loop: unused.
- **Audiomatic (Retro Transformer) is installed** and used as an insert on the Kong channels, Drum loop and Bass (labels "KONG AUDIOM...", "DRUM LOOP A...", "BASS AUDIOM..."). The song info says the song needs it; the rack loaded without a missing-device message (no dialog appeared).

### 4c. Drum loop and Bass
- Drum loop = **Dr. OctoRex** (label "DRUM LOOP") -> MClass Compressor "DRUM LOOP C..." -> Audiomatic "DRUM LOOP A..." -> MClass Equalizer "DRUM LOOP EQ" -> Drum loop strip. Read: Audiomatic Left Output -> Drum loop eq Left input (Seen), Drum loop eq output R -> "Drum loop: Input R" (Seen). Compressor and Dr. OctoRex jacks not read.
- Bass = **Malstrom** "BASS": main out L/R -> **Bass com** (Compressor) Left/Right (Seen); chain then "BASS EQ", "BASS AUDIOM..." (shown, links not read).
- **Bass arp = RPG-8 arpeggiator ("BASS ARP") cabled into the Bass Malstrom with CV/gate cables** (Seen by hover): Malstrom Gate <- Bass arp: Gate; CV <- Bass arp: Note; Mod Wheel <- Bass arp: Mod Wheel; Pitch Wheel <- Bass arp: Pitch Bend.
- **Bass sidechain:** the right-hand rack column holds a Redrum labelled "BASS SIDECHA..." whose Output 1 L/R are cabled to **Bass: Side Chain Input L / R** (Seen). The Bass channel's dynamics "KEY" button was lit in the mixer (Seen). Kick-shaped pump for the bass from a dedicated Redrum. What triggers that Redrum (no matching track seen): not read yet.

### 4d. Piano L, Piano R, Mal L, Mal R
- Piano L = **NN-XT**: Out 1/L and 2/R -> **Piano L comp** (MClass Compressor) L/R (Seen); chain in the rack: Compressor "PIANO L COMP", Equalizer "PIANO L EQ", **Scream 4** "PIANO L SCRE...", Equalizer "PIANO L EQ S..."; last Equalizer output L/R -> **Piano L: Input L/R** (Seen).
- Piano R = NN-XT with the same four inserts ("PIANO R COMP", "PIANO R EQ", Scream 4, "PIANO R EQ S...") (Seen labels; jacks not read).
- Mal L, Mal R = **Malstrom** each, with Compressor "MAL x COMP", Equalizer "MAL x EQ", Scream 4 "MAL x SCREAM", Equalizer "MAL x EQ SCR...". Mal R main out L/R -> **Mal R Comp** L/R (Seen).
- Piano L and Piano R are two NN-XTs (a "Piano" split into two devices) and Mal L / Mal R two Malstroms; whether they are the same patch panned apart: **Guess**, not checked.

### 4e. UN-16 Unison
- UN-16 Unison (rack, red): Left in <- Master Section FX 5 Send L; out L/R -> FX 5 Return L/R (Seen). Used as a send effect (chorus/unison) on send 5 (front panel shows Detune and Dry/Wet knobs and a voice-count switch, Seen; that it is a chorus-type device is **Guess** from the name, manual not checked).

### 4f. Jayy vox comp and mixer outputs
- "Jayy vox comp" is an Audio Track device with the strip "Jayy vox comp" and "Audio Output: Master Section" (Seen).
- The Kong half channel's Audio Output also reads Master Section (Seen); the other channel outputs were not read.

### 4g. Right-hand rack column: Thors, Resample, Redrum (Seen)
- **Wub M** = Thor. Its Audio Output 1 Mono/Left and 2 Right are cabled to **Wub audiomatic** Left/Right Input (the folded Audiomatic below it, label "WUB AUDIOMA..."); the strip above it is "Wub M". Audiomatic to strip: not read.
- **Rave M** = Thor: Audio Output 1/2 -> **Rave M: Input L / R** (straight to its strip, no insert).
- **Wub R** = Thor: Audio Output 1/2 -> **Wub R: Input L / R** (straight to its strip).
- The Thors' Modulation Output jacks (CV 1-4, Global Envelope, LFO 2) read as bare jack names ("Modulator 1", "Modulator 2"): **no CV cables** on the ones I hovered. Two green cables that look like CV are the Wub M audio cables to the Audiomatic (Seen).
- **Resample** = an Audio Track device (folded strip, orange), no cables. Its clip is a short hit at about bar 24.5 (section 3).
- **Redrum, label "BASS SIDECHA..."** (last device in the right column, only rear and front looked at):
  - Rear: channel 1 Left and Right audio outputs -> **Bass: Side Chain Input L / R** (Seen, both tooltips). Gate In 1, Gate Out 1, Pitch 1 CV, Send 1 and Stereo Out L: bare jack names (**not connected**).
  - Front: patch "Init Patch"; channel 1 holds a sample named "Bd_404Tig..." (a bass drum, name cut off); channels 2-10 empty; **pattern A1, 16 steps, resolution 1/16, steps 1, 5, 9 and 13 lit** (four to the floor); "Enable Pattern Section" LED lit; **RUN button looked unlit** with the transport stopped.
  - It has **no sequencer track** (18 rows listed in section 2). So it can only sound if its own pattern section runs with the transport. **Whether it really runs: unknown** (needs a play test and a look at the Bass compressor meter, or ears). I did not press Play (audible).

## 6. Mixer (Seen; Main Mixer, values read at song position 1.1.1.0)
- 14 channels, left to right: Jayy vox comp (yellow), Kong half, Kong double, Kong FX, Drum loop (grey-green), Bass, Piano L, Piano R, Mal L, Mal R (red), Wub M, Rave M, Wub R (light blue), Resample (orange, beyond the edge; not read). Colours match the sequencer track colours.
- FX send names: 1 Plate, 2 Room, 3 Echo, 4 Echo 2, 5 Unison, 6-8 blank. Every send button in a channel strip is a numbered button; **Manual [17] line 12219-12224: the numbered button is "FX Send On" and PRE takes the send before the fader.** I read lit blue as "send on" (my reading; the button also carries the word PRE, so I could not tell the PRE state from the picture).
| Send | On (blue) | Off |
|---|---|---|
| 1 Plate | Jayy vox comp, Kong FX, Piano L, Piano R, Mal L, Mal R, Rave M, Wub R | Kong half, Kong double, Drum loop, Bass, Wub M |
| 2 Room | all 13 | none |
| 3 Echo | Kong half, Kong double, Kong FX, Drum loop, Piano L, Piano R, Mal L, Mal R, Wub M, Rave M, Wub R | Jayy vox comp, Bass |
| 4 Echo 2 | none | all 13 |
| 5 Unison | all 13 | none |
- So **send 4 (Echo 2) is unused by every channel** at song start, and the vocal (Jayy vox comp) has send 3 and 4 off. Whether an automation lane turns them on later: no such lane seen. Levels are knob positions only (not read as numbers).
- **Bass channel: the dynamics "KEY" button is lit** (Seen), matching the Redrum cables into its Side Chain Input. Every channel strip also has its compressor "ON", with the gate sections mostly off.
- **Drum loop channel HPF Frequency knob has a green frame** (automated parameter, **Manual [6] lines ~2954-2965, 4303: green borders mark automated parameters**). Its tooltip read "High Pass Filter Frequency: 121.2 Hz" at the start (Seen; that value is where the song starts, before the lane).
- Both strips whose Audio Output I read (Jayy vox comp, Kong half) say "Master Section" and the Insert FX jacks I read on Drum loop are unused (Seen). The Output labels under the faders were blank on every channel I saw (blank = default to the Master Section, my reading from Airplane).

## 7. Automation lanes (Seen, shape only)
- **Drum loop channel "HPF Frequency"**: one clip at about bars 25-29; in a zoom it is a nearly flat line with a small slope and the cut-corner end. Direction and amount: not read (needs the lane opened).
- **Jayy echo "Dry/Wet Balance"**: one clip at about bars 40-42; in a zoom the line dips a little then rises. A device on The Echo/echo type has a Dry/Wet knob (the two Echoes in the rack have one, Seen), **but which device "Jayy echo" is I did not resolve** (The Echo 1 or The Echo 2; I tried selecting the track and looking at the rack and it did not scroll to it).
- No other automation lanes were listed under any track (17 track rows plus Transport).

## 8. What I did and my slips (mine, not Reason facts)
- Opened the demo with `open -a`; no missing-device dialog. Never pressed Play, never saved.
- **My slip:** my first mouse scroll on the mixer ran while the pointer was over the mixer controls. I checked the Edit menu (it read plain "Undo" with no action named) and the song is read-only, so I believe no value changed. A tooltip showing "High Pass Filter Frequency: 121.2 Hz" is the automated knob's current value, not a change.
- I guessed by eye where a few long cables went (for example a dark-green cable running down through the Kong devices, and the two green cables on the Wub M Thor) before hovering. Only tooltip reads and printed labels are in this file as fact. One long dark-green cable running down the left column was never traced (unresolved).
- The owner showed me the rack by unfolding devices and scrolling while I watched (his words: to see "how much of that rack you can open up in the back and see how everything is connected"). I did not unfold or fold anything myself in this song.
- Blocked tools: the macOS Dictation overlay (orange microphone dot) made every mouse **click** and **scroll** fail ("would land on Dictation") but not hover, keyboard, or the background app tools. Hover reads worked throughout.

## 9. Not read yet
- Wub M Audiomatic to strip; Bass chain end (EQ, Audiomatic, strip); Kong double and Kong FX chain ends; Piano R and Mal chain middle links (order taken from the rack order); Dr. OctoRex jacks; RPG-8 own inputs; Resample mixer channel; Thor patches and what the Wubs sound like.
- The Redrum trigger (see 4g), which device "Jayy echo" is, the lane values.
- Every strip's Output routing except Kong half and Jayy vox comp.

## 10. Where it ended (Seen)
- Closed with the red button; **no save dialog appeared** (the file is read-only). `BLKMGK - Power.rsndemo` SHA-1 after: `704ee4ff38319a70d214e907afb9af65375c45f9` (same as before). Airplane `91a2df7a...` and Street Phone `e377af37...` unchanged.
- Reason still has only the scratch song "Step 8 test copy 09 29 26" open and unsaved. The zip and unzipped song stay in `~/Downloads/Reason Demo Songs/` (nothing deleted).
- Lists updated from this song: [phrase ideas](demo-song-phrase-ideas.md) section G, [skill ideas](demo-song-skill-ideas.md) (3 rows), [template and automation ideas](demo-song-template-and-automation-ideas.md) (7 template rows, 2 automation rows). OPEN-ISSUES 40-43, DECISIONS entry.

=====================================================
SOURCE FILE: demo-song-notes-quazmo.md
ORIGINAL LOCATION: HS:docs/reason/demo-song-notes-quazmo.md
=====================================================

# Qua z mo - I Just Wanna Be (Reason demo song, step 00e)

Started 2026-09-29 after the owner picked "Qua z mo next" (clickable answer) following the BLKMGK "Power" visit. Same rules
as [Power](demo-song-notes-power.md), [Airplane](demo-song-notes-airplane.md), [Street Phone](demo-song-notes.md): tags
**Seen** / **Manual** / **Guess**; never saved; my own slips labelled as mine. Nothing was heard. This visit is a **first
pass**: the whole rack was scrolled and the master and Pad FX chains were hovered, but most channel cables were not.

## 0. Where the song came from (Seen)
- Reasonstudios.com demo page, hip hop entry ("A HipHop track ... shows great use of the Neptune Pitch Adjuster"). Owner said yes to this
  download. `https://cdn.reasonstudios.com/demo-songs/Quazmo-IJustWannaBe.zip`, 63,484,511 bytes (same as the server), saved in
  `~/Downloads/Reason Demo Songs/`. Unzipped `Qua z mo - I Just Wanna Be.rsndemo` (89,129,012 bytes, dated 2015-01-08).
- **SHA-1 before opening: `290f75ff1e5713ca9e4316b31f907da80ec8d25c`.**

## 1. Song info (Seen)
- Title bar: `Qua z mo - I Just Wanna Be.rsndemo [Reason Demo Song] [Read-only]`. A photo of the artist shows in the splash.
- Text: written and produced by Qua z mo, "2014 American Boys Entertainment / Starmaker Management", @Quazmo, and "This song requires
  Audiomatic to sound correct." (Audiomatic is installed here and used; no missing-device message.) Tempo **97.290 BPM**, 4/4.

## 2. Sequencer (Seen; about 88 bars at "Show All")
30 rows. Names: Drum Loop, Bass, Spunk, Pad, Piano (two rows, colours light green and green; the lower one has a device icon and a red "link" mark), Strings, Air Vox, Don Intro,
Don Intro Dub 1-3, HOOK LEAD, Neptune 1 Dub, Hook Lead Dbl, Bridge Lead, Neptune Bridge Lead, Bridge Adlibs, Neptune Bridge Adlibs, LEAD VOCAL,
Lead Add 1, Lead Add 2, Lead Dub, Adlib 1-7. Most of the vocal rows have the red record dot (they are Audio Tracks holding recorded vocal
clips); the rows named "Neptune ..." have a grey rack-device icon and no record dot (**Guess:** Neptune pitch-adjuster tracks; the page says the song uses Neptune; the device itself was not identified on screen). The three coloured rows Drum Loop, Bass, Spunk,
Pad are audio tracks as well (rack labels "AUDIO TRACK").
- Clips (read from position, approximate): Drum Loop runs the whole song with one gap near bar 61; Bass has short hits at bars 17-21 and
  33-37 and about 61-67; Spunk 5-49; Pad 5-25 and 49-85; Piano 17-29, 37-57 and 57-85; Strings and Air Vox 5-57 and 61-69; Don Intro and its three
  Dubs only bars 1-9; HOOK LEAD 9-25 and 49-57 and 77-85; Neptune bridge tracks and Bridge Lead/Adlibs at bars 65-73; LEAD VOCAL 25-49;
  Adlibs only at bars 29-47. **Guess:** intro 1-9 (Don Intro), hook 9-25, verse 25-49, hook 49-57, bridge 65-73, outro to 85.
- No automation lane rows were listed under any track (Seen). Green frames show automation anyway (section 4).

## 3. Rack (Seen, front to back by scrolling, rear view with Tab)
Top to bottom: Hardware Interface; **Master Section**; Scream 4 "SCREAM 2"; Scream 4 "SCREAM 1"; RV7000 "PLATE"; RV7000 "ROOM"; The Echo "ECHO";
DDL-1 "DELAY 3/16"; audio tracks Drum Loop, Bass, Spunk; **Pad** audio track with an insert Combinator "PAD FX"; audio track/NN-XT part for Piano
(a Combinator labelled "PIANO"), Strings (NN-XT), Air Vox (NN-XT); audio tracks Don Intro, Don Intro Dub 1-3, HOOK LEAD, Hook Lead Dbl, Bridge Lead, Bridge
Adlibs, LEAD VOCAL, Lead Add 1, Lead Add 2, Lead Dub, Adlib 1-7; four mixer channels used as output buses: **Lead Vox Bus, Adlib Bus, Hook Bus, P1: Hook Bus**.
Nothing else (no Kong, Redrum, Thor, Malstrom).

## 4. Mixer (Seen)
- **FX sends:** 1 Plate, 2 Room, 3 Echo, 4 Delay 3/16, 5 Scream 1, 6 Scream 2, 7-8 blank. (Two Scream 4s used as SEND effects, not inserts. In Power they were inserts.)
- Send 4 (Delay 3/16) is lit on Don Intro, Don Intro Dub 1-3, HOOK LEAD and most vocal rows (bridge, adlibs, lead rows), and **its Level knob has a green
  frame on Don Intro and the three Dubs and HOOK LEAD** (automated parameter, **Manual [6] ~2954-2965**). Send 5 and 6 (the Screams) are lit only on Lead Vox
  Bus and Hook Bus. Sends 1 and 2 lit on HOOK LEAD, Bridge, Adlibs and some vocals; the drums, bass and pad had no sends lit in what I saw. Not every channel read.
- **Fader automation (green frame on the fader):** Piano, Don Intro, HOOK LEAD. (Seen; the lane shape was not opened.)
- **Output buses:** the pink-style bus channels are named on the mixer strips: "Lead Vox Bus" (dark green) receives Lead Add 1, Lead Add 2, Lead Dub;
  "Adlib Bus" receives Adlib 1-6; "Hook Bus" receives HOOK LEAD, Hook Lead Dbl, Bridge Lead, Bridge Adlibs; "P1: Hook Bus" (rightmost) has a blank output (Seen).
  The bus channels' own outputs read blank (my reading: default to the master). Adlib 7 and LEAD VOCAL: output blank.
  So this song uses the sub-mix bus method (**Manual [17], "Output Busses", line 12600 on**) for the vocal layers, unlike Power and Airplane.
- Master bus meter, "DELAY COMP" off, Control Room out "Master".

## 5. Wiring read by hover (Seen; tooltip "Connected to <device>: <jack>")
### 5a. Master Section and effects
| From | To |
|---|---|
| FX Send 1 L | Plate: Left Input |
| FX Send 2 L | Room: Left Input |
| FX Send 3 L | Echo: Left Input |
| FX Send 4 L | Delay 3/16: Left |
| FX Send 5 L | Scream 1: Left Input |
| FX Send 6 L | Scream 2: Left Input |
| FX Returns 1-6 (Left) | Plate, Room, Echo, Delay 3/16, Scream 1, Scream 2 Left Output (read from the effect side) |
| Master Out L / R | Hardware Interface II: Output 1 / Output 2 |
| Insert FX To Device L | Master Section FX (Combinator): Combi Input Left |
| Insert FX From Device L | Master Section FX (Combinator): Combi Output L |
| Combinator "MASTER SECT..." | Same shape as Airplane and Street Phone: control labels "Loudness Curve", "Compression", "EQ Boost Freq", "Master Gain"; inside Equalizer "M EQ", Stereo Imager "HI BAND" and "LO BAND" (two-band imager), Equalizer "CUT/BOOST", Maximizer "MAXIMIZER". **Different from the other two songs' four devices** (M EQ, Stereo Imager, M Comp, Maximizer) |
So the master Combinator is **a third variant** of the same shell. Only Left jacks read; inner cables not traced.

### 5b. Pad channel insert Combinator "PAD FX"
- Pad channel Insert FX: To Device L is connected to "**Pad: To Insert FX L**" on the Combinator input; From Device L to the Combinator output ("Pad: From Insert FX L").
- Front (Seen): control CV labels **Delay Time, Decay, Gain, Frequency**; buttons: Editor, Devices.
- Inside (Seen labels): Combinator mixer, Stereo Imager "HI BAND", Stereo Imager "LO BAND", Equalizer "CUT/BOOST", Maximizer, **RV7000 "ECHO"** (a reverb used as an echo:
  front knobs Decay, HF Damp, Gate Trig), Audiomatic "AUDIOMATIC 1", and (**Guess**, not seen) something for delay (the Combinator front lists "Delay Time", "Decay", "Gain", "Frequency"; **Guess:** they drive the RV7000 echo and a filter; Modulation Routing not opened). Read: RV7000 Audio Input L <- **Maximizer: Left**; RV7000 Audio Output L -> **Audiomatic 1: Left Input**;
  Audiomatic's Transform CV Trim reads 100% and its CV inputs have no cable.
  So the audio path (left side) is Combinator in, Stereo Imagers and Equalizer, Maximizer, RV7000 echo, Audiomatic, Combinator out. Order of the first three not read.
- Same idea as the Power master Combinator's "Master Section FX" in shape: the author uses the same imager/EQ/maximizer as a channel effect on the pad.

### 5c. Others (Seen labels only)
- Piano: a Combinator labelled "PIANO" (an NN-XT-style or piano patch inside); its mixer channel shows an automated fader.
- Strings and Air Vox: NN-XT samplers cabled by red pairs into their strips (Seen, cables only).
- The audio-track vocals feed their own mixer channels; a long cyan cable runs down the rack to the Bus channels (Seen; not traced with hover).

## 6. Not read
- Neptune devices (which track, what settings): I did not see a device labelled Neptune in the rack while scrolling (I may have missed folded strips); nothing was opened.
- Any automation lane (Piano/Don Intro/Hook Lead faders, Don Intro send 4 level).
- PAD FX Combinator's Modulation Routing, the Piano Combinator's insides, the bus insert devices (if any), every audio track's output.
- Sequencer clips' contents (recorded vocals), pitch data.

## 7. What I did and my slips (mine)
- Opened the demo, hid nothing but the Browser (menu toggle only), used View menu items, Tab, PageUp/PageDown, scroll-bar drags. Never played, never saved.
- **My slip:** I first read the mixer strips at a zoom where I assumed the coloured names were the whole track list; the track list has 30 rows (section 2).
- I unfolded the Master Section device once with a click (it had folded strips); that is a view fold, not a song edit.
- Dictation was on earlier (mouse clicks blocked); here app_* clicks and drags worked, hover worked.

## 8. Where it ended
- Closed with the red button; **no save dialog appeared** (read-only file). SHA-1 after: `290f75ff1e5713ca9e4316b31f907da80ec8d25c` (same as before). Power, Airplane and Street Phone hashes unchanged too.
- Reason has only the scratch song open, unsaved. Zip and unzipped song stay in `~/Downloads/Reason Demo Songs/`.

=== END OF PART ===
