# Objekt Rebuild VST3

## Installed plugin

`~/Library/Audio/Plug-Ins/VST3/Objekt Rebuild.vst3`

Host name: **Objekt Rebuild (Homeroom Studio)**

## Features

- Native arm64 VST3 instrument
- Eight-voice real-time MIDI polyphony
- Stereo output, zero reported latency
- Four programs: Glass Bell, Wood Mallet, Metal Plate, Imaginary String
- Sixteen automatable parameters
- Generic host editor
- Host state save and restoration

## Build

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --target ObjektRebuild_VST3
```

Built bundle:

`build/ObjektRebuild_artefacts/Release/VST3/Objekt Rebuild.vst3`

## Verification performed

- CTest DSP engine test: passed
- CTest JUCE processor/audio/state test: passed
- Existing Python renderer tests: 6 passed
- pluginval 1.0.4 strictness 10: SUCCESS
  - Editor and editor-during-processing
  - 44.1, 48, and 96 kHz
  - 64, 128, 256, 512, and 1024 sample blocks
  - Automation and editor automation
  - State and state restoration
  - Background-thread state
  - Parameter thread safety and fuzzing
  - Bus configuration
- REAPER arm64 scanner: discovered the plugin
- REAPER project: loaded and saved the plugin state
- REAPER `-peaktest`: rendered MIDI C4 through the installed VST3, peak `+-0.01 dB at 0:01.161`
- Installed bundle: ad-hoc signed and verified by `codesign --deep --strict`

## Scope

This is an independently written clean-room instrument. It is not a Reason Rack Extension and does not claim exact audio parity with Reason Studios Objekt.
