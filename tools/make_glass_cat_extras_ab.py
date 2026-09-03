"""A/B audition: Glass Cat's guest-lane clutter, before vs after the
2026-09-03 extras.p/nmax cut.

Second finding from the same research pass as the gated-reverb move (see
make_glass_cat_space_ab.py / DJ-PROFILES-GAP-ANALYSIS.md). The research:
"keep the kit small: 3-4 elements maximum... resist the urge to add
layers... the most air of any DJ in the roster." His extras.p (0.62)
wasn't even the roster's LOWEST -- Sunday Chop's 0.53 was -- despite that
superlative claim. Cut to p=0.35, nmax=1: clearly the sparsest guest-lane
rate on the roster now, still not zero (the research says "resist the
urge", not "never").

This is a PROBABILITY, not a per-beat deterministic effect like the reverb
move -- the honest proof is a RATE over many composed beats, not one
before/after pair. Rendered anyway: a few real variants where a guest lane
happened to land under the old rate and not the new one, so there's
something to actually listen to as well as a number to read.

Run:  ./.venv/bin/python tools/make_glass_cat_extras_ab.py
Out:  ~/Desktop/Homeroom Glass Cat Extras <today>/
"""
import copy
import os
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
import pattern_gen
from make_drum_loops import write_wav24
from make_drum_beats import build_shots
from crew import CREW, build_kit, lock_stamps, render_crew_beat

DESK = Path(os.path.expanduser(
    f"~/Desktop/Homeroom Glass Cat Extras {date.today()}"))
NAME = "Glass Cat"
NEW_EXTRAS = CREW[NAME]["extras"]                # today's live value
OLD_EXTRAS = dict(NEW_EXTRAS, p=0.62, nmax=2)    # what it was before today
N_SWEEP = 200
N_EXAMPLES = 3


def sweep(extras, n=N_SWEEP):
    """Fraction of composed beats that pick up a guest lane, and how many
    -- measured, not guessed, over many variants rather than one beat."""
    pattern_gen.PAT_HIST = Path(tempfile.mktemp())   # never touch the real one
    hits, extra_sum, guest_variants = 0, 0, []
    for v in range(n):
        p = copy.deepcopy(CREW[NAME])
        p["extras"] = extras
        pattern_gen.compose(p, NAME, v)
        guests = p.get("_guests", [])
        if guests:
            hits += 1
            extra_sum += len(guests)
            guest_variants.append(v)
    return hits / n, extra_sum / n, set(guest_variants)


def main():
    old_rate, old_avg, old_v = sweep(OLD_EXTRAS)
    new_rate, new_avg, new_v = sweep(NEW_EXTRAS)
    print(f"OLD p={OLD_EXTRAS['p']} nmax={OLD_EXTRAS['nmax']}: guest lane "
          f"on {old_rate:.0%} of beats, avg {old_avg:.2f} extra")
    print(f"NEW p={NEW_EXTRAS['p']} nmax={NEW_EXTRAS['nmax']}: guest lane "
          f"on {new_rate:.0%} of beats, avg {new_avg:.2f} extra")

    # real variants where OLD added a guest and NEW doesn't -- the RNG draw
    # that decides "guest or not" is identical between the two conditions
    # for a given variant (extras isn't part of the seed), so this set is
    # exactly the beats that flip
    examples = sorted(old_v - new_v)[:N_EXAMPLES]
    if not examples:
        print("No example variants found in range -- the rate numbers "
              "above are still the real proof.")
        return

    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)
    avoid = {s[0] for s in stamps.values() if s[0]}
    scratch = Path(tempfile.mkdtemp(prefix="glass-cat-extras-ab-"))
    p = CREW[NAME]
    rows = []
    for v in examples:
        for tag, extras in [("a Before", OLD_EXTRAS), ("b After", NEW_EXTRAS)]:
            preset = copy.deepcopy(p)
            preset["extras"] = extras
            pattern_gen.PAT_HIST = Path(tempfile.mktemp())
            pattern_gen.compose(preset, NAME, v)
            kit, _ = build_kit(shots, NAME, stamps[NAME][1], variant=v,
                               avoid=set(avoid), preset=preset)
            L, R, got = render_crew_beat(NAME, kit, preset=preset)
            fn = f"{NAME} variant{v} {tag}.wav"
            write_wav24(scratch / fn, L, R)
            guests = preset.get("_guests", [])
            rows.append((fn, got, guests))
            print(f"  {fn:46s} LUFS {got:6.2f}  guests: {guests or 'none'}")

    if DESK.exists():
        shutil.rmtree(DESK)
    DESK.mkdir(parents=True)
    for f in sorted(scratch.glob("*.wav")):
        shutil.copy2(f, DESK / f.name)
    (DESK / "READ ME.txt").write_text(
        readme(old_rate, old_avg, new_rate, new_avg, rows))
    shutil.rmtree(scratch)
    print(f"\n{len(list(DESK.glob('*.wav')))} files -> {DESK}")


def readme(old_rate, old_avg, new_rate, new_avg, rows):
    lines = [
        f"GLASS CAT — fewer guest lanes   {date.today()}",
        "=" * 62, "",
        "WHY THIS BATCH",
        "  A second finding from the same research pass as the reverb",
        "  move. The research says Glass Cat should have 'the most air",
        "  of any DJ in the roster' and 'resist the urge to add layers'.",
        "  His old guest-lane rate (0.62, up to 2 extras) wasn't even the",
        "  roster's LOWEST -- Sunday Chop's 0.53 was. Cut to 0.35, max 1",
        "  extra -- clearly the sparsest on the roster now. This is LIVE",
        "  already, same as the reverb move.",
        "",
        "THIS IS A PROBABILITY, NOT A GUARANTEED SOUND CHANGE",
        f"  Measured over {N_SWEEP} composed beats, not just this file:",
        f"    old settings: a guest lane on {old_rate:.0%} of beats, "
        f"averaging {old_avg:.2f} extra sounds",
        f"    new settings: a guest lane on {new_rate:.0%} of beats, "
        f"averaging {new_avg:.2f} extra sounds",
        "  Most beats were ALREADY guest-free either way -- this narrows",
        "  how OFTEN the extra clutter shows up, it doesn't remove a",
        "  sound that was always there.",
        "",
        "WHAT'S IN THE FILES",
        "  A few real beat numbers where the OLD settings happened to add",
        "  a guest sound and the NEW settings don't. 'a Before' has the",
        "  extra layer, 'b After' doesn't -- same beat otherwise.",
        "",
    ]
    for fn, lu, guests in rows:
        lines.append(f"    {fn:46s} {lu:6.2f} LUFS   guests: "
                     f"{', '.join(guests) if guests else 'none'}")
    lines += [
        "",
        "NOT HEARD",
        "  Whether 0.35/1 is the right amount, or too far. I can measure",
        "  the rate; I can't tell you if it still feels like a real DJ or",
        "  now too bare.",
        "",
        "WHAT I NEED BACK FROM YOU",
        "  Keep it, or say a number that feels more right.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
