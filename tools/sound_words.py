"""Group sounds by the words in their names, for the rack's dropdowns.

Owner 2026-09-28: "the first drop down lets you choose what type of
instrument ... then another drop down grouped by the naming vocabulary and
synonyms used to describe them ... generic sounding names grouped together".
A sound goes under every word group its name has; a name with no describing
word goes under "Plain names · <pack>" (his pick: split by pack, like the old
pack grouping, since ~9 in 10 drum names have no describing word).

Synonyms are HIS rulings, never guesses (memory: synonyms-ask-owner), and
there is ONE list of them: flavor_tags.SYNONYM_GROUPS -- the same one every
DJ's and genre's picks use (his 2026-09-28 rulings included, at his ask).
"""
from __future__ import annotations

import re
from collections import Counter

from flavor_tags import SYNONYM_GROUPS

# Describing words with no synonym: each is ONE word in its spellings.
ONE_WORD = [
    ("dry",), ("lofi",), ("open",), ("closed",), ("loose",), ("wide",),
    ("muted", "mute"), ("reverse", "reversed"), ("flam", "flams"),
    ("buzz", "buz"), ("rimshot", "rimshots"), ("sidestick",),
    ("gated", "gate"), ("roll", "rolls"), ("medium", "med"),
    ("break", "breaks", "breakbeat"), ("kick", "kicks"),
    ("snare", "snares", "snr"), ("hat", "hats", "hihat", "hihats"),
    ("perc", "percs", "percussion"), ("top", "tops"), ("ride", "rides"),
    ("crash", "crashes"), ("clap", "claps"), ("rim", "rims"),
    ("tom", "toms"), ("cowbell",), ("conga", "congas"),
    ("bongo", "bongos"), ("tambourine", "tamb"),
    ("riser", "risers", "uplifter"), ("sweep", "sweeps"),
    ("impact", "impacts"), ("whoosh",),
    ("sustain", "sustains", "sus"), ("tremolo", "trem"),
    ("vibrato", "vib"), ("legato",), ("marcato",), ("swell", "swells"),
    ("crescendo", "cresc"), ("chop", "chops", "chopped"),
    ("arp", "arps", "arpeggio"), ("jazz", "jazzy"), ("trap",), ("rnb",),
    ("soul", "soulful"), ("funk", "funky"), ("gospel",), ("disco",),
    ("synthpop",), ("dubstep",), ("drill",), ("nostalgic",),
    ("acoustic",), ("electric",), ("detuned",), ("liquid",),
    ("cloud", "clouds"), ("unison",), ("stack", "stacked"), ("brutal",),
    ("doom", "doomed"), ("angry",), ("aged",), ("dreamy", "dream"),
    ("sad",), ("chill",), ("epic",),
]

# A label says the whole word, not the file's short form.
_FULL = {"stac": "staccato", "stacc": "staccato", "spic": "spiccato",
         "pizz": "pizzicato", "sus": "sustain", "trem": "tremolo",
         "vib": "vibrato", "snr": "snare", "med": "medium", "buz": "buzz",
         "tamb": "tambourine", "cresc": "crescendo", "dist": "distorted",
         "verb": "reverb", "shkr": "shaker", "tite": "tight"}

_GROUPS = {k: set(ws) for k, ws in SYNONYM_GROUPS.items()}  # key -> words
for _ws in ONE_WORD:
    _GROUPS.setdefault(_ws[0], set()).update(_ws)
_SYN = set(SYNONYM_GROUPS)
_KEY_OF = {}
for _k, _ws in _GROUPS.items():
    for _w in _ws:
        _KEY_OF.setdefault(_w, _k)

PLAIN = "Plain names"


def tokens(name):
    """Whole words of a name, lowercased. "SusVib" -> sus, vib; a word right
    after "no"/"non" is dropped ("NoSus" is not sustain, "Non-Vibrato" is
    not vibrato); "Lo Fi" reads as lofi."""
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(name))
    out, skip = [], False
    for t in re.split(r"[^a-z]+", s.lower()):
        if not t:
            continue
        if skip:
            skip = False
        elif t in ("no", "non"):
            skip = True
        elif t == "fi" and out and out[-1] == "lo":
            out[-1] = "lofi"
        else:
            out.append(t)
    return out


def _label(key, seen):
    if key not in _SYN:            # one word in its spellings: say it once
        return key.capitalize()
    words = sorted({_FULL.get(w, w) for w in seen}, key=lambda w: (w != key, w))
    return " · ".join(words[:4]).capitalize()


def group_labels(names, packs):
    """For each name, the dropdown groups it goes under: every word group its
    name or its pack/folder belongs to (he sorts sounds into folders named
    "Deep", "Dirty", "Short"), else "Plain names · <pack>". In a list longer
    than 12, a group needs 2+ sounds, and a word in more than half of the
    NAMES says nothing about them (every kick is a "kick"), so neither makes
    a group. Folder words don't count toward that half: 284 of his 488 kicks
    sit in a folder he named "Short", and that says plenty."""
    found, in_name = [], Counter()
    for n, pack in zip(names, packs):
        hit = {}
        for src in (n, pack or ""):
            for t in tokens(src):
                k = _KEY_OF.get(t)
                if k:
                    hit.setdefault(k, set()).add(t)
            if src is n:
                in_name.update(list(hit))    # the name's own words, once
        found.append(hit)
    size = len(names)
    count = Counter(k for hit in found for k in hit)
    keep = {k for k, c in count.items()
            if size <= 12 or (c >= 2 and in_name[k] <= size / 2)}
    seen = {}
    for hit in found:
        for k, ws in hit.items():
            seen.setdefault(k, set()).update(ws)
    labels = {k: _label(k, seen[k]) for k in keep}
    return [sorted(labels[k] for k in hit if k in keep)
            or ["%s · %s" % (PLAIN, pack or "other")]
            for hit, pack in zip(found, packs)]


def tag(items, name_key="name", pack_key="pack", by=None):
    """Put `words` (group labels) on each item dict, in place. `by` splits
    the list first (e.g. by instrument type) so each part is grouped on its
    own terms."""
    parts = {}
    for it in items:
        parts.setdefault(it.get(by) if by else None, []).append(it)
    for part in parts.values():
        for it, labels in zip(part, group_labels(
                [it[name_key] for it in part],
                [it.get(pack_key) for it in part])):
            it["words"] = labels
    return items

