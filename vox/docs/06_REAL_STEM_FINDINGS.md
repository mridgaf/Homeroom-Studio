# Real-stem findings (delo mirror 18 13 26.wav)

First real material tested (synthetic test bench findings are in
`05_FINDINGS.md`; everything below is from an actual vocal take, 44.1 kHz
stereo, dual-mono, ~3:54, −17.9 LUFS raw, no clipping).

## User-reported: processed output sounded muffled
Isolation tests (drive each stage with a pure dry sustained tone that has
*zero* reverb and *is* clearly voice-like energy — a fair stand-in for a held
vowel) confirmed two real, serious bugs:

- **De-reverb** (`dsp/dereverb.py`): a dry sustained tone with NO reverb
  dropped **~20 dB**. Root cause: the algorithm models "late reverberant
  energy" as anything whose STFT-bin energy persists past a fixed number of
  frames (`direct_frames`). It cannot distinguish "this is a decaying reverb
  tail" from "this is a note being held" — both look identical to a
  frame-persistence detector. On real sung/spoken vocal with sustained
  vowels, this guts exactly the content that should survive.
  **Consequence: OFF by default now** (`chain_demo.run_full_pipeline`,
  `dereverb=False`). This needs a redesign, not a parameter tweak — see
  "What would actually fix this" below.
- **ML denoise** (DeepFilterNet3): the same dry tone dropped **~59 dB** at
  full wet. It's a speech/VoIP model; a pure sustained tone doesn't match
  its learned speech manifold, so it's suppressed as non-speech. On real
  singing (sustained vowels, vibrato, held notes) this is the same failure
  shape as de-reverb, for a different reason. **Consequence: OFF by default
  now** (`denoise_blend=0.0`).

Both stages were engaged (dereverb full-strength, denoise at 0.35 blend) on
the first real-stem test and stacked — confirmed via band-energy
measurement to cut 300 Hz–8 kHz by 2–7 dB compared to raw, which is what
read as "muffled." Re-rendered with both disabled, DSP-chain-only
(gate → de-ess → EQ → compressor → saturation → limiter): −3.5 to +4 dB
band deltas, no destructive cuts. That corrected file is what the user
confirmed sounded right.

### What would actually fix de-reverb (for whoever picks this up)
The frame-persistence model is the wrong tool. Options, roughly in order of
effort:
1. **Coherence/onset-gated suppression**: only start subtracting "late
   energy" after a detected onset, and re-arm on the next onset — so a note
   that's simply held past `direct_frames` isn't treated as decaying.
