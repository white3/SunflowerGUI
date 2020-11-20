import threading

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
n = {}
result1 = np.zeros(l)
result1_lock = threading.Condition()
result2 = np.zeros(l)
result2_lock = threading.Condition()
result3 = np.zeros(l)
result3_lock = threading.Condition()

writing = threading.Condition()
thread_num = 0


def func(left, right):
    global l, ra, dec, pmra, pmraerr, pmdecerr, para, paraerr, result1, result2, result3
    for i in range(left, right):
        r = np.array([math.cos(math.radians(ra[i])) * math.cos(math.radians(dec[i])),
                      math.sin(math.radians(ra[i])) * math.cos(math.radians(dec[i])),
                      math.sin(math.radians(dec[i]))], dtype='d')
        h = 0
        n.clear()
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
        with result1_lock:
            if y[0] == 0:
                result1[i] = pmra[i]
            else:
                y = 1 / y ** 2
                result1[i] = np.average(x, weights=y)

        x = np.array([pmdec[k] for k in n], dtype='d')
        y = np.array([pmdecerr[k] for k in n], dtype='d')
        with result2_lock:
            if y[0] == 0:
                result2[i] = pmdec[i]
            else:
                y = 1 / y ** 2
                result2[i] = np.average(x, weights=y)

        x = np.array([para[k] for k in n], dtype='d')
        y = np.array([paraerr[k] for k in n], dtype='d')

        with result3_lock:
            if y[0] == 0:
                result3[i] = para[i]
            else:
                y = 1 / y ** 2
                result3[i] = np.average(x, weights=y)
        print(i)
    funcs(left, right)


def funcs(a, b):
    print(a, b)
    with writing:
        global thread_num
        thread_num -= 1
        if thread_num == 0:
            writing.notifyAll()


def write():
    global result1, result2, result3
    with writing:
        writing.wait()
    # print(True)
    csv_data['pmramean'] = result1
    csv_data['pmdecmean'] = result2
    csv_data['paramean'] = result3
    csv_data.to_csv('D:\qsodata\meanfiveresult_latest.csv', mode='a', header=True, index=False)


if __name__ == '__main__':
    thread_num = int(input('num:'))
    temp = math.ceil(l / thread_num)
    write_thread = threading.Thread(target=write, daemon=True)
    write_thread.start()
    for num in range(thread_num - 1):
        threading.Thread(target=func, args=(num * temp, (num + 1) * temp), daemon=True).start()
    threading.Thread(target=func, args=((thread_num - 1) * temp, l), daemon=True).start()
    write_thread.join()
