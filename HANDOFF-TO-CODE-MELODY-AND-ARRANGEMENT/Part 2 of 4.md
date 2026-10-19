# Handoff to Code: Answer melody + loop arrangement
## Part 2 of 4: VERIFIED facts (read in the code 2026-10-19, after the bass groove landed)
**Previous:** Part 1  **Next:** Part 3 of 4.md (design spec + UNVERIFIED)

Line numbers are `tools/beat_machine.py` unless named, as of 2026-10-19 evening. Re-check them; the file changes daily.

## Melodic parts today
- `_split_chord_roles(notes)` ~line 1915 splits one chord into support (root+5th), lead (the colour tones, +12) and passing (the top extension, +24). See `theory/arrangement.md` (66 lines, the house rules for 2-3 parts: different heights, split don't double, take turns, one boss, silence counts).
- Part count is rolled ~line 2790: `random.Random(variant*617+5).choices((1,2,3), weights=OWNER_TASTE["melody_part_weights"])`. The weights are `(0.55, 0.35, 0.10)` in `tools/groove.py` ~line 299, with `passing_note_p` 0.5. So 55% of beats have ONE melodic part.
- `part_count = 1` when `voice` was picked or `primary in ("loop", "chip", "midi")`.
- Role render ~line 2824: `_render_one(..., notes=splits[k][role], rhythm_override=None if role == 1 else "sustain")`. So the **lead plays the chord's own rhythm figure**, and support/passing are held. The lead never plays an independent line. **This is the gap.**
- Lanes: `chord{i}` = the first instrument, `chord{i}v{n}` = each extra layered part. The regexes are `_CHORD_LANE` and `_CHORD_BASS_LANE` ~line 5014. `_chord_family()` ~line 5025 maps them to rack rows (`chords`, `chords2`, `chordbass`). A new lane name needs a rack family, a stem label (`beat_recipes.LANE_LABELS`) and a drop/trim path. Reusing `chord{i}v{n}` gets all of that for free.
- `_one_instrument(used)` ~line 2060 refuses mixing instruments in one lane.
- A chord lane's lone `X` triggers its whole slot buffer, so a performance must be baked INTO the buffer. The `chord_rhythm.py` header explains this, and `bass_rhythm.py` repeats it.

## Bass groove (landed and kept 2026-10-19, the model to copy)
- `tools/bass_rhythm.py`: `plan_line()` is pure, `render_line()` renders the whole loop into one buffer, `kick_feel()`. Tests: `tests/test_bass_rhythm.py` (16).
- It's wired at ~lines 3006-3060: one loop buffer, cut at each slot's render trigger sample `int(start_bar*bar_s*SR)`, each piece one sample short of the next trigger. Gain is uniform on stamped beats. MIDI: `bass_line` per `midi_chords` entry, written by `beat_recipes.write_midi` as a `bass` track on channel 2.
- The render's low-end choke (crew.py ~1740) only touches `_ducks_deep` lanes (bass/808). Chord lanes are NOT choked, so overlapping chord-lane buffers SUM.

## Arrangement today
- **Drum fills:** `pattern_gen._fill()` ~line 879 adds hits in the last quarter of a bar. `assemble()`, `_phrase()` and `_seed_phrase()` put fills on the closing bar of each 4-bar group (bars 4 and 8).
- **Drop-out:** the preset key `breakdown` = `{bars: [1-based], len: fraction of the bar, p: odds, keep: [lanes]}`. It's read in `crew.render_crew_beat` ~lines 1620-1648, with one bar picked per beat (seeded by `num`, `vel_seed`). It skips every lane hit in that bar's front `len`, unless the lane starts with a `keep` name. **Only Night Metro has it** (bars 3/5/7, len 0.5, p 0.6, keep kick). No legend or genre uses it.
- **Read in code, NOT tested:** chord and bass lanes only have a hit on their slot's FIRST bar. So a drop-out on a mid-slot bar does nothing to them, and a drop-out on a slot's first bar silences that WHOLE slot (all its bars). Phase B must not reuse `breakdown` for melodic parts as-is.
- **Turnaround:** chord flow can add a quick turnaround chord at the loop end (`harmony_info["flow"]["turnaround"]`).
- **Loop length:** `crew.bars_of(preset)`, 4 bars normally (2 or 8 possible). The render folds anything past the end back onto the start (loop-safe; no edge fades — memory rule).
- **Risers and swell fx** exist as sample lanes in some identities (`crew_config.json`). They're his samples, so allowed.

## Research on hand
- `Production Research Hub/Chapters/13 College theory for MIDI patterns/` (4 parts): voice-leading, modes and their colour note, emotion map, testable rules. **It has no melody-writing or counter-melody rules.** Melody rules in Part 3 are standard practice from Claude's knowledge, labelled as such.
- Ch.04 Part 4 ~line 166: phrase-tail holes belong to the soloist (synthesis).

=== END OF PART ===
