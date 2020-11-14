# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from sunflower.internal.window_ui import Ui_Form
from sunflower.internal.viewer import Viewer
from sunflower.internal.model.target import Target
from sunflower.internal.model.offset import HAOffset, DECOffset
from sunflower.internal.model.times import Times
from sunflower.internal.config import Config
from sunflower.internal.communicator import Communicator
from sunflower.internal.recorder import Recorder
from sunflower.internal.corrector import Corrector
import threading
from time import sleep
from PyQt5.QtCore import QDateTime


class Window(object):
    ui_form = Ui_Form()  # 定义GUI界面
    globalClock = Times()  # 定义全局时钟
    target = Target(name="sun")  # 望远镜目标方位，实时
    currentDirecting = Target(name="current")  # 望远镜指向方位，实时
    targetList = []  # 软件内置目标图，修改即更新

    config = Config()  # 配置文件管理模块

    version = int(config.getValue(section='offset', option='version'))
    haManualCalibrateOffset = HAOffset(ha=target.hourAngle, haOffset=0, version=version)  # 手动校准时角误差
    haFitOffset = HAOffset(ha=target.hourAngle, haOffset=0, version=version)  # 拟合数据的估算时角误差
    haOffset = HAOffset(ha=target.hourAngle, haOffset=0, version=version)  # 时角误差的和

    decManualCalibrateOffset = DECOffset(dec=target.declination, decOffset=0, version=version)  # 手动校准的赤纬误差
    decFitOffset = DECOffset(dec=target.declination, decOffset=0, version=version)  # 拟合数据的估算赤纬误差
    decOffset = DECOffset(dec=target.declination, decOffset=0, version=version)  # 赤纬误差的和

    def __init__(self):
        self.VIEW_FLUSH_TIME = int(self.config.getValue(section="view", option="FLUSH_TIME"))
        self.RECORD_FLUSH_TIME = int(self.config.getValue(section="record", option="FLUSH_TIME"))

        self.isView = True  # 是否启动View, 用于刷新仪表
        self.viewer = Viewer(target=self.target, config=self.config)

        self.isConnect = False  # 是否连接到望远镜, 如果未连接, 则关闭相关模块
        self.communicator = Communicator(comNumber=self.config.getValue(section='serial', option='COM_Number'))

        self.isRecord = False  # 是否开启指向修正
        self.recorder = Recorder()  # 配置记录器
        self.recordThread = None

        self.isCorrect = False  # 是否开启指向修正
        self.corrector = Corrector(recorder=self.recorder)
        self.correctThread = None

    def setupSunflower(self):
        # 定义仪表显示模块
        self.displayStatus(status="setupView")
        self.setupView()

        # 定义望远镜通信模块
        # self.displayStatus(status="setupControl")
        # self.setupControl()

        # 定义望远镜目标模块
        # self.displayStatus(status="setupTarget")
        # self.setupTarget()

        # 定义望远镜目标模块
        self.displayStatus(status="setupCorrect")
        self.correctThread = threading.Thread(target=self.corrector.update, daemon=True)
        self.ui_form.correctButton.clicked.connect(self.setupCorrect)

        # 定义指向误差记录模块
        self.displayStatus(status="setupRecord")
        self.recordThread = threading.Thread(target=self.record, daemon=True)
        self.ui_form.recordButton.clicked.connect(self.setupRecord)

    def setupRecord(self):
        if self.isRecord:
            self.isRecord = False
            self.ui_form.recordButton.setText("RECORD")
        else:
            self.isRecord = True
            self.ui_form.recordButton.setText("OFF-RECORD")

    def record(self):
        """
        以RECORD_FLUSH_TIME为间隙，持续向数据库记录数据
        :return:
        """
        while self.isRecord:
            sleep(self.RECORD_FLUSH_TIME)
            self.recorder.writeData(HAoffset=self.haOffset, DECoffset=self.decOffset, Target=self.target,
                                    globalClock=self.globalClock)

    def setupCorrect(self):
        if self.isCorrect:
            self.isCorrect = False
            self.ui_form.correctButton.setText("CORRECT")
        else:
            while self.correctThread.is_alive():
                sleep(1)
            self.isCorrect = True
            self.ui_form.correctButton.setText("OFF-CORRECT")
            self.correctThread = threading.Thread(target=self.corrector.update, daemon=True)
            self.correctThread.start()

    def setupControl(self):
        """
        配置组件的事件

        Args:
            control ([type]): [description]
        """
        pass

    def control(self):
        """
        俯仰、方位
        :return:
        """
        while self.isConnect:
            sleep(self.VIEW_FLUSH_TIME)
            self.currentDirecting.hourAngle, self.currentDirecting.declination \
                = self.communicator.getPosition()

    def setupTarget(self):
        pass

    def setupView(self):
        """
        启动仪表显示器
        :return:
        """
        updateViewThread = threading.Thread(target=self.view, daemon=True)
        updateViewThread.start()

    def view(self):
        """
        后台运行 时角、赤纬、赤经、时间的计算
        :return:
        """
        while self.isView:
            sleep(self.VIEW_FLUSH_TIME)
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
            self.ui_form.decOffsetLcdNumber.display(self.decOffset.decOffset)
            self.ui_form.haOffsetLcdNumber.display(self.haOffset.haOffset)

            # display telescope position
            self.ui_form.telescopeHALcdNumber.display(self.currentDirecting.hourAngle)
            self.ui_form.telescopeDecLcdNumber.display(self.currentDirecting.declination)

    def displayStatus(self, status, isError=False):
        if isError:
            log = "[-]"
        else:
            log = "[+]"
        log += str(QDateTime.currentDateTime().toTime_t()) + "\t" + status + "\n"
        print(log)
        self.ui_form.statusTextBrowser.append(log)

    def setupUi(self, MainWindow):
        """
        用于加载Ui_Form设计的UI于MainWindow
        :param MainWindow:
        :return:
        """
        self.ui_form.setupUi(MainWindow)
