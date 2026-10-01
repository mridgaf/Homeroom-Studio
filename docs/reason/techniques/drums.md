# Drums — routing, buses, parallel, grit, patterns
Tags: **[Manual]** Reason 12.7 manual. **[Web]** web source (URLs at bottom). **[Guess]** my idea, untested. Nothing here has been heard on our machine.
Kong/Redrum/Dr. Octo Rex deep detail (Drum Output selector, choke/link/alt groups, Redrum channel limits): `../manual-digest/drum-devices.md`. Sibling files: `../manual-digest/routing-and-main-mixer.md` (recipes C, D, H), `../../../.claude/skills/drum-loops` (project skill, not read for this file).

## 1. Get each drum onto its own channel
- **Redrum:** each of the 10 drums has its own output jack on the back. Plug a cable into one and that drum is **removed from the Redrum's main stereo out** (so it is not heard twice). Mono sound: use Left (Mono). Send Out 1–2 jacks carry the S1/S2 knob sends. Gate Out per drum can trigger other devices. [Manual, ch. 28]
- **Kong:** 16 drum channels. Each has Drum / FX1 / FX2 slots of its own, then a shared **Bus FX** (a reverb here works as one send for all pads) and **Master FX**. 14 extra audio jacks (Audio Out 3–16 = seven stereo pairs) are never auto-routed. Choose each pad's destination with the **Drum Output** selector. [Manual, ch. 27]
- **Already have a MIDI drum clip?** Use **Explode** (Tool Window, F8): one clip per drum pitch on its own lane. Then give each lane its own ReGroove channel. Or bounce each lane to audio. [Manual ch. 9 + Web: r/reasoners]
- Don't split everything by default. Split only when you want to treat one drum differently (EQ, effect, bus). Level and pan can be done inside the drum device. [Web: r/reasoners]

