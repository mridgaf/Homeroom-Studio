# NN-XT Sampler

Reason's deep multisampler: many samples spread across keys and velocities,
each "zone" with its own tuning, loop, filter and envelopes. Loads NN-XT/NN-19
patches, SoundFonts, WAV/AIFF and whole REX loops (one slice per key).
Source: Reason 12.7 Operation Manual, ch. 43, pp. 1005–1056.

## When you'd use it
- Playing your own one-shots (kicks, 808s, chops) from the keyboard.
- Real instruments built from many samples (piano, strings) with velocity layers.
- Drum kits where the open hat must be cut off by the closed hat (Group Mono).
- Chopping a REX loop onto keys to replay it in a new order.

## Key controls (front panel)
Named exactly as Reason's Remote layer names them. The front knobs are
offsets: centred = no change; they push every zone's setting up or down at once.

- **Filter Freq**: filter cutoff for all zones. The filter must be switched on in the editor, or this does nothing.
- **Filter Res**: filter resonance for all zones.
- **Amp Env Attack**: how slowly each note fades in.
- **Amp Env Decay**: how fast it falls to the sustain level while held.
- **Amp Env Release**: how long it rings after you let go.
- **Mod Env Decay**: decay of the modulation envelope (what it does depends on what the mod envelope is routed to).
- **Master Volume**: output level.
- **High Quality Interpolation**: better-sounding pitch shifting, more CPU.
- **External Controller** / **External Controller Source**: pick aftertouch, expression pedal or breath as a mod source.
- **Mod Wheel** / **Pitch Bend**: the wheels.

Everything in the Remote Editor (per-zone settings below) is NOT reachable over
Remote — the factory maps only expose the front panel. Automate editor
settings by wrapping the NN-XT in a Combinator.

## Remote Editor essentials (per zone / group)
- **Root Note / Tune**: which key plays the sample at original pitch.
- **Lo Key / Hi Key**, **Lo Vel / Hi Vel**: where on the keyboard and how hard you must play.
- **Fade In / Fade Out**: crossfade between velocity layers instead of a hard switch.
- **Alt**: rotate between zones on repeated hits (no machine-gun repeats).
- **Play Mode**: FW (one-shot), FW-LOOP (loop forever), FW-BW (ping-pong loop), FW-SUS (loop while held, then play the tail), BW (reversed one-shot).
- **Out**: send a zone to its own output pair on the back (separate mixer channel).
- **Key Poly** (group): how many keys can sound at once, 1–99.
- **Group Mono** (group): new note cuts the previous — the open/closed hi-hat trick.
- **Legato / Retrig** (group): legato = mono slides with no new attack (set Key Poly to 1).
- Filter modes: Notch, HP 12, BP 12, LP 6, LP 12, LP 24. K.Track makes the filter follow the key.

## Where it shines / falls short
Shines: realistic multisampled instruments and tight drum kits. Falls short:
fast sound design — Grain, Mimic or Europa get to an interesting sound quicker.

## Pairs well with
Combinator (to macro its editor settings), MClass Equalizer, RV7000.
