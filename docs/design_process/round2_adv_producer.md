# ROUND 2 — ADVERSARIAL PRODUCER REVIEW

**Role: A&R / mix engineer with veto power. Nothing advances on enthusiasm.**

Reviewed: `/home/claude/vox/round1_producer.md`

---

## 0. HEADLINE

The Round 1 doc is the best-written version of a document I have read fifty times. It is well-argued, it is specific, and **six of its eight "why nothing on the market does it" paragraphs are factually wrong.** Not debatable — wrong. Products exist. Some are $59. One of them is so close to your #3 idea that iZotope built it, shipped it, and then **discontinued it**, which is a market signal you did not look for.

The single most dangerous sentence in the document is §5: *"That shared classifier is the real technical moat."* A phoneme-class classifier is not a moat. Forced aligners and phoneme classifiers derived from wav2vec2 / Whisper encoders are open-source, off-the-shelf, and a competent DSP team ships one in a quarter. iZotope has a research org and Native Instruments' balance sheet. If our entire defensibility is a small classifier, we have no defensibility — we have a head start of roughly two release cycles.

I am letting three things through. I am killing three. Two are conditional and will be killed at the next gate if the conditions aren't met with numbers.

---

## 1. PER-EFFECT VERDICTS

---

### 3.1 DICTION — Consonant/Vowel Ratio Engine → **CONDITIONAL**

**Prior art you missed:**
- **Waves Sibilance** (shipping since 2018) uses *Organic ReSynthesis* — it decomposes the vocal into pitch, formant, amplitude and carrier components and treats sibilance by **resynthesis rather than attenuation**, marketed explicitly on "no lisping, no dulling." Your §3.1 says *"Sibilant resynthesis sub-mode… Attenuation causes lisps; substitution cannot. **This alone is worth the module.**"* That sentence has to come out. Waves owns that claim in the market's mind and a reviewer will find it in ten minutes.
- **Eventide Physion / Physion Mk II** already splits a signal into transient and tonal streams for fully independent processing. Your harmonic/residual decomposition is not new; only the phoneme-class *labelling* of it is.
- CVR manipulation is 30 years of hearing-aid literature (IIT Bombay, *Int. J. Speech Technology* 2014, and the 1991/1999 PubMed work on consonant-vowel intensity ratio). You cite this as a strength. It is also **published prior art**, which means it is not patentable and it is trivially findable by any competitor's researcher.

**What actually survives:** nobody has shipped a *general* consonant-class rebalancer for music — one that raises /t/, /k/, /f/, /ʃ/ independently of vowels across the whole consonant inventory, with a target CVR in dB. That is real and it is the only module in this document that produces a marketing number a competitor cannot answer.

**Honesty flag — this will not sound as good as pitched.** "Push it and the lyric gets dramatically more intelligible… but the vowels don't get any brighter, so there's no harshness." False. Fricatives and affricates *are* a large part of what listeners call harsh. +6 dB on the /ʃ/ in "she" at 6–9 kHz is harsh. You have moved the harshness, not eliminated it. And the module immediately fights the de-esser downstream — you boost sibilants by class, the de-esser pulls them back by level, and the user is now driving two things in opposite directions.

**Would I reach for it on a session?** Yes — the rap-verse-over-808s moment is real and I have that problem weekly. But I reach for it *once, at the top of the chain, as one knob*. Not as a phoneme editor.

**CONDITION TO PASS:**
1. Strike the sibilant-resynthesis novelty claim entirely. It is a table-stakes implementation detail, not an invention.
2. Blind A/B, ten working mixers, in-the-mix (not solo): DICTION at target CVR must beat *(3 kHz shelf + Soothe2 + a competent de-esser)* on intelligibility **and** on "would you print this." If it only wins in solo, it dies.
3. It ships as **one knob with an auto-set target**, wired into the Assistant. The moment it needs an engineer to drive it, it loses to Nectar for the person who actually pays.
4. Prove the interaction with the de-esser is resolved internally, not left to the user.

---

### 3.2 ARBITER — Masking-Threshold Unmask → **CONDITIONAL (weakest of the survivors — expect this to be killed)**

