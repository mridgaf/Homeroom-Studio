# Handoff to Code: Answer melody + loop arrangement
## Part 4 of 4: build order, tests, listening, questions
**Previous:** Part 3

## Ask FIRST (Q1 blocks Phase A, Q3 blocks Phase B)
Ask as clickable options, at the END of your first reply. Put your recommendation first.
1. **Where the melody lives (BLOCKING):**
   (a) Upgrade the existing 2nd part ("lead") from the chord's rhythm to a real answering tune. It only plays on the ~45% of beats that roll 2+ parts. Smallest change, and the rack stays the same.
   (b) A new melody part that can play on any beat (rolled, e.g. half of beats). It needs a new rack row and stem name.
2. **How often (ASSUMING "about half of non-loop beats"):** every beat, about half, or only certain DJs.
3. **Arrangement place (BLOCKING for Phase B):** inside every 4-bar loop (repeats every loop), or only in Song Sketch songs (sections across 3:00).
4. Do NOT ask about the 808. Answer from the 2026-09-23 rule.

## Build order (each step small and checkable)
1. **Confirm the facts.** Re-read the Part 2 line ranges. Fix this brief if anything moved. Baseline: `./.venv/bin/python -m pytest tests/test_bass_rhythm.py tests/test_chord_rhythm.py tests/test_harmony.py -q`.
2. **Count the pool** (UNVERIFIED #3): melodic one-shots per group with a measured note, and their note range. Report the numbers before writing the picker.
3. **Back up** `beat_machine.py`, `beat_recipes.py`, `pattern_gen.py` and `crew.py` as `*.pre-melody-2026-10-XX.py`.
4. **Phase A:** write `tools/melody_rhythm.py` (pure `plan_phrase()` + `render_line()` like `bass_rhythm`). Write `tests/test_melody_rhythm.py` BEFORE wiring:
   - determinism;
   - every note in the key's scale, or a chord tone;
   - chord tone on steps 0/8 when a note lands there;
   - at least one silent bar per 4;
   - no more than one leap per phrase;
   - all notes within 12 semitones of the file;
   - levels only from characters;
   - no stamp gives byte-identical old output;
   - a loop-led beat gets no melody.
5. **Wire Phase A** behind `melody_flow`. Stamp it in `add_bass_and_chords`, plus the MIDI track and the recipe record.
6. **Full suite**, run ALONE: `./.venv/bin/python -m pytest tests/ -q --ignore-glob='*.pre-*'`. The ignore is needed: a stray `tests/test_sound_engine.pre-base-layer-2026-10-18.py` breaks collection without it. Known unrelated failures on 2026-10-19: `test_boundary::test_tools_never_import_reason_voice` (`panel_sweep.py`) and `test_pattern_gen::test_guest_lanes_appear_from_the_dj_palette` (reversefx). One line at the end of the report, no diagnosis.
7. **Rebuild check:** rebuild 3 recent beats in memory (`swap_many(no, {}, trims={"kick": -6.0}, render_only=True)`) with the backed-up code and with the new code. The SHA-256 must match. (A no-change rebuild raises "Nothing to change". The same trim on both sides is fine.)
8. **Phase A A/B** (only if his prompt asks for renders): copy `tools/make_bass_groove_ab.py` → `make_melody_ab.py`. Two identities per chord family, at least 1 legend and 1 genre, skipping 808 DJs is NOT needed (the melody isn't bass), skipping loop-led beats. Save to `~/Desktop/Homeroom Auditions/Homeroom MELODY <date>/` with a one-part READ ME naming the motif per file. **STOP for his verdict.**
9. **Phase B** only after he keeps Phase A and answers Q3. Same steps 3-8, with `arrange_flow`, its own tests (silences loop-safe, never bar 1's downbeat, at most one silence per loop, the fill lands in the last beat), and its own A/B folder `Homeroom ARRANGEMENT <date>`.
10. **DECISIONS.md entry** per phase: what changed, overruled rules quoted, backups, how to verify, status open until he listens.

## Done means
- All tests pass (except the known unrelated two), rebuilds are identical, and the A/B is on his Desktop.
- He listens and says keep or change. Nothing is "fixed" before his ear says so.

## Ideas noticed (NOT this task; mention once, at the end)
- Per-section arrangement for full songs already lives in Song Sketch. If he picks "Song Sketch" for Q3, Phase B moves there instead.

=== END OF PART ===
