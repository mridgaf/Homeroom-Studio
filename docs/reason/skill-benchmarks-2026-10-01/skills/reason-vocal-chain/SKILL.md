---
name: reason-vocal-chain
description: How to record, process and place a vocal in Reason 12.7 with stock devices. Insert chain order and starting settings (EQ, de-ess, two-stage compression), reverb and delay on sends, doubles and backing-vocal buses, Neptune pitch correction (natural vs robot, octave dub, harmonies) and the BV512 vocoder. Use whenever the owner asks for a vocal chain, "make my vocal sit", rap or singing vocal mixing, de-essing, vocal reverb or slapback, doubling, auto-tune or Neptune, vocoder or robot voice, or asks how to get a vocal "radio ready" in Reason. Reason 12.7 only; nothing has been heard, so settings are starting points.
---

# Reason 12.7 vocal chain

Sources: Reason 12.7 Operation Manual (ch. 6, 17, 52, 54, 57 to 61), a Reason Studios vocal-chain article written for Reason
13, Reason Studios articles on reverb and delay, and r/reasoners threads. Nothing here has been heard on this machine.
Tell him once, briefly, that the numbers are starting points to adjust by ear.

## How to answer
- Plain words, a short numbered chain, exact device and knob names. Say what each step is FOR in half a sentence, so he can
  decide whether to skip it.
- Fit the length to the question: one narrow question (just Neptune, just the vocoder) gets about 250 words or fewer. A full
  chain can be longer. Offer the next section in one line instead of writing it out.
- Reason 12.7 only. The Reason 13 and 14 devices that web tutorials use are NOT in 12.7: Gain Tool, Stereo Tool, Sidechain
  Tool, Ripley, RV-9. Use the 12.7 substitutes in the table. If a tip needs one of them, say "that is a Reason 13/14 device".
- Never type a knob name from memory. Copy from `device_refs/<device>.md` or `docs/reason/remote-vocab.json`
  (`tools/reason_vocab.py` does the same but only runs on the Mac with Reason installed). A near-miss name fails silently.
  Some controls have a panel label in the manual and a different Remote name: use the panel label when telling him what to
  click ("Filters To Dyn S/C", "HF Emph"), and the Remote name when writing automation or a remote map ("Filters Dyn S/C",
  "HF Emphasis").
