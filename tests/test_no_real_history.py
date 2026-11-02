"""Tests must never write his real beat memory in ~/.reason_voice
(conftest._histories_never_touch_his_real_ones). If this fails, the
redirect was removed and test beats are steering his real ones again."""
import os

import beat_recipes
import pattern_gen


def test_histories_point_away_from_his_home_folder():
    real = os.path.expanduser("~/.reason_voice")
    for path in (pattern_gen.PAT_HIST, beat_recipes.HIST):
        assert not str(path).startswith(real), path
