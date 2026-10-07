"""Final reusable handwriting renderer. See README.md for details."""
from PIL import Image, ImageDraw
import numpy as np, pickle, random
import os

HERE = os.path.dirname(os.path.abspath(__file__))
variants = pickle.load(open(os.path.join(HERE, "glyphs_variants.pkl"), "rb"))

var_widths = {}
for ch, vlist in variants.items():
    var_widths[ch] = []
    for v in vlist:
        al = np.array(v["img"])[:, :, 3]
        xs = np.where((al > 40).any(axis=0))[0]
        var_widths[ch].append((xs[0], xs[-1]) if len(xs) else (0, 8))

DOT_DX, DOT_DY = 8.0, -10.0
GAP, SPACE_W = 5, 26
NO_VARY = set(['(', ')'])  # paren pairs must match
X_DROP = 20  # multiplication x lowered

def render(lines, box_lines=(), seed=42):
    """lines: list of strings. box_lines: indices to box. Returns PIL image."""
    random.seed(seed)
    def adv(ch, vi=0):
        k = "deg" if ch == "\u00b0" else ch
        if k not in var_widths:
            return SPACE_W
        x0, x1 = var_widths[k][vi]
        return x1 - x0 + GAP if ch != " " else SPACE_W
    W = int(max(sum(adv(c) for c in ln) for ln in lines)) + 120
    H = len(lines) * 130 + 60
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    Y = 95
    boxes = []
    for li, ln in enumerate(lines):
        x = 50
        top = Y - 95
        for ci, ch in enumerate(ln):
            if ch == " ":
                x += SPACE_W
                continue
            key = "deg" if ch == "\u00b0" else ch
            if key not in variants:
                x += SPACE_W
                continue
            vi = 0 if key in NO_VARY else random.randrange(len(variants[key]))
            v = variants[key][vi]
            x0, x1 = var_widths[key][vi]
            dx, dy = (DOT_DX, DOT_DY) if ch == "." else (0, 0)
            tile = v["img"]
            tc = tile.crop((x0, 0, x1 + 1, tile.size[1]))
            canvas.paste(tc, (int(x + dx), int(round(Y + v["d"] - tile.size[1] + dy))), tc)
            x += (x1 - x0) + GAP
        boxes.append((top, Y + 20, x))
        Y += 130
    draw = ImageDraw.Draw(canvas)
    for bl in box_lines:
        top, bot, right = boxes[bl]
        draw.rectangle([40, top, right + 20, bot], outline=(0, 0, 0), width=3)
    return canvas

if __name__ == "__main__":
    img = render(["M = 90(1.20) = 108 lb in counterclockwise"], box_lines=(0,))
    img.save(os.path.join(HERE, "test_render.png"))
    print("ok")
