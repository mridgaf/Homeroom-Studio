"""Owner 2026-10-10: sound-effects lanes sit 3.2 dB (20% quieter) lower."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import crew


def test_fx_trim_is_3_2_db_on_every_fx_lane():
    assert crew.FX_LANE_TRIM_DB == -3.2
    assert set(crew.FX_LANES) == {"fx", "fxloop", "fxloop2", "airs"}


def test_trim_runs_before_the_lock_reads_lane_gains():
    src = Path(crew.__file__).read_text()
    assert src.index("_fx_g = 10 **") < src.index("_lane_gains = {}")
