"""Remote bridge guard — the three things that fail SILENTLY in Reason.

Why this file exists: until 2026-09-10 the copies in remote/ were an old draft
that had never installed successfully, while the working files lived only in
~/Library. Nothing noticed, because every failure mode here is silent — Reason
does not report a bad codec, it just ignores the surface.

See .claude/skills/reason-remote-bridge/SKILL.md.
"""
import re
from pathlib import Path

import pytest

from reason_voice.reason_control import CC

REMOTE = Path(__file__).parent.parent / "remote"
LUA = REMOTE / "ReasonVoice.lua"
CODEC = REMOTE / "ReasonVoice.luacodec"
MAP = REMOTE / "ReasonVoice.remotemap"


def _cc_map_from_lua():
    """{'patch_next': 20, ...} as the .lua codec actually declares it.

    Lines look like: {pattern="b? 14 7f", name="Patch Next", value="1"}
    """
    text = LUA.read_text(encoding="utf-8")
    found = {}
    for hexcc, name in re.findall(
        r'pattern\s*=\s*"b\?\s*([0-9a-fA-F]{2})\s*\w+"\s*,\s*name\s*=\s*"([^"]+)"', text
    ):
        found[name.lower().replace(" ", "_")] = int(hexcc, 16)
    return found


def test_lua_cc_numbers_match_the_python_side():
    """The one that breaks the bridge quietly: change one side, not the other."""
    assert _cc_map_from_lua() == CC


def test_every_declared_item_has_an_input_pattern():
    """An item with no auto-input is a control Reason shows but nothing can drive."""
    text = LUA.read_text(encoding="utf-8")
    items = set(re.findall(r'\{name="([^"]+)",\s*input="button"\}', text))
    assert items, "no items declared — codec would expose nothing"
    assert items == {n.replace("_", " ").title() for n in _cc_map_from_lua()}


@pytest.mark.parametrize("key", [
    "remote_supported_control_surfaces",  # absent => Reason ignores the codec
    "out_ports",                          # absent => same, with no error
    'source="ReasonVoice.lua"',           # points at the logic file
])
def test_luacodec_keeps_its_mandatory_keys(key):
    assert key in CODEC.read_text(encoding="utf-8")


def test_remotemap_header_is_tab_separated_v1():
    """Tabs are load-bearing; copy-paste turns them into spaces and it dies quietly."""
    lines = MAP.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "Propellerhead Remote Mapping File"
    version = next(l for l in lines if l.startswith("File Format Version"))
    assert version == "File Format Version\t1.0.0"
    assert all("\t" in l for l in lines if l.startswith(("Map", "Scope")))


def test_map_covers_every_command_the_app_can_send():
    text = MAP.read_text(encoding="utf-8")
    mapped = {l.split("\t")[1] for l in text.splitlines() if l.startswith("Map\t")}
    assert {n.replace("_", " ").title() for n in CC} <= mapped
