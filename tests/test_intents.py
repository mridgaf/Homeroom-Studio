"""Intent grammar tests — ported from the ad-hoc checks used during v0.x.

Run from the project root:  ./.venv/bin/python -m pytest
Pattern ORDER matters in intents.py (first match wins); several tests below
exist purely to lock that ordering down (e.g. reindex must outrank recipe
search, transport 'stop' must outrank 'stop walkthrough').
"""
import pytest

from reason_voice.intents import parse


def cmd(text):
    return parse(text).command


def args(text):
    return parse(text).args


# -- patch browsing ----------------------------------------------------------

@pytest.mark.parametrize("text", ["next patch", "forward patch", "patch next", "next"])
def test_patch_next(text):
    assert cmd(text) == "patch_next"


@pytest.mark.parametrize("text", ["previous patch", "last patch", "back", "previous"])
def test_patch_prev(text):
    assert cmd(text) == "patch_prev"


# -- transport ---------------------------------------------------------------

@pytest.mark.parametrize("text,expected", [
    ("play", "play"), ("play the song", "play"), ("start", "play"),
    ("stop", "stop"), ("record", "record"),
    ("undo", "undo"), ("redo", "redo"),
])
def test_transport(text, expected):
    assert cmd(text) == expected


def test_loop_states():
    assert parse("loop on").args["state"] == "on"
    assert parse("loop off").args["state"] == "off"
    assert parse("loop").args["state"] == "toggle"


def test_case_and_punctuation_stripped():
    assert cmd("Play.") == "play"
    assert cmd("NEXT PATCH!") == "patch_next"


# -- track targeting ---------------------------------------------------------

@pytest.mark.parametrize("text,expected", [
    ("next track", "track_next"), ("track down", "track_next"),
    ("previous track", "track_prev"), ("track up", "track_prev"),
])
def test_tracks(text, expected):
    assert cmd(text) == expected


# -- reindex must outrank recipe search --------------------------------------

@pytest.mark.parametrize("text", [
    "rebuild the index", "rebuild the recipe index",
    "refresh the library", "update the patch index",
])
def test_reindex_outranks_recipe_search(text):
    assert cmd(text) == "reindex"


# -- walkthrough / steps -----------------------------------------------------

def test_walkthrough_start():
    assert cmd("walk me through it") == "walkthrough"


@pytest.mark.parametrize("text,expected", [
    ("next step", "step_next"), ("step", "step_next"),
    ("previous step", "step_prev"), ("back step", "step_prev"),
    ("repeat", "step_repeat"), ("repeat that", "step_repeat"),
    ("say that again", "step_repeat"),
    ("done", "walkthrough_done"), ("finished", "walkthrough_done"),
    ("done recipe", "walkthrough_done"),
])
def test_walkthrough_navigation(text, expected):
    assert cmd(text) == expected


def test_transport_stop_outranks_stop_walkthrough():
    # Documented pattern-order quirk: "stop" is transport even mid-walkthrough;
    # the UI/session layer decides, not the grammar.
    assert cmd("stop walkthrough") == "stop"


# -- recipe search -----------------------------------------------------------

@pytest.mark.parametrize("text,query", [
    ("recipe for a trap 808", "a trap 808"),
    ("recipes to make a gated snare", "a gated snare"),
    ("how do i get a shoegaze wall", "a shoegaze wall"),
    ("sounds like nirvana drums", "nirvana drums"),
])
def test_recipe_find(text, query):
    intent = parse(text)
    assert intent.command == "recipe_find"
    assert intent.args["query"] == query


# -- feelings ----------------------------------------------------------------

@pytest.mark.parametrize("text,query", [
    ("make it feel nostalgic", "nostalgic"),
    ("how do i make this feel dark", "dark"),
    ("make the beat feel triumphant", "triumphant"),
    ("i want it to feel like a rainy sunday", "like a rainy sunday"),
])
def test_feeling_search(text, query):
    intent = parse(text)
    assert intent.command == "recipe_find"
    assert intent.args["query"] == query


# -- device reference --------------------------------------------------------

@pytest.mark.parametrize("text,name", [
    ("what is scream 4", "scream 4"),
    ("what's the rv7000", "rv7000"),
    ("tell me about the subtractor", "subtractor"),
    ("what are reference tracks", "reference tracks"),
    ("what are the best mixing references", "best mixing references"),
])
def test_device_ref(text, name):
    intent = parse(text)
    assert intent.command == "device_ref"
    assert intent.args["name"] == name


# -- patch search / load -----------------------------------------------------

def test_find_like_last():
    assert cmd("find something like this") == "find_like_last"
    assert cmd("find something like the last one") == "find_like_last"


@pytest.mark.parametrize("text,query", [
    ("find a warm analog pad", "a warm analog pad"),
    ("search for massive bass", "massive bass"),
    ("show me some pads", "some pads"),
    ("i want a fat bass", "a fat bass"),
])
def test_find(text, query):
    intent = parse(text)
    assert intent.command == "find"
    assert intent.args["query"] == query


@pytest.mark.parametrize("text,which", [
    ("load two", 2), ("load number 3", 3), ("open 4", 4), ("use first", 1),
    ("load to", 2),   # whisper homophone: "two" heard as "to"
])
def test_load_result_numbers(text, which):
    intent = parse(text)
    assert intent.command == "load_result"
    assert intent.args["which"] == which


def test_load_by_name_falls_through_to_find_and_load():
    intent = parse("load massive bass")
    assert intent.command == "find_and_load"
    assert intent.args["query"] == "massive bass"


def test_more_results():
    assert cmd("more results") == "more_results"
    assert cmd("more") == "more_results"


# -- sample preview -----------------------------------------------------------

