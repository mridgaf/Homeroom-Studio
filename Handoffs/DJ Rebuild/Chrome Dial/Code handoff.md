# Chrome Dial: settings handoff for Code (Mac), 2026-10-23

Line is DONE and in `crew_config.json` (only `listen` and `_research_note` changed; backup `crew_config.pre-chrome-dial-rebuild-2026-10-23.json`; JSON-compared). Settings are NOT changed. **Do NOT render. Do NOT run the suite until the owner asks for a render.** Research: `research transcript.md` (24 sources).

## ASSUMING list (owner was away; correct any)
1. **ASSUMING era = 1996-2002** (Virginia, Swing Mob, ASR-10: Aaliyah, Missy, Ginuwine, Jay-Z). Era left for Timberline: **2006-08**, which its line already holds. No overlap.
2. **ASSUMING "completely" dropped** from "completely CLEAN" so the tool does not read a hard rule. Also, Douglass says the kick came from overloaded tape (one source), so a hard "clean" claim was not safe. Restore if he wants it hard.
3. **ASSUMING crew odds rule 50-50** (50% of chord_source to research-named instruments). The split numbers are the owner's pick, not sourced.
4. **ASSUMING "bar 6" and "stamp late in bars 4/8"** stay (carried over from the old line, research silent).

## New listen line
"Virginia 1996-2002 bounce: stuttering, sparse syncopation with silence as an instrument — bar 6 drops to almost nothing and answers bar 5; kick lands in odd spots, claps and snares answer; tabla, shaker and conga off-center as the rhythm; a plucked or flute-like lead over a rubbery bass, in minor or phrygian_dominant; clean (the grit is arrangement, not crush); stamp is an exotic perc hit late in bars 4/8"

## Phrase -> setting change
| Phrase | Setting | Change needed | Tag |
|---|---|---|---|
| stuttering sparse syncopation | kick grammar, lanes | none | [CONFIRMED] |
| silence, bar 6 | lane bar 6 | none | silence [CONFIRMED], bar 6 carried over |
| kick in odd spots | kick grammar | none | [CONFIRMED] |
| claps and snares answer | clap modes | none | [CONFIRMED] |
| tabla, shaker, conga | kit perc tags | none (bongo is a possible add, see picks) | tabla [CONFIRMED] |
| plucked / flute-like lead | chord_source | **odds change** | [CONFIRMED] wood, guitar, synth |
| rubbery bass | bass figures | **add funk figure** | [CONFIRMED] slap/snaky/rubbery |
| minor or phrygian_dominant | signature.key.mode | **change** | minor [CONFIRMED], phrygian [UNSURE] |
| (tempo, not in line) | bpm, signature.tempo | **change** | see below |
| clean | dust/vinyl/wow/kick_dist/mix_sat | none | carried over |

