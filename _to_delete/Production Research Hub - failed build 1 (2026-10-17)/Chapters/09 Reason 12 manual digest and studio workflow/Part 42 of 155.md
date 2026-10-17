# Chapter 09: Reason 12 manual digest and studio workflow
## Part 42 of 155

_Digested Reason 12.7 manual, the manual reference, study guide, demo-song teardowns, and studio notes._

**In this part:**
- Reason_12.7_Operation_Manual_Full_Text.md (piece 33 of 131) — Reason 12.7 Operation Manual — Full Text (searchable)

(Next: Part 43 of 155)


=====================================================
SOURCE FILE: Reason_12.7_Operation_Manual_Full_Text.md (piece 33 of 131)
ORIGINAL LOCATION: HS:docs/reason/Reason_12.7_Operation_Manual_Full_Text.md
=====================================================

          The Manage Plugins window.
      Here, all VST plugins installed in your VST folder(s) on your computer are listed (see “Defining custom VST folders”).
      The Manage Plugins window is divided into the following columns:
      • Manufacturer
          Shows the name of the plugin manufacturer.
      • Plugin Name
          Shows the name of the plugin.
      • Auto-scale (Windows only)
          Here you can choose whether Reason or Windows should scale the VST panel. See “Auto-scale (Windows only)”
          below for more details.
      • Plugin Type
          Shows whether the plugin is a VST2 or VST3.
      • Device Type
          Shows whether the plugin is defined as an “Instrument”, “Effect” or “Utility” in Reason.
      • Status
          Shows the current status of the plugin (see “Plugin Status” below).
      In the Plugin Management windows you can also:
      D   Click and drag the column headings to sort the list.
      D   Click a plugin to select it.
          Additional info (path to the dll and comments about its status) is then shown in the Details area.
      D   Click the Disable/Enable button to disable or enable the selected plugin (see “Plugin Status” below).

      Auto-scale (Windows only)
      Some VST panels might show up quite small in Reason 12 standalone on Windows computers. This is most likely be-
      cause they are scaled by Reason's hi-res graphics instead of Windows. In Reason 12.2.4 and later there is a function
      for scaling up these VST panels.
      In this example we have created a VST in the Rack and clicked to open the VST Plugin window:

      As you can see the VST panel is small and a little hard to edit.
      1. Select "Manage Plugins" on the Windows menu in Reason.
      2. Select the VST in the list and tick the "Auto-scale (follow Windows display scaling)" check box:

      3. Close the Manage Plugins window and re-load the VST (e.g. by dragging and dropping the VST from the
         browser and replacing the current instance in the Rack):

      4. Click the VST Rack device to open the VST Plugin window:

        Now the VST panel is larger and a lot easier to view and edit.

      Plugin Status
      A plugin can have four different Status values, with additional texts in the Details area.

      Plugin Status: Enabled
      • If the plugin was enabled in a previous session, the plugin is enabled and ready for use.
      • If the plugin has been enabled during this session, it will be loaded when you restart Reason.

      Plugin Status: Disabled
      • If the plugin was manually disabled in a previous session, it’s now disabled.
      • If the plugin has been manually disabled during this session, it will be disabled when you restart Reason.

      Plugin Status: Could not load
      • If the plugin has the “Could not load” status, the plugin returned an error code and couldn’t be loaded.
          If you enable it, Reason will attempt to load it the next time you restart.

      Plugin Status: Crashed
      • If the plugin has the “Crashed” status, it was automatically disabled because it crashed or caused Reason to
        hang.
          If you enable it, Reason will attempt to load it the next time you restart.

      Defining custom VST folders
      It’s possible to specify custom VST folders. This can be done on the Folders tab in Preferences:

      D   Tick the check boxes for the folders you want Reason to scan for VST plugins at launch.
          You will have to restart Reason for the changes to take effect.
      D   Click the Add button to add a custom VST Plugin folder.
          Note that you will have to create the folder in the computer’s file system before you can add it - you cannot create
          a new folder using the Add function.
          You will then have to restart Reason for the changes to take effect.
      D   Click the Remove button to remove a custom VST Plugin folder.
          Note that you don’t delete the folder from the file system of your computer - you only make it unavailable in the list.
          You then have to restart Reason for the changes to take effect.


---

<a id="sounds-patches-and-the-browser-15"></a>

=== END OF PART ===
