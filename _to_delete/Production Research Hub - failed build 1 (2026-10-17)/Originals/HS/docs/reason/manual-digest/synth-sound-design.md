# Synths and samplers: how to build sounds
Source: Reason 12.7 Operation Manual, ch. 30 Europa, 32 Mimic, 33 Thor, 34 Subtractor, 36 Monotone, 43 NN-XT (all six read in full). Tag: **Manual**.
Control lists are in `device_refs/` (subtractor, thor, europa, monotone, mimic, nn-xt) and are NOT repeated. This file = signal flow, routing ideas, recipes.
Anything not stated in the manual is marked **[Guess]**. Subtractor has no Remote names in device_refs, so its panel names are used.

## 0. Quick picks
| Want | Best tool | Why (manual) |
|---|---|---|
| Simple sub / 808 with pitch drop | Subtractor | Mod Envelope can drive Osc 1 / Osc 2 pitch |
| Fast fat mono bass, no fuss | Monotone | Sine sub osc + ladder filter + Drive; but NO pitch envelope |
| Wide pad / supersaw / evolving | Europa | Unison + Harmonics "Ensemble" (made for dense pads) |
| Anything weird, routed your way | Thor | 13 mod-matrix rows, step sequencer, 3 filters |
| Chop a loop or vocal | Mimic | Auto-slices on hits, slices land on keys from C1 |
| Drum kit from one-shots, velocity layers | NN-XT | Per-zone key/velocity ranges, 8 stereo outs, Group Mono |

Who has a pitch envelope? Subtractor: Mod Env, destination Osc 1 or Osc 2. Thor: Mod Env routed in the matrix to Osc pitch. Europa: any Envelope 1-4 to Mod Bus "Engine: Pitch". NN-XT: Mod Envelope, destination Pitch. Monotone: none (pitch only moves by LFO, bend, portamento).

