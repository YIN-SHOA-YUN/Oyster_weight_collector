from flask import Flask, render_template,request, Response
import time
app = Flask(__name__)

frames = open('1.jpg', 'rb').read()

@app.route('/')
def index():
     print(request.method)
     if request.method == 'POST':
        if request.form['submit_button'] == 'get_frame':
            print('a')
        elif request.form['submit_button'] == 'upload_server':
            print('b')
        else:
            pass
     return render_template('index.html')

def gen_frames():
    while True:
        frame = frames
        print(frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #time.sleep(0.5)

@app.route('/video_feed1')
def video_feed1():
    print(1)
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/contact')
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'get_frame':
            print('a')
        elif request.form['submit_button'] == 'upload_server':
            print('b')
        else:
            pass
    return 0

if __name__ == '__main__':
    app.run()