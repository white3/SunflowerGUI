# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from sunflower.internal.controller.light_corrector import LightCalibrateController
from sunflower.internal.util.communicator import Communicator
from sunflower.internal.view.window_ui import Ui_Form
from sunflower.internal.model.target import Target
from sunflower.internal.model.offset import Offset
from sunflower.internal.model.times import Times
from sunflower.internal.controller.recorder import RecorderController
from sunflower.internal.controller.corrector import CorrectorController
from sunflower.internal.controller.telescope import ManualCalibrateController, CommunicatorControl
from sunflower.internal.controller.serial_channer import SerialController
from sunflower.internal.controller.viewer import Viewer
from sunflower.internal.model.container import ConDataContainer
from sunflower.internal.constants import constant
from sunflower.internal.controller import status
from PyQt5.QtGui import QPixmap
import serial


class Window(object):
    ui_form = Ui_Form()  # 定义GUI界面
    container = ConDataContainer()
    modules = {}

    def __init__(self):
        """
        此时 ui_form 未加载，所以只能初始化与GUI无关的变量
        """
        pass

    def __del__(self):
        self.container.get('ser').close()

    def init_data(self):
        """
        初始化模块所使用的共享数据对象
        :return:
        """
        # 串口对象
        self.container.set('ser', serial.Serial(timeout=constant.timeout, baudrate=constant.baudrate))
        # 全局时钟
        self.container.set('globalClock', Times())
        # 望远镜目标方位，实时
        self.container.set('target', Target(name="sun", isInherent=True))
        # 望远镜指向方位，实时
        self.container.set('currentDirecting', Target(name="current"))
        # 手动校准时角误差
        self.container.set('haManualCalibrateOffset',
                           Offset(angle=self.container.get('target').hourAngle, offset=0, version=constant.version))
        # 拟合数据的估算时角误差
        self.container.set('haFitOffset', Offset(angle=self.container.get('target').hourAngle, offset=0,
                                                 version=constant.version))
        # 时角误差的和
        self.container.set('haOffset',
                           Offset(angle=self.container.get('target').hourAngle, offset=0, version=constant.version))
        # 手动校准的赤纬误差
        self.container.set('decManualCalibrateOffset', Offset(angle=self.container.get('target').declination, offset=0,
                                                              version=constant.version))
        # 拟合数据的估算赤纬误差
        self.container.set('decFitOffset', Offset(angle=self.container.get('target').declination, offset=0,
                                                  version=constant.version))
        # 赤纬误差的和
        self.container.set('decOffset', Offset(angle=self.container.get('target').declination, offset=0,
                                               version=constant.version))
        # 软件内置目标图
        self.container.set('targets', {0: ['SOLAR_SYSTEM_BARYCENTER', 'SSB', 'SOLAR SYSTEM BARYCENTER'],
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
                                       499: ['MARS']})
        self.container.set('communicator', Communicator(serial_channel=self.container.get('ser')))
        self.container.set('traced', False)

    def init_modules(self):
        """
        初始化模块对象
        :return:
        """
        # 自动修正
        # self.modules['correctorController'] = CorrectorController(view=self.ui_form, data=self.container)

        # 初始化串口模块, 运行串口探活线程
        self.modules['serialController'] = SerialController(view=self.ui_form, data=self.container)

        # 定义望远镜通信模块
        self.modules['control'] = CommunicatorControl(view=self.ui_form, data=self.container)

        # 手动修正
        self.modules['manualCalibrateController'] = ManualCalibrateController(view=self.ui_form, data=self.container)

        # 初始化仪表模块
        self.modules['viewer'] = Viewer(view=self.ui_form, data=self.container)

        # 光学修正模块 lightCorrectButton
        self.modules['lightCalibrateController'] = LightCalibrateController(view=self.ui_form, data=self.container)

        # 定义望远镜目标模块
        # self.displayStatus(status="setupTarget", color=constants.MEDIUM)
        # self.setupTarget()

        # 定义指向误差记录模块
        # self.modules['recorderController'] = RecorderController(view=self.ui_form, data=self.container)

    def setupSunflower(self):
        """
        加载完 ui_form 后再执行的函数
        :return:
        """
        self.init_data()
        self.init_modules()

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
