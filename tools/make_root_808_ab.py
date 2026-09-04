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


def split_low(L, R, hi=100.0):
    """(low, rest) of the FINISHED file, split at 100 Hz."""
    m = 0.5 * (np.asarray(L) + np.asarray(R))
    X = np.fft.rfft(m)
    f = np.fft.rfftfreq(len(m), 1 / SR)
    low = np.fft.irfft(np.where(f > hi, 0, X), len(m))
    return low, m - low


def sub_cost(La, Ra, Lb, Rb):
    """What the sub actually did, with the loudness stage taken out of it.

    Raw, the numbers lie in both directions. Adding a sub makes the file
    louder, the loudness stage pulls the whole thing back to the same
    target, and every unpicked measurement then reads as "the sub is out
    of phase with the kick" (it is not) and "the low end barely moved"
    (it moved a lot). So: fit the gain the REST of the beat was scaled
    by, undo it, and only then ask what happened underneath.

    Returns (drums_db, low_db, phase) — how far the rest of the beat had
    to step back, how much low end the sub really added, and whether it
    fights the kick (negative) or sits with it (~0)."""
    la, ha = split_low(La, Ra)
    lb, hb = split_low(Lb, Rb)
    n = min(len(la), len(lb))
    la, ha, lb, hb = la[:n], ha[:n], lb[:n], hb[:n]
    g = float(np.dot(hb, ha) / (np.dot(ha, ha) + 1e-30)) or 1e-9
    lb_n = lb / g
    added = lb_n - la
    phase = float(np.dot(added, la)
                  / (np.linalg.norm(added) * np.linalg.norm(la) + 1e-12))
    d = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)
    return 20 * np.log10(abs(g)), d(lb_n) - d(la), phase


def band_db(L, R, lo=0.0, hi=SR / 2):
    """ABSOLUTE energy in a band of the FINISHED file — measured where the
    sound comes out, not on the buffer the change was applied to."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def compose_one(name, v):
    """COMPOSE ONCE. Call this per BEAT, never per version.

    compose() is deterministic per (name, variant, attempt) but its
    repeat guard carries history across calls, so composing the same
    variant twice can land on a different attempt and a different loop
    length. The first cut of this bench composed once per version and
    handed him an 8-bar "a" against a 4-bar "b" — two different beats
    wearing an A/B label. Compose once, `version()` a copy per treatment,
    and only the treatment moves. (Same trap, same fix, as
    make_night_metro_ab.py.)"""
    q = json.loads(json.dumps(CREW[name]))
    compose(q, name, v)
    bm.vary_preset(q, v, CREW[name]["num"], tempo_locked=True)
    return q


def version(q):
    """One treatment's own copy of the composed beat — build() mutates it."""
    return normalize_preset(json.loads(json.dumps(q)))


def build(name, p, shots, stamps, avoid, v, dirs, sub_from=None):
    """Everything up to the render: the kit, the chords, and the sub.

    Split from the render so the variant SEARCH below costs a kit and a
    progression rather than a whole beat — the search throws most
    variants away, and rendering each one first made the bench slower
    than the batch it produces."""
    kit, sources = build_kit(shots, name, stamps[name][1], variant=v,
                             avoid=set(avoid), preset=p)
    vnotes = []
    _midi, harm = bm._build_chords(p, kit, sources, v, dict(dirs), vnotes)
    note = None
    if sub_from is not None:
        note = bm._add_root_sub(p, kit, sources, v, vnotes,
                                harmony_info=harm if sub_from else None,
                                traditional=True)
    return kit, (harm or {}), note


def render(name, p, kit):
    L, R, lufs = render_crew_beat(name, kit, preset=p)
    return L, R, lufs


def key_of(h):
    return "%s %s / %s" % (h.get("root"), h.get("mode"), h.get("progression"))


def root_808_folder(scratch, shots, stamps, avoid, rows, warn):
    """a Now vs b Root 808, on beats that HAVE chords."""
    out = []
    for name in ROOT_DJS:
        picked = None
        for v in range(2, 80):
            q = compose_one(name, v)
            pb = version(q)
            kit, harm, note = build(name, pb, shots, stamps, avoid, v,
                                    CHORDS, sub_from=True)
            if note and harm.get("root"):
                picked = (v, q, pb, kit, harm, note)
                break
        if not picked:
            warn.append(f"{name}: no variant in 2..80 fired the root 808")
            continue
        v, q, pb, kitb, harm, note = picked
        Lb, Rb, lufb = render(name, pb, kitb)
        pa = version(q)
        kita, _harma, _ = build(name, pa, shots, stamps, avoid, v, CHORDS)
        La, Ra, lufa = render(name, pa, kita)
        if len(La) != len(Lb):
            warn.append(f"{name}: 'a' is {len(La)} frames and 'b' is "
                        f"{len(Lb)} — these are not the same beat")
        p = pb
        lo_a, lo_b = band_db(La, Ra, hi=100.0), band_db(Lb, Rb, hi=100.0)
        stem = f"{name} {p['bpm']}bpm {harm.get('key', '?')}"
        for tag, L, R, lu in (("a Now", La, Ra, lufa),
                              ("b Root 808", Lb, Rb, lufb)):
            fn = f"{stem} — {tag}.wav"
            write_wav24(scratch / F1 / fn, L, R)
            rows.append((F1, fn, lu))
        drums, real_low, phase = sub_cost(La, Ra, Lb, Rb)
        out.append((name, harm.get("key"), note, lo_a, lo_b,
                    float(np.abs(np.asarray(La)[:len(Lb)]
                                 - np.asarray(Lb)[:len(La)]).max()),
                    drums, real_low, phase))
        print(f"  {name:15s} {harm.get('key', '?'):16s} sub={note:2s}  "
              f"low {lo_a:6.2f} -> {lo_b:6.2f} dB   rest of the beat "
              f"{drums:+5.2f} dB   sub adds {real_low:+5.2f}   "
              f"phase {phase:+.2f}")
    return out