2. **Externally-supplied RT60**, measured once from actual room tone (silence
   between phrases, which this file has plenty of) rather than blind
   full-clip estimation — blind estimation was independently confirmed
   unreliable on both the synthetic bench (guessed 2.9 s vs true 0.45 s) and
   this real file (guessed ~3.0 s, clamped at the estimator's own ceiling).
3. A proper direct/reverberant split via a decay-rate-consistency check per
   bin (does this bin's energy trajectory actually match an exponential
   decay from the last onset, vs. staying roughly flat like sustained
   voicing) before subtracting anything.

### What would actually fix the denoiser
Not a bug to "fix" so much as a scope mismatch: DeepFilterNet3 is trained on
speech, not singing. Either (a) keep it strictly for the noise-floor-only
regions (gate it to engage only where a VAD says there's no vocal, e.g.
between phrases), or (b) find/train a model on sung material, or (c) accept
it as an optional, clearly-labeled "aggressive" mode the user engages
per-source and A/Bs themselves, not a default.

## pedalboard evaluation (user asked to check the "Homeroom" sound_engine code)
`reason_voice/` (voice control for the Reason DAW) is unrelated — no audio
DSP, not applicable here. `sound_engine/` + `tools/audio_engine.py` wrap
`pedalboard` (Spotify's JUCE-adjacent audio library) and are genuinely
relevant. Installed and measured it with the same rigor as our own modules:

- **`pedalboard.Limiter`: do not use.** Same true-peak test that caught our
  own limiter bug: swept 5 frequencies × 3 phases, worst-case overshoot
  **+4.1 dB** past its own ceiling (ours, after the fix, is 0 dB over the
  same sweep). It's a sample-peak limiter; it does not see inter-sample
  peaks at all. Their own `audio_engine.py` docstring already documents a
  different real issue with it (unwanted makeup gain under threshold) —
  good sign that whoever built it was verifying things too — but hadn't
  caught this one.
- **`pedalboard.Distortion`: do not use.** −19.4 dB alias floor, nowhere
  close to our −90 dB bar. Not oversampled.
- **`pedalboard.Reverb`: usable, with a catch.** Does NOT null cleanly at
  `wet=0, dry=1` (−6.6 dB against silence) — its "dry" path is not a
  transparent bypass. Fixed by never using its internal dry/wet: our
  `ReverbSend` module takes a 100%-wet tap and mixes it against our own
  untouched input externally. Verified null at our own `mix=0`: −400 dB.
- **`pedalboard.Chorus` / `pedalboard.Phaser`: usable directly.** Both null
  cleanly at their own internal `mix=0` (−156 dB, float32-precision-limited,
  not a real defect). Wrapped as `Dimension`.
- Note: the −90 dB aliasing bar does not meaningfully apply to modulation
  effects (chorus/phaser/reverb) — they're linear/time-varying, and
  deliberately spread energy around the fundamental via modulation (that's
  what chorus *is*). Measuring them with the harmonic-distortion aliasing
  test produces numbers that look alarming (chorus showed "+6.5 dB alias")
  but that's expected modulation sidebands, not digital aliasing. The bar
  stays enforced on `Saturation`, where it's the right test.

**Decision:** keep every hand-rolled, already-verified module (Gate,
DeEsser, ParametricEQ, Compressor, Saturation, Limiter) exactly as is — they
already passed adversarial-grade verification and pedalboard's equivalents
don't clearly beat them (the limiter is worse). Added `ReverbSend` and
`Dimension` (pedalboard-backed) to fill in the two modules we hadn't built
yet, both wired into the default chain but **mix=0 (inert) by default** —
available, verified, not forced on.

**Scope honesty**: pedalboard is Python-only and cannot ship inside the
eventual JUCE/C++ plugin. These two modules are a Phase-1 stand-in to prove
the product's reverb/modulation quality now; Phase 2 needs a native
reimplementation (most plausibly directly against `juce::dsp`, which is
plausibly what pedalboard itself wraps for these effects, though that
internal detail isn't independently confirmed here — verify before
assuming bit-for-bit equivalence).

---

## 2026-08-14 — de-reverb FIXED and re-verified on this same file

The frame-persistence bug above is fixed. `suppress_late_reverb` now gates
every bin's subtraction by whether that bin's energy is actually **decaying**:

    w = clip(measured_decay_slope / expected_reverb_slope, 0, 1)

Sustained content has slope ~0, so w ~0 and nothing is subtracted from it.
A genuine tail decays at (or faster than) the modeled reverb rate, so w -> 1
and the full Habets estimate is subtracted. The slope is measured on a
**smoothed log envelope** — the first attempt used a linear frame-to-frame
ratio, which measured 0.25..13.5 *inside a real decaying tail* (bin
magnitudes are stochastic; their arithmetic mean is meaningless). Log-domain
averaging is the part that makes this work at all.

### Measured on the same 20 s segment (2:56–3:16) of `delo mirror 18 13 26.wav`

| Band (Hz) | OLD (broken) | NEW (fixed) |
|---|---|---|
| 80–300 | −1.09 dB | **−0.33 dB** |
| 300–1000 | **−3.65 dB** | **−0.84 dB** |
| 1000–3000 | −2.61 dB | −0.49 dB |
| 3000–8000 | −2.11 dB | −0.34 dB |
| 8000–16000 | −2.01 dB | −0.38 dB |
| Overall RMS | −2.85 dB | −0.58 dB |

The OLD column reproduces the original "muffled" complaint exactly — it sits
inside the 2–7 dB, 300 Hz–8 kHz destructive cut documented above. The NEW
column is 3–6× smaller in every band. Mean decay weight on this file is
**0.464**, i.e. the gate is genuinely engaging, not passing everything
through untouched (there is a test asserting exactly that,
`test_decay_gate_separates_sustained_from_reverberant`).

### The honest trade — read this before re-enabling it by default
The old version scored a uniform ~18 dB tail-RMS drop on the synthetic bench
**because it floored every bin indiscriminately**, including the ones
carrying the vocal. The fixed version is selective, so tail suppression is
now condition-dependent: across a seed × RT60 sweep it ranged **3.9 to 18 dB**
(weakest at RT60 1.2 s, where 0.15 s of "tail" is still mid-decay). The
SNR-vs-dry-reference proxy, which is the metric that actually tracks quality,
improved consistently: **+1.0 to +2.9 dB in every one of the nine conditions.**

Less tail suppression, far less collateral damage. That is the right trade
and it should not be tuned back.

**Still not done:** this is a measurement, not a listening test. Nobody has
yet A/B'd the fixed version by ear on real material, and `chain_demo.py`
still defaults `dereverb=False`. Do not flip that default on these numbers
alone — that is precisely the mistake documented at the top of this file.
