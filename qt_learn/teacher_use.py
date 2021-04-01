import sys
import datetime
import requests
from typing import DefaultDict

from PySide2 import QtGui
from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PySide2.QtCore import QThread, Signal, QTimer, QStringListModel
from PySide2.QtGui import QColor
from PySide2.QtCharts import QtCharts
import pyqtgraph as pg

from teacher import Ui_MainWindow as TMainWindow


class Time_Get(QThread):
    second = Signal(int)

    def __init__(self, parent):
        super(Time_Get, self).__init__()
        self.setParent(parent)
        self.parent = parent
        self.ask_for_stop = False
        self.parent.thread_stop.connect(self.get_ask)

    def run(self) -> None:
        while not self.ask_for_stop:
            try:
                time = requests.get("http://127.0.0.1:8000/get_time", timeout=1)
                sec = time.json()
            except requests.exceptions.ConnectionError:
                self.second.emit(0)
            else:
                self.second.emit(int(sec['second']))
            finally:
                self.sleep(1500)

    def get_ask(self, ask):
        self.ask_for_stop = ask


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


class Start_Sign_IN(QThread):
    sign_msg = Signal(str)

    def __init__(self, parent):
        super(Start_Sign_IN, self).__init__()
        self.setParent(parent)
        self.parent = parent

    def run(self) -> None:
        try:
            response = requests.post('http://127.0.0.1:8000/start_signIn',
                                     data={''})
            _ = response.json()
        except requests.exceptions.ConnectionError:
            self.sign_msg.emit('签到开始失败！')
        except ValueError:
            self.sign_msg.emit('请输入课程名称！')
        else:
            self.sign_msg.emit('签到开始成功！')


class Teacher_OP(QMainWindow, TMainWindow):
    thread_stop = Signal(bool)
    table_index = Signal(int)

    def __init__(self):
        super(Teacher_OP, self).__init__()
        self.setupUi(self)
        self.time = 0
        self.num = 0  # 记录上张表的数量

        self.get_time_thread = Time_Get(self)

        self.get_table_list_thread = Table_List_Get(self)

        self.count_timer = QTimer(self)

        self.clear_msg_timer = QTimer(self)

        self.list_model = QStringListModel()
        self.table_list.setModel(self.list_model)

        self.get_table_data_thread = Table_Data_Get(self)

        self.start_sign_thread = Start_Sign_IN(self)

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

    def init_connect(self):
        layout = QVBoxLayout()
        layout.addWidget(self.qcv)  # 将pw加入到布局中
        self.data_show_widget.setLayout(layout)

        self.count_timer.timeout.connect(self.time_count)
        self.count_timer.start(1000)

        self.clear_msg_timer.timeout.connect(self.clear_msg)
        self.clear_msg_timer.start(3000)

        self.get_time_thread.second.connect(self.get_time)

        self.get_table_list_thread.table_list.connect(lambda x: self.list_model.setStringList(x))
        self.get_table_list_thread.start()

        self.start_sign_thread.sign_msg.connect(self.show_msg)

        self.get_table_data_thread.axis_x.connect(self.set_axis_x)
        self.get_table_data_thread.axis_y.connect(self.set_axis_y)
        # self.list_model.setStringList([1, 2, 3, 4])

        self.start_sign_pb.clicked.connect(self.start_sign_thread.start)

        self.table_list.clicked.connect(self.get_table_index)

    def set_axis_x(self, date_list):
        self.axis_x.clear()
        self.axis_x.append(date_list)

    def set_axis_y(self, people_num_list):
        self.target_bar.remove(0, self.num)
        self.axis_y.setRange(0, sum(people_num_list))
        self.target_bar.append(people_num_list)
        self.num = len(people_num_list)

    def get_table_index(self, index):
        self.table_index.emit(index.row())

    def get_time(self, time):
        self.time = time

    def time_count(self):
        if self.time:
            self.time -= 1
        self.show_time_label.setText(f'{str(datetime.timedelta(seconds=self.time))}')

    def show_msg(self, string):
        self.show_msg_label.setText(string)

    def clear_msg(self):
        self.show_msg_label.setText('')

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        self.thread_stop.emit(True)
        self.start_sign_thread.wait()
        self.get_table_data_thread.wait()
        self.get_table_list_thread.wait()
        self.get_time_thread.wait()
        event.accept()


if __name__ == '__main__':
    app = QApplication()
    t_win = Teacher_OP()
    t_win.show()
    sys.exit(app.exec_())
