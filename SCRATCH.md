# SCRATCH — muddy/harsh from-scratch mix fix (2026-09-19, PAUSED, usage low)

Owner: Loops page (`loops_only`) sounds great; from-scratch (one-shots +
synth chords + 808) sounds muddy/harsh. Authorized new research to OVERRULE
old code for this sound design. Chose MEASURE FIRST, then fix.

## Where the two paths live in code
- Good path: Loops page → `loops_only=True` in `beat_machine.py` (~2666,
  2804+), lanes come pre-mixed from `loop_lanes.render_bufs` /
  `loop_mode.py`; `loop_mode.apply_dj_finish` colors a bare loop.
- Bad path: `loops_only=False` → `crew.render_crew_beat` (crew.py:1362)
  builds lanes from one-shots/synth, kick-duck + `peak_ceiling_for`
  scaling, then ONE mix-bus EQ + master tilt. NO per-lane carving.
- Mix-bus EQ (weak): `groove.OWNER_TASTE["mix_eq"]` = low +1.5@120,
  mid -1@800 Q0.9, high +2@8k. Master tilt in `make_drum_loops.master()`
  (air shelf >9k, dip 300-900). `audio_engine.eq3` is the EQ primitive;
  `make_drum_loops.highpass(x,f0)` exists as a filter primitive.

## Diagnosis = no per-element carving before the sum
A pre-mixed loop already has each element HPF'd + slotted. Raw one-shots
each carry full-range energy, so they stack:
- **Mud**: 200-500 Hz low-mid buildup.
- **Harsh**: 2-5 kHz, worst 3-4 kHz (ear's most sensitive band).
- **Boom**: kick + 808 both under ~150 Hz, no separation.

## Research targets (TinyFish agent, sourced)
Per-element frequency slots:
- Kick: 40-60 sub / 60-100 punch / 100-200 body; 2-4k beater. Cut 200Hz-2k ring.
- 808/sub: 30-60 Hz fundamental; keep full, clear lows out of everything else.
- Bass: 80-200 fundamental (cut ~180-200 if boomy); kick owns 60-100, bass 80-200.
- Snare: 200-400 body; 2-4k crack; 5-10k sizzle. Often cut 400-800 hollow.
- Hats/cymbals: HPF hard (~300+); 6k+ air. Nothing useful low.
- Keys/samples: 100-200 boom (cut first in dense mix); 400-600 mud; 1-2k / 3-4k presence.

Target spectral tilt (computable from WAV): fit octave-band energy on
log-freq axis → **-3 to -4.5 dB/oct** (pink ≈ -3; commercial mixes -4 to
-4.5; Voxengo SPAN default 4.5). Lows a few dB above the line = fine;
**8-10 dB above = bass too loud**. No lump in 200-500; no spike in 2-5k.

Fixes:
- Mud: HPF everything but kick/bass/808 at ~80-150 Hz; subtractive first,
  ~3-4 cuts per boost, wide Q 0.7-1.0, cut 200-500 when congested.
- Harsh: 1-3 dB static shelf/cut from ~3 kHz (Q 1.5-2.5), OR dynamic EQ
  (Q 2-4.5, 2-3 dB, attack 2-5 ms) for harshness only on loud hits.
  Don't boost upper-mid/HF on many lanes at once (top cause of fatigue).

Reference-match method: (1) loudness-match (same LUFS) first; (2) capture
avg spectrum of reference A and mix B over a busy section; (3) compare
slopes + band energies, ignore narrow peaks, EQ B toward A. Pink-noise
cross-check: lows a few dB hot ok, 8-10 too much.

Level-balance method (gives dB relationships): solo each element vs pink
noise at -6 dBFS, raise fader till barely audible over noise → matches a
good by-ear mix within a fraction of a dB. EXCEPTION: skip hats/cymbals
(HF sensitivity forces them ~10 dB too loud) — do those by ear.
Practitioner start points (NOT a spec): kick peaks ~-9/-10 dBFS, 808/bass
same or up to ~5 dB hotter.

## NEXT SESSION plan (Mac, in order — do NOT start on low usage)
1. HARD RULE: run full suite ONCE first, render nothing during it:
   `./.venv/bin/python -m pytest tests/ -q`  (~8 min)
2. Render matched A/B into a SCRATCH dir (NEVER the library): same
   DJ+key+tempo, once `loops_only=True`, once `loops_only=False`.
3. Build a small spectral-measure tool (numpy+scipy; reference_track.py
   only does tempo/key). Compute octave-band energies + best-fit slope +
   LUFS-match. Output per-band dB and slope for both files.
4. Report the per-band gap = the correction target (expect from-scratch
   hotter in 200-500 Hz and 2-5 kHz).
5. THEN implement per-lane carving on the `loops_only=False` path in
   `crew.render_crew_beat` (HPF non-bass lanes ~80-150, 200-500 trim on
   midrange lanes, gain-stage), re-render, re-measure, and audition for
   owner's ear (audition-batch). His ear is final judge.

Skills to use next time: audio-fix-verify (measure the finished file, not
the buffer), audition-batch, hard-rule-invariant, beat-output-conventions
(scratch dir + NN naming, never into library while testing).
