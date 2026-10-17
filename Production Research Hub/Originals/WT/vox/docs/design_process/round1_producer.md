# ROUND 1 — SONIC DIRECTION & NOVEL EFFECT INVENTION
**Role: Producer. No code. Opinions are load-bearing.**

---

## 1. THE COMPETITIVE FIELD — WHAT'S ACTUALLY THERE

### 1.1 Nectar 4 (Advanced) — verified module list

13 modules: **EQ** (dynamic + pitch-tracking), **Compressor**, **De-esser**, **Gate**, **Saturation**, **Pitch**, **Auto-Level (ALM)**, **Breath Control**, **Voices** (harmony gen), **Backer** (persona/formant re-voicing), **Reverb**, **Delay**, **Dimension**. Plus **Vocal Assistant** (macro-driven auto-setup), **Vocal Unmask** (now its own tab), **Audiolens** (extract a tonal profile from a reference track), and component plug-ins. Bundled Melodyne 5 Essential.

### 1.2 Documented criticisms (from reviews, not vibes)

- **Backer is the marquee feature and it's the weakest.** SOS: "you can't turn your own vocals into a captured version of Adele." MusicTech: "robotic-sounding," "artefacts and glitches."
- **Reverb and delay have no internal ducking.** Confirmed in MusicTech. This is 2026. Every engineer sidechains their verb; iZotope shipped a vocal plugin where you can't.
- **One reverb algorithm.** No low-cut on Saturation.
- **CPU-heavy with multiple modules; steep upgrade price.**

### 1.3 The structural problems nobody in the category has solved

These are the real gaps. Every one of them is an opening.

**(a) Every "AI" in this category is frame-based and phoneme-blind.**
Vocal Assistant, smart:EQ, smart:comp, Gullfoss, Soothe2 — all of them compute statistics over short spectral frames. None of them know that *this* frame is an /s/, *that* one is a sustained vowel, *that* one is an inhale, *that* one is a plosive. Every processing decision in the category is made without the single most important piece of context. A de-esser firing at -20 dB doesn't know it's mid-vowel; a leveler doesn't know it's boosting room tone. This is the category's foundational blind spot and it is now cheap to fix.

**(b) Static targets for a non-static source.**
Vocal Assistant analyzes a clip once and sets a fixed chain. But a singer in verse 1 (chest, 6" off the capsule, conversational) and the same singer in the last chorus (belt, 14" back, off-axis, pushing) are effectively two different instruments. One static target is wrong for at least one of them — which is exactly why "the chorus vocal sounds different" is the single most common complaint on modern comped records.

**(c) Unmasking ducks the wrong thing.**
Nectar's Vocal Unmask, Trackspacer, and every clone duck the music where the *vocal is loud*. That is precisely backwards. Loud vowels are already winning the masking fight — ducking there is wasted, audible, and pumps. The lyric gets lost on the *quiet consonants*, where these tools do nothing because there's no energy to key off. This is a genuine technical error shipped by the whole category, and it's provable with a psychoacoustic masking model.

**(d) Breath handling is binary.** Nectar Breath Control, Waves DeBreath: reduce or remove. Nobody *shapes* breaths. Breaths are 30% of the intimacy of a modern pop vocal, and a gated breath is the #1 tell that a record was processed by a machine.

**(e) Leveling tools ride level, but engineers are chasing something else.**
The Gearspace consensus on Vocal Rider is real: it "changes the inner groove," it's "better for voiceover." The reason is that a human engineer rides for *intelligibility and emotional weight*, not for constant RMS. Riding a soft phrase up 6 dB makes it loud — but it still *sounds* soft, because vocal effort is encoded in spectral tilt and glottal behavior, not amplitude. Nobody has separated those two axes.

**(f) Suppression tools destroy identity.** The recurring practitioner warning about Soothe2: "very easy to overdo," "don't end up killing the character." No tool in the category has any concept of what makes *this singer* sound like themselves and therefore what is off-limits.

**(g) Latency is a real constraint.** Pro-Q 4's spectral mode is avoided by working engineers purely because of latency. Anything we build with lookahead needs an honest low-latency mode, not a "please freeze the track" mode.

**(h) Nobody works across tracks.** Every one of these plugins is an island on one channel. Lead + doubles + 18 BGVs is how records are actually made, and the category has nothing to say about it.

---

## 2. SONIC TARGET — "CRISP, CLEAR, COMPRESSED, TOP-OF-THE-LINE" IN NUMBERS

