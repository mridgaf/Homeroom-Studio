"""Template library: reusable starting points built from recipes.

Reason has no API to build device chains, so templates are made BY HAND once
(follow the recipe, then save the song or Combinator patch into the templates
folder). From then on this module finds them, links them to recipes by name,
and starts fresh sessions from them. A session is a dated COPY of the
template — the original can never be accidentally overwritten.
"""
from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from rapidfuzz import fuzz

TEMPLATE_KINDS = {
    ".reason": "song",
    ".rns": "song",
    ".record": "song",
    ".cmb": "combinator",
}

MATCH_THRESHOLD = 70


class TemplateLibrary:
    def __init__(self, dir: str):
        self.dir = os.path.expanduser(dir)

    def items(self) -> list[dict]:
        """Rescans on every call — the folder changes whenever he saves from
        Reason, and it's a dozen files at most."""
        root = Path(self.dir)
        if not root.exists():
            return []
        out = []
        for p in sorted(root.iterdir()):
            kind = TEMPLATE_KINDS.get(p.suffix.lower())
            if kind and p.is_file():
                out.append({"name": p.stem, "path": str(p), "kind": kind})
        return out

    def find(self, query: str) -> Optional[dict]:
        query = (query or "").lower().strip()
        if not query:
            return None
        best, best_score = None, 0.0
        for t in self.items():
            sc = fuzz.token_set_ratio(query, t["name"].lower())
            if sc > best_score:
                best, best_score = t, sc
        return best if best_score >= MATCH_THRESHOLD else None

    def for_recipe(self, recipe_name: str) -> Optional[dict]:
        return self.find(recipe_name)

    def mirror_to(self, dest_dir: str) -> int:
        """Copy song templates into Reason's own Template Songs folder so
        they also appear in Reason's File > New From Template. Skips when
        Reason's folder doesn't exist. Returns how many were copied."""
        dest = Path(os.path.expanduser(dest_dir))
        if not dest.parent.exists():
            return 0
        dest.mkdir(exist_ok=True)
        copied = 0
        for t in self.items():
            if t["kind"] != "song":
                continue
            src = Path(t["path"])
            target = dest / src.name
            if not target.exists() or \
                    src.stat().st_mtime > target.stat().st_mtime:
                shutil.copy2(src, target)
                copied += 1
        return copied

    def new_session(self, tpl: dict, sessions_dir: str) -> Path:
        """Copy a song template into the sessions folder with a date stamp
        and return the copy's path. Never overwrites an existing session."""
        dest_dir = Path(os.path.expanduser(sessions_dir))
        dest_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d %H.%M")
        suffix = Path(tpl["path"]).suffix
        dest = dest_dir / f"{tpl['name']} {stamp}{suffix}"
        n = 2
        while dest.exists():
            dest = dest_dir / f"{tpl['name']} {stamp} ({n}){suffix}"
            n += 1
        shutil.copy2(tpl["path"], dest)
        return dest
