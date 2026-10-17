# ECF-42 Envelope Controlled Filter

Resonant filter with its own envelope. The envelope does NOT follow the audio —
it fires only from a gate (Matrix, Redrum gate outs) or MIDI notes on its own
sequencer track. With audio only, it's a static filter.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Mode**: 24 dB lowpass, 12 dB lowpass, 12 dB bandpass.
- **Frequency**: cutoff; also where the envelope sweep starts and ends.
- **Resonance**: emphasis at the cutoff — more "synthy".
- **Env Amount**: how far the envelope opens the filter. If Frequency is already high this does little — lower Frequency.
- **Velocity**: how much the gate/note velocity scales Env Amount.
- **Attack** / **Decay** / **Sustain** / **Release**: the filter envelope.
- **Trigger**: fires the envelope, same as a gate arriving (remote-controllable).
- **Enabled**: bypass/on/off.

Back panel: CV in for Freq, Decay, Res; Env Gate in.

## Tricks from the manual
- Right-click > "Create Track for …", draw notes: note length + velocity (not pitch) shape the filter.
- Matrix Gate → Env Gate and Matrix Curve → Freq CV = pattern-controlled filter.
- Redrum gate outs → Spider CV → Env Gate = filter pumping in time with the drums.

## Where it shines / falls short
Shines: rhythmic filter chops on pads and loops. Falls short: needs a gate or
track to be more than a static filter.
