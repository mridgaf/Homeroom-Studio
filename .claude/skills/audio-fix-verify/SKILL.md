---
name: audio-fix-verify
description: Prove an audio change actually worked by measuring the finished file, not the code or an intermediate buffer. Use whenever this project changes anything that affects how a beat SOUNDS — levels, panning, reverb, ducking, velocity, chord voicing, sample selection, mixing rules — and before telling the owner a sound problem is fixed. Catches the failure that keeps recurring here: measuring at a point that is not where the sound comes out, and reporting the median when one failing beat is the whole story.
---

# Verify an audio fix by measuring the output

The owner's ear is the only test instrument this project has ever had, and
that is the bottleneck. Measuring closes it — but only if you measure the
right thing. Every audio bug that survived multiple sessions here survived
because someone measured **near** the problem instead of **at** it.

## The rule

**Measure the WAV or the stem the owner will actually open. Not the buffer,
not the pattern, not the constant you just changed.**

Run `./.venv/bin/python tools/measure_batch.py <folder>` on a rendered
batch. It reports length in bars, per-bar level of the mix AND of the drum
stems alone, stereo width, and every stem's level against the kick.

## The four traps, all of which have bitten

**1. Measuring an intermediate.** A volume cap took FOUR passes on
2026-08-03 because each version measured one stage too early:

| measured | missed | result |
|---|---|---|
| dry buffer | — | 1.2 dB over |
| + reverb tail | reverb is folded in later | shaker at −1.6 vs a −3 cap |
| + constant-power pan | centred lane gets 0.707, panned gets 1.0 | 3 lanes over |
| + sidechain duck | only the kick escapes its own duck | **0 over** |

Ask: *what else happens to this signal between here and the file?* In this
engine the tail is ambience → governors → pan → duck → stems.

**2. Measuring the pattern instead of the audio.** On 2026-08-01 the gap
rate was dialled to 1-in-6 in the composer and a real render still came back
at 40%, because a SECOND pass ran afterwards on the finished audio. A
pattern-level harness cannot see anything that runs after composition.

**3. Reporting the median when one beat is the story.** The pan and duck
bugs each showed up on ONE beat in twenty. The aggregate looked fine.
**When something fails on one beat, open that beat.** Do not average it away.

**4. Measuring your own fixture.** Twice on 2026-08-03 a check reported
success while testing nothing: `voice_files` read from the wrong level of
the recipe gave a meaningless "0 of 0", and a test fixture hardcoded to an
old taste constant had quietly stopped exercising the thing it guarded.
A number that cannot fail is not evidence.

## Before saying "fixed"

- [ ] Rendered a real batch — not a unit test, not a simulation
- [ ] Measured the **same number** before and after; a bare "after" proves nothing
- [ ] The denominator is non-zero and the metric CAN fail
- [ ] Checked the worst case, not just the median
- [ ] If any beat still fails, opened that beat specifically
- [ ] Said plainly what is measured versus what is still **unheard**

## Measured is not heard

Measurement proves the number moved. It does not prove it sounds good.
Always say which you have: *"0 lanes over cap across 24 beats — measured,
not heard."* The owner decides by ear; your job is to stop wasting his ears
on things a number could have caught.

## When a taste constant moves

Changing an `OWNER_TASTE` value (levels, targets, probabilities) can make a
test pass vacuously — its fixture may have been calibrated to the old value.
Grep the tests for that constant and check each one still exercises what it
claims. See `hard-rule-invariant` for the companion rule on writing them.
