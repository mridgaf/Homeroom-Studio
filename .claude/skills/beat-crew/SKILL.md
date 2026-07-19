---
name: beat-crew
description: Make beats as one of the nine DJ personalities (Otto Grit, Cutz, Crate Prophet, Chrome Dial, Glass Cat, Sunday Chop, Night Metro, Rage Engine, New Math) or one of the twelve Legends — signature-style producers (Farrow, Doc Day, Kane East, J Dillo, Mustang, Swish Beatz, DJ Premium, Timberline, Just Flame, Razor, Hitt Kid, No Alias) — and evolve the crew between batches. Use whenever the user names a crew member or Legend ("make me an Otto Grit beat", "two more from Night Metro", "a Doc Day beat", "something like Dilla/Premier/Timbaland"), asks for personality/producer-style beats, says "evolve the crew" or "next batch", asks for traditional hip-hop beats or a tuned root/808, wants a drum swapped or a beat's variations, wants to play/sort a batch into favorites or trash, gives audition feedback on Proto/crew beats, or asks who's in the crew.
---

# The Beat Crew

Nine invented DJ characters, each built closely on one real producer's
documented style. Since 2026-07-16 their numbers live in
`/Users/johnsuhr/Desktop/Homeroom Studio/crew_config.json` (the
editable roster, per the DJ Drone Machine spec — auto-written from
`tools/crew.py`'s DEFAULT_CREW on first run, loaded ever after; delete
it to regenerate). Read crew.py for the machinery and the config for
current timing numbers, arrangement habits, and mix flavor.

| # | Name | Built on | BPM | Feel in one line |
|---|------|----------|-----|------------------|
| 1 | Otto Grit | J Dilla | 88 | snare early, kick late, hats straight, half dust |
| 2 | Cutz | DJ Premier | 93 | surgical 53% swing, ghost notes, scratch stabs |
| 3 | Crate Prophet | Pete Rock / Madlib | 92 | 60% swing, late snare, congas, vinyl+wow |
| 4 | Chrome Dial | Timbaland | 100 | straight syncopated bounce, silence as instrument |
| 5 | Glass Cat | The Neptunes | 98 | minimal, no hats, late-clap flam, bone clean |
| 6 | Sunday Chop | Kanye | 96 | 57% gospel bounce, big clap, driving kicks |
| 7 | Night Metro | Metro Boomin | 140 | dark halftime, ramped rolls, drop-outs |
| 8 | Rage Engine | Lex Luger | 150 | wall-to-wall 32nd rolls, distortion, relentless |
| 9 | New Math | no one — the front edge | 144 | Jersey-club kick grammar, quintuplet hats, Euclidean perc, one lane swung against a straight kit |

These are the crew — NOT the numbered beats in `make_drum_beats.py`
(Anvil, Sunroof, …); those are earlier one-off beats, not characters.

**There is a THIRD roster (2026-07-19):** seventeen subgenres — Baltimore
Club, Reggaeton Alt, Memphis, Houston Screw, Trip Hop, Plug and the rest
— in their own box, keyed to scenes rather than people. They deliberately
do NOT follow the rules on this page (that is the point: fidelity over
variety). See [beat-styles](../beat-styles/SKILL.md) before touching
`pattern_gen`, `vary_preset`, or anything that rebuilds `CREW`.

## How to render one

```python
from crew import CREW, build_kit, lock_stamps, render_crew_beat
from make_drum_beats import build_shots
shots = build_shots()
stamps = lock_stamps(shots)                      # producer tags, locked
kit, sources = build_kit(shots, "Otto Grit", stamps["Otto Grit"][1],
                         variant=N)              # N = which beat
L, R, lufs = render_crew_beat("Otto Grit", kit)
```

`render_crew_beat` already applies EVERYTHING downstream — snare trim,
gated/room space, sidechain, dust, vinyl, the −8 LUFS master. Do not
re-apply any of those to its output; just `write_wav24` it.

**Where the library lives (moved 2026-07-18):** `/Volumes/TBOTC 3/Claude
Drum Beats` — off iCloud, onto the external drive beside the sample packs
(that drive must be connected to make a beat anyway, since the one-shots
are on it). The path is NOT hardcoded any more: `beats_root.json` at the
project root pins it, `REASON_VOICE_BEATS_ROOT` overrides, and failing
both, `_resolve_beats_root()` searches the usual spots and picks whichever
actually contains beats. This exists because the old hardcoded
`~/Documents/...` path went missing when he turned off Desktop &
Documents sync, and the machine would otherwise have silently started an
EMPTY library and restarted numbering on top of 309 existing beats. If
the library ever looks empty, check that the drive is mounted first.

