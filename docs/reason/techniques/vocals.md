# Vocals — recording, chain, space
Built from: Manual (ch. 6, 17, 57–61), Reason Studios articles, and r/reasoners advice. Nothing here has been heard on our machine. Knob names follow `device_refs/`.

Tags: **[Manual]** = Reason 12.7 manual. **[Web]** = a web source, URL at the bottom. **[Guess]** = my own idea, untested.

## 1. Order of work (the big picture)
1. Record clean, **dry**, at about −12 dB peaks. [Manual] → details in `../manual-digest/recording.md`
2. Take-pick (comp) and fix single words by punching over them. [Manual]
3. Tidy the audio: even out levels clip by clip, remove breaths you don't want, fix timing of doubles with Slice Edit, tune in Pitch Edit. [Web: r/reasoners]
4. Insert chain on the channel (below).
5. Sends: plate reverb + a delay. [Web, Manual]
6. Stack/bus doubles and backing vocals. [Manual, Web]

## 2. The insert chain (Reason 12.7 devices only)
Suggested order, assembled from the sources. Each step is small. Many gentle moves beat one big one. [Web: both agree]

| # | Device | What to do | Where it comes from |
|---|---|---|---|
| 1 | Channel Dynamics → **Input Gain** (±18 dB) | Level the signal going in. Re-check level after every big EQ move | [Web] R13 article used a Gain Tool; that device isn't in 12.7, Input Gain does the job |
| 2 | **Channel EQ** → HPF On | HPF about 60–100 Hz. Do it in the Channel EQ DEVICE, not the strip's HPF, if you de-ess with the strip (row 3): [Manual ch. 17] with Filters To Dyn S/C on, the strip's HPF/LPF filter the compressor trigger, not the sound | [Web] 60 Hz (R13 article), "at least 100 Hz" (r/reasoners user) |
| 3 | De-ess (mono vocals only) | Mixer channel strip: compressor on, then **Filters To Dyn S/C**; the HPF/LPF now filter only what triggers the compressor, so set the HPF high and only "s" sounds clamp down. Or MClass EQ with a boosted "S" band into a compressor's sidechain | [Manual] recipe F in `routing-and-main-mixer.md`. [Web] put the de-esser BEFORE the compressors so "S" doesn't trigger them |
| 4 | **MClass Equalizer** (surgical) | Low shelf cut around 150 Hz (6–8 dB). Find mud: boost a narrow band, sweep 300–500 Hz, turn the nasty spot into a ~3 dB cut | [Web] R13 article |
| 5 | **Channel EQ** (tone) | Presence boost 3–4 kHz, wide Q. Air: +3–4 dB high shelf from about 8 kHz | [Web] |
| 6 | Compressor stage 1: **Channel Dynamics** | Ratio 2:1, about 2 dB reduction, **Comp Peak On**, shortish Release | [Web] |
| 7 | Compressor stage 2: **MClass Compressor** | 2:1 again, about 2 more dB. Smooths, "glues" | [Web] |
| 8 | **Scream 4** (optional, parallel) | Tube or Tape type, low Damage. Blend in parallel to keep body. Use Cut Lo to keep mud out | [Guess] based on device_refs/scream-4.md |

- EQ-before-compressor vs after: people disagree. Pick one and compare. [Web]
- Why serial compression: two compressors doing ~2 dB each sound less squashed than one doing 6. [Web]
- Check the gain-reduction meter, not the knob positions. [Manual device guides]

### Level-matching rule
Every time a move makes the vocal quieter, bring the level back (Input Gain or EQ Gain) before judging. The point is to sound better, not louder. [Web]

## 3. Width and space
- Keep the LEAD vocal in the middle and mono. Put width in the sends. [Web]
- **Stereo width tool:** the R13 Stereo Tool is NOT in 12.7. The **MClass Stereo Imager** can't make stereo from mono (device guide). So widen with a stereo delay on a send: The Echo → **Right Ch Time Offset** gives left/right time difference. [Web idea from Ripley's Offset knob, applied with a 12.7 device = Guess]
- **Reverb on a send, not an insert.** Plate works well on vocals. [Web: Reason Studios "Tools for Mixing: Reverb", Manual]
  - More send + lower fader = farther away. Less send + higher fader = closer. [Web]
  - Cut the lows/low-mids of the reverb itself with the RV7000's built-in EQ (the article cranked the Low EQ down at its highest frequency, 1 kHz, as a high-pass). Stops mud. [Web]
  - Predelay 20–40 ms helps the words stay clear. [device_refs/rv7000-mkii.md]
- **Delay with ducking:** The Echo → **Ducking** lowers the repeats while the singer is singing and raises them in the gaps, so words stay clear. Put it on a send at 100 % wet. [Web: Reason Studios delay article, device_refs/the-echo.md]
- **Slapback + reverb** is a common lead setup. [Web: r/reasoners]
- **Pre-fader sends** (Pre button) keep the effect level steady when you automate the vocal fader down; post-fader sends follow the fader. [Web: Record U]

