"""Ten drum-only beats built from HIS one-shot library. No melody, no bass.

Each beat is a hand-programmed kit (kick/snare-or-clap/hat + spice) chosen
from his samples by tag, sequenced with per-beat swing and velocity, then
mixed and mastered Pharrell-style: bone dry, transients intact, punchy and
loud WITHOUT the squashed brickwall sound. The "drive" knob per beat is the
whole trick — clean/poppy beats get light glue (1.15), gritty ones get
pushed (1.7) plus bit-crush/saturation on the loop.

Run:  ./.venv/bin/python tools/make_drum_beats.py
Out:  ~/Documents/Samples/Claude Drum Beats/   (+ README.txt with sources)
"""
import os
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR, bandpass, env, highpass, lowpass, master, write_wav24
from make_hiphop_tracks import edge_fade, load_audio, norm_rms

OUT_DIR = Path(os.path.expanduser("~/Documents/Samples/Claude Drum Beats"))
# Owner rule 2026-07-23: "only use samples from the folders I gave this
# session and the ones already being used." The old whole-drive list
# (["/Volumes/TBOTC 3", "~/Documents", "~/Music"]) let the name-token
# scanner reach anywhere on the drive — including his own songs. build_shots
# now sources ONLY from the pack roots in sample_packs.json (load_roots()),
# which is exactly that whitelist: the already-used packs plus wherever this
# session's folders were consolidated. Kept as a constant for back-compat.
FOLDERS = ["/Volumes/TBOTC 3", "~/Documents", "~/Music"]
rng = np.random.default_rng(2049)

# tag -> which token words identify that drum, most specific first so a
# "rimshot" lands in rim not snare, a "clap" in clap not snare, etc.
SHOT_WORDS = [
    ("crash", {"crash", "cymbal", "ride", "splash"}),
    ("clap", {"clap", "claps"}),
    ("snap", {"snap", "snaps", "finger", "fingers"}),
    ("rim", {"rim", "rimshot", "sidestick", "stick", "click"}),
    ("hat", {"hat", "hats", "hihat", "hh", "cymbal"}),
    # "boom" removed 2026-07-18: it matched a BOTC band take ("Bang boom
    # Pow lyr...") and shipped it as a kick in dozens of beats. Real kick
    # samples say kick/bd/808; song titles say boom.
    ("kick", {"kick", "kicks", "bd", "808"}),           # an 808 IS a kick
    ("snare", {"snare", "snares", "sd"}),
    ("perc", {"perc", "percussion", "conga", "bongo", "shaker", "tom",
              "toms", "tamb", "tambourine", "rim", "cowbell", "block",
              "clave", "tabla"}),
    ("bongo", {"bongo", "bongos", "conga", "congas"}),
    ("fx", {"fx", "riser", "sweep", "impact", "whoosh", "foley", "glitch",
            "laser", "zap", "scratch", "texture", "reverse", "vinyl"}),
    # phase 2 (owner 2026-07-23): bass/808 shots and vocals are their own
    # roles now, no longer skipped. 808 is deliberately in BOTH kick and
    # bass — it's a kick you can also play as the low note.
    ("bass", {"bass", "sub", "808", "reese", "bassline", "basses"}),
    ("vox", {"vox", "vocal", "vocals", "voice", "adlib", "adlibs", "chant",
             "chants", "acapella", "acappella", "choir", "phrase"}),
]


# Owner blocklist (2026-07-18): file NAMES in banned_samples.json (repo
# root) never enter the pool again, on any drive. Seeded with the "Bang
# boom Pow lyr" band take that rode as a kick through many beats.
BANNED_FILE = Path(__file__).resolve().parent.parent / "banned_samples.json"

# never sample these, whatever the tokens say: our own rendered output
# (beat 280's clap was a previously generated stem!) and BOTC band takes
BAND_TOKENS = {"botc", "tbotc", "botb", "lyr", "lyric", "lyrics"}


class BanListDamaged(RuntimeError):
    """The blocklist is on disk but unreadable. Raised, never swallowed —
    see _ban_doc."""


def _ban_doc():
    """The blocklist file, in any of its shapes. THREE kinds of ban:

      names   hand-typed SUBSTRINGS. "Bang boom Pow" takes every date and
              master variant of that band take at once. Deliberately broad;
              he types these himself.
      stems   exact file names, from the button's "ban all of them". Exact
              because the button TELLS HIM A NUMBER first, and the action
              has to ban that many and no more.
      sounds  one specific sound, by content fingerprint.

    A missing file is an empty blocklist — that is the normal first-run
    state. A file that EXISTS but will not parse raises instead, because
    returning "nothing is banned" would silently un-ban his whole curated
    list, and the next ban would then write that emptiness back over it."""
    import json
    if not BANNED_FILE.exists():
        return {"names": [], "stems": [], "sounds": []}
    try:
        raw = json.loads(BANNED_FILE.read_text())
    except (OSError, ValueError) as e:
        raise BanListDamaged(
            f"{BANNED_FILE} could not be read ({e}). Nothing has been "
            "changed. Fix or delete the file — carrying on would have "
            "un-banned every sound on it.")
    if isinstance(raw, list):                      # the original shape
        return {"names": [str(s) for s in raw], "stems": [], "sounds": []}
    return {"names": [str(s) for s in raw.get("names", [])],
            "stems": [str(s) for s in raw.get("stems", [])],
            "sounds": [s for s in raw.get("sounds", [])
                       if isinstance(s, dict)]}


