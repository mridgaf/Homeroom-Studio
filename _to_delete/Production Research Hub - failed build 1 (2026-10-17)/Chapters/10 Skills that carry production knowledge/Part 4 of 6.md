# Chapter 10: Skills that carry production knowledge
## Part 4 of 6

_The saved skills (beat crew, drum loops, recipes, Reason reference, plus older style/gear skills) that hold production rules and producer styles._

**In this part:**
- SKILL.md — One Legend, rebuilt from research, judged by his ear
- SKILL.md — Looking up Reason facts

(Next: Part 5 of 6)


=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:.claude/skills/legend-new-build/SKILL.md
=====================================================

---
name: legend-new-build
description: "Rebuild one Legend's or one GENRE's sound from research and audition it old-vs-new. Use when the owner names a Legend or genre to work on, asks what is left to do on the legends or genres, says tune the genres / new build / rebuild / research him / make him sound like himself, or when a Legend's beats do not match his own written description. Covers the Legends and the 18 genres; the nine crew DJs are explicitly NOT in scope."
---

# One Legend, rebuilt from research, judged by his ear

## What this is

Owner 2026-09-05, after Doc Day's rebuild landed: *"I'll want this same for
all remaining legends. Not in the 9. Create something to make that easy and
clear for each session"* — **"So you remember."**

Fourteen Legends: 11 confirmed, 3 not started (DJ Premium, No Alias, Well
Damn — run the status command below, it is always current). One per
session. **The nine crew DJs are not in scope** and their settings must not
move.

## Genres use this same process (owner 2026-09-24)

"Start tuning the genres using the same format as the rebuild for DJs,
research first then build." His answers, all clickable:
- **A-Z, one at a time**, same as the Legends. Progress lives in
  `genre_newbuild_status.json`. All 18 were research-built by 2026-09-25;
  what is left is rendering (only when he asks) and his ear.
- **Keep the approved mix, tune the style.** True levels, the low-end
  rules, one bass per beat and the Loops page's own levels stay exactly
  as they are. Change the genre's drums, tempo, sounds, tags and chords.
- **Dirt follows the research** without asking: if the sources say the
  genre is dirty, set `allow_dirt` (True or "low") for that genre.
- Every tool takes `--genres`:
  `tools/legend_newbuild.py --genres --legend "Name" --tags` and
  `tools/make_legend_newbuild.py --genres --legend "Name" --structure`.
  Backups are `genres_config.pre-<slug>-<date>.json`.
- A genre with a `_research_note` is never reset by a GENRES_VERSION bump.
- Genres are not DJs: `own_soundbank` gates EVERY pick (no open-bank
  share) and they are exempt from the kick-flavor streak-breaker.
- **Fresh TinyFish research for every genre** (owner 2026-09-24), sources
  quoted in its `_research_note`. Never build from the old config alone.
