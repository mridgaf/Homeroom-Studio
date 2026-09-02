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
import re
import sys
import zlib
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from pattern_gen import DEFAULT_STYLE, STYLE_VERSION
from make_drum_loops import SR, master, write_wav24
from make_drum_beats import build_shots, duck
from make_hiphop_tracks import load_audio, norm_rms
from groove import (LaneFeel, OWNER_TASTE, dist808, gated_reverb,
                    glue_compress, loop_convolve, make_ir, master_to_lufs,
                    mono_below, mpc_swing_offset, perc_scale, roughness_am,
                    sat_unity, snare_scale, sp1200, velocity, vinyl_bed,
                    wow_flutter)

OUT = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))
LOCK = Path(os.path.expanduser("~/.reason_voice/crew_kits.json"))
BARS = 8                         # the old fixed loop; now only a fallback


def bars_of(preset):
    """How many bars THIS beat runs (owner call 2026-07-22: "make the
    loops half as long" + let the length vary per beat). A preset that
    doesn't say falls back to the historic 8, so every older recipe and
    batch file re-renders at exactly the length it was written at."""
    try:
        n = int((preset or {}).get("bars") or BARS)
    except (TypeError, ValueError):
        return BARS
    return n if 1 <= n <= 16 else BARS
SNARE_LIKE = {"snare", "clap"}   # lanes that follow the owner's snare trim
# bright percussion that reads louder than it meters — owner 2026-07-18:
# snaps/bells/stamps sat over the kick, so they get their own bus trim
# (startswith match covers stamp2/stamp3 collab lanes)
PERC_LIKE = {"snap", "stamp", "bell", "cowbell", "rim", "tamb"}

# OWNER MIX HIERARCHY, 2026-08-03. His words: "the snap and claps and bells
# are always quieter than the snare and the kick drum. The hi hats follow the
# same rules as the claps." And on where to anchor it: "start with the
# loudness of the kick and the snare where they're at right now and go from
# there" — so kick and snare are the reference and are NEVER touched by this.
#
# The reference is the QUIETER of the kick and the snare, not the kick alone.
# Before this the ceilings were kick-relative, which let a clap sit under the
# kick while still being louder than the snare — his rule says under both.
#
# Everything here only ever ATTENUATES, so an identity that deliberately
# tucks a lane away keeps it tucked away.
PERC_UNDER_DB = -3.0      # EVERY drum that is not the kick or the snare
PUNCTUATION_UNDER_DB = -6.0   # crashes, impacts, risers — punctuation
MELODIC_UNDER_DB = -6.0   # chords/bass: under the backbone AND the perc tier

# THE BLANKET RULE (owner 2026-08-03, after hearing beat 1763): "anything
# named shaker or impacts or effects or percussion or any other 'drum' sound
# that is not the kick and the snare should follow the same volume rule as
# for hi hats. Unless otherwise stated this session."
#
# So this is a DEFAULT, not a list. The old version was a list of prefixes
# and it kept missing lanes — congas, toms, woods, claves, blips, cutfx,
# foundfx, glitches, mathperc, exotic, gamefx and every guest lane a future
# pool adds were all uncovered, which is exactly how a shaker came out at
# -1.6 dB. Now everything falls to PERC_UNDER_DB unless it is named here.
BACKBONE_LANES = ("kick", "snare")        # the reference — never adjusted
# The LOW END is exempt, same set the ambience bed already refuses to touch
# (`dry_lows`). "sub" is the tuned sub and plain "bass" is the sampled 808 —
# both are the kick's own low end rather than a percussion colour, and
# capping them 3 dB under the kick would hollow the beat out. Note this is
# the digit-less "bass": bass0..N are the MELODIC chord bass and do fall
# under the melodic ceiling below, which is why the check is exact.
_LOW_END = {"sub", "bass", "sub808", "808"}
PEAK_CEILING_DB = {
    # louder than the perc floor: nothing. quieter: these two families.
    "crash": PUNCTUATION_UNDER_DB,
    "impact": PUNCTUATION_UNDER_DB,
    "swellfx": PUNCTUATION_UNDER_DB,
    "riser": PUNCTUATION_UNDER_DB,
    "siren": PUNCTUATION_UNDER_DB,
    # Melodic lanes: "the instruments are not louder than the kick drum or
    # the snap. or the snare" — so they must clear the PERCUSSION tier too,
    # not just the backbone. The chord governor sets the bus's RMS (15 dB
    # under the kick), but RMS says nothing about a transient: a piano stab
    # measured a 1.8 dB peak under the reference while snaps sat at 2.0.
    "chord": MELODIC_UNDER_DB,
    "bass": MELODIC_UNDER_DB,
}
# longest first, so "cowbell" is matched before "bell" would swallow it
_PEAK_PREFIXES = sorted(PEAK_CEILING_DB, key=len, reverse=True)

# How far over the kick the BACKBEAT may peak (owner 2026-09-02). There was
# no rule here at all: kick and snare are the reference pair and both return
# None from peak_ceiling_for, so nothing ever measured the snare's peak
# against anything. The RMS governor above then made that reachable — a snare
# with a sharp crack has a low average and a high peak, so lifting it by
# average sent the peak a long way over the kick (measured on beat 2159:
# +9.9 dB, from +5.3 before the governor).
#
# 2.0 comes from the reference mix the owner asked me to check against: a
# measured hip-hop/trap master with the kick at -5.1 dBTP and the snare at
# -3.6, i.e. the backbeat peaking 1.5 dB OVER the kick while the two sit
# level in loudness. Slightly over is normal and is the sound of a record;
# ten dB over is not. This is a CEILING, not a target — where the backbeat
# actually lands is set by backbeat_bus_under_kick_db and the sample's own
# crest factor.
BACKBEAT_OVER_KICK_DB = 2.0


def peak_ceiling_for(lane):
    """dB below the kick/snare reference this lane may peak, or None for the
    backbone itself. Anything not named falls to the perc floor — that is the
    blanket rule, and the reason it is a default rather than a lookup."""
    if lane.startswith(BACKBONE_LANES) or lane in _LOW_END:
        return None
    for pre in _PEAK_PREFIXES:
        if lane.startswith(pre):
            return PEAK_CEILING_DB[pre]
    return PERC_UNDER_DB

