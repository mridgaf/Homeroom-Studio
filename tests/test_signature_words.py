"""Every signature's chord_source/progression/mode words must be ones the
engine actually understands.

This exists because of a real bug (2026-07-24): Rage Engine was written
with chord_source "string", but the valid word is "strings" (the London
library) — "string" is an instrument_sampler GROUP name, not a
chord_source word. Nothing raised. The voice just silently fell through
to the next source, and the only way to notice was reading a stem list
and wondering where the strings went.

A typo in a config is the easiest mistake to make on this project and the
hardest to hear, so it gets a test across ALL THREE rosters rather than a
comment.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "tools"))

import pytest                                               # noqa: E402

import instrument_sampler                                   # noqa: E402
import key_context                                          # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# the words beat_machine._build_chords actually branches on:
#   - every instrument_sampler.VOICES key (sampled from his own banks)
#   - "loop"    a melodic loop from his library
#   - "strings" the London Symphonic library, via string_sampler
#   - "chip"    the synthesized chip voice (New Math / Chiptune only)
VALID_SOURCES = set(instrument_sampler.VOICES) | {"loop", "strings", "chip"}
VALID_RHYTHMS = {"arp", "sustain"}
# Every mode KeyContext can actually build a scale from. A modal key is
# fine now: melodic_loops.in_key matches samples by mode FAMILY (fixed
# 2026-07-24), so "dorian" no longer starves the loop voice the way it
# silently did for DJ Premium.
VALID_MODES = set(key_context.MODES)

CONFIGS = ("crew_config.json", "legends_config.json", "genres_config.json")


def _signatures():
    """(config, identity, signature) for every identity that has one."""
    out = []
    for cfg in CONFIGS:
        path = ROOT / cfg
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        for name, preset in doc.items():
            if name.startswith("_") or not isinstance(preset, dict):
                continue
            sig = preset.get("signature")
            if isinstance(sig, dict):
                out.append((cfg, name, sig))
    return out


def _weighted(spec):
    """A weighted [[word, n], ...] list -> the words. A bare string is a
    valid unweighted form too."""
    if isinstance(spec, str):
        return [spec]
    if not isinstance(spec, list):
        return []
    return [s[0] if isinstance(s, list) else s for s in spec]


def test_there_are_signatures_to_check():
    assert len(_signatures()) >= 9, "expected at least the nine crew"


@pytest.mark.parametrize("cfg,name,sig", _signatures())
def test_chord_source_words_are_understood(cfg, name, sig):
    for word in _weighted(sig.get("chord_source")):
        assert word in VALID_SOURCES, (
            "%s/%s: chord_source %r is not a word the engine branches on "
            "(it would silently fall through). Valid: %s"
            % (cfg, name, word, sorted(VALID_SOURCES)))


@pytest.mark.parametrize("cfg,name,sig", _signatures())
def test_progressions_exist_in_the_library(cfg, name, sig):
    known = set(json.loads((ROOT / "progressions_config.json").read_text()))
    for word in _weighted(sig.get("progressions")):
        assert word in known, (
            "%s/%s: progression %r is not in progressions_config.json"
            % (cfg, name, word))


@pytest.mark.parametrize("cfg,name,sig", _signatures())
def test_rhythm_and_mode_words_are_understood(cfg, name, sig):
    for word in _weighted(sig.get("chord_rhythm")):
        assert word in VALID_RHYTHMS, "%s/%s: chord_rhythm %r" % (
            cfg, name, word)
    for word in _weighted((sig.get("key") or {}).get("mode")):
        assert word in VALID_MODES, (
            "%s/%s: mode %r is not in key_context.MODES. Modal keys ARE "
            "supported (dorian/phrygian/harmonic_minor/phrygian_dominant/"
            "mixolydian/lydian) — but remember mode does not change chord "
            "QUALITIES; it sets the label and which samples count as "
            "in-key. Put the modal colour in a progression as well."
            % (cfg, name, word))


@pytest.mark.parametrize("cfg,name,sig", _signatures())
def test_weights_are_positive_numbers(cfg, name, sig):
    for field in ("chord_source", "progressions", "chord_rhythm"):
        spec = sig.get(field)
        if not isinstance(spec, list):
            continue
        for entry in spec:
            if isinstance(entry, list):
                assert len(entry) == 2, "%s/%s: %s %r" % (cfg, name, field, entry)
                assert isinstance(entry[1], (int, float)) and entry[1] > 0, (
                    "%s/%s: %s weight for %r must be > 0 (a zero weight is a "
                    "dead option, delete it instead)" % (cfg, name, field, entry[0]))
