path = "tools/beat_machine.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# lines are 1-indexed in our notes; convert to 0-indexed
start = 5841 - 1
end = 5947 - 1  # inclusive

assert lines[start].startswith('<h2 class="box">The Crew'), lines[start]
assert lines[end].rstrip('\n') == '<div id="pullmsg"></div>', repr(lines[end])

with open("_scratch_new_body.html", "r", encoding="utf-8") as f:
    new_block = f.read()
if not new_block.endswith("\n"):
    new_block += "\n"

new_lines = lines[:start] + [new_block] + lines[end+1:]

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("body restructure done. old line count:", len(lines), "new:", len(new_lines))
