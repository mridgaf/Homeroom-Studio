"""Any Legend: what he has already, against his new build. One command.

Owner 2026-09-05: "I'll want this same for all remaining legends. Not in
the 9. Create something to make that easy and clear for each session."

This is make_doc_day_newbuild.py with the name taken as an argument and the
hand-written prose replaced by a generated diff. That script is LEFT ALONE
on purpose — it is the exact thing that produced the batch he approved, and
rewriting it to be generic would put his one good result at risk to save a
copy. This one is what every legend after him uses.

EVERY LESSON FROM THE THREE DOC DAY BATCHES IS BAKED IN HERE. Do not
re-derive them:

  * compose() is CALLED. The `lanes` block in the config is a skeleton
    whose kick line is a byte-for-byte copy of the snare line, on all
    twelve legends. Rendering it is what made him say "the kick drum is
    right on the snare with all of these auditions". beat_machine.py calls
    compose() first; so does this.
  * compose() is called ONCE per beat and the result handed to BOTH
    versions. Composing per version lets the form drift and then a-vs-b
    stops being a test of the changes.
    THE ONE EXCEPTION is --structure, added 2026-09-05 on Farrow. That
    default also overwrites both versions' `kit`, so a build whose whole
    change IS the kit and the grammar renders two byte-identical files —
    which is what happened, and the "nothing moved by even 0.5 dB" guard
    below is what caught it. Under --structure each version composes and
    picks its own drums. The two beats then genuinely differ in form, and
    that is the point: you are judging the new arrangement, not the same
    arrangement through new processing. Say which mode was used in the
    READ ME so he knows what he is comparing.
  * compose() is NOT reproducible across processes — it loads a persisted
    repeat history and re-rolls. So beats are never selected by variant
    number from a separate scan; choose() composes a run and selects from
    what it actually composed.
  * Beats whose kick is already a long 808, or which hit the kick fewer
    than MIN_KICK_HITS times, do not go in the comparison — an 808 with no
    headroom measures ~0 and half a two-beat audition being a dud is what
    wasted his ears twice. They ship in a sibling folder instead, and the
    READ ME says so rather than quietly stacking the deck.
  * The KIT is held constant across a and b. Sample choice is not what he
    is being asked to judge.
  * The picked sample NAME is printed per lane per beat. A weird pick has
    to be visible on the page, not need a code dive. Its absence cost a
    whole round trip.

Run:  ./.venv/bin/python tools/make_legend_newbuild.py --legend "Razor"
Out:  ~/Desktop/Homeroom Auditions/Homeroom <Legend> NEW BUILD <today>/
      ~/Desktop/Homeroom Auditions/Homeroom <Legend> NEW BUILD <today> — Two more/
"""
import argparse
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


def drop_stamp(preset):
    import beat_machine as bm
    bm._drop_stamp(preset)


def roll_swing(preset, variant):
    """generate()'s swing roll. Found 2026-09-24: this script never called
    it. compose() already sets most genres' swing, but a CANON lane (the
    Baltimore 8-count, the dembow) comes out of compose() at 50, so
    Baltimore Club's new 54 was inaudible in its audition while real beats
    had it. Legends lost their pocket wander the same way. Same variant for
    both versions, so the old side gets ITS swing and the new its own."""
    import beat_machine as bm
    bm.roll_swing(preset, variant)


def pair_kick(preset, variant, name, shots):
    """generate()'s kick pairing (2026-09-23), before the kit is picked:
    short kick whenever a bass plays, never an 808 kick on an 808 beat."""
    import beat_machine as bm
    if (preset.get("signature") or {}).get("chords_default"):
        bm.pair_kick_for(preset, variant,
                         dict(bm.parse_directions(""), chords=True),
                         name, shots)


