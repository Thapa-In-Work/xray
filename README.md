
Conversation with Gemini
make me a clean read.me for his # X-Ray Hand Vision



Real-time webcam application that overlays a glowing neon skeleton on your hand, creating an X-ray vision effect. Built for social media content and fun.



## Demo



Hold your hand up to the camera and watch a neon bone structure appear, complete with a soft glow halo and a darkened background that sells the "X-ray in the dark" look.



## Requirements



- Python 3.9 -- 3.12

- Webcam



### Python packages



```

opencv-python>=4.8.0

mediapipe>=1.0.0

numpy>=1.24.0

```



### MediaPipe model



The hand landmark model must be placed at `models/hand_landmarker.task` relative to the script.



Download it automatically with:



```powershell

Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task" -OutFile "models\hand_landmarker.task"

```



Or let the script check and print the download URL on launch.



## Quick start



```powershell

pip install -r requirements.txt

python xray_hand.py

```



## Controls



| Key | Action |

|---|---|

| `1` -- `6` | Cycle glow color: cyan, green, magenta, orange, white, red |

| `B` | Toggle background darkening |

| `S` | Save a screenshot to `screenshots/` |

| `Space` | Toggle bone-pulse animation |

| `+` / `-` | Increase / decrease glow intensity |

| `Q` / `Esc` | Quit |



## How it works



1. **Capture** -- OpenCV reads frames from the default webcam and flips them for a mirror view.

2. **Detection** -- Each frame is passed to MediaPipe's `HandLandmarker` (Tasks API), which returns normalized (x, y) coordinates for 21 landmarks per hand (up to 2 hands).

3. **Skeleton drawing** -- Landmarks are converted to pixel coordinates and connected into bones using MediaPipe's predefined `HAND_CONNECTIONS` graph. Joint circles are drawn at each landmark, with larger circles at the fingertips.

4. **Glow generation** -- The skeleton is drawn onto a black layer. Two Gaussian blur passes at different sigma values (8 and 25) are blended together to produce a soft halo. The sharp skeleton is re-drawn on top for a crisp neon core.

5. **Compositing** -- The glow layer is additively blended onto the original camera frame using `cv2.add`.

6. **Background darkening** -- A convex hull mask is built from the hand landmarks, dilated, and used to darken everything outside the hand region. The glow is re-applied on top so it stays bright.

7. **HUD** -- FPS, current color, glow strength, and pulse status are displayed in the top-left corner.



## Features



- **Multi-hand support** -- Detects up to 2 hands simultaneously, each rendered in a different color.

- **Bone-pulse animation** -- Skeleton brightness pulses in a sine wave; pulse speed is proportional to how fast you move your hand.

- **6 glow colors** -- Switchable at runtime.

- **Adjustable glow intensity** -- Scale from subtle (0.4) to blown-out (4.0).

- **Screenshot export** -- Saves PNGs with timestamps into `screenshots/`.



## Project structure



```

xray/

  models/

    hand_landmarker.task   # MediaPipe hand model (~7.8 MB)

  screenshots/             # Auto-created, saved PNGs go here

  requirements.txt

  xray_hand.py             # Single-file application

  README.md

```



## Configuration



All tunables live at the top of `xray_hand.py`:



- `GLOW_COLORS` -- dict of name to BGR tuples.

- Blur sigmas in `make_glow_layer()` -- `sigma1` (sharp core) and `sigma2` (wide halo).

- `darken_background()` fade factor -- controls how dark the background gets.

- `HandLandmarkerOptions` -- detection/presence/tracking confidence thresholds and `num_hands`.



## Troubleshooting



| Problem | Fix |

|---|---|

| `Cannot open webcam` | Check that no other app is using the camera. Try changing `cv2.VideoCapture(0)` to `1` or `2`. |

| `Model not found` | Download `hand_landmarker.task` into `models/` (see above). |

| Low FPS | Close other applications using the GPU/CPU. Reduce capture resolution by editing the `cap.set()` calls. |

| Hands not detected | Improve lighting and keep your hand within the camera frame. Lower `min_hand_detection_confidence` in the options. |



## License



This project is provided as-is for educational and creative use.

Here is a polished, modern, and clean README.md formatted to make your project stand out on GitHub.

