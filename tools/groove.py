"""The studio engine: research-backed timing, feel, and DSP for beats.

Every function implements a documented technique from the July 2026
research pass (see .claude/skills/drum-loops/references/techniques.md):
MPC swing with authentic 96-PPQ tick rounding, Dilla per-lane offsets,
structured velocity humanization, SP-1200 character, kick layering with
numeric phase verification, 808 distortion, plate/room/gated reverb,
transient shaping, vinyl/tape texture, Haas widening, Euclidean patterns,
ratchets, and a K-weighted loudness chain targeting modern beat levels.

Pure numpy, offline. Numerically testable — see tests/test_groove.py.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).parent))
from make_drum_loops import SR

# ------------------------------------------------------------ timing / feel

def mpc_swing_offset(step16, bpm, swing, tick_round=True):
    """Seconds to delay a 16th-grid step. Only EVEN-numbered 16ths (odd
    index) move — Roger Linn's definition. 50=straight, 54=loose, 58=classic
    boom bap, 62=golden era, 66.7=triplet, 75=max. Rounding to the MPC's
    96-PPQ ticks is part of the authentic feel (keep tick_round=True)."""
    if step16 % 2 == 0 or swing <= 50:
        return 0.0
    if tick_round:
        ticks = round((swing / 100 - 0.5) * 48)
        return ticks * 60.0 / (bpm * 96)
    return (swing / 100 - 0.5) * 2 * (60.0 / (bpm * 4))


class LaneFeel:
    """Dilla physics: a constant per-lane offset (the same few ms every
    bar — that's what analyses found, NOT random jitter) plus a small
    per-hit wobble re-rolled each bar. offset_ms>0 drags (late), <0 rushes."""

    def __init__(self, offset_ms=0.0, jitter_ms=4.0, swing=50.0, seed=0):
        self.offset = offset_ms / 1000.0
        self.jitter = jitter_ms / 1000.0
        self.swing = swing
        self.rng = np.random.default_rng(seed)

    def hit_time(self, bar_start_s, step16, bpm):
        t = bar_start_s + step16 * 60.0 / (bpm * 4)
        t += mpc_swing_offset(step16, bpm, self.swing)
        t += self.offset
        t += self.rng.normal(0, self.jitter / 3)   # σ ≈ jitter/3, ±jitter
        return max(t, 0.0)


# How much each kind of hit wanders in level, as a lognormal sigma in
# octaves. Owner call 2026-07-22: "add velocity variants between the
# sounds to give a more natural feel" — the old single 0.12 for every
# character was ~±0.7 dB, a whisper, so repeated hits came out almost
# identical and read as programmed. A real player is the opposite of
# uniform: accents land consistently because they're the point, while
# ghost notes are barely-controlled and vary wildly. So the spread now
# grows as the hit gets quieter.
VEL_SPREAD = {"X": 0.16, "x": 0.24, "o": 0.26, ".": 0.34}


def velocity(char, step16, wobble_rng, ghost_floor=0.26):
    """How loud one written hit plays.

    OWNER RULE 2026-08-03: "The volume variations per drum hit is not
    working out. Sometimes the drum parts get way too quiet and don't come
    back. So let's just have everything level." He chose option (a) when
    asked how far to take it: kill the RANDOMNESS, keep the WRITTEN
    dynamics. So the accent/normal/ghost characters still mean what they
    say — that is the groove, and ghost notes are most of what makes the
    Funky Drummer and the Amen read as breaks — but nothing wanders any
    more.

    What was removed: a per-hit `2 ** normal(0, sigma)` wobble. Measured
    before removing it, a single hit could land 8.0 dB from its neighbour
    on a normal hit and 17.3 dB on a ghost, with a hard floor at 0.05
    (26 dB down). That is the "way too quiet" — it was one hit, not a
    stuck fader, but at 17 dB of swing a ghost simply vanished.

    `wobble_rng` is still accepted and ignored: every caller threads one
    through and a beat's determinism is seeded off it elsewhere. Removing
    the parameter would touch every call site for no gain."""
    base = {"X": 1.0, "x": 0.72, "o": 0.45, ".": ghost_floor}.get(char, 0.0)
    if base == 0.0:
        return 0.0
    # Positional accent stays — this is a WRITTEN rule (the two-finger
    # alternation: 'e' and 'a' sixteenths sit under the on-beats), not
    # randomness, so option (a) keeps it.
    if char == "x" and step16 % 4 in (1, 3):
        base *= 0.78
    return float(base)

# ------------------------------------------------------------ spectral tools

def _fft_weight(x, weight_fn):
    X = np.fft.rfft(x)
    X *= weight_fn(np.fft.rfftfreq(len(x), 1 / SR))
    return np.fft.irfft(X, len(x))


def lp4(x, fc):
    """4-pole (24 dB/oct) lowpass, SSM2044 stand-in."""
    return _fft_weight(x, lambda f: np.abs(1 / (1 + 1j * f / fc)) ** 4)


def lp1(x, fc):
    return _fft_weight(x, lambda f: np.abs(1 / (1 + 1j * f / fc)))


def hp1(x, fc):
    return _fft_weight(x, lambda f: np.abs((1j * f / fc) / (1 + 1j * f / fc)))


def zoh_resample(x, sr_in, sr_out):
    """Zero-order-hold resample — deliberately NO interpolation. The
    stair-steps create the images/aliasing that read as SP-1200 bright."""
    n_out = int(round(len(x) * sr_out / sr_in))
    idx = np.minimum((np.arange(n_out) * sr_in / sr_out).astype(int),
                     len(x) - 1)
    return x[idx]


def sp1200(x, smear_45_33=False, out_lp=9000.0, amount=1.0):
    """E-mu SP-1200 character: 26.04 kHz ZOH decimate, 12-bit quantize at
    the LOW rate, optional 45→33 RPM smear, ZOH back up (images kept),
    then the analog-style 4-pole lowpass. Mono in, mono out.

    amount = wet/dry blend. The owner auditioned full dirt vs clean and
    chose HALF (A/B verdict, July 2026) — pass amount=OWNER_TASTE
    ["sp1200_amount"] for house flavor; 1.0 is the full vintage unit."""
    y = zoh_resample(x, SR, 26040)
    y = np.round(y * 2047) / 2047
    if smear_45_33:
        r = 45.0 / 33.3
        y = zoh_resample(zoh_resample(y, 26040, int(26040 / r)),
                         int(26040 / r), 26040)
    y = zoh_resample(y, 26040, SR)[:len(x)]
    if len(y) < len(x):
        y = np.concatenate([y, np.zeros(len(x) - len(y))])
    y = lp4(y, out_lp) if out_lp else y
    return y * amount + x * (1 - amount)


# The owner's A/B audition verdicts (July 2026) — house defaults for every
# beat unless a personality's era demands otherwise (flag deviations for
# his ears at the prototype stage):
OWNER_TASTE = {
    "dilla_snare": "early",      # AB1: snare rushes (woozy), kick leans late
    "sp1200_amount": 0.5,        # AB2: half dirt, half clean
    "sidechain_prob": 0.9,       # AB3: duck the beat around the kick 90% of
                                 #      beats; 1 in 10 renders skips it
    "master": "modern_loud",     # AB4 picked the loud chain; owner revised
                                 #      2026-07-18: beats redlined when dropped
                                 #      into Reason, so the chain now lands on
                                 #      master_lufs with real peak headroom
    "master_lufs": -12.0,        # was -8: loud enough to audition, quiet
                                 #      enough to sit on a Reason channel at
                                 #      unity without pinning the meter
    "peak_ceiling_db": -4.0,     # was -1: peaks stay ~4 dB under 0 dBFS so
                                 #      EQ/comp in Reason has room to boost
    "snare_space": "vary",       # AB5 said gated; owner revised 2026-07-15:
                                 #      use VARIATIONS of gated and dry
                                 #      across a batch, roughly alternating
    "snare_trim_db": -5.0,       # 2026-07-14 set -3.5; owner 2026-07-18:
                                 #      snares STILL sat above the kick —
                                 #      pull the snare bus back further
    "perc_trim_db": -3.5,        # owner 2026-07-18: snaps, bells, and other
                                 #      bright percussion also ride over the
                                 #      kick — they get their own bus trim
    "gate_wet": 0.3,             # was 0.4; part of the same snare-taming fix
    "clean_renders": True,       # owner 2026-07-18: "I want the beats
                                 #      clean" — no baked-in dirt (808 dist,
                                 #      roughness AM, mix saturation, SP-1200
                                 #      dust, vinyl bed, wow/flutter, hot
                                 #      master drive); he adds his own color
                                 #      in Reason
    "open_soundbank": True,      # owner 2026-07-18: no limits on a DJ's
                                 #      sound bank — every sound in the kits
                                 #      is fair game for every DJ (taste
                                 #      tags stop gating picks; locked
                                 #      stamps still ride)
    # --- where the harmony sits under the drums (owner 2026-07-25:
    # "everything starts off the same volume ... I want traditional
    # velocity/volume dynamics at the start so it doesn't sound loud and
    # crazy"). Read against the drum lanes they share a mix with:
    # kick 1.0, snare 0.88, hat 0.36. The chord bass used to open at 0.85 —
    # louder than the snare — and the chords at 0.5, above the hats, which
    # is why a fresh beat arrived shouting. These put the pad under the kit
    # the way a record does, and are the STARTING point: the rack's dB
    # arrows move them per beat.
    # 2026-07-31: left at the owner's 0.30. Raising it to 0.55 was tried
    # first and rejected on measurement — it shifted the whole distribution
    # up 5.3 dB but did nothing about the SPREAD, so beats came back ranging
    # from 2.5 dB under the kick (shouting) to 15.5 dB under (inaudible).
    # An open-loop gain can't hit a target when the source samples vary that
    # much in loudness. The level is now set by chord_bus_under_kick_db in
    # crew.render_crew_beat, the same way the snare bus has been governed
    # since 2026-07-18. This number is just the starting point that
    # normaliser works from, and the rack's dB arrows still move it.
    "chord_gain": 0.30,          # starting point; the bus target below wins
    # how far under the kick the whole harmonic bus lands. The old comment
    # on chord_gain always claimed "~10 dB under the kick" as the intent —
    # this is that intent, finally enforced instead of hoped for.
    #
    # 9.0 -> 15.0 (owner 2026-08-03, chosen by ear from a 12/15/18 audition):
    # "the chords should sit further back. not just under the kick. I will be
    # adding my own thing to these tracks." This is a bed to play over, not a
    # part. Note that until the same day this number was not actually being
    # reached — a bug in the governor's arithmetic and a clamp that could not
    # cut more than 12 dB meant real beats were landing at -4.6 dB. Both are
    # fixed, so 15 now measures -15.1 dB with a 0.3 dB spread.
    "chord_bus_under_kick_db": 15.0,
    "chord_bass_gain": 0.55,     # ~5 dB under the kick — felt, not fighting
    # A real player leans on the downbeat and eases off the repeats. These
    # scale each chord slot in turn, cycling if the progression is longer,
    # so the harmony breathes instead of landing identically every bar.
    # FLATTENED 2026-08-03: owner heard beat 1761 and said "I don't like how
    # the samples get louder and quieter like this one. Let's keep those at a
    # steady volume." This cycle was 1.7 dB of it (the rest was the per-slot
    # variation in beat_machine, now 0 too). Kept as a tuple of ones rather
    # than deleted so the "a real player leans on the downbeat" idea is one
    # edit away if he ever wants it back — but every chord now starts level.
    "chord_accents": (1.0, 1.0, 1.0, 1.0),
    # --- DORMANT (owner 2026-07-29 hard rule overrides this): exactly one
    # melodic part now, always — see _build_chords in beat_machine.py,
    # which hardcodes part_count = 1 and no longer reads these two values.
    # Left here, unused, rather than deleted, in case the multi-part rule
    # ever comes back — was: weights for (1, 2, 3) parts (owner 2026-07-25,
    # "one or two samples at a time, up to three"), and the probability the
    # rare 3rd "passing" part played when a chord had a spare note for it.
    "melody_part_weights": (0.55, 0.35, 0.10),
    "passing_note_p": 0.5,
    # --- bus glue compression (owner 2026-07-29: "add the glue
    # compression... for better sound quality"). Gentle house starting
    # point, tune like everything else here once he's heard it — see
    # glue_compress() in this file for what each one does.
    "glue_threshold_db": -18.0,
    "glue_ratio": 1.8,
    "glue_env_ms": 25.0,
    "glue_makeup_db": 2.0,
}


def snare_scale():
    """Linear gain for the snare bus, per the owner's balance feedback."""
    return 10 ** (OWNER_TASTE["snare_trim_db"] / 20)


def perc_scale():
    """Linear gain for the bright-perc bus (snaps, bells, stamps, rims)."""
    return 10 ** (OWNER_TASTE["perc_trim_db"] / 20)

# ------------------------------------------------------------ dynamics

def transient_shape(x, onsets, gain=0.8, tau_ms=3.0, span_ms=40.0):
    """Sharpen (gain>0) or soften (gain<0) attacks. Offline advantage: we
    KNOW every onset, so a synthetic 1+g·exp(−t/τ) at each hit beats any
    envelope follower."""
    y = x.copy()
    span = int(span_ms / 1000 * SR)
    t = np.arange(span) / SR
    env = 1 + gain * np.exp(-t / (tau_ms / 1000))
    for p in onsets:
        e = min(len(y), p + span)
        y[p:e] *= env[:e - p]
    return y


def roughness_am(x, rate_hz=40.0, depth=0.35):
    """The menace knob (connections 2026-07): the 30-80 Hz threat band is
    an amplitude-modulation RATE, not a pitch. Tremolo a lane at that
    rate and it reads as danger; depth stays moderate so the fundamental
    still carries. Documented mechanism (Arnal), untried as a deliberate
    drums-only device."""
    t = np.arange(len(x)) / SR
    mod = 1.0 - depth * (0.5 + 0.5 * np.sin(2 * np.pi * rate_hz * t))
    return x * mod


def soft_clip(x, ceiling=0.94):
    return np.tanh(x / ceiling) * ceiling


def sat_unity(x, drive_db=5.0):
    """Forum 808 recipe: drive in hot, tanh, pull back to unity-ish."""
    g = 10 ** (drive_db / 20)
    return np.tanh(x * g) / np.tanh(g)

# ------------------------------------------------------------ low end

def kick_layer(top, sub, split_hz=100.0):
    """Frequency-split layering with NUMERIC phase verification: high-pass
    the top layer, low-pass the sub, then try polarity flip and small
    offsets, keeping whichever alignment makes the low band LOUDEST
    (misalignment cancels lows — the Gearspace test, automated)."""
    n = max(len(top), len(sub))
    top = np.pad(top, (0, n - len(top)))
    sub = np.pad(sub, (0, n - len(sub)))
    top_f = hp1(hp1(top, split_hz), split_hz)
    sub_f = lp4(sub, split_hz * 2)

    def low_rms(a):
        lo = lp4(a, split_hz)
        return np.sqrt((lo ** 2).mean())

    best, best_rms = None, -1.0
    for pol in (1.0, -1.0):
        for off in (0, int(0.001 * SR), int(0.002 * SR), int(0.004 * SR)):
            cand = top_f + pol * np.pad(sub_f, (off, 0))[:n]
            r = low_rms(cand)
            if r > best_rms:
                best, best_rms = cand, r
    return best / (np.abs(best).max() + 1e-9)


def dist808(x, drive_db=5.0):
    """Saturate → LP 6 kHz → mud dip 300–500 → gentle clip. The added mids
    are what make an 808 audible on a phone."""
    y = sat_unity(x, drive_db)
    y = _fft_weight(y, lambda f: np.abs(1 / (1 + 1j * f / 6000)) ** 2
                    * (1 - 0.16 * np.exp(-((f - 400) / 180) ** 2)))
    return soft_clip(y, 0.97)


def mono_below(L, R, fc=120.0):
    """Remove side-channel content under fc (forum consensus 100–120 Hz):
    a smooth raised-cosine edge over one octave, decisive below it — bass
    stays centered, width lives above."""
    mid, side = 0.5 * (L + R), 0.5 * (L - R)

    def edge(f):
        lo, hi = fc / np.sqrt(2), fc * np.sqrt(2)
        t = np.clip((np.log2(np.maximum(f, 1)) - np.log2(lo))
                    / (np.log2(hi) - np.log2(lo)), 0, 1)
        return 0.5 - 0.5 * np.cos(np.pi * t)

    side = _fft_weight(side, edge)
    return mid + side, mid - side

# ------------------------------------------------------------ space

def make_ir(seconds, tone_hz, predelay_ms=25.0, flat=False, hp_hz=300.0,
            seed=4242):
    """Stereo IR. flat=True gives constant amplitude that stops dead — the
    gated-plate body. Return is high-passed (reverb tails must not eat the
    low mids — uncontested forum rule)."""
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    shape = np.ones(n) if flat else np.exp(-3.0 * t / seconds)
    irL = hp1(lp4(r.normal(0, 1, n) * shape, tone_hz), hp_hz)
    irR = hp1(lp4(r.normal(0, 1, n) * shape, tone_hz), hp_hz)
    pre = np.zeros(int(predelay_ms / 1000 * SR))
    irL, irR = np.concatenate([pre, irL]), np.concatenate([pre, irR])
    e = np.sqrt((irL ** 2 + irR ** 2).sum()) + 1e-12
    return irL / e, irR / e


def fft_convolve(sig, ir):
    n = len(sig) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(sig, N) * np.fft.rfft(ir, N))[:len(sig)]


