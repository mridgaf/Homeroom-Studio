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
