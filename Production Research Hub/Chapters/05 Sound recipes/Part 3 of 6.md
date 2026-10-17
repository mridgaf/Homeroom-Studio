# Chapter 05: Sound recipes
## Part 3 of 6

_Every get-close recipe: hip-hop, rock, feelings, and the anti-recipes (what NOT to do)._

**In this part:**
- boom-bap-drum-bus.md — Boom-Bap Drum Bus — 90s hip-hop knock
- chiptune-8bit-nes-atari.md — Cartridge Bleep — NES and Atari 2600 game sound
- doechii-anxiety-loop-build.md — Anxious Loop-Build — sounds like Doechii "Anxiety"
- doechii-denial-is-a-river.md — Jazzy Chord-Planing Boom-Bap — sounds like Doechii "Denial Is a River"
- hiphop-mix-glue.md — Hip-Hop Mix Glue — master bus chain
- jayz-next-one-drums.md — Next One Drums — sounds like Jay-Z / Swizz Beatz "On to the Next One"
- jayz-next-one-lead-hook.md — Next One Lead Hook — sounds like the chopped Justice hook
- jayz-next-one-vocal.md — Next One Vocal — sounds like Jay-Z, "On to the Next One"

(Next: Part 4 of 6)


=====================================================
SOURCE FILE: boom-bap-drum-bus.md
ORIGINAL LOCATION: HS:recipes/hiphop/boom-bap-drum-bus.md
=====================================================

---
name: Boom-Bap Drum Bus
book: hip-hop
sounds_like: 90s East Coast knock — DJ Premier / Pete Rock era
accuracy: B
status: theoretical
source: programmed drums (Redrum/Kong) or chopped breaks
tags: drums bus boom bap knock 90s lofi crunch kong redrum
technique: bus saturation + heavy compression as a SOUND, not a repair
---
# Boom-Bap Drum Bus — 90s hip-hop knock

**Accuracy: B** — the crunch is reachable; the exact SP-1200/MPC60 12-bit artifact isn't in stock Reason. Close enough to bob heads.

## The Chain
All drums → bus channel → Scream 4 → MClass Compressor → channel EQ

## Steps
1. Route every drum (kick, snare, hats, perc) to one bus channel. This recipe lives on the BUS, elements stay mostly raw.
2. Scream 4 on the bus: Damage type Digital, Damage 30–45, P1 (rate) down around 60–70 to fake bit-reduction grit. This is the SP-1200 impression.
3. MClass Compressor: ratio 6:1, attack medium-fast (~10 ms), release fast, 4–6 dB reduction. Yes, that's heavy — boom-bap bus compression is an effect, not glue.
4. Channel EQ on the bus: +2 dB at 80 Hz (boom), -2 dB at 500 Hz (cardboard), +1.5 dB at 7 kHz (dust and air).
5. If it pumps musically, you're done. If it pumps annoyingly, slow the release slightly.
6. Optional: nudge snare timing a few ticks LATE by hand. The lazy snare is half the boom-bap feel — no plugin does this, it's sequencing.

## Why this works
Heavy bus compression makes hits mash into each other (the "knock"); digital-type saturation supplies vintage-sampler grime.

## Order of operations
Scream before comp: the compressor should slam the already-dirty signal — reversing it makes the dirt level jump around.

## Reason-specific trick
Do the chopping in Kong's NN-Nano or NN-XT, one hit per pad, then this bus chain unifies hits from different records into one kit.

## RE upgrade path
For the true 12-bit artifact: a bit-crusher RE or free VST (decimort-style). Marginal gain — the compressor is 80% of this sound.

## Technique you just learned
Processing the group instead of the parts — cohesion comes from shared abuse.

=====================================================
SOURCE FILE: chiptune-8bit-nes-atari.md
ORIGINAL LOCATION: HS:recipes/hiphop/chiptune-8bit-nes-atari.md
=====================================================

---
name: Cartridge Bleep
book: hip-hop
sounds_like: NES / Atari 2600 game music — Mega Man, Super Mario Bros era
accuracy: B
status: theoretical
source: documented sound-chip architecture (Ricoh 2A03 and Atari TIA), adapted to Reason stock devices — the chip behaviour is public and exact, the Reason mapping is mine
tags: chiptune 8-bit nes nintendo atari videogame arcade square pulse arpeggio subtractor rpg8 noise retro bleep game
technique: fake a chord with speed — when you only have one voice, cycle the notes fast enough and the ear stops hearing an arpeggio and starts hearing harmony
---
# Cartridge Bleep — NES and Atari 2600 game sound

