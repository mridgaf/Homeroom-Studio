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

import crew                                       # noqa: E402
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


def test_the_low_end_stays_mono():
    """The real safety property when adding width anywhere: bass must stay
    centred. A widened low end loses punch and partially cancels on club
    systems and phone speakers. mono_below(120) enforces it; this proves it
    survived the 2026-07-31 ambience work, which deliberately skips kick,
    the sampled 808 and the tuned sub for exactly this reason."""
    name = "Otto Grit"
    L, R, _ = render_crew_beat(name, _tone_kit(CREW[name]), space="room")
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


def test_the_tuned_808_never_gets_louder_than_the_kick():
    """Owner 2026-09-01: "kick stays on top."

    The low end (`crew._LOW_END`) was exempt from the peak ceiling
    ENTIRELY, written when the tuned root 808 could only land on a beat
    with no chords — which, once every identity gained chords_default,
    meant almost never. The moment the 808 came back on chords beats it
    was measured taking the top of the mix at -6.0 dB with the kick pushed
    down to -11 / -16 dB, i.e. 5 to 10 dB over it.

    Now the low end is capped LEVEL with the backbone: it may match the
    kick, never beat it. It stays exempt from the HAT ceiling, which is
    the half of the exemption that was always the point — a sub does not
    belong under a hi-hat.
    """
    name = "Mustang"
    p = copy.deepcopy(CREW[name])
    assert "kick" in p["lanes"]
    # give the identity a sub lane on the kick's own pattern, the way
    # beat_machine's "add the root" does
    kpan, kgain, kfeel, kbars = p["lanes"]["kick"]
    p["lanes"]["sub"] = (0.0, 0.7, kfeel, list(kbars))
    kit = _tone_kit(p)
    kit["sub"] = kit["sub"] * 8.0              # 18 dB hotter than the kick
    _L, _R, _lufs, parts = render_crew_beat(name, kit, preset=p,
                                            want_parts=True)
    stems = parts["stems"]
    kpk = max(np.abs(stems["kick"][0]).max(), np.abs(stems["kick"][1]).max())
    spk = max(np.abs(stems["sub"][0]).max(), np.abs(stems["sub"][1]).max())
    assert kpk > 0 and spk > 0
    assert _db(spk) - _db(kpk) <= 0.5, (
        "the 808 peaks %.1f dB over the kick" % (_db(spk) - _db(kpk)))
    # ...and it is NOT dragged under the hat tier with everything else
    tier = [ln for ln in stems if ln.startswith(crew.HAT_TIER)]
    if tier:
        hpk = max(max(np.abs(stems[ln][0]).max(), np.abs(stems[ln][1]).max())
                  for ln in tier)
        assert _db(spk) > _db(hpk), (
            "the 808 was pulled under the hat — it is exempt from that "
            "ceiling on purpose")


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


def test_nothing_is_louder_than_the_hat_that_is_actually_in_the_beat():
    """Owner 2026-08-31: "everything besides the kick and the snare follows
    the rule of the high hat as far as volume. always quieter."

    THE REGRESSION THIS EXISTS FOR. The rule shipped first as a fixed offset
    under the kick, which equals "under the hat" only while the hat happens
    to sit exactly at its own cap. Rendered over 19 beats with a hat, 5 broke
    the rule the moment the hat sat lower — cutfx +2.8 dB over the hat, perc
    +1.9, and one Otto Grit render with toms 11 dB over.

    So the hat is BURIED here on purpose. A ceiling computed from the kick
    passes this test; only a ceiling measured against the real hat fails it.
    """
    name = "Otto Grit"                    # kick, snare, hat and a stamp
    p = CREW[name]
    assert "hat" in p["lanes"] and "stamp" in p["lanes"]
    kit = _tone_kit(p)
    kit["hat"] = kit["hat"] * 0.05        # ~26 dB down: far below its cap
    kit["stamp"] = kit["stamp"] * 8.0     # and a colour lane running hot
    _L, _R, _lufs, parts = render_crew_beat(name, kit, preset=copy.deepcopy(p),
                                            want_parts=True)
    stems = parts["stems"]
    pk = {ln: max(np.abs(sL).max(), np.abs(sR).max())
          for ln, (sL, sR) in stems.items()}
    hat = pk["hat"]
    assert hat > 0
    for ln, v in pk.items():
        if ln.startswith(crew.BACKBONE_LANES) or ln in crew._LOW_END:
            continue                      # kick, snare and the 808 sit on top
        if ln.startswith(crew.HAT_TIER):
            continue                      # the hat tier IS the ceiling
        assert _db(v) - _db(hat) <= 0.5, (
            "%s peaks %.1f dB OVER the hat" % (ln, _db(v) - _db(hat)))


