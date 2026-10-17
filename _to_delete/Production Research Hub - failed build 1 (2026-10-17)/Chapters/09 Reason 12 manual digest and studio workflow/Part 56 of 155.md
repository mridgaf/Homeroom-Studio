# Chapter 09: Reason 12 manual digest and studio workflow
## Part 56 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 47 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 57 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 47 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

      Saving edited samples
      D   Click the Save button in the Edit Sample Window to save your edited sample.

          The sample is saved, complete with all the edits you have made in the Edit Sample Window (Start, End, Loop set-
          tings, Name etc.) The sample will appear in the Song Samples location in the Browser, with the new name if this
          has been changed.

      !   If you have opened and edited a ReFill sample, a copy of this sample (including any edits) will be saved with its
          original name in the All Self-contained Samples folder.

      Renaming samples
      1. Type in the desired name of your sample in the Name field in the Edit Sample Window.

      2. Click the Save button to save the sample with the new name.
      !   Note that saving a sample under a different name will simply replace the current name - it will not create a copy
          of the original sample!

      Sample management
      About Assigned and Unassigned samples
      Assigned Samples
      Samples can be assigned to devices that support sample playback, such as the NN-XT, NN19, Redrum and Kong.
      Samples that are assigned to a device can be found in the Assigned Samples folder in the Song Samples location in
      the Browser:

      The Assigned Samples folder can contain various sub folders, one for each sampler device used in the current song.
      The song in the picture above contains two sampler devices; the “NN-XT 1” and the “Redrum 1”. The instrument fold-
      ers can be unfolded to display their current sample contents. Sounds you have sampled yourself as well as samples
      from the Factory Soundbank and from ReFills are displayed with icons.

      Unassigned Samples
      Samples that have been removed from a sampler device and have not (yet) been assigned to another sampler device
      are displayed in the Unassigned Samples folder:

      Unassigned samples can be assigned to any sampler device by simply loading them into a sampler device - see
      “Loading samples into a device”.

      Saving samples in a song
      When you have recorded a sample, by clicking a Sample button on a sampler device, the sample is automatically
      stored in the All Self-contained Samples folder in the Song Samples location in the Browser:

      The samples you have recorded are automatically named “Sample ‘n’” where ‘n’ is a serial number.
      You can rename a sample by selecting it in the All Self-contained Samples folder, clicking the Edit button, then re-
      naming it in the Edit Sample Window and then clicking the Save button.

      As soon as you save your song, all samples you have recorded will be automatically saved as self-contained samples
      in the song document. This way you don’t have to keep track of any “loose” samples on your computer.

      Deleting samples from a song
      It’s only possible to delete samples you have recorded yourself in a Reason song, i.e. samples that are located in the
      All Self-contained Samples folder in the Browser. Samples from the Factory Soundbank and from ReFills cannot be
      deleted because they are contained in ReFills.
      D   To delete a sample in the All Self-contained Samples folder, select it and select “Delete Sample(s)” from the
          context menu.
      !   Since the selected sample also exists, either in the Assigned Samples folder or Unassigned Samples folder, it
          will be deleted from there as well. Similarly, if you select and delete a non-Factory Soundbank/ReFill sample
          from the Assigned Samples folder or Unassigned Samples folder, it will be deleted from the All Self-contained
          Samples folder as well.

      Loading samples into a device
      To load samples into a sampler device (NN-XT, NN19, Redrum, Kong and RV7000 Mk II) proceed as follows:
      1. Click on a Browse Sample button on the device.

        Browse Sample buttons on NN-XT, NN19, Redrum and Kong respectively.
      2. Navigate to the desired location in the Browser.
        In the picture below, we have clicked the Song Samples location and expanded all folders and subfolders:

      3. Select the sample you want to load into your device.
        You can select a sample in any of the folders. If you like to audition a sample, click the Play button below the
        Browser list. To make samples automatically play upon selection, click the Auto button.
      4. Click the Load button (or double click the sample) to load the selected sample into the device.
        When the selected sample has been loaded into the device, the corresponding sample file icon in the Browser has
        been placed under the device’s icon in the Assigned Samples folder. If the loaded sample was originally in the Un-
        assigned Samples folder, it has now been moved from this folder to the Assigned Samples folder:

      Duplicating samples
      If you want to use an existing sample as base for new edits, you can do this by first duplicating the existing sample
      and then performing the edits on the duplicate. It’s even possible to duplicate samples from the Factory Soundbank
      and from any existing ReFills! However, duplicated samples from the Factory Soundbank or from ReFills cannot be
      exported to disk as separate files, but can only be saved as self-contained samples inside the song document.
      To duplicate a sample, proceed as follows:
      1. Select the desired sample in the Song Samples location in the Browser.

      2. Select “Duplicate Sample(s)” from the context menu.
          The duplicated sample appears - with its original name followed by the word “Copy” - in the All Self-contained
          Samples folder. The sample also appears in the Unassigned Samples folder:

          To edit and/or rename the duplicated sample, refer to “Editing samples” and “Renaming samples”.

      Exporting samples
      If you like you can export samples that you have recorded in your song and save them as separate WAV or AIFF files
      to disk. Proceed as follows:
      1. Select desired sample(s) in the Song Samples location in the Browser.
      !   Note that it is not possible to export samples that originate from the Factory Soundbank or from a ReFill.
      2. Select “Export Sample(s)” from the context menu.

      • If your sample(s) are not cropped, or use a Crossfade Loop, the Lossy Sample Export dialog appears:

          The following options are available:
      • Crop selected sample(s) and render loop crossfades
          This item shows up if you have edited the Start and/or End Markers and use a Loop with Crossfades. The sample
          will be cropped at the Start and End Markers and the crossfaded loop will be rendered into the sample.
      !   This will make the sample sound exactly the same when you import it to a sample playback device/application,
          but the sample data has been changed compared to the original.
      • Crop selected sample(s)
          This item shows up instead of the above item if no Loop is used. The sample will be cropped at the Start and End
          Markers.
      • Save raw sample(s)
          The sample will be exported without Start or End Marker position data but with Loop data, if any. If the loop is
          crossfaded, the crossfade will be removed.
      !   This will make the sample sound differently when you import it to a sample playback device/application.
      3. Click Export to proceed.
          The “Export Sample as...” dialog appears;

      4. Choose location for your sample file, type in desired name and choose WAV or AIFF file format.
      5. Click Save to export the sample file to disk.
          The sample is saved to disk using its original resolution (bit depth) and sample rate. The original self-contained
          sample in your song will remain intact.

      About self-contained samples
      All samples you record in a song automatically become self-contained. Self-contained means that the samples are
      automatically stored within the song when you save it. A great advantage with this is that you never have to keep
      track of any “loose” custom samples you use in your song - they are always included in the song document.
      All self-contained samples in a song can be viewed by unfolding the All Self-contained Samples folder in the Song
      Samples location in the Browser:

      Self-contained samples can also be loaded into any sampler device from the Browser. See “Loading samples into a
      device” for more details.

      Un-self-containing samples
      There might be situations where you want to “un-self-contain” your own samples, i.e. export the samples to disk as
      separate files and at the same time remove them from the song document. This can be done by selecting “Song Self-
      Contain Settings...” from the File menu - see “About Self-Contained Songs” for more details.

566   SAMPLING


---

<a id="the-regroove-mixer-22"></a>

=== END OF PART ===