**Accuracy: B** — the hardware is thoroughly documented, so the shapes here
are exact; what's mine is the mapping onto Reason's stock devices. The one
honest approximation is the Atari tuning in step 7, flagged where it happens.

The whole trick: those consoles had no room for recordings. A tiny chip made
every sound live, and it could only make about four shapes — a square, a
triangle, noise, and a pitch slide. **The limits are the sound.** Nothing
below is smoothed, filtered, or reverbed, and that's on purpose.

The NES had five voices, each with one job: two squares (melody and
harmony), one triangle (bass), one noise (drums), one tiny crunchy sample.
You're rebuilding four of them.

## The Chain
Launchkey MK3 → RPG-8 Arpeggiator (fast) → SubTractor #1 (square lead) + SubTractor #2 (triangle bass) + Kong (synth drum modules) → straight to the mixer, NO reverb, NO delay

## Steps
1. The melody voice: create a SubTractor. Osc 1 waveform → **square** (the second waveform). Set **Polyphony to 1** — the chip could only play one note per voice, and holding yourself to that is most of the authenticity. Turn Filter 1's Freq all the way **up** (fully open): the hardware had no filter at all, and any filtering instantly sounds like a modern synth pretending.
2. Make it blocky: Amp Envelope **Attack 0, Decay 0, Sustain full, Release 0**. Notes must start and stop instantly, like a switch. Any fade in or out is wrong for this.
   Then set the tone: switch Phase mode to **"x"** and move the **Phase** knob. On a square wave this changes the pulse width — thin and nasal at one end, round and fat at the other. That single knob is the NES's entire timbre control; park it around 12 o'clock for the classic Mario lead, hard left for the thin, reedy one.
3. The fake chord (this is the money step): put an **RPG-8 Arpeggiator** above the SubTractor so it feeds it. Mode **Up**, Octave **1**, Gate Length short, Rate **1/64** (or 1/32 if 1/64 sounds like buzzing rather than notes). Hold a normal 3-note chord on the Launchkey and press RPG-8's **Hold**.
   The NES only had two square voices, so a real three-note chord was *impossible* — they cycled the notes 20–60 times a second instead and let your ear glue them together. That bubbling ripple under every NES tune is a chord being faked, and this is how you fake it.
