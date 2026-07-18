"""Sample-pack library (owner directive 2026-07-18: "You're not working
with very many sounds. That's why everything sounds the same.").

Scans the pack roots listed in <project>/sample_packs.json and buckets
every usable ONE-SHOT into the engine's drum roles. Unlike the old
name-token-only scan, this reads the pack's own organization: a file
inside "KICKS/" is a kick no matter what it's called — which is exactly
what the old bucketing missed (most pack sounds never say "kick" in the
file name).

Rules (owner's):
- one-shots only — NO loops (loop tokens, bpm-in-name, Loops/Fills/
  Stems folders, and anything longer than the duration gate are out);
- drums, percussion, and fx only — no instruments (Bass/Melodic/Keys/
  Synth/Chords/Vocals/MIDI/patch-preset folders are skipped; 808s ARE
  kicks and stay);
- extensible: drop new packs into any listed root (or add a new root
  path to sample_packs.json) and the next Beat Machine launch picks
  them up. An unplugged drive falls back to the last successful scan
  (cached in ~/.reason_voice/pack_index.json).
"""
import json
import os
import re
import sys
import wave
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

PACKS_CONFIG = Path(__file__).resolve().parent.parent / "sample_packs.json"
CACHE = Path(os.path.expanduser("~/.reason_voice/pack_index.json"))

DEFAULT_ROOTS = [
    "/Volumes/TBOTC 3/DAW Projects/Sample Packs - Downloads Backup",
    "/Volumes/TBOTC 3/Sample Packs/2022 sample packs",
]

AUDIO_EXTS = {".wav", ".aif", ".aiff"}      # what load_audio can read
MAX_SECS = {"crash": 10.0, "fx": 10.0}      # generous for cymbals/fx
MAX_SECS_DEFAULT = 6.0                       # anything longer = not a one-shot

# Folder-name vocabulary -> engine role. Ordered: first match wins, so
# "808S" beats the generic "DRUMS", "OPEN HATS" beats "HATS".
DIR_ROLES = [
    ("kick", ("808", "KICK", "BD", "BOOM")),
    ("snare", ("SNARE", "SD")),
    ("clap", ("CLAP",)),
    ("snap", ("SNAP", "FINGER")),
    ("rim", ("RIM", "SIDESTICK", "STICK", "CLICK")),
    ("hat", ("HIHAT", "HI HAT", "HI-HAT", "HH", "OH", "OPEN HAT",
             "CLOSED HAT", "HAT", "RIDE")),
    ("crash", ("CRASH", "CYMBAL", "SPLASH", "CHINA")),
    ("bongo", ("BONGO", "CONGA")),
    ("perc", ("PERC", "TOM", "SHAKER", "TAMB", "COWBELL", "BLOCK",
              "CLAVE", "TABLA", "TIMBALE")),
    ("fx", ("FX", "SFX", "IMPACT", "RISER", "SWEEP", "WHOOSH", "FOLEY",
            "TEXTURE", "WHITE NOISE", "NOISE", "REVERSE", "SCRATCH",
            "TRANSITION", "DOWNLIFTER", "UPLIFTER", "AMBIEN")),
]

# folders whose contents are never wanted (instruments, loops, project
# files) — checked on every ancestor directory name
EXCLUDE_DIR_WORDS = ("LOOP", "STEM", "FILL", "MIDI", "PATCH", "PRESET",
                     "BASS", "MELOD", "CHORD", "SYNTH", "KEY", "PIANO",
                     "GUITAR", "VOCAL", "VOX", "ACAPELLA", "INSTRUMENT",
                     "SERUM", "MASSIVE", "PROJECT", "DEMO SONG",
                     "CONSTRUCTION")

# file-level loop signals (a loop misfiled in a one-shot folder)
LOOP_FILE_RE = re.compile(r"loop|(?:^|[^a-z0-9])\d{2,3}\s?bpm", re.I)

# filename tokens -> extra roles (a "Rimshot" in PERCUSSION is rim too)
from make_drum_beats import SHOT_WORDS                      # noqa: E402
TOKEN_RE = re.compile(r"[a-z0-9]+")


