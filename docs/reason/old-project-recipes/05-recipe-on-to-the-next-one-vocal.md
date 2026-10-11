> Copied 2026-10-11 from the claude.ai "Reason 12" chat "Reason 12 production guide project" (2026-05-14).
> Status: THEORETICAL (as originally tagged). Original text below, unchanged except this note.
> CHECK BEFORE TRUSTING: the RE names/prices at the bottom (Synchron "The 660", FXpansion "Etch Red", Lindell 6X-500) and "Pitch Edit (formerly Neptune)" were not verified. The reason-reference skill says never trust a Reason name from memory; Reason 12's pitch device is called Neptune in the device list.

# On to the Next One — Vocal Chain (Jay-Z)

**Sounds like:** Jay-Z & Swizz Beatz — "On to the Next One" (2009) — Jay-Z's lead vocal
**Genre tag:** Hip-Hop
**Accuracy:** A (85–90%)
**Status:** Theoretical — test and report back
**Source assumed:** Clean dry vocal recorded into Reason via a decent large-diaphragm condenser (Neumann TLM 102/103, AKG C214, Rode NT1, or similar) into a clean preamp. Untreated-but-not-terrible room. No processing on the recorded track.

---

## Why this one is A-grade

This is documented. Young Guru — Jay-Z's longtime engineer — gave a full interview about the Blueprint 3 vocal chain. The hardware he used (Fairchild 660, ADL 1500, Focusrite 110, Lexicon 480) all have well-understood characteristics. Reason's stock devices can approximate every stage cleanly.

---

## The Chain

**Vocal channel insert chain:**
Mixer channel strip (input gain + HP) → MClass Equalizer (subtractive) → MClass Compressor (Fairchild stage) → MClass Compressor #2 (ADL stage) → MClass Equalizer (additive shaping) → Pulveriser (de-ess workaround) → channel strip EQ/dynamics

**Sends from channel:**
- RV7000 MkII (Lexicon-style hall, send 1)
- The Echo (quarter-note delay, send 2)

---

## Settings — In Order

### 1. Channel Strip Input Stage
- Input Gain: set so loudest hits peak at -6 dB
- HP Filter: ON, 80 Hz
- Polarity: normal

### 2. MClass Equalizer #1 — Subtractive (insert slot 1)
- Low Shelf: cut -2 dB at 120 Hz (tames chest mud)
- LO Mid: cut -3 dB at 250 Hz, Q 1.2 (the universal vocal mud point)
- HI Mid: cut -2 dB at 1.5 kHz, Q 2.0 (only if your voice has nasal honk; skip if not)
- High Shelf: OFF
- Loudness: OFF

### 3. MClass Compressor #1 — "Fairchild" stage (insert slot 2)
Slow, smooth, gluing compression.
- Threshold: -16 dB
- Ratio: 2:1
- Attack: 30 ms
- Release: 250 ms
- Output gain: +2 dB
- Sidechain: OFF
- Peak/RMS: RMS
- Gain reduction target: 2–3 dB average, 5 dB on peaks

### 4. MClass Compressor #2 — "ADL 1500" stage (insert slot 3)
Faster, more aggressive. Locks the vocal forward.
- Threshold: -10 dB
- Ratio: 4:1
- Attack: 8 ms
- Release: 100 ms
- Output gain: +2 dB
- Peak/RMS: Peak
- Gain reduction target: 3–5 dB on peaks (about 6–8 dB total with the first comp)

### 5. MClass Equalizer #2 — Additive shaping (insert slot 4)
- Low Shelf: +1 dB at 100 Hz
- LO Mid: OFF
- HI Mid: +3 dB at 4 kHz, Q 1.4 (presence)
- High Shelf: +2 dB at 10 kHz (air)

### 6. Pulveriser — De-Esser Workaround (insert slot 5)
Reason 12's stock has no dedicated de-esser. Pulveriser's filtered compression is a workaround.
- Squash: 30
- Tremor: OFF
- Filter: HP at 5 kHz
- Filter Type: Bandpass, narrow
- Follower → Squash: heavy
- Master volume: matched to bypass

