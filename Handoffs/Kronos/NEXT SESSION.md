# Kronos - next session

Owner (2026-10-26): new session. Show him "crazy cool drum beats" made with the Kronos. Start by searching basic-memory for "Kronos 61 - start here".

## Done 2026-10-26: chaptered "super homework" memory
- basic-memory notes `gear/kronos/homework/` chapters 00-07 (drum kits, Drum Track, KARMA, effects, sequencer/RPPR/wave sequences, engines, tested facts + open questions) and `gear/homeroom/Homeroom Studio and Reason - map`. Read chapter 00 first.
- Parameter Guide saved: `Production Research Hub/Originals/Kronos/KRONOS_Param_Guide_E3.pdf` (extracted text lives in the old session scratchpad only; re-extract with pypdf in a temp venv if needed).
- First tasks next: read Global object (obj 0x03) to see Enable Exclusive / Memory Protect; copy kit 4 to a free USER kit slot; verify kit 4 and INT-F 095 are untouched; then retry kick saturation inside the Kronos.

## Rules for this session
- Use the Kronos's OWN engine for sounds and effects. No Mac-side plugins unless he says so.
- Work only in bank USER-G (SysEx bank 0x46, Bank Select LSB 14). Never edit factory sounds. Slots 0-63 drums, 64-127 keys.
- Kronos scripts: sandbox OFF from the first call; anything over ~30 s runs in the background with a log.
- Replies: ONE short paragraph, `YOUR ACTION` last. Questions as clickable options.
- Do not record/render audio files unless he asks. Playing live to the Kronos is fine.

## What works (heard by him)
- Switching sounds (INT banks), chords, GM Power Kit beat, and `USER-G 000 Claude Hip Hop Kit` beat ("drums sound right").
- `tools/kronos.py`: `beat(kit=HH_KIT)` 8-bar 90 BPM live; `find`, `play`, `chord`, `cc`.
- Reading the Kronos back by SysEx (names, current sound, whole programs). Store a bank with func 0x76.

## What does not work yet
- Effect-type change via SysEx (ignored). Kit Drive via func 0x53 (no measurable change). Kick saturation inside the Kronos is still open.
- IFX1 Send2 (func 0x43 TYP7 SOC0 SUB0 PID8) DOES work for snare reverb; it defaults to 127.
- Ideas to try: edit the copy's program bytes offline then re-dump to USER-G (object dump route); use Kronos KARMA / Drum Track (CC and SysEx 0x6D/0x6E); layer kits; velocity and swing programming; use several kits at once on different MIDI channels.

## Pending small things (classifier errored last turn)
1. Set Hermes `reasoning_effort: high` in `~/.hermes/config.yaml` line 38 (backup first). He approved this.
2. Write `tools/kronos_play_claude_beat.py` (select USER-G 000, play `kronos.beat(kit=kronos.HH_KIT)`), then have Hermes run it: warm-up message, then `--continue`.
3. Hermes tested: with the tool named (`search_notes`, `read_note`) at high effort it recalled exact bank numbers correctly; plain requests failed at medium.

## Where things are
- Notes: basic-memory `gear/kronos/*`. Code: `tools/kronos*.py`. Manuals: `Production Research Hub/Originals/Kronos/`.
- Ledger: DECISIONS.md entries 2026-10-25.
