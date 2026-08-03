# Scratch (live reasoning trace)

Disposable. Cleared or overwritten each session. Purpose: capture the *path*
through a problem, not just the destination — so if I reverse course, the
reason is visible instead of lost.

One line per turning point. Not a transcript.

Format:
```
- [tried/considered] X → [result] → [kept / reversed because Y]
```

---

## Session 2026-08-01 — owner's six-point punch list (clap/crash, gaps,
## vocal hits, chord limits, length, missing breaks)

Status: MEASURED, nothing changed yet. Waiting on his answers.

### Method
Measured rather than read code (same method that worked 07-31). Two data sets:
- 506 recipe JSONs in `/Volumes/TBOTC 3/Claude Drum Beats/.recipes` — what he
  has actually been listening to.
- 1,560 FRESH in-memory generations (39 identities x 40 variants) through
  `pattern_gen.compose` + `beat_machine.vary_preset` — what the engine does
  TODAY. The library is diluted by pre-07-29 beats, so the fresh number is the
  honest one. Where they differ I quote both.

### 1. Clap + crash
- clap lane present: 44% fresh / 49% library.
- **Of beats with BOTH snare and clap, 89% fresh / 93% library put the clap on
  EXACTLY the same 16th steps as the snare.** Not variety — a doubled backbeat
  nearly every time. Causes: (a) 6 identities declare `{"copy":"snare"}`
  outright (Glass Cat, Rage Engine, Farrow, Just Flame, Hitt Kid, Acid Rap
  Bright); (b) everyone else's clap grammar weights mode "backbeat" 0.45-0.9
  and the snare rolls backbeat too, so they collide anyway.
- crash lane present only 9% fresh / 6% library — **but when present it fires a
  MEDIAN of 14 hits per loop, max 51.** One line causes it:
  `pattern_gen.py:1123` hands EVERY guest lane the timekeeper grammar
  (offbeats/sparse/answer), so a crash cymbal is programmed like a shaker. And
  `EXTRA_SECS["crash"] = 2.2`, so each of those hits rings 2.2s.
- RULED OUT: "crashes are on too many beats." They aren't. It's the density.
- The `stamp` lane (on 100% of beats) is NOT the problem — median 2 hits/loop,
  correctly punctuation. Only the guest path is broken.

### 2. The gaps — there IS a rule, and it is his own
`beat_machine.py:383-442`, step 4 of `vary_preset`. Every beat gets one of four
structural treatments; `thinbar` and `frisson` blank EVERY non-canon lane for a
whole bar, and step 4b blanks the back half of a bar on `bshift`/`quietbar`.
The hole is not occasional, it is by design.
- Fresh: **47% have a completely silent bar, 90% have a hole of some kind.**
- Smoking gun, by beat number: 1100-1399 = **0%** silent bar. 1400-1499 = 6%.
  1500-1599 = **57%**. 1600-1699 = **42%**. The cutover is exactly the
  2026-07-29 owner call that removed the BACKBONE floor.
- Blocking: that ledger entry, plus `tests/test_beat_machine.py:654
  test_backbone_can_go_fully_silent_for_a_bar`, which ASSERTS the gap exists.

### 3. Vocal hits — two sources; he probably only knows about one
- `beat_machine.py:941 VOX_LANE_P = 0.3` — vox one-shot on 30% of beats, gain
  0.5, downbeat of bar 1 + '&' of the last bar. Library 28.7%. Gets its own
  stem AND sits in the main mix.
- Separately **17 of 18 genres plus 5 crew/legends carry "vocal" in their
  `stamp` tags**, so the fx stamp is often a vocal too. Zeroing VOX_LANE_P
  alone would NOT stop the vocal hits. 22% of library beats have a vocal-ish
  sample somewhere.

### 4. Chord limits — the complaint is literally true
- Pool is 27 progressions; **each identity is allowed only 2-5** (mean 3.4).
  Roots 3-5, modes 2-8, voices 1-4 per identity.
- **68% of rendered beats get a 1- or 2-chord progression.**
  `vamp_static_riff` (ONE chord, held) alone is 18.8% of the library.
- Pool composition: 1 chord x1, 2 chords x12, 3 chords x6, 4 chords x8.
  Nothing longer than 4 exists.
- `key_context.CHORDS` has 14 qualities; the progressions use 9. Never used:
  `aug`, `add9`, `7#9`, `sus4`, `5`. 76% of chords in the pool are plain
  major/minor triads.
- Ceiling on any fix: 2026-07-29 rule, `part_count = 1` in `_build_chords` —
  one melodic voice per beat, no stacking, ever.

### 5. Length — reversed my first assumption
First guess was that renders were being cut off mid-bar. WRONG — checked two
wavs, durations are exact bar multiples (3.000 and 8.000 bars). So:
- fresh: 2-bar 9%, 4-bar 33%, 8-bar 58%; library: 13% / 44% / 40%.
- 25 of 506 (5%) are odd METERS — 19 in 3/4, 6 in 6/8. A 3-bar 3/4 loop
  (7.91s) is the only genuinely odd-feeling length found.
- Set at `pattern_gen.py:943` (crew rolls 2/4/8 at 0.15/0.60/0.25, genres
  pinned to 8) — from the 2026-07-22 owner call "make the loops half as long".
- 16 bars is not on the table today at all.
**Do not guess which of these he means. Asked.**

### 6. Breaks (Funky Drummer / Amen / Impeach)
- `pattern_library/` has 180 entries. Contains `amen-break-classic` and
  `jungle-amen-rework` (filed under **electronic**, not hip-hop) plus generic
  `funk-breakbeat-chop` / `funk-sixteenth-ghost-groove`. **No Funky Drummer, no
  Impeach the President, no Apache, no Assembly Line, no Synthetic
  Substitution.**
- `pattern_library/README.md:71-75` says so outright: "original,
  characteristic patterns... not copies of specific copyrighted recordings."
- Library IS wired in (`_pick_library`, weighted per DJ) but `lib_p` is only
  0.10-0.65, so most beats never see a seed.
