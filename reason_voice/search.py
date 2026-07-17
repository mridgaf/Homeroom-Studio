"""Style search over the patch index.

Synonym-expanded token scoring with fuzzy fallback. "warm analog pad" will
match "Vintage_Moog_Softpad.zyp" because warm->vintage/soft and the device
tags contribute. Deliberately transparent — you can see exactly why a patch
matched, unlike a black-box embedding model.
"""
import re

from rapidfuzz import fuzz

from .indexer import tokenize

# descriptor -> related tokens that patch designers actually use in names
SYNONYMS = {
    "warm": ["soft", "vintage", "analog", "smooth", "mellow", "cozy"],
    "dark": ["deep", "moody", "sub", "shadow", "night"],
    "bright": ["shiny", "sparkle", "crisp", "sharp", "glass"],
    "fat": ["thick", "phat", "wide", "big", "huge", "massive"],
    "dirty": ["gritty", "grit", "distorted", "dist", "crunch", "fuzz", "raw"],
    "clean": ["pure", "clear", "pristine", "smooth"],
    "pad": ["pads", "atmosphere", "atmo", "ambient", "texture", "drone", "sweep"],
    "bass": ["sub", "low", "808", "bassline", "wobble", "reese"],
    "lead": ["leads", "solo", "melody", "mono", "screamer"],
    "pluck": ["plucks", "plucked", "stab", "pizz", "pizzicato"],
    "keys": ["piano", "epiano", "rhodes", "wurli", "clav", "organ"],
    "strings": ["string", "violin", "cello", "orchestral", "ensemble"],
    "brass": ["horn", "horns", "trumpet", "sax", "trombone"],
    "drums": ["drum", "kit", "kick", "snare", "perc", "percussion", "beat"],
    "arp": ["arpeggio", "arpeggiated", "sequence", "seq", "pattern"],
    "vintage": ["retro", "classic", "old", "tape", "analog", "70s", "80s"],
    "digital": ["fm", "glitch", "cyber", "modern", "hyper"],
    "acid": ["303", "tb303", "squelch"],
    "wobble": ["dubstep", "lfo", "womp"],
    "ambient": ["space", "spacey", "ether", "cinematic", "dreamy", "wash"],
    "aggressive": ["hard", "angry", "brutal", "heavy", "metal"],
    "vocal": ["voice", "choir", "vox", "formant"],
    "guitar": ["gtr", "strat", "acoustic", "electric"],
    "bell": ["bells", "chime", "chimes", "mallet", "glock", "vibes"],
    "synth": ["synthesizer", "analog", "poly", "mono"],
    "house": ["deep", "tech", "dance", "edm", "club"],
    "techno": ["tech", "industrial", "rave", "berlin"],
    "hiphop": ["hip", "hop", "trap", "boom", "bap", "lofi"],
    "lofi": ["lo", "fi", "dusty", "tape", "vinyl", "chill"],
}


def expand(tokens: list[str]) -> dict[str, float]:
    """token -> weight. Direct terms weigh 1.0, synonyms 0.6."""
    weights: dict[str, float] = {}
    for tok in tokens:
        weights[tok] = 1.0
        for syn in SYNONYMS.get(tok, []):
            weights.setdefault(syn, 0.6)
        # reverse lookup: query token appears in someone's synonym list
        for head, syns in SYNONYMS.items():
            if tok in syns:
                weights.setdefault(head, 0.6)
    return weights


def score(entry: dict, weights: dict[str, float]) -> float:
    entry_tokens = set(entry["tokens"])
    s = sum(w for tok, w in weights.items() if tok in entry_tokens)
    if s == 0.0:  # fuzzy fallback for typos / odd transcriptions
        name = entry["name"].lower()
        best = max((fuzz.partial_ratio(tok, name) for tok in weights), default=0)
        if best >= 85:
            s = 0.5
    return s


# Query words that mean "browse audio files, not patches"
LOOP_WORDS = {"loop", "loops", "break", "breaks"}
SAMPLE_WORDS = {"sample", "samples", "hit", "hits", "oneshot", "oneshots",
                "shot", "shots"}


def filter_by_kind(entries: list[dict], query_tokens: list[str]) -> list[dict]:
    """Narrow the pool when the query names loops/samples explicitly.
    Returns the original list untouched when it doesn't."""
    t = set(query_tokens)
    if t & LOOP_WORDS:
        return [e for e in entries
                if e.get("kind") == "sample" and e.get("category") == "loop"]
    if t & SAMPLE_WORDS:
        return [e for e in entries if e.get("kind") == "sample"]
    return entries


BPM_QUERY_RE = re.compile(r"(\d{2,3})\s*bpm")


def filter_by_bpm(entries: list[dict], query: str,
                  tolerance: int = 5) -> list[dict]:
    """'find 90 bpm drum loops' -> only entries whose filename carried a
    tempo within ±tolerance. No bpm in the query = pool untouched."""
    m = BPM_QUERY_RE.search(query.lower())
    if not m:
        return entries
    target = int(m.group(1))
    return [e for e in entries
            if e.get("bpm") and abs(e["bpm"] - target) <= tolerance]


def search(entries: list[dict], query: str, top_n: int = 5) -> list[dict]:
    weights = expand(tokenize(query))
    if not weights:
        return []
    scored, misses = [], []
    for e in entries:
        entry_tokens = set(e["tokens"])
        s = sum(w for tok, w in weights.items() if tok in entry_tokens)
        if s > 0:
            scored.append((s, e))
        else:
            misses.append(e)
    # fuzzy fallback (typos / odd transcriptions) only when token matching
    # came up short — on a 68k-file library it costs ~1s, so skip it when
    # there are already plenty of real hits
    if len(scored) < top_n:
        for e in misses:
            name = e["name"].lower()
            best = max((fuzz.partial_ratio(tok, name) for tok in weights),
                       default=0)
            if best >= 85:
                scored.append((0.5, e))
    scored.sort(key=lambda x: (-x[0], x[1]["name"].lower()))
    return [dict(e, score=round(s, 2)) for s, e in scored[:top_n]]


def similar_to(entries: list[dict], reference: dict, top_n: int = 5) -> list[dict]:
    """Find patches like a reference patch, excluding the reference itself."""
    query = " ".join(reference["tokens"])
    results = search(entries, query, top_n + 1)
    return [r for r in results if r["path"] != reference["path"]][:top_n]
