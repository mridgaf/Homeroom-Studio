"""The ban button's data layer (owner 2026-08-31).

The rule he gave: "When I ban a sound, it is banned everywhere. forever."
And, when shown that 17.5% of his 4,202 samples share a file name with
another file: ask each time, so one click never silently takes samples he
did not mean.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import make_drum_beats as mdb


@pytest.fixture
def lib(tmp_path, monkeypatch):
    """Two DIFFERENT sounds that share a file name, plus a third. This is
    the collision the fingerprint exists for."""
    a = tmp_path / "packA" / "Kick 3.wav"
    b = tmp_path / "packB" / "Kick 3.wav"          # same name, other audio
    c = tmp_path / "packA" / "Snare 1.wav"
    for p in (a, b, c):
        p.parent.mkdir(parents=True, exist_ok=True)
    a.write_bytes(b"AAAA" * 40)
    b.write_bytes(b"BBBB" * 60)                    # different bytes AND size
    c.write_bytes(b"CCCC" * 40)
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "banned.json")
    (tmp_path / "banned.json").write_text("[]")
    shots = {"kick": [{"path": str(a)}, {"path": str(b)}],
             "snare": [{"path": str(c)}]}
    return {"a": str(a), "b": str(b), "c": str(c), "shots": shots}


def test_banning_a_sound_spares_the_sample_that_shares_its_name(lib):
    """THE REGRESSION. Banning by file name would have killed both 'Kick 3'
    files. Measured on his library, that mistake was waiting on 17.5% of
    samples; a name+duration key still collided on 14.5%."""
    mdb.ban_sound(lib["a"], shots=lib["shots"])
    assert mdb.is_banned(lib["a"]) is True
    assert mdb.is_banned(lib["b"]) is False, \
        "banned the innocent sample that only shares a name"
    assert mdb.is_banned(lib["c"]) is False


def test_a_ban_survives_the_file_being_moved_or_renamed(lib, tmp_path):
    """A pack re-copied to a new path must not un-ban the sound. This is
    why the entry stores content and not just a path."""
    mdb.ban_sound(lib["a"], shots=lib["shots"])
    moved = tmp_path / "packMOVED" / "Kick 3.wav"
    moved.parent.mkdir(parents=True)
    moved.write_bytes(Path(lib["a"]).read_bytes())
    assert mdb.is_banned(str(moved)) is True


def test_the_broad_ban_still_takes_every_variant(lib):
    """His two hand-typed entries are deliberately broad — "Bang boom Pow"
    kills every date/master variant at once. That behaviour is preserved as
    the explicit whole_name choice."""
    mdb.ban_sound(lib["a"], whole_name=True, shots=lib["shots"])
    assert mdb.is_banned(lib["a"]) is True
    assert mdb.is_banned(lib["b"]) is True, "whole-name ban missed a twin"
    assert mdb.is_banned(lib["c"]) is False


def test_the_button_can_tell_him_how_many_it_would_take(lib):
    """Drives the prompt: one twin bans outright, more than one asks."""
    assert len(mdb.name_twins(lib["a"], lib["shots"])) == 2
    assert len(mdb.name_twins(lib["c"], lib["shots"])) == 1


def test_the_old_hand_typed_list_still_loads(lib, tmp_path):
    """The file began as a bare JSON list. His real one is still that shape
    on disk, so reading it must not need a migration step."""
    (tmp_path / "banned.json").write_text(json.dumps(["Bang boom Pow"]))
    assert mdb.banned_substrings() == ["bang boom pow"]
    assert mdb.is_banned("/x/Bang boom Pow 3-14 master.wav") is True
    # ...and a button ban appends without dropping the curated entries
    mdb.ban_sound(lib["a"], shots=lib["shots"])
    assert "bang boom pow" in mdb.banned_substrings()
    assert mdb.is_banned(lib["a"]) is True


def test_a_banned_sound_leaves_the_generator_pool(lib):
    """End to end: the ban has to reach the thing that picks samples, not
    just the file on disk."""
    mdb.ban_sound(lib["a"], shots=lib["shots"])
    pool = mdb._clean_pool({k: list(v) for k, v in lib["shots"].items()})
    left = {e["path"] for es in pool.values() for e in es}
    assert lib["a"] not in left
    assert lib["b"] in left and lib["c"] in left


def test_an_unreadable_file_never_matches(tmp_path, monkeypatch):
    """A missing file must not fingerprint to something that collides with
    another missing file — that would ban a whole class of samples at once."""
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text("[]")
    assert mdb.sample_fingerprint(tmp_path / "nope.wav") is None
    mdb.ban_sound(str(tmp_path / "nope.wav"))
    assert mdb.is_banned(str(tmp_path / "also-gone.wav")) is False


@pytest.mark.skip(reason="the ban BUTTON (beat_machine.ban_lane) lands in pass 2 with the rest of beat_machine.py; the ban ENGINE it calls is here and tested above")
def test_ban_lane_names_the_lane_not_the_file(tmp_path, monkeypatch):
    """The browser sends a beat number and a lane; the path is resolved
    here from the recipe. Same rule the swap dropdown follows — no client
    string reaches disk unchecked."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
    import beat_machine as bm

    a = tmp_path / "packA" / "Kick 3.wav"
    b = tmp_path / "packB" / "Kick 3.wav"
    for p in (a, b):
        p.parent.mkdir(parents=True, exist_ok=True)
    a.write_bytes(b"AAAA" * 40)
    b.write_bytes(b"BBBB" * 60)
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "banned.json")
    (tmp_path / "banned.json").write_text("[]")
    shots = {"kick": [{"path": str(a)}, {"path": str(b)}]}

    root = tmp_path / "lib"
    (root / ".recipes").mkdir(parents=True)
    (root / ".recipes" / "1.json").write_text(json.dumps(
        {"kit_paths": {"kick": str(a)}, "preset": {}, "kit_spec": {}}))

    # two files share the name, so it ASKS instead of banning
    r = bm.ban_lane(1, "kick", root=root, shots=shots)
    assert r["asked"] is True and r["twins"] == 2
    assert mdb.is_banned(str(a)) is False, "banned before he answered"

    # he picks "only this one"
    r = bm.ban_lane(1, "kick", choice="sound", root=root, shots=shots)
    assert r["asked"] is False
    assert mdb.is_banned(str(a)) is True
    assert mdb.is_banned(str(b)) is False

    # a lane with no sample behind it says so plainly
    (root / ".recipes" / "2.json").write_text(json.dumps(
        {"kit_paths": {}, "preset": {}, "kit_spec": {}}))
    with pytest.raises(ValueError, match="no file to ban"):
        bm.ban_lane(2, "sub", root=root, shots=shots)


