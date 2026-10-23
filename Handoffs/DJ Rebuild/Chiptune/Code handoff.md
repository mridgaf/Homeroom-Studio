# Chiptune: Code handoff (settings NOT changed yet)

Do NOT render. Do NOT run the suite unless he asks for a render. One identity: Chiptune, in `genres_config.json`. Back up first (`genres_config.pre-chiptune-settings-<date>.json`). Edit the JSON as text inside that one block (own indent; a load/dump rewrite makes a huge diff).
New line and map are already in the config (`listen` + `_research_note` only; backup `genres_config.pre-chiptune-rebuild-2026-10-23.json`). Research: `research transcript.md` in this folder.

## ASSUMING (owner away, nothing asked)
1. ASSUMING the sound = NES / Famicom first (two squares, triangle, noise), with the Atari 2600 as the second chip. Not C64 SID, not Game Boy, not modern "fakebit" or chiptune-pop (Anamanaguchi, Chipzel are noted but not the target).
2. ASSUMING the existing owner answers of 2026-09-24 stay: chord_fallback [bell, pluck], dust 0.25 + allow_dirt, flavor_match, own_soundbank.
3. ASSUMING "mostly major" is NOT in the line: sources show both major and minor and give no ratio. The line says nothing about key.
4. ASSUMING "thin bright bleeps" and "nothing smooth anywhere" are carried over from the old line; research does not contradict them (triangle is "buzzing", 2600 is out of tune) but does not count them either.
5. ASSUMING all odds numbers, tempo, bass weights and key-mode shares below are Claude's picks (rule 8), not sourced.
6. ASSUMING DuckTales Moon credit = Tonomura (Wikipedia); SongBPM says Sakaguchi. Not used in settings.

## Engine fact the owner must know (chip sounds vs the no-machine-tones rule)
Chiptune's chord voice stays `synth` = sampled synth / pluck / pad out of his own banks. The engine's `chip` voice would use his 8-bit files, but he owns **0 chip files**, so it would fall to `tools/chip_synth.py`, a synthesized oscillator, which his 2026-09-23 rule bans (and "chip banned for all DJs", 2026-09-20). **Do not add `chip` to chord_source.** The genre's NES feel has to come from arpeggiated sampled synth/pluck/bell plus noise-style drum samples. If he ever adds real 8-bit files, then `chip` becomes possible; that is his call.

## New line
"8-bit game music: a fast, bubbling square-wave arpeggio standing in for chords the way the NES faked them, thin bright bleeps, a plain kick and snare under a ticking noise hat, a bass line that follows the kick, no reverb, and nothing smooth anywhere"

## Phrase -> setting
| Line phrase | Change in genres_config.json -> Chiptune | Source / who picked |
|---|---|---|
| "fast" | bpm 126 -> 150; add signature.tempo [128, 180] (check the key name other genres use, e.g. Acid Rap Bright `tempo`). Mario's 100 is left out of the pocket | tracks cluster 100 / 128-129 / 150 / 180 [CONFIRMED]; 150 = median; pocket = owner pick |
| "bubbling square-wave arpeggio standing in for chords" | none: chord_rhythm "arp", chords_default true already. Optional: chord arp_step 1 (16ths) if the engine offers it per genre, for a faster flicker; check chord_rhythm.py first, do not invent | arpeggios replace chords [CONFIRMED]; arp_step = Claude's pick, ask |
| "thin bright bleeps" | none (carried over; extras pool has `gamefx`/`blips`; stamp lane globally off) | carried, not researched |
| "a plain kick and snare" | none: kick grammar hits [2,4], snare backbeat 0.7 stays | not published [NOT FOUND]; leave |
| "ticking noise hat" | none: hat eighths 0.4 + sixteenths 0.35 = 75 percent steady; perc tags block/click/noise | noise-channel hats [CONFIRMED] |
| "a bass line that follows the kick" | signature.bass_grammar figures: kick 4, hold 2, octave 1 (the "grit"-like set), or set chord_family "grit". Currently `bright_funk` pushes funk + octave + ghost notes, which the research does not support. A bass synth/808 sample stands in only where the bass pool has nothing; say so in the report | triangle plain bass line [CONFIRMED]; weights = Claude's pick |
| "no reverb" | none (space dry) | NES has no reverb [CONFIRMED] |
| "nothing smooth anywhere" | none (dust 0.25, drive 1.1 stay) | carried over |

