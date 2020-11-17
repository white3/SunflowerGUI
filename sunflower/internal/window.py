# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from sunflower.internal.view.window_ui import Ui_Form
from sunflower.internal.controller.viewer import Viewer
from sunflower.internal.model.target import Target
from sunflower.internal.model.offset import HAOffset, DECOffset
from sunflower.internal.model.times import Times
from sunflower.internal.util.communicator import Communicator
from sunflower.internal.util.recorder import Recorder
from sunflower.internal.controller.corrector import Corrector
from sunflower.internal.controller.control import Keyboard
from sunflower.internal.util import decorator
import threading
from time import sleep
from PyQt5.QtCore import QDateTime
from sunflower.internal.constants import constant
import serial


class Window(object):
    ser = serial.Serial()  # 定义连接的串口
    ui_form = Ui_Form()  # 定义GUI界面
    globalClock = Times()  # 定义全局时钟
    target = Target(name="sun", isInherent=True)  # 望远镜目标方位，实时
    currentDirecting = Target(name="current")  # 望远镜指向方位，实时
    targetList = []  # 软件内置目标图，修改即更新

    haManualCalibrateOffset = HAOffset(ha=target.hourAngle, ha_offset=0, version=constant.version)  # 手动校准时角误差
    haFitOffset = HAOffset(ha=target.hourAngle, ha_offset=0, version=constant.version)  # 拟合数据的估算时角误差
    haOffset = HAOffset(ha=target.hourAngle, ha_offset=0, version=constant.version)  # 时角误差的和

    decManualCalibrateOffset = DECOffset(dec=target.declination, decOffset=0, version=constant.version)  # 手动校准的赤纬误差
    decFitOffset = DECOffset(dec=target.declination, decOffset=0, version=constant.version)  # 拟合数据的估算赤纬误差
    decOffset = DECOffset(dec=target.declination, decOffset=0, version=constant.version)  # 赤纬误差的和

    def __init__(self):
        """
        此时 ui_form 未加载，所以只能初始化与GUI无关的变量
        """
        self.isView = True  # 是否启动View, 用于刷新仪表
        self.viewer = Viewer(target=self.target)

        self.isConnect = False  # 是否连接到望远镜, 如果未连接, 则关闭相关模块
        self.isTrace = False
        self.control = Control(communicator=None, window=None)
        self.telescopePositionThread = None

        self.isRecord = False  # 是否开启指向修正
        self.recorder = Recorder()  # 配置记录器
        self.recordThread = None

        self.isCorrect = False  # 是否开启指向修正
        self.corrector = Corrector(recorder=self.recorder)
        self.correctThread = None

    @decorator.debugLog
    def setupSunflower(self):
        """
        加载完 ui_form 后再执行的函数
        :return:
        """
        self.keyboard = Keyboard(window=self)

        self.ser.baudrate = constant.baudrate
        self.ser.port = constant.port
        self.ui_form.comNumberSpinBox.setProperty("value", constant.port)

        # 定义仪表显示模块
        self.displayStatus(status="setupView", color=constant.MEDIUM)
        self.setupView()

        # 定义望远镜通信模块
        self.displayStatus(status="setupControl", color=constant.MEDIUM)
        self.setupControl()

        # 定义望远镜目标模块
        # self.displayStatus(status="setupTarget", color=constants.MEDIUM)
        # self.setupTarget()

        # 定义望远镜目标模块
        self.displayStatus(status="setupCorrect", color=constant.MEDIUM)
        self.correctThread = threading.Thread(target=self.corrector.update, daemon=True)
        self.ui_form.correctButton.clicked.connect(self.setupCorrect)

        # 定义望远镜目标模块
        self.displayStatus(status="setupKeyboard", color=constant.MEDIUM)
        self.setupKeyboard()

        # 定义指向误差记录模块
        self.displayStatus(status="setupRecord", color=constant.MEDIUM)
        self.ui_form.recordButton.clicked.connect(self.setupRecord)

    def setupKeyboard(self):
        self.ui_form.traceButton.clicked.connect(self.doTrace)
        self.ui_form.comButton.clicked.connect(self.doSerialComConnect)
        self.ui_form.stopButton.clicked.connect(self.doStop)
        self.ui_form.resetButton.clicked.connect(self.doReset)
        # self.ui_form.speedSpinBox.keyPressEvent(e=SpeedKeyEvent()) # .setShortcutEnabled(id=Qt.Key_Q, enabled=True)

    def setupControl(self):
        self.telescopePositionThread = threading.Thread(target=self.doUpdateTelescopePosition, daemon=True)
        try:
            self.communicator = Communicator(serialChannel=self.ser)
            self.control.communicator = self.communicator
        except Exception as e:
            print(e)
            self.displayStatus(status="Failed to connect to serial com", color=constant.HIGH)
        self.control.window = self
        self.isConnect = True
        self.telescopePositionThread.start()

    def doReset(self):
        self.control.reset()

    def doStop(self):
        self.control.stop()

    def doTrace(self):
        if self.isTrace:
            self.isTrace = False
            self.ui_form.traceButton.setText('Trace')
            self.control.stop()
        else:
            self.isTrace = True
            self.ui_form.traceButton.setText('stopTrace')
            self.control.trace()

    def doSerialComConnect(self):
        com = "COM" + str(self.ui_form.comNumberSpinBox.value())
        try:
            self.communicator = Communicator(comNumber=com)
            self.control.communicator = self.communicator
        except Exception as e:
            self.displayStatus(status=e, color=constant.HIGH)
            self.displayStatus(status="Failed to connect to serial com", color=constant.HIGH)

    def doUpdateTelescopePosition(self):
        """
        俯仰、方位
        :return:
        """
        show_failed = True
        while self.isConnect:
            sleep(constant.VIEW_FLUSH_TIME)
            try:
                self.currentDirecting.hourAngle, self.currentDirecting.declination \
                    = self.communicator.getPosition()
                show_failed = True
            except Exception as e:
                if show_failed:
                    self.displayStatus(status=e, color=constant.HIGH)
                    show_failed = False
                self.currentDirecting.hourAngle = 999
                self.currentDirecting.declination = 999

    def setupRecord(self):
        if self.isRecord:
            self.isRecord = False
            self.ui_form.recordButton.setText("RECORD")
        else:
            self.isRecord = True
            self.recordThread = threading.Thread(target=self.doRecord, daemon=True)
            self.recordThread.start()
            self.ui_form.recordButton.setText("OFF-RECORD")

    def doRecord(self):
        """
        以RECORD_FLUSH_TIME为间隙，持续向数据库记录数据
        :return:
        """
        while self.isRecord:
            sleep(constant.RECORD_FLUSH_TIME)
            self.recorder.writeData(haOffset=self.haOffset, decOffset=self.decOffset, target=self.target,
                                    globalClock=self.globalClock)

    @decorator.debugLog
    def setupCorrect(self):
        """
        Correct 事件业务
        :return:
        """
        if self.isCorrect:  # 停止修正
            self.isCorrect = False
            self.ui_form.correctButton.setText("CORRECT")
        else:
            while self.correctThread.is_alive():
                sleep(1)
            self.isCorrect = True
            self.ui_form.correctButton.setText("OFF-CORRECT")
            self.correctThread = threading.Thread(target=self.corrector.update, daemon=True)
            self.correctThread.start()

    def setupTarget(self):
        pass

    def setupView(self):
        """
        启动仪表显示器
        :return:
        """
        updateViewThread = threading.Thread(target=self.doView, daemon=True)
        updateViewThread.start()

    def doView(self):
        """
        后台运行 时角、赤纬、赤经、时间的计算
        :return:
        """
        while self.isView:
            sleep(constant.VIEW_FLUSH_TIME)
            # display target position
            self.target.hourAngle, self.target.declination, self.target.rightAscension, self.globalClock = \
                self.viewer.getViewData()
            self.ui_form.haLcdNumber.display(self.target.hourAngle)
            self.ui_form.decLcdNumber.display(self.target.declination)
            self.ui_form.raLcdNumber.display(self.target.rightAscension)

            # display global time
            self.ui_form.localtimeDateTimeEdit.setDateTime(self.globalClock.toLocalTime())
            self.ui_form.utcDateTimeEdit.setDateTime(self.globalClock.toUTC())
            self.ui_form.lstDateTimeEdit.setDateTime(self.globalClock.toLST())

            # display correction
            self.decOffset = self.decFitOffset + self.decManualCalibrateOffset
            self.haOffset = self.haFitOffset + self.haManualCalibrateOffset
            self.ui_form.decOffsetLcdNumber.display(self.decOffset.decOffset)
            self.ui_form.haOffsetLcdNumber.display(self.haOffset.ha_offset)

            # display telescope position
            self.ui_form.telescopeHALcdNumber.display(self.currentDirecting.hourAngle)
            self.ui_form.telescopeDecLcdNumber.display(self.currentDirecting.declination)

            if not self.ser.is_open:
                self.ui_form.comNumberSpinBox.setStyleSheet("color: rgb(255, 0, 0);border: 2px solid #707070;")

    def getPosition(self):
        """
        返回直接用于望远镜追踪的坐标
        :return:
        """
        return self.haOffset + self.target.hourAngle, self.decOffset + self.target.declination

    def displayStatus(self, status: str, color=constant.LOW):
        """
        LOW = "#000000"
        MEDIUM = "#00aaff"
        HIGH = "#00aaff"
        :param color: 配置状态信息的颜色
        :param status: 需要显示的状态信息
        :return:
        """
        log = "<font color=\"%s\">[+]%d %s</font>" % (color, QDateTime.currentDateTime().toTime_t(), status.__str__())
        self.ui_form.statusTextBrowser.append(log)

    def setupUi(self, MainWindow):
        """
        用于加载Ui_Form设计的UI于MainWindow
        :param MainWindow:
        :return:
        """
        self.ui_form.setupUi(MainWindow)


