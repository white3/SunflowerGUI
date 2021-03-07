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
from PyQt5.QtWidgets import QApplication
from sunflower.internal.controller import status
import time


# class SerialController(interruptible_thread.ThreadMeta):
class SerialController(object):
    """
    1. 未连接时: 扫描当前，尝试连接
    2. 已连接时: 扫描间隔加长，保持探活
    3. 切换端口: 需要点击一次再尝试连接新端口
    :return:
    """

    @status.status_log("init SerialController", constant.MEDIUM)
    def __init__(self, **kwargs):
        # interruptible_thread.ThreadMeta.__init__(self)
        self.data = kwargs['data']
        self.view = kwargs['view']
        self.data['ser'].port = constant.port
        # self.view['comNumberSpinBox'].valueChanged.connect(self.work)
        self.view['comButton'].clicked.connect(self.work)

    def work(self):
        time.sleep(constant.SERIAL_FLUSH_TIME)
        port = "COM" + str(self.view['comNumberSpinBox'].value())

        if self.data['ser'].port != port:  # 更换端口前，如果旧端口还连接,则先断开
            self.data['ser'].close()
            self.data['ser'].port = port  # 更换端口
        # 未更换端口
        # 已连接则进行探活
        try:
            QApplication.processEvents()
            self.data['ser'].open()  # 尝试连接
            # 连接成功：界面蓝色，线程睡眠
            status.status_log("connect success", constant.MEDIUM)
            self.view['comNumberSpinBox'].setStyleSheet("color: #00aaff;border: 2px solid #707070;")
            # self.wait()
        except Exception as e:
            # 连接失败：输出异常，界面显示红色    print(e)
            status.status_log(e, constant.HIGH)
            print(e)
            self.view['comNumberSpinBox'].setStyleSheet("color: #aa0000;border: 2px solid #707070;")
