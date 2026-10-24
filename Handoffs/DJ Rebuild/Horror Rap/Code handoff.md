# Horror Rap: Code handoff (2026-10-23) — LINE DONE, SETTINGS NOT CHANGED

Do NOT render. Do NOT run the full suite unless he asks for a render. One identity only: Horror Rap, in `genres_config.json`. Back up first (`genres_config.pre-horror-rap-settings-<date>.json`). Research: `research transcript.md` in this folder.
The genre was HEARD and KEPT on 2026-09-28 (`genre_newbuild_status.json`: stage confirmed). Changing the odds below changes what he heard. Offer an old-vs-new audition afterwards; never render on your own.

## ASSUMING (every one labelled, correct any)
1. ASSUMING the era = 1991-95 horrorcore in three strands: Geto Boys (Houston, 1991), Gravediggaz (New York, 1994), Brotha Lynch Hung (Sacramento, 1995). Esham is Acid Rap Detroit, Three 6 is Memphis, G-funk is its own genre.
2. ASSUMING the line keeps 92 BPM (Gravediggaz median 92, Geto Boys 94 and 85). Brotha Lynch reads slower (69-85); see pick 1.
3. ASSUMING dropped words stay dropped while their settings stay put: reverb ("drowning in a long dark reverb"), bells ("detuned bell and chime colors"), "tape hiss", "hard snare". None were found in any source.
4. ASSUMING instrument odds follow dj-rebuild rule 12 for genres: 100% research instruments, zero (entry kept) for the rest. Every odds number below is Claude's pick, NOT sourced.

## New line (already written to `genres_config.json`, only `listen` and `_research_note` changed, JSON-compared)
"mid-90s horrorcore around 92 BPM: dark minor piano and guitar sample loops, dusty drums over a deep bass, sparse and minimal, vinyl scratches and cassette grit, vocal samples dropped in"
Old line: "mid-90s boom bap turned to face the wall: a heavy dusty kick, a hard snare drowning in a long dark reverb, detuned bell and chime colors, tape hiss, and space left deliberately empty so it feels like something's in it"

## Settings the new line needs
| Line phrase | Change in genres_config.json -> Horror Rap | Source / who picked |
|---|---|---|
| "piano and guitar sample loops" | signature.chord_source: piano 3, guitar 2.5, loop 2, synth 1, organ 1, choir 1. ZERO (keep the entry) for bell, pad, pluck, strings, wood, horns. midi: see pick 6. | piano: 4 tracks, 3 publishers. guitar: Defective Trip, MPTOM, Mommy. synth/organ/choir: single-source (UNSURE). Numbers are Claude's |
| "around 92 BPM" | no change if pick 1 = keep. Else see pick 1. | Gravediggaz median 92; Lynch 69-85 |
| "dark minor" | no change (mode minor 3 / harmonic_minor 2; dark progressions). See pick 5 for the mode. | minor CONFIRMED; harmonic minor NOT FOUND |
| "dusty drums over a deep bass" | no change (kit dusty tags, kick_flavors 808 deep/dark/sub, chord_family dark hold/kick) | dusty CONFIRMED (RZA tracks); deep bass UNSURE (one source) |
| "sparse and minimal" | no change (density sparse) | UNSURE, carried over |
| "vinyl scratches and cassette grit" | no change (vinyl -42, wow 0.12, dust 0.7, allow_dirt) | UNSURE; numbers are the old pass's |
| "vocal samples dropped in" | no change (stamp tags vocal/dark/reverse) | vocal CONFIRMED |

## Owner picks (ask clickable)
1. **Tempo.** (a) keep bpm 92, pocket 81-96 (b) keep bpm 92, widen the pocket to 70-102 so Lynch-speed beats can happen (c) bpm 88, pocket 69-102 (median of all 18 tracks).
2. **Bells.** The bell lane, kit bell and bell extras have no source. (a) keep (he heard and kept them) (b) remove the bell lane/kit/extras. The line already omits bells.
3. **Reverb.** `space: washed` on the snare has no source (the old note misread "washed in minor chords", a phrase about chords). (a) keep (b) room (c) dry. Changing it means editing `tests/test_audio_quality.py` ~line 677 (`test_a_washed_preset_gets_a_real_wet_space`, four genres).
4. **Key roots.** C and A are not on record; G# and C# are. (a) keep E3 Bb2 F#1 C1 A1 (b) E3 Bb2 F#1 G#1 C#1.
5. **Mode.** (a) keep minor 3 / harmonic_minor 2 (b) minor only (harmonic minor NOT FOUND).
6. **MIDI chord share.** midi 2.9 is about 25% of chord odds; MIDI chords replay the file's own progression and its voices include bell, pluck and pad. (a) keep 2.9 (about 22% after the odds above) (b) lower to 1.5 (about 12%).
7. The odds numbers in the table are Claude's. Keep or edit.

