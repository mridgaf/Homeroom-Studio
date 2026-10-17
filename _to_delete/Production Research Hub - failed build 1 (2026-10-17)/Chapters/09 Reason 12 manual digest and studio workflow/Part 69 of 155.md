# Chapter 09: Reason 12 manual digest and studio workflow
## Part 69 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 60 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 70 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 60 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Sets the Pan (stereo position) for the channel.
      D   If the LED above the Pan control is lit, the sound uses a stereo sample.
          In that case, the Pan control serves as a stereo balance control.

      Level and Velocity

      The Level knob sets the volume for the channel. However, the volume can also be affected by velocity (as set with the
      Dynamic value, or as played via MIDI). How much the volume should be affected by velocity is set with the “Vel” knob.
      D   If the Vel knob is set to a positive value, the volume will become louder with increasing velocity values.
          The higher the Vel value, the larger the difference in volume between low and high velocity values.
      D   A negative value inverts this relationship, so that the volume decreases with higher velocity values.

      D   If the Vel knob is set to zero (middle position), the sound will play at a constant volume, regardless of the ve-
          locity.
          When Vel is set to zero, the LED above the knob goes dark.

      Length and the Decay/Gate switch

      The Length knob determines the length of the drum sound, but the result depends on the setting of the Decay/Gate
      switch:
      D   In Decay mode (switch down), the sound will decay (gradually fade out) after being triggered. The decay time is
          determined by the Length setting.
          In this mode, it doesn’t matter for how long a drum note is held (if played back from the main sequencer or via
          MIDI) - the sound will play the same length for short notes as for long notes. This is the traditional “drum machine”
          mode.

      D   In Gate mode (switch up), the sound will play for the set Length, and then be cut off.
          Furthermore, if a sound set to Gate mode is played from the main sequencer, from a CV/Gate device or via MIDI,
          the sound will be cut off when the note ends or after the set Length, depending on which comes first. Or in other
          words, the sound plays for as long as you hold the note, but the Length setting serves as the maximum length for
          the sound.
          There are several uses for the Gate mode:
      • For “gated” drum sounds, when the tail of the sound is abruptly cut off as an effect.
      • For when you want to use very short sounds, and don’t want them to “lose power” by being faded out.
      • For when you play the Redrum from the sequencer or via MIDI, with sounds for which the length is important
        (e.g. when using the Redrum as a sound effects module).
      !   Audio samples sometimes contain a “loop”, which is set by editing the audio in a sample editor. This loop re-
          peats a part of the sample to produce sustain as long as you hold down a note. Drum samples usually don’t
          contain loops, but who is to say that Redrum should only play drum samples?
          Note that if a sample contains a loop, and Length is set to maximum, the sound will have infinite sustain, in
          other words it will never become silent, even if you stop playback. Decreasing the Length setting solves this
          problem.

      Pitch

      Sets the pitch of the sound. The range is +/- 1 octave.
      D   When the pitch is set to any other value than 0, the LED above the knob lights up to indicate that the sample
          isn’t played back at its original pitch.

      Pitch Bend

      By setting the Bend knob to a positive or negative value, you specify the start pitch of the sound (relative to the Pitch
      setting). The pitch of the sound will then be bent to the main Pitch value. Thus, selecting a positive Bend value will
      cause the pitch to start higher and bend down to the original Pitch, and vice versa.
      D   The Rate knob determines the bend time - the higher the value, the slower the bend.
      D   The Vel knob determines how the Bend amount should be affected by velocity.
          With a positive Vel value, higher velocity results in wider pitch bends.
      D   The Bend and Vel knobs have LEDs that light up when the functions are activated (i.e. when a value other than
          zero is selected).
      !   Pitch bend is available for drum sound channels 6 and 7 only.

      Tone

      The Tone knob determines the brightness of the drum sound. Raising this parameter results in a brighter sound. The
      Vel knob determines whether the sound should become brighter (positive Vel value) or darker (negative Vel value)
      with higher velocity.
      D   The Tone and Vel knobs have LEDs that light up when the functions are activated (i.e. when a value other than
          zero is selected).
      !   The Tone controls are available for drum sound channels 1, 2 and 10 only.

      Sample Start

      The Start parameter allows you to adjust the start point of the sample. The higher the Start value, the further the start
      point is moved “into” the sample. If you set the Start Velocity knob to a positive amount, the sample start point is
      moved forward with higher velocities. A negative Start Velocity amount inverts this relationship.
      D   When Start Velocity is set to any other value than zero, the LED above the knob lights up.
      D   A negative Start Velocity amount is only useful if you have set the Start parameter to a value higher than 0.
          By raising the Start value a bit and setting Start Velocity to a negative value, you can create rather realistic velocity
          control over some drum sounds. This is because the very first transients in the drum sound will only be heard when
          you play hard notes.
      !   The Sample Start settings are available for drum sound channels 3-5, 8 and 9.

      Global settings
      Channel 8 & 9 Exclusive

      If this button is activated, the sounds loaded into drum channels 8 and 9 will be exclusive. In other words, if a sound
      is played in channel 8 it will be silenced the moment a sound is triggered in channel 9, and vice versa.
      The most obvious application for this feature is to “cut off” an open hi-hat with a closed hi-hat, just like a real one
      does.

      High Quality Interpolation

      When this is activated, the sample playback is calculated using a more advanced interpolation algorithm. This results
      in better audio quality, especially for drum samples with a lot of high frequency content.
      D   High Quality Interpolation uses more computer power - if you don’t need it, it’s a good idea to turn it off!
          Listen to the drum sounds in a context and determine whether you think this setting makes any difference.

      Master Level
      The Master Level knob in the top left corner of the device panel governs the overall volume from Redrum.

      Using Redrum as a sound module
      The drum sounds in Redrum can be played via MIDI notes. Each drum sound is triggered by a specific note number,
      starting at C1 (MIDI note number 36):
          C1                                        C2

               2       4           7       9

          1        3       5   6       8       10

      This allows you to play Redrum live from a MIDI keyboard or a MIDI percussion controller, or to record or draw drum
      notes in the main sequencer. If you like, you can combine pattern playback with additional drum notes, such as fills
      and variations. However:
      !   If you want to use Redrum purely as a sound module (i.e. without pattern playback) you should make sure that
          the “Enable Pattern Section” button is deactivated (see “The Enable Pattern Section switch”), otherwise the
          Redrum pattern sequencer will start as soon as you start the main sequencer.

      Connections

      On the back of the Redrum you will find the following connections:

      For each drum sound channel:
      | Connection         | Description
      Audio Outputs         There are individual audio outputs for each drum sound channel, allowing you to route a drum sound to
                            a separate channel in the mixer, possibly via insert effects, etc.
                            For mono sounds, use the “Left (Mono)” output (and pan the sound using the Pan control in the mixer).
                            When you use an individual output for a sound, the sound is automatically excluded from the master
                            stereo output.
      Gate Out              This sends out a gate signal when the drum sound is played (from a pattern, via MIDI or by using the
                            Trigger button on the device panel). This lets you use the Redrum as a “trig sequencer”, controlling
                            other devices.
                            The length of the gate signal depends on the Decay/Gate setting for the sound: In Decay mode, a
                            short “trig pulse” is sent out, while in Gate mode, the gate signal will have the same length as the drum
                            note.
      Gate In               Allows you to trigger the sound from another CV/Gate device. All settings apply, just as when playing
                            the drum sound conventionally.
      Pitch CV In           Lets you control the pitch of the drum sound from another CV device.

      Other
      | Connection        | Description
      Send Out 1-2         Outputs for the send signals controlled with the S1 and S2 knobs.
      Stereo Out           This is the master stereo output, outputting a mix of all drum sounds (except those for which you use
                           individual outputs).

694   REDRUM DRUM COMPUTER


---

<a id="dr-octo-rex-loop-player-29"></a>

=== END OF PART ===
