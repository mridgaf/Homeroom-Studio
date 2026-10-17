# Chapter 08: Reason panel map
## Part 1 of 44

_Front and back panel maps of Reason devices: every knob, button and jack, by device._

**In this part:**
- PANEL-MAP.md (piece 1 of 21) — Panel Map — every knob, button, slider and jack, with a code

(Next: Part 2 of 44)


=====================================================
SOURCE FILE: PANEL-MAP.md (piece 1 of 21)
ORIGINAL LOCATION: HS:device_refs/_panel_map/PANEL-MAP.md
=====================================================

# Panel Map — every knob, button, slider and jack, with a code

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
| Device | Code | Front | Back | Data | Status |
|---|---|---|---|---|---|
| Scream 4 Distortion | SCR4 | scream-4_front_labeled.png | scream-4_back_labeled.png | scream-4.json | **done** — all 38 checked in Reason, manual ch.51 checked |
| The Echo | ECHO | the-echo_front_labeled.png | the-echo_back_labeled.png | the-echo.json | **done** — 48/48 checked in Reason; manual ch.50 spot-checked; drafted by helper |
| CF-101 Chorus/Flanger | CF101 | cf-101_front_labeled.png | cf-101_back_labeled.png | cf-101.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| COMP-01 Compressor | COMP01 | comp-01_front_labeled.png | comp-01_back_labeled.png | comp-01.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| D-11 Foldback Distortion | D11 | d-11_front_labeled.png | d-11_back_labeled.png | d-11.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| DDL-1 Digital Delay Line | DDL1 | ddl-1_front_labeled.png | ddl-1_back_labeled.png | ddl-1.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| ECF-42 Envelope Controlled Filter | ECF42 | ecf-42_front_labeled.png | ecf-42_back_labeled.png | ecf-42.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual; ONE ASSUMING: GATE light (ECF42-F-D02) = Remote 'Trigger' (no tooltip, unproven) |
| PEQ-2 Two Band Parametric EQ | PEQ2 | peq-2_front_labeled.png | peq-2_back_labeled.png | peq-2.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| PH-90 Phaser | PH90 | ph-90_front_labeled.png | ph-90_back_labeled.png | ph-90.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| RV-7 Digital Reverb | RV7 | rv-7_front_labeled.png | rv-7_back_labeled.png | rv-7.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| UN-16 Unison | UN16 | un-16_front_labeled.png | un-16_back_labeled.png | un-16.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| MClass Compressor | MCMP | mclass-compressor_front_labeled.png | mclass-compressor_back_labeled.png | mclass-compressor.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual (picture tape reads M COMP 2; this song's instance reads M COMP 1) |
| MClass Equalizer | MEQ | mclass-equalizer_front_labeled.png | mclass-equalizer_back_labeled.png | mclass-equalizer.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| MClass Maximizer | MMAX | mclass-maximizer_front_labeled.png | mclass-maximizer_back_labeled.png | mclass-maximizer.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| MClass Stereo Imager | MSIM | mclass-stereo-imager_front_labeled.png | mclass-stereo-imager_back_labeled.png | mclass-stereo-imager.json | done 2026-10-07: all positions hover-checked in Reason 12 by Claude; name_check PASS; 'what' lines spot-checked against the manual |
| RV7000 Mk II Advanced Reverb | RV7K | rv7000_front_labeled.png | rv7000_back_labeled.png | rv7000.json | done 2026-10-07: everything hover-checked; soft knobs (RV7K-F-K05..K12) numbered by position per owner, their names change by page; programmer EQ and Gate edit-mode views not captured; name_check PASS |
| Matrix Pattern Sequencer | MTRX | matrix_front_labeled.png | matrix_back_labeled.png | matrix.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Matrix (not added; out of scope) |
| Spider Audio Merger & Splitter | SPDA | spider-audio_front_labeled.png | spider-audio_back_labeled.png | spider-audio.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Spider Audio (not added; out of scope) |
| Spider CV Merger & Splitter | SPDC | spider-cv_front_labeled.png | spider-cv_back_labeled.png | spider-cv.json | done 2026-10-07: every position hover-checked in Reason. name_check cannot run: our remotemap has no Scope block for Spider CV (not added; out of scope) |
| Pulsar Dual LFO | PULS | pulsar_front_labeled.png | pulsar_back_labeled.png | pulsar.json | done 2026-10-07: every position hover-checked in Reason. Rack Extension; name_check cannot run: our remotemap has no Scope block for Pulsar (not added; out of scope) |
| RPG-8 Monophonic Arpeggiator | RPG8 | rpg-8_front_labeled.png | rpg-8_back_labeled.png | rpg-8.json | done 2026-10-07: all positions hover-checked in Reason; Pattern turned on briefly to read step tooltips, then off; name_check can't run (no RPG-8 Scope block in remotemap, not edited) |
| Line Mixer 6:2 | LNMX | line-mixer_front_labeled.png | line-mixer_back_labeled.png | line-mixer.json | done 2026-10-07: all 79 positions hover-checked in Reason; name_check: Remote items all matched, only error is no Line Mixer Scope block in remotemap (not edited) |
| Mixer 14:2 | MX14 | mixer-14-2_front_labeled.png | mixer-14-2_back_labeled.png | mixer-14-2.json | done 2026-10-07: all 324 positions hover-checked in Reason; name_check: Remote items all matched; only errors are no Mixer 14:2 Scope block in remotemap (not edited) and 3-digit codes K100-K102 failing the checker's 2-digit code pattern (codes kept, checker not edited) |
| Mix Channel | MXCH | mix-channel_front_labeled.png | mix-channel_back_labeled.png | mix-channel.json | done 2026-10-07: all 31 positions hover-checked in Reason. name_check can't pass: vocab lists this device as 'Reason Main Mixer Channel' (not 'Mix Channel') and the remotemap has no Scope block (not edited). Remote names used (Mute, Solo, Level, Pan, Bypass Insert FX, Channel Name) all appear in that vocab entry. Audio Output menu not opened (no tooltip). Insert FX slot was empty, so no insert-FX controls exist to map. Two tooltips cut off at the zoom edge (Bypass ... Off; Show in Spectrum EQ Window). |
| Combinator | COMB | combinator_front_labeled.png | combinator_back_labeled.png | combinator.json | done 2026-10-07: all 47 positions hover-checked in Reason (default Init Patch panel: Control 1-4, Switch 1-4). Unfolded Combinator mixer and the Programmer/Devices views are separate views, not mapped here. Selector dropdowns not opened. Orange light and green meters have no tooltip; their Remote item (Audio In/Out, Note On indicators) not confirmed, so left unnamed. name_check PASS (0 errors; 20 warnings: Remote items like Rotary 5-16, Run Pattern Devices, Bypass All FX have no control on this default panel; patch up/down arrows are one row named Select Next Patch, top half is Select Previous Patch). |
| Audio Track | AUDT | audio-track_front_labeled.png | audio-track_back_labeled.png | audio-track.json | done 2026-10-07: all 15 positions checked in Reason (11 front, 4 back). name_check: only errors are no vocab entry and no Scope block (Audio Track has no Remote map). Back has no jacks. Level fader checked on the handle. |
| Hardware Interface | HWIF | hardware-interface_front_labeled.png | hardware-interface_back_labeled.png | hardware-interface.json | done 2026-10-07: all 354 positions (207 front, 147 back) checked in Reason. Rack name seen in tooltips: 'Hardware Interface II'. Front meters name the right channel of each pair; D16, D40, D64 name other channels (recorded as seen). name_check: only the expected no-vocab/no-Scope errors. |
| Master Section | MSEC | master-section_front_labeled.png | master-section_back_labeled.png | master-section.json | done 2026-10-07: all 59 positions (13 front, 46 back) checked in Reason. Device name here is the rack Master Section panel; the remotemap 'Reason Master Section' scope is the mixer's channel Remote scope, so it does not apply. name_check: only the expected no-vocab/no-Scope errors. |
| Main Mixer | MMIX | main-mixer_front_labeled.png | — (mixer window has no back) | main-mixer.json | done 2026-10-07: ASSUMED view = Reason's Main Mixer window (F5), one representative channel strip (the Mix Channel strip) plus the master strip, stitched from 4 scroll slices (picture is 4 stacked slices, each 1362 px tall; overlaps repeat but each control is boxed once). Other channel strips repeat the same controls. All 168 positions hovered in Reason; faders, meters and displays show no tooltip in this window (recorded as seen). name_check: only the expected no-vocab/no-Scope errors. |
| Channel EQ | CEQ | channel-eq_front_labeled.png | channel-eq_back_labeled.png | channel-eq.json | done 2026-10-07: all 44 positions (25 front, 19 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'ChannelEQ'); 'what' lines spot-checked against manual ch.58. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). Rack Channel EQ attached itself to the Mix Channel's insert chain, so its audio jacks show cables. |
| Channel Dynamics | CDYN | channel-dynamics_front_labeled.png | channel-dynamics_back_labeled.png | channel-dynamics.json | done 2026-10-07: all 33 positions (22 front, 11 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'ChannelDynamics'); 'what' lines spot-checked against manual ch.57. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). |
| Master Bus Compressor | MBC | master-bus-compressor_front_labeled.png | master-bus-compressor_back_labeled.png | master-bus-compressor.json | done 2026-10-07: all 23 positions (13 front, 10 back) hover-checked in Reason 12 by Claude; name_check PASS (vocab/remotemap name is 'MasterCompressor'); 'what' lines spot-checked against manual ch.59. Test chain Mix Channel > ChanEQ > ChanDyn > MasterComp: audio jacks show cables ('Connected to ...'), cut-off tooltip text noted per row; empty-jack names are what Reason showed. Light/meter/icon rows have no tooltip (by eye). |
| Sweeper Modulation Effect | SWPR | sweeper_front_labeled.png | sweeper_back_labeled.png | sweeper.json | done 2026-10-07 except two rows (Claude, hover-checked in Reason 12; LFO/Env synced-rate readouts SWPR-F-D05/D06-type rows NOT hovered): Phaser+Envelope main view, Filter view, Audio Follower view, back panel. NOT shown: Flanger view (same controls as Phaser minus Bandwidth/Stages). 7 front controls and 3 back icons give no tooltip (recorded as seen); the 4 audio jacks are cabled so their own names are unread (null). Device Name / BeatSync / Trig On / Stereo Mode / LFO Wave / LFO Sync / Env Loop assignments rest on the Remote list, not a tooltip. |
| Synchronous Effect Modulator | SYNC | synchronous_front_labeled.png | synchronous_back_labeled.png | synchronous.json | done 2026-10-07 (Claude, hover-checked in Reason 12): front (all positions), back (all positions). Display controls (TOOL, RATE, SPEED, FREE, tracks, FRZ/KILL, MASTER OFFSET, PHASE, DIM, MOD CTRL, 10 MOD knobs) give NO tooltip and have no Remote item. Delay Time (ms) row and the 4 audio jack names are unproven (see rows). |
| Audiomatic Retro Transformer | AUDM | audiomatic_front_labeled.png | audiomatic_back_labeled.png | audiomatic.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. No Patch Name item (device has no patch browser). 16 preset buttons all read tooltip 'Preset'. Audio jack names unread (cabled). |
| Neptune Pitch Adjuster | NEPT | neptune_front_labeled.png | neptune_back_labeled.png | neptune.json | done 2026-10-07 except noted (Claude, hover-checked in Reason 12): all front and back positions. Remote has case-variant duplicate items (Midi Destination, Mod wheel, Vibrato rate, pitch bend) and 'Pitch Adjust Amount' with no known panel control: rows are placeholders, NOT proven. Faders PITCHED SIGNAL / VOICE SYNTH and 12 note keys give no tooltip. Audio jack names unread (cabled). |
| Pulveriser | PULV | pulveriser_front_labeled.png | pulveriser_back_labeled.png | pulveriser.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. Follow (flat Remote item) placed on the follower light, NOT proven. Waveform arrows, light LEDs, routing icons give no tooltip. Audio jack names unread (cabled). |
| Quartet Chorus Ensemble | QRTT | quartet_front_labeled.png | quartet_back_labeled.png | quartet.json | done 2026-10-07 (Claude, hover-checked in Reason 12): BBD main view (pictured), Chorus, FFT and Grain modes, back panel. Stereo selector, FFT Start/End handles give no tooltip (names from Remote list). Audio jack names unread (cabled). Set back to BBD mode. |
| Alligator Filter Gate | ALGT | alligator_front_labeled.png | alligator_back_labeled.png | alligator.json | done 2026-10-07 (Claude, hover-checked in Reason 12): all front and back positions. Controls past slot 48 (band Phaser/Delay amounts, Dry Pan, Delay and Phaser sections) have Remote names but no slot in our remotemap. Gate Open lights (flat items), meter lights, pattern/LFO arrows give no usable tooltip. Audio jack names unread (cabled). |
| Softube Amp (ReasonAmp) | RAMP | reasonamp_front_labeled.png | reasonamp_back_labeled.png | reasonamp.json | done 2026-10-07 (Claude, hover-checked in Reason 12; rack name 'Softube Amp', Remote name ReasonAmp): all front and back positions. Amp/Cab model lights all show one tooltip each. Lamp, logos, level lights, fuses, ground screw give no tooltip. Audio jack names unread (cabled). |
| Softube Bass Amp (ReasonBassAmp) | RBAS | reasonbassamp_front_labeled.png | reasonbassamp_back_labeled.png | reasonbassamp.json | done 2026-10-07 (Claude, hover-checked in Reason 12; rack name 'Softube Bass Amp', Remote name ReasonBassAmp): all front and back positions. Amp/Cab model lights each show one tooltip. Both patch arrows read 'Select previous patch' in this pass (not told apart). Level lights, fuses, vent, labels give no tooltip. Audio jack names unread (cabled). |
| Kong Drum Designer | KONG | kong-drum-designer_front_labeled.png | kong-drum-designer_back_labeled.png | kong-drum-designer.json | done 2026-10-08 (Claude, hover-checked in Reason 12): main panel, enlarged right column, Drum and FX section (Drum 1 / Bass Drum state) and back panel. The 16 drum modules differ; only Drum 1 pictured. LCD knobs (offsets, sends, pan, tone, level) gave no tooltip; names from the Remote list. Rows K301-K345 are aliases of the one LCD knob for Drum 2-16. |
| Redrum Drum Computer | REDR | redrum-drum-computer_front_labeled.png | redrum-drum-computer_back_labeled.png | redrum-drum-computer.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front (10 channels + pattern section) and back. Channels 1-4 fully hovered; channels 5-10 hovered except the two small lights and SELECT (no tooltip seen on channels 1-4). Step buttons, SELECT, lights, patch/sample displays gave no tooltip: names from the Remote list. |
| Dr. Octo Rex Loop Player | DREX | dr-rex-loop-player_front_labeled.png | dr-rex-loop-player_back_labeled.png | dr-rex-loop-player.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front with Programmer open, and back. Loop buttons, loop-name displays, lamps, RUN, filter-mode lights, LFO wave/dest lights gave no tooltip: names from the Remote list. Remote slot 10 'Selected Loop in Editor' has no proven control (stand-in row, low confidence). Lower half of loop-file arrows and Trigger-Next BAR/BEAT/1/16 buttons not separately proven. |
| Mimic Creative Sampler | MIMC | mimic_front_labeled.png | mimic_back_labeled.png | mimic.json | done 2026-10-08 (Claude, hover-checked in Reason 12): front (Slot 1 selected) and back. Menus, modes, slot tabs, envelope D/S sliders, wheels, markers gave no tooltip: names from the Remote list. Remote has Slot 1-8 versions of every control; one physical control serves all; rows K301-K335 are aliases for slots 2-8. Slot 43 'Algorithm' placed on the stretch menu (low confidence). Some knobs (Start/Pitch/Pan mod amounts, Filter Kbd/Vel, Send 2, wheels) have tooltip names but no Remote item. |
| Thor Polysonic Synthesizer | THOR | thor_front_labeled.png | thor_back_labeled.png | thor.json | PARTIAL 2026-10-08: front+back+Filter 2 view hovered; matrix rows other than 1, 8, 12 inferred from pattern; Programmer panel + step sequencer panel not mapped |
| Grain Sample Manipulator | GRAN | grain_front_labeled.png | grain_back_labeled.png | grain.json | PARTIAL 2026-10-08: front (top + lower views + 5 effect panels) and back hovered; matrix rows 2-8 inferred from row 1; other grain algorithm modes (Formant knob) and LFO 3 not captured |
| Europa Shapeshifting Synthesizer | EURO | europa_front_labeled.png | europa_back_labeled.png | europa.json | PARTIAL 2026-10-08: front (engine I, 2 other engine views, lower view, 6 effect panels) and back hovered; engine III hovered on 10 of 43 controls (rest by pattern); LFO 2/3 and envelopes 1/3/4 tabs not opened; Europa displays/menus give no tooltip |
| Malstrom Graintable Synthesizer | MALS | malstrom_front_labeled.png | malstrom_back_labeled.png | malstrom.json | PARTIAL: all front and back controls hovered; front mapped from one picture |
| Humana Vocal Ensemble | HUMA | humana_front_labeled.png | humana_back_labeled.png | humana.json | PARTIAL: all front and back controls hovered; syllable buttons in the sample display not mapped |
| NN19 Digital Sampler | NN19 | nn19_front_labeled.png | nn19_back_labeled.png | nn19.json | PARTIAL: all front and back controls hovered; sample-name/key text readouts under the keymap not mapped |
| SubTractor Analog Synthesizer | SUBT | subtractor_front_labeled.png | subtractor_back_labeled.png | subtractor.json | PARTIAL: all front and back controls hovered; radio LED rows and the two display text fields not hovered |
| Radical Piano | RADP | radical-piano_front_labeled.png | radical-piano_back_labeled.png | radical-piano.json | PARTIAL: all knobs, buttons and back jacks hovered; mic LED groups hovered once per group |
| Monotone Bass Synthesizer | MONO | monotone_front_labeled.png | monotone_back_labeled.png | monotone.json | mapped 2026-10-15; every position hovered in Reason (range spinner, fold arrow, patch display, small light: no tooltip) |
| Pangea World Instruments | PANG | pangea_front_labeled.png | pangea_back_labeled.png | pangea.json | mapped 2026-10-15; every position hovered in Reason (fold arrow, NOTE light, range spinner, instrument dropdown, filter type menu: no tooltip) |
| Klang Tuned Percussion | KLNG | klang_front_labeled.png | klang_back_labeled.png | klang.json | mapped 2026-10-15; every position hovered in Reason (fold arrow, NOTE light, instrument dropdown, filter type menu: no tooltip) |
| NN-XT Advanced Sampler | NNXT | nn-xt_front_labeled.png | nn-xt_back_labeled.png | nn-xt.json | main panel + back mapped 2026-10-15; every position hovered in Reason; NN-XT Remote Editor (folded sample editor) NOT mapped |
| ID8 Instrument Device | ID8 | id8_front_labeled.png | id8_back_labeled.png | id8.json | mapped 2026-10-15; every position hovered in Reason (category/parameter displays, sound list, tape, back power switch: no tooltip). Remote items Category Name, Preset, Sound, Sound Name, Select Next/Previous Preset/Sound have no proven panel control |
| BV512 Digital Vocoder | BV51 | bv512_front_labeled.png | bv512_back_labeled.png | bv512.json | mapped 2026-10-15; every position hovered in Reason (fold arrows, meters, display, small light, back icons: no tooltip). No Scope block in our remotemap, so no knob slots/CC; names from remote-vocab.json. Only 16 of the 32 Remote band levels are on the panel |
| Rytmik Drum Machine | RYTM | rytmik_front_labeled.png | rytmik_back_labeled.png | rytmik.json | mapped 2026-10-15 (main panel with KICK selected + back); every position hovered in Reason (sample readouts, waveform/filter displays, faders, pads: no tooltip). No Remote map for Rytmik: no slots/CC. Other drums' sample section views not mapped separately |
| MIDI Out Device | MIDO | midi-out_front_labeled.png | midi-out_back_labeled.png | midi-out.json | mapped 2026-10-15; every position hovered in Reason (wheel-side lights, arrows, device menu, tape: no tooltip). No Remote map: no slots/CC. Device menu not opened |
| Elements DS-LFO (AirRaid) | DSLF | elements-ds-lfo_front_labeled.png | elements-ds-lfo_back_labeled.png | elements-ds-lfo.json | mapped 2026-10-15 (AirRaid Rack Extension, no Remote map); every position hovered in Reason (fold arrow, shape arrows, LFO 2 SYNC/MODE: no tooltip) |
| Morfin XF Crossfader (Groovy Melon) | MORF | morfin-xf_front_labeled.png | morfin-xf_back_labeled.png | morfin-xf.json | mapped 2026-10-15 (Groovy Melon Rack Extension, no Remote map); every position hovered in Reason (fold arrow: no tooltip). Fade-type light ring not mapped separately |
| A/B 12 Audio Out Switch (pongasoft) | AB12 | ab12-audio-out_front_labeled.png | ab12-audio-out_back_labeled.png | ab12-audio-out.json | mapped 2026-10-15 (pongasoft Rack Extension, no Remote map); front: every knob hovered, buttons/displays/A-B/lights no tooltip. Back: A1/B1 gate jacks hovered, other gate jacks by row pattern (marked) |
| A/B Audio & CV Switch (pongasoft) | ABSW | ab-switch_front_labeled.png | ab-switch_back_labeled.png | ab-switch.json | mapped 2026-10-15 (pongasoft RE, no Remote map); back jacks all hovered; front knob/light tooltips partly ambiguous (marked) |
| CVA-7 CV Analyzer (pongasoft) | CVA7 | cva-7_front_labeled.png | cva-7_back_labeled.png | cva-7.json | mapped 2026-10-15 (pongasoft RE, no Remote map); front all hovered; back: CV In/trim/aux outs hovered, CV Out slider/jack 1-4 by row pattern (marked) |
| RE 181 Mid/Side Audio Converter | RE18 | re181-mid-side_front_labeled.png | re181-mid-side_back_labeled.png | re181-mid-side.json | mapped 2026-10-15 (Red Rock Sound RE, no Remote map); back jacks all hovered; front: only the two LISTEN buttons have tooltips, rest are meters/lights |
| Select CV Switch (Robotic Bean) | SELC | select-cv-switch_front_labeled.png | select-cv-switch_back_labeled.png | select-cv-switch.json | mapped 2026-10-15 (Robotic Bean RE, no Remote map); back: all named by tooltip (jacks 3-7 by pattern, marked); front buttons/displays have no tooltips |
| RPSpec Spectrogram (Rob Papen) | RPSP | rpspec_front_labeled.png | rpspec_back_labeled.png | rpspec.json | mapped 2026-10-15 (Rob Papen RE, no Remote map); 4 front controls have tooltips; view icons/mode/readouts have none and were not clicked; back jacks cabled (own names not read) |
| Elements Splitter (AirRaid) | SPLT | elements-splitter_front_labeled.png | elements-splitter_back_labeled.png | elements-splitter.json | mapped 2026-10-15 (AirRaid RE 'Elements Splitter 2', no Remote map); nearly all hovered; a few On/M/S buttons gave no tooltip (marked); a few CV jacks by neighbour pattern (marked) |
| kHs Chorus (kiloHearts) | KHSC | khs-chorus_front_labeled.png | khs-chorus_back_labeled.png | khs-chorus.json | mapped 2026-10-15 (kiloHearts RE, no Remote map); every position hovered in Reason (tape/logo: no tooltip) |
| Efektor Silencer Noise Gate (Kuassa) | SILN | efektor-silencer_front_labeled.png | efektor-silencer_back_labeled.png | efektor-silencer.json | mapped 2026-10-15 (Kuassa RE, no Remote map); front all hovered; back audio jacks hovered, 4 small jacks near INPUT/OUTPUT labels had no tooltip and are not identified |

