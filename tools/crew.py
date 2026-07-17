"""The crew: nine invented DJ personalities as engine presets (Checkpoint 3).

Each personality is an original character built closely on one real
producer's documented style (July 2026 research, techniques.md). A preset
carries everything a batch needs to sound like THEM:

- timing/feel numbers per lane (LaneFeel offsets, MPC swing, jitter),
- a taste in drums (want-tags per lane) rather than fixed samples: the
  owner's rule (2026-07-14) is that every character EXPERIMENTS — kick,
  snare, and the rest are re-picked per beat from that character's tags.
  Only the STAMP is locked in ~/.reason_voice/crew_kits.json: it's their
  producer tag in drums, the one percussion hit in all their beats,
- arrangement habits written into the 8-bar A/B form (bars 1-4 = A,
  bars 5-8 = B with fills/ghosts/drop-outs where that character puts them),
- mix flavor: SP-1200 dust for the 90s heads only (ASR-10/MPC3000 folks
  stay clean — research says their grit is arrangement, not crunch),
  vinyl bed, wow, sidechain depth, master drive.

Owner taste (groove.OWNER_TASTE) is the house default everywhere; where a
personality's era strongly argues otherwise the prototype renders BOTH
ways (main = house, "Alt" file = era) so the deviation faces his ears
before Checkpoint 4 ships the twenty.

Run:  ./.venv/bin/python tools/crew.py          (prototype per personality)
Out:  ~/Documents/Samples/Claude Drum Beats/Proto N <Name> Drums NNNbpm.wav
"""
import json
import os
import sys
import zlib
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from pattern_gen import DEFAULT_STYLE, STYLE_VERSION
from make_drum_loops import SR, master, write_wav24
from make_drum_beats import build_shots, duck
from make_hiphop_tracks import load_audio, norm_rms
from groove import (LaneFeel, OWNER_TASTE, dist808, fft_convolve,
                    gated_reverb, make_ir, master_to_lufs, mono_below,
                    mpc_swing_offset, roughness_am, sat_unity, snare_scale,
                    sp1200, velocity, vinyl_bed, wow_flutter)

OUT = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))
LOCK = Path(os.path.expanduser("~/.reason_voice/crew_kits.json"))
BARS = 8
SNARE_LIKE = {"snare", "clap"}   # lanes that follow the owner's snare trim

R16 = "-" * 16

# --------------------------------------------------------------- the roster
# kit entry: lane -> (library role, must-word, want-tags, choke seconds)
# lane entry: lane -> (pan, gain, (offset_ms, jitter_ms, swing, seed), bars)
# space: (house treatment, [lanes it applies to]); alt: era-argued
#   deviation rendered as a second "Alt" file, or None when era and house
#   agree. Room/plate params are (decay_s, tone_hz, wet).

