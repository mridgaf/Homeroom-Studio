# Crunk: Code handoff (Part 1 of 2: what to change)

Do NOT render. Do NOT run the suite unless he asks for a render. One identity only: Crunk, in `genres_config.json`. Back up first (`genres_config.pre-crunk-settings-<date>.json`). The new line and map are already in the config (listen + _research_note only; backup `genres_config.pre-crunk-rebuild-2026-10-23.json`). Research: `research transcript.md` in this folder.

## ASSUMING (owner away, nobody could be asked)
1. Era: Lil Jon's Atlanta run 2002-2004 plus the hard festival end (Turn Down for What 2013, Aoki records). Memphis/Three 6 is the partner genre and keeps its dark end.
2. "Half-time at 140" stays: it fits the slow-grind records (73-82 felt = 146-164) and the 140 festival track. It does not fit the 100-105 records (Get Low, TDFW, Yeah!). Left as is; see pick 1.
3. The old words "a huge distorted 808" and "the room deliberately EMPTY" stay (test_crew.py ~427 reads the first; the second is a carried-over claim, one source for open space).
4. Dropped from the old line: "claps that hit like a crowd" (became "stacked 808 claps", same tags), "almost no hats" (research has eighths in choruses and double-time hats; now "sparse hats that turn plain eighths"), "hard synth-stab energy" (now the concrete "short repeated synth stab riff").
5. Phrygian: TDFW is E phrygian; Yeah! sources disagree (D major vs G minor). Kept the existing mode weights.

## Settings the new line needs
| Line phrase | Change in genres_config.json -> Crunk | Source / who picked |
|---|---|---|
| "short repeated synth stab riff" | signature.chord_rhythm "arp" -> "stab" (figure word from chord_rhythm.FIGURES). Optional: a dict with figures [["stab",3],["arp",1]] if he wants some arp left | Wikipedia (ostinato + bass stabs), RBMA (3-note vamp), Recording Arts (stabs). Claude's pick for the 3:1 split |
| "synth" first in the chords | signature.chord_source, GENRE RULE = 100% research instruments (his rule 2026-10-23). Proposed: synth 4, horns 2, strings 2, piano 1.5, guitar 1.5, bell 0.5, pluck 0.5. ZERO for choir, organ, pad, wood. Keep all entries. midi unchanged (2.416, now a different share of a smaller total: check it still lands near 25 percent; adjust midi to keep its share only if he asks) | Which instruments are research instruments is sourced (below). The NUMBERS are Claude's picks, NOT sourced |
| "phrygian minor" | none. key mode phrygian 3 / harmonic_minor 2 already back it | TDFW |
| "bass that holds" | none. chord_family dark (hold 3, kick 3) stays | no source for a bass figure |
| "sparse hats that turn plain eighths" | none. hat modes sparse .45 + eighths .30 already back it (75 percent). offbeats .15 and trip_rolls .10 stay unnamed | Wikipedia, Loopcloud |
| "stacked 808 claps", "short snare" | none. clap/snare tags already back them | Wikipedia, iZotope, Recording Arts |
| "half-time stomp at 140" | none (see pick 1) | |

## Research instruments (who gets odds, and why)
- synth: Wikipedia, RBMA, Recording Arts, Loopcloud, Wikipedia Oh Yeah, Racine Record [CONFIRMED, 6]
- horns (brass presets): PopMatters horn fanfares, Inside the Credits horn-like synth [CONFIRMED, 2]
- strings: RBMA Triton string melody, PopMatters orchestral flourishes [CONFIRMED, 2]. Goes to string_sampler.
- piano: RBMA sampled pianos, Inside the Credits Memphis hard piano [CONFIRMED, 2]
- guitar: Wikipedia infobox, Some Cut credit (Craig Love) [CONFIRMED the genre uses it; nobody says how often]
- bell: one 16th-note bell melody in Yeah! [UNSURE, 1 source]
- pluck: "minimal synth plucks" on Snap Yo Fingers [UNSURE, 1 source; the synth group already reaches pluck/pad]
- NOT research instruments, so zero: choir (only 2 samples anyway), organ, pad, wood. No source names them.
- Bass: bass synths may stand in where no bass sample fits (the 808 lane already carries the low end). Bass guitar is credited on Yeah! and Some Cut (LaMarquis Jefferson); he has no bass guitar pool noted here, so say so in the report rather than faking it.

