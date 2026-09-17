---
name: audio-fix-verify
description: "Prove an audio change actually worked by measuring the finished file, not the code or an intermediate buffer. Use whenever this project changes anything that affects how a beat SOUNDS — levels, panning, reverb, ducking, velocity, chord voicing, sample selection, mixing rules — and before telling the owner a sound problem is fixed. Catches the failure that keeps recurring here: measuring at a point that is not where the sound comes out, and reporting the median when one failing beat is the whole story."
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

## The eight traps, all of which have bitten

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

**5. The control specimen never had the bug.** 2026-09-03, Night Metro: an
A/B batch for the missing "bar 5 drops to the 808 alone" rendered every
"after" file BYTE-IDENTICAL to its "before". The bench was the static
prototype in `crew_config.json` — and that file already has bar 5 empty.
The bug only exists in beats that go through `compose()` + `vary_preset()`,
which rewrite the lanes from grammar. The fix looked like a no-op because
it was being tested on the one specimen that never had the fault.

Related to trap 2 but not the same: trap 2 is a later pass undoing your
work, this is a control that was never broken. Ask: *does my BEFORE file
actually reproduce the problem?* If it does not, there is nothing to fix
and nothing to prove. **Build the bench the way the owner's real output is
built** — for beats that means composed, not the prototype.

**6. Right file, right stage, wrong BAND.** Same session, same batch: bar
5's full-band RMS moved 0.6 dB and read as "the drop does nothing." False.
Night Metro's sustained 808 carries most of the beat's energy, and the 808
is exactly what the breakdown KEEPS. The hats and clap are what leave, and
they live up top; measured above 2 kHz the same drop is **-19 dB**.

A whole-mix number is dominated by whatever is loudest, which is often the
thing you did not touch. Ask: *where in the sound does this change live?*
Then measure there. Two cousins of this already cost a session each — a
low shelf measured as a SHARE of the total instead of absolute band energy
(reported +0.22 where the truth was +0.42), and a per-hit sub layer
averaged across a loop of mostly silence (+0.17 whole-file vs +3.54 at the
hit). Per-hit effects need a per-hit ruler; one-bar effects need a one-bar
ruler; band effects need a band ruler.

**7. The loudness stage moved everything you did not touch.** 2026-09-04,
the root 808: adding a sub measured as being OUT OF PHASE with the kick on
all three test beats (correlation -0.31 to -0.65) — a scary, wrong finding
that nearly went in a READ ME.

The renders are loudness-normalised. A sub makes the file louder, the
loudness stage pulls the WHOLE beat back to hit the same target, and the
difference between before and after therefore contains a scaled-down copy
of everything you did not change. That scaling reads as anti-correlation
on any unpicked measurement.

Fix the ruler, not the code: fit the gain on a band the change does NOT
touch (here, everything above 100 Hz), divide it out, and only then ask
what happened underneath. Phase came back -0.01 to -0.22 — no fight at
all. And the gain you divided out is not noise, it is **the finding**: the
drums step back 2.5-5.2 dB to make room for the sub, which is the real
trade-off his ear has to judge.

Any A/B where the change adds or removes energy has this. Ask: *is my
"after" the same loudness as my "before"?* If yes, something scaled
everything else to make that true.

**8. The placement plan is not where the sound is.** 2026-09-16, loops-only beats: the recipe said the FX lane hits bars 3 and 8.
He heard FX "on every bar". Both were true. The FX file was 8 seconds
long, so the two hits (with the tail wrapping round the loop) covered 6 of
the 8 bars. The plan was correct and the sound was wrong.

Check any "plays on bars X" rule by measuring the lane's STEM bar by bar
(peak per bar, over 5% of the stem's own peak = sounding), then compare
that list to the plan. Keep testing with the longest real file in the
pool, not a short test click.

## Before saying "fixed"

- [ ] Rendered a real batch — not a unit test, not a simulation
- [ ] Measured the **same number** before and after; a bare "after" proves nothing
- [ ] The denominator is non-zero and the metric CAN fail
- [ ] Checked the worst case, not just the median
- [ ] The BEFORE file actually reproduces the problem
- [ ] The ruler looks where the change lives — band, bar, and hit
- [ ] Divided out the loudness gain before comparing anything
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
