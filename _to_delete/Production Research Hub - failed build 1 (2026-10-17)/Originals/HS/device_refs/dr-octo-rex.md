# Dr. Octo Rex Loop Player

A loop player that holds **eight** REX loops at once, one per slot, and plays
one at a time. A REX loop is a loop that has already been cut into slices at
every hit, so it follows your song tempo without changing pitch — and the
slices can be treated as separate sounds.

Reason calls this device `Dr.REX Loop Player` when it talks to a control
surface. Same device, older name.

## When you'd use it

When the loop IS the song — boom-bap flips, breakbeats, anything built on a
sampled bar. Load eight variations (main, fill, drop, half-time) in the eight
slots and switch between them instead of programming a drum part.

It is also the one device here that reads your sealed ReFills natively, so the
whole factory loop library is available without anything being indexed first.

## Key controls

- **Select Loop**: the eight slots. "Go to loop 3" switches which loop plays. Say the slot NUMBER.
- **Selected Loop Slot**: the same choice as one dial instead of eight buttons.
- **Trigger Next Setting**: WHEN a slot switch lands — next bar, next beat, or next 1/16. Bar is musical, 1/16 is snappy.
- **Run**: starts and stops the loop without the transport.
- **Enable Loop Playback**: turn this OFF and the device stops looping and becomes a slice sampler — the keyboard plays one slice per key from C1 up. The single biggest thing this device does that is not obvious.
- **Follow Loop Playback**: keeps the slice display tracking what is playing.
- **Notes to Slot**: which of the eight slots your keyboard is playing.
- **Selected Loop in Editor**: which slot the loop knobs below are pointed at.
- **Transpose**: pitches every loop in the device. On drums this is a varispeed effect, not a key change.
- **Loop Transpose**: pitches only the loop in the selected slot.
- **Loop Level**: the volume of the loop in the selected slot.
- **Osc Env Amount**: sends the FILTER envelope to slice PITCH. This is the vinyl-scratch and warped-pop knob — nothing else in Reason does it. Small amounts warble, large amounts scratch.
- **Osc Octave / Osc Fine Tune**: coarse and fine tuning over the whole device.
- **Amp Env**: an attack/decay/sustain/release shape applied to EVERY slice. Decay down with sustain at zero gives a hard gated stutter; attack up past a fifth of the way gives a slow, backwards-sounding swell.
- **Amp Vel Amount**: how much harder playing makes slices louder.
- **Filter Env**: the same envelope idea on the filter, re-triggered on every slice. With the filter frequency low, resonance high and this amount high, you get a 303-style swoop on each hit.
- **Filter**: frequency, resonance, mode (notch, high pass, band pass, low pass 12, low pass 24) and an on/off. Note that the envelope is usually driving the frequency, so moving Freq alone may do less than expected.
- **LFO Sync**: locks the LFO's rate to the song tempo instead of free-running.
- **LFO1**: rate, amount, waveform and destination — a slow wobble over the whole loop. What Amount means depends on where Dest is pointed.

## What the app can and can't do here

**Say the slot NUMBER.** "Go to loop 3", "switch to loop 7". Reason never tells
a control surface which loop is loaded in which slot, so "play the drum loop"
has no answer and the app refuses to guess.

**Loop Transpose and Loop Level move whichever slot is selected in the editor**,
not the one playing. If they seem to do nothing, that is why — check
Selected Loop in Editor first.

**Nothing slice-level is reachable.** Slice pitch, pan, level, decay, reverse,
alt group and slice output are not parameters Reason exposes to a control
surface at all. So the famous Octo Rex tricks that live down there — alt-group
randomising, sending just the snare slices to a reverb through the eight back
outputs, drawing modulation in Slice Edit Mode — can only be done with the
mouse. The app will not pretend otherwise. Same limit as Kong's drum-module
knobs.

**The settings can be said by name now, not just as percentages.** Rex reports
every picker to the app as a bare number — "3" where the panel says LP 12 — so
until 2026-09-12 a phrase like "stop the loop" was heard, understood, and then
did nothing at all. The panel's own words are now filled in from the manual:

| Control | Say one of |
|---|---|
| Filter Mode | Notch, HP 12, BP 12, LP 12, LP 24 |
| LFO1 Wave | Triangle, Inverted Sawtooth, Sawtooth, Square, Random, Soft Random |
| LFO1 Dest | Osc, Filter, Pan |
| Trig Next | Bar, Beat, 1/16 |
| Run, Enable Loop Playback, Follow Loop Playback, Filter, LFO Sync | Off, On |

**Transpose takes real semitones.** "Pitch the loop down two semitones" lands on
−2, not near it. Same for Loop Transpose, and Osc Fine Tune takes cents.

**Osc Octave still takes percentages only.** It reads 0 to 8 and nothing outside
Reason knows which of those is neutral — calling 4 "4 octaves" when it means no
change would be worse than leaving it a bare number.

**The eight Select Loop buttons take percentages only.** They report "1" at
every position no matter what is written to them, so there is nothing to look a
number up in. "Go to loop 3" still works — it moves the knob, it just can't
read back where it landed.

**Master Level is not mapped.** It is spelled the same on Scream 4, which
would leave the app unable to tell the two apart. Loop Level does the job and
is per-slot anyway.

## Where it shines / falls short

Shines: instant tempo-following loops, eight variations under one hand, and a
full synth filter and envelope section wrapped around a sample.
Falls short: everything interesting about individual slices is mouse-only, and
it only plays one slot at a time — for two loops at once you need two devices.

## Pairs well with

Scream 4 and the MClass EQ for the lo-fi flip; Kong for one-shots under the
loop. Kong's pads can also be cabled to a Rex device's volume to turn loops
into an Ableton-style clip launcher — that is a cable job, not a voice one.

## Reference

Reason 12.7 Operation Manual, chapter 29 "Dr. Octo Rex Loop Player"
(pp. 695-718) for the parameters — the filter modes, LFO waveforms, LFO
destinations and Trig Next settings above are that chapter's own lists, in its
order. The slice-sampler mode, the Osc Env pitch trick and the envelope
gating are covered in Sound On Sound, "Introducing Dr OctoRex" (January 2011)
and ModeAudio, "The Art Of Loop Mangling" (January 2015) — the manual lists
those controls but never says what they are for.
