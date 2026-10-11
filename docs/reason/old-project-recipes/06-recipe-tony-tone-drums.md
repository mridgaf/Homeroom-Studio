> Copied 2026-10-11 from the claude.ai "Reason 12" chat "Reason 12 production guide project" (2026-05-14).
> Status: THEORETICAL (as originally tagged). Original text below, unchanged except this note.
> NOTE: this is the old project's file 06 (Tony Tone drums). A different file is also called "06" (kick/808 relationship) — the two numbering schemes collided.
> CHECK BEFORE TRUSTING: sample/patch names under Kong, the "Q Strength" and "Shuffle" control names, RE names/prices, and "VST works in Reason via a Rack Extension VST host" were not verified against Reason 12.

# Tony Tone — Drums

**Sounds like:** A$AP Rocky — "Tony Tone" from *Testing* (2018)
**Genre tag:** Hip-Hop / East Coast Boom-Bap Revivalism
**Accuracy:** B+ (80–85%)
**Status:** Theoretical — test and report back
**Source assumed:** Kong drum samples from Reason factory ReFill plus optional vinyl-style sample loading. No external samples required.

---

## What you're actually building

This is NOT the punchy electro hip-hop sound from "On to the Next One." "Tony Tone" goes the opposite direction — intentionally dusty, lo-fi, sample-based East Coast boom-bap that pays homage to late-80s/early-90s NY hip-hop (Salt-N-Pepa era). The source sample is The Roger Webb Sound's "Man Inside," a 1970s library track. The drum aesthetic mimics MPC-style programming with vinyl crackle, lo-fi grit, and gentle swing.

Three things define this sound:
1. Dusty character — drums sound sampled off vinyl, not crisp recordings
2. Swing/groove timing — not perfectly quantized
3. Tight, dry mix — minimal reverb, drums sit forward and dry

---

## The Chain (per element)

**Kick:** Kong (NN-Nano slot) → MClass Equalizer → Scream 4 (Tape mode, light) → Channel strip
**Snare:** Kong (NN-Nano slot) → MClass Equalizer → MClass Compressor → Scream 4 (Tape mode, light) → Channel strip
**Hats:** Kong (NN-Nano slot) → MClass Equalizer → Channel strip
**Drum bus:** Scream 4 (Tape, vinyl character) → MClass Compressor → MClass Equalizer → Channel strip Drive

---

## Settings

### KICK

**Kong — NN-Nano slot**
- Load: a vintage/sampled-style kick from the factory soundbank
  - First choice: `Kong Kit Patches > Acoustic Kits > "Vintage Kit"` kick
  - Alternative: `Drum Samples > Kick > "Kick Acoustic 03"` or `"Kick 909 Dusty"`
  - You want a kick with body but not modern punch — NO sub-heavy electro kicks
- Pitch: -1 semitone
- Decay: medium-short — around 11 o'clock
- Tone: 12 o'clock
- Level: -5 dB output

**MClass Equalizer (kick insert)**
- Low Shelf: +2 dB at 70 Hz (warmth, not sub)
- LO Mid: cut -2 dB at 250 Hz, Q 1.0 (subtle)
- HI Mid: boost +2 dB at 1.8 kHz, Q 1.0 (gentle thump, NOT click)
- High Shelf: cut -3 dB at 8 kHz (rolls off air — the "dusty" move)

**Scream 4 (kick insert)**
- Damage Control: 18
- Damage Type: TAPE
- P1 (Tape Speed): 30
- P2 (Tape Comp): 75
- Cut Lo: 50
- Cut Mid: 50
- Cut Hi: 30
- Master: 0

### SNARE

**Kong — NN-Nano slot**
- Load: a sampled/dusty-style snare — body and crack, not modern crispness
  - First choice: `Kong Kit Patches > Acoustic Kits > "Vintage Kit"` snare
  - Alternative: `Drum Samples > Snare > "Snare Acoustic 04"` or `"Snare Vinyl 02"`
  - Look for low-mid weight and a slightly grainy top
- Pitch: -2 semitones
- Decay: ~10 o'clock
- Level: -4 dB output

**MClass Equalizer (snare insert)**
- Low Shelf: cut -4 dB at 100 Hz
- LO Mid: boost +2 dB at 200 Hz, Q 1.2 (body — the boom-bap snare signature)
- HI Mid: boost +3 dB at 3 kHz, Q 1.4 (presence, NOT modern 4-5 kHz crack)
- High Shelf: cut -2 dB at 10 kHz

**MClass Compressor (snare insert)**
- Threshold: -16 dB
- Ratio: 3:1
- Attack: 10 ms
- Release: 150 ms
- Output gain: +2 dB
- Peak/RMS: RMS

**Scream 4 (snare insert)**
- Damage Control: 22
- Damage Type: TAPE
- P1 (Tape Speed): 35
- P2 (Tape Comp): 70
- Cut Lo: 50
- Cut Mid: 50
- Cut Hi: 35
- Master: 0

### HATS

**Kong — NN-Nano slot**
- Load: closed hi-hat with vintage character
  - First choice: `Drum Samples > Hi-Hat > "HH Closed Acoustic 02"` or `"HH Vinyl"`
  - Avoid bright, modern hats
