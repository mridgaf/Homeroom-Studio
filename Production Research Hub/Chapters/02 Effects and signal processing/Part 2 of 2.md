# Chapter 02: Effects and signal processing
## Part 2 of 2

_Compression, EQ, saturation, reverb, delay, stereo width, convolution and beat-repeat: the research, techniques, and the upgrade proposals._

**In this part:**
- EFFECTS-UPGRADE-PROPOSAL.md — Sound of Science — Effects Upgrade Proposal (2026-10-16)
- LOW-END-LAYOUT-PROPOSAL.md — Beat Machine — Instrument Layout + Low-End Proposal (2026-09-23)
- 2026-08-08-sound-engine-mixer-design.md — Sound Engine: multi-stem mixer + deep effects

(Next: end of chapter)


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

=====================================================
SOURCE FILE: 2026-08-08-sound-engine-mixer-design.md
ORIGINAL LOCATION: HS:docs/superpowers/specs/2026-08-08-sound-engine-mixer-design.md
=====================================================

# Sound Engine: multi-stem mixer + deep effects

## Context

The Sound Engine app (`sound_engine/`) currently loads one audio file at a
time and shapes it with 5 real-time effects (EQ, Compressor, Saturation,
Stereo Width, Reverb) — live preview via Web Audio API in the browser,
export via the same Python DSP the beat generator uses
(`tools/audio_engine.py`, pedalboard-backed).

The owner asked for two things, explicitly ambitious, explicitly not a
"lightweight product":

1. **Control over each stem of a generated beat** — his beat generator
   (`tools/beat_machine.py`) already writes every stem (kick, snare, hat,
   bass, everything) as a separate WAV file next to every beat it renders
   (`write_stems()` in `tools/beat_recipes.py`), but nothing lets him load
   and mix them.
2. **More than one slider per effect** — real depth, not just a single
   knob standing in for a whole effect.

Non-negotiable constraint, his words: *"I want to be able to hear the
changes I make while I'm making them. That's the point."* Every control in
scope must update live while audio plays, in the browser, via Web Audio —
not a batch "Apply" step. This is why VST plugin hosting was ruled out for
this round: pedalboard can load real VST3/AU plugins, but only the Python
server process can host them, and routing live audio through Python was
already tested and rejected earlier the same day (Python's garbage
collector causes audible clicks — "the opposite of AAA quality"). VSTs
would only ever be able to shape the exported file, never the live
preview, which breaks the one rule that matters most here. Off the table
for this round; deferred, not rejected outright.

