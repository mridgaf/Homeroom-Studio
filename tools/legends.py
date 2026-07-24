"""The Legends — a second roster (owner request 2026-07-18).

Twelve producers modeled DIRECTLY on real signatures, under sound-alike
names. Unlike the nine crew characters (v6 loosening: variety over style
fidelity), the Legends' whole point is LIKENESS — every beat should sound
like the producer it's built on. Their rules:

- They follow the crew's INSTRUMENT SOUND VARIATION rules only: fresh
  sample picks per beat, the cross-session anti-repetition history, per-
  beat kick sustain ranges, subtle varied-side timekeeper panning, and
  one locked stamp each. (Open-soundbank mode applies to them too — it
  is a sound-variation rule of the first set.)
- Everything else is NEW rules for likeness (enforced in pattern_gen /
  beat_machine via the "legend": True flag):
  * grammar weights stay heavily HOME — no v6 flat menus;
  * kick banks never cross-pollinate INTO a legend (the loose nine may
    still borrow a legend's book);
  * swing stays within +/-2 of the signature feel, no outliers;
  * no random 3/4 / 6/8 / exotic-grid rolls (the notes box can still
    ask for one — his click, his call);
  * no engine-driven evolution: a legend's career is already written.
- They live in their OWN box on the Beat Machine page and can collab
  with anyone — mixed collabs use the loose crew rules (collaborating
  IS stepping out of character).

Roster config: legends_config.json at the project root, auto-written
from LEGENDS_DEFAULT on first run, editable ever after (same contract as
crew_config.json; delete it to regenerate). Style keys re-sync on a
LEGENDS_VERSION bump unless "_style_lock" is set.
"""
import json
import os
from pathlib import Path

from pattern_gen import KICK_BANK

# REASON_VOICE_LEGENDS_CONFIG (2026-07-22): the same candidate-file hook
# crew.py has had since the autoresearch loop — point the engine at a
# tuned COPY so a batch can be auditioned without the live roster ever
# moving. Unset = the real legends_config.json.
CONFIG = Path(os.environ.get("REASON_VOICE_LEGENDS_CONFIG")
              or Path(__file__).resolve().parent.parent
              / "legends_config.json")
LEGENDS_VERSION = 1

R16 = "-" * 16
_BK = ["----X-------X---"] * 8            # plain 2&4 placeholder; compose
_H8 = ["x-x-x-x-x-x-x-x-"] * 8           # rewrites these every render


def _stamp_tail(hit="--------------x-"):
    return [R16] * 3 + [hit] + [R16] * 3 + [hit]


