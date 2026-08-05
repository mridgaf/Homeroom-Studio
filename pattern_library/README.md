# Beat Generator Drum Pattern Library

193 drum patterns as General MIDI files, organized by genre, with a machine-
readable `catalog.json` for your beat-generator project. 180 of them are style
grammars; the other 13 are the famous figures in `patterns_breaks.json`, which
work differently — see the two sections at the bottom.

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

## patterns_breaks.json — the famous figures

`patterns_breaks.json` is a different kind of file from the other three, and
the difference matters.

The other files are **style grammars**: what a boom-bap beat or a house beat
generally does. This one is **thirteen specific drum performances**, written
out step by step — the Funky Drummer, the Amen, Impeach the President, Apache,
Assembly Line, Synthetic Substitution, Cold Sweat, Ashley's Roachclip, Get Out
of My Life Woman, Nautilus, Think (About It), When the Levee Breaks, and The
Big Beat. Each entry names its recording in a `source` field.

Two bars, 32 steps, three real velocity levels (118 accent / 100 hit / 55
ghost), because the ghosts between the accents are most of what makes one of
these sound like itself. The engine plays them **verbatim** — no thinning, no
variation, and the beat's variety pass is not allowed to touch those lanes.
Everything else in the library is treated as an influence and gets varied.

**Adding one:** put it in this file with `"subgenre": "breaks"`, 32 steps, and
a `source` line, then add a trigger word to `BREAK_WORDS` in
`tools/beat_machine.py` so the picker can offer it. `tests/test_breaks.py`
fails if a figure is in the pack that nothing can select.

## A note on sourcing

Two different things live in this folder, and only one of them is generic.

The genre files (`patterns_hiphop`, `patterns_electronic`, `patterns_rock`) are
original, characteristic patterns of each style — the common musical "grammar"
of those genres: backbeats, four-on-the-floor, boom-bap swing, trap hat rolls.
Not specific recordings.

`patterns_breaks.json` **is** transcriptions of specific recorded performances,
and says so in each entry's `source`. What is stored is the *pattern* — which
drum on which step, and how hard — the way a drum book or a MIDI groove pack
stores it. **No audio from any recording is used or included.** The figure is
played on your own drum samples, which is how every drum machine since the
SP-1200 has shipped a break. A drum pattern is not the sound recording; the
recording is what you must never copy, and none of it is here.

The hat lanes were written from published notation and have **not been
confirmed by ear** — treat them as a first draft until they've been through an
audition batch.
