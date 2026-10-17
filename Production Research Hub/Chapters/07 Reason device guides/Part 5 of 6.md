# Chapter 07: Reason device guides
## Part 5 of 6

_Plain-language guide for each Reason device (compressors, EQs, reverbs, delays, synths, drums...)._

**In this part:**
- redrum.md — Redrum Drum Computer
- rpg-8.md — RPG-8 Arpeggiator
- rv-7.md — RV-7 Digital Reverb
- rv7000-mkii.md — RV7000 MkII
- rytmik.md — Rytmik Drum Machine
- samson-servo-300.md — Samson Servo 300 (your rack power amp)
- scream-4.md — Scream 4
- subtractor.md — SubTractor
- sweeper.md — Sweeper
- synchronous.md — Synchronous
- the-echo.md — The Echo

(Next: Part 6 of 6)


=====================================================
SOURCE FILE: redrum.md
ORIGINAL LOCATION: HS:device_refs/redrum.md
=====================================================

# Redrum Drum Computer

A 10-channel drum machine with a 16-step pattern sequencer built in. Each
channel plays one sample and has its own small set of controls.

## When you'd use it

When you want a pattern fast. Redrum is shallower per drum than Kong but the
step sequencer is right there on the front panel, so a beat happens in
seconds.

## Key controls

- **Level**: how loud that channel is. The first thing to reach for when a drum sits wrong against the others.
- **Pitch**: tunes that channel up or down. On a kick this is the difference between a thud and a boom.
- **Length**: how long the sound lasts. Short for tight and modern, long for a room-y tail. What it does depends on the channel's Decay/Gate switch — in Decay it fades out over that time, in Gate it cuts off dead at it.
- **Pan**: where it sits left to right. Leave kick and snare centred.
- **Tone**: a built-in filter on channels 1, 2 and 10 only. Up is brighter, down is duller.
- **Send 1 / Send 2 Amount**: how much of that channel goes to Redrum's two effect sends.
- **Master Level**: the whole kit at once.
- **Flam Amount**: how far apart the two hits of a flam land.
- **Shuffle**: swings the pattern. The amount is set by the song's global shuffle.

## What the app can and can't do here

All 10 channels are reachable, four controls each: **Level, Pitch, Length and
Pan**. Those four mean the same thing on every channel no matter which sample
is loaded, so real values and percentages both work everywhere.

**Say the channel NUMBER.** "Turn up drum 3", "tune channel 7 down". Redrum
does report which sample sits on a channel, but the app does not read it yet —
so asking for "the snare" by name would be a guess, and it refuses to guess.

Tone, the two effect sends, Vel to Level, the Decay/Gate switch, the mute and
solo buttons, the pattern buttons and the sequencer steps are not mapped. Four
controls on ten channels is 40 of the 48 slots that exist.

## Where it shines / falls short

Shines: a pattern in seconds, ten sounds on one panel, two effect sends built
in.
Falls short: one sample per channel with no layering, and Length is the only
shaping there is — no envelope, no filter except on three channels.

## Pairs well with

Kong when one drum needs real shaping; the RV7000 on a Redrum send for one
room around the whole kit.

## Reference

Reason 12.7 Operation Manual, chapter 26 "Redrum Drum Computer" — the Drum
Sound Settings section for the per-channel controls, and "Using the Pattern
Sequencer" for the steps and flam.

=====================================================
SOURCE FILE: rpg-8.md
ORIGINAL LOCATION: HS:device_refs/rpg-8.md
=====================================================

# RPG-8 Arpeggiator

