# Chapter 08: Reason panel map
## Part 1 of 22

_Front and back panel maps of Reason devices: every knob, button and jack, by device._

**In this part:**
- INVENTORY.md — Panel Map inventory (Phase 2, 2026-10-03)
- PLAN.md — Panel Map — full build plan
- 00-INDEX.md — Panel Map index (read this first, then ONLY the chapter you need)
- a-b-12-audio-out-switch-pongasoft.md — a-b-12-audio-out-switch-pongasoft
- a-b-audio-cv-switch-pongasoft.md — a-b-audio-cv-switch-pongasoft

(Next: Part 2 of 22)


=====================================================
SOURCE FILE: INVENTORY.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/INVENTORY.md
=====================================================

# Panel Map inventory (Phase 2, 2026-10-03)

Source of truth for what is INSTALLED: Reason 12.7's own Create menus, read 2026-10-03 (installed.csv).
inventory.csv = every device Reason has a Remote map for (148), most of which he does NOT own. Use it only to look up names.

## What he has
| Kind | Count | Notes |
|---|---|---|
| Reason-made (stock) | 63 | 19 instruments, 29 effects, 10 utilities, 5 players |
| Rack Extensions from other makers | 15 | 8 utilities, 7 effects (AirRaid, Groovy Melon, pongasoft, Red Rock Sound, Rob Papen, Robotic Bean, kiloHearts, Kuassa, Softube, ThatMusicCompany) |
| VST plugins | 15 | 5 instruments, 10 effects. Their controls live in a separate plugin window, not on a rack panel. Not part of the rack map unless John says so. |
| Always in every song | — | Hardware Interface, Master Section, Main Mixer. Not in the Create menus; map them too. |