# How far the chord-bus governor may turn a lane DOWN (owner 2026-08-03).
# 0.02 is -34 dB, enough for the loudest sample measured in his library with
# room to spare, and far enough from zero that a lane can never be silenced
# by the governor alone. See the note at the clamp itself for why the cut and
# the boost limits are deliberately not the same number.
CHORD_CUT_FLOOR = 0.02

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
    # ------------------------------------------------------------------
    # New Math, deepened 2026-07-24 at the owner's request ("give it
    # deeper personality/style of your own design, along with adding that
    # [video game] sound"). The design brief I set myself, written down so
    # the character stays coherent if anyone extends it later:
    #
    #   ONE IDEA, FOUR DOMAINS: arithmetic you can hear.
    #
    # His rhythm was already division — five against four, Euclidean
    # necklaces (spreading k hits evenly over n steps), clash-as-groove.
    # Chip sound is division too: a square wave is a counter flipping
    # between two states, the noise channel is a shift register, the
    # faked chord is counting fast enough to fool the ear, and the
    # Atari's sourness is integer division failing to land on a note.
    # So the chiptune voice is not a costume on this character — it is
    # the same idea he already was, in a new domain. The three additions:
    #
    #   HARMONY   progressions that divide the octave into EQUAL parts
    #             (minor thirds = 4, major thirds = 3, whole tones = 6)
    #             instead of resolving. Every other identity on every
    #             roster uses functional harmony, which has a home to
    #             return to. These have no home; they just come back
    #             around. That is the harmonic form of a polyrhythm.
    #   TUNING    chip_tuning "atari" — chords snap to the TIA's
    #             integer-divider grid, so they are genuinely out of
    #             tune. Everyone else calls that broken; he calls it the
    #             number the division actually gives. This is the
    #             character trait, and it is the one thing here I would
    #             expect the owner to either love or veto outright.
    #   RIPPLE    chip_count 5 — the chord flickers five times a beat, so
    #             his five-against-four hat idea now also runs in the
    #             harmony, drifting against the bar and re-aligning.
    #
    # Mode is major on purpose: none of these progressions are minor in
    # any functional sense, and the bright chip square against a hard
    # club kick is the "front edge" the character is named for.
    "New Math": dict(
        num=9, bpm=144, era="now", built="no one — the front edge",
        listen=("the new one. A club kick pattern that never sits where "
                "trap taught you to expect it; a hat lane counting FIVE "
                "against everyone else's four (quintuplet grid); "
                "percussion running world-rhythm math (E(7,16) and "
                "E(5,16) necklaces); and one lane swinging 58% while the "
                "rest of the kit stays dead straight — the clash IS the "
                "groove. Clean and punchy, mid-forward kick. Stamp is a "
                "found-sound fx hit on the tail of bars 4/8. Harmony is "
                "an 8-bit square-wave ripple counting five to the beat, "
                "on chords that divide the octave into equal steps and "
                "never resolve — and it is tuned to an Atari's own "
                "arithmetic, so it lands slightly, deliberately sour"),
        signature=dict(
            key=dict(roots=[["C", 3], ["D", 2], ["G", 2], ["A", 2],
                            ["F", 1]], mode="major"),
            progressions=[["math_minor_thirds", 3], ["math_major_thirds", 3],
                          ["math_whole_tone", 2], ["vamp_static_riff", 1]],
            chord_source=[["chip", 1]],
            chord_rhythm="arp",
            chip_tuning="atari",
            chip_count=5,
            # his harmony IS the chip voice, so it should not need the
            # notes box to ask for it — see beat_machine's chords_default
            chords_default=True),
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

# REASON_VOICE_CONFIG (2026-07-17, autoresearch): point the engine at a
# CANDIDATE roster file — the experiment loop scores tuned copies without
# the live config ever moving. Unset = the real crew_config.json.
CONFIG = Path(os.environ.get("REASON_VOICE_CONFIG")
              or Path(__file__).resolve().parent.parent
              / "crew_config.json")


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


# ---------------------------------------------------------- harmony DNA
# Owner directive 2026-07-24: give the previous DJs harmonic identities
# too, "where it would fit for their identity/style".
#
# Two rules I held myself to, so these are derived and not invented:
#  1. Every signature comes from that DJ's OWN `listen` text, not from
#     the real producer they were built on. Otto Grit's is dusty because
#     his line says SP-1200 dust and vinyl; Chrome Dial's is a drone
#     because his says "silence as an instrument".
#  2. Where a crew member shares a producer with a LEGEND, they are
#     deliberately voiced differently. The legends are strict likenesses
#     and never evolve; the crew are loose and do. Same source, own
#     character — otherwise the two rosters collapse into each other.
#
# These lean on the sampled instrument groups added 2026-07-23
# (instrument_sampler.VOICES), which is what makes them separable at all
# — before that every identity could only ask for loop/synth/strings.
# Worth noting: the legends research flagged "pluck/bell timbre vs huge
# negative space" as a distinguishing trait with NO FIELD to express it.
# There is one now, and Glass Cat is built on exactly that.
CREW_SIGNATURES = {
    # dusty soul keys, played late. Dilla-lineage but PIANO-forward where
    # the J Dillo legend is loop-forward — same warmth, different hands.
    "Otto Grit": dict(
        key=dict(roots=[["F", 3], ["C", 2], ["Bb", 2], ["G", 1]],
                 mode=[["minor", 2], ["major", 2]]),
        progressions=[["nostalgic_jazz", 3], ["dreamy", 3],
                      ["vamp_ii_V", 2], ["nostalgic_borrowed_minor", 2]],
        chord_source=[["piano", 3], ["loop", 2]],
        chord_rhythm=[["sustain", 2], ["arp", 1]]),

    # surgical: one hard stab, no wash. Brass stabs rather than the
    # legend's loop+synth, because his whole line is "scratch stab".
    "Cutz": dict(
        key=dict(roots=[["C", 2], ["D", 2], ["G", 2], ["A", 1]],
                 mode="minor"),
        progressions=[["vamp_static_riff", 3], ["vamp_i_iv7", 3],
                      ["dark_menacing", 2]],
        chord_source=[["horns", 3], ["loop", 3]],
        chord_rhythm="arp"),

    # the horn loop IS this character (Pete Rock lineage), and it keeps
    # him from colliding with Otto Grit, who owns the keys.
    "Crate Prophet": dict(
        key=dict(roots=[["F", 3], ["Bb", 2], ["C", 2], ["G", 2]],
                 mode=[["minor", 2], ["major", 1]]),
        progressions=[["nostalgic_jazz", 3], ["vamp_ii_V", 2],
                      ["vamp_i_iv7", 2], ["nostalgic_borrowed_minor", 2]],
        chord_source=[["horns", 3], ["loop", 3], ["piano", 1]],
        chord_rhythm=[["sustain", 3], ["arp", 1]]),

    # "silence as an instrument" -> almost no chord movement at all, and
    # an exotic wood/flute voice to match "exotic perc off-center".
    "Chrome Dial": dict(
        key=dict(roots=[["D", 2], ["A", 2], ["E", 2], ["C", 1]],
                 mode="minor"),
        progressions=[["vamp_static_riff", 4], ["dark_menacing", 3],
                      ["vamp_i_VI", 1]],
        chord_source=[["wood", 3], ["synth", 2]],
        chord_rhythm=[["sustain", 3], ["arp", 2]]),

    # minimal, dry, icy. This is the bell/pluck + negative-space trait
    # the legend research said had no field. Two-chord vamps only.
    "Glass Cat": dict(
        key=dict(roots=[["C", 2], ["G", 2], ["A", 2], ["E", 1]],
                 mode="minor"),
        progressions=[["vamp_static_riff", 3], ["vamp_i_v7", 3],
                      ["vamp_i_iv7", 2]],
        chord_source=[["bell", 3], ["pluck", 2]],
        chord_rhythm="arp"),

    # gospel bounce: major-leaning, piano-led, choir behind it.
    "Sunday Chop": dict(
        key=dict(roots=[["C", 3], ["F", 2], ["G", 2], ["Bb", 1]],
                 mode=[["major", 3], ["minor", 1]]),
        progressions=[["uplifting", 3], ["nostalgic_borrowed_minor", 2],
                      ["sad_accepting", 2], ["nostalgic_jazz", 1]],
        chord_source=[["piano", 3], ["choir", 2], ["loop", 1]],
        chord_rhythm=[["sustain", 3], ["arp", 1]]),

    # dark halftime drama. trap_dark_metro is literally the progression
    # named for this sound; bells over a pad is the trap-bell cliche and
    # he is the one character who should own it.
    "Night Metro": dict(
        key=dict(roots=[["C", 2], ["D", 2], ["F", 2], ["A", 2]],
                 mode="minor"),
        progressions=[["trap_dark_metro", 3], ["dark_menacing", 3],
                      ["vamp_static_riff", 2], ["vamp_i_VI", 1]],
        chord_source=[["bell", 3], ["pad", 2], ["loop", 1]],
        chord_rhythm=[["sustain", 2], ["arp", 3]]),

    # relentless and cinematic: the big orchestral stab over a trap wall.
    "Rage Engine": dict(
        key=dict(roots=[["C", 2], ["D", 2], ["E", 1], ["A", 2]],
                 mode="minor"),
        progressions=[["epic", 3], ["dark_menacing", 3],
                      ["trap_dark_metro", 2]],
        # "strings" (plural) = the London Symphonic library via
        # string_sampler, which names an exact MIDI note per file and so
        # never pitch-shifts. NOT "string" — that is an instrument_sampler
        # GROUP name, not a chord_source word, and it silently fell
        # through to horns until this was caught 2026-07-24.
        chord_source=[["strings", 3], ["horns", 2]],
        chord_rhythm=[["sustain", 2], ["arp", 2]]),
}

for _n, _sig in CREW_SIGNATURES.items():
    DEFAULT_CREW[_n]["signature"] = _sig


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
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False))
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
        # A crew member's harmony `signature` (New Math got the first one,
        # 2026-07-24) is added to an existing config if it's missing, but
        # NEVER overwritten — unlike the style keys above, this is meant to
        # be hand-tunable and survive. Same add-only contract genres.py
        # uses for a brand-new style.
        for n, p in raw.items():
            if not n.startswith("_") and n in DEFAULT_CREW \
                    and "signature" in DEFAULT_CREW[n] \
                    and "signature" not in p:
                p["signature"] = json.loads(
                    json.dumps(DEFAULT_CREW[n]["signature"]))
                changed = True
        if changed:
            path.write_text(json.dumps(raw, indent=1, ensure_ascii=False))
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

