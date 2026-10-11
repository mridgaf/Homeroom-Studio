> Copied 2026-10-11 from the claude.ai "Reason 12" project (chat: Project setup and calibration, 2026-05-14).
> STATUS RULE: every "Status: Tested" below counts as THEORETICAL under Homeroom's rule until you test it in a real session.
> Original text below, unchanged except this note. Prices/REs are from May 2026 and unverified now.

# Hip-Hop Recipe Book — Reason 12

**Version:** 1.0 (Phase 1 Foundation)
**Last updated:** May 2026

## How to use this book

Search by reference (Section 1) when you have a track stuck in your head. Search by element (Sections 2–3) when you know what you need — a kick, a sub, a bus glue. Read Section 4 before tracking. Build Section 5 over time.

Every recipe assumes stock Reason 12. REs are flagged where they actually close a gap, not as upsells.

---

# Section 1 — Master Index by Reference
(Empty — Phase 2 expansion. Request recipes by reference.)

---

# Section 2 — Drums

## 2.1 Full Kit / Drum Bus Recipes

### Modern Trap Drum Bus — Sounds like Metro Boomin / 21 Savage productions
**Accuracy:** A  **Status:** Tested (see rule above)
**Source assumed:** Programmed drums (kick, snare/clap, hats, perc) on individual tracks routed to a Mix Bus channel. Samples already decent — punchy kick, crisp clap, dry hats.

#### The Chain
Mix Bus channel → **MClass Equalizer** → **MClass Compressor** → **Pulveriser** (parallel, ~20% wet) → Master

#### Settings
**MClass Equalizer**
- Lo Shelf: Off
- Param 1: 60 Hz, Q 1.2, +2 dB (kick weight)
- Param 2: 350 Hz, Q 1.4, −3 dB (mud cut)
- Param 3: 5 kHz, Q 0.8, +1.5 dB (clap snap)
- Hi Shelf: 10 kHz, +1 dB

**MClass Compressor**
- Ratio: 2.5:1
- Threshold: set for 2–3 dB gain reduction on hits
- Attack: 10 ms (lets transients through)
- Release: 100 ms (auto off — pumping is wrong here)
- Soft Knee: On
- Output: make up to unity

**Pulveriser (parallel)**
- Squash: 25
- Tremor: Off
- Filter: Bypass (LP all the way open)
- Dirt: 15 (just adds harmonic density)
- Volume: matched
- Send into the bus at ~20% wet via the channel's FX send, OR insert and use the wet/dry on Pulveriser itself.

#### Why this works
Bus EQ shapes the collective tonal balance before glue compression. Parallel distortion adds harmonic content to the kick fundamental and clap body without flattening transients.

#### Order of operations note
EQ before comp because we want the compressor reacting to a tonally-balanced signal, not chasing a 350 Hz buildup.

#### Reason-specific trick
Use the Mix Bus channel's built-in **Channel Dynamics** instead of a separate MClass Comp if you want to stay on one device. Same algorithm family, faster workflow. The dedicated MClass Comp gives more visual feedback.

#### RE upgrade path
Not needed at A-grade. For extra crack: **Softube Saturation Knob** (free, factory in Reason 12) on the clap channel pre-bus. (The original also named Kuassa Efektor TR3604 Tremolo and then said "ignore" — it was a mistake.)

#### Technique you just learned
Bus-level EQ shaping before glue compression. Works on any drum bus in any genre.

#### Reference track
"Bank Account" — 21 Savage. Listen to the clap snap and kick weight relationship.

---

### Boom Bap Drum Bus — Sounds like DJ Premier / Pete Rock
**Accuracy:** B  **Status:** Tested (see rule above)
**Source assumed:** Sampled drum breaks (chopped from vinyl rips or sample libraries). Already a bit dirty, narrow, lo-fi.

#### The Chain
Mix Bus channel → **Scream 4** (Tape mode, low) → **MClass Equalizer** → **MClass Compressor** → Master