**Prior art you missed, and it is fatal to the pitch as written:**
- **Three-Body Technology UNMASK** (2026, **$59 intro / $129 list**). Its **EXT Glue** module, in the vendor's own words, *"analyzes mutual masking between two signals and resolves the psychoacoustic conflicts between them"* via external sidechain. It is marketed as "a psychoacoustically informed dynamic EQ" operating across spectral, tonal and temporal dimensions — including a TIME module that models **post-transient temporal masking shadows**. That is your Bark-band-plus-spreading-function-plus-temporal-masking architecture, already on sale, for fifty-nine dollars.
- **sonible learn:unmask / smart:unmask** ($69) — AI spectral ducking that analyzes both the prioritized and background signal.
- Plus the ones you already named: Trackspacer, Neutron Unmask.

So §3.2's central assertion — *"This is a genuine technical error shipped by the whole category"* and *"the whole category ducks maximally at exactly the moments ducking is least needed"* — is **no longer true as of this year.** If we publish that line we get corrected in public by a $59 plugin, and every other claim in our marketing becomes suspect by association.

**What actually survives:** two things, both narrow.
- **SII band weighting** — spending the ducking budget where it buys *words* (1–4 kHz), not where it buys meter movement. I have not found this in any shipping product. It is real.
- **The ESTOI outer loop** — the user sets a *result* ("intelligibility 0.80") rather than a threshold. That is a genuinely different control law and it is the only thing in this entire document that lets us print a measured number on the box.

**Would I reach for it?** Honestly: I already sidechain. I have Trackspacer. The friction of routing a sidechain from the instrumental bus into a plugin on the vocal is the reason Neutron Unmask is under-used, and you wave that away as *"parity, not a new cost."* It isn't parity — it's the reason the incumbent feature is unpopular. Inheriting an unpopular workflow is not a neutral act.

**CONDITION TO PASS:**
1. Head-to-head bench against **Three-Body UNMASK (EXT Glue)** and **sonible learn:unmask** on a 20-song corpus. Metric: total instrumental gain reduction applied at matched ESTOI. **If we cannot show ≥40% less gain reduction at equal measured intelligibility, this is killed at the next gate.** No exceptions, no "it sounds better anyway."
2. The invented "~60% less gain reduction" figure in §3.2 is deleted from all documents *today*. You wrote a marketing number before you measured anything. That number will escape into a press release and then a reviewer will measure it.
3. Sidechain routing must auto-detect and auto-configure, or the module doesn't ship.

---

### 3.3 SEAM — Comp Welder / Take Matcher → **CONDITIONAL (but this is the one I most want)**

**Prior art you missed, and §3.3's justification paragraph is flatly false:**

You wrote: *"Match-EQ tools exist but are static, manual, one-region-at-a-time, and match spectrum only — not room decay, not noise floor."*

- **iZotope Dialogue Match** matches **EQ, reverb, AND ambience** between recordings. The reverb module is a neural network that estimates reflection density, decay time, colour and size from a reference and drives an Exponential Audio engine. iZotope ran MUSHRA tests against professional engineers and reported the human's and the network's ratings were *drawn from the same distribution* (p = 0.24). That is not "spectrum only" and it is not static.
- **Accentize Chameleon 2** — automatic reverb/room profile matching between recordings.
- **Accentize SpectralBalance 2** — learns a reference spectral signature and has a **Dynamic Mode that re-adapts the EQ curve over 50 times per second in real time**, explicitly targeting boxiness and proximity variation. That is continuous, not one-region-at-a-time.

**The finding you needed and didn't get: iZotope Dialogue Match is discontinued.** Its product page today reads *"This product is no longer available for purchase."* The closest existing product to SEAM — technically validated against human engineers, from the market leader, aimed at post-production where the problem is *more* acute and the budgets are *larger* — was withdrawn. Before one line of DSP is written, somebody explains to me why. Either it is our opening (wrong market, wrong price, wrong workflow) or it is the market telling us this is a feature people admire in a demo and do not buy.

