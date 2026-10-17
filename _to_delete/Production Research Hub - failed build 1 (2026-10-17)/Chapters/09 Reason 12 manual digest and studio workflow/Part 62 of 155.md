# Chapter 09: Reason 12 manual digest and studio workflow
## Part 62 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 53 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 63 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 53 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 25: Optimizing Performance

Optimizing
Performance

      Introduction
      Reason is a program of infinite possibilities. You can create extremely complex songs, with a vast number of audio
      tracks and rack devices. While this is one of the most exciting properties of the program, it does have a drawback –
      it means that you must be careful with how you manage your computer processing power.
      Each audio track and device you add in your song uses up a bit of computer processing power – the more audio
      tracks and devices, the faster the computer has to be. However, you can set up your devices to require more or less
      processing power. For example, a sound on the Subtractor synthesizer that only uses one oscillator and one filter re-
      quires less processing power than one using both dual oscillators and dual filters.
      Samples used in your songs also require RAM (memory) to load properly. The use of RAM can also be managed, as
      described at the end of this chapter.
      When collaborating on songs with other Reason owners, you should do what you can to reduce the requirements for
      playing back a certain song, both in terms of processing power and in terms of RAM requirements. Other users may
      not have as powerful a computer as you do!

      Checking overall processing power
      To the right on the Transport Panel you will find a meter labeled DSP. This indicates how much processing power is
      used at any given moment.

      The DSP meter on the Transport Panel
      The higher this meter goes, the higher the strain on your computer processor. You will note when your processor is
      heavily loaded that graphics will update slower. Finally, when there’s too little power left to generate audio properly,
      the sound will start to break up.

      Checking processing power for individual devices
      There is also a function for displaying the processing power of individual devices in the rack. This lets you pinpoint
      any CPU hogs, letting you possibly replace those devices with less CPU demanding ones if necessary.
      D   Select “Show CPU Load for Devices” from the Options menu.
          The CPU Load for the devices is shown in their upper right corners:

          Dr OctoRex is currently using 1% CPU together with its Mix Channel device, and Grain is using 15% CPU together with its Mix
          Channel device
      • Each Mix Channel/Audio Track device shows the total CPU sum of their connected devices, including any In-
        sert Effects.

      Optimization and latency reduction
      As described in “About latency” in the Audio Basics chapter, you generally want the lowest possible latency, to get
      the best response when you record and play in Reason in real time. However, selecting too low a latency is likely to
      result in playback problems (clicks, pops, dropouts, etc.). There are several technical reasons for this, the main one
      being that with smaller buffers (lower latency), the average strain on the CPU will be higher. This also means that the
      more CPU-intensive your Reason song (i.e. the more devices and audio tracks you use), the higher the minimum la-
      tency required for avoiding playback difficulties.
      Therefore, you may need to adjust the latency. This is done differently depending on which audio cards, drivers and
      operating system you are using.

      Making Buffer Size adjustments in the ASIO Control Panel (Windows)
      If you are using an ASIO driver (Windows only) specifically written for the audio hardware, you can in most cases
      make settings for the hardware in its ASIO Control Panel. This panel (opened by clicking the ASIO Control Panel but-
      ton in the Preferences-Audio dialog) may or may not contain parameters for adjusting the latency. Usually this is
      done by changing the number and/or size of the audio buffers - the fewer and smaller the audio buffers, the lower
      the latency. Please consult the documentation of your audio hardware and its ASIO drivers for details.
      !   Raising the buffer size to eliminate audio artefacts on playback is mainly effective if you are currently using
          very small buffers, 64 to 256 samples. If the buffers are already big (1024 or 2048 samples) you will not notice
          much difference.

      Making Buffer Size adjustments in the Reason Preferences dialog
      If you are running Reason under Windows and are using an ASIO driver, or under macOS and are using a Core Audio
      driver, you can adjust the input and output latencies in the Preferences – Audio dialog.
      D   This is done by dragging the Buffer Size slider.

      General procedure for reducing latency
      The basic procedure for optimizing the latency is the following:
      1. Open a song and start playback.
          You want to choose a song that is reasonably demanding, i.e. with more than just a few tracks and devices.
      2. Open the Preferences dialog.
          Under macOS, this is found on the Reason menu; under Windows it’s found on the Edit menu.
      3. Click the Audio tab and locate the Buffer Size slider.
      !   If you are making adjustments in the ASIO Control Panel for hardware with an ASIO driver (Windows only), you
          should make a note of the current buffer settings before changing them.
      4. While the song is playing, listen closely for pops and clicks and try lowering the latency (Buffer Size).
      5. When you get pops and clicks, raise the Buffer Size value a bit.
      6. Close the Preferences dialog (and ASIO Control Panel, if open).

      About Latency Compensation
      Below the Input Latency and Output Latency rows in the Preferences-Audio dialog, you will find an item called Re-
      cording Latency Compensation. This value is used internally in Reason to compensate for latencies when recording
      audio using external monitoring.

      Recording Latency Compensation
      !   Adjusting the Recording Latency Compensation parameter is never necessary when you have selected “Auto-
          matic” in the Monitoring section on the Audio page in Preferences - see “Monitoring”.
      Recording Latency Compensation is when the program adjusts the position of the recorded audio according to the
      current latency. Here's how it works:
      If you're recording audio and are not monitoring through Reason (e.g. monitoring directly through the audio card or
      via an external mixer), the audio you record will reach the program slightly late. This is because you play along with
      background tracks or the metronome - and you hear these delayed by the output latency. Also, the sound you record
      is sent to the program via the buffers in the audio hardware - it is delayed by the input latency.
      Reason compensates for this by moving the recorded audio earlier by the sum of the input+output latencies. This
      compensation is also done in "Manual Monitoring" mode, if Monitor was Off for the recorded track (when you started
      recording).
      If Monitor is On, there is no Recording Latency Compensation. This is because the monitored sound will also be de-
      layed, and numerous tests have shown that the performer will actually play slightly ahead to compensate for this. In
      other words, when monitoring through Reason, the performer is expected to do the Recording Latency Compensa-
      tion himself/herself.
      If you are monitoring via an external mixer, and have selected “External” in the Monitoring section on the Audio tab in
      Preferences, there might be situations where you experience that the recorded audio is generally played back too
      early - or too late - in the song. This could be because your audio card doesn’t actually have the latency values it re-
      ported to Reason.
      If you should experience that your audio recordings are played back too early or too late compared to the instrument
      tracks in your song, you can adjust this by editing the Recording Latency Compensation parameter:

      D   Click the Recording Latency Compensation spin controls to compensate for early or late playback of audio
          track recordings
          If the audio appears too early during playback, adjust to a negative (-) value.
          If the audio appears too late during playback, adjust to a positive value.

      Optimizing your computer system
      In this manual we do not have the possibility to give you detailed procedures for optimizing your computer for maxi-
      mum power. This is a subject that we could write complete books on. However, there are a couple of very useful
      things to check and adjust.

      About Multi-core processors
      When you’re using a multi-core processor, such as a dual-core or quad-core processor, Reason will take full advan-
      tage of this in a very sophisticated way. Similarly, if your computer has several multi-core processors, Reason will use
      the full capacity of these to enhance the performance.
      In the “Max audio threads” drop-down you can select the maximum number of audio threads Reason should be al-
      lowed use. The “Default” setting equals the total number of physical cores in your computer’s CPU (corresponding to
      the old "Use multi-core audio rendering" option, but without the "Use hyper-threading audio rendering" option in
      older Reason versions). On Apple M1 the Max audio threads setting defaults to the number of high performance
      cores.

      This preference can also be used to limit the number of threads if you want to leave room for other apps or perhaps
      multi-core VSTs.
      • If you should experience performance problems in Reason, try selecting another Max audio threads number,
        starting from the highest number and going down one number at a time until you get the best performance.
      q   If you are using a dual-core Intel CPU and previously used the "Use multi-core audio rendering" and "Use hy-
          per-threading audio rendering" functions available in earlier Reason versions, select the "3 (HT)" setting to get
          the equivalent performance.

      About hyper-threading audio rendering
      Hyper-threading audio rendering could improve the performance even further. Note that this depends on your com-
      puter’s CPU and other hardware, so there is no guarantee the performance will improve. If you are experiencing per-
      formance problems, try activating or deactivating this to see if the performance improves.

      About audio rendering using the audio card buffer size setting

      The “Render audio using audio card buffer size setting” function should be selected (ticked) for best plugin perfor-
      mance. When selected, the audio batches are rendered internally according to the set Buffer size (see “Making Buf-
      fer Size adjustments in the Reason Preferences dialog” above). For example, if you have a Buffer size of 512
      Samples, each audio batch will be 512 samples internally. Raising the Buffer size will let Reason process larger audio
      batches in one go, which is often more efficient. Many plugins are also more efficient when doing larger audio
      batches. if you are using DSP-heavy VSTs (mastering effects, for example), these will run a lot smoother with this
      function selected.

      !   Note that old songs might sound different with this function selected, if the songs uses feedback routings and
          CV connections.
      If unchecked (off), all audio batches are rendered internally at a fixed size of 64 samples - regardless of the Buffer
      size setting. This might be desirable if you are using feedback signal routings and CV connections in your songs, and
      want the internal latency of those connections to be fixed at a short value all the time. This might result in perfor-
      mance problems for DSP-heavy VSTs, though.
      Unchecked will give the same performance as in Reason 10.2 and older versions.

      About hard drives
      Most state-of-the-art hard drives, including SSD drives, will work perfectly together with Reason. Generally, the faster
      hard drive(s) you use, the better. Most mechanical hard drives of today runs at 5.400 rpm or faster, which is sufficient
      for use with Reason. A large hard drive is also highly recommended when working with DAWs like Reason. A single
      song with a lot of recordings in it could easily reach around 1 GB in final size. During recording and editing, the song
      file size could be a lot bigger than that, so a hard drive space of at least 20 GB is definitely recommended.

      General optimization tips
      Finally, we’d like to share a couple of other general optimization tips:
      • Quit other programs that are running at the same time as Reason.
      • Remove background tasks on your computer.
          This might be any background utilities you have installed as well as networking, background Internet activities etc.
      • Under Windows, make sure you use the latest and most efficient ASIO driver for your audio card.
      • Only work on one Reason Song document at a time.
          Songs that are open in the background do consume some processing power, even though they’re not playing.
      • Lower the sample rate setting on the Audio tab in the Preferences dialog.
          This is a very quick and convenient way to try to play a song that your computer otherwise can’t handle.
      • Raise the Buffer size on the Audio tab in the Preferences dialog.
          See “Making Buffer Size adjustments in the Reason Preferences dialog”.

      Optimizing Songs
      Below follows things you can check and change to make sure your song uses as little computer processing power
      and memory as possible:

      Global
      • To reduce the Song file size, delete unused recordings on Audio Tracks.
        This won’t affect the processing power but will reduce the Song file size, which might be desirable in many situa-
        tions. See “Delete Unused Recordings”.
      • Use the “Save and Optimize” function when you’re finished editing your song.
        As a final step, after you have recorded and edited your song, use the “Save and Optimize” function on the File
        menu. This will remove any “empty” disk areas in the song file, making the file as small as possible - see “Saving
        and optimizing a Song”.
      • Bounce Mixer Channels.
        If you’re using a lot of devices in an instrument track, you could bounce the instrument track to an Audio Track. Do-
        ing so makes it possible to delete the instrument track afterwards and thus reduce the processing power. See
        “Bouncing Mixer Channels”.
      • Delete unused devices.
        If a device isn’t actually doing anything, delete it from the rack.
      • Use fewer devices.
        For example, instead of using several similar reverbs as separate insert effects, replace them all with one, set up as
        a send effect on a Send FX bus in the Main Mixer. By the same token, try to use one sampler playing several dif-
        ferent samples instead of numerous samplers playing one sample each.
      • Don’t use stereo unless it is required.
        For example, if a sampler or Dr. Octo Rex loop player is playing mono material, only connect the Left output and
        leave the Right output unconnected.

      Main Mixer
      • Make sure you deactivate any channel strip parameters or sections you don’t use in your song.
        This could, for example, be Input Gain and INV, EQ, Filters, Dynamics and Insert FX.
      • Delete any Mix Channel devices and/or Audio Track devices you don’t use in your song.

      Sample Players – NN19, NNXT, Dr. Octo Rex, Grain and Redrum
      • Only activate High Quality Interpolation (where applicable) when it is required.
        Listen to the sound in a context and determine whether you think this setting makes any difference.
      • If you are playing back a sample at a much higher pitch than it was recorded at, consider sample rate convert-
        ing the actual sample file to a lower sample rate.
        This will require an external sample editor with good sample rate conversion facilities.
      • Try to refrain from using stereo samples.

      Filters – Subtractor, Thor, Malström, NN19, NNXT, Grain, Europa and Dr. Octo Rex
      • Deactivate filters that are not used.
        Observe that if the Cutoff is all the way up or the envelope is set to open the filter fully, then the filter doesn’t affect
        the sound. Conserve processing power by disabling the filter altogether.
      • Where applicable, use the 12dB lowpass filter instead of the 24dB lowpass filter.
        See if you can get the same sonic result by using the 12dB filter, since it uses up less processing power.

      Polyphonic Devices – Subtractor, Thor, Malström, NN19, NNXT, Grain, Europa, Dr.
      Octo Rex and Redrum
      • Try making the device play fewer voices.
          This can be done for example by lowering the release and setting the Polyphony setting to exactly the maximum
          number of notes played simultaneously by this device.
      !   Note that just lowering the polyphony setting has no effect. Unused voices do not consume processing power.
      • Where applicable, try the Low Bandwidth (Low BW) setting.
          This will remove some high frequency content from the sound of this particular device, but often this is not notice-
          able (this is especially true for bass sounds).

      Subtractor
      • Try avoiding using Oscillator 2 altogether.
          If you can create the sound you need with only one oscillator, this saves considerable amounts of processing
          power.
      • Do not use the oscillator Phase mode if you don’t need it.
          In other words, set the Oscillator Mode switches to “o”, not “*” or “–”.
      • Do not activate Noise unless required.
      • Do not activate Filter 2 unless required.
      • Do not use FM unless required.
          In other words, set the oscillator FM knob to “0” and make sure no modulation source is routed to FM.

      Thor
      • In general, unload any filters or oscillators that aren’t used.

      Malström
      • If it isn’t necessary, refrain from using Osc B at all.
          If you can produce the desired sound by using Osc A only, this will save a lot of processing power.
      • If one or both Oscillators are routed to one Filter only, and/or the Spread parameter is set to “0”, only connect
        one of the outputs (the one to which the filter is connected) to the mixer, and leave the other one unconnected.
      • Try to see if you can achieve the desired effect by using only one of the filters, and without using the shaper.
          Using both of the filters and the shaper in conjunction requires considerably more processing power than using
          just one of the filters and/or the shaper.

      Redrum
      • Do not use the Tone feature available on channels 1, 2 and 9.
          Make sure the Tone controls and their accompanying Vel knobs are set to “0” (“twelve o’ clock” position).

      Mixer devices
      • Avoid using stereo inputs when not required.
          For example, if your sampler or Dr. Octo Rex player is playing mono material, only connect it to the Left input on a
          mixer channel. Leave the Right input unconnected.
      • Do not activate EQ (Mixer 14:2 only) unless required.
          If a channel doesn’t make use of EQ, make sure it’s EQ button is deactivated.

      Distortion
      • The D-11 Foldback Distortion will use up less CPU power than the Scream 4 Distortion device.

      Reverb
      • The RV-7 uses much less power than the RV7000.
        For some applications the RV-7 might do just fine, and will use up much less power.
      • If you are running out of processing power, try the Low Density algorithm for the RV-7.
        This uses up much less power than other algorithms.

      Send Effects
      • When you are using mono effects as send effects, you can connect the effect returns in mono as well (discon-
        nect the cable to Aux Return Right on the Main Mixer).
        This is true for the following effects:
      • D-11 Distortion
      • Scream 4 Distortion
      • ECF-42 Envelope Controlled Filter
      • COMP-01 Compressor
      • PEQ-2 Parametric EQ
      • DDL-1 Delay (provided the Pan parameter is set to center position).
      • MClass effects; Equalizer, Compressor, Maximizer.

      RAM requirements
      Songs not only use up system resources in terms of processing power and hard disk space, they also require RAM
      (memory) to load at all. The amount of RAM required for loading a song, is directly proportional to the amount of sam-
      ples used in the song. For example, a song which uses only Subtractors and effects requires very little RAM.
      If you are running out of RAM try the following:
      • Close other Song documents.
        All open songs compete for RAM.
      • Terminate other applications.
        All running applications compete for the RAM available in the computer.
      • Use mono samples instead of stereo ones.
        Mono samples require half the amount of RAM.
      • Try sample rate converting sample files to a lower sample rate.
        Note that this could affect sound quality negatively. Also note that it will require an external sample editor with
        good sample rate conversion facilities.

626   OPTIMIZING PERFORMANCE


---

<a id="hardware-interface-26"></a>

=== END OF PART ===