@pytest.mark.parametrize("text,which", [
    ("preview two", 2), ("audition 3", 3), ("hear number one", 1),
])
def test_preview_result(text, which):
    intent = parse(text)
    assert intent.command == "preview_result"
    assert intent.args["which"] == which


def test_stop_preview_outranks_transport_stop():
    assert cmd("stop preview") == "preview_stop"
    assert cmd("stop the preview") == "preview_stop"
    assert cmd("stop") == "stop"    # bare stop is still transport


def test_preview_nonnumber_falls_through():
    # "hear a fat bass" is a search, not a preview of result "a"
    assert cmd("hear a fat bass") != "preview_result"


# -- claude loop pack -----------------------------------------------------------

@pytest.mark.parametrize("text", ["claude loops", "my claude loops",
                                  "play claude's drum loops",
                                  "show the claude loops"])
def test_claude_loops(text):
    assert cmd(text) == "claude_loops"


def test_plain_drum_loops_still_searches():
    assert parse("find drum loops").command == "find"


# -- templates ----------------------------------------------------------------

@pytest.mark.parametrize("text", ["templates", "list templates", "show templates",
                                  "my templates"])
def test_template_list(text):
    assert cmd(text) == "template_list"


@pytest.mark.parametrize("text,query", [
    ("new session from trap 808", "trap 808"),
    ("start a session with the gated snare", "the gated snare"),
    ("use template trap 808", "trap 808"),
    ("open the template gated snare", "gated snare"),
])
def test_template_start(text, query):
    intent = parse(text)
    assert intent.command == "template_start"
    assert intent.args["query"] == query


def test_template_start_bare():
    intent = parse("new session")
    assert intent.command == "template_start"
    assert intent.args.get("query") in (None, "",)


@pytest.mark.parametrize("text", ["save this as a template", "save as template",
                                  "make this a template"])
def test_template_howto(text):
    assert cmd(text) == "template_howto"


def test_open_template_by_name_still_loads_patches():
    # "open" without the word template keeps its old meaning
    assert parse("open massive bass").command == "find_and_load"


# -- audition mode ------------------------------------------------------------

def test_audition_with_query():
    intent = parse("audition drum loops")
    assert intent.command == "audition"
    assert intent.args["query"] == "drum loops"


def test_audition_bare_and_controls():
    assert cmd("audition") == "audition"
    assert cmd("skip") == "audition_skip"
    assert cmd("that one") == "audition_pick"
    assert cmd("keep it") == "audition_pick"


def test_preview_number_still_wins_over_audition():
    assert parse("preview two").command == "preview_result"
    assert parse("preview warm pads").command == "audition"


# -- crates --------------------------------------------------------------------

def test_star_number():
    intent = parse("star two")
    assert intent.command == "crate_add"
    assert intent.args == {"which": 2, "crate": "favorites"}


def test_add_to_named_crate():
    intent = parse("add two to my drums crate")
    assert intent.command == "crate_add"
    assert intent.args == {"which": 2, "crate": "drums"}


def test_unstar():
    intent = parse("unstar three")
    assert intent.command == "crate_remove"
    assert intent.args["which"] == 3


def test_crate_open():
    assert parse("open my drums crate").args["name"] == "drums"
    assert parse("my favorites").command == "crate_open"
    assert parse("my favorites").args["name"] == "favorites"


# -- recipe honesty ------------------------------------------------------------

def test_recipe_tested():
    assert cmd("it worked") == "recipe_tested"
    assert cmd("mark it tested") == "recipe_tested"


def test_recipe_note():
    intent = parse("note: used damage 35 instead")
    assert intent.command == "recipe_note"
    assert intent.args["text"] == "used damage 35 instead"


# -- housekeeping ------------------------------------------------------------

def test_help_and_quit():
    assert cmd("help") == "help"
    assert cmd("what can i say") == "help"
    assert cmd("quit") == "quit"
    assert cmd("exit") == "quit"


def test_empty_is_noop():
    assert cmd("") == "noop"
    assert cmd("   ") == "noop"


def test_unmatched_text_goes_to_the_dial():
    """Owner decision 2026-09-10: an unrecognised phrase is a knob move, not a
    patch search. His patches are sealed inside ReFills, so the old fallback
    search found nothing useful; "give it more punch" is the real use."""
    intent = parse("give it more punch")
    assert intent.command == "dial"
    assert intent.args["phrase"] == "give it more punch"


def test_explicit_search_still_searches():
    """The fallback moved; the `find` patterns did not. This includes the
    sidebar bin buttons, which send "find <group> loops"."""
    for text in ("find a warm analog pad", "find drum loops", "search for 808"):
        assert parse(text).command == "find", text


# -- v2: fuzzy intent matching (whisper mis-transcriptions) -------------------
# "find something like this" is often heard as "and something like this".
# The grammar must rescue near-miss command phrases instead of dumping them
# into a patch search, while leaving genuine sound descriptions alone.

@pytest.mark.parametrize("text,expected", [
    ("and something like this", "find_like_last"),
    ("find something like these", "find_like_last"),
    ("walk me thru it", "walkthrough"),
    ("walk me through this", "walkthrough"),
])
def test_fuzzy_rescues_mangled_commands(text, expected):
    assert cmd(text) == expected


@pytest.mark.parametrize("text", [
    "warm analog pad", "dusty lofi keys", "big room techno kick",
])
def test_fuzzy_leaves_plain_descriptions_alone(text):
    """The point of this test is unchanged: fuzzy rescue must not swallow
    phrases that merely resemble a command. Only the destination moved."""
    intent = parse(text)
    assert intent.command == "dial"
    assert intent.args["phrase"] == text
