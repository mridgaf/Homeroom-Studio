-- ReasonVoice control surface codec.
--
-- 10 momentary buttons (transport / patch / undo) plus NUM_KNOBS continuous
-- knobs, and one text item that reports WHICH device the surface is locked to.
-- Knob N moves a different parameter on every device -- see the Scope blocks
-- in ReasonVoice.remotemap.

NUM_KNOBS = 48

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
        -- Which device are we locked to? Mapped to "Device Name" in every
        -- Scope block, exactly as Reason's own factory maps do it
        -- (Novation/Launchkey MK3: `Map LCD <tab><tab> Device Name`).
        -- Without this the app cannot tell a Scream from a compressor and
        -- would read a knob's value out of the wrong calibration table.
        {name="Device", output="text"},
        -- knobs: continuous values, one auto-input line each (no press/release).
        -- Written out rather than generated: tests/test_remote_bridge.py reads
        -- this file as TEXT, so a loop here would blank its guards.
        {name="Knob 1", input="value", output="value", min=0, max=127},
        {name="Knob 2", input="value", output="value", min=0, max=127},
        {name="Knob 3", input="value", output="value", min=0, max=127},
        {name="Knob 4", input="value", output="value", min=0, max=127},
        {name="Knob 5", input="value", output="value", min=0, max=127},
        {name="Knob 6", input="value", output="value", min=0, max=127},
        {name="Knob 7", input="value", output="value", min=0, max=127},
        {name="Knob 8", input="value", output="value", min=0, max=127},
        {name="Knob 9", input="value", output="value", min=0, max=127},
        {name="Knob 10", input="value", output="value", min=0, max=127},
        {name="Knob 11", input="value", output="value", min=0, max=127},
        {name="Knob 12", input="value", output="value", min=0, max=127},
        {name="Knob 13", input="value", output="value", min=0, max=127},
        {name="Knob 14", input="value", output="value", min=0, max=127},
        {name="Knob 15", input="value", output="value", min=0, max=127},
        {name="Knob 16", input="value", output="value", min=0, max=127},
        {name="Knob 17", input="value", output="value", min=0, max=127},
        {name="Knob 18", input="value", output="value", min=0, max=127},
        {name="Knob 19", input="value", output="value", min=0, max=127},
        {name="Knob 20", input="value", output="value", min=0, max=127},
        {name="Knob 21", input="value", output="value", min=0, max=127},
        {name="Knob 22", input="value", output="value", min=0, max=127},
        {name="Knob 23", input="value", output="value", min=0, max=127},
        {name="Knob 24", input="value", output="value", min=0, max=127},
        {name="Knob 25", input="value", output="value", min=0, max=127},
        {name="Knob 26", input="value", output="value", min=0, max=127},
        {name="Knob 27", input="value", output="value", min=0, max=127},
        {name="Knob 28", input="value", output="value", min=0, max=127},
        {name="Knob 29", input="value", output="value", min=0, max=127},
        {name="Knob 30", input="value", output="value", min=0, max=127},
        {name="Knob 31", input="value", output="value", min=0, max=127},
        {name="Knob 32", input="value", output="value", min=0, max=127},
        {name="Knob 33", input="value", output="value", min=0, max=127},
        {name="Knob 34", input="value", output="value", min=0, max=127},
        {name="Knob 35", input="value", output="value", min=0, max=127},
        {name="Knob 36", input="value", output="value", min=0, max=127},
        {name="Knob 37", input="value", output="value", min=0, max=127},
        {name="Knob 38", input="value", output="value", min=0, max=127},
        {name="Knob 39", input="value", output="value", min=0, max=127},
        {name="Knob 40", input="value", output="value", min=0, max=127},
        {name="Knob 41", input="value", output="value", min=0, max=127},
        {name="Knob 42", input="value", output="value", min=0, max=127},
        {name="Knob 43", input="value", output="value", min=0, max=127},
        {name="Knob 44", input="value", output="value", min=0, max=127},
        {name="Knob 45", input="value", output="value", min=0, max=127},
        {name="Knob 46", input="value", output="value", min=0, max=127},
        {name="Knob 47", input="value", output="value", min=0, max=127},
        {name="Knob 48", input="value", output="value", min=0, max=127},
    }
    remote.define_items(items)

    -- Item indices are 1-based in definition order. Derive them rather than
    -- hardcoding, so reordering the items above can't silently break feedback.
    -- NOTE the `+` in the pattern: with a bare `%d` this matched Knob 1-9 and
    -- silently dropped Knob 10 upward.
    g_knob_index = {}
    g_device_index = nil
    for i, item in ipairs(items) do
        local n = string.match(item.name, "^Knob (%d+)$")
        if n then g_knob_index[tonumber(n)] = i end
        if item.name == "Device" then g_device_index = i end
    end
    g_dirty = {}
    g_text = {}
    g_device_dirty = false
    g_device_text = ""

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
        -- Knob k arrives on CC 29 + k; CC 30 is 0x1e. Knobs 1-16 keep the
        -- exact CCs they have always had. The FEEDBACK range moved (60-75 ->
        -- 78-125) to make room for knobs 17-48 going out on 46-77 -- the two
        -- directions share one IAC bus, so they must never overlap or the app
        -- reads its own echo as Reason's answer.
        {pattern="b? 1e xx", name="Knob 1"},
        {pattern="b? 1f xx", name="Knob 2"},
        {pattern="b? 20 xx", name="Knob 3"},
        {pattern="b? 21 xx", name="Knob 4"},
        {pattern="b? 22 xx", name="Knob 5"},
        {pattern="b? 23 xx", name="Knob 6"},
        {pattern="b? 24 xx", name="Knob 7"},
        {pattern="b? 25 xx", name="Knob 8"},
        {pattern="b? 26 xx", name="Knob 9"},
        {pattern="b? 27 xx", name="Knob 10"},
        {pattern="b? 28 xx", name="Knob 11"},
        {pattern="b? 29 xx", name="Knob 12"},
        {pattern="b? 2a xx", name="Knob 13"},
        {pattern="b? 2b xx", name="Knob 14"},
        {pattern="b? 2c xx", name="Knob 15"},
        {pattern="b? 2d xx", name="Knob 16"},
        {pattern="b? 2e xx", name="Knob 17"},
        {pattern="b? 2f xx", name="Knob 18"},
        {pattern="b? 30 xx", name="Knob 19"},
        {pattern="b? 31 xx", name="Knob 20"},
        {pattern="b? 32 xx", name="Knob 21"},
        {pattern="b? 33 xx", name="Knob 22"},
        {pattern="b? 34 xx", name="Knob 23"},
        {pattern="b? 35 xx", name="Knob 24"},
        {pattern="b? 36 xx", name="Knob 25"},
        {pattern="b? 37 xx", name="Knob 26"},
        {pattern="b? 38 xx", name="Knob 27"},
        {pattern="b? 39 xx", name="Knob 28"},
        {pattern="b? 3a xx", name="Knob 29"},
        {pattern="b? 3b xx", name="Knob 30"},
        {pattern="b? 3c xx", name="Knob 31"},
        {pattern="b? 3d xx", name="Knob 32"},
        {pattern="b? 3e xx", name="Knob 33"},
        {pattern="b? 3f xx", name="Knob 34"},
        {pattern="b? 40 xx", name="Knob 35"},
        {pattern="b? 41 xx", name="Knob 36"},
        {pattern="b? 42 xx", name="Knob 37"},
        {pattern="b? 43 xx", name="Knob 38"},
        {pattern="b? 44 xx", name="Knob 39"},
        {pattern="b? 45 xx", name="Knob 40"},
        {pattern="b? 46 xx", name="Knob 41"},
        {pattern="b? 47 xx", name="Knob 42"},
        {pattern="b? 48 xx", name="Knob 43"},
        {pattern="b? 49 xx", name="Knob 44"},
        {pattern="b? 4a xx", name="Knob 45"},
        {pattern="b? 4b xx", name="Knob 46"},
        {pattern="b? 4c xx", name="Knob 47"},
        {pattern="b? 4d xx", name="Knob 48"},
    }
    remote.define_auto_inputs(inputs)
