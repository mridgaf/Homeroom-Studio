# Chapter 09: Reason 12 manual digest and studio workflow
## Part 16 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 7 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 17 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 7 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 5: Sequencer Functions

Sequencer Functions

     About this chapter
     This chapter describes the layout and general functions of the main sequencer. Recording, editing clips and events,
     arranging and working with Blocks in the sequencer are described in detail in the chapters “Recording in the Se-
     quencer”, “Audio Editing in the Sequencer”, “Note and Automation Editing”, “Arranging in the Sequencer” and “Work-
     ing with Blocks in the Sequencer”.

     Introduction
     The sequencer is where you record your songs. The sequencer can be used to record audio tracks as well as instru-
     ment tracks, performance controllers, parameter automation and pattern automation. You can also arrange your
     songs, or parts of your songs, in Blocks. In Blocks mode you can build complete “sections” - consisting of a desired
     number of bars and tracks - that can be reused throughout the song. This chapter mainly describes the Song View
     and Edit Mode. Functions specific to Blocks and the Blocks View are described in the separate chapter “Working
     with Blocks in the Sequencer”.

     Sequencer area overview
                             Toolbar            Edit Mode button(s)                   Inspector (context sensitive)
     Track
     List

                                                                    Ruler
                                              Blocks Track
                                                                                        Audio Clips

                                                                                       Edit/Arrangement pane

                                                                                       Note Clips

                 Lanes                                                                  Automation Clips

                                                                                       Song Navigator

        Tracks                                                           Transport Panel

     Song View and Edit Mode
     The Song View is the “normal view” where you are working with your song arrangement. This mode gives a good
     overview of the contents of the tracks in your song. If the Enable Blocks function on the Options menu is active, the
     Blocks track is also visible at the top in the Track List. If the Enable Blocks function is off, there is no Blocks track in
     the Track List.
     On the Blocks track you arrange the Block automation clips that control which Block should play back (see “Working
     with Blocks in the Sequencer”).
     Edit Mode is where you edit the contents of the clips in your song.
     D   Click (any of) the Edit button(s) in the Toolbar to enter Edit Mode. Alternatively, hold down [Ctrl](Win) or
         [Cmd](Mac) and press [E].
         In Edit Mode the Edit Pane shows detailed information about the content of one track (see “Tracks overview”), or
         lane (see “Lanes overview”) at a time and you can edit the events in individual clips (see “Clips overview”).
     • Instrument Tracks only have a single Edit Mode, whereas Audio Tracks have three different Edit Modes de-
       pending on what and how you want to edit.
     q   When you open a note or Comp audio clip by double-clicking it in Song View (or Block View), the sequencer
         automatically switches to Edit Mode. However, if you double-click a Single Take audio clip or parameter auto-
         mation clip, it may open up for editing inline, directly in the Song View or Block View.

     Song View

     In the Song View, all clips on all tracks can be viewed. Use this mode to get an overview of your arrangement, and
     when you want to perform clip-based editing such as rearranging whole sections of your song, etc.
     !   Note that if the Enable Blocks function on the Options menu is off, there is no Blocks track in the Track List.

     Edit Mode

     In Edit Mode, you get a close-up look at the recordings on a track. In Edit Mode, the Edit Pane can be divided into
     several horizontal edit rows, showing different types of events (notes, velocity, audio, parameter automation, etc.). This
     is the view mode of choice for fine editing the content of your recorded clips, and for drawing notes, performance
     controllers and other events manually.

     Toolbar overview

     The sequencer Toolbar features various sequencer editing tools as well as the Snap function. The tools can be used
     in both Edit Mode and the Song/Block Views, with slightly different purposes in the respective modes. See “Toolbar
     details” for details about each tool.

     Track List overview

     To the left in the sequencer, all tracks are listed in the Track List. Each track in the sequencer is associated with a
     specific device in the rack. By clicking on a device icon in the Track List you automatically set Master Keyboard Input
     (see “Setting Master Keyboard Input”) to the corresponding device in the rack for playing and/or recording.

     Tracks overview

     Tracks

     Most rack devices in a song automatically get their own dedicated track in the sequencer when you create the device.
     Each track can feature one or several lanes on which audio, note, performance controller, pattern and parameter au-
     tomation events can be recorded - in clips. See “Track details” for more details about tracks.
     !   If the Blocks button on the Transport Panel is on, the Blocks Track is also shown at the top in the Track List.

     Lanes overview

                                                Lanes

     Each track consists of one (default) or several parallel lanes. The lanes can contain clips that feature note events or
     audio recordings, depending on track type. A track can also feature automation lanes that contain clips with parame-
     ter automation events - or pattern automation for pattern based devices. See “Lane details” for more details about
     lanes.

     Clips overview
                                             (Single Take) Audio Clips

                                                  Note Clips

                                            Automation Clips

     Note, audio, performance controller, pattern and parameter automation events are always contained in clips. A clip is
     basically a “container” for recorded data. Audio clips are displayed in the Edit/Arrange Pane as a rectangular box with
     one or two graphical audio waves inside (mono or stereo). Note events are displayed in a “piano roll” fashion in the
     clip. Performance controllers and parameter automation events are displayed as continuous lines, and pattern events
     are displayed as repeated rectangles in the clips. See “Clip basics” for information about the different clip types.

     Inspector overview

     The context sensitive Inspector shows the properties of whatever is currently selected in the sequencer: clips, notes,
     automation events, audio comp rows and cuts etc. The properties of the selected item can be edited by changing the
     values in the various displays. See “About the Inspector” for more info.

     Ruler overview

     The Ruler is the song’s “time line”, measured in bars. In the Ruler, the Song Position Pointer indicates the current po-
     sition in the song, i.e. in which bar the song is, or will begin, playing. The Ruler also shows the Left and Right Loop Lo-
     cators as well as the Song End Marker. See “Ruler details” for more details.

     Edit/Arrangement Pane overview

     The big center section of the sequencer is called the Edit/Arrangement Pane. This is where all recorded events re-
     side in clips - on one or more lanes on the respective track.

     Track scrollbar overview

     To the far right in the sequencer is the Track scrollbar. With the Track scrollbar you can scroll vertically on the Edit/
     Arrange Pane. See “Scrolling” and “Zooming in the Sequencer” for more details.

     Song Navigator overview

     Below the Edit/Arrangement Pane is the Song Navigator. With the Song Navigator you can scroll and zoom horizon-
     tally on the Edit/Arrangement Pane. The Song Navigator also features indicators for the Ruler’s Loop Locators, Song
     Position Pointer and Song End Marker. In the Song Navigator, all clips on all lanes are displayed as colored lines, in-
     dicating their positions in the song. See “Scrolling” and “Zooming in the Sequencer” for more details.

     Transport Panel overview

     The Transport Panel features the sequencer transport controls (Rewind, Fast Forward, Stop, Play and Record) as well
     as controls for Tempo, Time Signature, Position, Time and Loop Locator placements and some other functions. See
     “Transport Panel details” for more details.

     Track details
     Track definition
     The tracks in the sequencer are where you record your audio, note and automation to create your songs. A track is al-
     ways associated with a device in the rack (except for the Transport track and Blocks track). An icon with a picture of
     the associated device is shown in the Track List on the left hand side in the sequencer. In the Track List, the name of
     the associated device is shown, as well as icons and buttons related to the specific track. Each track can incorporate
     various lane types (depending on track type). To the right of the Track List - on the Edit/Arrangement pane - each
     track has its own dedicated area for recorded events.
     In the picture below, six sequencer tracks are shown. From the top down are the Transport Track (which is always
     present and cannot be moved or deleted), two audio tracks, two instrument tracks associated with one ID8 instru-
     ment device each, and one automation track for a Mix Channel strip.

                                                                                            Transport Track
                                                                                            Audio Tracks

                                                                                            Instrument Tracks

                                                                                            Automation Track

     The relationship between the track, the rack and the Main Mixer
     A track in the sequencer is always associated with a device in the rack; i.e. there can never be a sequencer track with-
     out an associated rack device (except for the Transport track and Blocks track). Audio Track devices and Mix Chan-
     nel devices in the rack also have their corresponding channel strips in the Main Mixer. Mixer channel strips can be
     considered “remote controls” for their corresponding rack devices. Depending on track type, the signal chain differs
     somewhat. The picture below shows the signal flow in five scenarios with three different track types:
                                                                                 HF                                                                                                                                                                                                                                                                                                                           HF
                                                                                                     BELL

                                                                                      dB                                                                                                                                                                                                                                                                                                                            dB
                                                                                 HMF                                                                                                                                                                                                                                                                                                                           HMF
                                                                                                     K hz                                                                                                                                                                                                                                                                                                                           Khz

                                                                                      dB                                                                                                                                                                                                                                                                                                                            dB
                                                                                                     K hz                                                                                                                                                                                                                                                                                                                           Khz

                                                                                      Q               ON                                                                                                                                                                                                                                                                                                            Q
                                                                                 LMF                   E                                                                                                                                                                                                                                                                                                       LMF                     E

                                                                                      dB                                                                                                                                                                                                                                                                                                                            dB
                                                                                                     K hz                                                                                                                                                                                                                                                                                                                           Khz

                                                                                      Q                                                                                                                                                                                                                                                                                                                             Q
                                                                                 LF                                                                                                                                                                                                                                                                                                                            LF
                                                                                                     K hz                                                                                                                                                                                                                                                                                                                           Khz
                                                                                                     BELL
                                                                                      dB                                                                                                                                                                                                                                                                                                                            dB

                                                                                  INSERT                                                                                   INSERT                                                                                                                                                                                                                              INSERT                                                                 INSERT

                                                                                                       EQ                                                                                                                                                                                                                                                                                                                              EQ
                                                                                   BYP                                                                                                                                 ROUTING                                                                                                                                                                                  BYP                                                                                                     ROUTING
                                                                                                       DYN                                                                          BY                                                                                                                                                                                                                                                 DYN                                                    BY
                                                                                                                                                                                   PASS                                              DYN                                                                                                                                                                                                                                                     PASS                                     DYN

                                                                                  Init Patch                                                                                   Init Patch                                                                                                                                                                                                                      Init Patch                                                                 Init Patch
                                                                                       Rotary 1                                                                                                                                                                                                                                                                                                                      Rotary 1
                                                                                                                                                                                   Rotary 1                                                                                                                                                                                                                                                                                                  Rotary 1
                                                                                                                                                                                                                                  Button 1                                                                                                                                                                                                                                                                                         Button 1
                                                                                       Button 1                                                                                                                                                                                                                                                                                                                      Button 1
                                                                                       Rotary 2                                                                                                                                                                                                                                                                                                                      Rotary 2
                                                                                                                                                                                   Rotary 2                                                                                                                                                                                                                                                                                                  Rotary 2
                                                                                                                                                                                                                                  Button 2                                                                                                                                                                                                                                                                                         Button 2

                                                                                       Button 2                                                                                                                                                                                                                                                                                                                      Button 2
                                                                                       Rotary 3                                                                                                                                                                                                                                                                                                                      Rotary 3
                                                                                                                                                                                   Rotary 3                                                                                                                                                                                                                                                                                                  Rotary 3
                                                                                                                                                                                                                                  Button 3                                                                                                                                                                                                                                                                                         Button 3

                                                                                       Button 3                                                                                                                                                                                                                                                                                                                      Button 3
                                                                                       Rotary 4                                                                                                                                                                                                                                                                                                                      Rotary 4
                                                                                                                                                                                   Rotary 4                                                                                                                                                                                                                                                                                                  Rotary 4
                                                                                                                                                                                                                                  Button 4                                                                                                                                                                                                                                                                                         Button 4
                                                                                       Button 4                                                                                                                                                                                                                                                                                                                      Button 4

                                                                                   EDIT INSERTS                                                                                                           EDIT INSERTS                                                                                                                                                                                          EDIT INSERTS                                                                                EDIT INSERTS

                                                                                  DYNAMICS                                                                                 DYNAMICS                                                                                                                                                                                                                            DYNAMICS                                                               DYNAMICS
                                                                                  COMP/LIM                                                                                                                                                                                                                                                                                                                     COMP/LIM
                                                                                                     ON
                                                                                                  PEAK
                                                                                                     K
                                                                                  RATIO                                                                                            ON                                                                                                                                                                                                                                                                                                        ON

                                                                                                  THRES                                                                                                                                                                                                                                                                                                                         THRES
                                                                                   REL                                                                                                                                                                                                                                                                                                                           REL
                                                                                                 GE CL                                                                                                                                                                                                                                                                                                                          GE CL
                                                                                  FAST
                                                                                     T
                                                                                   KEY                                                                                                                                           EXTERNAL                                                                                                                                                                                                                                                                                          EXTERNAL
                                                                                                                                                                                                                                 SIDECHAIN                                                                                                                                                                                                                                                                                         SIDECHAIN
                                                                                 GATE/                                                                                                                                                                                                                                                                                                                         GATE/
                                                                                 EXP                                                                                                                                                                                                                                                                                                                           EXP
                                                                                                     ON
                                                                                                     EXP
                                                                                                                                                                                   THRESHOLD               RATIO                                                                                                                                                                                                                                                                             THRESHOLD       RATIO
                                                                                  RANGE

                                                                                                  THRES                                                                                                                                                                                                                                                                                                                          THRES
                                                                                      REL                                                                                               AT TACK                                                                                                                                                                                                                                                                                                   AT TACK
                                                                                                                                                                                                          RELEASE         MAKE-UP                                                                                                                                                                                                                                                                           RELEASE        MAKE-UP
                                                                                  FAST
                                                                                                  HOLD                                                                                                                                                                                                                                                                                                                          HOLD
                                                                                  FX SEND                                                                                  FX SEND                                      FX RETURN                                                                                                                                                                              FX SEND                                                                FX SEND                             FX RETURN
                                                                                                                                                                                                                                                PAN                                                                                                                                                                                                                                         LEVEL                                              PAN
                                                                                  1        PRE                                                                                                                                                                                                                                                                                                                  1        PRE
                                                                                                                                                                                          1                                              MUTE                                                                                                                                                                                                                                                        1                                 MUTE

                                                                                  2        PRE                                                                                                                                                                                                                                                                                                                  2        PRE
                                                                                                                                                                                          2                                              MUTE                                                                                                                                                                                                                                                        2                                 MUTE

                                                                                  3        PRE                                                                                                                                                                                                                                                                                                                  3        PRE
                                                                                                                                                                                          3                                              MUTE                                                                                                                                                                                                                                                        3                                 MUTE

                                                                                  4        PRE                                                                                            4                                              MUTE                                                                                                                                                                   4        PRE                                                                         4                                 MUTE

                                                                                                 5     PRE                                                                                5                                              MUTE                                                                                                                                                                                   5      PRE                                                           5                                 MUTE

                                                                                                 6     PRE                                                                                6                                              MUTE                                                                                                                                                                                   6      PRE                                                           6                                 MUTE

                                                                                                 7     PRE                                                                                7                                              MUTE                                                                                                                                                                                   7      PRE                                                           7                                 MUTE

                                                                                                 8     PRE                                                                                8                                              MUTE                                                                                                                                                                                   8      PRE                                                           8                                 MUTE

                                                                                  FADER                                                                                                                                                                                                                                                                                                                        FADER
                                                                                                                                                                                                                                         CONTROL                                                                                                                                                                                                                                                                                       CONTROL
                                                                                                                                                                                 SOLO                                                     ROOM                                                                                                                                                                                                                                             SOLO                                         ROOM
                                                                                                                                                                                ALL OFF                                                    OUT                                                                                                                                                                                                                                            ALL OFF                                        OUT
                                                                                                  L R
                                                                                                                                                                                                                                                7
                                                                                                                                                                                                                                                                                                                                                                                                                                 L R

                                                                                   MUTE              SOLO
                                                                                                                                                                                 MUTE
                                                                                                                                                                                                                                                                                                                                                                                                                MUTE                SOLO
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           MUTE
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                7
                                                                                                                                                                                ALL OFF                                                  MASTER                                                                                                                                                                                                                                           ALL OFF                                      MASTER
                                                                                                                                                                                                                                         FX SEND                                                                                                                                                                                                                                                                                       FX SEND
                                                                                                                                                                                                                                         FX RE T                                                                                                                                                                                                                                                                                       FX RE T
                                                                                                                                                                                                                                            SOURCE                                                                                                                                                                                                                                                                                          SOURCE
                                                                                                                                                                                 DIM                                                                                                                                                                                                                                                                                                        DIM
                                                                                                                                                                                -20dB                                                                                                                                                                                                                                                                                                      -20dB

                                                                                                                                                                                                                                           LEVEL                                                                                                                                                                                                                                                                                           LEVEL

                        Control                                                                                                                                                                                                                                                                                                                                        Control
                                                                                                                                                                                                                       Control                                                                                                                                                                                                                                                                                           Control
                                   MASTER SECTION                                                                                                                                                                                                                                                                                                                              MASTER SECTION                                                My Master Patch
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    -56     VU      -2
                                                                                                                  My Master Patch
                                                                                                                                                                         -56     VU                                                                                                                                                                                                                             DIM -20dB
                                                                                      DIM -20dB                                                                                                                                                                                                                                                                                TTM SERIES SUPERDIGITAL                                                                          L
                                   TTM SERIES SUPERDIGITAL                                                                                                           L

                                                                                                                                                                     R                                                                                                                                                                                                                                                                                                          R
                                          External Routing                                                                                                                                                                                                                                                                                                                            External Routing                                                                              -56     VU      -22
                                                                                                                                                                         -56     VU
                                          Bypass Insert FX                                                                                                                                                                                                                                                                                                                            Bypass Insert FX                                                                               MODE           VU
                                                                                                                                                                          MODE           VU         PPM         PEAK             RESET

                                          Show Programmer                                                                                                                                                                                                                                                                                                                             Show Programmer
                                          Show Insert FX                                                                                                                                                       Rec Source                                                                                                                                                             Show Insert FX                                                                                                                 Rec Source

                                                                                                                                                                                                                                                      Audio                                                                                                                                                                                                                                                                                                               Audio
                                   AUDIO TR...                 Stretch Type        MUTE              SOLO         IInit
                                                                                                                     i Patch
                                                                                                                     it P t h                                                                                                                                                                                                                                                  MIX CHAN...                      MUTE             SOLO        I it
                                                                                                                                                                                                                                                                                                                                                                                                                                             Init
                                                                                                                                                                                                                                                                                                                                                                                                                                               i Patch

                                          Show Programmer                     External Routing                    Frippe FW ASIO Interfaze Analog In 1                   -56      VU      -20     -10      0       4      8 10 12                                                                                                                                                     Show Programmer      External Routing
                                          Show Insert FX                      Bypass Insert FX                                                                                                                     Rec Source                                                                                                                                                         Show Insert FX       Bypass Insert FX

                                                                                                                                                                                                                                                                                                                                       Audio
                                                                Audio                                                                                                                                                                                                                                                                                                                                    Piano
                                                                                                                                                                                                                                                                                                                                                                                                                                                     Grand
                                                                                                                                                                                                                                                                                                                                                                                                                                                    Upright
                                                                                                                                                                                                                                                                                                                                                                                                                                                     Dance
                                                                                                                                                                                                                                                                                                                                                                                                                                                               A
                                                                                                                                                                                                                                                                                                                                                                                                                                                               B
                                                                                                                                                                                                                                                                                                                                                                                                                                                               C
                                                                                                                                                                                                                                                                                                                                                                                                                                                                       Delay
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ID8 2

                                                                                                                                                                                                                                                                                                                                                                                                                                                      Vibes    D       Chorus                                instrument device
                                                                                                                                                                                                                                                                                                                                                                                  PITCH        MOD                                                                                               VOLUME

                                                                                                                                                                                                                                                                                                                                                                                                         MIDI
                                                                                                 Disk Channel 1

                                                                                                                    M S
                                                                                                                                                                                                                                                                                                                                                                               MIDI                                            ID8 1

                                                                                                                                                                                                                                                                                                                                                                                                                                              M S                  M

                         Audio

                                                        Audio Track                                                                                                                                                                                                                                                                  Instrument Track (for internal instrument)

                                                                                                                                                                                                                                                                                                                                 EQ
                                                                                                                                                                                                                                                                                                               BYP
                                                                                                                                                                                                                                                                                                                                 DYN

                                                                                                                                                                                                                                                                                                               Init Patch
                                                                                                                                                                                                                                                                                                                    Rotary 1

                                                                                                                                                                                                                                                                                                                    Button 1
                                                                                                                                                                                                                                                                                                                    Rotary 2

                                                                                                                                                                                                                                                                                                                    Button 2
                                                                                                                                                                                                                                                                                                                    Rotary 3

                                                                                                                                                                                                                                                                                                                    Button 3
                                                                                                                                                                                                                                                                                                                    Rotary 4

                                                                                                                                                                                                                                                                                                                    Button 4

                                                                                                                                                                                                                                                                                                               EDIT INSERTS
                                                                                                                                                                                                                                                                                                              DYNAMICS
                                                                                                                                                                                                                                                                                                              COMP/LIM
                                                                                                                                                                                                                                                                                                                               ON
                                                                                                                                                                                                                                                                                                                           PEAK
                                                                                                                                                                                                                                                                                                                              K
                                                                                                                                                                                                                                                                                                               RATIO


=== END OF PART ===
