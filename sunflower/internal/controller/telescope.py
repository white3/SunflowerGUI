#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:35
# @Author  : Menzel3
# @Site    : 
# @File    : Control.py
# @Software: PyCharm
# @version : 0.0.1
import time
from sunflower.internal.meta import singleton_meta
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.constants import constant
from sunflower.internal.util.communicator import Communicator
from sunflower.internal.controller import status


class CommunicatorControl(interruptible_thread.ThreadMeta, metaclass=singleton_meta.SingletonMeta):
    """
    做望远镜指令控制(communicator)的上层封装
    """
    isTrace = False

    @status.status_log("init CommunicatorControl", constant.MEDIUM)
    def __init__(self, **kwargs):
        interruptible_thread.ThreadMeta.__init__(self)
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.communicator = Communicator(serialChannel=self.data['ser'])
        self.view['traceButton'].clicked.connect(self.trace)
        self.view['stopButton'].clicked.connect(self.stop)
        self.view['resetButton'].clicked.connect(self.reset)
        self.view['dropPowerButton'].clicked.connect(self.drop_power)
        self.view['powerButton'].clicked.connect(self.insert_power)
        self.view['initButton'].clicked.connect(self.init_telescope_for_warm)
        self.view['lowLocationButton'].clicked.connect(self.low_location)
        self.show_failed = True
        self.isTrace = False
        # self.warm = False

    # 上下0.5
    def init_telescope_for_warm(self):
        self.communicator.warm_telescope(ha=1)
        # self.communicator.warm_telescope(dec=-1)
        # self.communicator.warm_telescope(ha=-1)
        # self.communicator.warm_telescope(dec=1)

    #     if self.warm: # True -> False 退出热身模式
    #         self.warm = False
    #         self.view['initButton'].setText('停止预热')
    #     else: # 开始热身模式
    #         self.warm = True
    #         self.view['initButton'].setText('进行预热, 点击Trace按钮')

    def work(self):
        """
        线程执行函数, 用于更新指向数值
        :return:
        """
        try:
            time.sleep(constant.TRACE_FLUSH_TIME)
            self.data['decOffset'] = self.data['decFitOffset'] + self.data['decManualCalibrateOffset']
            self.data['haOffset'] = self.data['haFitOffset'] + self.data['haManualCalibrateOffset']
            ha, dec = self.data['haOffset'] + self.data['target'].hourAngle, self.data['decOffset'] + self.data[
                'target'].declination
            status.display_status("tracing %f, %f" % (ha, dec), constant.LOW)
            self.show_telescope_pointing()
            # if self.warm:
            self.communicator.point(ha, dec)
            # else:
            #     if self.data['currentDirecting'].declination > 0: # 42,0 -> 0,0
            #         self.communicator.warm_telescope(dec=-1)
            #     else:
            #         if self.data['currentDirecting'].hourAngle > 0:
            #             if self.data['currentDirecting'].hourAngle < 80: # 0,0 -> 90, 0
            #                 self.communicator.warm_telescope(ha=1)
            #         elif
            #         self.communicator.warm_telescope(ha=-1)
            #     self.communicator.warm_telescope(dec=1)
        except Exception as e:
            status.display_status(e.__str__(), constant.HIGH)

    def show_telescope_pointing(self):
        """
        显示望远镜指向位置
        :return:
        """
        try:
            try:
                self.data['conditions']['currentDirecting'].write_lock()
                self.data['currentDirecting'].hourAngle, self.data['currentDirecting'].declination \
                    = self.communicator.getPosition()
            finally:
                self.data['conditions']['currentDirecting'].write_unlock()
            self.show_failed = True
        except Exception as e:
            if self.show_failed:
                print(e.__str__())
                status.display_status(status=e, color=constant.HIGH)
                self.show_failed = False
            try:
                self.data['conditions']['currentDirecting'].write_lock()
                self.data['currentDirecting'].hourAngle = 999
                self.data['currentDirecting'].declination = 999
            finally:
                self.data['conditions']['currentDirecting'].write_unlock()

    def stop(self):
        """
        急停指令
        :return:
        """
        self.communicator.stop()

    def low_location(self):
        """
        望远镜归天顶位
        :return:
        """
        self.communicator.low_location()

    def reset(self):
        """
        望远镜归天顶位
        :return:
        """
        self.communicator.reset()

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

    def trace(self):
        """
        开始跟踪目标
        :return:
        """
        if self.isTrace:
            print(self.status())
            self.isTrace = False
            self.view['traceButton'].setText('Trace')
            self.wait()
        else:
            self.isTrace = True
            self.view['traceButton'].setText('stopTrace')
            self.run()


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
        try:
            self.data['conditions']['haManualCalibrateOffset'].write_lock()
            self.data['haManualCalibrateOffset'].offset += base
        finally:
            self.data['conditions']['haManualCalibrateOffset'].write_unlock()

    def cw(self):
        """
        方位角预算误差降低
        :return:
        """
        base = self.view['speedSpinBox'].value() / constant.SPEED_MAX
        try:
            self.data['conditions']['haManualCalibrateOffset'].write_lock()
            self.data['haManualCalibrateOffset'].offset -= base
        finally:
            self.data['conditions']['haManualCalibrateOffset'].write_unlock()

    def up(self):
        """
        俯仰角预算误差升高
        :return:
        """
        base = self.view['speedSpinBox'].value() / constant.SPEED_MAX
        try:
            self.data['conditions']['decManualCalibrateOffset'].write_lock()
            self.data['decManualCalibrateOffset'].offset += base
        finally:
            self.data['conditions']['decManualCalibrateOffset'].write_unlock()

    def down(self):
        """
        俯仰角预算误差降低
        :return:
        """
        base = self.view['speedSpinBox'].value() / constant.SPEED_MAX
        try:
            self.data['conditions']['decManualCalibrateOffset'].write_lock()
            self.data['decManualCalibrateOffset'].offset -= base
        finally:
            self.data['conditions']['decManualCalibrateOffset'].write_unlock()
