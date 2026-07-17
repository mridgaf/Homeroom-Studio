"""Batch 3 ("three from each DJ", owner order 2026-07-15): files 41-67.

Three beats per crew member. Beat 1 = current DNA, fresh drums. Beat 2 =
that character's one evolution for this batch (journal-logged). Beat 3 =
another fresh variation (new samples, shifted feel seeds, tempo nudge).

New rules applied batch-wide:
- snare space ALTERNATES gated/dry per file (owner: "variations of gated
  and dry production used") — logged per beat in the README;
- Crate Prophet's snare sits ~3 dB lower still (his lane gain 0.62) and
  his picks no longer prefer pre-reverbed samples;
- New Math runs boom-bap mode on ODD variants (owner: half his beats
  incorporate boom bap) — this batch that's 2 of his 3;
- Crate Prophet's three are the batch's no-sidechain renders (3 of 27
  ≈ the 90% rule).

Never overwrites existing files. Run:
  ./.venv/bin/python tools/make_three_each.py
"""
import copy
import json
import os
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, write_wav24
from make_drum_beats import build_shots
from crew import (BARS, CREW, R16, boom_bap_variant, build_kit,
                  lock_stamps, render_crew_beat)
from make_the_twenty import mutated

OUT = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))
JOURNAL = Path(os.path.expanduser("~/.reason_voice/crew_journal.json"))


def seed_shifted(preset_or_name, shift):
    """Same character, different breath: every lane's feel/velocity seed
    moves so jitter and wobble land differently beat to beat."""
    p = copy.deepcopy(preset_or_name if isinstance(preset_or_name, dict)
                      else CREW[preset_or_name])
    for lane, (pan, gain, (o, j, sw, seed), bars) in p["lanes"].items():
        p["lanes"][lane] = (pan, gain, (o, j, sw, seed + shift), bars)
    return p


def bpm_nudged(name, bpm, shift):
    p = seed_shifted(name, shift)
    p["bpm"] = bpm
    return p


