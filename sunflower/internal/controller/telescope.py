#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:35
# @Author  : Menzel3
# @Site    : 
# @File    : Control.py
# @Software: PyCharm
# @version : 0.0.1
import time
import traceback

from sunflower.internal.controller.controller import Controller, ConController
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.constants import constant
from sunflower.internal.util.communicator import Communicator
from sunflower.internal.controller import status


class CommunicatorControl(ConController):
    """
    做望远镜指令控制(communicator)的上层封装W
    """

    def setup(self) -> bool:
        return False

    @status.status_log("init CommunicatorControl", constant.MEDIUM)
    def __init__(self, **kwargs):
        interruptible_thread.ThreadMeta.__init__(self)
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.communicator = self.data.get('communicator')

        # self.communicator = Communicator(serial_channel=self.data.get('ser'))

        self.view.traceButton.clicked.connect(self.trace)
        self.view.stopButton.clicked.connect(self.stop)
        self.view.resetButton.clicked.connect(self.reset)
        self.view.dropPowerButton.clicked.connect(self.drop_power)
        self.view.powerButton.clicked.connect(self.insert_power)
        self.view.initButton.clicked.connect(self.init_telescope_for_warm)
        self.view.lowLocationButton.clicked.connect(self.low_location)
        self.view.rpc_edit.returnPressed.connect(self.command_exec)
        self.show_failed = True
        self.ha, self.dec = 0.5, 42.8
        # self.warm = False

    def command_exec(self):
        try:
            rpc = self.view.rpc_edit.text()
            self.view.rpc_edit.clear()
            self.communicator.rpc_exec(rpc)
            status.display_status(rpc, constant.MEDIUM)
        except Exception as e:
            status.display_status(str(e), constant.HIGH)

    def init_telescope_for_warm(self):
        """
        低速运动 30s
        :return:
        """
        # 移到 2 min至中间处 1200 * 0.1 = 120s
        for i in range(1200):
            self.communicator.rpc_exec('低速下转')
            time.sleep(0.1)

        for j in range(14):
            end_time = 60 * 5
            for i in range(end_time):
                self.communicator.rpc_exec('低速下转')
                self.communicator.rpc_exec('低速逆转')
                time.sleep(0.1)
                self.communicator.rpc_exec('低速下转')
                self.communicator.rpc_exec('低速逆转')
                time.sleep(0.1)

            for i in range(end_time):
                self.communicator.rpc_exec('低速顺转')
                self.communicator.rpc_exec('低速上转')
                time.sleep(0.1)
                self.communicator.rpc_exec('低速顺转')
                self.communicator.rpc_exec('低速上转')
                time.sleep(0.1)

    def work(self):
        """
        线程执行函数, 用于更新指向数值
        :return:
        """
        try:
            time.sleep(constant.TRACE_FLUSH_TIME)
            self.data.set('decOffset', self.data.get('decFitOffset') + self.data.get('decManualCalibrateOffset'))
            self.data.set('haOffset', self.data.get('haFitOffset') + self.data.get('haManualCalibrateOffset'))
            ha, dec = self.data.get('haOffset') + self.data.get('target').hourAngle, self.data.get(
                'decOffset') + self.data.get('target').declination
            # -179, 180
            # ha changed
            if ha + constant.limit > self.ha or ha - constant.limit > self.ha:
                is_ha, self.ha = True, ha
            else:
                is_ha = False
            # dec changed
            if dec + constant.limit > self.dec or dec - constant.limit > self.dec:
                is_dec, self.dec = True, dec
            else:
                is_dec = False
            self.communicator.track(ha, dec, is_ha, is_dec)
            if is_ha or is_dec:
                status.display_status("tracing %f, %f" % (self.ha, self.dec), constant.LOW)
            self.show_telescope_pointing()
        except Exception:
            status.display_status(traceback.format_exc(), constant.HIGH)

    def show_telescope_pointing(self):
        """
        显示望远镜指向位置
        :return:
        """
        cur_direct = self.data.get('currentDirecting')
        try:
            cur_direct.hourAngle, cur_direct.declination = self.communicator.get_position()
            self.data.set('currentDirecting', cur_direct)
            self.show_failed = True
        except Exception:
            if self.show_failed:
                print(traceback.format_exc())
                status.display_status(status=traceback.format_exc(), color=constant.HIGH)
                self.show_failed = False
            cur_direct.hourAngle = 999
            cur_direct.declination = 999
            self.data.set('currentDirecting', cur_direct)

    def stop(self):
        """
        急停指令
        :return:
        """
        self.communicator.rpc_exec("急停")

    def low_location(self):
        """
        望远镜归天顶位
        :return:
        """
        self.communicator.rpc_exec("转至低位")

    def reset(self):
        """
        望远镜归天顶位
        :return:
        """
        self.communicator.rpc_exec("收藏")

    def insert_power(self):
        """
        驱动上电
        :return:
        """
        self.communicator.rpc_exec("驱动上电")

    def drop_power(self):
        """
        驱动断电
        :return:
        """
        self.communicator.rpc_exec("驱动断电")

    def trace(self):
        """
        开始跟踪目标
        :return:
        """
        if self.data.get('traced'):
            self.data.set('traced', False)
            self.view.traceButton.setText('Trace')
            self.wait()
        else:
            self.data.set('traced', True)
            self.view.traceButton.setText('stopTrace')
            self.run()


