## UCAS 4.5m telescope simple Control program
# This GUI based on QT5
#  ucas4.5m telescope Control program for obs sun
#  PyQt5 GUI
#  @Date 24-03-2018
#  @Author Lei
#
# https://apscheduler.readthedocs.io/en/latest/userguide.html

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import threading
import time
from ucas45mTele import *
import ctypes, sys

from apscheduler.schedulers.background import BackgroundScheduler

import configparser

cf = configparser.ConfigParser()
cf.read('config.ini')

time_start = float(cf.get("time", "time_start"))
time_stop = float(cf.get("time", "time_stop"))

stop_schedule = str(cf.get('schedule', 'stopTele')).split(';')
reset_schedule = str(cf.get('schedule', 'resetTele')).split(';')
trace_schedule = str(cf.get('schedule', 'traceSun')).split(';')

try:
    teleS = sTeleScope()
except Exception as e:
    print(e, flush=True)


class window4_5mGUI(QDialog):
    def setSchedulers(self):
        self.scheduler = BackgroundScheduler()
        for i in stop_schedule: # 配置停止任务的具体时间
            arr = i.split(':')
            self.scheduler.add_job(func=self.stopTele, trigger='cron',
                                   year=arr[0], month=arr[1], day=arr[2],
                                   hour=arr[3], minute=arr[4],second=arr[5])
        for i in reset_schedule:  # 配置重置任务的具体时间
            arr = i.split(':')
            self.scheduler.add_job(func=self.resetTele, trigger='cron',
                                   year=arr[0], month=arr[1], day=arr[2],
                                   hour=arr[3], minute=arr[4],second=arr[5])
        for i in trace_schedule:  # 配置跟踪任务的具体时间
            arr = i.split(':')
            self.scheduler.add_job(func=self.traceSun, trigger='cron',
                                   year=arr[0], month=arr[1], day=arr[2],
                                    hour=arr[3], minute=arr[4],second=arr[5])
        self.scheduler.start() # 计划任务守护进程启动

    def __init__(self, control, parent=None):
        super(window4_5mGUI, self).__init__(parent)

        self.setSchedulers()  # 配置定时计划

        self.cond = threading.Condition()  # a global lock to Control the thread of tracing the Sun
        self.traceFlag = True  # a signal
        self.tracefuncThread = threading.Thread(target=self.tracefunc, daemon=True)
        self.tracefuncThread.start()

        self.createBottomRightGroupBox()
        self.autoConnect()

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Configuration")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        # label .....
        label_AZ = QLabel("HourAngle:")
        label_AZ.setAlignment(Qt.AlignCenter)
        label_EL = QLabel('Declination:')
        label_EL.setAlignment(Qt.AlignCenter)

        # az(ha or others) ,el(or others )display o
        self.az_lcd = QLCDNumber(self.bottomRightGroupBox)
        self.az_lcd.setSegmentStyle(QLCDNumber.Flat)
        # self.az_lcd.setSmallDecimalPoint(True)
        self.az_lcd.setDigitCount(6)
        self.palette_az = self.az_lcd.palette()
        # foreground color
        self.palette_az.setColor(self.palette_az.WindowText, QColor(0, 0, 255))
        # background color
        self.palette_az.setColor(self.palette_az.Background, QColor(0, 170, 255))
        self.az_lcd.setPalette(self.palette_az)
        self.az_lcd.setVisible(True)

        # self.az_lcd.display(141.51)
        # #########################
        self.el_lcd = QLCDNumber(self.bottomRightGroupBox)
        self.el_lcd.setSegmentStyle(QLCDNumber.Flat)
        # self.el_lcd.setSmallDecimalPoint(True)
        self.el_lcd.setDigitCount(6)
        self.palette_el = self.el_lcd.palette()
        # foreground color
        self.palette_el.setColor(self.palette_el.WindowText, QColor(0, 0, 255))
        # background color
        self.palette_el.setColor(self.palette_el.Background, QColor(0, 170, 255))
        self.el_lcd.setPalette(self.palette_el)

        # self.el_lcd.display(12.33)
        self.el_lcd.setVisible(True)

        ## spinbox with label ##############################################

        label_speed = QLabel("Speed")
        label_speed.setAlignment(Qt.AlignCenter)
        # self.delaz_spinBox = QDoubleSpinBox(self.bottomRightGroupBox)
        self.speed_spinBox = QSpinBox(self.bottomRightGroupBox)
        self.speed_spinBox.setValue(1)
        self.speed_spinBox.setMaximum(3)
        self.speed_spinBox.setMinimum(1)

        #  orientation with label ##########################
        label_orien = QLabel("Orientation")
        label_orien.setAlignment(Qt.AlignCenter)

        self.orien = QComboBox()
        # Clockwise
        self.orien.addItem("CW")
        # Counter Clockwise
        self.orien.addItem("CCW")
        self.orien.addItem("UP")
        self.orien.addItem("DOWN")
        self.orien.currentIndexChanged.connect(self.getSOvalue)

        self.configB = QPushButton("MOVE", self)
        self.configB.clicked.connect(self.moveConfig)

        self.stopB = QPushButton("STOP", self)
        self.stopB.clicked.connect(self.stopTele)

        self.traceB = QPushButton("TRACE", self)
        self.traceB.clicked.connect(self.traceSun)

        self.resetB = QPushButton("RESET", self)
        self.resetB.clicked.connect(self.resetTele)

        self.positionB = QPushButton("POSITION", self)
        self.positionB.clicked.connect(self.getPosition)

        layout = QGridLayout()
        layout.setSpacing(15)

        layout.addWidget(label_AZ, 0, 0)
        layout.addWidget(label_EL, 0, 2)

        layout.addWidget(self.az_lcd, 2, 0, 4, 1)
        layout.addWidget(self.el_lcd, 2, 2, 4, 1)

        layout.addWidget(label_speed, 5, 0, 4, 1)
        layout.addWidget(self.speed_spinBox, 7, 0, 4, 1)

        layout.addWidget(label_orien, 5, 2, 4, 1)
        layout.addWidget(self.orien, 7, 2, 4, 1)

        layout.addWidget(self.configB, 11, 0)
        layout.addWidget(self.stopB, 11, 2)
        layout.addWidget(self.traceB, 12, 0)
        layout.addWidget(self.resetB, 12, 2)

        layout.addWidget(self.positionB, 13, 0)

        # layout.addWidget(self.ResetButton, 0, 4)

        layout.setRowStretch(9, 1)

        # add them on layout
        self.bottomRightGroupBox.setLayout(layout)

        self.updateLCD()

        tabWidget = QTabWidget()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QGridLayout()
        mainLayout.addWidget(tabWidget, 1, 0)
        mainLayout.addWidget(buttonBox, 2, 0)

        mainLayout.addWidget(self.bottomRightGroupBox, 0, 0)

        self.setLayout(mainLayout)

        self.setWindowTitle('UCAS 4.5M Telescope')
        self.setWindowIcon(QIcon('sunflower/favicon.ico'))
        # set position and height width
        self.setGeometry(QRect(400, 200, 450, 250))

    #################### functions ###########################
    def autoConnect(self):
        try:
            if teleS.isOpenPort():
                # connected
                if teleS.connectTele():
                    print('telescope is connected')

                else:
                    print('telescope is not connected')
                    self.bottomRightGroupBox.setChecked(False)
        except Exception as e:
            print("autoConnect: ", e, flush=True)

    def startRefresh(self):
        # repeat  sec
        self.timer2.start(2000)

    # get antenna speed and orientation
    def getSOvalue(self):
        speedValue = int(self.speed_spinBox.value())
        orienValue = self.orien.currentText()

        return speedValue, orienValue

    #
    #     for count in range(self.cb.count()):
    #         print self.cb.itemText(count)
    def moveConfig(self):

        speed, ori = self.getSOvalue()
        print('tele move with speed :', speed, ' orientation: ', ori)
        try:
            teleS.commdSpwOr(speed, ori)
        except Exception as e:
            print("[-]moveConfig: ", e, flush=True)

    def stopTele(self):
        self.traceB.setEnabled(True)
        self.resetB.setEnabled(True)
        # self.timer.stop()
        self.traceFlag = True
        try:
            teleS.stopMove()
        except Exception as e:
            print("[-]stop: ", flush=True)
        self.updateLCD()

    def traceSun(self):
        self.resetB.setEnabled(False)
        self.traceB.setEnabled(False)
        self.traceFlag = False
        self.cond.acquire()
        self.cond.notify()
        self.cond.release()
        # self.tracefunc()

    #     teleS.traceToMove()
    # 废弃
    def tracefunc(self):
        '''

        :return:
        '''
        while True:
            ### if traceFlag is True, the tracefunc thread will wait for notification
            if self.traceFlag:
                self.cond.acquire()
                self.cond.wait()
                self.cond.release()
            # print(time.asctime( time.localtime(time.time())))
            try:
                tt = time.localtime(time.time())
                if tt.tm_hour >= time_start and tt.tm_hour <= time_stop:
                    self.updateLCD()
                    teleS.traceSun()
                elif tt.tm_hour > time_stop:
                    print('过了' + str(time_stop) + '点')
                    teleS.resetTele()
                elif tt.tm_hour < time_start:
                    print('没到' + str(time_start) + '点')
                    teleS.resetTele()
            except Exception as e:
                print('[-]tracefunc error: ', e, flush=True)
            finally:
                time.sleep(5)

    def resetTele(self):
        self.traceB.setEnabled(True)
        # self.timer.stop()
        self.traceFlag = True
        try:
            teleS.resetTele()
        except Exception as e:
            print("[-]reset: ", e, flush=True)

    def threadUpLcd(self):
        # threading.Thread(target=self.updateLCD()).start()
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.updateLCD)
        threading.Thread(target=self.startRefresh()).start()

    def updateLCD(self):
        try:
            HA, DEC = teleS.getPosition(isDisp=False)
            # print('HA DEC',HA,DEC)
        except Exception as e:
            print("[-]updateLCD: ", e, flush=True)
            HA, DEC = -1, -1
        # self.az_lcd.display(float(HA))
        # self.el_lcd.display(float(DEC))
        self.az_lcd.display(HA)
        self.el_lcd.display(DEC)

    def getPosition(self):
        try:
            Ha, Dec = teleS.getPosition()
            # spliti recMsg
            # teleHa,teleDec=self.XXX(recMsg)
            # compare with
            SunHa, SunDec = teleS.getSunPosition()
        except Exception as e:
            print("[-]getPosition: ", e, flush=True)
            Ha, Dec = 0, 0
            SunHa, SunDec = 0, 0

    def closeEvent(self, event):
        """
        overwrite the closeEvent method
        :param event: close
        :return: None
        """
        self.stopTele()
        reply = QMessageBox.question(self, 'UCAS 4.5M Telescope', 'Are you sure you want to close the program?  ',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()