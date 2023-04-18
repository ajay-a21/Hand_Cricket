import cv2
import mediapipe
import numpy as np
import random
import time
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['mycollection']
pipeline = [
    {
        '$group': {
            '_id': None,
            'max_data1': {'$max': '$player'},
            'max_data2': {'$max': '$computer'}
        }
    }
]

for document in collection.find():
    print(document)

result = list(collection.aggregate(pipeline))
playerMax = result[0]['max_data1']
computerMax = result[0]['max_data2']
print(playerMax)

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
        bowl = 7
        
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
        cv2.putText(img, f"HighestScore: {playerMax}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(1)
        
    print("Target for player : ",innings1+1)
    target = innings1+1
    print(" * InningsBreak * ")
    computer = innings1

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
        cv2.putText(img, f"HighestScore: {playerMax}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(1)

        print("Second innings live score : ",innings2)
        if innings2 > innings1 :
            print("PlayerWon !")
            break

    if innings2 == innings1 :
        print("MatchTied")
    elif innings2 < innings1 :
        print("ComputerWon")
    player = innings2
    

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
        cv2.putText(img, f"HighestScore: {playerMax}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Webcam", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print("LiveScore ",innings1)
        time.sleep(5)
        
    print("Target For Computer : ",innings1+1)
    target = innings1+1
    print(" * InningsBreak * ")

    player = innings1

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
        cv2.putText(img, f"HighestScore: {playerMax}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
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
    computer = innings2



"""


from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import random

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

@app.route('/')
def index():
    return render_template('login.html')

global message
global tossResult 
tossResult = 0

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    global currUser
    user = db.users.find_one({'email': email})
    print(db.users.find_one({'email': email}))
    currUser = user['username']
    
    if user and user['password'] == password:
        message = 'Login successful!'
        return render_template('home.html')
    
    else:
        message = 'Invalid email or password.'
        return redirect(url_for('register'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    iuser = db.users.find_one({'email': email})
    if iuser and iuser['username']:
        message = "Username already exists"
        return render_template('register.html', message = message)

    if username and email and password:
        user = {'username': username, 'email': email, 'password': password}
        db.users.insert_one(user)
        message = 'Registration successful!'
        return redirect(url_for('login'))
        
    else:
        message = 'Please fill in all fields.'

    return render_template('register.html', message = message)

@app.route('/toss')
def toss():
    return render_template('toss.html')

@app.route('/Heads')
def Heads():
    val = 1
    message = random.randint(0,1)
    if(val == message):
        message = "Player Won the Toss"
        return render_template('batBowl.html', message = message)
    val = random.randint(0,1)
    if(val==0):
        message = "Computer Won the Toss and choose to Bat First"
    else:   
        message = "Computer Won the Toss and choose to Bowl First"
    return render_template('display.html', message = message, val = int(val))

@app.route('/Tails')
def Tails():
    print("user clicked")
    val = 0
    message = random.randint(0,1)
    
    if(val == message):
        message = "Player Won the Toss"
        
        return render_template('batBowl.html', message = message)
    val = random.randint(0,1)
    if(val==0):
        message = "Computer Won the Toss and choose to Bat First"
    else:   
        message = "Computer Won the Toss and choose to Bowl First"
    return render_template('display.html', message = message, val = int(val))

@app.route('/bat')
def bat(): 
    import cv2
    import mediapipe
    import numpy as np
    import random
    import time
    from pymongo import MongoClient

    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydb']
    collection = db['mycollection']
    pipeline = [
        {
            '$group': {
                '_id': None,
                'max_data1': {'$max': '$player'},
                'max_data2': {'$max': '$computer'}
            }
        }
    ]

    result = list(collection.aggregate(pipeline))
    highscore = max(result[0]['max_data1'],result[0]['max_data2'])
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
        return landmarkList

    def fingers(landmarks):
        fingerTips = 0
        tipIds = [4, 8, 12, 16, 20]

        # Check if thumb is up
        if landmarks[tipIds[0]][1] > landmarks[tipIds[0] - 1][1]:
            fingerTips += 1

        for id in range(1, 5):
            if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
                fingerTips += 1

        return fingerTips

    flag , computer , player , sleep , bowl , autoBat ,  bat , autoBowl = 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0

    data = "Lost ):" 
    while True:

        ret, img = cap.read()
        if not ret:
            break
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = mainHand.process(imgRGB)

        if results.multi_hand_landmarks:
            if sleep % 30 == 0 : 
                sleep = 0
                lmList = handLandmarks(imgRGB)
                if len(lmList) != 0:
                    finger = fingers(lmList)
                    bowl = finger
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
            time.sleep(10)
            break
        if cv2.waitKey(1) == ord('q'):
            break

    flag = 0

    while True:

        ret, img = cap.read()
        if not ret:
            break
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = mainHand.process(imgRGB)

        if results.multi_hand_landmarks:
            if sleep % 30 == 0 : 
                sleep = 0
                lmList = handLandmarks(imgRGB)
                if len(lmList) != 0:

                    finger = fingers(lmList)
                    bat = finger
                    
                    # Match 
                    autoBowl = random.randint(0,5)
                    
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
            time.sleep(10)
            break

        if player >= computer :
            data = "Match tied !"
            if player > computer :
                data = "Won (:"
                break 
        if cv2.waitKey(1) == ord('q'):
            break

    while True :
        ret, img = cap.read()
        if not ret:
            break
        cv2.putText(img, f"Result : {data}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Hand Detection', img)
        if cv2.waitKey(1) == ord('q'):
            break
        time.sleep(15)
        break

    cap.release()
    cv2.destroyAllWindows()
    collection.insert_one({'player':player,'computer':computer})
    differenceRun = abs(player - computer)
    if data == "Match tied !" :
        resultOfMatch = "Match Tied between Player and Computer"
    elif data == "Won (:":
        resultOfMatch = "Player won Computer by "
    else :
        resultOfMatch = "Computer won player by "
    return render_template('scoreboard.html',message = message , data = resultOfMatch ,differenceRun = differenceRun , player = player , computer = computer)

@app.route('/bowl')
def bowl():
    return redirect(url_for('bat'))

@app.route('/profile')
def profile():

    userNameProfile = db.users.find_one({'username': currUser})
    email = userNameProfile['email']
    
    return render_template('profile.html', username = currUser, email = email)


if __name__ == '__main__':
    app.run()



"""