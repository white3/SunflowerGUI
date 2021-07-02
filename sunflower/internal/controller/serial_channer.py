#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/16 23:03
# @Author  : Menzel3
# @Site    : 
# @File    : serial_channer.py
# @Software: PyCharm
# @version : 0.0.1
import traceback

from sunflower.internal.constants import constant
from PyQt5.QtWidgets import QApplication
from sunflower.internal.controller import status
import time

from sunflower.internal.controller.controller import Controller


class SerialController(Controller):
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
        self.data.get('ser').port = constant.port
        # self.view.comNumberSpinBox.valueChanged.connect(self.work)
        self.view.comButton.clicked.connect(self.work)

    def work(self):
        time.sleep(constant.SERIAL_FLUSH_TIME)
        port = "COM" + str(self.view.comNumberSpinBox.value())

        if self.data.get('ser').port != port:  # 更换端口前，如果旧端口还连接,则先断开
            self.data.get('ser').close()
            self.data.get('ser').port = port  # 更换端口
        # 未更换端口
        # 已连接则进行探活
        try:
            QApplication.processEvents()
            self.data.get('ser').open()  # 尝试连接
            # 连接成功：界面蓝色，线程睡眠
            status.status_log("connect success", constant.MEDIUM)
            self.view.comNumberSpinBox.setStyleSheet("color: #00aaff;border: 2px solid #707070;")
            # self.wait()
        except Exception:
            # 连接失败：输出异常，界面显示红色    print(e)
            status.status_log(traceback.format_exc(), constant.HIGH)
            print(traceback.format_exc())
            self.view.comNumberSpinBox.setStyleSheet("color: #aa0000;border: 2px solid #707070;")