def loop_convolve(sig, ir):
    """Circular convolution: the reverb tail that runs past the loop end
    wraps back onto the start — the tail a listener hears at bar 1 is the
    one bar 8 just made, so the seam is continuous (owner 2026-07-18:
    beats didn't loop clean; truncated tails were one of the reasons).
    Requires len(ir) <= len(sig) — true for every house IR vs 8 bars."""
    n = len(sig)
    return np.fft.irfft(np.fft.rfft(sig) * np.fft.rfft(ir, n), n)


def gated_reverb(dry, onsets, wet=0.5, decay=1.8, hold_ms=140.0,
                 rel_ms=25.0, tone=5200.0, loop=False, stereo=False):
    """The 80s snare explosion: big bright flat-bodied tail, held then cut
    brutally fast after each hit. loop=True renders the tail circularly
    and wraps a gate window that runs past the end back onto the start,
    so a hit in the last beat of bar 8 gates cleanly across the seam.

    stereo=True additionally returns the decorrelated side component, so
    callers can print a genuinely wide gate. make_ir has always produced a
    stereo pair; until 2026-07-31 this function convolved irL and dropped
    irR on the floor, which is a third of the library's beats rendered with
    a mono gate. Default stays mono so existing callers/tests are unchanged.
    """
    irL, irR = make_ir(min(decay, 0.35), tone, predelay_ms=6, flat=True)
    conv = loop_convolve if loop else fft_convolve
    tail = conv(dry, irL)
    tailR = conv(dry, irR) if stereo else None
    n = len(tail)
    h, rl = int(hold_ms / 1000 * SR), int(rel_ms / 1000 * SR)
    gate = np.zeros(n + h + rl)          # room for overhang past the end
    for p in onsets:
        gate[p:p + h] = 1.0
        gate[p + h:p + h + rl] = np.maximum(gate[p + h:p + h + rl],
                                            np.linspace(1, 0, rl))
    if loop:
        gate[:h + rl] = np.maximum(gate[:h + rl], gate[n:])
    g = gate[:n] * wet
    if not stereo:
        return dry + tail * g
    wetL, wetR = tail * g, tailR * g
    return dry + (wetL + wetR) * 0.5, (wetL - wetR) * 0.5


