# Synchronous

Tempo-locked effect "loop" machine: you DRAW up to three modulation curves
(2 bars long by default, 1–4 bars with speed) and they move its built-in
distortion, filter, delay, reverb and level in perfect sync with the song.
Source: Reason 12.7 Operation Manual, ch. 60, pp. 1253–1272.

## When you'd use it
- Rhythmic filter chops, gated/"trance-gate" volume, stutter delays on a loop.
- Mangling a Dr. Octo Rex or Redrum output bar after bar.
- Gated or reverse-style reverb (Reverb in Return mode + a curve on Amount).

## Key controls
Named exactly as Reason's Remote layer names them. Note: Reason spells
**Delay  Amount** with TWO spaces — copy it exactly.

- **Dist On** / **Dist Type** / **Dist Amount** / **Dist Character**: two distortions, ring mod (Character = ring pitch), lo-fi (Character = sample rate, no anti-aliasing).
- **Dist Post Filter**: put distortion after the filter to keep its new highs.
- **Filter On** / **Filter Type** / **Filter Freq** / **Filter Reso**: 12 dB HP, 6 dB BP, 24 dB LP, comb.
- **Filter Lag**: glide on the filter moves — smooths steppy curves.
- **Delay On** / **Delay  Amount** / **Delay Time** / **Delay Tempo Sync** / **Delay Synched Time** / **Delay Feedback** / **Delay Pan** / **Delay Ping Pong** / **Delay Keep Pitch**: delay.
- **Delay Roll**: stutter mode — turning Feedback up freezes the repeat; back to 0 to release.
- **Delay SendReturn**: where Amount sits (before or after the delay).
- **Reverb On** / **Reverb Amount** / **Reverb Decay** / **Reverb Size** / **Reverb Damp** / **Reverb SendReturn**: reverb.
- **Level** / **Level InOut**: level stage (−∞ to +12 dB), modulatable — this is the volume-gate.
- **DryWet**: 0 = whole device bypassed.
- **Master Level**: output, −∞ to +12 dB.
- **Enabled**: bypass/on/off.

## The display (drawing the curves)
- Tools: waveforms (with a Rate button: 1/4, 1/8…) or free/stepped lines. Smallest step = 1/16 at Speed ×1.
- Per curve: **Speed** ×0.5 (4 bars) / ×1 (2 bars) / ×2 (1 bar), **Phase**, loop length marker, **FRZ** (hold current value), **Kill** (mute curve).
- **Master Offset** shifts where the loop starts (±32 steps).
- Pick a curve, then turn the small modulation knob above any effect knob to set how much (and which direction) that curve moves it.
- Offset, Speed and Phase can be automated.

## Where it shines / falls short
Shines: tight, musical, repeatable movement with zero MIDI programming. Falls
short: anything that shouldn't repeat every 1–4 bars — automate instead.

## Pairs well with
Dr. Octo Rex, Redrum, Kong bus, pads.
