# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'student.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(508, 422)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 471, 331))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.show_time_label = QLabel(self.layoutWidget)
        self.show_time_label.setObjectName(u"show_time_label")

        self.gridLayout.addWidget(self.show_time_label, 10, 4, 1, 1)

        self.name_inp = QLineEdit(self.layoutWidget)
        self.name_inp.setObjectName(u"name_inp")

        self.gridLayout.addWidget(self.name_inp, 3, 4, 1, 1)

        self.msg = QLabel(self.layoutWidget)
        self.msg.setObjectName(u"msg")
        self.msg.setMaximumSize(QSize(36, 16777215))

        self.gridLayout.addWidget(self.msg, 10, 0, 1, 1)

        self.stu_name_label = QLabel(self.layoutWidget)
        self.stu_name_label.setObjectName(u"stu_name_label")

        self.gridLayout.addWidget(self.stu_name_label, 2, 4, 1, 1)

        self.sign_button = QPushButton(self.layoutWidget)
        self.sign_button.setObjectName(u"sign_button")

        self.gridLayout.addWidget(self.sign_button, 11, 2, 1, 3)

        self.camera_label = QLabel(self.layoutWidget)
        self.camera_label.setObjectName(u"camera_label")
        self.camera_label.setMinimumSize(QSize(271, 0))
        self.camera_label.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.camera_label, 0, 0, 4, 3, Qt.AlignHCenter)

        self.file_select_b = QPushButton(self.layoutWidget)
        self.file_select_b.setObjectName(u"file_select_b")
        self.file_select_b.setStyleSheet(u"")

        self.gridLayout.addWidget(self.file_select_b, 7, 4, 1, 1)

        self.file_path = QLabel(self.layoutWidget)
        self.file_path.setObjectName(u"file_path")

        self.gridLayout.addWidget(self.file_path, 7, 0, 1, 3)

        self.stu_num_label = QLabel(self.layoutWidget)
        self.stu_num_label.setObjectName(u"stu_num_label")

        self.gridLayout.addWidget(self.stu_num_label, 0, 4, 1, 1)

        self.show_msg = QLabel(self.layoutWidget)
        self.show_msg.setObjectName(u"show_msg")

        self.gridLayout.addWidget(self.show_msg, 10, 1, 1, 2)

        self.time_last_label = QLabel(self.layoutWidget)
        self.time_last_label.setObjectName(u"time_last_label")

        self.gridLayout.addWidget(self.time_last_label, 10, 3, 1, 1)

        self.num_inp = QLineEdit(self.layoutWidget)
        self.num_inp.setObjectName(u"num_inp")

        self.gridLayout.addWidget(self.num_inp, 1, 4, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 508, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5b66\u751f\u7b7e\u5230\u7cfb\u7edf", None))
        self.show_time_label.setText("")
        self.name_inp.setText("")
        self.msg.setText(QCoreApplication.translate("MainWindow", u"\u4fe1\u606f\uff1a", None))
        self.stu_name_label.setText(QCoreApplication.translate("MainWindow", u"\u59d3\u540d\uff1a", None))
        self.sign_button.setText(QCoreApplication.translate("MainWindow", u"\u7b7e\u5230", None))
        self.camera_label.setText(QCoreApplication.translate("MainWindow", u"          \u6444\u50cf\u5934\u51c6\u5907\u4e2d       ", None))
        self.file_select_b.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u9009\u62e9", None))
        self.file_path.setText("")
        self.stu_num_label.setText(QCoreApplication.translate("MainWindow", u"\u5b66\u53f7\uff1a", None))
        self.show_msg.setText("")
        self.time_last_label.setText(QCoreApplication.translate("MainWindow", u"\u5269\u4f59\u65f6\u95f4\uff1a", None))
        self.num_inp.setText("")
    # retranslateUi

