"""Moves every beat (wav + mid + "NNN ... Stems" folder) found anywhere in
the beats library into a single dated holding folder, e.g.
"Cleared 2026-07-22/", along with its .recipes/NN.json if one exists.
Nothing is deleted — a manifest.txt records exactly where every item came
from, so this is fully reversible: drag things back out, or throw away
the whole "Cleared ..." folder once you're sure. Same pattern the project
already uses for banned samples (tools/quarantine_banned.py).

Owner decision 2026-07-22: confirmed this is a full reset — EVERY folder
counts, including Favorites/ and Fixed Bank/, no exceptions. If that's
ever not what you want, edit KEEP_FOLDERS below and re-run.

Numbering: beat_machine.next_number() floors at 85 and scans .wav files
for the highest number, so once the library has no numbered .wav files
left, the next beat made will be #86 again — not a bug, just how it
works.

README.txt (the append-only render log) is snapshotted into the holding
folder and reset to empty; the engine recreates it on the next render
(it opens README.txt in "a" mode, which creates the file if missing).

Usage (from the project folder):
    ./.venv/bin/python tools/clear_junk_beats.py            # asks to confirm, then moves everything
    ./.venv/bin/python tools/clear_junk_beats.py --dry-run  # only lists what would move
    ./.venv/bin/python tools/clear_junk_beats.py --yes      # skip the "type yes" prompt

Easier: double-click "Clear Junk Beats.command" next to this file.
"""
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))
from beat_machine import ROOT                       # noqa: E402  (needs sys.path first)

NUM_RE = re.compile(r"^(\d+) ")

# Folders here are never touched, no matter what. Empty on purpose per
# owner decision 2026-07-22 (this is a full reset). Add names here later
# if you ever want to protect a folder from this script.
KEEP_FOLDERS = set()

SKIP_ALWAYS = {".recipes"}          # not a beat folder — handled separately


def beat_number(name):
    m = NUM_RE.match(name)
    return int(m.group(1)) if m else None


def find_beats(root):
    """number -> {"wavs": [...], "mids": [...], "stems": [...]}, scanning
    every top-level folder in the library except KEEP_FOLDERS, SKIP_ALWAYS,
    and any earlier "Cleared ..." folder from a previous run of this
    script."""
    idx = {}
    for top in root.iterdir():
        if not top.is_dir():
            continue
        if top.name in SKIP_ALWAYS or top.name in KEEP_FOLDERS:
            continue
        if top.name.startswith("Cleared "):
            continue
        for f in top.rglob("*"):
            no = beat_number(f.name)
            if no is None:
                continue
            slot = idx.setdefault(no, {"wavs": [], "mids": [], "stems": []})
            if f.is_dir() and f.name.endswith("Stems"):
                slot["stems"].append(f)
            elif f.suffix == ".wav":
                slot["wavs"].append(f)
            elif f.suffix == ".mid":
                slot["mids"].append(f)
    return idx


def main():
    dry = "--dry-run" in sys.argv
    skip_confirm = "--yes" in sys.argv

    if not ROOT.exists():
        print(f"Can't find the beats library at {ROOT} — is the drive connected?")
        return

    dest = ROOT / f"Cleared {datetime.now():%Y-%m-%d}"
    recipe_dir = ROOT / ".recipes"
    readme = ROOT / "README.txt"

    beats = find_beats(ROOT)
    total_items = sum(len(s["wavs"]) + len(s["mids"]) + len(s["stems"])
                       for s in beats.values())
    recipe_count = sum(1 for no in beats if (recipe_dir / f"{no}.json").exists())

    print(f"Found {len(beats)} beat(s), {total_items} file/folder(s) total, "
          f"across every folder in the library (Favorites and Fixed Bank "
          f"included).")
    print(f"{recipe_count} matching recipe file(s) in .recipes/ will move too.")
    if readme.exists() and readme.stat().st_size > 0:
        print("README.txt will be snapshotted and reset to empty.")
    print(f"\nEverything moves into:\n  {dest}\n"
          f"(nothing is deleted — drag it back, or trash that one folder later)")

    if not beats:
        print("\nNothing to move.")
        return

    if dry:
        print("\nDRY RUN — nothing moved. Re-run without --dry-run to do it.")
        return

    if not skip_confirm:
        ans = input(f"\nMove all {len(beats)} beats into "
                     f"\"{dest.name}\"? Type yes to continue: ").strip().lower()
        if ans != "yes":
            print("Cancelled — nothing touched.")
            return

    dest.mkdir(parents=True, exist_ok=True)
    dest_recipes = dest / ".recipes"
    manifest_rows = []
    moved = 0

    for no in sorted(beats):
        slot = beats[no]
        for f in slot["wavs"] + slot["mids"] + slot["stems"]:
            rel = f.relative_to(ROOT)
            target = dest / f.name
            if target.exists():
                target = dest / f"{no} DUP {f.name}"
            shutil.move(str(f), str(target))
            manifest_rows.append((no, str(rel)))
            moved += 1

        rjson = recipe_dir / f"{no}.json"
        if rjson.exists():
            dest_recipes.mkdir(parents=True, exist_ok=True)
            shutil.move(str(rjson), str(dest_recipes / rjson.name))

    if readme.exists() and readme.stat().st_size > 0:
        shutil.copy(str(readme), str(dest / "README (before clear).txt"))
        readme.write_text("")

    manifest = dest / "manifest.txt"
    with manifest.open("a") as m:
        m.write(f"\n# cleared {datetime.now():%Y-%m-%d %H:%M} "
                f"— {len(beats)} beats, {moved} file/folder(s)\n")
        for no, rel in manifest_rows:
            m.write(f"{no}\t{rel}\n")

    print(f"\nMoved {moved} file/folder(s) from {len(beats)} beats into "
          f"{dest.name}/.")
    print(f"Manifest: {manifest}")
    print("Next beat you generate will start numbering from 86 again "
          "(the engine floors at 85+1 once no numbered .wav files remain).")


if __name__ == "__main__":
    main()
