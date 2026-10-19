# Handoff to Code: Bass groove
## Part 3 of 4: design spec, and what is UNVERIFIED
**Previous:** Part 2  **Next:** Part 4 of 4.md (build order, tests, listening, questions)

## Figures (new module `tools/bass_rhythm.py`)
Each figure writes one 16-char string per bar of the slot (X/x/o/. or -) plus a pitch per hit. These are standard bass-playing techniques. The weights below are MY creative choices (owner gave creative control), not sourced numbers; say so in DECISIONS.
- **hold**: root on step 0; on slots of 2+ bars, a soft `o` re-strike on later bars. (Keeps the old sound as one option.)
- **kick**: bass hits on the kick's steps in each bar (read from the kick lane bars). The first hit is the root `X`; occasional later hits go to the octave or fifth. Hip-hop staple.
- **fifth**: root on beat 1, fifth on beat 3 (or the fifth below if the one above is out of range).
- **octave**: root/octave alternating 8ths, accents on beats, some rests (disco/funk).
- **walk**: quarter notes: root, chord tone, chord tone or scale step, then a chromatic approach (next root plus or minus 1 semitone) on the slot's last beat.
- **push**: the next chord's root struck early, on step 14 (an 8th early) or 15 (a 16th early) of the slot's last bar. The NEXT slot then skips its own downbeat hit (tied in). Needs a planning pass across all slots.
- **funk**: root `X` on step 0 plus syncopated hits from cells {3, 6, 7, 10, 11, 14}, some written `.` (ghost/dead notes), occasional octave pops.

Loop wrap: the last slot's approach or push targets the FIRST slot's root.

## Family weights (my starting point; tune by ear)
| Family | Figure weights |
|---|---|
| soul_jazz | walk 3, kick 2, fifth 2, push 2, hold 1 |
| dark | hold 3, kick 3, push 1, pulse 1 |
| grit | kick 4, push 2, fifth 1, hold 1, octave 1 |
| dreamy | hold 3, push 2, fifth 2, walk 1 |
| bright_funk | funk 3, octave 3, kick 2, push 1 |

"pulse" means 8th-note roots, accented on the beats with ghost off-beats. Add it to the figure list. An identity can override with an optional `signature.bass_grammar` dict (same pattern as chord_grammar). If the family is missing, use a house default of kick 3, hold 2, fifth 2, push 1.
Roll the figure per slot with its own seed (e.g. `variant*887 + 31 + slot`) so no other roll moves.

## Rendering rules
- Pitches stay near the picked file's recorded note (`pick["note"]`). If a target is more than 12 semitones from it, substitute: octave goes to root, fifth goes to the fifth below. If still more than 12, use the root. Never synthesize.
- Monophonic: a note's length runs to the next hit (legato), minus nothing. A ghost `.` note is short, about 0.5 of a 16th.
- Feel: `LaneFeel(kick_off_ms, min(kick_jit, 4), kick_swing, seed)`. If there is no kick lane, use `(0, 2, 50)`. The lane tuple stays `(0, 0, 50, ...)` because the feel is baked in.
- If any note can't be voiced, fall back to the root for that note. If the root fails too, return None so the caller keeps today's behaviour for the whole line.

## UNVERIFIED (test before building on these)
1. That a held root bass is a MAIN cause of "AI slop" by ear. This is code-proven to be simple, not ear-proven to be the culprit. Falsified if the owner hears the A/B and says no difference that matters.
2. That `voice_note` with short durations sounds clean (attack/release ramps are 8ms/60ms per its docstring; a 60ms release on 16th ghosts at 140 BPM, where a 16th is about 107ms, may smear). Falsified by listening and by checking that the ghost notes are audible.
3. Pitch-stretch quality up to 12 semitones on HIS bass files. The owner accepted chipmunk risk for chords (PREFER_MAX_SHIFT note), but not explicitly for bass.
4. That `bass_flow` stamping keeps rebuilds identical. Prove it by rebuilding 3 existing beats and comparing hashes before and after.
5. That the kick lane is always present and shaped as described in every path, including genres, legends and free beats. Guard for a missing kick.
6. Family weights: invented by me, tune by ear.
7. The kick-locked figure may double the kick and add mud on 808-like bass files. Watch the low end; there's a one-low-sound rule.

=== END OF PART ===
