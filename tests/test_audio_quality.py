"""Tests that LISTEN to the render instead of inspecting dictionaries.

Why this file exists (2026-07-31): the suite was 732 tests green while every
one of these defects was shipping, because nothing asserted on the audio
itself — only on file existence, recipe keys and parser behaviour. Each test
below was written against a defect measured in the real library, and each one
FAILS on the code as it stood before 2026-07-31:

  * the mix was effectively mono (side energy 22-31 dB under mid; 247 of 247
    core stems bit-identical L/R) because make_ir() has always returned a
    stereo pair and both reverb paths threw the right channel away
  * 17 of 506 stems (3.4%) were written as digital silence while still being
    listed as live lanes

Keep adding to this file rather than to the orchestration suites. The rule:
if the owner had to use his ears to find it, it belongs here.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from crew import CREW, render_crew_beat            # noqa: E402
from groove import gated_reverb                    # noqa: E402
from make_drum_loops import SR                     # noqa: E402


def _db(v):
    return 20.0 * np.log10(float(v) + 1e-20)


def _side_vs_mid_db(L, R):
    """How wide the mix is. -inf is pure mono; commercial beats sit around
    -6 to -12 dB. Anything past about -20 dB reads as flat and small."""
    mid = (L + R) / 2.0
    side = (L - R) / 2.0
    return _db(np.sqrt(np.mean(side ** 2))) - _db(np.sqrt(np.mean(mid ** 2)))


def _tone_kit(p):
    """Synthetic stand-in kit: one short decaying tone per lane. Matches the
    helper in test_crew.py so neither test needs the external drive."""
    kit = {}
    t = np.arange(int(0.25 * SR)) / SR
    for i, lane in enumerate(p["lanes"]):
        f = 60.0 if lane == "kick" else 200.0 + 120.0 * i
        kit[lane] = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.06) * 0.5
    return kit


# --------------------------------------------------------------- width

@pytest.mark.parametrize("space", ["gated", "room", "plate", "hall"])
def test_wet_spaces_produce_a_real_stereo_image(space):
    """A beat with any wet space must not come out mono.

    Measured before the fix: -24 to -30 dB. After: -14 to -17.5 dB. The -22
    threshold sits in the gap, so this fails the moment either reverb path
    goes back to using one IR."""
    name = "Otto Grit"
    L, R, _ = render_crew_beat(name, _tone_kit(CREW[name]), space=space)
    width = _side_vs_mid_db(L, R)
    assert width > -22.0, (
        f"{space} render is effectively mono ({width:.1f} dB side-vs-mid). "
        "The stereo IR's right channel is being discarded again.")


def test_dry_beats_are_still_narrower_than_wet_ones():
    """The counterpart, so the width test can't be satisfied by widening
    everything into mush.

    This used to assert dry beats were near-mono (< -20 dB). The owner's
    standing rule of 2026-07-31 overrides that: "in order to have studio
    ready quality tracks I want you to be able to use reverb and any other
    effect, as much as needed... this overrules any other command where
    sound is concerned." So a dry beat now gets the house ambience bed too,
    and lands around -16 to -22 dB instead of -24 to -30. What must STILL
    hold is the relationship: dry is the narrow end of the range, because
    the DJ's signature snare treatment is what it's doing without."""
    name = "Otto Grit"
    kit = _tone_kit(CREW[name])
    dry, _, _ = render_crew_beat(name, kit, space="dry")
    dryR = render_crew_beat(name, kit, space="dry")[1]
    wet, _, _ = render_crew_beat(name, kit, space="room")
    wetR = render_crew_beat(name, kit, space="room")[1]
    assert _side_vs_mid_db(dry, dryR) < _side_vs_mid_db(wet, wetR), \
        "a dry beat is no narrower than a wet one — the spaces stopped " \
        "meaning anything"


@pytest.mark.parametrize("name, space", [
    ("Glass Cat", "dry"),         # a dry roll over a preset that declares gated
    ("Plug", "washed"),           # a space string no reverb branch implements
    ("Swish Beatz", "gated"),     # wet roll: the space list names clap, not snare
    ("Hitt Kid", "dry"),          # ...and the sibling is panned off centre
    ("Acid Rap Bright", "room"),  # a genre locked to its own space
    ("Baltimore Club", "dry"),    # a genre whose style locks it to dry
])
def test_no_live_lane_ships_in_mono(name, space):
    """The invariant behind three separate bugs, all the same shape: a lane
    that nothing treated, excluded from the house ambience bed anyway, and
    printed with the two channels carrying the same signal.

    This is the check the full-band side-vs-mid figure keeps missing. A
    kick-dominated drums-only beat can read -25 dB and be fine (every audible
    lane genuinely wide, the kick just 20 dB louder than all of them), while
    a beat reading -21 dB can have its backbeat playing in mono.

    THE METRIC IS CORRELATION, and two cheaper ones are wrong. array_equal
    passes on the broken code: the constant-power pan's cos and sin differ in
    the last bit, so L and R are never EXACTLY equal. A side-vs-mid floor is
    worse than it looks — an untreated mono lane's side-vs-mid is a pure
    function of its pan (dead centre -320 dB, pan 0.1 -22 dB, pan 0.35
    -11 dB), so any fixed floor only catches lanes panned near centre and
    waves through every mono lane panned wide. Correlation does not care
    about the pan: a mono lane panned anywhere is 1.0 to the last bit, and
    measured across the roster a real treated lane runs 0.67 to 0.96.

    The kick and the low end are exempt and must STAY exempt — they are
    deliberately centred (mono_below(120), and the bed skips them by name)."""
    p = CREW[name]
    _, _, _, parts = render_crew_beat(name, _tone_kit(p), space=space,
                                      want_parts=True)
    exempt = {"kick", "bass", "sub", "vinyl"}
    dead = {ln: round(float(np.corrcoef(sL, sR)[0, 1]), 6)
            for ln, (sL, sR) in parts["stems"].items()
            if ln not in exempt and np.abs(sL).max() > 0
            and float(np.corrcoef(sL, sR)[0, 1]) > 0.999}
    assert not dead, (
        f"{name} on a '{space}' render printed {dead} (L/R correlation) — "
        "nothing treated those lanes and the ambience bed skipped them too.")


@pytest.mark.parametrize("name, space, lane, treated", [
    # the space THIS render rolled is dry, over a preset that declares gated
    # (moved to the stamp lane 2026-09-03 -- see the DJ-profile research)
    ("Glass Cat", "dry", "stamp", "gated"),
    # the sibling backbeat lane: every preset's space list names exactly
    # ONE of snare/clap, so the other one is never the DJ's call and the bed
    # is all it will ever get. (This slot used to be ("Plug", "washed", ...)
    # — a space string no branch implemented. washed is a real plate as of
    # 2026-09-02, so that case no longer exercises the bed at all.)
    ("Swish Beatz", "dry", "clap", "gated"),
])
def test_a_lane_no_space_treated_still_gets_the_ambience_bed(
        name, space, lane, treated):
    """Owner 2026-09-01, "a fresh batch didn't have enough effects".

    The house ambience bed skipped every lane in the preset's space list as
    "already treated — the DJ's call". But the render's space is an ARGUMENT:
    beat_machine rolls gated/dry/room/plate per beat, 35% of them dry, and
    the dry branch treats nothing. So on a dry roll the DJ's snare or clap —
    the loudest lane in the beat after the kick — printed bit-identical L/R
    and was excluded from the bed as well.

    Measured on the 48 beats rendered since the previous crew.py change: 9
    at or under the -22 dB S/M line, 8 of them dry rolls, worst -36.2 dB.
    On this synthetic kit the lane's own stem read -320 dB (that is exact
    digital silence in the side channel) and now reads -11 to -12 dB.

    The second half of the check matters as much as the first: a lane the
    space DID treat must be untouched by this, or the fix has quietly
    replaced the DJ's signature treatment with house air."""
    p = CREW[name]
    kit = _tone_kit(p)
    _, _, _, parts = render_crew_beat(name, kit, space=space, want_parts=True)
    sL, sR = parts["stems"][lane]
    width = _side_vs_mid_db(sL, sR)
    assert width > -22.0, (
        f"{name}'s {lane} came out mono ({width:.1f} dB side-vs-mid) on a "
        f"'{space}' render. Nothing treated it and the ambience bed skipped "
        "it anyway.")

    _, _, _, wet = render_crew_beat(name, kit, space=treated, want_parts=True)
    wL, wR = wet["stems"][lane]
    assert _side_vs_mid_db(wL, wR) > width, (
        f"{name}'s {lane} is no wider under its real {treated} treatment "
        "than under the house bed — the DJ's signature has been diluted.")


