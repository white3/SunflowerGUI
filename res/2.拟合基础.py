#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 23:16
# @Author  : Menzel3
# @Site    : 
# @File    : 2.拟合基础.py
# @Software: PyCharm
# @version : 0.0.1
from context import *


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
    # kinds = ['linear', 'nearest', 'previous', 'next']

    xnew = np.linspace(scale[0], scale[1], num=200)
    for kind in kinds:
        f = interpolate.interp1d(x, y, kind=kind, fill_value="extrapolate")
        ynew = f(xnew)
        pl.plot(xnew, ynew, label=str(kind))
    pl.xticks(fontsize=20)
    pl.xticks(fontsize=20)
    pl.legend(loc='lower right')
    pl.show()


if __name__ == "__main__":
    # 望远镜RA   望远镜DEC   RA_offset   DEC_offset
    ra = [23.76153215391256, 31.168754830018017, 31.853349116583416, 36.26792003332821, 38.68135271905504,
          41.260941232476746, 43.448195137480454, 45.61301352630765, 48.27885959218019, 50.34754611973788]
    offset_ra = [19.0, 19.0, 19.5, 19.25, 19.1, 18.9, 18.9, 18.9, 18.85, 18.85]
    ra_scale = [23, 51]
    fit_test(ra, offset_ra, ra_scale)

    dec = [-3.3922330810514882, -3.4001945563262996, -3.4009302916765476, -3.4056743106063454, -3.408267613265428,
           -3.4110392743056757, -3.413389245283975, -3.4157149860054545, -3.4185788314731047, -3.4208010416085095]
    offset_dec = [7.5, 8.5, 8.8, 9.0, 9.3, 9.5, 9.7, 9.8, 10.05, 10.15]
    dec_scale = [-3.5, -3.3]
    # fit_test(dec, offset_dec, dec_scale)