end

-- ---------------------------------------------------------------------------
-- Feedback: Reason -> us. Lets the app know where a knob actually sits (so
-- "turn it down 5%" has something to count down from) and what Reason DISPLAYS
-- for it ("-20.0 dB", "Tape", "C"), which is the only trustworthy source for
-- real units -- the CC-to-dB curve is not linear and is not documented.
--
-- Messages, all on the surface's MIDI OUT:
--   CC 78-125 = knob 1-48 raw position, 0-127
--   SysEx     = f0 7d <slot> <ascii "Param=display value"> f7
--               slot 1-48 = that knob; slot 0 = the locked device's name
-- 7d is the MIDI-registered non-commercial manufacturer ID.
-- ---------------------------------------------------------------------------

function remote_set_state(changed_items)
    for _, idx in ipairs(changed_items) do
        if idx == g_device_index then
            local st = remote.get_item_state(idx)
            g_device_text = (st.remote_item_name or "Device Name")
                .. "=" .. (st.text_value or "")
            g_device_dirty = true
        end
        for k = 1, NUM_KNOBS do
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

-- 40, not 28: "Device Name=Scream 4 Distortion" is 31 characters and a
-- truncated device name would be matched against the wrong calibration table.
local TEXT_MAX = 40

function remote_deliver_midi()
    local events = {}
    if g_device_dirty then
        g_device_dirty = false
        local text = string.sub(g_device_text or "", 1, TEXT_MAX)
        if text ~= "" then
            table.insert(events, remote.make_midi(
                "f0 7d 00" .. ascii_hex(text) .. " f7"))
        end
    end
    for k = 1, NUM_KNOBS do
        if g_dirty[k] then
            g_dirty[k] = false
            local idx = g_knob_index[k]
            local value = remote.get_item_value(idx) or 0
            -- CC 78 is 0x4e, so knob k -> 0x4d + k
            table.insert(events, remote.make_midi(
                string.format("b0 %02x %02x", 0x4d + k, value)))
            local text = string.sub(g_text[k] or "", 1, TEXT_MAX)
            if text ~= "" then
                table.insert(events, remote.make_midi(
                    "f0 7d " .. string.format("%02x", k) .. ascii_hex(text) .. " f7"))
            end
        end
    end
    return events
end
