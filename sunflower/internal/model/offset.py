#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 21:08
# @Author  : Menzel3
# @Site    : 
# @File    : offset.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.model.target import Target


class HAOffset(object):
    def __init__(self, ha: float, ha_offset: float, version: int):
        """
        抽象时角误差对象
        :param ha: 时角
        :param haOffset: 时角误差
        :param localTime: 本地时间
        :param version: 版本
        :param target: 目标
        """
        self.ha, self.ha_offset, self.version = ha, ha_offset, version

    def __add__(self, other):
        """
        误差相加
        :param other:
        :return:
        """
        if type(other) is HAOffset:
            ha_offset = self.ha_offset + other.ha_offset
            return HAOffset(ha=self.ha, ha_offset=ha_offset, version=self.version)
        else:
            return float(other) + self.ha_offset


class DECOffset(object):
    def __init__(self, dec: float, decOffset: float, version: int):
        """
        抽象赤纬误差对象
        :param dec: 赤纬
        :param decOffset: 赤纬误差
        :param localTime: 本地时间
        :param version: 版本
        :param target: 目标
        """
        self.dec, self.decOffset, self.version = dec, decOffset, version

    def __add__(self, other):
        """
        误差相加
        :param other:
        :return:
        """
        if type(other) is DECOffset:
            dec_offset = self.decOffset + other.decOffset
            return DECOffset(dec=self.dec, decOffset=dec_offset, version=self.version)
        else:
            return float(other) + self.decOffset