DEFAULT_CREW = {
    "Otto Grit": dict(
        num=1, bpm=88, era="90s", built="J Dilla",
        listen=("the drunk pull: snare rushes early, kick leans back late, "
                "hats dead straight; half SP-1200 dust; vinyl bed; his stamp "
                "is a dusty tom on the tail of bars 4 and 8"),
        kit=dict(
            kick=("kick", None,["dust", "vinyl", "boom", "dirty"],
                  (0.55, 0.95)),
            snare=("snare", None, ["vinyl", "dusty", "lofi"], 1.0),
            hat=("hat", None, ["closed", "vintage"], 0.5),
            stamp=("perc", None, ["tom"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (+10, 4, 50, 101), [
                "X------x--X-----", "X------x--X---x-",
                "X------x--X-----", "X-----xx--X---x-",
                "X------x--X---x-", "X---x--x--X-----",
                "X------x--X---x-", "X-x---xx--X-----"]),
            snare=(0.0, 0.88, (-18, 4, 50, 102), [
                "----X-------X---", "----X-------X---",
                "----X-------X---", "----X-------X--.",
                "----X--.----X---", "----X-------X--.",
                "----X--.----X---", "----X-----.-X---"]),
            hat=(-0.12, 0.36, (0, 2, 50, 103),
                 ["x-x-x-x-x-x-x-x-"] * 7 + ["x-x-x-x-x-x-----"]),
            stamp=(-0.35, 0.4, (0, 3, 50, 104),
                   [R16] * 3 + ["--------------x-"]
                   + [R16] * 3 + ["--------------x-"]),
        ),
        dust=0.5, vinyl=-42, wow=0.0, sidechain=0.15,
        space=("gated", ["snare"]), alt=("room", (0.45, 3500, 0.32)),
        drive=1.35, kick_dist=0.0, mix_sat=0.0,
    ),

    "Cutz": dict(
        num=2, bpm=93, era="90s", built="DJ Premier",
        listen=("surgical: everything tight at 53% swing (his effective "
                "51-54 zone), ghost snares, and his stamp — a scratch stab "
                "fill closing bars 4 and 8"),
        kit=dict(
            kick=("kick", None,["punch", "hard", "knock"], (0.55, 0.95)),
            snare=("snare", None, ["crack", "tight", "hard"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.5),
            stamp=("fx", None, ["scratch"], 0.8),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1.5, 53, 111), [
                "X--x------X--X--", "X--x------X--X--",
                "X--x------X--X--", "X--x------X--X-x",
                "X--x------X--X--", "X--x----x-X--X--",
                "X--x------X--X--", "X--x------X-xX-x"]),
            snare=(0.0, 0.88, (0, 1.5, 53, 112), [
                "----X-------X---", "----X-------X---",
                "----X--.----X---", "----X-------X--.",
                "----X-------X---", "----X--.----X---",
                "----X-------X---", "----X--.--.-X--."]),
            hat=(0.14, 0.38, (0, 1.5, 53, 113), ["x-x-x-x-x-x-x-x-"] * 8),
            stamp=(-0.3, 0.42, (0, 2, 50, 114),
                   [R16] * 3 + ["------------x-x-"]
                   + [R16] * 3 + ["----------x-x-x-"]),
        ),
        dust=0.5, vinyl=-46, wow=0.0, sidechain=0.15,
        space=("gated", ["snare"]), alt=("room", (0.4, 3800, 0.25)),
        drive=1.4, kick_dist=0.0, mix_sat=0.0,
    ),

    "Crate Prophet": dict(
        num=3, bpm=92, era="90s", built="Pete Rock / Madlib",
        listen=("warm and loose: 60% golden-era swing, snare sits LATE "
                "(era-driven, flagged — house verdict is early, but laid-"
                "back is this character), loose congas, the heaviest vinyl "
                "bed plus record wow; stamp is a conga slap on bars 4/8. "
                "This is also the prototype that SKIPS sidechain (the "
                "1-in-10 no-duck rule)"),
        kit=dict(
            kick=("kick", None,["warm", "deep", "boom"], (0.6, 1.0)),
            # owner 2026-07-15: his snare was still too loud — the "room"/
            # "reverb" wants pulled pre-reverbed hits; now dry-ish picks and
            # the space treatment carries the wetness
            snare=("snare", None, ["dusty", "vintage", "warm"], 1.0),
            hat=("hat", None, ["closed"], 0.5),
            bongo=("bongo", None, ["conga", "bongo"], 0.8),
            stamp=("bongo", None, ["conga", "slap"], 0.8),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 5, 60, 121), [
                "X-----x---X--x--", "X-----x---X-----",
                "X-----x---X--x--", "X-----x---X-x---",
                "X-----x---X--x--", "X---x-x---X-----",
                "X-----x---X--x--", "X-----x-x-X-x---"]),
            snare=(0.0, 0.62, (+8, 5, 60, 122), [   # extra ~3 dB down, owner
                "----X-------X---", "----X-------X---",
                "----X-------X---", "----X-------X--.",
                "----X-------X---", "----X--.----X---",
                "----X-------X---", "----X-------X-.."]),
            hat=(-0.15, 0.36, (0, 4, 60, 123),
                 ["x-xox-x-x-xox-x-"] * 7 + ["x-xox-x-x-xox-xx"]),
            bongo=(0.32, 0.3, (0, 6, 60, 124), [
                "--x---x-------x-", "------x---x-----",
                "--x---x-------x-", "------x---x---x-",
                "--x---x-------x-", "------x---x-----",
                "--x---x-------x-", "--x---x---x-x-x-"]),
            stamp=(-0.3, 0.38, (0, 5, 60, 125),
                   [R16] * 3 + ["--------------x-"]
                   + [R16] * 3 + ["--------------x-"]),
        ),
        dust=0.5, vinyl=-40, wow=0.3, sidechain=0.0,
        space=("gated", ["snare"]), alt=("room", (0.6, 3000, 0.35)),
        drive=1.3, kick_dist=0.0, mix_sat=0.0,
    ),

    "Chrome Dial": dict(
        num=4, bpm=100, era="2000s", built="Timbaland",
        listen=("syncopated bounce with silence as an instrument — bar 6 "
                "drops to almost nothing and answers bar 5; exotic perc "
                "off-center; completely CLEAN (his ASR-10 was 16-bit — the "
                "grit is arrangement, so no crush here by research, not "
                "taste); stamp is an exotic perc hit late in bars 4/8"),
        kit=dict(
            kick=("kick", None,["clean", "punch", "tight"], (0.7, 1.2)),
            clap=("clap", None, ["clap"], 1.0),
            perc=("perc", None, ["tabla", "shaker", "conga"], 0.9),
            snap=("snap", None, ["snap", "finger"], 0.5),
            stamp=("perc", None, ["block", "tabla", "cowbell"], 0.6),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 131), [
                "X--X--X---X-----", "X--X--X---------",
                "X--X--X---X-----", "X--X--X---X--X--",
                "X--X--X---X-----", "----------X--X--",
                "X--X--X---X-----", "X--X--X---------"]),
            clap=(0.0, 0.85, (0, 1, 50, 132),
                  ["----X-------X---"] * 5 + ["----X-----------"]
                  + ["----X-------X---"] * 2),
            perc=(-0.35, 0.32, (0, 2, 50, 133), [
                "--x---x----x--x-", "--x---x----x----",
                "--x---x----x--x-", "--x---x--x-x--x-",
                "--x---x----x--x-", "--------x--x----",
                "--x---x----x--x-", "--x-x-x----x--x-"]),
            snap=(0.18, 0.4, (0, 1, 50, 134),
                  [R16, "--------------X-"] * 4),
            stamp=(0.28, 0.4, (0, 1, 50, 135),
                   [R16] * 3 + ["-------------x--"]
                   + [R16] * 3 + ["-------------x--"]),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.2,
        space=("gated", ["clap"]), alt=None,
        drive=1.45, kick_dist=0.0, mix_sat=0.0,
    ),

    "Glass Cat": dict(
        num=5, bpm=98, era="2000s", built="The Neptunes / Pharrell",
        listen=("minimal and dry: NO hats — a snap keeps time; the clap "
                "lands ~18 ms LATE against the snare (the documented "
                "Neptunes flam); bar 8 stop-starts. The Alt file is the one "
                "to compare hard: era says bone dry, house says gated. "
                "Stamp is a weird click/zap on bars 4/8"),
        kit=dict(
            kick=("kick", None,["clean", "tight", "pop"], (0.7, 1.2)),
            snare=("snare", None, ["clean", "rim", "snap"], 1.0),
            clap=("clap", None, ["clap"], 1.0),
            snap=("snap", None, ["snap", "finger"], 0.5),
            stamp=("fx", None, ["click", "zap", "glitch", "laser"], 0.6),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 141), [
                "X-------X-X-----", "X-------X-X-----",
                "X-------X-X-----", "X-------X-X---X-",
                "X-------X-X-----", "X-------X-X-----",
                "X-------X-X---X-", "X---X-----------"]),
            snare=(0.0, 0.85, (0, 1, 50, 142),
                   ["----X-------X---"] * 7 + ["----X-----------"]),
            clap=(0.1, 0.5, (+18, 1, 50, 143),
                  ["----X-------X---"] * 7 + ["----X-----------"]),
            snap=(0.12, 0.42, (0, 1, 50, 144),
                  ["x--x--x--x--x--x"] * 7 + ["x--x------------"]),
            stamp=(-0.3, 0.38, (0, 1, 50, 145),
                   [R16] * 3 + ["--------------x-"]
                   + [R16] * 3 + ["--------------x-"]),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.2,
        space=("gated", ["snare"]), alt=("dry", None),
        drive=1.4, kick_dist=0.0, mix_sat=0.0,
    ),

    "Sunday Chop": dict(
        num=6, bpm=96, era="2000s", built="Kanye West",
        listen=("gospel bounce at 57% swing, driving pushed kicks, a BIG "
                "clap with a snare tucked underneath, tambourine offbeats; "
                "clean (MPC3000 = 16-bit). His stamp is the crash swell "
                "opening bars 1 and 5"),
        kit=dict(
            kick=("kick", None,["punch", "knock", "clean"], (0.7, 1.2)),
            clap=("clap", None, ["big", "clap"], 1.0),
            snare=("snare", None, ["snare"], 1.0),
            hat=("hat", None, ["closed"], 0.5),
            perc=("perc", None, ["tamb", "shaker"], 1.0),
            stamp=("crash", None, ["crash"], 2.5),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 57, 151), [
                "X---x---X---x---", "X---x--xX---x---",
                "X---x---X---x---", "X---x--xX---x-x-",
                "X---x---X---x---", "X---x--xX---x---",
                "X---x---X---x---", "X--xx---X---x-x-"]),
            clap=(0.0, 0.9, (0, 2, 57, 152), ["----X-------X---"] * 8),
            snare=(0.0, 0.5, (0, 2, 57, 153), ["----X-------X---"] * 8),
            hat=(0.1, 0.4, (0, 2, 57, 154),
                 ["x-x-x-x-x-x-x-x-"] * 7 + ["x-x-x-x-x-x-x-xx"]),
            perc=(-0.25, 0.3, (0, 3, 57, 155), ["--x---x---x---x-"] * 8),
            stamp=(0.0, 0.4, (0, 2, 57, 156),
                   ["X---------------"] + [R16] * 3
                   + ["X---------------"] + [R16] * 3),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.2,
        space=("gated", ["clap"]), alt=None,
        drive=1.4, kick_dist=0.0, mix_sat=0.0,
    ),

    "Night Metro": dict(
        num=7, bpm=140, era="2010s", built="Metro Boomin",
        listen=("dark halftime: sustained distorted 808, clap on 3, hat "
                "rolls that ramp INTO the snare, and the drama — bar 5 "
                "drops to the 808 alone. Stamp is a reversed cymbal "
                "resolving onto the next downbeat (bars 4 and 8)"),
        kit=dict(
            kick=("kick", None,["deep", "sub", "long"], (0.9, 2.2)),
            clap=("clap", None, ["clap", "reverb"], 1.0),
            hat=("hat", None, ["trap", "closed"], 0.5),
            stamp=("fx", None, ["reverse", "sweep", "riser"], 1.6),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 0, 50, 161), [
                "X-----X---X-----", "X-----X---X-----",
                "X-----X-----X---", "X-----X---X---X-",
                "X---------------", "X-----X---X-----",
                "X-----X-----X---", "X-----X---X-X---"]),
            clap=(0.0, 0.85, (0, 0, 50, 162),
                  ["--------X-------"] * 4 + [R16]
                  + ["--------X-------"] * 3),
            hat=(-0.1, 0.4, (0, 0, 50, 163), [
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-x-x-x-x-xxxxxxxx",
                "x-x-x-x-xxxxx-x-x-x-x-x-xxxxxxxx",
                "-" * 32,
                "x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-",
                "x-x-x-x-x-x-x-x-xxxxxxxxx-x-x-x-",
                "x-x-x-x-x-x-x-x-xxxxxxxxxxxxxxxx"]),
            stamp=(-0.3, 0.45, (0, 0, 50, 164),
                   [R16] * 3 + ["------------x---"]
                   + [R16] * 3 + ["------------x---"]),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.35,
        space=("gated", ["clap"]), alt=None,
        drive=1.5, kick_dist=5.0, mix_sat=0.0,
    ),

    "Rage Engine": dict(
        num=8, bpm=150, era="2010s", built="Lex Luger",
        listen=("relentless: wall-to-wall 32nd hat rolls, snare+clap "
                "stacked, distortion on the 808 AND glue saturation on the "
                "whole mix, zero drop-outs, extra snare fills every 4th "
                "bar. Stamp is the crash/impact opening bars 1 and 5"),
        kit=dict(
            kick=("kick", None,["hard", "punch", "distort"], (0.8, 2.2)),
            snare=("snare", None, ["trap", "snare"], 1.0),
            clap=("clap", None, ["clap"], 1.0),
            hat=("hat", None, ["trap", "closed"], 0.5),
            stamp=("crash", None, ["crash", "impact"], 2.5),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 0, 50, 171), [
                "X-----X-----X---", "X-----X-----X--X",
                "X-----X-----X---", "X--X--X-----X---",
                "X-----X-----X---", "X-----X-----X--X",
                "X--X--X-----X---", "X-----X--X--X--X"]),
            snare=(0.0, 0.82, (0, 0, 50, 172),
                   ["--------X-------"] * 3 + ["--------X-----xx"]
                   + ["--------X-------"] * 3 + ["--------X---xx-x"]),
            clap=(0.1, 0.5, (0, 0, 50, 173), ["--------x-------"] * 8),
            hat=(0.12, 0.4, (0, 0, 50, 174), [
                "x-x-x-x-xxxxxxxxx-x-x-x-xxxxxxxx",
                "x-x-x-x-x-x-x-x-xxxxxxxxxxxxxxxx",
                "x-x-x-x-xxxxxxxxx-x-x-x-xxxxxxxx",
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "x-x-x-x-xxxxxxxxx-x-x-x-xxxxxxxx",
                "x-x-x-x-x-x-x-x-xxxxxxxxxxxxxxxx",
                "xxxxxxxxxxxxxxxxx-x-x-x-xxxxxxxx",
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]),
            stamp=(0.0, 0.45, (0, 0, 50, 175),
                   ["X---------------"] + [R16] * 3
                   + ["X---------------"] + [R16] * 3),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.35,
        space=("gated", ["snare"]), alt=None,
        drive=1.55, kick_dist=6.0, mix_sat=4.0,
    ),

    # Snap Church retired 2026-07-15 (owner: too close to Night Metro and
    # Rage Engine). Slot 9 belongs to New Math — the only crew member built
    # on NO ancestor: Jersey-club kick grammar plus the genuinely-untried
    # findings from the July 2026 research (quintuplet hat grid, Euclidean
    # percussion, one lane deliberately swinging against a straight kit).
    "New Math": dict(
        num=9, bpm=144, era="now", built="no one — the front edge",
        listen=("the new one. A club kick pattern that never sits where "
                "trap taught you to expect it; a hat lane counting FIVE "
                "against everyone else's four (quintuplet grid); "
                "percussion running world-rhythm math (E(7,16) and "
                "E(5,16) necklaces); and one lane swinging 58% while the "
                "rest of the kit stays dead straight — the clash IS the "
                "groove. Clean and punchy, mid-forward kick. Stamp is a "
                "found-sound fx hit on the tail of bars 4/8"),
        kit=dict(
            kick=("kick", None,["punch", "knock", "club", "tight"],
                  (0.5, 1.6)),
            snare=("snare", None, ["crack", "clean", "trap"], 1.0),
            snap=("snap", None, ["snap", "finger"], 0.5),
            hat=("hat", None, ["closed", "tight", "crisp"], 0.5),
            perc=("perc", None, ["glitch", "click", "wood", "block"], 0.8),
            stamp=("fx", None, ["squeak", "vocal", "yeah", "hey",
                                "reverse", "glitch"], 1.2),
        ),
        lanes=dict(
            # the Jersey-club five: 1 . . & . 3 . 4 — then it mutates
            kick=(0.0, 1.0, (0, 1, 50, 191), [
                "X--X--X-X-X-----", "X--X--X-X-X-----",
                "X--X--X-X-X---X-", "X--X--X-X-X-X---",
                "X--X--X-X-X-----", "X--X---X--X-X---",
                "X--X--X-X-X---X-", "X--X--XX--X-----"]),
            snare=(0.0, 0.85, (0, 1, 50, 192),
                   ["----X-------X---"] * 7 + ["----X-----X-X---"]),
            snap=(0.15, 0.4, (+12, 1, 50, 193), [
                "-x-x---x-x---x--", "-x-x---x-x------",
                "-x-x---x-x---x--", "-x-x---x-xx--x--",
                "-x-x---x-x---x--", "-x-x---x-x------",
                "-x-x---x-x---x--", "-x-x-x-x-x---x-x"]),
            # 20-step bars: sixteenth-quintuplets running against the four
            hat=(-0.16, 0.38, (0, 1, 50, 194), [
                "x-x-xx-x-xx-x-xx-x-x", "x-x-xx-x-xx-x-xx-x-x",
                "x-x-xx-x-xx-x-xx-x-x", "x-x-xx-x-xxxx-xx-xxx",
                "x-x-xx-x-xx-x-xx-x-x", "x-x-xx-x-xx-x-xx-x-x",
                "x-x-x-x-x-x-x-x-x-x-", "xx-xx-xx-xx-xx-xxxxx"]),
            # Euclidean necklaces, swung 58% against a straight kit
            perc=(0.18, 0.3, (0, 2, 58, 195), [
                "x--x-x-x--x-x-x-", "x---x--x--x--x--",
                "x--x-x-x--x-x-x-", "x---x--x--x--x--",
                "x--x-x-x--x-x-x-", "x---x--x--x--x--",
                "x--x-x-x--x-x-x-", "x--x-x-xx-x-x-x-"]),
            stamp=(-0.28, 0.4, (0, 1, 50, 196),
                   [R16] * 3 + ["--------------x-"]
                   + [R16] * 3 + ["--------------x-"]),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.3,
        space=("gated", ["snare"]), alt=None,
        drive=1.5, kick_dist=3.0, mix_sat=0.0,
    ),
}