- **The killer for his ask:** `pattern_gen.py:1039-1042` refuses a library
  snare seed for `legend` and `traditional` beats. DJ Premium, Kane East,
  J Dillo, No Alias — the exact producers built on these breaks — can NEVER
  receive a break's snare figure. And a kick seed passes `_thin_kick` +
  `_bank_vary` first, so it's an influence, not the groove.
- Format is friendly: `load_library` accepts 16- or 32-step entries (2-bar
  breaks fit) and globs `patterns_*.json`, so a new `patterns_breaks.json`
  drops in with no code change.

### Config plumbing — matters for any fix
`crew_config.json` has `_style_lock: true`, so `load_crew` will NOT re-sync
`grammar`/`kick_flavors`/`extras`/`library` from the .py defaults, and
`signature` is never overwritten regardless. Any chord-limit change must go in
BOTH the live JSON (so his machine sees it) and the .py defaults (so a fresh
install matches). Editing only the .py does nothing on his machine.

### Flagged, not touched
`crew_config.json` has an uncommitted edit adding `["rim", ["clave","wood"],
"claves"]` to one DJ's extras pool. Unknown provenance. Do not clobber it.

---

## VERIFY PASS (same day) — owner: "make sure you're not generalizing"
He was right to push. Rendered **42 real beats** to a scratch dir and measured
the audio and the stems. Several of my own claims changed.

### Corrections to my own first report
- **"The crash is broken" was too narrow.** EVERY guest lane gets the
  timekeeper grammar: rim 3.8 hits/bar, bongo 3.8, crash 3.5, fx 3.4, perc 3.4.
  `impacts` 4.0/bar, `risers` 3.8, `sirens` 3.6, `swellfx` 3.5, `bells` 2.2.
  Crash was just the lane I happened to open. The bug is `pattern_gen.py:1123`
  for all of them.
- **"90% of beats have a hole" was measured on PATTERNS and reads as silence.
  In the real audio it isn't.** Full mix, per-bar level vs the beat's loudest
  bar: worst dips are -8.2, -8.0, -7.5, -6.9 dB. Audible, but not a stop —
  the chords sustain through it. **BUT the DRUM STEMS ALONE go -17 to -61 dB
  in 8 of 12 beats** (one at -61 = digital silence). Since he works from stems
  in Reason, the stem number is the one that matches what he reported.
- **Clap-vs-snare is worse than I said, and verified in audio.** Timing offset
  between them: median 0.0 ms, identical swing, 1 ms jitter — literally
  simultaneous, not a flam. And across 42 beats the clap peaks **+1.2 dB above
  the kick**, the snare -1.4. The clap is the loudest drum in the beat.
- **"2-5 progressions per DJ" understated it.** Counted actual reachable
  (progression, root, mode) combinations: **Farrow = 6 outcomes, ever.**
  Baltimore Club/NOLA = 8. Mustang/Swish/Razor = 9. Half the roster <= 12.
- **"Exact bar multiples" was from 2 files.** Re-checked on 12 renders — all
  exactly 4.0000 or 8.0000 bars. Claim holds.
- **"The stamp lane is fine" — half right.** Density is fine (2 hits/loop).
  LEVEL is not: peak-vs-kick ranges -21.5 to +9.7, a **31 dB spread**.
- **NEARLY REPORTED A FEATURE AS A BUG.** 32/24/20-step bar strings look wrong
  but are deliberate — `crew.grid_accent` handles each grid (32nds, triplets,
  quintuplets). Checked before speaking. Do not "fix" these.

### New findings he did NOT ask about
1. **The stamp sample pool is tiny.** 509 picks, **32 unique files**, half of
   all picks from **6 files**. `Sub Riser.wav` is on **17% of every beat**
   made. Cause: the want-tags filter hard against his library —
   Chiptune's stamp can only ever match **5 files**, Glass Cat and Farrow
   **6**, Razor 8, Cutz and DJ Premium 11. The stamp is on 100% of beats.
2. **Clap variety is capped by his LIBRARY, not the code.** He owns 77 clap
   one-shots; the machine has already used 74 of them. Snaps: owns 23, used
   23. No code change can widen this — that's a sample-buying problem.
3. **REAL BUG, and it lands exactly on his breaks question:** `pattern_gen.py`
   gates library seeds on `len(bar) == 16`, so **all 14 two-bar (32-step)
   patterns are silently discarded for kick and snare — including the only
   Amen Break in the project.** The hat has NO such gate, so a 2-bar hat seed
   passes through and the renderer treats 32 chars as 32 steps in ONE bar
   (`crew.py:968 res = len(pat)`) — it plays at **double speed with swing
   skipped** (`if res == 16` gates the swing). Measured: 48 of 83 32-char
   hat bars on the breakbeat-tagged identities came from this path.
4. **1 in 20 fresh beats starts with no kick in bar 1; 1 in 50 starts with no
   drums at all.** Worst: J Dillo 8/40, Hitt Kid 6/40.
5. **Only the chords have a level governor.** Peak-vs-kick spread across 42
   beats: stamp 31 dB, hat 28, chord 28, snare 24, snap 20, vox 17, perc 16,
   crash 16, clap 16.
6. **The 07-31 ledger entry over-claimed.** It says the chord governor gives a
   2.2 dB spread — that was from **5 beats**. On 42: median -8.0 dB vs the
   -9.0 target, **spread 6.1 dB**. Still a big win over the 19 dB before, but
   the entry needs correcting.

## IMPLEMENTATION (2026-08-01 evening) — owner answered, said go

His answers: gaps rare at 1 in 6 / claps keep the signature stacks, otherwise
off the snare and in fewer beats / kill vocal hits completely / chords option
(c) both / mostly 4-8 bars / yes to breaks / REMOVE THE STAMP LANE / yes to
Part E (level governors). Plus a new cross-cutting rule: **"All sounds are
open to all DJs, but they try to maintain 75% of their personality within"**
— implemented as `OPEN_P = 0.25` in beat_machine.py.

