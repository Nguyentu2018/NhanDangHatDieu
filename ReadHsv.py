import cv2
import numpy as np
drawing = False
point1 = ()
point2 = ()
def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing is False:
            drawing = True
            point1 = (x, y)
        else:
            drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            point2 = (x, y)
cap = cv2.VideoCapture(0)
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

def hsv_Value(img, p1, p2):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = []
    s = []
    v = []
    if p1 < p2:
        point1 = p1
        point2 = p2
    else:
        point1 = p2
        point2 = p1

    for i in range(point1[0], point2[0] + 1):
        for j in range(point1[1], point2[1] + 1):
            imghsv = hsv[j][i]
            h.append(imghsv[0])
            s.append(imghsv[1])
            v.append(imghsv[2])
    if h and s and v:
        ValueMin = [min(h), min(s), min(v)]
        ValueMax = [max(h), max(s), max(v)]
    return ValueMax, ValueMin
cap.set(3, 640)
cap.set(4, 480)
def Run():
    while True:
        _, img = cap.read()
        if point1 and point2:
            cv2.rectangle(img, point1, point2, (0, 255, 0), 1)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.imshow("Frame", img)
        key = cv2.waitKey(1)
        if key == ord("e"):
            a, b = hsv_Value(img, point1, point2)
            print(a, b)
            return a, b
            break
# max, min = Run()
# a = np.array(max, np.uint8)
# b = np.array(min, np.uint8)
# c = (a - b) / 2 + b
# c.astype(int)
# delta = 10
# c1 = c + delta
# c2 = c - delta
# print(c1, c2)