def test_the_mix_hierarchy_holds_as_absolute_numbers():
    """Guards the CONSTANTS, not just their relationship to each other.

    The first version of this test compared the function against the same
    constants it uses, so it passed with the cut set to -0.0001 dB and passed
    with the hat tier moved 6 dB ABOVE the kick. Every number below is stated
    absolutely for that reason.
    """
    ceil = crew.peak_ceiling_for

    # the hat tier is a real distance under the backbone, not a token one
    assert crew.PERC_UNDER_DB <= -3.0
    for lane in ("hat", "hat2", "clap", "clap2", "snap"):
        assert ceil(lane) == crew.PERC_UNDER_DB, lane

    # the cut is a real cut. -0.0001 dB is not "always quieter".
    assert crew.EXTRA_CUT_DB <= -3.0

    # the backbone is never capped — it IS the reference
    for lane in ("kick", "kick2", "snare", "snare2"):
        assert ceil(lane) is None, lane

    # the low end is capped LEVEL with it: may match the kick, never beat
    # it (owner 2026-09-01, "kick stays on top", after the tuned root 808
    # measured 5-10 dB over the kick on chords beats). Stated as an
    # absolute number, not as "whatever the constant says" — a positive
    # value here would be a licence to rise above the backbone.
    for lane in ("sub", "bass", "sub808", "808"):
        assert ceil(lane) == crew.LOW_END_UNDER_DB, lane
    assert crew.LOW_END_UNDER_DB <= 0.0

    # NOTHING outside the hat tier may be allowed as loud as the hat tier,
    # whatever family it belongs to. This is the assertion that fails if a
    # new family is ever added above the floor.
    hat = crew.PERC_UNDER_DB
    for lane in ("shaker", "tamb", "bongo", "congas2", "perc", "cutfx",
                 "foundfx", "gamefx", "exotic2", "stamp", "stamp2", "bell",
                 "cowbell", "rim", "blips", "mathperc", "woods", "toms",
                 "chord0", "bass0", "crash", "impacts", "riser", "siren",
                 "swellfx", "cymbals", "airs", "a_lane_nobody_wrote_yet"):
        assert ceil(lane) <= hat - 3.0, lane
    for fam in crew.PEAK_CEILING_DB.values():
        assert fam <= crew.PERC_UNDER_DB

    # same instrument, same tier, whatever the pool happened to name the lane
    assert ceil("cymbals") == ceil("crash")
    assert ceil("airs") == ceil("swellfx")

    # a positive EXTRA_CUT_DB must not be able to RAISE a ceiling
    old = crew.EXTRA_CUT_DB
    try:
        crew.EXTRA_CUT_DB = +9.0
        assert ceil("shaker") <= crew.PERC_UNDER_DB
        assert ceil("chord0") <= crew.MELODIC_UNDER_DB
    finally:
        crew.EXTRA_CUT_DB = old


# ------------------------------------------------- the sub's own sidechain

def _drone_beat(name="Otto Grit", secs=2.0, sub_sc=None):
    """A beat whose `sub` lane is one continuous 55 Hz drone.

    A drone is the only honest way to read a duck out of a stem: with a
    normal sub PATTERN the level between kicks depends on where its own
    hits land, so a quiet moment could be the duck or could be a rest. A
    steady tone has nothing in it but the envelope.
    """
    p = copy.deepcopy(CREW[name])
    kit = _tone_kit(p)
    t = np.arange(int(secs * SR)) / SR
    kit["sub"] = np.sin(2 * np.pi * 55.0 * t) * 0.5
    p["lanes"]["sub"] = (0.0, 0.7, (0, 0, 50, 3), ["X" + "-" * 15])
    p["sidechain"] = 0.2
    if sub_sc is not None:
        p["sub_sidechain"] = sub_sc
    else:
        p.pop("sub_sidechain", None)
    _, _, _, parts = render_crew_beat(name, kit, preset=p, want_parts=True)
    sL, sR = parts["stems"]["sub"]
    return np.abs(sL) + np.abs(sR)