## Chord odds (genre rule: 100% research instruments)
Set chord_source: **synth 1.33, pluck 0.67** (instruments sum 2.0 so midi 0.667 stays at 25 percent of beats, the same share as now). ZERO (keep entries) for bell, choir, guitar, horns, organ, pad, piano, strings, wood. midi stays at 0.667 (about 25 percent of beats now and after; it plays exact MIDI notes and ignores the loops, report the share).
- synth/pluck: the nearest real sound to a pulse square; `synth` already covers synth+pluck+pad files. Square arpeggio [CONFIRMED]; the 2:1 split and the numbers are Claude's picks.
- bell stays reachable only through the existing chord_fallback [bell, pluck] (owner answer 2026-09-24), so it keeps a role at weight 0.
- Add a test asserting the zeros. Grep tests first: `grep -rn "Chiptune" tests/`. Known: tests/test_genres.py `test_chord_fallback_is_chiptune_only`; tests/test_crew.py lines ~449 and ~786 (allow_dirt, own_soundbank lists); tests/test_collab_genres.py line 16 (host in a collab set); tests/test_signature_words.py line 34 comments "chip ... Chiptune only" (read it before editing, it may pin chord_source).

## Key and mode (owner pick)
Now: major 3, lydian 1, mixolydian 1, no minor. Sources show both (Mario C major; Vampire Killer D/minor-sounding; DDRKirby Dm). Suggested: add minor 2 (leave lydian 1, mixolydian 0.5). Roots unchanged.

## Progressions (owner pick)
Plain triads fit best. Keep: uplifting, epic, vamp_i_VI, sparkle_add9, plain_chip_lift, plain_bounce_up. Candidates to drop as too jazz or gospel for an NES line (no source names them): gospel_walkup, plain_gospel_walk, plain_secondary, plain_dorian_vamp, dreamy (maj7s), sad_accepting. Ask before removing any. Do NOT use deep_* entries (jazz-out pass).

## Owner picks (ask clickable after the Code pass)
1. bpm 150 and pocket 128-180, or keep 126.
2. Add minor to the key mix, or leave major-only.
3. Bass: kick-following figures (recommended) or leave bright_funk.
4. Prune the gospel/jazz-sounding progressions, or leave.
5. Whether he wants an old-vs-new audition (closed only by his ear).

## Blind-spot table
| Check | Finding |
|---|---|
| Jazz coloring / deep loops | chord_color depth 0.0, lean {}; progressions list uses `plain_*` only (no deep_*). Clean. But sparkle_add9 / plain_gospel_walk / plain_secondary add colour the sources don't name (see Progressions) |
| MIDI chord share | midi 0.667 of 2.67 now (25 percent); stays 25 percent after; MIDI chords ignore the loops and instruments. Report only |
| Chord odds | PROBLEM: 9 instruments the sources never name hold 1.64 of 2.67 (61 percent). Fixed by the zeros above |
| Hats and percussion | eighths + sixteenths 75 percent: matches "ticking noise hat". Perc grammar sparse 0.6 / eighths 0.4: fine |
| Bass | PROBLEM: chord_family bright_funk vs a plain kick-following line |
| Percussion lane | kit perc tags block/click/noise match the noise channel; library has almost no true chip percussion (prior note), so words reach the nearest real files |
| Tempo | PROBLEM (mild): 126 is below the researched median 150; inside the 100-180 range |
| Daily drift | tools/evolution.py reads crew_config.json only; genres cannot drift. Verify with `grep -n "genres_config" tools/evolution.py` before claiming |
| Duplicate | none close; New Math shares the "8-bit square ripple" idea (crew.py line ~681), different tuning/harmony; keep them apart |

## Leave alone
genre_swing 50, space dry, kit tags (real filenames, verified 2026-09-24), own_soundbank, flavor_match, dust 0.25 + allow_dirt (his pick), chord_fallback [bell, pluck], extras pool, canon lanes, stamp lane (globally off), drive 1.1.

## Not buildable
- True NES/2600 noise-burst drums and pitched triangle-slide fills: the library has nearly no chip percussion; the nearest short/digital/909 one-shots stand in (said in the old note).
- The 2600's deliberately off-key tuning (`chip_tuning "atari"` exists only for the synthesized chip voice, which is banned).
- Echo from a second pulse channel: no sampled-synth echo figure exists; could be a later feature.

## After the Code pass
`tools/identity_survival.py --genres --dj "Chiptune"` (run unsandboxed, analysis only): any line phrase surviving under half the time gets fixed or reported. Update TRACKER.md (settings done), DECISIONS.md, genre_newbuild_status.json (stage `built`). Closed only by his ear. Do not render.
