#!unzip /content/digital_data.zip

import numpy as np
from tensorflow import keras
import cv2
import os
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True
session = tf.compat.v1.InteractiveSession(config=config)

def process(img):
    gray = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    ret, th1 = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    return th1

def img_preprocessing(img_in):
        print(img_in.shape)
        #角度處理，使用homography(單映性矩陣)
        pts_dst = np.float32([[0,0],[640,0],[0,480],[640,480]])
        contours = np.float32([[50,240],[450,250],[0,360],[460,370]])
        frame = cv2.resize(img_in,(640,480),interpolation=cv2.INTER_AREA)
        m = cv2.getPerspectiveTransform(contours,pts_dst)
        frame = cv2.warpPerspective(frame,m,(640,480))


        #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #亮度處理
        l_h = 54
        l_s = 35
        l_v = 82
        u_h = 94
        u_s = 255
        u_v = 121
        lower_red = np.array([l_h,l_s,l_v])
        upper_red = np.array([u_h,u_s,u_v])
        mask = cv2.inRange(hsv,lower_red,upper_red)
        kernel = np.ones((5,5),np.uint8)
        mask2 = cv2.erode(mask,kernel)
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.dilate(mask2,kernel,iterations = 1)
        contours,h = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:
            area = cv2.contourArea(i)
            if area<1300:
                cv2.drawContours(image = mask,contours = [i],contourIdx=-1,color=(0,0,0),thickness=cv2.FILLED)
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.erode(mask,kernel,iterations=1)

        contours,h = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:
            area = cv2.contourArea(i)
            if area<1000:
                cv2.drawContours(image=mask ,contours = [i],contourIdx=-1,color = (255,255,255),thickness=cv2.FILLED)
        mask = np.float32(mask)
        mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
        output_img = mask
        return output_img

def show_img(img):
    image = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    cv2.imshow("frame",image)


def prepare(filepath):
    IMG_SIZE = 28
    IMAGE_CHANNEL = 1 
    img_array = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    #print("prepare finished",new_array)
    return new_array.reshape(-1,IMG_SIZE, IMG_SIZE, IMAGE_CHANNEL)

def digital_recognition(mnist_model,img=r'C:\Users\ADSLab\Downloads\data_collect_website\data_collect_website\digital_data\0\0.jpg'):
    
    print("step1")
    result = mnist_model.predict(prepare(img))
    print("step2")
    classes_x=np.argmax(result,axis=1)
    print("\n final預測結果",classes_x[0])
    return classes_x[0]

#mnist_model = keras.models.load_model('./remakeModel.h5',compile=False)

#num = digital_recognition(mnist_model)
