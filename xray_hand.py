"""
X-Ray Hand Vision — Real-time webcam X-ray skeleton overlay on hands.

Controls:
    1-6     Cycle glow color
    B       Toggle background darkening
    S       Save screenshot
    SPACE   Toggle bone-pulse animation
    +/-     Adjust glow intensity
    Q/ESC   Quit
"""

import cv2
import numpy as np
import mediapipe as mp
import math
import time
import os
from collections import deque
from pathlib import Path

# ── MediaPipe Tasks setup ─────────────────────────────────────────────────────
BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarksConnections = mp.tasks.vision.HandLandmarksConnections

MODEL_PATH = str(Path(__file__).parent / "models" / "hand_landmarker.task")

HAND_CONNECTIONS = HandLandmarksConnections.HAND_CONNECTIONS
FINGERTIPS = {4, 8, 12, 16, 20}

# ── Glow color presets (BGR) ──────────────────────────────────────────────────
GLOW_COLORS = {
    "cyan":    (255, 255, 0),
    "green":   (0, 255, 0),
    "magenta": (255, 0, 255),
    "orange":  (0, 165, 255),
    "white":   (255, 255, 255),
    "red":     (0, 0, 255),
}
COLOR_NAMES = list(GLOW_COLORS.keys())


class State:
    def __init__(self):
        self.color_idx = 0
        self.darken = True
        self.pulse_enabled = True
        self.glow_strength = 1.8
        self.screenshot_dir = "screenshots"
        self.prev_landmarks_list = None
        self.prev_time = time.time()
        self.pulse_phase = 0.0
        self.fps_history = deque(maxlen=30)

    @property
    def color_name(self):
        return COLOR_NAMES[self.color_idx]

    @property
    def color(self):
        return GLOW_COLORS[self.color_name]

    def next_color(self):
        self.color_idx = (self.color_idx + 1) % len(COLOR_NAMES)


# ── Drawing helpers ───────────────────────────────────────────────────────────

def draw_skeleton(layer, landmarks, w, h, color, thickness=2, joint_radius=4):
    """Draw bones (lines) and joints (circles) on *layer* (in-place)."""
    h_pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    for conn in HAND_CONNECTIONS:
        i, j = conn.start, conn.end
        cv2.line(layer, h_pts[i], h_pts[j], color, thickness, cv2.LINE_AA)

    for idx, pt in enumerate(h_pts):
        r = joint_radius + (2 if idx in FINGERTIPS else 0)
        cv2.circle(layer, pt, r, color, -1, cv2.LINE_AA)


def make_glow_layer(layer, sigma1=8, sigma2=25, strength=1.8):
    """Return a blurred glow image by blending two Gaussian blur passes."""
    blur1 = cv2.GaussianBlur(layer, (0, 0), sigmaX=sigma1)
    blur2 = cv2.GaussianBlur(layer, (0, 0), sigmaX=sigma2)
    glow = cv2.addWeighted(blur1, 1.0, blur2, 1.4, 0)
    glow = (glow * strength).clip(0, 255).astype(np.uint8)
    return glow


def darken_background(frame, mask, pad=40, fade=0.70):
    """Darken everything outside a padded bounding box around the hand mask."""
    h, w = frame.shape[:2]
    coords = cv2.findNonZero(mask)
    if coords is None:
        return frame
    x, y, bw, bh = cv2.boundingRect(coords)
    x0 = max(x - pad, 0)
    y0 = max(y - pad, 0)
    x1 = min(x + bw + pad, w)
    y1 = min(y + bh + pad, h)

    dark = (frame * (1 - fade)).astype(np.uint8)
    dark[y0:y1, x0:x1] = frame[y0:y1, x0:x1]
    return dark


