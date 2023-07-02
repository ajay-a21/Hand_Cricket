import cv2
import mediapipe
import numpy as np
import random
import time

cap = cv2.VideoCapture(0)

# Initialize hand detection model
initHand = mediapipe.solutions.hands
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils

def handLandmarks(colorImg):
    landmarkList = []
    landmarkPositions = mainHand.process(colorImg) 
    landmarkCheck = landmarkPositions.multi_hand_landmarks
    if landmarkCheck :
        for hand in landmarkCheck:
            for index, landmark in enumerate(
                    hand.landmark):
                draw.draw_landmarks(img, hand,initHand.HAND_CONNECTIONS) 
                h, w, c = img.shape
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)
                landmarkList.append([index, centerX, centerY])

    if len(landmarkList) == 0 :
        return 0
    
    fingerTips = 0
    tipIds = [4, 8, 12, 16, 20]
    
    # Check if thumb is up
    if landmarkList[tipIds[0]][1] < landmarkList[tipIds[0] - 1][1]:
        fingerTips += 1

    for id in range(1, 5):
        if landmarkList[tipIds[id]][2] < landmarkList[tipIds[id] - 3][2]:
            fingerTips += 1

    return fingerTips

flag , computer , player , sleep , bowl , autoBat ,  bat , autoBowl , highscore = 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0

while True:

    ret, img = cap.read()
    if not ret:
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = mainHand.process(imgRGB)

    if results.multi_hand_landmarks:
        
        if sleep % 30 == 0 : 
            sleep = 0
            bowl = handLandmarks(imgRGB)
            if bowl == 5 :
                bowl = 6
            # Match 
            autoBat = random.randint(0,5)
            if autoBat == 5 :
                autoBat = 6
            if bowl != autoBat :
                computer += autoBat
                highscore = max(computer,highscore)
            else :
                flag = 1
        sleep += 1
    cv2.putText(img, f"Computer : {autoBat}", (350, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (190, 100, 10), 2)
    cv2.putText(img, f"Player   : {bowl}", (350, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (210, 170, 250), 2)
    cv2.putText(img, f"HighScore     : {highscore}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 230, 230), 2)
    cv2.putText(img, f"ComputerScore : {computer}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow('Hand Detection', img)

    if flag == 1 :
        break
    if cv2.waitKey(1) == ord('q'):
        break

flag = 0

for i in range(1,120) :
    ret, img = cap.read()
    if not ret:
        break
    tempData = "Wicket !"
    cv2.putText(img, f"Result : {tempData}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Hand Detection', img)
    if cv2.waitKey(1) == ord('q'):
        break

for i in range(1,300) :
    ret, img = cap.read()
    if not ret:
        break
    tempData = "Innings Break !"
    cv2.putText(img, f"Session : {tempData}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Hand Detection', img)
    if cv2.waitKey(1) == ord('q'):
        break

while True:

    ret, img = cap.read()
    if not ret:
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = mainHand.process(imgRGB)

    if results.multi_hand_landmarks:
        if sleep % 30 == 0 : 
            sleep = 0
            bat = handLandmarks(imgRGB)
            if bat == 5 :
                bat = 6
            # Match 
            autoBowl = random.randint(0,5)
            if autoBowl == 5 :
                autoBowl = 5
            if bat != autoBowl :
                player += bat
            else :

                flag = 1
                print("out !")

        sleep += 1
    cv2.putText(img, f"Computer : {autoBowl}", (350, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (190, 100, 10), 2)
    cv2.putText(img, f"Player   : {bat}", (350, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (210, 170, 250), 2)
    cv2.putText(img, f"Target      : {computer+1}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(img, f"PlayerScore : {player}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Hand Detection', img)

    if flag == 1 :
        break

    if player >= computer :
        data = "Match tied !"
        if player > computer :
            data = "Won (:"
            break 
    if cv2.waitKey(1) == ord('q'):
        break

for i in range(1,600) :
    ret, img = cap.read()
    if not ret:
        break
    cv2.putText(img, f"Result : {data}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Hand Detection', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()