**ASSUMPTION FLAGGED, not yet confirmed:** he wrote "For bright beats, stay
verbatim" in answer to the question about how faithful a break should be.
Read as "for BREAK beats, stay verbatim" — the only reading that fits the
question. One line to change if wrong.

### Part A — DONE, verified in audio (20 fresh renders)
| | before | after |
|---|---|---|
| stamp lane present | 95% of beats | **0%** |
| vox lane present | 26% | **0%** |
| crash peak vs kick | median +3.7 dB, max +9.4 | **median -7.1 dB** |
| crash hits per bar | 3.5 | **0.25** |
| stereo width (median S/M) | -13.5 dB | -13.2 dB (unchanged) |

- `STAMP_LANE = False` + `_drop_stamp()` at one choke point in generate().
  Old recipes keep their `stamp_paths`, so all 506 existing beats still
  rebuild. `stamp_paths`/`stamp_secs` are written empty for new beats so the
  app's swap list doesn't offer a lane the beat lacks.
- `VOX_LANE_P` 0.3 -> 0.0.
- Vocal words stripped from the 5 `cutfx` guest pools (genres.py + the live
  JSON, since `_style_lock` blocks the re-sync).
- `PUNCTUATION_LANES` + `punctuation_bars()` in pattern_gen.py.
- **BUG I CAUGHT BY MEASURING:** first version matched lane names exactly, so
  it missed `crash2` — the guest lane is named crash2, "crash" is the kit
  lane. The one lane he complained about was still at 3.12 hits/bar. Now a
  prefix match via `is_punctuation()`.
- **RISK I CHECKED:** removing the stamp removes a "colour" lane that was
  getting the house ambience bed, so it could have narrowed the mix.
  Measured: width median -13.5 -> -13.2, worst -21.4 -> -18.8. No harm.

### Part B — DONE, verified in patterns (2,340 fresh beats)
| | before | after | target |
|---|---|---|---|
| loop lengths | 2/4/8 bars | **4 and 8 only** | 4-8 |
| any hole (full or half bar) | 90% | **15.9%** | ~17% |
| fully silent bar | 47% | 11.2% | |
| beats starting with no kick | 5% | **0%** | 0 |
| clap on the snare's EXACT steps, non-stack DJs | 89% | **11%** | |
| clap on exact steps, declared-stack DJs | ~100% | 99% | keep |

- `HOLE_P = 1/6` splits the four treatments into rare (thinbar / frisson /
  breath) and free (bshift / quietbar). The unconditional "breath" that used
  to ride along on two of four branches is now one of the rare three.
- New step 4c: bar 1 always gets its kick back if a treatment emptied it.
- Odd meters removed from the roll in generate(); exotic grids (triplets,
  quintuplets, 32nds) KEPT — they are note values inside 4/4, not time
  signatures, and they are what gives trap and the swung genres their feel.
- `ALLOWED_BARS = (4, 8)`; J Dillo's `bar_lengths` pin [2,4] is now filtered
  rather than obeyed ("regardless of DJ" was explicit).
- Clap backbeat weight capped at 0.35 in all three JSONs AND in legends.py /
  genres.py (crew already leaned 0.24 via `_bb`). Baltimore Club protected —
  its clap is in its `canon` block.
- **MISTAKE I MADE AND FIXED:** first pass protected claps whose *mode names*
  looked canonical ("stomp"). Wrong test — the real rule is whether the
  identity's `canon` block names the clap lane. Miami Bass's canon is on the
  KICK, so its clap was wrongly skipped. Redone against the actual data.
- **SECOND MISTAKE, found by measuring per-identity instead of in aggregate:**
  the stack runs BOTH ways. I exempted the 6 with `clap: {copy: snare}` but
  missed 6 more with `snare: {copy: clap}` (Sunday Chop, Kane East, Crunk,
  Miami Bass, Plug, Swish Beatz) — all documented in their `listen` text as
  "a BIG clap with the snare tucked underneath" / "a harsh clap-snare stack".
  Both directions are now exempt.
- `_maybe_seat_snare()` gives the 4 clap-only identities (Chrome Dial, Night
  Metro, Mustang, Timberline) a snare on OPEN_P of beats, so their clap is
  free to move or rest.

### Part C — DONE (chords), verified on 15,600 picks + 24 renders
| | before | after |
|---|---|---|
| progressions in the pool | 27 | **47** |
| chord qualities reachable | 9 of 14 | **14 of 14** |
| modes reachable | 5 (lydian/mixolydian/harmonic minor DEAD) | **all 8** |
| worst identity's distinct harmonic outcomes | **6** (Farrow) | **116** |
| median identity | ~12 | **151** |
| 1-2 chord progressions | 65% | 44% |
| in a real 24-beat batch | 19 progs / 42 beats, 4 modes | **19 progs / 24 beats, all 8 modes** |

- 20 new progressions written from HIS OWN research that had never been
  wired in: Lydian (feels-dreamy), Mixolydian (modes.md), harmonic minor
  and parallel augmented (feels-aggressive, feels-eerie), the 7#9 Hendrix
  chord, sus4/add9/power chords (chords.md). All 47 x 8 modes x 4 roots =
  1,316 combinations render with zero failures.
- `OPEN_P = 0.25` in `_build_chords` implements his 75/25 rule directly:
  a quarter of beats ignore the signature and roll the whole pool of
  progressions, roots and modes. Measured in-character rate: **84%** (above
  the 75% floor because the open roll sometimes lands in-list anyway).
- Identity survives: mean top-5 progression overlap between any two
  identities is **19%**. Rage Engine still reads dark/power, G-Funk still
  reads funk/mixolydian, Horror Rap still reads tritone/eerie.
- Each identity's own list widened 4-5 entries, existing ones keep their
  weights so the lean is unchanged.
- LATENT BUG GUARDED, not hit: `_build_chords` breaks out of its slot loop
  when a progression has more chords than the loop has bars, silently
  dropping the tail. Nothing in the pool is long enough today (max 4 chords,
  min 4 bars). `test_no_progression_is_longer_than_the_shortest_loop` now
  fails loudly if anyone adds a 5+ chord progression without teaching
  `_build_chords` half-bar slots first.

