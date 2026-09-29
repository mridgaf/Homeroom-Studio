import re, sys

path = "tools/beat_machine.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

orig_len = len(src)

# ---------- 1. :root block ----------
old_root = """ :root {
   --paper:   #f4ecc4;
   --card:    #fffef4;
   --card2:   #ffffff;
   --line:    #1020a826;
   --line2:   #1020a845;
   --text:    #12157f;
   --dim:     #12157f99;
   --dimmer:  #12157f66;
   /* straight off the Back of the Class mark: the yellow scrawl and the
      blue square it sits on — verbatim, "keep the blue and yellow no
      matter what" (owner, 2026-08-06). --co/--ch used to be lifted
      tints for a dark background; on paper the ink blue reads fine on
      its own, so both now just alias --blue.                         */
   --hi:      #e8d810;   /* band yellow — actions, keeps, selection    */
   --hi-ink:  #16150a;
   --blue:    #1020a8;   /* band blue — masthead, fills, blocks, ink   */
   --co:      #1020a8;
   --no:      #ff4d4d;   /* trash + real errors only                   */
   --ch:      #1020a8;
   --display: "Anton", Impact, "Haettenschweiler", sans-serif;
   --mono:    "Space Mono", ui-monospace, "SF Mono", Menlo, monospace;
 }"""

new_root = """ :root {
   --paper:   #f4ecc4;
   --card:    #fffef4;
   --card2:   #ffffff;
   --line:    #00000026;
   --line2:   #00000045;
   --text:    #171717;
   --dim:     #17171799;
   --dimmer:  #17171766;
   /* owner ask 2026-09-29: swap the blue ink for black + yellow-family
      accents. --hi (band yellow) and --no (red, trash/errors) are
      unchanged on purpose — --hi was already the action/selection
      color, and --no is a functional safety color, not decoration. */
   --hi:      #e8d810;   /* unchanged: band yellow — actions, keeps, selection */
   --hi-ink:  #16150a;
   --blue:    #8a6d00;   /* was band blue; dark mustard now — black+yellow palette (owner ask 2026-09-29) */
   --co:      #b8860b;   /* legend picks — goldenrod: keeps a visually distinct 3rd shade from crew's --hi and genre's --ch */
   --no:      #ff4d4d;   /* trash + real errors only — kept red on purpose, it's a safety signal not decoration */
   --ch:      #8a6d00;   /* genre picks — dark mustard; dashed border still sets it apart from legend's solid goldenrod border */
   --display: "Anton", Impact, "Haettenschweiler", sans-serif;
   --mono:    "Space Mono", ui-monospace, "SF Mono", Menlo, monospace;
   --graffiti: "Blackboard Graffiti", "Marker Felt", "Chalkboard SE", var(--display);
 }"""

assert src.count(old_root) == 1, f"root block match count: {src.count(old_root)}"
src = src.replace(old_root, new_root)

# ---------- 2. @font-face, inserted right after the :root block ----------
with open("/tmp/graffiti_b64.txt", "r", encoding="utf-8") as f:
    b64 = f.read().strip()

fontface = """
 @font-face {
   font-family: "Blackboard Graffiti";
   src: url("data:font/woff2;base64,%s") format("woff2");
   font-display: swap;
 }""" % b64

marker = new_root
assert src.count(marker) == 1
src = src.replace(marker, marker + fontface)

# ---------- 3. remaining #1020a8 literals -> black, with 2 exceptions ----------
PULLUP_OLD = "border: 1px solid var(--co); border-radius: 9px; background: #1020a81a;"
PULLUP_NEW = "border: 1px solid var(--co); border-radius: 9px; background: #b8860b1f;"
assert src.count(PULLUP_OLD) == 1
src = src.replace(PULLUP_OLD, PULLUP_NEW)

SVG_OLD = "stroke='%231020a8'"
SVG_NEW = "stroke='%23171717'"
assert src.count(SVG_OLD) == 1
src = src.replace(SVG_OLD, SVG_NEW)

def repl(m):
    return "#000000" + m.group(1)

before_count = len(re.findall(r"#1020a8([0-9a-fA-F]{2})", src))
src = re.sub(r"#1020a8([0-9a-fA-F]{2})", repl, src)
after_remaining = len(re.findall(r"#1020a8", src))
print("hex-with-alpha replaced:", before_count, "remaining #1020a8 occurrences:", after_remaining)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("done. size before/after:", orig_len, len(src))
