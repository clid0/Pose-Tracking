import cv2
import numpy as np
import time
import PoseModule as pm
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('PersonalTrainer/squat.mp4')
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img, False)  # 해당 좌표들을 제외하고는 그리지 않음
    # 포지션을 그리진 않음
    lmList = detector.findPosition(img, False)
    # print(lmList) # 전체 좌표가 나옴
    if len(lmList) != 0:
        # Right Arm
        # angle = detector.findAngle(img, 12, 14, 16)
        # # Left Arm
        # angle = detector.findAngle(img, 11, 13, 15)
        # Right legs
        left_angle = detector.findAngle(img, 23, 25, 27)
        # Left legs
        right_angle = detector.findAngle(img, 24, 26, 28)
        # angle = detector.findAngle(img, 11, 13, 15, False)
        # 210도를 0라고 하고 310을 100이라고 함
        # per = np.interp(angle, (210, 310), (0, 100))
        # squat angel
        per1 = np.interp(left_angle, (180, 210), (0, 100))
        per2 = np.interp(right_angle, (170, 180), (0, 100))
        # bar = np.interp(angle, (220, 310), (650, 100))
        print(per1, per2)
        bar1 = np.interp(left_angle, (170, 210), (650, 100))
        # print(angle, per)
        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per1 == 100 and per2 == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per1 == 0 and per2 == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)
        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar1)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per1)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)
        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