- **`"flavor_match": true` on every genre build** (owner 2026-09-24: "we
  should at least look for synonyms or similar words"). He ruled on every
  synonym pair himself — see `tools/flavor_tags.py` SYNONYM_GROUPS. Any
  NEW pairing you are unsure of: ask him with clickable options ("I can
  tell you immediately what should be what"), never guess.
- A synonym never lands a sidestick/rim/clap/combo in a snare slot or an
  open hat/combo in a hat slot (`_NOT_A_SNARE`, `_NOT_A_CLOSED_HAT`). After
  `--tags`, still list the files each lane newly reaches and read them.
- **Every build touches two test lists** in `tests/test_crew.py`: the
  own_soundbank allow-list, and (if dirt goes on) the `allow_dirt` dict in
  `test_allow_dirt_is_eight_presets_not_the_roster`. Also grep the tests
  for the genre's name: a test may use it as its "clean" example (Memphis
  in `test_fx_on_saves_a_copy...` broke when Memphis turned dirty).
- **A sound the research names may not exist in his library** (bounce
  whistles, timbale, clave: 0 files). Use the nearest real sound and say
  so in the `_research_note`; never fake it with a wrong word.

## Start every session here

```
./.venv/bin/python tools/legend_newbuild.py
```

Prints where every Legend stands, and for anyone not started: his `listen`
line, any ABSOLUTE words in it, and what is still wrong with his config.
Stage comes from `legend_newbuild_status.json`; the checks are read live so
they cannot go stale. Add `--tags` to audit taste tags against the real
library (needs TBOTC 3 mounted).

## The order of work

**0. A Legend lives in `legends_config.json` — that file ONLY.**
`legends.load_legends()` reads the config; the built-ins in `tools/legends.py`
are used only when the config file is missing. A block added to
`tools/legends.py` alone silently does not exist. Adding or removing a Legend
also breaks the roster count in `tests/test_crew.py`
(`assert len(legends) == 14`) — update it in the same step.

**1. Back up first, or there is nothing to A/B.**
```
cp legends_config.json legends_config.pre-<slug>-$(date +%F).json
```
One backup per legend, and only one — the render script now REFUSES to
guess between two, and refuses with NO backup. A brand-new Legend (not in
the backup) has no "old": the audition is new beats only, say so in the
README — don't fake a before. It REFUSES to
guess between two, because it once silently picked a half-built
intermediate and reported +0.92 dB where the truth was +5.03.

**1b. Check the nine for the same producer BEFORE you research.**
```
./.venv/bin/python -c "import sys;sys.path.insert(0,'tools');import json;\
d=json.load(open('crew_config.json'));print([(n,p.get('built')) for n,p in \
(d.get('CREW') or d).items() if isinstance(p,dict)])"
```
Two of the twelve turned out to be straight duplicates of a crew DJ, both
found on 2026-09-05 and neither noticed for months, because the legends and
the nine are audited separately: **Farrow was Glass Cat** (Pharrell, same
bpm, same lanes, same kit tags, same 18 ms flam) and **Kane East was Sunday
Chop** (Kanye, same 57% swing, same "BIG clap with the snare tucked
underneath", same tambourine offbeats). If the producer is already in the
nine, stop and ask the owner which era each one keeps — he has answered
this twice and both times the crew DJ kept what it had and the LEGEND moved
to a different era. Do not pick the era for him.

**2. Research him, then write down who said so.** Every change goes in his
`_research_note` with its source. A change nobody can source is not a
research build — flag it as unsourced and leave it at the roster default,
the way saturation and sidechain were left for Doc Day.

**3. His `listen` line is the top rule.** Owner, 2026-09-05: *"Keep
following the description as the top rule."* Where the description and an
inherited house rule disagree, the description wins — see below.

**4. Turn his ABSOLUTES into invariants.** If his line says *never*,
*always*, *dead straight*, *locked* — that is not a weight. Read
`hard-rule-invariant`: one choke point, it refuses, and a test that goes
red if it is removed. Doc Day's snare mode was `[[backbeat, 0.9], [sparse,
0.1]]` against a description saying the snare NEVER leaves 2 and 4, and the
one-in-ten fired in a real audition.

**5. Turn his sound bank on and fix the tags.**
`"own_soundbank": true` makes his taste tags actually gate sample picks —
without it the July open-sound-bank rule wipes them and every pick is
random from the whole bucket. **Pick tags FROM the library, not from
the description.** First list the real words in that lane's bucket:
```
./.venv/bin/python tools/legend_newbuild.py --words snare
```
(any bucket: kick, snare, hat, clap, rim, perc, fx, vox, bass, crash...).
Choose from what it prints. `--tags` afterwards only confirms; used alone it
tells you a word is dead after you picked it (09-09, cost a render).
**Never put `dry` on a snare:** it matches sidesticks and rims (8 of 41 dry
snares were sidesticks; walked into twice). **Then check the tags against real
filenames** (`--tags`): they match FILENAMES, not intent. Doc Day's
`punch/knock/deep` matched ONE file in the library, and `boom` matched
three of which two were 808s — the words read perfectly and delivered the
opposite.

**Set `"flavor_match": true`.** It lets a sound word also reach its
synonyms/spellings ("tight" also finds "tite" files). Since 2026-09-25 it is
on for EVERY crew DJ, Legend and genre (owner). `--tags` audits with the same
synonym logic. See `tools/flavor_tags.py` for the words deliberately NOT
grouped (`dry`, `boom`, `punch`/`knock`/`deep`) and why.

**6. Render the audition.**
```
./.venv/bin/python tools/make_legend_newbuild.py --legend "Name"
```
Every lesson from the three Doc Day batches is already in that script —
read its docstring rather than re-deriving them. It refuses to overwrite a
folder he already has.

**7. Read the printed sample list before you ship it.**
NOT the stamp: `STAMP_LANE = False` in `tools/beat_machine.py` since
2026-08-01, so the stamp never plays — tuning its tags changes nothing you
can hear (this cost a full render cycle on 09-09). Read every lane that
DOES play: snare, hat, kick, perc. State the pass
condition first, then check it. This is the step whose absence cost a whole
round trip: a batch went out with two sidesticks where snares belong, open
hats where tight hats belong, and a talking drum.

**8. Tests, then hand it to him.** Full suite (`.venv/bin/python -m pytest
tests/ -q`, ~14 min, baseline 1275 passed / 3 skipped on 2026-09-28). Any invariant test
that touches `compose()` must be run several times over — compose() re-rolls
per process, so one green run proves nothing.

**9. Record the stage.** Update `legend_newbuild_status.json` and append to
`DECISIONS.md`. `confirmed` means **he has heard it and said yes** — nothing
else counts. Measured-and-shipped is `auditioned`.

## What the melodic library actually holds (re-measured 2026-09-28)

Chord voices (`chord_source`) come from the instrument index, NOT the drum
buckets. 4,386 pitched samples: piano 959, brass 783, string 745, wood 712,
bell 469, guitar 305, synth 235, organ 146, pad 16, pluck 16. **Zero choir,
zero chip.** So `choir` plays pad, and `chip` has nothing to play. The old
"only 7 bell samples exist" note (09-09) is dead — don't repeat it. Re-count:
`instrument_sampler.scan()` grouped by `"group"`.

## When an old decision blocks the new build

His standing rule, 2026-09-05: *"Overrule old decisions when they cause
problems with my new request. But always ask in plain language first."*

Ask him with real options, include the scope choice (this one legend vs all
twelve — he has twice chosen the narrow one), and then act on his answer in
the same session. Do not park it as a flagged open item; that is what he
was correcting.

**Scope every exemption to the one legend.** `own_soundbank` and
`snare_locked_24` are both single-preset opt-outs defaulting to off, and
each has a test asserting only the intended legend carries it. Follow that
shape — a roster-wide change to fix one man is how the nine get damaged.

## Do not

- Touch the nine crew DJs. Not in scope, he said so.
- Blanket-apply Doc Day's answers. Only Doc Day's line says the snare NEVER
  leaves 2 and 4; **Timberline's clap "answers instead of insists", J
  Dillo's snare rushes 20 ms early, Farrow's clap lands 18 ms late.** Locking
  those to 2 and 4 would destroy the identity.
- Call it done off a measurement. Only his ear closes a legend.

=====================================================
SOURCE FILE: SKILL.md
ORIGINAL LOCATION: HS:.claude/skills/reason-reference/SKILL.md
=====================================================

---
name: reason-reference
description: "How to look up a fact about Reason 12 without guessing — the exact spelling of any device parameter, and what any control actually does. Use whenever you need a Reason device or parameter name (for a remotemap, a recipe, a device_refs entry, or a prompt handed to the local model), whenever asked what a Reason control does, and whenever new Reason documentation arrives and needs absorbing. Also use before claiming a device or parameter does not exist. Prevents the failure this layer punishes hardest: a parameter name that is almost right, which Reason rejects silently."
---

# Looking up Reason facts

**This project is Reason 12, at all times.** The install is 12.7.4d3; the
documentation is the Reason 12.7 Operation Manual. Reason 7 material is out of
scope — the 2013 Help Files that used to sit in `reason_docs/` were retired on
2026-09-10 and must not be cited, quoted, or regenerated. If something can only
be sourced to Reason 7, the honest answer is **"not confirmed for Reason 12."**

**Never type a Reason parameter name from memory.** A name that is slightly wrong
fails *silently* — Reason doesn't complain, the knob just never moves. Every name
gets copied from a source below.

## Two sources, two different jobs

| Question | Source | Vintage |
|---|---|---|
| What is this parameter **called**? | `docs/reason/remote-vocab.json` | Reason 12.7.4d3 factory maps |
| What does this control **do**? | `~/.reason_voice/reason12_manual/` | Reason 12.7 Operation Manual (Oct 2023) |

Both are current Reason 12. They still do different jobs, so don't swap them: the
manual's prose is not a spelling authority. A control the manual calls "Filter
Freq" may be `Filter 1 Freq` in the factory map, and only the map is what Reason
accepts.

Full background on the three ways into Reason and why two of them are the wrong
ones to build on: **`docs/reason/FINDINGS.md`. Read it before proposing anything
about controlling Reason.**

## Names — `tools/reason_vocab.py`

Built from Reason 12's own factory mapping files
(`/Applications/Reason 12.app/Contents/Resources/Remote/`, 182 `.remotemap` files).
**148 devices, 11,503 parameters**, spelled exactly as Reason spells them.

```bash
python3 tools/reason_vocab.py --device "MClass Compressor"   # look one up
python3 tools/reason_vocab.py                                # rebuild the json
```

Rebuild after a Reason update — the file is a snapshot, not a fixed truth. It
records the Reason version it came from.

Rack Extensions and Reason-12 devices appear under reverse-DNS ids
(`se.propellerheads.Mimic`); the tool also stores a readable `name` ("Mimic"), and
`--device` matches on that.

**It is a lower bound, not a complete list.** It holds what factory control surfaces
happen to map, which is not everything a device exposes. Absence from this file does
not prove a parameter doesn't exist — check the device in Reason before concluding
anything is missing.

Not every entry in a factory map is a parameter — the same column also holds text
constants (`"Thresh"`), numeric constants and mapping-variation assignments
(`Group=3`, `Shift=ShiftDown`), which drive the *surface's* display rather than the
rack. The parser filters them and `tests/test_reason_vocab.py` pins that; if you
loosen the filter, that test is what tells you.

## Behaviour — the Reason 12.7 Operation Manual

`~/.reason_voice/reason12_manual/`

| File | What it is |
|---|---|
| `full_chapters/NN-slug.txt` | one file per chapter, 70 of them — **grep these** |
| `chapter_pages.tsv` | chapter number, title, first page, last page |
| `Reason_12.7_Operation_Manual_Full_Text.md` | all 70 chapters in one 2.8 MB file |
| `Reason_12.7_Illustrated_Device_Reference.html` | front/back panel photos, 54 devices |
| `manifest.json` | chapter + device + page range + panel image, already joined |

1,466 pages, 385,496 words, extracted from the official PDF with `pdftotext -layout`,
so the page numbers are the manual's own.

**Cite the page.** "Kbd Track holds the oscillator's pitch constant regardless of
incoming note pitch — manual p. 869" can be checked in ten seconds. An uncited claim
about a control cannot.

Search the per-chapter files. Don't read the 2.8 MB combined file into context:

```bash
cd ~/.reason_voice/reason12_manual
grep -rli "kbd" full_chapters/                                      # which chapters
grep -n -B2 -A8 -iE "kbd[. ]+track" full_chapters/34-subtractor-synthesizer.txt
awk -F'\t' '$1==34 {print $2, "pp."$3"-"$4}' chapter_pages.tsv       # -> pp.857-882
```

**Always match punctuation loosely.** The manual writes Subtractor's control as
`Kbd. Track` — with a period. `grep -i "kbd track"` returns **zero** hits on that
chapter and would have you report the control doesn't exist. `grep -iE "kbd[. ]+track"`
finds it. Verified 2026-09-10; treat a zero-hit result as "my search was wrong" before
"the manual is silent."

Known limits, so nobody over-claims from it:

- **Stock Reason 12 only.** No Rack Extensions, no VST specifics beyond the generic
  VST chapter. For an RE, the factory maps are the only source here.
- **Grep is literal.** It finds "sidechain", not "pumping", and it splits on hyphens
  the PDF inserted at line breaks. Try the control's real name, loosely punctuated,
  before concluding the manual is silent.
- The manual is 12.7; the install is 12.7.4d3. Minor drift is possible, and the
  factory maps win on any naming disagreement.

## What a Standard MIDI File does on import (Reason 12.7 manual, confirmed live 2026-09-25)

Sources: docs.reasonstudios.com/reason12/song-file-handling, and the test in
`experiments/automation-test-2026-09-25/`.

- File > Import MIDI File: **one track per MIDI track, each with an ID8** (the
  General MIDI sound module), and the file's tempo is applied (90 BPM landed as
  90). Use SMF **format 1** so the parts stay separate.
- Pitch bend and mod wheel stay inside the note clip.
- Other CCs → **separate automation lanes** named "Controller #N". If the
  device has no control for that CC it is an **alien clip** (striped red and
  yellow) and does nothing. CC74 on an ID8 did exactly this.
- A MIDI file **cannot** create effects, cables or patches, or target an
  effect. Aiming CCs at specific instrument knobs needs a Reason 12 CC chart,
  and we have none (only Reason 7, which is out of scope). Don't guess the numbers.
- For automation on real parameters, use the Remote bridge (see
  `reason-remote-bridge` → "Recording automation through the bridge").

## When new documentation arrives

More is expected. The routine:

1. Note where it came from and **what version of Reason it describes** — that is the
   single most important fact about any Reason document here, and the easiest to lose.
2. If it describes **Reason 12.x**, it supersedes what's here. Extract it, record the
   version, and update the table above.
3. If it predates Reason 12, **it does not enter this project.** Not as a fallback,
   not as "better than nothing." A wrong answer that sounds right is worse than a gap.
4. If it changes a conclusion in `docs/reason/FINDINGS.md`, edit that file. It exists
   so nobody re-derives this, and it is only useful if it stays true.

## Related

- `reason-remote-bridge` — the codec/map files themselves, and how to add a knob.
- `device_refs/*.md` — plain-language guides the app reads aloud. Original wording,
  in the repo; the extracted manual is raw source, not a substitute.

=== END OF PART ===
