# Chapter 09: Reason 12 manual digest and studio workflow
## Part 16 of 25

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Reference.md (piece 7 of 10) — Reason 12.7 Operation Manual — Compiled Reference

(Next: Part 17 of 25)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Reference.md (piece 7 of 10)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Reference.md
=====================================================

## 42. Humana Vocal Ensemble


Set Pitch Bend range for the wheel via up/down buttons or by dragging the display; range control sits to the right of the Mod wheel. The wheel bends note pitch and responds to incoming MIDI pitch bend.

If S.Start (Sample Start) in the Instruments section is at 0 ms, it cannot move back further; at 150 ms, it cannot move forward further.

If Cutoff in the Filter section is at 20 Hz, it cannot be lowered further; at 25 kHz, it cannot be raised further.

The standard ADSR envelope controls filter cutoff frequency modulation over time (see Amp Envelope for characteristics).

The Delay effect is routed as a send effect, with Amount as an effect-return control - a short note at Amount zero can still trigger delay if Amount is raised afterward, depending on Feedback.

The Reverb effect works the same way - a short note at Amount zero can still trigger reverb if Amount is raised afterward, depending on the Time setting.

(Humana shares its Instruments/Filter/Envelope/Delay/Reverb architecture with Pangea and Klang - all three are sample-playback "world/tuned percussion/vocal" instruments built on the same panel design.)

---

<a id="nn-xt-sampler-43"></a>
## 43. NN-XT Sampler


NN-XT's basic functions resemble its companion NN-19: load samples and build multi-sample patches by mapping samples across the keyboard, then shape the sound with a comprehensive set of synth-type parameters. Key differences: NN-XT can load presets and samples from SoundFont banks (see "Loading SoundFonts"), and can route different samples to different mixer channels for individual effect processing (see "Out").

Sampling procedure is generic across NN-19, NN-XT, Redrum and Kong (see the "Sampling" chapter).

SoundFont presets load via the patch browser; single SoundFont samples load via the sample browser.

REX files (loops from ReCycle or bounced audio clips) are primarily used in Dr. Octo Rex but also work in NN-XT; extensions: .rx2, .rcy, .rex.

Main panel controls globally modify parameters for all samples in a patch by the same amount. Aftertouch, expression pedal, or breath controller input (if your MIDI keyboard sends it) can modulate NN-XT parameters, assigned in the remote editor panel (see "The Modulation controls"); movements record as automation like any other performance controller.

Two knobs control filter parameters (filter must be on to have effect); one changes filter resonance (character/quality).

Three knobs control the Amplitude Envelope: one changes Decay (time to return to sustain level after full value is reached while the key is still held).

A separate knob controls Decay of the Modulation Envelope.

Clicking the (unlabeled) zone-group area selects all zones belonging to a group (see "Working with Grouping").

The keyboard-range guide is also used for setting root keys and auditioning loaded samples (see "About the Root Key" and "Auditioning samples").

Per-group parameters mostly relate to performance/playing style.

MIDI-based sample selection is velocity sensitive - zones with velocity ranges only trigger if the key is played within that range (see "Setting velocity range for a Zone").

Synth parameters occupy most of the remote editor panel; changes always apply to all selected zones. Selecting multiple zones and adjusting a parameter sets all of them; when selected zones have conflicting values, NN-XT shows a small "M" (multiple) symbol next to the parameter.

Copying settings between zones only copies synth parameters, not sample parameters (root key, velocity range, etc.).

After loading samples, the next step is usually adjusting key range, root note, and tuning so they play sensibly across the keyboard (see "Working with Key Ranges").

A slice is a snippet of sound within a REX file; browsing to a REX file and opening it like a folder reveals its slices as individual files, importable and treated like samples throughout the manual.

Clicking a sample plays it at root pitch, unprocessed (no synth parameters applied). Clicking a key on the keyboard guide plays the sample at that key's pitch with all processing applied, simulating velocity 100 - this can trigger multiple samples depending on overlapping key/velocity ranges.

Soloing a sample helps check how far from its root key it can be played before sounding "unnatural," useful when setting up key ranges.

Zone sorting only works within a group - zones from different groups can't be sorted relative to each other.

NN-XT has eight separate stereo output pairs; each zone can be assigned to one, so an 8-zone key map can have eight independent stereo outputs routed to separate mixer channels.

Unlike samplers where polyphony sets total simultaneous voices, NN-XT's polyphony setting determines the number of keys that can sound, regardless of how many voices each key triggers. (Activating a related mono button is not equivalent to setting polyphony to 1 - it can't be used for Legato or mono Retrig.)