def haas(mono, ms=12.0, side_db=-4.0):
    """Widen hats/perc: delayed opposite side. NEVER for kick/808 — at
    60 Hz a 10 ms delay is ~2/3 cycle and the mono sum cancels."""
    d = int(ms / 1000 * SR)
    g = 10 ** (side_db / 20)
    L = mono
    R = np.pad(mono, (d, 0))[:len(mono)] * g + mono * (1 - g)
    return L, R

# ------------------------------------------------------------ texture

def vinyl_bed(n, clicks_per_s=14.0, level_db=-42.0, seed=7):
    """Crackle: Poisson clicks (mostly small, few big) band-limited, over a
    dark noise floor. The standard boom bap glue layer."""
    r = np.random.default_rng(seed)
    x = np.zeros(n)
    idx = r.random(n) < clicks_per_s / SR
    x[idx] = r.uniform(-1, 1, idx.sum()) * r.random(idx.sum()) ** 2
    x = hp1(x, 300)
    x = _fft_weight(x, lambda f: np.abs(1 / (1 + 1j * f / 8000)))
    floor = _fft_weight(r.standard_normal(n),
                        lambda f: np.abs(1 / (1 + 1j * f / 2500))) * 0.25
    bed = x * 3.0 + floor
    return bed / (np.abs(bed).max() + 1e-9) * 10 ** (level_db / 20)