The phrase is useless until it's measurable. These are the targets I want the DSP team hitting. Where a number is convention rather than measured law, I say so.

### 2.1 Dynamics / consistency
| Metric | Raw vocal (typical) | Target (finished lead) | Notes |
|---|---|---|---|
| Crest factor (peak vs 400 ms RMS) | 14–20 dB | **6–9 dB** pop/R&B, **5–7 dB** rap/rock, **10–12 dB** folk/jazz | Below 5 dB it reads as squashed and lifeless |
| Short-term loudness range (LRA) over a section | 10–15 LU | **3–5 LU** | This is the single best proxy for "sits in the mix" |
| Syllable-nucleus RMS std. dev. within a section | 4–7 dB | **< 1.5 dB** | *Measure per syllable, not per frame.* This is the metric that actually correlates with a hand-ridden vocal |
| Gain-reduction motion | — | **< 3 dB of change within any 50 ms window** | Faster than this and you hear it as pumping; this is the rule Vocal Rider violates |
| Lead vocal level vs. full mix | — | **−4 to −2 LU** (pop/hiphop), **−7 to −5 LU** (rock/alt) short-term | Genre-dependent; must be a target the user sets |

### 2.2 Spectral balance (long-term average spectrum of the processed lead)
- **HPF:** 80–100 Hz (male), 100–140 Hz (female) — 12–18 dB/oct.
- **Body:** fundamental region intact (male ~100–160 Hz, female ~180–280 Hz). Do not thin the fundamental to fix mud.
- **Mud (200–450 Hz):** −2 to −4 dB, **dynamically**, keyed to when it's actually excessive — not a static cut.
- **Nasal/boxy (700 Hz–1.2 kHz):** singer-dependent notch, −2 to −5 dB, narrow (Q 4–8), only when resonance exceeds neighbors by >5 dB.
- **Presence (2.5–5 kHz):** +2 to +4 dB vs. raw. **This is where the category goes wrong** — presence should be raised on *consonants*, not on the whole signal, or you get harsh vowels (see §3.1).
- **Air (>10 kHz):** +2 to +3 dB shelf. Above +4 dB it's a "plugin-y" sound.
- **Spectral tilt above 1 kHz:** roughly **−3 to −4 dB/octave** for a modern pop lead. Steeper reads dull, flatter reads harsh/thin.

### 2.3 Sibilance — the target nobody uses
Absolute-threshold de-essing is the wrong control law. The correct target is **relative**:

> Energy in the 5–10 kHz band during a sibilant frame should sit **+3 to +6 dB** above the same band's energy averaged over the adjacent vowel frames *of the same phrase*.

Below +3 dB you have a lisp; above +8 dB it's a spit-take. This target auto-adapts to the singer, the mic, and the section — which is exactly what a fixed threshold can never do. **Non-negotiable requirement: our de-esser must never induce a lisp.** Attenuation-only de-essing always will at some point; resynthesis will not (see §3.1).

### 2.4 Breaths
- Breath RMS: **12–20 dB below adjacent phrase RMS**, and — critically — **consistent within ±2 dB across the whole song**.
- Never fully removed. A gated breath (fast attack, >25 dB reduction) is the machine tell.
- Breath duration preserved. Truncating an inhale changes the perceived phrasing.

### 2.5 Plosives / mechanical noise
- Any sub-120 Hz transient exceeding adjacent vowel LF energy by **>10 dB** = pop, must be removed without touching the following vowel's fundamental.
- Mouth clicks: <30 ms broadband events with harmonicity <0.2 between phrases.

### 2.6 Intelligibility (the one the category has never measured)
- **Consonant-to-Vowel Ratio (CVR):** the documented speech-science parameter for intelligibility. Raw vocals run **−8 to −15 dB**. Great pop mixes run **−4 to −8 dB**. This, not "brightness," is what "cuts through" actually means.
- **Objective intelligibility of vocal-against-mix (ESTOI-class metric): target > 0.75.** Measured against the *instrumental bed*, not in solo.
- Both of these are claimable in marketing with real numbers. iZotope cannot currently make a single measurable claim about Unmask.

### 2.7 Consistency across the record (the "one performance" test)
- Take-to-take LTAS deviation across a comped lead: **< 1.5 dB RMS in any 1/3-octave band**.
- Estimated direct-to-reverberant ratio variance across the comp: **< 2 dB**.
- If these two hold, nobody hears the punch-ins. If they don't, no amount of EQ saves it.