Modulation/external control wheel knobs set how much they modulate a given parameter, e.g., Decay of the Modulation Envelope. The LFO 1 "scaling" knob determines how much the Modulation Wheel/External Controller affects the amounts already set by the three LFO 1 destination knobs (Pitch, Filter, Level) - e.g., to use the Mod Wheel to increase vibrato depth versus to decrease it, set the scaling knob's polarity accordingly.

Velocity can control Modulation Envelope Decay, Amplitude Envelope Attack, and Sample Start offset (so harder/softer playing shifts where the sample starts).

Amplitude Envelope Release works like Decay but determines the time to fall to zero after key release.

The Pitch section's envelope-to-pitch knob raises pitch when turned right, lowers when turned left, and has no effect at center. The equivalent Filter cutoff knob works the same way for cutoff frequency.

Most Amplitude Envelope parameters mirror the Modulation Envelope's (see "The Modulation Envelope").

NN-XT has two LFOs (LFO 1 and LFO 2); unlike normal oscillators, low-frequency oscillators generate a waveform/frequency for modulation, not audible sound. In one Rate mode, an LFO runs at the rate set for its group in the group section rather than its own Rate knob, so all zones in that group share the exact same modulation rate.

NN-XT has 16 audio output jacks (8 stereo pairs) on the back panel; the first pair auto-routes to the first available mixer channel when a new NN-XT device is created.

---

<a id="nn-19-sampler-44"></a>
## 44. NN-19 Sampler


The NN-19 is a sampler capable of recording and reproducing - but not editing - sound files.

Samplers are often used for more than playing "real instrument" samples: different sounds per key zone, complete verse/chorus vocals plus variations across "one note" key zones, or chord samples that play rhythmic figures at tempo to build song structures. In these uses, keys trigger samples rather than corresponding to pitch.

REX files (loops from ReCycle or bounced audio clips) can be loaded into NN-19 as complete patches or as individual sliced samples.

A new NN-19 device loads with a default patch; select "Reset Device" from the context/Edit menu to start from scratch. NN-19 needs a loaded patch, sample, or self-sampled sound (via "Sampling") to produce sound.

REX files are primarily used in Dr. Octo Rex but work in NN-19 too; extensions: .rx2, .rcy, .rex.

Sampling procedure is generic across NN-19, NN-XT, Redrum and Kong (see the "Sampling" chapter).

SoundFont samples are stored hierarchically (User Samples, Instruments, Presets, etc.); NN-19 can browse/load single SoundFont samples but not entire SoundFonts.

Loading a new sample into a zone that already had one replaces it in that zone and in sample memory - unless the old sample is also used by another zone, in which case it's kept. To remove a sample from a zone without removing it from memory, select "No Sample" with the Sample knob, or replace it with another.

A per-map tuning parameter can correct samples that are slightly out of tune with each other, by +/- half a semitone each; if all samples share the same tuning offset relative to the song, it's simpler to use the Sample Pitch controls in the Osc section directly instead.

Looping requires loop points set up in the audio file itself - NN-19 can't set loop points directly; that's done in the Edit Sample window or an external sample editor.

In a sample patch, the samples themselves are the "oscillators" - the main sound source, configured in the Osc section.

A pitch-by-envelope parameter sets how much the Filter Envelope affects overall sample pitch, with positive/negative values raising or lowering it.

Legato works best with monophonic sounds - set Polyphony to 1 to use it.

---

<a id="midi-out-device-45"></a>
## 45. MIDI Out Device


To play and/or record MIDI from your MIDI instrument into Reason, connect the instrument's MIDI Out to your computer's MIDI In as well (see "Recording MIDI Controller automation from the controlled MIDI instrument").

MIDI latency mainly occurs in the MIDI interface and connected MIDI instruments and is not something Reason can automatically compensate for (see "Moving clips" for related info).

---

<a id="quartet-chorus-ensemble-46"></a>
## 46. Quartet Chorus Ensemble


Loading/saving patches works like any other internal Reason device.

Mod Depth sets how much the LFO modulates delay time; at 0, delay time is static (unless Noise Mod is in use).

If both Mod Depth and Noise Mod are 0, the Width control has no effect.

Noise Mod amplitude-modulates the signal with lowpass-filtered noise, creating a "sparkling" effect; if both Noise Mod and Mod Depth are 0, Width has no effect.

An FFT-based noise-depth parameter controls a combination of noise amplitude and bandwidth applied to the signal's partials, with the result also depending on the Frequency Range parameter.

