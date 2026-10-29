"""Build chord_tables.json from the Chordonomicon dataset (2026-10-29).

Chordonomicon (Kantarelis et al. 2024, arXiv 2410.22046, CC BY-NC 4.0):
666,000 songs as chord symbols, each tagged with its artist's Spotify
genres. This reads it once and writes the small table chord_gen.py plays
from: per STYLE (hip-hop sub-genres matched on those Spotify tags) and per
key family (major / minor), the chord loops real songs repeat and how
often, plus which chord follows which.

Every chord is stored TONIC-RELATIVE ([semitones from the tonic,
quality]) the same way progressions_config.json is, so harmony.py can
drop it into any key. The song's tonic comes from a Krumhansl key-finder
run over all its chord tones.

The CSV is 264 MB and lives on the external drive (owner rule 2026-10-29:
anything that can go on the drive goes there). Run it in the background:

    ./.venv/bin/python tools/build_chord_tables.py
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from key_context import CHORDS, MINORISH                    # noqa: E402

SRC = Path("/Volumes/TBOTC 3/Datasets/Chordonomicon/chordonomicon_v2.csv")
OUT = Path(__file__).resolve().parent.parent / "chord_tables.json"

# style -> Spotify genre tags that put a song in it (substring match).
# Claude's grouping of Spotify's tags onto this project's identities.
STYLE_TAGS = {
    "boom_bap": ["boom bap", "east coast hip hop", "hardcore hip hop",
                 "golden age hip hop", "underground hip hop",
                 "conscious hip hop", "queens hip hop", "brooklyn"],
    "jazz_rap": ["jazz rap", "jazz hip hop", "abstract hip hop",
                 "alternative hip hop"],
    "trap": ["trap", "atl hip hop", "southern hip hop", "dirty south",
             "crunk", "rage"],
    "drill": ["drill"],
    "memphis": ["memphis", "phonk", "horrorcore"],
    "gfunk": ["g funk", "west coast", "gangster rap", "chicano rap"],
    "rnb": ["r&b", "neo soul", "urban contemporary", "quiet storm"],
    "soul": ["soul", "motown"],
    "funk": ["funk", "disco", "boogie"],
    "gospel": ["gospel"],
    "lofi": ["lo-fi", "lofi", "chillhop"],
    "emo_rap": ["emo rap", "cloud rap", "sad rap", "plugg"],
    "jazz": ["jazz"],
    "club": ["house", "baltimore club", "miami bass", "bounce",
             "jersey club", "electro", "ghettotech", "footwork"],
    "latin": ["reggaeton", "dancehall", "latin hip hop", "trap latino",
              "dembow"],
    "trip_hop": ["trip hop"],
    "rock": ["rap rock", "rap metal", "nu metal", "alternative rock",
             "grunge"],
}
TOP_LOOPS = 150          # loops kept per style and family
TOP_NEXT = 12            # follow-on chords kept per chord
MIN_SONGS = 150          # a style with fewer songs is left out

PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
# Chordonomicon's quality spellings -> the engine's CHORDS vocabulary
QUAL = {"": "major", "min": "minor", "7": "dom7", "min7": "min7",
        "maj7": "maj7", "dim": "dim", "dim7": "dim", "hdim7": "dim",
        "min7b5": "dim", "aug": "aug", "sus4": "sus4", "sus2": "sus2",
        "sus": "sus4", "7sus4": "sus4", "9": "dom7", "11": "dom7",
        "13": "dom7", "min9": "min9", "maj9": "maj9", "add9": "add9",
        "min11": "min9", "6": "major", "min6": "minor", "minmaj7": "minor",
        "5": "5", "maj": "major"}
TOKEN = re.compile(r"^([A-G])(s|b)?([^/]*)(?:/.*)?$")
TAGS = re.compile(r"'([^']*)'")

# Krumhansl-Kessler key profiles
MAJ = (6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88)
MIN = (6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17)


def parse(tok):
    """'Csmin7' -> (1, 'min7'); None for anything that isn't a chord."""
    m = TOKEN.match(tok)
    if not m:
        return None
    pc = (PC[m.group(1)] + {"s": 1, "b": -1}.get(m.group(2), 0)) % 12
    q = m.group(3)
    qual = QUAL.get(q) or ("minor" if q.startswith("min") else
                           "major" if q[:1] in ("", "m", "a", "6", "7", "9")
                           else None)
    return (pc, qual) if qual in CHORDS else None