**What actually survives, and it is worth a lot:** none of the above **auto-segments a comp**. Every one of them needs a human to say "this region, that reference." SEAM's actual invention is the **change-point detection + confidence-weighted median identity target + crossfaded per-segment correction** — i.e. *zero user input*. That is the whole value. Dialogue Match still needed an editor. If SEAM needs an editor, SEAM is Dialogue Match, and Dialogue Match is dead.

**Would I reach for it?** Every single song. This is the most expensive boring problem in my week and you are right about that. The workflow moment is precise: comp is locked, I'm about to start mixing, I hit analyse, I go make coffee, I come back and the punch-ins are gone.

**CONDITION TO PASS:**
1. **Zero-input operation on a real comp.** If the demo requires nominating a reference region, it's dead. Auto-target or nothing.
2. Written answer, before DSP starts, on why Dialogue Match was withdrawn.
3. Absorb DISTANCE LOCK into this module (see below).
4. The offline analysis pass must be genuinely background — analyse-while-you-work, not "please render and wait."

---

### 3.4 CONSONANT LOCK — Stack Aligner → **KILL**

You wrote: *"Zero plugins in this category work across tracks."* and *"Vocalign is the closest thing and it time-warps the whole signal to a guide, which flattens the performance and pitch-smears vowels."*

Both false, and the second one is out of date by a full major version.

- **VocAlign Pro 6** has a **Process Groups** function that adds multiple tracks to a group and processes them as a single operation. Sound On Sound's reviewer ran it on **a 21-track backing-vocal ensemble** — doubles, octave-downs, harmonies, choral ooohs — in one pass. That is precisely the "20 stacked vocals" demo you describe as our hero.
- VocAlign 6 has **SmartPitch modes** (unison vs. non-unison), **Protected Areas** to exclude regions from processing, user **Sync Points**, and independent formant shifting. It is no longer a blunt whole-signal warp.
- **Revoice Pro 5 (APT)** transfers timing, pitch, vibrato and level with **separate tightness controls per dimension** — that *is* your "lock at 70% and keep human width" strength knob, shipping today.
- Synchro Arts has twenty-plus years in this exact problem, deep patents, ARA integration in every major DAW, and universal pro adoption. **Sound Radix Auto-Align Post 2** covers the adjacent dynamic-alignment territory.

Here is the part that matters most: **the Round 1 doc contains the correct rule and then breaks it.** §4 kills a resonance suppressor with *"Soothe2 exists, is excellent, and is entrenched. Building a worse Soothe is a losing move."* Apply that sentence verbatim to VocAlign and you get the same answer. Instead the doc nominates this as the **hero demo** — the thing we put in front of press. We would be walking into a press demo where the obvious question is "how is this different from VocAlign?" and the honest answer is "it runs inside our plugin."

The delta — consonant-only warping, no guide render, no ARA — is a *convenience* delta on somebody else's mature product, purchased with the most expensive engineering in the document (multi-instance linking, cross-DAW, a permanent support burden). That is the worst ratio in the set.

**KILLED as an invention and as the hero demo.** It may return, later, only as an unbranded "tighten stack" mode on a group bus, and it may never appear in marketing as something new.

---

### 3.5 EFFORT — Vocal Effort Morph → **CONDITIONAL PASS (R&D only, off the roadmap, off the box)**

I searched hard and I could not find prior art. Formant shifters (zplane Élastique Pitch, Minimal Audio Formant, Waves Vocal Bender), vocal-tract modellers (Antares THROAT), transformers (Baby Audio Humanoid), personas (Nectar Backer) — all of them change *who* or *what timbre*. **None of them change how hard the singer sounds like they are working, independent of level.** This is the only genuinely novel idea in the document, and it is the only one that would change how records get made rather than how fast they get mixed.

**Would I reach for it?** Unambiguously yes, and I'd pay on its own. The 2 a.m. last-chorus problem is universal and currently unfixable.

