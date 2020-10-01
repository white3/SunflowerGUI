# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ori_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from sunflower.control import control
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLCDNumber


class window(object):
    def setupUi(self, Form):
        Form.setObjectName("UCAS 4.5M Telescope")
        Form.resize(517, 526)
        Form.setStyleSheet("*{\n"
                           "font-size:14px;\n"
                           "font-family:sans-serif;\n"
                           "}\n"
                           "QFrame{\n"
                           "background:#fdfdfd;\n"
                           "border-radius:6px;\n"
                           "color:#757575;\n"
                           "}\n"
                           "QPushButton{\n"
                           "background:#03a9f4;\n"
                           "color:#fff;\n"
                           "border-radius:6px;\n"
                           "}\n"
                           "QLineEdit{\n"
                           "border-radius:6px;\n"
                           "color:#03a9f4;\n"
                           "}\n"
                           "QLCDNumber{\n"
                           "border: 2px solid #707070;\n"
                           "}\n"
                           "")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 10, 501, 511))
        self.frame.setMinimumSize(QtCore.QSize(501, 411))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(90, 30, 91, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(330, 30, 101, 20))
        self.label_2.setObjectName("label_2")
        self.haLcdNumber = QtWidgets.QLCDNumber(self.frame)
        self.haLcdNumber.setGeometry(QtCore.QRect(20, 60, 211, 51))
        self.haLcdNumber.setObjectName("haLcdNumber")
        self.decLcdNumber = QtWidgets.QLCDNumber(self.frame)
        self.decLcdNumber.setGeometry(QtCore.QRect(270, 60, 211, 51))
        self.decLcdNumber.setObjectName("decLcdNumber")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(100, 230, 91, 21))
        self.label_3.setObjectName("label_3")
        self.oriComboBox = QtWidgets.QComboBox(self.frame)
        self.oriComboBox.setGeometry(QtCore.QRect(270, 270, 211, 31))
        self.oriComboBox.setObjectName("OriComboBox")
        self.moveButton = QtWidgets.QPushButton(self.frame)
        self.moveButton.setGeometry(QtCore.QRect(20, 330, 211, 41))
        self.moveButton.setObjectName("moveButton")
        self.traceButton = QtWidgets.QPushButton(self.frame)
        self.traceButton.setGeometry(QtCore.QRect(20, 390, 211, 41))
        self.traceButton.setObjectName("traceButton")
        self.stopButton = QtWidgets.QPushButton(self.frame)
        self.stopButton.setGeometry(QtCore.QRect(270, 330, 211, 41))
        self.stopButton.setObjectName("stopButton")
        self.resetButton = QtWidgets.QPushButton(self.frame)
        self.resetButton.setGeometry(QtCore.QRect(270, 390, 211, 41))
        self.resetButton.setObjectName("resetButton")
        self.positionButton = QtWidgets.QPushButton(self.frame)
        self.positionButton.setGeometry(QtCore.QRect(20, 450, 211, 41))
        self.positionButton.setObjectName("positionButton")
        self.debugButton = QtWidgets.QPushButton(self.frame)
        self.debugButton.setGeometry(QtCore.QRect(270, 450, 211, 41))
        self.debugButton.setObjectName("debugButton")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(340, 230, 91, 21))
        self.label_4.setObjectName("label_4")
        self.speedSpinBox = QtWidgets.QSpinBox(self.frame)
        self.speedSpinBox.setGeometry(QtCore.QRect(20, 270, 211, 31))
        self.speedSpinBox.setObjectName("speedSpinBox")
        self.RALcdNumber = QtWidgets.QLCDNumber(self.frame)
        self.RALcdNumber.setGeometry(QtCore.QRect(20, 160, 211, 51))
        self.RALcdNumber.setObjectName("RALcdNumber")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(80, 130, 101, 21))
        self.label_6.setObjectName("label_6")
        self.StarsComboBox = QtWidgets.QComboBox(self.frame)
        self.StarsComboBox.setGeometry(QtCore.QRect(270, 170, 211, 41))
        self.StarsComboBox.setObjectName("StarsComboBox")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(350, 130, 91, 21))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "HourAngle"))
        self.label_2.setText(_translate("Form", "Declination"))
        self.label_3.setText(_translate("Form", "Speed"))
        self.moveButton.setText(_translate("Form", "MOVE"))
        self.traceButton.setText(_translate("Form", "TRACE"))
        self.stopButton.setText(_translate("Form", "STOP"))
        self.resetButton.setText(_translate("Form", "RESET"))
        self.positionButton.setText(_translate("Form", "POSITION"))
        self.debugButton.setText(_translate("Form", "DEBUG"))
        self.label_4.setText(_translate("Form", "Orientation"))
        self.label_6.setText(_translate("Form", "Right Ascension"))
        self.label_5.setText(_translate("Form", "Target"))

    def setupAction(self, Form, flower):
        self.__setLCDNumberUI(self.haLcdNumber)
        self.__setLCDNumberUI(self.decLcdNumber)
        self.__setLCDNumberUI(self.RALcdNumber)

        # self.OriComboBox
        self.oriComboBox.addItem("CW")
        self.oriComboBox.addItem("CCW")
        self.oriComboBox.addItem("UP")
        self.oriComboBox.addItem("DOWN")
        self.oriComboBox.currentIndexChanged.connect(self.getSpeedAndOriValue)

        # self.speedSpinBox
        self.speedSpinBox.setValue(1)
        self.speedSpinBox.setMaximum(3)
        self.speedSpinBox.setMinimum(1)

        # self.
        self.haLcdNumber.setDigitCount(6)

        # self.moveButton.clicked.connect(flower.moveButton)
        self.traceButton.clicked.connect(flower.traceStar)
        self.stopButton.clicked.connect(flower.stopTrace)
        self.resetButton.clicked.connect(flower.resetTelescope)
        self.positionButton.clicked.connect(flower.getStarPosition)
        self.debugButton.clicked.connect(flower.connectTelescope)

    def getSpeedAndOriValue(self):
        return int(self.speedSpinBox.value()), self.oriComboBox.currentText()

    def __setLCDNumberUI(self, lcdNumber):
        lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        lcdNumber.setDigitCount(6)
        palette = lcdNumber.palette()
        # foreground color
        
        palette.setColor(palette.WindowText, QColor(0, 0, 255))
        # background color
        palette.setColor(palette.Background, QColor(0, 170, 255))
        lcdNumber.setPalette(palette)
        lcdNumber.setVisible(True)