---

## 3. EIGHT CANDIDATE NOVEL EFFECTS

Ranked by my confidence. Nothing here is a chorus, delay, reverb, autotune, or vocoder. Where an idea is weaker than it looks, I say so in its own entry.

---

### 3.1 **DICTION** — Consonant/Vowel Ratio Engine
**Pitch:** Turn up the singer's *diction* instead of their treble.

**What it does sonically:** Splits the vocal into consonant energy and vowel energy and lets you rebalance them independently. Push it and the lyric gets dramatically more intelligible and forward — but the vowels don't get any brighter, so there's no harshness, no ess-buildup, no "exciter sheen." Pull it back and you get a soft, blurred, intimate delivery on demand. It's the difference between a vocal that *cuts* and a vocal that's merely *loud and bright*.

**Why nothing on the market does it:** Every tool in the category has exactly two ways to make a vocal clearer: a presence boost (which raises consonants AND vowels, and vowels are where harshness lives) or a de-esser (which only *reduces*, and only one consonant class). Nobody separates the streams. This is the most under-exploited lever in vocal processing and it comes straight out of hearing-aid research, where CVR manipulation is standard practice.

**Approach — DSP + ML:**
- Lightweight phoneme-class classifier (6–8 classes: sibilant / stop-plosive / non-sibilant fricative / nasal / voiced vowel / breath / silence / transitional), ~10 ms hop, ~25 ms lookahead. Small enough to run real-time; this is a classification problem, not synthesis.
- Sines + transients + noise decomposition (harmonic/percussive/residual) so the noise-band residual is separable from the harmonic vowel core.
- The classifier drives independent gain envelopes on the residual and harmonic streams, with class-specific spectral shaping (a /t/ wants 3–6 kHz, an /s/ wants 6–10 kHz, an /f/ wants broadband).
- **Sibilant resynthesis sub-mode:** rather than attenuating an over-hot /s/, replace its noise band with a synthesized sibilant matched to the singer's own average /s/ spectrum at the target level. Attenuation causes lisps; substitution cannot. This alone is worth the module.

**Real record use case:** A dense rap verse over an 808-and-sample bed where the delivery is fast and mumbly. Today, engineers reach for an exciter and a 3 kHz boost, and the vowels turn to razor blades by the third chorus. DICTION gets the words back with the vowel character untouched. Equally: a breathy indie ballad where the artist under-enunciates and the label wants the lyric legible.

**Honest risk:** Classifier errors on heavily processed/distorted sources. Must fail *soft* — a misclassified frame should produce ≤1 dB of error, not an audible artifact. Mandatory: the module must sound like nothing at all at 0%.

---

### 3.2 **ARBITER** — Masking-Threshold Unmask
**Pitch:** Ducks the music only where the vocal is actually being *buried*, not everywhere it's loud.

**What it does sonically:** Compared to Nectar Unmask or Trackspacer set for the same intelligibility, ARBITER moves a fraction of the music — the backing track stops breathing and pumping on every syllable, but you never lose a word. On quiet consonants and phrase-ends (where lyrics actually get lost) it acts hard; on belted vowels (where the vocal is already winning) it does nothing.

**Why nothing on the market does it:** Existing unmaskers key off the vocal's *energy*. Masking is not about energy — it's about the vocal's in-band level relative to the *masking threshold* the music creates in that band. Those two are wildly different quantities. The whole category ducks maximally at exactly the moments ducking is least needed. This is a correctable engineering error, and it lets us make a numbers claim in marketing that iZotope cannot answer: *"same intelligibility, ~60% less gain reduction applied to your mix."*

**Approach — DSP (psychoacoustics), optional ML refinement:**
- Bark/ERB-band analysis of both the vocal and the sidechained instrumental.
- Compute the instrumental's masking threshold per band per frame using a standard spreading function (with temporal forward/backward masking spread — forward masking is why ducking *before* a consonant works).
- Compute the vocal's in-band level minus that threshold. Duck the instrumental only in bands where that difference falls below a user-set intelligibility margin, and only by the amount needed to restore it.
- Weight bands by their contribution to speech intelligibility (Speech Intelligibility Index band weights) so we spend our ducking budget where it buys words — around 1–4 kHz — instead of on sub-bass nobody's lyric lives in.
- Optional: an ESTOI-class estimator as an outer control loop targeting a measured intelligibility score, so the user sets a *result*, not a threshold.

