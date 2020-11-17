#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 19:33
# @Author  : Menzel3
# @Site    : 
# @File    : test_times.py
# @Software: PyCharm
# @version : 0.0.1
from sunflower.internal.model.times import *
import unittest


class TestStringMethods(unittest.TestCase):
    test_time = datetime.utcfromtimestamp(1605347977.211388)
    t = Times(utc=test_time)
    def test_time_convert(self):
        self.assertTrue(([23.76153215391256, ], [19.0, ]), self.t.toUTC())
        self.assertTrue(([23.76153215391256, ], [19.0, ]), self.t.toLST())
        self.assertTrue(([23.76153215391256, ], [19.0, ]), self.t.toLocalTime())


if __name__ == '__main__':
    unittest.main()
