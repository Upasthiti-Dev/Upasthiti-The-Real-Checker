from flask import Flask, render_template, Response, request, redirect, url_for
from camera import VideoCamera
import datetime
from recognize import verification
import pandas as pd
from speed import get_speed


app = Flask(__name__)

# reading Names in CSV
data = pd.read_csv("data.csv")
student_name = data['Name'].values
retry = 0

# first route
# >>> Redirects to Speed Check
@app.route('/')
def redirection():
    print("Testing Speed")
    return redirect('/speed-check')

# second route
# >>> Calls get_speed function
# >>> Checks for Bandwidth Speed
@app.route('/speed-check')
def speed():
    download_sp = get_speed()
    if download_sp%1000000 >= 2.0 and download_sp!=-1:
        print(download_sp%1000000)
        return redirect('/form')
    else:
        return render_template("error.html")

# third route
# >>> Renders a form for entering Name of Student
@app.route('/form')
def form():
    return render_template('form.html')

# fourth route
# >>> Gets the Name from form
@app.route("/form_check", methods=['POST'])
def name():
    if request.method == 'POST':
        Name = request.form['Name']
        try:
            print(Name)
            if Name in student_name:
                print("Found Name in Data")

                # Dump name in the Text File
                with open("Names.txt", 'w') as f:
                    f.write(Name)
                return redirect(url_for('index'))

            # return to the form page if Name not found
            else:
                print("Name not Found")
                return redirect(url_for('form'))

        # In case of any error return to the SpeedTest
        except:
            return redirect(url_for('redirection'))


# fifth route
# >>> Renders video Capture page
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

# Sixth Route
# >>> Starts Video Feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Run app at Host 0.0.0.0
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)