def banned_substrings():
    """Owner blocklist as lowercase SUBSTRINGS. One entry "Bang boom Pow"
    bans every date/master variant of that band song at once; an exact
    filename still matches itself. Shared with quarantine_banned.py."""
    return [s.lower() for s in _ban_doc()["names"]]


def sample_fingerprint(path):
    """Identify a sound by its CONTENT, so a ban survives the file being
    moved or the pack being re-copied to a new path.

    Why this is not name-matching: measured on his own 4,202-file library,
    17.5% of samples share a file name with another file, and name+duration
    still collides on 14.5% (many entries have no duration recorded). A
    one-click ban that matched by name would have taken innocent samples
    roughly one time in five — banning "bass" alone would kill nine files.

    Size plus the first 64 KB, not the whole file: enough to separate any
    two real samples, and it reads one block instead of a whole drum loop.
    Returns None when the file cannot be read, and a None fingerprint never
    matches anything."""
    import hashlib
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as fh:
            head = fh.read(65536)
    except OSError:
        return None
    h = hashlib.sha1()
    h.update(str(size).encode())
    h.update(head)
    return h.hexdigest()


def banned_sounds(doc=None):
    """The exact-sound bans, indexed for a CHEAP filter: basename -> the
    entries banned under that name.

    Keyed on basename so `is_banned` does no I/O at all for the ~99.9% of
    the library that shares no name with a banned sound. Only a name
    collision costs a fingerprint read, which is exactly the case that
    needs one."""
    doc = _ban_doc() if doc is None else doc
    idx = {}
    for e in doc["sounds"]:
        key = str(e.get("name", "")).lower()
        if key:
            idx.setdefault(key, []).append(e)
    return idx


def banned_stems(doc=None):
    """Exact file names banned by the button's "all of them" choice."""
    doc = _ban_doc() if doc is None else doc
    return {s.lower() for s in doc["stems"]}


def is_banned(sample_name, banned=None, sounds=None, stems=None):
    """True if this sample is blocked — by a hand-typed name substring, by
    an exact file name, or because it IS one of the sounds he banned."""
    low = str(sample_name).lower()
    stem = Path(sample_name).stem.lower()
    banned = banned_substrings() if banned is None else banned
    if any(b in low for b in banned):
        return True
    # Exact, NOT a substring. The button quotes him a count before he
    # answers, so the ban has to take exactly the files that count covered:
    # appending "Hat" to the substring list would have taken every path on
    # the drive containing the letters "hat", including a folder called
    # "Kick 3" and a file called "Phat Kick".
    stems = banned_stems() if stems is None else stems
    if stem in stems:
        return True
    sounds = banned_sounds() if sounds is None else sounds
    if not sounds:
        return False
    hits = sounds.get(Path(sample_name).stem.lower())
    if not hits:
        return False
    # Same name as something he banned. Same PATH settles it for free;
    # otherwise the content decides, so a different sample that happens to
    # share the name survives.
    same = str(sample_name)
    if any(str(e.get("path", "")) == same for e in hits):
        return True
    fp = sample_fingerprint(sample_name)
    return bool(fp) and any(e.get("fp") == fp for e in hits)


def name_twins(path, shots):
    """Every sample in the pool sharing this one's file name, itself
    included. Drives the button's prompt (owner 2026-08-31, "ask me each
    time"): one twin means ban it outright, more than one means show him
    the count and let him choose."""
    stem = Path(path).stem.lower()
    seen, out = set(), []
    for entries in (shots or {}).values():
        for e in entries:
            p = e.get("path")
            if p and p not in seen and Path(p).stem.lower() == stem:
                seen.add(p)
                out.append(p)
    return sorted(out)


