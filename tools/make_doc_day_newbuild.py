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
from groove import OWNER_TASTE

ROOT = Path(__file__).parent.parent
DESK = Path(os.path.expanduser(
    f"~/Desktop/Homeroom Doc Day NEW BUILD {date.today()}"))
NAME = "Doc Day"
NBEATS = 4

# The "before" comes off disk, not off the live preset. A before built by
# deleting keys is only as honest as the list of keys you remembered.
OLD_FILE = ROOT / "legends_config.pre-doc-day-2026-09-05.json"
_old = json.loads(OLD_FILE.read_text())[NAME]
_old["legend"] = True
OLD = normalize_preset(_old)
NEW = CREW[NAME]

VERSIONS = [("a Old", OLD), ("b New", NEW)]


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
    rows, deltas = [], []

    for i in range(NBEATS):
        ref = None
        for tag, p in VERSIONS:
            kit, _ = build_kit(shots, NAME, stamps[NAME][1], variant=i,
                               avoid=set(avoid), preset=p)
            L, R, got = render_crew_beat(NAME, kit, preset=p)
            sub = band_db(L, R, 30.0, 55.0)
            air = band_db(L, R, 8000.0)
            atk = attack_db(L, R)
            if ref is None:
                ref = (sub, air, atk, np.asarray(L).copy())
            else:
                d = float(np.abs(np.asarray(L) - ref[3][:len(L)]).max())
                deltas.append((f"beat {i + 1}", sub - ref[0], air - ref[1],
                               atk - ref[2], d))
            fn = f"{NAME} {p['bpm']}bpm beat {i + 1} {tag}.wav"
            write_wav24(scratch / fn, L, R)
            peak = 20 * np.log10(max(np.abs(L).max(),
                                     np.abs(R).max()) + 1e-12)
            rows.append((fn, got, peak))
            print(f"  {fn:42s} LUFS {got:6.2f}  sub {sub:6.2f}  "
                  f"air {air:6.2f}  attack {atk:5.2f}")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(readme(rows, deltas))
    shutil.rmtree(scratch)

    n = len(list(DESK.glob("*.wav")))
    print(f"\n{n} files -> {DESK}")
    if n != NBEATS * len(VERSIONS):
        print(f"WARNING: expected {NBEATS * len(VERSIONS)} files.")

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


def readme(rows, deltas):
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
        f"  {NBEATS} beats. Two versions of each. Same beat, same samples.",
        "",
        "  a Old   him exactly as he was, read straight off the backup",
        "          file — not rebuilt from memory.",
        "  b New   the research build.",
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
        "Per-file numbers (loudness / peak):",
    ] + [f"  {fn:42s} {lu:6.2f} LUFS   {pk:6.2f} dBFS"
         for fn, lu, pk in rows]) + "\n"


if __name__ == "__main__":
    main()
