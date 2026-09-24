---
name: legend-new-build
description: "Rebuild one Legend's or one GENRE's sound from research and audition it old-vs-new. Use when the owner names a Legend or genre to work on, asks what is left to do on the legends or genres, says tune the genres / new build / rebuild / research him / make him sound like himself, or when a Legend's beats do not match his own written description. Covers the Legends and the 18 genres; the nine crew DJs are explicitly NOT in scope."
---

# One Legend, rebuilt from research, judged by his ear

## What this is

Owner 2026-09-05, after Doc Day's rebuild landed: *"I'll want this same for
all remaining legends. Not in the 9. Create something to make that easy and
clear for each session"* — **"So you remember."**

Twelve Legends. One is done. This is the process for the rest, one per
session. **The nine crew DJs are not in scope** and their settings must not
move.

## Genres use this same process (owner 2026-09-24)

"Start tuning the genres using the same format as the rebuild for DJs,
research first then build." His answers, all clickable:
- **A-Z, one at a time**, same as the Legends. Progress lives in
  `genre_newbuild_status.json`.
- **Keep the approved mix, tune the style.** True levels, the low-end
  rules, one bass per beat and the Loops page's own levels stay exactly
  as they are. Change the genre's drums, tempo, sounds, tags and chords.
- **Dirt follows the research** without asking: if the sources say the
  genre is dirty, set `allow_dirt` (True or "low") for that genre.
- Every tool takes `--genres`:
  `tools/legend_newbuild.py --genres --legend "Name" --tags` and
  `tools/make_legend_newbuild.py --genres --legend "Name" --structure`.
  Backups are `genres_config.pre-<slug>-<date>.json`.
- A genre with a `_research_note` is never reset by a GENRES_VERSION bump.
- Genres are not DJs: `own_soundbank` gates EVERY pick (no open-bank
  share) and they are exempt from the kick-flavor streak-breaker.
- **Fresh TinyFish research for every genre** (owner 2026-09-24), sources
  quoted in its `_research_note`. Never build from the old config alone.