def ban_sound(path, whole_name=False, shots=None):
    """Ban one sound from every future beat, forever (owner 2026-08-31).

    Default bans THIS sound only, by content, so the samples that merely
    share its name are untouched. `whole_name=True` is the broad kill — it
    appends to the same hand-typed substring list his two existing entries
    live on, which is how "Bang boom Pow" takes every variant at once.

    Never touches beats already made: a ban stops the sound being picked
    again and nothing else (his call — existing beats stay put)."""
    import datetime
    import json
    import os
    import tempfile
    doc = _ban_doc()
    path = str(path)
    name = Path(path).stem
    if whole_name:
        # the EXACT-name list, not the substring list — see is_banned
        if name.lower() not in [s.lower() for s in doc["stems"]]:
            doc["stems"].append(name)
        did = "name"
    else:
        fp = sample_fingerprint(path)
        already = any(e.get("fp") == fp and fp for e in doc["sounds"])
        if not already:
            doc["sounds"].append({
                "name": name, "path": path, "fp": fp,
                "when": datetime.date.today().isoformat()})
        did = "sound"
    # Write a whole new file and swap it in. A plain write truncates first,
    # so a crash or a full disk mid-write left an unparseable blocklist —
    # which used to read back as "nothing is banned" and take his two
    # hand-typed entries with it.
    fd, tmp = tempfile.mkstemp(dir=str(BANNED_FILE.parent),
                               prefix=".banned-", suffix=".json")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(doc, fh, indent=1)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, str(BANNED_FILE))
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return {"banned": did, "name": name,
            "twins": len(name_twins(path, shots)) if shots else None}


def _clean_pool(shots):
    doc = _ban_doc()                  # read ONCE, not per sample
    banned = [s.lower() for s in doc["names"]]
    sounds = banned_sounds(doc)
    stems = banned_stems(doc)
    for role, entries in shots.items():
        shots[role] = [
            e for e in entries
            if not is_banned(e["path"], banned, sounds, stems)
            and "/Claude Drum Beats/" not in e["path"]
            and not (BAND_TOKENS
                     & set(e.get("tokens")
                           or Path(e["path"]).stem.lower().split()))]
    return shots


def build_shots():
    """Bucket every sample into roles by name tokens. A sample can land in
    several buckets (a 'rimshot' is both rim and perc) — that just gives
    each beat more to choose from. The folder-aware sample-pack scan
    (sample_library) is merged on top — that's where most of the sounds
    live.

    Owner rules 2026-07-23:
    - source ONLY from the pack roots ("only my folders"). The old
      whole-drive name-token pass (indexer.scan over "/Volumes/TBOTC 3")
      is gone: it reached his own songs AND, lacking the folder-aware
      loop/tonal tagging, flattened drum loops into the one-shot roles
      (an "808 Loop" landing in the bass pool). scan_packs over the roots
      is now the single source — same folders, but folder-aware.
    - no one-shot rule: loops and long samples are kept. Loops go to the
      "_loops" bucket (played AS full loops, a real lane); long one-shots
      stay in their role, choked to lane length at playback."""
    from sample_library import merge_into
    shots = {k: [] for k, _ in SHOT_WORDS}
    return _clean_pool(merge_into(shots))

# ------------------------------------------------------------- kit picking

def pick(shots, kind, want, max_secs, seed, must=None):
    """Grab a one-shot of `kind`. Three preference tiers, tried in order:
    1. `must` — a word that has to appear in the file name or folder path
       (how "always a real 808" is enforced),
    2. `want` — taste tags in the name ("vinyl", "clean", "reverb"),
    3. any usable candidate.
    A usable candidate loads cleanly and fits the duration cap."""
    cands = shots.get(kind, [])
    r = np.random.default_rng(seed)
    order = [cands[int(i)] for i in r.permutation(len(cands))]

    def usable(e):
        x = load_audio(e["path"])
        if x is None or len(x) / SR < 0.01:
            return None
        cap = int(max_secs * SR)
        if len(x) > cap:            # choke instead of reject — an MPC gate.
            x = x[:cap].copy()      # era decides how long a kick rings.
            fade = min(int(0.03 * SR), len(x))
            x[-fade:] *= np.linspace(1, 0, fade)[:, None]
        return norm_rms(x, -14.0)

    tiers = []
    if must:
        tiers.append((f" [{must}]",
                      lambda e: must in e["path"].lower()))
    if want:
        tiers.append(("", lambda e: any(w in e["name"].lower() for w in want)))
    tiers.append(("", lambda e: True))
    for tag, match in tiers:
        for e in order:
            if match(e):
                x = usable(e)
                if x is not None:
                    return e["name"] + tag, x
    return f"(none:{kind})", np.zeros((int(0.1 * SR), 2))

# ------------------------------------------------------------- fx

def saturate(x, amt):
    return np.tanh(x * amt) / np.tanh(amt)


def make_ir(seconds, tone_hz, predelay=0.018):
    """Synthetic stereo impulse response: decorrelated noise with an
    exponential decay, darkened to tone_hz. Small predelay keeps the dry
    transient separate from the wash — drums stay punchy under reverb."""
    r = np.random.default_rng(4242)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    decay = np.exp(-3.0 * t / seconds)
    irL = lowpass(r.normal(0, 1, n) * decay, tone_hz)
    irR = lowpass(r.normal(0, 1, n) * decay, tone_hz)
    pre = np.zeros(int(predelay * SR))
    irL, irR = np.concatenate([pre, irL]), np.concatenate([pre, irR])
    e = np.sqrt((irL ** 2 + irR ** 2).sum()) + 1e-12
    return irL / e, irR / e