4. The bass: a second SubTractor, Osc 1 → **triangle**, Polyphony **1**, filter fully open again. Amp Envelope same blocky settings, but here's the period-correct part — the NES triangle had **no volume control at all**. It was on or off. So leave the level parked and never automate it; play bass an octave below the melody, mostly root notes, straight 8ths.
5. The drums: Kong on the Launchkey pads (**Shift + Pad Mode → Drum**). Use the **synthesized** modules, not sampled ones — Synth Bass Drum on pad 1, Synth Snare on pad 2, Synth Hi-Hat on pad 3. The NES made all its drums from the noise channel and a pitch drop, so anything sampled here is the wrong century. Keep the snare short and bright; no tails.
6. Jumps and lasers: back on the lead SubTractor, set the **Mod Envelope** destination to **Osc 1 pitch**, Amount high, Decay very short (under 100 ms). Now every note starts high and snaps down — that's the coin/jump/laser sound. Drop the Amount to about a third for a subtler "chirp" on the melody, or run it as its own FX track.
7. The Atari flavour (optional, and the honest one): the Atari 2600 had only **32 possible pitches**, unevenly spaced, so a lot of its notes were genuinely out of tune and the composer simply couldn't fix it. That sourness is the Atari sound. To approximate it, detune Osc 2's **Cent** knob 25–40 either way and mix it under Osc 1.
   Be aware this is an approximation: the real chip was out of tune *by a different amount on every note* (in one octave, C is nearly perfect while G# is more than a quarter-tone flat). One Cent knob detunes everything equally, so you get the sourness but not the note-to-note unevenness. Closest you'll get without a dedicated chip emulator.
8. Keep it dry and save it: no reverb, no delay, no chorus, no tape. It should sound like it's coming out of a plastic speaker across the room, because it is. Once the four voices sit together, select them all and **save as "Cartridge Bleep.cmb"** so the whole console is one Combinator you can drop into any song.

## Why this works
Every element is a limitation being honoured rather than worked around: one note per voice, no filter, instant envelopes, no effects. Modern synths default to smooth and wide, which is precisely what makes a "chiptune preset" sound fake. Reason can do the real thing because SubTractor is a plain subtractive synth — you're just refusing to use most of it.

## Order of operations
Bass and drums first (they're the grid), then the square lead, then the arpeggiator on top. Do step 3 last of the melodic parts — if the arp goes on before the lead tone is right, you'll be tuning a moving target.

## Reason-specific trick
The RPG-8 at 1/64 with Hold is the single closest thing in stock Reason to a real chip arpeggio, and it's better than drawing the notes in by hand because the ripple stays locked to tempo when you change BPM. Also worth knowing: SubTractor's own **Noise** oscillator (with Decay short and Color bright) is a legitimate second route to chip drums if you'd rather not use Kong — that's exactly what the NES's noise channel was.

## RE upgrade path
None needed for the sound. If you end up doing a lot of this, a dedicated chip emulator (Plogue chipsynth-style) models the *per-note* tuning error from step 7 and the true 15-bit noise register, which SubTractor can only approximate — that's the one thing worth buying, and only if the sourness matters to you.

## Technique you just learned
Fake a chord with speed. When you only have one voice, cycle its notes fast enough and the ear stops hearing an arpeggio and starts hearing harmony — a trick that works on any mono synth, not just for game music.

## Reference
NES sound chip in action — Mega Man 2 (1988): https://www.youtube.com/results?search_query=Mega+Man+2+NES+soundtrack

=====================================================
SOURCE FILE: doechii-anxiety-loop-build.md
ORIGINAL LOCATION: HS:recipes/hiphop/doechii-anxiety-loop-build.md
=====================================================

---
name: Anxious Loop-Build
book: hip-hop
sounds_like: Doechii "Anxiety"
accuracy: C
status: theoretical
source: MIDI + rap/sung vocal; original is sample-based
tags: doechii anxiety gotye loop pluck guitar ostinato energy chant hook stacked vocals
technique: building a whole song on one hypnotic pluck ostinato, with arrangement mutes as the drama
---
# Anxious Loop-Build — sounds like Doechii "Anxiety"

**Accuracy: C — honest flag up front:** the identity of "Anxiety" is a licensed sample of Gotye's "Somebody That I Used to Know" (itself sampling Luiz Bonfa's "Seville"). No recipe reproduces a specific sample; this recipe gives you the framework — a nervous pluck ostinato, driving beat, and stacked chant hook — which is the transferable part anyway.

## The Chain
NN-XT nylon-guitar patch (pluck ostinato) → MClass EQ + Scream 4 (Tape) → driving kit + shaker → SubTractor sub → stacked chant vocals

## Steps
1. The ostinato: on an NN-XT nylon or muted-guitar patch, write a 2-bar syncopated single-note figure in a minor key — short notes, lots of off-beats, one note bending the minor 2nd for unease. Keep amp release short so every note plucks and dies.
2. Lo-fi the loop: MClass EQ — cut above 8 kHz and below 150 Hz, then Scream 4 Tape at Damage 25. Goal: it should sound like it came off someone else's record. That "found object" quality is the aesthetic.
3. Drums: brisk and insistent. Kick on every beat in the hook sections (four-on-the-floor energy), claps layered with snare on 2+4, shaker straight 8ths. Verses: drop to a sparser kick so the hook lifts.
4. Sub: SubTractor sine following the ostinato's root notes only. Simple on purpose — the pluck loop owns the midrange.
5. Hook vocals: this production is a vocal-stack showcase. Record the chant hook 4+ times: lead center, doubles hard L/R, one harmony above. Same chain per track (Upfront Rap Vocal recipe), then bus them and compress the BUS 3-4 dB so they move as a crowd.
6. The anxiety mechanic: automation mutes. Kill the drums for the last beat of every 4th bar; drop everything but the loop for one bar before each hook. The song breathes in nervous gasps — that's arrangement, not effects.
7. Verses ride dry and conversational over the loop; energy comes from the drum arrangement, never from pushing the vocal.

## Why this works
One hypnotic loop + disciplined mutes = tension that keeps renewing itself; the ear never gets to settle.

## Order of operations
Loop first, drums second, mutes LAST — you can't place the gasps until the full arrangement exists.

## Reason-specific trick
Put the pluck loop in a Combinator with a macro mapped to the MClass EQ high cut — automate it opening slightly into hooks for a "curtain lifting" effect without a volume change.

## RE upgrade path
None needed. If you want the actual interpolation route, that's a clearance question, not a gear question.

## Technique you just learned
Loop-based song architecture: commit to one ostinato, then make arrangement subtraction do the emotional work.

## Reference
Doechii — "Anxiety": https://www.youtube.com/watch?v=INEbUVpn8t4

=====================================================
SOURCE FILE: doechii-denial-is-a-river.md
ORIGINAL LOCATION: HS:recipes/hiphop/doechii-denial-is-a-river.md
=====================================================

---
name: Jazzy Chord-Planing Boom-Bap
book: hip-hop
sounds_like: Doechii "Denial Is a River"
accuracy: B
status: theoretical
source: MIDI + a rap vocal; no samples needed
tags: doechii denial river boom bap jazzy chords planing dominant 13 golden age drunken kick
technique: chord planing — copy one rich chord shape chromatically for instant jazz harmony
---
# Jazzy Chord-Planing Boom-Bap — sounds like Doechii "Denial Is a River"

**Accuracy: B** — the harmony and groove are fully reproducible; producer Ian James built the original by replaying one sampled chord as MIDI and dragging copies around a piano roll. Reason's sequencer does the identical move. What you won't clone is Doechii herself.

## The Chain
E-piano patch (ID8 or NN-XT Rhodes) → Scream 4 (Tape) → boom-bap kit (Kong/Redrum) + ReGroove → SubTractor bass → dry rap vocal

## Steps
1. The chord: build ONE dominant-13 in spread voicing — from bottom: A, G, C#, F#, B (root, flat-7, 3, 13, 9). Program it once in the sequencer on an e-piano sound (ID8 E-Piano or an NN-XT Rhodes patch).
2. The planing trick: copy that whole chord block and drag the copies — down a half-step (Ab13), down again (G13), once more (F#13). Two-bar loop. Do NOT correct notes to the key; moving the shape intact IS the sound. This is how the actual record was made, just in a different DAW.
3. Rhythm of the chords: hit them in a 3+3+2 pattern (count "one-two-three, one-two-three, one-two") rather than on downbeats. That off-balance push is half the groove.
4. Tone: Scream 4 after the e-piano, Tape, Damage 20-30 — dusty, slightly compressed, early-90s sampler warmth. Small RV7000 room, barely audible.
5. Drums: sparse boom-bap kit. Snare on 2 and 4, nudged a few ticks LATE. Kicks deliberately loose — the original's kicks are "drunken." Reason move: push the drum track through a ReGroove channel with shuffle around 54-58% instead of quantizing.
6. Bass: SubTractor, waveform 3 (triangle), following the chord roots down: A, Ab, G, F#. Short notes, locked to the kick.
7. Vocal: dry and upfront (use the Upfront Rap Vocal recipe). For the inner-dialogue second voice: duplicate track, pan 30% off-center, MClass EQ — cut below 300 Hz and above 5 kHz for a boxy "voice in your head" contrast.

## Why this works
Four unresolvable dominant-13 chords in parallel create rich tension that never lands — a mood bed that lets the rap carry all the direction.

## Order of operations
Write chords before drums: the 3+3+2 chord rhythm defines where the drums should NOT hit.

## Reason-specific trick
ReGroove Mixer is the platform advantage here — per-channel shuffle and slide gets the drunken-kick feel no grid quantize can. Save the e-piano + Scream + RV7000 as a Combinator: "Golden EP.cmb".

## RE upgrade path
None. This one is genuinely all-stock.

## Technique you just learned
Chord planing: one good voicing, copied chromatically, beats an hour of theory.

## Reference
Doechii — "Denial Is a River": https://www.youtube.com/watch?v=f-OWO1aZz0g

=====================================================
SOURCE FILE: hiphop-mix-glue.md
ORIGINAL LOCATION: HS:recipes/hiphop/hiphop-mix-glue.md
=====================================================

---
name: Hip-Hop Mix Glue
book: hip-hop
sounds_like: a modern rap record — loud, controlled low end, vocal on top
accuracy: B
status: theoretical
source: balanced rough mix, 808 and vocal already sitting right
tags: master bus mix glue hip hop loud low end mclass
technique: mastering triage — low-end control first, loudness last
---
# Hip-Hop Mix Glue — master bus chain

**Accuracy: B** — same MClass honesty as the rock version: capable, characterless. No stock LUFS meter; grab a free VST3 meter (Youlean, $0). Streaming target ≈ -14 LUFS integrated; rap often masters hotter (-9 to -7) accepting platform turndown.

## The Chain
Master insert: MClass Equalizer → MClass Stereo Imager → MClass Compressor → MClass Maximizer

## Steps
1. MClass EQ: Lo Cut OFF (you need the sub!). Param 1: if the 808 is wooly, cut 1–2 dB around 250 Hz. Hi shelf +1 dB at 12 kHz for expensive-sounding air.
2. MClass Stereo Imager: LOW band (below ~150 Hz) width toward mono. Mono bass hits harder everywhere and survives club systems. High band width +10–20%, no more.
3. MClass Compressor: ratio 2:1, slow attack, Adapt release, 1–2 dB reduction. Even in loud rap masters, bus glue stays gentle — loudness comes next, not here.
4. MClass Maximizer: this genre leans on it harder — 3–5 dB of limiting is normal. Look Ahead ON, output -0.3. Listen for 808 distortion; if the sub farts, the limiter is fighting the low end — go back to step 2 and mono/tame the bass more.
5. Volume-matched A/B against a commercial rap reference. Check on earbuds AND anything with a subwoofer: two different low-end realities, both have to work.

## Why this works
Rap masters live or die on low-end management; every step here disciplines the sub before the limiter has to.

## Order of operations
Imager before compressor: mono-ing the bass changes energy the comp reacts to. Maximizer always dead last.

## Reason-specific trick
Save this whole master insert chain as a preset from the master section — every new song starts one click from your mastering baseline.

## RE upgrade path
For A: a modern true-peak limiter VST (many free/cheap) outperforms the 2004-era Maximizer at high limiting depths.

## Technique you just learned
Loudness is earned upstream — a limiter reveals low-end problems, it doesn't solve them.

=====================================================
SOURCE FILE: jayz-next-one-drums.md
ORIGINAL LOCATION: HS:recipes/hiphop/jayz-next-one-drums.md
=====================================================

---
name: Next One Drums — Electro Punch
book: hip-hop
sounds_like: Jay-Z & Swizz Beatz "On to the Next One" (2009) drums
accuracy: C
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), built from web research about the track, not from stems. Old project rated it B; re-rated to Homeroom's scale
tags: jay-z swizz beatz on to the next one electro drums kong scream tape punchy short kick snare clap
technique: short electronic drums with a mid-range push and gentle grit, glued lightly
---
# Next One Drums — sounds like Jay-Z / Swizz Beatz "On to the Next One"

**Accuracy: C** — built from descriptions of the track, not from the real session. The drums are short, punchy and a little distorted, not a long boomy 808. Judge it in a full beat. The Justice sample carries most of the top end, so drums alone will sound thin.

## The Chain
Kick: Kong → MClass Equalizer → MClass Compressor → Scream 4. Snare and clap: Kong (two pads) → MClass Equalizer → MClass Compressor, with RV7000 on a send. All → drum bus group → MClass Compressor → MClass Equalizer.

## Steps
1. Kick: load a tight electronic kick into a Kong pad. Pitch -2 semitones, decay short, level -6 dB. (The old notes named specific Kong sample names. Unverified, so just audition the electronic kits.)
2. Kick EQ: +3 dB shelf at 80 Hz, cut -4 dB at 300 Hz (boxy), +4 dB at 2.5 kHz (the click).
3. Kick compressor then Scream 4: compressor ratio 4:1, attack 10 ms, release 80 ms. Scream 4 Tape, Damage 25 for a slightly pushed, crunchy kick.
4. Snare and clap: layer a snare and a clap on two pads and hit both on beats 2 and 4. Clap a touch louder than the snare. EQ: -6 dB shelf at 100 Hz, -3 dB at 400 Hz, +5 dB at 4 kHz (crack), +2 dB shelf at 10 kHz. Compressor 3:1, attack 5 ms, release 100 ms.
5. Snare room: send a little to RV7000, Hall, decay 1.8 s, predelay 30 ms, send at -18 dB. Just a hint of space.
6. Drum bus: group kick and snare together. Compressor 2:1, attack 15 ms, release 120 ms, 2–3 dB of squeeze. EQ +1.5 dB at 60 Hz and 12 kHz. Channel Drive 15–20%.

## Why this works
Short kick decay, a mid-range push for snap, tape grit for the pushed sound, and a light glue on the bus.

## Order of operations
EQ before compressor on each drum. Scream 4 after the kick compressor. Gentle bus compression so the drums still breathe.

## Reason-specific trick
Group the drums on the mixer and put the processing on the group. Use the group channel's Drive knob instead of another saturation device. Finger the Kong pads on the Launchkey for a looser feel.

## RE upgrade path
None required. The old notes named some saturation REs. Unverified.

## Technique you just learned
Short electronic drums, cut the box (300–400 Hz), boost the snap (2.5–4 kHz), light saturation, 2:1 bus glue.

## Reference
Jay-Z — "On to the Next One": https://www.youtube.com/results?search_query=Jay-Z+On+to+the+Next+One+official+audio

=====================================================
SOURCE FILE: jayz-next-one-lead-hook.md
ORIGINAL LOCATION: HS:recipes/hiphop/jayz-next-one-lead-hook.md
=====================================================

---
name: Next One Lead Hook — Mangled Synth
book: hip-hop
sounds_like: Jay-Z & Swizz Beatz "On to the Next One" (2009), the chopped Justice "D.A.N.C.E." hook
accuracy: C
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), built from web research about Justice's sound, not from the real session. Old project also rated it C
tags: jay-z swizz beatz on to the next one justice dance lead hook thor scream bitcrush chop dr octo rex stab
technique: build a plain synth source, then wreck it on purpose and chop it into rhythmic stabs
---
# Next One Lead Hook — sounds like the chopped Justice hook