def add_melodic(preset, kit, src, variant, name, shots):
    """Put the CHORDS (and the beat's one low sound) on the audition.

    Owner 2026-09-19: "The auditions seem like they're only drums. Nobody
    should be only drums." He was right, and it was never a regression --
    checked every commit of this file and it has NEVER built a chord lane.
    Every legend audition from Razor onward was judged on drums alone
    while the researched `signature` block (Hitt Kid's piano/horns, No
    Alias's Symphony strings, J Dillo's filtered soul) never sounded.

    This is the melodic half of generate(), in generate()'s own order,
    calling generate()'s own functions rather than reimplementing them --
    since 2026-09-23 literally generate()'s own add_bass_and_chords, so
    the one-bass order (decide the bass, chords + bass line, 808 lane,
    refuse a second low) cannot drift between the two.

    A legend without `chords_default` is left alone: this turns the lane
    on the way generate() does, it does not invent one."""
    import beat_machine as bm
    dirs = bm.parse_directions("")
    if not (preset.get("signature") or {}).get("chords_default"):
        return None
    dirs = dict(dirs, chords=True)
    vnotes = []
    _midi, harmony = bm.add_bass_and_chords(preset, kit, src, shots,
                                            variant, dirs, vnotes, False,
                                            name)
    return harmony

ROOT = Path(__file__).parent.parent

NJUDGE = 2          # beats rendered old-vs-new
NEXTRA = 2          # beats rendered new-only, extra listening
NSCAN = 12          # variants composed before choosing
MIN_KICK_HITS = 15  # below this the kick is too sparse to judge (his word)


CONFIG = "legends_config.json"      # --genres switches to genres_config.json


def find_before(name):
    """The 'before' comes off disk, never rebuilt by popping keys off the
    new preset — a before assembled from memory is only as honest as the
    list of keys you remembered."""
    slug = name.lower().replace(" ", "-")
    stem = CONFIG[:-len(".json")]
    hits = sorted(ROOT.glob(stem + ".pre-*.json"))
    hits = [h for h in hits if slug in h.name.lower()]
    if not hits:
        raise SystemExit(
            "no 'before' backup for %r. Copy %s to\n"
            "  %s.pre-%s-<today>.json\n"
            "BEFORE you edit his settings, or there is nothing to A/B."
            % (name, CONFIG, stem, slug))
    if len(hits) > 1:
        # NEVER GUESS THE BASELINE. This picked the alphabetically-last
        # file once and silently chose a HALF-BUILT intermediate
        # ("pre-doc-day-glue-...") over the true original
        # ("pre-doc-day-..."), which reported +0.92 dB where the real
        # old-vs-new was +5.03. A wrong baseline does not fail — it
        # quietly understates the change and he judges the wrong thing.
        raise SystemExit(
            "%d backups match %r, so which one is the TRUE 'before' is a\n"
            "judgement, not a guess. Pass one with --before:\n  %s"
            % (len(hits), name, "\n  ".join(str(h.name) for h in hits)))
    return hits[0]


def choose(raw, name, kick="plain"):
    """Compose a run of variants; split into the ones worth judging and
    the rest. See the module docstring for why this is not a list of
    variant numbers.

    `kick` says which beats may be JUDGED. The default "plain" excludes
    808 kicks, because an 808 with no headroom measures ~0 on a low-end
    change and half a two-beat audition being a dud wasted his ears twice.
    But that rule is a proxy, and on an 808-LED legend it inverts: Mustang
    is 60% 808 by his own declared weights, and the change under test on
    his 2026-09-05 build was 808 distortion — which is audible on exactly
    the beats "plain" throws away. Pass "808" or "any" when the change
    lives in the 808, and say so in the READ ME."""
    judged, extra = [], []
    for v in range(NSCAN):
        q = json.loads(json.dumps(raw))
        notes = compose(q, name, v)
        k = q["lanes"]["kick"][3]
        hits = sum(b.count("X") + b.count("x") for b in k)
        is808 = q["kit"]["kick"][1] == "808"
        want = {"plain": not is808, "808": is808, "any": True}[kick]
        ok = want and hits >= MIN_KICK_HITS
        # "completely different beats": no two judged beats share a kick
        # line, or it is one beat rendered twice.
        if ok and len(judged) < NJUDGE and all(k != j[1]["lanes"]["kick"][3]
                                               for j in judged):
            judged.append((v, q, notes))
        elif len(extra) < NEXTRA:
            extra.append((v, q, notes))
        if len(judged) == NJUDGE and len(extra) == NEXTRA:
            break
    if len(judged) < NJUDGE:
        raise SystemExit(
            "only %d of %d variants had a %r kick with %d+ hits — raise "
            "NSCAN, try --kick any, or look at the grammar"
            % (len(judged), NSCAN, kick, MIN_KICK_HITS))
    return judged, extra


