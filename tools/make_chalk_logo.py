"""One-off: derive brand/logo-chalk.png from the ORIGINAL brand/logo-white.png.

What changes (design handoff 2026-10-04, "Homeroom Studios"):
  * the words above and below the face are cropped away,
  * the solid black backing becomes transparent (alpha = brightness),
  * a gap is cut in the middle of the mouth's RIGHT edge (a squared C).
The original file is read only and never modified. Needs Pillow + numpy
(not in the app's venv: run it with any Python that has them).
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

BRAND = Path(__file__).resolve().parent.parent / "brand"
CHALK = (242, 241, 234)          # the board's chalk white
TOP, BOTTOM = 190, 975           # face only: words live above / below this
GAP_X, GAP_Y0, GAP_Y1 = 925, 775, 885   # the mouth's right-edge opening

im = np.asarray(Image.open(BRAND / "logo-white.png").convert("L"), dtype=float)
face = im[TOP:BOTTOM].copy()
face[GAP_Y0 - TOP:GAP_Y1 - TOP, GAP_X:] = 0
alpha = np.clip((face - 24) * (255 / (255 - 24)), 0, 255).astype(np.uint8)
ys, xs = np.nonzero(alpha > 8)
pad = 24
box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
       min(xs.max() + pad, alpha.shape[1]), min(ys.max() + pad, alpha.shape[0]))
alpha = alpha[box[1]:box[3], box[0]:box[2]]
out = np.zeros(alpha.shape + (4,), np.uint8)
out[..., :3] = CHALK
out[..., 3] = alpha
dest = BRAND / "logo-chalk.png"
Image.fromarray(out, "RGBA").save(dest)
print("wrote", dest, Image.open(dest).size)