Random Phase randomly alters grain phase for a "bubbly" phase-cancellation effect, especially noticeable when Jitter is set low.

---

<a id="sweeper-modulation-effect-47"></a>
## 47. Sweeper Modulation Effect


Loading/saving patches works like any other internal Reason device.

One knob controls LFO modulation depth to the Frequency control of the Phaser, Flanger, and Filter sections. Another controls Modulator (Envelope Modulator / Audio Follower Modulator) depth to the same Frequency controls.

A separate knob controls LFO modulation depth to a built-in amplifier - bipolar, so negative values invert the modulation. Another controls Modulator depth to that same amplifier.

The LFO provides cyclic modulation of Phaser/Flanger/Filter Frequency and/or Volume; its Rate can sync to sequencer tempo and can itself be modulated by the Modulator.

Modulating LFO Rate while in SYNC mode forces the LFO to switch between sync divisions.

Envelope/loop playback starts as soon as audio is present in Sweeper, or can be triggered via Audio Trig or a rear-panel CV trig signal (Trig Envelope); Audio Trig and Trig Envelope can coexist.

---

<a id="alligator-triple-filtered-gate-48"></a>
## 48. Alligator Triple Filtered Gate


Like all effect devices, Alligator has a Bypass/On/Off switch and an input level meter (see "Common effect device features").

Select which of 64 built-in patterns plays back to control the gates (see "The built-in patterns" for a guide).

For a general introduction to filter types, see "The Filter Section" in the Subtractor chapter.

---

<a id="pulveriser-49"></a>
## 49. Pulveriser


Features and procedures common to all effect devices (Bypass/On/Off switch, etc.) are covered in "Common effect device features".

Filter options: a 24 dB/octave lowpass similar to Subtractor's LP24; a bandpass similar to Subtractor's BP12; a 12 dB/octave highpass similar to Subtractor's HP12; and a comb filter similar to Malström's "Comb +".

The LFO Rate range is very wide, reaching up into the audio frequency range; it can sync to sequencer tempo (Sync button), in which case the Rate knob sets sync resolution instead. Rate can also be modulated from the envelope follower in the Follower section.

---

<a id="the-echo-50"></a>
## 50. The Echo


Features common to all effect devices (Bypass On/Off, etc.) are covered in "Common effect device features". The Echo's Input Meter differs from the standard 7-segment LED meter elsewhere in Reason - it's a 3-segment meter (green/yellow/red, red = clipping).

Standard mode: input signal feeds continuously into the device (typical send/insert behavior).

Roll mode: the unprocessed (dry) signal passes through unaffected until you raise the Roll slider, which gradually suppresses Dry while raising Feedback and mixing delay/echo output into the Wet signal - useful for repeat, stutter, and glitch effects. Recommended: set Dry/Wet to (or near) Wet for Roll mode (see "Using the Roll function" for an example).

Setting Delay to Sync mode keeps repeats in sync with the loop, e.g. at 1/16th notes or another chosen resolution.

---

<a id="scream-4-sound-destruction-unit-51"></a>
## 51. Scream 4 Sound Destruction Unit


Common effect device features (Input meter, Bypass/On/Off switch, Signal Flow Graphs) are covered in "Common effect device features".

You don't have to route a whole drum kit through Scream - route individual outputs (bass drum, snare, toms) to a Spider Audio Merger, connect its merged output to Scream 4, then route that to a separate mixer channel, leaving hi-hats/cymbals unprocessed.

The Spider CV Merger and Splitter can invert and split the Auto CV output for extra flexibility.

---

<a id="bv512-vocoder-52"></a>
## 52. BV512 Vocoder


Typical vocoder setup (assumes a connected MIDI keyboard): the carrier needs high frequencies/harmonics - on Subtractor, a sawtooth-based sound with the filter fairly open works well as a simple, effective carrier (see "Choosing a carrier sound").

See "Recording audio from Mix Channel outputs" for recording Mix Channel output.

The individual band level connectors (CV) enable creative routing: cross-patch frequency bands so low frequencies in the modulator control high vocoder bands, extract CV signals to control synth parameters elsewhere, or base vocoding on CV from other devices instead of an audio modulator signal.

The Hold button "freezes" the current filter spectrum until deactivated - useful for sample & hold-like effects, stuttering, or garbled vocoder sounds.

The individual band level jacks on the back: the upper row outputs envelope-follower CV per frequency band; the lower jacks are CV inputs for controlling individual bandpass filters (this breaks the internal envelope-follower connection when patched).

---

