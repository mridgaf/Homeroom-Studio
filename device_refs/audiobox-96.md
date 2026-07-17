# PreSonus AudioBox USB 96 (your audio interface)

The blue metal box. It's the middleman between microphones/guitars and the
Mac: mics plug into the front, sound comes out the back to your speakers or
headphones. "96" just means it can record at up to 96 kHz quality.

## Make Reason use it — once per machine

1. Reason menu → **Settings/Preferences → Audio**.
2. Set **Audio Output** (and Input) to **AudioBox USB 96**.
3. If the sound crackles, raise the **Buffer Size** one notch and try again.
   Bigger buffer = safer sound but more delay when you play keys.

## The front knobs, in plain words
- The two knobs by the inputs are **gain** — how loud the mic or guitar
  comes IN. Turn up until the light flickers green while you play or sing;
  if it ever goes red, turn it back down — red means distortion is being
  recorded and no knob can fix it later.
- **Mixer** knob: blends "what's going in RIGHT now" (turn toward Inputs —
  no delay, good for singing) with "what the Mac plays back" (turn toward
  Playback).
- **48V button**: phantom power. ON for condenser mics (the sensitive
  studio kind). OFF for guitars and most stage mics.
- **Main** knob: speaker volume. **Phones** knob: headphone volume.

## Recording a take into Reason
Create an audio track, click its little input picker, choose AudioBox
input 1 (or 2), arm the track (red dot), check the meter moves when you
make noise, press record. If the meter doesn't move: wrong input picked or
gain knob all the way down — it's always one of those two.
