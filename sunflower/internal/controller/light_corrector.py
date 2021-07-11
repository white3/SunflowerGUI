#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 23:10
# @Author  : Menzel3
# @Site    :
# @File    : corrector.py
# @Software: PyCharm
# @version : 0.0.1
import numpy as np
import qimage2ndarray
from PyQt5.QtGui import QPixmap

from sunflower.internal.controller.controller import ConController
import cv2
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.constants import constant
from sunflower.internal.controller import status
import time


class LightCalibrateController(ConController):

    @status.status_log("Setup light corrector controller", constant.MEDIUM)
    def __init__(self, **kwargs):
        interruptible_thread.ThreadMeta.__init__(self)
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.isCorrect = False  # 是否开启指向修正
        self.view.lightCorrectButton.clicked.connect(self.correct)
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, constant.camera_width)  # 设置帧宽
        self.cap.set(4, constant.camera_height)  # 设置帧高
        self.font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
        self.kernel = np.ones((5, 5), np.uint8)  # 卷积核

    def __del__(self):
        self.cap.release()

    def correct(self):
        """
        Correct 事件业务
        :return:
        """
        if self.isCorrect:
            self.view.lightCorrectButton.setText('启动修正')
            self.isCorrect = False
            self.wait()
        else:
            self.view.lightCorrectButton.setText('关闭修正')
            self.isCorrect = True
            self.run()

    def work(self):
        """
        通过 cv 识别图像获取offset
        1. 将图像贴在 qt5上
        2. 计算图像误差
        130度, 中心30%放大

        :return:
        """
        time.sleep(constant.CORRECT_FLUSH_TIME)
        haFitOffset = self.data.get('haFitOffset')
        decFitOffset = self.data.get('decFitOffset')

        if self.cap.isOpened() is True:  # 检查摄像头是否正常启动
            ret, frame = self.cap.read()

            # 将图像贴在 qt5上
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰色通道

            #  消除噪声
            gray = cv2.GaussianBlur(gray, ksize=(constant.radius, constant.radius), sigmaX=0)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
            cv2.circle(frame, maxLoc, constant.radius, (255, 0, 255), 10)
            offset = [
                (constant.camera_center[0] - maxLoc[0]) * constant.camera_alpha_width_percentage,
                (constant.camera_center[1] - maxLoc[1]) * constant.camera_alpha_height_percentage, ]

            if constant.is_debug:
                print("需顺移 x_offset: %s, 需上移 y_offset: %s" % (offset[0], offset[1]))

            # 需要偏转的,
            # if haFitOffset.offset * offset[0] > 0 and haFitOffset.offset = offset[0]
            haFitOffset.offset = offset[0]
            decFitOffset.offset = offset[1]

            image = qimage2ndarray.array2qimage(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            pixmap = QPixmap.fromImage(image)
            # 211, 190
            pixmap_resized = pixmap.scaled(211, 190)
            self.view.graphicsView.setPixmap(pixmap_resized)

        else:
            print('cap is not opened!')

        self.data.set('haFitOffset', haFitOffset)
        self.data.set('decFitOffset', decFitOffset)
