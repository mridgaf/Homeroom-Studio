# Sweeps by voice: 3 named types + a running phrase list (item 31)

Owner 2026-09-30: "Wanted, small first." Research first, name three sweep types, keep a running list of
phrases he can reference and add to. Tags: **Source** = read on a page, **Seen** = looked at in a demo song on
this Mac, **Guess** = my reading.

## Honest note on "professional producers"
The pages I found (Soundfly, Perfect Circuit, a producer forum thread) describe techniques; they do **not** name
specific producers doing each one, apart from passing mentions (DJ intros, Rush "Tom Sawyer", the Chemical
Brothers' resonant low-pass swell). I am not putting a producer's name on a technique I can't source. The three
demo songs on this Mac (Street Phone, Airplane, Power) are the real examples below.

## The three types

| # | Name | What you hear | What moves | Typical length | Where it came from |
|---|---|---|---|---|---|
| 1 | **Fill-In** | Starts thin and tinny, bass and body arrive by the end (the DJ-intro sound) | High-pass / low-cut cutoff, from high to low (Source example: 8 kHz down to 20 Hz) | one intro or section, 4-16 bars | Source: Soundfly. Seen: Street Phone Organ 1 filter, a stepped version over bars 9-21 (Guess: a staircase) |
| 2 | **Build and Snap-Back** | Lows drain out during a build, then everything returns on the drop | High-pass cutoff on the bass/loop rises slowly, then jumps back down on the downbeat | 4-8 bars up, instant back | Source: r/trapproduction comment ("slowly removing the low frequencies, then bring it all the way back for extra energy") |
| 3 | **Throw** | The voice or a hit suddenly splashes into reverb or delay, then dries up | A reverb or delay SEND switched on (or turned up) for a short stretch | 1-2 bars | Seen: Street Phone Main Vox send lanes (FX1/FX2/FX4 on/off clips at bars 24-29, 49-61; Guess that they hold "on"). Source: forum says reverb is among the most automated things |

Runners-up, not built into the first three: **Wobble** (filter driven by a rhythm, Source: Perfect Circuit),
**Sidechain-depth ride** (how hard the kick ducks, Source: forum), **Reverse swell** (slow rise, sudden end,
Source: Perfect Circuit).

## Running phrase list (add to it; one line per idea)

Rule of thumb from the app's existing design: **one knob per phrase**, bars not seconds, plain words.
Status: `live` = works today (one knob moved now, not stored in the song), `needs build` = would write a move
over time (nothing in `reason_voice/` does this yet; proven by hand on Scream 4, needs the device to have its own
sequencer track and Reason recording: `experiments/automation-test-2026-09-25/RESULTS.md`).

| Phrase | Type | Status |
|---|---|---|
| "filter down 20 percent" | (single move) | live (existing nudge) |
| "sweep the filter up over four bars" | generic sweep | **live 2026-09-30** (recorded + played back in Reason) |
| "sweep the filter down over eight bars" | generic sweep | **live 2026-09-30** |
| "open the filter over eight bars" | 1 / 2 (low-pass opens) | needs build |
| "fill in over eight bars" | 1 Fill-In (high-pass from high to low) | **live 2026-09-30**: a sweep DOWN of "low cut or high pass"; proven on a Scream 4 (Cut Lo), not on a real filter |
| "build the high pass over four bars" | 2 Build | needs build |
| "snap back" | 2 Snap-Back (return to where it started) | **live 2026-09-30**: records at the playhead a jump to where the last sweep/throw began, holds 1.5 s |
| "throw the reverb for one bar" | 3 Throw | **live 2026-09-30** on any device knob ("the" knob the model picks, goes to the top for N bars then back); mixer sends not wired |
| "sweep the filter from 500 hertz to 4 kilohertz over two bars" | generic, exact ends | needs build |

### Open choices for later (not decided)
- Where does a sweep start in time: now, the playhead, or a selected bar? (Guess: playhead.)
- Does "sweep up" end at the knob's top, or at a number he says?
- Who records: the app presses Record and plays, or he does?