**Explicitly out of scope for this round** (owner's own words: "I will
have a longer list [of new effect types] once the first ones are
stable"): Gate, master-bus Limiter, Multiband Compressor, Chorus, Phaser,
Delay. These exist in `tools/audio_engine.py` already but get no UI in
this round.

## What ships this round

1. A real multi-channel mixer: pick a beat from the library, every stem
   loads as its own channel, all play together, each channel gets the
   full effects rack, one Play/Stop, one export.
2. The 5 existing effects gain their real parameter depth — every new
   knob maps to a parameter that **already exists** in
   `tools/audio_engine.py` or pedalboard's own plugin classes today,
   confirmed by reading the actual signatures (see below). No new DSP
   code, no new dependency.

## Architecture: one "project," one or more "channels"

Today's single-file flow and the new multi-stem flow become the same code
path: a **project** has 1+ **channels**. Dragging in one file today's way
creates a 1-channel project (today's exact behavior, unchanged). Picking a
beat from the library creates an N-channel project, one channel per stem.
One engine, one UI paradigm, no duplicated logic between "simple mode" and
"mixer mode."

### Server-side session model (`sound_engine/server.py`)

Replace the current flat `SESSIONS: dict[file_id -> {dry, wet, ...}]` with:

```
PROJECTS: dict[project_id -> {
    name: str,               # beat title, or the dropped file's name
    channels: {
        lane_id: {
            label: str,       # "kick", "snare", real sample name, etc.
            sr: int,
            dry: (L, R),
            wet: (L, R),
            gain_db: float,   # channel fader, default 0
            pan: float,       # -1..1, default 0
            muted: bool,
            solo: bool,
            params: {...},    # this channel's effect settings
        }
    },
}]
```

Eviction/cap logic (`MAX_SESSIONS`, `_evict_old_sessions`) carries over
unchanged in spirit — cap on project count, same reasoning (bounded memory
over a long working session), same cleanup of associated scratch files.

### New endpoints

- `GET /api/library/beats` — list beats available to load. Reuses
  `tools/beat_machine.py`'s `_resolve_beats_root()` (same
  `beats_root.json` / `REASON_VOICE_BEATS_ROOT` lookup, same "drive not
  mounted" warning behavior — do not reimplement this, import and call
  it). Scans each DJ subfolder for files matching `NN * Drums *bpm*.wav`
  and pairs each with its sibling `NN * Stems` folder (same leading beat
  number, found in the same parent directory — confirmed exact naming
  from `beat_machine.py`'s `write_stems()` call site: `folder / f"{no}
  {names} {title} Stems"` sits next to `folder / f"{no} {names} {title}
  Drums {bpm}bpm.wav"`). Beats whose Drums file has no matching Stems
  folder are omitted from the list (nothing to mix). Response: list of
  `{beat_id, dj, title, bpm, stem_count}`, newest first.
- `POST /api/project/from-beat/{beat_id}` — loads every stem in that
  beat's Stems folder via `dsp.load_audio()` (already handles arbitrary
  sample rates), creates a project with one channel per stem file.
- `POST /api/project/from-upload` — today's `/api/upload`, renamed and
  returning a 1-channel project instead of a bare file_id. (Internal API,
  no external consumers besides `app.js` — no back-compat shim needed,
  update both sides together.)
- `POST /api/project/{project_id}/channel/{lane_id}/process` — today's
  per-file `/api/process/{file_id}` body, scoped to one channel; also
  accepts `gain_db`, `pan`, `muted`.
- `GET /api/project/{project_id}/channel/{lane_id}/{dry|wet}` — today's
  `/api/audio/{file_id}/{variant}`, scoped to one channel.
- `POST /api/project/{project_id}/export` — processes every unmuted (or
  solo'd) channel through its own chain, applies each channel's gain/pan,
  sums to a stereo mix, runs a peak-safety clamp (reuse
  `audio_engine.brickwall_limit` — it already exists, this is not a new
  mastering rack, just clip protection on the sum), writes one new file
  to `~/Desktop/Homeroom Sound Engine Exports/` exactly as today.

### Client-side (`sound_engine/static/app.js` — near-full rewrite)

Today's module-level singletons (`lowShelf`, `compressor`, `wetGain`,
etc.) become a `channels` array of objects, each holding its own full
node set (the exact same node graph `buildGraph()` builds today, just
factored into a function that returns a channel object instead of
assigning module globals). Each channel's output feeds a per-channel
`GainNode` (fader) → `StereoPannerNode` (pan) → a shared `masterGain` →
`audioCtx.destination`. Mute = zero the channel gain node (ramped, not an
instant cut, to avoid a click). Solo = mute every channel that isn't
soloed (standard solo semantics).

**Playback sync:** one `AudioBufferSourceNode` per channel, all created
and `.start()`'d in the same tick against the same `audioCtx.currentTime`
offset — sample-accurate, since Web Audio schedules starts against the
audio clock, not wall time. All stems from one beat render are already
identical length (same render pass), so a shared Loop toggle keeps them
locked; no per-channel loop state.

**UI:** a channel list (name, fader, pan, mute, solo) plus one "selected
channel" detail pane showing that channel's full effects rack — not N
simultaneous full racks (a beat can have 10+ stems; showing every panel
open at once is unusable). Matches how Ableton itself shows track list +
one open device chain. Clicking a channel in the list opens its rack in
the detail pane; the currently-open channel's knobs are the only ones
rendered as live DOM sliders at a time, but every channel's Web Audio
graph keeps running regardless of which one is "open" in the UI (closing
a panel must never stop that channel's audio processing or reset its
values). Channels list in whatever order the Stems folder's files are
read in — no canonical lane ordering (kick-first, etc.) in this round;
revisit only if the default order actually feels wrong in use.

## Deepened effects — every new knob maps to a real, already-existing parameter

Confirmed by reading current signatures, not assumed:

**EQ** — `tools/audio_engine.py` `eq3(L, R, low_db=0.0, low_hz=120.0,
mid_db=0.0, mid_hz=800.0, mid_q=0.9, high_db=0.0, high_hz=8000.0, sr=None)`.
Today only the three `_db` values are wired to sliders; `_hz`/`mid_q` are
hardcoded in `buildGraph()`. Fix: add sliders for `low_hz`, `mid_hz`,
`mid_q`, `high_hz`; live side sets `lowShelf.frequency.value` /
`midPeak.frequency.value` / `midPeak.Q.value` / `highShelf.frequency.value`
(native `BiquadFilterNode` params, already the node types in use — no new
node types). Export side passes the same values through to `eq3()`, which
already accepts them.

**Compressor** — `glue_compressor(L, R, threshold_db=-14.0, ratio=2.5,
attack_ms=12.0, release_ms=180.0, makeup_db=2.0, sr=None)`. Today
`server.py` hardcodes `makeup_db=0.0` to match the live
`DynamicsCompressorNode`, which has no makeup-gain concept built in. Fix:
add a makeup gain slider; live side adds one `GainNode` after the
compressor node (`makeupGain.gain.value = 10 ** (db / 20)`), export side
passes the same `makeup_db` through instead of hardcoding 0.

**Reverb** — `algo_reverb`/`loop_algo_reverb(L, R, room_size=0.5,
damping=0.5, wet=0.25, dry=0.9, width=1.0, freeze=False, sr=None)`. Every
one of these already exists in the Python function signature and maps
directly to `pedalboard.Reverb`'s own real parameters (`room_size`,
`damping`, `wet_level`, `dry_level`, `width`, `freeze_mode`) — confirmed
by reading `pb.Reverb`'s actual attribute list. Today only `room_size`
(via the "Size" slider) and a single coupled mix knob (driving both `wet`
and `dry` as `mix`/`1-mix`) are exposed. Fix, 6 independent knobs:
  - `wet` / `dry` become two separate sliders (no more coupling).
  - `damping` (tone of the tail — live approximation: a `BiquadFilterNode`
    lowpass on the wet path only, cutoff frequency driven by the damping
    knob; darker at low damping, brighter at high).
  - `width` (stereo width of the tail specifically — live: reuse the
    exact M/S gain-scaling pattern already built for the channel's own
    Stereo Width effect, applied to the reverb's wet signal only, not the
    whole channel).
  - `freeze` (infinite sustain toggle — live: when on, generate the
    impulse response with a flat/non-decaying envelope instead of
    `makeReverbIR()`'s current exponential decay; when off, restore the
    normal decaying IR at the current Size).