@pytest.mark.parametrize("name, space", [("Otto Grit", "room"),
                                        ("Farrow", "dry"),
                                        ("Wonky", "room")])
def test_the_low_end_stays_mono(name, space):
    """The real safety property when adding width anywhere: bass must stay
    centred. A widened low end loses punch and partially cancels on club
    systems and phone speakers. mono_below(120) enforces it; this proves it
    survived the 2026-07-31 ambience work, which deliberately skips kick,
    the sampled 808 and the tuned sub for exactly this reason.

    The three cases are the roster's worst, not a comfortable sample.
    Wonky/room is the single worst combination there is; Farrow/dry is the
    one the widening work moved the most; Otto Grit/room is the original.

    THE RULE IS NOW TRUE BY CONSTRUCTION, and that is the thing to protect.
    Until 2026-09-02 mono_below(120) ran BEFORE master_to_lufs, which
    soft-clips L and R separately — a non-linear stage on two channels that
    differ regenerates side energy under the crossover, so the low end was
    only mono until the very next thing that touched it. Every dB of width
    a beat gained came back as a little more low-frequency side. Measured
    over the roster on this synthetic kit: Wonky/room 0.067, Acid Rap
    Detroit/room 0.054 and three others were breaching the 0.05 limit
    BEFORE any of the 2026-09 work, and the backbeat governor pushed
    Farrow/dry, Wonky/dry and No Alias/dry over as well.

    Centring the bass last fixed all of it: the same cases now measure
    0.00009 to 0.00029, roughly 170x inside the limit, and it cost 0.05 dB
    of peak and 0.00 dB of loudness on real beats. So a failure here does
    not mean "a bit too much width" — it means somebody moved mono_below
    back up the chain, or put a new non-linear stage after it."""
    L, R, _ = render_crew_beat(name, _tone_kit(CREW[name]), space=space)
    side = (L - R) / 2.0
    spec = np.abs(np.fft.rfft(side))
    freqs = np.fft.rfftfreq(len(side), 1.0 / SR)
    low = spec[freqs < 100].sum()
    mid = spec[(freqs >= 300) & (freqs < 4000)].sum()
    assert low < mid * 0.05, \
        f"the side channel has low-end energy (low/mid = {low / mid:.3f})"


