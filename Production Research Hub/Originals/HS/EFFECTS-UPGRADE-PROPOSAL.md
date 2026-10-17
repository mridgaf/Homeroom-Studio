# Sound of Science — Effects Upgrade Proposal (2026-10-16)

Research only. Nothing changed, nothing rendered.

## Why they sound thin — the root causes

| # | Cause | Where |
|---|---|---|
| 1 | **What you hear while turning knobs is NOT the real effect.** The page plays a quick browser copy (Web Audio). Export uses a different engine. Reverb live = fake noise tail; chorus/phaser live = hand-built stand-ins. | `static/app.js` 392–570 |
| 2 | **Drive is one hard clipper** with no tone control and no oversampling → fizzy, harsh top ("aliasing" = fake high frequencies). | `audio_engine.saturate` |
| 3 | **Reverb is Freeverb (1990s design)** → metallic ring, no pre-delay, no early reflections, no tail EQ. Pro reverbs cut lows and highs on the tail. | `audio_engine.algo_reverb` |
| 4 | **Echo repeats are all the same brightness.** Real tape/analog delays darken and blur each repeat. No ping-pong, no beat-sync. | `audio_engine.loop_delay` |
| 5 | **Width widens the bass too** → muddy, collapses on phones/clubs. | `audio_engine.stereo_width` |
| 6 | **Each knob moves only 1–2 settings in a straight line.** Pro "macro" knobs move several settings along a curve, so 30% already sounds good. | `static/effects.js` EFFECTS |
| 7 | **No output safety per effect** — turning up adds volume, and louder fools the ear; no auto level match. | chain-wide |

## Effect by effect — what changes

| Knob | Now | Pro version |
|---|---|---|
| EQ | bass + air shelf | Musical curves (Pultec-style "boost + dip" low end), high-pass to clean mud, auto gain-match |
| Compress | ratio + makeup | Soft knee, sidechain high-pass (kick stops pumping it), auto makeup, parallel blend ("NY compression") |
| Drive | hard clip | 4× oversampled soft/tape curve, tone filter after, low-end kept clean, 3 flavors: Tape / Tube / Crunch |
| Width | side gain | Bass stays mono below ~150 Hz, Haas/micro-delay widening, mono-safety check |
| Chorus | 1 voice | 2–3 voices, different speeds L/R, slight darkening (Juno-style) |
| Phaser | 1 sweep | more stages, feedback/"resonance", tempo-synced sweep |
| Echo | clean repeats | Repeats darken + saturate (tape), ping-pong, beat-synced (1/4, 1/8 dotted), slight wobble, ducks under the dry |
| Stutter | ok | add pitch/fade per repeat, tempo grid |
| Reverb | Freeverb | Pre-delay, early reflections, tail EQ (cut <200 Hz, >8 kHz), Room/Plate/Hall types, duck under dry |
| Convolve | needs your file | ship a starter pack of free real-room/plate/spring IRs |

## Three ways to get there (can combine)

| Tier | What | New installs? | Size |
|---|---|---|---|
| **A. Fix the live preview** | Knobs play the real export engine (server renders a short loop as you turn). What you hear = what you export. | none | medium |
| **B. Rebuild effects in our code** | Items above, with tools already installed (pedalboard + numpy). Loop-safe rule kept. | none | large |
| **C. Host free pro plugins** | pedalboard can load Mac plugins. **Airwindows** (free, MIT, Mac AU/VST3: ToTape, Density, Console) for drive/tape; **Dragonfly Reverb** (free, GPL: Room/Plate/Hall/Early Reflections). | yes — 2 downloads | small code, big jump |

Recommended order: **A first** (otherwise you can't judge any upgrade by ear), then **C for Drive + Reverb**, then **B for Echo, Width, Compress, knob curves**.

## Added 2026-10-16: what the other two folders give us

### Plugins you ALREADY own — tested loading in our engine (white-noise test, no beats)

| Plugin | Loads? | Controls | Use for |
|---|---|---|---|
| **Obliterate** (Newfangled Audio) | ✅ | 23 | Pro distortion → new **Drive** "Crunch" flavor |
| **DS-10 Drum Shaper** (XLN) | ✅ | 6 (attack, sustain, kick tightness, snare body, presence) | New **Punch** knob for drum stems |
| **AIR Multiband Filterbank** | ✅ | 40 | Multiband shaping / filter sweeps |
| **Gateway** (amp modeler) | ✅ | 14 (bass/mid/treble, gate) | Amp/cabinet grit for bass + keys |
| Apple reverb/limiter (built into macOS) | ❓ check hung | — | maybe a better reverb; retest |
| ReaVerb, ReaComp, ReaDelay (REAPER) | ❌ old VST2 format, our engine can't load | — | — |

→ Tier C may need **fewer or zero downloads**: Drive and a Punch knob are covered by plugins you already own.

### Sonic Reference Engine — reuse
- **`comparator.py`**: compares two sounds and names what's different. Use it to
  check each upgraded effect against a reference sound with numbers, before your ears.
- Its key lesson applies here: judge an effect by **before vs after**, never alone
  (real bass already measures "distorted").
- **REAPER effect source code** (`~/Library/Application Support/REAPER/Effects`, plain readable text) —
  recipes to copy ideas from: *Bad Buss Mojo w/AA* (smooth drive that avoids the fizzy top), *Delay Tempo / Ping-Pong*,
  *Chorus Stereo*, *1175* (1176-style compressor), *Event Horizon* (clipper), Loser *Transient Controller*, *Saturation*, *Exciter*.
  Learning only: their licenses vary, so I write our own versions rather than copying their code.

### Ardour 9.7 source (Downloads) — learning only
- **a-delay**: tempo-sync + low-pass *inside the feedback* = exactly the "darker repeats" fix for Echo.
- **a-comp**: soft knee + sidechain → model for the Compress upgrade.
- **a-reverb**: same old style as ours, no gain. **zita-convolver**: we already have convolution.
- License: Ardour is GPL — read for ideas, don't paste its code in.
- Nothing worth building into the app. You can move this folder out of Downloads when you like; we don't need it.

## Caveats
- Dragonfly: no confirmed Apple-Silicon Mac build yet — must check on download.
- Plugins from outside may be blocked by macOS Gatekeeper once (one approval click).
- Every change needs your ears; tests can't hear "cheap".

Sources: [Pedalboard (Spotify)](https://engineering.atspotify.com/introducing-pedalboard-spotifys-audio-effects-library-for-python/), [pedalboard plugin loading](https://pypi.org/project/pedalboard/0.9.2), [Dragonfly Reverb](https://wiki.linuxaudio.org/apps/all/dragonflyreverb), [Airwindows ConsoleX3](https://bedroomproducersblog.com/2026/09/30/airwindows-consolex3/), [Airwindows](https://equipboard.com/brands/airwindows), [Tape delay feedback-loop tone (Reel Tape)](https://vintageking.com/avid-reel-tape-suite)