def convolve(sig, ir):
    n = len(sig) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    out = np.fft.irfft(np.fft.rfft(sig, N) * np.fft.rfft(ir, N))
    return out[:len(sig)]


def crush(x, bits):
    q = 2 ** bits
    return np.round(x * q) / q


def loudness_match(L, R, target_db):
    """Set perceived loudness by RMS, then soft-clip the transients that
    poke through and trim to -0.5 dBFS peak. This decouples loudness from
    peak — so one loud crash can't drag a whole beat quiet the way plain
    peak-normalizing does. This is the Pharrell 'consistent and punchy'
    trick more than any single EQ move."""
    cur = np.sqrt(0.5 * (L ** 2 + R ** 2).mean()) + 1e-12
    g = 10 ** (target_db / 20) / cur
    ceil = 0.94
    L = np.tanh(L * g / ceil) * ceil                   # soft-clip the peaks
    R = np.tanh(R * g / ceil) * ceil
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
    return L / peak * 0.944, R / peak * 0.944


def swing_pos(step, bar_n, res, swing):
    t = int(step / res * bar_n)
    if res == 16 and step % 2:
        t += int(swing * bar_n / 16)
    return t

# ------------------------------------------------------------- sequencer

VEL = {"X": 1.0, "x": 0.7, "o": 0.45, ".": 0.26, "-": 0.0}


def seq(bar_n, bars, kit, tracks, swing, humanize):
    """tracks: list of (kit_key, pan, gain, [bar patterns]).
    Returns one stereo buffer PER role so reverb can be sent to just the
    snare (or bongo, or fx) instead of washing the whole kit."""
    n = bars * bar_n + int(1.5 * SR)
    bufs = {}
    kick_pos = []
    for key, pan, gain, barlist in tracks:
        name, snd = kit[key]
        m = snd.mean(axis=1) if snd.ndim == 2 else snd
        gl = np.cos((pan + 1) * np.pi / 4)
        gr = np.sin((pan + 1) * np.pi / 4)
        L, R = bufs.setdefault(key, (np.zeros(n), np.zeros(n)))
        for b in range(bars):
            pat = barlist[b % len(barlist)]
            res = len(pat)
            for s, ch in enumerate(pat):
                if ch == "-":
                    continue
                pos = b * bar_n + swing_pos(s, bar_n, res, swing)
                if humanize:
                    pos += int(rng.uniform(-humanize, humanize) * SR)
                v = VEL[ch] * gain * rng.uniform(0.92, 1.0)
                end = min(n, pos + len(m))
                if 0 <= pos < n:
                    L[pos:end] += m[:end - pos] * v * gl
                    R[pos:end] += m[:end - pos] * v * gr
                    if key == "kick":
                        kick_pos.append(pos)
    return bufs, kick_pos


def mixdown(bufs, verb):
    """Sum the role buffers; if verb=(decay_s, tone_hz, {role: wet}) is
    given, convolve each sent role and add its tail at the send level."""
    n = len(next(iter(bufs.values()))[0])
    L, R = np.zeros(n), np.zeros(n)
    for l, r in bufs.values():
        L += l
        R += r
    if verb:
        decay, tone, sends = verb
        irL, irR = make_ir(decay, tone)
        for key, wet in sends.items():
            if key in bufs and wet > 0:
                l, r = bufs[key]
                L += convolve(l, irL) * wet
                R += convolve(r, irR) * wet
    return L, R


def duck(L, R, kick_pos, depth, rel=0.09, loop=False):
    if depth <= 0:
        return L, R
    n = len(L)
    Ln = int(rel * 3 * SR)
    dip = 1 - depth * np.exp(-np.arange(Ln) / (rel * SR))
    g = np.ones(n + Ln)                  # room for overhang past the end
    for p in kick_pos:
        g[p:p + Ln] = np.minimum(g[p:p + Ln], dip[:min(Ln, n + Ln - p)])
    if loop:
        # a kick in the last ~270 ms keeps ducking across the seam instead
        # of snapping back to unity at the loop point
        g[:Ln] = np.minimum(g[:Ln], g[n:])
    g = g[:n]
    return L * g, R * g

# ------------------------------------------------------------- the 10 beats
# (name, bpm, style tags, bars, swing, humanize, drive, grit, tracks)
# tracks reference kit keys; want-tags steer sample choice.