**Real record use case:** A big EDM/pop drop chorus where a supersaw stack eats the hook. Today you either duck the synths audibly or push the vocal until it's harsh. Also: any hip-hop record built on a busy soul-sample loop sitting exactly in the 2–5 kHz consonant range.

**Honest risk:** Requires a sidechain feed, which is a UX friction point — but Nectar already asks for this, so it's parity, not a new cost.

---

### 3.3 **SEAM** — Comp Welder / Take Matcher
**Pitch:** Makes a lead vocal comped from six sessions, three mics, and one iPhone demo sound like one take on one day.

**What it does sonically:** Auto-detects where the timbre, room, and noise-floor statistics of a comped vocal change — punch-ins, different days, different headphone bleed, the writer's demo line the artist won't re-sing — and continuously morphs each region toward one learned identity target. The seams stop being audible. You stop hearing "oh, that line was flown in."

**Why nothing on the market does it:** Match-EQ tools exist but are static, manual, one-region-at-a-time, and match spectrum only — not room decay, not noise floor. Nobody auto-segments. Every mixer on earth does this by hand with clip gain and multiple EQ instances, and it takes hours per song. This is the single most boring, most universal, most expensive unsolved problem in vocal mixing.

**Approach — DSP + ML:**
- Change-point detection on a feature stream (MFCC/LTAS over *voiced frames only*, noise-floor estimate from inter-phrase gaps, estimated direct-to-reverberant ratio) to segment the comp.
- Robust identity target = confidence-weighted median across segments (weighted by duration and how "clean" the segment reads), or user-nominated "this section is the reference."
- Correction per segment = low-order (8–16 band) minimum-phase morphing filter + noise-floor match + reverb-tail match via decay-time estimation and a short corrective early-reflection stage.
- Crossfade corrections across boundaries over 100–300 ms so no correction change is itself a seam.

**Real record use case:** Literally every commercial pop, country, and R&B record made in the last decade. Concretely: a chorus comped 60% from the tracking session and 40% from a hotel-room punch-in on tour.

**Honest risk:** Needs the whole file, so it's an offline/analysis-pass feature in a real-time plugin — architecturally the most awkward of the eight. Worth it anyway.

---

### 3.4 **CONSONANT LOCK** — Stack Aligner
**Pitch:** Makes 20 stacked vocals land their consonants on the same sample so the stack sounds like one enormous voice instead of a smear.

**What it does sonically:** The flammed /t/, /k/ and smeared /s/ that make an amateur vocal stack sound like mud — gone. The stack tightens into a single wide voice with weight. Vowel pitch, vibrato, and formants are untouched, so it does not sound quantized or robotic; only consonant boundaries move.

**Why nothing on the market does it:** Zero plugins in this category work across tracks. Everyone does this by hand in the DAW, nudging doubles, and it is the difference between a pro stack and a bedroom stack. Vocalign is the closest thing and it time-warps the *whole* signal to a guide, which flattens the performance and pitch-smears vowels.

**Approach — DSP + ML:**
- Multi-instance linked, one designated as the lead/reference.
- Consonant onset detection per track (same classifier as DICTION — shared model, shared cost).
- Per-consonant offset via cross-correlation constrained to ±40 ms, with per-event confidence gating so it never "fixes" a deliberate stagger.
- WSOLA/PSOLA micro time-warping applied *only* to consonant boundary regions, with vowel bodies untouched and warp rate limited (≤3%) so no formant or pitch artifacts.
- Strength control so you can lock at 70% and keep human width.

**Real record use case:** A modern pop last-chorus stack of 16–24 layers, or a gang-vocal rock chorus, or rap ad-lib doubles where sibilant flam is the reason it reads amateur.

**Honest risk:** Multi-instance linking is real engineering work and a support burden across DAWs. It is also the best demo in this document — a before/after on a big stack will sell the product on its own.

---

### 3.5 **EFFORT** — Vocal Effort Morph
**Pitch:** A knob for *how hard the singer sounds like they're trying*, completely independent of how loud they are.

**What it does sonically:** Vocal effort is encoded in spectral tilt, first-formant position, glottal open quotient, harmonic-to-noise ratio, and the onset of grit — not in level. That's why turning up a soft phrase makes it *loud but still timid*, and why compressing a belt makes it *quiet but still shouty*. EFFORT decouples the two. Push it up and a tired 2 a.m. last chorus sounds like the singer went for it. Pull it down and an over-belted verse becomes intimate without dropping in the mix.

