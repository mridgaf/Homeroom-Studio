# Handoff to Code: Answer melody + loop arrangement
## Part 3 of 4: design spec, and what is UNVERIFIED
**Previous:** Part 2  **Next:** Part 4 of 4.md (build order, tests, questions)

These are standard arranging and melody-writing practices from Claude's own knowledge, not sourced. The numbers are starting points; tune by ear. Say so in DECISIONS.

## Phase A: `tools/melody_rhythm.py` (the answer melody)
- **Notes:** the key's scale (`KeyContext.scale()`). Strong beats (steps 0 and 8) take a chord tone of the chord sounding then. Other notes move by step (1-2 scale steps). At most one leap per phrase, then step back the other way.
- **Motif:** roll a 2-5 note cell (rhythm + contour) once per beat. Play it, then answer it with the same rhythm and a changed ending (call and response). The loop's last phrase ends on a chord tone of the chord that lands on bar 1, so the wrap resolves.
- **Where it plays:** in the chord figure's gaps. Weight against the cells where the chord parts hit (the way `chord_rhythm` "comp" avoids drum cells). Lean to phrase tails: the back half of bars 2 and 4.
- **How much:** rests most of the time. Starting point: notes in about 40% of the bars, 2-6 notes per phrase, at least one fully silent bar per 4. Never on every 16th.
- **Register:** above the chords (the chords' top note +3 to +12 semitones) and within `instrument_sampler.PREFER_MAX_SHIFT` (12) of the picked file's note. Out of range → octave-shift the whole phrase, never single notes.
- **Instrument:** ONE file family from his library, never the chord's own instrument if another owned voice exists. Keys, mallets, plucks or bells cut through. Lock per beat (`_one_instrument`). If no instrument can voice the phrase, the beat ships without a melody. Never synthesize.
- **Feel:** the hats' or chords' feel (offset/swing, jitter ≤4 ms). Levels only from X/x/o/. characters.
- **Per identity:** family defaults (`signature.chord_family`), plus an optional `signature.melody_grammar` override (same pattern as `bass_grammar`). The dark family plays the sparsest; bright_funk the busiest.
- **Output:** one loop buffer cut at the slot starts (the bass trick). The lane is either `chord{i}v{n}` (reusing the lead role) or a new lane. That choice is Q1 in Part 4, BLOCKING.
- **MIDI:** a separate `melody` track (channel 3), like the bass line. **Recipe:** `harmony_info["melody"]` = motif + notes.

## Phase B: arrangement moves (new beats only, `arrange_flow`)
Pick 0-2 moves per beat, seeded from the variant:
- **stop:** chords + bass + melody go silent for the last 1-2 beats of the loop. Drums play a fill into bar 1. Bake the silence INTO the slot buffers (zero that region, with ~5 ms ramps). Do NOT use `breakdown` (Part 2: it would kill a whole slot).
- **thin bar:** one bar (3 by default) where the drums drop to kick (+ hat), and the melodic parts play.
- **melodic drop:** one bar where the chords drop out and only the bass + melody play.
- **fill into 1:** a stronger drum fill on the loop's last bar (snare/perc 16ths in the last beat). Extend `pattern_gen._fill` with a "big" option rather than adding a second fill system.
- Never more than one silence per loop. Never touch bar 1's downbeat. Everything must stay loop-safe (a silence at the end must not cut a note that wraps).

## UNVERIFIED (test before building on these)
1. That "no melody" is a main cause of "samey" by ear. Falsified if the A/B shows no difference that matters to him.
2. That a melody doesn't crowd a rapper. Nothing here can test that. Say so; maybe ask him to rap or hum over one.
3. That his library has enough single-note melodic one-shots with measured pitch in a usable range. Count them per group BEFORE designing the picker (use the `check-which-pool` memory rule: name the pool).
4. That zeroing a region inside chord slot buffers sounds clean (no clicks) through the master bus.
5. The Part 2 reading of `breakdown` on chord/bass lanes. Prove it with a quick synthetic preset before relying on it.
6. That a move repeating every 4 bars still sounds musical, not mechanical. A 4-bar loop repeats its drop every loop. Q3 asks whether this belongs in Song Sketch instead.
7. Every weight and percentage above: invented, tune by ear.

=== END OF PART ===
