import cv2
import numpy as np
import win32con

import HandTrackingModule as htm
import time
import autopy
import win32api

widtheightCam, heightCam = 640, 480
frameR = 30
smoothening = 7

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, widtheightCam)
cap.set(4, heightCam)
detector = htm.handDetector(maxHands=1)
widthScreen, heightScreen = autopy.screen.size()

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[8][1:]

    fingers = detector.fingersUp()
    print(fingers)

    if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
        x3 = np.interp(x1, (frameR, widtheightCam - frameR), (0, widthScreen))
        y3 = np.interp(y1, (frameR, heightCam - frameR), (0, heightScreen))

        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening

        autopy.mouse.move(widthScreen - clocX, clocY)
        cv2.circle(img, (x1, y1), 20, (0, 100, 0), cv2.FILLED)
        plocX, plocY = clocX, clocY

    if fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:

        autopy.mouse.click()
        length, img, lineInfo = detector.findDistance(8, 4, img)
        print("distance:" + str(int(length)))
        #
        # if length < 45:
        #     cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
        #     autopy.mouse.click()

    if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        win32api.mouse_event(0x0800, 0, 0, -10, 0)

    if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
        win32api.mouse_event(0x0800, 0, 0, 10, 0)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
