# Mimic

Fast "creative sampler" with eight slots. Each slot holds one sample and has
its own pitch, stretch, filter, envelopes, LFO and a lo-fi effect. Best for
chopping: drop a loop in, it slices it on the hits, each slice lands on a key.
Source: Reason 12.7 Operation Manual, ch. 32, pp. 787–816.

Samples are referenced, not saved in the patch.

## When you'd use it
- Chopping a loop or break into slices and replaying them (Slice mode).
- Eight one-shots on pads, drum-machine style (Multi Slot mode).
- Re-pitching a vocal or melody and keeping its speed (Vocal / Melody stretch).
- Tape-stop and lo-fi texture.

## Slot modes (Play Mode)
- **Pitch**: one slot played chromatically.
- **Slice**: one slot's slices across the keys from C1 (up to 92 slices).
- **Multi Slot**: keys C–G in every octave fire slots 1–8, unpitched.
- **Multi Pitch**: up to 8 slots layered/split across the keyboard, pitched.

## Key controls
Named exactly as Reason's Remote layer names them. The number is the slot
(1 shown; every one exists for slots 1–8).

- **Play Mode**: the four modes above (whole device).
- **Start Pos 1** / **End Pos 1**: play region.
- **Reverse 1**: play backwards.
- **Loop On 1** / **Loop Length 1** / **Loop Xfade 1**: loop at the end of the sample/slice.
- **Global Pos 1**: new notes continue from the playhead — keeps polyphonic chops in time.
- **Start Mod 1**: move the start earlier/later by modulation.
- **Snap Slices 1**: start points snap to slice markers.
- **Slice Sens 1**: auto-slicing sensitivity (more = more slices).
- **Play Thru 1**: on = a slice keeps playing past the next marker while held.
- **Stretch Mode 1**: Tape (speed = pitch), Advanced (full mixes), Melody (mono lines, clean loops), Vocal, Granular.
- **Stretch Speed 1** / **Speed Mod 1** / **Speed ModAmt 1**: playhead speed (0% = stopped/tape stop) and its modulation.
- **Transients On 1**: Preserve Transients (Advanced/Melody).
- **Voice Formant 1**: Vocal stretch — smaller/bigger "body" (child ↔ adult).
- **Voice Fixed 1**: Vocal stretch "Fixed Pitch" — auto-tunes the sample to the key you play.
- **Grain Len 1**: Granular stretch grain size.
- **Pitch Semi 1** / **Tune 1** / **Pitch Kbd 1** / **Pitch Mod 1**: pitch ±24 semitones, keyboard tracking, modulation.
- **Filter Type 1** / **Filter Freq 1** / **Filter Reso 1** / **Filter Drive 1** / **Filter Env 1**: 8 filter types incl. comb; drive and envelope depth.
- **Filter Attack 1** / **Filter Decay 1** / **Filter Sustain 1** / **Filter Release 1**: filter envelope.
- **Hi Cut 1** / **Lo Cut 1**: quick band limiting.
- **Amp Attack 1** / **Amp Decay 1** / **Amp Sustain 1** / **Amp Release 1** / **Amp Gain 1** / **Amp Velocity 1**: volume envelope.
- **Pan 1** / **Pan Mod 1**: pan and its modulation.
- **LFO Rate 1** / **LFO Wave 1** / **LFO Beat Sync 1** / **LFO Synced Rate 1** / **LFO Key Sync 1** / **LFO Delay 1**: per-slot LFO.
- **Effect Type 1** / **Effect Mix 1** / **Effect Mod 1**: per-slot lo-fi effect and amount.
- **Send1 1**: send to the Send 1 output (back panel).
- **Key Mode 1**, **Portamento Mode 1** / **Portamento Rate 1**, **Pitchbend Range 1**, **Master Volume**.

## Back panel
Separate out per slot, two send outputs — each chop can go to its own mixer channel.

## Where it shines / falls short
Shines: fastest way to chop and flip his own loops — directly useful for the
beat workflow. Falls short: huge multisampled instruments — NN-XT.

## Pairs well with
Channel Dynamics / Pulveriser on the output, The Echo in Roll mode for fills.