- **`"flavor_match": true` on every genre build** (owner 2026-09-24: "we
  should at least look for synonyms or similar words"). He ruled on every
  synonym pair himself — see `tools/flavor_tags.py` SYNONYM_GROUPS. Any
  NEW pairing you are unsure of: ask him with clickable options ("I can
  tell you immediately what should be what"), never guess.
- A synonym never lands a sidestick/rim/clap/combo in a snare slot or an
  open hat/combo in a hat slot (`_NOT_A_SNARE`, `_NOT_A_CLOSED_HAT`). After
  `--tags`, still list the files each lane newly reaches and read them.

## Start every session here

```
./.venv/bin/python tools/legend_newbuild.py
```

Prints where all twelve stand, and for anyone not started: his `listen`
line, any ABSOLUTE words in it, and what is still wrong with his config.
Stage comes from `legend_newbuild_status.json`; the checks are read live so
they cannot go stale. Add `--tags` to audit taste tags against the real
library (needs TBOTC 3 mounted).

## The order of work

**1. Back up first, or there is nothing to A/B.**
```
cp legends_config.json legends_config.pre-<slug>-$(date +%F).json
```
One backup per legend, and only one — the render script now REFUSES to
guess between two, because it once silently picked a half-built
intermediate and reported +0.92 dB where the truth was +5.03.

**1b. Check the nine for the same producer BEFORE you research.**
```
./.venv/bin/python -c "import sys;sys.path.insert(0,'tools');import json;\
d=json.load(open('crew_config.json'));print([(n,p.get('built')) for n,p in \
(d.get('CREW') or d).items() if isinstance(p,dict)])"
```
Two of the twelve turned out to be straight duplicates of a crew DJ, both
found on 2026-09-05 and neither noticed for months, because the legends and
the nine are audited separately: **Farrow was Glass Cat** (Pharrell, same
bpm, same lanes, same kit tags, same 18 ms flam) and **Kane East was Sunday
Chop** (Kanye, same 57% swing, same "BIG clap with the snare tucked
underneath", same tambourine offbeats). If the producer is already in the
nine, stop and ask the owner which era each one keeps — he has answered
this twice and both times the crew DJ kept what it had and the LEGEND moved
to a different era. Do not pick the era for him.

**2. Research him, then write down who said so.** Every change goes in his
`_research_note` with its source. A change nobody can source is not a
research build — flag it as unsourced and leave it at the roster default,
the way saturation and sidechain were left for Doc Day.

**3. His `listen` line is the top rule.** Owner, 2026-09-05: *"Keep
following the description as the top rule."* Where the description and an
inherited house rule disagree, the description wins — see below.

**4. Turn his ABSOLUTES into invariants.** If his line says *never*,
*always*, *dead straight*, *locked* — that is not a weight. Read
`hard-rule-invariant`: one choke point, it refuses, and a test that goes
red if it is removed. Doc Day's snare mode was `[[backbeat, 0.9], [sparse,
0.1]]` against a description saying the snare NEVER leaves 2 and 4, and the
one-in-ten fired in a real audition.

**5. Turn his sound bank on and fix the tags.**
`"own_soundbank": true` makes his taste tags actually gate sample picks —
without it the July open-sound-bank rule wipes them and every pick is
random from the whole bucket. **Then check the tags against real
filenames** (`--tags`): they match FILENAMES, not intent. Doc Day's
`punch/knock/deep` matched ONE file in the library, and `boom` matched
three of which two were 808s — the words read perfectly and delivered the
opposite.

**New for legends built from 2026-09-09 on: also set `"flavor_match":
true`.** This turns on `flavor_tags.py`'s synonym layer, so a want-tag
also reaches its documented synonyms/spelling variants (e.g. "tight" now
also matches this library's "tite" files) instead of only the exact
literal word — the class of dead-tag finding `--tags` keeps turning up on
every legend so far. Owner directive, 2026-09-09: wire this forward-only.
**Do not add this flag to any of the twelve existing legends or the nine
crew DJs** — they stay on the old literal-only matching until he asks for
that retag pass separately. `--tags` audits a `flavor_match` legend with
the same synonym-aware logic it will actually run with, so a lower "dead
word" count on a new legend is real, not a blind spot. See
`tools/flavor_tags.py`'s module docstring for which words are
deliberately NOT grouped (`dry`, `boom`, `punch`/`knock`/`deep` — each has
its own documented over-matching history) and why.

**6. Render the audition.**
```
./.venv/bin/python tools/make_legend_newbuild.py --legend "Name"
```
Every lesson from the three Doc Day batches is already in that script —
read its docstring rather than re-deriving them. It refuses to overwrite a
folder he already has.

**7. Read the printed sample list before you ship it — the STAMP first.**
The locked stamp is the one sample heard on every single beat, and until
2026-09-05 the list did not print it: `build_kit` puts it in `kit["stamp"]`
but never in `sources`. Four legends in a row shipped a wrong producer tag
under that blind spot — a rain field recording (Farrow), a river (Kane
East). It is printed first now. If it is wrong, fix the `kit["stamp"]` tags
AND delete that legend's entry from `~/.reason_voice/crew_kits.json`, or the
stale lock survives the fix. State the pass
condition first, then check it. This is the step whose absence cost a whole
round trip: a batch went out with two sidesticks where snares belong, open
hats where tight hats belong, and a talking drum.

**8. Tests, then hand it to him.** Full suite (`.venv/bin/python -m pytest
tests/ -q`, ~8 min, baseline 994 passed / 3 skipped). Any invariant test
that touches `compose()` must be run several times over — compose() re-rolls
per process, so one green run proves nothing.

**9. Record the stage.** Update `legend_newbuild_status.json` and append to
`DECISIONS.md`. `confirmed` means **he has heard it and said yes** — nothing
else counts. Measured-and-shipped is `auditioned`.

## When an old decision blocks the new build

His standing rule, 2026-09-05: *"Overrule old decisions when they cause
problems with my new request. But always ask in plain language first."*

Ask him with real options, include the scope choice (this one legend vs all
twelve — he has twice chosen the narrow one), and then act on his answer in
the same session. Do not park it as a flagged open item; that is what he
was correcting.

**Scope every exemption to the one legend.** `own_soundbank` and
`snare_locked_24` are both single-preset opt-outs defaulting to off, and
each has a test asserting only the intended legend carries it. Follow that
shape — a roster-wide change to fix one man is how the nine get damaged.

## Do not

- Touch the nine crew DJs. Not in scope, he said so.
- Blanket-apply Doc Day's answers. Only Doc Day's line says the snare NEVER
  leaves 2 and 4; **Timberline's clap "answers instead of insists", J
  Dillo's snare rushes 20 ms early, Farrow's clap lands 18 ms late.** Locking
  those to 2 and 4 would destroy the identity.
- Call it done off a measurement. Only his ear closes a legend.
