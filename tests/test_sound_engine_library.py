"""Tests for sound_engine/library.py's beat-listing. Uses a fixture
folder under tmp_path — NEVER the real beats_root.json / TBOTC 3 path,
which isn't always mounted and must never be a test dependency."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
pytest.importorskip("pedalboard")

from sound_engine import library  # noqa: E402
from tools.make_drum_loops import write_wav24  # noqa: E402


def _make_fixture_beat(root: Path, dj="Test DJ", no="1", title="Sample Beat",
                        bpm="90", with_stems=True, n_stems=3):
    folder = root / dj
    folder.mkdir(parents=True, exist_ok=True)
    prefix = f"{no} {dj} {title}"
    main = folder / f"{prefix} Drums {bpm}bpm.wav"
    sig = np.sin(2 * np.pi * 220 * np.arange(4410) / 44100) * 0.3
    write_wav24(main, sig, sig)
    if with_stems:
        stems_dir = folder / f"{prefix} Stems"
        stems_dir.mkdir()
        for i in range(n_stems):
            write_wav24(stems_dir / f"lane{i}.wav", sig, sig)
    return folder


def test_list_beats_finds_a_beat_with_stems(tmp_path):
    _make_fixture_beat(tmp_path)
    beats = library.list_beats(tmp_path)
    assert len(beats) == 1
    b = beats[0]
    assert b["dj"] == "Test DJ"
    assert b["bpm"] == 90.0
    assert b["stem_count"] == 3
    assert b["stems_dir"].is_dir()


def test_list_beats_skips_a_beat_with_no_stems_folder(tmp_path):
    _make_fixture_beat(tmp_path, with_stems=False)
    beats = library.list_beats(tmp_path)
    assert beats == []


def test_list_beats_skips_dotdirs(tmp_path):
    (tmp_path / ".recipes").mkdir()
    (tmp_path / ".recipes" / "1.json").write_text("{}")
    _make_fixture_beat(tmp_path)
    beats = library.list_beats(tmp_path)
    assert len(beats) == 1


def test_find_beat_round_trips_from_list_beats(tmp_path):
    _make_fixture_beat(tmp_path)
    beat_id = library.list_beats(tmp_path)[0]["beat_id"]
    found = library.find_beat(tmp_path, beat_id)
    assert found is not None
    assert found["stems_dir"].is_dir()


def test_find_beat_returns_none_for_unknown_id(tmp_path):
    assert library.find_beat(tmp_path, "nope/nope") is None


def test_resolve_beats_root_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("REASON_VOICE_BEATS_ROOT", str(tmp_path))
    assert library.resolve_beats_root() == tmp_path
