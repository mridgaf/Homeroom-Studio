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
