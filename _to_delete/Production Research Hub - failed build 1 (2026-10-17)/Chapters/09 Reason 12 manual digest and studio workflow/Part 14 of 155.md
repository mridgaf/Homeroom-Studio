# Chapter 09: Reason 12 manual digest and studio workflow
## Part 14 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 5 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 15 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 5 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 4: Audio Basics

Audio Basics

     About this chapter
     This chapter contains some useful information about how audio is handled by Reason and how the audio is routed.
     Some of it may seem a bit technical, but we recommend that you read it to get the most out of Reason.

     How Reason communicates with your audio hardware
     Reason receives, generates and plays back digital audio - a stream of numerical values in the form of ones and ze-
     roes. For you to be able to record and play back anything, the audio must be converted from analog to digital when
     recording, and from digital to analog when playing back through some kind of listening equipment (a set of speakers,
     headphones, etc.).
     This conversion is most often handled by the audio card installed in your computer, or by an external audio interface
     connected via USB. To achieve the best possible performance, Reason requires that the audio card uses an ASIO
     driver on Windows systems. On macOS systems, Reason supports Core Audio.
     To receive and deliver digital audio to the computer’s audio hardware, Reason uses the driver you have selected in
     the Preferences dialog. In the Rack on screen, this connection is represented by the Hardware Interface (also known
     as the Hardware Device):

     The Hardware Interface is always located at the top of the rack.
     The Hardware Interface contains 64 input and 64 output “sockets”, each with an indicator and a level meter. There
     are also two Sampling Inputs that can be used for sampling audio to sampler devices. 16 input and 16 output sockets
     are shown on the main panel, and an additional 48+48 sockets are shown if the “More Audio” button is activated on
     the main panel. Each one of these indicators represents a connection to an input or output on your hardware audio
     interface.
     However, the number of available inputs and outputs depends on the number of inputs and outputs on your hardware
     audio interface. For example, if you are using a standard sound card with stereo inputs and outputs, only the first two
     inputs and outputs will be available. In the Hardware Interface, the indicators are lit green for all currently active and
     connected inputs and outputs. Activation of inputs and outputs on your hardware audio interface is done on the Au-
     dio page in the Preferences dialog (see “Active input and output channels”).
     Inputs and outputs that are currently connected have green indicators. Available but un-connected inputs and out-
     puts have yellow indicators and any connections made to unavailable inputs and outputs have red indicators.

     In this case, Inputs 1 and 2 are available, but not connected, Outputs 1 and 2 are available and
     connected, whereas Output 3 is unavailable, but connected on the back of the Hardware Interface.
     !   You never have to connect any cables to the Audio In jacks of the Hardware Interface to be able to record au-
         dio on sequencer tracks. This routing is made internally “in the background”, which means you just have to se-
         lect audio interface inputs from the Audio Input drop-down list - see “Selecting audio input(s) and defining
         mono or stereo”.

     Manual audio routing
     In most cases, you will want to have the Main Mixer Master Section device connected to outputs 1 and 2 of the Hard-
     ware Interface. This connection is made automatically as soon as you create a new Song document. However, there
     might be situations where you want to manually route audio to other outputs of the Hardware Interface. For example
     if you want to use the Control Room Outputs of the Main Mixer (see “Control Room output section”).
     To send the sound of a device in the Rack to a specific output, you route the device output to the corresponding Out-
     put jack on the Hardware Interface. This is done by using the patch cables on the back of the rack, as described in
     “Manual routing”. If we flip the rack around, by pressing the [Tab] key, the Hardware Interface looks like this:

     On the rear of the Hardware Interface, Inputs 1 and 2 are available but not connected,
     Outputs 1 and 2 are available and connected, whereas Output 3 is connected but unavailable.
     !   You never have to connect any cables to the Audio In jacks of the Hardware Interface to be able to record au-
         dio on sequencer tracks. This routing is made internally “in the background”, which means you just have to se-
         lect audio interface inputs from the Audio Input drop-down list in the sequencer Track List - see “Selecting
         audio input(s) and defining mono or stereo”.

     Audio quality
     The audio quality in a computer based recording system depends on two things:
     • The quality of the software calculating the audio.
         In our case, this is the Reason DSP (Digital Signal Processing) code.
     • The quality of the hardware audio interface used for recording and playing back the sound.

     Software
     • Reason uses 32-bit floating point arithmetic for all internal audio operations, with 64-bit summing in the mix
       bus in the Main Mixer Master Section.
         This ensures the highest possible audio quality throughout the entire signal chain.
     • Reason supports 16, 20, and 24 bit resolution for input and output audio.
     • Reason supports all standard sample rates between 44.1 kHz and 192 kHz.
         Reason also supports lower sampling frequencies, but using a sample rate of less than 44.1 kHz is not recom-
         mended since it might affect the audio quality negatively.
     • A number of digital audio techniques that reduce the risk of “aliasing”, background noise, unwanted distortion
       and “zipper noise” are implemented in Reason.

     Audio hardware
     How good a hardware audio interface actually sounds depends on a number of things; its frequency range and fre-
     quency response curve, the resolution (bit depth), the signal to noise ratio, the distortion under various circumstances,
     etc. Furthermore, some designs are more prone to disturbance from the other electronics in the computer than oth-
     ers. Such disturbance might add hum or high pitched noise to the signal.
     The only advice we can give is that if you are serious about sound, choose your audio hardware carefully!

     Audio settings
     Sample rate and resolution are properties of digital audio which determine the quality of the sound. Generally, higher
     sample rate and resolution result in better audio quality (but also larger audio files and higher demands on computer
     performance and audio hardware). The table below shows some common sample rate/resolution combinations:

     | Sample rate:            | Resolution:           | Comment:
         44.1 kHz               16 bit                  This is the format used on standard audio CDs.
         44.1 kHz –             24 bit                  These are formats used in professional studios and high-end recording
         192 kHz                                        equipment.

     To cater for all different situations, Reason supports multiple sample rates and resolutions.

     Sample Rate settings for recording and playback
     Reason handles all internal audio processing in 32-bit floating point resolution, with 64-bit summing in the mix bus in
     the Main Mixer Master Section. However, the resolution of the input and output audio is determined by the hardware
     audio interface. That is, if you have a 24-bit audio card, Reason will record and output audio in 24-bit resolution, and
     if you have a 20-bit audio card, audio will be recorded and played back in 20-bit resolution.
     The recording and playback sample rate can be specified on the Audio tab in the Preferences dialog (accessed from
     the Edit menu (Win) or Reason menu (Mac)):

     D     Select the desired sample rate from the drop-down menu.
           Note that the available options on this pop-up menu depend on which sample rates are supported by the audio
           hardware.
     !     Reason supports multiple sample rates in the same song!
           Reason allows import (or recording) of audio of any sample rate. If the original sample rate of a recording is differ-
           ent than the rate currently set for the audio card, Reason will automatically do a sample rate conversion.
           First, a real-time sample rate conversion algorithm is used (allowing the audio to be played back immediately).
           Meanwhile, in the background, the program calculates a sample rate conversion of the highest quality, which will
           be used as soon as it is calculated. The CALC progress indicator on the transport panel lights up whenever the
           program is doing high quality calculations in the background:

           The CALC progress indicator on the Transport Panel appears when Reason performs high quality audio calculations.

     Buffer Size settings
     The Buffer Size can be adjusted on the Audio tab in the Preferences dialog (accessed from the Edit menu (Win) or
     Reason menu (Mac)):

     D   Select Buffer Size by clicking and dragging the slider sideways.
     The trick here is to find the optimum relationship between audio quality, DSP Load and latency. Experiment with dif-
     ferent Sample Rate settings in combination with different Buffer Size settings to get the best result.
     A professional audio interface used together with a state-of-the-art computer should normally be able to handle a
     combination of a high sample rate (96 kHz) and a small Buffer Size (64-128 samples) without problems. A budget
     priced audio interface normally requires a lower sampling frequency (44.1 kHz) in combination with a little higher
     Buffer Size (256-512 samples).
     See “About latency” for more information about buffer size and latency. Also see “About audio rendering using the
     audio card buffer size setting” below for information on how to improve the DSP performance.

     About Max Audio Threads
     Reason fully supports multi-core audio rendering. This means that if your computer has multiple CPU Cores (Quad
     Core, for example), or multiple CPUs, Reason takes advantage of this to significantly enhance the performance. A
     higher system performance allows for more tracks and devices in your songs.
     Here you can select the maximum number of audio threads Reason should be allowed use. The “Default” setting
     equals the total number of physical cores in your computer’s CPU (corresponding to the old "Use multi-core audio
     rendering" option, but without the "Use hyper-threading audio rendering" option in older Reason versions). On Apple
     M1 the Max audio threads setting defaults to the number of high performance cores.
     This preference can also be used to limit the number of threads if you want to leave room for other apps or perhaps
     multi-core VSTs.

     See “Max audio threads” for more details.

     About audio rendering using the audio card buffer size setting

     The “Render audio using audio card buffer size setting” function should be selected (checked) for best plugin perfor-
     mance. When selected, the audio batches are rendered internally according to the set Buffer size (see “Buffer Size
     settings” above). For example, if you have a Buffer size of 512 Samples, each audio batch will be 512 samples inter-
     nally. Raising the Buffer size will let Reason process larger audio batches in one go, which is often more efficient.
     Many plugins are also more efficient when doing larger audio batches. if you are using DSP-heavy VSTs (mastering
     effects, for example), these will run a lot smoother with this function selected.
     !   Note that old songs might sound different with this function selected, if the songs use feedback routings and
         CV connections.

     If unchecked (off), all audio batches are rendered internally at a fixed size of 64 samples - regardless of the Buffer
     size setting. This might be desirable if you are using feedback signal routings and CV connections in your songs, and
     want the internal latency of those connections to be fixed at a short value all the time. This might result in perfor-
     mance problems for DSP-heavy VSTs, though.

     Master Tune setting
     By default, Reason plays back a “middle A” at 440 Hz, which is the standard tuning in most instruments. However, if
     you are playing Reason together with other instruments, you may want to adjust the tuning:
     1. Select “Preferences...” from the Edit menu (Win) or Reason menu (Mac).
     2. Click the “Audio” tab.
     3. Adjust the global tuning with the Master Tune slider or button controls.

     D   If you like, you can also adjust the Master Tune during playback.
     !   The Master Tune setting affects the tuning of all sound sources in Reason, including the Tuner function on the
         Audio Tracks. It also affects the tuning of the Redrum and Dr. Octo Rex loop player.
     !   Note that the Master Tune setting does NOT affect the pitch of the audio on audio tracks!
     !   Note that the Master Tune setting does NOT affect the pitch of any VST plugins used in the song!

     About audio levels
     When recording and playing back in Reason, you should keep an eye on the Audio In and Audio Out Clip indicators
     on the Transport Panel, or on the Hardware Interface and the Big Meter. You should also keep an eye on the clip in-
     dicators on the Main Mixer Master Section. If any of the clip indicators light up, the audio level is too high, resulting in
     clipping (digital distortion).

                              The Clip indicators will stay lit for a short
                              moment, to make them easier to spot.

     The Clip indicators on the Audio In and Audio Out meters on the Transport Panel.

                          Reset button

                                           Audio Out Clip indicators

                                           If the audio out level is, or has been, too
                                           high, the Clip indicators in the Master
                                           Section will stay lit until you click the
                                           “Reset” button.

     The Clip indicators in the Master Section of the Main Mixer.
     !   Note that if you use the Propellerhead Balance audio interface when recording audio tracks in Reason, you can
         use the unique Clip Safe function. The Clip Safe function allows you to heal clipped input signals! See
         “Recording using the Clip Safe function in Propellerhead Balance” for more information.
     !   Note that the Main Mixer Master Section Clip indicators will only work if there are no other devices connected
         between the Master Section device and the Hardware Interface!

                The “Show Big Meter” button                                               Channel Selection buttons
                                                                                          for the “Big Meter”

                                                                                                                      Reset
                                                                                                                      button
                                 Channel Selection knob
                                 for the “Big Meter”                                     Clip indicators
         The Big Meter on the Hardware Interface.

     D   To remedy Audio In clipping, adjust the level at the input source, i.e. on the hardware audio interface or on the
         preamp connected to the hardware audio interface.
     !   When recording or sampling external audio signals, clipping cannot be adjusted in the Reason application - it
         must be adjusted at the audio input source!
     !   When sampling audio internally from devices in the rack, you have to adjust the Output Level on the source de-
         vice to make sure clipping doesn’t occur in the Hardware Interface.
     D   To remedy Audio Out clipping, lower the master level on the Mixer (or other device) that is connected to the
         Hardware Interface, until Audio Out clipping doesn’t light up on playback.
         You could also use the MClass Maximizer as an insert effect on the Master Section in the Main Mixer to ensure
         that clipping never occurs - see “The MClass Maximizer”.
     D   To get a better overview of the levels, bring up the Big Meter on the Hardware Interface, by clicking the “Big
         Meter” button on the front panel. Then, select the input or output pairs to view in the Big Meter by clicking on
         the corresponding channel selection button below each input or output pairs. Alternatively, select channel by
         turning the channel selection knob.
         If the audio level is, or has been, too high, the Clip indicators on the Big Meter will stay lit until you click the Reset
         button, or select new audio channels for the Big Meter.
     !   In some situations, the Audio Out Clip indicator on the Transport Panel and the Output Clip indicators on the
         Reason Hardware Interface might light up if the metronome Click is active in the sequencer during playback
         (see “Click and Pre-count”). This is nothing to worry about and won’t cause any distortion in your song. To de-
         termine if the metronome is causing the clipping indication, just disable Click and see if the clipping stops.
     !   Note that it doesn’t matter if the level meters on the individual devices (effects, MIxer channels, etc.) “hit the
         red”. Output clipping can only occur in the Hardware Interface.
         The technical reason for this is that internally, Reason uses high resolution floating point processing, which en-
         sures highest audio quality and virtually limitless headroom. In the Hardware Interface, the floating point audio is
         converted to the resolution used by the computer’s audio interface, and that’s where audio out clipping might oc-
         cur.

     If you are using multiple outputs
     If you are using an audio interface with more than two outputs, you might want to have different devices connected
     to different outputs. If the Audio Out Clip indicator on the Transport Panel lights up, you should play back the section
     again while checking the Reason Hardware Interface. Each output socket has a level meter - if the red meter seg-
     ment lights up, the output is clipping.

                                                                                         Output 7 indicates
                                                                                         audio clipping.

     The indicator for Output 7 on the Hardware Interface indicates clipping.
     D   If necessary, bring up the Big Meter and select the output pair where the clipping occurs. Lower the output
         level of the device connected to the clipping output, until no clipping occurs.

     System signal paths
     Depending on the track types in the sequencer, the default signal chain varies. In this section we’re going to describe
     the default audio signal paths for Audio Tracks and Instrument Tracks.

     Audio Track signal paths
     When you’re recording and playing back audio that originates from an external source, like a guitar or a vocalist, the
     audio signal must first travel from the source, via a hardware audio interface, into the Reason application. Then, when
     played back, the audio travels from the Reason application, via the hardware audio interface, to a speaker system or
     similar. The figure below shows a schematic overview of the audio signal paths for a “standard” auto-routed Audio
     Track in Reason:

                                                                                                                                                                                                                                                                            Main Mixer
                                                                                                                                                                                                                                                                                                INV
                                                                                                                                                                                                                                                                                            PHASE
                                                                                                                                                                                                                                                                             GAIN
                                                                                                                                                                                                                                                                                                DYN
                                                                                                                                                                                                                                                                                                  N
                                                                                                                                                                                                                                                                                                S/C

                                                                                                                                                                                                                                                                             LPF

                                                                                                                                                                                                                                                                                                K hz
                                                                                                                                                                                                                                                                                                HPF
                                                                                                                                                                                                                                                                             K hz

                                                                                                                                                                                                                                                                            HF
                                                                                                                                                                                                                                                                                                BELL

                                                                                                                                                                                                                                                                                 dB
                                                                                                                                                                                                                                                                            HMF
                                                                                                                                                                                                                                                                                                K hz

                                                                                                                                                                                                                                                                                 dB
                                                                                                                                                                                                                                                                                                K hz

                                                                                                                                                                                                                                                                                 Q               ON

                                                                                                                                                                                                                                                                            LMF                   E

                         Audio Interface                                                                                                                                                                                                                                         dB
                                                                                                                                                                      F I R E W Y R E 1 6 x 1 6 AUDIO INTERFACE                                                                                 K hz
                          A UD I O IN                                                 A U D IO O UT
                                                                                                                                               1   2    3   4     5   6       7     8        9 10 11 12 13 14 15 16                                                              Q
                                                  -L-                                                        -L-                                                                                                                                                            LF
                                                                                                                                                                                                                                                                                                K hz
                                                  -R-                                                        -R-                                                                                                                       POWER
                                                                                                                                                                                                                                                                                                BELL
                                                                                                                                                                                                                                                                                 dB

                                                                                                                                                                                                                                                                            INSERT                      INSERT

                                                                                                                                                                                                                                                                                                  EQ
                                                                                                                                                                                                                                                                             BYP                                                                ROUTING
                                                                                                                                                                                                                                                                                                  DYN           BY
                                                                                                                                                                                                                                                                                                               PASS                                             DYN

                                                                                                                                                                                                                                                                            Init Patch                   Init Patch
                                                                                                                                                                                                                                                                                  Rotary 1
                                                                                                                                                                                                                                                                                                             Rotary 1
                                                                                                                                                                                                                                                                                                                                                             Button 1

                         Rack                                                                                                                                                                                                                                                     Button 1
                                                                                                                                                                                                                                                                                  Rotary 2
                                                                                                                                                                                                                                                                                                             Rotary 2
                                                                                                                                                                                                                                                                                                                                                             Button 2

                                                                                                                                                                                                                                                                                  Button 2
                                                                                                   AUDIO INPUT                                                   AUDIO OUTPUT
                                                         FIREWYRE 16x16 Audio Interf
                                                                                                  1 2   3 4   5    6   7   8   9 10 11 12 13 14 15 16           1 2   3 4  5 6                7     8         9 10 11 12 13 14 15 16                                              Rotary 3
                                                              ADV. MIDI DEVICE        IN USE                                                                                                                                                                                                                 Rotary 3
                                                                                                                                                                                                                                                                                                                                                             Button 3
                                                              MORE AUDIO I/O         IN USE
                                  REWIRE                                                                                                                                                                                                                                          Button 3
                                  AUDIO CARD                  SHOW BIG METR                                                                                                                                                                                                       Rotary 4
                                                                                                                                                                                                                                                                                                             Rotary 4
                                                                                                                                                                                                                                                                                                                                                             Button 4
                                                                                                                                                                                                                                                                                  Button 4

                                                                                                                                                                                                                                                                             EDIT INSERTS                                             EDIT INSERTS

           Input signal from Hardware Device                                                                                                                                                                                                                                DYNAMICS
                                                                                                                                                                                                                                                                            COMP/LIM
                                                                                                                                                                                                                                                                                                        DYNAMICS

                                                                                                                                                                                                                                                                                                ON
                                                                                                                                                                                                                                                                                            PEAK
                                                                                                                                                                                                                                                                            RATIO                            ON

                                                                                                                                                                                                                                                                                            THRES
                                                                                                                                                                                                                                                                             REL
                                                                                                                                                                                                                                                                                            GE CL
                                                                                                                                                                                                                                                                            FAST
                                                                                                                                                                                                                                                                               T

                              AUDIO TRA...                    Stretch Type        MUTE     SOLO     IInit
                                                                                                       i Patch
                                                                                                          P h                                                                                                                                  Audio Track device control    KEY
                                                                                                                                                                                                                                                                            GATE/
                                                                                                                                                                                                                                                                            EXP
                                                                                                                                                                                                                                                                                                                                                          EXTERNAL
                                                                                                                                                                                                                                                                                                                                                          SIDECHAIN

                                      Show Programmer                        External Routing       Frippe FW ASIO Interfaze Analog In 1                                      -56       VU    -20       -10      0    4     8 10
                                                                                                                                                                                                                                                                                                ON                                                     KEY
                                                                                                                                                                                                                                                                                                EXP
                                      Show Insert FX                         Bypass Insert FX                                                                                                                         Rec Source                                            RANGE
                                                                                                                                                                                                                                                                                                               THRESHOLD               RATIO

                                                                                                                                                                                                                                                                                            THRES
                                                                                                                                                                                                                                                                                 REL                              AT TACK             RELEASE        MAKE-UP
                                                                                                                                                                                                                                                                             FAST
                                                                                                                                                                                                                                                                                T
                                                                                                                                                                                                                                                                                            HOLD
                                                                                                                                                                                                                                                                            FX SEND                     FX SEND                                  FX RETURN

                   Playback signal via Audio Track device                                                                                                                                                                                                                    1        PRE
                                                                                                                                                                                                                                                                                                            LEVEL

                                                                                                                                                                                                                                                                                                                      1
                                                                                                                                                                                                                                                                                                                                                       LEVEL

                                                                                                                                                                                                                                                                                                                                                                MUTE
                                                                                                                                                                                                                                                                                                                                                                        PAN

                                                                                                                                                                                                                                                                             2        PRE
                                                                                                                                                                                                                                                                                                                      2                                         MUTE

                                                                                                                                                                                                                                                                             3        PRE
                                                                                                                                                                                                                                                                                                                      3                                         MUTE

                    Monitor signal via Audio Track device                                                                                                                                                                                                                    4        PRE
                                                                                                                                                                                                                                                                                                                      4                                         MUTE


=== END OF PART ===
