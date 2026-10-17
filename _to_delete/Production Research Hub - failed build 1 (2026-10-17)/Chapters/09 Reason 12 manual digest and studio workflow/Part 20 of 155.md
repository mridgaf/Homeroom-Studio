# Chapter 09: Reason 12 manual digest and studio workflow
## Part 20 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 11 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 21 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 11 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Sync Mode
      Here you can set the desired synchronization mode for the Reason sequencer: Internal, MIDI Clock (if applicable) or
      Ableton Link (if applicable). You can also choose “Send MIDI Clock” to sync other applications/instruments from
      Reason (if applicable). See the chapter “Synchronization and Advanced MIDI” for more information about synchroni-
      zation.

      Song Position
      The current song position is shown in the display. The song position is where the Song Position Pointer in the Ruler
      (see Ruler details) is at the moment. The display is divided into Bars, Beats, 1/16th Note and Ticks (there are 240
      Ticks for each 16th note) segments. You can edit the position of the Song Position Pointer, and thus change the
      song playback position, according to the descriptions in “Transport Panel segment displays”.

      About subticks in the Song Position display
      When editing notes and automation events in the sequencer you have a resolution of 240 ticks per 1/16th note,
      which allows for very accurate positioning. But for the Song Position Pointer, the internal resolution is even higher
      (15360 ppq) which means that the position can end up on a fraction of a tick, a so called subtick.
      If the Song Position Pointer value is on a fraction of a tick, this is displayed with an asterisk (*) in the Tick section of
      the Song Position display.

      D   To adjust the Song Position Pointer to the closest tick value, press [Ctrl](Win) or [Cmd](Mac) and click on the
          asterisk in the display.
          The Song Position Pointer will now adjust to the closest tick value and the asterisk disappears.

      Time Position
      The current position of the Song Position Pointer in the Ruler (see Ruler details) is shown in time format (hours, min-
      utes, seconds and milliseconds) in the display. You can change the position in time of the Song Position Pointer, and
      thus change the song playback time position, according to the descriptions in “Transport Panel segment displays”.

      Click On/Off
      D   Click this button to hear an audible metronome click as the sequencer plays.
          The click will sound on every beat, with the first beat in every bar accented (higher pitched). See “Click and Pre-
          count” for more details.

      Pre(-count) On/Off
      D   Click the Pre button to hear a pre-count (count-in) click sound before recording.
          Pre-count will only be present before recording - not before regular playback. See “Click and Pre-count” for details
          about selecting number of pre-count bars etc.

      Click Level
      D   Adjust the audio level of the metronome (and Pre-count) with this slider.
          See “Click and Pre-count” for more details.

      Tempo
      The current song tempo is shown in the display in BPM (Beats Per Minute) and 1/1000 of a BPM. You can edit the
      tempo according to the descriptions in “Transport Panel segment displays”. The Tempo range is 1.000-999.999
      BPM.

      Tap Tempo
      Instead of setting the Tempo with the Tempo control (see above), you can manually tap in the desired tempo in real-
      time.
      D   Click the Tap button repeatedly to set desired sequencer tempo.
          The tempo is defined by averaging the time between a minimum of two clicks and a maximum of 16 clicks. The
          more clicks, the more “steady” the tempo. The time-out between two series of clicks is 2 seconds. The detectable
          tap tempo range is 30-999.999 BPM.

      Signature
      The current song time signature is shown in the display. You can edit the time signature according to the descriptions
      in “Transport Panel segment displays”.
      The available Signatures are: 1/2-16/2, 1/4-16/4, 1/8-16/8 and 1/16-16/16.

      Rewind and Fast Forward
      D   Click on the Rewind or Fast Forward buttons to move the Song Position Pointer in steps of one bar (from its
          current position).
      D   To move the Song Position Pointer several bars at once, click and hold the mouse button depressed.
      Instead of clicking the buttons, you can use the computer keyboard:
      D   Press [4] on the numeric keypad for Rewind and [5] for Fast Forward.
      D   If you click and hold the Rewind or Fast Forward buttons, or press and hold the [4] or [5] keys, the positioning
          speed will be faster after the first 20 bars.

      Play and Stop
      D   Click the Play button to start playback from the Song Position Pointer’s current position.
      D   Alternatively, press [Enter] on the numeric keypad on the computer keyboard.
      D   Click the Stop button to stop playback (or recording).

      D   Alternatively, press [0] on the numeric keypad or [Shift]+[Return] on the computer keyboard.
      By default, if you click the Stop button or use the keyboard “Stop” commands when the song is already stopped, the
      Song Position Pointer is moved according to the following rules:
      • Clicking/pressing Stop the first time moves the Song Position Pointer to where playback was last started.
      • Clicking/pressing Stop a second time moves the Song Position Pointer to the beginning of the song.
      • If the Song Position Pointer already is at the beginning of the song, nothing happens.
          This means you can always click twice on the Stop button in “stop mode”, to return to the beginning of the song.
      D   Press [Spacebar] on the computer keyboard to toggle between Play and Stop.
      • To have the Song Position Pointer automatically return to its last start position when you hit Stop, select “Re-
        turn to last start position on stop” in the Miscellaneous section on the General tab in Preferences, see “Return
        to last start position on stop”.

      Record
      D   Click the Record button to begin recording on the selected track/lane in your song.
          Alternatively, press [*] on the numeric keypad or hold down [Ctrl](Win) or [Cmd](Mac) and press [Return] on the
          computer keyboard. If Pre-count has been activated (see Pre(-count) On/Off above), the recording will begin after
          the set number of pre-count bars.
      !   Nothing you play during the pre-count period will be recorded.

      Dub and Alt
      Clicking on any of these buttons will add additional audio tracks or note lanes for overdub purposes. Refer to “Over-
      dubbing audio using the “Dub” function” and “Recording notes using the “Dub” and “Alt” functions” for more details
      about these functions.

      Loop On/Off
      D   Click the Loop button or press [L] to activate the Loop function.
      When the loop function is activated, recording and playback will be continuously looped between the Left and Right
      Locators. Some general rules regarding loop mode are these:
      • If the Song Position Pointer is to the left of (before) the Right Locator when playback is started, the song will
        play to the Right Locator and then immediately jump back and seamlessly continue from the Left Locator.
      • If the Song Position Pointer is to the right of (after) the Right Locator when playback is started, the Locators
        will be ignored and the song will continue to play “un-looped”.
      • If the Left Locator is to the right of the Right Locator, i.e. in “reversed” order, the song will play to the Right Lo-
        cator and then immediately jump and seamlessly continue from the Left Locator, skipping the part of the song
        in-between the Locators. The song will then continue to play “un-looped”.

      Go to Left and Right Locators
      D   Click on the “L” or “R” button to move the Song Position Pointer to the Left or Right Locators respectively.
      D   Alternatively, press [1] on the numeric keypad on the computer keyboard to move the Song Position Pointer to
          the Left Locator or [2] to move to the Right Locator.

      Left and Right Locator Positions
      The current positions of the Left and Right Locators in the Ruler (see Ruler details) are shown in the displays. The
      display is divided into Bar, Beat, 1/16th Note and Ticks (there are 240 Ticks for each 1/16th Note). You can change
      the positions of the Locators, and thus change the loop playback region, according to the descriptions in “Transport
      Panel segment displays”.

      Transport keyboard commands and modifier keys
      Below is a complete list of the computer keyboard shortcuts for the Sequencer Transport functions:

      | Function                             | Key command
      Stop, Go to start position,             [0] on the numeric keypad or [Shift]+[Return]
      Go to start of song
      Play                                    [Enter] on the numeric keypad
      Toggle Stop/Play                        [Spacebar]
      Rewind                                  [4] on the numeric keypad
      Fast Forward                            [5] on the numeric keypad
      Record                                  [*] on the numeric keypad or
                                              [Ctrl](Win) or [Cmd](Mac)+[Return]
      Go to Left Locator                      [1] on the numeric keypad
      Go to Right Locator                     [2] on the numeric keypad
      Go to the start of the song             [.] on the numeric keypad
      Move forward one bar                    [8] on the numeric keypad
      Go back one bar                         [7] on the numeric keypad
      Tempo up                                [+] on the numeric keypad
      Tempo down                              [-] on the numeric keypad
      Loop On/Off                             [/] on the numeric keypad or [L]
      Click On/Off                            [C] or [9] on the numeric keypad
      Pre-count On/Off                        [Ctrl](Win) or [Cmd](Mac)+[P]
      Set the Left and Right Loop Locators to [Ctrl](Win) or [Cmd](Mac)+[L]
      encompass selected clips.
      Set the Left and Right Loop Locators to [P]
      encompass selected clips and start play-
      back in Loop Mode.
      Set Left Locator in ruler.              [Ctrl](Win)/[Option](Mac)+Click in the ruler
      Set Right Locator in ruler.             [Alt](Win)/[Cmd](Mac)+Click in the ruler
      Set End Marker in ruler.                [Shift]+Click in the ruler

      About the Inspector
                                                             Inspector (context sensitive)

      The Inspector, located above the Edit/Arrangement Pane, can be used for a number of different editing purposes
      pertaining to clips, events and recordings. The Inspector is context sensitive, meaning it will have different content
      and functionality depending on what is currently selected. How to edit using the Inspector is described in detail in the
      sections “Resizing clips using the Inspector”, “Moving clips using the Inspector”, “Editing recordings and cuts in the In-
      spector” and “Editing notes and events in the Inspector”.
      !   When the Pencil Tool is selected, the Inspector isn’t visible. Instead, menus pertaining to Time Signature, Pat-
          tern Automation and Blocks Automation are displayed.

      About subticks in the Position and Length displays
      When editing notes and automation events in the sequencer you have a resolution of 960 ppq (240 ticks per 1/16th
      note), which allows for very accurate positioning. But when you record, the internal resolution is even higher (15360
      ppq) which means that notes and automation events can end up on a fraction of a tick, a so called subtick.
      If the value is a fraction of a tick, this is displayed with an asterisk (*) in the Tick section of the Position or Length dis-
      play.

      D   To adjust the clip or event position (or length) to the closest tick value, press [Ctrl](Win) or [Cmd](Mac) and
          click on the asterisk in the display.
          The position or length value will now adjust to the closest tick value and the asterisk disappears.
      !   When it comes to audio editing, you will have access all the way down to the sub-tick level. This means there
          won’t be any sub-tick asterisks when editing audio.

      About the “Match Values” function

      The “Match Values” function in the Inspector can be used to match the positions, lengths and/or values of several se-
      lected clips, notes, events or recordings to the position, length and/or value of the topmost (or leftmost) selected clip,
      note, event or recording. Refer to “Matching clips using the “Match Values” function”, “Matching audio values using
      the "Match Values" function” and “Matching notes or events using the “Match Values” function”.

134   SEQUENCER FUNCTIONS


---

<a id="recording-in-the-sequencer-6"></a>

=== END OF PART ===
