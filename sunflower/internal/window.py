# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from sunflower.internal.view.window_ui import Ui_Form
from sunflower.internal.controller.viewer import Viewer
from sunflower.internal.model.target import Target
from sunflower.internal.model.offset import Offset
from sunflower.internal.model.times import Times
from sunflower.internal.controller.recorder import RecorderController
from sunflower.internal.controller.corrector import CorrectorController
from sunflower.internal.controller.telescope import ManualCalibrateController, CommunicatorControl
from sunflower.internal.controller.serial_channer import SerialController
from sunflower.internal.model.container import ConcurrentDataContainer
from sunflower.internal.model.circle_lock import CircleLock
from sunflower.internal.constants import constant
from sunflower.internal.controller import status
from PyQt5.QtGui import QPixmap
import serial


class Window(object):
    ui_form = Ui_Form()  # 定义GUI界面
    container = ConcurrentDataContainer()

    def __init__(self):
        """
        此时 ui_form 未加载，所以只能初始化与GUI无关的变量
        """
        self.container.ser = serial.Serial(timeout=constant.timeout, baudrate=constant.baudrate)
        self.container.globalClock = Times()  # 定义全局时钟
        self.container.target = Target(name="sun", isInherent=True)  # 望远镜目标方位，实时
        self.container.currentDirecting = Target(name="current")  # 望远镜指向方位，实时

        self.container.haManualCalibrateOffset = Offset(angle=self.container.target.hourAngle, offset=0,
                                                        version=constant.version)  # 手动校准时角误差
        self.container.haFitOffset = Offset(angle=self.container.target.hourAngle, offset=0,
                                            version=constant.version)  # 拟合数据的估算时角误差
        self.container.haOffset = Offset(angle=self.container.target.hourAngle, offset=0,
                                         version=constant.version)  # 时角误差的和

        self.container.decManualCalibrateOffset = Offset(angle=self.container.target.declination, offset=0,
                                                         version=constant.version)  # 手动校准的赤纬误差
        self.container.decFitOffset = Offset(angle=self.container.target.declination, offset=0,
                                             version=constant.version)  # 拟合数据的估算赤纬误差
        self.container.decOffset = Offset(angle=self.container.target.declination, offset=0,
                                          version=constant.version)  # 赤纬误差的和
        self.container.conditions = {
            'ser' : CircleLock(),
            'globalClock' : CircleLock(),
            'target' : CircleLock(),
            'currentDirecting' : CircleLock(),
            'haManualCalibrateOffset' : CircleLock(),
            'haFitOffset' : CircleLock(),
            'haOffset' : CircleLock(),
            'decManualCalibrateOffset' : CircleLock(),
            'decFitOffset' : CircleLock(),
            'decOffset' : CircleLock(),
        }
        self.container.targetList = {0: ['SOLAR_SYSTEM_BARYCENTER', 'SSB', 'SOLAR SYSTEM BARYCENTER'],
                                     1: ['MERCURY_BARYCENTER', 'MERCURY BARYCENTER'],
                                     2: ['VENUS_BARYCENTER', 'VENUS BARYCENTER'],
                                     3: ['EARTH_BARYCENTER', 'EMB', 'EARTH MOON BARYCENTER', 'EARTH-MOON BARYCENTER',
                                         'EARTH BARYCENTER'],
                                     4: ['MARS_BARYCENTER', 'MARS BARYCENTER'],
                                     5: ['JUPITER_BARYCENTER', 'JUPITER BARYCENTER'],
                                     6: ['SATURN_BARYCENTER', 'SATURN BARYCENTER'],
                                     7: ['URANUS_BARYCENTER', 'URANUS BARYCENTER'],
                                     8: ['NEPTUNE_BARYCENTER', 'NEPTUNE BARYCENTER'],
                                     9: ['PLUTO_BARYCENTER', 'PLUTO BARYCENTER'],
                                     10: ['SUN'], 199: ['MERCURY'], 299: ['VENUS'], 399: ['EARTH'], 301: ['MOON'],
                                     499: ['MARS']}  # 软件内置目标图，修改即更新

    def __del__(self):
        self.container.ser.close()

    def setupSunflower(self):
        """
        加载完 ui_form 后再执行的函数
        :return:
        """
        # 自动修正
        # self.correctorController = CorrectorController(
        #     view={
        #         'correctButton': self.ui_form.correctButton,
        #         'updateCorrectionButton': self.ui_form.updateCorrectionButton,
        #     }, data=self.container)

        #
        # 初始化串口模块, 运行串口探活线程
        self.serialController = SerialController(view={
            # 'ser': self.ser,
            'comNumberSpinBox': self.ui_form.comNumberSpinBox,
            'comButton': self.ui_form.comButton,
        }, data=self.container)

        # 定义望远镜通信模块
        self.control = CommunicatorControl(view={
            'traceButton': self.ui_form.traceButton,
            'stopButton': self.ui_form.stopButton,
            'resetButton': self.ui_form.resetButton,
            'dropPowerButton': self.ui_form.dropPowerButton,
            'powerButton': self.ui_form.powerButton,
            'initButton': self.ui_form.initButton,
        }, data=self.container)

        # 定义指向误差记录模块
        self.recorderController = RecorderController(view={
            'recordButton': self.ui_form.recordButton,
        }, data=self.container)

        # 手动修正
        self.manualCalibrateController = ManualCalibrateController(
            view={'speedSpinBox': self.ui_form.speedSpinBox, 'upButton': self.ui_form.upButton,
                  'downButton': self.ui_form.downButton, 'ccwButton': self.ui_form.ccwButton,
                  'cwButton': self.ui_form.cwButton,
                  },
            data=self.container
        )

        # 初始化仪表模块
        # 运行仪表更新线程
        self.viewer = Viewer(view={
            'localtimeDateTimeEdit': self.ui_form.localtimeDateTimeEdit,
            'utcDateTimeEdit': self.ui_form.utcDateTimeEdit,
            'lstDateTimeEdit': self.ui_form.lstDateTimeEdit,
            'haLcdNumber': self.ui_form.haLcdNumber,
            'decLcdNumber': self.ui_form.decLcdNumber,
            'raLcdNumber': self.ui_form.raLcdNumber,
            'decOffsetLcdNumber': self.ui_form.decOffsetLcdNumber,
            'haOffsetLcdNumber': self.ui_form.haOffsetLcdNumber,
            'telescopeHALcdNumber': self.ui_form.telescopeHALcdNumber,
            'telescopeDecLcdNumber': self.ui_form.telescopeDecLcdNumber,
        }, data=self.container)

        # 定义望远镜目标模块
        # self.displayStatus(status="setupTarget", color=constants.MEDIUM)
        # self.setupTarget()

    def setupUi(self, MainWindow):
        """
        用于加载Ui_Form设计的UI于MainWindow
        :param MainWindow:
        :return:
        """
        self.ui_form.setupUi(MainWindow)
        self.ui_form.graphicsView.setPixmap(QPixmap('res/4.5.png'))
        status.setup_display = True
        status.statusTextBrowser = self.ui_form.statusTextBrowser
