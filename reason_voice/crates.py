"""Crates: named collections of starred samples/patches.

Found sounds are worthless if you lose them again. "Star two" drops result
#2 into the favorites crate; "add two to my drums crate" makes crates on the
fly. Crates persist as one small JSON file and show up as browsable bins.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

KEEP_FIELDS = ("name", "path", "kind", "device", "folder",
               "category", "group", "tokens", "bpm")


def _slim(entry: dict) -> dict:
    return {k: entry[k] for k in KEEP_FIELDS if k in entry}


class Crates:
    def __init__(self, path: str = "~/.reason_voice/crates.json"):
        self.path = Path(os.path.expanduser(path))
        self.data: dict = {}
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text())
            except (ValueError, OSError):
                self.data = {}

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=1))

    @staticmethod
    def _norm(name: str) -> str:
        name = (name or "favorites").lower().strip()
        for junk in ("my ", "the "):
            if name.startswith(junk):
                name = name[len(junk):]
        return name.removesuffix(" crate")

    def add(self, crate: str, entry: dict) -> str:
        crate = self._norm(crate)
        items = self.data.setdefault(crate, [])
        if not any(e["path"] == entry["path"] for e in items):
            items.append(_slim(entry))
            self._save()
        return crate

    def remove(self, crate: str, path: str) -> bool:
        crate = self._norm(crate)
        items = self.data.get(crate, [])
        kept = [e for e in items if e["path"] != path]
        if len(kept) != len(items):
            self.data[crate] = kept
            if not kept:
                del self.data[crate]
            self._save()
            return True
        return False

    def remove_anywhere(self, path: str) -> bool:
        hit = False
        for crate in list(self.data):
            if self.remove(crate, path):
                hit = True
        return hit

    def entries(self, crate: str) -> list[dict]:
        return list(self.data.get(self._norm(crate), []))

    def summary(self) -> list[dict]:
        return [{"name": k, "count": len(v)}
                for k, v in sorted(self.data.items())]
