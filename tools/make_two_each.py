"""Batch 5 ("two more from each, using what you've learned"): files 68-85.

Two beats per crew member, each built around a finding from the
2026-07-15 school synthesis (connections-2026-07.md):

Beat 1 — THE FRISSON BEAT: bar 7 strips to a lone kick (the documented
  2-4-beat anticipation dose), bar 8 slams back full-kit plus a "spark"
  — one brand-new timbre the beat hasn't used, at max velocity. That
  stacks all three chill triggers (new voice + dynamic jump + unprepared
  timbre) at one downbeat, and the strip guarantees the bar-RMS contrast
  the emotion research wants. Bounce characters also get shorter kick
  chokes (low-band FLUX drives groove, not sustain).

Beat 2 — THE TIMBRE-SHIFT BEAT: Margulis's law (vary timbre across
  repeats, keep the pattern) — one lane swaps to a different sample for
  bars 5-8 while its pattern carries on.

Specials: Night Metro's frisson beat debuts the Roughness 808 (30-80 Hz
AM = the documented threat band). New Math's second beat is boom-bap
mode with the swung club kick (Jersey grammar at 57%). Crate Prophet's
pair skip sidechain (his trademark; 2 of 18 ≈ the 90% rule). Snare
space keeps alternating gated/dry by file number.

Never overwrites. Run:  ./.venv/bin/python tools/make_two_each.py
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
from make_three_each import seed_shifted

OUT = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))
JOURNAL = Path(os.path.expanduser("~/.reason_voice/crew_journal.json"))

# era-true short chokes for the frisson beats (flux rule) — bounce
# characters only; Night Metro keeps his long sub (weight IS his job)
FLUX_CHOKE = {
    "Otto Grit": (0.4, 0.65), "Cutz": (0.4, 0.65),
    "Crate Prophet": (0.45, 0.7), "Chrome Dial": (0.5, 0.8),
    "Glass Cat": (0.5, 0.8), "Sunday Chop": (0.5, 0.8),
    "Rage Engine": (0.6, 1.0), "New Math": (0.45, 0.75),
}


def frisson(name, shift):
    """Bar 7 = lone kick (anticipation dose), bar 8 = full kit + spark."""
    p = seed_shifted(name, shift)
    for lane, (pan, gain, feel, bars) in p["lanes"].items():
        nb = list(bars)
        nb[6] = ("X" + "-" * (len(nb[6]) - 1)) if lane == "kick" \
            else "-" * len(nb[6])
        p["lanes"][lane] = (pan, gain, feel, nb)
    p["lanes"]["spark"] = (-0.22, 0.5, (0, 1, 50, 990 + p["num"]),
                           [R16] * 7 + ["X---------------"])
    p["kit"]["spark"] = ("fx", None,
                         ["impact", "hit", "vox", "yeah", "laser",
                          "reverse"], 1.2)
    if name in FLUX_CHOKE:
        role, must, wants, _ = p["kit"]["kick"]
        p["kit"]["kick"] = (role, must, wants, FLUX_CHOKE[name])
    return p


def timbre_shift(name_or_preset, lane, shift):
    """Margulis move: same pattern, new sample for the B section — the
    lane splits into an A-half and a B-half with independent picks."""
    p = seed_shifted(name_or_preset, shift)
    pan, gain, (o, j, sw, seed), bars = p["lanes"][lane]
    a_bars = list(bars[:4]) + ["-" * len(b) for b in bars[4:]]
    b_bars = ["-" * len(b) for b in bars[:4]] + list(bars[4:])
    p["lanes"][lane] = (pan, gain, (o, j, sw, seed), a_bars)
    p["lanes"][lane + "B"] = (pan, gain, (o, j, sw, seed + 7), b_bars)
    p["kit"][lane + "B"] = p["kit"][lane]
    space, on = p["space"]
    if lane in on:
        p["space"] = (space, list(on) + [lane + "B"])
    return p


def batch():
    B = []  # (file_no, name, title, variant, preset, note)
    specs = [
        ("Otto Grit", "Held Breath", "Second Snare", "snare"),
        ("Cutz", "Cut the Lights", "New Blade", "hat"),
        ("Crate Prophet", "Inhale", "Reel Change", "snare"),
        ("Chrome Dial", "Flashbulb", "Costume Change", "perc"),
        ("Glass Cat", "Held Empty", "Second Skin", "snap"),
        ("Sunday Chop", "Hold the Choir", "New Robe", "clap"),
        ("Night Metro", "Pressure Drop", "Shadow Swap", "hat"),
        ("Rage Engine", "Cliff Edge", "Fresh Fuel", "hat"),
    ]
    no = 68
    for name, t1, t2, swap_lane in specs:
        p1 = frisson(name, 600)
        note1 = ("frisson build: bar 7 strips to a lone kick, bar 8 slams "
                 "with a spark (new timbre, max velocity); short-choke "
                 "kick for low-band flux"
                 if name in FLUX_CHOKE else
                 "frisson build: bar-7 strip, bar-8 spark slam")
        if name == "Night Metro":
            p1["rough_808"] = (40.0, 0.35)
            note1 += ("; DEBUT of the Roughness 808 — the sub's tail "
                      "trembles at 40 Hz, the documented threat band")
        B.append((no, name, t1, 6, p1, note1))
        no += 1
        p2 = timbre_shift(name, swap_lane, 700)
        B.append((no, name, t2, 7, p2,
                  f"timbre shift: the {swap_lane} swaps to a different "
                  f"sample for bars 5-8, pattern unchanged (repetition "
                  f"law: vary timbre, keep pattern)"))
        no += 1
    # New Math — beat 1 pure front-edge frisson, beat 2 boom mode with
    # the swung club kick (school novelty: Jersey grammar at 57% swing)
    B.append((84, "New Math", "Cold Equation", 6, frisson("New Math", 600),
              "frisson build on the front-edge kit"))
    p = boom_bap_variant(bpm=94)
    pan, gain, (o, j, _, seed), bars = p["lanes"]["kick"]
    p["lanes"]["kick"] = (pan, gain, (o, j, 57, seed), bars)
    p = seed_shifted(p, 700)
    B.append((85, "New Math", "Swing Proof", 7, p,
              "boom-bap mode + DEBUT of the swung club kick — the Jersey "
              "kick grammar itself swings at 57% (school: boom bap and "
              "tresillo are the same sweet spot from different eras)"))
    return B


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    today = str(date.today())
    lines = ["", f"TWO MORE FROM EACH — batch 5, school applied ({today})",
             "=" * 56,
             "Beat 1 per member = the frisson build (bar-7 strip, bar-8",
             "spark slam, short flux kicks). Beat 2 = the timbre shift",
             "(one lane changes sample for bars 5-8, pattern kept).",
             "Night Metro debuts the Roughness 808; New Math debuts the",
             "swung club kick. Gated/dry keeps alternating by file no.",
             "Crate Prophet's pair skip sidechain, as always.", ""]
    ok, made = True, 0
    for no, name, title, variant, p, note in batch():
        space = "gated" if no % 2 == 0 else "dry"
        path = OUT / f"{no} {name} {title} Drums {p['bpm']}bpm.wav"
        if path.exists() or list(OUT.rglob(path.name)):
            print(f"  {path.name:56s} exists — skipped (no re-renders)")
            continue
        kit, sources = build_kit(shots, name, stamps[name][1],
                                 variant=variant, avoid=avoid, preset=p)
        if stamps[name][0]:   # a Legend picks his own per beat
            sources["stamp"] = stamps[name][0]
        L, R, got = render_crew_beat(name, kit, space=space, preset=p)
        write_wav24(path, L, R)
        dur, want = len(L) / SR, BARS * 240.0 / p["bpm"]
        rms = 20 * np.log10(np.sqrt(0.5 * (L**2 + R**2).mean()) + 1e-12)
        # frisson beats legitimately carry a near-silent bar
        good = abs(dur - want) < 0.02 and -15 < rms < -5 and -10 < got < -6.5
        ok &= good
        made += 1
        print(f"  {path.name:56s} LUFS {got:5.1f}  RMS {rms:5.1f}  "
              f"[{space}]  {'ok' if good else 'CHECK'}")
        lines.append(f"{no} {name} — {title} ({p['bpm']}bpm, {space} snare)")
        lines.append(f"  school: {note}")
        if name == "Crate Prophet":
            lines.append("  (no sidechain — his laid-back trademark)")
        lines += [f"  {ln}: {Path(sp).name if sp else '(none)'}"
                  for ln, sp in sources.items()] + [""]
    if made:
        with open(OUT / "README.txt", "a") as f:
            f.write("\n".join(lines))

        journal = json.loads(JOURNAL.read_text()) if JOURNAL.exists() else {}
        for no, name, title, variant, p, note in batch():
            if variant == 6:      # one journal entry per member for the batch
                journal.setdefault(name, []).append(
                    {"date": today, "batch": "school-applied",
                     "change": "learned the frisson build + B-section timbre "
                               "shift from the synthesis pass"})
        JOURNAL.write_text(json.dumps(journal, indent=1))
    print(f"\n{made} new beats -> {OUT}\nJournal updated.")
    if not ok:
        print("WARNING: at least one render failed its numeric sanity check.")


if __name__ == "__main__":
    main()
