# Chapter 10: Skills that carry production knowledge
## Part 5 of 6

_The saved skills (beat crew, drum loops, recipes, Reason reference, plus older style/gear skills) that hold production rules and producer styles._

**In this part:**
- SKILL.md — ReGroove: swing and feel
- SKILL.md — Verify an audio fix by measuring the output

(Next: Part 6 of 6)


=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:.claude/skills/reason-regroove/SKILL.md
=====================================================

---
name: reason-regroove
description: How to add swing, push/pull timing and human feel with Reason 12's ReGroove Mixer, step by step. Use when the owner asks for swing, shuffle, "loose", "laid back", "drunken kicks", "push the snare", MPC feel, or when a recipe says "use ReGroove" and he needs the steps. Source is the Reason 12.7 manual, ch. 22. Status DRAFT: not yet run through the skill-creator benchmark loop, nothing here has been heard.
---

# ReGroove: swing and feel

Source: Reason 12.7 Operation Manual, ch. 22 (`~/.reason_voice/reason12_manual/full_chapters/22-the-regroove-mixer.txt`).
Every number below is from the manual. Nothing was heard. No API sets these knobs for us (see CLAUDE.md); he or the
screen does it. A surface CAN be locked to the ReGroove Mixer (`docs/reason/FINDINGS.md`), untested.

## What it does, in one line
Changes when and how hard NOTES play (timing, velocity, length), live, without moving the notes in the clip.
**Note lanes only.** It does nothing to audio tracks.

## The steps (do them in this order)
1. Click the **Groove** button on the left of the Transport Panel. The ReGroove Mixer opens: 32 channels, 4 banks (A-D) of 8.
2. On the note lane you want to change, use the **Groove Select pop-up** and pick a channel. ("No Channel" = off.)
3. In the mixer, make sure that channel's **On** button is lit.
4. Turn the knobs (below) while the song plays. Use your ears, not your eyes.
5. To compare with the plain version: turn the channel's **On** off, or untick **Enabled** in the lane's pop-up.

## The knobs (per channel)
| Knob | Plain meaning | Numbers |
|---|---|---|
| **Shuffle** | Delays every other 16th note | 50% = straight. 66% = triplet swing. Below 50% = un-swings a swung beat (34% straightens a triplet feel) |
| **Slide** | Pushes the whole lane ahead of or behind the beat | -120 to +120 ticks (120 ticks = a 32nd note). Negative = rushes, positive = lays back |
| **Groove Amount** | Master strength of the loaded groove patch | 0% = nothing, 100% = full. Scales the four impacts below |
| **Groove patch** | A saved feel (.grov file) | Browse and step through with Next Patch |
| **Pre-Align** | Snaps notes to a rigid 16th grid first, so shuffle and slide land predictably | Non-destructive |
| **Global Shuffle** | Use the song-wide shuffle instead of this channel's own knob | Keeps the lane in step with Redrum, Matrix, RPG-8 and Dual Arpeggio, which only use Global Shuffle |

**Global Shuffle** knob (left side of the mixer) is the song-wide value. It also sets the swing of Redrum's own sequencer,
Matrix, RPG-8 and Dual Arpeggio. If the drums swing but a pattern device sits straight, check this knob.

## Groove Settings (click a channel's **Edit** button)
Four "impact" sliders, each scaled by Groove Amount:
- **Timing impact**: 100% = notes move exactly to the groove's positions, 50% = halfway, 200% = twice as far.
- **Velocity impact**: changes only the differences between notes (soft stays soft). Set Timing impact to 0 to take only the dynamics.
- **Note length impact**: mostly empty on drum grooves. Only the Bass-Comp patches carry length.
- **Random timing**: 0 to 120 ticks of random shift. Same every playback until you edit the clip.

## Moves that work (all from the manual's tips)
- **Split the kit into lanes first.** Kick, snare and hat on separate lanes, each to its own channel. One groove on everything sounds clumsy.
  Use Extract Notes to Lanes to split one lane.
- **Push or drag the snare**: snare lane to a channel with a small + (lay back) or - (push) Slide.
- **Clap doubling a snare**: send the clap to a channel with a little Random timing so the two stop sounding like one hit.
- **Same groove patch on several lanes at different Groove Amounts** beats different patches on each lane.
- **Rushing the first beat**: leave an empty bar at the start and set the Anchor Point to 2, or beat 1 has nowhere to move to.
- **Anchor Point**: tells ReGroove which bar the groove starts on. A time-signature change restarts every groove at that bar
  (add one with the same signature to force a restart).
- **Keep groove lengths as multiples** (1, 2, 4, 8 bars). A 3-bar and a 4-bar groove together repeat every 12.
- **Copy a channel**: Ctrl-click the patch name > Copy Channel, then Paste Channel on another. **Initialize Channel** resets one.

## Factory groove patches (Browse > Factory Sounds > ReGroove Patches)
| Folder | What it is |
|---|---|
| **MPC-60** | Timing from an Akai MPC-60. No velocity or length. Some use Random Timing |
| **Programmed** | Hand-made feels in **Hiphop** and **Pop-Rock** folders |
| **Vinyl** | Timing and velocity pulled from classic records |
| Drummer, Percussion, Bass-Comp | Session musicians. Only Bass-Comp has note length |

## Make it permanent, or make your own
- **Commit to Groove** (Edit menu or track menu): moves the notes to where they now play, so you can edit them. It applies to
  the WHOLE track. To keep one lane grooved, untick Enabled on it first, commit, then tick it back.
- **Your own groove**: select a clip, pick an unused channel in the Tool Window Groove tab, click **Get from clip**, then **Save Patch**.
  Best source clips: many 16th notes (gaps in the clip become gaps in the groove), similar velocities, an exact bar count
  (1, 2, 4...). You can pull one from a MIDI file or from a REX loop (Dr. Octo Rex "Copy Loop To Track").

## Recipes that rely on this
`recipes/hiphop/doechii-denial-is-a-river.md` (loose kicks, late snare), `recipes/hiphop/jid-never-story-music-box.md`
(drum bus, shuffle 55-60%, slide a few ticks late), `recipes/feelings/feels-warm-soulful.md`. Those recipes name ReGroove;
this file has the steps. The numbers in them are their authors' reading, not tested.

## Open
- Not yet through the skill-creator benchmark loop (owner's standing rule for new skills).
- Nothing here heard. Slide values in the recipes ("a few ticks") are unmeasured.

=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:.claude/skills/audio-fix-verify/SKILL.md
=====================================================

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

=== END OF PART ===
