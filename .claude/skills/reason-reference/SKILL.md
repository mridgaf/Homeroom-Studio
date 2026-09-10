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
