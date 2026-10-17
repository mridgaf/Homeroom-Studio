# Grain

Granular sampler: it plays your sample as tiny overlapping snippets ("grains"),
so you can stretch, freeze, scrub and re-pitch it independently — or play it
straight like a normal sampler. Plus an oscillator, filter, envelopes, LFOs,
Mod Bus and a multi-effect.
Source: Reason 12.7 Operation Manual, ch. 31, pp. 755–786.

Samples are referenced, not saved in the patch — keep the file (or save the song self-contained).

## When you'd use it
- Turning one of YOUR samples (a vocal, a chord, a loop) into a pad or texture.
- Freezing a moment of a sample and playing it as an instrument.
- Tape-stop and scrub effects (Tape algorithm, Speed to 0).
- Playing a loop in time with the song (Motion = Envelope 1, Beat Sync on a ramp).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Algorithm**: how the sample is played — Spectral Grains (FFT; can force it harmonic), Grain Oscillator (tiny grains, pitch from the keyboard, sample only colours the tone), Long Grains (keeps the sample's own pitch), Tape (speed and pitch linked).
- **Motion**: Freeze (stay at Start), One Shot, FW Loop, FW-BW Loop, End Freeze, Envelope 1 (Envelope 1 draws the path through the sample).
- **Position** / **End Pos**: sample start and end. Start after End = plays backwards.
- **Speed**: how fast the playhead moves (0% = stopped; in Tape it's also pitch).
- **Jitter**: random wobble of the play position — makes it alive/chorus-y.
- **Global Position**: new notes carry on from where the playhead is instead of restarting.
- **Grain Length** / **Rate-Spacing** / **XFade**: grain size, spacing/rate, and crossfade between grains (low XFade = gritty/poppy).
- **Pan Spread**: alternate grains left/right (Grain Oscillator: also adds a sub an octave down).
- **Pitch Jitter**: random pitch per grain.
- **Formant** / **Formant Tune**: tone colour (or pitch in Spectral Grains when Snap and Filter are 0).
- **Harm Snap** / **Harm Filter**: Spectral Grains — pull partials onto harmonics / remove the inharmonic ones.
- **FFT Size**: Spectral analysis accuracy (0 fast, 3 catches lows).
- **Curve On** / **Curve Amt**: your drawn formant curve.
- **Oct** / **Semi** / **Tune** / **Pitch Kbd**: pitch; Kbd 100% = normal keyboard.
- **Sample Level** / **Sample To Filter**: sample level and routing to the filter.
- **Osc On** / **Osc Wave** / **Osc Mod** / **Osc Oct** / **Osc Level** / **Osc To Filter**: extra oscillator (sine, triangle, saw, pulse, noise…), handy as a pitch reference under a smeared sample.
- **Filter Type** / **Filter Freq** / **Filter Reso** / **Filter Env2** / **Filter Vel** / **Filter Kbd**: HP12, BP12, LP12, LP24 ladder; Envelope 2 hard-wired to cutoff.
- **Amp Attack** / **Amp Decay** / **Amp Sustain** / **Amp Release** / **Amp Gain**: volume envelope.
- **LFO 1 Rate** / **LFO 1 TempoSync** / **LFO 1 KeySync** / **LFO 1 Global**: LFOs (also 2 and 3).
- **Env 1 Rate** / **Env 2 Rate**: envelope speeds.
- **Effect Select** / **Effect On**: pick/enable an effect in the multi-effect.
- **Dist On** / **Dist Drive** / **Dist Tone** / **Dist Amount**, **Comp On** / **Comp Threshold** / **Comp Ratio** / **Comp Attack** / **Comp Release**, **Delay On** / **Delay Time** / **Delay Sync** / **Delay FB** / **Delay PingPong** / **Delay Amount**, **Reverb On** / **Reverb Size** / **Reverb Decay** / **Reverb Damp** / **Reverb Amount**, **EQ On** / **EQ Freq** / **EQ Gain** / **EQ Q**, **Mod Effect Type** / **Mod Effect Rate** / **Mod Effect Depth**: the effects.
- **Key Mode** (Poly up to 12 / Mono Retrig / Mono Legato), **Portamento** / **Portamento Mode**, **Master Volume**, **Mod Wheel**, **Pitch Bend**.

## Where it shines / falls short
Shines: making something new and musical out of samples he already owns — fits
the no-synthesized-sounds house rule. Falls short: tight, punchy one-shot drum
playback — NN-XT or Kong for that.

## Pairs well with
The Echo, RV7000, MClass Stereo Imager.