- Pitch: 0
- Decay: short — 9 o'clock
- Level: -8 dB output (hats sit BEHIND kick and snare)

**MClass Equalizer (hat insert)**
- Low Shelf: cut -10 dB at 250 Hz
- HI Mid: cut -2 dB at 4 kHz
- High Shelf: cut -3 dB at 12 kHz (the boom-bap hat move — kill the air)

**Rhythm note:** Don't play hats on every 16th. Boom-bap hats typically hit on 8ths with occasional 16th rolls. Some bars should have no hats at all.

### DRUM BUS (group channel for kick + snare + hats)

**Scream 4 (group insert)**
- Damage Control: 15
- Damage Type: TAPE
- P1 (Tape Speed): 40
- P2 (Tape Comp): 65
- Cut Lo: 50
- Cut Mid: 50
- Cut Hi: 45
- Master: 0

**MClass Compressor (group insert, after Scream)**
- Threshold: -12 dB
- Ratio: 3:1
- Attack: 20 ms
- Release: 150 ms
- Output gain: +3 dB
- Gain reduction target: 3–5 dB on hits

**MClass Equalizer (group insert, last)**
- Low Shelf: +1 dB at 60 Hz
- LO Mid: cut -1 dB at 400 Hz
- High Shelf: cut -2 dB at 10 kHz (the signature)

**Channel strip Drive (group's mixer channel):** 12–18%

---

## Why this works

The "dust" comes from three coordinated moves: rolling off the top end (high shelf cuts on every element and the group), tape saturation everywhere (Scream 4 on individual elements AND the bus, gentle but cumulative), and mid-forward EQ (1.8 kHz on kick, 200 Hz and 3 kHz on snare). Compression is gluier and longer-release than electro drums because boom-bap drums need to breathe and groove.

## Order of operations note

EQ before saturation on individual elements so the saturator hears shaped frequencies. Scream 4 on the bus before the final EQ because that's where the cumulative tape character glues everything together. Bus compression after the saturation, EQ as final polish.

## Reason-specific tricks

1. Quantize loosely. Reason's piano roll quantize has a strength setting — set to 75–85% instead of 100%. Or nudge snares 5–15 ticks late for a behind-the-beat feel.
2. Apply shuffle. In the sequencer Transport panel there is a Shuffle/Groove control. Set to 55–60% (subtle swing on 16ths). This is the biggest difference between programmed boom-bap and modern trap-style drums.
3. Combinator: wrap the drum bus chain (Scream → Comp → EQ) in a Combinator 2 called "Dusty Bus." Macro 1 = Scream 4 Damage Control (more/less dust). Macro 2 = Bus Comp Threshold (more/less glue).
4. Vinyl crackle (optional): load a vinyl noise sample loop into NN-XT on its own channel, under the drums at -25 to -30 dB. There's no factory vinyl noise in Reason; free vinyl crackle loops are widely available. Pushes accuracy from B+ toward A.

## RE upgrade path

Solid at B+. To push toward A:
- Softube Saturation Knob (free with Reason) — parallel with Scream 4 on the bus, "Keep High" mode at 30%.
- Kuassa Amplifikation Vermillion ($49) — tube saturation; replace Scream 4 on the drum bus. [unverified]
- iZotope Vinyl (free plugin, not an RE) — vinyl crackle, wow/flutter. [the original claimed it works in Reason through a VST host RE — unverified]
- Native Instruments Maschine — not Reason-specific.

## Technique you just learned

Vintage/dusty drum processing. Three principles:
1. High-shelf CUT, not boost. Modern drums boost the high shelf for air; vintage drums roll off the top.
2. Stack subtle tape saturation across the signal path. One heavy Scream 4 sounds gross; multiple gentle ones (15–25 Damage on each element and the bus) sound like real tape.
3. Loose quantize + shuffle = groove. 75–85% quantize strength + 55–60% shuffle is the starting point.
Transfers to any 90s East Coast revival, lo-fi hip-hop, and producers paying homage to that era.

## Reference track

YouTube search: "A$AP Rocky Tony Tone official audio"
- 0:15 — drum intro before vocals; dusty character and behind-the-beat snare
- 1:00 — full mix; notice how dry the drums sit
Listen for: dust at the top end (no sparkle), the snare's mid-weight at 200 Hz, a kick that's warm but not subby.

---

## Honest flags

1. The Salt-N-Pepa reference matters. This recipe sounds intentionally like 1988–1991 hip-hop drum programming. If it sounds old next to modern trap, that's correct.
2. Quantize and shuffle are half the sound. Spend more time on groove than on saturation.
3. Why B+ and not A: Reason's stock samples are clean modern recordings. Real boom-bap drums were sampled off 1970s funk vinyl. Authentic sampled breaks loaded into Kong/NN-XT would push it to A.
4. Dr. Octo Rex alternative: find a 1970s funk drum break, load into Dr. Octo Rex, chop the loop, trigger individual slices. Settings above still apply. (The original suggested YouTube rips and named Roy Ayers, Bob James, Skull Snaps "It's a New Day." Mind licensing/sourcing.)
5. Tagged Theoretical: built from production analysis, not session verification.