class Control(object):
    communicator = None  # 通信工具
    window = None  # 数据窗口
    isTracing = threading.Condition()  # a global lock to Control the thread of tracing the Sun
    traceFlag = False  # True表示跟踪, False表示不跟踪
    traceThread = None

    def __init__(self, communicator: Communicator, window: Window):
        self.communicator = communicator
        self.window = window

        self.isTracing = threading.Condition()  # a global lock to Control the thread of tracing the Sun
        self.traceThread = threading.Thread(target=self.doTrace, daemon=True)
        self.traceThread.start()

    def trace(self):
        # self.resetB.setEnabled(False)
        # self.traceB.setEnabled(False)
        self.traceFlag = True
        self.isTracing.acquire()
        self.isTracing.notify()
        self.isTracing.release()

    def stopTrace(self):
        # self.traceB.setEnabled(True)
        # self.resetB.setEnabled(True)
        self.traceFlag = False

    def doTrace(self):
        while True:
            # if traceFlag is True, the doTrace thread will wait for notification
            if not self.traceFlag:
                self.isTracing.acquire()
                self.isTracing.wait()
                self.isTracing.release()
            # tracing
            ha, dec = self.window.getPosition()
            print("tracing %f, %f" % (ha, dec))
            self.communicator.point(ha, dec)

    def drop_power(self):
        self.communicator.drop_power()

    def stop(self):
        self.communicator.stop()

    # def ccw(self):
    #     self.communicator.commdSpwOr(speed=0, orient='ccw')

    def reset(self):
        self.communicator.reset()
