# Stereoscopic Layer Shifter (Inkscape Extension)

This Inkscape extension creates **stereoscopic 3D images** by shifting SVG layers left and right relative to a chosen "window layer".  
It can export:
- Left and Right eye views (SVG or PNG)
- A combined side-by-side stereo view

---

## 🛠 How It Works

- Layers *in front of* the window layer shift **right** (for left view) and **left** (for right view).  
- Layers *behind* the window layer shift in the opposite direction.
- The shifts are proportional to depth:
  - `max` = strongest separation
  - `moderate` = medium separation
  - `conservative` = subtle depth
- Uses `inkex.Transform()` for accurate coordinate translation.

---

## 📤 Output

- `left_view.svg` / `left_view.png`
- `right_view.svg` / `right_view.png`
- `stereo_side_by_side_layers.svg` / `stereo_side_by_side_layers.png`

