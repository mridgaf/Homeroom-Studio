# Tony Tone — Drums

**Sounds like:** A$AP Rocky — "Tony Tone" from *Testing* (2018)
**Genre tag:** Hip-Hop / East Coast Boom-Bap Revivalism
**Accuracy:** B+ (80–85%)
**Status:** Theoretical — test and report back
**Source assumed:** Kong drum samples from Reason factory ReFill plus optional vinyl-style sample loading. No external samples required.

---

## What you're actually building

This is NOT the punchy electro hip-hop sound from "On to the Next One." "Tony Tone" goes the opposite direction — intentionally **dusty, lo-fi, sample-based East Coast boom-bap** that pays homage to late-80s/early-90s NY hip-hop (Salt-N-Pepa era). The source sample is The Roger Webb Sound's "Man Inside," a 1970s library track. The drum aesthetic mimics MPC-style programming with vinyl crackle, lo-fi grit, and gentle swing.

Three things define this sound:
1. **Dusty character** — drums sound like they're sampled off vinyl, not crisp recordings
2. **Swing/groove timing** — not perfectly quantized
3. **Tight, dry mix** — minimal reverb, drums sit forward and dry

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
- Pitch: -1 semitone (a touch lower for weight)
- Decay: medium-short — around 11 o'clock (longer than electro, shorter than rock)
- Tone: 12 o'clock (neutral)
- Level: -5 dB output

**MClass Equalizer (kick channel insert)**
- Low Shelf: +2 dB at 70 Hz (warmth, not sub)
- LO Mid: cut -2 dB at 250 Hz, Q 1.0 (subtle mud reduction — NOT aggressive)
- HI Mid: boost +2 dB at 1.8 kHz, Q 1.0 (gentle thump, NOT click)
- High Shelf: cut -3 dB at 8 kHz (rolls off air — this is the "dusty" move)

**Scream 4 (kick channel insert)**
- Damage Control: 18 (subtle)
- Damage Type: **TAPE**
- P1 (Tape Speed): 30
- P2 (Tape Comp): 75 (heavy tape compression = vintage character)
- Cut Lo: 50
- Cut Mid: 50
- Cut Hi: 30 (rolls high end further — dusty)
- Master: 0

---

### SNARE

**Kong — NN-Nano slot**
- Load: a sampled/dusty-style snare — body and crack, not modern crispness
  - First choice: `Kong Kit Patches > Acoustic Kits > "Vintage Kit"` snare
  - Alternative: `Drum Samples > Snare > "Snare Acoustic 04"` or `"Snare Vinyl 02"`
  - Look for snares with low-mid weight and a slightly grainy top — NOT the crisp electronic snares
- Pitch: -2 semitones (deeper, vintage feel)
- Decay: ~10 o'clock (short-ish but not snappy)
- Level: -4 dB output

**MClass Equalizer (snare channel insert)**
- Low Shelf: cut -4 dB at 100 Hz (clears kick space, but less aggressively than modern hip-hop)
- LO Mid: boost +2 dB at 200 Hz, Q 1.2 (body and weight — this is the boom-bap snare signature)
- HI Mid: boost +3 dB at 3 kHz, Q 1.4 (presence, NOT modern 4-5 kHz crack)
- High Shelf: cut -2 dB at 10 kHz (rolls air, adds dust)

**MClass Compressor (snare channel insert)**
- Threshold: -16 dB
- Ratio: 3:1
- Attack: 10 ms (lets the transient through)
- Release: 150 ms (longer release than electro — natural sustain)
- Output gain: +2 dB
- Peak/RMS: RMS

**Scream 4 (snare channel insert)**
- Damage Control: 22
- Damage Type: **TAPE**
- P1 (Tape Speed): 35
- P2 (Tape Comp): 70
- Cut Lo: 50
- Cut Mid: 50
- Cut Hi: 35
- Master: 0

---

### HATS

**Kong — NN-Nano slot**
- Load: closed hi-hat with vintage character
  - First choice: `Drum Samples > Hi-Hat > "HH Closed Acoustic 02"` or `"HH Vinyl"`
  - Avoid bright, modern hats
- Pitch: 0
- Decay: short — 9 o'clock
- Level: -8 dB output (hats should sit BEHIND the kick and snare, not in front)

**MClass Equalizer (hat channel insert)**
- Low Shelf: cut -10 dB at 250 Hz (steep — hats need no low end)
- HI Mid: cut -2 dB at 4 kHz (tames any harshness)
- High Shelf: cut -3 dB at 12 kHz (THIS is the boom-bap hat move — kill the air, keep them dusty)

**Important rhythm note:** Don't play hats on every 16th. Boom-bap hats typically hit on 8ths with occasional 16th-note rolls. Less is more. Some bars should have no hats at all.

---

### DRUM BUS (group channel for kick + snare + hats)

**Scream 4 (group insert)**
- Damage Control: 15 (very subtle — this is the "vinyl glue")
- Damage Type: **TAPE**
- P1 (Tape Speed): 40
- P2 (Tape Comp): 65
- Cut Lo: 50
- Cut Mid: 50
- Cut Hi: 45
- Master: 0

**MClass Compressor (group insert, after Scream)**
- Threshold: -12 dB
- Ratio: 3:1 (slightly more aggressive than electro — boom-bap drums get glued harder)
- Attack: 20 ms
- Release: 150 ms
- Output gain: +3 dB
- Gain reduction target: 3–5 dB on hits

