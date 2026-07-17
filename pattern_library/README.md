# Beat Generator Drum Pattern Library

131 drum patterns as General MIDI files, organized by genre, with a machine-
readable `catalog.json` for your beat-generator project.

## Contents

```
drum_library/
├── catalog.json          # index of every pattern (metadata + file path)
├── MIDI/
│   ├── hip-hop/          # 42 patterns: boom-bap, trap, drill, lofi, neo-soul, R&B, cloud-rap
│   ├── electronic/       # 44 patterns: house, techno, dnb, jungle, garage, dubstep, trance, disco
│   └── rock/             # 45 patterns: rock, punk, metal, funk, soul, motown, reggae, blues shuffle
└── README.md
```

## MIDI format

- Each `.mid` is a 2-bar loop, standard MIDI (format 0), on **channel 10** (the
  General MIDI drum channel), so it maps to drum sounds in any DAW, sampler, or
  synth automatically.
- Tempo and time signature are embedded in each file (from the pattern's `bpm`
  and `time_signature`).
- Velocity is preserved: ghost notes (~50–65), normal hits (~95–105), accents
  (~115–125) — so grooves have dynamics, not flat robotic hits.

### General MIDI drum note map used

| Instrument   | Note | Instrument | Note |
|--------------|------|------------|------|
| kick         | 36   | crash      | 49   |
| snare        | 38   | ride       | 51   |
| side stick / rim | 37 | tom_low  | 41   |
| hand clap    | 39   | tom_mid    | 45   |
| closed hat   | 42   | tom_hi     | 50   |
| open hat     | 46   | shaker     | 82   |
| cowbell      | 56   |            |      |

## catalog.json

Each entry looks like:

```json
{
  "name": "Classic Boom-Bap Backbeat",
  "genre": "hip-hop",
  "subgenre": "boom-bap",
  "bpm": 90,
  "time_signature": "4/4",
  "steps": 16,
  "feel": "swung",
  "bars": 2,
  "instruments": ["kick", "snare", "closed_hat"],
  "midi_file": "MIDI/hip-hop/classic-boom-bap-backbeat.mid"
}
```

Use `catalog.json` to filter/select patterns programmatically inside your
generator (by genre, subgenre, bpm range, feel, or instrumentation).

## Regenerating / extending

The source step-grid data lives in `patterns_hiphop.json`,
`patterns_electronic.json`, and `patterns_rock.json` (one bar per pattern, each
track an array of per-step MIDI velocities, 0 = rest). Add or edit entries there
and re-run `build_library.py` to rebuild all MIDI files and the catalog. Change
`NUM_BARS` in that script to render longer loops.

## A note on sourcing

These are original, characteristic patterns of each style — the common musical
"grammar" of these genres (backbeats, four-on-the-floor, boom-bap swing, trap
hat rolls, the Amen-style breakbeat, etc.), not copies of specific copyrighted
recordings. They're safe to use, modify, and build on in your project.
