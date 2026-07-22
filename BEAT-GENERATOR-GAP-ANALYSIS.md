# Beat Generator — Gap Analysis & Rule-Engine Map

*What already exists in this project, what the Wedge-1 product still needs, and a
concrete punch list. Grounded in the actual code as of 2026-07-19.*

**The one-line finding:** this is not an idea to build — it's a working generative
beat engine that's missing two specific pieces. The market/spec work treated it as
greenfield; it isn't. The real job is closing two gaps, not starting over.

**Wedge 1 (the product goal):** an app you point at your own sample bank that
generates a full, *in-key* musical idea — drums **plus bass plus chords** — from
sounds you own. The differentiator vs. Atlas/XO/Playbeat is harmonic intelligence:
they're drums-only; this understands key.

---

## Part 1 — What already exists (and it's a lot)

| Capability | Where it lives | What it does | Reuse for Wedge 1 |
|---|---|---|---|
| Generative rhythm engine | `tools/pattern_gen.py` (`compose()`) | Writes a fresh drum pattern per generation from each DJ's grammar (per-step kick weights, snare/clap/hat modes, ghost notes, kick flavors) | **Core engine — keep.** This is the rhythm brain. |
| 9 producer "DJs" | `crew_config.json` | Each a full style grammar with identity constraints | Keep as the style layer. |
| 18+ genre configs | `genres_config.json` | Memphis, Crunk, G-Funk, Trip-Hop, Bounce, etc. as data | Keep — genre rule-sets. |
| Automated tuning loop | `autoresearch.*`, `tools/variety.py`, `tools/evolution.py` | Measures beat *variety* vs. a metric + noise floor; proposes changes; owner approves by ear; per-DJ rollback | Keep — this is your QA/R&D system. Rare and valuable. |
| Sample ingestion | `tools/sample_library.py` | Scans pack roots from `sample_packs.json`, reads folder structure, buckets one-shots into drum roles, caches to `~/.reason_voice/pack_index.json` | **Partial — see Gap 1.** The "point at your samples" door exists but only for drums. |
| Drum MIDI library | `pattern_library/` | 131 patterns + `catalog.json` indexed by genre/bpm/feel | Keep — seed grooves. |
| Music-theory knowledge base | `theory/*.md` | Chords, intervals, modes, progressions, keys, tension/release — plain-English, rap-tuned | **The harmony brain — but as prose, see Gap 2.** |
| Mood → build recipes | `recipes/feelings/*.md` | Each maps a feeling → key, progression, bassline, production, with theory citations | **The bridge** from theory to generation rules. |
| Tuned 808 root | `tools/beat_machine.py` (`sub808`, `ROOT_HZ`) | Synthesizes a tuned sub on a musical root under the kick; follows the "808 root rule" | **The seam — see Part 3.** The engine already has a notion of key. |

---

## Part 2 — The two gaps (precise, code-grounded)

### Gap 1 — Sample ingestion exists, but it's drums-only *by design*
`sample_library.py` blocks melodic content with one list — `EXCLUDE_DIR_WORDS`
(`BASS, MELOD, CHORD, SYNTH, KEY, PIANO, GUITAR, VOCAL, LOOP, MIDI, ...`) — and
one function, `_excluded()`, which rejects any file whose ancestor folder matches.
Bass/Melodic/Keys/Chords aren't missed by accident; they're deliberately dropped.

That means the engine today has *the exact blind spot Atlas has* — it ignores the
melodic and harmonic samples in a user's library. To deliver Wedge 1, ingestion
needs a **second path**: remove the melodic words from `EXCLUDE_DIR_WORDS`, add
matching `DIR_ROLES` (`bass`, `chord`, `keys`, `melodic`), and attach a detected
key to each.

**Critical correction from the actual library scan (see Part 7).** The owner's
melodic material is **~485 files but 466 are loops, only 19 one-shots.** So the
harmony path CANNOT mirror the drum "one-shots only" rule — that would capture 19
files, essentially nothing. It must ingest **melodic loops** and detect each
loop's **key AND tempo**, then time-stretch to the beat's tempo and pitch-shift to
its key. This is heavier than stacking one-shot chords, but it's the only way to
use the library that actually exists. It also sharpens the wedge: Atlas ignores
loops too, so "handles your melodic loops, in key and in tempo" is a cleaner gap
than one-shots-only would have been.

**The low-risk shortcut: MIDI first.** The library also contains MIDI packs
(`Cymatics - Python Free MIDI Pack`, plus `Essential Chord MIDI` / `Melody MIDI`
inside the Cobra pack). MIDI is already notes — exact chords and keys with **zero
pitch-detection risk**. Wire MIDI ingestion *before* audio pitch detection: read
the file, you know the chord, done. It's the safest possible seed material for the
harmony generator and de-risks the whole gap.

