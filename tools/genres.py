"""The Styles — a third roster: subgenres, not people (owner request
2026-07-19).

The nine crew are loose characters (v6: variety over style fidelity).
The twelve Legends chase one producer's likeness. This roster chases a
SCENE — seventeen subgenres that the first two rosters leave uncovered or
barely touched, each tuned so the beat comes out sounding like that style
and not like a crew beat wearing its hat.

Owner decisions that shaped this file (2026-07-19):

- Three picks overlapped the existing rosters, so they are aimed
  deliberately AWAY from the character that already covers them:
  Detroit at the post-Dilla street side (Black Milk / Danny Brown /
  Apollo Brown) rather than the drunk-swing side Otto Grit and J Dillo
  already own; G-Funk at the DJ Quik / Warren G / Above the Law bounce
  rather than Doc Day's surgical Dre pocket; Wonky at the LA beat scene
  (Flying Lotus, Hudson Mohawke, Rustie) where it goes properly off-grid
  instead of Dilla-adjacent.
- "Acid rap" means two unrelated things, so it is two buttons: the 1989
  Detroit Esham lineage that fathered horrorcore, and the bright jazzy
  2013 lineage.
- "Southern hip hop" is an umbrella and Miami Bass and NO Bounce were
  already asked for separately, so it split four ways: Crunk (with the
  harder festival edge, not just 2003 crunk), Memphis, Organized Noize,
  and Houston / Screw.
- GENRE FIDELITY WINS OVER THE SPARSE-BED RULE inside this box. The
  standing 2026-07-17 rule leans every beat sparse because he plays over
  the top; Baltimore club, bounce and Miami bass are dense by definition,
  so each preset DECLARES its own density and the engine honours it.

The rules that make these strict (all keyed off "genre": True):

- canon lanes. Each style names the lanes carrying the figure that
  DEFINES it — the dembow, the Baltimore 8-count, the Triggerman answer.
  compose() places those verbatim from the authentic variants here, and
  vary_preset gives them the gentle anchor wander instead of the
  drop/add mutation. Variety comes from everywhere else: hats, perc,
  guests, fills, flavors, samples, arrangement.
- grammar weights stay heavily HOME — no v6 flat menus.
- kick banks never cross-pollinate INTO a style.
- swing is pinned per style (genre_swing) — a reggaeton that wanders to
  62% swing is not a reggaeton.
- no random 3/4, 6/8 or exotic-grid rolls (the notes box may still ask).
- no engine-driven evolution: a genre is a tradition, not a career.
- "traditional" means the TEXTBOOK version of that style (canon variant
  0), never the generic 2&4 backbone — forcing plain 2&4 onto reggaeton
  or club would simply stop being the genre.

Roster config: genres_config.json at the project root, auto-written from
GENRES_DEFAULT on first run, editable ever after (same contract as
crew_config.json and legends_config.json; delete it to regenerate).
"""
import json
from pathlib import Path

from pattern_gen import KICK_BANK

CONFIG = Path(__file__).resolve().parent.parent / "genres_config.json"
GENRES_VERSION = 6

R16 = "-" * 16
_BK = ["----X-------X---"] * 8            # placeholder; compose rewrites
_H8 = ["x-x-x-x-x-x-x-x-"] * 8


def _stamp_tail(hit="--------------x-"):
    return [R16] * 3 + [hit] + [R16] * 3 + [hit]


# ---------------------------------------------------------------- canon
# The figures that ARE these styles. Step 0 is the downbeat; capitals
# fall on beat starts (0, 4, 8, 12), lowercase are syncopations, "." is
# a ghost. Every variant here is a real way the style is played — the
# engine picks among them, so beats differ without the style eroding.

# reggaeton: the dembow. Two mirrored tresillo cells — kick, +3, +6,
# kick, +3, +6. This is the whole riddim; move a hit and it's gone.
DEMBOW_SNARE = ["---X--X----X--X-",      # textbook
                "---X--X----X--XX",      # with the tail double
                "---X--X-.--X--X-",      # a ghost in the gap
                "---X--X----X--X."]
DEMBOW_KICK = ["X-------X-------",       # beats 1 and 3, nothing else
               "X-------X-----x-",
               "X-----x-X-------",
               "X-------X---X---",
               "X-----x-X-----x-"]

# Baltimore club: the 8-count. A doubled tresillo (0 +3 +6, 8 +11 +14)
# at 130 — the same cell reggaeton uses, played twice as fast on the
# kick instead of the snare. That kinship is real, not a coincidence.
BMORE_KICK = ["X--x--x-X--x--x-",        # the 8-count
              "X--x--x-X--x--X-",
              "X--x--x-X-x---x-",
              "X--x--x-X--x-x--",
              "X--x--x-X--xx-x-"]
BMORE_CLAP = ["----X--X--X-X---",        # 2 and 4 plus the two pushes
              "----X--X--X-X--x",
              "----X--X--X-X-x-",
              "----X--X----X---"]

# Miami bass: the electro kick out of the Planet Rock lineage, with the
# long decaying 808 doing the work between hits.
ELECTRO_KICK = ["X--x--x---x-X---",
                "X--x--x-----X--x",
                "X--x--x---x-X--x",
                "X-----x---x-X---",
                "X--x----X-x-X---"]

# New Orleans bounce: the Triggerman answer — backbeat plus the stutter
# at the top of 4 that the whole style calls and responds to.
BOUNCE_SNARE = ["----X--X----X-xx",
                "----X--X----X-x-",
                "----X--X--x-X-xx",
                "----X-xX----X-xx"]


