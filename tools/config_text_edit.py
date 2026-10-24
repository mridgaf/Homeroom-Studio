"""Edit identity configs as TEXT (dj-rebuild Code passes, 2026-10-24).

The config files each have their own indent, so json load/dump rewrites the
whole file. These helpers replace one key's value and leave every other byte
alone. Usage from a Code pass:

    import sys; sys.path.insert(0, "tools")
    from config_text_edit import set_path, add_after, del_path, original_odds
    s = open("genres_config.json").read()
    s = set_path(s, ["Horror Rap", "signature", "tempo"], [70, 102])
    open("genres_config.json", "w").write(s)

Then JSON-compare against the backup: only the identity you meant changed.
"""
import json

_D = json.JSONDecoder()


def _ws(s, i):
    while s[i] in " \t\r\n":
        i += 1
    return i


def members(s, o):
    """[(key, key_start, val_start, val_end)] of the object whose '{' is at o."""
    out, i = [], _ws(s, o + 1)
    if s[i] == "}":
        return out
    while True:
        k, ke = _D.raw_decode(s, i)
        j = _ws(s, ke)
        assert s[j] == ":"
        vs = _ws(s, j + 1)
        _, ve = _D.raw_decode(s, vs)
        out.append((k, i, vs, ve))
        j = _ws(s, ve)
        if s[j] == "}":
            return out
        assert s[j] == ","
        i = _ws(s, j + 1)


def _find(s, path):
    o = _ws(s, 0)
    for n, key in enumerate(path):
        m = {k: (ks, vs, ve) for k, ks, vs, ve in members(s, o)}
        if key not in m:
            raise KeyError(path[:n + 1])
        ks, vs, ve = m[key]
        if n == len(path) - 1:
            return ks, vs, ve, o
        o = vs


def _indent(s, pos):
    ls = s.rfind("\n", 0, pos) + 1
    return s[ls:pos]


def _dump(value, ind, step):
    txt = json.dumps(value, indent=len(step), ensure_ascii=False)
    return txt.replace("\n", "\n" + ind)


def set_path(s, path, value, step=" "):
    """Replace the value at `path` (a list of object keys)."""
    ks, vs, ve, _ = _find(s, path)
    return s[:vs] + _dump(value, _indent(s, ks), step) + s[ve:]


def add_after(s, path, after, key, value, step=" "):
    """Insert "key": value into the object at `path`, right after `after`."""
    ks, vs, ve, _ = _find(s, path + [after])
    ind = _indent(s, ks)
    return (s[:ve] + ",\n" + ind + json.dumps(key) + ": "
            + _dump(value, ind, step) + s[ve:])


def del_path(s, path):
    """Remove the key at `path` (and its comma)."""
    ks, vs, ve, o = _find(s, path)
    mem = members(s, o)
    idx = [m[1] for m in mem].index(ks)
    if idx > 0:
        return s[:mem[idx - 1][3]] + s[ve:]
    nxt = mem[1][1] if len(mem) > 1 else None
    return s[:ks] + s[nxt:] if nxt else s[:_ws(s, o + 1)] + s[ve:]


def original_odds(cs, research=None):
    """Original-side chord_source (owner 2026-10-24): midi 75, loop 10, sound
    packs 15 split by the research ratios. `research` = {instrument: weight};
    instruments it leaves out go to 0. None keeps today's ratios. Entry order
    and zero entries are kept; "loop" is added if missing."""
    rows = [list(r) for r in cs]
    names = [r[0] for r in rows]
    if research is not None:
        for k in research:
            assert k in names, k
        for r in rows:
            if r[0] not in ("midi", "loop"):
                r[1] = research.get(r[0], 0)
    inst = sum(r[1] for r in rows if r[0] not in ("midi", "loop"))
    for r in rows:
        if r[0] == "midi":
            r[1] = 75
        elif r[0] == "loop":
            r[1] = 10
        elif r[1]:
            r[1] = round(r[1] * 15.0 / inst, 3)
    if "loop" not in names:
        rows.insert(names.index("midi"), ["loop", 10])
    return rows


if __name__ == "__main__":
    t = '{\n "A": {\n  "x": 1,\n  "y": [1, 2]\n },\n "B": 2\n}'
    u = set_path(t, ["A", "x"], 5)
    assert json.loads(u)["A"]["x"] == 5 and u.endswith('"B": 2\n}')
    u = add_after(u, ["A"], "x", "z", {"k": 1})
    assert json.loads(u)["A"]["z"] == {"k": 1}
    u = del_path(u, ["A", "y"])
    assert "y" not in json.loads(u)["A"]
    o = dict(original_odds([["piano", 1], ["bell", 1], ["midi", 2]],
                           {"piano": 1}))
    assert o == {"piano": 15.0, "bell": 0, "loop": 10, "midi": 75}
    print("ok")