**Honesty flags:**
1. **The pitch overclaims and must be rewritten.** "A tired 2 a.m. last chorus sounds like the singer went for it" — no. Effort lives in timbre *and* in timing, attack, pitch commitment and intention. We can move the timbre. We cannot manufacture conviction. Market it as **effort timbre**, never as performance. If we promise performance we get the exact review Backer got.
2. You correctly identify this as Backer's graveyard. Then §5 puts it in "parallel R&D." Good. Hold that line against every product manager who sees the demo and wants it on the box.
3. **Collision risk with DISTANCE LOCK — this is a real technical objection and nobody has flagged it.** EFFORT estimates effort from spectral tilt, F1 and HNR. DISTANCE LOCK estimates mic distance from LF shelf slope and HF tilt. **These are the same features.** And they are physically confounded in the worst possible way: a singer who pushes harder *also backs off the mic*, so LF drops and HF rises from both causes simultaneously. Two independent estimators reading the same evidence and attributing it to different causes will fight, oscillate, and produce a wandering artefact that nobody will be able to debug. This must be **one joint estimator that decomposes source effort and channel distance together**, or both modules are unshippable together. Solve this on paper before either one gets funded.

**CONDITION:** blind test — ten working engineers, processed vs. genuinely re-tracked takes. If more than 2 in 10 correctly identify the processed take, it does not ship and it is never mentioned publicly. No announcement, no teaser, no NAMM demo until that test passes.

---

### 3.6 DISTANCE LOCK — Proximity Normalizer → **KILL AS A MODULE / MERGE INTO SEAM**

**Prior art:**
- **Accentize SpectralBalance 2** — real-time Dynamic Mode, >50 curve updates per second, learns a reference profile, and the vendor explicitly names **"boxiness, proximity issues"** and mic-positioning-induced tonal variation as its targets. That is time-varying inverse rendering of mic-position error, shipping now.
- **Townsend Labs / UA Sphere DLX** — post-recording **Proximity / Prox EQ** and **Axis** (off-axis) controls. Requires their mic and is a static knob, but the "fix proximity after the fact, it's physics" position is taken and well known.

**Honesty flag:** *"Renders every word as if the singer never moved off the microphone"* is an overclaim I would not let past legal. You cannot recover off-axis high frequencies the capsule never captured, and you cannot un-mix direct from room. This is a time-varying shelf plus a direct/room rebalance. It is a good time-varying shelf. It is a filter with a physics story attached, and the doc's own §4 refuses ideas that are "a filter with a fancy name" — apply the rule consistently.

**The structural reason it dies as a module:** SEAM and DISTANCE LOCK solve *the same complaint* ("the chorus vocal sounds different") with *the same class of processing* (time-varying spectral + direct/room correction) driven by *the same features*. Shipping both means two analysers, two correction filters stacked in series fighting each other, twice the CPU, twice the UI, and a user who has to understand which one to reach for. That is a product-architecture error, and it is exactly how channel strips bloat into the CPU-heavy complaint we're attacking Nectar for.

**One module. One promise: "one voice, one distance, one room."** The proximity physics and the capsule presets are good work and they become SEAM's within-segment correction layer.

---

### 3.7 RESPIRE — Breath Choreographer → **PASS**

The only clean pass in the document. It is also the idea the doc rates lowest intellectually, which is usually how this goes.

**One correction to the justification, and fix it before marketing sees it.** You wrote: *"Nobody has framed breaths as a creative element with a mixer strip."* **Waves DeBreath** has always split the signal into a **Vocal path and a Breath path** with independent monitoring, and its own manual documents duplicating the track to process the breath path separately — i.e. the "breath send bus" is a *documented Waves workflow from roughly 2005*. You called the breath-bus routing "the novel bit." It is the least novel bit.

**What is genuinely absent from every product I could find, including DeBreath, Nectar 4 Breath Control and RX:** they all only *attenuate* by a fixed reduction amount. **Nobody normalizes each breath to a target level relative to its own adjacent phrase, held to ±2 dB across a whole song.** That is the invention, it's cheap, it's low-risk, it's audible instantly, and it fixes the thing everyone hates (gated-breath machine tell) without any resynthesis risk.

**Would I reach for it?** Yes, on every ballad and every intimate pop record, and I currently do it by hand with clip gain over 40 breaths a song.

