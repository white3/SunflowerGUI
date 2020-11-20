#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 8:30
# @Author  : Menzel3
# @Site    : 
# @File    : test_process.py
# @Software: PyCharm
# @version : 0.0.1
import multiprocessing

import pandas as pd
import numpy as np
import math

# 读出ra,dec,pmra,pmraerr,pmdec,pmdecerr,para,paraerr这些数据
csv_data = pd.read_csv("D:\qsodata\meanfivedeg.csv")
vsh_data = np.array(csv_data)

# 将这些数据各自分为独立数组
ra = vsh_data[:, 0]
dec = vsh_data[:, 1]
pmra = vsh_data[:, 2]
pmraerr = vsh_data[:, 3]
pmdec = vsh_data[:, 4]
pmdecerr = vsh_data[:, 5]
para = vsh_data[:, 6]
paraerr = vsh_data[:, 7]
l = len(ra)
# n = {}
result1 = np.zeros(l)
result2 = np.zeros(l)
result3 = np.zeros(l)


def func(left, right, l, ra, dec, pmra, pmraerr, pmdecerr, para, paraerr, result1, result2, result3):
    for i in range(left, right):
        r = np.array([math.cos(math.radians(ra[i])) * math.cos(math.radians(dec[i])),
                      math.sin(math.radians(ra[i])) * math.cos(math.radians(dec[i])),
                      math.sin(math.radians(dec[i]))], dtype='d')
        h = 0
        n = {}
        for j in range(0, l):
            d = np.array([math.cos(math.radians(ra[j])) * math.cos(math.radians(dec[j])),
                          math.sin(math.radians(ra[j])) * math.cos(math.radians(dec[j])),
                          math.sin(math.radians(dec[j]))], dtype='d')
            cosangel = np.dot(r, d) / (np.linalg.norm(r) * np.linalg.norm(d))

            if 0.996194698 <= cosangel <= 1.1:
                n[h] = j
                h = h + 1

        x = np.array([pmra[k] for k in n], dtype='d')
        y = np.array([pmraerr[k] for k in n], dtype='d')
        if y[0] == 0:
            result1[i] = pmra[i]
        else:
            y = 1 / y ** 2
            result1[i] = np.average(x, weights=y)

        x = np.array([pmdec[k] for k in n], dtype='d')
        y = np.array([pmdecerr[k] for k in n], dtype='d')
        if y[0] == 0:
            result2[i] = pmdec[i]
        else:
            y = 1 / y ** 2
            result2[i] = np.average(x, weights=y)

        x = np.array([para[k] for k in n], dtype='d')
        y = np.array([paraerr[k] for k in n], dtype='d')

        if y[0] == 0:
            result3[i] = para[i]
        else:
            y = 1 / y ** 2
            result3[i] = np.average(x, weights=y)
        print('[+]', i)
    write(result1, result2, result3, left, right)


def write(result1, result2, result3, left, right):
    csv_data['pmramean'] = result1
    csv_data['pmdecmean'] = result2
    csv_data['paramean'] = result3
    # csv_data.to_csv('D:\qsodata\meanfiveresult_latest-%d-%d.csv' % (left, right), mode='a', header=True, index=False)


if __name__ == '__main__':
    thread_num = multiprocessing.Value('i', 10)
    temp = math.ceil(l / thread_num.value)
    for num in range(thread_num.value - 1):
        p = multiprocessing.Process(target=func, args=(
            num * temp, (num + 1) * temp, l, ra, dec, pmra, pmraerr, pmdecerr, para, paraerr, result1, result2,
            result3), daemon=True)
        p.start()
        p.join()
    p = multiprocessing.Process(target=func, args=(
        (thread_num.value - 1) * temp, l, l, ra, dec, pmra, pmraerr, pmdecerr, para, paraerr, result1, result2,
        result3), daemon=True)
    p.start()
    p.join()
