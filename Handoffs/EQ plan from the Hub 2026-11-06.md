# EQ plan from the Production Research Hub (2026-11-06) — DRAFT, nothing applied

Source = Hub only (no web search). Chapter / part named so you can check each line.
"Sourced" = the Hub says it. "Guess" = I filled a gap; no source.

## What the engine does today (AUDITED 2026-11-06, read from code, nothing rendered)
Order on a normal new beat, lane first, then the whole mix:

| Stage | What it does | Where |
|---|---|---|
| Chord + melody lanes | high-pass 120 Hz | `crew.py:128, 1865` |
| Every lane except kick/808/sub/bass | 30 Hz rumble cut (12 dB/oct) | `base_clean.py` RUMBLE_HZ |
| **Chord lanes only** | extra 150 Hz low cut (12 dB/oct) | `base_clean.py` CHORD_HZ |
| Whole mix | side signal removed below ~85–170 Hz (bass centred) | `base_clean.mono_below`, `crew.py:2584` |
| Whole mix, `mix_eq` | low shelf +1.5 dB @120 Hz, mid -1.0 dB @800 Hz (Q 0.9), high +2.0 dB @8 kHz | `groove.py:216` |
| Master | air shelf (+35% above ~9 kHz), 300–900 Hz scoop (-15%), side high-pass 200 Hz, tanh glue | `make_drum_loops.master` |

Findings:
- **Chords already have a 150 Hz cut** (so the "150 Hz" row below is already done). **Melody only gets 120 Hz** — its role is `melody`, not `chord`.
- No per-lane EQ exists for hats, clap, snare, melody tone or bass tone. The only tone shaping is whole-mix.
- Drums, snare reverb and reverb tails: I did not check for their own filters (the Sound Engine in `sound_engine/` is a separate path I did not read).
- Levels: true-levels ON, chord gain 0.30 (back to original).

## Per-lane suggestions

| Lane | Suggestion | Source |
|---|---|---|
| Chords | High-pass ~150 Hz — ALREADY DONE (`base_clean.py`) | Sourced: Ch03 P3 L422 (Audeobox) |
| Chords | If boxy: ~3 dB cut, narrow, found by sweeping 300–500 Hz | Sourced: Ch03 P4 L101 (a vocal tip; works the same on any source) |
| Melody | Same 150 Hz high-pass as chords — NOT done yet (melody gets 120 only) | Sourced: same line |
| Melody | Optional presence ~3–4 kHz wide boost, air 3–4 dB at 8 kHz+ | Sourced for vocals only (Ch03 P4 L103–105). For a sample melody: Guess |
| Bass / 808 | Keep it mono below ~100–150 Hz; never widen it | Sourced: Ch02 P1 L260, P2 L42 |
| Bass / 808 | One low sound at a time; two long 808s in the same range = mud | Sourced: Ch02 P2 L116, L140 |
| Kick layer | Click 1–4 kHz on top, body under 100 Hz, each filtered to its band | Sourced: Ch02 P1 L250 |
| Snare reverb | High-pass the reverb 300–500 Hz; EQ the return, not the snare | Sourced: Ch02 P1 L273 |
| Any reverb tail | Cut under ~200 Hz and over ~8 kHz | Sourced: Ch02 P2 L47 |
| Drum bus | Gentle low-pass ~8–10 kHz softens harsh hits | Sourced: Ch03 P4 L45 |
| Lo-fi / dusty feel | Soft roll-off 6–10 kHz | Sourced: Ch02 P1 L160 |

## Gaps (the Hub has nothing solid on these)
- Hat and clap EQ numbers.
- Sampled pluck / stab / pad EQ.
- A bass-line (not 808) EQ curve.
- How much to cut where chords and melody overlap each other.
Say the word and I do a fresh Firecrawl search for those four.

## How I'd test it (only if you say go)
Change one lane at a time, measure the finished file (audio-fix-verify), you listen. No renders from me.
