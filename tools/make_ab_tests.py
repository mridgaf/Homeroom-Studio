"""A/B audition pairs for the contested research findings.

Each pair renders the SAME beat twice with ONE variable changed, so the
owner's ears can rule on the questions the sources disagreed about (plus
the two biggest new colors). His verdicts become the engine defaults.

Run:  ./.venv/bin/python tools/make_ab_tests.py
Out:  ~/Documents/Samples/AB Tests/
"""
import os
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, write_wav24, master
from make_drum_beats import build_shots, pick, duck
from groove import (LaneFeel, dist808, gated_reverb, fft_convolve, make_ir,
                    master_to_lufs, mono_below, sp1200, velocity)

OUT = Path(os.path.expanduser("~/Documents/Samples/AB Tests"))
BARS = 4

BOOM = {   # 92 bpm boom bap bed shared by AB1/AB2/AB5
    "kick":  ["X-----x---X-----"] * 3 + ["X-----x---X--x--"],
    "snare": ["----X-------X---"] * 4,
    "hat":   ["x-x-x-x-x-x-x-x-"] * 4,
}
TRAP = {   # 140 bpm half-time bed for AB3
    "kick":  ["X-----X---X-----"] * 4,
    "clap":  ["--------X-------"] * 4,
    "hat":   ["x-x-x-x-x-x-x-x-", "x-x-x-x-xxxxx-x-"] * 2,
}


def render(bpm, patterns, kit, lane_feels, wob_seed=5):
    bar_n = int(round(240 / bpm * SR))
    n = BARS * bar_n + int(1.2 * SR)
    bufs = {k: np.zeros(n) for k in patterns}
    kicks = []
    wob = np.random.default_rng(wob_seed)
    for lane, bars in patterns.items():
        snd = kit[lane].mean(axis=1)
        feel = lane_feels.get(lane, LaneFeel())
        for b, pat in enumerate(bars):
            for s, ch in enumerate(pat):
                if ch == "-":
                    continue
                t = feel.hit_time(b * bar_n / SR, s, bpm)
                pos = int(t * SR)
                v = velocity(ch, s, wob) * {"kick": 1.0, "snare": 0.9,
                                            "clap": 0.9, "hat": 0.4}[lane]
                e = min(n, pos + len(snd))
                if 0 <= pos < n:
                    bufs[lane][pos:e] += snd[:e - pos] * v
                    if lane == "kick":
                        kicks.append(pos)
    # fold tail
    end = BARS * bar_n
    for k in bufs:
        bufs[k][:n - end] += bufs[k][end:]
        bufs[k] = bufs[k][:end]
    return bufs, [p for p in kicks if p < end], bar_n


def finish(mix_mono, name, loud_chain="classic"):
    L = R = mix_mono
    if loud_chain == "classic":
        L, R = master(L.copy(), R.copy(), drive=1.4)
    else:
        L, R = master(L.copy(), R.copy(), drive=1.15)
        L, R = mono_below(L, R, 120)
        L, R, got = master_to_lufs(L, R, target=-8.0)
    write_wav24(OUT / f"{name}.wav", L, R)
    rms = 20 * np.log10(np.sqrt(0.5 * (L ** 2 + R ** 2).mean()) + 1e-12)
    print(f"  {name:44s} RMS {rms:5.1f} dBFS")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shots = build_shots()
    _, kick = pick(shots, "kick", [], 1.0, seed=901, must="808")
    _, snare = pick(shots, "snare", ["room", "snare"], 1.0, seed=902)
    _, hat = pick(shots, "hat", ["closed"], 0.5, seed=903)
    _, clap = pick(shots, "clap", ["clap"], 1.0, seed=904)
    _, kick_t = pick(shots, "kick", [], 2.2, seed=905, must="808")
    kit_b = {"kick": kick, "snare": snare, "hat": hat}
    kit_t = {"kick": kick_t, "clap": clap, "hat": hat}

    print("AB1 — Dilla snare: EARLY vs LATE (kick moves opposite; hats straight)")
    for tag, snoff, koff in (("a Snare EARLY", -18, +10), ("b Snare LATE", +18, -10)):
        feels = {"kick": LaneFeel(koff, 3, 50, 1),
                 "snare": LaneFeel(snoff, 3, 50, 2),
                 "hat": LaneFeel(0, 2, 50, 3)}
        bufs, kicks, _ = render(92, BOOM, kit_b, feels)
        mix = sum(bufs.values())
        finish(mix, f"AB1{tag} 92bpm")

    print("AB2 — SP-1200 dust: OFF vs ON (54% swing both)")
    feels = {k: LaneFeel(0, 3, 54, i) for i, k in enumerate(BOOM)}
    bufs, kicks, _ = render(92, BOOM, kit_b, feels)
    mix = sum(bufs.values())
    finish(mix, "AB2a Clean 92bpm")
    finish(sp1200(mix), "AB2b SP1200 92bpm")

    print("AB3 — Trap 808: SIDECHAIN duck vs NONE (straight grid)")
    feels = {k: LaneFeel(0, 2, 50, i) for i, k in enumerate(TRAP)}
    bufs, kicks, _ = render(140, TRAP, kit_t, feels)
    bufs["kick"] = dist808(bufs["kick"], drive_db=5)
    others = sum(v for k, v in bufs.items() if k != "kick")
    ducked_L, _ = duck(others.copy(), others.copy(), kicks, depth=0.35)
    finish(bufs["kick"] + others, "AB3a No Sidechain 140bpm")
    finish(bufs["kick"] + ducked_L, "AB3b Sidechained 140bpm")

    print("AB4 — Loudness: current chain vs -8 LUFS modern chain")
    feels = {k: LaneFeel(0, 3, 58, i) for i, k in enumerate(BOOM)}
    bufs, kicks, _ = render(92, BOOM, kit_b, feels)
    mix = sum(bufs.values())
    finish(mix, "AB4a Classic Master 92bpm", "classic")
    finish(mix, "AB4b Modern Loud 92bpm", "modern")

    print("AB5 — Snare space: PLATE tail vs GATED reverb")
    bufs, kicks, bar_n = render(92, BOOM, kit_b, feels)
    irL, _ = make_ir(0.9, 6500, predelay_ms=30)
    plate = bufs["snare"] + fft_convolve(bufs["snare"], irL) * 0.35
    finish(bufs["kick"] + bufs["hat"] + plate, "AB5a Plate Snare 92bpm")
    on = [int((b * 16 + s) / 16 * bar_n) for b in range(BARS)
          for s in (4, 12)]
    gated = gated_reverb(bufs["snare"], on, wet=0.5)
    finish(bufs["kick"] + bufs["hat"] + gated, "AB5b Gated Snare 92bpm")

    (OUT / "LISTEN-GUIDE.txt").write_text(
        "AB Tests - what to listen for\n"
        "==============================\n"
        "AB1  Dilla feel: a=snare rushes (urgent/woozy)  b=snare drags (lazy/limp)\n"
        "AB2  a=clean     b=SP-1200 12-bit dust (grittier, brighter crunch)\n"
        "AB3  a=808 untouched  b=beat breathes/pumps with each kick\n"
        "AB4  a=today's master  b=modern -8 LUFS (denser, louder, less dynamic)\n"
        "AB5  a=plate tail on snare  b=80s gated blast that cuts dead\n"
        "\nSay/note which letter wins each pair - those become the defaults.\n")
    print(f"\n-> {OUT}")


if __name__ == "__main__":
    main()
