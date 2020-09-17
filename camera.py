import cv2
import time


face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):

        # Detect and Capture Fix
        success, image = self.video.read()
        with open('Names.txt', 'r') as f:
            student_name = f.read()
        cv2.imwrite('captured/'+ student_name +'.jpeg', image)
        image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()