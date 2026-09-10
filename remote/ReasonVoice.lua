function remote_init()
    local items={
        {name="Patch Next", input="button"},
        {name="Patch Prev", input="button"},
        {name="Play", input="button"},
        {name="Stop", input="button"},
        {name="Record", input="button"},
        {name="Loop", input="button"},
        {name="Track Prev", input="button"},
        {name="Track Next", input="button"},
        {name="Undo", input="button"},
        {name="Redo", input="button"},
        -- knobs: continuous values, one auto-input line each (no press/release)
        {name="Knob 1", input="value", output="value", min=0, max=127},
        {name="Knob 2", input="value", output="value", min=0, max=127},
        {name="Knob 3", input="value", output="value", min=0, max=127},
        {name="Knob 4", input="value", output="value", min=0, max=127},
        {name="Knob 5", input="value", output="value", min=0, max=127},
        {name="Knob 6", input="value", output="value", min=0, max=127},
        {name="Knob 7", input="value", output="value", min=0, max=127},
        {name="Knob 8", input="value", output="value", min=0, max=127},
    }
    remote.define_items(items)

    -- Item indices are 1-based in definition order. Derive them rather than
    -- hardcoding 11..18, so reordering the items above can't silently break
    -- feedback.
    g_knob_index = {}
    for i, item in ipairs(items) do
        local n = string.match(item.name, "^Knob (%d)$")
        if n then g_knob_index[tonumber(n)] = i end
    end
    g_dirty = {}
    g_text = {}

    local inputs={
        {pattern="b? 14 7f", name="Patch Next", value="1"},
        {pattern="b? 14 00", name="Patch Next", value="0"},
        {pattern="b? 15 7f", name="Patch Prev", value="1"},
        {pattern="b? 15 00", name="Patch Prev", value="0"},
        {pattern="b? 16 7f", name="Play", value="1"},
        {pattern="b? 16 00", name="Play", value="0"},
        {pattern="b? 17 7f", name="Stop", value="1"},
        {pattern="b? 17 00", name="Stop", value="0"},
        {pattern="b? 18 7f", name="Record", value="1"},
        {pattern="b? 18 00", name="Record", value="0"},
        {pattern="b? 19 7f", name="Loop", value="1"},
        {pattern="b? 19 00", name="Loop", value="0"},
        {pattern="b? 1a 7f", name="Track Prev", value="1"},
        {pattern="b? 1a 00", name="Track Prev", value="0"},
        {pattern="b? 1b 7f", name="Track Next", value="1"},
        {pattern="b? 1b 00", name="Track Next", value="0"},
        {pattern="b? 1c 7f", name="Undo", value="1"},
        {pattern="b? 1c 00", name="Undo", value="0"},
        {pattern="b? 1d 7f", name="Redo", value="1"},
        {pattern="b? 1d 00", name="Redo", value="0"},
        {pattern="b? 1e xx", name="Knob 1"},
        {pattern="b? 1f xx", name="Knob 2"},
        {pattern="b? 20 xx", name="Knob 3"},
        {pattern="b? 21 xx", name="Knob 4"},
        {pattern="b? 22 xx", name="Knob 5"},
        {pattern="b? 23 xx", name="Knob 6"},
        {pattern="b? 24 xx", name="Knob 7"},
        {pattern="b? 25 xx", name="Knob 8"},
    }
    remote.define_auto_inputs(inputs)
end

-- ---------------------------------------------------------------------------
-- Feedback: Reason -> us. Lets the app know where a knob actually sits (so
-- "turn it down 5%" has something to count down from) and what Reason DISPLAYS
-- for it ("-20.0 dB"), which is the only trustworthy source for real units --
-- the CC-to-dB curve is not linear and is not documented.
--
-- Two messages per change, both on the surface's MIDI OUT:
--   CC 60-67  = knob 1-8 raw position, 0-127
--   SysEx     = f0 7d <knob 1-8> <ascii "Param=display value"> f7
-- 7d is the MIDI-registered non-commercial manufacturer ID.
-- ---------------------------------------------------------------------------

function remote_set_state(changed_items)
    for _, idx in ipairs(changed_items) do
        for k = 1, 8 do
            if g_knob_index[k] == idx then
                local st = remote.get_item_state(idx)
                g_text[k] = (st.remote_item_name or "") .. "=" .. (st.text_value or "")
                g_dirty[k] = true
            end
        end
    end
end

local function ascii_hex(str)
    -- SysEx bodies must be 7-bit; drop anything that isn't printable ASCII.
    local out = ""
    for i = 1, string.len(str) do
        local b = string.byte(str, i)
        if b >= 32 and b <= 126 then
            out = out .. string.format(" %02x", b)
        end
    end
    return out
end

function remote_deliver_midi()
    local events = {}
    for k = 1, 8 do
        if g_dirty[k] then
            g_dirty[k] = false
            local idx = g_knob_index[k]
            local value = remote.get_item_value(idx) or 0
            -- CC 60 is 0x3c, so knob k -> 0x3b + k
            table.insert(events, remote.make_midi(
                string.format("b0 %02x %02x", 0x3b + k, value)))
            local text = string.sub(g_text[k] or "", 1, 28)
            if text ~= "" then
                table.insert(events, remote.make_midi(
                    "f0 7d " .. string.format("%02x", k) .. ascii_hex(text) .. " f7"))
            end
        end
    end
    return events
end
