---
name: dj-rebuild
description: Rebuild ONE Beat Machine identity (crew DJ, Legend or genre) so its listen line is researched, written in the engine's own words, and its settings match. Use when the owner says "rebuild <name>", "do the next DJ", "next one on the list", asks what's left on the DJs/legends/genres, or says a DJ doesn't sound like its description. Replaces legend-new-build (retired 2026-10-23).
---

# DJ rebuild: one identity, done properly (Part 1 of 4: the rules)

Owner, 2026-10-23: "I'm going to need this done for all of my DJs. All of them." Scope: all 45. That's 11 crew DJs, 16 Legends and 18 genres. This overrules the 2026-09-05 "not the nine" rule, by his own choice.
Progress: `Handoffs/DJ Rebuild/TRACKER.md`. Read it first, every session.
Worked example of every step: Doc Day, 2026-10-23 (DECISIONS.md, `Claude outputs/Dr Dre 2001 research transcript.md`).

## Why the old skill failed (don't repeat it)
legend-new-build rebuilt settings to match a description that was itself thin (Doc Day's old line was drums only, with no era, instruments or numbers). It rendered without being asked. It never checked the engine-wide settings that override a DJ: jazz coloring, deep loops, MIDI share, equal chord odds. And the Jul 24 and Oct 19 batch passes produced skimmed research and guessed numbers.

## Where each part can run (learned 2026-10-23, DJ Hint: a whole cloud session was wasted)
- **Research (Part 2) needs to OPEN web pages.** A cloud session or Cowork sandbox cannot: the network proxy blocks every page (Wikipedia, Revolt, Roland, Tunebat all failed; only search-result summaries come back). That cannot meet the quality bar. **Research runs in Claude Code on his Mac.** Say so in the first line of the reply.
- **First action of any research session:** try to open ONE real page (e.g. the Wikipedia page of the producer). If it fails, STOP, tell him "this session can't open pages, run it in Code on your Mac", write the handoff, and do not burn searches.
- Writing the line, blind-spot table, config edits and tracker/DECISIONS updates are fine anywhere. Tests, renders and drive reads are Mac-only (see CLAUDE.md "Where work runs").

## Git hygiene (so branches stop piling up)
- Evidence 2026-10-23: 9 old branches (Sept 1-26) have NO shared history with main (main restarted as a fresh snapshot 2026-10-12) and only 3 PRs ever existed. Cloud sessions each make their own branch; nobody deletes them, and GitHub never notifies about stale branches.
- Cloud session: start from the latest `main`, one branch per session (`dj-<name>-<date>`), commit + push only when he says so, open a draft PR, and after it merges tell him the branch can be deleted (offer, don't do it).
- DECISIONS.md and TRACKER.md are append-hot files: two sessions always conflict at the end of DECISIONS.md. Resolve by keeping BOTH sides, never one.
- Never merge the old pre-October branches into main: unrelated history, it would drag back old code.

## Hard rules
1. **ONE identity per session.** When it's done, stop. The next one gets a fresh session. The owner's worry, confirmed by this log: batching makes the work lazy.
2. **Research is fresh, for this identity only.** Never copy another identity's transcript, line or numbers. Never count the existing config as research.
3. **The listen line is the top rule** (owner 2026-09-05). A line that names nothing the engine can set is useless, so every phrase must map to one setting.
4. **Never render** unless he asks in that message.
5. **Never guess.** Ambiguity means a clickable question. A number nobody sourced is either "your pick" (say so) or left at the default (say so).
6. **Anything he must click goes last** in the reply.
7. Back up before every edit (`<config>.pre-<slug>-<date>.json`). Log it in DECISIONS.md and update TRACKER.md.

## Two sides: Original and Loops (owner, 2026-10-23)
Research and the listen line are done ONCE per identity and shared by both sides. Settings are built TWICE, at separate times, in separate sessions, from that same line. Tracker has a column for each.
- **Original side** = MIDI + sound packs (Part 4 below). When the research names a sound the packs lack (strings, orchestral hits, stabs, pads), fill it with real London Symphonic Strings samples, never a machine tone. Already wired: `tools/string_sampler.py` reads `/Volumes/TBOTC 3/Sample Packs/London Symphonic Strings Volume I`; `London Strings Packets` is a curated copy (Violin, Viola, Cello, Basses x pizz/short/sustain/tremolo) with a manifest CSV. List each such gap in the handoff and say which strings voice fills it.
- **Loops side** = the "loops only" box on Make (`tools/loop_mode.py`, `apply_dj_finish`). Loop material only. Never reaches into the arrangement code (`tests/test_loop_mode_boundary.py` guards it). Say in the handoff which settings that side can actually set.
- A handoff names its side on line 1. A session builds ONE side of ONE identity. Never change the other side's column. Closed only by his ear, per side.

---

# Part 2 of 4: the research session (CODE ON THE MAC ONLY, not Cowork, not a cloud session)

**Step 0. Pick and scope.** Take the next row in TRACKER.md, or the one he names. Read the identity's current `listen`, `built` and `_research_note`.
- **Producer pairs.** These 5 producers appear twice: Dilla (Otto Grit + J Dillo), Premier (Cutz + DJ Premium), Timbaland (Chrome Dial + Timberline), Pharrell (Glass Cat + Farrow), Kanye (Sunday Chop + Kane East). Each pair MUST keep different eras. Read the partner's line first. If the eras overlap, ask him which era each one keeps. Never pick for him.
- **"no one" identities** (New Math, Half Light, Fast Water): there's no producer to research. Ask him (clickable) what each should sound like and which real records point there, then research those records.
- **Era.** If the producer has more than one era, ask which one (clickable) before searching.

**Step 1. Research.** Use web search and fetch. **Quality bar** (don't call research done below it):
- 10+ independent sources
- 5+ signature tracks in the era, with credits, BPM and key, each BPM from 2 sources where possible
- Words from 2+ people who worked with them
- Every fact tagged [CONFIRMED] (2+ sources, or the person themselves), [UNSURE] (one secondary source, or sources disagree) or NOT FOUND
- Quotes under 15 words
- Blocked page: list it and give him the link. He will open any page for you.
- Swing % and drum grids are rarely published. Say NOT FOUND. If he has the audio, measuring it in Code is the real fix.

**Step 2. Transcript.** Save `Handoffs/DJ Rebuild/<Name>/research transcript.md` in the Doc Day format: track table, tempo, swing, drums, instruments ranked, key and chords, bass, mix and arrangement, quotes, who carries it, then a comparison of current settings vs research. Sources and blocked links at the end. Split it into parts.

**Step 3. Collect the engine's words** (read them live; the lists change):
- Chord sounds: `tools/instrument_sampler.py` VOICES (piano includes rhodes/wurli/keys; `strings` and `orchestral` go to string_sampler)
- Modes: `tools/key_context.py` MODES
- Chord loops: `progressions_config.json` keys (find the ones that spell the researched moves, e.g. vamp_i_v7)
- Chord rhythm figures: `tools/chord_rhythm.py` FIGURES
- Bass figures: `tools/bass_rhythm.py` FAMILY
- Drum and hat patterns: the grammar modes used in the configs (backbeat, eighths, sparse, offbeats...)
- Sound-tag words: the flavor groups in `tools/flavor_tags.py` SYNONYM_GROUPS, plus the identity's current kit tags. Real-filename checks (`legend_newbuild.py --words/--tags`) need the drive, so that's a Code step.
- Reverb (`space`): dry / room / plate / gated / washed

---

# Part 3 of 4: writing the line, and the blind-spot check

**Step 4. Write the line.** Same length as the other lines, plain words.
- Each phrase maps to ONE setting, written in the engine's word. Put the phrase-to-setting map at the end of `_research_note`.
- Only [CONFIRMED] facts go in. Claims carried over from the old line, where research is silent, may stay; label them in the map.
- **Words that misfire:** "boom"/"booming" (grouped with 808), "punch"/"punchy" (matched one file, an 808), "live" (grouped with room), "dry" as a snare tag (matches sidesticks), and "always"/"every"/"locked"/"completely"/"zero"/"dead straight" (the tool reads these as hard rules). Use them only when he wants a hard rule, and ask first.
- **Keep existing hard rules** (e.g. Doc Day's "NEVER leaves 2 and 4"). A test probably depends on the wording: grep `tests/` for the name.
- **No gear names in the line.** No setting reads them. They stay in the transcript.
- Leave out what the engine can't do: song sections, chorus-only parts, "strings every 8 bars", mono, steady loudness, part counts.

**Step 5. Blind-spot check.** Fill this table for the identity, every time:

| Check | Where to look | Problem if |
|---|---|---|
| Jazz coloring / deep loops | signature.chord_color, deep_* progressions | still on after the 2026-10-23 jazz-out pass |
| MIDI chord share | chord_source "midi" weight vs the family weights | high share and MIDI chords ignore the loops |
| Chord odds | chord_source | the line names an instrument but the odds are equal (equal families = owner rule 2026-09-25; an exception needs his OK) |
| Hats and percussion | grammar home weights | a line word is backed by under ~50% weight |
| Bass | chord_family (drives bass figures), bass lanes | the line says one bass style and the family pushes another; or the sound needs samples he doesn't own |
| Percussion lane | kit perc tags | the line and the kit disagree |
| Tempo | bpm, signature.tempo | outside the researched range |
| Daily drift | `tools/evolution.py` ops | evolution can move a field the line pins (crew and genres especially) |
| Duplicate | the partner identity | same era, same sounds |

**Step 6. Finish the session.**
- Back up, write the new line plus the map to the config, and verify only `listen` and `_research_note` changed (compare the JSON).
- Write `Handoffs/DJ Rebuild/<Name>/Code handoff.md`: each phrase, the setting change it needs, the owner's picks, what to leave alone, and "do not render."
- Update TRACKER.md (stage: line done), and add a DECISIONS.md entry.
- Ask his decisions as clickable questions. End with his one action: the paste line for Code.

---

# Part 4 of 4: the Code session (his Mac, one identity)

1. Read the handoff. Run the full test suite ONCE, alone, before any render (if he asks for one later): `./.venv/bin/python -m pytest tests/ -q`, about 1331 tests, about 17 min. Never overlap it with a render or library scan.
2. Settings live in the config file ONLY (legends_config / crew_config / genres_config). Back up first.
3. Tags: pick FROM the library (`tools/legend_newbuild.py --words <lane>`), then confirm with `--tags`. Never `dry` on a snare. A synonym pairing you're unsure of: ask him.
4. A sound the research names that he doesn't own: use the nearest real sound and say so. Never fake it with a wrong word. Melodic library (2026-09-28): piano 959, brass 783, string 745, wood 712, bell 469, guitar 305, synth 235, organ 146, pad 16, pluck 16, choir 0, chip 0.
5. Turn any absolute (NEVER) into an invariant: see `hard-rule-invariant`.
6. `tools/identity_survival.py --dj "<Name>"` (+ `--legends` / `--genres`): any line phrase that survives under half the time gets fixed or reported.
7. Test lists to update: the own_soundbank allow-list, and the allow_dirt dict in tests/test_crew.py. Grep tests for the name.
8. Scope every exception to this one identity, with a test asserting only it carries it. Never blanket-apply one identity's answers.
9. No render. Report the numbers, then ask (clickable) whether he wants an old-vs-new audition.
10. Update TRACKER.md (stage: settings done), DECISIONS.md, and the status file: `legend_newbuild_status.json` for Legends, `genre_newbuild_status.json` for genres (set stage to `built`, keep the old verdict in notes).
12. Genre chord odds (owner 2026-10-23): a genre's chord_source is 100% research instruments; every instrument no source names gets weight 0 (keep the entry), plus a test asserting the zeros. midi stays as is. Edit the JSON as text inside that one block: `genres_config.json` has its own indent, so a load/dump rewrite makes a huge diff.
13. Drift: `tools/evolution.py` only reads `crew_config.json`, so genre chord_source cannot drift (Legends are in their own file too; check before claiming). `identity_survival.py` writes `~/.reason_voice/pattern_history.json`; the Claude sandbox blocks that, so run it unsandboxed (analysis only, no render).
11. **Closed only by his ear.** Measured is not done.
