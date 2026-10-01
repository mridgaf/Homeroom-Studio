# Delay Compensation (digest of Reason 12.7 manual, ch. 18)

Source: `~/.reason_voice/reason12_manual/full_chapters/18-delay-compensation.txt` (manual pp. 501-516). Digested 2026-09-30.
Tag: all **Manual**. Nothing here was tried or heard. Index: [README](README.md)

## In one line
Some effects delay the sound a little. Delay Compensation delays every OTHER channel by the same amount so everything arrives together.
Without it, a channel and its parallel copy that runs through an effect sound phasey or smeared.

## Where the switch is
Three places, same setting: the **Delay Comp button** in the Master Section of the Main Mixer, on the **Transport panel**, and the **Options menu**.
The total delay shows as a number of samples next to it. Hover over the number to see milliseconds.
(The Quazmo demo song had it off: `demo-song-notes-quazmo.md`.)

## How it works (the 12-sample example)
Reason adds up the reported delay of every effect in each channel's chain. The channel with the biggest total gets nothing.
Every other channel gets extra silent delay to match. Four channels at 12, 12, 10 and 3 samples: the 10 gets +2, the 3 gets +9, the 12s get 0.
It recalculates by itself when you add or remove effects.

## What is compensated (standard setups only)
- Effects in series between an instrument and its Mix Channel.
- Insert FX inside a channel (between the To/From Insert FX jacks), including an Effect Combinator in there.
- Effects in series from a channel's **Parallel Out** to another channel.
- Any mix of those three (the delays are added up).
- Signals going from channels to the 8 Send FX buses are kept in step.
- The Metronome click, and bounces (to disk, to new tracks, Bounce in Place).

## What is NOT compensated
| Thing | What happens |
|---|---|
| Rack mixer (Mixer 14:2) channels | No compensation. Only the Main Mixer is covered |
| Channels using **Direct Outs** | Skipped. The channel's delay display shows " - " |
| The Send FX devices themselves | Their own delay is ignored (reverbs and delays hardly matter here) |
| Return channels fed from Send FX | Not compensated |
| **Master Insert FX** (maximizer, mastering EQ) | Not compensated, on purpose: everything passes through together. The Master Section has no Channel Delay display |
| Effects inside an **Instrument** Combinator | Not compensated (Effect Combinators are) |
| CV, MIDI, automation, MIDI Clock, Ableton Link | Not compensated. MIDI Clock Sync Offset can be set by hand |

## Odd routings: the red LED
Splits, feedback loops, cross-routing and effects wired outside the Insert FX section confuse it. Reason uses only the SHORTEST path
and ignores feedback loops and send effects inside the chain. A **red LED** in the Delay Compensation section on the back of the Mix Channel
or Audio Track lights up and a tooltip names the problem. "Could not calculate latency. The default value of 0 samples was used" means a cable is not fully connected.

## Setting it by hand
On the back of the Audio Track / Mix Channel, the unfolded Insert FX section has two displays: the effects' reported delay, and your manual adjustment.
You can only add to the reported figure, never go below it. Works only if the effects are in the Insert FX chain. Use it when a plugin reports its delay wrongly.

## Rules of thumb from the manual (for playing and recording)
1. **Playing an instrument live, or monitoring through Reason: switch Delay Comp OFF**, record, then switch it back on. Otherwise even a clean
   channel is delayed to match the slowest one.
2. Or bypass the Insert FX on the highest-delay channels, and the Master Insert FX, while recording.
3. Recording audio with External Monitoring: Reason moves the clip earlier by input + output latency, plus the Delay Comp total when it is on.

## Ideas for us (not built)
- A voice command "turn delay comp off for recording" (a Transport-panel button; whether the remote map can reach it is NOT checked).
- A line in any recipe that builds a parallel chain (parallel compression): "keep Delay Comp on, or the parallel copy phases."
