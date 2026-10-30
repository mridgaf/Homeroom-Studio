# Beat Machine open issues: next session (handoff 2026-10-30)

Paste to start: `Read Handoffs/Open Issues - NEXT SESSION 2026-10-30.md and continue the open issues.`

Read the `DECISIONS.md` entries dated 2026-10-29 and 2026-10-30 first. Nothing since 2026-10-23 has been rendered or heard.

## Done this session (uncommitted; he commits in GitHub Desktop)
- **Original side: no loops unless every instrument fails** (owner: "This side, I don't want to use loops. Unless absolutely necessary."). New stamp `preset["no_loop"]`. A loop comes last in `_source_order` and in the plan list. Texture is now full 10% / two 90% (his pick). Loops-only beats are a separate path and weren't touched. Backup: `tools/beat_machine.pre-no-loop-2026-10-30.py`.
- Tests: new `test_original_beats_use_a_loop_only_as_last_resort`. `test_loops_always_play_alone` now turns no_loop off so it keeps testing its own rule. 47 pass.

## Still open, most important first (checked against the Mac 2026-10-30)
1. **He hasn't heard anything since 10-23.** That's no MIDI, no EQ/dirt, no loops, two-note texture, new chord styles, 50% open sounds. Needs his ears. Only render if he asks.
2. ~~**Full chords per identity from research**~~ DONE 10-30 (`texture_full`, 14 identities; see DECISIONS). Was: Today it's a flat 10% for all 45 (`riff_gen.TEXTURES`). He picked "rare, research decides". Research which DJs/genres should get full keys (likely soul/R&B/G-funk/jazz) and give each its own full/two odds. Two notes now carry 90% of Original beats, so this matters more than it did.
3. DONE 10-30: no guitar-tab chords; those styles borrow the iReal sheets (`chord_gen.BORROW`, see DECISIONS). Was: **Hip-hop/club/latin/rock/G-funk chords still come from guitar-tab data** (🗳️). 85% plain triads, same pop loops in every style. Options he was offered but hasn't picked: favor each style's own loops, tag whole words only, add color when voicing. Ask with clickable options.
4. ~~**"chord1 made no sound, no stem written"**~~ CHECKED 10-30: old by-design empty-lane note (08-01 guard), not a bug. Was: shows up on some test beats (🤖). Check whether this is old behavior before calling it a bug.
5. **Loops-side settings per identity** (🤖): none of the 45 started. The shared rules are built (`loops_config.json`, `tools/loop_vocab.py`); the per-identity `words` blocks are empty. `Handoffs/DJ Rebuild/TRACKER.md` is stale: its Original column is right, its Loops column is all "not started".
6. ~~**New Math, Half Light, Fast Water**~~ DONE 10-30, Original side (see DECISIONS and `Handoffs/DJ Rebuild/<Name>/research transcript.md`). New Math = Flying Lotus Cosmogramma (88 bpm, unquantized, harp/strings, octave+walk bass). Half Light = Earl Sweatshirt / Alchemist (68 bpm, piano/guitar/strings loops, soft lo-fi snare). Fast Water = Bukem / Goldie atmospheric jungle (155 bpm, strings + pads). Their Loops column is still "not started" (item 5). Not heard.
6b. **Fast Water's break lane** still plays 32nds in only 24/100 beats (weight 62%): library hat seeds (library p 0.6) replace it. Snare "2 and & of 3" is 42/100. Going further means lowering `library.p`, which changes its sound: ask him by ear first.
6c. **New Math / Half Light / Fast Water description phrases that are carried over, not researched:** lane offsets and swing, plate/hall space, stamp bars. Marked "carried over" in each `_research_note`.
7. **Parked by him, do later:** chopping loops into vocal/chorus parts; a Madlib pass for Crate Prophet.
8. **Beats made before 10-30 can still shift a little when a sound is removed.** Known limit, not a task.
9. **Low value:** 14 unfiled loops from 09-27, the key detector, the skipped VSCO piano/organ.

Don't redo these, they're done: the sound-removal drift fix (10-30), No Alias, all 42 Original rebuilds, `test_loops_always_play_alone`, the full suite after the chord work (10-30). The OPEN-ISSUES.md items 29-44 are Reason Voice / Reason control, not the Beat Machine.

## Done later the same day (second half of 10-30, after the "no loop" work above)
- Full-chord odds per identity (`texture_full`), no guitar-tab chords (`chord_gen.BORROW`), and the three "no one" DJ rebuilds above. All tests pass apart from the known Night Metro failures. Nothing rendered.

