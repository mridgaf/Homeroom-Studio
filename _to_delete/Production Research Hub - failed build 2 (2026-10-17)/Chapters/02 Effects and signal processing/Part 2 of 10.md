# Chapter 02: Effects and signal processing
## Part 2 of 10

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- EFFECTS-UPGRADE-PROPOSAL.md — Sound of Science — Effects Upgrade Proposal (2026-10-16)
- LOW-END-LAYOUT-PROPOSAL.md — Beat Machine — Instrument Layout + Low-End Proposal (2026-09-23)

(Next: Part 3 of 10)


=====================================================
SOURCE FILE: EFFECTS-UPGRADE-PROPOSAL.md
ORIGINAL LOCATION: HS:EFFECTS-UPGRADE-PROPOSAL.md
=====================================================

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

=====================================================
SOURCE FILE: LOW-END-LAYOUT-PROPOSAL.md
ORIGINAL LOCATION: HS:LOW-END-LAYOUT-PROPOSAL.md
=====================================================

# Beat Machine — Instrument Layout + Low-End Proposal (2026-09-23)

Scope: drums + 808 + bass only. Loops left out entirely (owner, 2026-09-23).
Status: PROPOSAL — nothing built. Needs owner OK per item.

## What the code does today (checked in files, not assumed)
- 808 lane ("bass") copies the kick's pattern exactly — beat_machine.py ~1583.
- Low end (sub/808) ducks 5.0 dB under the kick (SUB_DUCK_DEFAULT, owner's ear 2026-09-01).
- Melodic bass notes (bass0..N) are NOT in _LOW_END, so they only get the
  mix-wide duck (~1.4-3.7 dB depending on DJ) — crew.py _lane_sc().
- Duck shape: instant attack, fixed 90 ms release at every tempo (make_drum_beats.duck).
- Hits on a lane stack (crew.py ~1587). A second 808 hit does not cut the first,
  so close kicks (e.g. "X-x") = two 808 tails summing = mud/phase smear.
- No choke between hats: open hat keeps ringing under the closed hat.
- Hard rule 2026-09-14 "don't pile lows on lows": a LONG 808 kick counts as the
  beat's one low sound, so no 808 lane is added under it.
- Sampled 808 appears on ~40% of beats (SAMPLED_BASS_P).

## Proposed track layout (mirrors MPC A01-A16 / TR-8S / Maschine)
| # | Track | Job | Ducked by kick | Choke / mono |
|---|-------|-----|----------------|--------------|
| 1 | Kick (short "top" kick) | punch/click | never (it's the trigger) | — |
| 2 | 808 | sub + note | YES, 5 dB (keep) | mono: new hit cuts old |
| 3 | Bass notes | melodic low | YES, same low-end duck | mono |
| 4 | Snare | backbeat | no | — |
| 5 | Clap / Snap | backbeat layer | no | — |
| 6 | Closed hat | timekeeper | light (mix duck) | chokes open hat |
| 7 | Open hat | timekeeper | light | choked by closed hat |
| 8 | Perc 1-3 | color | light | — |
| 9 | Crash / FX | punctuation | light | — |
| 10 | Chords / instruments | harmony | light (mix duck) | — |

## Changes, in order of payoff
1. Bass notes join the low-end duck (put bass0..N on the 5 dB duck). Small change.
2. 808 goes mono (choke itself): each new 808 hit fades the previous one out in ~5 ms.
3. Kick + 808 together: when an 808 lane is on, pick a SHORT punchy kick
   (keeps the 09-14 one-low-sound rule — two long 808s in the same range is mud).
4. Duck shape: 2-3 ms attack ramp (avoids a click on a ringing sub) and release
   tied to tempo (about a 1/16 note: ~110-170 ms at 90-140 BPM), industry range 100-150 ms.
5. Hat choke group: closed hat cuts open hat (MPC mute target / TR-8S standard).
6. Optional: 808 lane gets its own rhythm (not only kick copies) — trap/Metro style
   808s that land between kicks. Owner decision needed (touches 07-29 bassline history).
7. Optional: duck only below ~120 Hz (multiband) so the 808's grit stays audible.

## Sources
- majormixing.com/10-tips-for-mixing-808 (tune, saturate, sidechain, decay, mono <100 Hz, don't layer two 808s in one range)
- iconcollective.edu/808-mixing-tips (top kick over 808; kick transient first, 808 fades in)
- audeobox.com/learn/fl-studio/how-to-sidechain-in-fl-studio (4-6 dB, fast attack, 100-150 ms release)
- rolandcorp.com.au TR-8S guide (kick-triggered sidechain on bass track)
- mpc-forums.com / mpc-tutor.com (mute targets: closed hat chokes open hat)

=== END OF PART ===
