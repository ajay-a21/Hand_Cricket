#python app.py
from flask import Flask, render_template, request
from keras.applications import ResNet50
import cv2
import numpy as np
import pandas as pd
import random

app = Flask(_name_)

resnet = ResNet50(weights='imagenet', input_shape=(224, 224, 3), pooling='avg')

print("+" * 50, "Model is loaded")

labels = pd.read_csv("labels.txt").values


@app.route('/')

def index():
    return render_template("index.html", data="hey")


@app.route("/prediction", methods=["POST"])
def prediction():
    val = int(request.form['number'])

    pred = ""
    computerBat = val
    playerBat = 1

    if computerBat == 1:
        print("Computer Batting First:")
        cBat = 7
        print("Computer Bowling:")
        pBat = 8

        if cBat > pBat:
            pred = "Computer Won the Match!"
            print("Computer Won the Match!")
        else:
            pred = "You Won!"
            print("You won!")

    elif playerBat == 1:
        print("Player Batting First")
        # pBat = bat(0)
        print("Player Bowling")
        # cBat = bat(0)

        if pBat > cBat:
            pred = "You Won!"
            print("You won!")
        else:
            pred = "Computer Won the Match!"
            print("Computer Won the Match!")

    return render_template("prediction.html", data=pred)


if _name_ == "_main_":
    app.run(debug=True)