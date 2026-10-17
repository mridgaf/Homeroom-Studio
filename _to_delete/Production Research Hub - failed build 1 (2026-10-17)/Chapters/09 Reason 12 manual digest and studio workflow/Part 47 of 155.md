# Chapter 09: Reason 12 manual digest and studio workflow
## Part 47 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 38 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 48 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 38 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 17: The Main Mixer

The Main Mixer

      About this chapter
      This chapter describes the various procedures, parameters and functions in the Main Mixer as well as the relationship
      between mixer channels and the Audio Track/Mix Channel devices in the rack. The chapter also covers how to set up
      and use Insert and Send effects, as well as some advanced routing tips and tricks.

      Overview

      The Main Mixer is a fully equipped mixer with pro features to meet the most demanding mixing needs. You can have
      an unlimited number of channels, each with advanced eq and dynamics control.
      The mixer can be viewed as a remote control for Audio Track and Mix Channel rack devices. This is where you control
      levels, make eq and effect settings etc., although the devices themselves “live” in the rack.

      The Audio Track, its device and mixer channel strip
      Audio Tracks and their associated rack devices are for recording/playing back audio.
      When you create a new Audio Track, a corresponding Audio Track device is added to the rack and an Audio Track
      channel strip is added to the Main Mixer.
      The track, device and channel strip all belong together. If you delete the device, the corresponding track and channel
      strip are also deleted.

      An Audio Track in the sequencer with its corresponding rack device and channel strip in the Main Mixer.
      • Audio Track devices have no audio inputs on the back - the audio is fed internally to the Audio Track device
        from the associated sequencer track.

      The Mix Channel device and channel strip
      A Mix Channel device acts as a host to a source device (e.g. an instrument device). When you create an instrument,
      a Mix Channel device is added automatically to the rack and a corresponding Mix Channel strip is added to the Main
      Mixer. You can also create Mix Channels manually from the Devices tab in the Tool Window or from the Create menu.
      This is useful if you need to make manual mixer routings - see “Advanced routing tips and tricks” at the end of this
      chapter.
      The Mix Channel device has inputs to which the source (instrument) device is connected. The Mix Channel device
      and channel strip will automatically be assigned the name of the connected source device, but this can be changed -
      see “Naming mixer channels”.
      A Mix Channel device will not automatically have a corresponding track created in the sequencer (but the connected
      source device will). Mix Channel tracks are created manually and used for automating channel strip parameters - see
      “Automating mixer parameters”.

      A Mix Channel device (with an ID8 source device connected) and the corresponding channel strip in the Main Mixer.

      The Master Section device and mixer strip
      The Master Section device is always present and is fixed in the rack, just below the Reason Hardware Interface. This
      is where all your Audio Track and Mix channels are summed and mixed to stereo, and where you set up your Send ef-
      fects and Master Insert effects. For descriptions of how to set up and use effects, see “Insert FX” and “Send FX”.
      The corresponding Master Section mixer strip is also fixed and is always visible to the right in the Main Mixer.
      The Master Section track is used for automating Master Section parameters - see “Automating mixer parameters”.

      The Master Section device and mixer strip.

      Navigating in the Main Mixer
      Viewing the Main Mixer area
      There are several ways to bring the Main Mixer area into view:
      • By dragging the gray Rack header downwards to reveal the mixer area.
      • By pressing [F5] on your keyboard or selecting “View Main Mixer” from the Windows menu.
      • By clicking the Show/Hide icon on the gray Mixer header.
      • To view the mixer in a separate window, either click the Detach icon on the Mixer header, select “Detach Main
        Mixer Window” from the Windows menu or hold down [Ctrl](Win) or [Cmd](Mac) and press [F5].

      Scrolling and navigating in the Main Mixer
      The Channel Strip Navigator and Mixer scrollbar allow you to navigate between channels in the Main Mixer or to fo-
      cus on a specific channel strip area. The Channel Strip navigator area can be shown/hidden using the “Show Navi-
      gators” Options menu item.
      The Channel Strip Navigator is the miniature mixer and channel strip area at the far right of the Main Mixer window.
      The blue rectangle shown inside the area acts much in the same way as a scrollbar in standard document windows.
      If you move the pointer inside the rectangle the pointer changes to a hand, allowing you to click and scroll. You can
      also click anywhere in the Navigator area to immediately get to the desired destination.

                                                   Channel Strip Navigator

                                                   Mixer scrollbar
      • The Mixer scrollbar allows you to scroll between all the channels in the mixer.
        The Mixer scrollbar will only show and scroll the regular channel strips - the Master Section is always visible and
        fixed to the right in the Main Mixer area.
      • The Channel Strip Navigator area allows you to scroll between the various channel strip sections (channel strip
        sections can also be hidden, see below).
        All areas of the channel strips and Master Section can be scrolled, except the Channel Header section (the area
        below the faders) which is always visible at the bottom. If the Main Mixer is detached, the fader section is also al-
        ways visible and stays at the bottom.
      • Alternatively, you can use a mouse scroll wheel or a trackpad to scroll.
      • The [left]/[right] arrow keys can be used to move between channels
      • The [Page Up]/[Page Down] keys can be used to scroll vertically.
      • The [Home] and [End] keys will scroll the mixer to the leftmost and rightmost channel strip, respectively.

      Showing and hiding channel strip sections
      Channel strips are divided into sections, which can be globally shown or hidden in the mixer. This enables you to hide
      sections that you don’t need to tweak or to focus on specific sections. Hiding a section does not alter the mixer func-
      tionality in any way, sections are still active when hidden.
      Each section has a section name header in the channel strip. The sections are as follows (from the top down): Input,
      Dynamics, EQ, Inserts, FX Sends and Fader. (See “The channel strip” for descriptions of each section.)
      The section headers are always visible even if a section is hidden, as is the channel header (name label) section be-
      low the faders. Note that if the Main Mixer is detached from the rack, the fader section cannot be hidden.

      Section headers in the channel strip. A red light to the right of the section header name indicates that the section is in use for the channel.
      Here, all sections are hidden (except the Fader section), so that only the section headers are visible.
      There are two ways to show/hide channel strip sections:
      D   By using the Show/Hide buttons in the bottom right corner of the Channel Strip Navigator.
          Each button enables you to show or hide the corresponding section. Hidden sections are indicated by grayed-out
          buttons. Hold down [Alt](Win) or [Option](Mac) and click on any of the buttons to show or hide all sections in one
          go. Hold down [Ctrl](Win) or [Cmd](Mac) and click on a button to show this section and hide all other sections.

          The Show/Hide buttons. Here, the EQ section is hidden.
      D   By double-clicking a section header in the channel strip.
          This will also show or hide the corresponding section.
      • Showing/hiding channel strip sections affects all channel strips, including the Master Section strip.

      Differences between the channel strips and the Master Section strip
      Showing/hiding mixer strip sections also affects the Master Section strip. There are a few differences in the Master
      Section and the channel strip sections when using the Show/Hide buttons:
      • There is no Input section in the Master Section. If the Input section is shown, the Master Section will display a
        blank panel.
      • The “EQ” Show/Hide button affects the FX Send section in the Master Section.
      • The “FX Sends” Show/Hide button affects the FX Return section.

      Switching between channels, rack devices and tracks
      The RACK and SEQ buttons allow you to go to a channel’s rack device or sequencer track directly from the Main
      Mixer. Both buttons are located in the Channel Header section of the Main Mixer:

      If you click the RACK button the following happens:
      D   For Audio Track channels, this will bring the Audio Track rack device into view.
          The rack area will be shown (if hidden) with the channel device in view.
      D   For Mix channels, this will bring the Source device (i.e. the instrument device connected to the channel) into
          view.
          [Shift]-clicking the RACK button for a Mix channel will instead bring the Mix Channel device into view.
      The SEQ button allows you to go to a channel’s sequencer track from the mixer. The SEQ button is also located in the
      Channel Header section. If you click the SEQ button the following happens:
      D   For Audio Track channels, this will bring the Audio Track into view.
          The sequencer area will be shown (if hidden) with the track in view.
      D   For Mix channels, this will bring the track for the Source device into view.
          [Shift]-clicking the SEQ button for a Mix channel will instead bring the Mix Channel automation track into view. If
          there isn’t an automation track, one will automatically be created.
      D   If you have previously deleted Mix Channel tracks and/or Audio tracks in the sequencer, clicking the SEQ but-
          tons on the corresponding channel strips in the mixer will automatically create new sequencer tracks.
      To find the mixer channel for a specific track in the sequencer, or for a specific Mix Channel or Audio Track device in
      the rack, proceed as follows:
      1. Select the track in the sequencer, or select the Mix Channel/Audio Track device in the rack.
      2. Bring the mixer into view.
          The channel will get Edit Focus (see “Channel Header section”) and be scrolled into view in the Main Mixer. If you
          have both the sequencer and Main Mixer in view, or the rack and Main Mixer, clicking a track in the Track List, or
          on a Mix Channel/Audio Track device in the rack, will flash the corresponding channel strip in the Main Mixer.

      Managing mixer channels
      Creating and deleting channels
      Mixer channel strips are automatically created when you create Audio Track and Mix Channel devices. In most situa-
      tions, a Mix Channel device (with its channel strip) is also automatically created when you create an instrument de-
      vice (see “Creating devices”).
      To delete a channel, proceed as follows:
      D   Select the channel strip in the Main Mixer, or select its device in the rack, and press [Delete] or [Backspace].
          Alternatively, select “Delete Channels and Tracks” from the Edit menu or context menu.
          This will delete the channel strip, device and associated track. An alert appears asking you to confirm deletion.
          If there are devices connected to the Mix Channel device you delete, and “Auto-group Devices and Tracks” is se-
          lected on the Options menu, the alert will ask if you want to delete only the selected device, or all devices in the
          Device Group (see “About Device Groups” for more information).

      Selecting channels
      To select channels in the mixer you can use any of the following methods:
      D   Clicking anywhere on a channel strip (including parameters) will select the channel.
          If you are not editing parameters but want to select a channel, the channel header is a good place to click. You
          could also click anywhere on the channel strip background (where there are no parameters or displays).
      D   If the Main Mixer has focus, you can use the left and right arrow keys to select channels.
          The selection will move to the next adjacent channel (left or right) with each keystroke.
      D   It is possible to select several channels, by using standard [Shift], or [Ctrl](Win) or [Cmd](Mac) selection tech-
          niques.
          This allows you to e.g. change the Fader levels of all selected channels simultaneously (see “Changing Fader sec-
          tion parameters on multiple channels simultaneously”), or move or delete several channels in one go. The last se-
          lected channel will be given edit focus which is indicated by a red strip in the channel header (see “Channel
          Header section”).
      D   To select all channels, use the “Select All Channels” item on the Edit menu or channel strip context menu.
          The Main Mixer must have focus for this item to be available.

      Moving channels
      To move channels in the Main Mixer, simply select them and use standard drag and drop method. A red insertion line
      will show the insertion point, exactly like when moving devices in the rack or tracks in the sequencer.

      Moving a channel. The thicker red line indicates where the moved channel will be inserted.

      Displaying channels, devices and tracks in the same order
      Channel strips in the mixer, Audio Track and Mix Channel devices and tracks can be independently re-ordered. This
      allows you to set up the main work areas according to your preferences.
      Should you wish to display mixer channels, devices in the rack and tracks in the same order, proceed as follows:
      1. Select the area where everything is in the order you want reflected in the other areas.
          This could either be the Main Mixer, the sequencer or the rack.
      2. Use the “Select All” Edit menu item.
          This menu item would be “Select All Devices” if the rack is selected, or “Select All Channels” if the mixer is se-
          lected. You could also select channels, tracks or devices manually.
      3. Select the “Sort Selected Device Groups” Edit menu item.
          Channels, devices and tracks will now all be presented in the same order as the area you selected in the first step.

      Copying and duplicating channels
      Cut, Copy and Paste functions
      Selected channels can be moved or copied using the “Cut/Copy/Paste Channels and Tracks” functions on the Edit
      menu or channel strip context menu. This allows you to copy one or several channels from one Song document to an-
      other. The following rules apply:
      D   Cut and Copy affects all selected channels, and behaves according to the standard procedures.
          Cut moves the channels to the clipboard, removing them from the rack, sequencer, and mixer, while Copy creates
          copies of the channels on the clipboard, leaving the originals as they were.
      D   If the “Auto-group Devices and Track” option is activated on the Options menu, this will copy the channel’s en-
          tire Device Group, including tracks and clips - see “About Device Groups”.
      D   If no channel is selected when pasting, channels will be added to the left of existing channels in the Main
          Mixer.
          If a channel is selected when pasting, the copied channel(s) will be inserted to the right of the selected channel.

      Duplicating channels
      D   To make a duplicate copy of a mixer channel, with its settings and Insert FX (if any), hold down [Ctrl](Win) or
          [Option](Mac) and drag the channel to where you want it.
          Several selected channels can be duplicated. You can also select “Duplicate Channels and Tracks” functions on
          the Edit menu or mixer context menu.
      D   If the “Auto-group Devices and Track” option is activated on the Options menu, this will duplicate the chan-
          nel’s entire Device Group, including tracks and clips - see “About Device Groups”.

      Copy channel settings
      If you wish to copy mixer channel settings from one channel to another you can use this function.
      1. Select the channel you wish to copy settings from.
          Copy channel settings only works when a single channel is selected, if several (or no) channels are selected the
          function is not available.
      2. Select “Copy Channel Settings >” on the Edit menu or channel context menu.
          On the submenu you can select to copy channel settings from a single section (Dynamics, Filters and EQ, Insert
          FX or FX Sends), or “All”, which copies everything including any Insert FX devices with their settings.
      3. To paste the settings, select the channel you wish to copy channel settings to, then select “Paste Channel Set-
         tings” on the Edit menu or mixer context menu.
          The type of settings you copied will be reflected in the paste menu item, e.g. “Paste Channel Settings: EQ” if you
          only copied the EQ section.
      D   The copied channel settings remain on the clipboard (until you cut or copy again) so you can paste them to
          other channels if you so wish.
          This can only be done with one selected channel at a time - pasting channel settings is not possible if several
          channels are selected.
      D   Copying channel settings can also be done by selecting an Audio Track or Mix Channel device in the rack.
          The procedure is the same. You can copy settings from a device to a mixer channel or vice versa.

      Resetting channel settings
      Resetting channel settings initializes all channel strip parameters to default values and removes any insert effects
      (see “Insert FX section”) from the channel.
      D   To initialize a mixer channel (or Mix Channel/Audio Track device), select “Reset All Channel Settings” from the
          Edit menu or channel/device context menu.
          Channel settings reset is not possible if several channels are selected.
      !   Any Output Bus routings are not affected (see “Output Busses”).

      Naming mixer channels
      New Audio Tracks will by default be named “Audio Track + number”. When creating an Instrument, the Mix channel
      will take its name from the patch of the connected Instrument device.
      D   To enter a new name for a channel, double-click the name in the channel header.
          A text field opens allowing you to enter a name for the channel.
      Channel names are reflected - and can be changed - in all areas; the Track List., the Main Mixer and in the device.
      Mix Channel source devices and tracks have independent names from the Mix Channel device/channel strip. By de-
      fault, a Mix channel takes its name from its source device (typically, the instrument device connected to it). If you
      change the name of the source device, the Mix channel name will change too.

      If you want the source device and Mix channel to have different names, change the name of the Mix channel. To re-
      turn to the default state (and use the source device name for the Mix channel), just delete the Mix channel name.
      !   There are special naming conventions when you are using Parallel Channels, see “Naming Parallel Channels”.

      Coloring mixer channels
      Mixer channels are shown with the same color as their corresponding rack devices and tracks. The color is shown in
      the channel header and channel strip section headings:

      A channel strip with all sections folded, except for the Fader section.
      • You can change the color for a channel by selecting it and using the Channel Color submenu on the Edit menu
        or context menu. This will also change the color of the corresponding rack device and track (and vice versa).
      • For Mix Channels connected to a source device (e.g. an instrument), the Channel Color submenu has a special
        setting called "Mirror Source Track Color". If this is on, any color settings you make will be reflected both in the
        source device (the instrument device and track) and in the channel strip.
          This is true regardless of whether you change the color in the mixer, in the rack or in the sequencer.
      • To make independent color settings for Mix Channels, turn off "Mirror Source Track Color" first.
          For example, this is useful if you have a Redrum with separate outputs connected to different Mix Channels, and
          want these to have different colors in the mixer.
      !   If you change the color of an Output Bus channel, this will be reflected in the Output areas on all other chan-
          nels connected to that Output Bus, see “Creating an Output Bus”.

      The channel strip
      The channel strip is divided into sections, each marked with a section header. Mix Channel and Audio Track channel
      strips have identical parameters. Here is a detailed rundown of the parameters and functions in each section.

      Input section

      Input Gain
      | Parameter                | Description
      Gain                       This sets the input gain for the channel. Range is +/- 18 dB. If Gain is set to any other value than the default 0,0 dB
                                 or Invert Phase is on (see below), a LED is lit to the right in the section header to indicate the section is active.
      INV (Invert Phase)         This inverts the phase of the input signal to correct eventual phase problems. For example, using multiple micro-
                                 phones during recording can sometimes cause phase-cancellation between microphones picking up the same sound
                                 source but at slightly different distances. Phase problems are most noticeable when signals are summed to mono. Out
                                 of phase signals are indicated by a lack of lower frequencies and a generally “hollow” sound quality.

      Signal Path section
      The Dynamics, EQ and Insert effect sections will by default process a channel signal in that order, i.e. the order of the
      sections as shown in the channel strip (from the top down). By using the buttons in this section, the signal path order
      can be changed internally.

      | Parameter                   | Description
      Insert Pre                     If this button is activated, the Insert effects are placed before the Dynamics and EQ sections in the signal path.
      Dyn Post EQ                    Activating this button places the EQ before the Dynamics and Insert sections in the signal path.
      Insert Pre + Dyn Post EQ       If both buttons are activated, the order will be Insert, EQ and lastly Dynamics.
      FILTERS TO DYN S/C             See “About the Filters To Dynamics Sidechain button”.

                                                              The displays illustrate the selected
                                                              signal path order of the processing
                                                              for each channel.

      Dynamics section

      Each channel strip has a powerful dynamics section featuring compression/limiting and gating/expansion. The upper
      part of the section (with a white background) is the compressor/limiter, and the lower part (gray background) is the
      gate/expander. The compressor and gate processing can be independently switched in or out of the circuit.

      Compressor/Limiter
      Compressors reduce dynamic range by evening out the difference between loud and quiet signals. This makes signal
      levels easier to balance, and can add punch and sustain to the sound.
      The Main Mixer’s compressor/limiter is a flexible processor which has soft-knee (a gradual, smooth onset of com-
      pression) characteristics but can be switched to peak limiting, where levels above the set threshold are instantly re-
      duced. The compressor also features automatic make-up gain.
      The parameters are as follows:

      | Parameter              | Description
      Comp “ON” button          Activates/deactivates the compressor.
      RATIO                     Sets the amount of gain reduction applied to the signal above the set Threshold. The Ratio can be set from 1:1 (no
                                reduction) to Infinite:1.
      PEAK button               When activated this changes the signal detection from RMS to Peak, which results in an instant attack time. Peak
                                mode is suitable for compression of sounds with fast attacks like drums.
      THRES (Threshold)         This sets the level at which onset of compression occurs. Signals below the Threshold setting are unaffected, but
                                when the level exceeds the threshold, compression kicks in.
                                Range: -52 dB to 0 dB
                                Automatic make-up gain (based on the Ratio and Threshold settings) is applied to compensate for level reduction
                                caused by compression and maintain a steady output level.
      REL (Release)             Release determines the time it takes before the compressor lets the sound through unaffected after the signal
                                level drops below the set threshold. Set this to short values for “pumping” compressor effects, or to longer values
                                for a smoother change of the dynamics. Range: 100ms to 1000ms.
      FAST button               Attack - the time it takes for the compressor to react when signals rise above the set threshold level. If the FAST
                                button is activated the attack will be fixed at 3ms for 20 dB gain reduction.
      Meter                     The right LED meter shows the gain reduction applied by the compressor.

      Gate/Expander
      Gating or expansion will attenuate signals below a set threshold; the opposite of compression. It can be used to re-
      duce or eliminate unwanted background noise that may be present when there is no signal to mask it. Gating is also
      commonly used to reduce microphone “bleeding”, e.g. when recording a close-mic’ed drum kit you can use gating to
      silence the tom microphones when the toms aren’t being played to tighten up the sound, and for special effects like
      “keying” (see below).
      Higher expansion ratios (10:1 and above) are referred to as noise gating, where the channel is completely silenced
      if the level drops below the set threshold.
      The Gate/expander has the following parameters:

      | Parameter                | Description
          Gate “ON” button       Activates/deactivates the gate.
          RANGE                  Sets the amount of gain reduction applied to signals below the set Threshold. The Range can be set from 0dB (no
                                 reduction) to -40dB. If the EXP button is on (see below), the RANGE knob sets the expansion amount.
          EXP button             When activated this changes the operating mode from Gate to Expansion. The RANGE knob (see above) then
                                 sets the expansion amount.
          THRES (Threshold)      This sets the level at which the gate opens or closes. Signals below the Threshold setting are gated, but when the
                                 level exceeds the threshold, the gate opens.
                                 Range: -52 dB to 0 dB
                                 Note that the threshold for closing the gate is slightly lower than the threshold for opening the gate. This is to
                                 avoid undesirable gate triggering with signal levels close to the set threshold.
          REL (Release)          Release determines the time it takes for the gate to go from open to fully closed. Fast release times will fade the
                                 signal abruptly once the level falls below the threshold, and longer release times will slowly fade out the signal.
                                 Range: 100ms to 1000ms.
          FAST button            Attack - the time it takes for the gate to open - is normally1.5ms per 40dB. If the FAST button is activated the at-
                                 tack will be 100µs (microseconds) per 40 dB, which is useful for percussive material were the waveform rises
                                 steeply in a very short time.
          HOLD                   This determines the time the gate stays fully open after the signal falls below the threshold. Hold interacts with
                                 the Release parameter such that Release only starts acting after the set Hold time.
                                 Range: 0ms to 4000ms.
          Meter                  The left LED meter shows the gain reduction applied by the gating/expansion.

      About the Filters To Dynamics Sidechain button

      When this button (found in both the Input and EQ sections) is activated, the Low Pass and High Pass filters can be
      used to filter the channel sidechain signal before the dynamic processing.
      The channel signal itself will not be directly affected by the filters, only the sidechain signal. The filtered sidechain sig-
      nal is what triggers the dynamic processing, but the dynamic processing is applied to the channel signal. This allows
      you to use frequency sensitive compression.
      By trimming low and/or high frequencies you can specify which frequency range should trigger the compressor or
      gate. A typical application of frequency sensitive compression is “de-essing” where harsh sibilants in vocal material
      are reduced or eliminated. This is done by filtering the Sidechain signal so that only high frequencies (“s” noises) will
      trigger the compressor.
      !     When the “Filters To Dyn S/C” is active, the LPF and HPF buttons are not available in the Spectrum EQ Win-
            dow, see “The Spectrum EQ Window”.

      The Key button and the Dynamics Sidechain inputs
      You can use external signals to trigger the Dynamics section. This is done by connecting an external signal output to
      the Sidechain inputs on the back of the Mix Channel or Audio Track rack device.


=== END OF PART ===
