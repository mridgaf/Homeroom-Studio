# Chapter 09: Reason 12 manual digest and studio workflow
## Part 39 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 30 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 40 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 30 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

         C4
                                  Step 1                  Step 2                 Step 3                 Step 4
           H  ld                                     Pl   d b  k
        If you hold down C4 and E4, the pattern plays back note C4 on step 1, note E4 on step 2, note C5 on step 3 and
        note E5 on step 4. So, the two held notes are played back one octave higher on steps 3 and 4:
           Held notes:                                 Played back notes:

         C4
                                      Step 1                 Step 2                  Step 3                   Step 4
        If you hold down C4, E4, and G4 the pattern plays back C4 on step 1, E4 on step 2, G4 on step 3 and C5 on step
        4. As you can see, the lowest held note is played back one octave higher on step 4:
           Held notes:                                 Played back notes:

         C4
                                      Step 1                 Step 2                  Step 3                   Step 4

      Velocity
      In default mode, when the Velocity function is off, the velocities of the input notes set the velocity of each generated
      note in the arpeggio/pattern. If you want to define the velocity values and draw them in manually, you can activate the
      Velocity function.
      1. Click the Velocity switch:

      2. Click or click-hold and drag the blue Velocity bars to manually set the velocity values.
        When you play your chords, the input velocity is disregarded and replaced by the values you drew in the display.
        Range: 0-127.

      Shift Step

      D   Change where in the arpeggio/pattern you want the playback to begin.
          Range: -16 to + 16 steps.

      Transpose

      D   Transpose all the generated arpeggio/pattern notes equally, in semitone steps.
          Range: -24 to + 24 semitones.

      Gate Length

      D   Change the lengths of the generated arpeggio/pattern notes.
          Here you can change the “gate/hold” time for the generated arpeggio/pattern notes. 100% means the gate time
          is exactly one full Step. A Length of 25% results in a gate time of 1/4 of a Step and a Length of 400% means a
          gate time of four Steps.
          Range: 25%-400%.

      Note Echo

      Note Echo simulates a MIDI delay effect, by adding repeats of the incoming MIDI notes. The Note Echo device is
      polyphonic, so you can get repeats of entire chords if you like.

      Step Length
      The Step Length knob controls the echo time, and consequently also the time between the repeats. The step length
      range is 0 to 1000 milliseconds. When Tempo Sync (see below) is enabled, the range is 1/128 notes up to ½ note.
      q   A Step Length of 0 makes it possible to create chords and clusters, since all steps are played back simultane-
          ously. See “Creating parallel chords” for a practical example.

      Tempo Sync
      Switch on to sync the Step Length (see above) to the Reason sequencer tempo.

      Repeats
      This knob sets the number of repeats, from 1-16. The number of repeats is also shown in the display.

      Velocity
      The Velocity knob controls the linear increase or decrease of the Note Velocity value for each step.
      The range is from 10% to 200%, where 100% means the velocity value is left unchanged throughout the repeats.
      Values below 100% means a decrease of the velocity values, and values above 100% means increasing velocity with
      each repeat.
      The velocity values are represented by blue bars in the display. The blue line in the bars indicates the 100% value.

      Pitch
      With the Pitch knob you set how many semitones each step should be transposed relative to the previous step. The
      function is linear for all repeats. The Pitch values are represented by orange bars in the display.
      The range is –12 to +12 semitones. 0 is the default value and means no transposition of the input notes.
      !   If you use very high or very low Pitch value settings together with many Repeats, the note range of the associ-
          ated instrument might be exceeded. If this happens, any remaining repeats will be silent.

      Display
      Aside from showing number of Repeats, Velocity and Pitch (transposition) information, the display can also be used
      if you want to mute individual repeats.
      D   Click the desired green circles in the display, to mute the corresponding repeat.
          This way you can create interesting rhythmic repeats. The first green circle (to the left in the display) represents
          the incoming “dry” MIDI Note. This can be muted as well, if you like. By default, all repeats are on (unmuted).

      Scales & Chords

      The Scales & Chords device either transposes incoming notes to fit a set scale, or transposes notes and generates
      chords that fit the desired scale. Scales & Chords has a number of built-in preset scales, and you can also create your
      own custom scales!
      Here are some examples of how you can use it:
      • to get chords from single note inputs.
      • to get new chord voicings and progressions that feel fresh and inspires your music making.
      • to experiment with existing note lines, by transforming them to different scales.
      • to get the notes you play to automatically fit the music.
      • to easily be able to play chords without using a MIDI Control Keyboard.
          You could write single MIDI notes in a Note clip and have the Scales & Chords Player generate the chords for you.
      • to get chords that sound right, without knowledge of tonality/scales.

      Scales
      In the Scales section you choose which key and scale you want.
      q   Note that all parameters in the Scales section can be automated, so you could change key and scale anywhere
          throughout your song if you like!

      Key
      D   Click to select the desired Key from the list that appears.
          12 Keys are available, from C to B.

      Scale
      D   Click to select the desired Scale from the list that appears.
          13 scales are available, plus a Custom scale that you can create yourself (see below). The preset Scales are:
          Major, Minor, Lydian, Mixolydian, Spanish, Dorian, Phrygian, Harmonic Minor, Melodic Minor, Major Pentatonic,
          Minor Pentatonic, Hemi Pentatonic and Chromatic.

      • The notes that fit the selected Key and Scale are displayed in light blue in the keyboard display in the Scales
        section:

          The Dorian scale in the key of E.
          The notes in the selected Key and Scale are then automatically repeated throughout all octaves of the entire MIDI
          Note range.
      • Notes you play on your MIDI Control Keyboard/On-screen Piano Keys are indicated in orange in the Scales
        keyboard display.

      Creating a Custom Scale
      D   Create a custom Scale by clicking the desired keys in the keyboard display in the Scale section:

          Selected notes are colored light blue. The selected notes are then automatically repeated throughout all octaves
          of the entire MIDI Note range.
      • You can easily switch between your Custom Scale and any of the preset Scales whenever you want, by clicking
        the “Scale” display and selecting the desired scale from the list that appears.
      • Your Custom Scale is automatically saved with the song.
          Your Custom Scale is also saved in the Scales & Chords patch, should you choose to save your settings as a
          patch.

      Filter Notes
      • When the Filter Notes switch is off (default), incoming notes outside the set Scale (see “Scales”) are trans-
        posed to fit the scale.
          Wrong notes are automatically transposed to the closest correct note. If the wrong note is equally near two correct
          notes, the wrong note is transposed to the lowest of the correct notes.
      • When the Filter Notes switch is on, incoming notes that are outside the set scale will be filtered out (silent) in-
        stead of transposed.
          The display below shows a hand symbol whenever wrong input notes are filtered out (silent).

      Chords
      D   Switch on the Chords function to generate chords out of single notes.
          When you play a note, you will get a chord that fits the set Scale (see “Scales”), and contains the number of notes
          set with the “Notes” knob. The generated notes are shown in real-time in the keyboard display at the bottom of the
          Chords section:

      !   If you play several notes at the same time you will get several chords, which might be cool or just weird. If
          notes in the generated chords should coincide, only one instance of the notes are played back (to avoid dou-
          bled/layered notes).
      q   If you want to create “parallel chords”, i.e. chords that contain notes with the same relative intervals, the Note
          Echo device is better suited for this, see “Creating parallel chords”.

      Notes
      D   Set the desired number of notes in the generated chords.
          Range: 1-5 notes.

      Inversion
      The Inversion knob defines which note in the generated chord should be the lowest. The function tries to keep the
      lowest generated note in the chord as close to the played root note as possible. Below is an example of inversions of
      a generated 4-note chord in the Scale C Major, played from a C note of the MIDI Control Keyboard:

                        Inversion 0:

          C                C             C

                        Inversion 1:

          C                C             C

                        Inversion 2:

          C                C             C

                        Inversion 3:

          C                C             C

      Inversions of a generated 4-note chord played from the (orange) C note.
      !       Note that the Inversion function is only relevant if the Inversion number is less than the selected “Notes” value.
              So, if the Notes value is 4, only a maximum Inversion value of 3 is useful.

      Open Chords
      When the Open Chords function is active, some notes in the generated chords are transposed in octave steps, so
      that the notes are not so close to each other. The transposition is different depending on the “Inversion” and the
      “Notes” settings.

      Add
      The Add functions can be used for adding notes to the generated chords:
      • The Add Oct Up function adds a note one octave above the root note.
      • The Add Oct Down function adds a note one octave below the root note.

      • The Add Color function adds a note two thirds above the highest note in the tertian chord structure.
          If the Notes value in the Chord section is 3, you will get a regular triad (e.g. a C major). Adding a sixth above top will
          mean adding a 9 (e.g. the note D). Similarly, if the Notes value in the Chord section is 4, this will add an 11; if the
          Notes value in the Chord section is 5, this will add a 13.
      q   All three Add functions can be used together, simultaneously.
      !   If the added note is already used in the chord (due to inversions, open chord etc), the note is transposed up an-
          other octave (or down, in case of Oct Down).

      Alter
      The Alter button is a momentary button that turns off as soon as you release the mouse button (like the Trig button
      on The Echo, for example). It alters the chord slightly so that it goes outside the current scale. The result depends on
      the Key (as set in the Scale section), whether the current scale is major or minor and what note you play (relative to
      the Scale Key).
      The chord is altered by having one of the chord notes changed. For example, a major chord may be changed to a mi-
      nor chord, or vice versa.

      Beat Map

      The Beat Map Algorhythmic Drummer is a Player that generates drum patterns based on built-in beats, algorithms
      and simple but powerful controls. It's normally used with a drum instrument such as Kong, Rytmik or Umpf, but can
      also be used with melodic instruments for interesting results.

      Included content
      To browse the content of Beat Map, click "Rack Extensions" in the Browser and then double click the Beat Map
      folder:

      Beat Map comes with a number of patches, both for the Player itself and for several different drum devices. The drum
      device patches are tailored to work well with Beat Map, but you can of course use any patch from the Factory Sound
      Bank, or make your own.
      If you want immediate results, start by loading one of the patches in the Combinator Style Patches folder! These
      combine Beat Map with drum devices and effects for instant rhythmic goodness.
      If you want a taste of what can be done with multiple Beat Maps in combination with other devices, check out the
      Demos and Song Starters folder.
      !   Note that some of the combi patches use Rack Extensions included with Reason Suite.
      Finally, the Template Key Mappings folder contains Beat Map patches where the keys (note numbers) have been
      adapted for other drum configurations such as GM, Reason Drum Kits and various 3rd party drummers.

      The front panel

      The central item on Beat Map's panel is the Map display. This is where you select a basic rhythm, by clicking and
      dragging the cross-hair.
      • The cross-hair position is also indicated with the X and Y position parameters, which you can edit directly if
        you like.
      Each integer XY position corresponds to a different beat. The map graphics are there for visual reference and for the
      nice looks – there is no particular rhythmic significance to the elements on the map. However, as a general rule, mov-
      ing the position to the right will make the bass drum pattern more syncopated and moving the position upwards will
      make the snare pattern more syncopated.
      • Clicking the Spawn XY button drops you at a random position:

      Map Select
      1. Click the Map Select button to show the four included maps:

        They contain beats in different styles – click on a map to see some info about it in the display.
      2. To select a map for use, either double click it or select it and click Map Select again.

      Density

      The beats consists of four different rhythmic patterns, for kick, snare, hi-hat and percussion. Once you've found a
      beat that you like, you can adjust the Density of each drum. This means reducing or increasing the number of notes.
      Turning Density down to zero will mute that drum. The Density parameters can be automated or CV controlled, for
      continuous variations.
      • Clicking the Random Density button to the left will change all four Density controls to random values, useful
        for live variations:

      Lock Position

      You may find a beat where for example the kick is perfect, but not the other drums. Then you can click Lock Pos for
      the kick. This will put a "pin" on the map – the kick beat will stay at this position but you can continue exploring the
      map for the other instruments.
      This can be done independently for all four drums, locking them to different map positions. This way you can combine
      rhythms from different basic beats, for infinite variations.
      !   You can still adjust Density for locked drums.

      Mirror notes

      Each of the four drums has a "Mirror" function, which plays a note in between two note positions from it's main drum.
      For example, if the kick beat plays like this:

      ... then its Mirror notes (dark red) will play like this:

      This means that the Mirror notes will be affected by the Density of the main drum, creating interesting counter-
      rhythms or ghost notes.
      Use the Mirror knobs to set the velocity (typically level) of the Mirror notes. Turning the knob down completely will
      turn off the Mirror note.

      Setting MIDI note numbers
      Each drum and Mirror function sends out notes on a separate MIDI note number, meaning that Beat Map can control
      eight different drum sounds.
      • Clicking the red signal LED for a drum will send out that note, for quick auditioning of drum sounds:

        The Perc drum sends out MIDI Note F#1
      • You can set which note a drum should send by clicking and dragging the note number on the panel:

      Alternatively, use the Learn function:
      1. Click Learn Key:

      2. Click the note number value for a drum or Mirror to highlight it.

      3. Play the desired note on your MIDI controller.
      4. Repeat for the other notes.
      5. Click the Learn Key again to exit Learn mode.
        This is required for the changes to stick when you save the patch or song.

      Global settings

      To the right are three settings that affect the overall playback:
      • Rate is the note value of each step. Normally this is set to 1/16th notes.
      • Shuffle allows you to add a swing feel to the beats by delaying the offbeat 1/16th notes.
        You can set it manually from 50-75% or select “Global” to use the Global Shuffle setting (found in the Groove
        mixer in Reason).
      • Reset Step determines the number of steps before the beat starts over from the beginning.
        The default is 64, but it can be useful to lower this to make a beat less varying or to impose some structure on a
        chaotic rhythm.

      Beat Map and the sequencer
      You can click the Run button manually for auditioning the beat, but the Run function is normally controlled by the Play
      function in the main sequencer.
      However, if you want Beat Map to play in certain parts of your song but not in others, it's also possible to control this
      using Pattern automation. Here's how to do this in Reason:
      1. Right-click Beat Map and select “Create Track”.
        This creates a sequencer track for the Beat Map device.

      2. With the Beat Map track selected, click the Create Pattern Lane button above the track list

        This creates a Pattern lane on the Beat Map track. Since there are no pattern clips on the lane, Beat Map will be
        stopped. This will be indicated in the map display:

      3. Draw pattern clips in the sections where you want Beat Map to play:

        Unlike other pattern devices, there is only one pattern to select from here – Pattern 1. This is just a nifty way to
        control playback – you can also use pattern offset to start playback with an upbeat or in the middle of a bar.
      • Alternatively, you could automate the On button to automate the Beat Map playback:

      In addition, most Beat Map parameters can be automated. For example, you can record map movements or Density
      changes.

      A couple of special features:
      • The Locked XY positions can be automated for each drum.
        This allows you to lock a single drum to a rhythm but change it with automation:

      • The Map selection ("Beat Map" parameter) can be automated or controlled from a Combinator.
        Switching to another map can be useful as a break or fill.

      Editing the drum notes
      To manually edit the beats from Beat Map, you need to send the MIDI notes to a sequencer track. You do this with
      the Send To Track function on the Player top panel, see “Common Player device parameters”.

      Using CV

      On the back of Beat Map, you'll find a comprehensive selection of CV inputs and outputs.
      • Density CV in and Mirror Velocity CV in for each drum.
        Using these with a Pulsar CV LFO can create longer, varying rhythmic patterns or random variations. There are
        plenty of examples of this among the Combinator Style Patches.
      • Gate Out from main drums and Mirror sections, allowing you to trigger other sounds or effects in parallel.
      • Reset Step Trig In.
        Whenever this receives a positive CV value, the beat will start over from the first step.
      • Map XY CV Inputs, for automatically modulating the map position during playback.
      • Map XY CV Outputs.
        These send out the X/Y coordinates as CV values, letting you use the Map display as an XY controller for other
        devices in Reason.

      Tips & Tricks
      Generating scale-correct arpeggios from single notes
      By chaining a Scales & Chords device with a Dual Arpeggio device you will be able to generate scale-correct arpeg-
      gios by playing single notes.
      1. Create an Instrument device.
        In this example we create an ID8.
      2. Select the ID8 device in the rack and double-click a Scales & Chords device.
        The Scales and Chords device is automatically attached to the ID8.
      3. Select the ID8 device in the rack and double-click a Dual Arpeggio device.
        The Dual Arpeggio device is attached between the Scales & Chords device and the ID8 device:
      4. On the Scales & Chords device, select Key and Scale, then switch on the Chords function set the Notes knob to
         4.
      5. Play single notes on your MIDI Control Keyboard (or On-screen Piano Keys) and hear how four-note scale-cor-
         rect arpeggios are now generated.

      Generating chord arpeggios
      By chaining a Dual Arpeggio device with a Scales & Chords device you will be able to generate arpeggiated chords.
      1. Create an Instrument device.
        In this example we create an ID8.
      2. Select the ID8 device in the rack and double-click a Dual Arpeggio device.
        The Dual Arpeggio device is automatically attached to the ID8.
      3. Select the ID8 device in the rack and double-click a Scales & Chords device.
        The Scales and Chords device is attached between the Dual Arpeggio device and the ID8 device:
      4. On the Scales & Chords device, select Key and Scale, then switch on the Chords function set the Notes knob to
         3.
      5. Play chords on your MIDI Control Keyboard (or On-screen Piano Keys) and hear how arpeggiated three-note
         chords are now generated.


=== END OF PART ===
