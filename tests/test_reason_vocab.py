"""Guard for tools/reason_vocab.py.

The vocabulary only has value if the names in it are exactly Reason's names --
a near-miss fails silently in Reason, so a parser that quietly lets junk through
is worse than no parser. These pin it against Reason's own factory data.
"""
import pytest

from tools.reason_vocab import MAPS, build, display_name, is_parameter

pytestmark = pytest.mark.skipif(not MAPS.exists(),
                                reason="Reason 12 not installed on this machine")


@pytest.fixture(scope="module")
def vocab():
    return build()


def test_mclass_compressor_matches_the_manual(vocab):
    """Every parameter the Operation Manual lists for this device, and no junk."""
    items = set(vocab["devices"]["MClass Compressor"]["items"])
    assert {"Threshold", "Ratio", "Attack", "Release", "Soft Knee",
            "Input Gain", "Output Gain", "Adapt", "Sidechain Solo"} <= items
    assert not any(i.startswith('"') or "=" in i for i in items)


def test_reason_12_only_devices_are_present(vocab):
    """The 2013 PDF knows none of these; the factory maps do."""
    names = {d["name"] for d in vocab["devices"].values()}
    assert {"Mimic", "Europa", "Quartet", "Objekt"} <= names


def test_rack_extension_ids_become_readable_names():
    assert display_name("se.propellerheads.Mimic") == "Mimic"
    assert display_name("MClass Compressor") == "MClass Compressor"


@pytest.mark.parametrize("junk", ['"Thresh"', "Group=3", "Shift=ShiftDown",
                                  "Display=DeviceName", "0", "-1", ""])
def test_constants_and_group_assignments_are_not_parameters(junk):
    assert not is_parameter(junk)


@pytest.mark.parametrize("real", ["Threshold", "Amp Attack 1", "Filter Freq 1",
                                  "Select Next Patch", "Loop On/Off"])
def test_real_parameter_names_survive(real):
    assert is_parameter(real)
