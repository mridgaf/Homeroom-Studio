# Chapter 09: Reason 12 manual digest and studio workflow
## Part 24 of 25

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- demo-song-wiring-airplane.md — Airplane: full wiring map (step 00c follow-up)
- guide-new-ideas-2026-09-30.md — What is NEW in Reason12_HomeroomStudio_Guide.md (checked 2026-09-30)
- manual-bigger-wins-2026-09-30.md — Bigger wins found in the Reason 12.7 manual (2026-09-30)
- rack-back-reading-howto.md — How to read a Reason song's rack back (method notes)
- reason12-project-notes.md — Reason 12 Project (claude.ai) — copied notes
- skill-edits-draft-2026-09-30.md — Draft wording: what I would put into the skills (nothing is applied yet)

(Next: Part 25 of 25)


=====================================================
SOURCE FILE: demo-song-wiring-airplane.md
ORIGINAL LOCATION: HS:docs/reason/demo-song-wiring-airplane.md
=====================================================

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

=====================================================
SOURCE FILE: guide-new-ideas-2026-09-30.md
ORIGINAL LOCATION: HS:docs/reason/guide-new-ideas-2026-09-30.md
=====================================================

# What is NEW in Reason12_HomeroomStudio_Guide.md (checked 2026-09-30)

Source: [Reason12_HomeroomStudio_Guide.md](Reason12_HomeroomStudio_Guide.md). I compared all 29 tips with the skills,
`docs/reason/` notes, `device_refs/` and the Reason 12.7 manual. Nothing below is built or added to a skill yet.
Tags: **Manual** = confirmed in the Reason 12.7 manual. **Unverified** = only the guide says so.

## A. New, and confirmed in the manual (worth adding)