- Mark each setting: manual, web (one person's opinion), or your own idea. Do not present a guess as a rule.

## Order of work (do not start mixing before steps 1 and 2)
1. **Record clean and dry**, peaks around -12 dB. A hot or distorted take can't be fixed later. Audio records DRY in Reason
   anyway; to hear effects while singing, route through effects as in `reason-mixer-chains` recipe 8.
2. **Comp the takes**: pick the best one, punch over single bad words.
3. **Tidy the audio**: even out loud and quiet words clip by clip, remove breaths you do not want, tune with Pitch Edit.
4. **Insert chain** (below).
5. **Sends**: a plate reverb and a delay.
6. **Doubles and backing vocals** on a bus.

## The insert chain (stock 12.7 devices; many small moves beat one big one)
The mixer channel strip already has input gain, gate, compressor, EQ, HPF and LPF, and processes them in the order Dynamics,
then EQ, then Insert FX (the **Insert Pre** and **Dyn Post EQ** buttons change that). The rack devices **Channel Dynamics** and
**Channel EQ** are the same circuits as devices. The order below is the order the sound travels.

| # | What | Starting point | Why |
|---|---|---|---|
| 1 | **Input Gain** (±18 dB, strip) | Level the signal going in. After any big EQ move, level-match again | Fair comparisons: louder always sounds better, so match level before you judge |
| 2 | **De-ess** (mono vocals; strip) | Strip compressor On, then **Filters To Dyn S/C** On, HPF set high so only "s" sounds trigger it, raise Ratio | Before the other compressors, so "s" does not trigger them. The strip's compressor comes first anyway |
| 3 | **Channel EQ device, HPF On** (Insert FX) | About 60 to 100 Hz | Removes rumble and plosive thumps. Use the DEVICE here: with Filters To Dyn S/C on, the strip's own HPF and LPF filter the compressor trigger, not the sound (the manual says those buttons are then unavailable in the Spectrum EQ window) |
| 4 | **MClass Equalizer** (cut mud) | Low shelf cut near 150 Hz, 6 to 8 dB. Boost a narrow band, sweep 300 to 500 Hz, find the ugly spot, turn it into a cut of about 3 dB | Cutting beats boosting |
| 5 | **Channel EQ device** (tone; can be the same device as step 3) | Presence boost 3 to 4 kHz, wide Q. Air: high shelf +3 to 4 dB from about 8 kHz | Clarity |
| 6 | **Channel Dynamics** (comp 1) | Ratio 2:1, about 2 dB of reduction, **Comp Peak On**, shortish Release | Catch peaks gently |
| 7 | **MClass Compressor** (comp 2) | 2:1 again, about 2 dB more | Two gentle stages sound less squashed than one at 6 dB |
| 8 | **Scream 4** (optional, parallel) | Tube or Tape, low **Damage Control**. Pull **Cut Lo** down | Body and warmth without losing the clean take |

- Watch the gain-reduction meter, not the knob positions.
- People disagree on EQ before or after the compressor. Pick one, then flip it and compare.
- Compress with **Mix** under 100% on Channel Dynamics for built-in parallel compression.

## Width and space (the lead stays centered and mono)
- **Reverb on a send, not an insert.** Plate suits vocals. More send plus lower fader = farther away. Less send plus higher fader
  = closer. Cutting the reverb's own lows (RV7000 EQ page) keeps it from muddying the mix. Predelay about 20 to 40 ms keeps
  words clear.
- **Delay with ducking**: **The Echo** on a send at 100% wet, **Ducking** on, so repeats drop while he sings and rise in the gaps.
- **Slapback plus a plate** is a common lead setup.
- **Width** comes from the sends, not from widening the lead. The MClass Stereo Imager can't widen a mono signal. For a stereo
  delay, The Echo's **Right Ch Time Offset** gives a left/right time difference (an idea adapted from a 13/14 tool; not tested).
- **PRE** on a send keeps the effect level steady when you ride the vocal fader.
- Send steps: `reason-mixer-chains` recipe 2.

## Doubles, harmonies, backing vocals
- **Dub** (Transport) copies a track including its insert effects, so every layer gets the same chain.
- Route all doubles to one **Output Bus** (select channels, Cmd+G) and put shared effects on the bus once.
- Use the best take loud, and 2 to 3 other takes very quiet beneath it. If it sounds like several voices, it is too loud.
- Line doubles up with Slice Edit.
- Print a backing-vocal stem: Rec Source on the bus (see `reason-mixer-chains` recipe 9).

## Neptune (pitch, harmony, octave) manual ch. 54
Control names below are the Remote names (`device_refs/neptune.md`): **Pitch Adjust On/Off**, **Correction Speed**,
**Preserve Expression**, **Formant On/Off**, **Formant Shift**, **Transpose On/Off**, **Semitones**, **Cent**.
- **Natural tune**: Neptune as an INSERT. Pitch Adjust On, set the key and **Scale**, **Correction Speed** around the middle
  (the device guide says the middle sounds natural; turning it up gives the stepped robot sound), **Formant On** so notes keep
  their character. **Preserve Expression** keeps the singer's own vibrato during fast correction.
- **Hard robot tune**: Correction Speed to max, **Preserve Expression** to minimum.
- **Fix only the flat bits**: give Neptune a sequencer track and automate its **Pitch Adjust** button On only for bad passages.
- **Change the singer's character**: Pitch Adjust and Formant on, move **Formant Shift** down (deeper) or up.
- **Octave dub**: a SECOND Neptune on a SEND (the insert keeps doing the natural tune), Pitch Adjust OFF, Transpose ON,
  **Semitones** +12, Formant On, balance with the channel's send knob until it is barely there. Idea, not tested: automate that
  send level so the double is only up in the chorus.
- **Harmonies**: Neptune as an insert, send MIDI to the **Voice Synth** (from its track or a keyboard); the Voice Synth jacks
  can feed their own Mix Channel.
- Robotic by accident? Back Correction Speed off from its maximum, check the Scale matches the song, keep the Formant section
  on. (Not a manual step; it follows from the two settings above. Try it by ear.)

## BV512 vocoder (manual ch. 52)
- Needs two signals: a **carrier** (a bright, sustained synth such as a Subtractor sawtooth with the filter fairly open) and a
  **modulator** (his voice). With no notes played on the carrier you hear nothing.
- Setup: create the carrier synth, select it, create a BV512 (it auto-inserts via the Carrier jacks). Patch the audio interface
  input to the **Modulator Input** on the back (Ctrl-click the jack, or flip the rack with Tab). Master Keyboard Input on the
  carrier's track so you can play it. **Dry/Wet fully Wet**. Raise **HF Emph** (Remote name HF Emphasis) if muddy.
- To print the result: Rec Source on the vocoder's Mix Channel, a new Audio Track with that as its input, arm only the Audio
  Track (`reason-mixer-chains` recipe 8 has the same pattern).
- Band count: fewer bands (4, 8, 16) sound more robotic, and one forum user finds they sit better in a mix than 32. Try 16
  first. **FFT** mode is clearest for speech and singing.
- To vocode an existing audio track, patch that track's left **Insert FX To Device** jack into the Modulator Input.
- A vocoder output is already in tune with the keys, so Neptune after it has nothing to fix.

## Go deeper
`docs/reason/techniques/vocals.md` (same material with source URLs and a Combinator-macro idea), `docs/reason/manual-digest/recording.md`
(levels, loop recording, comping), `docs/reason/manual-digest/audio-editing.md` (Slice Edit, Pitch Edit), device guides in
`device_refs/` (channel-dynamics, channel-eq, mclass-equalizer, mclass-compressor, scream-4, rv7000-mkii, the-echo, neptune, bv512).
