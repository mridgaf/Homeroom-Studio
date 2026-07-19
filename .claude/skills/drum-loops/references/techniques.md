# Distilled Beat-Making Knowledge (cross-checked, July 2026)

Synthesis of three research passes — producer signatures, forum consensus,
and DSP implementation notes (raw reports sit beside this file). Everything
here was corroborated by at least two independent sources unless marked
[single-source] or [contested]. Use these numbers when programming beats;
resolve [contested] items by rendering both and letting the owner's ears
decide.

## Timing & swing (the strongest findings)

- MPC swing delays only EVEN-numbered 16ths. `delay = (swing/100 − 0.5) × 2 × T16`,
  rounded to 96-PPQ ticks (`round((swing/100 − 0.5) × 48)` ticks; tick = 60/(bpm×96) s).
  The integer rounding is part of the authentic feel — keep it.
- Calibration (Roger Linn + Frane 2017 + forum consensus, all agree):
  50% straight · **54% "loosens without sounding swung"** (measured median of
  30 classic breaks = 54.5%; Premier's effective zone 51–54) · 58% classic
  boom bap preset · 62% loose golden-era at ~90 BPM · 66.7% exact triplet ·
  75% max. Same % feels stronger at slower BPM (ms grows).
- **Trap is straight (50%)** — groove comes from hat subdivision + velocity,
  not swing. Swing muddies 808 slides.
- **Dilla feel is NOT the swing knob**: constant per-LANE offsets. Hats stay
  straight; snare displaced ~a 32nd (10–25 ms, up to 65 ms measured); kick
  displaced the OPPOSITE direction 10–15 ms. Direction is [contested]
  (book analysis: snare early = woozy; tutorials: snare late = lazy) — both
  are real Dilla moves on different records; A/B per beat.
- Human feel = fixed accent map + tiny wobble: velocity σ 3–8 MIDI units
  (~1 dB), timing jitter σ 3–12 ms, re-rolled per bar (identical repeated
  bars are the giveaway). Random ≠ human; structure dominates.

## Hats & rolls

- Velocity: accent on-beats, drop the "e"/"a" 16ths by 20–40; alternate
  strong/weak like two fingers. Ghost notes 30–50% of accent velocity,
  ≥15 velocity-points below mains.
- Rolls: bed of 16ths → bursts of 32nds → 64ths/64th-triplets right before
  the snare (64th triplets shine at 65–75 BPM half-time). Velocity ramps UP
  into the roll. Optional linear pitch-down through a roll (tape-stop feel).
- Pan a few individual hat hits slightly off-center for life.
- 1/24 (16th-triplet) stutter for one beat before the first snare: cheap
  interest trick.

## Kick / 808 low end

- Layer by frequency split: transient "top" (~1–4 kHz click) + sub body
  (<100 Hz); filter each to its band; phase-check (flip/nudge until low end
  gets LOUDER). Retune a layer ±1–2 semitones to fix cancellation.
- Real TR-808 kick fundamental: 48–56 Hz (≈G1) with pitch droop over decay.
- Tune 808s to the song key — uncontested. Monophonic (overlaps choke).
- Glide: 30–50 ms zip · 80–150 ms natural (100 default) · 200 ms+ dramatic.
  Glide selected notes only.
- Distortion chain: saturation (+4–6 dB in, unity out) → EQ (LP ~6 kHz,
  dip 300–500 Hz if muddy) → soft clip. Purpose = mid harmonics (200 Hz–1 kHz)
  so the 808 reads on phones.
- Mono below ~100–120 Hz (cut side channel, not hard mono) [contested up
  to 200]. Never Haas-delay kick/808 (10 ms ≈ ⅔ cycle at 60 Hz → mono-sum
  cancellation).
- Sidechain kick↔808: fast attack, ~3:1 — or skip entirely and trim the
  808 start [contested; per-personality choice].

## Snare / clap / reverb

- Stacks of 2–4 filtered layers (main + clap + rim + vinyl/brush). Layer
  micro-offsets −10…+15 ms fatten without flam [contested vs dead-aligned].
- Neptunes move: clap layered slightly LATE vs snare (flam ~10–30 ms), fast
  release compression, NO snare reverb, few/no hats.
- Plate = default snare verb; room for boom bap. Predelay 20–50 ms.
  High-pass all snare reverb 300–500 Hz. EQ the RETURN, not the source.
- Gated reverb: bright plate 1.8 s decay (2–4 s for drama), hold ~300 ms
  (scale to tempo; 80–150 ms tighter variant), release 5–70 ms (fast = the
  effect), predelay 0–10 ms. A flat/constant IR that stops dead gates
  harder than an exponential one.
- Alternation trick: dry snare on one backbeat, snare+clap+verb on the next.

## Machines (which personalities get which character)

- SP-1200: 12-bit @ 26.04 kHz, zero-order-hold everywhere (NO interpolation,
  NO reconstruction filter — the aliasing IS the brightness), SSM2044-ish
  4-pole LP ~9 kHz after. 45→33 trick: ZOH-resample up ×1.35 then back.
  Quantize at the LOW rate.
- MPC60: 12-bit/40 kHz. MPC3000: 16-bit/44.1 kHz, famously tight timing.
- ASR-10 (Timbaland/Neptunes): CLEAN 16-bit — their grit is arrangement,
  not bit-crush. Do not crush 2000s-era personalities.
- SP-303 (Madlib/late Dilla): lo-fi + compressor + "vinyl sim" character.

## Bus & loudness

- Drum bus: saturation BEFORE compressor; 2:1, attack 10–30 ms (let
  transients pass), release ~100 ms/auto, 1–2 dB GR average, 3 max. Soft
  clip for RMS. Parallel-crush a duplicate instead of pushing the main bus.
- Loudness target for finished beats: **−8 LUFS integrated** (working range
  −10…−7), true peak −1 dBTP (−0.1 when clipping intentionally). −14 LUFS
  reads weak next to commercial rap references.

## Texture & substitution

- Vinyl crackle bed under the whole loop = standard boom bap glue (Poisson
  clicks 5–30/s, amplitudes squared-uniform, band 300 Hz–8 kHz, plus LP'd
  noise floor ~−50 dB). Wow: 0.556 Hz = once-per-rev at 33⅓ RPM, depth
  0.1–1% (1% ≈ 17 cents); flutter 6–12 Hz via LP'd noise.
- Foley as hats (clock ticks, keys, lighter clicks), mouth percussion —
  Timbaland-documented and forum-loved.
- Reversed snare/cymbal resolving exactly ON the downbeat; reverse-reverb
  "felt more than heard".
- Haas widening: 8–20 ms hats/perc, 3–10 ms snare tops, delayed side
  −2…−6 dB. Check mono-sum RMS.

## Generative tools

- Euclidean: `[(i*k) % n < k]` gives E(k,n) (one rotation; rotations
  matter). E(3,8) tresillo · E(5,8) cinquillo · E(5,16) bossa · E(7,16)
  samba bell. Good for collab-beat percussion lanes.
- Ratchets: m ∈ {2,3,4} sub-hits across one step, velocity ramp, optional
  +cents per retrig. Per-step chance p (mains 1.0, ornaments 0.25–0.6),
  seeded per bar for reproducibility. Fills: extra snare 16ths in the last
  half-bar every 4th bar.

## Arrangement habits (era summaries)

- 90s: 2–4 bar loops, drop-outs under hooks/first verse bar, filtered-loop
  intros, horn stabs as tags.
- 2000s: silence as an instrument; two-bar patterns where bar 2 answers
  bar 1; 4×-loop intro tag; stop-start programming.
- 2010s: half-time (snare/clap on 3 at 130–150), riser/build before drops,
  whole-section drop-outs, producer tag up front.

## Transient shaping

- Renderer knows every onset — apply synthetic `1 + g·exp(−t/τ)` attack
  gain at each hit (cheaper and cleaner than envelope followers offline).
  τ ≈ 1–5 ms for click, g up to ~1.5 for hard styles, negative g to soften.