🦴 X-Ray Hand Vision
A real-time webcam application that overlays a glowing neon bone structure onto your hands to produce a striking "X-ray in the dark" visual effect. Perfect for creative social media content, live streams, or interactive visual experiments.

✨ Key Features
Multi-Hand Tracking — Detects up to 2 hands simultaneously, assigning distinct neon glow colors to each.

Dynamic Bone-Pulse — Skeleton brightness pulses in a sine wave, with pulse speed adapting dynamically to hand velocity.

6 Preset Glow Colors — Instantly cycle between Cyan, Green, Magenta, Orange, White, and Red.

Customizable Glow Intensity — Scale visual strength smoothly from subtle (0.4×) to high-contrast neon (4.0×).

Selective Background Darkening — Uses convex-hull masking to dim the surrounding background while keeping your hand and glow bright.

One-Key Screenshots — Capture and save full-resolution PNGs with timestamps straight to disk.

🛠️ Requirements & Setup
Prerequisites
Python: 3.9 to 3.12

Hardware: Functional Webcam

1. Installation
Clone this repository and install the required dependencies:

Bash
git clone https://github.com/your-username/xray-hand-vision.git
cd xray-hand-vision
pip install -r requirements.txt
2. Download MediaPipe Model
The application requires MediaPipe's hand_landmarker.task file in the models/ directory.

Automatically via PowerShell:

PowerShell
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task" -OutFile "models\hand_landmarker.task"
Alternatively, launch python xray_hand.py without the file, and the script will print the direct download link.

🚀 Quick Start
Ensure your webcam is connected, then run:

Bash
python xray_hand.py
🎮 Interactive Controls
Key	Action
1 – 6	Cycle glow colors (Cyan, Green, Magenta, Orange, White, Red)
B	Toggle background darkening mask
Space	Toggle dynamic bone-pulse animation
+ / -	Increase / decrease glow intensity
S	Save a timestamped screenshot to screenshots/
Q / Esc	Quit application
🔬 How It Works
Video Capture: Reads live video frames via OpenCV and flips them horizontally for a natural mirror display.

Landmark Detection: Uses MediaPipe’s HandLandmarker Tasks API to track 21 normalized 3D hand coordinates per hand.

Skeleton Rendering: Maps landmarks to image pixels and connects them using MediaPipe's HAND_CONNECTIONS graph, drawing proportional joint points at fingertips.

Multi-Pass Glow Effect: Renders the skeleton onto an isolated layer, applies dual-pass Gaussian blurs (σ 
1
​
 =8, σ 
2
​
 =25) for atmospheric bloom, and overlays the sharp core skeleton.

Additive Compositing: Blends the glowing overlay back onto the primary frame using cv2.add.

Background Masking: Builds a dilated convex hull around detected landmarks to dim the surrounding background while maintaining maximum neon pop.

📂 Project Structure
Plaintext
xray/
├── models/
│   └── hand_landmarker.task   # MediaPipe hand model (~7.8 MB)
├── screenshots/               # Output directory for saved snapshots
├── requirements.txt           # Python dependencies
├── xray_hand.py               # Main application entry point
└── README.md                  # Documentation
⚙️ Configuration & Tuning
You can easily adjust core parameters directly at the top of xray_hand.py:

GLOW_COLORS — Modify BGR color palettes.

make_glow_layer() — Fine-tune sigma1 (sharp core glow) and sigma2 (wide atmospheric halo).

darken_background() — Adjust the background attenuation factor.

HandLandmarkerOptions — Customize detection confidence thresholds or set max hand count.

❓ Troubleshooting
Issue	Solution
Cannot open webcam	Ensure no other app (Zoom, Teams, Browser) is using the camera. If you have multiple devices, change cv2.VideoCapture(0) to 1 or 2 in xray_hand.py.
Model not found	Ensure hand_landmarker.task is saved inside the models/ directory.
Low FPS / Stuttering	Close GPU/CPU-heavy apps. Lower the capture resolution via cap.set() in the script.
Tracking Drops	Ensure adequate room lighting. If issues persist, lower min_hand_detection_confidence in xray_hand.py.
📄 License
This project is open-source and provided as-is for educational, creative, and experimental use.

i want to add it to githiub so make in that kind of file format

1. Installation
Clone this repository and install the dependencies:

