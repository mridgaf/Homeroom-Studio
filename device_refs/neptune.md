# Neptune (Pitch Adjuster and Voice Synth)

Vocal pitch corrector (natural to hard "robot"), pitch shifter (±1 octave), formant
control, and a Voice Synth that turns one sung line into MIDI-played harmonies.
Monophonic input only.
Source: Reason 12.7 Operation Manual, ch. 54, pp. 1197–1220.

## When you'd use it
- Tuning a vocal to a key (insert on the vocal track).
- The hard auto-tune effect: Correction Speed max, Preserve Expression min.
- Octave-up or -down dub on a send (Transpose ±12 + Formant).
- Harmony stacks played from the keyboard (Voice Synth).
- Pitching drums or other non-pitched audio (Transpose only, Pitch Adjust off).

## Key controls
Named exactly as Reason's Remote layer names them.

- **Pitch Adjust On/Off**: the corrector.
- **Correction Speed**: slow = invisible; ~12 o'clock = natural; fast = stepped robot.
- **Preserve Expression**: how much of the singer's own vibrato survives fast correction.
- **Catch Zone**: how far off (±20–600 cents, default ±100) a note can be and still get pulled to the scale. Outside it passes untouched.
- **Scale Memory**: 4 memories of Root/Scale/Catch Zone — automate to change key mid-song. (Root and Scale themselves: Chromatic, Major, Natural/Harmonic Minor, Dorian, Mixolydian, or click your own notes.)
- **Pitch Adjust Amount**: correction amount.
- **Transpose On/Off** / **Semitones** / **Cent**: fixed pitch shift, ±1 octave.
- **Formant On/Off** / **Formant Shift**: keeps the voice natural after big shifts; Shift alone = "gender" change without pitch change.
- **Low Freq Input**: better tracking for deep voices (more latency).
- **Wide Vibrato**: ignore heavy vibrato when detecting pitch.
- **Live Mode**: lowest latency for singing through it live (slightly lower quality).
- **MIDI Destination**: MIDI notes go "To Pitch Adjust" (force the sung note to the key you hold) or "To Voice Synth" (harmonies).
- **Pitched Signal Level** / **Voice Synth Level**: output mix of the corrected voice and the harmonies.
- **Pitch Bend** / **Pitch Bend Range** / **Mod Wheel** / **Vibrato Rate**: bend and add vibrato to the corrected voice.
- **Enabled**: bypass/on/off.

## Notes
- MIDI control needs its own sequencer track: right-click > Create Track for Neptune.
- Voice Synth ignores the Pitch Adjust/Transpose/Formant settings and has its own outputs on the back.
- The sequencer's Pitch Edit mode can also correct audio graphically.

## Where it shines / falls short
Shines: fast in-rack tuning, the classic hard-tune sound, instant harmonies.
Falls short: chords, polyphonic or noisy material — it only tracks one note at a time.
