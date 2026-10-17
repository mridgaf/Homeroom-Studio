# Matrix Pattern Sequencer

Classic step sequencer. Up to 32 steps, 32 pattern memories (4 banks × 8).
Sends Note CV + Gate CV (plays one voice of an instrument) and a separate Curve
CV lane that can move any parameter with a CV input.
Source: Reason 12.7 Operation Manual, ch. 66, pp. 1359–1372.

## Key controls
Named exactly as Reason's Remote layer names them.

- **Run**: start/stop (also starts with the transport).
- **Pattern Enable**: mute/unmute the pattern.
- **Bank A** / **Bank B** / **Bank C** / **Bank D**, **Pattern 1** … **Pattern 8**: pick the pattern (automatable for song arrangements).
- **Resolution**: step length (e.g. 1/16).
- **Pattern Shuffle**: swing on/off (amount from ReGroove global shuffle).

## Panel (not Remote)
- Keys/Curve switch: draw notes (upper) and gate velocities (lower), or the Curve lane.
- Steps (1–32), Tie per step, Octave switch.
- Back: Unipolar/Bipolar curve switch; Curve CV out to e.g. a filter's CV input = stepped filter pattern.

## Handy tricks from the manual
- Matrix Gate → ECF-42 Env Gate and Curve → Freq CV = pattern-controlled filter.
- Curve CV steps after a zero step also fire gates — use it to trigger samples.

## Where it shines / falls short
Shines: quick mono riffs and stepped modulation. Falls short: mono; the main sequencer is easier for real parts.