## Name joins (menu name -> Reason's Remote name)
- Exact or near-exact for most. Hand joins (wording differs): RV7000 MkII Reverb -> RV7000 Advanced Reverb, Dr. Octo Rex -> Dr.REX Loop Player, Channel Dynamics/EQ -> ChannelDynamics/ChannelEQ, Master Bus Compressor -> MasterCompressor, Alligator Filter Gate -> Alligator, Pulveriser Demolition -> Pulveriser.
- PROBABLE, confirm in Reason while mapping: Scales & Chords -> ScalesAndChords, Dual Arpeggio -> Arpeggio, Softube Amp -> ReasonAmp, Softube Bass Amp -> ReasonBassAmp, Mix Channel -> Reason Main Mixer Channel.
- No Remote map found: Audio Track, Drum Sequencer, all 15 third-party Rack Extensions (no Remote map for them in Reason's files, so tooltips are the only name source).

## Settled from the manual
- Ch.62 Half-Rack Effects covers all 9: CF-101, COMP-01, D-11, DDL-1, ECF-42, PEQ-2, PH-90, RV-7, UN-16 (each named as a heading in the chapter text).
- Ch.55 covers Softube Amp + Softube Bass Amp (chapter text).
- device_refs/guitar-amps.md is about his physical amps (hardware), like audiobox-96, launchkey-mk3, samson-servo-300, yamaha-*.

## Proposed batch order (counts)
- A. Simple fixed effects (18): Half-rack 9, MClass 4, The Echo, RV7000, Channel EQ, Channel Dynamics, Master Bus Compressor.
- B. Other stock effects (10): Alligator, Audiomatic, BV512, Neptune, Pulveriser, Quartet, Softube Amp, Softube Bass Amp, Sweeper, Synchronous.
- C. Mixing & utilities (13): Mix Channel, Audio Track, Mixer 14:2, Line Mixer 6:2, Spider Audio, Spider CV, Matrix, Pulsar, RPG-8, Combinator (outer panel), Hardware Interface, Master Section, Main Mixer.
- D. Instruments (19) — several with views (Kong pads, Thor, Europa, Mimic, Grain, Redrum).
- E. Players (5).
- F. Third-party Rack Extensions (15).

=====================================================
SOURCE FILE: PLAN.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/PLAN.md
=====================================================

# Panel Map — full build plan

Goal: every Reason device John uses gets a coded front + back map (pictures, codes, exact Reason names, MIDI slots, cable-menu jack names, positions), so Claude and Hermes can find, turn, click and cable anything. For Claude and Hermes only; John never has to read it.

Proven so far (2026-10-02): Scream 4 mapped (37 controls). One cable made by map position alone and confirmed by Reason's check marks.

## House rules for every phase
- Work only in a NEW blank test song. Never touch his real songs. Never save over anything.
- Every fact comes from a source: Reason's own menus, remote-vocab.json, the remotemap, or the manual. Never from memory.
- A device is "done" only when its click-test passes (step 4.6 below).
- Log each finished device in PANEL-MAP.md and DECISIONS.md.

## Phase 0 — Finish the standard (Scream 4)
1. Click-test all 37 positions (jacks by right-click; knobs/buttons: find a method that proves the spot without leaving any change behind).
2. Read Auto CV Output's exact menu name.
3. Check the patch arrow direction.
4. Check the table against the Reason 12 manual (needs ~/.hermes opened to this session).
5. Write a "panel-map" skill: the exact same steps for every device, so any session does it the same way.

## Phase 1 — Build helpers (so most of the work is done by scripts, not eyes)
1. Position helper: map position -> screen point, using the panel's corner screws. (Done by hand once; make it a script.)
2. Jack harvester: right-click each jack, read the menu text through the Mac accessibility system. That gives Reason's exact jack names with no picture-reading.
3. Name checker: every Remote item in remote-vocab.json for that device has a code, and no name is misspelled.
4. Idea to test (not promised): find jacks automatically by matching their look (every jack looks the same), so only knobs/buttons need placing by eye.

## Phase 2 — Inventory
1. List every device he has: stock (about 55 guides in device_refs) plus Rack Extensions (Create menus show about 14 other makers in Effects alone; Instruments, Utilities and Players not counted yet).
2. Mark which panels change (Kong modules, Combinator, Thor, Europa, Mimic and others) — those need one picture per view.
3. Order by how often he uses them (from his songs) and how hard they are.

## Phase 3 — Batches (same steps every device)
- Batch A: simple fixed effects (Echo, RV7000, DDL-1, CF-101, PH-90, MClass set, etc.)
- Batch B: mixer, Mix Channel, Combinator outer panel, utilities (Spider, Matrix, RPG-8)
- Batch C: instruments with one view (SubTractor, Malström, NN-19, ID8, Dr. Octo Rex...)
- Batch D: devices with changing panels (Kong, Thor, Europa, Mimic, Combinator custom panels, Redrum)
- Batch E: Rack Extensions, in his order of use

## Phase 4 — Per-device steps (every device, every time)
1. New blank song, add the device.
2. Front + back pictures at the same zoom.
3. Place codes + boxes. Save labeled pictures.
4. Fill names: Remote names from files, jack names from the harvester.
5. Run the name checker.
6. Click-test: every jack by right-click. Knobs/buttons: method decided in Phase 0 (hover tooltip, if Reason shows one — not verified yet; or a nudge read back through the Remote bridge, then put back).
7. Save + log.

## Phase 5 — Hermes
1. Copy the maps into Hermes's notes.
2. Re-run the Round 1 picture questions with and without the map; compare scores.
3. Cable test for Hermes (needs its computer control turned on and John's yes).

## Phase 6 — Upkeep
- Re-check a device's map when Reason updates or he buys a new Rack Extension.

## Where John is needed
- Mac permission prompts (screen control, folder access).
- A yes before Hermes gets computer control.
- Nothing else.

=====================================================
SOURCE FILE: 00-INDEX.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/chapters/00-INDEX.md
=====================================================

# Panel Map index (read this first, then ONLY the chapter you need)

Chapters live beside this file: one `<device>.md` each (front + back tables). Rules and method are below.

Reference for Claude and Hermes. John doesn't need to read this. Plan: PLAN.md. Method: the `panel-map` skill.

## Code format
`DEVICE-SIDE-TYPE##`, for example `SCR4-F-K03`.
- SIDE: F = front, B = back
- TYPE: K = knob, B = button/switch, S = slider, J = jack, D = display
- The code is only a nickname. To control something, use the **Reason name** column. Reason only accepts its own exact names, and a wrong name fails without any warning.
- MIDI: knob slot k is sent on CC 29+k, and its value comes back on CC 77+k (reason_voice/reason_control.py).
- pos = the control's centre as a fraction (0–1) of the labeled picture. To get a screen point, match the panel's corner screws on screen and in the picture (`tools/to_screen.py`). This works at any zoom.

## What Reason tells you (tested in Reason 12.7, 2026-10-02/03)
- **Hover = proof.** Hovering a control shows a tooltip with its exact name, and its value if it has one ("Damage Control: 70"). Nothing changes. This is how every position gets checked.
- Hovering a slider: the tooltip only shows on the **handle**, which moves with the value.
- Hovering an empty jack shows its name ("Right Output"). Hovering a cabled jack shows where the cable goes ("Connected to Room: Decay CV In").
- The hover name can differ from the Remote name (The Echo: hover "Diffusion Spread", Remote "Diffuse Spread"). Keep both; control with the Remote name.
- A back trim knob shows its input's name plus a value ("Damage Control CV Input: 127").
- Displays (meters, light lists) and the fold triangle show no tooltip.
- **Folded devices** become a thin strip, and the controls move. Unfold first (click the triangle).

## How to make a cable (proven 2026-10-02)
1. Right-click the source jack (its position comes from this map).
2. A menu lists every device in the song by its rack name, e.g. "EasyFuzz (Scream 4)". Each one opens a submenu with only the jacks that fit.
3. Click the target jack name. The menus are real Mac menus, readable as text.
4. Prove it: right-click the jack again. The target device and jack now have a ✓, "Scroll to Connected Device" appears, and "Disconnect" turns on. Or hover the jack: "Connected to <device>: <jack>".
- `*` after a jack name = that jack already has a cable. Grey = can't take this cable. Audio outputs also offer "Route to New Mix Channel".
- Undo a cable: right-click the jack, then **Disconnect**.

## Devices
| Device | Code | Front | Back | Data | Status | Chapter |
|---|---|---|---|---|---|---|
| Scream 4 Distortion | SCR4 | scream-4_front_labeled.png | scream-4_back_labeled.png | scream-4.json | **done** — all 38 checked in Reason, manual ch.51 checked | [scream-4.md](scream-4.md) |
| The Echo | ECHO | the-echo_front_labeled.png | the-echo_back_labeled.png | the-echo.json | **done** — 48/48 checked in Reason; manual ch.50 spot-checked; drafted by helper | [the-echo.md](the-echo.md) |
| CF-101 Chorus/Flanger | CF101 | cf-101_front_labeled.png | cf-101_back_labeled.png | cf-101.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [cf-101-chorus-flanger.md](cf-101-chorus-flanger.md) |
| COMP-01 Compressor | COMP01 | comp-01_front_labeled.png | comp-01_back_labeled.png | comp-01.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [comp-01-compressor.md](comp-01-compressor.md) |
| D-11 Foldback Distortion | D11 | d-11_front_labeled.png | d-11_back_labeled.png | d-11.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [d-11-foldback-distortion.md](d-11-foldback-distortion.md) |
| DDL-1 Digital Delay Line | DDL1 | ddl-1_front_labeled.png | ddl-1_back_labeled.png | ddl-1.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [ddl-1-digital-delay-line.md](ddl-1-digital-delay-line.md) |
| ECF-42 Envelope Controlled Filter | ECF42 | ecf-42_front_labeled.png | ecf-42_back_labeled.png | ecf-42.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual; ONE ASSUMING: GATE light (ECF42-F-D02) = Remote 'Trigger' (no tooltip, unproven) | [ecf-42-envelope-controlled-filter.md](ecf-42-envelope-controlled-filter.md) |
| PEQ-2 Two Band Parametric EQ | PEQ2 | peq-2_front_labeled.png | peq-2_back_labeled.png | peq-2.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [peq-2-two-band-parametric-eq.md](peq-2-two-band-parametric-eq.md) |
| PH-90 Phaser | PH90 | ph-90_front_labeled.png | ph-90_back_labeled.png | ph-90.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [ph-90-phaser.md](ph-90-phaser.md) |
| RV-7 Digital Reverb | RV7 | rv-7_front_labeled.png | rv-7_back_labeled.png | rv-7.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [rv-7-digital-reverb.md](rv-7-digital-reverb.md) |
| UN-16 Unison | UN16 | un-16_front_labeled.png | un-16_back_labeled.png | un-16.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [un-16-unison.md](un-16-unison.md) |
| MClass Compressor | MCMP | mclass-compressor_front_labeled.png | mclass-compressor_back_labeled.png | mclass-compressor.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual (picture tape reads M COMP 2; this song's instance reads M COMP 1) | [mclass-compressor.md](mclass-compressor.md) |
| MClass Equalizer | MEQ | mclass-equalizer_front_labeled.png | mclass-equalizer_back_labeled.png | mclass-equalizer.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [mclass-equalizer.md](mclass-equalizer.md) |
| MClass Maximizer | MMAX | mclass-maximizer_front_labeled.png | mclass-maximizer_back_labeled.png | mclass-maximizer.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [mclass-maximizer.md](mclass-maximizer.md) |
| MClass Stereo Imager | MSIM | mclass-stereo-imager_front_labeled.png | mclass-stereo-imager_back_labeled.png | mclass-stereo-imager.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual | [mclass-stereo-imager.md](mclass-stereo-imager.md) |
| RV7000 Mk II Advanced Reverb | RV7K | rv7000_front_labeled.png | rv7000_back_labeled.png | rv7000.json | done 2026-10-07: everything hover-checked; soft knobs (RV7K-F-K05..K12) numbered by position per owner, their names change by page; programmer EQ and Gate edit-mode views not captured; name_check PASS | [rv7000-mk-ii-advanced-reverb.md](rv7000-mk-ii-advanced-reverb.md) |
| Matrix Pattern Sequencer | MTRX | matrix_front_labeled.png | matrix_back_labeled.png | matrix.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Matrix (not added; out of scope) | [matrix-pattern-sequencer.md](matrix-pattern-sequencer.md) |
| Spider Audio Merger & Splitter | SPDA | spider-audio_front_labeled.png | spider-audio_back_labeled.png | spider-audio.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Spider Audio (not added; out of scope) | [spider-audio-merger-splitter.md](spider-audio-merger-splitter.md) |
| Spider CV Merger & Splitter | SPDC | spider-cv_front_labeled.png | spider-cv_back_labeled.png | spider-cv.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Spider CV (not added; out of scope) | [spider-cv-merger-splitter.md](spider-cv-merger-splitter.md) |
| Pulsar Dual LFO | PULS | pulsar_front_labeled.png | pulsar_back_labeled.png | pulsar.json | done 2026-10-07: every position hover-checked in Reason. Rack Extension; name_check cannot run: our remotemap has no Scope block for Pulsar (not added; out of scope) | [pulsar-dual-lfo.md](pulsar-dual-lfo.md) |
| RPG-8 Monophonic Arpeggiator | RPG8 | rpg-8_front_labeled.png | rpg-8_back_labeled.png | rpg-8.json | done 2026-10-07: all positions hover-checked in Reason; Pattern turned on briefly to read step tooltips, then off; name_check can't run (no RPG-8 Scope block in remotemap, not edited) | [rpg-8-monophonic-arpeggiator.md](rpg-8-monophonic-arpeggiator.md) |
| Line Mixer 6:2 | LNMX | line-mixer_front_labeled.png | line-mixer_back_labeled.png | line-mixer.json | done 2026-10-07: all 79 positions hover-checked in Reason; name_check: Remote items all matched, only error is no Line Mixer Scope block in remotemap (not edited) | [line-mixer-6-2.md](line-mixer-6-2.md) |
| Mixer 14:2 | MX14 | mixer-14-2_front_labeled.png | mixer-14-2_back_labeled.png | mixer-14-2.json | done 2026-10-07: all 324 positions hover-checked in Reason; name_check: Remote items all matched; only errors are no Mixer 14:2 Scope block in remotemap (not edited) and 3-digit codes K100-K102 failing the checker's 2-digit code pattern (codes kept, checker not edited) | [mixer-14-2.md](mixer-14-2.md) |
| Mix Channel | MXCH | mix-channel_front_labeled.png | mix-channel_back_labeled.png | mix-channel.json | done 2026-10-07: all 31 positions hover-checked in Reason. name_check can't pass: vocab lists this device as 'Reason Main Mixer Channel' (not 'Mix Channel') and the remotemap has no Scope block (not edited). Remote names used (Mute, Solo, Level, Pan, Bypass Insert FX, Channel Name) all appear in that vocab entry. Audio Output menu not opened (no tooltip). Insert FX slot was empty, so no insert-FX controls exist to map. Two tooltips cut off at the zoom edge (Bypass ... Off; Show in Spectrum EQ Window). | [mix-channel.md](mix-channel.md) |
| Combinator | COMB | combinator_front_labeled.png | combinator_back_labeled.png | combinator.json | done 2026-10-07: all 47 positions hover-checked in Reason (default Init Patch panel: Control 1-4, Switch 1-4). Unfolded Combinator mixer and the Programmer/Devices views are separate views, not mapped here. Selector dropdowns not opened. Orange light and green meters have no tooltip; their Remote item (Audio In/Out, Note On indicators) not confirmed, so left unnamed. name_check PASS (0 errors; 20 warnings: Remote items like Rotary 5-16, Run Pattern Devices, Bypass All FX have no control on this default panel; patch up/down arrows are one row named Select Next Patch, top half is Select Previous Patch). | [combinator.md](combinator.md) |
| Audio Track | AUDT | audio-track_front_labeled.png | audio-track_back_labeled.png | audio-track.json | done 2026-10-07: all 15 positions checked in Reason (11 front, 4 back). name_check: only errors are no vocab entry and no Scope block (Audio Track has no Remote map). Back has no jacks. Level fader checked on the handle. | [audio-track.md](audio-track.md) |
| Hardware Interface | HWIF | hardware-interface_front_labeled.png | hardware-interface_back_labeled.png | hardware-interface.json | done 2026-10-07: all 354 positions (207 front, 147 back) checked in Reason. Rack name seen in tooltips: 'Hardware Interface II'. Front meters name the right channel of each pair; D16, D40, D64 name other channels (recorded as seen). name_check: only the expected no-vocab/no-Scope errors. | [hardware-interface.md](hardware-interface.md) |
| Master Section | MSEC | master-section_front_labeled.png | master-section_back_labeled.png | master-section.json | done 2026-10-07: all 59 positions (13 front, 46 back) checked in Reason. Device name here is the rack Master Section panel; the remotemap 'Reason Master Section' scope is the mixer's channel Remote scope, so it does not apply. name_check: only the expected no-vocab/no-Scope errors. | [master-section.md](master-section.md) |
| Main Mixer | MMIX | main-mixer_front_labeled.png | — (mixer window has no back) | main-mixer.json | done 2026-10-07: ASSUMED view = Reason's Main Mixer window (F5), one representative channel strip (the Mix Channel strip) plus the master strip, stitched from 4 scroll slices (picture is 4 stacked slices, each 1362 px tall; overlaps repeat but each control is boxed once). Other channel strips repeat the same controls. All 168 positions hovered in Reason; faders, meters and displays show no tooltip in this window (recorded as seen). name_check: only the expected no-vocab/no-Scope errors. | [main-mixer.md](main-mixer.md) |
| Channel EQ | CEQ | channel-eq_front_labeled.png | channel-eq_back_labeled.png | channel-eq.json | done 2026-10-07: all 44 positions (25 front, 19 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'ChannelEQ'); 'what' lines spot-checked against manual ch.58. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). Rack Channel EQ attached itself to the Mix Channel's insert chain, so its audio jacks show cables. | [channel-eq.md](channel-eq.md) |
| Channel Dynamics | CDYN | channel-dynamics_front_labeled.png | channel-dynamics_back_labeled.png | channel-dynamics.json | done 2026-10-07: all 33 positions (22 front, 11 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'ChannelDynamics'); 'what' lines spot-checked against manual ch.57. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). | [channel-dynamics.md](channel-dynamics.md) |
| Master Bus Compressor | MBC | master-bus-compressor_front_labeled.png | master-bus-compressor_back_labeled.png | master-bus-compressor.json | done 2026-10-07: all 23 positions (13 front, 10 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'MasterCompressor'); 'what' lines spot-checked against manual ch.59. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). | [master-bus-compressor.md](master-bus-compressor.md) |
| Sweeper Modulation Effect | SWPR | sweeper_front_labeled.png | sweeper_back_labeled.png | sweeper.json | done 2026-10-07 except two rows (Claude, hover-checked in Reason 12; LFO/Env synced-rate readouts SWPR-F-D05/D06-type rows NOT hovered): Phaser+Envelope main view, Filter view, Audio Follower view, back panel. NOT shown: Flanger view (same controls as Phaser minus Bandwidth/Stages). 7 front controls and 3 back icons give no tooltip (recorded as seen); the 4 audio jacks are cabled so their own names are unread (null). Device Name / BeatSync / Trig On / Stereo Mode / LFO Wave / LFO Sync / Env Loop assignments rest on the Remote list, not a tooltip. | [sweeper-modulation-effect.md](sweeper-modulation-effect.md) |
| Synchronous Effect Modulator | SYNC | synchronous_front_labeled.png | synchronous_back_labeled.png | synchronous.json | done 2026-10-07 (Claude, hover-checked in Reason 12): front (all positions), back (all positions). Display controls (TOOL, RATE, SPEED, FREE, tracks, FRZ/KILL, MASTER OFFSET, PHASE, DIM, MOD CTRL, 10 MOD knobs) give NO tooltip and have no Remote item. Delay Time (ms) row and the 4 audio jack names are unproven (see rows). | [synchronous-effect-modulator.md](synchronous-effect-modulator.md) |
| Audiomatic Retro Transformer | AUDM | audiomatic_front_labeled.png | audiomatic_back_labeled.png | audiomatic.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. No Patch Name item (device has no patch browser). 16 preset buttons all read tooltip 'Preset'. Audio jack names unread (cabled). | [audiomatic-retro-transformer.md](audiomatic-retro-transformer.md) |
| Neptune Pitch Adjuster | NEPT | neptune_front_labeled.png | neptune_back_labeled.png | neptune.json | done 2026-10-07 except noted (Claude, hover-checked in Reason 12): all front and back positions. Remote has case-variant duplicate items (Midi Destination, Mod wheel, Vibrato rate, pitch bend) and 'Pitch Adjust Amount' with no known panel control: rows are placeholders, NOT proven. Faders PITCHED SIGNAL / VOICE SYNTH and 12 note keys give no tooltip. Audio jack names unread (cabled). | [neptune-pitch-adjuster.md](neptune-pitch-adjuster.md) |
| Pulveriser | PULV | pulveriser_front_labeled.png | pulveriser_back_labeled.png | pulveriser.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. Follow (flat Remote item) placed on the follower light, NOT proven. Waveform arrows, light LEDs, routing icons give no tooltip. Audio jack names unread (cabled). | [pulveriser.md](pulveriser.md) |
| Quartet Chorus Ensemble | QRTT | quartet_front_labeled.png | quartet_back_labeled.png | quartet.json | done 2026-10-07 (Claude, hover-checked in Reason 12): BBD main view (pictured), Chorus, FFT and Grain modes, back panel. Stereo selector, FFT Start/End handles give no tooltip (names from Remote list). Audio jack names unread (cabled). Set back to BBD mode. | [quartet-chorus-ensemble.md](quartet-chorus-ensemble.md) |
| Alligator Filter Gate | ALGT | alligator_front_labeled.png | alligator_back_labeled.png | alligator.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. Controls past slot 48 (band Phaser/Delay amounts, Dry Pan, Delay and Phaser sections) have Remote names but no slot in our remotemap. Gate Open lights (flat items), meter lights, pattern/LFO arrows give no usable tooltip. Audio jack names unread (cabled). | [alligator-filter-gate.md](alligator-filter-gate.md) |
| Softube Amp (ReasonAmp) | RAMP | reasonamp_front_labeled.png | reasonamp_back_labeled.png | reasonamp.json | done 2026-10-07 (Claude, hover-checked in Reason 12; rack name 'Softube Amp', Remote name ReasonAmp): all front and back positions. Amp/Cab model lights all show one tooltip each. Lamp, logos, level lights, fuses, ground screw give no tooltip. Audio jack names unread (cabled). | [softube-amp-reasonamp.md](softube-amp-reasonamp.md) |
| Softube Bass Amp (ReasonBassAmp) | RBAS | reasonbassamp_front_labeled.png | reasonbassamp_back_labeled.png | reasonbassamp.json | done 2026-10-07 (Claude, hover-checked in Reason 12; rack name 'Softube Bass Amp', Remote name ReasonBassAmp): all front and back positions. Amp/Cab model lights each show one tooltip. Both patch arrows read 'Select previous patch' in this pass (not told apart). Level lights, fuses, vent, labels give no tooltip. Audio jack names unread (cabled). | [softube-bass-amp-reasonbassamp.md](softube-bass-amp-reasonbassamp.md) |
| Kong Drum Designer | KONG | kong-drum-designer_front_labeled.png | kong-drum-designer_back_labeled.png | kong-drum-designer.json | done 2026-10-08 (Claude, hover-checked in Reason 12): main panel, enlarged right column, Drum and FX section (Drum 1 / Bass Drum state) and back panel. The 16 drum modules differ; only Drum 1 pictured. LCD knobs (offsets, sends, pan, tone, level) gave no tooltip; names from the Remote list. Rows K301-K345 are aliases of the one LCD knob for Drum 2-16. | [kong-drum-designer.md](kong-drum-designer.md) |
| Redrum Drum Computer | REDR | redrum-drum-computer_front_labeled.png | redrum-drum-computer_back_labeled.png | redrum-drum-computer.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front (10 channels + pattern section) and back. Channels 1-4 fully hovered; channels 5-10 hovered except the two small lights and SELECT (no tooltip seen on channels 1-4). Step buttons, SELECT, lights, patch/sample displays gave no tooltip: names from the Remote list. | [redrum-drum-computer.md](redrum-drum-computer.md) |
| Dr. Octo Rex Loop Player | DREX | dr-rex-loop-player_front_labeled.png | dr-rex-loop-player_back_labeled.png | dr-rex-loop-player.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front with Programmer open, and back. Loop buttons, loop-name displays, lamps, RUN, filter-mode lights, LFO wave/dest lights gave no tooltip: names from the Remote list. Remote slot 10 'Selected Loop in Editor' has no proven control (stand-in row, low confidence). Lower half of loop-file arrows and Trigger-Next BAR/BEAT/1/16 buttons not separately proven. | [dr-octo-rex-loop-player.md](dr-octo-rex-loop-player.md) |
| Mimic Creative Sampler | MIMC | mimic_front_labeled.png | mimic_back_labeled.png | mimic.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front (Slot 1 selected) and back. Menus, modes, slot tabs, envelope D/S sliders, wheels, markers gave no tooltip: names from the Remote list. Remote has Slot 1-8 versions of every control; one physical control serves all; rows K301-K335 are aliases for slots 2-8. Slot 43 'Algorithm' placed on the stretch menu (low confidence). Some knobs (Start/Pitch/Pan mod amounts, Filter Kbd/Vel, Send 2, wheels) have tooltip names but no Remote item. | [mimic-creative-sampler.md](mimic-creative-sampler.md) |
| Thor Polysonic Synthesizer | THOR | thor_front_labeled.png | thor_back_labeled.png | thor.json | PARTIAL 2026-10-08: front+back+Filter 2 view hovered; matrix rows other than 1, 8, 12 inferred from pattern; Programmer panel + step sequencer panel not mapped | [thor-polysonic-synthesizer.md](thor-polysonic-synthesizer.md) |
| Grain Sample Manipulator | GRAN | grain_front_labeled.png | grain_back_labeled.png | grain.json | PARTIAL 2026-10-08: front (top + lower views + 5 effect panels) and back hovered; matrix rows 2-8 inferred from row 1; other grain algorithm modes (Formant knob) and LFO 3 not captured | [grain-sample-manipulator.md](grain-sample-manipulator.md) |
| Europa Shapeshifting Synthesizer | EURO | europa_front_labeled.png | europa_back_labeled.png | europa.json | PARTIAL 2026-10-08: front (engine I, 2 other engine views, lower view, 6 effect panels) and back hovered; engine III hovered on 10 of 43 controls (rest by pattern); LFO 2/3 and envelopes 1/3/4 tabs not opened; Europa displays/menus give no tooltip | [europa-shapeshifting-synthesizer.md](europa-shapeshifting-synthesizer.md) |
| Malstrom Graintable Synthesizer | MALS | malstrom_front_labeled.png | malstrom_back_labeled.png | malstrom.json | PARTIAL: all front and back controls hovered; front mapped from one picture | [malstrom-graintable-synthesizer.md](malstrom-graintable-synthesizer.md) |
| Humana Vocal Ensemble | HUMA | humana_front_labeled.png | humana_back_labeled.png | humana.json | PARTIAL: all front and back controls hovered; syllable buttons in the sample display not mapped | [humana-vocal-ensemble.md](humana-vocal-ensemble.md) |
| NN19 Digital Sampler | NN19 | nn19_front_labeled.png | nn19_back_labeled.png | nn19.json | PARTIAL: all front and back controls hovered; sample-name/key text readouts under the keymap not mapped | [nn19-digital-sampler.md](nn19-digital-sampler.md) |
| SubTractor Analog Synthesizer | SUBT | subtractor_front_labeled.png | subtractor_back_labeled.png | subtractor.json | PARTIAL: all front and back controls hovered; radio LED rows and the two display text fields not hovered | [subtractor-analog-synthesizer.md](subtractor-analog-synthesizer.md) |
| Radical Piano | RADP | radical-piano_front_labeled.png | radical-piano_back_labeled.png | radical-piano.json | PARTIAL: all knobs, buttons and back jacks hovered; mic LED groups hovered once per group | [radical-piano.md](radical-piano.md) |
| Monotone Bass Synthesizer | MONO | monotone_front_labeled.png | monotone_back_labeled.png | monotone.json | mapped 2026-10-15; every position hovered in Reason (range spinner, fold arrow, patch display, small light: no tooltip) | [monotone-bass-synthesizer.md](monotone-bass-synthesizer.md) |
| Pangea World Instruments | PANG | pangea_front_labeled.png | pangea_back_labeled.png | pangea.json | mapped 2026-10-15; every position hovered in Reason (fold arrow, NOTE light, range spinner, instrument dropdown, filter type menu: no tooltip) | [pangea-world-instruments.md](pangea-world-instruments.md) |
| Klang Tuned Percussion | KLNG | klang_front_labeled.png | klang_back_labeled.png | klang.json | mapped 2026-10-15; every position hovered in Reason (fold arrow, NOTE light, instrument dropdown, filter type menu: no tooltip) | [klang-tuned-percussion.md](klang-tuned-percussion.md) |
| NN-XT Advanced Sampler | NNXT | nn-xt_front_labeled.png | nn-xt_back_labeled.png | nn-xt.json | main panel + back mapped 2026-10-15; every position hovered in Reason; NN-XT Remote Editor (folded sample editor) NOT mapped | [nn-xt-advanced-sampler.md](nn-xt-advanced-sampler.md) |
| ID8 Instrument Device | ID8 | id8_front_labeled.png | id8_back_labeled.png | id8.json | mapped 2026-10-15; every position hovered in Reason (category/parameter displays, sound list, tape, back power switch: no tooltip). Remote items Category Name, Preset, Sound, Sound Name, Select Next/Previous Preset/Sound have no proven panel control | [id8-instrument-device.md](id8-instrument-device.md) |
| BV512 Digital Vocoder | BV51 | bv512_front_labeled.png | bv512_back_labeled.png | bv512.json | mapped 2026-10-15; every position hovered in Reason (fold arrows, meters, display, small light, back icons: no tooltip). No Scope block in our remotemap, so no knob slots/CC; names from remote-vocab.json. Only 16 of the 32 Remote band levels are on the panel | [bv512-digital-vocoder.md](bv512-digital-vocoder.md) |
| Rytmik Drum Machine | RYTM | rytmik_front_labeled.png | rytmik_back_labeled.png | rytmik.json | mapped 2026-10-15 (main panel with KICK selected + back); every position hovered in Reason (sample readouts, waveform/filter displays, faders, pads: no tooltip). No Remote map for Rytmik: no slots/CC. Other drums' sample section views not mapped separately | [rytmik-drum-machine.md](rytmik-drum-machine.md) |
| MIDI Out Device | MIDO | midi-out_front_labeled.png | midi-out_back_labeled.png | midi-out.json | mapped 2026-10-15; every position hovered in Reason (wheel-side lights, arrows, device menu, tape: no tooltip). No Remote map: no slots/CC. Device menu not opened | [midi-out-device.md](midi-out-device.md) |
| Elements DS-LFO (AirRaid) | DSLF | elements-ds-lfo_front_labeled.png | elements-ds-lfo_back_labeled.png | elements-ds-lfo.json | mapped 2026-10-15 (AirRaid Rack Extension, no Remote map); every position hovered in Reason (fold arrow, shape arrows, LFO 2 SYNC/MODE: no tooltip) | [elements-ds-lfo-airraid.md](elements-ds-lfo-airraid.md) |
| Morfin XF Crossfader (Groovy Melon) | MORF | morfin-xf_front_labeled.png | morfin-xf_back_labeled.png | morfin-xf.json | mapped 2026-10-15 (Groovy Melon Rack Extension, no Remote map); every position hovered in Reason (fold arrow: no tooltip). Fade-type light ring not mapped separately | [morfin-xf-crossfader-groovy-melon.md](morfin-xf-crossfader-groovy-melon.md) |
| A/B 12 Audio Out Switch (pongasoft) | AB12 | ab12-audio-out_front_labeled.png | ab12-audio-out_back_labeled.png | ab12-audio-out.json | mapped 2026-10-15 (pongasoft Rack Extension, no Remote map); front: every knob hovered, buttons/displays/A-B/lights no tooltip. Back: A1/B1 gate jacks hovered, other gate jacks by row pattern (marked) | [a-b-12-audio-out-switch-pongasoft.md](a-b-12-audio-out-switch-pongasoft.md) |
| A/B Audio & CV Switch (pongasoft) | ABSW | ab-switch_front_labeled.png | ab-switch_back_labeled.png | ab-switch.json | mapped 2026-10-15 (pongasoft RE, no Remote map); back jacks all hovered; front knob/light tooltips partly ambiguous (marked) | [a-b-audio-cv-switch-pongasoft.md](a-b-audio-cv-switch-pongasoft.md) |
| CVA-7 CV Analyzer (pongasoft) | CVA7 | cva-7_front_labeled.png | cva-7_back_labeled.png | cva-7.json | mapped 2026-10-15 (pongasoft RE, no Remote map); front all hovered; back: CV In/trim/aux outs hovered, CV Out slider/jack 1-4 by row pattern (marked) | [cva-7-cv-analyzer-pongasoft.md](cva-7-cv-analyzer-pongasoft.md) |
| RE 181 Mid/Side Audio Converter | RE18 | re181-mid-side_front_labeled.png | re181-mid-side_back_labeled.png | re181-mid-side.json | mapped 2026-10-15 (Red Rock Sound RE, no Remote map); back jacks all hovered; front: only the two LISTEN buttons have tooltips, rest are meters/lights | [re-181-mid-side-audio-converter.md](re-181-mid-side-audio-converter.md) |
| Select CV Switch (Robotic Bean) | SELC | select-cv-switch_front_labeled.png | select-cv-switch_back_labeled.png | select-cv-switch.json | mapped 2026-10-15 (Robotic Bean RE, no Remote map); back: all named by tooltip (jacks 3-7 by pattern, marked); front buttons/displays have no tooltips | [select-cv-switch-robotic-bean.md](select-cv-switch-robotic-bean.md) |
| RPSpec Spectrogram (Rob Papen) | RPSP | rpspec_front_labeled.png | rpspec_back_labeled.png | rpspec.json | mapped 2026-10-15 (Rob Papen RE, no Remote map); 4 front controls have tooltips; view icons/mode/readouts have none and were not clicked; back jacks cabled (own names not read) | [rpspec-spectrogram-rob-papen.md](rpspec-spectrogram-rob-papen.md) |
| Elements Splitter (AirRaid) | SPLT | elements-splitter_front_labeled.png | elements-splitter_back_labeled.png | elements-splitter.json | mapped 2026-10-15 (AirRaid RE 'Elements Splitter 2', no Remote map); nearly all hovered; a few On/M/S buttons gave no tooltip (marked); a few CV jacks by neighbour pattern (marked) | [elements-splitter-airraid.md](elements-splitter-airraid.md) |
| kHs Chorus (kiloHearts) | KHSC | khs-chorus_front_labeled.png | khs-chorus_back_labeled.png | khs-chorus.json | mapped 2026-10-15 (kiloHearts RE, no Remote map); every position hovered in Reason (tape/logo: no tooltip) | [khs-chorus-kilohearts.md](khs-chorus-kilohearts.md) |
| Efektor Silencer Noise Gate (Kuassa) | SILN | efektor-silencer_front_labeled.png | efektor-silencer_back_labeled.png | efektor-silencer.json | mapped 2026-10-15 (Kuassa RE, no Remote map); front all hovered; back audio jacks hovered, 4 small jacks near INPUT/OUTPUT labels had no tooltip and are not identified | [efektor-silencer-noise-gate-kuassa.md](efektor-silencer-noise-gate-kuassa.md) |