GENRES_DEFAULT = {
    # ============================================ SOUTHERN, four ways
    "Memphis": dict(
        num=22, bpm=140, era="genre", built="Three 6 Mafia / DJ Paul",
        genre=True, genre_swing=52, density="home",
        listen=("mid-90s Memphis: half-time feel at 140, dark and minor, "
                "lo-fi to the point of distortion, cowbell riding through, "
                "fast triplet hats, a deep 808 and a snare that lands on "
                "3 like a door slamming"),
        kit=dict(
            kick=("kick", None, ["808", "deep", "sub"], (0.4, 0.9)),
            snare=("snare", None, ["lofi", "dusty", "tight"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.3),
            perc=("perc", None, ["cowbell", "block"], 0.5),
            stamp=("fx", None, ["vocal", "scream", "dark"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 52, 2201), _BK),
            snare=(0.0, 0.86, (0, 1, 52, 2202), _BK),
            hat=(-0.14, 0.34, (0, 1, 52, 2203), _H8),
            perc=(0.18, 0.32, (0, 2, 52, 2204), _H8),
            stamp=(-0.3, 0.4, (0, 1, 52, 2205), _stamp_tail()),
        ),
        dust=0.5, vinyl=-46, wow=0.0, sidechain=0.2,
        space=("dry", ["snare"]), alt=None,
        drive=1.6, kick_dist=0.12, mix_sat=0.15,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 4, 1, 1, 5, 2, 6, 1, 4, 3, 2, 2, 3, 1],
                      hits=[3, 5], double_p=0.3),
            snare=dict(modes=[["halftime", 0.7], ["backbeat", 0.2],
                              ["sparse", 0.1]],
                       ghosts=[0, 1], gcells=[7, 15]),
            hat=dict(modes=[["triplets", 0.4], ["trip_rolls", 0.25],
                            ["sixteenths", 0.2], ["eighths", 0.15]],
                     open_p=0.05, roll_n=[1, 2]),
            perc=dict(modes=[["offbeats", 0.45], ["sparse", 0.3],
                             ["eighths", 0.25]]),
        ),
        kick_flavors=[[0.55, "808", ["deep", "sub", "long"], [0.6, 1.1]],
                      [0.45, None, ["knock", "punch", "deep"],
                       [0.25, 0.5]]],
        library=dict(p=0.2, tags=[["trap", 3], ["lofi", 3],
                                  ["boom-bap", 1]]),
        extras=dict(p=0.55, nmax=2, pool=[
            ["perc", ["cowbell"], "cowbell"],
            ["fx", ["dark", "riser", "reverse"], "cutfx"],
            ["crash", ["crash", "china"], "crash2"]]),
    ),
    "Crunk": dict(
        num=23, bpm=140, era="genre", built="Lil Jon (through the hard, "
        "festival end — Turn Down for What)",
        genre=True, genre_swing=50, density="sparse",
        listen=("half-time stomp at 140 with the room deliberately EMPTY "
                "for a chant: a huge distorted 808, claps that hit like a "
                "crowd, almost no hats, and a hard synth-stab energy — "
                "space is the instrument, and everything in it is loud"),
        kit=dict(
            kick=("kick", None, ["808", "distort", "hard"], (0.5, 1.0)),
            clap=("clap", None, ["big", "crowd", "hard"], 1.0),
            snare=("snare", None, ["crack", "hard"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.25),
            stamp=("fx", None, ["vocal", "yeah", "airhorn", "shout"], 1.0),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 2211), _BK),
            clap=(0.0, 0.92, (0, 1, 50, 2212), _BK),
            snare=(0.0, 0.7, (0, 1, 50, 2213), _BK),
            hat=(0.12, 0.28, (0, 1, 50, 2214), _H8),
            stamp=(-0.28, 0.46, (0, 1, 50, 2215), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.3,
        space=("gated", ["clap"]), alt=None,
        drive=1.8, kick_dist=0.3, mix_sat=0.25,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 3, 1, 1, 4, 1, 7, 1, 3, 2, 2, 1, 3, 1],
                      hits=[2, 4], double_p=0.35),
            clap=dict(modes=[["stomp", 0.65], ["backbeat", 0.25],
                             ["halftime", 0.1]],
                      ghosts=[0, 0], gcells=[7, 15]),
            snare=dict(copy="clap"),
            hat=dict(modes=[["sparse", 0.45], ["eighths", 0.3],
                            ["offbeats", 0.15], ["trip_rolls", 0.1]],
                     open_p=0.04, roll_n=[1, 1]),
        ),
        kick_flavors=[[0.7, "808", ["distort", "hard", "long"], [0.6, 1.2]],
                      [0.3, None, ["punch", "hard", "knock"], [0.3, 0.6]]],
        library=dict(p=0.15, tags=[["trap", 3], ["electro", 1]]),
        extras=dict(p=0.45, nmax=1, pool=[
            ["fx", ["airhorn", "shout", "riser"], "cutfx"],
            ["crash", ["crash"], "crash2"]]),
    ),
    "Organized Noize": dict(
        num=24, bpm=95, era="genre", built="Organized Noize / Dungeon "
        "Family (Outkast, Goodie Mob)",
        genre=True, genre_swing=56, density="home",
        listen=("Atlanta soul-funk played like a band, not a machine: a "
                "warm rounded kick, a fat snare with real ghost notes, "
                "congas and tambourine moving underneath, loose 56% "
                "swing, live-room warmth instead of dust"),
        kit=dict(
            kick=("kick", None, ["warm", "round", "boom"], (0.25, 0.6)),
            snare=("snare", None, ["fat", "warm", "rimshot"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.45),
            bongo=("bongo", None, ["conga", "bongo"], 0.7),
            perc=("perc", None, ["tamb", "shaker"], 0.7),
            stamp=("fx", None, ["vocal", "horn", "guitar"], 0.8),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 56, 2221), _BK),
            snare=(0.0, 0.88, (0, 2, 56, 2222), _BK),
            hat=(-0.16, 0.36, (0, 2, 56, 2223), _H8),
            bongo=(0.22, 0.3, (0, 3, 56, 2224), _H8),
            perc=(0.16, 0.28, (0, 3, 56, 2225), _H8),
            stamp=(-0.26, 0.36, (0, 2, 56, 2226), _stamp_tail()),
        ),
        dust=0.15, vinyl=-52, wow=0.05, sidechain=0.15,
        space=("room", ["snare"]), alt=None,
        drive=1.35, kick_dist=0.0, mix_sat=0.1,
        grammar=dict(
            kick=dict(w=[10, 1, 3, 5, 2, 2, 5, 3, 4, 2, 5, 3, 2, 3, 4, 2],
                      hits=[4, 7], double_p=0.35),
            snare=dict(modes=[["backbeat", 0.75], ["displaced", 0.15],
                              ["sparse", 0.1]],
                       ghosts=[1, 2], gcells=[3, 7, 11, 15]),
            hat=dict(modes=[["eighths", 0.35], ["sixteenths", 0.25],
                            ["offbeats", 0.2], ["broken", 0.2]],
                     open_p=0.1),
            bongo=dict(modes=[["offbeats", 0.4], ["broken", 0.3],
                              ["sparse", 0.3]]),
            perc=dict(modes=[["offbeats", 0.45], ["eighths", 0.3],
                             ["sparse", 0.25]]),
        ),
        kick_flavors=[[0.15, "808", ["deep", "warm"], [0.4, 0.8]],
                      [0.85, None, ["warm", "round", "boom", "punch"],
                       [0.2, 0.55]]],
        library=dict(p=0.4, tags=[["funk", 3], ["soul", 3],
                                  ["motown", 2], ["rnb", 1]]),
        extras=dict(p=0.7, nmax=2, pool=[
            ["perc", ["tamb"], "tamb"],
            ["bongo", ["conga"], "congas2"],
            ["rim", ["rim", "stick"], "rims"],
            ["perc", ["shaker"], "shaker"]]),
    ),
    "Houston Screw": dict(
        num=25, bpm=66, era="genre", built="DJ Screw / chopped and screwed",
        genre=True, genre_swing=54, density="sparse",
        listen=("everything dragged down to 66 and left to sag: a huge "
                "slow sustained 808, hats so sparse you count the gaps, a "
                "thick lazy snare well behind the beat, and air "
                "everywhere — the tempo IS the style"),
        kit=dict(
            kick=("kick", None, ["808", "sub", "deep", "long"], (0.9, 1.6)),
            snare=("snare", None, ["fat", "warm", "dusty"], 1.0),
            hat=("hat", None, ["closed"], 0.5),
            stamp=("fx", None, ["vocal", "reverse", "tape"], 1.2),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 54, 2231), _BK),
            snare=(0.0, 0.84, (+22, 3, 54, 2232), _BK),
            hat=(-0.12, 0.3, (+8, 3, 54, 2233), _H8),
            stamp=(-0.3, 0.38, (0, 2, 54, 2234), _stamp_tail()),
        ),
        dust=0.3, vinyl=-48, wow=0.35, sidechain=0.2,
        space=("washed", ["snare"]), alt=None,
        drive=1.3, kick_dist=0.05, mix_sat=0.12,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 3, 1, 1, 4, 1, 6, 1, 3, 2, 1, 1, 3, 1],
                      hits=[2, 4], double_p=0.2),
            snare=dict(modes=[["backbeat", 0.5], ["halftime", 0.4],
                              ["sparse", 0.1]],
                       ghosts=[0, 1], gcells=[7, 15]),
            hat=dict(modes=[["sparse", 0.4], ["eighths", 0.3],
                            ["offbeats", 0.2], ["sixteenths", 0.1]],
                     open_p=0.08),
        ),
        kick_flavors=[[0.75, "808", ["sub", "deep", "long"], [1.0, 1.7]],
                      [0.25, None, ["boom", "warm"], [0.4, 0.8]]],
        library=dict(p=0.2, tags=[["lofi", 3], ["cloud-rap", 2],
                                  ["boom-bap", 1]]),
        extras=dict(p=0.4, nmax=1, pool=[
            ["fx", ["reverse", "tape", "riser"], "cutfx"],
            ["rim", ["rim"], "rims"]]),
    ),
    # ================================================== the emo/dark set
    "Emo Hip Hop": dict(
        num=26, bpm=150, era="genre", built="Lil Peep / XXXTentacion",
        genre=True, genre_swing=50, density="home",
        listen=("half-time at 150 with everything soaked in reverb: a "
                "clipped distorted 808, a big washed-out snare that hits "
                "like a live drummer, simple straight hats, and enough "
                "room in the middle for a guitar to sit"),
        kit=dict(
            kick=("kick", None, ["808", "distort", "deep"], (0.45, 0.95)),
            snare=("snare", None, ["big", "roomy", "acoustic"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.3),
            crash=("crash", None, ["crash", "splash"], 2.2),
            stamp=("fx", None, ["vocal", "tape", "noise"], 1.0),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 2241), _BK),
            snare=(0.0, 0.9, (0, 2, 50, 2242), _BK),
            hat=(-0.12, 0.32, (0, 1, 50, 2243), _H8),
            crash=(0.2, 0.3, (0, 2, 50, 2244), _stamp_tail("X" + R16[1:])),
            stamp=(-0.28, 0.36, (0, 1, 50, 2245), _stamp_tail()),
        ),
        dust=0.1, vinyl=-54, wow=0.0, sidechain=0.25,
        space=("washed", ["snare"]), alt=None,
        drive=1.6, kick_dist=0.28, mix_sat=0.22,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 4, 1, 1, 5, 2, 6, 1, 4, 3, 2, 2, 3, 1],
                      hits=[3, 5], double_p=0.3),
            snare=dict(modes=[["halftime", 0.6], ["backbeat", 0.3],
                              ["sparse", 0.1]],
                       ghosts=[0, 1], gcells=[7, 15]),
            hat=dict(modes=[["eighths", 0.4], ["sixteenths", 0.25],
                            ["sparse", 0.2], ["trip_rolls", 0.15]],
                     open_p=0.06, roll_n=[1, 2]),
        ),
        kick_flavors=[[0.65, "808", ["distort", "deep", "long"],
                       [0.6, 1.1]],
                      [0.35, None, ["punch", "acoustic", "knock"],
                       [0.25, 0.55]]],
        library=dict(p=0.25, tags=[["trap", 2], ["rock", 2], ["punk", 1]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["crash", ["crash", "splash"], "crash2"],
            ["fx", ["noise", "tape", "reverse"], "cutfx"]]),
    ),
    "Acid Rap Detroit": dict(
        num=27, bpm=92, era="genre", built="Esham — the 1989 Detroit acid "
        "rap that fathered horrorcore",
        genre=True, genre_swing=54, density="sparse",
        listen=("raw and wrong on purpose: rock samples chopped over a "
                "dusty mid-tempo kit, a snare that cracks too loud, tape "
                "hiss and vinyl noise left in, sparse eerie colors, "
                "nothing polished anywhere"),
        kit=dict(
            kick=("kick", None, ["boom", "dusty", "punch"], (0.3, 0.6)),
            snare=("snare", None, ["crack", "dusty", "lofi"], 1.0),
            hat=("hat", None, ["closed", "dusty"], 0.35),
            stamp=("fx", None, ["vocal", "scream", "dark", "noise"], 1.0),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 54, 2251), _BK),
            snare=(0.0, 0.9, (0, 2, 54, 2252), _BK),
            hat=(0.14, 0.34, (0, 2, 54, 2253), _H8),
            stamp=(-0.3, 0.42, (0, 2, 54, 2254), _stamp_tail()),
        ),
        dust=0.85, vinyl=-40, wow=0.15, sidechain=0.1,
        space=("room", ["snare"]), alt=None,
        drive=1.5, kick_dist=0.15, mix_sat=0.2,
        grammar=dict(
            kick=dict(w=[10, 1, 3, 5, 2, 2, 5, 3, 5, 2, 4, 3, 2, 3, 3, 2],
                      hits=[3, 6], double_p=0.3),
            snare=dict(modes=[["backbeat", 0.7], ["displaced", 0.2],
                              ["sparse", 0.1]],
                       ghosts=[0, 2], gcells=[3, 7, 11, 15]),
            hat=dict(modes=[["eighths", 0.4], ["sparse", 0.3],
                            ["offbeats", 0.2], ["broken", 0.1]],
                     open_p=0.1),
        ),
        kick_flavors=[[0.15, "808", ["deep", "dark"], [0.4, 0.8]],
                      [0.85, None, ["boom", "dusty", "punch"],
                       [0.25, 0.6]]],
        library=dict(p=0.3, tags=[["lofi", 3], ["rock", 2],
                                  ["boom-bap", 2]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["fx", ["dark", "noise", "reverse"], "cutfx"],
            ["perc", ["block", "tamb"], "woods"]]),
    ),
    "Acid Rap Bright": dict(
        num=28, bpm=88, era="genre", built="the 2013 Acid Rap lineage — "
        "bright, jazzy, gospel-leaning",
        genre=True, genre_swing=58, density="home",
        listen=("major-key and grinning: a light kick, a snappy clap-and-"
                "snare stack, hand percussion everywhere, 58% swing that "
                "skips rather than drags, live-room air and not one grain "
                "of dust"),
        kit=dict(
            kick=("kick", None, ["warm", "round", "tight"], (0.2, 0.45)),
            snare=("snare", None, ["snappy", "tight", "rimshot"], 1.0),
            clap=("clap", None, ["clap", "bright"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.4),
            bongo=("bongo", None, ["conga", "bongo"], 0.6),
            stamp=("fx", None, ["vocal", "horn", "organ"], 0.7),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 58, 2261), _BK),
            snare=(0.0, 0.82, (0, 2, 58, 2262), _BK),
            clap=(0.1, 0.6, (+10, 2, 58, 2263), _BK),
            hat=(-0.15, 0.36, (0, 2, 58, 2264), _H8),
            bongo=(0.24, 0.32, (0, 3, 58, 2265), _H8),
            stamp=(-0.24, 0.34, (0, 2, 58, 2266), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.12,
        space=("room", ["snare"]), alt=None,
        drive=1.3, kick_dist=0.0, mix_sat=0.05,
        grammar=dict(
            kick=dict(w=[10, 1, 3, 5, 2, 2, 5, 3, 4, 2, 5, 3, 2, 3, 4, 2],
                      hits=[3, 6], double_p=0.35),
            snare=dict(modes=[["backbeat", 0.8], ["displaced", 0.1],
                              ["sparse", 0.1]],
                       ghosts=[1, 2], gcells=[3, 7, 11, 15]),
            clap=dict(copy="snare"),
            hat=dict(modes=[["eighths", 0.35], ["sixteenths", 0.25],
                            ["offbeats", 0.25], ["broken", 0.15]],
                     open_p=0.12),
            bongo=dict(modes=[["offbeats", 0.4], ["broken", 0.35],
                              ["eighths", 0.25]]),
        ),
        kick_flavors=[[0.1, "808", ["warm"], [0.35, 0.7]],
                      [0.9, None, ["warm", "round", "tight", "punch"],
                       [0.18, 0.45]]],
        library=dict(p=0.4, tags=[["soul", 3], ["funk", 2],
                                  ["neo-soul", 2], ["rnb", 1]]),
        extras=dict(p=0.75, nmax=2, pool=[
            ["perc", ["tamb"], "tamb"],
            ["bongo", ["conga"], "congas2"],
            ["perc", ["shaker"], "shaker"],
            ["perc", ["block", "clave"], "woods"]]),
    ),
    "Horror Rap": dict(
        num=29, bpm=90, era="genre", built="Gravediggaz / Brotha Lynch / "
        "the horrorcore lane",
        genre=True, genre_swing=53, density="sparse",
        listen=("mid-90s boom bap turned to face the wall: a heavy dusty "
                "kick, a hard snare drowning in a long dark reverb, "
                "detuned bell and chime colors, tape hiss, and space left "
                "deliberately empty so it feels like something's in it"),
        kit=dict(
            kick=("kick", None, ["boom", "deep", "dusty"], (0.3, 0.65)),
            snare=("snare", None, ["crack", "hard", "dusty"], 1.0),
            hat=("hat", None, ["closed", "dusty"], 0.35),
            bell=("perc", None, ["bell", "chime"], 1.2),
            stamp=("fx", None, ["dark", "scream", "reverse", "vocal"], 1.2),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 53, 2271), _BK),
            snare=(0.0, 0.88, (0, 2, 53, 2272), _BK),
            hat=(-0.16, 0.32, (0, 2, 53, 2273), _H8),
            bell=(0.28, 0.26, (0, 3, 53, 2274), _stamp_tail()),
            stamp=(-0.32, 0.4, (0, 2, 53, 2275), _stamp_tail()),
        ),
        dust=0.7, vinyl=-42, wow=0.12, sidechain=0.12,
        space=("washed", ["snare"]), alt=None,
        drive=1.45, kick_dist=0.1, mix_sat=0.18,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 5, 2, 1, 5, 2, 5, 1, 4, 3, 2, 2, 3, 1],
                      hits=[3, 5], double_p=0.25),
            snare=dict(modes=[["backbeat", 0.75], ["halftime", 0.15],
                              ["sparse", 0.1]],
                       ghosts=[0, 1], gcells=[7, 11, 15]),
            hat=dict(modes=[["eighths", 0.35], ["sparse", 0.35],
                            ["offbeats", 0.2], ["broken", 0.1]],
                     open_p=0.08),
            bell=dict(modes=[["answer", 0.5], ["sparse", 0.35],
                             ["offbeats", 0.15]]),
        ),
        kick_flavors=[[0.25, "808", ["deep", "dark", "sub"], [0.5, 0.95]],
                      [0.75, None, ["boom", "deep", "dusty"], [0.3, 0.65]]],
        library=dict(p=0.3, tags=[["boom-bap", 3], ["lofi", 2]]),
        extras=dict(p=0.6, nmax=2, pool=[
            ["fx", ["dark", "reverse", "riser"], "cutfx"],
            ["perc", ["bell", "chime"], "bells"],
            ["crash", ["china", "crash"], "crash2"]]),
    ),
    # ================================================ the off-grid set
    "Wonky": dict(
        num=30, bpm=86, era="genre", built="the LA beat scene — Flying "
        "Lotus, Hudson Mohawke, Rustie (NOT the Dilla lane Otto Grit and "
        "J Dillo already hold)",
        genre=True, genre_swing=62, density="sparse",
        listen=("deliberately off the grid: every lane jittered by "
                "milliseconds so nothing lines up, 62% swing pulling it "
                "sideways, a sub-heavy kick, a snare that arrives late "
                "and smeared, and colors that sound slightly out of tune"),
        kit=dict(
            kick=("kick", None, ["sub", "deep", "808"], (0.35, 0.8)),
            snare=("snare", None, ["fat", "dusty", "smear"], 1.0),
            hat=("hat", None, ["closed", "loose"], 0.4),
            blips=("fx", None, ["glitch", "zap", "bend"], 0.7),
            stamp=("fx", None, ["vocal", "bend", "glitch"], 0.9),
        ),
        lanes=dict(
            # the JITTER is the genre: 6-9 ms of wander per lane, where
            # the crew and legends sit at 1-3. Nothing quantizes.
            kick=(0.0, 1.0, (+6, 7, 62, 2281), _BK),
            snare=(0.0, 0.86, (+14, 9, 62, 2282), _BK),
            hat=(-0.15, 0.34, (-5, 8, 62, 2283), _H8),
            blips=(0.3, 0.26, (0, 9, 62, 2284), _stamp_tail()),
            stamp=(-0.3, 0.36, (0, 7, 62, 2285), _stamp_tail()),
        ),
        dust=0.25, vinyl=-50, wow=0.3, sidechain=0.25,
        space=("room", ["snare"]), alt=None,
        drive=1.5, kick_dist=0.12, mix_sat=0.25,
        grammar=dict(
            kick=dict(w=[10, 2, 4, 5, 2, 3, 5, 4, 4, 3, 5, 4, 3, 3, 4, 3],
                      hits=[3, 6], double_p=0.45),
            snare=dict(modes=[["displaced", 0.45], ["backbeat", 0.25],
                              ["sparse", 0.2], ["halftime", 0.1]],
                       ghosts=[1, 2], gcells=[3, 7, 11, 15]),
            hat=dict(modes=[["broken", 0.35], ["sparse", 0.25],
                            ["triplets", 0.2], ["offbeats", 0.2]],
                     open_p=0.14),
            blips=dict(modes=[["answer", 0.45], ["sparse", 0.35],
                              ["broken", 0.2]]),
        ),
        kick_flavors=[[0.45, "808", ["sub", "deep", "bend"], [0.5, 1.0]],
                      [0.55, None, ["boom", "round", "deep"], [0.3, 0.7]]],
        library=dict(p=0.35, tags=[["lofi", 3], ["neo-soul", 2],
                                   ["garage", 1]]),
        extras=dict(p=0.7, nmax=2, pool=[
            ["fx", ["glitch", "bend", "zap"], "blips"],
            ["perc", ["tabla", "block"], "woods"],
            ["bongo", ["conga"], "congas2"]]),
    ),
    "Trip Hop": dict(
        num=31, bpm=88, era="genre", built="Massive Attack / Portishead / "
        "Tricky",
        genre=True, genre_swing=56, density="sparse",
        listen=("a slow heavy breakbeat left mostly alone: kick and snare "
                "far apart, the snare huge in a plate reverb, a thick "
                "vinyl bed under everything, hats barely there, and a "
                "patient half-time weight that never speeds up"),
        kit=dict(
            kick=("kick", None, ["boom", "round", "deep"], (0.3, 0.7)),
            snare=("snare", None, ["fat", "roomy", "dusty"], 1.0),
            hat=("hat", None, ["closed", "loose"], 0.4),
            rim=("rim", None, ["rim", "stick"], 0.5),
            stamp=("fx", None, ["vocal", "noise", "tape"], 1.1),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 3, 56, 2291), _BK),
            snare=(0.0, 0.9, (+8, 3, 56, 2292), _BK),
            hat=(-0.14, 0.28, (0, 3, 56, 2293), _H8),
            rim=(0.2, 0.24, (0, 3, 56, 2294), _H8),
            stamp=(-0.3, 0.34, (0, 3, 56, 2295), _stamp_tail()),
        ),
        dust=0.4, vinyl=-38, wow=0.25, sidechain=0.15,
        space=("plate", ["snare"]), alt=None,
        drive=1.35, kick_dist=0.0, mix_sat=0.12,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 4, 1, 2, 5, 2, 5, 1, 4, 2, 2, 2, 3, 1],
                      hits=[2, 5], double_p=0.25),
            snare=dict(modes=[["halftime", 0.45], ["backbeat", 0.35],
                              ["sparse", 0.2]],
                       ghosts=[1, 2], gcells=[3, 7, 11, 15]),
            hat=dict(modes=[["sparse", 0.4], ["eighths", 0.25],
                            ["offbeats", 0.2], ["broken", 0.15]],
                     open_p=0.1),
            rim=dict(modes=[["sparse", 0.5], ["answer", 0.3],
                            ["offbeats", 0.2]]),
        ),
        kick_flavors=[[0.2, "808", ["deep", "sub"], [0.5, 0.9]],
                      [0.8, None, ["boom", "round", "deep"], [0.3, 0.7]]],
        library=dict(p=0.45, tags=[["breakbeat", 3], ["lofi", 2],
                                   ["dnb", 1], ["boom-bap", 1]]),
        extras=dict(p=0.55, nmax=1, pool=[
            ["fx", ["noise", "tape", "reverse"], "cutfx"],
            ["perc", ["shaker", "tamb"], "shaker"]]),
    ),
    # ================================================== the club set
    "Baltimore Club": dict(
        num=32, bpm=130, era="genre", built="Baltimore club — Rod Lee, "
        "KW Griff, the Bmore 8-count",
        genre=True, genre_swing=50, density="busy",
        listen=("the 8-count: a five-and-six-hit kick figure looping "
                "hard at 130 while claps push on the 'a' of 2 and the "
                "'&' of 3, breakbeat chops and vocal stabs flying over "
                "the top. Relentless, and it never lets up"),
        canon=dict(kick=BMORE_KICK, clap=BMORE_CLAP),
        kit=dict(
            kick=("kick", None, ["punch", "tight", "club"], (0.14, 0.35)),
            clap=("clap", None, ["clap", "big"], 1.0),
            snare=("snare", None, ["tight", "crack"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.28),
            stamp=("fx", None, ["vocal", "stab", "shout"], 0.8),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 2301), _BK),
            clap=(0.0, 0.88, (0, 1, 50, 2302), _BK),
            snare=(0.08, 0.62, (0, 1, 50, 2303), _BK),
            hat=(-0.12, 0.36, (0, 1, 50, 2304), _H8),
            stamp=(-0.26, 0.44, (0, 1, 50, 2305), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.2,
        space=("dry", ["clap"]), alt=None,
        drive=1.55, kick_dist=0.08, mix_sat=0.15,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 6, 1, 1, 6, 1, 8, 1, 1, 6, 1, 1, 6, 1],
                      hits=[5, 6], double_p=0.2),
            clap=dict(modes=[["club", 1.0]], ghosts=[0, 1],
                      gcells=[3, 15]),
            snare=dict(modes=[["club", 0.6], ["backbeat", 0.4]],
                       ghosts=[0, 1], gcells=[3, 15]),
            hat=dict(modes=[["sixteenths", 0.3], ["shuffle", 0.25],
                            ["offbeats", 0.25], ["eighths", 0.2]],
                     open_p=0.12),
        ),
        kick_flavors=[[0.1, "808", ["punch"], [0.2, 0.4]],
                      [0.9, None, ["punch", "tight", "club", "knock"],
                       [0.12, 0.32]]],
        library=dict(p=0.1, tags=[["breakbeat", 3], ["house", 2],
                                  ["garage", 1]]),
        extras=dict(p=0.8, nmax=2, pool=[
            ["fx", ["stab", "shout", "vocal"], "cutfx"],
            ["perc", ["tamb", "cowbell"], "tamb"],
            ["crash", ["crash"], "crash2"]]),
    ),
    "Miami Bass": dict(
        num=33, bpm=138, era="genre", built="Miami bass — 2 Live Crew, "
        "Magic Mike, the 808 electro lineage",
        genre=True, genre_swing=50, density="busy",
        listen=("Planet Rock's grandchild: an electro kick figure with a "
                "long decaying 808 filling every gap, driving 16th hats "
                "with the offbeats cracked open, handclaps hard on 2 and "
                "4, cowbell riding through. Bright, fast, and clean"),
        canon=dict(kick=ELECTRO_KICK),
        kit=dict(
            kick=("kick", None, ["808", "sub", "long"], (0.7, 1.3)),
            clap=("clap", None, ["clap", "big"], 1.0),
            snare=("snare", None, ["tight", "crack"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.24),
            perc=("perc", None, ["cowbell"], 0.5),
            stamp=("fx", None, ["vocal", "zap", "laser"], 0.7),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 2311), _BK),
            clap=(0.0, 0.86, (0, 1, 50, 2312), _BK),
            snare=(0.08, 0.6, (0, 1, 50, 2313), _BK),
            hat=(-0.13, 0.38, (0, 1, 50, 2314), _H8),
            perc=(0.2, 0.3, (0, 2, 50, 2315), _H8),
            stamp=(-0.28, 0.4, (0, 1, 50, 2316), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.15,
        space=("dry", ["clap"]), alt=None,
        drive=1.5, kick_dist=0.05, mix_sat=0.12,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 6, 1, 1, 6, 1, 4, 1, 5, 1, 6, 1, 3, 2],
                      hits=[4, 6], double_p=0.25),
            clap=dict(modes=[["backbeat", 0.85], ["stomp", 0.15]],
                      ghosts=[0, 1], gcells=[7, 15]),
            snare=dict(copy="clap"),
            hat=dict(modes=[["drive16", 0.4], ["sixteenths", 0.3],
                            ["offbeats", 0.2], ["eighths", 0.1]],
                     open_p=0.16),
            perc=dict(modes=[["offbeats", 0.4], ["eighths", 0.35],
                             ["sixteenths", 0.25]]),
        ),
        kick_flavors=[[0.8, "808", ["sub", "long", "deep"], [0.9, 1.5]],
                      [0.2, None, ["punch", "tight"], [0.2, 0.45]]],
        library=dict(p=0.15, tags=[["electro", 3], ["disco", 1],
                                   ["house", 1]]),
        extras=dict(p=0.8, nmax=2, pool=[
            ["perc", ["cowbell"], "cowbell"],
            ["fx", ["zap", "laser"], "blips"],
            ["crash", ["crash"], "crash2"]]),
    ),
    "New Orleans Bounce": dict(
        num=34, bpm=100, era="genre", built="NO bounce — the Triggerman / "
        "Drag Rap lineage",
        genre=True, genre_swing=54, density="busy",
        listen=("call and response at 100: a tambourine running 16ths "
                "without stopping, the snare answering itself with that "
                "stuttered double at the top of 4, and a busy syncopated "
                "kick underneath. Everything is talking at once"),
        canon=dict(snare=BOUNCE_SNARE),
        kit=dict(
            kick=("kick", None, ["punch", "boom", "knock"], (0.2, 0.5)),
            snare=("snare", None, ["tight", "crack", "snappy"], 1.0),
            perc=("perc", None, ["tamb"], 0.4),
            hat=("hat", None, ["closed", "tight"], 0.3),
            stamp=("fx", None, ["vocal", "shout", "whistle"], 0.8),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 54, 2321), _BK),
            snare=(0.0, 0.88, (0, 1, 54, 2322), _BK),
            perc=(0.16, 0.4, (0, 2, 54, 2323), _H8),
            hat=(-0.14, 0.3, (0, 2, 54, 2324), _H8),
            stamp=(-0.28, 0.42, (0, 1, 54, 2325), _stamp_tail()),
        ),
        dust=0.1, vinyl=-54, wow=0.0, sidechain=0.2,
        space=("dry", ["snare"]), alt=None,
        drive=1.5, kick_dist=0.06, mix_sat=0.12,
        grammar=dict(
            kick=dict(w=[10, 1, 3, 6, 1, 2, 6, 3, 6, 2, 5, 4, 2, 3, 4, 2],
                      hits=[4, 7], double_p=0.4),
            snare=dict(modes=[["bounce", 1.0]], ghosts=[0, 2],
                       gcells=[3, 10, 11]),
            perc=dict(modes=[["sixteenths", 0.45], ["shuffle", 0.3],
                             ["drive16", 0.25]]),
            hat=dict(modes=[["offbeats", 0.35], ["shuffle", 0.3],
                            ["eighths", 0.2], ["sparse", 0.15]],
                     open_p=0.1),
        ),
        kick_flavors=[[0.2, "808", ["deep", "punch"], [0.4, 0.8]],
                      [0.8, None, ["punch", "boom", "knock"], [0.2, 0.5]]],
        library=dict(p=0.15, tags=[["breakbeat", 3], ["funk", 2],
                                   ["electro", 1]]),
        extras=dict(p=0.85, nmax=2, pool=[
            ["perc", ["tamb"], "tamb"],
            ["fx", ["shout", "whistle", "vocal"], "cutfx"],
            ["bongo", ["conga"], "congas2"]]),
    ),
    # ================================================ the west + latin
    "G-Funk": dict(
        num=35, bpm=94, era="genre", built="DJ Quik / Warren G / Above "
        "the Law (NOT Doc Day's surgical Dre pocket)",
        genre=True, genre_swing=56, density="home",
        listen=("the bouncier, looser West Coast: a deep round kick "
                "leaning back, a crisp snare planted on 2 and 4, "
                "tambourine and shaker keeping 16ths, 56% swing rolling "
                "it forward. Warm, clean, and unhurried"),
        kit=dict(
            kick=("kick", None, ["deep", "round", "punch"], (0.25, 0.6)),
            snare=("snare", None, ["crack", "tight", "snappy"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.4),
            perc=("perc", None, ["tamb", "shaker"], 0.6),
            stamp=("fx", None, ["vocal", "talkbox", "scratch"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 56, 2331), _BK),
            snare=(0.0, 0.88, (0, 2, 56, 2332), _BK),
            hat=(-0.15, 0.36, (0, 2, 56, 2333), _H8),
            perc=(0.18, 0.3, (0, 2, 56, 2334), _H8),
            stamp=(-0.28, 0.38, (0, 2, 56, 2335), _stamp_tail()),
        ),
        dust=0.05, vinyl=-56, wow=0.0, sidechain=0.18,
        space=("room", ["snare"]), alt=None,
        drive=1.4, kick_dist=0.0, mix_sat=0.08,
        grammar=dict(
            kick=dict(w=[10, 1, 3, 5, 2, 2, 5, 3, 5, 2, 5, 3, 2, 3, 4, 2],
                      hits=[3, 6], double_p=0.35),
            snare=dict(modes=[["backbeat", 0.85], ["displaced", 0.1],
                              ["sparse", 0.05]],
                       ghosts=[0, 2], gcells=[3, 7, 11, 15]),
            hat=dict(modes=[["eighths", 0.35], ["sixteenths", 0.3],
                            ["offbeats", 0.2], ["broken", 0.15]],
                     open_p=0.1),
            perc=dict(modes=[["sixteenths", 0.35], ["offbeats", 0.35],
                             ["eighths", 0.3]]),
        ),
        kick_flavors=[[0.25, "808", ["deep", "sub"], [0.5, 1.0]],
                      [0.75, None, ["deep", "round", "punch"],
                       [0.25, 0.6]]],
        library=dict(p=0.4, tags=[["funk", 3], ["motown", 2],
                                  ["soul", 2], ["rnb", 1]]),
        extras=dict(p=0.7, nmax=2, pool=[
            ["perc", ["tamb"], "tamb"],
            ["perc", ["shaker"], "shaker"],
            ["perc", ["cowbell"], "cowbell"],
            ["rim", ["rim", "stick"], "rims"]]),
    ),
    "Reggaeton Alt": dict(
        num=36, bpm=92, era="genre", built="alternative reggaeton — the "
        "Tainy / experimental end of the dembow",
        genre=True, genre_swing=50, density="home",
        listen=("the dembow, played dark: kick on 1 and 3, the snare "
                "answering with the tresillo cell — boom, ch-ch, boom, "
                "ch-ch — timbale and conga colors around it, and an "
                "airier, moodier treatment than the radio version"),
        canon=dict(snare=DEMBOW_SNARE, kick=DEMBOW_KICK),
        kit=dict(
            kick=("kick", None, ["deep", "round", "sub"], (0.3, 0.7)),
            snare=("snare", None, ["tight", "rim", "snappy"], 1.0),
            bongo=("bongo", None, ["conga", "bongo"], 0.6),
            perc=("perc", None, ["timbale", "clave", "shaker"], 0.6),
            hat=("hat", None, ["closed", "tight"], 0.3),
            stamp=("fx", None, ["vocal", "reverse", "noise"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 2341), _BK),
            snare=(0.0, 0.86, (0, 1, 50, 2342), _BK),
            bongo=(0.22, 0.3, (0, 2, 50, 2343), _H8),
            perc=(-0.18, 0.28, (0, 2, 50, 2344), _H8),
            hat=(0.12, 0.3, (0, 2, 50, 2345), _H8),
            stamp=(-0.3, 0.36, (0, 1, 50, 2346), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.08, sidechain=0.2,
        space=("plate", ["snare"]), alt=None,
        drive=1.4, kick_dist=0.05, mix_sat=0.12,
        grammar=dict(
            kick=dict(w=[10, 1, 1, 2, 1, 1, 3, 1, 8, 1, 2, 2, 2, 1, 3, 1],
                      hits=[2, 4], double_p=0.2),
            snare=dict(modes=[["dembow", 1.0]], ghosts=[0, 1],
                       gcells=[8, 15]),
            bongo=dict(modes=[["offbeats", 0.4], ["broken", 0.3],
                              ["sparse", 0.3]]),
            perc=dict(modes=[["offbeats", 0.35], ["sparse", 0.35],
                             ["sixteenths", 0.3]]),
            hat=dict(modes=[["sparse", 0.35], ["offbeats", 0.3],
                            ["eighths", 0.2], ["sixteenths", 0.15]],
                     open_p=0.1),
        ),
        kick_flavors=[[0.45, "808", ["sub", "deep"], [0.5, 1.0]],
                      [0.55, None, ["deep", "round", "punch"],
                       [0.28, 0.6]]],
        library=dict(p=0.1, tags=[["reggae", 3], ["minimal", 1]]),
        extras=dict(p=0.75, nmax=2, pool=[
            ["perc", ["timbale"], "timbales"],
            ["bongo", ["conga"], "congas2"],
            ["perc", ["clave", "block"], "woods"],
            ["fx", ["reverse", "noise"], "cutfx"]]),
    ),
    # ================================================ the remaining two
    "Detroit": dict(
        num=37, bpm=93, era="genre", built="post-Dilla Detroit — Black "
        "Milk, Apollo Brown, Danny Brown's harder side (NOT the drunk "
        "swing Otto Grit and J Dillo already hold)",
        genre=True, genre_swing=55, density="home",
        listen=("Detroit with the swing straightened out and the grit "
                "left in: a hard dusty kick hitting square, a crunchy "
                "loud snare, driving 16th hats, and a forward push where "
                "the Dilla lane would drag"),
        kit=dict(
            kick=("kick", None, ["boom", "hard", "dusty"], (0.25, 0.55)),
            snare=("snare", None, ["crack", "crunch", "dusty"], 1.0),
            hat=("hat", None, ["closed", "tight"], 0.35),
            perc=("perc", None, ["shaker", "tamb"], 0.6),
            stamp=("fx", None, ["scratch", "vocal", "horn"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 2, 55, 2351), _BK),
            snare=(0.0, 0.9, (0, 2, 55, 2352), _BK),
            hat=(-0.16, 0.36, (0, 2, 55, 2353), _H8),
            perc=(0.18, 0.28, (0, 2, 55, 2354), _H8),
            stamp=(-0.3, 0.4, (0, 2, 55, 2355), _stamp_tail()),
        ),
        dust=0.45, vinyl=-46, wow=0.08, sidechain=0.15,
        space=("gated", ["snare"]), alt=None,
        drive=1.5, kick_dist=0.1, mix_sat=0.18,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 5, 2, 1, 5, 3, 6, 1, 4, 3, 2, 2, 4, 1],
                      hits=[3, 6], double_p=0.35),
            snare=dict(modes=[["backbeat", 0.8], ["displaced", 0.1],
                              ["sparse", 0.1]],
                       ghosts=[1, 2], gcells=[3, 7, 11, 15]),
            hat=dict(modes=[["sixteenths", 0.35], ["eighths", 0.25],
                            ["broken", 0.25], ["offbeats", 0.15]],
                     open_p=0.1),
            perc=dict(modes=[["offbeats", 0.4], ["sixteenths", 0.3],
                             ["sparse", 0.3]]),
        ),
        kick_flavors=[[0.2, "808", ["deep", "boom"], [0.45, 0.85]],
                      [0.8, None, ["boom", "hard", "dusty", "knock"],
                       [0.22, 0.55]]],
        library=dict(p=0.4, tags=[["boom-bap", 3], ["funk", 2],
                                  ["lofi", 2]]),
        extras=dict(p=0.65, nmax=2, pool=[
            ["perc", ["shaker", "tamb"], "shaker"],
            ["rim", ["rim", "stick"], "rims"],
            ["fx", ["scratch", "vocal"], "cutfx"]]),
    ),
    "Plug": dict(
        num=38, bpm=140, era="genre", built="plugg / pluggnb — MexikoDro, "
        "Kankan, the soft end of trap",
        genre=True, genre_swing=50, density="sparse",
        listen=("trap with all the aggression removed: a soft rounded "
                "808 that never distorts, airy hats drifting in and out "
                "with the occasional triplet roll, a light clap on 3, "
                "and a lot of empty dreamy space around it"),
        kit=dict(
            kick=("kick", None, ["808", "soft", "round", "sub"],
                  (0.5, 1.0)),
            clap=("clap", None, ["clap", "soft", "light"], 1.0),
            snare=("snare", None, ["soft", "tight"], 1.0),
            hat=("hat", None, ["closed", "light", "airy"], 0.25),
            stamp=("fx", None, ["vocal", "bell", "chime"], 1.0),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 2361), _BK),
            clap=(0.0, 0.78, (0, 1, 50, 2362), _BK),
            snare=(0.08, 0.55, (0, 1, 50, 2363), _BK),
            hat=(-0.12, 0.3, (0, 2, 50, 2364), _H8),
            stamp=(-0.26, 0.32, (0, 1, 50, 2365), _stamp_tail()),
        ),
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.28,
        space=("washed", ["clap"]), alt=None,
        drive=1.25, kick_dist=0.0, mix_sat=0.05,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 4, 1, 1, 4, 2, 6, 1, 3, 3, 2, 2, 3, 1],
                      hits=[2, 5], double_p=0.3),
            clap=dict(modes=[["halftime", 0.65], ["backbeat", 0.25],
                             ["sparse", 0.1]],
                      ghosts=[0, 1], gcells=[7, 15]),
            snare=dict(copy="clap"),
            hat=dict(modes=[["sparse", 0.35], ["eighths", 0.25],
                            ["trip_rolls", 0.2], ["sixteenths", 0.2]],
                     open_p=0.08, roll_n=[1, 2]),
        ),
        kick_flavors=[[0.7, "808", ["soft", "round", "sub"], [0.7, 1.3]],
                      [0.3, None, ["round", "soft", "warm"], [0.3, 0.6]]],
        library=dict(p=0.2, tags=[["cloud-rap", 3], ["trap", 2],
                                  ["minimal", 2]]),
        extras=dict(p=0.5, nmax=1, pool=[
            ["perc", ["bell", "chime"], "bells"],
            ["fx", ["vocal", "reverse"], "cutfx"]]),
    ),
    # Owner request 2026-07-24: "I like video game sounds, like, from
    # Atari and early Nintendo." The 18th style, and the only one whose
    # harmony voice is SYNTHESIZED — see tools/chip_synth.py for why that
    # is a sanctioned exception rather than a backslide.
    #
    # Deliberate hybrid, stated so nobody 'fixes' it later: the CHORDS are
    # chip (arpeggio-fused pulse, the real NES gesture) but the DRUMS come
    # from his own sample packs, leaning tight/electronic/lo-fi. Reasons:
    # the drum lanes are a sample-pool system and rebuilding them around
    # synthesized noise would be a much larger change; and chiptune-
    # influenced hip hop genuinely uses modern drums under chip melodies,
    # so this is a musical choice, not only a cheap one. chip_synth does
    # provide chip_kick/chip_snare/chip_hat if a pure-hardware drum lane
    # is ever wanted — that is the upgrade path.
    "Chiptune": dict(
        num=39, bpm=126, era="genre",
        built="NES / Atari 2600 chip music — square leads, noise drums",
        genre=True, genre_swing=50, density="home",
        listen=("8-bit game music: a bubbling square-wave arpeggio "
                "standing in for chords the way the NES faked them, "
                "thin bright bleeps, tight dry drums with no reverb, "
                "and nothing smooth anywhere"),
        kit=dict(
            kick=("kick", None, ["punch", "tight", "electronic"], (0.4, 0.8)),
            snare=("snare", None, ["tight", "electronic", "clap"], 1.0),
            hat=("hat", None, ["closed", "tight", "bright"], 0.22),
            perc=("perc", None, ["blip", "block", "click"], 0.5),
            stamp=("fx", None, ["laser", "blip", "bleep", "arcade"], 0.9),
        ),
        lanes=dict(
            kick=(0.0, 1.0, (0, 1, 50, 2371), _BK),
            snare=(0.0, 0.82, (0, 1, 50, 2372), _BK),
            hat=(-0.1, 0.3, (0, 2, 50, 2373), _H8),
            perc=(0.16, 0.28, (0, 2, 50, 2374), _H8),
            stamp=(-0.24, 0.34, (0, 1, 50, 2375), _stamp_tail()),
        ),
        # bone dry on purpose: the hardware had no reverb, no filter, and
        # the dryness is a big part of why chip music sounds like that.
        dust=0.0, vinyl=0, wow=0.0, sidechain=0.12,
        space=("dry", ["snare"]), alt=None,
        drive=1.1, kick_dist=0.0, mix_sat=0.0,
        grammar=dict(
            kick=dict(w=[10, 1, 2, 4, 1, 1, 5, 2, 7, 1, 3, 3, 2, 2, 4, 1],
                      hits=[2, 4], double_p=0.25),
            snare=dict(modes=[["backbeat", 0.7], ["halftime", 0.2],
                              ["sparse", 0.1]],
                       ghosts=[0, 1], gcells=[7, 15]),
            hat=dict(modes=[["eighths", 0.4], ["sixteenths", 0.35],
                            ["sparse", 0.25]],
                     open_p=0.05, roll_n=[1, 2]),
            perc=dict(modes=[["sparse", 0.6], ["eighths", 0.4]]),
        ),
        kick_flavors=[[0.6, None, ["punch", "tight", "electronic"], [0.3, 0.6]],
                      [0.4, "808", ["punch", "short"], [0.4, 0.8]]],
        library=dict(p=0.15, tags=[["electronic", 3], ["minimal", 2]]),
        extras=dict(p=0.45, nmax=1, pool=[
            ["perc", ["blip", "block"], "blips"],
            ["fx", ["laser", "arcade"], "gamefx"]]),
    ),
}


