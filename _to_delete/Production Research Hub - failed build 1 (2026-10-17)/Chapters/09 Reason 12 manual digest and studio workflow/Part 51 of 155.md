# Chapter 09: Reason 12 manual digest and studio workflow
## Part 51 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 42 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 52 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 42 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

# Chapter 18: Delay Compensation

Delay
Compensation

      About this chapter
      This chapter describes how delay compensation is implemented in Reason.

      About Delay Compensation in Reason
      Delay compensation is desired because some effect devices have inherent latencies, due to internal processing
      (re-sampling, FFT, lookahead compression etc). When a signal passes through such a device, it gets delayed and
      thus “out-of-sync” with other signals. This is especially noticeable if you're using Parallel Channels in the Reason
      mixer, because both the original channel and the parallel channel(s) carry the same source signal. If the effects on
      one of these parallel channels delay the signal, this will be heard as comb filtering, phasing, blurring, etc.
      Traditionally, Reason hasn’t had any delay compensation, mainly because of the totally free routing possibilities. How-
      ever, as from version 9.5 Reason features delay compensation for its native effect devices, Rack Extension effect de-
      vices and VST effect plugins.
      Typically, there are two ways to achieve delay compensation:
      By inserting “invisible” delays on the other signal paths, so that all paths are delayed equally.
      By having the tracks with latency effects in their paths play back earlier.
      • The delay compensation introduced in Reason 9.5 uses the first method only, i.e. inserting delays in the other
        signal paths.

      Activating the Delay Compensation
      The delay compensation can be activated in the Master Section fader section, on the Transport panel, and on the
      Options menu.

      The Delay Compensation button in the Master Section of the Main Mixer.

      The Delay Compensation button on the Transport panel.
      D   Click the Delay Comp button to switch on/off the delay compensation.
          When on, the delay compensation affects all configurations described in “Delay Compensation rules” below.
      • The total signal path latency is displayed (in no. of samples) below the Delay Comp buttons.
          Hovering over any of these latency figures brings up a tool tip which also displays the latency in milliseconds.

      Delay Compensation rules and limitations
      Due to the free routing possibilities in Reason, delay compensation could become infinitely complicated. Therefore,
      we have chosen to keep it fairly simple by imposing some general rules and limitations.
      !   The delay compensation aims at getting a coherent mix using the main mixer in a *standard* configuration. If
          you do unconventional routings, the delay compensation may not work as intended and things might sound
          off. See “Problematic configurations” for examples of problematic routings.

      Delay Compensation rules
      Here are the basic rules for delay compensation in Reason:
      • Delay compensation can be applied to Effect devices that are connected in series between an instrument de-
        vice and the inputs of a Mix Channel device:

          An ID8 instrument device routed via a Scream 4 effect and an RV7000 Reverb effect in series.
          The configuration above can be described schematically in the following picture:

           Instrument device

              Effect device
              with latency

              Effect device
              with latency

               Mix Channel

      • Delay compensation can be applied to Effects devices connected in series as Insert FX in the mixer channels
        (between the "To/From Insert FX" jacks on Audio Track and Mix Channel devices):

        A Scream 4 and an RV7000 effect device routed in series inside a Combinator device in the Insert FX container in a Mix Channel.
        The configuration above can be described schematically in the following picture:

          Instrument device

             Mix Channel

             To Insert FX

            Effect device
            with latency

            Effect device
            with latency

           From Insert FX

      • Delay compensation can be applied to Effect devices that are connected in series between the Parallel Out
        jacks of a Mix Channel or Audio Track device, to the Input jacks of another Mix Channel device:

        The Parallel Outs of a Mix Channel (ID8 3) routed via a Scream 4 and an RV7000 to another Mix Channel (Mix Channel).
        The configuration above can be described schematically in the following picture:

          Instrument device

           Mix Channel 1

          From Parallel Out

            Effect device
            with latency

            Effect device
            with latency

           Mix Channel 2

      • Delay compensation can also be applied to combinations of the three examples above.
          This could be, for example, if an Instrument device is routed in series via Effect devices to a Mix Channel device,
          and the Mix Channel device has Effect devices in series in its Insert FX section. Then, the latency is summed for
          all effect devices in the serial signal chain.
      • Delay compensation can be applied to signals that are sent from the mixer channels to the Send FX busses.
          This means that the signals from the Mix Channels are delay-compensated (if necessary) before they are sent to
          the Send FX busses.
      • Reason fully depends on getting latency values reported from the Effect devices/plugins.
          In other words, Reason doesn’t measure any latency of the effect devices. However, you can manually adjust the
          delay compensation if needed (if things sound wrong due to plugins reporting wrong latencies etc.). See “Manually
          adjusting the latency values” for more details.

      Delay Compensation limitations
      • Only signals routed to a channel in Reason’s main mixer will be compensated. There is no delay compensation
        for the channels on a rack mixer, such as Mixer 14:2.
      • Only signals that pass the Master Section will be compensated (not channels connected using Direct Outs, see
        “About using the Direct Out connections of the mixer channels”).
      • The delay compensation ignores the latency reported by devices connected as Send Effects (see “About Send
        FX Returns”).
      • With some non-standard routings (splits, loopbacks, cross-routing etc), delay compensation may not work or
        may be limited. See “Problematic configurations”.
      • Effects inside an Instrument Combinator are not delay-compensated (but Effect Combis are).
      • CV, MIDI and automation signals are not delay-compensated.
      • MIDI Clock sync and Ableton Link are not delay-compensated.
          However, you can manually adjust the MIDI Clock Sync Offset, see “External synchronization considerations”.

      How the Delay Compensation works
      Delay Compensation in individual mixer channels
      As soon as you add an effect device/plugin as Insert FX in a Mix Channel or Audio Track device - or in the Master
      Section device - the sum of the reported inherent latencies of the effect devices in that channel is displayed (in sam-
      ples) at the bottom of the Insert FX section on the corresponding channel strip in the main mixer. If you add more ef-
      fect devices in an Insert FX chain, the latency figures are added and summed to a total latency value, which is then
      displayed in the respective Insert FX sections:

      Latency values (in samples) displayed in the Insert FX sections on the main mixer channel strips.
      q   Hovering over any of these latency figures brings up a tool tip which also displays the latency in milliseconds.
      What Reason then does to compensate for the inherent latencies in effect devices is to automatically add “invisible
      delays” to the signals of the other mixer channels. The goal for the delay compensation is to have all mixer channel
      signals arriving at exactly the same time to the Master Section of the main mixer.

      In the picture below, four mixer channels with different Insert FX devices are routed to the Master Section of the main
      mixer. Reason checks which mixer channel has the longest combined inherent latency, by summing the effect de-
      vice’s reported latencies individually for each channel.

          Mix Channel 1                Mix Channel 2                 Mix Channel 3                Mix Channel 4

           To Insert FX                 To Insert FX                  To Insert FX                 To Insert FX

           Effect device                Effect device                 Effect device                Effect device
           with latency 0               with latency 2                with latency 2               with latency 0

           Effect device                Effect device                 Effect device                Effect device
           with latency 4               with latency 10               with latency 8               with latency 3

          From Insert FX               From Insert FX                From Insert FX               From Insert FX
                 =4                           =12                           =10                          =3
                 +8                            +0                           +2                           +9

                    =12                          =12                           =12                          =12

                                                      Master Section

              = Delay Compensation                   +0 = No Delay Compensation

      Delay compensation principle for a number of mixer channels routed to the Master Section of the main mixer.
      Mix Channel 2 has the longest inherent latency in the example above: 2+10=12 samples. The goal now is to add in-
      ternal “invisible delays” to the signals from the other mixer channels so that the total delay for each channel is 12
      samples.
      This means that for Mix Channel 1 Reason automatically adds a compensation delay of 8 samples (to add up to ‘12’).
      Mix Channel 2, which has the longest inherent latency, doesn’t get any delay compensation at all. Mix Channel 3 gets
      a delay compensation of 2 samples (to add up to ‘12’) and Mix Channel 4 gets a a delay compensation of 9 samples
      (to add up to ‘12’).
      Now, the signals from all Mix Channels have a total delay of 12 samples and are thus perfectly “in sync” with each
      other when they reach the Master Section.
      If you add more effect devices to any of the Mix Channels, the inherent latencies might become longer, and the delay
      compensation values are automatically recalculated and adjusted.

      A more “graphical” way of looking at the delay compensation is shown in the picture below. Here the inherent laten-
      cies of the mixer channels and the delay compensation are represented by proportionally sized boxes, which could
      make it easier to understand the principle:

         Mix Channel 1                 Mix Channel 2                 Mix Channel 3                Mix Channel 4
                                        Effect device                Effect device
          Effect device                                                                           Effect device
                                        with latency 2               with latency 2
          with latency 3                                                                          with latency 3

                                                                                                  Effect device
          Effect device
                                                                                                  with latency 3
          with latency 4                                             Effect device
                                        Effect device                with latency 8
                                        with latency 10
                                                                                               Delay
       Delay                                                                                   Compensation +6
       Compensation +5
                                                                  Delay
                                                                  Compensation +2

                    =12                          =12                           =12                          =12

                                                      Master Section

      Delay compensation principle for a number of mixer channels routed to the Master Section of the main mixer.
      As you can see in the picture above Mix Channel 2 doesn’t get any delay compensation, since it has the longest in-
      herent latency of the four channels.

      Manually adjusting the latency values
      There might be situations where you want to manually adjust the latency values. This could be, for example, if effect
      devices should report the wrong latency values and thus cause the audio to sound out of phase or weird in other
      ways.
      On the rear panel of the Audio Track device’s and Mix Channel device’s unfolded Insert FX section are two displays:
      the display to the left shows the total inherent latency for the channel (the sum of the reported inherent latencies of
      the effect devices in the Insert FX signal chain), and the display to the right shows the number of samples you might
      have manually adjusted the latency value:

      !   Note that the Channel Delay figure can never be less than the sum of the reported inherent latencies of the ef-
          fect devices in the Insert FX signal chain.
      !   Note that manually adjusting the latency is only possible if you have connected your effects as an Insert FX
          chain (between the To Device and From Device jacks).
      The sum of the reported inherent latencies (Channel Delay) and any manual adjustment is displayed in the respective
      Insert FX sections on the main mixer channel strips:

      The “Total signal path latency” figure displayed on the Transport panel is the sum of the individual channel which has
      the longest inherent latency, plus the inherent latency of the Master Inserts effect devices:

      q   Hovering over any of the latency figures in the three pictures above brings up a tool tip which displays the la-
          tency in milliseconds.

      Delay Compensation with Busses and Parallel Channels
      When using Parallel Channels and Output Busses the same principles apply, i.e. the total latencies for all mixer chan-
      nels and busses should be the same when the signals reach the Master Section. Also, the latencies of the signals en-
      tering the same Output Bus must also be the same, to avoid phasing problems etc. In the picture below, a number of
      mixer channels, parallel channels and busses are used:

          Mix Channel 1            Mix Channel 2              Mix Channel 3                                        Mix Channel 4

           To Insert FX              To Insert FX                 To Insert FX                                      To Insert FX

          Effect device             Effect device             Effect device                                        Effect device
          with latency 2            with latency 0            with latency 6                                       with latency 4

         From Insert FX            From Insert FX             From Insert FX                                       From Insert FX
                 =2                       =0                         =6                                                   =4

                                          +6                             +0

                                             =6                     =6        Parallel Out        =6
                                                      Bus 1                           Parallel to Bus 1

                                                  Effect device                        Effect device
                                                  with latency 3                       with latency 5

                                                         =9                                    =11
                                                                                             +0                         +7

                                                                                               =11                   =11
                                                                                                           Bus 2

                                                                                                       Effect device
                                                                                                       with latency 2

                                                                                                              =13
                +11                                    +4                                                   +0

                    =13                                     =13                                                =13

                                                             Master Section

             = Delay Compensation                 +0 = No Delay Compensation

      Delay compensation when using Parallel Channels and Busses.
      As you can see in the picture above, the signal chain with the longest inherent combined latency is: Mix Channel 3 >
      Bus 1 > Parallel Bus 1 > Bus 2 > Master Section; this signal chain is therefore not delay-compensated. All other sig-
      nals are delay-compensated where necessary, which is indicated by the orange circles in the picture.

      Delay Compensation to Send FX busses
      Since each mixer channel is delay-compensated individually, we need to make sure that any signals from the mixer
      channels to the Send FX busses reaches the Send FX busses at the same time. To make the signals to each of the
      Send FX busses come “in sync”, there is also a built-in delay compensation to the eight FX sends of each mixer
      channel.

      About Send FX Returns
      Reason doesn't compensate for any inherent delays in the Send Effect devices themselves, as this would make the
      delay compensation scheme extremely complex. Also, Send FX are traditionally often used for delays and reverbs,
      where a little extra inherent delay won't matter much.
      !   In the situation where you might route the outputs of Send Effects back to separate Mix Channels, no delay
          compensation is being performed on the “return” Mix Channels.

      About the Master Insert FX
      Reason considers all audio signals to pass through the Master Section in the main mixer; this is where all signals
      eventually should end up in sync. But the Master Section has an Insert FX section too, and effect devices used here
      can often have a significant inherent latency (maximizers, mastering EQs etc). However, since all signals pass
      through these effect devices in sync, no delay compensation is performed on the Master Insert FX devices. This is
      why the Master Section device in the rack lacks Channel Delay and Adjustment displays.

      Problematic configurations
      The examples below describe a number of “problematic” routings and how Reason handles these regarding delay
      compensation.
      When non-standard routings are detected, the red LED in the Delay Compensation section of the back of the Mix
      Channel/Audio Track device Programmer section lights up. Hovering over the LED brings up a tool tip, which de-
      scribes the detected type of problem;

      Parallel signal paths within the channel
      In these types of configurations Reason uses delay compensation only for the shortest signal path, i.e. the signal path
      that has the shortest inherent latency between the To Device and From Device connections:

                                                                                                                                  Split

                                                                                                                       Effect device
                                                                                                                       with short latency

                                                                                                                                 Effect device
                                                                                                                                 with long latency

                                                                                                                                 Merge

                                                                                                                                   or

                                                                                                                                  Split

                                                                                                                                 Effect device
                                                                                                                                 with short latency

                                                                                                                                 Merge

      Example of a parallel signal configuration where only the delay for the shortest path is used for delay compensation.

      Sub-mixers with Send FX routings within the channel
      In these types of configurations Reason uses delay compensation only for the shortest signal path, i.e. the signal path
      that has the shortest inherent latency between the To Device and From Device connections. If there are send effects
      in the path, this means that the inherent latency will be the same, or longer with these effects. Therefore, send effects
      are always disregarded from any delay compensation:

      Example of an internal “send fx” routing inside an Insert FX configuration.

      Loopback within the channel
      In these types of configurations Reason uses Delay compensation only for the shortest signal path, i.e. the signal
      path that has the shortest inherent latency between the To Device and From Device connections. If there are any
      feedback connections in the signal path, these will be disregarded from any delay compensation:

                                                                                                           Merge

                                                                                                        Effect device
                                                                                                        with latency

                                                                                                                    Effect device in
                                                                                                                    feedback loop

                                                                                                            Split

      Example of a feedback loop, which is disregarded from delay compensation.

      External routing from the channel
      If there are any connections to devices outside the Insert FX section, and these devices are routed to other mix chan-
      nels (or to the Master Section), any inherent latencies in the external effect devices will be disregarded from any de-
      lay compensation:

                                                                                                      External

                                                                                                                     Merge

                                                                                                                 Effect device(s)
                                                                                                                 with latency

                                                                                                                      Split

                                                                                                                              External

      Example of an external routing from (any of) the Insert FX devices.

      Broken signal path in the channel
      If the effects signal path should be broken in the channel, the tool tip “Could not calculate latency. The default value
      of 0 samples was used” is displayed. This means that the program couldn't follow the signal path, which may be be-
      cause it's not completely connected, for example:

      About using the Direct Out connections of the mixer channels
      Since connecting the Direct Outs of a Mix Channel or Audio Track device automatically disconnects it from the Mas-
      ter Section of the main mixer, any delay compensation is also automatically disabled. This is indicated by “ - “ in the
      Channel Delay display:


=== END OF PART ===
