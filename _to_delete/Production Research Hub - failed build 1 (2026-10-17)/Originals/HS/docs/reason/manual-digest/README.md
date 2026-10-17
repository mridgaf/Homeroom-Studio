# Reason 12.7 manual digests: index

Plain-language, organized digests of manual chapters your notes did not cover. Built 2026-09-30 from
`~/.reason_voice/reason12_manual/full_chapters/`. Every fact is tagged **Manual** (read in the manual). Nothing was tried in Reason or heard.
Use with the `reason-reference` skill (search rules) and `docs/reason/remote-vocab.json` (parameter spellings, not the manual).

## What is here

| File | Manual chapter | Use it when | Skill status |
|---|---|---|---|
| [players.md](players.md) | 12 Working with Players | chords/arps from single notes, Note Echo, Direct Record | idea only |
| [blocks.md](blocks.md) | 10 Blocks | build and reuse song sections, intros by muting lanes | idea only |
| [audio-editing.md](audio-editing.md) | 8 Audio Editing | fix audio timing, tune vocals, comp takes, drums to MIDI, audio to REX | idea only |
| [sampling.md](sampling.md) | 21 Sampling | resample a device, Edit Sample window, Song Samples | idea only |
| [delay-compensation.md](delay-compensation.md) | 18 Delay Compensation | phasey parallel chains; when to switch it off to record | idea only |
| [key-commands.md](key-commands.md) | 70 Key Commands | any shortcut (Mac left of the slash, Windows right) | reference |
| [routing-and-main-mixer.md](routing-and-main-mixer.md) | 16 Routing, 17 Main Mixer | cables, auto-routing, channel strip, sends, buses, sidechain, de-ess, recipes A-J | idea only (`reason-mixer-chains`) |
| [rack.md](rack.md) | 11 Working with the Rack | creating/moving/duplicating devices, Device Groups, naming, Shift tricks | reference |
| [combinator.md](combinator.md) | 63 Combinator (extras only; basics in `device_refs/combinator.md`) | split/layer zones, macro knobs, CV, panel design | idea only |
| [recording.md](recording.md) | 6 Recording | vocal levels, monitoring, takes, resampling, automation recording | idea only |
| [note-and-automation-editing.md](note-and-automation-editing.md) | 9 Note and Automation Editing | quantize, velocity, Explode, Alter Notes, curves, cleanup | idea only |
| [remote-control.md](remote-control.md) | 23 Remote | map hardware knobs, lock surfaces, Remote Override, keyboard control | reference |
| [sequencer-functions.md](sequencer-functions.md) | 5 Sequencer Functions | track types, lanes, toolbar, snap, locators, loop, tempo | reference |
| [arranging.md](arranging.md) | 7 Arranging | copy a section across tracks, Razor in Ruler, Bounce in Place, insert/remove bars | reference |
| [export-and-performance.md](export-and-performance.md) | 19 Song files, 20 Import/Export, 25 Performance | export a mix, stems, dither, crackle fix order, cheap-CPU habits | reference |
| [patches-and-browser.md](patches-and-browser.md) | 13 Rack Extensions, 14 VST, 15 Patches and Browser | find/load/save patches, Insert FX patches, ReFills, RE and VST handling | reference |
| [drum-devices.md](drum-devices.md) | 27 Kong, 28 Redrum, 29 Dr. Octo Rex (technique only; knobs in `device_refs/`) | Kong output/FX flow, choke and layer groups, Redrum pattern tricks, REX to MIDI | idea only |
| [synth-sound-design.md](synth-sound-design.md) | 30 Europa, 32 Mimic, 33 Thor, 34 Subtractor, 36 Monotone, 43 NN-XT | build bass/pad/pluck/lead, mod routing, slicing | idea only |
| ReGroove | 22 ReGroove Mixer | swing, slide, groove patches | **draft skill**: `.claude/skills/reason-regroove/SKILL.md` |
Earlier summaries: [../manual-bigger-wins-2026-09-30.md](../manual-bigger-wins-2026-09-30.md), [../guide-new-ideas-2026-09-30.md](../guide-new-ideas-2026-09-30.md).

## Manual chapters NOT digested yet
24 Sync and Advanced MIDI, 69 Menu and Dialog Reference (only a few lines read), 1-4 intro/basics, and the device chapters not listed above (35 Malstrom, 37 ID8, 38 Rytmik, 39 Radical Piano, 40 Klang, 41 Pangea, 42 Humana, 44 NN-19, 45-51 and 56-62 effects, 55 Softube Amps, 64-68 utilities). The effects and instruments in that list already have short guides in `device_refs/`; 52 BV512 and 54 Neptune were read for `../techniques/vocals.md`.
Suggested next, by likely value: 24 Sync (if he syncs hardware), 55 Softube Amps, 61 MClass effects, 49 Pulveriser.

## Chain techniques (manual + web) live next door
[../techniques/README.md](../techniques/README.md): vocals, drums, bass/808, instruments and movement, buses/sends/master.

## Known limits
- Key Commands was converted by script and spot-checked; join-wrapped rows should be checked against the manual before relying on them.
- Skill ideas are not yet tested with the skill-creator benchmark loop (your standing rule for new skills).
