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
    "/Volumes/TBOTC 3/Sample Packs/Function Loops - Black Friday 2024 Sampler",
    "/Volumes/TBOTC 3/Sample Packs/Live loop cds",
]

AUDIO_EXTS = {".wav", ".aif", ".aiff"}      # what load_audio can read
MAX_SECS = {"crash": 10.0, "fx": 10.0}      # (legacy) per-role one-shot caps
MAX_SECS_DEFAULT = 6.0                       # (legacy) kept for reference
# owner 2026-07-23 "stop the one-shot rule": the per-role caps above no
# longer gate scanning. This single ceiling only rejects full-length
# songs/mixes masquerading as samples — loops, phrases, and long 808s pass.
SANITY_SECS = 45.0

# Folder-name vocabulary -> engine role. Ordered: first match wins, so
# "808S" beats the generic "DRUMS", "OPEN HATS" beats "HATS".
DIR_ROLES = [
    # "808" left the kick tuple 2026-09-07 (owner: "the 808, the kick drum
    # and chords should all have their own separate lanes"). It is on the
    # BASS entry below now. The old rule was "an 808 IS a kick", which put
    # all 411 files of his 808s folder into the kick pool alongside 283
    # real kicks -- over half of every DJ's kick picks were sustained bass
    # tones. Same change in make_drum_beats.SHOT_WORDS for the filename path.
    ("kick", ("KICK", "BD", "BOOM")),
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
    # phase 2 (owner 2026-07-23): bass + vocals are in now.
    ("bass", ("808", "BASS", "SUB", "REESE", "BASSLINE")),
    ("vox", ("VOCAL", "VOX", "ACAPELLA", "ACAPPELLA", "ADLIB", "CHANT",
             "VOICE", "CHOIR")),
    ("fx", ("FX", "SFX", "IMPACT", "RISER", "SWEEP", "WHOOSH", "FOLEY",
            "TEXTURE", "WHITE NOISE", "NOISE", "REVERSE", "SCRATCH",
            "TRANSITION", "DOWNLIFTER", "UPLIFTER", "AMBIEN")),
]

# folders whose contents are never wanted — checked on every ancestor dir.
# Owner 2026-07-23 "stop the one-shot rule": LOOP + FILL dropped (loops are
# allowed) and BASS/VOCAL/VOX/ACAPELLA dropped (those are roles now, above).
# Still excluded: melodic/instrument content (handled by the separate
# melodic-loop scanner, not the drum pool), and non-audio project junk.
EXCLUDE_DIR_WORDS = ("STEM", "MIDI", "PATCH", "PRESET",
                     "MELOD", "CHORD", "SYNTH", "KEY", "PIANO",
                     "GUITAR", "INSTRUMENT",
                     "SERUM", "MASSIVE", "PROJECT", "DEMO SONG",
                     "CONSTRUCTION",
                     # OWNER 2026-08-03: "There are a lot of nature sounds.
                     # I think they're from the cymatics folder. It's, like,
                     # water and things of that nature. Remove those from
                     # the sound pool." He chose to drop the WHOLE pack.
                     # It was 172 files — a THIRD of the entire fx pool —
                     # and it is field recordings end to end: Rain (54),
                     # Vinyl Crackles (32), Rivers and Streams (28),
                     # Walking (28), Waterfall (7) and a "Various" folder
                     # of car AC, a generator, and a car driving over a
                     # metal bridge. None of it is a drum or an fx stab.
                     # Vinyl Crackles went too because clean_renders
                     # already keeps vinyl and dust out of a render so he
                     # can add his own colour in Reason.
                     "AMBIENT RECORDING")

# Individual field-recording FILES scattered through other packs — the same
# category as the pack above, but without a folder to catch them by. Matched
# as whole words against the file name so "Rainbow" or "Windup" can't trip
# them. Deliberately narrow: only sounds of weather, water and wildlife, not
# anything that could be a usable texture or an impact.
NATURE_FILE_WORDS = ("RAIN", "RIVER", "STREAM", "WATERFALL", "OCEAN",
                     "FOREST", "BIRDS", "THUNDER", "CRICKETS", "SEAGULL",
                     "WAVES", "CREEK", "BROOK")

