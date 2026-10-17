# Chapter 09: Reason 12 manual digest and studio workflow
## Part 40 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 31 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 41 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 31 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Creating parallel chords
      The Scales & Chords Player is great for generating chords that stay within a set scale, but sometimes you may want
      chords that keep their form when you play different notes. For example, you might want a minor 9th chord that is
      transposed with the notes you play, but stays a minor 9th chords (like with the Chord Memory function of some syn-
      thesizers, for example). This can be called “parallel chords”, and is actually best done with the Note Echo device:
      1. Set Step Length to 0.
      2. Raise the Repeats value to maximum.
      3. Set the Pitch to +1 semitone.
        This means that each repeat is 1 semitone higher than the previous - and since Step Length is 0, they are all
        played at the same time. If you play a note now, you get a dense cluster of notes - not very musical or useful, but
        let’s continue:

      4. Click the Repeat circles in the display to turn off the notes you don't want.
          This is how you would set up a minor 9th chord for example:

      5. Play different (single) notes on your MIDI Control Keyboard/On-screen Piano Keys to get parallel, transposed
         chords.
          You could also add a Dual Arpeggio Player after the Note Echo for cool arpeggios!
      q   The Note Echo device comes with a number of ready-made chord patches. You find them by clicking the
          Browse Patch button on the Note Echo device and opening the “Chords” sub-folder in the browser.

      Using a Scales & Chords device as a “MIDI Note monitor”
      Sometimes it might be interesting to see in real-time what notes/chords a Player or “Player chain” actually generates.
      1. Add a Chords & Scales device last (at the bottom) in the Player chain.
      2. Make sure Scale is set to “Chromatic” and that Filter Notes and Chords are Off.
          When you play through your Player(s) the generated notes/chords are now displayed in the Scales & Chords key-
          board display:

          The “Creating parallel chords” example monitored in a Scales & Chords device when playing the note C.

372   WORKING WITH PLAYERS


---

<a id="working-with-rack-extensions-13"></a>
# Chapter 13: Working with Rack Extensions