def wow_flutter(x, wow_hz=0.556, wow_pct=0.35, flut_pct=0.08, seed=11,
                loop=False):
    """Variable-speed read: wow at once-per-revolution (33⅓ RPM = 0.556 Hz)
    plus noisy flutter. 1% speed ≈ 17 cents. loop=True snaps the wow rate
    to whole cycles per pass and wraps the read position, so the warp
    lands back at zero at the seam instead of jumping pitch (the flutter
    noise is FFT-filtered, i.e. already loop-continuous)."""
    r = np.random.default_rng(seed)
    n = len(x)
    t = np.arange(n)
    if loop:
        wow_hz = max(1, round(wow_hz * n / SR)) * SR / n
    wow = (wow_pct / 100) / (2 * np.pi * wow_hz) * SR * \
        np.sin(2 * np.pi * wow_hz * t / SR)
    fl = _fft_weight(r.standard_normal(n),
                     lambda f: np.abs(1 / (1 + 1j * f / 10)))
    fl = fl / (np.abs(fl).max() + 1e-9) * (flut_pct / 100) * SR / 60
    if loop:
        return np.interp((t + wow + fl) % n, t, x, period=n)
    pos = np.clip(t + wow + fl, 0, n - 1)
    return np.interp(pos, t, x)

# ------------------------------------------------------------ generative