def test_gated_reverb_stereo_flag_is_additive():
    """stereo=True must widen without changing what each channel hears.

    The naive assertion here would be 'the mono sum is unchanged', and that
    is false by construction: folding two decorrelated reverb channels to
    mono partially cancels them (measured -2.9 dB on the wet signal alone).
    What must hold instead is that the LEFT channel still receives exactly
    the reverb it always did, so no level downstream needed retuning."""
    rng = np.random.default_rng(0)
    dry = rng.normal(0, 0.1, SR // 2)
    onsets = [0, SR // 8, SR // 4]

    mono = gated_reverb(dry, onsets, loop=True)
    summed, side = gated_reverb(dry, onsets, loop=True, stereo=True)
    left = summed + side

    assert np.allclose(left, mono, atol=1e-9), \
        "the left channel no longer matches the original mono reverb"
    assert np.sqrt(np.mean(side ** 2)) > 1e-6, \
        "stereo=True returned a silent side channel"
    # the mono fold-down must stay close enough that the snare-vs-kick
    # backstop and _track_gain don't need new numbers
    drop = _db(np.sqrt(np.mean(summed ** 2))) - _db(np.sqrt(np.mean(mono ** 2)))
    assert -1.0 < drop <= 0.0, f"mono fold-down moved {drop:.2f} dB"


# -------------------------------------------------------------- silence

def test_no_stem_is_written_as_digital_silence(tmp_path):
    """A lane that makes no sound must not leave a file behind. Dragging a
    silent stem into Reason gets you an empty track and no explanation."""
    from beat_recipes import write_stems

    n = 1000
    live = np.sin(2 * np.pi * 220 * np.arange(n) / SR) * 0.3
    stems = {
        "kick": (live.copy(), live.copy()),
        "blips": (np.zeros(n), np.zeros(n)),     # the real 1623 failure
    }
    folder = write_stems(tmp_path / "Stems", stems)

    written = sorted(p.name for p in Path(folder).glob("*.wav"))
    assert len(written) == 1, f"a silent stem was written: {written}"
    assert "blips" not in " ".join(written).lower()


def test_a_rendered_beat_is_not_silent_and_does_not_clip():
    name = "Otto Grit"
    L, R, _ = render_crew_beat(name, _tone_kit(CREW[name]))
    peak = max(np.abs(L).max(), np.abs(R).max())
    assert peak <= 1.0, "the master clipped"
    assert np.sqrt(np.mean(L ** 2)) > 1e-3, "the render came out silent"
    # NOTE: no DC assertion here. _tone_kit is decaying sines, which carry a
    # real DC component of their own (~3e-3), so a DC check on this fixture
    # would be testing the fixture, not the engine. Real renders measure
    # ~3e-4; that check lives in the real-library test below where it means
    # something.


def test_chord_bus_lands_at_a_consistent_level_under_the_kick():
    """The harmonic bus must be governed, not hoped for.

    Before 2026-07-31 the chord level was an open-loop constant, so where it
    landed depended entirely on how loud the chosen samples happened to be:
    measured across 39 shipped beats, the loudest chord part sat anywhere
    from 5.9 to 24.9 dB under the kick — a 19 dB spread. Raising the
    constant moved the whole range without narrowing it. This asserts the
    governor is doing its job on a deliberately lopsided input."""
    from groove import OWNER_TASTE

    name = "Otto Grit"
    p = CREW[name]
    target = OWNER_TASTE["chord_bus_under_kick_db"]

    def chord_vs_kick(source_level):
        kit = _tone_kit(p)
        lanes = dict(p["lanes"])
        t = np.arange(int(1.5 * SR)) / SR
        pad = np.sin(2 * np.pi * 220 * t) * np.exp(-t / 1.2) * source_level
        for i in range(2):
            lanes["chord%d" % i] = (0.0, 0.3, (0, 0, 50, i), ["X" + "-" * 15])
            kit["chord%d" % i] = pad
        beat = dict(p, lanes=lanes)
        _, _, _, parts = render_crew_beat(name, kit, preset=beat,
                                          want_parts=True)
        stems = parts["stems"]

        def rms(lane):
            sL, sR = stems[lane]
            return np.sqrt(np.mean(sL ** 2) + np.mean(sR ** 2))

        chords = np.sqrt(sum(rms(ln) ** 2 for ln in stems
                             if ln.startswith("chord")))
        return _db(chords) - _db(rms("kick"))

    # Within the governor's design range (it clamps at 4x/0.25x, i.e. +/-12
    # dB, so a pathological sample can't be hauled up 30 dB and drag its own
    # noise floor into the mix). The real library's spread was 19 dB peak to
    # peak, so +/-12 dB covers what actually occurs, with margin.
    quiet = chord_vs_kick(0.15)
    loud = chord_vs_kick(1.0)
    swing_in = 20 * np.log10(1.0 / 0.15)          # ~16.5 dB of input swing
    assert abs(quiet - loud) < 4.0, (
        f"the chord bus is not governed: {swing_in:.0f} dB of input swing "
        f"came through as {abs(quiet - loud):.1f} dB at the mix "
        f"({quiet:.1f} vs {loud:.1f} dB under the kick)")
    for got in (quiet, loud):
        assert -target - 8.0 < got < -target + 8.0, (
            f"chord bus landed {got:.1f} dB under the kick, nowhere near "
            f"the {target:.0f} dB target")


def test_the_chord_governor_refuses_to_rescue_a_hopeless_sample():
    """The clamp is deliberate, so it gets a test of its own rather than
    being quietly loosened the next time something fails.

    A pad 34 dB too quiet must NOT be dragged all the way up — that would
    bring its noise floor with it. It should improve and then stop."""
    from groove import OWNER_TASTE

    name = "Otto Grit"
    p = CREW[name]

    def chord_vs_kick(level):
        kit = _tone_kit(p)
        lanes = dict(p["lanes"])
        t = np.arange(int(1.5 * SR)) / SR
        pad = np.sin(2 * np.pi * 220 * t) * np.exp(-t / 1.2) * level
        for i in range(2):
            lanes["chord%d" % i] = (0.0, 0.3, (0, 0, 50, i), ["X" + "-" * 15])
            kit["chord%d" % i] = pad
        _, _, _, parts = render_crew_beat(name, kit,
                                          preset=dict(p, lanes=lanes),
                                          want_parts=True)
        stems = parts["stems"]

        def rms(lane):
            sL, sR = stems[lane]
            return np.sqrt(np.mean(sL ** 2) + np.mean(sR ** 2))

        chords = np.sqrt(sum(rms(ln) ** 2 for ln in stems
                             if ln.startswith("chord")))
        return _db(chords) - _db(rms("kick"))

    # The level here MUST be derived from the governor's own constants, not
    # hardcoded. It used to be a flat 0.02, which was hopeless against the
    # old 9 dB target and reachable against the 15 dB one (2026-08-03) — so
    # the moment the owner moved a taste constant, this test silently stopped
    # exercising the clamp while still passing. A fixture calibrated to a
    # tunable number is a test that quietly retires itself.
    #
    # The governed range is as wide as the two clamps together: the governor
    # can cut by CHORD_CUT_FLOOR and boost by 4x, so any source inside that
    # span comes out on target and only something BELOW it is hopeless.
    # (Measured on the real transfer curve: flat from source 1.0 all the way
    # down to ~0.03, then it starts falling away.) A first attempt put this
    # at "24 dB past the boost ceiling", which quietly assumed the knee sat
    # at source 1.0 — it does not, and the test failed for that reason
    # rather than for a real defect.
    from crew import CHORD_CUT_FLOOR
    from groove import OWNER_TASTE as _OT
    target = _OT["chord_bus_under_kick_db"]
    ceiling_db = 20 * np.log10(4.0)               # the governor's +12 dB
    cut_db = -20 * np.log10(CHORD_CUT_FLOOR)      # how far it may turn down
    governed_span_db = ceiling_db + cut_db
    hopeless_level = 10 ** (-(governed_span_db + 12.0) / 20.0)

    hopeless = chord_vs_kick(hopeless_level)
    normal = chord_vs_kick(1.0)
    # it helps...
    assert hopeless > -60.0, "the governor did nothing at all"
    # ...but it does not pretend it can fix everything
    assert hopeless < normal - 5.0, (
        "the +%.0f dB boost ceiling is not holding — a source %.0f dB below "
        "the governed span was corrected anyway, which means noise floors "
        "are being amplified into mixes (target %.1f dB under the kick, "
        "governed span %.0f dB)"
        % (ceiling_db, 12.0, target, governed_span_db))


# ----------------------------------------------- the real library (opt-in)

def _beats_root():
    import json
    try:
        root = Path(json.load(open("beats_root.json"))["root"])
    except Exception:
        return None
    return root if root.is_dir() else None


@pytest.mark.skipif(_beats_root() is None,
                    reason="beats library not mounted (TBOTC 3)")
def test_real_beats_are_not_mono_or_silent():
    """Runs only when the drive is connected. Checks what actually shipped,
    which is the thing no synthetic test can prove.

    Scope is 'beats rendered since the renderer last changed', taken from
    crew.py's own mtime. That is the exact question worth asking — does
    output made by the CURRENT code hold up — and it needs no maintenance.

    Two worse versions were tried first: a hard-coded cutoff date (rots, and
    it fired on beat 1187 whose file had been touched since) and a 24-hour
    window (still caught beats rendered earlier the same day, before the
    fix). The back catalogue genuinely IS mono — 1,600-odd beats predate the
    2026-07-31 reverb fix — so failing on those is noise, not signal.

    Skips rather than passing vacuously when nothing new has been rendered."""
    import os
    import wave

    root = _beats_root()
    cutoff = os.path.getmtime(Path(__file__).parent.parent / "tools" / "crew.py")
    checked = 0
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        for wav in folder.glob("*.wav"):
            if os.path.getmtime(wav) < cutoff:
                continue
            with wave.open(str(wav), "rb") as w:
                if w.getsampwidth() != 3 or w.getnchannels() != 2:
                    continue
                raw = w.readframes(w.getnframes())
            a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
            v = (a[:, 0].astype(np.int32) | (a[:, 1].astype(np.int32) << 8)
                 | (a[:, 2].astype(np.int32) << 16))
            v = np.where(v & 0x800000, v - 0x1000000, v)
            x = (v.astype(np.float64) / 8388608.0).reshape(-1, 2)
            assert np.abs(x).max() > 1e-6, f"{wav.name} is silent"
            # DC offset eats headroom and makes stems sum badly in Reason.
            # Threshold is a "something is genuinely wrong" line, not a
            # quality target: measured across the current library, real
            # beats sit between 0.00006 and 0.0015 (about -76 to -56 dBFS).
            # master() removes DC, but the tanh stage downstream of it is
            # nonlinear and puts a little back. 0.01 (-40 dBFS) is an order
            # of magnitude above anything observed.
            assert abs(float(np.mean(x))) < 0.01, f"{wav.name} has DC offset"
            assert _side_vs_mid_db(x[:, 0], x[:, 1]) > -22.0, \
                f"{wav.name} came out mono"
            checked += 1
            if checked >= 12:
                return
    if not checked:
        pytest.skip("no beats rendered in the last day to check")


# ------------------------------------------- peak ceilings (owner 2026-08-01)

def test_a_loud_clap_sample_is_pulled_under_the_kick():
    """Owner 2026-08-01, "clap and crash are being overused".

    The existing bus governors work on RMS, which is blind to a single loud
    transient: measured across 42 rendered beats the clap PEAKED a median
    1.2 dB ABOVE the kick (worst +8.4) while its RMS sat politely underneath.
    A hit that spikes over the kick reads as too much however quiet its
    average is.

    Feeds a deliberately hot clap into a render and asserts the peak ceiling
    hauls it back under the kick."""
    name = "Rage Engine"                       # has both a kick and a clap
    p = CREW[name]
    assert "clap" in p["lanes"], "test needs an identity with a clap lane"
    kit = _tone_kit(p)
    kit["clap"] = kit["clap"] * 8.0            # 18 dB hotter than the kick
    _L, _R, _lufs, parts = render_crew_beat(name, kit, preset=copy.deepcopy(p),
                                            want_parts=True)
    stems = parts["stems"]
    kpk = max(np.abs(stems["kick"][0]).max(), np.abs(stems["kick"][1]).max())
    cpk = max(np.abs(stems["clap"][0]).max(), np.abs(stems["clap"][1]).max())
    assert kpk > 0
    assert _db(cpk) - _db(kpk) <= 0.5, (
        "clap peaks %.1f dB over the kick" % (_db(cpk) - _db(kpk)))


def test_the_peak_ceiling_only_ever_turns_things_down():
    """The ceiling must not RAISE a quiet lane — an identity that deliberately
    tucks its clap away stays tucked away. Guards against someone later
    turning this into a two-way governor like the chord bus, which would
    flatten every personality's balance into one house mix."""
    name = "Rage Engine"
    p = CREW[name]
    kit = _tone_kit(p)
    kit["clap"] = kit["clap"] * 0.02           # deliberately buried
    _L, _R, _lufs, parts = render_crew_beat(name, kit, preset=copy.deepcopy(p),
                                            want_parts=True)
    stems = parts["stems"]
    kpk = max(np.abs(stems["kick"][0]).max(), np.abs(stems["kick"][1]).max())
    cpk = max(np.abs(stems["clap"][0]).max(), np.abs(stems["clap"][1]).max())
    assert _db(cpk) - _db(kpk) < -20.0, (
        "a buried clap was pulled UP to %.1f dB under the kick"
        % (_db(kpk) - _db(cpk)))


# ------------------------------------------ the level cascade (owner 2026-09-02)
#
# Four fixes went in together after the owner reported beats where the kick
# was 17-32 dB louder than everything else. Measured across 16 beats before
# and after, the backbeat's peak relative to the kick went from a 29.8 dB
# spread (-22.8 to +7.0) to a 5.8 dB one (-3.8 to +2.0). One test each, and
# each one fails on the code as it stood on 2026-09-01.
#
# All four use Swish Beatz because it is one of the seven identities that
# TUCK A THIN SNARE UNDER A LOUD CLAP (snare gain 0.50, clap 0.90) — the
# shape that broke the old anchor. An identity with a loud snare hides the
# bug.

_LEVEL_ID = "Swish Beatz"


def _stem_peak(stems, lane):
    return max(np.abs(stems[lane][0]).max(), np.abs(stems[lane][1]).max())


def _stem_rms(stems, lane):
    sL, sR = stems[lane]
    return np.sqrt(np.mean(sL ** 2) + np.mean(sR ** 2))


def _render_levels(kit_edit=None, name=_LEVEL_ID):
    """Render the identity with a synthetic kit and hand back {lane: dB
    relative to the kick's peak} plus the raw stems."""
    p = CREW[name]
    kit = _tone_kit(p)
    if kit_edit is not None:
        kit_edit(kit)
    _L, _R, _lufs, parts = render_crew_beat(name, kit, preset=copy.deepcopy(p),
                                            want_parts=True)
    stems = parts["stems"]
    kpk = _stem_peak(stems, "kick")
    assert kpk > 0
    rel = {ln: _db(_stem_peak(stems, ln)) - _db(kpk) for ln in stems}
    return rel, stems


def test_a_broken_snare_does_not_drag_the_whole_mix_down():
    """The kick is the anchor. Nothing else gets to be.

    Until 2026-09-02 every peak ceiling was measured against
    `min(kick_pk, snare_pk)` — the QUIETER of the kick and the lane spelled
    "snare". On the seven identities that tuck a thin snare under the clap
    that reference was the support layer, not the backbeat: measured inside
    render_crew_beat on beat 2164, kick -2.1, clap -0.9, snare -20.6, and
    every colour lane was cut to sit under the -20.6. The clap lost 26.6 dB,
    the hat 24.1, the bells 20.9. A kick with faint tapping behind it.

    So: turn the snare down 26 dB and the REST of the mix must not move."""
    normal, _ = _render_levels()
    broken, _ = _render_levels(lambda kit: kit.__setitem__(
        "snare", kit["snare"] * 0.05))
    for lane in ("hat", "stamp", "clap"):
        assert abs(normal[lane] - broken[lane]) < 1.5, (
            "a 26 dB snare accident moved the %s by %.1f dB (%.1f -> %.1f "
            "under the kick) — something other than the kick is anchoring "
            "the mix" % (lane, normal[lane] - broken[lane],
                         normal[lane], broken[lane]))
    # and the mix is still a mix, not a kick solo
    assert broken["hat"] > -14.0, (
        "the hat is %.1f dB under the kick with a broken snare in the beat"
        % broken["hat"])


def test_the_backbeat_is_whichever_lane_carries_it():
    """On a clap-led identity the CLAP is the backbeat and has to survive.

    Same root cause as the test above, seen from the other side: the old
    code treated the lane literally named "snare" as the backbeat, so on
    Swish Beatz (snare 0.50, clap 0.90) the loud clap was measured against
    the quiet snare and cut ~27 dB out of the beat. The backbeat family is
    now snare AND clap together (SNARE_LIKE), governed as one bus."""
    from groove import OWNER_TASTE
    target = OWNER_TASTE["backbeat_bus_under_kick_db"]

    rel, _ = _render_levels(lambda kit: kit.__setitem__(
        "snare", kit["snare"] * 0.05))
    assert rel["clap"] > -(target + 6.0), (
        "the clap — this identity's backbeat — landed %.1f dB under the "
        "kick while the beat's quiet snare lane was intact at whatever "
        "level it happened to be" % rel["clap"])


def test_the_backbeat_bus_is_governed_in_both_directions():
    """Same governor the chord bus got on 2026-07-31, same reason.

    Measured across 64 shipped beats the backbeat sat a median 3.8 dB under
    the kick — right — with a 19.5 dB spread around it (15.7 under to 3.8
    over), entirely from how loud the chosen samples happened to be. The old
    code had a one-way cap ("the snare bus never out-powers the kick"), which
    does nothing at all for the quiet half of that spread.

    Includes the clamp: a hopeless sample must NOT be hauled all the way up,
    for the same reason as the chord bus — it brings its noise floor."""
    from groove import OWNER_TASTE
    target = OWNER_TASTE["backbeat_bus_under_kick_db"]

    def bus_under_kick(level):
        def edit(kit):
            for ln in ("snare", "clap"):
                kit[ln] = kit[ln] / 0.5 * level
        _rel, stems = _render_levels(edit)
        bus = np.sqrt(sum(_stem_rms(stems, ln) ** 2
                          for ln in stems
                          if any(ln.startswith(s) for s in ("snare", "clap"))))
        return _db(_stem_rms(stems, "kick")) - _db(bus)

    quiet = bus_under_kick(0.15)
    loud = bus_under_kick(1.0)
    swing_in = 20 * np.log10(1.0 / 0.15)          # ~16.5 dB of input swing
    assert abs(quiet - loud) < 3.0, (
        "the backbeat bus is not governed: %.0f dB of input swing came "
        "through as %.1f dB at the mix (%.1f vs %.1f under the kick)"
        % (swing_in, abs(quiet - loud), quiet, loud))
    for got in (quiet, loud):
        assert abs(got - target) < 4.0, (
            "backbeat bus landed %.1f dB under the kick, nowhere near the "
            "%.0f dB target" % (got, target))

    # the +12 dB boost clamp still holds
    hopeless = bus_under_kick(0.02)
    assert hopeless > target + 8.0, (
        "a backbeat %.0f dB past the governor's reach was corrected anyway "
        "(landed %.1f dB under the kick) — the boost clamp is not holding "
        "and noise floors are being amplified into mixes"
        % (20 * np.log10(0.5 / 0.02), hopeless))


def test_no_backbeat_lane_peaks_over_the_kick():
    """The backbeat never had a peak ceiling at all.

    peak_ceiling_for() returns None for both BACKBONE_LANES, so the snare's
    peak was measured against nothing: beat 2159's backbeat came out 9.9 dB
    over the kick. The RMS governor above cannot catch this — a short spiky
    hit has a big peak and almost no RMS, so it sails through.

    Per-lane, not just the loudest one: capping only the loudest leaked on
    2162, where the clap got pulled to +2 and then again to -3 as a clap,
    leaving the untouched snare underneath as the loudest thing in the beat
    at +5.4 over the kick."""
    from crew import BACKBEAT_OVER_KICK_DB

    def spike(kit):
        t = np.arange(int(0.25 * SR)) / SR
        # big peak, negligible RMS — invisible to the bus governor
        kit["snare"] = np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.0008) * 4.0

    rel, _ = _render_levels(spike)
    for lane in ("snare", "clap"):
        assert rel[lane] <= BACKBEAT_OVER_KICK_DB + 0.2, (
            "the %s peaks %.1f dB over the kick (ceiling is %.1f)"
            % (lane, rel[lane], BACKBEAT_OVER_KICK_DB))


# ------------------------------------------- "washed" (owner 2026-09-02)

@pytest.mark.parametrize("name", ["Houston Screw", "Emo Hip Hop",
                                  "Horror Rap", "Plug"])
def test_a_washed_preset_gets_a_real_wet_space(name):
    """Four genre presets declare space=("washed", ...) and no reverb branch
    implemented that word, so the string fell through to the "dry" path.
    beat_machine LOCKS a genre to its declared space, so these four never had
    any space treatment on any beat — 24 shipped recipes rolled it — while
    their own style notes say the opposite ("horrorcore is drowned").

    washed is now the plate branch, matching beat_machine.py:977, which has
    always mapped the TYPED word washed -> plate. The same word had been
    meaning two different things depending on who said it.

    The assertion is that identity, not a width threshold. A threshold is the
    wrong tool here: the house ambience bed already puts air on these lanes,
    so on Houston Screw the plate only buys 1.3 dB of side-vs-mid over the
    bed and any number big enough to be meaningful would fail on it. Equality
    with plate is exactly what the change claims, and inequality with dry is
    exactly what was broken."""
    p = CREW[name]
    lane = p["space"][1][0]
    kit = _tone_kit(p)

    def stem(space):
        _, _, _, parts = render_crew_beat(name, kit, space=space,
                                          want_parts=True)
        return parts["stems"][lane]

    washed, plate, dry = stem("washed"), stem("plate"), stem("dry")
    for ch in (0, 1):
        assert np.allclose(washed[ch], plate[ch], atol=1e-12), (
            "%s's %s renders differently under 'washed' than under 'plate' "
            "— the two words are meant to be the same space" % (name, lane))
    moved = max(np.abs(washed[ch] - dry[ch]).max() for ch in (0, 1))
    assert moved > 1e-6, (
        "%s's %s is bit-for-bit identical under 'washed' and 'dry' — the "
        "washed branch is doing nothing at all" % (name, lane))


# ------------------------------------------------- eq / echo switches
# Both added 2026-09-02 for the owner's delay+EQ audition. They are opt-in
# per render; nothing on the roster turns them on. These two tests hold the
# two promises that were made when they went in.


def test_eq_and_echo_off_by_default_change_nothing():
    """Passing eq=None, echo=None must render EXACTLY today's beat.

    The whole case for adding two effects to a mix he already approved was
    that the default path is untouched. That is a claim about bytes, so it
    is asserted on bytes, not on a tolerance."""
    name = "Otto Grit"
    kit = _tone_kit(CREW[name])
    base_L, base_R, base_lufs = render_crew_beat(name, kit, space="gated")
    off_L, off_R, off_lufs = render_crew_beat(name, kit, space="gated",
                                              eq=None, echo=None)
    assert np.array_equal(base_L, off_L)
    assert np.array_equal(base_R, off_R)
    assert base_lufs == off_lufs


def test_echo_does_not_let_the_backbeat_out_power_the_kick():
    """The echo runs BEFORE the backbeat bus governor on purpose.

    Put it after and the repeats are free level: the bus is measured clean,
    trimmed to target, and then handed an echo the governor never saw. The
    owner's hard rule since 2026-07-18 is that the snare bus never
    out-powers the kick, so the echoed bus has to land where the dry one
    does, not above it."""
    name = "Otto Grit"
    kit = _tone_kit(CREW[name])
    echo = {"note": 0.5, "feedback": 0.5, "mix": 0.6}   # deliberately hot
    dry = render_crew_beat(name, kit, space="gated", want_parts=True)[3]
    wet = render_crew_beat(name, kit, space="gated", echo=echo,
                           want_parts=True)[3]

    def bus_over_kick(parts):
        stems = parts["stems"] if isinstance(parts, dict) else parts
        def rms(lane):
            sL, sR = stems[lane]
            return float(np.sqrt(np.mean(sL ** 2 + sR ** 2)))
        back = sum(rms(ln) for ln in stems if ln.startswith(("snare", "clap")))
        return _db(back) - _db(rms("kick"))

    assert bus_over_kick(wet) <= bus_over_kick(dry) + 1.0, (
        "the echo moved the backbeat bus up relative to the kick — it is "
        "being applied after the governor instead of before it")


# ------------------------------------------------- chorus / phaser switches
# Added 2026-09-03 on the same terms as eq/echo above: wired, opt-in per
# render, nothing on the roster turns them on, and NOT yet approved by ear.


def test_chorus_and_phaser_off_by_default_change_nothing():
    """Same bytes promise the eq/echo switches made. Four opt-in effects
    now hang off this function; the default render still has to be the
    beat he already approved."""
    name = "Otto Grit"
    kit = _tone_kit(CREW[name])
    base_L, base_R, base_lufs = render_crew_beat(name, kit, space="gated")
    off_L, off_R, off_lufs = render_crew_beat(name, kit, space="gated",
                                              chorus=None, phaser=None)
    assert np.array_equal(base_L, off_L)
    assert np.array_equal(base_R, off_R)
    assert base_lufs == off_lufs


def test_chorus_dict_without_a_mix_is_not_a_silent_no_op():
    """audio_engine defaults mix to 0 so the Sound Engine rack has an OFF
    position. That default must not leak into the crew path, where passing
    the dict at all means "switch it on" — an effect that silently does
    nothing is this project's most expensive recurring bug."""
    name = "Otto Grit"
    p = dict(CREW[name])
    kit = _tone_kit(p)
    base = render_crew_beat(name, kit, space="gated", want_parts=True)[3]
    # the default lane for chorus is the chords, so put the effect where
    # this kit actually has a lane instead
    wet = render_crew_beat(name, kit, space="gated", want_parts=True,
                           chorus={"lanes": ("hat",)})[3]

    def hat(parts):
        stems = parts["stems"] if isinstance(parts, dict) else parts
        return np.concatenate(stems["hat"])

    assert not np.allclose(hat(base), hat(wet), atol=1e-5), (
        "chorus={} rendered an identical hat — the mix default leaked "
        "through and the effect is off")