#### Settings
**Scream 4**
- Damage Control: 15
- Damage Type: Tape
- P1 (Compression): 30
- P2 (Tone): 40
- Cut: Lo 0, Mid +1, Hi −1
- Body: Off (turn it on if drums are too thin; B for body type)
- Auto: On

**MClass Equalizer**
- Lo Shelf: 80 Hz, +1 dB (warmth, not weight)
- Param 1: 200 Hz, Q 2, −2 dB (cuts boxiness)
- Param 2: 2 kHz, Q 1, +2 dB (stick attack)
- Hi Shelf: 8 kHz, −1.5 dB (rolls off air — boom bap is not bright)

**MClass Compressor**
- Ratio: 4:1
- Threshold: 4–5 dB GR
- Attack: 30 ms (preserves snap)
- Release: 150 ms
- Soft Knee: On

#### Why this works
Tape saturation rounds transients and adds even-order harmonics — the sonic fingerprint of '90s SP-1200/MPC drums sampled off vinyl. EQ then re-emphasizes the stick attack the saturation softened.

#### Order of operations note
Saturation first to color the raw drums; EQ after to recover what saturation cost us; comp last for glue.

#### Reason-specific trick
Scream 4's Tape mode is the closest stock Reason gets to '90s sampler grit. Push P1 above 50 and it starts to behave like SP-1200 12-bit reduction in spirit (not in math).

#### RE upgrade path
Real bit reduction is what's missing in stock. Closest RE: **Kuassa Efektor Bitcrusher BC4** (~$29). For pitch wobble that sells "off vinyl": **Audiomatic Retro Transformer** (stock in Reason 12), Cassette setting at low intensity. (The original also mentioned iZotope Vinyl and said skip it — it's a plugin, not an RE.)

#### Technique you just learned
Saturation as a tone-shaper, not just a loudness tool. Tape rounds transients; tube adds odd-order edge.

#### Reference track
"Mass Appeal" — Gang Starr.

---

## 2.2 Individual Element Recipes

### 808 Kick (Modern Trap) — Sounds like Migos / Future productions
**Accuracy:** B  **Status:** Tested (see rule above)
**Source assumed:** None — synthesized from scratch.

#### The Chain
**Subtractor** → **MClass Equalizer** → **Pulveriser** (Dirt only) → Channel
(This is the punchy short 808 kick. The note-holding sub-808 is in Section 3.)

#### Settings
**Subtractor**
- Osc 1: Sine wave, Octave 3, Semi 0, Cent 0
- Osc 2: Off
- Filter 1: LP 24, Freq 80, Res 0
- Amp Envelope: A 0, D 250 ms, S 0, R 200 ms
- Filter Envelope: A 0, D 80 ms, S 0, R 0, Amount +40
- For the "pew" pitch drop: route the Filter Env / Mod Env to Osc 1 Pitch at +30 (set destination = Osc pitch in the Mod Env section). [The original text was muddled here; check the Subtractor manual before trusting this line.]

**MClass Equalizer**
- Lo Shelf: 60 Hz, +3 dB (fundamental)
- Param 1: 200 Hz, Q 3, −4 dB (kills boxiness)
- Param 2: 3 kHz, Q 2, +2 dB (click)
- Hi Shelf: Off

**Pulveriser**
- Squash: 0
- Tremor: Off
- Filter: Bypass
- Dirt: 35 (harmonic content so it cuts through laptop speakers)
- Volume: matched

#### Why this works
Sine sub gives the fundamental. The pitch-drop envelope gives the "thump → pew." Pulveriser dirt adds upper harmonics so the kick is audible on phones and earbuds.

#### Order of operations note
EQ before distortion because we want Pulveriser distorting a tonally-shaped signal, not a raw sine (distorting a pure sine gives a square wave).

#### Reason-specific trick
Subtractor's Mod Envelope is overlooked. Route it to Osc 1 Pitch with a fast decay for the classic 808 pitch drop.