B = [
    # --- hard hitting ---
    ("Anvil", 88, {"kick": ["punch", "hard", "808", "sub"],
                   "snare": ["crack", "hard", "big"], "hat": ["closed", "tight"],
                   "crash": ["crash"]}, 4, 0.0, 0.0006, 1.5, 0.0, [
        ("kick", 0.0, 1.0, ["X-----X---X-----"] * 3 + ["X-----X---X--X-x"]),
        ("snare", 0.0, 0.9, ["----X-------X---"] * 4),
        ("hat", 0.3, 0.42, ["x-x-x-x-x-x-x-x-"] * 4),
        ("crash", -0.2, 0.4, ["X---------------"] + ["-"] * 3),
    ]),
    ("Stomp Parade", 92, {"kick": ["punch", "hard", "knock"],
                          "snare": ["clap", "big", "snap"], "hat": ["open"],
                          "perc": ["tom", "perc"]}, 4, 0.02, 0.0006, 1.55, 0.0, [
        ("kick", 0.0, 1.0, ["X---X-----X-X---"] * 4),
        ("snare", 0.0, 0.92, ["----X-------X---"] * 3 + ["----X-----X-X---"]),
        ("hat", 0.28, 0.4, ["--o---o---o---o-"] * 4),
        ("perc", -0.35, 0.5, ["--------------x-"] * 3 + ["----------x-x-x-"]),
    ]),
    # --- gritty ---
    ("Dust Cellar", 90, {"kick": ["vinyl", "dusty", "lofi", "old"],
                         "snare": ["vinyl", "dusty", "rim", "lofi"],
                         "hat": ["vinyl", "dusty", "old"],
                         "perc": ["vinyl", "shaker"]}, 4, 0.08, 0.0018, 1.7, 0.55, [
        ("kick", 0.0, 1.0, ["X------x--X-----"] * 3 + ["X------x--X---x-"]),
        ("snare", 0.0, 0.85, ["----X-------X--."] * 4),
        ("hat", 0.3, 0.36, ["x-xox-x-x-xox-x-"] * 4),
        ("perc", -0.3, 0.32, ["--x---x---x---x-"] * 4),
    ]),
    ("Static Alley", 96, {"kick": ["dirty", "gritty", "crunch", "distort"],
                          "snare": ["dirty", "gritty", "noise", "trap"],
                          "hat": ["dirty", "noise"], "rim": ["rim"]}, 4, 0.05, 0.0016, 1.68, 0.7, [
        ("kick", 0.0, 1.0, ["X----X--X---X---"] * 4),
        ("snare", 0.0, 0.88, ["----X-------X---"] * 4),
        ("hat", 0.32, 0.4, ["x-x-x-xxx-x-x-xx"] * 4),
        ("rim", -0.4, 0.5, ["------x-----x---"] * 4),
    ]),
    # --- clean / poppy ---
    ("Sunroof", 100, {"kick": ["clean", "punch", "pop", "tight"],
                      "clap": ["clap", "clean", "pop"],
                      "hat": ["closed", "clean", "tight", "crisp"],
                      "snap": ["snap", "finger"]}, 4, 0.0, 0.0, 1.34, 0.0, [
        ("kick", 0.0, 1.0, ["X-------X-------"] * 3 + ["X-------X-----X-"]),
        ("clap", 0.0, 0.8, ["----X-------X---"] * 4),
        ("hat", 0.25, 0.44, ["x-x-x-x-x-x-x-x-"] * 4),
        ("snap", -0.3, 0.5, ["--------o-------"] * 4),
    ]),
    ("Bubblegum Bounce", 104, {"kick": ["clean", "pop", "tight"],
                              "clap": ["clap", "pop", "clean"],
                              "hat": ["crisp", "clean", "closed"],
                              "perc": ["shaker", "tamb"]}, 4, 0.03, 0.0, 1.34, 0.0, [
        ("kick", 0.0, 1.0, ["X-----X-X-------"] * 4),
        ("clap", 0.0, 0.82, ["----X-------X---"] * 4),
        ("hat", 0.26, 0.42, ["x-xxx-x-x-xxx-x-"] * 4),
        ("perc", -0.28, 0.4, ["--x-x-x-x-x-x-x-"] * 4),
    ]),
    ("Glass Pop", 98, {"kick": ["clean", "tight", "sub", "pop"],
                       "snare": ["clap", "clean", "rim"],
                       "hat": ["crisp", "closed"], "snap": ["snap"]}, 4, 0.0, 0.0, 1.38, 0.0, [
        ("kick", 0.0, 1.0, ["X---------X-----"] * 4),
        ("snare", 0.0, 0.82, ["----X-------X---"] * 4),
        ("hat", 0.25, 0.4, ["x-x-x-x-x-x-x-x-"] * 3 + ["x-x-x-x-x-x-xxxx"]),
        ("snap", -0.3, 0.45, ["--------------o-"] * 4),
    ]),
    # --- boom bap ---
    ("Corner Store", 90, {"kick": ["boom", "vintage", "punch"],
                          "snare": ["snare", "vintage", "crack"],
                          "hat": ["closed", "vintage"], "rim": ["rim"]}, 4, 0.09, 0.002, 1.4, 0.25, [
        ("kick", 0.0, 1.0, ["X-----x---X-----"] * 3 + ["X-----x---X-x---"]),
        ("snare", 0.0, 0.9, ["----X-------X---"] * 4),
        ("hat", 0.3, 0.38, ["x-x-x-x-x-x-x-x-"] * 4),
        ("rim", -0.4, 0.4, ["-------x--------"] * 4),
    ]),
    ("Fire Escape", 94, {"kick": ["boom", "punch", "vintage"],
                        "snare": ["snare", "big", "crack"],
                        "hat": ["open", "closed"], "perc": ["conga", "perc"]}, 4, 0.075, 0.002, 1.42, 0.3, [
        ("kick", 0.0, 1.0, ["X---x-----X--x--"] * 4),
        ("snare", 0.0, 0.9, ["----X--.----X---"] * 4),
        ("hat", 0.3, 0.4, ["x-xox-x-x-xox-x-"] * 4),
        ("perc", -0.32, 0.42, ["------x-------x-"] * 3 + ["------x---x-x-x-"]),
    ]),
    # --- experimental ---
    ("Broken Clock", 86, {"kick": ["sub", "808", "deep"],
                         "snare": ["rim", "click", "glitch", "snap"],
                         "hat": ["noise", "glitch", "closed"],
                         "perc": ["glitch", "perc", "click"]}, 4, -0.04, 0.003, 1.55, 0.4, [
        ("kick", 0.0, 1.0, ["X-----X----X----" , "X----X-----X--X-",
                            "X-----X---X-----", "X--X-----X---X--"]),
        ("snare", 0.1, 0.85, ["-----X------X---", "----X------X----",
                             "-----X----X---X-", "----X--X---X----"]),
        ("hat", 0.33, 0.36, ["x-xx-x-xx-x-xx-x", "x-x-xx-x-xx-x-xx",
                            "xx-x-x-xx-x-x-xx", "x-xxxx-x-x-xxxxx"]),
        ("perc", -0.35, 0.4, ["--x-------x---x-", "----x---x-----x-",
                             "--x---x-------x-", "x---x---x---xx--"]),
    ]),
]