# ------------------------------------------------------------ config file
# Owner spec 2026-07-16 (dj-drone-machine-spec.md): the roster lives in an
# EDITABLE config file, stable between sessions. crew_config.json at the
# project root is written from DEFAULT_CREW on first run and loaded ever
# after — tweak a number there and the next beat uses it; delete the file
# to regenerate the built-ins. A broken edit falls back loudly.

CONFIG = Path(__file__).resolve().parent.parent / "crew_config.json"


def normalize_preset(p):
    """JSON round-trips tuples into lists; give a preset its shapes back.
    Shared by the config loader and saved beat recipes (beat_recipes)."""
    q = dict(p)
    if "kit" in q:
        q["kit"] = {ln: (r, m, list(w),
                         tuple(s) if isinstance(s, list) else s)
                    for ln, (r, m, w, s) in q["kit"].items()}
    if "lanes" in q:
        q["lanes"] = {ln: (pan, gain, tuple(feel), list(bars))
                      for ln, (pan, gain, feel, bars) in q["lanes"].items()}
    if q.get("space"):
        q["space"] = (q["space"][0], list(q["space"][1]))
    if q.get("alt"):
        kind, params = q["alt"]
        q["alt"] = (kind, tuple(params) if params else None)
    return q


def load_crew(path=CONFIG):
    if not path.exists():
        doc = {"_readme": [
            "This file IS the crew: edit a number and the Beat Machine "
            "uses it on the next render. Delete the file to regenerate "
            "the built-in roster.",
            "kit entry: lane -> [library role, must-word, want-tags, "
            "choke seconds (or [lo, hi] range rolled per beat)]",
            "lane entry: lane -> [pan, gain, [offset_ms, jitter_ms, "
            "swing, seed], bars]"]}
        doc.update(DEFAULT_CREW)
        path.write_text(json.dumps(doc, indent=1))
    try:
        raw = json.loads(path.read_text())
        # 2026-07-17 upgrade: pattern grammar, kick flavors, and guest-lane
        # palettes joined the personality. When the engine's style
        # defaults advance (STYLE_VERSION bump), those three keys are
        # re-synced in place — hand edits to everything else survive. Set
        # "_style_lock": true in the file to keep hand-tuned style keys.
        changed = False
        if raw.get("_style_version", 0) < STYLE_VERSION \
                and not raw.get("_style_lock"):
            for n, p in raw.items():
                if not n.startswith("_") and n in DEFAULT_STYLE:
                    for k in ("grammar", "kick_flavors", "extras",
                              "library"):
                        p[k] = DEFAULT_STYLE[n][k]
            raw["_style_version"] = STYLE_VERSION
            changed = True
        for n, p in raw.items():
            for k in ("grammar", "kick_flavors", "extras", "library"):
                if not n.startswith("_") and n in DEFAULT_STYLE \
                        and k not in p:
                    p[k] = DEFAULT_STYLE[n][k]
                    changed = True
        if changed:
            path.write_text(json.dumps(raw, indent=1))
        crew = {n: normalize_preset(p) for n, p in raw.items()
                if not n.startswith("_")}
        if crew:
            return crew
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"WARNING: {path.name} is broken ({e}) — using the "
              "built-in roster. Fix or delete the file to silence this.")
    return {n: normalize_preset(json.loads(json.dumps(p)))
            for n, p in DEFAULT_CREW.items()}


