# Chapter 07: Reason device guides
## Part 4 of 6

_Plain-language guide for each Reason device (compressors, EQs, reverbs, delays, synths, drums...)._

**In this part:**
- mixer-14-2.md — Mixer 14:2 and Line Mixer 6:2
- monotone.md — Monotone
- neptune.md — Neptune (Pitch Adjuster and Voice Synth)
- nn-19.md — NN-19 Sampler
- nn-xt.md — NN-XT Sampler
- pangea.md — Pangea World Instruments
- peq-2.md — PEQ-2 Two Band Parametric EQ
- ph-90.md — PH-90 Phaser
- pulsar.md — Pulsar Dual LFO
- pulveriser.md — Pulveriser
- quartet.md — Quartet Chorus Ensemble
- radical-piano.md — Radical Piano

(Next: Part 5 of 6)


=====================================================
SOURCE FILE: mixer-14-2.md
ORIGINAL LOCATION: HS:device_refs/mixer-14-2.md
=====================================================

# Mixer 14:2 and Line Mixer 6:2

Small rack mixers. Mostly used INSIDE a Combinator (to combine sounds before
the main mixer) — the main SSL-style mixer does the real mixing.
Source: Reason 12.7 Operation Manual, ch. 67 (pp. 1373–1380) and ch. 68 (pp. 1381–1384).

## Key controls (Mixer 14:2)
Named exactly as Reason's Remote layer names them (channel 1 shown; 1–14 exist).

- **Channel 1 Level** / **Channel 1 Pan** / **Channel 1 Mute** / **Channel 1 Solo**.
- **Channel 1 EQ On/Off** / **Channel 1 Bass Amount** / **Channel 1 Treble Amount**: simple two-band EQ.
- **Channel 1 Aux 1 Send** … **Channel 1 Aux 4 Send**, **Channel 1 Aux 4 Pre Fader On/Off**: four sends (Aux 4 can be pre-fader).
- **Aux 1 Return Level** … **Aux 4 Return Level**: effect returns.
- **Master Level**.

## Line Mixer 6:2
Six channels, one send. **Channel 1 Level** / **Channel 1 Pan** / **Channel 1 Mute** / **Channel 1 Solo** / **Channel 1 Aux Send**, **Aux Pre/Post**, **Aux Return Level**, **Master Level**.
Best for summing several devices inside a Combi when its 8 inputs run out.

=====================================================
SOURCE FILE: monotone.md
ORIGINAL LOCATION: HS:device_refs/monotone.md
=====================================================

# Monotone

Small mono bass synth: two oscillators + noise, a 24 dB ladder filter with drive,
amp envelope, a mod envelope, LFO, chorus and tempo delay.
Source: Reason 12.7 Operation Manual, ch. 36, pp. 909–922.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Osc1 Wave** / **Osc1 Oct**, **Osc2 Wave** / **Osc2 Oct** / **Osc2 Pitch**: ramp (saw), square (pulse on Osc 2), triangle, sine. Sine an octave down = sub.
- **Osc Mix** / **Osc Detune** / **Noise**: balance, fatness, white noise.
- **FM Env Amt**: envelope-driven FM from Osc 2 into Osc 1 (metallic/bell).
- **Filter Freq** / **Filter Reso** / **Filter Drive**: 24 dB ladder lowpass; high Res self-oscillates (loud).
- **Filter Env Amount** / **Filter Key Amt** / **Filter LFO Amt**: what moves the cutoff.
- **Filter Attack** / **Filter Decay** / **Filter Sustain** / **Filter Release**: the mod envelope (for filter and FM).
- **Amp Attack** / **Amp Decay** / **Amp Sustain** / **Amp Release**: volume envelope.
- **LFO Rate** / **LFO Wave** / **Pitch LFO Amt**: sine/triangle/square LFO; vibrato.
- **Chorus Amount** / **Chorus Rate** / **Chorus Spread**, **Delay Amount** / **Delay Time** / **Delay Feedback** / **Delay Pingpong**: effects (delay is tempo-locked).
- **Portamento** / **Portamento Mode** / **ReTrig**: glide On/Auto; ReTrig off = legato notes don't restart envelopes.
- **Volume**, **Mod Wheel** (filter + LFO depth), **Pitch Bend**.

## Where it shines / falls short
Shines: fat mono bass in seconds. Falls short: one voice only — no chords or pads.

=====================================================
SOURCE FILE: neptune.md
ORIGINAL LOCATION: HS:device_refs/neptune.md
=====================================================

# Neptune (Pitch Adjuster and Voice Synth)