def build_hand_mask(landmarks, w, h, pad=30):
    """Create a filled convex-hull mask for the hand region."""
    pts = np.array(
        [(int(lm.x * w), int(lm.y * h)) for lm in landmarks],
        dtype=np.int32,
    )
    hull = cv2.convexHull(pts)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillConvexPoly(mask, hull, 255)
    kernel = np.ones((pad, pad), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask


def compute_pulse_speed(landmarks, prev_landmarks, dt):
    """Return a scalar 0-1 based on average hand movement speed."""
    if prev_landmarks is None or dt <= 0:
        return 0.3
    total = 0.0
    for lm_cur, lm_prev in zip(landmarks, prev_landmarks):
        dx = lm_cur.x - lm_prev.x
        dy = lm_cur.y - lm_prev.y
        total += math.sqrt(dx * dx + dy * dy)
    avg = total / len(landmarks)
    return min(avg / 0.015, 1.0)


def pulse_color(base_color, intensity):
    """Brighten a BGR colour tuple by *intensity* (0-1)."""
    arr = np.array(base_color, dtype=np.float32)
    arr = arr + (255 - arr) * intensity * 0.5
    return tuple(int(v) for v in arr.clip(0, 255).astype(np.uint8))


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    state = State()
    os.makedirs(state.screenshot_dir, exist_ok=True)

    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Model not found at {MODEL_PATH}")
        print("Download from: https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task")
        return

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.6,
        min_tracking_confidence=0.6,
    )
    hand_landmarker = HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    window = "X-Ray Hand Vision"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    print("Controls: 1-6 color | B darken | S screenshot | SPACE pulse | +/- glow | Q quit")

    frame_idx = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            now = time.time()
            dt = now - state.prev_time
            state.prev_time = now
            state.fps_history.append(1.0 / dt if dt > 0 else 0)

            timestamp_ms = int(now * 1000)
            result = hand_landmarker.detect_for_video(mp_image, timestamp_ms)

            glow_layer = np.zeros((h, w, 3), dtype=np.float32)
            combined_mask = np.zeros((h, w), dtype=np.uint8)

            if result.hand_landmarks:
                for hand_idx, hand_lms in enumerate(result.hand_landmarks):
                    if len(result.hand_landmarks) > 1:
                        ci = hand_idx % len(COLOR_NAMES)
                        base_color = GLOW_COLORS[COLOR_NAMES[ci]]
                    else:
                        base_color = state.color

                    if state.pulse_enabled:
                        prev = (state.prev_landmarks_list[hand_idx]
                                if state.prev_landmarks_list and hand_idx < len(state.prev_landmarks_list)
                                else None)
                        speed = compute_pulse_speed(hand_lms, prev, dt)
                        state.pulse_phase += speed * dt * 6.0
                        pulse_i = (math.sin(state.pulse_phase) + 1) * 0.5
                        draw_color = pulse_color(base_color, pulse_i * 0.6)
                    else:
                        draw_color = base_color

                    draw_skeleton(glow_layer, hand_lms, w, h, draw_color, thickness=3, joint_radius=5)

                    if state.darken:
                        mask = build_hand_mask(hand_lms, w, h, pad=50)
                        combined_mask = cv2.bitwise_or(combined_mask, mask)

                state.prev_landmarks_list = result.hand_landmarks
            else:
                state.prev_landmarks_list = None

            glow_uint8 = glow_layer.astype(np.uint8)
            glow_blur = make_glow_layer(glow_uint8, strength=state.glow_strength)
            composite = cv2.add(frame, glow_blur)

            if state.darken and result.hand_landmarks:
                composite = darken_background(composite, combined_mask, pad=60, fade=0.72)
                composite = cv2.add(composite, glow_blur)

            avg_fps = sum(state.fps_history) / len(state.fps_history) if state.fps_history else 0
            hud = f"FPS:{avg_fps:.0f}  Color:{state.color_name}  Glow:{state.glow_strength:.1f}"
            if state.pulse_enabled:
                hud += "  Pulse:ON"
            cv2.putText(composite, hud, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(composite, hud, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow(window, composite)
            frame_idx += 1

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            elif key == ord("b"):
                state.darken = not state.darken
            elif key == ord("s"):
                ts = time.strftime("%Y%m%d_%H%M%S")
                path = os.path.join(state.screenshot_dir, f"xray_{ts}.png")
                cv2.imwrite(path, composite)
                print(f"Screenshot saved: {path}")
            elif key == ord(" "):
                state.pulse_enabled = not state.pulse_enabled
            elif key in (ord("="), ord("+")):
                state.glow_strength = min(state.glow_strength + 0.2, 4.0)
            elif key == ord("-"):
                state.glow_strength = max(state.glow_strength - 0.2, 0.4)
            elif ord("1") <= key <= ord("6"):
                state.color_idx = key - ord("1")
    finally:
        hand_landmarker.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