**Sell the consistency, not the send bus.** Headline: *"every breath, the same size, all record long."* If we headline the send bus, a reviewer opens the DeBreath manual and we look like we didn't do our homework.

---

### 3.8 GESTURE — Pitch Contour Sculptor → **KILL**

The doc already half-kills it and ranks it 8/8. I'm finishing the job.

- **Revoice Pro 5** ships a new **Shaper Tool for pitch and level curves**, dedicated **vibrato editing**, SmartPitch and enhanced pitch editing. That covers transition shape, vibrato and phrase-level contour today.
- **Melodyne** has per-note pitch modulation and pitch drift (you acknowledge this).
- **Auto-Tune Pro X** has Flex-Tune, Humanize and Natural Vibrato.

The remaining delta is a **naming layer** — calling existing curve edits "Transition Decisiveness" and "Scoop Depth." That is a UI reskin of shipping controls, on top of the highest-artefact-risk resynthesis in the document, in a category owned by two entrenched vendors with bundled-Melodyne distribution (Nectar 4 *ships* Melodyne 5 Essential — we would be competing with something our competitor gives away free in the box).

And the practical objection: doing this properly requires offline note segmentation, which makes it an ARA editor, which is a **different product** with a different UI, a different QA surface and a different buyer. It does not belong in a channel strip.

**KILL.** Do not revisit.

---

## 2. VERDICT TABLE

| # | Effect | Verdict | One-line reason |
|---|---|---|---|
| 3.7 | **RESPIRE** | **PASS** | Only unchallenged gap (per-breath normalization); cheap, low-risk, instantly audible. Reframe the pitch — DeBreath already has the breath bus. |
| 3.3 | **SEAM** | **CONDITIONAL** | Biggest real pain, but Dialogue Match / Chameleon 2 / SpectralBalance 2 exist — and Dialogue Match was **discontinued**. Auto-segmentation is the only invention; zero-input or dead. |
| 3.1 | **DICTION** | **CONDITIONAL** | Real gap (general CVR engine), but Waves Sibilance owns the resynthesis claim and Physion owns the stream split. Must be one auto-set knob and must win in-mix, not solo. |
| 3.5 | **EFFORT** | **CONDITIONAL — R&D only** | The one true invention. Off the box, off the roadmap, no public mention until it passes a 10-engineer blind test. Must share an estimator with distance or it oscillates. |
| 3.2 | **ARBITER** | **CONDITIONAL — expect death** | Three-Body **UNMASK EXT Glue** ($59) already does masking-model cross-signal ducking; sonible learn:unmask ($69) too. Only SII weighting + ESTOI target survive. Bench or die. |
| 3.6 | **DISTANCE LOCK** | **KILL / MERGE** | Accentize SpectralBalance 2 (dynamic, proximity-aware) + UA Sphere DLX Proximity/Axis. Same problem and same features as SEAM — merge, don't duplicate. |
| 3.4 | **CONSONANT LOCK** | **KILL** | **VocAlign Pro 6 Process Groups** aligned a 21-track BGV stack in one pass (SOS); Revoice Pro APT has per-dimension tightness. This is "building a worse Soothe" — the doc's own rule, ignored. |
| 3.8 | **GESTURE** | **KILL** | Revoice Pro 5 Shaper + vibrato editing, Melodyne drift/modulation, Auto-Tune Humanize. A naming layer over shipping controls, and Nectar bundles Melodyne free. |

---

## 3. THE THREE I LET THROUGH

**SEAM (with DISTANCE LOCK absorbed), RESPIRE, DICTION.**

Rationale: all three apply to 100% of vocals, all three can be **fully auto-driven** (which is the only way to beat Nectar with the buyer who actually pays), and all three carry low artefact risk. I dropped the doc's pick of ARBITER because a $59 plugin took its central claim this year, and promoted RESPIRE because it is the only module in the set with no serious challenger, the shortest path to a shipping demo, and the best love-per-engineering-hour in the document.

**EFFORT is not one of the three.** It is the only real invention here and it is precisely why it cannot be a shipping commitment. It runs in a locked room and it gets announced when it's clean, or never.

