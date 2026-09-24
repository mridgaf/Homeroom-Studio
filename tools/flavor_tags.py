"""Synonym layer for taste-tag matching (added 2026-09-09).

THE PROBLEM THIS EXISTS TO FIX. `_pick_path`'s taste-tag check
(tools/crew.py, `has_want`) has always been a literal substring test:
`word in filename.lower()`. Every legend's `_research_note` documents the
same failure repeating: Doc Day's punch/knock/deep matched ONE file in the
whole library; this library spells "tight" as `tite` so `tight` matches 1
file and `tite` matches 71; "warm" and "big"/"huge" match ZERO files
anywhere. The fix so far has been manual, every time: run
`legend_newbuild.py --tags`, see which words are dead, hand-rewrite the
tag list to a word that happens to exist in real filenames. This module
lets a tag word also match its documented synonyms/spelling variants, so
fewer new legends need that manual pass.

SCOPE, ON PURPOSE. Owner directive 2026-09-09: wire this going forward
only, existing legends get retagged by hand later. So this is OPT-IN per
preset (`"flavor_match": true` in legends_config.json), defaulting to
False/absent, which makes `_pick_path` fall back to the exact old
literal-substring check -- see test_flavor_match_off_matches_old_behavior
in tests/test_crew.py. Same shape as `own_soundbank` and the sorted-folder
feature: a single boolean opt-out/opt-in, never a roster-wide behavior
change. Do not flip this on for an existing legend without being asked --
that is exactly the "blanket-apply" the legend-new-build skill forbids.

UPDATE 2026-09-24: the owner ruled on every pair himself (see the notes
in SYNONYM_GROUPS). He grouped punch/knock, deep/sub/low/dark and boom/808,
overruling the paragraph below, and split lofi from dirty, clipped from
distorted and fat from warm. `dry` is still not grouped.

WHAT WAS DELIBERATELY NOT GROUPED HERE (2026-09-09), and why: `dry` (already documented
as an over-eager match -- it drags in SIDESTICK samples like
"HWIP_Dry_SideStick" and "sn4 flam dry" on nearly every legend that tried
it); `boom` (matched 808 files under the OLD kick/808 pool split -- the
808 role now buckets separately per sample_library.py's 2026-09-07 change,
but the word has a bad history and isn't touched here without a fresh
audit); `punch`/`knock`/`deep` (Doc Day's dead-and-wrong-bucket words,
same reason). None of these get a synonym cluster -- grouping them wider
would only make a documented failure mode easier to trigger, not harder.
The clusters below are a starting vocabulary, built from words that
already co-occur describing the same character in the `_research_note`
fields (e.g. Otto Grit's kick wants "dust"+"dirty" together; the RZA/Razor
note describes "gritty and raw"). Expand them as real audits turn up more
-- this is meant to be edited, not treated as finished.
"""

# canonical group -> the words/spellings that should count as each other.
# A tag word not listed here just falls back to plain substring matching,
# same as before this module existed.
SYNONYM_GROUPS = {
    "grit":    {"grit", "dirt", "dust", "dusty", "dirty", "gritty", "raw",
                "grimy", "grungy", "filthy", "vinyl"},
    "tight":   {"tight", "tite", "short"},
    "clean":   {"clean", "crisp", "pristine", "bright"},
    "warm":    {"warm", "round"},
    "big":     {"big", "huge", "massive", "thick"},
    "soft":    {"soft", "gentle", "mellow", "light"},
    "vintage": {"vintage", "retro", "old-school", "oldschool", "analog"},
    "room":    {"room", "roomy", "live", "natural"},
    "crack":   {"crack", "crackly", "snappy"},
    # 2026-09-24, owner: "Word sounds won't be exact matches we should at
    # least look for synonyms or similar words". HE RULED ON EACH PAIR
    # (clickable, same day): lofi is NOT dirty/dusty, clipped is NOT
    # distorted, fat is NOT warm; raw=dirty, crunch=crush, heavy/slam=hard,
    # live=roomy, reverb/hall=washed, tight=tite=short, huge/massive=big,
    # snappy=crack, shake=shaker are all his "same sound". Each group below was
    # counted against his real drum pools first (distort/clip +4 kicks,
    # heavy +3 snares, ...); none of them is a word any preset used before.
    "distort": {"distort", "distorted", "dist", "saturated", "overdrive",
                "fuzz"},
    "hard":    {"hard", "heavy", "slam", "smack"},
    "crunch":  {"crunch", "crunchy", "crush", "crushed"},
    "noise":   {"noise", "noisy", "static"},
    "wash":    {"wash", "washed", "verb", "reverb", "hall"},
    "shaker":  {"shaker", "shake", "shkr"},
    # round 2 of his rulings, same day: every existing group above confirmed
    # as-is, plus these. punch/knock, deep and boom were deliberately left
    # ungrouped on 2026-09-09 because of Doc Day's history (see the module
    # docstring); HE overruled that on 2026-09-24 - "punch = knock",
    # "deep = sub = low", "dark = low", "boom = 808" are his words.
    "punch":   {"punch", "punchy", "knock"},
    "deep":    {"deep", "sub", "low", "dark"},
    "boom":    {"boom", "808"},
}

# A SNARE want reached only through a synonym never lands on one of these
# (2026-09-24): the grit group's "lofi" pulls DECEPT_Lofi_Sidestick, "raw"
# pulls CRAWL_SideStick, "dirty" pulls MZ Clap [Dirty] out of the snare
# bucket. Same failure as the documented `dry` trap. The LITERAL word still
# matches anything, so asking for "rimshot" on purpose keeps working.
import re as _re
_NOT_A_SNARE = _re.compile(r"side ?stick|\bstick\b|\bss\b|\brim\b|clap|kick n")
# and a HAT want reached only through a synonym never lands on an open hat:
# "tite" -> "tight" pulled "Cymatics - Tight Open Hihat" into closed lanes.
# "kick n hat"/"kick n snare" are layered combos (tite=short reached them).
_NOT_A_CLOSED_HAT = _re.compile(r"\bopen\b|\boh\b|kick n")

_WORD_TO_GROUP = {}
for _canon, _words in SYNONYM_GROUPS.items():
    for _w in _words:
        _WORD_TO_GROUP[_w] = _canon


def expand_word(word):
    """A taste-tag word -> the set of words it should be treated as
    equivalent to (itself, plus its synonym-group siblings if it has
    any). A word with no group returns just itself, so this is always a
    superset of the literal word."""
    w = word.lower()
    group = _WORD_TO_GROUP.get(w)
    if not group:
        return {w}
    return set(SYNONYM_GROUPS[group]) | {w}


def matches(word, name, role=None):
    """True if taste-tag `word` matches sample-name-or-path `name`,
    either literally or via a documented synonym/spelling variant. Pass
    `name` already lowercased (callers already do this for the plain
    check, so this stays a drop-in replacement). Always a superset of
    `word in name` -- never matches less than the old check did.
    role="snare": a synonym-only match on a sidestick/rim/clap is refused
    (see _NOT_A_SNARE)."""
    name = name.lower()
    if word.lower() in name:
        return True
    if role == "snare" and _NOT_A_SNARE.search(name):
        return False
    if role == "hat" and _NOT_A_CLOSED_HAT.search(name):
        return False
    return any(variant in name for variant in expand_word(word))
