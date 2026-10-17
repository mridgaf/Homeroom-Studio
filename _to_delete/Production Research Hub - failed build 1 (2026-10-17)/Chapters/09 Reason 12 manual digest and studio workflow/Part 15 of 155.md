# Chapter 09: Reason 12 manual digest and studio workflow
## Part 15 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 6 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 16 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 6 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

                                                                                                                                                                                                                                                                                            5     PRE                 5                                         MUTE

                                                                                                                                                                                                                                                                                            6     PRE                 6                                         MUTE

                                                                                                                                                                                                                                                                                            7     PRE                 7                                         MUTE

                                                                                                                                                                                                                                                                                            8     PRE                 8                                         MUTE

                               MASTER SECTION                                                       My Master Patch
                                                                                                                                                                                                                                               Master Section control
                                                                                                                                                                              -56       VU    -20       -10      0    4     8 10 12
                                                                                   DIM -20dB                                                                                                                                                                                FADER
                               TTM SERIES SUPERDIGITAL                                                                                                                    L
                                                                                                                                                                                                                                                                                                                                                                CONTROL
                                                                                                                                                                          R
                                                                                                                                                                                                                                                                                                                                                                 ROOM
                                      External Routing                                                                                                                        -56       VU    -20       -10      0    4     8 10 12
                                                                                                                                                                                                                                                                                                           SOLO
                                                                                                                                                                                                                                                                                                          ALL OFF                                                 OUT
                                      Bypass Insert FX                                                                                                                                                                                                                                       L R
                                                                                                                                                                               MODE           VU          PPM        PEAK          RESET
                                                                                                                                                                                                                                                                             MUTE               SOLO
                                                                                                                                                                                                                                                                                                           MUTE
                                                                                                                                                                                                                                                                                                                                                                         7
                                                                                                                                                                                                                                                                                                                                       12
                                      Show Programmer                                                                                                                                                                                                                                                     ALL OFF                                                MASTER
                                                                                                                                                                                                                                                                                                                                                                 FX SEND
                                      Show Insert FX                                                                                                                                                                 Rec Source                                                      12
                                                                                                                                                                                                                                                                                                                                       8
                                                                                                                                                                                                                                                                                                                                                                 FX RE T
                                                                                                                                                                                                                                                                                     8
                                                                                                                                                                                                                                                                                                                                       4                              SOURCE
                                                                                                                                                                                                                                                                                                            DIM
                                                                                                                                                                                                                                                                                     4                     -20dB             0         0

                                                                                                                                                                                                                                                                                     0
                                                                                                                                                                                                                                                                                                                             -         -
                                                                                                                                                                                                                                                                                                                                                                   LEVEL
                                                                                                                                                                                                                                                                                     -
                                                                                                                                                                                                                                                                                                                            20         20

                                                                                                                                                                                                                                                                                     20
                                                                                                                                                                                                                                                                                                                             -         -

                                                                                                                                                                                                                                                                                     -                                      56         -56
                                                                                                                                                                                                                                                                                                                                 VU
                                                                                                                                                                                                                                                                                     56                                          VU

                Playback signal from Audio Track in sequencer                                                                                                                                                                                                               SEQ

                                                                                                                                                                                                                                                                            DISK CHA...
                                                                                                                                                                                                                                                                                            RACK         SEQ       RACK

             Monitor signal                                             Sequencer
                            Audio Track 1

                                            M S

          Input signal

       Output signal from Master Section device

     An Audio Track signal path in Reason.

     Instrument Track signal paths
     When you’re recording and playing back audio from an instrument device, like the ID8 Instrument device, the audio
     signal only has to travel only in one direction: from the Instrument device, via the hardware audio interface, to a
     speaker system or similar. The figure below shows a schematic overview of the audio signal paths for an auto-routed
     Instrument Track in Reason:
                                                                                                                                                                                                                                                                         Main Mixer
                                                                                                                                                                                                                                                                                             INV
                                                                                                                                                                                                                                                                                         PHASE
                                                                                                                                                                                                                                                                          GAIN
                                                                                                                                                                                                                                                                                             DYN
                                                                                                                                                                                                                                                                                             S/C

                                                                                                                                                                                                                                                                          LPF

                                                                                                                                                                                                                                                                                             K hz

           MIDI Out from Master Keyboard                                                                                                                                                                                                                                  K hz
                                                                                                                                                                                                                                                                                             HPF

                                                                                                                                                                                                                                                                         HF
                                                                                                                                                                                                                                                                                             BELL

                                                                                                                                                                                                                                                                              dB
                                                                                                                                                                                                                                                                         HMF
                                                                                                                                                                                                                                                                                             K hz

                                                                                                                                                                                                                                                                              dB
                                                                                                                                                                                                                                                                                             K hz

                                                                                                                                                                                                                                                                              Q               ON

                                                                                                                                                                                                                                                                         LMF                   E

                         Audio Interface                                                                                                                                                                                                                                      dB
                                                                                                                                                                     F I R E W Y R E 1 6 x 1 6 AUDIO INTERFACE                                                                               K hz
                           A UD I O IN                                             A U D IO O UT
                                                                                                                                              1   2    3   4     5   6       7     8        9 10 11 12 13 14 15 16                                                            Q
                                                   -L-                                                     -L-                                                                                                                                                           LF
                                                                                                                                                                                                                                                                                             K hz
                                                   -R-                                                     -R-                                                                                                                          POWER
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

                        Rack                                                                                                                                                                                                                                                   Button 1
                                                                                                                                                                                                                                                                               Rotary 2
                                                                                                                                                                                                                                                                                                          Rotary 2
                                                                                                                                                                                                                                                                                                                                                          Button 2
                                                                                                                                                                                                                                                                               Button 2
                                                                                                AUDIO INPUT                                                     AUDIO OUTPUT
                                                         FIREWYRE 16x16 Audio Interf                                                                                                                                                                                           Rotary 3
                                                                                               1 2   3 4   5      6   7   8   9 10 11 12 13 14 15 16           1 2   3 4  5 6                7      8         9 10 11 12 13 14 15 16
                                                              ADV. MIDI DEVICE     IN USE                                                                                                                                                                                                                 Rotary 3
                                                                                                                                                                                                                                                                                                                                                          Button 3
                                                              MORE AUDIO I/O       IN USE
                                     REWIRE                                                                                                                                                                                                                                    Button 3
                                     AUDIO CARD               SHOW BIG METR                                                                                                                                                                                                    Rotary 4
                                                                                                                                                                                                                                                                                                          Rotary 4
                                                                                                                                                                                                                                                                                                                                                          Button 4
                                                                                                                                                                                                                                                                               Button 4

                                                                                                                                                                                                                                                                          EDIT INSERTS                                             EDIT INSERTS
                                                                                                                                                                                                                                                                         DYNAMICS                    DYNAMICS
                                                                                                                                                                                                                                                                         COMP/LIM
                                                                                                                                                                                                                                                                                             ON
                                                                                                                                                                                                                                                                                         PEAK
                                                                                                            Grand             A               Delay
                                                                                                                                                                                                                           ID8 1                                                                          ON

                                                                   Piano
                                                                                                                                                                                                                                                                         RATIO
                                                                                                          Upright             B
                                                                                                           Dance              C
                                                                                                                                                                                                                                                                                         THRES
                                                                                                           Vibes              D               Chorus                                                             instrument device                                        REL
                                     PITCH      MOD                                                                                                                                     VOLUME                                                                                           GE CL
                                                                                                                                                                                                                                                                         FAST
                                                                                                                                                                                                                                                                            T
                                                                                                                                                                                                                                                                          KEY                                                                          EXTERNAL

                                                            ID8 audio output signal
                                                                                                                                                                                                                                                                                                                                                       SIDECHAIN
                                                                                                                                                                                                                                                                         GATE/
                                                                                                                                                                                                                                                                         EXP
                                                                                                                                                                                                                                                                                             ON                                                     KEY
                                                                                                                                                                                                                                                                                             EXP
                                                                                                                                                                                                                                                                                                            THRESHOLD               RATIO
                                                                                                                                                                                                                                                                         RANGE

                               MIX CHAN...                                       MUTE   SOLO      IInit
                                                                                                     iit PPatch
                                                                                                            t h                                                          L
                                                                                                                                                                             -56       VU     -20       -10       0    4      8 10 12
                                                                                                                                                                                                                                                Mix Channel control           REL
                                                                                                                                                                                                                                                                                         THRES
                                                                                                                                                                                                                                                                                                               AT TACK             RELEASE        MAKE-UP
                                                                                                                                                                         R                                                                                                FAST
                                        Show Programmer                   External Routing                                                                                   -56       VU     -20       -10       0    4      8 10 12                                                    HOLD

                                        Show Insert FX                                                                                                                                                                                                                   FX SEND                     FX SEND                                  FX RETURN
                                                                          Bypass Insert FX                                                                                                                              Rec Source
                                                                                                                                                                                                                                                                                                         LEVEL                                      LEVEL            PAN
                                                                                                                                                                                                                                                                          1        PRE
                                                                                                                                                                                                                                                                                                                   1                                         MUTE

                                                                                                                                                                                                                                                                          2        PRE
                                                                                                                                                                                                                                                                                                                   2                                         MUTE

                                                                                                                                                                                                                                                                          3        PRE
                                                                                                                                                                                                                                                                                                                   3                                         MUTE

                                                                                                                                                                                                                                                                          4        PRE
                                                                                                                                                                                                                                                                                                                   4                                         MUTE

                                                                                                                                                                                                                                                                                         5     PRE
                                                                                                                                                                                                                                                                                                                                                             MUTE
                                                                                                                                                                                                                                                                                                                   5

                     ID8 audio output signal via Mix Channel device                                                                                                                                                                                                                      6     PRE                 6                                         MUTE

                                                                                                                                                                                                                                                                                         7     PRE                 7                                         MUTE

                                                                                                                                                                                                                                                                                         8     PRE                 8                                         MUTE

                               MASTER SECTION                                                    My Master Patch
                                                                                                                                                                                                                 0     4      8 10 12
                               TTM SERIES SUPERDIGITAL

                                        External Routing
                                                                                 DIM -20dB
                                                                                                                                                                                                                                                Master Section control   FADER

                                                                                                                                                                                                                                                                                                        SOLO
                                                                                                                                                                                                                                                                                                                                                             CONTROL
                                                                                                                                                                                                                                                                                                                                                              ROOM
                                                                                                                                                                                                                 0     4      8 10 12                                                                                                                          OUT
                                                                                                                                                                                                                                                                                                       ALL OFF
                                                                                                                                                                                                                                                                                          L R
                                        Bypass Insert FX                                                                                                                     MODE            VU           PPM         PEAK         RESET
                                                                                                                                                                                                                                                                          MUTE               SOLO
                                                                                                                                                                                                                                                                                                        MUTE
                                                                                                                                                                                                                                                                                                                                                                      7
                                                                                                                                                                                                                                                                                                                         12
                                        Show Programmer                                                                                                                                                                                                                                                ALL OFF                                                MASTER
                                                                                                                                                                                                                                                                                  12                                                                          FX SEND
                                        Show Insert FX                                                                                                                                                                Rec Source                                                                                          8
                                                                                                                                                                                                                                                                                                                                                              FX RE T
                                                                                                                                                                                                                                                                                  8
                                                                                                                                                                                                                                                                                                                          4                                        SOURCE
                                                                                                                                                                                                                                                                                                         DIM
                                                                                                                                                                                                                                                                                                        -20dB             0         0

                                                                                                                                                                                                                                                                                                                          -         -
                                                                                                                                                                                                                                                                                                                                                                LEVEL
                                                                                                                                                                                                                                                                                                                         20         20

                                                                                                                                                                                                                                                                                                                          -         -
                                                                                                                                                                                                                                                                                                                         56         -56
                                                                                                                                                                                                                                                                                                                              VU
                                                                                                                                                                                                                                                                                                                              VU

                Live and playback MIDI data from Instrument Track in sequencer                                                                                                                                                                                           SEQ

                                                                                                                                                                                                                                                                         MIX CHAN...
                                                                                                                                                                                                                                                                                         RACK         SEQ       RACK

                                                                     Sequencer
           MIDI In           ID8 1

                                             M S                                   M

       Output signal from Master Section device

     An Instrument Track signal path in Reason.

     General information about audio and computers
     About latency
     On any personal computer system, there is a delay between the moment you input a sound, or “tell” the hardware to
     play a sound, and when you actually hear it. This delay is referred to as the “latency” of the design. This imposes a
     problem for any system where you want real-time user input to affect the sound.

     Why is there latency?
     All audio applications receive and generate their audio in chunks. These chunks are then passed on to the audio card
     where they are temporarily stored before being converted into regular audio signals. The storage place for these
     chunks are called “buffers” (an analogy would be a bucket brigade, where a number of people each have a bucket,
     and water is poured from one bucket to another to reach its final destination).
     The smaller the buffers and the fewer they are, the more responsive the system will be (lower latency). The general
     rules regarding the buffer size are these:
     • A small buffer size reduces the latency (the time it takes for the audio to “travel” from the audio interface in-
       put(s) to the application and from the application to the audio interface output(s)).
         However, a small buffer size also increases the DSP Load. Too small a buffer size setting could also make the
         sound crackle and distort.
     • A large buffer size reduces the DSP Load (allowing for more tracks to be played back simultaneously) and also
       ensures good audio quality.
         However, a large buffer size also increases the latency.
     A high sample rate will also reduce the latency. However, this will also raise the demands on the computer and its
     software. If the system can’t cope with moving the data to and from the buffers fast enough, there will be problems
     that manifest themselves as glitches in audio playback.
     To make things worse, audio playback is always competing with other activities on your computer. For example, a
     buffer size that works perfectly under normal circumstances might be too small when you try to open files during
     playback, switch over to another program while Reason is playing or simply play back a very demanding song.

     What is acceptable?
     On a regular PC, the latency can vary quite a lot. This is an effect of the fact that computers and their operating sys-
     tems were created for many purposes, not just for recording and playing back audio. For multimedia and games, a la-
     tency of a 100 ms might be perfectly acceptable, but for recording and playing back audio it is definitely not!
     • PC audio cards running under Windows with a MME driver might at best give you a latency of around 160ms.
     • The same card with a DirectX driver running under Windows provides at best around 40ms.
     • A card specifically designed for low latency, with an ASIO driver under Windows, or a Core Audio driver under
       macOS, can usually give you figures as low as 2-3 ms. This is definitely good enough for audio applications.
       That’s also why ASIO or Core Audio drivers are required to run Reason.

     Reducing latency
     There are a few general methods for making sure latency is as low as possible:
     D   Make sure you are using the latest version of the drivers for your hardware audio interface.
     D   Adjust the Sample Rate and Buffer Size parameters as described in “Audio settings”.
     D   Remove unnecessary background tasks on your computer.
         This might be any background utility you have installed as well as networking, background Internet activities etc.

     D   Optimize your songs.
         You might run into situations where you have to raise the Output Latency setting to be able to play back a very de-
         manding song on your computer. Another option would be to actually optimize the song. See “Optimizing Perfor-
         mance” for details.
     D   Get a better audio interface.
         This is only required if you find that you need to increase Output Latency because your audio card can’t really cope
         with the songs you try to play.
     D   Get a faster computer.
         This is only required if you find that you need to increase Output Latency because your computer can’t really cope
         with the songs you try to play.

     About processors
     When you run Reason, the numbers of physical CPU cores and the CPU clock speed are major factors determining
     how many audio tracks and devices you can use at the same time.
     If you plan to buy a computer specifically for Reason, you could play it safe and choose a computer with at least a
     quad-core Intel i7 processor, or equivalent AMD processor, running at 2.0 GHz or faster. MultiCore processors will
     give better performance and are highly recommended.

     About RAM
     Another important performance factor is the amount of installed RAM in the computer. Generally, one could say: the
     more the better, especially if you’re running several applications simultaneously. To run Reason, a minimum of 4 GB
     RAM is required, but more is highly recommended for better performance.


---

<a id="sequencer-functions-5"></a>

=== END OF PART ===
