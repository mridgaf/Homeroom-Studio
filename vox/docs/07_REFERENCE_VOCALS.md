# Reference vocals — Jay-Z, Tupac, Eminem

Research pass, 2026-08-14. Sourced from engineer interviews (Sound On Sound,
Waves, Gearspace, Equipboard), not from tutorial-blog paraphrase where
avoidable. Nothing here is built yet. This document exists so the build starts
from evidence instead of vibes.

Provenance tags: `[verified]` = stated by the engineer who did the work.
`[recalled]` = widely reported, weaker sourcing. `[inferred]` = my reasoning.

---

## 0. The finding that reorganises everything

The three sounds are **not three mix chains**. They are three different KINDS
of thing, and only one of them is mostly mixing.

| | What actually makes the sound | Reachable by processing one take? |
|---|---|---|
| Jay-Z | **Mix identity.** One engineer, consistent chain. | **Yes — mostly.** |
| Eminem | **Arrangement identity.** 3–6 separate real overdubs, panned. | **Partly.** Needs takes from him. |
| Tupac | **Performance + tracking identity.** One take, sung hot, minimal processing. | **Partly.** Some is the performance. |

This is why "apply a look to my lyrics" works cleanly for one of the three and
needs his participation for the other two. That's not a limitation of the tool —
it's what those records actually are.

---

## 1. Jay-Z

The owner's note is correct and it is the key to this entry: **Jay-Z has used
many producers** — Ski, DJ Premier, Just Blaze, Kanye, Timbaland, Pharrell,
No I.D., Mike Dean. The beats have nothing in common.

The vocal still sounds like Jay-Z on all of them.

**Because the constant is not the producer — it's Young Guru.** Guru has mixed
10 of Jay-Z's 12 albums `[verified]`. The producer changes; the vocal engineer
doesn't. That is the entire reason a "Jay-Z look" is a coherent thing to build,
and it means the target is Guru's chain, not any producer's.

### Tracking `[verified]`
- Neumann U87 or U67 → **Avalon VT-737** (using its preamp *and* its compressor)
- 24-bit / 44.1 kHz into Pro Tools. Guru is explicitly not a high-sample-rate guy.

### Mix `[verified]`
- **Fairchild 660** (Waves) on *every* vocal track — lead and ad-libs alike.
  Guru's words: it "glues them together without having this super compressor sound."
  Read: gentle, slow, colouring — not a level-control compressor.
- **ADL 1500** in series after it — "presence that the plug-in can't do."
  So: **two compressors in series, each doing a little**, not one doing a lot.
- **Two Focusrite 110 EQs** after compression. EQ AFTER compression, not before.
- **Lexicon 480** reverb.
- **TC Electronic D-Two, quarter-note delay.** Note: 1/4, not the dotted-eighth
  that's fashionable now.
- Lead, doubles and ad-libs all get the **same** processing `[verified]`.

### The philosophy `[verified]`
Guru's teaching is built around **subtractive EQ**: he makes room for the vocal
by carving the *beat*, not by boosting the voice. He also stresses clip-gaining
before any processing.

**What this means for us:** the Jay-Z look is a *restraint* profile. Two gentle
compressors, EQ after them, cuts not boosts, a plate and a 1/4-note delay.
Nothing extreme anywhere. That is very buildable.

---

## 2. Eminem

### Tracking `[verified]`
- **Sony C800G** → **Avalon VT-737**. Same mic Dre uses; Em has always used it.
- 44.1/24 into Pro Tools, tracked in a large live room with gobos.

### Mix `[verified — Mike Strange, SOS]`
- Compression: **Alta Moda Unicomp**, plus a **Requisite L2M** tube mastering
  compressor — "on every song I've recorded for Em."
- **Massenburg EQ** on the rap vocals. SSL console EQ + compression.
- Delay: **TC 2290**. Reverbs: Bricasti, Eventide 2016, Lexicon 480 & PCM70, SPX90.
- **Distortion**: made by driving the vocal hard from the Alta Moda back into
  the SSL returns. Not a plugin — a deliberate overdrive stage.

### The part that is NOT mixing `[verified]`
- Rap vocals **double-tracked throughout**.
- Hooks recorded **five times**. Bridges **six times**. Real overdubs, not copies.
- **"I have never done vocal comps for him."** No comping. Every take is a take.

`[recalled]` Em has described four dubs: one screamed, one whispered, two normal;
dubs panned to different places rather than stacked in one spot, with different
dynamics per dub.

`[recalled]` Common reconstruction: 3 tracks, two panned ~65% L/R and dropped in
level under a centre lead, the group bus-compressed in parallel.

**What this means for us:** the crispness people hear as "Eminem" is largely
**many real takes, panned wide, at different intensities**, plus a hard-driven
distortion stage. Fabricating that from one take is exactly the STACK problem
already documented in `01_MASTER_SPEC.md`. Confirms the earlier decision: STACK
should align and glue **real takes he records**, not synthesise fake ones.

---

## 3. Tupac

