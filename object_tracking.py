import cv2
import numpy as np
from Object_detection import ObjectDetection

ob = ObjectDetection()
cap = cv2.VideoCapture("1.mp4")
a = True
count = 0

while a:
    a, frame = cap.read()
    if not a or frame is None:
        print("Failed to read frame from video. Exiting...")
        break

    (class_id, scores, boxes) = ob.detect(frame=frame)
    for box in boxes:
        (x, y, w, h) = box
        count = count + 1
        cv2.rectangle(frame, (x, y), (w + x, h + y), (30, 255, 156), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

print(f"Total Detection: {count}")