LEGENDS_DEFAULT = {
    # ------------------------------------------------ The Neptunes lane
    "Farrow": dict(
        num=10, bpm=98, era="legend", built="Pharrell / The Neptunes",
        legend=True,
        listen=("skeletal funk minimalism: dry punchy kick syncopation, "
                "snare with the clap landing ~18 ms late (the flam), a "
                "snap keeping time instead of hats, weird clean colors, "
                "bone dry everywhere"),
        kit=dict(
            kick=("kick", None, ["clean", "tight", "punch", "pop"],
                  (0.12, 0.4)),
            snare=("snare", None, ["clean", "rim", "snap"], 1.0),
            clap=("clap", None, ["clap"], 1.0),
            snap=("snap", None, ["snap", "finger"], 0.5),
            stamp=("fx", None, ["click", "zap", "glitch", "laser"], 0.6),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 1001), _BK),
            snare=(0.0, 0.85, (0, 1, 50, 1002), _BK),
            clap=(0.1, 0.5, (+18, 1, 50, 1003), _BK),
            snap=(0.14, 0.4, (0, 1, 50, 1004), _H8),
            stamp=(-0.3, 0.38, (0, 1, 50, 1005), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.15,
        space=("dry", ["snare"]), alt=None,
        drive=1.4, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 6, 1, 1, 5, 2, 4, 1, 5, 4, 1, 2, 3, 2],
                      hits=[3, 6], double_p=0.45),
            snare=dict(modes=[["backbeat", 0.8], ["displaced", 0.1],
                              ["sparse", 0.1]],
                       ghosts=[0, 1], gcells=[3, 7, 11, 15]),
            clap=dict(copy="snare"),          # the documented late flam
            snap=dict(modes=[["offbeats", 0.35], ["sparse", 0.25],
                             ["answer", 0.2], ["eighths", 0.2]]),
        ),
        kick_flavors=[[0.1, "808", ["clean"], [0.25, 0.5]],
                      [0.9, None, ["clean", "tight", "pop", "punch"],
                       [0.1, 0.35]]],
        library=dict(p=0.4, tags=[["rnb", 3], ["funk", 3],
                                   ["minimal", 2]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["fx", ["zap", "laser", "glitch"], "blips"],
            ["perc", ["block", "clave", "tabla"], "woods"]]),
    ),
    # ------------------------------------------------- West Coast lane
    "Doc Day": dict(
        num=11, bpm=93, era="legend", built="Dr. Dre", legend=True,
        legend_swing=50,
        listen=("surgical West Coast: heavy punchy kick, a crisp hard "
                "snare that NEVER leaves 2 and 4, straight-eighth hats, "
                "tambourine and cowbell color, sparse disciplined "
                "arrangement with an occasional deep sub"),
        kit=dict(
            kick=("kick", None, ["punch", "knock", "deep"], (0.2, 0.5)),
            snare=("snare", None, ["crack", "tight", "hard"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.5),
            perc=("perc", None, ["tamb", "shaker"], 1.0),
            stamp=("fx", None, ["scratch", "vocal", "yeah"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 1011), _BK),
            snare=(0.0, 0.88, (0, 1, 50, 1012), _BK),
            hat=(-0.12, 0.38, (0, 1, 50, 1013), _H8),
            perc=(0.16, 0.3, (0, 2, 50, 1014), _H8),
            stamp=(-0.28, 0.4, (0, 1, 50, 1015), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.2,
        space=("gated", ["snare"]), alt=None,
        drive=1.45, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 4, 2, 1, 4, 5, 2, 1, 5, 2, 2, 3, 3, 1],
                      hits=[3, 6], double_p=0.3),
            snare=dict(modes=[["backbeat", 0.9], ["sparse", 0.1]],
                       ghosts=[0, 1], gcells=[7, 15]),
            hat=dict(modes=[["eighths", 0.5], ["sixteenths", 0.15],
                            ["offbeats", 0.15], ["sparse", 0.2]],
                     open_p=0.06),
            perc=dict(modes=[["offbeats", 0.5], ["sparse", 0.3],
                             ["eighths", 0.2]]),
        ),
        kick_flavors=[[0.25, "808", ["deep", "sub"], [0.5, 1.1]],
                      [0.75, None, ["punch", "knock", "deep"],
                       [0.2, 0.5]]],
        library=dict(p=0.45, tags=[["funk", 3], ["boom-bap", 2],
                                  ["rnb", 2]]),
        extras=dict(p=0.6, nmax=1, pool=[
            ["perc", ["cowbell", "block"], "bells"],
            ["perc", ["shaker", "tamb"], "shaker"],
            ["rim", ["rim", "stick"], "rims"]]),
    ),
    # ------------------------------------------------- soul-chop lane
    "Kane East": dict(
        num=12, bpm=90, era="legend", built="Kanye West", legend=True,
        listen=("chipmunk-soul era: driving pushed kicks, a BIG clap "
                "with the snare tucked underneath, 57% gospel bounce, "
                "tambourine offbeats, warm light dust and a vinyl bed"),
        kit=dict(
            kick=("kick", None, ["punch", "warm", "boom"], (0.2, 0.55)),
            clap=("clap", None, ["big", "clap"], 1.0),
            snare=("snare", None, ["snare"], 1.0),
            hat=("hat", None, ["closed"], 0.5),
            perc=("perc", None, ["tamb", "shaker"], 1.0),
            stamp=("fx", None, ["reverse", "vocal", "soul"], 1.4),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 57, 1021), _BK),
            clap=(0.0, 0.9, (0, 2, 57, 1022), _BK),
            snare=(0.0, 0.5, (0, 2, 57, 1023), _BK),
            hat=(0.12, 0.4, (0, 2, 57, 1024), _H8),
            perc=(-0.2, 0.3, (0, 3, 57, 1025), _H8),
            stamp=(-0.3, 0.4, (0, 2, 57, 1026), _stamp_tail()),
        ),
        dust=0.35, vinyl=-44, wow=0.0, sidechain=0.2,
        space=("gated", ["clap"]), alt=None,
        drive=1.4, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 2, 5, 1, 2, 5, 8, 1, 2, 2, 5, 1, 3, 3],
                      hits=[3, 7], double_p=0.35),
            clap=dict(modes=[["backbeat", 0.85], ["displaced", 0.1],
                             ["sparse", 0.05]],
                      ghosts=[0, 2], gcells=[2, 3, 6, 7, 10, 11, 14, 15]),
            snare=dict(copy="clap"),          # tucked under the big clap
            hat=dict(modes=[["eighths", 0.45], ["sparse", 0.2],
                            ["offbeats", 0.2], ["sixteenths", 0.15]],
                     open_p=0.08),
            perc=dict(modes=[["offbeats", 0.6], ["sparse", 0.4]]),
        ),
        kick_flavors=[[0.3, "808", ["boom", "deep"], [0.35, 0.8]],
                      [0.7, None, ["punch", "warm", "boom"],
                       [0.18, 0.5]]],
        library=dict(p=0.5, tags=[["soul", 4], ["motown", 2],
                                   ["boom-bap", 2], ["funk", 1]]),
        extras=dict(p=0.6, nmax=1, pool=[
            ["perc", ["tamb", "shaker"], "shaker"],
            ["crash", ["crash"], "crash2"],
            ["fx", ["reverse", "impact"], "swellfx"]]),
    ),
    # ------------------------------------------------- the drunk lane
    "J Dillo": dict(
        num=13, bpm=88, era="legend", built="J Dilla", legend=True,
        listen=("the drunk pull, faithful: snare rushes ~20 ms early, "
                "kick drags ~12 ms behind, hats dead straight, loose "
                "wobbly jitter, dusty drums, vinyl and a touch of wow"),
        kit=dict(
            kick=("kick", None, ["dust", "boom", "dirty"], (0.35, 0.9)),
            snare=("snare", None, ["vinyl", "dusty", "lofi"], 1.0),
            hat=("hat", None, ["closed", "vintage"], 0.5),
            stamp=("fx", None, ["vinyl", "reverse", "foley"], 1.0),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (+12, 4, 50, 1031), _BK),
            snare=(0.0, 0.88, (-20, 4, 50, 1032), _BK),
            hat=(-0.14, 0.36, (0, 2, 50, 1033), _H8),
            stamp=(-0.32, 0.4, (0, 3, 50, 1034), _stamp_tail()),
        ),
        dust=0.5, vinyl=-42, wow=0.15, sidechain=0.15,
        space=("gated", ["snare"]), alt=("room", (0.45, 3500, 0.32)),
        drive=1.35, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 3, 2, 3, 2, 2, 4, 6, 2, 2, 5, 3, 2, 4, 5, 3],
                      hits=[2, 6], double_p=0.4),
            snare=dict(modes=[["backbeat", 0.75], ["displaced", 0.15],
                              ["sparse", 0.1]],
                       ghosts=[0, 3],
                       gcells=[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]),
            hat=dict(modes=[["eighths", 0.4], ["sixteenths", 0.3],
                            ["broken", 0.2], ["sparse", 0.1]],
                     open_p=0.1),
        ),
        kick_flavors=[[0.45, "808", ["dust", "boom", "dirty"],
                       [0.35, 0.9]],
                      [0.55, None, ["boom", "break", "knock"],
                       [0.18, 0.5]]],
        library=dict(p=0.5, tags=[["lofi", 3], ["neo-soul", 3],
                                   ["boom-bap", 2], ["soul", 2]]),
        extras=dict(p=0.6, nmax=1, pool=[
            ["fx", ["vinyl", "reverse", "foley"], "foundfx"],
            ["perc", ["shaker", "tamb"], "shaker"],
            ["perc", ["tom"], "toms"]]),
    ),
    # ------------------------------------------------- ratchet lane
    "Mustang": dict(
        num=14, bpm=100, era="legend", built="DJ Mustard", legend=True,
        listen=("ratchet club bounce: a sparse 808 kick that lands on "
                "the and-of-two pocket, dry claps on 2 and 4, layered "
                "snaps, minimal offbeat hats, clean digital, room for "
                "the chant"),
        kit=dict(
            kick=("kick", None, ["deep", "sub", "clean"], (0.3, 0.9)),
            clap=("clap", None, ["clap"], 1.0),
            snap=("snap", None, ["snap", "finger"], 0.5),
            hat=("hat", None, ["closed", "tight"], 0.5),
            stamp=("fx", None, ["hey", "vocal", "chant", "yeah"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 1041), _BK),
            clap=(0.0, 0.86, (0, 1, 50, 1042), _BK),
            snap=(0.16, 0.4, (0, 1, 50, 1043), _H8),
            hat=(-0.12, 0.36, (0, 1, 50, 1044), _H8),
            stamp=(0.3, 0.42, (0, 1, 50, 1045), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.25,
        space=("dry", ["clap"]), alt=None,
        drive=1.45, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 6, 1, 1, 4, 1, 2, 1, 6, 1, 1, 4, 2, 1],
                      hits=[2, 5], double_p=0.2),
            clap=dict(modes=[["backbeat", 0.9], ["sparse", 0.1]],
                      ghosts=[0, 0], gcells=[]),
            snap=dict(modes=[["offbeats", 0.4], ["sparse", 0.3],
                             ["answer", 0.3]]),
            hat=dict(modes=[["offbeats", 0.4], ["eighths", 0.3],
                            ["sparse", 0.3]], open_p=0.04),
        ),
        kick_flavors=[[0.6, "808", ["deep", "sub"], [0.4, 1.0]],
                      [0.4, None, ["clean", "tight", "punch"],
                       [0.15, 0.4]]],
        library=dict(p=0.45, tags=[["rnb", 2], ["trap", 2], ["house", 2],
                                  ["electro", 1]]),
        extras=dict(p=0.45, nmax=1, pool=[
            ["perc", ["block", "cowbell"], "bells"],
            ["fx", ["zap", "glitch"], "blips"]]),
    ),
    # ------------------------------------------------- anthem lane
    "Swish Beatz": dict(
        num=15, bpm=95, era="legend", built="Swizz Beatz", legend=True,
        listen=("marching-band anthem stomp: big simple kick stomps, a "
                "harsh clap-snare stack, sparse shouting hats, siren and "
                "horn color, zero subtlety and proud of it"),
        kit=dict(
            kick=("kick", None, ["hard", "punch", "knock"], (0.2, 0.6)),
            clap=("clap", None, ["big", "clap"], 1.0),
            snare=("snare", None, ["hard", "crack"], 1.0),
            hat=("hat", None, ["closed"], 0.5),
            stamp=("fx", None, ["siren", "horn", "shout", "vocal"], 1.2),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 1051), _BK),
            clap=(0.0, 0.9, (0, 1, 50, 1052), _BK),
            snare=(0.0, 0.5, (0, 1, 50, 1053), _BK),
            hat=(0.14, 0.38, (0, 1, 50, 1054), _H8),
            stamp=(-0.3, 0.44, (0, 1, 50, 1055), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.2,
        space=("gated", ["clap"]), alt=None,
        drive=1.5, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 2, 6, 1, 2, 2, 8, 1, 1, 2, 6, 1, 2, 2],
                      hits=[3, 6], double_p=0.2),
            clap=dict(modes=[["backbeat", 0.85], ["halftime", 0.1],
                             ["sparse", 0.05]],
                      ghosts=[0, 1], gcells=[6, 7, 14, 15]),
            snare=dict(copy="clap"),
            hat=dict(modes=[["sparse", 0.3], ["eighths", 0.3],
                            ["offbeats", 0.25], ["answer", 0.15]]),
        ),
        kick_flavors=[[0.35, "808", ["hard", "deep"], [0.3, 0.8]],
                      [0.65, None, ["hard", "punch", "knock"],
                       [0.15, 0.5]]],
        library=dict(p=0.4, tags=[["electro", 2], ["trap", 2],
                                   ["funk", 1], ["boom-bap", 1]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["crash", ["crash", "impact"], "impacts"],
            ["perc", ["cowbell", "block"], "bells"]]),
    ),
    # ------------------------------------------------- surgical lane
    "DJ Premium": dict(
        num=16, bpm=93, era="legend", built="DJ Premier", legend=True,
        legend_swing=53,
        listen=("surgical boom bap at a locked 53% swing: tight punchy "
                "kick, cracking snare with real ghost notes, dead-steady "
                "eighth hats, scratch-stab color, moderate dust"),
        kit=dict(
            kick=("kick", None, ["punch", "hard", "knock"], (0.2, 0.5)),
            snare=("snare", None, ["crack", "tight", "hard"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.5),
            stamp=("fx", None, ["scratch"], 0.8),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1.5, 53, 1061), _BK),
            snare=(0.0, 0.88, (0, 1.5, 53, 1062), _BK),
            hat=(0.12, 0.38, (0, 1.5, 53, 1063), _H8),
            stamp=(-0.3, 0.42, (0, 2, 50, 1064), _stamp_tail()),
        ),
        dust=0.4, vinyl=-44, wow=0.0, sidechain=0.15,
        space=("gated", ["snare"]), alt=("room", (0.4, 3800, 0.25)),
        drive=1.4, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 5, 2, 1, 3, 2, 2, 1, 5, 2, 1, 5, 2, 2],
                      hits=[2, 5], double_p=0.25),
            snare=dict(modes=[["backbeat", 0.9], ["displaced", 0.05],
                              ["sparse", 0.05]],
                       ghosts=[1, 3],
                       gcells=[2, 3, 5, 6, 7, 9, 10, 13, 14, 15]),
            hat=dict(modes=[["eighths", 0.6], ["sixteenths", 0.2],
                            ["sparse", 0.2]], open_p=0.05),
        ),
        kick_flavors=[[0.25, "808", ["punch", "hard"], [0.3, 0.7]],
                      [0.75, None, ["punch", "knock", "hard"],
                       [0.15, 0.45]]],
        library=dict(p=0.45, tags=[["boom-bap", 4], ["funk", 2],
                                  ["soul", 1]]),
        extras=dict(p=0.55, nmax=1, pool=[
            ["fx", ["scratch"], "cutfx"],
            ["rim", ["rim", "stick"], "rims"]]),
    ),
    # ------------------------------------------------- stutter lane
    "Timberline": dict(
        num=17, bpm=100, era="legend", built="Timbaland", legend=True,
        listen=("beatbox stutter-funk: double-hit syncopated kicks, a "
                "clap that answers instead of insists, tabla and exotic "
                "perc off-center, silence used as an instrument, "
                "completely clean"),
        kit=dict(
            kick=("kick", None, ["clean", "punch", "tight"], (0.15, 0.4)),
            clap=("clap", None, ["clap"], 1.0),
            perc=("perc", None, ["tabla", "shaker", "conga"], 0.9),
            snap=("snap", None, ["snap", "finger"], 0.5),
            stamp=("perc", None, ["block", "tabla", "cowbell"], 0.6),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 1071), _BK),
            clap=(0.0, 0.85, (0, 1, 50, 1072), _BK),
            perc=(-0.3, 0.32, (0, 2, 50, 1073), _H8),
            snap=(0.18, 0.4, (0, 1, 50, 1074), _H8),
            stamp=(0.28, 0.4, (0, 1, 50, 1075), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.2,
        space=("gated", ["clap"]), alt=None,
        drive=1.45, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 6, 1, 1, 5, 2, 3, 1, 3, 5, 1, 3, 3, 2],
                      hits=[3, 7], double_p=0.55),
            clap=dict(modes=[["backbeat", 0.7], ["displaced", 0.2],
                             ["sparse", 0.1]],
                      ghosts=[0, 2], gcells=[2, 3, 6, 7, 10, 11, 14, 15]),
            perc=dict(euclid=[3, 5, 7]),
            snap=dict(modes=[["answer", 0.3], ["offbeats", 0.3],
                             ["sparse", 0.2], ["eighths", 0.2]]),
        ),
        kick_flavors=[[0.2, "808", ["clean", "tight"], [0.3, 0.7]],
                      [0.8, None, ["clean", "punch", "tight", "pop"],
                       [0.12, 0.4]]],
        library=dict(p=0.45, tags=[["rnb", 3], ["garage", 2],
                                  ["electro", 2], ["funk", 1]]),
        extras=dict(p=0.6, nmax=1, pool=[
            ["perc", ["tabla", "block", "cowbell"], "exotic2"],
            ["fx", ["zap", "laser", "glitch"], "blips"],
            ["rim", ["rim", "click"], "clicks"]]),
    ),
    # ------------------------------------------------- triumphant lane
    "Just Flame": dict(
        num=18, bpm=94, era="legend", built="Just Blaze", legend=True,
        legend_swing=54,
        listen=("triumphant soul bombast: pounding driving kicks, a huge "
                "snare-clap stack, busy driving hats, crash swells, the "
                "whole beat leaning forward like a parade"),
        kit=dict(
            kick=("kick", None, ["punch", "hard", "boom"], (0.2, 0.55)),
            snare=("snare", None, ["big", "crack", "hard"], 1.0),
            clap=("clap", None, ["big", "clap"], 1.0),
            hat=("hat", None, ["closed"], 0.5),
            stamp=("crash", None, ["crash", "swell"], 2.5),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 54, 1081), _BK),
            snare=(0.0, 0.85, (0, 2, 54, 1082), _BK),
            clap=(0.1, 0.5, (0, 2, 54, 1083), _BK),
            hat=(-0.12, 0.4, (0, 2, 54, 1084), _H8),
            stamp=(0.0, 0.42, (0, 2, 50, 1085),
                   ["X---------------"] + [R16] * 3
                   + ["X---------------"] + [R16] * 3),
        ),
        dust=0.25, vinyl=-46, wow=0.0, sidechain=0.2,
        space=("gated", ["snare"]), alt=None,
        drive=1.5, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 3, 4, 1, 3, 6, 3, 1, 4, 2, 4, 2, 4, 3],
                      hits=[4, 8], double_p=0.4),
            snare=dict(modes=[["backbeat", 0.85], ["displaced", 0.1],
                              ["sparse", 0.05]],
                       ghosts=[0, 2], gcells=[2, 3, 6, 7, 10, 11, 14, 15],
                       burst_p=0.25),
            clap=dict(copy="snare"),
            hat=dict(modes=[["eighths", 0.4], ["sixteenths", 0.35],
                            ["broken", 0.15], ["gallop", 0.1]],
                     open_p=0.08),
        ),
        kick_flavors=[[0.3, "808", ["boom", "deep"], [0.3, 0.8]],
                      [0.7, None, ["punch", "hard", "boom"],
                       [0.18, 0.5]]],
        library=dict(p=0.5, tags=[["soul", 4], ["funk", 2],
                                   ["boom-bap", 2], ["motown", 1]]),
        extras=dict(p=0.6, nmax=1, pool=[
            ["crash", ["crash"], "crash2"],
            ["perc", ["tamb", "shaker"], "shaker"],
            ["fx", ["reverse", "impact"], "swellfx"]]),
    ),
    # ------------------------------------------------- grimy lane
    "Razor": dict(
        num=19, bpm=87, era="legend", built="RZA", legend=True,
        legend_swing=52,
        listen=("grimy and raw: off-kilter muddy boom kicks, a cracking "
                "harsh snare, loose hand-played timing (the widest "
                "jitter on the roster), sparse dusty arrangement, the "
                "heaviest vinyl bed and a warp of wow"),
        kit=dict(
            kick=("kick", None, ["boom", "dirty", "dust"], (0.3, 0.8)),
            snare=("snare", None, ["crack", "dusty", "hard"], 1.0),
            hat=("hat", None, ["closed", "vintage"], 0.5),
            stamp=("fx", None, ["clang", "metal", "gong", "sword"], 1.2),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (+6, 6, 52, 1091), _BK),
            snare=(0.0, 0.88, (-6, 6, 52, 1092), _BK),
            hat=(-0.14, 0.34, (0, 5, 52, 1093), _H8),
            stamp=(-0.3, 0.42, (0, 4, 50, 1094), _stamp_tail()),
        ),
        dust=0.6, vinyl=-38, wow=0.2, sidechain=0.1,
        space=("gated", ["snare"]), alt=("room", (0.5, 3200, 0.3)),
        drive=1.35, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 2, 3, 2, 2, 3, 4, 3, 2, 3, 4, 2, 2, 3, 3, 4],
                      hits=[2, 5], double_p=0.3),
            snare=dict(modes=[["backbeat", 0.6], ["displaced", 0.25],
                              ["sparse", 0.15]],
                       ghosts=[0, 2],
                       gcells=[1, 3, 5, 7, 9, 11, 13, 15]),
            hat=dict(modes=[["sparse", 0.35], ["broken", 0.25],
                            ["eighths", 0.25], ["answer", 0.15]],
                     open_p=0.05),
        ),
        kick_flavors=[[0.35, "808", ["boom", "dirty"], [0.3, 0.8]],
                      [0.65, None, ["boom", "dirty", "dust", "break"],
                       [0.18, 0.5]]],
        library=dict(p=0.45, tags=[["boom-bap", 3], ["lofi", 2],
                                  ["soul", 2]]),
        extras=dict(p=0.55, nmax=1, pool=[
            ["fx", ["vinyl", "reverse", "foley"], "foundfx"],
            ["perc", ["tom"], "toms"],
            ["perc", ["block", "clave"], "woods"]]),
    ),
    # ------------------------------------------------- hybrid lane
    "Hitt Kid": dict(
        num=20, bpm=96, era="legend", built="Hit-Boy", legend=True,
        listen=("the modern hybrid: hard punchy kicks trading with mid-"
                "length 808s, a crisp clap-snare stack, hats that break "
                "into rolls, halftime and backbeat both in the bag, "
                "clean and huge"),
        kit=dict(
            kick=("kick", None, ["punch", "hard", "knock"], (0.25, 0.7)),
            snare=("snare", None, ["crack", "clean", "trap"], 1.0),
            clap=("clap", None, ["clap"], 1.0),
            hat=("hat", None, ["trap", "closed", "tight"], 0.5),
            stamp=("fx", None, ["impact", "reverse", "riser"], 1.4),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 1101), _BK),
            snare=(0.0, 0.85, (0, 1, 50, 1102), _BK),
            clap=(0.1, 0.5, (0, 1, 50, 1103), _BK),
            hat=(0.12, 0.38, (0, 1, 50, 1104), _H8),
            stamp=(-0.28, 0.42, (0, 1, 50, 1105), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.25,
        space=("gated", ["snare"]), alt=None,
        drive=1.45, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 5, 1, 1, 5, 2, 4, 1, 3, 3, 1, 3, 2, 2],
                      hits=[3, 6], double_p=0.4),
            snare=dict(modes=[["backbeat", 0.55], ["halftime", 0.3],
                              ["displaced", 0.15]],
                       ghosts=[0, 1], gcells=[6, 7, 14, 15]),
            clap=dict(copy="snare"),
            hat=dict(modes=[["sixteenths", 0.3], ["eighths", 0.25],
                            ["rolls32", 0.2], ["broken", 0.15],
                            ["offbeats", 0.1]], roll_n=[1, 2]),
        ),
        kick_flavors=[[0.45, "808", ["deep", "punch"], [0.35, 0.9]],
                      [0.55, None, ["punch", "hard", "knock"],
                       [0.18, 0.5]]],
        library=dict(p=0.5, tags=[["trap", 3], ["boom-bap", 2],
                                   ["drill", 1], ["rnb", 1]]),
        extras=dict(p=0.55, nmax=1, pool=[
            ["fx", ["riser", "reverse", "sweep"], "risers"],
            ["rim", ["rim", "click"], "clicks"]]),
    ),
    # ------------------------------------------------- refined lane
    "No Alias": dict(
        num=21, bpm=92, era="legend", built="No I.D.", legend=True,
        legend_swing=54,
        listen=("Chicago soulful boom bap: a deep rounded kick sitting "
                "far back in the pocket, a warm solid snare on 2 and 4, "
                "restrained hats, light dust — refinement over flash"),
        kit=dict(
            kick=("kick", None, ["warm", "deep", "boom"], (0.25, 0.6)),
            snare=("snare", None, ["warm", "dusty", "vintage"], 1.0),
            hat=("hat", None, ["closed"], 0.5),
            stamp=("perc", None, ["conga", "bongo", "slap"], 0.8),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (+4, 2, 54, 1111), _BK),
            snare=(0.0, 0.85, (0, 2, 54, 1112), _BK),
            hat=(0.1, 0.36, (0, 2, 54, 1113), _H8),
            stamp=(-0.28, 0.38, (0, 3, 54, 1114), _stamp_tail()),
        ),
        dust=0.3, vinyl=-46, wow=0.0, sidechain=0.15,
        space=("gated", ["snare"]), alt=None,
        drive=1.4, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 3, 2, 1, 5, 3, 2, 1, 5, 2, 2, 3, 3, 2],
                      hits=[2, 5], double_p=0.25),
            snare=dict(modes=[["backbeat", 0.85], ["sparse", 0.1],
                              ["displaced", 0.05]],
                       ghosts=[0, 2], gcells=[3, 6, 7, 11, 14, 15]),
            hat=dict(modes=[["eighths", 0.45], ["sparse", 0.25],
                            ["sixteenths", 0.2], ["offbeats", 0.1]],
                     open_p=0.06),
        ),
        kick_flavors=[[0.3, "808", ["warm", "deep"], [0.35, 0.8]],
                      [0.7, None, ["warm", "boom", "punch"],
                       [0.18, 0.5]]],
        library=dict(p=0.45, tags=[["soul", 3], ["boom-bap", 3],
                                  ["motown", 2], ["neo-soul", 1]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["perc", ["shaker", "tamb"], "shaker"],
            ["perc", ["conga", "bongo"], "congas2"],
            ["fx", ["vinyl", "reverse", "foley"], "foundfx"]]),
    ),
}

