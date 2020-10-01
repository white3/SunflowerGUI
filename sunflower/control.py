#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:35
# @Author  : Menzel3
# @Site    : 
# @File    : control.py
# @Software: PyCharm
# @version : 0.0.1
import threading

from sunflower.service import service

class control:
    def __init__(self, config):
        self.__sunflower = service(config=config)
        self.isTracing = threading.Condition()  # a global lock to control the thread of tracing the Sun
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

    def resetTelescope(self):
        self.traceFlag = True
        self.__sunflower.resetTelescope()

    def telescopePosition(self):
        self.__sunflower.getTelescopeLocation()

    def connectTelescope(self, comNumber):
        self.__sunflower.setCOM(comNumber)
        self.__sunflower.connectTelescope()

    def disconnectTelescope(self):
        self.__sunflower.disconnectTelescope()

    def changeMoveConfig(self, speed, ori):
        self.__sunflower.commdSpwOr(speed, ori)

    def getTelescopeLocation(self):
        self.__sunflower.getStarPosition()

    def getInnerStarsList(self):
        self.__sunflower.getInnerStarsList()

    def getStarPosition(self):
        self.__sunflower.getStarPosition()