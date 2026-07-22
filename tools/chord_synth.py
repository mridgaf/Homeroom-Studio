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

sample_pool/loop_voice (punch list step 5-6 wiring, 2026-07-22): a real
melodic-loop file from the owner's own library, in key, standing in for
pad_voice when one's available — melodic_loops.py does the finding and
the pitch-fit, this just picks and loads. bass_voice is untouched: the
sub is a synth tone on purpose (song-keys.md wants one consistent low
end), the pad is the one the docstring above always said sampled audio
would beat.
"""
from __future__ import annotations

import random

import numpy as np

from key_context import KeyContext
from make_drum_loops import SR, sub808
from make_hiphop_tracks import load_audio, norm_rms
from melodic_loops import fit_loop, in_key, scan as scan_loops


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


def sample_pool(key, bpm=None):
    """In-key "chord"-role melodic files from the owner's library, once
    per beat (scanning is disk I/O — don't repeat it per chord slot).

    ponytail: restricted to kind="oneshot". fit_loop pitch-corrects by
    resample but can't stretch tempo independently, so a rhythmic loop
    tiled to `dur` at the wrong BPM would drift audibly against the
    beat grid; a one-shot pad/keys hit has no internal rhythm to clash.
    Judgment call, flagged rather than guessed: if this reads as too
    conservative (loops sound fine in practice, or "melody"-role picks
    would work as a pad too), loosen the filter here.
    """
    return [e for e in in_key(scan_loops(), key, role="chord", bpm=bpm)
            if e["kind"] == "oneshot"]


def loop_voice(pool, dur, key, sr=SR, rng=None):
    """Load+fit the best-available pick from `pool` into `dur` seconds
    at `key`; (None, None) if the pool's empty or the file won't load,
    so the caller can fall back to pad_voice."""
    if not pool:
        return None, None
    pick = (rng or random).choice(pool[:3])
    x = load_audio(pick["path"])
    if x is None:
        return None, None
    mono = x.mean(axis=1) if x.ndim == 2 else x
    src_key = KeyContext(pick["key"], pick["mode"] or key.mode)
    fitted = fit_loop(mono, sr, dur, src_key=src_key, dst_key=key)
    return norm_rms(fitted, -18.0), pick["name"]