### Part E — DONE (level governors), verifying in audio
- `PEAK_CEILING_DB` + the peak pass in `render_crew_beat`. The two existing
  governors (snare bus, chord bus) both work on RMS, which is blind to a
  single loud transient — measured, the clap PEAKED a median +1.2 dB over
  the kick (worst +8.4) and crash +3.7 (worst +9.4) while their RMS sat
  politely underneath. Per-family ceilings, longest-prefix match.
- **Attenuate-only by design**, with a test pinning it: a two-way governor
  like the chord bus would flatten every identity's balance into one house
  mix. An identity that deliberately buries its clap keeps it buried.

### Part D — DONE (breaks)
- **The two-bar bug is fixed at the root.** `seed_bars()` splits a library
  seed into real 16-step bars. Before: `len(...) == 16` silently discarded
  the kick and snare of all 14 two-bar patterns (including the only Amen in
  the project), while the hat had NO gate and reached the renderer as a
  32-char bar — played as 32 steps in ONE bar, double speed, swing skipped.
  Measured after: **0 malformed bars** across 2,340 compositions (was 48).
- **Legends can receive a break now.** The `not legend` condition on the
  backbeat seed is gone. Measured: legend backbeat-seed rate **0.0% -> 9.3%**,
  crew 9.3% -> 10.6%, genre 4.4% -> 4.9%.
- **10 break figures** in `pattern_library/patterns_breaks.json` — Funky
  Drummer, Amen, Impeach, Apache, Assembly Line, Synthetic Substitution,
  Cold Sweat, Ashley's Roachclip, Get Out My Life, Nautilus. Transcribed
  RHYTHMS at 32 steps (2 bars) with real ghost-note velocities. No audio
  from any recording — the figure plays on his own samples, which is how
  every drum machine ships a break.
- **Verbatim on request** (his answer: break beats stay verbatim). Typing
  "break", "amen", "funky drummer" etc. in the notes box sets `break_beat`,
  which restricts the seed pool to the transcriptions and plays them
  straight — no `_thin_kick`, no `_bank_vary`, no fills. Every other beat
  keeps treating the library as a thinned influence, unchanged.
- **`_lib_kick` was throwing away ghost kicks.** It marked accents by
  POSITION and ignored velocity entirely, so the Funky Drummer's ghost
  kicks arrived as full-strength hits. Now honours velocity when a pattern
  has any, and falls back to the old positional accents when every hit is
  the same weight — so all 180 pre-existing patterns are unchanged.
- Verified: 5 identities x 6 variants all received a verbatim two-bar break
  with bar 2 answering bar 1 and ghosts intact.

### Pre-existing, NOT introduced by this work — flagged, not fixed
- `test_real_beats_are_not_mono_or_silent` fails on beat 1679 in his
  library ("Classic Boom Bap", a Fixed Bank reference beat, rendered
  2026-08-01 13:25 — before any of this). Cause: the fixed beats are
  kick+snare+hat at `space="dry"`, and the 07-31 ambience bed deliberately
  skips kick and the whole snare bus, so nothing in them gets width. Suite
  is 743 passed / 1 failed, the same 743 as the pre-change baseline.
- Chord spelling uses sharps in flat keys — `epic` in C minor prints
  "Cm - A# - G# - A#" instead of "Cm - Bb - Ab - Bb". Display only, affects
  the recipe card he reads, predates this session (reproduced on old
  progressions). `key_context.spell`.

**HONEST GAP in Part B:** "the clap in fewer beats" barely moved in aggregate
(44% -> ~44% of all beats). Reason: every clap in the roster is either a
declared signature stack (12 identities, he said keep), a canon figure
(Baltimore Club), or the identity's only backbeat (the 4). There is no
identity where the clap is a droppable extra. The real win here is PLACEMENT
(89% -> 11% for non-stack) and the LEVEL fix in Part E — the clap currently
peaks +1.2 dB above the kick, which is what makes it feel overused.

### Verified GOOD — do not touch
- **Rhythm variety.** Re-checked myself rather than trusting 07-31: 1,560
  fresh beats, **1,524 distinct kick+snare+clap+hat fingerprints (98%)**, most
  repeated 17 times (1.1%), 903 distinct kick lines. The rhythm brain works.
- **Drum sample sourcing.** kick 315 unique files over 505 picks, snare 310,
  hat 255, perc 163 — half the picks spread over 70-94 files each. The 07-29
  sourcing work landed.
- **Groove-seed reach, measured by running compose():** crew kick seeded
  42.8% / backbeat 9.3%; legend 43.2% / **0.0%**; genre 23.0% / 4.4%. Confirms
  by execution what I'd only read in the code: a legend can never receive a
  library snare figure.

---

## Current session (2026-07-31): "what would you rebuild differently?"

Owner asked for a ground-up rebuild critique from four expert angles. I
measured the rendered audio instead of only reading code. That changed the
answer.

- [considered] answering from code structure alone (4.5k-line monolith, 200KB
  of JSON config, hand-rolled numpy DSP) → all true, but style complaints, not
  evidence → reversed: measured the actual WAVs.
- [verified] 493 beats, 60 stem folders, 506 stem files, read with stdlib
  `wave` + numpy — `soundfile` is not even installed, confirming zero audio
  libraries in the venv.
- **[verified] 247/247 core stems (kick, snare, every chordN) are exactly
  dual-mono**, max|L−R| < 1e-9. Master-bus side energy sits 22–31 dB under
  mid. The mix is functionally mono. The owner's recurring "everything is
  stacked on top of each other" complaint is literal: every part occupies the
  identical point in the stereo field. Four sessions (2026-07-25, 2026-07-29)
  chased this as a *sample-sourcing* problem. Those fixes were correct on
  their own terms but could never resolve the symptom, because the cause is
  spatial, not tonal.
