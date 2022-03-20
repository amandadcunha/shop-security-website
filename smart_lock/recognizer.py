import cv2
import datetime
from iot_project.settings import BASE_DIR
import urllib
import numpy as np

class FaceRecognizer(object):
    def __init__(self):
        #self.url = "http://192.168.43.77:8080/shot.jpg"
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        #cv2.destroyAllWindows()
        self.video.release()
    
    def recognizer(self):
        success, img = self.video.read()
        frame_flip = cv2.flip(img, 1)
        face_cascade = cv2.CascadeClassifier(str(BASE_DIR) + "/smart_lock/ML/data/haarcascade_frontalface_default.xml")
        frame_flip = cv2.flip(img, 1)
        gray = cv2.cvtColor(frame_flip, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            frame_flip = cv2.rectangle(frame_flip, (x, y), (x+w,y+h), (255,0,0), 3)

        date_time = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame_flip = cv2.putText(frame_flip, date_time, (5, 40), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()

class IPWebCam(object):
    def __init__(self):
        self.url = "http://192.168.0.102:8080/shot.jpg"

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        frame_flip = cv2.flip(img, 1)
        face_cascade = cv2.CascadeClassifier(str(BASE_DIR) + "/smart_lock/ML/data/haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(frame_flip, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            frame_flip = cv2.rectangle(frame_flip, (x, y), (x+w,y+h), (255,0,0), 3)

        date_time = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame_flip = cv2.putText(frame_flip, date_time, (10, 100), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()