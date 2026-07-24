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
