# Plan B: Crate digger (Loops side only) — BUILT 2026-10-31, not rendered, not heard

2026-10-31. Loops page only. Original side untouched. Nothing rendered or heard.

## What it does
On a new loops beat, the **lead loop** (sometimes) gets chopped instead of played whole:

1. Stretch the loop to the beat's tempo (already done today, pedalboard).
2. Cut it at its hits (`melodic_loops.chop_onsets`, already in the code).
3. **One chord only:** slices come only from bars whose notes match the
   first bar's (score 0.95+; on his chord-named loops a real chord change
   scored 0.55-0.92, a repeat 0.94-0.99). A slice stops where a different
   bar starts. Ceiling: a chord change mid-bar is not caught.
4. Lay the slices on the beat grid in a new order, in the identity's chop style.
   The 2-bar phrase repeats to fill 8 bars, so it loops seamlessly.
5. ~~Pitch the slices to the beat's key~~ NOT BUILT: the lead loop is the
   loop the beat's key is taken from (bass/chords match IT), so there is
   nothing to move. Pitching would only matter if another loop set the key.
6. Optional **resample**: chop the chopped phrase once more.

Old beats rebuild exactly as made: the chop settings are saved in the beat's
loop state (new stamp `chop`); beats without it play the whole loop like today.
Only his own loops. Nothing synthesized.

## What I found
| Fact | Number |
|---|---|
| Lead + chord loops on the Loops side | 3,944 |
| Key in the file name from the pack maker | ~3,540 |
| Key guessed by the detector (the `synthNN_Key_140` files in Melody) | ~105 |
| No key at all | ~300 |
| Key detector accuracy (2026-09-26 test) | 46 of 100 loops right |

## Chop styles (draft)
| Style | Sounds like | Slices | Placement |
|---|---|---|---|
| Stabs | Premier | short (1/4–1/2 beat), 6-10 per 2 bars | on the 8th grid, gaps between |
| Loose | Dilla | 1/2–1 beat, 5-8 per 2 bars | slid up to 30 ms late / 9 ms early |
| Held | Alchemist | 2-4 per 2 bars, ring to the next hit | on the beat |

## His picks (2026-10-31, clickable)
- Key trust: pack-labelled keys only (the ~105 guessed `synthNN_Key_140` loops are never chopped).
- How often: half of new loops beats chop the lead loop.
- Styles: Claude drafts per identity from the listen line, he approves (table below).
- Resample: 25% of chopped beats get chopped a second time.

## Style per identity (approved 2026-10-31; he moved Memphis, New Orleans Bounce, Mustang to Loose)
| Style | Identities | Why (words in the line) |
|---|---|---|
| Stabs (Premier) | Cutz, Crate Prophet, DJ Premium, Chrome Dial, Glass Cat, Rage Engine, Kane East, Swish Beatz, Timberline, Just Flame, Hitt Kid, DJ Light Green, Well Damn, Crunk, Baltimore Club, Miami Bass, Detroit, Chiptune (18) | "chopped small with gaps", "stabs", "stuttering", "short repeated stab riff", "hard straight pulse", "stutter" |
| Loose (Dilla) | Otto Grit, J Dillo, New Math, Razor, Farrow, Organized Noize, Acid Rap Detroit, Acid Rap Bright, Wonky, + Memphis, New Orleans Bounce, Mustang (his move) (12) | "drunk pull", "not quantized", "loose hand-played", "played like a band", "off the grid" |
| Held (Alchemist) | Doc Day, Half Light, Tenth Wonder, No Alias, Sunday Chop, Night Metro, Fast Water, DJ Hint, Horror Rap, Houston Screw, Emo Hip Hop, Trip Hop, G-Funk, Reggaeton Alt, Plug (15) | "long chopped soul phrases", "one chord held", "loops that start off the beat", "left mostly alone", "room to be talked over", "empty dreamy space" |

## Open choices (asked as clickable questions)
1. Which loops may be chopped (key trust)?
2. How often a loops beat chops instead of playing whole?
3. How each identity gets its chop style?
4. Resample (chop the chop): on, sometimes, or off?

## Done =
His picks built, one focused test that fails if the chop logic breaks,
DECISIONS.md entry (status open). No render, no full test suite.

## Measured (in memory, nothing rendered or played), 29 of his lead loops at 90 BPM
| Style | Silent share of the phrase (median, range) |
|---|---|
| Stabs | 72% (63-73) |
| Loose | 56% (50-68) |
| Held | 31% (0-61) |
New-beat check: 10 of 24 test rolls chopped (half roll, and some leads have no pack key).

## Code
`tools/loop_lanes.py` (chop, chop_roll, chop_ok, CHOP_STYLES), `tools/beat_machine.py`
(_pick_loop_bed rolls the chop), `tools/loop_vocab.py` (chop_style),
`tools/melodic_loops.py` (onset_starts split out of chop_onsets, same output),
`loops_config.json` ("chop" per identity). Test: `tests/test_loop_chop.py`.
Backups: `*.pre-loops-chop-2026-10-31.*`.
