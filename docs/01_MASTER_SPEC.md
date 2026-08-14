# 01 — MASTER SPEC: the effect shortlist

Written 2026-08-14. This is the synthesis that was owed from the adversarial
design workflow and never got written. Sources: `design_process/round1_producer.md`
(8 candidate effects) and `design_process/round2_adv_producer.md` (the hostile
review that killed three and put conditions on the rest).

**You pick 3. Nothing gets built until you do.**

---

## Read this first — it changes what you should pick

The adversarial reviewer was reviewing **a plugin someone is going to sell**.
Their verdicts turn on things that don't apply to you: is there prior art, is
there a $59 competitor, will a reviewer catch us overclaiming, can we win a
blind test with ten working mixers.

You are not launching a product. You are building a tool to make your own
vocals sound right.

So the reviewer's rankings are **not** your rankings. "A $59 plugin already
does this" is a reason not to sell it. It is not a reason not to have it —
you don't own that plugin, and it doesn't run in your chain. What you should
actually weigh: does it fix a problem I have, and can it be built cleanly.

Both columns below are given, separately.

---

## The five survivors

### RESPIRE — breath shaper
**What it does:** finds every breath and sets it to the same size — a fixed
number of dB under the singing around it, held within ±2 dB across the whole
song. Doesn't remove them. Can also send just the breaths to their own reverb.

**The problem it fixes:** breaths that jump from inaudible to enormous
take-to-take, and gated breaths, which are the #1 sign a vocal was machined.

**Reviewer verdict:** PASS — the only clean pass in the whole document. Nobody
else normalizes each breath against its own neighbouring phrase; they only
turn breaths down by a fixed amount.

