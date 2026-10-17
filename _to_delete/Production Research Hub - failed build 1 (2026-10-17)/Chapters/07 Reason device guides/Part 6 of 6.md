# Chapter 07: Reason device guides
## Part 6 of 6

_Plain-language guide for each Reason device (compressors, EQs, reverbs, delays, synths, drums...)._

**In this part:**
- thor.md — Thor
- un-16.md — UN-16 Unison
- yamaha-dtx400k.md — Yamaha DTX400K (your electronic drum kit)
- yamaha-emx66m.md — Yamaha EMX66M (your powered mixer)

(Next: end of chapter)


=====================================================
SOURCE FILE: thor.md
ORIGINAL LOCATION: HS:device_refs/thor.md
=====================================================

# Thor

Reason's big "semi-modular" synth. Three oscillator slots (Analog, Wavetable,
Phase Mod, FM Pair, Multi, Noise), three filter slots (Ladder LP, State
Variable, Comb, Formant), a Shaper, four envelopes, two LFOs, built-in chorus
and delay, a 16-step sequencer, and a modulation matrix that can route almost
anything to anything.
Source: Reason 12.7 Operation Manual, ch. 33, pp. 817–856.

## When you'd use it
- Any classic synth sound: basses, leads, pads, plucks — Ladder filter for warm Moog-ish lows.
- Vowel/talking sounds (Formant filter), bells and metal (FM Pair, Multi).
- Built-in step-sequenced riffs and gated patterns without a Matrix.
- As an effect: its rear audio inputs run other sounds through Thor's filters.

## Key controls
Named exactly as Reason's Remote layer names them. Osc 1 shown; Osc 2 and 3 have the same set.

- **Osc 1 Type**: which oscillator is in the slot.
- **Osc 1 Oct** / **Osc 1 Semi** / **Osc 1 Tune** / **Osc 1 Kbd**: pitch; Kbd fully right = normal keyboard tracking.
- **Osc 1 Mod**: each type's main tone knob — pulse width (Analog; 64 = square), table position (Wavetable), phase distortion (Phase Mod), FM amount (FM Pair; 0 = pure sine), detune amount (Multi), noise character (Noise).
- **Osc 2 Sync To Osc 1** / **Osc 3 Sync To Osc 1**: hard sync to oscillator 1.
- **Osc 1 AM From Osc 2**: ring-mod amount (Osc 2 × Osc 1).
- **Osc 1 And 2 Level** / **Osc 1 And 2 Balance** / **Osc 3 Level**: the mixer.
- **Osc 1 To Filter 1 Enable** / **Osc 1 To Filter 2 Enable**: the routing buttons — nothing reaches a filter until lit.
- **Filter 1 Type**: Ladder LP (6/12/18/24 dB, warm), State Variable (LP/BP/HP/Notch/Peak), Comb, Formant (vowels).
- **Filter 1 Freq** / **Filter 1 Res** / **Filter 1 Drive**: cutoff, resonance, input drive.
- **Filter 1 Env Amount** / **Filter 1 Velocity** / **Filter 1 Kbd** / **Filter 1 Env Invert**: how the filter envelope, playing strength and key move the cutoff.
- **Filter 1 Self Osc**: lets the filter ring as its own tone at high Res.
- **Filter 1 Param X** / **Filter 1 Param Y**: Formant filter vowel position.
- **Filter2ToAmplifier Enable**: Filter 2 output to the amp (parallel filters).
- **Shaper On** / **Shaper Type** / **Shaper Drive**: waveshaper after Filter 1 — Soft/Hard Clip, Saturate, Sine, Bipulse, Unipulse, Peak, Rectify, Wrap.
- **Amp Env Attack** / **Amp Env Decay** / **Amp Env Sustain** / **Amp Env Release**: volume envelope.
- **Filter Env Attack** / **Filter Env Decay** / **Filter Env Sustain** / **Filter Env Release**: filter envelope (Attack up to 10.3 s; Decay/Release up to 29.6 s).
- **Mod Env Delay** / **Mod Env Attack** / **Mod Env Decay** / **Mod Env Release** / **Mod Env Loop** / **Mod Env Tempo Sync**: free envelope; loop + sync = rhythmic modulation.
- **LFO 1 Rate** / **LFO 1 Waveform** / **LFO 1 Delay** / **LFO 1 Tempo Sync** / **LFO 1 Key Sync**: per-voice LFO.
- **LFO 2 Rate** / **LFO 2 Waveform** / **LFO 2 Tempo Sync**: global LFO (needs a mod-matrix route to do anything).
- **Filter 3 Type** / **Filter 3 Freq** / **Filter 3 Res** / **Filter 3 Global Env Amount**: global filter on the summed voices.
- **Global Env Attack** / **Global Env Hold** / **Global Env Decay** / **Global Env Sustain** / **Global Env Release** / **Global Env Loop** / **Global Env Tempo Sync**: single-trigger envelope.
- **Chorus On** / **Chorus Dry Wet** / **Delay On** / **Delay Time** / **Delay Sync** / **Delay Feedback** / **Delay Dry Wet**: built-in effects.
- **Amplifier Gain** / **Amplifier Velocity** / **Amplifier Pan**: voice level, velocity to level, per-voice pan.
- **Key Mode**: Polyphonic (up to 32 voices), Mono Legato, Mono Retrig.
- **Portamento** / **Portamento Mode**: glide time; Off / On / Auto (only on overlapping notes).
- **Rotary 1** / **Rotary 2** / **Button 1** / **Button 2**: assignable front-panel controls (map them in the mod matrix).
- **Step Sequencer Run** / **Step Sequencer Run Mode** / **Step Sequencer Direction** / **Step Sequencer Rate** / **Step Sequencer Synced**: 16-step sequencer — Repeat/1 Shot/Step; Forward/Reverse/Pendulum/Random.
- **Mod 1 Source** / **Mod 1 Dest** / **Mod 1 Dest Amount** / **Mod 1 Scale Amount**: a mod-matrix row (rows 1–13). Amount ±100%; Scale lets a second source (e.g. mod wheel) control how much.
- **Master Level**, **Pitch Bend Range**, **Mod Wheel**.

