# Crate Prophet: settings handoff for Code (Mac), 2026-10-23

Line is DONE and in `crew_config.json` (only `listen` and `_research_note` of Crate Prophet changed; backup `crew_config.pre-crate-prophet-rebuild-2026-10-23.json`; JSON-compared). Settings are NOT changed. **Do NOT render. Do NOT run the suite until the owner asks for a render.** Research: `research transcript.md` (23 sources).

## ASSUMING list (owner was away; correct any)
1. **ASSUMING producer = Pete Rock only.** Config says "Pete Rock / Madlib"; the old line (golden-era swing, SP-1200 era "90s") leans on Pete Rock. Madlib NOT researched. If the owner wants the Madlib side, it needs its own era pick and a second pass.
2. **ASSUMING era = 1991-94** (Mecca and the Soul Brother, The Main Ingredient, remixes). Not Soul Survivor 1998, not the live-band 2020 work.
3. **ASSUMING crew odds rule 50-50.** The weights below are the owner's pick, not sourced.
4. **ASSUMING carried-over claims stay**: 60% swing, snare LATE, congas and the conga-slap stamp, wow. Research is silent or leans against them (see map). Labeled "carried over" in the line.
5. **ASSUMING "hats on eighths" is worth a line word** (one source: hat locked to eighths in the Mecca era) and so needs the hat odds raised.

## New listen line
"New York 1991-94 sample-chop boom-bap, 87 to 102 bpm: warm and loose with 60% golden-era swing (carried over, not sourced); crunchy 12-bit drums under the heaviest vinyl bed plus record wow; hats on eighths; horns and piano chops over a walking bass line; snare sits LATE (era-driven, flagged, carried over...); loose congas, stamp is a conga slap on bars 4/8 (carried over). This is also the prototype that SKIPS sidechain (the 1-in-10 no-duck rule)"

## Phrase -> setting change
| Phrase | Setting | Change | Tag |
|---|---|---|---|
| 87 to 102 bpm | bpm, signature.tempo | bpm stays 92; ADD `signature.tempo` [[87,102]] (none now) | [CONFIRMED] |
| 60% swing | hat lane swing 60 | none (test pins 58-62) | NOT FOUND; carried over |
| crunchy 12-bit drums | dust 0.5 | none | [CONFIRMED] |
| heaviest vinyl + wow | vinyl -40, wow 0.3 | none | vinyl [UNSURE]; wow NOT FOUND |
| hats on eighths | grammar.hat modes | **eighths 0.38 -> 0.55**; scale the other 7 modes (sixteenths .16, sparse .16, offbeats .10, broken .08, answer .05, gallop .04, rolls32 .03) by 0.45/0.62 so the total stays 1.0 | [UNSURE] |
| horns and piano chops | chord_source | **odds change** below | [CONFIRMED] |
| walking bass | chord_family soul_jazz | none | [CONFIRMED] played melodic bass |
| snare LATE | lanes.snare offset 8 ms | none | NOT FOUND; carried over |
| congas, conga slap stamp | kit bongo/stamp | none | NOT FOUND; carried over |
| SKIPS sidechain | sidechain 0.0 | none (test pins) | owner rule |

