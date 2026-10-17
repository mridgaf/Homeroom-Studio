# REAPER Song Builder

Double-click **Start Song Builder.command**. A local page opens in your browser. Drop a Homeroom Song Sketch ZIP, edit or randomize the sections, and click **Create in REAPER**. The project and every WAV it needs are saved together in `~/Desktop/REAPER Song Builder Songs/`. Each build gets a new folder; existing projects are never replaced.

New Song Sketch ZIPs contain `source_stems/` and allow clean 2-, 4-, or 8-bar arrangements. Older ZIPs still work: the helper cuts their four rendered sections into reusable variations, although those sections already contain baked levels and effects. The page offers editable section order, length, variation, scene, drum breath, and fades. New ZIPs receive track volume envelopes for scenes and moves.

The helper opens the finished project in REAPER when REAPER is closed. If REAPER is already running, it leaves that session alone and shows the new project path. The helper does not touch the Homeroom beat library or an existing REAPER project.

Run the included checks with `/usr/bin/python3 -m unittest test_builder.py` from this folder. No packages need to be installed for the helper.