# ------------------------------------------- their kick books
# Only the styles WITHOUT a canon kick need a bank; the canon styles
# (Baltimore Club, Miami Bass, Reggaeton Alt) place their figure
# directly and never draw from here.

GENRE_KICK_BANK = {
    "Memphis": [
        "X-------X--x----", "X-------X-x-----", "X-----x-X-------",
        "X--x----X--x----", "X-------X----x--", "X-x-----X--x----",
        "X-----x-X----x--", "X-------X-x---x-", "X--x----X-------",
        "X----x--X--x----", "X-------Xx------", "X--x--x-X-------"],
    "Crunk": [
        "X-------X-------", "X-------X-----x-", "X-----x-X-------",
        "X-------X---x---", "X--x----X-------", "X-------X-x-----",
        "X-----x-X-----x-", "X-------X--x----", "Xx------X-------",
        "X-------X----x--", "X---x---X-------", "X--x----X--x----"],
    "Organized Noize": [
        "X--x--x---X-----", "X-----x---X--x--", "X--x------X-x---",
        "X---x-x---X-----", "X--x--x---X--x--", "X-x---x---X-----",
        "X-----x-X-X-----", "X--x---x--X--x--", "X----x----X-x---",
        "X--x--x---X---x-", "X-----x---X-x-x-", "X--xx-----X--x--"],
    "Houston Screw": [
        "X-------X-------", "X-----------X---", "X-------X---x---",
        "X-----x---------", "X-------X-----x-", "X---------X-----",
        "X-------X-x-----", "X-----x-X-------", "X-----------x---",
        "X--x----X-------", "X-------X----x--", "X----x------X---"],
    "Emo Hip Hop": [
        "X-------X--x----", "X-------X-------", "X-----x-X-------",
        "X-------X---x---", "X--x----X--x----", "X-------X-x---x-",
        "X-----x-X-----x-", "X-------X----x--", "X--x----X-------",
        "X---x---X-------", "X-------Xx--x---", "X-x-----X--x----"],
    "Acid Rap Detroit": [
        "X--x------X-----", "X-----x---X--x--", "X--x---x--X-----",
        "X---x-----X-x---", "X-----x---X---x-", "X--x--x---X-----",
        "X-x-------X--x--", "X-----x-x-X-----", "X--x------X-x---",
        "X----x----X--x--", "X------x--X-----", "X--xx-----X-----"],
    "Acid Rap Bright": [
        "X--x--x---X-----", "X-----x---X--x--", "X--x------X--x--",
        "X---x-x---X-----", "X--x--x---X--x--", "X-x---x---X-x---",
        "X-----x---X---x-", "X--x---x--X--x--", "X----x----X-x---",
        "X--x--x-X-X-----", "X-----xx--X-----", "X--x----X-X--x--"],
    "Horror Rap": [
        "X--x------X-----", "X-----x---X-----", "X--x---x--X--x--",
        "X---------X-x---", "X-----x---X--x--", "X--x------X---x-",
        "X-x-------X-----", "X----x----X-----", "X------x--X--x--",
        "X--x--x---X-----", "X---------X--x--", "X-----x-x-X-----"],
    "Wonky": [
        "X-----x---X--x--", "X--x------X-x---", "X----x----X---x-",
        "X------x-X---x--", "X-x----x--X--x--", "X---x-----Xx--x-",
        "X-----xx--X----x", "X--x---x--X-x---", "X------x--X--xx-",
        "X-x---x---X---x-", "X----x--x-X--x--", "X--x-x----X---x-"],
    "Trip Hop": [
        "X-------X-------", "X-------X---x---", "X-----x---X-----",
        "X-------X-----x-", "X--x------X-----", "X---------X-x---",
        "X-----x-X-------", "X-------X-x-----", "X--x----X-------",
        "X----x----X-----", "X-------X----x--", "X------x--X-----"],
    "New Orleans Bounce": [
        "X--x--x-X-x---x-", "X--x--x---X--x--", "X--x----X-x---x-",
        "X--x--x-X-----x-", "X-x---x-X-x-----", "X--x--x---X-x-x-",
        "X-----x-X-x---x-", "X--x-x--X-x---x-", "X--x--x-X--x--x-",
        "X-x---x---X--x-x", "X--x--x-X-------", "X--x--xxX-x---x-"],
    "G-Funk": [
        "X------x--X-----", "X--x------X--x--", "X------x-XX-----",
        "X---x-----X--x--", "X------x--X-x---", "X--x---x--X-----",
        "X-----x---X---x-", "X------x--X--x-x", "X--x------X-x---",
        "X---x--x--X-----", "X------x-xX-----", "X-x----x--X--x--"],
    "Detroit": [
        "X--x----X-X-----", "X--x--x---X-----", "X-----x---X--x--",
        "X--x----X-X---x-", "X--x--x-X-------", "X------xX-X-----",
        "X--x------X-x---", "X--x--xxX-X-----", "X-----x-X-X--x--",
        "X--x--x---X---x-", "X-x---x-X-X-----", "X--x----X-X-x---"],
    "Plug": [
        "X-------X-------", "X-------X--x----", "X-----x-X-------",
        "X-------X---x---", "X--x----X-------", "X-------X-x-----",
        "X-----x-X----x--", "X-------X-----x-", "X---------X-----",
        "X--x----X--x----", "X-------X----x--", "X-x-----X-------"],
    "Chiptune": [
        "X-------X-------", "X-------X--x----", "X--x----X-------",
        "X-------X-x-----", "X-----x-X-------", "X-------X---x---",
        "X--x----X--x----", "X-x-----X-x-----", "X-------X-----x-",
        "X---x---X-------", "X-------Xx------", "X--x--x-X-------"],
}