<a id="rv7000-mk-ii-advanced-reverb-53"></a>
## 53. RV7000 Mk II Advanced Reverb


You typically don't want to hear the dry sound when using the Reverse effect (see "The Gate section").

Common effect device features (Input meter, Bypass/On/Off switch, Signal Flow Graphs) are in "Common effect device features".

In the Convolution algorithm, input signals are first summed to mono (except in Parallel Stereo Mode) then processed with the impulse response sample.

Changing some Convolution parameters recalculates the impulse response in real time, so modulating them can give unexpected results - CV modulation of RV7000 Mk II in Convolution mode is not recommended.

When combining the Gate function with Convolution, set Decay Mod to 0.

Stereo effects in the Stereo Mode alternatives require stereo samples/sampling in stereo (see the "Sampling" chapter).

---

<a id="neptune-pitch-adjuster-and-voice-synth-54"></a>
## 54. Neptune Pitch Adjuster and Voice Synth


Pitch correction controls include scale, correction speed, and a display showing Input Pitch, Target Note, and Catch Zone (see "Using pitch correction").

Pitch shifting parameters are covered in "Using pitch shifting (Transpose)".

Additional parameters define audio input characteristics (Input signal type), MIDI control (MIDI Input), and output level (Output Mixer section).

Catch Zones display as red horizontal boxes above each selected key on the virtual keyboard; a box turns green when the detected Input Pitch falls within its zone (see "Setting Catch Zone Size").

Wide Vibrato makes pitch detection ignore vibrato in the input audio (fixing wobbling notes/unwanted swoops caused by heavy vibrato); the vibrato can still be retained in the output by raising Preserve Expression.

A MIDI-enable option lets pitch correction be controlled via MIDI (see "Using manual pitch correction").

Four Scale Memory slots store Root Key, Scale, and Catch Zone settings for automation - similar to how Redrum stores which 16th-note buttons are active in a pattern. Automating Scale Memory slot selection from the Neptune sequencer track lets you switch pitch-correction characteristics through a song; settings save with the Song.

Preserve Expression controls how much input vibrato passes through at fast Correction Speed settings.

Receiving a MIDI note temporarily overrides Root Key/Scale/Catch Zone settings (Correction Speed and Preserve Expression stay active).

A Formant Shift setting can make pitch-adjusted vocals sound like the same person singing at the new pitch.

MIDI Input can route Note/Pitch Bend/Mod Wheel data either to the Pitch Adjust section (manual pitch-correction control) or to the Voice Synth (harmony-voice generation) - the routing choice determines which section responds.

Root Key and Scale are set via spin controls, or a custom scale by selecting individual notes on the keyboard display (see "Setting Root Key and Scale").

Edits to Root/Scale/Catch Zone auto-save into the selected Scale Memory slot and with the Song.

Catch Zone Size sets the input-pitch range corrected to specific notes.

Correction Speed sets how quickly pitch snaps to the target scale.

The Output Mixer slider sets total output volume for Pitch Adjust, Transpose and Formant sections to the L/R outputs.