# ---- what the adversarial review broke, 2026-09-01 ----

def test_ban_all_of_them_bans_exactly_the_number_he_was_shown(tmp_path,
                                                              monkeypatch):
    """THE CRITICAL ONE. The dialog quotes a count from exact file names,
    but the ban used to append that name to the SUBSTRING list — so
    "ban all 2" could take 5, including a file in a folder that merely
    contained the name, and banning a lane called "Hat" took every path
    containing the letters "hat"."""
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text("[]")
    mk = lambda rel, data: (
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True),
        (tmp_path / rel).write_bytes(data), str(tmp_path / rel))[2]
    a = mk("packA/Kick 3.wav", b"A" * 100)
    b = mk("packB/Kick 3.wav", b"B" * 120)
    c = mk("packC/Kick 30.wav", b"C" * 100)          # NOT a twin
    d = mk("packC/Kick 3 Punchy.wav", b"D" * 100)    # NOT a twin
    e = mk("Kick 3/Some Snare.wav", b"E" * 100)      # folder, not the sound
    shots = {"kick": [{"path": p} for p in (a, b, c, d, e)]}

    shown = len(mdb.name_twins(a, shots))
    assert shown == 2
    mdb.ban_sound(a, whole_name=True, shots=shots)
    hit = [p for p in (a, b, c, d, e) if mdb.is_banned(p)]
    assert len(hit) == shown, (
        "told him %d, banned %d: %s" % (shown, len(hit),
                                        [Path(p).name for p in hit]))
    assert set(hit) == {a, b}
    # banning the same name twice must not stack up entries
    mdb.ban_sound(b, whole_name=True, shots=shots)
    stems = mdb._ban_doc()["stems"]
    assert len(stems) == len(set(x.lower() for x in stems)), stems


def test_a_short_name_does_not_ban_the_whole_drive(tmp_path, monkeypatch):
    """"Hat" as a substring matched "Phat Kick" and "That Snare"."""
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text("[]")
    for n in ("Hat.wav", "Phat Kick.wav", "That Snare.wav"):
        (tmp_path / n).write_bytes(b"x" * 50)
    mdb.ban_sound(str(tmp_path / "Hat.wav"), whole_name=True,
                  shots={"hat": [{"path": str(tmp_path / "Hat.wav")}]})
    assert mdb.is_banned(str(tmp_path / "Hat.wav")) is True
    assert mdb.is_banned(str(tmp_path / "Phat Kick.wav")) is False
    assert mdb.is_banned(str(tmp_path / "That Snare.wav")) is False


