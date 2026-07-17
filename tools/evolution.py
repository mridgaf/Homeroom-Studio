"""Engine-driven evolution (owner decision 2026-07-17: the engine itself
picks each DJ's one deliberate change, with rollback when his ears say no).

The 2026-07-15 rule stands — "we'll have them evolve as we go", one
deliberate change per featured character per batch, timing DNA (LaneFeel,
swing) and stamps untouchable. What changes: the ENGINE now owns the
picking. The first time a DJ is featured on a given day, one change from
the curated menu below lands in crew_config.json, is journaled with its
exact before/after delta, and shows up in the README so he knows what to
listen for. If a change sours a DJ, one command puts it back:

    ./.venv/bin/python tools/evolution.py --rollback "Otto Grit"
    ./.venv/bin/python tools/evolution.py --status
    ./.venv/bin/python tools/evolution.py --history "Otto Grit"

Guard rails:
- one change per DJ per calendar day, never the same op twice in a row;
- every op is BOUNDED (clamped zones, weight transfers, small steps) —
  a DJ can drift, never teleport;
- ops touch only taste keys (grammar weights, kick flavors/zones, guest
  palette, groove-library lean). LaneFeel offsets, swing, stamps, and
  bpm are not on the menu — the character always survives;
- the long-sustain-808 weight cap (<=0.2, owner rule 2026-07-17) is
  enforced after every flavor change;
- applying any evolution sets "_style_lock": true in the config so a
  future STYLE_VERSION re-sync can't silently erase the crew's careers.
  (Engine style upgrades then need a deliberate merge — that's correct:
  evolved DJs are no longer the factory presets.)

Journal: ~/.reason_voice/crew_journal.json — same file, same shape the
batches have always used, plus "op"/"delta"/"status" fields so entries
made here can be reverted precisely.
"""
import argparse
import copy
import json
import os
import random
import sys
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

JOURNAL = Path(os.path.expanduser("~/.reason_voice/crew_journal.json"))

# colors no DJ carries by default — the new_color op deals them out
GLOBAL_COLORS = [
    ["perc", ["cowbell", "bell"], "bells2"],
    ["rim", ["clave", "wood"], "claves"],
    ["perc", ["tabla", "udu"], "tablas"],
    ["fx", ["vocal", "chant", "hey", "yeah"], "voxchops"],
    ["perc", ["timbale", "tom"], "timbales"],
    ["fx", ["reverse", "swell"], "reversefx"],
]

LONG_808_CAP = 0.2       # owner rule 2026-07-17


# --------------------------------------------------------- path helpers


def _get(doc, path):
    cur = doc
    for k in path:
        cur = cur[k]
    return cur


def _set(doc, path, value):
    cur = doc
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value


def _delta(doc, path, new):
    """Set and record one change as [path, old, new] (JSON-safe)."""
    old = copy.deepcopy(_get(doc, path))
    _set(doc, path, new)
    return [list(path), old, new]


def _transfer(weights, i, j, amount):
    """Move weight from entry i to entry j; floors keep every mode alive."""
    take = min(amount, max(0.0, weights[i] - 0.05))
    return [round(w + take if k == j else (w - take if k == i else w), 3)
            for k, w in enumerate(weights)]


# ------------------------------------------------------------- the menu
# Each op: name -> (is_applicable(p), apply(p, name, rng) -> (deltas, note))
# p is the DJ's RAW config dict (JSON shapes: lists, not tuples).


def _op_kick_zone(p, name, rng):
    lo, hi = p["kit"]["kick"][3]
    f = rng.choice((0.8, 0.85, 1.18, 1.25))
    nlo = round(min(max(lo * f, 0.25), 1.8), 2)
    nhi = round(min(max(hi * f, nlo + 0.15), 2.4), 2)
    d = [_delta(p, ["kit", "kick", 3], [nlo, nhi])]
    word = "longer" if f > 1 else "shorter"
    return d, ("kick zone drifts %s (%.2f-%.2fs -> %.2f-%.2fs)"
               % (word, lo, hi, nlo, nhi))


def _op_flavor_lean(p, name, rng):
    fl = p["kick_flavors"]
    if len(fl) < 2:
        return None
    i, j = rng.sample(range(len(fl)), 2)
    ws = _transfer([f[0] for f in fl], i, j, rng.choice((0.08, 0.12)))
    # the long-808 cap survives every lean
    for k, f in enumerate(fl):
        secs = f[3]
        hi = secs[1] if isinstance(secs, list) else secs
        if f[1] == "808" and hi >= 1.2 and ws[k] > LONG_808_CAP:
            ws[k] = LONG_808_CAP
    d = [_delta(p, ["kick_flavors", k, 0], w) for k, w in enumerate(ws)
         if w != fl[k][0]]
    if not d:
        return None
    dest = "808s" if fl[j][1] == "808" else "clean/short kicks"
    return d, "kick taste leans toward %s" % dest


def _weighted_lane(p, lanes):
    return [(ln, spec) for ln, spec in p.get("grammar", {}).items()
            if ln in lanes and isinstance(spec, dict)
            and len(spec.get("modes", [])) >= 2]


