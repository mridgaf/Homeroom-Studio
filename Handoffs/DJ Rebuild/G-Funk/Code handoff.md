# G-Funk: Code handoff (Part 1 of 2: what to change)

Do NOT render. Do NOT run the suite unless he asks for a render. One identity only: G-Funk, in `genres_config.json`. Back up first (`genres_config.pre-g-funk-settings-<date>.json`).
New line is already in the config (listen + _research_note only). Research: `research transcript.md` in this folder.

## Settings the new line needs
| Line phrase | Change in genres_config.json -> G-Funk | Source / who picked |
|---|---|---|
| "synth and electric piano chords" | signature.chord_source, GENRE RULE = 100% research instruments (his rule 2026-10-23): synth 3, piano 3, guitar 1.5, organ 1, strings 1, loop 1. ZERO for bell, choir, pluck, wood, horns, pad. midi unchanged (it is a source of exact notes, not an instrument; check it still fits) | Direction = his picks 2026-10-23 (lean to keys/synth; genres honor research fully). Which sounds are research instruments is sourced (see list below). The numbers are Claude's picks, NOT sourced |
| "rolling funk bass" | bass stays chord_family bright_funk. If the library has too little electric bass for a beat, a bass synth stands in. Say so in the report | his rule 2026-10-23: bass synths allowed where needed |
| "around 95 BPM" | bpm stays 95. Optional: tempo 88-105 -> 90-100 | Sources: 92-96 core, 90-100 genre. Optional, Claude's suggestion; ask him |
| everything else | no change | the old settings already back it |

## Research instruments (who gets odds, and why)
- synth: high portamento lead and keys, 5 sources [CONFIRMED]
- piano (electric piano, Wurlitzer, Rhodes): Wikipedia, POW, Krims [CONFIRMED]
- guitar: Quik with Robert Bacon, funk guitar riffs [CONFIRMED the genre uses it]
- organ: Hammond-style riff in Regulate, one source [UNSURE]
- strings: SY77 string sound in Regulate, one source [UNSURE]
- loop: Regulate is a four-bar sampled loop, but Krims says minimal sampling [CONFIRMED both ways, so a small share]
- NOT research instruments, so zero: bell, choir (no sample anyway), pluck, wood (none named by any source); horns (only Quik's early records, not carried into the line); pad (no source)

## Exception rules
- The 100%-research-instruments odds are a genre rule (dj-rebuild rule 8). Each genre gets its own instrument list. Add a test asserting G-Funk's chord_source has zero weight on bell, choir, pluck, wood, horns and pad.
- Grep tests for G-Funk wording first: `grep -rn "G-Funk" tests/`. test_crew.py lines ~778-787 mention its kit tags; do not break them.

## Leave alone
Swing 56 (his pick), snare 0.95/0.05 (his pick), kit tags, kick flavors, bass family bright_funk, progressions, key. The hat and perc rhythm weights stay: the line no longer names them.

# Part 2 of 2: checks and what is missing

1. `tools/identity_survival.py --genres --dj "G-Funk"`: any line phrase surviving under half the time gets fixed or reported. Expect "synth and electric piano chords" to improve after the lean.
2. Blind-spot table: jazz coloring (chord_color depth 0.55, dom9/7sus4 lean) and deep_* progressions are still on for G-Funk. Research says simple loops at the core, jazzier only in Quik's later records. Check whether the "Jazz out for everyone" pass has run; if not, flag it, do not fix it here.
3. Daily drift: `tools/evolution.py` can move genre fields. Check it cannot move chord_source for G-Funk.
4. Not buildable (no samples, no synthesized-tone rule): whistle portamento lead, talkbox, female backing vocals. Say so; do not fake with wrong words.
5. Update TRACKER.md (stage: settings done), DECISIONS.md, genre_newbuild_status.json.
6. Closed only by his ear. Ask (clickable) whether he wants an old-vs-new audition.
