# MClass Maximizer

Loudness limiter for the end of the chain. 4 ms look-ahead for true brick-wall
limiting, plus a Soft Clip stage that adds warm saturation.
Source: Reason 12.7 Operation Manual, ch. 61, pp. 1273–1280.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Input Gain**: pushes the mix into the limiter (±12 dB). This is the "louder" knob.
- **Limiter Enable**: the limiter section on/off.
- **Look Ahead Enable**: 4 ms preview of peaks. On + Attack Fast + Output 0 dB = nothing gets over 0 dB.
- **Attack Speed**: Fast / Mid / Slow. Slower keeps more punch but lets peaks through.
- **Release Speed**: Fast / Slow / Auto. Auto adapts to the music — a safe default.
- **Output Gain**: leave at 0 dB normally.
- **Soft Clip Enable** / **Soft Clip Amount**: warm clipping at 0 dB. With Amount at zero it's harsh hard-clip, so give it some Amount.
- **Output Level Meter Mode**: Peak (fast) or VU (average loudness).
- **Enabled**: bypass/on/off.

## Where it shines / falls short
Shines: quick safe loudness on a beat or demo; Soft Clip adds pleasant grit on
drums. Falls short: no LUFS or true-peak metering, so check loudness elsewhere.

## Pairs well with
MClass Equalizer (Low Cut on) → MClass Compressor → MClass Stereo Imager → this. That is exactly Reason's factory "Mastering Combi" layout.