def _op_timekeeper_mode(p, name, rng):
    cands = _weighted_lane(p, ("hat", "snap"))
    if not cands:
        return None
    ln, spec = rng.choice(cands)
    modes = spec["modes"]
    ws = [m[1] for m in modes]
    top = ws.index(max(ws))
    j = rng.choice([k for k in range(len(modes)) if k != top])
    nws = _transfer(ws, top, j, 0.12)
    d = [_delta(p, ["grammar", ln, "modes", k, 1], w)
         for k, w in enumerate(nws) if w != ws[k]]
    return d, ("%ss reach for '%s' more often" % (ln, modes[j][0]))


def _op_backbeat_mode(p, name, rng):
    cands = _weighted_lane(p, ("snare", "clap"))
    if not cands:
        return None
    ln, spec = rng.choice(cands)
    modes = spec["modes"]
    ws = [m[1] for m in modes]
    top = ws.index(max(ws))
    j = rng.choice([k for k in range(len(modes)) if k != top])
    nws = _transfer(ws, top, j, 0.1)
    d = [_delta(p, ["grammar", ln, "modes", k, 1], w)
         for k, w in enumerate(nws) if w != ws[k]]
    return d, ("the %s tries '%s' more often" % (ln, modes[j][0]))


def _op_ghosts(p, name, rng):
    for ln in ("snare", "clap"):
        spec = p.get("grammar", {}).get(ln)
        if spec and spec.get("gcells") and "ghosts" in spec:
            lo, hi = spec["ghosts"]
            step = rng.choice((-1, 1))
            nhi = min(max(hi + step, lo, 1), 4)
            if nhi == hi:
                return None
            d = [_delta(p, ["grammar", ln, "ghosts", 1], nhi)]
            word = "chattier" if nhi > hi else "quieter"
            return d, "ghost notes get %s (up to %d per bar)" % (word, nhi)
    return None


def _op_double_p(p, name, rng):
    spec = p.get("grammar", {}).get("kick")
    if not spec or "double_p" not in spec:
        return None
    old = spec["double_p"]
    new = round(min(max(old + rng.choice((-0.08, 0.08)), 0.05), 0.5), 2)
    if new == old:
        return None
    d = [_delta(p, ["grammar", "kick", "double_p"], new)]
    word = "stutters more" if new > old else "stutters less"
    return d, "the kick %s (double chance %.0f%%)" % (word, new * 100)


def _op_open_hats(p, name, rng):
    spec = p.get("grammar", {}).get("hat")
    if not spec or "open_p" not in spec:
        return None
    old = spec["open_p"]
    new = round(min(max(old + rng.choice((-0.05, 0.05)), 0.0), 0.3), 2)
    if new == old:
        return None
    d = [_delta(p, ["grammar", "hat", "open_p"], new)]
    word = "splash open more" if new > old else "stay closed more"
    return d, "hats %s" % word


def _op_guest_appetite(p, name, rng):
    ex = p.get("extras")
    if not ex:
        return None
    old = ex["p"]
    new = round(min(max(old + rng.choice((-0.12, 0.12)), 0.2), 0.85), 2)
    if new == old:
        return None
    d = [_delta(p, ["extras", "p"], new)]
    word = "invites guests more" if new > old else "keeps the room smaller"
    return d, "%s (guest chance %.0f%%)" % (word, new * 100)


def _op_new_color(p, name, rng):
    ex = p.get("extras")
    if not ex:
        return None
    have = {e[2] for e in ex["pool"]}
    cands = [c for c in GLOBAL_COLORS if c[2] not in have]
    if not cands:
        return None
    color = rng.choice(cands)
    pool = [list(e) for e in ex["pool"]] + [list(color)]
    d = [_delta(p, ["extras", "pool"], pool)]
    return d, "a new color joins the palette: %s" % color[2]


def _op_library_lean(p, name, rng):
    lib = p.get("library")
    if not lib:
        return None
    old = lib["p"]
    new = round(min(max(old + rng.choice((-0.1, 0.1)), 0.1), 0.55), 2)
    if new == old:
        return None
    d = [_delta(p, ["library", "p"], new)]
    word = ("digs the record crates more" if new > old
            else "trusts their own grammar more")
    return d, "%s (groove-seed chance %.0f%%)" % (word, new * 100)


def _op_genre_taste(p, name, rng):
    lib = p.get("library")
    if not lib or not lib.get("tags"):
        return None
    i = rng.randrange(len(lib["tags"]))
    tag, w = lib["tags"][i]
    nw = min(max(w + rng.choice((-1, 1)), 1), 5)
    if nw == w:
        return None
    d = [_delta(p, ["library", "tags", i, 1], nw)]
    word = "deeper into" if nw > w else "cooler on"
    return d, "digs %s %s records" % (word, tag)