**Why nothing on the market does it:** Nectar's Backer changes *who* the singer sounds like (badly — "robotic," per MusicTech). Nobody changes *how hard they're singing*. This is the actual thing producers wish for on every session, and today the only fix is to re-track — which on a booked-out artist means the take you have is the take you ship.

**Approach — DSP + ML:**
- Source-filter separation (glottal inverse filtering or a neural source-filter model) to get an excitation signal and a vocal-tract filter.
- Effort estimator (regressor on spectral tilt, F1, HNR, jitter/shimmer) gives current effort level per frame.
- Rendering: retilt the excitation spectrum (loud singing has markedly less HF rolloff), shift F1 upward with effort, modulate harmonic-to-noise ratio, and introduce controlled subharmonic/roughness content at high effort — all resynthesized through the preserved tract filter so identity is untouched.
- Effort target can be absolute or a *consistency* mode: hold effort constant across the song even where the performance wandered.

**Real record use case:** The last chorus of a ballad tracked at the end of a 10-hour day, where the artist has flown home. Also the reverse: a country vocal where the second verse was over-sung and needs to pull back emotionally without pulling back in level.

**Honest risk:** **The highest-ceiling and highest-risk idea here.** Resynthesis of glottal behavior is where every competitor has produced artifacts, and this is exactly the territory where Backer failed publicly. If it's only 80% clean it's unshippable. I'd prototype this in parallel but not put it on the box until it's proven.

---

### 3.6 **DISTANCE LOCK** — Proximity Normalizer
**Pitch:** Renders every word as if the singer never moved off the microphone.

**What it does sonically:** When a singer leans back for a loud note, three things change at once: the proximity bass shelf collapses, the off-axis high end dulls, and the room ratio jumps. A compressor fixes only the level, which is why the fixed vocal still sounds thin and distant on the loud lines. DISTANCE LOCK estimates mic distance and off-axis angle per frame and inverse-renders every frame to one fixed distance. Suddenly verse and chorus sound like the same instrument.

**Why nothing on the market does it:** The entire category models this as a gain problem. It is a *transfer-function* problem, and the transfer function is time-varying. This is one of the two real reasons "the chorus vocal sounds different" (SEAM is the other).

**Approach — DSP + ML:**
- Small regressor estimating distance/angle from a feature vector: LF-shelf slope below ~200 Hz, HF tilt above ~6 kHz, and an estimated direct-to-reverberant ratio from early-decay coherence.
- Inverse rendering: time-varying first-order LF shelf implementing the inverse proximity curve (approaching +6 dB/octave below the cutoff, with cutoff set by capsule pattern), plus a gentle off-axis HF correction shelf and a direct/room rebalance.
- Rate-limit the correction (≤2 dB per 100 ms) so it never sounds like a filter sweep.
- Capsule presets (cardioid LDC, ribbon, SM7-class dynamic) to set the proximity model — this is real physics, not guesswork.

**Real record use case:** Any live-tracked rock or soul vocal where the singer works the mic. Also the increasingly common case of an artist self-recording at home with wildly inconsistent mic technique.

**Honest risk:** Estimation is only reliable in reasonably direct-sound-dominant recordings. Needs a confidence readout and a hard "do nothing when unsure" behavior.

---

### 3.7 **RESPIRE** — Breath Choreographer
**Pitch:** Treats every breath as a production element with its own level, tone, and effects send — instead of noise to be gated.

**What it does sonically:** Detects each breath and *renders* it rather than removing it: normalized to a set dB below the phrase (consistent to ±2 dB across the whole song), spectrally reshaped, optionally time-adjusted, and — the good part — routable to its own effects send. Put the breaths in a long reverb while the words stay dry and you get the modern intimate-pop sound (Billie/Ariana territory) that people currently build by hand-splitting breaths onto a separate track. Or clamp them to a fixed −18 dB so a screamed rock chorus doesn't sound like a wind tunnel.

**Why nothing on the market does it:** Nectar's Breath Control and Waves DeBreath both only *reduce*. Everyone hears fully-gated breaths as a machine artifact, so everyone under-uses these tools and does it by hand instead. Nobody has framed breaths as a creative element with a mixer strip.

**Approach — DSP + ML:** Breath detection is comparatively easy — broadband noise, harmonicity < 0.2, centroid 1–4 kHz, characteristic 150–400 ms envelope (shares the DICTION classifier). Then: per-breath gain normalization against the adjacent phrase RMS, optional spectral tilt/shaping, optional envelope reshaping, optional time-warp to the grid, and a separate output/send bus for the breath stream. The breath-bus routing is the novel bit and it's trivially implementable.