def diff_preset(old, new):
    """What actually differs between the two presets, generated rather
    than described. Hand-written change lists drift from the code; this
    one cannot."""
    keys = sorted(set(old) | set(new))
    out = []
    for k in keys:
        # `lanes` is composed fresh per beat, so diffing it is noise. `kit`
        # and `listen` are not: on a structure build they carry the change.
        if k.startswith("_") or k == "lanes":
            continue
        a, b = old.get(k, "(unset)"), new.get(k, "(unset)")
        if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
            out.append((k, a, b))
    return out


def _shape(p):
    """Five of the twelve legends have no `snare` lane at all — Mustang,
    Farrow, Mustang-shaped club presets and the rest carry a `clap` (and
    sometimes a `snap`) instead, which is their identity, not an omission.
    Reading p["lanes"]["snare"] blind crashed the whole render on Mustang."""
    k = p["lanes"]["kick"][3]
    back = next((ln for ln in ("snare", "clap", "snap")
                 if ln in p["lanes"]), None)
    hits = sum(b.count("X") + b.count("x") for b in k)
    tail = "" if back is None else " | %s %s" % (back, p["lanes"][back][3][0])
    return ("%d bars, %d different kick bars, %d kick hits | kick %s%s"
            % (len(k), len(set(k)), hits, k[0], tail))