## Scream 4 — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SCR4-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 16 / CC 45 | voice/MIDI or click | tooltip "Enabled: On" |
| SCR4-F-D01 | (LED column) | Input level meter | Input Peak Meter | — | display/Remote item, not mapped | no tooltip (display); position checked by eye |
| SCR4-F-D02 | EASYFUZZ tape | Device name tape (shows this device's name) | Device Name | — | display/Remote item, not mapped | tooltip "EasyFuzz" (device name) |
| SCR4-F-B02 | (triangle) | Fold/unfold device | — | — | click only | no tooltip; clicked = device folded, clicked again (new spot when folded) = unfolded |
| SCR4-F-D03 | EasyFuzz | Patch name display | Patch Name | — | display/Remote item, not mapped | tooltip "EasyFuzz" (patch name) |
| SCR4-F-B03 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| SCR4-F-B09 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| SCR4-F-B04 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| SCR4-F-B05 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| SCR4-F-B06 | DAMAGE | Damage section on/off | Damage On/Off | 14 / CC 43 | voice/MIDI or click | tooltip "Damage On/Off" |
| SCR4-F-K01 | DAMAGE CONTROL | Amount of distortion | Damage Control | 1 / CC 30 | voice/MIDI or click | tooltip "Damage Control: 70" |
| SCR4-F-K02 | (type selector) | Picks 1 of 10 damage types | Damage Type | 2 / CC 31 | voice/MIDI or click | tooltip "Damage Type" |
| SCR4-F-D04 | OVERDRIVE...SCREAM | Damage type list with lights (shows P1/P2 meaning) | — | — | click only | no tooltip (display); position checked by eye |
| SCR4-F-K03 | P1 | Parameter 1 (meaning depends on type) | Parameter 1 | 3 / CC 32 | voice/MIDI or click | tooltip "Parameter 1: 52" |
| SCR4-F-K04 | P2 | Parameter 2 (meaning depends on type) | Parameter 2 | 4 / CC 33 | voice/MIDI or click | tooltip "Parameter 2: 28" |
| SCR4-F-B07 | CUT | Cut EQ on/off | Cut On/Off | 15 / CC 44 | voice/MIDI or click | tooltip "Cut On/Off" |
| SCR4-F-S01 | LO | Cut EQ low slider | Cut Lo | 5 / CC 34 | voice/MIDI or click | tooltip "Cut Lo: 10" (on the handle only) |
| SCR4-F-S02 | MID | Cut EQ mid slider | Cut Mid | 6 / CC 35 | voice/MIDI or click | tooltip "Cut Mid: -11" (on the handle only) |
| SCR4-F-S03 | HI | Cut EQ high slider | Cut Hi | 7 / CC 36 | voice/MIDI or click | tooltip "Cut Hi: 11" (on the handle only) |
| SCR4-F-B08 | BODY | Body section on/off | Body On/Off | 9 / CC 38 | voice/MIDI or click | tooltip "Body On/Off" |
| SCR4-F-K05 | RESO | Body resonance | Body Resonance | 12 / CC 41 | voice/MIDI or click | tooltip "Body Resonance: 2" |
| SCR4-F-K06 | SCALE | Body size (clockwise = smaller) | Body Scale | 11 / CC 40 | voice/MIDI or click | tooltip "Body Scale: 62" |
| SCR4-F-K07 | AUTO | How much the input level moves Body Scale (envelope follower) | Body Auto | 13 / CC 42 | voice/MIDI or click | tooltip "Body Auto: 0" |
| SCR4-F-K08 | TYPE | Body type A-E | Body Type | 10 / CC 39 | voice/MIDI or click | tooltip "Body Type" |
| SCR4-F-K09 | MASTER | Output volume | Master Level | 8 / CC 37 | voice/MIDI or click | tooltip "Master Level: 85" |

## Scream 4 — back
| Code | On panel | What it is | Reason name | How | Checked |
|---|---|---|---|---|---|
| SCR4-B-J01 | Damage Control (CV in) | CV input | Damage Control CV Input | cable: right-click jack > device > jack name | tooltip "Damage Control CV Input" |
| SCR4-B-K01 | (trim) | Amount knob for J01 | Damage Control CV Input | drag (trim/amount for its CV input); no Remote item | tooltip "Damage Control CV Input: 127" |
| SCR4-B-J02 | P1 (CV in) | CV input | Parameter 1 CV Input | cable: right-click jack > device > jack name | tooltip "Parameter 1 CV Input" |
| SCR4-B-K02 | (trim) | Amount knob for J02 | Parameter 1 CV Input | drag (trim/amount for its CV input); no Remote item | tooltip "Parameter 1 CV Input: 127" |
| SCR4-B-J03 | P2 (CV in) | CV input | Parameter 2 CV Input | cable: right-click jack > device > jack name | tooltip "Parameter 2 CV Input" |
| SCR4-B-K03 | (trim) | Amount knob for J03 | Parameter 2 CV Input | drag (trim/amount for its CV input); no Remote item | tooltip "Parameter 2 CV Input: 127" |
| SCR4-B-J04 | Scale (CV in) | CV input | Body Scale CV Input | cable: right-click jack > device > jack name | tooltip "Body Scale CV Input" |
| SCR4-B-K04 | (trim) | Amount knob for J04 | Body Scale CV Input | drag (trim/amount for its CV input); no Remote item | tooltip "Body Scale CV Input: 127" |
| SCR4-B-J05 | Auto CV Output | CV output from the Body envelope follower (follows input level) | Body Auto CV Output | cable: right-click jack > device > jack name | tooltip "Body Auto CV Output"; also a test cable made by map position to Room (RV7000) Decay CV In, confirmed, then disconnected |
| SCR4-B-J06 | Input L | Audio input left | Left Input | cable: right-click jack > device > jack name | tooltip "Connected to MatrixBass2: Out" (cabled); name "Left Input" from cable menu |
| SCR4-B-J07 | Input R | Audio input right | Right Input | cable: right-click jack > device > jack name | tooltip "Right Input" |
| SCR4-B-J08 | Output L | Audio output left | Left Output | cable: right-click jack > device > jack name | tooltip "Connected to side chain: Left" (cabled); name "Left Output" from cable menu |
| SCR4-B-J09 | Output R | Audio output right | Right Output | cable: right-click jack > device > jack name | tooltip "Right Output" |

## The Echo — front
| Code | On panel | What it does | Reason name | Knob slot / CC | Checked |
|---|---|---|---|---|---|
| ECHO-F-B02 | Bypass/On/Off | 3-way device switch | Enabled | 9 / CC 38 | tooltip "Enabled: On" |
| ECHO-F-B01 | (triangle) | Fold/unfold device | — | — | no tooltip; clicked = folded, clicked folded strip's triangle = unfolded |
| ECHO-F-D02 | Input | Input level meter (3 LEDs: green, yellow, red = clipping) | Input Peak Meter | — | tooltip "Master" (twice). Not proof of the name "Input Peak Meter"; position is the INPUT meter by eye |
| ECHO-F-D03 | WARM ECHO tape | Device name tape (shows this device's name) | Device Name | — | tooltip "Warm Echo" |
| ECHO-F-D01 | Warm Echo | Patch name display | Patch Name | — | tooltip "Warm Echo" |
| ECHO-F-B03 | (up arrow) | Load previous patch | Select Previous Patch | — | tooltip "Select previous patch" |
| ECHO-F-B04 | (down arrow) | Load next patch | Select Next Patch | — | tooltip "Select next patch" |
| ECHO-F-B05 | (folder) | Open patch browser | — | — | tooltip "Browse patch" |
| ECHO-F-B06 | (disk) | Save patch | — | — | tooltip "Save patch" |
| ECHO-F-B07 | NORMAL/TRIGGERED/ROLL | Mode switch, 3 positions: Normal, Triggered, Roll | Input Mode | 15 / CC 44 | tooltip "Input Mode: Normal" |
| ECHO-F-B09 | TRIG | Trigger button; opens the input gate while held (Triggered mode only) | Trig | 25 / CC 54 | tooltip "Trig" |
| ECHO-F-S01 | 0 ... ROLL | Roll slider; slide 0 to full Roll for stutter/repeat (Roll mode only) | Roll Enabled | 23 / CC 52 | tooltip "Roll Enabled: 0%" |
| ECHO-F-K01 | TIME | Delay time (1-1000 ms, or note values with Sync) | Delay Time | 1 / CC 30 | tooltip "Delay Time: 3/16" |
| ECHO-F-K02 | OFFSET R (Delay) | Right channel delay time offset | Right Ch Time Offset | 22 / CC 51 | tooltip "Right Ch Time Offset: 0" |
| ECHO-F-B10 | KEEP PITCH | Keep pitch fixed when delay time changes | Keep Pitch | 16 / CC 45 | tooltip "Keep Pitch" |
| ECHO-F-B11 | SYNC | Tempo sync for Time and Offset R | Sync | 24 / CC 53 | tooltip "Sync" |
| ECHO-F-B14 | PING-PONG | Ping-pong on/off (repeats alternate left and right) | Ping-Pong Mode | 19 / CC 48 | tooltip "Ping-Pong Mode" |
| ECHO-F-K09 | PAN | Ping-pong stereo width and first-repeat side | Ping-Pong Pan | 20 / CC 49 | tooltip "Ping-Pong Pan: -100" |
| ECHO-F-K03 | FEEDBACK | Amount of echo fed back (number of repeats) | Feedback | 11 / CC 40 | tooltip "Feedback: 22%" |
| ECHO-F-K04 | OFFSET R (Feedback) | Right channel feedback offset (bipolar) | Right Ch Feedback Offset | 21 / CC 50 | tooltip "Right Ch Feedback Offset: 0%" |
| ECHO-F-B12 | DIFFUSION (button) | Diffusion on/off | Diffuse On | 3 / CC 32 | tooltip "Diffuse On" |
| ECHO-F-K10 | SPREAD | Diffusion spread (how wide the smear is) | Diffuse Spread | 4 / CC 33 | tooltip "Diffusion Spread: 50%" |
| ECHO-F-K11 | AMOUNT (Diffusion) | Diffusion amount | Diffuse Amount | 2 / CC 31 | tooltip "Diffusion Amount: 50%" |
| ECHO-F-K05 | DRIVE | Amount of the selected limiter/distortion | Drive Amount | 5 / CC 34 | tooltip "Drive Amount: 32%" |
| ECHO-F-B08 | TYPE (LIM/OVDR/DIST/TUBE) | Color type switch, 4 positions | Drive Type | 6 / CC 35 | tooltip "Drive Type: Tube" |
| ECHO-F-B13 | FILTER (button) | Filter on/off | Filter On | 13 / CC 42 | tooltip "Filter On" |
| ECHO-F-K12 | FREQ | Filter frequency | Filter Frequency | 12 / CC 41 | tooltip "Filter Frequency: 651.3 Hz" |
| ECHO-F-K13 | RESO | Filter resonance | Filter Resonance | 14 / CC 43 | tooltip "Filter Resonance: 22%" |
| ECHO-F-K06 | ENV | Pitch bend of repeats, down or up (bipolar) | Envelope | 10 / CC 39 | tooltip "Envelope: 0%" |
| ECHO-F-K07 | WOBBLE | Random tape-speed wobble | Wobble | 26 / CC 55 | tooltip "Wobble: 0%" |
| ECHO-F-K14 | RATE | LFO speed | LFO Rate | 18 / CC 47 | tooltip "LFO Rate: 0.46 Hz" |
| ECHO-F-K15 | AMOUNT (LFO) | LFO amount | LFO Amount | 17 / CC 46 | tooltip "LFO Amount: 0%" |
| ECHO-F-K08 | DRY/WET | Balance between dry and echo signal | Dry/Wet Balance | 7 / CC 36 | tooltip "Dry/Wet Balance: 100%" |
| ECHO-F-K16 | DUCKING | Lowers echo while input is playing | Ducking | 8 / CC 37 | tooltip "Ducking: 0%" |

## The Echo — back
| Code | On panel | What it is | Reason name | Checked |
|---|---|---|---|---|
| ECHO-B-J01 | Trig (CV in) | Gate input for the Trig function | Trig CV In | tooltip "Trig CV In" |
| ECHO-B-J02 | Roll (CV in) | CV input for Roll amount | Roll CV In | tooltip "Roll CV In" |
| ECHO-B-J03 | Delay Time (CV in) | CV input for delay time | Delay Time CV In | tooltip "Delay Time CV In" |
| ECHO-B-J04 | Filter Freq (CV in) | CV input for filter frequency | Filter Frequency CV In | tooltip "Filter Frequency CV In" |
| ECHO-B-K01 | (trim) | Amount knob for Delay Time CV | Delay Time CV Modulation Amount | tooltip "Delay Time CV Modulation Amount: 100" |
| ECHO-B-K02 | (trim) | Amount knob for Filter Freq CV | Filter Frequency CV Modulation Amount | tooltip "Filter Frequency CV Modulation Amoun[t] (cut off)" |
| ECHO-B-J05 | Breakout Output L | Feedback loop send, left | Feedback Loop Left Output | tooltip "Feedback Loop Left Output" |
| ECHO-B-J06 | Breakout Output R | Feedback loop send, right | Feedback Loop Right Output | tooltip "Feedback Loop Right Output" |
| ECHO-B-J07 | Main Input L | Audio input left | Left Input | tooltip "Connected to Mix Channel: To Insert FX"; name "Left Input" read from the cable menu |
| ECHO-B-J08 | Main Input R | Audio input right | Right Input | tooltip "Connected to Mix Channel: To Insert FX"; name "Right Input" read from the cable menu |
| ECHO-B-J09 | Breakout Input L | Feedback loop return, left | Feedback Loop Left Input | tooltip "Feedback Loop Left Input" |
| ECHO-B-J10 | Breakout Input R | Feedback loop return, right | Feedback Loop Right Input | tooltip "Feedback Loop Right Input" |
| ECHO-B-J11 | Main Output L | Audio output left | Left Output | tooltip "Connected to Mix Channel: From Insert"; name "Left Output" read from the cable menu |
| ECHO-B-J12 | Main Output R | Audio output right | Right Output | tooltip "Connected to Mix Channel: From Insert"; name "Right Output" read from the cable menu |

Notes: hover shows "Diffusion Spread/Amount" but the Remote names are "Diffuse Spread/Amount" (use the Remote name to control). The INPUT meter's hover says "Master". Labels were drafted by a Sonnet helper; all 48 positions confirmed in Reason by Claude.

## CF-101 Chorus/Flanger — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| CF101-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 2 / CC 31 | voice/MIDI or click | hover: 'Enabled: On' |
| CF101-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| CF101-F-D01 | CHORUS/FLAN... tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Chorus/Flanger 1' (device name tape) |
| CF101-F-K01 | DELAY | Delay time: short = flanger, medium = chorus | Delay | 1 / CC 30 | voice/MIDI or click | hover: 'Delay: 40' |
| CF101-F-K02 | FEEDBACK | Feedback amount, centre = off; left/right = two flavours of resonant flanging | Feedback | 3 / CC 32 | voice/MIDI or click | hover: 'Feedback: 0' |
| CF101-F-K03 | RATE | LFO speed | Rate | 6 / CC 35 | voice/MIDI or click | hover: 'Rate: 40' |
| CF101-F-B02 | SYNC | LFO tempo sync on/off | LFO Sync Enable | 4 / CC 33 | voice/MIDI or click | hover: 'LFO Sync Enable' |
| CF101-F-K04 | MOD AMOUNT | LFO modulation depth (0 = frozen) | Modulation Amount | 5 / CC 34 | voice/MIDI or click | hover: 'Modulation Amount: 64' |
| CF101-F-B03 | SEND MODE | Send mode: outputs only the wet signal | Send/Insert Mode | 7 / CC 36 | voice/MIDI or click | hover: 'Send/Insert Mode' |

## CF-101 Chorus/Flanger — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| CF101-B-J01 | Delay (CV in) | CV input for Delay | Delay CV | — | cable: right-click jack > device > jack name | hover: 'Delay CV' |
| CF101-B-J02 | Rate (CV in) | CV input for Rate | Rate CV | — | cable: right-click jack > device > jack name | hover: 'Rate CV' |
| CF101-B-K01 | (trim) | Amount knob for Delay CV | — | — | click/drag only (no Remote item) | hover: 'Delay CV: 127' |
| CF101-B-K02 | (trim) | Amount knob for Rate CV | — | — | click/drag only (no Remote item) | hover: 'Rate CV: 127' |
| CF101-B-D01 | CHORUS/FLAN... tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'Chorus/Flanger 1' (device name tape) |
| CF101-B-J03 | Left (Input) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Mix Channel: To Insert FX Left' |
| CF101-B-J04 | Right (Input) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Mix Channel: To Insert FX Right' |
| CF101-B-J05 | Left (Output) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Compressor 1: Left' |
| CF101-B-J06 | Right (Output) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Compressor 1: Right' |

## COMP-01 Compressor — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| COMP01-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 2 / CC 31 | voice/MIDI or click | hover: 'Enabled: On' |
| COMP01-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| COMP01-F-D01 | COMPRESSOR 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Compressor 1' (device name tape) |
| COMP01-F-K01 | RATIO | Compression ratio, 1:1 to 16:1 | Ratio | 4 / CC 33 | voice/MIDI or click | hover: 'Ratio: 64' |
| COMP01-F-K02 | THRESHOLD | Level above which compression starts | Threshold | 6 / CC 35 | voice/MIDI or click | hover: 'Threshold: 40' |
| COMP01-F-K03 | ATTACK | How fast compression kicks in | Attack | 1 / CC 30 | voice/MIDI or click | hover: 'Attack: 40' |
| COMP01-F-K04 | RELEASE | How fast compression lets go | Release | 5 / CC 34 | voice/MIDI or click | hover: 'Release: 64' |
| COMP01-F-D03 | GAIN (LED row) | Gain reduction meter, -36 to +36 dB (display) | Gain | 3 / CC 32 | voice/MIDI or click | no tooltip; checked by eye: gain-reduction LED meter (no hover tooltip) |

## COMP-01 Compressor — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| COMP01-B-D01 | COMPRESSOR 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'Compressor 1' (device name tape) |
| COMP01-B-J01 | L (In) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Chorus/Flanger 1: Left' |
| COMP01-B-J02 | R (In) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Chorus/Flanger 1: Right' |
| COMP01-B-J03 | L (Out) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Dist 1: Left' |
| COMP01-B-J04 | R (Out) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Dist 1: Right' |

## D-11 Foldback Distortion — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| D11-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 2 / CC 31 | voice/MIDI or click | hover: 'Enabled: On' |
| D11-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| D11-F-D01 | DIST 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Dist 1' (device name tape) |
| D11-F-K01 | AMOUNT | Distortion amount | Amount | 1 / CC 30 | voice/MIDI or click | hover: 'Amount: 20' |
| D11-F-K02 | FOLDBACK | Foldback threshold: how far the wave folds back | Foldback | 3 / CC 32 | voice/MIDI or click | hover: 'Foldback: 34' |

## D-11 Foldback Distortion — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| D11-B-D01 | DIST 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | no tooltip; checked by eye: tape reads DIST 1 |
| D11-B-K01 | Amount CV (trim) | Amount knob for Amount CV | — | — | click/drag only (no Remote item) | hover: 'Amount CV: 127' |
| D11-B-J01 | Amount CV (jack) | CV input for Amount | Amount CV | — | cable: right-click jack > device > jack name | hover: 'Amount CV' (empty jack) |
| D11-B-J02 | L (In) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Compressor 1: Left' |
| D11-B-J03 | R (In) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Compressor 1: Right' |
| D11-B-J04 | L (Out) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Delay 1: Left' |
| D11-B-J05 | R (Out) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Delay 1: Right' |

## DDL-1 Digital Delay Line — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| DDL1-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 4 / CC 33 | voice/MIDI or click | hover: 'Enabled: On' |
| DDL1-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| DDL1-F-D01 | DELAY 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Delay 1' (device name tape) |
| DDL1-F-D03 | (digit display) | Delay time readout (shows 'DelayTime (steps)' in Reason when UNIT = STEPS) | DelayTime (steps) | 2 / CC 31 | Remote: knob slot 2 (steps mode); same display as D04 | hover on digit display: 'DelayTime (steps)' while UNIT=STEPS; after clicking UNIT to MS it showed 'DelayTime (ms)'; UNIT clicked back to STEPS (undone) |
| DDL1-F-D04 | (digit display, MS mode) | Same digit display as D03, when UNIT = MS (Reason shows 'DelayTime (ms)') | DelayTime (ms) | 1 / CC 30 | Remote: knob slot 1 (ms mode); no separate control, same spot as D03 (no box drawn) | hover with UNIT=MS: 'DelayTime (ms)' (UNIT set back to STEPS afterwards) |
| DDL1-F-B02 | (up/down arrows) | Change the delay time | — | — | click only | no tooltip; checked by eye: up/down arrows (no tooltip on either arrow) |
| DDL1-F-B03 | MS / STEPS lights + UNIT | UNIT button: switches between ms and steps (lights show which) | Unit | 8 / CC 37 | voice/MIDI or click | hover UNIT button: 'Unit'; MS/STEPS lights have no tooltip |
| DDL1-F-B04 | 1/16 / 1/8T lights + STEP LENGTH | STEP LENGTH button: step size 1/16 or 1/8 triplet | Step Length | 7 / CC 36 | voice/MIDI or click | hover STEP LENGTH button: 'Step Length'; 1/16, 1/8T lights have no tooltip |
| DDL1-F-K01 | FEEDBACK | Amount of delayed signal fed back | Feedback | 5 / CC 34 | voice/MIDI or click | hover: 'Feedback: 40' |
| DDL1-F-K02 | PAN | Pan of the delayed signal, L to R | Pan | 6 / CC 35 | voice/MIDI or click | hover: 'Pan: 0' |
| DDL1-F-K03 | DRY/WET | Balance dry and delayed signal | Dry/Wet Balance | 3 / CC 32 | voice/MIDI or click | hover: 'Dry/Wet Balance: 127' |

## DDL-1 Digital Delay Line — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| DDL1-B-J01 | Pan (CV in) | CV input for Pan | Pan CV | — | cable: right-click jack > device > jack name | hover: 'Pan CV' |
| DDL1-B-J02 | Feedback (CV in) | CV input for Feedback | Feedback CV | — | cable: right-click jack > device > jack name | hover: 'Feedback CV' |
| DDL1-B-K01 | (trim) | Amount knob for Pan CV | — | — | click/drag only (no Remote item) | hover: 'Pan CV: 127' |
| DDL1-B-K02 | (trim) | Amount knob for Feedback CV | — | — | click/drag only (no Remote item) | hover: 'Feedback CV: 127' |
| DDL1-B-D01 | DELAY 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'Delay 1' (device name tape) |
| DDL1-B-J03 | Left (Input) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Dist 1: Left' |
| DDL1-B-J04 | Right (Input) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Dist 1: Right' |
| DDL1-B-J05 | Left (Output) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Filter 1: Left' |
| DDL1-B-J06 | Right (Output) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Filter 1: Right' |

## ECF-42 Envelope Controlled Filter — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| ECF42-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 3 / CC 32 | voice/MIDI or click | hover: 'Enabled: On' |
| ECF42-F-D03 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column (peak meter) left side |
| ECF42-F-D01 | FILTER 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Filter 1' (device name tape) |
| ECF42-F-D02 | GATE (light) | Gate light: lights when the envelope is triggered (display) | Trigger | 10 / CC 39 | read-only light (no tooltip in Reason) | no tooltip; checked by eye: GATE light (no hover tooltip) |
| ECF42-F-K01 | FREQ | Filter frequency | Frequency | 5 / CC 34 | voice/MIDI or click | hover: 'Frequency: 64' |
| ECF42-F-K02 | RES | Filter resonance | Resonance | 8 / CC 37 | voice/MIDI or click | hover: 'Resonance: 0' |
| ECF42-F-K03 | ENV.AMT | How far the envelope moves the filter | Env Amount | 4 / CC 33 | voice/MIDI or click | hover: 'Env Amount: 32' |
| ECF42-F-K04 | VEL. | How much note velocity opens the filter | Velocity | 11 / CC 40 | voice/MIDI or click | hover: 'Velocity: 0' |
| ECF42-F-B02 | BP12/LP12/LP24 lights + MODE | MODE button: cycles filter type BP 12, LP 12, LP 24 (lights show which) | Mode | 6 / CC 35 | voice/MIDI or click | hover MODE button: 'Mode'; BP12/LP12/LP24 lights have no tooltip |
| ECF42-F-K05 | A (Envelope) | Envelope attack | Attack | 1 / CC 30 | voice/MIDI or click | hover: 'Attack: 0' |
| ECF42-F-K06 | D (Envelope) | Envelope decay | Decay | 2 / CC 31 | voice/MIDI or click | hover: 'Decay: 64' |
| ECF42-F-K07 | S (Envelope) | Envelope sustain | Sustain | 9 / CC 38 | voice/MIDI or click | hover: 'Sustain: 0' |
| ECF42-F-K08 | R (Envelope) | Envelope release | Release | 7 / CC 36 | voice/MIDI or click | hover: 'Release: 64' |

## ECF-42 Envelope Controlled Filter — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| ECF42-B-D01 | FILTER 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'Filter 1' (device name tape) |
| ECF42-B-K01 | (trim) | Amount knob for Freq CV | — | — | click/drag only (no Remote item) | hover: 'Freq CV: 127' |
| ECF42-B-J01 | Freq (CV in) | CV input for Freq | Freq CV | — | cable: right-click jack > device > jack name | hover: 'Freq CV' |
| ECF42-B-K02 | (trim) | Amount knob for Decay CV | — | — | click/drag only (no Remote item) | hover: 'Decay CV: 127' |
| ECF42-B-J02 | Decay (CV in) | CV input for Decay | Decay CV | — | cable: right-click jack > device > jack name | hover: 'Decay CV' |
| ECF42-B-K03 | (trim) | Amount knob for Res CV | — | — | click/drag only (no Remote item) | hover: 'Resonance CV: 127' |
| ECF42-B-J03 | Res (CV in) | CV input for Res | Resonance CV | — | cable: right-click jack > device > jack name | hover: 'Resonance CV' |
| ECF42-B-J04 | Env. Gate (CV in) | Gate input for the envelope | Env Gate | — | cable: right-click jack > device > jack name | hover: 'Env Gate' |
| ECF42-B-J05 | Left (In) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Delay 1: Left' |
| ECF42-B-J06 | Right (In) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Delay 1: Right' |
| ECF42-B-J07 | Left (Out) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to EQ 1: Left' |
| ECF42-B-J08 | Right (Out) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to EQ 1: Right' |

## PEQ-2 Two Band Parametric EQ — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PEQ2-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 1 / CC 30 | voice/MIDI or click | hover: 'Enabled: On' |
| PEQ2-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| PEQ2-F-D01 | EQ 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'EQ 1' (device name tape) |
| PEQ2-F-D03 | (EQ display) | Frequency response graph, 31 Hz to 16k, +18 to -18 dB (display) | — | — | click only | no tooltip; checked by eye: EQ curve display (no hover tooltip) |
| PEQ2-F-K01 | A FREQ | Band A frequency | Filter A Freq | 2 / CC 31 | voice/MIDI or click | hover: 'Filter A Freq: 64' |
| PEQ2-F-K02 | A Q | Band A width (Q) | Filter A Q | 4 / CC 33 | voice/MIDI or click | hover: 'Filter A Q: 64' |
| PEQ2-F-K03 | A GAIN | Band A boost/cut | Filter A Gain | 3 / CC 32 | voice/MIDI or click | hover: 'Filter A Gain: 0' |
| PEQ2-F-K04 | B FREQ | Band B frequency | Filter B Freq | 5 / CC 34 | voice/MIDI or click | hover: 'Filter B Freq: 64' |
| PEQ2-F-K05 | B Q | Band B width (Q) | Filter B Q | 8 / CC 37 | voice/MIDI or click | hover: 'Filter B Q: 64' |
| PEQ2-F-K06 | B GAIN | Band B boost/cut | Filter B Gain | 6 / CC 35 | voice/MIDI or click | hover: 'Filter B Gain: 0' |
| PEQ2-F-B02 | B (button) | Band B on/off (light shows on) | Filter B On/Off | 7 / CC 36 | voice/MIDI or click | hover: 'Filter B On/Off' |

## PEQ-2 Two Band Parametric EQ — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PEQ2-B-J01 | Freq 1 (CV in) | CV input for Freq 1 | Filter 1 Freq CV | — | cable: right-click jack > device > jack name | hover: 'Filter 1 Freq CV' |
| PEQ2-B-J02 | Freq 2 (CV in) | CV input for Freq 2 | Filter 2 Freq CV | — | cable: right-click jack > device > jack name | hover: 'Filter 2 Freq CV' |
| PEQ2-B-K01 | (trim) | Amount knob for Freq 1 CV | — | — | click/drag only (no Remote item) | hover: 'Filter 1 Freq CV: 127' |
| PEQ2-B-K02 | (trim) | Amount knob for Freq 2 CV | — | — | click/drag only (no Remote item) | hover: 'Filter 2 Freq CV: 127' |
| PEQ2-B-D01 | EQ 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'EQ 1' (device name tape) |
| PEQ2-B-J03 | Left (In) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Filter 1: Left' |
| PEQ2-B-J04 | Right (In) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Filter 1: Right' |
| PEQ2-B-J05 | Left (Out) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Phaser 1: Left' |
| PEQ2-B-J06 | Right (Out) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Phaser 1: Right' |

## PH-90 Phaser — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PH90-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 1 / CC 30 | voice/MIDI or click | hover: 'Enabled: On' |
| PH90-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| PH90-F-D01 | PHASER 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Phaser 1' (device name tape) |
| PH90-F-K01 | FREQ | Phaser frequency | Frequency | 3 / CC 32 | voice/MIDI or click | hover: 'Frequency: 58' |
| PH90-F-K02 | SPLIT | Split of the phase stages | Split | 7 / CC 36 | voice/MIDI or click | hover: 'Split: 64' |
| PH90-F-K03 | WIDTH | Stereo width | Width | 8 / CC 37 | voice/MIDI or click | hover: 'Width: 100' |
| PH90-F-K04 | RATE | LFO speed | Rate | 6 / CC 35 | voice/MIDI or click | hover: 'Rate: 32' |
| PH90-F-B02 | SYNC | LFO tempo sync on/off (light shows on) | LFO Sync Enable | 5 / CC 34 | voice/MIDI or click | hover: 'LFO Sync Enable' |
| PH90-F-K05 | F. MOD | How much the LFO moves the frequency | Frequency Modulation | 4 / CC 33 | voice/MIDI or click | hover: 'Frequency Modulation: 70' |
| PH90-F-K06 | FEEDBACK | Feedback amount | Feedback | 2 / CC 31 | voice/MIDI or click | hover: 'Feedback: 100' |


=== END OF PART ===
