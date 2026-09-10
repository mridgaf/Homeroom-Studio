---
name: reason-reference
description: "How to look up a fact about Reason 12 without guessing — the exact spelling of any device parameter, and what any control actually does. Use whenever you need a Reason device or parameter name (for a remotemap, a recipe, a device_refs entry, or a prompt handed to the local model), whenever asked what a Reason control does, and whenever new Reason documentation arrives and needs absorbing. Also use before claiming a device or parameter does not exist. Prevents the failure this layer punishes hardest: a parameter name that is almost right, which Reason rejects silently."
---

# Looking up Reason facts

**Never type a Reason parameter name from memory.** A name that is slightly wrong
fails *silently* — Reason doesn't complain, the knob just never moves. Every name
gets copied from one of the two sources below.

## Two sources, two different jobs

| Question | Source | Vintage |
|---|---|---|
| What is this parameter **called**? | `docs/reason/remote-vocab.json` | Reason 12 — current |
| What does this control **do**? | `reason_docs/*.md` | Reason 7 (2013) |

Do not swap them. The 2013 manual predates Mimic, Europa, Quartet, Objekt and every
Player device — it will confidently tell you a device doesn't exist when it does.

Full background, including the three ways into Reason and why two of them are the
wrong ones to build on: **`docs/reason/FINDINGS.md`. Read it before proposing
anything about controlling Reason.**

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

Not every entry in a factory map is a parameter — the same column also holds text
constants (`"Thresh"`), numeric constants and mapping-variation assignments
(`Group=3`, `Shift=ShiftDown`), which drive the *surface's* display rather than the
rack. The parser filters them and `tests/test_reason_vocab.py` pins that; if you
loosen the filter, that test is what tells you.

## Behaviour — `tools/reason_docs.py`

Extracts Reason's Help Files to `reason_docs/` (325 topics, one `.md` each, plus
`INDEX.md`). **Gitignored on purpose** — it is the owner's licensed manual and stays
on his machine.

```bash
python3 tools/reason_docs.py
```

The `.pdf` manuals in the same folder are deliberately skipped: the Help Files are
the same manual in a form that parses cleanly. Don't fight the 78 MB PDF.

## When new documentation arrives

More is expected. The routine:

1. Note where it came from and **what version of Reason it describes** — that is the
   single most important fact about any Reason document here, and the easiest to
   lose.
2. If it's a folder of HTML/text, point `tools/reason_docs.py` at it rather than
   reading it by hand.
3. If it changes a conclusion in `docs/reason/FINDINGS.md`, edit that file. It exists
   so nobody re-derives this, and it is only useful if it stays true.

## Related

- `reason-remote-bridge` — the codec/map files themselves, and how to add a knob.
- `device_refs/*.md` — plain-language guides the app reads aloud. Original wording,
  in the repo; the extracted `reason_docs/` is raw source, not a substitute.
