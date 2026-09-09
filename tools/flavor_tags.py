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

WHAT IS DELIBERATELY NOT GROUPED HERE, and why: `dry` (already documented
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
    "grit":    {"dust", "dusty", "dirty", "gritty", "raw", "grimy",
                "grungy", "lofi", "lo-fi", "filthy"},
    "tight":   {"tight", "tite"},
    "clean":   {"clean", "crisp", "pristine"},
    "warm":    {"warm", "round", "fat"},
    "big":     {"big", "huge", "massive", "thick"},
    "soft":    {"soft", "gentle", "mellow"},
    "vintage": {"vintage", "retro", "old-school", "oldschool", "analog"},
    "room":    {"room", "roomy", "live", "natural"},
    "crack":   {"crack", "crackly", "snappy"},
}

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


def matches(word, name):
    """True if taste-tag `word` matches sample-name-or-path `name`,
    either literally or via a documented synonym/spelling variant. Pass
    `name` already lowercased (callers already do this for the plain
    check, so this stays a drop-in replacement). Always a superset of
    `word in name` -- never matches less than the old check did."""
    name = name.lower()
    return any(variant in name for variant in expand_word(word))
