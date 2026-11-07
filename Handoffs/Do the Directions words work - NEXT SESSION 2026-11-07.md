# Do the Directions words do anything? — handoff (2026-11-07)

**Question from the owner:** the words in the Directions dropdown ("e.g. dark, melodic, aggressive…") — do they actually change the beat, and does the change match the word? Answer word by word. Read `DECISIONS.md` first (not the ARCHIVE). He commits himself unless he says otherwise. **No renders to disk, no full test suite** (house rules) — in-memory builds and focused tests only.

## What I already found (code read, 2026-11-07, nothing run)
- The dropdown is `<select id="quick">` in `tools/beat_machine.py` (~line 7144). Its placeholder says "dark, melodic, aggressive", but **"melodic" and "aggressive" appear in NO parser** — typing/picking them likely does nothing.
- The text goes to `parse_directions()` (~1081) then `apply_directions()` (~1173), called at ~3917/3996. Anything it doesn't recognise is "just a note".
- Words that ARE read:
  - `FEEL_WORDS` (~1019): dreamy, sad, sinking, uplifting, happy, nostalgic, jazzy, epic, **dark** (→ `dark_menacing` chord feel), menacing, vamp. These only choose a chord progression.
  - `DIRECTION_TAGS` (~969): acoustic, clean, dirty, dusty, lofi, vintage, warm, hard, soft, punchy, deep, crisp, tight, boomy, distorted, vinyl → sample want-tags (a nudge to which sample is picked, not a mix change).
  - Others: sparse/minimal/busy, swing words, waltz/6-8, halftime, space (gated/dry/room/washed), long 808 / no 808, no <lane>, "no chords"/"drums only", famous-break names.
- **Loops-only mode** has its own mood words in `tools/loop_vocab.py` (`finish`: dark/lofi/creepy → EQ + glue only).
- Today's dirt change: `allow_dirt`, `dust`, `vinyl`, `kick_dist`, `mix_sat` are all off for everyone and `drive` is 0.1. So **dirty, dusty, lofi, vinyl, distorted may now do less than they say** — check them with that in mind.

## The test to run (per word)
For each word in the dropdown and in the lists above, build the beat **in memory** twice (same DJ, same seed/take number, with and without the word) and diff:
1. Did the preset change at all? (`parse_directions` output + `apply_directions` notes echo)
2. Is the change what the word says? Examples: dark → minor/dark chord feel, lower/darker samples?; aggressive/melodic → nothing today, so report "does nothing"; hard/punchy/tight → which sample got picked; dusty/vinyl/lofi → any audible machinery left now that dirt is off?
3. Does it survive for Legends, genres and Original-side beats, and is it ignored on loop-only beats (loops are fully clean by owner rule)?
Output: one table, word → "does what it says / does something else / does nothing", with the evidence. Then ask him (clickable) which "does nothing" words to wire up, drop from the dropdown, or leave. Do NOT wire anything up before he answers.

## Tools to batch together before starting
Load/start these in ONE go so nothing waits mid-task:
- **Skills:** `audio-fix-verify`, `expected-churn`, `hard-rule-invariant`, `beat-crew` (project skills, 1% rule), plus `session-ledger`.
- **Read:** `DECISIONS.md`; `tools/beat_machine.py` lines ~962–1175, 3900–4000, 7140–7160; `tools/loop_vocab.py`; `tools/flavor_tags.py`; `tools/sound_words.py`.
- **Run:** `./.venv/bin/python` from the project folder (3.9 — add `from __future__ import annotations` for `X | Y`); import `beat_machine` and call `parse_directions` / `apply_directions` directly in a scratch script in the scratchpad dir, not in the repo.
- **Drive:** check `/Volumes/TBOTC 3` is mounted first (sample pools and beat locks live there); if not, stop and say so.
- **Focused tests only:** `./.venv/bin/python -m pytest tests/test_crew.py -q` and any `-k direction` tests. The 5 known failures there are today's dirt-off tests (4) plus the unrelated kick-sustain test.
- **Browser (only if you need to see the dropdown):** the Beat Machine page on port 8770 via the built-in browser or gstack `/browse`; restart it first so it loads today's changes. Do not use TinyFish or Chrome-extension tools.
- **Git:** `git status`, `git log -3` before touching anything.

## Also loaded today (don't redo)
- Drive 0.1 / vinyl 0 / dust 0 / dirt off for all 45 identities (backups `*_config.pre-no-dirt-2026-11-07.json`; the configs are gitignored, so those edits are NOT in git).
- Percussion, snaps, clicks, chords, melody −2.5 dB (`tools/crew.py`, `TRIM_2_5_*`). New beats only.
- EQ plan closed — see `Handoffs/EQ work - NEXT SESSION 2026-11-07.md`.
- Shared-words list: `Handoffs/Shared words across DJs 2026-11-07.md`.
