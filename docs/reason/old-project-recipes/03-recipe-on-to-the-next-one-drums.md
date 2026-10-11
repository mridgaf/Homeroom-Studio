> Copied 2026-10-11 from the claude.ai "Reason 12" chat "Reason 12 production guide project" (2026-05-14).
> Status: THEORETICAL (as originally tagged). Original text below, unchanged except this note.
> CHECK BEFORE TRUSTING: Kong patch/sample names, and RE names/prices (Softube Tape Echoes, Sweetwater Sweet Driver, Polar Audio Vintage Drum Bus) were not verified.

# On to the Next One — Drums

**Sounds like:** Jay-Z & Swizz Beatz — "On to the Next One" (2009)
**Genre tag:** Hip-Hop
**Accuracy:** B (75–80%)
**Status:** Theoretical — test and report back
**Source assumed:** Kong drum samples from Reason factory ReFill; no external samples needed

---

## The Chain (per element)

**Kick:** Kong (NN-Nano sample player slot) → MClass Equalizer → MClass Compressor → Scream 4 → Channel strip
**Snare/Clap:** Kong (NN-Nano slot) → MClass Equalizer → MClass Compressor → RV7000 MkII (send) → Channel strip
**Drum bus (Mixer group channel):** MClass Compressor → MClass Equalizer → Channel strip Drive

---

## Settings

### KICK

**Kong — NN-Nano slot**
- Load: tight electro-style kick from factory soundbank
  - First choice: `Kong Kit Patches > Electronic Kits > "Electro Kit 1"` kick
  - Alternative: `Drum Samples > Kick > "Kick Electro 02"` or `"Kick Tight 04"`
- Pitch: -2 semitones (weight without going sub)
- Decay: short — around 9 o'clock
- Tone: 11 o'clock
- Level: -6 dB output

**MClass Equalizer (kick channel insert)**
- Low Shelf: ON, +3 dB at 80 Hz
- LO Mid (Parametric): cut -4 dB at 300 Hz, Q 1.0 (kills boxiness)
- HI Mid (Parametric): boost +4 dB at 2.5 kHz, Q 1.4 (the click/snap)
- High Shelf: OFF
- Loudness: OFF

**MClass Compressor (kick channel insert)**
- Threshold: -18 dB
- Ratio: 4:1
- Attack: 10 ms (lets the click through)
- Release: 80 ms
- Output gain: +2 dB
- Sidechain: OFF
- Peak/RMS: RMS

**Scream 4 (kick channel insert)**
- Damage Control: 25
- Damage Type: TAPE
- P1 (Tape Speed): 50
- P2 (Tape Comp): 60
- Cut Lo: 40
- Cut Mid: 50
- Cut Hi: 50
- Master: 0

Adds the slightly crunched, "pushed" character of Swizz's kick.

---

### SNARE / CLAP

**Kong — NN-Nano slot(s)**
- Best results from layering two pads:
  - Pad 1: `Drum Samples > Snare > "Snare Electro 03"`
  - Pad 2: `Drum Samples > Clap > "Clap 01"`
  - Trigger both on the 2 and 4
- Pitch on snare layer: 0
- Pitch on clap layer: +1 semitone
- Decay: snare ~10 o'clock, clap ~11 o'clock
- Level balance: clap slightly louder than snare

**MClass Equalizer (snare channel insert)**
- Low Shelf: cut -6 dB at 100 Hz (clears the kick's space)
- LO Mid: cut -3 dB at 400 Hz, Q 1.2 (removes muddy honk)
- HI Mid: boost +5 dB at 4 kHz, Q 1.0 (presence and crack)
- High Shelf: boost +2 dB at 10 kHz (air)

**MClass Compressor (snare channel insert)**
- Threshold: -15 dB
- Ratio: 3:1
- Attack: 5 ms
- Release: 100 ms
- Output gain: +2 dB

**RV7000 MkII (send via Mixer FX send, NOT insert)**
- Algorithm: Hall
- Decay: 1.8 seconds
- Predelay: 30 ms
- HF Damp: 60%
- Send amount on snare channel: -18 dB (subtle, room only)

---

### DRUM BUS (group channel for kick + snare + percussion)

**MClass Compressor (group insert)**
- Threshold: -12 dB
- Ratio: 2:1
- Attack: 15 ms (preserves transients)
- Release: 120 ms
- Output gain: +2 dB
- Gain reduction target: 2–3 dB on peaks (the "glue")

**MClass Equalizer (group insert, after comp)**
- Low Shelf: +1.5 dB at 60 Hz
- High Shelf: +1.5 dB at 12 kHz

**Channel strip Drive (group's mixer channel)**
- Drive knob: 15–20%

---

## Why this works

Swizz's drums on this track are short, punchy, and slightly distorted. The recipe replicates that with a tight kick (short decay), aggressive midrange EQ (2.5 kHz on kick, 4 kHz on snare for the late-2000s "snap"), tape saturation via Scream 4 for pushed/dirty character, and gentle bus compression to glue.

## Order of operations note

EQ before comp on individual elements so the compressor reacts to shaped sound, not raw mud. Scream 4 last on the kick because saturation after compression sounds tighter than before. Bus comp is gentle (2:1) so it glues without flattening.

## Reason-specific trick

Route kick and snare channels to a group channel in the SSL mixer (right-click channel → Group). All bus processing goes on that group. Use the channel strip's Drive knob on the group instead of inserting another saturator — free, sounds good, saves CPU.

## RE upgrade path

Scream 4's Tape mode gets 70% of the way to the Swizz crunch but is a bit harsh in upper mids. Options:
- Softube Saturation Knob (free with Reason) — try in place of Scream 4 on the kick, "Keep High" mode at 40%.
- Softube Tape Echoes ($99) or Kuassa Amplifikation Vermillion ($49) — closes C-grade saturation to A-grade. [unverified]
- For drum bus glue: Sweetwater Sweet Driver or Polar Audio Vintage Drum Bus ($49–79). [unverified]

## Technique you just learned

Short-decay electronic drums with mid-forward EQ and parallel saturation for bus glue. Transfers to any late-2000s/early-2010s electro hip-hop, EDM-rap crossover, or modern trap with electronic kicks. Cut boxy 300–400 Hz, boost 2.5–4 kHz for snap, saturate gently, glue with 2:1 bus comp.

## Reference track

YouTube search: "Jay-Z On to the Next One official audio"
- 0:15 — drums only before vocal enters
- 1:30 — full mix context
Listen for the kick's short decay and the snare's snap around 4 kHz.

---

## Honest flags

1. Reason's factory soundbank doesn't have a sample that exactly matches Swizz's kick. Best stock approximation is Kong electronic kits; closer matches come from free packs loaded into NN-XT or Kong. Settings above still apply — swap the source.
2. The Justice "D.A.N.C.E." sample carries most of the song's rhythmic top end. Drums alone sound emptier than expected when soloed. Judge the recipe in context of a full beat.
3. Tagged Theoretical: built from production analysis, not session verification.
4. Accuracy is B because Reason's stock saturation is the weakest link. EQ, compression, kit selection, routing are all A-grade. The Saturation Knob swap costs nothing and pushes this toward A.
