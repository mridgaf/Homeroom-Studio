---
name: audition-batch
description: Deliver rendered beats for the owner to listen to, so a change gets judged by his ear instead of only by measurement. Use whenever a sound change is ready for his verdict, when he says "render a batch" or "let me hear it", or before treating an audio decision as settled. Covers where to put the files so his library numbering is never disturbed, what the plain-English README must say, and the difference between measured and heard.
---

# Give him something to listen to

Every real sound bug in this project was found by his ear. Measurement stops
you wasting his ears on things a number could catch — it does not replace
them. A change is not settled until he has heard it.

## Where the files go

**Render to a scratch folder, then COPY to the Desktop. Never render into
his library.**

```
~/Desktop/Homeroom <what it is> <YYYY-MM-DD>/
```

Rendering into `/Volumes/TBOTC 3/Claude Drum Beats` takes real beat numbers
from the global counter and mixes auditions in with keepers. `generate()`
takes `root=`; point it at the scratch dir under this session's scratchpad.

Sub-folders only when there is a real reason to separate — a before/after
comparison, or normal beats vs break beats. Two or three folders, not six.
Delete any older audition folder first so there is no doubt which is current.

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
one. This is cheap, it runs every render, and it is the only thing standing
between a wrong bench and an hour of his listening time.

If a check fires, **do not ship the batch and explain the warning to him**
— fix the bench and re-render. A batch he can't learn anything from costs
more than the render did. See `audio-fix-verify` traps 5 and 6 for the two
that fired.

## Before you hand it over

- [ ] Rendered to scratch, copied to the Desktop — library untouched
- [ ] Old audition folder deleted
- [ ] No duplicate files across the sub-folders (copy, then move — and
      re-count afterwards; this has gone wrong)
- [ ] README written in plain words, quoting his complaint
- [ ] Deliberate oddities named beat-by-beat
- [ ] Said what is measured vs what is unheard
- [ ] Told him the one thing you actually need back from him
- [ ] The script's own fail-loud checks ran and stayed silent

## After he listens

His verdict goes in `DECISIONS.md` — `confirmed` if it held, `failed` if it
did not, with the number to move if he wants it different. A batch he never
reported back on stays `open`; do not quietly promote it.