---

## 4. WHAT IS STILL MISSING TO BEAT NECTAR 4

The Round 1 doc analyses the *category's* blind spots correctly and then completely fails to address *the buyer's* decision. Nectar 4's selling point is not its 13 modules. It is **Vocal Assistant: one click, sounds decent, done.** That is what the money buys. Against that, here is what we do not have:

**1. An Assistant that beats theirs. This is the entire product and it is not in the document.**
Eight clever modules with no auto-driver loses to Nectar for the person who pays. The phoneme classifier's highest-value application is not DICTION — it is **making the Assistant itself phoneme-aware**, so the auto-set chain knows an /s/ from a vowel from an inhale. That is a one-click experience nobody can currently match, and it is described nowhere. Reframe: the classifier drives the *Assistant*; the modules are how we prove it.

**2. The boring channel strip.**
Nectar has EQ, comp, de-ess, gate, saturation, pitch, auto-level, breath, harmony, reverb, delay, dimension. If we ship three clever modules and no strip, we are a $49 utility that requires the customer to *also own Nectar*. Nobody replaces their vocal chain with a supplement. We need the full strip and it needs to be competent, or we are permanently an add-on.

**3. Ducked reverb and delay — put it back.**
§4 kills "Tail Traffic Control" for being unoriginal. **Originality is not the buying criterion.** It is the single documented, in-print weakness of Nectar 4's effects section (MusicTech confirmed no internal ducking), it is a checkbox every reviewer will name in a comparison table, and it costs a fortnight. Ship it. Don't call it an invention; just have it.

**4. A reason to switch, not a reason to add.**
Every surviving module is *additive* — it sits alongside what the buyer owns. Nothing in this document makes anyone uninstall anything. That is a $79 impulse purchase, not a $249 flagship. Find the one thing that makes an engineer delete a plugin from their template, and lead with that.

**5. Measurement infrastructure — we are claiming numbers we have no way to produce.**
The doc's strongest strategic idea is making *measured* claims (CVR in dB, ESTOI, GR-per-unit-intelligibility) that iZotope cannot answer. There is no test corpus, no listening-test protocol, no baseline measurements, and no budget for any of it. Meanwhile §3.2 already contains an invented "~60% less gain reduction." Build the measurement rig **first**. The first reviewer who measures a claim and gets a null result ends the product.

**6. CPU, latency and price position.**
Nectar's other documented weaknesses are CPU load and upgrade price. Our stack — phoneme classifier, source-filter resynthesis, masking model, offline analysis pass, multi-instance links — is *heavier* than Nectar's, and nothing in the document commits to being lighter or cheaper. If we are more expensive and more CPU-hungry, we have handed the reviewer their conclusion. Commit to hard numbers on both, now, as design constraints.

**7. Melodyne.**
Nectar 4 Advanced ships **Melodyne 5 Essential** in the box. We ship nothing. Either license something of comparable perceived value or accept that our box looks emptier on the comparison chart every buyer reads.

**8. Harmony generation.**
Voices/Backer are weak, and you're right about Backer. But harmony generation is what people *demo*, and demoing is what sells channel strips. We have no answer at any quality level.

---

## 5. STANDING ORDERS

- Delete every "nothing on the market does this" sentence from every document until it has been re-verified against a named product list. Six of eight were wrong. That failure rate, in a launch deck, is a company-level credibility event.
- Delete the invented "~60% less gain reduction" figure today.
- Rewrite the DICTION ("no harshness"), DISTANCE LOCK ("as if the singer never moved") and EFFORT ("sounds like they went for it") pitches to claims we can defend in a blind test.
- Stop describing the phoneme classifier as a moat. It is a head start. The moat, if we get one, is the auto-driven Assistant built on top of it plus the measurement corpus behind the numbers.
- Answer, in writing, why iZotope discontinued Dialogue Match before SEAM gets a line of code.
- Resolve the EFFORT / DISTANCE joint-estimation collision on paper before either is funded.

**Nothing advances to Round 3 until the ARBITER bench-off and the SEAM auto-segmentation demo exist.**