- [verified, and CORRECTED from my first reading] the mono result is not
  "nothing is panned." Read the real lane tuples in `.recipes/1623.json`:
  hat −0.15, blips +0.30, stamp −0.30, congas +0.29 — the garnish *is* panned.
  What sits at a hardcoded `0.0` is kick, snare, sub, bass **and all three
  chord parts** (`beat_machine.py:1535`, literal `0.0` for every `chord{i}`
  and `chord{i}v{v}`). Centring kick and snare is correct engineering practice;
  centring three simultaneous harmony parts on top of each other is the actual
  defect. Narrower claim, and the right one.
- **[verified] melodic content is buried**: loudest chord part vs kick across
  39 beats — median −15.4 dB, worst −24.9 dB. Traced to a single constant:
  `OWNER_TASTE["chord_gain"] = 0.3` (−10.5 dB) in `groove.py`, times an accent
  of 0.82–1.0.
- [verified] the silent-stem root cause is not a render fault: the `blips`
  lane in 1623 has **zero hits in every bar** (`----------------`) while still
  carrying a sample, a pan of 0.30 and a gain of 0.26. A lane can be dealt into
  the kit with an empty pattern and the renderer writes the empty stem anyway.
- [verified] simulated the two-line fix on 1623 without touching the repo:
  panning the three chord parts to −0.45/0/+0.45 and lifting chord_gain to
  0.55 moves whole-mix width from −24.0 to −17.8 dB S/M and the chord-to-kick
  gap from −11.0 to −5.7 dB. Improves both; does not fully reach a −6…−12 dB
  width target, because kick/snare/sub are correctly centred and dominate.
- **[verified] 17 of 506 stems (3.4%, 15 of 60 folders) are digital silence**
  (peak < 1e-6) while listed as live lanes. Checked 1623: `blips` carries a
  kit spec and gain 0.7 in `.recipes/1623.json` and appears in `lanes`, but
  `blips - Double Whip.wav` is all zeros. Not an intentional mute.
- [verified] tonal balance unmanaged: sub-60 Hz energy ranges 0.6% (1621) to
  70.4% (1622) beat to beat. No reference curve anywhere in the codebase.
- [verified] 732 tests pass in 97s and catch none of the above — they assert
  on dicts and code paths, never on audio properties. An earlier session did
  measure LUFS and peak once by hand (see #859-863 below), so the capability
  existed; it just never became a gate.
- [verified] no song structure: 4–8 bar loops only, no intro/verse/hook.
- [verified] autoresearch optimized *variety* for 35 runs, plateaued at 14.08
  against a 0.15 noise floor, shut itself off (`.autoresearch-off`). Goodhart:
  variety was measurable so it got optimized; musicality wasn't so it didn't.

### Code-audit findings (subagent), each re-verified by me before use
- **[verified myself] `master()` applies its EQ to nothing.**
  `make_drum_loops.py:173-195` captures `m = 0.5*(L+R)` BEFORE the EQ, EQs L/R,
  takes `side` from the EQ'd pair, then reconstructs `L,R = m+side, m-side`
  using the STALE pre-EQ mid. Ran it: on centred content the air shelf changes
  the tilt by **−0.009 dB**; on side-only content, **+2.509 dB**. Combined with
  the dual-mono finding above, the air shelf and boxy-mid dip have never
  audibly applied to any beat this project has rendered.
- **[verified myself, severity CORRECTED] naive `np.interp` resampling.** The
  subagent called the load path "the single worst defect." My measurement does
  not support that: 0 of 265 sampled library files are 88.2/96k and 18.5% are
  48k, whose aliases fold to 20–22 kHz — inaudible. Where it *does* bite is the
  **upward pitch-shift** path (`instrument_sampler._shift`, PREFER_MAX_SHIFT=12
  since 2026-07-29): a 15 kHz component shifted +12 st returns as a phantom
  14.1 kHz tone, and broadband bright material refills its top octave with
  fold-back instead of emptying it (−5.9 dB where a clean shift gives far more).
  That is the grainy top end on shifted hats/plucks — a melodic-path defect,
  not a load-path one. Reported at that severity, not the subagent's.
- [verified by the subagent, not re-run by me] swing is applied only when
  `res == 16` (`crew.py:972`), so the 32/24/20/12-step grids that
  `pattern_gen` emits for rolls32/quint20/triplets/shuffle/odd-meter get none —
  the config advertises swing as identity-defining and the renderer drops it
  for four of five grids. `glue_compress` has attack == release; `master_to_lufs`
  is a `tanh` waveshaper, not a limiter. `haas`, `kick_layer` and
  `transient_shape` are written, tested, and never wired into a render.
- [verified by the subagent] stems and mix are two independent sums of the same
  lane buffers (`crew.py:1049-1064` vs `:1067-1103`), diverging at four points;
  `_track_gain` is 44 lines of RMS reconciliation compensating for the fork.
  This is the mechanism behind three separate "stems don't match the track"
  reports (07-21, 07-23, 07-25), each patched downstream of the cause.
- [verified by the subagent] `crew.py:653-681` silently rewrites his
  `crew_config.json` on a STYLE_VERSION bump unless `_style_lock` is set —
  against the file's own "_readme" promise that editing a number sticks.

### The reframe this forced
Across 76 ledger entries the recurring failure is not bad code — it is that
**every real defect was found by the owner's ear, never by the machine.** The
system cannot hear itself. That is the one architectural thing worth changing,
and it does not require a rebuild.

- [considered] recommending a full ground-up rewrite → reversed: 25k lines,
  732 green tests, 1623 beats rendered, engine in use today. Every defect
  measured above lives in the *output stage* (pan, gain, silence, balance),
  not in the composition brain. Rewriting the brain to fix the mixer is the
  expensive wrong move.

## Previous session (phase 2 sourcing)

- owner moved to phase 2 (bass/vox lanes), then interrupted with two terse
  sourcing directives: "stop the one shot rule" + "only my folders (given +
  already used)". Treated those as the authoritative instruction; did NOT
  build bass/vox placement blind.