def band_db(L, R, lo=0.0, hi=SR / 2):
    """ABSOLUTE energy in a band of the FINISHED file — measured where the
    sound comes out, not on the buffer an effect was applied to."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def attack_db(L, R):
    """How much louder the first 5 ms of each hit is than the 40 ms after.
    The only ruler here that sees a transient shaper.

    CAUTION, learned the hard way: a long sub tone under the kick fills the
    40 ms window and drives this NEGATIVE while the front edge is in fact
    sharper. If it goes negative, render once with the sub off before
    telling him the drums got duller."""
    x = np.abs(0.5 * (np.asarray(L) + np.asarray(R)))
    n = len(x)
    step, win = int(0.005 * SR), int(0.040 * SR)
    thr = np.percentile(x, 99.0)
    hits, i = [], 0
    while i < n - win:
        if x[i] >= thr:
            hits.append(i)
            i += win
        else:
            i += 1
    if not hits:
        return 0.0
    a = np.mean([x[h:h + step].mean() for h in hits])
    b = np.mean([x[h + step:h + win].mean() for h in hits])
    return 20 * np.log10((a + 1e-12) / (b + 1e-12))


def _avg(deltas, idx):
    return float(np.mean([d[idx] for d in deltas])) if deltas else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--legend", required=True)
    ap.add_argument("--before", help="override the auto-found backup file")
    ap.add_argument("--kick", choices=("plain", "808", "any"),
                    default="plain",
                    help="which kicks may be JUDGED. Default plain (no "
                         "808s). Use 808/any when the change under test "
                         "lives in the 808 itself — see choose().")
    ap.add_argument("--structure", action="store_true",
                    help="the change is in kit/lanes/grammar, not in the "
                         "processing. Each version composes its own beat "
                         "with its own drums at the same variant, instead "
                         "of both borrowing the new build's. Without this "
                         "a structure-only change renders IDENTICAL files.")
    ap.add_argument("--genres", action="store_true",
                    help="a genre from genres_config.json (owner "
                         "2026-09-24: genres get the same pass)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing Desktop folder (it may be a "
                         "batch he already has — check before using this)")
    a = ap.parse_args()
    global CONFIG
    if a.genres:
        CONFIG = "genres_config.json"
    name = a.legend
    if name not in CREW:
        raise SystemExit("no legend named %r" % name)

    before = Path(a.before) if a.before else find_before(name)
    print("before: %s" % before.name)
    old = json.loads(before.read_text())[name]
    old["genre" if a.genres else "legend"] = True
    live = json.loads((ROOT / CONFIG).read_text())[name]
    # Kit held constant across a and b — sample choice is not on trial.
    # Unless it IS: under --structure the old build keeps its own kit and
    # its own sound-bank setting, because that is the change being judged.
    # Leaving this in place under --structure also CRASHES rather than
    # quietly mis-comparing, once the two builds have different lanes:
    # Farrow's old build has a clap lane and his new one does not, so the
    # old preset ended up with new-kit keys and old-lane keys and
    # render_crew_beat died on KeyError: 'clap'.
    if not a.structure:
        old["kit"] = live["kit"]
        old["own_soundbank"] = live.get("own_soundbank", False)
    OLD, NEW = normalize_preset(old), CREW[name]
    changed = diff_preset(json.loads(before.read_text())[name], live)
    if not changed:
        raise SystemExit(
            "nothing differs between the backup and the live config for %r "
            "— there is no new build to audition yet." % name)
    print("changed: %s" % ", ".join(k for k, _o, _n in changed))

    desk = Path(os.path.expanduser(
        "~/Desktop/Homeroom Auditions/Homeroom %s NEW BUILD %s" % (name, date.today())))
    versions = [("a Old", OLD), ("b New", NEW)]

    # CHECKED BEFORE ANYTHING IS RENDERED — both so he never loses a batch
    # and so this fails in a second rather than after five minutes of
    # rendering. This deleted the approved Doc Day batch on 2026-09-05
    # (same legend, same date, same folder name); rmtree does not go to
    # the Trash. House rule: never delete his files.
    for d in (desk, desk.parent / (desk.name + " — Two more")):
        if d.exists() and not a.force:
            raise SystemExit(
                "%s\nalready exists, and may be a batch he has already been "
                "given.\nMove it aside, or re-run with --force if you are "
                "certain it is disposable." % d)

    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="legend-new-"))
    (scratch / "extra").mkdir()
    rows, deltas, picks = [], [], []

    judged, extras = choose(json.loads(json.dumps(NEW)), name, a.kick)
    print("chose beats " + ", ".join(str(v) for v, _q, _n in judged))

    for i, seed_p, notes in judged:
        ref, beat_used = None, set()
        for tag, p in versions:
            if a.structure:
                # The default below hands BOTH versions the new build's kit
                # and bars so only the processing differs. That is right for
                # a dirt/EQ/saturation build and WRONG for a build whose
                # whole point is the kit and the grammar: on Farrow
                # 2026-09-05 every change lived in kit/lanes/grammar, the
                # overwrite made the two presets identical, and the renders
                # came out byte-for-byte the same. Here each version
                # composes its own beat at the same variant. Note that
                # this is NOT a controlled roll — compose() re-rolls from a
                # persisted history and the two presets have different
                # grammar, so the FORM differs too. That is intended here
                # and it is the honest comparison for a structure change,
                # but it means a-vs-b is no longer a one-variable test.
                p = normalize_preset(json.loads(json.dumps(p)))
                shape_p = p
                compose(p, name, i)
            else:
                p = normalize_preset(dict(p, lanes=seed_p["lanes"],
                                          kit=seed_p["kit"]))
                shape_p = seed_p
            # generate() drops the stamp lane on every new beat (owner
            # 2026-08-01). This script never did, so every audition since
            # carried a producer-tag sample his real beats cannot have --
            # found 2026-09-24 when a siren rode both Acid Rap Bright pairs.
            drop_stamp(p)
            roll_swing(p, i)
            pair_kick(p, i, name, shots)
            kit, src = build_kit(shots, name, stamps[name][1], variant=i,
                                 avoid=set(avoid), preset=p)
            if ref is None or a.structure:
                # build_kit puts the locked stamp in kit["stamp"] but never
                # in `sources`, so until 2026-09-05 the ONE sample that
                # rides every single beat was the one sample this list did
                # not show. Four legends in a row shipped a wrong producer
                # tag under that blind spot — Doc Day, Razor, Mustang and
                # Farrow — and Kane East's was a field recording of a
                # river. It goes first now, because it is heard most.
                shown = {ln: Path(v).name if v else "(none)"
                         for ln, v in src.items() if ln in p["kit"]}
                picks.append((i, tag, shown, _shape(shape_p)))
            harmony = add_melodic(p, kit, src, i, name, shots)
            if harmony and (ref is None or a.structure):
                # which instrument the chords actually played -- the part
                # of a build this list could not show until 2026-09-24
                shown["chords"] = ", ".join(harmony.get("chord_source")
                                            or []) or "(none)"
            L, R, got = render_crew_beat(name, kit, preset=p)
            sub, air, atk = (band_db(L, R, 30.0, 55.0),
                             band_db(L, R, 8000.0), attack_db(L, R))
            if ref is None:
                ref = (sub, air, atk, np.asarray(L).copy())
            else:
                # Same-length subtraction only means anything when both
                # versions played the same bars. Under --structure they
                # compose separately and a 4-bar old vs an 8-bar new is
                # normal, so a length mismatch IS the proof they differ.
                La = np.asarray(L)
                d = (float("inf") if len(La) != len(ref[3])
                     else float(np.abs(La - ref[3]).max()))
                deltas.append(("beat %d" % i, sub - ref[0], air - ref[1],
                               atk - ref[2], d))
            fn = "%s %dbpm beat %d %s.wav" % (name, p["bpm"], i, tag)
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(), np.abs(R).max())
                                 + 1e-12)
            rows.append((fn, got, peak))
            beat_used = set(src.values())
            print("  %-44s LUFS %6.2f  sub %6.2f  air %6.2f  attack %5.2f"
                  % (fn, got, sub, air, atk))
        # Only AFTER both versions. Inside the loop, b would pick different
        # samples from a and the comparison would stop being a comparison.
        avoid |= {v for v in beat_used if v}

    extra = []
    for i, seed_p, _n in extras:
        q = normalize_preset(dict(NEW, lanes=seed_p["lanes"],
                                  kit=seed_p["kit"]))
        drop_stamp(q)
        roll_swing(q, i)
        pair_kick(q, i, name, shots)
        kit, _src = build_kit(shots, name, stamps[name][1], variant=i,
                              avoid=set(avoid), preset=q)
        add_melodic(q, kit, _src, i, name, shots)
        L, R, _got = render_crew_beat(name, kit, preset=q)
        write_wav24(scratch / "extra" / ("%s %dbpm beat %d b New.wav"
                                         % (name, q["bpm"], i)), L, R)
        extra.append((i, _shape(seed_p)))

    if desk.exists():
        shutil.rmtree(desk)
    desk.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, desk / f.name)
    xdir = desk.parent / (desk.name + " — Two more")
    if xdir.exists() and not a.force:
        raise SystemExit("%s already exists — see above." % xdir)
    if xdir.exists():
        shutil.rmtree(xdir)
    xdir.mkdir(parents=True)
    for f in sorted((scratch / "extra").glob("*.wav")):
        shutil.copy2(f, xdir / f.name)
    (xdir / "READ ME.txt").write_text("\n".join([
        "TWO MORE %s BEATS — extra listening, not the comparison" % name.upper(),
        "=" * 62, "",
        "  New build only, no old version to compare against. These are",
        "  here so you can hear his range, not to judge the changes on.",
        "  The comparison is in the folder next to this one.", "",
    ] + ["  beat %d: %s" % (i, s) for i, s in extra]) + "\n")
    (desk / "READ ME.txt").write_text(
        readme(name, before, changed, rows, deltas, picks,
               a.structure))
    shutil.rmtree(scratch)

    print("\nwhat each beat actually is:")
    for i, tag, src, shape in picks:
        print("  beat %d %s: %s" % (i, tag, shape))
        print("           " + "  ".join("%s=%s" % kv for kv in src.items()))

    n = len(list(desk.glob("*.wav")))
    print("\n%d files -> %s" % (n, desk))
    if n != NJUDGE * len(versions):
        print("WARNING: expected %d files." % (NJUDGE * len(versions)))

    # FAIL LOUD. A "new build" that measures the same as the old one is not
    # a new build, and shipping it would waste his ears.
    dead = [k for k, _s, _a, _t, d in deltas if d < 1e-6]
    if dead:
        print("WARNING: identical to 'a Old':\n  " + "\n  ".join(dead))
    print("\nnew vs old, averaged over %d beats:" % len(deltas))
    for lbl, idx in (("sub weight 30-55 Hz", 1), ("air above 8 kHz", 2),
                     ("attack", 3)):
        print("  %-20s %+.2f dB" % (lbl, _avg(deltas, idx)))
    if max(abs(_avg(deltas, i)) for i in (1, 2, 3)) < 0.5:
        print("WARNING: nothing moved by even 0.5 dB — do NOT ship this, "
              "there is nothing in it to hear.")


def readme(name, before, changed, rows, deltas, picks,
           structure=False):
    lufs = [r[1] for r in rows]
    out = [
        "%s — OLD vs A NEW BUILD   %s" % (name.upper(), date.today()),
        "=" * 62, "",
        "WHAT THIS IS",
        "  Two completely different beats. Two versions of each.", ""] + ([
        "  STRUCTURE BUILD. The change is the DRUMS and the PATTERNS, so a",
        "  and b do NOT share a beat or a sound — each side plays its own.",
        "  You are judging the whole new character, not one setting.",
        "  The dB numbers below compare two different beats, so treat them",
        "  as rough, not as a measurement of the change.", ""]
        if structure else [
        "  Same beat and the same drum sounds inside a pair, so the only",
        "  thing you're hearing between a and b is the settings.", ""]) + [
        "  a Old   him exactly as he was, read straight off %s" % before.name,
        "  b New   the research build.", "",
        "  Only this one changed. Nobody else on the roster moved.",
        "",
        "I PICKED THESE TWO, and I'm saying so rather than pretending it",
        "  was random. Beats whose kick is already a long 808, or that hit",
        "  the kick fewer than %d times, can't show a low-end change — a" % MIN_KICK_HITS,
        "  dud file wastes the audition. Those are in the 'Two more' folder",
        "  next door instead. Worth hearing, not worth judging on.", "",
        "WHAT ACTUALLY CHANGED (generated from the two settings files, so",
        "it can't drift from what was really done):",
    ]
    for k, o, n in changed:
        out.append("  %-22s %s  ->  %s"
                   % (k, json.dumps(o)[:24], json.dumps(n)[:24]))
    out += [
        "", "MEASURED, in the finished files, new against old:",
        "    sub weight (30-55 Hz)   %+.2f dB" % _avg(deltas, 1),
        "    air (above 8 kHz)       %+.2f dB" % _avg(deltas, 2),
        "    attack                  %+.2f dB" % _avg(deltas, 3), "",
        "  If the attack number is negative, that is not automatically the",
        "  drums going soft — a long sub under the kick fills the window",
        "  this ruler measures against. It gets checked before it's",
        "  explained to you.", "",
        "  All %d files sit between %.2f and %.2f LUFS, so you're judging"
        % (len(rows), min(lufs), max(lufs)),
        "  character, not loudness.", "",
        "NOT HEARD",
        "  Whether it sounds like him. I can measure that each change is",
        "  there and how big. I can't tell you which one sounds right.", "",
        "WHAT I NEED BACK",
        "  Old or new. And if new, anything that now sounds too far.", "",
        "-" * 62,
        "What each beat actually is, and what it is played with:",
    ]
    for i, tag, src, shape in picks:
        out += ["  beat %d %s: %s" % (i, tag, shape),
                "           " + "  ".join("%s=%s" % kv
                                          for kv in src.items()), ""]
    out += ["", "-" * 62, "Per-file numbers (loudness / peak):"]
    out += ["  %-44s %6.2f LUFS   %6.2f dBFS" % r for r in rows]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    main()
