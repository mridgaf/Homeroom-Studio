"""Checkpoint 3: numeric verification of the nine personality presets."""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).parent.parent / "tools"))
import crew
from crew import BARS, CREW, render_crew_beat
from groove import OWNER_TASTE

SR = 44100


def test_roster_is_the_agreed_eleven():
    # Snap Church retired 2026-07-15 (too close to Night Metro/Rage
    # Engine); New Math holds slot 9. Half Light (10) and Fast Water (11)
    # were added 2026-08-07/08 and came back off never-guess-hooks on
    # 2026-09-03 -- they had been stranded on that branch, not dropped.
    # The Legends are a separate roster and are excluded here.
    loose = {n for n in CREW if n not in crew.LEGEND_NAMES
             and n not in crew.GENRE_NAMES}
    assert loose == {"Otto Grit", "Cutz", "Crate Prophet", "Chrome Dial",
                     "Glass Cat", "Sunday Chop", "Night Metro",
                     "Rage Engine", "New Math", "Half Light", "Fast Water"}
    assert sorted(CREW[n]["num"] for n in loose) == list(range(1, 12))


def test_every_lane_is_eight_valid_bars():
    for name, p in CREW.items():
        for lane, (pan, gain, feel, bars) in p["lanes"].items():
            assert len(bars) == BARS, (name, lane)
            for b in bars:
                # 16ths, 32nds, or New Math's 20-step quintuplet grid
                assert len(b) in (16, 20, 32), (name, lane, len(b))
                assert set(b) <= set("Xxo.-"), (name, lane)
            assert -1 <= pan <= 1 and 0 < gain <= 1.0
            assert lane in p["kit"], (name, lane)


def test_machine_truth_dust_only_for_the_90s_heads():
    # research: SP-1200 dust belongs to the 90s; ASR-10/MPC3000 stay clean.
    # The Legends carry their own producer's grit level, so they're out.
    for name, p in CREW.items():
        if name in crew.LEGEND_NAMES or name in crew.GENRE_NAMES:
            continue
        if p["era"] == "90s":
            # Otto Grit is the one head who has actually HEARD his dust:
            # the 2026-09-03 audition, where his verdict was "c Plus, dust
            # too much". So his sits under the house amount by ear rather
            # than at it. Everyone else is still on the house number
            # because nobody has judged theirs yet.
            if name == "Otto Grit":
                assert 0.0 < p["dust"] < OWNER_TASTE["sp1200_amount"], name
            else:
                assert p["dust"] == OWNER_TASTE["sp1200_amount"], name
        else:
            assert p["dust"] == 0.0, name


def test_exactly_one_prototype_skips_sidechain():
    # the owner's 1-in-10 rule, applied deterministically to one of nine
    skips = [n for n, p in CREW.items() if p["sidechain"] == 0]
    assert skips == ["Crate Prophet"]


def test_house_snare_space_is_gated_everywhere():
    # the house treatment for the nine. Legends follow their producer —
    # Farrow and Mustang are documented bone-dry — so they're excluded.
    for name, p in CREW.items():
        space, on = p["space"]
        if name not in crew.LEGEND_NAMES \
                and name not in crew.GENRE_NAMES:
            assert space == "gated", name
        assert all(lane in p["lanes"] for lane in on), name


def test_owner_taste_lane_feels():
    # AB1: Otto's spine — snare early, kick late, hats straight
    otto = CREW["Otto Grit"]["lanes"]
    assert otto["snare"][2][0] < 0 < otto["kick"][2][0]
    assert otto["hat"][2][2] == 50
    # Premier zone 51-54; golden era 58-62; trap straight
    assert 51 <= CREW["Cutz"]["lanes"]["hat"][2][2] <= 54
    assert 58 <= CREW["Crate Prophet"]["lanes"]["hat"][2][2] <= 62
    for name in ("Night Metro", "Rage Engine"):
        for lane in CREW[name]["lanes"].values():
            assert lane[2][2] == 50, name
    # the documented Neptunes late-clap flam, 10-30 ms
    assert 10 <= CREW["Glass Cat"]["lanes"]["clap"][2][0] <= 30
    # New Math's identity: exactly one lane swings against a straight kit
    nm_swings = [ln[2][2] for ln in CREW["New Math"]["lanes"].values()]
    assert sorted(nm_swings) == [50, 50, 50, 50, 50, 58]
    # ...and the quintuplet hat grid is really there
    assert any(len(b) == 20 for b in CREW["New Math"]["lanes"]["hat"][3])


def test_hat_pans_subtle_and_both_sides():
    # owner feedback 2026-07-15: hats were parked hard right on everyone —
    # timekeeper lanes stay subtle (|pan| <= 0.2) and vary in side
    hats = []
    for name, p in CREW.items():
        for lane in ("hat", "snap"):
            if lane in p["lanes"]:
                pan = p["lanes"][lane][0]
                assert abs(pan) <= 0.2, (name, lane, pan)
                if lane == "hat":
                    hats.append(pan)
    assert any(x < 0 for x in hats) and any(x > 0 for x in hats)


