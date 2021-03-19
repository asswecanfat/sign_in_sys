# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'face_catch.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_widget(object):
    def setupUi(self, widget):
        if not widget.objectName():
            widget.setObjectName(u"widget")
        widget.setEnabled(True)
        widget.resize(400, 400)
        widget.setMinimumSize(QSize(400, 400))
        widget.setMaximumSize(QSize(400, 400))
        self.label = QLabel(widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 30, 321, 261))
        self.pushButton = QPushButton(widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(160, 340, 75, 24))
        self.pushButton.setStyleSheet(u"font: 9pt \"Microsoft Tai Le\";")
        self.label_2 = QLabel(widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(110, 310, 181, 16))

        self.retranslateUi(widget)

        QMetaObject.connectSlotsByName(widget)
    # setupUi

    def retranslateUi(self, widget):
        widget.setWindowTitle(QCoreApplication.translate("widget", u"\u9762\u90e8\u622a\u53d6", None))
        self.label.setText(QCoreApplication.translate("widget", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("widget", u"\u622a\u53d6", None))
        self.label_2.setText("")
    # retranslateUi

