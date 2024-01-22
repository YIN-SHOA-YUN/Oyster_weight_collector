from flask import Flask, render_template, Response,request,send_file,send_from_directory
import cv2
import pymysql
from datetime import datetime
import pandas as pd
import os
#import zipfile
from tensorflow import keras
import numpy as np
#以下為自訂義函式庫
import oyster_weights_prediction as oyster
import run_model

file_name = "img.zip"
frame1 = []
frame2 = [] 
weight = 0
picture1_path = "path1"
picture2_path = "path2"
s_img1 = []
s_img2 = []
mnist_model = keras.models.load_model(r'C:\Users\ADSLab\Downloads\data_collect_website\data_collect_website\remakeModel.h5')
oyster_model = oyster.Load_model()
app = Flask(__name__)
camera = cv2.VideoCapture(0)
camera.set(3,160)
camera.set(4,120)
camera2 = cv2.VideoCapture(1)#"1.avi")#1

camera2.set(3,160)
camera2.set(4,120)
oyster_weight=""
weight_prediction = ""

def zip_dir(path):
    zf = zipfile.ZipFile('{}.zip'.format(path), 'w', zipfile.ZIP_DEFLATED)
   
    for root, dirs, files in os.walk(path):
        for file_name in files:
            zf.write(os.path.join(root, file_name))

def get_mysql_data(sql):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        db='oyster',
        charset='utf8',
        port=3306
    )
    cur = conn.cursor() 
    sql_select = sql 
    cur.execute(sql_select)
    result = cur.fetchall()
    col_result = cur.description  # 獲取查詢結果的欄位描述
    columns = []
    for i in range(len(col_result)):
        columns.append(col_result[i][0])  # 獲取欄位名，以列表形式儲存
    df = pd.DataFrame(columns=columns)
    for i in range(len(result)):
        df.loc[i] = list(result[i])  # 按行插入查詢到的資料
    conn.close()  # 關閉資料庫連線
    return df


# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

def gen_frames():  
    global frame1
    while True:
        success, frame1 = camera.read()
        if not success:
            break
        else:
            frame1= cv2.resize(frame1,(640,480))
            ret, buffer1 = cv2.imencode('.jpg', frame1)
            
            frame = buffer1.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_frames2():  
    global frame2
    while True:
        #


        #
        success, frame2 = camera2.read()  # read the camera frame
        if not success:
            camera2.set(cv2.CAP_PROP_POS_AVI_RATIO,0)

            continue
        else:
            frame2= cv2.resize(frame2,(640,480))
            #frame2 = run_model.img_preprocessing(frame2)
            
            ret, buffer2 = cv2.imencode('.jpg', frame2)
            
            frame = buffer2.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')

#按下擷取當前串流的圖像
@app.route('/get_weight/img', methods=['GET', 'POST'])
def get_weight():
    global weight,picture1_path,picture2_path,frame1,frame2,file_name,s_img1,s_img2,oyster_weight,weight_prediction
    #  利用request取得使用者端傳來的方法為何
    if request.method == 'POST':
        if request.values['send']=='send':
        #利用request取得表單欄位值
            weight =  request.values.get("weight")

            p1 = r"C:\Users\ADSLab\Downloads\data_collect_website\data_collect_website\img\camera1.jpg"
            p2 = r"C:\Users\ADSLab\Downloads\data_collect_website\data_collect_website\img\camera2.jpg"
            saveImg1 = cv2.imwrite(p1,np.array(frame1))
            saveImg2 = cv2.imwrite(p2,np.array(frame2))
            print(weight,len(weight))
            if len(weight)==0:
                num = run_model.digital_recognition(mnist_model=mnist_model,img = p2)
                weight_prediction = oyster_model.predict(oyster.concat_img(p1,p2))
                weight_prediction = weight_prediction[0][0]
                oyster_weight = str(float(num)/10.0)
            else:
                oyster_weight = str(weight)
            s_img1 = frame1
            s_img2 = frame2
            print("提示完成圖像儲存")
            directory = r"C:\Users\ADSLab\Downloads\data_collect_website\data_collect_website\img"
            #with open(os.path.join(directory,"tmp.txt"),'w',encoding='utf-8') as f:
            #    f.write(str(num))
            #zip_dir(os.path.join(directory,"img"))
            print("finished prediction")
            #return send_file(file_name,as_attachment=True),
        elif request.values['send']=='upload':
            sql = "SELECT * FROM   oyster_data ORDER  BY time DESC LIMIT  1;"
            df = get_mysql_data(sql)
            if len(df)!=0:
                pic_id = str(df["id"].values[0] + 1)
            else:
                pic_id = str(0)
            print(df)
            directory_pic = r"C:\Users\ADSLab\Downloads\data_collect_website\data_collect_website\camera1"
            pic_path1 = os.path.join(directory_pic ,pic_id+".jpg")
            directory = r"C:\Users\ADSLab\Downloads\data_collect_website\data_collect_website\camera2"
            pic_path2 = os.path.join(directory ,pic_id+".jpg")
            print("目標路徑","\n",pic_path1,"\n",pic_path2)
            saveImg1 = cv2.imwrite(pic_path1,s_img1)
            saveImg2 = cv2.imwrite(pic_path2,s_img2)
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = []
            data.append((float(weight),pic_path1,pic_path2,time,int(float(pic_id))))
            sql="insert into oyster_data (weight,picture1_path,picture2_path,time,id) values (%s,%s,%s,%s,%s)"
            conn = pymysql.connect(host='127.0.0.1',user='root',password='',db='oyster',charset='utf8',port=3306)
            cur = conn.cursor()
            cur.executemany(sql,data)
            conn.commit()
            conn.close()

        elif request.values['send']=='check':
            sql = "select * from oyster_data ORDER  BY time DESC limit 10"
            df = get_mysql_data(sql)
            print(len(df))
            return df.to_html(classes='data')
        elif request.values['send']=='again':
            oyster_weight = ""
            weight_prediction = ""
            render_template('index.html')
    

    #  非POST的時候就會回傳一個空白的模板
    return render_template('index.html',suggestion = oyster_weight,prediction=weight_prediction)


if __name__ == "__main__":
    app.run(debug=True)