| | |
|---|---|
| Build cost | **Lowest of the five.** Detection is easy — a breath is broadband, unpitched, 150–400 ms. [inferred from the producer doc's own description; not separately costed by the engineer] |
| Survives the JUCE port | **Yes.** No ML, no resynthesis, no whole-file pass needed. |
| Risk of wrecking your vocal | **Very low.** It only changes gain on regions it flagged. Worst case it misses a breath. |

---

### DICTION — consonant vs vowel balance
**What it does:** separates the consonants from the vowels and lets you turn
the consonants up on their own. The words get clearer without the vocal
getting brighter or harsher.

**The problem it fixes:** a mumbly or dense delivery where you'd normally
reach for a 3 kHz boost — and then the vowels turn to razor blades.

**Reviewer verdict:** CONDITIONAL. The general consonant rebalancer is a real
gap. But two claims in the pitch were false — Waves Sibilance already does
sibilant resynthesis, Eventide Physion already does the stream split. And an
honest warning: **turning up consonants can itself sound harsh** (a +6 dB /ʃ/
at 6–9 kHz is harsh), and it fights your de-esser, which is downstream pulling
the same sounds back down. That conflict has to be solved inside the module,
not left to you.

| | |
|---|---|
| Build cost | **Highest of the five.** Needs a phoneme-class classifier (6–8 classes) plus a harmonic/noise split. [inferred] |
| Survives the JUCE port | **Partly.** The DSP does; the classifier means shipping a model, which is a whole second track of work. |
| Risk of wrecking your vocal | **Medium.** A misclassified frame must cost ≤1 dB, not make a noise. Must be silent at 0%. |

---

### SEAM — comp welder (with DISTANCE LOCK folded in)
**What it does:** finds where a comped vocal changes character — punch-ins,
different days, different distance from the mic — and morphs every region
toward one sound. Tone, room, and noise floor, not just EQ. Zero input from
you: no picking a reference region.

**The problem it fixes:** "the chorus vocal sounds different." The flown-in
line. The verse you re-sang three weeks later.

**Reviewer verdict:** CONDITIONAL, and the one they most wanted. Two things
to know: (1) the auto-segmentation is the *entire* invention — every existing
tool makes a human nominate the reference. (2) iZotope built the closest
thing, Dialogue Match, validated it against human engineers, and then
**discontinued it.** The reviewer demanded a written explanation of why before
any code gets written. For a personal tool that's a curiosity, not a gate.

| | |
|---|---|
| Build cost | **High**, and the most awkward shape — needs the whole file, so it's an offline analysis pass. |
| Survives the JUCE port | **Awkward.** Whole-file analysis doesn't fit a real-time plugin cleanly. Fine for Phase 1 Python. |
| Risk of wrecking your vocal | **Medium.** It's morphing tone across the whole take. A bad identity target degrades everything at once. |

---

### EFFORT — how hard the singer sounds like they're trying
**What it does:** separates *how hard you sound like you're pushing* from *how
loud you are*. Turn it up and a tired last-chorus take sounds like you went
for it. Turn it down and an over-belted verse gets intimate without dropping
in the mix.

**Reviewer verdict:** CONDITIONAL — R&D only, off the roadmap. This is the
finding worth reading twice: **they searched for prior art and found none.**
It is the only genuinely novel idea in the whole document. It is also the
riskiest — it's resynthesis of the voice, which is exactly where iZotope's
Backer got called "robotic" with "artefacts and glitches" in print.

Two hard notes: it can move the *timbre* of effort, it cannot manufacture
conviction — timing and pitch commitment are effort too. And it reads the
**same features** as the distance estimator (spectral tilt, HF/LF balance),
which are physically confounded — a singer who pushes harder also backs off
the mic. If both exist as separate estimators they will fight and wander.
One joint estimator, or neither.

| | |
|---|---|
| Build cost | **Highest and least predictable.** Source-filter separation and resynthesis. |
| Survives the JUCE port | **Unknown.** Depends entirely on what the approach turns out to be. |
| Risk of wrecking your vocal | **High.** If it's 80% clean it's unusable. This is the one that either sounds magic or sounds broken. |

---

### ARBITER — duck the beat only where the words get buried
**What it does:** instead of ducking your beat everywhere the vocal is loud,
it works out where the beat is actually *masking* the vocal and ducks only
there — mostly on quiet consonants, which is where lyrics get lost. Much less
pumping for the same clarity.

**Reviewer verdict:** CONDITIONAL — "expect death." A $59 plugin (Three-Body
UNMASK) shipped this exact architecture this year, and sonible has one too.
The pitch's central claim — the whole category gets this wrong — stopped being
true. What survives is narrow but real: weighting the ducking toward 1–4 kHz
where words live, and setting a target *result* (an intelligibility score)
instead of a threshold.

Note for you specifically: this needs a sidechain feed from the instrumental,
which is friction in a plugin — but you already have the beat as a separate
file, so it's just a second input. **The friction that killed it commercially
mostly doesn't apply to you.**

| | |
|---|---|
| Build cost | **Medium.** Psychoacoustic masking model, no ML required. [inferred] |
| Survives the JUCE port | **Yes**, but needs sidechain routing. |
| Risk of wrecking your vocal | **Low** — it doesn't touch the vocal at all. It touches the beat. |

---

## Killed — for the record, don't revisit

| Effect | Why |
|---|---|
| **CONSONANT LOCK** (align 20 stacked vocals) | VocAlign Pro 6's Process Groups aligned a 21-track backing-vocal stack in one pass. Building a worse VocAlign. |
| **GESTURE** (edit pitch gestures, scoops, vibrato) | Revoice Pro 5 and Melodyne already do it, and Nectar ships Melodyne free in the box. Also the highest artefact risk. |
| **DISTANCE LOCK** (as its own module) | Not killed — **merged into SEAM.** Same problem, same features, same class of processing. Two of them stacked in series would fight. |

---

## What the reviewer says you're missing regardless of which 3 you pick

Reproduced because they're right and they're cheap:

1. **Ducked reverb and delay.** Nectar 4 has none — it's their one documented
   in-print weakness. Not an invention; just have it.
2. **Measure before claiming.** The Round 1 doc invented a "~60% less gain
   reduction" figure before measuring anything. Delete numbers you haven't
   measured. This matches the project's existing ground rule.
3. **Six of eight "nothing on the market does this" claims were factually
   wrong.** Don't write that sentence again without checking a named product.

---

## Your decision

Pick 3. If it helps, the two axes pull in different directions:

- **Lowest risk, fastest to something you can hear:** RESPIRE, then ARBITER.
- **Fixes the most annoying problem:** SEAM.
- **Only genuinely new thing here:** EFFORT — and the most likely to sound broken.

I'm not picking for you. Tell me the three and I'll spec them properly.
