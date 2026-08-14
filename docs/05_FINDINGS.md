# Measured findings so far (not opinions — every number below has a test behind it)

## Meter (vox/meter.py) — validated against published standards
- BS.1770-4 integrated loudness reproduces the EBU Tech 3341 conformance
  case (stereo 1 kHz sine at N dBFS → N LUFS) to within 0.01 dB, at
  44.1/48/96/192 kHz.
- K-weighting: +4.04 dB HF shelf, −6.0 dB at the 38 Hz RLB corner — matches
  the published response shape.
- True-peak (4x oversampled FIR per BS.1770-4 Annex 2) confirmed against a
  12 kHz tone at −6.02 dBFS: reads −5.87 dBTP, a 0.15 dB positive bias that
  is a documented, known limitation of 4x oversampling near Nyquist. This
  is why the limiter (below) uses 8x, not the meter's 4x.
- Null test resolves a single 24-bit LSB of difference at −138.5 dB, as
  expected from `20*log10(2^-23)`.

## Aliasing — the bar's −90 dBFS requirement is not automatically met
Measured with a non-commensurate test tone (see `meter.aliasing_floor_db`
docstring for why a naive integer-ratio test tone would hide aliasing):

| Saturation config              | Alias floor | vs. −90 dB bar |
|---------------------------------|------------:|:---------------|
| tanh, no oversampling            | −19.3 dB    | FAIL, badly     |
| tanh, 4× oversampled             | −81.6 dB    | **FAIL**        |
| tanh, 8× oversampled             | −117.4 dB   | PASS            |
| hard clip, 16× oversampled       | −69.6 dB    | **FAIL**        |
| hard clip, ADAA (1st-order), 8×  | −91.9 dB    | PASS            |

Conclusion baked into the product spec: soft nonlinearities need ≥8×
oversampling; hard-knee clippers cannot be fixed by oversampling alone and
require antiderivative anti-aliasing (ADAA).

## Limiter — two real bugs found and fixed during verification, not before
1. **Sample-peak detection instead of true-peak.** First working version
   measured 0.4–2.3 dB over its own ceiling on high-frequency material,
   because it looked at raw sample magnitude, missing inter-sample peaks.
2. **Rectify-before-interpolate.** The fix for (1) still overshot by up to
   2.3 dB at 12 kHz. Root cause: the detector took `abs()` of the signal
   *before* upsampling. Rectifying a sine creates a kink at every
   zero-crossing that was never in the original band-limited signal: the
   interpolator then faithfully reconstructs that fabricated high-frequency
   content and under-estimates the true peak. Fixed by interpolating the
   signed waveform per channel and rectifying only after filtering — the
   same order of operations `meter.true_peak_db` already used.

After both fixes: swept 12 frequencies (200 Hz–20.5 kHz) × 4 phases × a
12 kHz worst case → **0 dB worst-case overshoot**, and the limiter's own
detector matches the independently-implemented reference meter to within
0.003 dB (`test_limiter_detector_matches_reference_meter`).

## De-reverb (vox/dsp/dereverb.py) — real, but with an honest limitation
- Built from Habets (2007) / Lebart-Boucher-Denbigh (2001) causal statistical
  late-reverb suppression, after `nara_wpe` was tried and found to need
  multiple microphones (it did nothing on a single-channel stem: −77.5 →
  −77.8 dB tail energy).
- On the synthetic test bench: reverb-tail energy in the post-phrase silence
  drops from −75.1 dBFS to −93.7 dBFS (≈18.6 dB reduction).
- **Caveat found during this session's verification, not previously
  documented:** blind per-band RT60 estimation on a short (3.3 s) clip is
  unreliable — it estimated ~2.9 s against a ground-truth 0.45 s room.
  Despite the wrong estimate, tail suppression and vocal-region SDR were
  *not* worse than using the correct RT60 (in fact marginally better on this
  synthetic signal), which is itself a mild red flag that the vocal-region
  SDR metric isn't very sensitive here — more validation on a real stem is
  needed before trusting this module's default blind-estimation mode.
  Recommendation for the product: let a longer capture (or a dedicated
  room-tone snippet) drive the RT60 estimate rather than a short vocal take.

## Denoise (vox/engines/denoise_dfn.py) — real pretrained model, real caveats
- DeepFilterNet3 (MIT/Apache-2.0, pretrained weights, ~16 MB, CPU-capable).
- Measured on the synthetic test bench: −75.1 dBFS → −100.0 dBFS noise floor
  in the silent region, a ~25 dB reduction.
- Ships as an operator-controlled dry/wet blend (default 0.35), not forced
  full-strength, because it's a speech/VoIP-trained model and its behavior
  on sustained sung vowels and vibrato has not yet been validated against a
  real vocal performance.

## What still needs a real vocal stem
Every number above comes from the synthetic test bench (`vox/testsignal.py`)
because it has known ground truth. The synthetic voice is a source-filter
model, not a real larynx — it is good for proving DSP correctness and
catching bugs like the two above, but the denoise and de-reverb *quality*
numbers should be treated as provisional until validated on real material.
