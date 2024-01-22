import cv2
import numpy as np
import pandas as pd

def readDataBase(sql):
    import pymysql
    conn = pymysql.connect(
        host = '127.0.0.1',
        user = 'root',
        password = '',
        db = 'oyster',
        charset = 'utf-8',
        port = 3306,
    )
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    col_result = cur.description
    columns = []
    for i in range(len(col_result)):
        columns.append(col_result[i][0])
    df = pd.Dataframe(columns = columns)
    for i in range(len(result)):
        df.loc[i] = list(result[i])
    conn.close()
    return df
#read image and contact they
def readFileData(data_path1,data_path2,weight):
    import os
    import pymysql
    data_set = []
    num_files = sum(os.path.isfile(os.path.join(data_path1, f)) for f in os.listdir(data_path1))
    for i in range(num_files):
        pic1 = cv2.imread("path1/"+str(i)+".jpg")
        pic2 = cv2.imread("path2/"+str(i)+".jpg")
        gray1 = cv2.resize(pic1,(320,160))
        gray2 = cv2.resize(pic2,(320,160))
        new_img = cv2.vconcat([gray1, gray2])
        data_set.append(new_img)
    return data_set


sql = ""
df = readDataBase(sql)
path1 = ""
path2 = ""
weight = df["weight"]
text = "" ##weight we predict

def writeData2File(data_set):
    for i in range(len(data_set)):
        cv2.imwrite("path"+str(i)+'.jpg', data_set[i])

pic1 = cv2.imread("/content/darknet/up.jpg") #camera1
pic2 = cv2.imread("/content/darknet/Ahead.jpg") #camera2    

gray1 = cv2.resize(pic1,(320,160))
gray2 = cv2.resize(pic2,(320,160))

new_img = cv2.vconcat([gray1, gray2])
cv2.putText(new_img, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
  1, (0, 255, 255), 1, cv2.LINE_AA)

cv2.imshow(new_img)

cv2.imwrite("00.jpg",new_img)


from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten
import keras

def modelStructure():
    model = Sequential()  
    model.add(Conv2D(64, 3, 3, input_shape = (640, 640, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    # Second convolutional layer
    model.add(Conv2D(32, 3, 3, activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    # Third convolutional layer
    model.add(Conv2D(64, 3, 3, activation = 'relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Flatten())
    model.add(Dense(units = 16))
    model.add(Dense(units = 1))
    return model

model = modelStructure()
model.compile(optimizer = 'adam', loss = keras.losses.MeanSquaredError(),metrics=[keras.metrics.MeanAbsoluteError()])

from keras.preprocessing.image import ImageDataGenerator
#圖像歸一化
train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
test_datagen = ImageDataGenerator(rescale = 1./255)
training_set = train_datagen.flow_from_directory('/content/darknet/training_set', target_size = (640, 640), batch_size = 32, class_mode = 'categorical')
test_set = test_datagen.flow_from_directory('/content/darknet/testing_set', target_size = (640, 640), batch_size = 32, class_mode = 'categorical')
model.fit(training_set,batch_size=  1, epochs = 30,validation_data = test_set, validation_steps = 1,verbose=1,)#,