# The Legends (owner request 2026-07-18): a SECOND roster of twelve
# signature-style producers, kept in their own legends_config.json but
# merged into CREW so every engine function (build_kit, render_crew_beat,
# compose, collabs) reaches them by name with no special-casing. Their
# LIKENESS rules key off CREW[name]["legend"] downstream. They still lock
# stamps and experiment with samples like the nine; only their patterns
# and feel stay faithful. LEGEND_NAMES lets the UI put them in a separate
# box and lets evolution skip them (a legend's career is already written).
# Updated IN PLACE, never rebound (2026-08-04). Other modules do
# `from crew import LEGEND_NAMES` at import, which binds the OBJECT, not
# the name — so assigning a fresh set here left every importer holding a
# stale copy after a reload. It went unnoticed only because both copies
# load from the same file and so happen to agree. Same trap that dropped
# the Legends out of CREW; closed the same way, by mutating the one object.
LEGEND_NAMES = set()


def merge_legends(target):
    """Load the Legends roster and fold it into `target` (the shared CREW
    dict), returning their names. Kept a function so anything that rebuilds
    CREW — the module import here, and tests that reset the roster — can
    restore the Legends the same way instead of dropping them."""
    try:
        import legends
        leg = legends.load_legends(normalize_preset)
    except Exception as e:                    # never let a legend break the nine
        print(f"WARNING: Legends roster unavailable ({e}).")
        return LEGEND_NAMES                   # a failed load changes nothing
    target.update(leg)
    LEGEND_NAMES.clear()
    LEGEND_NAMES.update(leg)
    return LEGEND_NAMES


# The Styles (owner request 2026-07-19): a THIRD roster, keyed to
# subgenres rather than people — Baltimore club, reggaeton, Memphis,
# bounce and the rest. Same merge contract as the Legends, so the whole
# engine reaches them by name; their strictness rules key off
# CREW[name]["genre"] downstream (canon lanes placed verbatim, pinned
# swing, no cross-pollination, no evolution, per-style density).
GENRE_NAMES = set()          # in place, never rebound — see LEGEND_NAMES