# ------------------------------------------------- their beat titles
# Two-word banks in each style's voice (beat_machine merges these into
# TITLES); the runtime picker keeps titles globally unique.

GENRE_TITLES = {
    "Memphis": (["Smoked", "Tomb", "Candle", "Hollow", "Bluff", "Cypress",
                 "Mask", "Ashen"],
                ["Ritual", "Chapter", "Warning", "Verse", "Prowl",
                 "Sermon", "Curfew", "Vigil"]),
    "Crunk": (["Stadium", "Rowdy", "Blackout", "Riot", "Sweat", "Reckless",
               "Neon", "Packed"],
              ["Chant", "Stomp", "Callout", "Uproar", "Anthem", "Surge",
               "Holler", "Slam"]),
    "Organized Noize": (["Dungeon", "Peachtree", "Clay", "Southern",
                         "Porch", "Magnolia", "Humid", "Gilded"],
                        ["Sermon", "Family", "Parable", "Homecoming",
                         "Gathering", "Testimony", "Reunion", "Hymnal"]),
    "Houston Screw": (["Syrup", "Molasses", "Chrome", "Candy", "Slab",
                       "Amber", "Drowsy", "Velvet"],
                      ["Crawl", "Drift", "Lean", "Haze", "Sinker",
                       "Undertow", "Sag", "Nightfall"]),
    "Emo Hip Hop": (["Bruised", "Rainy", "Faded", "Hollow", "Static",
                     "Pale", "Torn", "Distant"],
                    ["Confession", "Goodbye", "Letter", "Bedroom",
                     "Ache", "Ceiling", "Voicemail", "Bruise"]),
    "Acid Rap Detroit": (["Rusted", "Boiler", "Hex", "Cellar", "Scarlet",
                          "Feral", "Wretched", "Static"],
                         ["Gospel", "Delirium", "Sermon", "Trespass",
                          "Fever", "Nightmare", "Reckoning", "Bootleg"]),
    "Acid Rap Bright": (["Sunlit", "Kite", "Lemon", "Chalk", "Recess",
                         "Sidewalk", "Choir", "Golden"],
                        ["Parade", "Skip", "Blessing", "Cartwheel",
                         "Chorus", "Homeroom", "Daydream", "Jubilee"]),
    "Horror Rap": (["Crypt", "Grave", "Lantern", "Ashen", "Rotten",
                    "Midnight", "Cobweb", "Buried"],
                   ["Elegy", "Sermon", "Requiem", "Procession", "Omen",
                    "Ritual", "Epitaph", "Wake"]),
    "Wonky": (["Melted", "Tilted", "Rubber", "Liquid", "Bent", "Warped",
               "Sideways", "Drowsy"],
              ["Lurch", "Wobble", "Slouch", "Smear", "Stumble", "Sway",
               "Puddle", "Slippage"]),
    "Trip Hop": (["Overcast", "Harbour", "Smoke", "Concrete", "Cold",
                  "Distant", "Grey", "Hollow"],
                 ["Undertow", "Signal", "Corridor", "Lament", "Drift",
                  "Interior", "Static", "Vespers"]),
    "Baltimore Club": (["Rowhouse", "Harbor", "Crabcake", "Charm",
                        "Pratt", "Eastside", "Marquee", "Blockparty"],
                       ["Eightcount", "Workout", "Shakedown", "Rollcall",
                        "Sweatbox", "Drill", "Stomp", "Callback"]),
    "Miami Bass": (["Ocean", "Chrome", "Neon", "Palm", "Convertible",
                    "Sunburn", "Boombox", "Causeway"],
                   ["Booster", "Quake", "Rattle", "Cruise", "Frequency",
                    "Trunk", "Blast", "Sunset"]),
    "New Orleans Bounce": (["Bayou", "Ward", "Parade", "Praline",
                            "Levee", "Brass", "Humid", "Frenchmen"],
                           ["Callback", "Secondline", "Shoutout", "Twirl",
                            "Response", "Rollcall", "Wobble", "Holler"]),
    "G-Funk": (["Lowrider", "Sunroof", "Boulevard", "Poolside", "Chrome",
                "Palmshade", "Westside", "Tinted"],
               ["Glide", "Cruise", "Bounce", "Whine", "Sundown",
                "Coastline", "Rollout", "Breeze"]),
    "Reggaeton Alt": (["Marea", "Neon", "Coastal", "Humid", "Violet",
                       "Salt", "Tidal", "Nocturne"],
                      ["Dembow", "Current", "Undertow", "Pulse", "Tide",
                       "Nightswim", "Signal", "Drift"]),
    "Detroit": (["Foundry", "Belt", "Boiler", "Brick", "Motor", "Iron",
                 "Furnace", "Eastside"],
                ["Grind", "Shift", "Overtime", "Assembly", "Hardhat",
                 "Clockout", "Forge", "Payday"]),
    "Plug": (["Cotton", "Cloudy", "Pastel", "Drowsy", "Marshmallow",
              "Lilac", "Soft", "Hazy"],
             ["Drift", "Pillow", "Lullaby", "Float", "Daydream",
              "Slumber", "Cushion", "Vapor"]),
    "Chiptune": (["Pixel", "Arcade", "Cartridge", "Sprite", "Neon",
                  "Copper", "Palette", "Console"],
                 ["Continue", "Warpzone", "Highscore", "Bonus", "Extralife",
                  "Gameover", "Levelup", "Checkpoint"]),
}

