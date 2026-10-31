"""Your ear is the judge (Plan C, owner 2026-10-31).

Reads the recipes of every beat in Favorites and Trash and scores each
sample FOLDER (pack + role folder, e.g. ".../PHONK KIT VOL. 5/Kicks") by
how often it shows up in kept vs thrown-out beats. New beats then pick from
liked folders more often and from disliked ones less often -- a lean, never
a ban: every sample stays reachable.

Folders, not files: most samples were used only once, so a file says
nothing; a folder used across several beats does.
"""
from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path

FAV_DIR, TRASH_DIR = "Favorites", "Trash"
MAX_LEAN = 3.0        # a loved folder is picked up to 3x as often, a hated 1/3
PRIOR = 4.0           # beats of evidence before a folder's lean gets strong
_cache = {}


def _beat_numbers(folder):
    try:
        names = os.listdir(folder)
    except OSError:
        return []
    return sorted({int(m.group(1)) for f in names
                   if (m := re.match(r"(\d+) ", f))})


def _folders(root, sub):
    c = Counter()
    for no in _beat_numbers(Path(root) / sub):
        try:
            rec = json.loads((Path(root) / ".recipes" / f"{no}.json")
                             .read_text())
        except (OSError, ValueError):
            continue
        # one vote per folder per beat
        c.update({str(Path(p).parent) for p in
                  (rec.get("kit_paths") or {}).values()
                  if isinstance(p, str)})
    return c


def score(fav, trash, n_fav, n_trash):
    """-1..1 per folder: Trash counts are scaled up to Favorites' size so a
    smaller Trash pile still weighs the same."""
    k = n_fav / max(n_trash, 1)
    out = {}
    for f in set(fav) | set(trash):
        a, b = fav.get(f, 0), trash.get(f, 0) * k
        out[f] = (a - b) / (a + b + PRIOR)
    return out


def weights(root):
    """{folder: pick weight}, rebuilt whenever Favorites or Trash change."""
    key = []
    for sub in (FAV_DIR, TRASH_DIR):
        try:
            key.append(os.stat(Path(root) / sub).st_mtime)
        except OSError:
            key.append(None)
    hit = _cache.get(str(root))
    if hit and hit[0] == key:
        return hit[1]
    fav, trash = _folders(root, FAV_DIR), _folders(root, TRASH_DIR)
    s = score(fav, trash, len(_beat_numbers(Path(root) / FAV_DIR)),
              len(_beat_numbers(Path(root) / TRASH_DIR)))
    w = {f: MAX_LEAN ** v for f, v in s.items()}
    _cache[str(root)] = (key, w)
    return w


def lean_order(cands, w, rng):
    """`cands` in a random order that favours heavier folders (weighted
    shuffle: key = u ** (1/weight), largest first)."""
    keys = [rng.random() ** (1.0 / w.get(str(Path(e["path"]).parent), 1.0))
            for e in cands]
    return [cands[i] for i in sorted(range(len(cands)),
                                     key=lambda i: -keys[i])]


if __name__ == "__main__":
    import numpy as np
    s = score({"A": 6}, {"B": 2}, 189, 69)
    assert s["A"] > 0.5 and s["B"] < -0.5
    w = {"/x/A": MAX_LEAN, "/x/B": 1 / MAX_LEAN}
    cands = [{"path": "/x/A/k.wav"}, {"path": "/x/B/k.wav"}]
    firsts = Counter(lean_order(cands, w, np.random.default_rng(i))[0]
                     ["path"] for i in range(2000))
    assert firsts["/x/A/k.wav"] > 1600, firsts       # ~90% with 3 vs 1/3
    print("ok")