def merge_genres(target):
    """Load the Styles roster and fold it into `target` (the shared CREW
    dict), returning their names. Same shape as merge_legends so anything
    rebuilding CREW restores all three rosters the same way."""
    try:
        import genres
        gen = genres.load_genres(normalize_preset)
    except Exception as e:                    # never let a style break the nine
        print(f"WARNING: Styles roster unavailable ({e}).")
        return GENRE_NAMES                    # a failed load changes nothing
    target.update(gen)
    GENRE_NAMES.clear()
    GENRE_NAMES.update(gen)
    return GENRE_NAMES


merge_legends(CREW)
merge_genres(CREW)


def reload_rosters(target=CREW, path=None):
    """Rebuild `target` into the COMPLETE roster — the nine, the Legends,
    and the Styles — from whatever config files are currently in force.

    Anything that resets CREW should call this rather than reassembling
    the rosters by hand: test_evolution's sandbox teardown used to
    re-merge only the Legends, so adding a third roster silently dropped
    it for every module that ran afterwards (2026-07-19). One call means
    a fourth roster can never reintroduce that bug.

    `path` is read at call time, not bound at import, so a sandboxed
    crew.CONFIG (tests) reloads from the sandbox and not the real file."""
    target.clear()
    target.update(load_crew(path or CONFIG))
    merge_legends(target)
    merge_genres(target)
    return target

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
    if OWNER_TASTE.get("open_soundbank"):
        # owner 2026-07-18: no limits on a DJ's sound bank — the whole
        # role pool is fair game, taste tags and must-words stop gating
        wants, must = [], None
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
    if res == 12:                # 3/4 or 6/8: strong-weak on the 12-grid
        if s % 4 == 0:
            return 1.0
        return 0.85 if s % 2 == 0 else 0.72
    if res == 24:                # triplet grid in 4/4 (genre roster
        if s % 6 == 0:           # 2026-07-19): six per beat, so beats
            return 1.0           # start every 6 and the triplet 8ths
        return 0.86 if s % 2 == 0 else 0.7    # sit on the even steps
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
    # v6 (2026-07-18): real time signatures. 3/4 and 6/8 bars both span
    # three quarter-note beats; 4/4 stays the default four.
    num, den = p.get("tsig", (4, 4))
    bar_s = num * (4.0 / den) * 60.0 / bpm
    nbars = bars_of(p)
    end = int(round(nbars * bar_s * SR))
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
        percish = any(lane.startswith(s) for s in PERC_LIKE)
        g = gain * (snare_scale() if snarish
                    else perc_scale() if percish else 1.0)
        snd = kit[lane]
        buf = np.zeros(n)
        ons, evs = [], []
        for b in range(nbars):
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

    # owner 2026-07-18: clean renders — every dirt stage (808 dist,
    # roughness, saturation, dust, vinyl, wow) stays off; he adds his own
    # color in Reason. Presets keep their dirt numbers so flipping
    # OWNER_TASTE["clean_renders"] back restores each character's grime.
    clean = OWNER_TASTE.get("clean_renders", False)
    if not clean and p["kick_dist"] > 0 and "kick" in bufs:
        bufs["kick"] = dist808(bufs["kick"], p["kick_dist"])
    if not clean and p.get("rough_808") and "kick" in bufs:
        rate, depth = p["rough_808"]
        bufs["kick"] = roughness_am(bufs["kick"], rate, depth)

    space = space or p["space"][0]
    # 2026-07-31: make_ir() has ALWAYS returned a stereo pair of decorrelated
    # IRs (groove.py:303, docstring "Stereo IR") and this block used to do
    # `irL, _ = make_ir(...)` — throwing the right channel away and printing a
    # mono reverb. Measured consequence: every rendered beat came out with
    # side energy 22-31 dB under mid, i.e. effectively mono, and all 247 core
    # stems checked were bit-identical L/R. The reverb is the one stage in the
    # chain designed to create width, so restoring its right channel is the
    # cheapest real fix. Chord lanes are deliberately NOT panned apart: chord0
    # /1/2 are the progression's chords in SEQUENCE (verified — zero overlap),
    # so panning them would swing the progression across the image.
    wet_side = {}
    treated = set()          # the lanes this block ACTUALLY treated
    # a treated lane may have been removed outright (stem rack
    # 2026-07-21) — treat what's actually here
    for lane in [ln for ln in p["space"][1] if ln in bufs]:
        if space == "gated":
            # hold scales to tempo — one 8th note (school 2026-07-15;
            # forums put 80s drama at 300+ ms, which a 90 bpm 8th hits)
            bufs[lane], wet_side[lane] = gated_reverb(
                bufs[lane], onsets[lane],
                wet=OWNER_TASTE["gate_wet"],
                hold_ms=min(30000.0 / bpm, 350.0),
                loop=True, stereo=True)
            treated.add(lane)
        elif space in ("room", "plate", "hall", "washed"):
            # v6: every DJ can roll a wet space per beat — use the era
            # Alt params when the preset carries them, house defaults
            # otherwise
            defaults = {"room": (0.45, 3500, 0.32),
                        "plate": (0.9, 6500, 0.34),
                        "hall": (1.8, 2800, 0.3),
                        # "washed" IS plate, deliberately the same numbers
                        # rather than a new sound: beat_machine.py:977
                        # already maps the typed word washed -> plate, so a
                        # bigger bespoke reverb here would make the same word
                        # mean two different things depending on whether he
                        # typed it or a genre preset declared it.
                        "washed": (0.9, 6500, 0.34)}
            alt = p.get("alt")
            decay, tone, wet = (alt[1] if alt and alt[0] == space
                                and alt[1] else defaults[space])
            irL, irR = make_ir(decay, tone)
            dry = bufs[lane]
            wetL = loop_convolve(dry, irL) * wet
            wetR = loop_convolve(dry, irR) * wet
            # bufs[] keeps the true MONO FOLD-DOWN, which is what every
            # downstream reader wants — the snare-vs-kick backstop just
            # below, _track_gain, _preview_mix, the stem peak-normalise.
            # Measured, so it's not hand-waved: the per-channel wet level is
            # UNCHANGED (+0.00 dB — L still gets exactly irL, as before),
            # while the wet's mono fold-down drops 2.9 dB because two
            # decorrelated channels partially cancel when summed. That is
            # physically correct, not a loss. On a whole beat the dry signal
            # dominates, so the figure those readers actually see moves
            # 0.18 dB. Nothing downstream needed retuning.
            bufs[lane] = dry + (wetL + wetR) * 0.5
            # ...and the decorrelated half rides along as a side signal,
            # folded in at pan time below. mono_below(120) still collapses
            # the bass, so this cannot smear the low end.
            wet_side[lane] = (wetL - wetR) * 0.5
            treated.add(lane)
        # "dry" leaves the lane alone, so it does NOT go in `treated`.
        #
        # "washed" used to land here too, which was the bug (fixed
        # 2026-09-02, owner's call). Four genre presets declare
        # space=("washed", ...) and beat_machine locks a genre to its
        # declared space, so Houston Screw, Emo Hip Hop, Horror Rap and Plug
        # had never had ANY space treatment across 24 shipped recipes, while
        # their own style notes say the opposite ("horrorcore is drowned").
        # They now take the plate branch above.

    # ---- house ambience bed (owner standing rule, 2026-07-31) ----
    # "In order to have studio ready quality tracks I want you to be able to
    #  use reverb and any other effect, as much as needed, for quality and
    #  style and dj. It can even vary instrument to instrument. This
    #  overrules any other command where sound is concerned."
    #
    # Every DJ's space list turned out to be ONE lane — `["snare"]` or
    # `["clap"]`. Nothing else in the mix had ever seen a reverb: chords,
    # melodic parts, bongos, stamps and guest colour all printed bone dry.
    # That is most of why a finished beat sounded small next to a record,
    # and it is why beats that rolled space="dry" came out near-mono.
    #
    # This runs REGARDLESS of the rolled space, including "dry" — per the
    # rule above, a quality floor is not a per-beat style choice. The DJ's
    # signature snare/clap treatment above is untouched, so identity still
    # comes from that; this is the room those parts sit in.
    #
    # Deliberately NOT treated: kick, the sampled 808 ("bass"), the tuned
    # sub, and any lane the DJ already treated. Low end must stay dry and
    # centred or the punch goes with it.
    HARMONIC_RE = re.compile(r"^(chord\d|bass\d)")
    # WHAT THE BLOCK ABOVE ACTUALLY TREATED, not what the preset asks for.
    # This used to be `set(p["space"][1])`, which is a different question:
    # `space` is what THIS render rolled and beat_machine rolls it per beat
    # (35% of them dry), so on a dry roll the DJ's snare/clap lane was
    # excluded from the bed as "already treated" while the dry branch had
    # left it alone — and that lane is the loudest thing in the beat after
    # the kick. Measured 2026-09-01 across the 48 beats rendered since the
    # last crew.py change: 9 sat at or under the -22 dB S/M mono line, 8 of
    # them dry rolls, worst -36.2 dB, with the snare and clap stems
    # bit-identical L/R. The same hole swallowed the four "washed" genre
    # presets, whose space string no branch above implemented until
    # 2026-09-02; they take the plate branch now, but the bed still has to
    # catch their sibling backbeat lane like everyone else's.
    already = treated
    dry_lows = {"kick", "bass", "sub"}
    # MONO BACKSTOP (owner 2026-08-01: "fix beat 1679"). The bed used to skip
    # the whole snare bus — "the DJ's call" — unless the beat was drums-only
    # AND bone dry. Three separate holes came out of that one condition, all
    # of them the same shape: a lane that NOTHING treated, excluded from the
    # bed anyway, printing bit-identical L/R.
    #   * a dry roll (35% of beats) over a preset that declares gated;
    #   * a "washed" preset, a space string no branch above implemented
    #     (fixed 2026-09-02 — washed is now plate);
    #   * the sibling backbeat lane on ANY beat — every DJ's space list names
    #     exactly one of snare/clap, so the other one was never treated and
    #     never bedded. Measured on 2105 (Mustang, gated): the snare sat
    #     3.6 dB under the kick and printed dual-mono.
    # So the rule is now simply: treated by the DJ's space, or bedded here.
    #
    # The chord bed cannot stand in for this. On 2143, a dry Kane East with
    # three chord lanes, the kick stem measures -17.8 dB RMS, the snare -35.3
    # and the clap -43.4 — 25-30 dB of air cannot move the image.
    #
    # Justified by his standing rule of 2026-07-31: effects in service of
    # QUALITY overrule a per-beat style choice. The DJ's signature treatment
    # is untouched wherever it actually ran, and the low end is never
    # touched either way.
    for lane in bufs:
        if lane in already or lane in dry_lows:
            continue
        if HARMONIC_RE.match(lane):
            decay, tone, wet = 1.4, 3200, 0.18   # air around the harmony
        elif any(lane.startswith(s) for s in SNARE_LIKE):
            decay, tone, wet = 0.6, 4000, 0.14   # the backbeat's own room
        else:
            decay, tone, wet = 0.5, 4200, 0.10   # a touch of room on colour
        irL, irR = make_ir(decay, tone, seed=4242 + p["num"])
        dry = bufs[lane]
        wetL = loop_convolve(dry, irL) * wet
        wetR = loop_convolve(dry, irR) * wet
        bufs[lane] = dry + (wetL + wetR) * 0.5
        side = (wetL - wetR) * 0.5
        wet_side[lane] = wet_side.get(lane, 0.0) + side

    # BACKBEAT BUS GOVERNOR (owner 2026-09-02). Was a one-way cap: "the
    # snare bus never out-powers the kick" (owner 2026-07-18), which is
    # still true below and still the hard rule — but it only ever turned
    # the backbeat DOWN, so how loud it landed was set by nothing except
    # which sample happened to get picked. Measured across 64 shipped
    # beats: a median 3.8 dB under the kick, which is right, and a SPREAD
    # of 19.5 dB around it (15.7 under to 3.8 over). At the bottom of that
    # range the beat is a kick with whispers behind it, which is what he
    # heard as "not enough effects".
    #
    # This is the same failure the chord bus had, and the same fix he
    # approved on 2026-07-31: an open-loop gain cannot hit a target when
    # the source samples vary that much, so govern the BUS in BOTH
    # directions. Target OWNER_TASTE["backbeat_bus_under_kick_db"].
    #
    # The clamp is asymmetric the opposite way to the chord governor's, and
    # deliberately: the BOOST is capped at 4.0 (+12 dB) so a hopeless sample
    # cannot be hauled up with its own noise floor, and the CUT is left
    # uncapped so the 2026-07-18 hard rule holds by construction — the
    # target is 3 dB under the kick, which is already past the 1 dB line, so
    # a bus that lands on target can never out-power the kick and the old
    # separate backstop has nothing left to do.
    if "kick" in bufs:
        kick_rms = np.sqrt((bufs["kick"] ** 2).mean())
        sn = [ln for ln in bufs
              if any(ln.startswith(s) for s in SNARE_LIKE)]
        if kick_rms > 0 and sn:
            bus = sum(bufs[ln] for ln in sn)
            bus_rms = np.sqrt((bus ** 2).mean())
            want = kick_rms * 10 ** (
                -OWNER_TASTE.get("backbeat_bus_under_kick_db", 3.0) / 20)
            if bus_rms > 1e-9:
                adj = min(want / bus_rms, 4.0)
                for ln in sn:
                    bufs[ln] = bufs[ln] * adj
                    # ...and its reverb with it. The chord governor below and
                    # the peak ceiling below that both do this; this one did
                    # not, and it was harmless only because the snare bus had
                    # no wet_side to leave behind — the ambience bed used to
                    # skip the whole family. Now that it doesn't, a trimmed
                    # snare would have kept its full-strength tail: measured
                    # on 2122, a 2.38 dB trim left the reverb 2.38 dB louder
                    # relative to the drum making it, and the rule's own
                    # promise ("whatever the reverb energy added up to") was
                    # being kept on the mono fold only.
                    if ln in wet_side:
                        wet_side[ln] = wet_side[ln] * adj

        # the harmonic bus gets the same governor (2026-07-31). Unlike the
        # snare's, this one corrects in BOTH directions: a chord bed that
        # lands too quiet is the more common failure and an open-loop gain
        # cannot fix it. Measured across 39 shipped beats the loudest chord
        # part sat a median 15.4 dB under the kick (worst 24.9, best 5.9) —
        # a 19 dB spread, entirely from how loud the chosen samples happened
        # to be. Raising OWNER_TASTE["chord_gain"] moved the whole range up
        # without narrowing it, which just swapped "inaudible" for
        # "shouting". Targeting the bus is what actually holds it steady.
        ch = [ln for ln in bufs if re.match(r"^(chord\d|bass\d)", ln)]
        # BUG FIXED 2026-08-03 (owner: "it's always way too loud"). This
        # divided the bus's total energy by the COMBINED length of all the
        # chord lanes instead of by the length of the beat, so it under-read
        # the bus by 10*log10(number of lanes) and left the chords that much
        # louder than the target. Chord slots are sequential, so N lanes each
        # sounding 1/N of the time still sum to a bus that plays the whole
        # way through — dividing by N*len is measuring the average lane, not
        # the bus. Measured before the fix on 34 real beats: target -9.0 dB
        # under the kick, actual -4.6 dB, with a median of 3 chord lanes
        # (3 lanes = 4.8 dB, which is the whole discrepancy).
        # The snare governor immediately above always did this correctly —
        # `bus = sum(...)` then RMS — which is why nobody caught it here.
        ch_rms = np.sqrt((sum(bufs[ln] for ln in ch) ** 2).mean()) if ch \
            else 0.0
        if kick_rms > 0 and ch_rms > 1e-9:
            want = kick_rms * 10 ** (
                -OWNER_TASTE.get("chord_bus_under_kick_db", 9.0) / 20)
            # ASYMMETRIC on purpose (owner 2026-08-03, "it's always way too
            # loud"). The clamp used to be symmetric at +/-12 dB, and the
            # stated reason — "a pathological sample can't be hauled up 30 dB
            # and drag its own noise floor into the mix" — is an argument
            # about BOOSTING only. Turning a lane DOWN cannot raise anyone's
            # noise floor, so the floor half of that clamp was protecting
            # against nothing while doing real harm.
            #
            # Measured with a probe in this function: a loud chord sample
            # needed adj 0.148 (a 16.6 dB cut) and a very loud one 0.074
            # (22.6 dB) — both were clamped at 0.25 and shipped 4.6 and
            # 10.6 dB over target. That is the "always too loud", and it gets
            # worse the further back he asks the chords to sit, because a
            # bigger target means a bigger cut.
            #
            # Boost ceiling unchanged at 4.0 (+12 dB) — that one is real, and
            # tests/test_audio_quality.py pins that a hopeless sample is NOT
            # rescued, so nobody quietly loosens it.
            adj = min(max(want / ch_rms, CHORD_CUT_FLOOR), 4.0)
            for ln in ch:
                bufs[ln] = bufs[ln] * adj
                # the ambience bed above already stashed this lane's stereo
                # half; it has to move with the lane or the reverb ends up
                # louder than the sound making it
                if ln in wet_side:
                    wet_side[ln] = wet_side[ln] * adj

        # MOVED here 2026-08-03, AFTER the chord governor. It used to run
        # before it, which was fine while it only touched drums — but the
        # melodic ceiling added today would have been undone immediately,
        # since the governor rescales the whole chord bus straight after.
        # Trimming a transient barely moves RMS, so the governor's bus
        # level survives this; the reverse order does not work.
        # PEAK ceiling for the bright transient lanes (owner 2026-08-01,
        # "clap and crash are being overused"). The bus governors above work
        # on RMS, which is the right control for a sustained bed but blind to
        # a single loud transient: measured across 42 rendered beats the clap
        # PEAKED a median 1.2 dB ABOVE the kick (worst +8.4) and the crash
        # +3.7 (worst +9.4), while their RMS sat politely underneath. A hit
        # that spikes over the kick reads as "too much" however quiet its
        # average is — that is why the clap felt overused even on beats where
        # it was correctly placed.
        #
        # Peak-only, and it only ever turns things DOWN, so a lane that is
        # already sitting under the kick is untouched and no identity gets
        # quietly re-balanced. Ceilings are per-family, not one number: a
        # backbeat is meant to be nearly as strong as the kick, a cymbal
        # crash is punctuation and belongs below it.
        # The reference is the QUIETER of kick and snare (owner 2026-08-03:
        # the small percussion must sit under BOTH). Falls back to the kick
        # alone on a beat with no snare — several identities have only a
        # clap, and on those the clap IS the backbeat, so it is measured
        # against the kick and nothing else.
        # Everything below is measured AFTER the constant-power pan, because
        # that is what the listener and the stem file get. Missed on the
        # first pass and it is worth spelling out: a CENTRED lane gets 0.707
        # per side, a lane panned hard gets up to 1.0 on its loud side. The
        # kick is centred and percussion is not, so comparing raw buffers
        # let a hat capped at -3 dB arrive ~1 dB louder than that against
        # the kick — which is exactly the residue the owner still heard on
        # the shaker after the first fix.
        # ...and after the SIDECHAIN DUCK, which is the last thing between
        # here and the stem. Only the kick sits outside its own duck, so
        # every other lane is pulled down wherever a kick lands — and
        # because it is time-varying, how much a lane loses depends on
        # whether its loudest hit falls on a kick or between them. Left out
        # of the first two attempts and it was the whole of the residue:
        # three lanes on one beat sitting ~1 dB over their cap.
        _duck_env = None
        if p["sidechain"] > 0 and onsets.get("kick"):
            _duck_env = np.ones(end)
            _L = int(0.11 * 3 * SR)
            _dip = 1 - p["sidechain"] * np.exp(-np.arange(_L) / (0.11 * SR))
            for _pos in onsets["kick"]:
                _e = min(end, _pos + _L)
                if _pos < end:
                    _duck_env[_pos:_e] = np.minimum(_duck_env[_pos:_e],
                                                    _dip[:_e - _pos])

        def _panned_pk(ln):
            row = p["lanes"].get(ln)
            pan = row[0] if row else 0.0
            side = max(np.cos((pan + 1) * np.pi / 4),
                       np.sin((pan + 1) * np.pi / 4))
            eff = np.abs(bufs[ln]) * side
            w = wet_side.get(ln)
            if w is not None:
                eff = eff + np.abs(w)
            if _duck_env is not None and ln != "kick":
                eff = eff[:end] * _duck_env[:len(eff)]
            return float(eff.max())

        kick_pk = _panned_pk("kick")
        # THE KICK IS THE ANCHOR (owner 2026-09-02, after checking his rules
        # against how hip-hop is normally mixed). This used to be
        # `min(kick_pk, snare_pk)` — measure everything against the QUIETER
        # of the kick and the lane spelled "snare" — and it is the single
        # line that made a level accident anywhere in the beat able to drag
        # the whole mix down with it. Every producer reference anchors to
        # the kick and mixes relative to that; nothing anchors to whichever
        # of two elements happens to be quietest.
        #
        # What it cost, measured inside this function on 2164 before the
        # ceiling ran: kick -2.1, clap -0.9, snare -20.6. On 7 of the 13
        # identities that carry both lanes the snare is a THIN LAYER TUCKED
        # UNDER THE CLAP (Kane East, Sunday Chop, Swish Beatz, Baltimore
        # Club, Miami Bass, Plug and Crunk all set snare 0.5-0.7 against clap
        # 0.78-0.92) — so the reference came out as that -20.6 support layer,
        # and the beat's actual backbeat was cut by 26.6 dB, the hat by 24.1
        # and the bells by 20.9. A kick with faint tapping behind it.
        #
        # His rule that colour sits under the backbeat as well as the kick is
        # not lost with the `min` — it is now carried by the governor above,
        # which pins the backbeat bus near the kick instead of letting it
        # land anywhere. The one case that rule can still miss is a backbeat
        # so quiet the governor's boost clamp cannot reach it; that is a
        # broken sample, not a mix balance, and it is logged rather than
        # papered over.
        ref_pk = kick_pk
        # ...and the backbeat gets a peak ceiling, which it never had. Both
        # backbone lanes return None from peak_ceiling_for, so the snare's
        # peak was measured against nothing at all. See BACKBEAT_OVER_KICK_DB.
        # Applied to EVERY lane of the snare/clap family, not just whichever
        # is loudest here. Capping only the loudest leaked: on 2162 the clap
        # was the loudest at this point and got pulled to +2, then the loop
        # below pulled it again to -3 as a clap, which left the untouched
        # snare underneath as the beat's loudest backbeat lane at +5.4 over
        # the kick. Per-lane is also simply what the rule says — no part of
        # the backbeat peaks more than this over the kick — and the clap
        # still takes its own -3 ceiling in the loop below on top.
        if kick_pk > 0:
            b_cap = kick_pk * 10 ** (BACKBEAT_OVER_KICK_DB / 20)
            for ln in [l for l in bufs
                       if any(l.startswith(sl) for sl in SNARE_LIKE)]:
                b_pk = _panned_pk(ln)
                if b_pk > b_cap:
                    bufs[ln] = bufs[ln] * (b_cap / b_pk)
                    if ln in wet_side:
                        wet_side[ln] = wet_side[ln] * (b_cap / b_pk)
        if ref_pk > 0:
            for ln in bufs:
                head = peak_ceiling_for(ln)
                if head is None:          # kick, snare, and the low end
                    continue
                # Measure the DRY LANE PLUS ITS REVERB TAIL. The cap used to
                # read bufs[ln] alone, but wet_side[ln] is folded in later at
                # pan time, so the file he actually gets was louder than the
                # number here promised: owner reported the shaker on beat
                # 1763 as too loud and it measured -1.6 dB against a -3.0 cap.
                # Elementwise |dry| + |wet| is the worst case the panned stem
                # can reach, so capping on that is the figure that holds in
                # the stem rather than only inside this function.
                pk = _panned_pk(ln)
                cap = ref_pk * 10 ** (head / 20.0)
                if pk > cap > 0:
                    bufs[ln] = bufs[ln] * (cap / pk)
                    w = wet_side.get(ln)
                    if w is not None:
                        wet_side[ln] = w * (cap / pk)


    # stems: each lane panned to stereo with its space treatment, kick
    # character, and the duck baked in (duck is a plain envelope multiply,
    # so per-lane ducking sums to exactly the mix-bus duck)
    stems = {}
    if want_parts:
        for lane, (pan, *_rest) in p["lanes"].items():
            gl = np.cos((pan + 1) * np.pi / 4)
            gr = np.sin((pan + 1) * np.pi / 4)
            sL, sR = bufs[lane] * gl, bufs[lane] * gr
            sd = wet_side.get(lane)
            if sd is not None:
                sL, sR = sL + sd, sR - sd
            # Owner call 2026-07-22: "have the kick gate the bass and
            # other instruments". The tuned root sub used to ride the
            # un-ducked path WITH the kick; now only the kick itself
            # stays out of its own duck, so the sub, the harmony bass
            # and the chord pads all breathe around it.
            if p["sidechain"] > 0 and lane != "kick" \
                    and onsets.get("kick"):
                sL, sR = duck(sL, sR, onsets["kick"], depth=p["sidechain"],
                              loop=True)
            stems[lane] = (sL, sR)

    # stereo mix, kick kept aside so the duck breathes around it
    oL, oR = np.zeros(end), np.zeros(end)
    kL, kR = np.zeros(end), np.zeros(end)
    for lane, (pan, *_rest) in p["lanes"].items():
        gl = np.cos((pan + 1) * np.pi / 4)
        gr = np.sin((pan + 1) * np.pi / 4)
        sd = wet_side.get(lane)
        if lane == "kick":       # only the kick sits outside its own duck
            kL += bufs[lane] * gl
            kR += bufs[lane] * gr
            if sd is not None:
                kL, kR = kL + sd, kR - sd
        else:
            oL += bufs[lane] * gl
            oR += bufs[lane] * gr
            if sd is not None:
                oL, oR = oL + sd, oR - sd
    if p["sidechain"] > 0 and onsets.get("kick"):
        oL, oR = duck(oL, oR, onsets["kick"], depth=p["sidechain"],
                      loop=True)
    L, R = kL + oL, kR + oR

    if not clean and p["vinyl"]:
        L = L + vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 1)
        R = R + vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 2)
    if not clean and p["wow"] > 0:
        L = wow_flutter(L, wow_pct=p["wow"], seed=p["num"], loop=True)
        R = wow_flutter(R, wow_pct=p["wow"], seed=p["num"], loop=True)
    if not clean and p["mix_sat"] > 0:
        L, R = sat_unity(L, p["mix_sat"]), sat_unity(R, p["mix_sat"])
    if not clean and p["dust"] > 0:
        L, R = sp1200(L, amount=p["dust"]), sp1200(R, amount=p["dust"])

    # bus glue compression (owner 2026-07-29) runs BEFORE master() — glue
    # the mix's dynamics first, then tone/saturate/limit it. Always on,
    # clean render or not: this is mix glue, not the SP-1200/wow/vinyl
    # "dirt" clean_renders turns off.
    L, R = glue_compress(L, R)
    # clean master: drive 0.7 keeps the tanh glue essentially linear —
    # tone EQ and mono-bass still apply, saturation effectively doesn't
    L, R = master(L, R, drive=0.7 if clean else p["drive"])
    # CENTRE THE BASS LAST (owner 2026-09-02, "take it"). This used to run
    # BEFORE master_to_lufs, and master_to_lufs soft-clips L and R
    # separately — running a non-linear stage on two channels that differ
    # regenerates side energy underneath the crossover, so the low end was
    # only mono until the very next thing that happened to it. Widening the
    # mix always leaked a little back; the backbeat governor added enough
    # level to push it over the project's own limit (Farrow/dry measured
    # 0.056 against the 0.05 line, and Wonky/room and Acid Rap Detroit/room
    # were already breaching it before any of this work).
    #
    # Measured cost on four real beats, which is why this is free rather
    # than a trade: low-end side energy 0.006-0.013 -> 0.0000-0.0001, peak
    # moves at most 0.05 dB, loudness 0.00 dB. `got` is still the honest
    # figure for the file — the re-measured LUFS after this line matches it
    # to two decimal places. (On the synthetic test kit the peak moves up to
    # 0.85 dB, because a pure sine has no crest factor to hide the filter's
    # ringing. Real drums do.)
    L, R, got = master_to_lufs(L, R)
    L, R = mono_below(L, R, 120)
    if not want_parts:
        return L, R, got

    # finish the stems: the vinyl bed becomes its own stem, wow and dust
    # (the character-defining colors) print per lane, and one shared gain
    # sets the loudest stem to -6 dBFS so the balance between stems
    # survives and the summed set keeps headroom in Reason.
    # Mix-bus glue (mix_sat, master drive, LUFS) stays off the stems —
    # they're for editing in Reason 12; the WAV is the glued reference.
    if not clean and p["vinyl"]:
        stems["vinyl"] = (
            vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 1),
            vinyl_bed(end, level_db=p["vinyl"], seed=p["num"] * 2 + 2))
    for lane, (sL, sR) in list(stems.items()):
        if not clean and lane != "vinyl":
            if p["wow"] > 0:
                sL = wow_flutter(sL, wow_pct=p["wow"], seed=p["num"],
                                 loop=True)
                sR = wow_flutter(sR, wow_pct=p["wow"], seed=p["num"],
                                 loop=True)
            if p["dust"] > 0:
                sL = sp1200(sL, amount=p["dust"])
                sR = sp1200(sR, amount=p["dust"])
        stems[lane] = (sL, sR)
    peak = max(max(np.abs(sL).max(), np.abs(sR).max())
               for sL, sR in stems.values())
    if peak > 0:
        # 0.5 = -6 dBFS on the loudest stem; was 0.9, which summed to a
        # redlining channel the moment the stems landed in Reason
        stems = {ln: (sL * 0.5 / peak, sR * 0.5 / peak)
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
            want = bars_of(p) * 240.0 / p["bpm"]
            rms = 20 * np.log10(np.sqrt(0.5 * (L**2 + R**2).mean()) + 1e-12)
            # LUFS is the loudness truth; plain RMS runs low on spacious
            # halftime styles (drop-out bars average in), so its floor is soft
            good = abs(dur - want) < 0.02 and -18 < rms < -9 \
                and abs(got - OWNER_TASTE["master_lufs"]) < 2.0
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
