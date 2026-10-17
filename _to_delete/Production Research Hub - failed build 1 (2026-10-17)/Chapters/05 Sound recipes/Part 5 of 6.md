# Chapter 05: Sound recipes
## Part 5 of 6

_Every get-close recipe: hip-hop, rock, feelings, and the anti-recipes (what NOT to do)._

**In this part:**
- upfront-rap-vocal.md — Upfront Rap Vocal — modern dry rap chain
- driven-rock-bass.md — Driven Rock Bass — sounds like Royal Blood / Muse
- gated-snare-80s.md — 80s Gated Snare — sounds like Phil Collins / 80s rock
- gritty-rock-vocal.md — Gritty Rock Vocal — sounds like 90s alt-rock lead
- rock-mix-glue.md — Rock Mix Glue — master bus chain
- shoegaze-guitar-wall.md — Shoegaze Guitar Wall — sounds like MBV / Slowdive

(Next: Part 6 of 6)


=====================================================
SOURCE FILE: upfront-rap-vocal.md
ORIGINAL LOCATION: HS:recipes/hiphop/upfront-rap-vocal.md
=====================================================

---
name: Upfront Rap Vocal
book: hip-hop
sounds_like: modern rap vocal — dry, close, every word intelligible
accuracy: B
status: theoretical
source: condenser or SM7B, quiet room, rapper 4-6 inches off the mic
tags: vocal rap hip hop upfront dry compression delay throw
technique: serial compression — two compressors doing 3 dB each beat one doing 6
---
# Upfront Rap Vocal — modern dry rap chain

**Accuracy: B** — honest gap: stock Reason has no de-esser. If your source is sibilant, that's the weak link (fix below).

