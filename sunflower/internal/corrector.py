# -*- coding: utf-8 -*-
import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pylab as pl
from sunflower.internal.recorder import Recorder, HA, DEC


class Corrector(object):
    def __init__(self, recorder: Recorder):
        # TODO 配置mod的选择于GUI上
        self.modes = ['linear', 'nearest', 'previous', 'next', 'zero', 'slinear', 'quadratic', 'cubic', 5, 7]
        self.kind = 'quadratic'
        self.recorder = recorder
        self.offsetMap = {}

    def fit(self, x: list, y: list, scale: list):
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

    def changeMod(self, fitmod):
        self.fitmod = fitmod

    def update(self):
        has, haOffsets = self.recorder.readData(kind=HA)
        decs, decOffsets = self.recorder.readData(kind=DEC)
        self.offsetMap['ha'], self.offsetMap['haOffset'] = self.fit(x=has, y=haOffsets, scale=[-180, 180, 3600])
        self.offsetMap['dec'], self.offsetMap['decOffset'] = self.fit(x=decs, y=decOffsets, scale=[-90, 90, 1800])

    def fitHA(self, ha):
        # 获取差值最小的索引 np.abs(self.offsetMap['ha'] - 6).argmin()
        # 返回该索引对应的haOffset
        return self.offsetMap['haOffset'][np.abs(self.offsetMap['ha'] - ha).argmin()]

    def fitDEC(self, dec):
        # 获取差值最小的索引 np.abs(self.offsetMap['ha'] - 6).argmin()
        # 返回该索引对应的haOffset
        return self.offsetMap['decOffset'][np.abs(self.offsetMap['dec'] - dec).argmin()]


def show_data(dec, offset_dec):
    import pprint
    pl.figure(figsize=(10, 10))
    pprint.pprint(dec)
    pprint.pprint(offset_dec)
    pl.plot(dec, offset_dec, 'ro')
    pl.show()


def fit_test(x, y, scale):
    # 描绘数据
    pl.figure(figsize=(12, 9))
    pl.plot(x, y, 'ro')
    # 开始拟合    kinds = ['nearest', 'zero', 'linear', 'quadratic', 5]
    kinds = ['linear', 'nearest', 'previous', 'next', 'zero', 'slinear', 'quadratic', 'cubic', 5, 7]

    xnew = np.linspace(scale[0], scale[1], num=200)
    for kind in kinds:
        f = interpolate.interp1d(x, y, kind=kind, fill_value="extrapolate")
        ynew = f(xnew)
        pl.plot(xnew, ynew, label=str(kind))
    pl.xticks(fontsize=20)
    pl.xticks(fontsize=20)
    pl.legend(loc='lower right')
    pl.show()


def fourier(x, *a):
    w = 2 * np.pi / 200
    ret = 0
    for deg in range(0, int(len(a) / 2) + 1):
        ret += a[deg] * np.cos(deg * w * x) + a[len(a) - deg - 1] * np.sin(deg * w * x)
    return ret


def fourierfit(x, y, xlims, ylims):
    popt, pcov = curve_fit(fourier, x, y, [1.0] * 100)
    plt.ylim(xlims[0], xlims[1])
    plt.xlim(ylims[0], ylims[1])
    plt.plot(x, y, color='r', label="original")
    plt.plot(x, fourier(x, *popt), color='g', label="fitting")
    plt.legend()
    plt.show()
    return popt


def demo_fourierfit():
    x = np.arange(1, 201, 1)
    print(x)
    y = [490, 477, 467, 458, 450, 442, 433, 426, 419, 413, 411, 428, 445, 441, 434, 436, 446, 442, 427, 414, 402,
         391, 381, 372, 366, 363, 363, 364, 366, 372, 382, 397, 414, 430, 444, 460, 481, 502, 522, 539, 551, 561,
         567, 569, 568, 566, 570, 576, 578, 574, 565, 553, 541, 529, 519, 507, 496, 486, 494, 528, 551, 563, 576,
         596, 612, 624, 631, 636, 639, 640, 640, 638, 635, 633, 630, 625, 620, 615, 609, 603, 597, 590, 584, 578,
         571, 559, 541, 529, 524, 511, 486, 454, 422, 394, 372, 348, 340, 335, 334, 332, 332, 332, 332, 332, 333,
         336, 339, 341, 344, 349, 355, 360, 366, 372, 383, 396, 408, 419, 432, 448, 463, 473, 482, 493, 511, 530,
         551, 568, 580, 595, 597, 597, 595, 593, 598, 606, 619, 632, 642, 653, 659, 658, 653, 645, 640, 641, 643,
         650, 656, 659, 659, 655, 649, 640, 632, 626, 621, 614, 603, 590, 575, 564, 550, 530, 519, 507, 495, 484,
         472, 462, 452, 445, 437, 430, 423, 417, 423, 442, 445, 435, 423, 422, 431, 436, 428, 413, 401, 390, 381,
         373, 367, 363, 364, 365, 367, 371, 378, 396, 411, 428]
    print(len(y))
    y = np.array(y)
    popt = fourierfit(x, y, [0, 700], [0, 200])
    print("参数如下：")
    print(popt)


if __name__ == "__main__":
    # 望远镜RA   望远镜DEC   RA_offset   DEC_offset
    ra = [23.76153215391256, 31.168754830018017, 31.853349116583416, 36.26792003332821, 38.68135271905504,
          41.260941232476746, 43.448195137480454, 45.61301352630765, 48.27885959218019, 50.34754611973788]
    offset_ra = [19.0, 19.0, 19.5, 19.25, 19.1, 18.9, 18.9, 18.9, 18.85, 18.85]
    ra_scale = [23, 51]

    fit_test(ra, offset_ra, ra_scale)
    # popt = fourierfit(ra, offset_ra, [20, 50], [18, 20])
    # print("参数如下：")
    # print(popt)

    dec = [-3.3922330810514882, -3.4001945563262996, -3.4009302916765476, -3.4056743106063454, -3.408267613265428,
           -3.4110392743056757, -3.413389245283975, -3.4157149860054545, -3.4185788314731047, -3.4208010416085095]
    offset_dec = [7.5, 8.5, 8.8, 9.0, 9.3, 9.5, 9.7, 9.8, 10.05, 10.15]
    dec_scale = [-4, -3]

    # fit_test(dec, offset_dec, dec_scale)

# def demo1():
#     # 描绘数据
#     pl.figure(figsize=(12, 9))
#     x = np.linspace(0, 10, 11)
#     y = np.sin(x)
#
#     # 开始拟合
#     kinds = ['nearest', 'zero', 'linear', 'quadratic', 5]
#
#     xnew = np.linspace(0, 10, 101)
#     for kind in kinds:
#         f = interpolate.interp1d(x, y, kind=kind)
#         ynew = f(xnew)
#         pl.plot(xnew, ynew, label=str(kind))
#     pl.xticks(fontsize=20)
#     pl.xticks(fontsize=20)
#     pl.legend(loc='lower right')
#     pl.show()
#
# def plotx(x, y):
#     # 描绘数据
#     pl.figure(figsize=(12, 9))
#     # x = np.linspace(0, 10, 11)
#     # y = np.sin(x)
#     pl.plot(x, y, 'ro')
#     pl.show()