**Accuracy: C** — honest ceiling. The real hook is a chopped audio sample of a Justice track, and you can't synthesize the exact sound. This gets the family: narrow-pulse analog synth, distorted, bit-crushed. Next to the record it sounds like a cousin, not a twin. In a full mix it gets much closer.

## The Chain
Thor (two pulse oscillators) → Scream 4 (Digital) → MClass Equalizer → The Echo → MClass Stereo Imager → MClass Compressor → mixer channel. Bounce the Thor part, chop it in Dr. Octo Rex.

## Steps
1. Thor, oscillators: both Analog mode, Square/Pulse. Osc 1 pulse width 25, Osc 2 width 30 with detune +7 cents, octave 4. Osc 3 off. (Check exact parameter names against docs/reason/remote-vocab.json.)
2. Thor, filter and envelopes: Low Pass Ladder filter, frequency 78, resonance 35, drive 40. Quick filter envelope decay (35) so each note plucks. Amp envelope A 0, D 30, S 75, R 25. Chorus on, subtle.
3. Play short stabs in groups of three in A minor, A3 → C4 → E4, with a rest in the pattern. Bounce it to audio (Bounce in Place).
4. Chop: load the bounce into Dr. Octo Rex, slice it, and trigger slices out of order. Reverse one slice now and then, and drop one down a fifth.
5. Wreck it: Scream 4 Digital, Damage 55, then MClass Equalizer: -8 dB shelf at 150 Hz, -4 dB at 350 Hz, +6 dB at 3 kHz, -4 dB shelf at 8 kHz.
6. Movement: The Echo synced to 1/8 dotted, feedback 25, ducking ON at 40, mix 25%.
7. Stereo and glue: MClass Stereo Imager, low width 0, high width 130, crossover 600 Hz (keeps the lows centered). Compressor 4:1, attack 8 ms, release 60 ms, 4–6 dB reduction.

