# DSP & Algorithmic-Composition Research for Pure-Numpy Drum Renderer

All techniques offline-friendly, numpy-only (no scipy). Timing math assumes `T16 = 60/(bpm*4)` seconds per 16th.

## 1. MPC swing math + Dilla per-track shifts

**MPC swing** (Roger Linn's definition): delay every EVEN-numbered 16th (the 2nd 16th inside each 8th). Swing % = share of the 8th-note pair given to the first 16th. 50% = straight, 66% ≈ triplet, 75% = max (second 16th lands halfway to the next one).

```
delay_sec = (swing/100 - 0.5) * 2 * T16          # continuous form
# MPC60/SP-1200 ran 96 PPQ (24 ticks per 16th, 48 per 8th) and rounded to ticks:
delay_ticks = round((swing/100 - 0.5) * 48)
# 54% -> 2 ticks, 58% -> 4, 62% -> 6, 66% -> 8, 75% -> 12
# tick_sec = 60 / (bpm * 96); at 90 BPM: 54%=13.9ms, 58%=27.8ms, 62%=41.7ms
```
Implement: when scheduling a hit at grid step `i`, if `i % 2 == 1` (odd index = even-numbered 16th), add `delay_sec` to its start sample. The integer-tick rounding is part of the authentic MPC feel — keep it optional.

**Dilla-style per-track shift**: instead of one global swing, give each *instrument lane* its own constant offset and its own swing amount. Documented characteristics (Charnas's *Dilla Time*, Ethan Hein's analysis, "21st Century Funk" microtiming paper):
- Kick rushed (early), snare dragged (late) — or vice versa — as *constant* lane offsets, not random jitter.
- Typical magnitudes: 10–60 ms lane offsets at ~85–95 BPM; one analyzed snare sat ~65 ms off the metric grid; bass/synth anticipating the drums by ~a 32nd note (~80–100 ms at 90 BPM).
- Mixed feels layered: hats straight (swing 50%) while snare/kick lanes are swung or shifted — the clash IS the effect.

```
lane_offset = {"kick": -0.015, "snare": +0.025, "hat": 0.0}   # seconds, constant per lane
hit_time = grid_time + swing_delay(lane_swing[lane], step) + lane_offset[lane]
```
Sources: melodiefabriek.com/sound-tech/mpc-swing-reason/ ; attackmagazine.com Roger Linn interview on MPC swing; ethanhein.com/wp/2022/dilla-time/ ; academia.edu "21st Century Funk: A Microtiming Analysis of the Beats of J Dilla".

## 2. Published microtiming research (target numbers)

- **Frane 2017, "Swing Rhythm in Classic Drum Breaks From Hip-Hop's Breakbeat Canon"** (*Music Perception* 34(3):291): measured 30 canon breakbeats. 16th-note swing common but subtle — **median swing ratio 1.2:1** (≈ 54.5% MPC swing). Swing magnitude uncorrelated with tempo. Practical default: swing 53–56% for "real break" feel, not 62–66%.
- **Dilla analyses** (above): deviations up to ~65 ms; systematic per-lane, not Gaussian noise.
- General finding across groove literature: human deviations are *consistent tendencies* (same hit lands the same few ms off every bar) plus small jitter (~±4–12 ms). Model as `constant_lane_offset + per_hit_gaussian(sigma≈3-6ms)`.

Sources: shamslab.psych.ucla.edu Frane_SwingInBreakbeats_2017.pdf ; academia.edu Dilla microtiming paper; drummerworld.com microtiming article.

## 3. SP-1200 emulation

Hardware facts (Wikipedia E-mu SP-1200; Rossum reissue docs; Gearspace filter thread):
- **12-bit linear** sampling at **26.04 kHz**; ~10 s total sample RAM.
- **No reconstruction filter on output** → imaging above Nyquist = the signature "bright grit".
- Analog **SSM2044 4-pole (24 dB/oct) lowpass** per output channel; on the SP it's mostly a fixed anti-grunge/tone filter, often described as a gentle darkening ~7–10 kHz.
- **Drop-sample (zero-order-hold) pitch shifting** — no interpolation → aliasing artifacts on any repitch.
- **45→33 trick**: sample vinyl at 45 RPM, pitch back down 45/33.3 ≈ ×1.35 — saves memory; the pitch-down via sample-dropping smears/aliases the top end. Emulate by resampling UP by r=1.35 then back DOWN by 1/r with zero-order-hold both ways.

Numpy fake, in order:
```
def sp1200(x, sr=44100, r=1.35):
    x = zoh_resample(x, sr, 26040)          # decimate: idx = floor(arange(N26)/26040*sr)
    x = np.round(x * 2047) / 2047           # 12-bit quantize (signed, x in [-1,1])
    x = zoh_resample(zoh_resample(x, 26040, 26040/r), 26040/r, 26040)  # 45/33 smear (optional)
    x = zoh_resample(x, 26040, sr)          # back up WITHOUT lowpass -> keep images
    return onepole_lp_cascade(x, fc=9000, poles=4)   # SSM2044 stand-in
# zoh_resample(x, sr_in, sr_out): y = x[np.minimum((np.arange(n_out)*sr_in/sr_out).astype(int), len(x)-1)]
# onepole: a = exp(-2*pi*fc/sr); y[n] = (1-a)*x[n] + a*y[n-1]  (apply 4x; use lfilter-free loop or
# frequency-domain: X = rfft(x); X *= (1/(1+1j*f/fc))**4; x = irfft(X))
```
Key: quantize at the LOW rate, upsample with ZOH (not interpolation), lowpass only lightly afterward. For a filter-off "ring" output, skip the final lowpass.

## 4. Transient shaping without lookahead (dual envelope follower)

Classic SPL Transient Designer topology (differential envelope): two rectified envelope followers with different attack times; their difference isolates the attack; a second pair with different release times isolates sustain. Gain = product of the two shaped ratios. Works sample-by-sample, zero lookahead.

```
def env(x, atk_ms, rel_ms, sr):             # one-pole peak follower on |x|
    aa, ar = exp(-1/(atk_ms*1e-3*sr)), exp(-1/(rel_ms*1e-3*sr))
    e = 0; out = empty_like(x)
    for n in range(len(x)):
        a = aa if abs(x[n]) > e else ar
        e = a*e + (1-a)*abs(x[n]); out[n] = e
    return out
fast, slow = env(x,0.1,50,sr), env(x,15,50,sr)      # attack detector pair
attack_env  = np.maximum(fast - slow, 0) / (slow + 1e-9)
fast2,slow2 = env(x,5,50,sr),  env(x,5,300,sr)      # sustain detector pair
sustain_env = np.maximum(slow2 - fast2, 0) / (fast2 + 1e-9)
y = x * (1 + attack_amt*attack_env) * (1 + sustain_amt*sustain_env)   # amt in ~[-0.8, +2]
```
Speed note: the follower is a data-dependent recursion; for one-shots it's short, or vectorize the release-only case with `np.maximum.accumulate` tricks. Since your renderer already knows hit onsets, a cheaper offline alternative: multiply each hit by a synthetic `1 + g*exp(-t/tau_atk)` envelope anchored at the known onset. Source: SPL Transient Designer white papers / standard "differential envelope" descriptions (e.g., SPL manual, DAFx envelope-follower literature).

## 5. Gated reverb (80s snare)

Algorithm (offline, trivial with known onsets): big reverb, then hard-gate the tail with a hold+fast-release envelope keyed to the dry hit.

```
wet = fftconvolve(dry, big_bright_ir)        # dense IR, 1.5-3 s decay, boost 1-5 kHz
gate = np.zeros(len(wet))
for t0 in snare_onsets:                       # you already know these
    h  = int(hold_ms*1e-3*sr)                 # hold 80-150 ms
    r  = int(rel_ms *1e-3*sr)                 # release 5-30 ms (fast = the effect)
    gate[t0:t0+h] = 1.0
    gate[t0+h:t0+h+r] = np.maximum(gate[t0+h:t0+h+r], np.linspace(1,0,r))
out = dry + wet_gain * wet * gate
```
Character tips: use a nonexponential (flat/gated-plate-style) IR — e.g., white noise with *constant* amplitude for 200 ms then zero — so the gate cut is brutal; slight predelay 0–10 ms; mono-sum the tail below 300 Hz. Origin: Hugh Padgham/Phil Collins "In the Air Tonight" gated ambience (widely documented, e.g., Sound On Sound "Classic Tracks").

## 6. Euclidean rhythms (Bjorklund) + real-groove table

E(k,n): distribute k onsets as evenly as possible over n steps = Euclid's GCD algorithm on interval structure (Bjorklund 2003, SNS timing paper; Toussaint 2005 "The Euclidean Algorithm Generates Traditional Musical Rhythms").

Simplest correct implementation (no list-shuffling needed):
```
pattern = [ (i*k) % n < k for i in range(n) ]      # E(k,n), one standard rotation
# or onset positions: floor(i*n/k) for i in range(k)
```
Rotations matter — real grooves are specific rotations. Documented matches (Toussaint):
- E(3,8) = [x..x..x.] tresillo (Cuban / habanera / reggaeton kick)
- E(5,8) = cinquillo
- E(2,5) = Khafif-e-ramal; E(5,16) = Bossa-nova necklace (rotated)
- E(7,16) ≈ Brazilian samba necklace; E(5,12) = Venda / South African
- E(4,9) = Aksak (Turkey); E(9,16) ≈ West/Central African bell rotations
Use: k,n per lane (e.g., kick E(3,8), hat E(7,16) rotated 1) + your swing on top. Source: cgm.cs.mcgill.ca/~godfried/publications/banff.pdf

## 7. Groovebox generative tricks (Elektron/TR-8S-style, all trivially offline)

- **Ratchets / retrigs**: replace one hit with m sub-hits spanning one step: `times = t0 + arange(m)*T16/m`, velocity ramp `v * linspace(0.7, 1.0, m)` (or decreasing). m ∈ {2,3,4}; pitch each retrig up a few cents for flams-to-buzz.
- **Per-step chance**: each step carries `p`; render hit iff `rng.random() < p`. Use a seeded RNG per bar so re-renders are reproducible. Common musical values: main hits p=1.0, ghost/ornament steps p=0.25–0.6.
- **Conditional trigs / fill-every-N**: Elektron "A:B" condition = play only on pass A of every B loops. `play = (bar_index % B) == (A-1)`. Fill logic: mark steps as `fill_only`; render them when `(bar_index+1) % 4 == 0` (every 4th bar) — typically extra snare 16ths in the last half-bar, or swap hat lane to ratchets.
- **Velocity-from-pattern**: accent grid (e.g., accents on E(3,8) positions) adds +20–30 velocity.
Source: Elektron Digitakt manual (trig conditions), Roland TR-8S manual (per-step probability/sub-steps) — standard documented features.

## 8. Tape / vinyl character

**Wow/flutter** = pitch modulation via modulated-delay resampling (variable-speed read with linear interp):
```
# phase-modulated read position
t = np.arange(N)
mod = d_wow*np.sin(2*pi*f_wow*t/sr + ph) + d_flut*flutter_noise(t)
pos = t + mod*sr                          # mod in seconds
y = np.interp(pos, t, x)                  # linear-interp resample (numpy-only)
```
Numbers (Wikipedia wow-and-flutter measurement; SOS "Are wow and flutter key to analogue tape sound?"; Baby Audio wow/flutter article):
- Wow: 0.5–3 Hz (turntable wow is once-per-rev: **0.556 Hz at 33⅓ RPM**, 0.75 Hz at 45). Depth: cassette spec 0.1–0.3% speed deviation → mod peak = 0.001–0.003 * (1/f_wow)/(2π) seconds; audible "lo-fi" settings 0.2–1%.
- Flutter: 6–12 Hz (drive motor), scrape flutter >1 kHz (skip — inaudible as pitch). Depth ~0.05–0.2%. Use filtered noise (one-pole-LP'd randn, cutoff ~10 Hz) rather than a sine for realism.
- Percent→cents: 1% speed ≈ 17 cents.

**Crackle**: sparse random impulses + filtered noise bed.
```
clicks = np.zeros(N); idx = rng.random(N) < rate/sr        # rate 5-30 clicks/sec (Poisson)
clicks[idx] = rng.uniform(-1,1,idx.sum()) * rng.random(idx.sum())**2   # mostly small, few big
clicks = onepole_hp(clicks, 300) ; clicks = onepole_lp(clicks, 8000)   # band-limit thumps/fizz
bed = onepole_lp(rng.standard_normal(N), 2500) * 0.003                 # surface noise ~-50 dB
```
**Dusty HF rolloff**: gentle first-order lowpass at 6–10 kHz (vinyl-era masters) or a shelf −6 to −12 dB above ~8 kHz; add fixed 30–60 Hz rumble at −45 dB for turntable feel. Do it in your existing FFT spectral-mask EQ.

## 9. Haas widening for drums

Precedence effect (Haas 1949): a delayed copy within ~1–35 ms fuses into one event localized toward the earlier side; beyond ~35–40 ms it splits into an echo.
```
L = x ;  R = delay(x, d_ms) * g       # or split: dry both sides + delayed opposite side
```
Safe drum ranges: **d = 8–20 ms for hats/percussion/room layers; 3–10 ms max on snare top layers; NEVER on kick/808/sub**. Why bass stays mono: (a) at 60 Hz, 10 ms is ~2/3 of a cycle → mono-sum comb filtering can nearly cancel the fundamental; (b) low frequencies carry the most energy, so channel-asymmetric bass wastes headroom and wrecks vinyl/club playback. Rule: mono below 120–200 Hz. Always check mono-sum: `mono = (L+R)/2` and compare RMS vs dry — if a comb notch hits the fundamental, shorten d. Attenuate the delayed side 2–6 dB (g≈0.5–0.8) to keep the image from pulling. Source: Haas precedence-effect literature (Haas 1949, *The Influence of a Single Echo on the Audibility of Speech*); standard mixing guidance (SOS stereo-width articles).

## 10. Velocity humanization (human-drummer ranges)

Findings across MIDI-performance and groove studies (see Frane 2017; PMC6025871 "Groove in drum patterns..."; standard drum-programming references):
- Variation is **structured, not white noise**: metric-position accents dominate. Backbeat snare loudest; 8th-note hats alternate strong/weak by ~15–25 MIDI velocity; 16th subdivisions weaker still.
- Ghost notes are a separate population: ~30–50% of the accent velocity (keep ≥15 velocity-points gap from main hits so they read as ghosts).
- Residual per-hit randomness on top of the accent pattern is small: σ ≈ 3–8 velocity units (≈0.5–1.5 dB); timing jitter σ ≈ 3–12 ms.
- Repetition of an *identical* bar is the giveaway — vary at bar level (re-roll the small jitter each bar, keep the accent map fixed).
```
vel = accent_map[step] * lane_base                       # deterministic structure
vel *= 2 ** (rng.normal(0, 0.12) )                       # ~ +/-1 dB lognormal wobble
vel = clip(vel, ghost_min if is_ghost else main_min, 1.0)
gain = (vel)**1.6                                        # velocity->amplitude curve (perceptual)
```

## Suspicious content
None encountered.

## Source list
- melodiefabriek.com/sound-tech/mpc-swing-reason/ (MPC swing mechanics, 96 vs 960 PPQ)
- attackmagazine.com — Roger Linn interview "Swing, Groove & the Magic of the MPC's Timing"
- mpc-forums.com t=139021 (96 PPQ tick range for swing)
- ethanhein.com/wp/2022/dilla-time/ ; academia.edu "21st Century Funk: Microtiming of J Dilla"; Charnas, *Dilla Time* (2022)
- Frane 2017, *Music Perception* 34(3):291 — swing in 30 classic breaks, median ratio 1.2:1
- en.wikipedia.org/wiki/E-mu_SP-1200 ; samplesfrommars.com SP-1200 page; gearspace SP-1200 filter thread (12-bit/26.04 kHz, SSM2044, no reconstruction filter, drop-sample repitch, 45→33 trick)
- SPL Transient Designer documentation (differential envelope topology)
- Sound On Sound "Classic Tracks: In the Air Tonight" (gated reverb origin)
- Toussaint 2005, "The Euclidean Algorithm Generates Traditional Musical Rhythms" (BRIDGES) — E(k,n) pattern table; Bjorklund 2003 SNS paper
- Elektron Digitakt / Roland TR-8S manuals (trig conditions, probability, ratchets)
- en.wikipedia.org/wiki/Wow_and_flutter_measurement ; soundonsound.com wow/flutter Q&A; babyaud.io/blog/wow-and-flutter
- Haas 1949 precedence effect; pmc.ncbi.nlm.nih.gov/articles/PMC6025871/ (groove/velocity study)
