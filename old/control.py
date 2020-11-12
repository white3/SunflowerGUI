#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:35
# @Author  : Menzel3
# @Site    : 
# @File    : Control.py
# @Software: PyCharm
# @version : 0.0.1
import threading

from sunflower import *

class Control:
    def __init__(self, configer, communicator, calculator, recordor, corrector):
        self.configer = configer
        self.communicator, self.calculator, self.recordor, self.corrector = communicator, calculator, recordor, corrector
        self.isTracing = threading.Condition()  # a global lock to Control the thread of tracing the Sun
        self.traceFlag = True  # a signal
        self.traceThread = threading.Thread(target=self.traceStar, daemon=True)
        self.traceThread.start()

    def traceStar(self):
        self.traceFlag = False
        self.isTracing.acquire()
        self.isTracing.notify()
        self.isTracing.release()

    def stopTrace(self):
        self.traceFlag = True
        self.__sunflower.stopTelescope()