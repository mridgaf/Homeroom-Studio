---
name: dj-identity-audit
description: Use when adding or editing a DJ/Legend persona in crew_config.json, when pattern_gen.compose() or tools/crew.py changes, when a beat sounds weaker or different than a persona's own description, or before calling a new or adjusted persona's identity "done".
---

# Does the persona's written identity survive the engine?

## The failure this exists to stop

Fast Water (slot 11) came out weaker than Half Light (slot 10) and the owner
noticed (2026-08-08). The cause was measurable, not a matter of taste:
`pattern_gen.compose()` rewrites every lane's bars from scratch on every
single beat, so a trait written only as a bar figure in `crew_config.json`
is gone before he hears it. `tools/identity_survival.py` was built that same
day to measure this instead of guessing — it composes N beats per DJ and
reports what actually survives.

Nothing points Claude at that tool. It isn't referenced from
`beat-crew/SKILL.md`, doesn't run automatically, and has no guidance on when
to reach for it. So a persona ships, its `listen` line makes a claim, and
whether that claim is even mechanically possible to hear stays unverified
until the owner catches it himself again.

## When to run it

- Adding or editing a DJ/Legend in `crew_config.json`
- After a change to `pattern_gen.compose()` or `tools/crew.py` — engine
  changes can silently break survival for personas that used to be fine
- The owner reports a persona sounding weaker/different than described, or
  asks "does X still sound like X"
- Before telling him a new or adjusted persona's identity is done

## Run it

```
./.venv/bin/python tools/identity_survival.py [--dj "Name" ...] [-n 12] [--legends] [--genres]
```
`--dj` is repeatable. No flags = every DJ (crew + legends + genres, sorted
by roster number). Read-only: renders nothing, writes nothing, no drive
needed.

## Reading the three sections

| Section | What it means | Anything short of 100%? |
|---|---|---|
| **INVARIANT** | Slots `compose()` is documented to never touch: lane roster, LaneFeel, pan/gain, tempo/mix, space/alt | **Engine bug.** Not a weak identity — fix the code. |
| **FIGURE** | Declared bar figures in `crew_config.json` still present after composing | Low is *expected* unless the lane is pinned in `canon` — a bar figure is structurally a bad place to hold identity. |
| **HOME** | How often a lane lands in its grammar's highest-weighted mode | The durable way to keep a trait; a 30% home weight showing up ~30% of the time is working as designed. |

## A fragile lane found — do one of these

Don't just note it and move on. A `listen` line promising a trait that
survives less than half the time is a description that lies to him.

1. Move the trait into an invariant slot (compose() won't touch it)
2. Raise the grammar's home weight for that lane
3. Pin the lane in the persona's `canon`

## Don't alarm on

FIGURE below 100% alone — that's normal for any unpinned lane. Only
INVARIANT rows below N/N, or an unpinned lane whose FIGURE stays under 50%
while its `listen` line claims the trait, are actionable.
