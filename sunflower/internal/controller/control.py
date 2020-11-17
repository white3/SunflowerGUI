#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/26 12:35
# @Author  : Menzel3
# @Site    : 
# @File    : Control.py
# @Software: PyCharm
# @version : 0.0.1
import threading
from sunflower.internal.util.communicator import Communicator
from sunflower.internal import constants


class Control(object):
    communicator = None  # 通信工具
    window = None  # 数据窗口
    isTracing = threading.Condition()  # a global lock to Control the thread of tracing the Sun
    traceFlag = False  # True表示跟踪, False表示不跟踪
    traceThread = None

    def __init__(self, communicator: Communicator, window):
        self.communicator = communicator
        self.window = window

        self.isTracing = threading.Condition()  # a global lock to Control the thread of tracing the Sun
        self.traceThread = threading.Thread(target=self.doTrace, daemon=True)
        self.traceThread.start()

    def trace(self):
        # self.resetB.setEnabled(False)
        # self.traceB.setEnabled(False)
        self.traceFlag = True
        self.isTracing.acquire()
        self.isTracing.notify()
        self.isTracing.release()

    def stopTrace(self):
        # self.traceB.setEnabled(True)
        # self.resetB.setEnabled(True)
        self.traceFlag = False

    def doTrace(self):
        while True:
            # if traceFlag is True, the doTrace thread will wait for notification
            if not self.traceFlag:
                self.isTracing.acquire()
                self.isTracing.wait()
                self.isTracing.release()
            # tracing
            ha, dec = self.window.getPosition()
            print("tracing %f, %f" % (ha, dec))
            self.communicator.point(ha, dec)

    def drop_power(self):
        self.communicator.drop_power()

    def stop(self):
        self.communicator.stop()

    # def ccw(self):
    #     self.communicator.commdSpwOr(speed=0, orient='ccw')

    def reset(self):
        self.communicator.reset()


class Keyboard(object):
    window = None
    ui_form = None

    def __init__(self, window):
        self.window = window
        self.ui_form = window.ui_form
        self.ui_form.upButton.clicked.connect(self.up)
        self.ui_form.downButton.clicked.connect(self.down)
        self.ui_form.cwButton.clicked.connect(self.cw)
        self.ui_form.ccwButton.clicked.connect(self.ccw)

    def ccw(self):
        base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
        self.window.haManualCalibrateOffset.ha_offset += base

    def cw(self):
        base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
        self.window.haManualCalibrateOffset.ha_offset -= base

    def up(self):
        base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
        self.window.decManualCalibrateOffset.decOffset += base

    def down(self):
        base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
        self.window.decManualCalibrateOffset.decOffset -= base

# class Keyboard(object):
#     window = None
#     ui_form = None
#
#     def __init__(self, window):
#         self.window = window
#         self.ui_form = window.ui_form
#         self.ui_form.upButton.clicked.connect(self.up)
#         self.ui_form.downButton.clicked.connect(self.down)
#         self.ui_form.cwButton.clicked.connect(self.cw)
#         self.ui_form.ccwButton.clicked.connect(self.ccw)
#
#     def ccw(self):
#         base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
#         self.window.haManualCalibrateOffset.ha_offset += base
#
#     def cw(self):
#         base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
#         self.window.haManualCalibrateOffset.ha_offset -= base
#
#     def up(self):
#         base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
#         self.window.decManualCalibrateOffset.decOffset += base
#
#     def down(self):
#         base = self.ui_form.speedSpinBox.value() / constants.SPEED_MAX
#         self.window.decManualCalibrateOffset.decOffset -= base