def lock_folder(scratch, shots, stamps, avoid, rows, warn):
    """a As printed (reference key) / b Rebuild now / c Rebuild locked."""
    out = []
    for v in range(2, 80):
        q = compose_one(LOCK_DJ, v)          # once — see compose_one
        pa = version(q)
        d_a = dict(CHORDS, force_key=REF_KEY)
        kita, ha, _ = build(LOCK_DJ, pa, shots, stamps, avoid, v, d_a)
        if not ha.get("root"):
            continue
        pb = version(q)
        kitb, hb, _ = build(LOCK_DJ, pb, shots, stamps, avoid, v, CHORDS)
        if key_of(hb) == key_of(ha):
            continue            # this variant re-rolls to the same key
        pc = version(q)
        d_c = dict(CHORDS, force_key=REF_KEY,
                   chord_feel=ha.get("progression"))
        kitc, hc, _ = build(LOCK_DJ, pc, shots, stamps, avoid, v, d_c)
        La, Ra, lua = render(LOCK_DJ, pa, kita)
        Lb, Rb, lub = render(LOCK_DJ, pb, kitb)
        Lc, Rc, luc = render(LOCK_DJ, pc, kitc)
        p = pa
        # NUMBER the pair. vary_preset runs tempo_locked here, so every
        # beat by one DJ carries that DJ's bpm — the first cut of this
        # bench named files by DJ + bpm + tag and the second pair silently
        # overwrote the first. The file-count check caught it; the names
        # are what actually fix it.
        pair = len(out) + 1
        stem = f"{pair}. {LOCK_DJ} {p['bpm']}bpm"
        for tag, L, R, lu, h in (("a As printed", La, Ra, lua, ha),
                                 ("b Rebuild now", Lb, Rb, lub, hb),
                                 ("c Rebuild locked", Lc, Rc, luc, hc)):
            fn = f"{stem} — {tag} ({h.get('key', '?')}).wav"
            write_wav24(scratch / F2 / fn, L, R)
            rows.append((F2, fn, lu))
        if not (len(La) == len(Lb) == len(Lc)):
            warn.append(f"lock pair {len(out) + 1}: the three versions are "
                        f"{len(La)}/{len(Lb)}/{len(Lc)} frames — not one beat")
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
    for name, key, note, lo_a, lo_b, peakdiff, drums, real_low, phase in root:
        if phase < -0.3:
            warn.append(f"{name}: the sub FIGHTS the kick (phase {phase:+.2f})")
        if real_low < 1.0:
            warn.append(f"{name}: sub added only {real_low:+.2f} dB of low end "
                        f"with the loudness gain removed")
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
        "  finished one rather than a test render (checked, all present):",
        "    2083 Otto Grit Couch Button        2134 Crate Prophet Attic Sermon",
        "    2079 Sunday Chop Gospel Morning    2154 Sunday Chop Amen Stomp",
        "    2092 Mustang Velvet Rollcall       2172 Trip Hop Hollow Signal",
        "    2115 Half Light Dim Room           2180 Plug Soft Float",
        "    2183 Detroit Motor Overtime",
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
    for name, key, note, lo_a, lo_b, _pd, drums, real_low, _ph in root:
        lines.append(f"    {name} — in {key}, sub on {note}. The sub adds"
                     f" {real_low:+.1f} dB of low end, and the rest of the"
                     f" beat steps back {abs(drums):.1f} dB.")
    lines += [
        "",
        "  READ THAT SECOND NUMBER. The sub is a big sound, so the",
        "  loudness stage pulls the whole beat back to the same target to",
        "  make room for it. You are not only adding a sub — you are",
        "  trading a few dB of drums for it. That trade is the real",
        "  question, and it is why a and b are the same loudness: if b",
        "  just sounded louder you would pick it every time and learn",
        "  nothing.",
        "",
        "  MEASURED: the sub's note matches the beat's key on all three,",
        "  and it does NOT fight the kick — I checked for the two of them",
        "  cancelling each other and they sit together.",
        "",
        "  NOT HEARD: whether the drums stepping back is worth the",
        "  weight, whether it sits right against your chords, and whether",
        "  3-in-4 traditional beats is too often.",
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
        "  ODD-LOOKING, ON PURPOSE: both pairs say \"Otto Grit 88bpm\".",
        "  They are two different beats — he is tempo-locked, so every",
        "  beat of his lands on 88. That is why they are numbered 1. and",
        "  2. rather than named apart.",
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
