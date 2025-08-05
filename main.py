import cv2
import mediapipe as mp
import math
from brightness_controller import increase_brightness, decrease_brightness
from fire_animator import FireAnimator
from snap_detector import SnapDetector
from fire_controller import FireController

# Init MediaPipe
mphands = mp.solutions.hands
hands = mphands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mpdraw = mp.solutions.drawing_utils

# Modules
fire_anim = FireAnimator(fire_folder="fire", size=200)
snapper = SnapDetector()
controller = FireController()

# Box positions
RED_BOX = (50, 50, 190, 190)     # 140x140 box
BLUE_BOX = (220, 50, 360, 190)   # same size, spaced apart

# Webcam
cap = cv2.VideoCapture(0)

# Persistent color state
left_color = None

def is_inside_box(x, y, box):
    return box[0] < x < box[2] and box[1] < y < box[3]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    imgrgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgrgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label

            # ---------------- Right Hand for Snap ----------------
            if label == 'Right':
                is_snapped = snapper.update(hand_landmarks)
                if is_snapped:
                    controller.set_fire_position(
                        (hand_landmarks.landmark[0].x + hand_landmarks.landmark[9].x) / 2,
                        (hand_landmarks.landmark[0].y + hand_landmarks.landmark[9].y) / 2,
                    )

            # ---------------- Left Hand for Control ----------------
            if label == 'Left':
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]

                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                mx, my = int(middle_tip.x * w), int(middle_tip.y * h)

                # Gesture detection
                pinch_dist = math.hypot(ix - mx, iy - my)

                # Pick color (if pinched inside a box)
                if pinch_dist < 60:
                    if is_inside_box(ix, iy, RED_BOX) or is_inside_box(mx, my, RED_BOX):
                        left_color = 'red'
                    elif is_inside_box(ix, iy, BLUE_BOX) or is_inside_box(mx, my, BLUE_BOX):
                        left_color = 'blue'

                # Drop color (fingers spread apart)
                elif pinch_dist > 110:
                    left_color = None

                # Draw fingertips with selected color
                if left_color == 'red':
                    cv2.circle(frame, (ix, iy), 12, (0, 0, 255), -1)
                    cv2.circle(frame, (mx, my), 12, (0, 0, 255), -1)
                elif left_color == 'blue':
                    cv2.circle(frame, (ix, iy), 12, (255, 0, 0), -1)
                    cv2.circle(frame, (mx, my), 12, (255, 0, 0), -1)
                else:
                    cv2.circle(frame, (ix, iy), 10, (255, 255, 255), -1)
                    cv2.circle(frame, (mx, my), 10, (255, 255, 255), -1)

                # Interact with fire
                if left_color and controller.fire_position:
                    fx = int(controller.fire_position[0] * w)
                    fy = int(controller.fire_position[1] * h)
                    finger_x = (ix + mx) // 2
                    finger_y = (iy + my) // 2
                    dist = math.hypot(finger_x - fx, finger_y - fy)

                    if dist < 100:
                        if left_color == 'red':
                            fire_anim.size = min(400, fire_anim.size + 5)
                            increase_brightness()

                        elif left_color == 'blue':
                            fire_anim.size = max(100, fire_anim.size - 5)
                            decrease_brightness()


    # Draw UI boxes
    cv2.rectangle(frame, RED_BOX[:2], RED_BOX[2:], (0, 0, 255), 2)
    cv2.putText(frame, "Increase", (RED_BOX[0], RED_BOX[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.rectangle(frame, BLUE_BOX[:2], BLUE_BOX[2:], (255, 0, 0), 2)
    cv2.putText(frame, "Decrease", (BLUE_BOX[0], BLUE_BOX[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Draw fire
    if snapper.issnapped and controller.fire_position:
        fx = int(controller.fire_position[0] * w)
        fy = int(controller.fire_position[1] * h)
        fire_anim.draw_fire(frame, fx - fire_anim.size // 2, fy - fire_anim.size)

    cv2.imshow("🔥 Fire Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