Working with
Rack Extensions

      About this chapter
      This chapter describes the procedures and techniques for managing Rack Extension devices.

      What are Rack Extensions?
      Rack Extensions are additional rack devices that can be purchased in the Reason Studios web shop at
      www.reasonstudios.com/shop and used together with the internal devices in the rack. Rack Extensions can be in-
      struments, effects or utility devices, such as mixers and CV processors. Rack Extension devices are developed by
      Reason Studios as well as by 3rd party companies.
      Rack Extension devices integrate fully with the Reason rack:
      • Cables can be connected on the rear panels, just like on the internal rack devices.
      • CV signals can be routed like on the internal rack devices.
      • Rack Extension devices are combinable with other Rack Extension and internal devices (see “The Combinator”
        chapter).
      • Panel parameters are automatable and remotable.

      Future compatibility
      Rack Extensions are Windows and Mac-compatible and will work with any operating system and platform that Rea-
      son supports - now and in the future.

      Trying and buying Rack Extensions
      Trial versions of Rack Extensions
      You can try out a Rack Extension by going to the Reason Studios web shop at www.reasonstudios.com/shop and us-
      ing the "Try" function. This gives you a trial license which will last for 30 days (counted from when you clicked the
      “Try” button). During this time, the Rack Extension is fully operational, with no limitations.
      When the trial license expires, the Rack Extension will be removed from the program menus. However, it will remain
      installed unless you manually uninstall it. Should you choose to purchase the Rack Extension later on, you don't need
      to download it again.
      You can only try a Rack Extension once (one 30-day period).

      Buying Rack Extensions
      When you purchase a Rack Extension, a license is automatically written to your Reason Studios user account on the
      Reason Studios web site. Just like with your Reason license, you can write a Rack Extension license to your autho-
      rized computer. You can download and install the Rack Extension on as many computers as you like. However, to use
      the Rack Extension in Reason you either need your authorized computer or an Internet connection to run with Inter-
      net Verification.
      !   Rack Extension devices are not available when you run Reason in Demo Mode.
      If you move to another computer, you can download and install all your Rack Extensions by going to the Devices tab
      in the Reason Companion app and clicking the "Install all" button. This function is also excellent for making sure you
      got the latest versions and updates of all your Rack Extensions. Only files that are missing on your computer will be
      downloaded and installed.

      Rack Extensions can be updated, with fixes and additions. Updates are indicated on the Devices tab in the Reason
      Companion app. Rack Extensions are backwards compatible, meaning that you can open older songs and patches
      and they will sound the same.

      Rent-to-Own Rack Extensions
      An alternative to purchasing Rack Extension licenses one at a time is to use the Rent-to-Own program. To utilize
      Rent-to-Own Rack Extensions, please go to the Reason Studios web shop at www.reasonstudios.com/shop.

      Installing and managing Rack Extensions
      !   in Reason 12.7 and later, Rack Extension installation and management is handled completely in the Reason
          Companion app - not by Authorizer, which is now deprecated.
      Whenever you download and install a Rack Extension, from the web shop or your user account, this will be handled
      by the Reason Companion application. Reason Companion will automatically launch when you Buy, Try or Download
      a Rack Extension from the Reason Studios web shop.
      Reason Companion checks what's already installed on your computer, downloads any missing files and puts them in
      the correct locations.
      !   Reason Companion automatically writes Rack Extension licenses to your computer, when applicable.
      If you want to check what Rack Extensions are installed on your computer, you need to launch Reason Companion:
      D   Either select Rack Extensions from the Window menu in Reason or locate the Reason Companion application
          on your computer and launch it manually.
          Reason Companion lists all currently available Rack Extensions on the Devices tab:

          The Devices tab in Reason Companion lists the Rack Extension devices currently installed on your computer.
      • If you are subscribing to Reason+, the Reason+ Rack Extensions are listed at the top of the Devices tab.
          Further down on the Devices tab your purchased Rack Extensions are displayed in the “My Rack Extensions” sec-
          tion.
      • You can search for a Rack Extension, by typing in its name (or the first part of the name) in the Filter Rack Ex-
        tensions box.
      D   Click the Update all button to update all currently installed Rack Extension to the latest versions.
          Note that only the Rack Extensions in the corresponding section (Reason+ Rack Extensions or “My Rack Exten-
          sions”) are affected.
      D   Click the Install all button to install all Rack Extensions displayed on the Devices tab.
          Note that only the Rack Extensions in the corresponding section (Reason+ Rack Extensions or “My Rack Exten-
          sions”) are affected.

      D   Click the Update/Install/Uninstall buttons to perform the corresponding actions for individual Rack Exten-
          sions.
          If you have purchased the Rack Extension (or if it’s included in your Reason+ subscription), you can always rein-
          stall an uninstalled Rack Extension at any time.

      Using Rack Extensions in Reason
      Rack Extensions behave just like internal Reason devices, and are listed together with the Reason devices in the
      Create menu subgroups and on the Device Palette in the Browser:

      The A-List Power Drummer Rack Extension is available from the Create menu and on the Instruments palette in the Browser.
      The installed Rack Extension devices are sorted in the appropriate subgroups and are listed, per manufacturer, in al-
      phabetical order. However, Rack Extension devices from Reason Studios are always placed first in the list, below the
      internal Reason devices.
      D   Click the Show/hide RE button to choose whether or not to show 3rd-party Rack Extensions in the browser:

      D   To create a Rack Extension device, either select it in the appropriate subgroup in the Create menu, double click
          or drag and drop from the Device Palette in the Browser, or select “Create Instrument...” or “Create Effect...”
          from the Create menu.
          The Rack Extension device is placed in the rack and routed according to the standard rules, see “Creating de-
          vices”.

      If a Rack Extension supports patches, you will find the included patches in the Rack Extension itself. To get there:
      1. In the Browser, click "Rack Extensions" in the locations list to the left.
        This lists all available Rack Extensions in alphabetical order:

      2. Double click a Rack Extension folder (or click the expansion triangle) in the list to browse its patch content.

        If you are browsing patches from a Rack Extension device (by clicking the “folder” button on the device panel),
        patches and folders for that specific device type are displayed in the Browser list right away.

      About missing Rack Extensions
      When you open a Reason song from another user, it may have been created with Rack Extensions that you don't
      have. It might be a song from a friend, or a song that you have made using a Rack Extension with a trial license (that
      has since expired).
      When you open such a song, the following alert appears:

      Now, you can choose to open the song without the Rack Extension(s), or go to the Reason Studios web shop and Try
      or Buy the missing Rack Extension(s). If you click OK, the song opens without the missing Rack Extension(s).
      All such missing devices in a song are replaced by generic placeholder devices:

      A “Missing Device” placeholder plate for a Rack Extension device, which is currently unavailable on your computer.
      The placeholder device itself will be silent. If it's an effect, it will bypass the sound (or be silent, if connected as a send
      effect).
      If you're collaborating with a friend you can safely save the song and send it back. When your friend opens the song,
      the Rack Extension device will be restored with all settings intact.

      Acquiring missing Rack Extensions
      If you change your mind and want to hear the song with the Rack Extension(s) included, you could either download
      a paid version or a trial version from the Reason Studios web shop:
      1. Click inside the “View in web shop” area on the placeholder panel to get to the Reason Studios web shop and
         Try or Buy the Rack Extension:

      2. After you have downloaded the (paid or trial) Rack Extension device(s), restart Reason and open the song
         again.
         Now, the Missing Device placeholders have been replaced by the downloaded Rack Extension(s) and the song will
         sound as originally intended.


---

<a id="working-with-vst-plugins-14"></a>

=== END OF PART ===
