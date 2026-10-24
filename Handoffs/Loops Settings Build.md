# Loops side: settings build (from the 2026-10-24 vocabulary rethink)

**Status:** BUILT 2026-10-24 (see DECISIONS.md "Loops side settings: built"). Changes from the build: one strongest mood row instead of add-up; swing = jazz in loop titles only; partynextdoor dropped. Nothing rendered.
Mirror of the entry "Loops-side vocabulary rethink" in DECISIONS.md. House rules: ask clickable
questions, no guessing, never render unless he asks, tests before beats.

## Where things are (read these first)
- `tools/loop_lanes.py`: `pick_state`, `scan_all`, `WORDS` (lane buckets), `LANE5`.
- `tools/sample_library.py` `loops_scored()`: exact filename-word match only today (no synonyms, no listen line).
- `tools/loop_mode.py` `pick_loop`: weighted lean by `fit_score`; `apply_dj_finish` is an UNUSED duplicate.
- `tools/beat_machine.py` `_pick_loop_bed` (~3510) feeds `crew.render_crew_beat(loop_bufs=...)`.
- `tools/crew.py` ~1872: `clean_mix = house clean_renders AND allow_dirt is not True`; vinyl/wow/mix_sat/dust sit behind it (~2584-2658); drive forced 0.7 when clean.
- Loop counts (last saved scan, `~/.reason_voice/loop_lanes.json`): drums 1870, lead 3689, chords 483, bass 440, perc 278, vocals 182, fx 115.

## Rulings
1. **What steers picks:** listen line + library tags.
2. **Title reading:** file name + every folder up to the pack. Drop pack names (Looperman, Cymatics, Bizkel, Cobra, Oracle, Library of Congress...), key tags (CMAJ...) and BPM tags from the vocabulary.
3. **Vocabulary:** extend with style/genre/era/mood groups from his real titles (below). Existing sound-word families (grit, warm, punch, deep...) stay. Texture words (clean, analog, hard, soft, deep, dirty, dry, wet) join existing families.
4. **Lead split** into keys, guitar, strings, horns, synth/arp, other. By title words that gives synth/arp 558, keys 351, guitar 283, horns 103, strings 98, **other 2348** (no instrument word, usually just "MELODY n"). Untyped = "other", steered by folder style words. No audio analysis. 51 loops hit two types.
5. **Mood/texture/era words** steer the PICK and the FINISH.
6. **Artist words:** drake and partynextdoor = moody rnb/trap; carti, playboi = dark trap; juice, wrld = melodic emo trap. Only four were ruled by name (drake, carti, playboi, juice); partynextdoor and wrld are my additions to those groups, confirm with him. Other artist words below the top 120 are unlisted.
7. **Loop beats are FULLY clean:** no vinyl, dust, wow, saturation or 808 grit for ANY identity. `allow_dirt` (True and "low") is ignored on loops-only beats, and so is the post-hoc "effects on" swap (`beat_machine.py` ~4589-4595). One rule in the loops path. Today 15 identities (4 crew, 3 legends, 8 genres) run the full dirt chain on loop beats, plus 4 "low".
8. **Mood words move EQ and glue ONLY on loops.** Saturation and drive columns dropped (clean pins them anyway). Several matching words add up, capped. Values are untuned draft v1, judged by ear only when he asks for a render.
9. **Settings home:** separate `loops_config.json`, keyed by identity name; the `listen` line is read from the existing config (no copy). Evolution rewrites crew_config.json daily, so the Loops file stays out of it.

## Word groups (counts = loops whose title has the word; approved as drafted)
| Group | Words |
|---|---|
| jazz | jazz 473, jazzy 12, swing 79 |
| blues | blues 358 |
| hip hop | hip 205, hop 201, hiphop 8, rap 35, bap 30, boom 32, break/breaks 465 |
| trap | trap 341, drill 27, rage 10, yeat 25, lil 32 |
| dark trap | carti 42, playboi 40 |
| moody rnb/trap | drake 69, partynextdoor 23 |
| melodic emo trap | juice 44, wrld 10 |
| rnb / soul | rnb 142, soul 19, smooth 14 |
| classical | classical 202, opera 235, choir 20, ensemble 12, cinematic 13 |
| electronic | techno 107, ebm 94, acid 67, house 26, edm 15, trance 11, dubstep 36, electro 8, electronic 46, industrial 32 |
| ambient / dreamy | ambient 67, dreamy 12, dream 14, ethereal 17, cloud 20, cosmic 13, galaxy 19, space 34, spacey 39, astral 11 |
| dark / horror | dark 83, horror 81, creepy 22, terror 8, doomed 8, weird 9 |
| lofi / chill | lofi 123, chill 27, nostalgic 21, old 18, slow 18 |
| sad / emotional | sad 25, emotional 29, lonely 8, memories 8 |
| happy / bright | happy 15, bright 11, party 12, funky 11 |
| world | japanese 38, eastern 31, afro 16, afrobeat 25, brazilian 10, spanish 9, reggaeton 12 |
| psychedelic | psychedelic 27, trippy 13 |
| pop / indie / rock | pop 79, synthpop 38, indie 77, rock 42, punk 15, hyperpop 20 |
| funk / disco | funk 61, disco 8 |
Ruled: swing = jazz; boom = hip hop (boom bap), NOT the 808 family, inside loop titles; break/breaks = hip hop; theory = ignored. "warm/soft" get no finish row (pick-steering only).

## Mood-to-finish table, draft v1 (EQ and glue ONLY on loops)
| Word group | EQ | Glue |
|---|---|---|
| lofi / chill | highs -3, low +1 | gentle |
| dark / horror | highs -2, low +2 | medium |
| ambient / dreamy | highs -1, mids -1 | very gentle |
| sad / emotional | highs -1, mids +1 | gentle |
| happy / bright | highs +2 | gentle |
| trap / dark trap | low +2, highs +1 | tight |
| hip hop | low +1, mids +1 | tight |
| jazz / blues / classical | highs -1 | very gentle |
| rnb / soul | low +1, highs -1 | gentle |
| electronic | low +1, highs +2 | tight |
| funk/disco/pop/indie/rock | highs +1 | medium |
| world / psychedelic | none | gentle |
| clean (existing family) | none | gentle |
| hard / crunch / distort (existing) | low +1 | tight |
(Dropped for loops: the saturation and drive values from the original draft.) "gentle/medium/tight" still need mapping to real `glue_compress` numbers; EQ goes through `audio_engine.eq3`.

## Open
- Other artist words below the top 120; confirm partynextdoor/wrld grouping.
- Map glue words to numbers; check `glue_compress` really runs on loop beats (it is outside the clean gate, ~crew.py 2597).
- Make `loops_config.json` shape and a test that loops-only beats ignore `allow_dirt` (and that `tests/test_loop_mode_boundary.py` still passes: loop picking must stay out of arrangement code).
- Full suite once BEFORE the first render, alone.
