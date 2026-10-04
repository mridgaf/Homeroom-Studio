"""Owner 2026-10-03: DJs collab with genres; in loops mode a DJ collabs
with genres only, never another DJ. No audio is rendered here."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import beat_machine as bm  # noqa: E402
from crew import CREW, GENRE_NAMES  # noqa: E402


@pytest.mark.parametrize("names", [
    ["DJ Light Green", "Baltimore Club"],   # host has no stamp lane
    ["Crunk", "Razor"],                     # guest has no stamp lane
    ["Otto Grit", "Crunk", "Chiptune"],
])
def test_dj_genre_collab_builds(names):
    p, _ = bm.collab_preset(names, 1234, None, dirs=bm.parse_directions(""))
    assert set(p["lane_parent"].values()) <= set(names)


def test_loops_only_refuses_dj_with_dj():
    with pytest.raises(ValueError, match="not with another DJ"):
        bm.generate(["Otto Grit", "Cutz"], loops_only=True, root=None)


def test_page_loops_beats_gaplessly():
    page = Path(bm.__file__).read_text()
    assert "n.loop = true" in page and "<audio loop preload" not in page
