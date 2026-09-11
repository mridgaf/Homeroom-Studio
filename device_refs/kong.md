# Kong Drum Designer

A 16-pad drum instrument. Each pad is its own little drum machine: a drum
module that makes the sound, two effect slots on top of it, and a set of macro
knobs that shape whatever is in there.

## When you'd use it

When you want to build a kit pad by pad and shape each drum on its own —
rather than Redrum, which is faster for a pattern but shallower per sound.

## Key controls

- **Level**: how loud that pad is. The first thing to reach for when a drum sits wrong against the others.
- **Pitch Offset**: tunes the whole pad up or down. On a kick this is the difference between a thud and a boom.
- **Tone**: a built-in filter, same idea as Redrum's tone. Up is brighter, down is duller.
- **Decay Offset**: how long the sound rings. Short for tight and modern, long for a room-y tail.
- **Pan**: where it sits left to right. Leave kick and snare centred.
- **Bus FX Send**: how much of the pad goes to Kong's shared effect. One reverb or delay for the whole kit lives here.
- **DM Pitch / DM Decay / DM Level**: the drum module's OWN pitch, decay and level, underneath the macro knobs above. What they do depends on which module is loaded.
- **FX1 / FX2**: two effect slots per pad, each with an on/off and two controls whose job depends on which effect is loaded.

## What the app can and can't do here

All 16 pads are reachable, three controls each: **Level, Pitch Offset and
Decay Offset**. Those three mean the same thing no matter which drum module is
loaded, so real values and percentages both work on every pad.

**Say the pad NUMBER.** "Turn up pad 5", "tune drum 9 down". Reason never tells
a control surface what is loaded on a pad, so the app cannot know which pad
holds the snare — asking for "the snare" by name is a guess, and it refuses to
guess.

The Tone, Pan, Bus FX Send, drum-module and per-pad effect controls are not
mapped. There are 48 knob slots and 16 pads; reaching every pad cost the depth.
The module and effect knobs were the cheapest half to give up — they scale
whatever is loaded in the slot, which Reason never reports, so they could only
ever take percentages anyway.

## Where it shines / falls short

Shines: deep per-drum control, two effects per pad, a shared bus effect.
Falls short: every parameter names its pad number and there is no "the
selected pad" to talk to, so a control surface has to spend a slot per pad per
control — 16 pads x 6 macro knobs would need 96 slots and only 48 exist.

## Pairs well with

Redrum for quick patterns; the RV7000 on Kong's Bus FX for one room around the
whole kit.

## Reference

Reason 12.7 Operation Manual, chapter 27 "Kong Drum Designer" — the Drum
Control Panel section for the macro knobs, and "Physical Modelling Drums" for
the bass-drum module's own head, shell and beater parameters.
