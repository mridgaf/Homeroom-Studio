# Chapter 09: Reason 12 manual digest and studio workflow
## Part 52 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 43 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 53 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 43 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Example of when the Direct Outs are used in a channel.

      About the Metronome Click
      Reason adds the Metronome Click (if selected) at the Hardware Interface (after the Master Section). This means that
      if there's a delay in the signal path, the Metronome would be heard before the rest of the audio on playback. There-
      fore, Reason uses delay compensation also for the Metronome so it always plays back correctly in sync.

      Recording with Delay Compensation
      When you record audio using External Monitoring (Preferences - the Audio tab), Reason repositions the audio ac-
      cording to the reported audio card latency. Recorded audio is positioned earlier on the track, by Input Latency + Out-
      put Latency. When delay compensation is active, the total delay time is then added to the audio repositioning.

      Playing and monitoring with Delay Compensation
      A problem with delay-based delay compensation is that all signal paths are delayed equally. Even if you have no Insert
      FXs in the signal path for your track, it might be delay-compensated (depending on what’s in the rest of the channels
      in the mixer). This could make it hard to play instrument devices and monitor through Reason. Some good advice
      could be to:
      q   Record and monitor through Reason with delay compensation Off, and then switch it on after recording.
      q   You could also bypass the Insert FX on the channels with highest latency when recording. Also remember to
          bypass Master Insert FX when recording or playing.

      About bouncing mixer channels
      Delay compensation is taken into account when you bounce mixer channels - both to files on disk and to new tracks
      in the song - as well as when you use the “Bounce in Place” function.


---

<a id="song-file-handling-19"></a>

=== END OF PART ===
