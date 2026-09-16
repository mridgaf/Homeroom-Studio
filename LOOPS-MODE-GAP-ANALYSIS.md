# Loops Mode — Gap Analysis & Rule-Engine Map

Companion to `BEAT-GENERATOR-GAP-ANALYSIS.md` and `PACKAGING-GAP-ANALYSIS.md` —
same format, same house rules. Read `CLAUDE.md` and the most recent
`DECISIONS.md` entries before touching anything.

## Part 0 — What this is

A standalone "Loops" page: the same nine-plus DJs (crew + legends), same
personalities, but instead of composing a full arranged beat, each DJ hands
you a usable loop — melodic/chord or drum — that you can audition and export
straight into Reason. **Explicitly not** a mode inside the beat-builder page;
it's its own screen on the same server (owner decision, 2026-09-16 session).

Out of scope for this doc: time-stretching a drum loop to a target tempo,
any UI polish beyond "cards you can click and download," and touching
anything in `remote/` or the Reason Voice half.

## Part 1 — What already exists (more than expected)

Two loop pools already exist as data. Neither is exposed anywhere as "give
me a loop."

1. **`tools/melodic_loops.py`** — scans `BOTC Sorted Loops` via its own
   `loop_roots`/`loop_sorted_root` config keys (fixed 2026-09-14, same shape
   as the instrument and MIDI root fixes). `scan()` tags every file's role
   (chord/melody/bass/drum/vocal), key, mode, bpm. `in_key(index, key,
   role=None, bpm=None)` matches on **mode family**, not exact mode (fixed
   2026-07-24 — same bug class the MIDI packs hit again on 2026-09-15/16).
   `fit_loop(x, sr, dst_secs, src_key, dst_key)` pitch-shifts a loop into a
   target key by resampling — **it cannot correct tempo**, only pitch.
   `chop_onsets(x, sr, min_dur, max_dur)` slices a loop into its individual
   note/chord hits, built so `chord_synth.loop_voice` can drop pieces of a
   loop into individual chord slots.

2. **`tools/sample_library.py`'s `scan_packs()`** (lines ~395-424) — any
   audio file in a folder or with a filename matching `_LOOP_NAME_RE` gets
   tagged `kind="loop"` into a **`"_loops"` bucket**, with `role`, a
   filename-parsed `bpm`, and a `tonal` flag, specifically so it's kept OUT
   of the one-shot drum-hit pools ("a loop must never be choked into a drum
   hit"). Grepped the whole `tools/` tree: **nothing reads `shots["_loops"]`
   anywhere except the scanner that writes it.** This is a fully-populated,
   fully-dormant drum-loop library.

3. **Per-DJ identity is much bigger than composition rules.** Each entry in
   `crew_config.json` / `legends_config.json` carries, independent of any
   arrangement logic: a `library` taste (`{"p": 0.5, "tags": [["lofi",3],
   ["boom-bap",2], ...]}` — see Otto Grit), a `signature` (chord_source
   weights, key mode/root weights, progression weights), and a full
   mix/processing fingerprint (`mix_eq`, `drive`, `dust`, `vinyl`, `wow`,
   `sidechain`, `chorus`, `kick_flavors`) plus a freeform `listen`
   description. A DJ's "sound" lives in all of this, not just in which
   files they're allowed to touch.

4. **The exact "mostly personality, not a hard wall" mechanic already
   exists and already ships.** `tools/pattern_gen.py` (~line 1137): when
   building a beat's rhythm seed, `if lib and rng.random() < lib.get("p",
   0): lib_seed = _pick_library(lib, rng)` — a per-beat weighted roll into
   the DJ's own tagged reference-groove pool; **on a miss, nothing narrows
   the pool at all.** This is precisely the "50%+ personality, otherwise
   wide open" shape you asked for on the loops page — it's proven,
   shipping code, not a new idea.

5. **The server plumbing a loop page needs already exists.** `tools/
   beat_machine.py` runs a hand-rolled `BaseHTTPRequestHandler` on port
   8770 (not FastAPI/Flask — see `run_web()`). It already has WAV
   encode/stream helpers (`_wav`, `_media`, `wav24_bytes`/`write_wav24`
   from `make_drum_loops.py`), a JSON-candidates-list endpoint shape
   (`/candidates`), and the file-naming convention: `f"{no} {title} Drums
   {preset['bpm']}bpm.wav"` (line 3046 and two other call sites) paired
   with a `.recipes/NN.json` sidecar.

