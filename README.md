
# 🔥 AI Firebender

Control virtual fire and your **Mac screen brightness** using just **hand gestures** and **snaps** – powered by MediaPipe and OpenCV.

This project lets you:
- Summon fire using a snap gesture with your **right hand**
- Increase or decrease fire size using your **left hand's fingers** in specific zones
- Change **screen brightness on macOS** based on fire intensity

---

## ✨ Features

- 🔥 Snap with your right hand to summon fire at that position
- Make a peace sign with your left hand and move into:
- 🟥 **Red box** to increase fire (and screen brightness)
- 🟦 **Blue box** to decrease fire (and screen brightness)
-  Brightness control support for **macOS**
-  Real-time hand tracking with **MediaPipe**

---

##  Project Structure
│
├── main.py # Main application logic
├── fire_animator.py # Handles fire animation rendering
├── fire_controller.py # Stores and manages fire position
├── snap_detector.py # Detects snap gestures
├── brightness_controller.py # Adjusts screen brightness (macOS only)
├── fire/ # Folder with fire animation frames
└── README.md # You're here!

## Requirements

- Python 3.8+
- macOS (for brightness control)
- Webcam

---

## Install dependencies:
- pip install opencv-python mediapipe

---

## How it Works
1. MediaPipe detects hand landmarks (21 points per hand)
2. SnapDetector checks the distance between thumb and middle finger
3. FireController saves the snap location
4. FireAnimator draws flame animations frame-by-frame
5. Peace gesture + position in control zones modifies fire size and brightness

---

## To-Do / Ideas
 - Add support for Windows/Linux brightness control
 - Add sound effects or visual feedback for brightness change
 - Replace fire animation with particle effects
 - Log user gestures for analytics
 ### feel free to contribute 

--- 

## Author
- Made by [Sarthak Tyagi](https://github.com/sarthaktyagi1)
- 📫 Connect with me on [LinkedIn](https://www.linkedin.com/in/sarthak-tyagi-a18812226/)

## MIT License – do whatever you want, just give credit.
