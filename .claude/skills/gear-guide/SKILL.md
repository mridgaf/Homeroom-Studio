---
name: gear-guide
description: Write a plain-English (explain-like-I'm-five) guide for a piece of studio gear and wire it into the Reason Voice app so "what is my X" answers with it. Use whenever the user shows or mentions new equipment (photos of hardware, "I just got a...", "here's my new pedal/mic/synth"), asks how a piece of his gear works or connects, or asks to update what the app knows about his setup. Also use when he says gear names like Launchkey, AudioBox, DTX, EMX66M, or asks how to hook something up to Reason.
---

# Gear Guide

Three deliverables whenever new gear enters his world:

1. **A device_ref guide** at
   `/Users/johnsuhr/Desktop/Homeroom Studio/device_refs/<gear-name>.md`
2. **Voice aliases** in `DEVICE_ALIASES` inside
   `/Users/johnsuhr/Desktop/Homeroom Studio/reason_voice/recipes.py`
   — every plain-words name he'd say for it ("my drum kit", "the mixer"),
   including likely whisper mis-hearings ("personas" for PreSonus).
   Alias values are the file's stem with dashes as spaces.
3. **The gear memory** at
   `~/.claude/projects/-Users-johnsuhr-reason-code/memory/user-gear-and-style.md`
   — add the item to the gear list so every future session knows it.

Read an existing guide first (`device_refs/yamaha-dtx400k.md` is the best
example) — match its voice exactly.

## The house style (why these guides work for him)

He's a self-taught musician, not an engineer. Each guide must:

- **Open by saying what the thing IS in one breath** ("The blue metal box.
  It's the middleman between microphones and the Mac").
- **Tour the controls in plain words**, translating every term inline
  ("gain — how loud the mic comes IN"). Green-light/red-light rules beat
  decibel numbers.
- **Show where it fits HIS rig**, not gear in general: recording goes
  through the AudioBox USB 96; playing Reason instruments goes over USB
  (Launchkey MK3 49, DTX400K); loud-in-the-room goes through the EMX66M
  mixer / Servo 300 amp; guitar tones come from the Crate, Epiphone
  Electar, or the red combo, mic'd into the AudioBox.
- **End with the "it's always one of these two" section** — the couple of
  things that are actually wrong when it doesn't work (wrong track
  selected, gain at zero, wrong pad mode). This is the most-used part.
- Include one safety/longevity rule if the gear has one (phantom power,
  amp power-on order), stated once without drama.

The first heading is the display name; the H1 line is skipped by the app's
doc panel, so don't put load-bearing info only there.

## Verify

```bash
cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python -c "
from reason_voice.recipes import RecipeLibrary
lib = RecipeLibrary('recipes', 'device_refs')
print(lib.device_ref('<an alias he would say>'))"
```

Must print the new file's path for each alias added. Run the project test
suite too (`./.venv/bin/python -m pytest tests -q`) since aliases live in
code. The guide is live in the app after a restart; mention that.
