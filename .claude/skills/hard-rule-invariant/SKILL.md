---
name: hard-rule-invariant
description: Turn an owner rule stated as absolute ("always", "never", "no matter what", "hard rule") into an invariant that refuses to be broken, instead of a preference that usually holds. Use whenever the owner states a rule about how beats must sound or behave, and whenever a rule he already gave has come back a second time. Prevents the failure that cost six weeks here — a rule implemented as a weight or a "prefer", with its own exception written into the code comment.
---

# A hard rule is an invariant, not a preference

## The failure this exists to stop

"One instrument per stem" appears in `DECISIONS.md` on **2026-07-25,
2026-07-29 and 2026-08-03**. Three sessions, same complaint.

Each time it was implemented as a *preference*:

> `PREFER_MAX_SHIFT = 12` — prefer reusing one sample, up to 12 semitones.
> *"a chord spanning more than an octave still switches packs"*

**That comment is the bug.** The exception was known, written down, and
shipped — three times. And nothing failed when it broke, so it came back by
his ear instead of by a test.

## The rule

When he says **always / never / no matter what / hard rule / I don't want
any**, do all four of these:

**1. One choke point.** Find the single place every path routes through. If
you are adding the same guard in three callers, you are in the wrong place.

**2. It REFUSES.** Not a weight, not a probability, not "prefer". The
operation fails and the caller falls back or the feature is dropped.

**3. Handle the refusal explicitly.** Ask him what should happen when the
rule cannot be satisfied — that is a real question with a real answer.
(2026-08-03: "no single instrument can voice this chord" → he chose *drop
the chord lane entirely*, and the beat card now says so.)

**4. A test that FAILS when violated.** Not a test that the happy path
works — a test that the forbidden thing is impossible. Without this the rule
degrades silently the next time someone touches the file.

## Smells that mean you built a preference

- A number that says how *often* the rule holds — `0.75`, `p=0.5`, `weight`
- A tolerance with the failure case in its comment
- "prefer", "usually", "leans toward", "mostly"
- The rule enforced in some code paths and not others
- No test that would go red if the rule were removed

## The distinction to get right

Implement what he MEANT, not the nearest thing that is easy to check.

On 2026-08-03 "one instrument per stem" was first built as **one FILE per
stem**. That is not the same rule — a real sampled piano is one instrument
across many files — and it made the engine silently swap his chosen piano
for a bell because the bell happened to fit in one file. **Silently playing
the wrong thing is worse than refusing.**

If the two readings differ, that is a BLOCKING question. Ask.

## When a rule comes back a second time

Do not tune the number. Find out why it leaked:

- Which code path skipped the check?
- Which test should have caught it and did not?
- Was it written as a preference?

Then write the invariant. A rule that has been reported twice will be
reported a third time unless something now refuses.
