"""Clears out the 12 Legend folders and 9 DJ (crew) folders in the beats
library, leaving Favorites and Fixed Bank untouched. Then, separately,
permanently empties the Trash folder (owner decision 2026-08-07: unlike
every other cleanup in this project, the Trash step for real deletes —
he asked for it directly, see DECISIONS.md).

Step 1 (Legends + DJs): same safe pattern as clear_junk_beats.py — moves
every beat (wav + mid + stems + matching .recipes/NN.json) out of those
21 folders into a dated "Cleared YYYY-MM-DD" holding folder. Nothing in
this step is deleted. Asks you to type "yes" first.

Step 2 (Trash): lists what's in the Trash folder, then asks you to type
DELETE (capitals, on purpose — different word than step 1's "yes" so you
can't blow through both prompts on autopilot) before permanently erasing
those files. This one cannot be undone.

Usage (from the project folder):
    ./.venv/bin/python tools/clear_legends_djs.py            # asks to confirm each step
    ./.venv/bin/python tools/clear_legends_djs.py --dry-run  # only lists what would happen
    ./.venv/bin/python tools/clear_legends_djs.py --yes      # skip both typed prompts

Easier: double-click "Clear Legends and DJs.command" next to this file.
"""
import json
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))
from beat_machine import ROOT, next_number         # noqa: E402  (needs sys.path first)

PROJECT = Path(__file__).parent.parent
NUM_RE = re.compile(r"^(\d+) ")

FAV_DIR = "Favorites"
FIXED_BANK_DIR = "Fixed Bank"
TRASH_DIR = "Trash"
SKIP_ALWAYS = {".recipes"}


def load_names(config_file, project=PROJECT):
    data = json.loads((project / config_file).read_text())
    return [k for k in data if not k.startswith("_")]


def target_folders(root):
    """The 12 Legend + 9 DJ folder names — only these, nothing else."""
    legends = load_names("legends_config.json")
    crew = load_names("crew_config.json")
    names = legends + crew
    return [root / n for n in names if (root / n).is_dir()]


def beat_number(name):
    m = NUM_RE.match(name)
    return int(m.group(1)) if m else None


def find_beats(folders):
    idx = {}
    for top in folders:
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


def do_move(root, folders, dry, skip_confirm):
    dest = root / f"Cleared {datetime.now():%Y-%m-%d}"
    recipe_dir = root / ".recipes"

    beats = find_beats(folders)
    total_items = sum(len(s["wavs"]) + len(s["mids"]) + len(s["stems"])
                       for s in beats.values())
    recipe_count = sum(1 for no in beats if (recipe_dir / f"{no}.json").exists())

    names = ", ".join(f.name for f in folders) if folders else "(none found)"
    print(f"Legend + DJ folders found in the library: {names}")
    print(f"Found {len(beats)} beat(s), {total_items} file/folder(s) total, "
          f"across those folders. Favorites and Fixed Bank are not touched.")
    print(f"{recipe_count} matching recipe file(s) in .recipes/ will move too.")
    print(f"\nEverything moves into:\n  {dest}\n"
          f"(nothing is deleted in this step — drag it back, or trash that "
          f"one folder later)")

    if not beats:
        print("\nNothing to move.")
        return 0

    if dry:
        print("\nDRY RUN — nothing moved. Re-run without --dry-run to do it.")
        return 0

    if not skip_confirm:
        ans = input(f"\nMove all {len(beats)} beats out of the Legends and "
                     f"DJ folders into \"{dest.name}\"? Type yes to continue: "
                     ).strip().lower()
        if ans != "yes":
            print("Cancelled — nothing touched.")
            return 0

    dest.mkdir(parents=True, exist_ok=True)
    dest_recipes = dest / ".recipes"
    manifest_rows = []
    moved = 0

    for no in sorted(beats):
        slot = beats[no]
        for f in slot["wavs"] + slot["mids"] + slot["stems"]:
            rel = f.relative_to(root)
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

    manifest = dest / "manifest.txt"
    with manifest.open("a") as m:
        m.write(f"\n# cleared {datetime.now():%Y-%m-%d %H:%M} "
                 f"— {len(beats)} beats, {moved} file/folder(s) "
                 f"(Legends + DJ folders only)\n")
        for no, rel in manifest_rows:
            m.write(f"{no}\t{rel}\n")

    print(f"\nMoved {moved} file/folder(s) from {len(beats)} beats into "
          f"{dest.name}/.")
    print(f"Manifest: {manifest}")
    return moved


def do_trash_delete(root, dry, skip_confirm):
    trash = root / TRASH_DIR
    if not trash.exists():
        print("\nNo Trash folder found — nothing to empty.")
        return 0

    items = [p for p in trash.iterdir() if p.name != ".DS_Store"]
    if not items:
        print("\nTrash folder is already empty.")
        return 0

    print(f"\nTrash folder has {len(items)} item(s):")
    for p in sorted(items)[:20]:
        print(f"  {p.name}")
    if len(items) > 20:
        print(f"  ... and {len(items) - 20} more")

    if dry:
        print("\nDRY RUN — Trash not touched.")
        return 0

    print("\nThis step PERMANENTLY DELETES those files. Not moved, not "
          "recoverable.")
    if not skip_confirm:
        ans = input("Type DELETE (all caps) to permanently erase the Trash "
                     "folder's contents: ").strip()
        if ans != "DELETE":
            print("Cancelled — Trash left as-is.")
            return 0

    count = 0
    for p in items:
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
        count += 1

    print(f"\nPermanently deleted {count} item(s) from Trash.")
    return count


def main():
    dry = "--dry-run" in sys.argv
    skip_confirm = "--yes" in sys.argv

    if not ROOT.exists():
        print(f"Can't find the beats library at {ROOT} — is the drive connected?")
        return

    folders = target_folders(ROOT)
    do_move(ROOT, folders, dry, skip_confirm)
    do_trash_delete(ROOT, dry, skip_confirm)

    if not dry:
        print(f"\nNext beat you generate will be numbered "
              f"#{next_number(ROOT)}.")


if __name__ == "__main__":
    main()