**MClass Equalizer (group insert, last)**
- Low Shelf: +1 dB at 60 Hz (subtle final weight)
- LO Mid: cut -1 dB at 400 Hz (final mud cleanup)
- High Shelf: cut -2 dB at 10 kHz (final dust — the high shelf cut is the signature)

**Channel strip Drive (group's mixer channel)**
- Drive: 12–18%

---

## Why this works

The "dust" comes from three coordinated moves: **rolling off the top end** (high shelf cuts on every element + group), **tape saturation everywhere** (Scream 4 on individual elements AND the bus, gentle but cumulative), and **mid-forward EQ** (boosts at 1.8 kHz on kick, 200 Hz and 3 kHz on snare — vintage frequencies, not modern crack). Compression is gluier and longer-release than electro drums because boom-bap drums need to *breathe* and groove, not punch.

## Order of operations note

EQ before saturation on individual elements so the saturator hears shaped frequencies. Scream 4 LAST on bus (well, before final EQ) because that's where the cumulative tape character glues everything into one cohesive vintage sound. Bus compression after the saturation glue, EQ as final polish — standard top-down approach.

## Reason-specific tricks

1. **Quantize loosely.** Don't snap drums to grid 100%. Reason's piano roll has a **Q Strength** setting (under quantize options) — set to 75–85% instead of 100%. This preserves micro-timing variations that give boom-bap its swing. Alternatively, manually nudge snares 5–15 ticks late for a behind-the-beat feel.

2. **Apply Shuffle.** In the sequencer Transport panel, there's a **Shuffle** knob (sometimes labeled "Groove"). Set to 55–60% (subtle swing on 16ths). This is the single biggest difference between programmed boom-bap and modern trap-style drums.

3. **The Combinator move.** Wrap the drum bus chain (Scream → Comp → EQ) into a Combinator 2 patch called "Dusty Bus." Macro 1 controls Scream 4 Damage Control (more/less dust). Macro 2 controls Bus Comp Threshold (more/less glue). One Combinator you can drop on any drum bus to instantly age it.

4. **Vinyl crackle — optional but recommended.** Load a vinyl noise sample loop into NN-XT on its own channel, run it under the drums at -25 to -30 dB. There's no factory vinyl noise in Reason, but free vinyl noise samples are everywhere (search "vinyl crackle loop free"). This pushes accuracy from B+ to A.

## RE upgrade path

This recipe is solid at B+. To push toward A:

- **Softube Saturation Knob** (free with Reason) — try in parallel with Scream 4 on the bus, "Keep High" mode at 30%. Adds harmonic warmth Scream misses.
- **Kuassa Amplifikation Vermillion** ($49) — tube saturation that nails the vintage character better than Scream 4. Replace Scream 4 on the drum bus.
- **iZotope Vinyl** (free plugin, not RE — but VST works in Reason via Rack Extension VST host) — adds authentic vinyl crackle, wow/flutter, and aging. Single most impactful free addition for this sound.
- **Native Instruments Maschine** (separate hardware/software) — not Reason-specific, but if you build boom-bap regularly, dedicated MPC-style workflow tools are worth the investment.

## Technique you just learned

**Vintage/dusty drum processing.** Three transferable principles:

1. **High-shelf CUT, not boost.** Modern hip-hop drums boost the high shelf for "air" and "crispness." Vintage drums do the opposite — rolling off the top creates the sampled-off-vinyl character.
2. **Stack subtle tape saturation across the signal path.** One heavy Scream 4 sounds gross. Multiple gentle Screams (15–25 Damage on each element + the bus) sound like real tape.
3. **Loose quantize + shuffle = groove.** Boom-bap's swing isn't an effect, it's a timing choice. 75–85% quantize strength + 55–60% shuffle is the universal starting point.

This recipe transfers directly to any 90s East Coast hip-hop revival, lo-fi hip-hop (Nujabes / Lord Finesse / J Dilla territory), and modern producers paying homage to that era (Conway, Westside Gunn, Roc Marciano).

## Reference track

YouTube search: "A$AP Rocky Tony Tone official audio"
- 0:15 — drum intro before vocals; listen for the dusty character and behind-the-beat snare
- 1:00 — full mix; notice how dry the drums sit (almost no reverb)

A/B in detail. Listen specifically for: dust at the top end (no sparkle), snare's mid-weight at 200 Hz, kick that's warm but not subby.

---

## Honest flags

1. **The Salt-N-Pepa reference matters.** This recipe sounds *intentionally* like 1988-1991 hip-hop drum programming. If you A/B it against modern trap and think "this sounds old" — that's correct, it's supposed to. The sound is anachronistic by design.

2. **Quantize and shuffle are 50% of the sound.** You can dial all these settings perfectly and still miss the recipe if your timing is locked to a perfect grid. Spend more time on groove than on saturation. The dust is the polish; the swing is the foundation.

3. **The reason this is B+ and not A**: Reason's stock samples are clean modern recordings. Real boom-bap drums were sampled off vinyl breaks from 1970s funk records. Without access to actual vinyl-sourced drum samples (free packs from sites like Whosampled, Tracklib, or YouTube vinyl drum break collections), you're approximating the sound rather than nailing it. Loading authentic sampled breaks into Kong/NN-XT would push this to A.

4. **Dr. Octo Rex alternative.** If you want to truly nail this aesthetic, find a 1970s funk drum break on YouTube (Roy Ayers, Bob James, Skull Snaps "It's a New Day" — the classic ones), load into Dr. Octo Rex, chop the loop, and trigger individual slices. That IS how this music was originally made. Settings above still apply.

5. Tagged **Theoretical** — built from production analysis, not session verification. Test, A/B, report back.
