"""Nightly Looperman fetcher: the parts that can be checked without the internet.

NOT covered here (needs the real site + the owner's login, tested by hand):
logging in, the real download, the daily cap message, the launchd schedule.
"""
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import nightly_loops as nl


def test_theme_rotates_through_all_four_and_is_stable():
    start = datetime.date(2026, 9, 20)
    names = [nl.theme_for(start + datetime.timedelta(days=i))["name"] for i in range(4)]
    assert len(set(names)) == 4
    assert nl.theme_for(start) == nl.theme_for(start)
    # day 5 repeats day 1
    assert nl.theme_for(start + datetime.timedelta(days=4)) == nl.theme_for(start)


def test_norm_key():
    assert nl.norm_key("D#") == "D#"
    assert nl.norm_key("fm") == "Fm"
    assert nl.norm_key("A minor") == "Am"
    assert nl.norm_key("C major") == "C"
    assert nl.norm_key("Bb") == "Bb"
    assert nl.norm_key("Unknown") is None
    assert nl.norm_key("") is None
    assert nl.norm_key(None) is None
    assert nl.norm_key("H#") is None


def test_clean_slug_strips_tempo_lookalikes():
    assert nl.clean_slug("faith-free-123bpm-lo-fi-synth-loop") == "faith-free-lo-fi-synth-loop"
    assert nl.clean_slug("battle-86-bpm-dark-epic") == "battle-dark-epic"
    assert nl.clean_slug("song-2-of-9") == "song-2-of-9"          # small numbers stay
    assert nl.clean_slug("140") == "loop"                          # never empty


def test_filename_matches_house_convention():
    n = nl.make_filename("3900272", "0413844", "serenity-lofi-keys-free-103bpm", "D#", 103)
    assert n == "looperman-l-3900272-0413844-serenity-lofi-keys-free_D#_103bpm.wav"


def test_filename_without_key_is_c_nokey_and_bpm_optional():
    n = nl.make_filename("1", "0000002", "strange-loop", None, 95)
    assert n.endswith("_C_nokey_95bpm.wav")
    n2 = nl.make_filename("1", "0000002", "strange-loop", "Fm", None)
    assert n2.endswith("_Fm.wav") and "bpm" not in n2


def test_engine_reads_only_the_real_tempo():
    # the engine takes the FIRST bpm-looking token; the slug must not contain one
    import re
    n = nl.make_filename("1", "0000003", "loop-123bpm-and-99-bpm", "Am", 87)
    assert re.findall(r"\d+\s*bpm", n) == ["87bpm"]


DETAIL = """
<div class="player-wrapper" data-hash="5ae9" data-type="loop"
 data-mp3="https://www.looperman.com/media/loops/3900272/looperman-l-3900272-0413844-serenity-lofi-keys.mp3"></div>
<p>Tags :
 103 bpm  Lo-Fi Loops  Synth Loops  4/4  6.27 MB  Key : D#  FL Studio
</p>
<a href="/getfiles/loops/3900272/looperman-l-3900272-0413844-serenity.wav?a=1&amp;b=2">Download</a>
"""


def test_parse_detail_reads_key_bpm_ids_and_download_link():
    d = nl.parse_detail(DETAIL, "serenity-lofi-keys-free-103bpm")
    assert d["key"] == "D#"
    assert d["bpm"] == 103
    assert d["user"] == "3900272" and d["id7"] == "0413844"
    assert d["href"] == "https://www.looperman.com/getfiles/loops/3900272/looperman-l-3900272-0413844-serenity.wav?a=1&b=2"


def test_parse_detail_key_variants():
    for raw, want in [("C#m", "C#m"), ("Fm", "Fm"), ("Bb", "Bb"), ("A", "A"), ("G#", "G#"), ("Dm", "Dm")]:
        d = nl.parse_detail("<p>Tags : 90 bpm Key : %s FL Studio</p>" % raw, "x")
        assert d["key"] == want, (raw, d["key"])


def test_parse_detail_logged_out_has_no_download_link_and_unknown_key():
    page = DETAIL.replace("Key : D#", "Key : Unknown")
    page = page[: page.index("<a href")]
    d = nl.parse_detail(page, "x")
    assert d["href"] is None
    assert d["key"] is None


