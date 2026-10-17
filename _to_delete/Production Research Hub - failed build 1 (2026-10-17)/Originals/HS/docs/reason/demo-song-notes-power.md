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