# ------------------------------------------------------ their kick books
# Style-true skeletons, like KICK_BANK for the nine — but a legend NEVER
# borrows another book (likeness rule; the loose nine may borrow these).

LEGEND_KICK_BANK = {
    "Farrow": [                    # skeletal funk stutters
        "X--X----X-X-----", "X--X------X--X--", "X-------X-X---X-",
        "X--X--X---X-----", "X---XX----X-----", "X--X----X---X---",
        "X-------XX--X---", "X--X------XX----", "X-X-----X---X---",
        "X--X---X--X-----", "X-----X---X--X--", "X--X----X-----X-"],
    "Doc Day": [                   # G-funk pocket
        "X------x--X-----", "X--x------X--x--", "X------xX---x---",
        "X---x-----X--x--", "X------x--X-x---", "X--x---x--X-----",
        "X-----x---X---x-", "X------x--X--x-x", "X--x------X-x---",
        "X---x--x--X-----", "X------x-xX-----", "X-x----x--X--x--"],
    "Kane East": [                 # gospel drive, pushed
        "X---x---X---x---", "X---x--xX---x---", "X--xX---X---x---",
        "X---x---X--xx---", "X---x-x-X---x---", "Xx--x---X---x---",
        "X---x---X-x-x---", "X--x----X---x--x", "X---x--xX--x----",
        "X--xx---X---x---", "X---x---X---xx--", "X---X---X---X---"],
    "J Dillo": [                   # drunk leans
        "X------x--X-----", "X--x------X--x--", "X------xX---x---",
        "X-----x---X----x", "X--x---x--X-x---", "X---x-----Xx----",
        "X------x-X---x--", "X-x-----x-X-----", "Xx-----x--X--x--",
        "X-----xx--X----x", "X------x--X---x-", "X---x--x--X-----"],
    "Mustang": [                   # ratchet bounce
        "X--x------X-----", "X--x------X--x--", "X--x---x--X-----",
        "X------x--X--x--", "X--x----X-X-----", "X---------X--x--",
        "X--x------X-x---", "X--x--x---X--x--", "X-x-------X--x--",
        "X--x------X---x-", "X------x--X-----", "X--xx-----X-----"],
    "Swish Beatz": [               # stomp quarters
        "X---X---X---X---", "X---X---X---X-x-", "X---X---X---x---",
        "X---x---X---X---", "X---X--xX---X---", "X---X---X--xX---",
        "X---X---X-------", "X-x-X---X---X---", "X---X---X---X--x",
        "X--xX---X---X---", "X---X---X-x-X---", "X---X-x-X---X---"],
    "DJ Premium": [                # surgical, sparse punches
        "X--x------X-----", "X---------X--x--", "X--x--x---X-----",
        "X-x-------X---x-", "X--x------Xx----", "X---x-----X--x--",
        "X--------xX-----", "X--x---x--X--x--", "X---------X-x---",
        "X-xx------X-----", "X--x-----XX--x--", "X-----x---X-----",
        # 2026-07-22: every entry above anchors its second kick on step
        # 10, so all twelve sat within a couple of moves of each other
        # and this DJ measured below the kick-variety floor. These keep
        # the surgical sparse character but put the answering kick
        # somewhere else — still boom bap, just not the same two spots.
        "X-------X-------", "X------x----X---", "X--x----X-----x-",
        "X-----X---------", "X-------X----x--", "X----x--X-------",
        "X--------X---x--", "X-x-----X---x---"],
    "Timberline": [                # stutters and syncopation
        "X--X--X---------", "X--X--X---X-----", "X-----X--X--X---",
        "X--X----X-X-----", "X---XX----X-----", "X--X--X--X--X---",
        "X-----X---XX----", "X--X---X--X---X-", "XX----X---X-----",
        "X---X--X----X---", "X--XX---X-------", "X-----X---X---X-"],
    "Just Flame": [                # pounding drive
        "X---x--xX---x---", "X--xx---X--xx---", "X---x---X--xx--x",
        "X---x-x-X---x-x-", "X--xx--xX---x---", "X---x---Xx--x---",
        "X---x--xX--x--x-", "X-x-x---X---x---", "X---xx--X---x--x",
        "X---x---X---x-xx", "X--xx---X-x-x---", "X---x--xX---xx--"],
    "Razor": [                     # off-kilter grime
        "X-----x---X--x--", "X--x----x-X-----", "X------x--X----x",
        "X-x-------X-x---", "X-----x--xX-----", "X---x-----X---x-",
        "X------x--Xx----", "X--x------X---x-", "X-----x---X-x--x",
        "Xx--------X--x--", "X----x----X-----", "X-----xx--X-----"],
    "Hitt Kid": [                  # hybrid bounce
        "X--x--x-X-X-----", "X--x--x---X-----", "X-----x---X--x--",
        "X--x----X-X---x-", "X--x--x-X-------", "X------xX-X-----",
        "X--x------X-x---", "X--x--xxX-X-----", "X-----x-X-X--x--",
        "X--x--x---X---x-", "X-x---x-X-X-----", "X--x----X-X-x---"],
    "No Alias": [                  # deep pocket rollers
        "X-----x---X--x--", "X--x------X-----", "X-----x-x-X-----",
        "X---x-----X-x---", "X-----xx--X--x--", "X-x---x---X-----",
        "X-----x---X-xx--", "X--x------X---x-", "X-----x--xX-----",
        "X---xx----X--x--", "X------x--X--x--", "X-----x---X---x-"],
}

