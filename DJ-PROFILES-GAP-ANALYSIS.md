# DJ Production Profiles — Gap Analysis (Part 0)

*What `dj_production_profiles.json`'s research confirms vs. what it actually
changes. Grounded in `crew_config.json`, `tools/crew.py`, `tools/groove.py`,
`tools/pattern_gen.py`, and `.claude/skills/drum-loops/references/*.md` as of
2026-09-03. No code touched — this is the read-only pass.*

**Baseline:** `.venv/bin/python -m pytest tests/` — **976 passed, 3 skipped**,
374.99s, before anything below is touched.

**The one-line finding:** the profile is mostly confirmation, exactly as
billed — I checked every persona's `grounded_in` claim against the live
numbers in `crew_config.json` and they hold (offsets, swing %, dust/vinyl/
drive/sidechain/kick_dist/mix_sat, space treatments, harmonic `signature`
blocks). The real deltas are few, and one of them **collides with a standing
rule** rather than sharpening the code — flagged below, not resolved.

---

## What's already confirmed (no work — listed so you can see the coverage)

Spot-checked across all 9: Otto Grit's kick+10/snare-18ms split and 50% dust;
Cutz's uniform 53% swing and zero-jitter tightness; Crate Prophet's 60% swing
+ late snare + zero sidechain (the "1-in-10 no-duck" persona); Chrome Dial's
18ms-late clap flam is actually Glass Cat's (checked — matches), and Chrome
Dial's own bone-dry `dust=0.0`/`vinyl=0`; Sunday Chop's big-clap-over-snare
gain balance (0.9 vs 0.5) and MPC3000-clean mix; Night Metro's kick-only
distortion (`kick_dist=5.0`, mix stays clean) and heaviest sidechain; Rage
Engine's stacked distortion+glue (`kick_dist=6.0` **and** `mix_sat=4.0`, the
only nonzero `mix_sat` on the roster) plus its `burst_p=0.5` snare-fill
mechanism, which is a *live grammar feature*, not just a static bar; New
Math's quintuplet hat / Euclidean perc / 5-voice Atari-tuned chip harmony.
Rage Engine and New Math in particular came back almost entirely
`grounded_in`-confirmed — expected, since New Math was built from engine
design notes to begin with.

---

## The punch list

### 1. Three personas' signature arrangement move doesn't survive `compose()`
**Verified**, not inferred — ran `tools/identity_survival.py` (12 composed
beats/DJ) before writing this:

| Persona | Claimed move (profile + `listen`) | Lanes involved | FIGURE survival |
|---|---|---|---|
| Chrome Dial | bar 6 drops to near-nothing, answers bar 5 | kick, clap, perc | 0/12, 6/12, 0/12 |
| Night Metro | bar 5 drops to the 808 alone | kick, clap, hat | 0/12, 5/12, 0/12 |
| Glass Cat | bar 8 stop-starts | kick, snare, clap, snap | 0/12, 3/12, 3/12, 0/12 |

