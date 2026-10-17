# Device inventory report

Built by build_inventory.py from the files in /home/claude/pmwork/in only. Being in remote-vocab means "Reason has a Remote map for it", not that the owner has it.

## Counts

- Rows in inventory.csv: 151 (148 from remote-vocab ids + 3 not in remote-vocab: Rytmik Drum Machine, MIDI Out Device, Softube Amps)
- In remote-vocab: 148 (one row per vocab id; vocab file says device_count = 148)
- Made by Propellerheads / Propellerhead Software (manufacturer strings in the file; "Reason Studios" does not appear in the file): 97; other makers: 51
- With our guide: 50 rows (56 guide files total: 50 joined, 5 hardware, 1 undecided)
- With our remotemap scope: 48 (of 48 scopes in the file; all 48 matched a vocab entry)
- With a manual chapter: 54
- Panel map done: 1 (Scream 4 Distortion); all others not started

## Guides that matched no Reason device (hardware)

- audiobox-96.md
- launchkey-mk3.md
- samson-servo-300.md
- yamaha-dtx400k.md
- yamaha-emx66m.md

(Classified as hardware from the task statement: launchkey-mk3, yamaha-*, samson-*, audiobox-96. No vocab name or chapter title matches any of them.)

## Remote-vocab manufacturers (device count = vocab ids)

| Manufacturer | Devices |
|---|---|
| Propellerheads | 50 |
| Propellerhead Software | 47 |
| Arturia | 34 |
| Peff | 3 |
| Black and Orange | 3 |
| Blamsoft, Inc. | 3 |
| Deadman Audio Devices | 2 |
| KORG | 2 |
| DLD Technology | 1 |
| LAB ONE Recordings | 1 |
| Cakewalk | 1 |
| Audio Damage, Inc. | 1 |

## Judged name matches (everything not exactly equal after ignoring case/punctuation)

Method labels: "prefix" = one normalised name starts with the other (still a judgment, listed for completeness); "judged" = names differ in wording. All other joins (remotemap scopes, exact guide/chapter names) were exact.

