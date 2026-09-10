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
    }
    remote.define_items(items)

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
    }
    remote.define_auto_inputs(inputs)
end