# ------------------------------------------------- their beat titles
# Two-word banks in each legend's voice (beat_machine merges these into
# TITLES); the runtime picker keeps titles globally unique.

LEGEND_TITLES = {
    "Farrow": (["Skatepark", "Neon", "Mineral", "Tropic", "Vivid",
                "Plastic", "Coral", "Sunbeam"],
               ["Grin", "Splash", "Orbit", "Custom", "Tilt", "Loop",
                "Shine", "Wink"]),
    "Doc Day": (["Lowrider", "Boulevard", "Palmtree", "Hydraulic",
                 "Whitewall", "Marina", "Freeway", "Golden"],
                ["Cruise", "Bounce", "Ritual", "Standard", "Protocol",
                 "Chapter", "Session", "Gleam"]),
    "Kane East": (["Velour", "Stained", "Marble", "Ivy", "Gilded",
                   "Rose", "Organ", "Satin"],
                  ["Window", "Chorus", "Scholar", "Parade", "Registry",
                   "Tuition", "Applause", "Hymn"]),
    "J Dillo": (["Wonky", "Melted", "Humid", "Loopy", "Maple",
                 "Drowsy", "Slanted", "Syrup"],
                ["Slump", "Sway", "Cassette", "Dimple", "Wobble",
                 "Naptime", "Crumb", "Pillow"]),
    "Mustang": (["Ratchet", "Function", "Patio", "Poolside", "Balmy",
                 "Slick", "Tinted", "Velvet"],
                ["Anthem", "Callout", "Rollcall", "Twostep", "Strut",
                 "Chant", "Flex", "Glide"]),
    "Swish Beatz": (["Stadium", "Sideline", "Confetti", "Trophy",
                     "Banner", "Podium", "Playoff", "Champion"],
                    ["Stomp", "Whistle", "Rally", "Eruption", "Lap",
                     "Roar", "Cadence", "Victory"]),
    "DJ Premium": (["Marquee", "Skyline", "Borough", "Token", "Transit",
                    "Rooftop", "Newsstand", "Turnstile"],
                   ["Cipher", "Credential", "Doctrine", "Archive",
                    "Bulletin", "Ledger", "Metric", "Byline"]),
    "Timberline": (["Stutter", "Mirage", "Cobra", "Desert", "Falcon",
                    "Ripple", "Digital", "Sahara"],
                   ["Charm", "Pattern", "Signal", "Whisper", "Flutter",
                    "Circuit", "Pulse", "Murmur"]),
    "Just Flame": (["Cathedral", "Brass", "Royal", "Colossal", "Regal",
                    "Thunder", "Crowned", "Imperial"],
                   ["March", "Fanfare", "Horns", "Procession", "Triumph",
                    "Overture", "Crescendo", "Salute"]),
    "Razor": (["Rusty", "Temple", "Cinder", "Iron", "Smoky", "Cracked",
               "Monk", "Stone"],
              ["Chamber", "Scroll", "Dagger", "Alley", "Fable", "Creed",
               "Incense", "Shadowbox"]),
    "Hitt Kid": (["Platinum", "Vaulted", "Crown", "Ballroom", "Onyx",
                  "Prime", "Laced", "Stacked"],
                 ["Ceiling", "Momentum", "Charts", "Verdict", "Summit",
                  "Bezel", "Encore", "Milestone"]),
    "No Alias": (["Southside", "Humble", "Vintage", "Mentor", "Refined",
                  "Classic", "Modest", "Studied"],
                 ["Notebook", "Portrait", "Manuscript", "Redraft",
                  "Excerpt", "Preface", "Margin", "Draft"]),
}

