"""The pattern sheet: a plain-text picture of what every lane is
playing, saved beside each beat (owner request 2026-07-22 — "so I can
visually know what's going on and see what I don't like").

The WAV tells you it's wrong; this tells you WHY. Every lane is one row
on a shared grid, the backbeat is called out explicitly, and the beat's
whole setup (length, meter, swing, duck, key) sits at the top — so a
beat you don't like can be diagnosed without opening Reason or reading
a recipe.

Legend, matching the engine's own notation:
    X  accent      x  normal      o  open hat     .  ghost
    -  rest        |  start of a beat (quarter note)
"""
from __future__ import annotations

# lanes worth showing first, in the order a drummer would read them
ORDER = ("kick", "sub", "bass", "snare", "clap", "snap", "rim", "hat",
         "perc", "bongo", "stamp")
BACKBEAT_LANES = ("snare", "clap")


def _rank(lane):
    base = lane.rstrip("0123456789")
    for i, name in enumerate(ORDER):
        if base == name:
            return (i, lane)
    return (len(ORDER), lane)          # guests and colors after the kit


def _ruler(steps, per_beat):
    """A counting row: 1 . . . 2 . . . — where the beats fall."""
    out = []
    for i in range(steps):
        if per_beat and i % per_beat == 0:
            out.append(str(i // per_beat + 1)[-1])
        else:
            out.append(".")
    return "".join(out)


def _grid(bar, per_beat):
    """One bar with a | at each beat boundary, so the eye can count."""
    if not per_beat:
        return bar
    return "".join(("|" + c) if i and i % per_beat == 0 else c
                   for i, c in enumerate(bar))


def _expand(bar, steps):
    """Stretch a bar onto a finer shared grid. Lanes don't all run at
    the same resolution — a 16th-grid kick under a 32nd-grid hat roll —
    and printing them at their own widths made the columns disagree, so
    nothing lined up vertically. Every row is drawn on the finest grid
    in the beat; the in-between slots are genuinely silent, so they
    print as rests."""
    if not bar or steps % len(bar):
        return bar
    factor = steps // len(bar)
    if factor == 1:
        return bar
    return "".join(c + "-" * (factor - 1) for c in bar)


def sheet(preset, title="", extra=None):
    """The full text sheet for one beat. `extra` is a list of plain-words
    lines (the README's "this one:" notes) shown under the header."""
    lanes = preset.get("lanes") or {}
    bpm = preset.get("bpm", 0)
    num, den = tuple(preset.get("tsig", (4, 4)))
    nbars = int(preset.get("bars") or 8)

    body = [t for t in (title,) if t]
    head = "%d BPM | %d/%d | %d bars" % (bpm, num, den, nbars)
    swings = sorted({s[2][2] for k, s in lanes.items()
                     if not k.startswith("stamp")})
    if swings:
        head += " | swing %s" % ("/".join(str(int(s)) for s in swings))
    # "fully quantized" means dead on the grid — no shuffle AND no
    # human drag/wobble. Reporting it while swing was still 52 (which
    # the first draft did) is a contradiction, not a description.
    quantized = swings == [50] and all(
        s[2][0] == 0 and s[2][1] == 0
        for k, s in lanes.items() if not k.startswith("stamp"))
    if quantized:
        head += " (fully quantized)"
    duck = preset.get("sidechain") or 0
    head += " | kick duck %s" % ("%.0f%%" % (100 * duck) if duck else "off")
    body.append(head)
    for line in (extra or []):
        body.append("  " + line)
    body.append("")

    rows = sorted(lanes, key=_rank)
    width = max([len(r) for r in rows] + [8])
    # every row is drawn on the FINEST grid any lane uses, so the
    # columns actually line up under each other
    steps = max((len(b) for s in lanes.values() for b in s[3] if b),
                default=16)
    per_beat = steps // num if num and steps % num == 0 else 0

    for b in range(nbars):
        body.append("bar %d" % (b + 1))
        body.append("  %-*s  %s" % (width, "", _grid(_ruler(steps, per_beat),
                                                     per_beat)))
        for lane in rows:
            bars = lanes[lane][3]
            if not bars:
                continue
            bar = _expand(bars[b % len(bars)], steps)
            mark = " <- backbeat" if lane.rstrip("0123456789") \
                in BACKBEAT_LANES else ""
            body.append("  %-*s  %s%s" % (width, lane, _grid(bar, per_beat),
                                          mark))
        body.append("")

    body.append("X accent   x normal   o open   . ghost   - rest")
    return "\n".join(body) + "\n"


def write_sheet(path, preset, title="", extra=None):
    """Save the sheet next to the beat. Never raises — a picture failing
    to write must not lose you a render."""
    try:
        from pathlib import Path
        Path(path).write_text(sheet(preset, title, extra))
        return path
    except (OSError, AttributeError, KeyError, TypeError, ValueError,
            IndexError):
        return None
