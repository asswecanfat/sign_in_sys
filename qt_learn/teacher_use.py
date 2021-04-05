import sys
import datetime
import requests
import json
from typing import DefaultDict

from PySide2 import QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QMenu, QAction
from PySide2.QtCore import QThread, Signal, QTimer, QStringListModel, Qt, QPoint
from PySide2.QtGui import QColor, QCursor
from PySide2.QtCharts import QtCharts

from teacher import Ui_MainWindow as TMainWindow


class Get_Time(QThread):
    count_start = Signal(int)

    def __init__(self, parent):
        super(Get_Time, self).__init__()
        self.setParent(parent)

    def run(self) -> None:
        try:
            time = requests.get("http://127.0.0.1:8000/get_time", timeout=1)
            sec = time.json()
        except requests.exceptions.ConnectionError:
            self.count_start.emit(0)
        else:
            self.count_start.emit(int(sec['second']))


class Table_List_Get(QThread):
    table_list = Signal(list)

    def __init__(self, parent):
        super(Table_List_Get, self).__init__()
        self.setParent(parent)

    def run(self) -> None:
        try:
            raw_data = requests.get('http://127.0.0.1:8000/table_list_get')
            print(raw_data.text)
            temp = raw_data.json()
        except requests.exceptions.ConnectionError:
            self.table_list.emit([])
        else:
            self.table_list.emit(temp['detail'])


class Table_Data_Get(QThread):
    axis_x = Signal(list)
    axis_y = Signal(list)

    def __init__(self, parent):
        super(Table_Data_Get, self).__init__()
        self.setParent(parent)
        parent.table_index.connect(self.deal)
        self.table_index = 0

    def run(self) -> None:
        try:
            result = requests.get('http://127.0.0.1:8000/get_table_data',
                                  params={'table_index': self.table_index})
            data = result.json()
        except requests.exceptions.ConnectionError:
            pass
        else:
            raw_data: DefaultDict[int] = data.get('axis', {})
            self.axis_x.emit(list(raw_data.keys()))
            self.axis_y.emit(list(raw_data.values()))

    def deal(self, t_index):
        self.table_index = t_index
        self.start()


class Stop_Sign_IN(QThread):
    res_msg = Signal(str)

    def __init__(self, parent):
        super(Stop_Sign_IN, self).__init__()
        self.setParent(parent)

    def run(self) -> None:
        try:
            response = requests.post('http://127.0.0.1:8000/stop_signIn')
            msg = response.json()
        except requests.exceptions.ConnectionError:
            pass
        else:
            self.res_msg.emit(msg.get('detail', '未知错误'))


class Start_Sign_IN(QThread):
    sign_msg = Signal(str)
    sign_pb_disable = Signal(bool)
    table_list_refresh = Signal()

    def __init__(self, parent):
        super(Start_Sign_IN, self).__init__()
        self.setParent(parent)
        self.parent = parent

        self.hour = 0
        self.minute = 0
        self.second = 0
        self.course = None
        self.parent.time_data.connect(self.get_time_data)

    def run(self) -> None:
        self.sign_pb_disable.emit(True)
        if self.second + self.minute + self.hour:
            data = json.dumps({"time": {
                "seconds": self.second,
                "minutes": self.minute,
                "hours": self.hour
            },
                "course": self.course})
            res = dict()
            try:
                response = requests.post('http://127.0.0.1:8000/start_signIn',
                                         data=data,
                                         timeout=1)
                res = response.json()
            except requests.exceptions.ConnectionError:
                self.sign_msg.emit('签到开始失败！')
            else:
                self.sign_msg.emit(res.get('detail', '建表失败'))
            finally:
                self.sign_pb_disable.emit(res.get('status_code', 100) == 200)
                self.table_list_refresh.emit()
        else:
            self.sign_pb_disable.emit(False)
            self.sign_msg.emit('时间之和不可为0！')

    def get_time_data(self, hour, minute, second, course):
        self.hour, self.minute, self.second, self.course = hour, minute, second, course
        self.start()


class Delete_Option(QThread):
    delete_msg = Signal(str)

    def __init__(self, parent):
        super(Delete_Option, self).__init__()
        self.setParent(parent)
        self.table_index = None
        self.parent = parent

    def run(self) -> None:
        try:
            response = requests.get('http://127.0.0.1:8000/delete_table',
                                    params={"table_index": self.parent.table_list.currentIndex().row()})
            res = response.json()
        except requests.exceptions.ConnectionError:
            pass
        else:
            self.delete_msg.emit(res.get('detail', '未知错误'))
            self.parent.get_table_list_thread.start()


