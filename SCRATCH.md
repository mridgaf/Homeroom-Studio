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
- owner's real favorites: #843 (m7, held, strings), #845 (gfunk, held, mixed
  voice), #849 (gfunk, arp, mixed voice) → the m7-removal and strings-only
  calls from last entry were WRONG per the owner's own ear; #847 was never
  about the chord quality. Reversed both, made rhythm+source a per-beat roll
  instead of picking one fixed answer.
- mid-task found a partial auto-edit already in the file (chord_rhythm roll +
  vary_preset tempo clamp — good, kept) but with stale values (90-93 not 90-96,
  strings-only not 2:1, m7 still missing) → chat instructions are the source of
  truth over an unreviewed file edit, corrected all three against what the
  owner actually typed.
- "constrain kick to clean-punch, ignore 808" — asked Dre-only vs engine-wide
  since engine-wide kills a real owner rule (2026-07-18 "add the root") and
  collides with G-funk/Memphis/Miami-bass's OWN 808 identity from yesterday's
  proposal doc → owner said engine-wide, proceeded (reaffirmed = decided).
- grepped every caller before declaring the kick filter done (ponytail
  discipline) → found _compose_odd (3/4, 6/8 path) rolls kick_flavors
  independently of compose()'s main path → would have shipped odd-meter beats
  still reaching 808 if I'd stopped at the first call site.
- checked how many DJs actually have a 2nd non-808 kick flavor to fall back on
  → ZERO, roster-wide (every style is one clean + one 808, never two clean) →
  "no 808" quietly also means "no kick variety" for literally everyone. Real
  finding, not hypothetical — flagged plainly, didn't hide it in the render.
- 2 of 5 rendered kicks had "808" IN THE FILENAME despite the clean-punch
  filter → looked like a possible leak → read crew._load_choked, confirmed
  every kick is hard-truncated to the flavor's 0.2-0.5s choke regardless of
  source file name/length → sample-pack branding, not a real miss. Verified by
  reading the choke code, not by trusting a tag or a noisy DSP heuristic (first
  attempt at measuring "is this really short" by decay-time was too noisy to
  trust; the choke code is the authoritative answer).
- test_pattern_gen.py had 2 tests asserting the OLD "808 reachable" behavior —
  rewrote both against the new verified reality rather than leaving them red;
  also had to fix my own bug in the rewrite (compose() mutates in place and
  returns notes only, not (preset, notes) — mis-unpacked a list as a tuple
  once, TypeError, fixed).
- rendered #859-863 last: tempo 96/90/93/96/90 (all in range), kick
  clean/short punch+knock on all 5, chord_rhythm 2 arp + 3 held, progressions
  4 gfunk + 1 vamp (m7 confirmed reachable again), chord source strings in all
  5 + synth-arp in 2. All LUFS -13.0, peaks -5.7 to -6.1 dBFS. Not yet
  committed — waiting on owner sign-off same as every batch this session.

(clear this section at the start of a new session, or archive worth-keeping
lines into DECISIONS.md's Reasoning field first)
