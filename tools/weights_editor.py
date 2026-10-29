"""See and edit every weighted roll in the DJ / Legend / genre configs.

A "weight" is a number that sets how often one option is picked relative to
its siblings (progressions, chord sources, hat modes, keys...). The engine
only uses the ratios, so [3, 1] and [75, 25] are the same roll.

Reads the three configs, finds every weighted group, and saves one group at
a time as a TEXT edit (config_text_edit), so nothing else in the file moves.
A dated pre-weights backup is made the first time a file is edited each day.
"""
import json
import shutil
from datetime import date
from pathlib import Path

from config_text_edit import set_path

ROOT = Path(__file__).resolve().parent.parent
FILES = {"DJs": "crew_config.json", "Genres": "genres_config.json",
         "Legends": "legends_config.json"}
# dict-of-number groups that ARE weights (the other number dicts are dB/Hz
# settings, not odds)
WEIGHT_DICTS = {"pattern_tags"}


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _pairs(v):
    return (isinstance(v, list) and len(v) >= 2 and all(
        isinstance(p, list) and len(p) == 2 and isinstance(p[0], str)
        and _num(p[1]) for p in v))


def _groups(v, path):
    """Yield (path, kind, items) for each weighted group under `v`."""
    if _pairs(v):
        yield path, "pairs", v
    elif isinstance(v, dict):
        if path and path[-1] in WEIGHT_DICTS and v and all(
                _num(x) for x in v.values()):
            yield path, "dict", [[k, x] for k, x in v.items()]
            return
        for k, x in v.items():
            if k.startswith("_"):
                continue
            yield from _groups(x, path + [k])
    elif (path and path[-1] == "w" and isinstance(v, list) and v
          and all(_num(x) for x in v)):
        yield path, "array", [["step %d" % (i + 1), x]
                              for i, x in enumerate(v)]


def collect(root=ROOT):
    out = {}
    for label, fn in FILES.items():
        d = json.load(open(Path(root) / fn))
        ids = []
        for name, spec in d.items():
            if not (isinstance(spec, dict) and "kit" in spec):
                continue
            gs = [{"path": p, "kind": k, "items": it}
                  for p, k, it in _groups(spec, [])]
            ids.append({"name": name, "listen": spec.get("listen", ""),
                        "groups": gs})
        out[label] = {"file": fn, "ids": ids}
    return out


def save(label, name, path, items, root=ROOT):
    """Write `items` ([[option, weight], ...]) to one group. Option names and
    order must match the group's current ones (no renaming here)."""
    f = Path(root) / FILES[label]
    s = f.read_text()
    cur = {tuple(p): (k, it) for p, k, it in _groups(json.loads(s)[name], [])}
    if tuple(path) not in cur:
        raise ValueError("no such weight group")
    kind, old = cur[tuple(path)]
    if [i[0] for i in items] != [i[0] for i in old]:
        raise ValueError("option names changed")
    ws = [i[1] for i in items]
    if not all(_num(w) and w >= 0 for w in ws) or not any(w > 0 for w in ws):
        raise ValueError("weights must be numbers >= 0, not all zero")
    ws = [round(float(w), 4) for w in ws]
    if kind == "pairs":
        val = [[i[0], w] for i, w in zip(items, ws)]
    elif kind == "dict":
        val = {i[0]: w for i, w in zip(items, ws)}
    else:
        val = ws
    bak = f.with_name(f.stem + ".pre-weights-%s.json" % date.today())
    if not bak.exists():
        shutil.copy2(f, bak)
    f.write_text(set_path(s, [name] + list(path), val))
    return True
