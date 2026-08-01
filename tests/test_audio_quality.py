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

    hopeless = chord_vs_kick(0.02)
    normal = chord_vs_kick(1.0)
    # it helps...
    assert hopeless > -30.0, "the governor did nothing at all"
    # ...but it does not pretend it can fix everything
    assert hopeless < normal - 5.0, (
        "the +/-12 dB clamp is not holding — a 34 dB deficit was fully "
        "corrected, which means noise floors are being amplified into mixes")


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
