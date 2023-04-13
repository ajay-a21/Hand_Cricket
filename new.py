import cv2
import mediapipe
import numpy as np
import random
import time

cap = cv2.VideoCapture(0)

while not cap.isOpened():
    cap = cv2.VideoCapture(0)
    cv2.waitKey(1000)

innings1 = 0

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

    return landmarkList

def fingers(landmarks):
    fingerTips = []
    tipIds = [4, 8, 12, 16, 20]

    # Check if thumb is up
    if landmarks[tipIds[0]][1] > landmarks[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

print(" TossTime ! ")

while True :
    toss = int(input("SPIN NUMBER (0,1) -> (HEADS , TAILS) : "))
    coin = random.randint(0,1)
    if toss == coin :
        print("PlayerWonTheToss (: ")
        input1 = int(input("Enter 0 -> BAT OR 1 -> BOWl : "))
        if input1 == 0 :
            print("Player Won The Toss and choose to Bat First")
            schedule = 1 
            break
        else :
            print("Player Won The Toss and choose to Bowl First")
            schedule = 0
            break

    else :
        print("TossLossed ): ")
        input1 = random.randint(0,1)
        if input1 == 1 :
            print("Computer Won The Toss and choose to Bat First")
            schedule = 0
            break
        else :
            print("Computer Won The Toss and choose to Bowl First")
            schedule = 1
            break

# Computer Won The Toss and choose to Bat First
# Player Won The Toss and choose to Bowl First

# computerBatting
# PlayerBowling

schedule = 0 

if schedule == 0 :

    innings1 = 0

    while True :

        ret, img = cap.read()
        if not ret:
            break
        #bowl = int(input("Bowl -----> "))
        bowl = 0
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lmList = handLandmarks(imgRGB)

        if len(lmList) != 0:
            finger = fingers(lmList)
            fingerCount = np.sum(finger)
            bowl = fingerCount
        
        if bowl not in range(0,7) :
            print("Bowlcorrectly")
            time.sleep(2)
            continue

        autoBat = random.randint(0,6)
        if innings1 >= 200 :
            autoBat = bowl
            break

        if bowl == autoBat :
            print("ComputerOut ! ")
            time.sleep(10)
            break

        print("LastBall run (auto): " , autoBat)
        innings1 += autoBat

        print("LiveScore ",innings1)

        cv2.putText(img, f"Innings 1: {innings1}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Webcam", img)

        time.sleep(5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    print("Target for player : ",innings1+1)
    target = innings1+1
    print(" * InningsBreak * ")

    # computerBowling
    # PlayerBatting


    innings2 = 0
    while True :
        print("Target : ",target)
        #bat = int(input("Bat -----> "))
        bat = 7
        ret, img = cap.read()
        if not ret:
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lmList = handLandmarks(imgRGB)

        if len(lmList) != 0:
            finger = fingers(lmList)
            fingerCount = np.sum(finger)
            bat = fingerCount

        if bat not in range(0,7) :
            print("BatCorrectly")
            time.sleep(2)
            continue

        autoBowl = random.randint(0,6)
        if bat == autoBowl :
            print("PlayerOut !")
            break

        print("LastBall (auto): ",autoBowl)
        innings2 += bat
        target -= bat

        cv2.putText(img, f"Innings2: {innings2}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Webcam", img)
        time.sleep(4)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("Second innings live score : ",innings2)
        if innings2 > innings1 :
            print("PlayerWon !")
            break

    if innings2 == innings1 :
        print("MatchTied")
    elif innings2 < innings1 :
        print("ComputerWon")

    

# Player Won The Toss and choose to Bat First
# Computer Won The Toss and choose to Bowl First

# computerBowling
# PlayerBatting

else :

    innings1 = 0

    while True :
        #bat = int(input("Bat -----> "))
        bat = 7
        ret, img = cap.read()
        if not ret:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lmList = handLandmarks(imgRGB)

        if len(lmList) != 0:
            finger = fingers(lmList)
            fingerCount = np.sum(finger)
            bat = fingerCount

        if bat not in range(0,7) :
            print("BatCorrectly ")
            time.sleep(2)
            continue
        autoBowl = random.randint(0,6)
        if innings1 >= 200 :
            autoBowl = bat
            break

        if bat == autoBowl :
            print("PlayerOut !")
            time.sleep(25)
            break

        print("LastBall (auto): " , autoBowl)
        innings1 += bat

        cv2.putText(img, f"LiveScore innings1: {innings1}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Webcam", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print("LiveScore ",innings1)
        time.sleep(5)
        
    print("Target For Computer : ",innings1+1)
    target = innings1+1
    print(" * InningsBreak * ")

    # computerBatting
    # PlayerBowling

    innings2 = 0
    while True :
        print("Target : ",target)
        #bowl = int(input("Bowl -----> "))
        bowl = 7
        ret, img = cap.read()
        if not ret:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lmList = handLandmarks(imgRGB)

        if len(lmList) != 0:
            finger = fingers(lmList)
            fingerCount = np.sum(finger)
            bowl = fingerCount

        if bowl not in range(0,7) :
            print("BowlCorrectly")
            time.sleep(2)
            continue
        autoBat = random.randint(0,6)
        if bowl == autoBat :
            print("ComputerOut !")
            break
        print("LastBall run (auto): ",autoBat)
        innings2 += autoBat

        cv2.putText(img, f"LiveScore innings2: {innings2}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        target -= autoBat

        print("Second innings live score : ",innings2)
        if innings2 > innings1 :
            print("ComputerWon !")
            break
        time.sleep(3)
    if innings2 == innings1 :
        print("MatchTied")
    elif innings2 < innings1 :
        print("PlayerWon")
