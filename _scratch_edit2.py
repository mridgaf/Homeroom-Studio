path = "tools/beat_machine.py"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

# 1. h1 -> graffiti font for the masthead
old_h1 = ' h1 { font-family: var(--display); font-weight: 700;\n      font-size: clamp(38px, 6vw, 66px); line-height: .86;\n      letter-spacing: .012em; margin: 0; text-transform: uppercase;\n      color: #fff; }'
new_h1 = ' h1 { font-family: var(--graffiti); font-weight: 700;\n      font-size: clamp(38px, 6vw, 66px); line-height: .86;\n      letter-spacing: .012em; margin: 0; text-transform: uppercase;\n      color: #fff; }'
assert src.count(old_h1) == 1, "h1 rule not found once"
src = src.replace(old_h1, new_h1)

# 2. new CSS block, inserted right before </style>
NEW_CSS = r'''
 /* ---------------------------------------------------------------
    Black + yellow "school bus" pass (mockup M, owner ask 2026-09-29):
    two-column layout, black chalkboard results column, graffiti +
    typewriter type accents, mural crookedness on static chips only.
    ---------------------------------------------------------------- */

 /* typewriter feel on all small/label text across the page */
 small, .hint, .note, label { font-family: var(--mono) !important; }

 .cols { display: grid; grid-template-columns: minmax(0,1fr) 420px; gap: 26px;
         align-items: stretch; }
 @media (max-width: 1000px) { .cols { grid-template-columns: 1fr; } }

 /* the right column is its own little chalkboard: re-theme its vars
    locally so every card/field/track inside just re-skins for free */
 .right {
   --card: #171717; --card2: #171717; --line: #ffffff26; --line2: #ffffff45;
   --text: #f4f1e6; --dim: #f4f1e699; --dimmer: #f4f1e666;
   background: #111; color: #f4f1e6; border-radius: 10px; padding: 20px;
   display: flex; flex-direction: column; min-height: 100%;
   transform: rotate(-1.1deg);
 }
 .right h2.box, .right #go { font-family: var(--graffiti); }

 .logo-spacer { flex: 1; display: flex; align-items: center; justify-content: center;
                min-height: 80px; }
 .logo-mark { width: 80%; max-width: 260px; aspect-ratio: 1;
              background-image: url("/brand?name=logo-black.png");
              background-size: contain; background-repeat: no-repeat;
              background-position: center;
              filter: invert(1) sepia(1) saturate(8) hue-rotate(-20deg) brightness(1.15);
              mix-blend-mode: screen; opacity: .5; pointer-events: none; }

 /* mural/crooked touches — static chips only, never .track or anything
    inside #tracklist (rotation there breaks drag-and-drop hit-testing) */
 .dj:nth-child(3n)   { transform: rotate(-1.6deg); }
 .dj:nth-child(3n+1) { transform: rotate(1.3deg); }
 .dj:nth-child(3n+2) { transform: rotate(-.9deg); }
 .fixedbtn:nth-child(3n)   { transform: rotate(-1.4deg); }
 .fixedbtn:nth-child(3n+1) { transform: rotate(1.1deg); }
 .fixedbtn:nth-child(3n+2) { transform: rotate(-.8deg); }
 .pullup button { transform: rotate(-.8deg); }
 .panel { transform: rotate(.5deg); }

 .bottom { margin: 20px 0 40px; padding: 22px; border: 9px solid transparent;
           border-image: repeating-linear-gradient(45deg, #111 0 16px, #e8d810 16px 32px) 18;
           border-radius: 2px; }
'''

marker = "</style></head><body>"
assert src.count(marker) == 1
src = src.replace(marker, NEW_CSS + marker)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)

print("css pass done, new size:", len(src))
