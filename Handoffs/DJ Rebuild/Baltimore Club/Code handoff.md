# Baltimore Club: Code handoff (settings NOT changed yet)

Do NOT render. Do NOT run the suite unless he asks for a render. One identity: Baltimore Club, in `genres_config.json`. Back up first (`genres_config.pre-baltimore-club-settings-<date>.json`). Edit the JSON as text inside that one block (own indent; a load/dump rewrite makes a huge diff).
New line and map are already in the config (listen + _research_note only). Research: `research transcript.md` in this folder.

## ASSUMING (owner away, nothing asked)
1. ASSUMING the era = classic Baltimore club, about 1991-2008 (Unruly, Technics, Griff, Class, Rod Lee). The shake-off era (K-Spin, Blaqstarr, 132-150 BPM, gunshots) is left out of the line.
2. ASSUMING "KW Griff / Rod Lee" in the brief mean the Unruly/Club Kingz sound, not Jersey club.
3. ASSUMING the clap placement ("a" of 2, "&" of 3) stays in the line as a carried-over claim, because no source contradicts it and none supports it.
4. ASSUMING "never lets up" stays: it is an existing hard rule with a test.
5. ASSUMING instrument odds numbers below are Claude's picks (rule 8), not sourced.
6. Vice article was paywalled: the five-hit kick figure rests on No Tags + RA + a search-engine summary of Vice.

## Settings the new line needs
| Line phrase | Change in genres_config.json -> Baltimore Club | Source / who picked |
|---|---|---|
| "five-hit kick figure" | grammar.kick.hits [5,6] -> [5,5]. kick_min_hits 5 stays. Canon kick figures stay (they are 5 and 6 hit; check the 6-hit ones: `X--x--x-X--xx-x-` has 6, drop or keep) | five hits [CONFIRMED]; changing 6 to 5 is Claude's reading, ask him |
| "looping hard at 130" | none (bpm 130, tempo 125-130) | matches |
| "big 808 low end" | none (808 kick 70%) | matches |
| "handclaps ... a of 2, & of 3" | none | carried over, unsourced |
| "shuffling shakers" | extras: shakers is 1 of 5 pool entries. Make it first priority so most beats carry it (check how the pool picks; if by random draw, put shakers + vocal chops in a guaranteed slot or raise their pick odds) | Sing Sing = "glue" (Booman). Priority amount = his pick |
| "chopped, looped vocal chants" | same: vox 'vocal chops' guaranteed or favored | [CONFIRMED] genre-defining |
| "horns on top" | chord_source, genre rule | see below |
| "raw and distorted" | none (allow_dirt true, drive 1.55) | matches |
| bass (not in line, mismatch) | chord_family bright_funk gives funk/octave bass; research says 808 sub on the kick. Add signature.bass_grammar figures kick 4, hold 2, push 1 (the "grit" family) or set chord_family grit. A bass synth/808 stands in where no bass sample fits; say so in the report | [UNSURE] reading of "rattling subs, bass pulses" (RA); weights Claude's pick |

## Chord odds (genre rule: 100% research instruments)
Set chord_source: loop 3, horns 2, synth 2, piano 1. ZERO (keep entries) for bell, choir, guitar, organ, pad, pluck, strings, wood. midi stays at 3.383 (exact notes, not an instrument; it is ~25% of beats now and ignores the loops, check that share still fits).
- loop: chopped breaks/hooks [CONFIRMED]. horns: [CONFIRMED] (RBMA + RA). synth: tinny synths, arpeggio (RA, one source) [UNSURE]. piano: minor-key piano hook (SPIN, one source) [UNSURE].
- Not named by any source: bell, choir, guitar, organ, pad, pluck, strings, wood.
- Numbers 3/2/2/1 are Claude's picks. Add a test asserting the zeros. Grep tests first: `grep -rn "Baltimore" tests/` (test_collab_genres.py line 14 lists it as a host with no stamp lane; test_genres.py test_baltimore_kick_never_lets_up must still pass, and the docstring there quotes the old line).

## Owner picks (ask clickable after the Code pass)
1. Kick hits [5,5] or keep [5,6].
2. How much to favor shakers and vocal chops in extras.
3. Bass: 808 sub figures (recommended) or leave bright_funk.
4. Horn rhythm: horns now play under chord_rhythm "sustain"; no source says stabs. Leave unless he wants stabs.

## Blind-spot table
| Check | Finding |
|---|---|
| Jazz coloring / deep loops | chord_color depth 0.0, only plain_* and vamp progressions listed: clean. Confirm the jazz-out pass ran (backup genres_config.pre-jazz-out-2026-10-23.json exists) |
| MIDI chord share | 3.383 of ~13.5 total = ~25%; MIDI chords ignore the loops. Report only |
| Chord odds | PROBLEM: 8 unnamed instruments hold ~38% (0.65 each of 13.5). Fixed by the zeros above |
| Hats and percussion | hat modes sixteenths 30 / shuffle 25 / offbeats 25 / eighths 20; the line names no hat. Fine. Shakers/vox: PROBLEM, 1 of 5 pool entries |
| Bass | PROBLEM: bright_funk vs 808 sub (above) |
| Percussion lane | kit has no perc tag; shakers come from extras only |
| Tempo | 125-130: inside the researched range |
| Daily drift | tools/evolution.py reads crew_config.json only, so a genre cannot drift. Verify with a grep before claiming |
| Duplicate | none: nearest is DJ Light Green (shares the vocal-chop entry). Different era and tempo, no clash |

## Leave alone
genre_swing 54 (his pick, NOT FOUND in research), hat grammar, canon clap figures, space dry, drive/mix_sat/kick_dist, key and modes (sources disagree), kit tags, stamp lane (globally off), pre-existing snare grammar.

## Not buildable
Gunshots, Lil Jon shouts (shake-off era, left out). Specific Think/Sing Sing one-shots: library has none by name; the real-drum snare tags stand in (said in the old note).

## After the Code pass
`tools/identity_survival.py --genres --dj "Baltimore Club"`: any line phrase surviving under half the time gets fixed or reported. Update TRACKER.md (settings done), DECISIONS.md, genre_newbuild_status.json. Closed only by his ear: ask (clickable) whether he wants an old-vs-new audition. Do not render.
