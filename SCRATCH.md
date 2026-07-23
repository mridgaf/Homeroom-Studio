# Scratch (live reasoning trace)

Disposable. Cleared or overwritten each session. Purpose: capture the *path*
through a problem, not just the destination — so if I reverse course, the
reason is visible instead of lost.

One line per turning point. Not a transcript.

Format:
```
- [tried/considered] X → [result] → [kept / reversed because Y]
```

---

## Current session

- goal: continue chord-synth integration → 3 Dre audition beats → traced the
  render, found the identity-blind seam (beat_machine ~L1017: random root,
  hardcoded minor, no chord_source) → wired a signature chooser instead of
  patching one call site.
- chose strings-as-source (built, never wired) over the deferred synth-lead
  voices → Dre is the proposal's pick precisely because he exercises strings.
- kept `signature` a deep-copied preset key (normalize_preset preserves unknown
  keys) → zero loader changes, no-signature path stays byte-identical.
- first render batch #842-844 looked all-synth-pad → was a stem-glob bug (Doc
  Day folder holds every beat's stems); real stems showed strings landing.
- but sustain family included legato (~2s) → tiled 4-5x on ~10s chords → dropped
  leg from ARTIC_FAMILY, retired #842-844 to Trash, re-rendered #845-847 clean.
- added only gfunk_minor_i_iv_v (Dre's slug); skipped the 2 slugs for
  G-funk/Miami as config nothing reads yet.
- owner feedback on #845-847: "847 out of key at the end, none sound like Dre."
  → FFT/nearest check proved pitches were correct (not a bug); root causes were
  #847's m7 (vamp_i_iv7) + the held-drone voice.
- fixed m7 (Dre = triads only), then asked direction → owner: "rhythmic riff".
- built arp as one buffer per chord (rhythm baked in) not multi-lane → keeps all
  the lane/bass/MIDI wiring + clean stems; gated on signature chord_rhythm=arp so
  every other identity's held chord is untouched.
- synth-arp (pluck) smears under beat reverb (onset detector saw 1), strings-arp
  stays crisp; raw arp verified rhythmic (16 onsets). Left pluck decay for the
  ear to judge rather than tuning blind. Re-rendered #848-850.

(clear this section at the start of a new session, or archive worth-keeping
lines into DECISIONS.md's Reasoning field first)
