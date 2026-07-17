"""Sample/loop indexing and browsing: classification, kind filtering, bins."""
from pathlib import Path

import pytest

from reason_voice.indexer import bins, classify_sample, scan, tokenize
from reason_voice.search import filter_by_kind, search


@pytest.fixture
def tree(tmp_path):
    d = tmp_path / "sounds"
    (d / "Drums" / "Kicks").mkdir(parents=True)
    (d / "Drums" / "Kicks" / "Deep_Kick_01.wav").write_bytes(b"x")
    (d / "Drums" / "Amen_Break_170bpm.wav").write_bytes(b"x")
    (d / "Bass").mkdir()
    (d / "Bass" / "Funky_Bassline.rx2").write_bytes(b"x")
    (d / "Vox").mkdir()
    (d / "Vox" / "Choir_Aah.aiff").write_bytes(b"x")
    (d / "MySynth.zyp").write_bytes(b"x")           # patch, not sample
    # Music.app media must be excluded
    (d / "Media.localized" / "Artist").mkdir(parents=True)
    (d / "Media.localized" / "Artist" / "song.wav").write_bytes(b"x")
    return d


def by_name(entries):
    return {e["name"]: e for e in entries}


def test_scan_classifies_samples(tree):
    e = by_name(scan([str(tree)]))
    kick = e["Deep_Kick_01"]
    assert kick["kind"] == "sample"
    assert kick["category"] == "one-shot"
    assert kick["group"] == "drums"

    brk = e["Amen_Break_170bpm"]      # "break" token + bpm in name
    assert brk["category"] == "loop"
    assert brk["group"] == "drums"

    rex = e["Funky_Bassline"]          # .rx2 is a loop by definition
    assert rex["category"] == "loop"
    assert rex["group"] == "bass"

    vox = e["Choir_Aah"]
    assert vox["group"] == "vocal"

    patch = e["MySynth"]
    assert patch["kind"] == "patch"
    assert "category" not in patch


def test_scan_excludes_music_app_media(tree):
    assert "song" not in by_name(scan([str(tree)]))


def test_classify_loop_signals():
    assert classify_sample(["drum", "loop"], ".wav", "drum_loop.wav")[0] == "loop"
    assert classify_sample(["pad"], ".rx2", "pad.rx2")[0] == "loop"
    assert classify_sample(["kick"], ".wav", "kick.wav")[0] == "one-shot"
    assert classify_sample(["thing"], ".wav", "thing_90bpm.wav")[0] == "loop"
    # Ableton looper captures are loops
    assert classify_sample(["looper0003", "audio"], ".aif",
                           "Looper0003 2-Audio.aif")[0] == "loop"


def test_group_falls_back_to_folder(tmp_path):
    d = tmp_path / "s"
    (d / "Live Recordings").mkdir(parents=True)
    (d / "Live Recordings" / "0001 2-Audio.aif").write_bytes(b"x")
    (d / "Samples" / "Waveforms").mkdir(parents=True)
    (d / "Samples" / "Waveforms" / "Phrantasy-C5.aif").write_bytes(b"x")
    e = by_name(scan([str(d)]))
    assert e["0001 2-Audio"]["group"] == "live recordings"
    # "Samples" is too generic — the meaningful subfolder wins
    assert e["Phrantasy-C5"]["group"] == "waveforms"


def test_folder_label_distinguishes_duplicates():
    from reason_voice.indexer import folder_label
    a = folder_label(("Ableton", "MySong Project", "Samples", "Recorded",
                      "0001 1-Audio.aif"))
    b = folder_label(("Ableton", "OtherSong Project", "Samples", "Recorded",
                      "0001 1-Audio.aif"))
    assert a != b
    assert "MySong Project" in a


def test_orchestral_bins_by_instrument():
    # a 50k-file orchestral library must not become one giant bin
    _, group = classify_sample(["violin", "attack", "c6"], ".aif",
                               "Violin Attack-C6.aif")
    assert group == "violin"
    _, group = classify_sample(["solo", "flute", "f4"], ".aif",
                               "Solo Flute-F4.aif")
    assert group == "flute"


def test_pack_folder_becomes_group(tmp_path):
    # machine-named zones inside a pack bin under the PACK, not the
    # instrument word buried in the pack's folder name
    d = tmp_path / "s"
    deep = d / "Sample Packs" / "London Symphonic Strings Volume I" / "l" / "close"
    deep.mkdir(parents=True)
    (deep / "sord_c_38_43_21_21.wav").write_bytes(b"x")
    e = by_name(scan([str(d)]))
    assert e["sord_c_38_43_21_21"]["group"] == "london symphonic strings"


def test_unplugged_drive_keeps_cached_entries(tmp_path):
    from reason_voice.indexer import PatchIndex
    local = tmp_path / "local"
    local.mkdir()
    (local / "kick.wav").write_bytes(b"x")
    gone = str(tmp_path / "external")   # never exists = unplugged drive
    idx = PatchIndex(str(tmp_path / "cache.json"))
    idx.entries = [
        {"name": "ext_loop", "path": gone + "/ext_loop.wav",
         "kind": "sample", "category": "loop", "group": "drums",
         "folder": "", "device": "drums loop", "tokens": ["ext"]},
    ]
    n = idx.rebuild([str(local), gone])
    names = {e["name"] for e in idx.entries}
    assert names == {"kick", "ext_loop"}
    assert n == 2


def test_filter_by_kind(tree):
    entries = scan([str(tree)])
    loops = filter_by_kind(entries, tokenize("drum loops"))
    assert loops and all(e["category"] == "loop" for e in loops)
    samples = filter_by_kind(entries, tokenize("bass samples"))
    assert samples and all(e["kind"] == "sample" for e in samples)
    # no loop/sample word -> pool untouched (same object, patches included)
    assert filter_by_kind(entries, tokenize("warm pad")) is entries


def test_search_drum_loops_end_to_end(tree):
    entries = scan([str(tree)])
    pool = filter_by_kind(entries, tokenize("drum loops"))
    hits = search(pool, "drum loops", 10)
    names = [h["name"] for h in hits]
    assert "Amen_Break_170bpm" in names
    assert "Deep_Kick_01" not in names      # one-shot filtered out
    assert "MySynth" not in names           # patch filtered out


def test_bins(tree):
    entries = scan([str(tree)])
    b = {x["label"]: x for x in bins(entries)}
    assert b["drums loops"]["count"] == 1
    assert b["drums samples"]["count"] == 1
    assert b["bass loops"]["count"] == 1
    assert b["vocal samples"]["count"] == 1
    assert all(x["query"].startswith("find ") for x in b.values())
