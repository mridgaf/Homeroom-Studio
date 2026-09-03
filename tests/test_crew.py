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


def test_roster_is_the_agreed_nine():
    # Snap Church retired 2026-07-15 (too close to Night Metro/Rage
    # Engine); New Math holds slot 9. The Legends (slots 10+) are a
    # separate roster and are excluded here.
    nine = {n for n in CREW if n not in crew.LEGEND_NAMES
            and n not in crew.GENRE_NAMES}
    assert nine == {"Otto Grit", "Cutz", "Crate Prophet", "Chrome Dial",
                    "Glass Cat", "Sunday Chop", "Night Metro",
                    "Rage Engine", "New Math"}
    assert sorted(CREW[n]["num"] for n in nine) == list(range(1, 10))


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


def test_every_personality_has_a_stamp():
    for name, p in CREW.items():
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
    return {role: [{"name": f.stem, "path": str(f)} for f in files]
            for role in ("kick", "snare", "hat", "clap", "snap", "perc",
                         "bongo", "fx", "crash", "rim")}


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


def test_only_otto_carries_the_kick_sub_layer():
    """2026-09-03: the sub layer is Otto Grit's researched trait, approved
    on its own audition. It is not a house default — if it ever shows up
    on a second preset that was a decision, and this test should be the
    thing that says so out loud."""
    have = {n for n, p in CREW.items() if p.get("sub_layer")}
    assert have == {"Otto Grit"}
    assert CREW["Otto Grit"]["sub_layer"]["amount"] == 0.35


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


def test_allow_dirt_is_one_dj_not_the_roster():
    """Owner 2026-09-03 opened the clean-render rule for Otto's dust ONLY
    by ear-audition. Until he says yes, no preset ships with it — and the
    2026-07-18 clean rule stands for everyone."""
    assert OWNER_TASTE["clean_renders"] is True
    assert not [n for n, p in CREW.items() if p.get("allow_dirt")]


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


def test_no_preset_ships_with_a_breakdown_or_dirt_until_he_hears_it():
    """Both mechanisms are built and auditioned, neither is switched on.
    Same contract as every other effect in this pass — approving the
    SOUND is what turns it on, not building it."""
    assert not [n for n, q in CREW.items() if q.get("breakdown")]
    assert not [n for n, q in CREW.items() if q.get("allow_dirt")]


def test_every_dj_carries_exactly_one_personal_twist():
    """Owner 2026-09-03: "one of the three thrown on either the snare, the
    hat, or the backbeat ... as an addition to every DJ for my own personal
    twist", and he asked me to place them.

    One of echo/chorus/phaser per DJ, never two, and the amounts must be
    HIS approved numbers rather than something retuned quietly. Rage Engine
    is the one documented exception — he chose "research can veto it", and
    Rage Engine's sources say the mix is glued by saturation, not
    modulation. If someone drops the veto, this test says so out loud
    rather than letting a wall of sound grow a chorus.
    """
    from crew import DEFAULT_CREW
    nine = list(DEFAULT_CREW)
    approved = {"backbeat_echo": OWNER_TASTE["backbeat_echo"],
                "chorus": OWNER_TASTE["chorus"],
                "phaser": OWNER_TASTE["phaser"]}
    for name in nine:
        p = CREW[name]
        on = [k for k in approved if p.get(k)]
        if name == "Rage Engine":
            assert on == [], f"Rage Engine's veto was dropped: {on}"
            assert p.get("_no_twist"), "the veto lost its written reason"
            continue
        assert len(on) == 1, f"{name} carries {len(on)} twists, want 1: {on}"
        cfg, want = p[on[0]], approved[on[0]]
        for k in ("rate_hz", "depth", "mix", "note", "feedback"):
            if k in want:
                assert cfg[k] == want[k], f"{name} retuned {on[0]}.{k}"
        # snare/clap (the echo's built-in lanes), the hats, or the chords
        assert tuple(cfg.get("lanes", ("snare",))) in (
            ("snare",), ("hat",), ("chord",)), f"{name} -> {cfg.get('lanes')}"
