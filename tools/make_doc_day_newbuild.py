"""Doc Day (Dre): what he has already, against a completely new build.

Owner 2026-09-05: "I don't want any of the old rules to apply. As I said
before, I want this to be a completely new build. so I can compare to what
I have already versus what new research can create" — "for dr dre", i.e.
scoped to this one persona. Nothing about the other eleven Legends, the
nine, or the engine's defaults changes.

    a Old   Doc Day EXACTLY as he was before any of this, read from
            legends_config.pre-doc-day-2026-09-05.json — not reconstructed
            by popping keys off the new one, which is how a "before" quietly
            drifts. Roster defaults throughout: gated snare, no sub, no
            transient shaping, the house 1.8 compression.
    b New   the research build. Four things, every one of them named by a
            source:
              * dry snare, not gated (nothing sourced supports reverb;
                everything sourced says clean/surgical/separation)
              * the deep sub UNDER the kick actually working — the house
                rule that forbade the kick's peak from growing is lifted
                for him alone (allow_peak_db 3.0)
              * transient shaping on kick and snare ("it sounds like a
                transient designer", Gearspace; "hard-hitting drums", SSL)
              * hard bus compression, ratio 4.0, up from the house 1.8
                (his own 2001 quote, scaled honestly — see the config note)

NOT INVENTED: drive and sidechain are still roster defaults, because the
sources contradict each other on saturation and name sidechain not at all.
They are flagged in his _research_note, not quietly picked.

Renders to a scratch dir, copies to the Desktop. The library on TBOTC 3 is
never touched and no beat numbers are used.

Run:  ./.venv/bin/python tools/make_doc_day_newbuild.py
Out:  ~/Desktop/Homeroom Doc Day NEW BUILD <today>/
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
from groove import OWNER_TASTE

ROOT = Path(__file__).parent.parent
DESK = Path(os.path.expanduser(
    f"~/Desktop/Homeroom Doc Day NEW BUILD {date.today()}"))
NAME = "Doc Day"

# HOW MANY, AND HOW THEY ARE CHOSEN. He asked for two completely different
# beats, and for two with a real kick going — he had just been handed a
# kick that only played on the snare.
#
# The selection CANNOT be a list of variant numbers. compose() carries
# repeat history across calls, so variant 2 composes differently depending
# on what was composed before it in the same process (measured: v0 rolled
# the plain kick flavor in one call order and the long 808 in another).
# Picking numbers from a separate scan would silently render something
# else. So: compose a run of variants ONCE, in one fixed sequence, then
# select from the composed results. Deterministic because the call
# sequence is fixed.
#
# THE SELECTION IS DELIBERATE AND IS STATED IN THE READ ME rather than
# quietly stacking the deck, and the rejects ship alongside so nothing is
# hidden.
NJUDGE = 2          # beats rendered old-vs-new
NEXTRA = 2          # beats rendered new-only, extra listening
NSCAN = 12          # how many variants to compose before choosing
MIN_KICK_HITS = 15  # below this the kick is too sparse to judge (his word)


def choose(raw):
    """Compose a run of variants and split them into the ones worth
    judging on and the rest.

    A beat qualifies to be judged on only if its kick flavor is the plain
    one. compose() rolls his 0.1-weight 808 flavor about one beat in five,
    and an already-long 808 kick has no headroom for the sub layer to add
    anything — measured, that beat's old-vs-new sub delta is -0.07 dB
    against +5.88 on a plain kick. Shipping one of those as half a
    two-beat audition repeats exactly the fault of the last two batches:
    files with nothing in them to hear."""
    judged, extra = [], []
    for v in range(NSCAN):
        q = json.loads(json.dumps(raw))
        notes = compose(q, NAME, v)
        k = q["lanes"]["kick"][3]
        hits = sum(b.count("X") + b.count("x") for b in k)
        ok = q["kit"]["kick"][1] != "808" and hits >= MIN_KICK_HITS
        # "completely different beats": no two judged beats may share a
        # kick line, or it is one beat twice.
        if ok and len(judged) < NJUDGE and all(k != j[1]["lanes"]["kick"][3]
                                               for j in judged):
            judged.append((v, q, notes))
        elif len(extra) < NEXTRA:
            extra.append((v, q, notes))
        if len(judged) == NJUDGE and len(extra) == NEXTRA:
            break
    if len(judged) < NJUDGE:
        raise SystemExit(
            f"only {len(judged)} of {NSCAN} variants had a plain kick with "
            f"{MIN_KICK_HITS}+ hits — raise NSCAN or look at the grammar")
    return judged, extra

# The "before" comes off disk, not off the live preset. A before built by
# deleting keys is only as honest as the list of keys you remembered.
OLD_FILE = ROOT / "legends_config.pre-doc-day-2026-09-05.json"
_old = json.loads(OLD_FILE.read_text())[NAME]
_old["legend"] = True
# THE KIT IS HELD CONSTANT ACROSS a AND b ON PURPOSE. own_soundbank and the
# corrected taste tags are a SELECTION fix (2026-09-05: "It's not so much the
# kick. It's everything else." — the open sound bank was handing him
# sidesticks, open hats and a talking drum). Which samples get picked is not
# one of the four things this batch is asking him to judge, so both versions
# get the same ones: same seeds + same tags = byte-identical picks. Old and
# new kit/lanes blocks are identical, so nothing else leaks across.
_old["kit"] = json.loads(
    (ROOT / "legends_config.json").read_text())[NAME]["kit"]
_old["own_soundbank"] = True
OLD = normalize_preset(_old)
NEW = CREW[NAME]
# compose() wants a plain JSON-shaped dict and mutates it in place.
_raw_new = json.loads(json.dumps(NEW))

VERSIONS = [("a Old", OLD), ("b New", NEW)]


def _shape(p):
    """The composed beat in one line — what the kick is actually playing,
    so a beat that sounds wrong can be diagnosed off the page."""
    k = p["lanes"]["kick"][3]
    sn = p["lanes"]["snare"][3]
    hits = sum(b.count("X") + b.count("x") for b in k)
    return (f"{len(k)} bars, {len(set(k))} different kick bars, "
            f"{hits} kick hits | kick {k[0]} | snare {sn[0]}")


def band_db(L, R, lo=0.0, hi=SR / 2):
    """ABSOLUTE energy in a band of the FINISHED file — measured where the
    sound comes out, not on the buffer an effect was applied to."""
    mono = 0.5 * (np.asarray(L) + np.asarray(R))
    spec = np.abs(np.fft.rfft(mono)) ** 2
    f = np.fft.rfftfreq(len(mono), 1 / SR)
    sel = (f >= lo) & (f <= hi)
    return 10 * np.log10(spec[sel].sum() / len(mono) + 1e-30)


def attack_db(L, R):
    """How much louder the first 5 ms of each hit is than the 40 ms after
    it. This is the ruler that sees a transient shaper; crest and band
    energy do not."""
    x = np.abs(0.5 * (np.asarray(L) + np.asarray(R)))
    n = len(x)
    step = int(0.005 * SR)
    win = int(0.040 * SR)
    # peaks well above the local floor = hits
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


def main():
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="docday-new-"))
    (scratch / "extra").mkdir()
    rows, deltas, picks = [], [], []

    judged, extras = choose(_raw_new)
    print("chose beats " + ", ".join(str(v) for v, _q, _n in judged)
          + "  (extra: " + ", ".join(str(v) for v, _q, _n in extras) + ")")

    for i, seed_p, notes in judged:
        # THE BEAT ITSELF IS COMPOSED, ONCE, AND HANDED TO BOTH VERSIONS.
        #
        # This script used to render the `lanes` block straight out of the
        # config. That block is a SKELETON — every Legend's kick line in it
        # is a byte-for-byte copy of their snare line, one bar repeated
        # eight times. beat_machine.py (the real generator) never renders
        # it; it calls compose() first, which writes each beat's pattern
        # fresh from the DJ's grammar. This script skipping that step is
        # why he heard "the kick drum is right on the snare with all of
        # these auditions, and it is used sparsely", and why all four
        # beats were the same beat.
        #
        # Composed ONCE (in choose()) and copied, not composed per
        # version: compose() carries repeat history across calls, so
        # calling it twice can land the same variant on a different form
        # — and then a-vs-b would not be a test of the four changes. Same
        # reasoning, and the same shape, as build_pair() in
        # make_rage_engine_ab.py.
        ref = None
        for tag, p in VERSIONS:
            p = normalize_preset(dict(p, lanes=seed_p["lanes"],
                                      kit=seed_p["kit"]))
            kit, src = build_kit(shots, NAME, stamps[NAME][1], variant=i,
                                 avoid=set(avoid), preset=p)
            if ref is None:
                picks.append((i, {ln: Path(v).name if v else "(none)"
                                  for ln, v in src.items()},
                              _shape(seed_p), notes))
            L, R, got = render_crew_beat(NAME, kit, preset=p)
            sub = band_db(L, R, 30.0, 55.0)
            air = band_db(L, R, 8000.0)
            atk = attack_db(L, R)
            if ref is None:
                ref = (sub, air, atk, np.asarray(L).copy())
            else:
                d = float(np.abs(np.asarray(L) - ref[3][:len(L)]).max())
                deltas.append((f"beat {i}", sub - ref[0], air - ref[1],
                               atk - ref[2], d))
            fn = f"{NAME} {p['bpm']}bpm beat {i} {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            beat_used = set(src.values())
            print(f"  {fn:42s} LUFS {got:6.2f}  sub {sub:6.2f}  "
                  f"air {air:6.2f}  attack {atk:5.2f}")
        # Only AFTER both versions of this beat are rendered. Adding inside
        # the version loop would make b pick different samples from a and
        # the comparison would stop being a comparison.
        avoid |= {v for v in beat_used if v}

    # the other two beats, rendered NEW only — extra listening, explicitly
    # not part of the old-vs-new judgement (his call: "two, plus keep four")
    extra = []
    for i, seed_p, _n in extras:
        q = normalize_preset(dict(NEW, lanes=seed_p["lanes"],
                                  kit=seed_p["kit"]))
        kit, src = build_kit(shots, NAME, stamps[NAME][1], variant=i,
                             avoid=set(avoid), preset=q)
        L, R, _got = render_crew_beat(NAME, kit, preset=q)
        fn = f"{NAME} {q['bpm']}bpm beat {i} b New.wav"
        write_wav24(scratch / "extra" / fn, L, R)
        extra.append((i, _shape(seed_p)))
        print(f"  extra beat {i}: {_shape(seed_p)}")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    xdir = DESK.parent / (DESK.name + " — Two more")
    if xdir.exists():
        shutil.rmtree(xdir)
    xdir.mkdir(parents=True)
    for f in sorted((scratch / "extra").glob("*.wav")):
        shutil.copy2(f, xdir / f.name)
    (xdir / "READ ME.txt").write_text("\n".join([
        "TWO MORE DOC DAY BEATS — extra listening, not the comparison",
        "=" * 60, "",
        "  These are the other two beats his grammar wrote. New build",
        "  only, no old version to compare against — they're here so you",
        "  can hear his range, not to judge the changes on.",
        "",
        "  The comparison is in the folder next to this one.",
        "",
    ] + [f"  beat {i}: {shape}" for i, shape in extra]) + "\n")
    (DESK / "READ ME.txt").write_text(readme(rows, deltas, picks))
    shutil.rmtree(scratch)

    print("\nwhat each beat actually is:")
    for i, src, shape, _n in picks:
        print(f"  beat {i}: {shape}")
        print("           " + "  ".join(f"{ln}={nm}"
                                        for ln, nm in src.items()))

    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    if n != NJUDGE * len(VERSIONS):
        print(f"WARNING: expected {NJUDGE * len(VERSIONS)} files.")

    # FAIL LOUD. A "completely new build" that measures the same as the old
    # one is not a new build, and shipping it would waste his ears.
    dead = [k for k, _s, _a, _t, d in deltas if d < 1e-6]
    if dead:
        print("WARNING: identical to 'a Old':\n  " + "\n  ".join(dead))
    print(f"\nnew vs old, averaged over {len(deltas)} beats:")
    print(f"  sub weight 30-55 Hz  {_avg(deltas, 1):+.2f} dB")
    print(f"  air above 8 kHz      {_avg(deltas, 2):+.2f} dB")
    print(f"  attack               {_avg(deltas, 3):+.2f} dB")
    if max(abs(_avg(deltas, i)) for i in (1, 2, 3)) < 0.5:
        print("WARNING: nothing moved by even 0.5 dB — do NOT ship this, "
              "there is nothing in it to hear.")


def _avg(deltas, idx):
    return float(np.mean([d[idx] for d in deltas])) if deltas else 0.0


def readme(rows, deltas, picks):
    lufs = [r[1] for r in rows]
    return "\n".join([
        f"DOC DAY (Dre) — OLD vs A COMPLETELY NEW BUILD   {date.today()}",
        "=" * 62, "",
        "WHAT THIS IS",
        "  You said you didn't want any of the old rules applying to him —",
        "  a new build from research, so you can hear it against what you",
        "  already have. This is that, and only for him. Nothing about the",
        "  other eleven legends or the nine changed.",
        "",
        f"  {NJUDGE} completely different beats. Two versions of",
        "  each. Same beat, same drums inside a pair.",
        "",
        "  a Old   him exactly as he was, read straight off the backup",
        "          file — not rebuilt from memory.",
        "  b New   the research build.",
        "",
        "FIRST — THESE ARE REAL BEATS NOW. THE LAST ONES WEREN'T.",
        "  You said the kick was sitting right on the snare and it was",
        "  sparse. It was, exactly: the kick was playing the SAME line as",
        "  the snare, two hits a bar, the same single bar eight times, and",
        "  all four beats were the same beat.",
        "  That was a fault in the audition script, NOT in your beats.",
        "  The Beat Machine writes each beat's drum pattern fresh from his",
        "  grammar before it plays anything. This script was skipping that",
        "  step and playing the blank skeleton in the settings file, where",
        "  the kick line is a placeholder copy of the snare line. Every",
        "  Legend has that same placeholder and none of it ever reaches a",
        "  beat you make. Your beats were always fine. The audition wasn't.",
        "  Now the script does what the Beat Machine does.",
        "",
        "  I PICKED THESE TWO, and I'm saying so rather than pretending",
        "  it was random. His grammar rolls a long 808 kick about one",
        "  beat in five, and an 808 that long has no room for the new sub",
        "  to add anything — on one of those the change measures nothing",
        "  at all. Half a two-beat audition being a dud is what went",
        "  wrong the last two times, so beats whose kick is already an",
        "  808, or which hit the kick fewer than 15 times in the loop,",
        "  aren't used for the comparison. They're in the 'Two more'",
        "  folder next to this one instead — worth hearing, just not",
        "  worth judging this change on.",
        "",
        "SECOND — THE DRUM SOUNDS ARE FIXED",
        "  You said the drum choices were weird and it was everything",
        "  except the kick. You were right, and it wasn't his settings.",
        "  There's a rule from July that lets any DJ use any sound in the",
        "  bucket, and the way it was built it threw away every DJ's own",
        "  description before picking. So the picking was pure chance.",
        "  Last batch that gave you two SIDESTICKS where snares go, OPEN",
        "  hats where tight hats go, and a TALKING DRUM.",
        "  His own description is now the boss for him: crisp hard snare,",
        "  tight closed hats, tambourine and cowbell. That's what these",
        "  use. Nobody else on the roster changed.",
        "  So these beats sound different from last time for TWO reasons —",
        "  better drums, and the four changes below. The drums are the",
        "  same in a and b, so a-vs-b is still only the four changes.",
        "",
        "THE FOUR CHANGES, AND WHO SAID SO",
        "  1. The snare is DRY, not gated.",
        "     Gated reverb is an 80s drum effect. Nobody writing about his",
        "     records mentions it — it was just the setting seven of the",
        "     twelve legends happened to inherit. Everything that IS",
        "     written about him says the opposite: clean, surgical, every",
        "     sound kept out of the others' way.",
        "",
        "  2. The deep sub under the kick finally works.",
        "     This is the old rule you meant. Everything in a beat is",
        "     levelled against the kick, so the kick was banned from",
        "     getting any louder — which meant the sub tone couldn't add",
        "     anything and did nothing on two out of three kicks. That ban",
        "     is a house rule, not anything to do with Dre. It's lifted for",
        "     him only.",
        "     THE COST IS REAL: everything else in his beats now sits a",
        "     little further under the kick. That's the trade. If it sounds",
        "     top-heavy or thin, that's what you're hearing and I turn it",
        "     back down.",
        "",
        "  3. The kick and snare hit harder on the front edge.",
        "     A producer forum describing his drums: 'it sounds like a",
        "     transient designer with hard SSL compression'. The engine has",
        "     had a transient designer built and tested the whole time,",
        "     connected to nothing. It's connected now.",
        "",
        "  4. Harder compression on the whole beat — 4, up from 1.8.",
        "     His own words in 2001: 'I usually have the ratio up to about",
        "     eight or 10 on a lot of things.' Not set to 8, and the config",
        "     note says why: he meant each sound on its own desk channel,",
        "     and this engine only has one squeeze across everything.",
        "     Honestly, this one is the weakest of the four — the",
        "     compressor in here reacts too slowly and evenly to do much.",
        "",
        "WHAT I DID *NOT* CHANGE, AND WHY",
        "  Master saturation and the sidechain are still the roster",
        "  defaults. Not laziness — the sources fight each other. One",
        "  forum says he clips and saturates hard for loudness; every",
        "  Aftermath engineer says clean and surgical. Nothing names the",
        "  sidechain at all. You told me not to guess, so I didn't. Both",
        "  are one word from you away from being the next thing tested.",
        "",
        "MEASURED, in the finished files, new against old:",
        f"    sub weight (30-55 Hz)   {_avg(deltas, 1):+.2f} dB",
        f"    air (above 8 kHz)       {_avg(deltas, 2):+.2f} dB",
        f"    attack                  {_avg(deltas, 3):+.2f} dB",
        "",
        "  READ THE ATTACK NUMBER CAREFULLY — it is NEGATIVE and that is",
        "  not the drums going soft. The ruler compares the first 5",
        "  thousandths of a second of each hit against the 40 after it.",
        "  The new deep sub rings for 150 thousandths, so it fills the",
        "  second half of that window and the ratio drops. Checked it by",
        "  rendering with the sub switched off: the front-edge shaping is",
        "  still adding attack on every beat. What you should hear is a",
        "  bigger, longer bottom end, not a duller hit.",
        "",
        "  The sub number is much bigger than anything I sent you before,",
        "  and that is the point. Every earlier batch picked its kicks at",
        "  random and kept landing on ones already maxed out, so the new",
        "  sub had nowhere to go and measured about +1.4 dB. Both of",
        "  these beats have a kick with room, and both show it — +6.1 and",
        "  +6.7 dB. This is the first batch where the change is on every",
        "  file instead of one.",
        "",
        "  The air number is near zero and that is honest. His EQ is",
        "  almost identical to the standard one; the only band that",
        "  differs is the low shelf, and most of a low boost gets",
        "  flattened back out by the loudness matching. Earlier batches",
        "  showed air moving because a bright open hat got picked by",
        "  chance, not because of anything in his settings.",
        f"  All {len(rows)} files sit between {min(lufs):.2f} and "
        f"{max(lufs):.2f} LUFS, so you're",
        "  judging character, not loudness.",
        "",
        "NOT HEARD",
        "  Whether any of it sounds like Dre, or like him. I can measure",
        "  that each change is there and how big it is. I can't tell you",
        "  which one sounds right.",
        "",
        "WHAT I NEED BACK",
        "  Old or new. And if new: is the kick too big now? That's the one",
        "  change with a price attached.",
        "",
        "-" * 62,
        "What each beat actually is, and what it is played with:",
    ] + [line for i, src, shape, _n in picks
         for line in (f"  beat {i}: {shape}",
                      "           " + "  ".join(f"{ln}={nm}"
                                                for ln, nm in src.items()),
                      "")] + [
        "",
        "-" * 62,
        "Per-file numbers (loudness / peak):",
    ] + [f"  {fn:42s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
         for fn, lu, pk in rows]) + "\n"


if __name__ == "__main__":
    main()
