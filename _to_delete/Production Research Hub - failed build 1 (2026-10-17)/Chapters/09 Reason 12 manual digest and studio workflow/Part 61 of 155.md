# Chapter 09: Reason 12 manual digest and studio workflow
## Part 61 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 52 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 62 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 52 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 24: Synchronization and Advanced MIDI

Synchronization and
Advanced MIDI

      About this chapter
      This chapter describes how to synchronize Reason to external MIDI Clock or Ableton Link and how to sync external
      equipment from Reason’s internal MIDI Clock. The chapter also describes how to use the External Control Bus inputs
      for advanced MIDI routing.

      Synchronization to MIDI Clock
      What is synchronization and MIDI Clock?
      Synchronization, in this context, is when you make Reason play at the same tempo as another MIDI device; where
      both start, stop and can locate to certain positions, together. This is done by transmitting MIDI Clock signals between
      Reason and the other device. MIDI Clock is a very fast “metronome” that can be transmitted in a MIDI cable. As part
      of the MIDI Clock concept there are also instructions for Start, Stop and locating to sixteenth note positions.
      You can set up synchronization between Reason and hardware devices (tape recorders, drum machines, stand alone
      sequencers, workstations etc.) and other computer programs running on the same or on another computer.

      Host/Device
      In a synchronized system there is always one Host and one or more Devices. In our case, the host is the one that con-
      trols the tempo. In other words, it is only the tempo setting on the host that is of any relevance, since the devices fol-
      low the host's tempo.
      • Reason can act as Host or Device. That is, Reason can transmit MIDI Clock signals and also receive them.

      Using Reason as MIDI Clock Host
      Reason can transmit standard MIDI Clock signal. It also sends Start, Stop, Continue and Song Position Pointer (SPP)
      MIDI messages so that you can also control the transport functions of the synced equipment from the Transport
      Panel in Reason. To set up Reason as a MIDI Clock host, proceed as follows:
      1. Select the desired MIDI Port from the Output drop-down menu in the “MIDI clock sync” section on the Sync tab
         in Preferences.

        Selecting MIDI clock output port.
      2. Close the Preferences window.

      3. Select “Sync -> Send MIDI Clock” from the Options menu:

      D   Alternatively, click the Send Clock button in the Sync Mode section on the Transport panel:

          Now, you have set up Reason as a MIDI Clock sync master. When you start the Reason sequencer, MIDI Clock is
          sent out on the selected MIDI Out Port.
      D   If your synced MIDI equipment is not in phase with the Reason sequencer, you might have to change the Out-
          put Offset in the “MIDI clock sync” section on the Sync tab in Preferences.

      D   If the external MIDI equipment lags, set the Output Offset to a negative value.
          A negative Output Offset means that the MIDI Clock signal is sent out from Reason earlier to compensate for the
          lag.
      D   If the external MIDI equipment plays ahead of the Reason sequencer, set the Output Offset to a positive value.
      There are also some additional options regarding the MIDI Clock signal that can be selected at the bottom of the
      MIDI clock sync section:

      • Send MIDI clock while sequencer is stopped.
          When this box is checked, Reason continues to send out MIDI clock signal also when the sequencer is stopped.
      • Send song position pointer.
          When this box is checked, Reason sends out MIDI Song Position Pointer information to the device. If the synced
          device doesn't support Song Position Pointer, turning this setting off can improve synchronization. This is also use-
          ful if the synced device is playing a looped pattern and should disregard all positioning.

      • Send stop/continue when repositioning.
          When this box is checked Reason sends out Stop/Song Position Pointer/Continue messages to the synced de-
          vice, if the song position locator in the sequencer is moved (either manually or when in Loop mode) when the se-
          quencer is running.
          If unchecked, only Song Position Pointer messages are sent out if the song position locator is moved (or in Loop
          mode) while the sequencer is running.

      Syncing Reason to an external MIDI application or instrument
      This example assumes that you have an external device, such as a drum machine, hardware sequencer, another com-
      puter, tape recorder etc., that transmits MIDI Clock signals to which you want to synchronize Reason.
      1. Connect the device via USB/MIDI to the computer running Reason.
      2. Set up the host so that it transmits MIDI Clock signals to the MIDI Out you just connected to the computer run-
         ning Reason.
      3. In Reason, pull down the Edit menu (under macOS, the Reason menu) and open the Preferences dialog. Click
         the Sync tab.

      4. Pull down the MIDI Clock Input pop-up and select the MIDI Input to which you connected the host.
      5. Close the dialog.
      6. Activate MIDI Clock Sync from the Options menu - “Sync” submenu in Reason.
      7. Activate playback on the host.
          Reason will start playing in sync with it.
      D   If the Reason sequencer lags or plays ahead of the host, adjust the Input Offset on the Sync page in Prefer-
          ences, see “Adjusting for Latency”.

      Syncing Reason to another program on the same computer
      This section describes how to use MIDI Clock to synchronize Reason to another application running on the same
      computer.
      !   Note that synchronization via MIDI Clock makes the two programs play at the same time, that is, they both
          “run” when you “hit play”. It does not mean they can both play audio at the same time.
      Proceed as follows:
      1. Set up the host, so that it transmits MIDI Clock to Reason:
          Under Windows this is done by selecting one of the MIDI routing utility ports.
      2. In Reason, open the Preferences - Sync page.
      3. Pull down the MIDI Clock Input pop-up and select the corresponding MIDI port.
      4. Close the dialog.

      5. Activate MIDI Clock Sync from the Options menu - “Sync” submenu in Reason.
      6. Activate playback on the host.
          Reason will start playing in sync with it.
      D   If the Reason sequencer lags or plays ahead of the host adjust the Input Offset on the Sync page in Prefer-
          ences, see “Adjusting for Latency”.

      External synchronization considerations
      Adjusting for Latency

      Because of MIDI latency problems, you might need to adjust Reason’s playback in relation to the sync host, so that
      they are in perfect time. The tempo will not differ between the two, but Reason might play ahead or behind the other
      application. You might need to adjust this. However, this is something you only need to do once. The setting is stored
      with your other preferences, so you don’t need to adjust it again.
      Proceed as follows:
      1. Set up the other application so that it generates a solid click, on for example quarter or eighth notes, prefera-
         bly with a special sound on the downbeat.
          This click can either come from an internal metronome or from a MIDI source. If you use a MIDI source, make sure
          you pick one that has solid MIDI timing.
      2. Set up Reason so that it plays a similar rhythm as the other application.
          You might for example use the sequencer Click or a Redrum drum computer for this.
      3. Start the two applications in sync.
      4. Make sure you hear both applications at approximately equal level.
      5. Open the Preferences dialog in Reason and click the Sync tab.
      6. Trim the “Input Offset” setting until the “clicks” from the both sources sound at exactly the same time.
      7. Close the Preferences dialog in Reason.

      If Latency Compensation isn’t enough
      There might be situations where you can’t compensate enough in Reason to make two software applications run in
      sync. This might especially be true if the other application is an audio sequencer, that is if it can record and playback
      both audio and MIDI.
      This problem is an indication of the fact that the other application has not been set up properly and that its audio play-
      back is not in sync with its own MIDI playback.
      !   This is not something that you can or should compensate for in Reason. Instead, follow the instruction in-
          cluded with the other application to make sure its MIDI playback and audio playback are correctly locked to
          each other.

      About the beginning of the Song
      Due to the latency phenomenon, described in “About latency”, Reason needs some time to correct its playback speed
      when it first receives the Start command. This can be noted as a small glitch in the audio playback, when the program
      starts. If this is a problem, you need to insert a couple of empty measures at the beginning of the Song. Proceed as
      follows:
      1. Set the Left Locator to “1. 1. 1.0” and the right Locator to “3. 1. 1.0“.
      2. Click somewhere in the main sequencer area to move the menu focus to the sequencer.
      3. Select “Insert Bars Between Locators” from the Edit menu.
      4. Set up the other device/application, so that it also plays two empty bars at the beginning.

      About MIDI Song Position Pointers
      MIDI Clock actually consists of five type of messages: The actual clock (the metronome that establishes the tempo),
      Start, Stop and Continue commands and Song Position Pointers. This last type of message contains information
      about positions, so that a program for example “knows” where in a Song to start playback from.
      Normally, this ensures that you can locate to any position and activate playback from there. In older devices, Song Po-
      sition Pointers might not be implemented. This means that you will be able to synchronize properly only if you start
      both devices from the absolute beginning of the song.

      About Tempo and Tempo Changes
      Again, due to the latency phenomenon, Reason needs a bit of time to adjust to changes in tempo. If there are abrupt
      changes in the MIDI Clock, due to drastic tempo changes in the master, you will note that Reason will require up to
      one measure to adjust itself to the change. How long this actually takes also depends on the precision of the incom-
      ing MIDI Clock. The more precise it is, the faster Reason can adjust to it.
      If this adjustment is a problem, try to use gradual tempo changes rather than immediate ones.
      !   When Reason is synchronized to external MIDI Clock, there is no Tempo readout.
      !   Note that high-quality stretching of audio tracks is automatically disabled when syncing from external MIDI
          Clock.

      Input Focus and Play Focus
      If you activate (external) MIDI Clock sync on the Options|Sync menu, the Transport Panel controls will be disabled,
      and Reason will not run unless MIDI Sync data is provided from an external device.
      The Input Focus (MIDI + Audio) and Play Focus (MIDI Sync) buttons (located on the Reason Hardware Interface) re-
      late to how incoming MIDI and MIDI sync should be handled if there are several open Song documents. If you have
      two or more Songs opened, and no MIDI sync is used, the currently selected Song (the document “on top”) always
      has Input focus.
      If (external) MIDI Clock sync is enabled (which is global for all currently open Song documents), this functionality
      changes in the following way:
      • If both “Play Focus” and “Input Focus” are activated for a Song, incoming MIDI data, MIDI sync (and Audio)
        will be sent to this Song, regardless of whether another Song is currently in focus.
      • If only “Input Focus” is activated for Song, and another Song has “Play Focus”, incoming MIDI (and Audio) will
        be sent to the former and MIDI sync to the latter (i.e this Song will play back), regardless of which Song is cur-
        rently in focus.

      Synchronization using Ableton Link
      About Ableton Link
      Link by Ableton is a technology that keeps sequencing/playback devices and applications in sync over a wireless
      network. By connecting to the same network as other Ableton Link users you will be able to jam in perfect sync with
      other Ableton Link-enabled applications. Other users may be using apps on iOS devices or similar, but that’s perfectly
      fine, Link works across platforms!
      Any of the Ableton Link users can then start and stop their part while others keep playing. Any user in the network
      can also adjust the tempo in real-time and the rest of the “linked” applications/devices will follow.

      Synchronizing Reason’s sequencer with Ableton Link
      1. Connect your computer to the wireless network where the other Ableton Link devices/applications are con-
         nected.
          This is done where you configure your network in your computer OS.
      2. Select “Ableton Link” from the Sync Mode selector in the Transport panel - or from the Sync sub-menu in the
         Options menu.

          In the Sync Mode section a green progress bar constantly indicates the tempo and the current “position” (phase)
          within one single Bar.
          The number to the right of the progress bar shows how many other Link users you are connected to (4 in the ex-
          ample above).
      3. Hit Play in the sequencer.
          The Reason sequencer will start when the green progress bar reaches the current play head position (phase)
          within the current Bar. This means that the start of the sequencer will always be correct within the Bar and thus in
          perfect phase-sync with the rest of the Link devices/applications.
      D   If you change the Tempo in the sequencer, the tempo in all other Link applications will follow accordingly.
          Similarly, if the tempo is changed in any of the other Link applications in the network, Reason’s sequencer tempo
          will change. The tempo is constantly updated and displayed in real-time in the Tempo display on the Transport
          panel.
      D   If you switch back to Internal sync from Ableton Link sync, the Tempo in the Reason sequencer will remain at
          the tempo it had when you switched back.
          If your song has tempo automation, please have a look at “About Tempo Automation when using Ableton Link” for
          some additional information.
      !   Note that high-quality stretching of audio tracks is automatically disabled when using Ableton Link sync.

      About recording in the sequencer when using Ableton Link
      It’s also possible to record in the sequencer while synchronized to Ableton Link. A couple of important things, tough:
      !   We strongly recommend using “External Monitoring” when recording audio in Ableton Link sync mode.
          This is to enable the Recording Latency Compensation function, see “Recording Latency Compensation”.
      !   Pre-count in the sequencer is automatically disabled when synchronized with Ableton Link!

      About using different time signatures with Ableton Link
      Using a different time signature than the other devices/applications in the Ableton Link network works just fine. The
      sync progress bar on the Transport panel always shows the sync phase of one single Bar, regardless of selected time
      signature. Using different time signatures may of course generate interesting rhythmical results, though.

      About synchronizing external MIDI instruments while using Ableton Link
      It’s also possible to synchronize external MIDI instruments from Reason via MIDI Clock, while you are using Ableton
      Link. This is very useful if you, for example, are using external hardware MIDI instruments and want them to follow the
      Ableton Link synchronization tempo.
      1. Set up Reason to send MIDI Clock, as described in “Using Reason as MIDI Clock Host”.
      2. Select “Ableton Link” from the Sync Mode selector and then click the Send Clock button in the Transport
         panel:

      3. Hit Play in the Reason sequencer.
          The Reason sequencer will start when the green progress bar reaches the current play head position (phase)
          within the current Bar. As the sequencer starts, any external MIDI instruments will also be started and synced to
          Reason’s MIDI Clock signal. The MIDI Clock tempo will then automatically follow the Ableton Link tempo.

      About Tempo Automation when using Ableton Link
      If you use Ableton Link synchronization in a Reason song which has Tempo Automation, the Tempo Automation lane
      will be automatically muted in the sequencer:

      The song will then automatically follow the Ableton Link tempo instead and disregard any tempo automation.
      !   As long as Ableton Link synchronization is active it’s not possible to manually unmute the Tempo Automation
          lane!
      D   If you switch back to Internal sync from Ableton Link sync, the Tempo in the Reason sequencer will remain at
          the tempo it had when you switched back.
          The Tempo Automation lane is also automatically unmuted.
          The Automation Override indicator on the Transport panel is also lit:

      D   Click the Automation Override indicator - or press stop in the Reason sequencer - to set the tempo according
          to the Tempo Automation clip.

      Advanced MIDI - The External Control Bus inputs
      About the External Control Bus inputs
      The External Control Bus inputs allow you to receive MIDI from external equipment/applications directly to individual
      Reason devices.
      !   MIDI control keyboards/surfaces should NOT be set up using the External Control Bus! Instead, set them up on
          the MIDI tab, see “Preferences – MIDI”.
      • These MIDI inputs are for controlling Reason devices from an external sequencer.
          This could be an external hardware sequencer or a sequencer application running on another computer.
      !   Do NOT use the External Control Bus if you are only going to use Reason’s internal sequencer for recording
          and playback!
      You set up the External Control Bus inputs on the Sync tab in the Preferences dialog:

      D   Select a separate MIDI port for each bus you plan to use.
          Each bus provides 16 MIDI channels, for a total of up to 64 MIDI input channels. For example, if you have an ex-
          ternal sequencer with two MIDI outputs, you connect these to two MIDI inputs on your MIDI interface and select
          these two inputs for the first two busses on the Advanced MIDI page. You will then be able to send MIDI on up to
          32 channels from the external sequencer to Reason.
      D   Make sure you don’t select a MIDI port that is already selected on the Control surfaces tab (or in the MIDI
          Clock Sync section).
      q   To control external MIDI equipment from Reason, you can use the MIDI Out Device. Refer to “MIDI Out Device”
          for more details.

      Routing MIDI to devices
      Each External Control Bus can control up to 16 different Reason devices, one for each MIDI channel. To route a MIDI
      channel directly to a Reason device, proceed as follows:
      1. Locate the Reason Hardware Interface at the top of the rack and click the ADVANCED MIDI button.

          The Advanced MIDI Device panel is unfolded.
      2. On the Advanced MIDI Device panel, click the Bus Select button for the External Control Bus you want to use
         (A, B, C or D).

      3. Below the Bus Select buttons there are fields for the 16 MIDI channels. Click the arrow button for the desired
         MIDI channel and select a Reason device from the menu that appears.
          Incoming MIDI data on that bus and channel will now be sent directly to the selected device. In other words, the
          master keyboard routing in the sequencer is bypassed.

      Receiving Controller data via MIDI
      It is possible to send controller data from an external sequencer to control Reason parameters. Just set up your ex-
      ternal device to transmit the correct MIDI controller messages on the right MIDI port.
      To find out which MIDI Controller number corresponds to which control on each device, please see the “MIDI Imple-
      mentation Charts.pdf” document.
      Once you have located the controller numbers and set everything up, you can record and edit the controller data in
      the external sequencer as you normally do, and the Reason parameters will react correspondingly.
      q   Do not confuse this with Remote control. Remote does not require any mapping of controller numbers for sup-
          ported control surfaces! See “About Remote”.

      About recording Pattern Changes
      As specified in the MIDI Implementation, MIDI Controller #3 can be used to switch patterns in a device. However, pat-
      tern changes activated this way occur immediately (not at the end of the bar), which may or may not be what you pre-
      fer.
      Please, see “Recording pattern automation”, “Editing pattern automation” and “Drawing pattern automation” for infor-
      mation on recording and editing pattern changes.


---

<a id="optimizing-performance-25"></a>

=== END OF PART ===
