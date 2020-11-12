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
    def __init__(self, ha: float, haOffset: float, localTime, version: int, target: Target):
        self.ha, self.haOffset, self.localTime, self.version, self.target = ha, haOffset, localTime, version, target


class DECOffset(object):
    def __init__(self, dec: float, decOffset: float, localTime, version: int, target: Target):
        self.dec, self.decOffset, self.localTime, self.version, self.target = dec, decOffset, localTime, version, target
