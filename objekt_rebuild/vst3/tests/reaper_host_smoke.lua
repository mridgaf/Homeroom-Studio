local project_path = "/Users/johnsuhr/Desktop/Homeroom Studio/objekt_rebuild/vst3/build/Objekt-Rebuild-Host-Smoke.rpp"
local result_path = "/Users/johnsuhr/Desktop/Homeroom Studio/objekt_rebuild/vst3/build/reaper-host-smoke.txt"

while reaper.CountTracks(0) > 0 do
  reaper.DeleteTrack(reaper.GetTrack(0, 0))
end

reaper.InsertTrackAtIndex(0, true)
local track = reaper.GetTrack(0, 0)
reaper.GetSetMediaTrackInfo_String(track, "P_NAME", "Objekt Rebuild Host Smoke", true)
local fx = reaper.TrackFX_AddByName(track, "VST3i: Objekt Rebuild (Homeroom Studio)", false, -1)
if fx < 0 then
  local f = io.open(result_path, "w")
  f:write("FAILED: plugin not found\n")
  f:close()
  error("Objekt Rebuild VST3 was not found by REAPER")
end

local item = reaper.CreateNewMIDIItemInProj(track, 0.0, 3.0, false)
local take = reaper.GetActiveTake(item)
local start_ppq = reaper.MIDI_GetPPQPosFromProjTime(take, 0.10)
local end_ppq = reaper.MIDI_GetPPQPosFromProjTime(take, 1.30)
reaper.MIDI_InsertNote(take, false, false, start_ppq, end_ppq, 0, 60, 110, false)
reaper.MIDI_Sort(take)
reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 0, true)
reaper.GetSetProjectInfo(0, "RENDER_STARTPOS", 0.0, true)
reaper.GetSetProjectInfo(0, "RENDER_ENDPOS", 3.0, true)
reaper.Main_SaveProjectEx(0, project_path, 0)

local f = io.open(result_path, "w")
f:write("OK fx_index=" .. tostring(fx) .. " project=" .. project_path .. "\n")
f:close()
