#!/usr/bin/env python3
"""RETIRED 2026-09-10 — DO NOT RUN. This project is Reason 12 only.

This script extracts the **Reason 7 (2013)** Help Files. Its output was retired to
`_retired_reason7_2026-09-10/reason_docs/` because Reason 7 material is out of scope:
the behaviour source is now the Reason 12.7 Operation Manual, extracted to
`~/.reason_voice/reason12_manual/`. See `docs/reason/FINDINGS.md` and the
`reason-reference` skill.

Running this would silently recreate a stale `reason_docs/` alongside the current
manual, which is the exact confusion the retirement removed. The guard below stops
that; override only if you deliberately need the 2013 text for historical comparison.

Original notes follow.

Extract Reason's Help Files into plain text for local reference / Hermes.

    python3 tools/reason_docs.py

Writes one .md per help topic into reason_docs/ (gitignored -- this is the
owner's licensed documentation; it stays on his machine).

Two things worth knowing before you trust the output:

* These are the **Reason 7** (2013) help files, from /Applications/Reason. Reason
  12 ships no local manual. They explain what each knob DOES, which hasn't
  changed for the classic devices -- but they predate Mimic, Europa, Quartet and
  every Player device. For what a parameter is CALLED in Reason 12, use
  tools/reason_vocab.py instead. See docs/reason/FINDINGS.md.
* Only `Operation Manual.pdf` is redundant with the Help Files, and it alone is
  skipped deliberately (78 MB, same content, and the Help Files parse cleanly).
  The other three PDFs in that folder -- MIDI Implementation Chart, Key
  Commands, Installation Manual -- are SEPARATE documents with no Help-File
  equivalent, so they are simply not covered here. Read them directly. The MIDI
  Implementation Chart is the CC-number table, and nothing in reason_docs/
  contains it.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

HELP = Path("/Applications/Reason/Documentation/Help Files/English")
OUT = Path(__file__).parent.parent / "reason_docs"

DROP = re.compile(r"(?s)<script.*?</script>|<head.*?</head>|<!--.*?-->")
TAG = re.compile(r"<[^>]+>")


def titles() -> dict[str, str]:
    """Topic titles from the help system's own index (wwhdata/common/files.js)."""
    js = HELP / "wwhdata/common/files.js"
    if not js.exists():
        return {}
    pairs = re.findall(r'P\.fA\("((?:[^"\\]|\\.)*)","([^"]+)"\)',
                       js.read_text(encoding="utf-8", errors="replace"))
    return {f: html.unescape(t).encode().decode("unicode_escape")
            for t, f in pairs}


def to_text(path: Path) -> str:
    raw = DROP.sub("", path.read_text(encoding="utf-8", errors="replace"))
    text = html.unescape(TAG.sub(" ", raw))
    text = re.sub(r"[ \t]+", " ", text)
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    if not HELP.exists():
        raise SystemExit(f"Help Files not found at {HELP}")

    args.out.mkdir(parents=True, exist_ok=True)
    index, name_of = [], titles()
    for src in sorted(HELP.glob("*.html")):
        body = to_text(src)
        if len(body) < 200:            # nav stubs and frame shells
            continue
        title = name_of.get(src.name, src.stem)
        dest = args.out / (src.stem.replace(" ", "_") + ".md")
        dest.write_text(f"# {title}\n\n_Reason 7 help file: {src.name}_\n\n{body}\n",
                        encoding="utf-8")
        index.append(f"- [{title}]({dest.name})")

    (args.out / "INDEX.md").write_text(
        "# Reason help files (extracted)\n\n"
        "Reason 7 (2013) documentation, extracted by `tools/reason_docs.py`.\n"
        "Explains what controls do. For Reason 12 parameter NAMES use\n"
        "`docs/reason/remote-vocab.json`.\n\n" + "\n".join(sorted(index)) + "\n",
        encoding="utf-8")
    print(f"{len(index)} topics -> {args.out}")



def _retired_guard() -> None:
    """Stop an accidental regeneration of the retired Reason 7 docs."""
    import os
    if os.environ.get("REASON7_HISTORICAL") == "1":
        return
    raise SystemExit(
        "reason_docs.py is RETIRED. This project is Reason 12 only.\n"
        "The Reason 7 (2013) output was moved to _retired_reason7_2026-09-10/.\n"
        "Current behaviour source: ~/.reason_voice/reason12_manual/ (Reason 12.7 manual).\n"
        "If you genuinely need the 2013 text for historical comparison:\n"
        "    REASON7_HISTORICAL=1 python3 tools/reason_docs.py"
    )

if __name__ == "__main__":
    _retired_guard()
    main()
