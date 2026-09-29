"""Owner 2026-09-28: the rack's dropdowns group sounds by the words in their
names (his synonyms as one group, plain names by pack), and his new synonym
rulings reach every DJ's and genre's picks too -- as whole words only."""
import flavor_tags
from sound_words import group_labels, tokens


def test_names_read_as_whole_words():
    assert tokens("Violin SusVib") == ["violin", "sus", "vib"]
    assert tokens("NoSus") == [] and tokens("Non-Vibrato") == []  # not that word
    assert tokens("Lo Fi Keys") == ["lofi", "keys"]


def test_his_synonyms_are_one_group_and_plain_names_split_by_pack():
    names = ["Horn Stab C", "Brass Hit 2", "Trumpet stac", "Tuba Short",
             "Horn 01", "Spacey Horn", "Psychedelic Brass", "Wet Horn"]
    got = group_labels(names, ["P"] * len(names))
    assert got[0] == got[1] == ["Stab · hit"]              # stab = hit
    assert got[2] == got[3] == ["Short · staccato"]        # staccato = short
    assert got[4] == ["Plain names · P"]
    assert got[5] == got[6]                                # spacey = psychedelic
    assert got[7] == ["Wet"]                               # wet joins washed
    big = ["Kick %d" % i for i in range(20)] + ["Hard Kick", "Heavy Kick"]
    lab = group_labels(big, ["A"] * 10 + ["B"] * 10 + ["C", "C"])
    assert lab[0] == ["Plain names · A"] and lab[15] == ["Plain names · B"]
    assert lab[20] == lab[21] == ["Hard · heavy"]          # "kick" says nothing


def test_his_folder_names_count_as_words():
    """He sorts kicks into folders named "Deep", "Short": a plain name in
    them is a deep/short sound, even when the folder holds most of them."""
    lab = group_labels(["Kick %d" % i for i in range(14)],
                       ["Deep"] * 3 + ["Short"] * 9 + ["Pack"] * 2)
    assert lab[0] == ["Deep"] and lab[5] == ["Short"]
    assert lab[13] == ["Plain names · Pack"]


def test_new_synonyms_reach_dj_picks_as_whole_words_only():
    m = flavor_tags.matches
    assert m("tight", "hat staccato 01") and not m("tight", "kick stack 01")
    assert m("washed", "snare wet") and m("stab", "brass hit 2")
    assert not m("stab", "white noise") and not m("tight", "spicy hat")
    assert m("ambient", "trippy pad") and m("horror", "creepy bell")
    assert not m("stab", "kick chop")                      # chop is NOT stab
    # the older groups keep matching exactly as before
    assert m("tight", "kick_tite_3.wav") and m("dusty", "dustyroom kick")
