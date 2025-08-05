import mediapipe as mp 
import cv2 
import math

# init mediapipe 
mpface = mp.solutions.face_mesh
face = mpface.FaceMesh(refine_landmarks =True)
mpdrawing = mp.solutions.drawing_utils

# capturing 
cap = cv2.VideoCapture(0)
blowing = False
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame  = cv2.flip(frame,1)
    img_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = face.process(img_rgb)

    if results.multi_face_landmarks:
        for faceldm in results.multi_face_landmarks:
            upper_lips = faceldm.landmark[13]
            lower_lips = faceldm.landmark[14]

            mouth_open = math.dist([upper_lips.x,upper_lips.y],[lower_lips.x,lower_lips.y])

            cv2.putText(frame,f"dist: {mouth_open}",(70,120),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),2)
            # mpdrawing.draw(results.multi_face_landmarks,(0,255,0))
            if mouth_open > 0.009:
                blow_timer += 1
            else:
                blow_timer = 0

            if blow_timer > 3:
                cv2.putText(frame,"blowing ",(70,150),cv2.FONT_HERSHEY_COMPLEX,0.8,(123,255,68),2)
                

    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()