class Teacher_OP(QMainWindow, TMainWindow):
    table_index = Signal(int)
    right_menu_table_index = Signal(int)
    time_data = Signal(int, int, int, str)

    def __init__(self):
        super(Teacher_OP, self).__init__()
        self.setupUi(self)
        self.time = 0
        self.num = 0  # 记录上张表的数量

        self.get_time_timer = QTimer(self)

        self.get_table_list_thread = Table_List_Get(self)

        self.count_timer = QTimer(self)

        self.clear_msg_timer = QTimer(self)

        self.list_model = QStringListModel()
        self.table_list.setModel(self.list_model)

        self.get_table_data_thread = Table_Data_Get(self)

        self.start_sign_thread = Start_Sign_IN(self)

        self.stop_sign_thread = Stop_Sign_IN(self)

        self.get_time_thread = Get_Time(self)

        self.delete_table_thread = Delete_Option(self)

        # chart
        self.series = QtCharts.QBarSeries(self)
        self.target_bar = QtCharts.QBarSet('学生数量')
        self.series.append(self.target_bar)

        self.axis_x = QtCharts.QBarCategoryAxis()
        self.axis_x.setLabelsColor(QColor(255, 0, 0))

        self.axis_y = QtCharts.QValueAxis()
        # self.axis_y.setTitleText('人数')

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.series)
        self.chart.setAxisX(self.axis_x, self.series)
        self.chart.setAxisY(self.axis_y, self.series)

        self.qcv = QtCharts.QChartView(self.chart)

        self.init_connect()
        self.set_start_dis_and_set_stop_en(False)

    def init_connect(self):
        layout = QVBoxLayout()
        layout.addWidget(self.qcv)  # 将pw加入到布局中
        self.data_show_widget.setLayout(layout)

        self.count_timer.timeout.connect(self.time_count)
        self.count_timer.start(1000)

        self.clear_msg_timer.timeout.connect(
            lambda: self.show_msg_label.setText(''))
        self.clear_msg_timer.start(3000)

        self.get_time_timer.timeout.connect(self.get_time_thread.start)
        self.get_time_timer.start(1500)

        self.get_table_list_thread.table_list.connect(
            lambda x: self.list_model.setStringList(x))
        self.get_table_list_thread.start()

        self.start_sign_thread.sign_msg.connect(self.set_msg)
        self.start_sign_thread.sign_pb_disable.connect(lambda x: self.start_sign_pb.setDisabled(x))
        self.start_sign_thread.table_list_refresh.connect(self.get_table_list_thread.start)

        self.stop_sign_thread.res_msg.connect(self.set_msg)

        self.get_table_data_thread.axis_x.connect(self.set_axis_x)
        self.get_table_data_thread.axis_y.connect(self.set_axis_y)

        self.get_time_thread.count_start.connect(self.get_time)

        self.delete_table_thread.delete_msg.connect(self.set_msg)

        self.start_sign_pb.clicked.connect(
            lambda: self.time_data.emit(
                self.timeEdit.time().hour(),
                self.timeEdit.time().minute(),
                self.timeEdit.time().second(),
                self.course_inp_line.text()))

        self.stop_sign_pb.clicked.connect(self.stop_sign_thread.start)
        self.stop_sign_pb.clicked.connect(self.stop_sign)

        self.table_list.clicked.connect(self.get_table_index)
        self.table_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_list.customContextMenuRequested[QPoint].connect(self.set_menu)

    def set_menu(self, _):
        delete_option = QMenu()
        delete_option.addAction(QAction("删除", delete_option, triggered=self.delete_table_thread.start))
        delete_option.exec_(QCursor.pos())

    def set_start_dis_and_set_stop_en(self, is_enable):
        self.stop_sign_pb.setDisabled(not is_enable)
        self.start_sign_pb.setDisabled(is_enable)

    def set_axis_x(self, date_list):
        self.axis_x.clear()
        self.axis_x.append(date_list)

    def set_axis_y(self, people_num_list):
        self.target_bar.remove(0, self.num)
        self.axis_y.setRange(0, sum(people_num_list))
        self.target_bar.append(people_num_list)
        self.num = len(people_num_list)

    def set_msg(self, text):
        self.show_msg_label.setText(text)

    def get_table_index(self, index):
        self.table_index.emit(index.row())

    def get_time(self, sec):
        if sec:
            self.count_timer.start(1000)
            self.time = sec
            self.get_time_timer.stop()

    def stop_sign(self):
        self.time = 0

    def time_count(self):
        if self.time:
            self.time -= 1
            self.set_start_dis_and_set_stop_en(True)
        else:
            self.count_timer.stop()
            self.set_start_dis_and_set_stop_en(False)
            self.get_time_timer.start(1500)
        self.show_time_label.setText(
            f'{str(datetime.timedelta(seconds=self.time))}')

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.start_sign_thread.wait()
        self.get_table_data_thread.wait()
        self.get_table_list_thread.wait()
        event.accept()


if __name__ == '__main__':
    app = QApplication()
    t_win = Teacher_OP()
    t_win.show()
    sys.exit(app.exec_())
