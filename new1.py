# HandCricket

# schedule 0  1 # Computer # Bat        # 2 # Player   # Bowl

# schedule 1  3 # Computer # Bowl       # 4 # Player   # Bat

import random

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

if schedule == 0 :

    innings1 = 0

    while True :
        bowl = int(input("Bowl -----> "))
        if bowl not in range(0,7) :
            print("Bowlcorrectly")
            continue
        autoBat = random.randint(0,6)
        if innings1 >= 200 :
            autoBat = bowl
            break
        if bowl == autoBat :
            print("ComputerOut !")
            break
        print("LastBall run (auto): " , autoBat)
        innings1 += autoBat
        print("LiveScore ",innings1)
        
    print("Target for player : ",innings1)
    target = innings1+1
    print(" * InningsBreak * ")

    # computerBowling
    # PlayerBatting


    innings2 = 0
    while True :
        print("Target : ",target)
        bat = int(input("Bat -----> "))
        if bat not in range(0,7) :
            print("BatCorrectly")
            continue
        autoBowl = random.randint(0,6)
        if bat == autoBowl :
            print("PlayerOut !")
            break
        print("LastBall (auto): ",autoBowl)
        innings2 += bat
        target -= bat
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
        bat = int(input("Bat -----> "))
        if bat not in range(0,7) :
            print("BatCorrectly ")
            continue
        autoBowl = random.randint(0,6)
        if innings1 >= 200 :
            autoBowl = bat
            break
        if bat == autoBowl :
            print("PlayerOut !")
            break
        print("LastBall (auto): " , autoBowl)
        innings1 += bat
        print("LiveScore ",innings1)
        
    print("Target For Computer : ",innings1+1)
    target = innings1+1
    print(" * InningsBreak * ")

    # computerBatting
    # PlayerBowling

    innings2 = 0
    while True :
        print("Target : ",target)
        bowl = int(input("Bowl -----> "))
        if bowl not in range(0,7) :
            print("BowlCorrectly")
            continue
        autoBat = random.randint(0,6)
        if bowl == autoBat :
            print("ComputerOut !")
            break
        print("LastBall run (auto): ",autoBat)
        innings2 += autoBat
        target -= autoBat
        print("Second innings live score : ",innings2)
        if innings2 > innings1 :
            print("ComputerWon !")
            break

    if innings2 == innings1 :
        print("MatchTied")
    elif innings2 < innings1 :
        print("PlayerWon")

"""
while True :
    toss = int(input("SPIN NUMBER (0,1) -> (ODD , EVEN) : "))
    if toss == 0 :
        num = int(input("Enter number : "))
        computer = random.randint(0,15)
        total = num + computer 
        if total % 2 == 0 :
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
    else :
        num = int(input("Enter any number : "))
        computer = random.randint(0,15)
        total = num + computer 
        if total % 2 == 1 :
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
                
                """