Output naming: `NN Name Drums NNNbpm.wav` (spaces, no underscores) in
`<beats root>/<DJ name>/` — since 2026-07-15
every beat lives in its DJ's own subfolder (collabs with the
first-named DJ; also `Early Beats/` = pre-crew 01-20, `Prototypes/`,
`Experiments/`). Never the word "Claude" in a filename; numbering is
GLOBAL across all subfolders (`beat_machine.next_number()` computes
it). Log sample sources in the root README.txt.

## v6 — THE LOOSENING (owner directive 2026-07-18, supersedes below)

Owner verdict: "Variety is more important than staying true to style.
Minimal constraints while keeping the personality." Identity is now ONLY
the stamp + mix flavor (dust/vinyl/clean/distortion) + tempo zone.
Superseded rules are marked ⊘ below; these rules govern:

- **Sample-pack library.** `sample_packs.json` (project root) lists pack
  roots (his two TBOTC pack folders); `tools/sample_library.py` does
  folder-aware classification (a file in KICKS/ is a kick whatever its
  name). One-shots only — loops, MIDI, presets, instrument folders
  (bass/melodic/keys/vocals) auto-skipped; >6 s rejected (fx/crash 10 s).
  EXTENSIBLE: drop packs into a root or add a path to the JSON; next
  launch picks them up (durations cached; unplugged drive falls back to
  cache). Pools went ~2-4x (kick 861, snare 604, hat 596...).
- **Density fully FREE** ⊘ sparse-bed rule. sparse/home/busy equally
  likely; the notes box still forces one.
- **Swing rolls per beat** ⊘ locked timing DNA. Wide window around the
  DJ's home feel + 10% outliers; whole kit shifts together so lane
  clashes survive. README notes "swing NN%".
- **Time signatures: 80% 4/4, 10% real 3/4 or 6/8** (12-step grids,
  filename gets " in 3-4"/" in 6-8", MIDI carries the meta), **10%
  exotic-grid beats in 4/4** (quintuplets, 32nd walls, gallops boosted).
- **Space rolls per beat** ⊘ odd/even gated/dry parity: gated .35 /
  dry .35 / room .2 / plate .1; notes box overrides ("gated", "dry",
  "roomy", "washed").
