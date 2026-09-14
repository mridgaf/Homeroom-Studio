"""How free the DJs really are: a no-audio report on the 70/30 rule.

Owner 2026-09-14: "all djs have all instruments, chords and keys available
to them. keep djs 70% true to character weights, 70% of the time. the rest
is free for all" — drum sounds, patterns and backbeats included, and one
low sound per beat. This runs the engine's OWN decision functions (the
composer, the low-sound call, the voice order, the key roll, the chord
rhythm figures) over a spread of seeds for every DJ and counts what they
chose. Nothing is rendered and nothing is written: the pattern history is
pointed at a throwaway file for the run.

    ./.venv/bin/python tools/freedom_report.py          # 40 beats per DJ
"""
import collections
import random
import sys
import tempfile
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import beat_machine as bm                                   # noqa: E402
import chord_rhythm                                         # noqa: E402
import harmony                                              # noqa: E402
import crew                                                 # noqa: E402
import pattern_gen                                          # noqa: E402


def _line(title, counter, total):
    parts = ", ".join("%s %d%%" % (k, round(100.0 * v / total))
                      for k, v in counter.most_common())
    print("  %-22s %s" % (title, parts))


def main(per_dj=40):
    pattern_gen.PAT_HIST = Path(tempfile.mkdtemp()) / "pattern_history.json"
    djs = sorted(n for n in crew.CREW if crew.is_dj(n))
    C = collections.Counter
    free_n, low, lead, roots, progs, figs, parts = (
        C(), {True: C(), False: C()}, C(), C(), C(), C(), C())
    beats = 0
    for name in djs:
        for i in range(per_dj):
            v = 2 + (crew.CREW[name]["num"] * 7919 + i * 104729) % 9998
            free = pattern_gen.free_beat(v)
            dirs = bm.parse_directions("")
            p, notes = bm.solo_preset(name, v, None, dirs=dirs)
            sig = p.get("signature") or {}
            if not dirs["chords"] and sig.get("chords_default"):
                dirs = dict(dirs, chords=True)
            beats += 1
            free_n[free] += 1
            low[free][str(bm._low_voice(p, v, dirs, False, name,
                                        {"bass": [1]}))] += 1
            lead[bm._source_order(sig.get("chord_source"),
                                  random.Random(v * 461), free=free)[0]] += 1
            root, _mode, prog = bm._roll_key(sig, v, dirs, free,
                                             random.Random(v * 353 + 17))
            roots[root] += 1
            progs[prog or "(random)"] += 1
            spec = chord_rhythm.spec_for(p, free=free)
            for slot in range(4):
                figs[chord_rhythm.gen_figure(
                    spec, random.Random(v * 31 + slot), 1)[0]] += 1
            if notes and notes[0].startswith("free beat, drums:"):
                for part in notes[0].split(":", 1)[1].split(","):
                    parts[part.split(" from ")[0].strip()] += 1
    print("%d DJs x %d beats = %d beats\n" % (len(djs), per_dj, beats))
    print("  free beats             %d%%" % round(100.0 * free_n[True] / beats))
    _line("low sound, in char.", low[False], sum(low[False].values()))
    _line("low sound, free", low[True], sum(low[True].values()))
    _line("lead instrument", lead, beats)
    print("  keys used              %d of 12: %s" % (
        len(roots), ", ".join(sorted(roots))))
    print("  progressions used      %d of %d, most common: %s" % (
        len([p for p in progs if p != "(random)"]),
        len(harmony.PROGRESSIONS),
        ", ".join("%s %d%%" % (k, round(100.0 * n / beats))
                  for k, n in progs.most_common(3))))
    _line("chord figures", figs, sum(figs.values()))
    print("  drum parts borrowed    %s" % ", ".join(
        "%s %d" % kv for kv in parts.most_common()))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
