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
from sunflower.internal.model.target import Target

class Viewer(object):
    def __init__(self, target: Target):
        """

        :param target: 目标
        :param config: 配置文件，需要用到经纬度及海拔
        """
        self.data = {}
        self.target = target
        self.calculator = Calculator(lat=constant.LAT,
                                     lon=constant.LON,
                                     elevation=constant.ELEVATION,
                                     target=self.target)

    def getViewData(self):
        """

        :return: ha, dec, ra, ctime
        """
        self.data['HA'], self.data['Dec'], self.data['RA'], self.data['utc_datetime'] = self.calculator.computeLocation()
        time = Times(utc=self.data['utc_datetime'])
        return self.data['HA'], self.data['Dec'], self.data['RA'], time