def test_parse_list_is_ordered_and_unique():
    page = ('<a href="/loops/detail/412190/faith-free">x</a>'
            '<a href="/loops/detail/412190/faith-free#comments">x</a>'
            '<a href="/loops/detail/413282/plugg-lead">y</a>')
    assert nl.parse_list(page) == [("412190", "faith-free"), ("413282", "plugg-lead")]


LOGIN = """
<form id="account" method="post" action="https://www.looperman.com/account/login">
<input type="hidden" name="csrftoken" value="abc123">
<input type="hidden" name="page_token" value="def456">
<input type="email" name="user_email" id="user_email" required>
<input type="password" name="upass" id="upass" required>
<input type="checkbox" name="user_disclaimer" id="user_disclaimer" required>
<input type="checkbox" name="user_remember_code" id="user_remember_code" value="1">
<button type="submit" name="submit" id="submit">Login</button>
</form>
"""


def test_parse_login_form():
    hidden, checks, submit = nl.parse_login_form(LOGIN)
    assert hidden == {"csrftoken": "abc123", "page_token": "def456"}
    assert checks == {"user_disclaimer": "on", "user_remember_code": "1"}
    assert submit == ("submit", "Login")


def test_skip_rules():
    assert nl.skip_reason("rain and thunder", "", "") == "noise/fx/riser"
    assert nl.skip_reason("cool sub riser", "", "") == "noise/fx/riser"
    assert nl.skip_reason("dusty keys", "Drum Loops 90 bpm", "") == "drums"
    assert nl.skip_reason("dusty keys", "", "License: CC BY-NC") == "non-commercial or no-derivatives licence"
    assert nl.skip_reason("dreamy ambient pad", "Pad Loops", "") is None   # tonal ambient is fine


def test_role_folder():
    assert nl.role_for(11, "warm thing") == "Chords"      # pad category
    assert nl.role_for(4, "lofi chords loop") == "Chords"  # synth but says chords
    assert nl.role_for(21, "piano melody") == "Melody"
    assert nl.role_for(3, "guitar lick") == "Melody"


def test_duplicate_detection_from_filenames():
    names = ["looperman-l-6349255-0407075-space-duel_C_143bpm.wav",
             "looperman-l-1-0000001-x_Am.wav", "not-looperman.wav"]
    assert nl.ids_in_names(names) == {"0407075", "0000001"}


def test_classify_download():
    riff = b"RIFF" + b"\x00" * 2000
    assert nl.classify_download(200, riff) == "ok"
    assert nl.classify_download(429, b"download limits are in place, try again in 24 hours") == "cap"
    assert nl.classify_download(429, b"Please try again in a minute") == "wait"
    assert nl.classify_download(200, b"<html>nope</html>" * 200) == "fail"
    assert nl.classify_download(200, b"RIFF") == "fail"      # too small to be audio


def test_dry_run_and_drive_check(tmp_path, monkeypatch):
    monkeypatch.setattr(nl, "LIB_ROOT", str(tmp_path / "missing"))
    monkeypatch.setattr(nl, "NOTES_DIR", str(tmp_path / "notes"))
    assert nl.drive_ok() is False
    code = nl.main(["--count", "5"])
    assert code == 2                                   # drive missing -> stops loudly
    latest = (tmp_path / "notes" / "LATEST.txt").read_text()
    assert "not reachable" in latest
    assert not (tmp_path / "missing").exists()         # nothing created elsewhere


def test_count_is_capped_at_45(tmp_path, monkeypatch):
    monkeypatch.setattr(nl, "LIB_ROOT", str(tmp_path / "missing"))
    monkeypatch.setattr(nl, "NOTES_DIR", str(tmp_path / "notes"))
    seen = {}
    real_run = nl.run
    monkeypatch.setattr(nl, "run", lambda a: seen.setdefault("count", a.count) or 0)
    nl.main(["--count", "500"])
    assert seen["count"] == 45
    monkeypatch.setattr(nl, "run", real_run)