## 2. The drum bus
1. Route kick, snare, hats etc. to separate Mix Channels.
2. Group them into one **Output Bus** (select the channels, create the bus). One fader to mute/solo/compress/EQ all drums. [Manual: Output Busses; Web: r/reasoners]
3. Sub-bus similar sounds first if you layer (two snares → "Snares" → Drum bus). [Web]
4. Per channel: compression and saturation as needed. On the bus: glue compression and/or saturation. Reverb on a send. [Web]
- Glue compressor on the bus: **Master Bus Compressor** device (SSL style): Ratio 2:1, 1–3 dB reduction; Attack 10–30 ms lets hits punch through. [Manual device guide; Web gave the same idea]
- Alternative: **MClass Compressor**, slow-ish attack (30 ms+) = punchy. [device_refs/mclass-compressor.md]
- Kick separately: one forum user keeps kicks on their own Combinator and sends them to the master clean, drums-percussion-hats in other Combis. [Web, one person's habit]

## 3. Parallel compression (keep punch AND weight)
Three ways. All are [Manual]-based; the first two are simplest.
1. **Mix knob:** Channel Dynamics or Master Bus Compressor on the drum bus, **Mix** 30–50 %, squash hard. No cables. [device guides]
2. **Parallel Channel:** Mix Channel's Parallel Out jacks → a second channel carrying a heavy compressor; blend with its fader. [Manual: routing recipe D]
3. **Spider split:** Redrum/bus out → Spider Audio splitter → (a) clean path, (b) compressor/reverb/Scream each on its own mixer channel. Ron Headback does this with a reverb and a Scream: wet paths are purely the effect, the clean beat stays as backbone. [Web]
- Redrum or one drum only? Common to parallel-compress just the kick or snare rather than the whole kit. [Web: Reason101]

## 4. Grit and glue
- **Saturation per drum, clipper/saturation on the bus.** Treat the kit as one instrument: when the kick pushes the bus into the clipper, hats and shakers get squashed and gritty with it. This is the "edge of breakup" feel. [Web: Joey Sturgis blog]
- Reason 12.7 tools for this: **Scream 4** (Tape/Tube = warm, Overdrive = harder) and **MClass Maximizer**. A hard clipper plug-in isn't in the box. [Guess]
- Scream 4 in parallel: keep **Cut Lo** down so the low end doesn't get muddy. [device_refs/scream-4.md]
- Reverb for cohesion: ONE subtle room send shared by the whole kit makes it feel "played in one space". Don't wash it. [Web: r/reasoners]
- Gated 80s snare: RV7000 **Gate** section. [device_refs]

## 5. Sidechain and rhythm tricks with drums
- Kick ducks bass/pad: see `bass-and-low-end.md`.
- **Redrum as trigger:** Gate Out sends a pulse each hit; Pitch CV In and Gate In let other devices play Redrum sounds. Use it to trigger things (e.g. a Pulsar envelope). [Manual ch. 28; the Pulsar link is Guess]
- **Redrum send effects:** S1/S2 knobs per drum feed Send Out 1–2, typically wired to delays. Ron Headback sends a half-speed noise clap to a digital delay (4/16 time, high feedback) and **raises the delay's dry/wet over the loop to build a crescendo**. A pitched tom "beep" goes to a second delay. [Web: Reason Studios Pulsar/Europa article]
- Kick and sidechain ghost-kick idea ("ghost kick" = silent trigger track) appears in a video title only. Not read.

## 6. Pattern recipes
### Trap drums [Web: Reason Studios, 2018]
- Tempo 60–90 BPM. Clap/snare on 2 and 4.
- Hats: write straight 16ths, then vary with triplets, 32nds, 64ths, and 128th bursts at phrase ends. Use Quantize to change the rhythm feel (see `../manual-digest/note-and-automation-editing.md`).
- Kick (808): hits on beat 1, space on beat 3, a few on the "and" around 3. A second 808 with long sustain, pitch changed per note, becomes the bassline.
- Snare layer: syncopated 16ths between the 8ths, and triplet runs that rise or fall in pitch (put the sample in NN-XT and play different keys).
- Bit-crushing the snare: the article used Decimort (a Rack Extension; only if owned).

### Industrial deep-house beat [Web: Ron Headback, 2025]
- Kick: low, long tail, "subby thud," four-on-the-floor.
- Hats: short, metallic. Add shakers for movement. Clap with a long tail so the reverb smears it.
- Add industrial texture: half-speed noise clap, pitched tom, each through its own Redrum send delay.
- Parallel RV7000 (space) + Scream (scuzz) via a Spider split.

## 7. Ideas for our own drum Combi [Guess]
- One Combi: Redrum → per-drum Mix Channels → Output Bus inside the Combi → Master Bus Compressor (Mix knob) → Scream 4 (parallel).
- Macro knobs: Glue (Comp Threshold), Parallel (Mix), Grit (Scream Damage), Space (reverb send level).
- Remember: cables to anything outside the Combi aren't saved. Keep it all inside. See `../manual-digest/combinator.md`.

## Sources (summaries only)
- Reason Studios, "How to Make Trap Drums in Reason 10", 2018 — https://www.reasonstudios.com/news/post/how-make-trap-drums-in-reason-10
- Reason Studios, "Darkroom Deep House Music with Pulsar" (Ron Headback), 2025 — https://www.reasonstudios.com/news/post/pulsar-europa-and-moody-darkroom-house
- r/reasoners, "Need tips on mixing drums", 2023 — https://www.reddit.com/r/reasoners/comments/13p47z3/need_tips_on_mixing_drums/ (individual users' habits)
- Reason101.net, "Let's Talk Compression", 2010 — http://www.reason101.net/2010/10/23/36-lets-talk-compression/ (old, Reason 5-era)
- Joey Sturgis Tones, "Mixing Harder Drum Loops In Reason", 2020 — https://joeysturgistones.com/blogs/learn/mixing-harder-drum-loops-in-reason (promotes his own plug-ins; the clipper idea is what's used here)