CREW = load_crew()

# ------------------------------------------------------------- kit locking

def _load_choked(path, secs):
    """Load a locked sample, apply the era choke + level, return mono."""
    x = load_audio(path)
    if x is None or len(x) / SR < 0.01:
        return None
    cap = int(secs * SR)
    if len(x) > cap:
        x = x[:cap].copy()
        fade = min(int(0.03 * SR), len(x))
        x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    x = norm_rms(x, -14.0)
    return x.mean(axis=1) if x.ndim == 2 else x


def _pick_path(shots, role, wants, secs, seed, must=None, avoid=()):
    """Like make_drum_beats.pick but returns the PATH so it can be locked.
    Tiers: must-word AND want-tag > must-word > want-tag > anything —
    the combined tier keeps a must="808" from grabbing an 808 *cowbell*
    when the wants say deep/sub. `avoid` holds paths already locked by
    other personalities: signature kits are identities, so no two crew
    members share a sample (waived only if the pool runs dry)."""
    cands = shots.get(role, [])
    r = np.random.default_rng(seed)
    order = [cands[int(i)] for i in r.permutation(len(cands))]

    def has_must(e):
        return must in e["path"].lower()

    def has_want(e):
        return any(w in e["name"].lower() for w in wants)

    tiers = []
    if must and wants:
        tiers.append(lambda e: has_must(e) and has_want(e))
    if must:
        tiers.append(has_must)
    if wants:
        tiers.append(has_want)
    tiers.append(lambda e: True)
    for skip_used in (True, False):
        for match in tiers:
            for e in order:
                if match(e) and not (skip_used and e["path"] in avoid):
                    x = _load_choked(e["path"], secs)
                    if x is not None:
                        return e["path"], x
    return None, np.zeros(int(0.1 * SR))


