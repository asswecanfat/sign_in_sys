import sys
from pathlib import Path

import cv2
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtNetwork import QNetworkRequest, QNetworkAccessManager

from face_catch import Ui_widget as DesktopUI


class Face_Get(QMainWindow, DesktopUI):
    def __init__(self):
        super(Face_Get, self).__init__()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.setupUi(self)
        self.label.setText('摄像头载入中。。。')
        # self.__set_camera()
        self.pushButton.clicked.connect(self.network)
        self.frame = None
        self.num = 0
        self.file_path = Path(__file__).parent / Path('face')
        self.nm = QNetworkAccessManager(self)
        self.nm.finished.connect(self.fffff)

    def __set_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.label.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.label.height())
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_pic)
        self.timer.start(30)

    def display_pic(self):
        ret, face = self.capture.read()
        self.frame = face
        frame = cv2.flip(cv2.cvtColor(face, cv2.COLOR_RGB2BGR), 1)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))

    def catch_pic(self):
        frame_detected = self.face_cascade.detectMultiScale(self.frame, scaleFactor=1.1, minNeighbors=5)
        try:
            x, y, w, h = frame_detected[0]
        except IndexError:
            self.label_2.setText('没有检测到人脸')
        else:
            if not self.file_path.exists():
                self.file_path.mkdir()
            cv2.imwrite(f'{str(self.file_path)}/{self.num}.jpg', self.frame[y:y + h, x:x + w])
            self.num += 1
            self.label_2.setText(f"第{self.num}张已生成")

    def network(self):
        url = QUrl("http://127.0.0.1:8000/excel_get")
        res = QNetworkRequest(url)
        self.nm.get(res)

    def fffff(self, reply):
        print(reply.readAll())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = Face_Get()
    f.show()
    sys.exit(app.exec_())