## 4. Doubles, harmonies, backing vocals
- **Dub** on the Transport copies the track INCLUDING insert FX, so every layer gets the same chain. [Manual]
- Send all doubles to an **Output Bus** (select channels, Cmd+G) and put shared effects once on the bus. [Manual, Web]
- Pick the best take. Mix 2–3 other takes in very quietly under it. "If it sounds like several voices, it's too loud." [Web]
- Line up doubles by timing with Slice Edit (tedious but works). [Web]
- A stem of backing vocals: Master Section **Rec Source** + Solo + Stereo input. Fader moves can be performed live while it records. [Manual]

## 5. Make a vocal Combi (idea for us) [Guess]
The R13 "SLAP GURU" patch (not downloadable for 12; built from R13 devices) used 8 knobs: Rumble & Mud, Presence & Air, Parallel Comp, Tape & Dist, Octave Down, etc. We can build our own with 12.7 devices using the Combinator mapping rules in `../manual-digest/combinator.md`:
| Knob | Maps to |
|---|---|
| Rumble | Channel EQ HPF Frequency |
| Mud | MClass EQ Parametric 1 Gain (narrow band ~350 Hz, cut) |
| Presence | Channel EQ HMF Gain |
| Air | Channel EQ HF Gain |
| Squash | Channel Dynamics Comp Threshold |
| Body | Channel Dynamics Mix (parallel) |
| Dirt | Scream 4 Damage Control |
| Space | Send level / Echo Dry/Wet |
- Need: a way to test it by ear. **Nobody has heard this.** Needs his listening.

## 6. Pitch and vocal effects
### Neptune (pitch correction, harmony, octave) [Manual ch. 54]
- **Natural-sounding tune:** Neptune as an INSERT on the vocal. Set the **Scale**, a moderate **Correction Speed**, turn the **Formant** section on so corrected notes keep their original character.
- **Hard "robot" tune:** Correction Speed to max and **Preserve Expression** to minimum.
- **Only fix the flat bits:** give Neptune a sequencer track, automate its **Pitch Adjust** button On only for the bad passages. For notes the scale would get wrong, set MIDI Input to Pitch Adjust and play the right notes on the keyboard for that stretch. You can freeze the result afterwards.
- **Change the singer's character:** Pitch Adjust + Formant on, move Formant **Shift** down (deeper) or up (more female-sounding).
- **Octave dub:** Neptune on a SEND, Pitch Adjust off, Transpose on, **Semitones** +12 (that is the Remote name), balance with the channel's send knob, tweak Formant Shift to taste.
- **Harmonies:** Neptune as insert, MIDI to the **Voice Synth** from the Neptune track or your keyboard; the Voice Synth breakout jacks can go to their own Mix Channel for separate processing.
- Pitch-shift drums: Pitch Adjust off, Transpose on.
- Graphical pitch editing exists too: Pitch Edit mode in the sequencer (see `../manual-digest/audio-editing.md`).

### BV512 vocoder [Manual ch. 52]
- Needs two signals: **carrier** (a bright, sustained synth, for example a Subtractor sawtooth with the filter fairly open) and **modulator** (your voice). Output = talking synth. Without notes played on the carrier you hear nothing (vocoders need musical input). [Manual; the r/reasoners thread says the same]
- Setup: create the carrier synth, select it, create a BV512 (it auto-routes as an insert via the Carrier jacks). Patch the audio interface input to the **Modulator Input** on the back. Master Keyboard Input on the carrier's track. **Dry/Wet fully Wet**. Raise **HF Emph** (Remote name: HF Emphasis) if muddy.
- Fewer bands (4/8/16) can sound better in a mix than 32. **FFT** mode is clearest for speech and singing, bad for drums (adds ~20 ms delay).
- Vocoding an existing audio track: patch the audio track's left **Insert FX To Device** jack into the Modulator Input.
- Record the vocoded result: Rec Source on the vocoder's Mix Channel, new audio track set to that input, arm only the audio track.
- BV512 in **Equalizer** mode = a graphic EQ with colour (4–32 band colours the sound even flat). FFT mode flat = no change.
- A forum user's note: a vocoder output is already perfectly in tune with the keys played, so Neptune afterwards has nothing to correct. For a robot voice without keys, use Neptune with notes limited to a few scale notes and fast correction. [Web: r/reasoners]

## Sources (summaries only, no copied text)
- Reason Studios, "How to Build a Vocal Chain in Reason 13" (Yana Mahal), 2024 — https://www.reasonstudios.com/news/post/build-an-epic-vocal-chain-in-reason-13 (R13 devices; numbers above are hers, adapt by ear)
- Reason Studios, "Tools for Mixing: Reverb" (Record U), 2006 — https://www.reasonstudios.com/news/post/tools-for-mixing-reverb
- r/reasoners thread on Neptune + vocoder, 2023 — https://www.reddit.com/r/reasoners/comments/134xy1f/i_can_never_get_neptune_to_play_nice_with/ (only the explanation by one user was used; a pasted chatbot answer in it is wrong)
- Reason Studios, "How to Use Delay in Reason 10", 2018 — https://www.reasonstudios.com/news/post/how-use-delay-in-reason-10
- r/reasoners thread "How do you mix vocals like a pro in Reason Studios?", 2023 — https://www.reddit.com/r/reasoners/comments/188sr82/how_do_you_mix_vocals_like_a_pro_in_reason_studios/ (individual users' opinions)
