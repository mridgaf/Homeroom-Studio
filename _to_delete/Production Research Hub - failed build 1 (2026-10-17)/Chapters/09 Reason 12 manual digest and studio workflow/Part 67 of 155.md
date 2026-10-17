# Chapter 09: Reason 12 manual digest and studio workflow
## Part 67 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 58 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 68 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 58 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      The Overdrive/Resonator is a combined distortion and resonator module. It can be used to add a nice distortion to
      the input signal. There is also a resonator section with a number of selectable characteristics, similar to the Body sec-
      tion in the Scream 4 Sound Destruction Unit. The parameters are as follows:
      • Drive
        Sets the overdrive distortion amount.
      • Resonance
        Sets the resonance amount for the resonator.
      • Size
        Sets the size of the virtual “resonance chamber”, from small to large.
      • Model
        Click to select one of five different resonator “body” characteristics.

      Connections
      On the back panel of Kong are a number of connectors. Many of these are CV/Gate related. Using CV/Gate is de-
      scribed in the chapter “Routing Audio and CV”.

      Sequencer Control
      The Sequencer Control CV and Gate inputs allow you to play Kong from another CV/Gate device (typically a Matrix
      or a Redrum). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers note on/
      off along with velocity.

      Modulation Input
      These control voltage (CV) inputs (with associated voltage trim pots), can modulate various Kong parameters from
      other devices. These inputs can control the following parameters:
      • Volume
        This controls the Master Level in Kong.
      • Pitch
        This controls the Pitch Bend wheel in Kong.
      • Mod
        This controls the Mod Wheel in Kong.

      Aux Send Out
      The two stereo Aux Send Outputs can be used for connecting external effect devices for external signal processing.
      The signal levels to these Aux Send Outputs are controlled from the Aux 1 and Aux 2 Send knobs on the Drum Con-
      trol Panel, see “The Drum Control Panel”.

      Gate In and Out
      • The Gate Inputs can receive a CV signal to trigger each of the 16 pads individually.
        You are still able to control the pads from the panel and/or via MIDI even when the Gate Inputs are being used.
      • The Gate Outputs send out a CV Gate signal each time the corresponding pad is played.
        The Gate signals can be used for triggering sounds in other devices.

      Audio Out 3-16
      There are 14 separate audio output jacks on Kong’s back panel - arranged as seven separate stereo pairs. These
      outputs are never auto-routed but can be manually connected and selected as individual outputs for any of the Drum
      channels by using the Drum Output selector in the Drum and FX section, see “Signal flow”.

      Main Audio Out
      These are the main audio outputs. When you create a new Kong device, the Main Audio Output pair is auto-routed to
      the first available mixer channel.

      Using Kong as an effect device
      Besides using the wide array of internal sound possibilities in Kong, you can also use it as an external effect device.
      If you unfold the Drum and FX section and flip the rack around, a set of additional audio jacks are visible at the bot-
      tom of the back panel.

      These audio jacks can be used for connecting external devices and processing their audio in Kong. As you can see,
      the signal flow for processing external audio is printed on the back panel. Even if you want to use Kong for process-
      ing external signals, you can still play and use its internal Drum channels just like before.
      Proceed as follows to connect an external device for audio processing in Kong:
      1. Connect the outputs of your other device (a synth, for example) to the Audio Inputs to the left.
        If your device only has a mono output, connect it to the Left Audio Input on Kong.

      2. Play a couple of notes on your other device.
          The audio is now routed via Kong’s Bus FX slot and further via the Master FX slot, to the Main Audio Outputs of
          Kong.
      3. Select suitable FX devices for the Bus FX and Master FX slots in Kong according to the descriptions in “The
         FX modules” and tweak the parameters to your liking.
      D   By connecting CV signals to the Parameter inputs in the Bus FX and Master FX sections on the back of the
          panel, you can modulate the first two parameters on the selected FX modules, see “Using CV modulation of
          Bus FX and Master FX parameters”.
          Attenuate the CV signal with the corresponding knobs next to the modulation jacks.

      Using external effects with Kong
      It’s also possible to hook up an external effect device in the signal chain to process the Kong audio, or to process any
      external audio routed via the Audio Inputs to the left on the unfolded back panel of Kong.
      D   Connect the external effect device to the External Effect Outputs and Inputs.
          In the picture below, an RV7000 Reverb is connected to Kong’s External Effect section allowing the RV7000 to
          process the signal between Kong’s internal Bus FX and Master FX slots:

          An RV7000 Reverb connected to Kong for processing the Kong audio signals
      !   Note that if you have selected “Master FX” or “Separate Out” as output in the Drum Output selector, the BUS
          FX Send knob on the Drum Control Panel controls the signal level also to the External Effect, see “Signal
          flow”.


---

<a id="redrum-drum-computer-28"></a>

=== END OF PART ===
