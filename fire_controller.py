import math

class FireController:
    def __init__(self):
        self.current_size = 200  # Starting fire size
        self.min_size = 100
        self.max_size = 400
        self.fire_position = None

    def set_fire_position(self, x, y):
        self.fire_position = (x, y)

    def is_peace_sign(self, hand_landmarks):
        index = hand_landmarks.landmark[8]
        middle = hand_landmarks.landmark[12]
        ring = hand_landmarks.landmark[16]
        pinky = hand_landmarks.landmark[20]

        # Peace sign: index and middle fingers open, others closed
        im_dist = math.dist([index.x, index.y], [middle.x, middle.y])
        rp_dist = math.dist([ring.x, ring.y], [pinky.x, pinky.y])
        return im_dist > 0.08 and rp_dist < 0.04

    def is_near_fire(self, finger_x, finger_y, fire_x, fire_y):
        dist = math.dist([finger_x, finger_y], [fire_x, fire_y])
        return dist < 0.15

    def update_fire_size(self, hand_landmarks, hand_label):
        if self.fire_position is None:
            return self.current_size

        fire_x, fire_y = self.fire_position
        index = hand_landmarks.landmark[8]
        middle = hand_landmarks.landmark[12]

        # Use left hand only for control
        if hand_label == 'Left' and self.is_peace_sign(hand_landmarks):
            # Midpoint of finger
            finger_x = (index.x + middle.x) / 2
            finger_y = (index.y + middle.y) / 2

            if self.is_near_fire(finger_x, finger_y, fire_x, fire_y):
                # 🔴 Increase fire if index+middle are colored red
                self.current_size = min(self.max_size, self.current_size + 5)
            else:
                # 🔵 Decrease fire if fingers moved away
                self.current_size = max(self.min_size, self.current_size - 2)

        return self.current_size
