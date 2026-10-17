# Drums — Unique & Surprising Techniques

## Turning Kong into a played keyboard/piano-roll controller [Sourced — detailed]
The single most elaborate documented drum-adjacent technique found in this research. Origin: reason101.net, inspired by Native Instruments Maschine's "Pad Mode – Keyboard" feature, rebuilt from scratch in Reason using CV routing.

**What it does:** lets you play full chromatic melodic lines (not just fixed drum hits) from a 16-pad controller mapped to Kong, with two pads dedicated to octave-up/octave-down shifting.

**How it's built:**
1. Combinator containing: a 14:2 Mixer, a Kong (the trigger surface), two empty Thors (one labeled "Octave Up," one "Octave Down"), three CV Spider Merger/Splitters, and 13 NN-XT devices (one per semitone across a full octave, C to C).
2. Load the same melodic sample/patch (example used: a Wurlitzer piano) into all 13 NN-XTs. Set Pitch Semitone to 0 on the first, then increment by exactly 1 semitone on each subsequent NN-XT (1, 2, 3 … up to 12) — this gives you a full chromatic octave spread across 13 identical-sounding instruments instead of relying on a single sampler's own keyboard tracking.
3. Route Kong's Gate CV output from pad 1 into NN-XT #1's Gate CV input (and Osc Pitch CV input trim set to 127), then the same pattern for pads 2–13 into NN-XTs 2–13.
4. **Octave Up (pad 15)** and **Octave Down (pad 16)**: each drives a dedicated Thor used purely as a step-transposer (not as a synth voice) — Step Sequencer set to Run Mode "Step," 1 step only, that step's note set to C2 (Octave Up) or C4 (Octave Down). The Thor's own MBRS lines (`Seq.Note: 100 > S.Transp` and `Seq.Note: 100 > CV Out1`) convert a pad-hit into a CV transpose signal.
5. That transpose CV is fanned out to all 13 NN-XTs' Osc Pitch CV inputs via the three Spider CV Merger/Splitters, daisy-chained.
6. In the Combinator Programmer, "Receive Notes" is unchecked for every device except Kong — otherwise playing the Combinator's own sequencer track would trigger every NN-XT simultaneously instead of routing through Kong's pads.

**The one non-obvious "magic number":** the Spider trim knob on the octave-transpose CV path is set to **84** specifically — noted in the source as the value that makes the octave switching land correctly (not derived from first principles in the writeup, just stated as the working value).

**Why this belongs in your drums file rather than a synth file:** the whole point is repurposing Kong — a drum device — as the *playing surface* for melodic material, which is the surprising/creative part. The underlying "borrow CV to transpose a bank of samplers" idea generalizes to any Reason device with an Oscillator Pitch CV input (i.e., nearly all of them), per the original author's own closing note. [Source: reason101.net]

## Kong layering discipline (less exotic, still underused) [Sourced]
- Each Kong pad supports **two module slots**. A documented pattern for a thicker kick: a Synth Bass Drum in slot 1 for the sub/body, an NN-Nano loaded with a short transient/click sample in slot 2 — both trigger simultaneously on one pad hit, giving you sub weight and attack definition from a single hit without manually layering two separate tracks.
- **Mute groups**: assigning closed-hat and open-hat pads to the same mute group makes hitting the closed hat choke the open hat's ring, mimicking how a real hi-hat physically works. Commonly skipped by producers who program hats as two unrelated one-shots.
- **Hit type variation**: each pad can store up to 4 alternate hits that cycle or randomize per trigger — this is Kong's built-in answer to the "same snare sample every single hit sounds robotic" problem, without needing a separate randomization MIDI effect.
- **Bus FX vs per-pad FX vs Master section**: Kong has three distinct processing tiers (per-pad insert effects, two shared Bus FX sends for grouping e.g. all pads into one compressor, and a master section for the whole kit) — worth deliberately deciding which tier a given process belongs on rather than defaulting to per-pad inserts for everything. [Source: Audeobox, "Reason Kong Drum Designer"]

## Grain as a granular drum machine [Sourced — description level]
Reason Studios published a dedicated "Quick Tip" specifically repurposing **Grain** (built for melodic/textural granular synthesis) as a drum sampler instead — i.e., using granular playback modes on drum hits rather than melodic samples, for drum sounds with built-in micro-variation and texture that a standard one-shot sampler can't produce. The official Combinator patch demonstrating this was distributed alongside the tutorial video. [Source: Reason Studios]

## Sources
- reason101.net, "Kong Drum Creation A to Z" / NN-XT tag archive (Kong-as-keyboard writeup) — http://www.reason101.net/tag/nn-xt/
- Audeobox, "Reason Kong Drum Designer" — https://www.audeobox.com/learn/reason/kong-drum-designer/
- Reason Studios, "Build your own granular drum machine in Reason 11" — https://www.reasonstudios.com/news/post/build-your-own-granular-drum-machine-reason-11