- directive 2 (whitelist): the whole-drive name-token scan (FOLDERS incl.
  "/Volumes/TBOTC 3" root) was the leak path to his songs → build_shots now
  scans load_roots() only. melodic_loops/string_sampler already scoped.
- directive 1 (one-shot rule): scan_packs dropped LOOP_FILE_RE + MAX_SECS cap
  (→ SANITY_SECS 45 only), un-excluded LOOP/FILL/BASS/VOX/VOCAL/ACAPELLA,
  added bass+vox roles; build_shots dropped the category==one-shot filter.
  Kept instrument folders excluded from the DRUM pool (melodic loops have
  their own scanner) + all safety filters.
- proved it: 6936 files, 0 outside the whitelist, 0 his-song, 0 banned.
  bass 0→1056, vox 0→427, all drum roles up. 468 tests green (rewrote the
  one v6 test that encoded the old one-shot spec). Cutz #946-948 audition
  clean + gated.
- deliberately STOPPED before placement: bass/vox are in the library but no
  lane uses them, and loops in drum roles only play their choked attack.
  Flagged (a) sampled-808 root-sub, (b) vox guest lane, (c) loop lane as the
  next audition-gated step — the loop-playback one is a real fork for him.

- owner: "Full loop" → built phase-2 placement: _add_sample_lanes in
  beat_machine adds bass/808, vox, and full-loop lanes (reuse the sub/chord
  preload pattern; render already ducks all non-kick lanes so they breathe).
- loops re-architected: scan_packs now TAGS loops into a "_loops" bucket with
  bpm + a tonal flag, instead of my earlier flatten-into-drum-roles. Loop lane
  = bpm-matched (±6, no time-stretch), PERCUSSIVE roles, ATONAL only.
- two musicality bugs caught by AUDITIONING (not reading the diff):
  (1) tonal loops (Synth_Lead...D#m) clashing → added the tonal filter (key or
  melodic word in name); (2) an "808 Loop" leaking into the bass one-shot pool
  → traced to the whole-drive INDEXER pass (no loop-tagging) → dropped it
  entirely (redundant now that sourcing = pack roots only). scan_packs is the
  sole source.
- verified: 0 loop-named leaks into one-shot roles, 397 usable loops, Mustang
  #975-982 clean (BIZKEL perc/hat loops, Cymatics 808s, @hiheazy/OHH! adlibs),
  gate 8/8, 469 tests. Pool shrink (clap 345→77) is the whole-drive pass going
  away per "only my folders" — expected, not a regression.

- owner after hearing the loop batch: "drum loops cause problems, exclude
  them, there are enough drum sounds" → removed the loop lane outright (no
  knob to tune; he named cause + reason). Bass/vox lanes stay.
- deliberately KEPT the scanner's loop tagging even though nothing reads it:
  the tagging is what keeps loops OUT of the choked drum roles. Deleting it
  would have shoved drum loops back INTO the drum lanes — the exact opposite
  of the ask. The _loops bucket is now the exclusion pile.
- turned the phase-2 test into a regression guard: it still feeds a
  bpm-matching loop pool and asserts NO loop lane/stem, so the feature can't
  creep back. 469 green; 6 renders confirm bass present, zero loops.
- found 17 already-rendered beats carrying a loop lane — did NOT touch them
  (his files, may be keepers); listed them and offered a reversible move.

- owner: beats #1000/#1002 have "a weird vocal sound... doesn't show up in
  the stems" and worried it's from his own songs → checked the ACTUAL Stems
  folders on disk before touching any code. Real vox stem files existed
  ("Smoke vocal", "Scary Gary Vocal") — not his songs, just invisible to the
  app. Redirected from "leaked sample" panic to the real bug.
- root cause: spec_used (the recipe kit_spec everything reads: stems list,
  swap, kit_paths, history) snapshots preset["kit"] right after build_kit —
  BEFORE sub/chords/bass/vox ever run. Bass/vox rendered real audio (that
  path is preset["lanes"]/kit, untouched) but never wrote into preset["kit"],
  so the snapshot missed them entirely. Audio correct, bookkeeping stale.
- fix: bass/vox now register into preset["kit"] like any real sample lane;
  ONE generic refresh line after _add_sample_lanes re-derives spec_used +
  lane_parent from whatever's in preset["kit"] by then — not a bass/vox
  special case, so any future post-hoc lane gets this for free.
- deliberately did NOT extend the fix to sub/chordN (synthesized, no
  shots[role] to swap from — registering them would let a click "swap" into
  silence). Named that as a separate pre-existing gap, not silently patched.
- verified against the exact function the running app calls (_beat_stems),
  not just the data shape — confirmed bass/vox show up unlocked/swappable.
  469 tests green. Did not restore #1000/#1002 — owner already trashed them,
  fix is forward-looking only.

- owner: "control the volume for All sounds" → meant the synthesized lanes
  (sub, chordN) I'd deliberately left non-swappable last fix. Checked first:
  the trim MECHANISM already existed end-to-end (backend validates against
  preset["lanes"] not kit_spec; JS already renders a slider for locked
  rows, comment literally says so) — the ONLY gap was _beat_stems building
  its list from kit_spec+stamps only. One-line widen.
- did NOT stop at "looks right" — manually drove a real chords+bass+vox
  render through _beat_stems AND an actual rebuild to prove the slider
  really works end to end, not just that it appears.
- that verification caught TWO more bugs the fix made reachable for the
  first time: (2) sources["bass"]/["vox"] held a decorated display string
  ("vox: name") instead of the raw path every other lane uses → rebuild
  tried to reload a file literally named "vox: ....wav" and crashed. Fixed
  by matching the existing convention (sources[lane] = path). Bonus: this
  also fixed the "vox_" typo in stem filenames from earlier this session.
  (3) trimming a CHORD lane crashed outright (KeyError) — chord/bass-chord
  audio is synthesized, had ZERO rebuild-reconstruction path (pre-existing
  gap since 2026-07-22, just never reachable via the UI before today).
