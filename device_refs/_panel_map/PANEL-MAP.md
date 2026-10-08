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

## PH-90 Phaser — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PH90-B-D01 | PHASER 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | no tooltip; checked by eye: tape reads PHASER 1 |
| PH90-B-K01 | (trim) | Amount knob for Freq CV | — | — | click/drag only (no Remote item) | hover: 'Freq CV: 127' |
| PH90-B-J01 | Freq (CV in) | CV input for Freq | Freq CV | — | cable: right-click jack > device > jack name | hover: 'Freq CV' |
| PH90-B-K02 | (trim) | Amount knob for Rate CV | — | — | click/drag only (no Remote item) | hover: 'Rate CV: 127' |
| PH90-B-J02 | Rate (CV in) | CV input for Rate | Rate CV | — | cable: right-click jack > device > jack name | hover: 'Rate CV' |
| PH90-B-J03 | Left (In) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to EQ 1: Left' |
| PH90-B-J04 | Right (In) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to EQ 1: Right' |
| PH90-B-J05 | Left (Out) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Reverb 1: Left' |
| PH90-B-J06 | Right (Out) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Reverb 1: Right' |

## RV-7 Digital Reverb — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RV7-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 5 / CC 34 | voice/MIDI or click | hover: 'Enabled: On' |
| RV7-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| RV7-F-D01 | REVERB 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Reverb 1' (device name tape) |
| RV7-F-D03 | (algorithm display) | Shows the reverb type (Hall, etc.) | — | — | click only | hover on display: 'Algorithm: 0' (display shows 'Hall') |
| RV7-F-B02 | (up/down arrows) | Step through reverb types | Algorithm | 1 / CC 30 | voice/MIDI or click | no tooltip; checked by eye: up/down arrows (no hover tooltip on either arrow; the display tooltip is 'Algorithm: 0') |
| RV7-F-K01 | SIZE | Room size | Size | 6 / CC 35 | voice/MIDI or click | hover: 'Size: 0' |
| RV7-F-K02 | DECAY | Reverb tail length | Decay | 3 / CC 32 | voice/MIDI or click | hover: 'Decay: 0' |
| RV7-F-K03 | DAMP | High-frequency damping | Damping | 2 / CC 31 | voice/MIDI or click | hover: 'Damping: 40' |
| RV7-F-K04 | DRY/WET | Balance dry and reverb | Dry/Wet | 4 / CC 33 | voice/MIDI or click | hover: 'Dry/Wet: 127' |

## RV-7 Digital Reverb — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RV7-B-J01 | Decay (CV in) | CV input for Decay | Decay CV | — | cable: right-click jack > device > jack name | hover: 'Decay CV' |
| RV7-B-K01 | (trim) | Amount knob for Decay CV | — | — | click/drag only (no Remote item) | hover: 'Decay CV: 127' |
| RV7-B-D01 | REVERB 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'Reverb 1' (device name tape) |
| RV7-B-J02 | Left (In) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Phaser 1: Left' |
| RV7-B-J03 | Right (In) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Phaser 1: Right' |
| RV7-B-J04 | Left (Out) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Unison 1: Left' |
| RV7-B-J05 | Right (Out) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Unison 1: Right' |

## UN-16 Unison — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| UN16-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 3 / CC 32 | voice/MIDI or click | hover: 'Enabled: On' |
| UN16-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| UN16-F-D01 | UNISON 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'Unison 1' (device name tape) |
| UN16-F-B02 | 16/8/4 lights + VOICE COUNT | VOICE COUNT button: cycles 16, 8, 4 voices (lights show which) | Voice Count | 4 / CC 33 | voice/MIDI or click | hover VOICE COUNT button: 'Voice Count'; 16/8/4 lights have no tooltip |
| UN16-F-K01 | DETUNE | Detune amount | Detune | 1 / CC 30 | voice/MIDI or click | hover: 'Detune: 40' |
| UN16-F-K02 | DRY/WET | Balance dry and unison signal | Dry/Wet | 2 / CC 31 | voice/MIDI or click | hover: 'Dry/Wet: 127' |

## UN-16 Unison — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| UN16-B-J01 | Detune (CV in) | CV input for Detune | Detune CV | — | cable: right-click jack > device > jack name | hover: 'Detune CV' |
| UN16-B-K01 | (trim) | Amount knob for Detune CV | — | — | click/drag only (no Remote item) | hover: 'Detune CV: 127' |
| UN16-B-D01 | UNISON 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'Unison 1' (device name tape) |
| UN16-B-J02 | Left (In) | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Reverb 1: Left' |
| UN16-B-J03 | Right (In) | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Reverb 1: Right' |
| UN16-B-J04 | Left (Out) | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to M EQ 1: Left' |
| UN16-B-J05 | Right (Out) | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to M EQ 1: Right' |

## MClass Compressor — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MCMP-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 8 / CC 37 | voice/MIDI or click | hover: 'Enabled: On' |
| MCMP-F-D02 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| MCMP-F-D03 | M COMP 2 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'M Comp 1' (device name tape; this song's instance is named M COMP 1, the picture's M COMP 2) |
| MCMP-F-K01 | INPUT GAIN | Level into the compressor | Input Gain | 4 / CC 33 | voice/MIDI or click | hover: 'Input Gain: 8.6 dB' |
| MCMP-F-K02 | THRESHOLD | Level above which compression starts | Threshold | 1 / CC 30 | voice/MIDI or click | hover: 'Threshold: -7.7 dB' |
| MCMP-F-B03 | SOFT KNEE | Soft knee on/off | Soft Knee | 2 / CC 31 | voice/MIDI or click | hover: 'Soft Knee' |
| MCMP-F-K03 | RATIO | Compression ratio, 1:1 to infinity:1 | Ratio | 3 / CC 32 | voice/MIDI or click | hover: 'Ratio: 44.7:1' |
| MCMP-F-D01 | GAIN (meter) | Gain reduction meter, 0 to -20 dB | Gain Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: gain-reduction meter (no hover tooltip) |
| MCMP-F-B02 | ACTIVE (sidechain) | Sidechain on/off (light shows on) | Sidechain Active | — | display/Remote item, not mapped | no tooltip; checked by eye: sidechain ACTIVE light (no hover tooltip) |
| MCMP-F-B05 | SOLO (sidechain) | Listen to the sidechain signal | Sidechain Solo | — | display/Remote item, not mapped | hover: 'Sidechain Solo' |
| MCMP-F-K04 | ATTACK | How fast compression kicks in | Attack | 5 / CC 34 | voice/MIDI or click | hover: 'Attack: 50 ms' |
| MCMP-F-K05 | RELEASE | How fast compression lets go | Release | 6 / CC 35 | voice/MIDI or click | hover: 'Release: 327 ms' |
| MCMP-F-B04 | ADAPT RELEASE | Adaptive release on/off | Adapt | — | display/Remote item, not mapped | hover ADAPT RELEASE button: 'Adapt' |
| MCMP-F-K06 | OUTPUT GAIN | Level out of the compressor | Output Gain | 7 / CC 36 | voice/MIDI or click | hover: 'Output Gain: 0.0 dB' |

## MClass Compressor — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MCMP-B-D01 | M COMP 2 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'M Comp 1' (device name tape) |
| MCMP-B-J01 | Audio Input L | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to British Drive 3: Main Out L' |
| MCMP-B-J02 | Audio Input R | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to British Drive 3: Main Out R' |
| MCMP-B-J03 | Audio Output L | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Peff 808 A: Input L' |
| MCMP-B-J04 | Audio Output R | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Peff 808 A: Input R' |
| MCMP-B-J05 | Sidechain In L | Sidechain input left | Sidechain Left | — | cable: right-click jack > device > jack name | hover: 'Sidechain Left' |
| MCMP-B-J06 | Sidechain In R | Sidechain input right | Sidechain Right | — | cable: right-click jack > device > jack name | hover: 'Sidechain Right' |
| MCMP-B-J07 | Gain Reduction CV Out | CV output following the gain reduction | Gain Reduction CV | — | cable: right-click jack > device > jack name | hover: 'Gain Reduction CV' |

## MClass Equalizer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MEQ-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 1 / CC 30 | voice/MIDI or click | hover on the bypass switch: 'Enabled: On' (hover ~9 px left of the drawn box centre; the box centre itself showed no tooltip) |
| MEQ-F-D01 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| MEQ-F-D02 | MEQ 1 tape | Device name tape (vertical) | Device Name | — | display/Remote item, not mapped | hover: tooltip 'M EQ 1' (device name tape) |
| MEQ-F-D03 | (EQ display) | Frequency response graph, 39 Hz to 20 kHz, +/-18 dB | — | — | click only | no tooltip; checked by eye: EQ curve display (no hover tooltip) |
| MEQ-F-B02 | LO CUT | Low cut on/off | Low Cut Enable | 6 / CC 35 | voice/MIDI or click | hover: 'Low Cut Enable' |
| MEQ-F-B03 | LO SHELF (button) | Low Shelf on/off | Low Shelf Enable | 7 / CC 36 | voice/MIDI or click | hover: 'Low Shelf Enable' |
| MEQ-F-K01 | LO SHELF FREQ | Low Shelf frequency | Low Shelf Frequency | 8 / CC 37 | voice/MIDI or click | hover: 'Low Shelf Frequency: 134.2 Hz' |
| MEQ-F-K05 | LO SHELF GAIN | Low Shelf boost/cut | Low Shelf Gain | 9 / CC 38 | voice/MIDI or click | hover: 'Low Shelf Gain: 0.0 dB' |
| MEQ-F-K09 | LO SHELF Q | Low Shelf width (Q) | Low Shelf Q | 10 / CC 39 | voice/MIDI or click | hover: 'Low Shelf Q: 0.62' |
| MEQ-F-B04 | PARAM 1 (button) | Parametric 1 on/off | Parametric 1 Enable | 11 / CC 40 | voice/MIDI or click | hover: 'Parametric 1 Enable' |
| MEQ-F-K02 | PARAM 1 FREQ | Parametric 1 frequency | Parametric 1 Frequency | 12 / CC 41 | voice/MIDI or click | hover: 'Parametric 1 Frequency: 883.9 Hz' |
| MEQ-F-K06 | PARAM 1 GAIN | Parametric 1 boost/cut | Parametric 1 Gain | 13 / CC 42 | voice/MIDI or click | hover: 'Parametric 1 Gain: 0.0 dB' |
| MEQ-F-K10 | PARAM 1 Q | Parametric 1 width (Q) | Parametric 1 Q | 14 / CC 43 | voice/MIDI or click | hover: 'Parametric 1 Q: 5.7' |
| MEQ-F-B05 | PARAM 2 (button) | Parametric 2 on/off | Parametric 2 Enable | 15 / CC 44 | voice/MIDI or click | hover: 'Parametric 2 Enable' |
| MEQ-F-K03 | PARAM 2 FREQ | Parametric 2 frequency | Parametric 2 Frequency | 16 / CC 45 | voice/MIDI or click | hover: 'Parametric 2 Frequency: 883.9 Hz' |
| MEQ-F-K07 | PARAM 2 GAIN | Parametric 2 boost/cut | Parametric 2 Gain | 17 / CC 46 | voice/MIDI or click | hover: 'Parametric 2 Gain: 0.0 dB' |
| MEQ-F-K11 | PARAM 2 Q | Parametric 2 width (Q) | Parametric 2 Q | 18 / CC 47 | voice/MIDI or click | hover: 'Parametric 2 Q: 5.7' |
| MEQ-F-B06 | HI SHELF (button) | Hi Shelf on/off | Hi Shelf Enable | 2 / CC 31 | voice/MIDI or click | hover: 'Hi Shelf Enable' |
| MEQ-F-K04 | HI SHELF FREQ | Hi Shelf frequency | Hi Shelf Frequency | 3 / CC 32 | voice/MIDI or click | hover: 'Hi Shelf Frequency: 6.000 kHz' |
| MEQ-F-K08 | HI SHELF GAIN | Hi Shelf boost/cut | Hi Shelf Gain | 4 / CC 33 | voice/MIDI or click | hover: 'Hi Shelf Gain: 0.0 dB' |
| MEQ-F-K12 | HI SHELF Q | Hi Shelf width (Q) | Hi Shelf Q | 5 / CC 34 | voice/MIDI or click | hover: 'Hi Shelf Q: 0.62' |

## MClass Equalizer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MEQ-B-D01 | MEQ 1 tape | Device name tape (back, vertical) | — | — | click/drag only (no Remote item) | hover: tooltip 'M EQ 1' (device name tape) |
| MEQ-B-J01 | Audio Input L | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to Unison 1: Left' |
| MEQ-B-J02 | Audio Input R | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to Unison 1: Right' |
| MEQ-B-J03 | Audio Output L | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to M Maximizer 1: Left' |
| MEQ-B-J04 | Audio Output R | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to M Maximizer 1: Right' |

## MClass Maximizer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MMAX-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 2 / CC 31 | voice/MIDI or click | hover: 'Enabled: On' |
| MMAX-F-D03 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| MMAX-F-D05 | M MAXIMIZER 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'M Maximizer 1' (device name tape) |
| MMAX-F-K01 | INPUT GAIN | Level into the maximizer | Input Gain | 3 / CC 32 | voice/MIDI or click | hover: 'Input Gain: 0.0 dB' |
| MMAX-F-B02 | LIMITER | Limiter on/off | Limiter Enable | 4 / CC 33 | voice/MIDI or click | hover: 'Limiter Enable' |
| MMAX-F-B04 | 4ms LOOK AHEAD | Look ahead on/off | Look Ahead Enable | 5 / CC 34 | voice/MIDI or click | hover: 'Look Ahead Enable' |
| MMAX-F-D01 | GAIN (meter) | Gain reduction meter, 0 to -20 dB | Gain Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: gain-reduction meter (no hover tooltip) |
| MMAX-F-B05 | ATTACK (FAST/MID/SLOW) | Attack speed: 3 buttons, pick one | Attack Speed | 1 / CC 30 | voice/MIDI or click | hover: 'Attack Speed: 4 ms' |
| MMAX-F-B06 | RELEASE (FAST/SLOW/AUTO) | Release speed: 3 buttons, pick one | Release Speed | 9 / CC 38 | voice/MIDI or click | hover: 'Release Speed: 150 ms' |
| MMAX-F-K02 | OUTPUT GAIN | Level out of the maximizer | Output Gain | 6 / CC 35 | voice/MIDI or click | hover: 'Output Gain: 0.0 dB' |
| MMAX-F-B03 | SOFT CLIP | Soft clip on/off | Soft Clip Enable | 11 / CC 40 | voice/MIDI or click | hover: 'Soft Clip Enable' |
| MMAX-F-K03 | AMOUNT (Soft Clip) | How much soft clipping | Soft Clip Amount | 10 / CC 39 | voice/MIDI or click | hover: 'Soft Clip Amount: 64' |
| MMAX-F-B07 | PEAK / VU | Output meter mode: Peak or VU | Output Level Meter Mode | — | display/Remote item, not mapped | hover PEAK and VU buttons: 'Output Level Meter Mode: Peak' |
| MMAX-F-D02 | OUTPUT LEVEL L | Output level meter, left bar | Output Level Left | — | display/Remote item, not mapped | no tooltip; checked by eye: output level meter L (no hover tooltip) |
| MMAX-F-D04 | OUTPUT LEVEL R | Output level meter, right bar | Output Level Right | — | display/Remote item, not mapped | no tooltip; checked by eye: output level meter R (no hover tooltip) |

## MClass Maximizer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MMAX-B-D01 | M MAXIMIZER 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'M Maximizer 1' (device name tape) |
| MMAX-B-J01 | Audio Input L | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to M EQ 1: Left' |
| MMAX-B-J02 | Audio Input R | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to M EQ 1: Right' |
| MMAX-B-J03 | Audio Output L | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to M Stereo 1: Left' |
| MMAX-B-J04 | Audio Output R | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to M Stereo 1: Right' |

## MClass Stereo Imager — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MSIM-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 1 / CC 30 | voice/MIDI or click | hover on the bypass switch: 'Enabled: On' |
| MSIM-F-D01 | (LED column) | Input level meter | Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column |
| MSIM-F-D02 | M STEREO 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'M Stereo 1' (device name tape) |
| MSIM-F-K01 | LO BAND (width) | Low band stereo width, mono to wide | Low Width | 5 / CC 34 | voice/MIDI or click | hover: 'Low Width: 0' |
| MSIM-F-B02 | LO BAND ACTIVE | Low band on/off (light shows on) | Low Band Active | 4 / CC 33 | voice/MIDI or click | no tooltip; checked by eye: LO BAND ACTIVE light (no hover tooltip) |
| MSIM-F-D03 | (Lo width meter) | Low band width meter | Low Width Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: lo width meter (no hover tooltip) |
| MSIM-F-K02 | X-OVER FREQ | Where the low and high bands split, 100 Hz to 6 kHz | X-Over Frequency | 8 / CC 37 | voice/MIDI or click | hover: 'X-Over Frequency: 787 Hz' |
| MSIM-F-B03 | HI BAND ACTIVE | High band on/off (light shows on) | High Band Active | 2 / CC 31 | voice/MIDI or click | no tooltip; checked by eye: HI BAND ACTIVE light (no hover tooltip) |
| MSIM-F-K03 | HI BAND (width) | High band stereo width, mono to wide | High Width | 3 / CC 32 | voice/MIDI or click | hover: 'High Width: 0' |
| MSIM-F-D04 | (Hi width meter) | High band width meter | High Width Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: hi width meter (no hover tooltip) |
| MSIM-F-B04 | SOLO (HI/LO/NORMAL) | Solo mode: 3 buttons, pick one | Solo Mode | 7 / CC 36 | voice/MIDI or click | hover: 'Solo Mode: Normal' |

## MClass Stereo Imager — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MSIM-B-D01 | M STEREO 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'M Stereo 1' (device name tape) |
| MSIM-B-J01 | Audio Input L | Audio input left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to M Maximizer 1: Left' |
| MSIM-B-J02 | Audio Input R | Audio input right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to M Maximizer 1: Right' |
| MSIM-B-J03 | Audio Output L | Audio output left | Left | — | cable: right-click jack > device > jack name | hover: 'Connected to ALL Plate Spread: Left Inpu...' (tooltip clipped by zoom) |
| MSIM-B-J04 | Audio Output R | Audio output right | Right | — | cable: right-click jack > device > jack name | hover: 'Connected to ALL Plate Spread: Right Inp...' (tooltip clipped by zoom) |
| MSIM-B-J05 | Separate Out L | Separate output left | Separate Out Left | — | cable: right-click jack > device > jack name | hover: 'Separate Out Left' |
| MSIM-B-J06 | Separate Out R | Separate output right | Separate Out Right | — | cable: right-click jack > device > jack name | hover: 'Separate Out Right' |
| MSIM-B-B01 | Hi Band / Lo Band switch | Which band the Separate Out carries | Separate Out Mode | 6 / CC 35 | voice/MIDI or click | hover: 'Separate Out Mode: Lo Band' (switch currently on Lo Band) |

## RV7000 Mk II Advanced Reverb — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RV7K-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 8 / CC 37 | voice/MIDI or click | hover on the bypass switch: 'Enabled: On' |
| RV7K-F-D03 | (LED column) | Input level meter | Input Peak Meter | — | display/Remote item, not mapped | no tooltip; checked by eye: LED column (input peak meter) |
| RV7K-F-D01 | ALL PLATE SP... tape | Device name tape | Device Name | — | display/Remote item, not mapped | hover: tooltip 'ALL Plate Spread' (device name tape; tape reads ALL PLATE SP...) |
| RV7K-F-D02 | (patch display) | Patch name display | Patch Name | — | display/Remote item, not mapped | hover on patch display: tooltip 'ALL Plate Spread' |
| RV7K-F-B03 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | hover: 'Select previous patch' |
| RV7K-F-B04 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | hover: 'Select next patch' |
| RV7K-F-B05 | (folder) | Open patch browser | — | — | click only | hover: 'Browse patch' |
| RV7K-F-B06 | (disk) | Save patch | — | — | click only | hover: 'Save patch' |
| RV7K-F-B02 | (triangle) | Fold/unfold device | — | — | click only | no tooltip; checked by eye: fold triangle (no hover tooltip) |
| RV7K-F-B08 | Remote Programmer (slot + arrow) | Show/hide the Remote Programmer section (see rv7000-programmer) | — | — | click only | no tooltip; checked by eye: Remote Programmer slot + arrow (no hover tooltip) |
| RV7K-F-B07 | EQ Enable | EQ section on/off (light shows on) | EQ On/Off | 6 / CC 35 | voice/MIDI or click | hover: 'EQ On/Off' |
| RV7K-F-B09 | Gate Enable | Gate section on/off (light shows on) | Gate On/Off | 7 / CC 36 | voice/MIDI or click | hover: 'Gate On/Off' |
| RV7K-F-K01 | Decay | Reverb tail length | Decay | 1 / CC 30 | voice/MIDI or click | hover: 'Decay: 104' |
| RV7K-F-K02 | HF Damp | High-frequency damping | HF Damp | 2 / CC 31 | voice/MIDI or click | hover: 'HF Damp: 28' |
| RV7K-F-K03 | HI EQ | High EQ amount | Hi EQ | 3 / CC 32 | voice/MIDI or click | hover: 'Hi EQ: 0' |
| RV7K-F-K04 | Dry - Wet | Balance dry and reverb | Dry/Wet | 4 / CC 33 | voice/MIDI or click | hover: 'Dry/Wet: 127' |
| RV7K-F-B13 | Edit Mode | Cycle the programmer view: Reverb, EQ, Gate | Edit Mode | 5 / CC 34 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] hover: 'Edit Mode' (Reverb/EQ/Gate button) |
| RV7K-F-D05 | Reverb/EQ/Gate lights | Shows which edit mode is showing | Edit Mode Name | — | display/Remote item, not mapped | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip; checked by eye: Reverb/EQ/Gate lights |
| RV7K-F-B10 | (up/down arrows) | Step through patches / Reason tooltips: up='Select previous sample', down='Select next sample' | — | — | click only | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] hover: up arrow 'Select previous sample', down arrow 'Select next sample' |
| RV7K-F-B11 | (folder) | Open patch browser | — | — | click only | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] hover: 'Browse sample' |
| RV7K-F-B12 | (waveform button) | Unknown (waveform icon); confirm by hover | — | — | click only | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] hover: 'Start sampling' |
| RV7K-F-D04 | (display) | Graph + parameter names/values for the current view | — | — | click only | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip; checked by eye: programmer display (no hover tooltip) |
| RV7K-F-K05 | (left knob 1) | Soft knob beside the display | Soft Knob 1 | 9 / CC 38 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |
| RV7K-F-K06 | (right knob 5) | Soft knob beside the display | Soft Knob 5 | 13 / CC 42 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |
| RV7K-F-K07 | (left knob 2) | Soft knob beside the display | Soft Knob 2 | 10 / CC 39 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |
| RV7K-F-K08 | (right knob 6) | Soft knob beside the display | Soft Knob 6 | 14 / CC 43 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |
| RV7K-F-K09 | (left knob 3) | Soft knob beside the display | Soft Knob 3 | 11 / CC 40 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |
| RV7K-F-K10 | (right knob 7) | Soft knob beside the display | Soft Knob 7 | 15 / CC 44 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |
| RV7K-F-K11 | (left knob 4) | Soft knob beside the display | Soft Knob 4 | 12 / CC 41 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |
| RV7K-F-K12 | (right knob 8) | Soft knob beside the display | Soft Knob 8 | 16 / CC 45 | voice/MIDI or click | [Remote Programmer, Reverb edit mode (picture rv7000-programmer-reverb_front_labeled.png)] no tooltip in Reason (hovered 2x, 2.5 s); soft-knob numbering NOT provable from the panel; manual says 8 dials around the display whose names show in the display |

## RV7000 Mk II Advanced Reverb — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RV7K-B-D01 | ALL PLATE SP... tape | Device name tape (back) | — | — | click/drag only (no Remote item) | hover: tooltip 'ALL Plate Spread' (device name tape) |
| RV7K-B-K01 | Decay (trim) | Amount knob for Decay CV | — | — | click/drag only (no Remote item) | hover: 'Decay CV In: 127' |
| RV7K-B-J01 | Decay (CV in) | CV input for Decay | Decay CV In | — | cable: right-click jack > device > jack name | hover: 'Decay CV In' |
| RV7K-B-K02 | HF Damp (trim) | Amount knob for HF Damp CV | — | — | click/drag only (no Remote item) | hover: 'HF Damp CV In: 127' |
| RV7K-B-J02 | HF Damp (CV in) | CV input for HF Damp | HF Damp CV In | — | cable: right-click jack > device > jack name | hover: 'HF Damp CV In' |
| RV7K-B-J03 | Gate Trig (CV in) | Gate trigger input | Gate Trig Input | — | cable: right-click jack > device > jack name | hover: 'Gate Trig Input' |
| RV7K-B-J04 | Audio Input L | Audio input left | Left Input | — | cable: right-click jack > device > jack name | hover: 'Connected to M Stereo 1: Left' |
| RV7K-B-J05 | Audio Input R | Audio input right | Right Input | — | cable: right-click jack > device > jack name | hover: 'Connected to M Stereo 1: Right' |
| RV7K-B-J06 | Audio Output L | Audio output left | Left Output | — | cable: right-click jack > device > jack name | hover: 'Connected to Mix Channel: From Insert F...' (tooltip clipped by zoom) |
| RV7K-B-J07 | Audio Output R | Audio output right | Right Output | — | cable: right-click jack > device > jack name | hover: 'Connected to Mix Channel: From Insert F...' (tooltip clipped by zoom) |

## Matrix Pattern Sequencer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MTRX-F-D04 | MATRIX 2 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tooltip 'Matrix 2' (device name) |
| MTRX-F-B01 | Pattern (switch) | Pattern Enable: turns pattern playback on/off at the next downbeat (light shows on) | Pattern Enable | — | display/Remote item, not mapped | tooltip 'Pattern Enable' |
| MTRX-F-D01 | Mute (light) | Mute light: lit when the Matrix track is muted in the sequencer | — | — | click only | no tooltip (light), checked by eye: Mute light, dark |
| MTRX-F-B04 | Pattern 1 | Pattern button 1 (selects pattern 1 in the current bank) | Pattern 1 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 1) |
| MTRX-F-B05 | Pattern 2 | Pattern button 2 (selects pattern 2 in the current bank) | Pattern 2 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 2) |
| MTRX-F-B06 | Pattern 3 | Pattern button 3 (selects pattern 3 in the current bank) | Pattern 3 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 3) |
| MTRX-F-B07 | Pattern 4 | Pattern button 4 (selects pattern 4 in the current bank) | Pattern 4 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 4) |
| MTRX-F-B08 | Pattern 5 | Pattern button 5 (selects pattern 5 in the current bank) | Pattern 5 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 5) |
| MTRX-F-B09 | Pattern 6 | Pattern button 6 (selects pattern 6 in the current bank) | Pattern 6 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 6) |
| MTRX-F-B10 | Pattern 7 | Pattern button 7 (selects pattern 7 in the current bank) | Pattern 7 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 7) |
| MTRX-F-B11 | Pattern 8 | Pattern button 8 (selects pattern 8 in the current bank) | Pattern 8 | — | display/Remote item, not mapped | tooltip 'Pattern Select' (Remote item is Pattern 8) |
| MTRX-F-B13 | Bank A | Bank button A (pick the bank, then click a Pattern button) | Bank A | — | display/Remote item, not mapped | tooltip 'Bank Select' (Remote item is Bank A) |
| MTRX-F-B14 | Bank B | Bank button B (pick the bank, then click a Pattern button) | Bank B | — | display/Remote item, not mapped | tooltip 'Bank Select' (Remote item is Bank B) |
| MTRX-F-B15 | Bank C | Bank button C (pick the bank, then click a Pattern button) | Bank C | — | display/Remote item, not mapped | tooltip 'Bank Select' (Remote item is Bank C) |
| MTRX-F-B16 | Bank D | Bank button D (pick the bank, then click a Pattern button) | Bank D | — | display/Remote item, not mapped | tooltip 'Bank Select' (Remote item is Bank D) |
| MTRX-F-B12 | Run | Run: starts/stops this Matrix on its own, without the main sequencer | Run | — | display/Remote item, not mapped | tooltip 'Play' (Remote item is Run) |
| MTRX-F-B02 | Keys/Curve switch | Switches the upper pattern window between Keys (note pitch) and Curve (curve CV) editing | — | — | click only | tooltip 'Mode: Key Edit' (shown with the switch on Keys) |
| MTRX-F-D02 | (Keys/Curve lights) | Lights show whether Keys or Curve is showing | — | — | click only | no tooltip (lights), checked by eye: lower light lit = Keys |
| MTRX-F-S01 | (octave slider 1-5) | 5-way slider: picks which of five octaves the note row shows | — | — | click only | tooltip 'Octave: 3' |
| MTRX-F-D06 | (octave arrows 1-5) | Arrows 1 to 5 beside the slider show the chosen octave | — | — | click only | no tooltip, checked by eye: arrows 1-5 beside the slider |
| MTRX-F-B17 | Tie | Tie: draw longer (tied) gate steps | — | — | click only | tooltip 'Gate Tie' |
| MTRX-F-D05 | (Curve/Keys pattern window) | Upper pattern window: note pitch (Keys) or curve values (Curve); click/drag to draw | — | — | click only | no tooltip, checked by eye: upper pattern grid with the note row |
| MTRX-F-D07 | (Gate pattern window) | Lower pattern window: gate/velocity strips; click/drag to draw | — | — | click only | no tooltip, checked by eye: gate strips |
| MTRX-F-D03 | Steps (display) | Number of steps in the pattern (1 to 32) | — | — | click only | tooltip 'Pattern Length: 16' |
| MTRX-F-B03 | Steps (up/down arrows) | Raise or lower the number of steps | — | — | click only | no tooltip (arrows never show one); checked by eye |
| MTRX-F-K01 | RESOLUTION | How fast the pattern plays relative to the tempo, 1/2 to 1/128 | Resolution | — | display/Remote item, not mapped | tooltip 'Resolution: 1/16' |
| MTRX-F-B18 | Shuffle | Shuffle on/off for this pattern (amount is set by Global Shuffle in the ReGroove Mixer) | Pattern Shuffle | — | display/Remote item, not mapped | tooltip 'Shuffle' (Remote item is Pattern Shuffle) |

## Matrix Pattern Sequencer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MTRX-B-D01 | MATRIX 2 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | tooltip 'Matrix 2' |
| MTRX-B-J01 | Curve CV | Curve CV output | Curve CV | — | cable: right-click jack > device > jack name | cabled: 'Connected to ALL Plate Spread: Decay CV In' |
| MTRX-B-J02 | Note CV | Note CV output (pitch) | Note CV | — | cable: right-click jack > device > jack name | empty: tooltip 'Note CV' |
| MTRX-B-J03 | Gate CV | Gate CV output (on/off + velocity) | Gate | — | cable: right-click jack > device > jack name | cabled: 'Connected to ALL Plate Spread: Gate Trig Input' |
| MTRX-B-B01 | Bipolar/Unipolar switch | Curve CV range: Bipolar (zero in the middle) or Unipolar (zero at the bottom) | — | — | click/drag only (no Remote item) | tooltip 'Unipolar/Bipolar Curve: 0' |

## Spider Audio Merger & Splitter — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SPDA-F-D01 | SPIDER AUDIO 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tooltip 'Spider Audio 1' |
| SPDA-F-D02 | Merge input 1 L (light) | Lights when audio arrives at merge input 1, left | Merge Input 1 Left Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D07 | Merge input 1 R (light) | Lights when audio arrives at merge input 1, right | Merge Input 1 Right Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D03 | Merge input 2 L (light) | Lights when audio arrives at merge input 2, left | Merge Input 2 Left Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D08 | Merge input 2 R (light) | Lights when audio arrives at merge input 2, right | Merge Input 2 Right Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D04 | Merge input 3 L (light) | Lights when audio arrives at merge input 3, left | Merge Input 3 Left Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D09 | Merge input 3 R (light) | Lights when audio arrives at merge input 3, right | Merge Input 3 Right Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D05 | Merge input 4 L (light) | Lights when audio arrives at merge input 4, left | Merge Input 4 Left Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D10 | Merge input 4 R (light) | Lights when audio arrives at merge input 4, right | Merge Input 4 Right Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D06 | Split input L (light) | Lights when audio arrives at the splitter input, left | Split Input Left Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |
| SPDA-F-D11 | Split input R (light) | Lights when audio arrives at the splitter input, right | Split Input Right Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye: dark when idle |

## Spider Audio Merger & Splitter — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SPDA-B-D01 | SPIDER AUDIO 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | tooltip 'Spider Audio 1' |
| SPDA-B-J01 | Merge input 1 L | Merger input 1, left (L/Mono) | Merge Input 1 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 1 Left' |
| SPDA-B-J11 | Merge input 1 R | Merger input 1, right | Merge Input 1 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 1 Right' |
| SPDA-B-J02 | Merge input 2 L | Merger input 2, left (L/Mono) | Merge Input 2 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 2 Left' |
| SPDA-B-J12 | Merge input 2 R | Merger input 2, right | Merge Input 2 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 2 Right' |
| SPDA-B-J03 | Merge input 3 L | Merger input 3, left (L/Mono) | Merge Input 3 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 3 Left' |
| SPDA-B-J13 | Merge input 3 R | Merger input 3, right | Merge Input 3 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 3 Right' |
| SPDA-B-J04 | Merge input 4 L | Merger input 4, left (L/Mono) | Merge Input 4 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 4 Left' |
| SPDA-B-J14 | Merge input 4 R | Merger input 4, right | Merge Input 4 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 4 Right' |
| SPDA-B-J05 | Merge out L | Merger output, left | Merge Output Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Output Left' |
| SPDA-B-J15 | Merge out R | Merger output, right | Merge Output Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Output Right' |
| SPDA-B-J06 | Split in A (L) | Splitter input, left (A) | Split Input Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Input Left' |
| SPDA-B-J16 | Split in B (R) | Splitter input, right (B) | Split Input Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Input Right' |
| SPDA-B-J07 | Split out 1 A (L) | Splitter output 1, left (A) | Split Output 1 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 1 Left' |
| SPDA-B-J17 | Split out 1 B (R) | Splitter output 1, right (B) | Split Output 1 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 1 Right' |
| SPDA-B-J08 | Split out 2 A (L) | Splitter output 2, left (A) | Split Output 2 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 2 Left' |
| SPDA-B-J18 | Split out 2 B (R) | Splitter output 2, right (B) | Split Output 2 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 2 Right' |
| SPDA-B-J09 | Split out 3 A (L) | Splitter output 3, left (A) | Split Output 3 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 3 Left' |
| SPDA-B-J19 | Split out 3 B (R) | Splitter output 3, right (B) | Split Output 3 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 3 Right' |
| SPDA-B-J10 | Split out 4 A (L) | Splitter output 4, left (A) | Split Output 4 Left | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 4 Left' |
| SPDA-B-J20 | Split out 4 B (R) | Splitter output 4, right (B) | Split Output 4 Right | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split Output 4 Right' |

## Spider CV Merger & Splitter — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SPDC-F-D01 | SPIDER CV 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tooltip 'Spider CV 1' |
| SPDC-F-D04 | Merge input 1 (light) | Lights when a CV signal arrives at merge input 1 | Merge Input 1 Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye |
| SPDC-F-D05 | Merge input 2 (light) | Lights when a CV signal arrives at merge input 2 | Merge Input 2 Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye |
| SPDC-F-D06 | Merge input 3 (light) | Lights when a CV signal arrives at merge input 3 | Merge Input 3 Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye |
| SPDC-F-D07 | Merge input 4 (light) | Lights when a CV signal arrives at merge input 4 | Merge Input 4 Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye |
| SPDC-F-D02 | Split A input (light) | Lights when a CV signal arrives at split A | Split A Input Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye |
| SPDC-F-D03 | Split B input (light) | Lights when a CV signal arrives at split B | Split B Input Activity | — | display/Remote item, not mapped | no tooltip (light), checked by eye |

## Spider CV Merger & Splitter — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SPDC-B-D01 | SPIDER CV 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | tooltip 'Spider CV 1' |
| SPDC-B-K01 | Merge trim 1 | Level knob for merge input 1 | — | — | click/drag only (no Remote item) | tooltip 'Merge Input 1: 127' (trim at full) |
| SPDC-B-J07 | Merge input 1 | Merger CV input 1 | Merge Input 1 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 1' |
| SPDC-B-K02 | Merge trim 2 | Level knob for merge input 2 | — | — | click/drag only (no Remote item) | tooltip 'Merge Input 2: 127' (trim at full) |
| SPDC-B-J08 | Merge input 2 | Merger CV input 2 | Merge Input 2 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 2' |
| SPDC-B-K03 | Merge trim 3 | Level knob for merge input 3 | — | — | click/drag only (no Remote item) | tooltip 'Merge Input 3: 127' (trim at full) |
| SPDC-B-J09 | Merge input 3 | Merger CV input 3 | Merge Input 3 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 3' |
| SPDC-B-K04 | Merge trim 4 | Level knob for merge input 4 | — | — | click/drag only (no Remote item) | tooltip 'Merge Input 4: 127' (trim at full) |
| SPDC-B-J10 | Merge input 4 | Merger CV input 4 | Merge Input 4 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Input 4' |
| SPDC-B-J11 | Merge out | Merger CV output | Merge Output | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Merge Output' |
| SPDC-B-J01 | Split A in | Split A input | Split A Input | — | cable: right-click jack > device > jack name | cabled: 'Connected to Matrix 2: Curve CV'; own name from Reason's cable menu: 'Split A Input' |
| SPDC-B-J02 | Split A out 1 | Split A output | Split A Output 1 | — | cable: right-click jack > device > jack name | cabled: 'Connected to ALL Plate Spread: Decay CV In'; own name from Reason's cable menu: 'Split A Output 1' |
| SPDC-B-J03 | Split A out 2 | Split A output | Split A Output 2 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split A Output 2' |
| SPDC-B-J12 | Split A out 3 | Split A output | Split A Output 3 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split A Output 3' |
| SPDC-B-J13 | Split A inverted out | Split A inverted output (Inv) | Split A Output 4/Inv | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split A Output 4/Inv' |
| SPDC-B-J04 | Split B in | Split B input | Split B Input | — | cable: right-click jack > device > jack name | cabled: 'Connected to Matrix 2: Gate'; own name from Reason's cable menu: 'Split B Input' |
| SPDC-B-J05 | Split B out 1 | Split B output | Split B Output 1 | — | cable: right-click jack > device > jack name | cabled: 'Connected to ALL Plate Spread: Gate Trig Input'; own name from Reason's cable menu: 'Split B Output 1' |
| SPDC-B-J06 | Split B out 2 | Split B output | Split B Output 2 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split B Output 2' |
| SPDC-B-J14 | Split B out 3 | Split B output | Split B Output 3 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split B Output 3' |
| SPDC-B-J15 | Split B inverted out | Split B inverted output (Inv) | Split B Output 4/Inv | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Split B Output 4/Inv' |

## Pulsar Dual LFO — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PULS-F-D04 | PULSAR 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tooltip 'Pulsar 1' |
| PULS-F-D01 | LFO 1 (rate lamp) | Lamp above the Rate knob; blinks at the LFO 1 rate | — | — | click only | no tooltip (lamp), checked by eye: lit |
| PULS-F-K02 | LFO 1 RATE | LFO 1 speed (tempo-sync step when Tempo Sync is on) | LFO1 Rate Free | — | display/Remote item, not mapped | tooltip 'LFO1 Rate Synced: 3/8' (Tempo Sync was on; with it off Reason shows LFO1 Rate Free) |
| PULS-F-B01 | LFO 1 waveform up | Next LFO 1 waveform | LFO1 Waveform | — | display/Remote item, not mapped | tooltip 'LFO1 Waveform' |
| PULS-F-D05 | LFO 1 waveform display | Shows the LFO 1 waveform (click-drag up/down to change) | LFO1 Waveform | — | display/Remote item, not mapped | tooltip 'LFO1 Waveform: Sine' |
| PULS-F-B05 | LFO 1 waveform down | Previous LFO 1 waveform | LFO1 Waveform | — | display/Remote item, not mapped | tooltip 'LFO1 Waveform' |
| PULS-F-K03 | LFO 1 LEVEL | LFO 1 output level | LFO1 Level | — | display/Remote item, not mapped | tooltip 'LFO1 Level: 50%' |
| PULS-F-B07 | ENV SYNC (LFO 1) | Envelope trigger also restarts LFO 1 | LFO1 Env Sync | — | display/Remote item, not mapped | tooltip 'LFO1 Env Sync' |
| PULS-F-B09 | TEMPO SYNC (LFO 1) | LFO 1 follows the song tempo | LFO1 Tempo Sync | — | display/Remote item, not mapped | tooltip 'LFO1 Tempo Sync' |
| PULS-F-K10 | PHASE (LFO 1) | Where in its cycle LFO 1 starts, 0-360 degrees | LFO1 Phase | — | display/Remote item, not mapped | tooltip 'LFO1 Phase: 0°' |
| PULS-F-K11 | SHUFFLE (LFO 1) | Swing between pairs of LFO 1 cycles, 50-75% | LFO1 Shuffle | — | display/Remote item, not mapped | tooltip 'LFO1 Shuffle: 50%' |
| PULS-F-K12 | LAG (LFO 1) | Smooths LFO 1 (lowpass) | LFO1 Lag | — | display/Remote item, not mapped | tooltip 'LFO1 Lag: 0%' |
| PULS-F-K01 | RATE (LFO 2 to LFO 1) | How much LFO 2 changes LFO 1 rate (FM) | LFO2 to LFO1 Rate | — | display/Remote item, not mapped | tooltip 'LFO2 to LFO1 Rate: 0%' |
| PULS-F-K04 | LEVEL (LFO 2 to LFO 1) | How much LFO 2 changes LFO 1 level (AM) | LFO2 to LFO1 Level | — | display/Remote item, not mapped | tooltip 'LFO2 to LFO1 Level: 0%' |
| PULS-F-B10 | SYNC (LFO 1 to LFO 2) | Every new LFO 2 cycle restarts LFO 1 | Sync LFO1 to LFO2 | — | display/Remote item, not mapped | tooltip 'Sync LFO1 to LFO2' |
| PULS-F-D02 | LFO 2 (rate lamp) | Lamp above the Rate knob; blinks at the LFO 2 rate | — | — | click only | no tooltip (lamp), checked by eye: dark |
| PULS-F-K05 | LFO 2 RATE | LFO 2 speed (tempo-sync step when Tempo Sync is on) | LFO2 Rate Free | — | display/Remote item, not mapped | tooltip 'LFO2 Rate Free: 8.18 Hz' |
| PULS-F-B02 | LFO 2 waveform up | Next LFO 2 waveform | LFO2 Waveform | — | display/Remote item, not mapped | tooltip 'LFO2 Waveform' |
| PULS-F-D06 | LFO 2 waveform display | Shows the LFO 2 waveform (click-drag up/down to change) | LFO2 Waveform | — | display/Remote item, not mapped | tooltip 'LFO2 Waveform: Triangle' |
| PULS-F-B06 | LFO 2 waveform down | Previous LFO 2 waveform | LFO2 Waveform | — | display/Remote item, not mapped | tooltip 'LFO2 Waveform' |
| PULS-F-K06 | LFO 2 LEVEL | LFO 2 output level | LFO2 Level | — | display/Remote item, not mapped | tooltip 'LFO2 Level: 50%' |
| PULS-F-B08 | ON/OFF (LFO 2) | Turn LFO 2 on or off | LFO2 Enabled | — | display/Remote item, not mapped | tooltip 'LFO2 Enabled' |
| PULS-F-B11 | TEMPO SYNC (LFO 2) | LFO 2 follows the song tempo | LFO2 Tempo Sync | — | display/Remote item, not mapped | tooltip 'LFO2 Tempo Sync' |
| PULS-F-K13 | PHASE (LFO 2) | Where in its cycle LFO 2 starts, 0-360 degrees | LFO2 Phase | — | display/Remote item, not mapped | tooltip 'LFO2 Phase: 0°' |
| PULS-F-K14 | SHUFFLE (LFO 2) | Swing between pairs of LFO 2 cycles, 50-75% | LFO2 Shuffle | — | display/Remote item, not mapped | tooltip 'LFO2 Shuffle: 50%' |
| PULS-F-K15 | LAG (LFO 2) | Smooths LFO 2 (lowpass) | LFO2 Lag | — | display/Remote item, not mapped | tooltip 'LFO2 Lag: 0%' |
| PULS-F-B04 | LFO2 TRIG | Every new LFO 2 cycle triggers the envelope | LFO2 Triggers Envelope | — | display/Remote item, not mapped | tooltip 'LFO2 Triggers Envelope' |
| PULS-F-D03 | (envelope lamp) | Lamp between LFO2 TRIG and TRIG; lit while the envelope runs | — | — | click only | no tooltip (lamp), checked by eye |
| PULS-F-B03 | TRIG | Non-latching button that triggers the envelope | Trig | — | display/Remote item, not mapped | tooltip 'Trig' |
| PULS-F-K07 | ATTACK | Envelope attack time (0.1 ms to 3 s) | Attack | — | display/Remote item, not mapped | tooltip 'Attack: 0.1 ms' |
| PULS-F-K08 | RELEASE | Envelope release time (0 ms to 10 s) | Release | — | display/Remote item, not mapped | tooltip 'Release: 1.29 s' |
| PULS-F-K16 | RATE (envelope to LFO 1) | How much the envelope changes LFO 1 rate | LFO1 Env Rate | — | display/Remote item, not mapped | tooltip 'LFO1 Env Rate: 0%' |
| PULS-F-K17 | LEVEL (envelope to LFO 1) | How much the envelope changes LFO 1 level | LFO1 Env Level | — | display/Remote item, not mapped | tooltip 'LFO1 Env Level: 0%' |
| PULS-F-K18 | RATE (envelope to LFO 2) | How much the envelope changes LFO 2 rate | LFO2 Env Rate | — | display/Remote item, not mapped | tooltip 'LFO2 Env Rate: 0%' |
| PULS-F-K19 | LEVEL (envelope to LFO 2) | How much the envelope changes LFO 2 level | LFO2 Env Level | — | display/Remote item, not mapped | tooltip 'LFO2 Env Level: 0%' |
| PULS-F-K09 | KBD FOLLOW | How much MIDI notes change the LFO rates (bipolar) | Keyboard Track | — | display/Remote item, not mapped | tooltip 'Keyboard Track: 0%' |

## Pulsar Dual LFO — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PULS-B-D01 | PULSAR 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | tooltip 'Pulsar 1' |
| PULS-B-K01 | LFO 1 Rate (trim) | Amount knob for the LFO 1 Rate CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO1 Rate Modulation Input: 100%' |
| PULS-B-J01 | LFO 1 Rate (CV in) | CV input: modulates LFO 1 Rate | LFO1 Rate CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 Rate CV' |
| PULS-B-K02 | LFO 1 Phase (trim) | Amount knob for the LFO 1 Phase CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO1 Phase Modulation Input: 100%' |
| PULS-B-J02 | LFO 1 Phase (CV in) | CV input: modulates LFO 1 Phase | LFO1 Phase CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 Phase CV' |
| PULS-B-K03 | LFO 1 Shuffle (trim) | Amount knob for the LFO 1 Shuffle CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO1 Shuffle Modulation Input: 100%' |
| PULS-B-J03 | LFO 1 Shuffle (CV in) | CV input: modulates LFO 1 Shuffle | LFO1 Shuffle CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 Shuffle CV' |
| PULS-B-K04 | LFO 1 Level (trim) | Amount knob for the LFO 1 Level CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO1 Level Modulation Input: 100%' |
| PULS-B-J04 | LFO 1 Level (CV in) | CV input: modulates LFO 1 Level | LFO1 Level CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 Level CV' |
| PULS-B-K05 | LFO 2 Rate (trim) | Amount knob for the LFO 2 Rate CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO2 Rate Modulation Input: 100%' |
| PULS-B-J05 | LFO 2 Rate (CV in) | CV input: modulates LFO 2 Rate | LFO2 Rate CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 Rate CV' |
| PULS-B-K06 | LFO 2 Phase (trim) | Amount knob for the LFO 2 Phase CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO2 Phase Modulation Input: 100%' |
| PULS-B-J06 | LFO 2 Phase (CV in) | CV input: modulates LFO 2 Phase | LFO2 Phase CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 Phase CV' |
| PULS-B-K07 | LFO 2 Shuffle (trim) | Amount knob for the LFO 2 Shuffle CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO2 Shuffle Modulation Input: 100%' |
| PULS-B-J07 | LFO 2 Shuffle (CV in) | CV input: modulates LFO 2 Shuffle | LFO2 Shuffle CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 Shuffle CV' |
| PULS-B-K08 | LFO 2 Level (trim) | Amount knob for the LFO 2 Level CV input | — | — | click/drag only (no Remote item) | tooltip 'LFO2 Level Modulation Input: 100%' |
| PULS-B-J08 | LFO 2 Level (CV in) | CV input: modulates LFO 2 Level | LFO2 Level CV | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 Level CV' |
| PULS-B-J10 | LFO 1 CV out 1 | LFO 1 CV output 1 | LFO1 CVOut1 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 CVOut1' |
| PULS-B-J20 | LFO 1 audio out 1 | LFO 1 audio output 1 | LFO1 AudioOut1 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 AudioOut1' |
| PULS-B-J11 | LFO 1 CV out 2 | LFO 1 CV output 2 | LFO1 CVOut2 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 CVOut2' |
| PULS-B-J21 | LFO 1 audio out 2 | LFO 1 audio output 2 | LFO1 AudioOut2 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 AudioOut2' |
| PULS-B-J12 | LFO 1 CV out 3 (inverted) | LFO 1 CV output 3 (inverted) | LFO1 CVOut3 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 CVOut3' |
| PULS-B-J22 | LFO 1 audio out 3 (inverted) | LFO 1 audio output 3 (inverted) | LFO1 AudioOut3 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 AudioOut3' |
| PULS-B-J13 | LFO 1 CV out 4 (inverted) | LFO 1 CV output 4 (inverted) | LFO1 CVOut4 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 CVOut4' |
| PULS-B-J23 | LFO 1 audio out 4 (inverted) | LFO 1 audio output 4 (inverted) | LFO1 AudioOut4 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO1 AudioOut4' |
| PULS-B-J14 | LFO 2 CV out 1 | LFO 2 CV output 1 | LFO2 CVOut1 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 CVOut1' |
| PULS-B-J25 | LFO 2 audio out 1 | LFO 2 audio output 1 | LFO2 AudioOut1 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 AudioOut1' |
| PULS-B-J15 | LFO 2 CV out 2 | LFO 2 CV output 2 | LFO2 CVOut2 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 CVOut2' |
| PULS-B-J26 | LFO 2 audio out 2 | LFO 2 audio output 2 | LFO2 AudioOut2 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 AudioOut2' |
| PULS-B-J16 | LFO 2 CV out 3 (inverted) | LFO 2 CV output 3 (inverted) | LFO2 CVOut3 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 CVOut3' |
| PULS-B-J27 | LFO 2 audio out 3 (inverted) | LFO 2 audio output 3 (inverted) | LFO2 AudioOut3 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 AudioOut3' |
| PULS-B-J17 | LFO 2 CV out 4 (inverted) | LFO 2 CV output 4 (inverted) | LFO2 CVOut4 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 CVOut4' |
| PULS-B-J28 | LFO 2 audio out 4 (inverted) | LFO 2 audio output 4 (inverted) | LFO2 AudioOut4 | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO2 AudioOut4' |
| PULS-B-J09 | LFO 1+2 CV out | Combined LFO 1+2 CV output | LFO12 CVOut | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO12 CVOut' |
| PULS-B-J24 | LFO 1+2 audio out | Combined LFO 1+2 audio output | LFO12 AudioOut | — | cable: right-click jack > device > jack name | empty jack: tooltip 'LFO12 AudioOut' |
| PULS-B-J18 | Envelope Gate In | CV/gate input that triggers the envelope | Envelope Gate In | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Envelope Gate In' |
| PULS-B-J19 | Envelope CV Out | Envelope CV output | Env CVOut | — | cable: right-click jack > device > jack name | empty jack: tooltip 'Env CVOut' |

## RPG-8 Monophonic Arpeggiator — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RPG8-F-D03 | ARP 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tape shows 'Arp 1'; tooltip 'Arp 1' label only |
| RPG8-F-K01 | VELOCITY | Fixed note velocity 1-127, or Manual (use played velocity) at the far right | Velocity/Manual | — | display/Remote item, not mapped | tooltip 'Velocity: Manual' |
| RPG8-F-D02 | (Manual light) | Light beside MAN.: lit when Velocity is on Manual | — | — | click only | LED, no tooltip |
| RPG8-F-D01 | MIDI IN (light) | Lights when MIDI notes arrive | — | — | click only | MIDI In LED, no tooltip |
| RPG8-F-B24 | HOLD | Hold: arpeggio keeps playing after you release the keys | Hold | — | display/Remote item, not mapped | tooltip 'Hold' |
| RPG8-F-D04 | (octave shift lights -3 to +3) | Seven lights show the octave shift, -3 to +3 | Octave Shift | — | display/Remote item, not mapped | octave-shift LEDs, no tooltip |
| RPG8-F-B31 | OCTAVE SHIFT (left arrow) | Shift the arpeggio down one octave | Octave Shift Down | — | display/Remote item, not mapped | tooltip 'Octave Shift: 0' |
| RPG8-F-B32 | OCTAVE SHIFT (right arrow) | Shift the arpeggio up one octave | Octave Shift Up | — | display/Remote item, not mapped | tooltip 'Octave Shift: 0' |
| RPG8-F-B01 | ON | Arpeggiator on/off | Arpeggiator Enable | — | display/Remote item, not mapped | tooltip 'Arpeggiator Enable' |
| RPG8-F-K02 | MODE | Arpeggio direction: Up, Up+Down, Down, Random, Manual | Mode | — | display/Remote item, not mapped | tooltip 'Mode' |
| RPG8-F-B05 | 4 OCT | Octave range 4 | Octave 4 | — | display/Remote item, not mapped | tooltip 'Octave' |
| RPG8-F-B25 | 3 OCT | Octave range 3 | Octave 3 | — | display/Remote item, not mapped | tooltip 'Octave' |
| RPG8-F-B27 | 2 OCT | Octave range 2 | Octave 2 | — | display/Remote item, not mapped | tooltip 'Octave' |
| RPG8-F-B28 | 1 OCT | Octave range 1 (just the played notes) | Octave 1 | — | display/Remote item, not mapped | tooltip 'Octave' |
| RPG8-F-B06 | INSERT 4-2 | Insert: adds notes in a 4-2 pattern | Insert 4-2 | — | display/Remote item, not mapped | tooltip 'Insert' |
| RPG8-F-B07 | INSERT 3-1 | Insert: adds notes in a 3-1 pattern | Insert 3-1 | — | display/Remote item, not mapped | tooltip 'Insert' |
| RPG8-F-B26 | INSERT HI | Insert: adds the highest note | Insert High | — | display/Remote item, not mapped | tooltip 'Insert' |
| RPG8-F-B29 | INSERT LOW | Insert: adds the lowest note | Insert Low | — | display/Remote item, not mapped | tooltip 'Insert' |
| RPG8-F-B30 | INSERT OFF | Insert off | Insert Off | — | display/Remote item, not mapped | tooltip 'Insert' |
| RPG8-F-B33 | SYNC | Rate follows the song tempo | Sync | — | display/Remote item, not mapped | tooltip 'Sync' |
| RPG8-F-B34 | FREE | Rate runs free (not tied to tempo) | — | — | click only | tooltip 'Sync' (Sync/Free pair is one Sync switch) |
| RPG8-F-D06 | (rate display) | Shows the rate value, e.g. 1/16 | — | — | click only | rate display shows 1/16; no tooltip |
| RPG8-F-K03 | RATE | Arpeggio speed (note value when Sync is on) | Rate | — | display/Remote item, not mapped | tooltip 'Synced Rate: 1/16' |
| RPG8-F-D07 | (Rate light) | Light by the Rate knob: blinks at the rate | — | — | click only | Rate LED, no tooltip |
| RPG8-F-K04 | GATE LENGTH | Length of each note, 0 to Tie (legato) | Gate Length | — | display/Remote item, not mapped | tooltip 'Gate Length: 95' |
| RPG8-F-B35 | SINGLE NOTE REPEAT | Repeat a single held note | Single Note Repeat | — | display/Remote item, not mapped | tooltip 'Single Note Repeat' |
| RPG8-F-B02 | PATTERN | Pattern editor on/off | Pattern Enable | — | display/Remote item, not mapped | tooltip 'Pattern Enable' |
| RPG8-F-B03 | STEPS - | Fewer pattern steps | Pattern Length Down | — | display/Remote item, not mapped | tooltip 'Pattern Step Count: 16' (shown only while Pattern is on; none when off) |
| RPG8-F-B04 | STEPS + | More pattern steps | Pattern Length Up | — | display/Remote item, not mapped | tooltip 'Pattern Step Count: 16' (shown only while Pattern is on; none when off) |
| RPG8-F-B08 | Pattern step 1 | Pattern step 1 on/off | Pattern Step 1 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B09 | Pattern step 2 | Pattern step 2 on/off | Pattern Step 2 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B10 | Pattern step 3 | Pattern step 3 on/off | Pattern Step 3 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B11 | Pattern step 4 | Pattern step 4 on/off | Pattern Step 4 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B12 | Pattern step 5 | Pattern step 5 on/off | Pattern Step 5 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B13 | Pattern step 6 | Pattern step 6 on/off | Pattern Step 6 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B14 | Pattern step 7 | Pattern step 7 on/off | Pattern Step 7 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B15 | Pattern step 8 | Pattern step 8 on/off | Pattern Step 8 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B16 | Pattern step 9 | Pattern step 9 on/off | Pattern Step 9 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B17 | Pattern step 10 | Pattern step 10 on/off | Pattern Step 10 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B18 | Pattern step 11 | Pattern step 11 on/off | Pattern Step 11 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B19 | Pattern step 12 | Pattern step 12 on/off | Pattern Step 12 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B20 | Pattern step 13 | Pattern step 13 on/off | Pattern Step 13 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B21 | Pattern step 14 | Pattern step 14 on/off | Pattern Step 14 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B22 | Pattern step 15 | Pattern step 15 on/off | Pattern Step 15 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-B23 | Pattern step 16 | Pattern step 16 on/off | Pattern Step 16 | — | display/Remote item, not mapped | tooltip 'Pattern value: 32767' (shown only while Pattern is on; none when off) |
| RPG8-F-D05 | (pattern display) | Shows the notes the arpeggio plays (C-1 to C7) | — | — | click only | pattern grid display, no tooltip seen |
| RPG8-F-B36 | SHUFFLE | Shuffle on/off | Pattern Shuffle | — | display/Remote item, not mapped | tooltip 'Shuffle' |

## RPG-8 Monophonic Arpeggiator — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RPG8-B-D01 | ARP 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | Tape shows 'Arp 1' (device name); no tooltip |
| RPG8-B-K01 | Gate Length (trim) | Amount knob for Gate Length CV In | Gate | — | click/drag only (no Remote item) | tooltip 'Gate: 127' |
| RPG8-B-J01 | Gate Length CV In | CV input: Gate Length CV In | Gate | — | cable: right-click jack > device > jack name | tooltip 'Gate' (empty jack) |
| RPG8-B-K02 | Velocity (trim) | Amount knob for Velocity CV In | Velocity | — | click/drag only (no Remote item) | tooltip 'Velocity: 127' |
| RPG8-B-J04 | Velocity CV In | CV input: Velocity CV In | Velocity | — | cable: right-click jack > device > jack name | tooltip 'Velocity' (empty jack) |
| RPG8-B-K03 | Rate/Resolution (trim) | Amount knob for Rate/Resolution CV In | Rate | — | click/drag only (no Remote item) | tooltip 'Rate: 127' |
| RPG8-B-J07 | Rate/Resolution CV In | CV input: Rate/Resolution CV In | Rate | — | cable: right-click jack > device > jack name | tooltip 'Rate' (empty jack) |
| RPG8-B-K04 | Octave Shift (trim) | Amount knob for Octave Shift CV In | Octave Shift | — | click/drag only (no Remote item) | tooltip 'Octave Shift: 127' |
| RPG8-B-J10 | Octave Shift CV In | CV input: Octave Shift CV In | Octave Shift | — | cable: right-click jack > device > jack name | tooltip 'Octave Shift' (empty jack) |
| RPG8-B-J13 | Start of Arpeggio Trig In | Trigger input: restarts the arpeggio | Restart Arpeggio Trig | — | cable: right-click jack > device > jack name | tooltip 'Restart Arpeggio Trig' (empty jack) |
| RPG8-B-J02 | Gate CV Out (velocity) | Output: Gate CV Out (velocity) | Gate | — | cable: right-click jack > device > jack name | tooltip 'Gate' (empty jack) |
| RPG8-B-J05 | Note CV Out | Output: Note CV Out | Note | — | cable: right-click jack > device > jack name | tooltip 'Note' (empty jack) |
| RPG8-B-J08 | Mod Wheel CV Out | Output: Mod Wheel CV Out | Mod Wheel | — | cable: right-click jack > device > jack name | tooltip 'Mod Wheel' (empty jack) |
| RPG8-B-J11 | Pitch Bend CV Out | Output: Pitch Bend CV Out | Pitch Bend | — | cable: right-click jack > device > jack name | tooltip 'Pitch Bend' (empty jack) |
| RPG8-B-J03 | Aftertouch CV Out | Output: Aftertouch CV Out | Aftertouch | — | cable: right-click jack > device > jack name | tooltip 'Aftertouch' (empty jack) |
| RPG8-B-J06 | Expression CV Out | Output: Expression CV Out | Expression | — | cable: right-click jack > device > jack name | tooltip 'Expression' (empty jack) |
| RPG8-B-J09 | Breath CV Out | Output: Breath CV Out | Breath | — | cable: right-click jack > device > jack name | tooltip 'Breath' (empty jack) |
| RPG8-B-J12 | Start of Arpeggio Trig Out | Output: Start of Arpeggio Trig Out | Start of Arpeggio Trig | — | cable: right-click jack > device > jack name | tooltip 'Start of Arpeggio Trig' (empty jack) |
| RPG8-B-J14 | Sustain Pedal Gate Out (pedal down = open) | Output: Sustain Pedal Gate Out (pedal down = open) | Sustain Pedal Gate | — | cable: right-click jack > device > jack name | tooltip 'Sustain Pedal Gate' (empty jack) |
| RPG8-B-D02 | (CV modulation in use light) | Lit when a CV input is cabled and modulating | — | — | click/drag only (no Remote item) | light, no tooltip (seen: red CV-modulation-in-use lamp) |

## Line Mixer 6:2 — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| LNMX-F-D01 | LINE MIXER 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tape, no tooltip |
| LNMX-F-K02 | Ch 1 AUX | Channel 1 aux send amount (to the Aux Send jacks) | Channel 1 Aux Send | — | display/Remote item, not mapped | tooltip 'Channel 1 Aux Send: 0' |
| LNMX-F-K04 | Ch 1 PAN | Channel 1 pan (left to right) | Channel 1 Pan | — | display/Remote item, not mapped | tooltip 'Channel 1 Pan: 0' |
| LNMX-F-K03 | Ch 1 LEVEL | Channel 1 volume | Channel 1 Level | — | display/Remote item, not mapped | tooltip 'Channel 1 Level: 100' |
| LNMX-F-B01 | Ch 1 Mute | Channel 1 mute button | Channel 1 Mute | — | display/Remote item, not mapped | tooltip 'Channel 1 Mute' |
| LNMX-F-B02 | Ch 1 Solo | Channel 1 solo button | Channel 1 Solo | — | display/Remote item, not mapped | tooltip 'Channel 1 Solo' |
| LNMX-F-D02 | (Ch 1 meter) | Channel 1 level meter | Channel 1 Peak Meter | — | display/Remote item, not mapped | level meter, no tooltip |
| LNMX-F-D10 | Ch 1 name tape | Channel 1 name label (type your own name) | Channel 1 Name | — | display/Remote item, not mapped | name tape, no tooltip |
| LNMX-F-K05 | Ch 2 AUX | Channel 2 aux send amount (to the Aux Send jacks) | Channel 2 Aux Send | — | display/Remote item, not mapped | tooltip 'Channel 2 Aux Send: 0' |
| LNMX-F-K07 | Ch 2 PAN | Channel 2 pan (left to right) | Channel 2 Pan | — | display/Remote item, not mapped | tooltip 'Channel 2 Pan: 0' |
| LNMX-F-K06 | Ch 2 LEVEL | Channel 2 volume | Channel 2 Level | — | display/Remote item, not mapped | tooltip 'Channel 2 Level: 100' |
| LNMX-F-B03 | Ch 2 Mute | Channel 2 mute button | Channel 2 Mute | — | display/Remote item, not mapped | tooltip 'Channel 2 Mute' |
| LNMX-F-B04 | Ch 2 Solo | Channel 2 solo button | Channel 2 Solo | — | display/Remote item, not mapped | tooltip 'Channel 2 Solo' |
| LNMX-F-D03 | (Ch 2 meter) | Channel 2 level meter | Channel 2 Peak Meter | — | display/Remote item, not mapped | level meter, no tooltip |
| LNMX-F-D11 | Ch 2 name tape | Channel 2 name label (type your own name) | Channel 2 Name | — | display/Remote item, not mapped | name tape, no tooltip |
| LNMX-F-K08 | Ch 3 AUX | Channel 3 aux send amount (to the Aux Send jacks) | Channel 3 Aux Send | — | display/Remote item, not mapped | tooltip 'Channel 3 Aux Send: 0' |
| LNMX-F-K10 | Ch 3 PAN | Channel 3 pan (left to right) | Channel 3 Pan | — | display/Remote item, not mapped | tooltip 'Channel 3 Pan: 0' |
| LNMX-F-K09 | Ch 3 LEVEL | Channel 3 volume | Channel 3 Level | — | display/Remote item, not mapped | tooltip 'Channel 3 Level: 100' |
| LNMX-F-B05 | Ch 3 Mute | Channel 3 mute button | Channel 3 Mute | — | display/Remote item, not mapped | tooltip 'Channel 3 Mute' |
| LNMX-F-B06 | Ch 3 Solo | Channel 3 solo button | Channel 3 Solo | — | display/Remote item, not mapped | tooltip 'Channel 3 Solo' |
| LNMX-F-D04 | (Ch 3 meter) | Channel 3 level meter | Channel 3 Peak Meter | — | display/Remote item, not mapped | level meter, no tooltip |
| LNMX-F-D12 | Ch 3 name tape | Channel 3 name label (type your own name) | Channel 3 Name | — | display/Remote item, not mapped | name tape, no tooltip |
| LNMX-F-K11 | Ch 4 AUX | Channel 4 aux send amount (to the Aux Send jacks) | Channel 4 Aux Send | — | display/Remote item, not mapped | tooltip 'Channel 4 Aux Send: 0' |
| LNMX-F-K13 | Ch 4 PAN | Channel 4 pan (left to right) | Channel 4 Pan | — | display/Remote item, not mapped | tooltip 'Channel 4 Pan: 0' |
| LNMX-F-K12 | Ch 4 LEVEL | Channel 4 volume | Channel 4 Level | — | display/Remote item, not mapped | tooltip 'Channel 4 Level: 100' |
| LNMX-F-B07 | Ch 4 Mute | Channel 4 mute button | Channel 4 Mute | — | display/Remote item, not mapped | tooltip 'Channel 4 Mute' |
| LNMX-F-B08 | Ch 4 Solo | Channel 4 solo button | Channel 4 Solo | — | display/Remote item, not mapped | tooltip 'Channel 4 Solo' |
| LNMX-F-D05 | (Ch 4 meter) | Channel 4 level meter | Channel 4 Peak Meter | — | display/Remote item, not mapped | level meter, no tooltip |
| LNMX-F-D13 | Ch 4 name tape | Channel 4 name label (type your own name) | Channel 4 Name | — | display/Remote item, not mapped | name tape, no tooltip |
| LNMX-F-K14 | Ch 5 AUX | Channel 5 aux send amount (to the Aux Send jacks) | Channel 5 Aux Send | — | display/Remote item, not mapped | tooltip 'Channel 5 Aux Send: 0' |
| LNMX-F-K16 | Ch 5 PAN | Channel 5 pan (left to right) | Channel 5 Pan | — | display/Remote item, not mapped | tooltip 'Channel 5 Pan: 0' |
| LNMX-F-K15 | Ch 5 LEVEL | Channel 5 volume | Channel 5 Level | — | display/Remote item, not mapped | tooltip 'Channel 5 Level: 100' |
| LNMX-F-B09 | Ch 5 Mute | Channel 5 mute button | Channel 5 Mute | — | display/Remote item, not mapped | tooltip 'Channel 5 Mute' |
| LNMX-F-B10 | Ch 5 Solo | Channel 5 solo button | Channel 5 Solo | — | display/Remote item, not mapped | tooltip 'Channel 5 Solo' |
| LNMX-F-D06 | (Ch 5 meter) | Channel 5 level meter | Channel 5 Peak Meter | — | display/Remote item, not mapped | level meter, no tooltip |
| LNMX-F-D14 | Ch 5 name tape | Channel 5 name label (type your own name) | Channel 5 Name | — | display/Remote item, not mapped | name tape, no tooltip |
| LNMX-F-K17 | Ch 6 AUX | Channel 6 aux send amount (to the Aux Send jacks) | Channel 6 Aux Send | — | display/Remote item, not mapped | tooltip 'Channel 6 Aux Send: 0' |
| LNMX-F-K19 | Ch 6 PAN | Channel 6 pan (left to right) | Channel 6 Pan | — | display/Remote item, not mapped | tooltip 'Channel 6 Pan: 0' |
| LNMX-F-K18 | Ch 6 LEVEL | Channel 6 volume | Channel 6 Level | — | display/Remote item, not mapped | tooltip 'Channel 6 Level: 100' |
| LNMX-F-B11 | Ch 6 Mute | Channel 6 mute button | Channel 6 Mute | — | display/Remote item, not mapped | tooltip 'Channel 6 Mute' |
| LNMX-F-B12 | Ch 6 Solo | Channel 6 solo button | Channel 6 Solo | — | display/Remote item, not mapped | tooltip 'Channel 6 Solo' |
| LNMX-F-D07 | (Ch 6 meter) | Channel 6 level meter | Channel 6 Peak Meter | — | display/Remote item, not mapped | level meter, no tooltip |
| LNMX-F-D15 | Ch 6 name tape | Channel 6 name label (type your own name) | Channel 6 Name | — | display/Remote item, not mapped | name tape, no tooltip |
| LNMX-F-K01 | AUX RETURN | Level of the signal coming back in at the Aux Return jacks | Aux Return Level | — | display/Remote item, not mapped | tooltip 'Aux Return Level: 100' |
| LNMX-F-K20 | MASTER | Master volume of the mixer | Master Level | — | display/Remote item, not mapped | tooltip 'Master Level: 100' |
| LNMX-F-D08 | (Master meter L) | Master output meter, left | Master Left Peak Meter | — | display/Remote item, not mapped | master meter L, no tooltip |
| LNMX-F-D09 | (Master meter R) | Master output meter, right | Master Right Peak Meter | — | display/Remote item, not mapped | master meter R, no tooltip |

## Line Mixer 6:2 — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| LNMX-B-D01 | LINE MIXER 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | tape, no tooltip |
| LNMX-B-J01 | Ch 1 in L | Channel 1 audio input, left (L/Mono) | Channel 1 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 1 Left' (empty jack) |
| LNMX-B-J09 | Ch 1 in R | Channel 1 audio input, right | Channel 1 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 1 Right' (empty jack) |
| LNMX-B-K01 | Ch 1 Pan CV trim | Amount knob for the Channel 1 Pan CV input | — | — | click/drag only (no Remote item) | tooltip 'Channel 1 Pan CV: 127' |
| LNMX-B-J10 | Ch 1 Pan CV in | Channel 1 pan CV input | Channel 1 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 1 Pan CV' (empty jack) |
| LNMX-B-J02 | Ch 2 in L | Channel 2 audio input, left (L/Mono) | Channel 2 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 2 Left' (empty jack) |
| LNMX-B-J11 | Ch 2 in R | Channel 2 audio input, right | Channel 2 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 2 Right' (empty jack) |
| LNMX-B-K02 | Ch 2 Pan CV trim | Amount knob for the Channel 2 Pan CV input | — | — | click/drag only (no Remote item) | tooltip 'Channel 2 Pan CV: 127' |
| LNMX-B-J12 | Ch 2 Pan CV in | Channel 2 pan CV input | Channel 2 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 2 Pan CV' (empty jack) |
| LNMX-B-J03 | Ch 3 in L | Channel 3 audio input, left (L/Mono) | Channel 3 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 3 Left' (empty jack) |
| LNMX-B-J13 | Ch 3 in R | Channel 3 audio input, right | Channel 3 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 3 Right' (empty jack) |
| LNMX-B-K03 | Ch 3 Pan CV trim | Amount knob for the Channel 3 Pan CV input | — | — | click/drag only (no Remote item) | tooltip 'Channel 3 Pan CV: 127' |
| LNMX-B-J14 | Ch 3 Pan CV in | Channel 3 pan CV input | Channel 3 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 3 Pan CV' (empty jack) |
| LNMX-B-J04 | Ch 4 in L | Channel 4 audio input, left (L/Mono) | Channel 4 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 4 Left' (empty jack) |
| LNMX-B-J15 | Ch 4 in R | Channel 4 audio input, right | Channel 4 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 4 Right' (empty jack) |
| LNMX-B-K04 | Ch 4 Pan CV trim | Amount knob for the Channel 4 Pan CV input | — | — | click/drag only (no Remote item) | tooltip 'Channel 4 Pan CV: 127' |
| LNMX-B-J16 | Ch 4 Pan CV in | Channel 4 pan CV input | Channel 4 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 4 Pan CV' (empty jack) |
| LNMX-B-J05 | Ch 5 in L | Channel 5 audio input, left (L/Mono) | Channel 5 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 5 Left' (empty jack) |
| LNMX-B-J17 | Ch 5 in R | Channel 5 audio input, right | Channel 5 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 5 Right' (empty jack) |
| LNMX-B-K05 | Ch 5 Pan CV trim | Amount knob for the Channel 5 Pan CV input | — | — | click/drag only (no Remote item) | tooltip 'Channel 5 Pan CV: 127' |
| LNMX-B-J18 | Ch 5 Pan CV in | Channel 5 pan CV input | Channel 5 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 5 Pan CV' (empty jack) |
| LNMX-B-J06 | Ch 6 in L | Channel 6 audio input, left (L/Mono) | Channel 6 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 6 Left' (empty jack) |
| LNMX-B-J19 | Ch 6 in R | Channel 6 audio input, right | Channel 6 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 6 Right' (empty jack) |
| LNMX-B-K06 | Ch 6 Pan CV trim | Amount knob for the Channel 6 Pan CV input | — | — | click/drag only (no Remote item) | tooltip 'Channel 6 Pan CV: 127' |
| LNMX-B-J20 | Ch 6 Pan CV in | Channel 6 pan CV input | Channel 6 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 6 Pan CV' (empty jack) |
| LNMX-B-B01 | Aux Pre/Post | Aux send taken before (Pre) or after (Post) the channel fader | Aux Pre/Post | — | click/drag only (no Remote item) | tooltip 'Aux Pre/Post: 0' |
| LNMX-B-J07 | Aux Send L | Aux send output, left | Send Left | — | cable: right-click jack > device > jack name | tooltip 'Send Left' (empty jack) |
| LNMX-B-J21 | Aux Send R | Aux send output, right | Send Right | — | cable: right-click jack > device > jack name | tooltip 'Send Right' (empty jack) |
| LNMX-B-J08 | Aux Return L | Aux return input, left | Return Left | — | cable: right-click jack > device > jack name | tooltip 'Return Left' (empty jack) |
| LNMX-B-J22 | Aux Return R | Aux return input, right | Return Right | — | cable: right-click jack > device > jack name | tooltip 'Return Right' (empty jack) |
| LNMX-B-J23 | Master Out L | Master output, left | Left | — | cable: right-click jack > device > jack name | tooltip 'Left' (empty jack) |
| LNMX-B-J24 | Master Out R | Master output, right | Right | — | cable: right-click jack > device > jack name | tooltip 'Right' (empty jack) |

## Mixer 14:2 — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MX14-F-D04 | MIXER 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tape tooltip 'Mixer 1' (device name) |
| MX14-F-K01 | Ch 1 AUX 1 | Channel 1 aux send 1 | Channel 1 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 1 Aux 1 Send: 0' |
| MX14-F-K17 | Ch 1 AUX 2 | Channel 1 aux send 2 | Channel 1 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 1 Aux 2 Send: 0' |
| MX14-F-K16 | Ch 1 AUX 3 | Channel 1 aux send 3 | Channel 1 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 1 Aux 3 Send: 0' |
| MX14-F-K44 | Ch 1 AUX 4 | Channel 1 aux send 4 | Channel 1 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 1 Aux 4 Send: 0' |
| MX14-F-B01 | Ch 1 P (aux 4 pre) | Channel 1 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 1 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 1 Aux 4 Pre Fader On/Off' |
| MX14-F-B15 | Ch 1 EQ on | Channel 1 EQ on/off | Channel 1 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 1 EQ On/Off' |
| MX14-F-K60 | Ch 1 TREBLE | Channel 1 treble amount | Channel 1 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 1 Treble Amount: 0' |
| MX14-F-K74 | Ch 1 BASS | Channel 1 bass amount | Channel 1 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 1 Bass Amount: 0' |
| MX14-F-B29 | Ch 1 Mute | Channel 1 mute | Channel 1 Mute | — | display/Remote item, not mapped | tooltip 'Channel 1 Mute' |
| MX14-F-B30 | Ch 1 Solo | Channel 1 solo | Channel 1 Solo | — | display/Remote item, not mapped | tooltip 'Channel 1 Solo' |
| MX14-F-K89 | Ch 1 PAN | Channel 1 pan (left to right) | Channel 1 Pan | — | display/Remote item, not mapped | tooltip 'Channel 1 Pan: 0' |
| MX14-F-S01 | Ch 1 fader | Channel 1 volume fader | Channel 1 Level | — | display/Remote item, not mapped | tooltip 'Channel 1 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D07 | (Ch 1 meter) | Channel 1 level meter | Channel 1 Peak Meter | — | display/Remote item, not mapped | level meter, no tooltip |
| MX14-F-D06 | Ch 1 name tape | Channel 1 name label (type your own name) | Channel 1 Name | — | display/Remote item, not mapped | name tape, no tooltip |
| MX14-F-K02 | Ch 2 AUX 1 | Channel 2 aux send 1 | Channel 2 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 2 Aux 1 Send: 0' |
| MX14-F-K19 | Ch 2 AUX 2 | Channel 2 aux send 2 | Channel 2 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 2 Aux 2 Send: 0' |
| MX14-F-K18 | Ch 2 AUX 3 | Channel 2 aux send 3 | Channel 2 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 2 Aux 3 Send: 0' |
| MX14-F-K45 | Ch 2 AUX 4 | Channel 2 aux send 4 | Channel 2 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 2 Aux 4 Send: 0' |
| MX14-F-B02 | Ch 2 P (aux 4 pre) | Channel 2 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 2 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 2 Aux 4 Pre Fader On/Off' |
| MX14-F-B16 | Ch 2 EQ on | Channel 2 EQ on/off | Channel 2 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 2 EQ On/Off' |
| MX14-F-K61 | Ch 2 TREBLE | Channel 2 treble amount | Channel 2 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 2 Treble Amount: 0' |
| MX14-F-K75 | Ch 2 BASS | Channel 2 bass amount | Channel 2 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 2 Bass Amount: 0' |
| MX14-F-B31 | Ch 2 Mute | Channel 2 mute | Channel 2 Mute | — | display/Remote item, not mapped | tooltip 'Channel 2 Mute' |
| MX14-F-B32 | Ch 2 Solo | Channel 2 solo | Channel 2 Solo | — | display/Remote item, not mapped | tooltip 'Channel 2 Solo' |
| MX14-F-K90 | Ch 2 PAN | Channel 2 pan (left to right) | Channel 2 Pan | — | display/Remote item, not mapped | tooltip 'Channel 2 Pan: 0' |
| MX14-F-S02 | Ch 2 fader | Channel 2 volume fader | Channel 2 Level | — | display/Remote item, not mapped | tooltip 'Channel 2 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D09 | (Ch 2 meter) | Channel 2 level meter | Channel 2 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D08 | Ch 2 name tape | Channel 2 name label (type your own name) | Channel 2 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K03 | Ch 3 AUX 1 | Channel 3 aux send 1 | Channel 3 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 3 Aux 1 Send: 0' |
| MX14-F-K21 | Ch 3 AUX 2 | Channel 3 aux send 2 | Channel 3 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 3 Aux 2 Send: 0' |
| MX14-F-K20 | Ch 3 AUX 3 | Channel 3 aux send 3 | Channel 3 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 3 Aux 3 Send: 0' |
| MX14-F-K46 | Ch 3 AUX 4 | Channel 3 aux send 4 | Channel 3 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 3 Aux 4 Send: 0' |
| MX14-F-B03 | Ch 3 P (aux 4 pre) | Channel 3 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 3 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 3 Aux 4 Pre Fader On/Off' |
| MX14-F-B17 | Ch 3 EQ on | Channel 3 EQ on/off | Channel 3 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 3 EQ On/Off' |
| MX14-F-K62 | Ch 3 TREBLE | Channel 3 treble amount | Channel 3 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 3 Treble Amount: 0' |
| MX14-F-K76 | Ch 3 BASS | Channel 3 bass amount | Channel 3 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 3 Bass Amount: 0' |
| MX14-F-B33 | Ch 3 Mute | Channel 3 mute | Channel 3 Mute | — | display/Remote item, not mapped | tooltip 'Channel 3 Mute' |
| MX14-F-B34 | Ch 3 Solo | Channel 3 solo | Channel 3 Solo | — | display/Remote item, not mapped | tooltip 'Channel 3 Solo' |
| MX14-F-K91 | Ch 3 PAN | Channel 3 pan (left to right) | Channel 3 Pan | — | display/Remote item, not mapped | tooltip 'Channel 3 Pan: 0' |
| MX14-F-S03 | Ch 3 fader | Channel 3 volume fader | Channel 3 Level | — | display/Remote item, not mapped | tooltip 'Channel 3 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D11 | (Ch 3 meter) | Channel 3 level meter | Channel 3 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D10 | Ch 3 name tape | Channel 3 name label (type your own name) | Channel 3 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K04 | Ch 4 AUX 1 | Channel 4 aux send 1 | Channel 4 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 4 Aux 1 Send: 0' |
| MX14-F-K23 | Ch 4 AUX 2 | Channel 4 aux send 2 | Channel 4 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 4 Aux 2 Send: 0' |
| MX14-F-K22 | Ch 4 AUX 3 | Channel 4 aux send 3 | Channel 4 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 4 Aux 3 Send: 0' |
| MX14-F-K47 | Ch 4 AUX 4 | Channel 4 aux send 4 | Channel 4 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 4 Aux 4 Send: 0' |
| MX14-F-B04 | Ch 4 P (aux 4 pre) | Channel 4 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 4 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 4 Aux 4 Pre Fader On/Off' |
| MX14-F-B18 | Ch 4 EQ on | Channel 4 EQ on/off | Channel 4 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 4 EQ On/Off' |
| MX14-F-K63 | Ch 4 TREBLE | Channel 4 treble amount | Channel 4 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 4 Treble Amount: 0' |
| MX14-F-K77 | Ch 4 BASS | Channel 4 bass amount | Channel 4 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 4 Bass Amount: 0' |
| MX14-F-B35 | Ch 4 Mute | Channel 4 mute | Channel 4 Mute | — | display/Remote item, not mapped | tooltip 'Channel 4 Mute' |
| MX14-F-B36 | Ch 4 Solo | Channel 4 solo | Channel 4 Solo | — | display/Remote item, not mapped | tooltip 'Channel 4 Solo' |
| MX14-F-K92 | Ch 4 PAN | Channel 4 pan (left to right) | Channel 4 Pan | — | display/Remote item, not mapped | tooltip 'Channel 4 Pan: 0' |
| MX14-F-S04 | Ch 4 fader | Channel 4 volume fader | Channel 4 Level | — | display/Remote item, not mapped | tooltip 'Channel 4 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D13 | (Ch 4 meter) | Channel 4 level meter | Channel 4 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D12 | Ch 4 name tape | Channel 4 name label (type your own name) | Channel 4 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K05 | Ch 5 AUX 1 | Channel 5 aux send 1 | Channel 5 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 5 Aux 1 Send: 0' |
| MX14-F-K25 | Ch 5 AUX 2 | Channel 5 aux send 2 | Channel 5 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 5 Aux 2 Send: 0' |
| MX14-F-K24 | Ch 5 AUX 3 | Channel 5 aux send 3 | Channel 5 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 5 Aux 3 Send: 0' |
| MX14-F-K48 | Ch 5 AUX 4 | Channel 5 aux send 4 | Channel 5 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 5 Aux 4 Send: 0' |
| MX14-F-B05 | Ch 5 P (aux 4 pre) | Channel 5 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 5 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 5 Aux 4 Pre Fader On/Off' |
| MX14-F-B19 | Ch 5 EQ on | Channel 5 EQ on/off | Channel 5 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 5 EQ On/Off' |
| MX14-F-K64 | Ch 5 TREBLE | Channel 5 treble amount | Channel 5 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 5 Treble Amount: 0' |
| MX14-F-K78 | Ch 5 BASS | Channel 5 bass amount | Channel 5 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 5 Bass Amount: 0' |
| MX14-F-B37 | Ch 5 Mute | Channel 5 mute | Channel 5 Mute | — | display/Remote item, not mapped | tooltip 'Channel 5 Mute' |
| MX14-F-B38 | Ch 5 Solo | Channel 5 solo | Channel 5 Solo | — | display/Remote item, not mapped | tooltip 'Channel 5 Solo' |
| MX14-F-K93 | Ch 5 PAN | Channel 5 pan (left to right) | Channel 5 Pan | — | display/Remote item, not mapped | tooltip 'Channel 5 Pan: 0' |
| MX14-F-S05 | Ch 5 fader | Channel 5 volume fader | Channel 5 Level | — | display/Remote item, not mapped | tooltip 'Channel 5 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D15 | (Ch 5 meter) | Channel 5 level meter | Channel 5 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D14 | Ch 5 name tape | Channel 5 name label (type your own name) | Channel 5 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K06 | Ch 6 AUX 1 | Channel 6 aux send 1 | Channel 6 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 6 Aux 1 Send: 0' |
| MX14-F-K27 | Ch 6 AUX 2 | Channel 6 aux send 2 | Channel 6 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 6 Aux 2 Send: 0' |
| MX14-F-K26 | Ch 6 AUX 3 | Channel 6 aux send 3 | Channel 6 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 6 Aux 3 Send: 0' |
| MX14-F-K49 | Ch 6 AUX 4 | Channel 6 aux send 4 | Channel 6 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 6 Aux 4 Send: 0' |
| MX14-F-B06 | Ch 6 P (aux 4 pre) | Channel 6 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 6 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 6 Aux 4 Pre Fader On/Off' |
| MX14-F-B20 | Ch 6 EQ on | Channel 6 EQ on/off | Channel 6 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 6 EQ On/Off' |
| MX14-F-K65 | Ch 6 TREBLE | Channel 6 treble amount | Channel 6 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 6 Treble Amount: 0' |
| MX14-F-K79 | Ch 6 BASS | Channel 6 bass amount | Channel 6 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 6 Bass Amount: 0' |
| MX14-F-B39 | Ch 6 Mute | Channel 6 mute | Channel 6 Mute | — | display/Remote item, not mapped | tooltip 'Channel 6 Mute' |
| MX14-F-B40 | Ch 6 Solo | Channel 6 solo | Channel 6 Solo | — | display/Remote item, not mapped | tooltip 'Channel 6 Solo' |
| MX14-F-K94 | Ch 6 PAN | Channel 6 pan (left to right) | Channel 6 Pan | — | display/Remote item, not mapped | tooltip 'Channel 6 Pan: 0' |
| MX14-F-S06 | Ch 6 fader | Channel 6 volume fader | Channel 6 Level | — | display/Remote item, not mapped | tooltip 'Channel 6 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D17 | (Ch 6 meter) | Channel 6 level meter | Channel 6 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D16 | Ch 6 name tape | Channel 6 name label (type your own name) | Channel 6 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K07 | Ch 7 AUX 1 | Channel 7 aux send 1 | Channel 7 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 7 Aux 1 Send: 0' |
| MX14-F-K29 | Ch 7 AUX 2 | Channel 7 aux send 2 | Channel 7 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 7 Aux 2 Send: 0' |
| MX14-F-K28 | Ch 7 AUX 3 | Channel 7 aux send 3 | Channel 7 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 7 Aux 3 Send: 0' |
| MX14-F-K50 | Ch 7 AUX 4 | Channel 7 aux send 4 | Channel 7 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 7 Aux 4 Send: 0' |
| MX14-F-B07 | Ch 7 P (aux 4 pre) | Channel 7 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 7 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 7 Aux 4 Pre Fader On/Off' |
| MX14-F-B21 | Ch 7 EQ on | Channel 7 EQ on/off | Channel 7 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 7 EQ On/Off' |
| MX14-F-K66 | Ch 7 TREBLE | Channel 7 treble amount | Channel 7 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 7 Treble Amount: 0' |
| MX14-F-K80 | Ch 7 BASS | Channel 7 bass amount | Channel 7 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 7 Bass Amount: 0' |
| MX14-F-B41 | Ch 7 Mute | Channel 7 mute | Channel 7 Mute | — | display/Remote item, not mapped | tooltip 'Channel 7 Mute' |
| MX14-F-B42 | Ch 7 Solo | Channel 7 solo | Channel 7 Solo | — | display/Remote item, not mapped | tooltip 'Channel 7 Solo' |
| MX14-F-K95 | Ch 7 PAN | Channel 7 pan (left to right) | Channel 7 Pan | — | display/Remote item, not mapped | tooltip 'Channel 7 Pan: 0' |
| MX14-F-S07 | Ch 7 fader | Channel 7 volume fader | Channel 7 Level | — | display/Remote item, not mapped | tooltip 'Channel 7 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D19 | (Ch 7 meter) | Channel 7 level meter | Channel 7 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D18 | Ch 7 name tape | Channel 7 name label (type your own name) | Channel 7 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K08 | Ch 8 AUX 1 | Channel 8 aux send 1 | Channel 8 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 8 Aux 1 Send: 0' |
| MX14-F-K31 | Ch 8 AUX 2 | Channel 8 aux send 2 | Channel 8 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 8 Aux 2 Send: 0' |
| MX14-F-K30 | Ch 8 AUX 3 | Channel 8 aux send 3 | Channel 8 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 8 Aux 3 Send: 0' |
| MX14-F-K51 | Ch 8 AUX 4 | Channel 8 aux send 4 | Channel 8 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 8 Aux 4 Send: 0' |
| MX14-F-B08 | Ch 8 P (aux 4 pre) | Channel 8 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 8 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 8 Aux 4 Pre Fader On/Off' |
| MX14-F-B22 | Ch 8 EQ on | Channel 8 EQ on/off | Channel 8 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 8 EQ On/Off' |
| MX14-F-K67 | Ch 8 TREBLE | Channel 8 treble amount | Channel 8 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 8 Treble Amount: 0' |
| MX14-F-K81 | Ch 8 BASS | Channel 8 bass amount | Channel 8 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 8 Bass Amount: 0' |
| MX14-F-B43 | Ch 8 Mute | Channel 8 mute | Channel 8 Mute | — | display/Remote item, not mapped | tooltip 'Channel 8 Mute' |
| MX14-F-B44 | Ch 8 Solo | Channel 8 solo | Channel 8 Solo | — | display/Remote item, not mapped | tooltip 'Channel 8 Solo' |
| MX14-F-K96 | Ch 8 PAN | Channel 8 pan (left to right) | Channel 8 Pan | — | display/Remote item, not mapped | tooltip 'Channel 8 Pan: 0' |
| MX14-F-S08 | Ch 8 fader | Channel 8 volume fader | Channel 8 Level | — | display/Remote item, not mapped | tooltip 'Channel 8 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D21 | (Ch 8 meter) | Channel 8 level meter | Channel 8 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D20 | Ch 8 name tape | Channel 8 name label (type your own name) | Channel 8 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K09 | Ch 9 AUX 1 | Channel 9 aux send 1 | Channel 9 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 9 Aux 1 Send: 0' |
| MX14-F-K33 | Ch 9 AUX 2 | Channel 9 aux send 2 | Channel 9 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 9 Aux 2 Send: 0' |
| MX14-F-K32 | Ch 9 AUX 3 | Channel 9 aux send 3 | Channel 9 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 9 Aux 3 Send: 0' |
| MX14-F-K52 | Ch 9 AUX 4 | Channel 9 aux send 4 | Channel 9 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 9 Aux 4 Send: 0' |
| MX14-F-B09 | Ch 9 P (aux 4 pre) | Channel 9 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 9 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 9 Aux 4 Pre Fader On/Off' |
| MX14-F-B23 | Ch 9 EQ on | Channel 9 EQ on/off | Channel 9 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 9 EQ On/Off' |
| MX14-F-K68 | Ch 9 TREBLE | Channel 9 treble amount | Channel 9 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 9 Treble Amount: 0' |
| MX14-F-K82 | Ch 9 BASS | Channel 9 bass amount | Channel 9 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 9 Bass Amount: 0' |
| MX14-F-B45 | Ch 9 Mute | Channel 9 mute | Channel 9 Mute | — | display/Remote item, not mapped | tooltip 'Channel 9 Mute' |
| MX14-F-B46 | Ch 9 Solo | Channel 9 solo | Channel 9 Solo | — | display/Remote item, not mapped | tooltip 'Channel 9 Solo' |
| MX14-F-K97 | Ch 9 PAN | Channel 9 pan (left to right) | Channel 9 Pan | — | display/Remote item, not mapped | tooltip 'Channel 9 Pan: 0' |
| MX14-F-S09 | Ch 9 fader | Channel 9 volume fader | Channel 9 Level | — | display/Remote item, not mapped | tooltip 'Channel 9 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D23 | (Ch 9 meter) | Channel 9 level meter | Channel 9 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D22 | Ch 9 name tape | Channel 9 name label (type your own name) | Channel 9 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K10 | Ch 10 AUX 1 | Channel 10 aux send 1 | Channel 10 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 10 Aux 1 Send: 0' |
| MX14-F-K35 | Ch 10 AUX 2 | Channel 10 aux send 2 | Channel 10 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 10 Aux 2 Send: 0' |
| MX14-F-K34 | Ch 10 AUX 3 | Channel 10 aux send 3 | Channel 10 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 10 Aux 3 Send: 0' |
| MX14-F-K53 | Ch 10 AUX 4 | Channel 10 aux send 4 | Channel 10 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 10 Aux 4 Send: 0' |
| MX14-F-B10 | Ch 10 P (aux 4 pre) | Channel 10 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 10 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 10 Aux 4 Pre Fader On/Off' |
| MX14-F-B24 | Ch 10 EQ on | Channel 10 EQ on/off | Channel 10 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 10 EQ On/Off' |
| MX14-F-K69 | Ch 10 TREBLE | Channel 10 treble amount | Channel 10 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 10 Treble Amount: 0' |
| MX14-F-K83 | Ch 10 BASS | Channel 10 bass amount | Channel 10 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 10 Bass Amount: 0' |
| MX14-F-B47 | Ch 10 Mute | Channel 10 mute | Channel 10 Mute | — | display/Remote item, not mapped | tooltip 'Channel 10 Mute' |
| MX14-F-B48 | Ch 10 Solo | Channel 10 solo | Channel 10 Solo | — | display/Remote item, not mapped | tooltip 'Channel 10 Solo' |
| MX14-F-K98 | Ch 10 PAN | Channel 10 pan (left to right) | Channel 10 Pan | — | display/Remote item, not mapped | tooltip 'Channel 10 Pan: 0' |
| MX14-F-S10 | Ch 10 fader | Channel 10 volume fader | Channel 10 Level | — | display/Remote item, not mapped | tooltip 'Channel 10 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D25 | (Ch 10 meter) | Channel 10 level meter | Channel 10 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D24 | Ch 10 name tape | Channel 10 name label (type your own name) | Channel 10 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K11 | Ch 11 AUX 1 | Channel 11 aux send 1 | Channel 11 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 11 Aux 1 Send: 0' |
| MX14-F-K37 | Ch 11 AUX 2 | Channel 11 aux send 2 | Channel 11 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 11 Aux 2 Send: 0' |
| MX14-F-K36 | Ch 11 AUX 3 | Channel 11 aux send 3 | Channel 11 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 11 Aux 3 Send: 0' |
| MX14-F-K54 | Ch 11 AUX 4 | Channel 11 aux send 4 | Channel 11 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 11 Aux 4 Send: 0' |
| MX14-F-B11 | Ch 11 P (aux 4 pre) | Channel 11 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 11 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 11 Aux 4 Pre Fader On/Off' |
| MX14-F-B25 | Ch 11 EQ on | Channel 11 EQ on/off | Channel 11 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 11 EQ On/Off' |
| MX14-F-K70 | Ch 11 TREBLE | Channel 11 treble amount | Channel 11 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 11 Treble Amount: 0' |
| MX14-F-K84 | Ch 11 BASS | Channel 11 bass amount | Channel 11 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 11 Bass Amount: 0' |
| MX14-F-B49 | Ch 11 Mute | Channel 11 mute | Channel 11 Mute | — | display/Remote item, not mapped | tooltip 'Channel 11 Mute' |
| MX14-F-B50 | Ch 11 Solo | Channel 11 solo | Channel 11 Solo | — | display/Remote item, not mapped | tooltip 'Channel 11 Solo' |
| MX14-F-K99 | Ch 11 PAN | Channel 11 pan (left to right) | Channel 11 Pan | — | display/Remote item, not mapped | tooltip 'Channel 11 Pan: 0' |
| MX14-F-S11 | Ch 11 fader | Channel 11 volume fader | Channel 11 Level | — | display/Remote item, not mapped | tooltip 'Channel 11 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D27 | (Ch 11 meter) | Channel 11 level meter | Channel 11 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D26 | Ch 11 name tape | Channel 11 name label (type your own name) | Channel 11 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K12 | Ch 12 AUX 1 | Channel 12 aux send 1 | Channel 12 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 12 Aux 1 Send: 0' |
| MX14-F-K39 | Ch 12 AUX 2 | Channel 12 aux send 2 | Channel 12 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 12 Aux 2 Send: 0' |
| MX14-F-K38 | Ch 12 AUX 3 | Channel 12 aux send 3 | Channel 12 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 12 Aux 3 Send: 0' |
| MX14-F-K55 | Ch 12 AUX 4 | Channel 12 aux send 4 | Channel 12 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 12 Aux 4 Send: 0' |
| MX14-F-B12 | Ch 12 P (aux 4 pre) | Channel 12 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 12 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 12 Aux 4 Pre Fader On/Off' |
| MX14-F-B26 | Ch 12 EQ on | Channel 12 EQ on/off | Channel 12 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 12 EQ On/Off' |
| MX14-F-K71 | Ch 12 TREBLE | Channel 12 treble amount | Channel 12 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 12 Treble Amount: 0' |
| MX14-F-K85 | Ch 12 BASS | Channel 12 bass amount | Channel 12 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 12 Bass Amount: 0' |
| MX14-F-B51 | Ch 12 Mute | Channel 12 mute | Channel 12 Mute | — | display/Remote item, not mapped | tooltip 'Channel 12 Mute' |
| MX14-F-B52 | Ch 12 Solo | Channel 12 solo | Channel 12 Solo | — | display/Remote item, not mapped | tooltip 'Channel 12 Solo' |
| MX14-F-K100 | Ch 12 PAN | Channel 12 pan (left to right) | Channel 12 Pan | — | display/Remote item, not mapped | tooltip 'Channel 12 Pan: 0' |
| MX14-F-S12 | Ch 12 fader | Channel 12 volume fader | Channel 12 Level | — | display/Remote item, not mapped | tooltip 'Channel 12 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D29 | (Ch 12 meter) | Channel 12 level meter | Channel 12 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D28 | Ch 12 name tape | Channel 12 name label (type your own name) | Channel 12 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K13 | Ch 13 AUX 1 | Channel 13 aux send 1 | Channel 13 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 13 Aux 1 Send: 0' |
| MX14-F-K41 | Ch 13 AUX 2 | Channel 13 aux send 2 | Channel 13 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 13 Aux 2 Send: 0' |
| MX14-F-K40 | Ch 13 AUX 3 | Channel 13 aux send 3 | Channel 13 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 13 Aux 3 Send: 0' |
| MX14-F-K56 | Ch 13 AUX 4 | Channel 13 aux send 4 | Channel 13 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 13 Aux 4 Send: 0' |
| MX14-F-B13 | Ch 13 P (aux 4 pre) | Channel 13 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 13 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 13 Aux 4 Pre Fader On/Off' |
| MX14-F-B27 | Ch 13 EQ on | Channel 13 EQ on/off | Channel 13 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 13 EQ On/Off' |
| MX14-F-K72 | Ch 13 TREBLE | Channel 13 treble amount | Channel 13 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 13 Treble Amount: 0' |
| MX14-F-K86 | Ch 13 BASS | Channel 13 bass amount | Channel 13 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 13 Bass Amount: 0' |
| MX14-F-B53 | Ch 13 Mute | Channel 13 mute | Channel 13 Mute | — | display/Remote item, not mapped | tooltip 'Channel 13 Mute' |
| MX14-F-B54 | Ch 13 Solo | Channel 13 solo | Channel 13 Solo | — | display/Remote item, not mapped | tooltip 'Channel 13 Solo' |
| MX14-F-K101 | Ch 13 PAN | Channel 13 pan (left to right) | Channel 13 Pan | — | display/Remote item, not mapped | tooltip 'Channel 13 Pan: 0' |
| MX14-F-S13 | Ch 13 fader | Channel 13 volume fader | Channel 13 Level | — | display/Remote item, not mapped | tooltip 'Channel 13 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D31 | (Ch 13 meter) | Channel 13 level meter | Channel 13 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D30 | Ch 13 name tape | Channel 13 name label (type your own name) | Channel 13 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K14 | Ch 14 AUX 1 | Channel 14 aux send 1 | Channel 14 Aux 1 Send | — | display/Remote item, not mapped | tooltip 'Channel 14 Aux 1 Send: 0' |
| MX14-F-K43 | Ch 14 AUX 2 | Channel 14 aux send 2 | Channel 14 Aux 2 Send | — | display/Remote item, not mapped | tooltip 'Channel 14 Aux 2 Send: 0' |
| MX14-F-K42 | Ch 14 AUX 3 | Channel 14 aux send 3 | Channel 14 Aux 3 Send | — | display/Remote item, not mapped | tooltip 'Channel 14 Aux 3 Send: 0' |
| MX14-F-K57 | Ch 14 AUX 4 | Channel 14 aux send 4 | Channel 14 Aux 4 Send | — | display/Remote item, not mapped | tooltip 'Channel 14 Aux 4 Send: 0' |
| MX14-F-B14 | Ch 14 P (aux 4 pre) | Channel 14 aux 4 Pre Fader on/off: send 4 is taken before the fader when on | Channel 14 Aux 4 Pre Fader On/Off | — | display/Remote item, not mapped | tooltip 'Channel 14 Aux 4 Pre Fader On/Off' |
| MX14-F-B28 | Ch 14 EQ on | Channel 14 EQ on/off | Channel 14 EQ On/Off | — | display/Remote item, not mapped | tooltip 'Channel 14 EQ On/Off' |
| MX14-F-K73 | Ch 14 TREBLE | Channel 14 treble amount | Channel 14 Treble Amount | — | display/Remote item, not mapped | tooltip 'Channel 14 Treble Amount: 0' |
| MX14-F-K87 | Ch 14 BASS | Channel 14 bass amount | Channel 14 Bass Amount | — | display/Remote item, not mapped | tooltip 'Channel 14 Bass Amount: 0' |
| MX14-F-B55 | Ch 14 Mute | Channel 14 mute | Channel 14 Mute | — | display/Remote item, not mapped | tooltip 'Channel 14 Mute' |
| MX14-F-B56 | Ch 14 Solo | Channel 14 solo | Channel 14 Solo | — | display/Remote item, not mapped | tooltip 'Channel 14 Solo' |
| MX14-F-K102 | Ch 14 PAN | Channel 14 pan (left to right) | Channel 14 Pan | — | display/Remote item, not mapped | tooltip 'Channel 14 Pan: 0' |
| MX14-F-S14 | Ch 14 fader | Channel 14 volume fader | Channel 14 Level | — | display/Remote item, not mapped | tooltip 'Channel 14 Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D33 | (Ch 14 meter) | Channel 14 level meter | Channel 14 Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D32 | Ch 14 name tape | Channel 14 name label (type your own name) | Channel 14 Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K15 | Return 1 level | Level of aux return 1 | Aux 1 Return Level | — | display/Remote item, not mapped | tooltip 'Aux 1 Return Level: 0' |
| MX14-F-D01 | Return 1 name tape | Name label for aux return 1 | Aux 1 Return Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K58 | Return 2 level | Level of aux return 2 | Aux 2 Return Level | — | display/Remote item, not mapped | tooltip 'Aux 2 Return Level: 0' |
| MX14-F-D02 | Return 2 name tape | Name label for aux return 2 | Aux 2 Return Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K59 | Return 3 level | Level of aux return 3 | Aux 3 Return Level | — | display/Remote item, not mapped | tooltip 'Aux 3 Return Level: 0' |
| MX14-F-D03 | Return 3 name tape | Name label for aux return 3 | Aux 3 Return Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-K88 | Return 4 level | Level of aux return 4 | Aux 4 Return Level | — | display/Remote item, not mapped | tooltip 'Aux 4 Return Level: 0' |
| MX14-F-D05 | Return 4 name tape | Name label for aux return 4 | Aux 4 Return Name | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-S15 | MASTER fader | Master volume fader | Master Level | — | display/Remote item, not mapped | tooltip 'Master Level: 100' (shown below the fader strip when hovering the handle) |
| MX14-F-D34 | (Master meter L) | Master output meter, left | Master Left Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |
| MX14-F-D35 | (Master meter R) | Master output meter, right | Master Right Peak Meter | — | display/Remote item, not mapped | meter/name tape, no tooltip |

## Mixer 14:2 — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MX14-B-D01 | MIXER 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | tape tooltip 'Mixer 1' (device name) |
| MX14-B-J01 | Ch 1 in L | Channel 1 audio input, left (L/Mono) | Channel 1 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 1 Left' (empty jack) |
| MX14-B-J21 | Ch 1 in R | Channel 1 audio input, right | Channel 1 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 1 Right' (empty jack) |
| MX14-B-J40 | Ch 1 Level CV in | Channel 1 level CV input | Channel 1 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 1 Level CV' (empty jack) |
| MX14-B-K01 | Ch 1 Level CV trim | Amount knob for Channel 1 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 1 Level CV: 127' |
| MX14-B-J62 | Ch 1 Pan CV in | Channel 1 pan CV input | Channel 1 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 1 Pan CV' (empty jack) |
| MX14-B-K16 | Ch 1 Pan CV trim | Amount knob for Channel 1 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 1 Pan CV: 127' |
| MX14-B-J02 | Ch 2 in L | Channel 2 audio input, left (L/Mono) | Channel 2 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 2 Left' (empty jack) |
| MX14-B-J22 | Ch 2 in R | Channel 2 audio input, right | Channel 2 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 2 Right' (empty jack) |
| MX14-B-J41 | Ch 2 Level CV in | Channel 2 level CV input | Channel 2 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 2 Level CV' (empty jack) |
| MX14-B-K02 | Ch 2 Level CV trim | Amount knob for Channel 2 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 2 Level CV: 127' |
| MX14-B-J63 | Ch 2 Pan CV in | Channel 2 pan CV input | Channel 2 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 2 Pan CV' (empty jack) |
| MX14-B-K17 | Ch 2 Pan CV trim | Amount knob for Channel 2 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 2 Pan CV: 127' |
| MX14-B-J03 | Ch 3 in L | Channel 3 audio input, left (L/Mono) | Channel 3 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 3 Left' (empty jack) |
| MX14-B-J23 | Ch 3 in R | Channel 3 audio input, right | Channel 3 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 3 Right' (empty jack) |
| MX14-B-J42 | Ch 3 Level CV in | Channel 3 level CV input | Channel 3 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 3 Level CV' (empty jack) |
| MX14-B-K03 | Ch 3 Level CV trim | Amount knob for Channel 3 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 3 Level CV: 127' |
| MX14-B-J64 | Ch 3 Pan CV in | Channel 3 pan CV input | Channel 3 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 3 Pan CV' (empty jack) |
| MX14-B-K18 | Ch 3 Pan CV trim | Amount knob for Channel 3 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 3 Pan CV: 127' |
| MX14-B-J04 | Ch 4 in L | Channel 4 audio input, left (L/Mono) | Channel 4 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 4 Left' (empty jack) |
| MX14-B-J24 | Ch 4 in R | Channel 4 audio input, right | Channel 4 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 4 Right' (empty jack) |
| MX14-B-J43 | Ch 4 Level CV in | Channel 4 level CV input | Channel 4 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 4 Level CV' (empty jack) |
| MX14-B-K04 | Ch 4 Level CV trim | Amount knob for Channel 4 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 4 Level CV: 127' |
| MX14-B-J65 | Ch 4 Pan CV in | Channel 4 pan CV input | Channel 4 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 4 Pan CV' (empty jack) |
| MX14-B-K19 | Ch 4 Pan CV trim | Amount knob for Channel 4 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 4 Pan CV: 127' |
| MX14-B-J05 | Ch 5 in L | Channel 5 audio input, left (L/Mono) | Channel 5 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 5 Left' (empty jack) |
| MX14-B-J25 | Ch 5 in R | Channel 5 audio input, right | Channel 5 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 5 Right' (empty jack) |
| MX14-B-J44 | Ch 5 Level CV in | Channel 5 level CV input | Channel 5 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 5 Level CV' (empty jack) |
| MX14-B-K05 | Ch 5 Level CV trim | Amount knob for Channel 5 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 5 Level CV: 127' |
| MX14-B-J66 | Ch 5 Pan CV in | Channel 5 pan CV input | Channel 5 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 5 Pan CV' (empty jack) |
| MX14-B-K20 | Ch 5 Pan CV trim | Amount knob for Channel 5 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 5 Pan CV: 127' |
| MX14-B-J06 | Ch 6 in L | Channel 6 audio input, left (L/Mono) | Channel 6 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 6 Left' (empty jack) |
| MX14-B-J26 | Ch 6 in R | Channel 6 audio input, right | Channel 6 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 6 Right' (empty jack) |
| MX14-B-J45 | Ch 6 Level CV in | Channel 6 level CV input | Channel 6 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 6 Level CV' (empty jack) |
| MX14-B-K06 | Ch 6 Level CV trim | Amount knob for Channel 6 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 6 Level CV: 127' |
| MX14-B-J67 | Ch 6 Pan CV in | Channel 6 pan CV input | Channel 6 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 6 Pan CV' (empty jack) |
| MX14-B-K21 | Ch 6 Pan CV trim | Amount knob for Channel 6 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 6 Pan CV: 127' |
| MX14-B-J07 | Ch 7 in L | Channel 7 audio input, left (L/Mono) | Channel 7 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 7 Left' (empty jack) |
| MX14-B-J27 | Ch 7 in R | Channel 7 audio input, right | Channel 7 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 7 Right' (empty jack) |
| MX14-B-J46 | Ch 7 Level CV in | Channel 7 level CV input | Channel 7 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 7 Level CV' (empty jack) |
| MX14-B-K07 | Ch 7 Level CV trim | Amount knob for Channel 7 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 7 Level CV: 127' |
| MX14-B-J68 | Ch 7 Pan CV in | Channel 7 pan CV input | Channel 7 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 7 Pan CV' (empty jack) |
| MX14-B-K22 | Ch 7 Pan CV trim | Amount knob for Channel 7 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 7 Pan CV: 127' |
| MX14-B-J08 | Ch 8 in L | Channel 8 audio input, left (L/Mono) | Channel 8 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 8 Left' (empty jack) |
| MX14-B-J28 | Ch 8 in R | Channel 8 audio input, right | Channel 8 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 8 Right' (empty jack) |
| MX14-B-J47 | Ch 8 Level CV in | Channel 8 level CV input | Channel 8 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 8 Level CV' (empty jack) |
| MX14-B-K08 | Ch 8 Level CV trim | Amount knob for Channel 8 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 8 Level CV: 127' |
| MX14-B-J69 | Ch 8 Pan CV in | Channel 8 pan CV input | Channel 8 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 8 Pan CV' (empty jack) |
| MX14-B-K23 | Ch 8 Pan CV trim | Amount knob for Channel 8 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 8 Pan CV: 127' |
| MX14-B-J09 | Ch 9 in L | Channel 9 audio input, left (L/Mono) | Channel 9 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 9 Left' (empty jack) |
| MX14-B-J29 | Ch 9 in R | Channel 9 audio input, right | Channel 9 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 9 Right' (empty jack) |
| MX14-B-J48 | Ch 9 Level CV in | Channel 9 level CV input | Channel 9 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 9 Level CV' (empty jack) |
| MX14-B-K09 | Ch 9 Level CV trim | Amount knob for Channel 9 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 9 Level CV: 127' |
| MX14-B-J70 | Ch 9 Pan CV in | Channel 9 pan CV input | Channel 9 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 9 Pan CV' (empty jack) |
| MX14-B-K24 | Ch 9 Pan CV trim | Amount knob for Channel 9 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 9 Pan CV: 127' |
| MX14-B-J10 | Ch 10 in L | Channel 10 audio input, left (L/Mono) | Channel 10 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 10 Left' (empty jack) |
| MX14-B-J30 | Ch 10 in R | Channel 10 audio input, right | Channel 10 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 10 Right' (empty jack) |
| MX14-B-J49 | Ch 10 Level CV in | Channel 10 level CV input | Channel 10 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 10 Level CV' (empty jack) |
| MX14-B-K10 | Ch 10 Level CV trim | Amount knob for Channel 10 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 10 Level CV: 127' |
| MX14-B-J71 | Ch 10 Pan CV in | Channel 10 pan CV input | Channel 10 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 10 Pan CV' (empty jack) |
| MX14-B-K25 | Ch 10 Pan CV trim | Amount knob for Channel 10 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 10 Pan CV: 127' |
| MX14-B-J11 | Ch 11 in L | Channel 11 audio input, left (L/Mono) | Channel 11 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 11 Left' (empty jack) |
| MX14-B-J31 | Ch 11 in R | Channel 11 audio input, right | Channel 11 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 11 Right' (empty jack) |
| MX14-B-J50 | Ch 11 Level CV in | Channel 11 level CV input | Channel 11 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 11 Level CV' (empty jack) |
| MX14-B-K11 | Ch 11 Level CV trim | Amount knob for Channel 11 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 11 Level CV: 127' |
| MX14-B-J72 | Ch 11 Pan CV in | Channel 11 pan CV input | Channel 11 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 11 Pan CV' (empty jack) |
| MX14-B-K26 | Ch 11 Pan CV trim | Amount knob for Channel 11 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 11 Pan CV: 127' |
| MX14-B-J12 | Ch 12 in L | Channel 12 audio input, left (L/Mono) | Channel 12 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 12 Left' (empty jack) |
| MX14-B-J32 | Ch 12 in R | Channel 12 audio input, right | Channel 12 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 12 Right' (empty jack) |
| MX14-B-J51 | Ch 12 Level CV in | Channel 12 level CV input | Channel 12 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 12 Level CV' (empty jack) |
| MX14-B-K12 | Ch 12 Level CV trim | Amount knob for Channel 12 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 12 Level CV: 127' |
| MX14-B-J73 | Ch 12 Pan CV in | Channel 12 pan CV input | Channel 12 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 12 Pan CV' (empty jack) |
| MX14-B-K27 | Ch 12 Pan CV trim | Amount knob for Channel 12 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 12 Pan CV: 127' |
| MX14-B-J13 | Ch 13 in L | Channel 13 audio input, left (L/Mono) | Channel 13 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 13 Left' (empty jack) |
| MX14-B-J33 | Ch 13 in R | Channel 13 audio input, right | Channel 13 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 13 Right' (empty jack) |
| MX14-B-J52 | Ch 13 Level CV in | Channel 13 level CV input | Channel 13 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 13 Level CV' (empty jack) |
| MX14-B-K13 | Ch 13 Level CV trim | Amount knob for Channel 13 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 13 Level CV: 127' |
| MX14-B-J74 | Ch 13 Pan CV in | Channel 13 pan CV input | Channel 13 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 13 Pan CV' (empty jack) |
| MX14-B-K28 | Ch 13 Pan CV trim | Amount knob for Channel 13 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 13 Pan CV: 127' |
| MX14-B-J14 | Ch 14 in L | Channel 14 audio input, left (L/Mono) | Channel 14 Left | — | cable: right-click jack > device > jack name | tooltip 'Channel 14 Left' (empty jack) |
| MX14-B-J34 | Ch 14 in R | Channel 14 audio input, right | Channel 14 Right | — | cable: right-click jack > device > jack name | tooltip 'Channel 14 Right' (empty jack) |
| MX14-B-J53 | Ch 14 Level CV in | Channel 14 level CV input | Channel 14 Level CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 14 Level CV' (empty jack) |
| MX14-B-K14 | Ch 14 Level CV trim | Amount knob for Channel 14 level CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 14 Level CV: 127' |
| MX14-B-J75 | Ch 14 Pan CV in | Channel 14 pan CV input | Channel 14 Pan CV | — | cable: right-click jack > device > jack name | tooltip 'Channel 14 Pan CV' (empty jack) |
| MX14-B-K29 | Ch 14 Pan CV trim | Amount knob for Channel 14 pan CV | — | — | click/drag only (no Remote item) | tooltip 'Channel 14 Pan CV: 127' |
| MX14-B-J15 | Aux 1 send L | Aux 1 send output, left (L/Mono) | Send 1 Left | — | cable: right-click jack > device > jack name | tooltip 'Send 1 Left' (empty jack) |
| MX14-B-J35 | Aux 1 send R | Aux 1 send output, right | Send 1 Right | — | cable: right-click jack > device > jack name | tooltip 'Send 1 Right' (empty jack) |
| MX14-B-J54 | Aux 1 return L | Aux 1 return input, left (L/Mono) | Return 1 Left | — | cable: right-click jack > device > jack name | tooltip 'Return 1 Left' (empty jack) |
| MX14-B-J58 | Aux 1 return R | Aux 1 return input, right | Return 1 Right | — | cable: right-click jack > device > jack name | tooltip 'Return 1 Right' (empty jack) |
| MX14-B-J76 | Aux 1 chain in L | Chaining Aux 1 send input, left (L/Mono) | Aux 1 Chain Left | — | cable: right-click jack > device > jack name | tooltip 'Aux 1 Chain Left' (empty jack) |
| MX14-B-J82 | Aux 1 chain in R | Chaining Aux 1 send input, right | Aux 1 Chain Right | — | cable: right-click jack > device > jack name | tooltip 'Aux 1 Chain Right' (empty jack) |
| MX14-B-J16 | Aux 2 send L | Aux 2 send output, left (L/Mono) | Send 2 Left | — | cable: right-click jack > device > jack name | tooltip 'Send 2 Left' (empty jack) |
| MX14-B-J36 | Aux 2 send R | Aux 2 send output, right | Send 2 Right | — | cable: right-click jack > device > jack name | tooltip 'Send 2 Right' (empty jack) |
| MX14-B-J55 | Aux 2 return L | Aux 2 return input, left (L/Mono) | Return 2 Left | — | cable: right-click jack > device > jack name | tooltip 'Return 2 Left' (empty jack) |
| MX14-B-J59 | Aux 2 return R | Aux 2 return input, right | Return 2 Right | — | cable: right-click jack > device > jack name | tooltip 'Return 2 Right' (empty jack) |
| MX14-B-J77 | Aux 2 chain in L | Chaining Aux 2 send input, left (L/Mono) | Aux 2 Chain Left | — | cable: right-click jack > device > jack name | tooltip 'Aux 2 Chain Left' (empty jack) |
| MX14-B-J83 | Aux 2 chain in R | Chaining Aux 2 send input, right | Aux 2 Chain Right | — | cable: right-click jack > device > jack name | tooltip 'Aux 2 Chain Right' (empty jack) |
| MX14-B-J17 | Aux 3 send L | Aux 3 send output, left (L/Mono) | Send 3 Left | — | cable: right-click jack > device > jack name | tooltip 'Send 3 Left' (empty jack) |
| MX14-B-J37 | Aux 3 send R | Aux 3 send output, right | Send 3 Right | — | cable: right-click jack > device > jack name | tooltip 'Send 3 Right' (empty jack) |
| MX14-B-J56 | Aux 3 return L | Aux 3 return input, left (L/Mono) | Return 3 Left | — | cable: right-click jack > device > jack name | tooltip 'Return 3 Left' (empty jack) |
| MX14-B-J60 | Aux 3 return R | Aux 3 return input, right | Return 3 Right | — | cable: right-click jack > device > jack name | tooltip 'Return 3 Right' (empty jack) |
| MX14-B-J78 | Aux 3 chain in L | Chaining Aux 3 send input, left (L/Mono) | Aux 3 Chain Left | — | cable: right-click jack > device > jack name | tooltip 'Aux 3 Chain Left' (empty jack) |
| MX14-B-J84 | Aux 3 chain in R | Chaining Aux 3 send input, right | Aux 3 Chain Right | — | cable: right-click jack > device > jack name | tooltip 'Aux 3 Chain Right' (empty jack) |
| MX14-B-J18 | Aux 4 send L | Aux 4 send output, left (L/Mono) | Send 4 Left | — | cable: right-click jack > device > jack name | tooltip 'Send 4 Left' (empty jack) |
| MX14-B-J38 | Aux 4 send R | Aux 4 send output, right | Send 4 Right | — | cable: right-click jack > device > jack name | tooltip 'Send 4 Right' (empty jack) |
| MX14-B-J57 | Aux 4 return L | Aux 4 return input, left (L/Mono) | Return 4 Left | — | cable: right-click jack > device > jack name | tooltip 'Return 4 Left' (empty jack) |
| MX14-B-J61 | Aux 4 return R | Aux 4 return input, right | Return 4 Right | — | cable: right-click jack > device > jack name | tooltip 'Return 4 Right' (empty jack) |
| MX14-B-J79 | Aux 4 chain in L | Chaining Aux 4 send input, left (L/Mono) | Aux 4 Chain Left | — | cable: right-click jack > device > jack name | tooltip 'Aux 4 Chain Left' (empty jack) |
| MX14-B-J85 | Aux 4 chain in R | Chaining Aux 4 send input, right | Aux 4 Chain Right | — | cable: right-click jack > device > jack name | tooltip 'Aux 4 Chain Right' (empty jack) |
| MX14-B-J19 | Master out L | Master output, left | Left | — | cable: right-click jack > device > jack name | tooltip 'Connected to Mixer 1: Input L' (cabled); own name 'Left' from the cable menu |
| MX14-B-J20 | Master out R | Master output, right | Right | — | cable: right-click jack > device > jack name | tooltip 'Connected to Mixer 1: Input R' (cabled); own name 'Right' from the cable menu |
| MX14-B-J39 | Master Level CV in | Master level CV input | Master Level CV | — | cable: right-click jack > device > jack name | tooltip 'Master Level CV' (empty jack) |
| MX14-B-K15 | Master Level CV trim | Amount knob for Master level CV | — | — | click/drag only (no Remote item) | tooltip 'Master Level CV: 127' |
| MX14-B-J80 | Chain master L | Chaining master input, left | Chain Left | — | cable: right-click jack > device > jack name | tooltip 'Chain Left' (empty jack) |
| MX14-B-J81 | Chain master R | Chaining master input, right | Chain Right | — | cable: right-click jack > device > jack name | tooltip 'Chain Right' (empty jack) |
| MX14-B-B01 | EQ switch (Compatible/Improved) | Picks the EQ type: Compatible (like the old mixer) or Improved | — | — | click/drag only (no Remote item) | tooltip 'EQ Mode: 0' |

## Mix Channel — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MXCH-F-B01 | (fold triangle) | Fold triangle: folds the device up to a thin strip | — | — | click only | no tooltip (fold triangle) |
| MXCH-F-D01 | Mix Channel name | Channel name label (type your own name) | Channel Name | — | display/Remote item, not mapped | tooltip 'Mix Channel' (channel name) |
| MXCH-F-B07 | Show Insert FX | Opens/closes the insert FX slot under the strip (drop an effect device there) | — | — | click only | tooltip 'Show Insert FX' |
| MXCH-F-B02 | MUTE | Mutes this channel | Mute | — | display/Remote item, not mapped | tooltip 'Mix Channel Mute Off' |
| MXCH-F-B03 | SOLO | Solos this channel | Solo | — | display/Remote item, not mapped | tooltip 'Mix Channel Solo Off' |
| MXCH-F-B08 | BYPASS | Bypasses the insert FX | Bypass Insert FX | — | display/Remote item, not mapped | tooltip 'Bypass Master Insert FX Of...' (cut off at the edge of the zoom; Off) |
| MXCH-F-S01 | Level fader | Channel level (horizontal fader) | Level | — | display/Remote item, not mapped | tooltip 'Level: 0.00 dB' |
| MXCH-F-K01 | PAN | Channel pan (left to right) | Pan | — | display/Remote item, not mapped | tooltip 'Pan: 0' |
| MXCH-F-B04 | SEQ | Shows this channel's sequencer track | — | — | click only | tooltip 'Show Sequencer Track' |
| MXCH-F-B05 | MIX | Shows this channel's mixer strip | — | — | click only | tooltip 'Show Mixer Strip' |
| MXCH-F-B06 | Spectrum EQ button | Shows this channel in the Spectrum EQ window | — | — | click only | tooltip 'Show in Spectrum EQ Windo...' (cut off at the edge of the zoom) |
| MXCH-F-D02 | (level meter) | Channel level meter | — | — | click only | no tooltip (level meter) |
| MXCH-F-B09 | AUDIO OUTPUT menu | Pick where the channel's sound goes (Master Section or another bus) | — | — | click only | no tooltip (output menu; not opened) |
| MXCH-F-B10 | REC SOURCE | Rec Source: marks this channel as a recording source | — | — | click only | tooltip 'Rec Source' |

## Mix Channel — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MXCH-B-B01 | (fold triangle) | Fold triangle (back) | — | — | click/drag only (no Remote item) | no tooltip (fold triangle) |
| MXCH-B-D01 | Mix Channel name | Channel name box (back) | — | — | click/drag only (no Remote item) | tooltip 'Mix Channel' (channel name) |
| MXCH-B-B03 | Show Insert FX | Opens/closes the insert FX slot | — | — | click/drag only (no Remote item) | tooltip 'Show Insert FX' |
| MXCH-B-D03 | (output-bus light) | Lit when the channel is used as an output bus (its input is then disabled) | — | — | click/drag only (no Remote item) | no tooltip (light) |
| MXCH-B-J01 | Input L | Audio input, left (L/Mono) | — | — | cable: right-click jack > device > jack name | tooltip 'Input L' (empty jack) |
| MXCH-B-J06 | Input R | Audio input, right | — | — | cable: right-click jack > device > jack name | tooltip 'Input R' (empty jack) |
| MXCH-B-J02 | Parallel out L | Parallel (pre-insert) output, left | — | — | cable: right-click jack > device > jack name | tooltip 'Parallel Output L' (empty jack) |
| MXCH-B-J07 | Parallel out R | Parallel (pre-insert) output, right | — | — | cable: right-click jack > device > jack name | tooltip 'Parallel Output R' (empty jack) |
| MXCH-B-J03 | Sidechain in L | Sidechain input, left | — | — | cable: right-click jack > device > jack name | tooltip 'Side Chain Input L' (empty jack) |
| MXCH-B-J08 | Sidechain in R | Sidechain input, right | — | — | cable: right-click jack > device > jack name | tooltip 'Side Chain Input R' (empty jack) |
| MXCH-B-B02 | KEY | Sidechain Key on/off | — | — | click/drag only (no Remote item) | tooltip 'Sidechain Key On/Off' |
| MXCH-B-J04 | Gain Reduction CV out | CV output that follows the dynamics gain reduction | — | — | cable: right-click jack > device > jack name | tooltip 'Gain Reduction CV' (empty jack) |
| MXCH-B-D04 | (insert FX slot) | Slot for an insert effect device | — | — | click/drag only (no Remote item) | no tooltip (insert FX slot) |
| MXCH-B-J05 | Direct out L | Direct output, left | — | — | cable: right-click jack > device > jack name | tooltip 'Mix Channel Output L' (empty jack) |
| MXCH-B-J09 | Direct out R | Direct output, right | — | — | cable: right-click jack > device > jack name | tooltip 'Mix Channel Output R' (empty jack) |
| MXCH-B-D02 | (breaks internal mixer routing) | Label: using Direct Out breaks the internal mixer routing | — | — | click/drag only (no Remote item) | no tooltip (label) |
| MXCH-B-D05 | (Audio Output display) | Shows where the channel is routed (Master Section) | — | — | click/drag only (no Remote item) | no tooltip (display) |

## Combinator — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| COMB-F-B01 | (fold triangle) | Fold triangle: folds the Combinator up to a thin strip | — | — | click only | no tooltip (fold triangle) |
| COMB-F-B02 | Bypass/On/Off switch | Bypass / On / Off switch for the whole Combinator | Enabled | — | display/Remote item, not mapped | tooltip 'Enabled: On' |
| COMB-F-D04 | Combinator 1 name tape | Device name label | Device Name | — | display/Remote item, not mapped | tooltip 'Combinator 1' (device name) |
| COMB-F-D01 | (orange LED) | Small orange light next to the Editor button | — | — | click only | no tooltip (orange light) |
| COMB-F-B03 | Editor (Show Programmer) | Opens the Programmer (where the knobs get mapped) | — | — | click only | tooltip 'Show Programmer' |
| COMB-F-B04 | Devices (Show Devices) | Shows the devices inside the Combinator | — | — | click only | tooltip 'Show Devices' |
| COMB-F-D02 | (green meters) | Small green meters left of the patch name | — | — | click only | no tooltip (green meters) |
| COMB-F-D03 | Patch name display | Shows the loaded patch name | Patch Name | — | display/Remote item, not mapped | tooltip 'Init Patch' (patch name) |
| COMB-F-B05 | Patch up/down arrows | Select previous (top half) / next (bottom half) patch | Select Next Patch | — | display/Remote item, not mapped | tooltips: top half 'Select previous patch', bottom half 'Select next patch' |
| COMB-F-B06 | Browse patch (folder) | Opens the patch browser | — | — | click only | tooltip 'Browse patch' |
| COMB-F-B07 | Save patch (disk) | Saves the patch | — | — | click only | tooltip 'Save patch' |
| COMB-F-S01 | PITCH wheel | Pitch bend wheel, passed to all instruments inside | Pitch Bend | — | display/Remote item, not mapped | tooltip 'Pitch Bend: 0' |
| COMB-F-S02 | MOD wheel | Mod wheel, passed to all instruments inside | Mod Wheel | — | display/Remote item, not mapped | tooltip 'Mod Wheel: 0' |
| COMB-F-K01 | Control 1 | Rotary 1: virtual knob, does nothing until mapped in the Programmer | Rotary 1 | 1 / CC 30 | voice/MIDI or click | tooltip 'Control 1: 64' |
| COMB-F-K02 | Control 2 | Rotary 2: virtual knob | Rotary 2 | 2 / CC 31 | voice/MIDI or click | tooltip 'Control 2: 64' |
| COMB-F-K03 | Control 3 | Rotary 3: virtual knob | Rotary 3 | 3 / CC 32 | voice/MIDI or click | tooltip 'Control 3: 64' |
| COMB-F-K04 | Control 4 | Rotary 4: virtual knob | Rotary 4 | 4 / CC 33 | voice/MIDI or click | tooltip 'Control 4: 64' |
| COMB-F-B08 | Switch 1 | Button 1: virtual switch | Button 1 | 5 / CC 34 | voice/MIDI or click | tooltip 'Switch 1' |
| COMB-F-B09 | Switch 2 | Button 2: virtual switch | Button 2 | 6 / CC 35 | voice/MIDI or click | tooltip 'Switch 2' |
| COMB-F-B10 | Switch 3 | Button 3: virtual switch | Button 3 | 7 / CC 36 | voice/MIDI or click | tooltip 'Switch 3' |
| COMB-F-B11 | Switch 4 | Button 4: virtual switch | Button 4 | 8 / CC 37 | voice/MIDI or click | tooltip 'Switch 4' |
| COMB-F-B12 | Mixer fold arrow | Unfolds the built-in Combinator mixer (not mapped here) | — | — | click only | no tooltip (mixer fold arrow) |
| COMB-F-D05 | (mixer channel lights 1-16) | Lights showing which of the 8 stereo inputs of the Combinator mixer are in use | — | — | click only | no tooltip (mixer lights) |

## Combinator — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| COMB-B-B01 | (fold triangle) | Fold triangle (back) | — | — | click/drag only (no Remote item) | no tooltip (fold triangle) |
| COMB-B-B02 | Editor (Show Programmer) | Opens the Programmer | — | — | click/drag only (no Remote item) | tooltip 'Show Programmer' |
| COMB-B-B03 | Devices (Show Devices) | Shows the devices inside | — | — | click/drag only (no Remote item) | tooltip 'Show Devices' |
| COMB-B-J01 | Gate In | Sequencer Control: Mono Gate Input | — | — | cable: right-click jack > device > jack name | tooltip 'Mono Gate Input' (empty jack) |
| COMB-B-J04 | CV In | Sequencer Control: Mono CV Input | — | — | cable: right-click jack > device > jack name | tooltip 'Mono CV Input' (empty jack) |
| COMB-B-K01 | Control CV In 1 trim | Amount knob for Control CV In 1 | — | — | click/drag only (no Remote item) | tooltip 'Control CV In 1: 127' |
| COMB-B-K03 | Control CV In 3 trim | Amount knob for Control CV In 3 | — | — | click/drag only (no Remote item) | tooltip 'Control CV In 3: 127' |
| COMB-B-J02 | Control CV In 1 | Control CV input 1 | — | — | cable: right-click jack > device > jack name | tooltip 'Control CV In 1' (empty jack) |
| COMB-B-J05 | Control CV In 3 | Control CV input 3 | — | — | cable: right-click jack > device > jack name | tooltip 'Control CV In 3' (empty jack) |
| COMB-B-D01 | Control 1 selector | Picks which Combinator control the top-left CV input drives (shows Control 1) | — | — | click/drag only (no Remote item) | no tooltip (selector, not opened) |
| COMB-B-D04 | Control 3 selector | Picks which control the lower-left CV input drives (shows Control 3) | — | — | click/drag only (no Remote item) | no tooltip (selector, not opened) |
| COMB-B-K02 | Control CV In 2 trim | Amount knob for Control CV In 2 | — | — | click/drag only (no Remote item) | tooltip 'Control CV In 2: 127' |
| COMB-B-K04 | Control CV In 4 trim | Amount knob for Control CV In 4 | — | — | click/drag only (no Remote item) | tooltip 'Control CV In 4: 127' |
| COMB-B-J03 | Control CV In 2 | Control CV input 2 | — | — | cable: right-click jack > device > jack name | tooltip 'Control CV In 2' (empty jack) |
| COMB-B-J06 | Control CV In 4 | Control CV input 4 | — | — | cable: right-click jack > device > jack name | tooltip 'Control CV In 4' (empty jack) |
| COMB-B-D02 | Control 2 selector | Picks which control the top-right CV input drives (shows Control 2) | — | — | click/drag only (no Remote item) | no tooltip (selector, not opened) |
| COMB-B-D05 | Control 4 selector | Picks which control the lower-right CV input drives (shows Control 4) | — | — | click/drag only (no Remote item) | no tooltip (selector, not opened) |
| COMB-B-D03 | Combinator 1 name tape | Device name label (back) | — | — | click/drag only (no Remote item) | tooltip 'Combinator 1' (device name) |
| COMB-B-D06 | (name strip) | Dark strip under the name tape | — | — | click/drag only (no Remote item) | no tooltip (dark strip) |
| COMB-B-J07 | Input L | Combi Input Left | — | — | cable: right-click jack > device > jack name | tooltip 'Combi Input Left' (empty jack) |
| COMB-B-J08 | Input R | Combi Input Right | — | — | cable: right-click jack > device > jack name | tooltip 'Combi Input Right' (empty jack) |
| COMB-B-J09 | Output L | Combi Output Left | Combi Output Left | — | cable: right-click jack > device > jack name | tooltip 'Connected to Combinator 1 Combi Output Left+Combi Output Right: Input L' (cabled to the auto-named Mix Channel); own name from cable menu: 'Combi Output Left' |
| COMB-B-J10 | Output R | Combi Output Right | Combi Output Right | — | cable: right-click jack > device > jack name | tooltip 'Connected to Combinator 1 Combi Output Left+Combi Output Right: Input R' (cabled to the auto-named Mix Channel); own name from cable menu: 'Combi Output Right' |
| COMB-B-B04 | Mixer fold arrow | Unfolds the built-in Combinator mixer (back) | — | — | click/drag only (no Remote item) | no tooltip (mixer fold arrow) |

## Audio Track — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AUDT-F-B01 | (fold triangle) | Folds/unfolds this track's device | — | — | click only | no tooltip (fold triangle) |
| AUDT-F-D01 | Audio Track 1 tape | Device (track) name tape | — | — | click only | tooltip 'Audio Track 1' (name tape) |
| AUDT-F-B02 | MUTE | Mutes this track (tooltip 'Audio Track 1 Mute Off') | — | — | click only | tooltip 'Audio Track 1 Mute Off' |
| AUDT-F-B03 | SOLO | Solos this track (tooltip 'Audio Track 1 Solo Off') | — | — | click only | tooltip 'Audio Track 1 Solo Off' |
| AUDT-F-S01 | (level fader) | Track level fader; tooltip 'Level: 0.00 dB' | — | — | click only | tooltip 'Level: 0.00 dB' (hover the handle at about 0.435 across the picture, not the box centre) |
| AUDT-F-K01 | (pan knob) | Track pan; tooltip 'Pan: 0' | — | — | click only | tooltip 'Pan: 0' |
| AUDT-F-B04 | SEQ | Scrolls the sequencer to this track | — | — | click only | tooltip 'Show Sequencer Track' |
| AUDT-F-B05 | MIX | Shows this track's mixer strip | — | — | click only | tooltip 'Show Mixer Strip' |
| AUDT-F-B06 | (curve button) | Opens the spectrum EQ window | — | — | click only | tooltip 'Show in Spectrum EQ Window' |
| AUDT-F-D02 | (level meter) | Track level meter | — | — | click only | no tooltip (level meter) |
| AUDT-F-D03 | AUDIO TRACK label | Device type label | — | — | click only | no tooltip (label) |

## Audio Track — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AUDT-B-B01 | (fold triangle) | Folds/unfolds the device (back) | — | — | click/drag only (no Remote item) | no tooltip (fold triangle) |
| AUDT-B-D01 | Audio Track 1 tape | Device name tape (back) | — | — | click/drag only (no Remote item) | tooltip 'Audio Track 1' (name tape) |
| AUDT-B-D02 | (black slot) | Black slot, no jack or control | — | — | click/drag only (no Remote item) | no tooltip (black slot, no jack) |
| AUDT-B-D03 | AUDIO TRACK label | Device type label (back) | — | — | click/drag only (no Remote item) | no tooltip (label) |

## Hardware Interface — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| HWIF-F-B01 | (fold triangle) | Folds/unfolds the Hardware Interface | — | — | click only | no tooltip |
| HWIF-F-D01 | HARDWARE INTERFACE label | Device name label | — | — | click only | no tooltip |
| HWIF-F-D02 | Active audio driver display | Shows the active audio driver (Scarlett 2i2 USB) | — | — | click only | no tooltip |
| HWIF-F-B02 | AUDIO I/O (button) | Shows/hides the Audio I/O section (1-16 and sampling input) | — | — | click only | Show basic Audio in and outs |
| HWIF-F-B03 | MORE AUDIO (button) | Shows/hides the Audio I/O 17-64 sections | — | — | click only | Show extra Audio ins and outs |
| HWIF-F-B04 | BIG METER (button) | Shows/hides the Big Meter section | — | — | click only | Show Big Meter panel |
| HWIF-F-B05 | ADVANCED MIDI (button) | Shows/hides the Advanced MIDI Device section | — | — | click only | Show MIDI External Control panel |
| HWIF-F-B06 | INPUT FOCUS (light) | Input focus light | — | — | click only | Input Focus |
| HWIF-F-B07 | PLAY FOCUS (light) | Play focus light | — | — | click only | Play Focus |
| HWIF-F-D03 | MIDI SYNC IN (light) | MIDI sync in light | — | — | click only | no tooltip |
| HWIF-F-B08 | Monitor (speaker button) | Sampling input monitor on/off | — | — | click only | Sample Monitoring On/Off |
| HWIF-F-B09 | AUTO (checkbox) | Sampling input monitor Auto | — | — | click only | Automatic Sample Monitoring On/Off |
| HWIF-F-K01 | LEVEL (knob) | Sampling input monitor level | — | — | click only | Sample Monitoring Level: 0.00 dB |
| HWIF-F-D04 | Sampling input meter L/R | Level meter for the sampling input L and R | — | — | click only | Sampling Right Input: in use |
| HWIF-F-B10 | Sampling input (checkbox) | Checkbox under the sampling input meter (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D05 | Audio Input 1-2 meter | Level meter for audio inputs 1 and 2 | — | — | click only | Input 2: in use |
| HWIF-F-B11 | Audio Input 1-2 (checkbox) | Checkbox under the meter for audio inputs 1-2 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D06 | Audio Input 3-4 meter | Level meter for audio inputs 3 and 4 | — | — | click only | Input 4: not available |
| HWIF-F-B12 | Audio Input 3-4 (checkbox) | Checkbox under the meter for audio inputs 3-4 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D07 | Audio Input 5-6 meter | Level meter for audio inputs 5 and 6 | — | — | click only | Input 6: not available |
| HWIF-F-B13 | Audio Input 5-6 (checkbox) | Checkbox under the meter for audio inputs 5-6 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D08 | Audio Input 7-8 meter | Level meter for audio inputs 7 and 8 | — | — | click only | Input 8: not available |
| HWIF-F-B14 | Audio Input 7-8 (checkbox) | Checkbox under the meter for audio inputs 7-8 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D09 | Audio Input 9-10 meter | Level meter for audio inputs 9 and 10 | — | — | click only | Input 10: not available |
| HWIF-F-B15 | Audio Input 9-10 (checkbox) | Checkbox under the meter for audio inputs 9-10 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D10 | Audio Input 11-12 meter | Level meter for audio inputs 11 and 12 | — | — | click only | Input 12: not available |
| HWIF-F-B16 | Audio Input 11-12 (checkbox) | Checkbox under the meter for audio inputs 11-12 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D11 | Audio Input 13-14 meter | Level meter for audio inputs 13 and 14 | — | — | click only | Input 14: not available |
| HWIF-F-B17 | Audio Input 13-14 (checkbox) | Checkbox under the meter for audio inputs 13-14 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D12 | Audio Input 15-16 meter | Level meter for audio inputs 15 and 16 | — | — | click only | Input 16: not available |
| HWIF-F-B18 | Audio Input 15-16 (checkbox) | Checkbox under the meter for audio inputs 15-16 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D13 | Audio Output 1-2 meter | Level meter for audio outputs 1 and 2 | — | — | click only | Output 2: available |
| HWIF-F-B19 | Audio Output 1-2 (checkbox) | Checkbox under the meter for audio outputs 1-2 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D14 | Audio Output 3-4 meter | Level meter for audio outputs 3 and 4 | — | — | click only | Output 4: not available |
| HWIF-F-B20 | Audio Output 3-4 (checkbox) | Checkbox under the meter for audio outputs 3-4 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D15 | Audio Output 5-6 meter | Level meter for audio outputs 5 and 6 | — | — | click only | Output 6: not available |
| HWIF-F-B21 | Audio Output 5-6 (checkbox) | Checkbox under the meter for audio outputs 5-6 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D16 | Audio Output 7-8 meter | Level meter for audio outputs 7 and 8 | — | — | click only | Output 7: not available |
| HWIF-F-B22 | Audio Output 7-8 (checkbox) | Checkbox under the meter for audio outputs 7-8 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D17 | Audio Output 9-10 meter | Level meter for audio outputs 9 and 10 | — | — | click only | Output 10: not available |
| HWIF-F-B23 | Audio Output 9-10 (checkbox) | Checkbox under the meter for audio outputs 9-10 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D18 | Audio Output 11-12 meter | Level meter for audio outputs 11 and 12 | — | — | click only | Output 12: not available |
| HWIF-F-B24 | Audio Output 11-12 (checkbox) | Checkbox under the meter for audio outputs 11-12 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D19 | Audio Output 13-14 meter | Level meter for audio outputs 13 and 14 | — | — | click only | Output 14: not available |
| HWIF-F-B25 | Audio Output 13-14 (checkbox) | Checkbox under the meter for audio outputs 13-14 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D20 | Audio Output 15-16 meter | Level meter for audio outputs 15 and 16 | — | — | click only | Output 16: not available |
| HWIF-F-B26 | Audio Output 15-16 (checkbox) | Checkbox under the meter for audio outputs 15-16 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D21 | Audio Input 17-18 meter | Level meter for audio inputs 17 and 18 | — | — | click only | Input 18: not available |
| HWIF-F-B27 | Audio Input 17-18 (checkbox) | Checkbox under the meter for audio inputs 17-18 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D22 | Audio Input 19-20 meter | Level meter for audio inputs 19 and 20 | — | — | click only | Input 20: not available |
| HWIF-F-B28 | Audio Input 19-20 (checkbox) | Checkbox under the meter for audio inputs 19-20 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D23 | Audio Input 21-22 meter | Level meter for audio inputs 21 and 22 | — | — | click only | Input 22: not available |
| HWIF-F-B29 | Audio Input 21-22 (checkbox) | Checkbox under the meter for audio inputs 21-22 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D24 | Audio Input 23-24 meter | Level meter for audio inputs 23 and 24 | — | — | click only | Input 24: not available |
| HWIF-F-B30 | Audio Input 23-24 (checkbox) | Checkbox under the meter for audio inputs 23-24 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D25 | Audio Input 25-26 meter | Level meter for audio inputs 25 and 26 | — | — | click only | Input 26: not available |
| HWIF-F-B31 | Audio Input 25-26 (checkbox) | Checkbox under the meter for audio inputs 25-26 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D26 | Audio Input 27-28 meter | Level meter for audio inputs 27 and 28 | — | — | click only | Input 28: not available |
| HWIF-F-B32 | Audio Input 27-28 (checkbox) | Checkbox under the meter for audio inputs 27-28 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D27 | Audio Input 29-30 meter | Level meter for audio inputs 29 and 30 | — | — | click only | Input 30: not available |
| HWIF-F-B33 | Audio Input 29-30 (checkbox) | Checkbox under the meter for audio inputs 29-30 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D28 | Audio Input 31-32 meter | Level meter for audio inputs 31 and 32 | — | — | click only | Input 32: not available |
| HWIF-F-B34 | Audio Input 31-32 (checkbox) | Checkbox under the meter for audio inputs 31-32 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D29 | Audio Input 33-34 meter | Level meter for audio inputs 33 and 34 | — | — | click only | Input 34: not available |
| HWIF-F-B35 | Audio Input 33-34 (checkbox) | Checkbox under the meter for audio inputs 33-34 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D30 | Audio Input 35-36 meter | Level meter for audio inputs 35 and 36 | — | — | click only | Input 36: not available |
| HWIF-F-B36 | Audio Input 35-36 (checkbox) | Checkbox under the meter for audio inputs 35-36 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D31 | Audio Input 37-38 meter | Level meter for audio inputs 37 and 38 | — | — | click only | Input 38: not available |
| HWIF-F-B37 | Audio Input 37-38 (checkbox) | Checkbox under the meter for audio inputs 37-38 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D32 | Audio Input 39-40 meter | Level meter for audio inputs 39 and 40 | — | — | click only | Input 40: not available |
| HWIF-F-B38 | Audio Input 39-40 (checkbox) | Checkbox under the meter for audio inputs 39-40 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D33 | Audio Input 41-42 meter | Level meter for audio inputs 41 and 42 | — | — | click only | Input 42: not available |
| HWIF-F-B39 | Audio Input 41-42 (checkbox) | Checkbox under the meter for audio inputs 41-42 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D34 | Audio Input 43-44 meter | Level meter for audio inputs 43 and 44 | — | — | click only | Input 44: not available |
| HWIF-F-B40 | Audio Input 43-44 (checkbox) | Checkbox under the meter for audio inputs 43-44 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D35 | Audio Input 45-46 meter | Level meter for audio inputs 45 and 46 | — | — | click only | Input 46: not available |
| HWIF-F-B41 | Audio Input 45-46 (checkbox) | Checkbox under the meter for audio inputs 45-46 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D36 | Audio Input 47-48 meter | Level meter for audio inputs 47 and 48 | — | — | click only | Input 48: not available |
| HWIF-F-B42 | Audio Input 47-48 (checkbox) | Checkbox under the meter for audio inputs 47-48 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D37 | Audio Input 49-50 meter | Level meter for audio inputs 49 and 50 | — | — | click only | Input 50: not available |
| HWIF-F-B43 | Audio Input 49-50 (checkbox) | Checkbox under the meter for audio inputs 49-50 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D38 | Audio Input 51-52 meter | Level meter for audio inputs 51 and 52 | — | — | click only | Input 52: not available |
| HWIF-F-B44 | Audio Input 51-52 (checkbox) | Checkbox under the meter for audio inputs 51-52 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D39 | Audio Input 53-54 meter | Level meter for audio inputs 53 and 54 | — | — | click only | Input 54: not available |
| HWIF-F-B45 | Audio Input 53-54 (checkbox) | Checkbox under the meter for audio inputs 53-54 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D40 | Audio Input 55-56 meter | Level meter for audio inputs 55 and 56 | — | — | click only | Input 55: not available |
| HWIF-F-B46 | Audio Input 55-56 (checkbox) | Checkbox under the meter for audio inputs 55-56 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D41 | Audio Input 57-58 meter | Level meter for audio inputs 57 and 58 | — | — | click only | Input 58: not available |
| HWIF-F-B47 | Audio Input 57-58 (checkbox) | Checkbox under the meter for audio inputs 57-58 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D42 | Audio Input 59-60 meter | Level meter for audio inputs 59 and 60 | — | — | click only | Input 60: not available |
| HWIF-F-B48 | Audio Input 59-60 (checkbox) | Checkbox under the meter for audio inputs 59-60 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D43 | Audio Input 61-62 meter | Level meter for audio inputs 61 and 62 | — | — | click only | Input 62: not available |
| HWIF-F-B49 | Audio Input 61-62 (checkbox) | Checkbox under the meter for audio inputs 61-62 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D44 | Audio Input 63-64 meter | Level meter for audio inputs 63 and 64 | — | — | click only | Input 64: not available |
| HWIF-F-B50 | Audio Input 63-64 (checkbox) | Checkbox under the meter for audio inputs 63-64 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D45 | Audio Output 17-18 meter | Level meter for audio outputs 17 and 18 | — | — | click only | Output 18: not available |
| HWIF-F-B51 | Audio Output 17-18 (checkbox) | Checkbox under the meter for audio outputs 17-18 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D46 | Audio Output 19-20 meter | Level meter for audio outputs 19 and 20 | — | — | click only | Output 20: not available |
| HWIF-F-B52 | Audio Output 19-20 (checkbox) | Checkbox under the meter for audio outputs 19-20 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D47 | Audio Output 21-22 meter | Level meter for audio outputs 21 and 22 | — | — | click only | Output 22: not available |
| HWIF-F-B53 | Audio Output 21-22 (checkbox) | Checkbox under the meter for audio outputs 21-22 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D48 | Audio Output 23-24 meter | Level meter for audio outputs 23 and 24 | — | — | click only | Output 24: not available |
| HWIF-F-B54 | Audio Output 23-24 (checkbox) | Checkbox under the meter for audio outputs 23-24 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D49 | Audio Output 25-26 meter | Level meter for audio outputs 25 and 26 | — | — | click only | Output 26: not available |
| HWIF-F-B55 | Audio Output 25-26 (checkbox) | Checkbox under the meter for audio outputs 25-26 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D50 | Audio Output 27-28 meter | Level meter for audio outputs 27 and 28 | — | — | click only | Output 28: not available |
| HWIF-F-B56 | Audio Output 27-28 (checkbox) | Checkbox under the meter for audio outputs 27-28 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D51 | Audio Output 29-30 meter | Level meter for audio outputs 29 and 30 | — | — | click only | Output 30: not available |
| HWIF-F-B57 | Audio Output 29-30 (checkbox) | Checkbox under the meter for audio outputs 29-30 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D52 | Audio Output 31-32 meter | Level meter for audio outputs 31 and 32 | — | — | click only | Output 32: not available |
| HWIF-F-B58 | Audio Output 31-32 (checkbox) | Checkbox under the meter for audio outputs 31-32 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D53 | Audio Output 33-34 meter | Level meter for audio outputs 33 and 34 | — | — | click only | Output 34: not available |
| HWIF-F-B59 | Audio Output 33-34 (checkbox) | Checkbox under the meter for audio outputs 33-34 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D54 | Audio Output 35-36 meter | Level meter for audio outputs 35 and 36 | — | — | click only | Output 36: not available |
| HWIF-F-B60 | Audio Output 35-36 (checkbox) | Checkbox under the meter for audio outputs 35-36 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D55 | Audio Output 37-38 meter | Level meter for audio outputs 37 and 38 | — | — | click only | Output 38: not available |
| HWIF-F-B61 | Audio Output 37-38 (checkbox) | Checkbox under the meter for audio outputs 37-38 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D56 | Audio Output 39-40 meter | Level meter for audio outputs 39 and 40 | — | — | click only | Output 40: not available |
| HWIF-F-B62 | Audio Output 39-40 (checkbox) | Checkbox under the meter for audio outputs 39-40 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D57 | Audio Output 41-42 meter | Level meter for audio outputs 41 and 42 | — | — | click only | Output 42: not available |
| HWIF-F-B63 | Audio Output 41-42 (checkbox) | Checkbox under the meter for audio outputs 41-42 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D58 | Audio Output 43-44 meter | Level meter for audio outputs 43 and 44 | — | — | click only | Output 44: not available |
| HWIF-F-B64 | Audio Output 43-44 (checkbox) | Checkbox under the meter for audio outputs 43-44 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D59 | Audio Output 45-46 meter | Level meter for audio outputs 45 and 46 | — | — | click only | Output 46: not available |
| HWIF-F-B65 | Audio Output 45-46 (checkbox) | Checkbox under the meter for audio outputs 45-46 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D60 | Audio Output 47-48 meter | Level meter for audio outputs 47 and 48 | — | — | click only | Output 48: not available |
| HWIF-F-B66 | Audio Output 47-48 (checkbox) | Checkbox under the meter for audio outputs 47-48 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D61 | Audio Output 49-50 meter | Level meter for audio outputs 49 and 50 | — | — | click only | Output 50: not available |
| HWIF-F-B67 | Audio Output 49-50 (checkbox) | Checkbox under the meter for audio outputs 49-50 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D62 | Audio Output 51-52 meter | Level meter for audio outputs 51 and 52 | — | — | click only | Output 52: not available |
| HWIF-F-B68 | Audio Output 51-52 (checkbox) | Checkbox under the meter for audio outputs 51-52 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D63 | Audio Output 53-54 meter | Level meter for audio outputs 53 and 54 | — | — | click only | Output 54: not available |
| HWIF-F-B69 | Audio Output 53-54 (checkbox) | Checkbox under the meter for audio outputs 53-54 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D64 | Audio Output 55-56 meter | Level meter for audio outputs 55 and 56 | — | — | click only | Output 55: not available |
| HWIF-F-B70 | Audio Output 55-56 (checkbox) | Checkbox under the meter for audio outputs 55-56 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D65 | Audio Output 57-58 meter | Level meter for audio outputs 57 and 58 | — | — | click only | Output 58: not available |
| HWIF-F-B71 | Audio Output 57-58 (checkbox) | Checkbox under the meter for audio outputs 57-58 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D66 | Audio Output 59-60 meter | Level meter for audio outputs 59 and 60 | — | — | click only | Output 60: not available |
| HWIF-F-B72 | Audio Output 59-60 (checkbox) | Checkbox under the meter for audio outputs 59-60 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D67 | Audio Output 61-62 meter | Level meter for audio outputs 61 and 62 | — | — | click only | Output 62: not available |
| HWIF-F-B73 | Audio Output 61-62 (checkbox) | Checkbox under the meter for audio outputs 61-62 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D68 | Audio Output 63-64 meter | Level meter for audio outputs 63 and 64 | — | — | click only | Output 64: not available |
| HWIF-F-B74 | Audio Output 63-64 (checkbox) | Checkbox under the meter for audio outputs 63-64 (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-B75 | Big meter VU (light) | Big Meter VU mode light | — | — | click only | no tooltip |
| HWIF-F-B76 | Big meter PPM (light) | Big Meter PPM mode light | — | — | click only | no tooltip |
| HWIF-F-B79 | Big meter PEAK (light) | Big Meter peak light | — | — | click only | no tooltip |
| HWIF-F-B77 | Big meter FIVE SEC (light) | Big Meter five-second peak hold light | — | — | click only | no tooltip |
| HWIF-F-B81 | Big meter INFINITE (light) | Big Meter infinite peak hold light | — | — | click only | no tooltip |
| HWIF-F-B80 | MODE (checkbox) | Big Meter mode checkbox | — | — | click only | Meter Mode: VU + Peak |
| HWIF-F-B82 | PEAK HOLD (checkbox) | Big Meter peak hold checkbox | — | — | click only | Change Peak Hold Time |
| HWIF-F-K02 | VU OFFSET (knob) | Big Meter VU offset | — | — | click only | Change VU Offset |
| HWIF-F-K03 | CHANNEL (knob) | Big Meter channel select (picks this as the Big Meter source) | — | — | click only | Select an input or output for the Big Meter |
| HWIF-F-D69 | Big meter display | Big Meter two-channel level display | — | — | click only | no tooltip |
| HWIF-F-B78 | Big meter RESET (button) | Resets the Big Meter clip and peak readings | — | — | click only | Reset Clip indicators |
| HWIF-F-B83 | BUS SELECT A | Advanced MIDI bus A | — | — | click only | MIDI Bus Select |
| HWIF-F-B84 | BUS SELECT B | Advanced MIDI bus B | — | — | click only | MIDI Bus Select |
| HWIF-F-B85 | BUS SELECT C | Advanced MIDI bus C | — | — | click only | MIDI Bus Select |
| HWIF-F-B86 | BUS SELECT D | Advanced MIDI bus D | — | — | click only | MIDI Bus Select |
| HWIF-F-D70 | MIDI input name display | Shows the MIDI input for the selected bus (No MIDI Input) | — | — | click only | no tooltip |
| HWIF-F-D71 | Channel 1 name display | Advanced MIDI channel 1 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D79 | Channel 1 (light) | Advanced MIDI channel 1 light | — | — | click only | no tooltip |
| HWIF-F-B87 | Channel 1 (dropdown) | Advanced MIDI channel 1 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D72 | Channel 2 name display | Advanced MIDI channel 2 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D81 | Channel 2 (light) | Advanced MIDI channel 2 light | — | — | click only | no tooltip |
| HWIF-F-B88 | Channel 2 (dropdown) | Advanced MIDI channel 2 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D73 | Channel 3 name display | Advanced MIDI channel 3 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D83 | Channel 3 (light) | Advanced MIDI channel 3 light | — | — | click only | no tooltip |
| HWIF-F-B89 | Channel 3 (dropdown) | Advanced MIDI channel 3 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D74 | Channel 4 name display | Advanced MIDI channel 4 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D85 | Channel 4 (light) | Advanced MIDI channel 4 light | — | — | click only | no tooltip |
| HWIF-F-B90 | Channel 4 (dropdown) | Advanced MIDI channel 4 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D75 | Channel 5 name display | Advanced MIDI channel 5 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D87 | Channel 5 (light) | Advanced MIDI channel 5 light | — | — | click only | no tooltip |
| HWIF-F-B91 | Channel 5 (dropdown) | Advanced MIDI channel 5 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D76 | Channel 6 name display | Advanced MIDI channel 6 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D89 | Channel 6 (light) | Advanced MIDI channel 6 light | — | — | click only | no tooltip |
| HWIF-F-B92 | Channel 6 (dropdown) | Advanced MIDI channel 6 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D77 | Channel 7 name display | Advanced MIDI channel 7 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D91 | Channel 7 (light) | Advanced MIDI channel 7 light | — | — | click only | no tooltip |
| HWIF-F-B93 | Channel 7 (dropdown) | Advanced MIDI channel 7 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D78 | Channel 8 name display | Advanced MIDI channel 8 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D93 | Channel 8 (light) | Advanced MIDI channel 8 light | — | — | click only | no tooltip |
| HWIF-F-B94 | Channel 8 (dropdown) | Advanced MIDI channel 8 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D80 | Channel 9 name display | Advanced MIDI channel 9 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D95 | Channel 9 (light) | Advanced MIDI channel 9 light | — | — | click only | no tooltip |
| HWIF-F-B95 | Channel 9 (dropdown) | Advanced MIDI channel 9 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D82 | Channel 10 name display | Advanced MIDI channel 10 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D96 | Channel 10 (light) | Advanced MIDI channel 10 light | — | — | click only | no tooltip |
| HWIF-F-B96 | Channel 10 (dropdown) | Advanced MIDI channel 10 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D84 | Channel 11 name display | Advanced MIDI channel 11 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D97 | Channel 11 (light) | Advanced MIDI channel 11 light | — | — | click only | no tooltip |
| HWIF-F-B97 | Channel 11 (dropdown) | Advanced MIDI channel 11 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D86 | Channel 12 name display | Advanced MIDI channel 12 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D98 | Channel 12 (light) | Advanced MIDI channel 12 light | — | — | click only | no tooltip |
| HWIF-F-B98 | Channel 12 (dropdown) | Advanced MIDI channel 12 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D88 | Channel 13 name display | Advanced MIDI channel 13 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D99 | Channel 13 (light) | Advanced MIDI channel 13 light | — | — | click only | no tooltip |
| HWIF-F-B99 | Channel 13 (dropdown) | Advanced MIDI channel 13 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D90 | Channel 14 name display | Advanced MIDI channel 14 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D100 | Channel 14 (light) | Advanced MIDI channel 14 light | — | — | click only | no tooltip |
| HWIF-F-B100 | Channel 14 (dropdown) | Advanced MIDI channel 14 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D92 | Channel 15 name display | Advanced MIDI channel 15 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D101 | Channel 15 (light) | Advanced MIDI channel 15 light | — | — | click only | no tooltip |
| HWIF-F-B101 | Channel 15 (dropdown) | Advanced MIDI channel 15 dropdown arrow | — | — | click only | no tooltip |
| HWIF-F-D94 | Channel 16 name display | Advanced MIDI channel 16 patch/name display | — | — | click only | no tooltip |
| HWIF-F-D102 | Channel 16 (light) | Advanced MIDI channel 16 light | — | — | click only | no tooltip |
| HWIF-F-B102 | Channel 16 (dropdown) | Advanced MIDI channel 16 dropdown arrow | — | — | click only | no tooltip |

## Hardware Interface — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| HWIF-B-B01 | (fold triangle) | Folds/unfolds the Hardware Interface (back) | — | — | click/drag only (no Remote item) | no tooltip (fold triangle) |
| HWIF-B-D01 | HARDWARE INTERFACE label | Device name label (back) | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D02 | (black slot) | Black slot, no jack or control | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-B02 | AUDIO I/O (button, back) | Shows/hides the Audio I/O section | — | — | click/drag only (no Remote item) | Show basic Audio in and outs |
| HWIF-B-B03 | MORE AUDIO (button, back) | Shows/hides the Audio I/O 17-64 sections | — | — | click/drag only (no Remote item) | Show extra Audio ins and outs |
| HWIF-B-B04 | BIG METER (button, back) | Shows/hides the Big Meter section | — | — | click/drag only (no Remote item) | Show Big Meter panel |
| HWIF-B-B05 | ADV. MIDI (button, back) | Shows/hides the Advanced MIDI section | — | — | click/drag only (no Remote item) | Show MIDI External Control panel |
| HWIF-B-D03 | AUDIO I/O name plate | Name plate for the 1-16 jack panel | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D04 | (black slot 2) | Black slot under the name plate | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D05 | BIG METER name plate | Name plate for the Big Meter panel | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D06 | LED status label | Label explaining the channel LED colours | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D07 | LED (indicator) | LED indicator drawing | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D08 | Big Meter fan vent | Fan vent grille (decoration) | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D09 | Big Meter power socket | Power cable plug picture | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D10 | ADVANCED MIDI name plate | Name plate for the Advanced MIDI panel | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D11 | Advanced MIDI fan vent | Fan vent grille (decoration) | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-D12 | Advanced MIDI power socket | Power cable plug picture | — | — | click/drag only (no Remote item) | no tooltip |
| HWIF-B-J01 | Sampling Input L | Sampling input left jack | Sampling Left Input | — | cable: right-click jack > device > jack name | Connected to Hardware Interface II: Input 1 |
| HWIF-B-J18 | Sampling Input R | Sampling input right jack | Sampling Right Input | — | cable: right-click jack > device > jack name | Connected to Hardware Interface II: Input 2 |
| HWIF-B-J02 | Audio Input 1 | From Audio Input 1 (L) | Input 1 | — | cable: right-click jack > device > jack name | Connected to Hardware Interface II: Sampling Left Input |
| HWIF-B-J19 | Audio Input 2 | From Audio Input 2 (R) | Input 2 | — | cable: right-click jack > device > jack name | Connected to Hardware Interface II: Sampling Right Input |
| HWIF-B-J03 | Audio Input 3 | From Audio Input 3 (L) | Input 3 | — | cable: right-click jack > device > jack name | Input 3 |
| HWIF-B-J20 | Audio Input 4 | From Audio Input 4 (R) | Input 4 | — | cable: right-click jack > device > jack name | Input 4 |
| HWIF-B-J04 | Audio Input 5 | From Audio Input 5 (L) | Input 5 | — | cable: right-click jack > device > jack name | Input 5 |
| HWIF-B-J21 | Audio Input 6 | From Audio Input 6 (R) | Input 6 | — | cable: right-click jack > device > jack name | Input 6 |
| HWIF-B-J05 | Audio Input 7 | From Audio Input 7 (L) | Input 7 | — | cable: right-click jack > device > jack name | Input 7 |
| HWIF-B-J22 | Audio Input 8 | From Audio Input 8 (R) | Input 8 | — | cable: right-click jack > device > jack name | Input 8 |
| HWIF-B-J06 | Audio Input 9 | From Audio Input 9 (L) | Input 9 | — | cable: right-click jack > device > jack name | Input 9 |
| HWIF-B-J23 | Audio Input 10 | From Audio Input 10 (R) | Input 10 | — | cable: right-click jack > device > jack name | Input 10 |
| HWIF-B-J07 | Audio Input 11 | From Audio Input 11 (L) | Input 11 | — | cable: right-click jack > device > jack name | Input 11 |
| HWIF-B-J24 | Audio Input 12 | From Audio Input 12 (R) | Input 12 | — | cable: right-click jack > device > jack name | Input 12 |
| HWIF-B-J08 | Audio Input 13 | From Audio Input 13 (L) | Input 13 | — | cable: right-click jack > device > jack name | Input 13 |
| HWIF-B-J25 | Audio Input 14 | From Audio Input 14 (R) | Input 14 | — | cable: right-click jack > device > jack name | Input 14 |
| HWIF-B-J09 | Audio Input 15 | From Audio Input 15 (L) | Input 15 | — | cable: right-click jack > device > jack name | Input 15 |
| HWIF-B-J26 | Audio Input 16 | From Audio Input 16 (R) | Input 16 | — | cable: right-click jack > device > jack name | Input 16 |
| HWIF-B-J10 | Audio Output 1 | To Audio Output 1 (L) | Output 1 | — | cable: right-click jack > device > jack name | Connected to Master Section: Master Output L |
| HWIF-B-J27 | Audio Output 2 | To Audio Output 2 (R) | Output 2 | — | cable: right-click jack > device > jack name | Output 2 |
| HWIF-B-J11 | Audio Output 3 | To Audio Output 3 (L) | Output 3 | — | cable: right-click jack > device > jack name | Output 3 |
| HWIF-B-J28 | Audio Output 4 | To Audio Output 4 (R) | Output 4 | — | cable: right-click jack > device > jack name | Output 4 |
| HWIF-B-J12 | Audio Output 5 | To Audio Output 5 (L) | Output 5 | — | cable: right-click jack > device > jack name | Output 5 |
| HWIF-B-J29 | Audio Output 6 | To Audio Output 6 (R) | Output 6 | — | cable: right-click jack > device > jack name | Output 6 |
| HWIF-B-J13 | Audio Output 7 | To Audio Output 7 (L) | Output 7 | — | cable: right-click jack > device > jack name | Output 7 |
| HWIF-B-J30 | Audio Output 8 | To Audio Output 8 (R) | Output 8 | — | cable: right-click jack > device > jack name | Output 8 |
| HWIF-B-J14 | Audio Output 9 | To Audio Output 9 (L) | Output 9 | — | cable: right-click jack > device > jack name | Output 9 |
| HWIF-B-J31 | Audio Output 10 | To Audio Output 10 (R) | Output 10 | — | cable: right-click jack > device > jack name | Output 10 |
| HWIF-B-J15 | Audio Output 11 | To Audio Output 11 (L) | Output 11 | — | cable: right-click jack > device > jack name | Output 11 |
| HWIF-B-J32 | Audio Output 12 | To Audio Output 12 (R) | Output 12 | — | cable: right-click jack > device > jack name | Output 12 |
| HWIF-B-J16 | Audio Output 13 | To Audio Output 13 (L) | Output 13 | — | cable: right-click jack > device > jack name | Output 13 |
| HWIF-B-J33 | Audio Output 14 | To Audio Output 14 (R) | Output 14 | — | cable: right-click jack > device > jack name | Output 14 |
| HWIF-B-J17 | Audio Output 15 | To Audio Output 15 (L) | Output 15 | — | cable: right-click jack > device > jack name | Output 15 |
| HWIF-B-J34 | Audio Output 16 | To Audio Output 16 (R) | Output 16 | — | cable: right-click jack > device > jack name | Output 16 |
| HWIF-B-J35 | Audio Input 17 | From Audio Input 17 (L) | Input 17 | — | cable: right-click jack > device > jack name | Input 17 |
| HWIF-B-J59 | Audio Input 18 | From Audio Input 18 (R) | Input 18 | — | cable: right-click jack > device > jack name | Input 18 |
| HWIF-B-J36 | Audio Input 19 | From Audio Input 19 (L) | Input 19 | — | cable: right-click jack > device > jack name | Input 19 |
| HWIF-B-J60 | Audio Input 20 | From Audio Input 20 (R) | Input 20 | — | cable: right-click jack > device > jack name | Input 20 |
| HWIF-B-J37 | Audio Input 21 | From Audio Input 21 (L) | Input 21 | — | cable: right-click jack > device > jack name | Input 21 |
| HWIF-B-J61 | Audio Input 22 | From Audio Input 22 (R) | Input 22 | — | cable: right-click jack > device > jack name | Input 22 |
| HWIF-B-J38 | Audio Input 23 | From Audio Input 23 (L) | Input 23 | — | cable: right-click jack > device > jack name | Input 23 |
| HWIF-B-J62 | Audio Input 24 | From Audio Input 24 (R) | Input 24 | — | cable: right-click jack > device > jack name | Input 24 |
| HWIF-B-J39 | Audio Input 25 | From Audio Input 25 (L) | Input 25 | — | cable: right-click jack > device > jack name | Input 25 |
| HWIF-B-J63 | Audio Input 26 | From Audio Input 26 (R) | Input 26 | — | cable: right-click jack > device > jack name | Input 26 |
| HWIF-B-J40 | Audio Input 27 | From Audio Input 27 (L) | Input 27 | — | cable: right-click jack > device > jack name | Input 27 |
| HWIF-B-J64 | Audio Input 28 | From Audio Input 28 (R) | Input 28 | — | cable: right-click jack > device > jack name | Input 28 |
| HWIF-B-J41 | Audio Input 29 | From Audio Input 29 (L) | Input 29 | — | cable: right-click jack > device > jack name | Input 29 |
| HWIF-B-J65 | Audio Input 30 | From Audio Input 30 (R) | Input 30 | — | cable: right-click jack > device > jack name | Input 30 |
| HWIF-B-J42 | Audio Input 31 | From Audio Input 31 (L) | Input 31 | — | cable: right-click jack > device > jack name | Input 31 |
| HWIF-B-J66 | Audio Input 32 | From Audio Input 32 (R) | Input 32 | — | cable: right-click jack > device > jack name | Input 32 |
| HWIF-B-J43 | Audio Input 33 | From Audio Input 33 (L) | Input 33 | — | cable: right-click jack > device > jack name | Input 33 |
| HWIF-B-J67 | Audio Input 34 | From Audio Input 34 (R) | Input 34 | — | cable: right-click jack > device > jack name | Input 34 |
| HWIF-B-J44 | Audio Input 35 | From Audio Input 35 (L) | Input 35 | — | cable: right-click jack > device > jack name | Input 35 |
| HWIF-B-J68 | Audio Input 36 | From Audio Input 36 (R) | Input 36 | — | cable: right-click jack > device > jack name | Input 36 |
| HWIF-B-J45 | Audio Input 37 | From Audio Input 37 (L) | Input 37 | — | cable: right-click jack > device > jack name | Input 37 |
| HWIF-B-J69 | Audio Input 38 | From Audio Input 38 (R) | Input 38 | — | cable: right-click jack > device > jack name | Input 38 |
| HWIF-B-J46 | Audio Input 39 | From Audio Input 39 (L) | Input 39 | — | cable: right-click jack > device > jack name | Input 39 |
| HWIF-B-J70 | Audio Input 40 | From Audio Input 40 (R) | Input 40 | — | cable: right-click jack > device > jack name | Input 40 |
| HWIF-B-J47 | Audio Input 41 | From Audio Input 41 (L) | Input 41 | — | cable: right-click jack > device > jack name | Input 41 |
| HWIF-B-J71 | Audio Input 42 | From Audio Input 42 (R) | Input 42 | — | cable: right-click jack > device > jack name | Input 42 |
| HWIF-B-J48 | Audio Input 43 | From Audio Input 43 (L) | Input 43 | — | cable: right-click jack > device > jack name | Input 43 |
| HWIF-B-J72 | Audio Input 44 | From Audio Input 44 (R) | Input 44 | — | cable: right-click jack > device > jack name | Input 44 |
| HWIF-B-J49 | Audio Input 45 | From Audio Input 45 (L) | Input 45 | — | cable: right-click jack > device > jack name | Input 45 |
| HWIF-B-J73 | Audio Input 46 | From Audio Input 46 (R) | Input 46 | — | cable: right-click jack > device > jack name | Input 46 |
| HWIF-B-J50 | Audio Input 47 | From Audio Input 47 (L) | Input 47 | — | cable: right-click jack > device > jack name | Input 47 |
| HWIF-B-J74 | Audio Input 48 | From Audio Input 48 (R) | Input 48 | — | cable: right-click jack > device > jack name | Input 48 |
| HWIF-B-J51 | Audio Input 49 | From Audio Input 49 (L) | Input 49 | — | cable: right-click jack > device > jack name | Input 49 |
| HWIF-B-J75 | Audio Input 50 | From Audio Input 50 (R) | Input 50 | — | cable: right-click jack > device > jack name | Input 50 |
| HWIF-B-J52 | Audio Input 51 | From Audio Input 51 (L) | Input 51 | — | cable: right-click jack > device > jack name | Input 51 |
| HWIF-B-J76 | Audio Input 52 | From Audio Input 52 (R) | Input 52 | — | cable: right-click jack > device > jack name | Input 52 |
| HWIF-B-J53 | Audio Input 53 | From Audio Input 53 (L) | Input 53 | — | cable: right-click jack > device > jack name | Input 53 |
| HWIF-B-J77 | Audio Input 54 | From Audio Input 54 (R) | Input 54 | — | cable: right-click jack > device > jack name | Input 54 |
| HWIF-B-J54 | Audio Input 55 | From Audio Input 55 (L) | Input 55 | — | cable: right-click jack > device > jack name | Input 55 |
| HWIF-B-J78 | Audio Input 56 | From Audio Input 56 (R) | Input 56 | — | cable: right-click jack > device > jack name | Input 56 |
| HWIF-B-J55 | Audio Input 57 | From Audio Input 57 (L) | Input 57 | — | cable: right-click jack > device > jack name | Input 57 |
| HWIF-B-J79 | Audio Input 58 | From Audio Input 58 (R) | Input 58 | — | cable: right-click jack > device > jack name | Input 58 |
| HWIF-B-J56 | Audio Input 59 | From Audio Input 59 (L) | Input 59 | — | cable: right-click jack > device > jack name | Input 59 |
| HWIF-B-J80 | Audio Input 60 | From Audio Input 60 (R) | Input 60 | — | cable: right-click jack > device > jack name | Input 60 |
| HWIF-B-J57 | Audio Input 61 | From Audio Input 61 (L) | Input 61 | — | cable: right-click jack > device > jack name | Input 61 |
| HWIF-B-J81 | Audio Input 62 | From Audio Input 62 (R) | Input 62 | — | cable: right-click jack > device > jack name | Input 62 |
| HWIF-B-J58 | Audio Input 63 | From Audio Input 63 (L) | Input 63 | — | cable: right-click jack > device > jack name | Input 63 |
| HWIF-B-J82 | Audio Input 64 | From Audio Input 64 (R) | Input 64 | — | cable: right-click jack > device > jack name | Input 64 |
| HWIF-B-J83 | Audio Output 17 | To Audio Output 17 (L) | Output 17 | — | cable: right-click jack > device > jack name | Output 17 |
| HWIF-B-J107 | Audio Output 18 | To Audio Output 18 (R) | Output 18 | — | cable: right-click jack > device > jack name | Output 18 |
| HWIF-B-J84 | Audio Output 19 | To Audio Output 19 (L) | Output 19 | — | cable: right-click jack > device > jack name | Output 19 |
| HWIF-B-J108 | Audio Output 20 | To Audio Output 20 (R) | Output 20 | — | cable: right-click jack > device > jack name | Output 20 |
| HWIF-B-J85 | Audio Output 21 | To Audio Output 21 (L) | Output 21 | — | cable: right-click jack > device > jack name | Output 21 |
| HWIF-B-J109 | Audio Output 22 | To Audio Output 22 (R) | Output 22 | — | cable: right-click jack > device > jack name | Output 22 |
| HWIF-B-J86 | Audio Output 23 | To Audio Output 23 (L) | Output 23 | — | cable: right-click jack > device > jack name | Output 23 |
| HWIF-B-J110 | Audio Output 24 | To Audio Output 24 (R) | Output 24 | — | cable: right-click jack > device > jack name | Output 24 |
| HWIF-B-J87 | Audio Output 25 | To Audio Output 25 (L) | Output 25 | — | cable: right-click jack > device > jack name | Output 25 |
| HWIF-B-J111 | Audio Output 26 | To Audio Output 26 (R) | Output 26 | — | cable: right-click jack > device > jack name | Output 26 |
| HWIF-B-J88 | Audio Output 27 | To Audio Output 27 (L) | Output 27 | — | cable: right-click jack > device > jack name | Output 27 |
| HWIF-B-J112 | Audio Output 28 | To Audio Output 28 (R) | Output 28 | — | cable: right-click jack > device > jack name | Output 28 |
| HWIF-B-J89 | Audio Output 29 | To Audio Output 29 (L) | Output 29 | — | cable: right-click jack > device > jack name | Output 29 |
| HWIF-B-J113 | Audio Output 30 | To Audio Output 30 (R) | Output 30 | — | cable: right-click jack > device > jack name | Output 30 |
| HWIF-B-J90 | Audio Output 31 | To Audio Output 31 (L) | Output 31 | — | cable: right-click jack > device > jack name | Output 31 |
| HWIF-B-J114 | Audio Output 32 | To Audio Output 32 (R) | Output 32 | — | cable: right-click jack > device > jack name | Output 32 |
| HWIF-B-J91 | Audio Output 33 | To Audio Output 33 (L) | Output 33 | — | cable: right-click jack > device > jack name | Output 33 |
| HWIF-B-J115 | Audio Output 34 | To Audio Output 34 (R) | Output 34 | — | cable: right-click jack > device > jack name | Output 34 |
| HWIF-B-J92 | Audio Output 35 | To Audio Output 35 (L) | Output 35 | — | cable: right-click jack > device > jack name | Output 35 |
| HWIF-B-J116 | Audio Output 36 | To Audio Output 36 (R) | Output 36 | — | cable: right-click jack > device > jack name | Output 36 |
| HWIF-B-J93 | Audio Output 37 | To Audio Output 37 (L) | Output 37 | — | cable: right-click jack > device > jack name | Output 37 |
| HWIF-B-J117 | Audio Output 38 | To Audio Output 38 (R) | Output 38 | — | cable: right-click jack > device > jack name | Output 38 |
| HWIF-B-J94 | Audio Output 39 | To Audio Output 39 (L) | Output 39 | — | cable: right-click jack > device > jack name | Output 39 |
| HWIF-B-J118 | Audio Output 40 | To Audio Output 40 (R) | Output 40 | — | cable: right-click jack > device > jack name | Output 40 |
| HWIF-B-J95 | Audio Output 41 | To Audio Output 41 (L) | Output 41 | — | cable: right-click jack > device > jack name | Output 41 |
| HWIF-B-J119 | Audio Output 42 | To Audio Output 42 (R) | Output 42 | — | cable: right-click jack > device > jack name | Output 42 |
| HWIF-B-J96 | Audio Output 43 | To Audio Output 43 (L) | Output 43 | — | cable: right-click jack > device > jack name | Output 43 |
| HWIF-B-J120 | Audio Output 44 | To Audio Output 44 (R) | Output 44 | — | cable: right-click jack > device > jack name | Output 44 |
| HWIF-B-J97 | Audio Output 45 | To Audio Output 45 (L) | Output 45 | — | cable: right-click jack > device > jack name | Output 45 |
| HWIF-B-J121 | Audio Output 46 | To Audio Output 46 (R) | Output 46 | — | cable: right-click jack > device > jack name | Output 46 |
| HWIF-B-J98 | Audio Output 47 | To Audio Output 47 (L) | Output 47 | — | cable: right-click jack > device > jack name | Output 47 |
| HWIF-B-J122 | Audio Output 48 | To Audio Output 48 (R) | Output 48 | — | cable: right-click jack > device > jack name | Output 48 |
| HWIF-B-J99 | Audio Output 49 | To Audio Output 49 (L) | Output 49 | — | cable: right-click jack > device > jack name | Output 49 |
| HWIF-B-J123 | Audio Output 50 | To Audio Output 50 (R) | Output 50 | — | cable: right-click jack > device > jack name | Output 50 |
| HWIF-B-J100 | Audio Output 51 | To Audio Output 51 (L) | Output 51 | — | cable: right-click jack > device > jack name | Output 51 |
| HWIF-B-J124 | Audio Output 52 | To Audio Output 52 (R) | Output 52 | — | cable: right-click jack > device > jack name | Output 52 |
| HWIF-B-J101 | Audio Output 53 | To Audio Output 53 (L) | Output 53 | — | cable: right-click jack > device > jack name | Output 53 |
| HWIF-B-J125 | Audio Output 54 | To Audio Output 54 (R) | Output 54 | — | cable: right-click jack > device > jack name | Output 54 |
| HWIF-B-J102 | Audio Output 55 | To Audio Output 55 (L) | Output 55 | — | cable: right-click jack > device > jack name | Output 55 |
| HWIF-B-J126 | Audio Output 56 | To Audio Output 56 (R) | Output 56 | — | cable: right-click jack > device > jack name | Output 56 |
| HWIF-B-J103 | Audio Output 57 | To Audio Output 57 (L) | Output 57 | — | cable: right-click jack > device > jack name | Output 57 |
| HWIF-B-J127 | Audio Output 58 | To Audio Output 58 (R) | Output 58 | — | cable: right-click jack > device > jack name | Output 58 |
| HWIF-B-J104 | Audio Output 59 | To Audio Output 59 (L) | Output 59 | — | cable: right-click jack > device > jack name | Output 59 |
| HWIF-B-J128 | Audio Output 60 | To Audio Output 60 (R) | Output 60 | — | cable: right-click jack > device > jack name | Output 60 |
| HWIF-B-J105 | Audio Output 61 | To Audio Output 61 (L) | Output 61 | — | cable: right-click jack > device > jack name | Output 61 |
| HWIF-B-J129 | Audio Output 62 | To Audio Output 62 (R) | Output 62 | — | cable: right-click jack > device > jack name | Output 62 |
| HWIF-B-J106 | Audio Output 63 | To Audio Output 63 (L) | Output 63 | — | cable: right-click jack > device > jack name | Connected to Master Section: Master Output R |
| HWIF-B-J130 | Audio Output 64 | To Audio Output 64 (R) | Output 64 | — | cable: right-click jack > device > jack name | Output 64 |

## Master Section — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MSEC-F-B01 | (fold triangle) | Folds/unfolds the Master Section | — | — | click only | no tooltip |
| MSEC-F-D01 | MASTER SECTION label | Device name label | — | — | click only | no tooltip |
| MSEC-F-B02 | (spectrum button) | Button with a curve picture | — | — | click only | Show in Spectrum EQ Window |
| MSEC-F-B03 | DIM -20dB | Dims the control room output by 20 dB | Dim -20dB | — | display/Remote item, not mapped | Lower Master Level 20 dB Off |
| MSEC-F-D02 | Master meter | Master output level meter (L/R, VU/PEAK) | — | — | click only | no tooltip |
| MSEC-F-B04 | REC SOURCE (checkbox) | Marks the Master Section as the Rec source | — | — | click only | Rec Source |
| MSEC-F-B05 | MODE (checkbox) | Meter mode | — | — | click only | Meter Mode: VU + Peak |
| MSEC-F-B06 | RESET (checkbox) | Resets the meter clip and peak readings | — | — | click only | Reset Clip indicators |
| MSEC-F-B08 | SHOW INSERT FX (arrow) | Shows/hides the insert FX slot | — | — | click only | Show Insert FX |
| MSEC-F-B07 | BYPASS (insert FX) | Bypasses the master insert FX | Bypass Insert FX | — | display/Remote item, not mapped | Bypass Master Insert FX On |
| MSEC-F-D03 | (grille 1) | Speaker grille (decoration) | — | — | click only | no tooltip |
| MSEC-F-D04 | (grille 2) | Speaker grille (decoration) | — | — | click only | no tooltip |
| MSEC-F-D05 | (grille 3) | Speaker grille (decoration) | — | — | click only | no tooltip |

## Master Section — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MSEC-B-B01 | (fold triangle) | Folds/unfolds the Master Section (back) | — | — | click/drag only (no Remote item) | no tooltip |
| MSEC-B-D01 | MASTER SECTION label | Device name label (back) | — | — | click/drag only (no Remote item) | no tooltip |
| MSEC-B-B02 | SHOW INSERT FX (button, back) | Shows/hides the insert FX slot (back) | — | — | click/drag only (no Remote item) | Show Insert FX |
| MSEC-B-J01 | Sidechain Input L | Dynamics sidechain input left | Side Chain Input L | — | cable: right-click jack > device > jack name | Side Chain Input L |
| MSEC-B-J03 | Sidechain Input R | Dynamics sidechain input right | Side Chain Input R | — | cable: right-click jack > device > jack name | Side Chain Input R |
| MSEC-B-B03 | KEY (button) | Sidechain key button | — | — | click/drag only (no Remote item) | Sidechain Key On/Off |
| MSEC-B-K01 | Master Level CV In (trim knob) | Trim for Master Level CV In | — | — | click/drag only (no Remote item) | Master Level CV In: 64 |
| MSEC-B-J02 | Master Level CV In | Master Level CV input | Master Level CV In | — | cable: right-click jack > device > jack name | Master Level CV In |
| MSEC-B-D02 | (black slot) | Black slot above the insert FX slot | — | — | click/drag only (no Remote item) | no tooltip |
| MSEC-B-D03 | INSERT FX slot | Insert FX slot (empty) | — | — | click/drag only (no Remote item) | no tooltip |
| MSEC-B-J04 | FX Send 1 L | FX Send 1 left | FX 1 Send L | — | cable: right-click jack > device > jack name | Connected to Plate: Left Input |
| MSEC-B-J22 | FX Send 1 R | FX Send 1 right | FX 1 Send R | — | cable: right-click jack > device > jack name | Connected to Plate: Right Input |
| MSEC-B-J05 | FX Send 2 L | FX Send 2 left | FX 2 Send L | — | cable: right-click jack > device > jack name | Connected to Room: Left Input |
| MSEC-B-J23 | FX Send 2 R | FX Send 2 right | FX 2 Send R | — | cable: right-click jack > device > jack name | Connected to Room: Right Input |
| MSEC-B-J06 | FX Send 3 L | FX Send 3 left | FX 3 Send L | — | cable: right-click jack > device > jack name | Connected to Echo: Left Input |
| MSEC-B-J24 | FX Send 3 R | FX Send 3 right | FX 3 Send R | — | cable: right-click jack > device > jack name | Connected to Echo: Right Input |
| MSEC-B-J07 | FX Send 4 L | FX Send 4 left | FX 4 Send L | — | cable: right-click jack > device > jack name | Connected to Delay 3/16: Left |
| MSEC-B-J25 | FX Send 4 R | FX Send 4 right | FX 4 Send R | — | cable: right-click jack > device > jack name | Connected to Delay 3/16: Right |
| MSEC-B-J08 | FX Send 5 L | FX Send 5 left | FX 5 Send L | — | cable: right-click jack > device > jack name | FX 5 Send L |
| MSEC-B-J26 | FX Send 5 R | FX Send 5 right | FX 5 Send R | — | cable: right-click jack > device > jack name | FX 5 Send R |
| MSEC-B-J09 | FX Send 6 L | FX Send 6 left | FX 6 Send L | — | cable: right-click jack > device > jack name | FX 6 Send L |
| MSEC-B-J27 | FX Send 6 R | FX Send 6 right | FX 6 Send R | — | cable: right-click jack > device > jack name | FX 6 Send R |
| MSEC-B-J10 | FX Send 7 L | FX Send 7 left | FX 7 Send L | — | cable: right-click jack > device > jack name | FX 7 Send L |
| MSEC-B-J28 | FX Send 7 R | FX Send 7 right | FX 7 Send R | — | cable: right-click jack > device > jack name | FX 7 Send R |
| MSEC-B-J11 | FX Send 8 L | FX Send 8 left | FX 8 Send L | — | cable: right-click jack > device > jack name | FX 8 Send L |
| MSEC-B-J29 | FX Send 8 R | FX Send 8 right | FX 8 Send R | — | cable: right-click jack > device > jack name | FX 8 Send R |
| MSEC-B-J12 | FX Return 1 L | FX Return 1 left | FX 1 Return L | — | cable: right-click jack > device > jack name | Connected to Plate: Left Output |
| MSEC-B-J30 | FX Return 1 R | FX Return 1 right | FX 1 Return R | — | cable: right-click jack > device > jack name | Connected to Plate: Right Output |
| MSEC-B-J13 | FX Return 2 L | FX Return 2 left | FX 2 Return L | — | cable: right-click jack > device > jack name | Connected to Room: Left Output |
| MSEC-B-J31 | FX Return 2 R | FX Return 2 right | FX 2 Return R | — | cable: right-click jack > device > jack name | Connected to Room: Right Output |
| MSEC-B-J14 | FX Return 3 L | FX Return 3 left | FX 3 Return L | — | cable: right-click jack > device > jack name | Connected to Echo: Left Output |
| MSEC-B-J32 | FX Return 3 R | FX Return 3 right | FX 3 Return R | — | cable: right-click jack > device > jack name | Connected to Echo: Right Output |
| MSEC-B-J15 | FX Return 4 L | FX Return 4 left | FX 4 Return L | — | cable: right-click jack > device > jack name | Connected to Delay 3/16: Left |
| MSEC-B-J33 | FX Return 4 R | FX Return 4 right | FX 4 Return R | — | cable: right-click jack > device > jack name | Connected to Delay 3/16: Right |
| MSEC-B-J16 | FX Return 5 L | FX Return 5 left | FX 5 Return L | — | cable: right-click jack > device > jack name | FX 5 Return L |
| MSEC-B-J34 | FX Return 5 R | FX Return 5 right | FX 5 Return R | — | cable: right-click jack > device > jack name | FX 5 Return R |
| MSEC-B-J17 | FX Return 6 L | FX Return 6 left | FX 6 Return L | — | cable: right-click jack > device > jack name | FX 6 Return L |
| MSEC-B-J35 | FX Return 6 R | FX Return 6 right | FX 6 Return R | — | cable: right-click jack > device > jack name | FX 6 Return R |
| MSEC-B-J18 | FX Return 7 L | FX Return 7 left | FX 7 Return L | — | cable: right-click jack > device > jack name | FX 7 Return L |
| MSEC-B-J36 | FX Return 7 R | FX Return 7 right | FX 7 Return R | — | cable: right-click jack > device > jack name | FX 7 Return R |
| MSEC-B-J19 | FX Return 8 L | FX Return 8 left | FX 8 Return L | — | cable: right-click jack > device > jack name | FX 8 Return L |
| MSEC-B-J37 | FX Return 8 R | FX Return 8 right | FX 8 Return R | — | cable: right-click jack > device > jack name | FX 8 Return R |
| MSEC-B-J20 | Ctrl Room Out L | Control room out left | Control Room L | — | cable: right-click jack > device > jack name | Control Room L |
| MSEC-B-J38 | Ctrl Room Out R | Control room out right | Control Room R | — | cable: right-click jack > device > jack name | Control Room R |
| MSEC-B-J21 | Master Out L | Master out left | Master Output L | — | cable: right-click jack > device > jack name | Connected to Hardware Interface II: Output 1 |
| MSEC-B-J39 | Master Out R | Master out right | Master Output R | — | cable: right-click jack > device > jack name | Connected to Hardware Interface II: Output 63 |

## Main Mixer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MMIX-F-K01 | strip Input gain knob | Channel strip: Input gain (+/-18 dB) (mixer window, slice 1 of 4) | — | — | click only | Input Gain: 0.00 dB |
| MMIX-F-B02 | strip INV button | Channel strip: Phase invert (mixer window, slice 1 of 4) | — | — | click only | Invert Phase Off |
| MMIX-F-B03 | strip INSERT PRE checkbox | Channel strip: Signal path: insert first (mixer window, slice 1 of 4) | — | — | click only | Insert Section Pre Dynamics and EQ Off |
| MMIX-F-B04 | strip DYN POSTEQ checkbox | Channel strip: Signal path: dynamics after EQ (mixer window, slice 1 of 4) | — | — | click only | Dynamics Section Post Equalizer Off |
| MMIX-F-D01 | strip Signal path display | Channel strip: Shows the processing order (mixer window, slice 1 of 4) | — | — | click only | no tooltip |
| MMIX-F-B05 | strip FILTERS TO DYN S/C checkbox (input) | Channel strip: Send EQ filters to dynamics side chain (mixer window, slice 1 of 4) | — | — | click only | Filters to Dynamics Sidechain Off |
| MMIX-F-B01 | strip Input section header light | Channel strip: Section header light (mixer window, slice 1 of 4) | — | — | click only | Input section Disabled |
| MMIX-F-B06 | strip Dynamics section header light | Channel strip: Section header light (mixer window, slice 1 of 4) | — | — | click only | Dynamics Disabled |
| MMIX-F-B08 | strip COMP ON | Channel strip: Compressor on/off (mixer window, slice 1 of 4) | — | — | click only | Compressor Disabled |
| MMIX-F-B10 | strip PEAK | Channel strip: Compressor peak detection (mixer window, slice 1 of 4) | — | — | click only | Compressor Peak Off |
| MMIX-F-K02 | strip COMP RATIO knob | Channel strip: Compressor ratio (mixer window, slice 1 of 4) | — | — | click only | Compressor Ratio: 4.06:1 |
| MMIX-F-K03 | strip COMP THRES knob | Channel strip: Compressor threshold (mixer window, slice 1 of 4) | — | — | click only | Compressor Threshold: -25.80 dB |
| MMIX-F-K04 | strip COMP REL knob | Channel strip: Compressor release (mixer window, slice 1 of 4) | — | — | click only | Compressor Release: 554 ms |
| MMIX-F-B11 | strip COMP FAST | Channel strip: Compressor fast attack (mixer window, slice 1 of 4) | — | — | click only | Compressor Fast Attack Off |
| MMIX-F-D03 | strip Gate gain-reduction lights | Channel strip: Left LED column (tooltip: Gate Gain Reduction) (mixer window, slice 1 of 4) | — | — | click only | Gate Gain Reduction |
| MMIX-F-D04 | strip Compressor gain-reduction lights | Channel strip: Right LED column (tooltip: Compressor Gain Reduction) (mixer window, slice 1 of 4) | — | — | click only | Compressor Gain Reduction |
| MMIX-F-B12 | strip Dynamics KEY | Channel strip: Sidechain key (mixer window, slice 1 of 4) | — | — | click only | Sidechain Key Off |
| MMIX-F-B13 | strip GATE ON | Channel strip: Gate on/off (mixer window, slice 1 of 4) | — | — | click only | Gate Disabled |
| MMIX-F-B14 | strip GATE EXP | Channel strip: Expander mode (mixer window, slice 1 of 4) | — | — | click only | Gate Expander Mode Off |
| MMIX-F-K07 | strip GATE RANGE knob | Channel strip: Gate range (mixer window, slice 1 of 4) | — | — | click only | Gate Range: -20.16 dB |
| MMIX-F-K08 | strip GATE THRES knob | Channel strip: Gate threshold (mixer window, slice 1 of 4) | — | — | click only | Gate Threshold: -38.90 dB |
| MMIX-F-K09 | strip GATE REL knob | Channel strip: Gate release (mixer window, slice 1 of 4) | — | — | click only | Gate Release: 554 ms |
| MMIX-F-K10 | strip GATE HOLD knob | Channel strip: Gate hold (mixer window, slice 1 of 4) | — | — | click only | Gate Hold: 0 ms |
| MMIX-F-B16 | strip GATE FAST | Channel strip: Gate fast attack (mixer window, slice 1 of 4) | — | — | click only | Gate Fast Attack Off |
| MMIX-F-B07 | Master compressor header light | Master strip: Section header light (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Disabled |
| MMIX-F-B09 | Master compressor ON | Master strip: Master compressor on/off (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Disabled |
| MMIX-F-D02 | Master compression meter | Master strip: Gain-reduction meter (mixer window, slice 1 of 4) | — | — | click only | no tooltip |
| MMIX-F-K05 | Master comp THRESHOLD knob | Master strip: Master compressor threshold (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Threshold: -14.88 dB |
| MMIX-F-K06 | Master comp RATIO knob | Master strip: Master compressor ratio (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Ratio: 2:1 |
| MMIX-F-K11 | Master comp ATTACK knob | Master strip: Master compressor attack (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Attack: 10.0 ms |
| MMIX-F-K12 | Master comp RELEASE knob | Master strip: Master compressor release (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Release: 0.6 s |
| MMIX-F-K13 | Master comp MAKE-UP knob | Master strip: Master compressor make-up gain (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Make-Up Gain: 2.87 dB |
| MMIX-F-B15 | Master comp EXTERNAL SIDE CHAIN KEY | Master strip: Master compressor external sidechain key (mixer window, slice 1 of 4) | — | — | click only | Master Compressor Sidechain Key Off |
| MMIX-F-D05 | strip EQ header light | Channel strip: EQ section on/off light (mixer window, slice 2 of 4) | — | — | click only | EQ Disabled |
| MMIX-F-B17 | strip EQ spectrum button | Channel strip: show channel spectrum EQ (mixer window, slice 2 of 4) | — | — | click only | Show in Spectrum EQ Window |
| MMIX-F-B18 | strip LPF ON | Channel strip: low-pass filter on (mixer window, slice 2 of 4) | — | — | click only | Low Pass Filter Disabled |
| MMIX-F-K14 | strip LPF kHz | Channel strip: low-pass frequency (mixer window, slice 2 of 4) | — | — | click only | Low Pass Filter Frequency: 3.54 kHz |
| MMIX-F-K15 | strip HPF Hz | Channel strip: high-pass frequency (mixer window, slice 2 of 4) | — | — | click only | High Pass Filter Frequency: 187.1 Hz |
| MMIX-F-B19 | strip HPF ON | Channel strip: high-pass filter on (mixer window, slice 2 of 4) | — | — | click only | High Pass Filter Disabled |
| MMIX-F-B21 | strip EQ filters to dyn S/C | Channel strip: filters feed dynamics side chain (mixer window, slice 2 of 4) | — | — | click only | Filters to Dynamics Sidechain Off |
| MMIX-F-B23 | strip HF BELL | Channel strip: HF bell/shelf switch (mixer window, slice 2 of 4) | — | — | click only | High Frequency Shelf Mode |
| MMIX-F-D08 | strip HF light | Channel strip: HF band on light (mixer window, slice 2 of 4) | — | — | click only | no tooltip |
| MMIX-F-K18 | strip HF dB | Channel strip: HF gain (mixer window, slice 2 of 4) | — | — | click only | High Frequency Gain: 0.00 dB |
| MMIX-F-K19 | strip HF kHz | Channel strip: HF frequency (mixer window, slice 2 of 4) | — | — | click only | High Frequency: 5.74 kHz |
| MMIX-F-K21 | strip HMF dB | Channel strip: HMF gain (mixer window, slice 2 of 4) | — | — | click only | High Mid Frequency Gain: 0.00 dB |
| MMIX-F-K23 | strip HMF kHz | Channel strip: HMF frequency (mixer window, slice 2 of 4) | — | — | click only | High Mid Frequency: 2.05 kHz |
| MMIX-F-D09 | strip HMF light | Channel strip: HMF band on light (mixer window, slice 2 of 4) | — | — | click only | no tooltip |
| MMIX-F-K24 | strip HMF Q | Channel strip: HMF Q (mixer window, slice 2 of 4) | — | — | click only | High Mid Frequency Q Value: 1.33 |
| MMIX-F-B26 | strip HMF ON | Channel strip: HMF/LMF on (mixer window, slice 2 of 4) | — | — | click only | Equalizer Disabled |
| MMIX-F-B28 | strip HMF E | Channel strip: E-series EQ (mixer window, slice 2 of 4) | — | — | click only | Equalizer E Mode (Constant Q) Disabled |
| MMIX-F-K26 | strip LMF dB | Channel strip: LMF gain (mixer window, slice 2 of 4) | — | — | click only | Low Mid Frequency Gain: 0.00 dB |
| MMIX-F-K28 | strip LMF kHz | Channel strip: LMF frequency (mixer window, slice 2 of 4) | — | — | click only | Low Mid Frequency: 632.5 Hz |
| MMIX-F-D10 | strip LMF light | Channel strip: LMF band on light (mixer window, slice 2 of 4) | — | — | click only | no tooltip |
| MMIX-F-K29 | strip LMF Q | Channel strip: LMF Q (mixer window, slice 2 of 4) | — | — | click only | Low Mid Frequency Q Value: 1.33 |
| MMIX-F-D11 | strip LF light | Channel strip: LF band on light (mixer window, slice 2 of 4) | — | — | click only | no tooltip |
| MMIX-F-K31 | strip LF Hz | Channel strip: LF frequency (mixer window, slice 2 of 4) | — | — | click only | Low Frequency: 154.9 Hz |
| MMIX-F-K32 | strip LF dB | Channel strip: LF gain (mixer window, slice 2 of 4) | — | — | click only | Low Frequency Gain: 0.00 dB |
| MMIX-F-B31 | strip LF BELL | Channel strip: LF bell/shelf switch (mixer window, slice 2 of 4) | — | — | click only | Low Frequency Shelf Mode |
| MMIX-F-D13 | strip INSERTS header light | Channel strip: insert section light (mixer window, slice 2 of 4) | — | — | click only | Insert FX Disconnected |
| MMIX-F-B33 | strip INSERTS BYPASS | Channel strip: bypass inserts (mixer window, slice 2 of 4) | — | — | click only | Bypass Master Insert FX Off |
| MMIX-F-B35 | strip EDIT INSERTS | Channel strip: edit inserts (mixer window, slice 2 of 4) | — | — | click only | Edit Inserts |
| MMIX-F-K16 | master FX1 LEVEL | Master strip: master FX 1 level (mixer window, slice 2 of 4) | — | — | click only | FX1 Master Send Level: 0.00 dB |
| MMIX-F-K17 | master FX2 LEVEL | Master strip: master FX 2 level (mixer window, slice 2 of 4) | — | — | click only | FX2 Master Send Level: 0.00 dB |
| MMIX-F-K20 | master FX3 LEVEL | Master strip: master FX 3 level (mixer window, slice 2 of 4) | — | — | click only | FX3 Master Send Level: 0.00 dB |
| MMIX-F-K22 | master FX4 LEVEL | Master strip: master FX 4 level (mixer window, slice 2 of 4) | — | — | click only | FX4 Master Send Level: 0.00 dB |
| MMIX-F-K25 | master FX5 LEVEL | Master strip: master FX 5 level (mixer window, slice 2 of 4) | — | — | click only | FX5 Master Send Level: 0.00 dB |
| MMIX-F-K27 | master FX6 LEVEL | Master strip: master FX 6 level (mixer window, slice 2 of 4) | — | — | click only | FX6 Master Send Level: 0.00 dB |
| MMIX-F-K30 | master FX7 LEVEL | Master strip: master FX 7 level (mixer window, slice 2 of 4) | — | — | click only | FX7 Master Send Level: 0.00 dB |
| MMIX-F-K33 | master FX8 LEVEL | Master strip: master FX 8 level (mixer window, slice 2 of 4) | — | — | click only | FX8 Master Send Level: 0.00 dB |
| MMIX-F-B20 | master FX1 EDIT | Master strip: edit FX 1 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX1 |
| MMIX-F-B22 | master FX2 EDIT | Master strip: edit FX 2 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX2 |
| MMIX-F-B24 | master FX3 EDIT | Master strip: edit FX 3 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX3 |
| MMIX-F-B25 | master FX4 EDIT | Master strip: edit FX 4 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX4 |
| MMIX-F-B27 | master FX5 EDIT | Master strip: edit FX 5 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX5 |
| MMIX-F-B29 | master FX6 EDIT | Master strip: edit FX 6 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX6 |
| MMIX-F-B30 | master FX7 EDIT | Master strip: edit FX 7 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX7 |
| MMIX-F-B32 | master FX8 EDIT | Master strip: edit FX 8 device (mixer window, slice 2 of 4) | — | — | click only | Edit FX8 |
| MMIX-F-D14 | master MASTER INSERTS light | Master strip: master inserts light (mixer window, slice 2 of 4) | — | — | click only | Master Insert FX Connected |
| MMIX-F-B34 | master MASTER INSERTS BYPASS | Master strip: bypass master inserts (mixer window, slice 2 of 4) | — | — | click only | Bypass Master Insert FX On |
| MMIX-F-B36 | master EDIT INSERTS | Master strip: edit master inserts (mixer window, slice 2 of 4) | — | — | click only | Edit Inserts |
| MMIX-F-B37 | master INSERTS PRE COMPRESSOR | Master strip: inserts before compressor (mixer window, slice 2 of 4) | — | — | click only | Insert Section Pre Compressor Off |
| MMIX-F-D06 | master FX1 LEDs | Master strip: FX1 activity LEDs (mixer window, slice 2 of 4) | — | — | click only | FX1 Send Level Meter |
| MMIX-F-D12 | master FX8 LEDs | Master strip: FX8 activity LEDs (mixer window, slice 2 of 4) | — | — | click only | FX8 Send Level Meter |
| MMIX-F-D07 | master FX1 name | Master strip: FX1 name display (mixer window, slice 2 of 4) | — | — | click only | no tooltip |
| MMIX-F-D15 | strip SEND header light | Channel strip: send section light (mixer window, slice 3 of 4) | — | — | click only | FX Sends Disabled |
| MMIX-F-B38 | strip SEND1 PRE | Channel strip: send 1 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX1 Send Off |
| MMIX-F-K36 | strip SEND1 LEVEL | Channel strip: send 1 level (mixer window, slice 3 of 4) | — | — | click only | FX1 Send Level: -12.04 dB |
| MMIX-F-B41 | strip SEND2 PRE | Channel strip: send 2 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX2 Send Off |
| MMIX-F-K37 | strip SEND2 LEVEL | Channel strip: send 2 level (mixer window, slice 3 of 4) | — | — | click only | FX2 Send Level: -12.04 dB |
| MMIX-F-B44 | strip SEND3 PRE | Channel strip: send 3 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX3 Send Off |
| MMIX-F-K40 | strip SEND3 LEVEL | Channel strip: send 3 level (mixer window, slice 3 of 4) | — | — | click only | FX3 Send Level: -12.04 dB |
| MMIX-F-B47 | strip SEND4 PRE | Channel strip: send 4 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX4 Send Off |
| MMIX-F-K43 | strip SEND4 LEVEL | Channel strip: send 4 level (mixer window, slice 3 of 4) | — | — | click only | FX4 Send Level: -12.04 dB |
| MMIX-F-B50 | strip SEND5 PRE | Channel strip: send 5 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX5 Send Off |
| MMIX-F-K46 | strip SEND5 LEVEL | Channel strip: send 5 level (mixer window, slice 3 of 4) | — | — | click only | FX5 Send Level: -12.04 dB |
| MMIX-F-B53 | strip SEND6 PRE | Channel strip: send 6 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX6 Send Off |
| MMIX-F-K49 | strip SEND6 LEVEL | Channel strip: send 6 level (mixer window, slice 3 of 4) | — | — | click only | FX6 Send Level: -12.04 dB |
| MMIX-F-B56 | strip SEND7 PRE | Channel strip: send 7 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX7 Send Off |
| MMIX-F-K52 | strip SEND7 LEVEL | Channel strip: send 7 level (mixer window, slice 3 of 4) | — | — | click only | FX7 Send Level: -12.04 dB |
| MMIX-F-B59 | strip SEND8 PRE | Channel strip: send 8 pre-fader (mixer window, slice 3 of 4) | — | — | click only | FX8 Send Off |
| MMIX-F-K55 | strip SEND8 LEVEL | Channel strip: send 8 level (mixer window, slice 3 of 4) | — | — | click only | FX8 Send Level: -12.04 dB |
| MMIX-F-K58 | strip WIDTH | Channel strip: stereo width (mixer window, slice 3 of 4) | — | — | click only | Stereo Width: 127 |
| MMIX-F-K59 | strip PAN | Channel strip: pan (mixer window, slice 3 of 4) | — | — | click only | Pan: 0 |
| MMIX-F-B62 | strip MUTE | Channel strip: mute (mixer window, slice 3 of 4) | — | — | click only | Mix Channel Mute Off |
| MMIX-F-B63 | strip SOLO | Channel strip: solo (mixer window, slice 3 of 4) | — | — | click only | Mix Channel Solo Off |
| MMIX-F-D16 | master RETURN1 name | Master strip: return 1 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B39 | master RETURN1 EDIT | Master strip: edit return 1 (mixer window, slice 3 of 4) | — | — | click only | Edit FX1 |
| MMIX-F-B40 | master RETURN1 M | Master strip: mute return 1 (mixer window, slice 3 of 4) | — | — | click only | FX1 Return Mute Off |
| MMIX-F-K34 | master RETURN1 LEVEL | Master strip: return 1 level (mixer window, slice 3 of 4) | — | — | click only | FX1 Return Level: 0.00 dB |
| MMIX-F-K35 | master RETURN1 PAN | Master strip: return 1 pan (mixer window, slice 3 of 4) | — | — | click only | FX1 Return Pan: 0 |
| MMIX-F-D17 | master RETURN1 LEDs | Master strip: return 1 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX1 Return Level Meter |
| MMIX-F-D18 | master RETURN2 name | Master strip: return 2 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B42 | master RETURN2 EDIT | Master strip: edit return 2 (mixer window, slice 3 of 4) | — | — | click only | Edit FX2 |
| MMIX-F-B43 | master RETURN2 M | Master strip: mute return 2 (mixer window, slice 3 of 4) | — | — | click only | FX2 Return Mute Off |
| MMIX-F-K38 | master RETURN2 LEVEL | Master strip: return 2 level (mixer window, slice 3 of 4) | — | — | click only | FX2 Return Level: 0.00 dB |
| MMIX-F-K39 | master RETURN2 PAN | Master strip: return 2 pan (mixer window, slice 3 of 4) | — | — | click only | FX2 Return Pan: 0 |
| MMIX-F-D19 | master RETURN2 LEDs | Master strip: return 2 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX2 Return Level Meter |
| MMIX-F-D20 | master RETURN3 name | Master strip: return 3 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B45 | master RETURN3 EDIT | Master strip: edit return 3 (mixer window, slice 3 of 4) | — | — | click only | Edit FX3 |
| MMIX-F-B46 | master RETURN3 M | Master strip: mute return 3 (mixer window, slice 3 of 4) | — | — | click only | FX3 Return Mute Off |
| MMIX-F-K41 | master RETURN3 LEVEL | Master strip: return 3 level (mixer window, slice 3 of 4) | — | — | click only | FX3 Return Level: 0.00 dB |
| MMIX-F-K42 | master RETURN3 PAN | Master strip: return 3 pan (mixer window, slice 3 of 4) | — | — | click only | FX3 Return Pan: 0 |
| MMIX-F-D21 | master RETURN3 LEDs | Master strip: return 3 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX3 Return Level Meter |
| MMIX-F-D22 | master RETURN4 name | Master strip: return 4 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B48 | master RETURN4 EDIT | Master strip: edit return 4 (mixer window, slice 3 of 4) | — | — | click only | Edit FX4 |
| MMIX-F-B49 | master RETURN4 M | Master strip: mute return 4 (mixer window, slice 3 of 4) | — | — | click only | FX4 Return Mute Off |
| MMIX-F-K44 | master RETURN4 LEVEL | Master strip: return 4 level (mixer window, slice 3 of 4) | — | — | click only | FX4 Return Level: 0.00 dB |
| MMIX-F-K45 | master RETURN4 PAN | Master strip: return 4 pan (mixer window, slice 3 of 4) | — | — | click only | FX4 Return Pan: 0 |
| MMIX-F-D23 | master RETURN4 LEDs | Master strip: return 4 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX4 Return Level Meter |
| MMIX-F-D24 | master RETURN5 name | Master strip: return 5 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B51 | master RETURN5 EDIT | Master strip: edit return 5 (mixer window, slice 3 of 4) | — | — | click only | Edit FX5 |
| MMIX-F-B52 | master RETURN5 M | Master strip: mute return 5 (mixer window, slice 3 of 4) | — | — | click only | FX5 Return Mute Off |
| MMIX-F-K47 | master RETURN5 LEVEL | Master strip: return 5 level (mixer window, slice 3 of 4) | — | — | click only | FX5 Return Level: 0.00 dB |
| MMIX-F-K48 | master RETURN5 PAN | Master strip: return 5 pan (mixer window, slice 3 of 4) | — | — | click only | FX5 Return Pan: 0 |
| MMIX-F-D25 | master RETURN5 LEDs | Master strip: return 5 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX5 Return Level Meter |
| MMIX-F-D26 | master RETURN6 name | Master strip: return 6 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B54 | master RETURN6 EDIT | Master strip: edit return 6 (mixer window, slice 3 of 4) | — | — | click only | Edit FX6 |
| MMIX-F-B55 | master RETURN6 M | Master strip: mute return 6 (mixer window, slice 3 of 4) | — | — | click only | FX6 Return Mute Off |
| MMIX-F-K50 | master RETURN6 LEVEL | Master strip: return 6 level (mixer window, slice 3 of 4) | — | — | click only | FX6 Return Level: 0.00 dB |
| MMIX-F-K51 | master RETURN6 PAN | Master strip: return 6 pan (mixer window, slice 3 of 4) | — | — | click only | FX6 Return Pan: 0 |
| MMIX-F-D27 | master RETURN6 LEDs | Master strip: return 6 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX6 Return Level Meter |
| MMIX-F-D28 | master RETURN7 name | Master strip: return 7 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B57 | master RETURN7 EDIT | Master strip: edit return 7 (mixer window, slice 3 of 4) | — | — | click only | Edit FX7 |
| MMIX-F-B58 | master RETURN7 M | Master strip: mute return 7 (mixer window, slice 3 of 4) | — | — | click only | FX7 Return Mute Off |
| MMIX-F-K53 | master RETURN7 LEVEL | Master strip: return 7 level (mixer window, slice 3 of 4) | — | — | click only | FX7 Return Level: 0.00 dB |
| MMIX-F-K54 | master RETURN7 PAN | Master strip: return 7 pan (mixer window, slice 3 of 4) | — | — | click only | FX7 Return Pan: 0 |
| MMIX-F-D29 | master RETURN7 LEDs | Master strip: return 7 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX7 Return Level Meter |
| MMIX-F-D30 | master RETURN8 name | Master strip: return 8 device name (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-B60 | master RETURN8 EDIT | Master strip: edit return 8 (mixer window, slice 3 of 4) | — | — | click only | Edit FX8 |
| MMIX-F-B61 | master RETURN8 M | Master strip: mute return 8 (mixer window, slice 3 of 4) | — | — | click only | FX8 Return Mute Off |
| MMIX-F-K56 | master RETURN8 LEVEL | Master strip: return 8 level (mixer window, slice 3 of 4) | — | — | click only | FX8 Return Level: 0.00 dB |
| MMIX-F-K57 | master RETURN8 PAN | Master strip: return 8 pan (mixer window, slice 3 of 4) | — | — | click only | FX8 Return Pan: 0 |
| MMIX-F-D31 | master RETURN8 LEDs | Master strip: return 8 activity LEDs (mixer window, slice 3 of 4) | — | — | click only | FX8 Return Level Meter |
| MMIX-F-D32 | master CONTROL ROOM OUT display | Master strip: control room out (mixer window, slice 3 of 4) | — | — | click only | no tooltip |
| MMIX-F-K60 | master CONTROL ROOM LEVEL | Master strip: control room level (mixer window, slice 3 of 4) | — | — | click only | Control Room Level: 0.00 dB |
| MMIX-F-D34 | strip output meter | Channel strip: level meter (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-S02 | strip fader handle | Channel strip: channel fader (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-B67 | strip OUTPUT menu arrow | Channel strip: output menu (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-D38 | strip OUTPUT display | Channel strip: output name display (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-B64 | master FADER RESET | Master strip: reset clip indicators (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-D33 | master FADER meter | Master strip: VU/peak level meter (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-B66 | master FADER MODE | Master strip: meter mode (mixer window, slice 4 of 4) | — | — | click only | Meter Mode: VU + Peak |
| MMIX-F-S01 | master FADER handle | Master strip: master fader (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-B65 | master DELAY COMP button | Master strip: delay compensation (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-D36 | master DELAY COMP OFF display | Master strip: delay comp state (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-D37 | master TOTAL DELAY display | Master strip: total delay (mixer window, slice 4 of 4) | — | — | click only | no tooltip |
| MMIX-F-B68 | master spectrum EQ button | Master strip: spectrum window (mixer window, slice 4 of 4) | — | — | click only | Show in Spectrum EQ Window |
| MMIX-F-D35 | master VU/PEAK label | Master strip: meter VU/PEAK label (mixer window, slice 4 of 4) | — | — | click only | no tooltip |

## Channel EQ — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| CEQ-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 2 / CC 31 | voice/MIDI or click | hover: 'Enabled: On' |
| CEQ-F-D05 | CHANEQ 1 tape | Device name tape (vertical) | Device Name | — | display/Remote item, not mapped | name tape: hover 'ChanEQ 1' |
| CEQ-F-B02 | HPF ON | High-pass filter on/off | HPF On | 11 / CC 40 | voice/MIDI or click | hover: 'HPF On' |
| CEQ-F-K07 | HPF Hz | High-pass filter frequency, 20 Hz to 4 kHz | HPF Frequency | 10 / CC 39 | voice/MIDI or click | hover: 'HPF Frequency: 20.0 Hz' |
| CEQ-F-B03 | LPF ON | Low-pass filter on/off | LPF On | 19 / CC 48 | voice/MIDI or click | hover: 'LPF On' |
| CEQ-F-K08 | LPF kHz | Low-pass filter frequency, 100 Hz to 20 kHz | LPF Frequency | 18 / CC 47 | voice/MIDI or click | hover: 'LPF Frequency: 20.00 kHz' |
| CEQ-F-K01 | LF dB | Low shelf boost/cut | LF Gain | 14 / CC 43 | voice/MIDI or click | hover: 'LF Gain: 0.00 dB' |
| CEQ-F-D01 | (LF light) | Light beside the LF dB knob | — | — | click only | light beside LF dB, no tooltip (by eye) |
| CEQ-F-B04 | LF Bell | Low band bell/shelf switch | LF Bell On | 12 / CC 41 | voice/MIDI or click | hover: 'LF Bell On' |
| CEQ-F-K09 | LF Hz | Low shelf frequency, 40 to 600 Hz | LF Frequency | 13 / CC 42 | voice/MIDI or click | hover: 'LF Frequency: 154.9 Hz' |
| CEQ-F-K02 | LMF dB | Low-mid boost/cut | LMF Gain | 16 / CC 45 | voice/MIDI or click | hover: 'LMF Gain: 0.00 dB' |
| CEQ-F-D02 | (LMF light) | Light beside the LMF dB knob | — | — | click only | light beside LMF dB, no tooltip (by eye) |
| CEQ-F-K03 | LMF Q | Low-mid width (Q), 0.70 to 2.50 | LMF Q | 17 / CC 46 | voice/MIDI or click | hover: 'LMF Q: 50.0 %' |
| CEQ-F-K10 | LMF kHz | Low-mid frequency, 200 Hz to 2 kHz | LMF Frequency | 15 / CC 44 | voice/MIDI or click | hover: 'LMF Frequency: 632.5 Hz' |
| CEQ-F-B05 | E Mode | E Mode on/off: keeps LMF/HMF bandwidth constant at all Gain settings | E Mode On | 1 / CC 30 | voice/MIDI or click | hover: 'E Mode On' |
| CEQ-F-K04 | HMF dB | High-mid boost/cut | HMF Gain | 8 / CC 37 | voice/MIDI or click | hover: 'HMF Gain: 0.00 dB' |
| CEQ-F-D03 | (HMF light) | Light beside the HMF dB knob | — | — | click only | light beside HMF dB, no tooltip (by eye) |
| CEQ-F-K05 | HMF Q | High-mid width (Q), 0.70 to 2.50 | HMF Q | 9 / CC 38 | voice/MIDI or click | hover: 'HMF Q: 50.0 %' |
| CEQ-F-K11 | HMF kHz | High-mid frequency, 600 Hz to 7 kHz | HMF Frequency | 7 / CC 36 | voice/MIDI or click | hover: 'HMF Frequency: 2.05 kHz' |
| CEQ-F-K06 | HF dB | High shelf boost/cut | HF Gain | 6 / CC 35 | voice/MIDI or click | hover: 'HF Gain: 0.00 dB' |
| CEQ-F-D04 | (HF light) | Light beside the HF dB knob | — | — | click only | light beside HF dB, no tooltip (by eye) |
| CEQ-F-K12 | HF kHz | High shelf frequency, 1.5 to 22 kHz | HF Frequency | 5 / CC 34 | voice/MIDI or click | hover: 'HF Frequency: 5.74 kHz' |
| CEQ-F-B06 | HF Bell | High band bell/shelf switch | HF Bell On | 4 / CC 33 | voice/MIDI or click | hover: 'HF Bell On' |
| CEQ-F-K13 | Gain | Output gain | Gain | 3 / CC 32 | voice/MIDI or click | hover: 'Gain: 0.00 dB' |
| CEQ-F-D06 | (LED column) | Level meter lights | — | — | click only | LED column, no tooltip (by eye) |

## Channel EQ — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| CEQ-B-D03 | CHANEQ 1 tape | Device name tape (back, vertical) | — | — | click/drag only (no Remote item) | name tape: hover 'ChanEQ 1' |
| CEQ-B-K01 | HMF Gain CV trim | CV amount for HMF Gain | — | — | click/drag only (no Remote item) | hover: 'HMF Gain CV Amt: 100.0 %' |
| CEQ-B-J01 | HMF Gain CV In | CV input for HMF Gain | HMF Gain CV Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'HMF Gain CV Input' |
| CEQ-B-K02 | HMF Freq CV trim | CV amount for HMF Frequency | — | — | click/drag only (no Remote item) | hover: 'HMF Frequency CV Amt: 100.0 %' |
| CEQ-B-J02 | HMF Freq CV In | CV input for HMF Frequency | HMF Freq CV Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'HMF Freq CV Input' |
| CEQ-B-K03 | HPF Freq CV trim | CV amount for HPF Frequency | — | — | click/drag only (no Remote item) | hover: 'HPF CV Amt: 100.0 %' |
| CEQ-B-J03 | HPF Freq CV In | CV input for HPF Frequency | HPF CV Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'HPF CV Input' |
| CEQ-B-K04 | LMF Gain CV trim | CV amount for LMF Gain | — | — | click/drag only (no Remote item) | hover: 'LMF Gain CV Amt: 100.0 %' |
| CEQ-B-J04 | LMF Gain CV In | CV input for LMF Gain | LMF Gain CV Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'LMF Gain CV Input' |
| CEQ-B-K05 | LPF Freq CV trim | CV amount for LPF Frequency | — | — | click/drag only (no Remote item) | hover: 'LPF CV Amt: 100.0 %' |
| CEQ-B-J05 | LPF Freq CV In | CV input for LPF Frequency | LPF CV Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'LPF CV Input' |
| CEQ-B-K06 | LMF Freq CV trim | CV amount for LMF Frequency | — | — | click/drag only (no Remote item) | hover: 'LMF Frequency CV Amt: 100.0 %' |
| CEQ-B-J06 | LMF Freq CV In | CV input for LMF Frequency | LMF Freq CV Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'LMF Freq CV Input' |
| CEQ-B-J07 | Input L | Audio input left | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to Mix Channel: To Insert FX' (text may continue past zoom edge) |
| CEQ-B-J08 | Input R | Audio input right | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to Mix Channel: To Insert FX' (text may continue past zoom edge) |
| CEQ-B-J09 | Output L | Audio output left | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to ChanDyn 1: Left Input' |
| CEQ-B-J10 | Output R | Audio output right | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to ChanDyn 1: Right Input' |
| CEQ-B-D01 | (routing icon 1) | Small icon at top right | — | — | click/drag only (no Remote item) | icon, no tooltip (by eye) |
| CEQ-B-D02 | (routing icon 2) | Small icon at right | — | — | click/drag only (no Remote item) | icon, no tooltip (by eye) |

## Channel Dynamics — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| CDYN-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 7 / CC 36 | voice/MIDI or click | hover: 'Enabled: On' |
| CDYN-F-D01 | CHANDYN 1 tape | Device name tape (vertical) | Device Name | — | display/Remote item, not mapped | name tape: hover 'ChanDyn 1' |
| CDYN-F-B02 | Comp ON | Compressor on/off | Comp On | 2 / CC 31 | voice/MIDI or click | hover: 'Comp On' |
| CDYN-F-B04 | Comp Peak | Compressor peak detection on/off (instead of RMS) | Comp Peak On | 3 / CC 32 | voice/MIDI or click | hover: 'Comp Peak On' |
| CDYN-F-B05 | Comp Fast | Compressor fast reaction on/off (fixed 3 ms for 20 dB) | Comp Fast On | 1 / CC 30 | voice/MIDI or click | hover: 'Comp Fast On' |
| CDYN-F-K03 | Input Gain | Level into the compressor, -18 to +18 dB | Input Gain | 15 / CC 44 | voice/MIDI or click | hover: 'Input Gain: 0.00 dB' |
| CDYN-F-K04 | Ratio | Compression ratio, 1 to infinity | Comp Ratio | 4 / CC 33 | voice/MIDI or click | hover: 'Comp Ratio: 4.00 : 1' |
| CDYN-F-K05 | Thresh (comp) | Level above which compression starts, -52 to 0 dB | Comp Threshold | 6 / CC 35 | voice/MIDI or click | hover: 'Comp Threshold: -26.0 dB' |
| CDYN-F-K06 | Release (comp) | How fast compression lets go, 100 to 1000 ms | Comp Release | 5 / CC 34 | voice/MIDI or click | hover: 'Comp Release: 550 ms' |
| CDYN-F-D02 | (Comp light column) | Compressor gain reduction lights | — | — | click only | comp light column, no tooltip (by eye) |
| CDYN-F-B03 | Gate ON | Gate/expander on/off | Gate On | 11 / CC 40 | voice/MIDI or click | hover: 'Gate On' |
| CDYN-F-B06 | Exp. | Expander instead of gate on/off | Gate Exp On | 8 / CC 37 | voice/MIDI or click | hover: 'Gate Exp On' |
| CDYN-F-K01 | Hold | Gate hold time, 0 to 4000 ms | Gate Hold | 10 / CC 39 | voice/MIDI or click | hover: 'Gate Hold: 0.0 ms' |
| CDYN-F-B07 | Gate Fast | Gate fast attack on/off (100 microseconds per 40 dB instead of 1.5 ms) | Gate Fast On | 9 / CC 38 | voice/MIDI or click | hover: 'Gate Fast On' |
| CDYN-F-K07 | Range | Gate range, 0 to 40 dB | Gate Range | 12 / CC 41 | voice/MIDI or click | hover: 'Gate Range: -20.00 dB' |
| CDYN-F-K08 | Thresh (gate) | Level at which the gate opens or closes, -52 to 0 dB | Gate Threshold | 14 / CC 43 | voice/MIDI or click | hover: 'Gate Threshold: -33.8 dB' |
| CDYN-F-K09 | Release (gate) | Time for the gate to go from open to fully closed, 100 to 1000 ms | Gate Release | 13 / CC 42 | voice/MIDI or click | hover: 'Gate Release: 550 ms' |
| CDYN-F-D03 | (Gate light column) | Gate activity lights | — | — | click only | gate light column, no tooltip (by eye) |
| CDYN-F-D04 | Connected (light) | Sidechain cable connected light | — | — | click only | Connected light, no tooltip (by eye) |
| CDYN-F-D05 | Active (light) | Sidechain active light | — | — | click only | Active light, no tooltip (by eye) |
| CDYN-F-B08 | Sidechain | Sidechain on/off | Sidechain | 17 / CC 46 | voice/MIDI or click | hover: 'Sidechain' |
| CDYN-F-K02 | Mix | Dry/wet mix | Mix | 16 / CC 45 | voice/MIDI or click | hover: 'Mix: 100.0 %' |

## Channel Dynamics — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| CDYN-B-D03 | CHANDYN 1 tape | Device name tape (back, vertical) | — | — | click/drag only (no Remote item) | hover on name tape: 'ChanDyn 1' (rack name) |
| CDYN-B-J03 | Comp Gain Reduction CV Out | CV output following compressor gain reduction | Comp CV Output | — | cable: right-click jack > device > jack name | hover (empty jack): 'Comp CV Output' |
| CDYN-B-J04 | Gate Gain CV Out | CV output following gate gain | GateExp CV Output | — | cable: right-click jack > device > jack name | hover (empty jack): 'GateExp CV Output' |
| CDYN-B-J01 | Sidechain In L | Sidechain input left | Left Key Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'Left Key Input' |
| CDYN-B-J02 | Sidechain In R | Sidechain input right | Right Key Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'Right Key Input' |
| CDYN-B-J05 | Input L | Audio input left | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to ChanEQ 1: Left Output' |
| CDYN-B-J06 | Input R | Audio input right | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to ChanEQ 1: Right Output' |
| CDYN-B-J07 | Output L | Audio output left | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to MasterComp 1: Left Input' |
| CDYN-B-J08 | Output R | Audio output right | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to MasterComp 1: Right Inpu...' (text cut at zoom edge) |
| CDYN-B-D01 | (routing icon 1) | Small icon at top right | — | — | click/drag only (no Remote item) | icon, no tooltip (by eye) |
| CDYN-B-D02 | (routing icon 2) | Small icon at right | — | — | click/drag only (no Remote item) | icon, no tooltip (by eye) |

## Master Bus Compressor — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MBC-F-B01 | Bypass/On/Off | 3-way device switch | Enabled | 2 / CC 31 | voice/MIDI or click | hover: 'Enabled: On' |
| MBC-F-D03 | MASTERCOMP 1 tape | Device name tape (vertical) | Device Name | — | display/Remote item, not mapped | name tape, no tooltip (by eye) |
| MBC-F-K01 | Threshold | Level above which compression starts, -30 to 0 dB | Threshold | 9 / CC 38 | voice/MIDI or click | hover: 'Threshold: -15.00 dB' |
| MBC-F-K05 | Ratio | Compression ratio, 2 to 10 | Ratio | 6 / CC 35 | voice/MIDI or click | hover: 'Ratio: 2:1' |
| MBC-F-K04 | Input Gain | Level into the compressor, -18 to +18 dB | Input Gain | 3 / CC 32 | voice/MIDI or click | hover: 'Input Gain: 0.00 dB' |
| MBC-F-D01 | (VU meter) | Gain reduction meter, 0 to 20 dB | — | — | click only | VU meter, no tooltip (by eye) |
| MBC-F-K02 | Attack-ms | Attack time, 0.1 to 30 ms | Attack | 1 / CC 30 | voice/MIDI or click | hover: 'Attack: 1ms' |
| MBC-F-K06 | Release-sec | Release time, 0.1 to 1.2 s or AUTO | Release | 7 / CC 36 | voice/MIDI or click | hover: 'Release: 0.6s' |
| MBC-F-K07 | Make-Up | Make-up gain, -5 to +15 dB | Make-Up Gain | 4 / CC 33 | voice/MIDI or click | hover: 'Make-Up Gain: 5.00 dB' |
| MBC-F-D02 | Connected (light) | Sidechain cable connected light | — | — | click only | Connected light, no tooltip (by eye) |
| MBC-F-D04 | Active (light) | Sidechain active light | — | — | click only | Active light, no tooltip (by eye) |
| MBC-F-B02 | Sidechain | Sidechain on/off | Sidechain | 8 / CC 37 | voice/MIDI or click | hover: 'Sidechain' |
| MBC-F-K03 | Mix | Dry/wet mix | Mix | 5 / CC 34 | voice/MIDI or click | hover: 'Mix: 100.0 %' |

## Master Bus Compressor — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MBC-B-D03 | MASTERCOMP 1 tape | Device name tape (back, vertical) | — | — | click/drag only (no Remote item) | hover on name tape: 'MasterComp 1' (rack name) |
| MBC-B-J03 | Comp Gain Reduction CV Out | CV output following gain reduction | GainRed CV Output | — | cable: right-click jack > device > jack name | hover (empty jack): 'GainRed CV Output' |
| MBC-B-J01 | Sidechain In L | Sidechain input left | Left Key Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'Left Key Input' |
| MBC-B-J02 | Sidechain In R | Sidechain input right | Right Key Input | — | cable: right-click jack > device > jack name | hover (empty jack): 'Right Key Input' |
| MBC-B-J04 | Input L | Audio input left | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to ChanDyn 1: Left Output' |
| MBC-B-J05 | Input R | Audio input right | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to ChanDyn 1: Right Output' |
| MBC-B-J06 | Output L | Audio output left | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to Mix Channel: From Insert F...' (text cut at zoom edge) |
| MBC-B-J07 | Output R | Audio output right | — | — | cable: right-click jack > device > jack name | hover (cabled): 'Connected to Mix Channel: From Insert F...' (text cut at zoom edge) |
| MBC-B-D01 | (routing icon 1) | Small icon at top right | — | — | click/drag only (no Remote item) | icon, no tooltip (by eye) |
| MBC-B-D02 | (routing icon 2) | Small icon at right | — | — | click/drag only (no Remote item) | icon, no tooltip (by eye) |

## Sweeper Modulation Effect — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SWPR-F-B03 | Bypass/On/Off | 3-way device switch | Enabled | 4 / CC 33 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Enabled: On" |
| SWPR-F-D01 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | [main panel (Phaser, Envelope view)] tooltip "Basic Phasing" |
| SWPR-F-B01 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | [main panel (Phaser, Envelope view)] tooltip "Select previous patch" |
| SWPR-F-B04 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | [main panel (Phaser, Envelope view)] tooltip "Select next patch" |
| SWPR-F-B05 | (folder) | Open patch browser | — | — | click only | [main panel (Phaser, Envelope view)] tooltip "Browse patch" |
| SWPR-F-B06 | (disk) | Save patch | — | — | click only | [main panel (Phaser, Envelope view)] tooltip "Save patch" |
| SWPR-F-B02 | (triangle) | Fold/unfold device | — | — | click only | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-D02 | BASIC PHASING tape | Patch name tape | Device Name | — | display/Remote item, not mapped | [main panel (Phaser, Envelope view)] tooltip "Basic Phasing" (tooltip is the patch name; 'Device Name' item not provable here) |
| SWPR-F-B07 | PHASER | Effect type: Phaser | Type | 32 / CC 61 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Effect Type"; clicked, view changed, set back to Phaser |
| SWPR-F-B08 | FLANGER | Effect type: Flanger | Type | — | display/Remote item, not mapped | [main panel (Phaser, Envelope view)] tooltip "Effect Type"; clicked, view changed, set back |
| SWPR-F-B09 | FILTER | Effect type: Filter | Type | — | display/Remote item, not mapped | [main panel (Phaser, Envelope view)] tooltip "Effect Type"; clicked, view changed, set back |
| SWPR-F-D03 | Stereo | Stereo / Dual Mono selector | Stereo Mode | 30 / CC 59 | voice/MIDI or click | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-K01 | LFO > Freq | LFO amount to Frequency | LFO Freq Mod | 18 / CC 47 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "LFO Freq Mod: 84.1 %" |
| SWPR-F-K07 | MOD > Freq | Modulator (envelope/follower) amount to Frequency | Env Freq Mod | 6 / CC 35 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Env Freq Mod: 0.0 %" |
| SWPR-F-K05 | Frequency | Phaser/flanger frequency | Freq | 16 / CC 45 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Freq: 798.2 Hz" |
| SWPR-F-K02 | Bandwidth | Phaser bandwidth | Bandwidth | 1 / CC 30 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Bandwidth: 79.5 %" |
| SWPR-F-K08 | Feedback | Feedback amount | Feedback | 10 / CC 39 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Feedback: 83.9 %" |
| SWPR-F-D04 | Stages | Number of phaser stages (up/down) | Phaser Stages | 25 / CC 54 | voice/MIDI or click | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-B10 | Polarity | Flip effect polarity | Polarity | 26 / CC 55 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Polarity" |
| SWPR-F-B11 | Mute Dry | Mute the dry signal | Mute Dry | 24 / CC 53 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Mute Dry" |
| SWPR-F-K03 | Spread | Stereo spread | Spread | 29 / CC 58 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Spread: 20.5 %" |
| SWPR-F-K09 | Dry/Wet | Balance dry and effect | DryWet | 3 / CC 32 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Dry-Wet: 100.0 %" (hover spells Dry-Wet; Remote name is DryWet) |
| SWPR-F-K06 | Volume | Output volume | Volume | 33 / CC 62 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Volume: -6.4 dB" |
| SWPR-F-K04 | LFO > Volume | LFO amount to Volume | LFO Amp Mod | 17 / CC 46 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "LFO Amp Mod: 0.0 %" |
| SWPR-F-K10 | MOD > Volume | Modulator amount to Volume | Env Amp Mod | 5 / CC 34 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Env Amp Mod: 0.0 %" |
| SWPR-F-B17 | LFO wave arrows | Pick LFO waveform (up/down) | LFO Wave | 22 / CC 51 | voice/MIDI or click | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-K12 | LFO rate | LFO rate (Hz, or note value when synced) | LFO Rate | 19 / CC 48 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "LFO Rate: 15.0 %" |
| SWPR-F-B19 | LFO SYNC | LFO tempo-sync on/off | LFO Sync | 20 / CC 49 | voice/MIDI or click | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-K11 | Rate Mod | Modulator amount to LFO rate | Rate Mod | 27 / CC 56 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Rate Mod: 0.0 %" |
| SWPR-F-B12 | Envelope tab | Modulator type: Envelope | ModType | 23 / CC 52 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Modulator Type"; clicked the other tab and back |
| SWPR-F-B13 | Audio Follower tab | Modulator type: Audio Follower | ModType | — | display/Remote item, not mapped | [main panel (Phaser, Envelope view)] tooltip "Modulator Type"; clicked, view changed, set back |
| SWPR-F-B15 | PRESET | Envelope preset menu | — | — | click only | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-B18 | EDIT | Envelope edit | — | — | click only | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-D07 | Envelope graph | Envelope shape | — | — | click only | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-B14 | LOOP | Loop the envelope | Env Loop | 7 / CC 36 | voice/MIDI or click | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-K13 | Env rate | Envelope time (s, or note value when synced) | Env Rate | 8 / CC 37 | voice/MIDI or click | [main panel (Phaser, Envelope view)] tooltip "Env Rate: 50.4 %" |
| SWPR-F-B20 | Env SYNC | Envelope tempo-sync on/off | BeatSync | 2 / CC 31 | voice/MIDI or click | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-B16 | AUDIO TRIG OFF | Audio trigger on/off | Trig On | 31 / CC 60 | voice/MIDI or click | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-D05 | LFO rate (synced) | LFO rate as a note value when SYNC is on (same spot as the LFO rate knob) | LFO Synced Rate | 21 / CC 50 | voice/MIDI or click | [main panel (Phaser, Envelope view)] not hovered: readout under the LFO rate knob (SYNC is off; the synced note value is not showing); name NOT proven |
| SWPR-F-D06 | Env rate (synced) | Envelope time as a note value when SYNC is on (same spot as the Env rate knob) | Env Synced Rate | 9 / CC 38 | voice/MIDI or click | [main panel (Phaser, Envelope view)] not hovered: readout under the Env rate knob (SYNC off); name NOT proven |
| SWPR-F-K14 | Threshold | Audio trigger threshold | — | — | click only | [main panel (Phaser, Envelope view)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-K101 | Drive | Filter drive | Filter Drive | 11 / CC 40 | voice/MIDI or click | [Filter view (Filter button; picture sweeper-filter-view_front_labeled.png)] tooltip "Filter Drive: 29.9 %" |
| SWPR-F-D101 | (Drive light) | Drive on light | — | — | click only | [Filter view (Filter button; picture sweeper-filter-view_front_labeled.png)] no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-F-K102 | Resonance | Filter resonance | Reso | 28 / CC 57 | voice/MIDI or click | [Filter view (Filter button; picture sweeper-filter-view_front_labeled.png)] tooltip "Reso: 78.0 %" |
| SWPR-F-B101 | Filter TYPE | Filter type menu (Notch 12 dB shown) | Filter Type | 12 / CC 41 | voice/MIDI or click | [Filter view (Filter button; picture sweeper-filter-view_front_labeled.png)] tooltip "Filter Type: Ladder LP 24dB" (while the panel display read 'Notch 12 dB': recorded as seen) |
| SWPR-F-K201 | Gain In | Audio follower input gain | Follow Gain | 14 / CC 43 | voice/MIDI or click | [Audio Follower view (picture sweeper-follower-view_front_labeled.png)] tooltip "Follow Gain: 0.00 dB" |
| SWPR-F-K202 | Attack | Audio follower attack | Follow Attack | 13 / CC 42 | voice/MIDI or click | [Audio Follower view (picture sweeper-follower-view_front_labeled.png)] tooltip "Follow Attack: 11 ms" |
| SWPR-F-K203 | Release | Audio follower release | Follow Release | 15 / CC 44 | voice/MIDI or click | [Audio Follower view (picture sweeper-follower-view_front_labeled.png)] tooltip "Follow Release: 110 ms" |
| SWPR-F-D201 | Follower graph | Follower display | — | — | click only | [Audio Follower view (picture sweeper-follower-view_front_labeled.png)] no tooltip in Reason (hovered 1.5-2.5 s) |

## Sweeper Modulation Effect — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SWPR-B-D01 | BASIC PHASING tape | Patch name tape (back) | — | — | click/drag only (no Remote item) | tooltip "Basic Phasing" |
| SWPR-B-K01 | Freq CV Amt (trim) | Amount for Freq CV | — | — | click/drag only (no Remote item) | tooltip "Freq CV Amt: 100.0 %" |
| SWPR-B-J01 | Freq CV In | CV input: Frequency | — | — | cable: right-click jack > device > jack name | tooltip "Freq CV Input" |
| SWPR-B-K02 | Feedback CV Amt (trim) | Amount for Feedback CV | — | — | click/drag only (no Remote item) | tooltip "Feedback CV Amt: 100.0 %" |
| SWPR-B-J03 | Feedback/Reso CV In | CV input: Feedback/Reso | — | — | cable: right-click jack > device > jack name | tooltip "Feedback CV Input" |
| SWPR-B-K03 | Spread CV Amt (trim) | Amount for Spread CV | — | — | click/drag only (no Remote item) | tooltip "Spread CV Amt: 100.0 %" |
| SWPR-B-J05 | Spread CV In | CV input: Spread | — | — | cable: right-click jack > device > jack name | tooltip "Spread CV Input" |
| SWPR-B-K04 | DryWet CV Amt (trim) | Amount for Dry/Wet CV | — | — | click/drag only (no Remote item) | tooltip "DryWet CV Amt: 100.0 %" |
| SWPR-B-J07 | Dry/Wet CV In | CV input: Dry/Wet | — | — | cable: right-click jack > device > jack name | tooltip "DryWet CV Input" |
| SWPR-B-J08 | Trig Envelope CV In | Trigger input for the envelope | — | — | cable: right-click jack > device > jack name | tooltip "Trig CV In" |
| SWPR-B-J02 | LFO CV Out | LFO CV output | — | — | cable: right-click jack > device > jack name | tooltip "LFO CV Output" |
| SWPR-B-J04 | Fol/Env CV Out | Follower/Envelope CV output | — | — | cable: right-click jack > device > jack name | tooltip "Env CV Output" |
| SWPR-B-J06 | Trigger CV Out | Trigger CV output | — | — | cable: right-click jack > device > jack name | tooltip "Trig CV Output" |
| SWPR-B-J09 | Audio Input L | Audio input left | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Smooth Bass: Main Out L" (cut off at edge); own jack name NOT read yet |
| SWPR-B-J10 | Audio Input R | Audio input right | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Smooth Bass: Main Out R" (cut off at edge); own jack name NOT read yet |
| SWPR-B-J11 | Audio Output L | Audio output left | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Default Synchronous: Le..." (cut off); own jack name NOT read yet |
| SWPR-B-J12 | Audio Output R | Audio output right | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Default Synchronous: Rig..." (cut off); own jack name NOT read yet |
| SWPR-B-D02 | (routing icon 1) | Routing icon (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-B-D03 | (routing icon 2) | Routing icon (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.5-2.5 s) |
| SWPR-B-D04 | (routing icon 3) | Routing icon (no tooltip) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.5-2.5 s) |

## Synchronous Effect Modulator — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SYNC-F-B03 | Bypass/On/Off | 3-way device switch | Enabled | 18 / CC 47 | voice/MIDI or click | tooltip "Enabled: On" |
| SYNC-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-D01 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | tooltip "Default Synchronous" |
| SYNC-F-B02 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| SYNC-F-B04 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| SYNC-F-B05 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| SYNC-F-B06 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| SYNC-F-D02 | INPUT meter | Input level light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-D06 | DEFAULT SYN tape | Patch name tape | Device Name | — | display/Remote item, not mapped | tooltip "Default Synchronous" (patch name; 'Device Name' item not provable here) |
| SYNC-F-B07 | TOOL 1 | Wave shape tool 1 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B08 | TOOL 2 | Wave shape tool 2 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B09 | TOOL 3 | Wave shape tool 3 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B10 | TOOL 4 | Wave shape tool 4 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B11 | TOOL 5 | Wave shape tool 5 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B12 | TOOL 6 | Wave shape tool 6 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B13 | TOOL 7 | Wave shape tool 7 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B14 | TOOL 8 | Wave shape tool 8 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B15 | TOOL 9 | Wave shape tool 9 (draws the shape on the selected track) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B16 | FREE | Free-run mode (no tempo sync) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B17 | RATE 1/64 | Wave rate 1/64 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B18 | RATE 1/32 | Wave rate 1/32 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B19 | RATE 1/16T | Wave rate 1/16T | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B20 | RATE 1/16 | Wave rate 1/16 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B21 | RATE 1/8T | Wave rate 1/8T | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B22 | RATE 1/8 | Wave rate 1/8 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B23 | RATE 1/4 | Wave rate 1/4 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B24 | RATE 1/2 | Wave rate 1/2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B25 | RATE 1/1 | Wave rate 1/1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B26 | SPEED x2 | Speed multiplier x2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B27 | SPEED x1 | Speed multiplier x1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B28 | SPEED x0.5 | Speed multiplier x0.5 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K01 | MASTER OFFSET | Master offset knob | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-D03 | MASTER OFFSET value | Master offset readout | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K02 | PHASE | Phase knob | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K03 | DIM | Dim knob | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B29 | TRACK 1 | Select track 1 (yellow) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B32 | TRACK 2 | Select track 2 (magenta) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B36 | TRACK 3 | Select track 3 (blue) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B30 | TRACK 1 FRZ | Freeze track 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B31 | TRACK 1 KILL | Kill track 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B33 | TRACK 2 FRZ | Freeze track 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B34 | TRACK 2 KILL | Kill track 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B35 | TRACK 3 FRZ | Freeze track 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B37 | TRACK 3 KILL | Kill track 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-D04 | Wave display | Curve drawing/preview area for the 3 tracks | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-B38 | MOD CTRL | Show/hide the modulation controls row | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K04 | MOD 1 | Modulation amount knob 1 (above the main knob 1) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K05 | MOD 2 | Modulation amount knob 2 (above the main knob 2) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K06 | MOD 3 | Modulation amount knob 3 (above the main knob 3) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K07 | MOD 4 | Modulation amount knob 4 (above the main knob 4) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K08 | MOD 5 | Modulation amount knob 5 (above the main knob 5) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K09 | MOD 6 | Modulation amount knob 6 (above the main knob 6) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K10 | MOD 7 | Modulation amount knob 7 (above the main knob 7) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K11 | MOD 8 | Modulation amount knob 8 (above the main knob 8) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K12 | MOD 9 | Modulation amount knob 9 (above the main knob 9) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K13 | MOD 10 | Modulation amount knob 10 (above the main knob 10) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-F-K14 | Dist Amount | Distortion amount | Dist Amount | 12 / CC 41 | voice/MIDI or click | tooltip "Dist Amount: 50%" |
| SYNC-F-K15 | Dist Character | Distortion character | Dist Character | 13 / CC 42 | voice/MIDI or click | tooltip "Dist Character: 50%" |
| SYNC-F-K16 | Filter Freq | Filter frequency | Filter Freq | 19 / CC 48 | voice/MIDI or click | tooltip "Filter Freq: 75%" |
| SYNC-F-K17 | Filter Resonance | Filter resonance | Filter Reso | 22 / CC 51 | voice/MIDI or click | tooltip "Filter Reso: 0%" |
| SYNC-F-K18 | Delay Amount | Delay amount | Delay  Amount | 1 / CC 30 | voice/MIDI or click | tooltip "Delay Amount: 50%" |
| SYNC-F-K19 | Delay Time | Delay time (note value when Sync is on) | Delay Synched Time | 9 / CC 38 | voice/MIDI or click | tooltip "Delay Synced Time: 3/16" |
| SYNC-F-K20 | Delay Feedback | Delay feedback | Delay Feedback | 2 / CC 31 | voice/MIDI or click | tooltip "Delay Feedback: 50%" |
| SYNC-F-K21 | Reverb Amount | Reverb amount | Reverb Amount | 27 / CC 56 | voice/MIDI or click | tooltip "Reverb Amount: 50%" |
| SYNC-F-K22 | Reverb Decay | Reverb decay | Reverb Decay | 29 / CC 58 | voice/MIDI or click | tooltip "Reverb Decay: 50%" |
| SYNC-F-K23 | Level | Level (In/Out switch below) | Level | 24 / CC 53 | voice/MIDI or click | tooltip "Level: 0.0 dB" |
| SYNC-F-D05 | Delay Time (ms) | Delay time in ms (same knob as Delay Time; shows when Sync is off) | Delay Time | 11 / CC 40 | voice/MIDI or click | not hovered: same knob as Delay Time; its Remote name 'Delay Time' (ms) NOT proven by tooltip (tooltip read 'Delay Synced Time' because Sync is on) |
| SYNC-F-S01 | Dist type | Distortion type slider (Dist 1 / Dist 2 / Lo-Fi / Ring Mod) | Dist Type | 16 / CC 45 | voice/MIDI or click | tooltip "Dist Type: Dist 1" |
| SYNC-F-B39 | Post Filter | Put the filter after the distortion | Dist Post Filter | 15 / CC 44 | voice/MIDI or click | tooltip "Dist Post Filter" |
| SYNC-F-S02 | Filter type | Filter type slider (HP / BP / LP / Comb) | Filter Type | 23 / CC 52 | voice/MIDI or click | tooltip "Filter Type: LP" |
| SYNC-F-K24 | Lag | Filter lag knob | Filter Lag | 20 / CC 49 | voice/MIDI or click | tooltip "Filter Lag: 0%" |
| SYNC-F-B40 | Keep Pitch | Keep pitch when delay time changes | Delay Keep Pitch | 3 / CC 32 | voice/MIDI or click | tooltip "Delay Keep Pitch" |
| SYNC-F-B41 | Sync | Delay tempo sync | Delay Tempo Sync | 10 / CC 39 | voice/MIDI or click | tooltip "Delay Tempo Sync" |
| SYNC-F-B43 | Ping Pong | Ping-pong delay | Delay Ping Pong | 6 / CC 35 | voice/MIDI or click | tooltip "Delay Ping Pong" |
| SYNC-F-B42 | Roll | Delay roll (hold feedback) | Delay Roll | 7 / CC 36 | voice/MIDI or click | tooltip "Delay Roll" |
| SYNC-F-B44 | Delay Send/Return | Delay as send or return effect | Delay SendReturn | 8 / CC 37 | voice/MIDI or click | tooltip "Delay Send/Return: Send" |
| SYNC-F-K28 | Pan | Delay pan | Delay Pan | 5 / CC 34 | voice/MIDI or click | tooltip "Delay Pan: 50%" |
| SYNC-F-K25 | Reverb Size | Reverb size | Reverb Size | 32 / CC 61 | voice/MIDI or click | tooltip "Reverb Size: 50%" |
| SYNC-F-K26 | Reverb Damp | Reverb damping | Reverb Damp | 28 / CC 57 | voice/MIDI or click | tooltip "Reverb Damp: 20%" |
| SYNC-F-B45 | Reverb Send/Return | Reverb as send or return effect | Reverb SendReturn | 31 / CC 60 | voice/MIDI or click | tooltip "Reverb Send/Return: Return" |
| SYNC-F-B46 | Level In/Out | Level knob works on In or Out | Level InOut | 25 / CC 54 | voice/MIDI or click | tooltip "Level In/Out: Out" |
| SYNC-F-K27 | Dry/Wet | Dry/wet balance | DryWet | 17 / CC 46 | voice/MIDI or click | tooltip "Dry/Wet: 100%" |
| SYNC-F-K29 | Master Level | Master output level | Master Level | 26 / CC 55 | voice/MIDI or click | tooltip "Master Level: 0.0 dB" |
| SYNC-F-B47 | DIST | Distortion section on/off | Dist On | 14 / CC 43 | voice/MIDI or click | tooltip "Dist On" |
| SYNC-F-B48 | FILTER | Filter section on/off | Filter On | 21 / CC 50 | voice/MIDI or click | tooltip "Filter On" |
| SYNC-F-B49 | DELAY | Delay section on/off | Delay On | 4 / CC 33 | voice/MIDI or click | tooltip "Delay On" |
| SYNC-F-B50 | REVERB | Reverb section on/off | Reverb On | 30 / CC 59 | voice/MIDI or click | tooltip "Reverb On" |

## Synchronous Effect Modulator — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| SYNC-B-K01 | Curve 1 CV trim | Amount for Curve 1 CV | — | — | click/drag only (no Remote item) | tooltip "Curve 1 CV Amount: 100%" |
| SYNC-B-J01 | Curve 1 CV In | CV input: curve 1 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 1 CV In" |
| SYNC-B-J02 | Freeze 1 CV In | CV input: freeze track 1 | — | — | cable: right-click jack > device > jack name | tooltip "Freeze 1 CV In" |
| SYNC-B-J03 | Curve 1 CV Out | CV output: curve 1 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 1 CV Out" |
| SYNC-B-J04 | Curve 1 Inverted CV Out | CV output: inverted curve 1 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 1 Inv CV Out" |
| SYNC-B-K02 | Curve 2 CV trim | Amount for Curve 2 CV | — | — | click/drag only (no Remote item) | tooltip "Curve 2 CV Amount: 100%" |
| SYNC-B-J05 | Curve 2 CV In | CV input: curve 2 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 2 CV In" |
| SYNC-B-J06 | Freeze 2 CV In | CV input: freeze track 2 | — | — | cable: right-click jack > device > jack name | tooltip "Freeze 2 CV In" |
| SYNC-B-J07 | Curve 2 CV Out | CV output: curve 2 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 2 CV Out" |
| SYNC-B-J08 | Curve 2 Inverted CV Out | CV output: inverted curve 2 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 2 Inv CV Out" |
| SYNC-B-K03 | Curve 3 CV trim | Amount for Curve 3 CV | — | — | click/drag only (no Remote item) | tooltip "Curve 3 CV Amount: 100%" |
| SYNC-B-J13 | Curve 3 CV In | CV input: curve 3 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 3 CV In" |
| SYNC-B-J14 | Freeze 3 CV In | CV input: freeze track 3 | — | — | cable: right-click jack > device > jack name | tooltip "Freeze 3 CV In" |
| SYNC-B-J15 | Curve 3 CV Out | CV output: curve 3 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 3 CV Out" |
| SYNC-B-J16 | Curve 3 Inverted CV Out | CV output: inverted curve 3 | — | — | cable: right-click jack > device > jack name | tooltip "Curve 3 Inv CV Out" |
| SYNC-B-K04 | Master Level CV trim | Amount for Master Level CV | — | — | click/drag only (no Remote item) | tooltip "Master Level CV Amount: 100%" |
| SYNC-B-J17 | Master Level CV In | CV input: master level | — | — | cable: right-click jack > device > jack name | tooltip "Master Level CV In" |
| SYNC-B-J09 | Audio In L | Audio input left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Basic Phasing: Left Output"; this jack's own name NOT read yet |
| SYNC-B-J10 | Audio In R | Audio input right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Basic Phasing: Right Output"; this jack's own name NOT read yet |
| SYNC-B-J11 | Audio Out L | Audio output left | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Mix Channel: From Insert FX..." (cut off); own jack name NOT read yet |
| SYNC-B-J12 | Audio Out R | Audio output right | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Mix Channel: From Insert FX..." (cut off); own jack name NOT read yet |
| SYNC-B-D03 | (routing icon 1) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-B-D04 | (routing icon 2) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-B-D05 | (routing icon 3) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-B-D06 | (routing icon 4) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-B-D07 | (routing icon 5) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| SYNC-B-D02 | DEFAULT SYN tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | tooltip "Default Synchronous" |
| SYNC-B-D01 | (triangle) back | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Audiomatic Retro Transformer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AUDM-F-B02 | Bypass/On/Off | 3-way device switch | Enabled | 2 / CC 31 | voice/MIDI or click | tooltip "Enabled: On" |
| AUDM-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-F-D02 | AUDIOMATIC 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tooltip "Audiomatic 1" (device name) |
| AUDM-F-D01 | Input meter | Input level lights (6) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-F-K02 | Gain | Input gain | Input Gain | 3 / CC 32 | voice/MIDI or click | tooltip "Input Gain: 0.0 dB" |
| AUDM-F-D03 | (screen) | Picture screen that changes with the chosen preset | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-F-B03 | Preset Tape | Preset button: Tape | Preset | 4 / CC 33 | voice/MIDI or click | tooltip "Preset" |
| AUDM-F-B04 | Preset Hi-Fi | Preset button: Hi-Fi | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B05 | Preset Bright | Preset button: Bright | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B06 | Preset Bottom | Preset button: Bottom | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B07 | Preset Spread | Preset button: Spread | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B08 | Preset Radio | Preset button: Radio | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B09 | Preset VHS | Preset button: VHS | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B10 | Preset Vinyl | Preset button: Vinyl | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B11 | Preset mp3 | Preset button: mp3 | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B12 | Preset Psyche | Preset button: Psyche | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B13 | Preset Cracked | Preset button: Cracked | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B14 | Preset Gadget | Preset button: Gadget | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B15 | Preset Circuit | Preset button: Circuit | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B16 | Preset Wash | Preset button: Wash | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B17 | Preset PVC | Preset button: PVC | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-B18 | Preset Eerie | Preset button: Eerie | Preset | — | display/Remote item, not mapped | tooltip "Preset" |
| AUDM-F-K01 | Transform | Transform amount | Transform | 5 / CC 34 | voice/MIDI or click | tooltip "Transform: 50%" |
| AUDM-F-K03 | Dry/Wet | Dry/wet balance | Dry Wet | 1 / CC 30 | voice/MIDI or click | tooltip "Dry Wet: 100%" (hover spells 'Dry Wet'; read as 'Dry/Wet: 100%' from the zoom) |
| AUDM-F-K04 | Volume | Output volume | Volume | 6 / CC 35 | voice/MIDI or click | tooltip "Volume: 0.0 dB" |

## Audiomatic Retro Transformer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| AUDM-B-K01 | Transform CV trim | Amount for Transform CV | — | — | click/drag only (no Remote item) | tooltip "Transform CV Trim: 100%" |
| AUDM-B-J01 | Transform CV In | CV input: Transform | — | — | cable: right-click jack > device > jack name | tooltip "Transform CV Input" |
| AUDM-B-K02 | Dry-Wet CV trim | Amount for Dry-Wet CV | — | — | click/drag only (no Remote item) | tooltip "Dry Wet CV Trim: 100%" |
| AUDM-B-J02 | Dry-Wet CV In | CV input: Dry-Wet | — | — | cable: right-click jack > device > jack name | tooltip "Dry Wet CV Input" |
| AUDM-B-J03 | Audio In L | Audio input left | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Pad Rhythmification: Left Ou..." (cut off); own jack name NOT read yet |
| AUDM-B-J04 | Audio In R | Audio input right | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Pad Rhythmification: Right ..." (cut off); own jack name NOT read yet |
| AUDM-B-J05 | Audio Out L | Audio output left | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Vocoder 1: Left Carrier"; own jack name NOT read yet |
| AUDM-B-J06 | Audio Out R | Audio output right | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Vocoder 1: Right Carrier"; own jack name NOT read yet |
| AUDM-B-D03 | (routing icon 1) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-B-D04 | (routing icon 2) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-B-D06 | (routing icon 3) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-B-D07 | (routing icon 4) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-B-D08 | (routing icon 5) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-B-D02 | AUDIOMATIC 1 tape (back) | Device name tape (back) | — | — | click/drag only (no Remote item) | tooltip "Audiomatic 1" |
| AUDM-B-D01 | (triangle) back | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| AUDM-B-D05 | Speaker grille | Decoration (speaker grille) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Neptune Pitch Adjuster — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| NEPT-F-B02 | Bypass/On/Off | 3-way device switch | Enabled | 4 / CC 33 | voice/MIDI or click | tooltip "Enabled: On" |
| NEPT-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-D01 | Input meter | Input level lights | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-D02 | FF logo | Powered by FF logo | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-D07 | NEPTUNE 1 tape | Device name tape | Device Name | — | display/Remote item, not mapped | tooltip "Neptune 1" (device name) |
| NEPT-F-B05 | LOW FREQ | Input: low-frequency mode | Low Freq Input | 8 / CC 37 | voice/MIDI or click | tooltip "Low Freq Input" |
| NEPT-F-B06 | WIDE VIBRATO | Input: wide vibrato | Wide Vibrato | 25 / CC 54 | voice/MIDI or click | tooltip "Wide Vibrato" |
| NEPT-F-B13 | LIVE MODE | Input: live mode | Live Mode | 7 / CC 36 | voice/MIDI or click | tooltip "Live Mode" |
| NEPT-F-B17 | MIDI | MIDI destination button (cycles between the three lights) | MIDI Destination | 9 / CC 38 | voice/MIDI or click | tooltip "MIDI Destination" |
| NEPT-F-B16 | MIDI (dup) | Remote duplicate of MIDI Destination (same button) | Midi Destination | 10 / CC 39 | voice/MIDI or click | not hovered separately: same spot as MIDI; Remote item with a case-variant duplicate name; probably the same control as the row above; NOT proven |
| NEPT-F-D10 | TO PITCH ADJUST | MIDI goes to Pitch Adjust (light) | — | — | click only | tooltip "MIDI Destination" |
| NEPT-F-D11 | TO VOICE SYNTH | MIDI goes to Voice Synth (light) | — | — | click only | tooltip "MIDI Destination" |
| NEPT-F-D12 | MIDI INPUT | MIDI input light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-D08 | BEND RANGE | Pitch bend range (stepper) | Pitch Bend Range | 16 / CC 45 | voice/MIDI or click | tooltip "Pitch Bend Range: 7" |
| NEPT-F-S04 | Pitch wheel | Pitch bend wheel | Pitch Bend | 15 / CC 44 | voice/MIDI or click | tooltip "Pitch Bend: 0" |
| NEPT-F-S05 | Pitch wheel (dup) | Remote duplicate 'pitch bend' (same wheel) | pitch bend | 26 / CC 55 | voice/MIDI or click | not hovered separately: same wheel as Pitch wheel; Remote item with a case-variant duplicate name; probably the same control as the row above; NOT proven |
| NEPT-F-S06 | Mod wheel | Mod wheel (vibrato wheel) | Mod Wheel | 11 / CC 40 | voice/MIDI or click | tooltip "Mod Wheel: 0" |
| NEPT-F-S07 | Mod wheel (dup) | Remote duplicate 'Mod wheel' (same wheel) | Mod wheel | 12 / CC 41 | voice/MIDI or click | not hovered separately: same wheel as Mod wheel; Remote item with a case-variant duplicate name; probably the same control as the row above; NOT proven |
| NEPT-F-K02 | VIBRATO RATE | Vibrato rate | Vibrato Rate | 22 / CC 51 | voice/MIDI or click | tooltip "Vibrato Rate: 64" |
| NEPT-F-K03 | VIBRATO RATE (dup) | Remote duplicate 'Vibrato rate' (same knob) | Vibrato rate | 23 / CC 52 | voice/MIDI or click | not hovered separately: same knob as VIBRATO RATE; Remote item with a case-variant duplicate name; probably the same control as the row above; NOT proven |
| NEPT-F-D04 | ROOT display | Root key display | — | — | click only | tooltip "Root Key"; no Remote item |
| NEPT-F-B07 | ROOT stepper | Root key up/down | — | — | click only | tooltip "Root Key"; no Remote item |
| NEPT-F-D05 | SCALE display | Scale name display | — | — | click only | tooltip "Scale"; no Remote item |
| NEPT-F-B08 | SCALE stepper | Scale up/down | — | — | click only | tooltip "Scale"; no Remote item |
| NEPT-F-B09 | SCALE MEMORY 1 | Scale memory slot 1 | Scale Memory | 19 / CC 48 | voice/MIDI or click | tooltip "Scale Memory" |
| NEPT-F-B10 | SCALE MEMORY 2 | Scale memory slot 2 | Scale Memory | — | display/Remote item, not mapped | tooltip "Scale Memory" |
| NEPT-F-B11 | SCALE MEMORY 3 | Scale memory slot 3 | Scale Memory | — | display/Remote item, not mapped | tooltip "Scale Memory" |
| NEPT-F-B12 | SCALE MEMORY 4 | Scale memory slot 4 | Scale Memory | — | display/Remote item, not mapped | tooltip "Scale Memory" |
| NEPT-F-S01 | CATCH ZONE SIZE | Catch zone slider (handle) | Catch Zone | 1 / CC 30 | voice/MIDI or click | tooltip "Catch Zone Size: 157" (Remote name is 'Catch Zone') |
| NEPT-F-D09 | Catch graph | Note catch display | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B18 | Key C | On-screen key C (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B19 | Key C# | On-screen key C# (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B20 | Key D | On-screen key D (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B21 | Key D# | On-screen key D# (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B22 | Key E | On-screen key E (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B23 | Key F | On-screen key F (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B24 | Key F# | On-screen key F# (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B25 | Key G | On-screen key G (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B26 | Key G# | On-screen key G# (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B27 | Key A | On-screen key A (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B28 | Key A# | On-screen key A# (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B29 | Key B | On-screen key B (note on/off for scale) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-F-B15 | PITCH ADJUST | Pitch adjust on/off | Pitch Adjust On/Off | 14 / CC 43 | voice/MIDI or click | tooltip "Pitch Adjust On/Off" |
| NEPT-F-B14 | PITCH ADJUST amount? | Remote item 'Pitch Adjust Amount': panel control NOT found | Pitch Adjust Amount | 13 / CC 42 | voice/MIDI or click | not located: no panel control is known for this Remote item; row placed on the PITCH ADJUST button only so the checker has a position; NOT proven |
| NEPT-F-K04 | CORRECTION SPEED | Correction speed | Correction Speed | 3 / CC 32 | voice/MIDI or click | tooltip "Correction Speed: 64" |
| NEPT-F-K05 | PRESERVE EXPRESSION | Preserve expression | Preserve Expression | 18 / CC 47 | voice/MIDI or click | tooltip "Preserve Expression: 0" |
| NEPT-F-B03 | TRANSPOSE | Transpose on/off | Transpose On/Off | 21 / CC 50 | voice/MIDI or click | tooltip "Transpose On/Off" |
| NEPT-F-D03 | SEMI | Transpose semitones (stepper) | Semitones | 20 / CC 49 | voice/MIDI or click | tooltip "Semitones: 0" |
| NEPT-F-D06 | CENT | Transpose cents (stepper) | Cent | 2 / CC 31 | voice/MIDI or click | tooltip "Cents: 0" (Remote name is 'Cent') |
| NEPT-F-B04 | FORMANT | Formant on/off | Formant On/Off | 5 / CC 34 | voice/MIDI or click | tooltip "Formant On/Off" |
| NEPT-F-K01 | SHIFT | Formant shift | Formant Shift | 6 / CC 35 | voice/MIDI or click | tooltip "Formant Shift: 0" |
| NEPT-F-S02 | PITCHED SIGNAL | Mixer fader: pitched signal level | Pitched Signal Level | 17 / CC 46 | voice/MIDI or click | no tooltip on the handle or the rail (3 tries); name from the Remote list and the panel label |
| NEPT-F-S03 | VOICE SYNTH | Mixer fader: voice synth level | Voice Synth Level | 24 / CC 53 | voice/MIDI or click | no tooltip on the handle or the rail (3 tries); name from the Remote list and the panel label |

## Neptune Pitch Adjuster — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| NEPT-B-D01 | (seq icon 1) | Sequencer control icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-B-D02 | (seq icon 2) | Sequencer control icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-B-D04 | Vent holes | Decoration | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-B-D03 | VOID IF REMOVED sticker | Decoration | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| NEPT-B-J01 | Note (Mono CV In) | Sequencer control: note CV input | — | — | cable: right-click jack > device > jack name | tooltip "Mono CV Input" |
| NEPT-B-J02 | Gate (Mono Gate In) | Sequencer control: gate input | — | — | cable: right-click jack > device > jack name | tooltip "Mono Gate Input" |
| NEPT-B-K01 | Bend trim | Amount for Bend CV | — | — | click/drag only (no Remote item) | tooltip "Pitch Bend Input: 127" |
| NEPT-B-K02 | Vibrato trim | Amount for Vibrato CV | — | — | click/drag only (no Remote item) | tooltip "Mod Wheel Modulation Input: 127" |
| NEPT-B-K03 | Formant trim | Amount for Formant CV | — | — | click/drag only (no Remote item) | tooltip "Formant Shift Input: 127" |
| NEPT-B-J03 | Bend CV In | CV input: pitch bend | — | — | cable: right-click jack > device > jack name | tooltip "Pitch Bend Input" |
| NEPT-B-J04 | Vibrato CV In | CV input: vibrato (mod wheel) | — | — | cable: right-click jack > device > jack name | tooltip "Mod Wheel Modulation Input" |
| NEPT-B-J05 | Formant CV In | CV input: formant shift | — | — | cable: right-click jack > device > jack name | tooltip "Formant Shift Input" |
| NEPT-B-J06 | Pitch CV Out | CV output: pitch (after pitch adjuster/transpose) | — | — | cable: right-click jack > device > jack name | tooltip "Pitch Output" |
| NEPT-B-J07 | Amplitude CV Out | CV output: amplitude | — | — | cable: right-click jack > device > jack name | tooltip "Amplitude Output" |
| NEPT-B-J08 | Audio In L | Audio input left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Vocoder 1: Left Output"; this jack's own name NOT read yet |
| NEPT-B-J09 | Audio In R | Audio input right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Vocoder 1: Right Output"; this jack's own name NOT read yet |
| NEPT-B-J10 | Voice Synth Out L | Voice synth output left | — | — | cable: right-click jack > device > jack name | tooltip "Voice Synth Left Output" |
| NEPT-B-J11 | Voice Synth Out R | Voice synth output right | — | — | cable: right-click jack > device > jack name | tooltip "Voice Synth Right Output" |
| NEPT-B-J12 | Audio Out L | Audio output left | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Basic Pulverisation: Left Inp..." (cut off); own jack name NOT read yet |
| NEPT-B-J13 | Audio Out R | Audio output right | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Basic Pulverisation: Right In..." (cut off); own jack name NOT read yet |

## Pulveriser — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PULV-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-F-B02 | Bypass/On/Off | 3-way device switch | Enabled | 3 / CC 32 | voice/MIDI or click | tooltip "Enabled: On" |
| PULV-F-D01 | (red light) | Red light next to the switch | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-F-D02 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | tooltip "Basic Pulverisation" |
| PULV-F-B03 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| PULV-F-B06 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| PULV-F-B04 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| PULV-F-B05 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| PULV-F-D06 | BASIC PULVER tape | Patch name tape | Device Name | — | display/Remote item, not mapped | tooltip "Basic Pulverisation" (patch name; 'Device Name' item not provable here) |
| PULV-F-K01 | SQUASH | Squash (compression) amount | Squash | 16 / CC 45 | voice/MIDI or click | tooltip "Squash: 49%" |
| PULV-F-K02 | DIRT | Dirt (distortion) amount | Dirt | 2 / CC 31 | voice/MIDI or click | tooltip "Dirt: 61%" |
| PULV-F-K09 | RELEASE | Squash release time | Release | 14 / CC 43 | voice/MIDI or click | tooltip "Release: 56%" |
| PULV-F-K10 | TONE | Tone | Tone | 18 / CC 47 | voice/MIDI or click | tooltip "Tone: 83%" |
| PULV-F-S01 | Filter mode | Filter mode lever (Bypass / Low Pass 24 / LP12+Notch / Band Pass / High Pass / Comb) | Filter Mode | 5 / CC 34 | voice/MIDI or click | tooltip "Filter Mode: Low Pass 24" |
| PULV-F-K12 | FREQUENCY | Filter frequency | Filter Frequency | 4 / CC 33 | voice/MIDI or click | tooltip "Filter Frequency: 11.05 kHz" |
| PULV-F-K13 | PEAK | Filter peak (resonance) | Peak | 13 / CC 42 | voice/MIDI or click | tooltip "Peak: 14%" |
| PULV-F-S02 | Routing | Order of Squash, Dirt and Filter | Routing | 15 / CC 44 | voice/MIDI or click | tooltip "Routing: 1" |
| PULV-F-K04 | Tremor RATE | Tremor rate | Tremor Rate | 20 / CC 49 | voice/MIDI or click | tooltip "Tremor Rate: 1.68 Hz" |
| PULV-F-D03 | Tremor SYNC light | Tremor sync light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-F-B08 | Tremor SYNC | Tremor tempo sync | Sync | 17 / CC 46 | voice/MIDI or click | tooltip "Tremor Sync" (Remote name is 'Sync') |
| PULV-F-D05 | Tremor WAVEFORM | Tremor waveform display (pick a shape with the arrows) | Tremor Waveform | 22 / CC 51 | voice/MIDI or click | tooltip "Tremor Waveform: Sine" |
| PULV-F-B07 | Waveform up arrow | Previous waveform | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-F-B09 | Waveform down arrow | Next waveform | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-F-D04 | Tremor SPREAD light | Tremor spread light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-F-B10 | Tremor SPREAD | Tremor stereo spread on/off | Tremor Spread | 21 / CC 50 | voice/MIDI or click | tooltip "Tremor Spread" |
| PULV-F-K05 | Tremor LAG | Tremor lag | Tremor Lag | 19 / CC 48 | voice/MIDI or click | tooltip "Tremor Lag: 16%" |
| PULV-F-K03 | Tremor > Frequency | Tremor amount to filter frequency | Tremor to Frequency | 23 / CC 52 | voice/MIDI or click | tooltip "Tremor to Frequency: 0%" |
| PULV-F-K08 | Follower > Rate | Follower amount to tremor rate | Follower to Rate | 12 / CC 41 | voice/MIDI or click | tooltip "Follower to Rate: 0%" |
| PULV-F-K14 | Follower > Frequency | Follower amount to filter frequency | Follower to Frequency | 11 / CC 40 | voice/MIDI or click | tooltip "Follower to Frequency: 0%" |
| PULV-F-K06 | Tremor > Volume | Tremor amount to volume | Tremor to Volume | 24 / CC 53 | voice/MIDI or click | tooltip "Tremor to Volume: 0%" |
| PULV-F-K07 | VOLUME | Output volume | Volume | 25 / CC 54 | voice/MIDI or click | tooltip "Volume: 65%" |
| PULV-F-K11 | BLEND | Dry/wet blend | Blend | 1 / CC 30 | voice/MIDI or click | tooltip "Blend: 100%" |
| PULV-F-B11 | Follower TRIG | Follower trigger button | Follower Trig | 10 / CC 39 | voice/MIDI or click | tooltip "Follower Trig" |
| PULV-F-K15 | THRESHOLD | Follower threshold | Follower Threshold | 9 / CC 38 | voice/MIDI or click | tooltip "Follower Threshold: 0%" |
| PULV-F-D07 | Follower light | Follower light (red) | Follow | 6 / CC 35 | voice/MIDI or click | no tooltip; Remote item 'Follow' is a 'flat' item (did not change during the sweep); placed on this light, NOT proven |
| PULV-F-K16 | ATTACK | Follower attack | Follower Attack | 7 / CC 36 | voice/MIDI or click | tooltip "Follower Attack: 0%" |
| PULV-F-K17 | Follower RELEASE | Follower release | Follower Release | 8 / CC 37 | voice/MIDI or click | tooltip "Follower Release: 0%" |

## Pulveriser — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| PULV-B-D04 | BASIC PULVER tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | tooltip "Basic Pulverisation" |
| PULV-B-D02 | (routing icon 1) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-B-D05 | (routing icon 2) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-B-D01 | (triangle) back | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-B-K01 | Squash CV trim | Amount for Squash CV | — | — | click/drag only (no Remote item) | tooltip "Squash CV Modulation Amount: 100%" |
| PULV-B-J01 | Squash CV In | CV input: Squash | — | — | cable: right-click jack > device > jack name | tooltip "Squash CV In" |
| PULV-B-K03 | Dirt CV trim | Amount for Dirt CV | — | — | click/drag only (no Remote item) | tooltip "Dirt CV Modulation Amount: 100%" |
| PULV-B-J06 | Dirt CV In | CV input: Dirt | — | — | cable: right-click jack > device > jack name | tooltip "Dirt CV In" |
| PULV-B-K05 | Filter Frequency CV trim | Amount for Filter Frequency CV | — | — | click/drag only (no Remote item) | tooltip "Filter Freq CV Modulation Amount: 100%" |
| PULV-B-J09 | Filter Frequency CV In | CV input: Filter Frequency | — | — | cable: right-click jack > device > jack name | tooltip "Filter CV In" |
| PULV-B-K06 | Tremor Rate CV trim | Amount for Tremor Rate CV | — | — | click/drag only (no Remote item) | tooltip "Tremor Rate CV Modulation Amount: 100%" |
| PULV-B-J10 | Tremor Rate CV In | CV input: Tremor Rate | — | — | cable: right-click jack > device > jack name | tooltip "Tremor CV In" |
| PULV-B-K07 | Volume CV trim | Amount for Volume CV | — | — | click/drag only (no Remote item) | tooltip "Volume CV Modulation Amount: 100%" |
| PULV-B-J13 | Volume CV In | CV input: Volume | — | — | cable: right-click jack > device > jack name | tooltip "Volume CV In" |
| PULV-B-K02 | Filter Frequency audio trim | Amount for Filter Frequency audio modulation | — | — | click/drag only (no Remote item) | tooltip "Filter Freq Audio Modulation Amount: 100%" |
| PULV-B-J02 | Filter Frequency audio In | Audio modulation input: Filter Frequency | — | — | cable: right-click jack > device > jack name | tooltip "Filter Freq Audio Modulation In" |
| PULV-B-K04 | Volume audio trim | Amount for Volume audio modulation | — | — | click/drag only (no Remote item) | tooltip "Volume Audio Modulation Amount: 100%" |
| PULV-B-J07 | Volume audio In | Audio modulation input: Volume | — | — | cable: right-click jack > device > jack name | tooltip "Volume Audio Modulation In" |
| PULV-B-K08 | Follower CV trim | Amount for Follower CV | — | — | click/drag only (no Remote item) | tooltip "Follower CV Modulation Amount: 100%" |
| PULV-B-J14 | Follower CV In | CV input: Follower (breaks internal routing) | — | — | cable: right-click jack > device > jack name | tooltip "Follow CV In" |
| PULV-B-J03 | Follower mod Out | Modulation output: Follower | — | — | cable: right-click jack > device > jack name | tooltip "Follower CV Out" |
| PULV-B-J08 | Tremor mod Out | Modulation output: Tremor | — | — | cable: right-click jack > device > jack name | tooltip "Tremor CV Out" |
| PULV-B-J04 | Audio In L | Audio input left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Neptune 1: Left Output"; this jack's own name NOT read yet |
| PULV-B-J05 | Audio In R | Audio input right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Neptune 1: Right Output"; this jack's own name NOT read yet |
| PULV-B-J11 | Audio Out L | Audio output left | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Big BBD Ensemble: Left Inpu(t)" (cut off); own jack name NOT read yet |
| PULV-B-J12 | Audio Out R | Audio output right | — | — | cable: right-click jack > device > jack name | cabled: tooltip "Connected to Big BBD Ensemble: Right Inp(ut)" (cut off); own jack name NOT read yet |
| PULV-B-D06 | Warning plate | Warning plate (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| PULV-B-D03 | PULVERISER logo | Logo (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Quartet Chorus Ensemble — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| QRTT-F-B05 | Bypass/On/Off | 3-way device switch | Enabled | 14 / CC 43 | voice/MIDI or click | tooltip "Enabled: On" |
| QRTT-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-F-D04 | (lights) | Level lights | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-F-D01 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | tooltip "Big BBD Ensemble" |
| QRTT-F-B02 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| QRTT-F-B06 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| QRTT-F-B03 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| QRTT-F-B04 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| QRTT-F-D02 | BIG BBD ENSE tape | Patch name tape | Device Name | — | display/Remote item, not mapped | tooltip "Big BBD Ensemble" (patch name; 'Device Name' item not provable here) |
| QRTT-F-D03 | Stereo | Stereo / Dual Mono selector | Stereo Mode | 28 / CC 57 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-F-B07 | CHORUS | Ensemble mode: Chorus | Effect Select | 13 / CC 42 | voice/MIDI or click | tooltip "Effect Select"; clicked, view changed, set back to BBD |
| QRTT-F-B08 | BBD | Ensemble mode: BBD | Effect Select | — | display/Remote item, not mapped | tooltip "Effect Select" |
| QRTT-F-B09 | FFT | Ensemble mode: FFT | Effect Select | — | display/Remote item, not mapped | tooltip "Effect Select"; clicked, view changed, set back to BBD |
| QRTT-F-B10 | GRAIN | Ensemble mode: Grain | Effect Select | — | display/Remote item, not mapped | tooltip "Effect Select"; clicked, view changed, set back to BBD |
| QRTT-F-K01 | BBD Delay | BBD Delay | BBD Delay | 1 / CC 30 | voice/MIDI or click | tooltip "BBD Delay: 7.23 ms" |
| QRTT-F-K02 | BBD Mod Depth | BBD Mod Depth | BBD Depth | 2 / CC 31 | voice/MIDI or click | tooltip "BBD Depth: 53.5 %" |
| QRTT-F-K03 | BBD Mod Rate | BBD Mod Rate | BBD Rate | 5 / CC 34 | voice/MIDI or click | tooltip "BBD Rate: 1.53 Hz" |
| QRTT-F-K04 | BBD Noise Mod | BBD Noise Mod | BBD Noise | 4 / CC 33 | voice/MIDI or click | tooltip "BBD Noise: 0.0 %" |
| QRTT-F-K05 | BBD Width | BBD Width | BBD Width | 6 / CC 35 | voice/MIDI or click | tooltip "BBD Width: 89.5 %" |
| QRTT-F-K06 | BBD Dry/Wet | BBD Dry/Wet | BBD DryWet | 3 / CC 32 | voice/MIDI or click | tooltip "BBD DryWet: 100.0 %" |
| QRTT-F-K101 | Chorus Delay | Chorus Delay | Chorus Delay | 7 / CC 36 | voice/MIDI or click | [Chorus mode (picture quartet-chorus-view_front_labeled.png)] tooltip "Chorus Delay: 5.08 ms" |
| QRTT-F-K102 | Chorus Mod Depth | Chorus Mod Depth | Chorus Depth | 8 / CC 37 | voice/MIDI or click | [Chorus mode (picture quartet-chorus-view_front_labeled.png)] tooltip "Chorus Depth: 50.0 %" |
| QRTT-F-K103 | Chorus Mod Rate | Chorus Mod Rate | Chorus Rate | 11 / CC 40 | voice/MIDI or click | [Chorus mode (picture quartet-chorus-view_front_labeled.png)] tooltip "Chorus Rate: 0.71 Hz" |
| QRTT-F-K104 | Chorus Feedback | Chorus Feedback | Chorus Feedback | 10 / CC 39 | voice/MIDI or click | [Chorus mode (picture quartet-chorus-view_front_labeled.png)] tooltip "Chorus Feedback: 0.0 %" |
| QRTT-F-K105 | Chorus Width | Chorus Width | Chorus Width | 12 / CC 41 | voice/MIDI or click | [Chorus mode (picture quartet-chorus-view_front_labeled.png)] tooltip "Chorus Width: 100.0 %" |
| QRTT-F-K106 | Chorus Dry/Wet | Chorus Dry/Wet | Chorus DryWet | 9 / CC 38 | voice/MIDI or click | [Chorus mode (picture quartet-chorus-view_front_labeled.png)] tooltip "Chorus DryWet: 100.0 %" |
| QRTT-F-S201 | FFT Size | FFT size slider (1 to 4) | FFT Size | 18 / CC 47 | voice/MIDI or click | [FFT mode (picture quartet-fft-view_front_labeled.png)] tooltip "FFT Size: 3" |
| QRTT-F-K201 | FFT Mod Depth | FFT mod depth | FFT Depth | 15 / CC 44 | voice/MIDI or click | [FFT mode (picture quartet-fft-view_front_labeled.png)] tooltip "FFT Depth: 50.0 %" |
| QRTT-F-S202 | Frequency Range start | Frequency range start handle | FFT Start | 19 / CC 48 | voice/MIDI or click | [FFT mode (picture quartet-fft-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (handle) |
| QRTT-F-S203 | Frequency Range end | Frequency range end handle | FFT End | 17 / CC 46 | voice/MIDI or click | [FFT mode (picture quartet-fft-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (handle) |
| QRTT-F-D201 | Frequency Range display | Frequency range display | — | — | click only | [FFT mode (picture quartet-fft-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-F-K202 | FFT Width | FFT width | FFT Width | 20 / CC 49 | voice/MIDI or click | [FFT mode (picture quartet-fft-view_front_labeled.png)] tooltip "FFT Width: 100.0 %" |
| QRTT-F-K203 | FFT Dry/Wet | FFT dry/wet | FFT DryWet | 16 / CC 45 | voice/MIDI or click | [FFT mode (picture quartet-fft-view_front_labeled.png)] tooltip "FFT DryWet: 100.0 %" |
| QRTT-F-B301 | Phase RND | Grain random phase on/off | Grain Phase | 25 / CC 54 | voice/MIDI or click | [Grain mode (picture quartet-grain-view_front_labeled.png)] tooltip "Grain Random Phase" (Remote name is 'Grain Phase') |
| QRTT-F-S301 | Grain Size | Grain size slider | Grain Size | 26 / CC 55 | voice/MIDI or click | [Grain mode (picture quartet-grain-view_front_labeled.png)] tooltip "Grain Size: 50.0 %" |
| QRTT-F-S302 | Grain Mod Depth | Grain mod depth slider | Grain Depth | 22 / CC 51 | voice/MIDI or click | [Grain mode (picture quartet-grain-view_front_labeled.png)] tooltip "Grain Depth: 40.0 %" |
| QRTT-F-S303 | Grain Jitter | Grain jitter slider | Grain Jitter | 24 / CC 53 | voice/MIDI or click | [Grain mode (picture quartet-grain-view_front_labeled.png)] tooltip "Grain Jitter: 50.0 %" |
| QRTT-F-S304 | Grain Density | Grain density slider | Grain Density | 21 / CC 50 | voice/MIDI or click | [Grain mode (picture quartet-grain-view_front_labeled.png)] tooltip "Grain Density: 60.0 %" |
| QRTT-F-K301 | Grain Width | Grain width | Grain Width | 27 / CC 56 | voice/MIDI or click | [Grain mode (picture quartet-grain-view_front_labeled.png)] tooltip "Grain Width: 100.0 %" |
| QRTT-F-K302 | Grain Dry/Wet | Grain dry/wet | Grain DryWet | 23 / CC 52 | voice/MIDI or click | [Grain mode (picture quartet-grain-view_front_labeled.png)] tooltip "Grain DryWet: 100.0 %" |

## Quartet Chorus Ensemble — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| QRTT-B-D01 | (triangle) back | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-B-D02 | BIG BBD ENSE tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | tooltip "Big BBD Ensemble" |
| QRTT-B-D03 | (routing icon 1) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-B-D04 | (routing icon 2) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-B-D05 | (routing icon 3) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| QRTT-B-K01 | Mod Depth CV trim | Amount for Mod Depth CV | — | — | click/drag only (no Remote item) | tooltip "Depth CV Amt: 100.0 %" |
| QRTT-B-J01 | Mod Depth CV In | CV input: Mod Depth | — | — | cable: right-click jack > device > jack name | tooltip "Depth CV Input" |
| QRTT-B-K02 | Width CV trim | Amount for Width CV | — | — | click/drag only (no Remote item) | tooltip "Width CV Amt: 100.0 %" |
| QRTT-B-J02 | Width CV In | CV input: Width | — | — | cable: right-click jack > device > jack name | tooltip "Width CV Input" |
| QRTT-B-K03 | DryWet CV trim | Amount for DryWet CV | — | — | click/drag only (no Remote item) | tooltip "DryWet CV Amt: 100.0 %" |
| QRTT-B-J03 | DryWet CV In | CV input: DryWet | — | — | cable: right-click jack > device > jack name | tooltip "DryWet CV Input" |
| QRTT-B-J04 | Audio In L | Audio input left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Basic Pulverisation: Left Out..." (cut off); own jack name NOT read yet |
| QRTT-B-J05 | Audio In R | Audio input right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Basic Pulverisation: Right O..." (cut off); own jack name NOT read yet |
| QRTT-B-J06 | Audio Out L | Audio output left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to British Drive 3: Main In Left"; this jack's own name NOT read yet |
| QRTT-B-J07 | Audio Out R | Audio output right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to British Drive 3: Main In Right"; this jack's own name NOT read yet |

## Alligator Filter Gate — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| ALGT-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| ALGT-F-B02 | Bypass/On/Off | 3-way device switch | Enabled | 48 / CC 77 | voice/MIDI or click | tooltip "Enabled: On" |
| ALGT-F-D01 | (meter lights) | Level lights | — | — | click only | tooltip "Master" (tooltip text; no Remote item assigned) |
| ALGT-F-D02 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | tooltip "Pad Rhythmification" |
| ALGT-F-B03 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| ALGT-F-B06 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| ALGT-F-B04 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| ALGT-F-B05 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| ALGT-F-D07 | PAD RHYTHMIF tape | Patch name tape | Device Name | — | display/Remote item, not mapped | tooltip "Pad Rhythmification" (patch name; 'Device Name' item not provable here) |
| ALGT-F-B07 | Pattern ON | Pattern on/off button | Pattern Enable | 41 / CC 70 | voice/MIDI or click | tooltip "Pattern Enable" |
| ALGT-F-D03 | Pattern light | Pattern on light | — | — | click only | tooltip "Pattern Enable" |
| ALGT-F-B10 | SHUFFLE | Pattern shuffle | Shuffle | 44 / CC 73 | voice/MIDI or click | tooltip "Shuffle" |
| ALGT-F-D05 | Pattern display | Pattern number (stepper) | Pattern | 40 / CC 69 | voice/MIDI or click | tooltip "Pattern: 1" |
| ALGT-F-B11 | Pattern up arrow | Next pattern | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| ALGT-F-B12 | Pattern down arrow | Previous pattern | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| ALGT-F-K20 | RESOLUTION | Pattern resolution | Resolution | 42 / CC 71 | voice/MIDI or click | tooltip "Resolution: 1/16" |
| ALGT-F-K33 | SHIFT | Pattern shift | Shift | 43 / CC 72 | voice/MIDI or click | tooltip "Shift: 0" |
| ALGT-F-B08 | MANUAL GATE 1 | Manual gate 1 button | Gate 1 Trig | 26 / CC 55 | voice/MIDI or click | tooltip "Gate 1 Trig" |
| ALGT-F-D04 | Gate 1 light | Gate 1 open light | Gate 1 Open | 25 / CC 54 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); Remote item 'Gate 1 Open' is a 'flat' item; placed on this light, NOT proven |
| ALGT-F-B13 | MANUAL GATE 2 | Manual gate 2 button | Gate 2 Trig | 28 / CC 57 | voice/MIDI or click | tooltip "Gate 2 Trig" |
| ALGT-F-D06 | Gate 2 light | Gate 2 open light | Gate 2 Open | 27 / CC 56 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); Remote item 'Gate 2 Open' is a 'flat' item; placed on this light, NOT proven |
| ALGT-F-B15 | MANUAL GATE 3 | Manual gate 3 button | Gate 3 Trig | 30 / CC 59 | voice/MIDI or click | tooltip "Gate 3 Trig" |
| ALGT-F-D08 | Gate 3 light | Gate 3 open light | Gate 3 Open | 29 / CC 58 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); Remote item 'Gate 3 Open' is a 'flat' item; placed on this light, NOT proven |
| ALGT-F-B09 | HIGH PASS ON | High Pass filter on/off | High Pass Filter On | 17 / CC 46 | voice/MIDI or click | tooltip "High Pass Filter On" |
| ALGT-F-K01 | HIGH PASS LFO | High Pass filter: LFO amount | High Pass LFO Amount | 21 / CC 50 | voice/MIDI or click | tooltip "High Pass LFO Amount: 22%" |
| ALGT-F-K02 | HIGH PASS FREQ | High Pass filter frequency | High Pass Frequency | 18 / CC 47 | voice/MIDI or click | tooltip "High Pass Frequency: 1.74 kHz" |
| ALGT-F-K03 | HIGH PASS RES | High Pass filter resonance | High Pass Resonance | 19 / CC 48 | voice/MIDI or click | tooltip "High Pass Resonance: 31%" |
| ALGT-F-K04 | HIGH PASS ENV | High Pass filter: envelope amount | High Pass Env Amount | 20 / CC 49 | voice/MIDI or click | tooltip "High Pass Env Amount: -25%" |
| ALGT-F-B14 | BAND PASS ON | Band Pass filter on/off | Band Pass Filter On | 9 / CC 38 | voice/MIDI or click | tooltip "Band Pass Filter On" |
| ALGT-F-K10 | BAND PASS LFO | Band Pass filter: LFO amount | Band Pass LFO Amount | 13 / CC 42 | voice/MIDI or click | tooltip "Band Pass LFO Amount: 22%" |
| ALGT-F-K11 | BAND PASS FREQ | Band Pass filter frequency | Band Pass Frequency | 10 / CC 39 | voice/MIDI or click | tooltip "Band Pass Frequency: 376.3 Hz" |
| ALGT-F-K12 | BAND PASS RES | Band Pass filter resonance | Band Pass Resonance | 11 / CC 40 | voice/MIDI or click | tooltip "Band Pass Resonance: 60%" |
| ALGT-F-K13 | BAND PASS ENV | Band Pass filter: envelope amount | Band Pass Env Amount | 12 / CC 41 | voice/MIDI or click | tooltip "Band Pass Env Amount: 19%" |
| ALGT-F-B16 | LOW PASS ON | Low Pass filter on/off | Low Pass Filter On | 1 / CC 30 | voice/MIDI or click | tooltip "Low Pass Filter On" |
| ALGT-F-K21 | LOW PASS LFO | Low Pass filter: LFO amount | Low Pass LFO Amount | 5 / CC 34 | voice/MIDI or click | tooltip "Low Pass LFO Amount: 22%" |
| ALGT-F-K22 | LOW PASS FREQ | Low Pass filter frequency | Low Pass Frequency | 2 / CC 31 | voice/MIDI or click | tooltip "Low Pass Frequency: 1.96 kHz" |
| ALGT-F-K23 | LOW PASS RES | Low Pass filter resonance | Low Pass Resonance | 3 / CC 32 | voice/MIDI or click | tooltip "Low Pass Resonance: 16%" |
| ALGT-F-K24 | LOW PASS ENV | Low Pass filter: envelope amount | Low Pass Env Amount | 4 / CC 33 | voice/MIDI or click | tooltip "Low Pass Env Amount: 16%" |
| ALGT-F-K05 | High Pass DRIVE | High Pass band: drive amount | High Pass Drive Amount | 22 / CC 51 | voice/MIDI or click | tooltip "High Pass Drive Amount: 17%" |
| ALGT-F-K06 | High Pass PHASER | High Pass band: phaser amount | High Pass Phaser Amount | — | display/Remote item, not mapped | tooltip "High Pass Phaser Amount: 0%" |
| ALGT-F-K07 | High Pass DELAY | High Pass band: delay amount | High Pass Delay Amount | — | display/Remote item, not mapped | tooltip "High Pass Delay Amount: 9%" |
| ALGT-F-K08 | High Pass PAN | High Pass band: pan | High Pass Pan | 23 / CC 52 | voice/MIDI or click | tooltip "High Pass Pan: -27" |
| ALGT-F-K09 | High Pass VOLUME | High Pass band: volume | High Pass Volume | 24 / CC 53 | voice/MIDI or click | tooltip "High Pass Volume: 75%" |
| ALGT-F-K14 | Band Pass DRIVE | Band Pass band: drive amount | Band Pass Drive Amount | 14 / CC 43 | voice/MIDI or click | tooltip "Band Pass Drive Amount: 31%" |
| ALGT-F-K15 | Band Pass PHASER | Band Pass band: phaser amount | Band Pass Phaser Amount | — | display/Remote item, not mapped | tooltip "Band Pass Phaser Amount: 0%" |
| ALGT-F-K16 | Band Pass DELAY | Band Pass band: delay amount | Band Pass Delay Amount | — | display/Remote item, not mapped | tooltip "Band Pass Delay Amount: 35%" |
| ALGT-F-K17 | Band Pass PAN | Band Pass band: pan | Band Pass Pan | 15 / CC 44 | voice/MIDI or click | tooltip "Band Pass Pan: 2" |
| ALGT-F-K18 | Band Pass VOLUME | Band Pass band: volume | Band Pass Volume | 16 / CC 45 | voice/MIDI or click | tooltip "Band Pass Volume: 70%" |
| ALGT-F-K25 | Low Pass DRIVE | Low Pass band: drive amount | Low Pass Drive Amount | 6 / CC 35 | voice/MIDI or click | tooltip "Low Pass Drive Amount: 39%" |
| ALGT-F-K26 | Low Pass PHASER | Low Pass band: phaser amount | Low Pass Phaser Amount | — | display/Remote item, not mapped | tooltip "Low Pass Phaser Amount: 0%" |
| ALGT-F-K27 | Low Pass DELAY | Low Pass band: delay amount | Low Pass Delay Amount | — | display/Remote item, not mapped | tooltip "Low Pass Delay Amount: 9%" |
| ALGT-F-K28 | Low Pass PAN | Low Pass band: pan | Low Pass Pan | 7 / CC 36 | voice/MIDI or click | tooltip "Low Pass Pan: 27" |
| ALGT-F-K29 | Low Pass VOLUME | Low Pass band: volume | Low Pass Volume | 8 / CC 37 | voice/MIDI or click | tooltip "Low Pass Volume: 75%" |
| ALGT-F-K30 | DUCKING | Ducking amount | Ducking | 47 / CC 76 | voice/MIDI or click | tooltip "Ducking: 0%" |
| ALGT-F-K31 | DRY PAN | Dry signal pan | Dry Pan | — | display/Remote item, not mapped | tooltip "Dry Pan: 2" |
| ALGT-F-K32 | DRY VOLUME | Dry signal volume | Dry Volume | 45 / CC 74 | voice/MIDI or click | tooltip "Dry Volume: 0%" |
| ALGT-F-K19 | MASTER | Master volume | Master Volume | 46 / CC 75 | voice/MIDI or click | tooltip "Master Volume: 72%" |
| ALGT-F-K34 | AMP ENV A | Amplitude envelope attack | Amp Env Attack | 31 / CC 60 | voice/MIDI or click | tooltip "Amp Env Attack: 16%" |
| ALGT-F-K35 | AMP ENV D | Amplitude envelope decay | Amp Env Decay | 32 / CC 61 | voice/MIDI or click | tooltip "Amp Env Decay: 61%" |
| ALGT-F-K36 | AMP ENV R | Amplitude envelope release | Amp Env Release | 33 / CC 62 | voice/MIDI or click | tooltip "Amp Env Release: 29%" |
| ALGT-F-D09 | LFO waveform display | LFO waveform (pick with the arrows) | LFO Waveform | 38 / CC 67 | voice/MIDI or click | tooltip "LFO Waveform: Triangle" |
| ALGT-F-B17 | LFO wave up arrow | Previous waveform | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| ALGT-F-B20 | LFO wave down arrow | Next waveform | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| ALGT-F-K37 | LFO FREQ | LFO frequency (note value when SYNC is on) | LFO Freq | 37 / CC 66 | voice/MIDI or click | tooltip "LFO Freq: 3/8" |
| ALGT-F-B18 | LFO SYNC | LFO tempo sync | LFOSync | 39 / CC 68 | voice/MIDI or click | tooltip "LFO Sync" (Remote name is 'LFOSync') |
| ALGT-F-K38 | FILTER ENV A | Filter envelope attack | Filter Env Attack | 34 / CC 63 | voice/MIDI or click | tooltip "Filter Env Attack: 9%" |
| ALGT-F-K39 | FILTER ENV D | Filter envelope decay | Filter Env Decay | 35 / CC 64 | voice/MIDI or click | tooltip "Filter Env Decay: 39%" |
| ALGT-F-K40 | FILTER ENV R | Filter envelope release | Filter Env Release | 36 / CC 65 | voice/MIDI or click | tooltip "Filter Env Release: 27%" |
| ALGT-F-K41 | DELAY TIME | Delay time (note value when SYNC is on) | Delay Time | — | display/Remote item, not mapped | tooltip "Delay Time: 1/8" |
| ALGT-F-B19 | DELAY SYNC | Delay tempo sync | DelaySync | — | display/Remote item, not mapped | tooltip "Delay Sync" (Remote name is 'DelaySync') |
| ALGT-F-K42 | DELAY FEEDBACK | Delay feedback | Delay Feedback | — | display/Remote item, not mapped | tooltip "Delay Feedback: 35%" |
| ALGT-F-K43 | DELAY PAN | Delay pan | Delay Pan | — | display/Remote item, not mapped | tooltip "Delay Pan: -2" |
| ALGT-F-K44 | PHASER RATE | Phaser rate | Phaser Rate | — | display/Remote item, not mapped | tooltip "Phaser Rate: 28%" |
| ALGT-F-K45 | PHASER FBK | Phaser feedback | Phaser Feedback | — | display/Remote item, not mapped | tooltip "Phaser Feedback: 29%" |

## Alligator Filter Gate — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| ALGT-B-D01 | PAD RHYTHMIF tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | tooltip "Pad Rhythmification" |
| ALGT-B-J05 | Gate 1 CV In | CV input: gate 1 (MIDI note) | — | — | cable: right-click jack > device > jack name | tooltip "Gate 1 CV In" |
| ALGT-B-J08 | Gate 2 CV In | CV input: gate 2 (MIDI note) | — | — | cable: right-click jack > device > jack name | tooltip "Gate 2 CV In" |
| ALGT-B-J13 | Gate 3 CV In | CV input: gate 3 (MIDI note) | — | — | cable: right-click jack > device > jack name | tooltip "Gate 3 CV In" |
| ALGT-B-K01 | High Pass Freq CV trim | Amount for High Pass Freq CV | — | — | click/drag only (no Remote item) | tooltip "High Pass Filter Freq CV Amount: 50%" |
| ALGT-B-J06 | High Pass Freq CV In | CV input: High Pass Freq | — | — | cable: right-click jack > device > jack name | tooltip "High Pass Filter Freq CV In" |
| ALGT-B-K02 | Band Pass Freq CV trim | Amount for Band Pass Freq CV | — | — | click/drag only (no Remote item) | tooltip "Band Pass Filter Freq CV Amount: 50%" |
| ALGT-B-J09 | Band Pass Freq CV In | CV input: Band Pass Freq | — | — | cable: right-click jack > device > jack name | tooltip "Band Pass Filter Freq CV In" |
| ALGT-B-K03 | Low Pass Freq CV trim | Amount for Low Pass Freq CV | — | — | click/drag only (no Remote item) | tooltip "Low Pass Filter Freq CV Amount: 50%" |
| ALGT-B-J14 | Low Pass Freq CV In | CV input: Low Pass Freq | — | — | cable: right-click jack > device > jack name | tooltip "Low Pass Filter Freq CV In" |
| ALGT-B-K04 | LFO Rate CV trim | Amount for LFO Rate CV | — | — | click/drag only (no Remote item) | tooltip "LFO Rate CV Modulation Amount: 50%" |
| ALGT-B-J18 | LFO Rate CV In | CV input: LFO Rate | — | — | cable: right-click jack > device > jack name | tooltip "LFO Rate CV In" |
| ALGT-B-J07 | Gate 1 CV Out | CV output: gate 1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate 1 CV Out" |
| ALGT-B-J10 | Gate 2 CV Out | CV output: gate 2 | — | — | cable: right-click jack > device > jack name | tooltip "Gate 2 CV Out" |
| ALGT-B-J15 | Gate 3 CV Out | CV output: gate 3 | — | — | cable: right-click jack > device > jack name | tooltip "Gate 3 CV Out" |
| ALGT-B-J19 | LFO CV Out | CV output: LFO | — | — | cable: right-click jack > device > jack name | tooltip "LFO CV Out" |
| ALGT-B-J03 | High Pass Channel L | Separate output left | — | — | cable: right-click jack > device > jack name | tooltip "High Pass Channel Left Output" |
| ALGT-B-J04 | High Pass Channel R | Separate output right | — | — | cable: right-click jack > device > jack name | tooltip "High Pass Channel Right Output" |
| ALGT-B-J11 | Band Pass Channel L | Separate output left | — | — | cable: right-click jack > device > jack name | tooltip "Band Pass Channel Left Output" |
| ALGT-B-J12 | Band Pass Channel R | Separate output right | — | — | cable: right-click jack > device > jack name | tooltip "Band Pass Channel Right Output" |
| ALGT-B-J16 | Low Pass Channel L | Separate output left | — | — | cable: right-click jack > device > jack name | tooltip "Low Pass Channel Left Output" |
| ALGT-B-J17 | Low Pass Channel R | Separate output right | — | — | cable: right-click jack > device > jack name | tooltip "Low Pass Channel Right Output" |
| ALGT-B-J01 | Audio In L | Audio input left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to MasterComp 1: Left Output"; this jack's own name NOT read yet |
| ALGT-B-J02 | Audio In R | Audio input right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to MasterComp 1: Right Output" (cut off at edge); own jack name NOT read yet |
| ALGT-B-J20 | Main Out L | Main output left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Audiomatic 1: Left Input"; this jack's own name NOT read yet |
| ALGT-B-J21 | Main Out R | Main output right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Audiomatic 1: Right Input"; this jack's own name NOT read yet |

## Softube Amp (ReasonAmp) — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RAMP-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-F-B03 | Bypass/On/Off | 3-way device switch | Enabled | 5 / CC 34 | voice/MIDI or click | tooltip "Enabled: On" |
| RAMP-F-D04 | BRITISH DRIVE tape | Patch name tape | Device Name | — | display/Remote item, not mapped | tooltip "British Drive 3" (patch name; 'Device Name' item not provable here) |
| RAMP-F-B04 | AMP TWANG | Amp model: Twang | Amp Switch | 1 / CC 30 | voice/MIDI or click | tooltip "Amp Switch" |
| RAMP-F-B05 | AMP CRUNCH | Amp model: Crunch | Amp Switch | — | display/Remote item, not mapped | tooltip "Amp Switch" |
| RAMP-F-B06 | AMP ROCK | Amp model: Rock | Amp Switch | — | display/Remote item, not mapped | tooltip "Amp Switch" |
| RAMP-F-B07 | AMP LEAD | Amp model: Lead | Amp Switch | — | display/Remote item, not mapped | tooltip "Amp Switch" |
| RAMP-F-B08 | AMP BYPASS | Amp model: Bypass | Amp Switch | — | display/Remote item, not mapped | tooltip "Amp Switch" |
| RAMP-F-D01 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | tooltip "British Drive 3" |
| RAMP-F-B02 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| RAMP-F-B09 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| RAMP-F-B10 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| RAMP-F-B11 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| RAMP-F-B12 | CAB BRIGHT | Cabinet: Bright | Cab Switch | 4 / CC 33 | voice/MIDI or click | tooltip "Cab Switch" |
| RAMP-F-B13 | CAB ROOM | Cabinet: Room | Cab Switch | — | display/Remote item, not mapped | tooltip "Cab Switch" |
| RAMP-F-B14 | CAB FAT | Cabinet: Fat | Cab Switch | — | display/Remote item, not mapped | tooltip "Cab Switch" |
| RAMP-F-B15 | CAB TIGHT | Cabinet: Tight | Cab Switch | — | display/Remote item, not mapped | tooltip "Cab Switch" |
| RAMP-F-B16 | CAB BYPASS | Cabinet: Bypass | Cab Switch | — | display/Remote item, not mapped | tooltip "Cab Switch" |
| RAMP-F-D02 | Softube logo | Logo (decoration) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-F-D03 | AMP logo | Logo (decoration) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-F-D05 | Red lamp | Red power lamp | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-F-B17 | Boost switch | Boost on/off toggle | Boost | 3 / CC 32 | voice/MIDI or click | tooltip "Boost: Normal" |
| RAMP-F-K07 | Gate | Noise gate threshold | Gate | 7 / CC 36 | voice/MIDI or click | tooltip "Gate: 0.1" |
| RAMP-F-K01 | Gain | Amp gain | Gain | 6 / CC 35 | voice/MIDI or click | tooltip "Gain: 10.0" |
| RAMP-F-K02 | Bass | Bass | Bass | 2 / CC 31 | voice/MIDI or click | tooltip "Bass: 4.7" |
| RAMP-F-K03 | Mid | Mid | Mid | 8 / CC 37 | voice/MIDI or click | tooltip "Mid: 8.4" |
| RAMP-F-K04 | Treble | Treble | Treble | 10 / CC 39 | voice/MIDI or click | tooltip "Treble: 6.9" |
| RAMP-F-K05 | Poweramp Gain | Poweramp gain | Poweramp Gain | 9 / CC 38 | voice/MIDI or click | tooltip "Poweramp Gain: 5.0" |
| RAMP-F-D06 | Level lights | Output level lights | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-F-K06 | Volume | Output volume | Volume | 11 / CC 40 | voice/MIDI or click | tooltip "Volume: -3.0 dB" |

## Softube Amp (ReasonAmp) — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RAMP-B-D01 | (triangle) back | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-B-D02 | BRITISH DRIVE tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | tooltip "British Drive 3" |
| RAMP-B-D03 | (routing icon 1) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-B-D04 | (routing icon 2) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-B-D05 | Warning sticker | Sticker (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-B-J04 | Input L | Audio input left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Big BBD Ensemble: Left Output" (cut off at edge); this jack's own name NOT read yet |
| RAMP-B-J05 | Input R | Audio input right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Big BBD Ensemble: Right Output" (cut off at edge); own jack name NOT read yet |
| RAMP-B-J06 | Output L | Audio output left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Smooth Bass: Main In Left"; this jack's own name NOT read yet |
| RAMP-B-J07 | Output R | Audio output right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Smooth Bass: Main In Right"; own jack name NOT read yet |
| RAMP-B-J01 | Gate CV In | CV input: gate | — | — | cable: right-click jack > device > jack name | tooltip "Gate CV" |
| RAMP-B-K01 | Gate CV trim | Amount for Gate CV | — | — | click/drag only (no Remote item) | tooltip "Gate CV: 127" |
| RAMP-B-J02 | Gain CV In | CV input: gain | — | — | cable: right-click jack > device > jack name | tooltip "Gain CV" |
| RAMP-B-K02 | Gain CV trim | Amount for Gain CV | — | — | click/drag only (no Remote item) | tooltip "Gain CV: 127" |
| RAMP-B-J03 | Volume CV In | CV input: volume | — | — | cable: right-click jack > device > jack name | tooltip "Volume CV" |
| RAMP-B-K03 | Volume CV trim | Amount for Volume CV | — | — | click/drag only (no Remote item) | tooltip "Volume CV: 127" |
| RAMP-B-D06 | Ground screw (J) | Ground terminal (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-B-D07 | Fuse 1 | Fuse cap (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RAMP-B-D08 | Fuse 2 | Fuse cap (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Softube Bass Amp (ReasonBassAmp) — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RBAS-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-F-B02 | Bypass/On/Off | 3-way device switch | Enabled | 5 / CC 34 | voice/MIDI or click | tooltip "Enabled: On" |
| RBAS-F-D01 | (speaker slots) | Decoration (vent slots) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-F-B03 | AMP MODERN | Amp model: Modern | Amp Switch | 1 / CC 30 | voice/MIDI or click | tooltip "Amp Switch" |
| RBAS-F-B04 | AMP VINTAGE | Amp model: Vintage | Amp Switch | — | display/Remote item, not mapped | tooltip "Amp Switch" |
| RBAS-F-B05 | AMP BYPASS | Amp model: Bypass | Amp Switch | — | display/Remote item, not mapped | tooltip "Amp Switch" |
| RBAS-F-D02 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | tooltip "Smooth Bass" |
| RBAS-F-B06 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| RBAS-F-B07 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" (second hover also read 'Select previous patch'; the down arrow's own text was not told apart; Remote item 'Select Next Patch' is by position) |
| RBAS-F-B08 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| RBAS-F-B09 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| RBAS-F-B10 | CAB DARK | Cabinet: Dark | Cab Switch | 3 / CC 32 | voice/MIDI or click | tooltip "Cab Switch" |
| RBAS-F-B11 | CAB BRIGHT | Cabinet: Bright | Cab Switch | — | display/Remote item, not mapped | tooltip "Cab Switch" |
| RBAS-F-B12 | CAB ROOM | Cabinet: Room | Cab Switch | — | display/Remote item, not mapped | tooltip "Cab Switch" |
| RBAS-F-B13 | CAB BYPASS | Cabinet: Bypass | Cab Switch | — | display/Remote item, not mapped | tooltip "Cab Switch" |
| RBAS-F-D03 | Softube logo | Logo (decoration) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-F-D04 | SMOOTH BASS tape | Patch name tape | Device Name | — | display/Remote item, not mapped | tooltip "Smooth Bass" (patch name; 'Device Name' item not provable here) |
| RBAS-F-K01 | Drive | Drive | Drive | 4 / CC 33 | voice/MIDI or click | tooltip "Drive: 7.0" |
| RBAS-F-K02 | Bass | Bass | Bass | 2 / CC 31 | voice/MIDI or click | tooltip "Bass: 5.5" |
| RBAS-F-K03 | Middle | Middle | Middle | 7 / CC 36 | voice/MIDI or click | tooltip "Middle: 2.5" |
| RBAS-F-K04 | Mid Freq | Mid frequency (1 to 5) | Mid Freq | 6 / CC 35 | voice/MIDI or click | tooltip "Mid Freq: 1" (read as 'Mid Freq: 1') |
| RBAS-F-K05 | Treble | Treble | Treble | 8 / CC 37 | voice/MIDI or click | tooltip "Treble: 5.0" |
| RBAS-F-B14 | ULTRA LO | Ultra Lo switch | Ultra Lo | 10 / CC 39 | voice/MIDI or click | tooltip "Ultra Lo" |
| RBAS-F-B15 | ULTRA HI | Ultra Hi switch | Ultra Hi | 9 / CC 38 | voice/MIDI or click | tooltip "Ultra Hi" |
| RBAS-F-D05 | Level lights | Output level lights | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-F-K06 | Volume | Output volume | Volume | 11 / CC 40 | voice/MIDI or click | tooltip "Volume: -8.2 dB" |
| RBAS-F-D06 | VOLUME label | Label bar under Volume (decoration) | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Softube Bass Amp (ReasonBassAmp) — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| RBAS-B-D01 | (triangle) back | Fold/unfold device | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-B-D02 | SMOOTH BASS tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | tooltip "Smooth Bass" |
| RBAS-B-D05 | (routing icon 1) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-B-D07 | (routing icon 2) | Routing icon | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-B-J01 | Drive CV In | CV input: drive | — | — | cable: right-click jack > device > jack name | tooltip "Drive CV" |
| RBAS-B-K01 | Drive CV trim | Amount for Drive CV | — | — | click/drag only (no Remote item) | tooltip "Drive CV: 127" |
| RBAS-B-J02 | Volume CV In | CV input: volume | — | — | cable: right-click jack > device > jack name | tooltip "Volume CV" |
| RBAS-B-K02 | Volume CV trim | Amount for Volume CV | — | — | click/drag only (no Remote item) | tooltip "Volume CV: 127" |
| RBAS-B-J03 | Input L | Audio input left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to British Drive 3: Main Out Le(ft)" (cut off); this jack's own name NOT read yet |
| RBAS-B-J04 | Input R | Audio input right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to British Drive 3: Main Out Rig(ht)" (cut off); own jack name NOT read yet |
| RBAS-B-J05 | Output L | Audio output left | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Basic Phasing: Left Input"; this jack's own name NOT read yet |
| RBAS-B-J06 | Output R | Audio output right | — | — | cable: right-click jack > device > jack name | tooltip "Connected to Basic Phasing: Right Input"; own jack name NOT read yet |
| RBAS-B-D03 | Fuse 1 | Fuse cap (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-B-D04 | Fuse 2 | Fuse cap (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-B-D06 | Vent grille | Decoration (vent) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| RBAS-B-D08 | Warning label | Sticker (decoration) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Kong Drum Designer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| KONG-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D01 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (display) |
| KONG-F-B02 | (up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| KONG-F-B03 | (down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| KONG-F-B04 | (folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| KONG-F-B05 | (disk) | Save patch | — | — | click only | tooltip "Save patch" |
| KONG-F-D02 | NOTE ON light | Note-on indicator light | Note On Indicator | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D05 | KONG KIT tape | Patch name tape | Device Name | — | display/Remote item, not mapped | tooltip "Kong Kit" (patch name; 'Device Name' item not provable here) |
| KONG-F-S01 | PITCH BEND wheel | Pitch bend wheel | Pitch Bend | — | display/Remote item, not mapped | tooltip "Pitch Bend: 0" (hover the lower part of the wheel; centre showed nothing) |
| KONG-F-S02 | MOD WHEEL | Modulation wheel | Mod Wheel | — | display/Remote item, not mapped | tooltip "Mod Wheel: 0" (hover the lower part of the wheel) |
| KONG-F-B06 | PAD 13 | Pad 13 (hit it with the mouse to play drum 13) | Pad 13 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B07 | PAD 14 | Pad 14 (hit it with the mouse to play drum 14) | Pad 14 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B08 | PAD 15 | Pad 15 (hit it with the mouse to play drum 15) | Pad 15 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B09 | PAD 16 | Pad 16 (hit it with the mouse to play drum 16) | Pad 16 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B10 | PAD 9 | Pad 9 (hit it with the mouse to play drum 9) | Pad 9 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B11 | PAD 10 | Pad 10 (hit it with the mouse to play drum 10) | Pad 10 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B12 | PAD 11 | Pad 11 (hit it with the mouse to play drum 11) | Pad 11 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B13 | PAD 12 | Pad 12 (hit it with the mouse to play drum 12) | Pad 12 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B18 | PAD 5 | Pad 5 (hit it with the mouse to play drum 5) | Pad 5 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B19 | PAD 6 | Pad 6 (hit it with the mouse to play drum 6) | Pad 6 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B20 | PAD 7 | Pad 7 (hit it with the mouse to play drum 7) | Pad 7 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B21 | PAD 8 | Pad 8 (hit it with the mouse to play drum 8) | Pad 8 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B22 | PAD 1 | Pad 1 (hit it with the mouse to play drum 1) | Pad 1 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B23 | PAD 2 | Pad 2 (hit it with the mouse to play drum 2) | Pad 2 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B24 | PAD 3 | Pad 3 (hit it with the mouse to play drum 3) | Pad 3 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B25 | PAD 4 | Pad 4 (hit it with the mouse to play drum 4) | Pad 4 Hit Indication | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K01 | MASTER LEVEL | Master level | Master Level | — | display/Remote item, not mapped | tooltip "Master Level: 100" |
| KONG-F-D03 | Meter L | Output level lights, left | — | — | click only | tooltip "Master Level Output Left" |
| KONG-F-D04 | Meter R | Output level lights, right | — | — | click only | tooltip "Master Level Output Right" |
| KONG-F-B14 | (drum patch arrows) | Previous / next drum patch (up arrow = previous, down arrow = next) | — | — | click only | tooltip "Select Previous Drum Patch" on the upper half; tooltip "Select Next Drum Patch" on the lower half |
| KONG-F-B15 | (drum folder) | Open drum patch browser | — | — | click only | tooltip "Browse Drum Patch" |
| KONG-F-B16 | (drum disk) | Save drum patch | — | — | click only | tooltip "Save Drum Patch" |
| KONG-F-B17 | (drum sample button) | Create a sample player by sampling | Quick Sample | — | display/Remote item, not mapped | tooltip "Create Sample Player by Sampling" |
| KONG-F-D06 | Drum name display | Name of the selected drum's patch | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (display) |
| KONG-F-D07 | DRUM number | Selected drum number | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (display) |
| KONG-F-D08 | (sample loading bar) | Sample loading progress bar | Sample Loading Progress | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K02 | OFFSET PITCH | Pitch offset of the selected drum | Drum 1 Pitch Offset | 2 / CC 31 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); again 2-3 s, still none |
| KONG-F-K05 | OFFSET DECAY | Decay offset of the selected drum | Drum 1 Decay Offset | 3 / CC 32 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K03 | SEND BUS FX | Send to Bus FX of the selected drum | Drum 1 Bus FX Send | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K06 | SEND AUX 1 | Send to Aux 1 of the selected drum | Drum 1 Aux 1 Send | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K07 | SEND AUX 2 | Send to Aux 2 of the selected drum | Drum 1 Aux 2 Send | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K04 | PAN | Pan of the selected drum | Drum 1 Pan | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K08 | TONE | Tone of the selected drum | Drum 1 Tone | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K09 | LEVEL | Level of the selected drum | Drum 1 Level | 1 / CC 30 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); again 3 s, still none |
| KONG-F-B26 | Q PITCH/DECAY | Quick Edit mode: Drum Pitch/Decay Offset | — | — | click only | tooltip "Quick Edit Mode: Drum Pitch/Decay Offset" |
| KONG-F-B27 | Q SENDS | Quick Edit mode: Drum Sends | — | — | click only | tooltip "Quick Edit Mode: Drum Sends" |
| KONG-F-B28 | Q PAN/LEVEL | Quick Edit mode: Drum Pan/Level | — | — | click only | tooltip "Quick Edit Mode: Drum Pan/Level" |
| KONG-F-B29 | Q TONE/LEVEL | Quick Edit mode: Drum Tone/Level | — | — | click only | tooltip "Quick Edit Mode: Drum Tone/Level" |
| KONG-F-B30 | SHOW DRUM AND FX | Open / close the Drum and FX section | — | — | click only | tooltip "Show Drum And FX" |
| KONG-F-B101 | DM ON | Drum module on/off | Drum 1 DM On | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 DM On" |
| KONG-F-B102 | DM menu arrow | Drum module menu | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K101 | DM PITCH | Drum module pitch | Drum 1 DM Pitch | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 DM Pitch: 0" |
| KONG-F-K102 | DM TUNE 1 | Bass drum tune 1 (module-only knob) | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Tune 1: 107" |
| KONG-F-K103 | DM TUNE 2 | Bass drum tune 2 (module-only knob) | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Tune 2: 60" |
| KONG-F-K104 | DM BEND AMOUNT | Bass drum bend amount (module-only knob) | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Bend Amount: 57" |
| KONG-F-K105 | DM DAMP | Bass drum damp (this module's variable knob) | Drum 1 DM Variable | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 DM Variable: 82" (printed label DAMP) |
| KONG-F-K106 | DM DECAY | Drum module decay | Drum 1 DM Decay | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 DM Decay: 28" |
| KONG-F-K109 | DM DENSITY | Beater density (module-only knob) | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Beater Density: 102" |
| KONG-F-K110 | DM SHELL LEVEL | Shell level (module-only knob) | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Shell Level: 33" |
| KONG-F-K113 | DM TONE | Beater tone (module-only knob) | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Beater Tone: 75" |
| KONG-F-K118 | DM BEATER LEVEL | Beater level (module-only knob) | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Beater Level: 64" |
| KONG-F-K119 | DM LEVEL | Drum module level (dark knob) | Drum 1 DM Level | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 DM Level: 100" |
| KONG-F-B103 | FX1 ON | FX 1 on/off | Drum 1 FX1 On | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX1 On" |
| KONG-F-B105 | FX1 menu arrow | FX 1 menu | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B104 | FX1 HIT I | FX 1 enable for hit type 1 | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX1 Enable Hit 1" |
| KONG-F-B112 | FX1 HIT II | FX 1 enable for hit type 2 | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX1 Enable Hit 2" |
| KONG-F-B113 | FX1 HIT III | FX 1 enable for hit type 3 | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX1 Enable Hit 3" |
| KONG-F-B114 | FX1 HIT IV | FX 1 enable for hit type 4 | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX1 Enable Hit 4" |
| KONG-F-D101 | FX1 waveform icon | Shows the FX 1 tone waveform | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K107 | FX1 PITCH | FX 1 tone: pitch (first FX knob) | Drum 1 FX1 P1 | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX1 P1: 6" |
| KONG-F-K111 | FX1 ATTACK | FX 1 tone: attack | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Attack: 20" |
| KONG-F-K112 | FX1 DECAY | FX 1 tone: decay (second FX knob) | Drum 1 FX1 P2 | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX1 P2: 59" |
| KONG-F-K116 | FX1 BEND DEC | FX 1 tone: bend decay | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Bend Decay: 25" |
| KONG-F-K117 | FX1 BEND | FX 1 tone: bend | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Bend: 0" |
| KONG-F-K120 | FX1 SHAPE | FX 1 tone: shape | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Shape: 67" |
| KONG-F-K121 | FX1 LEVEL | FX 1 tone: level | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Level: 72" |
| KONG-F-B106 | FX2 ON | FX 2 on/off | Drum 1 FX2 On | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 FX2 On" |
| KONG-F-B107 | FX2 menu arrow | FX 2 menu | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D104 | FX2 blank plate | FX 2 slot (empty: 'Blank Plate') | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (slot empty) |
| KONG-F-B108 | BUS FX ON | Bus FX on/off | Bus FX On | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Bus FX On" |
| KONG-F-B109 | BUS FX menu arrow | Bus FX menu | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D102 | BUS FX lights | Bus FX indicator lights | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D105 | BUS FX blank plate | Bus FX slot (empty: 'Blank Plate') | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (slot empty) |
| KONG-F-B110 | MASTER FX ON | Master FX on/off | Master FX On | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Master FX On" |
| KONG-F-B111 | MASTER FX menu arrow | Master FX menu | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D103 | MASTER FX lights | Master FX indicator lights | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K108 | COMP AMOUNT | Master compressor: amount | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Amount: 29" |
| KONG-F-K114 | COMP ATTACK | Master compressor: attack (first Master FX parameter) | Master FX P1 | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Master FX P1: 67" |
| KONG-F-K115 | COMP RELEASE | Master compressor: release (second Master FX parameter) | Master FX P2 | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Master FX P2: 67" |
| KONG-F-K122 | COMP MAKE UP GAIN | Master compressor: make-up gain | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Make Up Gain: 25" |
| KONG-F-D106 | COMP icon | Compressor corner icon | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-K124 | BUS FX TO MASTER FX | Level from Bus FX to Master FX | Level Bus FX to Master FX | — | display/Remote item, not mapped | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Level from Bus FX to Master FX: 100" |
| KONG-F-K123 | PITCH BEND RANGE | Pitch bend range of the selected drum | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] tooltip "Drum 1 Pitch Bend Range: 6" |
| KONG-F-D107 | DRUM OUTPUT menu | Which output the selected drum plays to (shows 'Master FX') | — | — | click only | [Drum and FX section open, Drum 1 selected (picture kong-drum-designer-dmfx-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B201 | PAD MUTE | Mute the selected pad | Pad 1 Mute | — | display/Remote item, not mapped | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Mute" (selected pad was 1) |
| KONG-F-B202 | PAD CLR | Clear all mutes and solos | Set all Mutes and Solos to Off | — | display/Remote item, not mapped | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Set all Mutes and Solos to Off" |
| KONG-F-B203 | PAD SOLO | Solo the selected pad | Pad 1 Solo | — | display/Remote item, not mapped | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Solo" (selected pad was 1) |
| KONG-F-B204 | PAD SETTINGS Q | Quick Edit mode: Pad Mute/Solo | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Quick Edit Mode: Pad Mute/Solo" |
| KONG-F-B205 | GROUP A | Pad group A (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group A" |
| KONG-F-B206 | GROUP B | Pad group B (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group B" |
| KONG-F-B207 | GROUP C | Pad group C (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group C" |
| KONG-F-B208 | GROUP D | Pad group D (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group D" |
| KONG-F-B209 | GROUP E | Pad group E (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group E" |
| KONG-F-B210 | GROUP F | Pad group F (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group F" |
| KONG-F-B211 | GROUP G | Pad group G (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group G" |
| KONG-F-B212 | GROUP H | Pad group H (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group H" |
| KONG-F-B213 | GROUP I | Pad group I (selected pad joins it) | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Group I" |
| KONG-F-D201 | GROUP MUTE light | Pad group mode light: MUTE | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D202 | GROUP LINK light | Pad group mode light: LINK | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-D203 | GROUP ALT light | Pad group mode light: ALT | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-F-B214 | PAD GROUP Q | Quick Edit mode: Pad Group | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Quick Edit Mode: Pad Group" |
| KONG-F-B215 | ASSIGN 13 | Drum assignment: give the selected pad drum 13 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B216 | ASSIGN 14 | Drum assignment: give the selected pad drum 14 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B217 | ASSIGN 15 | Drum assignment: give the selected pad drum 15 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B218 | ASSIGN 16 | Drum assignment: give the selected pad drum 16 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B219 | ASSIGN 9 | Drum assignment: give the selected pad drum 9 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B220 | ASSIGN 10 | Drum assignment: give the selected pad drum 10 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B221 | ASSIGN 11 | Drum assignment: give the selected pad drum 11 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B222 | ASSIGN 12 | Drum assignment: give the selected pad drum 12 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B223 | ASSIGN 5 | Drum assignment: give the selected pad drum 5 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B224 | ASSIGN 6 | Drum assignment: give the selected pad drum 6 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B225 | ASSIGN 7 | Drum assignment: give the selected pad drum 7 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B226 | ASSIGN 8 | Drum assignment: give the selected pad drum 8 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B227 | ASSIGN 1 | Drum assignment: give the selected pad drum 1 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B228 | ASSIGN 2 | Drum assignment: give the selected pad drum 2 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B229 | ASSIGN 3 | Drum assignment: give the selected pad drum 3 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B230 | ASSIGN 4 | Drum assignment: give the selected pad drum 4 | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Drum Assignment" (all 16 buttons show this same text) |
| KONG-F-B231 | DRUM ASSIGNMENT Q | Quick Edit mode: Pad Hit/Drum Assignment | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Quick Edit Mode: Pad Drum Assignment" |
| KONG-F-B232 | HIT TYPE I | Hit type 1 of the selected pad | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Hit Type" |
| KONG-F-B233 | HIT TYPE II | Hit type 2 of the selected pad | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Hit Type" |
| KONG-F-B234 | HIT TYPE III | Hit type 3 of the selected pad | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Hit Type" |
| KONG-F-B235 | HIT TYPE IV | Hit type 4 of the selected pad | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Pad 1 Hit Type" |
| KONG-F-D204 | HIT TYPE display | Hit type name display | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (display) |
| KONG-F-B236 | HIT TYPE Q | Quick Edit mode: Pad Hit Assignment | — | — | click only | [Right-hand column enlarged: Pad Settings, Pad Group, Drum Assignment, Hit Type (picture kong-drum-designer-padside-view_front_labeled.png)] tooltip "Quick Edit Mode: Pad Hit Assignment" |
| KONG-F-K301 | LEVEL (as Drum 2) | Level of drum 2: same physical knob as KONG-F-K09, aimed at drum 2 when that drum is selected | Drum 2 Level | 4 / CC 33 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 2 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K302 | OFFSET PITCH (as Drum 2) | Pitch offset of drum 2: same physical knob as KONG-F-K02, aimed at drum 2 when that drum is selected | Drum 2 Pitch Offset | 5 / CC 34 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 2 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K303 | OFFSET DECAY (as Drum 2) | Decay offset of drum 2: same physical knob as KONG-F-K05, aimed at drum 2 when that drum is selected | Drum 2 Decay Offset | 6 / CC 35 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 2 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K304 | LEVEL (as Drum 3) | Level of drum 3: same physical knob as KONG-F-K09, aimed at drum 3 when that drum is selected | Drum 3 Level | 7 / CC 36 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 3 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K305 | OFFSET PITCH (as Drum 3) | Pitch offset of drum 3: same physical knob as KONG-F-K02, aimed at drum 3 when that drum is selected | Drum 3 Pitch Offset | 8 / CC 37 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 3 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K306 | OFFSET DECAY (as Drum 3) | Decay offset of drum 3: same physical knob as KONG-F-K05, aimed at drum 3 when that drum is selected | Drum 3 Decay Offset | 9 / CC 38 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 3 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K307 | LEVEL (as Drum 4) | Level of drum 4: same physical knob as KONG-F-K09, aimed at drum 4 when that drum is selected | Drum 4 Level | 10 / CC 39 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 4 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K308 | OFFSET PITCH (as Drum 4) | Pitch offset of drum 4: same physical knob as KONG-F-K02, aimed at drum 4 when that drum is selected | Drum 4 Pitch Offset | 11 / CC 40 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 4 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K309 | OFFSET DECAY (as Drum 4) | Decay offset of drum 4: same physical knob as KONG-F-K05, aimed at drum 4 when that drum is selected | Drum 4 Decay Offset | 12 / CC 41 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 4 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K310 | LEVEL (as Drum 5) | Level of drum 5: same physical knob as KONG-F-K09, aimed at drum 5 when that drum is selected | Drum 5 Level | 13 / CC 42 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 5 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K311 | OFFSET PITCH (as Drum 5) | Pitch offset of drum 5: same physical knob as KONG-F-K02, aimed at drum 5 when that drum is selected | Drum 5 Pitch Offset | 14 / CC 43 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 5 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K312 | OFFSET DECAY (as Drum 5) | Decay offset of drum 5: same physical knob as KONG-F-K05, aimed at drum 5 when that drum is selected | Drum 5 Decay Offset | 15 / CC 44 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 5 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K313 | LEVEL (as Drum 6) | Level of drum 6: same physical knob as KONG-F-K09, aimed at drum 6 when that drum is selected | Drum 6 Level | 16 / CC 45 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 6 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K314 | OFFSET PITCH (as Drum 6) | Pitch offset of drum 6: same physical knob as KONG-F-K02, aimed at drum 6 when that drum is selected | Drum 6 Pitch Offset | 17 / CC 46 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 6 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K315 | OFFSET DECAY (as Drum 6) | Decay offset of drum 6: same physical knob as KONG-F-K05, aimed at drum 6 when that drum is selected | Drum 6 Decay Offset | 18 / CC 47 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 6 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K316 | LEVEL (as Drum 7) | Level of drum 7: same physical knob as KONG-F-K09, aimed at drum 7 when that drum is selected | Drum 7 Level | 19 / CC 48 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 7 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K317 | OFFSET PITCH (as Drum 7) | Pitch offset of drum 7: same physical knob as KONG-F-K02, aimed at drum 7 when that drum is selected | Drum 7 Pitch Offset | 20 / CC 49 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 7 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K318 | OFFSET DECAY (as Drum 7) | Decay offset of drum 7: same physical knob as KONG-F-K05, aimed at drum 7 when that drum is selected | Drum 7 Decay Offset | 21 / CC 50 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 7 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K319 | LEVEL (as Drum 8) | Level of drum 8: same physical knob as KONG-F-K09, aimed at drum 8 when that drum is selected | Drum 8 Level | 22 / CC 51 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 8 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K320 | OFFSET PITCH (as Drum 8) | Pitch offset of drum 8: same physical knob as KONG-F-K02, aimed at drum 8 when that drum is selected | Drum 8 Pitch Offset | 23 / CC 52 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 8 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K321 | OFFSET DECAY (as Drum 8) | Decay offset of drum 8: same physical knob as KONG-F-K05, aimed at drum 8 when that drum is selected | Drum 8 Decay Offset | 24 / CC 53 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 8 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K322 | LEVEL (as Drum 9) | Level of drum 9: same physical knob as KONG-F-K09, aimed at drum 9 when that drum is selected | Drum 9 Level | 25 / CC 54 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 9 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K323 | OFFSET PITCH (as Drum 9) | Pitch offset of drum 9: same physical knob as KONG-F-K02, aimed at drum 9 when that drum is selected | Drum 9 Pitch Offset | 26 / CC 55 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 9 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K324 | OFFSET DECAY (as Drum 9) | Decay offset of drum 9: same physical knob as KONG-F-K05, aimed at drum 9 when that drum is selected | Drum 9 Decay Offset | 27 / CC 56 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 9 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K325 | LEVEL (as Drum 10) | Level of drum 10: same physical knob as KONG-F-K09, aimed at drum 10 when that drum is selected | Drum 10 Level | 28 / CC 57 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 10 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K326 | OFFSET PITCH (as Drum 10) | Pitch offset of drum 10: same physical knob as KONG-F-K02, aimed at drum 10 when that drum is selected | Drum 10 Pitch Offset | 29 / CC 58 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 10 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K327 | OFFSET DECAY (as Drum 10) | Decay offset of drum 10: same physical knob as KONG-F-K05, aimed at drum 10 when that drum is selected | Drum 10 Decay Offset | 30 / CC 59 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 10 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K328 | LEVEL (as Drum 11) | Level of drum 11: same physical knob as KONG-F-K09, aimed at drum 11 when that drum is selected | Drum 11 Level | 31 / CC 60 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 11 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K329 | OFFSET PITCH (as Drum 11) | Pitch offset of drum 11: same physical knob as KONG-F-K02, aimed at drum 11 when that drum is selected | Drum 11 Pitch Offset | 32 / CC 61 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 11 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K330 | OFFSET DECAY (as Drum 11) | Decay offset of drum 11: same physical knob as KONG-F-K05, aimed at drum 11 when that drum is selected | Drum 11 Decay Offset | 33 / CC 62 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 11 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K331 | LEVEL (as Drum 12) | Level of drum 12: same physical knob as KONG-F-K09, aimed at drum 12 when that drum is selected | Drum 12 Level | 34 / CC 63 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 12 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K332 | OFFSET PITCH (as Drum 12) | Pitch offset of drum 12: same physical knob as KONG-F-K02, aimed at drum 12 when that drum is selected | Drum 12 Pitch Offset | 35 / CC 64 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 12 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K333 | OFFSET DECAY (as Drum 12) | Decay offset of drum 12: same physical knob as KONG-F-K05, aimed at drum 12 when that drum is selected | Drum 12 Decay Offset | 36 / CC 65 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 12 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K334 | LEVEL (as Drum 13) | Level of drum 13: same physical knob as KONG-F-K09, aimed at drum 13 when that drum is selected | Drum 13 Level | 37 / CC 66 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 13 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K335 | OFFSET PITCH (as Drum 13) | Pitch offset of drum 13: same physical knob as KONG-F-K02, aimed at drum 13 when that drum is selected | Drum 13 Pitch Offset | 38 / CC 67 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 13 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K336 | OFFSET DECAY (as Drum 13) | Decay offset of drum 13: same physical knob as KONG-F-K05, aimed at drum 13 when that drum is selected | Drum 13 Decay Offset | 39 / CC 68 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 13 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K337 | LEVEL (as Drum 14) | Level of drum 14: same physical knob as KONG-F-K09, aimed at drum 14 when that drum is selected | Drum 14 Level | 40 / CC 69 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 14 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K338 | OFFSET PITCH (as Drum 14) | Pitch offset of drum 14: same physical knob as KONG-F-K02, aimed at drum 14 when that drum is selected | Drum 14 Pitch Offset | 41 / CC 70 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 14 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K339 | OFFSET DECAY (as Drum 14) | Decay offset of drum 14: same physical knob as KONG-F-K05, aimed at drum 14 when that drum is selected | Drum 14 Decay Offset | 42 / CC 71 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 14 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K340 | LEVEL (as Drum 15) | Level of drum 15: same physical knob as KONG-F-K09, aimed at drum 15 when that drum is selected | Drum 15 Level | 43 / CC 72 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 15 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K341 | OFFSET PITCH (as Drum 15) | Pitch offset of drum 15: same physical knob as KONG-F-K02, aimed at drum 15 when that drum is selected | Drum 15 Pitch Offset | 44 / CC 73 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 15 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K342 | OFFSET DECAY (as Drum 15) | Decay offset of drum 15: same physical knob as KONG-F-K05, aimed at drum 15 when that drum is selected | Drum 15 Decay Offset | 45 / CC 74 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 15 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K343 | LEVEL (as Drum 16) | Level of drum 16: same physical knob as KONG-F-K09, aimed at drum 16 when that drum is selected | Drum 16 Level | 46 / CC 75 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K09 (drum 16 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K344 | OFFSET PITCH (as Drum 16) | Pitch offset of drum 16: same physical knob as KONG-F-K02, aimed at drum 16 when that drum is selected | Drum 16 Pitch Offset | 47 / CC 76 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K02 (drum 16 must be selected first). Name+slot from the remotemap and Remote list |
| KONG-F-K345 | OFFSET DECAY (as Drum 16) | Decay offset of drum 16: same physical knob as KONG-F-K05, aimed at drum 16 when that drum is selected | Drum 16 Decay Offset | 48 / CC 77 | voice/MIDI or click | not separately hovered: same knob as KONG-F-K05 (drum 16 must be selected first). Name+slot from the remotemap and Remote list |

## Kong Drum Designer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| KONG-B-D01 | KONG KIT tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| KONG-B-J11 | Sequencer Control Gate In | Gate input from a sequencer | — | — | cable: right-click jack > device > jack name | tooltip "Sequencer Control Gate In" |
| KONG-B-J12 | Sequencer Control CV In | CV (note) input from a sequencer | — | — | cable: right-click jack > device > jack name | tooltip "Sequencer Control CV In" |
| KONG-B-K01 | Master Volume trim | Amount for Master Volume CV | — | — | click/drag only (no Remote item) | tooltip "Master Volume In: 127" |
| KONG-B-J29 | Master Volume In | CV input: master volume | — | — | cable: right-click jack > device > jack name | tooltip "Master Volume In" |
| KONG-B-K02 | Pitch Wheel trim | Amount for Pitch Wheel CV | — | — | click/drag only (no Remote item) | tooltip "Pitch Wheel In: 127" |
| KONG-B-J30 | Pitch Wheel In | CV input: pitch wheel | — | — | cable: right-click jack > device > jack name | tooltip "Pitch Wheel In" |
| KONG-B-K03 | Mod Wheel trim | Amount for Mod Wheel CV | — | — | click/drag only (no Remote item) | tooltip "Mod Wheel In: 127" |
| KONG-B-J39 | Mod Wheel In | CV input: mod wheel | — | — | cable: right-click jack > device > jack name | tooltip "Mod Wheel In" |
| KONG-B-J44 | Aux Send 1 Left | Aux send 1 output, left | — | — | cable: right-click jack > device > jack name | tooltip "Send 1 Audio Out Left" |
| KONG-B-J45 | Aux Send 1 Right | Aux send 1 output, right | — | — | cable: right-click jack > device > jack name | tooltip "Send 1 Audio Out Right" |
| KONG-B-J46 | Aux Send 2 Left | Aux send 2 output, left | — | — | cable: right-click jack > device > jack name | tooltip "Send 2 Audio Out Left" |
| KONG-B-J47 | Aux Send 2 Right | Aux send 2 output, right | — | — | cable: right-click jack > device > jack name | tooltip "Send 2 Audio Out Right" |
| KONG-B-B01 | (Show Drum and FX) | Open / close the Drum and FX section | — | — | click/drag only (no Remote item) | tooltip "Show Drum And FX" |
| KONG-B-J01 | Pad 13 Gate In | Gate input: pad 13 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 13 Gate In" |
| KONG-B-J05 | Pad 13 Gate Out | Gate output: pad 13 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 13 Gate Out" |
| KONG-B-J02 | Pad 14 Gate In | Gate input: pad 14 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 14 Gate In" |
| KONG-B-J06 | Pad 14 Gate Out | Gate output: pad 14 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 14 Gate Out" |
| KONG-B-J03 | Pad 15 Gate In | Gate input: pad 15 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 15 Gate In" |
| KONG-B-J07 | Pad 15 Gate Out | Gate output: pad 15 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 15 Gate Out" |
| KONG-B-J04 | Pad 16 Gate In | Gate input: pad 16 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 16 Gate In" |
| KONG-B-J08 | Pad 16 Gate Out | Gate output: pad 16 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 16 Gate Out" |
| KONG-B-J13 | Pad 9 Gate In | Gate input: pad 9 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 9 Gate In" |
| KONG-B-J21 | Pad 9 Gate Out | Gate output: pad 9 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 9 Gate Out" |
| KONG-B-J14 | Pad 10 Gate In | Gate input: pad 10 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 10 Gate In" |
| KONG-B-J22 | Pad 10 Gate Out | Gate output: pad 10 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 10 Gate Out" |
| KONG-B-J15 | Pad 11 Gate In | Gate input: pad 11 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 11 Gate In" |
| KONG-B-J23 | Pad 11 Gate Out | Gate output: pad 11 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 11 Gate Out" |
| KONG-B-J16 | Pad 12 Gate In | Gate input: pad 12 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 12 Gate In" |
| KONG-B-J24 | Pad 12 Gate Out | Gate output: pad 12 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 12 Gate Out" |
| KONG-B-J31 | Pad 5 Gate In | Gate input: pad 5 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 5 Gate In" |
| KONG-B-J40 | Pad 5 Gate Out | Gate output: pad 5 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 5 Gate Out" |
| KONG-B-J32 | Pad 6 Gate In | Gate input: pad 6 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 6 Gate In" |
| KONG-B-J41 | Pad 6 Gate Out | Gate output: pad 6 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 6 Gate Out" |
| KONG-B-J33 | Pad 7 Gate In | Gate input: pad 7 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 7 Gate In" |
| KONG-B-J42 | Pad 7 Gate Out | Gate output: pad 7 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 7 Gate Out" |
| KONG-B-J34 | Pad 8 Gate In | Gate input: pad 8 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 8 Gate In" |
| KONG-B-J43 | Pad 8 Gate Out | Gate output: pad 8 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 8 Gate Out" |
| KONG-B-J48 | Pad 1 Gate In | Gate input: pad 1 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 1 Gate In" |
| KONG-B-J54 | Pad 1 Gate Out | Gate output: pad 1 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 1 Gate Out" |
| KONG-B-J49 | Pad 2 Gate In | Gate input: pad 2 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 2 Gate In" |
| KONG-B-J55 | Pad 2 Gate Out | Gate output: pad 2 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 2 Gate Out" |
| KONG-B-J50 | Pad 3 Gate In | Gate input: pad 3 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 3 Gate In" |
| KONG-B-J56 | Pad 3 Gate Out | Gate output: pad 3 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 3 Gate Out" |
| KONG-B-J51 | Pad 4 Gate In | Gate input: pad 4 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 4 Gate In" |
| KONG-B-J57 | Pad 4 Gate Out | Gate output: pad 4 | — | — | cable: right-click jack > device > jack name | tooltip "Pad 4 Gate Out" |
| KONG-B-J09 | Audio Out 3 | Separate audio output for drum 3 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 3" |
| KONG-B-J10 | Audio Out 4 | Separate audio output for drum 4 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 4" |
| KONG-B-J17 | Audio Out 5 | Separate audio output for drum 5 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 5" |
| KONG-B-J18 | Audio Out 6 | Separate audio output for drum 6 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 6" |
| KONG-B-J19 | Audio Out 7 | Separate audio output for drum 7 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 7" |
| KONG-B-J20 | Audio Out 8 | Separate audio output for drum 8 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 8" |
| KONG-B-J25 | Audio Out 9 | Separate audio output for drum 9 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 9" |
| KONG-B-J26 | Audio Out 10 | Separate audio output for drum 10 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 10" |
| KONG-B-J27 | Audio Out 11 | Separate audio output for drum 11 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 11" |
| KONG-B-J28 | Audio Out 12 | Separate audio output for drum 12 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 12" |
| KONG-B-J35 | Audio Out 13 | Separate audio output for drum 13 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 13" |
| KONG-B-J36 | Audio Out 14 | Separate audio output for drum 14 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 14" |
| KONG-B-J37 | Audio Out 15 | Separate audio output for drum 15 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 15" |
| KONG-B-J38 | Audio Out 16 | Separate audio output for drum 16 | — | — | cable: right-click jack > device > jack name | tooltip "Audio Out 16" |
| KONG-B-J52 | Main Audio Out L | Main audio output, left | — | — | cable: right-click jack > device > jack name | tooltip "Main Audio Out Left" (jack was empty) |
| KONG-B-J53 | Main Audio Out R | Main audio output, right | — | — | cable: right-click jack > device > jack name | tooltip "Main Audio Out Right" (jack was empty) |
| KONG-B-J58 | Bus FX Audio In L | Audio input into Bus FX, left | — | — | cable: right-click jack > device > jack name | tooltip "Bus FX Audio Input Left" |
| KONG-B-J59 | Bus FX Audio In R | Audio input into Bus FX, right | — | — | cable: right-click jack > device > jack name | tooltip "Bus FX Audio Input Right" |
| KONG-B-K04 | Bus FX Parameter 1 trim | Amount for Bus FX parameter 1 CV | — | — | click/drag only (no Remote item) | tooltip "Bus FX Parameter 1 In: 127" |
| KONG-B-J60 | Bus FX Parameter 1 In | CV input: Bus FX parameter 1 | — | — | cable: right-click jack > device > jack name | tooltip "Bus FX Parameter 1 In" |
| KONG-B-K07 | Bus FX Parameter 2 trim | Amount for Bus FX parameter 2 CV | — | — | click/drag only (no Remote item) | tooltip "Bus FX Paramater 2 In: 127" (Reason's own spelling 'Paramater') |
| KONG-B-J66 | Bus FX Parameter 2 In | CV input: Bus FX parameter 2 | — | — | cable: right-click jack > device > jack name | tooltip "Bus FX Paramater 2 In" (Reason's own spelling 'Paramater') |
| KONG-B-K05 | Bus FX to Master FX Level | Level from Bus FX to Master FX (back copy) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (the front knob of the same name did show a tooltip) |
| KONG-B-J61 | Breakout Output L | Breakout output to an external effect, left | — | — | cable: right-click jack > device > jack name | tooltip "To External FX Output Left" |
| KONG-B-J62 | Breakout Output R | Breakout output to an external effect, right | — | — | cable: right-click jack > device > jack name | tooltip "To External FX Output Right" |
| KONG-B-J63 | Breakout Input L | Breakout input from an external effect, left | — | — | cable: right-click jack > device > jack name | tooltip "From External FX Input Left" |
| KONG-B-J64 | Breakout Input R | Breakout input from an external effect, right | — | — | cable: right-click jack > device > jack name | tooltip "From External FX Input Right" |
| KONG-B-K06 | Master FX Parameter 1 trim | Amount for Master FX parameter 1 CV | — | — | click/drag only (no Remote item) | tooltip "Master FX Parameter 1 In: 127" |
| KONG-B-J65 | Master FX Parameter 1 In | CV input: Master FX parameter 1 | — | — | cable: right-click jack > device > jack name | tooltip "Master FX Parameter 1 In" |
| KONG-B-K08 | Master FX Parameter 2 trim | Amount for Master FX parameter 2 CV | — | — | click/drag only (no Remote item) | tooltip "Master FX Parameter 2 In: 127" |
| KONG-B-J67 | Master FX Parameter 2 In | CV input: Master FX parameter 2 | — | — | cable: right-click jack > device > jack name | tooltip "Master FX Parameter 2 In" |

## Redrum Drum Computer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| REDR-F-B01 | CH1 MUTE | Mute drum 1 | Drum 1 Mute | — | display/Remote item, not mapped | tooltip "Drum 1 Mute" |
| REDR-F-B02 | CH1 SOLO | Solo drum 1 | Drum 1 Solo | — | display/Remote item, not mapped | tooltip "Drum 1 Solo" |
| REDR-F-B03 | CH1 PLAY | Play (trigger) drum 1 | Channel 1 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 1" |
| REDR-F-D01 | CH1 sample name | Sample loaded on drum 1 | Channel 1 Sample | — | display/Remote item, not mapped | tooltip "Bd6_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B31 | CH1 sample arrows | Previous / next sample on drum 1 | — | — | click only | tooltip "Select previous sample" (upper half); tooltip "Select next sample" (lower half, checked on drum 1) |
| REDR-F-B41 | CH1 BROWSE | Browse samples for drum 1 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B42 | CH1 SAMPLE (wave button) | Start sampling into drum 1 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K02 | CH1 S1 | Send 1 amount, drum 1 | Drum 1 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 1 Send 1 Amount: 0" |
| REDR-F-K03 | CH1 S2 | Send 2 amount, drum 1 | Drum 1 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 1 Send 2 Amount: 0" |
| REDR-F-D11 | CH1 light (top) | Light between S1 and S2, drum 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K22 | CH1 PAN | Pan, drum 1 | Drum 1 Pan | 4 / CC 33 | voice/MIDI or click | tooltip "Drum 1 Pan: 0" |
| REDR-F-K32 | CH1 LEVEL | Level, drum 1 | Drum 1 Level | 1 / CC 30 | voice/MIDI or click | tooltip "Drum 1 Level: 96" |
| REDR-F-K33 | CH1 VEL (level) | How much velocity changes level, drum 1 | Drum 1 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 1 Vel to Level: 0" |
| REDR-F-K52 | CH1 LENGTH | Length, drum 1 | Drum 1 Length | 3 / CC 32 | voice/MIDI or click | tooltip "Drum 1 Length: 92" |
| REDR-F-B61 | CH1 DECAY/GATE | Decay or gate mode switch, drum 1 | Drum 1 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 1 Decay/Gate Mode: 0" |
| REDR-F-K62 | CH1 PITCH | Pitch, drum 1 | Drum 1 Pitch | 2 / CC 31 | voice/MIDI or click | tooltip "Drum 1 Pitch: 0" |
| REDR-F-D21 | CH1 light (pitch) | Light above the pitch knob, drum 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K74 | CH1 TONE | Tone, drum 1 | Drum 1 Tone | — | display/Remote item, not mapped | tooltip "Drum 1 Tone: -46" |
| REDR-F-K75 | CH1 VEL (tone) | How much velocity changes tone, drum 1 | Drum 1 Vel to Tone | — | display/Remote item, not mapped | tooltip "Drum 1 Vel to Tone: 0" |
| REDR-F-B71 | CH1 SELECT | Select drum 1 (edit its steps) | Select Drum 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B04 | CH2 MUTE | Mute drum 2 | Drum 2 Mute | — | display/Remote item, not mapped | tooltip "Drum 2 Mute" |
| REDR-F-B05 | CH2 SOLO | Solo drum 2 | Drum 2 Solo | — | display/Remote item, not mapped | tooltip "Drum 2 Solo" |
| REDR-F-B06 | CH2 PLAY | Play (trigger) drum 2 | Channel 2 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 2" |
| REDR-F-D02 | CH2 sample name | Sample loaded on drum 2 | Channel 2 Sample | — | display/Remote item, not mapped | tooltip "Bd7_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B32 | CH2 sample arrows | Previous / next sample on drum 2 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B43 | CH2 BROWSE | Browse samples for drum 2 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B44 | CH2 SAMPLE (wave button) | Start sampling into drum 2 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K04 | CH2 S1 | Send 1 amount, drum 2 | Drum 2 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 2 Send 1 Amount: 0" |
| REDR-F-K05 | CH2 S2 | Send 2 amount, drum 2 | Drum 2 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 2 Send 2 Amount: 0" |
| REDR-F-D12 | CH2 light (top) | Light between S1 and S2, drum 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K23 | CH2 PAN | Pan, drum 2 | Drum 2 Pan | 8 / CC 37 | voice/MIDI or click | tooltip "Drum 2 Pan: 0" |
| REDR-F-K34 | CH2 LEVEL | Level, drum 2 | Drum 2 Level | 5 / CC 34 | voice/MIDI or click | tooltip "Drum 2 Level: 100" |
| REDR-F-K35 | CH2 VEL (level) | How much velocity changes level, drum 2 | Drum 2 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 2 Vel to Level: 2" |
| REDR-F-K53 | CH2 LENGTH | Length, drum 2 | Drum 2 Length | 7 / CC 36 | voice/MIDI or click | tooltip "Drum 2 Length: 127" |
| REDR-F-B62 | CH2 DECAY/GATE | Decay or gate mode switch, drum 2 | Drum 2 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 2 Decay/Gate Mode: 0" |
| REDR-F-K63 | CH2 PITCH | Pitch, drum 2 | Drum 2 Pitch | 6 / CC 35 | voice/MIDI or click | tooltip "Drum 2 Pitch: -4" |
| REDR-F-D22 | CH2 light (pitch) | Light above the pitch knob, drum 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K76 | CH2 TONE | Tone, drum 2 | Drum 2 Tone | — | display/Remote item, not mapped | tooltip "Drum 2 Tone: 0" |
| REDR-F-K77 | CH2 VEL (tone) | How much velocity changes tone, drum 2 | Drum 2 Vel to Tone | — | display/Remote item, not mapped | tooltip "Drum 2 Vel to Tone: 0" |
| REDR-F-B72 | CH2 SELECT | Select drum 2 (edit its steps) | Select Drum 2 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B07 | CH3 MUTE | Mute drum 3 | Drum 3 Mute | — | display/Remote item, not mapped | tooltip "Drum 3 Mute" |
| REDR-F-B08 | CH3 SOLO | Solo drum 3 | Drum 3 Solo | — | display/Remote item, not mapped | tooltip "Drum 3 Solo" |
| REDR-F-B09 | CH3 PLAY | Play (trigger) drum 3 | Channel 3 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 3" |
| REDR-F-D03 | CH3 sample name | Sample loaded on drum 3 | Channel 3 Sample | — | display/Remote item, not mapped | tooltip "Clp1_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B33 | CH3 sample arrows | Previous / next sample on drum 3 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B45 | CH3 BROWSE | Browse samples for drum 3 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B46 | CH3 SAMPLE (wave button) | Start sampling into drum 3 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K06 | CH3 S1 | Send 1 amount, drum 3 | Drum 3 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 3 Send 1 Amount: 0" |
| REDR-F-K07 | CH3 S2 | Send 2 amount, drum 3 | Drum 3 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 3 Send 2 Amount: 0" |
| REDR-F-D13 | CH3 light (top) | Light between S1 and S2, drum 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K24 | CH3 PAN | Pan, drum 3 | Drum 3 Pan | 12 / CC 41 | voice/MIDI or click | tooltip "Drum 3 Pan: 0" |
| REDR-F-K36 | CH3 LEVEL | Level, drum 3 | Drum 3 Level | 9 / CC 38 | voice/MIDI or click | tooltip "Drum 3 Level: 100" |
| REDR-F-K37 | CH3 VEL (level) | How much velocity changes level, drum 3 | Drum 3 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 3 Vel to Level: 40" |
| REDR-F-K54 | CH3 LENGTH | Length, drum 3 | Drum 3 Length | 11 / CC 40 | voice/MIDI or click | tooltip "Drum 3 Length: 127" |
| REDR-F-B63 | CH3 DECAY/GATE | Decay or gate mode switch, drum 3 | Drum 3 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 3 Decay/Gate Mode: 0" |
| REDR-F-K64 | CH3 PITCH | Pitch, drum 3 | Drum 3 Pitch | 10 / CC 39 | voice/MIDI or click | tooltip "Drum 3 Pitch: -16" |
| REDR-F-D23 | CH3 light (pitch) | Light above the pitch knob, drum 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K78 | CH3 START | Sample start, drum 3 | Drum 3 Sample Start | — | display/Remote item, not mapped | tooltip "Drum 3 Sample Start: 0" |
| REDR-F-K79 | CH3 VEL (start) | How much velocity changes sample start, drum 3 | Drum 3 Vel to Sample Start | — | display/Remote item, not mapped | tooltip "Drum 3 Vel to Sample Start: 0" |
| REDR-F-B73 | CH3 SELECT | Select drum 3 (edit its steps) | Select Drum 3 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B10 | CH4 MUTE | Mute drum 4 | Drum 4 Mute | — | display/Remote item, not mapped | tooltip "Drum 4 Mute" |
| REDR-F-B11 | CH4 SOLO | Solo drum 4 | Drum 4 Solo | — | display/Remote item, not mapped | tooltip "Drum 4 Solo" |
| REDR-F-B12 | CH4 PLAY | Play (trigger) drum 4 | Channel 4 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 4" |
| REDR-F-D04 | CH4 sample name | Sample loaded on drum 4 | Channel 4 Sample | — | display/Remote item, not mapped | tooltip "Sd6_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B34 | CH4 sample arrows | Previous / next sample on drum 4 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B47 | CH4 BROWSE | Browse samples for drum 4 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B48 | CH4 SAMPLE (wave button) | Start sampling into drum 4 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K08 | CH4 S1 | Send 1 amount, drum 4 | Drum 4 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 4 Send 1 Amount: 0" |
| REDR-F-K09 | CH4 S2 | Send 2 amount, drum 4 | Drum 4 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 4 Send 2 Amount: 0" |
| REDR-F-D14 | CH4 light (top) | Light between S1 and S2, drum 4 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K25 | CH4 PAN | Pan, drum 4 | Drum 4 Pan | 16 / CC 45 | voice/MIDI or click | tooltip "Drum 4 Pan: 0" |
| REDR-F-K38 | CH4 LEVEL | Level, drum 4 | Drum 4 Level | 13 / CC 42 | voice/MIDI or click | tooltip "Drum 4 Level: 100" |
| REDR-F-K39 | CH4 VEL (level) | How much velocity changes level, drum 4 | Drum 4 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 4 Vel to Level: 40" |
| REDR-F-K55 | CH4 LENGTH | Length, drum 4 | Drum 4 Length | 15 / CC 44 | voice/MIDI or click | tooltip "Drum 4 Length: 127" |
| REDR-F-B64 | CH4 DECAY/GATE | Decay or gate mode switch, drum 4 | Drum 4 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 4 Decay/Gate Mode: 0" |
| REDR-F-K65 | CH4 PITCH | Pitch, drum 4 | Drum 4 Pitch | 14 / CC 43 | voice/MIDI or click | tooltip "Drum 4 Pitch: 0" |
| REDR-F-D24 | CH4 light (pitch) | Light above the pitch knob, drum 4 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-K80 | CH4 START | Sample start, drum 4 | Drum 4 Sample Start | — | display/Remote item, not mapped | tooltip "Drum 4 Sample Start: 0" |
| REDR-F-K81 | CH4 VEL (start) | How much velocity changes sample start, drum 4 | Drum 4 Vel to Sample Start | — | display/Remote item, not mapped | tooltip "Drum 4 Vel to Sample Start: 0" |
| REDR-F-B74 | CH4 SELECT | Select drum 4 (edit its steps) | Select Drum 4 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B13 | CH5 MUTE | Mute drum 5 | Drum 5 Mute | — | display/Remote item, not mapped | tooltip "Drum 5 Mute" |
| REDR-F-B14 | CH5 SOLO | Solo drum 5 | Drum 5 Solo | — | display/Remote item, not mapped | tooltip "Drum 5 Solo" |
| REDR-F-B15 | CH5 PLAY | Play (trigger) drum 5 | Channel 5 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 5" |
| REDR-F-D05 | CH5 sample name | Sample loaded on drum 5 | Channel 5 Sample | — | display/Remote item, not mapped | tooltip "Bd8_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B35 | CH5 sample arrows | Previous / next sample on drum 5 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B49 | CH5 BROWSE | Browse samples for drum 5 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B50 | CH5 SAMPLE (wave button) | Start sampling into drum 5 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K10 | CH5 S1 | Send 1 amount, drum 5 | Drum 5 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 5 Send 1 Amount: 0" |
| REDR-F-K11 | CH5 S2 | Send 2 amount, drum 5 | Drum 5 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 5 Send 2 Amount: 0" |
| REDR-F-D15 | CH5 light (top) | Light between S1 and S2, drum 5 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K26 | CH5 PAN | Pan, drum 5 | Drum 5 Pan | 20 / CC 49 | voice/MIDI or click | tooltip "Drum 5 Pan: 0" |
| REDR-F-K40 | CH5 LEVEL | Level, drum 5 | Drum 5 Level | 17 / CC 46 | voice/MIDI or click | tooltip "Drum 5 Level: 86" |
| REDR-F-K41 | CH5 VEL (level) | How much velocity changes level, drum 5 | Drum 5 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 5 Vel to Level: 0" |
| REDR-F-K56 | CH5 LENGTH | Length, drum 5 | Drum 5 Length | 19 / CC 48 | voice/MIDI or click | tooltip "Drum 5 Length: 127" |
| REDR-F-B65 | CH5 DECAY/GATE | Decay or gate mode switch, drum 5 | Drum 5 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 5 Decay/Gate Mode: 0" |
| REDR-F-K66 | CH5 PITCH | Pitch, drum 5 | Drum 5 Pitch | 18 / CC 47 | voice/MIDI or click | tooltip "Drum 5 Pitch: 0" |
| REDR-F-D25 | CH5 light (pitch) | Light above the pitch knob, drum 5 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K82 | CH5 START | Sample start, drum 5 | Drum 5 Sample Start | — | display/Remote item, not mapped | tooltip "Drum 5 Sample Start: 12" |
| REDR-F-K83 | CH5 VEL (start) | How much velocity changes sample start, drum 5 | Drum 5 Vel to Sample Start | — | display/Remote item, not mapped | tooltip "Drum 5 Vel to Sample Start: 0" |
| REDR-F-B75 | CH5 SELECT | Select drum 5 (edit its steps) | Select Drum 5 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B16 | CH6 MUTE | Mute drum 6 | Drum 6 Mute | — | display/Remote item, not mapped | tooltip "Drum 6 Mute" |
| REDR-F-B17 | CH6 SOLO | Solo drum 6 | Drum 6 Solo | — | display/Remote item, not mapped | tooltip "Drum 6 Solo" |
| REDR-F-B18 | CH6 PLAY | Play (trigger) drum 6 | Channel 6 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 6" |
| REDR-F-D06 | CH6 sample name | Sample loaded on drum 6 | Channel 6 Sample | — | display/Remote item, not mapped | tooltip "Bells_JC.aif" (the file name of the loaded sample) |
| REDR-F-B36 | CH6 sample arrows | Previous / next sample on drum 6 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B51 | CH6 BROWSE | Browse samples for drum 6 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B52 | CH6 SAMPLE (wave button) | Start sampling into drum 6 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K12 | CH6 S1 | Send 1 amount, drum 6 | Drum 6 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 6 Send 1 Amount: 0" |
| REDR-F-K13 | CH6 S2 | Send 2 amount, drum 6 | Drum 6 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 6 Send 2 Amount: 0" |
| REDR-F-D16 | CH6 light (top) | Light between S1 and S2, drum 6 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K27 | CH6 PAN | Pan, drum 6 | Drum 6 Pan | 24 / CC 53 | voice/MIDI or click | tooltip "Drum 6 Pan: 0" |
| REDR-F-K42 | CH6 LEVEL | Level, drum 6 | Drum 6 Level | 21 / CC 50 | voice/MIDI or click | tooltip "Drum 6 Level: 94" |
| REDR-F-K43 | CH6 VEL (level) | How much velocity changes level, drum 6 | Drum 6 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 6 Vel to Level: 40" |
| REDR-F-K57 | CH6 LENGTH | Length, drum 6 | Drum 6 Length | 23 / CC 52 | voice/MIDI or click | tooltip "Drum 6 Length: 127" |
| REDR-F-B66 | CH6 DECAY/GATE | Decay or gate mode switch, drum 6 | Drum 6 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 6 Decay/Gate Mode: 0" |
| REDR-F-K67 | CH6 PITCH | Pitch, drum 6 | Drum 6 Pitch | 22 / CC 51 | voice/MIDI or click | tooltip "Drum 6 Pitch: 0" |
| REDR-F-K68 | CH6 BEND | Pitch bend amount, drum 6 | Drum 6 Pitch Bend Amount | — | display/Remote item, not mapped | tooltip "Drum 6 Pitch Bend Amount: 0" |
| REDR-F-K84 | CH6 RATE | Pitch bend rate, drum 6 | Drum 6 Pitch Bend Rate | — | display/Remote item, not mapped | tooltip "Drum 6 Pitch Bend Rate: 64" |
| REDR-F-K85 | CH6 VEL (bend) | How much velocity changes pitch bend, drum 6 | Drum 6 Vel to Pitch Bend | — | display/Remote item, not mapped | tooltip "Drum 6 Vel to Pitch Bend: 0" |
| REDR-F-B76 | CH6 SELECT | Select drum 6 (edit its steps) | Select Drum 6 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B19 | CH7 MUTE | Mute drum 7 | Drum 7 Mute | — | display/Remote item, not mapped | tooltip "Drum 7 Mute" |
| REDR-F-B20 | CH7 SOLO | Solo drum 7 | Drum 7 Solo | — | display/Remote item, not mapped | tooltip "Drum 7 Solo" |
| REDR-F-B21 | CH7 PLAY | Play (trigger) drum 7 | Channel 7 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 7" |
| REDR-F-D07 | CH7 sample name | Sample loaded on drum 7 | Channel 7 Sample | — | display/Remote item, not mapped | tooltip "Sd8_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B37 | CH7 sample arrows | Previous / next sample on drum 7 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B53 | CH7 BROWSE | Browse samples for drum 7 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B54 | CH7 SAMPLE (wave button) | Start sampling into drum 7 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K14 | CH7 S1 | Send 1 amount, drum 7 | Drum 7 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 7 Send 1 Amount: 0" |
| REDR-F-K15 | CH7 S2 | Send 2 amount, drum 7 | Drum 7 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 7 Send 2 Amount: 0" |
| REDR-F-D17 | CH7 light (top) | Light between S1 and S2, drum 7 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K28 | CH7 PAN | Pan, drum 7 | Drum 7 Pan | 28 / CC 57 | voice/MIDI or click | tooltip "Drum 7 Pan: 0" |
| REDR-F-K44 | CH7 LEVEL | Level, drum 7 | Drum 7 Level | 25 / CC 54 | voice/MIDI or click | tooltip "Drum 7 Level: 100" |
| REDR-F-K45 | CH7 VEL (level) | How much velocity changes level, drum 7 | Drum 7 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 7 Vel to Level: 40" |
| REDR-F-K58 | CH7 LENGTH | Length, drum 7 | Drum 7 Length | 27 / CC 56 | voice/MIDI or click | tooltip "Drum 7 Length: 127" |
| REDR-F-B67 | CH7 DECAY/GATE | Decay or gate mode switch, drum 7 | Drum 7 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 7 Decay/Gate Mode: 0" |
| REDR-F-K69 | CH7 PITCH | Pitch, drum 7 | Drum 7 Pitch | 26 / CC 55 | voice/MIDI or click | tooltip "Drum 7 Pitch: 0" |
| REDR-F-K70 | CH7 BEND | Pitch bend amount, drum 7 | Drum 7 Pitch Bend Amount | — | display/Remote item, not mapped | tooltip "Drum 7 Pitch Bend Amount: 0" |
| REDR-F-K86 | CH7 RATE | Pitch bend rate, drum 7 | Drum 7 Pitch Bend Rate | — | display/Remote item, not mapped | tooltip "Drum 7 Pitch Bend Rate: 64" |
| REDR-F-K87 | CH7 VEL (bend) | How much velocity changes pitch bend, drum 7 | Drum 7 Vel to Pitch Bend | — | display/Remote item, not mapped | tooltip "Drum 7 Vel to Pitch Bend: 0" |
| REDR-F-B77 | CH7 SELECT | Select drum 7 (edit its steps) | Select Drum 7 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B22 | CH8 MUTE | Mute drum 8 | Drum 8 Mute | — | display/Remote item, not mapped | tooltip "Drum 8 Mute" |
| REDR-F-B23 | CH8 SOLO | Solo drum 8 | Drum 8 Solo | — | display/Remote item, not mapped | tooltip "Drum 8 Solo" |
| REDR-F-B24 | CH8 PLAY | Play (trigger) drum 8 | Channel 8 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 8" |
| REDR-F-D08 | CH8 sample name | Sample loaded on drum 8 | Channel 8 Sample | — | display/Remote item, not mapped | tooltip "Hh4_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B38 | CH8 sample arrows | Previous / next sample on drum 8 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B55 | CH8 BROWSE | Browse samples for drum 8 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B56 | CH8 SAMPLE (wave button) | Start sampling into drum 8 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K16 | CH8 S1 | Send 1 amount, drum 8 | Drum 8 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 8 Send 1 Amount: 0" |
| REDR-F-K17 | CH8 S2 | Send 2 amount, drum 8 | Drum 8 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 8 Send 2 Amount: 0" |
| REDR-F-D18 | CH8 light (top) | Light between S1 and S2, drum 8 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K29 | CH8 PAN | Pan, drum 8 | Drum 8 Pan | 32 / CC 61 | voice/MIDI or click | tooltip "Drum 8 Pan: 0" |
| REDR-F-K46 | CH8 LEVEL | Level, drum 8 | Drum 8 Level | 29 / CC 58 | voice/MIDI or click | tooltip "Drum 8 Level: 72" |
| REDR-F-K47 | CH8 VEL (level) | How much velocity changes level, drum 8 | Drum 8 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 8 Vel to Level: 40" |
| REDR-F-K59 | CH8 LENGTH | Length, drum 8 | Drum 8 Length | 31 / CC 60 | voice/MIDI or click | tooltip "Drum 8 Length: 117" |
| REDR-F-B68 | CH8 DECAY/GATE | Decay or gate mode switch, drum 8 | Drum 8 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 8 Decay/Gate Mode: 0" |
| REDR-F-K71 | CH8 PITCH | Pitch, drum 8 | Drum 8 Pitch | 30 / CC 59 | voice/MIDI or click | tooltip "Drum 8 Pitch: 16" |
| REDR-F-D26 | CH8 light (pitch) | Light above the pitch knob, drum 8 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K88 | CH8 START | Sample start, drum 8 | Drum 8 Sample Start | — | display/Remote item, not mapped | tooltip "Drum 8 Sample Start: 0" |
| REDR-F-K89 | CH8 VEL (start) | How much velocity changes sample start, drum 8 | Drum 8 Vel to Sample Start | — | display/Remote item, not mapped | tooltip "Drum 8 Vel to Sample Start: 0" |
| REDR-F-B78 | CH8 SELECT | Select drum 8 (edit its steps) | Select Drum 8 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B25 | CH9 MUTE | Mute drum 9 | Drum 9 Mute | — | display/Remote item, not mapped | tooltip "Drum 9 Mute" |
| REDR-F-B26 | CH9 SOLO | Solo drum 9 | Drum 9 Solo | — | display/Remote item, not mapped | tooltip "Drum 9 Solo" |
| REDR-F-B27 | CH9 PLAY | Play (trigger) drum 9 | Channel 9 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 9" |
| REDR-F-D09 | CH9 sample name | Sample loaded on drum 9 | Channel 9 Sample | — | display/Remote item, not mapped | tooltip "Hh5_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B39 | CH9 sample arrows | Previous / next sample on drum 9 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B57 | CH9 BROWSE | Browse samples for drum 9 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B58 | CH9 SAMPLE (wave button) | Start sampling into drum 9 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K18 | CH9 S1 | Send 1 amount, drum 9 | Drum 9 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 9 Send 1 Amount: 0" |
| REDR-F-K19 | CH9 S2 | Send 2 amount, drum 9 | Drum 9 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 9 Send 2 Amount: 0" |
| REDR-F-D19 | CH9 light (top) | Light between S1 and S2, drum 9 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K30 | CH9 PAN | Pan, drum 9 | Drum 9 Pan | 36 / CC 65 | voice/MIDI or click | tooltip "Drum 9 Pan: 0" |
| REDR-F-K48 | CH9 LEVEL | Level, drum 9 | Drum 9 Level | 33 / CC 62 | voice/MIDI or click | tooltip "Drum 9 Level: 66" |
| REDR-F-K49 | CH9 VEL (level) | How much velocity changes level, drum 9 | Drum 9 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 9 Vel to Level: 40" |
| REDR-F-K60 | CH9 LENGTH | Length, drum 9 | Drum 9 Length | 35 / CC 64 | voice/MIDI or click | tooltip "Drum 9 Length: 72" |
| REDR-F-B69 | CH9 DECAY/GATE | Decay or gate mode switch, drum 9 | Drum 9 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 9 Decay/Gate Mode: 0" |
| REDR-F-K72 | CH9 PITCH | Pitch, drum 9 | Drum 9 Pitch | 34 / CC 63 | voice/MIDI or click | tooltip "Drum 9 Pitch: 14" |
| REDR-F-D27 | CH9 light (pitch) | Light above the pitch knob, drum 9 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K90 | CH9 START | Sample start, drum 9 | Drum 9 Sample Start | — | display/Remote item, not mapped | tooltip "Drum 9 Sample Start: 0" |
| REDR-F-K91 | CH9 VEL (start) | How much velocity changes sample start, drum 9 | Drum 9 Vel to Sample Start | — | display/Remote item, not mapped | tooltip "Drum 9 Vel to Sample Start: 0" |
| REDR-F-B79 | CH9 SELECT | Select drum 9 (edit its steps) | Select Drum 9 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B28 | CH10 MUTE | Mute drum 10 | Drum 10 Mute | — | display/Remote item, not mapped | tooltip "Drum 10 Mute" |
| REDR-F-B29 | CH10 SOLO | Solo drum 10 | Drum 10 Solo | — | display/Remote item, not mapped | tooltip "Drum 10 Solo" |
| REDR-F-B30 | CH10 PLAY | Play (trigger) drum 10 | Channel 10 Play | — | display/Remote item, not mapped | tooltip "Trigger Drum 10" |
| REDR-F-D10 | CH10 sample name | Sample loaded on drum 10 | Channel 10 Sample | — | display/Remote item, not mapped | tooltip "Rd2_Rare.aif" (the file name of the loaded sample) |
| REDR-F-B40 | CH10 sample arrows | Previous / next sample on drum 10 | — | — | click only | tooltip "Select previous sample" (upper half; lower half checked on drum 1 only) |
| REDR-F-B59 | CH10 BROWSE | Browse samples for drum 10 | — | — | click only | tooltip "Browse sample" |
| REDR-F-B60 | CH10 SAMPLE (wave button) | Start sampling into drum 10 | — | — | click only | tooltip "Start sampling" |
| REDR-F-K20 | CH10 S1 | Send 1 amount, drum 10 | Drum 10 Send 1 Amount | — | display/Remote item, not mapped | tooltip "Drum 10 Send 1 Amount: 0" |
| REDR-F-K21 | CH10 S2 | Send 2 amount, drum 10 | Drum 10 Send 2 Amount | — | display/Remote item, not mapped | tooltip "Drum 10 Send 2 Amount: 0" |
| REDR-F-D20 | CH10 light (top) | Light between S1 and S2, drum 10 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K31 | CH10 PAN | Pan, drum 10 | Drum 10 Pan | 40 / CC 69 | voice/MIDI or click | tooltip "Drum 10 Pan: 0" |
| REDR-F-K50 | CH10 LEVEL | Level, drum 10 | Drum 10 Level | 37 / CC 66 | voice/MIDI or click | tooltip "Drum 10 Level: 72" |
| REDR-F-K51 | CH10 VEL (level) | How much velocity changes level, drum 10 | Drum 10 Vel to Level | — | display/Remote item, not mapped | tooltip "Drum 10 Vel to Level: 40" |
| REDR-F-K61 | CH10 LENGTH | Length, drum 10 | Drum 10 Length | 39 / CC 68 | voice/MIDI or click | tooltip "Drum 10 Length: 127" |
| REDR-F-B70 | CH10 DECAY/GATE | Decay or gate mode switch, drum 10 | Drum 10 Decay/Gate Mode | — | display/Remote item, not mapped | tooltip "Drum 10 Decay/Gate Mode: 0" |
| REDR-F-K73 | CH10 PITCH | Pitch, drum 10 | Drum 10 Pitch | 38 / CC 67 | voice/MIDI or click | tooltip "Drum 10 Pitch: 12" |
| REDR-F-D28 | CH10 light (pitch) | Light above the pitch knob, drum 10 | — | — | click only | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K92 | CH10 TONE | Tone, drum 10 | Drum 10 Tone | — | display/Remote item, not mapped | tooltip "Drum 10 Tone: 0" |
| REDR-F-K93 | CH10 VEL (tone) | How much velocity changes tone, drum 10 | Drum 10 Vel to Tone | — | display/Remote item, not mapped | tooltip "Drum 10 Vel to Tone: 0" |
| REDR-F-B80 | CH10 SELECT | Select drum 10 (edit its steps) | Select Drum 10 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-K01 | MASTER LEVEL | Master level | Master Level | 48 / CC 77 | voice/MIDI or click | tooltip "Master Level: 104" |
| REDR-F-D29 | (patch display) | Patch name display | Patch Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (display) |
| REDR-F-B88 | (patch arrows) | Previous / next patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" (upper half); tooltip "Select next patch" (lower half) |
| REDR-F-B89 | (patch folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| REDR-F-B90 | (patch disk) | Save patch | — | — | click only | tooltip "Save patch" |
| REDR-F-B100 | HIGH QUALITY INTERPOLATION | High quality interpolation on/off | High Quality Interpolation | — | display/Remote item, not mapped | tooltip "High Quality Interpolation" |
| REDR-F-B123 | CHANNEL 8-9 EXCLUSIVE | Drums 8 and 9 cut each other off (open / closed hat) | Channel 8 and 9 Exclusive | — | display/Remote item, not mapped | tooltip "Channel 8 and 9 Exclusive" |
| REDR-F-B81 | ENABLE PATTERN SECTION | Pattern section on/off | Enable Pattern Section Playback | — | display/Remote item, not mapped | tooltip "Enable Pattern Section Playback" |
| REDR-F-D31 | MUTE light | Mute light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B82 | PATTERN | Pattern on/off | Pattern Enable | 47 / CC 76 | voice/MIDI or click | tooltip "Pattern Enable" |
| REDR-F-B91 | PATTERN 1 | Pattern 1 button | Pattern 1 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B92 | PATTERN 2 | Pattern 2 button | Pattern 2 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B93 | PATTERN 3 | Pattern 3 button | Pattern 3 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B94 | PATTERN 4 | Pattern 4 button | Pattern 4 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B96 | PATTERN 5 | Pattern 5 button | Pattern 5 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B97 | PATTERN 6 | Pattern 6 button | Pattern 6 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B98 | PATTERN 7 | Pattern 7 button | Pattern 7 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B99 | PATTERN 8 | Pattern 8 button | Pattern 8 | — | display/Remote item, not mapped | tooltip "Pattern Select" |
| REDR-F-B95 | PATTERN SELECT (1-8 as one control) | Pick pattern 1-8 within the bank | Pattern Select in Bank | 41 / CC 70 | voice/MIDI or click | tooltip "Pattern Select" (same text on all 8 buttons) |
| REDR-F-B102 | BANK A | Bank A button | Bank A | — | display/Remote item, not mapped | tooltip "Bank Select" (same text on all 4) |
| REDR-F-B103 | BANK B | Bank B button | Bank B | — | display/Remote item, not mapped | tooltip "Bank Select" (same text on all 4) |
| REDR-F-B105 | BANK C | Bank C button | Bank C | — | display/Remote item, not mapped | tooltip "Bank Select" (same text on all 4) |
| REDR-F-B106 | BANK D | Bank D button | Bank D | — | display/Remote item, not mapped | tooltip "Bank Select" (same text on all 4) |
| REDR-F-B104 | BANK SELECT (A-D as one control) | Pick bank A-D | Bank Select | 42 / CC 71 | voice/MIDI or click | tooltip "Bank Select" (same text on all 4 buttons) |
| REDR-F-B101 | RUN | Run / stop the pattern | Run | 43 / CC 72 | voice/MIDI or click | tooltip "Play" (tooltip says Play; button is labelled RUN) |
| REDR-F-D30 | STEPS display | Pattern length (steps) display | — | — | click only | tooltip "Pattern Length: 16" |
| REDR-F-B83 | STEPS arrows | Pattern length up / down | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (upper half hovered; lower half also none) |
| REDR-F-K94 | RESOLUTION | Pattern resolution | Resolution | 46 / CC 75 | voice/MIDI or click | tooltip "Resolution: 1/16" |
| REDR-F-B84 | SHUFFLE | Pattern shuffle on/off | Shuffle | 44 / CC 73 | voice/MIDI or click | tooltip "Pattern Shuffle" |
| REDR-F-B85 | EDIT STEPS switch | Which 16 steps you edit (1-16 / 17-32 / 33-48 / 49-64) | Edit Steps | — | display/Remote item, not mapped | tooltip "Edit Steps Select" |
| REDR-F-B86 | DYNAMIC switch | Accent level to enter (hard / medium / soft) | Edit Accent | — | display/Remote item, not mapped | tooltip "Edit Accent" |
| REDR-F-K95 | FLAM knob | Flam amount | Flam Amount | 45 / CC 74 | voice/MIDI or click | tooltip "Flam Amount: 64" |
| REDR-F-B87 | FLAM button | Flam entry mode | — | — | click only | tooltip "Edit Flam" |
| REDR-F-B107 | STEP 1 | Step 1 button (toggles the step for the selected drum) | Selected Drum Toggle Step 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D32 | STEP 1 light | Step 1 light | Selected Drum Step 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B108 | STEP 2 | Step 2 button (toggles the step for the selected drum) | Selected Drum Toggle Step 2 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D33 | STEP 2 light | Step 2 light | Selected Drum Step 2 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B109 | STEP 3 | Step 3 button (toggles the step for the selected drum) | Selected Drum Toggle Step 3 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D34 | STEP 3 light | Step 3 light | Selected Drum Step 3 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B110 | STEP 4 | Step 4 button (toggles the step for the selected drum) | Selected Drum Toggle Step 4 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D35 | STEP 4 light | Step 4 light | Selected Drum Step 4 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B111 | STEP 5 | Step 5 button (toggles the step for the selected drum) | Selected Drum Toggle Step 5 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D36 | STEP 5 light | Step 5 light | Selected Drum Step 5 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B112 | STEP 6 | Step 6 button (toggles the step for the selected drum) | Selected Drum Toggle Step 6 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D37 | STEP 6 light | Step 6 light | Selected Drum Step 6 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B113 | STEP 7 | Step 7 button (toggles the step for the selected drum) | Selected Drum Toggle Step 7 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D38 | STEP 7 light | Step 7 light | Selected Drum Step 7 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B114 | STEP 8 | Step 8 button (toggles the step for the selected drum) | Selected Drum Toggle Step 8 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D39 | STEP 8 light | Step 8 light | Selected Drum Step 8 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B115 | STEP 9 | Step 9 button (toggles the step for the selected drum) | Selected Drum Toggle Step 9 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D40 | STEP 9 light | Step 9 light | Selected Drum Step 9 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-B116 | STEP 10 | Step 10 button (toggles the step for the selected drum) | Selected Drum Toggle Step 10 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D41 | STEP 10 light | Step 10 light | Selected Drum Step 10 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B117 | STEP 11 | Step 11 button (toggles the step for the selected drum) | Selected Drum Toggle Step 11 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D42 | STEP 11 light | Step 11 light | Selected Drum Step 11 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B118 | STEP 12 | Step 12 button (toggles the step for the selected drum) | Selected Drum Toggle Step 12 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D43 | STEP 12 light | Step 12 light | Selected Drum Step 12 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B119 | STEP 13 | Step 13 button (toggles the step for the selected drum) | Selected Drum Toggle Step 13 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D44 | STEP 13 light | Step 13 light | Selected Drum Step 13 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B120 | STEP 14 | Step 14 button (toggles the step for the selected drum) | Selected Drum Toggle Step 14 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D45 | STEP 14 light | Step 14 light | Selected Drum Step 14 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B121 | STEP 15 | Step 15 button (toggles the step for the selected drum) | Selected Drum Toggle Step 15 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D46 | STEP 15 light | Step 15 light | Selected Drum Step 15 | — | display/Remote item, not mapped | not hovered on this channel (no tooltip seen on this widget in channels 1-4) |
| REDR-F-B122 | STEP 16 | Step 16 button (toggles the step for the selected drum) | Selected Drum Toggle Step 16 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| REDR-F-D47 | STEP 16 light | Step 16 light | Selected Drum Step 16 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Redrum Drum Computer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| REDR-B-J01 | Ch 1 Left | Audio output, channel 1 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 1 Left" |
| REDR-B-J11 | Ch 1 Right | Audio output, channel 1 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 1 Right" |
| REDR-B-J25 | Gate Out 1 | Gate output, channel 1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 1" |
| REDR-B-J35 | Gate In 1 | Gate input, channel 1 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 1" |
| REDR-B-J45 | Pitch 1 CV In | Pitch CV input, channel 1 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 1 CV" |
| REDR-B-K01 | Pitch 1 CV trim | Amount for pitch CV, channel 1 | — | — | click/drag only (no Remote item) | tooltip "Pitch 1 CV: 127" |
| REDR-B-J02 | Ch 2 Left | Audio output, channel 2 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 2 Left" |
| REDR-B-J12 | Ch 2 Right | Audio output, channel 2 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 2 Right" |
| REDR-B-J26 | Gate Out 2 | Gate output, channel 2 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 2" |
| REDR-B-J36 | Gate In 2 | Gate input, channel 2 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 2" |
| REDR-B-J46 | Pitch 2 CV In | Pitch CV input, channel 2 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 2 CV" |
| REDR-B-K02 | Pitch 2 CV trim | Amount for pitch CV, channel 2 | — | — | click/drag only (no Remote item) | tooltip "Pitch 2 CV: 127" |
| REDR-B-J03 | Ch 3 Left | Audio output, channel 3 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 3 Left" |
| REDR-B-J13 | Ch 3 Right | Audio output, channel 3 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 3 Right" |
| REDR-B-J27 | Gate Out 3 | Gate output, channel 3 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 3" |
| REDR-B-J37 | Gate In 3 | Gate input, channel 3 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 3" |
| REDR-B-J47 | Pitch 3 CV In | Pitch CV input, channel 3 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 3 CV" |
| REDR-B-K03 | Pitch 3 CV trim | Amount for pitch CV, channel 3 | — | — | click/drag only (no Remote item) | tooltip "Pitch 3 CV: 127" |
| REDR-B-J04 | Ch 4 Left | Audio output, channel 4 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 4 Left" |
| REDR-B-J14 | Ch 4 Right | Audio output, channel 4 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 4 Right" |
| REDR-B-J28 | Gate Out 4 | Gate output, channel 4 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 4" |
| REDR-B-J38 | Gate In 4 | Gate input, channel 4 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 4" |
| REDR-B-J48 | Pitch 4 CV In | Pitch CV input, channel 4 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 4 CV" |
| REDR-B-K04 | Pitch 4 CV trim | Amount for pitch CV, channel 4 | — | — | click/drag only (no Remote item) | tooltip "Pitch 4 CV: 127" |
| REDR-B-J05 | Ch 5 Left | Audio output, channel 5 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 5 Left" |
| REDR-B-J15 | Ch 5 Right | Audio output, channel 5 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 5 Right" |
| REDR-B-J29 | Gate Out 5 | Gate output, channel 5 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 5" |
| REDR-B-J39 | Gate In 5 | Gate input, channel 5 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 5" |
| REDR-B-J49 | Pitch 5 CV In | Pitch CV input, channel 5 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 5 CV" |
| REDR-B-K05 | Pitch 5 CV trim | Amount for pitch CV, channel 5 | — | — | click/drag only (no Remote item) | tooltip "Pitch 5 CV: 127" |
| REDR-B-J06 | Ch 6 Left | Audio output, channel 6 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 6 Left" |
| REDR-B-J16 | Ch 6 Right | Audio output, channel 6 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 6 Right" |
| REDR-B-J30 | Gate Out 6 | Gate output, channel 6 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 6" |
| REDR-B-J40 | Gate In 6 | Gate input, channel 6 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 6" |
| REDR-B-J50 | Pitch 6 CV In | Pitch CV input, channel 6 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 6 CV" |
| REDR-B-K06 | Pitch 6 CV trim | Amount for pitch CV, channel 6 | — | — | click/drag only (no Remote item) | tooltip "Pitch 6 CV: 127" |
| REDR-B-J07 | Ch 7 Left | Audio output, channel 7 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 7 Left" |
| REDR-B-J17 | Ch 7 Right | Audio output, channel 7 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 7 Right" |
| REDR-B-J31 | Gate Out 7 | Gate output, channel 7 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 7" |
| REDR-B-J41 | Gate In 7 | Gate input, channel 7 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 7" |
| REDR-B-J51 | Pitch 7 CV In | Pitch CV input, channel 7 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 7 CV" |
| REDR-B-K07 | Pitch 7 CV trim | Amount for pitch CV, channel 7 | — | — | click/drag only (no Remote item) | tooltip "Pitch 7 CV: 127" |
| REDR-B-J08 | Ch 8 Left | Audio output, channel 8 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 8 Left" |
| REDR-B-J18 | Ch 8 Right | Audio output, channel 8 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 8 Right" |
| REDR-B-J32 | Gate Out 8 | Gate output, channel 8 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 8" |
| REDR-B-J42 | Gate In 8 | Gate input, channel 8 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 8" |
| REDR-B-J52 | Pitch 8 CV In | Pitch CV input, channel 8 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 8 CV" |
| REDR-B-K08 | Pitch 8 CV trim | Amount for pitch CV, channel 8 | — | — | click/drag only (no Remote item) | tooltip "Pitch 8 CV: 127" |
| REDR-B-J09 | Ch 9 Left | Audio output, channel 9 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 9 Left" |
| REDR-B-J19 | Ch 9 Right | Audio output, channel 9 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 9 Right" |
| REDR-B-J33 | Gate Out 9 | Gate output, channel 9 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 9" |
| REDR-B-J43 | Gate In 9 | Gate input, channel 9 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 9" |
| REDR-B-J53 | Pitch 9 CV In | Pitch CV input, channel 9 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 9 CV" |
| REDR-B-K09 | Pitch 9 CV trim | Amount for pitch CV, channel 9 | — | — | click/drag only (no Remote item) | tooltip "Pitch 9 CV: 127" |
| REDR-B-J10 | Ch 10 Left | Audio output, channel 10 left (or mono) | — | — | cable: right-click jack > device > jack name | tooltip "Ch 10 Left" |
| REDR-B-J20 | Ch 10 Right | Audio output, channel 10 right | — | — | cable: right-click jack > device > jack name | tooltip "Ch 10 Right" |
| REDR-B-J34 | Gate Out 10 | Gate output, channel 10 | — | — | cable: right-click jack > device > jack name | tooltip "Gate Out 10" |
| REDR-B-J44 | Gate In 10 | Gate input, channel 10 | — | — | cable: right-click jack > device > jack name | tooltip "Gate In 10" |
| REDR-B-J54 | Pitch 10 CV In | Pitch CV input, channel 10 | — | — | cable: right-click jack > device > jack name | tooltip "Pitch 10 CV" |
| REDR-B-K10 | Pitch 10 CV trim | Amount for pitch CV, channel 10 | — | — | click/drag only (no Remote item) | tooltip "Pitch 10 CV: 127" |
| REDR-B-J21 | Send Out 1 | Send output 1 | — | — | cable: right-click jack > device > jack name | tooltip "Send 1" |
| REDR-B-J22 | Send Out 2 | Send output 2 | — | — | cable: right-click jack > device > jack name | tooltip "Send 2" |
| REDR-B-J23 | Stereo Out Left | Stereo output, left | — | — | cable: right-click jack > device > jack name | tooltip "Left" |
| REDR-B-J24 | Stereo Out Right | Stereo output, right | — | — | cable: right-click jack > device > jack name | tooltip "Right" |
| REDR-B-D01 | Sample Memory display | Sample memory display | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Dr. Octo Rex Loop Player — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| DREX-F-B01 | (triangle top) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-S01 | PITCH BEND wheel | Pitch bend wheel | Pitch Bend | — | display/Remote item, not mapped | tooltip "Pitch Bend: 0" |
| DREX-F-S02 | MOD WHEEL | Modulation wheel | Mod Wheel | — | display/Remote item, not mapped | tooltip "Mod Wheel: 0" |
| DREX-F-D01 | ACOUSTIC DR tape | Patch name tape | Device Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D02 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B02 | (patch up arrow) | Load previous patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| DREX-F-B06 | (patch down arrow) | Load next patch | Select Next Patch | — | display/Remote item, not mapped | tooltip "Select next patch" |
| DREX-F-B03 | (patch folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| DREX-F-B04 | (patch disk) | Save patch | — | — | click only | tooltip "Save patch" |
| DREX-F-K01 | NOTES TO SLOT knob | Notes to slot (MIDI notes pick the loop slot) | Notes to Slot | 11 / CC 40 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (the lights beside the loop buttons show 'Notes to Slot') |
| DREX-F-B07 | LOOP BUTTON 1 | Play loop slot 1 | Select Loop 1 | 1 / CC 30 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D04 | LOOP 1 light | Notes-to-slot light, slot 1 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 1)" |
| DREX-F-D05 | LOOP 1 name | Loop file name, slot 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B08 | LOOP BUTTON 2 | Play loop slot 2 | Select Loop 2 | 2 / CC 31 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D06 | LOOP 2 light | Notes-to-slot light, slot 2 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 2)" |
| DREX-F-D07 | LOOP 2 name | Loop file name, slot 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B09 | LOOP BUTTON 3 | Play loop slot 3 | Select Loop 3 | 3 / CC 32 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D08 | LOOP 3 light | Notes-to-slot light, slot 3 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 3)" |
| DREX-F-D09 | LOOP 3 name | Loop file name, slot 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B10 | LOOP BUTTON 4 | Play loop slot 4 | Select Loop 4 | 4 / CC 33 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D10 | LOOP 4 light | Notes-to-slot light, slot 4 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 4)" |
| DREX-F-D11 | LOOP 4 name | Loop file name, slot 4 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B12 | LOOP BUTTON 5 | Play loop slot 5 | Select Loop 5 | 5 / CC 34 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D12 | LOOP 5 light | Notes-to-slot light, slot 5 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 5)" |
| DREX-F-D17 | LOOP 5 name | Loop file name, slot 5 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B13 | LOOP BUTTON 6 | Play loop slot 6 | Select Loop 6 | 6 / CC 35 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D13 | LOOP 6 light | Notes-to-slot light, slot 6 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 6)" |
| DREX-F-D18 | LOOP 6 name | Loop file name, slot 6 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B14 | LOOP BUTTON 7 | Play loop slot 7 | Select Loop 7 | 7 / CC 36 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D14 | LOOP 7 light | Notes-to-slot light, slot 7 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 7)" |
| DREX-F-D19 | LOOP 7 name | Loop file name, slot 7 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B15 | LOOP BUTTON 8 | Play loop slot 8 | Select Loop 8 | 8 / CC 37 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D15 | LOOP 8 light | Notes-to-slot light, slot 8 | — | — | click only | tooltip "Notes to Slot (shown on the light left of loop button 8)" |
| DREX-F-D20 | LOOP 8 name | Loop file name, slot 8 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B17 | TRIG NEXT LOOP: BAR | Switch loops at the next bar | Trigger Next Setting | 12 / CC 41 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); Remote 'Trigger Next Setting' covers BAR / BEAT / 1/16 |
| DREX-F-B18 | TRIG NEXT LOOP: BEAT | Switch loops at the next beat | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B19 | TRIG NEXT LOOP: 1/16 | Switch loops at the next 1/16 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B05 | ENABLE LOOP PLAYBACK | Loop playback on/off | Enable Loop Playback | 14 / CC 43 | voice/MIDI or click | tooltip "Enable Loop Playback" |
| DREX-F-D03 | MUTE light | Mute light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B11 | RUN | Run / stop loop playback | Run | 13 / CC 42 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); Remote item 'Run' matched by label, NOT proven |
| DREX-F-D16 | GLOBAL TRANSPOSE display | Global transpose (semitones) | Transpose | 16 / CC 45 | voice/MIDI or click | tooltip "Transpose: 0" (seen when hovering the arrows) |
| DREX-F-B16 | (global transpose arrows) | Global transpose up / down | — | — | click only | tooltip "Transpose: 0" seen on the display's lower edge; arrows themselves unproven |
| DREX-F-K02 | VOLUME | Master volume | Master Level | — | display/Remote item, not mapped | tooltip "Master Level: 100" |
| DREX-F-B20 | (triangle programmer) | Fold/unfold Programmer | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B21 | FOLLOW LOOP PLAYBACK | Programmer follows the playing loop | Follow Loop Playback | 15 / CC 44 | voice/MIDI or click | tooltip "Follow Loop Playback" |
| DREX-F-B22 | SELECT SLICE BY MIDI | Pick slice by MIDI note | — | — | click only | tooltip "Select Slice by MIDI" |
| DREX-F-B24 | (loop arrows) | Previous / next loop file | — | — | click only | tooltip "Select previous loop" (upper half; lower half not hovered) |
| DREX-F-B25 | (loop folder) | Browse loops | — | — | click only | tooltip "Browse loop" |
| DREX-F-B26 | SELECT SLOT 1 | Select loop slot 1 in the Programmer | Selected Loop Slot | 9 / CC 38 | voice/MIDI or click | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B29 | SELECT SLOT 2 | Select loop slot 2 in the Programmer | Selected Loop Slot | — | display/Remote item, not mapped | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B31 | SELECT SLOT 3 | Select loop slot 3 in the Programmer | Selected Loop Slot | — | display/Remote item, not mapped | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B33 | SELECT SLOT 4 | Select loop slot 4 in the Programmer | Selected Loop Slot | — | display/Remote item, not mapped | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B27 | SELECT SLOT 5 | Select loop slot 5 in the Programmer | Selected Loop Slot | — | display/Remote item, not mapped | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B30 | SELECT SLOT 6 | Select loop slot 6 in the Programmer | Selected Loop Slot | — | display/Remote item, not mapped | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B32 | SELECT SLOT 7 | Select loop slot 7 in the Programmer | Selected Loop Slot | — | display/Remote item, not mapped | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B34 | SELECT SLOT 8 | Select loop slot 8 in the Programmer | Selected Loop Slot | — | display/Remote item, not mapped | tooltip "Selected Loop Slot (same text on all 8)" |
| DREX-F-B28 | SELECT SLOT (editor, slot 10) | Remote item 'Selected Loop in Editor': probably the same 8 slot buttons or the loop-file arrows; NOT proven which | Selected Loop in Editor | 10 / CC 39 | voice/MIDI or click | not separately hovered: tooltip on these buttons reads 'Selected Loop Slot'; which control 'Selected Loop in Editor' drives was not proven |
| DREX-F-B35 | COPY LOOP TO TRACK | Copy the loop to a sequencer track | — | — | click only | tooltip "Copy Loop to Track" |
| DREX-F-K03 | LOOP TRANSPOSE | Transpose of the selected loop | Loop Transpose | 17 / CC 46 | voice/MIDI or click | tooltip "Loop 1 Transpose: 0" |
| DREX-F-K04 | LOOP LEVEL | Level of the selected loop | Loop Level | 26 / CC 55 | voice/MIDI or click | tooltip "Loop 1 Level: 100" |
| DREX-F-D23 | File name display | Loop file name | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D26 | Loop info display | Tempo and length of the loop | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D27 | Keyboard strip | Shows which MIDI keys play which slice | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D29 | Waveform display | Loop waveform with slices | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-K16 | SLICE SLICE knob | Slice slice (edits the selected slice) | — | — | click only | tooltip "Select Slice" |
| DREX-F-K17 | SLICE PITCH knob | Slice pitch (edits the selected slice) | — | — | click only | tooltip "Set Slice Pitch" |
| DREX-F-K18 | SLICE PAN knob | Slice pan (edits the selected slice) | — | — | click only | tooltip "Set Slice Pan" |
| DREX-F-K19 | SLICE LEVEL knob | Slice level (edits the selected slice) | — | — | click only | tooltip "Set Slice Level" |
| DREX-F-K20 | SLICE DECAY knob | Slice decay (edits the selected slice) | — | — | click only | tooltip "Set Slice Decay" |
| DREX-F-K21 | SLICE REV knob | Slice rev (edits the selected slice) | — | — | click only | tooltip "Set Slice Reverse" |
| DREX-F-K22 | SLICE F.FREQ knob | Slice f.freq (edits the selected slice) | — | — | click only | tooltip "Set Slice Filter Frequency" |
| DREX-F-K23 | SLICE ALT knob | Slice alt (edits the selected slice) | — | — | click only | tooltip "Set Slice Alternate Group" |
| DREX-F-K24 | SLICE OUTPUT knob | Slice output (edits the selected slice) | — | — | click only | tooltip "Set Slice Output" |
| DREX-F-K05 | OSC PITCH: ENV.A | Osc pitch envelope amount | Osc Env Amount | 20 / CC 49 | voice/MIDI or click | tooltip "Osc Env Amount: 0" |
| DREX-F-K06 | OSC PITCH: OCT | Osc octave | Osc Octave | 18 / CC 47 | voice/MIDI or click | tooltip "Osc Octave: 4" |
| DREX-F-K07 | OSC PITCH: FINE | Osc fine tune | Osc Fine Tune | 19 / CC 48 | voice/MIDI or click | tooltip "Osc Fine Tune: 0" |
| DREX-F-K08 | MOD.WHEEL: F.FREQ | Mod wheel to filter frequency | Filter Freq Mod Wheel Amount | — | display/Remote item, not mapped | tooltip "Filter Freq Mod Wheel Amount: 32" |
| DREX-F-K09 | MOD.WHEEL: F.RES | Mod wheel to filter resonance | Filter Res Mod Wheel Amount | — | display/Remote item, not mapped | tooltip "Filter Res Mod Wheel Amount: 0" |
| DREX-F-K10 | MOD.WHEEL: F.DECAY | Mod wheel to filter decay | Filter Decay Mod Wheel Amount | — | display/Remote item, not mapped | tooltip "Filter Decay Mod Wheel Amount: 0" |
| DREX-F-K11 | VELOCITY: F.ENV | Velocity to filter envelope amount | Filter Env Vel Amount | 36 / CC 65 | voice/MIDI or click | tooltip "Filter Env Vel Amount: 0" |
| DREX-F-K12 | VELOCITY: F.DECAY | Velocity to filter decay | Filter Decay Vel Amount | — | display/Remote item, not mapped | tooltip "Filter Decay Vel Amount: 0" |
| DREX-F-K13 | VELOCITY: AMP | Velocity to amp level | Amp Vel Amount | 25 / CC 54 | voice/MIDI or click | tooltip "Amp Vel Amount: 0" |
| DREX-F-B38 | SLICE EDIT MODE | Slice edit mode button | — | — | click only | tooltip "Slice Edit Mode" |
| DREX-F-D33 | PITCH BEND RANGE | Pitch bend range | Pitch Bend Range | — | display/Remote item, not mapped | tooltip "Pitch Bend Range: 7" |
| DREX-F-D34 | POLYPHONY | Number of voices | Polyphony | — | display/Remote item, not mapped | tooltip "Polyphony: 6" |
| DREX-F-B23 | FILTER ON | Filter on/off | Filter On/Off | 27 / CC 56 | voice/MIDI or click | tooltip "Filter On/Off" |
| DREX-F-D21 | FILTER MODE light Notch | Filter mode light: Notch | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D22 | FILTER MODE light HP 12 | Filter mode light: HP 12 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D24 | FILTER MODE light BP 12 | Filter mode light: BP 12 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D25 | FILTER MODE light LP 12 | Filter mode light: LP 12 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D28 | FILTER MODE light LP 24 | Filter mode light: LP 24 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B36 | FILTER MODE button | Step through filter modes | Filter Mode | 30 / CC 59 | voice/MIDI or click | tooltip "Filter Mode" |
| DREX-F-S03 | FILTER FREQ slider | Filter frequency | Filter Freq | 28 / CC 57 | voice/MIDI or click | tooltip "Filter Freq: 127" |
| DREX-F-S06 | FILTER RES slider | Filter resonance | Filter Res | 29 / CC 58 | voice/MIDI or click | tooltip "Filter Res: 0" |
| DREX-F-S07 | FILTER ENV AMOUNT slider | Filter envelope amount | Filter Env Amount | 31 / CC 60 | voice/MIDI or click | tooltip "Filter Env Amount: 0" |
| DREX-F-S08 | FILTER ENV A slider | Filter envelope attack | Filter Env Attack | 32 / CC 61 | voice/MIDI or click | tooltip "Filter Env Attack: 0" |
| DREX-F-S04 | FILTER ENV D slider | Filter envelope decay | Filter Env Decay | 33 / CC 62 | voice/MIDI or click | tooltip "Filter Env Decay: 64" |
| DREX-F-S09 | FILTER ENV S slider | Filter envelope sustain | Filter Env Sustain | 34 / CC 63 | voice/MIDI or click | tooltip "Filter Env Sustain: 0" |
| DREX-F-S05 | FILTER ENV R slider | Filter envelope release | Filter Env Release | 35 / CC 64 | voice/MIDI or click | tooltip "Filter Env Release: 64" |
| DREX-F-B37 | LFO SYNC | LFO tempo sync | LFO Sync Enable | 41 / CC 70 | voice/MIDI or click | tooltip "LFO Sync Enable" |
| DREX-F-D30 | LFO wave light 1 | LFO waveform light 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D31 | LFO wave light 2 | LFO waveform light 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D32 | LFO wave light 3 | LFO waveform light 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D35 | LFO wave light 4 | LFO waveform light 4 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D36 | LFO wave light 5 | LFO waveform light 5 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D39 | LFO wave light 6 | LFO waveform light 6 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B39 | LFO WAVEF. button | Step through LFO waveforms | LFO1 Wave | 39 / CC 68 | voice/MIDI or click | tooltip "LFO1 Wave" |
| DREX-F-K14 | LFO RATE | LFO rate | LFO1 Rate | 37 / CC 66 | voice/MIDI or click | tooltip "LFO1 Rate: 64" |
| DREX-F-K15 | LFO AMOUNT | LFO amount | LFO1 Amount | 38 / CC 67 | voice/MIDI or click | tooltip "LFO1 Amount: 0" |
| DREX-F-D37 | LFO DEST light OSC | LFO destination light: OSC | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D38 | LFO DEST light FILTER | LFO destination light: FILTER | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-D40 | LFO DEST light PAN | LFO destination light: PAN | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| DREX-F-B40 | LFO DEST. button | Step through LFO destinations | LFO1 Dest | 40 / CC 69 | voice/MIDI or click | tooltip "LFO1 Dest" |
| DREX-F-S11 | AMP ENV A slider | Amp envelope attack | Amp Env Attack | 21 / CC 50 | voice/MIDI or click | tooltip "Amp Env Attack: 0" |
| DREX-F-S10 | AMP ENV D slider | Amp envelope decay | Amp Env Decay | 22 / CC 51 | voice/MIDI or click | tooltip "Amp Env Decay: 127" |
| DREX-F-S12 | AMP ENV S slider | Amp envelope sustain | Amp Env Sustain | 23 / CC 52 | voice/MIDI or click | tooltip "Amp Env Sustain: 127" |
| DREX-F-S13 | AMP ENV R slider | Amp envelope release | Amp Env Release | 24 / CC 53 | voice/MIDI or click | tooltip "Amp Env Release: 10" |

## Dr. Octo Rex Loop Player — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| DREX-B-K01 | Amp Level (master volume) CV trim | Amount for Amp Level (master volume) CV | — | — | click/drag only (no Remote item) | tooltip "Amp Level Modulation Input: 127" |
| DREX-B-J01 | Amp Level (master volume) CV In | CV input: Amp Level (master volume) | — | — | cable: right-click jack > device > jack name | tooltip "Amp Level Modulation Input" |
| DREX-B-K03 | Mod Wheel CV trim | Amount for Mod Wheel CV | — | — | click/drag only (no Remote item) | tooltip "Mod Wheel Modulation Input: 127" |
| DREX-B-J13 | Mod Wheel CV In | CV input: Mod Wheel | — | — | cable: right-click jack > device > jack name | tooltip "Mod Wheel Modulation Input" |
| DREX-B-K05 | Pitch Wheel CV trim | Amount for Pitch Wheel CV | — | — | click/drag only (no Remote item) | tooltip "Pitch Wheel Modulation Input: 127" |
| DREX-B-J19 | Pitch Wheel CV In | CV input: Pitch Wheel | — | — | cable: right-click jack > device > jack name | tooltip "Pitch Wheel Modulation Input" |
| DREX-B-K02 | Filter cutoff CV trim | Amount for Filter cutoff CV | — | — | click/drag only (no Remote item) | tooltip "Filter1 Cutoff Modulation Input: 127" |
| DREX-B-J02 | Filter cutoff CV In | CV input: Filter cutoff | — | — | cable: right-click jack > device > jack name | tooltip "Filter1 Cutoff Modulation Input" |
| DREX-B-K04 | Filter resonance CV trim | Amount for Filter resonance CV | — | — | click/drag only (no Remote item) | tooltip "Filter1 Resonance Modulation Input: 127" |
| DREX-B-J14 | Filter resonance CV In | CV input: Filter resonance | — | — | cable: right-click jack > device > jack name | tooltip "Filter1 Resonance Modulation Input" |
| DREX-B-K06 | Osc pitch CV trim | Amount for Osc pitch CV | — | — | click/drag only (no Remote item) | tooltip "OSC Pitch Modulation Input: 127" |
| DREX-B-J20 | Osc pitch CV In | CV input: Osc pitch | — | — | cable: right-click jack > device > jack name | tooltip "OSC Pitch Modulation Input" |
| DREX-B-J03 | Filter Env Mod Out | CV output: filter envelope (voice 1) | — | — | cable: right-click jack > device > jack name | tooltip "Filter Env Modulation Output (Mono)" |
| DREX-B-J11 | LFO Mod Out | CV output: LFO | — | — | cable: right-click jack > device > jack name | tooltip "LFO Modulation Output" |
| DREX-B-J21 | Slice Gate Out | Gate output: slices | — | — | cable: right-click jack > device > jack name | tooltip "Slice Gate Output" |
| DREX-B-J04 | Amp Env Gate In | Gate input: amp envelope | — | — | cable: right-click jack > device > jack name | tooltip "Amp Env Gate Input" |
| DREX-B-J12 | Filter Env Gate In | Gate input: filter envelope | — | — | cable: right-click jack > device > jack name | tooltip "Filter Env Gate Input" |
| DREX-B-J05 | Slice Out 1 | Separate audio output for slice 1 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 1" |
| DREX-B-J06 | Slice Out 2 | Separate audio output for slice 2 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 2" |
| DREX-B-J07 | Slice Out 3 | Separate audio output for slice 3 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 3" |
| DREX-B-J08 | Slice Out 4 | Separate audio output for slice 4 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 4" |
| DREX-B-J15 | Slice Out 5 | Separate audio output for slice 5 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 5" |
| DREX-B-J16 | Slice Out 6 | Separate audio output for slice 6 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 6" |
| DREX-B-J17 | Slice Out 7 | Separate audio output for slice 7 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 7" |
| DREX-B-J18 | Slice Out 8 | Separate audio output for slice 8 | — | — | cable: right-click jack > device > jack name | tooltip "Slice Output 8" |
| DREX-B-J09 | Main Out L | Main output, left | — | — | cable: right-click jack > device > jack name | tooltip "Left" |
| DREX-B-J10 | Main Out R | Main output, right | — | — | cable: right-click jack > device > jack name | tooltip "Right" |
| DREX-B-B01 | HIGH QUALITY INTERPOLATION | High quality interpolation on/off | — | — | click/drag only (no Remote item) | tooltip "High Quality Interpolation" |
| DREX-B-B02 | LOW BANDWIDTH | Low bandwidth on/off | — | — | click/drag only (no Remote item) | tooltip "Low Bandwidth On/Off" |
| DREX-B-D01 | ACOUSTIC DR tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |

## Mimic Creative Sampler — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MIMC-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D01 | (red light) | Note-on light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D02 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B02 | (patch arrows) | Previous / next patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" (upper half; lower half = Select Next Patch, not hovered) |
| MIMC-F-B03 | (patch folder) | Open patch browser | — | — | click only | tooltip "Browse patch" |
| MIMC-F-B04 | (patch disk) | Save patch | — | — | click only | tooltip "Save patch" |
| MIMC-F-D03 | BASIC VIBE tape | Patch name tape | Device Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-K01 | MASTER VOLUME | Master volume | Master Volume | 41 / CC 70 | voice/MIDI or click | tooltip "Master Volume: 0.0 dB" |
| MIMC-F-B05 | MODE: Pitch | Play mode: Pitch | Play Mode | 42 / CC 71 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B06 | MODE: Slice | Play mode: Slice | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B07 | MODE: Multi Slot | Play mode: Multi Slot | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B08 | MODE: Multi Pitch | Play mode: Multi Pitch | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B09 | SLOT 1 tab | Select sample slot 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B10 | SLOT 2 tab | Select sample slot 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B11 | SLOT 3 tab | Select sample slot 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B12 | SLOT 4 tab | Select sample slot 4 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B13 | SLOT 5 tab | Select sample slot 5 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B14 | SLOT 6 tab | Select sample slot 6 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B15 | SLOT 7 tab | Select sample slot 7 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B16 | SLOT 8 tab | Select sample slot 8 | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D06 | Overview waveform | Whole-sample overview with start/end markers | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D07 | ANALYZED | Analysed pitch of the sample | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B17 | SET | Set root note from analysis | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D04 | ROOT note | Root note | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D05 | TUNE display | Root fine tune | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D08 | Main waveform | Waveform: sets start, end, loop and slices | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B18 | START marker | Sample start marker | Start Pos 1 | 4 / CC 33 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B19 | END marker | Sample end marker | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B20 | (sample arrows) | Previous / next sample | — | — | click only | tooltip "Select previous sample" (upper half; lower half not hovered) |
| MIMC-F-B21 | (sample folder) | Browse samples | — | — | click only | tooltip "Browse sample" |
| MIMC-F-B22 | (sample button) | Start sampling | — | — | click only | tooltip "Start sampling" |
| MIMC-F-D09 | Sample name display | Name of the loaded sample | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B23 | CLR | Delete the sample from the slot | — | — | click only | tooltip "Delete Sample" |
| MIMC-F-B24 | LOOP | Loop on/off | Loop On 1 | — | display/Remote item, not mapped | tooltip "Loop On 1" |
| MIMC-F-K02 | LOOP LENGTH | Loop length | Loop Length 1 | — | display/Remote item, not mapped | tooltip "Loop Length 1: 50.0 %" |
| MIMC-F-D10 | Keyboard | Keyboard: shows root note and range | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B26 | GLOBAL POSITION | Global start position | Global Pos 1 | — | display/Remote item, not mapped | tooltip "Global Pos 1" |
| MIMC-F-B28 | SNAP TO SLICES | Snap start to slices | Snap Slices 1 | — | display/Remote item, not mapped | tooltip "Snap Slices 1" |
| MIMC-F-B25 | REVERSE | Reverse the sample | Reverse 1 | — | display/Remote item, not mapped | tooltip "Reverse 1" |
| MIMC-F-K03 | START MOD amount | Start position: mod amount | — | — | click only | tooltip "Start ModAmt 1: 0.0 %" |
| MIMC-F-D11 | START MOD source | Start position: mod source menu | Start Mod 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-K04 | SPEED | Stretch speed | Stretch Speed 1 | — | display/Remote item, not mapped | tooltip "Stretch Speed 1: 100.0 %" |
| MIMC-F-K05 | SPEED MOD amount | Speed: mod amount | Speed ModAmt 1 | — | display/Remote item, not mapped | tooltip "Speed ModAmt 1: 0.0 %" |
| MIMC-F-D12 | SPEED MOD source | Speed: mod source menu | Speed Mod 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D13 | STRETCH mode menu | Stretch algorithm menu (Tape / ...) | Algorithm | 43 / CC 72 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-K06 | LOOP X-FADE | Loop crossfade | Loop Xfade 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) (knob; label LOOP X-FADE shows 50%) |
| MIMC-F-B27 | SLICES RESET | Reset slices | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B29 | PLAY THRU | Play-through for slices | Play Thru 1 | — | display/Remote item, not mapped | tooltip "Play Thru 1" |
| MIMC-F-K07 | SLICES SENSITIVITY | Slice detection sensitivity | Slice Sens 1 | — | display/Remote item, not mapped | tooltip "Slice Sens 1: 100.0 %" |
| MIMC-F-K08 | PORTA knob | Portamento rate | Portamento Rate 1 | — | display/Remote item, not mapped | tooltip "Portamento Rate 1: 25.0 %" |
| MIMC-F-B31 | PORTA switch (OFF/ON/AUTO) | Portamento mode | Portamento Mode 1 | — | display/Remote item, not mapped | tooltip "Portamento Mode 1: Off" |
| MIMC-F-B30 | POLY | Key mode: poly | Key Mode 1 | — | display/Remote item, not mapped | tooltip "Key Mode 1" |
| MIMC-F-B32 | MONO RETRIG | Key mode: mono retrig | — | — | click only | tooltip "Key Mode 1" |
| MIMC-F-B34 | MONO LEGATO | Key mode: mono legato | — | — | click only | tooltip "Key Mode 1" |
| MIMC-F-B33 | PITCH KBD | Pitch follows keyboard | Pitch Kbd 1 | — | display/Remote item, not mapped | tooltip "Pitch Kbd 1" |
| MIMC-F-K09 | PITCH SEMI | Pitch in semitones | Pitch Semi 1 | 2 / CC 31 | voice/MIDI or click | tooltip "Pitch Semi 1: 0" |
| MIMC-F-D16 | Semi display | Semitone readout | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-K13 | PITCH TUNE | Fine tune | Tune 1 | — | display/Remote item, not mapped | tooltip "Tune 1: 0.0" |
| MIMC-F-K14 | PITCH LFO | Pitch LFO amount | — | — | click only | tooltip "Pitch LFOAmt 1: 0.0 %" |
| MIMC-F-K15 | PITCH MOD amount | Pitch mod amount | — | — | click only | tooltip "Pitch ModAmt 1: 0.0 %" |
| MIMC-F-D17 | PITCH MOD source | Pitch: mod source menu | Pitch Mod 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-K20 | PITCH RANGE | Pitch bend range | Pitchbend Range 1 | — | display/Remote item, not mapped | tooltip "Pitchbend Range 1: 2" |
| MIMC-F-K21 | LFO SCALE | Mod wheel to LFO amount | — | — | click only | tooltip "MW LFO 1: 0.0 %" |
| MIMC-F-S09 | PITCH wheel | Pitch bend wheel | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); Remote item 'Pitch Bend' matched by label, NOT proven |
| MIMC-F-S10 | MOD wheel | Mod wheel | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); Remote item 'Mod Wheel' matched by label, NOT proven |
| MIMC-F-D14 | FILTER type menu | Filter type menu | Filter Type 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D15 | (filter light) | Filter indicator light | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-K12 | FILTER FREQ | Filter frequency | Filter Freq 1 | 3 / CC 32 | voice/MIDI or click | tooltip "Filter Freq 1: 769.4 Hz" |
| MIMC-F-K10 | FILTER RESO | Filter resonance | Filter Reso 1 | — | display/Remote item, not mapped | tooltip "Filter Reso 1: 50.0 %" |
| MIMC-F-K11 | FILTER DRIVE | Filter drive | Filter Drive 1 | — | display/Remote item, not mapped | tooltip "Filter Drive 1: 10.0 %" |
| MIMC-F-K16 | FILTER KBD | Filter key tracking | — | — | click only | tooltip "Filter Kbd 1: 50.0 %" |
| MIMC-F-K17 | FILTER VEL | Filter velocity | — | — | click only | tooltip "Filter Vel 1: 0.0 %" |
| MIMC-F-K18 | FILTER ENV | Filter envelope amount | Filter Env 1 | — | display/Remote item, not mapped | tooltip "Filter Env 1: 0.0 %" |
| MIMC-F-K19 | FILTER MOD amount | Filter mod amount | Filter ModAmt 1 | — | display/Remote item, not mapped | tooltip "Filter ModAmt 1: 0.0 %" |
| MIMC-F-D18 | FILTER MOD source | Filter: mod source menu | Filter Mod 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-S05 | FILTER ENV A | Filter envelope attack | Filter Attack 1 | — | display/Remote item, not mapped | tooltip "Filter Attack 1: 0.0 ms" |
| MIMC-F-S03 | FILTER ENV D | Filter envelope decay | Filter Decay 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); retried 2 s, still none |
| MIMC-F-S01 | FILTER ENV S | Filter envelope sustain | Filter Sustain 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); retried 2 s, still none |
| MIMC-F-S06 | FILTER ENV R | Filter envelope release | Filter Release 1 | — | display/Remote item, not mapped | tooltip "Filter Release 1: 35 ms" |
| MIMC-F-S07 | AMP ENV A | Amp envelope attack | Amp Attack 1 | — | display/Remote item, not mapped | tooltip "Amp Attack 1: 0.0 ms" |
| MIMC-F-S04 | AMP ENV D | Amp envelope decay | Amp Decay 1 | 5 / CC 34 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); retried 2 s, still none |
| MIMC-F-S02 | AMP ENV S | Amp envelope sustain | Amp Sustain 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away); retried 2 s, still none |
| MIMC-F-S08 | AMP ENV R | Amp envelope release | Amp Release 1 | — | display/Remote item, not mapped | tooltip "Amp Release 1: 189 ms" |
| MIMC-F-D21 | LFO WAVE display | LFO waveform | LFO Wave 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B35 | LFO WAVE arrows | Previous / next LFO wave | — | — | click only | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-B36 | KEY SYNC | LFO key sync | LFO Key Sync 1 | — | display/Remote item, not mapped | tooltip "LFO Key Sync 1" |
| MIMC-F-B37 | BEAT SYNC | LFO beat sync | LFO Beat Sync 1 | — | display/Remote item, not mapped | tooltip "LFO Beat Sync 1" |
| MIMC-F-K24 | LFO RATE | LFO rate | LFO Rate 1 | — | display/Remote item, not mapped | tooltip "LFO Rate 1: 1.58 Hz" |
| MIMC-F-K28 | LFO DELAY | LFO delay | LFO Delay 1 | — | display/Remote item, not mapped | tooltip "LFO Delay 1: 0.000 s" |
| MIMC-F-K25 | AMP VEL | Amp velocity amount | Amp Velocity 1 | — | display/Remote item, not mapped | tooltip "Amp Velocity 1: 0.0 %" |
| MIMC-F-K26 | AMP GAIN | Amp gain | Amp Gain 1 | 1 / CC 30 | voice/MIDI or click | tooltip "Amp Gain 1: 0.0 dB" |
| MIMC-F-K27 | AMP MOD amount | Amp mod amount | Amp ModAmt 1 | — | display/Remote item, not mapped | tooltip "Amp ModAmt 1: 0.0 %" |
| MIMC-F-D22 | AMP MOD source | Amp: mod source menu | Amp Mod 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-K29 | PAN | Pan | Pan 1 | — | display/Remote item, not mapped | tooltip "Pan 1: 0.0" |
| MIMC-F-K30 | PAN MOD amount | Pan mod amount | — | — | click only | tooltip "Pan ModAmt 1: 0.0 %" |
| MIMC-F-D24 | PAN MOD source | Pan: mod source menu | Pan Mod 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D19 | COMP light | Compressor indicator | Squeeze 1 | — | display/Remote item, not mapped | tooltip "Squeeze 1: 0.0 %" (shown on the Comp section's light) |
| MIMC-F-K31 | SQUEEZE | Compressor squeeze | Squeeze 1 | — | display/Remote item, not mapped | tooltip "Squeeze 1: 0.0 %" |
| MIMC-F-D23 | EFFECT type menu | Effect type menu (Noise ...) | Effect Type 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-F-D20 | EFFECT dots | Effect display | — | — | click only | tooltip "Effect Type 1: Noise" |
| MIMC-F-K32 | EFFECT MOD | Effect modulation | Effect Mod 1 | — | display/Remote item, not mapped | tooltip "Effect Mod 1: 50.0 %" |
| MIMC-F-K33 | EFFECT MIX | Effect mix | Effect Mix 1 | — | display/Remote item, not mapped | tooltip "Effect Mix 1: 0.0 %" |
| MIMC-F-K22 | LO CUT | Low cut | Lo Cut 1 | — | display/Remote item, not mapped | tooltip "Lo Cut 1: 20.0 Hz" |
| MIMC-F-K23 | HI CUT | High cut | Hi Cut 1 | — | display/Remote item, not mapped | tooltip "Hi Cut 1: 20.00 kHz" |
| MIMC-F-K34 | SEND 1 | Send 1 level | Send1 1 | — | display/Remote item, not mapped | tooltip "Send1 1: -∞ dB" |
| MIMC-F-K35 | SEND 2 | Send 2 level | — | — | click only | tooltip "Send2 1: -∞ dB" |
| MIMC-F-K301 | AMP GAIN (as Slot 2) | Amp Gain of slot 2: same physical control as MIMC-F-K26, aimed at slot 2 when that slot is selected | Amp Gain 2 | 6 / CC 35 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K26 (slot 2 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K302 | PITCH SEMI (as Slot 2) | Pitch Semi of slot 2: same physical control as MIMC-F-K09, aimed at slot 2 when that slot is selected | Pitch Semi 2 | 7 / CC 36 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K09 (slot 2 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K303 | FILTER FREQ (as Slot 2) | Filter Freq of slot 2: same physical control as MIMC-F-K12, aimed at slot 2 when that slot is selected | Filter Freq 2 | 8 / CC 37 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K12 (slot 2 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K304 | START marker (as Slot 2) | Start Pos of slot 2: same physical control as MIMC-F-B18, aimed at slot 2 when that slot is selected | Start Pos 2 | 9 / CC 38 | voice/MIDI or click | not separately hovered: same control as MIMC-F-B18 (slot 2 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K305 | AMP ENV D (as Slot 2) | Amp Decay of slot 2: same physical control as MIMC-F-S04, aimed at slot 2 when that slot is selected | Amp Decay 2 | 10 / CC 39 | voice/MIDI or click | not separately hovered: same control as MIMC-F-S04 (slot 2 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K306 | AMP GAIN (as Slot 3) | Amp Gain of slot 3: same physical control as MIMC-F-K26, aimed at slot 3 when that slot is selected | Amp Gain 3 | 11 / CC 40 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K26 (slot 3 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K307 | PITCH SEMI (as Slot 3) | Pitch Semi of slot 3: same physical control as MIMC-F-K09, aimed at slot 3 when that slot is selected | Pitch Semi 3 | 12 / CC 41 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K09 (slot 3 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K308 | FILTER FREQ (as Slot 3) | Filter Freq of slot 3: same physical control as MIMC-F-K12, aimed at slot 3 when that slot is selected | Filter Freq 3 | 13 / CC 42 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K12 (slot 3 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K309 | START marker (as Slot 3) | Start Pos of slot 3: same physical control as MIMC-F-B18, aimed at slot 3 when that slot is selected | Start Pos 3 | 14 / CC 43 | voice/MIDI or click | not separately hovered: same control as MIMC-F-B18 (slot 3 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K310 | AMP ENV D (as Slot 3) | Amp Decay of slot 3: same physical control as MIMC-F-S04, aimed at slot 3 when that slot is selected | Amp Decay 3 | 15 / CC 44 | voice/MIDI or click | not separately hovered: same control as MIMC-F-S04 (slot 3 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K311 | AMP GAIN (as Slot 4) | Amp Gain of slot 4: same physical control as MIMC-F-K26, aimed at slot 4 when that slot is selected | Amp Gain 4 | 16 / CC 45 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K26 (slot 4 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K312 | PITCH SEMI (as Slot 4) | Pitch Semi of slot 4: same physical control as MIMC-F-K09, aimed at slot 4 when that slot is selected | Pitch Semi 4 | 17 / CC 46 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K09 (slot 4 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K313 | FILTER FREQ (as Slot 4) | Filter Freq of slot 4: same physical control as MIMC-F-K12, aimed at slot 4 when that slot is selected | Filter Freq 4 | 18 / CC 47 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K12 (slot 4 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K314 | START marker (as Slot 4) | Start Pos of slot 4: same physical control as MIMC-F-B18, aimed at slot 4 when that slot is selected | Start Pos 4 | 19 / CC 48 | voice/MIDI or click | not separately hovered: same control as MIMC-F-B18 (slot 4 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K315 | AMP ENV D (as Slot 4) | Amp Decay of slot 4: same physical control as MIMC-F-S04, aimed at slot 4 when that slot is selected | Amp Decay 4 | 20 / CC 49 | voice/MIDI or click | not separately hovered: same control as MIMC-F-S04 (slot 4 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K316 | AMP GAIN (as Slot 5) | Amp Gain of slot 5: same physical control as MIMC-F-K26, aimed at slot 5 when that slot is selected | Amp Gain 5 | 21 / CC 50 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K26 (slot 5 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K317 | PITCH SEMI (as Slot 5) | Pitch Semi of slot 5: same physical control as MIMC-F-K09, aimed at slot 5 when that slot is selected | Pitch Semi 5 | 22 / CC 51 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K09 (slot 5 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K318 | FILTER FREQ (as Slot 5) | Filter Freq of slot 5: same physical control as MIMC-F-K12, aimed at slot 5 when that slot is selected | Filter Freq 5 | 23 / CC 52 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K12 (slot 5 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K319 | START marker (as Slot 5) | Start Pos of slot 5: same physical control as MIMC-F-B18, aimed at slot 5 when that slot is selected | Start Pos 5 | 24 / CC 53 | voice/MIDI or click | not separately hovered: same control as MIMC-F-B18 (slot 5 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K320 | AMP ENV D (as Slot 5) | Amp Decay of slot 5: same physical control as MIMC-F-S04, aimed at slot 5 when that slot is selected | Amp Decay 5 | 25 / CC 54 | voice/MIDI or click | not separately hovered: same control as MIMC-F-S04 (slot 5 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K321 | AMP GAIN (as Slot 6) | Amp Gain of slot 6: same physical control as MIMC-F-K26, aimed at slot 6 when that slot is selected | Amp Gain 6 | 26 / CC 55 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K26 (slot 6 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K322 | PITCH SEMI (as Slot 6) | Pitch Semi of slot 6: same physical control as MIMC-F-K09, aimed at slot 6 when that slot is selected | Pitch Semi 6 | 27 / CC 56 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K09 (slot 6 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K323 | FILTER FREQ (as Slot 6) | Filter Freq of slot 6: same physical control as MIMC-F-K12, aimed at slot 6 when that slot is selected | Filter Freq 6 | 28 / CC 57 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K12 (slot 6 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K324 | START marker (as Slot 6) | Start Pos of slot 6: same physical control as MIMC-F-B18, aimed at slot 6 when that slot is selected | Start Pos 6 | 29 / CC 58 | voice/MIDI or click | not separately hovered: same control as MIMC-F-B18 (slot 6 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K325 | AMP ENV D (as Slot 6) | Amp Decay of slot 6: same physical control as MIMC-F-S04, aimed at slot 6 when that slot is selected | Amp Decay 6 | 30 / CC 59 | voice/MIDI or click | not separately hovered: same control as MIMC-F-S04 (slot 6 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K326 | AMP GAIN (as Slot 7) | Amp Gain of slot 7: same physical control as MIMC-F-K26, aimed at slot 7 when that slot is selected | Amp Gain 7 | 31 / CC 60 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K26 (slot 7 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K327 | PITCH SEMI (as Slot 7) | Pitch Semi of slot 7: same physical control as MIMC-F-K09, aimed at slot 7 when that slot is selected | Pitch Semi 7 | 32 / CC 61 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K09 (slot 7 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K328 | FILTER FREQ (as Slot 7) | Filter Freq of slot 7: same physical control as MIMC-F-K12, aimed at slot 7 when that slot is selected | Filter Freq 7 | 33 / CC 62 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K12 (slot 7 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K329 | START marker (as Slot 7) | Start Pos of slot 7: same physical control as MIMC-F-B18, aimed at slot 7 when that slot is selected | Start Pos 7 | 34 / CC 63 | voice/MIDI or click | not separately hovered: same control as MIMC-F-B18 (slot 7 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K330 | AMP ENV D (as Slot 7) | Amp Decay of slot 7: same physical control as MIMC-F-S04, aimed at slot 7 when that slot is selected | Amp Decay 7 | 35 / CC 64 | voice/MIDI or click | not separately hovered: same control as MIMC-F-S04 (slot 7 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K331 | AMP GAIN (as Slot 8) | Amp Gain of slot 8: same physical control as MIMC-F-K26, aimed at slot 8 when that slot is selected | Amp Gain 8 | 36 / CC 65 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K26 (slot 8 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K332 | PITCH SEMI (as Slot 8) | Pitch Semi of slot 8: same physical control as MIMC-F-K09, aimed at slot 8 when that slot is selected | Pitch Semi 8 | 37 / CC 66 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K09 (slot 8 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K333 | FILTER FREQ (as Slot 8) | Filter Freq of slot 8: same physical control as MIMC-F-K12, aimed at slot 8 when that slot is selected | Filter Freq 8 | 38 / CC 67 | voice/MIDI or click | not separately hovered: same control as MIMC-F-K12 (slot 8 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K334 | START marker (as Slot 8) | Start Pos of slot 8: same physical control as MIMC-F-B18, aimed at slot 8 when that slot is selected | Start Pos 8 | 39 / CC 68 | voice/MIDI or click | not separately hovered: same control as MIMC-F-B18 (slot 8 must be selected first). Name+slot from the remotemap and Remote list |
| MIMC-F-K335 | AMP ENV D (as Slot 8) | Amp Decay of slot 8: same physical control as MIMC-F-S04, aimed at slot 8 when that slot is selected | Amp Decay 8 | 40 / CC 69 | voice/MIDI or click | not separately hovered: same control as MIMC-F-S04 (slot 8 must be selected first). Name+slot from the remotemap and Remote list |

## Mimic Creative Sampler — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| MIMC-B-D01 | BASIC VIBE tape (back) | Patch name tape (back) | — | — | click/drag only (no Remote item) | no tooltip in Reason (hovered 1.3 s, approached from 5 px away) |
| MIMC-B-J01 | Seq Gate In | Gate input from a sequencer | — | — | cable: right-click jack > device > jack name | tooltip "SeqGateInput" |
| MIMC-B-J05 | Seq Note CV In | Note CV input from a sequencer | — | — | cable: right-click jack > device > jack name | tooltip "SeqNoteInput" |
| MIMC-B-K01 | Pitch Bend CV trim | Amount for pitch bend CV | — | — | click/drag only (no Remote item) | tooltip "PitchBend CV Amount: 100.0 %" |
| MIMC-B-J02 | Pitch Bend CV In | CV input: pitch bend | — | — | cable: right-click jack > device > jack name | tooltip "PitchBend CV Input" |
| MIMC-B-K02 | Mod Wheel CV trim | Amount for mod wheel CV | — | — | click/drag only (no Remote item) | tooltip "ModWheel CV Amount: 100.0 %" |
| MIMC-B-J06 | Mod Wheel CV In | CV input: mod wheel | — | — | cable: right-click jack > device > jack name | tooltip "ModWheel CV Input" |
| MIMC-B-J03 | CV In 1 | CV input 1 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 1" |
| MIMC-B-J07 | CV In 2 | CV input 2 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 2" |
| MIMC-B-J04 | CV In 3 | CV input 3 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 3" |
| MIMC-B-J08 | CV In 4 | CV input 4 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 4" |
| MIMC-B-J09 | Slot 1 Out L | Audio output slot 1, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot1 Left" |
| MIMC-B-J10 | Slot 1 Out R | Audio output slot 1, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot1 Right" |
| MIMC-B-J11 | Slot 2 Out L | Audio output slot 2, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot2 Left" |
| MIMC-B-J12 | Slot 2 Out R | Audio output slot 2, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot2 Right" |
| MIMC-B-J13 | Slot 3 Out L | Audio output slot 3, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot3 Left" |
| MIMC-B-J14 | Slot 3 Out R | Audio output slot 3, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot3 Right" |
| MIMC-B-J15 | Slot 4 Out L | Audio output slot 4, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot4 Left" |
| MIMC-B-J16 | Slot 4 Out R | Audio output slot 4, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot4 Right" |
| MIMC-B-J17 | Slot 5 Out L | Audio output slot 5, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot5 Left" |
| MIMC-B-J18 | Slot 5 Out R | Audio output slot 5, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot5 Right" |
| MIMC-B-J19 | Slot 6 Out L | Audio output slot 6, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot6 Left" |
| MIMC-B-J20 | Slot 6 Out R | Audio output slot 6, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot6 Right" |
| MIMC-B-J21 | Slot 7 Out L | Audio output slot 7, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot7 Left" |
| MIMC-B-J22 | Slot 7 Out R | Audio output slot 7, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot7 Right" |
| MIMC-B-J23 | Slot 8 Out L | Audio output slot 8, left | — | — | cable: right-click jack > device > jack name | tooltip "Slot8 Left" |
| MIMC-B-J24 | Slot 8 Out R | Audio output slot 8, right | — | — | cable: right-click jack > device > jack name | tooltip "Slot8 Right" |
| MIMC-B-J25 | FX Send 1 L | FX send 1 output, left | — | — | cable: right-click jack > device > jack name | tooltip "Send1 Left" |
| MIMC-B-J26 | FX Send 1 R | FX send 1 output, right | — | — | cable: right-click jack > device > jack name | tooltip "Send1 Right" |
| MIMC-B-J27 | FX Send 2 L | FX send 2 output, left | — | — | cable: right-click jack > device > jack name | tooltip "Send2 Left" |
| MIMC-B-J28 | FX Send 2 R | FX send 2 output, right | — | — | cable: right-click jack > device > jack name | tooltip "Send2 Right" |
| MIMC-B-J29 | Master Out L | Master audio output, left | — | — | cable: right-click jack > device > jack name | tooltip "Left Output" |
| MIMC-B-J30 | Master Out R | Master audio output, right | — | — | cable: right-click jack > device > jack name | tooltip "Right Output" |

## Thor Polysonic Synthesizer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| THOR-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D01 | Range display | Keyboard range (number of keys) | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B02 | (range arrows) | Range down/up | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D02 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B03 | (patch arrows) | Previous / next patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch (upper half)" |
| THOR-F-B04 | (patch folder) | Browse patch | — | — | click only | tooltip "Browse patch" |
| THOR-F-B05 | (patch disk) | Save patch | — | — | click only | tooltip "Save patch" |
| THOR-F-D06 | Patch name tape | Patch name tape | Device Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-S01 | PITCH BEND wheel | Pitch bend wheel | Pitch Bend | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-S02 | MOD wheel | Mod wheel | Mod Wheel | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D03 | POLYPHONY display | Polyphony (voices) | Polyphony | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B06 | (polyphony arrows) | Polyphony down/up | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D07 | RELEASE POLYPHONY display | Release polyphony (voices) | Release Polyphony | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B11 | (release polyphony arrows) | Release polyphony down/up | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B07 | KEY MODE: Mono legato | Key mode: mono legato | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B08 | KEY MODE: Mono retrig | Key mode: mono retrig | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B12 | KEY MODE: Polyphonic | Key mode: polyphonic | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B13 | KEY MODE (mode button) | Key mode / Remote item 'Key Mode' | Key Mode | — | display/Remote item, not mapped | tooltip "Key Mode" |
| THOR-F-K03 | PORTAMENTO knob | Portamento | Portamento | — | display/Remote item, not mapped | tooltip "Portamento: 40" |
| THOR-F-B14 | PORTAMENTO switch (OFF/ON/AUTO) | Portamento mode | Portamento Mode | — | display/Remote item, not mapped | tooltip "Portamento Mode: 0" |
| THOR-F-B19 | Show Programmer | Show/hide the programmer panel | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B09 | TRIGGER: MIDI | Note trigger: MIDI | Note Trigger MIDI | — | display/Remote item, not mapped | tooltip "Note Trigger MIDI" |
| THOR-F-B10 | TRIGGER: STEP SEQ | Note trigger: step sequencer | Note Trigger Step Seq | — | display/Remote item, not mapped | tooltip "Note Trigger Step Seq" |
| THOR-F-D08 | NOTE ON light | Note-on light | Note On Indicator | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K01 | ROTARY 1 | Rotary 1 knob | Rotary 1 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D04 | ROTARY 1 label display | Rotary 1 label (assignment name) | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K02 | ROTARY 2 | Rotary 2 knob | Rotary 2 | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D05 | ROTARY 2 label display | Rotary 2 label (assignment name) | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B15 | BUTTON 1 | Button 1 | Button 1 | — | display/Remote item, not mapped | tooltip "Button 1" |
| THOR-F-D09 | BUTTON 1 display | Button 1 assignment display | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B16 | (button 1 arrows) | Button 1 destination prev/next | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D11 | BUTTON 1 label | Button 1 label | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B17 | BUTTON 2 | Button 2 | Button 2 | — | display/Remote item, not mapped | tooltip "Button 2" |
| THOR-F-D10 | BUTTON 2 display | Button 2 assignment display | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B18 | (button 2 arrows) | Button 2 destination prev/next | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D12 | BUTTON 2 label | Button 2 label | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K04 | MASTER VOLUME | Master level | Master Level | 48 / CC 77 | voice/MIDI or click | tooltip "Master Level: -19.1 dB" |
| THOR-F-K14 | OSC 1 AM FROM OSC 2 | Osc 1 amplitude modulation from osc 2 | Osc 1 AM From Osc 2 | — | display/Remote item, not mapped | tooltip "Osc 1 AM From Osc 2: 0" |
| THOR-F-D13 | OSC 1 type menu | Osc 1 type (Multi Osc) | Osc 1 Type | 1 / CC 30 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K05 | OSC 1 KBD | Osc 1 keyboard tracking | Osc 1 Kbd | — | display/Remote item, not mapped | tooltip "Osc 1 Kbd: 127" |
| THOR-F-K06 | OSC 1 OCT | Osc 1 octave | Osc 1 Oct | 2 / CC 31 | voice/MIDI or click | tooltip "Osc 1 Oct: 4" |
| THOR-F-K07 | OSC 1 SEMI | Osc 1 semitone | Osc 1 Semi | 3 / CC 32 | voice/MIDI or click | tooltip "Osc 1 Semi: 0" |
| THOR-F-K08 | OSC 1 TUNE | Osc 1 fine tune | Osc 1 Tune | 4 / CC 33 | voice/MIDI or click | tooltip "Osc 1 Tune: -1" |
| THOR-F-D16 | MULTI OSC DETUNE MODE display | Multi osc detune mode | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B27 | (detune mode arrows) | Detune mode prev/next | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K25 | OSC 1 DETUNE AMT | Osc 1 detune amount | Osc 1 Mod | 5 / CC 34 | voice/MIDI or click | tooltip "Osc 1 Detune Amt: 37" |
| THOR-F-B39 | OSC 1 MULTI WAVE | Osc 1 multi waveform select | — | — | click only | tooltip "Osc 1 Multi Wave" |
| THOR-F-D15 | OSC 1 mode LED 1 | Osc 1 multi osc mode light 1 | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D17 | OSC 1 mode LED 2 | Osc 1 multi osc mode light 2 | — | — | click only | not hovered (indicator light / sub-part of a hovered control) |
| THOR-F-D18 | OSC 1 mode LED 3 | Osc 1 multi osc mode light 3 | — | — | click only | not hovered (indicator light / sub-part of a hovered control) |
| THOR-F-D19 | OSC 1 mode LED 4 | Osc 1 multi osc mode light 4 | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D21 | OSC 2 type menu | Osc 2 type (Wavetable Osc) | Osc 2 Type | 6 / CC 35 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K30 | OSC 2 KBD | Osc 2 keyboard tracking | Osc 2 Kbd | — | display/Remote item, not mapped | tooltip "Osc 2 Kbd: 127" |
| THOR-F-K31 | OSC 2 OCT | Osc 2 octave | Osc 2 Oct | 7 / CC 36 | voice/MIDI or click | tooltip "Osc 2 Oct: 4" |
| THOR-F-K32 | OSC 2 SEMI | Osc 2 semitone | Osc 2 Semi | 8 / CC 37 | voice/MIDI or click | tooltip "Osc 2 Semi: 0" |
| THOR-F-K33 | OSC 2 TUNE | Osc 2 fine tune | Osc 2 Tune | 9 / CC 38 | voice/MIDI or click | tooltip "Osc 2 Tune: 0" |
| THOR-F-D23 | TABLE SELECT display | Osc 2 wavetable name | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B46 | (table arrows) | Wavetable prev/next | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K39 | OSC 2 POSITION | Osc 2 wavetable position | Osc 2 Mod | 10 / CC 39 | voice/MIDI or click | tooltip "Osc 2 Pos: 93" |
| THOR-F-B55 | OSC 2 X-FADE | Osc 2 wavetable smooth crossfade | — | — | click only | tooltip "Osc 2 Wavetable Smooth X fade" |
| THOR-F-D26 | OSC 2 X-FADE light | Osc 2 x-fade light | — | — | click only | not hovered (indicator light / sub-part of a hovered control) |
| THOR-F-B43 | OSC 2 SYNC | Osc 2 sync to osc 1 | Osc 2 Sync To Osc 1 | — | display/Remote item, not mapped | tooltip "Osc 2 Sync To Osc 1" |
| THOR-F-K46 | OSC 2 SYNC BW | Osc 2 sync bandwidth | Osc 2 Sync BW | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B56 | OSC 3 SYNC | Osc 3 sync to osc 1 | Osc 3 Sync To Osc 1 | — | display/Remote item, not mapped | tooltip "Osc 3 Sync To Osc 1" |
| THOR-F-K53 | OSC 3 SYNC BW | Osc 3 sync bandwidth | Osc 3 Sync BW | — | display/Remote item, not mapped | tooltip "Osc 3 Sync BW: 127" |
| THOR-F-D25 | OSC 3 type menu | Osc 3 type (Analog Osc) | Osc 3 Type | 11 / CC 40 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K47 | OSC 3 KBD | Osc 3 keyboard tracking | Osc 3 Kbd | — | display/Remote item, not mapped | tooltip "Osc 3 Kbd: 127" |
| THOR-F-K48 | OSC 3 OCT | Osc 3 octave | Osc 3 Oct | 12 / CC 41 | voice/MIDI or click | tooltip "Osc 3 Oct: 4" |
| THOR-F-K49 | OSC 3 SEMI | Osc 3 semitone | Osc 3 Semi | 13 / CC 42 | voice/MIDI or click | tooltip "Osc 3 Semi: 0" |
| THOR-F-K50 | OSC 3 TUNE | Osc 3 fine tune | Osc 3 Tune | 14 / CC 43 | voice/MIDI or click | tooltip "Osc 3 Tune: -1" |
| THOR-F-B65 | OSC 3 wave button 1 | Osc 3 analog waveform 1 | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B66 | OSC 3 wave button 2 | Osc 3 analog waveform 2 | — | — | click only | not hovered; same group as the first wave button, which gave no tooltip |
| THOR-F-B67 | OSC 3 wave button 3 | Osc 3 analog waveform 3 | — | — | click only | not hovered; same group as the first wave button, which gave no tooltip |
| THOR-F-B72 | OSC 3 wave button 4 | Osc 3 analog waveform 4 | — | — | click only | not hovered; same group as the first wave button, which gave no tooltip |
| THOR-F-K54 | OSC 3 PW | Osc 3 pulse width | Osc 3 Mod | 15 / CC 44 | voice/MIDI or click | tooltip "Osc 3 PW: 93" |
| THOR-F-B71 | OSC 3 ANALOG WAVE | Osc 3 analog waveform select | — | — | click only | tooltip "Osc 3 Analog Wave" |
| THOR-F-D14 | FILTER 1 type menu | Filter 1 type (Low Pass Ladder) | Filter 1 Type | 19 / CC 48 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B21 | FILTER 1 SELF OSC | Filter 1 self oscillation | Filter 1 Self Osc | — | display/Remote item, not mapped | tooltip "Filter 1 Self Osc" |
| THOR-F-B30 | FILTER 1 slope button 1 | Filter 1 ladder slope selector 1 | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B31 | FILTER 1 slope button 2 | Filter 1 ladder slope selector 2 | — | — | click only | not hovered; same group, other buttons gave no tooltip |
| THOR-F-B32 | FILTER 1 slope button 3 | Filter 1 ladder slope selector 3 | — | — | click only | not hovered; same group, other buttons gave no tooltip |
| THOR-F-B36 | FILTER 1 slope button 4 | Filter 1 ladder slope selector 4 | — | — | click only | not hovered; same group, other buttons gave no tooltip |
| THOR-F-B37 | FILTER 1 slope button 5 | Filter 1 ladder slope selector 5 | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K16 | FILTER 1 FREQ | Filter 1 frequency | Filter 1 Freq | 20 / CC 49 | voice/MIDI or click | tooltip "Filter 1 Freq: 9.30 kHz" |
| THOR-F-K17 | FILTER 1 RES | Filter 1 resonance | Filter 1 Res | 21 / CC 50 | voice/MIDI or click | tooltip "Filter 1 Res: 0" |
| THOR-F-K15 | FILTER 1 DRIVE | Filter 1 drive | Filter 1 Drive | 22 / CC 51 | voice/MIDI or click | tooltip "Filter 1 Drive: 79" |
| THOR-F-B40 | FILTER 1 INV | Filter 1 envelope invert | Filter 1 Env Invert | — | display/Remote item, not mapped | tooltip "Filter 1 Env Invert" |
| THOR-F-K26 | FILTER 1 ENV | Filter 1 envelope amount | Filter 1 Env Amount | 23 / CC 52 | voice/MIDI or click | tooltip "Filter 1 Env Amount: 33" |
| THOR-F-K27 | FILTER 1 VEL | Filter 1 velocity | Filter 1 Velocity | — | display/Remote item, not mapped | tooltip "Filter 1 Velocity: 47" |
| THOR-F-K28 | FILTER 1 KBD | Filter 1 keyboard tracking | Filter 1 Kbd | 24 / CC 53 | voice/MIDI or click | tooltip "Filter 1 Kbd: 0" |
| THOR-F-B41 | FILTER 1 slope selector | Filter 1 ladder slope | — | — | click only | tooltip "Filter 1 Ladder Slope" |
| THOR-F-B22 | FILTER 1 power | Filter 1 on/off | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B20 | OSC 1 to FILTER 1 | Route osc 1 to filter 1 | Osc 1 To Filter 1 Enable | — | display/Remote item, not mapped | tooltip "Osc 1 To Filter 1 Enable" |
| THOR-F-B64 | OSC 1 to FILTER 2 | Route osc 1 to filter 2 | Osc 1 To Filter 2 Enable | — | display/Remote item, not mapped | tooltip "Osc 1 To Filter 2 Enable" |
| THOR-F-B28 | OSC 2 to FILTER 1 | Route osc 2 to filter 1 | Osc 2 To Filter 1 Enable | — | display/Remote item, not mapped | tooltip "Osc 2 To Filter 1 Enable" |
| THOR-F-B68 | OSC 2 to FILTER 2 | Route osc 2 to filter 2 | Osc 2 To Filter 2 Enable | — | display/Remote item, not mapped | tooltip "Osc 2 To Filter 2 Enable" |
| THOR-F-B29 | OSC 3 to FILTER 1 | Route osc 3 to filter 1 | Osc 3 To Filter 1 Enable | — | display/Remote item, not mapped | tooltip "Osc 3 To Filter 1 Enable" |
| THOR-F-B69 | OSC 3 to FILTER 2 | Route osc 3 to filter 2 | Osc 3 To Filter 2 Enable | — | display/Remote item, not mapped | tooltip "Osc 3 To Filter 2 Enable" |
| THOR-F-K37 | MIXER BALANCE | Osc 1 and 2 balance | Osc 1 And 2 Balance | 18 / CC 47 | voice/MIDI or click | tooltip "Osc 1 And 2 Balance: 64" |
| THOR-F-S07 | MIXER OSC 1+2 slider | Osc 1 and 2 level | Osc 1 And 2 Level | 17 / CC 46 | voice/MIDI or click | tooltip "Osc 1 And 2 Level: -2.1 dB" |
| THOR-F-S08 | MIXER OSC 3 slider | Osc 3 level | Osc 3 Level | 16 / CC 45 | voice/MIDI or click | tooltip "Osc 3 Level: -2.1 dB" |
| THOR-F-B44 | SHAPER on | Shaper on/off | Shaper On | 40 / CC 69 | voice/MIDI or click | tooltip "Shaper On" |
| THOR-F-D24 | SHAPER type menu | Shaper type | Shaper Type | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B47 | (shaper type arrows) | Shaper type prev/next | — | — | click only | not hovered (indicator light / sub-part of a hovered control) |
| THOR-F-K38 | SHAPER DRIVE | Shaper drive | Shaper Drive | 41 / CC 70 | voice/MIDI or click | tooltip "Shaper Drive: 37" |
| THOR-F-K40 | AMP VEL | Amplifier velocity | Amplifier Velocity | — | display/Remote item, not mapped | tooltip "Amplifier Velocity: 105" |
| THOR-F-K41 | AMP GAIN | Amplifier gain | Amplifier Gain | 37 / CC 66 | voice/MIDI or click | tooltip "Amplifier Gain: -5.2 dB" |
| THOR-F-K42 | AMP PAN | Amplifier pan | Amplifier Pan | — | display/Remote item, not mapped | tooltip "Amplifier Pan: 0" |
| THOR-F-B50 | SHAPER to FILTER 2 | Shaper output to filter 2 | — | — | click only | tooltip "Shaper to Filter 2" |
| THOR-F-B51 | SHAPER to AMP | Shaper output to amplifier | — | — | click only | tooltip "Shaper to Amplifier" |
| THOR-F-B52 | FILTER 2 to AMP | Filter 2 output to amplifier | Filter2ToAmplifier Enable | — | display/Remote item, not mapped | tooltip "Filter2ToAmplifier Enable" |
| THOR-F-D27 | FILTER 2 type menu | Filter 2 type (bypassed, folded view) | Filter 2 Type | 25 / CC 54 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B23 | LFO 1 KEY SYNC | LFO 1 key sync | LFO 1 Key Sync | — | display/Remote item, not mapped | tooltip "LFO 1 Key Sync" |
| THOR-F-B33 | LFO 1 TEMPO SYNC | LFO 1 tempo sync | LFO 1 Tempo Sync | — | display/Remote item, not mapped | tooltip "LFO 1 Tempo Sync" |
| THOR-F-K18 | LFO 1 RATE | LFO 1 rate | LFO 1 Rate | 38 / CC 67 | voice/MIDI or click | tooltip "LFO 1 Rate: 1/8T" |
| THOR-F-K19 | LFO 1 DELAY | LFO 1 delay | LFO 1 Delay | — | display/Remote item, not mapped | tooltip "LFO 1 Delay: 0.0 ms" |
| THOR-F-K29 | LFO 1 KBD FOLLOW | LFO 1 keyboard follow | LFO 1 KbdFollow | — | display/Remote item, not mapped | tooltip "LFO 1 KbdFollow: 0" |
| THOR-F-D22 | LFO 1 WAVEFORM | LFO 1 waveform | LFO 1 Waveform | 39 / CC 68 | voice/MIDI or click | tooltip "LFO 1 Waveform: 0" |
| THOR-F-B45 | (LFO 1 waveform arrows) | LFO 1 waveform prev/next | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B24 | MOD ENV GATE TRIG | Mod envelope gate trigger | Mod Env Gate Trig On | — | display/Remote item, not mapped | tooltip "Mod Env Gate Trig On" |
| THOR-F-B34 | MOD ENV TEMPO SYNC | Mod envelope tempo sync | Mod Env Tempo Sync | — | display/Remote item, not mapped | tooltip "Mod Env Tempo Sync" |
| THOR-F-B38 | MOD ENV LOOP | Mod envelope loop | Mod Env Loop | — | display/Remote item, not mapped | tooltip "Mod Env Loop" |
| THOR-F-S05 | MOD ENV DELAY | Mod envelope delay | Mod Env Delay | — | display/Remote item, not mapped | tooltip "Mod Env Delay: 0.0 ms" |
| THOR-F-S06 | MOD ENV A | Mod envelope attack | Mod Env Attack | — | display/Remote item, not mapped | tooltip "Mod Env Attack: 0.0 ms" |
| THOR-F-S03 | MOD ENV D | Mod envelope decay | Mod Env Decay | — | display/Remote item, not mapped | tooltip "Mod Env Decay: 4.35 s" |
| THOR-F-S04 | MOD ENV R | Mod envelope release | Mod Env Release | — | display/Remote item, not mapped | tooltip "Mod Env Release: 4.35 s" |
| THOR-F-B57 | FILTER ENV GATE TRIG | Filter envelope gate trigger | Filter Env Gate Trig On | — | display/Remote item, not mapped | tooltip "Filter Env Gate Trig On" |
| THOR-F-S10 | FILTER ENV A | Filter envelope attack | Filter Env Attack | 29 / CC 58 | voice/MIDI or click | tooltip "Filter Env Attack: 0.0 ms" |
| THOR-F-S11 | FILTER ENV D | Filter envelope decay | Filter Env Decay | 30 / CC 59 | voice/MIDI or click | tooltip "Filter Env Decay: 4.35 s" |
| THOR-F-S12 | FILTER ENV S | Filter envelope sustain | Filter Env Sustain | 31 / CC 60 | voice/MIDI or click | tooltip "Filter Env Sustain: -21.8 dB" |
| THOR-F-S09 | FILTER ENV R | Filter envelope release | Filter Env Release | 32 / CC 61 | voice/MIDI or click | tooltip "Filter Env Release: 4.35 s" |
| THOR-F-B58 | AMP ENV GATE TRIG | Amp envelope gate trigger | Amp Env Gate Trig On | — | display/Remote item, not mapped | tooltip "Amp Env Gate Trig On" |
| THOR-F-S13 | AMP ENV A | Amp envelope attack | Amp Env Attack | 33 / CC 62 | voice/MIDI or click | tooltip "Amp Env Attack: 0.4 ms" |
| THOR-F-S14 | AMP ENV D | Amp envelope decay | Amp Env Decay | 34 / CC 63 | voice/MIDI or click | tooltip "Amp Env Decay: 3.49 s" |
| THOR-F-S15 | AMP ENV S | Amp envelope sustain | Amp Env Sustain | 35 / CC 64 | voice/MIDI or click | tooltip "Amp Env Sustain: -108.2 dB" |
| THOR-F-S16 | AMP ENV R | Amp envelope release | Amp Env Release | 36 / CC 65 | voice/MIDI or click | tooltip "Amp Env Release: 3.82 s" |
| THOR-F-B25 | DELAY on | Delay on/off | Delay On | 42 / CC 71 | voice/MIDI or click | tooltip "Delay On" |
| THOR-F-B26 | DELAY SYNC | Delay tempo sync | Delay Sync | — | display/Remote item, not mapped | tooltip "Delay Sync" |
| THOR-F-K09 | DELAY TIME | Delay time | Delay Time | 44 / CC 73 | voice/MIDI or click | tooltip "Delay Time: 2/16" |
| THOR-F-K10 | DELAY F.BACK | Delay feedback | Delay Feedback | 45 / CC 74 | voice/MIDI or click | tooltip "Delay Feedback: 50" |
| THOR-F-K11 | DELAY RATE | Delay modulation rate | Delay Rate | — | display/Remote item, not mapped | tooltip "Delay Rate: 0.63 Hz" |
| THOR-F-K12 | DELAY AMT | Delay modulation amount | Delay Amt | — | display/Remote item, not mapped | tooltip "Delay Amt: 45" |
| THOR-F-K13 | DELAY D/WET | Delay dry/wet | Delay Dry Wet | 43 / CC 72 | voice/MIDI or click | tooltip "Delay Dry Wet: 0" |
| THOR-F-B35 | CHORUS on | Chorus on/off | Chorus On | 46 / CC 75 | voice/MIDI or click | tooltip "Chorus On" |
| THOR-F-K20 | CHORUS DELAY | Chorus delay | Chorus Delay | — | display/Remote item, not mapped | tooltip "Chorus Delay: 12.1 ms" |
| THOR-F-K21 | CHORUS F.BACK | Chorus feedback | Chorus Feedback | — | display/Remote item, not mapped | tooltip "Chorus Feedback: 0" |
| THOR-F-K22 | CHORUS RATE | Chorus rate | Chorus Rate | — | display/Remote item, not mapped | tooltip "Chorus Rate: 0.66 Hz" |
| THOR-F-K23 | CHORUS AMT | Chorus amount | Chorus Amt | — | display/Remote item, not mapped | tooltip "Chorus Amt: 32" |
| THOR-F-K24 | CHORUS D/WET | Chorus dry/wet | Chorus Dry Wet | 47 / CC 76 | voice/MIDI or click | tooltip "Chorus Dry Wet: 60" |
| THOR-F-D20 | COMB FILTER type menu | Filter 3 type (Comb Filter) | Filter 3 Type | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B42 | COMB FILTER power | Filter 3 on/off | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K34 | COMB DRIVE | Filter 3 drive | Filter 3 Drive | — | display/Remote item, not mapped | tooltip "Filter 3 Drive: 80" |
| THOR-F-K35 | COMB FREQ | Filter 3 frequency | Filter 3 Freq | — | display/Remote item, not mapped | tooltip "Filter 3 Freq: 9.30 kHz" |
| THOR-F-K36 | COMB RES | Filter 3 resonance | Filter 3 Res | — | display/Remote item, not mapped | tooltip "Filter 3 Res: 0" |
| THOR-F-B48 | COMB+ | Comb filter positive | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B49 | COMB- | Comb filter negative | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B54 | COMB MODE | Filter 3 comb preset | — | — | click only | tooltip "Filter 3 Comb Preset" |
| THOR-F-B53 | COMB INV | Filter 3 global envelope invert | Filter 3 Global Env Invert | — | display/Remote item, not mapped | tooltip "Filter 3 Global Env Invert" |
| THOR-F-K43 | COMB ENV | Filter 3 global envelope amount | Filter 3 Global Env Amount | — | display/Remote item, not mapped | tooltip "Filter 3 Global Env Amount: 0" |
| THOR-F-K44 | COMB VEL | Filter 3 velocity | Filter 3 Velocity | — | display/Remote item, not mapped | tooltip "Filter 3 Velocity: 47" |
| THOR-F-K45 | COMB KBD | Filter 3 keyboard tracking | Filter 3 Kbd | — | display/Remote item, not mapped | tooltip "Filter 3 Kbd: 0" |
| THOR-F-B59 | GLOBAL ENV GATE TRIG | Global envelope gate trigger | Global Env Gate Trig On | — | display/Remote item, not mapped | tooltip "Global Env Gate Trig On" |
| THOR-F-B61 | GLOBAL ENV TEMPO SYNC | Global envelope tempo sync | Global Env Tempo Sync | — | display/Remote item, not mapped | tooltip "Global Env Tempo Sync" |
| THOR-F-B60 | GLOBAL ENV LOOP | Global envelope loop | Global Env Loop | — | display/Remote item, not mapped | tooltip "Global Env Loop" |
| THOR-F-S17 | GLOBAL ENV DELAY | Global envelope delay | Global Env Delay | — | display/Remote item, not mapped | tooltip "Global Env Delay: 0.0 ms" |
| THOR-F-S18 | GLOBAL ENV A | Global envelope attack | Global Env Attack | — | display/Remote item, not mapped | tooltip "Global Env Attack: 0.0 ms" |
| THOR-F-S19 | GLOBAL ENV HOLD | Global envelope hold | Global Env Hold | — | display/Remote item, not mapped | tooltip "Global Env Hold: 0.0 ms" |
| THOR-F-S20 | GLOBAL ENV D | Global envelope decay | Global Env Decay | — | display/Remote item, not mapped | tooltip "Global Env Decay: 1.24 s" |
| THOR-F-S21 | GLOBAL ENV S | Global envelope sustain | Global Env Sustain | — | display/Remote item, not mapped | tooltip "Global Env Sustain: -21.8 dB" |
| THOR-F-S22 | GLOBAL ENV R | Global envelope release | Global Env Release | — | display/Remote item, not mapped | tooltip "Global Env Release: 1.24 s" |
| THOR-F-B62 | LFO 2 KEY SYNC | LFO 2 key sync | LFO 2 Key Sync | — | display/Remote item, not mapped | tooltip "LFO 2 Key Sync" |
| THOR-F-B63 | LFO 2 TEMPO SYNC | LFO 2 tempo sync | LFO 2 Tempo Sync | — | display/Remote item, not mapped | tooltip "LFO 2 Tempo Sync" |
| THOR-F-K51 | LFO 2 RATE | LFO 2 rate | LFO 2 Rate | — | display/Remote item, not mapped | tooltip "LFO 2 Rate: 5/4" |
| THOR-F-K52 | LFO 2 DELAY | LFO 2 delay | LFO 2 Delay | — | display/Remote item, not mapped | tooltip "LFO 2 Delay: 0.0 ms" |
| THOR-F-D28 | LFO 2 WAVEFORM | LFO 2 waveform | LFO 2 Waveform | — | display/Remote item, not mapped | tooltip "LFO 2 Waveform: 0" |
| THOR-F-B70 | (LFO 2 waveform arrows) | LFO 2 waveform prev/next | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D29 | MOD 1 source menu | Mod 1 source | Mod 1 Source | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D30 | MOD 1 dest amount | Mod 1 destination amount | Mod 1 Dest Amount | — | display/Remote item, not mapped | tooltip "Mod 1 Dest Amount: 15" |
| THOR-F-D31 | MOD 1 dest menu | Mod 1 destination | Mod 1 Dest | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D32 | MOD 1 scale amount | Mod 1 scale amount | Mod 1 Scale Amount | — | display/Remote item, not mapped | tooltip "Mod 1 Scale Amount: 0" |
| THOR-F-D33 | MOD 1 scale menu | Mod 1 scale source | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B73 | MOD 1 clear | Clear mod row 1 | — | — | click only | tooltip "Clear Sources, Modulations and Scales" |
| THOR-F-D41 | MOD 2 source menu | Mod 2 source | Mod 2 Source | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D43 | MOD 2 dest amount | Mod 2 destination amount | Mod 2 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D45 | MOD 2 dest menu | Mod 2 destination | Mod 2 Dest | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D47 | MOD 2 scale amount | Mod 2 scale amount | Mod 2 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D49 | MOD 2 scale menu | Mod 2 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B75 | MOD 2 clear | Clear mod row 2 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D42 | MOD 3 source menu | Mod 3 source | Mod 3 Source | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D44 | MOD 3 dest amount | Mod 3 destination amount | Mod 3 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D46 | MOD 3 dest menu | Mod 3 destination | Mod 3 Dest | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D48 | MOD 3 scale amount | Mod 3 scale amount | Mod 3 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D50 | MOD 3 scale menu | Mod 3 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B76 | MOD 3 clear | Clear mod row 3 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D65 | MOD 4 source menu | Mod 4 source | Mod 4 Source | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D67 | MOD 4 dest amount | Mod 4 destination amount | Mod 4 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D69 | MOD 4 dest menu | Mod 4 destination | Mod 4 Dest | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D71 | MOD 4 scale amount | Mod 4 scale amount | Mod 4 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D73 | MOD 4 scale menu | Mod 4 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B79 | MOD 4 clear | Clear mod row 4 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D66 | MOD 5 source menu | Mod 5 source | Mod 5 Source | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D68 | MOD 5 dest amount | Mod 5 destination amount | Mod 5 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D70 | MOD 5 dest menu | Mod 5 destination | Mod 5 Dest | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D72 | MOD 5 scale amount | Mod 5 scale amount | Mod 5 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D74 | MOD 5 scale menu | Mod 5 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B80 | MOD 5 clear | Clear mod row 5 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D82 | MOD 6 source menu | Mod 6 source | Mod 6 Source | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D84 | MOD 6 dest amount | Mod 6 destination amount | Mod 6 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D86 | MOD 6 dest menu | Mod 6 destination | Mod 6 Dest | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D88 | MOD 6 scale amount | Mod 6 scale amount | Mod 6 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D90 | MOD 6 scale menu | Mod 6 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B82 | MOD 6 clear | Clear mod row 6 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D83 | MOD 7 source menu | Mod 7 source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D85 | MOD 7 dest amount | Mod 7 destination amount | Mod 7 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D87 | MOD 7 dest menu | Mod 7 destination | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D89 | MOD 7 scale amount | Mod 7 scale amount | Mod 7 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D91 | MOD 7 scale menu | Mod 7 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B83 | MOD 7 clear | Clear mod row 7 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D34 | MOD 8 source menu | Mod 8 source | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D35 | MOD 8 dest amount | Mod 8 destination amount | Mod 8 Dest Amount | — | display/Remote item, not mapped | tooltip "Mod 8 Dest Amount: -88" |
| THOR-F-D36 | MOD 8 dest 1 menu | Mod 8 destination 1 | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D37 | MOD 8 dest 2 amount | Mod 8 destination 2 amount | Mod 8 Dest 2 Amount | — | display/Remote item, not mapped | tooltip "Mod 8 Dest 2 Amount: 56" |
| THOR-F-D38 | MOD 8 dest 2 menu | Mod 8 destination 2 | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D39 | MOD 8 scale amount | Mod 8 scale amount | Mod 8 Scale Amount | — | display/Remote item, not mapped | tooltip "Mod 8 Scale Amount: 0" |
| THOR-F-D40 | MOD 8 scale menu | Mod 8 scale source | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B74 | MOD 8 clear | Clear mod row 8 | — | — | click only | tooltip "Clear Sources, Modulations and Scales" |
| THOR-F-D51 | MOD 9 source menu | Mod 9 source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D53 | MOD 9 dest amount | Mod 9 destination amount | Mod 9 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D55 | MOD 9 dest 1 menu | Mod 9 destination 1 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D57 | MOD 9 dest 2 amount | Mod 9 destination 2 amount | Mod 9 Dest 2 Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D59 | MOD 9 dest 2 menu | Mod 9 destination 2 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D61 | MOD 9 scale amount | Mod 9 scale amount | Mod 9 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D63 | MOD 9 scale menu | Mod 9 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B77 | MOD 9 clear | Clear mod row 9 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D52 | MOD 10 source menu | Mod 10 source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D54 | MOD 10 dest amount | Mod 10 destination amount | Mod 10 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D56 | MOD 10 dest 1 menu | Mod 10 destination 1 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D58 | MOD 10 dest 2 amount | Mod 10 destination 2 amount | Mod 10 Dest 2 Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D60 | MOD 10 dest 2 menu | Mod 10 destination 2 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D62 | MOD 10 scale amount | Mod 10 scale amount | Mod 10 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D64 | MOD 10 scale menu | Mod 10 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B78 | MOD 10 clear | Clear mod row 10 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D75 | MOD 11 source menu | Mod 11 source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D76 | MOD 11 dest amount | Mod 11 destination amount | Mod 11 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D77 | MOD 11 dest 1 menu | Mod 11 destination 1 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D78 | MOD 11 dest 2 amount | Mod 11 destination 2 amount | Mod 11 Dest 2 Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D79 | MOD 11 dest 2 menu | Mod 11 destination 2 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D80 | MOD 11 scale amount | Mod 11 scale amount | Mod 11 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D81 | MOD 11 scale menu | Mod 11 scale source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B81 | MOD 11 clear | Clear mod row 11 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D92 | MOD 12 source menu | Mod 12 source | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D94 | MOD 12 dest amount | Mod 12 destination amount | Mod 12 Dest Amount | — | display/Remote item, not mapped | tooltip "Mod 12 Dest Amount: 0" |
| THOR-F-D96 | MOD 12 dest menu | Mod 12 destination | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D98 | MOD 12 scale amount | Mod 12 scale 1 amount | Mod 12 Scale Amount | — | display/Remote item, not mapped | tooltip "Mod 12 Scale Amount: 0" |
| THOR-F-D100 | MOD 12 scale 1 menu | Mod 12 scale 1 source | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-D102 | MOD 12 scale 2 amount | Mod 12 scale 2 amount | Mod 12 Scale 2 Amount | — | display/Remote item, not mapped | tooltip "Mod 12 Scale 2 Amount: 0" |
| THOR-F-D104 | MOD 12 scale 2 menu | Mod 12 scale 2 source | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B84 | MOD 12 clear | Clear mod row 12 | — | — | click only | tooltip "Clear Sources, Modulations and Scales" |
| THOR-F-D93 | MOD 13 source menu | Mod 13 source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D95 | MOD 13 dest amount | Mod 13 destination amount | Mod 13 Dest Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D97 | MOD 13 dest menu | Mod 13 destination | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D99 | MOD 13 scale amount | Mod 13 scale 1 amount | Mod 13 Scale Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D101 | MOD 13 scale 1 menu | Mod 13 scale 1 source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D103 | MOD 13 scale 2 amount | Mod 13 scale 2 amount | Mod 13 Scale 2 Amount | — | display/Remote item, not mapped | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D105 | MOD 13 scale 2 menu | Mod 13 scale 2 source | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-B85 | MOD 13 clear | Clear mod row 13 | — | — | click only | not hovered; same column as the hovered row, name follows the row pattern (row number from table order). Click to confirm before relying on it. |
| THOR-F-D501 | FILTER 2 type menu | Filter 2 type (menu arrow) | Filter 2 Type | 25 / CC 54 | voice/MIDI or click | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B501 | FILTER 2 power | Filter 2 on/off (close button) | — | — | click only | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B502 | FILTER 2 SELF OSC | Filter 2 self oscillation | Filter 2 Self Osc | — | display/Remote item, not mapped | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Self Osc" |
| THOR-F-B503 | FILTER 2 slope button 1 | Filter 2 ladder slope selector 1 | — | — | click only | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B504 | FILTER 2 slope button 2 | Filter 2 ladder slope selector 2 | — | — | click only | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B505 | FILTER 2 slope button 3 | Filter 2 ladder slope selector 3 | — | — | click only | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B506 | FILTER 2 slope button 4 | Filter 2 ladder slope selector 4 | — | — | click only | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| THOR-F-B508 | FILTER 2 slope button 5 | Filter 2 ladder slope selector 5 | — | — | click only | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| THOR-F-K501 | FILTER 2 FREQ | Filter 2 frequency | Filter 2 Freq | 26 / CC 55 | voice/MIDI or click | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Freq: 1.56 kHz" |
| THOR-F-K502 | FILTER 2 RES | Filter 2 resonance | Filter 2 Res | 27 / CC 56 | voice/MIDI or click | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Res: 77" |
| THOR-F-S501 | FILTER 2 DRIVE | Filter 2 drive | Filter 2 Drive | — | display/Remote item, not mapped | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Drive: 64" |
| THOR-F-B507 | FILTER 2 INV | Filter 2 envelope invert | Filter 2 Env Invert | — | display/Remote item, not mapped | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Env Invert" |
| THOR-F-K503 | FILTER 2 ENV | Filter 2 envelope amount | Filter 2 Env Amount | 28 / CC 57 | voice/MIDI or click | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Env Amount: 33" |
| THOR-F-K504 | FILTER 2 VEL | Filter 2 velocity | Filter 2 Velocity | — | display/Remote item, not mapped | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Velocity: 47" |
| THOR-F-K505 | FILTER 2 KBD | Filter 2 keyboard tracking | Filter 2 Kbd | — | display/Remote item, not mapped | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Kbd: 0" |
| THOR-F-B509 | FILTER 2 slope selector | Filter 2 ladder slope | — | — | click only | [Filter 2 switched on (Low Pass Ladder; default patch has Bypass) (picture thor-filter2-view_front_labeled.png)] tooltip "Filter 2 Ladder Slope" |

## Thor Polysonic Synthesizer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| THOR-B-J01 | Mono Gate In | Gate input (mono) | — | — | cable: right-click jack > device > jack name | tooltip "Mono Gate Input" |
| THOR-B-J09 | Mono CV In | CV input (mono pitch) | — | — | cable: right-click jack > device > jack name | tooltip "Mono CV Input" |
| THOR-B-K01 | Pitch Bend trim | Amount for pitch bend CV | — | — | click/drag only (no Remote item) | tooltip "Pitch Wheel Modulation Input: 127" |
| THOR-B-J02 | Pitch Bend CV In | CV input: pitch bend | — | — | cable: right-click jack > device > jack name | tooltip "Pitch Wheel Modulation Input" |
| THOR-B-K03 | Mod Wheel trim | Amount for mod wheel CV | — | — | click/drag only (no Remote item) | tooltip "Mod Wheel Modulation Input: 127" |
| THOR-B-J10 | Mod Wheel CV In | CV input: mod wheel | — | — | cable: right-click jack > device > jack name | tooltip "Mod Wheel Modulation Input" |
| THOR-B-K02 | Rotary 1 trim | Amount for the Rotary 1 CV input | — | — | click/drag only (no Remote item) | tooltip "Rotary 1: 127" |
| THOR-B-J03 | Rotary 1 CV In | CV input for Rotary 1 | — | — | cable: right-click jack > device > jack name | tooltip "Rotary 1" |
| THOR-B-J04 | Mod Input CV 1 | Modulation input CV 1 (assignable modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 1" |
| THOR-B-K04 | Rotary 2 trim | Amount for the Rotary 2 CV input | — | — | click/drag only (no Remote item) | tooltip "Rotary 2: 127" |
| THOR-B-J11 | Rotary 2 CV In | CV input for Rotary 2 | — | — | cable: right-click jack > device > jack name | tooltip "Rotary 2" |
| THOR-B-J12 | Mod Input CV 2 | Modulation input CV 2 (assignable modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 2" |
| THOR-B-K05 | Filter Freq trim | Amount for the Filter Freq CV input | — | — | click/drag only (no Remote item) | tooltip "Filter 1 Param X: 127" |
| THOR-B-J17 | Filter Freq CV In | CV input for Filter Freq | — | — | cable: right-click jack > device > jack name | tooltip "Filter 1 Param X" |
| THOR-B-J19 | Mod Input CV 3 | Modulation input CV 3 (assignable modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 3" |
| THOR-B-K06 | Amp Level trim | Amount for the Amp Level CV input | — | — | click/drag only (no Remote item) | tooltip "Level: 127" |
| THOR-B-J18 | Amp Level CV In | CV input for Amp Level | — | — | cable: right-click jack > device > jack name | tooltip "Level" |
| THOR-B-J20 | Mod Input CV 4 | Modulation input CV 4 (assignable modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 4" |
| THOR-B-J05 | Global Envelope Out | Global envelope CV output | — | — | cable: right-click jack > device > jack name | tooltip "Global Envelope" |
| THOR-B-J13 | LFO 2 Out | LFO 2 CV output | — | — | cable: right-click jack > device > jack name | tooltip "LFO 2" |
| THOR-B-J06 | Mod Output CV 1 | Modulation output CV 1 | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 1" |
| THOR-B-J14 | Mod Output CV 2 | Modulation output CV 2 | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 2" |
| THOR-B-J21 | Mod Output CV 3 | Modulation output CV 3 | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 3" |
| THOR-B-J24 | Mod Output CV 4 | Modulation output CV 4 | — | — | cable: right-click jack > device > jack name | tooltip "Modulator 4" |
| THOR-B-J07 | Audio In 1 | Audio input 1 | — | — | cable: right-click jack > device > jack name | tooltip "In 1" |
| THOR-B-J15 | Audio In 2 | Audio input 2 | — | — | cable: right-click jack > device > jack name | tooltip "In 2" |
| THOR-B-J22 | Audio In 3 | Audio input 3 | — | — | cable: right-click jack > device > jack name | tooltip "In 3" |
| THOR-B-J25 | Audio In 4 | Audio input 4 | — | — | cable: right-click jack > device > jack name | tooltip "In 4" |
| THOR-B-J08 | Audio Out 1 | Audio output 1 | — | — | cable: right-click jack > device > jack name | tooltip "Out 1 Left" |
| THOR-B-J16 | Audio Out 2 | Audio output 2 | — | — | cable: right-click jack > device > jack name | tooltip "Out 2 Right" |
| THOR-B-J23 | Audio Out 3 | Audio output 3 | — | — | cable: right-click jack > device > jack name | tooltip "Out 3" |
| THOR-B-J26 | Audio Out 4 | Audio output 4 | — | — | cable: right-click jack > device > jack name | tooltip "Out 4" |
| THOR-B-J27 | Seq Gate In | Step sequencer trigger input | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Trig" |
| THOR-B-K07 | Seq Rate trim | Amount for step sequencer rate CV | — | — | click/drag only (no Remote item) | tooltip "Step Sequencer Rate: 127" |
| THOR-B-J28 | Seq Rate In | Step sequencer rate CV input | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Rate" |
| THOR-B-K09 | Seq Pitch trim | Amount for step sequencer transpose CV | — | — | click/drag only (no Remote item) | tooltip "Step Sequencer Transpose: 127" |
| THOR-B-J33 | Seq Pitch In | Step sequencer pitch/transpose CV input | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Transpose" |
| THOR-B-K08 | Seq Gate Length trim | Amount for step sequencer gate length CV | — | — | click/drag only (no Remote item) | tooltip "Step Sequencer Gate Length: 127" |
| THOR-B-J29 | Seq Gate Length In | Step sequencer gate length CV input | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Gate Length" |
| THOR-B-K10 | Seq Velocity trim | Amount for step sequencer velocity CV | — | — | click/drag only (no Remote item) | tooltip "Step Sequencer Velocity: 127" |
| THOR-B-J34 | Seq Velocity In | Step sequencer velocity CV input | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Velocity" |
| THOR-B-J30 | Seq Note Out | Step sequencer note CV output | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Note" |
| THOR-B-J31 | Seq Curve 1 Out | Step sequencer curve 1 CV output | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Curve 1" |
| THOR-B-J32 | Seq Start Out | Step sequencer start-of-sequence trigger output | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Start Trig" |
| THOR-B-J35 | Seq Gate Out | Step sequencer gate/velocity output | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Gate" |
| THOR-B-J36 | Seq Curve 2 Out | Step sequencer curve 2 CV output | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer Curve 2" |
| THOR-B-J37 | Seq End Out | Step sequencer end-of-sequence trigger output | — | — | cable: right-click jack > device > jack name | tooltip "Step Sequencer End Trig" |

## Grain Sample Manipulator — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| GRAN-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D01 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B02 | (patch arrows) | Previous / next patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| GRAN-F-B03 | (patch folder) | Browse patch | — | — | click only | tooltip "Browse patch" |
| GRAN-F-B04 | (patch disk) | Save patch | — | — | click only | tooltip "Save patch" |
| GRAN-F-D02 | Patch name tape | Patch name tape | Device Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D03 | VOICES display | Number of voices | — | — | click only | tooltip "Voices: 8" |
| GRAN-F-B05 | (voices arrows) | Voices down/up | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K01 | MASTER VOLUME | Master volume | Master Volume | 48 / CC 77 | voice/MIDI or click | tooltip "Master Volume: 1.5 dB" |
| GRAN-F-D04 | Sample name display | Name of the loaded sample | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B06 | (sample arrows) | Previous / next sample | — | — | click only | tooltip "Select previous sample" |
| GRAN-F-B07 | (sample folder) | Browse samples | — | — | click only | tooltip "Browse sample" |
| GRAN-F-B08 | (sample record) | Start sampling | Record Sample | — | display/Remote item, not mapped | tooltip "Start sampling" |
| GRAN-F-B09 | (sample edit pencil) | Edit sample | — | — | click only | tooltip "Edit Sample" |
| GRAN-F-D05 | Overview waveform | Whole-sample overview with the zoom window | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B10 | (preview button) | Preview the sample | — | — | click only | tooltip "Preview" |
| GRAN-F-D06 | Main waveform | Waveform display: start, end and playhead | Position | 2 / CC 31 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B11 | START marker | Sample start marker | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B12 | END marker | Sample end marker | End Pos | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-S01 | DISPLAY Y POS slider | Waveform display vertical position | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D07 | MOTION menu (Envelope 1) | Motion envelope menu | Motion | 5 / CC 34 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K02 | SPEED | Motion speed | Speed | 7 / CC 36 | voice/MIDI or click | tooltip "Speed: 34.4 %" |
| GRAN-F-K03 | JITTER | Motion jitter | Jitter | 6 / CC 35 | voice/MIDI or click | tooltip "Jitter: 0.0 %" |
| GRAN-F-B13 | GLOBAL POSITION | Global position on/off | Global Position | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D08 | ROOT KEY note | Root key note | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D09 | ROOT KEY fine tune | Root key fine tune | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B14 | SET | Set root key from analysis | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D10 | ANALYZED | Analysed pitch of the sample | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D11 | LONG GRAINS menu | Grain algorithm menu | Algorithm | 1 / CC 30 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K04 | FORMANT (other grain mode) | Formant knob: not visible in Long Grains mode | Formant | 8 / CC 37 | voice/MIDI or click | not hovered: control is not on screen in Long Grains mode |
| GRAN-F-K10 | PAN SPREAD | Grain pan spread | Pan Spread | 46 / CC 75 | voice/MIDI or click | tooltip "Pan Spread: 71.9 %" |
| GRAN-F-K13 | PITCH JITTER | Grain pitch jitter | Pitch Jitter | — | display/Remote item, not mapped | tooltip "Pitch Jitter: 0.0 %" |
| GRAN-F-D13 | Grain shape display | Grain window shape | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K14 | GRAIN LENGTH | Grain length | Grain Length | 3 / CC 32 | voice/MIDI or click | tooltip "Grain Length: 68.4 %" |
| GRAN-F-K15 | RATE | Grain rate / spacing | Rate-Spacing | 4 / CC 33 | voice/MIDI or click | tooltip "Rate-Spacing: 48.4 %" |
| GRAN-F-K16 | X-FADE | Grain crossfade | XFade | — | display/Remote item, not mapped | tooltip "X-Fade: 78.1 %" |
| GRAN-F-K05 | PITCH OCT | Pitch octave | Oct | 10 / CC 39 | voice/MIDI or click | tooltip "Oct: 2" |
| GRAN-F-K06 | PITCH SEMI | Pitch semitone | Semi | 11 / CC 40 | voice/MIDI or click | tooltip "Semi: 0" |
| GRAN-F-K07 | PITCH TUNE | Pitch fine tune | Tune | 12 / CC 41 | voice/MIDI or click | tooltip "Tune: 0" |
| GRAN-F-K08 | PITCH KBD | Pitch keyboard tracking | Pitch Kbd | — | display/Remote item, not mapped | tooltip "Pitch Kbd: 100.0 %" |
| GRAN-F-K09 | SAMPLE LEVEL | Sample level | Sample Level | 9 / CC 38 | voice/MIDI or click | tooltip "Sample Level: -8.3 dB" |
| GRAN-F-B15 | SAMPLE to FILTER (upper) | Route sample to filter | Sample To Filter | — | display/Remote item, not mapped | tooltip "Sample To Filter" |
| GRAN-F-B16 | SAMPLE to FILTER (lower) | Route sample to filter (second button of the pair) | Sample To Filter | — | display/Remote item, not mapped | tooltip "Sample To Filter" |
| GRAN-F-B17 | OSCILLATOR on | Oscillator on/off | Osc On | 13 / CC 42 | voice/MIDI or click | tooltip "Osc On" |
| GRAN-F-K17 | OSC OCT | Oscillator octave | Osc Oct | — | display/Remote item, not mapped | tooltip "Osc Oct: 0" |
| GRAN-F-D14 | OSC WAVEFORM display | Oscillator waveform | Osc Wave | 14 / CC 43 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B18 | (osc waveform arrows) | Oscillator waveform prev/next | — | — | click only | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K18 | OSC MOD | Oscillator mod amount | Osc Mod | — | display/Remote item, not mapped | tooltip "Osc Mod: 0.0 %" |
| GRAN-F-K19 | OSC LEVEL | Oscillator level | Osc Level | 15 / CC 44 | voice/MIDI or click | tooltip "Osc Level: -13.9 dB" |
| GRAN-F-B19 | OSC to FILTER (upper) | Route oscillator to filter | Osc To Filter | — | display/Remote item, not mapped | tooltip "Osc To Filter" |
| GRAN-F-B20 | OSC to FILTER (lower) | Route oscillator to filter (second button) | Osc To Filter | — | display/Remote item, not mapped | tooltip "Osc To Filter" |
| GRAN-F-D12 | FILTER type menu (LP 12dB) | Filter type menu | Filter Type | 16 / CC 45 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K11 | FILTER FREQ | Filter frequency | Filter Freq | 17 / CC 46 | voice/MIDI or click | tooltip "Filter Freq: 401.7 Hz" |
| GRAN-F-K12 | FILTER RESO | Filter resonance | Filter Reso | 18 / CC 47 | voice/MIDI or click | tooltip "Filter Reso: 12.5 %" |
| GRAN-F-K20 | FILTER ENV 2 | Filter envelope 2 amount | Filter Env2 | 19 / CC 48 | voice/MIDI or click | tooltip "Filter Env2: 57.8 %" |
| GRAN-F-K21 | FILTER VEL | Filter velocity | Filter Vel | — | display/Remote item, not mapped | tooltip "Filter Velocity: 15.6 %" |
| GRAN-F-K22 | FILTER KBD | Filter keyboard tracking | Filter Kbd | 20 / CC 49 | voice/MIDI or click | tooltip "Filter Kbd: 37.5 %" |
| GRAN-F-S02 | AMP A | Amp attack | Amp Attack | 21 / CC 50 | voice/MIDI or click | tooltip "Amp Attack: 0.6 ms" |
| GRAN-F-S03 | AMP D | Amp decay | Amp Decay | 22 / CC 51 | voice/MIDI or click | tooltip "Amp Decay: 6.95 s" |
| GRAN-F-S04 | AMP S | Amp sustain | Amp Sustain | 23 / CC 52 | voice/MIDI or click | no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-S05 | AMP R | Amp release | Amp Release | 24 / CC 53 | voice/MIDI or click | tooltip "Amp Release: 2.50 s" |
| GRAN-F-K23 | AMP GAIN | Amp gain | Amp Gain | 25 / CC 54 | voice/MIDI or click | tooltip "Amp Gain: 0.2 dB" |
| GRAN-F-K24 | AMP VEL | Amp velocity | — | — | click only | tooltip "Amp Velocity: 0.0 %" |
| GRAN-F-K25 | AMP PAN | Amp pan | — | — | click only | tooltip "Pan: 50.0 %" |
| GRAN-F-S301 | DIST type slider | Distortion type | — | — | click only | [Effects: DIST tab (picture grain-fxdist-view_front_labeled.png)] tooltip "Dist Type: Dist" |
| GRAN-F-K301 | DIST DRIVE | Distortion drive | Dist Drive | 30 / CC 59 | voice/MIDI or click | [Effects: DIST tab (picture grain-fxdist-view_front_labeled.png)] tooltip "Dist Drive: 50.0 %" |
| GRAN-F-K302 | DIST TONE | Distortion tone | Dist Tone | 31 / CC 60 | voice/MIDI or click | [Effects: DIST tab (picture grain-fxdist-view_front_labeled.png)] tooltip "Dist Tone: 80.0 %" |
| GRAN-F-K303 | DIST AMOUNT | Distortion amount | Dist Amount | 29 / CC 58 | voice/MIDI or click | [Effects: DIST tab (picture grain-fxdist-view_front_labeled.png)] tooltip "Dist Amount: 100.0 %" |
| GRAN-F-B501 | DELAY SYNC | Delay tempo sync | Delay Sync | — | display/Remote item, not mapped | [Effects: DLY tab (picture grain-fxdly-view_front_labeled.png)] tooltip "Delay Sync: On" |
| GRAN-F-S501 | DELAY TIME | Delay time (synced time when SYNC is on) | Delay Time | 37 / CC 66 | voice/MIDI or click | [Effects: DLY tab (picture grain-fxdly-view_front_labeled.png)] tooltip "Delay Synced Time: 3/16" |
| GRAN-F-B502 | DELAY PING PONG | Delay ping pong | Delay PingPong | — | display/Remote item, not mapped | [Effects: DLY tab (picture grain-fxdly-view_front_labeled.png)] tooltip "Delay PingPong: On" |
| GRAN-F-K501 | DELAY PAN | Delay pan | Delay Pan | — | display/Remote item, not mapped | [Effects: DLY tab (picture grain-fxdly-view_front_labeled.png)] tooltip "Delay Pan: 100.0 %" |
| GRAN-F-K502 | DELAY FB | Delay feedback | Delay FB | 38 / CC 67 | voice/MIDI or click | [Effects: DLY tab (picture grain-fxdly-view_front_labeled.png)] tooltip "Delay Feedback: 17.2 %" |
| GRAN-F-K503 | DELAY AMOUNT | Delay amount | Delay Amount | 36 / CC 65 | voice/MIDI or click | [Effects: DLY tab (picture grain-fxdly-view_front_labeled.png)] tooltip "Delay Amount: 27.2 %" |
| GRAN-F-K401 | EQ FREQ | EQ frequency | EQ Freq | — | display/Remote item, not mapped | [Effects: EQ tab (picture grain-fxeq-view_front_labeled.png)] tooltip "EQ Freq: 104.1 Hz" |
| GRAN-F-K402 | EQ Q | EQ Q | EQ Q | — | display/Remote item, not mapped | [Effects: EQ tab (picture grain-fxeq-view_front_labeled.png)] tooltip "EQ Q: 16.2 %" |
| GRAN-F-K403 | EQ GAIN | EQ gain | EQ Gain | — | display/Remote item, not mapped | [Effects: EQ tab (picture grain-fxeq-view_front_labeled.png)] tooltip "EQ Gain: -1.1 dB" |
| GRAN-F-S201 | MOD FX type slider | Modulation effect type (chorus/flanger/phaser) | Mod Effect Type | 43 / CC 72 | voice/MIDI or click | [Effects: PHSR (modulation FX) tab (picture grain-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Type: Phaser" |
| GRAN-F-K201 | MOD FX DEPTH | Modulation effect depth | Mod Effect Depth | — | display/Remote item, not mapped | [Effects: PHSR (modulation FX) tab (picture grain-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Depth: 80.0 %" |
| GRAN-F-K202 | MOD FX RATE | Modulation effect rate | Mod Effect Rate | 45 / CC 74 | voice/MIDI or click | [Effects: PHSR (modulation FX) tab (picture grain-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Rate: 0.20 Hz" |
| GRAN-F-K204 | MOD FX SPREAD | Modulation effect spread | Mod Effect Spread | — | display/Remote item, not mapped | [Effects: PHSR (modulation FX) tab (picture grain-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Spread: 25.0 %" |
| GRAN-F-K203 | MOD FX AMOUNT | Modulation effect amount | Mod Effect Amount | 44 / CC 73 | voice/MIDI or click | [Effects: PHSR (modulation FX) tab (picture grain-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Amount: 60.0 %" |
| GRAN-F-S601 | REVERB DECAY | Reverb decay | Reverb Decay | 41 / CC 70 | voice/MIDI or click | [Effects: REV tab (picture grain-fxrev-view_front_labeled.png)] tooltip "Reverb Decay: 67.7 %" |
| GRAN-F-K601 | REVERB SIZE | Reverb size | Reverb Size | 42 / CC 71 | voice/MIDI or click | [Effects: REV tab (picture grain-fxrev-view_front_labeled.png)] tooltip "Reverb Size: 70.0 %" |
| GRAN-F-K602 | REVERB DAMP | Reverb damp | Reverb Damp | — | display/Remote item, not mapped | [Effects: REV tab (picture grain-fxrev-view_front_labeled.png)] tooltip "Reverb Damp: 30.0 %" |
| GRAN-F-K603 | REVERB AMOUNT | Reverb amount | Reverb Amount | 40 / CC 69 | voice/MIDI or click | [Effects: REV tab (picture grain-fxrev-view_front_labeled.png)] tooltip "Reverb Amount: 36.6 %" |
| GRAN-F-B108 | KEY MODE switch | Key mode (POLY/RETRIG/LEGATO) | Key Mode | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Key Mode: Poly" |
| GRAN-F-B112 | PORTA switch (OFF/ON/AUTO) | Portamento mode | Portamento Mode | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Portamento Mode: Off" |
| GRAN-F-K104 | PORTA TIME | Portamento time | Portamento | 47 / CC 76 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Portamento: 25.0 %" |
| GRAN-F-B101 | ENVELOPE tab 1 (Motion) | Select envelope 1 | Env Select | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B102 | ENVELOPE tab 2 (Filter) | Select envelope 2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B103 | ENVELOPE tab 3 | Select envelope 3 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B104 | ENVELOPE tab 4 | Select envelope 4 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D102 | Envelope display | Envelope editor | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B109 | PRESET | Envelope preset | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B116 | EDIT Y-POS | Edit envelope y position | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B110 | SUSTAIN | Envelope sustain | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B113 | LOOP | Envelope loop | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B119 | KEY TRIG | Envelope key trigger | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B105 | LFO tab 1 | Select LFO 1 | LFO Select | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B106 | LFO tab 2 | Select LFO 2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B107 | LFO tab 3 | Select LFO 3 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D101 | LFO WAVEFORM display | LFO waveform | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B111 | (LFO waveform arrows) | LFO waveform prev/next | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K101 | LFO 1 RATE | LFO 1 rate | LFO 1 Rate | 26 / CC 55 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B114 | LFO 1 BEAT SYNC | LFO 1 tempo sync | LFO 1 TempoSync | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B117 | LFO 1 BIPOLAR | LFO 1 bipolar | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B120 | LFO 1 GLOBAL | LFO 1 global | LFO 1 Global | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K102 | LFO 2 RATE | LFO 2 rate | LFO 2 Rate | 27 / CC 56 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B115 | LFO 2 BEAT SYNC | LFO 2 tempo sync | LFO 2 TempoSync | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B118 | LFO 2 KEY SYNC | LFO 2 key sync | LFO 2 KeySync | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B121 | LFO 2 GLOBAL | LFO 2 global | LFO 2 Global | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K103 | LFO DELAY | LFO delay | LFO 1 Delay | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D103 | P.RANGE | Pitch bend range | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Pitchbend Range: 2" |
| GRAN-F-S101 | PITCH wheel | Pitch bend wheel | Pitch Bend | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "(Pitch Bend): 0.0%" |
| GRAN-F-S102 | MOD wheel | Mod wheel | Mod Wheel | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "(Mod Wheel): 0%" |
| GRAN-F-D104 | MOD 1 src | Modulation matrix row 1: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K105 | MOD 1 k1 | Modulation matrix row 1: k1 | Mod1 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Mod1 Dest1 Amt: 0" |
| GRAN-F-D105 | MOD 1 dest1 | Modulation matrix row 1: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K106 | MOD 1 k2 | Modulation matrix row 1: k2 | Mod1 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Mod1 Dest2 Amt: 0" |
| GRAN-F-D106 | MOD 1 dest2 | Modulation matrix row 1: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K107 | MOD 1 k3 | Modulation matrix row 1: k3 | Mod1 Scale Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Mod1 Scale Amt: 0" |
| GRAN-F-D107 | MOD 1 scale | Modulation matrix row 1: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B128 | MOD 1 clr | Modulation matrix row 1: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-D108 | MOD 2 src | Modulation matrix row 2: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K108 | MOD 2 k1 | Modulation matrix row 2: k1 | Mod2 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D110 | MOD 2 dest1 | Modulation matrix row 2: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K110 | MOD 2 k2 | Modulation matrix row 2: k2 | Mod2 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D112 | MOD 2 dest2 | Modulation matrix row 2: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K112 | MOD 2 k3 | Modulation matrix row 2: k3 | Mod2 Scale Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D114 | MOD 2 scale | Modulation matrix row 2: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B136 | MOD 2 clr | Modulation matrix row 2: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D109 | MOD 3 src | Modulation matrix row 3: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K109 | MOD 3 k1 | Modulation matrix row 3: k1 | Mod3 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D111 | MOD 3 dest1 | Modulation matrix row 3: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K111 | MOD 3 k2 | Modulation matrix row 3: k2 | Mod3 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D113 | MOD 3 dest2 | Modulation matrix row 3: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K113 | MOD 3 k3 | Modulation matrix row 3: k3 | Mod3 Scale Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D115 | MOD 3 scale | Modulation matrix row 3: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B137 | MOD 3 clr | Modulation matrix row 3: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D116 | MOD 4 src | Modulation matrix row 4: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K114 | MOD 4 k1 | Modulation matrix row 4: k1 | Mod4 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D117 | MOD 4 dest1 | Modulation matrix row 4: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K115 | MOD 4 k2 | Modulation matrix row 4: k2 | Mod4 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D118 | MOD 4 dest2 | Modulation matrix row 4: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K116 | MOD 4 k3 | Modulation matrix row 4: k3 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D119 | MOD 4 scale | Modulation matrix row 4: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B138 | MOD 4 clr | Modulation matrix row 4: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D120 | MOD 5 src | Modulation matrix row 5: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K119 | MOD 5 k1 | Modulation matrix row 5: k1 | Mod5 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D122 | MOD 5 dest1 | Modulation matrix row 5: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K121 | MOD 5 k2 | Modulation matrix row 5: k2 | Mod5 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D124 | MOD 5 dest2 | Modulation matrix row 5: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K123 | MOD 5 k3 | Modulation matrix row 5: k3 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D126 | MOD 5 scale | Modulation matrix row 5: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B139 | MOD 5 clr | Modulation matrix row 5: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D121 | MOD 6 src | Modulation matrix row 6: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K120 | MOD 6 k1 | Modulation matrix row 6: k1 | Mod6 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D123 | MOD 6 dest1 | Modulation matrix row 6: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K122 | MOD 6 k2 | Modulation matrix row 6: k2 | Mod6 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D125 | MOD 6 dest2 | Modulation matrix row 6: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K124 | MOD 6 k3 | Modulation matrix row 6: k3 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D127 | MOD 6 scale | Modulation matrix row 6: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B140 | MOD 6 clr | Modulation matrix row 6: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D128 | MOD 7 src | Modulation matrix row 7: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K125 | MOD 7 k1 | Modulation matrix row 7: k1 | Mod7 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D129 | MOD 7 dest1 | Modulation matrix row 7: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K126 | MOD 7 k2 | Modulation matrix row 7: k2 | Mod7 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D130 | MOD 7 dest2 | Modulation matrix row 7: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K127 | MOD 7 k3 | Modulation matrix row 7: k3 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D131 | MOD 7 scale | Modulation matrix row 7: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B141 | MOD 7 clr | Modulation matrix row 7: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D132 | MOD 8 src | Modulation matrix row 8: src | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K130 | MOD 8 k1 | Modulation matrix row 8: k1 | Mod8 Dest1 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D133 | MOD 8 dest1 | Modulation matrix row 8: dest1 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K131 | MOD 8 k2 | Modulation matrix row 8: k2 | Mod8 Dest2 Amt | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D134 | MOD 8 dest2 | Modulation matrix row 8: dest2 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-K132 | MOD 8 k3 | Modulation matrix row 8: k3 | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-D135 | MOD 8 scale | Modulation matrix row 8: scale | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B142 | MOD 8 clr | Modulation matrix row 8: clr | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] not hovered; same column/row pattern as the hovered row 1 (name inferred from table order) |
| GRAN-F-B129 | EFFECTS power | Effects section on/off | Effect On | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s); the upper light (753,286) showed tooltip "Effects On" |
| GRAN-F-B122 | PHSR tab | Show the PHSR panel | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B130 | PHSR ON/OFF | PHSR effect on/off | Phaser On | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B123 | DIST tab | Show the DIST panel | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B131 | DIST ON/OFF | DIST effect on/off | Dist On | 28 / CC 57 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B124 | EQ tab | Show the EQ panel | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B132 | EQ ON/OFF | EQ effect on/off | EQ On | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B125 | COMP tab | Show the COMP panel | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B133 | COMP ON/OFF | COMP effect on/off | Comp On | 32 / CC 61 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B126 | DLY tab | Show the DLY panel | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B134 | DLY ON/OFF | DLY effect on/off | Delay On | 35 / CC 64 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B127 | REV tab | Show the REV panel | — | — | click only | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-B135 | REV ON/OFF | REV effect on/off | Reverb On | 39 / CC 68 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.2 s) |
| GRAN-F-K117 | COMP ATTACK | Compressor attack | Comp Attack | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Comp Attack: 7.6 ms" |
| GRAN-F-K118 | COMP THRES | Compressor threshold | Comp Threshold | 33 / CC 62 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Comp Threshold: -12.0 dB" |
| GRAN-F-K128 | COMP RELEASE | Compressor release | Comp Release | — | display/Remote item, not mapped | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Comp Release: 636 ms" |
| GRAN-F-K129 | COMP RATIO | Compressor ratio | Comp Ratio | 34 / CC 63 | voice/MIDI or click | [Lower half: envelopes, LFOs, modulation matrix, effects row (scrolled down) (picture grain-lower-view_front_labeled.png)] tooltip "Comp Ratio: 2.00 : 1" |

## Grain Sample Manipulator — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| GRAN-B-J01 | Seq Gate In | Gate input (sequencer) | — | — | cable: right-click jack > device > jack name | tooltip "Seq Gate Input" |
| GRAN-B-J05 | Seq Note In | Note CV input (sequencer) | — | — | cable: right-click jack > device > jack name | tooltip "Seq Note Input" |
| GRAN-B-K01 | Pitch Bend CV trim | Amount for pitch bend CV | — | — | click/drag only (no Remote item) | tooltip "PitchBend CV Amount: 100.0 %" |
| GRAN-B-J02 | Pitch Bend CV In | CV input: pitch bend | — | — | cable: right-click jack > device > jack name | tooltip "Pitch Bend CV Input" |
| GRAN-B-K02 | Mod Wheel CV trim | Amount for mod wheel CV | — | — | click/drag only (no Remote item) | tooltip "ModWheel CV Amount: 100.0 %" |
| GRAN-B-J06 | Mod Wheel CV In | CV input: mod wheel | — | — | cable: right-click jack > device > jack name | tooltip "Mod Wheel CV Input" |
| GRAN-B-J03 | CV In 1 | CV input 1 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 1" |
| GRAN-B-J07 | CV In 2 | CV input 2 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 2" |
| GRAN-B-J09 | CV In 3 | CV input 3 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 3" |
| GRAN-B-J11 | CV In 4 | CV input 4 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 4" |
| GRAN-B-J04 | CV Out 1 | CV output 1 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 1" |
| GRAN-B-J08 | CV Out 2 | CV output 2 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 2" |
| GRAN-B-J10 | CV Out 3 | CV output 3 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 3" |
| GRAN-B-J12 | CV Out 4 | CV output 4 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 4" |
| GRAN-B-J13 | Audio Out L | Audio output, left | — | — | cable: right-click jack > device > jack name | tooltip "Left Output" |
| GRAN-B-J14 | Audio Out R | Audio output, right | — | — | cable: right-click jack > device > jack name | tooltip "Right Output" |

## Europa Shapeshifting Synthesizer — front
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| EURO-F-B01 | (triangle) | Fold/unfold device | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D01 | Patch name tape | Patch name tape | Device Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D02 | Patch display | Patch name display | Patch Name | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B02 | (patch arrows) | Previous / next patch | Select Previous Patch | — | display/Remote item, not mapped | tooltip "Select previous patch" |
| EURO-F-B03 | (patch folder) | Browse patch | — | — | click only | tooltip "Browse patch" |
| EURO-F-B04 | (patch disk) | Save patch | — | — | click only | tooltip "Save patch" |
| EURO-F-B10 | ENGINE I select | Select engine 1 for editing | OscSel | — | display/Remote item, not mapped | tooltip "Engine Select" |
| EURO-F-B12 | ENGINE II select | Select engine 2 for editing | — | — | click only | tooltip "Engine Select" |
| EURO-F-B19 | ENGINE III select | Select engine 3 for editing | — | — | click only | tooltip "Engine Select" |
| EURO-F-B09 | ENGINE I ON | Engine 1 on/off | Osc1 On | — | display/Remote item, not mapped | tooltip "Eng1 On" |
| EURO-F-B16 | ENGINE II ON | Engine 2 on/off | Osc2 On | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B18 | ENGINE III ON | Engine 3 on/off | Osc3 On | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B11 | (engine 1 arrow) | Engine 1 arrow (send engine to the filter section) | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B17 | (engine 2 arrow) | Engine 2 arrow (send engine to the filter section) | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B20 | (engine 3 arrow) | Engine 3 arrow (send engine to the filter section) | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B05 | WAVE ON | Wave section on/off (engine I) | Osc1 On | 1 / CC 30 | voice/MIDI or click | tooltip "Eng1 On" |
| EURO-F-D04 | WAVE display | Wave shape display | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D09 | WAVE menu (Basic Analog) | Wave type menu | Osc1 Wave | 2 / CC 31 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B13 | (wave arrows) | Wave previous/next | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K01 | OCT | Engine I octave | — | — | click only | tooltip "Eng1 Oct: 2" |
| EURO-F-K06 | SEMI | Engine I semitone | Osc1 Semi | 3 / CC 32 | voice/MIDI or click | tooltip "Eng1 Semi: 0" |
| EURO-F-K08 | TUNE | Engine I fine tune | — | — | click only | tooltip "Eng1 Tune: 0" |
| EURO-F-K20 | KBD | Engine I pitch keyboard tracking | — | — | click only | tooltip "Eng1 Pitch Kbd: 100.0 %" |
| EURO-F-K09 | SHAPE | Wave shape amount | Osc1 Shape | — | display/Remote item, not mapped | tooltip "Eng1 Shape: 50.0 %" |
| EURO-F-K10 | SHAPE mod amount | Shape modulation amount | Osc1 Shape Amt | 6 / CC 35 | voice/MIDI or click | tooltip "Eng1 Shape Amt: 0.0 %" |
| EURO-F-D11 | SHAPE mod source (LFO 1) | Shape modulation source | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K13 | SHAPE VELO | Shape velocity amount | Osc1 Shape Vel | — | display/Remote item, not mapped | tooltip "Eng1 Shape Vel: 0.0 %" |
| EURO-F-B21 | PHASE SYNC | Phase sync on/off | — | — | click only | tooltip "Eng1 SyncPhase" |
| EURO-F-B06 | MODIFIER 1 ON | Modifier 1 on/off | Osc1 Mod1 On | — | display/Remote item, not mapped | tooltip "Eng1 Mod1 On" |
| EURO-F-D03 | MODIFIER 1 menu | Modifier 1 type menu | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K04 | MODIFIER 1 AMOUNT | Modifier 1 amount | Osc1 Mod1 Amt | — | display/Remote item, not mapped | tooltip "Eng1 Mod1 Amt: 46.9 %" |
| EURO-F-K05 | MODIFIER 1 mod amount | Modifier 1 modulation amount | Osc1 Mod1 Mod | — | display/Remote item, not mapped | tooltip "Eng1 Mod1 Mod: 0.0 %" |
| EURO-F-D07 | MODIFIER 1 mod source | Modifier 1 modulation source | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B14 | MODIFIER 2 ON | Modifier 2 on/off | Osc1 Mod2 On | — | display/Remote item, not mapped | tooltip "Eng1 Mod2 On" |
| EURO-F-D12 | MODIFIER 2 menu | Modifier 2 type menu | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K14 | MODIFIER 2 AMOUNT | Modifier 2 amount | Osc1 Mod2 Amt | — | display/Remote item, not mapped | tooltip "Eng1 Mod2 Amt: 0.0 %" |
| EURO-F-K15 | MODIFIER 2 mod amount | Modifier 2 modulation amount | Osc1 Mod2 Mod | — | display/Remote item, not mapped | tooltip "Eng1 Mod2 Mod: 0.0 %" |
| EURO-F-D14 | MODIFIER 2 mod source | Modifier 2 modulation source | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B07 | SPECTRAL FILTER ON | Spectral filter on/off | Osc1 Filter On | — | display/Remote item, not mapped | tooltip "Eng1 Filter On" |
| EURO-F-D05 | SPECTRAL FILTER display | Spectral filter display | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D10 | SPECTRAL FILTER menu (HP 24) | Spectral filter type menu | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K02 | SPECTRAL FILTER FREQ | Spectral filter frequency | Osc1 Filter Freq | — | display/Remote item, not mapped | tooltip "Eng1 Filter Freq: 23.4 %" |
| EURO-F-K03 | SPECTRAL FILTER RESO | Spectral filter resonance | Osc1 Filter Reso | — | display/Remote item, not mapped | tooltip "Eng1 Filter Reso: 0.0 %" |
| EURO-F-K11 | SPECTRAL FILTER KBD | Spectral filter keyboard tracking | — | — | click only | tooltip "Eng1 Filter Kbd: 100.0 %" |
| EURO-F-K18 | SPECTRAL FILTER ENV mod amount | Spectral filter modulation amount | Osc1 Filter Mod | — | display/Remote item, not mapped | tooltip "Eng1 Filter Mod: 0.0 %" |
| EURO-F-D15 | SPECTRAL FILTER mod source (ENV 1) | Spectral filter modulation source | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K21 | SPECTRAL FILTER VELO | Spectral filter velocity amount | — | — | click only | tooltip "Eng1 Filter Vel: 0.0 %" |
| EURO-F-B15 | HARMONICS ON | Harmonics on/off | Osc1 Harm On | — | display/Remote item, not mapped | tooltip "Eng1 Harm On" |
| EURO-F-D13 | HARMONICS menu (Random Gain) | Harmonics type menu | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K16 | HARMONICS POS | Harmonics position | Osc1 Harm Pos | — | display/Remote item, not mapped | tooltip "Eng1 Harm Pos: 50.0 %" |
| EURO-F-K17 | HARMONICS AMOUNT | Harmonics amount | Osc1 Harm Amt | — | display/Remote item, not mapped | tooltip "Eng1 Harm Amt: 28.1 %" |
| EURO-F-B08 | UNISON ON | Unison on/off | Osc1 Unison On | 8 / CC 37 | voice/MIDI or click | tooltip "Eng1 Unison On" |
| EURO-F-D06 | UNISON display | Unison display | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D08 | UNISON menu (Normal) | Unison mode menu | Osc1 Unison Mode | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K07 | UNISON COUNT | Unison voice count | — | — | click only | tooltip "Eng1 Count: 2" |
| EURO-F-K12 | UNISON BLEND | Unison blend | Osc1 Blend | — | display/Remote item, not mapped | tooltip "Eng1 Blend: 100.0 %" |
| EURO-F-K19 | UNISON DETUNE | Unison detune | Osc1 Detune | 4 / CC 33 | voice/MIDI or click | tooltip "Eng1 Detune: 67.2 %" |
| EURO-F-K22 | UNISON SPREAD | Unison spread | Osc1 Spread | 7 / CC 36 | voice/MIDI or click | tooltip "Eng1 Spread: 100.0 %" |
| EURO-F-D16 | USER WAVE name display | Name of the user wave | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B22 | (user wave arrows) | Previous / next user wave | — | — | click only | tooltip "Select previous sample" |
| EURO-F-B23 | (user wave folder) | Browse user waves | — | — | click only | tooltip "Browse sample" |
| EURO-F-B24 | (user wave sample) | Start sampling a user wave | — | — | click only | tooltip "Start sampling" |
| EURO-F-B25 | (user wave edit) | Edit user wave | — | — | click only | tooltip "Edit Sample" |
| EURO-F-S01 | LEVEL slider I | Engine 1 level | Osc1 Level | 5 / CC 34 | voice/MIDI or click | tooltip "Eng1 Level: -7.0 dB" |
| EURO-F-K24 | PAN I | Engine 1 pan | — | — | click only | tooltip "Eng1 Pan: 50.0 %" |
| EURO-F-B26 | ENGINE I to FILTER | Send engine 1 to the filter | Osc1 To Filter | — | display/Remote item, not mapped | tooltip "Eng1 To Filter" |
| EURO-F-S04 | LEVEL slider II | Engine 2 level | Osc2 Level | 13 / CC 42 | voice/MIDI or click | tooltip "Eng2 Level: 15.6 dB" |
| EURO-F-K27 | PAN II | Engine 2 pan | — | — | click only | tooltip "Eng2 Pan: 50.0 %" |
| EURO-F-B28 | ENGINE II to FILTER | Send engine 2 to the filter | Osc2 To Filter | — | display/Remote item, not mapped | tooltip "Eng2 To Filter" |
| EURO-F-S07 | LEVEL slider III | Engine 3 level | Osc3 Level | 21 / CC 50 | voice/MIDI or click | tooltip "Eng3 Level: 10.8 dB" |
| EURO-F-K33 | PAN III | Engine 3 pan | — | — | click only | tooltip "Eng3 Pan: 50.0 %" |
| EURO-F-B29 | ENGINE III to FILTER | Send engine 3 to the filter | Osc3 To Filter | — | display/Remote item, not mapped | tooltip "Eng3 To Filter" |
| EURO-F-D17 | FILTER type menu (MFB LP 12dB) | Filter type menu | Filter Type | 25 / CC 54 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B27 | FILTER DRIVE on | Filter drive on/off | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K28 | FILTER DRIVE | Filter drive | Filter Drive | 28 / CC 57 | voice/MIDI or click | tooltip "Filter Drive: 15.0 %" |
| EURO-F-K29 | FILTER RESO | Filter resonance | Filter Reso | 27 / CC 56 | voice/MIDI or click | tooltip "Filter Reso: 0.0 %" |
| EURO-F-K30 | FILTER FREQ | Filter frequency | Filter Freq | 26 / CC 55 | voice/MIDI or click | tooltip "Filter Freq: 302.1 Hz" |
| EURO-F-K25 | FILTER KBD | Filter keyboard tracking | Filter Kbd | 29 / CC 58 | voice/MIDI or click | tooltip "Filter Kbd: 0.0 %" |
| EURO-F-K31 | FILTER mod amount | Filter modulation amount | Filter Mod | 30 / CC 59 | voice/MIDI or click | tooltip "Filter Mod: 81.2 %" |
| EURO-F-D18 | FILTER mod source (ENV 1) | Filter modulation source | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K34 | FILTER VELO | Filter velocity amount | — | — | click only | tooltip "Filter Velocity: 56.2 %" |
| EURO-F-K26 | AMP PAN | Amp pan | Pan | — | display/Remote item, not mapped | tooltip "Pan: 50.0 %" |
| EURO-F-K32 | AMP GAIN | Amp gain | Amp Gain | 35 / CC 64 | voice/MIDI or click | tooltip "Amp Gain: 12.3 dB" |
| EURO-F-K35 | AMP VELO | Amp velocity | Amp Velocity | 36 / CC 65 | voice/MIDI or click | tooltip "Amp Velocity: 32.8 %" |
| EURO-F-S05 | AMP A | Amp attack | Amp Attack | 31 / CC 60 | voice/MIDI or click | tooltip "Amp Attack: 0.6 ms" |
| EURO-F-S02 | AMP D | Amp decay | Amp Decay | 32 / CC 61 | voice/MIDI or click | tooltip "Amp Decay: 8.30 s" |
| EURO-F-S06 | AMP S | Amp sustain | Amp Sustain | 33 / CC 62 | voice/MIDI or click | tooltip "Amp Sustain: 0.0 %" |
| EURO-F-S03 | AMP R | Amp release | Amp Release | 34 / CC 63 | voice/MIDI or click | tooltip "Amp Release: 3.34 s" |
| EURO-F-K23 | MASTER VOLUME | Master volume | Master Volume | 48 / CC 77 | voice/MIDI or click | tooltip "Master Volume: 14.5 dB" |
| EURO-F-D19 | VOICES display | Number of voices | — | — | click only | tooltip "Voices: 16" |
| EURO-F-B30 | (voices arrows) | Voices down/up | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B31 | KEY MODE switch | Key mode (POLY/RETRIG/LEGATO) | Key Mode | — | display/Remote item, not mapped | tooltip "Key Mode: Poly" |
| EURO-F-B42 | PORTA switch (OFF/ON/AUTO) | Portamento mode | Portamento Mode | — | display/Remote item, not mapped | tooltip "Portamento Mode: Off" |
| EURO-F-K39 | PORTA TIME | Portamento time | Portamento | 47 / CC 76 | voice/MIDI or click | tooltip "Portamento: 0.0 %" |
| EURO-F-B32 | ENVELOPE tab 1 | Select envelope 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B33 | ENVELOPE tab 2 | Select envelope 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B34 | ENVELOPE tab 3 | Select envelope 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B35 | ENVELOPE tab 4 | Select envelope 4 | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B39 | PRESET | Envelope preset | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B44 | EDIT Y-POS | Edit envelope y position | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D21 | Envelope display | Envelope editor | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B40 | SUSTAIN | Envelope sustain | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B43 | LOOP | Envelope loop | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B49 | KEY TRIG | Envelope key trigger | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K36 | ENVELOPE RATE | Envelope rate (value shown as text above) | Env 2 Rate | — | display/Remote item, not mapped | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B46 | ENVELOPE BEAT SYNC | Envelope tempo sync | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B45 | ENVELOPE BIPOLAR | Envelope bipolar | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B50 | ENVELOPE GLOBAL | Envelope global | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B36 | LFO tab 1 | Select LFO 1 | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B37 | LFO tab 2 | Select LFO 2 | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B38 | LFO tab 3 | Select LFO 3 | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D20 | LFO WAVEFORM display | LFO waveform | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B41 | (LFO waveform arrows) | LFO waveform prev/next | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K37 | LFO RATE | LFO rate (value shown as text above) | LFO 1 Rate | 37 / CC 66 | voice/MIDI or click | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K38 | LFO DELAY | LFO delay | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B48 | LFO BEAT SYNC | LFO tempo sync | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B47 | LFO KEY SYNC | LFO key sync | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B51 | LFO GLOBAL | LFO global | — | — | click only | no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D22 | P.RANGE | Pitch bend range | — | — | click only | tooltip "Pitchbend Range: 2" |
| EURO-F-S08 | PITCH wheel | Pitch bend wheel | Pitch Bend | — | display/Remote item, not mapped | tooltip "(Pitch Bend): 0.0%" |
| EURO-F-S09 | MOD wheel | Mod wheel | Mod Wheel | — | display/Remote item, not mapped | tooltip "(Mod Wheel): 0%" |
| EURO-F-B801 | ENG II WAVE ON | Engine II: Wave section on/off | Osc2 On | 9 / CC 38 | voice/MIDI or click | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 On" |
| EURO-F-D802 | ENG II WAVE display | Engine II: Wave shape display | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D807 | ENG II WAVE menu | Engine II: Wave type menu | Osc2 Wave | 10 / CC 39 | voice/MIDI or click | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B805 | ENG II (wave arrows) | Engine II: Wave previous/next | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K801 | ENG II OCT | Engine II: Octave | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Oct: 1" |
| EURO-F-K806 | ENG II SEMI | Engine II: Semitone | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Semi: 0" |
| EURO-F-K808 | ENG II TUNE | Engine II: Fine tune | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Tune: 0" |
| EURO-F-K820 | ENG II KBD | Engine II: Pitch keyboard tracking | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Pitch Kbd: 10x (clipped)" |
| EURO-F-K809 | ENG II SHAPE | Engine II: Wave shape amount | Osc2 Shape | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K810 | ENG II SHAPE mod amount | Engine II: Shape modulation amount | Osc2 Shape Amt | 14 / CC 43 | voice/MIDI or click | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Shape Amt" |
| EURO-F-D809 | ENG II SHAPE mod source | Engine II: Shape modulation source | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K813 | ENG II SHAPE VELO | Engine II: Shape velocity amount | Osc2 Shape Vel | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Shape Vel: 0" |
| EURO-F-B808 | ENG II PHASE SYNC | Engine II: Phase sync on/off | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 SyncPhase" |
| EURO-F-B802 | ENG II MODIFIER 1 ON | Engine II: Modifier 1 on/off | Osc2 Mod1 On | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Mod1 On" |
| EURO-F-D801 | ENG II MODIFIER 1 menu | Engine II: Modifier 1 type menu | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K804 | ENG II MODIFIER 1 AMOUNT | Engine II: Modifier 1 amount | Osc2 Mod1 Amt | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Mod1 Amt" |
| EURO-F-K805 | ENG II MODIFIER 1 mod amount | Engine II: Modifier 1 modulation amount | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Mod1 Mod: 1x (clipped)" |
| EURO-F-D805 | ENG II MODIFIER 1 mod source | Engine II: Modifier 1 modulation source | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B806 | ENG II MODIFIER 2 ON | Engine II: Modifier 2 on/off | Osc2 Mod2 On | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Mod2 On" |
| EURO-F-D810 | ENG II MODIFIER 2 menu | Engine II: Modifier 2 type menu | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K814 | ENG II MODIFIER 2 AMOUNT | Engine II: Modifier 2 amount | Osc2 Mod2 Amt | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Mod2 Amt" |
| EURO-F-K815 | ENG II MODIFIER 2 mod amount | Engine II: Modifier 2 modulation amount | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Mod2 Mod: 0x (clipped)" |
| EURO-F-D812 | ENG II MODIFIER 2 mod source | Engine II: Modifier 2 modulation source | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B803 | ENG II SPECTRAL FILTER ON | Engine II: Spectral filter on/off | Osc2 Filter On | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Filter On" |
| EURO-F-D803 | ENG II SPECTRAL FILTER display | Engine II: Spectral filter display | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D808 | ENG II SPECTRAL FILTER menu | Engine II: Spectral filter type menu | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K802 | ENG II SPECTRAL FILTER FREQ | Engine II: Spectral filter frequency | Osc2 Filter Freq | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K803 | ENG II SPECTRAL FILTER RESO | Engine II: Spectral filter resonance | Osc2 Filter Reso | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Filter Reso: 0" |
| EURO-F-K811 | ENG II SPECTRAL FILTER KBD | Engine II: Spectral filter keyboard tracking | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Filter Kbd: 100" |
| EURO-F-K818 | ENG II SPECTRAL FILTER mod amount | Engine II: Spectral filter modulation amount | Osc2 Filter Mod | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Filter Mod: 0.0" |
| EURO-F-D813 | ENG II SPECTRAL FILTER mod source | Engine II: Spectral filter modulation source | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K821 | ENG II SPECTRAL FILTER VELO | Engine II: Spectral filter velocity amount | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Filter Vel: 0" |
| EURO-F-B807 | ENG II HARMONICS ON | Engine II: Harmonics on/off | Osc2 Harm On | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Harm On" |
| EURO-F-D811 | ENG II HARMONICS menu | Engine II: Harmonics type menu | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K816 | ENG II HARMONICS POS | Engine II: Harmonics position | Osc2 Harm Pos | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Harm Pos" |
| EURO-F-K817 | ENG II HARMONICS AMOUNT | Engine II: Harmonics amount | Osc2 Harm Amt | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Harm Amt" |
| EURO-F-B804 | ENG II UNISON ON | Engine II: Unison on/off | Osc2 Unison On | 16 / CC 45 | voice/MIDI or click | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Unison On" |
| EURO-F-D804 | ENG II UNISON display | Engine II: Unison display | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-D806 | ENG II UNISON menu | Engine II: Unison mode menu | Osc2 Unison Mode | — | display/Remote item, not mapped | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K807 | ENG II UNISON COUNT | Engine II: Unison voice count | — | — | click only | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Count: 2" |
| EURO-F-K812 | ENG II UNISON BLEND | Engine II: Unison blend | Osc2 Blend | 11 / CC 40 | voice/MIDI or click | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Blend: 100.0" |
| EURO-F-K819 | ENG II UNISON DETUNE | Engine II: Unison detune | Osc2 Detune | 12 / CC 41 | voice/MIDI or click | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Detune: 57.8" |
| EURO-F-K822 | ENG II UNISON SPREAD | Engine II: Unison spread | Osc2 Spread | 15 / CC 44 | voice/MIDI or click | [Engine II selected: its per-engine controls (picture europa-eng2-view_front_labeled.png)] tooltip "Eng2 Spread: 100.0" |
| EURO-F-B901 | ENG III WAVE ON | Engine III: Wave section on/off | Osc3 On | 17 / CC 46 | voice/MIDI or click | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 On" |
| EURO-F-D902 | ENG III WAVE display | Engine III: Wave shape display | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D907 | ENG III WAVE menu | Engine III: Wave type menu | Osc3 Wave | 18 / CC 47 | voice/MIDI or click | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B905 | ENG III (wave arrows) | Engine III: Wave previous/next | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K901 | ENG III OCT | Engine III: Octave | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K906 | ENG III SEMI | Engine III: Semitone | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 Semi: 0" |
| EURO-F-K908 | ENG III TUNE | Engine III: Fine tune | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K920 | ENG III KBD | Engine III: Pitch keyboard tracking | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K909 | ENG III SHAPE | Engine III: Wave shape amount | Osc3 Shape | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K910 | ENG III SHAPE mod amount | Engine III: Shape modulation amount | Osc3 Shape Amt | 22 / CC 51 | voice/MIDI or click | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 Shape Amt" |
| EURO-F-D909 | ENG III SHAPE mod source | Engine III: Shape modulation source | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K913 | ENG III SHAPE VELO | Engine III: Shape velocity amount | Osc3 Shape Vel | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-B908 | ENG III PHASE SYNC | Engine III: Phase sync on/off | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-B902 | ENG III MODIFIER 1 ON | Engine III: Modifier 1 on/off | Osc3 Mod1 On | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 Mod1 On" |
| EURO-F-D901 | ENG III MODIFIER 1 menu | Engine III: Modifier 1 type menu | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K904 | ENG III MODIFIER 1 AMOUNT | Engine III: Modifier 1 amount | Osc3 Mod1 Amt | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K905 | ENG III MODIFIER 1 mod amount | Engine III: Modifier 1 modulation amount | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D905 | ENG III MODIFIER 1 mod source | Engine III: Modifier 1 modulation source | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-B906 | ENG III MODIFIER 2 ON | Engine III: Modifier 2 on/off | Osc3 Mod2 On | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D910 | ENG III MODIFIER 2 menu | Engine III: Modifier 2 type menu | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K914 | ENG III MODIFIER 2 AMOUNT | Engine III: Modifier 2 amount | Osc3 Mod2 Amt | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K915 | ENG III MODIFIER 2 mod amount | Engine III: Modifier 2 modulation amount | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D912 | ENG III MODIFIER 2 mod source | Engine III: Modifier 2 modulation source | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-B903 | ENG III SPECTRAL FILTER ON | Engine III: Spectral filter on/off | Osc3 Filter On | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D903 | ENG III SPECTRAL FILTER display | Engine III: Spectral filter display | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D908 | ENG III SPECTRAL FILTER menu | Engine III: Spectral filter type menu | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K902 | ENG III SPECTRAL FILTER FREQ | Engine III: Spectral filter frequency | Osc3 Filter Freq | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-K903 | ENG III SPECTRAL FILTER RESO | Engine III: Spectral filter resonance | Osc3 Filter Reso | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K911 | ENG III SPECTRAL FILTER KBD | Engine III: Spectral filter keyboard tracking | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K918 | ENG III SPECTRAL FILTER mod amount | Engine III: Spectral filter modulation amount | Osc3 Filter Mod | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D913 | ENG III SPECTRAL FILTER mod source | Engine III: Spectral filter modulation source | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K921 | ENG III SPECTRAL FILTER VELO | Engine III: Spectral filter velocity amount | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-B907 | ENG III HARMONICS ON | Engine III: Harmonics on/off | Osc3 Harm On | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D911 | ENG III HARMONICS menu | Engine III: Harmonics type menu | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K916 | ENG III HARMONICS POS | Engine III: Harmonics position | Osc3 Harm Pos | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K917 | ENG III HARMONICS AMOUNT | Engine III: Harmonics amount | Osc3 Harm Amt | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-B904 | ENG III UNISON ON | Engine III: Unison on/off | Osc3 Unison On | 24 / CC 53 | voice/MIDI or click | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 Unison On" |
| EURO-F-D904 | ENG III UNISON display | Engine III: Unison display | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-D906 | ENG III UNISON menu | Engine III: Unison mode menu | Osc3 Unison Mode | — | display/Remote item, not mapped | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K907 | ENG III UNISON COUNT | Engine III: Unison voice count | — | — | click only | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] not hovered on engine III; same position and tooltip pattern ('Eng3 ...') as engine I and the hovered controls |
| EURO-F-K912 | ENG III UNISON BLEND | Engine III: Unison blend | Osc3 Blend | 19 / CC 48 | voice/MIDI or click | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 Blend: 100.0" |
| EURO-F-K919 | ENG III UNISON DETUNE | Engine III: Unison detune | Osc3 Detune | 20 / CC 49 | voice/MIDI or click | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 Detune: 25.0" |
| EURO-F-K922 | ENG III UNISON SPREAD | Engine III: Unison spread | Osc3 Spread | 23 / CC 52 | voice/MIDI or click | [Engine III selected: its per-engine controls (picture europa-eng3-view_front_labeled.png)] tooltip "Eng3 Spread: 100.0" |
| EURO-F-K701 | COMP ATTACK | Compressor attack | — | — | click only | [Effects: COMP tab (picture europa-fxcomp-view_front_labeled.png)] tooltip "Comp Attack: 7.6" |
| EURO-F-K702 | COMP THRES | Compressor thres | — | — | click only | [Effects: COMP tab (picture europa-fxcomp-view_front_labeled.png)] tooltip "Comp Threshold" |
| EURO-F-K703 | COMP RELEASE | Compressor release | — | — | click only | [Effects: COMP tab (picture europa-fxcomp-view_front_labeled.png)] tooltip "Comp Release: 63" |
| EURO-F-K704 | COMP RATIO | Compressor ratio | Comp Ratio | — | display/Remote item, not mapped | [Effects: COMP tab (picture europa-fxcomp-view_front_labeled.png)] tooltip "Comp Ratio: 2.00" |
| EURO-F-S301 | DIST type slider | Distortion type | — | — | click only | [Effects: DIST tab (picture europa-fxdist-view_front_labeled.png)] tooltip "Dist Type: Dist" |
| EURO-F-K301 | DIST DRIVE | Distortion drive | — | — | click only | [Effects: DIST tab (picture europa-fxdist-view_front_labeled.png)] tooltip "Dist Drive: 50.0 %" |
| EURO-F-K302 | DIST TONE | Distortion tone | — | — | click only | [Effects: DIST tab (picture europa-fxdist-view_front_labeled.png)] tooltip "Dist Tone: 80.0 %" |
| EURO-F-K303 | DIST AMOUNT | Distortion amount | Dist Amount | 39 / CC 68 | voice/MIDI or click | [Effects: DIST tab (picture europa-fxdist-view_front_labeled.png)] tooltip "Dist Amount: 100" |
| EURO-F-B501 | DELAY SYNC | Delay tempo sync | Delay Sync | — | display/Remote item, not mapped | [Effects: DLY tab (picture europa-fxdly-view_front_labeled.png)] tooltip "Delay Sync: On" |
| EURO-F-S501 | DELAY TIME | Delay time (synced time when SYNC is on) | Delay Time | 42 / CC 71 | voice/MIDI or click | [Effects: DLY tab (picture europa-fxdly-view_front_labeled.png)] tooltip "Delay (time slider handle; text clipped)" |
| EURO-F-B502 | DELAY PING PONG | Delay ping pong | Delay PingPong | — | display/Remote item, not mapped | [Effects: DLY tab (picture europa-fxdly-view_front_labeled.png)] tooltip "Delay PingPong: On" |
| EURO-F-K501 | DELAY PAN | Delay pan | Delay Pan | — | display/Remote item, not mapped | [Effects: DLY tab (picture europa-fxdly-view_front_labeled.png)] tooltip "Delay Pan: 25.0 %" |
| EURO-F-K502 | DELAY FB | Delay feedback | Delay FB | 43 / CC 72 | voice/MIDI or click | [Effects: DLY tab (picture europa-fxdly-view_front_labeled.png)] tooltip "Delay Feedback" |
| EURO-F-K503 | DELAY AMOUNT | Delay amount | Delay Amount | 41 / CC 70 | voice/MIDI or click | [Effects: DLY tab (picture europa-fxdly-view_front_labeled.png)] tooltip "Delay Amount: 25" |
| EURO-F-K401 | EQ FREQ | EQ frequency | EQ Freq | — | display/Remote item, not mapped | [Effects: EQ tab (picture europa-fxeq-view_front_labeled.png)] tooltip "EQ Freq: 12.69 kHz" |
| EURO-F-K402 | EQ Q | EQ Q | EQ Q | — | display/Remote item, not mapped | [Effects: EQ tab (picture europa-fxeq-view_front_labeled.png)] tooltip "EQ Q: 10.0 %" |
| EURO-F-K403 | EQ GAIN | EQ gain | EQ Gain | — | display/Remote item, not mapped | [Effects: EQ tab (picture europa-fxeq-view_front_labeled.png)] tooltip "EQ Gain: 5.6 dB" |
| EURO-F-S201 | MOD FX type slider | Modulation effect type (chorus/flanger/phaser) | — | — | click only | [Effects: PHSR (modulation FX) tab (picture europa-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Type" |
| EURO-F-K201 | MOD FX DEPTH | Modulation effect depth | — | — | click only | [Effects: PHSR (modulation FX) tab (picture europa-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Depth" |
| EURO-F-K202 | MOD FX RATE | Modulation effect rate | — | — | click only | [Effects: PHSR (modulation FX) tab (picture europa-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Rate" |
| EURO-F-K204 | MOD FX SPREAD | Modulation effect spread | — | — | click only | [Effects: PHSR (modulation FX) tab (picture europa-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Spread" |
| EURO-F-K203 | MOD FX AMOUNT | Modulation effect amount | Mod Effect Amount | — | display/Remote item, not mapped | [Effects: PHSR (modulation FX) tab (picture europa-fxphsr-view_front_labeled.png)] tooltip "Mod Effect Amount" |
| EURO-F-S601 | REVERB DECAY | Reverb decay | — | — | click only | [Effects: REV tab (picture europa-fxrev-view_front_labeled.png)] tooltip "Reverb Decay" |
| EURO-F-K601 | REVERB SIZE | Reverb size | Reverb Size | 46 / CC 75 | voice/MIDI or click | [Effects: REV tab (picture europa-fxrev-view_front_labeled.png)] tooltip "Reverb Size: 73.1" |
| EURO-F-K602 | REVERB DAMP | Reverb damp | Reverb Damp | — | display/Remote item, not mapped | [Effects: REV tab (picture europa-fxrev-view_front_labeled.png)] tooltip "Reverb Damp: 20.0" |
| EURO-F-K603 | REVERB AMOUNT | Reverb amount | Reverb Amount | 45 / CC 74 | voice/MIDI or click | [Effects: REV tab (picture europa-fxrev-view_front_labeled.png)] tooltip "Reverb Amount: 4x (clipped)" |
| EURO-F-D101 | MOD 1 src | Modulation matrix row 1: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K101 | MOD 1 k1 | Modulation matrix row 1: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod1 Dest1 Amt" |
| EURO-F-D103 | MOD 1 dest1 | Modulation matrix row 1: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B108 | MOD 1 up1 | Modulation matrix row 1: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K103 | MOD 1 k2 | Modulation matrix row 1: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod1 Dest2 Amt" |
| EURO-F-D105 | MOD 1 dest2 | Modulation matrix row 1: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B110 | MOD 1 up2 | Modulation matrix row 1: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K105 | MOD 1 k3 | Modulation matrix row 1: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod1 Scale Amt" |
| EURO-F-D107 | MOD 1 scale | Modulation matrix row 1: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B112 | MOD 1 clr | Modulation matrix row 1: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-D102 | MOD 2 src | Modulation matrix row 2: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K102 | MOD 2 k1 | Modulation matrix row 2: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod2 Dest1 Amt" |
| EURO-F-D104 | MOD 2 dest1 | Modulation matrix row 2: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B109 | MOD 2 up1 | Modulation matrix row 2: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K104 | MOD 2 k2 | Modulation matrix row 2: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod2 Dest2 Amt" |
| EURO-F-D106 | MOD 2 dest2 | Modulation matrix row 2: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B111 | MOD 2 up2 | Modulation matrix row 2: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K106 | MOD 2 k3 | Modulation matrix row 2: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod2 Scale Amt" |
| EURO-F-D108 | MOD 2 scale | Modulation matrix row 2: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B113 | MOD 2 clr | Modulation matrix row 2: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-D109 | MOD 3 src | Modulation matrix row 3: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K107 | MOD 3 k1 | Modulation matrix row 3: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod3 Dest1 Amt" |
| EURO-F-D110 | MOD 3 dest1 | Modulation matrix row 3: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B121 | MOD 3 up1 | Modulation matrix row 3: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K108 | MOD 3 k2 | Modulation matrix row 3: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod3 Dest2 Amt" |
| EURO-F-D111 | MOD 3 dest2 | Modulation matrix row 3: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B122 | MOD 3 up2 | Modulation matrix row 3: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K109 | MOD 3 k3 | Modulation matrix row 3: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod3 Scale Amt" |
| EURO-F-D112 | MOD 3 scale | Modulation matrix row 3: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B123 | MOD 3 clr | Modulation matrix row 3: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-D113 | MOD 4 src | Modulation matrix row 4: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K110 | MOD 4 k1 | Modulation matrix row 4: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod4 Dest1 Amt" |
| EURO-F-D114 | MOD 4 dest1 | Modulation matrix row 4: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B124 | MOD 4 up1 | Modulation matrix row 4: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K111 | MOD 4 k2 | Modulation matrix row 4: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod4 Dest2 Amt" |
| EURO-F-D115 | MOD 4 dest2 | Modulation matrix row 4: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B125 | MOD 4 up2 | Modulation matrix row 4: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K112 | MOD 4 k3 | Modulation matrix row 4: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod4 Scale Amt" |
| EURO-F-D116 | MOD 4 scale | Modulation matrix row 4: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B126 | MOD 4 clr | Modulation matrix row 4: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-D117 | MOD 5 src | Modulation matrix row 5: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K113 | MOD 5 k1 | Modulation matrix row 5: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod5 Dest1 Amt" |
| EURO-F-D119 | MOD 5 dest1 | Modulation matrix row 5: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B127 | MOD 5 up1 | Modulation matrix row 5: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K115 | MOD 5 k2 | Modulation matrix row 5: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod5 Dest2 Amt" |
| EURO-F-D121 | MOD 5 dest2 | Modulation matrix row 5: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B129 | MOD 5 up2 | Modulation matrix row 5: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K117 | MOD 5 k3 | Modulation matrix row 5: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod5 Scale Amt" |
| EURO-F-D123 | MOD 5 scale | Modulation matrix row 5: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B131 | MOD 5 clr | Modulation matrix row 5: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-D118 | MOD 6 src | Modulation matrix row 6: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K114 | MOD 6 k1 | Modulation matrix row 6: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod6 Dest1 Amt" |
| EURO-F-D120 | MOD 6 dest1 | Modulation matrix row 6: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B128 | MOD 6 up1 | Modulation matrix row 6: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K116 | MOD 6 k2 | Modulation matrix row 6: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod6 Dest2 Amt" |
| EURO-F-D122 | MOD 6 dest2 | Modulation matrix row 6: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B130 | MOD 6 up2 | Modulation matrix row 6: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K118 | MOD 6 k3 | Modulation matrix row 6: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod6 Scale Amt" |
| EURO-F-D124 | MOD 6 scale | Modulation matrix row 6: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B132 | MOD 6 clr | Modulation matrix row 6: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-D125 | MOD 7 src | Modulation matrix row 7: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K119 | MOD 7 k1 | Modulation matrix row 7: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod7 Dest1 Amt" |
| EURO-F-D126 | MOD 7 dest1 | Modulation matrix row 7: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B133 | MOD 7 up1 | Modulation matrix row 7: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K120 | MOD 7 k2 | Modulation matrix row 7: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod7 Dest2 Amt" |
| EURO-F-D127 | MOD 7 dest2 | Modulation matrix row 7: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B134 | MOD 7 up2 | Modulation matrix row 7: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K121 | MOD 7 k3 | Modulation matrix row 7: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod7 Scale Amt" |
| EURO-F-D128 | MOD 7 scale | Modulation matrix row 7: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B135 | MOD 7 clr | Modulation matrix row 7: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-D129 | MOD 8 src | Modulation matrix row 8: src | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K122 | MOD 8 k1 | Modulation matrix row 8: k1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod8 Dest1 Amt" |
| EURO-F-D130 | MOD 8 dest1 | Modulation matrix row 8: dest1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B136 | MOD 8 up1 | Modulation matrix row 8: up1 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K123 | MOD 8 k2 | Modulation matrix row 8: k2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod8 Dest2 Amt" |
| EURO-F-D131 | MOD 8 dest2 | Modulation matrix row 8: dest2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B137 | MOD 8 up2 | Modulation matrix row 8: up2 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-K124 | MOD 8 k3 | Modulation matrix row 8: k3 | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Mod8 Scale Amt" |
| EURO-F-D132 | MOD 8 scale | Modulation matrix row 8: scale | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B138 | MOD 8 clr | Modulation matrix row 8: clr | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) (rows hovered: text fields, arrows and clear buttons gave no tooltip) |
| EURO-F-B101 | EFFECTS light | Effects section on/off (light) | Effect On | — | display/Remote item, not mapped | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] tooltip "Effect On" |
| EURO-F-B114 | EFFECTS power | Effects power button | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B102 | PHSR tab | Show the PHSR panel | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B115 | PHSR ON/OFF | PHSR effect on/off | Phaser On | — | display/Remote item, not mapped | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B103 | DIST tab | Show the DIST panel | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B116 | DIST ON/OFF | DIST effect on/off | Dist On | 38 / CC 67 | voice/MIDI or click | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B104 | EQ tab | Show the EQ panel | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B117 | EQ ON/OFF | EQ effect on/off | EQ On | — | display/Remote item, not mapped | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B105 | DLY tab | Show the DLY panel | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B118 | DLY ON/OFF | DLY effect on/off | Delay On | 40 / CC 69 | voice/MIDI or click | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B106 | REV tab | Show the REV panel | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B119 | REV ON/OFF | REV effect on/off | Reverb On | 44 / CC 73 | voice/MIDI or click | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B107 | COMP tab | Show the COMP panel | — | — | click only | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |
| EURO-F-B120 | COMP ON/OFF | COMP effect on/off | Comp On | — | display/Remote item, not mapped | [Lower half: modulation matrix and effects row (scrolled down) (picture europa-lower-view_front_labeled.png)] no tooltip in Reason (hovered 1.3 s) |

## Europa Shapeshifting Synthesizer — back
| Code | On panel | What it does | Reason name | Knob slot / CC | How | Checked |
|---|---|---|---|---|---|---|
| EURO-B-J01 | Seq Gate In | Gate input (sequencer) | — | — | cable: right-click jack > device > jack name | tooltip "Seq Gate Input" |
| EURO-B-J05 | Seq Note In | Note CV input (sequencer) | — | — | cable: right-click jack > device > jack name | tooltip "Seq Note Input" |
| EURO-B-K01 | Pitch Bend CV trim | Amount for pitch bend CV | — | — | click/drag only (no Remote item) | tooltip "PitchBend CV Amount (clipped)" |
| EURO-B-J02 | Pitch Bend CV In | CV input: pitch bend | — | — | cable: right-click jack > device > jack name | tooltip "PitchBend CV Input" |
| EURO-B-K02 | Mod Wheel CV trim | Amount for mod wheel CV | — | — | click/drag only (no Remote item) | tooltip "ModWheel CV Amount (clipped)" |
| EURO-B-J06 | Mod Wheel CV In | CV input: mod wheel | — | — | cable: right-click jack > device > jack name | tooltip "ModWheel CV Input" |
| EURO-B-J03 | CV In 1 | CV input 1 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 1" |
| EURO-B-J07 | CV In 2 | CV input 2 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 2" |
| EURO-B-J09 | CV In 3 | CV input 3 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 3" |
| EURO-B-J11 | CV In 4 | CV input 4 (assignable as a modulation source) | — | — | cable: right-click jack > device > jack name | tooltip "CV Input 4" |
| EURO-B-J04 | CV Out 1 | CV output 1 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 1" |
| EURO-B-J08 | CV Out 2 | CV output 2 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 2" |
| EURO-B-J10 | CV Out 3 | CV output 3 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 3" |
| EURO-B-J12 | CV Out 4 | CV output 4 | — | — | cable: right-click jack > device > jack name | tooltip "CV Output 4" |
| EURO-B-J13 | Audio Out L | Audio output, left | — | — | cable: right-click jack > device > jack name | tooltip "Left Output" |
| EURO-B-J14 | Audio Out R | Audio output, right | — | — | cable: right-click jack > device > jack name | tooltip "Right Output" |

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