Vocal pitch corrector (natural to hard "robot"), pitch shifter (±1 octave), formant
control, and a Voice Synth that turns one sung line into MIDI-played harmonies.
Monophonic input only.
Source: Reason 12.7 Operation Manual, ch. 54, pp. 1197–1220.

## When you'd use it
- Tuning a vocal to a key (insert on the vocal track).
- The hard auto-tune effect: Correction Speed max, Preserve Expression min.
- Octave-up or -down dub on a send (Transpose ±12 + Formant).
- Harmony stacks played from the keyboard (Voice Synth).
- Pitching drums or other non-pitched audio (Transpose only, Pitch Adjust off).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Pitch Adjust On/Off**: the corrector.
- **Correction Speed**: turn UP for faster correction (stepped robot); turn DOWN for slower (invisible); the middle sounds natural.
- **Preserve Expression**: how much of the singer's own vibrato survives fast correction.
- **Catch Zone**: how far off (±20–600 cents, default ±100) a note can be and still get pulled to the scale. Outside it passes untouched.
- **Scale Memory**: 4 memories of Root/Scale/Catch Zone — automate to change key mid-song. (Root and Scale themselves: Chromatic, Major, Natural/Harmonic Minor, Dorian, Mixolydian, or click your own notes.)
- **Pitch Adjust Amount**: correction amount.
- **Transpose On/Off** / **Semitones** / **Cent**: fixed pitch shift, ±1 octave.
- **Formant On/Off** / **Formant Shift**: keeps the voice natural after big shifts; Shift alone = "gender" change without pitch change.
- **Low Freq Input**: better tracking for deep voices (more latency).
- **Wide Vibrato**: ignore heavy vibrato when detecting pitch.
- **Live Mode**: lowest latency for singing through it live (slightly lower quality).
- **MIDI Destination**: MIDI notes go "To Pitch Adjust" (force the sung note to the key you hold) or "To Voice Synth" (harmonies).
- **Pitched Signal Level** / **Voice Synth Level**: output mix of the corrected voice and the harmonies.
- **Pitch Bend** / **Pitch Bend Range** / **Mod Wheel** / **Vibrato Rate**: bend and add vibrato to the corrected voice.
- **Enabled**: bypass/on/off.

## Notes
- MIDI control needs its own sequencer track: right-click > Create Track for Neptune.
- Voice Synth ignores the Pitch Adjust/Transpose/Formant settings and has its own outputs on the back.
- The sequencer's Pitch Edit mode can also correct audio graphically.

## Where it shines / falls short
Shines: fast in-rack tuning, the classic hard-tune sound, instant harmonies.
Falls short: chords, polyphonic or noisy material — it only tracks one note at a time.

=====================================================
SOURCE FILE: nn-19.md
ORIGINAL LOCATION: HS:device_refs/nn-19.md
=====================================================

# NN-19 Sampler

Reason's original, simpler sampler: key zones across the keyboard, one filter,
envelopes, LFO. Loads samples, REX loops (one slice per key from C1) and single
SoundFont samples. Can't set loop points itself — those come from the file or
Reason's sample editor.
Source: Reason 12.7 Operation Manual, ch. 44, pp. 1057–1078.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Sample Start** / **Sample Start Vel Amount**: start further into the sample (trim a click or a word); velocity can push it.
- **Osc Octave** / **Osc Semitone** / **Osc Fine Tune** / **Osc Kbd Track** / **Osc Env Amount**: pitch; Kbd off = same pitch on every key.
- **Filter On/Off** / **Filter Mode** / **Filter Freq** / **Filter Res** / **Filter Kbd Track**: Subtractor-style multimode filter.
- **Filter Env Attack** / **Filter Env Decay** / **Filter Env Sustain** / **Filter Env Release** / **Filter Env Amount** / **Filter Env Invert** / **Filter Env Vel Amount**.
- **Amp Env Attack** / **Amp Env Decay** / **Amp Env Sustain** / **Amp Env Release** / **Amp Vel Amount** / **Amp Attack Vel Amount**.
- **LFO Wave** / **LFO Rate** / **LFO Sync Enable** / **LFO Dest** / **LFO Amount**: LFO to pitch, filter or pan.
- **Key Mode** (Legato/Retrig), **Polyphony**, **Portamento**.
- **Spread Mode** / **Stereo Spread**: pan voices by key or alternately.
- **Low Bandwidth On/Off**: cuts highs to save CPU (lo-fi side effect).
- **High Quality Interpolation**: cleaner re-pitching.
- **Solo Sample**: hear only the selected zone's sample across the keyboard.
- **Master Level**, **Mod Wheel**, **Pitch Bend** / **Pitch Bend Range**.

