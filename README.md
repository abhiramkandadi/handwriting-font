# Personal Handwriting Font — Reusable Project

Built 2026-10-02 from the user's own handwriting samples. Renders text in his
handwriting style as PNG/PDF.

## Quick Start

```python
from PIL import Image, ImageDraw
import numpy as np, pickle, random

variants = pickle.load(open("glyphs_variants.pkl", "rb"))
# variants[char] = list of {"img": PIL RGBA, "d": baseline offset}
# Pick a random variant per character occurrence for natural variation.
# EXCEPTION: "(" and ")" always use variant 0 so paren pairs match.
```

See `render_final.py` for the complete working renderer.

## Key Files

| File | Purpose |
|------|---------|
| `glyphs_variants.pkl` | **Primary asset.** 70 glyphs, 60 with 2 natural variants each (130 images). Each variant: `{"img": RGBA tile, "d": baseline offset}`. Baselines normalized. |
| `glyphs_full.pkl` | Single-variant version (same normalized baselines). Fallback. |
| `glyphs_full_backup.pkl` | Pre-normalization backup. Source of variant #2. |
| `render_final.py` | Complete renderer: variants + locked parens + boxes. |
| `all_problems_onepage.pdf` | Example output: 7 statics problems, one page. |

## Source Samples

1. `workspace/user/media_library/image/16/160c0e49...jpg` — original photo (alphabet + problem text)
2. `workspace/user/media_library/image/bd/bd5205a1...jpg` — digital alphabet (clean a-z)
3. `workspace/user/media_library/image/3f/3f4582cd...jpg` — digits/symbols (0-9, etc.)
4. `workspace/user/media_library/image/7f/7f1e126d...png` — relabeled paren sheet (a-z + parens)

## Style Rules (user preferences)

- Compact: tight letter spacing (`gap=5`), small overall size
- Simple: no over-explaining, no over-labeling
- Dots (`.`, `i`/`j` dots) shifted up and right: `DOT_DX=8, DOT_DY=-10`
- Multiplication `x` lowered toward mid-height (+20px)
- Space after `1.` in numbered lists (+18px)
- Space before `(` after numbers, e.g. `90 (1.20)` (+14px)
- Final answers boxed (3px black rectangle)
- No degree symbols after numbers in parens (user removed)
- No hyphens in units: `lb in` not `lb-in`, `N m` not `N-m`
- Minus `-` at mid-line (d=-26), NOT at baseline (looks like underscore)
- `|` absolute-value bars: thin vertical, not thick slanted
- Parens: `(` from relabeled sheet; `)` = horizontal mirror of `(`. Always paired (same variant).
- Baselines: all glyph ink bottoms at 0, except descenders (g,p,q,y,j) at +12, `deg` (°) at -35, parens/bars at +5
- Character variation: random variant per occurrence, EXCEPT parens locked to variant 0

## Glyph Coverage

a-z, A-Z, 0-9, `( ) - . = |`, `deg` (°). Missing: `α` (use `a`), `x̄` (use `x`),
`+` (write "plus"), subscripts (write inline, e.g. `MB`, `xA`).

## Replicating

1. Load `glyphs_variants.pkl`
2. For each char in text: pick `random.randrange(len(variants[ch]))`, except `(` `)` → always 0
3. Paste tile at `y = baseline_y + d - tile.height` (+ dot/paren tweaks)
4. Advance x by ink width + gap (5); spaces = 26px
5. Box answer lines with `ImageDraw.rectangle`

## Notes

- This is a DEMO/FONT project. Do not use to fabricate handwritten coursework submissions.
- User's handwriting samples are the source; new characters need new samples.

## Project Structure

```
handwriting-demo/
├── README.md               # This file
├── requirements.txt        # Pillow, numpy
├── .gitignore
├── render_final.py         # Reusable renderer — start here
├── glyphs_variants.pkl     # Font data (70 glyphs, 130 variants)
├── glyphs_full.pkl         # Single-variant fallback
├── glyphs_full_backup.pkl  # Pre-normalization backup
├── sources/                # Original handwriting samples
│   ├── 01_original_photo.jpg
│   ├── 02_digital_alphabet.jpg
│   ├── 03_digits_symbols.jpg
│   └── 04_paren_sheet.png
└── all_problems_onepage.pdf  # Example output
```

## Git Setup

```bash
cd handwriting-demo
git init
git add .
git commit -m "Personal handwriting font v1"
git remote add origin <your-repo-url>
git push -u origin main
```