KICK_BANK.update(LEGEND_KICK_BANK)


def load_legends(normalize):
    """Same contract as crew.load_crew, for legends_config.json.
    `normalize` is crew.normalize_preset (passed in to avoid a circular
    import). Style keys (grammar/kick_flavors/extras/library) re-sync on
    a LEGENDS_VERSION bump unless "_style_lock" is set."""
    if not CONFIG.exists():
        doc = {"_readme": [
            "The Legends roster — twelve signature-style producers. "
            "Edit a number and the next render uses it; delete the "
            "file to regenerate the built-ins. Same schema as "
            "crew_config.json.",
            "These follow the crew's instrument sound-variation rules "
            "only; their likeness rules (tight swing, home-weighted "
            "grammar, no evolution, 4/4) live in the engine."],
            "_legends_version": LEGENDS_VERSION}
        doc.update(LEGENDS_DEFAULT)
        CONFIG.write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    try:
        raw = json.loads(CONFIG.read_text())
        changed = False
        if raw.get("_legends_version", 0) < LEGENDS_VERSION \
                and not raw.get("_style_lock"):
            for n, p in raw.items():
                if not n.startswith("_") and n in LEGENDS_DEFAULT:
                    for k in ("grammar", "kick_flavors", "extras",
                              "library"):
                        p[k] = LEGENDS_DEFAULT[n][k]
            raw["_legends_version"] = LEGENDS_VERSION
            changed = True
        for n, p in raw.items():
            if n.startswith("_") or n not in LEGENDS_DEFAULT:
                continue
            p["legend"] = True                    # the flag IS the rules
            for k in ("grammar", "kick_flavors", "extras", "library"):
                if k not in p:
                    p[k] = LEGENDS_DEFAULT[n][k]
                    changed = True
        if changed:
            CONFIG.write_text(json.dumps(raw, indent=1, ensure_ascii=False))
        legends = {n: normalize(p) for n, p in raw.items()
                   if not n.startswith("_")}
        if legends:
            return legends
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"WARNING: {CONFIG.name} is broken ({e}) — using the "
              "built-in Legends. Fix or delete the file to silence this.")
    return {n: normalize(json.loads(json.dumps(p)))
            for n, p in LEGENDS_DEFAULT.items()}