# ------------------------------------------------- set 2: the era beats
# 10 more, per his notes: real 808 kick sample on every beat (musts),
# reverb experiments (verb = decay, tone, per-role sends), fx one-shots
# subbing for hats in places, bongos sparing and never loud.
# Eras: 1994 boom bap / 2000s bounce / 2010s halftime.

ROOM94 = (0.45, 3500, {"snare": 0.32, "hat": 0.10, "bongo": 0.28,
                       "rim": 0.25, "kick": 0.05})
PLATE2K = (0.9, 6500, {"snare": 0.34, "clap": 0.36, "snap": 0.22})
HALL10S = (1.8, 2800, {"clap": 0.42, "snare": 0.38, "fx": 0.5})

B2 = [
    # --- 1994 ---
    ("Stairwell 94", 92, {"_kick_secs": 0.9, "snare": ["room", "reverb", "black beauty", "vintage"],
                          "hat": ["closed", "vintage"], "rim": ["rim"],
                          "bongo": ["bongo"]},
     4, 0.09, 0.002, 1.45, 0.3, ROOM94, {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X-----x---X-----"] * 3 + ["X-----x---X--x--"]),
        ("snare", 0.0, 0.9, ["----X-------X---"] * 4),
        ("hat", 0.3, 0.38, ["x-x-x-x-x-x-x-x-"] * 4),
        ("rim", -0.35, 0.35, ["-------x--------"] * 4),
        ("bongo", 0.4, 0.28, ["--x-----------x-"] * 3 + ["--x-------x---x-"]),
    ]),
    ("Boiler Room 88", 88, {"_kick_secs": 0.9, "snare": ["reverb", "room", "dusty", "vinyl"],
                            "hat": ["closed"], "fx": ["vinyl", "noise", "texture"]},
     4, 0.08, 0.002, 1.5, 0.45, ROOM94, {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X------x--X---x-"] * 4),
        ("snare", 0.0, 0.88, ["----X-------X--."] * 4),
        # hats bars 1-2, an fx one-shot takes over the hat job bars 3-4
        ("hat", 0.3, 0.36, ["x-x-x-x-x-x-x-x-", "x-x-x-x-x-x-x-x-",
                            "-" * 16, "-" * 16]),
        ("fx", 0.32, 0.3, ["-" * 16, "-" * 16,
                           "x-x-x-x-x-x-x-x-", "x-x-x-x-x-xxx-x-"]),
    ]),
    ("Rooftop Echo", 96, {"_kick_secs": 0.9, "snare": ["reverb", "room", "snare"],
                          "hat": ["open"], "bongo": ["bongo", "conga"],
                          "rim": ["rim", "stick"]},
     4, 0.09, 0.002, 1.42, 0.25, ROOM94, {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X-----x-----X---"] * 4),
        ("snare", 0.0, 0.9, ["----X-------X---"] * 4),
        ("hat", -0.3, 0.34, ["--x---x---x---x-"] * 4),
        ("bongo", 0.42, 0.3, ["----------x---x-"] * 3 + ["------x---x-x-x-"]),
        ("rim", -0.42, 0.32, ["--------x-------"] * 4),
    ]),
    ("Dust and Bongos", 90, {"_kick_secs": 1.0, "snare": ["dusty", "vinyl", "reverb"],
                             "bongo": ["bongo"], "fx": ["shaker", "vinyl", "foley"],
                             "rim": ["rim"]},
     4, 0.085, 0.0022, 1.5, 0.35, (0.6, 3000, {"snare": 0.36, "bongo": 0.3,
                                               "fx": 0.2}), {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X-------x-X-----"] * 4),
        ("snare", 0.0, 0.88, ["--------X-------"] * 4),
        ("bongo", 0.35, 0.32, ["--x---x---x---x-"] * 3 + ["--x---x-x-x---xx"]),
        ("fx", -0.3, 0.28, ["x---x---x---x---"] * 4),
        ("rim", -0.42, 0.3, ["-----------x----"] * 4),
    ]),
    # --- 2000s ---
    ("Chrome Spinner", 100, {"_kick_secs": 1.1, "clap": ["clap"], "snap": ["snap"],
                             "hat": ["closed", "tight", "clean"]},
     4, 0.02, 0.0008, 1.5, 0.0, PLATE2K, {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X--X--X---X-----"] * 3 + ["X--X--X---X---X-"]),
        ("clap", 0.0, 0.85, ["----X-------X---"] * 4),
        ("snap", -0.25, 0.4, ["------------X---"] * 4),
        ("hat", 0.28, 0.42, ["x-x-x-x-x-x-x-x-"] * 4),
    ]),
    ("Trunk Rattle", 96, {"_kick_secs": 1.1, "snare": ["snare", "big"], "clap": ["clap"],
                          "hat": ["closed"], "fx": ["whoosh", "sweep", "riser"]},
     4, 0.03, 0.0008, 1.55, 0.15, PLATE2K, {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X-----X-X-------"] * 4),
        ("snare", 0.0, 0.85, ["----X-------X---"] * 4),
        ("clap", 0.1, 0.5, ["----x-------x---"] * 4),
        ("hat", 0.3, 0.4, ["x-x-x-x-x-x-x-x-"] * 3 + ["-" * 16]),
        ("fx", -0.3, 0.34, ["-" * 16] * 3 + ["x---x---x---x-x-"]),
    ]),
    ("Glitter Minimal", 104, {"_kick_secs": 1.1, "clap": ["clap", "clean"], "snap": ["snap"],
                              "fx": ["glitch", "click", "zap", "laser"]},
     4, 0.0, 0.0, 1.35, 0.0, PLATE2K, {"kick": "808"}, [
        # Neptunes move: NO hats at all — a weird fx one-shot keeps time
        ("kick", 0.0, 1.0, ["X-------X-X-----"] * 4),
        ("clap", 0.0, 0.85, ["----X-------X---"] * 4),
        ("fx", 0.3, 0.3, ["x--x--x--x--x--x"] * 4),
        ("snap", -0.3, 0.42, ["--------------X-"] * 4),
    ]),
    # --- 2010s (halftime feel) ---
    ("Night Drive", 140, {"clap": ["clap"], "hat": ["closed", "trap"],
                          "fx": ["sweep", "riser", "reverse"]},
     4, 0.0, 0.0, 1.5, 0.0, HALL10S, {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X-----X---X-----"] * 4),
        ("clap", 0.0, 0.85, ["--------X-------"] * 4),
        ("hat", 0.3, 0.4, ["x-x-x-x-x-x-x-x-", "x-x-x-x-xxxxx-x-",
                           "x-x-x-x-x-x-x-x-", "x-x-x-x-xxxxxxxx"]),
        ("fx", -0.32, 0.32, ["-" * 16] * 3 + ["------------x---"]),
    ]),
    ("Cloud Stomp", 132, {"clap": ["clap", "reverb"], "fx": ["texture", "foley",
                          "vinyl", "reverse"], "snap": ["snap"]},
     4, 0.0, 0.001, 1.45, 0.0, (2.2, 2400, {"clap": 0.5, "fx": 0.45,
                                            "snap": 0.3}), {"kick": "808"}, [
        # airy: fx one-shots ARE the hats here, hall on everything bright
        ("kick", 0.0, 1.0, ["X---------X-----"] * 4),
        ("clap", 0.0, 0.82, ["--------X-------"] * 4),
        ("fx", 0.3, 0.26, ["x---x---x---x---"] * 3 + ["x---x---x-x-x-x-"]),
        ("snap", -0.28, 0.36, ["------------x---"] * 4),
    ]),
    ("Money Counter", 144, {"snare": ["trap", "snare"], "clap": ["clap"],
                            "hat": ["closed", "trap"], "fx": ["laser", "zap",
                            "glitch", "scratch"]},
     4, 0.0, 0.0, 1.55, 0.0, HALL10S, {"kick": "808"}, [
        ("kick", 0.0, 1.0, ["X-----X-----X---"] * 4),
        ("snare", 0.0, 0.8, ["--------X-------"] * 4),
        ("clap", 0.1, 0.55, ["--------x-------"] * 4),
        ("hat", 0.3, 0.42, ["x-x-x-x-x-x-xxxx"] * 3
         + ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]),
        ("fx", -0.34, 0.3, ["--x-------x-----"] * 4),
    ]),
]