## Where each fact came from
- Pictures: screenshots of John's Reason 12.7, in a blank test song made from his template.
- Remote names: remote/ReasonVoice.remotemap (Scream 4 scope) and docs/reason/remote-vocab.json.
- Jack and control names: Reason's own tooltips and cable menus.
- What each control does: Reason 12.7 manual, chapter 51 (~/.reason_voice/reason12_manual/full_chapters/51-scream-4-sound-destruction-unit.txt). All 38 rows agree with it.
- Positions: measured from the picture, then every one hover-tested in Reason (2026-10-03).

## Not in our Remote map (Reason has them, our map doesn't send them)
- Select Previous/Next Patch (SCR4-F-B03/B09). "Select Patch Delta" is a Remote item with no control of its own on the panel (it steps patches by an amount), so it has no code. The trims (SCR4-B-K01–K04) have no Remote item at all.

## Still open
- Hermes doesn't have a copy yet (Phase 5).

=====================================================
SOURCE FILE: a-b-12-audio-out-switch-pongasoft.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/chapters/a-b-12-audio-out-switch-pongasoft.md
=====================================================

## A/B 12 Audio Out Switch (pongasoft) — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AB12-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip (fold arrow); checked by eye |
| AB12-F-D05 | AB12AUDOUT 1 tape | Device name tape (vertical, left edge) | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D01 | A1 display | Name display for output A1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K01 | A1 VOLUME | Volume of output A1 | — | — | click only | tooltip "Volume [A1]: 0.00 dB" |
| AB12-F-B02 | A1 button | Switch button for output A1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D06 | A2 display | Name display for output A2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K05 | A2 VOLUME | Volume of output A2 | — | — | click only | tooltip "Volume [A2]: 0.00 dB" |
| AB12-F-B06 | A2 button | Switch button for output A2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D11 | A3 display | Name display for output A3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K10 | A3 VOLUME | Volume of output A3 | — | — | click only | tooltip "Volume [A3]: 0.00 dB" |
| AB12-F-B10 | A3 button | Switch button for output A3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B03 | A4 button | Switch button for output A4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K02 | A4 VOLUME | Volume of output A4 | — | — | click only | tooltip "Volume [A4]: 0.00 dB" |
| AB12-F-D02 | A4 display | Name display for output A4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B07 | A5 button | Switch button for output A5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K06 | A5 VOLUME | Volume of output A5 | — | — | click only | tooltip "Volume [A5]: 0.00 dB" |
| AB12-F-D07 | A5 display | Name display for output A5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B11 | A6 button | Switch button for output A6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K11 | A6 VOLUME | Volume of output A6 | — | — | click only | tooltip "Volume [A6]: 0.00 dB" |
| AB12-F-D12 | A6 display | Name display for output A6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D03 | B1 display | Name display for output B1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K03 | B1 VOLUME | Volume of output B1 | — | — | click only | tooltip "Volume [B1]: 0.00 dB" |
| AB12-F-B04 | B1 button | Switch button for output B1 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D09 | B2 display | Name display for output B2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K08 | B2 VOLUME | Volume of output B2 | — | — | click only | tooltip "Volume [B2]: 0.00 dB" |
| AB12-F-B08 | B2 button | Switch button for output B2 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D13 | B3 display | Name display for output B3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K12 | B3 VOLUME | Volume of output B3 | — | — | click only | tooltip "Volume [B3]: 0.00 dB" |
| AB12-F-B15 | B3 button | Switch button for output B3 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B05 | B4 button | Switch button for output B4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K04 | B4 VOLUME | Volume of output B4 | — | — | click only | tooltip "Volume [B4]: 0.00 dB" |
| AB12-F-D04 | B4 display | Name display for output B4 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B09 | B5 button | Switch button for output B5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K09 | B5 VOLUME | Volume of output B5 | — | — | click only | tooltip "Volume [B5]: 0.00 dB" |
| AB12-F-D10 | B5 display | Name display for output B5 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B16 | B6 button | Switch button for output B6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K13 | B6 VOLUME | Volume of output B6 | — | — | click only | tooltip "Volume [B6]: 0.00 dB" |
| AB12-F-D14 | B6 display | Name display for output B6 | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D08 | A / B indicator lights | Shows which bank is active (A or B light) | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-K07 | A/B big knob | Bank switch knob (no tooltip) | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-B12 | MODE SELECT Single | Mode select: Single / Multi / Instr (tooltip 'Mode Select' on all three) | — | — | click only | tooltip "Mode Select" |
| AB12-F-B13 | MODE SELECT Multi | Mode select: Single / Multi / Instr | — | — | click only | tooltip "Mode Select" |
| AB12-F-B14 | MODE SELECT Instr | Mode select: Single / Multi / Instr | — | — | click only | tooltip "Mode Select" |
| AB12-F-B17 | SOFTEN | Soften (smooths switching) | — | — | click only | tooltip "Soften" |
| AB12-F-D15 | SINGLE OV light | Single override light | — | — | click only | no tooltip in Reason (hovered 2 s) |
| AB12-F-D16 | BANK OV light | Bank override light | — | — | click only | no tooltip in Reason (hovered 2 s) |

