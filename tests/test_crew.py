"""Checkpoint 3: numeric verification of the nine personality presets."""
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
