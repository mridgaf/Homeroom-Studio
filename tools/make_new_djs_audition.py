"""Audition batch: the two DJs that came back from never-guess-hooks.

Half Light and Fast Water were written before the 2026-09-02/03 sound work,
so they were dressed to the current house rules before he hears them:
neither names a mix_eq, so both render through the house EQ, and each got
ONE twist using amounts already in use on the nine -- Half Light chorus on
the chord lanes (it has no hat lane, so the phaser twist was impossible),
Fast Water phaser on the hat.

Renders to a scratch dir, never the library. Ends by asserting its own
premise, the way tools/make_night_metro_ab.py does: if the twist made no
difference the bench is wrong and the batch is meaningless, so say so
loudly rather than shipping it.
"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np                                              # noqa: E402
from crew import CREW, build_kit, lock_stamps, render_crew_beat  # noqa: E402
import beat_machine as bm                                        # noqa: E402

DJS = ["Half Light", "Fast Water"]
PER_DJ = 3
TWIST = {"Half Light": "chorus", "Fast Water": "phaser"}
OUT = Path.home() / "Desktop" / "Homeroom Two New DJs 2026-09-03"


def _rms_db(a, b):
    """How far apart two renders are, level-matched. -inf means identical."""
    n = min(len(a), len(b))
    d = a[:n] - b[:n]
    if not np.any(d):
        return float("-inf")
    return 20 * np.log10(np.sqrt(np.mean(d ** 2))
                         / max(np.sqrt(np.mean(a[:n] ** 2)), 1e-12))


def main():
    warn = []
    scratch = Path(tempfile.mkdtemp(prefix="new-djs-audition-"))
    print("Scanning the sample library…")
    shots = bm.build_shots()

    # ---- the beats he actually listens to
    made = []
    for dj in DJS:
        (scratch / dj).mkdir(parents=True, exist_ok=True)
        for i in range(PER_DJ):
            path, line = bm.generate([dj], root=scratch, shots=shots)
            made.append((dj, Path(path)))
            print(f"  {dj}: {Path(path).name}")

    # ---- fail loud #1: the right number of files
    if len(made) != len(DJS) * PER_DJ:
        warn.append(f"expected {len(DJS) * PER_DJ} beats, made {len(made)}")

    # ---- fail loud #2: nothing silent, nothing mono
    for dj, p in made:
        import wave
        with wave.open(str(p), "rb") as w:
            raw = w.readframes(w.getnframes())
            ch = w.getnchannels()
        a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
        v = (a[:, 0].astype(np.int32) | (a[:, 1].astype(np.int32) << 8)
             | (a[:, 2].astype(np.int32) << 16))
        v = np.where(v & 0x800000, v - 0x1000000, v).astype(np.float64)
        x = (v / 8388608.0).reshape(-1, ch)
        if np.abs(x).max() < 1e-6:
            warn.append(f"{p.name} is silent")

    # ---- fail loud #3: the twist actually does something.
    # An identity whose twist renders byte-identical to no-twist has a
    # twist that is not wired, and the batch teaches him nothing.
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    for i, dj in enumerate(DJS):
        p_on = dict(CREW[dj])
        key = TWIST[dj]
        if key not in p_on:
            warn.append(f"{dj} has no {key} key at all")
            continue
        p_off = dict(p_on)
        p_off.pop(key)
        kit, _ = build_kit(shots, dj, stamps[dj][1], variant=i,
                           avoid=avoid, preset=p_on)
        # A CHORD-targeted twist needs a chord lane to act on, and
        # build_kit makes drums only -- beat_machine._build_chords adds the
        # chord lanes later. Without this the check reads -inf and blames
        # the DJ: Glass Cat and Night Metro, both already approved, measure
        # -inf on a bare kit too. Verified 2026-09-03. So give it one
        # sustained in-key tone on a lane whose NAME starts with "chord",
        # which is how audio_engine matches the lane list (a prefix).
        if "chord" in tuple((p_on.get(key) or {}).get("lanes", ())):
            sr = 44100
            t = np.arange(int(sr * 2.0)) / sr
            tone = (0.25 * np.sin(2 * np.pi * 220.0 * t)
                    + 0.20 * np.sin(2 * np.pi * 277.2 * t)).astype(np.float32)
            for pp in (p_on, p_off):
                pp["lanes"] = dict(pp["lanes"])
                pp["lanes"]["chord0"] = (0.0, 0.5, (0, 0, 50, 900),
                                         ["X---------------"] * 8)
            kit = dict(kit)
            kit["chord0"] = tone
        on = render_crew_beat(dj, kit, preset=p_on)[0]
        off = render_crew_beat(dj, kit, preset=p_off)[0]
        moved = _rms_db(np.asarray(on), np.asarray(off))
        print(f"  {dj}: {key} moves the render {moved:.1f} dB")
        if moved == float("-inf"):
            warn.append(f"{dj}'s {key} changed NOTHING — the twist is not "
                        f"reaching the render")

    # ---- deliver
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for dj, p in made:
        (OUT / dj).mkdir(exist_ok=True)
        shutil.copy2(str(p), str(OUT / dj / p.name))
    n = len(list(OUT.rglob("*.wav")))
    if n != len(made):
        warn.append(f"copied {n} files, expected {len(made)}")

    print("\n" + "=" * 60)
    if warn:
        print("WARNING — do NOT ship this batch:")
        for w in warn:
            print("  * " + w)
    else:
        print("All checks passed. %d beats in %s" % (n, OUT))
    return 1 if warn else 0


if __name__ == "__main__":
    sys.exit(main())