def find_key(chords):
    """(tonic pc, 'major'|'minor') by Krumhansl over every chord tone."""
    h = [0.0] * 12
    for pc, q in chords:
        for iv in CHORDS[q]:
            h[(pc + iv) % 12] += 1
    # Am-F-C-G and C-G-Am-F hold the same tones; what a song starts and
    # ends on is what tells a minor song from its relative major
    ends = (chords[0], chords[-1])
    best = None
    for fam, prof in (("major", MAJ), ("minor", MIN)):
        for t in range(12):
            r = _corr(h, [prof[(i - t) % 12] for i in range(12)])
            r += 0.12 * sum(pc == t and (q in MINORISH) == (fam == "minor")
                            for pc, q in ends)
            if best is None or r > best[0]:
                best = (r, t, fam)
    return best[1], best[2]


def _corr(a, b):
    ma, mb = sum(a) / 12.0, sum(b) / 12.0
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = sum((x - ma) ** 2 for x in a) ** 0.5
    db = sum((y - mb) ** 2 for y in b) ** 0.5
    return num / (da * db) if da and db else -1


def loop_of(seq):
    """The 2-4 chord cycle a section repeats (at least twice), or None."""
    for p in (2, 3, 4):
        if len(seq) >= 2 * p and len(set(seq[:p])) == p and \
                all(seq[i] == seq[i % p] for i in range(len(seq))):
            return tuple(seq[:p])
    return None


def styles_of(tags, main):
    out = {s for s, keys in STYLE_TAGS.items()
           if any(k in t for t in tags for k in keys)}
    if not out and main == "rap":
        out.add("rap")
    return out


def build():
    if not SRC.exists():
        sys.exit("Chordonomicon CSV not found at %s (drive mounted?)" % SRC)
    csv.field_size_limit(10 ** 8)
    loops = collections.defaultdict(collections.Counter)
    nxt = collections.defaultdict(lambda: collections.defaultdict(
        collections.Counter))
    songs = collections.Counter()
    with SRC.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            st = styles_of([t.lower() for t in TAGS.findall(row["genres"] or "")],
                           row.get("main_genre"))
            if not st:
                continue
            sections, cur = [], []
            for tok in row["chords"].split():
                if tok.startswith("<"):
                    if cur:
                        sections.append(cur)
                    cur = []
                    continue
                c = parse(tok)
                if c:
                    cur.append(c)
            if cur:
                sections.append(cur)
            every = [c for s in sections for c in s]
            if len(every) < 4:
                continue
            tonic, fam = find_key(every)
            rel = lambda c: "%d:%s" % ((c[0] - tonic) % 12, c[1])  # noqa: E731
            for s in st:
                songs[(s, fam)] += 1
            for sec in sections:
                seq = [rel(c) for i, c in enumerate(sec)
                       if i == 0 or c != sec[i - 1]]
                lp = loop_of(seq)
                for s in st:
                    if lp:
                        loops[(s, fam)][lp] += 1
                    for a, b in zip(seq, seq[1:]):
                        nxt[(s, fam)][a][b] += 1
    out = {"_readme": __doc__.strip().splitlines()[0] +
           " Built by tools/build_chord_tables.py; chord = 'semitones:quality'.",
           "styles": {}}
    for (s, fam), n in sorted(songs.items()):
        if n < MIN_SONGS:
            continue
        out["styles"].setdefault(s, {})[fam] = {
            "songs": n,
            "loops": [[list(lp), c] for lp, c in
                      loops[(s, fam)].most_common(TOP_LOOPS)],
            "next": {a: dict(b.most_common(TOP_NEXT))
                     for a, b in nxt[(s, fam)].items()
                     if sum(b.values()) >= 5},
        }
    OUT.write_text(json.dumps(out, indent=0, ensure_ascii=False))
    for s, fams in sorted(out["styles"].items()):
        print(s, {f: (v["songs"], len(v["loops"])) for f, v in fams.items()})


if __name__ == "__main__":
    build()
