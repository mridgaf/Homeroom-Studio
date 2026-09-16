"""Chord + bass audio synthesis (punch list step 7, 2026-07-22).

harmony.py decides WHICH notes a beat's progression is; this decides
what they sound like once a beat actually asks for them ("chords" in
the notes box, beat_machine.parse_directions).

WHAT'S GONE (owner directive 2026-07-23, "get rid of them"): pad_voice
(the synthesized chord pad) and _pluck (the synthesized arp step) were
DELETED. Every melodic instrument now comes from his own sample banks —
see tools/instrument_sampler.py. Do not add a synthesized chord voice
back as a fallback; a step or chord that can't be voiced from his
samples is left silent and the caller falls through to another source.
arp_riff's `render_note` is required for that reason.

What's left here, and why:

- bass_voice: the chord root on sub808 — the same tone the drum-only
  tuned-808 feature already puts under the kick. This one is a synth
  tone ON PURPOSE and was deliberately NOT removed: it's the tuned 808,
  a drum-machine voice the owner asked for, and song-keys.md wants one
  consistent low end rather than a different sampled bass per beat.
- sample_pool/loop_voice: a real melodic-loop file from his library, in
  key — melodic_loops.py does the finding and the pitch-fit, this picks
  and loads.
- arp_riff: the broken-chord rhythm, driven by whatever sampled
  instrument the caller hands it.
"""
from __future__ import annotations

import random

import numpy as np

from key_context import KeyContext
from make_drum_loops import SR, sub808
from make_hiphop_tracks import load_audio, norm_rms
from melodic_loops import chop_onsets, fit_loop, in_key, scan as scan_loops


# Sample-peak ceiling for a chord buffer. NOT 0.99: a signal sitting at
# 0.99 at every sample can still exceed 0 dBFS BETWEEN samples, and the
# converter clips that on playback even though every stored sample is
# legal. Measured on the owner's own demos at the old 0.99 ceiling:
# "synth - high" hit +0.49 dBTP and "horns - stabs" +0.01 dBTP — real
# digital clipping he could hear while a sample-peak check said clean.
# -1 dBFS leaves room for the overshoot that resampling and stacked
# attacks create. (The beats' own master stays far below this anyway.)
PEAK_CEILING = 0.89


def midi_to_hz(note):
    return 440.0 * 2.0 ** ((note - 69) / 12.0)


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
    """In-key chord- or melody-role files from the owner's library, once
    per beat (scanning is disk I/O — don't repeat it per chord slot).
    Both kind="oneshot" and kind="loop" entries are usable: loop_voice
    chops a loop-kind pick into its individual note/chord hits first
    (melodic_loops.chop_onsets), so fit_loop's pitch-only-resample
    ceiling (it can't correct tempo) never has a whole rhythmic loop to
    drift against the beat grid — see chop_onsets' docstring."""
    return [e for e in in_key(scan_loops(), key, bpm=bpm)
            if e["role"] in ("chord", "melody")]


def midi_pool(key):
    """In-key chord-role MIDI phrases from the owner's MIDI packs
    (tools/midi_packs.py) — the symbolic twin of sample_pool above: a
    real chord progression someone else already wrote, instead of a
    real recorded loop someone else already played."""
    import midi_packs
    return midi_packs.in_key(midi_packs.scan(), key, role="chord")


def midi_progression(pick, key):
    """`pick`'s own chords, transposed into `key`:
    [(root_pc, quality, [midi notes]), ...] in file order — or None if
    the file has no usable chord content. Re-reads the file rather than
    trusting the cached scan()["chords"] field, because that cache drops
    the actual note stack (kept small on disk) and keeps only
    (time, root, quality) — see midi_packs.scan()."""
    import midi_packs
    prog = midi_packs.progression(midi_packs.read_notes(pick["path"]))
    if not prog:
        return None
    shift = key.shift_from(KeyContext(pick["key"], pick["mode"]))
    return [(root, quality, sorted(n + shift for n in stack))
            for _, root, quality, stack in prog]