# (file_no, personality, title, variant, preset, evolution-note)
def batch():
    B = []

    def add(no, name, title, variant, preset=None, note=None):
        B.append((no, name, title, variant, preset, note))

    # Otto Grit — evolution: the stumble doubles (drunker kick pairs)
    add(41, "Otto Grit", "Corner Nap", 3, seed_shifted("Otto Grit", 300))
    add(42, "Otto Grit", "Wobble Walk", 4, mutated("Otto Grit", bpm=87,
        bars={"kick": [
            "X------x--X-----", "X-----xx--X---x-",
            "X------x--X-xx--", "X-----xx--X---x-",
            "X------x-xX-----", "X---x-xx--X-----",
            "X------x--X-xx--", "X-x---xx-xX-----"]}),
        "the stumble doubled — kick pairs land drunker than ever")
    add(43, "Otto Grit", "Loose Thread", 5, bpm_nudged("Otto Grit", 90, 500))

    # Cutz — evolution: ghost hat pickups between the 8ths
    add(44, "Cutz", "Scalpel", 3, seed_shifted("Cutz", 300))
    add(45, "Cutz", "Ghost Fader", 4, mutated("Cutz", bpm=94, bars={
        "hat": ["x-x.x-x-x-x.x-x-"] * 6
               + ["x-x.x-x.x-x.x-x-", "x.x.x-x-x-x.x-xx"]}),
        "ghost hat pickups now whisper between his surgical 8ths")
    add(46, "Cutz", "Crossfade Sermon", 5, bpm_nudged("Cutz", 92, 500))

    # Crate Prophet — evolution: the record warps deeper (wow 0.45)
    add(47, "Crate Prophet", "Warm Static", 3,
        seed_shifted("Crate Prophet", 300))
    p = seed_shifted("Crate Prophet", 400)
    p["bpm"], p["wow"] = 91, 0.45
    add(48, "Crate Prophet", "Deep Groove", 4, p,
        "the record warps deeper — wow lifted toward tape-drunk")
    add(49, "Crate Prophet", "Basement Congas", 5,
        bpm_nudged("Crate Prophet", 93, 500))

    # Chrome Dial — evolution: the perc answers itself across the stereo
    add(50, "Chrome Dial", "Beep Test", 3, seed_shifted("Chrome Dial", 300))
    add(51, "Chrome Dial", "Answer Back", 4, mutated("Chrome Dial",
        bpm=102, bars={
        "perc": ["--x---x---------", "-----------x--x-",
                 "--x---x---------", "-----------x--x-",
                 "--x---x---x-----", "--------x--x----",
                 "--x---x---------", "--x-x------x--x-"]}),
        "the exotic perc now asks and answers itself, half-bar by half-bar")
    add(52, "Chrome Dial", "Silent Partner", 5,
        bpm_nudged("Chrome Dial", 98, 500))

    # Glass Cat — evolution: vacuum minimalism (kick almost disappears)
    add(53, "Glass Cat", "Empty Room", 3, seed_shifted("Glass Cat", 300))
    add(54, "Glass Cat", "Vacuum", 4, mutated("Glass Cat", bpm=97, bars={
        "kick": ["X---------------", "X---------X-----",
                 "X---------------", "X---------X---X-",
                 "X---------------", "X---------X-----",
                 "X---------------", "X---X-----------"]}),
        "vacuum minimalism — the kick nearly disappears and the snaps "
        "carry the room")
    add(55, "Glass Cat", "White Walls", 5, bpm_nudged("Glass Cat", 99, 500))

    # Sunday Chop — evolution: choir claps (doubled on the turnarounds)
    add(56, "Sunday Chop", "First Pew", 3, seed_shifted("Sunday Chop", 300))
    add(57, "Sunday Chop", "Double Clap", 4, mutated("Sunday Chop", bpm=97,
        bars={"clap": ["----X-------X---"] * 3 + ["----X---X---X---"]
                      + ["----X-------X---"] * 3 + ["----X---X---X-X-"]}),
        "choir claps — the backbeat doubles up on every turnaround")
    add(58, "Sunday Chop", "Late Service", 5,
        bpm_nudged("Sunday Chop", 94, 500))

    # Night Metro — evolution: committed to the long sub this one batch
    add(59, "Night Metro", "Underpass", 3, seed_shifted("Night Metro", 300))
    p = seed_shifted("Night Metro", 400)
    p["bpm"] = 138
    p["kit"]["kick"] = ("kick", "808", ["deep", "sub", "long"], (1.6, 2.2))
    add(60, "Night Metro", "Long Shadow", 4, p,
        "went all-in on the long sub this time — choke zone raised to "
        "1.6-2.2 s (variety rule still holds batch-wide)")
    add(61, "Night Metro", "Last Stop", 5, bpm_nudged("Night Metro", 142, 500))

    # Rage Engine — evolution: strobe hats (accented velocity flicker)
    add(62, "Rage Engine", "Full Throttle", 3,
        seed_shifted("Rage Engine", 300))
    add(63, "Rage Engine", "Strobe", 4, mutated("Rage Engine", bpm=151,
        bars={"hat": [
            "X-x-X-x-XxxxXxxxX-x-X-x-XxxxXxxx",
            "X-x-X-x-X-x-X-x-XxxxXxxxXxxxXxxx",
            "X-x-X-x-XxxxXxxxX-x-X-x-XxxxXxxx",
            "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx",
            "X-x-X-x-XxxxXxxxX-x-X-x-XxxxXxxx",
            "X-x-X-x-X-x-X-x-XxxxXxxxXxxxXxxx",
            "XxxxXxxxXxxxXxxxX-x-X-x-XxxxXxxx",
            "XxxxXxxxXxxxXxxxXxxxXxxxXxxxXxxx"]}),
        "strobe hats — hard velocity flicker through the rolls")
    add(64, "Rage Engine", "Pit Call", 5, bpm_nudged("Rage Engine", 149, 500))

    # New Math — owner rule: boom bap in half his beats (odd variants)
    add(65, "New Math", "Dusty Theorem", 3, boom_bap_variant(bpm=94),
        "boom-bap mode debut: the math at 94, swung dusty hats, short "
        "kick, half dust and a vinyl bed (owner: half his beats)")
    add(66, "New Math", "Fifth Axiom", 4, seed_shifted("New Math", 400))
    p = boom_bap_variant(bpm=92)
    p = seed_shifted(p, 500)
    add(67, "New Math", "Chalk Dust", 5, p)
    return B


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    today = str(date.today())
    lines = ["", f"THREE FROM EACH DJ — batch 3 ({today})", "=" * 56,
             "27 beats, files 41-67. Snare space now ALTERNATES gated/dry",
             "per beat (owner verdict). Crate Prophet's snare pulled ~3 dB",
             "further down and his three skip sidechain (the 90% rule).",
             "New Math runs boom-bap mode on 2 of 3 (half rule).", ""]
    ok, made = True, 0
    for no, name, title, variant, preset, note in batch():
        p = preset or CREW[name]
        space = "gated" if no % 2 == 0 else "dry"
        path = OUT / f"{no} {name} {title} Drums {p['bpm']}bpm.wav"
        if path.exists() or list(OUT.rglob(path.name)):
            print(f"  {path.name:56s} exists — skipped (no re-renders)")
            continue
        kit, sources = build_kit(shots, name, stamps[name][1],
                                 variant=variant, avoid=avoid, preset=p)
        sources["stamp"] = stamps[name][0]
        L, R, got = render_crew_beat(name, kit, space=space, preset=p)
        write_wav24(path, L, R)
        dur, want = len(L) / SR, BARS * 240.0 / p["bpm"]
        rms = 20 * np.log10(np.sqrt(0.5 * (L**2 + R**2).mean()) + 1e-12)
        good = abs(dur - want) < 0.02 and -14 < rms < -5 and -10 < got < -6.5
        ok &= good
        made += 1
        print(f"  {path.name:56s} LUFS {got:5.1f}  RMS {rms:5.1f}  "
              f"[{space}]  {'ok' if good else 'CHECK'}")
        lines.append(f"{no} {name} — {title} ({p['bpm']}bpm, {space} snare)")
        if note:
            lines.append(f"  evolution: {note}")
        if name == "Crate Prophet":
            lines.append("  (no sidechain — his laid-back trademark)")
        lines += [f"  {ln}: {Path(sp).name if sp else '(none)'}"
                  for ln, sp in sources.items()] + [""]
    if made:
        with open(OUT / "README.txt", "a") as f:
            f.write("\n".join(lines))

        journal = json.loads(JOURNAL.read_text()) if JOURNAL.exists() else {}
        evs = {name: note for _, name, _, _, _, note in batch() if note}
        for name, note in evs.items():
            journal.setdefault(name, []).append(
                {"date": today, "batch": "three-from-each",
                 "change": note})
        JOURNAL.write_text(json.dumps(journal, indent=1))
    print(f"\n{made} new beats -> {OUT}\nJournal updated.")
    if not ok:
        print("WARNING: at least one render failed its numeric sanity check.")


if __name__ == "__main__":
    main()
