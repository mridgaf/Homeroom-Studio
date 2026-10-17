---
name: reason-drum-bus
description: How to route, glue and add punch to drums in Reason 12.7. Getting each drum from Kong, Redrum or Dr. Octo Rex onto its own mixer channel, building a drum bus with glue compression, parallel compression (Mix knob, Parallel Channel, Spider split), saturation and grit, one shared room, kick-and-808 relationship, kick ducking the bass, plus trap and industrial pattern recipes. Use whenever the owner says his drums sound thin, flat, separate, weak, "not glued", asks how to route a kit, make a drum bus, parallel-compress drums, make hats roll, build a trap or boom-bap or industrial beat chain, or get the kick and 808 to stop fighting in Reason. Reason 12.7 only; nothing has been heard.
---

# Reason 12.7 drum routing and drum bus

Sources: Reason 12.7 Operation Manual (ch. 17 mixer, 27 Kong, 28 Redrum, 29 Dr. Octo Rex, 59 compressors), Reason Studios
articles (a trap drums piece, a 2025 industrial house piece), r/reasoners threads. Nothing here has been heard on this
machine. Tell him once, briefly, that settings are starting points.

## How to answer
- Plain words, short numbered steps, exact button and knob names. Name the cheapest fix first (usually a Mix knob), then the
  heavier one.
- Fit the length to the question: about 300 words or fewer unless he asks for the full setup. Offer the next piece in one line.
- Reason 12.7 only. NOT in 12.7: Sidechain Tool, Gain Tool, Stereo Tool, Ripley, RV-9. Use the cable method below.
- Knob names: never from memory. `device_refs/kong.md`, `redrum.md`, `master-bus-compressor.md`, `scream-4.md`, or
  `docs/reason/remote-vocab.json` (`tools/reason_vocab.py` does the same but only runs on the Mac with Reason installed).
- Separate what the manual says from web opinion and from your own idea. One short flag each, no more.
- Don't split everything by default. Split a drum onto its own channel only when it needs its own treatment (EQ, compressor,
  bus, sidechain). Level and pan can be done inside the drum device.

## 1. Get each drum onto its own channel
| Device | How |
|---|---|
| **Redrum** | Every drum has its own output jack on the back. Cable one out and that drum is **removed from Redrum's main stereo out**, so it is not heard twice. Mono sound: use the Left (Mono) jack. Ctrl-click the jack and pick "new Mix Channel". Per-drum **Send 1 / Send 2** feed Send Out 1 and 2 for per-drum effects |
| **Kong** | Pick the pad's destination with the **Drum Output** selector (bottom of the Drum and FX section). Master FX = normal, with Bus FX acting as a send. Outputs 3-4 up to 15-16 go to their own jack pairs. These are NEVER auto-routed. Cable them to a Mix Channel yourself |
| **Dr. Octo Rex** | Slices can go to their own jacks with the slice **Output** setting (1 to 8) |
| A MIDI drum clip already recorded | **Explode** (Tool Window, F8) makes one clip per drum pitch. Give each lane its own ReGroove channel, or bounce each to audio |

## 2. The drum bus
1. Drums on their own Mix Channels.
2. Select them, **Cmd+G** (Route to New Output Bus). Rename it "Drums".
3. If you layer, sub-bus similar sounds first (two snares to a "Snares" bus, then to Drums).
4. Per channel: only the compression or saturation that drum needs. On the bus: glue and/or saturation. Reverb on a send.
5. Glue: select the Drums bus channel and create a **Master Bus Compressor** (SSL-style); it lands in that channel's Insert FX.
   **Ratio 2:1**, **Mix 100%**, aim for **1 to 3 dB** of reduction, **Attack 10 to 30 ms** so the hits still punch through. Or
   **MClass Compressor** with a slowish attack (30 ms or more). Watch the reduction meter. This is the glue compressor, so
   leave Mix at 100%.
6. Kong shortcut: put a Compressor in Kong's **Master FX** for glue across the whole kit without any routing.
7. Redrum with no bus yet: select the Redrum and create the compressor; it is inserted between Redrum and its Mix Channel. The
   catch: a drum you cabled out of its own jack is no longer in Redrum's main stereo out, so a compressor on Redrum does not touch
   it. Build the bus once you split drums out.
Cable steps for buses, sends and parallel: `reason-mixer-chains` recipes 2, 3, 4.

## 3. Punch AND weight: parallel compression (cheapest first)
1. **Mix knob**: a SECOND compressor on the drum bus (a glue compressor at Mix 100% and a parallel one need two devices).
   Channel Dynamics or Master Bus Compressor, **Mix** about 30 to 50%, Ratio high, compress hard. No cables.
