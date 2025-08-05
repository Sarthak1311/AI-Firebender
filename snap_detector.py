import math

class SnapDetector:
    def __init__(self):
        self.issnapped = False

    def update(self, hand_landmarks):
        thumb = hand_landmarks.landmark[4]
        middle = hand_landmarks.landmark[12]
        pinky = hand_landmarks.landmark[20]

        snap_dist = math.dist([thumb.x, thumb.y], [middle.x, middle.y])
        wristopen = math.dist([thumb.x, thumb.y], [pinky.x, pinky.y])

        if snap_dist <= 0.02:
            self.issnapped = True
        elif wristopen >= 0.18:
            self.issnapped = False

        return self.issnapped
