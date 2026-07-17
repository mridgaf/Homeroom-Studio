"""Novelty-rule beats: two renders per truly-unusual idea, 6/day cap.

Today's three ideas (from the July 2026 drum research):
1. QUINTUPLET SWING — the beat divided into 5 instead of 4 (Dilla's
   documented-but-almost-never-used feel). Honesty: RARE, not unheard.
2. EUCLIDEAN LANES — every drum lane is a different Euclidean pattern
   (world-rhythm math: tresillo/bossa/samba necklaces), including a 12-step
   lane running against the 16 grid (polymeter). Euclidean drums live in
   techno/modular; as a full hip hop kit system this is genuinely untried.
3. CLASHING SWING — each lane gets its OWN MPC swing percentage (hats 62%,
   snare 58%, kick straight). Dilla mixed feels by hand; making it a
   systematic per-lane parameter clash is the untried part.

Owner taste applied throughout (groove.OWNER_TASTE): snare-early feel,
gated snare space, sidechain on 5 of 6 (the 90% rule), modern -8 LUFS
master, real 808 kick samples always.

Run:  ./.venv/bin/python tools/make_experiments.py
Out:  ~/Documents/Samples/Claude Drum Beats/Experiment NN ...
"""
import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, write_wav24, master
from make_drum_beats import build_shots, pick, duck
from groove import (LaneFeel, OWNER_TASTE, dist808, euclid, fft_convolve,
                    gated_reverb, make_ir, master_to_lufs, mono_below,
                    mpc_swing_offset, snare_scale, sp1200, velocity)

# lanes whose level follows the owner's snare-trim (snare + its stand-ins)
SNARE_LIKE = {"snare", "clap"}

OUT = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))
LOG = Path(os.path.expanduser("~/.reason_voice/novelty_log.json"))
BARS = 8
DAILY_CAP = 3    # lowered from 10 by owner, 2026-07-15 ("only do three of
                 # the very experimental tracks daily")


def remaining_budget():
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    return DAILY_CAP - log.get(str(date.today()), 0)


def charge(n):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    today = str(date.today())
    log[today] = log.get(today, 0) + n
    LOG.write_text(json.dumps(log, indent=1))


def ebar(k, n, rot=0, accent_first=True):
    """Euclidean pattern -> velocity string of length n."""
    pat = euclid(k, n, rot)
    out = []
    for i, on in enumerate(pat):
        if not on:
            out.append("-")
        else:
            out.append("X" if (i == 0 and accent_first) else "x")
    return "".join(out)


def reverse_swell(snare_buf, onsets, wet=0.45, swell_ms=180):
    """Idea 4: a reversed reverb tail that SWELLS UP INTO each hit, then the
    dry snare lands and (with the gate) cuts dead. Anticipation → impact."""
    irL, _ = make_ir(swell_ms / 1000, 6000, predelay_ms=0, flat=True)
    tail = fft_convolve(snare_buf, irL)
    rev = np.zeros_like(snare_buf)
    L = len(irL)
    for p in onsets:
        seg = tail[max(0, p - L):p][::-1]           # reverse the pre-hit tail
        s0 = p - len(seg)
        if s0 >= 0:
            rev[s0:p] += seg * np.linspace(0, 1, len(seg))  # swell shape
    return snare_buf + rev * wet