## Owner picks (clickable in the Code session)
1. Tempo: (a) keep 140 default, 140-160 pocket (recommended: fits slow grind + festival), (b) add a 100-105 lower pocket (widen to 100-160) so Get Low, TDFW and Yeah! tempos can occur. Changes: whether the radio records' tempo can appear.
2. Chord rhythm: (a) stab only (recommended), (b) stab 3 / arp 1. Changes: how often the riff is a stab versus an arpeggio.
3. Odds numbers above are Claude's picks: accept or change.

## Exception rules
- Add a test that Crunk's chord_source has zero weight on choir, organ, pad, wood. Scope to Crunk only; do not touch other genres.
- Tests that mention Crunk: test_crew.py ~427 (listen line says "a huge distorted 808"), ~450 (allow_dirt "low"), ~575 (low-dirt set is exactly Crunk, Mustang, Night Metro), ~787 (own_soundbank list); test_collab_genres.py lines 15-16. Do not break them.
- Edit the JSON as text inside the Crunk block: genres_config.json has its own indent, a load/dump rewrite makes a huge diff.

## Leave alone
Kit tags and kick flavors, allow_dirt low, kick_dist 9.0, clap and snare grammar, hat modes, genre_swing 50 (NOT FOUND, no reason to move), space gated clap, sidechain, drive, library/extras, key roots, chord_family dark, progressions list, flavor_match on. No vocal chops (the room stays empty for the chant).

# Part 2 of 2: checks and what is missing

## Blind-spot table
| Check | Where | Result |
|---|---|---|
| Jazz coloring / deep loops | chord_color, deep_* | OK: depth 0.0, lean empty, no deep_* in the list (jazz-out done) |
| MIDI chord share | chord_source midi | 2.416 of 9.665 = 25 percent. MIDI chords ignore the loops and the stab/arp figure; fine at 25 percent, recheck after the odds change |
| Chord odds | chord_source | PROBLEM: 11 families all 0.659, line names synth. Fixed by the handoff table |
| Hats and percussion | hat grammar | OK: sparse + eighths 75 percent |
| Bass | chord_family dark, 808 bass lane | OK; bass guitar (Yeah!, Some Cut) not buildable without a bass pool |
| Percussion lane | kit perc tags | none in kit; line names none |
| Tempo | bpm 140, tempo 140-160 | outside 100-105 records (pick 1) |
| Daily drift | tools/evolution.py | it edits crew_config.json only; grep shows chord_source deltas on crew presets. Genres are not in that file, so Crunk's chord_source cannot drift (verify before claiming) |
| Duplicate | Memphis | different: Memphis = lo-fi dark, triplet hats, cowbell; Crunk = bright synth stabs, 808 claps. Memphis not rebuilt yet; keep them apart when it is |
| Shared dirt | Mustang, Night Metro | all three are "low" dirt on purpose (test pins the set) |

## Checks to run (Code, no render)
1. `tools/identity_survival.py --genres --dj "Crunk"` (unsandboxed, it writes ~/.reason_voice). Any line phrase surviving under half the time gets fixed or reported. Expect "stab" to be the weak one until chord_rhythm changes.
2. Not buildable: chant vocals as the lead, bass guitar, the squeaking-chair sample from Some Cut, a whistle/flute lead (Yeah!). Say so; do not fake with wrong words.
3. Update TRACKER.md (stage: settings done), DECISIONS.md, genre_newbuild_status.json (stage built, keep the old verdict in notes: the earlier Crunk audition was heard and confirmed 2026-10-1x, "They sound good").
4. Closed only by his ear. Ask (clickable) whether he wants an old-vs-new audition. DO NOT RENDER unless he asks in that message.
