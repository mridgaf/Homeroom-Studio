# Chapter 09: Reason 12 manual digest and studio workflow
## Part 10 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 1 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 11 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 1 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Reason 12.7 Operation Manual — Full Text (searchable)

This is the complete text of the real Reason 12.7 Operation Manual PDF you provided (1,466 pages, Reason Studios, ©2023), extracted and cleaned up into one searchable, chapter-organized document. Page headers/footers were stripped; wording, order, and all parameter descriptions are otherwise as published. Illustrations, screenshots, and knob-position diagrams from the original PDF are not reproduced here (text only) — keep the PDF itself on hand for those.

This supersedes the earlier partial version I compiled from Reason Studios' web manual, which was missing most parameter tables because that site renders them as interactive graphics rather than text. Everything that was missing there is here now, pulled straight from your PDF.

---

## Table of Contents

1. [Introduction](#introduction-1)
2. [Common Operations and Concepts](#common-operations-and-concepts-2)
3. [On-screen Piano Keys](#on-screen-piano-keys-3)
4. [Audio Basics](#audio-basics-4)
5. [Sequencer Functions](#sequencer-functions-5)
6. [Recording in the Sequencer](#recording-in-the-sequencer-6)
7. [Arranging in the Sequencer](#arranging-in-the-sequencer-7)
8. [Audio Editing in the Sequencer](#audio-editing-in-the-sequencer-8)
9. [Note and Automation Editing](#note-and-automation-editing-9)
10. [Working with Blocks in the Sequencer](#working-with-blocks-in-the-sequencer-10)
11. [Working with the Rack](#working-with-the-rack-11)
12. [Working with Players](#working-with-players-12)
13. [Working with Rack Extensions](#working-with-rack-extensions-13)
14. [Working with VST Plugins](#working-with-vst-plugins-14)
15. [Sounds, Patches and the Browser](#sounds-patches-and-the-browser-15)
16. [Routing Audio and CV](#routing-audio-and-cv-16)
17. [The Main Mixer](#the-main-mixer-17)
18. [Delay Compensation](#delay-compensation-18)
19. [Song File Handling](#song-file-handling-19)
20. [Importing and Exporting Audio](#importing-and-exporting-audio-20)
21. [Sampling](#sampling-21)
22. [The ReGroove Mixer](#the-regroove-mixer-22)
23. [Remote - Playing and Controlling Devices](#remote-playing-and-controlling-devices-23)
24. [Synchronization and Advanced MIDI](#synchronization-and-advanced-midi-24)
25. [Optimizing Performance](#optimizing-performance-25)
26. [Hardware Interface](#hardware-interface-26)
27. [Kong Drum Designer](#kong-drum-designer-27)
28. [Redrum Drum Computer](#redrum-drum-computer-28)
29. [Dr. Octo Rex Loop Player](#dr-octo-rex-loop-player-29)
30. [Europa Shapeshifting Synthesizer](#europa-shapeshifting-synthesizer-30)
31. [Grain Sample Manipulator](#grain-sample-manipulator-31)
32. [Mimic Creative Sampler](#mimic-creative-sampler-32)
33. [Thor Polysonic Synthesizer](#thor-polysonic-synthesizer-33)
34. [Subtractor Synthesizer](#subtractor-synthesizer-34)
35. [Malström Synthesizer](#malstr-m-synthesizer-35)
36. [Monotone Bass Synthesizer](#monotone-bass-synthesizer-36)
37. [ID8 Instrument Device](#id8-instrument-device-37)
38. [Rytmik Drum Machine](#rytmik-drum-machine-38)
39. [Radical Piano](#radical-piano-39)
40. [Klang Tuned Percussion](#klang-tuned-percussion-40)
41. [Pangea World Instruments](#pangea-world-instruments-41)
42. [Humana Vocal Ensemble](#humana-vocal-ensemble-42)
43. [NN-XT Sampler](#nn-xt-sampler-43)
44. [NN-19 Sampler](#nn-19-sampler-44)
45. [MIDI Out Device](#midi-out-device-45)
46. [Quartet Chorus Ensemble](#quartet-chorus-ensemble-46)
47. [Sweeper Modulation Effect](#sweeper-modulation-effect-47)
48. [Alligator Triple Filtered Gate](#alligator-triple-filtered-gate-48)
49. [Pulveriser](#pulveriser-49)
50. [The Echo](#the-echo-50)
51. [Scream 4 Sound Destruction Unit](#scream-4-sound-destruction-unit-51)
52. [BV512 Vocoder](#bv512-vocoder-52)
53. [RV7000 Mk II Advanced Reverb](#rv7000-mk-ii-advanced-reverb-53)
54. [Neptune Pitch Adjuster and Voice Synth](#neptune-pitch-adjuster-and-voice-synth-54)
55. [Softube Amps](#softube-amps-55)
56. [Audiomatic Retro Transformer](#audiomatic-retro-transformer-56)
57. [Channel Dynamics Compressor & Gate](#channel-dynamics-compressor-gate-57)
58. [Channel EQ Equalizer](#channel-eq-equalizer-58)
59. [Master Bus Compressor](#master-bus-compressor-59)
60. [Synchronous Timed Effect Modulator](#synchronous-timed-effect-modulator-60)
61. [The MClass Effects](#the-mclass-effects-61)
62. [Half-Rack Effects](#half-rack-effects-62)
63. [The Combinator](#the-combinator-63)
64. [Pulsar Dual LFO](#pulsar-dual-lfo-64)
65. [RPG-8 Arpeggiator](#rpg-8-arpeggiator-65)
66. [Matrix Pattern Sequencer](#matrix-pattern-sequencer-66)
67. [Mixer 14:2](#mixer-14-2-67)
68. [The Line Mixer 6:2](#the-line-mixer-6-2-68)
69. [Menu and Dialog Reference](#menu-and-dialog-reference-69)
70. [Key Commands](#key-commands-70)

---

<a id="introduction-1"></a>
# Chapter 1: Introduction

Introduction

     Welcome!
     This is the Operation Manual for Reason Version 12 music production software from Reason Studios. The informa-
     tion in this manual is also available as html files from the Reason Help menu. The separate Operation Manual for
     Reason Rack Plugin can be downloaded here.
     Don’t forget to check out the Video Tutorials web site, which can be accessed from the Reason Help menu.
     Also, be sure to regularly check out www.reasonstudios.com for the latest news!

     About this chapter
     The Introduction chapter describes some of the general conventions used throughout the Reason Operation Manual.
     It also contains instructions on how to utilize the Reason authorization system.

     About this manual
     In this Operation Manual, all aspects of the Reason program are described in detail. The first chapters deal with gen-
     eral methods and techniques, e.g. how to connect audio sources, mix and record. Then follow descriptions of all rack
     devices in Reason.
     !   The information in this document is subject to change without notice and does not represent a commitment on
         the part of Reason Studios AB.

     About the Reason operating system versions
     Reason comes in two platform versions: one for Windows 10/11 (64-bit) and one for macOS 10.13 (High Sierra)
     (64-bit) or later. The screenshots in this manual were taken from both platform versions of Reason, and some
     screenshots remain from older versions of Reason. Since the program layout is more or less identical in these ver-
     sions, there shouldn’t be any problem following the instructions.

     Conventions in the manual
     This manual describes both the Windows and macOS versions of Reason; wherever the versions differ this is clearly
     stated in the text.

     Text conventions
     The text conventions are pretty straightforward. The examples below describe when certain text styles are used:
     D   This style instructs the user to perform the task(s) described in the sentence.
     !   This text style means IMPORTANT INFORMATION. Read carefully to avoid problems!
     q   This text style is used for tips and additional info.

     Key command conventions
     In the manual, computer keyboard commands are indicated with brackets. For example:
     D   Hold down [Shift] and press [C].
     However, some modifier keys are different on Windows and Mac computers. Whenever this is the case, the manual
     separates the commands with “(Win)” and “(Mac)” indications as in the following example:
     D   Hold down [Ctrl](Win) or [Cmd](Mac) and press [S] to save your song.

     References to context menus
     Whenever the manual instructs you to select an item from the “context menu”, it means that you should right-click (or
     [Ctrl]-click if you’re using a Mac with single-button mouse) on the specific area, section or device, and then select the
     item from the pop-up menu that appears - the context menu. The item list in context menus varies depending on
     where in the application you click. See “Context menus” for an overview of the context menus in Reason.

     Frames and circles (call-outs)

                                                     Rack

                                        Sequencer

     In pictures throughout this manual there might be circles and/or rectangles highlighting certain areas or objects.
     These are indicated by filled lines according to the examples in the picture above. Sometimes these highlighting
     frames/circles might also be accompanied by descriptive texts. The different colors of the frames and texts are only
     to enhance the contrast to the background pictures.

     Dashed arrows

     A dashed arrow in a picture indicates the directions in which the pointer (or other tool) should be dragged to perform
     the desired operation. The example in the picture above shows in which directions (up and down) to drag the pointer
     to change the knob’s setting.

     About the Authorization system
     Reason uses an authorization system designed to be as flexible as possible, while at the same time providing the best
     possible copy protection for the product.
     • The core of the authorization system is your Reason Studios account (and license number, if you are using a
       perpetual version of Reason 12).

     Registering Reason (perpetual version only)
     To be able to run your perpetual (licensed) version of Reason, the program must be registered to your account on the
     Reason Studios web site.
     D   If you purchased a Reason license in a music store, follow the instructions you received from the shop.
     !   If you purchased Reason directly from the Reason Studios Shop web site, the Reason license has already been
         automatically registered to your user account and you can use Reason by running it on a computer connected
         to the Internet.

     Authorizing Reason
     !   Note that Internet connection is initially required for the procedures described below.

     D   Launch Reason and enter you Username/e-mail address and Password for your Reason Studios account and
         click the Log in button.
         Reason launches in Authorized Mode.

     • The first time you log in to the "Welcome to Reason" login dialog, the program will automatically store your
       user credentials.
         The next time you launch Reason it will start without showing the login dialog. This also automatically enables off-
         line use, allowing Reason to run even if you have no Internet connection. Reason will then run off-line for a month.
         This period is continuously renewed when you run Reason (perpetual or Annual Reason+ subscription) with an In-
         ternet connection. You do not have to do anything manually, except connecting to the Internet once a month.

     Logging out from Reason
     Logging out means removing the stored login credentials - do this if you’re not going to use Reason on that com-
     puter, or if you need to log in to another Reason Studios user account.
     D   In Reason, select “Quit/Exit and Log out” from the Reason (Mac) or File (Windows) menu.
         The next time you run Reason, you will need to enter your Username/e-mail and password in the "Welcome to
         Reason" dialog again. Internet connection is then required again.

     Authorizing a computer for long-term off-line use
     In addition, if you have an Annual (yearly) Reason+ subscription or own a perpetual (licensed) version of Reason 12,
     you can authorize your computer for long-term off-line use. This can be useful if you are traveling or working in a stu-
     dio without Internet access, etc. The long-term authorization allows for staying off-line on the authorized computer for
     one (1) year. If you are a Reason+ subscriber you are limited by the subscription end date, though. In most situations,
     authorizing a computer for long-term use is not necessary, though.

     Authorizing Reason for long-term off-line use
     1. Open Reason’s Preferences and click the Account tab.
     2. Click the “Add long-term authorization” button:

     • The authorization expiry date for your computer is now shown in the Offline Authorization section.
     • You can authorize up to three (3) computers for long-term off-line use.

     Removing a long-term authorization for a computer
     If you've already long-term authorized three computers and would like to authorize another computer, you will need to
     remove the authorization for one of the computers first:
     1. Launch Reason on one of the computers that already has a long-term authorization.
     2. Open Reason’s Preferences and click the Account tab.
     3. Click the “Remove long-term authorization” button:

     • If you can no longer access any of your authorized computers, you need to contact support to have them re-
       move the authorization(s). This can be done here.

     What happens if an authorization expires?
     • If a Reason authorization should expire during a session, the program will automatically enter Demo Mode,
       see “Running Reason in Demo Mode”.
       You can continue to work, and save your songs as usual.
     • When you reconnect to the Internet and log in, Reason will automatically revert to authorized mode (provided
       that you have a valid Reason license or Reason+ subscription).

     Running Reason in Demo Mode
     If you don't have a Reason license, a Reason+ subscription, or if you don’t have an authorized computer and don’t
     have a working Internet connection, you can run Reason in Demo Mode:
     1. Launch Reason.
       The following window appears:

     2. Click "Run in Demo Mode".
       Reason launches in Demo Mode.
       The Demo Mode LED lights up to the right on the Transport Panel:

     Running Reason in Demo Mode allows you to perform all operations as in authorized mode, with three exceptions:
     • You cannot export audio or bounce mixer channels to disk.
     • You will only have access to the built-in devices in Reason, not to any Rack Extensions installed by the Reason
       Companion app.
     • You cannot open songs.
       The only songs that can be opened in Demo Mode are the dedicated demo songs (file extensions ".rsndemo"
       (Reason Demo Song). See “Opening a Reason Demo Song”.

     Managing additional content
     Reason comes with some additional content (Rack Extensions and ReFills) that you can download separately,
     either right after the Reason installation or at a later point. To download additional content, proceed as follows:
     !   Note that this procedure requires Internet connection!
     1. Select “Manage Content” from the Windows menu.
         This brings up the Manage Content window:

     2. Select the item(s) you wish to install.
         It’s possible to select multiple items in the list.
     3. Click the “Install” button to download and install the selected item(s).
     D   Alternatively, skip step 2 and 3 and click the “Install all” button to download and install all items in the list in
         one go.
         Progress bars show the download of the item(s):

     4. After download, restart Reason for the downloaded and installed items to become available.
     All additional content is stored in sub-folders in the Music > Propellerhead Content folder on your computer. Rack
     Extension devices are stored in the Optional Devices sub-folder and ReFills are stored in the Optional Refills sub-
     folder.

     Reassigning the Function Keys in macOS
     When you work with Reason, you will do a lot of navigating between the three main areas - the main mixer, the rack
     and the sequencer. The quickest way to switch between these areas is to use the function keys F5, F6 and F7 (see
     “Navigating between the areas” for details). Also, the F2, F3, F4 and F8 keys are shortcuts for showing and hiding the
     Spectrum EQ window, Browser, On-screen Piano Keys window and the Tool Window, respectively.
     However, on many Macintosh models (especially MacBooks), the function keys double as hardware control buttons.
     For example, they might control the volume of the built-in speaker, the display brightness or keyboard backlight. To
     make these keys actually work as function keys for software such as Reason, you need to hold the "Fn" key while
     pressing them.
     This can work perfectly OK, but to get the best workflow in Reason we recommend that you change this behavior, so
     that pressing e.g. the F5 key actually sends "F5" to Reason (and you hold down the Fn key to get the hardware con-
     trol functions instead). Here is how you change this:
     1. Open the System Preferences in macOS and select the "Keyboard" item.

     2. Click the “Keyboard Shortcuts...” button:

     3. Select the "Function Keys" tab and make sure "Use F1, F2, etc. keys as standard function keys" is switched on.
       Now you can use F2-F8 for controlling functions in Reason. To use hardware control features such as volume and
       display brightness, you need to hold down the "Fn" key before pressing the function keys.

     Some function keys might also be pre-assigned to macOS keyboard shortcuts, which will have priority over software
     such as Reason. This is easily changed:
     4. Select the “Accessibility” tab.
       The Accessibility window shows lists of keyboard shortcuts assigned to system functions. For example, [Cmd]-[F5]
       is assigned to turn VoiceOver on or off. In Reason, this is the keyboard shortcut for detaching the main mixer into
       a separate window.
     5. Either remove the tick from the checkbox or assign it to another keyboard shortcut.

     6. Now you’re finished with the settings and can exit System Preferences.
       From now on, the function keys and keyboard shortcuts will perform their intended functions in Reason.

     About automatic program updates
     Reason supports automatic program updates (within each major release). When you launch Reason it automatically
     checks for new updates on the Reason Studios web site - provided your computer is connected to the Internet.
     If you are working with Reason off-line, and then connect to the Internet, you can manually check for updates by se-
     lecting the “Check for Updates...” item on the Reason (Mac) or Help (Win) menu.
     !   Note that the automatic program update function only works within each major Reason release version, i.e.
         there will be no automatic update between Reason 11.x and 12.x.
     Each time a new Reason version is available, an “update bar” appears at the top of the Reason song document after
     launch. In the update bar you can choose to either download the update now or later. You can also check the release
     notes for the update by clicking More Info:

     If you click “Not Now” Reason will wait a number of days before it checks for updates again.
     If you click “Download” the update is downloaded and prepared for installation. A download progress bar appears in
     the update bar:

     D   If you want to abort the download, click “Cancel”.
     D   If you want to hide the download progress bar, click “Hide”.
     When the download is ready, two options are available:

     D   Click “Restart and Install Now” to install the update and launch the updated version of Reason.
     D   Click “Install on Quit” to continue running the current Reason version and install the update after you quit the
         current Reason session.

42   INTRODUCTION


---

<a id="common-operations-and-concepts-2"></a>

=== END OF PART ===