def test_kick_sustain_is_a_range_not_a_constant():
    # owner feedback 2026-07-15: not every beat gets the long drawn-out 808
    for name, p in CREW.items():
        secs = p["kit"]["kick"][3]
        assert isinstance(secs, tuple) and secs[0] < secs[1], name
        assert secs[0] <= 1.0, name          # everyone can reach a thump
    from crew import _resolve_secs
    rolls = {round(_resolve_secs((0.9, 2.2), 7, v), 3) for v in range(6)}
    assert len(rolls) > 3                    # variants really vary


# Razor, 2026-09-05: the ONLY preset without a stamp lane, by the owner's
# own call. His kung-fu stamp asked the fx bucket for clang/metal/gong/sword
# and exactly ONE file in 356 matches any of them — with own_soundbank on
# that lane falls through to a random fx pick, which is how a talking drum
# reached a Dr. Dre beat. His listen line says "sparse dusty arrangement"
# and never names a stamp. kit["stamp"] deliberately STAYS (crew.lock_stamps
# reads it unconditionally); only the pattern is gone. A SECOND name here is
# that decision being made again — say why, in the config's _research_note.
NO_STAMP_LANE = {"Razor"}


def test_every_personality_has_a_stamp():
    for name, p in CREW.items():
        if name in NO_STAMP_LANE:
            assert "stamp" not in p["lanes"], name
            assert "stamp" in p["kit"], name      # lock_stamps needs it
            continue
        assert "stamp" in p["lanes"], name
        bars = p["lanes"]["stamp"][3]
        assert any(set(b) - {"-"} for b in bars), name


def test_grid_accents_cover_every_grid():
    # school 2026-07-15: metric accents must exist off the 16-grid too
    from crew import grid_accent
    # quintuplets: beat-start strong, mid medium, rest soft
    q = [grid_accent(20, s) for s in range(5)]
    assert q[0] == 1.0 and q[2] > q[1] and len(set(q)) >= 3
    # 32nds: beat-starts full, off-32nds softest
    assert grid_accent(32, 0) == 1.0
    assert grid_accent(32, 1) < grid_accent(32, 2) < 1.0
    # 16ths untouched (velocity() already handles them)
    assert all(grid_accent(16, s) == 1.0 for s in range(16))


def test_roughness_am_modulates_without_clipping():
    from groove import roughness_am
    x = np.ones(SR)                        # 1 s of DC "tail"
    y = roughness_am(x, rate_hz=40.0, depth=0.35)
    assert y.max() <= 1.0 and y.min() >= 0.64   # depth bounds respected
    spec = np.abs(np.fft.rfft(y - y.mean()))
    assert spec.argmax() == 40                  # envelope beats at 40 Hz


def _tone_kit(p):
    """Synthetic stand-in kit: short decaying tones, one per lane."""
    kit = {}
    t = np.arange(int(0.25 * SR)) / SR
    for i, lane in enumerate(p["lanes"]):
        f = 60.0 if lane == "kick" else 200.0 + 120.0 * i
        kit[lane] = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.06) * 0.5
    return kit


def test_render_is_loop_length_and_loudness_true():
    p = CREW["Otto Grit"]
    L, R, got = render_crew_beat("Otto Grit", _tone_kit(p))
    assert len(L) == len(R) == int(round(BARS * 240.0 / p["bpm"] * SR))
    # the house master aims at OWNER_TASTE["master_lufs"]; a sparse
    # synthetic kit lands a bit shy
    assert abs(got - OWNER_TASTE["master_lufs"]) < 2.0
    assert np.abs(L).max() <= 1.0 and np.abs(R).max() <= 1.0
    assert np.sqrt((L ** 2).mean()) > 1e-3              # not silence


def test_alt_render_differs_from_house():
    p = CREW["Glass Cat"]
    kit = _tone_kit(p)
    Lg, _, _ = render_crew_beat("Glass Cat", kit)
    Ld, _, _ = render_crew_beat("Glass Cat", kit, space="dry")
    assert not np.allclose(Lg, Ld)                      # gate audibly there