def rhythmic_crush(mix, bpm, deep=0.9, clean=0.1):
    """Idea 5: the SP-1200 dirt itself becomes rhythmic — deep crush on the
    off-beats, clean on the downbeats — so the grit pulses with the bar."""
    dirty = sp1200(mix, amount=1.0)
    step = int(60.0 / bpm / 4 * SR)                 # a 16th
    mask = np.empty(len(mix))
    for i in range(0, len(mix), step):
        on_beat = (i // step) % 4 == 0
        mask[i:i + step] = clean if on_beat else deep
    # smooth the mask so the crush morphs rather than clicks
    k = np.hanning(step)
    k /= k.sum()
    mask = np.convolve(mask, k, "same")
    return dirty * mask + mix * (1 - mask)


def render(bpm, lanes, kit, sidechain=True, gate_snare=True, dust=0.0,
           swell_snare=False, rhythm_crush=False):
    """lanes: {name: (bars_list, gain, LaneFeel)} — each bar string may be
    ANY length; its length is the bar's grid resolution (16=16ths, 20=
    quintuplets, 12=triplet grid), so polymeter is just a shorter string."""
    bar_s = 240.0 / bpm
    n = int(BARS * bar_s * SR) + int(1.5 * SR)
    bufs = {k: np.zeros(n) for k in lanes}
    kicks = []
    wob = np.random.default_rng(77)
    for lane, (bars, gain, feel) in lanes.items():
        if lane in SNARE_LIKE:
            gain *= snare_scale()          # house balance: tame the snare bus
        snd = kit[lane].mean(axis=1)
        for b in range(BARS):
            pat = bars[b % len(bars)]
            res = len(pat)
            for s, ch in enumerate(pat):
                if ch == "-":
                    continue
                t = b * bar_s + s * bar_s / res
                if res == 16:
                    t += mpc_swing_offset(s, bpm, feel.swing)
                t += feel.offset + feel.rng.normal(0, feel.jitter / 3)
                pos = int(max(t, 0) * SR)
                v = velocity(ch, s if res == 16 else 0, wob) * gain
                e = min(n, pos + len(snd))
                if 0 <= pos < n:
                    bufs[lane][pos:e] += snd[:e - pos] * v
                    if lane == "kick":
                        kicks.append(pos)
    end = int(BARS * bar_s * SR)
    for k in bufs:
        bufs[k][:n - end] += bufs[k][end:]
        bufs[k] = bufs[k][:end]
    kicks = [p for p in kicks if p < end]
    if "snare" in bufs and (gate_snare or swell_snare):
        s = bufs["snare"]
        on = np.flatnonzero(np.abs(s) > np.abs(s).max() * 0.5)
        thin, last = [], -SR
        for p in on:
            if p - last > 0.1 * SR:
                thin.append(int(p)); last = p
        if swell_snare:
            bufs["snare"] = reverse_swell(bufs["snare"], thin)
        if gate_snare:
            bufs["snare"] = gated_reverb(bufs["snare"], thin,
                                         wet=OWNER_TASTE["gate_wet"])
    mix_others = sum(v for k, v in bufs.items() if k != "kick")
    if sidechain:
        mix_others, _ = duck(mix_others, mix_others.copy(), kicks, depth=0.3)
    mix = bufs.get("kick", 0) + mix_others
    if rhythm_crush:
        mix = rhythmic_crush(mix, bpm)
    elif dust > 0:
        mix = sp1200(mix, amount=dust)
    L, R = master(mix.copy(), mix.copy(), drive=1.2)
    L, R = mono_below(L, R, 120)
    L, R, got = master_to_lufs(L, R, target=-8.0)
    return L, R, got


def main():
    # --rerender: rebuild EXISTING experiment files with current engine
    # settings (a mix fix, not new novelty) — ignores and never charges the
    # daily budget. Normal run: only render new, budget-limited experiments.
    rerender = "--rerender" in sys.argv
    allowed = 10 ** 6 if rerender else remaining_budget()
    if allowed <= 0:
        print(f"Novelty budget spent for {date.today()} "
              f"(0 of {DAILY_CAP} left).")
        return
    if not rerender:
        print(f"Novelty budget: {allowed} of {DAILY_CAP} left today.")
    shots = build_shots()
    _, k808a = pick(shots, "kick", [], 1.1, seed=301, must="808")
    _, k808b = pick(shots, "kick", [], 2.2, seed=302, must="808")
    _, snr = pick(shots, "snare", ["room", "snare"], 1.0, seed=303)
    _, snt = pick(shots, "snare", ["trap", "snare"], 1.0, seed=304)
    _, hat = pick(shots, "hat", ["closed"], 0.5, seed=305)
    _, rim = pick(shots, "rim", ["rim"], 0.4, seed=306)
    _, prc = pick(shots, "perc", ["perc", "conga"], 0.9, seed=307)

    F = LaneFeel
    beats = [
        # -- Idea 1: quintuplet swing (5 per beat = 20-step bars) --
        ("Experiment 01 Quintuplet Roll", 88, {
            "kick": (["X----x----X---------"] * 3 + ["X----x----X----x----"],
                     1.0, F(0, 3, 50, 1)),
            "snare": (["-----X----------X---"] * 4, 0.85, F(-16, 3, 50, 2)),
            "hat": (["x-x-xx-x-xx-x-xx-x-x"] * 4, 0.38, F(0, 2, 50, 3)),
        }, {"kick": k808a, "snare": snr, "hat": hat}, dict(dust=0.5)),
        ("Experiment 02 Quintuplet Bounce", 95, {
            "kick": (["X--------xX---------"] * 4, 1.0, F(0, 3, 50, 4)),
            "snare": (["-----X---------X----"] * 4, 0.85, F(-14, 3, 50, 5)),
            "perc": (["--x---x---x---x---x-"] * 4, 0.3, F(0, 4, 50, 6)),
            "hat": (["x-x-x-x-x-x-x-x-x-x-"] * 4, 0.36, F(0, 2, 50, 7)),
        }, {"kick": k808a, "snare": snr, "perc": prc, "hat": hat}, {}),
        # -- Idea 2: Euclidean lanes (incl. 12-step polymeter lane) --
        ("Experiment 03 Euclid Corner", 96, {
            "kick": ([ebar(3, 8) + ebar(3, 8, 1)] * 4, 1.0, F(0, 3, 54, 8)),
            "snare": (["----X-------X---"] * 4, 0.85, F(-15, 3, 50, 9)),
            "rim": ([ebar(5, 16, 2)] * 4, 0.4, F(0, 3, 54, 10)),
            "hat": ([ebar(7, 16, 1)] * 4, 0.4, F(0, 2, 58, 11)),
            "perc": ([ebar(5, 12, 0)] * 4, 0.28, F(0, 4, 50, 12)),
        }, {"kick": k808a, "snare": snr, "rim": rim, "perc": prc,
            "hat": hat}, dict(dust=0.5)),
        ("Experiment 04 Euclid Nightshift", 140, {
            "kick": ([ebar(3, 8)] * 4, 1.0, F(0, 2, 50, 13)),
            "snare": (["--------X-------"] * 4, 0.8, F(0, 2, 50, 14)),
            "hat": ([ebar(7, 16)] * 3 + [ebar(11, 16, 3)], 0.42,
                    F(0, 2, 50, 15)),
            "perc": ([ebar(5, 12, 2)] * 4, 0.26, F(0, 3, 50, 16)),
        }, {"kick": k808b, "snare": snt, "hat": hat, "perc": prc},
            dict(sidechain=False)),   # the 1-in-10 no-duck render
        # -- Idea 3: clashing per-lane swing --
        ("Experiment 05 Swing Collision", 90, {
            "kick": (["X-----x---X-----"] * 4, 1.0, F(+8, 3, 50, 17)),
            "snare": (["----X-------X---"] * 4, 0.85, F(-18, 3, 58, 18)),
            "hat": (["x-x-x-x-x-x-x-x-"] * 4, 0.4, F(0, 2, 62, 19)),
            "rim": (["-------x--------"] * 4, 0.35, F(0, 3, 66, 20)),
        }, {"kick": k808a, "snare": snr, "hat": hat, "rim": rim},
            dict(dust=0.5)),
        ("Experiment 06 Swing Collision Deep", 84, {
            "kick": (["X-------x-X-----"] * 4, 1.0, F(+10, 3, 54, 21)),
            "snare": (["--------X-------"] * 4, 0.88, F(-20, 3, 62, 22)),
            "hat": (["x--xx--xx--xx--x"] * 4, 0.36, F(0, 2, 58, 23)),
            "perc": (["--x---x---x---x-"] * 4, 0.26, F(0, 4, 66, 24)),
        }, {"kick": k808b, "snare": snr, "hat": hat, "perc": prc}, {}),
        # -- Idea 4: reverse-swell gated snare (anticipation -> impact) --
        ("Experiment 07 Reverse Swell", 92, {
            "kick": (["X-----x---X-----"] * 4, 1.0, F(0, 3, 54, 25)),
            "snare": (["----X-------X---"] * 4, 0.85, F(-15, 3, 50, 26)),
            "hat": (["x-x-x-x-x-x-x-x-"] * 4, 0.4, F(0, 2, 54, 27)),
        }, {"kick": k808a, "snare": snr, "hat": hat},
            dict(swell_snare=True, dust=0.5)),
        ("Experiment 08 Reverse Swell Halftime", 136, {
            "kick": (["X-------X---X---"] * 4, 1.0, F(0, 2, 50, 28)),
            "snare": (["--------X-------"] * 4, 0.82, F(0, 2, 50, 29)),
            "hat": (["x-x-x-x-x-x-xxxx"] * 4, 0.42, F(0, 2, 50, 30)),
        }, {"kick": k808b, "snare": snt, "hat": hat},
            dict(swell_snare=True)),
        # -- Idea 5: rhythmic bit-crush (the dirt pulses with the bar) --
        ("Experiment 09 Pulse Crush", 94, {
            "kick": (["X-----x---X-----"] * 4, 1.0, F(0, 3, 58, 31)),
            "snare": (["----X-------X---"] * 4, 0.85, F(-15, 3, 50, 32)),
            "hat": (["x-x-x-x-x-x-x-x-"] * 4, 0.4, F(0, 2, 58, 33)),
            "rim": (["-------x--------"] * 4, 0.34, F(0, 3, 58, 34)),
        }, {"kick": k808a, "snare": snr, "hat": hat, "rim": rim},
            dict(rhythm_crush=True)),
        ("Experiment 10 Pulse Crush Trap", 148, {
            "kick": (["X-----X---X-----"] * 4, 1.0, F(0, 2, 50, 35)),
            "snare": (["--------X-------"] * 4, 0.8, F(0, 2, 50, 36)),
            "hat": (["x-x-x-x-xxxxx-x-"] * 4, 0.42, F(0, 2, 50, 37)),
        }, {"kick": k808b, "snare": snt, "hat": hat},
            dict(rhythm_crush=True)),
    ]

    if rerender:                       # rebuild what already exists
        todo = [b for b in beats
                if (OUT / f"{b[0]} Drums {b[1]}bpm.wav").exists()]
    else:                              # render new ones up to budget
        todo = [b for b in beats
                if not (OUT / f"{b[0]} Drums {b[1]}bpm.wav").exists()][:allowed]
    print(f"{'Re-rendering' if rerender else 'Rendering'} {len(todo)} experiment(s).")

    lines = ["", "EXPERIMENTS " + str(date.today()), "-" * 40]
    made = 0
    for name, bpm, lanes, kit, opts in todo:
        L, R, got = render(bpm, lanes, kit, **opts)
        path = OUT / f"{name} Drums {bpm}bpm.wav"
        write_wav24(path, L, R)
        print(f"  {path.name:52s} LUFS {got:5.1f}")
        lines.append(f"{name} ({bpm}bpm)")
        made += 1
    if not rerender:
        charge(made)
    NOTES = {
        "07": "07-08 REVERSE SWELL: a reversed reverb tail swells UP INTO "
              "each snare, then the dry hit lands and the gate cuts it dead "
              "— anticipation into impact. Untried combined with the gate.",
        "09": "09-10 PULSE CRUSH: the SP-1200 dirt itself is rhythmic — deep "
              "12-bit crush on the off-beats, clean on the downbeats — so "
              "the grit breathes with the bar. Untried.",
    }
    idea_notes = [
        "01-02 QUINTUPLET SWING: the beat split into 5 instead of 4.",
        "  Dilla documented, almost never used. Rare, not unheard.",
        "03-04 EUCLIDEAN LANES: each drum is world-rhythm math -",
        "  kick=tresillo E(3,8), hats=samba bell E(7,16), rims=bossa",
        "  E(5,16), plus a 12-step perc lane drifting against the",
        "  grid (polymeter). Untried as a full hip hop kit system.",
        "05-06 CLASHING SWING: every lane its own swing % (hats 62,",
        "  snare 58+early, kick straight). Dilla did it by hand;",
        "  as a systematic parameter clash it is untried.",
        NOTES["07"], NOTES["09"], ""]
    lines += [""] + idea_notes
    if made:
        with open(OUT / "README.txt", "a") as f:
            f.write("\n".join(lines))
    print(f"\n{'Re-rendered' if rerender else 'Made'} {made}"
          f"{'' if rerender else ', charged budget'}. -> Claude Drum Beats")


if __name__ == "__main__":
    main()