def load_roots():
    if not PACKS_CONFIG.exists():
        PACKS_CONFIG.write_text(json.dumps({
            "_readme": [
                "Sample-pack roots for the Beat Machine. Add a folder "
                "path to \"roots\" (or drop new packs inside an existing "
                "root) and the next launch picks it up.",
                "One-shots only: loops, MIDI, presets, and instrument "
                "folders (bass/melodic/keys/vocals) are skipped "
                "automatically."],
            "roots": DEFAULT_ROOTS}, indent=1))
    try:
        return json.loads(PACKS_CONFIG.read_text()).get("roots", [])
    except (OSError, json.JSONDecodeError):
        return DEFAULT_ROOTS


def _dir_role(rel_parts):
    """Role from the nearest classifying ancestor folder, or None."""
    for part in reversed(rel_parts[:-1]):
        up = part.upper()
        for role, words in DIR_ROLES:
            if any(w in up for w in words):
                return role
    return None


def _excluded(rel_parts):
    return any(w in part.upper()
               for part in rel_parts[:-1] for w in EXCLUDE_DIR_WORDS)


def _wav_secs(path):
    """Cheap duration from the header; None when unreadable."""
    try:
        if path.suffix.lower() == ".wav":
            with wave.open(str(path), "rb") as f:
                return f.getnframes() / max(f.getframerate(), 1)
        import aifc
        import contextlib
        with contextlib.closing(aifc.open(str(path), "rb")) as f:
            return f.getnframes() / max(f.getframerate(), 1)
    except Exception:
        return None


def _load_cache():
    try:
        return json.loads(CACHE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def scan_packs(roots=None):
    """Walk the pack roots -> {role: [entry, ...]}. Entries match the
    indexer's shape so the pickers use them unchanged. Durations are
    cached per (path, size), so only files added since the last scan
    pay the header-read cost — a fresh pack shows up in seconds."""
    roots = roots if roots is not None else load_roots()
    cache = _load_cache()
    durs = cache.get("_durations", {})
    shots = {}
    seen_any = False
    for root in roots:
        rootp = Path(os.path.expanduser(root))
        if not rootp.exists():
            continue
        seen_any = True
        for path in rootp.rglob("*"):
            if path.suffix.lower() not in AUDIO_EXTS or not path.is_file():
                continue
            rel = path.relative_to(rootp).parts
            if _excluded(rel) or LOOP_FILE_RE.search(path.name):
                continue
            role = _dir_role(rel)
            toks = TOKEN_RE.findall(" ".join(rel).lower())
            tokset = set(toks)
            roles = set()
            if role:
                roles.add(role)
            for r, words in SHOT_WORDS:            # filename can add roles
                if tokset & words:
                    roles.add(r)
            if not roles:
                continue                            # unclassifiable: skip
            key = "%s|%d" % (path, path.stat().st_size)
            secs = durs.get(key)
            if secs is None:
                secs = _wav_secs(path)
                if secs is None:
                    continue
                durs[key] = round(secs, 3)
            entry = {"name": path.stem, "path": str(path),
                     "kind": "sample", "category": "one-shot",
                     "tokens": sorted(tokset)}
            for r in roles:
                if secs <= MAX_SECS.get(r, MAX_SECS_DEFAULT):
                    shots.setdefault(r, []).append(entry)
    if seen_any:
        try:
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            out = dict(shots)
            out["_durations"] = durs
            CACHE.write_text(json.dumps(out))
        except OSError:
            pass
    else:                                           # drive unplugged
        cached = _load_cache()
        cached.pop("_durations", None)
        return cached
    return shots


def merge_into(shots, pack_shots=None):
    """Add pack sounds to a build_shots() dict, deduped by path."""
    pack_shots = pack_shots if pack_shots is not None else scan_packs()
    for role, entries in pack_shots.items():
        have = {e["path"] for e in shots.get(role, [])}
        for e in entries:
            if e["path"] not in have:
                shots.setdefault(role, []).append(e)
                have.add(e["path"])
    return shots


if __name__ == "__main__":
    got = scan_packs()
    total = {id(e) for es in got.values() for e in es}
    print("pack one-shots by role:")
    for role in sorted(got, key=lambda r: -len(got[r])):
        print("  %-6s %5d" % (role, len(got[role])))
    print("unique files:", len({e["path"] for es in got.values()
                                for e in es}))
