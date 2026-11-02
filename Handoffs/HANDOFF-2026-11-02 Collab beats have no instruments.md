# Handoff: two-DJ collab = drums only, no instruments (2026-11-02)

## Owner's report
Pick two DJs to collaborate → the beat comes out as a drum beat only. No chords, bass line or melody.
A solo beat from the same DJs has instruments.

## Most likely cause (read in code, NOT yet proven by a test run)
`tools/beat_machine.py`, `generate()` ~line 3918:

```python
if not dirs["chords"] and not dirs.get("no_chords") \
        and (preset.get("signature") or {}).get("chords_default"):
    dirs = dict(dirs, chords=True)
```

Chords only turn on without typed directions when the preset carries a
`signature` with `chords_default`. A solo preset has the DJ's `signature`.
`collab_preset()` (~line 834) builds a fresh dict `p` and never copies
`signature` (nor `chord_flow`, `chord_gen`, `one_chord`, melody settings,
which `_build_chords` ~line 2331 reads off the preset). So for a collab
`dirs["chords"]` stays False → `_build_chords` returns `(None, None)` →
no chord, bass or melody lanes.

Workarounds that already make chords appear in a collab (so no audio
bug downstream): typing a chord word in Directions, or picking a Key
(line ~3846 forces chords on).

## Owner decision needed BEFORE the fix (ask, clickable)
Whose harmony does a collab get?
1. Host's (first-picked DJ) signature — simplest, matches "first pick names the folder".
2. Deal it like the drum jobs: harmony is a 5th job, seeded 50/50 between the DJs (matches the 2026-07-16 "even 50/50 blend" rule).
3. Instruments on if EITHER DJ has `chords_default`; voice from whoever wins the deal.

## Fix shape once decided
- In `collab_preset`, copy the chosen parent's `signature` (and the other harmony keys `_build_chords` reads) into `p`.
- Check melody: confirm the melody lane is driven by the same signature path; if not, follow it.
- Also check the Legends and Genres collab paths use `collab_preset` too (mixed collabs: line ~3868).

## Proof
- New test: a two-DJ collab of DJs whose solo beats have chords → collab recipe has `harmony` and chord lanes.
- Measure a generated collab's chord stem is not silent. Don't render a full beat unless the owner asks (house rule).
