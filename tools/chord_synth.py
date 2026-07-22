"""Chord + bass audio synthesis (punch list step 7, 2026-07-22).

harmony.py decides WHICH notes a beat's progression is; this decides
what they sound like once a beat actually asks for them ("chords" in
the notes box, beat_machine.parse_directions). Same DSP style as
make_drum_loops.py — plain numpy oscillators, no new dependency:

- bass_voice: the chord root, reusing sub808 (the same tone the
  drum-only tuned-808 feature already puts under the kick) — the bass
  IS the note the rest of the harmony reads as the key (song-keys.md).
- pad_voice: a soft multi-note chord voice, slow attack so it sits
  BEHIND the drums instead of fighting them for the transient.

Both return a plain mono array sized to `dur` seconds, meant to be
dropped straight into beat_machine's kit dict as one long "one-shot"
per chord — the same trick the tuned-808 sub already uses, just with a
duration long enough to hold a whole chord section instead of one hit.

ponytail: no sampled instrument here. The owner's own Symphonic
Strings / melodic-loop library (punch list steps 5-6) is real audio
that would sound better than a synth pad, but fitting it in key AND
tempo is a separate, heavier job the gap analysis itself flagged as
fast-follow, not MVP. The seam is already there: harmony.compose()
gives exact MIDI notes, ready to hand to a sampler instead of this pad
whenever that lands.
"""
from __future__ import annotations

import numpy as np

from make_drum_loops import SR, sub808


def _osc(freq, n, shape="sine"):
    t = np.arange(n) / SR
    if shape == "sine":
        return np.sin(2 * np.pi * freq * t)
    return 2 / np.pi * np.arcsin(np.sin(2 * np.pi * freq * t))  # triangle


def midi_to_hz(note):
    return 440.0 * 2.0 ** ((note - 69) / 12.0)


def pad_voice(notes, dur, sr=SR):
    """A soft chord pad from a stack of MIDI notes: sine + a little
    triangle per note for warmth, slow attack/release so the onset
    never competes with the kick/snare transient."""
    n = int(dur * sr)
    if n <= 0 or not notes:
        return np.zeros(max(n, 0))
    out = np.zeros(n)
    for note in notes:
        freq = midi_to_hz(note)
        out += 0.6 * _osc(freq, n, "sine") + 0.4 * _osc(freq, n, "triangle")
    out /= len(notes)
    a = min(int(0.08 * sr), n // 4)          # 80ms attack, or shorter if n is tiny
    r = min(int(0.15 * sr), n // 4)          # release tail, wraps via the
    env = np.ones(n)                         # loop-fold like every other lane
    if a:
        env[:a] = np.linspace(0, 1, a)
    if r:
        env[-r:] *= np.linspace(1, 0, r)
    return out * env * 0.5


def bass_voice(root_note, dur, sr=SR):
    """The chord's root an octave down, on the drum-only 808's own
    tone — bass_voice(60, ...) sounds like the same sub as a C kick
    root, just addressable by any MIDI note instead of one fixed dict."""
    freq = midi_to_hz(root_note - 12)
    n = max(int(dur * sr), 1)
    tone = sub808(freq, min(dur, 1.2), drive=1.1)
    if len(tone) >= n:
        return tone[:n]
    out = np.zeros(n)
    out[:len(tone)] = tone
    return out
