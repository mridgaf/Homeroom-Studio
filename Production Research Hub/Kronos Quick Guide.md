# Korg Kronos 61 — Quick Guide

Source: Korg KRONOS Operation Guide, MIDI Implementation, Voice Name List (copies in `Originals/Kronos/`, personal use only).

## What it is
A keyboard that is also a whole studio. It makes its own sounds (it does not need Reason) AND can control Reason.

## What is on the front (left to right)
| Part | Does |
|---|---|
| Touchscreen | Pick sounds, change settings. Touch it. |
| Hold HELP + touch any knob | Tells you what that control does |
| 8 knobs + 9 sliders | Change the sound live (brightness, attack, reverb...). Meaning changes per sound |
| Joystick | Left/right = pitch bend. Forward = vibrato. Back = wah |
| Ribbon (touch strip) | Slide a finger to change the sound |
| SW1 / SW2 | Two switches, do different things per sound |
| KARMA | Plays patterns for you while you hold keys. Button: KARMA ON/OFF. LATCH keeps it going |
| Drum Track | Built-in drummer. Button: DRUM TRACK |
| Modes (buttons) | PROG = single sounds. COMBI = layered/split sounds. SEQ = record songs |

## Back of the keyboard
- USB B → your Mac (MIDI **and** USB audio — your Mac sees both).
- Audio outs L/R → speakers or Scarlett.

## Sound families (by Korg's categories)
2,176 sounds on this unit: pianos, electric pianos, organs, strings, brass, pads, bells, basses, leads, drums, FX.
Find one by words: ask Claude "creepy piano" and it shortlists names.

## 5 things to try first
1. Press PROG. Turn the VALUE dial. Play. Listen to a few.
2. Press KARMA ON/OFF, hold a chord. It plays patterns by itself.
3. Press DRUM TRACK. A drummer starts.
4. Move the joystick forward while holding a note.
5. Hold HELP and wiggle a slider — it tells you what it does.

## What Claude can do from your Mac (tools/kronos.py)
- Shortlist sounds by words ("creepy piano", "dark pad", "dirty drums").
- Switch the Kronos to a named sound.
- Play a test chord.
- Move cutoff / resonance / attack / release / reverb-send-type controls.
- Record the Kronos audio through the Mac and add distortion, reverb, pitch-down (pedalboard).

## What it cannot do
- Build a new sound from scratch by itself (needs the touchscreen).
- Tell you if a sound is "creepy" — only your ears can.

## Not yet confirmed on your unit
- Global MIDI channel = 1 and "Enable Program and Bank Change" ticked (Global → MIDI). If a sound does not switch, check these two.