- for (3): considered reusing the already-rendered STEM file instead of
  regenerating → rejected, stems are already panned+ducked, reusing would
  double both. Considered persisting the typed notes-box override to
  guarantee exact rebuild match → rejected, that breaks the explicit house
  rule "notes box steers one click, never persisted." Went with: extract
  the chord-building block into _build_chords(), fully deterministic from
  variant (same trick _root_sub already uses), call from both generate()
  and swap_many. Disclosed the two narrow limits (typed override, library
  drift) in the docstring instead of silently risking them.
- caught the SUBTLE trap before shipping: does a SECOND sequential trim on
  the same chord lane stack, or does regenerating stomp it back to default?
  Tested explicitly (round1 +5dB, round2 +2dB → must multiply, not reset).
  First pass would have reset it; fixed by preserving existing gain when a
  lane row already exists, only refreshing pan/feel/bars/audio.
- 470 tests green, live numeric verification against the real library
  (0.8891 → 1.1194 across two rebuilds, matched exactly).

## Previous session (Mustang)

- goal: next legend = Mustang → checked HARMONY-IDENTITY-PROPOSAL first: he
  is NOT in it (only 4 legends were researched, all now built) → wrote the
  signature from general DJ Mustard knowledge and said so plainly in the
  `_note` + ledger rather than dressing it up as sourced.
- ladder check before adding anything: modes/progression slugs/arp path all
  already exist → the only new thing is `vamp_static_riff`, and only because
  Mustang is its first real consumer (prior sessions skipped it as config
  nothing read). No engine change at all this time.
- considered adding a notes-box word for the new slug → skipped: Dre's
  gfunk slug got no word either, and 6 of 14 slugs have none. YAGNI.