### Tracking `[verified]`
- Death Row: **Neumann U87** → Neve or SSL 4000 preamp → **Studer A800** tape.
- Other rooms `[verified — engineer Paul Arnold]`: U87 through an SSL E preamp
  and its onboard compressor (Quad, NYC); later an **AKG 414** through an SSL G
  preamp with the console compressor or a **dbx 160**.

### The defining fact `[verified]`
**"One-Take Tupac."** *All Eyez on Me* was recorded in about two weeks. Speed
and performance, not production, are the sound.

**What this means for us:** the Tupac profile is the *least* processed of the
three. Console compressor, tape, room, done. Two things carry it:

1. **Tape.** The Studer A800 is doing real work — soft saturation, gentle
   high-end loss, transient rounding. That is `Saturation` + a tilt, and it's
   buildable.
2. **Analogue console compression**, which behaves differently from a modern
   digital compressor — softer knee, program-dependent release.

`[inferred]` The risk with this profile is faking rawness by *adding* dirt.
Correct move is the opposite: take processing away, then add tape.

---

## 4. Common ground across all three

Worth noting how much overlaps — this is the "studio quality baseline" the
owner asked for, and all three sit on top of it:

- **Large-diaphragm condenser → Avalon 737 or an SSL/Neve channel.** Every one.
- **Compression in stages**, each doing a few dB. Never one compressor doing 10.
  `[recalled]` Dre's *In Da Club* chain: ~7:1, medium attack, fast release,
  3–4 dB typical, up to 7 dB on peaks.
- **Vocals mixed deliberately loud.** `[recalled]` Dre mixes them a little hot
  on purpose so mastering's bass doesn't bury them.
- **Doubles are recorded, never generated.** All three.
- Hardware reverb + a tempo-synced delay. Delay time is the main dialect
  difference (Jay 1/4, modern rap 1/8D).

`[recalled]` Measurable targets from mix-analysis literature: lead vocal
integrated loudness ≈ **4.5 LUFS below** the full mix (range 3–6); for rap,
momentary vocal **4–6 dB above** the instrumental.

---

## 5. How we get past "clearly in the lane"

The owner asked for as close as possible, not just the right neighbourhood.
The honest engineering path:

**We cannot copy the gear.** No Fairchild, no Studer, no C800G, no SSL.
Modelling each box by ear is how you land at "in the lane" and stop.

**We can copy the RESULT, measured.** Take actual reference records, measure
what the vocal is doing, and make our output hit the same numbers:

| Measure | What it captures |
|---|---|
| Long-term spectrum of the vocal | tone — the single biggest identity cue |
| Crest factor / short-term dynamics | how hard it's compressed, and how fast |
| Vocal-to-beat loudness ratio | how forward the voice sits |
| Stereo width vs. frequency | how the doubles are spread |
| Harmonic distortion vs. level | how much tape/drive is on it |
| Reverb decay + pre-delay, delay time | the space |

Six numbers per artist. Then it's a closed loop: measure the target, measure our
render, correct the difference. Same method already proven on THROW's ducking,
where an open-loop control delivered 4.3 dB for a requested 6 and the closed
loop delivered 5.93.

That is the difference between imitating settings and matching an outcome, and
it is the only route to "as comparable as possible" that doesn't depend on
owning the rack.

**Requirement:** this needs real reference audio. Isolated vocal stems would be
ideal; full mixes are workable for some measures and useless for others.

---

## 6. Open questions

**BLOCKING — reference audio.** Section 5 is the whole plan and it can't start
without files. What can the owner supply?

**BLOCKING — the Eminem profile.** Its core is 3–6 real takes. Is he willing to
record doubles, or does the Eminem look have to work from a single take?
The answer changes what gets built, not just how well it works.

## Sources

- [Secrets Of The Mix Engineers: Young Guru — Sound On Sound](https://www.soundonsound.com/techniques/secrets-mix-engineers-young-guru)
- [Mike Strange Jr: Eminem *Recovery* — Sound On Sound](https://www.soundonsound.com/techniques/mike-strange-jr-eminem-recovery)
- [Young Guru: The Art of Vocal Mixing and Subtractive EQ — Waves](https://www.waves.com/waves-premium-masterclasses-young-guru)
- [2Pac — Equipboard](https://equipboard.com/pros/2pac)
- [Eminem — Equipboard](https://equipboard.com/pros/eminem)
- [What gear was used to record Pac vocals — Gearspace](https://gearspace.com/board/rap-hip-hop-engineering-and-production/380555-what-gear-used-record-pac-vocals.html)
- [Eminem vocal stacks — Gearspace](https://gearspace.com/board/rap-hip-hop-engineering-and-production/178467-eminem-vocal-stacks.html)
- [Secrets to Mixing Rap Vocals — Produce Like A Pro](https://producelikepro.com/blog/mixing-rap-vocals/)
- [The Perfect Vocal Loudness (Backed by Data) — Mastering The Mix](https://www.masteringthemix.com/blogs/learn/the-perfect-vocal-loudness-with-data)