2. **Parallel Channel**: select the Drums bus, Create Parallel Channel, turn on its compressor with a high Ratio, blend its
   fader under the dry bus. (The manual's own example.)
3. **Spider split**: bus out into a Spider Audio splitter, one clean path plus effect-only paths (a reverb, a Scream 4), each
   on its own mixer channel. The clean beat stays as the backbone.
It is common to parallel-compress only the kick or snare, not the whole kit.

## 4. Grit and glue
- Saturation per drum, and on the bus. When the kick pushes the bus into the saturation, hats and shakers get squashed and
  gritty with it. That is the "edge of breakup" feel.
- Tools in 12.7: **Scream 4** (Tape or Tube = warm, Overdrive = harder) and **MClass Maximizer**. A hard clipper is not in
  the box. In parallel, pull Scream 4's **Cut Lo** down so the low end stays clean. Keep Damage Control in the 20 to 60 range.
- ONE subtle room send shared by the whole kit makes it sound played in one space. Don't wash it. Gated 80s snare: RV7000's
  Gate section. How to wire it: put a send reverb on the Master Section (Create Send FX, `reason-mixer-chains` recipe 2) and
  turn the Drums bus's send up a little. Redrum's own per-drum **Send 1 / Send 2 Amount** go to the Mixer's first two Chaining
  Aux inputs and only work if send effects exist there. For a drum bus, the bus send is the simpler route.

## 5. Kick, 808 and the bass
- Two sounds cannot own the same low notes. Separate them by **pitch** or by **time**.
- Treat the kick as the **attack** and the 808 as the **sustain**. Keep the kick's low end short; give the 808 a long decay or
  delay it 10 to 50 ms (back off if you hear two hits). Add light saturation to the 808 so it shows on small speakers.
- Kick ducks the bass: see `reason-mixer-chains` recipe 5 (kick channel's Parallel Out to the bass compressor's Sidechain
  input, KEY lights). A drum machine's kick must be on its own channel first (table above).
- Details, EQ separation, building an 808 from a synth: `docs/reason/techniques/bass-and-low-end.md`.

## 6. Pattern recipes
**Trap** (web: Reason Studios, 2018): 60 to 90 BPM, clap or snare on 2 and 4. Hats: write straight 16ths, then vary with
triplets, 32nds and bursts of 64ths at phrase ends; Quantize changes the rhythm feel. 808 kick on beat 1, space on 3, a few
on the "and" around 3. A second long-sustain 808, pitch changed per note, becomes the bassline.

**Redrum rolls and accents**: Flam button then add a step; flams on steps in a row make a roll; the Flam knob can give 1/32
on a 1/16 grid. Set a channel's **Vel** knob off zero or accents are inaudible. Redrum hat choke: **Channel 8 & 9 Exclusive** on.

**Kong hat choke and variation** (manual ch. 27, "Working with Pad Groups"): Kong has 9 pad groups: 3 Mute, 3 Link, 3 Alt.
Click **Quick Edit** in the Pad Group section; every pad then shows its group letters. Click the SAME Mute Group letter on the
closed-hat pad and the open-hat pad (the manual's example uses letter B for a Mute Group and G for an Alt Group; so A to C are
probably the Mute letters, D to F Link, G to I Alt. That split is my inference from the example, so read the letters on screen).
Click Quick Edit again or press Esc to leave. An **Alt Group** makes the pads in it fire in random order, so no two hits match.
Fast rolls: each pad answers three MIDI keys in the C3 to B6 range, so you can play or draw quick repeats.

**Industrial deep house** (web: Reason Studios, 2025): low kick with a long "subby" tail, four on the floor, short metallic
hats, shakers for movement, a clap with a long tail. Send a half-speed noise clap through a delay (high feedback) and raise
the delay's dry/wet over the loop for a build. Parallel: an RV7000 for space and a Scream 4 for scuzz via a Spider split.

## 7. Idea for later (not tested)
One Combinator holding Redrum, per-drum Mix Channels, an Output Bus, Master Bus Compressor (Mix) and Scream 4 (parallel), with
macro knobs Glue (Comp Threshold), Parallel (Mix), Grit (Scream Damage Control), Space (reverb send). Cables to anything
outside a Combinator are not saved, so keep all of it inside.

## Go deeper (files in the Homeroom Studio project folder; skip if they are not there)
`docs/reason/techniques/drums.md` (same material with source URLs), `docs/reason/manual-digest/drum-devices.md` (Kong, Redrum
and Dr. Octo Rex in detail), `docs/reason/techniques/bass-and-low-end.md`, `docs/reason/manual-digest/routing-and-main-mixer.md`.
