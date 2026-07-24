"""Atari 2600 and NES voices — the ONE sanctioned synthesis in this
project (owner request 2026-07-24: "I like video game sounds, like, from
Atari and early Nintendo").

=====================================================================
READ THIS BEFORE DELETING ME.
Every other synthesized instrument in this codebase was deliberately
removed on 2026-07-23 ("get rid of them"), and instrument_sampler.py
says never to reintroduce an oscillator. That rule stands. This file is
a NAMED EXCEPTION, approved by the owner, and the distinction is real:

  the synth horn was deleted because it IMITATED a real trumpet badly.
  A square wave imitates nothing. On an NES there was no instrument
  being faked — the chip generating a square wave IS the authentic
  article, and there is no sample of it that would be "more real".

Checked before writing this: his banks hold ~5 "blip" synths and 9
laser FX and no chip material at all, so sampling was not an option
even in principle. If chip sample packs ever land in his library, a
sampled path would be a fine ADDITION, but it would not be more
authentic than this.
=====================================================================

What the real hardware did, and what that means for the code:

- Atari 2600 (TIA, 1977): two voices, 4-bit volume, and only **32
  possible pitches**, unevenly spaced. Many notes are genuinely out of
  tune with each other and no composer could fix it — that sourness IS
  the Atari sound. `atari_note` quantizes to the real divider grid
  rather than playing in tune, so it is wrong in the same way the
  hardware was wrong.
- NES (Ricoh 2A03, 1983): five voices, each with one job — two pulses
  (melody/harmony, timbre set by DUTY CYCLE), a triangle (bass, fixed
  volume, 16 quantized steps, hence the hollow buzz), a noise channel
  (drums, driven by a linear-feedback shift register), and one crunchy
  sample channel (not modelled — that one WOULD be a sample).
- Only two pulse voices means a 3-note chord is impossible, so chords
  were faked by flicking between the notes ~60 times a second. That
  bubbling ripple is `arp_chord`, and it is the single most
  recognisable chiptune gesture.

Everything is band-unlimited on purpose: no filter, no reverb, no
anti-aliasing. The harshness is the sound. Output still honours the
house rules that are about safety rather than taste — de-clicked edges
and PEAK_CEILING headroom (see chord_synth).

    ./.venv/bin/python tools/chip_synth.py       # writes a demo WAV set
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

import numpy as np                                          # noqa: E402

from chord_synth import PEAK_CEILING                        # noqa: E402
from make_drum_loops import SR                              # noqa: E402

# NES pulse duty cycles. 12.5% is thin and nasal, 50% is the fat classic,
# 75% is identical in tone to 25% (the hardware quirk is real — it's the
# inverse waveform, and your ear can't tell them apart).
DUTIES = (0.125, 0.25, 0.5, 0.75)

# The 2A03 ran its envelope/arpeggio updates once per video frame.
NTSC_FRAME_HZ = 60.0

# 4-bit volume, exactly as the hardware had it.
VOL_STEPS = 16


def midi_to_hz(note):
    return 440.0 * 2.0 ** ((note - 69) / 12.0)


def _quantize(x, steps):
    """Crush to `steps` discrete levels. The NES triangle is 4-bit (16
    steps) and that stepping is audible — it's why the bass buzzes
    instead of sounding like a smooth synth triangle."""
    return np.round(x * (steps / 2.0)) / (steps / 2.0)


def pulse(freq, dur, duty=0.5, sr=SR):
    """A pulse (square) wave — the NES melody voice. `duty` sets the
    timbre: 0.5 is the round classic, 0.125 the thin nasal one."""
    n = max(int(dur * sr), 1)
    t = np.arange(n) / sr
    phase = (t * freq) % 1.0
    return np.where(phase < duty, 1.0, -1.0)


def triangle(freq, dur, sr=SR, steps=16):
    """The NES bass voice: a triangle quantized to 16 steps. Fixed
    volume on the real chip, so it never fades — it just stops."""
    n = max(int(dur * sr), 1)
    t = np.arange(n) / sr
    phase = (t * freq) % 1.0
    tri = 4.0 * np.abs(phase - 0.5) - 1.0
    return _quantize(tri, steps)


def noise(dur, period=64, sr=SR, short=False):
    """The NES noise channel — the drums. A real linear-feedback shift
    register, not white noise: bit 0 XORed with bit 1 (or bit 6 in
    "short" mode, which gives the metallic, almost pitched rattle the
    hardware is known for). `period` sets how often the register
    clocks, i.e. how bright the hiss is."""
    n = max(int(dur * sr), 1)
    reg = 1 << 14                       # 15-bit register, seeded non-zero
    out = np.empty(n)
    hold = max(int(period), 1)
    val = 1.0
    for i in range(n):
        if i % hold == 0:
            tap = 6 if short else 1
            fb = ((reg ^ (reg >> tap)) & 1)
            reg = (reg >> 1) | (fb << 14)
            val = 1.0 if (reg & 1) else -1.0
        out[i] = val
    return out


def sweep(freq_from, freq_to, dur, duty=0.5, sr=SR):
    """A pitch slide on a pulse voice — up is a jump/power-up, down is a
    laser or a death. Same trick either direction."""
    n = max(int(dur * sr), 1)
    t = np.arange(n) / sr
    freqs = np.linspace(freq_from, freq_to, n)
    phase = (np.cumsum(freqs) / sr) % 1.0
    return np.where(phase < duty, 1.0, -1.0)


def _envelope(n, atk=0.002, dec=0.0, sus=1.0, rel=0.02, sr=SR):
    """A blocky chip envelope. Short attack so it clicks in the way the
    hardware did, and a release so the buffer can't step into silence
    (the ONE house rule that still applies here — see DECISIONS
    2026-07-24 on the click/clip fix)."""
    env = np.ones(n) * sus
    a = min(int(atk * sr), n)
    d = min(int(dec * sr), max(n - a, 0))
    r = min(int(rel * sr), n)
    if a:
        env[:a] = np.linspace(0, 1, a)
    if d:
        env[a:a + d] = np.linspace(1.0, sus, d)
    if r:
        env[-r:] *= np.linspace(1, 0, r)
    return env


def chip_note(note, dur, duty=0.5, voice="pulse", sr=SR):
    """One chip note at MIDI `note`. voice: pulse | triangle."""
    hz = midi_to_hz(note)
    raw = (triangle(hz, dur, sr) if voice == "triangle"
           else pulse(hz, dur, duty, sr))
    out = raw * _envelope(len(raw), sr=sr)
    return _quantize(out, VOL_STEPS) * 0.6


def arp_chord(notes, dur, rate_hz=NTSC_FRAME_HZ / 3.0, duty=0.5, sr=SR,
              tuning="equal"):
    """THE chiptune gesture: a chord faked on one voice by flicking
    between its notes many times a second. Two pulse channels meant a
    real triad was impossible, so the chip cycled the notes fast enough
    that the ear smears them into a chord.

    Default ~20 flips/second (every 3rd video frame), which is the
    classic bubbling speed. Faster reads as a buzzing timbre rather than
    a chord; slower stops fusing and just sounds like a fast arpeggio.

    `tuning="atari"` snaps every note to the TIA's integer-divider grid
    instead of equal temperament, so the chord comes out genuinely sour
    in the way the hardware was — see `atari_detune_cents`. That is a
    character choice, not a bug (New Math uses it deliberately).
    """
    n = max(int(dur * sr), 1)
    if not notes:
        return np.zeros(n)
    step = max(int(sr / max(rate_hz, 1e-6)), 1)
    out = np.zeros(n)
    pos = 0
    k = 0
    while pos < n:
        note = notes[k % len(notes)]
        seg = min(step, n - pos)
        hz = midi_to_hz(note)
        if tuning == "atari":
            hz, _ = _tia_freq(hz)
        t = np.arange(seg) / sr
        phase = ((t + pos / sr) * hz) % 1.0     # continuous phase, no clicks
        out[pos:pos + seg] = np.where(phase < duty, 1.0, -1.0)
        pos += seg
        k += 1
    out = out * _envelope(n, sr=sr)
    return _quantize(out, VOL_STEPS) * 0.6


# ------------------------------------------------------------ Atari
# The TIA divides in TWO stages, and both matter:
#   f = 31400 / (TONE_DIV * (AUDF + 1))
# AUDF is the 5-bit pitch register (0-31 — hence only 32 pitches), and
# TONE_DIV comes from the AUDC tone setting. Modelling only AUDF puts
# every note ~3 octaves too high, which is exactly what the first draft
# of this file did and what its own report caught.
# TONE_DIV 6 is the AUDC=12 "pure tone" setting used for most Atari
# melodies; it lands the 32 available pitches across ~163-5233 Hz.
TIA_CLOCK = 31400.0
# The documented pure-tone AUDC settings: AUDC 4/5 divide by 2, AUDC
# 12/13 divide by 6. Games picked between them to reach different
# registers, so the model tries both and takes whichever lands closest.
TIA_TONE_DIVS = (2, 6)
TIA_AUDF_MAX = 31
# With div 6 and AUDF maxed the chip bottoms out here. Below this the
# TIA simply could not play a pitched note on a pure tone — real games
# used the buzzy polynomial tones for bass instead. Not a bug to fix.
TIA_FLOOR_HZ = TIA_CLOCK / (max(TIA_TONE_DIVS) * (TIA_AUDF_MAX + 1))


def _tia_freq(want_hz):
    """The frequency the TIA can actually produce nearest `want_hz`, and
    the (tone_div, AUDF) that gets it."""
    best = None
    for div in TIA_TONE_DIVS:
        audf = int(round(TIA_CLOCK / (div * max(want_hz, 1e-6)))) - 1
        audf = max(0, min(TIA_AUDF_MAX, audf))
        got = TIA_CLOCK / (div * (audf + 1))
        err = abs(1200.0 * np.log2(got / max(want_hz, 1e-6)))
        if best is None or err < best[2]:
            best = (got, audf, err, div)
    return best[0], best[1]


def atari_note(note, dur, sr=SR):
    """A note as the Atari 2600 would ACTUALLY have played it — snapped
    to the nearest available divider, which is often noticeably sharp or
    flat. Playing this in tune would be the inauthentic choice."""
    got, _ = _tia_freq(midi_to_hz(note))
    raw = pulse(got, dur, 0.5, sr)
    return _quantize(raw * _envelope(len(raw), sr=sr), VOL_STEPS) * 0.6


def atari_detune_cents(note):
    """How far off `note` the Atari lands, in cents. Purely diagnostic —
    but it's the number that explains the whole Atari sound: some notes
    land nearly perfect, their neighbours are 30-50 cents out, and a
    composer could only pick keys where the important notes fell close."""
    want = midi_to_hz(note)
    got, _ = _tia_freq(want)
    return 1200.0 * np.log2(got / want)


# ------------------------------------------------------------ drums
def chip_kick(dur=0.18, sr=SR):
    """A pitch-swept pulse — the NES kick, a fast drop."""
    return sweep(160, 45, dur, 0.5, sr) * _envelope(
        max(int(dur * sr), 1), atk=0.001, rel=0.04, sr=sr) * 0.7


def chip_snare(dur=0.16, sr=SR):
    """Noise burst = the NES snare."""
    n = max(int(dur * sr), 1)
    return noise(dur, period=16, sr=sr) * _envelope(
        n, atk=0.001, rel=0.05, sr=sr) * 0.6


def chip_hat(dur=0.05, sr=SR):
    """Short, bright, short-mode noise = the metallic chip hat."""
    n = max(int(dur * sr), 1)
    return noise(dur, period=4, sr=sr, short=True) * _envelope(
        n, atk=0.0005, rel=0.02, sr=sr) * 0.4


def count_rate(bpm, per_beat=3.0):
    """Arp flicker rate from tempo, so the ripple is LOCKED to the beat
    instead of free-running. `per_beat` is how many notes the chord
    cycles through per quarter note — 3 is a triplet ripple, 5 is a
    quintuplet (New Math's five-against-four, moved off the hat lane and
    into the harmony).

    Worth knowing before tuning this: a beat-locked rate lands WELL under
    the ~20Hz the NES free-ran at — 5 per beat at 144bpm is only 12Hz —
    which is below the point where the ear fuses the notes into a single
    chord. That is the intended trade here, not an oversight: fused, you
    hear a chord and the counting disappears; at 12Hz you actually hear
    the five running against the four, which is the whole point of the
    character. Push `per_beat` up if you want fusion instead of counting.
    Clamped to a sane band either way.
    """
    hz = (bpm / 60.0) * float(per_beat)
    return max(8.0, min(hz, 80.0))


def chip_chord(notes, dur, duty=0.5, sr=SR, tuning="equal",
               rate_hz=NTSC_FRAME_HZ / 3.0):
    """A chord the chiptune way — arpeggio-fused, not stacked. Peak
    guarded to the house ceiling so it can't clip between samples."""
    out = arp_chord(notes, dur, rate_hz=rate_hz, duty=duty, sr=sr,
                    tuning=tuning)
    peak = np.max(np.abs(out))
    if peak > PEAK_CEILING:
        out = out * (PEAK_CEILING / peak)
    return out


def _report():
    print("NES duty cycles:", DUTIES)
    print("\nAtari tuning error (why it sounds sour), C4-B4:")
    NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    worst = (0, "")
    for note in range(60, 72):
        c = atari_detune_cents(note)
        bar = "#" * min(int(abs(c) / 2), 30)
        print("  %-3s %+7.1f cents %s" % (NAMES[note % 12], c, bar))
        if abs(c) > abs(worst[0]):
            worst = (c, NAMES[note % 12])
    print("\n100 cents = one semitone; past ~15 is audibly off.")
    print("Worst note in this octave: %s at %+.0f cents." % (worst[1], worst[0]))
    print("That is the Atari sound — not every note, just enough of them.")
    print("Pitched notes bottom out at %.0f Hz (%s below that the chip "
          "used its buzz tones instead)." % (TIA_FLOOR_HZ, "everything"))


if __name__ == "__main__":
    _report()
