# Oyster weight collector
This project tried to predict a oyster meat content, and this maybe make some store cost down.
That's why I start this project.
## How to use this project
First, you need to create a 'MySQL' server, and then build a database 'oyster'.
Second,  create a table that contain 'id','up_path','ahead_path','time'
## Then you need to pip some package that we will use
  pip install -r requirement
## Active our server
  python webprocess.py

note : if we have enough data, and then we could start to train our own model.
## Training model as our oyster predictor
  python oyster_detect.py