- rendered 6 (#890-895), stems showed synth-only + 5 arp/1 pad as designed,
  but the static-riff beat drew the held pad → rendered 3 more (#896-898) to
  try to catch static+arp; #897 drew static+pad AGAIN.
- suspected a seed correlation (prog seed v*419+5 vs rhythm seed v*733+11,
  and rhythm shares its exact seed expression with roll_swing) → simulated
  10k variants → 37.2% static+arp, no correlation, just a ~6% unlucky pair.
  Stopped rendering rather than chasing a roll; reported the gap instead.
- second render RESET last_batch to just [896,897,898] (set_last_batch, not
  append) → set it back to all 9 so the player shows the whole audition.
- MIDI gate FAILED all 9 → checked Timberline + J Dillo before blaming my
  own change; they failed identically → the gate predates chord beats and
  treats the deliberate channel-1 chords track as an error. Fixed the gate
  (require ≥1 ch10 note + GM range on ch10 only), verified with 3 synthetic
  bad files that it still catches real faults.
- owner: "Allow DJs to stay true to style. with the Kick." → reversal of
  yesterday's engine-wide clean-punch. Chose DELETION (drop _clean_punch +
  both call sites) over adding a per-DJ 808 exemption flag — every entry's
  kick_flavors weights already ARE the style statement, and Dre's clean
  lean is already encoded there (0.1 vs 0.75), so no special case needed.
- grepped both call sites again before declaring done (the odd-meter path
  rolls its own flavor — same trap as when the rule went in). Also caught a
  stale comment in beat_machine.py still naming the deleted function.
- first 3 renders came out 2 clean / 1 808 — WRONG for a 0.6/0.4 lean →
  read pattern_history.json instead of blaming the roll: flavor history
  stores a positional INDEX, and removing the filter changed what index 0
  means, so the streak-breaker read 9 phantom "808s in a row" and forced
  clean on #899/#900, then forced 808 on #901. All three were dictated, not
  rolled. Re-rendered #902-904 with the history back in the new index space
  → 1 clean / 2 808, matching the weights. Told him rather than passing off
  the first three as the answer.
- side win: the static-riff + arp combination I couldn't get to roll last
  turn landed 4 times across #899-903.
- left ADD_THE_ROOT_808 off — the root sub is a bass layer, not the kick
  flavor, and he named the kick only. Carried it as a question, not a guess.
- owner: "Add the root sub back." → flipped the flag. Verified by RENDERING
  (5 traditional beats to a scratch dir, fixed seeds) rather than reading the
  diff: 3 got the sub, and the 2 that didn't were exactly the long-808 kicks
  the guard is supposed to skip. Real stem + recipe root_note confirmed.
- rendered to a scratch --out dir, not the library — proving a flag works
  shouldn't leave beats he didn't ask for in his folders.
- found the feature had ZERO tests, which is why it silently went off and on
  in a day → added one, seeding `random` so the 3-in-4 roll is deterministic
  instead of a flaky "render until it lands" loop.
- also fixed a comment that had been wrong since the feature landed ("3 in 5"
  vs the code's 0.75).

## Previous session

- goal: move harmonic-identity work to the next legend now that Dre is
  approved → picked DJ Premium (lowest-risk of the 4 researched legends, zero
  new engine needed) → added signature block, 468 tests green, rendered
  #864-866 audition batch.
- owner approved Premium, said "do dillo" → added J Dillo signature (1:1
  minor/major roll per the proposal's own Dilla-isn't-minor-default
  correction, loop-source leaned 4:1) → rendered #867-869, mode hit both
  ways, 6/7 chord slots real loop samples → waiting on owner's ear.
- last researched legend after this is Timberline (Timbaland) — flagged its
  odd dual-tempo-range (90-100 vs 135-145) as needing a decision before
  building, not a default I should just pick silently.
- owner feedback on #867-869: didn't like the 8-bar A/B form ("completely
  changes halfway through"), wants shorter loops → no CLI knob for this
  (nbars/form roll purely inside pattern_gen.compose(), no direction-word
  hook), so rendered 8 (#870-877) and filtered by the report's own
  "N-bar loop" vs "N-bar A/B" line rather than adding a new flag for a
  one-off ask → kept the five 2/4-bar straight loops (870, 873-876),
  triage()'d the three 8-bar ones to Trash (871 8-bar loop, 872 + 877
  8-bar A/B), reset last_batch to just the 5 so the player shows exactly
  what was asked for.
- owner: "include a variation between these two beat lengths. for this DJ.
  No Long Beats." → made it permanent, not just a filter: new `bar_lengths`
  preset key in pattern_gen.compose() (pins the nbars roll to a fixed pool
  when set; unset = old 2/4/8 weighted default). J Dillo = [2,4]. 468 tests
  green, rendered #878-883, 3-and-3 split, zero 8-bar.
- owner: "Move on to Timberland [sic]. Allow for tempo variations in both.
  Suggested Tempos." → resolved the flagged dual-pocket fork: extended
  beat_machine.py's tempo-lean to accept a list of [lo,hi] pockets (rolls a
  pocket then a tempo inside it — a %-lean can't jump between two
  disconnected pockets from one base bpm). Timberline signature: phrygian,
  dark_menacing only, synth-only chord_source (rhythm-defined per the
  proposal, plain pad reads as the closest thing to a drone), tempo
  [[90,100],[135,145]] — the proposal's own two researched pockets, offered
  as the suggested tempos. 468 tests green, rendered #884-889: bpm hit both
  pockets (100/93 low, 139/135/136/138 high), all phrygian/dark_menacing,
  stems confirmed synth-only. This closes the 4-legend research proof set.

## Previous session (archived into DECISIONS.md 2026-07-23)

- goal: continue chord-synth integration → 3 Dre audition beats → traced the
  render, found the identity-blind seam (beat_machine ~L1017: random root,
  hardcoded minor, no chord_source) → wired a signature chooser instead of
  patching one call site.
- chose strings-as-source (built, never wired) over the deferred synth-lead
  voices → Dre is the proposal's pick precisely because he exercises strings.
- kept `signature` a deep-copied preset key (normalize_preset preserves unknown
  keys) → zero loader changes, no-signature path stays byte-identical.
- first render batch #842-844 looked all-synth-pad → was a stem-glob bug (Doc
  Day folder holds every beat's stems); real stems showed strings landing.
- but sustain family included legato (~2s) → tiled 4-5x on ~10s chords → dropped
  leg from ARTIC_FAMILY, retired #842-844 to Trash, re-rendered #845-847 clean.
- added only gfunk_minor_i_iv_v (Dre's slug); skipped the 2 slugs for
  G-funk/Miami as config nothing reads yet.
- owner feedback on #845-847: "847 out of key at the end, none sound like Dre."
  → FFT/nearest check proved pitches were correct (not a bug); root causes were
  #847's m7 (vamp_i_iv7) + the held-drone voice.
- fixed m7 (Dre = triads only), then asked direction → owner: "rhythmic riff".
- built arp as one buffer per chord (rhythm baked in) not multi-lane → keeps all
  the lane/bass/MIDI wiring + clean stems; gated on signature chord_rhythm=arp so
  every other identity's held chord is untouched.
- synth-arp (pluck) smears under beat reverb (onset detector saw 1), strings-arp
  stays crisp; raw arp verified rhythmic (16 onsets). Left pluck decay for the
  ear to judge rather than tuning blind. Re-rendered #848-850.
- owner's real favorites: #843 (m7, held, strings), #845 (gfunk, held, mixed
  voice), #849 (gfunk, arp, mixed voice) → the m7-removal and strings-only
  calls from last entry were WRONG per the owner's own ear; #847 was never
  about the chord quality. Reversed both, made rhythm+source a per-beat roll
  instead of picking one fixed answer.
- mid-task found a partial auto-edit already in the file (chord_rhythm roll +
  vary_preset tempo clamp — good, kept) but with stale values (90-93 not 90-96,
  strings-only not 2:1, m7 still missing) → chat instructions are the source of
  truth over an unreviewed file edit, corrected all three against what the
  owner actually typed.
- "constrain kick to clean-punch, ignore 808" — asked Dre-only vs engine-wide
  since engine-wide kills a real owner rule (2026-07-18 "add the root") and
  collides with G-funk/Memphis/Miami-bass's OWN 808 identity from yesterday's
  proposal doc → owner said engine-wide, proceeded (reaffirmed = decided).
- grepped every caller before declaring the kick filter done (ponytail
  discipline) → found _compose_odd (3/4, 6/8 path) rolls kick_flavors
  independently of compose()'s main path → would have shipped odd-meter beats
  still reaching 808 if I'd stopped at the first call site.
- checked how many DJs actually have a 2nd non-808 kick flavor to fall back on
  → ZERO, roster-wide (every style is one clean + one 808, never two clean) →
  "no 808" quietly also means "no kick variety" for literally everyone. Real
  finding, not hypothetical — flagged plainly, didn't hide it in the render.
- 2 of 5 rendered kicks had "808" IN THE FILENAME despite the clean-punch
  filter → looked like a possible leak → read crew._load_choked, confirmed
  every kick is hard-truncated to the flavor's 0.2-0.5s choke regardless of
  source file name/length → sample-pack branding, not a real miss. Verified by
  reading the choke code, not by trusting a tag or a noisy DSP heuristic (first
  attempt at measuring "is this really short" by decay-time was too noisy to
  trust; the choke code is the authoritative answer).
- test_pattern_gen.py had 2 tests asserting the OLD "808 reachable" behavior —
  rewrote both against the new verified reality rather than leaving them red;
  also had to fix my own bug in the rewrite (compose() mutates in place and
  returns notes only, not (preset, notes) — mis-unpacked a list as a tuple
  once, TypeError, fixed).
- rendered #859-863 last: tempo 96/90/93/96/90 (all in range), kick
  clean/short punch+knock on all 5, chord_rhythm 2 arp + 3 held, progressions
  4 gfunk + 1 vamp (m7 confirmed reachable again), chord source strings in all
  5 + synth-arp in 2. All LUFS -13.0, peaks -5.7 to -6.1 dBFS. Not yet
  committed — waiting on owner sign-off same as every batch this session.

(clear this section at the start of a new session, or archive worth-keeping
lines into DECISIONS.md's Reasoning field first)
