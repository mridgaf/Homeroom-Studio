# Skill benchmarks, 2026-10-01: reason-mixer-chains, reason-vocal-chain, reason-drum-bus

What this is: the record of the skill-creator test loop for the three Reason 12.7 skills built from `docs/reason/techniques/` and `docs/reason/manual-digest/`.
Nothing here was heard in Reason. The tests check whether an answer is complete and correct against the 12.7 manual and `device_refs/`, not whether it sounds good.

## How the test worked
- 8 realistic questions (3 mixer, 3 vocal, 2 drum), each answered twice by a fresh assistant: once with the skill, once with no skill and no project files (plain Claude from its own knowledge).
- Each question has 5 to 8 yes/no checks (assertions) written by me. A separate grader assistant scored each answer against them and quoted its evidence.
- Round 1 used the first drafts. Round 2 used the fixed skills and tightened checks. The no-skill answers were reused in round 2 and re-scored against the tightened checks.
- Files: `evals-*.json` (the questions and checks), `review-iteration-1.html` and `review-iteration-2.html` (every answer, side by side, with the score tables).

## Scores (checks passed / checks total)
| Question | Round 1 with skill | Round 1 no skill | Round 2 with skill | Round 2 no skill |
|---|---|---|---|---|
| Mixer 1: Kong kick ducks bass | 6/6 | 4/6 | 6/6 | 3/6 |
| Mixer 2: record through effects, shared reverb | 6/6 | 2/6 | 6/6 | 1/6 |
| Mixer 3: effect made with wrong thing selected | 5/5 | 4/5 | 5/5 | 3/5 |
| Vocal 1: rap lead chain | 7/7 | 5/7 | 8/8 | 6/8 |
| Vocal 2: Neptune natural + octave double | 4/5 | 1/5 | 5/5 | 1/5 |
| Vocal 3: vocoder robot voice | 5/5 | 3/5 | 5/5 | 3/5 |
| Drum 1: thin Redrum, glue + punch | 6/7 | 3/7 | 6/7 | 4/7 |
| Drum 2: Kong trap routing, hat choke, rolls | 6/6 | 3/6 | 5/6 | 2/6 |
| **Total** | **45/47** | **25/47** | **46/48** | **23/48** |

## What the no-skill answers got wrong or missed
They knew the general ideas. They missed the Reason 12.7 specifics: Parallel Out into the Sidechain input (they cabled a Kong output straight to the key input), the Rec Source route for recording through effects (one said it might not be possible), Create Send FX on the Master Section (they used old mixer wording like "Aux Return"), Kong's Drum Output selector and Quick Edit pad groups, the Redrum individual-output catch, a de-esser, and Neptune's real control names. They were honest about being unsure, which is good, but the steps would not have worked as written.

## What the test caught in my own drafts (fixed)
1. De-essing with the strip's Filters To Dyn S/C turns the strip HPF/LPF into trigger filters, so the rumble cut has to be a separate EQ device. My first chain used both on the strip.
2. Wrong knob names: Neptune "Semitones" (not "Semi"), BV512 "HF Emphasis" (panel label "HF Emph"). Panel labels and Remote names differ for some controls; the skills now say which to use when.
3. Missing click steps: how to split the kick out of Kong or Redrum before sidechaining; what to do when an effect was made with the wrong thing selected; Mix Channel strip vs Insert FX when recording through effects.
4. A glue compressor and a parallel compressor are two devices, not one.
5. Octave double needs a second Neptune on a send.
Also fixed in `techniques/vocals.md` and `manual-digest/routing-and-main-mixer.md`.

## Limits (read these before trusting the numbers)
- I wrote the checks from the same notes the skills are built from, so they favour the skills. The real gap is smaller on generic advice and larger on 12.7-specific steps.
- The graders and the answerers are AI assistants. I checked the key steps against the manual myself (Tab flips the rack, Cmd+G output bus, Create Parallel Channel, Rec Source recipe, Filters To Dyn S/C caveat, Kong pad groups). The rest is not independently checked.
- Three small wording edits were made to the skills AFTER round 2 (Redrum output warning, Mute Group letter note, vocoder band count) and were not re-tested.
- No answer was tried in Reason. "Passed" means the steps match the manual and the device guides.
- Triggering (whether Claude picks the right skill from the description alone) was NOT tested, and the description optimizer was not run.
- Still unverified in the manual: whether Parallel Out follows the kick fader, and whether a Mix Channel's own strip compressor is captured when recording through it.
- Eight questions is a small sample. Add more before calling these finished.
