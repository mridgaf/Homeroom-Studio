# Cutz: settings handoff for Code (Mac), 2026-10-23

Line is DONE and in `crew_config.json` (only `listen` and `_research_note` of Cutz changed; JSON-compared; backup `crew_config.pre-cutz-rebuild-2026-10-23.json`). Settings are NOT changed. **Do NOT render. Do NOT run the suite until the owner asks for a render.** Research: `research transcript.md` (21 pages, 8 tracks).

## ASSUMING list (owner was away; correct any)
1. **Era = Premier 1992-96.** Not my guess: DJ Premium's own note (2026-09-30) says the owner picked "Cutz keeps Premier's mid-90s, DJ Premium = late-90s/2000s". **Left for DJ Premium: 1998-2006** (Moment of Truth on; horn stabs, Pro Tools mix, Mathematics, So Ghetto, Full Clip). Premier says stabs came after the mid-90s jazz phase.
2. **ASSUMING crew odds rule 50-50.** The numbers below are the owner's pick, not sourced.
3. **ASSUMING piano and guitar are the instruments to name** (Chambers piano, Vic Juris and Byrd guitar). Organ (Illmatic samples) left out: I did not confirm Premier made those tracks. Keys he plays (post Step in the Arena) and bleeps/pads are one-source, so they stay in the "rest".
4. **ASSUMING carried over, NOT FOUND:** ghost snares, the scratch stamp on bars 4 and 8. Labeled "(placement carried over)" in the line.
5. **ASSUMING "chopped small with gaps" = chord_rhythm `comp`** (the engine has stab/arp/pad/comp; no source says arps).
6. **ASSUMING the old word "tight" is dropped** ("everything tight" vs Mode Audio "heavily swung" and SoS "behind the beat").

## New listen line
"New York 1992-96 jazz-sample boom bap, 83 to 98 bpm: 53% swing, a little behind the beat; hard kick and snare cut from old breaks, with ghost snares; piano and guitar loops chopped small with gaps; stamp is a scratched vocal hook closing bars 4 and 8 (placement carried over)"

Old line: "surgical: everything tight at 53% swing (his effective 51-54 zone), ghost snares, and his stamp, a scratch stab fill closing bars 4 and 8". No test pins the old wording (grep of tests/ finds only the name Cutz in generate/render calls); the line also lives in `tools/crew.py` lines 368-369 as a default for when the json is deleted: update it too.

## Phrase -> setting change
| Phrase | Setting | Change | Tag |
|---|---|---|---|
| 83 to 98 bpm | `signature.tempo`, bpm | ADD `signature.tempo` [83,98]; bpm 93 stays (inside) | 2 sources on 2 tracks; rest [UNSURE] |
| 53% swing | lane swing | none (53 in all four lanes) | [UNSURE] 51-54 is one blog |
| a little behind the beat | `lanes.snare` offset_ms | owner pick: 0 -> 4 ms (hat and kick stay 0). Check tests/test_crew.py for offset pins first | [CONFIRMED] feel (SoS + Mode Audio); number NOT FOUND |
| hard kick and snare cut from old breaks | kit tags, `kick_flavors` | tags already hard/crack/tight. **808 flavor 0.3 -> 0.1** (no source names an 808 for Premier; drums are break-based). Note "punch" is a misfire word; kit kick tag list has it | [CONFIRMED] |
| ghost snares | `grammar.snare.ghosts` [0,4] | none | NOT FOUND, carried over |
| piano and guitar loops | `chord_source` | odds below | [CONFIRMED] |
| chopped small with gaps | `signature.chord_rhythm` | "arp" -> "comp" (owner pick; also set `rest_p` default 0.18 stays) | [UNSURE] mapping |
| scratched vocal hook | kit `stamp` fx scratch, `extras.pool` cutfx, voxchops | none | [CONFIRMED] |
| closing bars 4 and 8 | `lanes.stamp` | none | NOT FOUND, carried over |

