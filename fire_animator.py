import os
import cv2

class FireAnimator:
    def __init__(self, fire_folder="fire", size=200):
        self.fire_frames = self._load_fire_frames(fire_folder)
        self.size = size
        self.frame_idx = 0

    def _load_fire_frames(self, folder):
        fire_frames = []
        fire_files = sorted(os.listdir(folder))
        for file in fire_files:
            img = cv2.imread(os.path.join(folder, file), cv2.IMREAD_UNCHANGED)
            if img is not None:
                fire_frames.append(img)
        return fire_frames

    def overlay_transparent(self, background, overlay, x, y):
        overlay = cv2.resize(overlay, (self.size, self.size))
        h, w = overlay.shape[:2]

        if x + w > background.shape[1] or y + h > background.shape[0] or x < 0 or y < 0:
            return

        b, g, r, a = cv2.split(overlay)
        mask = a / 255.0
        mask_inv = 1.0 - mask

        for c in range(3):
            background[y:y+h, x:x+w, c] = (mask * overlay[:, :, c] +
                                           mask_inv * background[y:y+h, x:x+w, c])

    def draw_fire(self, frame, x, y):
        fire_frame = self.fire_frames[self.frame_idx % len(self.fire_frames)]
        self.overlay_transparent(frame, fire_frame, x, y)
        self.frame_idx += 1