Turns held notes/chords into arpeggios and sends them to an instrument via CV
(monophonic — one voice). Makes no sound itself. Has a 16-step rest pattern.
Source: Reason 12.7 Operation Manual, ch. 65, pp. 1343–1358.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Arpeggiator Enable**: on/off (off = plain MIDI-to-CV converter).
- **Mode**: Up, Up+Down, Down, Random, Manual (order you played).
- **Octave 1** / **Octave 2** / **Octave 3** / **Octave 4**: range of the arpeggio.
- **Insert Off** / **Insert Low** / **Insert High** / **Insert 3-1** / **Insert 4-2**: repeat-note variations.
- **Rate** / **Sync**: note value (1/2–1/128, dotted, triplet) or free 0.1–250 Hz.
- **Gate Length**: note length; full = "Tie" (legato).
- **Shuffle**: swing, amount set by ReGroove's global shuffle.
- **Single Note Repeat**: whether a single held note re-triggers.
- **Hold**: keeps arpeggiating after you let go (follows sustain pedal).
- **Octave Shift Up** / **Octave Shift Down**: ±3 octaves.
- **Velocity/Manual** / **Manual Velocity**: fixed velocity, or pass through what you played.
- **Pattern Enable** / **Pattern Length Up** / **Pattern Length Down**: 16-step rest pattern (rests don't skip notes).

## Handy
- Edit > "Arpeggio Notes to Track" renders the arp to real, editable notes on the instrument's track (then mute the Arp track).
- Recording on the Arp track records the chords you played, not the arp notes.

## Where it shines / falls short
Shines: instant arps and rhythmic riffs. Falls short: mono only — one arp voice per RPG-8.

=====================================================
SOURCE FILE: rv-7.md
ORIGINAL LOCATION: HS:device_refs/rv-7.md
=====================================================

# RV-7 Digital Reverb

Simple, light-on-CPU reverb with ten preset spaces. Use as a send when several
instruments share one room.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Algorithm**: Hall, Large Hall, Hall 2 (brighter), Large Room, Medium Room, Small Room (drum booth), Gated (80s cut-off), Low Density (grainy, cheapest on CPU), Stereo Echoes, Pan Room.
- **Size**: centre = the algorithm's normal size. Down = closer, boxier; up = bigger, longer pre-delay. In Stereo Echoes / Pan Room it sets the echo time.
- **Decay**: tail length (centre = default). Ignored by Gated.
- **Damping**: cuts the reverb's highs — warmer, darker.
- **Dry/Wet**: full Wet when used as a send.
- **Enabled**: bypass/on/off.

Back panel: CV in for Decay.

## Where it shines / falls short
Shines: quick, cheap, lo-fi-friendly spaces; Gated snare. Falls short: realism
and control — RV7000 does that.

=====================================================
SOURCE FILE: rv7000-mkii.md
ORIGINAL LOCATION: HS:device_refs/rv7000-mkii.md
=====================================================

# RV7000 MkII

Reason's flagship reverb: nine algorithms, a built-in EQ, and a gate section, programmed through the fold-out Remote Programmer panel. Also does convolution (loads impulse responses) as of MkII.

## When you'd use it
- Any serious reverb job: vocal plates, drum rooms, gated 80s snares, hall washes. The convolution mode loads real-space IRs for realism the algorithms can't match.

## Key controls
- **Algorithm** (in Remote Programmer): Hall, Room, Plate, Spring, Echo, Multi-tap, Reverse, Arena, Convolution. Plate for vocals, Room for drums are the workhorses.
- **Edit Mode**: which page the programmer shows — Reverb, EQ or Gate. It is a button: it steps through the three. The dials mean different things on each page, which is why the app sets this itself before it names a reverb type.
- **Decay**: tail length. Under 1 s = space; over 2.5 s = effect.
- **HF Damp**: rolls treble off the tail — almost always ON for natural results.
- **Predelay**: gap before the reverb starts. 20–40 ms keeps vocals intelligible inside big reverbs.
- **EQ button**: post-reverb EQ. Low-cut the tail (~200 Hz) on almost everything — reverb mud is the #1 mix killer.
- **GATE button**: the 80s gated-reverb section — threshold, hold, release. Also CV-triggerable.
- **Dry/Wet**: 100% wet on sends; blend as insert.

## Where it shines / falls short
Shines: everything reverb, honestly — it has aged well, and convolution mode keeps it modern. Falls short: ultra-modern shimmer/modulated tails (that's Valhalla territory, free VST3 fills it).

## Pairs well with
One instance on a send shared across drums + vocal for "same room" cohesion; CV gate tricks with Redrum.

=====================================================
SOURCE FILE: rytmik.md
ORIGINAL LOCATION: HS:device_refs/rytmik.md
=====================================================

# Rytmik Drum Machine

Simple 8-channel drum sample player with built-in samples, a distortion and
low/hi-cut per channel, shared delay and reverb, and a master compressor.
Samples are embedded, so patches always carry their sounds.
Source: Reason 12.7 Operation Manual, ch. 38, pp. 927–942.

**No Remote names:** Reason's factory control-surface maps don't include Rytmik,
so the bridge has no verified parameter names for it. Don't guess any.

## Controls (panel labels, from the manual)
- Per channel: sample choice, Start/End, Pan, Pitch, Fade In/Out, Distortion, Low Cut / Hi Cut, Volume, Mute/Solo, Delay and Reverb sends. Channels play from keys C0–G0.
- Delay: Stereo or Ping Pong, tempo-locked, 1/1 to 1/16 incl. dotted and triplet; Feedback.
- Reverb: Room, Large Room, Culvert, Plate, Gated, Hall; Decay; low/hi cut.
- Master: Compressor (Threshold 0 dB or Ratio 1.00 = off), Master Pitch, Master Reverb, Master Filter (HP+LP), Master Volume.
- Back: Drum Gate in/out per channel; separate outs (these skip the master FX).

## Where it shines / falls short
Shines: fast built-in kit for sketches. Falls short: it plays its OWN samples,
not his library — Kong, Redrum or NN-XT load his one-shots.

=====================================================
SOURCE FILE: samson-servo-300.md
ORIGINAL LOCATION: HS:device_refs/samson-servo-300.md
=====================================================

# Samson Servo 300 (your rack power amp)

The flat rack unit with the two big knobs and level meters. It does exactly
one job: takes a quiet line signal and makes it strong enough to drive
passive speakers. No tone controls, no effects — volume left, volume
right, done. 300 watts total.

## When you'd actually use it
- **Passive monitors or spare speakers**: AudioBox main outs → Servo 300
  inputs → speakers. Now your interface has a speaker system.
- **Extra monitor send at practice**: EMX66M's MONITOR out → Servo →
  a wedge, so vocals can be louder in one spot of the room.

## The two rules that keep it alive
1. **Knobs down before power on.** Turn both volume knobs all the way
   down, power everything else first, the Servo LAST, then bring the
   knobs up. (Reverse order to shut down: Servo off FIRST.)
2. **Watch the PEAK light.** Flickering red at loud moments is the amp
   saying "that's all I've got." Constant red = turn down before a
   speaker pays for it.

## What NOT to plug in
Never plug a speaker output from another amp (like the EMX66M's MAIN
outs) into the Servo's inputs — amp-into-amp is how gear dies. It wants
line-level sources only: interface outs, mixer line outs, monitor sends.

=====================================================
SOURCE FILE: scream-4.md
ORIGINAL LOCATION: HS:device_refs/scream-4.md
=====================================================

# Scream 4

Distortion and destruction unit with ten damage algorithms — Reason's main saturation, overdrive, and lo-fi tool. Used in more recipes here than any other effect.

## When you'd use it
- Parallel grit on vocals (Tube), 808 harmonics (Tape), vintage sampler grime (Digital), fuzz walls (Fuzz), speaker-cab impressions (Body section).

## Key controls
Named exactly as Reason's Remote layer names them, because the voice dial reads
these lines to decide which knob you meant.

- **Damage Control**: overall intensity of the dirt. Most musical range is 20–60; past 75 everything becomes the same buzz.
- **Damage Type**: the algorithm — Tube/Tape = warmth, Overdrive/Distortion/Fuzz = increasing aggression, Digital = bit/rate crush, Modulate/Warp = weird, Feedback/Scream = unusable-until-they're-perfect.
- **Parameter 1**: the P1 knob. Means something different per Damage Type (Tape: compression). Sweep it after picking a type.
- **Parameter 2**: the P2 knob. Same deal (Tape: speed).
- **Cut Lo**: low band of the 3-band EQ that sits AFTER the damage. Pull this down on parallel chains to keep mud out.
- **Cut Mid**: mid band, after the damage. Where the honk and the bite live.
- **Cut Hi**: high band, after the damage. Down for darker/older, up for fizz and air.
- **Master Level**: output volume. Distortion adds loudness, so this is how you match levels before and after.
- **Body Type**: resonant-cavity shape, a crude cab sim — A, B, C, D, E for different sizes. Useful on bass and drums, cheesy on vocals.
- **Body Resonance**: how ringing and hollow the cavity sounds.
- **Body Scale**: the size of that cavity — moves the resonant note.
- **Body Auto**: lets the body follow the incoming signal instead of sitting still.
- **Damage On/Off**: the distortion section's own switch. Off means clean through.
- **Cut On/Off**: the EQ section's switch.
- **Body On/Off**: the cab-sim section's switch.
- **Enabled**: bypass/on/off for the whole device.
- **CV inputs**: Damage Control is CV-controllable — an LFO here makes evolving degradation.

## Where it shines / falls short
Shines: parallel saturation, drum busses, lo-fi color. Falls short: convincing guitar amp tones (Body is not a real cab sim) and transparent "mastering" saturation — it always has a flavor.

## Pairs well with
Spider Audio (parallel routing), Combinator 2 macro on Damage, MClass EQ before it to shape what gets distorted.

=====================================================
SOURCE FILE: subtractor.md
ORIGINAL LOCATION: HS:device_refs/subtractor.md
=====================================================

# SubTractor

Reason's original analog-style subtractive synth: two oscillators, two filters, three envelopes, one LFO-and-a-half. Old, mono-timbral, CPU-cheap — and still the fastest route to basses and 808s in the rack.

## When you'd use it
- 808s and sub bass (sine osc + mod-env pitch drop), simple analog leads, quick layer tones, CV-modulation experiments (huge CV I/O on the back).

## Key controls
- **Osc 1/2 waveform**: 32 waves; 1–4 are the classics (saw, square, triangle, sine). Phase-offset modes (o, x, –) fake pulse-width and extra harmonics.
- **Filter 1**: LP24 is the default character; the LINK button makes Filter 2 track it for steeper slopes.
- **Mod Envelope**: routable to pitch, phase, FM, or filter 2 — the pitch destination is the 808/kick knock trick.
- **Amp Envelope**: standard ADSR. For basses: sustain high, release short. For plucks: sustain 0, decay does the work.
- **Portamento + Legato**: the trap 808 slide lives here.
- **Noise section**: replaces Osc 2 — mix a little in for analog hiss or snare synthesis.
- **Back panel CV**: nearly everything is CV-controllable — this is SubTractor's secret weapon in Combinators.

## Where it shines / falls short
Shines: bass, mono leads, learning subtractive synthesis (every control visible at once). Falls short: pads and anything needing unison/detune width or modern wavetables — that's Europa's job. No effects onboard.

## Pairs well with
Scream 4 (it's dry and polite alone), Combinator 2 macros, Matrix Pattern Sequencer via CV for acid lines.

=====================================================
SOURCE FILE: sweeper.md
ORIGINAL LOCATION: HS:device_refs/sweeper.md
=====================================================

# Sweeper

Phaser, flanger or filter (Europa's filters) with an LFO plus a drawable
envelope or an audio follower to sweep it — tempo-synced movement on anything.
Source: Reason 12.7 Operation Manual, ch. 47, pp. 1103–1122.

## When you'd use it
- Deep, modern phasers (up to 40 stages) and flangers on keys, pads, loops.
- Tempo-synced filter sweeps and gates (LFO or a looped drawn envelope).
- Auto-wah that follows playing level (audio follower).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Type**: Phaser, Flanger or Filter.
- **Freq**: phaser/flanger/filter frequency, 37.6 Hz–16.17 kHz.
- **Feedback**: intensity of the phaser or flanger (those two modes only).
- **Bandwidth** / **Phaser Stages**: phaser notch width and number of notches (1–40).
- **Polarity**: flip notches to peaks (or back).
- **Mute Dry**: remove the dry signal — phaser becomes tremolo-like, flanger thinner.
- **Reso**: the filter's resonance (Filter mode) — the peak at the cutoff.
- **Filter Type** / **Filter Drive**: SVF HP/BP/LP 12, SVF Notch, Ladder LP 24, MFB LP 12/24, MFB HP 24, K35 LP 12 (MS-20 style). Careful: Ladder/MFB/K35 can self-oscillate loudly.
- **LFO Wave** / **LFO Rate** / **LFO Sync** / **LFO Synced Rate**: ten shapes, 0.05–50 Hz or 8 bars–1/64.
- **LFO Freq Mod** / **LFO Amp Mod**: LFO to frequency / to volume (tremolo). Bipolar.
- **ModType**: modulator is the drawn Envelope or the Audio Follower (one at a time).
- **Env Rate** / **Env Synced Rate** / **BeatSync** / **Env Loop** / **Trig On**: drawn envelope speed, sync, loop (= custom LFO), retrigger on audio.
- **Follow Attack** / **Follow Release** / **Follow Gain**: audio follower response.
- **Env Freq Mod** / **Env Amp Mod** / **Rate Mod**: modulator to frequency, to volume, to LFO speed.
- **Spread**: stereo detune for width.
- **Stereo Mode**: Stereo (mono in → stereo out) or Dual Mono.
- **DryWet** / **Volume** / **Enabled**.

## Where it shines / falls short
Shines: rich, controllable sweeps the old PH-90/CF-101 can't reach. Falls short:
per-bar pattern programming of several effects at once — Synchronous.

=====================================================
SOURCE FILE: synchronous.md
ORIGINAL LOCATION: HS:device_refs/synchronous.md
=====================================================

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

=====================================================
SOURCE FILE: the-echo.md
ORIGINAL LOCATION: HS:device_refs/the-echo.md
=====================================================

# The Echo

Stereo delay that colors every repeat — drive, a resonant filter, tape wobble —
plus two performance modes (Triggered, Roll) for one-off throws and stutters.
Source: Reason 12.7 Operation Manual, ch. 50, pp. 1147–1156.

## When you'd use it
- Dub/tape delays that get darker and dirtier each repeat.
- "Echo only this word / this 4th snare" throws (Triggered mode).
- Beat-repeat stutters and fills (Roll mode).
- Clean delay under a lead that stays out of the way while you play (Ducking).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Delay Time**: 1–1000 ms, or 1/128 note up to 1/2 note when Sync is on.
- **Sync**: locks Delay Time (and the right-channel offset) to song tempo.
- **Right Ch Time Offset**: delays the right side more than the left — instant stereo delay.
- **Keep Pitch**: stops the pitch bending when you move Delay Time live.
- **Ping-Pong Mode** / **Ping-Pong Pan**: repeats bounce L/R; Pan sets how wide and which side goes first.
- **Feedback**: number of repeats. 0 = one repeat, 100% = endless; past 100% it grows and distorts.
- **Right Ch Feedback Offset**: more/less feedback on the right only — the echo drifts sideways as it fades.
- **Diffuse On** / **Diffuse Amount** / **Diffuse Spread**: smears each repeat, reverb-like.
- **Drive Amount** / **Drive Type**: dirt added to EVERY repeat, so it builds. Types: LIM (squash), OVDR, DIST (denser), TUBE.
- **Filter On** / **Filter Frequency** / **Filter Resonance**: band-pass on the repeats; low = dark dub, high = thin telephone. Also stacks per repeat.
- **Envelope**: repeats bend down (left) or up (right). Centre = off.
- **Wobble**: random tape-speed wobble.
- **LFO Rate** / **LFO Amount**: separate pitch wobble per side — small = stereo width, big = warped.
- **Dry/Wet Balance**: mix. Use fully Wet on a send, and in Roll mode.
- **Ducking**: turns the echo down while the dry signal plays, back up in the gaps.
- **Input Mode**: Normal / Triggered / Roll.
- **Trig**: in Triggered mode, audio only enters the delay while held — like tapping a send.
- **Roll Enabled**: the Roll slider. Throw it fully right ON the beat to loop that beat; fully back to return. Don't park it halfway.
- **Enabled**: bypass/on/off.

## Back panel
- CV in: Trig (gate), Roll, Delay Time, Filter Freq.
- **Breakout jacks**: patch any effect INTO the feedback loop, so each repeat goes through it again (e.g. Scream 4 — keep Scream's master low, it gets loud fast).

## Tricks from the manual
- **Roll fill**: Sync on, 1/16, fully Wet, flick Roll on the beat.
- **Pitched metallic delay**: Delay Time 1 ms, Feedback 100%, Diffusion on and maxed; then play with Spread and Envelope.

## Where it shines / falls short
Shines: characterful, evolving echoes and live stutter moves. Falls short: long
ambient delays (tops out at 1 s / half note) and dead-clean digital delay — use
DDL-1 for that.

## Pairs well with
Scream 4 in the breakout loop, RV7000 after it for space, Combinator macro on Roll for a one-knob stutter.

=== END OF PART ===