| Kind | Source | Joined to (vocab name) | Method | Reason |
|---|---|---|---|---|
| guide | bv512.md | BV512 Digital Vocoder | prefix (one name starts with the other) | one name is the start of the other |
| guide | cf-101.md | CF-101 Chorus/Flanger | prefix (one name starts with the other) | one name is the start of the other |
| guide | comp-01.md | COMP-01 Compressor/Limiter | prefix (one name starts with the other) | one name is the start of the other |
| guide | d-11.md | D-11 Foldback Distortion | prefix (one name starts with the other) | one name is the start of the other |
| guide | ddl-1.md | DDL-1 Digital Delay Line | prefix (one name starts with the other) | one name is the start of the other |
| guide | dr-octo-rex.md | Dr.REX Loop Player | judged | guide slug "dr-octo-rex" vs vocab "Dr.REX Loop Player"; manual ch.29 is titled "Dr. Octo Rex Loop Player", sharing "Dr." and "Rex" - same device by name similarity |
| guide | ecf-42.md | ECF-42 Envelope Controlled Filter | prefix (one name starts with the other) | one name is the start of the other |
| guide | id8.md | ID8 Instrument Device | prefix (one name starts with the other) | one name is the start of the other |
| guide | kong.md | Kong Drum Designer | prefix (one name starts with the other) | one name is the start of the other |
| guide | malstrom.md | Malstrom Graintable Synthesizer | prefix (one name starts with the other) | one name is the start of the other |
| guide | master-bus-compressor.md | MasterCompressor | judged | guide "Master Bus Compressor" vs vocab "MasterCompressor": different wording, same words Master+Compressor; ch.59 is "Master Bus Compressor" |
| guide | matrix.md | Matrix Pattern Sequencer | prefix (one name starts with the other) | one name is the start of the other |
| guide | neptune.md | Neptune Pitch Adjuster | prefix (one name starts with the other) | one name is the start of the other |
| guide | nn-19.md | NN19 Digital Sampler | prefix (one name starts with the other) | one name is the start of the other |
| guide | nn-xt.md | NN-XT Advanced Sampler | prefix (one name starts with the other) | one name is the start of the other |
| guide | peq-2.md | PEQ-2 Two Band Parametric EQ | prefix (one name starts with the other) | one name is the start of the other |
| guide | ph-90.md | PH-90 Phaser | prefix (one name starts with the other) | one name is the start of the other |
| guide | redrum.md | Redrum Drum Computer | prefix (one name starts with the other) | one name is the start of the other |
| guide | rpg-8.md | RPG-8 Monophonic Arpeggiator | prefix (one name starts with the other) | one name is the start of the other |
| guide | rv-7.md | RV-7 Digital Reverb | prefix (one name starts with the other) | one name is the start of the other |
| guide | rv7000-mkii.md | RV7000 Advanced Reverb | judged | guide "RV7000 Mk II" vs vocab "RV7000 Advanced Reverb": share "RV7000"; ch.53 title is "RV7000 Mk II Advanced Reverb" |
| guide | scream-4.md | Scream 4 Distortion | prefix (one name starts with the other) | one name is the start of the other |
| guide | subtractor.md | SubTractor Analog Synthesizer | prefix (one name starts with the other) | one name is the start of the other |
| guide | thor.md | Thor Polysonic Synthesizer | prefix (one name starts with the other) | vocab has two ids that differ only by case ("THOR..." 207 items, "Thor..." 369 items); attached to the "Thor" one, which is the exact-case name used in our remotemap |
| guide | un-16.md | UN-16 Unison | prefix (one name starts with the other) | one name is the start of the other |
| guide | rytmik.md | Rytmik Drum Machine | prefix (one name starts with the other) | no vocab device; row created from manual chapter title |
| chapter | ch.22 The ReGroove Mixer | ReGroove Mixer | judged | title "The ReGroove Mixer" vs "ReGroove Mixer": leading "The" |
| chapter | ch.29 Dr. Octo Rex Loop Player | Dr.REX Loop Player | judged | title "Dr. Octo Rex Loop Player" vs vocab "Dr.REX Loop Player": same "Dr." / "Rex" / "Loop Player" words |
| chapter | ch.30 Europa Shapeshifting Synthesizer | Europa | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.31 Grain Sample Manipulator | Grain | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.32 Mimic Creative Sampler | Mimic | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.34 Subtractor Synthesizer | SubTractor Analog Synthesizer | judged | title "Subtractor Synthesizer" vs "SubTractor Analog Synthesizer": same word Subtractor + Synthesizer (case differs, "Analog" extra) |
| chapter | ch.35 Malström Synthesizer | Malstrom Graintable Synthesizer | judged | title "Malström Synthesizer" vs "Malstrom Graintable Synthesizer": diacritic differs, "Graintable" extra |
| chapter | ch.36 Monotone Bass Synthesizer | Monotone | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.40 Klang Tuned Percussion | Klang | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.41 Pangea World Instruments | Pangea | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.42 Humana Vocal Ensemble | Humana | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.43 NN-XT Sampler | NN-XT Advanced Sampler | judged | title "NN-XT Sampler" vs "NN-XT Advanced Sampler": "Advanced" extra |
| chapter | ch.44 NN-19 Sampler | NN19 Digital Sampler | judged | title "NN-19 Sampler" vs "NN19 Digital Sampler": hyphen and "Digital" differ |
| chapter | ch.46 Quartet Chorus Ensemble | Quartet | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.47 Sweeper Modulation Effect | Sweeper | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.48 Alligator Triple Filtered Gate | Alligator | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.51 Scream 4 Sound Destruction Unit | Scream 4 Distortion | judged | title "Scream 4 Sound Destruction Unit" vs "Scream 4 Distortion": share "Scream 4" |
| chapter | ch.52 BV512 Vocoder | BV512 Digital Vocoder | judged | title "BV512 Vocoder" vs "BV512 Digital Vocoder": "Digital" extra |
| chapter | ch.53 RV7000 Mk II Advanced Reverb | RV7000 Advanced Reverb | judged | title "RV7000 Mk II Advanced Reverb" vs "RV7000 Advanced Reverb": "Mk II" extra |
| chapter | ch.54 Neptune Pitch Adjuster and Voice Synth | Neptune Pitch Adjuster | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.56 Audiomatic Retro Transformer | Audiomatic | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.57 Channel Dynamics Compressor & Gate | ChannelDynamics | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.58 Channel EQ Equalizer | ChannelEQ | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.59 Master Bus Compressor | MasterCompressor | judged | title "Master Bus Compressor" vs "MasterCompressor": "Bus" extra, spacing differs |
| chapter | ch.60 Synchronous Timed Effect Modulator | Synchronous | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.61 The MClass Effects | MClass Compressor | judged (group chapter) | group chapter "The MClass Effects": every vocab device whose name starts "MClass" |
| chapter | ch.61 The MClass Effects | MClass Equalizer | judged (group chapter) | group chapter "The MClass Effects": every vocab device whose name starts "MClass" |
| chapter | ch.61 The MClass Effects | MClass Maximizer | judged (group chapter) | group chapter "The MClass Effects": every vocab device whose name starts "MClass" |
| chapter | ch.61 The MClass Effects | MClass Stereo Imager | judged (group chapter) | group chapter "The MClass Effects": every vocab device whose name starts "MClass" |
| chapter | ch.62 Half-Rack Effects | CF-101 Chorus/Flanger | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | COMP-01 Compressor/Limiter | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | D-11 Foldback Distortion | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | DDL-1 Digital Delay Line | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | ECF-42 Envelope Controlled Filter | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | PEQ-2 Two Band Parametric EQ | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | PH-90 Phaser | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | RV-7 Digital Reverb | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.62 Half-Rack Effects | UN-16 Unison | judged (group chapter) | group chapter "Half-Rack Effects": WEAKEST JOIN. Title lists no devices; membership chosen as the 9 vocab devices with hyphen-code names and a guide/remotemap scope (CODE-NN pattern). NOT verifiable from the files - verify against chapter text |
| chapter | ch.63 The Combinator | Combinator | judged | one name is the start of the other |
| chapter | ch.64 Pulsar Dual LFO | Pulsar | prefix (one name starts with the other) | one name is the start of the other |
| chapter | ch.65 RPG-8 Arpeggiator | RPG-8 Monophonic Arpeggiator | judged | title "RPG-8 Arpeggiator" vs "RPG-8 Monophonic Arpeggiator": "Monophonic" extra |
| chapter | ch.68 The Line Mixer 6:2 | Line Mixer 6:2 | judged | one name is the start of the other |

