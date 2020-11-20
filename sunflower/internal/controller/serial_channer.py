#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/16 23:03
# @Author  : Menzel3
# @Site    : 
# @File    : serial_channer.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.constants import constant
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.controller import status
import time


class SerialController(interruptible_thread.ThreadMeta):

    @status.status_log("init SerialController", constant.MEDIUM)
    def __init__(self, **kwargs):
        interruptible_thread.ThreadMeta.__init__(self)
        self.data = kwargs['data']
        self.view = kwargs['view']
        self.data['ser'].port = constant.port
        self.data['ser'].baudrate = constant.baudrate
        self.view['comNumberSpinBox'].valueChanged.connect(self.work)

    def work(self):
        time.sleep(constant.VIEW_FLUSH_TIME)
        port = "COM" + str(self.view['comNumberSpinBox'].value())
        self.data['ser'].port = port
        if not self.data['ser'].is_open:
            self.view['comNumberSpinBox'].setStyleSheet("color: #aa0000;border: 2px solid #707070;")
