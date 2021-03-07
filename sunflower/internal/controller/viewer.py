#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 22:41
# @Author  : Menzel3
# @Site    : 
# @File    : viewer.py
# @Software: PyCharm
# @version : 0.0.1

from sunflower.internal.constants import constant
from sunflower.internal.util.calculator import Calculator
from sunflower.internal.model.times import Times
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.controller import status
import time


class Viewer(interruptible_thread.ThreadMeta):

    @status.status_log("init Viewer", constant.MEDIUM)
    def __init__(self, **kwargs):
        """

        :param target: 目标
        :param config: 配置文件，需要用到经纬度及海拔
        """
        interruptible_thread.ThreadMeta.__init__(self)
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.calculator = Calculator(lat=constant.LAT,
                                     lon=constant.LON,
                                     elevation=constant.ELEVATION,
                                     target=self.data['target'])
        self.run()

    def work(self):
        """
        后台运行 时角、赤纬、赤经、时间的计算
        :return:
        """
        # display target position
        self.data['conditions']['target'].write_lock()
        try:
            self.data['target'].hourAngle, self.data['target'].declination, self.data[
                'target'].rightAscension, utc_datetime = self.calculator.computeLocation()
            self.view['haLcdNumber'].display(self.data['target'].hourAngle)
            self.view['decLcdNumber'].display(self.data['target'].declination)
            self.view['raLcdNumber'].display(self.data['target'].rightAscension)
        finally:
            self.data['conditions']['target'].write_unlock()

        self.data['conditions']['globalClock'].write_lock()
        try:
            self.data['globalClock'] = Times(utc=utc_datetime)
            self.view['utcDateTimeEdit'].setDateTime(self.data['globalClock'].toUTC())
            self.view['localtimeDateTimeEdit'].setDateTime(self.data['globalClock'].toLocalTime())
            self.view['lstDateTimeEdit'].setDateTime(self.data['globalClock'].toLST())
        finally:
            self.data['conditions']['globalClock'].write_unlock()

        # display correction
        self.data['conditions']['decOffset'].read_lock()
        try:
            self.view['decOffsetLcdNumber'].display(self.data['decOffset'].offset)
        finally:
            self.data['conditions']['decOffset'].read_unlock()

        self.data['conditions']['haOffset'].read_lock()
        try:
            self.view['haOffsetLcdNumber'].display(self.data['haOffset'].offset)
        finally:
            self.data['conditions']['haOffset'].read_unlock()

        # display telescope position
        self.data['conditions']['currentDirecting'].read_lock()
        try:
            self.view['telescopeHALcdNumber'].display(self.data['currentDirecting'].hourAngle)
            self.view['telescopeDecLcdNumber'].display(self.data['currentDirecting'].declination)
        finally:
            self.data['conditions']['currentDirecting'].read_unlock()
            time.sleep(constant.VIEW_FLUSH_TIME)