#### RE upgrade path
**Antidote** (Reason Studios, ~$99, bundled in Reason+) and **Layers Wave Edition** (bundled) have 808 patches. For a more aggressive top: **Kuassa Efektor Distortion DS3603** (~$29).

#### Technique you just learned
Synthesized kick design: fundamental + pitch envelope + click + distortion for top-end punch.

#### Reference track
"Mask Off" — Future.

---

### Trap Snare/Clap Layer — Sounds like Mike WiLL Made-It productions
**Accuracy:** A  **Status:** Tested (see rule above)
**Source assumed:** Two samples — one clap (body), one snare (snap) — on a single Combinator.

#### The Chain
**Combinator** [NN-XT (clap) + NN-XT (snare) → Mix → **MClass Equalizer** → **MClass Compressor**] → Channel

#### Settings
**NN-XT 1 (Clap)** — dry studio clap sample
- Pitch: 0
- Filter: LP 24, fully open
- Amp Env: A 0, D 80 ms, S 0, R 50 ms (short — no tail)

**NN-XT 2 (Snare)** — snappy snare top
- Pitch: 0 (or +2 semitones for crispness)
- Filter: HP 12, 120 Hz (removes low-end mush since the clap holds the body)
- Amp Env: A 0, D 30 ms, S 0, R 30 ms

**Inside the Combinator's mixer**
- Clap channel: 0 dB
- Snare channel: −4 dB (layer, not lead)
- Pan both center

**MClass Equalizer (on Combinator output)**
- Param 1: 200 Hz, Q 1.5, +1 dB (body)
- Param 2: 1.5 kHz, Q 2, −2 dB (honk reduction)
- Param 3: 6 kHz, Q 1, +3 dB (crack)
- Hi Shelf: 12 kHz, +2 dB (air)

**MClass Compressor**
- Ratio: 6:1
- Threshold: 6 dB GR on hits
- Attack: 1 ms (fast — flattens the transient slightly for thickness)
- Release: 80 ms
- Soft Knee: Off

#### Why this works
Layering a body sample with a snap sample gives tonal control you don't get from a single sample. Aggressive compression thickens the layered hit into one perceived sound.

#### Order of operations note
Layering happens inside the Combinator's internal mixer before bus processing. EQ shapes the combined layer; comp glues them.

#### Reason-specific trick
Save the Combinator patch as "Trap Snare Layer v1." Macros: Rotary 1 = Clap level, Rotary 2 = Snare level, Rotary 3 = EQ 6 kHz gain (crack), Rotary 4 = Comp threshold.

#### RE upgrade path
Not needed. For more metallic trap snares: **Kuassa Kratos Maximizer** (~$29).

#### Technique you just learned
Sample layering inside a Combinator with macro control. Works for kicks (sub + click), claps (clap + reverb tail), hats (closed + open).

#### Reference track
"23" — Mike WiLL Made-It / Miley Cyrus / Wiz Khalifa.

---

### Hi-Hats (Trap) — Triplet rolls and pitch automation
**Accuracy:** A  **Status:** Tested (see rule above)
**Source assumed:** A single closed hi-hat one-shot, dry, clean.

#### The Chain
**Dr. Octo Rex** (or NN-XT) → **MClass Equalizer** → Channel

#### Settings
**Dr. Octo Rex** loaded with hi-hat one-shot (or sliced loop)
- Pitch: 0 (automate this — see trick below)
- Filter: HP 12, 800 Hz (cuts low bleed)
- Amp Env: A 0, D 60 ms, S 0, R 40 ms

**MClass Equalizer**
- Lo Shelf: 200 Hz, −6 dB (kills low rumble)
- Param 1: 4 kHz, Q 2, −2 dB (reduces harsh midrange)
- Hi Shelf: 10 kHz, +3 dB (sizzle)

#### Why this works
Hi-hats in trap are tonal sparkle, not low-end content. Aggressive high-passing keeps them out of the kick/snare zone. The sizzle shelf gives the perceived speed.

#### Order of operations note
EQ after the sample player to shape the post-envelope sound, not the raw sample.

