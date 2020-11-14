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
    def __init__(self, ha: float, haOffset: float, version: int):
        """
        抽象时角误差对象
        :param ha: 时角
        :param haOffset: 时角误差
        :param localTime: 本地时间
        :param version: 版本
        :param target: 目标
        """
        self.ha, self.haOffset, self.version = ha, haOffset, version

    def __add__(self, other):
        """
        误差相加
        :param other:
        :return:
        """
        dec_offset = self.haOffset + other.haOffset
        return DECOffset(dec=self.ha, decOffset=dec_offset, version=self.version)


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
        dec_offset = self.decOffset + other.decOffset
        return DECOffset(dec=self.dec, decOffset=dec_offset, version=self.version)