## Odds changes (crew 50-50; numbers are the owner's pick)
1. **chord_source.** Now: loop 3.5, midi 3.0, 11 families at 0.5 (total 12.0). Named by research: loop (the chopping method), piano, guitar. Proposal: loop **3.0**, piano **1.5**, guitar **1.0**, organ **0.5** (kept: one-source, so it stays small) = 6.0 (50%); the rest 6.0: midi **2.0** (was 3.0; MIDI chords ignore the vamps), horns/bell/choir/pad/pluck/strings/synth/wood **0.5** each (4.0). Horns stay low on purpose: they are DJ Premium's.
2. **Key roots.** Now C 2, D 2, G 2, A 1. Researched: A#/Bb (4 tracks), F# (2), F, D, C#. Proposal: A# **3**, F# **2**, F **1**, D **1**, C# **1** (drop C and G; owner pick whether to keep them at 1). Keys are [UNSURE] (one site; MC's Act disagrees with itself).
3. **Key mode.** Now minor 3, mixolydian 1, dorian 1. Proposal: minor **4**, dorian **1** (jazz), drop mixolydian (no source). Owner pick.
4. **Chord rhythm** arp -> comp (above). Leaves `pattern_tags` alone.
5. **Library** `library.p` 0.45, boom-bap tags: no change; owner pick whether to raise "breakbeat" since the drums are cut from breaks.

## Owner picks (clickable questions for the Code session)
1. Snare offset 4 ms: yes / no / smaller.
2. 808 share 0.3 -> 0.1: yes / 0 / keep.
3. chord_rhythm comp: yes / keep arp.
4. Odds in change 1 and midi 2.0: yes / change.
5. Drop mixolydian and C/G roots: yes / keep at 1.
6. Do you hear the swing as 53 or heavier ("heavily swung" per one source)?

## Leave alone
- sidechain 0.15, space gated snare, backbeat_echo, drive 1.4, kick_dist 0, mix_sat 0, mix_eq, lanes grids, snare modes, hat grammar (the line names no hat word), allow_dirt, dust 0.5 / vinyl -46 (era mix NOT FOUND; RouteNote's clean Pro Tools mix is DJ Premium's era), progressions (vamp_static_riff, vamp_i_iv7, dark_menacing and the plain_* set; no deep_*).
- No gear names (MPC60, S950) in the line.

## Blind-spot table
| Check | Where I looked | Finding |
|---|---|---|
| Jazz coloring / deep loops | chord_color depth 0.0, no deep_* progressions | clean |
| MIDI chord share | midi 3.0 of 12.0 = 25% | high; change 1 cuts to 17%. MIDI chords ignore the loops |
| Chord odds | 11 families equal at 0.5 | **Problem:** line names piano and guitar, odds equal. Fix = change 1 |
| Hats and percussion | hat modes eighths .33, sixteenths .25, offbeats .2 | no hat word in line; nothing to back |
| Bass | chord_family `grit` (kick-locked, kick 4) | research: bass follows the sample line, jazz double bass; no kick-lock claim. Line says no bass word. Owner pick: leave grit or move to soul_jazz (walk). Bass samples he owns: unchecked (Code); bass synths may stand in where none fits, say so |
| Percussion lane | extras pool: rim, shaker, scratch fx, vocal fx | scratch/vocal fx match the line; rim/shaker not sourced, leave |
| Tempo | bpm 93, no signature.tempo | inside 83-98; add range |
| Daily drift | evolution.py ops: kick_zone, flavor_lean, backbeat_mode, ghosts, double_p, open_hats, guest_appetite, new_color, library_lean, chord_voice, progression_lean, key_taste, timekeeper_mode | evolution CAN move chord_source (chord_voice), key (key_taste), ghosts, hat modes. The line pins ghosts and instruments. Decide whether to freeze `chord_voice` and `ghosts` for this DJ |
| Duplicate | DJ Premium (Legend): "late-90s/2000s horn-stab, Pro Tools clean mix, locked 53%" | eras differ by design. **Shared risk:** both say 53% swing (Premium "locked") and both use scratch stamp, vinyl-style kit, loop+midi. Differences to keep: Cutz = piano/guitar loops, comp, behind the beat, break-cut drums; Premium = horns 3, stab 5, clean. Do not give Cutz horns or stab figures |

## Code session steps
Part 4 of dj-rebuild: back up crew_config.json, edit as text (not load/dump; it uses indent 1 with compact arrays), update `tools/crew.py` default line, `tools/identity_survival.py --dj "Cutz"` (unsandboxed, analysis only), grep tests for Cutz (test_crew allow_dirt and offsets), update TRACKER (settings done) and DECISIONS. **Do not render.** Report numbers, then ask whether he wants an old-vs-new audition.