- **Every mode for every DJ** (v6 grammars, STYLE_VERSION 6): backbeat +
  timekeeper menus are full for everyone, weights only LEAN home. Kick
  banks 16-18 skeletons each and CROSS-POLLINATE (15% borrow another
  DJ's book — README says so). Guests up to 2 lanes.
- **Notes box vocabulary grew**: no snare / no hi hats / acoustic /
  sparse / busy / no 808 / long 808 (as before) + gated / dry / roomy /
  washed / no swing / more swing / triplet swing / 3/4 / waltz / 6/8 /
  half time. Still one-click-only, echoed "(as asked)".
- Migration: crew_config.v5.backup.json holds the pre-v6 roster;
  evolution deltas were re-applied on top of v6 defaults.

## THE LEGENDS — the second roster (owner request 2026-07-18)

Twelve producers modeled DIRECTLY on real signatures, under sound-alike
names, in `tools/legends.py` + `legends_config.json` (same editable
contract as crew_config.json). They are merged into `CREW` at import via
`crew.merge_legends()` so every engine function reaches them by name;
`crew.LEGEND_NAMES` marks them. They get their OWN box on the page.

| Name | Built on | BPM | Name | Built on | BPM |
|------|----------|-----|------|----------|-----|
| Farrow | Pharrell / Neptunes | 98 | DJ Premium | DJ Premier | 93 |
| Doc Day | Dr. Dre | 93 | Timberline | Timbaland | 100 |
| Kane East | Kanye West | 90 | Just Flame | Just Blaze | 94 |
| J Dillo | J Dilla | 88 | Razor | RZA | 87 |
| Mustang | DJ Mustard | 100 | Hitt Kid | Hit-Boy | 96 |
| Swish Beatz | Swizz Beatz | 95 | No Alias | No I.D. | 92 |

**They follow the nine's INSTRUMENT SOUND-VARIATION rules only** — fresh
sample picks per beat, cross-session anti-repetition history, per-beat
kick sustain ranges, subtle varied-side timekeeper pans, one locked
stamp, open sound bank. **Everything else is new LIKENESS rules** (keyed
off `preset["legend"]`):

- grammar weights stay heavily HOME — no v6 flat menus;
- kick banks never cross-pollinate INTO a legend (`LEGEND_KICK_BANK`;
  the loose nine may still borrow a legend's book);
- swing stays within ±2 of the signature feel — `legend_swing` pins it
  outright for Doc Day (50), DJ Premium (53), Just Flame (54), Razor
  (52), No Alias (54) — and never rolls the straight/triplet outliers;
- no random 3/4, 6/8, or exotic-grid beats (the notes box may still ask);
- **no engine-driven evolution** — a legend's career is already written
  (`generate` filters them out of `evolution.maybe_evolve`).

Collabs with the nine are allowed and use the normal loose 50/50 rules —
collaborating IS stepping out of character.

## The batch player + Favorites/Trash (owner request 2026-07-18)

The page plays the batch he just asked for and lets him sort it:

- Every track from the last click renders as a draggable card with an
  HTML5 player (`GET /audio?no=NN`, byte-range supported so seeking
  works). Only a beat NUMBER crosses the wire — resolved to a file
  server-side, so no client path ever touches disk.
- **Drag a card** (or tap ★ / 📁 / 🗑) onto a bin: Favorites, DJ folder,
  or Trash. `POST /triage` MOVES the wav, its `.mid`, and its Stems
  folder. **Trash is a folder move, never a delete** — nothing is ever
  destroyed. Anything he leaves alone stays in its DJ folder.
- Placement IS where the file lives (`beat_location` reads the top-level
  folder), so it survives everything. The batch itself is remembered in
  `~/.reason_voice/beat_machine_state.json`, so closing, relaunching, or
  asking for a new batch all behave: `GET /batch` repopulates the player
  with current placements. Test/`--out` renders never touch that state.

## Full-stem swap + song-family folders (owner request 2026-07-18)

- The swap dropdown is now **built from the beat's own recipe**
  (`GET /lanes?no=NN` → every `kit_spec` lane), so guest colors —
  congas2, exotic2, blips, clicks, cutfx, risers, crash2 … — are all
  swappable, not a hardcoded seven. Stamps stay locked; the synthesized
  root sub isn't a sample, so it isn't offered.
- Swapping any sound files the song and every variation into ONE folder:
  `<DJ>/<NN Title> Variations/`. The original is MOVED in the first time
  (left alone if he'd already filed it in Favorites/Trash).

## Traditional half + "add the root" (owner rule 2026-07-18)

- **A batch of 4 or more comes out half traditional** (`_traditional_flags`,
  interleaved). A traditional beat keeps the BACKBONE common and popular:
  kick straight from the DJ's curated bank, snare/clap locked to a plain
  2&4 backbeat, no library-seed detours, no odd meter or exotic grid.
  Hats, perc, guests and fx still roll free — familiar, not generic.
- **"Add the root"**: traditional beats get a tuned 808 sub on a musical
  root (C D E F G A Bb, low octave) mirroring the final kick line —
  about 40% of them, so *808 is not in everything*. Skipped when the kick
  already rolled a LONG 808 (that sample carries its own sub). It's a
  real synth layer (`sub808`), rides the un-ducked bass path with the
  kick, prints its own stem (`sub - synth 808 sub, root A.wav`), lands in
  the MIDI on note 35, and the root note goes in the README + recipe so
  swaps rebuild it.

## The standing rules (owner decisions — do not drift)

- **They all experiment (2026-07-14).** No fixed kick or snare per
  character. Every beat re-picks drums from that character's taste tags
  via `build_kit(variant=N)`. Only the **stamp** — their producer-tag
  hit, present in all their beats — is locked
  (`~/.reason_voice/crew_kits.json`). Never re-pick a stamp unless he
  asks.
- **Kick sustain varies (2026-07-15).** Not every beat gets the long
  drawn-out 808: each character has a choke *range* in `CREW[...]["kit"]`
  and `build_kit` rolls a length per beat.
- **Hats are never parked on one side (2026-07-15).** Timekeeper lanes
  (hat/snap) stay subtle, |pan| ≤ 0.2, and the side varies by character.
  Wider placement is for occasional color (bongos, stamps, fx), not the
  groove's pulse.
- **Machine truth.** SP-1200 dust (at `OWNER_TASTE["sp1200_amount"]`)
  belongs to the three 90s heads only; Chrome Dial, Glass Cat, Sunday
  Chop, and the 2010s three stay clean.
- **Snare space varies (owner verdict 2026-07-15).** No more single
  house treatment: ALTERNATE gated and dry across a batch (odd/even
  file number works), logged per beat in the README.
- **Crate Prophet's snare runs extra quiet (2026-07-15).** His lane
  gain is 0.62 (≈3 dB below the others) on top of the house −3.5 dB
  trim, and his snare wants no longer include pre-reverbed samples.
- **New Math is half boom bap (2026-07-15).** On ODD variants use
  `crew.boom_bap_variant(bpm≈92-96)` — the math survives at boom-bap
  tempo with 58%-swung hats, dusty snare, short kick, half dust and a
  vinyl bed. Even variants stay pure front-edge.
- **Variety is a hard requirement (2026-07-16).** Owner verdict: beats
  that share a rhythm skeleton read as "the same beat slightly changed"
  — he wants every beat significantly different from the next, no
  matter the DJ; that's what the school was for. Sample-swapping alone
  is NOT variety. Every beat (machine or batch) must differ in pattern
  AND arrangement: `beat_machine.vary_preset` is the floor (small-hit
  mutation, kick-grammar wander, density profile, hat density, one
  structural treatment from the school notes, tempo lean), and every
  loop must measure >=4 dB bar-RMS swing (school §4; the machine
  deepens and re-renders automatically if it comes up flat). Timing DNA
  (LaneFeel, swing) and stamps stay untouched — the character survives,
  the beat doesn't repeat.
- **He plays over the top — room means SPARSE, never silent
  (2026-07-17, supersedes the 2026-07-15 hole rule).** Every beat is a
  BED for the owner's live instruments, but "room" is fewer drums
  playing, NOT gaps: no silent bars, no 2-beat holes, no DJ-cuts. The
  kick+snare backbone plays through every bar; quiet moments = hats and
  colors resting plus velocity dips (vary_preset "thinbar"/"frisson"
  keep the backbone; the bar-swing floor is 2.5 dB via thinning). Beats
  lean noticeably sparse overall: density weights favor sparse, kick
  hits ~2-5/bar, thin hat modes, max ONE guest lane.
  Timekeepers stay subtle so his voice owns the mids.
- **The notes box steers ONE click only (2026-07-17).** Directions
  typed in the Beat Machine notes box ("no hi hats", "no snare",
  "acoustic", "dusty", "sparse", "no 808") are parsed
  (beat_machine.parse_directions) and applied to the beats of that
  click ONLY — never persisted to config, crew, or later generations.
  Applied directions echo in the README as "(as asked)". Parser
  spellings are GENEROUS ("no high hats", "remove the cymbals", "take
  out the kick" all work) — when he reports a miss, check the README
  "notes:" line for his exact wording and add it to LANE_WORDS.
- **Kick banks + final-pattern guard (2026-07-17, 2nd round).** Each DJ
  carries ~10 curated kick skeletons (pattern_gen.KICK_BANK) — the
  composer starts from one 75% of the time, freestyles otherwise. The
  kick is IMMUNE to the density pass (it once eroded two beats into the
  same line), and generate() re-checks the FINAL post-variety kick
  against the DJ's rendered history ("<name>#final" in
  pattern_history.json), rerolling the variant until it's ≥3 moves from
  everything recent.
- All of `groove.OWNER_TASTE` applies (sidechain on ~90% of beats).
  Check the live values rather than trusting numbers written here — they
  have been revised twice: as of 2026-07-18 the master targets **−12
  LUFS with a −4 dBFS peak ceiling** (was −8/−1: beats redlined when
  dropped into Reason), the snare bus trim is **−5 dB** (was −3.5, the
  snare still sat over the kick), bright percussion has its own −3.5 dB
  bus, and `clean_renders` is ON — every dirt stage (808 distortion,
  roughness, saturation, dust, vinyl, wow) stays off because he adds his
  own color in Reason.

## Evolution (owner rule 2026-07-15: "we'll have them evolve as we go")

The crew are characters with careers, not frozen presets. Each new batch,
every character featured in it changes **one deliberate thing** — a new
kick-length zone, a fresh snare flavor, a pattern habit, a new
arrangement trick from the research — while their timing DNA (LaneFeel
numbers, swing) and stamp stay recognizable.

Track it in `~/.reason_voice/crew_journal.json`:

```json
{"Otto Grit": [{"date": "2026-07-15", "batch": "prototypes",
                "change": "baseline established"}]}
```

Before rendering a batch: read the journal so you know where each
character currently is. After: append one entry per featured character
saying what evolved, and mention it in the output README. Evolve one
step at a time — his ears audition every batch before the next
(quality-first project; never rush).

## The pattern grammar (owner verdict 2026-07-17)

Owner heard every machine beat coming out with the same rhythm — the old
engine only mutated each DJ's ONE hardcoded skeleton, every kick was
forced to be an 808 (must="808"), the accent sequence repeated, and the
lane roster was frozen. `tools/pattern_gen.py` replaced that:

- **compose()** writes a FRESH pattern per generation from the DJ's
  grammar (per-step kick weights, backbeat modes + ghosts, timekeeper
  modes incl. 32nd roll walls and New Math's quintuplets). Grammar,
  kick_flavors, and extras live per-DJ in crew_config.json (editable —
  tune numbers there when his audition feedback says a DJ is off).
- **Kick flavors**: each DJ rolls 808 vs clean/short per beat,
  era-weighted. Owner rule (later 2026-07-17): must="808" is GONE from
  every base kick spec, long-sustain 808 is ≤0.2 weight even for the
  trap DJs (a mid-choke 808 tier sits between), and a STREAK-BREAKER in
  compose() forbids any flavor running 3 beats in a row.
  NOTE: the Beat Machine server holds loaded code — after any engine
  change, kill the process on port 8770 so his next launch reloads.
- **Guest lanes**: 0-2 extra colors per beat (shaker, rims, toms,
  congas, blocks, fx one-shots) from that DJ's palette.
- **Pattern memory**: ~/.reason_voice/pattern_history.json keeps each
  DJ's last 24 rhythms; a kick line within 2 moves of a recent one (or
  3 with matching modes) regenerates. vel_seed varies accents per beat.
- Backbeats hold their mode all beat (identity); fills live only in
  phrase tails. Timing DNA and stamps still never touched.
- Collabs compose fresh per parent BEFORE dealing the 50/50 jobs.

Tests: tests/test_pattern_gen.py. Owner offered to drop the tempo/count
UI options and wait minutes per beat for quality — not needed (the
sameness was the one-skeleton design, not speed); options kept.

## The variety + evolution machinery (built 2026-07-17, 2nd session)

Owner-approved architecture: engine-driven evolution with rollback,
numeric variety scoring, and an autoresearch tune-then-audition loop.
The reason-voice repo is now a GIT REPO (initialized 2026-07-17).

- **Variety scorer — `tools/variety.py`.** Reads the saved `.recipes/`
  and scores each DJ's recent window: pairwise kick moves (floor: min 3,
  mean 4.5), kit overlap (max 50% between consecutive beats), flavor
  streaks (max 2), bar swing (min 2.5 dB, `--audio`). CLI:
  `./.venv/bin/python tools/variety.py [--dj NAME] [--last N] [--audio]`.
  `generate()` runs a quick check after every render — warnings land in
  the README, never block. Tests: tests/test_variety.py holds the
  floors against the live engine (sameness-drift regression).
- **Groove-library seeding is WIRED (was dormant).** The 131-groove
  pattern_library import existed but compose() never called it — fixed
  2026-07-17. Each DJ has a "library" style key in crew_config.json
  (seed chance p + genre tag weights); seeded kicks pass _thin_kick,
  _bank_vary, and both repeat guards. STYLE_VERSION is now 5.
- **Engine-driven evolution — `tools/evolution.py`.** First time a DJ
  is featured in a day, the engine applies ONE bounded change from an
  11-op menu (kick zone, flavor lean, mode weights, ghosts, guests, new
  color, library taste...) to crew_config.json, journals the exact
  delta, and notes it in the README ("<DJ> evolution: ..."). Timing
  DNA, stamps, bpm, mix flavor are NOT on the menu. When his ears
  reject a change: `./.venv/bin/python tools/evolution.py --rollback
  "Name"` (also --status, --history, --evolve). Evolution sets
  `_style_lock: true` so future STYLE_VERSION syncs can't erase
  careers. Only fires for the real library root (never tests/--out).
  Tests: tests/test_evolution.py.
- **Autoresearch loop (tune-then-audition).** Branch
  `autoresearch/crew-variety-2026-07-17` in the repo. Experiments edit
  ONLY `experiments/crew_config.candidate.json`; the locked harness
  (`autoresearch.sh` → `experiments/score_variety.py`) scores compose-
  time variety; `checks.sh` runs 44 identity tests against the
  candidate before any keep. Winners staged as
  `crew_config.proposed.json` + PROPOSAL.md — the LIVE config only
  changes after he auditions (render a scratch batch with
  `REASON_VOICE_CONFIG=<proposed> ... beat_machine.py --render ...
  --out <scratch>`). Never edit the live config from the loop.
- **`REASON_VOICE_CONFIG` env var** points crew.py at any roster file —
  how proposals and tests load tuned crews safely.

## The Drone Machine layer (spec landed 2026-07-16)

`~/Downloads/dj-drone-machine-spec.md` is the reference doc; all four of
its new features are BUILT (tools/beat_recipes.py + beat_machine.py):

- **Every beat ships as WAV + MIDI + stems.** Same basename `.mid` next
  to the wav, per-lane 24-bit stems in a "NN … Stems" subfolder (vinyl
  bed is its own stem; stems are un-glued — the WAV is the reference).
- **Recipes + swap flow.** Each render saves `<root>/.recipes/NN.json`.
  "Same beat, different snare" = `swap(NN, "snare")` — web page card or
  `--swap NN --lane snare`. Pattern/groove/other sounds locked, new
  numbered file, nothing overwritten. Only beats from 2026-07-16 on.
- **Anti-repetition persists across sessions.**
  `~/.reason_voice/sample_history.json` remembers the last 6 picks per
  DJ per lane and feeds the avoid set; stamps exempt. Hard rule.
- **Collabs are 50/50** (owner override 2026-07-16 — supersedes the
  spec doc's 80/20 AND the old host-carries-it recipe): the four jobs
  (kick, backbeat, timekeepers, color) are dealt 2-2 between the
  parents, each lane keeping its parent's pattern, groove, and drum
  taste; mix flavor averaged, kick_dist follows the kick's parent, both
  stamps ride. First-checked DJ still names the folder.

Tests for all of it live in `tests/test_beat_machine.py`.

NOTE (2026-07-18): the swap flow now files results into song-family
folders and the lane list is dynamic — see the two sections above.

## Project state

Folders + Beat Machine (2026-07-15): all beats reorganized into per-DJ
subfolders; `tools/beat_machine.py` is his self-serve jukebox. Double-
clicking "Beat Machine.command" opens it as a LOCAL WEB PAGE in his
browser (stdlib http.server on 127.0.0.1:8770, `run_web()`) — NOT a Tk
window: macOS ships the deprecated Tk 8.5.9 which fails to paint plain
tk widgets AND ttk widgets on his machine (verified 2026-07-15 via
screenshots), so the native-GUI path was abandoned. The page has a
checkbox per DJ (JS tracks click ORDER so the first-checked DJ hosts and
the beat lands in their folder — his original spec), tempo override,
how-many-beats 1-10, notes box logged to README; 1 checked = solo, 2+ =
collab. CLI test mode still works: `--render "Name,Name" --tempo N
--count N --notes "..." --out DIR`. It applies the standing rules itself (gated/dry by file-number
parity, ~10% no-sidechain, New Math boom bap on odd variants). Batch
scripts now skip files found ANYWHERE under the beats root (rglob) and
only touch README/journal when they actually rendered something.
Batch 5 delivered (2026-07-15): files 68-85 via `tools/make_two_each.py`
(school findings applied: frisson builds, B-section timbre shifts;
Roughness 808 and swung-club-kick debuts; engine gained grid_accent for
20/32 grids, tempo-scaled gate hold, and groove.roughness_am).
Batch 3 delivered (2026-07-15): files 41-67 via
`tools/make_three_each.py` (3 per member, gated/dry alternating,
New Math boom-bap 2-of-3, Crate's three = the no-sidechain renders).
Checkpoint 4 delivered (2026-07-15): files 21-40 rendered via
`tools/make_the_twenty.py` (2 per member, beat B = that character's one
evolution, + 2 collabs with both parents' stamps). Snap Church retired
that day (owner: too close to Night Metro/Rage Engine) — New Math holds
slot 9. The 13 "Proto" files and the Alt snare-space questions
(Otto/Cutz/Crate gated vs room; Glass Cat gated vs dry) still await his
verdicts. NEVER re-render or overwrite existing beat files unless he
explicitly asks (owner rule 2026-07-15) — batch scripts must skip
existing paths. Tests: `tests/test_crew.py` must stay green
(`./.venv/bin/python -m pytest tests/ -q` from the Homeroom Studio root).

## Honesty

You cannot hear the renders — verify numerically (duration, LUFS −8ish,
RMS sanity, per-bar levels) and say so plainly. His ears are QA: describe
what changed in plain words and let him judge. Regeneration is cheap —
offer variants instead of arguing.
