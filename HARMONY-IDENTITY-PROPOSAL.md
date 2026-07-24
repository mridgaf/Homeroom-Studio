# Harmony & Instrument Identity — research + proposal (2026-07-22)

*Giving each legend/genre a harmonic + instrument fingerprint, not just a
drum one. Researched for 4 legends + 4 genres as a proof set. Nothing here
is wired yet — this is for approval.*

## The core finding (why this was overlooked)
The roster encodes drums and mix in deep detail, but **zero** notes or
instruments. Verified in code: every "chords" beat — for every legend and
genre — gets a **random root, always minor, random progression**. A Dr. Dre
chord beat and a Memphis chord beat are harmonically identical today. The
harmonizer isn't weak; it's **identity-blind**. Your `theory/progressions.md`
already defines 13 named progressions as data — the fix is a *mapping* from
who-the-beat-is → which of those, which key, which instrument voice. Almost
no new engine.

One correction the research forced: **J Dilla is NOT minor-default.** His
harmony is sample-dictated and skews soul/major as often as minor. So the
schema's mode must be a *weighted* choice, never a hard minor lock.

---

## Proposed `signature=` block (additive, optional)
An entry without it behaves exactly as today. With it, the harmonizer reads
identity. One small chooser function in beat_machine; everything it points at
already exists (progression slugs, string_sampler, chord_synth sources).

```python
signature=dict(
    key=dict(roots=["F","G","C"], mode="minor"),   # mode can be a weighted list
    progressions=[["nostalgic_jazz", 3], ["dreamy", 2]],   # slugs, weighted
    chord_source=[["strings",2], ["loop",2], ["synth",1]], # answers "strings vs loop vs synth"
    articulation="sustain",        # strings only: sustain=bed, pizz=stab
    tempo=(85, 100),               # a RANGE, backfills the single bpm
)
```

**`chord_source` is the answer to your earlier question** — strings vs loop
vs synth is a *per-identity weight*, not a global rule and not a volume thing.

---

## The 8 profiles → proposed signatures

Slugs in **bold** are new (3 total); everything else already exists.

| Roster entry | built on | tempo | mode | progressions | chord_source lean |
|---|---|---|---|---|---|
| **J Dillo** | J Dilla | 70–95 | minor+major (sample) | nostalgic_jazz, dreamy, vamp_ii_V | **loop** (Rhodes/soul) |
| **DJ Premium** | DJ Premier | 82–96 | minor/dorian | vamp_i_iv7, vamp_i_VI, dark_menacing | **loop** (dark stab) |
| **Doc Day** | Dr. Dre | 85–100 | minor | **`gfunk_minor_i_iv_v`**, vamp_i_iv7 | **strings**+synth |
| **Timberline** | Timbaland | 90–100 / 135–145 | phrygian | dark_menacing | minimal / drone |
| **Memphis** | Three 6 | 140 (¾-time feel) | minor/phrygian | dark_menacing, vamp_i_VI | synth (horror) / pitched-808 |
| **G-Funk** | Quik/Warren G | 85–105 | dorian/minor | **`vamp_i_IV9`**, vamp_i_VI, nostalgic_jazz | synth-lead + loop |
| **Miami Bass** | 2 Live Crew | 118–140 | minor pentatonic | **`vamp_static_riff`**, vamp_i_VI | minimal (808 riff) |
| **Reggaeton Alt** | dembow | 85–100 | minor/phrygian | sad_accepting, dark_menacing | synth stab / marimba / loop |

