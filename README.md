# Stereoscopic Layer Shifter (Inkscape Extension)

This Inkscape extension creates **stereoscopic 3D images** by shifting SVG layers left and right relative to a chosen "window layer".  
It can export:
- Left and Right eye views (SVG or PNG)
- A combined side-by-side stereo view

---

## 🧩 Installation

1. Download or clone this repository.
2. Copy the folder `hello_extension` to your Inkscape extensions directory:
   - **Windows:** `%APPDATA%\Inkscape\extensions`
   - **macOS:** `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions/`
   - **Linux:** `~/.config/inkscape/extensions/`
3. Restart Inkscape.

---

## 🧠 Usage

1. Open your layered SVG file in Inkscape.
2. Go to **Extensions → 3D → Stereoscopic Layer Shifter**.
3. Choose:
   - The “window layer” (the reference layer that appears at zero depth)
   - Depth mode (`max`, `moderate`, `conservative`)
   - Export options (SVG / PNG / side-by-side)
4. Choose the path where you want to save your results.
5. Click **Apply**.

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

