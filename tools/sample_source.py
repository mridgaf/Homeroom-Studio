"""Which folders the Beat Machine takes samples from. One switch.

Owner 2026-09-06: "I'm going to copy them into that folder and then make
it so that's the only folder you check for the samples. If I move
everything, it will mess with reason."

COPYING is right and this is why: Reason songs and patches point at the
original files by path, so MOVING them breaks his sessions. Copies would
normally be a problem here — the same sound at two paths counts twice and
quietly costs variety — but pointing the scan at the sorted folder ALONE
removes the originals from the pool entirely, so there is nothing to
double-count. The earlier "move, don't copy" advice is superseded; it was
written when both folders were going to be scanned.

Nothing is ever deleted or moved by this script. It edits one line in
sample_packs.json and can be put back with one word.

  ./.venv/bin/python tools/sample_source.py            what it uses now
  ./.venv/bin/python tools/sample_source.py sorted     the sorted folder only
  ./.venv/bin/python tools/sample_source.py all        back to every pack
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "sample_packs.json"
# What a lane needs before it can hand every preset its own sound. Below
# this the `avoid` rule (no two DJs share a sample) runs out and beats
# start repeating each other. Counted from the real roster on 2026-09-06:
# 41 kick lanes, 38 snare, 37 hat, 33 fx, 20 perc, 16 clap.
NEEDED = {"kick": 41, "snare": 38, "hat": 37, "fx": 33, "perc": 20,
          "clap": 16, "snap": 6, "bongo": 5, "crash": 4, "rim": 2, "vox": 1}


def _counts(roots):
    import sample_library
    got = sample_library.scan_packs([r for r in roots if Path(r).exists()])
    return {k: len(v) for k, v in got.items() if v}


def report(cfg):
    sorted_root = cfg.get("sorted_root") or ""
    packs = cfg.get("roots") or []
    mode = "SORTED FOLDER ONLY" if not packs else "ALL PACKS"
    print("Right now the Beat Machine uses: %s\n" % mode)
    if not sorted_root:
        print("No sorted folder is set up.")
        return
    if not Path(sorted_root).exists():
        print("The sorted folder is not there (is the drive plugged in?):")
        print("   %s" % sorted_root)
        return
    have = _counts([sorted_root])
    print("In your sorted folder:")
    if not have:
        print("   nothing yet — it's empty.")
    short = []
    for role, need in NEEDED.items():
        n = have.get(role, 0)
        flag = "" if n >= need else "   <- thin, wants about %d" % need
        if n or need >= 16:
            print("   %-7s %4d%s" % (role, n, flag))
        if n < need:
            short.append(role)
    print()
    if not packs:
        print("You are on the sorted folder only.")
        if short:
            print("Thin lanes will make DJs repeat each other's sounds:")
            print("   " + ", ".join(short))
            print("Put more in, or switch back with:  sample_source.py all")
    else:
        if short:
            print("NOT READY to switch yet. These lanes are still thin:")
            print("   " + ", ".join(short))
            print("\nSwitch anyway with: sample_source.py sorted")
        else:
            print("Ready. Switch with:  sample_source.py sorted")


def main():
    cfg = json.loads(CFG.read_text())
    arg = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    if arg in ("sorted", "all"):
        # the full pack list is never thrown away — it is parked here so
        # "all" can put it back without anyone retyping four paths
        parked = cfg.get("_all_roots") or cfg.get("roots") or []
        cfg["_all_roots"] = parked
        cfg["roots"] = [] if arg == "sorted" else list(parked)
        CFG.write_text(json.dumps(cfg, indent=1, ensure_ascii=False) + "\n")
        print("Switched to: %s\n"
              % ("the sorted folder only" if arg == "sorted"
                 else "all sample packs"))
    elif arg:
        print(__doc__)
        return
    report(cfg)


if __name__ == "__main__":
    main()
