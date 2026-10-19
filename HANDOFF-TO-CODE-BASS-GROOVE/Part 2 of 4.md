# Handoff to Code: Bass groove
## Part 2 of 4: VERIFIED facts (read in the code 2026-10-19)
**Previous:** Part 1  **Next:** Part 3 of 4.md (design spec + UNVERIFIED)

All line numbers are `tools/beat_machine.py` as of 2026-10-19; re-check them, the file is 8,890 lines and changes often.

## The bass today
- `add_bass_and_chords()` ~line 1538 sets `preset.setdefault("chord_flow", harmony.FLOW_VERSION)` and calls `_build_chords(..., allow_basses=False, bass_line=(low != "808"))`.
- `_build_chords()` ~line 2210. `slots` is built ~line 2465: a list of `(i, chord, start_bar, dur_seconds)`. `chord["notes"][0]` is the root and `chord.get("voiced")` holds the voiced notes. `bar_s`, `nb` (bars), `num` (beats per bar) and `key = KeyContext(...)` are in scope.
- Bass block ~lines 2950-3025: the bass index is `instrument_sampler.scan_bass()` minus files with "808" in the name, reduced to ONE file `pick` (seed `variant*29+3`, or `bass_pick`). `bass_oct` shifts the line by whole octaves to meet that file. Per slot: `instrument_sampler.voice_note(bass_idx, chord["notes"][0] - 12 + bass_oct, dur, cache=bcache, used=bused, snap_sec=bar_s/num)` gives ONE held note for the whole slot. If any slot returns None, the whole line is dropped (no synth fallback, house rule).
- Lane row ~line 3060: `preset["lanes"][f"bass{i}"] = (0.0, gain, (0, 0, 50, variant + i), bars_list)` where `bars_list[start_bar] = "X" + "-"*15`. Feel is `(0,0,50)`: no swing at all.
- `midi_chords` entry ~line 3110: `notes = voiced + [bass_note]`, so the bass is exported as one held note inside the chords track.
- Rebuild ~line 4407 calls `_build_chords` with the saved preset, `bass_pick=_bp`, and `bass808` for the old 808 beats.
- Also calling `_build_chords` directly: `make_chord_ab.py`, `make_chord_flow_ab.py`, `make_chord_patterns_ab.py`, `make_root_808_ab.py`, `make_strings_ab.py`. `make_legend_newbuild.py` calls `add_bass_and_chords`.
- The kick lane is already in `preset["lanes"]["kick"]` when `_build_chords` runs, as `(pan, gain, (off, jit, swing, seed), bars)` with one 16-char string per bar. The 808 branch reads it.

## Reusable pieces (all real, read in code)
- `chord_rhythm.render_figure()` and `gen_figure()`: the model to copy. They use `groove.LaneFeel(off_ms, jit_ms, swing, seed).hit_time(bar_start_s, step16, bpm)`, `groove.velocity(char, step, None)`, `chord_synth.add_wrapped(out, seg, start)` (loop-safe wrap) and `chord_synth.finish_riff(out, sr)`.
- `pattern_gen.BEATS = (0, 4, 8, 12)` and `pattern_gen._weighted(rng, [[name, w], ...])`.
- `KeyContext.scale()` gives the key's pitch classes, tonic first; `.degree(pc)` gives the degree or None.
- `instrument_sampler.MAX_SHIFT = 4`, `PREFER_MAX_SHIFT = 12`. With a one-file index, `nearest()` returns the least-bad pick, NOT None, so a note far from the file's recorded pitch gets stretched (chipmunk risk).
- Every identity has `signature.chord_family`, one of: `soul_jazz`, `dark`, `grit`, `dreamy`, `bright_funk`.
  - Crew 11: soul_jazz 3, grit 2, dreamy 3, dark 2, bright_funk 1.
  - Legends 16: dreamy 4, soul_jazz 5, dark 4, grit 3.
  - Genres 18: dark 6, soul_jazz 3, grit 1, dreamy 3, bright_funk 5.
- `beat_recipes.write_midi(path, events, bpm, tpq=480, tsig, chords=None)` writes the chords as one track on channel 1 (0x90/0x80, velocity 90).

## Environment facts
- Cowork's Linux VM on his Mac had numpy 2.2.6 and Python 3.10. I pip-installed scipy, soundfile and pytest there, which says nothing about his `.venv`. Use `./.venv/bin/python -m pytest` on the Mac.
- His samples are on `/Volumes/TBOTC 3` (not visible from Cowork). Renders need the drive mounted.

## Already delivered today (context, not to redo)
- `Production Research Hub/Chapters/13 College theory for MIDI patterns/` (4 parts): sourced theory, voice-leading rules, drum grids, emotion map.
- `tools/theory_loops.py`, plus 8 test MIDI loops in `Production Research Hub/Theory loops 2026-10-19/` and copied to `~/Desktop/Homeroom Auditions/Theory loops 2026-10-19/`. These are grid-straight, fixed-velocity rule demos, NOT the engine. The owner hasn't heard them yet.

=== END OF PART ===