## Where it shines / falls short
Shines: nearly any synth sound, very deep, CPU-light. Falls short: speed — the
open-slot design and mod matrix take a while; Europa is faster for modern wide sounds.

## Pairs well with
The Echo, RV7000, Scream 4 (after the Shaper for more dirt), Combinator for macro knobs.

=====================================================
SOURCE FILE: un-16.md
ORIGINAL LOCATION: HS:device_refs/un-16.md
=====================================================

# UN-16 Unison

Makes one voice sound like 4, 8 or 16 slightly detuned, slightly delayed copies spread in stereo.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Voice Count**: 4, 8 or 16 voices.
- **Detune**: how far apart they drift. More = thicker, then seasick.
- **Dry/Wet**: full Wet as a send.
- **Enabled**: bypass/on/off.

Back panel: CV in for Detune.

## Where it shines / falls short
Shines: fattening leads, pads, supersaw-style width. Falls short: on bass (smears the low end — keep it off subs).

=====================================================
SOURCE FILE: yamaha-dtx400k.md
ORIGINAL LOCATION: HS:device_refs/yamaha-dtx400k.md
=====================================================

# Yamaha DTX400K (your electronic drum kit)

The e-drum kit. Its brain (the black box with the sticker) makes its own
drum sounds — but the magic trick is that it's ALSO a MIDI controller:
plug it into the Mac and your real sticks can play any drum sound in
Reason. Sampled vintage kits, Kong, Redrum — played with actual hands and
feet instead of pencil-clicking a grid.

## Play Reason's drums with real sticks — 3 steps

1. **USB cable from the DTX brain to the Mac.** Use the square USB port on
   the module (the same kind printers use). Plug in BEFORE opening Reason.
2. **In Reason, click the Kong (or Redrum) track** so it's highlighted —
   same rule as the Launchkey: the highlighted track is who hears you.
3. **Hit the drums.** Snare pad plays Kong's snare, kick pedal plays the
   kick, hats respond to the pedal. Harder = louder, automatically.

If a pad plays the "wrong" drum (say the tom triggers a clap), don't fight
it — either move the sound to that Kong pad, or just use it: wrong-drum
happy accidents are half of hip-hop.

## Why this beats the pencil tool
Grooves you PLAY are loose in a human way that no shuffle knob fully
fakes. Record a pass, delete the bad hits, keep the feel. The "drums with
holes" and "drunken kick" moves in the recipe book are much easier to
play badly-on-purpose than to program badly-on-purpose.

## Practice mode (no Mac needed)
The module works alone too: headphones into the brain, pick a kit with
the drum-numbered buttons, play. The built-in metronome button is the
plain way to build stick timing that then shows up in your Reason takes.

=====================================================
SOURCE FILE: yamaha-emx66m.md
ORIGINAL LOCATION: HS:device_refs/yamaha-emx66m.md
=====================================================

# Yamaha EMX66M (your powered mixer)

The big box with rows of knobs. It's two things glued together: a 6-channel
mixer (blends microphones and instruments) AND a 300-watt-per-side power
amp (makes it loud enough for speakers). That's what "powered mixer" means
— you don't need anything else between it and a pair of passive speakers.

## Plain-words tour, top to bottom
- **Each channel strip** (the vertical rows): HIGH / MID / LOW knobs are
  tone (treble, middle, bass), MONITOR sends that channel to stage
  monitors, EFFECT sends it to the built-in echo/reverb, LEVEL is how loud
  that channel is in the mix.
- **DIGITAL EFFECT buttons**: built-in vocal echoes, reverbs, halls. Pick
  one, press ON, and turn a channel's EFFECT knob up to hear it on that
  channel.
- **GEQ sliders** (the two rows of little faders): overall tone shaping.
  If the room booms, pull down 125; if vocals sting, pull down 2k–4k.
- **PHANTOM switch**: 48V for condenser mics — same rule as the AudioBox:
  ON for studio condensers, OFF for everything else.
- **Bottom jacks**: XLR mic inputs per channel, Hi-Z for guitars,
  MAIN out to speakers, MONITOR out to wedges, FOOT SW for effect on/off.

## When to use it vs the AudioBox
- **Recording into Reason** → AudioBox. Always.
- **Being LOUD in a room** (practice, a party, vocals over your beats) →
  the EMX66M. Play the Mac's output into a channel (the LINE/CD input
  works), mic into another channel, balance with the LEVEL knobs.
- **REC OUT** on the mixer can feed the AudioBox inputs if you ever want
  to record a live jam mix into Reason — one cable pair, LEVEL knobs
  become your recording balance.

=== END OF PART ===