def build(ix, name, bpm, tags, bars, swing, human, drive, grit, tracks, pool,
          verb=None, musts=None):
    shots = pool
    musts = musts or {}
    bar_n = int(round(240 / bpm * SR))
    kit = {}
    used = []
    max_secs = {"kick": 2.2, "snare": 1.0, "clap": 1.0, "hat": 0.5,
                "rim": 0.4, "perc": 1.2, "crash": 2.5, "snap": 0.5,
                "bongo": 0.8, "fx": 1.0}   # real 808s ring long — allow it
    # era choke: "_kick_secs" in a beat's tags shortens how long its 808
    # rings (0.9 = 1994 thump, 2.2 = 2010s sustained sub)
    max_secs["kick"] = tags.get("_kick_secs", max_secs["kick"])
    for key in {t[0] for t in tracks}:
        want = tags.get(key, [])
        nm, snd = pick(shots, key, want, max_secs.get(key, 1.0),
                       seed=ix * 100 + hash(key) % 97, must=musts.get(key))
        kit[key] = (nm, snd)
        used.append(f"{key}: {nm}")
    bufs, kpos = seq(bar_n, bars, kit, tracks, swing, human)
    L, R = mixdown(bufs, verb)
    L, R = duck(L, R, kpos, depth=0.18 if grit < 0.5 else 0.10)
    if grit > 0:
        L = saturate(crush(L, 10 - int(grit * 3)), 1 + grit * 1.5)
        R = saturate(crush(R, 10 - int(grit * 3)), 1 + grit * 1.5)
        # gritty air rolloff — old-sampler top end
        L, R = lowpass(L, 15000 - grit * 4000), lowpass(R, 15000 - grit * 4000)
    # fold tail for seamless loop
    end = bars * bar_n
    tail = L[end:], R[end:]
    L, R = L[:end].copy(), R[:end].copy()
    L[:len(tail[0])] += tail[0]
    R[:len(tail[1])] += tail[1]
    # tone/glue master (mono bass, air, spectral shaping), then match
    # loudness so all ten sit together in an audition. Clean/poppy beats
    # keep a touch more headroom (quieter target) so they breathe; hard
    # and gritty beats hit the loud target.
    L, R = master(L, R, drive=drive)
    target = -10.5 if grit >= 0.5 else (-11.0 if drive >= 1.45 else -11.8)
    L, R = loudness_match(L, R, target)
    return L, R, used


