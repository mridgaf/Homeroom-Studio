"""Checkpoint 4: the twenty. Files 21-40 in Claude Drum Beats.

2 beats per crew member (beat A faithful to their prototype DNA, beat B
carrying that character's ONE evolution for this batch, per the owner's
evolve-as-we-go rule) + 2 collab beats where two personalities share the
room. Every beat picks fresh drums from the character's taste tags
(variant-seeded); only stamps are locked. Crate Prophet's two beats are
the batch's two no-sidechain renders (the ~90% rule: 2 of 20).

Never overwrites: existing files are skipped (owner rule 2026-07-15 —
no re-rendering previously made beats unless he asks).

Run:  ./.venv/bin/python tools/make_the_twenty.py
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
import crew
from crew import (BARS, CREW, R16, build_kit, lock_stamps,
                  render_crew_beat, _pick_path, _resolve_secs)

OUT = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))
JOURNAL = Path(os.path.expanduser("~/.reason_voice/crew_journal.json"))


def mutated(name, bpm=None, bars=None, feels=None, sidechain=None):
    """A per-beat copy of a personality: same DNA, one evolution applied.
    bars/feels override single lanes; everything else stays theirs."""
    p = copy.deepcopy(CREW[name])
    if bpm:
        p["bpm"] = bpm
    for lane, nb in (bars or {}).items():
        pan, gain, feel, _ = p["lanes"][lane]
        p["lanes"][lane] = (pan, gain, feel, nb)
    for lane, nf in (feels or {}).items():
        pan, gain, _, b = p["lanes"][lane]
        p["lanes"][lane] = (pan, gain, nf, b)
    if sidechain is not None:
        p["sidechain"] = sidechain
    return p


# --------------------------------------------------- the 18 solo beats
# (file_no, personality, title, variant, preset-or-None, evolution note)
# preset None = faithful render of the character as auditioned.

SOLOS = [
    (21, "Otto Grit", "Loose Change", 1, None, None),
    (22, "Otto Grit", "Pocket Lint", 2, mutated("Otto Grit", bpm=86, bars={
        "snare": ["----X--.----X---", "----X-------X-.-",
                  "----X--.----X---", "----X--.--.-X--.",
                  "----X-------X-.-", "----X--.----X---",
                  "----X--.--.-X---", "----X-.---.-X--."]}),
     "ghost-note conversation deepened — the snare now mutters between "
     "backbeats"),

    (23, "Cutz", "Blade Work", 1, None, None),
    (24, "Cutz", "Fader Hand", 2, mutated("Cutz", bpm=95, bars={
        "stamp": [R16, "------------x-x-", R16, "----------x-x-x-"] * 2}),
     "the scratch stab answers every two bars instead of every four"),

    (25, "Crate Prophet", "Attic Light", 1, None, None),
    (26, "Crate Prophet", "Smoke Rings", 2, mutated("Crate Prophet",
        bpm=90, bars={
        "bongo": ["--x---x---x---x-", "--x-x-----x---x-",
                  "------x---x-----", "--x---x-x-x---x-",
                  "--x---x---x---x-", "----x---x---x---",
                  "--x---x-------x-", "--x-x-x---x-x-x-"],
        "hat": ["x-xox-x-x-xox-x-"] * 6
               + ["x-xox-xox-xox-x-", "x-xox-x-x-xoxoxx"]}),
     "bongos turned into call-and-response, open-hat accents multiplied"),

    (27, "Chrome Dial", "Dial Tone", 1, None, None),
    (28, "Chrome Dial", "Missed Call", 2, mutated("Chrome Dial", bpm=104,
        bars={
        "kick": ["X--X--X---X-----", "X--X--X---------",
                 "X--X--X-X-------", "--------X--X--X-",
                 "X--X--X---X-----", "----------------",
                 "X--X--X---X--X--", "X--X------------"]}),
     "stop-start pushed harder — bar 6 is pure silence with one clap"),

    (29, "Glass Cat", "Nine Lives", 1, None, None),
    (30, "Glass Cat", "Velvet Claw", 2, mutated("Glass Cat", bpm=96, bars={
        "kick": ["X---------X-----"] * 3 + ["X---------X---X-"]
                + ["X---------X-----"] * 2
                + ["X---------X---X-", "X---X-----------"]},
        feels={"clap": (+28, 1, 50, 143)}),
     "the late-clap flam widened to ~28 ms and the kick got even more "
     "minimal"),

    (31, "Sunday Chop", "Pew Stomp", 1, None, None),
    (32, "Sunday Chop", "Offering Plate", 2, mutated("Sunday Chop", bpm=98,
        bars={
        "perc": ["x-x-x-x-x-x-x-x-"] * 7 + ["x-x-x-x-x-xxx-x-"]}),
     "the tambourine moved from offbeats to driving 8ths"),

    (33, "Night Metro", "Late Train", 1, None, None),
    (34, "Night Metro", "Tunnel Vision", 2, mutated("Night Metro", bpm=136,
        bars={
        "kick": ["X-----X---X-----", "X-----X---X-----",
                 "X-----X-----X---", "X-----X---X---X-",
                 "X---------------", "X-----------X---",
                 "X-----X-----X---", "X-----X---X-X---"],
        "clap": ["--------X-------"] * 4 + [R16, R16]
                + ["--------X-------"] * 2,
        "hat": ["x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-x-x-x-x-xxxxxxxx",
                "x-x-x-x-xxxxx-x-x-x-x-x-xxxxxxxx",
                "-" * 32, "-" * 32,
                "x-x-x-x-x-x-x-x-xxxxxxxxx-x-x-x-",
                "x-x-x-x-xxxxxxxxxxxxxxxxxxxxxxxx"]}),
     "the drop-out grew to two full bars of 808 alone"),

    (35, "Rage Engine", "Redline", 1, None, None),
    (36, "Rage Engine", "Overheat", 2, mutated("Rage Engine", bpm=152,
        bars={
        "kick": ["X-----X-----X---", "XX----X-----X---",
                 "X-----X-----X---", "XX-X--X-----X---",
                 "X-----X-----X---", "XX----X-----X--X",
                 "X--X--XX----X---", "XX----X--X--X--X"],
        "stamp": ["X---------------", R16] * 4}),
     "double-tap kicks arrived and the crash now opens every other bar"),

    (37, "New Math", "First Theorem", 1, None,
     "debut — the crew's first member built on no ancestor"),
    (38, "New Math", "Proof by Motion", 2, mutated("New Math", bpm=140,
        bars={
        "perc": ["-x-x-x--x-x-x-x-", "-x--x--x--x--x--"] * 4,
        "hat": ["x-x-xx-x-xx-x-xx-x-x"] * 5
               + ["x-x-x-x-x-x-x-x-x-x-",
                  "xx-xx-xx-xx-xx-xxxxx",
                  "xxxxx-x-xx-x-xxxxxxx"]}),
     "the Euclidean necklaces rotate between beats and the five-count "
     "gets denser"),
]

# ------------------------------------------------------- the 2 collabs

def collab_presets():
    """Two hand-built hybrids. Both parents' stamps appear — two tags on
    one beat, like a split single."""
    slow_leak = dict(
        num=10, bpm=134, era="collab",
        built="Otto Grit x Night Metro",
        listen="Otto's drunk lanes dragged into Metro's dark halftime: "
               "early snare on the 3, kick leaning late over a sustained "
               "sub, rolls and a two-bar blackout. Both stamps present.",
        kit={}, dust=0.25, vinyl=-44, wow=0.0, sidechain=0.3,
        space=("gated", ["snare"]), alt=None,
        drive=1.4, kick_dist=4.0, mix_sat=0.0,
        lanes=dict(
            kick=(0.0, 1.0, (+10, 3, 50, 201), [
                "X-----x---------", "X---------X-----",
                "X-----x---------", "X---------X---x-",
                "X-----x---------", "X---------------",
                "X-----x---X-----", "X-x-------X-----"]),
            snare=(0.0, 0.85, (-18, 3, 50, 202),
                   ["--------X-------"] * 3 + ["--------X------."]
                   + ["--------X-------"] * 2
                   + ["--------X--.----", "--------X-----.-"]),
            hat=(0.12, 0.36, (0, 1, 50, 203), [
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-x-x-x-x-xxxxxxxx",
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "-" * 32,
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-xxxxxxxxx-x-x-x-",
                "x-x-x-x-xxxxx-x-xxxxxxxxxxxxxxxx"]),
            stampA=(-0.3, 0.38, (0, 3, 50, 204),
                    [R16] * 3 + ["--------------x-"]
                    + [R16] * 3 + ["--------------x-"]),
            stampB=(0.3, 0.4, (0, 0, 50, 205),
                    [R16] * 3 + ["------------x---"]
                    + [R16] * 3 + ["------------x---"]),
        ),
        picks=dict(   # lane -> (parent for taste, role, choke override)
            kick=("Night Metro", "kick", (0.9, 2.0)),
            snare=("Otto Grit", "snare", None),
            hat=("Night Metro", "hat", None),
        ),
        stamp_parents=("Otto Grit", "Night Metro"),
    )
    clean_room = dict(
        num=11, bpm=142, era="collab",
        built="Glass Cat x New Math",
        listen="minimal club math: Jersey kick grammar stripped to Glass "
               "Cat's negative space, snap timekeeper, the late-clap flam "
               "over a swung Euclidean necklace. Both stamps present.",
        kit={}, dust=0.0, vinyl=0, wow=0.0, sidechain=0.25,
        space=("gated", ["snare"]), alt=None,
        drive=1.45, kick_dist=2.0, mix_sat=0.0,
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 211), [
                "X--X----X-------", "X--X--X-X-------",
                "X--X----X-------", "X--X--X-X-X-----",
                "X--X----X-------", "X--X--X-X-------",
                "X--X----X---X---", "X---X-----------"]),
            snare=(0.0, 0.85, (0, 1, 50, 212),
                   ["----X-------X---"] * 7 + ["----X-----------"]),
            clap=(0.1, 0.5, (+18, 1, 50, 213),
                  ["----X-------X---"] * 7 + ["----X-----------"]),
            snap=(0.12, 0.4, (0, 1, 50, 214),
                  ["x--x--x--x--x--x"] * 7 + ["x--x------------"]),
            perc=(-0.18, 0.28, (0, 2, 58, 215),
                  ["x---x--x--x--x--"] * 8),
            stampA=(-0.25, 0.38, (0, 1, 50, 216),
                    [R16] * 3 + ["--------------x-"]
                    + [R16] * 3 + ["--------------x-"]),
            stampB=(0.28, 0.4, (0, 1, 50, 217),
                    [R16] * 3 + ["-----------x----"]
                    + [R16] * 3 + ["-----------x----"]),
        ),
        picks=dict(
            kick=("Glass Cat", "kick", (0.6, 1.2)),
            snare=("Glass Cat", "snare", None),
            clap=("Glass Cat", "clap", None),
            snap=("Glass Cat", "snap", None),
            perc=("New Math", "perc", None),
        ),
        stamp_parents=("Glass Cat", "New Math"),
    )
    return [(39, "Otto Grit x Night Metro", "Slow Leak", slow_leak),
            (40, "Glass Cat x New Math", "Clean Room", clean_room)]


def collab_kit(shots, preset, stamps, variant, avoid):
    kit, sources = {}, {}
    for lane, (parent, plane, choke) in preset["picks"].items():
        role, must, wants, secs = CREW[parent]["kit"][plane]
        secs = _resolve_secs(choke or secs, preset["num"], variant)
        seed = preset["num"] * 1000 + variant * 7919 + hash(lane) % 97
        path, x = _pick_path(shots, role, wants, secs, seed,
                             must=must, avoid=avoid)
        if path:
            avoid.add(path)
        kit[lane] = x
        sources[lane] = path
    a, b = preset["stamp_parents"]
    kit["stampA"], kit["stampB"] = stamps[a][1], stamps[b][1]
    sources["stampA"] = f"{stamps[a][0]}  [{a}'s stamp]"
    sources["stampB"] = f"{stamps[b][0]}  [{b}'s stamp]"
    return kit, sources


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    lines = ["", f"THE TWENTY — Checkpoint 4 ({date.today()})", "=" * 56,
             "2 beats per crew member (the second carries that character's",
             "one evolution for this batch) + 2 collabs. Fresh drums every",
             "beat; stamps locked. Crate Prophet's pair are the batch's two",
             "no-sidechain renders (the ~90 percent rule).", ""]
    ok, made = True, 0

    def render_one(path, name, kit, preset):
        nonlocal ok
        L, R, got = render_crew_beat(name, kit, preset=preset)
        write_wav24(path, L, R)
        bpm = (preset or CREW[name])["bpm"]
        dur, want = len(L) / SR, BARS * 240.0 / bpm
        rms = 20 * np.log10(np.sqrt(0.5 * (L**2 + R**2).mean()) + 1e-12)
        good = abs(dur - want) < 0.02 and -14 < rms < -5 and -10 < got < -6.5
        ok &= good
        print(f"  {path.name:58s} LUFS {got:5.1f}  RMS {rms:5.1f}  "
              f"{'ok' if good else 'CHECK'}")

    for no, name, title, variant, preset, note in SOLOS:
        bpm = (preset or CREW[name])["bpm"]
        path = OUT / f"{no} {name} {title} Drums {bpm}bpm.wav"
        if path.exists() or list(OUT.rglob(path.name)):
            print(f"  {path.name:58s} exists — skipped (no re-renders)")
            continue
        kit, sources = build_kit(shots, name, stamps[name][1],
                                 variant=variant, avoid=avoid)
        sources["stamp"] = stamps[name][0]
        render_one(path, name, kit, preset)
        made += 1
        lines.append(f"{no} {name} — {title} ({bpm}bpm)")
        if note:
            lines.append(f"  evolution: {note}")
        if name == "Crate Prophet":
            lines.append("  (no sidechain — his laid-back trademark)")
        lines += [f"  {ln}: {Path(p).name if p else '(none)'}"
                  for ln, p in sources.items()] + [""]

    for no, name, title, preset in collab_presets():
        path = OUT / f"{no} {name} {title} Drums {preset['bpm']}bpm.wav"
        if path.exists() or list(OUT.rglob(path.name)):
            print(f"  {path.name:58s} exists — skipped (no re-renders)")
            continue
        kit, sources = collab_kit(shots, preset, stamps, variant=1,
                                  avoid=avoid)
        render_one(path, name, kit, preset)
        made += 1
        lines.append(f"{no} COLLAB {name} — {title} ({preset['bpm']}bpm)")
        lines.append(f"  {preset['listen']}")
        lines += [f"  {ln}: {Path(p).name if p else '(none)'}"
                  for ln, p in sources.items()] + [""]

    if made:
        with open(OUT / "README.txt", "a") as f:
            f.write("\n".join(lines))

        journal = json.loads(JOURNAL.read_text()) if JOURNAL.exists() else {}
        today = str(date.today())
        for no, name, title, variant, preset, note in SOLOS:
            if note:
                journal.setdefault(name, []).append(
                    {"date": today, "batch": "the-twenty",
                     "change": f"{note} (file {no})"})
        journal.setdefault("Snap Church", []).append(
            {"date": today, "batch": "the-twenty",
             "change": "retired — owner: too close to Night Metro and Rage "
                       "Engine; slot 9 passed to New Math"})
        JOURNAL.write_text(json.dumps(journal, indent=1))

    print(f"\n{made} new beats -> {OUT}")
    print(f"Journal updated -> {JOURNAL}")
    if not ok:
        print("WARNING: at least one render failed its numeric sanity check.")


if __name__ == "__main__":
    main()
