"""Loops-side vocabulary and finish (owner rulings 2026-10-24 — read
Handoffs/Loops Settings Build.md and its DECISIONS.md entry before changing
anything here; every word list lives in loops_config.json, not in code).

  steering  an identity's listen line + library tags (+ its loops_config
            "words") -> word groups; a loop whose title/folders hit the
            same groups scores closer (sample_library.loops_scored)
  lead      lead loops typed keys/guitar/strings/horns/synth-arp by title
            words; no word = "other", steered by its folder style words
  finish    mood groups move the mix EQ and glue ONLY (crew.render_crew_beat,
            loop beats only); loop beats are always fully clean
"""
from __future__ import annotations

import json
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "loops_config.json"


@lru_cache(maxsize=1)
def _cfg():
    return json.loads(CONFIG.read_text())


def _split(s):
    return [w for w in re.split(r"[^a-z0-9]+", str(s).lower()) if w]


@lru_cache(maxsize=1)
def word_groups():
    """word -> group. Existing flavor families first, the texture words
    joining them, then the loop groups, which win a shared word."""
    from flavor_tags import SYNONYM_GROUPS
    out = {w: g for g, ws in SYNONYM_GROUPS.items() for w in ws}
    out.update(_cfg()["_texture"])
    out.update({w: g for g, ws in _cfg()["_groups"].items() for w in ws})
    return out


def lead_types(tokens):
    toks = {t.lower() for t in tokens}
    return [t for t, ws in _cfg()["_lead_types"].items() if toks & set(ws)] \
        or ["other"]


def groups_of(words):
    """Every group and lead type ("type:keys") these words reach. "other"
    is never a want: an untyped loop is steered by its style words."""
    words = {w.lower() for w in words}
    wg = word_groups()
    return ({wg[w] for w in words if w in wg}
            | {"type:" + t for t in lead_types(words) if t != "other"})


def identity_words(name, preset=None):
    """The words that steer this identity's loops: its listen line, its
    library tags and any loops_config "words"."""
    from crew import CREW
    own = CREW.get(name) or {}
    p = preset or {}
    title_only = set(_cfg()["_title_only"])
    words = [w for w in _split(p.get("listen") or own.get("listen") or "")
             if w not in title_only]
    lib = p.get("library") or own.get("library") or {}
    words += [w for t, _w in lib.get("tags", []) for w in _split(t)]
    words += [w.lower() for w in (_cfg().get(name) or {}).get("words", [])]
    return words


def finish(words, eq, glue):
    """(eq, glue) for a loop beat from the identity's words. ONE mood row
    (owner 2026-10-24): the group with the most distinct matching words,
    a tie to the one reached first. Its dB adds to the identity's own mix
    EQ; its glue word sets the ratio unless the identity names its own."""
    fin, wg = _cfg()["_finish"], word_groups()
    hits = Counter(wg[w] for w in dict.fromkeys(w.lower() for w in words)
                   if wg.get(w) in fin)
    eq, glue = dict(eq or {}), dict(glue or {})
    if not hits:
        return eq, glue
    row = fin[hits.most_common(1)[0][0]]           # ties keep first-seen
    for band in ("low_db", "mid_db", "high_db"):
        if row.get(band):
            eq[band] = eq.get(band, 0.0) + row[band]
    if row.get("glue") and "ratio" not in glue:
        glue["ratio"] = _cfg()["_glue"][row["glue"]]
    return eq, glue


if __name__ == "__main__":
    assert word_groups()["boom"] == "hip hop"            # not the 808 family
    assert word_groups()["swing"] == "jazz"
    assert word_groups()["dirty"] == "grit"
    assert lead_types(["melody", "1"]) == ["other"]
    assert lead_types(["rhodes", "chords"]) == ["keys"]
    assert "type:keys" in groups_of(["piano"])
    eq, glue = finish(["dark", "lofi", "creepy"], {"high_db": 2.0}, {})
    assert eq == {"high_db": 0.0, "low_db": 2.0}     # dark/horror: 2 words
    assert glue == {"ratio": 2.2}
    assert finish(["lofi", "dark"], {}, {})[1] == {"ratio": 1.6}  # tie: first
    assert finish(["jazz"], {}, {"ratio": 4.0})[1] == {"ratio": 4.0}
    print("self-check ok")
