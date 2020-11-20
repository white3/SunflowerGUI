#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:35
# @Author  : Menzel3
# @Site    : 
# @File    : Control.py
# @Software: PyCharm
# @version : 0.0.1
import time
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.constants import constant
from sunflower.internal.util.communicator import Communicator
from sunflower.internal.controller import status


class ControlController(interruptible_thread.ThreadMeta):
    """
    做望远镜指令控制(communicator)的上层封装
    """

    @status.status_log("init ControlController", constant.MEDIUM)
    def __init__(self, **kwargs):
        interruptible_thread.ThreadMeta.__init__(self)
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.communicator = Communicator(serialChannel=self.data['ser'])
        self.view['traceButton'].clicked.connect(self.trace)
        self.view['stopButton'].clicked.connect(self.stop)
        self.view['resetButton'].clicked.connect(self.reset)
        self.view['comButton'].clicked.connect(self.connectSerialChannel)
        self.view['dropPowerButton'].clicked.connect(self.drop_power)
        self.view['powerButton'].clicked.connect(self.insert_power)
        self.telescopePositionControl = TelescopePositionControl(communicator=self.communicator,
                                                                 currentDirecting=self.data['currentDirecting'])
        self.isTrace = False

    def showTelescopePosition(self):
        """
        显示望远镜指向位置
        :return:
        """
        self.telescopePositionControl.run()

    def trace(self):
        """
        开始跟踪目标
        :return:
        """
        if self.isTrace:
            self.isTrace = False
            self.view['traceButton'].setText('Trace')
            self.wait()
        else:
            self.isTrace = True
            self.view['traceButton'].setText('stopTrace')
            self.run()

    def work(self):
        """
        线程执行函数, 用于更新指向数值
        :return:
        """
        time.sleep(constant.TRACE_FLUSH_TIME)
        ha, dec = self.data['haOffset'] + self.data['target'].hourAngle, self.data['decOffset'] + self.data[
            'target'].declination
        status.display_status("tracing %f, %f" % (ha, dec), constant.LOW)
        self.communicator.point(ha, dec)

    def stop(self):
        """
        急停指令
        :return:
        """
        self.communicator.stop()

    def reset(self):
        """
        望远镜归天顶位
        :return:
        """
        self.communicator.reset()

    def connectSerialChannel(self):
        """
        串口连接
        :return:
        """
        try:
            self.data['ser'].open()
            self.communicator.serialChannel = self.data['ser']
            self.showTelescopePosition()
        except Exception as e:
            status.display_status(status=e, color=constant.HIGH)
            status.display_status(status="Failed to connect to serial com", color=constant.HIGH)
        else:
            status.display_status(status="Connect to serial com", color=constant.MEDIUM)

    def insert_power(self):
        """
        驱动上电
        :return:
        """
        self.communicator.insert_power()

    def drop_power(self):
        """
        驱动断电
        :return:
        """
        self.communicator.drop_power()


class TelescopePositionControl(interruptible_thread.ThreadMeta):
    def __init__(self, communicator, currentDirecting):
        interruptible_thread.ThreadMeta.__init__(self)
        self.communicator = communicator
        self.currentDirecting = currentDirecting
        self.show_failed = True

    def before_work(self):
        self.show_failed = True

    def work(self):
        """
        俯仰、方位
        :return:
        """
        time.sleep(constant.VIEW_FLUSH_TIME)
        try:
            self.currentDirecting.hourAngle, self.currentDirecting.declination \
                = self.communicator.getPosition()
            self.show_failed = True
        except Exception as e:
            if self.show_failed:
                print(e.__str__())
                status.display_status(status=e, color=constant.HIGH)
                self.show_failed = False
            self.currentDirecting.hourAngle = 999
            self.currentDirecting.declination = 999


class ManualCalibrateController(object):

    @status.status_log("init ManualCalibrateController", constant.MEDIUM)
    def __init__(self, **kwargs):
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.view['upButton'].clicked.connect(self.up)
        self.view['downButton'].clicked.connect(self.down)
        self.view['cwButton'].clicked.connect(self.cw)
        self.view['ccwButton'].clicked.connect(self.ccw)

    def ccw(self):
        """
        方位角预算误差升高
        :return:
        """
        base = self.view['speedSpinBox'].value() / constant.SPEED_MAX
        self.data['haManualCalibrateOffset'].offset += base

    def cw(self):
        """
        方位角预算误差降低
        :return:
        """
        base = self.view['speedSpinBox'].value() / constant.SPEED_MAX
        self.data['haManualCalibrateOffset'].offset -= base

    def up(self):
        """
        俯仰角预算误差升高
        :return:
        """
        base = self.view['speedSpinBox'].value() / constant.SPEED_MAX
        self.data['decManualCalibrateOffset'].offset += base

    def down(self):
        """
        俯仰角预算误差降低
        :return:
        """
        base = self.view['speedSpinBox'].value() / constant.SPEED_MAX
        self.data['decManualCalibrateOffset'].offset -= base