## The Chain
Channel strip (HPF + EQ + comp #1) → MClass Compressor (#2) → DDL-1 throw (send) → RV7000 tiny room (send)

## Steps
1. Channel strip HPF: 90 Hz. Rap vocals carry no useful info below that; the 808 owns it.
2. Channel EQ: cut 2 dB at 400 Hz (boxiness), boost 1.5 dB at 5 kHz (presence). Less is more — modern rap vocals are clean, not scooped.
3. Channel comp: ratio 3:1, medium attack, ~3 dB reduction. First stage catches phrases.
4. MClass Compressor: ratio 4:1, fast attack, another ~3 dB. Second stage catches syllables. Two gentle stages sound transparent; one 6 dB stage sounds squeezed.
5. De-ess workaround: MClass EQ between the comps, cut 3–4 dB at 6–8 kHz narrow Q, ONLY if esses hurt. Crude but stock. (Real fix: free VST3 de-esser — Techivation T-De-Esser, $0.)
6. DDL-1 on a send: 1/4 note sync, feedback ~25, pan it. Automate the send up on the last word of a line — the classic "throw".
7. RV7000 on a send: Room, decay 0.4 s, barely audible. Rap vocals read "dry" but a touch of room stops the sterile-booth feel.

## Why this works
Serial compression controls dynamics invisibly; the dryness keeps the voice in front of the beat instead of inside it.

## Order of operations
EQ cut before compression — otherwise the comps react to the 400 Hz mud you were going to remove anyway.

## Reason-specific trick
Automate the DDL-1 send in the sequencer lane rather than riding it live — draw a spike on the throw word. Perfectly repeatable.

## RE upgrade path
De-esser is the one real hole; free VST3 fills it. No RE purchase justified.

## Technique you just learned
Serial compression: split the workload across stages.

=====================================================
SOURCE FILE: driven-rock-bass.md
ORIGINAL LOCATION: HS:recipes/rock/driven-rock-bass.md
=====================================================

---
name: Driven Rock Bass
book: rock
sounds_like: Royal Blood / Muse — distorted bass that still has low end
accuracy: B
status: theoretical
source: DI electric bass or synth bass, clean
tags: bass distortion drive rock split parallel low end
technique: frequency-split processing — distort the mids, protect the sub
---
# Driven Rock Bass — sounds like Royal Blood / Muse

**Accuracy: B** — the split trick gets you most of the way; a real fuzz pedal and amp has hair stock Reason can't fully fake.

## The Chain
Spider Audio split → path A: MClass EQ (lows only) → path B: Scream 4 + MClass EQ (mids/highs only) → merge → channel comp

## Steps
1. Split the bass with a Spider Audio into two mix channels: "Bass Sub" and "Bass Dirt".
2. Bass Sub channel: MClass Equalizer, lo shelf OFF, use Lo Cut off; enable Param 1 as low-pass stand-in — cut everything above ~250 Hz (Param 1: freq 250, gain -inf style deep cut, wide Q). Keep this path CLEAN. No distortion ever.
3. Bass Dirt channel: MClass EQ hi-pass — cut below 250 Hz (Lo Cut ON, then Param 1 cut at 180 Hz, -12 dB, medium Q).
4. Bass Dirt: Scream 4 after the EQ. Damage type Distortion, Damage 55–70, P1 to taste. Body section ON, type B, for cab-ish resonance.
5. Balance: dirt path about equal level with sub path; the distortion should carry the character, the sub carries the weight.
6. Merge both to a bass bus channel; bus compressor ratio 4:1, ~3 dB reduction, to glue the two paths into one instrument.

## Why this works
Distortion destroys low frequencies (intermodulation mud); splitting first means the sub never touches the dirt.

## Order of operations
EQ BEFORE Scream on the dirt path — what you feed a distortion changes what comes out far more than EQ-ing after.

## Reason-specific trick
Combinator 2 the whole rig; map macro 1 to Scream Damage, macro 2 to dirt-path level. Save as "Driven Bass.cmb" — this is your first "Your Sound" patch.

## RE upgrade path
For A-grade: a dedicated bass amp sim RE (Kuassa Cerberus, ~$49) replaces step 4's cab approximation.

## Technique you just learned
Frequency-split (multiband) processing with Spiders — works for guitars, drum busses, anything.

=====================================================
SOURCE FILE: gated-snare-80s.md
ORIGINAL LOCATION: HS:recipes/rock/gated-snare-80s.md
=====================================================

---
name: 80s Gated Snare
book: rock
sounds_like: Phil Collins "In the Air Tonight" / 80s power ballads
accuracy: A
status: theoretical
source: any decent snare hit — sampled or acoustic
tags: snare drums gate reverb 80s huge gated
technique: gated reverb — huge without washing out the mix
---
# 80s Gated Snare — sounds like Phil Collins / 80s rock

**Accuracy: A** — this is one sound stock Reason genuinely nails, because RV7000 MkII has a built-in gate section. This is the textbook use for it.

## The Chain
Snare channel → RV7000 MkII (insert, not send) → channel strip EQ

## Steps
1. Insert RV7000 MkII directly on the snare channel (not as a send — you want the gate to chop the whole tail).
2. Algorithm: Hall. Decay 2.5–3 s. Size large. Predelay 0.
3. Press the GATE button on the RV7000. Open the gate section (Remote Programmer).
4. Gate: threshold so the gate opens only on hits; hold ~120–180 ms; release fast (under 50 ms). The abrupt cutoff IS the sound.
5. Dry/Wet around 45–55% — the snare crack must still lead.
6. Channel strip EQ after: boost 3 dB at 200 Hz for body, 2 dB shelf at 8 kHz for sizzle.

## Why this works
A huge reverb chopped mid-bloom reads as "massive room" without the tail eating the next beat.

## Order of operations
EQ after the reverb so you shape the combined sound, not just the dry hit.

## Reason-specific trick
The RV7000's gate can also be triggered by CV — run a Redrum channel's gate out into it and the reverb chops in rhythm even on sustained sources.

## RE upgrade path
None. Stock wins here.

## Technique you just learned
Gated reverb — and more broadly, that a reverb's envelope matters as much as its size.

=====================================================
SOURCE FILE: gritty-rock-vocal.md
ORIGINAL LOCATION: HS:recipes/rock/gritty-rock-vocal.md
=====================================================

---
name: Gritty Rock Vocal
book: rock
sounds_like: 90s alt-rock lead vocal (Foo Fighters / grunge era)
accuracy: B
status: theoretical
source: dynamic mic (SM7B/SM58-ish), untreated or semi-treated room
tags: vocal grit rock lead saturation parallel distortion
technique: parallel saturation — grit without destroying intelligibility
---
# Gritty Rock Vocal — sounds like 90s alt-rock lead

**Accuracy: B** — the attitude is there; the last 10% is a real tube pre and a great room.

## The Chain
Channel strip (HPF + EQ + comp) → parallel Scream 4 (via Spider Audio) → RV7000 MkII plate (send)

## Steps
1. Channel strip: engage HPF at 80 Hz. EQ: cut 2–3 dB around 300 Hz (LMF), boost 2 dB at 3 kHz (HMF) for bite.
2. Channel strip compressor: ratio around 4:1, fast attack OFF, release medium. Aim for 4–6 dB gain reduction on loud phrases.
3. Split the vocal with a Spider Audio: path A dry, path B into Scream 4.
4. Scream 4: Damage type Tube, Damage ~35, P1 ~60, P2 ~50. Cut section: lows -20. Master level down so it sits UNDER the dry path.
5. Blend the Scream path in at roughly -10 dB relative to dry — you should feel it, not hear it as distortion.
6. Send to RV7000 MkII: algorithm Plate, decay 1.1 s, predelay 30 ms, HF damp on. Send level low — rock vocals stay dry-ish.

## Why this works
The dry path keeps consonants intact; the parallel Scream adds harmonics that read as "power" at mix level.

## Order of operations
Compress BEFORE the parallel split so both paths get a consistent level — otherwise the grit pumps.

## Reason-specific trick
Build the whole thing in a Combinator 2 and map one macro knob to the Scream path's level. That knob is now a "grit" control per song section.

## RE upgrade path
None needed at B. If you chase A: a tape/console emulation (e.g., Softube Tape, ~$99) rounds the top end.

## Technique you just learned
Parallel saturation: distort a copy, tuck it under the clean signal.

=====================================================
SOURCE FILE: rock-mix-glue.md
ORIGINAL LOCATION: HS:recipes/rock/rock-mix-glue.md
=====================================================

---
name: Rock Mix Glue
book: rock
sounds_like: a finished rock record instead of separate tracks
accuracy: B
status: theoretical
source: a balanced rough mix hitting the master around -6 dB peaks
tags: master bus glue mix compression mclass full mix
technique: bus compression — slow attack, fast release, barely working
---
# Rock Mix Glue — master bus chain

**Accuracy: B** — MClass does the job; the missing 10% is the character of an SSL G-comp. Honest note: Reason 12 has no LUFS meter — load a free VST3 meter (Youlean Loudness Meter, $0) for streaming targets.

## The Chain
Master insert: MClass Equalizer → MClass Compressor → MClass Maximizer

## Steps
1. MClass Equalizer: Lo Cut ON (30 Hz rumble gone). Param 1: +1 dB at 100 Hz wide Q if the mix feels thin. Hi Shelf +1 dB at 10 kHz. That's it — master EQ is a nudge, not a fix.
2. MClass Compressor: ratio 2:1, attack SLOW (~35 ms so transients punch through), release fast or Adapt ON. Threshold until you see 1–2 dB reduction on the loud sections. Never more.
3. Listen with it bypassed vs in. The "in" version should feel slightly more like one performance. If it sounds squashed, back the threshold off.
4. MClass Maximizer: input gain until limiting shows 1–3 dB on peaks, Look Ahead ON, output -0.3 dB. Loudness comes from the mix, not this box.
5. A/B against a commercial rock reference at MATCHED volume (turn yours up/down till equal loudness) — louder always sounds "better" and lies to you.

## Why this works
1–2 dB of slow-attack compression makes tracks rise and fall together — the "glue" is shared gain movement.

## Order of operations
EQ before comp: fix tonal balance first so the compressor reacts to the mix you want, not the mud you're about to cut.

## Reason-specific trick
Put the chain in the master section's insert slot (SSL master bus), not on a separate channel — it stays with the song file.

## RE upgrade path
For A: an SSL-style bus comp emulation (Softube, ~$99) adds the nonlinear character MClass lacks.

## Technique you just learned
Glue compression: the compressor you barely hear working.

=====================================================
SOURCE FILE: shoegaze-guitar-wall.md
ORIGINAL LOCATION: HS:recipes/rock/shoegaze-guitar-wall.md
=====================================================

---
name: Shoegaze Guitar Wall
book: rock
sounds_like: My Bloody Valentine / Slowdive wash
accuracy: C
status: theoretical
source: DI electric guitar, clean; works better with two takes
tags: guitar shoegaze wall reverb wash chorus wide ambient
technique: reverb INTO distortion — the wash becomes part of the tone
---
# Shoegaze Guitar Wall — sounds like MBV / Slowdive

**Accuracy: C** — honest flag: real shoegaze is a fuzz pedal, a Jazzmaster, and reverse-reverb pedals into a loud amp. Stock Reason approximates the wash, not the bloom. This gets you "dreamy wide wall," not Loveless.

## The Chain
Double-tracked guitar → CF-101 chorus → RV7000 (100% wet) → Scream 4 → wide panning

## Steps
1. Record the part twice (real doubles, not a copy). Pan take 1 hard left, take 2 hard right.
2. Each side: CF-101 Chorus/Flanger — rate low (~30), feedback 0, delay ~40, sync off. Subtle movement, not seasick.
3. Here's the trick, per side: RV7000 as an INSERT set 60–80% wet, Hall, decay 4 s, THEN Scream 4 after it.
4. Scream 4: Damage type Fuzz, Damage 45–60. Because the reverb feeds the fuzz, the tail distorts and smears into the tone. That's the shoegaze move.
5. Roll off highs after: channel EQ high shelf -3 dB at 8 kHz. Shoegaze walls are dark, not bright.
6. Both sides to a guitar bus; bus comp 2:1, slow attack, 2 dB reduction, just to stop the wall from swallowing the snare.

## Why this works
Normal chains distort then reverberate (clean tail). Reversing the order makes the reverb tail itself distort — a continuous sustaining wall.

## Order of operations
That reversal IS the recipe. Reverb → distortion. Non-negotiable here.

## Reason-specific trick
Automate the RV7000 dry/wet from verse (30%) to chorus (80%) via a Combinator macro for the "the chorus just opened up" effect.

## RE upgrade path
This is a D→C rescue by stock. For a real B: a proper fuzz + reverse reverb RE or VST (Reason 12 runs VST3 — free options: Airwindows fuzz, Valhalla Supermassive, $0).

## Technique you just learned
Effect-order inversion: putting time-based effects BEFORE gain effects changes the instrument, not just the polish.

=== END OF PART ===
