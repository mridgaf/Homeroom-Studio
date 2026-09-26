# Reason Voice — Project Handoff & v2 Rebuild Brief

## The names — all one project, don't treat them as separate
**Beat Generator = Beat Machine = Homeroom = Homeroom Studio = Homeroom Studios
= this folder** (`~/Desktop/Homeroom Studio`). The owner uses these names
interchangeably. `BEAT-GENERATOR-GAP-ANALYSIS.md` in this folder is about this
code. If a request names any of them, it means here.

## This is one half of a pair
The other half is **`~/reason code`** (space in path — always quote) — the
translation brain:
recipe builder, Reason device parameter maps, audio analysis. Same owner, same
music, same house rules. They go hand in hand; treat them as one body of work.

- Its brief: `~/reason code/CLAUDE.md` — read it when work crosses over.
- **The skills live HERE.** `~/reason code/.claude/skills` is a symlink pointing
  at `Homeroom Studio/.claude/skills`, so both folders see the same set. Edit
  them in either place — it's one directory, and this is the real one.
- This file's house rules and hard rules apply over there too, and that file
  says so.

## What this is
A push-to-talk voice interface for Reason 12 (DAW) on macOS. Hold a hotkey, speak,
release: browse patches, control transport, search a sound-recipe knowledge base,
and get walked through recipes step-by-step. All speech is processed locally
(faster-whisper). v0.3 works end-to-end and is verified on the owner's machine.

## Owner & machine facts (do not rediscover these)
- User: self-taught musician, technical background, NOT a developer. All
  instructions to the user must be single paste-able commands or double-clickable
  files. He runs commands in Terminal, sometimes pastes into the wrong window.
- Machine (VERIFIED 2026-07-31 — the old entry here said "older MacBook Pro"
  and was simply wrong; do not reinstate it): **MacBook Pro 14" 2023,
  `Mac14,9`, Apple M2 Pro, 10 cores, 16 GB, arm64, macOS 26.5.2.** This is a
  fast, current machine. Nothing should be ruled out "because the hardware is
  old" — that reasoning was false and shaped months of decisions.
- Python: the venv points at Apple's Command Line Tools `python3` = **3.9.6**.
  That is a *choice*, not a machine limit (3.9 went end-of-life 2025-10-31);
  `uv 0.11.29` is already installed at `~/.local/bin/uv` if you want to move.
  Until it moves, keep targeting 3.9: no `X | Y` unions without
  `from __future__ import annotations`.
  **3.9 is NOT a blocker for the audio work** — verified by installing them:
  `soxr 1.1.0` (current) and `pedalboard 0.9.17` both have cp39 arm64 wheels,
  and that pedalboard build has PitchShift, Limiter, Compressor, Reverb,
  Resample, Convolution, `time_stretch` (Rubber Band) and `io.AudioFile`.
  Upgrading Python buys newer versions, not access.
- The M2 Pro's GPU and Neural Engine are unused. `faster-whisper`'s CTranslate2
  backend is CPU-only on macOS; `whisper.cpp` runs on the GPU via Metal. The
  "small.en ~1s latency" figure below was taken under the wrong hardware
  assumption and should be re-measured before anyone optimises around it.
- Project lives at: `~/Desktop/Homeroom Studio` (space in path — always quote).
  Moved here 2026-07-19 from `~/Music/Reason 12/reason-voice 3` so everything
  is in one folder on the Desktop. Beats + samples stay on `/Volumes/TBOTC 3`.
- Shell is bash (not zsh). macOS `sed` needs `-i ''`.
- **Everything lives on the cloud/external drive**, which isn't always mounted
  and is big + slow — verify presence with Finder size + item count, never a
  recursive search: recursive searches time out silently on these drives and
  report false "empty" results. Fail loud if a path is missing rather than
  writing to the wrong place.
- **Answer in plain, short language.** He is not a developer; explain the
  "why" only when it matters, and give single paste-able commands or
  double-clickable files, never multi-step developer instructions.
- **Never delete his files** — cleanup scripts move into a dated folder with a
  manifest and ask for a typed `yes` (see the `safe-file-ops` skill).
