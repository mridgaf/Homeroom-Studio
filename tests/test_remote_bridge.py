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

    Each command has TWO auto-input lines -- press and release:
        {pattern="b? 14 7f", name="Patch Next", value="1"}
        {pattern="b? 14 00", name="Patch Next", value="0"}
    Both must carry the same CC. Collecting a set rather than overwriting is the
    whole point: an earlier version of this test kept only the last line, so
    editing just the press line slipped through it.
    """
    text = LUA.read_text(encoding="utf-8")
    seen = {}
    for hexcc, name in re.findall(
        r'pattern\s*=\s*"b\?\s*([0-9a-fA-F]{2})\s*\w+"\s*,\s*name\s*=\s*"([^"]+)"', text
    ):
        seen.setdefault(name.lower().replace(" ", "_"), set()).add(int(hexcc, 16))
    split = {k: v for k, v in seen.items() if len(v) != 1}
    assert not split, f"press/release lines disagree on the CC: {split}"
    return {k: v.pop() for k, v in seen.items()}


def test_lua_cc_numbers_match_the_python_side():
    """The one that breaks the bridge quietly: change one side, not the other."""
    assert _cc_map_from_lua() == CC


def _declared_items():
    """Every control-surface item the codec exposes -- buttons and knobs."""
    text = LUA.read_text(encoding="utf-8")
    return set(re.findall(r'\{name="([^"]+)",\s*input="(?:button|value)"', text))


def test_every_declared_item_has_an_input_pattern():
    """An item with no auto-input is a control Reason shows but nothing can drive."""
    items = _declared_items()
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


def test_map_only_references_items_the_codec_declares():
    """A Map line naming an item the codec doesn't expose is ignored silently.

    This is the failure mode the device Scope blocks introduce: the parameter
    name can be right and the whole block still do nothing because the
    left-hand side ("Knob 5") was never declared in the .lua.
    """
    used = {l.split("\t")[1] for l in MAP.read_text(encoding="utf-8").splitlines()
            if l.startswith("Map\t")}
    assert used <= _declared_items(), f"mapped but not declared: {used - _declared_items()}"