## Part 2 — The gaps (precise, code-grounded)

1. Neither loop pool is reachable on its own. Melodic loops only surface
   pre-chopped, inside `chord_synth.loop_voice`, as one ingredient of a
   full chord slot — never as "here's the loop itself." Drum loops surface
   nowhere at all.
2. Every filter on both pools today is a **hard gate**: `melodic_loops.
   in_key()` / `chord_synth.sample_pool()` *exclude* anything outside the
   target key family. Nothing in either module scores-but-keeps.
3. No code applies a DJ's mix fingerprint (EQ/drive/dust/vinyl/sidechain)
   to a bare loop outside of full-beat rendering. `_solo_audio`/
   `_preview_render` color drum-kit lanes inside a beat, not a standalone
   file.
4. No naming/export convention exists for a loop deliverable — only the
   `"... Drums NNNbpm.wav"` shape for a fully arranged beat.
5. No page/route serves any of this. `beat_machine.py`'s `do_GET` has no
   `/loops` case.

## Part 3 — The seam (why this is closer than it looks)

Every piece this needs already exists in isolated, working form: two raw
loop pools, a proven "weighted-roll-then-wide-open" selection mechanic, a
render/encode/naming pipeline, and a per-DJ processing fingerprint. This is
wiring plus one new hard-gate-to-soft-score conversion, not a new engine.
Shape of the new code:

```
pick_loop(dj_signature, pool, rng) -> entry
    # rng.random() < dj_signature.get("loop_taste", {}).get("p", 0.5):
    #   -> weighted pick by the DJ's own tag/key/genre affinity
    #      (mirrors _pick_library, doesn't reuse it verbatim — different
    #      pool shape)
    # else:
    #   -> rng.choice(pool)  — the ENTIRE pool, zero filtering
```

Run every pick through that DJ's existing mix-processing chain before
export, so a freely-chosen raw file still comes back sounding like that DJ
touched it — personality lives in the color, not just the selection.

## Part 4 — Punch list for Claude Code

0. **Boundary test first.** Assert the new loop-mode code path never calls
   `_pin_bars_for_loop_voice`, never checks `PREFER_MAX_SHIFT`, and never
   imports anything from the chord/arrangement slot-fitting path. Loop mode
   must be provably decoupled from beat-arrangement rules — those rules
   stay exactly as they are for `compose()`. See Part 4a.
1. Add **scored, non-excluding** lookups: `melodic_loops.in_key_scored()`
   and a sample_library equivalent for the `"_loops"` bucket. Same key/
   mode-family/bpm logic as today's `in_key()`, but return every entry with
   a `fit_score` instead of dropping non-matches. Leave the existing
   `in_key()` untouched — full-beat generation keeps its hard filter
   unchanged.
2. Add `pick_loop()` per Part 3. Default `p = 0.5` for every DJ unless a
   persona later gets its own `loop_taste.p` — this is what makes "at least
   50%+ personality, never limited" literal.
3. Wire the **drum-loop** path: `sample_library.scan_packs()["_loops"]` ->
   `pick_loop()` -> that DJ's existing mix-fingerprint processing (reuse
   the beat renderer's own per-DJ chain function — do not write a second
   one) -> WAV out.
4. Wire the **melodic-loop** path the same way, sourced from
   `melodic_loops.scan()`. Offer the loop both whole and
   `chop_onsets()`-chopped (open question — Part 6).