## Where it shines / falls short
Shines: dead-simple "put one sample on the keys" with a synth filter. Falls
short: no velocity layers or per-zone envelopes — NN-XT, or Mimic for chops.

=====================================================
SOURCE FILE: nn-xt.md
ORIGINAL LOCATION: HS:device_refs/nn-xt.md
=====================================================

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

=====================================================
SOURCE FILE: pangea.md
ORIGINAL LOCATION: HS:device_refs/pangea.md
=====================================================

# Pangea World Instruments

Multisampled odd and world instruments: Acoustic Saz, Angklung, Bizarre Sitar,
Harp Guitar, Kinderklavier (toy piano), Lakeside Pipe Organ, Little Wooden
Flutes, Little Pump Reeds, Struck Grand Piano, Traveler Organ, Zitherette.
Same layout as Klang.
Source: Reason 12.7 Operation Manual, ch. 41, pp. 971–986.

## Key controls
Named exactly as Reason's Remote layer names them. (Note the underscores —
Pangea spells some differently from Klang.)

- **Instrument**, **Octave** / **Semitune** / **Finetune**, **SampleStart**.
- **Filter_On** / **Filter_Type** / **Filter_Cutoff** / **Filter_Reso** / **Filter_Env** / **Filter_Velocity** / **Filter_KeyFollow**: LP, HP, BP or Comb.
- **Filter_Attack** / **Filter_Decay** / **Filter_Sustain** / **Filter_Release**.
- **Amp_Attack** / **Amp_Decay** / **Amp_Sustain** / **Amp_Release**.
- **Delay_On** / **Delay_Time** / **Delay_Sync** / **Synced_Delay_Time** / **Delay_Feedback** / **Delay_Damp** / **Delay_PingPong** / **Delay_Amount**.
- **Reverb_On** / **Reverb_Time** / **Reverb_PreDelay** / **Reverb_LowDamp** / **Reverb_HighDamp** / **Reverb_Amount**.
- **ModWheel_to_Amp_Level**, **Master_Volume**, **Mod Wheel**, **Pitch Bend**.

## Where it shines / falls short
Shines: sample-flip-style melodic colour (sitar, saz, toy piano, organs). Falls short: fixed set of eleven sounds.

=====================================================
SOURCE FILE: peq-2.md
ORIGINAL LOCATION: HS:device_refs/peq-2.md
=====================================================

# PEQ-2 Two Band Parametric EQ

Two fully parametric bell bands, A and B.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Filter A Freq** / **Filter A Gain** / **Filter A Q**: band A — 31 Hz–16 kHz, ±18 dB, higher Q = narrower. Always on.
- **Filter B On/Off**: band B must be switched on.
- **Filter B Freq** / **Filter B Gain** / **Filter B Q**: band B, same ranges.
- **Enabled**: bypass/on/off.

Back panel: CV in for band A and band B frequency — LFO on Freq with a narrow boost = wah-like sweep.

## Where it shines / falls short
Shines: one or two surgical moves, sweepable by CV. Falls short: no shelves or filters — use Channel EQ or MClass Equalizer.

=====================================================
SOURCE FILE: ph-90.md
ORIGINAL LOCATION: HS:device_refs/ph-90.md
=====================================================

# PH-90 Phaser

Four-stage phaser: four notches sweep through the sound.
Source: Reason 12.7 Operation Manual, ch. 62 (Half-Rack Effects), pp. 1281–1304.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Frequency**: position of the notches (what the LFO sweeps).
- **Split**: spacing between the notches — changes the character.
- **Width**: notch width. Wider = deeper, more hollow.
- **Rate**: sweep speed.
- **LFO Sync Enable**: lock sweep to tempo.
- **Frequency Modulation**: sweep depth. 0 = static formant/vowel colour.
- **Feedback**: resonance. Max it for "singing" phasing.
- **Enabled**: bypass/on/off.

Back panel: CV in for Freq (envelope-driven phasing) and Rate. Mono in + stereo out gives the moving stereo effect.

## Where it shines / falls short
Shines: Rhodes, pads, guitars, slow sweeps on loops. Falls short: subtlety at high Feedback.

=====================================================
SOURCE FILE: pulsar.md
ORIGINAL LOCATION: HS:device_refs/pulsar.md
=====================================================

# Pulsar Dual LFO

Two LFOs plus an attack/release envelope, as a rack utility. Its CV outputs
modulate any other device's CV inputs. Rates reach audio range; can sync to tempo
and be "played" from the keyboard.
Source: Reason 12.7 Operation Manual, ch. 64, pp. 1333–1342.