## A/B 12 Audio Out Switch (pongasoft) — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AB12-B-J01 | Audio Out A1 Left (mono) | Audio output A1, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A1] Output Left" |
| AB12-B-J02 | Audio Out A2 Left (mono) | Audio output A2, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A2] Output Left" |
| AB12-B-J03 | Audio Out A3 Left (mono) | Audio output A3, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A3] Output Left" |
| AB12-B-J04 | Audio Out A4 Left (mono) | Audio output A4, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A4] Output Left" |
| AB12-B-J05 | Audio Out A5 Left (mono) | Audio output A5, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A5] Output Left" |
| AB12-B-J06 | Audio Out A6 Left (mono) | Audio output A6, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A6] Output Left" |
| AB12-B-J07 | Audio Out B1 Left (mono) | Audio output B1, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B1] Output Left" |
| AB12-B-J08 | Audio Out B2 Left (mono) | Audio output B2, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B2] Output Left" |
| AB12-B-J09 | Audio Out B3 Left (mono) | Audio output B3, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B3] Output Left" |
| AB12-B-J10 | Audio Out B4 Left (mono) | Audio output B4, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B4] Output Left" |
| AB12-B-J11 | Audio Out B5 Left (mono) | Audio output B5, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B5] Output Left" |
| AB12-B-J12 | Audio Out B6 Left (mono) | Audio output B6, left/mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B6] Output Left" |
| AB12-B-J14 | Audio Out A1 Right | Audio output A1, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A1] Output Right" |
| AB12-B-J15 | Audio Out A2 Right | Audio output A2, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A2] Output Right" |
| AB12-B-J16 | Audio Out A3 Right | Audio output A3, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A3] Output Right" |
| AB12-B-J17 | Audio Out A4 Right | Audio output A4, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A4] Output Right" |
| AB12-B-J18 | Audio Out A5 Right | Audio output A5, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A5] Output Right" |
| AB12-B-J19 | Audio Out A6 Right | Audio output A6, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A6] Output Right" |
| AB12-B-J20 | Audio Out B1 Right | Audio output B1, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B1] Output Right" |
| AB12-B-J21 | Audio Out B2 Right | Audio output B2, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B2] Output Right" |
| AB12-B-J22 | Audio Out B3 Right | Audio output B3, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B3] Output Right" |
| AB12-B-J23 | Audio Out B4 Right | Audio output B4, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B4] Output Right" |
| AB12-B-J24 | Audio Out B5 Right | Audio output B5, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B5] Output Right" |
| AB12-B-J25 | Audio Out B6 Right | Audio output B6, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B6] Output Right" |
| AB12-B-J27 | Gate In A1 | Gate input A1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In [A1]" |
| AB12-B-J29 | Gate In A2 | Gate input A2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A2]' assumed |
| AB12-B-J31 | Gate In A3 | Gate input A3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A3]' assumed |
| AB12-B-J33 | Gate In A4 | Gate input A4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A4]' assumed |
| AB12-B-J35 | Gate In A5 | Gate input A5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A5]' assumed |
| AB12-B-J37 | Gate In A6 | Gate input A6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [A1]; tooltip pattern 'Gate In [A6]' assumed |
| AB12-B-J39 | Gate In B1 | Gate input B1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In [B1]" |
| AB12-B-J41 | Gate In B2 | Gate input B2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B2]' assumed |
| AB12-B-J43 | Gate In B3 | Gate input B3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B3]' assumed |
| AB12-B-J45 | Gate In B4 | Gate input B4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B4]' assumed |
| AB12-B-J47 | Gate In B5 | Gate input B5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B5]' assumed |
| AB12-B-J49 | Gate In B6 | Gate input B6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate In [B1]; tooltip pattern 'Gate In [B6]' assumed |
| AB12-B-J28 | Gate Out A1 | Gate output A1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out [A1]" |
| AB12-B-J30 | Gate Out A2 | Gate output A2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A2]' assumed |
| AB12-B-J32 | Gate Out A3 | Gate output A3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A3]' assumed |
| AB12-B-J34 | Gate Out A4 | Gate output A4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A4]' assumed |
| AB12-B-J36 | Gate Out A5 | Gate output A5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A5]' assumed |
| AB12-B-J38 | Gate Out A6 | Gate output A6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [A1]; tooltip pattern 'Gate Out [A6]' assumed |
| AB12-B-J40 | Gate Out B1 | Gate output B1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out [B1]" |
| AB12-B-J42 | Gate Out B2 | Gate output B2 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B2]' assumed |
| AB12-B-J44 | Gate Out B3 | Gate output B3 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B3]' assumed |
| AB12-B-J46 | Gate Out B4 | Gate output B4 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B4]' assumed |
| AB12-B-J48 | Gate Out B5 | Gate output B5 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B5]' assumed |
| AB12-B-J50 | Gate Out B6 | Gate output B6 | — | — | cable: right-click jack > device > jack name | not hovered separately: same row as hovered Gate Out [B1]; tooltip pattern 'Gate Out [B6]' assumed |
| AB12-B-J13 | Main Audio In Left | Main audio input, left | — | — | cable: right-click jack > device > jack name | tooltip "Audio Input Left" |
| AB12-B-J26 | Main Audio In Right | Main audio input, right | — | — | cable: right-click jack > device > jack name | tooltip "Audio Input Right" |
| AB12-B-J52 | CV In (single mode) | CV input for single mode | — | — | cable: right-click jack > device > jack name | tooltip "CV in Switch State (single)" |
| AB12-B-B04 | Keyboard Single switch | Keyboard control of single mode: Disabled / Enabled | — | — | click/drag only (no Remote item) | tooltip "Keyboard (Single)" |
| AB12-B-B02 | Volume Change Filter switch | Volume change filter Off / On | — | — | click/drag only (no Remote item) | tooltip "Volume Change Filter" |
| AB12-B-J51 | CV Banks In | CV input for banks | — | — | cable: right-click jack > device > jack name | tooltip "CV in" |
| AB12-B-B03 | CV Banks mapping switch | Bank CV mapping: Unipolar / Bipolar / Note | — | — | click/drag only (no Remote item) | tooltip "Bank CV Mapping: Bipolar" |
| AB12-B-D02 | QR code | pongasoft QR code (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 2 s) |
| AB12-B-D03 | Power switch (drawn) | Power connector area (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 2 s) |
| AB12-B-D01 | AB12AUDOUT 1 tape (back) | Device name tape on the back | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 2 s) |
| AB12-B-B01 | (triangle, back) | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip (fold arrow); checked by eye |

