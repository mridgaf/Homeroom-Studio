"""Reusable move-don't-delete helper (Python 3.9, no 3.10+ syntax).

Implements the project's safety contract so cleanup scripts don't re-derive
it: files go into ONE dated holding folder under `root`, a tab-separated
manifest.txt records every original location, name collisions are renamed
(never overwritten), and nothing is ever deleted.

Example
-------
    from safe_move import SafeMover
    mover = SafeMover(root=ROOT, dest_label="Cleared")
    mover.add(list_of_paths)                 # Path objects to move
    mover.summary()                          # prints count + destination
    mover.run(dry_run="--dry-run" in argv,   # move nothing, just list
              skip_confirm="--yes" in argv)  # skip the typed-yes prompt
"""
from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class SafeMover:
    def __init__(self, root: Path, dest_label: str, date: Optional[str] = None):
        self.root = Path(root)
        stamp = date or "{:%Y-%m-%d}".format(datetime.now())
        self.dest = self.root / "{} {}".format(dest_label, stamp)
        self._items = []  # type: List[Path]

    def add(self, paths) -> None:
        for p in paths:
            self._items.append(Path(p))

    def summary(self) -> None:
        print("Found {} item(s) to move.".format(len(self._items)))
        print("Everything moves into:\n  {}".format(self.dest))
        print("(nothing is deleted — drag it back, or trash that one "
              "folder later)")

    def run(self, dry_run: bool = False, skip_confirm: bool = False) -> int:
        if not self.root.exists():
            print("Can't find {} — is the drive connected?".format(self.root))
            return 0
        if not self._items:
            print("Nothing to move.")
            return 0
        if dry_run:
            for p in self._items:
                print("  would move:", p)
            print("\nDRY RUN — nothing moved. Re-run without --dry-run.")
            return 0
        if not skip_confirm:
            ans = input('Move {} item(s) into "{}"? Type yes to continue: '
                        .format(len(self._items), self.dest.name)).strip().lower()
            if ans != "yes":
                print("Cancelled — nothing touched.")
                return 0

        self.dest.mkdir(parents=True, exist_ok=True)
        rows = []
        moved = 0
        for f in self._items:
            if not f.exists():
                continue
            try:
                rel = f.relative_to(self.root)
            except ValueError:
                rel = f
            target = self.dest / f.name
            if target.exists():
                target = self.dest / "DUP {}".format(f.name)
            shutil.move(str(f), str(target))
            rows.append((str(rel), target.name))
            moved += 1

        manifest = self.dest / "manifest.txt"
        with manifest.open("a") as m:
            m.write("\n# moved {} — {} item(s)\n"
                    .format(datetime.now().strftime("%Y-%m-%d %H:%M"), moved))
            for rel, name in rows:
                m.write("{}\t{}\n".format(rel, name))

        print("\nMoved {} item(s) into {}/.".format(moved, self.dest.name))
        print("Manifest:", manifest)
        return moved
