# Panel Map inventory (Phase 2, 2026-10-03)

Source of truth for what is INSTALLED: Reason 12.7's own Create menus, read 2026-10-03 (installed.csv).
inventory.csv = every device Reason has a Remote map for (148), most of which he does NOT own. Use it only to look up names.

## What he has
| Kind | Count | Notes |
|---|---|---|
| Reason-made (stock) | 63 | 19 instruments, 29 effects, 10 utilities, 5 players |
| Rack Extensions from other makers | 15 | 8 utilities, 7 effects (AirRaid, Groovy Melon, pongasoft, Red Rock Sound, Rob Papen, Robotic Bean, kiloHearts, Kuassa, Softube, ThatMusicCompany) |
| VST plugins | 15 | 5 instruments, 10 effects. Their controls live in a separate plugin window, not on a rack panel. Not part of the rack map unless John says so. |
| Always in every song | — | Hardware Interface, Master Section, Main Mixer. Not in the Create menus; map them too. |

## Name joins (menu name -> Reason's Remote name)
- Exact or near-exact for most. Hand joins (wording differs): RV7000 MkII Reverb -> RV7000 Advanced Reverb, Dr. Octo Rex -> Dr.REX Loop Player, Channel Dynamics/EQ -> ChannelDynamics/ChannelEQ, Master Bus Compressor -> MasterCompressor, Alligator Filter Gate -> Alligator, Pulveriser Demolition -> Pulveriser.
- PROBABLE, confirm in Reason while mapping: Scales & Chords -> ScalesAndChords, Dual Arpeggio -> Arpeggio, Softube Amp -> ReasonAmp, Softube Bass Amp -> ReasonBassAmp, Mix Channel -> Reason Main Mixer Channel.
- No Remote map found: Audio Track, Drum Sequencer, all 15 third-party Rack Extensions (no Remote map for them in Reason's files, so tooltips are the only name source).

## Settled from the manual
- Ch.62 Half-Rack Effects covers all 9: CF-101, COMP-01, D-11, DDL-1, ECF-42, PEQ-2, PH-90, RV-7, UN-16 (each named as a heading in the chapter text).
- Ch.55 covers Softube Amp + Softube Bass Amp (chapter text).
- device_refs/guitar-amps.md is about his physical amps (hardware), like audiobox-96, launchkey-mk3, samson-servo-300, yamaha-*.

## Proposed batch order (counts)
- A. Simple fixed effects (18): Half-rack 9, MClass 4, The Echo, RV7000, Channel EQ, Channel Dynamics, Master Bus Compressor.
- B. Other stock effects (10): Alligator, Audiomatic, BV512, Neptune, Pulveriser, Quartet, Softube Amp, Softube Bass Amp, Sweeper, Synchronous.
- C. Mixing & utilities (13): Mix Channel, Audio Track, Mixer 14:2, Line Mixer 6:2, Spider Audio, Spider CV, Matrix, Pulsar, RPG-8, Combinator (outer panel), Hardware Interface, Master Section, Main Mixer.
- D. Instruments (19) — several with views (Kong pads, Thor, Europa, Mimic, Grain, Redrum).
- E. Players (5).
- F. Third-party Rack Extensions (15).
