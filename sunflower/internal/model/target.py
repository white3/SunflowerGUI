#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 21:44
# @Author  : Menzel3
# @Site    :
# @File    : target.py
# @Software: PyCharm
# @version : 0.0.1
from copy import copy, deepcopy


class Target:
    def __init__(self, tid=None, name="tests", isInherent=True, hourAngle=0.0, declination=0.0, rightAscension=0.0):
        """

        :param tid: 目标id号
        :param name: 目标名称
        :param isInherent: 目标是否在内置星图
        :param hourAngle: 目标时角
        :param declination: 目标赤纬
        :param rightAscension: 目标赤经
        """
        self.tid = tid
        self.name = name
        self.hourAngle = hourAngle
        self.declination = declination
        self.rightAscension = rightAscension
        self.isInherent = isInherent

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return f"不存在{item}属性"

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

    def __str__(self):
        return "{ name:'%s', hourAngle:'%f', declination:'%f', rightAscension:'%f', isInherent:'%s' }" % \
               (self.name, self.hourAngle, self.declination, self.rightAscension, self.isInherent)


if __name__ == '__main__':
    target = Target(name='sun')
    target.hourAngle = 0.1
    target.declination = 1.1
    target.rightAscension = 2.1
    target.isInherent = False

    print(target)