=====================================================
SOURCE FILE: a-b-audio-cv-switch-pongasoft.md
ORIGINAL LOCATION: HS:device_refs/_panel_map/chapters/a-b-audio-cv-switch-pongasoft.md
=====================================================

## A/B Audio & CV Switch (pongasoft) — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| ABSW-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip (fold arrow); checked by eye |
| ABSW-F-D01 | A/B Switch title | Title text (no tooltip) | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-K01 | AUDIO SWITCH knob | Audio switch knob: chooses A or B | — | — | click only | tooltip "Switch Audio A & B" |
| ABSW-F-D02 | AUDIO A light | Audio A active light | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D06 | AUDIO B light | Audio B active light | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D03 | AUDIO A name field | Name field for audio A | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D07 | AUDIO B name field | Name field for audio B | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-B02 | SOFTEN | Soften (smooths switching) | — | — | click only | tooltip "Soften" |
| ABSW-F-D08 | wave icon | Small waveform icon (no tooltip) | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D09 | ABSWITCH 1 tape | Device name tape | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-K02 | CV SWITCH knob | CV switch knob: chooses A or B | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D04 | CV A light | CV A active light | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D10 | CV B light | CV B active light | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D05 | CV A name field | Name field for CV A | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D11 | CV B name field | Name field for CV B | — | — | click only | no tooltip in Reason (hovered 1.4 s) |
| ABSW-F-D12 | pongasoft logo/QR | Logo and small code (no tooltip) | — | — | click only | no tooltip in Reason (hovered 1.4 s) |