class ManualCalibrateController(Controller):

    @status.status_log("init ManualCalibrateController", constant.MEDIUM)
    def __init__(self, **kwargs):
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.communicator = self.data.get('communicator')
        self.view.upButton.clicked.connect(self.up)
        self.view.downButton.clicked.connect(self.down)
        self.view.cwButton.clicked.connect(self.cw)
        self.view.ccwButton.clicked.connect(self.ccw)

    def ccw(self):
        """
        方位角预算误差升高
        :return:
        """
        if self.data.get('traced'):
            base = self.view.speedSpinBox.value() / constant.SPEED_MAX
            of = self.data.get('haManualCalibrateOffset')
            of.offset = of.offset + base
            self.data.set('haManualCalibrateOffset', of)
        else:
            v = self.view.speedSpinBox.value()
            if v > 3600:
                self.communicator.rpc_exec('高速顺转')
            elif v > 60:
                self.communicator.rpc_exec('中速顺转')
            else:
                self.communicator.rpc_exec('低速顺转')

    def cw(self):
        """
        方位角预算误差降低
        :return:
        """
        if self.data.get('traced'):
            base = self.view.speedSpinBox.value() / constant.SPEED_MAX
            of = self.data.get('haManualCalibrateOffset')
            of.offset = of.offset - base
            self.data.set('haManualCalibrateOffset', of)
        else:
            v = self.view.speedSpinBox.value()
            if v > 3600:
                self.communicator.rpc_exec('高速逆转')
            elif v > 60:
                self.communicator.rpc_exec('中速逆转')
            else:
                self.communicator.rpc_exec('低速逆转')

    def up(self):
        """
        俯仰角预算误差升高
        :return:
        """
        if self.data.get('traced'):
            base = self.view.speedSpinBox.value() / constant.SPEED_MAX
            of = self.data.get('decManualCalibrateOffset')
            of.offset = of.offset + base
            self.data.set('decManualCalibrateOffset', of)
        else:
            v = self.view.speedSpinBox.value()
            if v > 3600:
                self.communicator.rpc_exec('高速上转')
            elif v > 60:
                self.communicator.rpc_exec('中速上转')
            else:
                self.communicator.rpc_exec('低速上转')

    def down(self):
        """
        俯仰角预算误差降低
        :return:
        """
        if self.data.get('traced'):
            base = self.view.speedSpinBox.value() / constant.SPEED_MAX
            of = self.data.get('decManualCalibrateOffset')
            of.offset = of.offset - base
            self.data.set('decManualCalibrateOffset', of)
        else:
            v = self.view.speedSpinBox.value()
            if v > 3600:
                self.communicator.rpc_exec('高速下转')
            elif v > 60:
                self.communicator.rpc_exec('中速下转')
            else:
                self.communicator.rpc_exec('低速下转')
