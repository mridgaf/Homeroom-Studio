# Remaining Objekt differences

This is an independently implemented physical-modeling VST3. The original device's synthesis has not been measured or matched. A working control or passing test establishes functionality, not original-Objekt audio parity.

## Functionality still unsupported

- Impact frequency is now separate from hardness, and hardness responds independently to velocity. Diffuse shape/time remains unsupported; the exact impact pulse and velocity curves are unmeasured.
- Per-voice exciter parametric EQ.
- Object trigger position/random position, collision bounce, signal-driven pitch deformation and its filter, independently tunable dispersion filter.
- Coupling Off/On/X-Over selectors and crossover filter. Current continuous coupling distributes previous-sample outputs among all other active stages.
- Three-band feedback damping with low/mid/high/slope controls. Current damping is a one-pole feedback low-pass.
- Separate Object Pitch versus Tuning semantics: current tuning changes delay lengths; it does not transpose all pitch-related filters together.
- Section-specific release mute settings. A fixed release attenuation is used.
- Auto Legato, selectable Poly 1–15 counts, portamento Auto mode. Poly currently supports up to 16 voices; Mono and Legato use last-held-note priority.
- Analyzer/Fix tuner and section-selective randomization in the VST interface.
- Original CV/Gate ports and patch-file compatibility. Original factory patches, templates, artwork, and algorithms are not supplied.

## Implemented with narrower behavior or approximations

- External mono/stereo host input is accepted, but stereo channels are summed before exciting the resonators. Mono/Legato can create an external-input voice without MIDI; this does not reproduce the original's complete input/key-mode behavior.
- Noise modes are independent approximations of the published mode names. ADSR uses exponential decay/release; impact is a short mixed noise/sine excitation. Diffuser and exact curves remain absent.
- Modal filters and nonlinear pickup are independent DSP models; symmetry uses a DC-compensated asymmetric tanh model.
- Object feedback delays use linear fractional interpolation. Dispersion changes the spacing of stage frequencies, not a measured original dispersion network. Nonlinearity is a saturating feedback function, not the original collision model.
- Stage factor/gain/polarity, active/tracked counts, tuning, routing mix and stereo pans are functional, but their original parameter tapers and frequency compensation are unmeasured.
- Two LFOs, a 16-step/interpolated curve, two macros and eight dual-destination matrix buses work. Destination selection is a subset of the original: pitch, impact, hardness, noise, three resonator levels/decays, damping, dispersion, collision, coupling and width. Pitch/decay/dispersion coefficients update every 32 samples; other listed modulation destinations update per sample. Original LFO waveforms, reset modes and curve timing are not fully matched.
- Pitch bend, sustain, Mono/Legato, note priority and portamento are functional independent implementations. Unreleased nonsustaining voices stop after 14 seconds; sustained noise and Mono/Legato external-input voices are exempt.
- Five reorderable effects implement documented categories with independently designed algorithms. Original distortion/reverb sounds, compressor curves and parameter tapers remain unmeasured. The previous simple reverb remains ahead of the new effects for old-preset compatibility; its control is separate from the new send reverb.
- Generic JUCE parameter editor remains; original panel organization, visualization and section workflows are not reproduced.

## Evidence and validation limits

Engine tests cover finite bounded output, 16-voice allocation, external excitation, stage disabling, Mono/Legato allocation, and audible effect of each coefficient-rate modulation destination. These checks do not establish perceptual similarity. Exact tuning, dynamics, timing, stereo behavior, patch compatibility and sound require controlled comparisons with a licensed reference device. No original-reference audio measurement was available for this pass.
