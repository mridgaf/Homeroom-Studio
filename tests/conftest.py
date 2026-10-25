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
