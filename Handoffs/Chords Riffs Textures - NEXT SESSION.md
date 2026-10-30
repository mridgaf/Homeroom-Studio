# Chords, riffs, textures: what's left (handoff 2026-10-29)

Read `DECISIONS.md` entries dated 2026-10-29 first. Nothing below is rendered or heard.
House rules for this work: one quick check after a change (seconds to ~2 min), then stop; never the full suite or long test runs unless he asks; nothing in the sandbox; long jobs in the background; no renders; he commits.

## Done today (uncommitted, his to commit)
- Every DJ/Legend/genre rolls any chord style, borrows any drum part and any kick book on 50% of beats (`tools/beat_machine.py`, `tools/pattern_gen.py`).
- Chord source: jazz, jazz rap, lo-fi, soul, gospel (major), funk, R&B now from iReal charts; "sus" parse bug fixed (`tools/build_chord_tables.py`, `chord_tables.json`). Other styles still Chordonomicon (guitar tabs).
- Riff table: `riff_tables.json` (Lakh rap/rnb + 51 from his pack melodies), built by `tools/build_riff_tables.py`.
- Texture per new beat (`tools/riff_gen.py`, `preset["texture_flow"]`): full 10% / two notes 30% / riff 30% / loop 30%. Riffs fitted to the chords; half get a soft 2-note bed. "Loops only" mode untouched.

## Left to fix
1. **`test_loops_always_play_alone`** (`tests/test_beat_machine.py`). Edited to skip riff/two beats and check 24 seeds (was 8) so enough loop beats are counted. That edit is UNTESTED: the run was stopped. Run just that one test.
2. **`test_removing_a_sound_leaves_every_other_sound_where_it_was`** fails. Not caused by today's work: on the pre-change code, removing a snare already moved chord levels on some beats (seed 2: chord0 -0.07 dB). The 50% drum borrow made the test's own beats hit it (bass0 +1.5 dB, chord0 -0.8 dB). Recipes match parent vs child; the cause is in the rebuild render, not found yet. This is his 2026-09-27 complaint ("remove a sound and the others change").
3. **Full chords per identity from research.** He picked "rare, research decides". Today it's a flat 10% for everyone (he had no preference on the split, so it's an ASSUMING). Next: research which DJs/genres get full keys (soul/R&B/G-funk/jazz likely) and give each its own texture weights.
4. **Hip-hop/club/latin/rock/G-funk chords are still guitar-tab data** (85% plain triads, same few pop loops in every style). Options he was offered: favor each style's own loops over shared ones, tag whole words only, add color when voicing. He has not picked yet.
5. **Silent extra lanes.** Some test beats print "chord1 made no sound, no stem written" (seen on a loop beat and a doubled-riff beat). Not checked whether that's old behavior. Look before calling it a bug.
6. **A riff on a 1-bar chord slot** that lands on the riff's empty half now plays the riff's other bar. Fine in theory, not heard.
7. **Full test suite** has not run since these changes. Only when he asks.

## Backups (all today)
`tools/*.pre-open-patterns-2026-10-29.py`, `tools/*.pre-texture-2026-10-29.py`, `tools/build_chord_tables.pre-ireal-2026-10-29.py`.

## What he should listen for (when he renders)
- Doc Day and others reaching styles outside their old three.
- Beats carried by a riff or two notes instead of big chords; full chords rare.
- The beat card's "texture:" line says which one it got.
