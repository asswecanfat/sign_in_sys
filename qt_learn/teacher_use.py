import sys
import datetime
import requests
import json

from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PySide2.QtCore import QThread, Signal, QTimer, QStringListModel
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
            temp = raw_data.json()
        except requests.exceptions.ConnectionError:
            self.table_list.emit([])
        else:
            self.table_list.emit(temp['detail'])


class Teacher_OP(QMainWindow, TMainWindow):
    thread_stop = Signal(bool)

    def __init__(self):
        super(Teacher_OP, self).__init__()
        self.setupUi(self)
        self.time = 0

        self.get_time_thread = Time_Get(self)

        self.get_table_list_thread = Table_List_Get(self)

        self.count_timer = QTimer(self)

        self.list_model = QStringListModel()
        self.table_list.setModel(self.list_model)

        self.init_connect()

    def init_connect(self):
        pw = pg.PlotWidget()
        data = [1, 2, 3]
        pw.plot(data)

        layout = QVBoxLayout()
        layout.addWidget(pw)  # 将pw加入到布局中
        self.data_show_widget.setLayout(layout)

        self.count_timer.timeout.connect(self.time_count)
        self.count_timer.start(1000)

        self.get_time_thread.second.connect(self.get_time)

        self.get_table_list_thread.table_list.connect(lambda x: self.list_model.setStringList(x))
        self.get_table_list_thread.start()

    def get_time(self, time):
        self.time = time

    def time_count(self):
        if self.time:
            self.time -= 1
        self.show_time_label.setText(f'{str(datetime.timedelta(seconds=self.time))}')


if __name__ == '__main__':
    app = QApplication()
    t_win = Teacher_OP()
    t_win.show()
    sys.exit(app.exec_())
