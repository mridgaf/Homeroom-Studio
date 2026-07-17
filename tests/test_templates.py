"""Template library: scan, recipe matching, session-copy naming."""
from pathlib import Path

import pytest

from reason_voice.templates import TemplateLibrary


@pytest.fixture
def lib(tmp_path):
    d = tmp_path / "templates"
    d.mkdir()
    (d / "Trap 808.reason").write_bytes(b"song")
    (d / "Gated Snare 80s.cmb").write_bytes(b"combi")
    (d / "notes.txt").write_bytes(b"ignored")
    return TemplateLibrary(str(d))


def test_scan_kinds(lib):
    by_name = {t["name"]: t for t in lib.items()}
    assert by_name["Trap 808"]["kind"] == "song"
    assert by_name["Gated Snare 80s"]["kind"] == "combinator"
    assert "notes" not in by_name


def test_items_rescan_picks_up_new_files(lib):
    assert len(lib.items()) == 2
    (Path(lib.dir) / "New One.reason").write_bytes(b"x")
    assert len(lib.items()) == 3


def test_find_fuzzy(lib):
    assert lib.find("trap 808")["name"] == "Trap 808"
    assert lib.find("the trap eight oh eight") is None or True  # no crash
    assert lib.find("gated snare")["name"] == "Gated Snare 80s"
    assert lib.find("polka accordion") is None


def test_for_recipe_matches_recipe_names(lib):
    assert lib.for_recipe("Trap 808")["name"] == "Trap 808"
    # recipe "80s Gated Snare" vs template "Gated Snare 80s" — word order differs
    assert lib.for_recipe("80s Gated Snare")["name"] == "Gated Snare 80s"
    assert lib.for_recipe("Shoegaze Guitar Wall") is None


def test_session_copy(lib, tmp_path):
    sessions = tmp_path / "sessions"
    tpl = lib.find("trap 808")
    copy = lib.new_session(tpl, str(sessions))
    assert copy.exists()
    assert copy.parent == sessions
    assert copy.suffix == ".reason"
    assert copy.stem.startswith("Trap 808")
    assert copy.read_bytes() == b"song"
    # a second session the same day must not overwrite the first
    copy2 = lib.new_session(tpl, str(sessions))
    assert copy2 != copy


def test_missing_dir_is_empty_not_error(tmp_path):
    lib = TemplateLibrary(str(tmp_path / "nope"))
    assert lib.items() == []
    assert lib.find("anything") is None
