"""Recipe knowledge base + patch style-search tests.

Ported from the ad-hoc checks used during v0.x. Covers reason_voice.recipes
(parsing, search, device refs, body sections) and reason_voice.search /
reason_voice.indexer (tokenize, synonym expansion, scoring) — the two share
the same tokenizer, so they live together here.

Synthetic fixtures only: the real recipes/*.md are content, never test data
to be edited. One read-only integration test checks the real library parses.
"""
from pathlib import Path

import pytest

from reason_voice.indexer import tokenize
from reason_voice.recipes import RecipeLibrary, parse_recipe, split_sections
from reason_voice.search import expand, search, similar_to

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RECIPE_MD = """---
name: Test Trap 808
book: hip-hop
sounds_like: Metro Boomin low end
accuracy: B
status: theoretical
tags: 808 bass sub trap
technique: parallel saturation
---

# Test Trap 808

## The Chain
SubTractor -> Scream 4 -> MClass Compressor

## Steps
1. Init a SubTractor and pull Osc 1 to a sine.
2. Drop the filter cutoff
   until only the sub remains.
3. Add Scream 4, Tape mode, damage 40.

## Why this works
Saturation adds harmonics the small speakers can reproduce.
"""

NO_FRONTMATTER_MD = "# Bare Notes\n\nJust prose, no YAML at all.\n"

BAD_YAML_MD = """---
name: [unclosed
---

## Steps
1. Only step.
"""


@pytest.fixture
def library(tmp_path):
    recipes = tmp_path / "recipes"
    (recipes / "hiphop").mkdir(parents=True)
    (recipes / "hiphop" / "test-trap-808.md").write_text(RECIPE_MD)
    (recipes / "hiphop" / "other.md").write_text(
        RECIPE_MD.replace("Test Trap 808", "Boom Bap Bus")
                 .replace("sounds_like: Metro Boomin low end", "sounds_like: DJ Premier drums")
                 .replace("tags: 808 bass sub trap", "tags: drums bus glue boom bap")
    )
    refs = tmp_path / "device_refs"
    refs.mkdir()
    (refs / "scream-4.md").write_text("# Scream 4\n\nA distortion unit.\n")
    (refs / "rv7000-mkii.md").write_text("# RV7000\n\nA reverb.\n")
    return RecipeLibrary(str(recipes), str(refs))


# -- parsing ------------------------------------------------------------------

def test_parse_frontmatter(tmp_path):
    p = tmp_path / "r.md"
    p.write_text(RECIPE_MD)
    r = parse_recipe(p)
    assert r.name == "Test Trap 808"
    assert r.book == "hip-hop"
    assert r.accuracy == "B"
    assert r.status == "theoretical"
    assert r.technique == "parallel saturation"
    assert r.sounds_like == "Metro Boomin low end"


def test_steps_extraction_with_continuation(tmp_path):
    p = tmp_path / "r.md"
    p.write_text(RECIPE_MD)
    r = parse_recipe(p)
    assert len(r.steps) == 3
    assert r.steps[0] == "Init a SubTractor and pull Osc 1 to a sine."
    # continuation line folds into the step above
    assert r.steps[1] == "Drop the filter cutoff until only the sub remains."
    # extraction stops at the next ## heading
    assert "Saturation" not in " ".join(r.steps)


def test_parse_without_frontmatter(tmp_path):
    p = tmp_path / "bare.md"
    p.write_text(NO_FRONTMATTER_MD)
    r = parse_recipe(p)
    assert r.name == "bare"          # falls back to filename stem
    assert r.steps == []


def test_parse_bad_yaml_does_not_crash(tmp_path):
    p = tmp_path / "bad.md"
    p.write_text(BAD_YAML_MD)
    r = parse_recipe(p)
    assert r.name == "bad"
    assert r.steps == ["Only step."]


def test_split_sections(tmp_path):
    p = tmp_path / "r.md"
    p.write_text(RECIPE_MD)
    r = parse_recipe(p)
    sections = split_sections(r.body)
    titles = [t for t, _ in sections]
    assert titles == ["The Chain", "Steps", "Why this works"]
    chain = dict(sections)["The Chain"]
    assert "SubTractor" in chain


# -- recipe search ------------------------------------------------------------

def test_search_by_tag(library):
    hits = library.search("trap 808")
    assert hits and hits[0].name == "Test Trap 808"