## Exception rules and tests
- Add a test asserting Horror Rap's chord_source has weight 0 on bell, pad, pluck, strings, wood, horns and positive weight on piano and guitar, and that no other genre carries exactly this set (scope the exception to this one identity). Grep first: `grep -rn "Horror Rap" tests/`. Hits: `tests/test_audio_quality.py` ~682 (washed, four genres), `tests/test_crew.py` ~432 (docstring citing EW), ~451 (allow_dirt dict, Horror Rap True), ~787 (own_soundbank allow-list). None depend on the listen wording. `test_weights_are_positive_numbers` was already relaxed for chord_source in the Acid Rap Bright pass.
- `tests/test_crew.py` ~432: the docstring says dirt is sourced to EW's "washed in minor chords". Reword to "dusty drums" (Albumism + Time Is Illmatic on Graveyard Chamber) in the same pass; the value stays True.
- `tools/genres.py` ~438 (`"Horror Rap": dict(`) and ~1182 hold the OLD defaults and old listen line. The JSON config is what plays. Tell him only if a regenerate-from-defaults path exists.
- Edit the JSON as text inside that block (genres_config.json has its own indent; a load/dump rewrite makes a huge diff).

## Blind-spot table
| Check | Where | Result |
|---|---|---|
| Jazz coloring / deep loops | signature.chord_color; progressions | depth 0, lean {}; no deep_* in progressions: jazz-out applied, OK |
| MIDI share | chord_source midi 2.9 of 11.6 | 25%, high. Pick 6 |
| Chord odds | chord_source | equal 0.7 on 11 instruments + loop 1, so piano/guitar get about 6% each. Needs the change above |
| Hats and percussion | grammar hat modes eighths .35 / sparse .35 / offbeats .2 / broken .1; bell lane | the line no longer names hats or bells. Bell lane unbacked (pick 2) |
| Bass | chord_family dark (hold/kick) | fits the one source (held 808 line) |
| Percussion lane | kit bell | unbacked, pick 2 |
| Tempo | bpm 92, signature.tempo 81-96 | inside Gravediggaz/Geto; Lynch under it. Pick 1 |
| Daily drift | tools/evolution.py | reads crew_config.json only (header line 8, line 365, line 389), so a genre cannot drift |
| Duplicate | Acid Rap Detroit (guitar-led, minor, 94 BPM, Esham); Memphis (140); G-Funk (synth-led) | Detroit shares guitar and minor. Horror Rap leads with piano, so it stays different. Tempo: Detroit 98 (92-104) vs Horror Rap 92 (81-96); pick 1 (b) or (c) widens Horror Rap down to 70, not up toward Detroit |

## Not buildable (no samples or no rule)
Skits and courtroom scenes (Diary), spoken film samples as a story, rain sounds (Bang Your Head), RZA's off-grid drums, a band jam recorded to tape. Say so; do not fake with wrong words.

## Leave alone
kit tags, kick_flavors, lanes, swing 53, grammar, sidechain, drive, kick_dist, mix_sat, progressions, library tags, extras (unless pick 2), key roots and mode (unless picks 4 and 5), space (unless pick 3).

## After
`tools/identity_survival.py --genres --dj "Horror Rap"` (run unsandboxed; it writes `~/.reason_voice/pattern_history.json`; analysis only, no render). Expect "piano and guitar sample loops" to rise after the odds change (today about 12% for both by weight). Then TRACKER.md (settings done), DECISIONS.md, `genre_newbuild_status.json` (set stage `built`, keep the old verdict in notes). Closed only by his ear; ask clickable whether he wants an old-vs-new audition.