# file-level loop signals (a loop misfiled in a one-shot folder)
LOOP_FILE_RE = re.compile(r"loop|(?:^|[^a-z0-9])\d{2,3}\s?bpm", re.I)
# a file whose NAME marks it a loop (owner 2026-07-23: play these as full
# loops, not choked hits). Same signal, named for the new use.
_LOOP_NAME_RE = LOOP_FILE_RE
_BPM_RE = re.compile(r"(?:^|[^0-9])(\d{2,3})(?=\s?bpm|[^0-9]|$)", re.I)


# a loop is TONAL (melodic — belongs to the in-key chord feature, not the
# untuned loop lane) if its name carries a musical key or a melodic word. The
# key form requires an accidental or an explicit maj/min so a bare version
# letter ("..._E Hat Loop") isn't mistaken for the key of E.
_MELODIC_WORDS = {"synth", "lead", "melody", "melodic", "chord", "chords",
                  "pad", "pads", "pluck", "harmony", "arp", "keys", "piano",
                  "guitar", "sax", "bass", "reese", "string", "strings",
                  "brass", "flute", "vocal", "vox"}
_KEYISH_RE = re.compile(r"^[a-g]((#|b)(m|maj|min)?|(m|maj|min))$", re.I)
_SEP_RE = re.compile(r"[\s_\-]+")


def _tonal(name):
    parts = _SEP_RE.split(name.lower())
    return any(p in _MELODIC_WORDS or _KEYISH_RE.match(p) for p in parts)


def _bpm_from_tokens(tokens):
    """A plausible loop BPM from name tokens, or None. Catches both a bare
    '92' token and a glued '140bpm'. Range-gated so a bass name like '808'
    isn't read as a tempo."""
    for t in tokens:
        if t.isdigit() and len(t) in (2, 3):
            n = int(t)
        else:
            m = re.match(r"^(\d{2,3})bpm$", t)
            if not m:
                continue
            n = int(m.group(1))
        if 60 <= n <= 200:
            return n
    return None

# filename tokens -> extra roles (a "Rimshot" in PERCUSSION is rim too)
from make_drum_beats import SHOT_WORDS                      # noqa: E402
TOKEN_RE = re.compile(r"[a-z0-9]+")


def sorted_root():
    """The one folder the OWNER sorts himself, where the FOLDER NAME says
    what a sample is and what it is like — "Kicks/Hard", "Snares/Brushes".

    Owner 2026-09-06, after the horns correction and the vocal/vox miss:
    "make folders where I could just load the samples that I know are all
    drum type samples into and you would know how to look there... so you
    would know what you're looking at regardless of the name."

    Two layers, and only the second one is new:
    * WHAT IT IS (kick vs snare vs vox) already came from the folder —
      see DIR_ROLES. A file called xz9_final_v2.wav in a Kicks folder has
      always been a kick.
    * WHAT IT IS LIKE (hard, dry, brushes) was filename-only, which is the
      whole reason "big" and "crack" matched nothing and a sidestick got
      picked for a snare. Under THIS root, taste words are read from the
      folder path too (crew._pick_path).

    Scoped to this root ON PURPOSE. His existing packs keep filename-only
    taste matching, so no pick he has already approved by ear can move —
    measured 2026-09-06 over 203 lanes across all 41 presets: zero moved,
    zero lost. Widening it to every pack was tried first and rejected:
    pack folders carry words like "Hard" and "Trap", which would have
    changed the nine (Otto Grit's snare pool 15 -> 38) without him
    hearing it first.

    Empty string when unset — the feature is simply off."""
    try:
        v = json.loads(PACKS_CONFIG.read_text()).get("sorted_root") or ""
    except (OSError, json.JSONDecodeError):
        return ""
    return str(v).rstrip("/").lower()


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
        cfg = json.loads(PACKS_CONFIG.read_text())
    except (OSError, json.JSONDecodeError):
        return DEFAULT_ROOTS
    roots = list(cfg.get("roots", []))
    # the sorted root is scanned like any other pack — being listed here is
    # what puts its samples in the pool at all; sorted_root() above is only
    # about how their TASTE words are read.
    sr = cfg.get("sorted_root")
    if sr and not any(str(sr).rstrip("/").lower() == str(r).rstrip("/").lower()
                      for r in roots):
        roots.append(sr)
    return roots