## When you'd use it
- Tempo-synced wobble, tremolo, filter pumping on devices that lack their own LFO.
- Complex modulation: LFO 2 speeding up/scaling LFO 1.
- Gated/pumping effects triggered by notes or its own envelope.

## Key controls
Named exactly as Reason's Remote layer names them.

- **LFO1 Waveform** / **LFO2 Waveform**: nine shapes incl. random, slope, stepped.
- **LFO1 Rate Free** / **LFO1 Rate Synced** / **LFO1 Tempo Sync**: speed (free Hz or note values).
- **LFO1 Level**: output amount.
- **LFO1 Phase**: start point in the cycle (0–360°).
- **LFO1 Shuffle**: swings pairs of cycles (stays in time when synced).
- **LFO1 Lag**: smooths sharp shapes.
- **LFO1 Env Sync**: envelope trigger restarts LFO 1.
- **LFO2 Enabled** + the same LFO2 set (**LFO2 Rate Free**, **LFO2 Rate Synced**, **LFO2 Tempo Sync**, **LFO2 Level**, **LFO2 Phase**, **LFO2 Shuffle**, **LFO2 Lag**).
- **LFO2 to LFO1 Rate** / **LFO2 to LFO1 Level**: LFO 2 FM/AM-modulates LFO 1.
- **Sync LFO1 to LFO2**: each LFO 2 cycle restarts LFO 1.
- **Attack** / **Release** / **Trig**: the AR envelope; Trig is a hold-to-open gate. Also fired by MIDI notes, the rear gate input, or LFO 2.
- **LFO2 Triggers Envelope**: every LFO 2 cycle fires the envelope.
- **LFO1 Env Rate** / **LFO1 Env Level** / **LFO2 Env Rate** / **LFO2 Env Level**: envelope moves each LFO's speed/level (bipolar).
- **Keyboard Track**: MIDI notes change LFO speed (100 = chromatic, centred on C3). Needs its own track.

## Where it shines / falls short
Shines: adds movement to anything with a CV input. Falls short: CV cables are not
saved in device patches — save the setup inside a Combinator.

=====================================================
SOURCE FILE: pulveriser.md
ORIGINAL LOCATION: HS:device_refs/pulveriser.md
=====================================================

# Pulveriser

Compressor + distortion + filter in one box, with an LFO ("Tremor") and an
envelope follower to move things, and a Blend knob for parallel processing.
Subtle glue to total demolition.
Source: Reason 12.7 Operation Manual, ch. 49, pp. 1137–1146.

## When you'd use it
- Parallel smash on a drum loop (Squash + Dirt, Blend around halfway).
- Warm fattening on bass, keys, a whole beat.
- Tempo-synced filter wobble or tremolo; auto-wah that follows playing level.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Squash**: compression — one knob sets ratio, threshold and make-up together.
- **Release**: compressor release. Short + lots of Squash = pumping.
- **Dirt**: distortion amount.
- **Tone**: low-pass on the distortion; fully right = open.
- **Filter Mode**: Bypass, Lowpass 24, LP12+Notch (animated), Band Pass, High Pass, Comb.
- **Filter Frequency** / **Peak**: cutoff and resonance.
- **Routing**: Squash > Dirt > Filter, or Filter > Squash > Dirt (filter first decides what gets crushed).
- **Tremor Rate** / **Sync** / **Tremor Waveform**: the LFO — nine shapes incl. random/stepped; can run into audio rates.
- **Tremor Spread**: left and right LFOs opposite — rotary-speaker feel.
- **Tremor Lag**: smooths sharp LFO shapes.
- **Tremor to Frequency** / **Tremor to Volume**: LFO depth to the filter and to the wet level (tremolo). Centre = none, left = inverted.
- **Follower Threshold** / **Follower Attack** / **Follower Release** / **Follower Trig**: envelope follower — reacts to input loudness; Trig fires it by hand.
- **Follower to Frequency** / **Follower to Rate**: louder input opens the filter (auto-wah) / speeds up the LFO.
- **Blend**: dry/wet. In between = parallel processing. Tremolo never touches the dry part.
- **Volume**: total output.
- **Enabled**: bypass/on/off.

## Back panel
CV in: Squash, Dirt, Filter Freq, Tremor Rate, Volume, Follower. Audio-rate in:
Filter Freq (filter FM) and Volume (AM). CV out: Follower and Tremor — use it
to move other devices from this one's rhythm.

## Tricks from the manual
- **Beef up**: LP24, Frequency low, Follower all minimum, raise Follower to Frequency until lows come through, then Blend/Squash/Dirt to taste.
- **Trembling pads**: Comb filter, low Peak, Tremor to Frequency past centre, Follower to Rate up, Tremor to Volume up.