## Changes (all numbers are the owner's pick unless stated)
1. **chord_source (crew 50-50).** Research names, by source count: wood (tumbi, flute, koto, Egyptian flute), guitar (staccato, jazz, wah-wah, chopped guitar), synth (sitar, squelch, droning), pluck (sitar, plucked strings), strings (Sock It 2 Me, Is That Your Bitch; Complex only). Total weight now 9.665. Proposal: those five at **0.97 each** (4.83 = 50%); the other six (bell, choir, horns, organ, pad, piano) at **0.40 each** (2.42) and midi stays **2.416** (2.42). Total unchanged. Organ/piano/bell/horns are each named on one track only, so they stay in the rest. Owner may instead fold midi into the 25 percent; his 2026-09-26 midi note.
2. **Bass.** chord_family `grit` (kick 4, push 2, fifth 1, hold 1, octave 1) has no slap/funk figure. Proposal: `signature.bass_grammar` figures kick 3, push 2, funk 2, hold 1 (numbers unsourced). Bass synths may stand in where no bass sample fits; say so in the report.
3. **Key mode:** minor 3, lydian 1, mixolydian 1 -> minor 3, phrygian_dominant 1, phrygian 1. Lydian and mixolydian have no research behind them. NOTE: Timberline's note says phrygian_dominant "belongs to Chrome Dial" by the era split; it keeps weight 1 there. Owner pick whether to demote it in Timberline when that one is rebuilt.
4. **Key roots:** now D 2, A 2, E 2, C 1. Researched keys: G# (Pony, Rain), C# (Try Again), B / F# (OIAM), E (GUFO), A (AYTS). Proposal: add G# 2, C# 1, B 1; keep E, A; drop C? Keys are [UNSURE] (tools disagree). Owner pick: add G# and C# only.
5. **Tempo.** bpm 100 is above the researched range. Half-time-counted pocket: 69-92 (71, 61, 80, 69, 92, 92, 89). Proposal: bpm **90**, `signature.tempo` [[78, 95]]. Owner pick; widen down to 69 if he wants the slow end.
6. **Extras words.** The fx pool says zap/laser/glitch; research names baby, cricket, car screech, horse, rain as rhythm. In Code run `legend_newbuild.py --words fx` and `--words perc`, pick real library words (cricket, baby, animal, vocal/beatbox), confirm with `--tags`. Nearest real sound if missing, say so.
7. **Library tags** (rnb 3, garage 2, funk 2, electro 2): "garage" is UK garage (Wikipedia Timbaland says his breakbeats helped shape it) [UNSURE]; leave.

## Owner picks (clickable questions)
1. Hats: sources conflict (crickets in place of hats vs stuttering hats on OIAM). Keep none, or add a sparse/broken hat lane at low weight?
2. Swing: keep 50 straight, or 58 on one lane? Only source is one blog (Garn 58-62), no producer says it.
3. Kick: keep clean, or allow a small `kick_dist` (Douglass's overloaded tape, one source)? House clean-render rule strips master drive anyway.
4. Odds numbers in change 1 and 2, midi share.
5. Tempo: 78-95 or 69-95.

## Leave alone
- Reason: no source disagrees, no source confirms: lanes, clap grammar numbers, kick_flavors, sidechain, drive, space gated clap, backbeat_echo, dust/vinyl/wow.
- Do not add gear names (ASR-10, Triton) to the line.

## Blind-spot table
| Check | Where I looked | Finding |
|---|---|---|
| Jazz coloring / deep loops | chord_color depth 0.0; progressions have `plain_*` only, no `deep_*` | clean after the jazz-out pass |
| MIDI chord share | midi 2.416 of 9.665 = 25% | high: MIDI chords play the file's own progression and ignore the vamps. Owner pick above |
| Chord odds | equal 0.659 x 11 | **Problem:** line names wood/pluck/guitar but odds are equal. Fix = change 1 |
| Hats and percussion | no hat lane; perc tags tabla/shaker/conga | line claims no hat; research conflicts. Owner pick 1 |
| Bass | chord_family grit | line says rubbery; family has no funk figure. Fix = change 2. Bass samples he owns: unchecked (Code) |
| Percussion lane | kit perc tabla, shaker, conga | matches line |
| Tempo | bpm 100 | outside research (69-92). Fix = change 5 |
| Daily drift | tools/evolution.py ops kick_zone, backbeat_mode, ghosts, double_p, chord_voice, key_taste, progression_lean | evolution CAN move chord_source, key and kick shape that this line pins; chord_voice will erode the 50-50 odds over days. Decide whether to freeze those ops for this DJ |
| Duplicate | Timberline | different eras now: 2006-08 vs 1996-2002. Shared: gated clap space, drive 1.45, phrygian_dominant colour. Timberline not yet rebuilt |

## Code session steps
Part 4 of the dj-rebuild skill: back up crew_config.json, edit as text (not load/dump), tests list (test_crew.py `loose` set and allow_dirt), `tools/identity_survival.py --dj "Chrome Dial"` (run unsandboxed), update TRACKER (settings done) and DECISIONS. No render; report numbers then ask about an old-vs-new audition.
