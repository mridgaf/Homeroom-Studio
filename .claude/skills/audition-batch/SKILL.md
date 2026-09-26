---
name: audition-batch
description: Deliver rendered beats for the owner to listen to, so a change gets judged by his ear instead of only by measurement. Use whenever a sound change is ready for his verdict, when he says "render a batch" or "let me hear it", or before treating an audio decision as settled. Covers where to put the files so his library numbering is never disturbed, what the plain-English README must say, and the difference between measured and heard.
---

# Give him something to listen to

Every real sound bug in this project was found by his ear. Measurement stops
you wasting his ears on things a number could catch — it does not replace
them. A change is not settled until he has heard it.

## Where the files go

**Render to a scratch folder, then COPY to ~/Desktop/Homeroom Auditions/. Never render into
his library.**

```
~/Desktop/Homeroom Auditions/Homeroom <what it is> <YYYY-MM-DD>/
```

Rendering into `/Volumes/TBOTC 3/Homeroom Rhythms` takes real beat numbers
from the global counter and mixes auditions in with keepers. `generate()`
takes `root=`; point it at the scratch dir under this session's scratchpad.

Sub-folders only when there is a real reason to separate — a before/after
comparison, or normal beats vs break beats. Two or three folders, not six.
Keep every older audition folder — all auditions, old and new, live in ~/Desktop/Homeroom Auditions (owner rule 2026-09-25). The date in the name shows which is current.

## The README

Every batch gets a `READ ME.txt` in plain words. It must say:

- **What to listen for**, in his language, tied to what HE reported. Quote
  his own words back where you can — "the samples getting louder and
  quieter" beats "per-slot gain variation".
- **What changed**, one line each, no jargon.
- **Anything deliberately odd**, so he doesn't report it as a bug. (A beat
  that shipped with no chords because no single instrument could voice the
  progression needs saying, by name.)
- **What you could NOT check** — the honest limit. This is the most valuable
  part and the easiest to leave out.

Put the beats he most needs to compare FIRST, and say why. If he named a
beat, include one from the same DJ.

## Measured is not heard

Report them as two different things, always:

> 0 lanes over cap across 24 beats — **measured**. Whether 3 dB is far
> enough back for the shaker, I can't tell you: **not heard**.

Never let a table of green numbers imply he has approved something. He
hasn't until he says so.

## The batch script must fail loud

Twice on 2026-09-03 a batch would have gone to him meaningless, and both
times the script's own check caught it — not review, not a test. Every A/B
script here (`tools/make_*_ab.py`) ends by asserting its own premise, and
prints a WARNING rather than shipping quietly:

- **Every version differs from its control.** A version that renders
  byte-identical to "a Now" is a bug in the bench, not a subtle effect.
- **The change went the direction it claims.** A "matte" version that
  measures brighter, or a drop that does not drop, is a wrong wire.
- **The file count is what was asked for.**

Copy the shape from `tools/make_night_metro_ab.py` rather than inventing
one. **This is not advice, it is the cheapest of the lessons here.** On
2026-09-04 a fresh bench was written instead of copied and reproduced,
exactly, the trap that file spends a paragraph warning about:

- **COMPOSE ONCE PER BEAT, then copy it per version.** `compose()` is
  deterministic per (name, variant, attempt), but its repeat guard carries
  history ACROSS calls — so calling it once per version can land on a
  different attempt and a different loop length. That batch had an 8-bar
  "a Now" against a 4-bar "b Root 808": two different beats wearing an A/B
  label. He would have been comparing nothing.
- **Assert the versions are the same LENGTH.** One line, and it fails on
  the actual defect. What caught it instead was a low-end number that
  happened to look odd, which is luck, not a check.
- **Name files so two versions cannot collide.** Every beat by one DJ
  carries that DJ's bpm (tempo_locked), so "DJ + bpm + tag" is not unique
  across two beats — two files silently overwrote and the count check was
  the only thing that noticed. Number the pairs. This is cheap, it runs every render, and it is the only thing standing
between a wrong bench and an hour of his listening time.

If a check fires, **do not ship the batch and explain the warning to him**
— fix the bench and re-render. A batch he can't learn anything from costs
more than the render did. See `audio-fix-verify` traps 5 and 6 for the two
that fired.

## Before you hand it over

- [ ] Rendered to scratch, copied into ~/Desktop/Homeroom Auditions — library untouched
- [ ] Landed inside ~/Desktop/Homeroom Auditions (old ones kept)
- [ ] No duplicate files across the sub-folders (copy, then move — and
      re-count afterwards; this has gone wrong)
- [ ] README written in plain words, quoting his complaint
- [ ] Deliberate oddities named beat-by-beat
- [ ] Said what is measured vs what is unheard
- [ ] Told him the one thing you actually need back from him
- [ ] Every version of a beat is the same length as its control
- [ ] The script's own fail-loud checks ran and stayed silent — and you
      SAW them run. A check chained ahead of a backgrounded command
      (`check && render &`) is backgrounded too: on 2026-09-04 a syntax
      check written exactly that way never printed, and the batch failed
      five minutes later on a broken string.

## After he listens

His verdict goes in `DECISIONS.md` — `confirmed` if it held, `failed` if it
did not, with the number to move if he wants it different. A batch he never
reported back on stays `open`; do not quietly promote it.
