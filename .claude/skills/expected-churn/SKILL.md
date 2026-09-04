---
name: expected-churn
description: "Tells apart the files this project rewrites BY ITSELF from changes someone actually made, and records that the owner is the one who commits. Use before reporting modified/uncommitted files, before saying something changed unexpectedly, before suggesting he commit or run git commands, and any time git status looks dirty in this project. Prevents the recurring waste of flagging the beat engine's own bookkeeping as a problem and telling him to commit work he always commits himself."
---

# The engine writes to itself. That is not a problem.

## The failure this exists to stop

He generates beats. The engine writes its own bookkeeping. The next
session runs `git status`, sees modified files, and reports them as if
something went wrong — or worse, tells him to commit. Both waste his
time, and both have happened repeatedly (2026-09-04 twice in one
session). His words: "This happens often... you seem not to remember."

## Two rules, no exceptions

**1. HE COMMITS. ALWAYS.** He writes and pushes every commit himself,
and he does it without being asked. Never run `git commit` or `git push`
unless he says to in that message. Never end a report with "you should
commit this" or a commit command. If work is uncommitted, that is the
normal resting state of this repo, not a loose end. Say what changed;
let him decide.

**2. DIRTY IS THE DEFAULT.** In this project a clean `git status` is the
unusual case. Do not open a report with it, do not treat it as a
finding, and do not investigate it unless something specific asks you to.

## What changes on its own, after every beat run

| File | Written by | Tracked? |
|---|---|---|
| `crew_config.json` | `tools/evolution.py` — ONE bounded change per DJ, first time that DJ is featured in a day | **yes — this is the one you will see** |
| `legends_config.json`, `genres_config.json` | same contract; also rewritten on a `STYLE_VERSION` bump | yes |
| `~/.reason_voice/crew_journal.json` | the evolution log — every delta, dated | no |
| `~/.reason_voice/pattern_history.json` | `pattern_gen.compose()` — 24-entry rolling window per DJ | no |
| `~/.reason_voice/sample_history.json` | `build_kit` anti-repetition | no |
| `~/.reason_voice/beat_machine_state.json` | the batch player's current batch | no |
| `<beats root>/**` + `.recipes/NN.json` + `README.txt` | the render itself | no (external drive) |

`.worktrees/`, `sonic/`, `vox_plugin/` sit permanently untracked. They
are not new. Do not report them.

## Is this diff the engine or a person?

One command answers it:

```bash
.venv/bin/python tools/whats_evolved.py
```

It prints every DJ the evolution engine changed TODAY, with the exact
`old -> new` for each value. A `crew_config.json` diff whose changed
values appear in that output IS the engine — say so in one line and move
on. If it prints "no evolution today", the diff came from a person and
is worth a closer look.

Worked example, 2026-09-04 — the whole diff was these three, plus 11
lines of the escaping mistake below:

```
Cutz           trusts their own grammar more (groove-seed chance 45%)
                 library.p: 0.55 -> 0.45
Chrome Dial    the kick stutters less (double chance 42%)
                 grammar.kick.double_p: 0.5 -> 0.42
Sunday Chop    writes more uplifting changes
                 signature.progressions.2.1: 2 -> 2.5
```

Rolling back a change his ear dislikes:
`./.venv/bin/python tools/evolution.py --rollback "Name"` (also
`--status`, `--history`).

## Do not create phantom diffs

Every engine writer saves the config as:

```python
CONFIG.write_text(json.dumps(doc, indent=1, ensure_ascii=False))
```

`json.dump` defaults to `ensure_ascii=True`, which escapes every
non-ASCII character — so an em-dash gets written as a six-character
backslash-u escape instead of the character itself. Editing the config
with the default flipped 11
lines and guaranteed that every future engine write would flip them
back — permanent diff noise from a one-character mistake (done
2026-09-04, fixed the same day). **Match the convention above whenever
you write any of the three config files.**

## What IS still worth raising

- A tracked file changed that is NOT in the table above.
- A `crew_config.json` change with no matching journal entry for today.
- The library gained or lost beats when nothing rendered — check with
  the `drive-verify` skill, never a recursive search.
- A test that was green is now red.
