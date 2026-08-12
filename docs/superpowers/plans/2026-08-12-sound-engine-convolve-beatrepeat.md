# Sound Engine — Convolve + Beat Repeat

**Goal:** two new effects on each channel's rack, both live-while-playing and
matched in the export.

**Owner's choices (2026-08-12, asked and answered — do not re-litigate):**
- Convolve IR source: **drop in your own file** (drag a WAV onto the panel).
- Beat Repeat timing: **note values AND free milliseconds, with a switch.**

**Constraints carried over from the mixer plan (still hold):**
- Every parameter must work live in Web Audio; nothing is export-only.
- Exports go to a NEW file in `~/Desktop/Homeroom Sound Engine Exports/`.
- Tests must not depend on `/Volumes/TBOTC 3` being mounted.
- Reuse `.panel`/`.knob`/`.btn` CSS; no new dependencies.
- **The quality loop is mandatory:** build → harsh-critic review → fix →
  a SECOND adversarial re-review by a fresh subagent → confirm. Plus a
  regression test per bug fixed and a full-suite run before "done".

---

## Task A — Convolve (do this first)

Run a stem through any sound the owner drops in: a snare, a door slam, a
vocal. Reuses the reverb machinery — it is convolution already.

**Server (`sound_engine/server.py`)**
- New endpoint `POST /api/project/{pid}/channel/{lane}/ir` (multipart,
  same safe-filename + `dsp.load_audio` + 400-on-unreadable pattern as
  `/api/project/from-upload`, `server.py:151`). Stores `(irL, irR)` on the
  channel dict. `DELETE` on the same path clears it.
- New param `conv_mix` (0.0–1.0, via `_finite_float(..., lo=0, hi=1)`).
- In `_apply_channel_chain`, after Saturation and before Reverb: if
  `conv_mix > 0` and the channel has an IR, wet =
  `groove.loop_convolve(L, irL)` / `(R, irR)` — **already loop-safe**
  (`tools/groove.py:377`), which the house rule requires.
- Guard the two things convolution always breaks:
  1. **IR longer than the stem** — `loop_convolve` requires
     `len(ir) <= len(sig)`; trim the IR.
  2. **Volume explosion** — normalize the wet result to the dry's peak
     before mixing, or a 3-second IR will clip the channel to mud.

**Client (`index.html` + `app.js`)**
- A `.panel` with a drop zone ("drop a sound here"), the loaded IR's name,
  a Mix slider, and a Clear button.
- Live: decode the dropped file with `audioCtx.decodeAudioData`, feed a
  `ConvolverNode` (`normalize = true`), wet/dry gains exactly like the
  existing reverb send (`app.js:267-315`). Same file also POSTs to the new
  IR endpoint so the export matches what was heard.

**Tests (`tests/test_sound_engine.py`)**
- `conv_mix` with no IR loaded is a no-op, not a crash.
- Uploading an IR then processing changes the channel's wet buffer.
- An IR longer than the stem does not raise.
- Output peak stays within ~1 dB of the dry peak (the normalize guard).

## Task B — Beat Repeat (after A is confirmed)

Grab a slice and stutter it.

- Controls: **Grid switch** (note values 1/4, 1/8, 1/16, 1/8T, 1/16T ↔ free
  ms), Slice length, Repeats, Chance/Gate, Pitch-decay toggle, Mix.
- Note values come from the project's BPM — already known per beat
  (`library.py` reads it from the filename); free-ms mode ignores it.
- Live: schedule slice playback with `AudioBufferSourceNode` copies on the
  channel's own buffer, feeding the channel's wet path — do NOT try to do
  this with a delay line, the repeats need independent start offsets.
- Export: numpy slice-and-paste on the channel buffer at the same grid,
  seeded so live and export land on the same slices.
- Tests: slice count and positions match the grid at a known BPM; free-ms
  mode ignores BPM; mix=0 is bit-identical to dry.

## Verification (both tasks)
1. `.venv/bin/python -m pytest tests/` — full suite.
2. Live browser pass on a real multi-stem beat: hear it, then export and
   confirm the file matches what was heard.
3. Quality loop as above, both passes, second one a fresh subagent.
4. Append a `DECISIONS.md` entry.