def loop_voice(pool, dur, key, sr=SR, rng=None, used=None):
    """Load+fit the best-available pick from `pool` into `dur` seconds
    at `key`; (None, None) if the pool's empty, the file won't load, or
    (for a loop-kind pick) chopping finds no usable onset, so the
    caller can fall through to a sampled instrument voice."""
    if not pool:
        return None, None
    pick = (rng or random).choice(pool[:3])
    if used is not None:                 # name the real file for the rack
        used.append(pick["path"])
    x = load_audio(pick["path"])
    if x is None:
        return None, None
    mono = x.mean(axis=1) if x.ndim == 2 else x
    if pick["kind"] == "loop":
        chops = chop_onsets(mono, sr)
        if not chops:
            return None, None
        mono = (rng or random).choice(chops)
    src_key = KeyContext(pick["key"], pick["mode"] or key.mode)
    fitted = fit_loop(mono, sr, dur, src_key=src_key, dst_key=key)
    # de-clicked for the same reason every other chord voice is: fit_loop
    # crops/tiles, so the bed can start or end mid-waveform and step into
    # whatever follows. Measured smaller here than on the samplers (0.008
    # vs 0.35) but it's the same defect, so it gets the same one-liner.
    # imported HERE, not at module top, on purpose: instrument_sampler
    # imports PEAK_CEILING from this module, so a top-level import would
    # be a circular one. Don't "tidy" it upward.
    from instrument_sampler import _declick
    return _declick(norm_rms(fitted, -18.0), sr), pick["name"]


def arp_riff(notes, dur, bpm, render_note, sr=SR):
    """Sequence chord `notes` as a repeating ascending arpeggio that fills
    `dur` seconds — the broken-chord "riff" feel (think the Still-D.R.E.
    figure) instead of one held block like play_chord. One note per
    eighth-note step; `render_note(note, seg_dur)` supplies each step's
    audio, so the same rhythm drives any sampled instrument. Bar-aligned,
    and the tail of the last steps wraps back to the top, so the buffer
    loops seamlessly (loop-safe render rule).

    `render_note` is REQUIRED as of 2026-07-23. It used to default to a
    synthesized pluck, which is exactly the generated-instrument sound the
    owner had removed; a step that can't be voiced from his samples is now
    left SILENT rather than filled with an oscillator. A caller whose
    render_note returns None for every step gets a silent buffer back, and
    _build_chords treats that as "this voice failed" and falls through."""
    n = max(int(dur * sr), 1)
    out = np.zeros(n)
    if not notes:
        return out
    step_s = (60.0 / bpm) / 2.0               # an eighth note, meter-agnostic
    nsteps = max(int(round(dur / step_s)), 1)
    pat = list(notes) + [notes[0] + 12]       # up through the octave, repeating
    seg_dur = step_s * 1.4                     # slight legato overlap into the next
    for k in range(nsteps):
        note = pat[k % len(pat)]
        seg = render_note(note, seg_dur)
        if seg is None:                       # unvoiceable step: leave it
            continue                          # silent, never synthesize one
        add_wrapped(out, seg, int(round(k * step_s * sr)))
    return finish_riff(out, sr)


def add_wrapped(out, seg, start):
    """Mix `seg` into `out` at sample `start`, wrapping anything past the
    end back to the front. That wrap is the loop-safe rule (a chord buffer
    is tiled, so a tail that runs off the end must arrive at the top, not
    be cut). Extracted 2026-09-05 so chord_rhythm's figures place their
    hits by exactly the same rule arp_riff always has."""
    n = len(out)
    if start >= n:
        start %= n
    end = start + len(seg)
    if end <= n:
        out[start:end] += seg
        return
    head = n - start
    out[start:] += seg[:head]
    tail = seg[head:][:n]
    out[:len(tail)] += tail


def finish_riff(out, sr=SR):
    """Edge ramps, RMS normalize, peak guard — the tail of arp_riff, now
    shared with chord_rhythm.render_figure."""
    peak = np.max(np.abs(out))
    if peak <= 0:            # every step came back unvoiceable: hand back
        return out           # the silence rather than NaN out of norm_rms
    # The wrap above puts the tail's CONTINUATION at the front, but the
    # buffer itself still ended mid-note at full amplitude — a step into
    # whatever follows, heard as a click at the end (owner 2026-07-23).
    # Ramping the last 60ms to zero removes the step without undoing the
    # wrap: on a loop the front already carries the continuation, so this
    # is the release the note should have had, not a fade on the loop.
    # ...and the same at the START, where the wrap deposits that tail at
    # full amplitude — a sound appearing from nothing on sample 0.
    a = min(int(0.008 * sr), len(out))
    r = min(int(0.06 * sr), len(out))
    if a:
        out[:a] *= np.linspace(0, 1, a)
    if r:
        out[-r:] *= np.linspace(1, 0, r)
    out = norm_rms(out, -18.0)
    peak = np.max(np.abs(out))                # overlapping stabs can stack
    return out * (PEAK_CEILING / peak) if peak > PEAK_CEILING else out
