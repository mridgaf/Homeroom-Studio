# Objekt Clean-Room Rebuild

A working, from-scratch physical-modeling synthesizer inspired by the published architecture of Reason Studios' Objekt.

This project does **not** copy Reason Studios code, patches, artwork, binary data, or proprietary device files. It implements the documented ideas independently: impact/noise excitation, an eight-mode resonator bank, two eight-line feedback-delay waveguide objects, routing, mixing, effects, external excitation, seeded randomization, and polyphonic offline rendering.

## VST3 deliverable

The requested product level is now **plugin**. Acceptance criteria:

1. A native Apple-silicon VST3 bundle is built and copied to the user's VST3 folder.
2. MIDI note-on/note-off produces finite, non-silent stereo audio in real time.
3. At least eight overlapping voices work.
4. Host-visible parameters automate the main exciter, modal, object, mixer, and effect controls.
5. Plugin state saves and restores through the VST3 host interface.
6. The bundle passes an automated plugin validator and is discovered by at least one installed host before it is called usable.
7. The existing offline renderer and its tests continue to pass.

The VST3 is a clean-room instrument named **Objekt Rebuild**. It does not use Reason Studios branding, artwork, factory patches, code, or binaries.

## What works

- Impact and noise exciters with velocity response
- External audio as an exciter
- Eight-mode tuned resonator bank
- Two eight-line tuned feedback-delay arrays
- Modal -> Object 1 -> Object 2 routing
- Decay, damping, dispersion, collision, pitch deformation, coupling, polarity, pan, and level controls
- EQ, distortion, compression, ping-pong delay, and algorithmic stereo reverb
- Seeded patch randomizer
- Polyphonic event rendering
- Four factory-style clean-room presets
- Stereo 16-bit WAV output
- Native Apple-silicon VST3 instrument
- Real-time MIDI input with eight-voice polyphony
- Sixteen automatable parameters and four host programs
- Host state save/restore and a generic parameter editor
- Tests for determinism, pitch tracking, external excitation, randomization, presets, file output, real-time DSP, plugin state, and host processing

## Run it

From this folder:

```bash
python3 -m objekt.cli --preset glass_bell --note 60 --duration 2.5 --output artifacts/my-bell.wav
```

Available presets:

- `glass_bell`
- `wood_mallet`
- `metal_plate`
- `imaginary_string`

Randomized variation:

```bash
python3 -m objekt.cli --preset imaginary_string --note 45 --randomize 0.25 --seed 44 --output artifacts/variation.wav
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Render the demonstration phrase:

```bash
python3 demo.py
```

## VST3 installation and use

The built plugin is installed at:

```text
~/Library/Audio/Plug-Ins/VST3/Objekt Rebuild.vst3
```

It appears in a host as **Objekt Rebuild (Homeroom Studio)** under VST3 instruments. Restart or rescan the host after installing. The editor is JUCE's generic parameter editor, so every exposed parameter is immediately usable and automatable.

Build from source:

```bash
cd vst3
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --target ObjektRebuild_VST3
```

The build fetches JUCE 9.0.4. This is a private local build; obtain appropriate JUCE licensing before distributing binaries outside the applicable open-source licence terms.

## Public seams

The behavior tests intentionally use two public boundaries:

1. `ObjektConfig -> ObjektSynth.render_note/render_sequence -> stereo float audio`
2. `stereo float audio -> write_wav -> stereo PCM WAV`
3. `MIDI + host parameters -> VST3 processor -> real-time stereo audio and saved host state`

## Important limit

This is a functional clean-room reconstruction, not a bit-identical clone. Exact Objekt algorithms, nonlinearities, templates, patch data, UI, Rack Extension integration, modulation timing, and parameter curves are proprietary and cannot be established from the manual alone. `PARITY.md` records what is implemented, approximated, or still unverified.

## Sources

- `research/Objekt_Operation_Manual.pdf` — Reason Studios, 2023
- Official online manual: `docs.reasonstudios.com/plusre/objekt-modeling-synthesizer`

The downloaded manual SHA-256 is recorded in `research/SOURCES.md`.