**Saturation, Stereo Width** — confirmed these are already at their full
native parameter depth (`saturate(L, R, drive_db, mix)` maps to
`pedalboard.Distortion`, which only has `drive_db`; `stereo_width(L, R,
width)` is a 6-line hand-rolled M/S function with nothing else to expose).
Staying as 2 knobs and 1 knob respectively — adding more here would mean
inventing new DSP, which is part-3 territory the owner explicitly deferred,
not "deepening" something that already has more to give.

## Error handling

- **Drive not mounted when browsing beats:** `_resolve_beats_root()`
  already handles this (warns, doesn't silently show an empty library) —
  reuse it verbatim, surface its warning text in the UI instead of a bare
  empty list.
- **A beat's Stems folder is missing or empty:** omit that beat from
  `/api/library/beats` entirely rather than showing a beat that can't
  actually be loaded.
- **Malformed/corrupt stem file:** same handling as today's single-upload
  path (`dsp.load_audio()` raising -> clean 400, no orphaned file) — apply
  per-stem during a beat load; one bad stem should skip that one channel
  with a visible warning, not abort loading the other 9 good ones.
- **Project/session cap:** same eviction pattern as today, scaled down —
  a multi-channel project's arrays are proportionally larger (10+ stereo
  pairs instead of 2), so cap at 3 concurrent projects instead of today's
  5 single files.

## Testing

New tests build a small fixture beat+stems folder under `tmp_path` (a
folder with a `"1 Test Beat Drums 90bpm.wav"` file and a sibling `"1 Test
Beat Stems"` folder containing 2-3 tiny WAVs) and point the library
scanner at it via a monkeypatched root — **never** the real
`beats_root.json`/TBOTC 3 path, which isn't always mounted and must never
be a test dependency. Cover: beat listing (finds the fixture, skips a
Drums file with no matching Stems folder), loading a beat into a
multi-channel project, per-channel process/export, mute/solo affecting
the exported mix, and the deepened EQ/Compressor/Reverb parameters
actually reaching the exported audio (same pattern as the existing
`test_reverb_size_top_of_slider_is_not_saturated` — assert two different
parameter values produce measurably different output).

## Explicitly deferred (not part of this spec)

New effect types (Gate, master Limiter, Multiband Compressor, Chorus,
Phaser, Delay) and anything VST-related. Owner will bring a longer list
once this round is stable and confirmed by ear.

=== END OF PART ===
