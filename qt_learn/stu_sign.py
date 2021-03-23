import sys
import requests
import datetime

import cv2
import numpy as np
from PySide2.QtCore import QTimer, Signal, QThread
from PySide2.QtGui import QImage, QPixmap, QCloseEvent
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog

from student import Ui_MainWindow as Stu_UI


class ValueNoneException(Exception):
    pass


class Prepare_Camera_and_Data_Verify(QThread):
    pic = Signal(QImage)
    collect_msg = Signal(str)
    start_sign = Signal()
    button_close = Signal(bool)
    mean_face_data = Signal(np.ndarray)

    def __init__(self, parent):
        super(Prepare_Camera_and_Data_Verify, self).__init__()
        self.capture = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.parent_is_close = False

        self.parent = parent
        self.parent.is_close.connect(self.get_is_close)

        self.frame = []

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.parent.camera_label.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.parent.camera_label.height())

    def run(self) -> None:
        try:
            if self.parent.pic is None:
                raise ValueNoneException('文件不存在')
            if not self.parent.num_inp.text():
                raise ValueNoneException('学号未输入')
            if not self.parent.name_inp.text():
                raise ValueNoneException('名字未输入')
            self.camera_verify()
        except ValueNoneException as e:
            self.collect_msg.emit(str(e))

    def camera_verify(self):
        self.button_close.emit(True)
        frame_list = []
        while not self.parent_is_close and len(frame_list) < 20:
            _, face = self.capture.read()
            frame_list.append(face)
            frame = cv2.flip(cv2.cvtColor(face, cv2.COLOR_RGB2BGR), 1)
            image = QImage(frame, frame.shape[1], frame.shape[0],
                           frame.strides[0], QImage.Format_RGB888)
            self.pic.emit(image)
            self.collect_msg.emit(f'正在收集第{len(frame_list)}张图片')
            self.msleep(100)
        self.collect_msg.emit('收集完成，处理中。。。')
        self.mean_face_data.emit(self.__load_face(frame_list).reshape((100, 100)))
        self.start_sign.emit()

    def __load_face(self, face_list):
        face = np.zeros((1 * 20, 100 * 100))
        for num, frame in enumerate(face_list):
            # 读取图片并进行矢量化,构成训练集
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_detected = self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            try:
                x, y, w, h = frame_detected[0]
            except IndexError:
                pass
            else:
                face[num, :] = self.__img2vector(gray[y:y + h, x:x + w])
        return np.mean(face, axis=0)

    def __img2vector(self, image):
        """
            读取图片并转换为一维向量

            :param image:图片
            :return:一维向量
            """
        img = cv2.resize(image, (100, 100), )  # 读取图片并重设大小
        rows, cols = img.shape  # 获取图片的像素
        # img_vector = np.zeros((1, rows * cols))  # 初始值均设置为0，大小就是图片像素的大小
        img_vector = np.reshape(img, (1, rows * cols))  # 使用imgVector变量作为一个向量存储图片矢量化信息
        return img_vector

    def get_is_close(self, is_close):
        self.parent_is_close = is_close

    def __del__(self):
        self.capture.release()
        self.wait()


class Sign_In(QThread):
    sign_msg = Signal(str)
    button_close = Signal(bool)

    def __init__(self, parent, friend):
        super(Sign_In, self).__init__()
        self.parent = parent
        self.friend = friend

        self.friend.start_sign.connect(self.start)
        self.friend.mean_face_data.connect(self.get_face_data)
        self.face_data = None

    def run(self) -> None:
        try:
            with open(self.parent.pic, 'rb') as f:
                msg = requests.post("http://127.0.0.1:8000/stu_msg_upload",
                                    data={'stu_name': (None, self.parent.name_inp.text()),
                                          'stu_id': (None, self.parent.num_inp.text()),
                                          'face': (None, self.face_data)},
                                    files={'pic': f})
                data = dict(msg.json())
                if isinstance(new_msg := data['detail'], str):
                    self.sign_msg.emit(new_msg)
                else:
                    print(new_msg)
                    self.sign_msg.emit('数据缺失')
            self.button_close.emit(False)
        except requests.exceptions.ConnectionError:
            self.sign_msg.emit('签到未开始！')

    def get_face_data(self, face_data):
        self.face_data = face_data.tobytes()


class Get_Time(QThread):
    sec = Signal(int)

    def __init__(self, parent):
        super(Get_Time, self).__init__()
        self.parent = parent
        self.parent_is_close = False
        self.parent.is_close.connect(self.get_is_close)

    def run(self) -> None:
        while not self.parent_is_close:
            try:
                time = requests.get("http://127.0.0.1:8000/get_time", timeout=1)
                s = time.json()
            except requests.exceptions.ConnectionError:
                self.sec.emit(0)
            else:
                self.sec.emit(int(s['second']))
            finally:
                self.msleep(1500)

    def get_is_close(self, is_close):
        self.parent_is_close = is_close


class SignUI(QMainWindow, Stu_UI):
    is_close = Signal(bool)
    face_verify = Signal()

    def __init__(self):
        super(SignUI, self).__init__()
        self.setupUi(self)
        self.is_close.emit(False)

        self.pic = None

        self.camera_thread = Prepare_Camera_and_Data_Verify(self)
        self.camera_thread.setParent(self)
        self.camera_thread.pic.connect(self.show_pic)
        self.camera_thread.collect_msg.connect(self.show_msge)
        self.camera_thread.button_close.connect(self.disable_sign_button)

        self.sign_thread = Sign_In(self, self.camera_thread)
        self.sign_thread.setParent(self)
        self.sign_thread.sign_msg.connect(self.show_msge)
        self.sign_thread.button_close.connect(self.disable_sign_button)

        self.get_time_thread = Get_Time(self)
        self.get_time_thread.setParent(self)
        self.get_time_thread.sec.connect(self.set_time)
        self.get_time_thread.start()

        self.clear_text_timer = QTimer(self)
        self.count_time = QTimer(self)
        self.second = 0
        self.init_connect()

    def show_pic(self, image):
        self.camera_label.setPixmap(QPixmap.fromImage(image))

    def show_msge(self, msg):
        self.show_msg.setText(msg)

    def disable_sign_button(self, ready):
        self.sign_button.setDisabled(ready)

    def init_connect(self):

        self.count_time.timeout.connect(self.time_count)
        self.count_time.start(1000)

        self.clear_text_timer.timeout.connect(lambda: self.show_msg.setText(''))
        self.clear_text_timer.start(2000)

        self.sign_button.clicked.connect(lambda: self.camera_thread.start())  # 签到
        self.file_select_b.clicked.connect(self.file_choose)  # 文件

    def set_time(self, sec):
        self.second = sec

    def time_count(self):
        if self.second:
            self.second -= 1
        self.show_time_label.setText(f'{str(datetime.timedelta(seconds=self.second))}')

    def file_choose(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self,
                                                       '打开文件',
                                                       '.',
                                                       "Image files (*.jpg *.png)")
        except BaseException as e:
            self.show_msg.setText(e)
        else:
            self.file_path.setText(file_name)
            self.pic = file_name

    def closeEvent(self, event: QCloseEvent) -> None:
        self.is_close.emit(True)
        self.sign_thread.wait()
        self.get_time_thread.wait()
        self.camera_thread.wait()
        event.accept()


if __name__ == '__main__':
    app = QApplication()
    start = SignUI()
    start.show()
    sys.exit(app.exec_())