- His sound library is almost entirely **inside ReFills + Factory Sound Bank =
  sealed archives, cannot be indexed**. He owns ~2 loose patch files. The patch
  style-search feature is therefore nearly useless to him today; it only gains
  value as he saves his own patches. Deprioritize it in v2 UI.

## Architecture that WORKS — keep these layers
1. **Reason Remote bridge — DO NOT REWRITE.** File formats, mandatory keys,
   install paths and device scopes are all in the `reason-remote-bridge` skill.
   Read it before touching anything under `remote/` or the mido CC map.
2. **Recipe knowledge base (keep the data format exactly):**
   - `recipes/**/*.md` with YAML frontmatter: name, book (rock|hip-hop),
     sounds_like, accuracy (A–D honesty rating), status (tested|theoretical),
     source, tags, technique. Body sections: `## The Chain`, `## Steps`
     (numbered — drives the voice walkthrough), `## Why this works`,
     `## Order of operations`, `## Reason-specific trick`, `## RE upgrade path`,
     `## Technique you just learned`, `## Reference`.
   - `device_refs/*.md` — plain-language device guides.
3. **Loading found patches:** `open -a Reason <patchfile>` adds the device to the
   rack. Only channel besides MIDI. There is NO API to build device chains,
   route cables, or set knobs programmatically. Never promise that.

## Current code — the two non-obvious bits
Read `reason_voice/` for the rest; only these two won't be obvious from the code:
- `intents.py` is an ORDERED regex grammar. Pattern order is load-bearing —
  reindex must outrank recipe search.
- `reason_control.py`'s mido CC map MUST stay in sync with the .lua codec.

## Why the owner wanted the rebuild (his words: "clunky", "jumbled")
- Terminal UI confuses him: results look like "a few sentences", the
  list→"load two"→walkthrough flow is not discoverable, spoken feedback (`say`)
  overlaps, and typing commands into the app's window does nothing (he did this
  repeatedly — one-window model fails him).
- Multi-step install with three macOS permission dialogs was painful.
- No visual state: can't see if it's listening, what recipe is open, what step
  he's on.

## v2 — BUILT (`reason_voice/server.py` + `static/`). Shape, so nobody re-litigates it
A **single always-visible window**: listening state (idle/recording/thinking),
transcript of what it heard, the current recipe as a readable card (like the PDF
layout), current step highlighted during walkthrough, big clickable buttons
duplicating every voice command (voice optional, never required), and a
browsable recipe list. Everything clickable AND speakable.

**Owner confirmed this shape — don't re-ask:**
local web UI: Python backend (keep all existing modules) + FastAPI/Flask +
WebSocket, serving `http://localhost:port`, auto-opened in the browser by the
launcher. Rationale: (a) rich UI without new macOS permission fights for
key-listening — put push-to-talk as a BUTTON (click-and-hold / spacebar in the
page) so pynput/Input Monitoring can be dropped entirely; (b) mic can stay in
the Python process (sounddevice, already permitted for Terminal) — do NOT move
audio capture into the browser; (c) recipe cards render beautifully in HTML.
Avoid Electron (heavy) and avoid packaging with PyInstaller until the UI is
stable.

**Keep:** recipe .md format + all content, PDF generator, Remote bridge files
verbatim, mido CC map, faster-whisper. **Drop:** pynput global hotkey (replace
with in-page control), `say` spoken feedback by default (visual instead, toggle
in settings), the bare-terminal REPL.

**Constraints that still hold:** venv uses system python3 (3.9), `pip install`
inside `.venv`. Do not move the project folder — the Remote files and his
muscle memory point at it. Tests are set up: `.venv/bin/python -m pytest tests/`
— **~1256 tests, ~14 min** (measured 2026-09-25; the old "~750 tests, ~4 min"
here was stale). Run it ALONE: it renders beats off the external drive, so a
render or a library scan in another terminal starves it and the same suite
crawls to hours. That looks exactly like a hang and isn't one.

## Known open items
- All recipes are status: theoretical — as he tests them, flip to tested.
- Whisper "find something like this" often transcribed as "and something like
  this" — v2 should fuzzy-match intents, not just regex.
