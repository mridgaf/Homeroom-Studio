# DJ Hint: settings handoff for Code (Mac), 2026-10-23

Line is DONE and in `legends_config.json` (only `listen` and `_research_note` changed; backup `legends_config.pre-dj-hint-2026-10-23.json`). Settings are NOT changed yet. **Do NOT render. Do NOT run the full suite before the owner asks for a render.**
Research: `research transcript.md` (14 sources; BPM each from ONE source, so [UNSURE]).
Skill: dj-rebuild Part 4. Owner rule 8 (not in the repo skill copy): instrument odds follow the research. Genres 100%, crew 50-50, Legends 75-25 (75% of chord_source/bass odds to instruments the research names, 25% to everything else). **The 75-25 numbers are the owner's pick, not sourced.** Bass synths may stand in where no bass sample fits.

## New listen line
"a mixtape DJ's beat on soul and funk records: a steady New York boom-bap bed with room to be talked over, hard short kick, hard snare and tight closed hats, strings and bells and pads on top, and the DJ's own scratch or siren landing at the end of the phrase; old jazz and blues records chopped in on some beats, plain instruments on the rest"

## Phrase -> setting (and the change it needs)
| Phrase | Setting | Change needed | Source tag |
|---|---|---|---|
| on soul and funk records | library.tags soul, funk | none (boom-bap 4, funk 2, soul 1 already) | [UNSURE] Wikipedia sample credits |
| steady NY boom-bap bed | snare backbeat 0.9, kick grammar | none | carried over, unsourced |
| room to be talked over | hat mode sparse 0.2 | none | [UNSURE] Hip Hop Scriptures |
| hard short kick / hard snare | kit tags hard, short / hard | none | [UNSURE] SonicScoop (general taste) |
| tight closed hats | kit hat tags closed, tight | none | carried over |
| strings and bells and pads | chord_source strings, bell, pad | **odds change below** | [UNSURE] Roland, one page |
| scratch or siren at phrase end | kit stamp fx scratch/siren | none | carried over, stand-in for a vocal drop |
| old jazz and blues records on some beats | chord_source loop (LoC) | **owner decision below** | carried over, NOT supported by research |
| plain instruments on the rest | chord_source families | **odds change below** | |

## Proposed settings changes (Claude's arithmetic on the owner's 75-25 rule; nothing sourced)
Chord_source today: loop 3 (Library of Congress, ~35% of beats), 11 instruments at 0.45 each, midi 0.6. Total weight 8.55.
- **Research-named (75%):** strings, bell, pad. 6.41 of 8.55 split three ways = **2.14 each**.
- **Everything else (25%):** piano, guitar, horns, organ, pluck, synth, wood, choir + loop + midi = 10 entries, 2.14 of 8.55 = **0.21 each**.
- That drops Library of Congress from about 35% of beats to about 2.5%. This is the big change, and the research does not support jazz/blues samples for Clue (see below). **Owner picks:** loop stays at 3 (old behaviour, ignores the 75-25 rule for loop) or loop goes into the 25% group.
- midi: the 2026-09-26 note keeps midi at ~10% of beats on all identities. If that still holds, midi keeps its share and the other nine split the rest. Owner picks.
- Bass: research names NO bass sound for Clue/Duro, so there is nothing to give 75%. Leave chord_family `soul_jazz` and the bass lanes alone. If bass samples are missing on the drive, a bass synth/sub may stand in; say so in the report.
- tempo: research 87 to 107 (one source), median 93. Current 86 to 95. Owner picks: widen to [86, 107] (adds I Like Control at 107), or keep.
- key roots: research keys F#, G#, D (one source, 5 tracks). Current roots F#, C#, G, G#, D#. Owner picks: add D, or keep.

## Owner's picks needed (the clickable questions)
1. Library of Congress share: keep at loop 3, or fold into the 25% group (about 2.5%).
2. Tempo range: keep 86-95 or widen to 86-107.
3. Add D to key roots, or keep.
4. midi share: keep ~10% or fold into the 25% group.

## Leave alone
- swing 53, lanes, grammar, mix, stamp, kit tags: no source says they are wrong; no source says they are right. Inherited from DJ Premium's preset.
- progressions list and chord_family: NOT FOUND, no change.
- Hard rules in the old line: none existed.
- Do not add gear names (JV-1080 etc.) to the line.

## Blind-spot table
| Check | Where I looked | Finding |
|---|---|---|
| Jazz coloring / deep loops | signature.chord_color depth 0.0; progressions list has no `deep_*` | clean after the 2026-10-23 pass |
| MIDI chord share | chord_source midi 0.6 of 8.55 (~7%) | low; MIDI chords replay the file's own progression, not the DJ's vamps |
| Chord odds | chord_source | **Problem:** line names strings/bells/pads but odds are equal (0.45). Fix = proposed odds above |
| Hats and percussion | grammar hat modes: eighths 0.6, sixteenths 0.2, sparse 0.2 | "tight closed hats" is backed (0.6 + 0.2 closed). "room to be talked over" rests on sparse 0.2 only; under the 50% bar if read as hats |
| Bass | chord_family soul_jazz (walk 3, kick 2, fifth 2, push 2, hold 1) | line says nothing about bass; no source; no mismatch |
| Percussion lane | extras pool scratch + rim; kit stamp scratch/siren | line and kit agree; scratch is not a sourced Clue sound |
| Tempo | bpm 92, tempo 86-95 | I Like Control (107) is outside; one source |
| Daily drift | `tools/evolution.py` reads `crew_config.json` only (docs say Legends are in their own file) | verify in code before saying Legends cannot drift |
| Duplicate | partner: DJ Premium ("late-90s/2000s horn-stab boom bap, 53% swing, hard tight kick, hard snare, closed tight hats, clean Pro Tools mix") | **Real overlap.** Same era and drum words. Hint's only differences: strings/bells/pads, scratch/siren stamp, LoC loops. The old note admitted this. Not a producer pair, but the owner may want them kept distinct |

## Code steps
1. Back up `legends_config.json` as `legends_config.pre-dj-hint-settings-<date>.json`. Edit the DJ Hint block as text (keep the file's indent).
2. Apply the owner's picks above. Add a test that only DJ Hint carries these odds. Grep `tests/test_signature.py` lines ~98-153: it asserts DJ Hint's LoC share is between 0.2 and 0.5. **If loop goes into the 25% group, that test fails; change it deliberately.**
3. Tags are carried over; run `tools/legend_newbuild.py --tags` (needs the drive) to confirm. No `dry` on a snare.
4. `tools/identity_survival.py --dj "DJ Hint" --legends` (unsandboxed; analysis only).
5. Update TRACKER.md (settings done), DECISIONS.md, `legend_newbuild_status.json` (stage `built`).
6. **No render.** Report numbers, then ask (clickable) about an old-vs-new audition.

## OWNER'S PICKS (answered 2026-10-23, clickable)
1. Library of Congress: **fold into the 25% group** (loop leaves weight 3). Change `tests/test_signature.py` (~line 153, DJ Hint share 0.2-0.5) on purpose.
2. Tempo: **widen to [86, 107]**.
3. Key roots: **add D**.
4. MIDI: **keep its current share (0.6).**

Final chord_source arithmetic (total kept at 8.55; Claude's arithmetic on the owner's 75-25 numbers): strings 2.14, bell 2.14, pad 2.14 (= 6.41, 75%); midi 0.6 (kept); the other 9 entries (loop, piano, guitar, horns, organ, pluck, synth, wood, choir) = 1.54 / 9 = **0.17 each**. LoC becomes about 2% of beats. Bass stays as is.
