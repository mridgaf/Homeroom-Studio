# Alligator

A triple filtered gate. One sound goes in, and Alligator splits it into three
parallel copies — a low pass, a band pass and a high pass. Each copy has its
own gate that chops it on and off in a rhythm, its own filter, and its own
drive and volume. What comes out is a rhythmic pattern made out of a sound
that had no rhythm in it.

## When you'd use it

Point it at something sustained and boring — a held pad, a long chord, a
drone, a loop that's just sitting there — and it comes back as a pattern.
It is the fastest way in Reason to turn a flat sound into a groove without
playing anything.

## Key controls

- **Low Pass Filter On/Band Pass Filter On/High Pass Filter On**: switches that whole band on or off. Off means that copy of the sound disappears.
- **Low Pass Frequency/Band Pass Frequency/High Pass Frequency**: where that band's filter sits. On the low pass, down is darker and thicker; on the high pass, up is thinner and more brittle.
- **Low Pass Resonance/Band Pass Resonance/High Pass Resonance**: how much that band rings and whistles at its own frequency. High resonance is the squelchy, vocal sound.
- **Low Pass Env Amount/Band Pass Env Amount/High Pass Env Amount**: how far the filter envelope sweeps that band's frequency every time its gate opens. This is what makes each hit move instead of sitting still.
- **Low Pass LFO Amount/Band Pass LFO Amount/High Pass LFO Amount**: how much the LFO wobbles that band's filter. Slow and small is a drift; fast and large is a warble.
- **Low Pass Drive Amount/Band Pass Drive Amount/High Pass Drive Amount**: distortion on that band alone. Driving just the band pass is how you get grit in the middle without dirtying the bass.
- **Low Pass Pan/Band Pass Pan/High Pass Pan**: where that band sits left to right. Spreading the three bands apart is the stereo trick Alligator is known for.
- **Low Pass Volume/Band Pass Volume/High Pass Volume**: how loud that band is in the mix of the three.
- **Gate 1 Open/Gate 2 Open/Gate 3 Open**: holds that gate open by hand, ignoring the rhythm. Gate 1 is the low pass, 2 the band pass, 3 the high pass.
- **Gate 1 Trig/Gate 2 Trig/Gate 3 Trig**: fires that gate once, like hitting it.
- **Amp Env Attack**: how fast each gated hit comes in. Slow softens the chop into a swell.
- **Amp Env Decay**: how long each hit lasts before it falls away.
- **Amp Env Release**: how long the tail hangs on after the gate shuts.
- **Filter Env Attack**: how fast the filter sweep starts on each hit.
- **Filter Env Decay**: how fast the filter sweep falls back. Short decay with high Env Amount is the classic pluck.
- **Filter Env Release**: how long the filter takes to settle after the gate shuts.
- **LFO Freq**: how fast the wobble is.
- **LFO Waveform**: the shape of the wobble — smooth, stepped, ramping.
- **LFOSync**: locks the wobble to the song tempo instead of free running.
- **Pattern**: which built-in gate rhythm plays. This is the single biggest change to how it sounds.
- **Pattern Enable**: whether the built-in rhythm runs at all. Off, the gates only open when you play notes or hold one open by hand.
- **Resolution**: how fast the pattern steps go by. Faster is a stutter, slower is a groove.
- **Shift**: slides the whole pattern earlier or later against the beat. A small shift is the difference between stiff and human.
- **Shuffle**: swings the pattern.
- **Ducking**: how far the untreated signal drops out of the way when the gates fire.
- **Dry Volume**: how much of the original untreated sound comes through underneath.
- **Master Volume**: the whole device at once.
- **Enabled**: bypass — on or off for the whole thing.

## What the app can and can't do here

All three bands are reachable in full — filter on/off, frequency, resonance,
envelope amount, LFO amount, drive, pan and volume, on every band. So are both
envelopes, the LFO, all the pattern controls and the three gates. That is 48
controls, which is every slot the surface has.

**Say the band by name.** "Open up the low pass", "more resonance on the band
pass", "drive the high pass harder". The bands are named, not numbered, so
this reads naturally.

**Say the gate NUMBER.** "Open gate 2", not "open the gate" — there are three
and the app refuses to pick one for you.

**Alligator's built-in delay and phaser are not mapped.** That is the one cut:
the per-band delay and phaser sends, Delay Time, Feedback, Pan and Sync, and
Phaser Rate and Feedback — 13 controls, dropped because 61 will not fit in 48.
They still work; you reach them with the mouse. Nothing else about the device
is out of reach.

**Pattern Enable off makes four knobs do nothing.** Pattern, Resolution, Shift
and Shuffle only matter while the internal rhythm is running. The app will
still move them, and you will hear no difference — check that switch first if
a pattern change does nothing.

## Where it shines / falls short

Shines: turning anything sustained into a rhythm in seconds, three-way stereo
splits, and gated filter sweeps that would take three separate devices
otherwise.
Falls short: it is a rhythm generator, not a mix tool — nothing here is
transparent. And the pattern is chosen from a built-in list, so it is a menu,
not something you draw.

## Pairs well with

Anything that holds a note: Subtractor or Thor on a pad, or a Dr. Octo Rex
loop. The RV7000 after it puts one room around all three bands. Scream 4 in
front of it gives the gates something dirty to chop.

## Reference

Reason 12.7 Operation Manual, the Alligator chapter, for the three gates, the
pattern section and the per-band controls. Parameter spellings were taken from
Reason's own Remote vocabulary (`docs/reason/remote-vocab.json`), not from the
panel.