### The giveaways (what each MUST sound like)
- **Dilla** — lush maj7/9 Rhodes/soul loop + drunk *quantize-off* swing. MPC3000.
- **Premier** — sparse minor stab + hard dry on-grid knock + **scratched vocal hooks**. MPC60→S950.
- **Dre** — slow minor `i–iv–v` on live Rhodes/**strings** + fat rolling 808 + one nasal portamento saw lead / talkbox. Clean, spacious, expensive.
- **Timbaland** — stuttering off-grid drums + vocal-percussion/breaths over a single droning **Phrygian (b2)** melody. Almost no chord movement.
- **Memphis** — dragging half-time drenched in tape hiss + detuned horror-organ over a Phrygian minor drone + pitched-808 sub melody. (bpm stays 140 = double-time count; the ¾-time *feel* is already the `halftime` snare mode.)
- **G-funk** — high gliding **portamento saw whistle** over a slow ~92 Dorian groove, fat Moog bass, talkbox. Warm, sunny — opposite of Memphis.
- **Miami bass** — long, pitched, wobbling **808 kick playing a bassline** + doubled snare+clap on 2 & 4 at ~130. Rhythm, not chords.
- **Reggaeton** — the **dembow** itself: boom-ch-boom-chick with rimshot accents on the "e" of 2 and 4 (steps 7 & 15) at ~95.

### 3 new progression slugs to add to progressions_config.json
- `gfunk_minor_i_iv_v` = i–iv–v, all minor triads (Still D.R.E. = Fm–Bbm–Cm).
- `vamp_i_IV9` = Dorian i9–IV9, the bright-4 G-funk vamp (Am9–D9).
- `vamp_static_riff` = single-root minor drone; the tuned-808/bass carries the melody (Miami bass, also fits Timbaland/Memphis drones).

---

## What this proposal deliberately does NOT cover (honest scope)
Two of the eight identities are **rhythm-defined, not harmony-defined**
(Miami bass = tuned-808 pattern; reggaeton = dembow; Timbaland = stutter).
Their fingerprint lives in the **existing grammar/kick/swing fields**, not
this harmony block. The research handed us exact patterns (e.g. reggaeton
snare on steps 7 & 15). **Follow-on #1:** audit whether the current grammar
already reproduces those, or needs a canonical pattern pinned.

Several signature **lead voices** — G-funk portamento saw, Dre talkbox,
Memphis horror-organ, Timbaland vocal-perc — need a **synth-lead generator
that doesn't exist yet**. `chord_source: synth` today means the soft pad, not
these. **Follow-on #2:** a lead-voice synth is the next instrument build
after chords, and it's what truly nails G-funk/Dre/Memphis.

---

## Recommended first step (reversible, audition-gated)
1. Add the 3 new slugs to `progressions_config.json` (pure data, no risk).
2. Add `signature=` to **Doc Day (Dre)** first — it's the one that exercises
   the whole chain: new slug + strings chord_source + articulation. It's also
   the best test of the strings instrument in a real identity.
3. Render a small audition batch (Dre with chords) into the library; you
   listen; we keep or tune. Then roll the pattern to the other 7.

This keeps the audition-before-live discipline: the live roster never moves
until your ears approve a batch.

---

## Addendum v2 (2026-07-23) — remaining 8 legends researched, deep pass

Same honest-sourcing rules as above: research-only, nothing wired into
`legends_config.json` yet. **This closes all 12 of 12 roster legends** —
Doc Day, J Dillo, DJ Premium, Timberline from the original proposal; the
other 8 below. (Mustang's signature was added directly from general
knowledge, flagged honestly in `legends_config.json` itself as NOT covered
by this research effort — it stays that way unless you want it redone too.)

The first pass on Farrow/Kane East/Razor/No Alias was too shallow (single
prompt, ~400 words, no source verification) and has been **replaced
entirely** by a deeper redo below — multi-era cross-checks, explicit
contrasts against neighboring legends, and (for Kane East/No Alias/Just
Flame) live web search verifying actual BPM/key/sample data rather than
recall alone. Swish Beatz, Just Flame, and Hitt Kid are new, done at the
same depth from the start.

| Roster entry | built on | tempo | mode | progressions | chord_source lean |
|---|---|---|---|---|---|
| **Farrow** | Pharrell/Neptunes | 95–115 (classic-minimal) / 100–160 (later pop/N.E.R.D) — genuinely bimodal | near-atonal/no clear mode (classic) → major/diatonic (later pop) | **vamp_static_riff** (classic), uplifting + vamp_i_iv7 (later) | **synth** (stab/pluck) both eras, dominant |
| **Kane East** | Kanye West | 83–97 (soul-chop) / 85–145 (orchestral, wide) — really 4-5 eras, collapsed to 2 for engine limits | major/minor sample-dictated (soul) ↔ minor/dramatic (orchestral) | nostalgic_jazz+nostalgic_borrowed_minor (soul) / epic+uplifting (orch.) | **loop** (soul) / **strings** as sustained choir-bed, not stab (orch.) |
| **Razor** | RZA | 80–96 | minor, sample-inherited short vamp cells that don't develop; "out-of-tune" is artifact-origin, aesthetically retained not composed | vamp_static_riff (dom.), dark_menacing (secondary) | **loop**, ~90%+, least-edited/longest cells on the roster |
| **No Alias** | No I.D. | 85–96, with a 172/half-time-86 outlier (D.O.A.) | major on soul-showcase records (verified C# major x2), minor on the tougher flex singles — purpose-tied, not random; single signature, no `alt` needed | nostalgic_jazz (dom.), vamp_i_iv7, dark_menacing (harder lane) | **loop**, high confidence, cleanest/best-mastered loop-user on the roster |
| **Swish Beatz** | Swizz Beatz | 90–105, narrow band, consistent across 20+ years | minor-dominant, low modal variance — "triumphant" comes from stab loudness/density, not major key | vamp_static_riff (dom.), trap_dark_metro, dark_menacing | **synth**, horn/brass-stab timbre — high confidence |
| **Just Flame** | Just Blaze | 82–110 half-time-felt (raw grid runs to 155–178) | major-lean but genuinely bimodal per-song (not per-era) — PSA major, U Don't Know minor, same album cycle | epic + uplifting (major lane), dark_menacing + vamp_i_iv7 (minor lane) | **strings** — but means horn/brass stack, NOT string pads (schema note) |
| **Hitt Kid** | Hit-Boy | 130–145 (club/trap era, 2011-15) / 85–105 (King's Disease era, 2020+) — hard pivot, not gradual drift | minor/thin-harmony (club era) → warmer soul-major-leaning, weighted not locked (King's Disease) | vamp_static_riff + trap_dark_metro (club) / nostalgic_jazz + vamp_i_iv7 + sad_accepting (KD) | **synth** stab (club) / **loop**, sustain (KD) — near-total inversion between eras |
| Mustang | DJ Mustard | *(unchanged — general-knowledge signature already in config, not part of this research pass)* | | | |

### The giveaways
- **Farrow** — huge dry silence between hits, one repeating synth stab doing double duty as riff and rhythm section (classic era); later solo work trades that silence for full major-key song structure and falsetto as the true hook.
- **Kane East** — a pitched-up soul vocal loops the whole hook over dusty boom-bap and the chords are whatever the record already had (soul mode); a minor-key choir or string swell enters like a film score, turning a verse into an arena moment (orchestral mode).
- **Razor** — a dusty, mildly-detuned soul/piano loop repeats almost unedited under raw, heavy-swing MPC60 drums with no bass EQ cleanup; kung-fu dialogue samples cold-open tracks as a structural device as identifying as the harmony itself.
- **No Alias** — a warm, deep-crate jazz/soul loop, spliced clean rather than chopped hard, under a mid-90s swung boom-bap pocket, confident and unhurried; on the rare harder single (D.O.A.) the same ear goes almost harmony-less and percussive, proving the loop discipline is a choice.
- **Swish Beatz** — a blaring 2–4 note synth-horn stab hammered on a static minor riff, shouted ad-libs baked directly into the beat, a drum pattern simple enough to read as a war chant — energy from loudness and repetition, not chord movement.
- **Just Flame** — a Godzilla-sized, sidechained horn stack detonating under a boom-bap-scaled half-time drum pocket, bigger and more orchestral than a chipped vocal loop; triumphant scale that doesn't require major key (U Don't Know is minor and still enormous).
- **Hitt Kid** — a single blaring synth or pitched vocal-chop stab looping under booming uptempo trap drums, almost no chord changes, all size and impact (club era); a warm soul/funk sample loop under clean, modern, "expensive"-sounding drums at a slower tempo (King's Disease era) — the two eras barely sound like the same producer.

### No new progression slugs needed — for any of the 8
Every legend maps onto existing slugs (`vamp_static_riff`, `vamp_i_iv7`,
`uplifting`, `nostalgic_jazz`, `nostalgic_borrowed_minor`, `epic`,
`dark_menacing`, `sad_accepting`, `trap_dark_metro`). Zero new
`progressions_config.json` entries required across all 12 researched
legends — the 3 slugs added for the first batch (Dre/Dilla/G-funk/Miami
Bass) turned out to cover the entire roster.

### Bimodal calls — CORRECTED 2026-07-23: no `alt` mechanism exists for this
Earlier drafts of this doc (and the research prompts that fed them) assumed
the schema already had an `alt` field for a legend's second harmony mode.
**That was wrong** — checked against the actual code: `preset["alt"]` is the
drum-era alt-snare/reverb mechanism (`crew.py`), completely unrelated to
harmony. There is no engine mechanism today for rolling between two full
harmony modes per beat, and building one wasn't asked for. Rather than add
that machinery speculatively, the four bimodal legends were each wired with
**one mode only** — the dropped mode is a documented, deliberately not-built
follow-on, same honest-scope discipline as the Miami Bass/reggaeton
rhythm-defined gap in the original proposal:
- **Kane East** — wired orchestral/epic (minor, strings sustain,
  epic+uplifting), NOT chipmunk-soul. Reasoning: the soul-chop loop space
  was already crowded (Dilla, No Alias, Razor all loop-dominant); nobody
  else uses `epic`+sustained strings, and `epic` had been sitting unused in
  the vocabulary since the original proposal.
- **Hitt Kid** — wired King's Disease/soulful-sample mode (loop, sustain,
  nostalgic_jazz), NOT the historically-earlier club-trap era, per the
  research's own explicit recommendation (more distinctive, more
  harmonically rich, adds more roster diversity).
- **Farrow** — wired classic-minimal (near-atonal, vamp_static_riff, synth
  stab), NOT the later major/pop era, since it's the more identifiably
  "Neptunes" sound.
- **Just Flame** — genuinely different case: his bimodality is *per-song*,
  not per-era (major/minor split within the same album cycle), so a single
  signature with a WEIGHTED mode list is the right shape — no `alt`-style
  mechanism needed at all, same pattern already used for J Dilla. He's
  still not wired, but for the horn-vs-strings reason below, not this one.
  **No Alias** is per-song too (major on soul-showcase, minor on harder flex
  singles) and is already wired this way.

### Honest caveats carried over from the agents
- **Farrow and Swish Beatz are both synth-forward and would render
  identically today** — chord_source alone can't distinguish them. The real
  difference is synth *timbre class* (pluck/bell vs. horn/brass-stab) and
  arrangement density (huge negative space vs. none) — neither field exists
  yet. This is a genuine schema gap, not a config choice, same category as
  the lead-voice-synth gap already flagged for G-funk/Dre/Memphis.
- **Just Flame's "strings" chord_source means horn/brass stack, not string
  pads** — if the engine's `strings` voice is timbred as literal orchestral
  strings, it will collapse Just Flame into Kane East's orchestral mode,
  which uses real string-section pads. Flagged as the single highest-priority
  schema note from this batch.
- **Razor's detune is now more precisely characterized**: very likely
  artifact-origin (turntable pitch drift, tape wow/flutter, coarse
  early-sampler pitch resolution) rather than a deliberate compositional
  choice from day one — but *aesthetically retained* once better gear was
  available (Wu-Tang Forever, bigger budget, same grime kept). State it as
  "artifact-origin, aesthetically retained," not "intentional pitch
  manipulation."
- **No Alias remains the least differentiated profile even after deeper
  research** — confirmed, not just a shallow-pass artifact. His actual
  signature is *disciplined restraint*: the same warm-loop move recurring
  essentially unchanged from 1994 (Common, "Resurrection") to 2017 (Jay-Z,
  "4:44"), verified via BPM/key/sample data across both. That consistency
  IS the finding.
- **Kane East is more accurately 4-5 eras collapsed to 2 for engine limits**,
  not truly bimodal — the deep pass found chipmunk-soul, orchestral-epic,
  synth-arena (Graduation), minimalist-Auto-Tune (808s), and
  industrial-rupture (Yeezus) as distinct modes, with MBDTF synthesizing
  several at once rather than being a 6th mode. Recommend encoding only the
  two most representative and roster-relevant (soul-chop, orchestral) and
  treating the rest as out of scope, same "honest scope" discipline as the
  Miami Bass/reggaeton rhythm-defined caveat in the original proposal.
- **Hitt Kid's two eras are a hard pivot (~2019-20), not a gradual drift** —
  unlike Kane East's slower evolution, averaging his two eras would produce
  a beat that sounds like neither. Recommend prioritizing King's Disease as
  default per the reasoning above.

### Corrections the research caught along the way
Two claims fed into the research prompts turned out to be wrong and were
caught rather than silently repeated: "Roc Boys (And the Winner Is...)" is
not a Just Blaze production (it's The Hitmen), and "Show Me What You Got"
samples Johnny Pate/Lafayette Afro Rock Band, not Jackson 5 as assumed. Both
excluded from the final signature. A "Baseline — Somebody Told Me" rock-
crossover credit for Just Blaze could not be verified and was flagged as
unconfirmed rather than included.

### Recommended next step
Same audition-before-live discipline as Doc Day's first pass.

- **No Alias** — wired 2026-07-23, audition batch #1028/#1029/#1030,
  **owner said "keep."** Live as-is.
- **Swish Beatz** — wired 2026-07-23, audition batch #1031/#1032/#1033,
  **owner said "keep."** Live as-is.
- **Razor** — wired 2026-07-23, audition batch #1034 "Temple Creed"
  (84bpm, F minor, vamp_static_riff), #1035 "Rusty Fable" (87bpm, D minor,
  vamp_static_riff), #1036 "Iron Scroll" (90bpm, G minor, vamp_static_riff).
- **Farrow** — wired 2026-07-23 (classic-minimal mode, see correction
  above), audition batch #1037 "Tropic Loop" (103bpm), #1038 "Mineral Tilt"
  (95bpm), #1039 "Tropic Wink" (95bpm), all G minor / vamp_static_riff.
- **Kane East** — wired 2026-07-23 (orchestral/epic mode, see correction
  above), audition batch #1040 "Marble Scholar" (93bpm, G minor, epic),
  #1041 "Rose Registry" (94bpm, G minor, epic), #1042 "Marble Applause"
  (93bpm, Bb minor, uplifting).
- **Hitt Kid** — wired 2026-07-23 (King's Disease mode, see correction
  above), audition batch #1043 "Ballroom Verdict" (93bpm, D minor,
  vamp_i_iv7), #1044 "Stacked Summit" (93bpm, C minor, vamp_i_iv7), #1045
  "Stacked Encore" (99bpm, C minor, vamp_i_iv7).

- **Just Flame** — wired 2026-07-23, LAST of the twelve and only after the
  horn engine existed. Audition batch #1046 "Cathedral Salute" (91bpm,
  epic), #1047 "Brass Crescendo" (99bpm, uplifting), #1048 "Royal March"
  (99bpm, epic).

**All 12 legends are now wired.** Everything from Razor onward is
**waiting on your ear.**

### Follow-on #2 (lead voices) is now BUILT — 2026-07-23
The original proposal flagged that several signature lead voices "need a
synth-lead generator that doesn't exist yet." Two engines now exist:
- **`tools/lead_synth.py`** — monophonic lead/brass. Presets: `talkbox`
  (Dre), `gfunk_whistle`, `horror_organ` (Memphis), `horn_stab`,
  `horn_sustain`. Plus `horn_chord()`, the polyphonic stack.
- **`tools/scratch.py`** — a real turntable scratch performance (position +
  fader curves, not a static one-shot). Patterns: baby, chirp, transform,
  scribble. Closes DJ Premium's scratched-hook gap.

Only the horn path is wired into a render so far (Just Flame, via the new
`chord_source: horns`). The talkbox / G-funk whistle / horror-organ presets
and all of `scratch.py` exist and are tested but are **not yet used by any
legend or genre** — wiring them into Doc Day, G-Funk, Memphis, and DJ
Premium is the natural next pass.

### Engine finding: `mode` does less than it looks like it does
Verified 2026-07-23: a signature's `mode` has **no effect on synthesized
chord qualities.** `harmony.compose(C major, epic)` and `(C minor, epic)`
return identical chords, because `progressions_config.json` fixes each
chord's quality absolutely — the key only supplies the root pitch class and
the spelling. `mode` therefore only changes (a) the printed key label and
(b) which melodic loop samples count as in-key. The weighted-mode feature
added for J Dillo does less than its description implies. Practical
symptom: a major-mode signature on a structurally-minor progression prints
a confusing `epic in C major (Cm, A#, G#, A#)`. Cosmetic, and it predates
all of this wiring.
