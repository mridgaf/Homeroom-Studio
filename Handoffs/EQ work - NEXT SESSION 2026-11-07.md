# EQ work — handoff (2026-11-07)

Next session: finish the EQ suggestions in `Handoffs/EQ plan from the Hub 2026-11-06.md`
EXCEPT the "4 gaps" (hat/clap, pluck/stab/pad, bass-line, chord-vs-melody). Do NOT do the web search.
Read `DECISIONS.md` first (not the ARCHIVE). He commits himself.

## Already done (don't redo)
- Chord gain back to 0.30 (`tools/groove.py` OWNER_TASTE) — his -5 dB cut undone. Melody swap, no-loop list, layered-chord fix all stay.
- Chords: 150 Hz low cut (`base_clean.py`, was already there).
- Melody: 150 Hz low cut added 2026-11-07 (`base_clean.lowcuts`, `role in ("chord","melody")`). Restart Beat Machine (port 8770) to load it.
- Uncommitted: `groove.py`, `base_clean.py`, the plan file. `banned_samples.json` is engine churn, ignore.

## To do (each is one item from the plan; sources are in the plan file)
1. Chords: if boxy, ~3 dB narrow cut found by sweeping 300–500 Hz. Needs a measure on real chord stems before choosing a number.
2. Melody: optional presence ~3–4 kHz wide boost + air at 8 kHz+ (source is vocal advice; for sample melody it's a guess — say so).
3. Bass / 808: confirm mono below ~100–150 Hz. Engine already centres below ~85–170 Hz (`base_clean.mono_below`, `crew.py` ~2584) — likely DONE; verify and close.
4. Bass / 808: "one low sound at a time" — check whether two long 808s can overlap.
5. Kick layer: click 1–4 kHz on top, body under 100 Hz, each filtered to its band. Check what `kick_sub_reinforce` (`groove.py` ~397) already does.
6. Snare reverb: high-pass the reverb 300–500 Hz, on the return. Find the snare-space code first.
7. Any reverb tail: cut under ~200 Hz and over ~8 kHz.
8. Drum bus: gentle low-pass ~8–10 kHz. Compare with the existing master air shelf (+8 kHz) — they pull opposite ways, so ask him.
9. Lo-fi feel: soft roll-off 6–10 kHz. Only on dirt/lo-fi beats; `clean_mix` beats skip dirt.

## Not yet audited (do first)
- The Sound Engine path (`sound_engine/`), drum-lane filters, reverb/snare-space filters. The audit so far covers chords, melody, rumble cut, mono bass, `mix_eq`, `master()`.
- Known failing test, unrelated to this work, fails with or without it: `tests/test_base_clean.py::test_sound_engine_does_not_cut_a_marked_beat_twice` (old beat gets cut 1.31 vs expected < 0.6). Look only if it turns out to be a real sound problem.

## Rules for this work
- ONE lane at a time; measure the finished file (audio-fix-verify skill), then tell him what to listen for. **No renders** unless he asks. No full test suite; focused tests only.
- Changes reach NEW beats only (a beat locks its saved settings).
- Anything that changes how it sounds and isn't a clear match to the plan: ask him, clickable options, recommendation first.
- Items 2 and 8 are taste calls — ask before applying.