def euclid(k, n, rot=0):
    """E(k,n) Euclidean onset pattern (list of n bools). E(3,8)=tresillo,
    E(5,8)=cinquillo, E(5,16)=bossa, E(7,16)=samba bell (with rotation)."""
    pat = [(i * k) % n < k for i in range(n)]
    return pat[rot:] + pat[:rot]


def ratchet_times(t0, step_s, m=3, rng=None):
    """m sub-hits across one step with a rising velocity ramp."""
    vels = np.linspace(0.7, 1.0, m)
    return [(t0 + i * step_s / m, float(vels[i])) for i in range(m)]


def chance(p, rng):
    return rng.random() < p

# ------------------------------------------------------------ loudness

def k_weight(x):
    """Approximate ITU-R BS.1770 K-weighting: shelf +4 dB above ~1.5 kHz
    and a ~38 Hz highpass."""
    def w(f):
        shelf = 1 + (10 ** (4 / 20) - 1) / (1 + (1500 / np.maximum(f, 1)) ** 2)
        hp = np.abs((1j * f / 38) / (1 + 1j * f / 38))
        return shelf * hp
    return _fft_weight(x, w)


def lufs(L, R):
    """Integrated loudness, gated per BS.1770 (400 ms blocks, −70 absolute
    and −10-relative gates). Close enough to a meter to mix by."""
    kL, kR = k_weight(L), k_weight(R)
    blk = int(0.4 * SR)
    hop = blk // 4
    p = []
    for i in range(0, len(kL) - blk, hop):
        p.append((kL[i:i + blk] ** 2).mean() + (kR[i:i + blk] ** 2).mean())
    p = np.array(p)
    lk = -0.691 + 10 * np.log10(p + 1e-12)
    p = p[lk > -70]
    if not len(p):
        return -70.0
    rel = -0.691 + 10 * np.log10(p.mean()) - 10
    p = p[(-0.691 + 10 * np.log10(p)) > rel]
    if not len(p):
        return -70.0
    return -0.691 + 10 * np.log10(p.mean())