SETS = {"1": (B, 1), "2": (B2, 11)}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "2"
    chosen = SETS.values() if which == "all" else [SETS[which]]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Scanning library for one-shots…")
    shots = build_shots()
    log = []
    for spec_list, offset in chosen:
        for ix, spec in enumerate(spec_list, offset):
            if len(spec) == 9:       # set 1 layout (no reverb/musts fields)
                name, bpm, tags, bars, sw, hu, dr, gr, tracks = spec
                verb = musts = None
            else:                    # set 2 layout
                (name, bpm, tags, bars, sw, hu, dr, gr,
                 verb, musts, tracks) = spec
            L, R, used = build(ix, name, bpm, tags, bars, sw, hu, dr, gr,
                               tracks, pool=shots, verb=verb, musts=musts)
            path = OUT_DIR / f"{ix:02d} {name} Drums {bpm}bpm.wav"
            write_wav24(path, L, R)
            rms = 20 * np.log10(np.sqrt(0.5 * (L ** 2 + R ** 2).mean()) + 1e-12)
            peak = 20 * np.log10(max(np.abs(L).max(), np.abs(R).max()) + 1e-12)
            print(f"  {path.name:42s} {len(L)/SR:5.2f}s  RMS {rms:5.1f}  "
                  f"peak {peak:4.1f} dBFS")
            log.append((name, bpm, used))
    lines = []
    readme = OUT_DIR / "README.txt"
    if not readme.exists():
        lines += ["Drum Beats — drums only, from YOUR one-shot library",
                  "=" * 58]
    lines.append("")
    for name, bpm, used in log:
        lines.append(f"{name} ({bpm}bpm) —")
        lines += [f"  {u}" for u in used] + [""]
    with open(readme, "a") as f:
        f.write("\n".join(lines))
    print(f"\n{len(log)} drum beats -> {OUT_DIR}")


if __name__ == "__main__":
    main()
