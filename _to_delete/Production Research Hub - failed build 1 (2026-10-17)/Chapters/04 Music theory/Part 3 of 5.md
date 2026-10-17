# Chapter 04: Music theory
## Part 3 of 5

_Chords, intervals, modes, progressions, keys, tension and release, arrangement, emotion science, and the harmony proposals._

**In this part:**
- research-emotion-science.md — The Science of How Music Elicits Emotion — Producer's Field Guide
- research-emotion-production.md — Production-Level Devices for Eliciting Feelings

(Next: Part 4 of 5)


=====================================================
SOURCE FILE: research-emotion-science.md
ORIGINAL LOCATION: HS:.claude/skills/drum-loops/references/research-emotion-science.md
=====================================================

# The Science of How Music Elicits Emotion — Producer's Field Guide

Audience: self-taught hip hop producer in Reason 12. Every claim is a knob you can turn.
"[weak]" = pop-science / single-source / not tightly quantified. Everything else is peer-reviewed.

---

## 1. Parameter → Emotion Mappings (the core cues)

The most-studied cues, in order of raw power over perceived emotion, come from a controlled
factorial study (Eerola, Friberg & Bresin 2013, *Frontiers in Psychology*, "Emotional expression
in music: contribution, linearity, and additivity of primary musical cues"). They synthesized
melodies varying 6 cues and ran regression. **Cue strength (median semi-partial correlation sr²):**

| Rank | Cue | sr² (share of variance) |
|---|---|---|
| 1 | **Mode** (major/minor) | 0.29 |
| 2 | **Tempo** (fast/slow) | 0.14 |
| 3 | **Register** (high/low pitch) | 0.08 |
| 4 | **Dynamics** (loud/soft) | 0.04 |
| 5 | **Articulation** (staccato/legato) | 0.02 |
| 6 | **Timbre** (bright/dark) | 0.01 |

Takeaway: **mode and tempo do most of the emotional lifting; the rest are fine-tuning.**
The model explained **89% of variance** for both happiness and sadness, effects were **linear and
additive** — no significant interactions. So cues stack predictably: you can dial each independently
and the feelings add up. (Eerola et al. 2013)

### Directional effects, with the numbers (Eerola et al. 2013, β = regression weight)

**MODE** — biggest single lever.
- Major → happy (β = +1.77 for happiness; sr² = 0.48). Minor → sad (β = −1.6 for sadness; sr² = 0.54).
- This is the dominant valence cue (Gabrielsson & Lindström 2001: mode + harmony drive *valence*).

**TEMPO** — biggest *arousal* lever, and it also shifts valence.
- Faster → happier/more excited (β = +0.25 happiness). Slower → sadder (β = −0.32 sadness, sr² = 0.21).
- Tempo governs arousal more than any other single cue (Gabrielsson & Lindström 2001).

**REGISTER / PITCH HEIGHT**
- Higher → happier, brighter, more aroused (β = +0.18 happiness). Lower → sadder, heavier
  (β = −0.05 sadness). High pitch also reads as "more potent/angry" at high arousal.

**LOUDNESS / DYNAMICS**
- Louder → higher arousal, more power/anger/joy; softer → tenderness, sadness, fear.
- Weak as a *static* cue for happy/sad (sr² ≈ 0.00–0.01, Eerola) BUT dynamic *changes* are potent for
  chills (§3). Loudness ≈ energy/arousal, not valence.

**ARTICULATION**
- Staccato (detached) → happy, playful, energetic (β = +0.14 happiness). Legato (connected) → sad,
  tender, calm (β = −0.18 sadness, sr² = 0.04). In production terms: short, gapped notes = up;
  smeared/overlapping = down. (Eerola 2013; Juslin 2000 cue study, below.)

**TIMBRE (brightness / harmonic richness)**
- Bright/sharp (more high harmonics) → happy, energetic, but also anger at high arousal.
  Dark/soft (rolled-off highs) → sad, tender, calm (β = −0.14 sadness). Weak as static happy/sad cue
  (sr² 0.01) but strong for *specific* emotions like anger/fear via roughness (§3). (Eerola 2013;
  Gabrielsson & Lindström 2001 list timbre as bright↔soft = arousal.)

**PITCH CONTOUR (melodic direction)**
- Rising contour → increasing tension/arousal, often positive/aspirational; falling contour →
  release, resignation, sadness. Hevner (1936) counted melodic direction among her 6 parameters;
  descending lines cluster with her "sad/dignified" groups. [Contour effects are real but smaller /
  more context-dependent than mode & tempo.]

**RHYTHMIC REGULARITY**
- Regular/firm rhythm → happy, dignified, stable, positive valence. Irregular/complex rhythm →
  tension, unease, agitation, excitement. Firm rhythm sits in Hevner's happy/vigorous clusters;
  irregular rhythm in restless/agitated ones (Hevner 1936; Gabrielsson & Lindström 2001).

### Juslin's performer cues (Juslin 2000, "Cue Utilization in Communication of Emotion in Music
Performance", *J. Exp. Psychol: HPP*) — how *performers* encode each emotion (matches perception):
- **Happiness:** fast tempo, moderate–loud, staccato, bright timbre, small timing variation.
- **Sadness:** slow tempo + final ritardando (slowing at end), soft, legato, dark/dull timbre,
  large expressive timing variability.
- **Anger:** fast, very loud, mostly staccato, sharp/harsh timbre, abrupt attacks.
- **Fear:** irregular/staccato, soft with large loudness swings, fast but unstable, thin timbre.
- **Tenderness:** slow, soft, legato, soft warm timbre, gentle timing.
Key principle: **multiple redundant cues** → far more reliable emotion recognition than any one cue.

### Hevner's Adjective Circle (Hevner 1936) — the original map
8 clusters arranged in a circle (roughly a valence/arousal ring): **solemn/spiritual → sad/heavy →
dreamy/tender → lyrical/serene → graceful/playful → happy/bright → exciting/vigorous → agitated/
robust**. Her manipulations found: **major = happy/graceful, minor = sad/dreamy; firm rhythm = vigorous/
dignified, flowing rhythm = happy/tender; complex/dissonant harmony = agitated/vigorous, simple/
consonant = happy/serene; high pitch = playful/happy, low pitch = sad/dignified; ascending = ?,
descending melody = sad.** Mode and rhythm were her strongest movers.

---

## 2. Valence / Arousal Model (Russell 1980 circumplex)

Two axes: **valence** (unpleasant ↔ pleasant, horizontal) and **arousal** (calm ↔ energized, vertical).
Four quadrants + the cue recipe that lands you there:

| Quadrant | Emotion | Recipe (stack the cues) |
|---|---|---|
| **High arousal + positive** | **Happy / excited / joyful** | Major, fast (~120+), higher register, loud, staccato, bright timbre, firm rhythm |
| **High arousal + negative** | **Tense / angry / fearful** | Minor (or dissonant/chromatic), fast, loud, harsh/rough timbre, irregular rhythm, high register |
| **Low arousal + negative** | **Sad / depressed** | Minor, slow (<80), low register, soft, legato, dark timbre, falling contour, ritardando |
| **Low arousal + positive** | **Calm / tender / serene** | Major, slow, soft, legato, warm/dark-but-smooth timbre, consonant, regular gentle rhythm |

**What moves a piece between quadrants:**
- **Valence axis is driven mostly by MODE + harmony (consonance/dissonance).** Flip major↔minor or
  add/remove dissonance to slide left/right.
- **Arousal axis is driven mostly by TEMPO + loudness + register + timbre brightness.** Speed up,
  get louder, go higher/brighter to slide up. (Gabrielsson & Lindström 2001; Russell 1980.)
- Because cues are additive (Eerola 2013), you can move on one axis without touching the other:
  keep minor but double the tempo and add loud drums → sad → *angry/driving* (same low valence,
  higher arousal). Keep the slow tempo but switch minor→major → sad → *tender/calm*.

---

## 3. Specific Reliable Effects (with numbers)

**Tempo ↔ heart-rate anchoring.** Perceived arousal tracks tempo against resting HR (~60–80 bpm).
- **Slow / calming: ~60–80 bpm** promotes parasympathetic dominance, lowers HR; largest stress-relief
  effects in meta-analyses. **Excited/ergogenic: >120 bpm** raises HR, sympathetic activation.
  **85–120 bpm** is a "no perceptual bias" comfort window near breathing/HR rhythms — reads as
  neutral/medium arousal. (Multiple tempo-HR studies; e.g. *Sci. Reports* 2025 tempo/EEG; exercise-
  music tempo literature.) [Exact boundaries vary by study — treat 60/120 as soft anchors, not laws.]
- Hip hop translation: 60–80 bpm (or 120–160 half-time) = introspective/heavy; 90–100 = head-nod
  neutral; 120–140 straight = energetic/club.

**"Sad music is enjoyable" (the paradox).** People seek out sad music and *like* it.
- Mechanism: liking of sad music is **fully mediated by "feeling moved"/being touched** — not the
  sadness itself (Vuoskoski & Eerola 2017, *Frontiers*, "The Pleasure Evoked by Sad Music Is Mediated
  by Feelings of Being Moved").
- Sadness felt from music is **vicarious** (no real-life loss), so positive emotions can co-occur;
  listeners report *mixed* emotions and separate "perceived" vs "felt" sadness (Kawakami et al.).
- Trait **empathy** predicts both feeling and preferring sad music (Vuoskoski & Eerola 2015).
- Also drives **nostalgia**, which lifts mood (Sachs/other reviews; *Frontiers* 2015 systematic review
  "The pleasures of sad music"). Practical: minor-key, slow, legato beats can be *pleasurable*, not a
  turn-off, if they evoke being-moved/nostalgia — lean into warm timbre + memory-triggering samples.

**Minor third ↔ sadness, shared with speech.** Curtis & Bharucha 2010 (*Emotion*), "The Minor Third
Communicates Sadness in Speech, Mirroring Its Use in Music": actresses' *sad* speech naturally
falls to a **minor-third (3-semitone) drop** between its two salient pitches; the minor third was the
**most reliable acoustic cue for sadness**. Implication: a falling minor-3rd motif (e.g. from the 5th
down to the b3, or any 3-semitone descent) is a hard-wired "sad" gesture — it mirrors how a human
voice sags when sad. Great for melodic hooks and vocal-chop pitching.

**Dissonance / roughness ↔ threat.** "Roughness" = amplitude modulation / beating in the
**~30–150 Hz (core 30–80 Hz) modulation range**, produced by close, clashing frequencies (Helmholtz).
- Human **alarm/scream signals exploit this exact band**; roughness triggers negative affect and fast
  defensive reactions and engages threat circuitry (amygdala/salience network). (Arnal et al.;
  "Auditory roughness elicits defense reactions", *Sci. Reports* 2020/21.)
- Harsh sounds ~2,000–5,000 Hz get their unpleasantness *amplified* by the amygdala.
- Production use: intentional dissonance, detuned/clustered stacks, distorted/clipping timbres, and
  gritty high-mids read as *danger/aggression* — the sonic vocabulary of drill/trap menace. Consonance
  (simple ratios, clean harmonics) reads safe/pleasant.

**Expectation, tension & chills (Meyer → Huron).**
- **Meyer (1956):** emotion in music arises from **delayed/denied expectation** — set up a pattern,
  withhold resolution, and the tension→release *is* the felt emotion. Suspensions, deceptive cadences,
  drops that don't land where expected.
- **Huron, *Sweet Anticipation* (2006), ITPRA:** five response stages — **I**magination, **T**ension
  (pre-outcome: arousal ramps as the expected event approaches), **P**rediction, **R**eaction (fast,
  automatic, conservative), **A**ppraisal (slow, conscious). Pleasure comes largely from the
  **prediction/appraisal payoff** when an outcome is *slightly* violated then confirmed — the "sweet"
  surprise. Build tension by delaying the downbeat / the bass / the drop, then resolve.

**Frisson / chills / "skin orgasm" triggers.** Sloboda 1991 (Keele) pinpointed the moments; Panksepp
1995 ran controlled chills experiments. Reliable triggers:
1. **Unexpected/unprepared harmony** (a chord you didn't see coming) — strongest structural cause.
2. **Sudden dynamic change** (a swell, or a sudden loud entry after quiet).
3. **Entry of a new voice/texture** (a solo, a choir, a new layer dropping in) — the single most cited
   chill trigger. (Sloboda 1991; Panksepp 1995; review in Harrison & Loui 2014 *Frontiers*, "Thrills,
   chills, frissons, and skin orgasms".) Openness-to-experience predicts who gets frisson [personality
   correlate].
   - Beat translation: bring in a new element *unquietly* after a stripped bar, modulate to an
     unexpected chord, or hit a big dynamic contrast at the hook.

---

## 4. Low Frequencies, Body & Repetition

**Bass / sub & the body (groove).**
- **Low-frequency amplitude directly increases the urge to move.** Adding inaudible-range
  **very-low-frequency bass** made people **dance 11.8% more** (Cameron et al. 2022, *Current Biology*
  — live EDM show with VLF speakers). Bass is *felt* as much as heard.
- Groove ratings correlate most strongly with **spectral flux in the 50–100 Hz band** (kick + bass
  region) (Stupacher et al. 2016). Louder, punchier sub = more groove.
- **Multimodal effect:** bass delivered to skin (tactile) as well as ears raises aesthetic appreciation
  and body movement — auditory-tactile percept links straight to the motor system (Hove et al.,
  "Feel the bass"). Why sub *feels powerful*: it recruits touch + motor pathways, not just hearing.
- **Low-frequency + syncopation both boost groove** in house music (Stupacher/UCL 2024, "Move Your
  Body!"). Mix your kick/808 loud and let it be *felt*.

**Syncopation sweet spot (inverted-U).** Witek et al. 2014 (*PLOS ONE*), "Syncopation, Body-Movement
and Pleasure in Groove Music": pleasure and desire-to-move follow an **inverted-U vs. syncopation** —
**medium syncopation maximizes groove**; too little = boring/robotic, too much = confusing, both kill
the urge to move. Practical: leave gaps and off-beat hits, but keep the pulse recoverable — don't
bury the "one." This is the theoretical basis for a good boom-bap/trap pocket.

**Repetition → pleasure (Margulis).** Elizabeth Margulis, *On Repeat* (2014):
- **Mere-exposure effect** (Zajonc 1968): more familiarity → more liking. Repetition makes music feel
  more enjoyable, more "wanting to move," even judged **more human/intentional**.
- Inserting *artificial literal repetition* into even random tone sequences raised liking and perceived
  musicality (Margulis 2013). Repetition shifts the listener from evaluating to *participating*
  (anticipating, singing along, embodied).
- Not infinite: liking rises then falls with over-repetition (inverted-U over many plays). [The
  wear-out point is fuzzy/individual.]
- Beat translation: loops, repeated hooks, and the 4/8-bar loop structure of hip hop are *why it works*
  — repetition is a feature, not laziness. Vary *timbre/texture* across repeats to delay wear-out.

---

## Summary Table — Turn This Knob, Get This Feeling

| Parameter | Move it this way | Feeling shifts toward | Source |
|---|---|---|---|
| **Mode** | major → minor | happy → sad / darker (valence ↓) | Eerola 2013 (sr² 0.29); Hevner 1936 |
| **Mode** | minor → major | sad → happy / bright (valence ↑) | Eerola 2013; Gabrielsson & Lindström 2001 |
| **Tempo** | slower (<80 bpm) | calm, sad, introspective (arousal ↓) | Eerola 2013; tempo-HR meta-analyses |
| **Tempo** | faster (>120 bpm) | excited, happy, energetic (arousal ↑) | Eerola 2013; Juslin 2000 |
| **Register/pitch** | lower | sad, heavy, potent | Eerola 2013 |
| **Register/pitch** | higher | happy, bright, aroused | Eerola 2013; Hevner 1936 |
| **Loudness** | louder | powerful, angry, joyful (arousal ↑) | Juslin 2000; Gabrielsson & Lindström 2001 |
| **Loudness** | softer | tender, sad, fearful | Juslin 2000 |
| **Articulation** | legato (connected) | sad, calm, tender | Eerola 2013; Juslin 2000 |
| **Articulation** | staccato (detached) | happy, playful, energetic | Eerola 2013; Juslin 2000 |
| **Timbre** | darker / rolled-off highs | sad, warm, calm | Eerola 2013; Gabrielsson & Lindström 2001 |
| **Timbre** | brighter / more harmonics | happy, energetic (or angry, hot) | Eerola 2013 |
| **Timbre** | add roughness/dissonance (30–80 Hz beating, distortion) | threat, aggression, fear | Arnal / *Sci.Reports* 2020; Helmholtz |
| **Melodic contour** | falling (esp. minor 3rd / 3-semitone drop) | sadness (mirrors sad speech) | Curtis & Bharucha 2010; Hevner 1936 |
| **Melodic contour** | rising | tension, aspiration, arousal ↑ | Hevner 1936 |
| **Rhythm** | irregular / complex | tension, agitation, excitement | Hevner 1936; Gabrielsson & Lindström 2001 |
| **Rhythm** | firm / regular | stable, dignified, happy | Hevner 1936 |
| **Syncopation** | toward *medium* (not zero, not max) | maximum groove / urge to move | Witek et al. 2014 (inverted-U) |
| **Sub-bass** | louder / felt (50–100 Hz, VLF) | more body movement, power, groove | Cameron 2022; Stupacher 2016; Hove |
| **Expectation** | delay/deny then resolve; unprepared harmony | tension → release, chills, "moved" | Meyer 1956; Huron 2006 (ITPRA) |
| **Dynamics/texture** | sudden swell / new voice entering | frisson / chills | Sloboda 1991; Panksepp 1995 |
| **Repetition** | loop / repeat hooks (to a point) | rising familiarity & pleasure; vary timbre to delay wear-out | Margulis 2014; Zajonc 1968 |
| **Sad-but-warm combo** | minor + slow + legato + warm timbre + nostalgic sample | pleasurable "being moved," not depressing | Vuoskoski & Eerola 2017 |

---
### Sources (primary)
- Eerola, Friberg & Bresin 2013, *Frontiers in Psychology* — primary-cue contribution/linearity/additivity.
- Gabrielsson & Lindström 2001/2010 — musical-structure/emotion survey; arousal vs valence cue split.
- Juslin 2000, *JEP:HPP* — performer cue utilization for happy/sad/angry/fearful/tender.
- Hevner 1936 — adjective circle & element manipulations.
- Russell 1980 — circumplex (valence × arousal).
- Curtis & Bharucha 2010, *Emotion* — minor third in sad speech & music.
- Arnal et al. / *Scientific Reports* 2020 — auditory roughness (30–80 Hz) & threat/defense.
- Meyer 1956 (*Emotion and Meaning in Music*); Huron 2006 (*Sweet Anticipation*, ITPRA).
- Sloboda 1991; Panksepp 1995; Harrison & Loui 2014 — frisson/chills triggers.
- Cameron et al. 2022 (*Current Biology*); Stupacher et al. 2016; Hove ("Feel the bass"); UCL 2024 — bass/groove/body.
- Witek et al. 2014, *PLOS ONE* — syncopation inverted-U & groove.
- Margulis 2014 (*On Repeat*); Zajonc 1968 — repetition/mere exposure.
- Vuoskoski & Eerola 2015/2017; Kawakami — enjoyment of sad music / being moved.

*No suspicious / AI-directed content was found on any page consulted. All claims paraphrased.*

=====================================================
SOURCE FILE: research-emotion-production.md
ORIGINAL LOCATION: HS:.claude/skills/drum-loops/references/research-emotion-production.md
=====================================================

# Production-Level Devices for Eliciting Feelings
Research for a hip hop producer in Reason 12. Devices that work *above/below harmony*: scoring tricks, sound design, mix moves, arrangement, groove, and voice. Each claim cited; [folklore] = community belief without hard evidence.

---

## 1. Film/game scoring device lists per emotion

### Dread / horror
- **Drone of Dread** — a sustained low note or slow-beating cluster under everything; often paired with sub-rumble. Infrasound-adjacent low end causes physical unease even when barely heard ([Tonal Chaos — horror trailer music](https://www.tonalchaostrailers.com/blog/horror-trailer-music-sound-of-fear/); [TV Tropes: Drone of Dread](https://tvtropes.org/pmwiki/pmwiki.php/Main/DroneOfDread)). *Recipe: one low root note (C1–G1), add a second voice a minor 2nd or tritone away, slow LFO on pitch ±10–20 cents.*
- **Tone clusters & minor 2nds** — adjacent semitones held together create "constant musical anxiety"; the tritone reads as dread ([Film Music Theory — harmonic tension in horror](https://filmmusictheory.com/article/the-psychology-of-harmonic-tension-in-horror-scores/)). *Recipe: stack 3–5 notes one semitone apart in strings/pad, low velocity, long attack.*
- **Low ostinato** — a short relentless repeating figure that never resolves (Jaws two-note motif); repetition without harmonic motion = trapped feeling ([Film Music Theory](https://filmmusictheory.com/article/the-psychology-of-harmonic-tension-in-horror-scores/); [MuseScore — four horror scores to study](https://musescore.com/news/features/four-horror-film-scores-every-composer-should-study-they-build-dread-yet-reveal-1970s-craft-how-strings-scream/)).
- **Silence-then-hit (stinger)** — drop everything, then a loud dissonant attack; expert analysis of jump-scare scoring confirms tension from withheld sound ([Phys.org — what makes a score frightening](https://phys.org/news/2023-10-score-expert-techniques-tension.html)). *Recipe: 1–2 bars of near-silence or a single held note, then full-band cluster hit + sub drop.*
- **Microtonal detuning** — quarter-tone clusters and lines that waver out of tune feel "alien and wrong" beyond normal dissonance ([Tonal Chaos](https://www.tonalchaostrailers.com/blog/horror-trailer-music-sound-of-fear/)).

### Wonder / awe
- **Lydian mode** — the #4 removes gravity toward resolution; "buoyant, weightless." Williams (E.T., Superman flight) and Zimmer (Dune vistas) both lean on it ([Mark Slater — Lydian & the Hollywood sound](https://markslater.net/unlocking-the-power-of-the-lydian-mode/); [Splice — Lydian guide](https://splice.com/blog/music-modes-lydian/)). *Recipe: major key, raise the 4th; melody hangs on the #4.*
- **Wide/open voicings** — stacked 5ths and open spacing; stacking fifths literally spells a Lydian scale ([MusicRadar — cinematic music theory](https://www.musicradar.com/how-to/a-quick-guide-to-the-music-theory-of-cinematic-music)). *Recipe: root low, next voice a 5th up, spread the rest over 2+ octaves; avoid 3rds in the low register.*
- **Slow harmonic rhythm** — hold each chord 2–4 bars; vastness comes from time, not motion ([MusicRadar](https://www.musicradar.com/how-to/a-quick-guide-to-the-music-theory-of-cinematic-music)).

### Grief
- **Solo instrument exposure** — one human-timbre voice (cello, violin) over sparse backing; space to "breathe" maximizes sadness ([Classic FM — sad violin repertoire](https://www.classicfm.com/discover-music/instruments/violin/sad-violin-pieces/); the Platoon/Barber Adagio association per [Jacob Murphy — music of mourning](https://www.jacobmurphyviolin.com/blog/2021/04/30/top-10-list-music-for-mourning)).
- **Appoggiatura / falling contour** — a dissonant "leaning" note on the beat resolving down triggers the tear response; documented in NPR's analysis of Adele's "Someone Like You" ([NPR — the appoggiatura](https://www.npr.org/2012/02/14/146888725/another-take-on-the-appoggiatura)). *Recipe: melody lands one step above the chord tone on the downbeat, sighs down onto it; phrase endings fall, never rise.*

### Heroism
- **Perfect 4th/5th leaps** — tonic→dominant leap opens nearly every Williams hero theme; 4ths/5ths saturate the whole fanfare structure ([Film Music Notes — Star Wars Main Title](https://filmmusicnotes.com/john-williams-themes-part-2-star-wars-main-title/); [Superman March analysis](https://filmmusicnotes.com/john-williams-superman-theme-superman-march/)).
- **Brass register as meaning** — trumpet at the top of its range = heroic strain; the same brass mid-low = menace (Imperial March) ([Film Music Notes — Imperial March](https://filmmusicnotes.com/john-williams-themes-part-3-of-6-the-imperial-march-darth-vaders-theme/)). *Recipe: brass patch, melody C4–C5 zone pushed loud (heroic) vs same line an octave down with minor harmony (villain).*

### Unease
- **Irregular meter** — 5/4, 7/8 read as "unbalanced and abrupt"; standard in tension/action cues ([Film Music Theory — odd time signatures](https://filmmusictheory.com/article/adding-unpredictability-in-music-odd-time-signatures/)). *Recipe: loop a 7/8 hat pattern under a 4/4 kick, or chop one 8th off every second bar.*
- **Detuned instruments** — heavily detuned strings, wavering pitch = "seasickness" ([Tonal Chaos](https://www.tonalchaostrailers.com/blog/horror-trailer-music-sound-of-fear/)). *Recipe: two copies of a lead, one −30 to −50 cents, both mono, no chorus — beating does the work.*

---

## 2. Sound design & mix moves → feelings

| Move | Feeling | Why / source |
|---|---|---|
| Vinyl crackle, tape hiss, saturation, softened highs | Nostalgia, intimacy, comfort | Simulates childhood media (old records/cassettes); "imperfection by design" reads as human and lived-in ([LANDR — what is lo-fi](https://blog.landr.com/lofi/); [Soundfly — nostalgic lo-fi](https://flypaper.soundfly.com/produce/how-to-add-a-nostalgic-touch-to-your-lo-fi-music/); [Musical Flora](https://www.musicalflora.com/genres/lofi/how-vinyl-records-shaped-soul-lofi-music/)). Reason: Scream 4 + EQ high shelf −6 dB @ 8 kHz + noise sample. |
| Heavy sub / low rumble | Power, menace | Near-infrasound causes physical discomfort and nervousness below conscious hearing ([Tonal Chaos](https://www.tonalchaostrailers.com/blog/horror-trailer-music-sound-of-fear/)). Sine sub 30–50 Hz, mono. |
| Big hall/cathedral reverb, wide stereo | Awe, grandeur, melancholy | "Where you are tells you how to feel"; long predelay (20–40 ms) signals a huge space ([Beat Kitchen — reverb](https://beatkitchen.io/guides/mix-primer/25-reverb/); [Relab — room size](https://relabdevelopment.com/learning-center/reverb-section/reverb-room-size/)). RV7000: hall, 3–6 s decay, predelay 30 ms. |
| Dry, close, small room | Intimacy, urgency, claustrophobia | Dry close vocal = "pillow talk"; 1–2 ms first reflections = tiny room ([Beat Kitchen](https://beatkitchen.io/guides/mix-primer/25-reverb/)). Reverb send under 10%, predelay ~0. |
| Detune / chorus / doubled slightly-off layers | Dreaminess, haze | Slow beating between voices blurs pitch certainty; core of dream-pop/lo-fi practice [folklore, but consistent across production guides e.g. [LANDR](https://blog.landr.com/lofi/)]. Unison +/−10 cents, slow chorus. |
| Distortion / saturation pushed hard | Aggression, rawness | Roughness is one of the vocal emotional behaviors (screams) that transfers to instruments — distorted timbre is heard like a distressed voice ([PMC — "Even violins can cry"](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8558776/)). |
| Low-pass / sample-rate-reduced "underwater" section | Memory, distance, submersion | 40's Drake sound (see case study 3 below); filtering reads as hearing through a wall/water = emotional remove ([HipHopDX — 40 interview](https://hiphopdx.com/news/id.37925/title.noah-40-shebib-details-creating-signature-sound-with-drake)). |
| Risers / falls, filter sweeps | Anticipation / release | Rising pitch+noise = incoming event; cutting lows+highs pre-drop then restoring them makes the drop land ([Point Blank — tension and release](https://www.pointblankmusicschool.com/blog/creating-tension-and-release-in-electronic-dance-music/); [iZotope — transitions](https://www.izotope.com/en/learn/how-to-create-better-transitions-in-your-mix)). |

---

## 3. Arrangement & dynamics → feelings
- **Drop-out before the hook** — strip to near-nothing for 1–2 beats/bars so the hook slams; "a moment of nothing is often more powerful than another riser" ([FaderPro — silence as a weapon](https://blog.faderpro.com/creativity/silence-in-music-production/); [Point Blank — make drops hit harder](https://www.pointblankmusicschool.com/blog/how-to-make-your-drops-hit-harder-tips-for-edm-producers/)). Impact = contrast, not loudness.
- **Additive builds** — introduce one element every 4–8 bars; momentum from accumulating layers ([Breve — arrangement hacks](https://brevemusicstudios.com/building-tension-and-release-arrangement-hacks-for-techno-music/)).
- **Sudden total silence** — a hard 4–8-count cut mid-track = shock; the drop after "hits extra-hard" ([Bax — ultimate drop](https://www.bax-shop.co.uk/blog/dj-gear/edm-tips-tricks-how-to-make-the-ultimate-drop/)).
- **Half-time switch** — halving perceived tempo adds weight; trap/drill live on the half-time feel (140 BPM feels like 70) ([Sample Focus — BPM guide](https://blog.samplefocus.com/blog/ultimate-guide-to-tempo-and-bpm-the-best-bpms-for-hip-hop-trap-dnb-and-more/)).
- **Key change up for the last hook** — lift, triumph — but it's the "Truck Driver's Gear Change," a widely mocked **cliché**; use knowingly or not at all ([TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/TruckDriversGearChange); [How Music Really Works](https://www.howmusicreallyworks.com/chapter-six-chords-progressions/truck-drivers-gear-change-shift.html)).
- **Ending unresolved** — stop on IV, V, or vi instead of I, or fade the loop mid-phrase = longing; the appoggiatura/unresolved-dissonance mechanism at song scale ([NPR](https://www.npr.org/2012/02/14/146888725/another-take-on-the-appoggiatura)) [partly folklore as a whole-song device].

---

## 4. Tempo & groove → body
- **Documented hip hop tempo bands**: boom-bap 80–100 BPM (golden-era core 85–95); introspective/melodic rap 60–85; lo-fi 75–95; trap 130–145 (feels 65–72 half-time); drill 132–155; grime ~140 ([Sample Focus BPM guide](https://blog.samplefocus.com/blog/ultimate-guide-to-tempo-and-bpm-the-best-bpms-for-hip-hop-trap-dnb-and-more/); [Firebeats — BPM by rap style](https://firebeats.shop/blog/bpm-guide-for-different-rap-styles-producers-reference/)). Hype = faster grid subdivision (hat rolls), chill = slower/half-time — not raw BPM.
- **Swing = attitude**: dead-on grid = machine/serious/cold; ~53–57% swing = classic MPC head-nod; beyond that, or fully unquantized, = human/drunk/relaxed ([Gearspace — Dilla swing thread [folklore numbers]](https://gearspace.com/board/rap-hip-hop-engineering-and-production/864711-j-dilla-quot-swing-quot-his-beats.html); [Roger Linn on drum machine groove](https://brettworks.com/2013/07/23/roger-linn-on-drum-machine-groove-and-j-dillas-off-beat-sound/)).
- **Dilla's actual trick**: quantize OFF, play live, then nudge — kicks/snares drag 10–20 ms behind grid while hats push slightly ahead; the conflict is the "drunk" pocket ([Big Noise Radio — Dilla Time techniques](https://bignoiseradio.com/dilla-time-simple-complex-music-production-techniques/); Roger Linn interview above). *Reason recipe: record pads live with quantize off, or shift kick lane +15 ms and leave hats on grid.*

---

## 5. Wordless voice → warmth / soul / ghostliness
- The voice is the most emotionally direct instrument: unmatched dynamic range and micro-expression ([Professional Composers](https://professionalcomposers.com/why-the-human-voice-is-the-best-instrument/)).
- Science: listeners hear emotion in *any* sound that mimics vocal behaviors — tremor, roughness, "smiling" brightness — even on violins ([PMC — vocal emotional behaviours drive emotion in non-vocal music](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8558776/)). Wordless voice keeps the emotional carrier and removes the semantic layer, so the feeling arrives unfiltered.
- Practical: humming/legato "oohs" = warmth; pitched-up chipmunk chops = soul-nostalgia (Kanye lineage, see case 4); choir pad low in the mix = sacred/ghostly; formant-shifted or reversed chops = haunted [device mapping is producer folklore; mechanism is the cited vocal-mimicry research].

---

## 6. Case studies (producer/composer explains the HOW)
1. **Hans Zimmer — Dunkirk (endless dread)**: three overlapping Shepard tones (illusion of ever-rising pitch) on three timescales; "tension in the endlessness of a note… you never know when it's going to strike" ([CBC interview](https://www.cbc.ca/radio/q/blog/hans-zimmer-explains-the-audio-trickery-that-made-dunkirk-audiences-nauseous-1.4311684); [Ed Newton-Rex analysis](https://medium.com/world-of-music/the-dunkirk-soundtrack-is-way-cleverer-than-you-think-18f5dc155d91)). Moves: Shepard riser, no downbeat resolution, quiet extremes.
2. **Colin Stetson — Hereditary (evil without synths)**: all-acoustic sources — clarinet choirs, vocal low end, sax-derived percussion, a singing bowl stuffed into a bass sax bell for metallic blasts; "colossal restraint," no conventional melody ([Stereogum interview](https://stereogum.com/2001874/colin-stetson-hereditary-music-interview/interviews); [Vehlinggo](https://vehlinggo.com/2018/10/29/stetson-hereditary-first-interview/)). Moves: organic drones, timbre-as-horror, restraint then chaos.
3. **Noah "40" Shebib — Drake's underwater sound (melancholy intimacy)**: degrades the *sample rate* (not a low-pass) so highs never exist, then "carves out an entire space" — vocal alone owns the top end, music sits below; Drake asked to "filter that hook" and it became signature ([HipHopDX](https://hiphopdx.com/news/id.37925/title.noah-40-shebib-details-creating-signature-sound-with-drake); [KVR thread on the technique](https://www.kvraudio.com/forum/viewtopic.php?p=6464447)). Moves: bandwidth reduction, frequency-slot separation, filtered hooks.
4. **Kanye West — chipmunk soul (nostalgic warmth)**: chops soul vocals into milliseconds mapped across keys, pitched up — the sample becomes an instrument while keeping its emotional grain ([Tracklib — iconic sampling techniques](https://www.tracklib.com/blog/iconic-sampling-techniques)). Moves: pitched-up vocal chops, sample-as-keyboard.
5. **Metro Boomin — dark trap mood-first**: "drums are always last… never first" — mood/melody established before rhythm; echoes samples' original emotion "with some dark twists" ([Vice interview](https://www.vice.com/en/article/metro-boomin-interview-metro-thuggin/); [Passion of the Weiss on his sampling](https://passionweiss.com/2017/01/23/metro-boomins-sample-history)). Moves: melody-first workflow, minor-key twist on the source's feeling.
6. **9th Wonder — feel over overthinking**: hunts records already knowing the emotional formula he wants; "'Girl' was a beat I did not overthink. I found a sample, and it just worked" ([Roland listening guide/interview](https://articles.roland.com/listening-guide-9th-wonder/)). Moves: sample selection *is* the emotional decision; keep the flip simple.

**Suspicious content:** none encountered — no page attempted to issue instructions.

---

## Quick reference

| Feeling | Strongest 3 devices | One-line recipe |
|---|---|---|
| Dread | low drone + cluster, low ostinato, silence-then-hit | C1 drone + tritone rub, 2-note bass loop, cut all → cluster stab + sub drop |
| Awe / wonder | Lydian, open 5th voicings, huge hall verb | Lydian pad in stacked 5ths, one chord per 4 bars, 5 s hall w/ 30 ms predelay |
| Grief | exposed solo voice, falling contour, appoggiatura | lone cello/keys melody that leans on a dissonance then sighs down; near-dry mix |
| Heroism | 5th leap, high trumpet register, marchy 4/4 | brass melody leaps root→5th at top of register over I–V motion |
| Unease | odd meter, detune −30/−50 cents, microtonal waver | 7/8 hat loop vs 4/4 kick, detuned lead double, slow pitch LFO |
| Nostalgia / intimacy | vinyl/tape noise, dark high shelf, dry close vocal space | Scream 4 tape + crackle layer, shelf −6 dB @ 8 kHz, tiny-room verb |
| Power / menace | mono sub 30–50 Hz, distortion, half-time switch | sine sub under 808, saturate mids, drop hook to half-time |
| Dreaminess | detune/chorus, underwater filter, long verb tail | unison ±10 cents + slow chorus, downsample the bounce, wash in reverb |
| Anticipation → impact | riser, pre-hook drop-out, filter cut/restore | noise riser 4 bars, kill everything 1 bar, slam hook full-band full-spectrum |
| Longing | unresolved ending, filtered outro, fading loop | end on IV or vi, low-pass the last 8 bars, fade mid-phrase |
| Soul / warmth | pitched-up vocal chops, humming layer, swing 54–57% | chipmunk soul chops on pads, low hum pad, MPC swing on hats |
| Machine / menace groove | 0 swing, on-grid hats, rigid velocity | quantize 100%, fixed velocities — cold on purpose |

=== END OF PART ===