## Changes (all numbers are the owner's pick unless stated)
1. **chord_source (crew 50-50).** Now: 9 instruments 0.559 each (horns, piano, bell, choir, guitar, organ, pad, pluck, strings, synth, wood = 11 x 0.559 = 6.149), loop 4.0, midi 3.383. Total 13.532. Research names **horns** (5+ sources) and **piano** (Ahmad Jamal, Rhodes) only. Proposal: horns **3.383**, piano **3.383** (= 50%); loop **4.0** (chopped records = the method; kept), midi **2.0** (was 3.383; MIDI chords ignore the vamps), the other 9 (bell, choir, guitar, organ, pad, pluck, strings, synth, wood) **0.085** each. Total unchanged, 13.532. Bell (Roy Ayers vibes) and choir (Harvey Scales vocal) are one-track [UNSURE], so they stay in the rest.
2. **Key mode:** now minor 2, major 1, lydian 1, mixolydian 1. Proposal: minor 3, major 2 (drop lydian and mixolydian: no research). Keys found: A#m x2, Em, D, B, C [UNSURE, tools disagree].
3. **Key roots:** now F 3, Bb 2, C 2, G 2. Researched: Bb (2 tracks), B (2), D, E, C. Proposal: keep Bb 2, C 2; add B 2, D 1, E 1; drop F and G? (F and G found nowhere; owner pick: keep them at 1 each instead of dropping).
4. **Tempo:** add `signature.tempo` [[87,102]] (centre 94-96). bpm 92 unchanged.
5. **Kick flavors.** 47% of kicks use the 808 flavor; research names no 808 or synth drum anywhere (break-sampled, layered kicks). Owner pick: cut 808 to 0.15 and the break/acoustic flavor to 0.85. Note kit tag "boom" is grouped with 808 in flavor_tags.
6. **Hats:** see table. Pete's own hats: eighths per one source.
7. **Extras:** pool has conga, shaker, vinyl/reverse/foley fx. Research names none of these for 1991-94. Leave; owner pick whether to cut the conga pool entry.

## Owner picks (clickable questions)
1. Madlib: add a second pass later with his own era, or drop the name from `built`?
2. Swing: keep 60 (carried over) or go straighter (one source says rigid hats)?
3. Congas and conga stamp: keep (carried over) or swap for the researched sounds (none found for 1991-94)?
4. Kick: cut the 808 share to 15%?
5. Odds numbers in change 1; midi 2.0 vs keep 3.383.
6. Snare LATE: keep? (NOT FOUND; house verdict is early.)

## Leave alone
- Reason: test-pinned or no source disagrees: sidechain 0, hat swing 58-62, space gated snare, backbeat_echo, drive 1.3, kick_dist 0, mix_sat 0, lanes, snare modes, kit tags (warm/dusty/vintage fits "gritty").
- Test lists: `tests/test_crew.py` (loose set, sidechain skips == ["Crate Prophet"], hat swing 58-62, allow_dirt, backbeat_echo) and `tests/test_pattern_gen.py` guest pool (reversefx). Grep tests for the name before editing.
- No gear names (SP-1200, S950) in the line.

## Blind-spot table
| Check | Where I looked | Finding |
|---|---|---|
| Jazz coloring / deep loops | chord_color depth 0.0; progressions list has `plain_*` only, no `deep_*` | clean after the jazz-out pass |
| MIDI chord share | midi 3.383 of 13.532 = 25% | high: MIDI chords ignore the vamps. Change 1 cuts it to 15% |
| Chord odds | 11 instruments equal 0.559; loop 4.0 | **Problem:** line names horns and piano, odds equal. Fix = change 1 |
| Hats and percussion | hat eighths 0.38 | **Problem:** under 50%. Fix = table row. Conga lane/pool: not in research |
| Bass | chord_family soul_jazz | matches (walking, melodic). Bass samples he owns: unchecked (Code); bass synths may stand in where no bass sample fits, say so |
| Percussion lane | kit bongo/stamp conga | line and research disagree (congas NOT FOUND) |
| Tempo | bpm 92, no signature.tempo | inside 87-102; add the range |
| Daily drift | tools/evolution.py ops: kick_zone, flavor_lean, backbeat_mode, ghosts, double_p, open_hats, guest_appetite, new_color, library_lean, chord_voice, progression_lean, key_taste, timekeeper_mode | evolution CAN move chord_source (chord_voice), key (key_taste), hat modes (timekeeper_mode) that this line pins. Decide whether to freeze those for this DJ |
| Duplicate | Otto Grit (Dilla), Cutz (Premier) | different producers; shared: "golden-era", swing zone near Cutz 51-54 vs 60 here; no overlap in instruments (horns/piano) |

## Code session steps
Part 4 of dj-rebuild: back up crew_config.json, edit as text (not load/dump), `tools/identity_survival.py --dj "Crate Prophet"` (unsandboxed), update TRACKER (settings done) and DECISIONS. No render; report numbers then ask about an old-vs-new audition.
