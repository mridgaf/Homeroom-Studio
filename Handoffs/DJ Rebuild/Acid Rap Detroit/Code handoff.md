# Acid Rap Detroit: Code handoff (2026-10-23)

DO NOT RENDER. Do not run the test suite unless he asks for a render. One identity only: Acid Rap Detroit, in `genres_config.json`. Back up first (`genres_config.pre-acid-rap-detroit-settings-<date>.json`). Research: `research transcript.md` in this folder. Edit the JSON as text inside that one block (own indent; a load/dump rewrite makes a huge diff).

## ASSUMING (owner was away; every one labelled, correct any)
1. ASSUMING the era = Esham 1989-1994 (Boomin' Words from Hell, Judgement Day, KKKill the Fetus, Closed Casket). Dead Flowerz (1996) onward is less sample-based and more polished (AllMusic), so it is out.
2. ASSUMING "keyboard" (RapReviews, Wikipedia personnel) = a cheap synth patch first, piano second. No source says which sound. Organ, bells, strings, horns, choir, pads, plucks: NOT FOUND, so zero.
3. ASSUMING the old line's "a snare that cracks too loud" leaves the line: NOT FOUND in any source ("thin", "skinny" are the only snare words). The snare kit tags (grit, heavy, 707, 909...) are left alone until he decides.
4. ASSUMING "tape hiss and vinyl noise" leaves the line: tape is UNSURE (one blog says cassette), vinyl is NOT FOUND. "lo-fi" is [CONFIRMED] (4 sources) and replaces them. The dirt settings (dust 0.85, vinyl -40) still run; see owner pick 3.
5. ASSUMING 54% swing and the horror-tritone/villain/augmented loops stay (carried over, NOT FOUND in research).
6. ASSUMING instrument odds follow dj-rebuild rule 8 for genres: 100% research instruments, every unnamed one weight 0 (entries kept), midi untouched. The 4.2 / 2.8 / 1.4 numbers are Claude's pick (3:2:1), NOT sourced. The sum (8.4) equals the old 11 x 0.764, so midi stays about 25%.

## The new line
"raw lo-fi acid rap around 94 BPM: a cheap drum-machine kit, slowed metal bass lines, rock-guitar samples over a keyboard, minor and eerie, sparse and simple, 54% swing, nothing polished"
(already written to `listen` in the config, with the map in `_research_note`; no engine setting has been changed)

## Phrase -> setting change
| Line phrase | Change in genres_config.json -> Acid Rap Detroit | Source / who picked |
|---|---|---|
| "around 94 BPM" | bpm 98 -> 94. signature.tempo [92,104] -> [86,104] | median 93.5 of 33 canon listings, 27 of 33 inside 85-105 (songbpm; Judgement Day 97 on songbpm + Chordify). Centre is Claude's median, pocket [CONFIRMED]. Owner pick: apply or leave (both are inside the range) |
| "rock-guitar samples over a keyboard" | signature.chord_source: guitar 4.2, synth 2.8, piano 1.4. ZERO (keep the entry) for organ, bell, choir, horns, pad, pluck, strings, wood. midi stays 2.801. | guitar: 5 sources (AllMusic bio, Wikipedia x2, Metro Times, Axios). keyboard: RapReviews + Wikipedia personnel (Mike E. Clark). The NUMBERS and the synth>piano order are Claude's picks |
| "slowed metal bass lines" | no change. chord_family "dark" already = hold 3, kick 3, push 1, pulse 1 (slow, root-led). | RapReviews, AllMusic, Hip Hop Creme ([CONFIRMED], 3). See Bass below |
| "a cheap drum-machine kit" | no change to kit tags. kick lofi/dirt/grit/oldie, snare lofi_snare/lofispace/'snare [dirty]'/grit/heavy/707/909/80s/retro/oldie, hat closed/tite/lofi/dirt stay. | "cheap drum machine" [CONFIRMED] (RapReviews, AllMusic x2). Model NOT FOUND, so 707/909/80s are the old pass's reading |
| "raw lo-fi", "nothing polished" | no change: allow_dirt true, own_soundbank true, mix_sat, drive, kick_dist stay. dust/vinyl/wow: owner pick 3 | lo-fi [CONFIRMED] (AllMusic, Hip Hop Creme, RapReviews, AllMusic bio) |
| "minor and eerie" | no change to modes (minor 3, harmonic_minor 2) or progressions. Roots: owner pick 2. | eerie/dark [CONFIRMED] (AllMusic). Minor [UNSURE] (one Chordify read, F# minor) |
| "sparse and simple" | no change: density sparse, snare backbeat 0.7, hat eighths 0.4 + sparse 0.3 | "simple" (RapReviews), "skeletal/minimal" (Hip Hop Creme), "primitive" (AllMusic) [CONFIRMED] |
| "54% swing" | no change | carried over, NOT FOUND, owner's pick |
| "acid rap" | n/a | the name; Esham's own word (Wikipedia, Metro Times) |

## Research instruments (who gets odds, and why)
- guitar 4.2: rock samples (Black Sabbath "War Pigs", Black Flag "Rise Above"); the sample material is guitar riffs. [CONFIRMED]
- synth 2.8: "keyboard" on RapReviews and Wikipedia personnel. Engine "synth" = sampled synth/pluck/pad group (instrument_sampler VOICES). [keyboard CONFIRMED, synth UNSURE]
- piano 1.4: Esham studied piano (Wikipedia). Smallest share. [UNSURE]
- midi 2.801 unchanged (about 25%): MIDI chords replay the file's own notes and chords; midi voices include bell, pluck and pad, which the research does not name (MIDI_VOICES in instrument_sampler.py). Owner pick 4.
- ZERO: organ (1 library file anyway), bell, choir (2 samples, backed by pad), horns, pad, pluck, strings, wood. Nothing in 20 pages ties them to Esham's 1989-94 records.
- "loop" source: not added. It draws any in-key loop, not rock loops (same reason as 2026-09-24).
- Bass synths may stand in where no bass sample fits (rule 8). Research says bass GUITAR; the library has no verified bass-guitar bucket (guitar group = 305 samples, mixed). Check on the Mac with `tools/legend_newbuild.py --words bass`. If none fits, the sub/808 or a bass synth stands in; say so, do not fake the word.

## Owner picks (ask clickable)
1. bpm 94 and tempo 86-104: apply / leave (both inside the range).
2. Key roots. Now A, C, D, E. Spotify's reads of the canon: F# about 11 of 33, G about 8, E about 5, A# 5, C# 5. Options: add F# and G (e.g. F# 3, G 2, E 2, A 1) / leave as is. Reads are off tape-era masters and give no mode, so UNSURE.
3. Dirt level. Line now says only "lo-fi". dust 0.85 and vinyl -40 are NOT FOUND (vinyl) / UNSURE (tape). Options: keep / halve dust and set vinyl to off, keep wow, mix_sat, drive, kick_dist.
4. MIDI share about 25%: keep / lower midi to 1.4 (about 14%).
5. Snare tags: keep the grit/heavy ("cracks too loud") tags / take heavy out. Research says only "thin" production, nothing about loud.
6. Odds numbers 4.2 / 2.8 / 1.4: keep or edit.

## Exception rules and tests
- Add a test: Acid Rap Detroit's chord_source weight is 0 for organ, bell, choir, horns, pad, pluck, strings, wood, and only guitar/synth/piano/midi are above 0 (genre rule; grep `tests/` first: `grep -rn "Acid Rap Detroit" tests/`). Existing: tests/test_crew.py ~448 (allow_dirt dict has Acid Rap Detroit True; update only if pick 3 turns dirt off) and ~786 (own_soundbank list). Neither reads the listen wording.
- `tools/genres.py` ~349 still holds the OLD defaults and old listen text. The JSON config is what plays; only matters if a regenerate-from-defaults path exists.

## Blind-spot table
| Check | Where | Result |
|---|---|---|
| Jazz coloring / deep loops | chord_color | depth 0, lean {}; no deep_* in progressions: jazz-out applied, OK |
| MIDI share | chord_source midi 2.801 of 11.2 | 25%. MIDI chords replay the file, voices include bell/pluck/pad. Pick 4 |
| Chord odds | chord_source | equal 0.764 each: guitar only 6.8% of odds, line says "rock-guitar samples". Needs the change above |
| Hats and percussion | grammar hat modes | eighths 0.4, sparse 0.3, offbeats 0.2, broken 0.1; "sparse and simple" is backed (density sparse + 70% eighths/sparse). Line names no hat or percussion; extras pool (fx dark/noise/reverse, perc block/tamb) is unsourced, left |
| Bass | chord_family dark | fits "slowed ... bass lines" (hold/kick). Bass guitar sample may not exist; see above |
| Percussion lane | kit stamp (vocal/scream/dark/noise) + extras | line silent; stamp lane globally off since 2026-08-01; leave |
| Tempo | bpm 98, 92-104 | inside 85-105; centre 94. Pick 1 |
| Daily drift | tools/evolution.py | grep: reads crew_config.json only (header line 8, line 365), so a genre cannot drift. Not traced further |
| Duplicate | Acid Rap Bright; Horror Rap | Bright is 78-85, major-leaning, horns/piano, clean: no overlap. Horror Rap (92 BPM, 81-96; "heavy dusty kick", tape hiss, long reverb, detuned bell) is close in tempo and darkness. Detroit now says guitar + keyboard, lo-fi, no reverb and no bells; keep Horror Rap's rebuild (Gravediggaz/Lynch) on bells, reverb and hiss so the two stay apart |

## Not buildable (no samples or no rule)
Tape-speed or cassette-wobble sourced treatment (wow 0.15 exists but unsourced), a named drum-machine voicing, 23-songs-in-72-minutes song length, sung/shouted hooks. Say so; do not fake with wrong words.

## Leave alone
kit tags, kick_flavors, genre_swing 54, grammar, space room, sidechain, drive, kick_dist, mix_sat, extras, library tags (lofi 3, rock 2, boom-bap 2 are fine), progressions, mode weights, key/mode unless pick 2.

## After
`tools/identity_survival.py --genres --dj "Acid Rap Detroit"` (run unsandboxed; it writes `~/.reason_voice/pattern_history.json`; analysis only). Expect "rock-guitar samples" to rise from about 7% to about 37% of chord picks by weight. Then TRACKER.md (settings done), DECISIONS.md, genre_newbuild_status.json (stage `built`, keep old verdict in notes). Closed only by his ear; ask clickable whether he wants an old-vs-new audition. Do not render until he says so.