| Idea | The real steps (from the manual, not the guide) | Where it could go | Status |
|---|---|---|---|
| **Make every new song start from your own setup** | Reason menu > Preferences > General tab > "Default Song" > click **Template** > folder icon > pick your song. Untick "Load last song on start-up" or it won't work. Also: File > New from Template > pick one; File > New from Template > Show Template Folder opens the folder where your own songs can be dropped to appear in that menu | New small skill `reason-default-song`, or a section in the template ideas list | Manual |
| **Map any one knob to any one parameter, in one song** | Right-click (Ctrl-click on Mac) the parameter > "Edit Remote Override Mapping" > turn on "Learn From Control Surface Input" > move the knob. Or double-click the parameter, then move the knob. A lightning bolt shows it is mapped. Esc leaves learn mode. "Clear Remote Override Mapping" removes it | New section in `reason-remote-bridge` (it does not mention overrides): a hand-made map for one-off jobs, next to our own `.remotemap` | Manual. I did not check whether it saves with the song |
| **Color tracks** | Edit > Track Color (or the track's right-click menu). It also colors the Audio Track/Mix Channel device and the mixer strip. New clips on that track take the color. The manual also lists an "Auto-color Tracks and Channels" option | One line in `fresh-blank-song` or the template list | Manual |

## B. Not added: you already have it

| Guide tip | Already covered in |
|---|---|
| 9, 12, 29 Combinators, name everything | `demo-song-template-and-automation-ideas.md` (macro-knob box, name-everything rule); skill idea `reason-combinator-macros` |
| 4, 5 Drum and bass chains, sidechain | same file (kick squash chain, pump bus, silent kick trigger, per-channel chain); `drum-loops` skill |
| 13 Edit automation | skill idea `reason-automation-lanes`; hold-a-value clip idea |
| 15 Surface locking | `reason-remote-bridge` rule 4 and `FINDINGS.md` |
| 2, 19 Keyboard control, MIDI keyboard | `FINDINGS.md` (Keyboard Control, Launchkey MK3 factory map) |
| 18 Control surfaces | `FINDINGS.md`, `device_refs/launchkey-mk3.md` |
| 21 CV routing | `demo-song-notes*.md`, skill idea `reason-signal-flow` |
| 22 Parallel processing / sends | "Send-effects trio" and "Pump bus" ideas |
| 23 Master chain | "Master chain" and "Same master Combinator" ideas |
| 16 Naming templates | `Song Starter - Trap` style already in use |
| 8, 10, 11, 27, 28 | Too general to be a skill (color is in table A) |

## C. Conflicts: the guide is wrong or disagrees with you. Do NOT add these

- Guide step 1 says **File > Song Information > Save as Default Song**. That menu item does not exist. Song Information only holds notes. Use the Preferences steps in table A.
- Guide tip 17 puts Mac templates in `Library/Application Support/Propellerhead Software/...`. The manual says the **Template Songs folder in the Music folder** (File > New from Template > Show Template Folder). Your notes already say `~/Music/Reason 12/Template Songs/`.
- Guide tip 15 says **Remote > Settings > Lock Surface**. Not in the manual. Your 2026-09-29 rule: do NOT use Options > Surface Locking; use the device's right-click "Lock ... to This Device".
- Guide tip 2 says map keys to pitch bend, mod wheel and LFO. `FINDINGS.md` says Keyboard Control only toggles switches (min/max), not knobs. Keep the `FINDINGS.md` version.

## D. Not verified, so not added

- **Gamepad control** (tips 3 and 20): needs a third-party app called "Universal Controller MIDI" and a PS5 or Xbox pad. The manual says nothing about it, and I don't know if you own a pad. Idea only, until you say you want it.
- **Live performance rack** (tip 7): you are a studio producer; skip unless you start gigging.

=====================================================
SOURCE FILE: manual-bigger-wins-2026-09-30.md
ORIGINAL LOCATION: HS:docs/reason/manual-bigger-wins-2026-09-30.md
=====================================================

# Bigger wins found in the Reason 12.7 manual (2026-09-30)

How I looked: listed all 70 manual chapters, searched your skills, notes, recipes and device guides for each topic, and read
the chapters where you had nothing. Tag **Manual** = read in the Reason 12.7 manual. None of this has been tried in Reason
or heard. Nothing is built. Not looked at yet: Key Commands (ch 70), Delay Compensation (18), Sampling (21), Audio Editing (8).

Full digests now live in [manual-digest/](manual-digest/README.md). The ReGroove skill is drafted at `.claude/skills/reason-regroove/SKILL.md`.

## 1. Players: chords and arpeggios from single notes (ch 12)  -- NOTHING in your notes
You have 0 files on Scales & Chords or Note Echo. Dual Arpeggio only appears inside song notes, never as a how-to.

| Piece | What it does | Tag |
|---|---|---|
| **Scales & Chords** | Pick a Key (12) and Scale (13 presets + a custom one you click in). Turn on **Chords**: one played note makes a chord that fits the scale. Notes knob = 1 to 5 notes. Wrong notes snap to the nearest right note (or go silent with Filter Notes on). Key and scale can be automated, so a song can change key | Manual |
| Chord extras | Inversion knob, Open Chords (spreads the notes), Add Oct Up / Oct Down / Color (adds the 9th, 11th or 13th), Alter (momentary: turns a major chord minor and the reverse) | Manual |
| **Note Echo** | A MIDI delay. Parallel chords (a shape that stays the same on every note, like a minor 9th): Step Length 0, Repeats max, Pitch +1, then click off the repeats you don't want | Manual |
| **Chain order matters** | Scales & Chords above Dual Arpeggio = scale-correct arpeggio from a single note. Dual Arpeggio above Scales & Chords = arpeggiated chords. Top device runs first | Manual |
| **Direct Record** | Records the notes the Player makes, not the notes you played. **Send to Track** renders them into a new clip, so you can edit them | Manual |
| Monitor trick | Scales & Chords last in the chain, Scale = Chromatic, Chords and Filter Notes off: shows what the chain is playing | Manual |

Skill idea: **reason-players** (small). Not checked: whether you own Beat Map (a Rack Extension Player in the same chapter).

## 2. ReGroove: how to actually use it (ch 22)  -- your recipes say "use ReGroove" but never say how
Recipes `doechii-denial-is-a-river`, `jid-never-story-music-box` and `feels-warm-soulful` all rely on it. No file has the steps.

- Open it with the **Groove button** on the Transport Panel (32 channels, 4 banks A-D of 8). Manual
- Send a note lane to a channel with the **Select Groove pop-up** on the lane. Only note lanes work, not audio. Manual
- Each channel has **Shuffle**, **Slide** (push a lane ahead of or behind the beat), **Groove Amount** and a groove patch. Manual
- **Global Shuffle: 50% = straight, 66% = triplet swing.** It also swings Redrum, Matrix, RPG-8 and Dual Arpeggio. Manual
- Compare with and without: turn the channel's On button off. Manual
- **Anchor Point** starts the groove at a later bar (for a pickup or intro). A time-signature change restarts the groove. Manual

Skill idea: **reason-regroove** (small). It would make the three recipes above walkable by voice.

## 3. Blocks: build sections once, reuse them (ch 10)  -- 0 files
- 32 Blocks, each usually 4-8 bars (a verse, a chorus). Reuse them anywhere in the song. Manual
- Block View and Song View share the same tracks but keep separate clips. Manual
- Block Automation Clips place a Block in the song and can mute lanes for that one use, which gives variations. Manual
- New songs have Blocks on. A song saved without them needs Options > **Enable Blocks**. Manual
- Linear clips can sit on top of Block data to override a bar here and there. Manual

Skill idea: **reason-blocks** (small). Fits the "64-bar song map" idea in `demo-song-template-and-automation-ideas.md`.

## Not worth adding
Osmium shows up in the device list file but has no chapter in this manual, so nothing to write from.

=====================================================
SOURCE FILE: rack-back-reading-howto.md
ORIGINAL LOCATION: HS:docs/reason/rack-back-reading-howto.md
=====================================================

# How to read a Reason song's rack back (method notes)

Written 2026-09-29 from four demo songs (Street Phone, Airplane, Power, Qua z mo). Tags: **Seen** = on screen · **Manual** = manual place named · **Guess** = not confirmed. Nothing here was heard. This is the method behind the `reason-signal-flow` skill idea in [demo-song-skill-ideas.md](demo-song-skill-ideas.md).

## 1. Open and close safely (Seen)
- Demo files show "[Read-only]" in the title bar. Never save. Close with the window's red button and read the dialog before answering; for a demo that has only been looked at, no dialog appeared (five-plus times).
- Check the file's SHA-1 before opening and after closing. All four demos came back identical.
- Unfolding a device or scrolling is a view change, not a song edit.

## 2. Moving around (Seen)
| To do this | Do this |
|---|---|
| Switch view | Window > View Main Mixer / View Racks / View Sequencer |
| Flip rack front/back | Tab (or Options > Toggle Rack Front/Rear) |
| Scroll the rack | PageUp / PageDown (key name `pagedown`); arrow keys move between rack columns |
| Scroll the mixer sideways | Drag its bottom scrollbar (a mouse wheel over knobs can turn them; my slip) |
| See the whole song | Sequencer ZOOM button |

## 3. Read a cable by hover (Seen)
- Hover a jack for 2-3 seconds. Tooltip: "Connected to <device>: <jack>". An unconnected jack shows only its own name.
- Hover jacks, not cable bodies (two tries on bodies showed nothing).
- Take hover coordinates from a display screenshot; app-window screenshots use a different scale (1382x868 vs 1372x891) and the tooltip will not appear.
- Ctrl-click a jack lists every rack device, check on the connected one, asterisk on occupied jacks (Airplane). Needs real clicks.

## 4. The unfold trap (Seen)
- Batching several fold-triangle clicks fails: Reason auto-scrolls when an unfolded device ends below the window, so later clicks land on the wrong thing (my method error).
- Do one unfold click, then one screenshot, every time.
- Option-click on a fold triangle should unfold the whole column (**Manual [11] line 9103**); not tested.

## 5. Layout convention (Seen in Power and Street Phone; Guess that it always holds)
- A mixer strip sits directly above its instrument. Insert devices sit below it, labelled with the channel name. The last insert's output goes up to the strip ("From Insert FX").
- Channel to master has no cable (P-LAN, **Manual [16]**). Send effects go through the Master Section's FX Send/Return 1-8.
- So you can trace a channel by reading the labels top to bottom before hovering anything.

## 6. Cable colours (Manual [16])
Green = effects · red = instrument to mixer · yellow = CV · blue = Combinator.

## 7. What could not be done
- Mouse clicks were blocked while macOS Dictation was on (keys, hover and the app-window tools still worked).
- Inner cables of Combinators were read only where hovered; most were not traced.
- Whether a device does what its name says was never heard.

=====================================================
SOURCE FILE: reason12-project-notes.md
ORIGINAL LOCATION: HS:docs/reason/reason12-project-notes.md
=====================================================

# Reason 12 Project (claude.ai) — copied notes
Copied 2026-10-11 from the claude.ai "Reason 12" project (started 2026-05). The project has no uploaded files; this is its instruction text (condensed) plus saved gear facts. Homeroom Studio is the main home; this is the record of the original.

## Original hard rules (condensed)
1. Quick recipe format: device chain, exact settings, one-line "why", accuracy rating. One screen each.
2. Stock Reason 12 first. Then flag any Rack Extension that closes a gap (name, maker, approx price). Never assume he owns REs.
3. State the assumed source quality; give a fallback if the recipe fails with a worse source.
4. Plain language, NO analogies.
5. Accuracy rating A (90%+), B (70-89), C (50-69), D (<50, name the REs).
6. Every recipe names the transferable technique at the bottom.
7. Justify order of operations in one line.
8. Use Reason's strengths: Combinator 2, SSL channel strip, CV sidechain, Players.
9. Tag each recipe Tested or Theoretical.
10. Push back if a sound is impossible in stock Reason.
Planned book layout: index by artist, drums, bass (incl. kick-bass and 808), anti-recipes, "Your Sound" (his own Combinator patches).

## Gear (stated)
- PreSonus AudioBox USB 96; Cordoba Mini II Bass acoustic-electric (piezo); PROformance passive DI.
- Working chain: guitar -> DI INPUT -> XLR from LOW Z OUT -> Mic Input 1, DI switch on INST. Gain target about -12 to -6 dB in Reason.
- Not owned (candidates): Fishman Pro-EQ Platinum, LR Baggs Para Acoustic DI, Kilohearts Multipass, FabFilter Pro-MB.

## Chats holding the built recipes (not copied yet)
"Hip-hop recipe book development priorities", "Project setup and calibration", "Low volume and distortion with acoustic bass recording", "Reason 12 operation manual".

## UPDATE 2026-10-11 — recipes now copied
Saved in docs/reason/old-project-recipes/ (all marked THEORETICAL per Homeroom's rule; each has a "check before trusting" note where names/prices were unverified):
- 03 On to the Next One drums, 04 lead hook, 05 vocal chain
- 06 kick + 808 relationship (this one is also "06" in the other numbering; the Tony Tone drums file is the other "06")
- 06 Tony Tone drums (A$AP Rocky)
- hiphop-recipe-book-v1-2026-05.md (7 starter recipes + 5 anti-recipes + Your Sound template)
Not found anywhere I could reach: the "Reason 12 Patchbook" and the "built-patches" folder. They are not in the project's chats or files.
Overlap: v1 book's "CV Sidechain Duck" is a short version of the kick/808 recipe (prefer the long one). Homeroom's recipes/hiphop/trap-808.md covers similar ground; compare before merging.

=====================================================
SOURCE FILE: skill-edits-draft-2026-09-30.md
ORIGINAL LOCATION: HS:docs/reason/skill-edits-draft-2026-09-30.md
=====================================================

# Draft wording: what I would put into the skills (nothing is applied yet)

Target file: `.claude/skills/reason-remote-bridge/SKILL.md` unless said otherwise.
Say "apply" and I put each block in; say what to change and I change it first.

---

## A. Replace rule 6 (it is wrong: it puts the arm button on each lane and says I never saw it)

> 6. **Arming a lane: the owner's steps (2026-09-30, then Seen).** Use these every time,
>    for any device or effect that can have a track:
>    1. Right-click the device > **Create Track for X**. Once a track exists the same
>       menu shows **Go to Track for X**; if that item is live, the track exists.
>    2. On that track's row, the button **just right of the S (solo) button** is the
>       record-arm. **Red = armed.** Read its colour before and after any click on it:
>       on 2026-09-30 I clicked a red one and disarmed it.
>    3. Start recording and move a knob. A lane **named after that knob** appears on
>       the track. Nothing appears until a knob moves during a recording.
>    If a lane does not record, look at the track row first (is it red?), then check
>    the lane exists, then check you are looking at the bars the sweep landed on (rule 11).
>    Seen 2026-09-30: with the track armed, a Filter Frequency lane on The Echo
>    recorded both a typed and a spoken sweep. The earlier belief that each lane has
>    its own button is dropped.

## B. Add to rule 8 (the microphone)

> **Microphone path proven 2026-09-30 (Softube Amp, The Echo).** He held the page's
> talk button: "make it twang." and "sweep the filter frequency down over 4 bars at
> 115" were heard word for word and ran. **He must hold the button the whole time he
> speaks;** a short tap loses the phrase and the app shows nothing new (no error).
> To see why a phrase is missing, run a watcher on the page's websocket
> (`ws://localhost:8765/ws`) and print status changes: recording > thinking > idle.
> A test that cannot move anything proves nothing: "gain up a bit" on a knob already
> at maximum was heard right but changed nothing. Pick a phrase that visibly moves.

## C. New rule 10: adding a device to the scratch song

> 10. **Add a device from Reason's own browser (Seen 2026-09-30).** Click the
>     browser's Effects (or Instruments) category, click the search box (click first;
>     typing before the box has focus goes nowhere), type part of the name, press
>     Return, then **double-click** the result. The Softube Amp ("Amp") was added this
>     way and then swept (Twang 0-25, Crunch 26-50, Rock 51-76, Lead 77-101,
>     Bypass 102-127). This replaces the 09-29 note that Create-menu presses added
>     nothing visible. A new device lands after the selected one; scroll the rack to it.

## D. New rule 11: where did the sweep land

> 11. **Before judging a sweep, know which bars it is on.** A move lands at the
>     playhead and Reason's sequencer view may be scrolled elsewhere (it sat at bar
>     98 while the song was at bar 1). Click the ruler to put the playhead on **empty
>     bars** (4 bars ahead of any other clip), note the bar number, and look at those
>     bars. Optional, the owner's idea: a short loop (about 5 bars) with Loop on and the
>     view zoomed to it, so the whole piece is always on screen. At the end of the
>     loop the playhead jumps back and the lane plays again from its start; that is
>     looping, not a failure. Not tried: recording while Loop is on may add a new
>     take each pass.

## E. New rule 12: the screen overlay

> 12. **Screen control puts an overlay over his whole screen.** While it is on he
>     cannot see or use the app page, so he cannot speak to it. Release it
>     (`release_full_control`) whenever he must look or talk, and ask again when I
>     need clicks. Overrides the earlier "never release" note.

## F. `OPEN-ISSUES.md` item 44 (add one line)

> 2026-09-30: adding a device from Reason's browser (search, double-click) worked
> under full-screen control; Create-menu presses were never the way. Cabling still
> not tried.

## G. `reason_voice` note, beside the Neptune fix (DECISIONS only, no skill)

> The model copies example wording from a device guide line: "~12 o'clock" came back
> as its answer. Write guide lines as plain direction ("turn UP for faster").

---

Not changed on purpose: no benchmark loop (these are corrections, not a new skill),
no change to `CLAUDE.md`.

=== END OF PART ===