def lock_stamps(shots):
    """Only the STAMP is locked per personality — it's their producer tag,
    the one hit that appears in every beat they make. Everything else is
    re-picked per beat (build_kit): the owner ruled that each character
    experiments, so nobody rides one kick or snare forever."""
    locked = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    stamps, changed = {}, False
    used = {e.get("stamp") for e in locked.values() if e.get("stamp")}
    for name, p in CREW.items():
        entry = locked.get(name, {})
        role, must, wants, secs = p["kit"]["stamp"]
        path = entry.get("stamp")
        x = _load_choked(path, secs) if path and Path(path).exists() \
            else None
        if x is None:
            seed = p["num"] * 1000 + zlib.crc32(b"stamp") % 997
            path, x = _pick_path(shots, role, wants, secs, seed,
                                 must=must, avoid=used)
            changed = True
        used.add(path)
        stamps[name] = (path, x)
    trimmed = {n: {"stamp": s[0]} for n, s in stamps.items()}
    if changed or trimmed != locked:
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        LOCK.write_text(json.dumps(trimmed, indent=1))
    return stamps


def _resolve_secs(secs, num, variant):
    """A (lo, hi) choke range becomes one length per beat — the owner's
    rule that not every beat gets the long drawn-out 808. Seeded by
    personality + variant so any beat re-renders identically."""
    if isinstance(secs, (tuple, list)):
        lo, hi = secs
        r = np.random.default_rng(num * 131 + variant * 17 + 7)
        return float(r.uniform(lo, hi))
    return secs