CV inputs: Note (controls pitch of whichever of Pitch Adjust/Voice Synth is selected in MIDI Input, e.g. from a Matrix or RPG-8's Note CV out), Gate, Bend (pitch bend CV), and a Mod Wheel CV input (controls vibrato amount).

Left/Right outputs carry Pitch Adjust, Transpose and Formant audio; if Voice Synth Sep Output isn't connected, Voice Synth audio also routes to these main outputs.

Adjust Scale to fit the song key; override specific passages manually via MIDI when needed (see "Using automation for temporary pitch correction" and "Bouncing Mixer Channels").

---

<a id="softube-amps-55"></a>
## 55. Softube Amps


To use a Softube Amp as an insert effect while recording an audio track, you must monitor through Reason (see "Monitoring") - otherwise you won't hear the amp sound while recording.

Low latency matters here (see "Buffer Size settings"); good audio hardware/drivers can usually get down to a few milliseconds - comparable to standing a meter from a real guitar amp.

The front panel has a display area (Patch/Amp/Cabinet selectors) on top and standard amplifier tone controls below (see "Amp panel controls").

Common effect device features (Input meter, Bypass/On/Off, Signal Flow Graphs) are covered in "Common effect device features".

Loading/saving patches works like any other Reason device (see "Sounds, Patches and the Browser").

Any Amp model can be paired with any Cabinet + microphone model (see "About the Amp and Cabinet models").

---

<a id="audiomatic-retro-transformer-56"></a>
## 56. Audiomatic Retro Transformer


Designed mainly as an insert effect on individual tracks or the Master Inserts section; also works well as an insert on Parallel Channels in the Reason Mixer, letting you further sculpt the effect sound with the channel EQ and Compressor (see "Parallel Channels").

Use the Volume knob together with Gain to compensate for high input Gain settings.

A bipolar CV signal patched to the Transform CV input modulates the Transform parameter (positive increases it, negative decreases it).

A bipolar CV signal patched to the Dry/Wet CV input modulates the Dry/Wet control (zero modulation = current knob setting stays valid).

Effect type options include Tape, VHS, MP3, Wash, and PVC-style degradation.

---

<a id="channel-dynamics-compressor--gate-57"></a>
## 57. Channel Dynamics Compressor & Gate


## Introduction
This is the rack version of the Dynamics section in Reason's Main Mixer, mainly intended for the VST3 plugin version of Reason (which lacks the Main Mixer) but usable anywhere. It matches the channel strip version's specs plus adds Input Gain and Dry/Wet Mix controls.

## Global controls
Input Gain: +/-18.00 dB, affects the input signal regardless of whether Compressor/Gate are on.
Mix: blends dry and processed signal; <100% enables parallel processing (dry and effect output together).

## The Compressor section
Compressors reduce dynamic range, evening out loud/quiet differences for easier balancing, added punch and sustain. This compressor/limiter has soft-knee characteristics, switchable to peak limiting (instant reduction above threshold), plus automatic make-up gain.
On: activates the Compressor section.
Peak: switches detection from RMS to Peak (instant attack time) - suited to fast-attack sounds like drums.
Fast: fixed 3 ms reaction time for 20 dB gain reduction above Threshold.
Ratio: 1:1 (no reduction) to Infinite:1.
Threshold: -52 dB to 0 dB; signals below are unaffected, automatic make-up gain compensates based on Ratio and Threshold.
Release: 100 ms to 1000 ms; short = pumping effect, long = smoother.
Compressor Gain Reduction Meter: LED meter showing applied gain reduction.

## The Gate/Expander section
Gating/expansion attenuates signals below a threshold (opposite of compression) - useful for removing background noise or mic bleed (e.g., silencing tom mics between hits) and for "keying" effects. Ratios of 10:1+ are noise gating (fully silences below threshold).
On: activates the section.
Exp: switches Gate mode to Expander mode - less severe, more gradual gain reduction around Threshold (scaled rather than a fixed dB cut); Expander lets some signal through at lower volume rather than muting, effectively an "inverted compressor" that expands dynamic range. Range knob then sets expansion amount.
Hold: 0-4000 ms, time the gate stays fully open after signal falls below Threshold; Release only starts acting after Hold elapses.
Fast: lowers attack time from the normal 1.5 ms/40 dB to 100 microseconds/40 dB - useful for steep, percussive waveforms.
Range: 0 dB (no reduction) to -40 dB gain reduction below Threshold (controls expansion amount if Exp is on).
Threshold: -52 dB to 0 dB; closing threshold is slightly lower than opening threshold to avoid chattering near the set level.
Release: 100 ms to 1000 ms; fast = abrupt fade, long = slow fade-out.
Gate Gain Reduction Meter: LED meter for gating/expansion reduction.

## External Sidechain
Connect an external signal to the rear Sidechain Inputs to key the Compressor and/or Gate/Expander from it instead of the channel signal; a "Connected" LED lights when a cable is present. Example: trigger a synth-pad channel's gate from a drum loop for rhythmic chord effects.

## Connections
CV Outputs: Compressor Gain Reduction, and Gate Gain (high when gate is open, low when closed) - both usable to modulate other CV-capable devices.
Sidechain Input Left & Right: external sidechain signal input.
Input Left & Right: audio to process (mono signals connect only to L).
Output Left & Right: processed audio outputs.

---

<a id="channel-eq-equalizer-58"></a>
## 58. Channel EQ Equalizer


The "Q" parameter adjusts the bandwidth around the set center LMF (Low-Mid Frequency) Frequency - the higher the Q, the narrower the affected frequency range (except in "E" mode).

---

<a id="master-bus-compressor-59"></a>
## 59. Master Bus Compressor


## Introduction
This is the rack version of the Master Bus Compressor in Reason's Main Mixer, mainly for the VST3 plugin version (no Main Mixer there) but usable anywhere. It adds punch, cohesion, and general "glue" to a mix or bus - straightforward operation with make-up gain and program-adaptive Release. Matches the Master Section version's specs plus Input Gain and Dry/Wet Mix.


=== END OF PART ===
