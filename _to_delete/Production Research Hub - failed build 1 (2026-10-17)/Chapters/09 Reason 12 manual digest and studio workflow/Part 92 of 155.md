# Chapter 09: Reason 12 manual digest and studio workflow
## Part 92 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 83 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 93 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 83 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 39: Radical Piano

Radical Piano

      Introduction

      Radical Piano is designed to be a straightforward, awesome sounding and very flexible piano. Radical Piano com-
      bines sample playback technology with physical modeling to give you great sound quality and seamless dynamic re-
      sponse as well as great freedom to tweak your sounds.
      The combination of sample playback and physical modeling also makes it possible to keep each piano sound set
      down to a minimum size. This allows for very quick loading times when you switch between instruments.
      Radical Piano also features sympathetic resonance, which means that any undamped strings will ring along with the
      played notes (strings), just like on acoustic pianos. This makes Radical Piano sound extremely realistic and alive.
      There are also a number of other controls for further shaping the sound the way you want it.
      As a bonus, we also included an audio input so you can route external audio and process it in Radical Piano!

      The pianos
      Radical Piano holds complete sound sets recorded from these three pianos:
      • Home Grand
        A Bechstein grand piano with a nice “not perfectly tuned” home grand character.
      • Deluxe Grand
        A Steinway Model D grand piano - one of the greatest grand pianos out there. This particular one belongs to
        Sveriges Radio (Swedish Radio Ltd).
      • Upright
        A Futura upright piano with a distinct “living room” character.

      The microphone configurations

      The microphone configurations for the grand pianos and the upright piano respectively.
      The pianos were recorded using up to nine microphones per instrument, placed at various critical positions inside and
      outside of the pianos. The different microphone recordings were then stored in Radical Piano as separate sound sets.
      The following microphone configurations were used:
      • Vintage Mono
         A single microphone placed outside the waist of the grand piano (or behind the upright piano). For the Steinway
         grand piano we used an old school mono ribbon mic with vintage characteristics and a narrow frequency response
         with the emphasis in the mid range. For the Futura upright piano we used a vintage tube microphone.
      • Ambience
         Two microphones in AB configuration* placed quite far away from the piano to capture the room ambience.
      • Floor
         Two pressure zone microphones that lay flat on the floor just behind the front legs of the grand piano (and behind
         the upright piano). They add depth and richness to the sound and are best used as a complement to the other
         mics.
      • Jazz
         Two microphones in AB configuration* placed just outside/in front of the piano. This gives a full bodied sound with
         a wide stereo image and a less pronounced attack.
      • Close
         Two microphones in XY configuration** placed close to the hammers. The close mics produce a distinct sound with
         a sharp attack, ideal for uptempo pop/rock.
      * AB configuration: Two mics in stereo configuration placed several feet apart and tilted slightly away from each
      other.
      ** XY configuration: Two mics in stereo configuration placed close together in 'V' shape at a 90° coincidence.

      Using Radical Piano
      Loading and saving patches
      Loading and saving patches is done in the same way as with any other internal Reason device, see “Loading patches”
      and “Saving patches” for details.

      Selecting piano sound sets
      A patch in Radical Piano can consist of a mix between two piano sound sets. The mix could be between two sound
      sets from the same piano, or from different pianos. You could, for example, blend a Close mic’ed upright piano with
      the Floor microphones from a grand piano to create your own custom piano sound. The piano sound sets can be se-
      lected in the Piano Select section:

      The Piano Select section.
      1. Select desired piano sound set(s) by clicking the corresponding LED button(s).
          You can select one sound set to the left of the Blend knob and one to the right.
      2. Set the mix between the sound sets with the Blend Microphones knob.
          If you only want to use a single sound set for your sound, set the Microphone Blend knob to min or max.

      Character

      D   Set the character of the sound with the Character knob.
          Range: Subdued to Agitated, in 24 steps, with natural sound at the 12 o’clock position.
          Subdued produces a warm and mellow tone whereas Agitated generates a brighter and significantly more pro-
          nounced tone.
      !   Changing the Character value temporarily mutes the audio outputs.

      Volume

      The master volume control for Radical Piano.

      Velocity Response

      Most sample-based piano instruments and sound libraries on the market use a predefined number of velocity layers.
      Depending on how soft or hard you play the keys, samples from a specific velocity layer play back. Due to memory
      limitations, the number of velocity layers aren’t often that many. This can make the velocity response feel and sound
      unnatural. Thanks to the combination of samples and physical modeling in Radical Piano, all sound sets feature very
      wide and completely seamless velocity ranges.
      With the Velocity Response knobs you can tailor the dynamic response of your piano sound.
      • With the High knob you set the timbre for the highest velocity.
          Note that the High parameter can go far beyond the natural range of an acoustic piano, which is great for experi-
          mental sounds.
      • With the Low knob you set the timbre for the lowest velocity.
          With the Low knob set to zero (marked with an ‘S’) playing really soft won’t play back any sound at all. This can be
          useful if you, for example, want to hold down a chord and then play other keys to introduce the sympathetic reso-
          nance effect, see “Resonance”.
      • With the Curve knob you set the shape of the velocity curve - from exponential, via linear to logarithmic.
          Set this parameter where it feels the best to play. There is no “perfect” position since most MIDI keyboards re-
          spond differently to velocity.
      q   If you want a natural dynamic range, set the Low knob to around the 9 o’clock position and the High knob to
          around the 12 o’clock position. Adjust the Curve setting to your liking.
      q   If you want a dynamic range that stretches beyond the range of an acoustic piano, set the Low knob to zero
          and the High knob past the 12 o’clock position.
      q   If you want a static response (with the same timbre no matter how soft or hard you play), set the Low knob to
          max and the High knob to zero. Note that there will still be some velocity sensitivity left for controlling the vol-
          ume.

      Tune

      Cent
      D   Set the overall master tune of your sound with the Cent knob.
          Range: +/-1 semitone (+/-100 cents).

      Drift
      The Drift parameter can be used for introducing a slow irregular pitch variation to your sound. It’s perfect for adding
      kind of a “scary” or melancholic touch to your piano sound.

      Sustain

      The Sustain parameter is a special feature in Radical Piano. It lets you control the piano sustain continuously from
      pedal up to pedal down. As on acoustic pianos, the sustain pedal is not either “on” or “off - it can be “somewhere in
      between” as well. The Sustain function in Radical Piano simulates this behavior.
      The Sustain parameter can be controlled either from the Pedal LED strip control on the front panel or from a Sustain
      pedal connected to the Sustain Pedal input of your MIDI master keyboard.
      • When you use a standard (switch type) sustain pedal connected to a standard sustain pedal input on your MIDI
        keyboard, this will control the Sustain function in Radical Piano as either Off (‘0’) or On (‘127’).
          You could record using the standard sustain pedal and then manually edit the Sustain Pedal performance control-
          ler data in the note clip in Reason afterwards and adjust the “in between” Sustain levels.
      !   The Sustain parameter value (and LED bar) will always adjust to the latest incoming Sustain Pedal data, be it
          from the Pedal LED strip control or from a sustain pedal connected to your MIDI keyboard.

      Resonance

      Sympathetic resonance is a physical phenomenon that can occur in acoustic instruments, like in pianos for example.
      It means that any undamped strings will ring along with the played strings. For example, if you play a key with the sus-
      tain pedal down, all other strings in the piano will also vibrate at various intensities. Similarly, if you hold down a num-
      ber of keys (so that the dampers are off the strings) and then play additional keys, the strings for the held keys will
      resonate.
      With the Resonance controls you set the amount of sympathetic resonance in your piano sound.

      Level
      D   Set the amount of overall sympathetic resonance in your sound.

      Release Time
      D   Set the time it should take for the sympathetic resonance to fade to silence.

      Envelope

      Radical Piano features a special type of envelope generator which is used for shaping the character of the piano
      sound.

      Attack
      D   Set the attack time for the piano sound, from immediate to (unnaturally) slow.
          The range is 0-200 ms.

      Decay Curve
      D   Set the shape of the decay curve.
          This control determines how the sound should decay when you play and hold the keys.
          The range is from exponential, via linear, to logarithmic. Exponential settings will make the sound decay faster,
          which simulates a piano with little body sustain. Logarithmic settings makes the sound sustain more slowly and
          simulates a piano with a lot of body sustain.

      Release
      D   Set the time it should take for the sound to fade to silence once you release the keys.
          This simulates the behavior of the dampers. For example, worn out dampers could result in somewhat longer re-
          lease times.

      Mechanics

      The Mechanics section features controls for the mechanical noise.

      Key Down
      • Key Down controls the level - and character - of the noise that occurs when the keys are pressed/hit.
          At the 12 o’clock position the noise is the most natural. Above the 12 o’clock position the noise is more pro-
          nounced and below the 12 o’clock position the noise is suppressed.

      Key Up
      • Key Up controls the level of the noise that occurs when the keys are released and the hammers and dampers
        return to their initial positions.
          At the 12 o’clock position the noise level is natural. Above the 12 o’clock position the noise is louder and below the
          12 o’clock position the noise is quieter.

      Pedal
      • Pedal controls the level of the noise that occurs when you press and release the sustain pedal.
          At the 12 o’clock position the noise level is natural. Above the 12 o’clock position the noise is louder and below the
          12 o’clock position the noise is quieter.

      EQ

      The built-in equalizer is a powerful 3-band EQ with gain controls for the Low, Mid and High bands. The EQ charac-
      teristics have been fine tuned and optimized for piano sounds. The gain range is +/-18dB for each of the bands,
      which makes it easy to quickly achieve great sonic results.
      The EQ can be switched on/off by clicking the LED button at the top.

      Ambience

      The Ambience section features four different reverb types and a Level control. The reverb types are:
      • Small Room
          This simulates the acoustic reflections in a small room.
      • Large Room
          This simulates the acoustic reflections in a large room.
      • Hall
          This simulates the acoustic reflections in a medium size hall.
      • Theater
          This simulates the acoustic reflections in a large hall/theater.

      Output

      Comp(ression)
      This controls the amount of compression of your piano sound.

      Width
      This lets you set the stereo width of the piano sound.
      !   Note that the Width control does not have any effect on the sound if you use only the “Vintage Mono” piano
          sound set(s), see “Selecting piano sound sets”.

      Connections
      !   Remember that CV connections will not be stored in the Radical Piano patch!

      Sequencer Control
      The Sequencer Control CV and Gate inputs allow you to play Radical Piano from another CV/Gate device (typically a
      Matrix or an RPG-8). The signal to the CV input controls the note pitch, while the signal to the Gate input delivers
      note on/off along with velocity.

      Modulation In
      These control voltage (CV) inputs (with associated trim pots) can modulate following parameters in Radical Piano:
      • Pitch
          The Pitch can be modulated at a maximum range of +/-1 octave.
      !   Note that +/- 1 octave is the maximum range a piano sound can be pitch shifted in Radical Piano. This as-
          sumes that no Pitch Bend performance controller is used (see “Pitch Bend”) and that the Character knob is set
          to Natural (see “Character”).
      • Master Volume

      Audio In
      Route an external audio signal to this input to process it with the Resonance, EQ, Ambience and Compression effects
      in Radical Piano.
      q   Routing a vocal signal and processing it with the sympathetic resonance effect (with the sustain pedal down)
          could generate really interesting results. It would be like singing into a piano body!

      Audio Out
      These are the main audio outputs. When you create a new Radical Piano device, these outputs are auto-routed to the
      first available Mix Channel in the main mixer. If there is no Mix Channel available, a new one will be automatically cre-
      ated.

      Additional external control
      The Radical Piano responds to the following standard Performance Controllers:
      • Pitch Bend
          Radical Piano responds to Pitch Bend data from the pitch bend control of your MIDI master keyboard.
          The range is fixed at +/-7 semitones.
      !   Note that the Character setting (see “Character”) as well as any Pitch CV modulation (see “Pitch”) can reduce
          the Pitch Bend range.
      • Sustain Pedal
          If you have a standard (switch type) sustain pedal connected to a standard Sustain Pedal input of your MIDI mas-
          ter keyboard, this can be used for controlling Sustain On/Off. You can then edit the Sustain values in your note
          clips in the sequencer afterwards and set continuous values all the way between 0-127, see “Sustain” for more
          details.

954   RADICAL PIANO


---

<a id="klang-tuned-percussion-40"></a>

=== END OF PART ===
