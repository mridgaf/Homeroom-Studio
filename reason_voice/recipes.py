from __future__ import annotations
from __future__ import annotations
"""Recipe knowledge base: parse, search, and step through sound recipes.

Recipes are markdown files with YAML frontmatter following the v3 anatomy
(accuracy rating, tested/theoretical status, transferable technique).
Device references are plain markdown files named after the device.
"""
import os
import re
from pathlib import Path

import yaml
from rapidfuzz import fuzz

from .indexer import tokenize
from .search import expand

STEP_RE = re.compile(r"^\s*\d+[\.\)]\s+(.*)$")


class Recipe:
    def __init__(self, path: Path, meta: dict, body: str):
        self.path = path
        self.meta = meta
        self.body = body
        self.name = meta.get("name", path.stem)
        self.book = str(meta.get("book", "")).lower()
        self.accuracy = str(meta.get("accuracy", "?")).upper()
        self.status = str(meta.get("status", "theoretical")).lower()
        self.technique = meta.get("technique", "")
        self.sounds_like = meta.get("sounds_like", "")
        tag_text = " ".join([
            self.name, self.book, str(meta.get("tags", "")),
            str(self.sounds_like), str(self.technique),
        ])
        self.tokens = sorted(set(tokenize(tag_text)))
        self.steps = self._extract_steps(body)

    @staticmethod
    def _extract_steps(body: str) -> list[str]:
        steps, in_steps = [], False
        for line in body.splitlines():
            if line.strip().lower().startswith("## steps"):
                in_steps = True
                continue
            if in_steps and line.startswith("## "):
                break
            if in_steps:
                m = STEP_RE.match(line)
                if m:
                    steps.append(m.group(1).strip())
                elif steps and line.strip():  # continuation line
                    steps[-1] += " " + line.strip()
        return steps

    def summary(self) -> str:
        like = f" — sounds like {self.sounds_like}" if self.sounds_like else ""
        return f"{self.name}{like} [{self.book}, accuracy {self.accuracy}, {self.status}]"


def split_sections(body: str) -> list[tuple[str, str]]:
    """Split a recipe body into (title, content) pairs at each `## ` heading.

    Text before the first `## ` (the H1 line, intro prose) is dropped — the
    card header renders that from frontmatter instead.
    """
    sections, title, buf = [], None, []
    for line in body.splitlines():
        if line.startswith("## "):
            if title is not None:
                sections.append((title, "\n".join(buf).strip()))
            title, buf = line[3:].strip(), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        sections.append((title, "\n".join(buf).strip()))
    return sections


def parse_recipe(path: Path) -> Recipe | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return Recipe(path, {}, text)
    parts = text.split("---", 2)
    if len(parts) < 3:
        return Recipe(path, {}, text)
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        meta = {}
    return Recipe(path, meta, parts[2])


class RecipeLibrary:
    def __init__(self, recipes_dir: str, device_refs_dir: str | None = None,
                 theory_dir: str | None = None):
        self.recipes: list[Recipe] = []
        root = Path(os.path.expanduser(recipes_dir))
        if root.exists():
            for p in sorted(root.rglob("*.md")):
                r = parse_recipe(p)
                if r:
                    self.recipes.append(r)
        # device_refs and theory notes share one lookup: both are plain .md
        # answered by "what is X" / "explain X"
        self.device_refs: dict[str, Path] = {}
        for d in (device_refs_dir, theory_dir):
            if not d:
                continue
            dref = Path(os.path.expanduser(d))
            if dref.exists():
                for p in sorted(dref.glob("*.md")):
                    self.device_refs[p.stem.lower().replace("-", " ")] = p

    def search(self, query: str, top_n: int = 5) -> list[Recipe]:
        weights = expand(tokenize(query))
        if not weights:
            return []
        scored = []
        for r in self.recipes:
            s = sum(w for tok, w in weights.items() if tok in r.tokens)
            # name/sounds_like fuzzy assist
            target = f"{r.name} {r.sounds_like}".lower()
            fz = fuzz.partial_ratio(query.lower(), target)
            if fz >= 80:
                s += 1.0
            if s > 0:
                scored.append((s, r))
        scored.sort(key=lambda x: -x[0])
        return [r for _s, r in scored[:top_n]]

    # What he calls his gear -> the reference file that explains it
    DEVICE_ALIASES = {
        "drum pads": "launchkey mk3", "pads": "launchkey mk3",
        "controller": "launchkey mk3", "midi controller": "launchkey mk3",
        "keyboard": "launchkey mk3", "launchkey": "launchkey mk3",
        "launch key": "launchkey mk3",
        "interface": "audiobox 96", "audio interface": "audiobox 96",
        "audiobox": "audiobox 96", "audio box": "audiobox 96",
        "presonus": "audiobox 96", "personas audiobox": "audiobox 96",
        "drum kit": "yamaha dtx400k", "e drums": "yamaha dtx400k",
        "edrums": "yamaha dtx400k", "electronic drums": "yamaha dtx400k",
        "electric drums": "yamaha dtx400k", "dtx": "yamaha dtx400k",
        "mixer": "yamaha emx66m", "powered mixer": "yamaha emx66m",
        "pa": "yamaha emx66m", "yamaha mixer": "yamaha emx66m",
        "power amp": "samson servo 300", "samson": "samson servo 300",
        "servo": "samson servo 300",
        "guitar amp": "guitar amps", "amps": "guitar amps",
        "crate": "guitar amps", "epiphone": "guitar amps",
        "electar": "guitar amps",
    }

    def device_ref(self, name: str) -> Path | None:
        name = name.lower().strip()
        for junk in ("my ", "the "):
            if name.startswith(junk):
                name = name[len(junk):]
        name = self.DEVICE_ALIASES.get(name, name)
        if name in self.device_refs:
            return self.device_refs[name]
        best, best_score = None, 0
        for key, path in self.device_refs.items():
            sc = fuzz.partial_ratio(name, key)
            if sc > best_score:
                best, best_score = path, sc
        return best if best_score >= 75 else None