## Why this works
The Thor patch gives the raw tone, the Scream and EQ break it and push the mids so it cuts through, the echo adds motion, and mono lows keep it out of the 808's way.

## Order of operations
Distort first, shape after. Echo after the EQ so the repeats are already filtered. Compressor last so levels stay steady.

## Reason-specific trick
Wrap Thor and the chain in a Combinator. Knobs: Scream Damage, Thor filter decay, Echo feedback, compressor threshold. Save as "Mangled Lead.cmb". The chopping step matters as much as the patch.

## RE upgrade path
Europa can layer an FM-style bell for the missing bell sound, and it's stock. The old notes also named other synths and prices. Unverified.

## Technique you just learned
Wreck-then-shape sound design, and mono lows with wide highs.

## Reference
Jay-Z — "On to the Next One": https://www.youtube.com/results?search_query=Jay-Z+On+to+the+Next+One+official+audio
Justice — "D.A.N.C.E." live version: https://www.youtube.com/results?search_query=Justice+D.A.N.C.E.+live+version

=====================================================
SOURCE FILE: jayz-next-one-vocal.md
ORIGINAL LOCATION: HS:recipes/hiphop/jayz-next-one-vocal.md
=====================================================

---
name: Next One Vocal — Two-Stage Compression
book: hip-hop
sounds_like: Jay-Z "On to the Next One" (2009) lead vocal, Young Guru chain
accuracy: B
status: theoretical
source: from the old Reason 12 claude.ai project (May 2026), based on a published interview about the engineer's hardware chain, adapted to stock Reason. Old project rated it A; re-rated because the hardware is replaced by stock devices
tags: jay-z vocal chain young guru compression two stage eq de-ess reverb delay rap lead mclass pulveriser
technique: slow compressor for glue, fast compressor for peaks, cut before and boost after, ambience on sends
---
# Next One Vocal — sounds like Jay-Z, "On to the Next One"

