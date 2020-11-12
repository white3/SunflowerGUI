#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/10 22:41
# @Author  : Menzel3
# @Site    : 
# @File    : viewer.py
# @Software: PyCharm
# @version : 0.0.1

from sunflower.internal.calculator import Calculator
from sunflower.internal.corrector import Corrector
from sunflower.internal.config import Config
from sunflower.internal.model.target import Target

class Viewer(object):
    """
    显示的数据格式：
    {
        HA
        Dec
        RA
        HAOffset
        DecOffset
        LocalTime
    }
    """
    def __init__(self, target: Target, config: Config):
        self.data = {}
        self.target = target
        self.calculator = Calculator(lat=config.getValue(section='location',option='lat'),
                                     lon=config.getValue(section='location',option='lon'),
                                     elevation=int(config.getValue(section='location',option='elevation')),
                                     target=self.target)

    def getViewData(self):
        # float(haDegree), float(sunDec), t
        self.data['HA'], self.data['Dec'], self.data['RA'], self.data['ctime'] = self.calculator.computeLocation()
        return self.data['HA'], self.data['Dec'], self.data['RA'], self.data['ctime']
