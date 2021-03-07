#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 23:10
# @Author  : Menzel3
# @Site    :
# @File    : corrector.py
# @Software: PyCharm
# @version : 0.0.1
import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pylab as pl
from sunflower.internal.controller.recorder import Recorder, HA, DEC
from sunflower.internal.meta import interruptible_thread
from sunflower.internal.constants import constant
from sunflower.internal.controller import status
import time


def takeFirst(elem):
    return elem[0]


class CorrectorController(interruptible_thread.ThreadMeta):

    @status.status_log("Setup corrector controller", constant.MEDIUM)
    def __init__(self, **kwargs):
        interruptible_thread.ThreadMeta.__init__(self)
        self.view = kwargs['view']
        self.data = kwargs['data']
        self.isCorrect = False  # 是否开启指向修正
        self.recorder = Recorder()
        self.corrector = Corrector(recorder=self.recorder)
        self.view['correctButton'].clicked.connect(self.correct)
        self.view['updateCorrectionButton'].clicked.connect(self.corrector.update)
        self.work()

    # @status.status_log("开始修正", constant.MEDIUM)
    def correct(self):
        """
        Correct 事件业务
        :return:
        """
        self.run()

    def fitHA(self, ha):
        """
        获取差值最小的索引 np.abs(self.offsetMap['angle'] - 6).argmin()
        返回该索引对应的haOffset

        :param ha:
        :return:
        """
        return self.corrector.fitHA(ha)

    def fitDEC(self, dec):
        """
        获取差值最小的索引 np.abs(self.offsetMap['angle'] - 6).argmin()
        返回该索引对应的haOffset

        :param dec:
        :return:
        """
        return self.corrector.fitDEC(dec)

    def work(self):
        time.sleep(constant.CORRECT_FLUSH_TIME)
        self.data['haFitOffset'].offset = self.corrector.fitHA(self.data['haFitOffset'].angle)
        self.data['decFitOffset'].offset = self.corrector.fitDEC(self.data['decFitOffset'].angle)


class Corrector(object):
    def __init__(self, recorder: Recorder):
        # TODO 配置mod的选择于GUI上
        self.modes = ['linear', 'nearest', 'previous', 'next', 'zero', 'slinear', 'quadratic', 'cubic', 5, 7]
        self.kind = 'quadratic'
        self.recorder = recorder
        self.offsetMap = {}

    def _cleanDuplicates(self, offset_packages: list):
        """
        筛选数据

        :param offset_packages: [[angles: 角度数组, offsets: 误差数组, globalClocks: 全局时钟数组, versions: 版本数组], ]
        :return:
        """
        # 排序
        offset_packages.sort(key=takeFirst)
        temp = 1  # 数组之间的差值
        angles, offsets = [offset_packages[0][0]], [offset_packages[0][1]]
        global_clock, version = offset_packages[0][2], offset_packages[0][3]
        # 去重
        for i in range(1, len(offset_packages) - 1):
            if angles[i - temp] == offset_packages[i][0]:
                if version < offset_packages[i][3]:
                    angles[i - temp] = offset_packages[i][0]
                    offsets[i - temp] = offset_packages[i][2]
                elif version > offset_packages[i][3]:
                    pass
                else:
                    if global_clock < offset_packages[i + 1][2]:
                        angles[i - temp] = offset_packages[i][0]
                        offsets[i - temp] = offset_packages[i][1]
                    else:
                        pass
                temp += 1
            else:
                angles.append(offset_packages[i][0])
                offsets.append(offset_packages[i][1])
                global_clock = offset_packages[i][2]
                version = offset_packages[i][3]
        return angles, offsets

    def __fit(self, x: list, y: list, scale: list):
        """

        :param x: x的值的列表
        :param y: y的值的列表
        :param scale: [0, 100, 300] 表示将导出拟合后[0, 100]之间均匀的300个数
        :return:
        """
        # 开始拟合
        variable = np.linspace(scale[0], scale[1], num=scale[2])
        f = interpolate.interp1d(x, y, kind=self.kind, fill_value="extrapolate")
        values = f(variable)
        return np.array(variable), np.array(values)

    def changeMod(self, fit_mod):
        """

        :param fit_mod: 拟合方式
        :return:
        """
        self.kind = fit_mod

    def update(self):
        """
        重新生成拟的修正图
        :return:
        """
        # 筛选数据
        ha_list = self.recorder.readData(kind=HA)
        dec_list = self.recorder.readData(kind=DEC, scale=(-90, 90))
        has, haOffsets = self._cleanDuplicates(ha_list)
        decs, decOffsets = self._cleanDuplicates(dec_list)

        self.offsetMap['ha'], self.offsetMap['haOffset'] = self.__fit(x=has, y=haOffsets, scale=[-180, 180, 3600])
        self.show(x=self.offsetMap['ha'], y=self.offsetMap['haOffset'], title='ro')
        self.offsetMap['dec'], self.offsetMap['decOffset'] = self.__fit(x=decs, y=decOffsets, scale=[-90, 90, 1800])
        self.show(self.offsetMap['dec'], self.offsetMap['decOffset'], 'ro')
        status.display_status("修正完毕", constant.MEDIUM)
        # try:
        # except ValueError as e:
        #     print("data of angle is too less")
        # try:
        # except ValueError as e:
        #     print("data of angle is too less")

    def fitHA(self, ha: float):
        """
        获取差值最小的索引 np.abs(self.offsetMap['angle'] - 6).argmin()
        返回该索引对应的haOffset

        :param ha:
        :return:
        """
        return self.offsetMap['haOffset'][np.abs(self.offsetMap['ha'] - ha).argmin()]

    def fitDEC(self, dec: float):
        """
        获取差值最小的索引 np.abs(self.offsetMap['angle'] - 6).argmin()
        返回该索引对应的haOffset

        :param dec:
        :return:
        """
        return self.offsetMap['decOffset'][np.abs(self.offsetMap['dec'] - dec).argmin()]

    def show(self, x, y, title='ro'):
        pl.figure(figsize=(10, 10))
        pl.plot(x, y, title)
        pl.show()
