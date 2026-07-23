---
name: midi-validity-gate
description: Verify generated drum MIDI actually parses and is drum-valid BEFORE handing files to the owner. Use as the final step whenever this project writes .mid files — beats, loops, patterns, packs, experiments, crew output. Checks channel 10 (GM drums), note numbers in the GM drum range, an embedded tempo and time signature, and a non-empty note count, and refuses to deliver a file that fails. Turns the manual "does it open in Reason?" spot-check into an automatic gate.
---

# MIDI Validity Gate

Every beat session used to end with a manual check that the `.mid` opened on
channel 10 with the right drum notes. That's a seatbelt being buckled by
hand. This skill makes it automatic: generate → **run the gate** → only then
tell the owner it's ready. A file that fails the gate is a bug to fix, not a
file to ship.

## What "valid drum MIDI" means here

- **Channel 10** (zero-indexed channel 9) — Reason and every GM device expect
  drums there. The file must carry at least one note on it.
- **GM drum note numbers**, roughly 35–81 (kick 35/36, snare 38/40, closed
  hat 42, open hat 46, claps 39, toms/cymbals up the range), for every
  channel-10 note. One outside that band means a melodic pattern leaked into
  the drum track.
- **Notes on other channels are fine.** A "chords" beat writes harmony.py's
  voicings as a polyphonic track on channel 1 deliberately, so Reason doesn't
  read them as drum hits (`beat_recipes.write_midi`). The gate used to fail
  every chord beat over this — it was older than the feature (fixed
  2026-07-23).
- **Embedded tempo** (`set_tempo`) so the loop plays back at the intended BPM
  instead of a default 120.
- **A time signature** meta event.
- **At least one note** — silent files have shipped before; catch them.

## Workflow

1. After writing the `.mid`(s), run:
   `cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python .claude/skills/midi-validity-gate/scripts/check_midi.py <file-or-folder>`
   (or wherever the skill is installed). It prints a PASS/FAIL table and exits
   non-zero if anything fails.
2. If a file FAILS, fix the generator and re-render — do not hand it over.
3. Only report beats as ready once the gate passes. Say so: "checked — all N
   files parse on channel 10 with embedded tempo."

## Honesty

The gate proves the file is *structurally* correct MIDI a device will read
right. It does **not** prove the beat sounds good — you can't hear it. Keep
those two claims separate: "verified it parses" is true; "it slaps" is for
his ears.