**Accuracy: B** — the order and idea come from a documented hardware chain. Reason's stock devices only approximate each hardware stage. Biggest limit: the sound starts with a clean source. A cheap mic in an untreated room won't get there. Assumes a clean dry vocal from a decent condenser mic, no processing on the recording.

## The Chain
Channel input and high-pass → MClass Equalizer (cuts) → MClass Compressor (slow) → MClass Compressor (fast) → MClass Equalizer (boosts) → Pulveriser (de-ess workaround). Sends: RV7000 hall and The Echo quarter-note delay.

## Steps
1. Channel: set input gain so the loudest words peak around -6 dB. High-pass at 80 Hz.
2. EQ #1, cuts only: -2 dB shelf at 120 Hz, -3 dB at 250 Hz (Q 1.2, the usual vocal mud), and -2 dB at 1.5 kHz (Q 2) only if the voice sounds nasal.
3. Compressor #1, the slow one: ratio 2:1, attack 30 ms, release 250 ms, threshold -16 dB, set to RMS mode. Aim for 2–3 dB reduction on average. This is smooth level control you barely hear.
4. Compressor #2, the fast one: ratio 4:1, attack 8 ms, release 100 ms, threshold -10 dB, Peak mode. Catches loud peaks, 3–5 dB. The two together do about 6–8 dB.
5. EQ #2, boosts: +1 dB shelf at 100 Hz, +3 dB at 4 kHz (presence, pushes it forward), +2 dB shelf at 10 kHz (air).
6. De-ess last: Pulveriser Squash 30, filter high-pass around 5 kHz, narrow band. This is a workaround for the harsh "s" sounds. Check the original's Pulveriser filter settings against the device before trusting them.
7. Sends: RV7000 Hall, decay 1.4 s, predelay 25 ms, return EQ high-pass 250 Hz and low-pass 8 kHz, send at -20 dB. The Echo synced 1/4, feedback 20, ducking ON at 50, send at -22 dB. Both subtle, the vocal stays dry and forward.

## Why this works
Two compressors share the work, so neither pumps. Cutting before compression means the compressor isn't wasting effort on mud. Boosting after means the boosts don't get squashed.

## Order of operations
Cuts, slow comp, fast comp, boosts, de-ess. Reverb and delay on sends so you can change them without touching the dry vocal.

## Reason-specific trick
Put the inserts in a Combinator, knobs for each compressor threshold, the 4 kHz boost, and the de-ess amount. Save as "Rap Lead Vocal.cmb". Use the channel's input gain, not the fader, to change what the chain hears.

## RE upgrade path
None required. The old notes named some hardware-emulation REs and a pitch-correction device. Names and prices unverified, and Reason's own pitch device is Neptune, so check the exact name in your Reason.

## Technique you just learned
Two-stage serial compression with split EQ. It works on any lead vocal in any genre.

## Reference
Jay-Z — "On to the Next One": https://www.youtube.com/results?search_query=Jay-Z+On+to+the+Next+One+official+audio

=== END OF PART ===
