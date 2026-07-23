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
