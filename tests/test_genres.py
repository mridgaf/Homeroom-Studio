"""The Styles roster — subgenre identity held against the live engine.

Owner rule 2026-07-19: "the genres do not have to follow any of the
rules, so they stay true to the genre." So these tests are the MIRROR of
tests/test_variety.py. That file guards the nine against sameness drift;
this one guards the seventeen against FIDELITY drift — the failure mode
here is a beat that stopped being its genre, not one that repeated.

Concretely, nothing in here asks a style to vary its spine. It asks:
does the dembow survive the whole pipeline? Is the swing still pinned?
Did a house rule quietly overwrite a style's own choice?
"""
import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import beat_machine as BM                                    # noqa: E402
import crew                                                  # noqa: E402
import genres                                                # noqa: E402
from crew import CREW, GENRE_NAMES                           # noqa: E402

STYLES = sorted(GENRE_NAMES, key=lambda n: CREW[n]["num"])
CANON_STYLES = [n for n in STYLES if CREW[n].get("canon")]
VARIANTS = range(2, 14)


def _beat(name, v):
    """One style's preset through the FULL pipeline — compose + the
    per-beat variety pass — which is where fidelity actually has to
    survive, not just at compose time."""
    p, notes = BM.solo_preset(name, v, None)
    vnotes = BM.vary_preset(p, v, CREW[name]["num"], tempo_locked=False)
    return p, notes + vnotes


# ------------------------------------------------------ the roster

def test_eighteen_styles_and_no_collisions():
    # 17 subgenres + Chiptune (added 2026-07-24). The count is pinned on
    # purpose: adding a style needs a kick bank and a title pool too, and
    # this catches a half-added one.
    assert len(STYLES) == 18
    assert not (GENRE_NAMES & crew.LEGEND_NAMES)
    nums = [CREW[n]["num"] for n in STYLES]
    assert len(set(nums)) == len(nums)          # unique on the page
    others = {CREW[n]["num"] for n in set(CREW) - GENRE_NAMES}
    assert not (set(nums) & others)             # and across all rosters


def test_every_style_is_flagged_and_pinned():
    for n in STYLES:
        assert CREW[n]["genre"] is True, n      # the flag IS the rules
        assert CREW[n].get("genre_swing") is not None, n
        assert CREW[n].get("density") in ("sparse", "home", "busy"), n


# -------------------------------------------------- canon fidelity

@pytest.mark.parametrize("name", CANON_STYLES)
def test_canon_survives_the_whole_pipeline(name):
    """The figure that DEFINES the style is still intact after compose
    and the variety pass. This is the single most important test here:
    if it fails, a reggaeton stopped being a reggaeton."""
    canon = CREW[name]["canon"]
    for v in VARIANTS:
        p, _ = _beat(name, v)
        for lane, figures in canon.items():
            bar = p["lanes"][lane][3][0]
            assert bar in figures, (name, v, lane, bar)


def test_the_dembow_is_the_dembow():
    """Reggaeton's snare is the tresillo cell — kick, +3, +6, mirrored.
    Spelled out so a future edit to the grammar can't quietly move it."""
    for fig in genres.DEMBOW_SNARE:
        hits = [i for i, c in enumerate(fig) if c in "Xx"]
        assert hits[:4] == [3, 6, 11, 14], fig


def test_baltimore_is_the_doubled_tresillo():
    """The Bmore 8-count: 0 +3 +6, then 8 +11 +14."""
    for fig in genres.BMORE_KICK:
        hits = [i for i, c in enumerate(fig) if c in "Xx"]
        assert hits[:3] == [0, 3, 6], fig
        assert 8 in hits, fig


@pytest.mark.parametrize("name", CANON_STYLES)
def test_canon_lanes_are_protected_from_the_variety_pass(name):
    for v in VARIANTS:
        p, _ = _beat(name, v)
        assert set(p.get("_canon") or ()) == set(CREW[name]["canon"]), name


# ------------------------------------------- the style's own choices

@pytest.mark.parametrize("name", STYLES)
def test_swing_never_wanders(name):
    """A style's feel is pinned — no ±6 wander, no straight/triplet
    outliers, and guest lanes ride the style's swing instead of the
    crew's coin-flip to 50."""
    pinned = CREW[name]["genre_swing"]
    for v in VARIANTS:
        p, _ = _beat(name, v)
        got = {s[2][2] for ln, s in p["lanes"].items()
               if not ln.startswith("stamp")}
        assert got == {pinned}, (name, v, sorted(got))


@pytest.mark.parametrize("name", STYLES)
def test_density_is_the_styles_own(name):
    """Genre fidelity beats the house sparse-bed lean inside this box
    (owner decision 2026-07-19), so the declared profile is what runs."""
    want = CREW[name]["density"]
    for v in VARIANTS:
        _, notes = _beat(name, v)
        assert f"{want} density" in notes, (name, v)


@pytest.mark.parametrize("name", STYLES)
def test_no_odd_meter_or_exotic_grids(name):
    """There is no such thing as a 6/8 Baltimore club record."""
    for v in VARIANTS:
        p, _ = _beat(name, v)
        assert tuple(p.get("tsig", (4, 4))) == (4, 4), (name, v)


def test_styles_never_evolve():
    """A genre is a tradition, not a career — evolution must skip them."""
    import evolution
    assert hasattr(evolution, "maybe_evolve")
    src = Path(__file__).resolve().parent.parent / "tools" / "beat_machine.py"
    text = src.read_text()
    assert "n not in GENRE_NAMES" in text        # filtered before evolving


def test_kick_banks_never_pollinate_into_a_style():
    """The loose nine may borrow a style's book; nothing borrows INTO
    one, or the figure stops being the figure."""
    src = (Path(__file__).resolve().parent.parent / "tools"
           / "pattern_gen.py").read_text()
    assert "not legend and not genre" in src


# ------------------------------------------------- variety, honestly
# Not a spine test. A style repeats its spine on purpose; what must NOT
# repeat is the whole beat.

@pytest.mark.parametrize("name", STYLES)
def test_no_two_beats_are_the_same_beat(name):
    seen = set()
    for v in range(2, 30):
        p, _ = _beat(name, v)
        sig = tuple(sorted((ln, tuple(spec[3]))
                           for ln, spec in p["lanes"].items()))
        assert sig not in seen, (name, v)
        seen.add(sig)


@pytest.mark.parametrize("name", STYLES)
def test_timekeepers_stay_subtle_and_unparked(name):
    """The one house rule the styles DO keep: his voice owns the mids,
    so no timekeeper lane is parked hard on one side."""
    for ln in ("hat", "snap"):
        spec = CREW[name]["lanes"].get(ln)
        if spec:
            assert abs(spec[0]) <= 0.2, (name, ln, spec[0])
