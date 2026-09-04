"""A/B audition: the root 808 on chord beats, and the rebuild key lock.

The two sound changes the 2026-09-03 handoff still owed him. Both were
found on never-guess-hooks, both were deliberately left out of the
chunk/FX restore because he had not heard them, and both live behind an
off-by-default flag in beat_machine until he does.

FOLDER 1 — the root 808 (beat_machine.ROOT_808_WITH_CHORDS)

  His rule from 2026-07-18 is "add the root": a traditional beat gets a
  tuned 808 sub on a musical root under the kick. The code skipped that
  whenever the beat had chords, because back then a chords beat had
  harmony's own moving bass underneath and two basses would fight. That
  bass was retired 2026-07-29 (bass_idx is permanently None) and every
  identity has since gained chords_default — so the skip quietly took
  the rule off the table.

  Measured on his own library, not argued: 150 traditional beats carry
  chords, and NOT ONE of them got a sub. The only 9 beats that ever had
  both are dated 2026-09-01, the day the branch was live, and all 9 took
  the beat's own key.

    a Now       today's sound: chords, no sub.
    b Root 808  the same beat with the sub, tuned to its own key.

FOLDER 2 — the rebuild key lock (beat_machine.REBUILD_LOCKS_KEY)

  When he rebuilds a beat (swaps a hat, trims a level), the chords are
  regenerated. Today the rebuild re-rolls the key and the progression
  instead of reading them off the recipe. That is deterministic from the
  saved variant, so on an ORDINARY beat it lands on the same answer and
  there is nothing to hear — 0 of the 118 September beats on his drive
  come back different.

  It breaks in exactly the two places he sets the key on purpose. This
  folder is the first of them, the loud one: a beat whose key came off a
  REFERENCE TRACK.

    a As printed     the beat as the reference track made it (F minor).
    b Rebuild now    what today's code hands back after a hat swap.
    c Rebuild locked what the fix hands back.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3
is never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_root_808_ab.py
Out:  ~/Desktop/Homeroom Root 808 and Locks <today>/
"""
import json
import os
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, write_wav24
from make_drum_beats import build_shots
from crew import CREW, build_kit, lock_stamps, normalize_preset, render_crew_beat
from pattern_gen import compose
import beat_machine as bm

DESK = Path(os.path.expanduser(
    f"~/Desktop/Homeroom Root 808 and Locks {date.today()}"))
F1 = "1 Root 808"
F2 = "2 Rebuild key lock"

# Three he has tuned recently and knows the sound of. None of them rolls a
# long sustained 808 kick, which is the one case the rule skips on purpose
# (that sample is already carrying the sub; two would fight).
ROOT_DJS = ["Otto Grit", "Cutz", "Crate Prophet"]
LOCK_DJ = "Otto Grit"
REF_KEY = ("F", "minor")        # what a reference track pinned
CHORDS = {"chords": True, "chord_feel": None}


