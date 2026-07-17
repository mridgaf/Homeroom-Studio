"""Crates, BPM filtering, template mirroring, cache staleness."""
from pathlib import Path

from reason_voice.crates import Crates
from reason_voice.indexer import PatchIndex, extract_bpm
from reason_voice.search import filter_by_bpm
from reason_voice.templates import TemplateLibrary

ENTRY = {"name": "Deep Kick", "path": "/x/deep_kick.wav", "kind": "sample",
         "device": "drums one-shot", "folder": "Kicks",
         "category": "one-shot", "group": "drums", "tokens": ["deep", "kick"]}


def make(tmp_path):
    return Crates(str(tmp_path / "crates.json"))


def test_add_and_persist(tmp_path):
    c = make(tmp_path)
    assert c.add("My Drums crate", ENTRY) == "drums"   # name normalized
    reloaded = make(tmp_path)
    assert reloaded.entries("drums")[0]["name"] == "Deep Kick"
    assert reloaded.summary() == [{"name": "drums", "count": 1}]


def test_add_is_idempotent(tmp_path):
    c = make(tmp_path)
    c.add("drums", ENTRY)
    c.add("drums", ENTRY)
    assert len(c.entries("drums")) == 1


def test_remove_anywhere(tmp_path):
    c = make(tmp_path)
    c.add("drums", ENTRY)
    c.add("favorites", ENTRY)
    assert c.remove_anywhere(ENTRY["path"])
    assert c.summary() == []


# -- bpm ------------------------------------------------------------------

def test_extract_bpm():
    assert extract_bpm("Amen_Break_170bpm.wav") == 170
    assert extract_bpm("Groove 92 bpm final.wav") == 92
    assert extract_bpm("808_Kick_03.wav") is None
    assert extract_bpm("take_500bpm.wav") is None   # out of sane range


def test_filter_by_bpm():
    entries = [
        {"name": "a", "bpm": 90}, {"name": "b", "bpm": 93},
        {"name": "c", "bpm": 140}, {"name": "d"},
    ]
    hits = filter_by_bpm(entries, "find 90 bpm drum loops")
    assert [e["name"] for e in hits] == ["a", "b"]
    assert filter_by_bpm(entries, "find drum loops") is entries


# -- template mirroring ----------------------------------------------------

def test_mirror_to(tmp_path):
    src = tmp_path / "templates"
    src.mkdir()
    (src / "Trap 808.reason").write_bytes(b"song")
    (src / "Chain.cmb").write_bytes(b"combi")   # combinators don't mirror
    dest = tmp_path / "Reason" / "Template Songs"
    dest.parent.mkdir()
    lib = TemplateLibrary(str(src))
    assert lib.mirror_to(str(dest)) == 1
    assert (dest / "Trap 808.reason").exists()
    assert not (dest / "Chain.cmb").exists()
    assert lib.mirror_to(str(dest)) == 0   # second run: nothing newer


def test_mirror_skips_when_reason_absent(tmp_path):
    src = tmp_path / "templates"
    src.mkdir()
    (src / "T.reason").write_bytes(b"x")
    lib = TemplateLibrary(str(src))
    assert lib.mirror_to(str(tmp_path / "nope" / "deeper" / "Templates")) == 0


# -- cache staleness --------------------------------------------------------

def test_load_cached_states(tmp_path):
    idx = PatchIndex(str(tmp_path / "cache.json"))
    assert idx.load_cached() == "none"
    d = tmp_path / "p"
    d.mkdir()
    (d / "kick.wav").write_bytes(b"x")
    idx.rebuild([str(d)])
    idx2 = PatchIndex(str(tmp_path / "cache.json"))
    assert idx2.load_cached() == "fresh"
    assert len(idx2.entries) == 1