def build_kit(shots, name, stamp_audio, variant=0, avoid=None, preset=None):
    """One beat's kit for a personality: fresh kick/snare/etc picked from
    the character's taste tags, different per `variant` (seeded, so any
    beat can be re-rendered identically). Kick sustain is also re-rolled
    per beat from the character's era range. Share one `avoid` set across
    a batch so the beats don't converge on the same samples. The locked
    stamp rides along unchanged. preset overrides CREW[name] (mutated
    copies, e.g. New Math's boom-bap mode, change kit tastes too)."""
    p = preset or CREW[name]
    avoid = avoid if avoid is not None else set()
    kit, sources = {"stamp": stamp_audio}, {}
    for lane, (role, must, wants, secs) in p["kit"].items():
        if lane == "stamp":
            continue
        secs = _resolve_secs(secs, p["num"], variant)
        seed = (p["num"] * 1000 + zlib.crc32(lane.encode()) % 997
                + variant * 7919)
        path, x = _pick_path(shots, role, wants, secs, seed,
                             must=must, avoid=avoid)
        if path:
            avoid.add(path)
        kit[lane] = x
        sources[lane] = path
    return kit, sources

def boom_bap_variant(bpm=94):
    """New Math's boom-bap mode (owner rule 2026-07-15: half his beats
    incorporate boom bap). The math survives — Jersey kick grammar and the
    Euclidean perc — but dropped to boom-bap tempo with 58%-swung 16th
    hats (one quintuplet bar kept as an accent), a dusty snare, short
    kick, half SP-1200 dust and a vinyl bed. Use on ODD variants so it
    averages to half over time."""
    import copy
    p = copy.deepcopy(CREW["New Math"])
    p["bpm"] = bpm
    p["dust"] = 0.5
    p["vinyl"] = -44
    p["kit"]["snare"] = ("snare", None, ["dusty", "vinyl", "lofi"], 1.0)
    p["kit"]["kick"] = ("kick", None, ["boom", "punch", "knock"],
                        (0.55, 0.9))
    pan, gain, (o, j, _, seed), _ = p["lanes"]["hat"]
    p["lanes"]["hat"] = (pan, gain, (o, j, 58, seed), [
        "x-x-x-x-x-x-x-x-", "x-x-x-x-x-x-x-x-",
        "x-x-x-x-x-x-x-x-", "x-x-xx-x-xx-x-xx-x-x",   # the five, as accent
        "x-x-x-x-x-x-x-x-", "x-x-x-x-x-x-x-x-",
        "x-x-x-x-x-x-x-x-", "x-x-xx-x-xx-x-xx-x-x"])
    return p

# --------------------------------------------------------------- rendering