class Ui_DebugGUIForm(object):
    def setupUi(self, DebugGUIForm):
        DebugGUIForm.setObjectName("DebugGUIForm")
        DebugGUIForm.resize(506, 250)
        DebugGUIForm.setStyleSheet("*{\n"
                                   "font-size:14px;\n"
                                   "font-family:sans-serif;\n"
                                   "}\n"
                                   "QFrame{\n"
                                   "background:#fdfdfd;\n"
                                   "border-radius:6px;\n"
                                   "color:#757575;\n"
                                   "}\n"
                                   "QPushButton{\n"
                                   "background:#03a9f4;\n"
                                   "color:#fff;\n"
                                   "border-radius:6px;\n"
                                   "}\n"
                                   "QLineEdit{\n"
                                   "border-radius:6px;\n"
                                   "color:#03a9f4;\n"
                                   "}\n"
                                   "QLCDNumber{\n"
                                   "border: 2px solid #707070;\n"
                                   "}\n"
                                   "")
        self.pushButton_2 = QtWidgets.QPushButton(DebugGUIForm)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 180, 200, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.haLcdNumber = QtWidgets.QLCDNumber(DebugGUIForm)
        self.haLcdNumber.setGeometry(QtCore.QRect(20, 110, 200, 50))
        self.haLcdNumber.setObjectName("haLcdNumber")
        self.pushButton_3 = QtWidgets.QPushButton(DebugGUIForm)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 20, 200, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(DebugGUIForm)
        self.pushButton_4.setGeometry(QtCore.QRect(290, 20, 200, 50))
        self.pushButton_4.setObjectName("pushButton_4")
        self.haLcdNumber_2 = QtWidgets.QLCDNumber(DebugGUIForm)
        self.haLcdNumber_2.setGeometry(QtCore.QRect(290, 110, 200, 50))
        self.haLcdNumber_2.setObjectName("haLcdNumber_2")
        self.pushButton_5 = QtWidgets.QPushButton(DebugGUIForm)
        self.pushButton_5.setGeometry(QtCore.QRect(290, 180, 200, 50))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_7 = QtWidgets.QLabel(DebugGUIForm)
        self.label_7.setGeometry(QtCore.QRect(80, 80, 91, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(DebugGUIForm)
        self.label_8.setGeometry(QtCore.QRect(340, 80, 101, 21))
        self.label_8.setObjectName("label_8")

        self.retranslateUi(DebugGUIForm)
        QtCore.QMetaObject.connectSlotsByName(DebugGUIForm)

    def retranslateUi(self, DebugGUIForm):
        _translate = QtCore.QCoreApplication.translate
        DebugGUIForm.setWindowTitle(_translate("DebugGUIForm", "Form"))
        self.pushButton_2.setText(_translate("DebugGUIForm", "PushButton"))
        self.pushButton_3.setText(_translate("DebugGUIForm", "PushButton"))
        self.pushButton_4.setText(_translate("DebugGUIForm", "PushButton"))
        self.pushButton_5.setText(_translate("DebugGUIForm", "PushButton"))
        self.label_7.setText(_translate("DebugGUIForm", "  RA Offset"))
        self.label_8.setText(_translate("DebugGUIForm", "  DEC Offset"))


class Ui_DebugTerminalForm(object):
    def setupUi(self, DebugTerminalForm):
        DebugTerminalForm.setObjectName("DebugTerminalForm")
        DebugTerminalForm.resize(728, 470)
        DebugTerminalForm.setStyleSheet("*{\n"
                                        "font-size:14px;\n"
                                        "font-family:sans-serif;\n"
                                        "}\n"
                                        "QFrame{\n"
                                        "background:#fdfdfd;\n"
                                        "border-radius:6px;\n"
                                        "color:#757575;\n"
                                        "}\n"
                                        "QPushButton{\n"
                                        "background:#03a9f4;\n"
                                        "color:#fff;\n"
                                        "border-radius:6px;\n"
                                        "}\n"
                                        "QLineEdit{\n"
                                        "border-radius:6px;\n"
                                        "color:#03a9f4;\n"
                                        "}\n"
                                        "QLCDNumber{\n"
                                        "border: 2px solid #707070;\n"
                                        "}\n"
                                        "")
        self.frame = QtWidgets.QFrame(DebugTerminalForm)
        self.frame.setGeometry(QtCore.QRect(10, 10, 701, 451))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(501, 186))
        self.frame.setStyleSheet("")
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.commandFrame = QtWidgets.QFrame(self.frame)
        self.commandFrame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandFrame.sizePolicy().hasHeightForWidth())
        self.commandFrame.setSizePolicy(sizePolicy)
        self.commandFrame.setMinimumSize(QtCore.QSize(0, 26))
        self.commandFrame.setSizeIncrement(QtCore.QSize(0, 0))
        self.commandFrame.setBaseSize(QtCore.QSize(0, 0))
        self.commandFrame.setStyleSheet("background:rgb(217, 255, 255)")
        self.commandFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.commandFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.commandFrame.setObjectName("commandFrame")
        self.CommandLabel = QtWidgets.QLabel(self.commandFrame)
        self.CommandLabel.setGeometry(QtCore.QRect(10, 0, 61, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommandLabel.sizePolicy().hasHeightForWidth())
        self.CommandLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.CommandLabel.setFont(font)
        self.CommandLabel.setStyleSheet("")
        self.CommandLabel.setObjectName("CommandLabel")
        self.lineEdit = QtWidgets.QLineEdit(self.commandFrame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 0, 591, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.commandFrame, 0, QtCore.Qt.AlignTop)
        self.outputScrollArea = QtWidgets.QScrollArea(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputScrollArea.sizePolicy().hasHeightForWidth())
        self.outputScrollArea.setSizePolicy(sizePolicy)
        self.outputScrollArea.setMinimumSize(QtCore.QSize(485, 400))
        self.outputScrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.outputScrollArea.setStyleSheet("")
        self.outputScrollArea.setWidgetResizable(True)
        self.outputScrollArea.setObjectName("outputScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 683, 401))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_1.setMinimumSize(QtCore.QSize(0, 20))
        self.label_1.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_1.setObjectName("label_1")
        self.verticalLayout_2.addWidget(self.label_1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setMinimumSize(QtCore.QSize(0, 20))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.outputScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.outputScrollArea)

        self.retranslateUi(DebugTerminalForm)
        QtCore.QMetaObject.connectSlotsByName(DebugTerminalForm)

    def retranslateUi(self, DebugTerminalForm):
        _translate = QtCore.QCoreApplication.translate
        DebugTerminalForm.setWindowTitle(_translate("DebugTerminalForm", "Form"))
        self.CommandLabel.setText(_translate("DebugTerminalForm", "UCAS >> "))
        self.lineEdit.setText(_translate("DebugTerminalForm", "Input the command"))
        self.label_1.setText(_translate("DebugTerminalForm", "ucas >> ！！！"))
        self.label_2.setText(_translate("DebugTerminalForm", "ucas >> Welcome"))
        self.label_3.setText(_translate("DebugTerminalForm", "ucas >> To"))
        self.label_4.setText(_translate("DebugTerminalForm", "ucas >> The"))
        self.label_5.setText(_translate("DebugTerminalForm", "ucas >> SunFlower"))
        self.label_6.setText(_translate("DebugTerminalForm", "ucas >> ！！！"))