def test_search_by_sounds_like(library):
    hits = library.search("metro boomin")
    assert hits and hits[0].name == "Test Trap 808"


def test_search_no_match(library):
    assert library.search("polka accordion") == []


def test_search_empty_query(library):
    assert library.search("") == []


# -- device references --------------------------------------------------------

def test_device_ref_exact(library):
    assert library.device_ref("scream 4").name == "scream-4.md"


def test_device_ref_fuzzy(library):
    assert library.device_ref("the scream unit").name == "scream-4.md"
    assert library.device_ref("rv7000").name == "rv7000-mkii.md"


def test_device_ref_miss(library):
    assert library.device_ref("kazoo") is None


def test_device_ref_gear_aliases(tmp_path):
    refs = tmp_path / "refs"
    refs.mkdir()
    for f in ("launchkey-mk3", "audiobox-96", "yamaha-dtx400k",
              "yamaha-emx66m", "samson-servo-300", "guitar-amps"):
        (refs / f"{f}.md").write_text(f"# {f}\n\nGear.\n")
    lib = RecipeLibrary(str(tmp_path / "none"), str(refs))
    cases = {
        "launchkey-mk3.md": ("drum pads", "my controller", "the keyboard",
                             "launchkey"),
        "audiobox-96.md": ("my interface", "audiobox",
                           "personas audiobox ninety six"),
        "yamaha-dtx400k.md": ("my drum kit", "electronic drums", "e drums"),
        "yamaha-emx66m.md": ("the mixer", "pa"),
        "samson-servo-300.md": ("power amp", "servo"),
        "guitar-amps.md": ("guitar amp", "the crate", "epiphone"),
    }
    for filename, phrases in cases.items():
        for phrase in phrases:
            assert lib.device_ref(phrase).name == filename, phrase


# -- patch style-search (reason_voice.search) ----------------------------------

PATCHES = [
    {"name": "Vintage Moog Softpad", "path": "/p/a.zyp",
     "device": "subtractor synth", "tokens": tokenize("vintage moog softpad subtractor synth")},
    {"name": "Gritty 808 Sub", "path": "/p/b.thor",
     "device": "thor synth", "tokens": tokenize("gritty 808 sub thor synth")},
    {"name": "Glass Bell Keys", "path": "/p/c.sxt",
     "device": "nnxt sampler", "tokens": tokenize("glass bell keys nnxt sampler")},
]


def test_tokenize_drops_stopwords_and_case():
    assert tokenize("The Warm Analog PAD patch") == ["warm", "analog", "pad"]


def test_expand_synonyms():
    w = expand(["warm"])
    assert w["warm"] == 1.0
    assert w["vintage"] == 0.6          # forward synonym
    assert expand(["moody"])["dark"] == 0.6   # reverse lookup


def test_search_matches_via_synonym():
    # "warm analog pad" must reach "Vintage Moog Softpad" through warm->vintage/soft
    hits = search(PATCHES, "warm analog pad")
    assert hits and hits[0]["name"] == "Vintage Moog Softpad"
    assert hits[0]["score"] > 0


def test_search_ranking_direct_beats_synonym():
    hits = search(PATCHES, "gritty 808")
    assert hits[0]["name"] == "Gritty 808 Sub"


def test_search_no_hits():
    assert search(PATCHES, "accordion polka") == []


def test_search_fuzzy_fallback_for_typos():
    # no token match, but the name is close enough — fuzzy rescue kicks in
    hits = search(PATCHES, "softpadd")
    assert hits and hits[0]["name"] == "Vintage Moog Softpad"


def test_similar_to_excludes_reference():
    ref = PATCHES[0]
    results = similar_to(PATCHES, ref, 5)
    assert all(r["path"] != ref["path"] for r in results)


# -- integration: the real library parses (read-only) -------------------------

def test_real_recipe_library_parses():
    recipes_dir = PROJECT_ROOT / "recipes"
    refs_dir = PROJECT_ROOT / "device_refs"
    if not recipes_dir.exists():
        pytest.skip("real recipes/ not present")
    lib = RecipeLibrary(str(recipes_dir), str(refs_dir))
    assert len(lib.recipes) >= 14
    assert len(lib.device_refs) >= 4
    # every non-anti recipe must yield walkthrough steps
    for r in lib.recipes:
        if "anti" not in r.path.stem:
            assert r.steps, f"{r.path.name} has no ## Steps"