# ------------------------------------------------------- harmony identity
# Owner directive 2026-07-24 ("tighten up the genres"), web-researched per
# style at his explicit request.
#
# The gap this closes, measured before writing any of it: every one of the
# 17 styles produced BYTE-IDENTICAL harmony — same random root from the
# same list, same distribution, always minor, always the loop voice. A
# Horror Rap beat and a Plug beat were harmonically twins. The drum layer
# was already well differentiated (own bpm/density/pinned swing/kick
# flavors); harmony was the whole gap.
#
# READ THIS BEFORE EDITING `mode` HERE: mode does NOT change chord
# qualities (verified 2026-07-23, DECISIONS). progressions_config.json
# fixes each chord's quality absolutely; the key only supplies the root.
# So a style's harmonic character lives ENTIRELY in `progressions` — mode
# only sets the printed label and which melodic loops count as in-key
# (which is real, so it's still set honestly). If a style needs a colour
# the library can't spell, add a progression; don't flip mode and hope.
#
# chord_source words map through instrument_sampler.VOICES to his own
# sampled banks (piano/guitar/organ/bell/brass/...). Before 2026-07-23
# only "loop"/"synth"/"strings" existed, so these voicings were not
# expressible at all.
GENRE_SIGNATURES = {
    # Three 6 Mafia / DJ Paul. Sources describe "sinister church organs
    # with 808s", choir stabs pitched into minor keys, horror-score
    # samples. dark_menacing IS i-bII — the Phrygian b2 that gives the
    # style its dread — and vamp_static_riff is the drone the pitched-808
    # carries the melody over.
    "Memphis": dict(
        key=dict(roots=[["C", 3], ["D", 2], ["F", 2], ["G", 1]], mode="minor"),
        progressions=[["dark_menacing", 4], ["vamp_static_riff", 3],
                      ["vamp_i_VI", 2]],
        chord_source=[["organ", 3], ["loop", 2]],
        chord_rhythm=[["sustain", 3], ["arp", 1]]),

    # Gravediggaz/Esham lineage. Sources: minor keys, slow-to-mid tempo,
    # sampled pipe organs, church choirs and DISSONANT strings. Nothing
    # in the library was actually dissonant, hence horror_tritone.
    "Horror Rap": dict(
        key=dict(roots=[["C", 2], ["D", 2], ["E", 1], ["A", 2]], mode="minor"),
        progressions=[["horror_tritone", 3], ["dark_menacing", 3],
                      ["vamp_static_riff", 2]],
        chord_source=[["organ", 3], ["strings", 2], ["loop", 1]],
        chord_rhythm="sustain"),

    # MexikoDro / BeatPluggz. Sources: electric piano carries the main
    # chords as BLOCK chords, bells and plucks are the counter-melody,
    # min7/add9 extensions for the jazzy colour, subby 808. This one
    # corrected a wrong assumption — plugg is NOT bright major.
    "Plug": dict(
        key=dict(roots=[["C", 2], ["D", 2], ["F", 2], ["A", 1]], mode="minor"),
        progressions=[["plugg_dream_9", 4], ["vamp_i_iv7", 2],
                      ["dreamy", 1]],
        chord_source=[["piano", 3], ["bell", 2]],
        chord_rhythm=[["sustain", 3], ["arp", 2]]),

    # Lil Peep / Juice WRLD lineage. Sources: "the guitar is the heartbeat
    # ... almost always a simple, minor-key melody that loops
    # hypnotically". emo_falling is the researched Cm-Fm-Bb-Ab staple;
    # sad_accepting (i-VI-III-VII) is the pop-punk cousin underneath it.
    "Emo Hip Hop": dict(
        key=dict(roots=[["C", 2], ["D", 1], ["E", 2], ["A", 2]], mode="minor"),
        progressions=[["emo_falling", 4], ["sad_accepting", 3],
                      ["trap_dark_metro", 1]],
        chord_source=[["guitar", 4], ["piano", 1]],
        chord_rhythm=[["sustain", 2], ["arp", 3]]),

    # The bright 2013 Chicago lineage — "a euphoric blur of gospel, jazz,
    # soul". The ONLY major-mode style in this batch, and the reason the
    # blanket minor default was actively wrong: it could never have
    # sounded like this. Its progressions are the genuinely major ones.
    "Acid Rap Bright": dict(
        key=dict(roots=[["C", 3], ["F", 2], ["G", 2], ["D", 1]], mode="major"),
        progressions=[["nostalgic_jazz", 3], ["uplifting", 3],
                      ["dreamy", 2], ["nostalgic_borrowed_minor", 1]],
        chord_source=[["piano", 3], ["loop", 2]],
        chord_rhythm=[["sustain", 2], ["arp", 2]]),

    # Quik / Warren G / Dre. The repo's own legend research already had
    # this: slow Dorian groove, warm and sunny, "the opposite of
    # Memphis". gfunk_dorian_9 is the bright-4 vamp that proposal asked
    # for and nobody ever added — without it G-funk collapses into plain
    # minor and stops being G-funk.
    # REWEIGHTED 2026-07-24 after the owner auditioned #1085-#1087: "G Funk
    # does not read sunnier." He was right and the roll counts showed why —
    # only 10 of 30 rolls got the Dorian bright-4; the rest were plain
    # minor, 8 of them `gfunk_minor_i_iv_v`, which is i-iv-v ALL MINOR, the
    # darkest thing in the library. That progression is also specifically
    # DRE's flavour (Still D.R.E. = Fm-Bbm-Cm) and Doc Day already owns it,
    # so it was making G-Funk both dark AND a duplicate. Dropped outright
    # rather than down-weighted: the sunny Warren G / Quik lane is what
    # this style is for. `dreamy` (Imaj7-IVmaj7) added as the warm major
    # option. Now 9 of 11 rolls land bright.
    "G-Funk": dict(
        key=dict(roots=[["C", 2], ["F", 2], ["G", 2], ["A", 1]], mode="minor"),
        progressions=[["gfunk_dorian_9", 6], ["dreamy", 2],
                      ["nostalgic_jazz", 2], ["vamp_i_VI", 1]],
        chord_source=[["synth", 3], ["loop", 2]],
        chord_rhythm=[["sustain", 3], ["arp", 1]]),
    # Game music leaned on bright, strong, simple functional harmony —
    # it had to read instantly on two voices through a TV speaker. The
    # heroic major (uplifting), the maj7 float (dreamy) and the driving
    # minor vamp (epic / vamp_i_VI) are the four colours that covers.
    # chord_source is chip alone: falling through to a sampled piano
    # would defeat the entire point of the style.
    "Chiptune": dict(
        key=dict(roots=[["C", 3], ["G", 2], ["A", 2], ["D", 1], ["F", 1]],
                 mode="major"),
        progressions=[["uplifting", 3], ["epic", 3], ["dreamy", 2],
                      ["vamp_i_VI", 2], ["sad_accepting", 1]],
        chord_source=[["chip", 1]],
        chord_rhythm="arp",
        # the whole style IS the chip voice; without this, picking
        # Chiptune and pressing go rendered drums and no chip at all
        chords_default=True),

    # Deepened batch 1, 2026-07-24 (owner: lean heavily on the Symphony
    # bank). Portishead / Massive Attack / Tricky. Research: minor, 2-4
    # chords, "one major chord in a sea of minor" = film-noir tension, the
    # unresolved bVI-bVII descending cycle, over STRINGS and Hammond organ.
    # A textbook Symphony-bank style — strings weighted 4 primary.
    "Trip Hop": dict(
        key=dict(roots=[["A", 3], ["C", 2], ["D", 2], ["E", 1]],
                 mode="minor"),
        progressions=[["noir_descend", 3], ["dark_menacing", 2],
                      ["nostalgic_borrowed_minor", 2], ["vamp_static_riff", 2]],
        chord_source=[["strings", 4], ["organ", 2], ["loop", 1]],
        chord_rhythm=[["sustain", 3], ["arp", 1]]),

    # Organized Noize / Dungeon Family (OutKast, Goodie Mob). Research:
    # LIVE instrumentation — organs, guitars, saxophones, strings — Southern
    # soul-funk, warm and organic. Leans on the Symphony strings for the
    # cinematic OutKast arrangements, with live guitar/organ as the band.
    "Organized Noize": dict(
        key=dict(roots=[["C", 2], ["F", 2], ["G", 2], ["A", 2], ["D", 1]],
                 mode=[["minor", 2], ["major", 2]]),
        progressions=[["nostalgic_jazz", 3], ["uplifting", 2],
                      ["dreamy", 2], ["vamp_i_iv7", 2]],
        chord_source=[["strings", 3], ["guitar", 2], ["organ", 2]],
        chord_rhythm=[["sustain", 2], ["arp", 2]]),
}