5. New route on the *existing* `beat_machine.py` server — same port 8770,
   same Handler class, same `_send`/`_json`/`_media` helpers. Suggested
   shape: `GET /loops` (the page), `GET /loops/batch?dj=<name>&kind=
   melodic|drum` (JSON list), `GET /loops/audio?...` (the file).
6. Naming/export — see Part 5, confirm with owner before finalizing.
7. **Proof step, not a claim:** render one drum loop and one melodic loop
   from two different DJs, plus a few picks with `p` forced to 0 (fully
   free) and 1 (fully on-taste), so the "personality still shows through"
   claim is something the owner can hear, not just something the diff
   asserts.

## Part 4a — The "no rules hinder" boundary (owner decision, 2026-09-16)

Scoped explicitly, not a repeal:

- The owner hard rule **"NO DRUM-LOOP LANE... exclude drum loops"**
  (2026-07-23, `beat_machine.py` ~line 1438) stays fully intact for
  `compose()` / full-beat generation. Nothing in this feature touches that
  code path.
- The **one-instrument-per-chord** rule (`PREFER_MAX_SHIFT=12`,
  `instrument_sampler.py`) and the **"4-bar beats if a loop is used"** pin
  (`_pin_bars_for_loop_voice`) are both about fitting a loop into an
  arrangement slot. Loop mode has no arrangement slot, so these rules don't
  apply here — not because they're weakened, but because the situation
  they govern doesn't exist on this page.
- Within the Loops page specifically, the owner has said explicitly: no DJ
  signature field (chord_source, key/mode weighting, genre tags) should
  ever *exclude* a sound — only weight toward it, at least half the time.
  This is a new, narrow, named exception for one feature. It is not license
  to loosen any hard rule anywhere else in the codebase. If a future
  session is tempted to reuse this reasoning elsewhere, it should come back
  to the owner first, same as any other hard-rule change.

## Part 5 — Naming/output convention (flag for owner — NOT decided)

Proposed, matching the existing beat convention as closely as makes sense
for a raw loop rather than a rendered beat:

- Filename: `"{no} {dj} {title} Loop {bpm}bpm.wav"` — bpm here is the
  loop's own native tempo (see Part 6), not a target.
- Output location: split `Loops - Melodic` / `Loops - Drum` folders, or one
  `Loops` folder with the kind in the filename? Leaning toward split, since
  the two pools have very different use cases in Reason.
- Does a loop get a `.recipes/NN.json` sidecar like a beat does, or is that
  overkill for something that isn't a composed arrangement? Leaning toward
  a much smaller sidecar (just: DJ, source file, key/bpm, whether it was
  a taste-pick or a free-pick) rather than reusing the beat recipe shape.
- Shares the beat library's `NN` counter, or gets its own? Leaning toward
  its own counter so loop numbering doesn't eat into beat numbering.

## Part 6 — Honest unknowns

- **Nothing in this document has been run.** This planning session's
  sandbox is Linux; the project's venv is macOS-only. Every claim above is
  from reading the source, not from executing it. Claude Code, working on
  the real Mac, should verify each numbered gap against the actual code
  before building on it.
- The `"_loops"` bucket's `tonal` flag (`sample_library.py`) has never been
  read by any other code. Whether it's even populated correctly is
  untested — worth a quick print-debug scan before trusting it to separate
  genuinely rhythmic drum loops from tonal material that happens to live
  in a LOOP-named folder.
- Drum loops surface at their own recorded tempo; nothing here stretches
  them to a target BPM. That's real, separate work if it's ever wanted —
  not scoped into this build.
- Whether a melodic loop should default to whole or chopped is unresolved
  (Part 4, step 4) — chopping exists today only to fit a chord slot, which
  doesn't exist on this page, so "whole" may simply be the right default
  and chopped an optional toggle.
- The five-persona-style precedent this document leans on
  (`_pick_library`, the `library.p` roll) was designed for a *rhythm
  groove* pool, not a loop pool. The shapes are close but not identical —
  Code should treat `pick_loop()` as new code inspired by that pattern, not
  a refactor of it.