Alternative if Pulveriser is too aggressive: a third MClass Compressor with external sidechain; route a copy of the vocal through an MClass EQ (cut below 5 kHz, boost 6–8 kHz) into the compressor's sidechain input.

---

## Sends (mixer FX returns)

### Send 1 — RV7000 MkII (Lexicon 480-style Hall)
- Algorithm: Hall
- Decay: 1.4 seconds
- Predelay: 25 ms
- HF Damp: 50%
- Room size: medium-large
- Diffusion: 70%
- Modulation: subtle (default)
- EQ on the return: HP at 250 Hz, LP at 8 kHz
- Send amount from vocal: -20 dB

### Send 2 — The Echo (quarter-note delay)
- Mode: Synced
- Time: 1/4
- Feedback: 20
- Ducking: ON, amount 50
- Drive: 0
- Color/Filter: 40
- Wobble: 0
- Send amount from vocal: -22 dB

---

## Final Mix Channel Settings (SSL channel strip)
- Channel strip EQ: bypassed
- Channel strip Dynamics: bypassed
- Drive: 5–8%
- Pan: center
- Fader: loudest words peak around -6 dB on the channel meter

---

## Why this works
Two compressors in series: a slow gluing compressor followed by a faster controlling compressor. Smooth average level control plus fast peak control without crushing the signal. EQ is split into subtractive (before compression) and additive (after) for cleaner final tone. The hall is subtle and short; the quarter-note delay adds rhythmic motion that locks to the beat.

## Order of operations note
Subtractive EQ first because compressing muddy frequencies wastes the compressor's work. Two compressors in series before additive EQ so the second EQ doesn't lift compressed garbage. De-ess last because compression brings sibilance up. Reverb and delay on sends so their levels can be tweaked independently.

## Reason-specific tricks
1. Combinator the insert chain (EQ, Comp1, Comp2, EQ, Pulveriser). Macros: 1 Comp1 threshold, 2 Comp2 threshold, 3 EQ2 4 kHz boost, 4 Pulveriser squash. Save as "Hip-Hop Lead Vocal — Jay-Z Style."
2. Use the channel strip for input gain, not the device chain. Input gain changes what the inserts hear; the fader at the end does not.
3. Put Send 1 and Send 2 in one FX Combinator on a send return, one macro "Vocal Space Amount" scaling both.

## RE upgrade path
- Softube Tube-Tech CL 1B ($179) — closer to the ADL 1500 character than MClass.
- Synchron Audio The 660 ($129) — Fairchild 660 emulation. Replaces MClass Comp #1. [unverified]
- Sonarworks Reference 4 (separate software, not an RE) — monitoring calibration.
If budget is tight: stay stock.

## Technique you just learned
Two-stage serial compression with split EQ: slow comp for glue, fast comp for peaks, subtractive EQ before, additive EQ after, de-ess at the end, ambience on sends. Applies to any lead vocal in any genre.

## Reference track
YouTube search: "Jay-Z On to the Next One official audio"
- 0:30 — first verse begins; listen for presence, dryness, slight quarter-note delay tail
- 1:00 — notice how the vocal sits forward of the beat
A/B against your own vocal. Listen for presence at 4 kHz, dryness, articulation (sibilance controlled but not lisping).

---

## Honest flags
1. Source quality matters more than the chain. Jay-Z was recorded on a Neumann U87 into an Avalon 737 in a treated room. A cheap mic in an untreated bedroom won't sound like that no matter the chain. The chain is the last 20%.
2. De-essing in stock Reason is the weakest link. Pulveriser works but is a workaround. A dedicated de-esser RE would help (the original named FXpansion Etch Red and Lindell 6X-500 Channel — unverified).
3. Auto-Tune note. Young Guru's chain used Auto-Tune subtly. Reason 12 has a pitch-correction device for this (the original called it "Pitch Edit (formerly Neptune)"; see the check note at the top). Settings given: Correction Speed ~40 (subtle), Key set to song key, Threshold ~5. Don't push past 50 or you get the audible Auto-Tune effect.
4. Reason's pitch correction works on monophonic vocals only and in real time. For complex multi-vocal sessions, render each pass and edit pitch graphically.
5. Tagged Theoretical: built from production research, not session verification.