def _pump_db(sig):
    """How far the loudest moment of a drone sits above its deepest dip.

    Measured on a windowed RMS, NOT on the raw samples: a 55 Hz sine passes
    through zero 110 times a second, so a straight min/max reads the
    waveform and says ~29 dB of "pump" on a beat with the duck switched
    off. The window is one full cycle, which is the shortest span that
    contains the envelope and nothing else."""
    win = int(SR / 55.0)                    # one cycle of the drone
    n = (int(1.5 * SR) // win) * win        # the drone's first 1.5 s only
    frames = np.sqrt((sig[:n].reshape(-1, win) ** 2).mean(axis=1))
    return _db(frames.max()) - _db(frames.min())


def test_the_sub_ducks_deeper_than_the_rest_of_the_mix():
    """Owner 2026-09-01: "I want sidechain compression on the sub. I haven't
    heard it working at all."

    It WAS working — at the mix-wide depth of 0.2, which is a 1.9 dB dip.
    Below about 3 dB a sub duck is a volume-knob nudge, not pumping, so
    this asserts on decibels measured at the STEM, not on the constant.

    The depth is read from beat_machine, so lowering it is not something
    that can happen quietly: 3.5 dB at the stem is the floor. He settled on
    5 dB by ear (measured 4.35 at the stem — the stem reads a little under
    the envelope because the drone is also carrying the render's own
    level moves).
    """
    from beat_machine import SUB_DUCK_DEFAULT

    deep = _pump_db(_drone_beat(sub_sc=SUB_DUCK_DEFAULT))
    assert deep > 3.5, (
        f"the sub only moves {deep:.1f} dB under the kick — that is back "
        f"toward the inaudible duck the owner reported, not a sidechain")

    # ...and it must be deeper than what the rest of the mix gets, or the
    # split has quietly collapsed back to one number.
    shallow = _pump_db(_drone_beat(sub_sc=0.2))
    assert deep > shallow + 2.0, (
        f"sub duck {deep:.1f} dB vs mix duck {shallow:.1f} dB — the low end "
        f"is not on its own depth any more")


def test_an_old_recipe_replays_at_the_depth_it_was_rendered_with():
    """A saved recipe from before the split carries no `sub_sidechain`. It
    must fall back to the mix-wide depth, or every beat in the library
    re-renders louder-pumping than the file the owner already approved."""
    assert crew.sub_sidechain({"sidechain": 0.2}) == 0.2
    old = _pump_db(_drone_beat(sub_sc=None))
    assert old < 3.0, (
        f"an old recipe replayed with a {old:.1f} dB sub duck; it was "
        f"rendered with ~1.9 dB")


def test_sidechain_off_means_the_sub_is_off_too():
    """The 1-in-10 no-duck beat is the owner's own texture call
    (2026-07-22). A deep sub duck must not sneak into it."""
    from beat_machine import SUB_DUCK_DEFAULT

    assert crew.sub_sidechain({"sidechain": 0.0,
                               "sub_sidechain": SUB_DUCK_DEFAULT}) == 0
    p = copy.deepcopy(CREW["Otto Grit"])
    p["sidechain"] = 0.0
    p["sub_sidechain"] = SUB_DUCK_DEFAULT
    t = np.arange(int(2.0 * SR)) / SR
    kit = _tone_kit(p)
    kit["sub"] = np.sin(2 * np.pi * 55.0 * t) * 0.5
    p["lanes"]["sub"] = (0.0, 0.7, (0, 0, 50, 3), ["X" + "-" * 15])
    _, _, _, parts = render_crew_beat("Otto Grit", kit, preset=p,
                                      want_parts=True)
    sL, sR = parts["stems"]["sub"]
    assert _pump_db(np.abs(sL) + np.abs(sR)) < 1.0


def test_the_peak_governor_measures_the_duck_it_will_actually_apply():
    """`peak_ceiling_for`'s predicted envelope has to match `duck()`, both
    in depth AND across the loop seam.

    The release already drifted here once (hardcoded 0.11 against duck()'s
    0.09) and let every ducked lane through above its cap. The loop wrap was
    the same bug still standing: the prediction snapped back to unity at the
    start while the real duck carried the dip across. A kick ON the seam is
    the case that separates them."""
    from make_drum_beats import duck
    import inspect

    rel = inspect.signature(duck).parameters["rel"].default
    n = int(1.0 * SR)
    kick_at_seam = [n - int(0.05 * SR)]           # 50 ms before the loop point
    real, _ = duck(np.ones(n), np.ones(n), kick_at_seam, depth=0.55,
                   loop=True)
    # the first sample of the loop must already be ducked, not unity
    assert real[0] < 0.75, real[0]
    # and the prediction the governor builds must agree with it
    L = int(rel * 3 * SR)
    g = np.ones(n + L)
    dip = 1 - 0.55 * np.exp(-np.arange(L) / (rel * SR))
    for pos in kick_at_seam:
        g[pos:pos + L] = np.minimum(g[pos:pos + L], dip[:len(g) - pos])
    g[:L] = np.minimum(g[:L], g[n:])
    assert np.allclose(g[:n], real, atol=1e-9)
