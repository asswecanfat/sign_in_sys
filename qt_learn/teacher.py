# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'teacher.ui'
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
        MainWindow.resize(835, 541)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(1, 0, 831, 511))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.table_list = QListView(self.layoutWidget)
        self.table_list.setObjectName(u"table_list")
        self.table_list.setMinimumSize(QSize(240, 458))
        self.table_list.setMaximumSize(QSize(240, 458))

        self.horizontalLayout_4.addWidget(self.table_list)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.data_show_widget = QWidget(self.layoutWidget)
        self.data_show_widget.setObjectName(u"data_show_widget")
        self.data_show_widget.setMinimumSize(QSize(570, 300))
        self.data_show_widget.setMaximumSize(QSize(570, 300))

        self.verticalLayout.addWidget(self.data_show_widget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.last_time_label = QLabel(self.layoutWidget)
        self.last_time_label.setObjectName(u"last_time_label")
        font = QFont()
        font.setFamily(u"Bahnschrift")
        font.setPointSize(10)
        font.setItalic(True)
        self.last_time_label.setFont(font)

        self.horizontalLayout.addWidget(self.last_time_label, 0, Qt.AlignRight)

        self.show_time_label = QLabel(self.layoutWidget)
        self.show_time_label.setObjectName(u"show_time_label")

        self.horizontalLayout.addWidget(self.show_time_label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.course_label = QLabel(self.layoutWidget)
        self.course_label.setObjectName(u"course_label")
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(11)
        font1.setItalic(True)
        self.course_label.setFont(font1)

        self.horizontalLayout_6.addWidget(self.course_label)

        self.course_inp_line = QLineEdit(self.layoutWidget)
        self.course_inp_line.setObjectName(u"course_inp_line")
        font2 = QFont()
        font2.setFamily(u"\u534e\u6587\u6977\u4f53")
        font2.setPointSize(12)
        self.course_inp_line.setFont(font2)

        self.horizontalLayout_6.addWidget(self.course_inp_line)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)

        self.timeEdit = QTimeEdit(self.layoutWidget)
        self.timeEdit.setObjectName(u"timeEdit")
        font3 = QFont()
        font3.setFamily(u"Ebrima")
        font3.setPointSize(10)
        self.timeEdit.setFont(font3)
        self.timeEdit.setCurrentSection(QDateTimeEdit.HourSection)

        self.horizontalLayout_7.addWidget(self.timeEdit)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_7)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.msg_label = QLabel(self.layoutWidget)
        self.msg_label.setObjectName(u"msg_label")
        font4 = QFont()
        font4.setFamily(u"\u7b49\u7ebf Light")
        font4.setPointSize(12)
        self.msg_label.setFont(font4)
        self.msg_label.setLayoutDirection(Qt.LeftToRight)
        self.msg_label.setStyleSheet(u"color: rgb(255, 2, 6);")
        self.msg_label.setMargin(0)

        self.horizontalLayout_5.addWidget(self.msg_label)

        self.show_msg_label = QLabel(self.layoutWidget)
        self.show_msg_label.setObjectName(u"show_msg_label")
        self.show_msg_label.setMinimumSize(QSize(420, 0))
        self.show_msg_label.setMaximumSize(QSize(420, 16777215))
        font5 = QFont()
        font5.setFamily(u"Arial")
        font5.setPointSize(12)
        self.show_msg_label.setFont(font5)

        self.horizontalLayout_5.addWidget(self.show_msg_label)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.start_sign_pb = QPushButton(self.layoutWidget)
        self.start_sign_pb.setObjectName(u"start_sign_pb")
        font6 = QFont()
        font6.setFamily(u"\u65b0\u5b8b\u4f53")
        font6.setPointSize(11)
        self.start_sign_pb.setFont(font6)

        self.horizontalLayout_3.addWidget(self.start_sign_pb)

        self.train_model_pb = QPushButton(self.layoutWidget)
        self.train_model_pb.setObjectName(u"train_model_pb")
        font7 = QFont()
        font7.setFamily(u"\u65b0\u5b8b\u4f53")
        font7.setPointSize(12)
        self.train_model_pb.setFont(font7)

        self.horizontalLayout_3.addWidget(self.train_model_pb)

        self.excel_creat_pb = QPushButton(self.layoutWidget)
        self.excel_creat_pb.setObjectName(u"excel_creat_pb")
        self.excel_creat_pb.setFont(font7)

        self.horizontalLayout_3.addWidget(self.excel_creat_pb)

        self.stop_sign_pb = QPushButton(self.layoutWidget)
        self.stop_sign_pb.setObjectName(u"stop_sign_pb")
        self.stop_sign_pb.setFont(font7)
        self.stop_sign_pb.setStyleSheet(u"color: rgb(255, 0, 4);")

        self.horizontalLayout_3.addWidget(self.stop_sign_pb)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 835, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.last_time_label.setText(QCoreApplication.translate("MainWindow", u"\u5269\u4f59\u65f6\u95f4\uff1a", None))
        self.show_time_label.setText("")
        self.course_label.setText(QCoreApplication.translate("MainWindow", u"\u8bfe\u7a0b\u540d\u79f0\uff1a", None))
        self.timeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss", None))
        self.msg_label.setText(QCoreApplication.translate("MainWindow", u"\u4fe1\u606f\uff1a", None))
        self.show_msg_label.setText("")
        self.start_sign_pb.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u7b7e\u5230", None))
        self.train_model_pb.setText(QCoreApplication.translate("MainWindow", u"\u8bad\u7ec3\u6a21\u578b", None))
        self.excel_creat_pb.setText(QCoreApplication.translate("MainWindow", u"\u4e00\u952e\u751f\u6210excel", None))
        self.stop_sign_pb.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u7b7e\u5230", None))
    # retranslateUi