for _name, _sig in GENRE_SIGNATURES.items():
    GENRES_DEFAULT[_name]["signature"] = _sig

KICK_BANK.update(GENRE_KICK_BANK)


def load_genres(normalize):
    """Same contract as crew.load_crew and legends.load_legends, for
    genres_config.json. `normalize` is crew.normalize_preset (passed in
    to avoid a circular import). Style keys (grammar/kick_flavors/extras/
    library/canon) re-sync on a GENRES_VERSION bump unless "_style_lock"
    is set."""
    if not CONFIG.exists():
        doc = {"_readme": [
            "The Styles roster — seventeen subgenres. Edit a number and "
            "the next render uses it; delete the file to regenerate the "
            "built-ins. Same schema as crew_config.json, plus two keys.",
            "canon: lane -> [figure, ...] — the rhythm that DEFINES the "
            "style. These are placed verbatim and protected from the "
            "variety pass; everything else still rolls free.",
            "density: sparse | home | busy — this style's own density, "
            "honoured instead of the house sparse-bed lean (owner "
            "decision 2026-07-19: genre fidelity wins in this box).",
            "Their other rules (pinned swing, home-weighted grammar, no "
            "cross-pollination, no evolution, 4/4) live in the engine."],
            "_genres_version": GENRES_VERSION}
        doc.update(GENRES_DEFAULT)
        CONFIG.write_text(json.dumps(doc, indent=1))
    try:
        raw = json.loads(CONFIG.read_text())
        changed = False
        if raw.get("_genres_version", 0) < GENRES_VERSION \
                and not raw.get("_style_lock"):
            for n, p in raw.items():
                if not n.startswith("_") and n in GENRES_DEFAULT:
                    for k in ("grammar", "kick_flavors", "extras",
                              "library", "canon", "signature"):
                        if k in GENRES_DEFAULT[n]:
                            p[k] = GENRES_DEFAULT[n][k]
            # A brand-new built-in style has no row to re-sync, so without
            # this it would never reach anyone who already had a config —
            # which is exactly what happened when Chiptune was added
            # (2026-07-24). Only ADDS; an existing style he has edited is
            # never replaced wholesale here.
            for n, p in GENRES_DEFAULT.items():
                if n not in raw:
                    raw[n] = json.loads(json.dumps(p))
            raw["_genres_version"] = GENRES_VERSION
            changed = True
        if changed:
            CONFIG.write_text(json.dumps(raw, indent=1))
        out = {}
        for n, p in raw.items():
            if n.startswith("_"):
                continue
            p["genre"] = True                     # the flag IS the rules
            out[n] = normalize(p)
        if out:
            return out
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"WARNING: {CONFIG.name} is broken ({e}) — using the "
              "built-in styles. Fix or delete the file to silence this.")
    return {n: normalize(json.loads(json.dumps(p)))
            for n, p in GENRES_DEFAULT.items()}
