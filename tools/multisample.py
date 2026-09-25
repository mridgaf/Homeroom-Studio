"""Note-by-note (multisampled) instruments: VCSL + VSCO 2 CE, both CC0,
in their own folder on the drive (owner 2026-09-24).

Why this exists: the owner wants instruments "with their variety of notes
so I don't have to stretch or pitch any sounds". His own banks are mostly
loops, so instrument_sampler.py has to GUESS a pitch by ear and may stretch
a note up to 12 semitones. These libraries record an instrument note by
note and put the note name in every file name ("Oboe_Vib_F5_v3_Main.wav"),
so the note comes from the name, not a guess.

His wiring decisions (2026-09-24, clickable, all BLOCKING-asked):
  - these play FIRST for their family; his own samples are the fallback
  - EXCEPT strings: London Symphonic Strings stays first. VSCO's strings
    are a BACKUP, behind everything else in the "string" group
  - thumb pianos / mbiras / kalimbas + psaltery -> bell (his synth plucks
    stay first for "pluck")
  - harps, Dan Tranh, Strumstick -> guitar
  - harpsichords -> piano; the TX81Z FM sounds -> synth
  - recorders, ocarinas, sax, saxello + VSCO woodwinds -> wood;
    harmonicas LEFT OUT

THE OCTAVE TRAP (measured 2026-09-24, not assumed): most of these file
names use the "middle C = C3" convention, so the name reads ONE OCTAVE LOW.
Not all of them: Steinway B, Pipe Organ, Concert Harp, FM Piano, Tubular
Bells 2, VSCO Upright Nr1, VSCO Harp and Solo Violin are named at true
pitch; Tubular Glockenspiel is off by five octaves; a Renaissance Organ
stop sounds two octaves up. Trusting the names would have played most of
the library an octave off. So:
  - the NAME gives the note (exact pitch class, no guessing), and
  - the OCTAVE is measured: a handful of files per folder are run through
    instrument_sampler.detect_pitch, and the folder takes the octave its
    readings agree on. A folder whose readings don't match its names'
    notes at all (Bell Tree: unpitched) is left out rather than guessed.
Measured on 135 files pulled from GitHub, two per instrument: detect_pitch
and librosa's pyin agree on every offset above.

    ./.venv/bin/python tools/multisample.py      # coverage report
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from sample_library import AUDIO_EXTS, PACKS_CONFIG           # noqa: E402

DEFAULT_ROOT = ("/Volumes/TBOTC 3/Sample Packs/"
                "BOTC Multisampled Instruments")
CACHE = Path(os.path.expanduser("~/.reason_voice/multisample_index.json"))
CACHE_VERSION = 1

# Instrument FOLDER name (lowercased, anywhere in the path) -> group.
# Folder, not file name: the file names are vendor shorthand ("UR1",
# "GPiano", "BrettTenor") and the folder is the vendor's own label for the
# instrument. Anything not listed here is not indexed — drums, FX, the
# harmonicas, whistles, siren, didgeridoo, Bell Tree.
FAMILIES = {
    # piano (VSCO "Upright Piano" uses numbered files + a mapping chart,
    # so it has no note in its names and is skipped until that's read)
    "grand piano, kawai": "piano",
    "grand piano, kawai - legacy": "piano",
    "grand piano, steinway b": "piano",
    "upright piano, knight": "piano",
    "upright piano, yamaha": "piano",
    "upright nr1": "piano",
    "harpsichord, english": "piano",
    "harpsichord, flemish": "piano",
    "harpsichord, french": "piano",
    "harpsichord, italian": "piano",
    "harpsichord, unk": "piano",
    # synth (owner: the TX81Z FM keyboards are synth, not piano)
    "fm piano": "synth",
    "piano 1": "synth",
    "clavisynth": "synth",
    # organ (VSCO's organ is numbered files -> skipped, same as its piano)
    "pipe organ": "organ",
    "renaissance organ": "organ",
    # bell
    "glockenspiel": "bell",
    "glock": "bell",
    "hand chimes": "bell",
    "marimba": "bell",
    "xylophone": "bell",
    "xylo": "bell",
    "vibraphone": "bell",
    "balafon": "bell",
    "wine glasses": "bell",
    "tubular bells 1": "bell",
    "tubular bells 2": "bell",
    "tubular bells 3 - legacy": "bell",
    "tubular glockenspiel": "bell",
    "kalimba, kenya": "bell",
    "kalimba, tanzania": "bell",
    "mbira mavembe (gandanga), zimbabwe, low g": "bell",
    "mbira dzavadzimu nyamaropa, zimbabwe, low b": "bell",
    "nyunga nyunga, mozambique, low f": "bell",
    "psaltery, bowed and plucked": "bell",
    # guitar (owner: harps, zither and strumstick are plucked strings)
    "concert harp": "guitar",
    "folk harp": "guitar",
    "harp": "guitar",
    "dan tranh": "guitar",
    "strumstick": "guitar",
    # brass
    "f horn": "brass",
    "oldtrombone": "brass",
    "tenor trombone": "brass",
    "trumpet": "brass",
    "tuba": "brass",
    # wood (harmonicas deliberately absent — owner)
    "baroque alto recorder": "wood",
    "baroque bass recorder": "wood",
    "baroque soprano recorder": "wood",
    "baroque tenor recorder": "wood",
    "ocarina, small": "wood",
    "ocarina, typical": "wood",
    "saxello": "wood",
    "tenor saxophone": "wood",
    "bassoon": "wood",
    "clarinet": "wood",
    "flute": "wood",
    "oboe": "wood",
    "piccolo": "wood",
    # strings: BACKUP only (London stays first — owner)
    "cello section": "string",
    "solo contrabass": "string",
    "solo violin": "string",
    "viola section": "string",
    "violin section": "string",
}
BACKUP_GROUPS = {"string"}

# Path/file tokens that mark a sample that isn't a playable held-or-struck
# note: release tails, key/pedal noise, falls, slides, effects.
SKIP_TOKENS = {"rel", "release", "releases", "noise", "noises", "fall",
               "falls", "buzz", "gliss", "glissando", "glide", "sfx", "fx",
               "flutter"}
# Checked only BELOW the instrument folder. "Pedal" is NOT skipped: in this
# library it is the pipe organ's pedal stop (real low notes), not noise.

NOTE_LO, NOTE_HI = 21, 108
# How close a measured pitch must sit to "name + whole octaves" to count
# as agreeing. The note itself comes from the name; this only has to tell
# the OCTAVE and reject unpitched junk. Real reads on pitched instruments
# landed up to 0.75 off (glockenspiel, kalimba); Bell Tree read 1.8 and
# 4.3 off and must NOT vote. 1.0 sits between the two.
AGREE = 1.0
VOTES_PER_FOLDER = 6            # files measured per leaf folder
_PC = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
# Upper-case letter only: every pitched file in both libraries writes its
# note that way, and it keeps a dynamic like "f2" (forte, take 2) in
# "KSHarp_A2_f2" from reading as a second note, F2. Measured: the only
# lower-case matches in either library are cymbals/snares and one file.
_NOTE_TOK = re.compile(r"([A-G])([#b]?)(-?\d)")
_SPLIT = re.compile(r"[\s_]+")
# loudness-layer tokens, softest first
_DYN = ["ppp", "pp", "p", "mp", "mf", "f", "ff", "fff"]
_DYN_WORDS = {"soft": 0.2, "quiet": 0.2, "med": 0.5, "medium": 0.5,
              "loud": 0.8, "hard": 0.8}


def root():
    try:
        cfg = json.loads(PACKS_CONFIG.read_text())
    except (OSError, ValueError):
        cfg = {}
    return cfg.get("multisample_root") or DEFAULT_ROOT


def named_note(stem):
    """The note the FILE NAME says (scientific numbering, C4 = 60), or
    None. Exactly one note-shaped token must be present: a name with two
    ("…_C4_to_D4") is a slide, and a name with none is a numbered file."""
    got = set()
    for tok in _SPLIT.split(stem):
        m = _NOTE_TOK.fullmatch(tok)
        if m:
            acc = {"#": 1, "b": -1}.get(m.group(2), 0)
            got.add(_PC[m.group(1).lower()] + acc + 12 * (int(m.group(3)) + 1))
    return got.pop() if len(got) == 1 else None


def layer_of(stem):
    """0..1 loudness of a file's layer, 0.5 when the name doesn't say.
    Only used to pick ONE layer per beat, so a chord's notes all come
    from the same dynamic."""
    toks = [t.lower() for t in re.split(r"[\s_\-]+", stem) if t]
    for t in toks:
        if t in _DYN:
            return round(_DYN.index(t) / (len(_DYN) - 1), 3)
        if t in _DYN_WORDS:
            return _DYN_WORDS[t]
    for t in toks:
        m = re.fullmatch(r"(?:v|vl|dyn)(\d)", t)
        if m:
            return min(int(m.group(1)), 9) / 10.0
    return 0.5


def _instrument(rel_parts):
    """(index of the instrument folder, group) — the DEEPEST path part
    that names one (VSCO "Strings/Harp": "harp" is the instrument, not
    "strings"), or (None, None)."""
    for i in range(len(rel_parts) - 2, -1, -1):
        g = FAMILIES.get(rel_parts[i].lower())
        if g:
            return i, g
    return None, None


def _raw_entries(rootp):
    out = []
    for path in sorted(rootp.rglob("*")):
        if path.suffix.lower() not in AUDIO_EXTS or not path.is_file():
            continue
        if path.name.startswith("._"):          # macOS resource forks
            continue
        parts = path.relative_to(rootp).parts
        i, group = _instrument(parts)
        if group is None:
            continue
        below = [p.lower() for p in parts[i + 1:-1]]
        toks = {t for p in below + [path.stem.lower()]
                for t in re.split(r"[^a-z0-9#]+", p) if t}
        if toks & SKIP_TOKENS:
            continue
        note = named_note(path.stem)
        if note is None:
            continue
        out.append({"path": str(path), "name": path.stem,
                    "named": note, "group": group,
                    "multi": "/".join(parts[:i + 1]),
                    "art": "/".join(parts[i + 1:-1]) or "-",
                    "layer": layer_of(path.stem)})
    return out


def _measure(path):
    """Measured MIDI pitch of a file's attack, or None (detect_pitch is
    the same reader his own instrument samples go through)."""
    from instrument_sampler import MIN_CLARITY, detect_pitch
    from make_hiphop_tracks import load_audio
    x = load_audio(path)
    if x is None:
        return None
    mono = x.mean(axis=1) if x.ndim == 2 else x
    midi, clarity = detect_pitch(mono)
    return midi if midi is not None and clarity >= MIN_CLARITY else None


def octave_vote(offsets):
    """The whole-octave correction a folder's readings agree on, or None.
    `offsets` are measured-minus-named semitones (None = no reading).
    A reading counts only if it lands within AGREE of a whole octave;
    the winner needs two votes and a clear majority of the counted ones."""
    votes = {}
    for d in offsets:
        if d is None:
            continue
        k = int(round(d / 12.0))
        if abs(d - 12 * k) <= AGREE:
            votes[k] = votes.get(k, 0) + 1
    if not votes:
        return None
    k, n = max(votes.items(), key=lambda kv: kv[1])
    if n < 2 or n < 0.6 * sum(votes.values()):
        return None
    return 12 * k


# Files measured for the vote are drawn from these NAMED notes when the
# folder has them: detect_pitch hears 55-1200 Hz, and a name here lands in
# that window even when the true pitch is an octave or two up. Measured: a
# xylophone's top notes read 7-24 semitones off, its middle notes exact.
VOTE_LO, VOTE_HI = 36, 74


def _spread(entries, n):
    """Up to n entries spread across the folder's notes (low to high),
    so one octave-slipped extreme can't carry the vote. Mid-range notes
    first (VOTE_LO..VOTE_HI) when there are at least two."""
    mid = [e for e in entries if VOTE_LO <= e["named"] <= VOTE_HI]
    es = sorted(mid if len(mid) >= 2 else entries,
                key=lambda e: (e["named"], e["path"]))
    if len(es) <= n:
        return es
    return [es[round(i * (len(es) - 1) / (n - 1))] for i in range(n)]


def scan(root_dir=None, measure=_measure, status=None):
    """Every playable note sample, true pitch in "note". Octave votes are
    cached per (folder, file count), so after the first run the drive is
    only walked, never re-read. Falls back to the last good scan when the
    drive is unplugged, same contract as string_sampler.scan."""
    rootp = Path(os.path.expanduser(root_dir or root()))
    try:
        cache = json.loads(CACHE.read_text())
        if cache.get("version") != CACHE_VERSION:
            cache = {}
    except (OSError, ValueError):
        cache = {}
    if not rootp.exists():
        return cache.get("index", [])
    raw = _raw_entries(rootp)
    folders = {}
    for e in raw:
        folders.setdefault((e["multi"], e["art"]), []).append(e)
    votes = cache.setdefault("votes", {})
    by_inst = {}
    for (inst, art), es in sorted(folders.items()):
        key = "%s|%s|%d" % (inst, art, len(es))
        if key not in votes:
            if status:
                status("measuring octaves: %s %s" % (inst, art))
            offs = []
            for e in _spread(es, VOTES_PER_FOLDER):
                m = measure(e["path"])
                offs.append(None if m is None else m - e["named"])
            votes[key] = offs
        by_inst.setdefault(inst, []).extend(votes[key])
    found = []
    for (inst, art), es in folders.items():
        key = "%s|%s|%d" % (inst, art, len(es))
        shift = octave_vote(votes[key])
        if shift is None:                    # this stop/articulation's own
            shift = octave_vote(by_inst[inst])   # reads are thin: the
        if shift is None:                    # instrument's, else leave out
            continue
        for e in es:
            note = e["named"] + shift
            if not NOTE_LO <= note <= NOTE_HI:
                continue
            row = dict(e, note=note, clarity=1.0)
            if e["group"] in BACKUP_GROUPS:
                row["backup"] = True
            found.append(row)
    cache["version"] = CACHE_VERSION
    cache["index"] = found
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache))
    except OSError:
        pass
    return found


def one_per_beat(index, rng):
    """Thin `index` so each group offers ONE multisampled instrument, one
    articulation folder and one loudness layer for this beat — one real
    recording per note. His own (non-multi) entries pass through
    untouched. Same "one instrument per stem" rule _one_instrument holds.

    ASSUMING (told to owner 2026-09-24): every instrument in a group is
    equally likely (harpsichord as likely as Steinway within "piano");
    within it, the articulation with more notes is likelier; the layer is
    the one nearest the middle (not the softest or hardest)."""
    own = [e for e in index if not e.get("multi")]
    multi = [e for e in index if e.get("multi")]
    keep = []
    for g in sorted({e["group"] for e in multi}):
        es = [e for e in multi if e["group"] == g]
        insts = sorted({e["multi"] for e in es})
        inst = rng.choice(insts)
        arts = {}
        for e in es:
            if e["multi"] == inst:
                arts.setdefault(e["art"], set()).add(e["note"])
        names = sorted(arts)
        art = rng.choices(names, weights=[len(arts[a]) for a in names])[0]
        mine = [e for e in es if e["multi"] == inst and e["art"] == art]
        layer = min({e["layer"] for e in mine}, key=lambda v: (abs(v - 0.5), v))
        by_note = {}
        for e in sorted(mine, key=lambda e: e["path"]):   # rr1 first
            best = by_note.get(e["note"])
            if best is None or (abs(e["layer"] - layer)
                                < abs(best["layer"] - layer)):
                by_note[e["note"]] = e
        keep.extend(by_note[n] for n in sorted(by_note))
    return own + keep


def _report():
    index = scan(status=lambda m: print("  " + m))
    if not index:
        print("No multisampled instruments found. Is the drive plugged in?")
        return
    by = {}
    for e in index:
        by.setdefault((e["group"], e["multi"]), set()).add(e["note"])
    print("\n%d playable note samples, %d instruments\n"
          % (len(index), len(by)))
    for (g, inst), notes in sorted(by.items()):
        ns = sorted(notes)
        gap = max([b - a for a, b in zip(ns, ns[1:])] or [0])
        print("%-7s %-55s %3d notes  %d..%d  biggest gap %d"
              % (g, inst[-55:], len(ns), ns[0], ns[-1], gap))


if __name__ == "__main__":
    _report()
