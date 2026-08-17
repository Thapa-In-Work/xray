# X-Ray Hand Vision

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