def _dir_role(rel_parts):
    """Role from the nearest classifying ancestor folder, or None."""
    for part in reversed(rel_parts[:-1]):
        up = part.upper()
        for role, words in DIR_ROLES:
            if any(w in up for w in words):
                return role
    return None


def _is_nature(name):
    """A field recording of weather/water/wildlife, by file name. Whole-word
    match so 'Rainbow', 'Windup' and 'Streamline' are safe."""
    words = set(re.split(r"[^A-Za-z]+", name.upper()))
    return bool(words & set(NATURE_FILE_WORDS))


def _excluded(rel_parts):
    if any(w in part.upper()
           for part in rel_parts[:-1] for w in EXCLUDE_DIR_WORDS):
        return True
    # ...and the stragglers in packs that have no ambient folder of their own
    return _is_nature(rel_parts[-1]) if rel_parts else False


# Where the soundfile fallback in _wav_secs is allowed to run. Owner
# 2026-09-07: "808s only for now". See _wav_secs for what it fixes and
# what widening this would do.
_FLOAT_WAV_DIRS = ("/808s/",)


def _wav_secs(path):
    """Cheap duration from the header; None when unreadable.

    THE FLOAT-WAV HOLE (found 2026-09-07): `wave` and `aifc` only read
    PCM. A float32 WAV — same .wav suffix, indistinguishable in Finder,
    plays fine in Reason — raises here, gets swallowed, and the file is
    dropped from the sample pool entirely with no message. Measured over
    the sorted root: 1,950 of 3,717 files invisible, including 289 of the
    411 808s and all 40 Stomps.

    `soundfile` reads them and is already a dependency (every actual
    audio load in this project goes through it), so the fallback costs
    nothing but a slower open on files the fast path rejects.

    SCOPED to _FLOAT_WAV_DIRS on the owner's call, because recovering a
    lane's files roughly doubles its pool and so changes which sample a
    DJ picks on a re-render — he wants to hear each lane before it moves.
    To widen it: add the folder to _FLOAT_WAV_DIRS, or drop the check for
    all lanes at once."""
    try:
        if path.suffix.lower() == ".wav":
            with wave.open(str(path), "rb") as f:
                return f.getnframes() / max(f.getframerate(), 1)
        import aifc
        import contextlib
        with contextlib.closing(aifc.open(str(path), "rb")) as f:
            return f.getnframes() / max(f.getframerate(), 1)
    except Exception:
        pass
    sp = str(path).replace(os.sep, "/")
    if not any(d.lower() in sp.lower() for d in _FLOAT_WAV_DIRS):
        return None
    try:
        import soundfile as sf
        info = sf.info(str(path))
        return info.frames / max(info.samplerate, 1)
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
            # owner 2026-07-23 "stop the one-shot rule": loops are kept now
            # (the LOOP_FILE_RE skip is gone). _excluded still drops the
            # instrument/project folders listed in EXCLUDE_DIR_WORDS.
            if _excluded(rel):
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
            # owner 2026-07-23: a LOOP is played as a full loop (its own
            # lane), not choked into a drum hit — so it goes to the "_loops"
            # bucket with its bpm (for tempo-matching), NOT the choked role
            # pools. A loop is a file in a LOOP folder or with a loop/bpm
            # name. Everything else stays a one-shot for the drum lanes.
            is_loop = bool(_LOOP_NAME_RE.search(path.name)) \
                or any("LOOP" in p.upper() for p in rel[:-1])
            if is_loop:
                shots.setdefault("_loops", []).append(
                    {"name": path.stem, "path": str(path),
                     "kind": "loop", "category": "loop",
                     "role": (role or next(iter(roles))),
                     "bpm": _bpm_from_tokens(toks), "secs": round(secs, 3),
                     "tonal": _tonal(path.stem), "tokens": sorted(tokset)})
                continue
            entry = {"name": path.stem, "path": str(path),
                     "kind": "sample", "category": "one-shot",
                     "tokens": sorted(tokset)}
            for r in roles:
                # owner 2026-07-23 "stop the one-shot rule": no per-role
                # length cap any more — long tails (long 808s, cymbals) are
                # welcome. SANITY_SECS only keeps a full-length song from
                # posing as a one-shot; playback still chokes each hit.
                if secs <= SANITY_SECS:
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