### Gap 2 — Harmony is not generated
`pattern_gen.compose()` produces drums. `beat_machine.py` adds a **monophonic**
tuned 808 on a root note. There is **no chord or progression generation** in the
code — no stacking of voicings, no key-aware selection of melodic samples.

The harmony *knowledge* is fully written down — `theory/progressions.md` (chord
loops by feeling, spelled in A-minor white keys), `theory/chords.md` (voicing
formulas as intervals from the root), `theory/song-keys.md` (key selection + the
808 root rule), and the `recipes/feelings/*` recipes that already combine key +
progression + bassline per mood. **None of it is code yet.** The build turns this
prose into a harmony generator.

---

## Part 3 — The seam (why this is closer than it looks)

The engine already tunes an 808 to a **musical root** (`ROOT_HZ` in
`beat_machine.py`). That means "what key is this beat in" is *already a value the
system tracks* — it just currently uses it for one sine-sub note.

That root is the hook to hang harmony on. The build path is: promote that single
root into a **key context** (root + mode), then have a new harmony module read
`theory/progressions.md` to lay chords over it and select/pitch-shift the user's
melodic samples to fit. You're extending an existing concept, not inventing one.

---

## Part 4 — Punch list for Claude Code

Ordered smallest-risk first. Each is a discrete, testable unit.

**Status (2026-07-22): 1, 2, 3, 4, and 7 are done and tested. 5 and 6 are
now done too, via a different route than planned — see below (444 tests
green).**

1. ~~**Key context object.**~~ DONE — `tools/key_context.py` +
   `tests/test_key_context.py`.
2. ~~**Progression generator.**~~ DONE — `progressions_config.json` +
   `tools/harmony.py` (`compose()`) + `tests/test_harmony.py`.
3. ~~**Chord voicing.**~~ DONE — folded into step 1;
   `KeyContext.voice()`/`triad()`/`roman()` in `tools/key_context.py`.
4. ~~**MIDI ingestion FIRST (low risk).**~~ DONE — `tools/midi_packs.py` +
   `tests/test_midi_packs.py`.