All three profiles restate this as a rule ("include at least one full
breakdown," "use a hard stop at a structural boundary," "at least one
deliberate near-empty bar"). Right now it's true of the one static prototype
file and roughly a quarter of real generated beats. `dj-identity-audit`'s own
fix list applies directly: raise the backbeat grammar's weight for the mode
that produces the drop (Night Metro already leans `halftime` 45%, which
isn't the same thing as "bar 5 specifically"), or pin the move in a
persona's `canon` the way genre figures are pinned. Kick is expected to be
low everywhere (0/12 across all 9 — by design, it's the freely-composed
lane) so it's not counted against these three.

### 2. Otto Grit: researched highs are matte/rolled-off — the parked EQ brightens
Two independent primary-source engineers (David Kennedy on the low end,
Dave Cooley on the master EQ) describe Otto Grit's reference sound as
**deliberately not bright** — "wasn't into slick top end," a "matte"
GML finish. `OWNER_TASTE["mix_eq"]` (parked in `groove.py`, approved by ear
2026-09-02, not yet applied to any DJ) is `high_db: +2.0 @ 8000Hz` — a
brightening move. `DECISIONS.md`'s 09-03 handoff names Otto Grit as the
suggested first DJ for the per-DJ effects pass. Applying the parked default
to him as-is would fight the research. No code change needed now — just a
flag before that pass starts: he likely wants `high_db` at 0 or negative,
not the roster default.

### 3. Otto Grit: a dormant function has a sourced use case now
Engineer Todd Fairall's account of the *Fantastic Vol. 2* sessions: the
sampled kick was reinforced with a short, gated ~40Hz sine/triangle under
it — sub weight, not a second audible drum. `groove.kick_layer()` does
exactly this kind of phase-verified top+sub blend and has been built,
tested, and uncalled since the 2026-09-02 audit found it. This is real work
(needs a sub-oscillator generator feeding it, not just a wire-up) but it's
the clearest "the research names the missing piece" match in the set.

### 4. Cutz: research conflicts with a standing rule — your call, not mine
Premier, in his own words: *"I'll go back to the same snares, kicks,
hi-hats... it's all in how you bounce them over the samples."* The profile's
rule: "reuse a small, consistent pool... rather than sourcing fresh drums
every time." That's a direct collision with the engine's own standing rule —
`tools/crew.py`'s docstring: *"the owner's rule (2026-07-14) is that every
character EXPERIMENTS — kick, snare, and the rest are re-picked per beat...
Only the STAMP is locked"* — reaffirmed 2026-07-18 when `open_soundbank`
removed even the taste-tag gating. I'm not picking a side. **Options, if you
want this pursued at all:** (a) leave Cutz on the same experiment-every-beat
rule as everyone else, research noted but not followed here; (b) give Cutz
specifically a small locked pool (3-5 kicks/snares/hats) the way the stamp
is already locked, as a one-persona exception. Say which, or say neither.

### 5. Glass Cat: which lane gets the gated reverb — contested inside the research itself
Chad Hugo's own quote is about the **"Grindin'" hook percussion** — "we
added a gate reverb to that sound" — which maps to Glass Cat's *stamp* lane
(the click/zap/glitch one-shot), not the snare. But the profile's own
summary paragraph calls the current `space=("gated",["snare"])` "historically
accurate" using that same quote. The profile's own `rules` line ("reserve
gated reverb for ONE signature/hook element") argues for moving it to the
stamp; its own prose argues for leaving it on the snare. Cheap to prove
either way — render both, let your ear pick, same as the Dilla
early/late question.

### 6. Crate Prophet: no mechanism for a second layer stacked under the main snare
Pete Rock, in his own words: *"Sometimes I'll use two snares, or a
tambourine on top of a snare, just to make it hit harder."* Right now a
tambourine can only arrive as an independent guest lane with its own
grammar-rolled timing — never locked to fire *with* the snare hit. Would
need a new "second sample synced to lane X's onsets" primitive. Real, but
more build than prove.

### 7. Chrome Dial: hat/perc density should ramp toward each snare hit, not just pick a shape
The research (secondary-sourced — "producers who've analyzed his catalog,"
not a direct quote) describes hats/shakers building in density *into* each
snare hit and tapering after. `gen_timekeeper()`'s modes (`eighths`,
`broken`, `offbeats`...) are fixed shapes per bar, none of them
snare-relative. Weaker sourcing than the others here, and would need new
per-hit density-shaping logic, not just a grammar-weight tweak.

### 8. Free: a stale gear fact in the skill's own reference file
`.claude/skills/drum-loops/references/research-producers.md:15,20` still
says DJ Premier's early sampler was an **Akai S950**, and doesn't mention
the RX-11 → SP-12 → HR-11 → S900 chain at all. The new profile's
primary-source correction (Premier's own account) is **Akai S900**. Doesn't
touch any code or number — `dust`/`vinyl`/`drive` aren't modeled per sampler
anywhere in the engine, confirmed by grep (no code references a sampler
model by name for any DJ). Pure doc fix, zero render needed, zero risk.

### 9. Cross-cutting: none of the 9 researched `bpm_range`s are implemented
Every profile gives an 8-10 BPM spread (e.g. Otto Grit 86-96); every one of
the 9 `engine_default_bpm` values matches `crew_config.json`'s single fixed
`bpm` exactly, and nothing rolls a beat's tempo within that range —
`render_crew_beat` reads `p["bpm"]` as one constant. This is one engine-level
feature, not nine persona fixes, and it's a judgment call: a single
signature tempo per DJ may be the point (each one has "a" pocket), or this
may be an omitted per-beat variation the research is now asking for.
Flagging, not recommending — this one's a taste call more than a research
call.

---

## Honest unknowns
- Items 6 and 7 are real but I haven't scoped the exact code shape for
  either — "needs a new primitive" is as far as read-only analysis goes.
- I did not run `identity_survival.py` against every claimed structural
  trait in all 9 profiles, only the three that describe a specific,
  multi-lane, single-bar arrangement move (the shape most likely to be
  fragile per the skill's own failure case). Stamp-lane traits (every
  persona's bars-4/8-or-1/5 producer tag) are confirmed safe by construction
  — `stamp` never appears in any DJ's `grammar` dict, so `compose()` never
  touches it.
- Item 5 (Glass Cat) is presented as contested because the research
  document disagrees with itself, not because I'm uncertain what it says.