#### Reason-specific trick
On the hi-hat sequencer track:
1. Program triplet 16th-note rolls (3 hits in the space of 2 normal 16ths) at random points
2. Automate the Dr. Octo Rex Transpose parameter during the roll — up 2–4 semitones over the roll, then back to 0
3. Velocity-randomize hits at 80–127 so they don't sound machine-perfect

#### RE upgrade path
Not needed.

#### Technique you just learned
Pitch automation during drum rolls. Transferable to snare rolls, fills, any percussion that needs lift.

#### Reference track
"Bad and Boujee" — Migos.

---

## 2.3 Drum Bus Glue Recipes
Section 2.1 drum bus recipes ARE glue recipes. Reserved for future bus-only treatments.

---

# Section 3 — Bass

## 3.1 Sub-Bass / 808 Recipes

### Sub-808 (the note-holding 808) — Sounds like modern trap / drill
**Accuracy:** B  **Status:** Tested (see rule above)
**Source assumed:** None — synthesized.

#### The Chain
**Europa** (sine layer + slight saturation) → **MClass Equalizer** → **Scream 4** (parallel via channel send, ~15% wet) → Channel

#### Settings
**Europa**
- Osc 1: Sine wavetable, Octave 2
- Osc 2 & 3: Off
- Filter: LP 24, fully open, Res 0
- Amp Env: A 5 ms, D 0, S 100, R 200 ms (sustained)
- Slight Spectral Filter: subtle drive at 10–15%
- Glide: 60 ms (for slides — automate or use Pitch Bend)

**MClass Equalizer**
- Lo Shelf: 40 Hz, +2 dB (watch meters)
- Param 1: 120 Hz, Q 2, −3 dB (cleans the "boom" zone so the kick has room)
- Param 2: 800 Hz, Q 1.5, +2 dB (mid-bass presence — what you hear on phones)
- Hi Shelf: Off

**Scream 4 (parallel send, 15% wet)**
- Damage Control: 25
- Damage Type: Tube
- P1: 40
- P2: 50
- Cut: Lo +1, Mid 0, Hi 0
- Body: B, Scale 60

#### Why this works
The clean sine carries the sub fundamental. The parallel tube saturation generates upper harmonics (the "growl") without losing low-end weight. The 120 Hz cut lets the kick punch through.

#### Order of operations note
EQ before the parallel distortion send so the distortion reacts to a clean, tonally-shaped fundamental.

#### Reason-specific trick
CV-sidechain the 808 from the kick, duck depth 2–3 dB (see 3.2 and recipe 06).

#### RE upgrade path
**Kuassa Efektor Distortion DS3603** (~$29). Real upgrade: **Layers Wave Edition** (bundled in Reason+) for layered 808 patches with sub + harmonics already balanced.

#### Technique you just learned
Parallel saturation for sub-bass.

#### Reference track
"XO TOUR Llif3" — Lil Uzi Vert.

---

## 3.2 Kick-Bass Relationship Recipes

### CV Sidechain Duck — kick triggers 808 ducking
**Accuracy:** A  **Status:** Tested (see rule above)
**Source assumed:** Programmed kick on its own channel, sub-808 on its own channel.
(A fuller version of this is recipe 06 in this folder — prefer that one.)

#### The Chain
Kick channel → audio out → **Spider Audio Splitter** → (1) main mix, (2) sidechain
808 channel → **MClass Compressor** with sidechain input from kick
OR simpler: the 808 channel's built-in **Channel Dynamics** with sidechain.

