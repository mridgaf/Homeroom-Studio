# Chapter 09: Reason 12 manual digest and studio workflow
## Part 45 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 36 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 46 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 36 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      | File type                | Extension                 | Description
      Reason Song                 .reason or .rns             This is the main document format in Reason. It contains the recordings on all audio, in-
                                                              strument and automation tracks - and the device setup in the rack, along with refer-
                                                              ences to any used instrument samples and loops - or it can contain the actual samples
                                                              and loops if you have made the song “self-contained” (see “About Self-Contained
                                                              Songs”). Opening a Reason Version 5 (or earlier) song will retain the original rack con-
                                                              figuration, but will route the signals originally connected to the Out 1 and 2 of the Rea-
                                                              son Hardware Interface to a new Mix Channel (see “About opening Reason Version 5
                                                              (or earlier) Songs in Reason Version 12”).
      Reason Demo Song            .rsndemo                    A Reason Demo Song is a factory made song intended to demo the sound and fea-
                                                              tures of the Reason program. Reason Demo Songs, Reason Essentials Demo Songs
                                                              and Record Demo Songs are the only song file types that can be opened when you run
                                                              Reason in Demo Mode (without authorization). See “Opening a Reason Demo Song”.
      Reason Published Song       .rps                        A Reason Published Song is a self-contained Reason song (created in Version 5 or
                                                              earlier) intended for playback only. It can only be opened in Reason and cannot be
                                                              changed. Its components cannot be extracted and it is only possible to export the song
                                                              as an audio file if you haven’t edited anything. Opening a Reason Published Song song
                                                              in Reason will retain the original rack configuration, but will route the signals originally
                                                              connected to the Out 1 and 2 of the Reason Hardware Device to a new Mix Channel
                                                              (see “About opening Reason Version 5 (or earlier) Songs in Reason Version 12”).
      Reason Adapted Song         .rsb                        A Reason Adapted Song is a song created in a Reason Adapted version. Opening a
                                                              Reason Adapted Song song in Reason will retain the original rack configuration, but
                                                              will route the signals originally connected to the Out 1 and 2 of the Reason Hardware
                                                              Device to a new Mix Channel (see “About opening Reason Version 5 (or earlier) Songs
                                                              in Reason Version 12”).
      Record Song                 .record                     This is the main document format in Propellerhead Record. It contains the recordings
                                                              on all audio, instrument and automation tracks - and the device setup in the rack, along
                                                              with references to any used instrument samples and loops - or it can contain the actual
                                                              samples and loops if the song is “self-contained” (see “About Self-Contained Songs”).
      Record Demo Song            .recdemo                    A Record Demo Song is a factory made song intended to demo the sound and features
                                                              of the Propellerhead Record program. Record Demo Songs, Reason Demo Songs and
                                                              Reason Essentials Demo Songs are the only song file types that can be opened when
                                                              you run Reason in Demo Mode (without authorization). See “Opening a Reason Demo
                                                              Song”.

      | File type              | Extension          | Description
      Reason Essentials Song   .ree                 This is a song created in Reason Essentials. It contains the recordings on all audio, in-
                                                    strument and automation tracks - and the device setup in the rack, along with refer-
                                                    ences to any used instrument samples and loops - or it can contain the actual samples
                                                    and loops if the song is “self-contained” (see “About Self-Contained Songs”).
      Reason Essentials Demo   .reedemo             A Reason Essentials Demo Song is a factory made song intended to demo the sound
      Song                                          and features of the Reason Essentials program. Reason Essentials Demo Songs can
                                                    be opened and edited in Reason just like a regular Reason Essentials Song.
      Reason Limited Song      .rltd                This is a song created in Reason Limited. It contains the recordings on all audio, instru-
                                                    ment and automation tracks - and the device setup in the rack, along with references to
                                                    any used instrument samples and loops - or it can contain the actual samples and loops
                                                    if the song is “self-contained” (see “About Self-Contained Songs”).
      Combinator Patch         .cmb                 The Combinator can store/recall combinations of Reason devices. Combinator patches
                                                    (Combis) will save all panel settings (as well as sample references if used) for all de-
                                                    vices that are part of the Combi. In addition, all routing (audio/CV) between devices in
                                                    the Combi are included in the patch. Effect Combi patches are also used for Insert FX
                                                    patches in the Main Mixer.
      Subtractor Patch         .zyp                 This is a patch for the Subtractor synth device, containing all panel settings. You store
                                                    your synth sounds by saving Subtractor patches.
      Thor Patch               .thor                This is a patch for the Thor synth device, containing all panel settings. You store your
                                                    synth sounds by saving Thor patches.
      Malström Patch           .xwv                 This is a patch for the Malström synth device, containing all panel settings. You store
                                                    your synth sounds by saving Malström patches.
      NN19 Sampler Patch       .smp                 This is a patch for the NN19 Sampler device, containing references to and settings for
                                                    all used samples, along with panel settings.
      NN-XT Sampler Patch      .sxt                 This is a patch for the NN-XT Sampler device, containing references to and settings for
                                                    all used samples, along with panel settings.
      Redrum Patch             .drp                 This is a patch for the Redrum drum machine device. It contains information about
                                                    which drum samples are used, along with all drum sound settings. In effect, a Redrum
                                                    patch is a stored drum kit.
      Dr. Octo Rex Patch       .drex                This is a patch for the Dr. Octo Rex Loop Player device. It contains information about
                                                    which REX Loops are used, along with all loop and panel parameter settings.
      Kong Kit Patch           .kong                This is a patch for the Kong Drum Designer device. It contains information about what
                                                    drum samples/modules are used, along with all drum sound settings for all 16 chan-
                                                    nels. In effect, a Kong Kit Patch is a complete stored drum kit.
      Kong Drum Patch          .drum                This is a patch for a single Drum channel in the Kong Drum Designer device. It contains
                                                    information about which drum samples/modules are used, along with all drum sound
                                                    settings for one single Drum channel.
      RV7000 Patch             .rv7                 This is a patch for the RV7000 reverb effect, containing all panel settings.
      Scream 4 Patch           .sm4                 This is a patch for the Scream 4 distortion effect, containing all panel settings.
      The Echo Patch           .echo                This is a patch for The Echo delay effect, containing all panel settings.
      Pulveriser Patch         .pulver              This is a patch for the Pulveriser effect, containing all panel settings.
      Alligator Patch          .gator               This is a patch for the Alligator gate effect, containing all panel settings.
      REX files                .rx2, .rcy or .rex   REX files are created in another Reason Studios application, the ReCycle loop editor.
                                                    REX files contain audio loops chopped into slices, with one slice for each significant
                                                    beat in the loop.
                                                    REX files can be imported to Audio Tracks in Reason and are automatically converted
                                                    to audio files. By loading a REX file into the Dr. Octo Rex Loop Player device, you can
                                                    play back the loop in virtually any tempo (without affecting the pitch), manipulate indi-
                                                    vidual beats in the loop, extract timing info, etc.
                                                    Note that you can also load REX files into the samplers, the Redrum drum machine and
                                                    Kong Drum Designer.

      | File type               | Extension                  | Description
      Audio files and Samples   .wav, .aif, mp3 etc.         Audio files of various formats, resolutions and sample rates can be imported to Audio
                                                             Tracks in Reason. All sampler devices in Reason can also load and play back samples
                                                             and audio files in these formats. You can use files of different formats in the same de-
                                                             vice - one drum sound can be an 8-bit sample, the next a 16-bit sample, etc.

                                                             The audio file format support differs depending on which computer OS you are using.

                                                             In macOS, the following audio file formats are supported:
                                                             .wav (not floating point), .aiff (not floating point), .3g2, .3gp, .mp1, .mp2, .mp3, .mpeg,
                                                             .mpa, .snd, .au, .sd2, .ac3, .aac, .adts, .amr, .caf, .m4a .m4r and .mp4.

                                                             In Windows, the following audio file formats are supported:
                                                             .wav (not floating point), .aif (not floating point), .mp3, .aac, .m4a and .wma
      SoundFont Bank            .sf2                         The SoundFont format was co-developed by E-mu Systems and Creative Technologies
                                                             and is used with many audio cards and software synthesizers. SoundFont banks store
                                                             wavetable synthesized sounds, allowing users to create and edit multi-sampled sounds
                                                             in special Soundfont editing programs. The SoundFonts can then be played back in
                                                             wavetable synthesizers, typically on audio cards, thereby effectively turning an ordinary
                                                             sound card into a sampler.
                                                             The NN-XT and NN19 Samplers and the Redrum drum machine allow you to browse
                                                             and load SoundFonts. Regardless of which editing program was used to create them,
                                                             these banks are similarly and hierarchically organized, with folders for instruments, pre-
                                                             sets, samples etc. The NN-XT, NN19 and the Redrum lets you load individual samples
                                                             and presets from a SoundFont bank, but not the complete SoundFont.
      Rack Extension Patch      .repatch                     These are patches for Rack Extension devices. All Rack Extension devices use the
                                                             same file extension but the patch files contain different data depending on which de-
                                                             vice was used for creating them.
      VST Patches               .fxp and .fxb VST2 patches   Reason can read the VST2 patch formats fxp and fxb and the VST3 patch format
                                .vstpreset VST3 patches      vstpreset. Provided that the VSTs are installed and detected by Reason, the patches
                                                             can be opened in the corresponding VSTs.


---

<a id="routing-audio-and-cv-16"></a>

=== END OF PART ===
