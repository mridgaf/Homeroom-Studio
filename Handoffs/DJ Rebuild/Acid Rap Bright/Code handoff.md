# Acid Rap Bright: Code handoff (2026-10-23)

Do NOT render. Do NOT run the suite unless he asks for a render. One identity only: Acid Rap Bright, in `genres_config.json`. Back up first (`genres_config.pre-acid-rap-bright-settings-<date>.json`). Research: `research transcript.md` in this folder.

## ASSUMING (owner was away; every one is labelled, correct any)
1. ASSUMING the lineage = Chance the Rapper's *Acid Rap* (2013) and its Chicago circle (CottonTale, Nate Fox, Cam O'bi, Ponce, Nico Segal). The tracker said "the 2013 Acid Rap lineage". Surf (2015) not researched.
2. ASSUMING "jazzy, gospel-leaning" is kept as "acid-jazz" only. Acid-jazz is [CONFIRMED]. Gospel is only sourced to vocal arrangements the engine can't play, so "gospel" left the line (gap, not dropped from the identity).
3. ASSUMING "major-key" leaves the line: the keys on record are not published as major/minor (UNSURE). The mode weights (major 3, lydian 1, mixolydian 1) stay as carried over. Your call below.
4. ASSUMING "hand percussion everywhere" leaves the line (NOT FOUND in any source). Percussion settings stay as they are. Your call below.
5. ASSUMING instrument odds follow dj-rebuild rule 8 for genres: 100% research instruments, others weight 0 (entries kept). Every odds number below is Claude's pick, NOT sourced.

## Settings the new line needs
Line: "bright acid-jazz hip hop around 80 BPM: a light natural kick, a snappy clap-and-snare stack, piano and organ chords under live horns, soul-sample chops, 58% swing, live-room air and not one grain of dust"

| Line phrase | Change in genres_config.json -> Acid Rap Bright | Source / who picked |
|---|---|---|
| "piano and organ chords under live horns", "soul-sample chops" | signature.chord_source: piano 3, horns 3, organ 1.5, guitar 1.5, loop 2, synth 0.5, choir 0.5. ZERO (keep the entry) for bell, pad, pluck, strings, wood. midi unchanged at 3.732 (about 24% after the change; was 25%). | Which instruments is sourced: horns 4 sources, keys CottonTale/Chance/Andscape, organ Goransson + AllMusic, guitar Goransson + Betty Wright sample, loops Fox. synth: one source (UNSURE). choir: sung stacks only (UNSURE). The NUMBERS are Claude's picks |
| "around 80 BPM" | bpm 82 -> 80 (optional, owner pick). signature.tempo [78,84] -> [76,85] (optional) | 78 (x2), 80, 85 from songbpm/songdata. 82 is already inside; leave if he does not care |
| "acid-jazz" | no change. progressions already hold nostalgic_jazz, plain_major_ii_v, gospel_walkup, soul_turnaround, mixo_soul_climb | sourced; the weights are the old pass's, left |
| "light natural kick", "snappy clap-and-snare stack", "58% swing", "live-room air", "not one grain of dust" | no change | carried over; research silent or weak (see map in `_research_note`) |

## Research instruments (who gets odds, and why)
- horns: Floyd (trombone), Segal (trumpet), DJBooth, Complex 10-year. [CONFIRMED]
- piano: CottonTale on keys, "sick jazz pianist" (Chance), Andscape. [CONFIRMED]. NOT Rhodes (only in a 2020 solo video).
- organ: Goransson "guitar and organ"; AllMusic "church organ swells". [CONFIRMED]. Library organ = 146 samples (2026-09-28).
- guitar: Goransson; Betty Wright sample. [CONFIRMED it exists, share unknown]
- loop: Fox chops Hutch/Wright/Hathaway. [CONFIRMED]
- synth (0.5): "synthesizer swirls", one source. choir (0.5): six-voice stacks on Good Ass Intro; the engine has 2 choir samples and backs them with pad.
- Zero, no source: bell, pad (only via choir backup), pluck, strings, wood.
- Bass synths may stand in where no bass sample fits (rule 8); research names no bass at all (NOT FOUND), so bass is left alone.

## Owner picks (ask clickable)
1. Key: put "major-key" back? (sources: unknown; the 2026-09-24 count was 4 major / 4 minor.) Options: keep modes as now / mix in minor / leave.
2. Percussion: keep the bongo lane and 75% extras (tamb, congas, shaker, woods) although no source backs them? Options: keep / lower extras p to 0.4.
3. bpm 80 and tempo 76-85, yes/no.
4. MIDI chords: midi_voices include bell, pluck and pad, which the research does not name (MIDI_VOICES in instrument_sampler). Midi stays about 24% of chord odds. Options: keep / lower midi to 1.5 (about 11%).
5. Odds numbers above are Claude's. Keep or edit.

## Exception rules and tests
- Add a test asserting Acid Rap Bright's chord_source has weight 0 on bell, pad, pluck, strings, wood (genre rule). Grep first: `grep -rn "Acid Rap Bright" tests/` (test_crew.py ~785 own_soundbank allow-list, test_audio_quality.py ~102 space room). Neither depends on the listen wording.
- `tools/genres.py` line ~387 still holds the OLD defaults and the old listen line (bpm 88, old kit tags). The JSON config is what plays; tell him only if a regenerate-from-defaults path exists.
- Edit the JSON as text inside that block (genres_config.json has its own indent).

## Blind-spot table
| Check | Where | Result |
|---|---|---|
| Jazz coloring / deep loops | chord_color | depth 0, no deep_* in progressions: jazz-out applied, OK |
| MIDI share | chord_source midi 3.732 of 14.93 = 25% | high; MIDI chords replay the file's own progression and voices include bell/pluck/pad. Owner pick 4 |
| Chord odds | chord_source | equal 0.836 each now, so "piano/organ/horns" are NOT favoured (5.6% each). Needs the change above |
| Hats and percussion | grammar hat modes, bongo | eighths .3, sixteenths .25, offbeats .2; the line no longer names hats. Percussion is unbacked (owner pick 2) |
| Bass | chord_family dreamy (hold/push/fifth/walk) | research silent. Leave. Optional later: soul_jazz family (walk/kick/fifth/push) fits "jazz" but is unsourced |
| Percussion lane | kit bongo + extras | line no longer says it; leave |
| Tempo | bpm 82, 78-84 | inside 78-85 |
| Daily drift | tools/evolution.py | reads crew_config.json only (header + line 365), so a genre cannot drift. Not traced further this session |
| Duplicate | Acid Rap Detroit | different era (Esham 1989), dusty, minor. Chiptune/others no overlap. Wonky shares "jazz-keys" nothing. OK |

## Not buildable (no samples or no rule)
Live horn solos, sung gospel backing vocals, the 30 s silence between Pusha Man and Paranoia, tape looping, juke footwork at double time. Say so; do not fake with wrong words.

## Leave alone
kit tags, kick_flavors, swing 58, grammar, space room, sidechain, drive, dust/vinyl/wow, progressions, key/mode weights, library tags, extras.

## After
`tools/identity_survival.py --genres --dj "Acid Rap Bright"`: expect "piano and organ chords under live horns" to rise after the odds change (today ~17% for those three combined, by weight). Then TRACKER.md (settings done), DECISIONS.md, genre_newbuild_status.json. Closed only by his ear; ask clickable whether he wants an old-vs-new audition.
