# Chapter 09: Reason 12 manual digest and studio workflow
## Part 79 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 70 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 80 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 70 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 32: Mimic Creative Sampler

Mimic Creative Sampler

      Introduction

      The Mimic Creative Sampler is a powerful yet very straight-forward sampler, tailor-made for quick and easy triggering,
      chopping and manipulation of samples. It features eight sample slots, where each slot can hold one sample. Each slot
      also has its own complete synth parameters setup, with pitch controls, filter, envelopes, LFO and effects.
      You could either load a sample from your computer or sample straight into Mimic (Reason stand-alone only). You can
      then select various sample playback modes and high-quality stretch algorithms to manipulate and process the audio.
      You could also use Mimic as a traditional sampler and just play back samples in a regular “tape-style” fashion.
      Mimic also features a great-sounding “lo-fi style” multi-effect to spice up your sounds even more.
      Don’t forget to check out the Mimic video tutorial here!

      Panel overview
      The Mimic front panel contains the following sections:

          1                                 2                                            3
                                        4                                         5

          6

          7

          8                                     9                            10              11

                                                12                      13                   14

      The Mimic front panel sections.
      • 1. MIDI Note On LED.
      • 2. Patch selector (for browsing, loading and saving patches).
      • 3. Master Volume controls.
      • 4. Playback Mode section.
      • 5. Slot selector.
      • 6. Sample section (for sample loading/sampling and sample playback functions).
      • 7. Playback Start Position, Speed, Stretch and Slices sections.
      • 8. Performance and “play” controls.
      • 9. Pitch section.
      • 10. Filter section.
      • 11. Envelopes section.
      • 12. LFO section.
      • 13. Amp section.
      • 14. Compressor, Effects and EQ sections.

      Signal flow
                          Slots (x8)

                                                           Pitch
                                                             or
                                                                               (x1)
                                                           Slice
                                                                                                                   Separate Out (x8)
                                                                                                                         Master Out
                                                  (x8)                                                      (x8)
                                                                                            Master Volume
                                                         Multi Slot
                                                             or
                                                         Multi Pitch    (x8)

                                                          Send 2 (x8)

                                                          Send 1 (x8)
                                                                        Send 1 Stereo Out          Send 2 Stereo Out

      Mimic signal flowchart.
      • Mimic features eight Slots, where each Slot holds a complete configuration of sample parameters and panel
        parameter settings.
         Each Slot features a Sample section, where you can load your sample - or sample your own (Reason stand-alone
         only). You can then select if you want to play back the sample as Slices or Pitched (chromatically). You can also
         choose among various sample Stretch algorithms. The signal is then routed through a complete configuration of
         synth parameters, such as Pitch, Filter, Amp and Effects.
      • Depending on the selected Slot Mode, the signals from the Slots are be routed a bit differently.
         In Pitch Mode and Slice Mode, only one single Slot can be played back at a time.
         In Multi Slot Mode and Multi Pitch Mode you can play back up to eight Slots simultaneously.
      • The synth sections in Mimic’s eight Slots are described in “Panel reference”.

      Playing and using Mimic
      Loading and saving patches

      A Mimic patch contains the parameter settings for all used Slots, i.e. up to eight complete parameter setups. Loading
      and saving patches is done in the same way as with any other internal Reason device, see “Loading patches” and
      “Saving patches” for details.
      !   Like with the other sampler devices in Reason, the patch does not include the actual sample - only a
          reference to it. Therefore, the sample has to be stored separately (self-contained with the song, or already on
          disk or in a ReFill on your computer).

      Global output controls

      Master Volume
      This is the main stereo output volume control and controls the volume of all eight Slots together.

      Slot Mode

      Mimic has four Slot Modes, which defines how the sample of each Slot should play back - and also if you can use one
      or several Slots simultaneously:

      Pitch Mode

      In Pitch Mode you select one of the eight Slots for melodic playback (playing the sample from the start to the end lo-
      cators). The sample can then be played chromatically pitched over the entire keyboard range.

      Slice Mode

      C1                    C2                  C3                   C4                C5              C6

      In Slice Mode you select one of the eight Slots for playback, and slice a (longer) sample, manually and/or automati-
      cally. The slices are then triggered from the keyboard (chromatically, with the leftmost slice playing back from note
      C1) without affecting the original pitch of the sample. See “Slices” for more details.

      Multi Slot Mode
      In Multi Slot Mode different keys (C-G in each octave) triggers Slots 1-8 (from the start to the end locators), drum-
      machine style - without affecting the sample pitches. This is displayed in the Note/range indicator as follows (the
      currently selected Slot is high-lighted on the keyboard - the others are dark blue):

                  Slot 2             Slot 2               Slot 2            Slot 2          Slot 2          Slot 2
                    Slot 4             Slot 4               Slot 4            Slot 4          Slot 4          Slot 4

                   Slot 3             Slot 3              Slot 3            Slot 3          Slot 3          Slot 3
                Slot 1             Slot 1             Slot 1              Slot 1        Slot 1         Slot 1          Slot 1
      Multi Slot Mode with samples loaded in Slots 1-4.
      q    Multi Slot Mode works great with pad controllers.

      Multi Pitch Mode

              C1                    C2                    C3                 C4              C5         C6

              C1                    C2                    C3                  C4             C5         C6

              C1                    C2                    C3                  C4             C5         C6

              C1                    C2                    C3                  C4             C5         C6

                                  One MIDI keyboard playing four Slots simultaneously (layered)

      Multi Pitch Mode with samples loaded in Slots 1-4, played back in a layered fashion.
      In Multi Pitch Mode you can play back up to eight samples (one sample per Slot) simultaneously, for melodic play-
      back (playing the sample from the start to the end locators). You can set different keyboard ranges (overlapping and/
      or adjacent) for the eight Slots and then play back the samples chromatically pitched. You can set the desired key-
      board range in the Note/range indicator as follows (the currently selected Slot is high-lighted on the keyboard - the
      others are dark blue):

      Setting the key range for the currently selected Slot.
      1. Click the desired Slot button (see “Slot Select” below) to select it.
      2. Drag the left and right note range markers to set the desired note range.
          The minimum “range” for a Slot is one note.
      3. Click another Slot button and set a new desired note range.
      q   Note that Slots can have overlapping note ranges (also completely overlapping so that you could play all eight
          Slots together in a layered fashion).

      Slot Select

      Mimic has eight Slots, which can hold one sample each. Each Slot also has a complete parameter setup on the Mimic
      front panel, so each slot can have its own unique parameter configuration.
      D   Click the desired Slot Select button to bring up all parameters for that slot, including the sample and its set-
          tings.
      !   Note that in Pitch Mode and Slice Mode (see above), only one single Slot can play back its sample at a time (as
          indicated by the grayed out waveforms below the other Slot Select buttons).

      Performance and “play” controls
      Each of the eight Slots has their own individual set of performance/play controls on the front panel:

      Porta
      Portamento makes note pitches glide from previous notes to new ones, at the time set with the Time knob. Porta-
      mento can be used in all Key modes (see above).
      • When On in Poly Key Mode (see below), the pitches will glide from any of the available voices.
          The results will be unpredictable since there is no way of controlling from which note(s) the glide(s) will com-
          mence. The effect is very nice, though.
      • When On in Mono Retrig or Mono Legato Key Mode (see below), the pitch will glide between consecutive
        notes.
      • In Auto mode, the pitch will glide between consecutive monophonic notes only when you play legato. If you
        have selected Poly Key Mode (see below), Auto will have no effect at all.
          If you release the previous key before hitting the new key, there will be no portamento effect.

      Key Mode
      Here you choose how Mimic should respond to MIDI Note data:
      • Poly
          Select this if you want to play Mimic polyphonically.
      • Mono Retrig
          Select this if you want to play Mimic in monophonic mode and always retrigger the envelopes as soon as you play
          a new note.

      • Mono Legato
          The Mono Legato mode is also monophonic. However, if you play a new note without having released the previous
          one, the envelopes and sample playback position won’t start over.
      q   Also see the description of the “Global Position”, which allows new notes to continue playing at the current
          sample playback position (and not restart playback).

      Pitch Range
      D   Set the desired Pitch Bend range for the “Pitch Bend” wheel with the up/down buttons, or by click-holding on
          the display and dragging up/down.
          Range: +/-24 semitones (+/-2 octaves) in steps of +/-1 semitone.

      Pitch Bend
      The Pitch Bend wheel can be used for bending note pitches up and down. Mimic also responds to Pitch Bend MIDI
      data from a connected MIDI master keyboard. You set the desired Pitch Bend Range with the “Pitch Range” control
      above the Pitch Bend wheel.
      !   Note that if you have selected the Tape Stretch algorithm (see “Tape”), pitch bending the sample will also
          affect its playback speed.

      Mod Wheel
      The Mod Wheel can be used for modulating a number of parameters in the eight Slots of Mimic. Use the Mod Wheel
      as a source parameter for the panel parameters that feature modulation source drop-down selectors.

      LFO Scale
      The LFO Scale knob can be used for scaling the LFO amount with the Mod Wheel - perfect for gradually introducing
      Vibrato effects, for example. If the LFO Scale knob is set to 100% the LFO Amount will be 0 when the Mod Wheel
      is at 0. See “The LFO section” for more details about the LFO.

      Panel reference
      The Sample section
      Here is where you load/sample the audio for the currently selected Slot. The Waveform display differs somewhat, de-
      pending on which Slot Mode you have selected (see “Slot Mode”).
                                                  Sample range markers
                                                                                               Root Key section
                 Start marker indicator                     End marker indicator

                                           Sample Overview
                                                                                                  Slice markers
                                                                                       End
                                                                                       marker
          Start
          marker                      Position marker                                       Waveform display

                    Sample Load/Sampling section                                         Note/range indicator

      A sample loaded in a Slot with Slice Mode selected.

      Loading/sampling
      D   Load a sample using drag & and drop, or by clicking the Browse sample button, or by using the Up/Down but-
          tons to scroll and load a sample from the currently selected folder.
      D   Drag a sample from the browser and drop on a Slot Select button, to load the sample in the desired Slot.
      D   Alternatively, sample straight into Mimic by clicking the Start sampling button (Reason stand-alone only):

          See the “Sampling” chapter for more information about setting up and using Reason for sampling.
      !   It’s possible to load/sample stereo signals. However, the waveform will always be displayed as a mono signal,
          regardless if it’s mono or stereo.

      Root Key
      A sample is automatically analyzed for its original pitch at the Sample Start position. The analyzed pitch is displayed
      in the Root Key section. If you move the Sample Start marker, the sample is automatically re-analyzed.
      D   Click the “SET” button to use the analyzed Root Key.
          This will automatically place the analyzed Root Key on the correct note on the keyboard, as indicated by an orange
          key in the Note/range indicator below the Waveform display.

      D   Alternatively, set the Root Key manually by dragging up/down in the “Root” and “Tune” (cent) boxes:

      !   Note that the Root Key function only works in Pitch Mode and Multi Pitch Mode.

      Setting the sample range
      First you could decide how much of the original sample you want to use - and where in the sample you want to work:
      D   Zoom and/or scroll in the Sample Overview to define the Sample range you want to work in.

          To scroll, click and drag sideways between the dark yellow sample range markers. To zoom, click and drag any of
          the sample range markers sideways. The set Sample range is automatically updated and displayed in the wave-
          form display.
      D   To work in the entire Sample range, drag the left Sample range marker all the way to the left, and the right
          Sample range marker all the way to the right, in the Sample Overview.

      Zooming in the Waveform Display

      D   Click and hold the mouse button anywhere in the waveform display, then drag down to zoom in, and up to
          zoom out in the waveform.
      q   Dragging sideways in the Waveform Display will scroll left/right.

      Setting the sample start and end

      D   Drag the Start and End marker handles to where you want the sample to begin and stop playing back.
          Note that the Start and End markers cannot be set in reversed order. If you want to play the sample backwards,
          from the End marker to the Start marker, click the Reverse button (see “Reverse”).

      • If you drag and move the Start/End marker up into the Slice Marker area above the waveform, the Start/End
        marker will snap to the closest slices. This works in all modes, not just in Slice Mode:

      D   Alternatively, double click in the Waveform Display to position the Start marker. Hold down [Shift] and double
          click to position the End marker.

      Previewing samples
      D   Preview the sample by holding down [Option]/[Alt] and clicking at the desired position in the Waveform Dis-
          play.
          The sample will play back for as long as the mouse button is depressed.
      q   It’s possible to automate the sample start and end settings, see “Automating the sample Start and End mark-
          ers”.

      Loop and Loop Length

                                                                                             Looped region

      It’s also possible to loop (Forward Loop) samples - or slices in Slice Mode. The loop always happens at the end of the
      sample/slice. In all modes except for Slice Mode the Loop Length is visually indicated with a transparent red region
      in the Waveform Display, so you can see exactly where the loop is.
      D   Enable Loop by clicking the Loop LED.
      D   Adjust the Loop Length by turning the Length knob, or by holding down [Command]/[Ctrl] and clicking/drag-
          ging sideways in the waveform display:

          If you are playing back the sample reversed (see “Reverse”) the looped region originates from the Start Marker in-
          stead and is displayed in transparent blue.
      !   In Slice Mode the looped region is not indicated visually in the Waveform Display.

      Start Position

      The Start Position section contains controls for determining where the sample/slice playback should begin, and in
      which direction the sample/slices should be played back.

      Global Position
      D   Click the Global Position LED to start the playback of new/additional voices from the global position, i.e. from
          where the red Position marker is currently positioned in the Waveform Display:

          This function is great for polyphonic rhythmic sounds, where you want to have all the voices synced in time.
          If not active, new/additional voices will always start playing back from the blue Sample Start marker.

      Reverse
      D   Click the Reverse LED to have the sample/slices play back backwards, from the end to the start.

      Start Position Mod
      D   Turn the Mod knob to set a modulation amount for the sample/slice playback start position.
          Note that the Mod amount is bipolar (-/+) so that you can modulate the start position either earlier or later than the
          default start position.
      D   Select a Modulation source from the drop-down selector, to modulate the sample/slice start position.
      !   The Start Position Modulation behavior also depends on the “Snap to Slices” setting described below.

      Snap to Slices
      D   Click the Snap to Slices LED to always start the playback from a Slice Marker (and not from somewhere in be-
          tween Slice Markers).
      !   Note that this function is only useful in when modulating the Start Position (see above) in Pitch Mode, Multi
          Slot Mode and Multi Pitch Mode, since the Start Position always snaps to slices in Slice Mode (see “Slice
          Mode”).

      Speed and Speed Mod

      The Speed control determines how fast the play position (“playhead”) moves in the waveform.

      Speed
      D   Set the sample playback speed with the Speed knob.
          Depending on which Stretch type (see “Stretch”) is currently selected, the sonic result will vary. If you have se-
          lected the Tape Stretch type (see “Tape”), the Speed knob also affects the pitch. Note that the Speed can be set
          all the way down to 0%, i.e. “stop”. Great for Tape Stop effects in Tape mode and for static playback in other
          Stretch types, for example.

      Speed Mod
      D   Modulate the Speed with the Mod knob.
      D   Assign a modulation source from the drop-down selector next to the Mod knob.
          For example, selecting an Envelope as a modulation source could cause the playback speed to start fast and grad-
          ually slow down when you hold a note - or vice versa.

      Stretch

      Mimic features five different Stretch types, which can be selected from the drop-down selector. Depending on the
      selected Stretch type, there are also some additional controls to modify the sample characteristics.

      Tape

      This is the good old “tape recorder” type, where speed and pitch are coupled. This means that to achieve a higher
      pitch you simply increase the playback speed of the sample/slices - and vice versa.
      With the Tape stretch type selected, there is a Loop X-Fade knob present. This controls the crossfade amount when
      the Loop function is active for the sample/slices (see “Loop and Loop Length”).
      If Loop is off, the Loop X-Fade knob has no effect.

      Advanced

      This is a high-quality stretch algorithm suitable for most type of polyphonic and complex audio material.

      With the Advanced stretch type selected, there is a Preserve Transients button present. Transients are regions in the
      sample where the level quickly goes from quiet to loud, for example in percussive hits and other types of “attacks”.
      D   Click the Preserve Transients button to preserve any transients in the sample/slices.
          When off, any transients will be “smeared out” and less prominent, which might be desired in some situations.

      Melody

      This is the Melody stretch type used for audio in the Reason sequencer, i.e. a high-quality stretch algorithm suitable
      for monophonic audio material.
      With the Melody stretch type selected, there is a Preserve Transients button present.
      D   Click the Preserve Transients button to preserve any transients in the sample/slices.
          When off, any transients will be “smeared out” and less prominent, which might be desired in some situations.
      q   The Melody stretch type is well suited if you are using the Loop function (see “Loop and Loop Length”), since
          it usually reduces clicks/pops at the loop point.

      Vocal


=== END OF PART ===
