# Oyster weight collector
This project tried to predict a oyster meat content, and this maybe make some store cost down.
That's why I start this project.

## How to use this project
First, you need to create a `MySQL` server, and then build a database `oyster`.
Second,  create a table that contain `weight`,`up_path`,`ahead_path`,`time`,`id`.
Make sure you have two webcams
Third create three folders `img`,`camera1` and `camera2`, and `img` is used to save two camera's photos(tmp).

## Then you need to pip some package that we will use
    pip install -r requirement
## Active our server
    python webprocess.py

In `webprocess.py` remakeModel.h5 is used to catch the weight that the scale display.
And `oyster.h5` is used to predict the input oyster, before input the oyster image, we need to concate two angle pictures as one, and then sent it into our model. 
note : if we have enough data, and then we could start to train our own model.

## Training model as our oyster predictor
    python oyster_detect.py