Bash
git clone [https://github.com/your-username/xray-hand-vision.git](https://github.com/your-username/xray-hand-vision.git)
cd xray-hand-vision
pip install -r requirements.txt
2. Download MediaPipe Model
The application requires MediaPipe's hand_landmarker.task file placed inside the models/ directory.

PowerShell:

PowerShell
Invoke-WebRequest -Uri "[https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task)" -OutFile "models\\hand_landmarker.task"
cURL / bash:

Bash
curl -L -o models/hand_landmarker.task [https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task)
Alternatively, launch python xray_hand.py without the model file and the script will display the download URL.

🚀 Quick Start
Ensure your webcam is connected, then run:

Bash
python xray_hand.py
🎮 Interactive Controls
Key	Action
1 – 6	Cycle glow color (Cyan, Green, Magenta, Orange, White, Red)
B	Toggle background darkening mask
Space	Toggle dynamic bone-pulse animation
+ / -	Increase / decrease glow intensity
S	Save a timestamped screenshot to screenshots/
Q / Esc	Quit application
🔬 How It Works
Video Capture: Reads live video frames via OpenCV and flips them horizontally for a natural mirror view.

Landmark Detection: Uses MediaPipe’s HandLandmarker Tasks API to track 21 normalized 3D coordinates per hand.

Skeleton Rendering: Maps landmarks to pixel coordinates and connects them using MediaPipe's HAND_CONNECTIONS graph, drawing joint nodes at fingertips.

Multi-Pass Glow Effect: Renders the skeleton onto an isolated layer, applies dual Gaussian blurs (σ 
1
​
 =8, σ 
2
​
 =25) for atmospheric bloom, and overlays the crisp skeleton core.

Additive Compositing: Blends the glowing layer back onto the camera frame using cv2.add.

Background Masking: Builds a dilated convex hull around detected hand landmarks to dim the background while maintaining neon brightness.

On-Screen Display: Displays FPS, active color preset, glow intensity, and pulse status in real time.

📂 Project Structure
Plaintext
xray/
├── models/
│   └── hand_landmarker.task   # MediaPipe hand model (~7.8 MB)
├── screenshots/               # Output directory for saved PNG snapshots
├── requirements.txt           # Python dependencies
├── xray_hand.py               # Main application entry point
└── README.md                  # Documentation
⚙️ Configuration & Tuning
Key tunables live near the top of xray_hand.py:

GLOW_COLORS — Modify BGR color definitions.

make_glow_layer() — Fine-tune sigma1 (sharp core glow) and sigma2 (wide atmospheric halo).

darken_background() — Adjust background attenuation level.

HandLandmarkerOptions — Customize detection confidence thresholds and max hand count.

❓ Troubleshooting
Issue	Solution
Cannot open webcam	Ensure no other application (Zoom, Teams, Browser) is using the camera. Try changing cv2.VideoCapture(0) to 1 or 2 in xray_hand.py.
Model not found	Ensure hand_landmarker.task is saved inside the models/ directory.
Low FPS / Stuttering	Close GPU/CPU-heavy apps. Lower capture resolution via cap.set() in the script.
Tracking Drops	Ensure proper room lighting. Lower min_hand_detection_confidence in xray_hand.py if needed.
📄 License
This project is open-source and provided as-is for educational, creative, and experimental use.
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("FILE_CREATED: README.md")


```text?code_stdout&code_event_index=1
FILE_CREATED: README.md

Your README.md file is ready

MD icon
README
 MD 
Open
I have generated the formatted README.md file ready to be pushed directly into your GitHub repository root directory.

Quick steps to add it to your GitHub repository:
Place the file in your project folder: Save the downloaded README.md into the root of your project directory (xray/README.md).

Commit and push to GitHub:

Bash
git add README.md
git commit -m "docs: add GitHub README documentation"
git push origin main



Gemini is AI and can make mistakes.

Analysing
# 🦴 X-Ray Hand Vision

A real-time webcam application that overlays a glowing neon bone structure onto your hands to produce a striking "X-ray in the dark" visual effect. Built for social media content, live streams, and creative visual projects.

---

## ✨ Key Features

- **Multi-Hand Tracking** — Detects up to 2 hands simultaneously, rendering each with distinct color palettes.
- **Dynamic Bone-Pulse** — Skeleton brightness pulses in a sine wave, with pulse speed adapting dynamically to hand movement.
- **6 Preset Glow Colors** — Instantly cycle between Cyan, Green, Magenta, Orange, White, and Red.
- **Customizable Glow Intensity** — Scale visual strength smoothly from subtle to high-contrast neon bloom.
- **Selective Background Darkening** — Uses convex-hull masking to dim the background while keeping your hand and glow bright.
- **One-Key Screenshots** — Capture and save timestamped PNG snapshots straight to disk.

---

## 🛠️ Requirements & Setup

### Prerequisites

- **Python:** `3.9` – `3.12`
- **Hardware:** Functional Webcam

### Dependencies

```text
opencv-python>=4.8.0
mediapipe>=1.0.0
numpy>=1.24.0
```

### 1. Installation

Clone this repository and install the dependencies:

```bash
git clone https://github.com/your-username/xray-hand-vision.git
cd xray-hand-vision
pip install -r requirements.txt
```

### 2. Download MediaPipe Model

The application requires MediaPipe's `hand_landmarker.task` file placed inside the `models/` directory.

**PowerShell:**
```powershell
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task" -OutFile "models\hand_landmarker.task"
```

**cURL / bash:**
```bash
curl -L -o models/hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
```

*Alternatively, launch `python xray_hand.py` without the model file and the script will display the download URL.*

---

## 🚀 Quick Start

Ensure your webcam is connected, then run:

```bash
python xray_hand.py
```

---

## 🎮 Interactive Controls

| Key | Action |
| :--- | :--- |
| `1` – `6` | Cycle glow color *(Cyan, Green, Magenta, Orange, White, Red)* |
| `B` | Toggle background darkening mask |
| `Space` | Toggle dynamic bone-pulse animation |
| `+` / `-` | Increase / decrease glow intensity |
| `S` | Save a timestamped screenshot to `screenshots/` |
| `Q` / `Esc` | Quit application |

---

## 🔬 How It Works

1. **Video Capture:** Reads live video frames via OpenCV and flips them horizontally for a natural mirror view.
2. **Landmark Detection:** Uses MediaPipe’s `HandLandmarker` Tasks API to track 21 normalized 3D coordinates per hand.
3. **Skeleton Rendering:** Maps landmarks to pixel coordinates and connects them using MediaPipe's `HAND_CONNECTIONS` graph, drawing joint nodes at fingertips.
4. **Multi-Pass Glow Effect:** Renders the skeleton onto an isolated layer, applies dual Gaussian blurs ($\sigma_1 = 8$, $\sigma_2 = 25$) for atmospheric bloom, and overlays the crisp skeleton core.
5. **Additive Compositing:** Blends the glowing layer back onto the camera frame using `cv2.add`.
6. **Background Masking:** Builds a dilated convex hull around detected hand landmarks to dim the background while maintaining neon brightness.
7. **On-Screen Display:** Displays FPS, active color preset, glow intensity, and pulse status in real time.

---

## 📂 Project Structure

```text
xray/
├── models/
│   └── hand_landmarker.task   # MediaPipe hand model (~7.8 MB)
├── screenshots/               # Output directory for saved PNG snapshots
├── requirements.txt           # Python dependencies
├── xray_hand.py               # Main application entry point
└── README.md                  # Documentation
```

---

## ⚙️ Configuration & Tuning

Key tunables live near the top of `xray_hand.py`:

- `GLOW_COLORS` — Modify BGR color definitions.
- `make_glow_layer()` — Fine-tune `sigma1` (sharp core glow) and `sigma2` (wide atmospheric halo).
- `darken_background()` — Adjust background attenuation level.
- `HandLandmarkerOptions` — Customize detection confidence thresholds and max hand count.

---

## ❓ Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **Cannot open webcam** | Ensure no other application (Zoom, Teams, Browser) is using the camera. Try changing `cv2.VideoCapture(0)` to `1` or `2` in `xray_hand.py`. |
| **Model not found** | Ensure `hand_landmarker.task` is saved inside the `models/` directory. |
| **Low FPS / Stuttering** | Close GPU/CPU-heavy apps. Lower capture resolution via `cap.set()` in the script. |
| **Tracking Drops** | Ensure proper room lighting. Lower `min_hand_detection_confidence` in `xray_hand.py` if needed. |

---

## 📄 License

This project is open-source and provided as-is for educational, creative, and experimental use.
README.md
Displaying README.md.
