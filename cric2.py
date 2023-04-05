import cv2
import mediapipe
import numpy as np

cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils

def handLandmarks(colorImg):
    landmarkList = []
    landmarkPositions = mainHand.process(colorImg) 
    landmarkCheck = landmarkPositions.multi_hand_landmarks
    if landmarkCheck:
        for hand in landmarkCheck:
            for index, landmark in enumerate(
                    hand.landmark):
                draw.draw_landmarks(img, hand,
                                    initHand.HAND_CONNECTIONS) 
                h, w, c = img.shape
                centerX, centerY = int(landmark.x * w), int(
                    landmark.y * h)
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

while True:
    ret, img = cap.read()
    if not ret:
        break
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)

    if len(lmList) != 0:
        finger = fingers(lmList)
        fingerCount = np.sum(finger)

        cv2.putText(img, f"Fingers: {fingerCount}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