**Real record use case:** An intimate pop ballad where every inhale should be audible and even. Also a dance vocal where you want the pre-drop inhale enormous and drenched while the words stay bone dry.

**Honest verdict:** The lowest-risk idea in this document and one of the most immediately loved. It is not intellectually deep — it is *good product*.

---

### 3.8 **GESTURE** — Pitch Contour Sculptor
**Pitch:** Edits the *shape* of a singer's pitch movement — scoops, overshoots, vibrato onset, phrase-end sag — without touching the tuning.

**What it does sonically:** Decomposes the f0 contour into note targets, transitions, vibrato, and slow drift, and lets you edit each independently. Tighten transitions and an R&B run gains authority and decisiveness. Remove phrase-end sag (pitch *and* level together) and a hesitant singer sounds confident. Exaggerate scoop-ins and a straight pop take gets soul phrasing. No scale, no snap, no correction.

**Why nothing on the market does it:** Auto-Tune and Melodyne model pitch as a value per note plus a correction speed. Nobody models it as a *gesture vocabulary* you can edit stylistically. The closest thing anyone ships is Melodyne's per-note pitch-drift and modulation sliders, which are manual, per-note, and offline.

**Approach — DSP + ML:** Pitch tracking (CREPE-class or YIN), contour decomposition into note-target + transition + vibrato + drift bands (sinusoidal contour modeling / STRAIGHT-style), per-band editing, resynthesis via PSOLA or phase vocoder with formant preservation.

**Honest risk — read this one carefully:** This is the closest idea in the set to the forbidden zone. If it ever exposes a scale, a key, or a "retune speed," it *is* an autotune reskin and we should kill it. It only justifies its existence if the controls are exclusively gestural (Transition Decisiveness / Vibrato Onset / Phrase-End Lift / Scoop Depth) and it demonstrably cannot fix a wrong note. I'd rank it 8th of 8 and ship it only after the top four are solid.

---

## 4. DARLINGS I KILLED

- **"Relative Sibilance" de-esser** (threshold set against the singer's own vowel spectrum). Genuinely better control law than anything shipping — but it is a *feature* of a de-esser, not a novel effect. It belongs in the baseline chain and inside DICTION, not on the box. Don't let marketing count it as an invention.
- **"Tail Traffic Control"** — phoneme-gated FX sends that put reverb tails in the gaps between words and duck them under consonants. Nectar 4 has no reverb ducking at all, so this is a competitive win. But honestly: *every engineer already sidechains their verb.* The novelty is only that ours is phoneme-aware. That's ducking with a fancy name. Ship it as a checkbox on the send, not as an invention.
- **"AI Saturation" / "neural tube warmth."** A filter and a waveshaper with a fancy name. The category is drowning in these. Refuse.
- **A resonance suppressor.** Soothe2 exists, is excellent, and is entrenched. Building a worse Soothe is a losing move. If we need it, we license or we do it quietly inside the auto-chain — we do not compete on it.
- **A "voice persona" transformer.** Nectar's Backer is the cautionary tale: it's the headline feature and reviewers called it "robotic" with "artefacts and glitches" in print. Voice conversion at shippable quality is a much bigger research problem than a vocal channel strip should take on, and losing the same fight in public buys us nothing.

---

## 5. RECOMMENDED FOCUS

**Build first (Round 2 prototypes):** DICTION, ARBITER, SEAM.
All three (a) apply to 100% of vocals, (b) rest on mature, low-risk DSP with modest ML, and (c) let us make *measured* claims — CVR in dB, intelligibility score, gain-reduction-per-unit-intelligibility — that no competitor can currently answer with a number.

**Hero demo:** CONSONANT LOCK. It has the most dramatic A/B of anything here. Cost is architectural (multi-instance linking), not algorithmic. If the budget exists, it moves into the top three.

**Parallel R&D, off the box until proven:** EFFORT. Highest ceiling in the document and the only idea here that would genuinely change how records get made — and the exact terrain where iZotope shipped an embarrassment. We only announce it when it's clean.

**One architectural note that pays for itself:** DICTION, RESPIRE, and CONSONANT LOCK all run off the same phoneme-class classifier. Build that model once, well, and three modules fall out of it. That shared classifier is the real technical moat — it's the thing the entire category is missing, and once we have it, every module downstream is smarter than its equivalent in Nectar.