def _wav_pool(tmp_path, n=3):
    """A little library: n distinct loadable wavs offered for every role."""
    import wave
    files = []
    for i in range(n):
        f = tmp_path / f"shot_808_{chr(97 + i)}.wav"
        x = (np.sin(2 * np.pi * (55 + 20 * i) * np.arange(SR // 4) / SR)
             * 32000).astype("<i2")
        with wave.open(str(f), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(x.tobytes())
        files.append(f)
    # `vox` is in this list because of a real 2026-09-05 failure, not for
    # completeness: Mustang's stamp moved from the fx bucket to the vox
    # bucket that day, and with own_soundbank now honoured in lock_stamps
    # a role the pool never offered came back with an empty path. The pool
    # must offer every role any preset's stamp can name.
    return {role: [{"name": f.stem, "path": str(f)} for f in files]
            for role in ("kick", "snare", "hat", "clap", "snap", "perc",
                         "bongo", "fx", "crash", "rim", "vox")}


def test_stamp_locks_but_drums_experiment(tmp_path, monkeypatch):
    monkeypatch.setattr(crew, "LOCK", tmp_path / "crew_kits.json")
    shots = _wav_pool(tmp_path)
    stamps1 = crew.lock_stamps(shots)
    assert all(path for path, _ in stamps1.values())
    # the stamp is the identity: a second call with an EMPTY pool must
    # reuse the saved paths, never re-pick
    stamps2 = crew.lock_stamps({r: [] for r in shots})
    assert {n: s[0] for n, s in stamps2.items()} \
        == {n: s[0] for n, s in stamps1.items()}
    # ...while kick/snare EXPERIMENT: across variants the same character
    # reaches for different drums (owner rule 2026-07-14)
    picks = set()
    for variant in range(5):
        kit, src = crew.build_kit(shots, "Otto Grit",
                                  stamps1["Otto Grit"][1], variant=variant)
        assert set(src) == {"kick", "snare", "hat"}     # stamp not re-picked
        assert all(src.values())
        picks.add(src["kick"])
    assert len(picks) > 1


def test_the_low_end_ducks_the_same_depth_on_every_path():
    """The sub's duck depth is decided in THREE places — the peak governor's
    measuring envelope, the mix bus, and the stem written to disk. They must
    all read it from `_lane_sc`.

    Caught for real on 2026-09-02: the stem path was still ducking the low
    end at the mix-wide depth while the governor measured it at the deeper
    sub depth, so the governor read the sub as level with the kick and the
    stem he actually opens arrived up to 1.5 dB OVER it. Measuring at a
    point that is not where the sound comes out — the same class as the
    shaker and the hardcoded release. A depth that differs by path is the
    bug, so this asserts the rule at the OUTPUT, not the constant."""
    import copy
    import beat_machine as bm

    # Cutz specifically: with the stem path ducking shallow it measured
    # +1.5 dB over the kick, the worst of the twelve. Otto Grit does NOT
    # work here — its sub sat at -0.0 either way, so a test built on it
    # passed against the broken code and proved nothing.
    p = copy.deepcopy(CREW["Cutz"])
    p["sidechain"] = 0.2                       # the shallow mix-wide depth
    p["sub_sidechain"] = bm.SUB_DUCK_DEFAULT   # the deep one, 5 dB
    assert p["sub_sidechain"] > p["sidechain"], "fixture proves nothing"

    kpan, kgain, (ko, kj, ksw, ks), kbars = p["lanes"]["kick"]
    note, sub_audio = bm._root_sub(p["num"])
    p["lanes"]["sub"] = (0.0, 0.7, (0, 0, ksw, ks + 7), list(kbars))

    shots = crew.build_shots()
    stamps = crew.lock_stamps(shots)
    kit, _ = crew.build_kit(shots, "Cutz", stamps["Cutz"][1], 0)
    kit = dict(kit)
    kit["sub"] = sub_audio

    _L, _R, _got, parts = render_crew_beat("Cutz", kit, preset=p,
                                           want_parts=True)
    pk = {}
    for lane in ("kick", "sub"):
        sL, sR = parts["stems"][lane]
        pk[lane] = float(max(np.abs(sL).max(), np.abs(sR).max()))
    assert pk["kick"] > 0 and pk["sub"] > 0, "no lane to measure"
    over_db = 20 * np.log10(pk["sub"] / pk["kick"])
    assert over_db <= 0.05, (
        "kick stays on top: sub is %+.2f dB over it in the STEM" % over_db)


def test_only_otto_and_doc_day_carry_the_kick_sub_layer():
    """2026-09-03: the sub layer is Otto Grit's researched trait, approved
    on its own audition. It is not a house default — if it ever shows up
    on a preset that was a decision, and this test should be the thing
    that says so out loud.

    It said so. Doc Day (Dre) was given one on 2026-09-05 — "an occasional
    deep sub" is in his own `listen` line, and Mike Elizondo was brought
    into that camp specifically for low-end weight. His is 0.45/0.15s,
    deliberately stronger than Otto's, because sub is named as core to
    that persona rather than incidental. NOT YET APPROVED BY EAR. Anyone
    adding a THIRD is making the same decision again — say so here."""
    have = {n for n, p in CREW.items() if p.get("sub_layer")}
    assert have == {"Otto Grit", "Doc Day"}
    assert CREW["Otto Grit"]["sub_layer"]["amount"] == 0.35
    assert CREW["Doc Day"]["sub_layer"]["amount"] == 0.45


def test_sub_layer_reaches_the_kick_one_shot_not_the_finished_beat():
    """build_kit is the choke point: the sub has to be baked into the raw
    one-shot BEFORE it is tiled across the beat's hits, or only whichever
    hit sits at sample 0 gets reinforced."""
    from unittest.mock import patch
    p = dict(CREW["Otto Grit"])
    seen = {}

    def fake_reinforce(x, **kw):
        seen.update(kw)
        seen["len"] = len(x)
        return x

    with patch("crew._pick_path", return_value=("k.wav", np.ones(1000))), \
            patch("crew.kick_sub_reinforce", side_effect=fake_reinforce):
        crew.build_kit({}, "Otto Grit", np.zeros(10), preset=p)
    assert seen["amount"] == 0.35 and seen["len"] == 1000


def test_allow_dirt_is_eight_presets_not_the_roster():
    """The 2026-07-18 clean-render rule still stands for the roster. Four
    DJs are out of it. Three because he heard them and said so on
    2026-09-03 — Otto Grit "c Plus", Night Metro "c Research" (the 808
    only, mix stays clean), Rage Engine "c Wall half".

    Cutz is the fourth and he got there a different way: 2026-09-03, his
    instruction for the rest of the per-DJ pass was "switch it on live"
    rather than take another audition batch, so his research went
    straight into the config and he judges it while making beats. The
    research is DJ Premier's own documented technique — driving the desk
    hot enough to kiss distortion ("tapping the red"). True, not Night
    Metro's "low": the grit is on the whole signal path, not the 808.

    Crate Prophet is the fifth, 2026-09-04, in by the same door as Cutz
    ("continue tuning DJs", switch it on live). His is the starkest case
    on the roster: his `listen` line calls him "the heaviest vinyl bed
    plus record wow", he carries the loudest vinyl of the nine (-40, vs
    Otto's -48), dust 0.5, and the only `wow` among them — and the
    clean-render rule meant NOT ONE of those numbers had ever played.
    Both producers behind him are documented lo-fi: Pete Rock's SP-1200
    12-bit/26 kHz "dirty Mecca-era tone", Madlib's tape hiss, clipping
    and pitch-warble. True, not "low" — the grit is the whole path, and
    he has kick_dist 0 and mix_sat 0, so what switches on is dust, the
    vinyl bed, wow, and his own 1.3 master drive.

    Razor is the sixth and the first LEGEND on the list, 2026-09-05, asked
    in plain language and answered "yes - and turn the wow up too". His is
    the same shape as Crate Prophet's, worse: he carries the loudest vinyl
    bed on the whole roster (-38), dust 0.6 - which IS the SP-1200 stage,
    crew.py feeds `dust` into groove.sp1200 as its wet amount - wow, and a
    1.35 drive, and not one of them had ever reached a beat. Sourced: the
    Gearspace RZA thread ("he wanted the console into the red for gritty and
    raw sound", "still big saturated rza kick") and Sweetwater's 36 Chambers
    gear piece (SP-1200 at 12-bit/26.04 kHz). True, not "low" - his grit is
    the whole path, and unlike Crate Prophet he also carries mix_sat 1.5 and
    kick_dist 3.0 from the same sources.

    Mustang is the seventh, 2026-09-05, and he is the only one on this
    list who went the OTHER way. Asked in plain language, he answered
    "yes - 808 only, mix stays clean", so Mustang is "low", not True.
    His own `listen` line says "clean digital" and the clean-render rule
    agrees with him — there was no buried grime to switch on, unlike
    Razor and Crate Prophet. What the sources call for is the bass
    specifically: Mustard's records are built on a distorted 808, so the
    dirt is scoped to the 808 and the rest of the path stays clean. Same
    shape as Night Metro, and the amount was MEASURED, not guessed —
    kick_dist swept 4/6/9/12/16 because 4.0 was inaudible (20.2 dB under
    the clean render), landing at 9.0.

    Kane East is the eighth, 2026-09-05, and he arrived by a route
    none of the others took: his was a DELETION, not a switch-on. His old
    line promised "warm light dust and a vinyl bed" and, with no
    allow_dirt, not one of those numbers had ever played — the same
    buried-grime fault as Razor and Crate Prophet. But the era moved the
    same day (he was a duplicate of Sunday Chop in the nine, so he was
    rebuilt as Yeezus), and a soul-era vinyl bed under an industrial
    record is the wrong fix. So dust went to 0.0 and vinyl to -80, and
    allow_dirt True is here for the OTHER stages it gates: kick_dist 6.0
    and mix_sat 3.0, which Wikipedia's Yeezus article calls for in as
    many words — "distorted drum machines and synthesizers". Turning a
    dead setting on is not always the fix; sometimes the setting was the
    wrong one and the honest move is to stop promising it.

    The house rule itself is untouched, and nobody joins this list
    without either an audition or him saying to switch it on."""
    assert OWNER_TASTE["clean_renders"] is True
    heard = {n: p["allow_dirt"] for n, p in CREW.items() if p.get("allow_dirt")}
    assert heard == {"Otto Grit": True, "Night Metro": "low",
                     "Rage Engine": True, "Cutz": True,
                     "Crate Prophet": True, "Razor": True,
                     "Mustang": "low", "Kane East": True}, heard


def test_per_dj_effects_come_off_the_preset_but_a_caller_still_wins():
    """render_crew_beat reads mix_eq/backbeat_echo/chorus/phaser off the
    preset (that IS the per-DJ rollout), and an explicit keyword still
    overrides it — which is what the A/B scripts rely on."""
    from unittest.mock import patch
    p = dict(CREW["Otto Grit"], mix_eq={"low_db": 3.0, "low_hz": 120.0,
                                        "mid_db": 0.0, "mid_hz": 800.0,
                                        "mid_q": 0.9, "high_db": 0.0,
                                        "high_hz": 8000.0})
    kit = _tone_kit(p)
    calls = []
    real_eq = __import__("audio_engine").eq3

    def spy(L, R, **kw):
        calls.append(kw["low_db"])
        return real_eq(L, R, **kw)

    with patch("audio_engine.eq3", side_effect=spy):
        render_crew_beat("Otto Grit", kit, preset=p)
        render_crew_beat("Otto Grit", kit, preset=p,
                         eq=dict(p["mix_eq"], low_db=6.0))
    assert calls == [3.0, 6.0]
    # A preset with NO mix_eq of its own falls back to the house EQ
    # (owner 2026-09-03: "I want to use the mix EQ ... on any DJs that
    # don't have specified EQs", scope confirmed as everything without
    # its own). This used to assert no EQ call at all; the EQ is the one
    # of the four that is now the default rather than opt-in.
    calls.clear()
    bare = dict(CREW["Cutz"])
    bare.pop("mix_eq", None)
    with patch("audio_engine.eq3", side_effect=spy):
        render_crew_beat("Cutz", kit, preset=bare)
    assert calls == [OWNER_TASTE["mix_eq"]["low_db"]]


def test_breakdown_empties_the_bar_for_every_lane_but_the_kept_one():
    """Night Metro's signature moment (owner 2026-09-03, "fix it now").
    Pinned in render_crew_beat because that loop is the one place EVERY
    render path passes through and the only place the chord lanes exist
    beside the drums."""
    kit = _tone_kit(CREW["Night Metro"])
    bar_s = 4 * 60.0 / CREW["Night Metro"]["bpm"]

    def bar5_energy(preset):
        L, R, _ = render_crew_beat("Night Metro", kit, preset=preset)
        m = 0.5 * (np.asarray(L) + np.asarray(R))
        # bar 5, above 2 kHz — the 808 is KEPT, so a full-band measure
        # would mostly measure the thing that did not leave
        X = np.fft.rfft(m)
        X[np.fft.rfftfreq(len(m), 1 / SR) < 2000] = 0
        m = np.fft.irfft(X, len(m))
        n = int(round(bar_s * SR))
        return float(np.sqrt((m[4 * n:5 * n] ** 2).mean()))

    # his prototype ALREADY has bar 5 empty, which is exactly why the bug
    # was invisible — compose a busy bar 5 in so the test has something
    # to remove
    busy = json.loads(json.dumps(
        {ln: list(v[3]) for ln, v in CREW["Night Metro"]["lanes"].items()}))
    full = dict(CREW["Night Metro"])
    full["lanes"] = {ln: (v[0], v[1], v[2],
                          [busy[ln][0] if i == 4 else b
                           for i, b in enumerate(busy[ln])])
                     for ln, v in CREW["Night Metro"]["lanes"].items()}
    dropped = dict(full, breakdown={"bar": 5, "keep": ["kick"]})
    # 0.3, not 0: the gated reverb and the samples' own decay ring on
    # from bar 4 into a bar that plays nothing. Measured at ~0.24 — the
    # bar goes quiet, it does not go digitally silent, and that is the
    # sound the research describes.
    assert bar5_energy(dropped) < bar5_energy(full) * 0.3
    # and the kick is still playing in that bar
    kick_only = dict(full, lanes={"kick": full["lanes"]["kick"]},
                     kit={"kick": full["kit"]["kick"],
                          "stamp": full["kit"]["stamp"]},
                     breakdown={"bar": 5, "keep": ["kick"]})
    L, _, _ = render_crew_beat("Night Metro", {"kick": kit["kick"],
                                               "stamp": kit["stamp"]},
                               preset=kick_only)
    n = int(round(bar_s * SR))
    assert np.abs(np.asarray(L)[4 * n:5 * n]).max() > 1e-4


def test_allow_dirt_low_grits_the_808_and_leaves_the_mix_clean():
    """Owner 2026-09-03 opened the clean rule for Night Metro's LOW END
    only — his own research: "distort the 808/kick specifically, don't
    apply that grit to the whole mix." Otto's plain True stays all-in."""
    from unittest.mock import patch
    p = dict(CREW["Night Metro"], dust=0.5, mix_sat=3.0, vinyl=-40,
             allow_dirt="low")
    kit = _tone_kit(p)
    with patch("crew.dist808", side_effect=crew.dist808) as d, \
            patch("crew.sp1200", side_effect=crew.sp1200) as s, \
            patch("crew.sat_unity", side_effect=crew.sat_unity) as sat, \
            patch("crew.master", side_effect=crew.master) as m:
        render_crew_beat("Night Metro", kit, preset=p)
    assert d.called                       # the 808 got its grit
    assert not s.called and not sat.called  # the mix did not
    assert m.call_args.kwargs["drive"] == 0.7   # master stays clean

    # and plain True is still everything, which is what Otto has
    with patch("crew.sp1200", side_effect=crew.sp1200) as s2, \
            patch("crew.master", side_effect=crew.master) as m2:
        render_crew_beat("Night Metro", kit,
                         preset=dict(p, allow_dirt=True))
    assert s2.called and m2.call_args.kwargs["drive"] == p["drive"]


def test_only_night_metro_ships_with_a_breakdown():
    """The drop is ONE DJ's signature moment, approved by ear 2026-09-03.
    It is not a house behaviour and no other preset may grow one without
    its own audition."""
    assert [n for n, q in CREW.items() if q.get("breakdown")] \
        == ["Night Metro"], "the breakdown is his signature, not a house rule"


def test_every_dj_carries_the_personal_twist_he_asked_for():
    """Owner 2026-09-03: "one of the three thrown on either the snare, the
    hat, or the backbeat ... as an addition to every DJ for my own personal
    twist", and he asked me to place them.

    The ruler is the exact placement, not a count — he also said the twist
    is ALWAYS EXTRA on top of whatever a DJ's research asks for, so Otto
    Grit legitimately carries two (the echo his `c Plus` verdict switched
    on, and the chorus that is his twist, whose lane list carries both).
    Rage Engine WAS the one documented veto: he chose "research can veto
    it", and Rage Engine's sources say the mix is glued by saturation, not
    modulation. THE VETO WAS LIFTED 2026-09-04 and this test now guards
    the replacement, not the absence. He asked for "one bonus effect to
    each DJ", was asked back whether that meant the three in flight or all
    nine, and picked all nine off an option that named Rage Engine as the
    only DJ carrying no printed effect at all. So it is his call, made on
    the specific fact — not a veto that got lost in a refactor. What he
    gets is an ECHO, not a chorus or a phaser: the research objection was
    to MODULATION smearing a wall of saturation, and a 1/16 delay throw at
    150 bpm is not modulation. `_no_twist` stays, with its original
    reason, because that reason is still true of chorus and phaser.

    THE 09-04 BONUS EFFECTS WERE REMOVED 2026-09-05. His words: "undo all
    of those newest additions of 2nd bonus effect. I'm sure i no longer
    approve of them." He was asked back about Rage Engine, whose bonus was
    his ONLY effect rather than a second one, and chose to KEEP it — so
    the eight second effects came out (Otto phaser, Cutz/Crate/Chrome
    chorus, Glass Cat/Sunday Chop/Night Metro echo, New Math chorus) and
    his echo stayed. Do not re-add them; this is a verdict, not a gap.
    The twists themselves were never touched — every bonus used a
    DIFFERENT key from that DJ's twist, which is what made the removal a
    clean revert. The approved twist amounts below still hold for all
    eleven.
    """
    from crew import DEFAULT_CREW
    TWIST = {"Otto Grit": ("chorus", "chord"),
             "Cutz": ("backbeat_echo", "snare"),
             "Crate Prophet": ("backbeat_echo", "snare"),
             "Chrome Dial": ("backbeat_echo", "snare"),
             "Glass Cat": ("chorus", "chord"),
             "Sunday Chop": ("phaser", "hat"),
             "Night Metro": ("chorus", "chord"),
             "New Math": ("phaser", "hat"),
             # slots 10 and 11, placed 2026-09-03 when they came back off
             # never-guess-hooks. Half Light has NO hat lane at all, so the
             # phaser twist was impossible on him; he takes the chord
             # chorus the other atmospheric DJs carry. Fast Water is a
             # break record with a real hat, so he takes the hat phaser.
             "Half Light": ("chorus", "chord"),
             "Fast Water": ("phaser", "hat")}
    approved = {"backbeat_echo": OWNER_TASTE["backbeat_echo"],
                "chorus": OWNER_TASTE["chorus"],
                "phaser": OWNER_TASTE["phaser"]}
    assert set(DEFAULT_CREW) - set(TWIST) == {"Rage Engine"}
    p = CREW["Rage Engine"]
    assert p.get("_no_twist"), "the veto lost its written reason"
    # the veto still holds for the two MODULATION effects — that was the
    # documented objection, and nothing has overturned it
    assert not p.get("chorus") and not p.get("phaser"), \
        "Rage Engine's research veto covers modulation; only the echo was lifted"
    assert p.get("backbeat_echo"), "his 2026-09-04 bonus echo went missing"

    for name, (key, lane) in TWIST.items():
        cfg = CREW[name].get(key)
        assert cfg, f"{name} lost its {key}"
        # the echo has no lanes key -- it is built onto the snare/clap
        assert lane in tuple(cfg.get("lanes", ("snare",))), \
            f"{name}'s twist moved off the {lane}"
        for k in ("rate_hz", "depth", "mix", "note", "feedback"):
            if k in approved[key]:
                assert cfg[k] == approved[key][k], f"{name} retuned {key}.{k}"


def test_the_breakdown_moves_shortens_and_skips_beats():
    """Owner 2026-09-03, correcting the drop he had just approved: "I don't
    want the drop to always be in the same spot", "make it shorter", "a
    dropout does not have to be in every beat."

    Checked on the CHOICE rather than on rendered audio: these three
    behaviours are the whole change, and an audio version would be slow
    and would have to re-derive where the drop landed. The audio side was
    measured on 25 composed beats (DECISIONS.md 2026-09-03): 56% got one,
    they used bars 3/5/7, and each lasted 0.50 of a bar.
    """
    bd = CREW["Night Metro"]["breakdown"]
    assert bd.get("bars") and len(bd["bars"]) > 1, "the drop cannot move"
    assert 0.0 < bd.get("len", 1.0) < 1.0, "the drop is still a whole bar"
    assert 0.0 < bd.get("p", 1.0) < 1.0, "every beat still gets one"

    def choose(num, nbars):
        """The same decision render_crew_beat makes, same seeding."""
        cands = [int(x) - 1 for x in bd["bars"] if 0 <= int(x) - 1 < nbars]
        r = np.random.default_rng(num * 104729)
        if cands and r.random() < bd["p"]:
            return cands[int(r.integers(len(cands)))]
        return None

    got = [choose(n, 8) for n in range(200)]
    hit = [g for g in got if g is not None]
    assert 0.4 < len(hit) / len(got) < 0.8, len(hit) / len(got)
    assert len(set(hit)) > 1, "the drop never moves"
    # a 4-bar loop has no bar 5 or 7: it must fall back to the one that
    # fits rather than crash or empty a bar that is not there
    short = [g for g in (choose(n, 4) for n in range(200)) if g is not None]
    assert short and set(short) == {2}, sorted(set(short))


def test_own_soundbank_is_the_new_build_legends_only():
    """2026-07-18 the owner opened every DJ's sound bank: taste tags stop
    gating picks, the whole role pool is fair game. On 2026-09-05 he heard
    what that actually costs — a Dre audition with two sidesticks where
    snares belong, open hats where tight hats belong, and a talking drum —
    and chose the narrow fix: his own tags gate his own picks, HIM ALONE.

    The open bank still stands for the rest. That is his decision, not an
    oversight, and it is deliberately not being widened by anyone who
    happens to notice the same thing later. A NEW name here is that
    decision being made again — say so, here and in the _research_note.

    Razor joined 2026-09-05, the second legend through the new-build pass.
    ORDER MATTERS and is the reason this is not a free flag: his tags were
    audited and rewritten FIRST. Turning it on over the tags he had would
    have gated him to four kicks, two of which are 808s — strictly worse
    than the open bank. Only a preset whose tags have been proved against
    real filenames (tools/legend_newbuild.py --tags) belongs in this set.

    Mustang joined 2026-09-05, the third, same order: tags first, flag
    after. His was the loudest proof yet that the tags are the work and
    the flag is only the switch — his stamp, the "Hey!" chant Billboard
    names as his single identifying feature, was asking the `fx` bucket
    for hey/vocal/chant/yeah and matching ZERO of 356 files, while the
    `vox` bucket holds "Cymatics - Hey Vox". Turning the flag on over
    those tags would have gated his producer tag to nothing at all.

    Farrow joined 2026-09-05, the fourth, tags proved first as always. His
    producer tag had been "Cymatics - LIFE - Rain and Windchimes 4.wav" —
    a field recording of rain on every beat he had ever made — because the
    open bank wiped his click/zap/glitch/laser and lock_stamps picked at
    random. Three presets in a row now where the ONE sample that rides
    every beat was the wrong sound entirely.

    Kane East joined 2026-09-05, the fifth, tags proved first as always,
    and he made it FOUR wrong producer tags in four legends: his lock was
    "Cymatics - LIFE - River - Light 4.wav", a field recording of a
    river, on every beat he had ever made. That run is why
    tools/make_legend_newbuild.py now prints the locked stamp at the head
    of its sample list — build_kit puts it in kit["stamp"] but never in
    `sources`, so the one sample heard on every single beat was the one
    sample the "read the list before you ship it" step could not show."""
    have = {n for n, p in CREW.items() if p.get("own_soundbank")}
    assert have == {"Doc Day", "Razor", "Mustang", "Farrow", "Kane East"}


def test_own_soundbank_honours_taste_tags():
    """The guard is one boolean and inverting it would silently un-fix the
    thing above, so it gets a test that fails loudly. With the house open
    bank ON: a preset without the flag can be handed the off-tag sample;
    one with it can never be."""
    from unittest.mock import patch

    pool = {"hat": [{"path": "/x/Hats_OHs_162.aif", "name": "Hats_OHs_162"},
                    {"path": "/x/Hat_Closed_1.wav", "name": "Hat_Closed_1"}]}
    audio = np.ones(1000)

    def only(*names):
        got = set()
        for seed in range(40):
            with patch("crew._load_choked", return_value=audio):
                path, _ = crew._pick_path(pool, "hat", ["closed"], 0.5, seed,
                                          **kw)
            got.add(Path(path).name)
        return got

    assert crew.OWNER_TASTE.get("open_soundbank"), "premise of this test"

    kw = {}
    assert "Hats_OHs_162.aif" in only(), \
        "open bank: the off-tag open hat is reachable"

    kw = {"own_bank": True}
    assert only() == {"Hat_Closed_1.wav"}, \
        "own_soundbank: the tags gate, so the open hat is never picked"


def test_doc_day_snare_never_leaves_2_and_4():
    """His `listen` line says the snare "NEVER leaves 2 and 4", and on
    2026-09-05 he made that line the tie-breaker for this persona: "Keep
    following the description as the top rule."

    A rule written as NEVER is an invariant, not a weight. It was a
    weight — modes [[backbeat, 0.9], [sparse, 0.1]] — and the one-in-ten
    fired in a real audition render: "----X--.--------", snare on 2 and
    nothing on 4. Pinned to backbeat 1.0. If a future pass reintroduces a
    second mode here, this is the test that should stop it."""
    import copy
    from pattern_gen import compose

    assert CREW["Doc Day"]["grammar"]["snare"]["modes"] == [["backbeat", 1.0]]

    # NOW AN INVARIANT END TO END. Pinning the mode alone did not close
    # it: since 2026-08-01 a legend could take a GROOVE SEED's snare line
    # outright (pattern_gen, 50% when the seed is not already a bare 2&4),
    # which skips the modes entirely — variant 7 composed
    # "--X---x-x---X---", displaced, nothing on beat 2.
    #
    # He was asked rather than one rule being quietly narrowed, and on
    # 2026-09-05 he ruled: "Overrule old decisions when they cause
    # problems." Doc Day now carries snare_locked_24. The 08-01 rule still
    # stands for the other 11 legends, which is who it was measured for.
    assert CREW["Doc Day"].get("snare_locked_24") is True
    assert {n for n, p in CREW.items() if p.get("snare_locked_24")} \
        == {"Doc Day"}, "a second locked preset is a decision, not a default"

    raw = json.loads(json.dumps(CREW["Doc Day"]))
    for v in range(24):
        q = copy.deepcopy(raw)
        compose(q, "Doc Day", v)
        for bar in q["lanes"]["snare"][3]:
            two, four = len(bar) // 4, 3 * len(bar) // 4
            assert bar[two] != "-" and bar[four] != "-", (
                "variant %d left 2 and 4: %s" % (v, bar))


def test_doc_day_plain_kick_flavor_never_reaches_an_808():
    """His kick_flavors carry TWO entries: a 0.1-weight long 808 ("an
    occasional deep sub") and the 0.75-weight plain kick. The plain one
    has to actually be plain — an already-long 808 has no headroom for
    the sub layer, so a beat that rolls one measures nothing and wastes
    an audition slot.

    The tags are FILE-NAME matchers, not intent. "punch" matched exactly
    one file of 525, "VOL5 - Punchy 808"; "boom" matched three, two of
    them "VOL5 - BOOM808/8082". Both words read like his description and
    both quietly delivered 808s. thump/hard are the words that match the
    files his line actually describes."""
    flavors = CREW["Doc Day"]["kick_flavors"]
    plain = [f for f in flavors if f[1] != "808"]
    assert len(plain) == 1, "expected exactly one plain kick flavor"
    assert set(plain[0][2]) == {"thump", "hard"}
    assert set(CREW["Doc Day"]["kit"]["kick"][2]) == {"thump", "hard"}


def test_j_dillo_hats_are_dead_straight():
    """His ABSOLUTE, in his own words: "hats dead straight".

    NEW BUILD 2026-09-06. The config numbers being zero is not the
    invariant — anyone can edit a number. The invariant is the choke point
    in crew.render_crew_beat that zeroes hat offset/jitter/swing when the
    preset asks, so this goes red if that block is deleted. Single-preset
    opt-in, like snare_locked_24: a second one is a decision, not a
    default.
    """
    import inspect
    from crew import CREW
    import crew as _crew

    assert CREW["J Dillo"].get("hats_dead_straight") is True
    assert {n for n, p in CREW.items() if p.get("hats_dead_straight")} \
        == {"J Dillo"}, "a second dead-straight preset is a decision"

    src = inspect.getsource(_crew.render_crew_beat)
    assert 'hats_dead_straight' in src and 'off, jit, swing = 0.0, 0.0, 50' \
        in src, "the choke point that REFUSES is gone; the flag does nothing"

    # and the config it guards has not drifted away from straight either
    for lane, feel in CREW["J Dillo"]["lanes"].items():
        if lane.startswith("hat"):
            off, jit, swing, _seed = feel[2]
            assert (off, jit, swing) == (0, 0, 50), (lane, feel[2])