def grid_accent(res, s):
    """Metric accent for non-16 grids (school 2026-07-15: the velocity
    map only covered 16ths — port the strong/weak alternation to any
    grid). 32nds: beat-starts full, off-32nds soft. Quintuplets (20):
    accent 1, medium 3, soft the rest — a hand, not a machine."""
    if res == 32:
        if s % 8 == 0:
            return 1.0
        return 0.75 if s % 2 else 0.9
    if res == 20:
        return {0: 1.0, 2: 0.88}.get(s % 5, 0.75)
    return 1.0


def render_crew_beat(name, kit, space=None, preset=None, want_parts=False):
    """Render one personality's 8-bar A/B beat. kit maps lane -> mono
    audio. space overrides the house snare treatment ('room'/'dry'/...)
    for era-deviation Alt renders. preset overrides CREW[name] — that's
    how batch files apply per-beat evolutions and collab hybrids without
    mutating the roster. want_parts additionally returns the beat's
    parts for the Reason 12 handoff (owner spec 2026-07-16): per-lane
    stereo stems and the note events behind the MIDI file."""
    p = preset or CREW[name]
    bpm = p["bpm"]
    bar_s = 240.0 / bpm
    end = int(BARS * bar_s * SR)
    n = end + int(1.5 * SR)
    # vel_seed (2026-07-17): without it every beat shared one accent
    # sequence — same loud/soft ripple over the same skeleton read as
    # "the same beat". Presets carry it so recipes re-render identically.
    wob = np.random.default_rng(p["num"] * 7919
                                + p.get("vel_seed", 0) * 13)
    bufs, onsets, events = {}, {}, {}

    for lane, (pan, gain, feel_args, bars) in p["lanes"].items():
        off, jit, swing, seed = feel_args
        feel = LaneFeel(off, jit, swing, seed=seed)
        snarish = any(lane.startswith(s) for s in SNARE_LIKE)
        g = gain * (snare_scale() if snarish else 1.0)
        snd = kit[lane]
        buf = np.zeros(n)
        ons, evs = [], []
        for b in range(BARS):
            pat = bars[b % len(bars)]
            res = len(pat)
            for s, ch in enumerate(pat):
                if ch == "-":
                    continue
                t = b * bar_s + s * bar_s / res
                if res == 16:
                    t += mpc_swing_offset(s, bpm, feel.swing)
                t += feel.offset + feel.rng.normal(0, feel.jitter / 3)
                pos = int(max(t, 0.0) * SR)
                v = velocity(ch, s if res == 16 else s // 2, wob) * g \
                    * grid_accent(res, s)
                e = min(n, pos + len(snd))
                if 0 <= pos < n and v > 0:
                    buf[pos:e] += snd[:e - pos] * v
                    ons.append(pos)
                    evs.append((pos / SR, v))
        bufs[lane] = buf
        onsets[lane] = ons
        events[lane] = evs

    # seamless loop: fold the ring-out past bar 8 back onto the start
    for lane in bufs:
        bufs[lane][:n - end] += bufs[lane][end:]
        bufs[lane] = bufs[lane][:end]
    onsets = {k: [x for x in v if x < end] for k, v in onsets.items()}
    events = {k: [(t, v) for t, v in evs if t * SR < end]
              for k, evs in events.items()}

    if p["kick_dist"] > 0:
        bufs["kick"] = dist808(bufs["kick"], p["kick_dist"])
    if p.get("rough_808"):
        rate, depth = p["rough_808"]
        bufs["kick"] = roughness_am(bufs["kick"], rate, depth)

    space = space or p["space"][0]
    for lane in p["space"][1]:
        if space == "gated":
            # hold scales to tempo — one 8th note (school 2026-07-15;
            # forums put 80s drama at 300+ ms, which a 90 bpm 8th hits)
            bufs[lane] = gated_reverb(bufs[lane], onsets[lane],
                                      wet=OWNER_TASTE["gate_wet"],
                                      hold_ms=min(30000.0 / bpm, 350.0))
        elif space in ("room", "plate", "hall"):
            decay, tone, wet = p["alt"][1]
            irL, _ = make_ir(decay, tone)
            bufs[lane] = bufs[lane] + fft_convolve(bufs[lane], irL) * wet
        # "dry": leave it alone

    # stems: each lane panned to stereo with its space treatment, kick
    # character, and the duck baked in (duck is a plain envelope multiply,
    # so per-lane ducking sums to exactly the mix-bus duck)
    stems = {}
    if want_parts:
        for lane, (pan, *_rest) in p["lanes"].items():
            gl = np.cos((pan + 1) * np.pi / 4)
            gr = np.sin((pan + 1) * np.pi / 4)
            sL, sR = bufs[lane] * gl, bufs[lane] * gr
            if p["sidechain"] > 0 and lane != "kick":
                sL, sR = duck(sL, sR, onsets["kick"], depth=p["sidechain"])
            stems[lane] = (sL, sR)

    # stereo mix, kick kept aside so the duck breathes around it
    oL, oR = np.zeros(end), np.zeros(end)
    kL, kR = np.zeros(end), np.zeros(end)
    for lane, (pan, *_rest) in p["lanes"].items():
        gl = np.cos((pan + 1) * np.pi / 4)
        gr = np.sin((pan + 1) * np.pi / 4)
        if lane == "kick":
            kL += bufs[lane] * gl
            kR += bufs[lane] * gr
        else:
            oL += bufs[lane] * gl
            oR += bufs[lane] * gr
    if p["sidechain"] > 0:
        oL, oR = duck(oL, oR, onsets["kick"], depth=p["sidechain"])
    L, R = kL + oL, kR + oR

    if p["vinyl"]:
        L = L + vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 1)
        R = R + vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 2)
    if p["wow"] > 0:
        L = wow_flutter(L, wow_pct=p["wow"], seed=p["num"])
        R = wow_flutter(R, wow_pct=p["wow"], seed=p["num"])
    if p["mix_sat"] > 0:
        L, R = sat_unity(L, p["mix_sat"]), sat_unity(R, p["mix_sat"])
    if p["dust"] > 0:
        L, R = sp1200(L, amount=p["dust"]), sp1200(R, amount=p["dust"])

    L, R = master(L, R, drive=p["drive"])
    L, R = mono_below(L, R, 120)
    L, R, got = master_to_lufs(L, R, target=-8.0)
    if not want_parts:
        return L, R, got

    # finish the stems: the vinyl bed becomes its own stem, wow and dust
    # (the character-defining colors) print per lane, and one shared gain
    # brings the set to 0.9 peak so the balance between stems survives.
    # Mix-bus glue (mix_sat, master drive, LUFS) stays off the stems —
    # they're for editing in Reason 12; the WAV is the glued reference.
    if p["vinyl"]:
        stems["vinyl"] = (
            vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 1),
            vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 2))
    for lane, (sL, sR) in list(stems.items()):
        if lane != "vinyl":
            if p["wow"] > 0:
                sL = wow_flutter(sL, wow_pct=p["wow"], seed=p["num"])
                sR = wow_flutter(sR, wow_pct=p["wow"], seed=p["num"])
            if p["dust"] > 0:
                sL = sp1200(sL, amount=p["dust"])
                sR = sp1200(sR, amount=p["dust"])
        stems[lane] = (sL, sR)
    peak = max(max(np.abs(sL).max(), np.abs(sR).max())
               for sL, sR in stems.values())
    if peak > 0:
        stems = {ln: (sL * 0.9 / peak, sR * 0.9 / peak)
                 for ln, (sL, sR) in stems.items()}
    return L, R, got, {"events": events, "stems": stems}

