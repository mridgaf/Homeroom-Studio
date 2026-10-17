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