## Where it shines / falls short
Shines: fast character and movement, parallel crush in one device. Falls short:
precise compression — no threshold/attack; MClass Compressor for control.

## Pairs well with
Drum bus, 808s (Dirt + Tone low), Scream 4 when you want more distortion types.

=====================================================
SOURCE FILE: quartet.md
ORIGINAL LOCATION: HS:device_refs/quartet.md
=====================================================

# Quartet Chorus Ensemble

Four chorus/ensemble algorithms in one box, each remembering its own settings.
Source: Reason 12.7 Operation Manual, ch. 46, pp. 1093–1102.

## When you'd use it
- Thickening keys, pads, guitars; vintage string-machine shimmer (BBD).
- Very dense modern ensemble on pads (FFT, Grain).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Effect Select**: Chorus, BBD, FFT or Grain.
- **Stereo Mode**: Stereo (sums L+R — mono in gives stereo out) or Dual Mono.
- **Chorus Delay** / **Chorus Depth** / **Chorus Rate** / **Chorus Feedback** / **Chorus Width** / **Chorus DryWet**: classic chorus — delay 1–30 ms, rate 0.1–5 Hz; Feedback near 100% = flanger tone, ~50% = gentle.
- **BBD Delay** / **BBD Depth** / **BBD Rate** / **BBD Noise** / **BBD Width** / **BBD DryWet**: three vintage bucket-brigade choruses at once — richer; Noise adds sparkle.
- **FFT Size** / **FFT Depth** / **FFT Start** / **FFT End** / **FFT Width** / **FFT DryWet**: noise-modulates the partials; Start/End pick which frequency range moves (leave lows still to keep the bass solid). Size 1 keeps transients, 4 is most accurate.
- **Grain Size** / **Grain Density** / **Grain Depth** / **Grain Jitter** / **Grain Phase** / **Grain Width** / **Grain DryWet**: grain-based ensemble; small Size = stutter, high Density = fat.
- **Enabled**: bypass/on/off.

Chorus needs some dry signal, so 100% Wet still contains some dry. Back panel: CV in for Mod Depth, Width, Dry/Wet.

## Where it shines / falls short
Shines: lush, dense width beyond CF-101 or UN-16. Falls short: on bass or kick (smears the low end).

=====================================================
SOURCE FILE: radical-piano.md
ORIGINAL LOCATION: HS:device_refs/radical-piano.md
=====================================================

# Radical Piano

Sampled + physically modelled acoustic piano: Bechstein home grand, Steinway D
("Deluxe Grand") and an upright, each recorded with five mic setups you can blend.
Seamless velocity, sympathetic string resonance, half-pedal sustain.
Source: Reason 12.7 Operation Manual, ch. 39, pp. 943–954.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Microphone 1 Type** / **Microphone 2 Type** / **Microphone and Instrument Blend**: pick two sound sets (Vintage Mono, Ambience, Floor, Jazz, Close) — even from different pianos — and blend them.
- **Character**: Subdued (warm) ↔ Agitated (bright). Briefly mutes when changed.
- **Vel Response Low** / **Vel Response High** / **Vel Response Curve**: tone at softest/hardest hit and the feel. Natural: Low ~9 o'clock, High ~12. Same tone always: Low max, High 0.
- **Tune** / **Tune Drift**: tuning; Drift = slow wandering pitch (melancholic, lo-fi).
- **Symp Res Level** / **Symp Res Release Time**: sympathetic resonance of undamped strings.
- **Env Attack** (0–200 ms) / **Env Decay Curve** (short body ↔ long sustain) / **Env Release** (damper speed).
- **Key Down Level** / **Key Up Level** / **Pedal Level**: mechanical noises; 12 o'clock = natural.
- **EQ On/Off** / **EQ Lo Gain** / **EQ Mid Gain** / **EQ Hi Gain**: piano-tuned 3-band EQ, ±18 dB.
- **Ambience Type** / **Ambience Level**: Small Room, Large Room, Hall, Theater.
- **Compression Amount** / **Stereo Width** (no effect on Vintage Mono only) / **Master Volume**.

Sustain pedal is continuous (edit half-pedal values in the note clip). Pitch bend
fixed ±7 semitones. Audio In on the back runs any sound through its resonance,
EQ, room and compressor ("singing into a piano").

## Where it shines / falls short
Shines: real, playable, small-footprint piano; Vintage Mono + Drift = instant
lo-fi keys. Falls short: nothing but piano.

=== END OF PART ===
