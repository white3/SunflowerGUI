#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/11 21:08
# @Author  : Menzel3
# @Site    : 
# @File    : offset.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.model.target import Target
from copy import copy, deepcopy


class Offset(object):
    def __init__(self, angle: float, offset: float, version: int):
        """
        抽象时角误差对象
        :param angle: 时角
        :param haOffset: 时角误差
        :param localTime: 本地时间
        :param version: 版本
        :param target: 目标
        """
        self.angle, self.offset, self.version = angle, offset, version

    def __add__(self, other):
        """
        误差相加
        :param other:
        :return:
        """
        if type(other) is Offset:
            offset = self.offset + other.offset
            return Offset(angle=self.angle, offset=offset, version=self.version)
        else:
            return float(other) + self.offset

    def __str__(self):
        return "%d - %f %f %d" % (id(self), self.angle, self.offset, self.version)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
