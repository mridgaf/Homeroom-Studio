# What EQ and effects the Original side adds when it renders (2026-10-29)

> **UPDATE same day (owner):** NEW beats now skip all mix EQ (house + DJ/genre), the 120 Hz chord cut, Doc Day's punch shaper, the darker soft hits, and all dirt. Kept: kick duck, master stage, snare reverb, echo, chorus, phaser, glue. Old beats rebuild as made. The tables below describe the chain BEFORE this change.

Read from the code (`tools/crew.py` render_crew_beat, `tools/make_drum_loops.py` master, `tools/groove.py`, `tools/beat_machine.py`). Nothing rendered or measured. In run order:

## On EVERY Original beat (all 45 DJs / Legends / genres)
| Step | What it does | Setting |
|---|---|---|
| Chord/melody low cut | cuts everything under 120 Hz on chords + melody, so the bass owns the bottom | 120 Hz high-pass |
| Sidechain duck | mix dips each time a real kick hits (ghost kicks don't) | 0 to 35% deep, per DJ |
| Reverb on the snare ("space") | one per beat, rolled: gated 31%, dry 31%, room 18%, plate 9%, hall 10%. Genres always use their own (21 gated, 10 dry, 8 room, 4 washed/plate, 2 plate). A typed word ("dry", "room") wins | usually snare/backbeat lanes only |
| Mix EQ | +1.5 dB lows (120 Hz), -1 dB at 800 Hz, +2 dB highs (8 kHz). 6 identities have their own (below) | house default |
| Glue compressor | whole mix, gentle | -18 dB threshold, 1.8:1, +2 dB makeup |
| Master tone | +air shelf above 9 kHz (up to +35%), small dip 300-900 Hz (up to -15%), stereo below 200 Hz made mono | always |
| Master drive | soft clip. Clean DJs: 0.7 (basically none). Dirt DJs: their own 1.1-1.8 | |
| Loudness | pushed to -12 LUFS, soft-clipped under a -4 dB ceiling | always |
| Bass mono | everything under 120 Hz made mono, last step | always |

Also: soft chord/bass hits play slightly darker (written loud/soft, 2026-10-29). Extra random moves per beat: Haas width on hats/percs 20%, hat ratchets 15%, kick layer 15%; a long kick gets a short kick's snap on 7 in 10 beats.

## Only some identities
- **Own mix EQ (6):** Otto Grit, Crate Prophet, Razor = highs -1.5 dB (darker). Cutz = highs 0. Doc Day = +1 dB lows at 100 Hz, +2 highs. J Dillo = +2 dB lows, highs -4 dB at 7 kHz (much darker).
- **Doc Day only:** harder glue (4:1) and a transient shaper on kick + snare.
- **Backbeat echo (5):** Otto Grit, Cutz, Crate Prophet, Chrome Dial (1/8 note, 20% wet); Rage Engine (1/16, 16%).
- **Chorus (4):** Otto Grit (snare/clap/chords), Glass Cat, Night Metro, Half Light (chords).
- **Phaser on hats (3):** Sunday Chop, New Math, Fast Water.

## Dirt ("clean renders" is the house rule, but 19 opt out)
Full dirt (vinyl crackle, wow, mix saturation, SP-1200 grit, hot master, 808/kick distortion): Otto Grit, Cutz, Crate Prophet, Rage Engine, Kane East, J Dillo, Razor, Memphis, Houston Screw, Acid Rap Detroit, Horror Rap, Trip Hop, Baltimore Club, Detroit, Chiptune.
Kick/808 distortion only, mix stays clean: Night Metro, Mustang, Crunk, Emo Hip Hop.
Everyone else: no dirt at all.

## Not on the Original side
Loops-only beats are fully clean for everyone (no dirt, no echo/chorus/phaser); only mix EQ + glue move with mood words.

## Stems vs the WAV
The stems skip the mix glue, master drive and loudness push (they're for Reason). Wow and dust print on each stem for dirt DJs; vinyl gets its own stem.
