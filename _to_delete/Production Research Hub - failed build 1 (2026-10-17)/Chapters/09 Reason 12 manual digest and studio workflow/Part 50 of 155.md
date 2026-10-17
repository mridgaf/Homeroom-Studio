# Chapter 09: Reason 12 manual digest and studio workflow
## Part 50 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 41 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 51 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 41 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

                                  Parallel                                                          Parallel

      The Drums Clean Output Bus is manually muted.                  Now, if you also manually mute the Drums SubMix Output Bus,
                                                                     the Send FX outputs of all channels that eventually end up in the
      Since the Drums Clean output bus is connected to an un-
                                                                     Drums SubMix Output Bus will be automatically muted.
      muted Parallel Channel, the Drums Dist channel, the Send FX
      outputs of the Kick, Snare and Overhead channels are not
      muted. However, if you should manually mute the Drums Dist
      channel, the Send FX outputs of the Kick, Snare and Overhead
      channels should be automatically muted.

      Remote controlling the Main Mixer
      There are two ways of Remote controlling the Main Mixer: one channel at a time, for detailed control of the parame-
      ters of one mixer channel at a time, or multiple channels simultaneously, for balancing levels etc.

      Remote controlling a single mixer channel
      You can control a single mixer channel, either by locking your control surface to the mixer channel, or by setting Mas-
      ter Keyboard Input to the mixer channel’s track in the sequencer.
      For example, if you set Master Keyboard Input to the audio track you’re recording on, you will be able to adjust the
      monitor level and other parameters of the channels you're using when recording.
      The extensive Remote control functionality in Reason allows for detailed control of the parameters of one mixer
      channel at a time.

      Remote controlling multiple mixer channels
      The typical way of remote controlling the Main Mixer is to control the Master Section (by setting Master Keyboard In-
      put to the Master Section track in the track list, or typically by locking your control surface). This lets you control the
      Master Section parameters plus mixer parameters for a number of channels (often 8 channels at a time, depending
      on the control surface). To define what channels to remote control at a given time, you need to set the “Remote Base
      Channel”.

      Setting the Remote Base Channel
      The first (leftmost) mixer channel controlled by Remote is called the “Remote Base Channel”. The current Remote
      Base Channel is indicated by a yellow arrow symbol in the mixer channel strip Header section:

      The Remote Base Channel indicator.
      To change the Remote Base Channel, proceed as follows:
      D   Select a mixer channel and select “Set Remote Base Channel” from the Edit menu or context menu.
          The Remote Base Channel indicator will move to the selected mixer channel.
      D   Alternatively, change Remote Base Channel via Remote (in steps of 1 or 8 channels).
          Functions for changing the Remote Base Channel may already be mapped to buttons on your control surface -
          see the “Control Surface Details” pdf document. If not, you can set this up manually in the Additional Remote Over-
          rides dialog on the Options menu - see “Additional Remote Overrides...”.

      Remote controlling multiple mixer channels - an example
      If you want to remote control several channel strips at once from your control surface, you can proceed as follows:
      D   Select the Master Section device in the rack or the Master Section Strip in the Main Mixer.
          If you want to lock your control surface to the Master Section, select “Lock Xxxxx to This Device” from the Edit
          menu or context menu. (“Xxxxx” represents the name of your connected control surface.) This way, you can ensure
          that your control surface will always control the Main Mixer, regardless of where the edit focus is.

          Selecting and locking the Master Section to the connected control surface.
      Depending on your connected control surface, it may now be possible to control parameters of several channel strips
      at the same time. In this example, we’re using a control surface which has nine sliders. These sliders are configured
      to control one channel strip Level Fader each, plus the Master Section Level Fader.
      In the picture below, the Remote Base Channel is currently set to Audio Track 1. This means we can control the Level
      Faders of Audio Track 1 through Audio Track 8, plus the Master Section Level Fader, with the nine sliders on the
      control surface:

      Remote
      Base
      Channel

                                                                         Remote controlled channels

      Controlling Audio Track 1 through Audio Track 8 and Master Section from the connected control surface.

      On our control surface it’s possible to select next and previous Remote Base Channel in steps of 8 channels. If we
      click the “Next” button on our control surface, the Remote Base Channel is set to Audio Track 9 and we can now
      control Audio Track 9 through Audio Track 12, plus the Master Section:

                                                        Remote Base Channel                        Remote controlled channels

      Controlling Audio Track 9 through Audio Track 12 and Master Section from the connected control surface.
      If your control surface doesn’t have buttons already assigned for controlling Remote Base Channel selection, you can
      manually assign controllers for this by using the Remote Override function described in “Remote Override mapping”.
      Alternatively, select a channel strip and select “Set Remote Base Channel” from the Edit menu or context menu.
      See “Remote - Playing and Controlling Devices” for more details about remote controlling Reason. See also the “Con-
      trol Surface Details” pdf document for information about parameter assignments on various common control sur-
      faces.

      Advanced routing tips and tricks
      Chaining Send effects from Redrum or Mixer devices
      The Redrum Drum Module and the Mixer 14:2 and 6:2 devices have separate Send FX connectors where you can
      add send effects individually for each device. The Redrum and Mixer devices also have separate Send FX level pots
      for each drum/mixer channel so that you could set the send effect levels individually for each drum/mixer channel in
      the device.
      Let’s say you want to add a Redrum device and use two of the Main Mixer’s Send FX, but with individual settings for
      each of the Redrum device’s internal channels. In the example below, we’re going to chain the two Send Outs from
      the Redrum device to two send effects in the Main Mixer:
      1. Create two extra Mix Channel devices - one for each of the send effects we’re going to chain.
          In this example we name the Mix Channel devices “FX 1 Chaining” and FX 2 Chaining”.
      2. Activate the Send FX bus you want to use in each of the mixer channels and also activate the corresponding
         Pre-fader button.
          In this example, we activate the Send FX 1 bus on the FX1 Chaining channel and the Send FX 2 bus on the FX 2
          Chaining channel. The Send FX 1 has a reverb connected and the Send FX 2 has a delay connected.
      !   The PRE buttons should be activated because we don’t want the mixer channel faders to affect the Send lev-
          els.
      3. Lower the “FX 1 Chaining” and “FX 2 Chaining” mixer channel faders to zero.
          This way, the effect signals won’t be mixed with the rest of the Main Mixer channel signals in the mix bus, but are
          kept isolated in the Send FX busses. Now, our setup should look like this in the rack and in the Main Mixer:

          The device setup, plus two new Mix Channel devices added. To the right, the channel strips with activated FX Send busses.

      4. Connect the Send Out 1 and 2 of the Redrum device to the Left inputs of each of the “FX 1 Chaining” and “FX
         2 Chaining” Mix Channel devices.
        Now, you should have a setup that looks something like this:

        The Redrum Effect Sends chained to one Send FX bus each of the Master Section, via two new Mix Channel devices.
      5. Set individual Send levels for each of Redrum’s internal channels.

        Now, you have individual send levels for each of the Redrum device’s internal channels - and are still able to use
        the Send FXs in the rest of the Main Mixer channels like before.

      Using compression sidechaining
      Compression sidechaining is a feature which lets you control the Compressor, not from the internal channel signal,
      but from an external signal. A typical use case would be to let the signal from a kick drum channel control the com-
      pression of the bass channel. The result would be that the bass signal is compressed each time the kick drum signal
      is present on the sidechain input, allowing the kick sound to momentarily suppress the bass sound.

      Compression sidechaining from an external channel
      The example below shows an audio track with a kick sound that is tapped from the Kick Audio Track device’s Parallel
      output and routed to the Dynamics Sidechain input of the Bass Audio Track device.
      • The Key button is automatically activated when you connect a signal to the Sidechain Input.
        This will force the Compressor to be controlled from the Sidechain input signal rather than from the internal signal.

        Compression Sidechaining of the Bass audio track from the Kick Drum audio track.

      About compression sidechaining of several channels from one source channel
      If you want to use compression sidechaining of several (destination) channels from a single source channel, there are
      some options of doing that:
      • If you are already using both Parallel outputs for sidechaining, tap an additional sidechain signal from one of
        the Insert FX “To Device” outputs of the source channel.
        This is useful if you are not using both “To Device” outputs for insert effects in the source channel.
      • Use a “Spider Audio Merger & Splitter” device to split the sidechain signal from the Parallel outputs and/or In-
        sert FX “To Device” output into several signals.
        Each of these signals can then be individually routed to each Sidechain Input of the desired destination Audio
        Track/Mix Channel devices.
      • Create an Output Bus (sub-mixer) and route all (destination) channels you want to control to this Output Bus.
        Then, route the sidechain signal from the source channel device to the Sidechain Input of the Output Bus Mix
        Channel device.
        See “Output Busses” for information.

      About internal compression sidechaining
      Another typical application for compression sidechaining is to use the internal signal of the channel, filter it, and then
      feed to the compressor via “internal” sidechaining. This type of internal sidechaining can be used for de-essing, for
      example. No additional patching is required for this; you only have to activate the “Filters to Dynamics Sidechain” but-
      ton in the Filter or EQ sections. See “About the Filters To Dynamics Sidechain button”.

      Using the Mix Channel and Audio Track devices’ Direct Outs
      The Mix Channel and Audio Track devices feature Direct Out connectors. By patching cables into these outputs, you
      break the internal signal chain from the device to the Master Section, and can route the channel output signals di-
      rectly to the Reason Hardware Device’s outputs. This is a very nice feature if you want to use outboard mixing or
      summing, to route individual channel signals to another application.

      The example below shows how to route the Direct Outs of a number of Audio Track devices to separate outputs of
      the Reason Hardware Interface:

      Direct routing of individual channel outputs to individual outputs on the Reason Hardware Interface.
      !   Using the Direct Outs will break the internal P-LAN routing to the Master Section device. This is indicated by
          the red dashes (---) in the Audio Output display on the Audio Track/Mix Channel devices.

      Creating an input channel for recording with effects
      When you record on an audio track, the input signal is routed “dry” to the audio track. Then, when you play back the
      recorded audio, the signal goes via the channel strip, with all its settings and any Insert FX etc. However, there might
      be situations where you want to record a processed signal to the audio track. For example, if you record an electric
      guitar, you might want to record it with distortion effects or similar.
      The example below shows a typical setup where a separate Mix Channel device is used for processing the input sig-
      nal before it’s routed to the audio track for recording:
      1. Begin by creating an Audio Track device and a separate Mix Channel device.
          The Mix Channel device is going to be used for housing the effects we’re going to record with.
      2. Create the effect(s) you want to use and patch them as Insert FX in the Mix Channel device.
          In this example, we use a Scream 4 distortion device and an RV7000 reverb device connected in series.

      3. Connect one of the Audio Ins of the Reason Hardware Interface to the “Input L” of the Mix Channel device.
        This manual patching from the Hardware Interface is made to route the input signal directly to the Mix Channel de-
        vice, where we have our effects.

        Direct routing of an Input signal from the Reason Hardware Device to the Mix Channel device.
      4. Flip the rack around to view the front.
      5. Click the “Rec Source” button on the Mix Channel device.
        This makes the Mix Channel device selectable as input source for the Audio Track device.

        Rec Source enabled on the Mix Channel device.

      6. Finally, select the Mix Channel device as Input on the Audio Track in the sequencer (or in the Audio Input se-
         lector on the Audio Track device in the rack).
        This will route the signal from the Mix Channel device’s output directly to the input of the Audio Track.

        The Mix Channel device selected as audio input on the Audio Track in the sequencer.
        Now, you can begin recording on the Audio Track according to the standard recording procedures described in
        “General recording procedure”. The signal will be processed by the Insert FX of the Mix Channel device before be-
        ing recorded on the track.
        With this setup, you will always hear the sound of the input processed through the Amp device - just as if you had
        a real hardware amp turned on and mic'ed in the studio. If you don't want the “Lead Gtr Rec Input” Mix channel to
        be heard, just mute it in the Main Mixer.

500   THE MAIN MIXER


---

<a id="delay-compensation-18"></a>

=== END OF PART ===
