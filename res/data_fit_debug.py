#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 23:35
# @Author  : Menzel3
# @Site    :
# @File    : 4.指定函数拟合求参数.py
# @Software: PyCharm
# @version : 0.0.1

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import *
import numpy as np


def fit_ha(angles, offset_ras):
    # print(angles)
    popt, pcov = curve_fit(correct_ha, angles, offset_ras)  # 训练函数
    Ca, Sa, y, miu, qingxiex, qingxiey, zcb1, zcb2, zcb3, zcb4 = popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], \
                                                                 popt[
                                                                     6], popt[7], popt[8], popt[9]
    yvals = correct_ha(angles, Ca, Sa, y, miu, qingxiex, qingxiey, zcb1, zcb2, zcb3, zcb4)
    plot1 = plt.plot(ra, offset_ra, '*', label='original values')
    plot2 = plt.plot(ra, yvals, 'r', label='curve_fit values')
    plt.xlabel('ra axis')
    plt.ylabel('offset_ra axis')
    plt.legend(loc=4)
    plt.title('curve_fit')
    plt.show()
    print(Ca, Sa, y, miu, qingxiex, qingxiey, zcb1, zcb2, zcb3, zcb4)


def fit_dec(angles, offset_ras):
    # print(angles)
    popt, pcov = curve_fit(correct_dec, angles, offset_ras)  # 训练函数
    Ce, Se, qingxiex, qingxiey, zcb3, zcb4 = popt[0], popt[1], popt[2], popt[3], popt[4], popt[5]
    yvals = correct_dec(angles, Ce, Se, qingxiex, qingxiey, zcb3, zcb4)
    plot1 = plt.plot(ra, offset_ra, '*', label='original values')
    plot2 = plt.plot(ra, yvals, 'r', label='curve_fit values')
    plt.xlabel('ra axis')
    plt.ylabel('offset_ra axis')
    plt.legend(loc=4)
    plt.title('curve_fit')
    plt.show()
    print(Ce, Se, qingxiex, qingxiey, zcb3, zcb4)


def correct_dec(angles, Ce, Se, qingxiex, qingxiey, zcb3, zcb4):
    """
    offset_dec = Ce + Se *  dec - qingxiex * cos(ra) + qingxiey * sin(ra) - zcb3 * cos(ra) * cos(ra)
        - zcb4 * cos(ra) * sin(ra) + odec
    :param angles:
    :param C:
    :return:
    """
    ra, dec = angles[0], angles[1]
    return Ce + Se * dec - qingxiex * cos(ra) + qingxiey * sin(ra) - zcb3 * cos(ra) * cos(ra) - zcb4 * cos(ra) * sin(
        ra)


def correct_ha(angles, Ca, Sa, y, miu, qingxiex, qingxiey, zcb1, zcb2, zcb3, zcb4):
    """
    offset_ra = Ca + Sa * ra + y * sec(dec) - miu * tan(dec) - qingxiex * sin(ra) * tan(dec) - qingxiey * cos(ra) * tan(dec) + zcb1 * sin(dec)
    + zcb2 * cos(dec) - zcb3 * cos(ra) * sin(ra) * tan(dec) - zcb4 * cos(ra) *cos(ra) * tan(dec) + ora
    :param angles:
    :param Ca:
    :param Sa:
    :param y:
    :param miu:
    :param qingxiex:
    :param qingxiey:
    :param zcb1:
    :param zcb2:
    :param zcb3:
    :param zcb4:
    :return:
    """
    ra, dec = angles[0], angles[1]
    return Ca + Sa * ra + y / cos(dec) - miu * tan(dec) - qingxiex * sin(ra) * tan(dec) - qingxiey * cos(ra) * tan(
        dec) + zcb1 * sin(dec) + zcb2 * cos(dec) - zcb3 * cos(ra) * sin(ra) * tan(dec) - zcb4 * cos(ra) * cos(ra) * tan(
        dec)  # + o

    # 望远镜RA   望远镜DEC   RA_offset   DEC_offset

from data_processor import query_ha, query_dec
# from data_fit_debug import fit_ha, fit_dec

if __name__ == '__main__':
    angles = []
    ra, offset_ra = query_ha()
    dec, offset_dec = query_dec()
    for i in range(len(ra)):
        angles.append([ra[i], dec[i]])
    angles = np.array(angles)
    print(angles)
    # fit_ha(angles, np.array(offset_ra))

    fit_dec(angles, np.array(offset_dec))