## 1. Subtractor (ch. 34) - signal flow
- Osc 1 + Osc 2 (+ Noise, which rides on Osc 2's output) -> Filter 1 (LP24 / LP12 / BP12 / HP12 / Notch) -> Filter 2 (fixed 12 dB lowpass, in series) -> Amp.
- Osc 1 is the FM carrier and Osc 2 the modulator. Manual FM walk-through (bell/metal): Osc 1 sine, Osc 2 triangle, FM ~50, Osc Mix all left, Osc 2 Semi 7 (fifth); fourths/fifths/octaves ring clean, odd intervals clang. Ring mod = Osc 1 x Osc 2 (you hear it with Osc Mix turned to Osc 2).
- Phase knob + mode (x multiply, - subtract) gives pulse, PWM and sync-like tones from ordinary waves. Subtraction with Phase = 0 is silent.
- 3 envelopes: Amp, Filter (Filter 1 only), Mod (pick ONE destination: Osc 1, Osc 2, Osc Mix, FM, Phase, Freq 2).
- LFO 1: monophonic, destinations Osc 1&2, Osc 2, Filter Freq, FM, Phase, Osc Mix. LFO 2: one cycle PER NOTE, destinations Osc 1&2, Phase, Filter Freq 2, Amp (tremolo), has Delay and Kbd tracking.
- Mod wheel can scale: F. Freq, F. Res, LFO 1 amount, Phase, FM. Velocity can scale 9 things (Amp, FM, M. Env, Phase, Freq 2, F. Env, F. Dec, Osc Mix, A. Attack). Both accept negative values.
- Back panel CV in: pitch, phase, FM, filter 1/2, amp, mod wheel. CV out: Mod Env, Filter Env, LFO 1. CV connections are NOT saved in the patch.
- Waveform numbers worth knowing: 9 = electric bass, 10 = deep sub, 6 = piano, 7 = electric piano, 23-24 = marimba, 26 = harp/pluck, 29 = metallic bell, 30-32 = noise with FM and Osc Mix on Osc 1.

### Subtractor recipes
| Sound | Set this | Why |
|---|---|---|
| Sub bass | Osc 1 = sine (wave 4) or wave 10, Osc 2 off, Filter 1 LP24 wide open, Amp Envelope Attack 0, Sustain full, Release short | Sine has no harmonics, so the filter has nothing to do |
| 808 | Sub bass above + Mod Envelope dest = Osc 1, Attack 0, Sustain 0, short Decay, raise Mod Env amount; Amp Decay long, Sustain 0; Polyphony 1 | Pitch falls from high to the note in a few ms = the knock. Direction/amount: tune by ear **[Guess: the manual does not give a pitch-drop example or the amount's direction]** |
| 808 slide | Polyphony 1, play overlapping notes (Legato), Portamento time up | Legato = pitch changes, envelopes do not restart (manual) |
| Reese | Osc 1 + Osc 2 both saw, Osc 2 Cent a few up, LP24, low cutoff, LFO 2 -> Filter Freq 2 slowly | Manual: detuning "a few cents" makes oscillators beat = wider; LFO 2 cycles beat against each other |
| Pad | Osc 1 saw, Phase mode "-" ~mid, LFO 2 -> Phase, LFO 2 Kbd tracking on, Amp Attack/Release long, add Filter 2 | Manual's PWM string-pad tip ("Sweeping Strings" factory patch) |
| Pluck | Wave 26 (harp) or saw, Amp Sustain 0, Decay medium, Filter Envelope Amount up, Decay short | Fast filter close = pluck. Piano-style decay recipe is in the manual |
| Stab | Saw + square, LP24, Filter Env Amount high, Filter Decay short, Amp Sustain low | Filter snaps shut after the hit. Velocity F. Env up so harder = brighter |
| Lead | Polyphony 1, Legato, Portamento; LFO 2 -> Osc 1&2 with Delay up; Mod wheel -> LFO 1 amount | Delayed vibrato (manual suggests for violin/flute-like leads) |
| Arp-friendly | Amp Release short, Polyphony as needed; feed notes from RPG-8 / Matrix into Sequencer Control CV + Gate | Manual says mono sounds work best on those inputs |
| Snare / hat body | Osc 2 off, Noise on, Osc Mix to the right, Noise Decay short, Noise Color high (white) | Noise Decay is separate from Amp Decay: a burst at the start |

## 2. Thor (ch. 33) - signal flow
- 3 oscillator slots (Analog, Wavetable, Phase Mod, FM Pair, Multi, Noise) -> routing buttons 1/2/3 pick which go to Filter 1 and/or Filter 2 -> mixer (Osc 1+2 level, balance, Osc 3 level).
- NOTHING reaches a filter until a routing button is lit (manual tutorial, steps 3-7).
- Filters in series: arrow below the Shaper sends Filter 1 (through Shaper) into Filter 2. Parallel: both oscillator rows lit, Filter 2 to Amp. Lighting both rows AND serial = signal goes through Filter 2 twice.
- Filter 1 -> Shaper (9 modes) -> Amp -> Global section: Filter 3 (all voices summed), Chorus, Delay -> out.
- Per voice: Amp Env (cannot be bypassed - no gate, no sound), Filter Env (pre-wired to both filters via the filter Env knob), Mod Env (Delay + A/D/R, Loop, tempo sync, free), LFO 1 (one cycle per note).
- Global: Global Env (single-trigger, Delay/Hold/Loop), LFO 2 (not wired to anything until you route it).
- Sync: Osc 1 is always the master for Osc 2/3. Ring mod (AM): Osc 2 multiplies Osc 1.

### The mod matrix (the manual's own tutorial)
1. Pick Source (e.g. LFO 1), Dest (Osc 1 > Pitch), Amount (+/-100%).
2. Add Scale = Performance > Mod wheel, Scale Amount 100% = no effect with wheel down, full effect wheel up. That is the vibrato-on-wheel recipe.
3. Three bus types: 7 plain (Source>Dest>Scale), 4 two-destination, 2 with two Scales. CLR clears a row.
- Useful sources: Voice Key (Note = key tracking, Velocity, Gate), Mod/Filter/Amp Env, LFOs, Polyphony (short attack for single notes, long for chords), Step Sequencer (Gate/Note/Curve 1/Curve 2/Gate Length/Step Duration/Start/End Trig), CV 1-4, Audio 1-4.
- Pitch vs FM destination: "Pitch" changes pitch and timbre; "FM" only timbre (for audio-rate sources). Same split for filter Frequency vs Frequency (FM).
- Osc type swap keeps the routing: the modulation moves to the matching knob of the new type.

### Thor recipes
| Sound | Set this | Why |
|---|---|---|
| Sub bass | Osc 1 Type Analog, sine; Osc 2 Analog saw, quieter (Osc 1 And 2 Balance); both routed to Filter 1; Ladder LP 24 dB; Key Mode Mono Legato | Sine for weight, saw for bite; Ladder is the warm Moog-style filter |
| 808 | Osc 1 sine, Amp Env Attack 0 Sustain Off, Decay long; Mod 1: Source Mod Envelope > Dest Osc 1 Pitch, Mod Env Attack 0, Decay short | Mod Env is a free envelope, so it can drop the pitch. Amount sign/size: by ear **[Guess]** |
| Reese | Osc 1 Multi, saw, Detune Mode Linear or Interval, Osc 1 Mod up a little; Ladder LP; Mod 1: LFO 2 > Filter 1 Freq slow | Multi osc makes several detuned saws per voice; the manual says low Amount = "moving chorus" |
| Pad | Osc 1 Multi or Wavetable (X-Fade on), Mod Env or LFO 1 > Osc 1 Mod (= table position); Amp Attack and Release long; Chorus On; Filter Env Attack slow | Wavetable Position sweeps through up to 64 waves; Amp Env max Attack/Decay/Release times are long (Attack to 10.3 s, Decay/Release to 29.6 s) |
| Pluck | Analog saw, Filter 1 Env Amount high, Filter Env Decay short, Sustain 0, Amp Sustain 0 | Filter shuts after the hit |
| FM bell/e-piano | Osc 1 FM Pair, set carrier:modulator ratio, Osc 1 Mod = FM amount; Mod Env > Osc 1 Mod, short Decay | FM = 0 is a pure sine; envelope on FM amount = bright start that mellows (manual: "Mod" is FM amount) |
| Stab | Osc 1 saw + Osc 2 pulse (Osc 1 Mod 64 = square), Filter 1 Env Amount high, Filter 1 Velocity up, Shaper On (Soft Clip), Filter 1 Drive up | Manual tip: raise Filter 1 Drive for more grit into the Shaper |
| Lead | Key Mode Mono Legato, Portamento Mode Auto, LFO 1 Delay up -> Osc 1 Pitch, Scale = Mod wheel | Auto glides only on overlapping notes |
| Arp/riff | Note Triggering = Step Sequencer (or both), Step Sequencer Run Mode Repeat, Rate Synced; Mod row: MIDI Key > Note -> Step Sequencer Transpose | Manual: MIDI Note into Transpose lets you play the pattern in new keys live |

### Thor step sequencer (manual walk-through)
- 16 steps; each knob edits Note / Velocity / Gate Length / Step Duration / Curve 1 / Curve 2 (the Edit knob picks which). Dark step = rest, but its Step Duration still counts.
- Defaults: velocity 100, gate length 75%. Note range per step: 2 oct, 4 oct or Full.
- Steps knob sets length (fewer than 16 = odd loops, e.g. 5 or 7). Direction: Forward, Reverse, Pendulum 1 (end steps play twice), Pendulum 2, Random.
- Edit menu: Randomize Pattern (only the value shown in Edit) and Shift Pattern L/R.
- Curves 1/2 are free per-step values: use as a mod source = a 16-step modulation sequence.

## 3. Europa (ch. 30) - signal flow
- Per engine (x3): Oscillator -> Modifier 1 -> Modifier 2 -> Spectral Filter -> Harmonics -> Unison. Order is fixed; each stage can be switched off.
- Engines -> Mixer (level + pan each) -> shared Filter (routing LEDs choose which engines enter it; unrouted engines skip to the Amp) -> Amp Envelope -> 6 reorderable effects -> out.
- There is NO dedicated filter envelope. Make one: Filter section Frequency Modulation Source = an Envelope (1-4), then set its amount. Same for Spectral Filter and Shape.
- 4 free envelopes (draw shapes, Loop, Beat Sync, Key Trig, Global, unipolar/bipolar), 3 LFOs, 8 Mod Bus rows (Source > Dest 1 > Dest 2 > Scale; first four pre-filled).
- Drag the Waveform display: vertical = Shape, horizontal = Modifier 1 Amount. Record it while the sequencer runs to automate (manual tip). Draw two waves in Envelope 3 / 4 and crossfade them with Shape via the "Envelope 3-4" waveform.

### Europa recipes
| Sound | Set this | Why |
|---|---|---|
| Supersaw | Osc1 Wave Basic Analog, Osc1 Shape 100% (= saw), Osc1 Unison On, Count 7, Osc1 Spread up, Osc1 Detune moderate | Shape 100% on Basic Analog is a sawtooth (manual); Unison makes pairs of detuned copies around the pitch |
| Wide pad without detune mush | Unison Mode "Phase Only", modulate Detune from an LFO in the Mod Bus | Manual: Phase Only = wide stereo without lots of detuning, LFO on Detune = phasing |
| Dense pad | Osc1 Harm On, Harmonics = Ensemble, Amp Attack and Release long, Reverb On | Manual calls Ensemble "perfect for dense pad sounds" |
| Evolving pad | Wave Tables wave, Osc1 Shape modulated by a slow LFO (or Env 1); add a second engine detuned 7-12 cents | Shape crossfades 8 waves per table |
| Sub / 808 | Osc1 Wave Basic Analog, Shape 0% (= sine), Oct -1; Mod Bus: Source Envelope 1 > Engine: Pitch short Decay; Amp Sustain 0, Decay long; Key Mode Legato + Portamento for slides | Shape 0 = pure sine. Which engine receives "Engine: Pitch" and the amount: by ear **[Guess]** |
| Reese | Osc1 saw + Osc2 saw, Osc2 Detune a few cents, Osc3 sine Oct -1 (sub), shared Filter Ladder LP 24dB, Filter Mod slow LFO | Three engines mix independently; Ladder LP can self-oscillate (careful with Reso) |
| Pluck | Osc1 Wave Karplus-Strong, Shape = damping (higher = shorter), Amp Sustain 0, Decay medium | Physical string model. Add Harmonics "Stretch" for metal |
| Stab | Basic Analog saw, Unison On, shared Filter Freq mod = Envelope 1 (short decay), Amp Sustain low | Envelope as filter envelope |
| Lead | Key Mode Legato, Porta Auto, Mod Bus: LFO 1 > Engine: Pitch with Scale = Mod Wheel, Scale Amount 100; LFOs: Delay up | Same Scale rule as Thor: 100% = nothing until wheel moves |
| Vowel | Osc1 Vocal Cord, Spectral Filter Vocal Formant, move Freq/Reso | Manual: use these two together |
| Gated/arp feel | Envelope 1 preset stepped curve, Loop on, Beat Sync on, Edit Y-Pos to set each step's level, Mod Bus Env 1 > Amp Gain or Filter Freq | Manual: Edit Y-Pos turns a stepped envelope into a pseudo-sequencer |
- Per-engine "amp envelope": Env 1 > Mixer: Engine Level, set that engine's Level slider to 0 (manual's walk-through). The main Amp Envelope still affects every engine.
- Sample as oscillator: load a sample in User Wave, Wave = User Wave (or Smooth), Shape = play position, sweep it with an envelope. Stereo is turned to mono. A length that is an exact multiple of 2048 samples is read as one waveform cycle.
- Vocoder-ish (manual): User Wave = speech, Spectral Filter = User Wave, Freq 50%, Reso 0%, Kbd 0%, Envelope ramp -> Reso at 100%.

## 4. Monotone (ch. 36) - signal flow
- Osc 1 + Osc 2 + Noise -> Osc Mix -> Filter (24 dB ladder lowpass + Drive) -> Amp -> Chorus -> Delay (tempo-locked) -> out. One voice. Retrig button, Portamento On/Auto.
- The single extra envelope (called Filter Attack/Decay/Sustain/Release in device_refs) feeds Filter Env Amount AND FM Env Amt. LFO (Sine/Triangle/Square) feeds pitch of both oscillators and/or filter.
- Mod wheel only does two things: filter cutoff and LFO depth (the FILT and LFO knobs above the wheel). The LFO part does nothing unless the Osc LFO or Filter LFO Amt knob is already up.
- FM Env Amt: Osc 2 frequency-modulates Osc 1, shaped by that envelope. Short Decay = a metallic "tonk" at note start, good for the attack of a pluck bass.
- Delay Time snaps to 1/16, 1/8T, 1/8, 2/8T, 3/16, 1/4, 5/16, 4/8T, 7/16, 2/4. Chorus Spread 0 = mono (keep bass mono).

### Monotone recipes
| Sound | Set this | Why |
|---|---|---|
| Sub | Osc1 Wave Sine, Osc2 Wave Ramp, Osc2 Oct/Osc1 Oct set so sine sits 1-2 octaves below, Osc Mix to taste, Filter Freq mid, Amp Sustain full | Manual: sine "perfect as a sub bass an octave or two below another waveform" |
| Fat saw bass | Osc1 + Osc2 Ramp, Osc Detune ~10-20 cents (opposite directions), Filter Env Amount up, Filter Decay short, Chorus Amount low | Detune is applied in opposite directions to the two oscillators |
| Reese-ish | Both Ramp, Osc Detune up, Filter Freq low, Filter LFO Amt up with slow LFO Rate, Mod Wheel LFO knob up | Slow filter movement over detuned saws **[Guess: a recipe built from manual parts, not a manual example]** |
| 808-like | Sine/triangle, Amp Decay long, Sustain 0, Portamento Auto + Retrig Off for slides | Monotone has no pitch drop; use a short FM Env Amt "tick" and Drive to fake the knock **[Guess]** |
| Acid | Ramp, Filter Reso high, Filter Env Amount high, short Decay, Portamento Auto, Retrig Off | Reso emphasises the cutoff sweep; high Reso is LOUD (manual warning) |

## 5. Mimic (ch. 32) - sampling and chopping
- 8 slots, each with its own pitch, stretch, filter, 2 envelopes (filter, amp), LFO, compressor (Squeeze), lo-fi Effect, EQ (Lo Cut / Hi Cut), 2 sends. Modes: Pitch / Slice (one slot at a time), Multi Slot / Multi Pitch (up to 8 together).
- Slice mode: slices land on keys from C1 upward (10 slices = first 10 keys), max 92 (C1 to G8). More slices than fit = only the start of the sample is covered: move the Start marker or lower Slice Sens.
- Slices: auto at transients (yellow, Slice Sens); drag to move, double-click the lane to add, double-click a marker to delete. Moved/added markers stop obeying Slice Sens. Reset restores auto slices.
- Play Thru OFF = each slice stops at the next marker (tight chops). ON = slice keeps going while held. Loop is at the end of the slice.
- Global Pos ON = new notes join at the playhead (keeps layered chops in time). Reverse flips the slice.
- Stretch Mode: Tape (speed and pitch tied, Speed 0% = tape stop), Advanced (full mixes; heavy on CPU), Melody (mono lines, fewest loop clicks), Vocal (Voice Formant, Voice Fixed), Granular (Grain Len, Overlap, Jitter, Spread).
- Sampling INTO Mimic works in Reason stand-alone only. Patch holds a reference, not the audio.

### Mimic recipes
| Job | Set this | Why |
|---|---|---|
| Drum break chop | Play Mode Slice, load break, Slice Sens up until every hit has a marker, Play Thru off, Stretch Mode Advanced + Transients On (or Tape) | Each hit = one key; Advanced + Preserve Transients keeps drums punchy |
| Chop and pitch freely | Stretch Mode Tape, Pitch Semi down | Tape ties speed to pitch: slower and lower |
| One-shot drum kit on pads | Play Mode Multi Slot, one sample per slot, Slot Out 1-8 to separate Mix Channels | Keys C-G per octave fire slots 1-8, unpitched; connecting a Slot Out removes it from the master out |
| Vocal chops | Slice Mode on a vocal phrase, Stretch Mode Vocal, Voice Fixed ON | Fixed Pitch tunes slices to the key you press (manual: "pitch from the keyboard") |
| Tape stop | Stretch Tape, Speed Mod source = Envelope or mod wheel, Speed toward 0% | Manual: Speed all the way down is "stop" |
| Longer drum tail | Speed near min, Speed Mod = Filt Env, Stretch Advanced, raise Filter Decay | Manual walk-through: speed rises then slows, so the tail stretches |
| Velocity-layered hit | Pitch Mode, Snap Slices on, Start Mod source = Velocity, several takes of one hit in one file | Manual's "velocity layered instrument" walk-through; set Amp Release short so next slice does not play |
| Lo-fi grit | Effect Type Lowres or Bitrate, Effect Mix up; Lo Cut / Hi Cut; Squeeze | 7 effects: Noise, Reso Noise, Ring Mod, Bitrate, Lowres, Sine Fold, Scream |

## 6. NN-XT (ch. 43) - key maps
- Sample = audio; Zone = container with key range, velocity range, root, loop, Out, and all synth settings. Two zones can use the same sample with different settings.
- Front panel knobs are global offsets; the Remote Editor (zones) is where the sound design lives, and it can NOT be automated or Remoted.
- New samples land in zones spanning C1-C6. Pitched instruments: Select All > "Set Root Notes from Pitch Detection" > "Automap Zones" (splits halfway between roots).
- "Automap Zones Chromatically" = one key per zone from C2 upward in LIST order, ignoring root: a kit builder.
- Group parameters (per group): Key Poly (1-99, counts KEYS), Group Mono (new note cuts old, same note may repeat), Legato / Retrig, Portamento, LFO 1 Rate.
- Loading a REX file: one slice per key from C1. To replay it in order: load REX in NN-XT, load same REX in a Dr. Octo Rex, Copy Loop To Track, move that group to the NN-XT track, delete Dr. Octo Rex.
- Mod Envelope (Delay/Attack/Hold/Decay/Sustain/Release, Key To Decay) can drive Pitch or Filter. Velocity can drive Sample Start, Level, filter, Amp Attack.

### NN-XT recipes
| Job | Set this | Why |
|---|---|---|
| Drum kit from one-shots | Load all, Select All, Automap Zones Chromatically; per zone Play Mode FW; Out 1-8 for separate mixer channels | One key each; FW plays once. Outputs 2-8 must be cabled by hand on the back, only 1-2 is auto-routed |
| Hats that choke | Put closed + open hat in one group, Group Mono ON | Closed hat cuts open hat |
| Natural snare repeats | 2-3 snare takes on the SAME keys, Alt ON for all | Alt rotates between overlapping zones |
| Velocity layers | Zones on same keys: Lo Vel / Hi Vel ranges, then "Create Velocity Crossfades" (needs one partial range, not full overlap) | Soft hit / hard hit switch or blend |
| Add rimshot on hard hits | Snare zone full range, rim zone Lo Vel 80, Fade In 110 | Manual example |
| Harder = more attack | Raise zone Sample Start, Velocity > Sample Start negative | Manual: harder you play, more of the attack is heard |
| Chop a vocal or loop on keys | Option A: load a REX version, slices fill keys from C1. Option B: Duplicate Zones, set each copy's Sample Start / End, one key per zone | Option B is built from manual features **[Guess: not a manual walk-through]**. Mimic does this faster |
| Sampled 808, glide | Root Note = sample's pitch, Play Mode FW-LOOP or FW-SUS, Group: Key Poly 1 + Legato + Portamento | Legato needs Key Poly 1 |