- `small.en` latency ~1s on his hardware; offer tiny.en toggle in UI settings.
- **MIDI chord packs as a new chord source (own session, owner 2026-09-14).**
  `tools/midi_packs.py` is real but dormant: it reads exact notes (no
  key-guessing) from 298 MIDI files sitting in the same loop pack folders
  (183 chord, 58 melody, 53 drum, 4 bass — measured), and its own
  vendor-label-vs-detected-key cross-check disagrees on 104 of 245 keyed
  files, which is real signal, not noise. The folder fix is DONE
  (2026-09-15: own `midi_roots`/`midi_sorted_root` keys, reads
  `BOTC Sorted MIDI`, guarded by `test_scan_finds_his_real_midi_packs`).
  Still open: MIDI is not a `chord_source` option in any live config;
  wiring it in means
  deciding how `"midi"` competes against sampled instruments and `"loop"` in the weighted
  chord_source lists. Owner wants this as its own session, not folded
  into whatever else is in progress.

## Working rules for this project

### 0. Talk to him like a person, not a developer

He is a self-taught musician with ADHD. He is not a developer and does not
want to become one. How you write is part of the work, not a wrapper around
it.

- **Fewest words that are still true.** Cut every sentence that isn't
  carrying a fact he needs. Long replies don't get read, and a wall of text
  is worse than no reply.
- **Answer first, reasoning after** — and only if he needs it. Never build
  up to the point.
- **Plain words.** No jargon without a plain-English version right there.
  Not "the governor's clamp was asymmetric" — "the volume control couldn't
  turn things down far enough."
- **One idea per line.** Short paragraphs, tables and bullets over prose.
  A table he can scan beats a paragraph he has to hold in his head.
- **Numbers, not adjectives.** "Was 6.7 dB apart, now 0.4" tells him
  something. "Much better" doesn't.
- **Say what he has to DO, and put it last** so it's easy to find. One
  paste-able command or one double-clickable file — never a multi-step
  developer procedure.
- Explain the "why" only when it changes what he decides.

### HARD RULE: If Claude can do it, Claude does it

Owner, 2026-09-25: "If there is something that I do not have to do manually, you need to do it. Explain what you're going to do and then just do it. Quit giving me tasks."
- Say in one or two lines what you are about to do, then do it. Do not hand him commands to paste, files to click, or steps to run that you could run yourself.
- Only hand something to him when it truly needs him: his ears (listening), his password, a macOS permission dialog, or a physical action.
- If a safety check blocks you, first try a safer way yourself (smaller steps, move instead of delete). Only then come to him, as one clickable yes/no, never as a to-do list.
- House safety rules still hold: never delete his files (move them), never commit/push unless he says so.

### 0b. Ambiguity: stop and ask. Never guess

His standing instruction (2026-08-03, after several breaches): "I don't want
you making any guesses or any inferences. If anything is ambiguous to you,
you stop and wait for me. You ask me."

- Label every question **BLOCKING** (nothing proceeds until he answers) or
  **ASSUMING X** (proceeding on a stated reading, correct me any time).
- **Never ask a question and then answer it yourself.** If it was worth
  asking, wait. This has happened repeatedly and it wastes his time twice —
  once reading the question, once undoing the wrong work.
- If a plan contains a "you listen here" checkpoint, STOP there. Do not
  carry on because the next part is obvious.
- When two readings of a word lead to different work, that is BLOCKING —
  even if one reading seems much more likely. ("stacks" meant the melodic
  instruments, not the drums; twelve identities were rewritten on the wrong
  guess and had to be reverted.)

### 0c. He commits. The engine rewrites itself. Neither is news

Two things happen constantly in this project and BOTH have been reported
to him as if they were problems. They are not.

- **He writes and pushes every commit himself**, without being asked.
  Never run `git commit`/`git push` unless he says so in that message,
  and never end a report by telling him to commit. Uncommitted work is
  this repo's normal resting state, not a loose end.