## What I learned about DJ rebuilds (saves time)
- **Web research works in Code with Firecrawl** (`firecrawl search ... --scrape --json -o file`, `firecrawl scrape <url> -o file.md`), saved to `/Volumes/TBOTC 3/Research Scratch/<name>/`. Needs the sandbox off. Search calls 429 if fired many at once: run them one at a time with `sleep 2`.
- **BPM sites (songbpm.com/@artist/track, Tunebat) read loose or slow tracks at double time.** Halve and say so as [UNSURE]. Both sites often share one source, so two sites is a weak "2 sources".
- **Tests pin old identity.** Rebuilding a DJ meant editing `test_crew.py` (New Math swing/quint20 asserts), `test_pattern_gen.py` (quint20 hat), `test_v6.py` (lanes are TUPLES, rebuild them, don't assign into them), and `ORIGINAL_BUILT` in `test_original_midi.py`. `built` must not stay "no one" if anything greps it.
- **Cheap identity check:** `./.venv/bin/python tools/identity_survival.py --dj "<Name>" -n 100` (unsandboxed). Drum figure rows usually read 0-30%; only the lines the `listen` text promises matter.
- **Weights lift:** to raise one grammar mode, set it to the target and scale the others by `(1-target)/sum(others)`; edit with `config_text_edit.set_path`. Library hat seeds cap how often a hat mode can show.

## What I learned (saves time)
- **How tests must run:** outside the sandbox from the first try. The sandbox blocks `~/.homeroom_engine` and `~/.reason_voice` and makes about 159 tests fail falsely. Scratch goes on the drive: `--basetemp="/Volumes/TBOTC 3/pytest-scratch/<name>" -p no:cacheprovider`. Anything over ~2 min runs in the background. Name the test files you want; for a whole-folder run add `--ignore-glob='*.pre-*'` (a backup test file breaks collection). Never render while tests run.
- **Focused files for sound-pick changes:** `tests/test_freedom.py tests/test_original_midi.py tests/test_signature.py tests/test_chord_bass_gen.py` (45 tests, ~2 min) plus `-k` picks in `tests/test_beat_machine.py` (each generate() test takes ~1-2 min).
- **Only report real failures** (owner 2026-10-30). Known minor ones are ignored and not listed: Otto Grit dirt check, Timberline chip-only chords, panel_sweep imports reason_voice, Night Metro spread/halftime, the `.pre-*` collection error.
- **New-beat-only changes go through a stamp.** `add_bass_and_chords` sets them with `preset.setdefault(...)`: `chord_gen`, `texture_flow`, `no_midi`, `no_loop`, `no_eq`, `dyn_flow`. Old beats lack the stamp and rebuild as they were made. Copy this pattern for any sound change.
- **Chord sound order:** `beat_machine._source_order(pref, rng, free, no_midi, no_loop)` takes a signature's `chord_source` weights. On 50% of beats (`free_beat(variant, SOUND_OPEN_P)`) the first pick is uniform over every voice. It is called in 3 places: `_pin_bars_for_loop_voice` (runs inside solo_preset before stamps exist, so it passes flags directly), the chord build (~line 2985), and the plan list after it (extra instrument groups get appended). A change to the order has to land in all of them.
- **Gotcha:** with no signature weights left, `_source_order` used to return a tuple. Code that does `order[1:] + [...]` crashed. It returns a list now when no_loop is set.
- **Loops-only beats** skip `add_bass_and_chords` entirely (`generate(..., loops_only=True)`), so chord-side changes never touch them.
- **Texture roll:** `riff_gen.roll(variant)`, then converted in beat_machine around line 2490: no_loop turns loop/riff into "two", and no_midi turns riff into two/loop.
- **To test one beat with a stamp switched off,** wrap `beat_machine.solo_preset` with monkeypatch and set the flag on the preset it returns (see `test_loops_always_play_alone`).
- **Where his settings live:** `chord_source` sits under `signature` in `crew_config.json`, `legends_config.json`, `genres_config.json`. 37 identities still carry `["midi", 75]` and `["loop", 10]` there. Leave them; the stamps filter them out at run time.

## House rules that bit this session
- He's asked "no loops on Original" and "no MIDI" in plain words. Never reintroduce either on new Original beats.
- Ask clickable; one short paragraph replies; he commits himself; no renders unless asked.
