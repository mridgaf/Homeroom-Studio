# Chapter 09: Reason 12 manual digest and studio workflow
## Part 75 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 66 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 76 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 66 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Tips and Tricks
      Creating an individual “pre amp envelope” for a Sound Engine
      There might be situations where you want to control the amplitude envelopes separately for each Sound Engine.
      Let’s say you have a plucked sound with a fairly long release in Sound Engine 2 and then you want to slowly fade in
      a pad sound from Sound Engine 1. Since the built-in Amp Envelope controls all three Sound Engines together, you
      could use the following “workaround”:
      1. Assign “Envelope 1” as Source and “Mixer: Eng1 Level” as Destination in the Modulation Bus.
          Turn the Amount knob to 100 in the Modulation Bus.

      2. Create your “fading” envelope curve in the Envelope 1 display.
          Click the Sustain button in the Envelopes display if you want to have a sustain stage in your envelope.

      3. Set the Sound Engine 1 Mixer Level slider to zero.

      4. As you play the keyboard, Envelope 1 will now fade in the signal from Sound Engine 1, while the signal from
         Sound Engine 2 is only controlled by the built-in Amp Envelope.

      !   Note that the built-in Amp Envelope’s settings will also affect the “fading pad” sound from Sound Engine 1,
          since all Sound Engine signals eventually pass through the Amp Envelope.

      Recording display movements in the sequencer
      If you are in “experimentation mode” and want to try out some wild waveform and/or Spectral Filter tweaking, you can
      record automation of your interactive display movements in the sequencer:
      1. Record some notes on the sequencer track in the Reason sequencer and then hit Stop twice.
      2. Hit Record again in the Reason sequencer and click and drag in the Waveform display during recording:

      3. Hit Stop in the sequencer twice when you are done recording.
        Any vertical movements have now been recorded as Shape parameter automation and any horizontal movements
        have been recorded as Modifier 1 Amount parameter automation.
      4. If you like, hit Record again in the Reason sequencer and click and drag in the Spectral Filter display during
         recording:

      5. Hit Stop in the sequencer twice when you are done recording.
        Any vertical movements have now been recorded as Spectral Filter Resonance parameter automation and any
        horizontal movements have been recorded as Spectral Filter Frequency parameter automation.


---

<a id="grain-sample-manipulator-31"></a>

=== END OF PART ===
