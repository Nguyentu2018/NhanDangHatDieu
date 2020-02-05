# importing modules
import ReadHsv
import cv2
import numpy as np

# capturing video through webcam
cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    a = cap.get(7)
    cv2.imshow("Color Tracking", img)
    # cv2.imshow("red",res)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break