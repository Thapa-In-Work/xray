# 🦴 X-Ray Hand Vision

> Real-time webcam application that overlays a glowing neon skeleton on your hand, creating an interactive X-ray vision effect. Perfect for social media content, demos, and creative vision experiments.

![Python](https://img.shields.io/badge/Python-3.9--3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-1.0+-00979D?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Demo & Overview

Hold your hand up to the camera and watch a glowing neon bone structure track your movement in real time—complete with a soft halo glow and dynamic background darkening that sells the "X-ray in the dark" visual.

---

## ✨ Features

- 🖐️ **Multi-Hand Tracking:** Detects up to 2 hands simultaneously, rendering each in a distinct glow color.
- 🎨 **6 Glow Palettes:** Switch between **Cyan**, **Green**, **Magenta**, **Orange**, **White**, and **Red** on the fly.
- 💓 **Bone-Pulse Animation:** Brightness pulses dynamically; pulse frequency scales based on hand movement speed.
- 🌑 **Background Darkening:** Generates a dynamic convex hull mask around hands to darken everything outside the gesture area.
- 🎚️ **Adjustable Intensity:** Fine-tune glow scaling dynamically from subtle (`0.4`) to intense bloom (`4.0`).
- 📸 **Screenshot Export:** Capture high-resolution PNG screenshots instantly with automatic timestamps.

---

## 🛠️ Requirements & Setup

### Prerequisites
- **Python:** `3.9` to `3.12`
- **Hardware:** standard webcam

### 1. Install Dependencies
```bash
pip install -r requirements.txt