5. ~~**Melodic-LOOP ingestion (the real library).**~~ DONE —
   `tools/melodic_loops.py` + `tests/test_melodic_loops.py`. Turns out
   Essentia/madmom weren't needed: Cymatics one-shots ("... - C.wav"),
   Function Loops loops ("..._140_..._Gm.wav"), and Live loop cds
   ("075_MoveOn_Bm/...") all put the key (and usually the bpm) in the
   file/folder name already — the vendor did the detection. Same MIDI-
   first logic (read the label, don't guess) applied to audio. 2,013
   key-labeled melodic files found once `sample_packs.json` grew two
   more roots (Function Loops sampler, Live loop cds); 1,442 of those
   carry a bpm tag too. Files with no parseable key are simply left out
   of the index — that's the one-shot/loop-vs-drum filter, no separate
   exclude-word list needed. Unlabeled loops (if any pack turns out to
   have them) still fall back to the original Essentia/madmom plan.
6. ~~**In-key/in-tempo sample fitting.**~~ DONE for the common case —
   `melodic_loops.fit_loop()`. Pitch-corrects by resample (the same
   `np.interp` trick `load_audio` already uses for sample-rate
   conversion, generalized to an arbitrary ratio), then crops/tiles to
   the target length the same loop-safe way every other lane in this
   project already fits a bar — no edge fades. **Ceiling:** one resample
   ratio can't correct pitch and tempo independently, so duration drifts
   by the pitch-shift ratio instead of landing exactly on the target
   tempo; `in_key()`'s bpm-closeness ranking keeps that drift small by
   picking a source loop already near the beat's tempo. A real
   independent time-stretch (librosa/rubberband) is still the upgrade
   path if that drift is ever audible on a real beat — that's the actual
   remaining use for a new dependency, not key detection.
7. ~~**Wire into the render.**~~ DONE, but via **synthesis, not sampled
   instruments.** `tools/chord_synth.py` (`pad_voice`/`bass_voice`) turns
   `harmony.compose()`'s exact MIDI notes into audio, wired into
   `beat_machine.py` behind an opt-in notes-box direction ("chords", or
   a mood word — "dreamy", "sad", "epic", ...). Real per-lane stems, a
   proper polyphonic MIDI chords track (channel 1, not the drum
   channel), and it takes over the bass-under-the-kick job so it never
   clashes with the plain tuned-808 sub. The Symphonic Strings library
   (24.5k pitched one-shots, real MIDI-note-in-filename — see Part 7)
   is the natural next seam for real instrument audio instead of a
   synth pad, and needs no audio-key-detection at all, unlike 5-6.
8. **MVP cut:** shipped, in synth form — drums + bass + chords, MIDI
   export, key picked automatically (no manual override built — every
   beat with "chords" gets a fresh random key/progression unless a mood
   word is given). `melodic_loops.py` (steps 5-6) is built and tested
   but NOT wired into `chord_synth`'s render path yet — that's the real
   remaining fast-follow: swap `pad_voice`/`bass_voice` for a picked,
   fitted sample when one's available in the beat's key. The Symphonic
   Strings shortcut above is a separate, still-untouched pool (pitched
   one-shots by note name, not loops — a different ingestion shape).

**Constraints (from `CLAUDE.md`, keep true):** target Python 3.9 (`from __future__
import annotations` for `X | Y`); quote the `Homeroom Studio` path (space);
bash not zsh; `sed -i ''`; don't touch the `remote/` Reason bridge; keep tests
green (`tests/`).

---

## Part 5 — The "legends" question — SETTLED 2026-07-22
Owner decision: keep the real-producer names, internal-only. No rename, no
drop. They may surface in the local batch-player UI (owner's own reference,
`beat_machine._dj_card`'s "like Pharrell" label) but must never reach an
exported file name, stem, or title — those already read from the sound-alike
codename (`preset["title"]`), never from `preset["built"]`, and `_dj_card`
now carries a comment saying so. Documented in `legends_config.json`'s
`_readme`. Re-open this before anything here ships publicly.

---

## Part 6 — Honest unknowns
- **"In key" ≠ "sounds good."** The progressions and voicings are solid, but
  taste still has to be tuned by ear — which is exactly what your `autoresearch`
  loop is built to do. Point it at a harmony metric once Gap 2 lands.
- **Pitch detection on messy one-shots is imperfect.** Ship a manual key
  override; don't trust auto-detection blindly.
- **Scope creep is the real risk.** The engine is rich enough to tempt endless
  tuning. The MVP cut in Part 4 (step 7) is the discipline that gets a shippable
  thing out.
- **This analysis reads the code, not a running build.** Before starting, do one
  `pytest` pass to confirm the current suite is green as a baseline.

---

## Part 7 — Actual melodic-library inventory (scanned 2026-07-19)

Root scanned: `/Volumes/TBOTC 3/Sample Packs/2022 sample packs` (the live root in
`sample_packs.json`). Melodic/bass/chord/key audio found:

| Pack | Total | One-shots | Loops |
|---|---|---|---|
| Cymatics – Oracle | 276 | 0 | 276 |
| Cymatics – Cobra Hip Hop | 53 | 0 | 53 |
| Cymatics – Lofi Starter | 60 | 8 | 52 |
| Cymatics – Trap Starter | 50 | 0 | 50 |
| Cymatics – Dubstep Starter | 45 | 10 | 35 |
| Cymatics – Zodiac Vol 2 | 1 | 1 | 0 |
| **TOTAL** | **~485** | **19** | **466** |

Plus MIDI packs (`Python Free MIDI`, `Essential Chord MIDI`, `Melody MIDI`) — exact
notes, the ideal harmony seed.

**Full-library scan (both roots, 2026-07-19):**

| Library | Melodic files | Kind |
|---|---|---|
| Cymatics (2022 packs) | ~485 | mostly loops |
| Live loop cds | 116 | loops |
| Downloads Backup (drum kits) | ~486 | 808/bass one-shots + loops |
| Function Loops sampler | 96 melodic / 401 total | loops + one-shots, **key+bpm already in the filename** |
| **London Symphonic Strings Vol I** | **24,513** | sampled orchestra — real pitched note one-shots |
| MIDI packs (Python, Cobra) | — | exact notes |

**Function Loops scan (2026-07-22, completes this table):** 401 audio/MIDI
files across 7 subgenre folders (Breakcore, Darkwave, Pluggnb, Psytrance,
Trap & Hiphop, Vocal Phonk, Vocal Pop). 96 are melodic (bass/keys/synth/
guitar/instrumental), and 94 of those 96 already carry an explicit key tag
in the file name (e.g. `FL_TT_140_Bass_Synth_Boston_808_Gm.wav` = 140bpm,
Gm) — same zero-detection-risk shape as the MIDI packs, just in audio. This
is what let step 5 finish without Essentia (see Part 4).

**Takeaways:** (1) three source types now need zero pitch-detection risk —
**MIDI** (exact notes), **filename-tagged loops** (Function Loops, plus most
of Cymatics and Live loop cds, which turned out to use the same "key in the
name" convention — see Part 4 step 5), and the **Symphonic Strings** library
(24.5k real pitched notes, effectively a playable instrument in audio —
ideal for in-key chords and melody, though heavy to index; treat as pitched
one-shots keyed by note name, still un-ingested). (2) That leaves only
whatever loops turn out to have NO parseable key/bpm tag needing true audio
detection (Essentia/madmom) — a much smaller remainder than the original
gap analysis assumed. (3) Variety: three deep, low-risk wells now (MIDI,
tagged loops, Strings), not just one. (4) Licensing unchanged: fine because
each user brings their own library; just mind redistribution terms if you
publish demo beats built from these packs.
