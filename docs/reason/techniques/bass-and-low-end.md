# Bass, 808s and the kick — low end
Tags: **[Manual]** manual (12.7). **[Web]** web source. **[Guess]** my idea. Nothing here has been heard on our machine.

## 1. The one rule
Two sounds can't own the same low notes at the same time. You have **two fixes** (r/reasoners, an experienced mixer): move their **pitch** apart, or move them apart in **time**. With kick + bass + 808 it gets much harder than with two. [Web]

## 2. Kick + 808 as one sound
Treat the kick as the **attack** and the 808 as the **sustain**. [Web]
- Kick: short, with its low end kept brief. Optional click at 2–4 kHz on the kick. [Web]
- 808: long decay, slower attack, or delay it by 10–50 ms (try 10 ms steps, back off when you hear two hits). [Web]
- If it's a sample and overlaps: gate or shorten the kick. [Web]
- Add harmonics (light distortion, Scream 4 Tape/Tube) to the 808 so it's audible on small speakers, and leave the kick alone. [Web: one user]
- Build your own sustain: sine oscillator + fast pitch envelope + amp envelope for length. Put it in a Combinator beside the kick sample and bounce to a new kick. [Web: one user] (Subtractor/Thor/Europa all can; not tested)
- Don't pile a kick on top of an 808 with no reason. "An 808 is already a kick." [Web]

## 3. Sidechain: kick ducks the bass
Manual methods (Reason 12.7):
1. **Compressor key:** put a compressor (MClass Compressor, Channel Dynamics with **Sidechain** on, Master Bus Compressor) on the bass. Feed the kick into its **sidechain input** on the back of the device. [Manual: routing recipe E]
2. **Get the kick signal there:** use the drum channel's **Parallel Out** jacks, or a **Spider Audio splitter** on the kick's path. [Manual; Web: Facebook thread summary]
3. Redrum caution: if you plug the kick's own output jack straight into a sidechain, that drum **leaves the Redrum's main out** (nothing plays it for the mix). Split it first with a Spider so one copy goes to the mixer, the other to the sidechain. [Manual (Redrum jacks), Web: Tornevalls (R13 guide for the same problem)]
4. More than three targets: chain several Spiders. [Web: Tornevalls]
5. You can use Kong or Redrum triggers instead of audio. The 2010 Reason101 tutorial used Kong to compress a Thor bass. [Web]
6. Sidechain doesn't have to be a kick. Any sound can duck any other. Kick ducking a synth makes rhythmic gating. [Web: Reason101]

**NOT in 12.7:** the **Sidechain Tool** and "audio pump" described in the Tornevalls guide are Reason 13 features (not in the 12.7 manual).

### Which kick signal feeds the sidechain? [Web: Reason101]
When you also parallel-compress the kick: sidechain from dry kick, wet kick, or both gives different ducking. If the wet path has a delay, the bass ducks with the delay too. The author says try all three by ear.

## 4. EQ separation
- High-pass the bass's lowest sub with the equalizer so kick stays lowest and they don't fight. [Web, r/reasoners]
- Combine the HP roll-off with sidechain. [Web]
- Use **MClass Equalizer → Low Cut Enable (30 Hz)** before dynamics so sub rumble doesn't trigger the compressor. [device_refs/mclass-equalizer.md]
- Keep stereo width OUT of the low end: **MClass Stereo Imager** with a narrow **Low Width** (centre-ish bass) and wider highs. Only works on a true stereo signal. [device_refs/mclass-stereo-imager.md]
- Pick a kick pitched above the bass's fundamental, or the reverse. [Web: one user]

## 5. 808 sound design in 12.7 [Web, thin]
- The Reason Studios page titled "Tutorial: How to Make 808 Bass Lines" (2025) is **low quality**: it reads as generic filler with mistakes (e.g., says to use a "subwoofer module"). I did NOT use it. A YouTube video "Make 8 Different 808 Basses in Reason Rack" exists (not watched).
- Starting points to test [Guess]: Subtractor/Thor sine or triangle oscillator, long amp release, pitch envelope on the oscillator for the "boom" on attack, Scream 4 Tape at low Damage, MClass Compressor 2:1.
- Trap-style pitched 808 as a bassline: second 808 kick with long sustain, change its pitch per note. [Web: Reason Studios trap drums article]

### Which synth can do the pitch drop? [Manual, via `../manual-digest/synth-sound-design.md`]
Subtractor (Mod Env → Osc 1/2 pitch), Thor (Mod Env through the matrix to pitch), Europa (Envelope → "Engine: Pitch") and NN-XT (Mod Envelope → Pitch) can all drop pitch on the attack. **Monotone has no pitch envelope** (pitch moves only by LFO, bend and portamento). Direction and amount are for the ear to set. [Guess]

## 6. Parallel bass [Guess]
Use a **Parallel Channel** (Manual recipe D): low path stays clean (HPF the top, mono), high path gets Scream 4 distortion and a wide stereo imager. Idea only, untested. Based on Manual routing and the Imager's "crossover" trick (Solo = Lo, Separate Out = Hi).

## 7. Envelope-follower tricks with Gain Reduction CV
- **[Manual]** Every Mix Channel / Audio Track has a **Gain Reduction CV out** on the back. It follows how much the channel's compressor/gate is working, so it acts as an **envelope follower**. The manual's own example: use it to move a filter frequency ("auto-wah"). [Manual ch. 17]
- **[Guess, needs a test]** Key a channel compressor from the kick (Sidechain input), then take that channel's Gain Reduction CV out to a CV input elsewhere (a synth's filter, a Combinator control, a level). The kick then drives the movement without any audio ducking. The manual says the CV exists; it does not give this exact recipe.
- **[Guess]** Pulsar has an envelope fired by MIDI notes or its gate input; it could also act as a ducker. Not verified. A video titled "Audio and Envelope Methods" suggests an envelope method exists. I haven't read it.

## Sources (summaries only)
- r/reasoners, "Anyone have suggestions on layering an 808 behind a kick?", 2024 — https://www.reddit.com/r/reasoners/comments/1f8uhxh/anyone_have_suggestions_on_layering_an_808_behind/
- Tornevalls, "Reason 13 sidechaining — Quickstart", 2024 — https://www.tornevalls.se/reason-13-sidechaining-quick-guide/ (Reason 13)
- Reason101.net, "Let's Talk Compression", 2010 — http://www.reason101.net/2010/10/23/36-lets-talk-compression/
- Reason Studios, "How to Make Trap Drums in Reason 10", 2018 — https://www.reasonstudios.com/news/post/how-make-trap-drums-in-reason-10
