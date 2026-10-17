# Beat Machine — Instrument Layout + Low-End Proposal (2026-09-23)

Scope: drums + 808 + bass only. Loops left out entirely (owner, 2026-09-23).
Status: PROPOSAL — nothing built. Needs owner OK per item.

## What the code does today (checked in files, not assumed)
- 808 lane ("bass") copies the kick's pattern exactly — beat_machine.py ~1583.
- Low end (sub/808) ducks 5.0 dB under the kick (SUB_DUCK_DEFAULT, owner's ear 2026-09-01).
- Melodic bass notes (bass0..N) are NOT in _LOW_END, so they only get the
  mix-wide duck (~1.4-3.7 dB depending on DJ) — crew.py _lane_sc().
- Duck shape: instant attack, fixed 90 ms release at every tempo (make_drum_beats.duck).
- Hits on a lane stack (crew.py ~1587). A second 808 hit does not cut the first,
  so close kicks (e.g. "X-x") = two 808 tails summing = mud/phase smear.
- No choke between hats: open hat keeps ringing under the closed hat.
- Hard rule 2026-09-14 "don't pile lows on lows": a LONG 808 kick counts as the
  beat's one low sound, so no 808 lane is added under it.
- Sampled 808 appears on ~40% of beats (SAMPLED_BASS_P).

## Proposed track layout (mirrors MPC A01-A16 / TR-8S / Maschine)
| # | Track | Job | Ducked by kick | Choke / mono |
|---|-------|-----|----------------|--------------|
| 1 | Kick (short "top" kick) | punch/click | never (it's the trigger) | — |
| 2 | 808 | sub + note | YES, 5 dB (keep) | mono: new hit cuts old |
| 3 | Bass notes | melodic low | YES, same low-end duck | mono |
| 4 | Snare | backbeat | no | — |
| 5 | Clap / Snap | backbeat layer | no | — |
| 6 | Closed hat | timekeeper | light (mix duck) | chokes open hat |
| 7 | Open hat | timekeeper | light | choked by closed hat |
| 8 | Perc 1-3 | color | light | — |
| 9 | Crash / FX | punctuation | light | — |
| 10 | Chords / instruments | harmony | light (mix duck) | — |

## Changes, in order of payoff
1. Bass notes join the low-end duck (put bass0..N on the 5 dB duck). Small change.
2. 808 goes mono (choke itself): each new 808 hit fades the previous one out in ~5 ms.
3. Kick + 808 together: when an 808 lane is on, pick a SHORT punchy kick
   (keeps the 09-14 one-low-sound rule — two long 808s in the same range is mud).
4. Duck shape: 2-3 ms attack ramp (avoids a click on a ringing sub) and release
   tied to tempo (about a 1/16 note: ~110-170 ms at 90-140 BPM), industry range 100-150 ms.
5. Hat choke group: closed hat cuts open hat (MPC mute target / TR-8S standard).
6. Optional: 808 lane gets its own rhythm (not only kick copies) — trap/Metro style
   808s that land between kicks. Owner decision needed (touches 07-29 bassline history).
7. Optional: duck only below ~120 Hz (multiband) so the 808's grit stays audible.

## Sources
- majormixing.com/10-tips-for-mixing-808 (tune, saturate, sidechain, decay, mono <100 Hz, don't layer two 808s in one range)
- iconcollective.edu/808-mixing-tips (top kick over 808; kick transient first, 808 fades in)
- audeobox.com/learn/fl-studio/how-to-sidechain-in-fl-studio (4-6 dB, fast attack, 100-150 ms release)
- rolandcorp.com.au TR-8S guide (kick-triggered sidechain on bass track)
- mpc-forums.com / mpc-tutor.com (mute targets: closed hat chokes open hat)
