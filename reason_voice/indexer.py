"""Scan patch + sample folders and build a searchable index.

Covers filesystem patches and loose audio (your own saves, third-party sound
packs, extracted ReFill content, sample libraries). The Factory Sound Bank is
a sealed archive Reason reads internally — it cannot be indexed. Voice
next/prev patch still works on it via the Remote codec.

Samples (.wav/.aiff/.rx2…) are classified on the way in: loop vs one-shot,
plus an instrument group (drums, bass, keys…) so "find drum loops" browses
them in bins.
"""
import json
import os
import re
import time
from pathlib import Path

# Reason patch formats -> device family (used as implicit tags)
PATCH_EXTENSIONS = {
    ".cmb": "combinator",
    ".zyp": "subtractor synth",
    ".thor": "thor synth",
    ".xwv": "malstrom synth",
    ".sxt": "nnxt sampler",
    ".smp": "nn19 sampler",
    ".drp": "redrum drums",
    ".kong": "kong drums",
    ".drex": "dr octo rex loop player",
    ".repatch": "rack-extension",
    ".rv7": "rv7000 reverb fx",
    ".sm4": "scream fx",
    ".grain": "grain synth",
}

# Loose audio Reason can use directly (drag in, or load into samplers/players)
SAMPLE_EXTENSIONS = {".wav", ".aif", ".aiff", ".rx2", ".rex", ".rcy"}
REX_EXTENSIONS = {".rx2", ".rex", ".rcy"}   # sliced loops by definition

# Folder names that are never sample libraries (Music.app media, GarageBand…)
EXCLUDE_DIR_NAMES = {"iTunes", "Media.localized", "GarageBand",
                     "Audio Music Apps", ".venv", "Backups"}

LOOP_TOKENS = {"loop", "loops", "break", "breaks", "groove", "grooves"}
# underscore is a \w char, so \b won't fire in "_90bpm" — match separators explicitly
BPM_RE = re.compile(r"(?:^|[^a-z0-9])(\d{2,3})\s?bpm(?:$|[^a-z0-9])")

INDEX_VERSION = 2   # bump to force a one-time rebuild after schema changes


def extract_bpm(filename: str):
    m = BPM_RE.search(filename.lower())
    if m:
        bpm = int(m.group(1))
        if 40 <= bpm <= 220:
            return bpm
    return None

# First group whose keywords appear in the tokens wins; order = specificity.
SAMPLE_GROUPS = [
    ("drums", {"kick", "kicks", "snare", "snares", "hat", "hats", "hihat",
               "hihats", "cymbal", "cymbals", "clap", "claps", "perc",
               "percussion", "tom", "toms", "drum", "drums", "break",
               "breaks", "beat", "beats", "ride", "crash", "shaker",
               "tambourine", "rim", "snap", "snaps", "conga", "bongo"}),
    ("bass", {"bass", "sub", "808", "reese", "bassline", "basslines"}),
    ("vocal", {"vocal", "vocals", "vox", "voice", "choir", "acapella",
               "acappella", "adlib", "adlibs", "phrase", "chant"}),
    ("keys", {"piano", "keys", "rhodes", "epiano", "organ", "wurli",
              "wurlitzer", "clav", "chord", "chords", "mallet", "bell",
              "bells", "glockenspiel", "glock", "vibes", "marimba",
              "xylophone", "celesta"}),
    ("orchestral", {"violin", "viola", "cello", "strings", "ensemble",
                    "orchestra", "orchestral", "flute", "oboe", "clarinet",
                    "bassoon", "trumpet", "horn", "brass", "sax",
                    "saxophone", "trombone", "harp"}),
    ("guitar", {"guitar", "guitars", "gtr", "strat", "riff", "riffs",
                "acoustic", "banjo", "ukulele"}),
    ("fx", {"fx", "riser", "risers", "sweep", "sweeps", "impact", "impacts",
            "whoosh", "foley", "ambience", "atmosphere", "noise", "vinyl",
            "texture", "textures", "downlifter", "uplifter"}),
    ("synth", {"synth", "synths", "lead", "leads", "pad", "pads", "arp",
               "arps", "pluck", "plucks", "stab", "stabs", "melody",
               "melodic", "sequence"}),
]

TOKEN_RE = re.compile(r"[a-z0-9]+")
STOP = {"the", "a", "an", "of", "and", "for", "patch", "patches", "sound",
        "sounds", "reason", "refill", "v1", "v2", "01", "02", "1", "2"}


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOP and len(t) > 1]


# Folder names too generic to serve as a browse group on their own
GENERIC_FOLDER_TOKENS = {"sample", "samples", "loop", "loops", "audio",
                         "wav", "aiff", "my", "new", "misc", "stuff",
                         "files", "folder", "untitled", "documents", "music"}


# A folder made only of these words is a container ("Sample Packs", "Loops");
# the folder INSIDE it is the pack name and makes a good browse group.
CONTAINER_TOKENS = {"sample", "samples", "loop", "loops", "sound", "sounds",
                    "pack", "packs", "library", "libraries", "audio"}


def _pack_group(rel_parts):
    parts = rel_parts[:-1]
    for i, part in enumerate(parts[:-1]):
        toks = tokenize(part)
        if toks and all(t in CONTAINER_TOKENS for t in toks):
            nxt = [t for t in tokenize(parts[i + 1])
                   if t not in GENERIC_FOLDER_TOKENS]
            if nxt:
                return " ".join(nxt[:3])
    return None


def _keyword_group(toks: set, ordered: list):
    group = next((g for g, kws in SAMPLE_GROUPS if toks & kws), None)
    if group == "orchestral":
        # a full orchestral library must not become one giant bin —
        # split by the first instrument word that actually appears
        kws = dict(SAMPLE_GROUPS)["orchestral"]
        group = next((t for t in ordered if t in kws), group)
    return group


