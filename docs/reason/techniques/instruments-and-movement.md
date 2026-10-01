# Instruments (synths, keys, guitar) and making them move
Tags: **[Manual]** 12.7 manual. **[Web]** web source. **[Guess]** my idea, untested. Nothing here has been heard on our machine.

## 1. Record clean, hear it dressed (guitar, bass, any live instrument)
- Put the effect/amp as an **insert on the Audio Track**. You hear it while playing and recording, but Reason records the **clean** signal. You can change the tone later. [Manual ch. 6 (monitoring), Web: Sound on Sound 2017]
- Built-in guitar tools: **Softube Amp** and **Softube Bass Amp** (amp + cabinet pairs; buttons choose amp and cab). The half-width effects (the old Reason pedals-style set) work as guitar pedals. The Echo suits chorus/delay on guitar. [Web: SOS, device_refs/guitar-amps.md]
- Save a chain you like: select the Audio Track › **File › Export › Insert FX Patch…** saves it as a Combinator .cmb. Later, drag it onto any Audio Track. Browse them via **Edit › Browse Insert FX Patches**. [Manual ch. 69, ch. 15; Web: SOS]
- Monitor externally if latency bothers you (Preferences › Audio: External/Manual). With Automatic monitoring through Reason there is no latency compensation, so keep the audio buffer small (SOS used 64 samples). [Web: SOS; Manual ch. 6]
- Built-in **Tuner** on every audio track. [Manual]
- Amp-in-a-box approach: record the mic'd amp dry/direct plus the amp mic and choose later. [Guess; not researched]

## 2. Pads and keys: separate by frequency
- Give every part its own band: high-pass what doesn't need lows, low-pass what doesn't need highs. This opens the mix up more than most EQ boosts. [Web: r/reasoners user]
- Tools: **Channel EQ** HPF (18 dB/oct, 20 Hz–4 kHz) and LPF (12 dB/oct). [device_refs/channel-eq.md]
- Narrow the lows of a wide pad: **MClass Stereo Imager** with Low Width to the left of centre, High Width a little to the right. Needs a stereo signal. [device_refs]
- Put pads far back: more reverb send + a bit lower fader. [Web: Record U]
- Choose the same reverb for everything you want to "sit in the same room", a different reverb or a delay for the part that should stand out. [Web: Record U]
- **Layers and splits** inside one Combi: key ranges and velocity ranges. See `../manual-digest/combinator.md` section 1.
- **Rhythmic gate / chopped pad:** Channel Dynamics gate with **Sidechain** keyed from a drum loop. [device_refs; Manual recipe G]

## 3. Make it move without drawing automation
### Pulsar (dual LFO) as a "player" [Web: Ron Headback, Reason Studios 2025 + device_refs/pulsar.md]
1. On the instrument's back panel, set up its **CV 1–4 inputs** (Europa has these) and choose what each controls: e.g. CV1 = filter frequency, CV2 = resonance, CV3 = phaser amount, CV4 = delay amount. Tip from the video: drag the small arrow onto the parameter on the front to assign it.
2. Cable Pulsar CV outputs to those inputs.
3. Use the **Phase, Shuffle and Lag** settings so the movement doesn't sound like a loop. Different slow rates for different targets.
4. Let a second Pulsar LFO modulate the first one's Level (or Rate) so the amount keeps changing.
5. VST plug-ins have a **CV programmer** (8 CVs) you can assign to plug-in parameters, then drive from Pulsar. [Web]
6. Some players/devices have CV inputs for gate length. Modulating gate length moves between short staccato and sliding legato on acid-style lines. [Web]
- Warning: CV cables are NOT saved with a single device's patch. Put the whole thing in a Combinator. [device_refs/pulsar.md]

### Combinator knobs [Manual]
- One knob → several parameters, forwards or reversed, over part of the knob's travel. `../manual-digest/combinator.md` section 3.
- Knob moves record as automation. [Manual]
- Free Reason Studios packs advise playing with the Combinator's macro knobs and mod wheel to find sounds. [Web: Reason Studios news, 2020]

### Real-time control and recording [Manual]
- Map hardware to ANY parameter with Remote Override + Learn. `../manual-digest/remote-control.md`
- Record the movement as parameter automation, then thin it with Automation Cleanup, bend it with curves. `../manual-digest/recording.md`, `../manual-digest/note-and-automation-editing.md`
- Record automation INTO the note clip so a riff and its filter move travel together (Options › Record Automation into Note Clip). [Manual]

## 4. Players: let Reason write variations [Manual]
Arpeggiator/Chord/Scale-type Players generate notes while you record. See `../manual-digest/players.md`.
Groove: ReGroove Mixer + the `reason-regroove` skill. Variation on Dr. Octo Rex loops: **Alter Notes** (tool in `../manual-digest/note-and-automation-editing.md`).

## 5. Ideas to try [Guess]
- A "pad mover" Combi: pad synth + Channel EQ + The Echo + Pulsar inside; knobs = Cutoff, Movement (Pulsar Level), Space (Echo Dry/Wet), Width.
- A "stab" Combi (Europa + Pulsar as in the video) with a Lurch/Intensity macro.

## Not researched yet
Kong pad design, Thor/Europa sound design from scratch, Mimic, sampler instruments (NN-XT/NN-19), Radical Piano, Klang, Pangea, Rytmik, ID8. Device refs in `device_refs/` have the basics.

## Sources (summaries only)
- Sound On Sound, "Recording Guitar & Bass In Reason", Simon Sherbourne, 2017 — https://www.soundonsound.com/techniques/recording-guitar-bass-reason
- Reason Studios, "Darkroom Deep House Music with Pulsar" (Ron Headback), 2025 — https://www.reasonstudios.com/news/post/pulsar-europa-and-moody-darkroom-house
- Reason Studios, "Tools for Mixing: Reverb" (Record U), 2006 — https://www.reasonstudios.com/news/post/tools-for-mixing-reverb
- r/reasoners, "How do you mix vocals like a pro in Reason Studios?" (the frequency-separation tip), 2023 — https://www.reddit.com/r/reasoners/comments/188sr82/how_do_you_mix_vocals_like_a_pro_in_reason_studios/
