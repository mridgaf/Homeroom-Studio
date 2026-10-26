# Kronos - next session

Owner (2026-10-26): show him "crazy cool drum beats" made with the Kronos, using the Kronos's own engine. Start by searching basic-memory for "Kronos Homework 00 - map of chapters" and "Kronos 61 - start here".

## Rules
- Kronos's OWN sounds and effects. No Mac plugins unless he asks.
- Write only to bank USER-G (SysEx bank 0x46, Bank Select LSB 14) and USER-G drum kit 00 (kit 136). Never edit factory sounds or kits.
- Kronos scripts: sandbox OFF from the first call, anything over ~30 s in the background with a log, and close MIDI ports at the end of every script (two finished scripts hung for hours without this).
- Replies: ONE short paragraph, `YOUR ACTION` last. Clickable options for every question. No audio renders unless he asks.

## State (verified)
- `tools/kronos.py` (find, play, chord, cc, beat), `kronos_names.py`, `kronos_bank.py`, `kronos_global.py`, `kronos_probe.py`, `kronos_kit_test.py`, `kronos_find_kitbyte.py`, `kronos_repoint.py`.
- USER-G 000 "Claude Hip Hop Kit" plays USER-G kit 00 (kit 136, a copy of kit 4). USER-G 064 "Claude Piano". USER-G 127 scratch. He heard the drums: right.
- Kit edits over SysEx work (func 0x71 kit 136 = idH 1, idL 8, then 0x53). Factory kit 4 verified untouched.

## Not solved
- Kick saturation inside the Kronos. Facts: effect-type change by func 0x43 is rejected (reply code 2); kit Drive alone is inaudible (it offsets the Program driver); IFX Send2 (func 0x43 TYP7 SOC n-1 PID8) is accepted.
- Next to try: dump a program, edit the kick-IFX effect type bytes offline (Prog_HD-1.txt / Effect.txt layouts, unit object version 4 is 256 bytes shorter than the doc's v5, so locate offsets by diffing real programs like kronos_find_kitbyte.py does), write it to a USER-G slot with func 0x73, store with 0x76, then verify by recording hits (peak and high-frequency share).

## Also pending
1. Hermes: set `reasoning_effort: high` in `~/.hermes/config.yaml` line 38 (he approved; backup first). Then have Hermes run a real Kronos command. Hermes passes memory recall when the tool is named (`search_notes`, `read_note`).
2. Parameter Guide text must be re-extracted if needed (pypdf in a temp venv; the old scratch copy is gone with the session).
