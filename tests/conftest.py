"""Shared fixtures.

`governed`: force the kick-relative level rules ON for the handful of tests
that assert them. crew.TRUE_LEVELS defaults ON since 2026-09-20 (the owner
heard the A/B and picked the "true levels" mix as the default), so the
governor now only runs in the escape-hatch mode REASON_VOICE_TRUE_LEVELS=0.
A test of the governor must opt back into that mode; every other test sees
the shipped default.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
import crew


@pytest.fixture
def governed():
    prev = crew.TRUE_LEVELS
    crew.TRUE_LEVELS = False
    yield
    crew.TRUE_LEVELS = prev


@pytest.fixture(autouse=True)
def _reason_folder_never_touches_the_desktop(tmp_path_factory, monkeypatch):
    """Every loop write copies into ~/Desktop/Homeroom Loops for Reason;
    tests must never fill his real folder."""
    import beat_machine
    monkeypatch.setattr(beat_machine, "REASON_ROOT",
                        tmp_path_factory.mktemp("reason_loops"))


@pytest.fixture(autouse=True)
def _sound_engine_never_touches_his_folders(tmp_path, monkeypatch):
    """Hard rule (owner 2026-11-01): Sound Engine tests write uploads,
    renders and exports into a temp folder, never ~/.homeroom_engine or
    his Exports folder -- the sandbox refuses those, failing ~54 tests."""
    import sys
    server = sys.modules.get("sound_engine.server")
    if server is None:
        return
    for name in ("UPLOADS", "RENDERS", "EXPORT_DIR"):
        d = tmp_path / ("engine_" + name.lower())
        d.mkdir()
        monkeypatch.setattr(server, name, d)


@pytest.fixture(autouse=True)
def _histories_never_touch_his_real_ones(tmp_path, monkeypatch):
    """Generated test beats must not land in the pattern / drum-sample
    memory that steers his next real beats (and the sandbox can't write
    ~/.reason_voice anyway). A test that sets its own path still wins."""
    import beat_recipes
    import pattern_gen
    monkeypatch.setattr(pattern_gen, "PAT_HIST", tmp_path / "pat_hist.json")
    monkeypatch.setattr(beat_recipes, "HIST", tmp_path / "sample_hist.json")