def folder_label(rel_parts) -> str:
    """Short 'where it lives' label so five files all named '0001 1-Audio'
    (Ableton clip names repeat across projects) stay tellable-apart."""
    parts = [p for p in rel_parts[:-1]
             if not all(t in GENERIC_FOLDER_TOKENS for t in tokenize(p))]
    return "/".join(parts[-2:])


def _folder_group(rel_parts) -> str:
    """Nearest meaningful ancestor folder name — his own organization is the
    best grouping we have for generically-named recordings."""
    for part in reversed(rel_parts[:-1]):
        toks = [t for t in tokenize(part) if t not in GENERIC_FOLDER_TOKENS]
        if toks:
            return " ".join(toks)
    return "other"


def classify_sample(tokens: list[str], ext: str, filename: str, rel_parts=()):
    """-> (category, group) e.g. ("loop", "drums") or ("one-shot", "bass")."""
    toks = set(tokens)
    is_loop = (ext in REX_EXTENSIONS
               or any(t.startswith("loop") for t in toks)   # loop/loops/looper…
               or bool(toks & LOOP_TOKENS)
               or bool(BPM_RE.search(filename.lower())))
    # group preference: instrument word in the FILE name > the sample-pack
    # folder it ships in > instrument word anywhere in the path > nearest
    # meaningful folder. Keeps a 50k-file "…Symphonic Strings…" pack of
    # machine-named zones from swallowing the strings keyword.
    name_ordered = tokenize(filename)
    group = (_keyword_group(set(name_ordered), name_ordered)
             or _pack_group(rel_parts)
             or _keyword_group(toks, list(tokens))
             or _folder_group(rel_parts))
    return ("loop" if is_loop else "one-shot"), group


def bins(entries: list[dict]) -> list[dict]:
    """Sample counts grouped by (group, category) for the browse buttons."""
    counts: dict = {}
    for e in entries:
        if e.get("kind") != "sample":
            continue
        key = (e["group"], e["category"])
        counts[key] = counts.get(key, 0) + 1
    out = []
    for (group, category), n in sorted(counts.items(), key=lambda kv: -kv[1]):
        noun = "loops" if category == "loop" else "samples"
        out.append({
            "label": f"{group} {noun}",
            "query": f"find {group} {noun}",
            "count": n,
        })
    return out[:12]   # sidebar stays scannable; the rest via typed search


def scan(folders: list[str]) -> list[dict]:
    entries = []
    for folder in folders:
        root = Path(os.path.expanduser(folder))
        if not root.exists():
            continue
        for path in root.rglob("*"):
            ext = path.suffix.lower()
            if ext not in PATCH_EXTENSIONS and ext not in SAMPLE_EXTENSIONS:
                continue
            rel_parts = path.relative_to(root).parts
            if EXCLUDE_DIR_NAMES.intersection(rel_parts[:-1]):
                continue
            if not path.is_file():
                continue
            tokens = tokenize(" ".join(rel_parts))
            if ext in PATCH_EXTENSIONS:
                entries.append({
                    "name": path.stem,
                    "path": str(path),
                    "v": INDEX_VERSION,
                    "kind": "patch",
                    "device": PATCH_EXTENSIONS[ext],
                    "tokens": sorted(set(tokens + tokenize(PATCH_EXTENSIONS[ext]))),
                })
            else:
                category, group = classify_sample(tokens, ext, path.name,
                                                  rel_parts)
                extra = ["loop", "loops"] if category == "loop" else \
                        ["sample", "samples", "hit", "oneshot"]
                entry = {
                    "name": path.stem,
                    "path": str(path),
                    "v": INDEX_VERSION,
                    "kind": "sample",
                    "category": category,
                    "group": group,
                    "folder": folder_label(rel_parts),
                    "device": f"{group} {category}",
                    "tokens": sorted(set(tokens + extra + tokenize(group))),
                }
                bpm = extract_bpm(path.name)
                if bpm:
                    entry["bpm"] = bpm
                entries.append(entry)
    return entries


class PatchIndex:
    def __init__(self, cache_path: str = "~/.reason_voice/index.json"):
        self.cache_path = Path(os.path.expanduser(cache_path))
        self.entries: list[dict] = []

    def load_or_build(self, folders: list[str], max_age_hours: float = 24.0) -> int:
        if self.load_cached(max_age_hours) == "fresh":
            return len(self.entries)
        return self.rebuild(folders)

    def load_cached(self, max_age_hours: float = 24.0) -> str:
        """Load whatever cache exists without scanning. Returns "fresh",
        "stale" (loaded but due for a background rebuild), or "none"."""
        if not self.cache_path.exists():
            return "none"
        entries = json.loads(self.cache_path.read_text())
        # older cache formats get rebuilt once
        if entries and entries[0].get("v") != INDEX_VERSION:
            return "none"
        self.entries = entries
        age = (time.time() - self.cache_path.stat().st_mtime) / 3600
        if self.entries and age < max_age_hours:
            return "fresh"
        return "stale" if self.entries else "none"

    def rebuild(self, folders: list[str]) -> int:
        fresh = scan(folders)
        # an unplugged drive must not wipe its library from the index —
        # keep the cached entries for any folder that isn't mounted
        for folder in folders:
            root = os.path.expanduser(folder)
            if not Path(root).exists():
                fresh += [e for e in self.entries
                          if e["path"].startswith(root + os.sep)
                          and "kind" in e]
        self.entries = fresh
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self.entries))
        return len(self.entries)