def glue_compress(L, R, threshold_db=None, ratio=None, env_ms=None,
                  makeup_db=None):
    """Bus 'glue' compression — the everyday effect the tanh saturation in
    master() can't give, because saturation reacts per-sample and this
    reacts over TIME. One shared envelope from the L+R sum (mono
    loudness, so the stereo image isn't skewed by two independent
    detectors), a soft downward ratio above threshold, the SAME gain
    applied to both channels so nothing shifts pan. Runs BEFORE master()
    in the chain — glue the mix first, then tone/saturate/limit it.

    ponytail: one symmetric smoothing time constant for the envelope
    (via lp1), not separate attack/release times — a real glue comp eases
    in fast and lets go slow, which is where the "pump"/groove character
    comes from. This version only breathes at one speed. Upgrade path if
    that difference matters to the ear: two lp1 passes at different fc
    (fast for rising level, slow for falling), combined per-sample with
    np.maximum instead of one lp1 call below."""
    threshold_db = OWNER_TASTE["glue_threshold_db"] if threshold_db is None else threshold_db
    ratio = OWNER_TASTE["glue_ratio"] if ratio is None else ratio
    env_ms = OWNER_TASTE["glue_env_ms"] if env_ms is None else env_ms
    makeup_db = OWNER_TASTE["glue_makeup_db"] if makeup_db is None else makeup_db
    det = 0.5 * (np.abs(L) + np.abs(R))
    env = lp1(det, 1000 / (2 * np.pi * env_ms))
    env_db = 20 * np.log10(np.maximum(env, 1e-9))
    over_db = np.maximum(env_db - threshold_db, 0.0)
    gain_db = makeup_db - over_db * (1 - 1 / ratio)
    g = 10 ** (gain_db / 20)
    return L * g, R * g


def master_to_lufs(L, R, target=None, ceiling_db=None):
    """Modern beat loudness: measure, gain toward target, soft-clip into
    the house ceiling, re-measure and report. Iterate twice — the clip
    changes the measurement. Defaults come from OWNER_TASTE so one edit
    there re-levels every render path."""
    if target is None:
        target = OWNER_TASTE["master_lufs"]
    if ceiling_db is None:
        ceiling_db = OWNER_TASTE["peak_ceiling_db"]
    for _ in range(2):
        cur = lufs(L, R)
        g = 10 ** ((target - cur) / 20)
        ceil = 10 ** (ceiling_db / 20)
        L = np.tanh(L * g / ceil) * ceil
        R = np.tanh(R * g / ceil) * ceil
    return L, R, lufs(L, R)
