---
name: drum-loops
description: Synthesize mixed-and-mastered drum loop packs (24-bit WAV) from scratch — 808/boom-bap/trap/drill/house patterns with tuned sliding subs, hat rolls, swing, and seamless looping. Use whenever the user asks for drum loops, beats, a beat pack, "make me five drill loops in F", "make the Slow Roller dirtier", new percussion sounds, or wants existing generated loops changed, re-tempoed, re-tuned, or extended. Any request to CREATE audio drum material (not search for it) is this skill.
---

# Drum Loops

Generate loops by editing and running the synthesizer at
`/Users/johnsuhr/Desktop/Homeroom Studio/tools/make_drum_loops.py`.
Read it first — patterns, sounds, and the master chain are all there and
it's the single source of truth. Output lands in
`~/Documents/Samples/Claude Drum Loops/` where the Reason Voice app indexes
it (group=drums, category=loop, bpm parsed from the filename).

## How the script thinks

- **Sounds are synthesized**, 808-style: `kick808` (sine + pitch drop),
  `sub808(freq, dur, glide_to=)` (tuned bass with optional slide),
  `snare808`, `clap`, `hat(open_=)`, `cowbell`, `tom808`, `rim`. New sound =
  new small function from these building blocks (noise + `bandpass`/
  `highpass` + `env` covers most percussion).
