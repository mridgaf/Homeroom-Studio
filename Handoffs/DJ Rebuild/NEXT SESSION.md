# DJ Rebuild: where it stands, how to continue (written 2026-10-24) — Part 1 of 1

Paste to start the next session (Claude Code on the Mac):
`Read Handoffs/DJ Rebuild/NEXT SESSION.md and continue the DJ rebuild.`

Read first, in order: this file, `TRACKER.md`, `.claude/skills/dj-rebuild/SKILL.md`, the top of `DECISIONS.md` (2026-10-24 entries).
Last commit with all of this: `c9f07ce` (plus this handoff's commit).

## 1. Owner rules set on 2026-10-24 (do not re-ask)
- **New research overrules old research and old rules.** If a handoff pick is "keep the old unsourced thing vs follow the new research", follow the research and say so in one line. Ask only when research is silent or split, or two readings mean different work.
- **He renders auditions himself** from the Beat Machine page. Do not render. Do not offer to render.
- **He batches now:** he asked for every identity with a finished line to be built in one session. The skill's "one identity per session" rule is overruled when he asks for more.
- "Make sure everything was committed" = commit this session's files yourself (never `Nightly Loops/.lm_ids.txt` or other engine churn). Push stays his (GitHub Desktop).

## 2. Where everything stands
| Stage | Identities |
|---|---|
| Original settings done (not heard) | Doc Day, G-Funk, DJ Hint, Acid Rap Bright (10-23, MIDI rule 10-24); Horror Rap, Cutz, Chrome Dial, Crate Prophet, Crunk, Chiptune, Baltimore Club, Acid Rap Detroit (10-24) |
| Line done, settings waiting | none |
| Not started (research needed first) | the other 33 rows in TRACKER.md |
| Loops settings done | none (all 45 "not started") |

Nothing from any rebuild has been heard. Closed only by his ear, per side.

## 3. ORIGINAL side: the rule (owner 2026-10-24)
"Originals using the MIDI chords and the sound packs mainly." The Loops side has its own page.
- `signature.chord_source` = **midi 75, loop 10, sound packs 15**. The 15 is split by the research.
  - **Genres:** research instruments only; every instrument no source names = 0 (keep the entry). Add the genre to `RESEARCH_ONLY` in `tests/test_crew.py` (its zero set must be unique).
  - **Crew:** "50-50" = the researched sounds get half of the 15, the rest share the other half.
  - **Legends:** the handoff's ratio inside the 15 (DJ Hint: strings/bell/pad 82.5% of the packs).
- Use `tools/config_text_edit.py`: `original_odds(cs, {instrument: weight})` does the math, and `set_path` / `add_after` / `del_path` edit the JSON as text (a load/dump rewrite makes a huge diff). Then JSON-compare against the backup.
- Add every new Original build to `ORIGINAL_BUILT` in `tests/test_original_midi.py`.
- Engine (built, new beats only, stamp `midi_voice_flow` 1): MIDI notes play on the identity's own chord_source instruments with weight > 0, never bell or pluck; if none reach the notes, the London strings play them. `evolution.py` never drifts midi, loop or zero-weight sounds.

### Code-pass checklist (per identity)
1. Back up the config (`<config>.pre-<slug>-<date>.json`).
2. Read the Code handoff. Apply the research; ask only what research leaves open (rule 1).
3. Chord odds per section 3. Tempo, key, mode, kit, bass and extras as the handoff says.
4. Grep `tests/` for the name and update the lists: `allow_dirt` dict AND the "low" set (both in `tests/test_crew.py`), own_soundbank list, washed-space list (`tests/test_audio_quality.py`), `RESEARCH_ONLY`, `ORIGINAL_BUILT`.
5. `tools/identity_survival.py [--genres|--legends] --dj "<Name>" -n 100` (run unsandboxed). A line phrase under 50% gets fixed: test the weight in memory first (patch `identity_survival.CREW`), then write it. Example: Crate Prophet hat eighths 0.55 gave 33/100, 0.8 gave 50/100.
6. Run the touched test files, then the full suite once at the end: `./.venv/bin/python -m pytest tests/ -q --ignore-glob='*.pre-*' --basetemp="/Volumes/TBOTC 3/pytest-tmp-<n>"` (about 27 min, alone; unsandboxed).
7. TRACKER (stage + Original column), `genre_newbuild_status.json` / `legend_newbuild_status.json` (stage `built`, old verdict kept in notes), DECISIONS.md, commit.

### Traps found this session
- `signature.chord_rhythm` takes ONLY `"arp"` / `"sustain"` (or a weighted list of those two). Stab, comp and pad are figures in a top-level `chord_grammar: {"figures": [["comp", 3], ["stab", 1]]}`. Set chord_rhythm to "sustain" alongside it. The handoffs said "chord_rhythm stab": that was wrong.
- Signature keys you add (`tempo`, `bass_grammar`) need `add_after`, since `set_path` only replaces an existing key.
- `allow_dirt: "low"` = kick/808 grit only; on a beat with an 808 lane it grits the 808, not the kick.
- `extras.pool` entries take an optional 4th number = weight (Baltimore Club: shakers and vocal chops 3). Pools without one shuffle exactly as before.
- Library words: `legend_newbuild.py --words fx` shows only the top 28. To find a specific word, search `make_drum_beats.build_shots()` per role (Chrome Dial: car screech 1, baby vocal 6, animals perc 1; NO cricket, horse or rain).
- **TRACKER can be wrong.** It said Acid Rap Detroit and Baltimore Club settings were done; the ledger and config showed they weren't. Check DECISIONS.md + the config itself before trusting a row.
- `identity_survival.py` rewrites `~/.reason_voice/pattern_history.json`; `tests/test_variety.py` Night Metro reads it, so it can flip after survival runs (old code scores the same 3.18 from an empty history). Known, not fixed.
- Two other failures, not ours: `test_boundary` (tools/panel_sweep.py imports reason_voice), and the Swish Beatz backbeat level test (failed once, then passed).

## 4. ORIGINAL side: what is next
- Next rows by tracker order: **Otto Grit (#3) and J Dillo (#4)** = the Dilla pair. Research first (skill Part 2, Code on the Mac, opens real pages). The pair MUST keep different eras: read the partner's line, ask him which era each keeps.
- Then DJ Premium (#6; Cutz now holds Premier 1992-96, Premium keeps 1998-2006), Timberline (#8; Chrome Dial holds 1996-2002), Glass Cat / Farrow, Sunday Chop / Kane East, and so on down the tracker.
- Later jobs he allowed but did not ask to build yet: a **Madlib pass for Crate Prophet** (own era); **chopping loops for vocal/chorus parts** on the Original side.
- Unfixed but known: Chrome Dial crickets/horse/rain (no files; download would be its own task).

## 5. LOOPS side: the state
Built 2026-10-24 (DECISIONS "Loops side settings: built"; `Handoffs/Loops Settings Build.md` has every ruling and word list).
- `loops_config.json` holds the shared vocabulary (`_groups`, `_texture`, `_lead_types`, `_finish`, `_glue`, `_title_only`). `tools/loop_vocab.py` reads it.
- What steers an identity's loop picks today: its `listen` line + its library tags + an optional `"<Name>": {"words": [...]}` block in loops_config.json. **No identity has a block yet.**
- Loop beats are fully clean for everyone (allow_dirt and "effects on" ignored). ONE mood row sets the loop EQ and glue: the group with the most distinct matching words wins; ties go to the first one in the listen line.
- Loops code may not reach the arrangement code (`tests/test_loop_mode_boundary.py`). `loop_mode.apply_dj_finish` is an UNUSED duplicate: the finish runs in `crew.render_crew_beat(loop_bufs=...)`.

### Loops build, per identity (nothing done yet)
1. Read its research transcript and listen line (shared with the Original side; no new research).
2. List the words that should steer its loops: style groups (`_groups`), lead types (`type:keys`, `type:guitar`... via `_lead_types`), texture words. Only words the research backs.
3. Check which `_finish` row wins: `loop_vocab.finish(loop_vocab.identity_words(name), {}, {})`. If the wrong mood wins, the block's words are how to steer it. Example measured 2026-10-24: Horror Rap AND Cutz both get the hip hop row (low +1, mid +1, glue 3.0); Horror Rap probably wants dark/horror.
4. Write `"<Name>": {"words": [...]}` into loops_config.json; add a test that only it carries those words.
5. TRACKER Loops column, DECISIONS. He hears it from the "loops only" box on Make.
- Suggested order: the 12 identities whose Original side is done (research is fresh).
- Open from the Loops build: artist words below the top 120 are unlisted; glue numbers (1.3 / 1.6 / 2.2 / 3.0) and the mood EQ are Claude's drafts, unheard.
