# THE BAR — iZotope Nectar 4 Advanced (verified feature set)

Source: iZotope Nectar 4 help docs + Sound On Sound review. This is the pass/fail
gate. Any proposal that does not meet or beat this list is REJECTED by the
adversarial agents.

## Modules in the Nectar 4 mothership
1. **Auto-Level (ALM)** — Learn, Target level, Mix, Tame Noise, Listen, Range 1–12 dB,
   Strength, Side-chain Mode (Enable/Blend), Bypass. Adaptive gain-riding, not compression.
2. **Voices** — 11 style presets, Direction, Filter (hi/lo shelf), Pitch Correction
   (Speed/Amount), Time Variation, Pitch Variation, Solo, per-voice Enable/Gain(-20..0)/
   Pan(-100..+100)/Fine(±100 cents)/Delay(0–100 ms), MIDI mode, Wet/Dry.
3. **Backer** — 8 target personas, Blend, Tone (tilt EQ ±100), Formant (±12),
   Pitch transpose (±1 oct), Vocal Register, custom voice upload, Wet/Dry.
4. **Pitch** — Vocal Register (Low/Mid/High), Scale (Major/Minor/Custom), Auto Detect,
   Transpose ±12, Enable Correction, Speed 0–200 ms, Strength, Formant Shift,
   Formant Scale, Mix.
5. **Compressor ×2** — Modes: Digital/Vintage/Optical/Solid-State. Peak/RMS detection,
   Threshold, Ratio, Attack, Release, Makeup, Auto Gain, Wet/Dry.
6. **De-Esser** — Detection filter cutoff 800 Hz–8 kHz, Threshold, Listen, Wet/Dry.
7. **Delay** — 1–3500 ms, tempo sync, Feedback, stereo Link, Saturation modes
   (Digital/Tape/Analog/Grunge/Echo) + Amount, Modulate (Rate/Depth), post HP/LP, Wet/Dry.
8. **Dimension** — Chorus/Flanger/Phaser, Rate 0.01–4 Hz or synced, Depth, Width,
   Freq (phaser), Wet/Dry.
9. **EQ ×2** — up to 24 bands, 20 Hz–20 kHz, −30/+15 dB, Q/slope, Bell/LoShelf/HiShelf/
   HP/LP, 16 filter shapes, Dynamic Gain mode (boost/cut), Dynamic Frequency mode,
   Threshold, Wet/Dry.
10. **Gate** — Open Threshold, Close Threshold (hysteresis), Ratio, Attack, Release, Wet/Dry.
11. **Reverb**
12. **Saturation**
13. **Vocal Unmask** — dedicated tab, sidechains the vocal against the instrumental bus.

## Vocal Assistant (the "AI")
- Intent controls: Shape (Amount+Power), Intensity (Amount+Power), FX (X/Y pad + Power),
  Voices (Amount+Direction+Power), Width (Amount), Backer (Amount+Direction+Power).
- Config: Key and Range, Target Library, Relearn, Bypass.
- Behaviour: listens to ~10 s of vocal, builds a full chain, exposes it as editable modules.

## Global per-module controls
Bypass, Solo, Remove, drag-reorder, Wet/Dry mix. **Module order is user-rearrangeable.**

## What Nectar does NOT do well (attack surface — where we must win)
- Assistant targets are a fixed library; it does not adapt to the actual instrumental bed
  beyond Unmask's static curve.
- No true source separation / bleed removal on the input stem.
- No de-reverb.
- Latency is high in Advanced with all modules engaged.
- Pitch module is competent but not Melodyne-grade (they literally bundle Melodyne).
- Unmask requires a sidechain send — no automatic detection of what is masking what over time.

## NON-NEGOTIABLE ENGINEERING REQUIREMENTS
- All processing 64-bit float internal, 44.1–192 kHz sample-rate agnostic.
- Every module must null-test bypass to < −120 dBFS.
- No DC offset introduced (< −100 dBFS at 0 Hz).
- No aliasing above −90 dBFS on a 1 kHz sine at 0 dBFS through any nonlinearity
  (i.e. saturation MUST oversample).
- Look-ahead limiter true-peak accurate to ±0.1 dBTP against ITU-R BS.1770-4.
- Loudness measurement must be BS.1770-4 / EBU R128 compliant (I, S, M, LRA).
