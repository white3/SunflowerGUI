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
from sunflower.internal.config import Config
from sunflower.internal.communicator import Communicator
from sunflower.internal.recorder import Recorder
from sunflower.internal.corrector import Corrector
import threading
from time import sleep
from PyQt5.QtCore import QDateTime


class Window(object):
    currentTarget = Target(name="current")  # 定义追踪目标
    target = Target(name="sun")  # 定义当前指向位置
    ui_form = Ui_Form()  # 定义GUI界面
    config = Config()  # 配置文件管理模块
    """
        self.concurrentData['HAoffset'],    correct带来的差值、control控制带来的差值——时角补偿值
        self.concurrentData['DECoffset']    correct带来的差值、control控制带来的差值——赤纬补偿值
    """

    def __init__(self):
        self.VIEW_FLUSH_TIME = int(self.config.getValue(section="view", option="FLUSH_TIME"))

        self.isView = True  # 是否启动View, 用于刷新仪表
        self.viewer = Viewer(target=self.target, config=self.config)

        self.isConnect = False  # 是否连接到望远镜, 如果未连接, 则关闭相关模块
        self.communicator = Communicator(comNumber=self.config.getValue(section='serial', option='COM_Number'))

        self.isRecord = False  # 是否开启指向修正
        self.recorder = Recorder()  # 配置记录器

        self.isCorrect = False  # 是否开启指向修正
        self.corrector = Corrector(recorder=self.recorder)

        self.concurrentData = {}  # 定义全局共享堆
        self.haOffset = HAOffset(ha=-361, haOffset=-361, localTime=QDateTime.currentDateTime(), version="",
                                 target=self.target)
        self.decOffset = DECOffset(dec=-361, decOffset=-361, localTime=QDateTime.currentDateTime(), version="",
                                   target=self.target)

    def setupSunflower(self):
        # 定义仪表显示模块
        self.displayStatus(status="setupView")
        self.setupView()

        # 定义望远镜通信模块
        self.displayStatus(status="setupControl")
        self.setupControl()

        # 定义望远镜目标模块
        self.displayStatus(status="setupTarget")
        self.setupTarget()

        # 定义望远镜目标模块
        self.displayStatus(status="setupCorrect")
        self.correctThread = threading.Thread(target=self.correct, daemon=True)
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
        while self.isRecord:
            self.recorder.writeData(HAoffset=self.concurrentData['HAoffset'],
                                    DECoffset=self.concurrentData['DECoffset'])

    def setupCorrect(self):
        if self.isCorrect:
            self.isCorrect = False
            self.ui_form.correctButton.setText("CORRECT")
        else:
            while self.correctThread.is_alive():
                sleep(1)
            self.isCorrect = True
            self.ui_form.correctButton.setText("OFF-CORRECT")
            self.correctThread = threading.Thread(target=self.correct, daemon=True)
            self.correctThread.start()

    def correct(self):
        """
        俯仰、方位
        :return:
        """
        while self.isCorrect:
            # TODO set sleep time in config
            sleep(1)
            self.concurrentData = self.corrector.fitHA()
            self.ui_form.decOffsetLcdNumber.display(float(self.concurrentData['decOffsetLcdNumber']))
            self.ui_form.haOffsetLcdNumber.display(float(self.concurrentData['haOffsetLcdNumber']))

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
            self.concurrentData['telescopeHALcdNumber'], self.concurrentData['telescopeDecLcdNumber'] \
                = self.communicator.getPosition()
            self.ui_form.telescopeHALcdNumber.display(self.concurrentData['telescopeHALcdNumber'])
            self.ui_form.telescopeDecLcdNumber.display(self.concurrentData['telescopeDecLcdNumber'])

    def setupTarget(self):
        pass

    def displayStatus(self, status, isError=False):
        if isError:
            log = "[-]"
        else:
            log = "[+]"
        log += str(QDateTime.currentDateTime().toTime_t()) + "\t" + status
        print(log)
        self.ui_form.statusTextBrowser.append(log)

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
            self.haOffset.localTime = QDateTime.currentDateTime()
            self.decOffset.localTime = self.haOffset.localTime
            self.haOffset.ha, self.haOffset.dec, self.concurrentData['raLcdNumber'], self.concurrentData[
                'ctime'] = self.viewer.getViewData()
            self.ui_form.haLcdNumber.display(self.haOffset.ha)
            self.ui_form.decLcdNumber.display(self.haOffset.dec)
            self.ui_form.raLcdNumber.display(self.concurrentData['raLcdNumber'])
            self.ui_form.localtimeDateTimeEdit.setDateTime(self.haOffset.localTime)
            self.ui_form.utcDateTimeEdit.setDateTime(QDateTime.currentDateTime().toUTC())
            self.ui_form.lstDateTimeEdit.setDateTime(self.concurrentData['ctime'])

    def setupUi(self, MainWindow):
        """
        用于加载Ui_Form设计的UI于MainWindow
        :param MainWindow:
        :return:
        """
        self.ui_form.setupUi(MainWindow)
