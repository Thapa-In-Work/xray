<p align="center">
  <h1 align="center">X-Ray Hand Vision</h1>
  <p align="center">Real-time webcam X-ray skeleton overlay on hands</p>
</p>

---

A glowing neon bone structure tracked live on your hand via webcam. Multi-hand, multi-color, with a darkened background for the full X-ray-in-the-dark look.

### File Structure

```
xray/
├── models/
│   └── hand_landmarker.task    ← MediaPipe hand model (7.8 MB)
├── screenshots/                ← saved PNGs go here (auto-created)
├── xray_hand.py                ← single-file application
├── requirements.txt
├── .gitignore
└── README.md
```

### Run

```powershell
# 1. Clone
git clone https://github.com/Thapa-In-Work/xray.git
cd xray

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the hand model
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task" -OutFile "models\hand_landmarker.task"

# 4. Run
python xray_hand.py
```

### Requirements

- Python 3.9 -- 3.12
- Webcam
- opencv-python `>=4.8`
- mediapipe `>=1.0`
- numpy `>=1.24`

### Controls

| Key | Action |
|:--:|:--|
| `1` -- `6` | Cycle glow color |
| `B` | Toggle background darkening |
| `S` | Save screenshot |
| `Space` | Toggle bone-pulse animation |
| `+` / `-` | Glow intensity up / down |
| `Q` / `Esc` | Quit |

### How It Works

```
Webcam frame
  → MediaPipe HandLandmarker (21 landmarks per hand)
    → Draw skeleton on black layer (bones + joints)
      → Dual Gaussian blur (σ=8 + σ=25) blended → glow halo
        → Sharp skeleton re-drawn on top → neon core
          → Additive composite onto original frame
            → Background darkened outside hand bounding box
```

### Features

- **Multi-hand** -- Up to 2 hands, each a different color
- **Pulse animation** -- Brightness syncs to hand movement speed
- **6 colors** -- Cyan, green, magenta, orange, white, red
- **Adjustable glow** -- Intensity 0.4 to 4.0
- **Screenshots** -- Timestamped PNGs saved to `screenshots/`