- **Patterns are strings**: 16 chars = one bar of 16ths, 32 chars = 32nds
  (that's how hat rolls are written). Velocity: `X`=accent, `x`=normal,
  `o`=half, `.`=ghost, `-`=rest. Each loop lists 4 bars per track; make
  bar 4 the fill/variation.
- **A loop entry** is `(name, bpm, swing, humanize, tracks)`; a track is
  `(sound_fn, pan, gain, [bar strings])`. Old-school styles want
  swing 0.05–0.09 and humanize ~0.002s; trap/drill want both at 0.
- **808 tuning**: pass note frequencies to `sub808` (A=55.0, G=49.0,
  F=43.65, E=41.2). Drill slides = `glide_to=` a lower note. "In F" means
  sub_f-style helpers — add one per key needed.
- **Naming**: keep `Drums` and the bpm in every filename
  (`"Drill Drums - Cold Slide" 142bpm.wav` pattern) — the word `Drums`
  routes it to the drums bin and `NNNbpm` powers tempo search.
- Mastering (mono bass, air shelf, tanh glue, −0.5 dBFS peaks, tail folded
  back for seamless looping) is already in `master()`/`render()` — don't
  re-implement it, just add loops.

## Workflow

1. Read the script; add or edit entries in `OLD_SCHOOL`/`MODERN` (or a new
   style list — any list of loop tuples fed to the same loop in `main()`).
2. Run: `cd "/Users/johnsuhr/Desktop/Homeroom Studio" && ./.venv/bin/python tools/make_drum_loops.py`
3. Sanity-check the printed table: duration must equal 4 bars at the bpm,
   RMS between about −16 and −8 dBFS. Way outside = a gain mistake.
4. Tell him: say **"rebuild index"** in Reason Voice, then
   **"audition drum loops"** to hear them (skip / that one / star two).

## Research library (read before designing new styles)

`references/techniques.md` holds cross-checked, numbers-first beat-making
knowledge: MPC swing math and calibration (54/58/62%), Dilla lane offsets,
trap hat-roll grammar, kick/808 layering and distortion chains, reverb
numbers (plate/room/gated), SP-1200/MPC/ASR-10 machine characters, bus and
loudness targets (−8 LUFS), texture recipes (vinyl/wow/foley), Euclidean
and groovebox generative tools, and era arrangement habits. The three raw
research reports (producers / forums / DSP) sit beside it for deep dives.
Contested findings are marked — resolve those by rendering BOTH options
and letting the owner's ears decide. `references/connections-2026-07.md`
holds the cross-report synthesis (drums-only emotion ladder, silence
dose-response, bar-RMS contrast rule, frisson recipe) — read it when
designing arrangements or tuning a character's feel. Owner rule for
"school"/research sessions: SYNTHESIZE the existing corpus first; only
go out for new web research when he explicitly asks.

## Snare balance (feedback 2026-07-14)

Snares/claps read too hot by default because reverb/gate/swell add energy
on top of the dry fader. House fix in `groove.OWNER_TASTE`:
`snare_trim_db = -3.5` (apply via `snare_scale()` to snare + clap lanes)
and `gate_wet = 0.3`. The −8 LUFS master re-normalizes afterward, so this
makes the snare quieter RELATIVE to the kit while loudness holds. Keep
snares tucked in every batch; flag any style that genuinely wants a hot
snare at the audition stage.

## Owner A/B verdicts (July 2026 — house defaults, see groove.OWNER_TASTE)

He auditioned rendered pairs and ruled: Dilla lanes = **snare early**
(woozy) with kick leaning late; SP-1200 dirt at **half strength**
(amount=0.5 blend); trap kick↔808 **sidechain on ~90%** of beats (vary —
1 in 10 skips it); master = the **modern −8 LUFS chain** always; snare
space (revised 2026-07-15) = **vary gated and dry** across a batch. Era-driven deviations are
allowed but flag them for his ears at the prototype stage.

## The crew (nine DJ personalities)

Personality-beat requests ("make me an Otto Grit beat", "evolve the
crew") belong to the dedicated **beat-crew skill** — use it, not this
one. The presets live in `tools/crew.py`; stamps are locked in
`~/.reason_voice/crew_kits.json`; evolution is journaled in
`~/.reason_voice/crew_journal.json`.

## Panning rule (feedback 2026-07-15)

He caught hats parked to one side across every beat. Timekeeper lanes
(hats, snaps) stay subtle — |pan| ≤ 0.2 — and VARY in side between
beats/characters. Wide placement is for occasional color (bongos, fx,
stamps), never the groove's pulse. Also: not every beat gets a long
drawn-out 808 — vary kick sustain between beats.

## Novelty pipeline (owner rule)

When research (or your own synthesis of it) surfaces a **truly unique or
untried** idea — something with no documented mainstream use, not merely
uncommon (say honestly which it is) — render **two beats from that one
idea** so he can hear it. Hard cap: **3 novelty beats per day**
(lowered from 10 on 2026-07-15), tracked in
`~/.reason_voice/novelty_log.json` as {"YYYY-MM-DD": count} — check and
update it before rendering. Never pad to hit the cap; fewer good ideas
beats filler. Name files
"Experiment NN <Idea> Drums <bpm>bpm.wav" in the Claude Drum Beats folder
and document the idea, its source, and why it's novel in the README.
Candidates so far unexplored (see connections-2026-07.md for the first
three): Roughness 808 (30-80 Hz AM on the sub tail = documented threat
band as a menace knob), swung club kick (Jersey grammar at 56-58% swing,
~94 bpm), bar-synced wow (pitch sag locked to bar length).

## Standing production rules (from the owner — always apply)

- **Never put "Claude" in a beat/loop filename** — the output folder name
  carries the branding; files are just "NN Name Drums NNNbpm.wav".
- **Sample-based beats** (`tools/make_drum_beats.py`) — a second engine
  beside the synthesizer; it sequences HIS one-shot library. For those:
  always a **real 808 kick sample** (`musts={"kick": "808"}` — matches
  name or folder path; ~280 exist) and real sample snares, never synth
  fallbacks. Era chokes: `"_kick_secs"` in tags (0.9 = 1994 thump,
  1.1 = 2000s, 2.2 = 2010s sustained sub).
- **Reverb is welcome** — `verb=(decay_s, tone_hz, {role: wet})` sends
  per-role convolution reverb; his library also has pre-reverbed snares
  (want-tags "room", "reverb"). Room ~0.45s for boom bap, plate ~0.9s for
  2000s, hall 1.8s+ for 2010s.
- **Nontraditional sounds replacing hats sometimes** — the "fx" bucket
  (lasers, reversed hits, vinyl crackle, foley) can take over the hat
  pattern for bars or whole beats. Keep fx gain ≤ 0.35.
- **Bongos sparingly, never loud** — "bongo" bucket, gain ≤ 0.32, a few
  hits per bar at most.

## Honesty

You can't hear the output — say so. Describe what was changed in plain
words ("kick decays longer, hats quieter and wider") and let his ears
judge. If he says a loop sounds wrong, ask what specifically (too clicky?
sub too quiet? hats harsh?) and map that to a parameter: clicky→`click=`,
weak sub→sub gain/`drive`, harsh hats→hat gain or the 7200 Hz highpass.
Regeneration is cheap — offer variants rather than arguing.
