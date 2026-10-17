# Airplane: full wiring map (step 00c follow-up)

Requested by the owner: "Map Airplane's wiring fully" (2026-09-29). Belongs with
[demo-song-notes-airplane.md](demo-song-notes-airplane.md) (sections 3-5 there hold the first, partial reading).
Method: mixer RACK button to jump to each device, rack in REAR view, hover each jack and read "Connected to ...".
**Seen** unless marked **Manual** (Reason 12.7 manual, line numbers in `~/.reason_voice/reason12_manual/Reason_12.7_Operation_Manual_Full_Text.md`)
or **Guess**. I read the left jack of most devices and the right jack where I say so. Where a tooltip was partly covered by
another tooltip I say so. Nothing was changed in the song; I pressed two view toggles (Master Section "Show Insert FX", the
Norwegian Boy Combinator's "Devices" button).

## A. Master chain

| From | To |
|---|---|
| Master Section FX Send 1 / 2 / 3 (Left) | Plate / Room / Echo, Left Input |
| Plate / Room / Echo outputs | Master Section FX Return 1 / 2 / 3 (read from the effect side: "Plate: Left Output", "Room: Left Output", "Echo: Left Output") |
| Master Section Insert FX, To Device L | Master Section FX (Combinator): Combi Input Left |
| Master Section Insert FX, From Device L | Master Section FX (Combinator): Combi Output (tooltip cut at the edge) |
| Master Out L / R | Hardware Interface II: Output 1 / Output 2 |
| Master Section FX Combinator, inside | To Devices Output L, then M EQ (L), Stereo Imager (L), M Comp (L), Maximizer (L), then Combinator Mixer Input Left 1. **The same chain as Street Phone's master Combinator, with the same four Control CV labels (Loudness Curve, Compression, EQ Boost Freq, Master Gain).** Only Left jacks were read |

## B. Instrument and audio wiring, channel by channel

| Channel | Source | Goes to |
|---|---|---|
| Nightclub Saw | Europa, Audio Left | Long Sidechain (Synchronous): Left Input. Synchronous output L: Nightclub Saw Mix Input L. Mix Audio Output reads "Master Section" |
| Punch Drunk Saw | Europa | Punch Drunk Saw Mix: Input L (right jack not read). Output label blank on the mixer |
| Fifth Dimension | Europa | Fifth Dimension Mix: Input L (right not read). Output: **Sidechain Bus** |
| Unisaw | Europa | Unisaw Mix: Input L and Input R. Output: **Sidechain Bus** |
| Kick | Redrum, Stereo Out Left / Right | **Pulveriser 1** Left Input / Right Input. Pulveriser 1 Output L / R go to Kick Mix Input L / R. Redrum Send Out 1: the tooltip read only "Send 1" (no "Connected to"), and a cable seen near it looks like the Stereo Out cable passing by, so I take it as **not connected** (my first note said "has a cable"; that was a misreading of a passing cable) |
| Hi-hat | Dr. Octorex, Main Output L / R | Hi-hat Mix Input L / R |
| Clap and Hats | Redrum "Clap", Stereo Out L / R | Clap and Hats Mix Input L / R (tooltip partly covered by a second tooltip, read as "Clap and Hats: Input L / R"). Redrum Send Out 1: tooltip read only "Send 1", so I take it as not connected (same reading as the Kick) |
| Ending Top | Dr. Octorex "ny_drm124_ruff_top" | Ending Top Mix Input L / R |
| Mushi | Grain | Mushi Mix Input L / R |
| Norwegian Boy -LNB | Combinator, Output | Norwegian Boy -LNB Mix, Input R read here (Input L read on an earlier visit). Output: **Sidechain Bus** |
| Mothership Landing | Grain | Mothership Landing Mix Input L (right not read). Mix Audio Output reads "Master Section" |
| Boomer Bass | Grain | Boomer Bass Mix Input L / R. Output: **Sidechain Bus** |
| Please Release Me | Grain | Please Release Me Mix Input L / R |
| Pulse Scream -LC | Combinator, Output | Pulse Scream -LC Mix Input L / R. The Combinator's own Input jacks show no cable; hover gave only the jack name ("Combi Input Left") |
| Stereo Noise Sweep [Run] x2 | Thor, "1 MONO / LEFT" | Stereo Noise Sweep [Run] Mix Input L (right jack tooltip partly cut off). Same for the second one. Output: **Sidechain Bus** for both |
| Crash | Audio Track device | No instrument cable (it is an audio track). Output: **Sidechain Bus** |
| Sidechain Bus | Mix Channel | Insert To Device L/R go to Sidechain Bus FX (Combinator) Combi Input; From Device L/R come from its Combi Output. Output: "Master Section" |

## C. Inside the Sidechain Bus FX Combinator (Seen)
- Synchronous "Long Sidechain" Audio In L / R: Sidechain Bus FX: **To Devices Output** L and R.
- Synchronous Audio Out L / R: Sidechain Bus FX: **Mixer Input Left 1 / Right 1**.
- Synchronous CV In (curves 1-3, freeze), CV Out and Master Level CV In: no cables.
- So the audio path is: bus input, Combinator input, Synchronous, Combinator mixer, Combinator output. Nothing else is in that chain.

## D. Inside the Norwegian Boy -LNB Combinator (Seen; opened with its Devices button)
- Two **Malstrom** synthesizers named **Kalimba L** and **Kalimba R**. Kalimba L's main outputs go to Line Mixer Channel 1
  Left / Right; Kalimba R's "Shaper / Filter A" and "Filter B" audio outputs go to Line Mixer Channel 2 Left / Right.
- A **Line Mixer 6:2 ("micromix")** has channels 1 and 2 in use. Its Send goes to an **RV7000** Left Input, and its Master
  Out L goes to the **Pulveriser** Left Input.
- Other devices in the Combinator's rack part: Pulveriser, The Echo ("THE ECHO"), Compressor ("MASTER COMP").
  **Not read:** the Pulveriser, Echo and Compressor outputs, the RV7000 return, and how the Compressor reaches the
  Combinator Output. **Guess:** the order is Line Mixer, Pulveriser, Echo, Compressor, out.
- The front knobs "Shift / Dirt / Width / Reverb Level" and the buttons: which inner parameters they drive is set in
  Modulation Routing (Editor button). **Not opened.**

## D2. Inside the Norwegian Boy -LNB Combinator, more (Seen, read later in the same visit)
- Compressor "MASTER COMP": Audio Input L is connected to **The Echo: Left Output**; its Audio Output L / R go to the
  Combinator's **Mixer Input Left 1 / Right 1**.
- Pulveriser: Input L is connected to **Line Mixer: Left**.
- So the order is Line Mixer, Pulveriser, The Echo, Compressor, Combinator mixer. The Echo's input source and the
  Pulveriser's output were not read: **Guess** that the Pulveriser feeds The Echo.

## D3. Inside the Pulse Scream -LC Combinator (Seen; opened with its Devices button)
Devices, top to bottom (front labels): RPG-8 Arpeggiator "VELO", Line Mixer "LEFT COPY", Line Mixer "RIGHT COPY", Spider Audio
Merger & Splitter "SPIDER AUDIO 1", Scream 4 "EASYFUZZ", Line Mixer "FIRST MIX", RV7000 "AMB BLUE RO...", Pulsar "PULSE OSC",
ECF-42 "FILTER__", Pulsar "VIBRATO". No synthesizer is in it: **the sound source is a Pulsar LFO used as an audio oscillator.**
- Pulsar "PULSE OSC" LFO 1, Audio Output 1 -> **ECF-42 "Filter__": Left** input. (Read from both ends: the ECF-42 input L tooltip
  says "Pulse Osc: LFO1 AudioOut1".)
- Pulsar "VIBRATO" LFO 1 CV Out 1 -> **Pulse Osc: LFO 1 Rate** (a CV cable). So one Pulsar wobbles the pitch of the other.
- ECF-42 Left Out -> **First Mix (Line Mixer): Channel 1 Left**.
- **Not read:** Right jacks, the Freq CV / Decay CV / Res CV and Env. Gate jacks of the ECF-42 (the CV knobs show no cable
  on the front), the "LEFT COPY / RIGHT COPY" mixers, Spider Audio, Scream 4, RV7000, and how the chain ends at the
  Combinator Output. Which Combinator knobs (Blend, Filter, Attack, Reverb) reach which of these is set in Modulation
  Routing (**not opened**).
- **Also Seen:** the "VELO" RPG-8 Arpeggiator has its own gate/CV cables (lime lines) into the Combinator; not traced.

## E. Not mapped
- Pulse Scream -LC Combinator inner cables. Its jack menu lists Spider Audio, EasyFuzz (Scream 4), First Mix (Line Mixer
  6:2), AMB Blue Room (RV7000), Pulse Osc (Pulsar), Filter__ (ECF-42), Vibrato (Pulsar); list read only to the first rows.
  Whether a Pulsar feeds the ECF-42 by CV is not read.
- Redrum Send Out 1 on the Kick and Clap: read as unconnected (see B). Not double-checked with the jack menu.
- Dual Arpeggio (a Player) and how it reaches the Combinator.
- Sequencer Control jacks (Gate / CV / Pitch Bend / Mod Wheel) on every device: the ones I saw had no cables; not all
  were looked at.
- Right jacks of Nightclub Saw, Punch Drunk Saw, Fifth Dimension, Mothership Landing and the first Thor.

## F. What the map says (my reading of the parts I read)
- Channels reach the Master Section by P-LAN (no cable), either directly or through the Sidechain Bus. The only audio
  cables in the rack are instrument to mixer (red), effect and Combinator hookups (green, blue) and the master hookup.
  **Manual [17], "Output Busses" (line 12600 on).**
- Every instrument feeds its own Mix Channel Input L/R with a red pair, except where an effect sits between (Kick:
  Pulveriser 1; Nightclub Saw: its Synchronous; Norwegian Boy and Pulse Scream: a Combinator).
- **Correction to my own earlier wording:** I first wrote that no CV cable appeared anywhere. That was wrong: inside the
  Pulse Scream -LC Combinator a Pulsar's CV output is cabled to another Pulsar's Rate input (D3), and the RPG-8 there has
  gate/CV cables. In the parts outside that Combinator I saw no CV cable: the Control CV inputs on the Norwegian Boy and
  Pulse Scream Combinators, the Synchronous CV inputs and the Sequencer Control jacks I looked at were empty. So the
  movement in this song comes from a mix of sequencer automation lanes, the Synchronous curves, CV cables inside the Pulse
  Scream Combinator and Combinator internal routing (not opened). Not every CV jack was checked.

## G. State at the time of writing
- SHA-1 of the demo file before this visit: `91a2df7aedba4313b274f45511b2046c72575649` (checked again after closing; see the
  Airplane notes "Where it ended").
- Street Phone's wiring (second part of the owner's answer "Map Street Phone too") was read only for the sends, returns
  and master chain; its channel cabling is not mapped yet.