## A/B Audio & CV Switch (pongasoft) — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| ABSW-B-J01 | Audio A In L/Mono | Audio jack: Audio A In L/Mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A] Input Left" |
| ABSW-B-J02 | Audio A In R | Audio jack: Audio A In R | — | — | cable: right-click jack > device > jack name | tooltip "Audio [A] Input Right" |
| ABSW-B-J03 | Audio B In L/Mono | Audio jack: Audio B In L/Mono | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B] Input Left" |
| ABSW-B-J04 | Audio B In R | Audio jack: Audio B In R | — | — | cable: right-click jack > device > jack name | tooltip "Audio [B] Input Right" |
| ABSW-B-J05 | Audio Out L/Mono | Audio jack: Audio Out L/Mono | — | — | cable: right-click jack > device > jack name | tooltip "Switched Audio Output Left" |
| ABSW-B-J06 | Audio Out R | Audio jack: Audio Out R | — | — | cable: right-click jack > device > jack name | tooltip "Switched Audio Output Right" |
| ABSW-B-J07 | Audio CV Control In | CV input that switches the audio | — | — | cable: right-click jack > device > jack name | tooltip "CV In (Audio switch control)" |
| ABSW-B-J08 | CV A In | CV input A | — | — | cable: right-click jack > device > jack name | tooltip "CV [A] Input" |
| ABSW-B-J09 | CV B In | CV input B | — | — | cable: right-click jack > device > jack name | tooltip "CV [B] Input" |
| ABSW-B-J10 | CV Out | Switched CV output | — | — | cable: right-click jack > device > jack name | tooltip "Switched CV Output" |
| ABSW-B-J11 | CV Control In | CV input that switches the CV | — | — | cable: right-click jack > device > jack name | tooltip "CV In (CV switch control)" |
| ABSW-B-D02 | Power area (drawn) | Power cable area (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.4 s) |
| ABSW-B-D01 | ABSWITCH 1 tape (back) | Device name tape | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.4 s) |
| ABSW-B-B01 | (triangle, back) | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip (fold arrow); checked by eye |

=== END OF PART ===