- **Generating beats rewrites tracked files by design.**
  `tools/evolution.py` makes ONE bounded change per DJ per day in
  `crew_config.json` and journals it. A dirty `git status` here is the
  default, not a finding.

Full detail — every file that self-writes, the one command that proves a
diff came from the engine rather than a person, and the
`ensure_ascii=False` convention that stops you creating phantom diffs —
is in the `expected-churn` skill
(`.claude/skills/expected-churn/SKILL.md`). Read it before reporting
that anything looks changed.

### 0d. HARD RULE: tests before beats, and never at the same time

Owner, 2026-09-09, after a session that rendered three batches before ever
running the suite — and found three roster tests had been broken the whole
time:

**Run the full test suite ONCE per session, BEFORE the first render.**
```
./.venv/bin/python -m pytest tests/ -q
```
~1256 tests, ~14 minutes. Later renders in the same session don't repeat
it unless code changed since.

**Never render while a test run is going.** They both read beats off the
external drive and starve each other — the suite crawls, the render slows,
and the suite looks hung when it isn't. Tests finish, THEN rendering starts.
Nothing overlaps. (2026-09-09: a suite was started in the background and
three batches rendered on top of it. That is the mistake this rule exists
to stop.)

This is a hard rule, not a preference. No "just this once because the
change is small" — that is exactly how it came back.

### 0e. The Dock always opens the newest version

Owner, 2026-09-25: the Dock icons (the row of apps at the bottom of the screen) must always open the
newest version. They point at the live apps in this folder, never a copy or an old build.
A new app or page gets a Dock icon. If an app is moved or renamed, re-point its Dock icon
in the same session. To check the paths: `defaults read com.apple.dock persistent-apps`.

### 0f. All auditions live in ONE folder: ~/Desktop/Homeroom Auditions

Owner, 2026-09-25. Every audition, new and old, goes inside `~/Desktop/Homeroom Auditions/`,
never loose on the Desktop, and old ones are kept. The audition scripts in `tools/` already write there.

### 1. Verify before claiming done
Don't report a fix, a build, a calculation, or a "this should work" as finished
without actually checking it:
- Code: run it. Run the tests. Run the linter/type checker if one exists. Don't
  infer success from reading the diff.
- Files/documents: open and re-read the output, don't just trust the generation
  step.
- Anything with no automatic check (a physical fix, a decision, advice): say so
  explicitly — "no way to verify this from here, log a check-back."

If verification isn't possible in this session, say that plainly instead of
implying it's confirmed.

### 2. Use DECISIONS.md as memory across sessions
This file persists; I don't. At the **start** of a session, read `DECISIONS.md`
in the project root before starting work — it has prior decisions, fixes, and
open items.

**Read `DECISIONS.md` only — NOT `DECISIONS-ARCHIVE.md`.** The ledger was
split on 2026-08-01 because it had reached ~50,000 tokens and this rule was
spending that on every single startup. `DECISIONS.md` now holds 2026-07-26
onward plus a one-line index of everything older; the archive holds the 66
earlier entries verbatim, nothing deleted or edited. Open the archive only
when you need the reasoning behind something older, or when a live entry
points back to one. Verified lossless at the time of the split: 73 entries
in, 73 out, zero text changed.

Statuses in the archive were true when written; several say `open` only
because nobody circled back, not because the thread is live. Check the code
before treating an old `open` as an outstanding task.

At the **end** of a session, append an entry to `DECISIONS.md` for anything
that was:
- a real decision or judgment call (not a trivial choice)
- a fix or change whose outcome isn't yet known
- something worth not re-litigating next time

Don't log routine, low-stakes steps — the file is for things worth remembering,
not a full transcript.

### 3. Format
Use the entry format defined at the top of `DECISIONS.md`. Keep entries short.
Mark status honestly: `open` if unverified, `confirmed` if checked and held,
`failed` if it didn't hold — update old entries when you learn the outcome,
don't just add new ones.

### 4. Skill
The `session-ledger` skill (`.claude/skills/session-ledger/SKILL.md`) has the
full read/append workflow and should trigger automatically. `SCRATCH.md`
(project root) is the disposable live-reasoning trace for a multi-step
problem in progress.