# ------------------------------------------------------------------- main

README_HEAD = """
MEET THE CREW — Checkpoint 3 prototypes ({today})
{rule}
Nine invented DJ personalities, one 8-bar prototype each (bars 1-4 = A,
bars 5-8 = B). Your ears are the QA department: for each one, say what's
right and what's off ("Otto drags too much", "Glass Cat needs weirder
clicks") — the full batch of twenty only renders after the crew passes.
Where an era argued with the house sound there's an extra "Alt" file:
same beat, one treatment changed. Every character EXPERIMENTS with their
drums — kick/snare/etc are picked fresh per beat from that character's
taste — but each one's STAMP (their producer-tag hit) is locked
(crew_kits.json) and appears in everything they make.
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Scanning library for one-shots…")
    shots = build_shots()
    stamps = lock_stamps(shots)

    from datetime import date
    lines = [README_HEAD.format(today=date.today(), rule="=" * 56)]
    ok = True
    avoid = {s[0] for s in stamps.values() if s[0]}
    for name, p in sorted(CREW.items(), key=lambda kv: kv[1]["num"]):
        kit, sources = build_kit(shots, name, stamps[name][1],
                                 variant=0, avoid=avoid)
        sources["stamp"] = stamps[name][0]
        renders = [("", None)]
        if p["alt"]:
            renders.append((f" Alt {p['alt'][0]} snare", p["alt"][0]))
        for suffix, space in renders:
            L, R, got = render_crew_beat(name, kit, space=space)
            path = OUT / (f"Proto {p['num']} {name}{suffix} "
                          f"Drums {p['bpm']}bpm.wav")
            write_wav24(path, L, R)
            dur = len(L) / SR
            want = BARS * 240.0 / p["bpm"]
            rms = 20 * np.log10(np.sqrt(0.5 * (L**2 + R**2).mean()) + 1e-12)
            # LUFS is the loudness truth; plain RMS runs low on spacious
            # halftime styles (drop-out bars average in), so its floor is soft
            good = abs(dur - want) < 0.02 and -14 < rms < -5 \
                and -10 < got < -6.5
            ok &= good
            print(f"  {path.name:52s} {dur:6.2f}s  LUFS {got:5.1f}  "
                  f"RMS {rms:5.1f}  {'ok' if good else 'CHECK'}")
        lines.append(f"Proto {p['num']} — {name} ({p['bpm']}bpm, "
                     f"built on {p['built']})")
        lines.append(f"  Listen for: {p['listen']}")
        if p["alt"]:
            lines.append(f"  Alt file: era argues for a {p['alt'][0]} snare "
                         f"vs the house gated — both rendered, you pick.")
        for lane, path in sources.items():
            tag = " [their locked stamp]" if lane == "stamp" else ""
            lines.append(f"  {lane}: "
                         f"{Path(path).name if path else '(none)'}{tag}")
        lines.append("")
    with open(OUT / "README.txt", "a") as f:
        f.write("\n".join(lines))
    print(f"\nPrototypes -> {OUT}\nStamps locked -> {LOCK}")
    if not ok:
        print("WARNING: at least one render failed its numeric sanity check.")


if __name__ == "__main__":
    main()