def band_db(L, R, lo=0.0, hi=SR / 2):
    """ABSOLUTE energy in a band of the FINISHED file — measured where the
    sound comes out, not on the buffer the change was applied to."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def compose_one(name, v):
    q = json.loads(json.dumps(CREW[name]))
    compose(q, name, v)
    bm.vary_preset(q, v, CREW[name]["num"], tempo_locked=True)
    return normalize_preset(q)


def render(name, p, shots, stamps, avoid, v, dirs, sub_from=None):
    """One version. Returns (L, R, lufs, harmony, sub_note)."""
    kit, sources = build_kit(shots, name, stamps[name][1], variant=v,
                             avoid=set(avoid), preset=p)
    vnotes = []
    _midi, harm = bm._build_chords(p, kit, sources, v, dict(dirs), vnotes)
    note = None
    if sub_from is not None:
        note = bm._add_root_sub(p, kit, sources, v, vnotes,
                                harmony_info=harm if sub_from else None,
                                traditional=True)
    L, R, lufs = render_crew_beat(name, kit, preset=p)
    return L, R, lufs, (harm or {}), note


def key_of(h):
    return "%s %s / %s" % (h.get("root"), h.get("mode"), h.get("progression"))


def root_808_folder(scratch, shots, stamps, avoid, rows, warn):
    """a Now vs b Root 808, on beats that HAVE chords."""
    out = []
    for name in ROOT_DJS:
        picked = None
        for v in range(2, 80):
            p = compose_one(name, v)
            L, R, lufs, harm, note = render(name, p, shots, stamps, avoid, v,
                                            CHORDS, sub_from=True)
            if note and harm.get("root"):
                picked = (v, p, L, R, lufs, harm, note)
                break
        if not picked:
            warn.append(f"{name}: no variant in 2..80 fired the root 808")
            continue
        v, p, Lb, Rb, lufb, harm, note = picked
        pa = compose_one(name, v)
        La, Ra, lufa, harma, _ = render(name, pa, shots, stamps, avoid, v,
                                        CHORDS, sub_from=None)
        lo_a, lo_b = band_db(La, Ra, hi=100.0), band_db(Lb, Rb, hi=100.0)
        stem = f"{name} {p['bpm']}bpm {harm.get('key', '?')}"
        for tag, L, R, lu in (("a Now", La, Ra, lufa),
                              ("b Root 808", Lb, Rb, lufb)):
            fn = f"{stem} — {tag}.wav"
            write_wav24(scratch / F1 / fn, L, R)
            rows.append((F1, fn, lu))
        out.append((name, harm.get("key"), note, lo_a, lo_b,
                    float(np.abs(np.asarray(La)[:len(Lb)]
                                 - np.asarray(Lb)[:len(La)]).max())))
        print(f"  {name:15s} {harm.get('key', '?'):16s} sub={note:2s}  "
              f"low {lo_a:6.2f} -> {lo_b:6.2f} dB")
    return out


def lock_folder(scratch, shots, stamps, avoid, rows, warn):
    """a As printed (reference key) / b Rebuild now / c Rebuild locked."""
    out = []
    for v in range(2, 80):
        p = compose_one(LOCK_DJ, v)
        d_a = dict(CHORDS, force_key=REF_KEY)
        La, Ra, lua, ha, _ = render(LOCK_DJ, p, shots, stamps, avoid, v, d_a)
        if not ha.get("root"):
            continue
        Lb, Rb, lub, hb, _ = render(LOCK_DJ, compose_one(LOCK_DJ, v), shots,
                                    stamps, avoid, v, CHORDS)
        d_c = dict(CHORDS, force_key=REF_KEY,
                   chord_feel=ha.get("progression"))
        Lc, Rc, luc, hc, _ = render(LOCK_DJ, compose_one(LOCK_DJ, v), shots,
                                    stamps, avoid, v, d_c)
        if key_of(hb) == key_of(ha):
            continue            # this variant re-rolls to the same key
        stem = f"{LOCK_DJ} {p['bpm']}bpm"
        for tag, L, R, lu, h in (("a As printed", La, Ra, lua, ha),
                                 ("b Rebuild now", Lb, Rb, lub, hb),
                                 ("c Rebuild locked", Lc, Rc, luc, hc)):
            fn = f"{stem} — {tag} ({h.get('key', '?')}).wav"
            write_wav24(scratch / F2 / fn, L, R)
            rows.append((F2, fn, lu))
        out.append((key_of(ha), key_of(hb), key_of(hc)))
        print(f"  printed {key_of(ha)}\n  rebuild {key_of(hb)}"
              f"\n  locked  {key_of(hc)}")
        if len(out) == 2:
            break
    if not out:
        warn.append("lock folder: no variant drifted — nothing to hear")
    return out


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="root808-ab-"))
    (scratch / F1).mkdir()
    (scratch / F2).mkdir()
    rows, warn = [], []

    print("\nFolder 1 — the root 808 on chord beats:")
    root = root_808_folder(scratch, shots, stamps, avoid, rows, warn)
    print("\nFolder 2 — the rebuild key lock:")
    locks = lock_folder(scratch, shots, stamps, avoid, rows, warn)

    # ---- fail loud, BEFORE it reaches him -------------------------------
    for name, key, note, lo_a, lo_b, peakdiff in root:
        if peakdiff < 1e-6:
            warn.append(f"{name}: 'b Root 808' is IDENTICAL to 'a Now'")
        if lo_b - lo_a < 0.5:
            warn.append(f"{name}: the sub did not add low end "
                        f"({lo_b - lo_a:+.2f} dB under 100 Hz)")
        if note not in (key or "").split()[0:1]:
            warn.append(f"{name}: sub root {note} is not the beat's key {key}")
    for was, now, locked in locks:
        if now == was:
            warn.append("lock: 'b Rebuild now' matched the printed key")
        if locked != was:
            warn.append(f"lock: 'c Rebuild locked' came back {locked}, "
                        f"printed was {was}")

    if DESK.exists():
        shutil.rmtree(DESK)
    shutil.copytree(scratch, DESK)
    (DESK / "READ ME.txt").write_text(readme(rows, root, locks))
    shutil.rmtree(scratch)

    n1 = len(list((DESK / F1).glob("*.wav")))
    n2 = len(list((DESK / F2).glob("*.wav")))
    print(f"\n{n1} + {n2} files -> {DESK}")
    if n1 != 2 * len(root):
        warn.append(f"folder 1 has {n1} files, expected {2 * len(root)}")
    if n2 != 3 * len(locks):
        warn.append(f"folder 2 has {n2} files, expected {3 * len(locks)}")
    if warn:
        print("\nWARNING — do not ship this batch:")
        for w in warn:
            print("  " + w)
    else:
        print("checks: all silent.")


def readme(rows, root, locks):
    lines = [
        f"THE ROOT 808, AND THE REBUILD LOCK        {date.today()}",
        "=" * 62, "",
        "Two changes you are owed a listen on. They are separate",
        "questions — answer them separately.",
        "",
        "TWO FOLDERS. Start with folder 1; it is the one that changes",
        "beats you make every day.",
        "",
        "", "-" * 62,
        "FOLDER 1 — THE ROOT 808", "-" * 62, "",
        "  Your rule from July: a traditional beat gets a tuned 808 sub",
        "  on a real musical note under the kick. \"Add the root.\"",
        "",
        "  It has not been happening. The code skips the sub whenever a",
        "  beat has chords, and since July every DJ has chords switched",
        "  on by default — so the rule almost never fires.",
        "",
        "  On your own drive: 150 traditional beats have chords, and",
        "  ZERO of them got a sub. The only 9 beats that ever had both",
        "  are from Sept 1st, and every one of those took the beat's own",
        "  key. Those 9 are still in your library if you want to hear a",
        "  finished example: beats 2079, 2083, 2092, 2115, 2134, 2154,",
        "  2172, 2180 and 2183.",
        "",
        "  Each beat here twice:",
        "    a Now       what you get today. Chords, no sub.",
        "    b Root 808  the same beat with the sub added, tuned to that",
        "                beat's own key so it cannot fight the chords.",
        "",
        "  WHAT TO LISTEN FOR: does the low end get a note under it, or",
        "  does it get muddy? The sub sits under the kick and follows",
        "  the same pattern, so a -> b should feel like weight, not like",
        "  a second kick.",
        "",
    ]
    for name, key, note, lo_a, lo_b, _pd in root:
        lines.append(f"    {name} — in {key}, sub on {note}. "
                     f"Low end {lo_b - lo_a:+.2f} dB.")
    lines += [
        "",
        "  MEASURED: the sub's note matches the beat's key on every one",
        "  of these. NOT HEARD: whether it sits right against your",
        "  chords, or whether 3-in-4 traditional beats is too often.",
        "",
        "", "-" * 62,
        "FOLDER 2 — THE REBUILD LOCK", "-" * 62, "",
        "  When you rebuild a beat — swap a hat, move a volume — the",
        "  chords get rebuilt too. Today the machine re-picks the key",
        "  instead of reading it off the recipe.",
        "",
        "  MOST OF THE TIME THIS COSTS YOU NOTHING and there is nothing",
        "  to hear: I checked all 118 of your September beats and every",
        "  one comes back in the same key it was printed in.",
        "",
        "  It goes wrong when YOU set the key on purpose. This folder is",
        "  that case: a beat whose key came off a reference track you",
        "  dropped in. You asked for reference-wins-hard on Sept 1st.",
        "",
        "    a As printed     the beat as the reference track made it.",
        "    b Rebuild now    what a hat swap hands back today.",
        "    c Rebuild locked what the fix hands back.",
        "",
    ]
    for was, now, locked in locks:
        lines += [f"    printed in {was}",
                  f"    comes back {now}    <- today",
                  f"    with the fix {locked}", ""]
    lines += [
        "  a and c should be the same key. b is the problem.",
        "",
        "  The other case I could not put in a folder: a mood word you",
        "  type in the notes box (\"dreamy\"). That word is never saved,",
        "  so a rebuild loses it and picks a different progression — 6",
        "  of 6 in a test. Same fix covers it.",
        "",
        "", "-" * 62,
        "WHAT I NEED BACK FROM YOU", "-" * 62, "",
        "  Two answers, one line each.",
        "  1. Folder 1: keep the sub on chord beats, or leave it off?",
        "  2. Folder 2: lock the key on rebuild, yes or no?",
        "",
        "  Nothing is switched on yet. Both are sitting behind a switch",
        "  that is off; your answer flips them.",
        "",
        "", "-" * 62,
        "Per-file loudness:",
    ]
    lines += [f"  {f}/{fn:52s} {lu:6.2f} LUFS" for f, fn, lu in rows]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
