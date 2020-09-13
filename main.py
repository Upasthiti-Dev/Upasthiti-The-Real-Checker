from flask import Flask, render_template, Response, request, redirect, url_for
from camera import VideoCamera
import datetime
#from models import run_example
from recognize import verification
import pandas as pd
from speed import get_speed

app = Flask(__name__)
show = False


data = pd.read_csv("data.csv")
student_name = data['Name'].values


# @app.route('/confirm')
# def confirm():
#     return render_template('confirm.html')
@app.route('/')
def redirection():
    print("Testing Speed")
    return redirect('/speed-check')

@app.route('/speed-check')
def speed():
    download_sp = get_speed()
    if download_sp%1000000 >= 2.0:
        print(download_sp%1000000)

        return redirect('/form')
    else:
        return "<h1>Internet Speed Not Optimum!</h1>"

@app.route('/form')
def form():
    return render_template('form.html')

@app.route("/form_check", methods=['POST'])
def name():
    if request.method == 'POST':
        Name = request.form['Name']
        try:
            print(Name)
            if Name in student_name:
                print("Found Name in Data")
                with open("Names.txt", 'w') as f:
                    f.write(Name)
                return redirect(url_for('index'))

            else:
                print("Name not Found")

        except:
            return redirect(url_for('name'))


@app.route('/capture')
def index():
    return render_template('index.html')


def gen(camera):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=10)
    while datetime.datetime.now() < endTime:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    show = True
    verification()


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)