def test_a_damaged_ban_file_refuses_instead_of_unbanning_everything(
        tmp_path, monkeypatch):
    """A truncated file used to read back as "nothing is banned", and the
    next ban wrote that emptiness over his hand-typed entries."""
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text('["Bang boom Pow", "Johnny St')
    with pytest.raises(mdb.BanListDamaged):
        mdb.banned_substrings()
    with pytest.raises(mdb.BanListDamaged):
        mdb.is_banned("/x/Bang boom Pow.wav")
    (tmp_path / "sample.wav").write_bytes(b"z" * 40)
    with pytest.raises(mdb.BanListDamaged):
        mdb.ban_sound(str(tmp_path / "sample.wav"))
    # the damaged file is left exactly as it was, not overwritten
    assert (tmp_path / "b.json").read_text() == '["Bang boom Pow", "Johnny St'


def test_the_ban_file_is_never_left_half_written(tmp_path, monkeypatch):
    """Written to a temp file and swapped in, so a crash mid-write cannot
    destroy the list. Checks the swap, and that no debris is left behind."""
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text(json.dumps(["Bang boom Pow"]))
    (tmp_path / "s.wav").write_bytes(b"q" * 40)
    mdb.ban_sound(str(tmp_path / "s.wav"))
    doc = json.loads((tmp_path / "b.json").read_text())
    assert doc["names"] == ["Bang boom Pow"], "lost his hand-typed entry"
    assert len(doc["sounds"]) == 1
    assert not list(tmp_path.glob(".banned-*")), "left a temp file behind"


def test_the_quarantine_tool_sees_a_button_ban(tmp_path, monkeypatch):
    """"Ban it, then collect the beats that used it" stopped working: the
    tool read only the hand-typed names, so a button ban was invisible and
    it reported the blocklist as empty."""
    import quarantine_banned as qb
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text("[]")
    (tmp_path / "s.wav").write_bytes(b"w" * 40)
    mdb.ban_sound(str(tmp_path / "s.wav"))
    doc = mdb._ban_doc()
    ban = ([s.lower() for s in doc["names"]],
           mdb.banned_sounds(doc), mdb.banned_stems(doc))
    assert any(ban), "quarantine would print 'nothing to collect'"
    assert qb.is_banned(str(tmp_path / "s.wav"), *ban) is True


@pytest.mark.skip(reason="the ban BUTTON (beat_machine.ban_lane) lands in pass 2 with the rest of beat_machine.py; the ban ENGINE it calls is here and tested above")
def test_it_asks_when_it_cannot_prove_the_name_is_unique(tmp_path,
                                                         monkeypatch):
    """`shots` is the FILTERED pool, so a path missing from it means the
    twin count is an undercount — which used to ban silently."""
    import beat_machine as bm
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    (tmp_path / "b.json").write_text("[]")
    a = tmp_path / "packA" / "Kick 3.wav"
    a.parent.mkdir(parents=True)
    a.write_bytes(b"A" * 60)
    root = tmp_path / "lib"
    (root / ".recipes").mkdir(parents=True)
    (root / ".recipes" / "1.json").write_text(json.dumps(
        {"kit_paths": {"kick": str(a)}, "preset": {}, "kit_spec": {}}))

    for pool in (None, {}, {"kick": [{"path": "/somewhere/else.wav"}]}):
        r = bm.ban_lane(1, "kick", root=root, shots=pool)
        assert r["asked"] is True, "banned without asking on pool %r" % (pool,)
        assert mdb.is_banned(str(a)) is False

    # ...and it does NOT ask when the file really is alone in the pool
    r = bm.ban_lane(1, "kick", root=root, shots={"kick": [{"path": str(a)}]})
    assert r["asked"] is False
    assert mdb.is_banned(str(a)) is True


def test_the_fingerprint_uses_size_and_a_real_block(tmp_path, monkeypatch):
    """Mutation cover: dropping the size, or reading only a few bytes,
    previously left every test passing."""
    monkeypatch.setattr(mdb, "BANNED_FILE", tmp_path / "b.json")
    # The first 64 KB are IDENTICAL and only the length differs, so these
    # two are told apart by the size component and nothing else. Both files
    # must exceed the read block or the read itself would separate them.
    head = b"H" * 65536
    (tmp_path / "x.wav").write_bytes(head + b"A" * 200)
    (tmp_path / "y.wav").write_bytes(head + b"A" * 300)
    assert mdb.sample_fingerprint(tmp_path / "x.wav") \
        != mdb.sample_fingerprint(tmp_path / "y.wav"), "size is not hashed"
    # same size, differing only well past a short read
    (tmp_path / "p.wav").write_bytes(b"P" * 5000 + b"1" + b"P" * 5000)
    (tmp_path / "q.wav").write_bytes(b"P" * 5000 + b"2" + b"P" * 5000)
    assert mdb.sample_fingerprint(tmp_path / "p.wav") \
        != mdb.sample_fingerprint(tmp_path / "q.wav"), "read block too short"