## Could not decide

- Guide guitar-amps.md: File name only; no vocab device name or manual title says "guitar amp". Could cover Line 6 Guitar/Bass Amp, ReasonAmp/ReasonBassAmp, or ch.55 Softube Amps - cannot tell from files.
- Manual ch.55 Softube Amps: group chapter whose members cannot be read from the files; kept as its own row (manufacturer unknown) and NOT joined to ReasonAmp / ReasonBassAmp / Line 6 Guitar Amp / Line 6 Bass Amp.
- Manual ch.62 Half-Rack Effects: title lists no devices. Assigned to the 9 hyphen-coded vocab devices (CF-101, COMP-01, D-11, DDL-1, ECF-42, PEQ-2, PH-90, RV-7, UN-16) by name pattern only; membership is a guess until checked against the chapter text.
- Manual ch.45 MIDI Out Device: not joined to any vocab device; a vocab entry "externalmidiinstrument" exists but nothing in the files links them. Chapter row stands alone.
- Manual ch.38 Rytmik Drum Machine: no vocab entry; guide rytmik.md joined to it by name (prefix) only. Manufacturer unknown.
- Duplicate-name vocab ids (kept as separate rows, not merged): se.propellerheads.PX7 / se.propellerheads.px7; se.propellerheads.RadicalKeys / se.propellerheads.radicalkeys; se.propellerheads.Rotor / se.propellerheads.rotor; THOR Polysonic Synthesizer / Thor Polysonic Synthesizer. Guide/chapter attached only to "Thor Polysonic Synthesizer" (exact-case name in our remotemap) and to radicalpiano; the other-case ids have none.
- Names that look like they might be the same product but are different vocab names and were NOT merged: "Dr.REX Loop Player" vs chapter 29 (merged, see judged table); RadicalKeys / radicalkeys / radicalpiano (only radicalpiano joined); Reason Document / Reason Master Section etc. are in our remotemap but have no guide or chapter - whether they are rack devices is not stated in the files.
- Chapters 17 (The Main Mixer) and others were not joined to "Reason Main Mixer Channel"/"Reason Master Section" vocab entries; nothing in the files ties them.
