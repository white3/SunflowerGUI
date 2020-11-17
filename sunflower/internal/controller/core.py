#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/16 23:33
# @Author  : Menzel3
# @Site    : 
# @File    : core.py
# @Software: PyCharm
# @version : 0.0.1
import threading


class threadController(threading.Thread):
    def __init__(self, window):
        threading.Thread.__init__(self)

    def run(self):
        pass
