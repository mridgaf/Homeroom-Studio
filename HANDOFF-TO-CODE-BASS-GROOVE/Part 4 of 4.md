# Handoff to Code: Bass groove
## Part 4 of 4: build order, tests, listening, open questions
**Previous:** Part 3

## Build order (each step small and checkable)
1. **Confirm the facts.** Re-read the Part 2 line ranges in `tools/beat_machine.py`, `tools/chord_rhythm.py` and `tools/beat_recipes.py`. Fix this brief if anything moved. Run `./.venv/bin/python -m pytest tests/test_chord_rhythm.py tests/test_harmony.py -q` as the baseline.
2. **Back up** first: `tools/beat_machine.pre-bass-groove-2026-10-19.py` and `tools/beat_recipes.pre-bass-groove-2026-10-19.py` (house pattern).
3. **Write `tools/bass_rhythm.py`** with `FLOW_VERSION = 1`, `spec_for(preset)`, `plan_line(slots, key, kick_bars, spec, rng, fits)` (pure, returns per-slot `[(bar, step, char, midi_note)]`), and `render_line(plan_slot, dur, bpm, render_note, feel, sr)`.
4. **Write `tests/test_bass_rhythm.py`** BEFORE wiring. Cover:
   - determinism (same seed gives the same plan);
   - first hit of every slot is the root on step 0, unless tied in by a push;
   - monophonic (no overlapping notes);
   - every note within 12 semitones of the file note;
   - approach notes land 1 semitone from the next root, including the loop wrap to slot 0;
   - levels only from characters;
   - 100 seeds per family give at least 4 distinct figures;
   - a missing kick lane doesn't crash;
   - no `bass_flow` stamp gives exactly the old single held note.
5. **Wire it into `_build_chords`** behind `preset.get("bass_flow")`, and stamp it in `add_bass_and_chords`. Keep `bass_files`, `bass_pick`, `voice_files`, the rack dropdown and the harmony record working. Add `harmony_info["bass_figures"]` (the figure per slot) for the recipe.
6. **MIDI**: `midi_chords` entries get `"bass_line": [(start_sec, dur_sec, note, vel), ...]` and leave `bass_note` out of `notes` when it's present. In `write_midi`, add a separate `bass` track on channel 2 (0x91/0x81) when any entry has `bass_line`. Old beats are unchanged.
7. **Full suite**: `./.venv/bin/python -m pytest -q`. The baseline is about 1,331 tests. Report the pass/fail counts plainly.
8. **Rebuild check**: rebuild 3 existing beats; the audio must match the files on disk (UNVERIFIED #4).
9. **Listening A/B (the real test)**:
   - Use the existing `tools/make_*_ab.py` benches as the model.
   - Render pairs, same beat, old bass vs new bass. Do at least 2 identities per family, plus 1 genre and 1 legend.
   - Save them to `~/Desktop/Homeroom Auditions/Homeroom BASS GROOVE 2026-10-XX/`, with a one-part README naming the figure in each file.
10. **DECISIONS.md entry**: what changed, every overruled rule quoted, the backups, how to verify, status open until he listens.

## Done means
- All tests pass, rebuilds are identical, and the A/B files are on his Desktop.
- He listens and says keep or change. Nothing counts as "fixed" before his ear says so.

## Open questions for the owner (ask as clickable options, at the END of your reply)
1. (Blocking only at step 9) Should the A/B use his usual audition length and naming? Check the existing `Homeroom ... NEW BUILD` folders and copy that format instead of asking, if it's clear.
2. After the A/B: do the family weights feel right per DJ, or should some DJs lean to a figure?
3. Should the 808 beats ever get the new figures? Default NO (2026-09-23 rule). Only ask if he raises it.

## Other ideas noticed (NOT this task; mention once, at the end)
- After the bass: a second melodic part (counter-melody/lead) that answers the chords, and section changes (drop-outs, fills) across a loop. Check `theory/arrangement.md` first.

=== END OF PART ===