MENU = [
    ("kick_zone", _op_kick_zone),
    ("flavor_lean", _op_flavor_lean),
    ("timekeeper_mode", _op_timekeeper_mode),
    ("backbeat_mode", _op_backbeat_mode),
    ("ghosts", _op_ghosts),
    ("double_p", _op_double_p),
    ("open_hats", _op_open_hats),
    ("guest_appetite", _op_guest_appetite),
    ("new_color", _op_new_color),
    ("library_lean", _op_library_lean),
    ("genre_taste", _op_genre_taste),
]


# ------------------------------------------------------------ the engine


def _load_journal():
    try:
        return json.loads(JOURNAL.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_journal(j):
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(j, indent=1))


def _config_path():
    import crew
    return crew.CONFIG


def _load_config():
    return json.loads(_config_path().read_text())


def _save_config(doc):
    doc["_style_lock"] = True        # evolved DJs outrank factory syncs
    _config_path().write_text(json.dumps(doc, indent=1))
    # refresh the loaded roster in place so this session's next beat
    # composes with the change (crew.CREW is shared by reference)
    import crew
    crew.CREW.clear()
    crew.CREW.update(crew.load_crew(_config_path()))


def evolved_today(name, journal=None):
    j = journal if journal is not None else _load_journal()
    today = str(date.today())
    return any(e.get("date") == today and e.get("op")
               for e in j.get(name, []))


def _last_op(name, journal):
    for e in reversed(journal.get(name, [])):
        if e.get("op") and e.get("status") != "rolled_back":
            return e["op"]
    return None


def evolve_one(name, journal=None, when=None):
    """Apply one menu change to `name` in crew_config.json. Returns the
    plain-words note, or None when nothing applied. Deterministic per
    (name, day)."""
    j = journal if journal is not None else _load_journal()
    when = when or str(date.today())
    rng = random.Random("%s|%s|evolve" % (name, when))
    doc = _load_config()
    if name not in doc:
        return None
    p = doc[name]
    avoid = _last_op(name, j)
    ops = [(op, fn) for op, fn in MENU if op != avoid]
    rng.shuffle(ops)
    for op, fn in ops:
        try:
            got = fn(p, name, rng)
        except (KeyError, IndexError, TypeError):
            got = None
        if not got:
            continue
        deltas, note = got
        _save_config(doc)
        j.setdefault(name, []).append({
            "date": when, "batch": "beat-machine-evolution",
            "change": note, "op": op, "delta": deltas, "status": "active"})
        _save_journal(j)
        return note
    return None


def maybe_evolve(names, status=lambda msg: None):
    """The per-batch hook: first time each featured DJ appears today,
    they evolve one step. Returns plain-words notes for the README.
    Never raises — evolution must not block a render."""
    notes = []
    try:
        j = _load_journal()
        for name in names:
            if evolved_today(name, j):
                continue
            note = evolve_one(name, journal=j)
            if note:
                status("%s evolves: %s" % (name, note))
                notes.append("%s evolution: %s" % (name, note))
    except Exception:
        pass
    return notes


def rollback(name):
    """Undo the newest active evolution for `name`. Returns the change
    that was reverted, or None."""
    j = _load_journal()
    entries = j.get(name, [])
    for e in reversed(entries):
        if e.get("op") and e.get("status") == "active":
            doc = _load_config()
            for path, old, _new in reversed(e["delta"]):
                try:
                    _set(doc[name], path, old)
                except (KeyError, IndexError, TypeError):
                    return None
            _save_config(doc)
            e["status"] = "rolled_back"
            entries.append({"date": str(date.today()),
                            "batch": "beat-machine-evolution",
                            "change": "rolled back: %s" % e["change"]})
            _save_journal(j)
            return e["change"]
    return None


# ------------------------------------------------------------------ CLI


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--status", action="store_true",
                    help="each DJ's current (active) evolutions")
    ap.add_argument("--history", default=None, help="one DJ's full journal")
    ap.add_argument("--rollback", default=None,
                    help="undo a DJ's newest active evolution")
    ap.add_argument("--evolve", default=None,
                    help="comma-separated DJs to evolve right now")
    a = ap.parse_args()
    from crew import CREW

    if a.rollback:
        change = rollback(a.rollback)
        print(("Rolled back for %s: %s" % (a.rollback, change)) if change
              else "Nothing active to roll back for %s." % a.rollback)
    elif a.history:
        for e in _load_journal().get(a.history, []):
            mark = {"active": "*", "rolled_back": "x"}.get(
                e.get("status"), " ")
            print(" %s %s  %s" % (mark, e.get("date", "?"), e["change"]))
    elif a.evolve:
        for name in [n.strip() for n in a.evolve.split(",")]:
            note = evolve_one(name)
            print("%s: %s" % (name, note or "(no change applied)"))
    else:
        j = _load_journal()
        for name in sorted(CREW, key=lambda n: CREW[n]["num"]):
            active = [e for e in j.get(name, [])
                      if e.get("op") and e.get("status") == "active"]
            if active:
                print("%-15s %d active evolution(s); newest: %s (%s)"
                      % (name, len(active), active[-1]["change"],
                         active[-1]["date"]))
            else:
                print("%-15s at baseline" % name)


if __name__ == "__main__":
    main()
