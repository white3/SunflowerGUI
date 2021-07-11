#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 22:41
# @Author  : Menzel3
# @Site    :
# @File    : viewer.py
# @Software: PyCharm
# @version : 0.0.1
import traceback

from sunflower.internal.constants import constant
from sunflower.internal.controller.controller import ConController
from sunflower.internal.util.calculator import Calculator
from sunflower.internal.model.times import Times
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.controller import status
import time


class Viewer(ConController):

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
                                     target=self.data.get('target'))
        self.view.viewButton.clicked.connect(self.start)

    def start(self):
        self.run()

    def setup(self) -> bool:
        """
        执行启动前
        :return: True 表示直接启动, False 表示不直接启动
        """
        return False

    def work(self):
        """
        后台运行 时角、赤纬、赤经、时间的计算
        :return:
        """
        # display target position
        ha, dec, ra, utc_datetime = self.calculator.computeLocation()
        target = self.data.get('target')
        target.hourAngle, target.declination, target.rightAscension = ha, dec, ra
        self.data.set('target', target)

        self.view.haLcdNumber.display(ha)
        self.view.decLcdNumber.display(dec)
        self.view.raLcdNumber.display(ra)

        self.data.set('globalClock', Times(utc=utc_datetime))
        self.view.utcDateTimeEdit.setDateTime(self.data.get('globalClock').toUTC())
        self.view.localtimeDateTimeEdit.setDateTime(self.data.get('globalClock').toLocalTime())
        self.view.lstDateTimeEdit.setDateTime(self.data.get('globalClock').toLST())

        # display correction
        self.view.decOffsetLcdNumber.display(self.data.get('decOffset').offset)
        self.view.haOffsetLcdNumber.display(self.data.get('haOffset').offset)

        # display telescope position
        self.view.telescopeHALcdNumber.display(self.data.get('currentDirecting').hourAngle)
        self.view.telescopeDecLcdNumber.display(self.data.get('currentDirecting').declination)
        time.sleep(constant.VIEW_FLUSH_TIME)
        # print(ha, dec, ra)