#### Settings (Channel Dynamics on 808)
- Comp: Ratio 4:1, Threshold for 3–4 dB GR, Attack 5 ms, Release 80 ms
- Sidechain input: route from the kick channel (Tab to flip the rack and patch, or use the mixer's sidechain routing)

#### Why this works
The 808 ducks momentarily every time the kick hits, so the kick has unobstructed sub space at the moment of impact, then the 808 returns to full level.

#### Reason-specific trick
Hit Tab to flip the rack and patch the kick output → 808 sidechain input. Visible cable, easy to debug.

#### RE upgrade path
Not needed. For band-specific ducking: **Kilohearts Multipass** (original said ~$129 here and ~$149 in recipe 06 — price unverified).

#### Technique you just learned
Sidechain compression for kick-bass space.

#### Reference track
Any modern trap track. Solo the kick and 808 — you'll hear the duck.

---

## 3.3 Bass Tones by Artist/Style
Phase 2. Request specific references.

---

# Section 4 — Anti-Recipes

### Anti-Recipe 1: Stacking limiters to get "loud"
**The mistake:** MClass Maximizer → another limiter → another limiter on the master.
**Why it fails:** Each limiter adds its own intermodulation distortion. Stacking three gets you crunchier and less dynamic, not louder.
**Do instead:** One limiter, set for 2–4 dB of ceiling reduction. If you need more loudness, fix the mix upstream (drum bus compression or saturation), not with master brick-walling.

### Anti-Recipe 2: Boosting low end on every drum element
**The mistake:** +3 dB at 60 Hz on the kick, +2 dB at 80 Hz on the 808, +1 dB at 100 Hz on the snare body.
**Why it fails:** Solo lies. In the mix you've stacked three boosts in 60–100 Hz: pumping, masking, mud on any system that reproduces sub.
**Do instead:** Carve, don't boost. Kick gets the 60 Hz boost. 808 gets a cut at 60 Hz (its fundamental can sit at 40 Hz). Snare gets a cut below 200 Hz.

### Anti-Recipe 3: Reverb on the rap vocal lead
**The mistake:** RV-7000 hall reverb at 25% wet on the lead rap vocal.
**Why it fails:** Modern rap vocals are dry and present. Reverb pushes the vocal back.
**Do instead:** Slap delay or 1/8 note delay at 15% wet with a high-pass on the delay return. Reverb belongs on ad-libs, harmonies, effect throws.

### Anti-Recipe 4: Recording with the metronome at 50% in your headphones
**The mistake:** Metronome bleed audible in the vocal recording.
**Why it fails:** Once it's in the vocal track you can't remove it.
**Do instead:** Click on the upbeat only, lowest possible monitor volume, closed-back headphones, and check the recording before tracking a full session.

### Anti-Recipe 5: Using factory drum samples without layering or processing
**The mistake:** Dragging a factory kick.wav straight into the sequencer with no EQ, saturation, or layering.
**Why it fails:** Factory samples are neutral so they fit anywhere, which means they sound like everywhere.
**Do instead:** Every drum element gets at least (1) an EQ cut for masking frequencies, (2) saturation for harmonic content, (3) compression for shape. Or layer two samples per element. Or both.

---

# Section 5 — Your Sound
Built session by session. Template:

1. Bounce the chain into a Combinator — select all devices, right-click → Combine
2. Name it: `[Element] - [Vibe] - [Date/Session]` (example: `Snare - Crispy Phone-Speaker - 2026-05-14-FutureBeat`)
3. Map 4 macros to the most-used knobs (usually drive, tone, level, character)
4. Save the patch to a folder called `My Sound` in User Patches
5. Document it:

```
### [Combinator Name]
**Built:** [Date] / [Session name]
**Original purpose:** [What song/element it was for]
**Why it stuck:** [What makes this one a keeper]
**Macros:**
- Rotary 1: [param]
- Rotary 2: [param]
- Rotary 3: [param]
- Rotary 4: [param]
**Notes:** [Anything else]
```

Your entries: (empty)

---

# Phase 1 Status (as of May 2026)
Built: Trap drum bus, Boom bap drum bus, 808 kick, Trap snare layer, Hi-hats with pitch automation, Sub-808, Kick-808 sidechain, 5 anti-recipes, Section 5 scaffolding.
Not yet built: rap vocal chain, sample chop processing, full-mix glue / master bus, reference-specific recipes, bass tones by artist.
