# 🫥 Invisible Cloak — Python + OpenCV

A beginner-friendly computer vision project inspired by the classic **Invisible Cloak** effect.

The webcam first captures the empty background. During the live video, the program detects **red-colored cloth** using HSV color segmentation and replaces that area with the previously captured background, creating an invisibility effect.

## Features

- Live webcam processing
- Red-cloth detection
- HSV color segmentation
- Morphological image processing
- Background replacement
- Live detection-mask preview
- Background re-capture

## Requirements

- Windows / macOS / Linux
- Python 3.9+
- Webcam
- VS Code (recommended)

## 1. Open the project

Extract the ZIP and open the `invisible_cloak_project` folder in VS Code.

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install libraries

```bash
pip install -r requirements.txt
```

## 4. Run

Windows:

```bash
python main.py
```

macOS/Linux:

```bash
python3 main.py
```

## 5. How to use

When the program starts, stand away from the camera while it captures the background for about 3 seconds.

Then wear/use a **bright red cloth**.

Controls:

- `B` → capture the background again
- `M` → show/hide the detection mask
- `Q` → quit

## Tips for a better result

1. Use a bright red cloth.
2. Avoid other red objects behind you.
3. Keep the camera still after background capture.
4. Use good, even lighting.
5. A plain background works best.
6. If the effect is weak, adjust the HSV thresholds in `create_red_mask()` inside `main.py`.

## Project structure

```text
invisible_cloak_project/
│
├── main.py
├── requirements.txt
└── README.md
```

## Concepts demonstrated

- OpenCV
- NumPy
- HSV color space
- Color masking
- Image thresholding
- Morphological operations
- Gaussian blur
- Bitwise image operations
- Real-time video processing

## Important

This is a computer-vision visual effect, not actual invisibility. The quality depends heavily on lighting, camera stability, background, and the color of the cloth.
