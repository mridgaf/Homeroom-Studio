# Chapter 09: Reason 12 manual digest and studio workflow
## Part 48 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 39 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 49 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 39 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      The Sidechain inputs.
      When a cable is connected to the Sidechain inputs the “KEY” button is activated automatically and the Dynamics
      section for the channel will now be “keyed” i.e. triggered by the external signal instead of the channel signal.
      For example, you could use a drum loop to trigger the gate for a channel playing a synth pad to create rhythmic chord
      effects.
      See “Using compression sidechaining” for a description of further uses of sidechaining.

      About Gain Reduction CV

      The Gain Reduction CV out connector on the back of a Mix Channel or Audio Track rack device can be used to mod-
      ulate other parameters with the amount of gain reduction applied by the compressor/gate. The gain reduction CV out
      can be used as an envelope follower as the CV follows the dynamics of the original signal.
      For example, try using gain reduction CV to control filter frequency for “auto-wah” effects.

      EQ section

      This is a four-band EQ with parametric midrange controls and high and low frequency shelving bands. The EQ can be
      switched between two operating modes, each with slightly different curve characteristics. There is also a filter section
      with low pass and high pass filters.
      The EQ can be placed before or after Dynamics in the signal path - see “Signal Path section”.
      The parameters are as follows:

      | Parameter                 | Description
      Spectrum EQ Window button Click this button to bring up the Spectrum EQ Window where you can edit the EQ and Filter parameters graphi-
                                cally, see “The Spectrum EQ Window”.
      LPF “ON” button              Activates/deactivates the low pass filter. A low pass filter lets low frequencies pass and cuts out the high frequen-
                                   cies.
      HPF “ON” button              Activates/deactivates the high pass filter. A highpass filter is the opposite of a lowpass filter, cutting out lower fre-
                                   quencies and letting high frequencies pass.
      LPF Frequency                The Low Pass filter (LPF) removes high frequencies from the signal, making the sound less bright. The LP filter
                                   has 12dB/Octave roll-off curve. Range is 100 Hz - 20 kHz.
      HPF Frequency                The High Pass filter (HPF) removes low frequencies from the signal, causing a thinner sound. The HP filter slope
                                   has a 18 dB/Octave roll-off. Range is 20 Hz - 4 kHz.
      FILTERS TO DYN S/C           See “About the Filters To Dynamics Sidechain button”.
      button
      EQ “ON” button               Activates/deactivates the EQ. (This does not affect the LPF/HPF filters.)
      “E” button                   When the “E” button is activated the EQ will have slightly different curve characteristics.
                                   In normal mode (E button deactivated), the Gain setting will also affect the bandwidth (Q) for the HMF and LMF
                                   EQ sections. The higher the gain, the narrower the bandwidth and vice versa. With E mode activated, bandwidth is
                                   constant at all gain settings. (Check out the difference in “The Spectrum EQ Window” if you like.)

      | Parameter                  | Description
          HF Gain/Frequency         The HF section provides high frequency shelving equalization. Frequencies above the set corner Frequency will be
                                    cut or boosted by the set HF Gain amount.
                                    The HF Gain control can cut or boost the selected frequency range +/- 20dB and the HF Frequency can be set
                                    between 1.5kHz - 22kHz.
          HF BELL mode              When this button is activated, the HF EQ will switch to peaking characteristics. This means it works like a regular
                                    parametric EQ band, cutting or boosting the signal around the set frequency. Bell mode has a fixed bandwidth or
                                    "Q" (see below).
          HMF                       The high medium frequency EQ is fully parametric. HMF Gain is adjustable +/- 20dB. Center frequency range is
          Gain/Frequency/Q          600 Hz - 7 kHz. The “Q” parameter adjusts the bandwidth around the set center frequency. Q range is 0.70 - 2.50.
                                    The higher the Q value, the narrower the affected frequency range - except in “E” mode (see above).
          LMF                       The low medium frequency EQ is also fully parametric. LMF Gain is adjustable +/- 20dB. Center frequency range
          Gain/Frequency/Q          is 200 Hz - 2 kHz. The “Q” parameter adjusts the bandwidth around the set center frequency. Q range is 0.70 -
                                    2.50. The higher the Q value, the narrower the affected frequency range - except in “E” mode (see above).
          LF Gain/Frequency         The LF section provides low frequency shelving equalization. All frequencies below the set Frequency will be cut
                                    or boosted by the set LF Gain amount.
                                    The LF Gain control can cut or boost the selected frequency range +/- 20dB and the LF Frequency can be set
                                    between 40 Hz - 600 Hz.
          LF BELL mode              This works in the same way as described above for the HF filter, but affects the LF filter.

      The Spectrum EQ Window
      The EQ section can also be displayed and edited “visually”. This is done in the Spectrum EQ floating window. Besides
      the EQ functionality, the Spectrum EQ also features a spectrum analyzer which displays the audio frequency content
      of the selected mixer channel in real-time. Here is how you can work with the Spectrum EQ:
      1. Select “Show Spectrum EQ Window” from the Window menu (or press [F2]), or click the Spectrum EQ Window
         button on the desired channel strip (see “Spectrum EQ Window button”) or on the device in the rack:
            The Spectrum EQ window shows up and the (pre-Fader) frequency content of the currently selected mixer chan-
            nel is displayed in gray during playback:

            The Spectrum EQ Window with audio playing back.
      !     The LPF and HPF buttons are only present when the “FILTERS TO DYN S/C” button is off.
      D     Click and drag the Spectrum EQ window frame to resize the window horizontally and vertically as desired.
      D     Select the desired mixer channel for the Spectrum EQ by selecting it from the drop-down list at the bottom of
            the window.

      !   If “Master Section” is selected, no controls are available in the window, since the Master Section lacks these.
      • If the “Follow Selection” checkbox is ticked, changing sequencer track, Mix Channel/Audio Track device in the
        rack, channel strip, or editing parameters on other channel strips will automatically change the Spectrum EQ
        Window focus to show the signal of the corresponding mixer channel.
      2. Tick the “EQ On” box to activate the EQ in the channel strip and bring up the parameters in the window.
          You can also activate the HPF and LPF Filters, E Mode, HF Bell mode and LF Bell mode for the selected mixer
          channel by ticking the corresponding check boxes in the window. The pictures below shows how the different ob-
          jects in the Spectrum EQ window correspond to the channel strip parameters:

          The Spectrum EQ Window with the Filters, EQ, E Mode, Bell Mode and Analyzer functions active during audio playback.

          The Spectrum EQ editing objects (points) and what parameter(s) they affect in the mixer channel strip.

      D   Click and drag any of the points in the window to change the frequency (and gain for the EQ points) value(s).
          Dragging sideways changes the frequency value and dragging vertically changes the gain (of the EQ points). As
          you edit the points, the corresponding channel strip parameter(s) are updated in real-time - and vice versa. The
          white line in the window shows the resulting EQ (and Filter, if activated) curve.
      • Hold down [Shift] and drag to constrain the movement to vertical and/or horizontal.
          This allows you to change either frequency or gain without affecting the other.
      D   [Ctrl]-click (Win) or [Cmd]-click (Mac) on an EQ point to reset its Gain value to 0dB.
      • When you hover over a point, its current values are displayed numerically in the Frequency, Gain and Q fields
        below the graph. The parameter’s (or section’s) name is also displayed at the bottom left in the window:
          (The point remains selected until you touch another point with the mouse or click on the window background.)

          The HMF EQ point is selected and highlighted in the window.
      !   Note that the Analyzer always shows the audio frequencies before the Fader section. This means that any Fil-
          ter and/or EQ changes you make will affect the displayed frequency content. Also, if you use any Insert FX,
          these could also affect the frequency content.
      D   Hold down [Alt](Win)/[Option](Mac) and drag an EQ point vertically to change its Q-value.
          This is only valid for the HMF and LMF EQ points, since these are the only ones that have a Q parameter.
      q   It is possible to record parameter automation in the sequencer by dragging the points around in the Spectrum
          EQ Window during recording. Just make sure you have created a sequencer track for the channel you want to
          automate. See “Parameter automation recording procedure” for more details.

      Insert FX section

      The channel strip Insert FX section allows you to add effect devices to be used as Insert Effects in the channel strip.
      You add Insert effect devices to the Audio Track or Mix Channel device in the rack. Insert effects process the whole
      channel signal, as opposed to Send effects where the effect is shared among all channels and the balance is individ-
      ually adjustable for each channel. Typical insert effects are compression, distortion and modulation effects such as
      chorus.
      The Insert effects can be placed ahead of the Dynamics and EQ sections in the signal path, see “Signal Path section”.
      • See “Insert FX” for descriptions of how to create and work with Insert effects.
      The Insert FX section in the channel strip contains the following parameters:

      | Parameter      | Description
      Bypass           Bypasses the Insert effect(s).
      Edit Inserts     This will bring the channel’s rack device into view with its Insert FX container opened, allowing you to edit the effect devices.

      FX Sends section

      Send effects, which are global for all channels in the Main Mixer, are connected to the Master Section rack device. Up
      to 8 Send effects can be used simultaneously. For a description of how to use Send effects, see “Send FX”.
      The FX Sends section contains the following parameters:

      | Parameter           | Description
      FX Send On 1-8         Activates the Send for the channel.
      Level 1-8              The Send Level knobs control the amount of channel signal that is to be sent to the effect connected to the corre-
                             sponding Send.
      PRE button             Send channel output is normally taken post channel fader, so that changing the channel's volume also changes the
                             send level. By activating the PRE button, the send output is taken pre channel fader. In this mode, the send level is in-
                             dependent of the channel fader.

      Fader section

      The Fader section is used for controlling the level of the channel and its stereo placement in the mix. The section has
      the following parameters:

      | Parameter              | Description
      Pan L/R                      Use this control to set the left/right position of the channel in the stereo field. [Ctrl]-click (Win) or [Cmd]-click
                                   (Mac) the Pan knob to reset to the default “0” (center position). The pan law is "-3dB compensated", with “com-
                                   pensated” meaning that the signal becomes +3dB louder when it's panned hard left/right compared to when it's
                                   completely centered.
      Width                        Width will only be available on stereo channels. It allows you to control the width of the stereo field for the channel.
                                   Normally this is fully on (value 127) which represents full stereo. By decreasing this value the stereo width is nar-
                                   rowed. Turned fully off the channel output will be in mono.
      MUTE/SOLO buttons        !     Note that the Mute and Solo functions in the Main Mixer are NOT the same as Mute
                                     and Solo of sequencer tracks (see “Muting tracks” and “Soloing tracks”).
                                   Clicking a channel’s Mute button silences the output of that channel. Click the button again to unmute the chan-
                                   nel.
                                   Clicking a channel’s Solo button silences all other mixer channels, so that you only hear the soloed channel. Sev-
                                   eral channels can be soloed at the same time, but if this is the case, note that soloed channels can’t be muted with
                                   the Mute button. To mute one of several channels in solo mode you simply “un-solo” it. There are also Mute All
                                   Off/Solo All Off buttons in the Master Section - see “Master Section Header”.
                                   If you are using Output Busses (see “Output Busses”) and/or Parallel Channels (see “Parallel Channels”), the Solo
                                   and Mute functions affect the other concerned channels in an intelligent way, see “Solo, Mute and Send FX logic”.
      Channel Fader                The channel fader is used to control the output level of each channel.
                                   By adjusting the faders, you can set the desired mix (balance) between channels.
                                   If a channel is an Output Bus (see “Output Busses”), the Fader section background is colored and the Fader knob
                                   is red.
      Channel Meter                The meter is a graphical representation of the channel output level. Stereo channels have two level bars and mono
                                   channels have one. If the signal level pushes the meter into the red, to avoid distortion try lowering either the out-
                                   put level of the device connected to the channel device or the channel fader itself. The meter is a VU meter, taking
                                   into account any VU offset set in the Big Meter of the Reason Hardware Device - see “The Big Meter”.
      Output Bus Selector          Here you can route the channel to an Output Bus (sub-mixer) instead of to the default Master Section, see “Out-
                                   put Busses”.

      About Level/Pan CV
      On the back of the Programmer section of a Mix Channel or Audio Track device you will find CV inputs for the chan-
      nel Level and Pan controls. These allow for automatic level and pan control from sources that output CV signals.
      D   Press [Tab] to flip the Rack around, then click the “Show Programmer” button to access the CV jacks.

      Changing Fader section parameters on multiple channels simultaneously
      In the Fader section you can change parameter values in a “ganged” or “linked” fashion on several selected Mix
      Channels. You can change the Mute, Solo and Level fader parameters this way. The example below shows seven se-
      lected channels, where the Level is reduced on the KorgBass channel and the rest of the channels’ Faders follow
      along (with the same amount of level change in dB for each channel):

      • If you don’t release the mouse button you can change the level back and the other channel faders will follow
        along as expected.
      !   If you lower the level to minimum (or raise to max) so that all faders reach their end values, and then release
          the mouse button, changing the level again will move all faders together equally.

      Channel Header section
      The Channel Header is always visible at the bottom of the channel strip. It contains the following items:
      The Edit Focus indicator - When you select a channel, the horizontal strip at the top of the Channel Header lights up
      red to indicate Edit Focus. The channel most recently clicked will have edit focus, regardless of how many channels
      are selected. When using [Ctrl](Win)-click or [Cmd](Mac)-click to deselect previously selected channels, edit focus
      will be on the most recently deselected channel.
      Edit Focus also reflects the last selected track or Mix device, which is useful when moving between work areas be-
      cause the channel with Edit Focus will always be in view in the Main Mixer. For example, if you select an ID8 track in
      the sequencer, the Mix channel to which it is connected will be scrolled into view in the Mixer, and will be given Edit
      Focus.

      The top strip is lit to indicate Edit Focus.
      • When you are using the Spectrum EQ Window, and the “Follow Selection” box is ticked, the channel with Edit
        Focus is displayed in the window, see “The Spectrum EQ Window”.
      The Remote Base Channel indicator - To the left in the same horizontal strip area a small yellow arrow symbol can be
      shown. This is the Remote Base Channel indicator, which shows which channel is considered the first or base chan-
      nel when using Remote Control - see “Setting the Remote Base Channel”.

      The Remote Base indicator.
      The RACK and SEQ buttons allow you to switch to a channel’s rack device or sequencer track directly from the mixer
      - see “Switching between channels, rack devices and tracks”.
      The Channel Header area reflects the selected Track Color (see “Coloring mixer channels”).
      You can rename the channel by double-clicking on the name (see “Naming mixer channels”).
      Note that the Channel Header is a little shorter if the channel is a Parallel Channel (see “Parallel Channels”).

      The Master Section strip

      The Master Section is where all your audio track and mix channels are mixed down to the Master Out bus. The Mas-
      ter Section strip contains a bus compressor and Insert FX section, both of which process the master bus, as well as
      send/return master level and pan controls for the eight FX Sends. Any processing applied to the master bus affects
      all channels that are routed to the Master Section.

      Master Compressor section

      The Master Compressor is perfect for providing the final “fairy dust” to your mix. It can add punch and cohesion, and
      generally make the mix sound bigger and more powerful. The compressor is very straightforward in operation and
      features make-up gain as well as program-adaptive Release.
      The Master Compressor can be applied pre or post Master Insert section - see “Master Inserts section”.
      The parameters are as follows:

      | Parameter           | Description                                                                         | Range
      On button             Activates/deactivates the Master Compressor.
      Meter                 The meter shows the amount of gain reduction in dB.                                    0dB - 20dB
      Threshold             This sets the level at which onset of compression occurs. The lower the Threshold,     -30dB to 0dB
                            the more compression will be applied.
      Ratio                 Ratio specifies the amount of gain reduction applied to signal levels above the set    Fixed Ratios:
                            threshold. A 2:1 compression ratio effectively means that a signal level 2dB above     2:1 / 4:1 / 10:1
                            threshold will have a signal gain of 1dB.
      Attack                This governs how quickly the Master Compressor will react when signals rise above Fixed settings (in ms):
                            the set threshold.                                                                0.1 / 0.3 / 1 / 3 / 10 / 30
      Release               When the signal level drops below the set threshold, this determines how long it        Fixed settings (in s):
                            takes before the compressor lets the sound through unaffected.                          0.1 / 0.3 / 0.6 / 1.2 /Auto
                            If set to “Auto”, the Release time will be program adaptive, so the Release time is au-
                            tomatically increased following long peaks and decreased following short peaks.
      Make-Up               Make-Up gain compensates for level reduction caused by compression and helps           -5dB to 15dB
                            maintain a steady output level.
      KEY button/External   When a cable is connected to the Sidechain inputs on the back of the Master Section
      Side Chain            device, the KEY button is activated automatically and the Master Compressor will
                            now be triggered by the external signal instead of the master bus signal. When a
                            sidechain source is connected you can turn the KEY button off to monitor the side-
                            chain signal.
                            See “Using compression sidechaining” for a description of how sidechaining can be
                            used.

      FX Send section

      This section controls the master levels of the FX Sends. Send effect devices are connected to the Master Section via
      the eight FX Send and eight FX Return connectors on the back of the rack device.
      See “Send FX” for a description of how to set up an use Send FX.
      The Send bus can be monitored via the Control Room output - see “Control Room output section”.
      The section contains the following items:

      | Parameter           | Description
      Level 1 - 8            Adjusts the FX Send master level. The master send levels are normally left at default 0dB. if you wish to increase/de-
                             crease the effect balance, this is best done by increasing/decreasing the send levels for the individual channels using
                             the effect.
      Meter                  Shows the signal level of the send bus.
      EDIT button            This brings the connected effect device in the rack into view for easy editing of its parameters.
      Name label             This automatically shows the name of the connected effect device. If you enter a new name for the label, this over-
                             rides the automatic naming. Deleting a manually entered name will bring back the automatic naming.

      Master Inserts section

      The Master Inserts Section is identical to the Insert FX section in the channel strips, except that it affects the master
      bus, i.e. the whole mix. Master Insert effects are ideally used to apply mastering effects, such as compression and lim-
      iting/maximizing for finalizing the mix.
      Master Insert effect devices are added to the Master Section device in the rack.
      The Master Insert effects can be placed ahead of the Master Compressor in the signal path. By default, the Master
      Insert effects are placed after the Master Compressor in the signal path. This makes sense, as you usually add a
      Maximizer or Mastering Combinator as a Master Insert effect, and this must be last in the signal path to avoid clipping
      on the output. However, if necessary, you can place the Master Insert effects before the Master Compressor, by ac-
      tivating the "Inserts Pre Compressor" button.
      • See “Insert FX” for descriptions of how to create and work with Insert effects.
      The Inserts section in the Master Section contains the following parameters:

      | Parameter            | Description
      Bypass                  Bypasses the loaded Insert effect(s).
      Edit Inserts            This will bring the Master Section device into view in the rack, with its Insert FX container opened, allowing you to edit
                              the effect devices.
      Signal Path button      If activated, the “Inserts Pre Compressor” button will place the Inserts before the Master Compressor in the signal
                              chain. If the Master Insert effects contain a maximizer or limiter, the inserts should normally be last (this button should
                              be left in the off position).

      FX Return section

      This section controls the master levels of the FX Returns. Send effect devices are connected to the Master Section
      via the eight FX Send and eight FX Return connectors on the Master Section device. See “Send FX” for a description
      of Send FX.

      Send/Return connectors on the Master Section device.
      You can monitor the Return bus via the Control Room output - see “Control Room output section”.
      The section contains the following items:

      | Parameter           | Description
      Level                  Adjusts the FX Return master level. The master return levels are normally left at the default value, 0dB. If you wish to in-
                             crease/decrease the effect balance, this is best done by increasing/decreasing the send levels for the individual chan-
                             nels using the effect. You can, however, use the FX Return level to change the overall balance of a send effect in the
                             mix.
      Pan                    Pan adjusts the return signal stereo balance.
      Meter                  Shows the signal level of the return bus.
      EDIT button            This brings the connected effect device in the rack into view for easy editing of its parameters.
      Mute (M)               This mutes the return signal for the send effect.
      Name label             This automatically shows the name of the last effect device in the send signal path. If you enter a new name for the la-
                             bel, this overrides the automatic naming. Deleting a manually entered name will bring back the automatic naming.

      Master Fader section

      The Master Fader controls the final output level of the mix to be recorded or exported to a file. It should normally be
      set to 0dB. The Master Fader should never be used to adjust the monitoring level - this is what the Control Room bus
      is for (see below).
      The section contains the following items:

      | Parameter              | Description
      Master Fader             Adjusts the level of the Master Out bus.
      Meter                    Shows the level of the Master Out bus.
      Mode                     The Mode button switches the meter between VU/Peak/PPM modes - see “The Big Meter”.
      Reset                    This resets the meter, deleting any registered peaks.

      Spectrum EQ (Spectrum Analyzer) Window button

      Below the Meter is a button for bringing up the Spectrum EQ Window. Since there are no Filter or EQ sections in the
      Master Section, the Spectrum EQ Window is used only for displaying the frequency content of the Master Section.

      Control Room output section
      The Control Room outputs are located on the back of the Master Section device. To use the Control Room output
      section, the outputs have to be connected to your monitor system. This can be done by manually patching cables
      from the “Ctrl Room Out” connectors to a separate output pair on the Reason Hardware Device - see “Manual audio
      routing”.

      The Control Room outputs, which are separate from the Master Out bus, are the outputs that you should monitor (lis-
      ten) from. This allows you to monitor the main mix and to adjust your monitoring level without affecting the Master
      Out bus. You can also monitor the FX Send or Return buses in this section.

      The section contains the following items:

      | Parameter                   | Description
      Monitor display/selector for Click the display to bring up a list where you can select what to monitor on the Ctrl Room Out jacks. You can se-
      Master/FX Send 1-8/FX Re- lect between Master, FX Send 1-8 and FX Return 1-8. One bus can be monitored at a time.
      turn 1-8
      Control Room Out Level         Adjusts the level of the Control Room Out bus.

      Delay Comp
      D   Click the Delay Comp button (or display) to activate delay compensation in the Main Mixer.
          The total delay of the Main Mixer signal (at the Master Out) is displayed below the display. See the “Delay Com-
          pensation” chapter for more information about delay compensation in Reason.

      Master Section Header

      The Header is always visible at the bottom of the Master Section. It contains the following items:

      | Parameter                | Description
      SEQ / RACK                  The RACK and SEQ buttons allow you to switch to the Master Section rack device or automation track directly from
      buttons                     the mixer - see “Switching between channels, rack devices and tracks”.
      Mute/Solo All Off           This allows you to switch off all channel Mute or Solo buttons in one go.
      DIM -20dB                   This simply dims the Master Out level -20dB. Use this to temporarily lower the output level when answering the
                                  phone, etc.

      Automating mixer parameters
      Automating mixer parameters works in the same way as for other parameters. Automation is part of the audio track
      or Mix channel track. See “Recording parameter automation”.
      D   A quick way to automate a parameter is to right-click (Win) or [Ctrl]-click (Mac) on the parameter and select
          “Edit Automation” from the context menu.
          This will create an automation lane (and track if needed) where you can record or draw automation.
      • When you select a sequencer track, the “Record Enable Parameter Automation” button is automatically en-
        abled, allowing for parameter automation to be recorded. However, when recording automation for Audio
        Track channel strip parameters, you may want to disable the regular Record Enable button to avoid recording
        audio by mistake.


=== END OF PART ===
